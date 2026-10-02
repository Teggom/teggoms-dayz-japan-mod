"""W3B render jobs for spikes/W3B/render_w3b_rooms.py: ONE rooms sheet (w3b_rooms.jpg): the main room of every
furnished variant (the room with the most counted props) + the bath room, the doma with the bandai, the dust-free back
room and the show stage."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)

FURNISHED = {
    "f_tr_sento": "Bathhouse (sento)", "f_tr_stablerow": "Stable row", "f_tr_booth_barber": "Barber's booth",
    "f_tr_booth_misemono": "Show booth", "f_tr_ws_joinery": "Joiner", "f_tr_ws_turner": "Woodturner + abacus",
    "f_tr_ws_basket": "Basket maker", "f_tr_ws_polisher": "Sword polisher", "f_tr_ws_lacquer": "Lacquerer",
    "f_tr_ws_kinko": "Fittings maker", "f_tr_timber_saw": "Sawing shed", "f_tr_timber_store": "Timber store",
    "f_tr_timber_shingle": "Shingle shed", "f_tr_foundry": "Foundry",
}
EXTRA_ROOMS = {"f_tr_sento": ["bath", "doma"], "f_tr_ws_lacquer": ["back"], "f_tr_booth_misemono": ["stage"]}

FLIP_X = set()


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
SHEETS = {"rooms": ("W3B furnished rooms + props (wave 3b: bathhouse, stable, booths, workshops, timber yard, foundry)", "", 4, 480, 320, 92, 58)}
