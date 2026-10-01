#!/usr/bin/env python3
r"""make_fp2_materials.py - FP2 (Stephen's re-check, 2026-10-01): the two firewood materials redrawn through B1's
pipeline (same ids, same paths, same palette entries).

  python make_fp2_materials.py [--no-pack] [--only ID[,ID...]] [--draft]

Route of make_fp1_materials.py: B1's make_one (textures, PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped
PAA), then jp_common.pbo is repacked. Results: src/JP/common/materials/checks_fp2.json. --draft writes the colour
PNGs to spikes/FP2/look/ only.

REDRAWN (Stephen: the firewood pile outside the houses "looks like mega shit": a flat box with yellow polygon decals):
- jp_m_wood_endgrain_firewood  M1 drew ~25 rings 4.5 px apart on a 256 px disc with 22 % contrast: at any distance
                        the rings mip down to one flat yellow, so every log end read as a flat yellow polygon. Now 512 px,
                        ~11 clear annual rings (19 px apart, latewood 40 % darker) with a faint ring between, rings
                        wobble and the pith sits a little off centre, darker heartwood core, a thin pale sapwood band, a
                        dark bark ring with a cambium line, drying checks (a V check from the bark in on every level, fine
                        radial checks from the pith; more and wider with wear), saw arcs, grime toward the rim. Still
                        one log end per texture, pith at (0.5, 0.5), bark from r = 0.45 to the rim (same mapping).
- jp_m_wood_firewood    M1 recoloured the Weathered Planks photo (board joints and nail holes) for the billet sides. Now
                        a two-band texture, both tiling along v (the billet's length): u 0.0-0.5 = oak bark (grey-brown,
                        deep fissures between long plates, lichen flecks), u 0.5-1.0 = split wood (tan fibres along v,
                        torn splinters, a few dark checks). The woodpile maps bark faces into the first band and split
                        faces into the second; world-UV users (brushwood bundles) get some sticks in bark, some split.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "spikes", "M1"))
import make_b1_materials as B  # noqa: E402

f32 = np.float32
T, MT = B.T, B.MT
LOOK = os.path.join(DEV, "spikes", "FP2", "look")


def _disc_lines(S, segs, width):
    im = Image.new("L", (S, S), 0)
    dr = ImageDraw.Draw(im)
    for pts, w in segs:
        dr.line(pts, fill=255, width=max(1, int(round(w * width))))
    return MT.blur(B._arr(im.convert("RGB"))[..., 0], 0.7)


def wood_endgrain_firewood(lv, S):
    t = [T("firewood_end", 3, 0, 2), T("firewood_end", -2, 0, -2), T("firewood_end", -4, 0, -3)][lv]
    yy, xx = B.grid(S)
    c = S / 2
    rg = np.random.default_rng(8100 + lv)
    pc = (c + 0.035 * S, c - 0.02 * S)                              # the pith a little off centre
    dx, dy = xx - pc[0], yy - pc[1]
    rr = np.sqrt(dx ** 2 + dy ** 2)
    ang = np.arctan2(dy, dx)
    rim = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / S                # 0 at the centre, 0.5 at the edge
    # wobbling rings: radius warped by a low-frequency function of the angle
    warp = 1.0 + 0.05 * np.sin(3 * ang + 0.7) + 0.035 * np.sin(5 * ang + 2.1) + 0.03 * MT.blur(MT.fbm(S, 4.0, 1, 1, 8101), 4)
    R0 = 0.45 * S
    ring_n = 11.0
    f = (rr * warp) / R0 * ring_n
    f = f + 0.18 * np.sqrt(np.clip(f, 0, None))                     # wider rings near the pith (fast young growth)
    fr = f % 1.0
    late = np.clip((fr - 0.55) / 0.30, 0, 1) ** 1.6 * np.clip((1.0 - fr) / 0.025, 0, 1)   # gradual in, sharp out
    half = ((f + 0.5) % 1.0)                                        # a faint ring between the strong ones
    faint = np.clip(1 - np.abs(half - 0.5) / 0.04, 0, 1) * 0.35
    inside = rim < 0.45
    rays = (np.sin(ang * 140 + 2.5 * MT.fbm(S, 3.0, 1, 1, 8106)) > 0.92).astype(f32)   # fine medullary rays
    val = 1.0 - 0.34 * late - 0.10 * faint - 0.05 * rays + 0.05 * MT.fbm(S, 2.6, 1, 1, 8102)
    heart = np.clip(1 - (rr / (0.55 * R0)) ** 4, 0, 1)              # darker, warmer heartwood
    val = val * (1 - 0.12 * heart)
    sap = np.clip(1 - np.abs(rim - 0.43) / 0.02, 0, 1)              # pale sapwood band just inside the bark
    val = val * (1 + 0.10 * sap)
    if lv == 0:                                                     # saw arcs on a fresh cut
        val = val * (1 + 0.04 * np.sin(np.sqrt((xx - c) ** 2 + (yy + 3 * S) ** 2) / 7 * 2 * math.pi))
    co = B.base(t, val)
    co = co * (1 + np.stack([0.06 * heart, 0.0 * heart, -0.06 * heart], -1))
    # grime toward the rim and the pith check stain
    co = MT.mix(co, (92, 78, 56), np.clip((rim - 0.36) / 0.09, 0, 1) * [0.15, 0.25, 0.35][lv])
    # bark ring: dark grey-brown, fissured; a thin dark cambium line inside it
    bark = np.clip((rim - 0.45) / 0.006, 0, 1)
    bkn = MT.fbm(S, 2.0, 1, 1, 8103)
    barkcol = B.base((86, 74, 60), 0.85 + 0.15 * np.clip(bkn, -1.5, 1.5))
    camb = np.clip(1 - np.abs(rim - 0.449) / 0.004, 0, 1)
    co = co * (1 - bark[..., None]) + barkcol * bark[..., None]
    co = MT.mix(co, (52, 40, 28), camb * 0.7)
    # drying checks: a V check from the bark in (every level), fine radial checks from the pith
    segs = []
    nv = [1, 2, 3][lv]
    for k in range(nv):
        a = rg.uniform(0, 2 * math.pi)
        r_in = rg.uniform(0.12, 0.22) * S
        pts = []
        for j in range(9):
            q = j / 8
            rad = 0.47 * S + (r_in - 0.47 * S) * q
            aa = a + 0.05 * math.sin(q * 5 + k)
            pts.append((pc[0] + rad * math.cos(aa), pc[1] + rad * math.sin(aa)))
        for j in range(8):                                          # wide at the bark, closing toward the pith
            segs.append(([pts[j], pts[j + 1]], (1 - j / 8) * [5, 6, 8][lv] + 1))
    for k in range([2, 4, 7][lv]):
        a = rg.uniform(0, 2 * math.pi)
        r1 = rg.uniform(0.12, 0.32) * S
        segs.append(([(pc[0] + 3 * math.cos(a), pc[1] + 3 * math.sin(a)),
                      (pc[0] + r1 * math.cos(a + 0.04), pc[1] + r1 * math.sin(a + 0.04))], [1.5, 2, 3][lv]))
    ck = _disc_lines(S, segs, 1.0)
    ck = ck * (rim < 0.49)
    co = MT.mix(co, (34, 26, 18), ck * 0.92)
    pith = np.exp(-(rr / 4.0) ** 2)
    co = MT.mix(co, (70, 52, 34), pith * 0.8)
    h = -late * 0.6 - ck * 3 + bark * (0.5 + 0.5 * bkn)
    if lv >= 1:
        co = MT.grey(co, [0, 0.18, 0.32][lv])
    mask = (ck > 0.3) | (rim >= 0.448) | (pith > 0.3)
    if lv == 2:                                                     # old: grey, mould spots on the end
        mo = B.blobs(S, 8104, 1.4, 2.6, 2) & inside
        co = MT.patch(co, mo, (120, 124, 104), 0.45, 8105)
        mask = mask | mo
    # the corners outside the disc are never mapped: fill them so the WHOLE texture's mean is the palette colour too
    # (B3a / B3b / L1 prop checks read the whole PNG; matcheck reads the unmasked cut face)
    co = np.clip(co, 0, 1)
    corner = rim >= 0.5
    m_cut = co[~mask].mean(0)                       # make_one scales everything by target / m_cut afterwards
    need = m_cut * S * S - co[~corner].reshape(-1, 3).sum(0)
    co[corner] = np.clip(need / max(1, int(corner.sum())), 0, 1)
    return B.R(np.clip(co, 0, 1), MT.h2n(h.astype(f32), 1.0), 0.8, mask, t, 0.1, 0.2)


def wood_firewood(lv, S):
    t = [T("firewood_split", 3, 0, 2), T("firewood_split", 0, 0, 0), T("firewood_split", -4, -1, -3)][lv]
    yy, xx = B.grid(S)
    u = xx / S
    barkband = u < 0.5
    # ---- bark (u 0-0.5): long plates along v separated by deep fissures, a net of cross cracks
    plates = MT.fbm(S, 2.4, 1, 9, 8201)                             # streaks along v
    plates2 = MT.fbm(S, 2.6, 1, 4, 8202)
    fis1 = np.clip(1 - np.abs(plates) / 0.30, 0, 1)                 # fissures where the fields cross 0: an
    fis2 = np.clip(1 - np.abs(plates2) / 0.22, 0, 1)                # anastomosing net of long plates (oak bark)
    fis = np.maximum(fis1, fis2 * 0.8) ** 1.3
    cross = np.zeros((S, S), f32)
    ridge = np.clip(1 - fis * 1.6, 0, 1)
    bv = 0.80 + 0.30 * ridge + 0.10 * np.clip(MT.fbm(S, 1.6, 1, 4, 8204), -2, 2) - 0.45 * fis
    bark = B.base((100, 86, 70), bv)
    bark = MT.mix(bark, (60, 48, 38), fis * 0.5)
    lich = (MT.fbm(S, 2.4, 1, 1, 8205) > 1.6) & (fis < 0.2)
    bark = MT.mix(bark, (150, 152, 128), MT.blur(lich.astype(f32), 1.0) * [0.35, 0.45, 0.6][lv])
    # ---- split wood (u 0.5-1): fibres along v, torn splinters, a few dark checks
    fib = MT.fbm(S, 1.1, 1, 60, 8206)
    tears = np.clip(MT.fbm(S, 2.0, 1, 14, 8207) - 0.9, 0, 1)
    sv = 1.0 + 0.10 * fib - 0.18 * tears + 0.08 * MT.fbm(S, 2.2, 1, 2, 8208)
    split = B.base((176, 136, 84), sv)
    checks = np.clip(1 - np.abs(MT.fbm(S, 2.6, 1, 25, 8209)) / 0.04, 0, 1) * (MT.fbm(S, 2.0, 1, 1, 8210) > 0.6)
    split = MT.mix(split, (52, 40, 28), checks * 0.8)
    split = MT.grey(split, [0.0, 0.22, 0.38][lv])
    co = np.where(barkband[..., None], bark * 0.92, split * 1.08)
    h = np.where(barkband, -fis * 1.2 - cross * 0.6 + 0.2 * plates2, fib * 0.15 - tears * 0.4 - checks * 1.5)
    mask = B.Z(S)
    if lv == 2:
        mo = B.blobs(S, 8211, 1.2, 2.6, 2)
        co = MT.patch(co, mo, (132, 136, 112), 0.55, 8212)
        mask = mo
    return B.R(np.clip(co, 0, 1).astype(f32), MT.h2n(h.astype(f32), 1.0), 0.85, mask, t, 0.1, 0.2)


def table():
    import make_m1_materials as M1
    by = {m["id"]: (m, w, u, n) for m, w, u, n in M1.table()}
    eg, egw, egu, _ = by["jp_m_wood_endgrain_firewood"]
    eg = dict(eg)
    eg.update({"maker": wood_endgrain_firewood, "px": (512, 512), "S": 512,
               "grain": "growth rings (~11, latewood dark), heartwood core, sapwood band, bark ring, drying checks"})
    fw, fww, fwu, _ = by["jp_m_wood_firewood"]
    fw = dict(fw)
    fw.update({"maker": wood_firewood, "srcs": [],
               "grain": "along v; u 0-0.5 oak bark (plates, fissures), u 0.5-1 split wood (fibres, splinters)",
               "uv": B.WORLD + "; TWO BANDS in u: 0.0-0.5 bark, 0.5-1.0 split wood (map bark faces into the first, "
                               "split faces into the second; v along the billet)"})
    return [
        (eg, egw, egu, "FP2 redraw: clear rings at 512 px, checks, bark ring (was 25 aliased rings -> flat yellow)"),
        (fw, {"_w0": "fresh: tan split faces, grey-brown bark", "_w1": "seasoned a year, greyer",
              "_w2": "old and damp, pale mould"}, fwu,
         "FP2 redraw: bark band + split-wood band (was the Weathered Planks photo with joints and nail holes)"),
    ]


def draft(only):
    os.makedirs(LOOK, exist_ok=True)
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    for m, _, _, _ in table():
        if only and m["id"] not in only:
            continue
        for lv in range(3):
            r = m["maker"](lv, m["S"])
            mask = np.asarray(r["mask"], bool)
            co = MT.fix_mean(np.clip(r["co"], 0, 1).astype(f32), r["target"], ~mask)
            Image.fromarray((co * 255 + 0.5).astype(np.uint8)).save(os.path.join(LOOK, "%s_w%d.png" % (m["id"], lv)))
            print("draft", m["id"], lv, (co[~mask].mean(0) * 255).round(1) if (~mask).any() else None)


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    if "--draft" in argv:
        draft(only)
        return 0
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        if only and mid not in only:
            continue
        B.BYID[mid] = m
        if not any(x["id"] == mid for x in B.MATS):
            B.MATS.append(m)
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by or B.NEED.get(mid, {}).get("used_by", []),
                       "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"] = [{"procedural": "make_fp2_materials.py (on make_b1_materials.make_one)"}]
        sc["made_by"] = "research/materials/make_fp2_materials.py (agent FP2, 2026-10-01), through B1's make_one"
        sc["fp2_note"] = note
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-40s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_fp2.json"), json.dumps({"check": "C1 palette (tools/matcheck), FP2 materials",
                                                            "results": allres}, indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("FP2 materials:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
