#!/usr/bin/env python3
"""Parts agent (B-PARTS) pre-steps 1-3, palette side (idempotent). Writes playbook/palette.json ('wb', LF, indent 1).

1. kawara_ibushi darker: in-engine calibration. Stephen approved B's machiya roof in game; its texture
   (data/B/textures/jp_kawara_co.png) averages (81, 83, 83). The photo-sampled entry (145, 149, 149) made the library
   _w1 average ~127, far lighter than the look he approved. New entry (118, 122, 123): the recipe's _w1 (-8 L) then
   averages ~(100, 104, 105) = mean ~103, inside the lead's 95-110 target; _w0 (clean, new tiles) ~121.
   The photo value is kept in the entry as photo_srgb.
2. board_new: fresh (unweathered) cedar/cypress board, for the _w0 of jp_m_roof_kureita and jp_m_roof_kokera.
   No build-list or playbook photo shows fresh boards in usable light (x01_ioka_a has one new board on the ground,
   in blue evening shade: (101, 100, 106), unusable). Sampled instead from the CC0 photo scan Poly Haven
   "Hinoki Planks" (Charlotte Baglioni; the source B already used for the machiya floor boards, see
   spikes/B_building/CREDITS.md): median of the mid-70 % luminance pixels (156, 122, 84), spread 2.7 -> tol 6.
3. grime_splash: the W1 splash band at the base of an exterior earth wall, sampled on x08_hirose_earthwall (two
   boxes on the lowest 3-4 % of the earth panels just above the sill; the same panels 0.1 m higher read
   (115-120, 98-103, 79-85), i.e. the band is ~12 % darker). Palette ID of the new jp_m_wall_grime decal material.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
PAL = os.path.join(DEV, "playbook", "palette.json")

KAWARA = [118, 122, 123]
NEW = [
    ("board_new", "roof_board_silver", {
        "name": "Fresh cedar / cypress board (unweathered)",
        "material": "newly split or sawn sugi / hinoki boards and shingles, before silvering",
        "group": "roof", "tiers": [1, 2, 3],
        "use": "_w0 (clean) of jp_m_roof_kureita and jp_m_roof_kokera: freshly roofed houses; weathers to "
               "roof_board_silver",
        "note": "Added 2026-09-27 by the parts agent (lead's materials-review decision). Source: CC0 photo scan "
                "Poly Haven 'Hinoki Planks' (Charlotte Baglioni, https://polyhaven.com/a/hinoki_planks), diffuse "
                "map, median of the mid-70 % luminance pixels. No build-list/playbook photo shows fresh boards in "
                "usable light (x01_ioka_a: one new board in blue evening shade). Upgrade to a museum/surviving-"
                "building sample of a freshly re-roofed house when one is found.",
        "srgb": [156, 122, 84], "method": "sampled", "tolerance_dE76": 6, "observed_spread_dE76": 2.7,
        "samples": [{"ref": "polyhaven:hinoki_planks_diff_1k (data/B/polyhaven/hinoki_planks)", "box": [0, 0, 1, 1],
                     "select": "mid 70 % luminance"}],
        "weathering": {"worst": "roof_board_silver", "max_mix": 1.0},
    }),
    ("grime_splash", "earth_road", {
        "name": "Splash / grime band at wall bases (W1)",
        "material": "rain-splashed soil and dust on the bottom 0-0.4 m of walls, posts and sills",
        "group": "ground", "tiers": [1, 2, 3],
        "use": "jp_m_wall_grime decal (jp_p_trim_grime_*): an alpha band over wall bases; never a base colour",
        "note": "Added 2026-09-27 by the parts agent (lead's materials-review decision: tiling textures cannot carry "
                "a height-bound band). Sampled on x08_hirose_earthwall: the lowest 3-4 % of the earth panels "
                "just above the sill; 0.1 m higher the same panels read (115-120, 98-103, 79-85).",
        "srgb": [104, 89, 71], "method": "sampled", "tolerance_dE76": 6, "observed_spread_dE76": 1.8,
        "samples": [{"ref": "x08_hirose_earthwall", "box": [0.69, 0.765, 0.815, 0.795], "select": "mid 70 % luminance"},
                    {"ref": "x08_hirose_earthwall", "box": [0.49, 0.74, 0.56, 0.775], "select": "mid 70 % luminance"}],
    }),
]


def main():
    pal = json.loads(open(PAL, "rb").read())
    ents = pal["entries"]
    ids = [e["id"] for e in ents]
    k = next(e for e in ents if e["id"] == "kawara_ibushi")
    if k["srgb"] != KAWARA:
        k["photo_srgb"] = k["srgb"]
        k["srgb"] = KAWARA
        k["hex"] = "#%02X%02X%02X" % tuple(KAWARA)
        k["method"] = "calibrated"
        k["note"] = ("Darkened 2026-09-27 by the parts agent on the lead's materials-review decision. Source: in-engine "
                     "calibration, Stephen approved the machiya roof in game (B's jp_kawara_co averages (81, 83, 83)). "
                     "The photo-sampled value (145, 149, 149) is kept as photo_srgb; with this entry the library "
                     "_w1 (recipe -8 L) averages ~103, _w0 ~121. Tolerance and samples unchanged.")
        print("kawara_ibushi ->", KAWARA)
    for pid, after, e in NEW:
        if pid in ids:
            continue
        e = dict(id=pid, **e)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        order = ["id", "name", "material", "group", "tiers", "use", "note", "srgb", "hex", "method", "tolerance_dE76",
                 "observed_spread_dE76", "samples", "weathering"]
        e = {kk: e[kk] for kk in order if kk in e}
        i = [x["id"] for x in ents].index(after) + 1
        ents.insert(i, e)
        print("added", pid, e["srgb"])
    with open(PAL, "wb") as f:
        f.write(json.dumps(pal, indent=1, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
