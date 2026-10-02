"""W3D render jobs for spikes/W3D/render_w3d_rooms.py: ONE rooms sheet (w3d_rooms.jpg): the furnished government halls
and the shells each site reuses (the guardhouse with its inspection room, the foot-soldiers' guardhouse, the post-station
office, the jinya office + court room + rice kura + gatehouse, the cell block, the fire brigade's tool shed). The new
props are on the family sheet (w3d_family.jpg). Copied from spikes/W3C2/w3c2_jobs.py."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)

FURNISHED = {
    "f_gv_bansho": "Checkpoint guardhouse", "f_gv_bunk_ashigaru": "Foot-soldiers' guardhouse",
    "f_gv_toiyaba": "Post-station office", "f_gv_jinya": "Jinya office", "f_gv_ginmisho": "Court room",
    "f_gv_kura_nengu": "Tax-rice kura", "f_gv_nagayamon_jinya": "Jinya gatehouse", "f_gv_roya": "Cell block",
    "f_gv_hikeshi": "Fire brigade tool shed",
}
ROOMS = {"f_gv_bansho": ["hall", "office", "doma"], "f_gv_bunk_ashigaru": ["living", "doma"],
         "f_gv_toiyaba": ["choba", "doma"], "f_gv_jinya": ["chanoma", "tsugi"], "f_gv_ginmisho": ["hall", "office"],
         "f_gv_kura_nengu": ["kura"], "f_gv_nagayamon_jinya": ["room"], "f_gv_roya": ["corridor", "cell_a", "cell_b"],
         "f_gv_hikeshi": ["floor"]}
CAMS = {}


def _view(key, title, r, its, far=False):
    x0, x1, z0, z1 = r["rect_model"]
    y = r["level_m"]
    names = ", ".join(sorted({i["name"].replace("jp_f_", "") for i in its}))
    n = sum(1 for i in its if i["count"])
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    mx = sum(i["x"] for i in its) / len(its) if its else cx
    mz = sum(i["z"] for i in its) / len(its) if its else cz
    ex = x0 + 0.25 if mx > cx else x1 - 0.25
    ez = z0 + 0.25 if mz > cz else z1 - 0.25
    lx = x1 - 0.4 if ex < cx else x0 + 0.4
    lz = z1 - 0.4 if ez < cz else z0 + 0.4
    return ("rm_%s_%s" % (key, r["name"]), "%s | %s (%s), %d props: %s" % (title, r["name"], r["tag"], n, names),
            {"key": key, "cam": [ex, y + (2.2 if far else 1.62), ez], "look": [lx, y + 0.55, lz], "lens": 12,
             "site": False, "res": [960, 640]})


def _rooms():
    import registry
    import pipeline
    out = []
    for key, title in FURNISHED.items():
        b = registry.get(key)
        mod = pipeline.load_module(b)
        M, floors, rooms = mod.model(name=b["name"], **b["params"])
        by = mod.D.by_room()
        rd = {r["name"]: r for r in rooms}
        for rn in ROOMS[key]:
            if rn in rd:
                j = _view(key, title, rd[rn], by.get(rn, []), far=(rn == "kura"))
                if (key, rn) in CAMS:
                    j[2]["cam"], j[2]["look"] = CAMS[(key, rn)]
                out.append(j)
    return out


class _Lazy(dict):
    def __missing__(self, k):
        if k == "rooms":
            self["rooms"] = _rooms()
            return self[k]
        raise KeyError(k)


JOBS = _Lazy()
JOBS_ALL = ("rooms",)
SHEETS = {"rooms": ("W3D furnished government halls and the reused shells (checkpoint, post-station office, jinya, jail, "
                    "fire brigade)", "", 4, 480, 320, 92, 58)}
