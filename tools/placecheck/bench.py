"""placecheck map-scale benchmark (python tools\\placecheck\\check.py bench [--n 3000000] [--size 12800] [--grid 4096]).

Builds a synthetic map: a fractal heightmap (grid^2 vertices over size m) and ~n objects that use real model profiles
(vanilla + JP trees, bushes, rocks, buildings, a hay bale, a stand-in lantern, a road piece), placed by T's rule with
some noise so a fraction fails. Then times:
  1. full pass (empty cache)
  2. rerun with nothing changed (everything from cache)
  3. incremental: 1% of the objects moved and a 4 x 4 block of terrain tiles (~800 m square) raised
Uses its own cache file data\\placecheck\\cache_bench.npz (deleted before step 1).
"""
import os
import time

import numpy as np

import grounding as G
from model import CACHE, Profiles, load_rules

MODELS = [  # (p3d, class, share, kind)
    (r"dz\plants\tree\t_fagussylvatica_2f.p3d", "", 0.30, "plant"),
    (r"dz\plants\tree\t_pinussylvestris_2s.p3d", "", 0.30, "plant"),
    (r"JP\plants\tree\jp_sakura_01.p3d", "", 0.1667, "plant"),
    (r"dz\plants\bush\b_corylusavellana_1f.p3d", "", 0.10, "plant"),
    (r"JP\plants\bamboo\jp_bamboo_clump_01.p3d", "", 0.05, "plant"),
    (r"dz\rocks\rock_apart1.p3d", "", 0.02, "rock"),
    (r"dz\structures\residential\houses\house_1w01.p3d", "Land_House_1W01", 0.02, "building"),
    (r"JP\structures\machiya\jp_machiya_01.p3d", "Land_JP_Machiya_01", 0.02, "building"),
    (r"dz\structures\industrial\misc\misc_haybale.p3d", "StaticObj_Misc_HayBale", 0.02, "prop_floor"),
    (r"dz\structures\industrial\misc\misc_haybale.p3d", "StaticObj_Misc_HayBale", 0.0033, "prop"),
    (r"dz\gear\cooking\cauldron.p3d", "JP_BenchLantern", 0.0027, "hanging"),
    (r"dz\structures\roads\parts\grav_25.p3d", "", 0.0007, "road"),
]


def fractal(n, seed=1, beta=2.2, relief=260.0):
    rng = np.random.default_rng(seed)
    f = np.fft.rfft2(rng.standard_normal((n, n)).astype(np.float32))
    ky = np.fft.fftfreq(n)[:, None]
    kx = np.fft.rfftfreq(n)[None, :]
    k = np.sqrt(kx * kx + ky * ky)
    k[0, 0] = 1.0
    f *= (k ** (-beta / 2 - 0.5)).astype(np.float32)
    f[0, 0] = 0
    h = np.fft.irfft2(f, s=(n, n)).astype(np.float32)
    h = (h - h.min()) / (h.max() - h.min()) * relief
    return h


def build(n_total, size, grid, profiles, rules, seed=7):
    rng = np.random.default_rng(seed)
    T = G.Terrain(fractal(grid), size / grid)
    O = G.ObjSet()
    Ms, ks = [], []
    counts = {}
    hosts_M = []
    for mi, (p3d, cls, share, kind) in enumerate(MODELS):
        prof = profiles.get(p3d)
        if prof is None or "error" in prof:
            raise SystemExit("bench needs %s on P:" % p3d)
        O.keys.append((p3d, cls))
        n = int(round(n_total * share))
        counts[kind] = counts.get(kind, 0) + n
        bc = np.array(prof["bc"])
        if kind in ("prop_floor", "hanging") and hosts_M:
            H = np.vstack(hosts_M)
            hp = profiles.get(MODELS[6][0])                      # house_1w01 hosts
            pick = H[rng.integers(0, len(H), n)]
            if kind == "prop_floor":
                V, F = hp["rw_v"], hp["rw_f"]
                tri = V[F[rng.integers(0, len(F), n)]]
                w = rng.dirichlet([1, 1, 1], n)
                loc = (w[:, :, None] * tri).sum(1)
                loc[:, 1] += -prof["bmin"][1] + rng.normal(0, 0.02, n)       # bottom on the floor +- 2 cm
                rot = G.yaw_matrix(np.zeros(n))
            else:
                V = hp["geo_v"]
                loc = V[rng.integers(0, len(V), n)] - np.asarray(prof["top"]) + rng.normal(0, 0.02, (n, 3))
                rot = G.yaw_matrix(np.zeros(n))
            pos = pick[:, 9:12] + loc[:, 0:1] * pick[:, 0:3] + loc[:, 1:2] * pick[:, 3:6] + loc[:, 2:3] * pick[:, 6:9]
            M = np.concatenate([pick[:, 0:9] if kind == "prop_floor" else rot, pos], 1)
        else:
            x = rng.uniform(60, size - 60, n)
            z = rng.uniform(60, size - 60, n)
            yaw = rng.uniform(0, 360, n)
            sc = rng.uniform(0.85, 1.1, n) if kind == "plant" else np.ones(n)
            R = G.yaw_matrix(yaw, scale=sc)
            g = T.sample(x, z).astype(np.float64)
            yoff = rng.normal(0, 0.03, n)
            if kind == "rock":
                yoff = -(bc[1] + prof["bmin"][1]) - 0.3 * prof["height"]
            origin = np.stack([x, g + yoff, z], 1)
            pos = origin + bc[0] * R[:, 0:3] + bc[1] * R[:, 3:6] + bc[2] * R[:, 6:9]
            M = np.concatenate([R, pos], 1)
            if kind == "building":
                hosts_M.append(M[:max(1, n)] if mi == 6 else np.zeros((0, 12)))
        Ms.append(M)
        ks.append(np.full(len(M), mi, np.int32))
    O.M = np.vstack(Ms)
    O.kidx = np.concatenate(ks)
    O.src = np.zeros(len(O.kidx), np.int32)
    O.row = np.arange(len(O.kidx), dtype=np.int32)
    O.sources = ["bench"]
    return T, O, counts


def main(args):
    def opt(name, default):
        return type(default)(args[args.index(name) + 1]) if name in args else default
    n, size, grid = opt("--n", 3000000), opt("--size", 12800.0), opt("--grid", 4096)
    rules = load_rules()
    rules["overrides"]["jp_benchlantern"] = "hanging"
    profiles = Profiles()
    t0 = time.time()
    T, O, counts = build(n, size, grid, profiles, rules)
    profiles.save()
    print("bench map: %d objects on %.1f km, %d^2 heightmap (%.3f m cells), built in %.1f s" % (
        len(O), size / 1000, grid, T.cell, time.time() - t0))
    print("  " + ", ".join("%s %d" % kv for kv in counts.items()))
    cfile = os.path.join(CACHE, "cache_bench.npz")
    if os.path.isfile(cfile):
        os.remove(cfile)
    out = []

    def run(label):
        ch = G.Checker(T, rules, profiles, scope="bench")
        t = time.time()
        R = ch.run(O)
        dt = time.time() - t
        st = ch.stats
        nf = int(((R.flags & (G.F_FLOAT | G.F_SINK | G.F_EMBED | G.F_NOHOST | G.F_ROAD)) != 0).sum())
        line = ("%-34s %6.2f s  checked %8d  cached %8d  fails %7d  (keys %.2f, cache load %.2f, check %.2f, save %.2f)"
                % (label, dt, st["checked"], st["cached"], nf, st["t_keys"], st["t_cache_load"], st["t_check"],
                   st["t_cache_save"]))
        line += "\n      by category: " + ", ".join("%s %d in %.2f s" % (c, v[0], v[1]) for c, v in st.get("by_cat", {}).items())
        print(line)
        out.append(line)
        return R

    run("1. full pass (empty cache)")
    run("2. rerun, nothing changed")
    rng = np.random.default_rng(99)
    mv = rng.choice(len(O), len(O) // 100, replace=False)
    O.M[mv, 10] += rng.normal(0, 0.05, len(mv))
    span = G.TILE
    T.h[10 * span:14 * span + 1, 20 * span:24 * span + 1] += 0.3
    T.flat = T.h.ravel()
    T._tiles = None
    run("3. incremental: 1% moved + 16 tiles")
    with open(os.path.join(CACHE, "bench_last.txt"), "wb") as f:
        f.write(("\n".join(out) + "\n").encode())
    return 0
