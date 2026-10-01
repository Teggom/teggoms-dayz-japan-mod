#!/usr/bin/env python3
r"""make_w2s_materials.py - W2S (Phase C wave 2, shrine + temple shells, 2026-10-01): the three roof / metal materials
the shrine and temple kit was waiting for (W2P1_NOTES / W2P2_NOTES "missing materials"). ADDS ONLY: never changes an
existing material or palette entry (the route of make_m1_materials.py: palette entries, then B1's make_one: textures,
PAAs, rvmats, sidecar, C1 matcheck on the PNG and the shipped PAA; then jp_common.pbo is repacked).

  python make_w2s_materials.py [--no-pack] [--only ID[,ID...]] [--draft]

- jp_m_roof_hiwada    cypress-bark roofing (hiwada-buki): very fine courses (~1.6 cm exposure), bark fibres down the
                      slope, strip-to-strip tone. New palette `roof_hiwada`, DERIVED: the chromaticity of the sunlit
                      sugi / hinoki trunks in k38_shrine_steps (the bark the roofs are stripped from), the value set
                      darker for a laid roof of fine overlapping courses that weathers to dark red-brown (GK).
- jp_m_roof_copper    aged copper sheet roofing (dobuki) with green patina (rokusho): staggered flat-lock sheets, rain
                      streaks. New palette `roof_copper_patina`, ASSUMED (GK): the one local copper roof (k38, far
                      background) shows a sky-lit sheen, not the patina colour; rejected as a sample.
- jp_m_metal_bronze   patinated cast bronze (temple bells, giboshi caps, hoju, door fittings): dark brown with
                      verdigris in the hollows, casting pits. New palette `bronze_patina`, ASSUMED (GK).
C1 results: src/JP/common/materials/checks_w2s.json. Never starts or stops the server or any GUI program.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import make_b1_materials as B  # noqa: E402

PAL = os.path.join(DEV, "playbook", "palette.json")
DRAFT = os.path.join(DEV, "spikes", "W2S", "draft")
f32 = np.float32
T, MT = B.T, B.MT

ADDED_BY = "Added 2026-10-01 by W2S (research/materials/make_w2s_materials.py; spikes/W2S/W2S_NOTES.md 'Materials')."
ENTRIES = [
    {"id": "roof_hiwada", "name": "Cypress-bark roofing (hiwada-buki), weathered",
     "material": "hinoki bark strips laid in very fine overlapping courses, nailed with bamboo pegs: shrine honden and "
                 "haiden, high-rank temple halls",
     "group": "roof", "tiers": [2, 3], "use": "shrine / temple hall roofs (jp_m_roof_hiwada; jp_p_roof_sori hiwada)",
     "note": ADDED_BY + " DERIVED, not a roof photo (none on this machine, no web in the run): the hue and saturation "
             "of the sunlit cedar / cypress trunks in k38_shrine_steps (Kashima shrine approach; boxes x 0.70-0.80 "
             "y 0.10-0.60 -> 166,133,119 and x 0.86-0.95 y 0.05-0.45 -> 158,125,112; the playbook box method), i.e. "
             "the bark itself, kept at its ratios (g/r 0.80, b/r 0.71) and set to r = 104 for a LAID roof: thousands "
             "of 1-2 cm course shadows and weathering make hiwada roofs read dark red-brown (general knowledge). "
             "Rejected: the left trunk of k38 (sky-washed, 209,189,180). Upgrade from a sunlit photo of a hiwada roof "
             "(Izumo, Kitano, Kibitsu) when one is saved locally.",
     "srgb": [104, 83, 74], "method": "derived", "tolerance_dE76": 16, "observed_spread_dE76": 6.2,
     "samples": [{"ref": "k38_shrine_steps", "box": [0.70, 0.10, 0.80, 0.60], "value": [166, 133, 119]},
                 {"ref": "k38_shrine_steps", "box": [0.86, 0.05, 0.95, 0.45], "value": [158, 125, 112]}]},
    {"id": "roof_copper_patina", "name": "Aged copper roofing, green patina (rokusho)",
     "material": "copper sheet roofing (dobuki: flat-lock sheets with batten seams) after decades of weather",
     "group": "roof", "tiers": [3], "use": "the richest halls, castle keeps (jp_m_roof_copper; jp_p_roof_sori copper)",
     "note": ADDED_BY + " ASSUMED (general knowledge: the matte blue-green of old Japanese copper roofs, Nikko / Edo "
             "castle-grade work). The one copper roof on this machine (k38_shrine_steps, the hall behind the trees, "
             "box x 0.48-0.53 y 0.53-0.56 -> 61,70,68 in shade, and a sky-lit sheen 200+ on its upper half) shows "
             "reflection, not the patina colour: rejected. Upgrade from a diffuse-lit photo of a temple copper roof.",
     "srgb": [96, 140, 122], "method": "assumed", "tolerance_dE76": 18, "observed_spread_dE76": 0.0, "samples": []},
    {"id": "bronze_patina", "name": "Patinated cast bronze (temple bell, finials, fittings)",
     "material": "cast bronze after years outdoors: dark brown-black, verdigris (green-blue) in the hollows and runs",
     "group": "fitting", "tiers": [1, 2, 3],
     "use": "temple bells, giboshi caps, hoju finials, honden door fittings (jp_m_metal_bronze)",
     "note": ADDED_BY + " ASSUMED (general knowledge of old temple bells and railing caps: brown-black body, green in the "
             "recesses). No local photo of an old bronze bell or giboshi.",
     "srgb": [78, 70, 56], "method": "assumed", "tolerance_dE76": 16, "observed_spread_dE76": 0.0, "samples": []},
]


def add_palette():
    pal = json.load(open(PAL, encoding="utf-8"))
    have = {e.get("id") for e in pal["entries"]}
    added = []
    for ent in ENTRIES:
        if ent["id"] in have:
            continue
        e = dict(ent)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        pal["entries"].append(e)
        added.append(ent["id"])
    if added:
        with open(PAL, "wb") as f:
            f.write(json.dumps(pal, indent=1).encode("utf-8"))
    return added


def _smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


# ================================================================================================ recipes
def roof_hiwada(lv, S):
    """1 m tile at 1024 px: 64 courses (1.6 cm exposure) across v, each darker at its top (where the course above laps
    over it) and lighter at its butt; the butt line wavers; bark fibres down the slope (along v); strips 12.5 cm wide
    with their own tone, staggered course to course. _w0 fresh red-brown, _w1 weathered dark brown, _w2 old: grey-brown,
    lichen, a few lifted strips."""
    t = [T("roof_hiwada", 7, 5, 6), T("roof_hiwada"), T("roof_hiwada", -5, -3, -5)][lv]
    yy, xx = B.grid(S)
    rows = 64
    rowh = S / rows
    wob = MT.fbm(S, 3.0, 1, 40, 9101)                        # smooth along v, varies along u: the butt line wavers
    pos = (yy + 1.6 * wob) / rowh
    ci = np.floor(pos).astype(int)
    fr = pos - ci
    val = 0.70 + 0.36 * _smooth(fr / 0.85)                    # dark top (lapped), light butt
    butt = np.clip((fr - 0.90) / 0.10, 0, 1)
    val = val * (1 - 0.18 * butt)                             # the butt edge's own shadow line
    fib = MT.fbm(S, 1.2, 1, 40, 9102)                         # fine fibres along v
    val = val + 0.07 * fib
    rg = np.random.default_rng(9103)
    tones = rg.normal(0.0, 0.055, (rows, 8))
    shift = (ci * 37) % S
    uc = (((xx + shift) % S) // (S // 8)).astype(int)
    tone = tones[ci % rows, uc % 8]
    val = val * (1 + tone)
    val = val * (1 + 0.06 * MT.fbm(S, 2.2, 1, 1, 9104))      # broad patches
    co = B.base(t, val)
    co = co * (1 + np.stack([0.5 * tone, 0.0 * tone, -0.6 * tone], -1))   # redder strips / browner strips
    mask = B.Z(S)
    if lv >= 1:
        co = co * (1 - 0.08 * np.clip(MT.vstreaks(S, 9105, 1.0, 18), 0, 1.3))[..., None]
    if lv == 2:
        co = MT.grey(co, 0.22)
        li = B.blobs(S, 9106, 1.25, 2.4, 1.5)
        co = MT.patch(co, li, (128, 128, 104), 0.5, 9107)    # lichen / moss on the old bark
        lift = (rg.random((rows, 8)) < 0.04)[ci % rows, uc % 8] & (fr > 0.55)
        co = MT.mix(co, (52, 40, 34), lift.astype(f32) * 0.55)   # lifted strips: a dark gap under them
        mask = li | lift
    h = _smooth(fr / 0.85) * 1.0 - butt * 0.6 + 0.12 * fib
    n = MT.h2n(h.astype(f32), 1.2)
    return B.R(np.clip(co, 0, 1).astype(f32), n, 0.88, mask, t, 0.08, 0.18)


def roof_copper(lv, S):
    """2 m tile at 1024 px: flat-lock sheets 0.25 m (v) x 0.50 m (u), staggered by half a sheet each row; the laps are
    darker lines with a thin light edge; green patina with low blotches and rain streaks down the slope. _w0 younger:
    brown copper shows through in flecks; _w2 old: chalky pale-green runs and black stains."""
    t = [T("roof_copper_patina", -3, 4, 6), T("roof_copper_patina"), T("roof_copper_patina", 4, -2, -2)][lv]
    yy, xx = B.grid(S)
    rows, cols = 8, 4
    rh, cw = S / rows, S / cols
    ri = np.floor(yy / rh).astype(int)
    fy = yy / rh - ri
    xo = (xx + (ri % 2) * cw / 2) % S
    fx = xo / cw - np.floor(xo / cw)
    lap = np.clip(1 - fy / 0.035, 0, 1)                         # the lap at the top of each sheet (the row above)
    lip = np.clip(1 - np.abs(fy - 0.045) / 0.012, 0, 1)        # its light folded edge
    vj = np.clip(1 - np.minimum(fx, 1 - fx) / 0.012, 0, 1)    # the staggered vertical joint
    val = 1.0 + 0.10 * MT.fbm(S, 2.4, 1, 1, 9201) + 0.04 * MT.fbm(S, 1.4, 1, 1, 9202)
    val = val * (1 - 0.30 * lap - 0.22 * vj) + 0.10 * lip
    co = B.base(t, val)
    st = np.clip(MT.vstreaks(S, 9203, 1.0, 16), 0, 1.3)
    co = MT.mix(co, (150, 184, 166), st * [0.10, 0.16, 0.26][lv])   # pale runs of washed patina
    mask = (lap > 0.5) | (vj > 0.5)
    if lv == 0:
        fl = B.blobs(S, 9204, 1.35, 2.8, 1.0)
        co = MT.patch(co, fl, (122, 82, 58), 0.6, 9205)          # brown copper not yet green
        mask = mask | fl
    if lv == 2:
        dk = np.clip(MT.vstreaks(S, 9206, 1.0, 22) - 0.6, 0, 1)
        co = MT.mix(co, (40, 44, 40), dk * 0.55)                  # black run stains under the laps
        ch = B.blobs(S, 9207, 1.2, 2.4, 1.5)
        co = MT.patch(co, ch, (176, 200, 184), 0.45, 9208)        # chalky pale patina
        mask = mask | ch | (dk > 0.3)
    h = -lap * 0.8 - vj * 0.6 + lip * 0.3 + 0.05 * MT.fbm(S, 2.6, 1, 1, 9209)
    n = MT.h2n(h.astype(f32), 1.0)
    return B.R(np.clip(co, 0, 1).astype(f32), n, 0.72, mask, t, 0.16, 0.28)


def metal_bronze(lv, S):
    """0.5 m tile at 512 px: cast bronze, dark brown with a mottled patina, verdigris collecting in the hollows (low
    noise troughs), casting pits. _w0 dark and even (an indoor bell), _w1 outdoor, _w2 green runs and pale bloom."""
    t = [T("bronze_patina", -4, 0, 0), T("bronze_patina"), T("bronze_patina", 3, -4, -2)][lv]
    yy, xx = B.grid(S)
    hgt = MT.fbm(S, 2.6, 1, 1, 9301)
    val = 1.0 + 0.10 * hgt + 0.05 * MT.fbm(S, 1.6, 1, 1, 9302)
    co = B.base(t, val)
    hol = np.clip((-hgt - [1.2, 0.8, 0.5][lv]) / 1.2, 0, 1)
    hol = hol * np.clip(0.55 + 0.6 * MT.fbm(S, 1.3, 1, 1, 9305), 0, 1)   # speckled, not a painted blob
    co = MT.mix(co, (84, 128, 110), hol * [0.45, 0.6, 0.75][lv])     # verdigris in the hollows
    rg = np.random.default_rng(9303)
    pits = np.zeros((S, S), f32)
    for _ in range([60, 90, 120][lv]):
        cx, cy, r = rg.uniform(0, S), rg.uniform(0, S), rg.uniform(0.8, 2.2)
        d = np.sqrt(((xx - cx + S / 2) % S - S / 2) ** 2 + ((yy - cy + S / 2) % S - S / 2) ** 2)
        pits = np.maximum(pits, np.clip(1 - d / r, 0, 1))
    co = MT.mix(co, (34, 30, 24), pits * 0.7)
    mask = (hol > 0.4) | (pits > 0.3)
    if lv == 2:
        st = np.clip(MT.vstreaks(S, 9304, 1.0, 14) - 0.5, 0, 1)
        co = MT.mix(co, (110, 150, 128), st * 0.5)
        mask = mask | (st > 0.3)
    h = 0.4 * hgt - pits * 1.0
    n = MT.h2n(h.astype(f32), 0.8)
    return B.R(np.clip(co, 0, 1).astype(f32), n, 0.6, mask, t, 0.22, 0.32)


def table():
    return [
        (B.M("jp_m_roof_hiwada", "roof", "roof_hiwada", 1.0, 1024, roof_hiwada, (0.08, 15), "wood", "wood_planks_ext",
             "down-slope (v): fine courses 1.6 cm across v, bark fibres along v", uv=B.WORLD, where="outdoor",
             note="Cypress-bark roof (hiwada-buki): shrine honden / haiden and high-rank temple halls. 1 m tile; the "
                  "courses run across v like jp_m_roof_kokera's (v down the slope). Replaces the roof_kureita "
                  "stand-in of jp_p_roof_sori hiwada (W2P2) and the straight shrine roofs' hiwada option (W2S)."),
         {"_w0": "fresh: red-brown bark, crisp course lines", "_w1": "weathered: dark red-brown, rain streaks",
          "_w2": "old: grey-brown, lichen, a few lifted strips"},
         ["jp_p_roof_sori (hiwada)", "W2S shrine shells"], "Cypress-bark shrine and temple roofs"),
        (B.M("jp_m_roof_copper", "roof", "roof_copper_patina", 2.0, 1024, roof_copper, (0.16, 30), "metalplate",
             "metal_thin_ext", "down-slope (v): flat-lock sheets 0.25 x 0.50 m, staggered", uv=B.WORLD,
             where="outdoor",
             note="Aged copper roofing with green patina (dobuki): the richest halls and castle-grade roofs (KEEP_CIVIC: "
                  "Nagoya / Edo copper keeps). 2 m tile; geometry carries the batten seams (jp_p_roof_sori copper, "
                  "every 0.45 m), the texture the sheet laps. Replaces W2P2's roof_kureita stand-in."),
         {"_w0": "younger patina: brown copper flecks through the green", "_w1": "full green patina, pale rain runs",
          "_w2": "old: chalky pale-green bloom, black run stains"},
         ["jp_p_roof_sori (copper)", "W2S temple / shrine shells"], "Copper roofs, green patina"),
        (B.M("jp_m_metal_bronze", "metal", "bronze_patina", 0.5, 512, metal_bronze, (0.22, 40), "castiron", None,
             "none; cast surface, patina in the hollows", uv=B.WORLD, where="outdoor",
             note="Patinated cast bronze: temple bells (W2F prop), giboshi caps (jp_p_porch_koran), hoju finials "
                  "(jp_p_roof_ornament), honden door fittings (jp_p_open_tobira) and shitomi hooks. Replaces the "
                  "metal_iron stand-in there (W2P1 note). Matte finish: an old patina does not mirror."),
         {"_w0": "dark, even brown-black (kept indoors / dry)", "_w1": "outdoor: green in the hollows",
          "_w2": "green runs, pale bloom"},
         ["jp_p_porch_koran", "jp_p_roof_ornament", "jp_p_open_tobira", "jp_p_open_shitomi_grid"],
         "Bronze fittings and bells"),
    ]


def draft(only):
    os.makedirs(DRAFT, exist_ok=True)
    for e in ENTRIES:
        MT.PAL[e["id"]] = dict(e)
    for m, _, _, _ in table():
        if only and m["id"] not in only:
            continue
        for lv in range(3):
            r = m["maker"](lv, m["S"])
            mask = np.asarray(r["mask"], bool)
            co = MT.fix_mean(np.clip(r["co"], 0, 1).astype(f32), r["target"], ~mask)
            Image.fromarray((co * 255 + 0.5).astype(np.uint8)).save(os.path.join(DRAFT, "%s_w%d.png" % (m["id"], lv)))
            print("draft", m["id"], lv, (co[~mask].mean(0) * 255).round(1))


def main(argv):
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))
    if "--draft" in argv:
        draft(only)
        return 0
    added = add_palette()
    pal = B.matcheck.load_palette()
    B.MT.PAL.update(pal)
    man = json.load(open(os.path.join(B.BM.DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    allres = []
    ok = True
    for m, wear, used_by, note in table():
        mid = m["id"]
        if only and mid not in only:
            continue
        B.MATS.append(m)
        B.BYID[mid] = m
        B.NEED[mid] = {"id": mid, "wear": wear, "used_by": used_by, "note": note}
        res = B.make_one(m, pal, man)
        sp = os.path.join(B.LIB, m["fam"], mid + ".json")
        sc = json.load(open(sp, encoding="utf-8"))
        sc["sources"] = [{"procedural": "make_w2s_materials.py (on make_b1_materials.make_one)"},
                         {"palette_samples": "data/research_okit/refs/k38_shrine_steps.jpg (hiwada hue only)"}
                         if mid == "jp_m_roof_hiwada" else {"palette": "assumed (general knowledge)"}]
        sc["made_by"] = "research/materials/make_w2s_materials.py (agent W2S, 2026-10-01), through B1's make_one"
        sc["requested_by"] = "parts/W2P1_NOTES.md + parts/W2P2_NOTES.md 'Missing materials' (W2S brief)"
        B.wb(sp, json.dumps(sc, indent=1, ensure_ascii=False))
        for r in res:
            print("  %-4s %-40s mean (%d,%d,%d) dE %.1f/%g  paa dE %.1f" % (
                r["verdict"], os.path.basename(r["file"]), *r["mean_srgb"], r["dE"], r["tol"], r["shipped_paa"]["dE"]))
            ok = ok and r["verdict"] != "FAIL" and r["shipped_paa"]["verdict"] != "FAIL"
        allres += res
    cp = os.path.join(B.LIB, "checks_w2s.json")
    if only and os.path.exists(cp):
        old = json.load(open(cp, encoding="utf-8")).get("results", [])
        allres = [r for r in old if not any(os.path.basename(r["file"]).startswith(i + "_w") for i in only)] + allres
    B.wb(cp, json.dumps({"check": "C1 palette (tools/matcheck), W2S materials", "palette_entries_added": added,
                         "results": allres}, indent=1))
    if "--no-pack" not in argv:
        ok = B.BM.pack() and ok
    print("W2S materials:", "OK" if ok else "FAILED", "; palette entries added:", added)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
