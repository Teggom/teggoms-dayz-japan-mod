#!/usr/bin/env python3
r"""FX3 DRAFT textures (phase 1; nothing shared is written): wood atlases, macro (MC) weathering layers, the thatch
_w2 base without baked moss, the irregular moss decal, and draft rvmats.

  python spikes/FX3/make_atlases.py            everything -> spikes/FX3/drafts/textures/*.png, spikes/FX3/rvmats/
  python spikes/FX3/make_atlases.py wood_weathered [...]   only those wood atlases

Wood atlas (one per material and wear, same file names as today, so rvmats and p3d texture paths do not change):
  2048 x 1024 px = 4 m across the grain x 2 m along it (512 px/m, as the library).
  left 1024 px  = today's tile, rolled sideways so a board joint sits at u = 0 (pixel-locked materials: not rolled);
  right 1024 px = a board-shuffled variant with the SAME joints: every board gets the content of another board of
                  the tile (shifted and maybe flipped along the grain, tone jittered), the left half of the variant a
                  little greyer (weathered), the right half a little warmer (fresher). Joint pixels are kept.
  Patches A | B | C | D = the four 512 px columns. Both strip seams are board joints, so the strip tiles across u;
  every column tiles along v. The variant is rescaled to the tile's mean colour (per channel, unmasked pixels), so
  the atlas mean is today's mean: the palette check (C1 / matcheck) is unchanged by construction.
  Inputs are the CURRENT library PNGs (data/materials/textures, whatever agent made them), so every maker's look is
  kept; phase 2 runs this as a post step after the makers.

Macro (Super shader Stage3, MC, uvSource="tex" + a non-uniform uvTransform, as 1,700 vanilla rvmats do):
  jp_m_macro_wood_w{0,1,2}_mc   grime clouds, sun-bleach, water streaks along v; alpha 0.22 / 0.38 / 0.52 max
  jp_m_macro_thatch_w{1,2}_mc   _w1 grime + sun-bleach; _w2 irregular moss carpets (moved here from the _w2 tile)
Moss decal jp_m_decal_moss: 1024 px = 2 m (was 256 px = 0.5 m), irregular cushions in drifts, cut alpha (FP1 rule).
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
sys.path.insert(0, os.path.join(DEV, "research", "materials"))
import make_textures as MT  # noqa: E402  (read-only import: noise, palette targets, recolour)

TEX = os.path.join(DEV, "data", "materials", "textures")
LIB = os.path.join(DEV, "src", "JP", "common", "materials")
OUT = os.path.join(HERE, "drafts", "textures")
RVOUT = os.path.join(HERE, "rvmats")
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
    J = joints(load("%s_w1_co.png" % jid))
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
        maps = {"co": load(stem + "_co.png"), "n": load(stem + "_nohq.png"), "smdi": load(stem + "_smdi.png")}
        mp = os.path.join(TEX, stem + "_mask.png")
        maps["mask"] = load(stem + "_mask.png", "L") if os.path.isfile(mp) else np.zeros((S, S), f32)
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
        co = load("jp_m_%s_w%d_co.png" % (mid, lv))
        m = mc[lv]
        if m is None:
            continue
        a = m[..., 3:4]
        before = co.reshape(-1, 3).mean(0)
        after = co.reshape(-1, 3).mean(0) * (1 - a.mean()) + (m[..., :3] * a).reshape(-1, 3).mean(0)
        out["_w%d" % lv] = round(float(np.linalg.norm(MT.srgb_to_lab(after * 255) - MT.srgb_to_lab(before * 255))), 2)
    return out


# ------------------------------------------------------------------------------------------------ thatch _w2 base
def thatch_w2_base():
    t = MT.tgt("thatch_weathered", -3, toward="stone_lantern", t=0.18)
    a, pn, pr = MT.reed(S)
    co = MT.recolor(a, t, 1.25, 0.1)
    h, sh = MT.courses(S, 5, 111, 1.0)
    co = co * (1 - 0.18 * sh)[..., None]
    h = h - 3.0 * np.clip(MT.fbm(S, 3.2, 1, 1, 114) - 0.5, 0, None)
    n = MT.combine(pn, MT.h2n(h, 2.0))
    co = MT.fix_mean(co.astype(f32), t, np.ones((S, S), bool))
    rough = np.clip(pr, 0, 1)
    smdi = np.stack([np.ones((S, S)), 0.08 * (1 - rough), 0.15 * (1 - rough)], -1)
    old = load("jp_m_roof_thatch_w2_co.png")
    msk = load("jp_m_roof_thatch_w2_mask.png", "L") < 0.5
    diff = float(np.abs(old[msk] - co[msk]).mean() * 255)
    save(co, "jp_m_roof_thatch_w2_co.png")
    save(n * 0.5 + 0.5, "jp_m_roof_thatch_w2_nohq.png")
    save(smdi, "jp_m_roof_thatch_w2_smdi.png")
    return diff


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
    stem = "jp_m_decal_moss_w%d" % lv
    save(np.concatenate([co, alpha[..., None]], -1), stem + "_ca.png")
    save(n * 0.5 + 0.5, stem + "_nohq.png")
    save(smdi, stem + "_smdi.png")
    return {"coverage": round(float((alpha > 0.5).mean()), 3), "semi": round(float(((alpha > 0.05) & (alpha < 0.95)).mean()), 4)}


# ------------------------------------------------------------------------------------------------ draft rvmats
def stage3(tex, su, sv):
    return ('class Stage3\n{\n\ttexture="%s";\n\tuvSource="tex";\n\tclass uvTransform\n\t{\n\t\taside[]={%s,0,0};\n'
            '\t\tup[]={0,%s,0};\n\t\tdir[]={0,0,0};\n\t\tpos[]={0,0,0};\n\t};\n};\n' % (tex, su, sv))


def draft_rvmat(fam, mid, wear, macro_tex, kind):
    src = os.path.join(LIB, fam, "jp_m_%s%s.rvmat" % (mid, wear))
    txt = open(src, "rb").read().decode("utf-8")
    su, sv = MACRO[kind]
    new = re.sub(r"class Stage3\n\{.*?\n\};\n", lambda m: stage3(macro_tex, su, sv), txt, count=1, flags=re.S)
    assert new != txt
    os.makedirs(RVOUT, exist_ok=True)
    with open(os.path.join(RVOUT, "jp_m_%s%s.rvmat" % (mid, wear)), "wb") as f:
        f.write(new.encode("utf-8"))


def preview(mids):
    """One small jpg of the _w1 atlases (committed; the full drafts are not)."""
    rows = []
    for mid in mids:
        im = Image.open(os.path.join(OUT, "jp_m_%s_w1_co.png" % mid)).resize((512, 256), Image.LANCZOS)
        rows.append(np.asarray(im))
    sheet = np.concatenate(rows, 0)
    Image.fromarray(sheet).save(os.path.join(HERE, "fx3_atlases_w1.jpg"), quality=85)


def main(argv):
    mids = argv or WOOD
    report = {"wood": {}, "macro_uv": MACRO}
    print("wood atlases")
    for mid in mids:
        wood_atlas(mid, report["wood"])
    if argv:
        return
    print("macro layers")
    mw = [macro_wood(lv) for lv in range(3)]
    for lv in range(3):
        save(mw[lv], "jp_m_macro_wood_w%d_mc.png" % lv)
    mth = [None, macro_thatch(1), macro_thatch(2)]
    for lv in (1, 2):
        save(mth[lv], "jp_m_macro_thatch_w%d_mc.png" % lv)
    mwd = [macro_wood(lv, dk=True) for lv in range(3)]
    for lv in range(3):
        save(mwd[lv], "jp_m_macro_wood_dark_w%d_mc.png" % lv)
    mwi = [macro_wood(lv, interior=True) for lv in range(3)]
    for lv in range(3):
        save(mwi[lv], "jp_m_macro_wood_int_w%d_mc.png" % lv)
    report["macro_shift_dE"] = {mid: macro_shift(mid, mwd if mid in DARK else (mwi if mid in INTERIOR else mw))
                                for mid in WOOD}
    report["macro_shift_dE"]["roof_thatch"] = macro_shift("roof_thatch", mth)
    report["macro_alpha_mean"] = {"wood": [round(float(m[..., 3].mean()), 3) for m in mw],
                                  "thatch": [None] + [round(float(mth[k][..., 3].mean()), 3) for k in (1, 2)],
                                  "thatch_w2_moss_cover": round(float((mth[2][..., 3] > 0.4).mean()), 3)}
    print("thatch _w2 base without baked moss")
    report["thatch_w2_regen_mean_abs_diff_outside_old_moss"] = round(thatch_w2_base(), 2)
    print("moss decal")
    report["moss_decal"] = {"_w%d" % lv: moss_decal(lv) for lv in range(3)}
    print("draft rvmats")
    for lv in range(3):
        draft_rvmat("wood", "wood_weathered", "_w%d" % lv, "JP\\common\\materials\\macro\\jp_m_macro_wood_w%d_mc.paa" % lv,
                    "wood")
    for lv in (1, 2):
        draft_rvmat("roof", "roof_thatch", "_w%d" % lv,
                    "JP\\common\\materials\\macro\\jp_m_macro_thatch_w%d_mc.paa" % lv, "thatch")
    preview(WOOD)
    with open(os.path.join(HERE, "atlas_report.json"), "wb") as f:
        f.write(json.dumps(report, indent=1).encode("utf-8"))
    print(json.dumps({k: report[k] for k in ("macro_shift_dE", "macro_alpha_mean", "moss_decal",
                                             "thatch_w2_regen_mean_abs_diff_outside_old_moss")}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
