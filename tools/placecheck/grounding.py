"""placecheck engine: vectorised terrain sampling, per-category grounding checks, object-on-object host tests
and the incremental cache.

Terrain: an 8WVR-style heightmap h[j, i] (row 0 = SOUTH), vertex (i, j) at x = i*cell, z = j*cell, sampled
bilinearly exactly like spikes/T_terrain/tools/terrain.py bilinear() (the engine's two triangles per cell differ by a
few cm on smooth slopes, nothing on flat ground).

Objects: an ObjSet of numpy arrays, one row per object. M[n, 12] = aside(3), up(3), dir(3), pos(3), the .wrp
matrix layout; scale is inside aside/up/dir. A model-frame point (x, y, z) lands at pos + x*aside + y*up + z*dir.

Cache: every object gets a 64-bit key = hash(model profile SHA-1, category rules, its 12 matrix floats, the hashes of
the terrain tiles under its footprint, and for host-supported categories the hash of every host in its grid cells).
Results are stored per key in data/placecheck/cache_<scope>.npz; a rerun re-checks only keys it has not seen:
moved objects, changed models or rules, edited terrain tiles, moved hosts.
"""
import math
import os
import time

import numpy as np

from model import CACHE

ENGINE_VERSION = 3
F_FLOAT, F_SINK, F_EMBED, F_NOHOST, F_NOPROFILE, F_SKIP, F_HOST, F_ROAD = 1, 2, 4, 8, 16, 32, 64, 128
FLAG_TEXT = {F_FLOAT: "floats", F_SINK: "sunk too deep", F_EMBED: "buried above ground line", F_NOHOST: "no host",
             F_NOPROFILE: "no model profile", F_SKIP: "not checked", F_HOST: "on host", F_ROAD: "road off terrain"}
TILE = 64            # heightmap vertices per cache tile
HOST_CELL = 64.0     # metres, host lookup grid
PROBE_UP = 0.5       # a supported sample looks for a host floor up to this far above itself

M64 = np.uint64(0x9E3779B97F4A7C15)


def _mix(h):
    h = h ^ (h >> np.uint64(33))
    h = h * np.uint64(0xFF51AFD7ED558CCD)
    h = h ^ (h >> np.uint64(33))
    h = h * np.uint64(0xC4CEB9FE1A85EC53)
    return h ^ (h >> np.uint64(33))


def combine(h, v):
    with np.errstate(over="ignore"):
        return _mix((h ^ v.astype(np.uint64)) * M64 + np.uint64(0x632BE59BD9B4E019))


# ------------------------------------------------------------------------------------------ terrain
class Terrain:
    def __init__(self, h, cell):
        self.h = np.ascontiguousarray(h, np.float32)
        self.n = self.h.shape[0]
        self.cell = float(cell)
        self.flat = self.h.ravel()
        self._tiles = None

    def sample(self, x, z):
        fx = np.asarray(x, np.float32) / np.float32(self.cell)
        fz = np.asarray(z, np.float32) / np.float32(self.cell)
        i = np.clip(np.floor(fx), 0, self.n - 2).astype(np.int32)
        j = np.clip(np.floor(fz), 0, self.n - 2).astype(np.int32)
        u = fx - i
        v = fz - j
        k = j * self.n + i
        h = self.flat
        a, b, c, d = h[k], h[k + 1], h[k + self.n], h[k + self.n + 1]
        return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v

    def tile_hashes(self):
        """uint64 per TILE x TILE block (plus the shared edge row/column)."""
        if self._tiles is None:
            nt = (self.n - 2) // TILE + 1
            out = np.zeros((nt, nt), np.uint64)
            for tj in range(nt):
                for ti in range(nt):
                    blk = self.h[tj * TILE:tj * TILE + TILE + 1, ti * TILE:ti * TILE + TILE + 1]
                    out[tj, ti] = np.frombuffer(__import__("hashlib").blake2b(blk.tobytes(), digest_size=8).digest(),
                                                np.uint64)[0]
            self._tiles = out
        return self._tiles

    def tiles_key(self, x0, z0, x1, z1):
        """Hash of the tiles under each AABB (up to 2 x 2 tiles; bigger boxes return 0 = always re-check)."""
        th = self.tile_hashes()
        nt = th.shape[0]
        span = TILE * self.cell
        ti0 = np.clip((x0 // span).astype(np.int64), 0, nt - 1)
        ti1 = np.clip((x1 // span).astype(np.int64), 0, nt - 1)
        tj0 = np.clip((z0 // span).astype(np.int64), 0, nt - 1)
        tj1 = np.clip((z1 // span).astype(np.int64), 0, nt - 1)
        k = combine(th[tj0, ti0], th[tj0, ti1])
        k = combine(k, th[tj1, ti0])
        k = combine(k, th[tj1, ti1])
        big = (ti1 - ti0 > 1) | (tj1 - tj0 > 1)
        k[big] = 0
        return k


# ------------------------------------------------------------------------------------------ objects
def yaw_matrix(yaw, pitch=0.0, roll=0.0, scale=1.0):
    """Same convention as spikes/T_terrain/tools/wrp8.py: yaw clockwise from north, +pitch = front up,
    +roll = right side up. Vectorised: returns (n, 9) aside|up|dir."""
    t, p, r = (np.radians(np.asarray(a, np.float64)) for a in (yaw, pitch, roll))
    c, s = np.cos(t), np.sin(t)
    z = np.zeros_like(c)
    aside = np.stack([c, z, -s], -1)
    up = np.stack([z, z + 1, z], -1)
    dirv = np.stack([s, z, c], -1)
    cp, sp = np.cos(p)[..., None], np.sin(p)[..., None]
    up, dirv = up * cp - dirv * sp, up * sp + dirv * cp
    cr, sr = np.cos(r)[..., None], np.sin(r)[..., None]
    aside, up = aside * cr + up * sr, -aside * sr + up * cr
    sc = np.asarray(scale, np.float64)[..., None]
    return np.concatenate([aside * sc, up * sc, dirv * sc], -1)


def matrix_angles(M):
    """(yaw, pitch, roll, scale) back from rows of M (inverse of yaw_matrix, exact for the yaw-only case)."""
    a, u, d = M[:, 0:3], M[:, 3:6], M[:, 6:9]
    sc = np.linalg.norm(u, axis=1)
    yaw = (np.degrees(np.arctan2(-a[:, 2], a[:, 0]))) % 360.0
    pitch = np.degrees(np.arcsin(np.clip(d[:, 1] / sc, -1, 1)))
    roll = np.degrees(np.arcsin(np.clip(a[:, 1] / sc, -1, 1)))
    return yaw, pitch, roll, sc


class ObjSet:
    """Objects to check. keys: (p3d, class) pairs; per object: M, key index, source file index, row."""

    def __init__(self):
        self.M = []
        self.kidx = []
        self.src = []
        self.row = []
        self.keys = []
        self._kmap = {}
        self.sources = []
        self._smap = {}

    def add(self, p3d, cls, M12, source, row):
        k = (p3d.lower(), (cls or "").lower())
        if k not in self._kmap:
            self._kmap[k] = len(self.keys)
            self.keys.append((p3d, cls or ""))
        if source not in self._smap:
            self._smap[source] = len(self.sources)
            self.sources.append(source)
        self.M.append(M12)
        self.kidx.append(self._kmap[k])
        self.src.append(self._smap[source])
        self.row.append(row)

    def freeze(self):
        self.M = np.asarray(self.M, np.float64).reshape(-1, 12)
        self.kidx = np.asarray(self.kidx, np.int32)
        self.src = np.asarray(self.src, np.int32)
        self.row = np.asarray(self.row, np.int32)
        return self

    def __len__(self):
        return len(self.kidx)


# ------------------------------------------------------------------------------------------ per-model check data
class KindInfo:
    """Everything the checks need for one (p3d, class): category, rule, local contact samples, meshes."""

    def __init__(self, p3d, cls, prof, cat, why, rule, rules):
        self.p3d, self.cls, self.prof, self.cat, self.why, self.rule = p3d, cls, prof, cat, why, rule
        self.S = None
        self.lod = ""
        self.gl = 0.0
        self.r_xz = 1.0
        ok = prof is not None and "error" not in prof
        self.hash = np.uint64(0)
        seed = "%s|%s|%s|%d" % (prof.get("sha1") if prof else "none", cat, rules["_hash"].get(cat, ""), ENGINE_VERSION)
        self.hash = np.frombuffer(__import__("hashlib").blake2b(seed.encode(), digest_size=8).digest(), np.uint64)[0]
        if not ok:
            if self.cat != "skip":
                self.cat = "noprofile"
            return
        self.gl = float(prof["mlod_origin"][1])
        bmin, bmax = np.array(prof["bmin"]), np.array(prof["bmax"])
        self.r_xz = float(max(np.abs(bmin[[0, 2]]).max(), np.abs(bmax[[0, 2]]).max()) * 1.42 + 0.5)
        if cat in ("plant", "rock", "building", "prop"):
            for kind in rule["contact_lods"]:
                P = prof.get("low_" + kind)
                if P is not None and len(P):
                    self.lod = kind
                    break
            else:
                self.cat = "noprofile"
                return
            if cat == "plant" and self.lod != "landcontact":
                P = base_rim(P, rule)
            if self.lod == "landcontact" or cat == "plant":
                S = P
            else:
                band = max(rule["band"], rule["band_frac"] * prof.get("height", 0.0))
                S = P[P[:, 1] <= P[:, 1].min() + band * 2 + 0.03]
            from model import fps
            S = S[fps(S.astype(np.float64), rule["max_samples"])]
            self.S = np.ascontiguousarray(S, np.float32)
            self.band = max(rule["band"], rule["band_frac"] * prof.get("height", 0.0)) + 1e-4
            if cat == "plant":
                self.band = 1e9            # every rim point counts
            self.r_xz = float(np.sqrt((self.S[:, [0, 2]] ** 2).sum(1)).max() + 0.5)
        self.mesh = None
        for name in ("rw", "geo"):
            if prof.get(name + "_v") is not None and len(prof[name + "_f"]):
                self.mesh = (np.asarray(prof[name + "_v"], np.float64), np.asarray(prof[name + "_f"]), name)
                break
        self.geo = None
        if prof.get("geo_v") is not None and len(prof["geo_f"]):
            self.geo = (np.asarray(prof["geo_v"], np.float64), np.asarray(prof["geo_f"]))
        if cat == "hanging":
            import re
            rx = re.compile(rule["attach_regex"], re.I)
            pts = [v for n, v in prof.get("memory", {}).items() if rx.search(n)]
            self.attach_from = "memory" if pts else "top"
            self.S = np.asarray(pts if pts else [prof["top"]], np.float32).reshape(-1, 3)
        if cat == "road":
            rw = prof.get("rw_v")
            if rw is None:
                self.cat = "noprofile"
        # the samples themselves go into the key too, so a change in how they are picked re-checks everything
        if self.S is not None:
            self.hash = np.frombuffer(__import__("hashlib").blake2b(
                self.hash.tobytes() + np.ascontiguousarray(self.S).tobytes(), digest_size=8).digest(), np.uint64)[0]


def base_rim(P, rule):
    """Plant base rim: the lowest point per angular sector around the centre of the bottom band."""
    Q = P[P[:, 1] <= P[:, 1].min() + rule["band"]]
    c = Q[:, [0, 2]].mean(0)
    d = np.hypot(Q[:, 0] - c[0], Q[:, 2] - c[1])
    if (d <= rule.get("base_radius", 1e9)).sum() >= 3:
        Q = Q[d <= rule.get("base_radius", 1e9)]
    n = int(rule.get("sectors", 12))
    ang = np.arctan2(Q[:, 0] - c[0], Q[:, 2] - c[1])
    rim = []
    for s in range(n):
        # overlapping 90 degree windows, so a coarse trunk (vertices 30-60 degrees apart) never leaves a window
        # holding only the taper above its bottom ring
        m = np.abs((ang - (2 * np.pi * s / n) + np.pi) % (2 * np.pi) - np.pi) <= np.pi / 4
        if m.any():
            rim.append(Q[m][np.argmin(Q[m][:, 1])])
    rim.append(Q[np.argmin(Q[:, 1])])
    return np.unique(np.array(rim, np.float32), axis=0)


# ------------------------------------------------------------------------------------------ the checker
class Result:
    FIELDS = (("flags", np.int16), ("gmax", np.float32), ("gmin", np.float32), ("embed", np.float32),
              ("worst", np.int16), ("host", np.int32), ("aux", np.float32))

    def __init__(self, n):
        for f, t in self.FIELDS:
            setattr(self, f, np.zeros(n, t))
        self.host[:] = -1
        self.gmax[:] = np.nan
        self.gmin[:] = np.nan

    def take(self, idx, other, oidx):
        for f, _ in self.FIELDS:
            getattr(self, f)[idx] = getattr(other, f)[oidx]


def fail_mask(kinds, O, R):
    """bool per object: the rule for its category is broken (skips/no-profile excluded)."""
    bad = (R.flags & (F_FLOAT | F_SINK | F_EMBED | F_NOHOST | F_ROAD)) != 0
    return bad


class Checker:
    def __init__(self, terrain, rules, profiles, class_index=None, scope="island", use_cache=True, log=print):
        self.T, self.rules, self.profiles, self.ci = terrain, rules, profiles, class_index
        self.scope, self.use_cache, self.log = scope, use_cache, log
        self.stats = {}

    # ---- kinds
    def kinds_for(self, O):
        from model import categorize
        out = []
        for p3d, cls in O.keys:
            prof = self.profiles.get(p3d) if p3d else None
            cat, why = categorize(self.rules, cls, p3d, prof) if prof else ("noprofile", "missing")
            if prof is None or "error" in prof:
                c2, _ = categorize(self.rules, cls, p3d or "", None)
                if c2 == "skip":
                    cat, why = "skip", "name"
            rule = self.rules["categories"].get(cat, {})
            out.append(KindInfo(p3d, cls, prof, cat, why, rule, self.rules))
        return out

    # ---- keys
    def object_keys(self, O, kinds):
        n = len(O)
        khash = np.array([k.hash for k in kinds], np.uint64)
        rxz = np.array([k.r_xz for k in kinds], np.float64)[O.kidx]
        h = khash[O.kidx]
        bits = np.ascontiguousarray(O.M.astype(np.float32)).view(np.uint32)
        for c in range(12):
            h = combine(h, bits[:, c])
        x, z = O.M[:, 9], O.M[:, 11]
        h = combine(h, self.T.tiles_key(x - rxz, z - rxz, x + rxz, z + rxz))
        hostdep = np.array([k.cat in ("hanging",) or k.rule.get("support") == "terrain_or_host" for k in kinds])[O.kidx]
        if hostdep.any() and self.hosts is not None:
            hk = self.host_cell_keys(x[hostdep], z[hostdep], rxz[hostdep])
            h[hostdep] = combine(h[hostdep], hk)
        h[h == 0] = 1
        return h

    # ---- host index
    def build_hosts(self, O, kinds):
        hc = set(self.rules.get("host_categories", ["building"]))
        ishost = np.array([k.cat in hc and k.mesh is not None for k in kinds])[O.kidx]
        idx = np.nonzero(ishost)[0]
        self.hosts = None
        if not len(idx):
            return
        # world AABB of each host from its 8 bbox corners
        corners = []
        for kk in range(len(kinds)):
            k = kinds[kk]
            if k.prof is None or "error" in k.prof:
                corners.append(np.zeros((8, 3)))
                continue
            b0, b1 = np.array(k.prof["bmin"]), np.array(k.prof["bmax"])
            corners.append(np.array([[x, y, z] for x in (b0[0], b1[0]) for y in (b0[1], b1[1]) for z in (b0[2], b1[2])]))
        C = np.asarray(corners)[O.kidx[idx]]                             # (h, 8, 3)
        M = O.M[idx]
        W = (M[:, None, 9:12] + C[..., 0:1] * M[:, None, 0:3] + C[..., 1:2] * M[:, None, 3:6]
             + C[..., 2:3] * M[:, None, 6:9])
        lo, hi = W.min(1), W.max(1)
        c0 = np.floor(lo[:, [0, 2]] / HOST_CELL).astype(np.int64)
        c1 = np.floor(hi[:, [0, 2]] / HOST_CELL).astype(np.int64)
        cells, owners = [], []
        for a in range(int((c1 - c0)[:, 0].max()) + 1):
            for b in range(int((c1 - c0)[:, 1].max()) + 1):
                ok = (c0[:, 0] + a <= c1[:, 0]) & (c0[:, 1] + b <= c1[:, 1])
                cells.append(((c0[ok, 0] + a) << 32) + (c0[ok, 1] + b))
                owners.append(np.nonzero(ok)[0])
        cells = np.concatenate(cells)
        owners = np.concatenate(owners)
        order = np.argsort(cells, kind="stable")
        self.hosts = {"idx": idx, "lo": lo, "hi": hi, "cells": cells[order], "own": owners[order]}
        # per-cell key = combination of the keys of every host touching it
        hkey = np.array([k.hash for k in kinds], np.uint64)[O.kidx[idx]]
        bits = np.ascontiguousarray(M.astype(np.float32)).view(np.uint32)
        for c in range(12):
            hkey = combine(hkey, bits[:, c])
        self.hosts["key"] = hkey
        uc, start = np.unique(self.hosts["cells"], return_index=True)
        ck = np.zeros(len(uc), np.uint64)
        np.bitwise_xor.at(ck, np.searchsorted(uc, self.hosts["cells"]), hkey[self.hosts["own"]])
        self.hosts["ucells"], self.hosts["ckey"] = uc, ck

    def _cells_of(self, x, z):
        return (np.floor(x / HOST_CELL).astype(np.int64) << 32) + np.floor(z / HOST_CELL).astype(np.int64)

    def host_cell_keys(self, x, z, r):
        H = self.hosts
        out = np.zeros(len(x), np.uint64)
        for dx in (-1, 1):
            for dz in (-1, 1):
                c = self._cells_of(x + dx * r, z + dz * r)
                p = np.clip(np.searchsorted(H["ucells"], c), 0, len(H["ucells"]) - 1)
                k = np.where(H["ucells"][p] == c, H["ckey"][p], np.uint64(0))
                out = combine(out, k)
        return out

    def host_pairs(self, O, obj_idx, kinds, rxz):
        """(object index, host index) pairs whose world AABBs overlap (self excluded)."""
        H = self.hosts
        if H is None or not len(obj_idx):
            return np.zeros(0, np.int64), np.zeros(0, np.int64)
        x, z = O.M[obj_idx, 9], O.M[obj_idx, 11]
        pa, pb = [], []
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                c = self._cells_of(x + dx * rxz, z + dz * rxz)
                lo = np.searchsorted(H["cells"], c, "left")
                hi = np.searchsorted(H["cells"], c, "right")
                cnt = hi - lo
                if not cnt.any():
                    continue
                rep = np.repeat(np.arange(len(obj_idx)), cnt)
                off = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt)
                pa.append(rep)
                pb.append(H["own"][np.repeat(lo, cnt) + off])
        if not pa:
            return np.zeros(0, np.int64), np.zeros(0, np.int64)
        pa, pb = np.concatenate(pa), np.concatenate(pb)
        u = np.unique((pa.astype(np.int64) << 32) + pb)
        pa, pb = u >> 32, u & 0xFFFFFFFF
        oi = obj_idx[pa]
        hi_ = H["idx"][pb]
        x, y, z = O.M[oi, 9], O.M[oi, 10], O.M[oi, 11]
        r = rxz[pa]
        ok = ((x + r >= H["lo"][pb, 0]) & (x - r <= H["hi"][pb, 0]) & (z + r >= H["lo"][pb, 2])
              & (z - r <= H["hi"][pb, 2]) & (y + r >= H["lo"][pb, 1] - 1) & (y - r <= H["hi"][pb, 1] + 1) & (oi != hi_))
        return pa[ok], pb[ok]

    # ---- main entry
    def run(self, O):
        t0 = time.time()
        kinds = self.kinds_for(O)
        self.kinds = kinds
        self.build_hosts(O, kinds)
        t1 = time.time()
        keys = self.object_keys(O, kinds)
        t2 = time.time()
        R = Result(len(O))
        self.stats = {}
        dirty = np.ones(len(O), bool)
        cfile = os.path.join(CACHE, "cache_%s.npz" % self.scope)
        if self.use_cache and os.path.isfile(cfile):
            z = np.load(cfile)
            ck = z["keys"]
            if len(ck):
                p = np.clip(np.searchsorted(ck, keys), 0, len(ck) - 1)
                hit = ck[p] == keys
                old = Result(len(ck))
                for f, _ in Result.FIELDS:
                    setattr(old, f, z[f])
                R.take(np.nonzero(hit)[0], old, p[hit])
                dirty = ~hit
        t3 = time.time()
        self.check(O, kinds, np.nonzero(dirty)[0], R)
        t4 = time.time()
        if self.use_cache:
            order = np.argsort(keys)
            os.makedirs(CACHE, exist_ok=True)
            with open(cfile, "wb") as f:
                np.savez(f, keys=keys[order], **{fn: getattr(R, fn)[order] for fn, _ in Result.FIELDS})
        t5 = time.time()
        self.stats.update({"objects": len(O), "checked": int(dirty.sum()), "cached": int((~dirty).sum()),
                      "t_setup": t1 - t0, "t_keys": t2 - t1, "t_cache_load": t3 - t2, "t_check": t4 - t3,
                      "t_cache_save": t5 - t4, "t_total": t5 - t0})
        self.keys = keys
        return R

    def check(self, O, kinds, idx, R):
        if not len(idx):
            return
        kid = O.kidx[idx]
        order = np.argsort(kid, kind="stable")
        idx, kid = idx[order], kid[order]
        bounds = np.nonzero(np.diff(kid))[0] + 1
        groups = np.split(idx, bounds)
        rxz_all = np.array([k.r_xz for k in kinds], np.float64)
        self.stats["by_cat"] = bc = {}
        for g in groups:
            k = kinds[O.kidx[g[0]]]
            tg = time.time()
            self._one(O, kinds, k, g, R, rxz_all)
            e = bc.setdefault(k.cat, [0, 0.0])
            e[0] += len(g)
            e[1] += time.time() - tg

    def _one(self, O, kinds, k, g, R, rxz_all):
        if True:
            if k.cat == "noprofile":
                R.flags[g] = F_NOPROFILE
            elif k.cat in ("skip",) or k.cat not in self.rules["categories"]:
                R.flags[g] = F_SKIP
            elif k.cat == "road":
                self.check_road(O, k, g, R)
            elif k.cat == "hanging":
                self.check_hanging(O, kinds, k, g, R, rxz_all)
            else:
                self.check_contact(O, kinds, k, g, R, rxz_all)

    # ---- contact categories (plant, rock, building, prop)
    @staticmethod
    def world(M, S):
        M = M.astype(np.float32)
        sx, sy, sz = S[:, 0], S[:, 1], S[:, 2]
        wx = M[:, 9:10] + sx * M[:, 0:1] + sy * M[:, 3:4] + sz * M[:, 6:7]
        wy = M[:, 10:11] + sx * M[:, 1:2] + sy * M[:, 4:5] + sz * M[:, 7:8]
        wz = M[:, 11:12] + sx * M[:, 2:3] + sy * M[:, 5:6] + sz * M[:, 8:9]
        return wx, wy, wz

    def check_contact(self, O, kinds, k, g, R, rxz_all, chunk=200000):
        rule = k.rule
        S = k.S
        for c0 in range(0, len(g), chunk):
            gi = g[c0:c0 + chunk]
            M = O.M[gi]
            wx, wy, wz = self.world(M, S)
            sup = self.T.sample(wx, wz)
            flags = np.zeros(len(gi), np.int16)
            hostid = np.full(len(gi), -1, np.int32)
            if rule.get("support") == "terrain_or_host" and self.hosts is not None:
                pa, pb = self.host_pairs(O, gi, kinds, rxz_all[O.kidx[gi]])
                if len(pa):
                    hy = self.host_floor(O, kinds, gi, pa, pb, wx, wy, wz)
                    better = hy > sup
                    sup = np.where(better, hy, sup)
                    on = better.any(1)
                    flags[on] |= F_HOST
                    hostid[np.unique(pa)] = self.hosts["idx"][pb[np.unique(pa, return_index=True)[1]]]
            gap = wy - sup
            wmin = wy.min(1, keepdims=True)
            m = wy <= wmin + np.float32(k.band)
            gm = np.where(m, gap, -np.inf)
            worst = gm.argmax(1)
            gmax = gm[np.arange(len(gi)), worst]
            gmin = np.where(m, gap, np.inf).min(1)
            embed = np.zeros(len(gi), np.float32)
            cat = k.cat
            if cat in ("plant", "building"):
                wy_gl = wy + (np.float32(k.gl) - S[:, 1]) * M[:, 4:5].astype(np.float32)
                # building: worst point of the footprint; plant: at the stem (mean of its base points)
                embed = (sup - wy_gl).max(1) if cat == "building" else (sup - wy_gl).mean(1)
            if cat == "plant":
                flags[gmax > -rule["min_sink"]] |= F_FLOAT
                flags[embed > rule["max_embed"]] |= F_SINK
            elif cat == "rock":
                flags[gmax > -rule["min_sink"]] |= F_FLOAT
            elif cat == "building":
                flags[gmax > rule["gap_tol"]] |= F_FLOAT
                flags[embed > rule["embed_max"]] |= F_EMBED
            elif cat == "prop":
                flags[gmax > rule["tol"]] |= F_FLOAT
                flags[gmin < -rule["tol"]] |= F_SINK
            R.flags[gi] = flags
            R.gmax[gi] = gmax
            R.gmin[gi] = gmin
            R.embed[gi] = embed
            R.worst[gi] = worst
            R.host[gi] = hostid

    def host_floor(self, O, kinds, gi, pa, pb, wx, wy, wz):
        """Highest host surface (Roadway LOD, else Geometry) straight below each sample (+PROBE_UP); -inf if none.
        Returns (len(gi), k). Vectorised per host model."""
        out = np.full(wx.shape, -np.inf, np.float32)
        H = self.hosts
        hobj = H["idx"][pb]
        hk = O.kidx[hobj]
        for kk in np.unique(hk):
            sel = hk == kk
            V, F, _ = kinds[kk].mesh
            Mh_all = O.M[hobj[sel]]
            upright = (np.abs(Mh_all[:, 3]) + np.abs(Mh_all[:, 5]) + np.abs(Mh_all[:, 1]) + np.abs(Mh_all[:, 7])) < 1e-5
            if upright.all():
                a_ = pa[sel]
                Mh = Mh_all
                sc = Mh[:, 4]
                # local x/z of each sample (yaw + uniform scale only): rows aside/dir are orthogonal, length sc
                dx = wx[a_].astype(np.float64) - Mh[:, None, 9]
                dz = wz[a_].astype(np.float64) - Mh[:, None, 11]
                lx = (dx * Mh[:, None, 0] + dz * Mh[:, None, 2]) / (sc[:, None] ** 2)
                lz = (dx * Mh[:, None, 6] + dz * Mh[:, None, 8]) / (sc[:, None] ** 2)
                ly = (wy[a_].astype(np.float64) + PROBE_UP - Mh[:, None, 10]) / sc[:, None]
                hyl = floor_grid(kinds[kk]).query(lx.ravel(), lz.ravel(), ly.ravel()).reshape(lx.shape)
                hy = Mh[:, None, 10] + hyl * sc[:, None]
                rowmax_into(out, a_, hy.astype(np.float32))
                continue
            A, B, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
            a_, h_ = pa[sel], hobj[sel]
            Mh = O.M[h_]
            R3 = Mh[:, 0:9].reshape(-1, 3, 3)                    # rows aside, up, dir
            Rinv = np.linalg.inv(np.transpose(R3, (0, 2, 1)))     # world = pos + R^T-columns... local = inv(Mcols) (w - p)
            P = np.stack([wx[a_], wy[a_] + PROBE_UP, wz[a_]], -1).astype(np.float64) - Mh[:, None, 9:12]
            L = np.einsum("nij,nkj->nki", Rinv, P)                 # local sample origins (n, k, 3)
            D = np.einsum("nij,j->ni", Rinv, np.array([0.0, -1.0, 0.0]))   # local ray dir per pair
            n, kk_, _ = L.shape
            Lf = L.reshape(-1, 3)
            Df = np.repeat(D, kk_, 0)
            best = np.full(len(Lf), np.inf)
            e1, e2 = B - A, C - A
            for t0 in range(0, len(Lf), 4096):
                o = Lf[t0:t0 + 4096, None, :]
                d = Df[t0:t0 + 4096, None, :]
                pvec = np.cross(d, e2[None])
                det = (e1[None] * pvec).sum(-1)
                ok = np.abs(det) > 1e-12
                inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
                tvec = o - A[None]
                u = (tvec * pvec).sum(-1) * inv
                qvec = np.cross(tvec, e1[None])
                v = (d * qvec).sum(-1) * inv
                t = (e2[None] * qvec).sum(-1) * inv
                hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t >= 0)
                best[t0:t0 + 4096] = np.where(hit, t, np.inf).min(1)
            # world y of the hit = origin y - t * |world dir| (world dir is exactly (0,-1,0) scaled back)
            hy = (wy[a_].astype(np.float64) + PROBE_UP).reshape(-1) - best
            hy = hy.reshape(n, kk_)
            rowmax_into(out, a_, hy.astype(np.float32))
        return out

    # ---- hanging
    def check_hanging(self, O, kinds, k, g, R, rxz_all):
        tol, search = k.rule["tol"], k.rule["search"]
        S = k.S
        wx, wy, wz = self.world(O.M[g], S)
        best = np.full(wx.shape, np.inf)
        bhost = np.full(len(g), -1, np.int32)
        hdist = np.full(len(g), np.inf)
        if self.hosts is not None:
            pa, pb = self.host_pairs(O, g, kinds, rxz_all[O.kidx[g]] + search)
            hobj = self.hosts["idx"][pb] if len(pb) else pb
            hk = O.kidx[hobj] if len(pb) else pb
            for kk in np.unique(hk):
                if kinds[kk].geo is None:
                    continue
                V, F = kinds[kk].geo
                sel = np.nonzero(hk == kk)[0]
                a_, h_ = pa[sel], hobj[sel]
                Mh = O.M[h_]
                Rinv = np.linalg.inv(np.transpose(Mh[:, 0:9].reshape(-1, 3, 3), (0, 2, 1)))
                P = np.stack([wx[a_], wy[a_], wz[a_]], -1).astype(np.float64) - Mh[:, None, 9:12]
                L = np.einsum("nij,nkj->nki", Rinv, P)
                sc = np.linalg.norm(Mh[:, 3:6], axis=1)[:, None]
                d = point_tri_dist(L.reshape(-1, 3), V[F[:, 0]], V[F[:, 1]], V[F[:, 2]],
                                   cap=search / float(sc.min())).reshape(L.shape[:2]) * sc
                dmin = d.min(1)
                np.minimum.at(best, a_, d)
                # remember the nearest host per object (last write wins = smallest distance)
                o = np.argsort(dmin)[::-1]
                cur = np.full(len(g), np.inf)
                np.minimum.at(cur, a_, dmin)
                bh = bhost.copy()
                bh[a_[o]] = h_[o]
                upd = cur < hdist
                bhost[upd] = bh[upd]
                hdist = np.minimum(cur, hdist)
        worst = best.argmax(1)
        dmax = best[np.arange(len(g)), worst]
        flags = np.zeros(len(g), np.int16)
        flags[~np.isfinite(dmax)] |= F_NOHOST
        flags[np.isfinite(dmax) & (dmax > tol)] |= F_FLOAT
        R.flags[g] = flags
        R.gmax[g] = np.where(np.isfinite(dmax), dmax, np.nan)
        R.gmin[g] = np.nan
        R.worst[g] = worst
        R.host[g] = bhost

    # ---- road pieces
    def check_road(self, O, k, g, R, chunk=20000):
        """Roadway surface vs terrain, vectorised per model. drape: the engine sets every Roadway vertex onto the
        terrain, so what can still be wrong is terrain poking through (or dipping under) the flat face between
        vertices. rigid: the piece as placed. Both are measured; rule mode picks which one fails; aux keeps the other."""
        V = np.asarray(k.prof["rw_v"], np.float64)
        F = np.asarray(k.prof["rw_f"])
        if not hasattr(k, "road_s"):
            fi, bw = [], []
            for f_i, f in enumerate(F):
                A, B, C = V[f]
                L = max(np.linalg.norm(B - A), np.linalg.norm(C - A), np.linalg.norm(C - B))
                n = max(2, int(L / k.rule["step"]) + 1)
                u, v = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))
                m = (u + v) <= 1
                u, v = u[m], v[m]
                fi.append(np.full(len(u), f_i))
                bw.append(np.stack([1 - u - v, u, v], 1))
            fi, bw = np.concatenate(fi), np.vstack(bw)
            k.road_s = (F[fi], bw, (bw[:, :, None] * V[F[fi]]).sum(1).astype(np.float32))
        Fv, bw, Ls = k.road_s
        use = 0 if k.rule["mode"] == "drape" else 1
        for c0 in range(0, len(g), chunk):
            gi = g[c0:c0 + chunk]
            M = O.M[gi]
            vx, vy, vz = self.world(M, V.astype(np.float32))
            tv = self.T.sample(vx, vz)                                          # terrain under each vertex
            dv = tv + (V[:, 1] - V[:, 1].min()).astype(np.float32) * M[:, 4:5].astype(np.float32)
            sx, sy, sz = self.world(M, Ls)
            ts = self.T.sample(sx, sz)
            yd = (dv[:, Fv] * bw[None].astype(np.float32)).sum(2)                # draped face height at each sample
            D0, D1 = yd - ts, sy - ts
            D = D0 if use == 0 else D1
            gmax, gmin = D.max(1), D.min(1)
            R.flags[gi] = np.where(np.maximum(gmax, -gmin) > k.rule["tol"], F_ROAD, 0)
            R.gmax[gi], R.gmin[gi], R.embed[gi] = gmax, gmin, 0.0
            o1, o2 = D1.max(1), D1.min(1)
            R.aux[gi] = np.where(o1 >= -o2, o1, o2)                              # rigid worst: + floats, - buried
            R.worst[gi] = D.argmax(1)


def rowmax_into(out, rows, vals):
    """out[rows[i]] = max(out[rows[i]], vals[i]) with repeated rows (a fast np.maximum.at for 2D rows)."""
    if not len(rows):
        return
    order = np.argsort(rows, kind="stable")
    rs = rows[order]
    starts = np.r_[0, np.nonzero(np.diff(rs))[0] + 1]
    red = np.maximum.reduceat(vals[order], starts, axis=0)
    u = rs[starts]
    out[u] = np.maximum(out[u], red)


class FloorGrid:
    """2D bucket grid over a host mesh (model frame): answers 'highest surface straight below (x, y, z)' fast."""

    def __init__(self, V, F, cell=1.0):
        A, B, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
        v0 = C[:, [0, 2]] - A[:, [0, 2]]
        v1 = B[:, [0, 2]] - A[:, [0, 2]]
        den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
        keep = np.abs(den) > 1e-9                                  # vertical faces never support anything
        self.A, self.B, self.C, self.v0, self.v1, self.den = A[keep], B[keep], C[keep], v0[keep], v1[keep], den[keep]
        lo = np.minimum(np.minimum(self.A, self.B), self.C)[:, [0, 2]]
        hi = np.maximum(np.maximum(self.A, self.B), self.C)[:, [0, 2]]
        self.o = lo.min(0) if len(lo) else np.zeros(2)
        self.cell = cell
        n = np.maximum(np.ceil((hi.max(0) - self.o) / cell).astype(int) + 1, 1) if len(lo) else np.array([1, 1])
        self.n = n
        buckets = [[] for _ in range(n[0] * n[1])]
        c0 = np.floor((lo - self.o) / cell).astype(int)
        c1 = np.floor((hi - self.o) / cell).astype(int)
        for t in range(len(lo)):
            for i in range(c0[t, 0], c1[t, 0] + 1):
                for j in range(c0[t, 1], c1[t, 1] + 1):
                    buckets[i * n[1] + j].append(t)
        K = max(1, max(len(b) for b in buckets))
        self.tab = np.full((len(buckets), K), -1, np.int32)
        for b, lst in enumerate(buckets):
            self.tab[b, :len(lst)] = lst

    def query(self, x, z, y, chunk=65536):
        out = np.full(len(x), -np.inf)
        if not len(self.A):
            return out
        i_all = np.floor((x - self.o[0]) / self.cell).astype(int)
        j_all = np.floor((z - self.o[1]) / self.cell).astype(int)
        inside_grid = np.nonzero((i_all >= 0) & (j_all >= 0) & (i_all < self.n[0]) & (j_all < self.n[1]))[0]
        for s in range(0, len(inside_grid), chunk):
            sel = inside_grid[s:s + chunk]
            px, pz, py = x[sel], z[sel], y[sel]
            b = i_all[sel] * self.n[1] + j_all[sel]
            T = self.tab[b]                                           # (p, K)
            valid = T >= 0
            Tc = np.where(valid, T, 0)
            ax, az = self.A[Tc, 0], self.A[Tc, 2]
            wx_, wz_ = px[:, None] - ax, pz[:, None] - az
            v0, v1, den = self.v0[Tc], self.v1[Tc], self.den[Tc]
            u = (wx_ * v1[..., 1] - wz_ * v1[..., 0]) / den            # weight of C
            v = (v0[..., 0] * wz_ - v0[..., 1] * wx_) / den            # weight of B
            inside = valid & (u >= -1e-6) & (v >= -1e-6) & (u + v <= 1 + 1e-6)
            yh = self.A[Tc, 1] + u * (self.C[Tc, 1] - self.A[Tc, 1]) + v * (self.B[Tc, 1] - self.A[Tc, 1])
            yh = np.where(inside & (yh <= py[:, None]), yh, -np.inf)
            out[sel] = yh.max(1)
        return out


def floor_grid(k):
    if getattr(k, "_fg", None) is None:
        V, F, _ = k.mesh
        k._fg = FloorGrid(np.asarray(V, np.float64), np.asarray(F))
    return k._fg


def point_tri_dist(P, A, B, C, cap=None):
    """Distance from each point P (p,3) to the nearest of triangles (A,B,C) (t,3). Ericson's closest point.
    cap: distances beyond it may come back as inf (triangles farther than cap from a point chunk are culled)."""
    if len(P) > 256:
        order = np.lexsort((P[:, 2], P[:, 0]))
        out = np.empty(len(P))
        for i in range(0, len(P), 256):
            o = order[i:i + 256]
            out[o] = point_tri_dist(P[o], A, B, C, cap)
        return out
    if cap is not None and len(A):
        lo, hi = P.min(0) - cap, P.max(0) + cap
        tlo = np.minimum(np.minimum(A, B), C)
        thi = np.maximum(np.maximum(A, B), C)
        keep = np.all((thi >= lo) & (tlo <= hi), axis=1)
        A, B, C = A[keep], B[keep], C[keep]
    out = np.full(len(P), np.inf)
    for s in range(0, len(A), 2048):
        a, b, c = A[s:s + 2048][None], B[s:s + 2048][None], C[s:s + 2048][None]
        p = P[:, None, :]
        ab, ac, ap = b - a, c - a, p - a
        d1, d2 = (ab * ap).sum(-1), (ac * ap).sum(-1)
        bp = p - b
        d3, d4 = (ab * bp).sum(-1), (ac * bp).sum(-1)
        cp = p - c
        d5, d6 = (ab * cp).sum(-1), (ac * cp).sum(-1)
        va = d3 * d6 - d5 * d4
        vb = d5 * d2 - d1 * d6
        vc = d1 * d4 - d3 * d2
        den = va + vb + vc
        den = np.where(np.abs(den) < 1e-18, 1e-18, den)
        v = vb / den
        w = vc / den
        q = a + ab * v[..., None] + ac * w[..., None]                  # interior
        # edge / vertex regions
        with np.errstate(divide="ignore", invalid="ignore"):
            t_ab = np.clip(d1 / np.where(d1 - d3 == 0, 1e-18, d1 - d3), 0, 1)
            t_ac = np.clip(d2 / np.where(d2 - d6 == 0, 1e-18, d2 - d6), 0, 1)
            t_bc = np.clip((d4 - d3) / np.where((d4 - d3) + (d5 - d6) == 0, 1e-18, (d4 - d3) + (d5 - d6)), 0, 1)
        e_ab = a + ab * t_ab[..., None]
        e_ac = a + ac * t_ac[..., None]
        e_bc = b + (c - b) * t_bc[..., None]
        inside = (va >= 0) & (vb >= 0) & (vc >= 0)
        cand = np.stack([np.where(inside[..., None], q, e_ab), e_ab, e_ac, e_bc], 0)
        d = np.sqrt(((cand - p[None]) ** 2).sum(-1)).min(0)
        out = np.minimum(out, d.min(1))
    return out


# ------------------------------------------------------------------------------------------ report helpers
SIDES = ["front", "front-right", "right", "back-right", "back", "back-left", "left", "front-left"]
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def side_of(k, M, worst):
    if k.S is None or worst < 0 or worst >= len(k.S):
        return ""
    sx, sz = float(k.S[worst, 0]), float(k.S[worst, 2])
    if abs(sx) < 0.05 and abs(sz) < 0.05:
        return "centre"
    loc = SIDES[int(round(math.degrees(math.atan2(sx, sz)) / 45.0)) % 8]
    wxv = sx * M[0] + sz * M[6]
    wzv = sx * M[2] + sz * M[8]
    comp = COMPASS[int(round(math.degrees(math.atan2(wxv, wzv)) / 45.0)) % 8]
    return "%s (%s)" % (loc, comp)


def tilt_fit(terrain, k, M):
    """Least-squares plane of the terrain under the contact samples -> (pitch, roll) in degrees
    (+pitch = front up, +roll = right side up, wrp8.yaw_matrix convention)."""
    if k.S is None or len(k.S) < 3:
        return 0.0, 0.0
    S = k.S.astype(np.float64)
    wx, _, wz = (a[0] for a in Checker.world(M[None], k.S))
    g = terrain.sample(wx, wz).astype(np.float64)
    sc = float(np.linalg.norm(M[3:6]))
    A = np.stack([np.ones(len(S)), S[:, 0] * sc, S[:, 2] * sc], 1)
    if np.linalg.matrix_rank(A) < 3:
        return 0.0, 0.0
    c, a, b = np.linalg.lstsq(A, g, rcond=None)[0]
    return math.degrees(math.atan(b)), math.degrees(math.atan(a))
