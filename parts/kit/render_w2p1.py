#!/usr/bin/env python3
r"""Render sheets for W2P1's shrine / temple parts and offline assemblies (render_b2.py's Blender side and composer).

  python render_w2p1.py <sheet> [job ...] [--compose]

Sheets -> parts/contact_sheets/<sheet>.jpg; PNGs -> parts/_render/<sheet>/. Builds: 'part:<id>' (a registry part),
'x:w2p1_assembly.<fn>' (an offline assembly builder, parts/kit/w2p1_assembly.py). Parts whose grade sits below y 0
are lifted with 'move' so the ground plane meets their grade.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_b2 as RB  # noqa: E402

DEV = RB.DEV
CHECKS = os.path.join(DEV, "parts", "w2p1_assembly_checks.json")


def P(name, cap, view="3q", target=(0.9, 0.6, 0.6), dist=7.0, move=1.0, persp=30, open_=0.0, human=None, **kw):
    v = {"build": "part:" + name, "view": view, "persp": persp, "target": list(target), "dist": dist,
         "move": [0.0, move, 0.0]}
    if open_:
        v["open"] = open_
    if human:
        v["human"] = list(human)
    v.update(kw)
    return (name.replace("jp_p_", ""), cap, v)


SHEETS = {
    "w2p1_koran": ("W2P1 jp_p_porch_koran: en (kirime-en) + kumi-koran, corners, kizahashi, wakishoji", [
        P("jp_p_porch_koran_plain", "1-ken en run, plain kumi-koran: jifuku, struts, hirageta, totsuka + to, round "
          "hokogi; en posts on stones, edge beam; floor +1.00", human=[2.6, 1.6, 0.0]),
        P("jp_p_porch_koran_giboshi", "Giboshi koran: octagonal end post with the onion finial (iron stands in for "
          "bronze)"),
        P("jp_p_porch_koran_corner_plain", "Corner, plain: the runs cross and run out 0.10 past the corner (the "
          "crossing run sits 1.5 cm higher: no shared planes, C20)", target=(0.6, 0.5, 0.6)),
        P("jp_p_porch_koran_corner_giboshi", "Corner with a giboshi corner post", target=(0.6, 0.5, 0.6)),
        P("jp_p_porch_koran_kizahashi", "Kizahashi in the koran gap: 5 risers of 0.20, 36.2 deg hidden walk ramp, "
          "1.10 clear between the stair rails, giboshi posts at the gap and the foot, foot stone",
          target=(0.9, 0.3, 1.8), dist=8.0, human=[2.6, 3.4, 0.0]),
        P("jp_p_porch_koran_kizahashi_plain", "The same stair with plain cut-top posts (village)",
          target=(0.9, 0.3, 1.8), dist=8.0),
        P("jp_p_porch_koran_wakishoji", "Side en run ending in the wakishoji board screen", target=(1.2, 0.9, 0.6)),
    ]),
    "w2p1_tobira": ("W2P1 jp_p_open_tobira: hinged double doors for honden and halls (shown fully open; rotation, "
                    "engine-untested)", [
        P("jp_p_open_tobira_board_out", "Board pair (ita-tobira), strap fittings + ring pulls, opening OUT; kamoi, "
          "threshold, jamb stops, pivot blocks", target=(0.9, 1.1, 0.3), move=0.0, open_=1.0, human=[2.6, 1.2, 0.0]),
        P("jp_p_open_tobira_board_in", "The same pair opening IN", target=(0.9, 1.1, 0.0), move=0.0, open_=1.0),
        P("jp_p_open_tobira_lattice_out", "Latticed doors (koshi-tobira) over a board base, opening OUT",
          target=(0.9, 1.1, 0.3), move=0.0, open_=1.0),
        P("jp_p_open_tobira_lattice_in", "Latticed doors opening IN (closed view)", target=(0.9, 1.1, 0.0),
          move=0.0),
        P("jp_p_open_tobira_sankara_in", "Temple framed panel doors (sankarado), latticed top band, opening IN "
          "(closed view)", target=(0.9, 1.1, 0.0), move=0.0),
        P("jp_p_open_tobira_board_ajar", "Static pair standing ajar (dead-world dressing)", target=(0.9, 1.1, 0.3),
          move=0.0),
    ]),
    "w2p1_roofs": ("W2P1 shrine / temple roofs, straight (village): nagare, kohai, hogyo; ridge ornaments", [
        P("jp_p_roof_nagare_1ken", "Nagare roof over a 1-ken body (issha), kokera: the front slope runs on over the "
          "en and kizahashi to two kohai posts on stones; kohai beam, tie beams parallel to the rafters",
          target=(0.9, 2.2, 0.2), dist=14.0, human=[4.0, 2.6, 0.0]),
        P("jp_p_roof_nagare_3ken", "Nagare roof over a 3 x 2 ken body (sangen-sha): four posts on the stair-foot line",
          target=(2.7, 2.2, -0.2), dist=17.0),
        P("jp_p_roof_nagare_1ken_tile", "Issha nagare roof in sangawara (onigawara, clay bed, fascia)",
          target=(0.9, 2.2, 0.2), dist=14.0),
        P("jp_p_roof_kohai_board", "Kohai step canopy (kokera) for any hall front: flatter than the hall roof (0.8 x "
          "its pitch), its top tucked under the main eave (C12), two posts, kohai beam, tie beams over the en",
          target=(0.9, 1.8, 1.4), dist=10.0, move=0.6),
        P("jp_p_roof_kohai_tile", "Kohai in sangawara (tie beams left out: < 2.00 m under them at the en rail)",
          target=(0.9, 1.8, 1.4), dist=10.0, move=0.6),
        P("jp_p_roof_forms_hogyo_board_2ken", "Hogyo pyramid roof, kokera, 2 x 2 ken hall: hip rolls, apex cap, "
          "bronze-type hoju (iron stand-in)", target=(1.8, 3.0, -1.8), dist=14.0, move=0.0, human=[4.6, 1.0, 0.0]),
        P("jp_p_roof_forms_hogyo_tile_3ken", "Hogyo in sangawara over a 3 x 3 ken hall, tile hip ridges, tile hoju",
          target=(2.7, 3.2, -2.7), dist=17.0, move=0.0),
        P("jp_p_roof_forms_hogyo_thatch_2ken", "Thatched hogyo (rural do) with a tile apex cap and hoju",
          target=(1.8, 3.4, -1.8), dist=14.0, move=0.0),
        P("jp_p_roof_ornament_chigi_soto", "Okichigi, tips cut vertical (soto-sogi)", target=(0.0, 0.40, 0.0),
          dist=4.0, move=0.0),
        P("jp_p_roof_ornament_chigi_uchi", "Okichigi, tips cut horizontal (uchi-sogi)", target=(0.0, 0.40, 0.0),
          dist=4.0, move=0.0),
        P("jp_p_roof_ornament_katsuogi_3", "3 katsuogi across a 1-ken ridge (n 2-9 in the generator)",
          target=(0.9, 0.1, 0.0), dist=4.0, move=0.0),
        P("jp_p_roof_ornament_katsuogi_5", "5 katsuogi across a 3-ken ridge", target=(2.7, 0.1, 0.0), dist=7.0,
          move=0.0),
        P("jp_p_roof_ornament_oniita", "Wooden ridge-end board (oni-ita)", target=(0.0, 0.25, 0.0), dist=2.5,
          move=0.0),
        P("jp_p_roof_ornament_oni_hall", "Hall onigawara (0.62 m)", target=(0.0, 0.3, 0.0), dist=2.5, move=0.0),
        P("jp_p_roof_ornament_hoju_bronze", "Hoju finial: roban, fukubachi, lotus seat, jewel (iron stand-in)",
          target=(0.0, 0.45, 0.0), dist=3.0, move=0.0),
        P("jp_p_roof_ornament_hoju_kawara", "Hoju finial in tile", target=(0.0, 0.45, 0.0), dist=3.0, move=0.0),
    ]),
    "w2p1_found_open": ("W2P1 raised floors (stilts), stone platforms (kidan), hall shitomido / lattice fronts", [
        P("jp_p_found_stilts_honden", "Honden floor +1.00 on underfloor posts on stones, sleepers, two rows of "
          "underfloor nuki, open beneath (yukashita)", target=(0.9, 0.5, -0.9), dist=7.0, human=[3.0, 0.8, 0.0]),
        P("jp_p_found_stilts_hall", "Haiden / hall floor +0.60 with a boarded skirt (vent gaps)",
          target=(2.7, 0.3, -1.8), dist=11.0, move=0.6),
        P("jp_p_found_stilts_ratguard", "Store on posts +1.20 with rat guards (nezumi-gaeshi)",
          target=(1.8, 0.6, -1.4), dist=9.0, move=1.2),
        P("jp_p_found_kidan_shoro", "Bell-tower platform 0.60: kerb stones, facing slabs, base course, earth top, "
          "stone flight (33 deg ramp) with cheek stones", target=(1.4, 0.3, -1.0), dist=8.0, move=0.6,
          human=[3.6, 1.4, 0.0]),
        P("jp_p_found_kidan_hall", "Hall platform 0.45, a 1-ken stone flight", target=(2.7, 0.2, -2.0), dist=11.0,
          move=0.45),
        P("jp_p_found_kidan_low", "Low platform 0.30, flights front and back", target=(1.8, 0.1, -1.4), dist=8.0,
          move=0.30),
        P("jp_p_open_shitomi_grid_hinged", "Hall shitomido: grid on a backing board; the upper leaf a top-hinged "
          "rotation window (shown open), the lower fixed", target=(0.9, 1.1, 0.4), move=0.0, open_=1.0, dist=7.0),
        P("jp_p_open_shitomi_grid_closed", "Shitomido closed", target=(0.9, 1.0, 0.1), move=0.0, dist=6.0),
        P("jp_p_open_shitomi_grid_open", "Shitomido open: upper leaf hooked up level, lower leaf removed (open bay)",
          target=(0.9, 1.2, 0.5), move=0.0, dist=7.0, human=[2.6, 1.0, 0.0]),
        P("jp_p_open_shitomi_grid_fixed", "Fixed see-through lattice front over a board base (hall side bays)",
          target=(0.9, 1.0, 0.0), move=0.0, dist=6.0),
    ]),
    "w2p1_hokora": ("W2P1 jp_p_site_hokora: 4 stone + 4 wood micro-shrines (site objects, no interior)", [
        P("jp_p_site_hokora_stone_kirizuma", "Stone shrine: gable roof stone, carved double doors, two base stones",
          target=(0.0, 0.5, 0.0), dist=4.0, move=0.0, human=[1.0, 0.6, 0.0]),
        P("jp_p_site_hokora_stone_yosemune", "Stone shrine with a hipped roof stone and a jewel knob",
          target=(0.0, 0.5, 0.0), dist=4.0, move=0.0),
        P("jp_p_site_hokora_stone_nagare", "Stone shrine, nagare roof stone (front runs out)", target=(0.0, 0.5, 0.0),
          dist=4.0, move=0.0),
        P("jp_p_site_hokora_stone_niche", "Tall kami stone with an offering niche and a roof slab",
          target=(0.0, 0.5, 0.0), dist=4.0, move=0.0),
        P("jp_p_site_hokora_wood_nagare", "Wooden hokora, miniature nagare-zukuri, 2 katsuogi, stone base",
          target=(0.0, 0.7, 0.0), dist=4.5, move=0.0),
        P("jp_p_site_hokora_wood_shinmei", "Wooden hokora, shinmei form: chigi + 3 katsuogi", target=(0.0, 0.7, 0.0),
          dist=4.5, move=0.0),
        P("jp_p_site_hokora_wood_inari", "Inari hokora painted shu (fox pair + torii are props)",
          target=(0.0, 0.7, 0.0), dist=4.5, move=0.0),
        P("jp_p_site_hokora_wood_saya", "Wooden hokora inside a shelter shed (saya-do)", target=(0.0, 1.2, 0.0),
          dist=7.0, move=0.0, human=[1.6, 1.0, 0.0]),
    ]),
}


def register(extra):
    SHEETS.update(extra)


def notes():
    if not os.path.isfile(CHECKS):
        return ""
    res = json.load(open(CHECKS, encoding="utf-8"))
    return "Assembly checks (parts/w2p1_assembly_checks.json): " + ", ".join(
        "%s %d/%d" % (nm, sum(1 for c in r["checks"] if c["ok"]), len(r["checks"])) for nm, r in sorted(res.items()))


def main(argv):
    try:
        import w2p1_sheets  # noqa: F401  (more sheet definitions, if present)
    except ImportError:
        pass
    sheet = argv[0]
    title, jobs = SHEETS[sheet]
    only = [a for a in argv[1:] if not a.startswith("--")]
    if "--compose" not in argv:
        todo = [j for j in jobs if not only or j[0] in only]
        jf = os.path.join(RB.RENDER, sheet + "_jobs.json")
        os.makedirs(RB.RENDER, exist_ok=True)
        with open(jf, "wb") as f:
            f.write(json.dumps({"out_dir": os.path.join(RB.RENDER, sheet), "res": list(RB.RES), "jobs": todo},
                               indent=1).encode("utf-8"))
        r = subprocess.run([RB.BLENDER, "--background", "--factory-startup", "--python",
                            os.path.join(HERE, "render_b2.py"), "--", "--blender", jf], capture_output=True, text=True,
                           errors="replace")
        done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
        print("%d/%d rendered" % (len(done), len(todo)))
        if len(done) < len(todo):
            print((r.stdout + r.stderr)[-4000:])
    RB.compose(sheet, title, jobs, notes() if "asm" in sheet else "Part checks: src/JP/parts/<group>/checks.json "
               "(C2 C3 C4 C5 C7 + C20 by spikes/W2P1/ptest.py). Grade = the ground plane; parts lifted onto it.")


if __name__ == "__main__":
    main(sys.argv[1:])
