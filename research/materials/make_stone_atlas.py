#!/usr/bin/env python3
r"""make_stone_atlas.py - FX4 (2026-10-01): stone texture variety, the materials half (the kit half is
parts/kit/jpparts/uvwood.py, stone mode). The stone sibling of make_wood_atlas.py and, like it, a POST STEP after the
makers (build_materials / make_textures for stone_cut + stone_carved, make_fp1_materials for stone_carved_aged).

Stephen (2026-10-01 walk): 'stone torii columns still show duplicated textures' (FX3 covered wood only). Cause: every
stone face is mapped world-planar from ONE small tile (stone_carved_aged 2 m, carved / cut 1 m), so the faces of an
octagonal post whose tangents line up sample the same strip of the tile, and every lichen rosette comes back every
1-2 m on every post, kasagi, lantern and grave.

  python research/materials/make_stone_atlas.py           atlases + stone macro -> PNG, PAA, rvmats (Stage3), sidecars
  python research/materials/make_stone_atlas.py --check   every stone atlas PNG is 2N x 2N and its PAAs are newer
  then pack jp_common (python research/materials/build_materials.py --rvmats-only keeps the macro).

PITFALL (as wood): a maker re-run rewrites the stone PNG as the old N x N tile; run this step again afterwards (it keeps
the maker's tile in data/materials/textures/_tile/ and always starts from it). uvwood refuses to remap a stone
material whose PNG is not the atlas.

Atlas (one per material and wear, same file names, so rvmats and p3d paths do not change): 2N x 2N px = 2 x 2 tiles
(stone_carved_aged 4 m x 4 m at 1024 -> 2048; stone_carved / stone_cut 2 m x 2 m at 512 -> 1024). Quadrant A = the
maker's tile; B, C, D = the same stone turned (0 / 90 / 180 / 270 deg), mirrored and rolled (normal map vectors turned
with it, DirectX green = down), each cut into the tiled canvas along an IRREGULAR (noise-wobbled) line inside its
quadrant, so the whole atlas tiles in u and v and has no straight seams. The variants and the whole atlas are rescaled
to the tile's mean colour (unmasked pixels): the palette check (C1) is unchanged by construction.
uvwood gives every flat stone face (plane group) and every smooth / explicit-uv stone solid its own turn (any angle),
offset (anywhere in the 2 x 2) and maybe a mirror: neighbouring faces of one post never show the same patch.

Macro (Stage3, as wood): jp_m_macro_stone_w{0,1,2}_mc = soft isotropic grime clouds + pale lichen-grey bleach (no
directional streaks: uvwood turns each face's uv, so a streak would point anywhere). ~11 m repeat.
"""
import json
import os
import sys
import concurrent.futures as cf

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_textures as MT  # noqa: E402

TEX = os.path.join(DEV, "data", "materials", "textures")
TILE = os.path.join(TEX, "_tile")
LIB = os.path.join(DEV, "src", "JP", "common", "materials")
REPORT = os.path.join(HERE, "FX4_STONE_ATLAS_REPORT.json")
f32 = np.float32

# key -> maker tile px (the atlas is 2x that); tile_size_m comes from the sidecar
STONE = {"stone_carved_aged": 1024, "stone_carved": 512, "stone_cut": 512}
# isotropic stones may be turned any way (atlas variants by 90 deg, uvwood any angle); the others carry rain streaks /
# tool marks along v (= down a vertical face): variants only 0 / 180 deg + mirror, uvwood turns them a few degrees only
ISO = {"stone_carved_aged"}
MACRO_REPEAT_M = 11.3                       # macro repeat (never lines up with the 2 / 4 m atlas)
MACRO_TEX = "JP\\common\\materials\\macro\\jp_m_macro_stone_%s_mc.paa"
MAPS = ("co", "nohq", "smdi")


def fnv(s):
    h = 2166136261
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h


def tile(name, n, mode="RGB"):
    """The maker's n x n tile: the library PNG if fresh from a maker (n wide; a copy goes to _tile/), else the copy."""
    import shutil
    p, c = os.path.join(TEX, name), os.path.join(TILE, name)
    im = Image.open(p)
    w = im.size[0]
    im.close()
    if w == n:
        os.makedirs(TILE, exist_ok=True)
        shutil.copyfile(p, c)
    elif not os.path.isfile(c):
        raise RuntimeError("%s is %d wide and there is no _tile copy: re-run its maker first" % (name, w))
    return np.asarray(Image.open(c).convert(mode)).astype(f32) / 255.0


def save(a, name):
    a = np.clip(a, 0, 1)
    mode = "L" if a.ndim == 2 else {3: "RGB", 4: "RGBA"}[a.shape[2]]
    Image.fromarray((a * 255 + 0.5).astype(np.uint8), mode).save(os.path.join(TEX, name))


def orient(maps, k, flip, dx, dy):
    """Turn every map by k * 90 deg (np.rot90), mirror left-right if flip, roll by (dy, dx); the normal map's (u, v)
    vector turns with the content (R = +u right, G = +v down: DirectX)."""
    out = {}
    for key, a in maps.items():
        b = np.rot90(a, k, axes=(0, 1))
        if flip:
            b = b[:, ::-1]
        b = np.roll(np.roll(b, dy, 0), dx, 1).copy()
        if key == "nohq":
            nu, nv = b[..., 0] * 2 - 1, b[..., 1] * 2 - 1
            for _ in range(k % 4):                        # rot90 CCW: (nu, nv) -> (nv, -nu)
                nu, nv = nv, -nu
            if flip:
                nu = -nu
            b[..., 0], b[..., 1] = nu * 0.5 + 0.5, nv * 0.5 + 0.5
        out[key] = b
    return out


def quad_mask(n, q, seed):
    """2n x 2n weight of quadrant q (0..3 = A B / C D): 1 deep inside, 0 near the quadrant's edges (so the 2 x 2 tile
    canvas shows there and the atlas tiles), the boundary wobbled by noise, a short soft edge."""
    N = 2 * n
    m = np.zeros((N, N), f32)
    qy, qx = divmod(q, 2)
    yy, xx = np.mgrid[0:n, 0:n].astype(f32)
    d = np.minimum(np.minimum(xx, n - 1 - xx), np.minimum(yy, n - 1 - yy))
    wob = MT.fbm(n, 2.6, 1, 1, seed) * (0.055 * n)
    w0, soft = 0.13 * n, max(4.0, n / 64.0)
    m[qy * n:(qy + 1) * n, qx * n:(qx + 1) * n] = np.clip((d + wob - w0) / soft, 0, 1)
    return m


def stone_atlas(key, report):
    n = STONE[key]
    jid = "jp_m_" + key
    rng = np.random.default_rng(fnv("fx4|" + key))
    # one layout for the three wears (a model keeps its look when its wear changes)
    plan = []
    for q in (1, 2, 3):
        plan.append({"q": q, "k": int(rng.integers(0, 4)) if key in ISO else 2 * int(rng.integers(0, 2)),
                     "flip": bool(rng.random() < 0.5),
                     "dx": int(rng.integers(0, n)), "dy": int(rng.integers(0, n)), "seed": int(rng.integers(1, 1 << 30))})
    if all(p["k"] == 0 and not p["flip"] for p in plan):
        plan[0]["k"] = 1 if key in ISO else 2
    rec = {"tile_px": n, "atlas_px": 2 * n, "plan": [{k: v for k, v in p.items() if k != "seed"} for p in plan],
           "wears": {}}
    masks = [quad_mask(n, p["q"], p["seed"]) for p in plan]
    for lv in range(3):
        stem = "%s_w%d" % (jid, lv)
        maps = {m: tile("%s_%s.png" % (stem, m), n) for m in MAPS}
        mp = os.path.join(TEX, stem + "_mask.png")
        has_mask = os.path.isfile(mp)
        maps["mask"] = tile(stem + "_mask.png", n, "L") if has_mask else np.zeros((n, n), f32)
        keep_t = maps["mask"] < 0.5
        mt = maps["co"][keep_t].mean(0)
        at = {k: np.tile(v, (2, 2, 1) if v.ndim == 3 else (2, 2)) for k, v in maps.items()}
        for p, w in zip(plan, masks):
            v = orient(maps, p["k"], p["flip"], p["dx"], p["dy"])
            kv = v["mask"] < 0.5
            for _ in range(3):
                v["co"] = np.clip(v["co"] * (mt / np.maximum(v["co"][kv].mean(0), 1e-4)), 0, 1)
            vt = {k: np.tile(a, (2, 2, 1) if a.ndim == 3 else (2, 2)) for k, a in v.items()}
            for k in at:
                if k == "mask":
                    at[k] = np.where(w > 0.5, vt[k], at[k])
                else:
                    at[k] = at[k] * (1 - w[..., None]) + vt[k] * w[..., None]
        nv = at["nohq"] * 2 - 1                                           # renormalise the blended normals
        nv[..., 2] = np.maximum(nv[..., 2], 0.05)
        nv = nv / np.linalg.norm(nv, axis=-1, keepdims=True)
        at["nohq"] = nv * 0.5 + 0.5
        keep = at["mask"] < 0.5
        for _ in range(4):
            at["co"] = np.clip(at["co"] * (mt / np.maximum(at["co"][keep].mean(0), 1e-4)), 0, 1)
        for m in MAPS:
            save(at[m], "%s_%s.png" % (stem, m))
        if has_mask:
            save(at["mask"], stem + "_mask.png")
        dE = float(np.linalg.norm(MT.srgb_to_lab(at["co"][keep].mean(0) * 255) - MT.srgb_to_lab(mt * 255)))
        qL = []
        for q in range(4):
            qy, qx = divmod(q, 2)
            sl = (slice(qy * n, (qy + 1) * n), slice(qx * n, (qx + 1) * n))
            qL.append(round(float(MT.srgb_to_lab(at["co"][sl][keep[sl]].mean(0) * 255)[0]), 1))
        rec["wears"]["_w%d" % lv] = {"atlas_vs_tile_dE": round(dE, 3), "quadrant_L": qL}
    report[key] = rec
    print("  %-18s %4d -> %4d px  quadrant L* (w1) %s  dE %.3f" % (key, n, 2 * n, rec["wears"]["_w1"]["quadrant_L"],
                                                                   rec["wears"]["_w1"]["atlas_vs_tile_dE"]))


# ------------------------------------------------------------------------------------------------ macro
def macro_stone(lv, S=1024):
    g = MT.fbm(S, 3.3, 1, 1, 701)
    b = MT.fbm(S, 3.0, 1, 1, 702)
    fine = 1 + 0.08 * MT.fbm(S, 2.0, 1, 1, 703)
    grime = np.clip((g - 0.3) / 1.3, 0, 1)
    bleach = np.clip((b - 0.5) / 1.2, 0, 1) * (1 - grime)
    w = (grime / (grime + bleach * 0.6 + 1e-4))[..., None]
    cd = np.array([40, 40, 34], f32) / 255 * fine[..., None]              # wet grime, dark grey-green
    cb = np.array([150, 152, 140], f32) / 255 * fine[..., None]           # pale lichen-grey bleach
    rgb = cd * w + cb * (1 - w)
    alpha = np.maximum(grime, bleach * 0.6) * [0.16, 0.26, 0.36][lv]
    return np.concatenate([rgb, alpha[..., None]], -1)


def macro_shift(key, mc):
    out = {}
    n = STONE[key]
    for lv in range(3):
        co = tile("jp_m_%s_w%d_co.png" % (key, lv), n)
        a = mc[lv][..., 3:4]
        before = co.reshape(-1, 3).mean(0)
        after = before * (1 - a.mean()) + (mc[lv][..., :3] * a).reshape(-1, 3).mean(0)
        out["_w%d" % lv] = round(float(np.linalg.norm(MT.srgb_to_lab(after * 255) - MT.srgb_to_lab(before * 255))), 2)
    return out


def sidecar(key):
    return os.path.join(LIB, "stone", "jp_m_%s.json" % key)


def macro_for_stone(mid, wear):
    """(texture, aside, up) for a stone library id, or None (called by make_wood_atlas.macro_for)."""
    key = mid[5:] if mid.startswith("jp_m_") else mid
    if key not in STONE:
        return None
    sc = json.load(open(sidecar(key), encoding="utf-8"))
    at = sc.get("atlas") or {}
    w = at.get("w_m", 2.0 * float(sc["tile_size_m"]))
    s = round(w / MACRO_REPEAT_M, 4)
    return MACRO_TEX % wear[1:], s, s


def patch_rvmats():
    import make_wood_atlas as WA
    n = 0
    for key in STONE:
        for wear in ("_w0", "_w1", "_w2"):
            p = os.path.join(LIB, "stone", "jp_m_%s%s.rvmat" % (key, wear))
            txt = open(p, "rb").read().decode("utf-8")
            new = WA.with_macro(txt, "jp_m_" + key, wear)
            if new != txt:
                with open(p, "wb") as f:
                    f.write(new.encode("utf-8"))
                n += 1
    print("rvmats: %d stone rvmats given the Stage3 macro" % n)


def patch_sidecars():
    for key, n in STONE.items():
        p = sidecar(key)
        sc = json.load(open(p, encoding="utf-8"))
        t = float(sc["tile_size_m"])
        sc["texture_px"] = [2 * n, 2 * n]
        sc["atlas"] = {"w_m": 2 * t, "h_m": 2 * t, "patches": 4, "lock": None, "roll_px": 0, "kind": "stone",
                       "px": [2 * n, 2 * n], "turn": "any" if key in ISO else "small",
                       "note": "FX4: 2 x 2 tile atlas (the tile + 3 turned / mirrored / rolled variants cut in along "
                               "irregular lines); tile_size_m stays the tile, parts/kit/jpparts/uvwood.py turns + "
                               "offsets + maybe mirrors each stone face / solid into it"}
        s = round(2 * t / MACRO_REPEAT_M, 4)
        sc["macro"] = {"stage3": MACRO_TEX % "w<n>", "aside_up": [s, s]}
        with open(p, "wb") as f:
            f.write(json.dumps(sc, indent=1, ensure_ascii=False).encode("utf-8"))
    print("sidecars: %d stone materials updated" % len(STONE))


def paa_pairs():
    pairs = []
    for key in STONE:
        for lv in range(3):
            for suf in MAPS:
                nm = "jp_m_%s_w%d_%s" % (key, lv, suf)
                pairs.append((os.path.join(TEX, nm + ".png"), os.path.join(LIB, "stone", nm + ".paa")))
    for lv in range(3):
        nm = "jp_m_macro_stone_w%d_mc" % lv
        pairs.append((os.path.join(TEX, nm + ".png"), os.path.join(LIB, "macro", nm + ".paa")))
    return pairs


def to_paa(pairs):
    """build_materials.to_paa with at most 4 ImageToPAA processes (README rule 2b)."""
    import build_materials as BM
    todo = [(a, b) for a, b in pairs if not (os.path.isfile(b) and os.path.getmtime(b) >= os.path.getmtime(a))]

    def one(pp):
        png, paa = pp
        os.makedirs(os.path.dirname(paa), exist_ok=True)
        r = BM.run([BM.IMAGE_TO_PAA, png, paa])
        if r.returncode != 0 or not os.path.isfile(paa):
            raise RuntimeError("ImageToPAA failed for %s: %s" % (png, (r.stdout + r.stderr).strip()))
    with cf.ThreadPoolExecutor(4) as ex:
        list(ex.map(one, todo))
    print("paa: %d converted, %d up to date" % (len(todo), len(pairs) - len(todo)))


def check():
    bad = []
    for key, n in STONE.items():
        for lv in range(3):
            png = os.path.join(TEX, "jp_m_%s_w%d_co.png" % (key, lv))
            if Image.open(png).size != (2 * n, 2 * n):
                bad.append("%s not an atlas" % png)
    for png, paa in paa_pairs():
        if not os.path.isfile(paa) or os.path.getmtime(paa) < os.path.getmtime(png):
            bad.append("%s older than its png" % paa)
    print("\n".join(bad) if bad else "FX4 stone atlas check: OK (%d PAAs)" % len(paa_pairs()))
    return not bad


def main(argv):
    if "--check" in argv:
        return 0 if check() else 1
    report = {"stone": {}}
    print("stone atlases")
    for key in STONE:
        stone_atlas(key, report["stone"])
    print("stone macro")
    mc = [macro_stone(lv) for lv in range(3)]
    for lv in range(3):
        save(mc[lv], "jp_m_macro_stone_w%d_mc.png" % lv)
    report["macro_shift_dE"] = {k: macro_shift(k, mc) for k in STONE}
    print("  macro mean shift dE", report["macro_shift_dE"])
    patch_sidecars()
    to_paa(paa_pairs())
    patch_rvmats()
    with open(REPORT, "wb") as f:
        f.write(json.dumps(report, indent=1).encode("utf-8"))
    return 0 if check() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
