"""W3C1: place wave 3c-1 (the trade quarter) on the test island: ONE new district, off the existing showcase (Stephen,
2026-10-02: 3a / 3b were hard to walk scattered through the showcase).

  python spikes/W3C1/layout_w3c1.py   -> test/placements/W3C1.csv, test/ce/W3C1_mapgrouppos.xml, spikes/W3C1/w3c1_items.json

The district: south-west of the yard, off the pad's corner, on the flattest free ground near the spawn (25.6-26.2 m;
spikes/SH1/terrain_sh1.ground survey in W3C1_NOTES.md), x 884-946, z 852-892, ~170 m from the spawn (1024, 985).
An east-west lane (z 861.5-866.0) runs through it:
  BR  north of the lane, west: the sake brewery (black board fence 12 x 13 ken, gate on the lane): the kasane-gura
      (o-kura + mae-gura) along the north fence, the rice-polishing shed and the cask kura in the yard; the brewer's
      shop with the sugidama outside the fence at the lane's west end
  DY  north of the lane, east: the indigo dyer (shop on the lane) and its drying yard behind (board fence, gate at the
      back door) with the tall cloth-drying frames
  PM  south of the lane, middle: the paper mill (lean-to steamer) and its bamboo-fenced drying yard (drying boards)
  WM  south of the lane, west: the water mill (wheel facing the lane, the flume running west; dry land, Stephen)
  LN  props along the lane
Checks as layout_w3b.py: footprints vs each other (yard rings as their wall strips), vs every building of every other
CSV, vs every point of the other CSVs, the reserved spots, T's trees; the ground under each footprint.
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
from jpparts.templates import tradesite as TS  # noqa: E402,F401  (registers the yard plots in dwelling.COMPOUNDS)
from jpparts.templates import dwelling as DW  # noqa: E402
import layout_w2f as LW  # noqa: E402

KEN = 1.82
CSV_OUT = os.path.join(DEV, "test", "placements", "W3C1.csv")
POS_OUT = os.path.join(DEV, "test", "ce", "W3C1_mapgrouppos.xml")
ITEMS = os.path.join(HERE, "w3c1_items.json")
DISTRICT = (884.0, 946.0, 852.0, 892.0)          # x0, x1, z0, z1 (SHOWCASE_MAP + the map)
LANE = (884.0, 946.0, 861.5, 866.0)

BY = (884.0 + 6 * KEN, 868.0 + 6.5 * KEN)        # brewery plot centre (SW corner 884.0, 868.0)
ZO = 886.6                                       # the o-kura's centre; the mae-gura 6.81 m south of it
DYY = (913.6 + 4 * KEN, 873.6 + 3 * KEN)         # dyer's yard centre (SW 913.6, 873.6)
PYY = (929.2 + 4.5 * KEN, 872.4 + 3 * KEN)       # paper yard centre (SW 929.2, 872.4)
# seat: an earth / board floor this far over the object's grade may not have the terrain poke through it, so a building
# on uneven ground sits on max(lowest point, highest point - clear) (the low side then floats that little); yards and
# fences sit on their lowest point (K3: modules tolerate +-0.3 m)
CLEAR = {"f_ts_okura": 0.29, "f_ts_maegura": 0.29, "f_ts_kura_casks": 0.40, "f_ts_seimai": 0.04, "f_ts_sakaya": 0.04,
         "f_ts_konya": 0.04, "f_ts_kamisuki": 0.04, "f_ts_suisha": 0.04}

# the ground that seats a building whose bbox reaches far past its floor (the mill's wheel + flume): model rect
SEAT_BOX = {"f_ts_suisha": (-2.85, 2.85, -1.95, 1.95)}

# id, registry key, x, z, yaw, label
BUILDINGS = [
    ("BR1", "ts_cmp_brewery", BY[0], BY[1], 0.0, "the brewery's black board fence, the wide gate south on the lane"),
    ("BR2", "f_ts_okura", BY[0], ZO, 180.0, "the large kura (o-kura): four big tubs, the lever press (west end), the "
     "starter loft (east end, stair up); doors on both gables"),
    ("BR3", "f_ts_maegura", BY[0], ZO - 6.81, 180.0, "the front kura (mae-gura), facing the yard: the brewers' rest room "
     "(west), the koji room, the steaming hearth + washing floor (east); its back eave + gutter against the o-kura"),
    ("BR4", "f_ts_seimai", 900.9, 871.02, 0.0, "the rice-polishing shed (open north to the yard): four treadle mortars"),
    ("BR5", "f_ts_kura_casks", 888.0, 870.9, 0.0, "the cask kura (door north to the yard): casks on both floors"),
    ("BR6", "f_ts_sakaya", 910.25, 868.9, 180.0, "the brewer's shop on the lane (open front south): casks, measures, the "
     "counting desk; the big brown sugidama under the front beam"),
    ("DY1", "f_ts_konya", 918.65, 869.33, 180.0, "the indigo dyer (shop open south to the lane, shop-front cloths); "
     "behind the step the vat room with the four sunk vats round the fire pit; back door north to the yard"),
    ("DY2", "ts_cmp_dyersyard", DYY[0], DYY[1], 0.0, "the dyer's drying yard: board fence, the gate behind the back door"),
    ("PM1", "f_ts_kamisuki", 935.0, 868.9, 180.0, "the paper mill (door south to the lane): the vat under the windows, "
     "the beating board, the couching press; the bark steamer in the lean-to (west)"),
    ("PM2", "ts_cmp_paperyard", PYY[0], PYY[1], 0.0, "the paper mill's drying yard behind it: bamboo fence, the gate at the "
     "south-east corner (the path east of the mill)"),
    ("WM1", "f_ts_suisha", 916.0, 857.8, 0.0, "the water mill south of the lane (door north on the lane): the overshot "
     "wheel on the east gable, its dry flume coming in from the north over the lane on trestles; inside three pestles "
     "on the cam shaft, the hand quern"),
]
FT = r"JP\furniture\brewfit\%s.p3d"
# free objects: id, p3d (P:-relative), x, z, yaw, label
EXTRA = [
    ("BR8", r"JP\furniture\meal\jp_f_taru_rack3.p3d", 897.5, 875.0, 0.0, "casks drying on a rack in the yard"),
    ("DY3", FT % "jp_f_monohoshi", 917.5, 877.3, 0.0, "a tall drying frame, indigo lengths hung doubled"),
    ("DY4", FT % "jp_f_monohoshi", 923.8, 877.3, 0.0, "a second drying frame"),
    ("DY5", FT % "jp_f_monohoshi_torn", 920.6, 880.9, 90.0, "a drying frame, two lengths fallen, two torn"),
    ("DY6", FT % "jp_f_sukumo_bales_scattered", 926.6, 882.6, 0.0, "sukumo bales tumbled in the yard"),
    ("DY7", FT % "jp_f_hangiri", 915.9, 882.4, 0.0, "rinsing tubs stacked by the fence"),
    ("PM3", FT % "jp_f_hoshiita_rack", 933.5, 878.0, 180.0, "drying boards leaned to the sun (south), sheets on three"),
    ("PM4", FT % "jp_f_hoshiita_rack", 939.8, 878.0, 180.0, "drying boards leaned to the sun"),
    ("PM5", FT % "jp_f_hoshiita_rack_fallen", 936.6, 881.4, 0.0, "drying boards fallen flat"),
    ("LN1", r"JP\site\yard\jp_s_handcart_load_bales.p3d", 903.5, 864.0, 90.0, "a handcart with rice bales on the lane"),
]
ALLOW = {("BR2", "BR3")}    # the kasane-gura: the o-kura's eave over the mae-gura's back eave (by design)
LINE_KINDS = ("ts_cmp_",)
ALLOW = {("BR2", "BR3")}    # the kasane-gura: the o-kura's eave over the mae-gura's back eave (by design)


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
        sb = SEAT_BOX.get(key)
        lo, hi = LW.ground_poly(LW.corners(bb if sb is None else (sb[0], sb[1], 0.0, 1.0, sb[2], sb[3]), pos, yaw,
                                           -0.3 if sb is None else 0.0))
        g0 = T.ground(x, z)
        clear = CLEAR.get(key)
        base = lo if clear is None else max(lo, hi - clear)
        if hi - lo > 0.05:
            problems.append("note %s: ground varies %.2f m under it (seated %s; the low side floats %.2f)" % (
                bid, hi - lo, "on the lowest point" if base == lo else "at the highest - %.2f" % clear, base - lo))
        if base - lo > 0.08:
            problems.append("FLOAT %s: %.2f m over its lowest ground" % (bid, base - lo))
        yoff = base - g0
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (r["model"].lstrip("\\"), x, z, yaw, yoff))
        if r.get("loot_points", 0):
            pos_xml.append('    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />'
                           % (r["class"], x, base, z, yaw, 90.0 - yaw))
        items.append({"id": bid, "class": r["class"], "p3d": r["model"].lstrip("\\"), "x": x, "z": z, "yaw": yaw,
                      "y_off": round(yoff, 3), "label": label, "area": bid[:2], "key": key})
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
                          "label": s["why"], "area": bid[:2]})
            pp = prop_poly(s["p3d"], wx, wz, (yaw + s["yaw"]) % 360.0)
            if pp:
                polys.append(("%s.s%d" % (bid, k + 1), pp))
    for eid, p3d, x, z, yaw, label in EXTRA:
        pp = prop_poly(p3d, x, z, yaw)
        lo, hi = LW.ground_poly(pp) if pp else (T.ground(x, z), T.ground(x, z))
        yoff = lo - T.ground(x, z)
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (p3d, x, z, yaw, yoff))
        items.append({"id": eid, "class": None, "p3d": p3d, "x": x, "z": z, "yaw": yaw, "y_off": round(yoff, 3),
                      "label": label, "area": eid[:2]})
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
        if os.path.basename(p) == "W3C1.csv":
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
    print("W3C1.csv %d rows, %d buildings, %d free objects, %d CE groups; %d problems (+%d notes)" % (
        len(rows) - 1, len(BUILDINGS), len(EXTRA), len(pos_xml), len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
