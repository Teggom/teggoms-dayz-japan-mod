#!/usr/bin/env python3
r"""Land_JP_Machiya_T3_01_Shop - the B4 pilot: machiya_t3_01 furnished as a Kamigata general-goods shop
(research/interior/BUILD_LIST.md "The pilot"), with its street front and back yard dressed (research/outdoor_kit
BUILD_LIST.md "Wave 1", column "B4 pilot").

PLAYBOOK §10.4: a furnished variant is its own p3d = the same shell parts (buildings/machiya_t3_01, rebuilt here from
its recipe) + a proxy set. Props are PROXIES in the LODs vanilla uses (BUILD_LIST Q5, jpparts/proxies.py + decor.py):
collision furniture in Resolution 1 + Geometry + View + Fire, flat and hanging props (litter, mats, the kamidana, the
shop-front cloth and lanterns) in Resolution 1 only. Yard and street objects with collision (well, tubs, cart, bench,
fire tub, firewood, laundry pole, the Jizo box, gutter covers) are separate map objects (test/placements/C.csv via
buildings/pipeline.py), placed in this building's model frame so they follow it.

Model frame: origin = footprint centre at grade, +z = street front, +x = the rooms side; placed at yaw 180 (front
south). Rooms (model rects, from machiya_t3_01.rooms): toriniwa x -3.58..-1.88 z -0.85..4.49 (doma 0.05); mise
x -1.76..3.58 z 1.88..4.49 (0.50; board strip z 4.035..4.49); zashiki z -0.85..1.76 (0.50); kitchen x -3.58..-0.06
z -4.49..-0.97 (doma 0.05, kamado x -3.52..-2.82 z -3.40..-1.60); storage x 0.06..3.58 z -4.49..-0.97 (boards 0.08).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings", "machiya_t3_01"))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))
import machiya_t3_01 as MT  # noqa: E402
from jpparts import decor as DC  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

NAME = "jp_machiya_t3_01_shop"
CLASS = "Land_JP_Machiya_T3_01_Shop"
FRAME_NOTE = MT.FRAME_NOTE
POSTS = MT.POSTS

KAMADO = (-3.56, -2.86, -3.40, -1.60)          # kamado plan rect (model) - machiya_t3_01.kamado()
KAMADO_SEAT = (-3.57, -2.85, 0.04, 0.78, -3.41, -1.59)
KAMA_X = -3.21                                  # the two pot rims: kamado centre line, z -2.95 / -2.05
RIM_TOP = 0.80                                  # kamado top 0.77 + the iron rim 0.03
KAMA_SEAT_Y = 0.168                             # jp_f_kama: flange height (B3a_PROGRESS)
# open passages (no door) the clear band must reach, and built-in obstacles it must go round
EXTRA_OPENINGS = {"toriniwa": [("passage to the kitchen", (-2.73, -0.91))],
                  "kitchen": [("passage from the toriniwa", (-2.73, -0.91))]}
FIXED_BAND = {"kitchen": [KAMADO]}
SITE_BOUNDS = (-60.0, 60.0, -60.0, 60.0)        # the 200 m test pad is (1024, 1024) +-100: generous in model frame
PENT_UNDER = 2.92                               # street pent soffit ~0.5 m out from the wall (pent y 3.30, slope 0.40)

D = None


def furnish(rooms, floors):
    it = DC.item
    d = DC.Decor(rooms, floors)
    P = d.place
    # ------------------------------------------------------------ toriniwa (doma: kept clear, a bucket, litter)
    P(it("jp_f_tana_091_1", "toriniwa", -3.575, 1.35, 90, why="shelf on the board wall between the two step stones"))
    P(it("jp_f_oke_bucket", "toriniwa", -3.38, 3.70, 0, why="bucket by the entrance wall"))
    P(it("jp_f_oke_tipped", "toriniwa", -3.10, -0.20, 200, why="a tipped bucket at the kitchen passage (disorder)"))
    P(it("jp_f_debris_leaves", "toriniwa", -2.85, 3.95, 15, why="leaves blown in under the entrance door"))
    P(it("jp_f_debris_straw", "toriniwa", -2.65, 0.95, 70, why="straw litter"))
    # ------------------------------------------------------------ mise (shop:general)
    P(it("jp_f_misedana_1ken", "mise", 1.50, 4.18, 0, why="stepped goods stand on the board strip, facing the lattice"))
    P(it("jp_f_goods_general_paper", "mise", 2.85, 4.26, 0, why="paper bundles on the display strip"))
    P(it("jp_f_zukue_choba", "mise", 3.05, 2.25, 0, why="account desk in the choba corner (back, east)"))
    P(it("jp_f_choba_goshi_3", "mise", 3.05, 2.62, 0, why="counting-desk lattice in front of the desk"))
    P(it("jp_f_tana_091_3_sag", "mise", 3.575, 3.90, 270, why="stock shelf on the gable wall, one board down"))
    P(it("jp_f_hibachi_box", "mise", 2.30, 2.40, 0, why="brazier by the choba"))
    P(it("jp_f_tabakobon_spilled", "mise", 2.25, 2.95, 30, why="tobacco tray knocked over (disorder)"))
    # ------------------------------------------------------------ zashiki (best room)
    P(it("jp_f_futon_laid", "zashiki", 0.30, -0.35, 0, why="bedding laid out along the back wall"))
    P(it("jp_f_futon_stack", "zashiki", 3.08, 1.40, 0, why="folded bedding stacked in the corner (no oshiire)"))
    P(it("jp_f_tansu_ransacked", "zashiki", 2.05, -0.62, 0, why="clothing chest, drawers out (disorder)"))
    P(it("jp_f_andon_kaku", "zashiki", 1.40, -0.66, 0, why="standing lamp by the bedding, unlit"))
    P(it("jp_f_hibachi_round", "zashiki", 2.25, 0.90, 0, why="round brazier"))
    P(it("jp_f_kori", "zashiki", 3.10, -0.62, 0, why="wicker trunk ('a box')"))
    # ------------------------------------------------------------ kitchen (doma)
    P(it("jp_f_kama", "kitchen", KAMA_X, -2.95, 90, y=RIM_TOP - KAMA_SEAT_Y, seat=KAMADO_SEAT,
         why="rice pot seated in the kamado's first mouth"))
    P(it("jp_f_kama_nolid", "kitchen", KAMA_X, -2.05, 90, y=RIM_TOP - KAMA_SEAT_Y, seat=KAMADO_SEAT,
         why="second pot, lid off and rusted (disorder)"))
    # F1 (G4 walk): its lid is now its own small prop, lying on the doma at the kamado's end (it used to float 0.63 m
    # up beside the seated pot); visual only, not counted against the room's props
    P(it("jp_f_kama_lid", "kitchen", -2.62, -1.80, 25, count=False,
         why="the second pot's lid, knocked off onto the doma"))
    P(it("jp_f_nagashi_wood", "kitchen", -1.22, -0.975, 180, why="wooden sink against the omoya back wall"))
    P(it("jp_f_mizugame", "kitchen", -0.40, -1.29, 0, why="water jar beside the sink"))
    sh = P(it("jp_f_tana_136_1", "kitchen", -1.22, -0.975, 180, y=0.05 + 0.50, why="shelf over the sink (board 1.45, "
                                                                                   "1.40 over the doma)"))
    sh["on_floor"] = False                       # wall-hung higher than its default: the wall check still applies
    P(it("jp_f_kamidana_plain", "kitchen", -0.40, -0.975, 180, why="god shelf high on the wall over the water jar, "
                                                                     "undisturbed"))
    P(it("jp_f_firewood_stack", "kitchen", -0.52, -4.29, 0, why="split wood under the kitchen window"))
    # ------------------------------------------------------------ storage (monooki)
    P(it("jp_f_rack_1ken", "storage", 1.90, -4.255, 0, why="board shelving along the back wall"))
    P(it("jp_f_nagamochi_open", "storage", 1.45, -1.48, 180, why="long chest against the front wall, lid thrown back"))
    P(it("jp_f_tawara_stack6_burst", "storage", 3.00, -1.36, 0, why="rice bales, one burst (heavier disorder)"))
    P(it("jp_f_box_stack3", "storage", 3.25, -4.26, 0, why="lidded boxes in the corner"))
    P(it("jp_f_kori_2", "storage", 0.47, -4.26, 0, why="two wicker trunks"))
    P(it("jp_f_jar_l", "storage", 3.30, -2.30, 0, why="big storage jar"))
    P(it("jp_f_mushiro", "storage", 1.90, -2.85, 10, why="a straw mat on the floor"))
    # ------------------------------------------------------------ street front: shop-front dressing as proxies (G1 A3-8)
    H = DC.item
    P(H("jp_s_shopfront_noren_long", "street", -2.73, 4.69, 0, y=0.10, why="long noren on the entrance"))
    P(H("jp_s_shopfront_mizuhiki", "street", 1.82, 4.98, 0, y=PENT_UNDER - 2.38, why="short curtain under the pent, "
                                                                                    "over the degoshi"))
    P(H("jp_s_shopfront_kanban_hang", "street", 3.35, 4.98, 0, y=0.0, why="hanging signboard at the shop corner"))
    P(H("jp_s_lantern_sign_kake", "street", -1.36, 4.69, 0, y=0.05, why="kake-andon beside the entrance"))
    P(H("jp_s_fire_tub_eave", "street", 3.72, 4.00, 90, y=0.0, why="fire bucket on a peg on the gable end"))
    for x in d.items:
        if x["room"] == "street":
            x["hung"] = True
    # ------------------------------------------------------------ street and yard: separate map objects
    S = d.place_site
    S(it("jp_s_gutter_slab", "street", -2.73, 6.20, 0, why="stone slab over the gutter at the door"))
    for gx in (-0.91, 0.91, 2.73):
        S(it("jp_s_gutter_board_1ken", "street", gx, 6.20, 0, why="covered gutter (dobu-ita) along the front"))
    S(it("jp_s_bench_ab_tipped", "street", -0.45, 5.10, 180, why="endai under the pent, tipped over"))
    S(it("jp_s_fire_tub_open", "street", 4.55, 5.60, 0, why="fire tub at the street corner, bucket pyramid fallen"))
    S(it("jp_s_nobori_ab_tattered", "street", 3.40, 7.00, 0, why="one tattered shop banner"))
    S(it("jp_s_handcart_load_bales", "street", 1.00, 9.80, 70, why="half-loaded cart left in the street"))
    S(it("jp_s_tenbin_leaning", "street", -3.785, 3.30, 270, why="carrying pole leaning by the shop door"))
    S(it("jp_s_jizo_hut_box", "street", -5.30, 6.60, 0, why="Kyoto corner box with its small Jizo"))
    S(it("jp_s_firewood_stack_wall_1ken_h120", "yard", -3.84, -2.50, 270, why="firewood against the kitchen wall"))
    S(it("jp_s_oke_tarai", "yard", -1.40, -5.40, 0, why="wash tub by the back door"))
    S(it("jp_s_oke_teoke", "yard", -0.70, -5.20, 0, why="hand bucket"))
    S(it("jp_s_oke_ab_tipped", "yard", -0.35, -5.95, 40, why="a tipped tub"))
    well = S(it("jp_s_well_tsurube_curb_stone", "yard", -2.40, -8.30, 0, why="pulley well (drink, wash, fill)"))
    S(it("jp_s_laundry_pole_load_cloth", "yard", 2.00, -7.30, 0, why="laundry pole, cloth fallen"))
    # the rope over the well: along the cap beam, in front of it (well frame: posts +-0.65, cap beam 2.40-2.52)
    wp = DC.to_model(well, (0.0, 0.0, 0.10))
    rope = S(it("jp_s_shimenawa_len_1ken", "yard", wp[0], wp[2], well["yaw"], y=2.40 - 2.54,
                why="rope hung on the well's cap beam"))
    rope["hung"] = True
    return d


def model():
    global D
    M, floors, rooms = MT.model()
    D = furnish(rooms, floors)
    return M, floors, rooms


def proxies():
    return DC.proxies(D.items)


def loot_points(floors):
    return D.loot_points(bloot.floor_points)


def site():
    return [{"p3d": s["info"]["p3d"], "x": round(s["x"], 4), "z": round(s["z"], 4), "yaw": s["yaw"],
             "y": round(s["y"], 4), "why": s["why"]} for s in D.site]


if __name__ == "__main__":
    M, floors, rooms = model()
    for r, its in D.by_room().items():
        print(r, len(its), [i["name"] for i in its])
    pts = loot_points(floors)
    print(len(pts), "loot points,", sum(1 for p in pts if p["container"] == "lootshelves"), "raised")
