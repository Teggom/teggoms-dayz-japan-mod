"""W3C2: place wave 3c-2 (the rural / industrial sites) on the test island: ONE new district next to 3c-1's trade
quarter (Stephen, 2026-10-02: one district per wave, off the showcase).

  python spikes/W3C2/layout_w3c2.py   -> test/placements/W3C2.csv, test/ce/W3C2_mapgrouppos.xml, spikes/W3C2/w3c2_items.json

The district wraps round 3c-1 (x 884-946, z 852-892) on its west and south sides, x 826-952, z 818-900, on the
island's gentle ground (24.9-26.4 m, a 2-3 % fall to the south). A LOOP of lanes starts and ends on 3c-1's lane:
  LW   from 3c-1's lane west end (884, 864) west to x 826 (z 862-866)
  LWS  south down x 826-830 to z 834;  LS  east along z 834-838 to x 952;  LES  north up x 948-952 to 3c-1's lane east
       end (946, 864)
  NP / LN  a spur north from LW (x 878.5-882) to the logging camp lane (z 887-890)
North of LW: TL tile works (board-fenced yard: daruma kiln, moulding shed, drying shed), NB the climbing kiln (fire mouth
on the lane), PT the potter's bamboo-fenced yard. North on LN: LG the logging camp (timber slide, bunk hall, saw shed).
South of LW: QR the quarry face + quarrymen's shed + the stonemason's lanterns, LM the lime kiln + slaking shed, CH the
charcoal kiln + the burner's hut. South of LS: MN the mine (adit, sorting shed, miners' bunk hall, spoil, windlass).
North of LS: SL the salt works (salt bed, boiling hut, sieve stands) on dry land (Stephen's water-mill rule).
Checks as layout_w3c1.py (+ the lanes are kept clear).
"""
import csv
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit"),
          os.path.join(DEV, "spikes", "SH1"), os.path.join(DEV, "spikes", "W2F"), os.path.join(DEV, "spikes", "W3C1")):
    sys.path.insert(0, p)
import terrain_sh1 as T  # noqa: E402
from jpparts import decor as DC  # noqa: E402
from jpparts.templates import tradesite as TS  # noqa: E402,F401  (3c-1's yard plots)
from jpparts.templates import ruralsite as RSI  # noqa: E402,F401  (registers the 3c-2 yard plots)
from jpparts.templates import dwelling as DW  # noqa: E402
import layout_w2f as LW  # noqa: E402
import layout_w3c1 as L1  # noqa: E402

KEN = 1.82
CSV_OUT = os.path.join(DEV, "test", "placements", "W3C2.csv")
POS_OUT = os.path.join(DEV, "test", "ce", "W3C2_mapgrouppos.xml")
ITEMS = os.path.join(HERE, "w3c2_items.json")
DISTRICT = (826.0, 952.0, 818.0, 900.0)
LANES = {"LW": (826.0, 884.0, 862.0, 866.0), "LWS": (826.0, 830.0, 834.0, 866.0), "LS": (826.0, 952.0, 834.0, 838.0),
         "LES": (948.0, 952.0, 834.0, 866.0), "LE": (946.0, 952.0, 862.0, 866.0), "NP": (878.5, 882.0, 866.0, 890.0),
         "LN": (850.0, 882.0, 887.0, 890.0)}
TY = (838.5 + 5 * KEN, 867.5 + 3.5 * KEN)        # tile yard centre (SW 838.5, 867.5; 10 x 7 ken)
PY = (864.0 + 3.5 * KEN, 867.5 + 3 * KEN)        # pottery yard centre (SW 864.0, 867.5; 7 x 6 ken)
# seat: earth / board floors this far over grade may not have terrain through them (see layout_w3c1); the site objects
# (kilns, quarry, adit, slide, salt bed) carry bodies 0.30 under their grade, so they may sit higher on their low side
CLEAR = {"f_rs_sumiyaki": 0.04, "f_rs_toki": 0.04, "f_rs_kawara": 0.04, "f_rs_kawara_dry": 0.04, "f_rs_ishibai": 0.04,
         "f_rs_ishiku": 0.04, "f_rs_senko": 0.04, "f_rs_bunk_miners": 0.04, "f_rs_bunk_loggers": 0.04,
         "f_rs_kamaya": 0.04, "f_tr_timber_saw": 0.04,
         "rs_sumigama": 0.04, "rs_noborigama": 0.04, "rs_darumagama": 0.04, "rs_ishibaigama": 0.04, "rs_ishiba": 0.04,
         "rs_mabu": 0.04, "rs_shura": 0.04, "rs_enden": 0.28}
# how far a low side may float (its hidden skirt): earth-floored huts / sheds / kiln roofs keep their 0.20 doma slab
# to -0.15 under the wall line, so 0.14 never opens a gap; the salt bed's body runs to -0.30
FLOAT_OK = {"rs_enden": 0.28}
FLOAT_HUT = 0.14
# where a site object is seated: its work floor (model rect), so its bank / knoll / slide sinks into the rising ground
# behind it (on the real map: into the hill), and no floor has terrain through it
SEAT_BOX = {"rs_noborigama": (-1.82, 1.82, 4.99, 6.81), "rs_mabu": (-1.80, 1.80, 4.09, 6.01),
            "rs_ishiba": (-5.46, 5.46, 0.61, 4.09), "rs_ishibaigama": (-1.82, 1.82, 2.59, 4.41),
            "rs_shura": (-1.82, 1.82, 6.07, 8.79)}
SHRINK = 0.85          # huts / sheds: the ground is judged under the walls, not the eaves

# id, registry key, x, z, yaw, label
BUILDINGS = [
    # ---- TL tile works (north of LW, west)
    ("TL1", "rs_cmp_tileyard", TY[0], TY[1], 0.0, "the tile works' board fence, the two-leaf cart gate south on the lane"),
    ("TL2", "rs_darumagama", 843.0, 876.6, 180.0, "the daruma tile kiln under its roof: a fire mouth at each end, the "
     "loading door (walled up) to the yard"),
    ("TL3", "f_rs_kawara", 852.4, 876.4, 180.0, "the moulding shed (open front south): moulding bench with the "
     "half-carved onigawara, wedging board, a rack of green tiles; tally desk in the raised room"),
    ("TL4", "f_rs_kawara_dry", 843.0, 870.5, 0.0, "the drying shed (open north to the kiln): racks of green tiles, one "
     "collapsed, a pallet of fired tiles"),
    # ---- NB the climbing kiln (between the two yards, its fire mouth on the lane)
    ("NB1", "rs_noborigama", 859.7, 874.8, 180.0, "the climbing kiln: stokers' shelter on the lane, the firebox, four "
     "chambers stepping up its bank to the north, the stack; the lowest loading door open (east side)"),
    # ---- PT the potter (north of LW)
    ("PT1", "rs_cmp_potteryyard", PY[0], PY[1], 0.0, "the potter's bamboo fence, a 1.5-ken cart opening south on the lane"),
    ("PT2", "f_rs_toki", 870.4, 875.0, 180.0, "the potter's work shed (open front south): kick wheel, wedging board, "
     "ware racks, glaze tubs; finished wares in straw in the raised room"),
    # ---- LG the logging camp (north, on LN)
    ("LG1", "rs_shura", 858.0, 893.5, 90.0, "the timber slide's last 4 bays on trestles, falling east to the landing; "
     "a log stopped in it"),
    ("LG2", "f_rs_bunk_loggers", 873.5, 895.5, 180.0, "the loggers' bunk hall (stone-weighted roof, door south): axes and "
     "saws on the wall, straw beds round the irori"),
    ("LG3", "f_tr_timber_saw", 870.4, 883.0, 0.0, "the sawing shed (W3B's, as built): the log on its raised trestle "
     "(the Japanese method, no sawpit)"),
    # ---- QR quarry + stonemason (south of LW, west)
    ("QR1", "rs_ishiba", 837.0, 845.0, 0.0, "the quarry face (cut north): two benches, wedge-hole rows, the half-split "
     "block with its wedges, the masons' shelter on the splitting floor"),
    ("QR2", "f_rs_ishiku", 836.0, 856.0, 180.0, "the quarrymen's shed (open south to the face): the sharpening forge, "
     "anvil, quench tub, chisels and wedges"),
    # ---- LM lime
    ("LM1", "rs_ishibaigama", 853.0, 845.0, 0.0, "the lime kiln: a dry-stone pit on its earth bank, the draw hole north "
     "under its small roof, the burnt-out heap over the rim"),
    ("LM2", "f_rs_ishibai", 853.0, 855.8, 180.0, "the slaking and packing shed (open south to the kiln): lime in straw "
     "bales, sieves, the slaking tub"),
    # ---- CH charcoal
    ("CH1", "rs_sumigama", 866.5, 846.0, 0.0, "the charcoal kiln under its roof: the earth dome, the fire mouth north "
     "(opened), the flue at the back"),
    ("CH2", "f_rs_sumiyaki", 876.5, 846.5, 0.0, "the charcoal burner's hut (door north): stove, water jar, axe and saw, "
     "straw bed round the irori; bales outside"),
    # ---- MN mine (south of LS)
    ("MN1", "rs_mabu", 893.0, 826.0, 0.0, "the mine adit (portal north on the lane): a 4-ken timbered drift to a "
     "rockfall, the drainage trough, the mountain god's shrine"),
    ("MN2", "f_rs_senko", 904.5, 829.0, 0.0, "the sorting shed (open north): sorting bench, the stone ore mill, the "
     "washing sluice, ore baskets"),
    ("MN3", "f_rs_bunk_miners", 917.0, 828.5, 0.0, "the miners' bunk hall (door north): picks on the wall, straw beds "
     "round the irori"),
    # ---- SL salt works (north of LS, east)
    ("SL1", "rs_enden", 931.0, 846.0, 0.0, "the salt bed (irihama, dry land): the raked bed ramped up from the north, "
     "the dry ditch and the embankment + sluice on the south ('sea') side"),
    ("SL2", "f_rs_kamaya", 918.5, 846.0, 90.0, "the salt-boiling hut (front door east to the bed, side door south): the "
     "shell pan on its firebox under the smoke vent, fuel heap, draining baskets, salt bags"),
]
F = r"JP\furniture\sitefit\%s.p3d"
# free objects: id, p3d (P:-relative), x, z, yaw, label
EXTRA = [
    ("TL5", F % "jp_f_kawara_stack", 848.4, 869.4, 90.0, "fired tiles stacked for the carts"),
    ("TL6", F % "jp_f_kawara_stack_scattered", 848.4, 872.0, 90.0, "fired tiles, a row pushed over"),
    ("NB2", F % "jp_f_kiln_shelves", 862.9, 868.6, 90.0, "kiln shelves and props stacked by the kiln"),
    ("NB3", r"JP\furniture\kitchen\jp_f_firewood_stack.p3d", 862.9, 872.0, 90.0, "red-pine firewood for the kiln"),
    ("PT3", F % "jp_f_ware_rack", 867.5, 869.4, 0.0, "a ware rack in the yard: unfired bowls drying"),
    ("PT4", F % "jp_f_ware_rack_fallen", 867.5, 870.9, 0.0, "a ware rack, its top plank fallen"),
    ("LG4", r"JP\furniture\tradefit\jp_f_log_stack.p3d", 864.5, 897.6, 90.0, "felled logs stacked at the landing"),
    ("LG5", r"JP\furniture\tradefit\jp_f_log_stack_collapsed.p3d", 855.0, 898.3, 0.0, "a log stack, collapsed"),
    ("QR3", F % "jp_f_ishi_blocks", 841.8, 852.2, 0.0, "cut blocks on skids, wedge holes, the lord's mark"),
    ("QR4", F % "jp_f_ishi_shura", 846.2, 853.6, 90.0, "the stone sledge on its rollers with a block lashed on"),
    ("QR5", r"JP\site\shrine\jp_s_stone_lantern_kasuga_18.p3d", 842.4, 856.4, 0.0, "the stonemason's work: a finished "
     "lantern waiting"),
    ("QR6", r"JP\site\shrine\jp_s_stone_lantern_ab_toppled.p3d", 845.2, 858.6, 0.0, "a lantern fallen"),
    ("LM3", F % "jp_f_limestone_heap", 859.6, 852.6, 0.0, "broken limestone waiting for the next burn"),
    ("CH3", r"JP\furniture\tradefit\jp_f_log_stack.p3d", 866.5, 852.6, 0.0, "kiln billets stacked before the mouth"),
    ("CH4", r"JP\furniture\kitchen\jp_f_firewood_stack.p3d", 861.6, 846.0, 90.0, "split wood for the kiln"),
    ("MN4", F % "jp_f_spoil_heap", 884.8, 826.0, 0.0, "the mine's spoil heap"),
    ("MN5", F % "jp_f_makiage", 905.0, 822.4, 0.0, "a windlass over a boarded-over prospect shaft"),
    ("MN6", r"JP\furniture\meal\jp_f_basket_back_crushed.p3d", 899.6, 833.0, 0.0, "an ore basket dropped by the portal"),
    ("SL3", F % "jp_f_zaru_tori", 928.6, 853.2, 0.0, "a sieve stand by the bed: brine tubs, sea-water buckets"),
    ("SL4", F % "jp_f_zaru_tori_ab", 933.6, 853.2, 0.0, "a sieve stand, a basket tipped off"),
]
# FX7: the climbing kiln's new battered side slope widens NB1's footprint rect over the tile yard's fence line; the
# Geometry stays 0.2 m clear of the fence (measured, every component's world bbox), so the rect overlap is allowed
ALLOW = {("NB1", "TL1")}
LINE_KINDS = ("rs_cmp_",)


def main():
    rows, pos_xml, items, polys, problems = ["p3d,x,z,yaw_deg,y_offset"], [], [], [], []
    recs = L1.all_records()
    for bid, key, x, z, yaw, label in BUILDINGS:
        r = L1.rec(key)
        bb = r["bbox"]
        pos = (x, 25.0, z)
        sb = SEAT_BOX.get(key)
        if sb:
            lo, hi = LW.ground_poly(LW.corners((sb[0], sb[1], 0.0, 1.0, sb[2], sb[3]), pos, yaw, 0.0))
        else:
            lo, hi = LW.ground_poly(LW.corners(bb, pos, yaw, -SHRINK if key.startswith("f_") else -0.3))
        g0 = T.ground(x, z)
        clear = CLEAR.get(key)
        base = lo if clear is None else max(lo, hi - clear)
        if hi - lo > 0.05:
            problems.append("note %s: ground varies %.2f m under it (seated %s; the low side floats %.2f)" % (
                bid, hi - lo, "on the lowest point" if base == lo else "at the highest - %.2f" % clear, base - lo))
        if base - lo > FLOAT_OK.get(key, FLOAT_HUT):
            problems.append("FLOAT %s: %.2f m over its lowest ground" % (bid, base - lo))
        yoff = base - g0
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (r["model"].lstrip("\\"), x, z, yaw, yoff))
        if r.get("loot_points", 0):
            pos_xml.append('    <group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />'
                           % (r["class"], x, base, z, yaw, 90.0 - yaw))
        items.append({"id": bid, "class": r["class"], "p3d": r["model"].lstrip("\\"), "x": x, "z": z, "yaw": yaw,
                      "y_off": round(yoff, 3), "label": label, "area": bid[:2], "key": key})
        if key.startswith(LINE_KINDS):
            for k, sp in enumerate(L1.strips(key, pos, yaw)):
                polys.append((bid + ".w%d" % k, sp))
        else:
            polys.append((bid, LW.corners(bb, pos, yaw)))
        for k, s in enumerate(r.get("site", [])):
            wx, wz = LW.to_world(s["x"], s["z"], pos, yaw)
            # a site prop outside the walls sits on its OWN ground (the building may be seated higher on a slope)
            spp = L1.prop_poly(s["p3d"], wx, wz, (yaw + s["yaw"]) % 360.0)
            sy = (LW.ground_poly(spp)[0] if spp else T.ground(wx, wz)) + s.get("y", 0.0)
            rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (s["p3d"].lstrip("\\"), wx, wz, (yaw + s["yaw"]) % 360.0,
                                                    sy - T.ground(wx, wz)))
            items.append({"id": "%s.s%d" % (bid, k + 1), "class": None, "p3d": s["p3d"].lstrip("\\"), "x": round(wx, 3),
                          "z": round(wz, 3), "yaw": (yaw + s["yaw"]) % 360.0, "y_off": round(sy - T.ground(wx, wz), 3),
                          "label": s["why"], "area": bid[:2]})
            pp = L1.prop_poly(s["p3d"], wx, wz, (yaw + s["yaw"]) % 360.0)
            if pp:
                polys.append(("%s.s%d" % (bid, k + 1), pp))
    for eid, p3d, x, z, yaw, label in EXTRA:
        pp = L1.prop_poly(p3d, x, z, yaw)
        if not pp:
            problems.append("NOCAT %s %s (not in the decor catalogue)" % (eid, p3d))
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
            if LW.poly_hit(a[1], b[1]):
                problems.append("OVERLAP %s x %s" % (a[0], b[0]))
    for nm, (a0, a1, c0, c1) in LANES.items():
        for nid, p in polys:
            if LW.poly_hit(p, [(a0, c0), (a1, c0), (a1, c1), (a0, c1)]):
                problems.append("LANE %s blocked by %s" % (nm, nid))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) == "W3C2.csv":
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
    print("W3C2.csv %d rows, %d buildings, %d free objects, %d CE groups; %d problems (+%d notes)" % (
        len(rows) - 1, len(BUILDINGS), len(EXTRA), len(pos_xml), len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
