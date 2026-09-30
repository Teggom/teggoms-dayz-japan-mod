"""C3 render jobs (spikes/C3/render_c3.py): (out, caption, spec) per sheet; cameras in the MODEL frame of the key
(x, y up, z = front), or scene frame (world - the scene origin) for 'street' / 'hamlet'. Room views and loot plans are
generated from each furnished variant's rooms (one wide view per room from a corner, a plan per floor level)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    if p not in sys.path:
        sys.path.insert(0, p)

K = "Kura (DW22, 3 x 2 ken, two floors): "
KURA = [
    ("kura_namako_3q", K + "Land_JP_Kura_Namako: diagonal namako on the front and gables, plastered eave bands and "
     "soffit, the door with its stepped surround, static open plaster leaves and tile pent, stone landing + step.",
     {"key": "kura_namako", "view": "3q"}),
    ("kura_namako_back", K + "Land_JP_Kura_Namako from the back: plain plaster with a grime band, the small ground "
     "window, the gable window and vent upstairs.", {"key": "kura_namako", "view": "back"}),
    ("kura_kuro_3q", K + "Land_JP_Kura_Kuro_Hinged: black lapped boards (shitami) on the lower walls, the plaster "
     "door leaves as ROTATION doors (engine test), hinged window shutters.", {"key": "kura_kuro_hinged", "view": "3q"}),
    ("kura_kuro_shut", K + "Land_JP_Kura_Kuro_Hinged with every door shut (outer leaves closed over the doorway).",
     {"key": "kura_kuro_hinged", "cam": [3.6, 1.7, 6.8], "look": [0.0, 1.8, 1.8], "lens": 22, "open": 0.0,
      "fill": False}),
    ("kura_plain_3q", K + "Land_JP_Kura_Plain: plain plaster with grime bands (rural / cheap).",
     {"key": "kura_plain", "view": "3q"}),
    ("kura_in_ground", K + "Ground floor from the door: boards on the footing, interior plaster (shikkui_int), "
     "the open stair (jp_p_stair _open) along the back wall up to the upper floor.",
     {"key": "kura_namako", "cam": [1.9, 2.05, 1.45], "look": [-1.2, 1.5, -1.3], "lens": 13, "open": 1.0}),
    ("kura_in_upper", K + "Upper floor: the stairwell with its rim and guard rail, the ridge beam and purlins, the "
     "gable windows (bars) and vent.", {"key": "kura_namako", "cam": [2.3, 4.45, 1.2], "look": [-1.4, 3.6, -0.9],
                                          "lens": 13}),
    ("kura_cut", K + "Cut at 4.6 m: the upper floor from above, the stairwell over the flight.",
     {"key": "kura_namako", "view": "3q", "cut_y": 4.6}),
]

# furnished variants: key -> short title (sheet captions)
FURNISHED = {
    "f_th_kamigata_3k_middle_komeya": "Kamigata townhouse 3 ken, rice dealer (T3)",
    "f_th_kamigata_2k_middle_kamiya": "Kamigata townhouse 2 ken, paper shop (T3)",
    "f_th_edo_2k_middle_gofuku": "Edo townhouse 2 ken, cloth dealer (T3)",
    "f_th_edo_3k_cornerr_sakaya": "Edo townhouse 3 ken corner, sake shop (T3)",
    "f_pt_det_tile_nuriya_home": "Post-town house, home (T2)",
    "f_inn_std_tile": "Ordinary inn (T2)",
    "f_inn_grand": "Grand inn (T3)",
    "f_farmhouse_kanto": "Kanto farmhouse (T2)",
    "f_farmhouse_kinai": "Kinai farmhouse (T2)",
    "f_hut_east_l_board": "Hut east (T1)",
    "f_hut_west_thatch_leanl": "Hut west (T1)",
    "f_shed_walled_woodshed": "Shed with woodshed (T1-2)",
    "f_kura_namako": "Kura, storage",
    "f_kura_kuro_hinged": "Kura (hinged leaves), storage",
}


def _furn_rooms():
    import registry
    import pipeline
    rooms_jobs, plan_jobs = [], []
    for key, title in FURNISHED.items():
        try:
            b = registry.get(key)
        except KeyError:
            continue
        mod = pipeline.load_module(b)
        M, floors, rooms = mod.model(name=b["name"], **b["params"])
        D = mod.D
        by = D.by_room()
        for r in rooms:
            x0, x1, z0, z1 = r["rect_model"]
            y = r["level_m"]
            its = by.get(r["name"], [])
            names = ", ".join(sorted({i["name"].replace("jp_f_", "") for i in its}))
            n = sum(1 for i in its if i["count"])
            # camera in the corner farthest from most of the furniture, looking at the opposite corner
            cx = (x0 + x1) / 2
            cz = (z0 + z1) / 2
            mx = sum(i["x"] for i in its) / len(its) if its else cx
            mz = sum(i["z"] for i in its) / len(its) if its else cz
            ex = x0 + 0.25 if mx > cx else x1 - 0.25
            ez = z0 + 0.25 if mz > cz else z1 - 0.25
            lx = x1 - 0.4 if ex < cx else x0 + 0.4
            lz = z1 - 0.4 if ez < cz else z0 + 0.4
            rooms_jobs.append(("rm_%s_%s" % (key, r["name"]), "%s | %s (%s), %d counted props: %s" % (
                title, r["name"], r["tag"], n, names),
                {"key": key, "cam": [ex, y + 1.62, ez], "look": [lx, y + 0.55, lz], "lens": 12, "site": False,
                 "res": [960, 640]}))
        levels = sorted({round(r["level_m"], 2) for r in rooms if r["level_m"] > 1.0})
        bb = M.bbox()
        scale = max(bb[1] - bb[0], bb[5] - bb[4]) * 1.08
        plan_jobs.append(("pl_%s" % key, "%s: loot plan cut at 1.75 m (GREEN floor points, ORANGE on props), street at "
                          "the top" % title, {"key": key, "plan": True, "scale": scale, "cut_y": 1.75, "loot": True,
                                               "site": False, "center": [(bb[0] + bb[1]) / 2, (bb[4] + bb[5]) / 2],
                                               "res": [900, 900]}))
        for lv in levels:
            plan_jobs.append(("pl_%s_%d" % (key, int(lv * 100)), "%s: upper floor (%.2f), loot plan" % (title, lv),
                              {"key": key, "plan": True, "scale": scale, "cut_y": lv + 1.75, "loot": True,
                               "loot_min_y": lv - 0.2, "site": False, "center": [(bb[0] + bb[1]) / 2,
                                                                                  (bb[4] + bb[5]) / 2],
                               "res": [900, 900]}))
    return rooms_jobs, plan_jobs


class _Lazy(dict):
    def __missing__(self, k):
        if k in ("rooms", "plans"):
            r, p = _furn_rooms()
            self["rooms"], self["plans"] = r, p
            return self[k]
        raise KeyError(k)


JOBS = _Lazy(kura=KURA)
JOBS_ALL = ("kura", "rooms", "plans")
SHEETS = {
    "kura": ("C3 kura (DW22): three shells, two floors by stair", "", 4, 480, 360, 76, 58),
    "rooms": ("C3 furnished rooms (props as proxies, life layer)", "", 4, 480, 320, 92, 58),
    "plans": ("C3 loot plans (green = floor, orange = on props)", "", 4, 450, 450, 40, 56),
}
