"""C3 island dressing: the free street and hamlet objects (B3b + L2 outdoor items) that are not tied to one building,
written to test/placements/C3.csv (world metres, yaw clockwise from north, y_offset over the ground; T's build_world
bakes them into the terrain). Building-bound yard / street objects stay in each furnished variant's site() (C.csv).

  python spikes/C3/dress_island.py          -> checks, then writes test/placements/C3.csv (exit 1 on a problem)

Checks: every footprint inside the flat pad (924..1124), clear of the reserved spots (README), of every building's
walls (its model bbox minus the eave overhang: the wall rectangle from its floors / rooms), of every other object's
footprint (C.csv site objects, the other *.csv drop-ins, F's trees), and of a 1.3 m apron in front of every outside
door of every placed building.
"""
import csv
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)
import registry  # noqa: E402
import pipeline  # noqa: E402
from jpparts import decor as DC, mlod, checks as C  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

OUT = os.path.join(DEV, "test", "placements", "C3.csv")
RESERVED = {"player spawn": (1019.0, 1029.0, 980.0, 990.0), "item grid": (998.0, 1052.0, 966.0, 978.0),
            "machiya shop + yard": (1014.0, 1034.0, 1036.0, 1062.0), "sakura W": (980.0, 990.0, 1005.0, 1015.0),
            "sakura E": (1058.0, 1068.0, 1005.0, 1015.0), "bamboo grove": (1080.0, 1110.0, 955.0, 995.0),
            "weapon range": (995.0, 1055.0, 925.0, 950.0), "swatch wall (M)": (952.0, 963.0, 1095.0, 1105.0)}

# ------------------------------------------------------------------------------------------------ the objects
# (p3d basename, x, z, yaw, why)
STREET = [
    # the dead-world road story: people fled down the street
    ("jp_s_kago_ab_tipped", 1016.0, 1079.6, 75, "an abandoned hired palanquin tipped in the street"),
    ("jp_s_travel_gear_hat_stick", 1011.2, 1080.4, 20, "a straw hat and a walking stick dropped"),
    ("jp_s_travel_gear_ab_burst", 1021.5, 1080.9, 200, "a traveller's bundle burst open"),
    ("jp_s_footwear_ab_scattered", 1026.0, 1078.9, 30, "clogs and sandals scattered before the grand inn"),
    ("jp_s_tenbin_spill_veg", 999.8, 1079.8, 105, "a vendor's pole dropped, vegetables spilled"),
    ("jp_s_tenbin_spill_fish", 1051.8, 1080.0, 250, "a fish seller's load dropped"),
    ("jp_s_lantern_fallen_chochin", 1006.3, 1080.6, 40, "a torn lantern fallen in the street"),
    ("jp_s_lantern_fallen_crushed", 1047.2, 1079.4, 160, "a crushed lantern"),
    ("jp_s_amado_fallen", 993.2, 1081.0, 95, "a shop shutter fallen into the street"),
    ("jp_s_stool_ab_tipped", 1030.6, 1079.3, 60, "a stool knocked over"),
    ("jp_s_handcart_ab_broken", 1038.5, 1080.4, 80, "a broken handcart left in the street"),
    ("jp_s_leaf_pile_small", 1057.0, 1080.3, 10, "leaves drifted against the gutter"),
    ("jp_s_leaf_pile_ab_scattered", 986.0, 1080.2, 0, "leaves scattered on the street"),
    # the street corner (the empty north lots between the rows): fire watch, notice board, crossroads lantern
    ("jp_s_fire_watch_ladder_tower", 1033.0, 1086.8, 180, "the ward's fire-watch ladder with its bell"),
    ("jp_s_fire_watch_rack", 1028.5, 1085.2, 180, "the ward's buckets and fire hooks on their rack"),
    ("jp_s_kosatsu_std", 1017.5, 1087.5, 180, "the official notice board at the ward corner"),
    ("jp_s_lantern_sign_tsuji", 1040.2, 1083.2, 180, "the crossroads lantern"),
    ("jp_s_fire_tub_full", 1008.9, 1083.2, 0, "a fire tub at the end of the Kamigata row"),
    ("jp_s_fire_tub_ab_scattered", 1042.0, 1085.3, 0, "a fire tub at the end of the Edo row, its buckets scattered"),
    ("jp_s_stone_jizo_bib", 1011.2, 1085.0, 180, "a roadside Jizo with a faded bib"),
    ("jp_s_potted_pair", 984.6, 1076.2, 0, "potted plants beside the post-town house door, dead"),
    ("jp_s_nobori_ab_tattered", 1008.0, 1077.0, 0, "a tattered banner at the inn"),
    # gutters in front of the bare units (the furnished ones carry their own)
    ("jp_s_gutter_board_1ken", 987.4, 1082.54, 180, "gutter, Kamigata 3k end unit"),
    ("jp_s_gutter_board_1ken", 989.3, 1082.54, 180, "gutter, Kamigata 3k end unit"),
    ("jp_s_gutter_board_1ken", 1002.3, 1082.54, 180, "gutter, Kamigata corner unit"),
    ("jp_s_gutter_board_1ken", 1004.2, 1082.54, 180, "gutter, Kamigata corner unit"),
    ("jp_s_gutter_board_1ken", 1045.3, 1082.54, 180, "gutter, Edo 2k end unit"),
    ("jp_s_gutter_board_1ken", 1049.0, 1082.54, 180, "gutter, Edo board-roof unit"),
    ("jp_s_gutter_board_1ken", 1050.9, 1082.54, 180, "gutter, Edo board-roof unit"),
    ("jp_s_gutter_board_1ken", 996.3, 1077.7, 0, "gutter, post-town row middle"),
    ("jp_s_gutter_board_1ken", 998.2, 1077.7, 0, "gutter, post-town row middle"),
    ("jp_s_gutter_board_1ken", 1001.9, 1077.7, 0, "gutter, post-town row end"),
    ("jp_s_gutter_board_1ken", 1003.8, 1077.7, 0, "gutter, post-town row end"),
]
HAMLET = [
    # autumn fields and the threshing yard
    ("jp_s_hasa_tiers", 974.0, 1012.0, 90, "rice drying rack hung with sheaves"),
    ("jp_s_hasa_ab_sagged", 974.0, 1019.0, 90, "a sagging rice rack"),
    ("jp_s_hasa_low", 929.0, 1011.5, 90, "a low rice rack at the field edge"),
    ("jp_s_straw_stack_nio_cone", 955.0, 1016.0, 0, "a straw stack (nio) in the threshing yard"),
    ("jp_s_straw_stack_nio_cyl", 930.5, 1036.5, 0, "a straw stack behind the Kanto house"),
    ("jp_s_straw_stack_stook", 927.8, 1016.5, 0, "rice stooks drying in the field"),
    ("jp_s_straw_stack_stook", 928.9, 1018.4, 30, "rice stooks drying in the field"),
    ("jp_s_straw_stack_stook", 927.6, 1020.3, 70, "rice stooks drying in the field"),
    ("jp_s_straw_stack_ab_slumped", 970.5, 1036.5, 0, "a straw stack slumped, cap blown off"),
    ("jp_s_straw_stack_tawara_stack", 956.6, 1043.8, 0, "rice bales stacked by the sheds"),
    ("jp_s_scarecrow_kasa", 977.5, 1004.0, 300, "a scarecrow in a hat and raincoat"),
    ("jp_s_scarecrow_naruko", 927.8, 1005.5, 90, "bird clappers on a rope over the field"),
    ("jp_s_laundry_pole_load_kaki", 952.6, 1022.3, 90, "persimmons drying on a pole in the yard"),
    ("jp_s_laundry_pole_load_daikon", 955.6, 1008.0, 0, "daikon drying on a pole"),
    # water: the bamboo pipe into a trough, and a lever well
    ("jp_s_kakei_trough", 953.2, 1036.0, 90, "a bamboo pipe running into a wooden trough"),
    ("jp_s_well_hanetsurube_well", 955.0, 1001.0, 0, "the hamlet's lever well"),
    # the stable yard beside the Kanto house's umaya
    ("jp_s_stable_yard_tie_post", 931.0, 1021.5, 90, "the horse's tie post"),
    ("jp_s_stable_yard_saddle_rack", 929.4, 1026.0, 90, "a pack saddle on its rack"),
    ("jp_s_stable_yard_trough_stone", 930.8, 1018.5, 90, "a stone trough"),
    # charcoal, tools, leaves
    ("jp_s_charcoal_bales_ab_burst", 967.6, 1041.8, 0, "charcoal bales, one burst"),
    ("jp_s_farm_tools_ab_fallen", 939.8, 1008.0, 20, "farm tools fallen by the hut"),
    ("jp_s_leaf_pile_broom", 947.5, 1008.2, 0, "a raked leaf pile with the broom left in it"),
    ("jp_s_ladder_ab_fallen", 968.4, 1008.6, 60, "a ladder fallen in the yard"),
    ("jp_s_oke_ab_staves", 944.8, 1009.5, 0, "a tub fallen to staves"),
    # the hamlet's roadside stones
    ("jp_s_stone_jizo_offer", 978.3, 1029.0, 270, "a Jizo with offerings at the hamlet entrance"),
    ("jp_s_stele_koshin", 978.3, 1031.0, 270, "a Koshin stone beside it"),
]


def item_at(name, x, z, yaw):
    cat = DC.catalog()
    if name not in cat:
        raise KeyError(name)
    return {"name": name, "info": cat[name], "x": x, "y": 0.0, "z": z, "yaw": yaw}


def fp_box(it, pad=0.0):
    fp = DC.footprint(it)
    if not fp:
        b = it["info"]["bbox"]
        pts = [DC.to_model(it, (xx, 0.0, zz)) for xx in (b[0], b[1]) for zz in (b[4], b[5])]
        fp = [(p[0], p[2]) for p in pts]
    xs, zs = [p[0] for p in fp], [p[1] for p in fp]
    return (min(xs) - pad, max(xs) + pad, min(zs) - pad, max(zs) + pad)


def building_boxes():
    """[(key, wall box, [door apron boxes], [site object boxes])] in world coordinates."""
    out = []
    for b in registry.BUILDINGS:
        if not b["ship"] or not b["placements"]:
            continue
        mod = pipeline.load_module(b)
        if "params" in b:
            M, floors, rooms = mod.model(name=b["name"], **b["params"])
        else:
            M, floors, rooms = mod.model()
        rx = [v for r in rooms for v in (r["rect_model"][0], r["rect_model"][1])]
        rz = [v for r in rooms for v in (r["rect_model"][2], r["rect_model"][3])]
        wall = (min(rx) - 0.35, max(rx) + 0.35, min(rz) - 0.35, max(rz) + 0.35)
        D = getattr(mod, "D", None)
        site = list(D.site) if D else []
        for pl in b["placements"]:
            def W(p, pl=pl):
                return bloot.model_to_world(p, pl["pos"], pl["yaw"])
            cs = [W((xx, 0.0, zz)) for xx in (wall[0], wall[1]) for zz in (wall[2], wall[3])]
            wb = (min(c[0] for c in cs), max(c[0] for c in cs), min(c[2] for c in cs), max(c[2] for c in cs))
            aprons = []
            for d in M.doors:
                if not getattr(d, "passable", True) or not d.action:
                    continue
                a = d.action
                # an outside door: its action point lies on the building's outer wall box
                if min(abs(a[0] - wall[0] - 0.35), abs(a[0] - wall[1] + 0.35), abs(a[2] - wall[2] - 0.35),
                       abs(a[2] - wall[3] + 0.35)) < 0.40:
                    w = W(a)
                    aprons.append((w[0] - 1.3, w[0] + 1.3, w[2] - 1.3, w[2] + 1.3))
            sboxes = []
            for s in site:
                it = dict(s)
                p = W((s["x"], 0.0, s["z"]))
                it.update(x=p[0], z=p[2], yaw=(pl["yaw"] + s["yaw"]) % 360.0)
                sboxes.append((s["name"], fp_box(it)))
            out.append((b["key"], wb, aprons, sboxes))
    return out


def overlap(a, b, gap=0.0):
    return a[0] < b[1] + gap and a[1] > b[0] - gap and a[2] < b[3] + gap and a[3] > b[2] - gap


def main():
    objs = [(n, x, z, y, w) for (n, x, z, y, w) in STREET + HAMLET]
    items = [(n, item_at(n, x, z, y), w) for (n, x, z, y, w) in objs]
    bb = building_boxes()
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) in ("C3.csv", "C.csv"):
            continue
        for r in csv.DictReader(open(p)):
            others.append((os.path.basename(p) + ":" + os.path.basename(r["p3d"]), float(r["x"]), float(r["z"])))
    probs = []
    boxes = []
    for n, it, why in items:
        box = fp_box(it)
        boxes.append((n, box))
        if not (925.0 < box[0] and box[1] < 1123.0 and 925.0 < box[2] and box[3] < 1123.0):
            probs.append((n, "outside the flat pad"))
        for rn, r in RESERVED.items():
            if overlap(box, r):
                probs.append((n, "reserved " + rn))
        for key, wb, aprons, sboxes in bb:
            if overlap(box, wb, 0.10):
                probs.append((n, "into building " + key))
            for a in aprons:
                if overlap(box, a):
                    probs.append((n, "door apron of " + key))
            for sn, sb in sboxes:
                if overlap(box, sb, 0.05):
                    probs.append((n, "site object %s of %s" % (sn, key)))
        for on, ox, oz in others:
            if box[0] - 1.5 < ox < box[1] + 1.5 and box[2] - 1.5 < oz < box[3] + 1.5:
                probs.append((n, "near " + on))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if overlap(boxes[i][1], boxes[j][1], 0.10):
                probs.append((boxes[i][0], "overlaps " + boxes[j][0]))
    rows = ["p3d,x,z,yaw_deg,y_offset"]
    for n, it, why in items:
        rows.append("%s,%.3f,%.3f,%.1f,0.0" % (it["info"]["p3d"].lstrip("\\"), it["x"], it["z"], it["yaw"]))
    print("%d objects (%d street, %d hamlet); %d buildings checked" % (len(items), len(STREET), len(HAMLET), len(bb)))
    for p in probs:
        print("PROBLEM", p)
    if probs and "--force" not in sys.argv:
        return 1
    with open(OUT, "wb") as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
