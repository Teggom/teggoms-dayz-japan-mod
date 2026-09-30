"""Summary of the C3 buildings: checks (from buildings/<dir>/checks/<key>.json), faces, and for furnished variants the
counted props, life items and loot (floor / raised) per room, rebuilt from the recipe.
  python spikes/C3/summary.py [--markdown]
"""
import json
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    sys.path.insert(0, p)
import registry  # noqa: E402
import pipeline  # noqa: E402


def main():
    md = "--markdown" in sys.argv
    tot_n = tot_f = 0
    rows = []
    for b in registry.C3_KURA + registry.C3_FURNISHED:
        p = os.path.join(DEV, "buildings", b["dir"], "checks", b["key"] + ".json")
        c = json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else {}
        n, f = c.get("checks_n", 0), c.get("failures", -1)
        tot_n += n
        tot_f += max(f, 0)
        line = "%-34s %-44s checks %3d fail %d faces %s budget %s" % (b["key"], b["class"], n, f, c.get("faces"),
                                                                        b["budget"])
        rows.append(line)
        if b["dir"] != "furnished":
            continue
        mod = pipeline.load_module(b)
        M, floors, rooms = mod.model(name=b["name"], **b["params"])
        pts = mod.loot_points(floors)
        by = mod.D.by_room()
        for r in rooms:
            its = by.get(r["name"], [])
            cnt = sum(1 for i in its if i["count"])
            life = sum(1 for i in its if not i["count"])
            fl = sum(1 for q in pts if q["floor"] == r["name"] and q["container"] == "lootFloor")
            rs = sum(1 for q in pts if q["floor"] == r["name"] and q["container"] == "lootshelves")
            rows.append("    %-12s %-14s props %d + life %d  loot floor %d raised %d" % (r["name"], r["tag"], cnt, life,
                                                                                      fl, rs))
        rows.append("    street / yard objects: %d; street-front proxies: %d" % (
            len(mod.D.site), sum(1 for i in mod.D.items if i["room"] == "street")))
    rows.append("TOTAL %d checks, %d failures" % (tot_n, tot_f))
    print("\n".join(rows))


if __name__ == "__main__":
    main()
