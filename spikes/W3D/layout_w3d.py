"""W3D: place wave 3d (the government buildings) on the test island: ONE new district west of 3c-2's west lane
(Stephen's one-district rule).

  python spikes/W3D/layout_w3d.py   -> test/placements/W3D.csv, test/ce/W3D_mapgrouppos.xml, spikes/W3D/w3d_items.json

District x 744-826, z 845-892 (24.0-25.7 m: a ~1.3 % fall west along the lane, ~3 % to the south). ONE lane, LG, from
3c-2's west-lane corner (826, 864) west along z 862-866 through the checkpoint's two kora-mon gates to x 744 (the
route's far landmark is the Kyoto-side gate). North of LG: JY the intendant's jinya (black nagaya-mon on the lane,
the office, the court room with its white-gravel court, the tax-rice kura). South of LG, from the east: TY the
post-station office and its yard, FB the fire brigade (the tall watchtower + the tool shed), RY the jail (cell block,
guard office). At the west end SK the checkpoint (palisade, two gates across the lane, the guardhouse with the gravel
court north of the road, the foot-soldiers' guardhouse south of it, the capture-tool rack, the notice board outside the
Edo-side gate). Checks as layout_w3c2.py; compounds seated on their lowest ground (the board fences may sink on their
high side, never float), the palisade mid-slope (its logs run 1 m into the ground).
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
from jpparts.templates import govsite as GV  # noqa: E402,F401  (registers the 3d plots)
import layout_w2f as LW  # noqa: E402
import layout_w3c1 as L1  # noqa: E402

KEN = 1.82
CSV_OUT = os.path.join(DEV, "test", "placements", "W3D.csv")
POS_OUT = os.path.join(DEV, "test", "ce", "W3D_mapgrouppos.xml")
ITEMS = os.path.join(HERE, "w3d_items.json")
DISTRICT = (744.0, 826.0, 845.0, 892.0)
LANES = {"LG": (744.0, 826.0, 862.0, 866.0)}
SK = (748.0 + 6.5 * KEN, 864.0 - 5.25 * KEN + 6.0 * KEN)       # checkpoint plot centre (SW 748.0, 854.45; 13 x 12 ken)
JY = (784.0 + 11 * KEN, 867.5 + 6.5 * KEN)                     # jinya plot centre (SW 784.0, 867.5; 22 x 13 ken)
TYC = (808.5 + 4.5 * KEN, 846.68 + 4.0 * KEN)                  # toiya yard (SW 808.5, 846.68; 9 x 8 ken), yaw 180
FBC = (792.5 + 4 * KEN, 848.5 + 3.5 * KEN)                     # fire brigade (SW 792.5, 848.5; 8 x 7 ken), yaw 180
RYC = (773.0 + 5 * KEN, 845.0 + 4.5 * KEN)                     # jail (SW 773.0, 845.0; 10 x 9 ken), yaw 180
CLEAR = {"gv_cmp_sekisho": 0.60}            # the palisade is seated 0.60 under its highest ground (logs to -1.00)
# how far a low side may float: the palisade's logs run 1 m down; the board fences have a 0.60 skirt; the W3D
# halls stand on a cut-stone foundation band to -0.55 (w3d_sets._plinth); the gravel courts' body runs to -0.20
FLOAT_OK = {"gv_cmp_sekisho": 0.95, "gv_cmp_jinya": 0.55, "gv_cmp_toiyayard": 0.55, "gv_cmp_hikeshi": 0.55,
            "gv_cmp_roya": 0.55, "f_gv_bansho": 0.50, "f_gv_bunk_ashigaru": 0.50, "f_gv_toiyaba": 0.50,
            "f_gv_jinya": 0.50, "f_gv_roya": 0.50, "f_gv_nagayamon_jinya": 0.50, "gv_oshirasu_s": 0.15,
            "gv_oshirasu_j": 0.15}
FLOAT_HUT = 0.14
SEAT_BOX = {}
SHRINK = 0.85

# id, registry key, x, z, yaw, label
BUILDINGS = [
    # ---- SK the checkpoint (west end; the lane through both gates)
    ("SK1", "gv_cmp_sekisho", SK[0], SK[1], 0.0, "the checkpoint's palisade: the Edo-side kora-mon east on the lane, the "
     "Kyoto-side kora-mon west"),
    ("SK2", "f_gv_bansho", 755.28, 871.79, 180.0, "the guardhouse (front south to the road): the inspection room's veranda "
     "+ tatami over the gravel court, the back office, the kitchen doma (west)"),
    ("SK3", "gv_oshirasu_s", 754.80, 867.30, 0.0, "the gravel court before the inspection room (where travellers knelt)"),
    ("SK4", "f_gv_bunk_ashigaru", 761.00, 858.40, 0.0, "the foot-soldiers' guardhouse (door north to the road): bedding, "
     "the capture tools on the wall"),
    # ---- JY the jinya (north of the lane)
    ("JY1", "gv_cmp_jinya", JY[0], JY[1], 0.0, "the jinya's black board fence; the back gate on the west line"),
    ("JY2", "f_gv_nagayamon_jinya", 804.02, 869.32, 180.0, "the black nagaya-mon on the lane (gate leaves, servants' room, "
     "store)"),
    ("JY3", "f_gv_jinya", 793.64, 883.64, 180.0, "the intendant's office (genkan south): clerks' desks, ledgers, the "
     "abacus, the rice measures; the intendant's room with its tokonoma"),
    ("JY4", "gv_oshirasu_j", 818.00, 878.60, 0.0, "the white-gravel court (oshirasu) before the court room"),
    ("JY5", "f_gv_ginmisho", 818.15, 885.70, 180.0, "the court room (front south over the gravel court): veranda + "
     "tatami, the official's desk; the records office behind"),
    ("JY6", "f_gv_kura_nengu", 818.40, 871.20, 0.0, "the tax-rice kura (door north to the court): bales on both floors"),
    # ---- TY the post-station office + yard (south of the lane, east)
    ("TY1", "gv_cmp_toiyayard", TYC[0], TYC[1], 180.0, "the post-station yard's board fence, the two-leaf gate north on "
     "the lane"),
    ("TY2", "f_gv_toiyaba", 816.69, 851.00, 0.0, "the post-station office (open north to the yard): the raised office "
     "with the clerks' desks and ledgers, the clerks' doma"),
    # ---- FB the fire brigade (south of the lane)
    ("FB1", "gv_cmp_hikeshi", FBC[0], FBC[1], 180.0, "the fire brigade's board fence, the wide gate north on the lane"),
    ("FB2", "f_gv_hikeshi", 802.60, 852.40, 0.0, "the brigade's tool shed (open north): the matoi-nobori, hooks, buckets"),
    # ---- RY the jail (south of the lane, west)
    ("RY1", "gv_cmp_roya", RYC[0], RYC[1], 180.0, "the jail's black board fence, its one gate north on the lane"),
    ("RY2", "f_gv_roya", 780.50, 849.40, 0.0, "the cell block (door north): the outer lattice, the corridor, two cells "
     "behind the inner lattice, their doors open"),
    ("RY3", "f_guardhut_m_itabuki", 777.00, 857.50, 90.0, "the guard office (the jishin-ban as built; door east)"),
]
F = r"JP\furniture\govfit\%s.p3d"
# free objects: id, p3d (P:-relative), x, z, yaw, label[, dy = height over the ground, or the id of the gravel court
# object it lies on]
EXTRA = [
    ("SK5", F % "jp_f_mitsudogu_tate", 755.00, 867.00, 180.0, "the three capture tools on their rack, on the gravel "
     "facing the road", "SK3"),
    ("SK6", r"JP\furniture\bedding\jp_f_mushiro.p3d", 757.60, 866.60, 0.0, "a straw mat on the gravel (where the "
     "traveller knelt)", "SK3"),
    ("SK7", r"JP\furniture\bedding\jp_f_mushiro_torn.p3d", 751.60, 867.00, 0.0, "a torn mat on the gravel", "SK3"),
    ("SK8", r"JP\site\roadside\jp_s_kosatsu_std.p3d", 775.00, 868.40, 180.0, "the notice board outside the Edo-side gate"),
    ("TY3", F % "jp_f_kanme_hakari", 811.60, 857.80, 0.0, "the big steelyard on its tripod, a bale hanging on the hook (the cargo "
     "weight check)"),
    ("TY4", r"JP\site\yard_life\jp_s_stable_yard_tie_post.p3d", 819.40, 860.00, 0.0, "a tie post for the relay horses"),
    ("TY5", r"JP\site\yard_life\jp_s_stable_yard_tie_post.p3d", 822.20, 860.00, 0.0, "a tie post"),
    ("TY6", r"JP\site\yard_life\jp_s_stable_yard_saddle_rack.p3d", 822.80, 856.60, 270.0, "pack saddles on their rack"),
    ("TY7", r"JP\site\street_life\jp_s_kago_down.p3d", 812.40, 860.20, 90.0, "a palanquin set down, waiting"),
    ("TY8", r"JP\site\yard\jp_s_handcart_load_bales.p3d", 819.80, 856.80, 90.0, "a handcart with bales for the relay"),
    ("FB3", r"JP\site\gov_site\jp_s_hinomi_yagura.p3d", 795.50, 856.50, 0.0, "the tall fire watchtower (climb the north "
     "face; the lookout deck at 6.40, the hansho bell)"),
    ("FB4", r"JP\site\street_life\jp_s_fire_watch_rack.p3d", 805.60, 858.80, 270.0, "buckets, a hook and a ladder on "
     "their rack"),
    ("FB5", F % "jp_f_matoi_nobori_fallen", 798.20, 853.00, 90.0, "a second standard knocked down in the yard"),
]
# eaves over a gravel court / a prop on a court, the nagaya-mon in the gap of its own fence line
def floor_seat(key, x, z, yaw, step=0.4):
    """The lowest seat height that keeps the terrain 2 cm under every room floor of the object."""
    r = L1.rec(key)
    rooms = json.load(open(os.path.join(DEV, "buildings", r["model_dir"], "rooms", key + ".json"),
                           encoding="utf-8"))["rooms"]
    need = -99.0
    for rm in rooms:
        x0, x1, z0, z1 = rm["rect_model"]
        n, k = max(1, int((x1 - x0) / step)), max(1, int((z1 - z0) / step))
        for i in range(n + 1):
            for j in range(k + 1):
                wx, wz = LW.to_world(x0 + (x1 - x0) * i / n, z0 + (z1 - z0) * j / k, (x, 25.0, z), yaw)
                need = max(need, T.ground(wx, wz) - rm["level_m"] + 0.02)
    return need


ALLOW = {("SK2", "SK3"), ("SK2", "SK5"), ("SK2", "SK7"), ("SK3", "SK5"), ("SK3", "SK6"), ("SK3", "SK7"), ("JY1", "JY2"),
         ("JY4", "JY5")}
# the lane runs THROUGH the checkpoint's two gates; the gravel court's road-side corner posts stand at the road edge
LANE_OK = {"SK1", "SK3"}
LINE_KINDS = ("gv_cmp_",)


def main():
    rows, pos_xml, items, polys, problems = ["p3d,x,z,yaw_deg,y_offset"], [], [], [], []
    bases = {}
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
        # W3D: no room floor (doma, boards, gate sill pads, gravel courts) may have the terrain through it on the high
        # side of the slope (spikes/W3D/floorcheck.py): seat at least that high; the low side then floats (checked)
        fl = floor_seat(key, x, z, yaw)
        base = max(base, fl)
        if hi - lo > 0.05:
            problems.append("note %s: ground varies %.2f m under it (seated %.2f over its lowest point by its floors)" % (
                bid, hi - lo, base - lo))
        if base - lo > FLOAT_OK.get(key, FLOAT_HUT):
            problems.append("FLOAT %s: %.2f m over its lowest ground" % (bid, base - lo))
        yoff = base - g0
        bases[bid] = base
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
    for ex in EXTRA:
        eid, p3d, x, z, yaw, label = ex[:6]
        dy = ex[6] if len(ex) > 6 else 0.0
        pp = L1.prop_poly(p3d, x, z, yaw)
        if not pp:
            problems.append("NOCAT %s %s (not in the decor catalogue)" % (eid, p3d))
        lo, hi = LW.ground_poly(pp) if pp else (T.ground(x, z), T.ground(x, z))
        if isinstance(dy, str):        # on a gravel court object: its top (0.10 over its seat)
            yoff = bases[dy] + 0.10 - T.ground(x, z)
        else:
            yoff = lo - T.ground(x, z) + dy
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
            if nid.split(".")[0] not in LANE_OK and LW.poly_hit(p, [(a0, c0), (a1, c0), (a1, c1), (a0, c1)]):
                problems.append("LANE %s blocked by %s" % (nm, nid))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) == "W3D.csv":
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
    print("W3D.csv %d rows, %d buildings, %d free objects, %d CE groups; %d problems (+%d notes)" % (
        len(rows) - 1, len(BUILDINGS), len(EXTRA), len(pos_xml), len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
