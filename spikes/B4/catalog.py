"""Compact listing of every B3a / B3b prop model (from the .prop.json sidecars), for choosing the pilot's set.
python spikes/B4/catalog.py [furniture|site] [filter]"""
import glob, json, os, sys
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def load(area):
    out = []
    for p in sorted(glob.glob(os.path.join(DEV, "src", "JP", area, "*", "*.prop.json"))):
        with open(p, "rb") as f:
            d = json.loads(f.read().decode("utf-8"))
        for m in d["models"]:
            m = dict(m)
            m["_id"] = d["id"]
            m["_cat"] = d.get("category", "")
            out.append(m)
    return out


if __name__ == "__main__":
    area = sys.argv[1] if len(sys.argv) > 1 else "furniture"
    flt = sys.argv[2] if len(sys.argv) > 2 else ""
    for m in load(area):
        name = os.path.basename(m["p3d"])[:-4]
        if flt and flt not in name:
            continue
        bb = m.get("bbox")
        ls = ";".join("%s y%.2f n%d" % (s.get("name", "?"), s["y"], len(s.get("points", []))) for s in m.get("loot_surfaces", []))
        extra = {k: m[k] for k in ("anchor", "wall_gap", "hang_y", "front_zone_m", "roadway") if k in m}
        print("%-40s %-9s coll=%-5s bb=%s fp=%s %s | %s" % (
            name, m.get("state", ""), m.get("collision", m.get("collision_lods")),
            [round(v, 2) for v in bb] if bb else None,
            [round(v, 2) for v in m.get("footprint_xz") or []] if m.get("footprint_xz") else m.get("footprint"),
            extra, ls))
