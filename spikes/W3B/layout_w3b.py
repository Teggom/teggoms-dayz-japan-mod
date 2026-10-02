"""W3B: place the wave-3b buildings, yards and stall props on the test island (own drop-ins, not registry placements).

  python spikes/W3B/layout_w3b.py     -> test/placements/W3B.csv, test/ce/W3B_mapgrouppos.xml, spikes/W3B/w3b_items.json

Areas (world metres; spawn (1024, 985); all in free space, checked below):
  A  the artisans' street (z ~1003, x 1033-1092) east of the spawn: six workshops on its north side facing south
     (joiner, turner + abacus maker, basket maker | the sakura | sword polisher, lacquerer, fittings maker), the
     barber's booth, the food / market stalls, the fortune-teller and the show booth on its south side facing north
  B  the bathhouse and the stable yard by the post-town street (z 1046-1066, x 1042-1077): the sento facing the street
     (north), the stable yard's fence with its gate on the street side, the stable row inside facing its yard
  T  the timber yard at the south edge (x 1000-1027, z 902-922): board fence + north gate, the sawing shed, the timber
     store, the shingle shed, log stacks and planks in the yard
  F  the foundry yard at the south edge (x 1035-1053, z 903-918): board fence + north gate, the foundry, the bell
     casting site, charcoal and scrap in the yard
Checks (as layout_d3.py, extended): footprints vs each other (yard rings as their wall strips), vs EVERY building any
other CSV places (record footprints, not just C.csv's), vs every point of the other CSVs, the reserved spots, T's trees;
the ground under each footprint.
"""
import csv
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit"),
          os.path.join(DEV, "spikes", "SH1"), os.path.join(DEV, "spikes", "W2F")):
    sys.path.insert(0, p)
import terrain_sh1 as T  # noqa: E402
from jpparts import decor as DC  # noqa: E402
from jpparts.templates import trade as TR  # noqa: E402,F401  (registers the yard plots in dwelling.COMPOUNDS)
from jpparts.templates import dwelling as DW  # noqa: E402
import layout_w2f as LW  # noqa: E402

KEN = 1.82
CSV_OUT = os.path.join(DEV, "test", "placements", "W3B.csv")
POS_OUT = os.path.join(DEV, "test", "ce", "W3B_mapgrouppos.xml")
ITEMS = os.path.join(HERE, "w3b_items.json")

ZN = 1012.3          # artisans' street: north row centre line (doma workshops; bench workshops +0.45)
ZS = 995.0           # south row
SY = (1069.3, 1056.4)    # stable yard plot centre
TY = (1013.65, 912.0)    # timber yard plot centre
FY = (1044.1, 910.3)     # foundry yard plot centre

# id, registry key, x, z, yaw, label
BUILDINGS = [
    ("A1", "f_tr_ws_joinery", 1036.5, ZN, 180.0, "joiner's workshop (earth floor, tiled): planing beam, sawhorses, tool "
     "chest, frames"),
    ("A2", "f_tr_ws_turner", 1043.4, ZN, 180.0, "woodturner + abacus maker (earth floor): the strap lathe, the abacus tray"),
    ("A3", "f_tr_ws_basket", 1050.3, ZN, 180.0, "bamboo + basket maker (earth floor): poles, the half-woven basket"),
    ("A4", "f_tr_ws_polisher", 1073.5, ZN + 0.45, 180.0, "sword polisher (raised-floor bench workshop, tiled): stone "
     "holder by the lattice window; the dust-free back room"),
    ("A5", "f_tr_ws_lacquer", 1081.0, ZN + 0.45, 180.0, "lacquerer (bench workshop): the work board, the drying cupboard "
     "in the back room"),
    ("A6", "f_tr_ws_kinko", 1088.5, ZN + 0.45, 180.0, "sword-fittings maker (bench workshop, tiled): pitch bowl, the "
     "little forge"),
    ("A7", "f_tr_booth_barber", 1039.6, ZS, 0.0, "barber's booth (de-doko): the kit box, the waiting bench"),
    ("A8", "f_tr_booth_misemono", 1071.2, ZS - 0.5, 0.0, "show booth (misemono-goya): mat walls, benches, the empty "
     "cage on the stage, the painted signboard"),
    ("B1", "f_tr_sento", 1048.5, 1061.0, 0.0, "public bathhouse (sento, furnished): entrance + bandai west, changing "
     "room, the zakuro-guchi, the bath room east, the boiler lean-to on the east gable"),
    ("B2", "tr_cmp_stableyard", SY[0], SY[1], 180.0, "the stable yard's board fence, the wide gate north (street side)"),
    ("B3", "f_tr_stablerow", SY[0], SY[1] - 6.37 + 1.70 + 2.275, 0.0, "stable row (furnished): four stalls open to the "
     "yard (north), the tack room east"),
    ("T1", "tr_cmp_timberyard", TY[0], TY[1], 180.0, "the timber yard's board fence, the wide gate north"),
    ("T2", "f_tr_timber_saw", 1007.0, 905.6, 0.0, "the sawing shed (open): the sawing trestle with the log and the big saw"),
    ("T3", "f_tr_timber_store", 1018.6, 905.3, 0.0, "the timber store: timber stood upright, planks"),
    ("T4", "f_tr_timber_shingle", 1003.1, 916.5, 90.0, "the shingle splitter's shed (open east)"),
    ("F1", "tr_cmp_foundryyard", FY[0], FY[1], 180.0, "the foundry yard's board fence, the gate north"),
    ("F2", "f_tr_foundry", 1040.6, 907.3, 0.0, "foundry (furnished): the cupola furnace, treadle bellows, sand casting "
     "bed, new pots, scrap; open bays north to the yard"),
]
# free objects: id, p3d (P:-relative), x, z, yaw, label
EXTRA = [
    ("A9", r"JP\site\street\jp_s_stall_yatai.p3d", 1046.0, ZS + 0.6, 0.0, "a roofed food stall (yatai: soba / dumplings)"),
    ("A10", r"JP\site\street\jp_s_stall_reed.p3d", 1050.8, ZS + 0.6, 0.0, "a reed-screen market stall"),
    ("A11", r"JP\site\street\jp_s_stall_row3.p3d", 1059.0, ZS + 0.3, 0.0, "the market row: three reed stalls"),
    ("A12", r"JP\furniture\tradefit\jp_f_ekisha_table_upset.p3d", 1064.6, ZS + 1.6, 0.0,
     "the fortune-teller's table, knocked over (lantern, sticks, counting rods)"),
    ("A13", r"JP\furniture\tradefit\jp_f_ekisha_table.p3d", 1054.8, 1004.8, 200.0,
     "a second fortune-teller's table, as left, by the sakura"),
    ("A14", r"JP\site\street\jp_s_nobori_shop.p3d", 1044.2, ZS + 2.0, 0.0, "a stall banner"),
    ("B4", r"JP\site\yard\jp_s_straw_stack_nio_cone.p3d", 1063.6, 1061.0, 0.0, "a straw stack in the stable yard"),
    ("B5", r"JP\site\yard\jp_s_handcart_load_bales.p3d", 1074.3, 1059.6, 0.0, "a handcart with fodder bales"),
    ("T5", r"JP\furniture\tradefit\jp_f_log_stack.p3d", 1016.0, 913.2, 0.0, "logs stacked on bearers, the dealer's mark"),
    ("T6", r"JP\furniture\tradefit\jp_f_log_stack_collapsed.p3d", 1023.0, 912.6, 0.0, "a log stack, the top rolled down"),
    ("T7", r"JP\furniture\tradefit\jp_f_plank_stack_scattered.p3d", 1021.0, 919.2, 0.0, "planks, half pulled down"),
    ("T8", r"JP\furniture\tradefit\jp_f_log_stack.p3d", 1006.5, 920.0, 0.0, "logs waiting for the saw"),
    ("F3", r"JP\furniture\tradefit\jp_f_bell_mould.p3d", 1048.3, 912.6, 0.0, "the bell casting site: the clay mould in "
     "its pit (never poured)"),
    ("F4", r"JP\site\yard_life\jp_s_charcoal_bales_stack.p3d", 1050.8, 906.3, 90.0, "charcoal bales for the melt"),
    ("F5", r"JP\furniture\tradefit\jp_f_scrap_heap.p3d", 1046.6, 906.2, 0.0, "scrap iron in the yard"),
    ("F6", r"JP\furniture\tradefit\jp_f_cast_pots.p3d", 1038.2, 914.6, 0.0, "new pots and kettles on a rack outside"),
]
LINE_KINDS = ("tr_cmp_",)
ALLOW = set()


def rec(key):
    for p in glob.glob(os.path.join(DEV, "buildings", "*", "records", key + ".json")):
        with open(p, "rb") as f:
            return json.loads(f.read().decode("utf-8"))
    raise KeyError(key)


def strips(key, pos, yaw):
    spec = DW.COMPOUNDS[rec(key)["params"]["plot"]]
    cx, cz = spec["W"] / 2, spec["D"] / 2
    out = []
    for (nodes, kind, opt, ends) in spec["runs"]:
        segs = list(zip(nodes[:-1], nodes[1:])) + ([(nodes[-1], nodes[0])] if spec.get("closed") else [])
        for a, b in segs:
            xs, zs = sorted((a[0], b[0])), sorted((a[1], b[1]))
            r = (xs[0] - 0.3 - cx, xs[1] + 0.3 - cx, zs[0] - 0.3 - cz, zs[1] + 0.3 - cz)
            out.append([LW.to_world(x, z, pos, yaw) for x, z in ((r[0], r[2]), (r[1], r[2]), (r[1], r[3]), (r[0], r[3]))])
    return out


def all_records():
    recs = {}
    for p in glob.glob(os.path.join(DEV, "buildings", "*", "records", "*.json")) + \
            glob.glob(os.path.join(DEV, "buildings", "*", "record.json")):
        try:
            with open(p, "rb") as f:
                r = json.loads(f.read().decode("utf-8"))
        except Exception:
            continue
        if r.get("model") and r.get("bbox"):
            recs[r["model"].lstrip("\\").lower()] = r
    return recs


def prop_poly(p3d, x, z, yaw):
    name = os.path.splitext(os.path.basename(p3d))[0]
    cat = DC.catalog().get(name)
    if not cat:
        return None
    b = cat["bbox"]
    return LW.corners([b[0], b[1], 0.0, 1.0, b[4], b[5]], (x, 25.0, z), yaw)


def main():
    rows, pos_xml, items, polys, problems = ["p3d,x,z,yaw_deg,y_offset"], [], [], [], []
    recs = all_records()
    for bid, key, x, z, yaw, label in BUILDINGS:
        r = rec(key)
        bb = r["bbox"]
        pos = (x, 25.0, z)
        lo, hi = LW.ground_poly(LW.corners(bb, pos, yaw, -0.3))
        g0 = T.ground(x, z)
        base = lo
        if hi - lo > 0.05:
            problems.append("note %s: ground varies %.2f m under it (seated on the lowest point)" % (bid, hi - lo))
        yoff = base - g0
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (r["model"].lstrip("\\"), x, z, yaw, yoff))
        if r.get("loot_points", 0):
            pos_xml.append('    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />'
                           % (r["class"], x, base, z, yaw, 90.0 - yaw))
        items.append({"id": bid, "class": r["class"], "p3d": r["model"].lstrip("\\"), "x": x, "z": z, "yaw": yaw,
                      "y_off": round(yoff, 3), "label": label, "area": bid[0], "key": key})
        if key.startswith(LINE_KINDS):
            for k, sp in enumerate(strips(key, pos, yaw)):
                polys.append((bid + ".w%d" % k, sp))
        else:
            polys.append((bid, LW.corners(bb, pos, yaw)))
        for k, s in enumerate(r.get("site", [])):
            wx, wz = LW.to_world(s["x"], s["z"], pos, yaw)
            sy = base + s.get("y", 0.0)
            rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (s["p3d"].lstrip("\\"), wx, wz, (yaw + s["yaw"]) % 360.0,
                                                    sy - T.ground(wx, wz)))
            items.append({"id": "%s.s%d" % (bid, k + 1), "class": None, "p3d": s["p3d"].lstrip("\\"), "x": round(wx, 3),
                          "z": round(wz, 3), "yaw": (yaw + s["yaw"]) % 360.0, "y_off": round(sy - T.ground(wx, wz), 3),
                          "label": s["why"], "area": bid[0]})
            pp = prop_poly(s["p3d"], wx, wz, (yaw + s["yaw"]) % 360.0)
            if pp:
                polys.append(("%s.s%d" % (bid, k + 1), pp))
    for eid, p3d, x, z, yaw, label in EXTRA:
        pp = prop_poly(p3d, x, z, yaw)
        lo, hi = LW.ground_poly(pp) if pp else (T.ground(x, z), T.ground(x, z))
        yoff = lo - T.ground(x, z)
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (p3d, x, z, yaw, yoff))
        items.append({"id": eid, "class": None, "p3d": p3d, "x": x, "z": z, "yaw": yaw, "y_off": round(yoff, 3),
                      "label": label, "area": eid[0]})
        if pp:
            polys.append((eid, pp))
    # ---- checks
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            a, b = polys[i], polys[j]
            ia, ib = a[0].split(".")[0], b[0].split(".")[0]
            if ia == ib or (ia, ib) in ALLOW or (ib, ia) in ALLOW:
                continue
            # a yard ring and what stands inside it: only the wall strips are checked (they are the ring's polys)
            if LW.poly_hit(a[1], b[1]):
                problems.append("OVERLAP %s x %s" % (a[0], b[0]))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) == "W3B.csv":
            continue
        with open(p, newline="") as f:
            for row in csv.DictReader(f):
                k = row["p3d"].lower()
                x, z, yaw = float(row["x"]), float(row["z"]), float(row["yaw_deg"])
                if k in recs:
                    poly = LW.corners(recs[k]["bbox"], (x, 25.0, z), yaw)
                    for nid, pp in polys:
                        if LW.poly_hit(poly, pp):
                            problems.append("OVERLAP %s x building %s (%s)" % (nid, os.path.basename(k),
                                                                               os.path.basename(p)))
                else:
                    others.append((os.path.basename(p), row["p3d"], x, z))
    for src, p3d, x, z in others:
        for nid, p in polys:
            if DC.point_poly_dist((x, z), p) < 0.3:
                problems.append("CLASH %s with %s %s at (%.1f, %.1f)" % (nid, src, os.path.basename(p3d), x, z))
    for nm, (a0, a1, c0, c1) in LW.RESERVED.items():
        for nid, p in polys:
            if LW.poly_hit(p, [(a0, c0), (a1, c0), (a1, c1), (a0, c1)]):
                problems.append("RESERVED %s in %s" % (nid, nm))
    for t in T.trees():
        tx, tz = float(t[0]), float(t[1])
        for nid, p in polys:
            if DC.point_poly_dist((tx, tz), p) < 0.8:
                problems.append("TREE in %s at (%.1f, %.1f)" % (nid, tx, tz))
    with open(CSV_OUT, "wb") as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    with open(POS_OUT, "wb") as f:
        f.write(("\n".join(pos_xml) + "\n").encode("utf-8"))
    with open(ITEMS, "wb") as f:
        f.write(json.dumps(items, indent=1, ensure_ascii=False).encode("utf-8"))
    hard = [p for p in problems if not p.startswith("note")]
    for p in problems:
        print(p)
    print("W3B.csv %d rows, %d buildings, %d free objects, %d CE groups; %d problems (+%d notes)" % (
        len(rows) - 1, len(BUILDINGS), len(EXTRA), len(pos_xml), len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
