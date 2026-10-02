"""W3C2 render jobs for spikes/W3C2/render_w3c2_rooms.py: ONE rooms sheet (w3c2_rooms.jpg): the furnished huts and
sheds of every site (charcoal hut, potter, tile moulding + drying, lime, quarry, sorting shed, the two bunk halls, the
salt-boiling hut) + the new props as pre-rendered rows (render_w3c2_props.py). Copied from spikes/W3C1/w3c1_jobs.py."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)

FURNISHED = {
    "f_rs_sumiyaki": "Charcoal burner's hut", "f_rs_toki": "Potter's work shed", "f_rs_kawara": "Tile moulding shed",
    "f_rs_kawara_dry": "Tile drying shed", "f_rs_ishibai": "Lime slaking shed", "f_rs_ishiku": "Quarrymen's shed",
    "f_rs_senko": "Mine sorting shed", "f_rs_bunk_miners": "Miners' bunk hall", "f_rs_bunk_loggers": "Loggers' bunk hall",
    "f_rs_kamaya": "Salt-boiling hut",
}
ROOMS = {"f_rs_sumiyaki": ["doma", "living"], "f_rs_toki": ["doma"], "f_rs_kawara": ["doma"], "f_rs_kawara_dry": ["floor"],
         "f_rs_ishibai": ["floor"], "f_rs_ishiku": ["floor"], "f_rs_senko": ["floor"], "f_rs_bunk_miners": ["living", "doma"],
         "f_rs_bunk_loggers": ["doma"], "f_rs_kamaya": ["floor"]}
CAMS = {}
PROP_TILES = [("jp_f_keri_rokuro", "Kick wheel: dry jar on the head | head knocked off"),
              ("jp_f_ware_rack", "Ware-drying rack: bowls | top plank fallen"),
              ("jp_f_neri_ban", "Wedging board + clay heap"), ("jp_f_kiln_shelves", "Kiln shelves and props"),
              ("jp_f_kawara_rack", "Green-tile rack: full | collapsed"),
              ("jp_f_kawara_stack", "Fired tiles on a pallet: stacked | pushed over"),
              ("jp_f_kawara_bench", "Tile moulding bench + half-carved onigawara"),
              ("jp_f_ishi_shura", "Stone sledge on rollers: lashed | slid off"),
              ("jp_f_ishi_blocks", "Cut blocks: wedge holes, the lord's mark"),
              ("jp_f_spoil_heap", "Mine spoil heap"), ("jp_f_limestone_heap", "Limestone heap"),
              ("jp_f_senko_dai", "Ore sorting bench"), ("jp_f_nekonagashi", "Gold-washing sluice, dry"),
              ("jp_f_makiage", "Windlass over a boarded shaft"),
              ("jp_f_zaru_tori", "Salt sieve stand (zaru-tori): set | tipped"),
              ("jp_f_shio_zaru", "Salt draining baskets"), ("jp_f_matsuba", "Pine-needle fuel heap")]


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
SHEETS = {"rooms": ("W3C2 furnished huts / sheds + the new props (wave 3c-2: kilns, quarry, lime, charcoal, mine, logging, salt)",
                    "", 4, 480, 320, 92, 58)}
