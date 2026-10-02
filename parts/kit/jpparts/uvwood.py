r"""uvwood.py - the one shared texture-variety pass for wood (FX3, 2026-10-01). Materials half:
research/materials/make_wood_atlas.py. Design + proof: spikes/FX3/INVENTORY.md, PHASE2_PLAN.md, fx3_samples.jpg.

Why: every wood face is mapped world-planar (u, v = metres / tile in the part's frame, v = along the grain), so every
torii pole, post and board of the same height range showed the same knot at the same height, and a 2 m tile repeated
on every long member.

What it does, on a finished Part (all solids finalized, in the MODEL frame, i.e. after parts are placed / merged):
  * Each wood material is ONE atlas texture (sidecar "atlas": 2048 x 1024 = 4 m across the grain x 2 m along it):
    the maker's tile (rolled so a board joint sits at u = 0) beside a board-shuffled variant of it; the four 512 px
    columns are the four patches. The strip tiles across u and every column tiles along v.
  * Every UV GROUP gets one random affine map  u' = fu * u * (tile / W) + U0,  v' = fv * v * (tile_v / H) + V0
    (fu, fv = +-1 flips; U0 picks the patch and the offset across the grain, V0 the offset along it). Upstream code
    keeps computing UVs exactly as before (metres / sidecar tile_size_m); only this pass knows the atlas.
  * UV groups:
      plane  flat faces with auto UVs ('world' / 'grain' / 'fit'): all faces of the same material in the same plane
             (normal to 0.01, offset clustered within 2 mm). Coplanar overlapping faces keep identical mappings, so
             zfight's 'drawn identically' verdicts stay true (no new C20 flicker; proven on K2: 209 -> 209 pairs).
      solid  smooth solids (fkit lathe / skit tube: per-vertex normals) and explicit uv lists: one map per solid,
             so the grain stays continuous round a turned member.
      band   faces fkit.band_fit put into one clean plank band (solid.uvband): u' = (u + roll) / 2 + h / 2, h = 0 / 1
             (the same band in the tile or the variant half; the variant keeps every groove), no u flip.
  * Deterministic: seed = FNV-1a(salt = model name, group key from rounded geometry): rebuild-stable, order-free.
  * Grain along the member is upstream's job (core.face_uvs 'grain' / sidecar 'along member'); axes never swapped.

Stone (FX4, 2026-10-01; Stephen: 'stone torii columns still show duplicated textures'): a sidecar atlas with
"kind": "stone" (research/materials/make_stone_atlas.py: 2 x 2 tiles, the tile + 3 turned / mirrored / rolled variants,
tiling in u AND v) gets the same plane / solid groups, but each group's map also TURNS:  (a, b) -> R(t) (a, b), then
u' = fu * a' * (tile / W) + U0,  v' = b' * (tile_v / H) + V0  with U0, V0 anywhere in the atlas. "turn": "any" =
t uniform 0-360 deg (isotropic lichen stone); "small" = t within +-8 deg or 180 +-8 deg (rain streaks / tool marks run
along v and stay vertical on a vertical face). So the 8 faces of an octagonal post, the kasagi's faces, a lantern's
pieces each show their own patch.

Not touched: materials without an "atlas" in their sidecar (text decals, cells, field / river stone, roofs, end grain,
firewood), except the moss decal (MOSS below: flips + offsets per decal, no patches).
Called by core.Part.lods() (idempotent: solid._uvw) and by buildings/pipeline.py before zfight.resolve.
"""
import bisect
import math
import os
import random

MOSS = {"decal_moss": {"w_m": 2.0, "h_m": 2.0, "patches": 1, "lock": None, "roll_px": 0}}
ALLOW_FLIP = True        # one switch: if the in-game check shows inverted bumps on flipped faces, set False
NQ = 100.0               # normal quantisation (as zfight)
DGAP = 0.002             # plane offsets closer than this share a group (zfight TOL is 1 mm)
_checked = {}


def fnv(s):
    h = 2166136261
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h


def _r(x, q=1000.0):
    return int(round(x * q))


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def spec(mat):
    """The atlas spec of a library key, or None (material left alone)."""
    from . import core
    if mat in MOSS:
        return MOSS[mat]
    a = core.mat_info(mat).get("atlas")
    if a and mat not in _checked:
        _checked[mat] = _png_ok(core, mat)
    return a


def _png_ok(core, mat):
    """A maker re-run without make_wood_atlas.py leaves a 1024 tile behind: refuse to map into a missing atlas."""
    from PIL import Image
    p = core.png_path(mat, "_w1")
    if os.path.isfile(p):
        w, h = Image.open(p).size
        want = (core.mat_info(mat).get("atlas") or {}).get("px", [2048, 1024])
        if [w, h] != list(want):
            raise RuntimeError("uvwood: %s is %dx%d, not the %dx%d atlas: run research/materials/"
                               "make_wood_atlas.py / make_stone_atlas.py after the maker (and pack jp_common)"
                               % (p, w, h, want[0], want[1]))
    return True


def _solid_sig(s):
    xs = [v[0] for v in s.verts]
    ys = [v[1] for v in s.verts]
    zs = [v[2] for v in s.verts]
    return "%d,%d,%d|%d,%d,%d|%d" % (_r(sum(xs) / len(xs)), _r(sum(ys) / len(ys)), _r(sum(zs) / len(zs)),
                                     _r(max(xs) - min(xs)), _r(max(ys) - min(ys)), _r(max(zs) - min(zs)),
                                     len(s.faces))


def _is_solid_group(s):
    return getattr(s, "vn", None) is not None or isinstance(s.uv, list)


def _map(salt, key, flip, band=False):
    r = random.Random(fnv("%s|%s" % (salt, key)))
    U0, V0 = r.random(), r.random()
    fu = -1.0 if (flip and ALLOW_FLIP and not band and r.random() < 0.5) else 1.0
    fv = -1.0 if (flip and ALLOW_FLIP and r.random() < 0.5) else 1.0
    h = r.randrange(2)
    return U0, V0, fu, fv, h


def _turn(salt, key, mode):
    """FX4 stone: the group's turn (cos, sin), from its own seed (the wood maps above stay as they were)."""
    r = random.Random(fnv("%s|%s|turn" % (salt, key)))
    if mode == "any":
        a = r.uniform(0.0, 2.0 * math.pi)
    else:
        a = math.radians(r.uniform(-8.0, 8.0)) + (math.pi if r.random() < 0.5 else 0.0)
    return math.cos(a), math.sin(a)


def remap_part(P, salt=None):
    """In place, idempotent. Returns {'faces': n remapped, 'groups': n}."""
    from . import core
    salt = salt if salt is not None else P.name
    sp_cache = {}

    def sp_of(m):
        if m not in sp_cache:
            sp_cache[m] = spec(m)
        return sp_cache[m]

    planes = {}
    todo = []
    for s in P.solids:
        if getattr(s, "_uvw", False) or s.fuv is None or s.fm is None:
            continue
        todo.append(s)
        if _is_solid_group(s):
            continue
        band = getattr(s, "uvband", ())
        for fi in range(len(s.faces)):
            m = s.fm[fi]
            if fi in band or sp_of(m) is None:
                continue
            n = s.fn[fi]
            nq = (_r(n[0], NQ), _r(n[1], NQ), _r(n[2], NQ))
            planes.setdefault((m, nq), []).append(_dot(n, s.verts[s.faces[fi][0]]))
    clusters = {}
    for k, ds in planes.items():
        starts, prev = [], None
        for d in sorted(ds):
            if prev is None or d - prev > DGAP:
                starts.append(d)
            prev = d
        clusters[k] = starts

    def plane_key(m, n, d):
        nq = (_r(n[0], NQ), _r(n[1], NQ), _r(n[2], NQ))
        st = clusters[(m, nq)]
        i = max(0, bisect.bisect_right(st, d + 1e-9) - 1)
        return "p|%s|%d,%d,%d|%d" % (m, nq[0], nq[1], nq[2], _r(st[i]))

    nf, groups = 0, set()
    for s in todo:
        band = getattr(s, "uvband", ())
        sg = _is_solid_group(s)
        sig = _solid_sig(s) if sg else None
        new = []
        for fi in range(len(s.faces)):
            uv = s.fuv[fi]
            m = s.fm[fi]
            sp = sp_of(m)
            if sp is None:
                new.append(uv)
                continue
            mi = core.mat_info(m)
            n = s.fn[fi]
            if fi in band:
                d = _dot(n, s.verts[s.faces[fi][0]])
                key = ("b|%s|%s" % (m, sig)) if sg else \
                    "b|%s|%d,%d,%d|%d" % (m, _r(n[0], NQ), _r(n[1], NQ), _r(n[2], NQ), _r(d))
                U0, V0, fu, fv, h = _map(salt, key, True, band=True)
                roll = sp.get("roll_px", 0) / 1024.0
                new.append([(((a + roll) % 1.0) * 0.5 + 0.5 * h, fv * b + V0) for a, b in uv])
            else:
                key = ("s|%s|%s" % (m, sig)) if sg else plane_key(m, n, _dot(n, s.verts[s.faces[fi][0]]))
                U0, V0, fu, fv, h = _map(salt, key, True)
                ku, kv = mi["tile"] / sp["w_m"], mi["tile_v"] / sp["h_m"]
                if sp.get("kind") == "stone":
                    c, sn = _turn(salt, key, sp.get("turn", "small"))
                    new.append([(fu * (a * c - b * sn) * ku + U0, (a * sn + b * c) * kv + V0) for a, b in uv])
                else:
                    new.append([(fu * a * ku + U0, fv * b * kv + V0) for a, b in uv])
            groups.add(key)
            nf += 1
        s.fuv = new                     # rebind (transformed / merged copies share the old list object)
        s._uvw = True
    return {"faces": nf, "groups": len(groups)}
