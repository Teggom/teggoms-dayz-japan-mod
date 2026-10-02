"""D3: place the wave-3a buildings, compounds and corridors on the test island (own drop-ins, not registry placements).

  python spikes/D3/layout_d3.py       -> test/placements/D3.csv, test/ce/D3_mapgrouppos.xml, spikes/D3/d3_items.json

Areas (world metres; spawn (1024, 985)):
  S  samurai quarter, south-west of the yard (x 924-991, z 937-993) along the samurai lane (z ~957): the hatamoto mansion
     (furnished) behind its samurai nagaya-mon in a black board fence, two doshin houses in board-fenced plots, the
     foot-soldier row behind its bamboo fence
  H  the Kanto headman's compound by the hamlet (x 924-960, z 961-992): the board nagaya-mon in a clipped hedge ring,
     the house, the board storehouse, the stable, the bath hut
  J  the honjin (x 1092-1123, z 1020-1068) by the street's east end: plastered street wall + the roofed kabuki-mon, the
     formal block (omote) and the family / kitchen block (oku) linked by a covered corridor; the waki-honjin (no gate)
     south of it, facing the honjin's back gate
  M  the great merchant's residence behind the Edo row (x 1038-1068, z 1099-1127): board fence, the tea hut and a kura
     in the garden
  E  south-east: the Kinai headman's house and the coastal (fisherman's) house; the mountain house east of the street
  U  the town temple U (W2F): the covered corridor from the hondo's side veranda to the kuri's genkan porch
Checks as spikes/W2F/layout_w2f.py: footprints vs each other (compound rings are lines: their objects are checked as
their wall strips), vs every building C.csv / W2F.csv / C3.csv place, vs every point of the other CSVs, the reserved
spots, T's trees; the ground under each footprint (flat seats).
"""
import csv
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit"),
          os.path.join(DEV, "spikes", "SH1"), os.path.join(DEV, "spikes", "W2F")):
    sys.path.insert(0, p)
import terrain_sh1 as T  # noqa: E402
from jpkit import loot as bloot  # noqa: E402
from jpparts import decor as DC  # noqa: E402
import layout_w2f as LW  # noqa: E402

KEN = 1.82
CSV_OUT = os.path.join(DEV, "test", "placements", "D3.csv")
POS_OUT = os.path.join(DEV, "test", "ce", "D3_mapgrouppos.xml")
ITEMS = os.path.join(HERE, "d3_items.json")

# --- the honjin: omote at (OX, OZ) yaw 270 (porch north); oku (OX + 1.365, OZ - 19.11) (the corridor doors line up,
# the gables 2 ken apart); the corridor between them; the compound plot SW corner (1092.0, 1020.5)
OX, OZ = 1106.29, 1052.84
KX, KZ = OX + 1.365, OZ - 8.19 - 7.28 - 2 * KEN
HJ_SW = (1094.0, 1020.5)
# --- the samurai mansion: plot SW (967.14, 961.0), 13 x 17.5 ken; the nagaya-mon in the 4.5..11.5 ken gap
SM_SW = (967.14, 961.0)
HD_SW = (924.0, 961.0)
MR_SW = (1038.0, 1099.5)
DS1_SW, DS2_SW = (950.0, 937.5), (970.0, 937.5)


def cen(sw, w_ken, d_ken):
    return (sw[0] + w_ken * KEN / 2, sw[1] + d_ken * KEN / 2)


# id, registry key, x, z, yaw, label
BUILDINGS = [
    # S: samurai quarter
    ("S1", "f_dw_samurai_m", 978.97, 979.05, 90.0, "hatamoto mansion (furnished): genkan porch south, the zashiki with "
     "tokonoma + chigaidana, garden engawa west, kitchen north"),
    ("S2", "f_dw_nagayamon", 981.70, 962.82, 180.0, "samurai nagaya-mon (furnished): the gate passage, servants' room, "
     "storage; plaster + namako"),
    ("S3", "dw_cmp_samurai_m", cen(SM_SW, 13, 17.5)[0], cen(SM_SW, 13, 17.5)[1], 0.0,
     "the mansion's black board fence + back gate (north)"),
    ("S4", "kura_plain", 975.0, 989.6, 0.0, "the mansion's kura (plain), door south"),
    ("S5", "f_dw_kumi", 937.0, 946.9, 0.0, "foot-soldier row (furnished: sword unit, umbrella side-job unit, an "
     "abandoned unit), doors north"),
    ("S6", "dw_cmp_kumi", 937.0, 953.0 + 0.91, 0.0, "the row's bamboo (yotsume) fence + small gate on the lane"),
    ("S7", "f_dw_doshin", 959.1, 944.8, 0.0, "doshin house (furnished), entrance on the east gable"),
    ("S8", "dw_cmp_doshin", cen(DS1_SW, 10, 8)[0], cen(DS1_SW, 10, 8)[1], 0.0, "board fence + kabuki gate (north)"),
    ("S9", "dw_doshin_sangawara", 979.1, 944.8, 0.0, "doshin house (tiled, bare), entrance on the east gable"),
    ("S10", "dw_cmp_doshin", cen(DS2_SW, 10, 8)[0], cen(DS2_SW, 10, 8)[1], 0.0, "board fence + kabuki gate (north)"),
    # H: Kanto headman compound by the hamlet
    ("H1", "f_dw_headman_east", 942.20, 977.16, 180.0, "Kanto headman house (furnished): genkan doma + shikidai at the "
     "east end of the front, the formal zashiki"),
    ("H2", "dw_nagayamon_headman", 942.20, 962.82, 180.0, "the headman's board nagaya-mon (bare)"),
    ("H3", "dw_cmp_headman_east", cen(HD_SW, 20, 17)[0], cen(HD_SW, 20, 17)[1], 0.0,
     "clipped hedge ring + back gate (north)"),
    ("H4", "f_dw_itagura", 954.0, 988.0, 180.0, "board storehouse on rat-guarded posts (furnished: grain)"),
    ("H5", "f_dw_stable", 930.0, 987.5, 180.0, "stable (furnished: two horse stalls)"),
    ("H6", "f_dw_furoba", 941.0, 987.7, 180.0, "bath hut (furnished)"),
    # J: the honjin + waki-honjin
    ("J1", "f_dw_honjin_omote", OX, OZ, 270.0, "honjin formal block (furnished): genkan + shikidai north, the "
     "jodan-no-ma (raised) with tokonoma + chigaidana, engawa east"),
    ("J2", "f_dw_honjin_oku", KX, KZ, 270.0, "honjin family / kitchen block (furnished), the family's door west"),
    ("J3", "dw_roka_honjin", OX - 1.365, OZ - 8.19 - KEN, 0.0, "covered corridor omote <-> oku (half walls, tiled)"),
    ("J4", "dw_cmp_honjin", cen(HJ_SW, 17, 26)[0], cen(HJ_SW, 17, 26)[1], 0.0,
     "plastered street wall + roofed kabuki-mon (north), board fence, back gate (south)"),
    ("J5", "f_dw_wakihonjin", 1110.0, 1005.0, 270.0, "waki-honjin (furnished; no gate): genkan north facing the "
     "honjin's back gate"),
    # M: the great merchant
    ("M1", "f_dw_merchant", 1051.5, 1107.0, 180.0, "great merchant residence (furnished): kitchen door south, the "
     "garden engawa north"),
    ("M2", "dw_cmp_merchant", cen(MR_SW, 16.5, 15)[0], cen(MR_SW, 16.5, 15)[1], 0.0, "board fence + gate (south)"),
    ("M3", "f_dw_chashitsu", 1060.0, 1121.0, 180.0, "tea hut in the merchant's garden (furnished)"),
    ("M4", "kura_namako", 1043.0, 1120.0, 90.0, "the merchant's kura (namako), door east"),
    # E: south-east + east
    ("E1", "f_dw_headman_kinai", 1078.0, 937.0, 180.0, "Kinai headman house (furnished): the tiled genkan lean-to on the "
     "east gable"),
    ("E2", "f_dw_coastal", 1113.0, 938.0, 180.0, "coastal (fisherman's) house (furnished): the net store on the east"),
    ("E3", "f_dw_mountain", 1113.0, 1080.0, 180.0, "mountain house (furnished): stone-weighted boards, the hidana"),
    # U: the corridor at the town temple
    ("U9", "dw_roka_temple_u", 1104.627 + KEN, 1109.45, 0.0, "covered corridor: the hondo's east veranda -> the kuri's "
     "genkan porch (step down at the porch)"),
]
EXTRA = []
LINE_KINDS = ("dw_cmp_",)                         # ring objects: overlap-checked as their wall strips only
# designed abutments: a gatehouse stands in its compound's gap (the wall ends meet its corners); a corridor's
# connectors meet its host buildings' gable walls
ALLOW = {("S2", "S3"), ("H2", "H3"), ("J1", "J3"), ("J2", "J3")}


def rec(key):
    for p in glob.glob(os.path.join(DEV, "buildings", "*", "records", key + ".json")):
        with open(p, "rb") as f:
            return json.loads(f.read().decode("utf-8"))
    raise KeyError(key)


def strips(key, pos, yaw):
    """The wall strips of a compound (0.6 m wide polygons along its runs), world frame."""
    sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
    from jpparts.templates import dwelling as DW
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


def main():
    rows, pos_xml, items, polys, problems = ["p3d,x,z,yaw_deg,y_offset"], [], [], [], []
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
    # ---- checks
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            a, b = polys[i], polys[j]
            ia, ib = a[0].split(".")[0], b[0].split(".")[0]
            if ia == ib or (ia, ib) in ALLOW or (ib, ia) in ALLOW:
                continue
            if LW.poly_hit(a[1], b[1]):
                problems.append("OVERLAP %s x %s" % (a[0], b[0]))
    for name, poly in LW.other_buildings():
        for nid, p in polys:
            if LW.poly_hit(poly, p):
                problems.append("OVERLAP %s x existing building %s" % (nid, name))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) in ("D3.csv",):
            continue
        with open(p, newline="") as f:
            for row in csv.DictReader(f):
                if os.path.basename(p) == "C.csv" and "\\buildings\\" in row["p3d"].lower():
                    continue
                others.append((os.path.basename(p), row["p3d"], float(row["x"]), float(row["z"])))
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
    print("D3.csv %d rows, %d buildings, %d CE groups; %d problems (+%d notes)" % (
        len(rows) - 1, len(BUILDINGS), len(pos_xml), len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
