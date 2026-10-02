"""D3 render jobs for spikes/D3/render_d3_rooms.py: ONE rooms sheet (d3_rooms.jpg): the main room of every furnished
variant (the room with the most counted props) + the status rooms (tokonoma, jodan-no-ma, the tea room)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)

FURNISHED = {
    "f_dw_mountain": "Mountain house", "f_dw_coastal": "Coastal house", "f_dw_kumi": "Foot-soldier row",
    "f_dw_doshin": "Doshin house", "f_dw_samurai_m": "Samurai mansion (M)", "f_dw_merchant": "Merchant residence",
    "f_dw_honjin_omote": "Honjin omote", "f_dw_honjin_oku": "Honjin oku", "f_dw_wakihonjin": "Waki-honjin",
    "f_dw_headman_east": "Kanto headman", "f_dw_headman_kinai": "Kinai headman", "f_dw_chashitsu": "Tea hut",
    "f_dw_itagura": "Board storehouse", "f_dw_stable": "Stable", "f_dw_furoba": "Bath hut",
    "f_dw_nagayamon": "Samurai nagaya-mon",
}
EXTRA_ROOMS = {"f_dw_samurai_m": ["zashiki"], "f_dw_honjin_omote": ["jodan_no_ma"], "f_dw_wakihonjin": ["jodan_no_ma"],
               "f_dw_mountain": ["doma"], "f_dw_chashitsu": ["chashitsu"], "f_dw_merchant": ["doma"]}

FLIP_X = {("f_dw_samurai_m", "zashiki"), ("f_dw_honjin_omote", "jodan_no_ma"), ("f_dw_wakihonjin", "jodan_no_ma")}


def _view(key, title, r, its):
    x0, x1, z0, z1 = r["rect_model"]
    y = r["level_m"]
    names = ", ".join(sorted({i["name"].replace("jp_f_", "") for i in its}))
    n = sum(1 for i in its if i["count"])
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    mx = sum(i["x"] for i in its) / len(its) if its else cx
    mz = sum(i["z"] for i in its) / len(its) if its else cz
    ex = x0 + 0.25 if mx > cx else x1 - 0.25
    ez = z0 + 0.25 if mz > cz else z1 - 0.25
    if (key, r["name"]) in FLIP_X:          # the default corner is inside the tokonoma: look AT it instead
        ex = x0 + 0.25 if ex > cx else x1 - 0.25
    lx = x1 - 0.4 if ex < cx else x0 + 0.4
    lz = z1 - 0.4 if ez < cz else z0 + 0.4
    return ("rm_%s_%s" % (key, r["name"]), "%s | %s (%s), %d props: %s" % (title, r["name"], r["tag"], n, names),
            {"key": key, "cam": [ex, y + 1.62, ez], "look": [lx, y + 0.55, lz], "lens": 12, "site": False,
             "res": [960, 640]})


def _rooms():
    import registry
    import pipeline
    out = []
    for key, title in FURNISHED.items():
        b = registry.get(key)
        mod = pipeline.load_module(b)
        M, floors, rooms = mod.model(name=b["name"], **b["params"])
        by = mod.D.by_room()
        cand = [r for r in rooms if not r.get("sparse") and r["tag"] != "doma"] or             [r for r in rooms if not r.get("sparse")] or rooms
        best = max(cand, key=lambda r: sum(1 for i in by.get(r["name"], []) if i["count"]))
        picks = [best] + [r for r in rooms if r["name"] in EXTRA_ROOMS.get(key, ()) and r is not best]
        for r in picks:
            out.append(_view(key, title, r, by.get(r["name"], [])))
    return out


class _Lazy(dict):
    def __missing__(self, k):
        if k == "rooms":
            self["rooms"] = _rooms()
            return self[k]
        raise KeyError(k)


JOBS = _Lazy()
JOBS_ALL = ("rooms",)
SHEETS = {"rooms": ("D3 furnished rooms (wave 3a: dwellings, honjin, outbuildings)", "", 4, 480, 320, 92, 58)}
