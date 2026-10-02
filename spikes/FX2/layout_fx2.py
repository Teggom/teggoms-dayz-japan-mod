"""FX2 layout: the komainu / kitsune pairs and the new lantern pair -> test/placements/FX2.csv, spikes/FX2/fx2_items.json,
the FX2 section of spikes/SH1/SHOWCASE_MAP.md and research/production/contact_sheets/fx2_map_guardians.jpg.

  python spikes/FX2/layout_fx2.py

Pair rule (research/statues/NOTES.md): facing the shrine, the 'a' (open mouth) on the right, the 'un' on the left;
both face down the approach, toed in 15 deg (yaw 180 + 15 on the east side, 180 - 15 on the west for a north-facing
shrine). Each pair is symmetric about its approach axis (mirror x about the axis, same z, same model family); the
precinct layout itself stays asymmetric. Bases seat on the lowest ground under the footprint (5 cm burial in the model).
Checks as layout_w2f: overlaps between FX2 items, clashes (< 0.3 m) with every other placement CSV point, buildings,
trees, reserved spots.
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
import layout_w2f as LW  # noqa: E402

CSV_OUT = os.path.join(DEV, "test", "placements", "FX2.csv")
ITEMS = os.path.join(HERE, "fx2_items.json")
MD = os.path.join(DEV, "spikes", "SH1", "SHOWCASE_MAP.md")
MAP = os.path.join(DEV, "research", "production", "contact_sheets", "fx2_map_guardians.jpg")
A_, B_ = "<!-- FX2 BEGIN -->", "<!-- FX2 END -->"


def pair(code, name_l, name_r, ax, z, half, yaw_axis=180.0, toe=15.0, what=""):
    """A pair about the approach axis x = ax (the shrine to the north, yaw_axis 180 = facing south down the
    approach): left (west) and right (east) as one faces the shrine."""
    return [(code + "a", name_l, ax - half, z, yaw_axis - toe, what + " (west / left, facing the shrine)"),
            (code + "b", name_r, ax + half, z, yaw_axis + toe, what + " (east / right)")]


ITEMS_DEF = (
    # town shrine P (Hachimangu): the compact Edo pair at the ichi-no-torii, the upright pair inside the ni-no-torii
    pair("FX-P1", "jp_s_komainu_b_un", "jp_s_komainu_b_a", 1024.0, 1102.1, 2.55,
         what="komainu pair, compact Edo form, just inside the ichi-no-torii S01")
    + pair("FX-P2", "jp_s_komainu_a_un", "jp_s_komainu_a_a", 1024.0, 1138.9, 2.70,
           what="komainu pair, upright form (un with horn), inside the ni-no-torii S14")
    # village shrine V: the mossy pair just outside its torii V3
    + pair("FX-V1", "jp_s_komainu_a_un_moss", "jp_s_komainu_a_a_moss", 945.0, 1059.5, 2.20,
           what="komainu pair, upright form, mossy (old village shrine), outside the torii V3")
    # Inari corner: the fox pair at the foot of the Inari stair (torii S80), a lantern pair below them
    + pair("FX-I1", "jp_s_kitsune_key", "jp_s_kitsune_jewel", 1058.0, 1223.9, 1.80,
           what="Inari fox pair (key / jewel), below the vermilion torii S80")
    + [("FX-I2a", "jp_s_stone_lantern_kasuga_18_moss", 1056.0, 1221.4, 90.0,
        "lantern pair on the Inari path, Kasuga 1.8 mossy (west)"),
       ("FX-I2b", "jp_s_stone_lantern_kasuga_18_moss", 1060.0, 1221.4, 270.0, "lantern pair on the Inari path (east)")]
)


def main():
    cat = DC.catalog()
    rows, items, polys, problems = ["p3d,x,z,yaw_deg,y_offset"], [], [], []
    for eid, name, x, z, yaw, label in ITEMS_DEF:
        inf = cat[name]
        poly = LW.corners(inf["bbox"], (x, 25.0, z), yaw)
        lo, hi = LW.ground_poly(poly)
        yoff = lo - T.ground(x, z)
        rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (inf["p3d"].lstrip("\\"), x, z, yaw, yoff))
        items.append({"id": eid, "class": inf["cls"], "p3d": inf["p3d"].lstrip("\\"), "x": x, "z": z, "yaw": yaw,
                      "y_off": round(yoff, 3), "label": label, "area": eid.split("-")[1][0]})
        polys.append((eid, poly))
        if hi - lo > 0.25:
            problems.append("note %s: ground falls %.2f m across the footprint (seated on the low side)" % (eid, hi - lo))
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            if LW.poly_hit(polys[i][1], polys[j][1]):
                problems.append("OVERLAP %s x %s" % (polys[i][0], polys[j][0]))
    for name, poly in LW.other_buildings():
        for nid, p in polys:
            if LW.poly_hit(poly, p):
                problems.append("OVERLAP %s x building %s" % (nid, name))
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) == "FX2.csv":
            continue
        with open(p, newline="") as f:
            for row in csv.DictReader(f):
                if os.path.basename(p) == "C.csv" and "\\buildings\\" in row["p3d"].lower():
                    continue
                for nid, poly in polys:
                    if DC.point_poly_dist((float(row["x"]), float(row["z"])), poly) < 0.3:
                        problems.append("CLASH %s with %s %s" % (nid, os.path.basename(p), os.path.basename(row["p3d"])))
    for t in T.trees():
        for nid, poly in polys:
            if DC.point_poly_dist((float(t[0]), float(t[1])), poly) < 0.8:
                problems.append("TREE in %s" % nid)
    for nm, (a0, a1, c0, c1) in LW.RESERVED.items():
        for nid, p in polys:
            if LW.poly_hit(p, [(a0, c0), (a1, c0), (a1, c1), (a0, c1)]):
                problems.append("RESERVED %s in %s" % (nid, nm))
    with open(CSV_OUT, "wb") as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    with open(ITEMS, "wb") as f:
        f.write(json.dumps(items, indent=1, ensure_ascii=False).encode("utf-8"))
    write_md(items)
    draw_map(items)
    hard = [p for p in problems if not p.startswith("note")]
    for p in problems:
        print(p)
    print("FX2.csv %d rows; %d problems (+%d notes)" % (len(rows) - 1, len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


AREAS = [("P", "Town shrine approach (map fx2_map_guardians.jpg, panel P; with SH1 S01-S32)"),
         ("V", "Village shrine (panel V; with W2F V1-V5)"),
         ("I", "Inari corner (panel I; with SH1 S80-S85, I01-I16)")]


def write_md(items):
    out = [A_, "", "## FX2: komainu, kitsune and lantern pairs (agent FX2, 2026-10-01)", "",
           "Regenerate: `python spikes/FX2/layout_fx2.py`. Pairs are symmetric about their approach axis: the 'a' "
           "(open mouth) on the right and the 'un' on the left as one faces the shrine, toed in 15 deg. Every lantern "
           "on the SH1 / W2F approaches already stood in a mirrored pair (S04/S05 ... S29/S30, S92-S95, V4/V5, T6/T7, "
           "U6/U7); the Inari path had none: FX-I2 adds one.", ""]
    for code, title in AREAS:
        out += ["### %s" % title, "", "| ID | Class | x | z | yaw | y_off | What |", "|---|---|---|---|---|---|---|"]
        for it in items:
            if it["area"] == code:
                out.append("| %s | `%s` | %.2f | %.2f | %.0f | %.2f | %s |" % (it["id"], it["class"], it["x"], it["z"],
                                                                             it["yaw"], it["y_off"], it["label"]))
        out.append("")
    out.append(B_)
    with open(MD, "rb") as f:
        s = f.read().decode("utf-8")
    block = "\n".join(out)
    if A_ in s:
        s = s[:s.index(A_)] + block + s[s.index(B_) + len(B_):]
    else:
        s = s.rstrip("\n") + "\n\n" + block + "\n"
    with open(MD, "wb") as f:
        f.write(s.encode("utf-8"))


def draw_map(items):
    """Three top-down panels: every placement point of every CSV (grey, with SH1 / W2F IDs where known) and the FX2
    items (red = komainu / kitsune, orange = lanterns) with their IDs."""
    from PIL import Image, ImageDraw
    pts = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) == "FX2.csv":
            continue
        with open(p, newline="") as f:
            for row in csv.DictReader(f):
                pts.append((float(row["x"]), float(row["z"]), os.path.basename(row["p3d"])))
    ids = {}
    with open(MD, "rb") as f:
        for ln in f.read().decode("utf-8").splitlines():
            c = [q.strip() for q in ln.split("|")]
            if len(c) > 5 and c[1] and not c[1].startswith(("ID", "---", "FX-")):
                try:
                    ids[(round(float(c[3]), 1), round(float(c[4]), 1))] = c[1]
                except ValueError:
                    pass
    panels = [("P", "P: town shrine approach", (1012.0, 1036.0, 1096.0, 1146.0)),
              ("V", "V: village shrine", (936.0, 954.0, 1055.0, 1082.0)),
              ("I", "I: Inari corner", (1048.0, 1068.0, 1216.0, 1246.0))]
    W, H = 560, 1000
    S = Image.new("RGB", (W * 3 + 40, H + 60), (245, 243, 236))
    d = ImageDraw.Draw(S)
    d.text((10, 8), "FX2 guardian pairs (red: komainu / kitsune, orange: new lanterns; grey: existing placements with "
                    "their SHOWCASE_MAP IDs). North up.", fill=(0, 0, 0))
    for k, (code, title, (x0, x1, z0, z1)) in enumerate(panels):
        ox = 10 + k * (W + 10)
        sc = min((W - 20) / (x1 - x0), (H - 40) / (z1 - z0))
        d.rectangle([ox, 40, ox + W, 40 + H], outline=(120, 120, 120))
        d.text((ox + 6, 44), title, fill=(0, 0, 0))

        def P(x, z):
            return ox + 10 + (x - x0) * sc, 40 + H - 10 - (z - z0) * sc
        for x, z, nm in pts:
            if x0 <= x <= x1 and z0 <= z <= z1:
                u, v = P(x, z)
                d.ellipse([u - 3, v - 3, u + 3, v + 3], fill=(150, 150, 150))
                lab = ids.get((round(x, 1), round(z, 1)))
                if lab:
                    d.text((u + 4, v - 6), lab, fill=(110, 110, 110))
        for it in items:
            if it["area"] != code:
                continue
            u, v = P(it["x"], it["z"])
            col = (210, 40, 30) if "lantern" not in it["class"].lower() else (230, 140, 20)
            d.rectangle([u - 6, v - 6, u + 6, v + 6], fill=col)
            d.text((u + 8, v - 6), it["id"], fill=col)
    os.makedirs(os.path.dirname(MAP), exist_ok=True)
    S.save(MAP, quality=88)


if __name__ == "__main__":
    sys.exit(main())
