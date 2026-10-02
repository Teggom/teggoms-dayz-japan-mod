"""W3C1 render jobs for spikes/W3C1/render_w3c1_rooms.py: ONE rooms sheet (w3c1_rooms.jpg): the rooms of every furnished
variant that show the trade (the brewing floor, the press bay, the starter loft, the steaming hearth, the koji room,
the brewers' rest room, the polishing shed, the cask kura, the brewer's shop, the mill floor with the stamps, the
dyer's vat room and shop, the paper workshop) + the new machinery props as pre-rendered rows (render_w3c1_props.py)."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)

FURNISHED = {
    "f_ts_okura": "Brewery o-kura", "f_ts_maegura": "Brewery mae-gura", "f_ts_seimai": "Rice-polishing shed",
    "f_ts_kura_casks": "Cask kura", "f_ts_sakaya": "Brewer's shop", "f_ts_suisha": "Water mill",
    "f_ts_konya": "Indigo dyer", "f_ts_kamisuki": "Paper mill",
}
# rooms to show per variant (the first is the main view); every other variant shows its fullest room
ROOMS = {"f_ts_okura": ["kura", "moto", "loft"], "f_ts_maegura": ["kama", "muro", "kaisho"], "f_ts_konya": ["aiba", "mise"],
         "f_ts_kura_casks": ["kura"], "f_ts_sakaya": ["doma"], "f_ts_seimai": ["floor"], "f_ts_suisha": ["floor"],
         "f_ts_kamisuki": ["floor"]}
# explicit cameras (model frame) where the corner rule lands inside a prop
CAMS = {("f_ts_okura", "kura"): ([7.70, 2.70, 0.40], [-1.80, 0.90, -0.60])}
PROP_TILES = [("jp_f_fune_press", "Lever press (fune + beam + stones): slack | down"),
              ("jp_f_kamaba", "Steaming hearth (kamado, cauldron, koshiki): cold | toppled"),
              ("jp_f_shikomi_oke", "Big fermentation tubs: lid half on | ladder | staved"),
              ("jp_f_karausu", "Foot-treadle rice mortar: intact | lever off"),
              ("jp_f_koji_toko", "Koji bed: cloth on | dragged off"), ("jp_f_sakabayashi", "Sugidama (brown, autumn)"),
              ("jp_f_hatcho_oke", "Hatcho miso vat: stone cone | tumbled"),
              ("jp_f_monohoshi", "Dyer's drying frame: hung | torn"),
              ("jp_f_sukibune", "Paper vat with mould + spring pole: intact | broken"),
              ("jp_f_hoshiita_rack", "Paper drying boards: leaned | fallen"),
              ("jp_f_akumizu", "Lye drip tubs: intact | knocked off"), ("jp_f_sukumo_bales", "Sukumo bales")]


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
    ren = os.path.join(HERE, "renders")
    for pid, cap in PROP_TILES:
        src = os.path.join(ren, pid + "_row.png")
        if os.path.isfile(src):
            shutil.copyfile(src, os.path.join(ren, "pr_%s.png" % pid))
            out.append(("pr_%s" % pid, "prop: " + cap, {"skip": True}))
    return out


class _Lazy(dict):
    def __missing__(self, k):
        if k == "rooms":
            self["rooms"] = _rooms()
            return self[k]
        raise KeyError(k)


JOBS = _Lazy()
JOBS_ALL = ("rooms",)
SHEETS = {"rooms": ("W3C1 furnished rooms + the new machinery (wave 3c-1: sake brewery, water mill, dyer, paper mill)",
                    "", 4, 480, 320, 92, 58)}
