"""W2F: place the furnished wave-2 buildings on the test island (own drop-ins, not registry placements).

  python spikes/W2F/layout_w2f.py            -> test/placements/W2F.csv, test/ce/W2F_mapgrouppos.xml,
                                                spikes/W2F/w2f_items.json (every object: id, class, p3d, pos, label)
Areas (world metres, spawn (1024, 985)):
  P  town shrine precinct: the hall site at the head of the SH1 approach (x 1024, z 1185-1208), the halls on stone
     terraces (the ground rises 1 m across the hall site), temizuya / shamusho / kagura west of the approach
  V  village shrine north of the C2 hamlet (x 945, z 1060-1081)
  T  village temple (Jodo) west of the SH1 graveyard (x 947-987, z 1101-1129)
  U  town temple (Zen) east of the street end (x 1079-1121, z 1095-1124)
  K  civic set at both street ends: kido + keeper's hut and tea houses east, smithy / swordsmith / jishin-ban west
Checks: footprints vs each other, vs every building record placed by C.csv, vs every point of the other CSVs
(C3 / SH1 / F / M), vs the reserved spots and T's trees; terraces vs the ground behind them.
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
          os.path.join(DEV, "spikes", "SH1")):
    sys.path.insert(0, p)
import terrain_sh1 as T  # noqa: E402
from jpkit import loot as bloot  # noqa: E402
from jpparts import decor as DC  # noqa: E402

REC = os.path.join(DEV, "buildings", "furnished", "records")
CSV_OUT = os.path.join(DEV, "test", "placements", "W2F.csv")
POS_OUT = os.path.join(DEV, "test", "ce", "W2F_mapgrouppos.xml")
ITEMS = os.path.join(HERE, "w2f_items.json")
TERR = {"jp_f_terrace_l": (12.0, 11.0, 1.35), "jp_f_terrace_m": (10.0, 7.4, 1.80)}
TERR_RUN = {k: math.ceil(v[2] / 0.16) * 0.91 / 3 for k, v in TERR.items()}

# id, furnished key, x, z, yaw, seat ('flat' | 'lowest' | ('terrace', name, model-z offset of its centre)), label
BUILDINGS = [
    ("P1", "f_shrine_haiden_town", 1024.0, 1192.0, 180.0, ("terrace", "jp_f_terrace_l", 0.90),
     "town haiden (Hachimangu): drum, offerings, bell rope, name board"),
    ("P2", "f_shrine_honden_nagare_town", 1024.0, 1207.0, 180.0, ("terrace", "jp_f_terrace_m", 1.29),
     "town honden (nagare sangen-sha, curved bark roof), sanctum sealed"),
    ("P3", "f_shrine_temizuya_town", 1014.0, 1147.0, 90.0, "lowest", "temizuya: basin + ladles"),
    ("P4", "f_shrine_shamusho_sangawara", 1011.0, 1165.0, 90.0, "lowest", "shamusho: amulet counter, talisman desk"),
    ("P5", "f_shrine_kagura_town", 1011.5, 1188.5, 90.0, "lowest", "kagura stage: drums, masks"),
    ("V1", "f_shrine_haiden_village", 945.0, 1070.0, 180.0, "flat", "village haiden: drum, offerings, bell rope"),
    ("V2", "f_shrine_honden_nagare_village_chigi", 945.0, 1078.5, 180.0, "flat",
     "village honden (nagare, chigi + katsuogi), sanctum sealed"),
    ("T1", "f_temple_hondo_village", 972.0, 1123.5, 180.0, "lowest", "village hondo (Jodo): Amida, sutra desk"),
    ("T2", "f_temple_kuri_village", 955.0, 1122.0, 180.0, "lowest", "village kuri: kamado row, irori, guest room"),
    ("T3", "f_temple_shoro_village", 984.0, 1112.0, 180.0, "flat", "village bell tower with its bell"),
    ("T4", "f_temple_gate_yakuimon", 972.0, 1104.5, 180.0, "flat", "village temple gate (yakui-mon)"),
    ("T5", "f_temple_do_2_board", 962.0, 1109.5, 90.0, "flat", "Jizo hall"),
    ("U1", "f_temple_hondo_town", 1100.0, 1112.0, 180.0, "flat", "town hondo (Zen): Shaka, big mokugyo, drum"),
    ("U2", "f_temple_kuri_town", 1114.5, 1111.0, 180.0, "flat", "town kuri (Zen): fish board, cloud gong"),
    ("U3", "f_temple_shoro_town", 1085.5, 1118.5, 90.0, "flat", "town bell tower (hakama), the bell upstairs"),
    ("U4", "f_temple_gate_shikyakumon", 1100.0, 1097.5, 180.0, "flat", "town temple gate (shikyaku-mon)"),
    ("U5", "f_temple_do_3_tile", 1083.0, 1104.0, 90.0, "flat", "Kannon hall"),
    ("K1", "f_kido_lattice_bantaya", 1069.0, 1080.0, 90.0, "flat",
     "ward gate (kido) across the street's east end + the keeper's hut (hinged gate leaves)"),
    ("K2", "f_teahouse_shop_thatch", 1075.5, 1086.8, 180.0, "flat", "tea house (chamise, thatch) at the street end"),
    ("K3", "f_teahouse_bench_itabuki", 1074.5, 1073.0, 0.0, "flat", "bench tea house across the road"),
    ("K4", "f_teahouse_tateba_itabuki", 1091.0, 1086.5, 180.0, "flat", "rest-stop tea house with rooms (tateba)"),
    ("K5", "f_smithy_open_itabuki", 969.5, 1086.0, 180.0, "flat", "village smithy (cold forge, bellows, anvil)"),
    ("K6", "f_swordsmith_sangawara", 967.0, 1072.0, 0.0, "flat", "swordsmith (forge room + work room)"),
    ("K7", "f_guardhut_m_itabuki", 977.5, 1072.5, 0.0, "flat", "jishin-ban guard house with the ridge fire ladder"),
]
# loose site objects: id, p3d name (catalogue), x, z, yaw, label
EXTRA = [
    ("V3", "jp_s_torii_wood_shinmei_rope_shide", 945.0, 1061.0, 180.0, "village shrine torii (shinmei, rope + streamers)"),
    ("V4", "jp_s_stone_lantern_oki_moss", 942.6, 1063.2, 90.0, "village shrine lantern (west)"),
    ("V5", "jp_s_stone_lantern_oki_moss", 947.4, 1063.2, 270.0, "village shrine lantern (east)"),
    ("T6", "jp_s_stone_lantern_kasuga_18_moss", 969.0, 1109.5, 90.0, "temple lantern (west of the walk)"),
    ("T7", "jp_s_stone_lantern_kasuga_18_moss", 975.0, 1109.5, 270.0, "temple lantern (east of the walk)"),
    ("T8", "jp_s_stone_jizo_bib", 958.4, 1106.8, 90.0, "a stone Jizo with its bib by the Jizo hall"),
    ("U6", "jp_s_stone_lantern_kasuga_24", 1097.0, 1102.5, 90.0, "temple lantern (west)"),
    ("U7", "jp_s_stone_lantern_kasuga_24", 1103.0, 1102.5, 270.0, "temple lantern (east)"),
    ("U8", "jp_s_chozubachi_small", 1094.0, 1103.0, 90.0, "temple water basin"),
]
RESERVED = {"spawn": (1014, 1034, 975, 995), "item grid": (995, 1035, 965, 985), "sakura W": (980, 990, 1005, 1015),
            "sakura E": (1058, 1068, 1005, 1015), "bamboo": (1080, 1110, 955, 995), "range": (995, 1055, 925, 950)}


def rec(key):
    with open(os.path.join(REC, key + ".json"), "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def to_world(mx, mz, pos, yaw):
    w = bloot.model_to_world((mx, 0.0, mz), pos, yaw)
    return w[0], w[2]


def corners(bb, pos, yaw, pad=0.0):
    x0, x1, z0, z1 = bb[0] - pad, bb[1] + pad, bb[4] - pad, bb[5] + pad
    return [to_world(x, z, pos, yaw) for x, z in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))]


def ground_poly(poly):
    gs = [T.ground(x, z) for x, z in poly]
    cx = sum(p[0] for p in poly) / 4
    cz = sum(p[1] for p in poly) / 4
    for i in range(4):                                      # edge midpoints too
        a, b = poly[i], poly[(i + 1) % 4]
        gs.append(T.ground((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
    gs.append(T.ground(cx, cz))
    return min(gs), max(gs)


def other_buildings():
    """[(name, poly)] of the buildings C.csv places (their record bbox)."""
    recs = {}
    for p in glob.glob(os.path.join(DEV, "buildings", "*", "records", "*.json")) + \
            glob.glob(os.path.join(DEV, "buildings", "*", "record.json")):
        try:
            with open(p, "rb") as f:
                r = json.loads(f.read().decode("utf-8"))
        except Exception:
            continue
        if r.get("model") and r.get("bbox"):
            recs[r["model"].lstrip("\\").lower()] = r["bbox"]
    out = []
    with open(os.path.join(DEV, "test", "placements", "C.csv"), newline="") as f:
        for row in csv.DictReader(f):
            k = row["p3d"].lower()
            if k in recs:
                out.append((row["p3d"], corners(recs[k], (float(row["x"]), 25.0, float(row["z"])), float(row["yaw_deg"]))))
    return out


def other_points():
    pts = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) in ("W2F.csv",):
            continue
        with open(p, newline="") as f:
            for row in csv.DictReader(f):
                if os.path.basename(p) == "C.csv" and "\\buildings\\" in row["p3d"].lower():
                    continue
                pts.append((os.path.basename(p), row["p3d"], float(row["x"]), float(row["z"])))
    return pts


def poly_hit(a, b):
    return DC.polys_intersect(a, b)


def main():
    rows, pos_xml, items, polys, problems = ["p3d,x,z,yaw_deg,y_offset"], [], [], [], []
    cat = DC.catalog()
    for bid, key, x, z, yaw, seat, label in BUILDINGS:
        r = rec(key)
        bb = r["bbox"]
        pos = (x, 25.0, z)
        poly = corners(bb, pos, yaw)
        g0 = T.ground(x, z)
        if seat == "flat":
            base = g0
        elif seat == "lowest":
            lo, hi = ground_poly(corners(bb, pos, yaw, -0.3))
            base = lo
            if hi - lo > 0.05:
                problems.append("note %s: seated on its lowest corner, uphill side %.2f m into the slope" % (bid, hi - lo))
        else:
            _, tname, dzc = seat
            W_, D, H = TERR[tname]
            tc = to_world(0.0, dzc, pos, yaw)
            tpoly = [to_world(mx, mz, pos, yaw) for mx, mz in ((-W_ / 2, dzc - D / 2), (W_ / 2, dzc - D / 2),
                                                             (W_ / 2, dzc + D / 2), (-W_ / 2, dzc + D / 2))]
            fpoly = [to_world(mx, mz, pos, yaw) for mx, mz in ((-1.45, dzc + D / 2), (1.45, dzc + D / 2),
                                                             (1.45, dzc + D / 2 + TERR_RUN[tname]),
                                                             (-1.45, dzc + D / 2 + TERR_RUN[tname]))]
            polys.append((bid + "f", fpoly))
            front = [to_world(mx, dzc + D / 2, pos, yaw) for mx in (-W_ / 2, 0.0, W_ / 2)]
            back = [to_world(mx, dzc - D / 2, pos, yaw) for mx in (-W_ / 2, 0.0, W_ / 2)]
            foot = [to_world(mx, dzc + D / 2 + TERR_RUN[tname], pos, yaw) for mx in (-1.2, 1.2)]
            tbase = min(T.ground(*p) for p in front + foot) - 0.06
            top = tbase + H
            gback = max(T.ground(*p) for p in back)
            if top < gback - 0.02:
                problems.append("TERRACE %s: top %.2f below the ground behind it %.2f" % (bid, top, gback))
            elif top - gback > 0.25:
                problems.append("note %s terrace: back edge stands %.2f m proud of the ground" % (bid, top - gback))
            p3d = cat[tname]["p3d"].lstrip("\\")
            rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (p3d, tc[0], tc[1], yaw, tbase - T.ground(*tc)))
            items.append({"id": bid + "t", "class": cat[tname]["cls"], "p3d": p3d, "x": round(tc[0], 3),
                          "z": round(tc[1], 3), "yaw": yaw, "y_off": round(tbase - T.ground(*tc), 3),
                          "label": "stone terrace under %s (%.1f m at the front)" % (bid, H), "area": bid[0]})
            polys.append((bid + "t", tpoly))
            base = top
        yoff = base - g0
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (r["model"].lstrip("\\"), x, z, yaw, yoff))
        pos_xml.append('    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />'
                       % (r["class"], x, base, z, yaw, 90.0 - yaw))
        items.append({"id": bid, "class": r["class"], "p3d": r["model"].lstrip("\\"), "x": x, "z": z, "yaw": yaw,
                      "y_off": round(yoff, 3), "label": label, "area": bid[0], "key": key})
        polys.append((bid, poly))
        for k, s in enumerate(r.get("site", [])):
            wx, wz = to_world(s["x"], s["z"], pos, yaw)
            sy = base + s.get("y", 0.0)
            rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (s["p3d"].lstrip("\\"), wx, wz, (yaw + s["yaw"]) % 360.0,
                                                    sy - T.ground(wx, wz)))
            items.append({"id": "%s.s%d" % (bid, k + 1), "class": None, "p3d": s["p3d"].lstrip("\\"), "x": round(wx, 3),
                          "z": round(wz, 3), "yaw": (yaw + s["yaw"]) % 360.0, "y_off": round(sy - T.ground(wx, wz), 3),
                          "label": s["why"], "area": bid[0]})
    for eid, name, x, z, yaw, label in EXTRA:
        inf = cat[name]
        b = inf["bbox"]
        poly = corners(b, (x, 25.0, z), yaw)
        lo, _ = ground_poly(poly)
        yoff = lo - T.ground(x, z) - (0.19 if "jizo" in name else 0.0)     # placecheck: a statue base sits 5 cm in
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (inf["p3d"].lstrip("\\"), x, z, yaw, yoff))
        items.append({"id": eid, "class": inf["cls"], "p3d": inf["p3d"].lstrip("\\"), "x": x, "z": z, "yaw": yaw,
                      "y_off": round(yoff, 3), "label": label, "area": eid[0]})
        polys.append((eid, poly))
    # ---- checks
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            a, b = polys[i], polys[j]
            if a[0].rstrip("tf") == b[0].rstrip("tf"):
                continue
            if poly_hit(a[1], b[1]):
                problems.append("OVERLAP %s x %s" % (a[0], b[0]))
    for name, poly in other_buildings():
        for nid, p in polys:
            if poly_hit(poly, p):
                problems.append("OVERLAP %s x existing building %s" % (nid, name))
    for src, p3d, x, z in other_points():
        for nid, p in polys:
            if DC.point_poly_dist((x, z), p) < 0.3:
                problems.append("CLASH %s with %s %s at (%.1f, %.1f)" % (nid, src, os.path.basename(p3d), x, z))
    for nm, (a0, a1, c0, c1) in RESERVED.items():
        for nid, p in polys:
            if poly_hit(p, [(a0, c0), (a1, c0), (a1, c1), (a0, c1)]):
                problems.append("RESERVED %s in %s" % (nid, nm))
    tr = T.trees()
    for t in tr:
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
    print("W2F.csv %d rows, %d buildings, %d CE groups; %d problems (+%d notes)" % (
        len(rows) - 1, len(BUILDINGS), len(pos_xml), len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
