"""The wave-1 dressings (C3, 2026-09-30): one function per furnished variant, called by buildings/furnishkit.py with a
Ctx (model frame of the base shell: x, y up, z = front; rooms and doors as spikes/C3/inspect_shell.py prints them).

Binding rules (research/catalogue/G1_DECISIONS.md A2, research/interior/BUILD_LIST.md, LIFE_LAYER.md / _ERA.md):
  5-7 counted props a room (wall / beam / post / surface life items do not count); collision cover <= 25 % of a room
  (40 % storage); a 1.00 m clear band door-to-door and door-to-centre; >= 1 raised loot surface a room; no tatami in
  T1; zabuton T3 only; no tetsubin, no tokonoma dressing in commoner houses; moderate "as left" disorder (one or two
  signs a room, one room in five heavier); butsudan / kamidana undisturbed and without loot; andon unlit; autumn
  (persimmons, daikon drying, the mosquito net folded away). Tier markers (tea set) only in upper (T3) houses.
KEEP_TRADES' 22 shop sets are not built yet: the shops take their trade from the goods and life-layer items that exist
(rice: bales, sacks, measures; paper: paper bundles, writing box; cloth: cloth bolts, scales; sake: casks, flasks).
Every placement carries a 'why' (rooms.json / checks read as a room-by-room list).
"""

LOFT_CEIL = 3.00          # townhouse / post-town / inn loft underside (templates/townhouse.py CEIL): the beam line


def _gutters(c, xs, z):
    for x in xs:
        c.site("jp_s_gutter_board_1ken", x, z, 0, why="covered street gutter (dobu-ita)")


# ================================================================================================ townhouse kit
def _tori_3k(c, x_wall="xmax", t=3):
    """The toriniwa of a 3-ken unit / post-town house / C1 row (x 0.97..2.67 or mirrored): kept clear."""
    c.wall("toriniwa", x_wall, 0.15, "jp_f_tana_091_1", why="shelf on the side wall between the two step stones")
    c.free("toriniwa", "jp_f_debris_leaves", 1.95, 3.10, 20, why="leaves blown in under the entrance door")
    c.free("toriniwa", "jp_f_debris_straw", 1.95, -0.30, 70, why="straw tracked in")
    c.onwall("toriniwa", x_wall, 3.35, "jp_f_ofuda_akiba", why="Akiba fire charm on the entrance post")


def _kitchen_3k(c, pots=("jp_f_kama", "jp_f_seiro_kama2"), extra="jp_f_oke_pickle", firewood=True):
    """The kitchen doma of a 3-ken unit (x -2.67..2.67, z -3.58..-1.88): the kamado at the far end (mouths to +x),
    sink + shelf + water jar on the back wall, split wood by the omoya wall."""
    c.kamado("kitchen", (-2.65, -1.95, -3.45, -2.15), "+x", n=2)
    for k, p in enumerate(pots):
        c.pot("kitchen", p, k, why="pot in mouth %d" % (k + 1))
    c.wall("kitchen", "zmin", -0.90, "jp_f_nagashi_wood", why="wooden sink against the back wall")
    sh = c.wall("kitchen", "zmin", -0.90, "jp_f_tana_136_1", y=0.05 + 0.50, why="shelf over the sink")
    c.free("kitchen", "jp_f_mizugame", -0.05, -3.25, 0, why="water jar beside the sink")
    if firewood:
        c.wall("kitchen", "zmax", -1.20, "jp_f_firewood_stack", why="split wood against the omoya wall")
    if extra:
        c.free("kitchen", extra, 0.90, -3.25, 0, why="tub / cask by the sink")
    c.surf(sh, "jp_f_hiuchi_box", dx=0.35, why="fire-striker box on the shelf")
    c.onwall("kitchen", "zmin", 0.85, "jp_f_utensil_board", why="ladles and dipper on the wall")
    c.passage(("toriniwa", "kitchen"), c.info_passage[0], c.info_passage[1], "passage toriniwa <-> kitchen")
    return sh


def _tori_2k(c):
    """The toriniwa of a 2-ken unit (x -1.76..-0.06, steps on the +x side)."""
    c.wall("toriniwa", "xmin", 0.20, "jp_f_tana_091_1", why="shelf on the party wall")
    c.free("toriniwa", "jp_f_oke_bucket", -1.52, 2.55, 15, why="bucket by the entrance")
    c.free("toriniwa", "jp_f_debris_leaves", -1.00, 3.10, 20, why="leaves blown in under the entrance door")
    c.onwall("toriniwa", "xmin", 3.35, "jp_f_ofuda_single", why="a charm on the entrance post")


def _kitchen_2k(c, pot="jp_f_kama_nolid", lid=True, flat="jp_f_suribachi_spilled"):
    """The kitchen of a 2-ken unit (x -1.76..1.76, z -3.58..-1.88; back door and passage on the -x side): a one-mouth
    kamado at the far end, the sink, a shelf, the water jar beside the stove."""
    c.kamado("kitchen", (1.04, 1.74, -3.50, -2.80), "-x", n=1)
    c.pot("kitchen", pot, 0, why="the pot left in the stove")
    if lid:
        c.free("kitchen", "jp_f_kama_lid", 0.70, -2.35, 25, count=False, why="its lid knocked off onto the doma")
    c.wall("kitchen", "zmin", 0.25, "jp_f_nagashi_wood", why="wooden sink against the back wall")
    sh = c.wall("kitchen", "zmin", 0.25, "jp_f_tana_091_1", y=0.05 + 0.55, why="shelf over the sink")
    c.free("kitchen", "jp_f_mizugame", 1.40, -2.30, 0, why="water jar beside the stove")
    c.free("kitchen", flat, -0.90, -2.70, 30, why="a grinding bowl dropped, contents spilled (disorder)")
    c.surf(sh, "jp_f_hiuchi_box", why="fire-striker box on the shelf")
    c.onwall("kitchen", "zmin", 1.39, "jp_f_utensil_board_small", why="ladles over the stove")
    c.passage(("toriniwa", "kitchen"), c.info_passage[0], c.info_passage[1], "passage toriniwa <-> kitchen")
    return sh


def kamigata_komeya(c):
    """Kamigata 3-ken middle unit (T3), a rice dealer's shop (komeya): bales, straw sacks, measures, the choba."""
    _tori_3k(c)
    c.free("toriniwa", "jp_f_oke_bucket", 2.40, 2.55, 15, why="bucket by the entrance")
    c.free("toriniwa", "jp_f_charcoal_bale", 2.45, -1.25, 0, why="a charcoal bale by the kitchen passage")
    c.onwall("toriniwa", "xmax", 2.10, "jp_f_bangasa_leaning", why="an oiled umbrella leaning by the door")
    c.hang("toriniwa", "jp_f_chochin_shop", 1.82, 2.40, LOFT_CEIL, why="the shop's lantern hung from the loft joists")
    # ---------------------------------------------------------------- mise (shop: rice)
    c.wall("mise", "xmin", 2.95, "jp_f_tawara_stack6", why="rice bales stacked against the party wall")
    t = c.free("mise", "jp_f_tawara", -1.30, 3.20, 8, why="a single bale left out by the lattice")
    c.free("mise", "jp_f_tawara_kamasu_stack3", -0.30, 3.25, -6, why="straw sacks (kamasu) of grain")
    d = c.wall("mise", "xmin", 1.85, "jp_f_zukue_choba", why="the account desk in the choba corner")
    c.free("mise", "jp_f_choba_set_zenibako", -1.95, 1.60, 20, why="the coin box beside the desk")
    c.free("mise", "jp_f_masu_spilled", -0.85, 2.55, 35, why="a measure knocked over, rice spilled (disorder)")
    c.surf(d, "jp_f_choba_set_desk", why="ledgers and abacus on the desk")
    c.surf(t, "jp_f_masu_to", why="the big measure on the bale")
    c.onwall("mise", "zmin", -2.30, "jp_f_kamidana_plain", why="god shelf high on the partition, undisturbed")
    c.onwall("mise", "xmin", 1.85, "jp_f_koyomi", why="this year's calendar over the desk")
    # ---------------------------------------------------------------- oku (zashiki, T3)
    c.wall("oku", "zmin", -1.20, "jp_f_futon_laid", why="bedding still laid out along the back wall")
    ts = c.wall("oku", "xmin", -0.30, "jp_f_tansu", why="clothing chest against the party wall")
    c.free("oku", "jp_f_andon_kaku", -2.45, -1.50, 0, why="standing lamp at the head of the bedding, unlit")
    c.free("oku", "jp_f_hibachi_round", -0.95, 0.10, 0, why="round brazier")
    c.wall("oku", "xmin", 0.52, "jp_f_butsudan_lacquer", why="lacquered Buddhist altar, undisturbed")
    c.free("oku", "jp_f_enza_zabuton", -0.95, -0.40, 12, why="a cotton cushion (T3)")
    c.surf(ts, "jp_f_tea_dobin", why="clay tea pot on the chest (T3 marker)")
    c.hang("oku", "jp_f_kaya_bundle", -2.30, -1.35, LOFT_CEIL, over="corner", why="the mosquito net folded away "
           "for autumn")
    _kitchen_3k(c)
    # ---------------------------------------------------------------- street front (proxies) + street / yard objects
    c.front("jp_s_shopfront_noren_long", 1.94, 3.96, 0.10, why="long noren on the entrance")
    c.front("jp_s_shopfront_kanban_hang", -2.40, 4.05, 0.0, why="hanging signboard at the shop end")
    c.site("jp_s_gutter_slab", 1.94, 5.10, 0, why="stone slab over the gutter at the door")
    _gutters(c, (-1.82, 0.00), 5.10)
    c.site("jp_s_oke_tarai", 1.60, -4.75, 0, why="wash tub by the back door")
    c.site("jp_s_firewood_stack_bundle", -1.80, -3.80, 180, why="firewood bundles against the kitchen wall")


def kamigata_kamiya(c):
    """Kamigata 2-ken middle unit (T3), a paper and sundries shop (kamiya): a stand of paper, the writing box."""
    _tori_2k(c)
    c.free("toriniwa", "jp_f_debris_paper", -1.10, -0.50, 40, why="paper scraps blown through from the shop")
    c.free("toriniwa", "jp_f_jar_m", -1.52, -1.30, 0, why="a lidded jar by the kitchen passage")
    c.hang("toriniwa", "jp_f_chochin_shop2", -0.91, 2.40, LOFT_CEIL, why="the shop lantern from the loft joists")
    # ---------------------------------------------------------------- mise (shop: paper)
    st = c.wall("mise", "zmax", 0.75, "jp_f_misedana_half", why="stepped stand of paper goods behind the lattice")
    d = c.wall("mise", "zmin", 1.20, "jp_f_zukue_choba", why="the account desk against the back partition")
    c.free("mise", "jp_f_goods_general_paper_swept", 0.70, 2.15, 25, why="paper bundles swept off the stand")
    c.free("mise", "jp_f_enza_zabuton", 1.25, 1.75, 5, why="the clerk's cushion behind the desk (T3)")
    c.free("mise", "jp_f_box_m", 1.45, 2.35, 10, why="a box of stock")
    c.surf(d, "jp_f_writing_box_open", why="the writing box open on the desk")
    c.onwall("mise", "zmin", 0.40, "jp_f_kamidana_plain", why="god shelf high on the partition, undisturbed")
    c.onwall("mise", "xmax", 2.10, "jp_f_koyomi_curled", why="the calendar, curling")
    # ---------------------------------------------------------------- oku (zashiki, T3)
    c.wall("oku", "xmax", -0.80, "jp_f_futon_laid", why="bedding laid out along the party wall")
    ts = c.wall("oku", "zmax", 0.62, "jp_f_tansu_single", why="a low chest against the shop partition")
    c.free("oku", "jp_f_andon_ariake", 0.35, 0.10, 0, why="night lamp by the chest, unlit")
    c.free("oku", "jp_f_mirror_stand_open", 0.45, -0.70, 30, why="mirror stand, its cover off")
    c.free("oku", "jp_f_enza_zabuton_folded", 0.35, -1.30, 0, why="a folded cushion (T3)")
    c.surf(ts, "jp_f_sewing_box", why="the sewing box on the chest")
    c.hang("oku", "jp_f_kaya_bundle", 1.45, -1.45, LOFT_CEIL, over="furniture", why="the mosquito net folded away")
    _kitchen_2k(c)
    c.front("jp_s_shopfront_noren_long", -1.03, 3.96, 0.10, why="long noren on the entrance")
    c.front("jp_s_shopfront_shape_brush", 1.55, 4.05, 0.0, why="a brush-shaped sign (paper and brushes)")
    c.site("jp_s_gutter_slab", -1.03, 5.10, 0, why="stone slab over the gutter at the door")
    _gutters(c, (0.91,), 5.10)
    c.site("jp_s_oke_ab_tipped", 0.60, -4.90, 30, why="a tipped tub in the back yard")


def edo_gofuku(c):
    """Edo 2-ken middle unit (T3), a cloth dealer (gofuku / futomono): bolts on a stand, the scales, a robe rack."""
    _tori_2k(c)
    c.free("toriniwa", "jp_f_debris_straw", -1.10, -0.50, 40, why="straw litter")
    c.free("toriniwa", "jp_f_jar_s", -1.55, -1.30, 0, why="a small jar by the kitchen passage")
    # ---------------------------------------------------------------- mise (shop: cloth)
    c.wall("mise", "zmax", 0.75, "jp_f_misedana_half", why="stepped stand of cloth bolts behind the lattice")
    d = c.wall("mise", "zmin", 1.20, "jp_f_zukue_choba", why="the account desk")
    c.free("mise", "jp_f_goods_general_cloth_swept", 0.75, 2.20, 20, why="bolts of cloth pulled down and "
           "trampled (heavier disorder: one room in five)")
    c.free("mise", "jp_f_enza_zabuton", 1.25, 1.75, 5, why="the clerk's cushion (T3)")
    c.free("mise", "jp_f_box_s_lacquer", 1.50, 2.40, 10, why="a lacquered box of samples")
    c.surf(d, "jp_f_choba_set_tenbin", why="the money scales on the desk")
    c.onwall("mise", "zmin", 0.40, "jp_f_kamidana_plain", why="god shelf, undisturbed")
    c.onwall("mise", "xmax", 2.10, "jp_f_koyomi", why="this year's calendar")
    # ---------------------------------------------------------------- oku
    c.wall("oku", "xmax", -0.80, "jp_f_futon_laid", why="bedding laid out along the party wall")
    ts = c.wall("oku", "zmax", 0.62, "jp_f_tansu_single", why="a low chest against the shop partition")
    c.free("oku", "jp_f_andon_kaku", 0.30, 0.05, 0, why="standing lamp, unlit")
    c.free("oku", "jp_f_clothes_kimono_obi", 0.40, -0.45, 60, why="a kimono and obi dropped on the mats")
    c.free("oku", "jp_f_enza_zabuton", 0.35, -1.35, 0, why="a cushion (T3)")
    c.surf(ts, "jp_f_tea_matcha", why="a tea bowl and caddy on the chest (T3 marker)")
    _kitchen_2k(c, pot="jp_f_kama", lid=False, flat="jp_f_tableware_scattered")
    c.front("jp_s_shopfront_noren_half", -1.03, 3.96, 0.0, why="half noren on the entrance")
    c.front("jp_s_shopfront_sudare_up", 1.48, 3.96, 0.0, why="a reed blind rolled up over the lattice")
    c.site("jp_s_gutter_slab", -1.03, 5.10, 0, why="stone slab over the gutter at the door")
    _gutters(c, (0.91,), 5.10)
    c.site("jp_s_oke_tarai", 0.70, -4.95, 0, why="a wash tub in the back yard")


def edo_sakaya(c):
    """Edo 3-ken corner unit (T3), a sake shop (sakaya): casks on a rack, a cask on the floor, flasks, measures."""
    _tori_3k(c)
    c.free("toriniwa", "jp_f_oke_bucket", 2.40, 2.55, 15, why="bucket by the entrance")
    c.free("toriniwa", "jp_f_taru_komo", 2.40, -1.25, 0, why="a straw-wrapped cask waiting by the passage")
    c.hang("toriniwa", "jp_f_chochin_shop", 1.79, 2.40, LOFT_CEIL, why="the shop lantern")
    # ---------------------------------------------------------------- mise (shop: sake)
    r = c.wall("mise", "xmin", 2.60, "jp_f_taru_rack3", why="three casks on their rack against the side wall")
    c.free("mise", "jp_f_taru_komo", 0.30, 3.20, 0, why="a straw-wrapped cask")
    c.free("mise", "jp_f_taru_cask", -0.30, 3.25, 12, why="a plain cask")
    d = c.free("mise", "jp_f_zukue_choba", -1.45, 3.05, 180, why="the account desk, its back to the lattice")
    c.free("mise", "jp_f_choba_set_zenibako", -0.72, 3.35, 15, why="the coin box")
    c.free("mise", "jp_f_masu_spilled", -1.10, 2.05, 20, why="a sake measure knocked over (disorder)")
    c.surf(r, "jp_f_tokkuri_pair", surface="top1", why="two flasks on the middle cask")
    c.surf(d, "jp_f_masu_set", why="measures on the desk")
    c.onwall("mise", "zmin", -2.35, "jp_f_kamidana_plain", why="god shelf, undisturbed")
    # ---------------------------------------------------------------- oku (heavier disorder)
    c.wall("oku", "xmin", -0.80, "jp_f_futon_laid", why="bedding laid out along the side wall, under the window")
    c.wall("oku", "zmin", -0.90, "jp_f_tansu", why="the chest of drawers against the back wall")
    c.free("oku", "jp_f_andon_kaku", 0.35, 0.15, 0, why="standing lamp, unlit")
    c.wall("oku", "xmin", 0.55, "jp_f_butsudan_lacquer", why="lacquered Buddhist altar, undisturbed")
    c.free("oku", "jp_f_enza_zabuton", -1.40, 0.35, 15, why="a cushion (T3)")
    c.free("oku", "jp_f_clothes_kimono", -0.25, 0.15, 40, why="a kimono pulled out and dropped (disorder)")
    c.hang("oku", "jp_f_kaya_bundle", -2.35, -1.40, LOFT_CEIL, over="corner", why="the mosquito net folded away")
    _kitchen_3k(c, pots=("jp_f_kama", "jp_f_kama_nolid"), extra="jp_f_taru_cask")
    c.free("kitchen", "jp_f_kama_lid", 0.30, -2.35, 25, count=False, why="the second pot's lid on the doma")
    c.front("jp_s_shopfront_noren_long", 1.91, 3.96, 0.10, why="long noren on the entrance")
    c.front("jp_s_shopfront_kanban_hang", -2.45, 4.05, 0.0, why="hanging signboard at the corner")
    c.site("jp_s_gutter_slab", 1.91, 5.10, 0, why="stone slab over the gutter at the door")
    _gutters(c, (-1.82, 0.00), 5.10)
    c.site("jp_s_fire_tub_open", -4.55, 3.40, 90, why="the corner fire tub on the side street, its bucket "
           "pyramid fallen")
    c.site("jp_s_oke_taru_lid", 1.50, -4.60, 0, why="an empty cask by the back door")


def posttown_home(c):
    """Tokaido post-town house, home side (T2): living room with the loom work, the best room, a farm-style kitchen."""
    _tori_3k(c)
    c.free("toriniwa", "jp_f_oke_bucket", 2.40, 2.55, 15, why="bucket by the entrance")
    c.free("toriniwa", "jp_f_basket_back", 2.40, -1.25, 0, why="a back basket set down by the passage")
    c.onwall("toriniwa", "xmax", 2.30, "jp_f_mino_pegs_rain", why="straw raincoat and hat on the pegs")
    # ---------------------------------------------------------------- mise = living (T2)
    ts = c.wall("mise", "xmin", 2.90, "jp_f_tansu", why="a chest of drawers against the side wall")
    c.free("mise", "jp_f_basket_back", -2.30, 1.75, 0, why="a back basket set down")
    c.free("mise", "jp_f_hibachi_box", -0.90, 2.55, 0, why="box brazier")
    c.free("mise", "jp_f_meal_left_two", -0.40, 1.90, 10, why="a meal for two left half eaten")
    c.free("mise", "jp_f_enza", -1.35, 2.20, 0, why="straw cushion (T2)")
    c.free("mise", "jp_f_itoguruma_thread", 0.20, 3.10, 0, why="the spinning wheel, thread still on it")
    c.surf(ts, "jp_f_sewing_box", why="sewing box on the chest")
    c.onwall("mise", "zmin", -2.30, "jp_f_kamidana_plain", why="god shelf, undisturbed")
    c.onwall("mise", "zmin", -1.95, "jp_f_kamidana_set_shimenawa_old", why="the old rope of the god shelf")
    c.onwall("mise", "xmax", 3.10, "jp_f_koyomi_curled", why="last year's calendar, curling")
    # ---------------------------------------------------------------- oku (T2 best room)
    c.wall("oku", "zmin", -1.20, "jp_f_nagamochi", why="the long chest against the back wall")
    c.free("oku", "jp_f_futon_laid", -1.25, -0.25, 0, why="bedding laid out as it was left")
    c.wall("oku", "xmin", 0.45, "jp_f_butsudan_plain", why="plain Buddhist altar, undisturbed")
    c.free("oku", "jp_f_andon_ariake", -2.35, 0.00, 0, why="night lamp by the altar, unlit")
    c.free("oku", "jp_f_sewing_work", 0.20, 0.30, 20, why="a half-sewn garment on the mats")
    c.hang("oku", "jp_f_hoshigaki_3", -1.20, -0.30, LOFT_CEIL, over="furniture", why="persimmons drying from the "
           "joists over the bedding (autumn)")
    _kitchen_3k(c)
    c.front("jp_s_shopfront_noren_half", 1.94, 3.96, 0.0, why="half noren on the entrance")
    c.eaves("jp_s_sandals_sale_eave", -1.60, 3.90, 0, 2.85, why="straw sandals hung for sale under the eave")
    c.site("jp_s_bench_1ken", -1.30, 4.60, 0, why="a bench under the eave")
    c.site("jp_s_gutter_slab", 1.94, 5.40, 0, why="stone slab over the gutter at the door")
    _gutters(c, (-1.82, 0.00), 5.40)
    c.site("jp_s_oke_tarai", 1.60, -4.75, 0, why="wash tub by the back door")


# ================================================================================================ inns
def _inn_tori(c):
    c.wall("toriniwa", "xmax", 1.20, "jp_f_tana_091_1", why="shelf on the gable wall")
    c.free("toriniwa", "jp_f_oke_bucket", 4.20, 3.55, 10, why="the foot-wash bucket by the entrance")
    c.free("toriniwa", "jp_f_debris_straw", 3.50, 1.80, 30, why="straw tracked in")
    c.free("toriniwa", "jp_f_debris_leaves", 3.70, 4.00, 20, why="leaves blown in")
    c.free("toriniwa", "jp_f_basket_back", 4.20, -0.40, 0, why="a porter's back basket left by the passage")
    c.onwall("toriniwa", "xmax", 3.40, "jp_f_sandals_hung_wall", why="spare straw sandals for guests")


def _inn_office(c, tier):
    d = c.wall("mise", "zmin", -3.45, "jp_f_zukue_choba", why="the chōba desk in the office corner")
    c.free("mise", "jp_f_choba_goshi_3", -3.50, 2.75, 0, why="the counting-desk lattice")
    c.free("mise", "jp_f_choba_set_zenibako", -4.20, 2.10, 10, why="the coin box")
    c.free("mise", "jp_f_hibachi_box", -2.40, 2.80, 0, why="box brazier by the chōba")
    c.free("mise", "jp_f_byobu_tsuitate", 1.95, 3.60, 90, why="the entrance screen facing the toriniwa door")
    c.free("mise", "jp_f_tabakobon_spilled", -2.00, 3.40, 30, why="the tobacco tray knocked over (disorder)")
    c.free("mise", "jp_f_enza_zabuton" if tier >= 3 else "jp_f_enza", -2.80, 3.60, 0, why="a cushion")
    c.surf(d, "jp_f_choba_set_desk", why="the guest register, ledgers and abacus")
    c.onwall("mise", "zmin", -3.00 if tier >= 3 else -1.50, "jp_f_kamidana_plain",
             why="god shelf over the office, undisturbed")
    c.onwall("mise", "xmin", 3.20, "jp_f_koyomi", why="this year's calendar")


def _inn_kitchen(c):
    c.kamado("kitchen", (-3.95, -1.70, -4.46, -3.76), "+z", n=3)
    c.pot("kitchen", "jp_f_kama", 0, why="rice pot")
    c.pot("kitchen", "jp_f_kama_nolid", 1, why="a pot, lid off")
    c.pot("kitchen", "jp_f_seiro_kama3", 2, why="a steamer stack")
    c.free("kitchen", "jp_f_kama_lid", -0.90, -3.30, 20, count=False, why="the lid on the doma")
    c.wall("kitchen", "zmin", 0.00, "jp_f_nagashi_wood", why="the sink against the back wall")
    c.free("kitchen", "jp_f_mizugame", 0.95, -4.10, 0, why="water jar beside the sink")
    sh = c.wall("kitchen", "zmax", -2.50, "jp_f_tana_182_3", why="two-board shelf on the omoya wall")
    c.wall("kitchen", "xmin", -2.30, "jp_f_taru_rack3", why="soy and sake casks on a rack")
    c.surf(sh, "jp_f_tableware_hakozen_stack", surface="board_1", why="guests' box trays stacked")
    c.surf(sh, "jp_f_tableware_bowls", surface="board_2", why="bowls")
    c.onwall("kitchen", "zmin", 1.60, "jp_f_utensil_board", why="ladles and knives on the wall")
    c.passage(("toriniwa", "kitchen"), c.info_passage[0], c.info_passage[1], "passage toriniwa <-> kitchen")


def inn_std(c):
    """Ordinary inn (hatago, T2 post town): the office with the chōba, two guest rooms, the big kitchen."""
    _inn_tori(c)
    _inn_office(c, 2)
    # ---------------------------------------------------------------- oku: guest room
    c.free("oku", "jp_f_futon_laid", 0.90, -0.35, 0, why="a guest's rented bedding, laid out as left")
    c.free("oku", "jp_f_andon_kaku", -0.55, 1.20, 0, why="standing lamp, unlit")
    c.free("oku", "jp_f_hibachi_box", 1.80, 0.95, 0, why="brazier")
    c.free("oku", "jp_f_tabakobon", 1.40, 1.00, 15, why="tobacco tray")
    c.free("oku", "jp_f_meal_left_zen", 0.20, 0.45, 10, why="a guest's tray meal left half eaten")
    c.hang("oku", "jp_f_kaya_bundle", 2.35, 1.45, LOFT_CEIL, over="corner", why="the rented net folded away (autumn)")
    # ---------------------------------------------------------------- oku2: guest room
    c.wall("oku2", "zmax", -2.70, "jp_f_futon_laid", why="bedding laid out")
    c.free("oku2", "jp_f_kori", -3.90, -0.50, 20, why="a traveller's wicker trunk")
    c.free("oku2", "jp_f_andon_ariake", -1.70, 1.35, 0, why="night lamp, unlit")
    c.free("oku2", "jp_f_meal_left_two", -2.80, 0.00, 10, why="two trays left")
    c.free("oku2", "jp_f_enza", -2.00, 0.25, 0, why="straw cushion")
    c.hang("oku2", "jp_f_kaya_bundle", -4.20, 1.40, LOFT_CEIL, over="corner", why="the net folded away (autumn)")
    _inn_kitchen(c)
    c.front("jp_s_shopfront_noren_long", 3.76, 4.87, 0.10, why="long noren on the entrance")
    c.front("jp_s_lantern_sign_chochin_inn", 2.30, 4.90, 0.0, why="the inn's lantern")
    c.eaves("jp_s_sandals_sale_eave", -1.20, 4.80, 0, 2.85, why="straw sandals for sale under the eave")
    c.site("jp_s_bench_long", -2.70, 5.45, 0, why="the guests' bench under the eave")
    c.site("jp_s_gutter_slab", 3.76, 6.20, 0, why="slab over the gutter at the door")
    _gutters(c, (-3.64, -1.82, 0.0, 1.82), 6.20)
    c.site("jp_s_firewood_stack_wall_1ken_h120", -2.73, -5.00, 180, why="firewood against the kitchen wall")


def inn_grand(c):
    """Grand inn (T3): office, the stair hall (oku), the kitchen, two guest rooms upstairs (G1 A1-3)."""
    _inn_tori(c)
    _inn_office(c, 3)
    st = c.stairs[0]
    xf = st["foot"][0]
    c.band_block("oku", (min(xf, xf + st["dir"] * st["run"]), max(xf, xf + st["dir"] * st["run"]),
                         st["foot"][1], st["foot"][1] + st["width"]))
    c.passage(("oku",), xf + 0.55, st["foot"][1] + 0.55, "stair foot")
    # ---------------------------------------------------------------- oku (the stair hall)
    ts = c.wall("oku", "xmin", 0.90, "jp_f_tansu", why="chest of drawers")
    c.free("oku", "jp_f_hibachi_box", -3.30, 0.60, 0, why="box brazier")
    c.free("oku", "jp_f_andon_kaku", -4.20, -0.60, 0, why="standing lamp, unlit")
    c.free("oku", "jp_f_enza_zabuton", -3.30, 1.25, 0, why="a cushion (T3)")
    c.free("oku", "jp_f_tabakobon", -2.70, 1.25, 10, why="tobacco tray")
    c.surf(ts, "jp_f_tea_dobin", why="clay tea pot (T3 marker)")
    # ---------------------------------------------------------------- upstairs front: guest room
    c.free("nikai_front", "jp_f_futon_laid", -3.20, 2.55, 0, why="a guest's bedding laid out")
    c.free("nikai_front", "jp_f_futon_laid_dragged", 3.00, 2.70, 0, why="bedding dragged half off (disorder)")
    c.free("nikai_front", "jp_f_andon_kaku", -1.80, 2.30, 0, why="standing lamp, unlit")
    c.free("nikai_front", "jp_f_hibachi_round", 0.50, 3.40, 0, why="round brazier")
    c.free("nikai_front", "jp_f_meal_left_two", -0.40, 3.35, 0, why="two trays left")
    c.free("nikai_front", "jp_f_kori", 4.05, 3.75, 90, why="a traveller's trunk")
    # ---------------------------------------------------------------- upstairs back: guest room + the stairwell
    well = c.stairs[0]["well"]
    c.band_block("nikai_back", well)
    head_x = xf + st["dir"] * st["run"]
    c.passage(("nikai_back",), head_x - 0.55 if st["dir"] < 0 else head_x + 0.55, st["foot"][1] + 0.55, "stair head")
    ts2 = c.wall("nikai_back", "xmax", 0.60, "jp_f_tansu_single", why="a low chest")
    c.free("nikai_back", "jp_f_futon_stack", 3.60, -0.40, 0, why="bedding folded in the corner")
    c.free("nikai_back", "jp_f_hibachi_box", 2.00, 1.20, 0, why="brazier")
    c.free("nikai_back", "jp_f_andon_ariake", 3.20, 1.30, 0, why="night lamp, unlit")
    c.free("nikai_back", "jp_f_goban_go_scattered", 2.10, -0.20, 20, why="a go board, stones scattered")
    c.free("nikai_back", "jp_f_enza_zabuton", 1.40, 0.35, 10, why="a cushion (T3)")
    c.surf(ts2, "jp_f_tea_matcha", why="a tea bowl and caddy (T3 marker)")
    _inn_kitchen(c)
    c.front("jp_s_shopfront_noren_long", 3.76, 4.87, 0.10, why="long noren on the entrance")
    c.front("jp_s_lantern_sign_chochin_inn", 2.30, 4.90, 0.0, why="the inn's lantern")
    c.site("jp_s_shopfront_kanban_stand", -3.60, 5.30, 0, why="a standing signboard")
    c.site("jp_s_bench_ab_tipped", -1.80, 5.40, 180, why="a bench tipped over")
    c.site("jp_s_gutter_slab", 3.76, 6.20, 0, why="slab over the gutter at the door")
    _gutters(c, (-3.64, -1.82, 0.0, 1.82), 6.20)
    c.site("jp_s_firewood_stack_wall_1ken_h120", -2.73, -5.00, 180, why="firewood against the kitchen wall")


# ================================================================================================ rural (C2)
def _kamado_on_spot(c, room, n=2):
    f = c.fit(room, "kamado")[0]
    (cx, cz), yaw, (w, d) = f["centre"], f["yaw"], f["size"]
    if round(yaw) % 180 == 0:
        rect = (cx - w / 2, cx + w / 2, cz - d / 2, cz + d / 2)
    else:
        rect = (cx - d / 2, cx + d / 2, cz - w / 2, cz + w / 2)
    mouth = {0: "+z", 90: "+x", 180: "-z", 270: "-x"}[int(round(yaw)) % 360]
    return c.kamado(room, rect, mouth, n=n)


def _irori(c, room, jizai="jp_f_jizai_kagi", pot=None):
    f = c.fit(room, "irori")[0]
    hx, hy, hz = f["hook"]
    c.hang(room, jizai, hx, hz, hy, over="hearth", why="the pot hook over the irori")
    return f


def farm_kanto(c):
    """Kanto farmhouse with the inside stable (T2): the doma with the stove and the stall, the hiroma round the irori,
    the dei best room, the nando."""
    # ---------------------------------------------------------------- doma
    _kamado_on_spot(c, "doma", 2)
    c.pot("doma", "jp_f_kama", 0, why="rice pot")
    c.pot("doma", "jp_f_kama_nolid", 1, why="a pot, lid off")
    c.free("doma", "jp_f_manger_trough", 4.90, -4.22, 0, why="the manger in the stable")
    c.free("doma", "jp_f_manger_straw_rotted", 5.20, -2.90, 20, why="the horse's straw, rotting")
    c.free("doma", "jp_f_usu", 2.00, -0.40, 0, why="the rice mortar")
    c.wall("doma", "zmax", 5.30, "jp_f_tawara_stack6", why="the year's rice bales stacked by the door")
    c.free("doma", "jp_f_mi_spilled", 2.60, 1.20, 30, why="a winnowing basket dropped, chaff spilled (disorder)")
    c.onwall("doma", "xmax", 2.40, "jp_f_mino_pegs_rain", why="straw raincoat and hat on the end wall")
    c.onwall("doma", "zmin", 1.40, "jp_f_tool_wall", why="farm tools on pegs by the back door")
    c.passage(("doma", "hiroma"), 0.91, 1.82, "kamachi step doma <-> hiroma")
    # ---------------------------------------------------------------- hiroma (daidokoro, irori)
    f = _irori(c, "hiroma")
    hx, hy, hz = f["hook"]
    c.hang("hiroma", "jp_f_hoshigaki_5", hx, 2.00, hy, over="hearth", why="persimmons drying over the smoke "
           "(autumn)")
    c.hang("hiroma", "jp_f_drying_daikon", hx, -2.00, hy, why="daikon drying on the tie beam")
    tn = c.wall("hiroma", "zmax", -1.00, "jp_f_tana_136_1", why="a plank shelf on the front wall")
    c.free("hiroma", "jp_f_andon_kaku", -2.30, -0.50, 0, why="standing lamp, unlit")
    c.free("hiroma", "jp_f_kama_nabe_rusted", 0.10, -0.90, 0, why="a pot left by the hearth, rusting")
    c.free("hiroma", "jp_f_meal_left_hakozen", -0.90, 1.20, 0, why="a box-tray meal by the hearth")
    c.free("hiroma", "jp_f_enza", -1.90, 0.00, 0, why="straw cushion")
    c.free("hiroma", "jp_f_mushiro", -1.80, 2.80, 5, why="a straw mat over the boards")
    c.surf(tn, "jp_f_tableware_hakozen_stack", why="box trays stacked on the shelf")
    c.onwall("hiroma", "zmin", -2.10, "jp_f_butsudan_shelf", why="the Buddhist shelf, undisturbed")
    c.onwall("hiroma", "zmax", 0.20, "jp_f_kamidana_plain", why="god shelf, undisturbed")
    # ---------------------------------------------------------------- dei (T2 best room)
    c.wall("dei", "xmin", 2.50, "jp_f_nagamochi", why="the long chest against the end wall")
    c.wall("dei", "zmin", -4.50, "jp_f_tansu_single", why="a low chest")
    c.free("dei", "jp_f_andon_kaku", -3.40, 3.80, 0, why="standing lamp, unlit")
    c.free("dei", "jp_f_box_m_lacquer", -5.00, 3.95, 10, why="a box of lacquered festival trays")
    c.free("dei", "jp_f_enza_stack3", -4.20, 2.20, 0, why="straw cushions stacked")
    c.onwall("dei", "xmin", 0.90, "jp_f_koyomi_curled", why="an old calendar curling on the end wall")
    # ---------------------------------------------------------------- nando (sleeping)
    c.wall("nando", "zmax", -4.90, "jp_f_futon_laid", why="bedding laid out")
    c.wall("nando", "xmin", -3.60, "jp_f_iko_plain", why="a clothes rack")
    c.free("nando", "jp_f_kori_open", -4.00, -3.85, 0, why="a wicker trunk, lid off (disorder)")
    c.free("nando", "jp_f_itoguruma", -5.30, -1.40, 0, why="the spinning wheel")
    c.free("nando", "jp_f_andon_ariake", -3.30, -0.55, 0, why="night lamp, unlit")
    c.onwall("nando", "zmin", -3.30, "jp_f_bangasa_hung", why="an oiled umbrella hung on the back wall")
    # ---------------------------------------------------------------- outside
    c.eaves("jp_s_kaki_curtain_1ken", -1.00, 4.66, 0, 3.10, why="persimmon curtain under the front eave")
    c.site("jp_s_farm_tools_lean", 5.60, 5.10, 0, why="hoe, sickle and rake leaned by the door")
    c.site("jp_s_charcoal_bales_stack", -1.20, -5.10, 180, why="charcoal bales stacked by the back wall")


def farm_kinai(c):
    """Kinai farmhouse with the ox (T2): the niwa with the stove and the ox stall, the mise (cotton work), the
    daidokoro round the irori, the zashiki, the nando."""
    _kamado_on_spot(c, "niwa", 2)
    c.pot("niwa", "jp_f_kama", 0, why="rice pot")
    c.pot("niwa", "jp_f_seiro_kama2", 1, why="a steamer stack")
    c.free("niwa", "jp_f_manger_trough_empty", -5.34, -3.30, 0, why="the ox's manger, empty")
    c.free("niwa", "jp_f_manger_straw_rotted", -5.30, -2.00, 15, why="the ox's straw, rotting")
    c.free("niwa", "jp_f_usu_ishiusu", -2.20, 0.40, 0, why="the stone hand mill")
    c.free("niwa", "jp_f_mi", -3.00, -1.10, 20, why="a winnowing basket")
    c.free("niwa", "jp_f_mizugame", -5.70, 0.40, 0, why="the water jar by the stove")
    c.onwall("niwa", "zmin", -4.10, "jp_f_rope_pegs_3", why="rope coils on the back wall by the stall")
    c.passage(("niwa", "mise"), -0.91, 1.82, "kamachi step niwa <-> mise")
    c.passage(("niwa", "daidokoro"), -0.91, -1.82, "kamachi step niwa <-> daidokoro")
    # ---------------------------------------------------------------- mise (living, cotton work)
    c.wall("mise", "zmax", 1.90, "jp_f_izaribata", why="the ground loom with cotton on it (Kawachi cotton)")
    c.free("mise", "jp_f_box_l", 0.35, 2.30, 0, why="a lidded box of cotton")
    c.free("mise", "jp_f_andon_kaku", -0.40, 3.20, 0, why="standing lamp, unlit")
    c.free("mise", "jp_f_enza", 1.20, 1.40, 0, why="straw cushion")
    c.free("mise", "jp_f_mushiro", 0.80, 0.90, 0, why="a straw mat over the boards")
    c.onwall("mise", "zmax", -0.30, "jp_f_kamidana_plain", why="god shelf, undisturbed")
    # ---------------------------------------------------------------- daidokoro (irori)
    f = _irori(c, "daidokoro", jizai="jp_f_jizai_kagi_abandoned")
    hx, hy, hz = f["hook"]
    c.hang("daidokoro", "jp_f_drying_chilli", hx, -0.90, hy, why="chillies drying on the tie beam (autumn)")
    tn = c.wall("daidokoro", "zmin", 0.00, "jp_f_tana_136_1", why="a plank shelf on the back wall")
    c.free("daidokoro", "jp_f_kama_nabe", 0.00, -1.00, 0, why="a pot by the hearth")
    c.free("daidokoro", "jp_f_enza", 2.00, -0.80, 0, why="straw cushion")
    c.free("daidokoro", "jp_f_tableware_scattered", 1.90, -2.90, 20, why="bowls scattered (disorder)")
    c.free("daidokoro", "jp_f_charcoal_scuttle", -0.30, -2.90, 0, why="the charcoal scuttle")
    c.surf(tn, "jp_f_tableware_bowls", why="bowls on the shelf")
    c.onwall("daidokoro", "xmax", -0.60, "jp_f_butsudan_shelf", why="the Buddhist shelf, undisturbed")
    # ---------------------------------------------------------------- zashiki (T2 best room)
    ts = c.wall("zashiki", "xmax", 1.80, "jp_f_tansu", why="chest of drawers")
    c.free("zashiki", "jp_f_andon_kaku", 3.50, 0.50, 0, why="standing lamp, unlit")
    c.free("zashiki", "jp_f_box_m_lacquer", 5.60, 0.40, 0, why="a box of lacquered trays")
    c.free("zashiki", "jp_f_enza_stack3", 4.40, 1.80, 0, why="straw cushions stacked")
    c.free("zashiki", "jp_f_byobu_makura", 4.40, 2.95, 0, why="a low screen")
    c.surf(ts, "jp_f_masu_set", why="measures on the chest")
    c.onwall("zashiki", "xmin", 3.00, "jp_f_koyomi", why="this year's calendar")
    # ---------------------------------------------------------------- nando
    c.wall("nando", "zmax", 4.60, "jp_f_futon_laid", why="bedding laid out")
    c.wall("nando", "xmax", -2.40, "jp_f_nagamochi", why="the long chest")
    c.free("nando", "jp_f_andon_ariake", 3.40, -2.60, 0, why="night lamp, unlit")
    c.free("nando", "jp_f_kori_2", 4.20, -3.20, 0, why="two wicker trunks")
    c.free("nando", "jp_f_clothes_haori", 3.80, -1.80, 30, why="a jacket dropped on the floor")
    c.onwall("nando", "zmax", 6.00, "jp_f_bangasa_hung", why="an oiled umbrella on the partition")
    c.eaves("jp_s_kaki_curtain_half", 1.20, 3.72, 0, 2.95, why="persimmons under the lower roof")
    c.site("jp_s_farm_tools_pair", -1.80, 4.10, 0, why="tools leaned by the door")


def _hut_living(c, bed_side, bed_at, bed="jp_f_straw_bed_quilt", yaw_extra=0.0):
    f = _irori(c, "living", jizai="jp_f_jizai_kagi_plain_abandoned")
    c.wall("living", bed_side, bed_at, bed, yaw_extra=yaw_extra, why="the straw bed (T1: no tatami, no futon)")
    return f


def hut_east(c):
    """Poor hut east, large, board floor (T1): sparse. A one-mouth stove, a straw bed, the irori."""
    _kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama_nolid", 0, why="the pot left in the stove")
    c.free("doma", "jp_f_jar_l", -1.40, -2.20, 0, why="the water jar, lid on")
    c.free("doma", "jp_f_oke_tarai_dry", -1.60, -1.10, 20, why="a dry wash tub")
    c.free("doma", "jp_f_firewood_bundle", -3.00, 0.10, 90, why="a bundle of brushwood")
    c.free("doma", "jp_f_straw_work_scattered", -2.10, 1.30, 15, why="straw work left scattered")
    c.onwall("doma", "xmin", 1.10, "jp_f_mino_pegs", why="raincoat, hat and tools on the pegs")
    c.passage(("doma", "living"), -0.91, 0.35, "kamachi step doma <-> living")
    f = _hut_living(c, "zmin", 1.30)
    hx, hy, hz = f["hook"]
    c.hang("living", "jp_f_hoshigaki_5", hx, -2.20, hy, over="furniture", why="persimmons drying over the bed")
    c.free("living", "jp_f_kama_nabe_rusted", 0.90, 0.60, 0, why="a rusting pot by the hearth")
    c.free("living", "jp_f_meal_left_hakozen", 1.80, 1.10, 0, why="a box-tray meal left")
    c.free("living", "jp_f_mushiro_torn", 0.20, 1.60, 10, why="a torn straw mat over the boards")
    c.free("living", "jp_f_basket_kago", -0.40, -1.80, 0, why="a basket")
    c.onwall("living", "zmax", 0.60, "jp_f_butsudan_shelf_dusty", why="a small Buddhist shelf, dusty, undisturbed")


def hut_west(c):
    """Poor hut west with its lean-to (T1): woodshed, one-mouth stove, straw bed round the irori."""
    c.wall("leanto", "xmin", 0.60, "jp_f_firewood_stack", why="split wood in the lean-to")
    c.free("leanto", "jp_f_basket_back", -3.60, -1.10, 0, why="a back basket")
    c.free("leanto", "jp_f_usu", -3.55, 0.90, 0, why="a wooden mortar")
    c.free("leanto", "jp_f_straw_work_beating", -3.40, -0.10, 30, why="straw beaten for rope and sandals")
    c.free("leanto", "jp_f_mushiro_pile", -3.20, -1.20, 0, count=True, why="old straw mats piled")
    c.onwall("leanto", "xmax", 0.30, "jp_f_tool_wall_wood", why="axe, hatchet and saw on pegs on the gable")
    _kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama_nolid", 0, why="the pot left in the stove")
    c.free("doma", "jp_f_jar_l", -1.30, -1.35, 0, why="the water jar")
    c.free("doma", "jp_f_oke_bucket", -2.30, 0.70, 0, why="a bucket")
    c.free("doma", "jp_f_debris_straw", -1.90, 0.00, 60, why="straw litter")
    c.free("doma", "jp_f_straw_work_sandal", -2.10, 1.20, 10, why="a half-made sandal")
    c.onwall("doma", "xmin", 0.40, "jp_f_mino_pegs_rain", why="raincoat and hat on the pegs")
    c.passage(("doma", "living"), -0.91, 0.0, "kamachi step doma <-> living")
    f = _hut_living(c, "xmax", 0.0, bed="jp_f_straw_bed_pile")
    c.free("living", "jp_f_kama_nabe", 0.20, 0.90, 0, why="a pot by the hearth")
    c.free("living", "jp_f_meal_left_hakozen", 0.40, -1.20, 0, why="a box-tray meal left")
    c.free("living", "jp_f_mushiro", 0.30, 1.35, 0, why="a straw mat")
    c.free("living", "jp_f_itoguruma", -0.20, -1.35, 0, why="the spinning wheel")
    hx, hy, hz = f["hook"]
    c.hang("living", "jp_f_drying_daikon_shrivelled", hx, 1.30, hy, over="corner", why="daikon drying, shrivelled")


def shed_barn(c):
    """Walled shed with the woodshed lean-to (T1-2): straw, bales, the sieve and winnow, a rack of tools."""
    c.wall("floor", "zmin", -1.40, "jp_f_rack_1ken", why="shelving along the back wall")
    c.wall("floor", "xmin", 0.60, "jp_f_tawara_stack6", why="rice bales against the end wall")
    c.free("floor", "jp_f_tawara_kamasu_stack3", 1.90, 0.60, 10, why="sacks of grain")
    c.free("floor", "jp_f_usu_mallet", 1.60, -0.80, 0, why="mortar and pounder")
    c.free("floor", "jp_f_mi_spilled", -0.50, 0.40, 30, why="a winnow dropped, chaff spilled")
    c.free("floor", "jp_f_basket_back_crushed", -0.60, -0.60, 0, why="a crushed back basket")
    c.onwall("floor", "zmin", 1.60, "jp_f_mi_wall", why="the winnowing basket hung up")
    c.onwall("floor", "xmax", -0.60, "jp_f_rope_pegs_2", why="rope coils")
    c.wall("leanto", "xmax", 0.70, "jp_f_firewood_stack", why="split wood")
    c.wall("leanto", "xmax", -0.40, "jp_f_firewood_stack", why="split wood")
    c.free("leanto", "jp_f_debris_straw", 3.40, -1.00, 40, why="straw and bark litter")
    c.free("leanto", "jp_f_charcoal_bale", 3.30, 1.20, 0, why="a charcoal bale")
    c.free("leanto", "jp_f_debris_leaves", 3.40, 0.10, 30, why="leaves blown in")


def kura_storage(c):
    """Kura (storage): chests, bales, boxes and racks on two floors; the stair foot / head and the door kept clear."""
    st = c.stairs[0]
    x0 = st["foot"][0]
    c.band_block("kura", (x0, x0 + st["run"], st["foot"][1], st["foot"][1] + st["width"]))
    c.passage(("kura",), x0 - 0.50, st["foot"][1] + 0.55, "stair foot")
    c.band_block("nikai", st["well"])
    c.passage(("nikai",), x0 + st["run"] + 0.45, st["foot"][1] + 0.55, "stair head")
    # ground floor (the stair along the back wall; the door and its parked leaf on the front)
    c.wall("kura", "xmax", 0.00, "jp_f_nagamochi", why="a long chest against the gable")
    ts = c.wall("kura", "zmax", -1.90, "jp_f_tansu", why="a chest of drawers against the front wall")
    c.free("kura", "jp_f_box_stack3", -1.20, 0.90, 0, why="lidded boxes stacked")
    c.free("kura", "jp_f_tawara_stack6", 0.90, 0.60, 0, why="rice bales")
    c.free("kura", "jp_f_kori_2", -2.15, 0.90, 0, why="wicker trunks")
    c.surf(ts, "jp_f_writing_box", why="a writing box left on the chest")
    # upper floor (the stairwell along the back wall)
    c.wall("nikai", "zmax", -1.30, "jp_f_nagamochi_open", why="a long chest, lid thrown back (disorder)")
    c.wall("nikai", "zmax", 1.30, "jp_f_rack_1ken", why="shelving")
    c.free("nikai", "jp_f_box_stack3_toppled", -2.10, -0.30, 0, why="a stack of boxes toppled")
    c.free("nikai", "jp_f_kori_open", 0.90, 0.90, 0, why="a wicker trunk, open")
    c.free("nikai", "jp_f_box_l", -2.20, -1.25, 0, why="a big box")


SETS = {
    "kamigata_komeya": {"tier": 3, "fn": kamigata_komeya},
    "kamigata_kamiya": {"tier": 3, "fn": kamigata_kamiya},
    "edo_gofuku": {"tier": 3, "fn": edo_gofuku},
    "edo_sakaya": {"tier": 3, "fn": edo_sakaya},
    "posttown_home": {"tier": 2, "fn": posttown_home},
    "inn_std": {"tier": 2, "fn": inn_std},
    "inn_grand": {"tier": 3, "fn": inn_grand},
    "farm_kanto": {"tier": 2, "fn": farm_kanto},
    "farm_kinai": {"tier": 2, "fn": farm_kinai},
    "hut_east": {"tier": 1, "fn": hut_east},
    "hut_west": {"tier": 1, "fn": hut_west},
    "shed_barn": {"tier": 1, "fn": shed_barn},
    "kura_storage": {"tier": 2, "fn": kura_storage},
}

# S1 (2026-09-30): the KEEP_TRADES shop sets (buildings/shop_sets.py): shop_<trade>_<3k|2k>_ab<0-2>
import shop_sets as _shop  # noqa: E402

SETS.update(_shop.sets())
