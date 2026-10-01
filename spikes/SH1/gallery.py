"""SH1 life-layer gallery: all 74 life-layer items (research/interior/LIFE_LAYER.md; L1 interior 1-50, L2 outdoor
51-74) at their mounts, in three bare open board sheds (Land_JP_Shed_Open_Board, registry SH1_GALLERY) in the east
yard plus a ground strip in front of them. One representative model per item (the first model of its sidecar, the
'intact' / 'as left' one); every other variant of an item is in the contact sheets.

Mounts (parts/kit/jpparts/decor.py): wall / post items on a shed's inner wall faces (the prop's z = 0 plane on the
face, heights built in), beam items and the inner noren from the open front's lower beam (underside 2.52 m), surface
items on wall shelves (B3a's jp_f_tana_*; decor.on_surface), floor items on the earth floor (0.05 m), the steamer
(mount 'kamado') on the floor as there is no stove here, eaves items under shed 3's front eave (decor.under_eaves,
eave 2.92 m), yard / street / field / road / shore items on the ground strip, the bench dressing on a B3b bench.

IDs: L<n> = the LIFE_LAYER.md item number; LS1-3 the sheds (west to east); LH = host props (shelves, bench).
Every object is a separate map object (test/placements/SH1.csv), not a proxy.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))
from jpparts import decor as DC  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

SHEDS = [(1072.0, 25.0, 1036.0), (1080.0, 25.0, 1036.0), (1088.0, 25.0, 1036.0)]
YAW = 180.0
FLOOR = 0.05          # shed earth floor (rooms level_m)
BACK = -1.76          # inner face of the back wall (model z)
SIDE = 2.67           # inner faces of the side walls (model x = +-SIDE)
BEAM_Y, BEAM_Z = 2.52, 1.82     # the open front's lower beam: underside, centre line
EAVE_Y, FACADE_Z = 2.92, 1.89   # front plate underside; just in front of the front beams
EPS = 0.005

ITEMS = {  # LIFE_LAYER number -> sidecar (src/JP/<area>/<folder>/<sidecar>.prop.json)
    1: "furniture/wall/jp_f_mino_pegs", 2: "furniture/wall/jp_f_ofuda", 3: "furniture/wall/jp_f_koyomi",
    4: "furniture/wall/jp_f_utensil_board", 5: "furniture/wall/jp_f_tool_wall", 6: "furniture/wall/jp_f_rope_pegs",
    7: "furniture/wall/jp_f_sandals_hung", 8: "furniture/wall/jp_f_hoshigaki", 9: "furniture/wall/jp_f_drying",
    10: "furniture/wall/jp_f_chochin", 11: "furniture/wall/jp_f_bangasa", 12: "furniture/wall/jp_f_noren_inner",
    13: "furniture/wall/jp_f_kaya", 14: "furniture/wall/jp_f_fire_gear", 15: "furniture/religious/jp_f_butsudan",
    16: "furniture/religious/jp_f_butsu_set", 17: "furniture/religious/jp_f_kamidana_set",
    18: "furniture/meal/jp_f_tableware", 19: "furniture/meal/jp_f_meal_left", 20: "furniture/meal/jp_f_tokkuri",
    21: "furniture/meal/jp_f_suribachi", 22: "furniture/meal/jp_f_seiro", 23: "furniture/meal/jp_f_taru",
    24: "furniture/meal/jp_f_basket", 25: "furniture/meal/jp_f_charcoal", 26: "furniture/meal/jp_f_hiuchi",
    27: "furniture/living/jp_f_enza", 28: "furniture/living/jp_f_byobu", 29: "furniture/living/jp_f_iko",
    30: "furniture/living/jp_f_clothes", 31: "furniture/living/jp_f_sewing", 32: "furniture/living/jp_f_mirror_stand",
    33: "furniture/living/jp_f_goban", 34: "furniture/living/jp_f_toys", 35: "furniture/living/jp_f_shokudai",
    36: "furniture/living/jp_f_straw_bed", 37: "furniture/work/jp_f_itoguruma", 38: "furniture/work/jp_f_izaribata",
    39: "furniture/work/jp_f_straw_work", 40: "furniture/work/jp_f_mi", 41: "furniture/work/jp_f_usu",
    42: "furniture/work/jp_f_writing_box", 43: "furniture/work/jp_f_choba_set", 44: "furniture/work/jp_f_masu",
    45: "furniture/tier/jp_f_katanakake", 46: "furniture/tier/jp_f_yoroibitsu", 47: "furniture/tier/jp_f_yumi_rack",
    48: "furniture/tier/jp_f_tea", 49: "furniture/tier/jp_f_manger", 50: "furniture/tier/jp_f_fallen_leaf",
    51: "site/yard_life/jp_s_hasa", 52: "site/yard_life/jp_s_kaki_curtain", 53: "site/yard_life/jp_s_tsukimi",
    54: "site/yard_life/jp_s_farm_tools", 55: "site/yard_life/jp_s_leaf_pile", 56: "site/yard_life/jp_s_ladder",
    57: "site/yard_life/jp_s_charcoal_bales", 58: "site/yard_life/jp_s_potted", 59: "site/yard_life/jp_s_bird_cage",
    60: "site/yard_life/jp_s_kakei", 61: "site/yard_life/jp_s_stable_yard", 62: "site/yard_life/jp_s_scarecrow",
    63: "site/street_life/jp_s_travel_gear", 64: "site/street_life/jp_s_kago", 65: "site/street_life/jp_s_tenbin_spill",
    66: "site/street_life/jp_s_fishnet", 67: "site/street_life/jp_s_boat", 68: "site/street_life/jp_s_fire_watch",
    69: "site/street_life/jp_s_sandals_sale", 70: "site/street_life/jp_s_bench_dress", 71: "site/street_life/jp_s_amado",
    72: "site/street_life/jp_s_lantern_fallen", 73: "site/street_life/jp_s_stool", 74: "site/street_life/jp_s_footwear"}


def first_model(n):
    p = os.path.join(DEV, "src", "JP", *ITEMS[n].split("/")) + ".prop.json"
    d = json.loads(open(p, "rb").read().decode("utf-8"))
    return os.path.basename(d["models"][0]["p3d"])[:-4]


def short(n):
    t = open(os.path.join(DEV, "research", "interior", "LIFE_LAYER.md"), "rb").read().decode("utf-8")
    for ln in t.splitlines():
        if ln.startswith("| %d |" % n):
            c = ln.split("|")[2].strip()
            return c.replace("★ ", "").replace("**", "").split(" (`")[0]
    return ITEMS[n].rsplit("/", 1)[1]


def layout():
    O = []
    probs = []
    pieces = []          # (shed index, decorator item dict (building frame), id, label, where)

    def M(n):
        return first_model(n)

    # ---------------------------------------------------------------- shed 1 (west): walls, posts, beams + kitchen floor
    s = 0
    for n, x in ((1, -1.92), (5, -0.54), (4, 0.67), (6, 1.55), (7, 2.27)):      # back wall (model x; world x mirrors)
        pieces.append((s, DC.on_wall(M(n), "g", x, BACK + EPS, 0.0, floor_y=FLOOR), "L%d" % n, "back wall"))
    pieces.append((s, DC.on_wall(M(14), "g", -SIDE + EPS, -0.60, 90.0, floor_y=FLOOR), "L14", "east side wall"))
    pieces.append((s, DC.on_wall(M(3), "g", -SIDE + EPS, 0.85, 90.0, floor_y=FLOOR), "L3", "east side wall, front"))
    pieces.append((s, DC.on_wall(M(47), "g", SIDE - EPS, -0.55, 270.0, floor_y=FLOOR), "L47", "west side wall"))
    pieces.append((s, DC.on_wall(M(11), "g", SIDE - EPS, 1.05, 270.0, floor_y=FLOOR), "L11", "west side wall, front"))
    pieces.append((s, DC.on_wall(M(2), "g", -0.91, FACADE_Z, 0.0, floor_y=FLOOR), "L2", "front face of the middle-east post"))
    for n, x in ((13, -1.82), (8, 1.35), (9, 2.15)):
        pieces.append((s, DC.on_beam(M(n), "g", x, BEAM_Z, 0.0, BEAM_Y), "L%d" % n, "hanging from the front beam"))
    pieces.append((s, DC.in_doorway(M(12), "g", 0.0, BEAM_Z, 0.0, BEAM_Y), "L12", "hanging in the middle bay of the front beam (as in a doorway)"))
    for n, x, z, yw in ((23, -1.9, -0.75, 0), (25, -0.95, -0.80, 0), (22, 0.20, -0.70, 0), (19, 1.35, -0.30, 0),
                        (27, 0.20, 0.55, 15)):
        pieces.append((s, DC.item(M(n), "g", x, z, yw, y=FLOOR), "L%d" % n, "floor"))
    # ---------------------------------------------------------------- shed 2 (middle): shelves + living-room floor
    s = 1
    tA = DC.on_wall("jp_f_tana_182_3", "g", 1.0, BACK + EPS, 0.0, floor_y=FLOOR)
    tB = DC.on_wall("jp_f_tana_182_3", "g", -1.0, BACK + EPS, 0.0, floor_y=FLOOR)
    tC = DC.on_wall("jp_f_tana_136_1", "g", -SIDE + EPS, -0.55, 90.0, floor_y=FLOOR)
    pieces += [(s, tA, "LH1", "shelf on the back wall, west half (host)"),
               (s, tB, "LH2", "shelf on the back wall, east half (host)"),
               (s, tC, "LH3", "shelf on the east side wall (host)")]
    for host, surf, n, dx, lab in ((tA, "board_2", 16, -0.55, "LH1 upper shelf"), (tA, "board_2", 17, 0.05, "LH1 upper shelf"),
                                   (tA, "board_2", 20, 0.58, "LH1 upper shelf"), (tA, "board_1", 43, -0.50, "LH1 lower shelf"),
                                   (tA, "board_1", 44, 0.15, "LH1 lower shelf"), (tA, "board_1", 26, 0.62, "LH1 lower shelf"),
                                   (tB, "board_2", 48, -0.55, "LH2 upper shelf"), (tB, "board_2", 42, 0.05, "LH2 upper shelf"),
                                   (tB, "board_2", 24, 0.60, "LH2 upper shelf"),
                                   (tC, "board_1", 18, -0.42, "LH3 shelf"), (tC, "board_1", 21, 0.05, "LH3 shelf"),
                                   (tC, "board_1", 31, 0.45, "LH3 shelf")):
        pieces.append((s, DC.on_surface(M(n), host, surf, dx=dx, dz=0.0), "L%d" % n, lab))
    for n, x, z, yw in ((15, 2.30, -1.10, 270), (28, 1.45, 0.95, 0), (30, -0.20, 0.55, 10), (33, -1.75, 0.95, 0),
                        (34, 0.95, -0.15, 30), (32, -1.55, -0.20, 0), (35, 2.30, 0.35, 0), (36, 0.30, -0.85, 0)):
        pieces.append((s, DC.item(M(n), "g", x, z, yw, y=FLOOR), "L%d" % n, "floor"))
    pieces.append((s, DC.on_beam(M(10), "g", 0.0, BEAM_Z, 0.0, BEAM_Y), "L10", "hanging from the front beam"))
    # ---------------------------------------------------------------- shed 3 (east): work + tier markers floor, eaves
    s = 2
    for n, x, z, yw in ((29, 1.60, -1.45, 0), (38, -1.55, -1.20, 0), (37, 0.05, -1.35, 0), (39, 1.75, 0.05, 0),
                        (40, 0.30, -0.15, 0), (41, -1.90, 0.20, 0), (45, -0.80, 1.25, 0), (46, 0.45, 1.10, 0),
                        (49, 2.05, 0.95, 90), (50, -0.95, 0.25, 80)):
        pieces.append((s, DC.item(M(n), "g", x, z, yw, y=FLOOR), "L%d" % n, "floor"))
    for n, x in ((52, -1.82), (69, 0.0), (59, 1.82)):
        pieces.append((s, DC.under_eaves(M(n), x, FACADE_Z, 0.0, EAVE_Y), "L%d" % n, "under the front eave"))
    # ---------------------------------------------------------------- outside: leaning on the end walls (outer face
    # at model x = +-2.795: posts +-2.73 + half their 0.12; these props' z = 0 plane is the wall, anchor 'wall')
    outer = [(0, 56, SIDE + 0.125, 0.6, 90.0, "leaning on shed 1's west end wall (outside)"),
             (0, 57, SIDE + 0.125, -1.0, 90.0, "stacked by shed 1's west end wall (outside)"),
             (2, 54, -SIDE - 0.125, -0.9, 270.0, "leaning on shed 3's east end wall (outside)"),
             (2, 71, -SIDE - 0.125, 0.9, 270.0, "a shutter stood against shed 3's east end wall (outside)")]
    for s, n, x, z, yw, lab in outer:
        pieces.append((s, DC.item(M(n), "g", x, z, yw, y=0.0), "L%d" % n, lab))
    # ---------------------------------------------------------------- the ground strip (world coordinates)
    ground = [  # (n, x, z, yaw, label)
        (63, 1068.6, 1030.0, 180), (74, 1071.0, 1030.3, 180), (72, 1073.4, 1030.0, 160), (73, 1075.5, 1030.3, 200),
        (53, 1081.0, 1030.6, 180), (58, 1083.2, 1030.3, 180), (61, 1085.9, 1030.2, 180), (62, 1089.0, 1030.0, 180),
        (68, 1092.4, 1030.4, 180),
        (51, 1069.4, 1025.4, 180), (60, 1075.0, 1025.4, 180), (55, 1080.3, 1025.0, 180), (65, 1085.0, 1025.2, 180),
        (64, 1089.8, 1025.0, 90), (66, 1095.6, 1023.5, 90), (67, 1072.5, 1020.4, 90)]
    gitems = [(DC.on_site(M(n), x, z, yw), "L%d" % n, "ground strip") for n, x, z, yw in ground]
    bench = DC.item("jp_s_bench_1ken", "g", 1078.2, 1030.5, 180.0, y=0.0)
    dress = DC.on_surface(M(70), bench, "seat", dx=0.35, dz=0.0)
    gitems += [(bench, "LH4", "a bench on the ground strip (host)"), (dress, "L70", "on the LH4 bench seat")]

    # ---------------------------------------------------------------- to world
    for k in range(3):
        O.append(("LS%d" % (k + 1), "@shed_open_board", SHEDS[k][0], SHEDS[k][2], YAW, 0.0,
                  "gallery shed %d (Land_JP_Shed_Open_Board, bare: placed through the registry)" % (k + 1),
                  {"registry": True}))
    for s, it, oid, where in pieces:
        pos = SHEDS[s]
        w = bloot.model_to_world((it["x"], it["y"], it["z"]), pos, YAW)
        yaw = (YAW + it["yaw"]) % 360.0
        lab = ("shed %d, %s: " % (s + 1, where)) + (short(int(oid[1:])) if oid[1:].isdigit() and oid[0] == "L" else it["name"])
        O.append((oid, it["name"], w[0], w[2], yaw, w[1] - pos[1], lab,
                  {"host": "shed%d" % (s + 1), "in_building": "shed_open_board", "shed": s + 1,
                   "mount": it["info"]["mount"]}))
    for it, oid, where in gitems:
        lab = "%s: %s" % (where, short(int(oid[1:])) if oid[1:].isdigit() else it["name"])
        extra = {"mount": it["info"]["mount"]}
        if oid in ("LH4", "L70"):
            extra["host"] = "bench"
        O.append((oid, it["name"], it["x"], it["z"], it["yaw"] % 360.0, it["y"] if it["y"] is not None else None, lab,
                  extra))
    # ---------------------------------------------------------------- own checks: all 74, collision props apart in each shed
    have = {int(o[0][1:]) for o in O if o[0][0] == "L" and o[0][1:].isdigit()}
    missing = sorted(set(range(1, 75)) - have)
    if missing:
        probs.append("life-layer items missing: %s" % missing)
    for s in range(3):
        fps = []
        for s2, it, oid, where in pieces:
            if s2 != s:
                continue
            fp = DC.footprint(it)
            if fp:
                xs, zs = [p[0] for p in fp], [p[1] for p in fp]
                box = (min(xs), max(xs), min(zs), max(zs))
                if where.startswith("leaning") or where.startswith("stacked") or where.startswith("a shutter"):
                    continue
                if box[0] < -SIDE - 0.01 or box[1] > SIDE + 0.01 or box[2] < BACK - 0.01 or box[3] > 1.67 + 0.25:
                    probs.append("%s outside shed %d's floor %s" % (oid, s + 1, [round(v, 2) for v in box]))
                fps.append((oid, box))
        for i in range(len(fps)):
            for j in range(i + 1, len(fps)):
                a, b = fps[i][1], fps[j][1]
                if a[0] < b[1] + 0.05 and a[1] > b[0] - 0.05 and a[2] < b[3] + 0.05 and a[3] > b[2] - 0.05:
                    probs.append("shed %d: %s overlaps %s" % (s + 1, fps[i][0], fps[j][0]))
    return O, {"problems": probs, "items": len(have)}
