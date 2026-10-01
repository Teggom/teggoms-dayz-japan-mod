"""SH1 showcase layout: the shrine, the graveyard and the life-layer gallery as free map objects
(test/placements/SH1.csv, baked into the terrain by T's build_world.py), checked before writing.

  python spikes/SH1/layout_sh1.py [--force]

Writes test/placements/SH1.csv, spikes/SH1/showcase_items.json (every object with its ID, label, class, world
position; the overhead maps and SHOWCASE_MAP.md read it). Checks (exit 1 on a problem unless --force): footprints
clear of each other (stairs, the torii spanning them and things deliberately set on a host excepted), of every placed
building's walls, door aprons and site objects (spikes/C3/dress_island.py helpers), of the other drop-ins and of
T's trees (trunks), and every class resolves to a p3d on P:.
"""
import csv
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE, os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"),
          os.path.join(DEV, "spikes", "B_building", "kit"), os.path.join(DEV, "spikes", "C3")):
    if p not in sys.path:
        sys.path.insert(0, p)
import terrain_sh1 as T  # noqa: E402
import shrine  # noqa: E402
from jpparts import decor as DC  # noqa: E402

OUT = os.path.join(DEV, "test", "placements", "SH1.csv")
ITEMS = os.path.join(HERE, "showcase_items.json")
VANILLA = {"t_fagussylvatica_3f": r"dz\plants\tree\t_fagussylvatica_3f.p3d",
           "t_quercusrobur_2f": r"dz\plants\tree\t_quercusrobur_2f.p3d"}


def areas():
    """[(area, [(id, name, x, z, yaw, y, label, extra)])]"""
    out = []
    objs, info = shrine.layout()
    out.append(("shrine", objs, info))
    try:
        import graveyard
        g, ginfo = graveyard.layout()
        out.append(("graveyard", g, ginfo))
    except ImportError:
        pass
    try:
        import gallery
        g, ginfo = gallery.layout()
        out.append(("gallery", g, ginfo))
    except ImportError:
        pass
    return out


def resolve(name):
    if name.startswith("@"):                     # a registry building (placed through buildings/registry.py)
        return None, None
    cat = DC.catalog()
    if name in cat:
        e = cat[name]
        return e["p3d"].lstrip("\\"), e
    if name in VANILLA:
        return VANILLA[name], None
    raise KeyError(name)


def half_sizes(e, yaw):
    if e is None:
        return 0.4, 0.4
    b = e["bbox"]
    return max(abs(b[0]), abs(b[1])), max(abs(b[4]), abs(b[5]))


def fp_box(e, x, z, yaw, pad=0.0):
    if e is None:
        return (x - 0.4, x + 0.4, z - 0.4, z + 0.4)
    it = {"name": e["name"], "info": e, "x": x, "y": 0.0, "z": z, "yaw": yaw}
    fp = DC.footprint(it)
    if not fp:
        b = e["bbox"]
        pts = [DC.to_model(it, (xx, 0.0, zz)) for xx in (b[0], b[1]) for zz in (b[4], b[5])]
        fp = [(p[0], p[2]) for p in pts]
    xs, zs = [p[0] for p in fp], [p[1] for p in fp]
    return (min(xs) - pad, max(xs) + pad, min(zs) - pad, max(zs) + pad)


def overlap(a, b, gap=0.0):
    return a[0] < b[1] + gap and a[1] > b[0] - gap and a[2] < b[3] + gap and a[3] > b[2] - gap


def group_of(oid, extra):
    if extra.get("grp"):
        return extra["grp"]
    if oid[0] in "KI" and oid[1:3].isdigit():
        return "stair" + oid[0]
    return None


def main(argv):
    rows = ["p3d,x,z,yaw_deg,y_offset"]
    items = []
    probs = []
    allobjs = []
    stair_info = {}
    for area, objs, info in areas():
        if area == "shrine":
            stair_info = info
        if info.get("problems"):
            probs += [(area, p) for p in info["problems"]]
        for (oid, name, x, z, yaw, y, label, extra) in objs:
            p3d, e = resolve(name)
            if p3d is None:
                items.append({"id": oid, "area": area, "name": name[1:], "class": "Land_JP_Shed_Open_Board",
                              "p3d": "JP\\buildings\\shed\\jp_shed_open_board.p3d", "x": x, "z": z, "yaw": yaw,
                              "y_offset": 0.0, "ground": round(T.ground(x, z), 3), "label": label, "registry": True})
                continue
            if not os.path.isfile(os.path.join("P:\\", p3d)):
                probs.append((oid, "p3d missing on P: " + p3d))
            if y is None:
                hw, hd = half_sizes(e, yaw)
                y, rise = T.seat(x, z, hw, hd, yaw)
            g = T.ground(x, z)
            rows.append("%s,%.3f,%.3f,%.1f,%.3f" % (p3d, x, z, yaw % 360.0, y))
            cls = e["cls"] if e else None
            items.append({"id": oid, "area": area, "name": name, "class": cls, "p3d": p3d, "x": round(x, 3),
                          "z": round(z, 3), "yaw": round(yaw % 360.0, 1), "y_offset": round(y, 3),
                          "ground": round(g, 3), "label": label, **{k: v for k, v in extra.items() if k != "grp"}})
            allobjs.append((oid, area, name, e, x, z, yaw, group_of(oid, extra), extra))
    # ---- checks -------------------------------------------------------------------------------------------
    import dress_island as DI
    bb = DI.building_boxes()
    boxes = []
    for oid, area, name, e, x, z, yaw, grp, extra in allobjs:
        geo = e is None or e["geo"]
        boxes.append((oid, name, fp_box(e, x, z, yaw), geo, grp, extra))
    for oid, name, box, geo, grp, extra in boxes:
        if extra.get("host"):
            continue                                  # set on / in a host on purpose (checked by the gallery itself)
        for key, wb, aprons, sboxes in bb:
            if extra.get("in_building") == key:
                continue
            if overlap(box, wb, 0.10):
                probs.append((oid, name, "into building " + key))
            if geo:
                for a in aprons:
                    if overlap(box, a):
                        probs.append((oid, name, "door apron of " + key))
            for sn, sb in sboxes:
                if overlap(box, sb, 0.05):
                    probs.append((oid, name, "site object %s of %s" % (sn, key)))
    for i in range(len(boxes)):
        a = boxes[i]
        if a[5].get("host") or not a[3]:
            continue
        for j in range(i + 1, len(boxes)):
            b = boxes[j]
            if b[5].get("host") or not b[3]:
                continue
            if a[4] and a[4] == b[4] and a[4] != "acc":
                continue
            ga, gb = a[4] or "", b[4] or ""
            if ("over:" in ga and ga[5:] == gb) or ("over:" in gb and gb[5:] == ga):
                continue
            if overlap(a[2], b[2], 0.05):
                probs.append((a[0], a[1], "overlaps %s %s" % (b[0], b[1])))
    others = []
    for p in glob.glob(os.path.join(DEV, "test", "placements", "*.csv")):
        if os.path.basename(p) in ("SH1.csv", "C.csv"):
            continue
        for r in csv.DictReader(open(p)):
            others.append((os.path.basename(p) + ":" + os.path.basename(r["p3d"]), float(r["x"]), float(r["z"])))
    for p in glob.glob(os.path.join(DEV, "test", "spawns", "*.json")):
        for o in json.load(open(p)).get("Objects", []):
            others.append((os.path.basename(p) + ":" + o["name"], o["pos"][0], o["pos"][2]))
    for oid, name, box, geo, grp, extra in boxes:
        for on, ox, oz in others:
            if box[0] - 1.0 < ox < box[1] + 1.0 and box[2] - 1.0 < oz < box[3] + 1.0:
                probs.append((oid, name, "near " + on))
    tr = T.trees()
    for oid, name, box, geo, grp, extra in boxes:
        if name.startswith("t_"):
            continue
        for tx, tz, ty, ts in tr:
            if box[0] - 0.9 < tx < box[1] + 0.9 and box[2] - 0.9 < tz < box[3] + 0.9:
                probs.append((oid, name, "tree trunk at (%.1f, %.1f)" % (tx, tz)))
    for k, (mods, worst) in stair_info.items():
        print("stair %s: %d modules, z %.1f -> %.1f, top %.2f m ASL; worst float %.3f, poke %.3f, first-riser sink %.3f"
              % (k, len(mods), mods[0][2], mods[-1][2] + mods[-1][5], mods[-1][3], worst["float"], worst["poke"],
                 worst.get("foot", 0.0)))
    n_area = {}
    for it in items:
        n_area[it["area"]] = n_area.get(it["area"], 0) + 1
    print("objects:", n_area, "total", len(items))
    for p in probs:
        print("PROBLEM", p)
    if probs and "--force" not in argv:
        return 1
    with open(OUT, "wb") as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    with open(ITEMS, "wb") as f:
        f.write(json.dumps(items, indent=1, ensure_ascii=False).encode("utf-8"))
    print("wrote", OUT, "and", ITEMS)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
