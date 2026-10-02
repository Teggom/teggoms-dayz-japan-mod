#!/usr/bin/env python3
r"""make_wood_atlas.py - FX3 (2026-10-01): wood texture variety, the materials half (the kit half is
parts/kit/jpparts/uvwood.py). A POST STEP after the makers (build_materials / make_textures, make_b1, make_m1 ...).

  python research/materials/make_wood_atlas.py            atlases + macro + thatch _w2 + moss -> PNG, PAA, rvmats, sidecars
  python research/materials/make_wood_atlas.py --check    every atlas material's library PNG is 2048 wide and its PAAs
                                                          are newer (exit 1 otherwise)
  then pack jp_common (python research/materials/build_materials.py --rvmats-only keeps the macro; or its pack()).

PITFALL: a maker re-run rewrites a wood material's PNG as the old 1024 tile; run this step again afterwards (it starts
from the maker's fresh 1024 PNG and keeps a copy in data/materials/textures/_tile/; on its own 2048 output it reads
that copy). uvwood refuses to remap a material whose PNG is not an atlas, so a forgotten step fails loudly.

Wood atlas (one per material and wear, same file names, so rvmats and p3d texture paths do not change):
  2048 x 1024 px = 4 m across the grain x 2 m along it (512 px/m, as the library).
  left 1024 px  = the maker's tile, rolled sideways so a board joint sits at u = 0 (pixel-locked: not rolled);
  right 1024 px = a board-shuffled variant with the SAME joints: every board gets the content of another board of
                  the tile (shifted and maybe flipped along the grain, tone jittered), the left half of the variant a
                  little greyer (weathered), the right half a little warmer (fresher). Joint pixels are kept.
  Patches A | B | C | D = the four 512 px columns. Both strip seams are board joints, so the strip tiles across u;
  every column tiles along v. The variant is rescaled to the tile's mean colour (per channel, unmasked pixels), so
  the atlas mean is the tile's mean: the palette check is unchanged by construction.

Macro (Super shader Stage3, MC, uvSource="tex" + a non-uniform uvTransform, as ~1,850 vanilla rvmats do; MC RGB is
alpha-blended over the diffuse): jp_m_macro_wood{,_dark,_int}_w{0,1,2}_mc (grime clouds, sun-bleach, water streaks
along v; dark woods half the bleach; interior grime only) and jp_m_macro_thatch_w{1,2}_mc (_w1 grime / bleach, _w2
irregular moss carpets, moved here from the thatch _w2 tile). build_materials.rvmat_text asks macro_for() so every
rvmat writer keeps the Stage3.
Moss decal jp_m_decal_moss: 1024 px = 2 m (was 256 px = 0.5 m), irregular cushions in drifts, cut alpha (FP1 rule);
make_fp1_materials.py uses moss_b1() as its maker.
"""
import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
TILE = os.path.join(DEV, "data", "materials", "textures", "_tile")
sys.path.insert(0, HERE)
import make_textures as MT  # noqa: E402  (read-only import: noise, palette targets, recolour)

TEX = os.path.join(DEV, "data", "materials", "textures")
LIB = os.path.join(DEV, "src", "JP", "common", "materials")
OUT = TEX
REPORT = os.path.join(HERE, "FX3_ATLAS_REPORT.json")
FAM = {"wood_bengara": "paint", "floor_boards_int": "floor", "floor_boards_rough": "floor"}   # default "wood"
f32 = np.float32
S = 1024

WOOD = ["wood_weathered", "wood_street_dark", "wood_kuro", "wood_sooted", "wood_bengara", "wood_new", "wood_silver",
        "wood_interior", "ceil_boards", "floor_boards_int", "floor_boards_rough"]
DARK = {"wood_kuro", "wood_sooted", "wood_street_dark", "wood_bengara"}   # these take jp_m_macro_wood_dark_*
INTERIOR = {"wood_interior", "ceil_boards", "floor_boards_int", "floor_boards_rough"}  # jp_m_macro_wood_int_*
PIXEL_LOCKED = {"wood_interior"}          # fkit.band_fit / tansu GROOVE use its plank-band pixels: never roll
MARGIN = 4                                # px kept from the tile on each side of a joint

# macro uvTransform (aside = u scale, up = v scale), chosen so the macro repeats at a scale that never lines up with
# the wood tile: wood atlas u = 4 m, v = 2 m -> 14.7 m x 17.3 m; thatch tile 2 m -> 9.3 m x 7.7 m
MACRO = {"wood": (round(4.0 / 14.7, 4), round(2.0 / 17.3, 4)), "thatch": (round(2.0 / 9.3, 4), round(2.0 / 7.7, 4))}


def fnv(s):
    h = 2166136261
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h


def load(name, mode="RGB"):
    return np.asarray(Image.open(os.path.join(TEX, name)).convert(mode)).astype(f32) / 255.0


def tile(name, mode="RGB"):
    """The maker's 1024 tile: the library PNG if it is fresh from a maker (1024 wide; a copy goes to _tile/), else the
    _tile/ copy (the library PNG is this step's own atlas)."""
    import shutil
    p, c = os.path.join(TEX, name), os.path.join(TILE, name)
    im = Image.open(p)
    if im.size[0] == S:
        os.makedirs(TILE, exist_ok=True)
        im.close()
        shutil.copyfile(p, c)
    elif not os.path.isfile(c):
        raise RuntimeError("%s is %s wide and there is no _tile copy: re-run its maker first" % (name, im.size))
    return np.asarray(Image.open(c).convert(mode)).astype(f32) / 255.0


def save(a, name):
    os.makedirs(OUT, exist_ok=True)
    a = np.clip(a, 0, 1)
    mode = {2: "L", 3: "RGB", 4: "RGBA"}[a.ndim if a.ndim == 2 else a.shape[2]]
    Image.fromarray((a * 255 + 0.5).astype(np.uint8), mode).save(os.path.join(OUT, name))


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def circ_avg(c, k=33):
    pad = k // 2
    return np.convolve(np.r_[c[-pad:], c, c[:pad]], np.ones(k) / k, "valid")


def joints(co, minsep=40, k=0.8):
    """Board joints = dark column dips (the planks run along v). Circular, strongest first, >= minsep apart."""
    c = lum(co).mean(0)
    cs = c - circ_avg(c)
    thr = -k * cs.std()
    n = len(c)
    cand = [x for x in range(n) if cs[x] < thr and cs[x] <= cs[x - 1] and cs[x] <= cs[(x + 1) % n]]
    cand.sort(key=lambda x: cs[x])
    sel = []
    for x in cand:
        if all(min(abs(x - y), n - abs(x - y)) >= minsep for y in sel):
            sel.append(x)
    return sorted(sel)


def plan_for(mid, J):
    """The board shuffle plan (identical for the three wears, so a model keeps its layout when its wear changes)."""
    rng = np.random.default_rng(fnv("fx3|" + mid))
    b = J + [S]
    boards = [(b[i], b[i + 1]) for i in range(len(J))]
    plan = []
    for i, (a0, a1) in enumerate(boards):
        w = a1 - a0
        donors = [j for j, (d0, d1) in enumerate(boards) if j != i and (d1 - d0) >= 0.8 * w] or \
                 [j for j in range(len(boards)) if j != i] or [i]
        j = int(rng.choice(donors))
        d0, d1 = boards[j]
        wt, wd = w - 2 * MARGIN, (d1 - d0) - 2 * MARGIN
        off = int(rng.integers(0, max(1, wd - wt + 1))) if wd >= wt else 0
        plan.append({"tgt": (a0, a1), "src": (d0, d1), "off": off, "vroll": int(rng.integers(0, S)),
                     "vflip": bool(rng.random() < 0.5), "tone": float(1 + rng.normal(0, 0.035)),
                     "char": "weathered" if (a0 + a1) / 2 < S / 2 else "fresh"})
    return plan


def shuffled(maps, plan):
    """maps: {'co', 'n', 'smdi', 'mask'} (rolled tile). Returns the variant tile."""
    out = {k: v.copy() for k, v in maps.items()}
    for p in plan:
        a0, a1 = p["tgt"]
        d0, d1 = p["src"]
        wt, wd = (a1 - a0) - 2 * MARGIN, (d1 - d0) - 2 * MARGIN
        if wt <= 0 or wd <= 0:
            continue
        if wd >= wt:
            cols = np.arange(d0 + MARGIN + p["off"], d0 + MARGIN + p["off"] + wt) % S
        else:                                                     # a narrower donor: stretch it a little
            cols = (d0 + MARGIN + np.floor(np.arange(wt) * wd / wt).astype(int)) % S
        rows = (np.arange(S) + p["vroll"]) % S
        if p["vflip"]:
            rows = rows[::-1]
        tc = np.arange(a0 + MARGIN, a1 - MARGIN) % S
        for k, v in maps.items():
            blk = v[np.ix_(rows, cols)].copy()
            if k == "co":
                blk = blk * p["tone"]
                if p["char"] == "weathered":
                    blk = MT.grey(blk, 0.10) * 0.985
                else:
                    blk = blk * np.array([1.02, 1.0, 0.975], f32)
            if k == "n" and p["vflip"]:
                blk[..., 1] = 1.0 - blk[..., 1]                   # DirectX green = down: a v flip negates it
            out[k][:, tc] = blk
    return out


def wood_atlas(mid, report):
    jid = "jp_m_" + mid
    J = joints(tile("%s_w1_co.png" % jid))
    if mid in PIXEL_LOCKED:
        roll = 0
    else:
        j0 = min(J, key=lambda x: min(x, S - x))
        roll = -j0
    Jr = sorted(((x + roll) % S) for x in J)
    if 0 not in Jr and mid not in PIXEL_LOCKED:
        Jr = [0] + Jr
    if mid in PIXEL_LOCKED and Jr[0] != 0:
        Jr = [0] + [x for x in Jr if x > MARGIN]
    plan = plan_for(mid, Jr)
    rec = {"joints": len(Jr), "roll_px": roll, "wears": {}}
    for lv in range(3):
        stem = "%s_w%d" % (jid, lv)
        maps = {"co": tile(stem + "_co.png"), "n": tile(stem + "_nohq.png"), "smdi": tile(stem + "_smdi.png")}
        mp = os.path.join(TEX, stem + "_mask.png")
        maps["mask"] = tile(stem + "_mask.png", "L") if os.path.isfile(mp) else np.zeros((S, S), f32)
        maps = {k: np.roll(v, roll, axis=1) for k, v in maps.items()}
        var = shuffled(maps, plan)
        keep_t = maps["mask"] < 0.5
        keep_v = var["mask"] < 0.5
        mt = maps["co"][keep_t].mean(0)
        for _ in range(4):
            var["co"] = np.clip(var["co"] * (mt / np.maximum(var["co"][keep_v].mean(0), 1e-4)), 0, 1)
        at = {k: np.concatenate([maps[k], var[k]], axis=1) for k in maps}
        save(at["co"], stem + "_co.png")
        save(at["n"], stem + "_nohq.png")
        save(at["smdi"], stem + "_smdi.png")
        if at["mask"].max() > 0:
            save(at["mask"], stem + "_mask.png")
        keep = at["mask"] < 0.5
        dE = float(np.linalg.norm(MT.srgb_to_lab(at["co"][keep].mean(0) * 255) - MT.srgb_to_lab(mt * 255)))
        pm = [MT.srgb_to_lab(at["co"][:, k * 512:(k + 1) * 512][keep[:, k * 512:(k + 1) * 512]].mean(0) * 255)[0]
              for k in range(4)]
        rec["wears"]["_w%d" % lv] = {"atlas_vs_tile_dE": round(dE, 2), "patch_L": [round(float(x), 1) for x in pm]}
    report[mid] = rec
    print("  %-20s joints %2d roll %5d  patch L* (w1) %s" % (mid, len(Jr), roll, rec["wears"]["_w1"]["patch_L"]))


# ------------------------------------------------------------------------------------------------ macro layers
def macro_wood(lv, dk=False, interior=False):
    g = MT.fbm(S, 3.4, 1, 1, 501)
    b = MT.fbm(S, 3.2, 1, 1, 502)
    st = MT.fbm(S, 2.2, 1, 10, 503)
    where = np.clip(MT.fbm(S, 3.0, 1, 1, 504) * 0.8 + 0.2, 0, 1)
    grime = np.clip((g - 0.35) / 1.3, 0, 1)
    streak = np.clip((st - 0.6) / 1.0, 0, 1) * where
    bleach = np.clip((b - 0.45) / 1.2, 0, 1) * (1 - grime)
    dark = np.maximum(grime, streak * 0.8)
    if interior:                                                  # indoors: no sun, no rain: dust / grime only
        bleach = bleach * 0.0
        dark = grime
    a = np.maximum(dark, bleach * 0.55)
    fine = 1 + 0.08 * MT.fbm(S, 2.0, 1, 1, 505)
    cd = np.array([24, 21, 18] if dk else [52, 46, 40], f32) / 255 * fine[..., None]
    cb = np.array([96, 94, 88] if dk else [150, 147, 138], f32) / 255 * fine[..., None]
    if dk:                                                        # dark woods: palette tolerance 6 (kuro): less bleach
        bleach = bleach * 0.5
    w = (dark / (dark + bleach * 0.55 + 1e-4))[..., None]
    rgb = cd * w + cb * (1 - w)
    alpha = a * ([0.12, 0.18, 0.25] if interior else [0.22, 0.38, 0.52])[lv]
    return np.concatenate([rgb, alpha[..., None]], -1)


def macro_thatch(lv):
    g = np.clip((MT.fbm(S, 3.2, 1, 1, 611) - 0.2) / 1.2, 0, 1)
    b = np.clip((MT.fbm(S, 3.0, 1, 1, 612) - 0.5) / 1.2, 0, 1) * (1 - g)
    fine = MT.fbm(S, 1.6, 1, 1, 603)
    if lv == 1:
        a = np.maximum(g * 0.25, b * 0.2)
        w = (g / (g + b + 1e-4))[..., None]
        rgb = np.array([58, 52, 40], f32) / 255 * w + np.array([168, 160, 140], f32) / 255 * (1 - w)
        return np.concatenate([rgb, a[..., None]], -1)
    D = MT.fbm(S, 3.6, 1, 1, 601)                                 # where moss can live at all (very broad)
    C = MT.fbm(S, 2.3, 1, 1, 602)                                 # carpets
    moss = np.clip((0.9 * C + 1.1 * D + 0.35 * fine - 0.9) / 0.35, 0, 1)
    moss = moss * np.clip(0.75 + 0.35 * fine, 0, 1)
    col = np.array([70, 86, 42], f32) / 255
    rgb = np.broadcast_to(col, (S, S, 3)).copy()
    rgb = MT.mix(rgb, (98, 104, 50), np.clip(fine, 0, 1) * 0.5)
    rgb = MT.mix(rgb, (46, 58, 30), np.clip(C - 0.8, 0, 1) * 0.6)
    gm = g * 0.25 * (1 - moss)
    rgb = MT.mix(rgb, (58, 52, 40), np.where(moss > 0.05, 0.0, 1.0))
    a = np.maximum(moss * 0.82, gm)
    return np.concatenate([rgb, a[..., None]], -1)


def macro_shift(mid, mc):
    """Expected in-game mean colour shift of a material under its macro (alpha-lerp), dE76."""
    out = {}
    for lv in range(3):
        co = tile("jp_m_%s_w%d_co.png" % (mid, lv)) if mid in WOOD else load("jp_m_%s_w%d_co.png" % (mid, lv))
        m = mc[lv]
        if m is None:
            continue
        a = m[..., 3:4]
        before = co.reshape(-1, 3).mean(0)
        after = co.reshape(-1, 3).mean(0) * (1 - a.mean()) + (m[..., :3] * a).reshape(-1, 3).mean(0)
        out["_w%d" % lv] = round(float(np.linalg.norm(MT.srgb_to_lab(after * 255) - MT.srgb_to_lab(before * 255))), 2)
    return out


# ------------------------------------------------------------------------------------------------ moss decal
def moss_decal(lv):
    t = [MT.tgt("moss_on_stone", 4, -4, -6), MT.tgt("moss_on_stone"), MT.tgt("moss_on_stone", -4, -2, 2)][lv]
    var = MT.fbm(S, 2.2, 1, 1, 3101)
    co = (np.asarray(t, f32) / 255)[None, None, :] * (1 + 0.12 * var)[..., None]
    co = MT.mix(co, (150, 150, 78), np.clip(var, 0, 1) * 0.3)
    co = MT.mix(co, (78, 92, 46), np.clip(-var, 0, 1) * 0.3)
    tips = MT.spots(S, 3200, 6, 0.6, 1.5, 10, 3102)
    co = MT.mix(co, (170, 170, 110), tips * 0.4)
    dens = MT.fbm(S, 3.5, 1, 1, 3110)                             # drifts: whole regions bare, others thick
    clump = MT.fbm(S, 2.5, 1, 1, 3111)
    rag = MT.fbm(S, 1.4, 1, 1, 3112)                              # ragged edges
    mask = np.zeros((S, S), bool)
    if lv == 0:                                                   # lichen + a few young cushions, clustered
        sp = MT.spots(S, 260, 10, 1.5, 6, 18, 3103) * (dens > 0.2)
        cush = np.clip((clump + 0.8 * dens + 0.25 * rag - 1.9) / 0.15, 0, 1)
        field = np.maximum(sp, cush)
    elif lv == 1:
        cush = MT.spots(S, 420, 9, 3, 14, 26, 3113) * (dens > -0.1)
        field = np.maximum(np.clip((clump + 0.9 * dens + 0.3 * rag - 1.1) / 0.15, 0, 1), cush * (rag > -0.6))
    else:
        cush = MT.spots(S, 520, 10, 4, 18, 30, 3114) * (dens > -0.5)
        field = np.maximum(np.clip((clump + 0.9 * dens + 0.3 * rag - 0.5) / 0.15, 0, 1), cush * (rag > -0.8))
        lf = MT.spots(S, 160, 4, 3, 6, 20, 3105) * (dens > 0.0)
        co = MT.mix(co, (122, 78, 40), lf * 0.95)
        field = np.maximum(field, lf)
        mask = lf > 0.3
    holes = MT.spots(S, 300, 4, 2, 7, 12, 3115) * (rag < 0.3)    # bare stone showing through the carpets
    field = field * (1 - holes)
    alpha = np.clip((MT.blur(field.astype(f32), 1.0) - 0.5) * 6 + 0.5, 0, 1)   # cut, 1-2 px edge (FP1 rule)
    alpha = np.where(alpha < 0.1, 0.0, np.where(alpha > 0.9, 1.0, alpha)).astype(f32)
    keep = (alpha > 0.5) & ~mask
    co = MT.fix_mean(co.astype(f32), t, keep)
    h = MT.blur(alpha, 3) * 3 + tips + var
    n = MT.h2n(h.astype(f32), 1.5)
    smdi = np.stack([np.ones((S, S)), np.full((S, S), 0.05 * 0.05), np.full((S, S), 0.1 * 0.05)], -1)
    return co, alpha, n, mask, t


def moss_b1(lv, S_):
    """make_fp1_materials' maker for jp_m_decal_moss (B1 recipe format: R dict with alpha)."""
    import make_b1_materials as B
    assert S_ == S, "jp_m_decal_moss is 1024 px (2 m) since FX3"
    co, alpha, n, mask, t = moss_decal(lv)
    return B.R(co, n, 0.95, mask, t, 0.05, 0.1, alpha=alpha)


def write_moss(lv):
    co, alpha, n, mask, t = moss_decal(lv)
    smdi = np.stack([np.ones((S, S)), np.full((S, S), 0.05 * 0.05), np.full((S, S), 0.1 * 0.05)], -1)
    stem = "jp_m_decal_moss_w%d" % lv
    save(np.concatenate([co, alpha[..., None]], -1), stem + "_ca.png")
    save(co, stem + "_co.png")
    save(n * 0.5 + 0.5, stem + "_nohq.png")
    save(smdi, stem + "_smdi.png")
    mp = os.path.join(TEX, stem + "_mask.png")
    if mask.any():
        save(mask.astype(f32), stem + "_mask.png")
    elif os.path.isfile(mp):
        os.remove(mp)
    return {"coverage": round(float((alpha > 0.5).mean()), 3),
            "semi": round(float(((alpha > 0.05) & (alpha < 0.95)).mean()), 4)}


# ------------------------------------------------------------------------------------------------ rvmats (Stage3)
MACRO_TEX = "JP\\common\\materials\\macro\\jp_m_macro_%s_%s_mc.paa"


def macro_for(mid, wear):
    """(texture, aside, up) of the Stage3 macro for library id jp_m_<key> and wear '_w0'..; None = no macro."""
    key = mid[5:] if mid.startswith("jp_m_") else mid
    if key in WOOD:
        kind = "wood_dark" if key in DARK else ("wood_int" if key in INTERIOR else "wood")
        su, sv = MACRO["wood"]
        return MACRO_TEX % (kind, wear[1:]), su, sv
    if key == "roof_thatch" and wear in ("_w1", "_w2"):
        su, sv = MACRO["thatch"]
        return MACRO_TEX % ("thatch", wear[1:]), su, sv
    return None


def stage3(tex, su, sv):
    return ('class Stage3\n{\n\ttexture="%s";\n\tuvSource="tex";\n\tclass uvTransform\n\t{\n\t\taside[]={%s,0,0};\n'
            '\t\tup[]={0,%s,0};\n\t\tdir[]={0,0,0};\n\t\tpos[]={0,0,0};\n\t};\n};\n' % (tex, su, sv))


def with_macro(txt, mid, wear):
    """An rvmat text with its Stage3 set from macro_for (unchanged if there is none)."""
    m = macro_for(mid, wear)
    if not m:
        return txt
    return re.sub(r"class Stage3\n\{.*?\n\};\n", lambda _: stage3(*m), txt, count=1, flags=re.S)


def fam_of(key):
    return FAM.get(key, "wood")


def patch_rvmats():
    n = 0
    for key, fam in [(k, fam_of(k)) for k in WOOD] + [("roof_thatch", "roof")]:
        for wear in ("_w0", "_w1", "_w2"):
            p = os.path.join(LIB, fam, "jp_m_%s%s.rvmat" % (key, wear))
            txt = open(p, "rb").read().decode("utf-8")
            new = with_macro(txt, "jp_m_" + key, wear)
            if new != txt:
                with open(p, "wb") as f:
                    f.write(new.encode("utf-8"))
                n += 1
    print("rvmats: %d given the Stage3 macro" % n)


def patch_sidecars(report):
    for key in WOOD:
        p = os.path.join(LIB, fam_of(key), "jp_m_%s.json" % key)
        sc = json.load(open(p, encoding="utf-8"))
        sc["texture_px"] = [2 * S, S]
        sc["atlas"] = {"w_m": 4.0, "h_m": 2.0, "patches": 4, "lock": "band" if key in PIXEL_LOCKED else None,
                       "roll_px": report["wood"][key]["roll_px"] % S,
                       "note": "FX3: 4 m x 2 m atlas (tile + board-shuffled variant); tile_size_m stays the board "
                               "tile, parts/kit/jpparts/uvwood.py maps the UVs into the atlas per uv group"}
        m = macro_for("jp_m_" + key, "_w1")
        sc["macro"] = {"stage3": m[0].replace("_w1_", "_w<n>_"), "aside_up": [m[1], m[2]]}
        with open(p, "wb") as f:
            f.write(json.dumps(sc, indent=1, ensure_ascii=False).encode("utf-8"))
    p = os.path.join(LIB, "stone", "jp_m_decal_moss.json")
    sc = json.load(open(p, encoding="utf-8"))
    sc.update({"tile_size_m": 2.0, "texture_px": S, "px_per_m": 512.0,
               "fx3": "1024 px = 2 m irregular drifts (was 256 px = 0.5 m); uvwood flips + offsets each decal"})
    with open(p, "wb") as f:
        f.write(json.dumps(sc, indent=1, ensure_ascii=False).encode("utf-8"))
    p = os.path.join(LIB, "roof", "jp_m_roof_thatch.json")
    sc = json.load(open(p, encoding="utf-8"))
    sc["macro"] = {"stage3": MACRO_TEX % ("thatch", "w<n>") + " (_w1, _w2)", "aside_up": list(MACRO["thatch"]),
                   "fx3": "_w2 moss lives in the macro (irregular carpets, ~9 m repeat), not in the 2 m tile"}
    if "_w2" in sc.get("wear", {}):
        sc["wear"]["_w2"]["masked_frac"] = 0.0
    with open(p, "wb") as f:
        f.write(json.dumps(sc, indent=1, ensure_ascii=False).encode("utf-8"))
    print("sidecars: %d wood + moss + thatch updated" % len(WOOD))


def paa_pairs():
    pairs = []
    for key in WOOD:
        for lv in range(3):
            for suf in ("_co", "_nohq", "_smdi"):
                n = "jp_m_%s_w%d%s" % (key, lv, suf)
                pairs.append((os.path.join(TEX, n + ".png"), os.path.join(LIB, fam_of(key), n + ".paa")))
    for kind, wears in (("wood", (0, 1, 2)), ("wood_dark", (0, 1, 2)), ("wood_int", (0, 1, 2)), ("thatch", (1, 2))):
        for lv in wears:
            n = "jp_m_macro_%s_w%d_mc" % (kind, lv)
            pairs.append((os.path.join(TEX, n + ".png"), os.path.join(LIB, "macro", n + ".paa")))
    for lv in range(3):
        for suf in ("_ca", "_nohq", "_smdi"):
            n = "jp_m_decal_moss_w%d%s" % (lv, suf)
            pairs.append((os.path.join(TEX, n + ".png"), os.path.join(LIB, "stone", n + ".paa")))
    for lv in range(3):
        for suf in ("_co", "_nohq", "_smdi"):
            n = "jp_m_roof_thatch_w%d%s" % (lv, suf)
            pairs.append((os.path.join(TEX, n + ".png"), os.path.join(LIB, "roof", n + ".paa")))
    return pairs


def check():
    bad = []
    for key in WOOD:
        for lv in range(3):
            png = os.path.join(TEX, "jp_m_%s_w%d_co.png" % (key, lv))
            if Image.open(png).size != (2 * S, S):
                bad.append("%s not an atlas" % png)
    for png, paa in paa_pairs():
        if not os.path.isfile(paa) or os.path.getmtime(paa) < os.path.getmtime(png):
            bad.append("%s older than its png" % paa)
    print("\n".join(bad) if bad else "FX3 atlas check: OK (%d PAAs)" % len(paa_pairs()))
    return not bad


def main(argv):
    if "--check" in argv:
        return 0 if check() else 1
    import build_materials as BM
    report = {"wood": {}, "macro_uv": MACRO}
    print("wood atlases")
    for mid in WOOD:
        wood_atlas(mid, report["wood"])
    print("macro layers")
    mw = [macro_wood(lv) for lv in range(3)]
    mwd = [macro_wood(lv, dk=True) for lv in range(3)]
    mwi = [macro_wood(lv, interior=True) for lv in range(3)]
    mth = [None, macro_thatch(1), macro_thatch(2)]
    for lv in range(3):
        save(mw[lv], "jp_m_macro_wood_w%d_mc.png" % lv)
        save(mwd[lv], "jp_m_macro_wood_dark_w%d_mc.png" % lv)
        save(mwi[lv], "jp_m_macro_wood_int_w%d_mc.png" % lv)
    for lv in (1, 2):
        save(mth[lv], "jp_m_macro_thatch_w%d_mc.png" % lv)
    report["macro_shift_dE"] = {mid: macro_shift(mid, mwd if mid in DARK else (mwi if mid in INTERIOR else mw))
                                for mid in WOOD}
    print("thatch (make_textures.roof_thatch: _w2 moss now in the macro)")
    MT.make("jp_m_roof_thatch")
    report["macro_shift_dE"]["roof_thatch"] = macro_shift("roof_thatch", mth)
    print("moss decal")
    report["moss_decal"] = {"_w%d" % lv: write_moss(lv) for lv in range(3)}
    BM.to_paa(paa_pairs())
    patch_rvmats()
    patch_sidecars(report)
    with open(REPORT, "wb") as f:
        f.write(json.dumps(report, indent=1).encode("utf-8"))
    return 0 if check() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
