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
    "f_shrine_haiden_town": "Town haiden (Hachimangu)", "f_shrine_haiden_village": "Village haiden",
    "f_shrine_honden_nagare_town": "Town honden (sealed)", "f_shrine_honden_nagare_village_chigi": "Village honden",
    "f_shrine_temizuya_town": "Temizuya", "f_shrine_shamusho_sangawara": "Shamusho (priests' office)",
    "f_shrine_kagura_town": "Kagura stage", "f_temple_hondo_village": "Village hondo (Jodo)",
    "f_temple_hondo_town": "Town hondo (Zen)", "f_temple_do_2_board": "Jizo hall", "f_temple_do_3_tile": "Kannon hall",
    "f_temple_kuri_village": "Village kuri", "f_temple_kuri_town": "Town kuri (Zen)",
    "f_temple_shoro_village": "Village bell tower", "f_temple_shoro_town": "Town bell tower",
    "f_temple_gate_yakuimon": "Yakui-mon gate", "f_temple_gate_shikyakumon": "Shikyaku-mon gate",
    "f_teahouse_bench_itabuki": "Bench tea house", "f_teahouse_shop_thatch": "Tea house (chamise)",
    "f_teahouse_tateba_itabuki": "Tateba tea house", "f_smithy_open_itabuki": "Smithy",
    "f_swordsmith_sangawara": "Swordsmith", "f_guardhut_m_itabuki": "Jishin-ban guard house",
    "f_kido_lattice_bantaya": "Kido + keeper's hut",
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
            if r["name"] in ("en_left", "en_right"):
                continue
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


S = "The dressed test street (z 1080): "
STREET = [
    ("st_west", S + "from the west end at eye height: the Kamigata row (north, left) with the rice dealer and the paper "
     "shop furnished, the post-town houses and the inns (south, right), the dead-world litter in the street.",
     {"scene": "street", "cam": [-42.0, 1.7, -0.3], "look": [0.0, 2.2, 0.8], "lens": 20}),
    ("st_east", S + "from the east end: the Edo row (the sake shop on the corner, the cloth dealer), the fire-watch ladder "
     "and the notice board on the ward corner, the grand inn beyond.",
     {"scene": "street", "cam": [42.0, 1.7, 0.2], "look": [0.0, 2.2, 0.8], "lens": 20}),
    ("st_corner", S + "the ward corner: fire-watch ladder with its bell, the bucket rack, the notice board, the Jizo, a "
     "tipped palanquin in the street.", {"scene": "street", "cam": [-4.0, 1.7, -1.5], "look": [10.0, 2.2, 5.5],
                                           "lens": 18}),
    ("st_inns", S + "the two inns (south side): noren and inn lanterns, benches, sandals for sale under the eave, "
     "scattered clogs.", {"scene": "street", "cam": [-1.0, 1.7, 1.6], "look": [-6.0, 2.4, -7.0], "lens": 16}),
    ("st_shops", S + "the Kamigata shops: noren, hanging signboard, the brush-shaped sign, gutter covers, a vendor's "
     "spilled load.", {"scene": "street", "cam": [-20.0, 1.7, 0.4], "look": [-29.0, 2.2, 5.5], "lens": 16}),
    ("st_air", S + "from above: the rows, the ward corner, and the town kura behind the Kamigata row.",
     {"scene": "street", "cam": [30.0, 30.0, -34.0], "look": [-6.0, 0.0, 5.0], "lens": 22}),
    ("st_kura", S + "the town kura (Land_JP_Kura_Namako_Furnished) behind the Kamigata row, its door south.",
     {"scene": "street", "cam": [-19.5, 1.7, 13.2], "look": [-24.0, 3.0, 17.5], "lens": 20}),
]
H = "The dressed hamlet (west yard): "
HAMLET = [
    ("hm_south", H + "from the south field: stooks, bird clappers and the low rice rack; the huts, the farmhouses behind.",
     {"scene": "hamlet", "cam": [4.0, 1.7, -30.0], "look": [0.0, 3.0, 0.0], "lens": 16}),
    ("hm_yard", H + "the threshing yard: straw stack, persimmons drying on a pole, the Kanto farmhouse with its persimmon "
     "curtain and tools by the door.", {"scene": "hamlet", "cam": [4.0, 1.7, -12.0], "look": [-8.0, 2.5, 3.0],
                                         "lens": 16}),
    ("hm_kinai", H + "the Kinai farmhouse: persimmons under the lower roof, tools by the door, the rice racks beyond.",
     {"scene": "hamlet", "cam": [8.0, 1.7, -12.0], "look": [14.0, 2.5, 3.0], "lens": 16}),
    ("hm_stable", H + "the stable yard beside the Kanto house: tie post, pack saddle on its rack, stone trough, stooks.",
     {"scene": "hamlet", "cam": [-10.5, 1.7, -9.0], "look": [-20.0, 1.2, -2.0], "lens": 18}),
    ("hm_water", H + "the bamboo pipe into its trough between the houses, and the lever well by the huts.",
     {"scene": "hamlet", "cam": [3.0, 1.7, 6.0], "look": [3.2, 0.8, 12.0], "lens": 20}),
    ("hm_kura", H + "the hamlet kura (Land_JP_Kura_Kuro_Hinged_Furnished, black boards, hinged plaster leaves), the "
     "Jizo and Koshin stone at the hamlet entrance.", {"scene": "hamlet", "cam": [15.0, 1.7, 15.0],
                                                        "look": [25.0, 2.5, 17.0], "lens": 18}),
    ("hm_air", H + "from above the south-east.", {"scene": "hamlet", "cam": [40.0, 34.0, -40.0], "look": [0.0, 0.0, 4.0],
                                                   "lens": 22}),
]


class _Lazy(dict):
    def __missing__(self, k):
        if k in ("rooms", "plans"):
            r, p = _furn_rooms()
            self["rooms"], self["plans"] = r, p
            return self[k]
        raise KeyError(k)


JOBS = _Lazy()
JOBS_ALL = ("rooms", "plans")
SHEETS = {
    "street": ("C3 the dressed test street (player height)", "", 2, 800, 500, 60, 95),
    "hamlet": ("C3 the dressed hamlet (player height)", "", 2, 800, 500, 60, 95),
    "kura": ("C3 kura (DW22): three shells, two floors by stair", "", 4, 480, 360, 76, 58),
    "rooms": ("W2F furnished rooms (wave 2: shrine, temple, civic)", "", 4, 480, 320, 92, 58),
    "plans": ("W2F loot plans (green = floor, orange = on props)", "", 4, 450, 450, 40, 56),
}
