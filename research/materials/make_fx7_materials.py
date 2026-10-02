#!/usr/bin/env python3
"""FX7 (2026-10-02): rock and soil for the 3c-2 earth / rock masses (Stephen's walk: the quarry face, the mine hillside,
the lime-kiln bank and the climbing-kiln bank "look kind of like shit; no idea what they are": they were built from
stone_cut / stone_field / ground_earth_bare, the same warm beige, so a cut face, a weathered crag and a soil bank all
read as one sandy blob). Through B1's make_one (same pipeline as make_fx5 / make_fx2), the PLAYBOOK 15.3 matte recipe.

- jp_m_stone_quarry_face  A freshly split quarry face (Izu andesite / Okazaki granite, TR25): grey with dark mafic
                          flecks and pale feldspar, horizontal bedding / sheet joints (dark cracks with a rust stain
                          bleeding down), two vertical joints, the half wedge-hole channels (ya-ana) left along the top
                          split line, patches of pick and chisel marks. 2 m tile. Palette `rock_andesite_cut`.
- jp_m_stone_outcrop      Natural weathered rock (the uncut crag, the crown, boulders): darker grey, a broad weathering
                          cloud, rain streaks, lichen rosettes (pale grey-green, ochre, black), moss in the hollows
                          (_w2). 3 m tile. Palette `rock_outcrop_weathered`.
- jp_m_ground_earth_bank  A soil bank (kiln banks, the adit's knoll, the quarry's cap): brown forest soil with clods
                          and pebbles, dry autumn grass tufts and fallen leaves over it (the bank has stood for years).
                          2 m tile. Palette `earth_bare` (the grass / leaves are overlay, masked out of the C1 check).
Sources: Poly Haven CC0 scans already in data/polyhaven (rock_surface, worn_rock_natural_01, clay_floor_001,
dry_decay_leaves; credited in research/materials/CREDITS.md); everything else procedural. No web access.
The two rock palette entries are ASSUMED (no licensed photo sample: Izu andesite and Okazaki granite faces are mid
grey, much cooler than the warm weathered Himeji ishigaki `stone_granite`); verify when a sample is found.

  python research/materials/make_fx7_materials.py [--no-pack]
C1 results: src/JP/common/materials/checks_fx7.json. Never starts or stops the server or any GUI program.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

f32 = np.float32
PAL = os.path.join(DEV, "playbook", "palette.json")

ENTRIES = [
    {"id": "rock_andesite_cut", "name": "Quarry face, freshly split andesite / granite (grey)",
     "material": "Izu andesite (komatsu-ishi) / Okazaki granite, split face a few years old",
     "group": "stone", "tiers": [1, 2, 3], "use": "quarry faces, split blocks, fresh rubble (jp_m_stone_quarry_face)",
     "note": "Added 2026-10-02 by FX7 (research/materials/make_fx7_materials.py), ASSUMED: no licensed photo sample. "
             "A split andesite / granite face is mid grey with a faint warm cast; the warm beige stone_granite "
             "(163,140,110) is sampled from the old weathered Himeji walls and read as sand on the quarry. Verify.",
     "srgb": [138, 136, 128], "method": "assumed", "tolerance_dE76": 14, "weathering": None},
    {"id": "rock_outcrop_weathered", "name": "Natural rock outcrop, weathered (grey, lichen)",
     "material": "andesite / granite crag weathered in place: grey-brown skin, lichen, moss in the joints",
     "group": "stone", "tiers": [1, 2, 3], "use": "uncut crags, a quarry's crown, boulders (jp_m_stone_outcrop)",
     "note": "Added 2026-10-02 by FX7, ASSUMED (reasoned: darker and browner than the fresh split face, lichen and "
             "moss as overlays). Verify against a licensed photo.",
     "srgb": [116, 113, 103], "method": "assumed", "tolerance_dE76": 14, "weathering": None},
]


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    have = {e.get("id") for e in pal["entries"]}
    added = []
    for e in ENTRIES:
        if e["id"] in have:
            continue
        e = dict(e)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        pal["entries"].append(e)
        added.append(e["id"])
    if added:
        with open(PAL, "wb") as f:
            f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return added


def _norm(a):
    return (a - a.mean()) / (a.std() + 1e-6)


def _wobble_line(S, v0, amp, seed, beta=3.2):
    """A tileable wobbling horizontal line: the v (row) of the line for every u column."""
    w = B.MT.fbm(S, beta, 1, 1, seed)[0]
    return (v0 * S + amp * S * _norm(w)) % S


def stone_quarry_face(lv, S):
    MT, T = B.MT, B.T
    t = [T("rock_andesite_cut", 4), T("rock_andesite_cut", 0), T("rock_andesite_cut", -3, 0, 1)][lv]
    rg = np.random.default_rng(7701)
    a = MT.photo("rock_surface", "diff", S, tiles=2)
    co = MT.recolor(a, t, 1.15, 0.15)
    pn_photo = MT.pnormal("rock_surface", S, tiles=2, k=0.45)
    yy, xx = B.grid(S)
    hgt = np.zeros((S, S), f32)
    # mineral flecks: dark mafic and pale feldspar grains
    fl = rg.random((S, S)).astype(f32)
    dark = MT.blur((fl > 0.982).astype(f32), 1) > 0.20
    pale = MT.blur((fl < 0.010).astype(f32), 1) > 0.25
    co = MT.mix(co, (58, 58, 56), dark.astype(f32) * 0.75)
    co = MT.mix(co, (196, 192, 182), pale.astype(f32) * 0.55)
    # the broad tone: blocks between the joints differ a little, the face is cleaner where freshly split
    co = co * (1 + 0.09 * MT.fbm(S, 3.2, 1, 1, 7702) + 0.05 * MT.fbm(S, 1.8, 1, 1, 7703))[..., None]
    mask = B.Z(S)
    # bedding / sheet joints: dark cracks, the lip above lit, a rust stain running down under them
    stain = np.zeros((S, S), f32)
    crack = np.zeros((S, S), f32)
    for i, v0 in enumerate((0.16, 0.49, 0.80)):
        vl = _wobble_line(S, v0, 0.010, 7710 + i)
        d = (yy - vl[None, :] + S / 2) % S - S / 2                        # signed rows below the line
        w = 3.0 + 1.5 * (i == 1)
        crack = np.maximum(crack, np.clip(1 - np.abs(d) / w, 0, 1))
        below = np.clip(d / (S * 0.06), 0, 1)
        stain = np.maximum(stain, (d > 0) * np.exp(-below * 3.0) * np.clip(0.5 + 0.6 * MT.fbm(S, 1.6, 1, 6, 7720 + i),
                                                                          0, 1))
        hgt -= np.clip(1 - np.abs(d) / (w + 2), 0, 1) * 0.8
        hgt += np.clip(1 - np.abs(d + w + 3) / 3.0, 0, 1) * 0.25           # the lit lip above
    # two vertical joints, slightly slanted, broken
    for i, u0 in enumerate((0.31, 0.73)):
        ul = (u0 * S + 0.02 * S * _norm(MT.fbm(S, 2.2, 1, 1, 7730 + i)[:, 0]) + 0.08 * yy[:, 0]) % S
        d = (xx - ul[:, None] + S / 2) % S - S / 2
        brk = (MT.fbm(S, 2.6, 6, 1, 7735 + i) > -1.0).astype(f32)
        c = np.clip(1 - np.abs(d) / 2.6, 0, 1) * brk
        crack = np.maximum(crack, c)
        hgt -= c * 0.7
    co = MT.mix(co, (118, 92, 66), stain * [0.20, 0.32, 0.42][lv])       # rust bleeding from the joints
    co = MT.mix(co, (34, 33, 31), crack * 0.9)
    mask |= (crack > 0.3) | (stain > 0.25)
    # the half wedge-hole channels (ya-ana) left along the top split line: vertical grooves 9 cm long, 13 cm apart
    W_ = MT.Wrap(S, fill=0)
    vtop = _wobble_line(S, 0.16, 0.010, 7710)
    step = int(0.13 / 2.0 * S)
    for u in range(step // 2, S, step):
        v = vtop[u] + 4
        W_.polygon([(u - 6, v), (u + 6, v), (u + 5, v + 46), (u - 5, v + 46)], 255)
    ya = W_.arr()
    co = MT.mix(co, (52, 50, 47), ya * 0.85)
    hgt -= ya * 1.2
    mask |= ya > 0.3
    # pick / chisel marks: clusters of short parallel strokes, lighter (fresh) on _w0, toned down with wear
    TM = MT.Wrap(S, fill=0)
    for _ in range(46):
        cx, cy = rg.uniform(0, S), rg.uniform(0, S)
        ang = math.radians(rg.uniform(50, 75) * (1 if rg.random() < 0.6 else -1))
        for k in range(int(rg.integers(8, 16))):
            ox, oy = cx + rg.normal(0, 22), cy + rg.normal(0, 22)
            L = rg.uniform(10, 22)
            TM.line([(ox, oy), (ox + L * math.cos(ang), oy + L * math.sin(ang))], 255, width=2)
    tm = TM.arr()
    co = MT.mix(co, (176, 172, 162), tm * [0.45, 0.32, 0.20][lv])
    hgt -= tm * 0.35
    if lv == 2:                                                      # dark damp streaks down the old face
        rain = np.clip(MT.vstreaks(S, 7740, 1.0, 12), 0, 1.4)
        co = co * (1 - 0.10 * rain)[..., None]
    n = MT.combine(MT.h2n(hgt, 2.0), pn_photo)
    return B.R(np.clip(co, 0, 1), n.astype(f32), 0.86, mask, t, 0.08, 0.16)


def stone_outcrop(lv, S):
    MT, T = B.MT, B.T
    import make_fp1_materials as F
    t = [T("rock_outcrop_weathered", 3), T("rock_outcrop_weathered", 0), T("rock_outcrop_weathered", -3)][lv]
    a = MT.photo("worn_rock_natural_01", "diff", S, tiles=2)
    co = MT.recolor(a, t, 1.05, 0.15)
    pn = MT.pnormal("worn_rock_natural_01", S, tiles=2, k=0.8)
    rough = MT.prough("worn_rock_natural_01", S, 2)
    cloud = MT.fbm(S, 2.8, 1, 1, 7751)
    co = co * (1 + 0.12 * cloud)[..., None]
    rain = np.clip(MT.vstreaks(S, 7752, 1.0, 10), 0, 1.4)
    co = co * (1 - [0.05, 0.09, 0.13][lv] * rain)[..., None]
    big = F._lichen(S, 7753, [1.45, 1.10, 0.90][lv], 2.4)
    small = F._lichen(S, 7754, [1.70, 1.40, 1.20][lv], 1.6)
    darkl = F._lichen(S, 7755, [1.80, 1.50, 1.25][lv], 1.9)
    co = MT.patch(co, big, (160, 164, 142), 0.55, 7756)
    co = MT.patch(co, small & ~big, (176, 150, 92), 0.45, 7757)
    co = MT.patch(co, darkl & ~big, (38, 38, 34), 0.50, 7758)
    mask = big | small | darkl
    if lv >= 1:
        mo = MT.blur((MT.fbm(S, 2.4, 1, 1, 7759) > [9, 1.3, 0.9][lv]).astype(f32), 2) > 0.5
        co = MT.patch(co, mo, (72, 84, 44), 0.85, 7760)
        mask |= mo
    return B.R(np.clip(co, 0, 1), pn, rough, mask, t, 0.06, 0.12)


def ground_earth_bank(lv, S):
    MT, T = B.MT, B.T
    t = [T("earth_bare", -10, 1, 2), T("earth_bare", -9), T("earth_bare", -8, -1, -2)][lv]
    rg = np.random.default_rng(7771)
    a = MT.photo("clay_floor_001", "diff", S, tiles=2)
    co = MT.recolor(a, t, 1.0, 0.2)
    pn = MT.pnormal("clay_floor_001", S, tiles=2, k=0.7)
    clod = MT.fbm(S, 2.2, 1, 1, 7772)
    co = co * (1 + 0.10 * clod)[..., None]
    peb = MT.spots(S, 90, 4, 2.0, 5.0, 30, 7773)
    co = MT.mix(co, (150, 146, 136), peb * 0.6)
    mask = peb > 0.4
    # fallen leaves in drifts (the dry_decay_leaves scan, masked in by a low-frequency field)
    lf = MT.photo("dry_decay_leaves", "diff", S, tiles=2)
    lfm = np.clip((MT.fbm(S, 2.4, 1, 1, 7774) - [0.6, 0.35, 0.15][lv]) / 0.5, 0, 1)
    lf = lf * 0.55 + np.array([88, 70, 52], f32) / 255 * 0.45            # the drifts dulled (damp, brown)
    co = co * (1 - lfm[..., None]) + lf * lfm[..., None]
    mask |= lfm > 0.3
    # dry autumn grass tufts: clusters of thin strokes fanning up (v down the texture = down the slope)
    G = MT.Wrap(S, fill=0)
    Gv = MT.Wrap(S, fill=0)
    dens = MT.fbm(S, 2.0, 1, 1, 7775)
    n_t = [2400, 3200, 4000][lv]
    for _ in range(n_t):
        x, y = rg.uniform(0, S), rg.uniform(0, S)
        if dens[int(y) % S, int(x) % S] < -0.3:
            continue
        for k in range(int(rg.integers(8, 16))):
            ang = math.radians(rg.uniform(-120, -60))
            L = rg.uniform(18, 40)
            v = int(rg.uniform(90, 255))
            pts = [(x, y), (x + L * math.cos(ang), y + L * math.sin(ang))]
            G.line(pts, 255, width=2)
            Gv.line(pts, v, width=2)
    g = G.arr() > 0.5
    gv = Gv.arr()
    straw = np.clip(gv, 0, 1) ** 2 * 0.8                                # mostly dull olive, straw tips
    grass = (1 - straw)[..., None] * np.array([70, 80, 40], f32) / 255 + straw[..., None] * np.array([140, 124, 80],
                                                                                                      f32) / 255
    co = np.where(g[..., None], grass, co)
    mask |= g
    h = clod * 0.4 + peb * 0.6 + g.astype(f32) * 0.5
    n = MT.combine(MT.h2n(h.astype(f32), 1.2), pn)
    return B.R(np.clip(co, 0, 1), n.astype(f32), 0.92, mask, t, 0.04, 0.10)


def table():
    return [
        (B.M("jp_m_stone_quarry_face", "stone", "rock_andesite_cut", 2.0, 1024, stone_quarry_face, (0.2, 40),
             "granite", "stone_ext", "horizontal bedding joints (u = along the face, v down)", uv=B.WORLD,
             srcs=["rock_surface"], where="outdoor",
             note="Quarry split faces and fresh blocks (FX7): u along the face, v down; the ya-ana channel row "
                  "sits 0.32 m under the tile top, so put the tile top at a bench edge."),
         {"_w0": "freshly split, pale tool marks", "_w1": "a few years old, rust in the joints",
          "_w2": "abandoned: darker, rust streaks, damp streaks"},
         ["jp_ishiba"], "Quarry face (TR25): the cut benches, the split block, the rubble"),
        (B.M("jp_m_stone_outcrop", "stone", "rock_outcrop_weathered", 3.0, 1024, stone_outcrop, (0.2, 40), "granite",
             "stone_ext", "none; weathered crag skin with lichen", uv=B.WORLD + "; turn and shift per piece",
             srcs=["worn_rock_natural_01"], where="outdoor",
             note="Natural weathered rock (FX7): the uncut crag round a quarry, the knoll's rocks, boulders."),
         {"_w0": "clean weathered rock, little lichen", "_w1": "lichen + moss in the hollows",
          "_w2": "heavily lichened, moss"},
         ["jp_ishiba", "jp_mabu"], "Natural rock (crags, the quarry's crown, the adit's knoll)"),
        (B.M("jp_m_ground_earth_bank", "ground", "earth_bare", 2.0, 1024, ground_earth_bank, (0.06, 12), "dirt",
             "dirt_ext", "none; clods, pebbles, grass tufts (strokes fan up the texture)", uv=B.WORLD,
             srcs=["clay_floor_001", "dry_decay_leaves"], where="outdoor",
             note="An old soil bank grown over with dry autumn grass and fallen leaves (FX7): kiln banks, the adit's "
                  "knoll, the quarry's cap, the feathered aprons at their feet."),
         {"_w0": "a newer bank: more soil, fewer tufts", "_w1": "grassed over, leaves",
          "_w2": "long untended: dense dry grass, leaf drifts"},
         ["jp_ishiba", "jp_mabu", "jp_ishibai_gama", "jp_noborigama"], "Soil banks and knolls (3c-2 sites)"),
    ]


def main(argv):
    added = add_palette()
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        B.MATS.append(m)
        B.BYID[mid] = m
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by, "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"] = [{"procedural": "make_fx7_materials.py (on make_b1_materials.make_one)"},
                         {"polyhaven_cc0": m["srcs"]}]
        sc["made_by"] = "research/materials/make_fx7_materials.py (agent FX7, 2026-10-02), through B1's make_one"
        sc["requested_by"] = "FX7 (Stephen's 3c-2 walk: the quarry / mine / kiln banks read as beige blobs)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-40s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    B.wb(os.path.join(B.LIB, "checks_fx7.json"), json.dumps({"check": "C1 palette (tools/matcheck), FX7 materials",
                                                          "palette_entries_added": added, "results": allres}, indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("FX7 materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
