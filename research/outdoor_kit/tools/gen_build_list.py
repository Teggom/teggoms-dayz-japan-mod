"""Generates the outdoor core-kit build list (JSON + MD), the materials list, the refs index and CREDITS.md from ONE
data source, so the markdown and the JSON always say the same thing (BUILD_LIST_TEMPLATE rule).

Run:  python research/outdoor_kit/tools/gen_build_list.py
Reads: data/research_okit/meta.json (this list's download log), data/research_ext/meta.json (exterior refs reused),
       playbook/refs_index.json and playbook/palette.json (id checks), research/outdoor/OUTDOOR_LIST.md §4 (settings),
       playbook/templates/build_list_schema.json (validation, if jsonschema is installed; a built-in check otherwise)
Writes (binary, LF): research/outdoor_kit/build_list.json, materials_needed.json, refs_index.json, BUILD_LIST.md,
       CREDITS.md
Research agent PA3 (task A3), 2026-09-29.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'outdoor_kit')
DATE = '2026-09-29'
AUTHOR = 'research agent PA3 (A3)'

def D(v, src=None, why=None):
    d = {'value': v}
    if src: d['source'] = src
    if why: d['assumed'] = True; d['reason'] = why
    return d

def R(i, shows, period=False):
    return {'id': i, 'shows': shows, 'period_image': period}

def M(surface, material, pal):
    return {'surface': surface, 'material': material, 'palette_id': pal}

def V(i, how, tier=None):
    v = {'id': i, 'differs_by': how}
    if tier: v['tier'] = tier
    return v

CK_STONE = ['C1', 'C2', 'C4', 'C5', 'C6', 'C8', 'C9']
CK_PROP = ['C1', 'C2', 'C4', 'C5', 'C6', 'C8']

# ------------------------------------------------------------------------------------------------ entries
E = []
def add(group, **k):
    k['_group'] = group
    k.setdefault('checks', CK_PROP)
    k.setdefault('region', 'all')
    k.setdefault('status_overlay', 'commoner')
    E.append(k)

# ================================================================= YARD AND FARM
add('Yard and farm', id='jp_s_firewood_stack', name='Firewood stack (maki-zumi) and brushwood bundles (soda)',
    what='Split billets stacked against an eave wall or free-standing between posts, plus tied brushwood bundles: the most-placed outdoor object in every setting.',
    importance='filler', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.3,
    period_evidence='firewood and brushwood are the universal fuel; charcoal and firewood trade in towns [OUTDOOR_LIST §2 R §6 / W §8, S108]; stacked firewood under eaves in a CC BY photo of a Tohoku farmyard with persimmons drying [k35] (modern, form only)',
    refs=[R('k35_firewood_hoshigaki', 'billets stacked under an eave with persimmons drying above (autumn yard; modern photo, form only)'),
          R('k36_firewood_motai', 'firewood wall along a Nakasendo post-town house (modern photo, form only)'),
          R('c05_ouchi_thatch', 'thatched post town: where stacks sit against the walls', False)],
    dimensions={
        'billet_length_m': D('0.30-0.36 (1 shaku to 1.2 shaku)', None, 'kitchen-fire billets are cut to about one shaku so they fit a kamado mouth; no period measurement found'),
        'billet_diameter_m': D('0.06-0.14, split halves and quarters', None, 'read off k35/k36; random per billet (W8)'),
        'stack_module_m': D('1 ken long (1.82) x 1.2 or 1.8 high x 1 billet deep; half-ken (0.91) end module', None, 'snaps to the house grid (PLAYBOOK rule 9) so a stack fills a wall bay exactly'),
        'brushwood_bundle_m': D('d 0.35-0.45 x 0.9-1.2 long, two straw-rope ties', None, 'hand-carried bundle; assumed from R §4 "brushwood / thatch bundles"'),
    },
    materials=[M('billet bark and sides', 'jp_m_wood_weathered', 'timber_weathered'), M('cut ends', 'jp_m_wood_endgrain', 'timber_weathered'),
               M('ties', 'jp_m_straw_rope', 'straw_aged'), M('brushwood twigs', 'jp_m_bamboo_weathered', 'bamboo_weathered')],
    connectors=['proxy_base on terrain or a stone course; back face 0.05 off a wall on the ken grid'],
    variants=[V('_wall_1ken_h120', 'against a wall, 1 ken x 1.2 m'), V('_wall_1ken_h180', 'against a wall, 1 ken x 1.8 m (winter-full)'),
              V('_half', 'half-ken end piece, stepped top'), V('_free_posts', 'free-standing between two stakes with a board cap'),
              V('_bundle', 'one brushwood bundle; place 1-6 leaning'), V('_ab_collapsed', 'ABANDONED: slumped end, billets spilled on the ground')],
    abandoned='Stacks were full for winter when the people left: stacks stay mostly intact, greyed, one end slumped; brushwood bundles lean and rot; leaf litter at the base.',
    families=['Firewood stack', 'Brushwood / thatch bundles', 'Driftwood stacks', 'Fuel stacks for salt boiling'],
    placement='Against the doma or kitchen wall under an eave, or between two stakes in the yard; never across a door or window; 1-3 modules per house.',
    lod_budget='small prop <=300 faces LOD0 per 1-ken module (billets as merged prisms; end grain carries the look)',
    banned_tells_to_watch=['chainsaw-flat identical ends', 'modern plastic tarp or pallets'])

add('Yard and farm', id='jp_s_laundry_pole', name='Laundry and drying pole (monohoshi-zao) with swappable loads',
    what='A bamboo pole on two forked posts or crossed stakes: laundry in towns, persimmons, daikon and nets in autumn villages.',
    importance='filler', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.3,
    period_evidence='monohoshi-zao on forked posts, kimono threaded through the sleeves [OUTDOOR_LIST §2 U Streets S162]; cloth stretched on bamboo (araihari) in a Harunobu print of 1767 [k33]; hung persimmons (hoshigaki) [k35]',
    refs=[R('k33_harunobu_araihari_1767', 'washed cloth stretched on bamboo stretchers in a yard (1767)', True),
          R('k35_firewood_hoshigaki', 'persimmon strings hung under an eave (autumn load)')],
    dimensions={
        'pole_m': D('3.64 (2 ken) x d 0.04-0.05 bamboo', None, 'two ken spans a yard; a madake culm this long is 4-5 cm thick'),
        'post_height_m': D('1.8-2.1 to the fork', None, 'hanging height a person reaches with a raised arm'),
        'crossed_stakes_m': D('two 2.2 m poles crossed at 1.8 m, legs 1.0 apart', None, 'the cheap rural support in R §6'),
    },
    materials=[M('pole, stakes', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('forked posts', 'jp_m_wood_weathered', 'timber_weathered'),
               M('cloth load', 'jp_m_textile_kinari', 'kinari_cloth'), M('indigo cloth load', 'jp_m_textile_noren', 'aizome_kon'),
               M('persimmon / daikon load', 'jp_m_straw_rope', 'straw_aged')],
    connectors=['proxy_base on terrain; loads are child proxies hung at load points 0.30 apart along the pole'],
    variants=[V('_forked', 'two forked wooden posts (towns, yards)'), V('_crossed', 'crossed bamboo stakes (villages, shore)'),
              V('_load_cloth', 'kimono and cloth threaded on the pole: faded, one fallen'), V('_load_kaki', 'strings of peeled persimmons, dried dark (AUTUMN)'),
              V('_load_daikon', 'daikon hung in pairs, shrivelled (AUTUMN)'), V('_load_net', 'a small net draped (fishing village)'),
              V('_ab_down', 'ABANDONED: one post leaning, pole slipped to the ground at one end')],
    abandoned='Cloth left out a year is faded, torn and partly fallen; persimmons and daikon have dried black and some strings snapped; poles stand but one in three leans.',
    families=['Laundry pole', 'Hanging produce (persimmons, daikon, chillies, seed bags)'],
    placement='In the back yard or back alley, parallel to the house wall 1.5-3 m out; in fishing villages between houses; never across a path.',
    lod_budget='small prop <=300 faces LOD0 (pole + posts); each load <=300',
    banned_tells_to_watch=['wire or plastic pegs', 'western trousers and shirts: garments are kimono shapes'])

add('Yard and farm', id='jp_s_straw_stack', name='Straw stacks, stooks, bundles and rice bales (wara-nio, wara-taba, tawara)',
    what='The AUTUMN signature: straw stacks round a centre pole in the stubble, stooks drying, tied bundles and stacked rice bales by barns.',
    importance='filler', tiers=[1, 2], region='rural', priority='P1', wave=1, effort=0.5,
    period_evidence='straw stacks round a centre pole with a straw cap, many regional names (niho, nigo) [OUTDOOR_LIST §2 R §4; O20]; rice bales stacked (R, port towns); autumn season decision [KEEP_OUTDOOR]',
    refs=[R('k34_straw_rice', 'rice straw tied and stood to dry in a harvested field, October 2008 (colour sample for straw_aged)'),
          R('c05_ouchi_thatch', 'thatch village context')],
    dimensions={
        'nio_m': D('d 1.5-2.2 x h 2.0-3.0 incl. conical cap; centre pole projects 0.3', 'O20 (form); sizes assumed', 'form sourced; size read as "higher than a man" in farm photos'),
        'stook_m': D('6-10 sheaves leaning, footprint d 0.6, h 1.0-1.2', None, 'assumed from k34'),
        'bundle_m': D('d 0.25 x 0.9-1.1, two ties', None, 'threshed straw bundle; assumed'),
        'tawara_m': D('0.75 long x d 0.45, 4 to (about 60 kg) of rice', None, 'standard Edo rice bale of 4 to; size from later survivors, assumed'),
    },
    materials=[M('stack surface', 'jp_m_straw_stack', 'straw_aged'), M('ties, cap binding, bale lids', 'jp_m_straw_rope', 'straw_aged'),
               M('centre pole', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['proxy_base on terrain (stubble field or yard); stacks sink 0.05 into the ground'],
    variants=[V('_nio_cyl', 'cylindrical stack with a conical cap (Kinai)'), V('_nio_cone', 'conical stack (Kanto)'),
              V('_stook', 'sheaves leaning in a ring'), V('_bundle', 'single tied bundle (place in 3s-12s)'),
              V('_tawara_stack', 'rice bales stacked 2-3 high, 3-6 bales'), V('_ab_slumped', 'ABANDONED: stack slumped, cap blown off, grey and darker on top')],
    abandoned='Straw from the last harvest: stacks greyed on top and slumped to one side, caps blown off; bales split with straw spilling; stooks fallen flat.',
    families=['Straw stack / sheaf stack', 'Straw bundles in stooks', 'Brushwood / thatch bundles', 'Rice bales stacked'],
    placement='Nio at field edges and on the threshing yard, 1-4 per farm; stooks in rows on stubble; bales only under an eave or in a shed doorway (never in the open field).',
    lod_budget='small prop <=300 faces LOD0 (nio as a 12-sided lathe with a ragged cap ring)',
    banned_tells_to_watch=['round machine bales or plastic wrap', 'square baler bales'])

add('Yard and farm', id='jp_s_oke', name='Wash tubs, buckets and barrels: the cooperage family (tarai, oke, teoke, taru)',
    what='One set of stave-and-hoop meshes that dresses yards, inn doors, graves, wells and fire corners: wash tub, hand bucket, carrying bucket, pickle barrel, buckets upside down on stakes.',
    importance='filler', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.5,
    period_evidence='wash tub (tarai) in yards, no washboard (Meiji) [OUTDOOR_LIST §2 R §6]; upturned buckets on stakes (oke-hoshi) R §6; wooden well buckets with iron bands from the Nara period [O23]',
    refs=[R('k32_harunobu_well', 'well bucket and wash tub at a well (1760s, near-period)', True),
          R('k33_harunobu_araihari_1767', 'wash tubs in a laundry yard (1767)', True)],
    dimensions={
        'tarai_m': D('d 0.60-0.80 x h 0.20-0.25', None, 'wash tub for clothes; assumed from prints'),
        'teoke_m': D('d 0.24-0.28 x h 0.25 + handle 0.20', None, 'hand bucket, same mesh as the fire-tub pyramid buckets'),
        'ninai_oke_m': D('d 0.38 x h 0.38 with two tall ears for a carrying pole', None, 'carrying bucket; assumed'),
        'taru_m': D('d 0.50-0.60 x h 0.60-0.70 with a lid and weight stone', None, 'pickle barrel; assumed'),
        'hoop': D('split-bamboo hoops (taga), 2-3 per vessel; iron band only on well buckets', 'O23 (iron fittings)', None),
    },
    materials=[M('staves', 'jp_m_wood_weathered', 'timber_weathered'), M('bamboo hoops', 'jp_m_bamboo_weathered', 'bamboo_weathered'),
               M('iron band (well bucket)', 'jp_m_metal_iron', 'iron_black'), M('leaf litter inside', 'jp_m_ground_leaf_litter', 'leaf_litter_autumn'),
               M('weight stone', 'jp_m_stone_river', 'stone_lantern')],
    connectors=['proxy_base on terrain, a board floor or a stake top (upturned)'],
    variants=[V('_tarai', 'wash tub'), V('_teoke', 'hand bucket (shared with the fire tub and grave rack)'), V('_ninai', 'carrying bucket (tenbin load)'),
              V('_taru_lid', 'pickle barrel with lid and stone'), V('_stake', 'bucket upside down on a stake (oke-hoshi)'),
              V('_ab_tipped', 'ABANDONED: tipped on its side, one hoop sprung'), V('_ab_staves', 'ABANDONED: collapsed into loose staves and a hoop')],
    abandoned='Tubs left standing hold rotten leaves and silt (no water: nothing is clean); a third are tipped over; a few have dried out and collapsed into staves.',
    families=['Wash tubs + buckets drying on stakes', 'Foot-washing tubs at inn doors', 'Pickle barrels with weight stones', "Divers' tubs and beach fire ring"],
    placement='By the well, the back door or the kitchen wall; foot-washing tubs at inn entrances; never in the street centre. Interior list (PA2) may list the same vessels: one mesh family serves both.',
    lod_budget='small prop <=300 faces LOD0 per vessel (12-16 staves as a faceted cylinder, hoops as rings)',
    banned_tells_to_watch=['galvanised or enamel buckets', 'ridged washboard (Meiji)', 'metal hoops on ordinary tubs'])

add('Yard and farm', id='jp_s_tenbin', name='Shoulder pole and loads (tenbin-bo) with swappable loads',
    what="A carrying pole with two loads: every peddler's and farmer's carrier, stood against a wall or dropped in the road.",
    importance='filler', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.3,
    period_evidence='peddler with a pole and two baskets in a Moronobu print, c.1680 [k06]; pole and baskets, buckets, boxes, rope-net soil carrier [OUTDOOR_LIST §2 U, S155]',
    refs=[R('k06_moronobu_ageyamachi', 'two round baskets set down from a carrying pole in a street, c.1680', True),
          R('k28_kusakabe_peddler', 'vegetable peddler with pole and two baskets (1880s photo)')],
    dimensions={
        'pole_m': D('1.52-1.82 x 0.05 x 0.03, slightly curved', 'O21 (museum poles 1.37 and 1.52 m; 6 shaku = 1.82 common)', None),
        'rope_drop_m': D('0.45-0.60 from pole to load rim', None, 'loads hang at knee height when carried; assumed'),
        'basket_m': D('d 0.45 x h 0.20-0.30 round baskets', None, 'read off k06/k28'),
    },
    materials=[M('pole', 'jp_m_wood_weathered', 'timber_weathered'), M('ropes', 'jp_m_straw_rope', 'straw_aged'),
               M('baskets', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('buckets', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['proxy_base on terrain; loads as child proxies at the two rope points'],
    variants=[V('_baskets', 'two round baskets (vegetables, fish)'), V('_buckets', 'two ninai-oke buckets (water, night soil)'),
              V('_boxes', "two stacked boxes (peddler's goods)"), V('_leaning', 'pole leaning on a wall, loads on the ground'),
              V('_ab_dropped', 'ABANDONED: dropped in the road, one basket overturned, goods spilled and rotted')],
    abandoned='Dropped where the carrier stopped: pole on the ground, one load tipped; baskets greyed and split.',
    families=['Shoulder pole and loads (tenbin-bō)', 'Peddler kits', 'Night-soil buckets and pole'],
    placement='Leaning by shop doors and yard walls; dropped singly on roads and bridges (rare: 1 per few hundred metres of road).',
    lod_budget='small prop <=300 faces LOD0')

add('Yard and farm', id='jp_s_handcart', name='Handcart (daihachi-guruma) and small cart (niguruma)',
    what="The dead world's abandoned vehicle: a two-wheeled plank cart left in streets, yards and on highways, loaded or tipped.",
    importance='standard', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.6,
    period_evidence='1,273 carts counted in Edo in 1703 [PLAYBOOK §1, T54]; 2,239 carts branded at Denmacho 1700-03, invented after the 1657 fire [O04]',
    refs=[R('k31_daihachi_uzumasa', 'a daihachi-guruma on a film-studio Edo street (2002 photo, form only)'),
          R('x37_eisen_narai', 'post-town street context (1830s)', True)],
    dimensions={
        'bed_m': D('2.42 long x 0.76 wide (8 shaku x 2.5 shaku)', 'O04', None),
        'wheel_diameter_m': D('1.06 (3.5 shaku), wooden spoked wheels with iron tyres', 'O04 (diameter); tyre assumed', None),
        'shafts_m': D('bed rails continue 0.9 forward as handles with a cross bar', None, 'read off later photos (k31)'),
        'niguruma_m': D('small cart: bed 1.5 x 0.6, wheel 0.75', None, 'the Daishichi (under 8 shaku) class in O04; sizes assumed'),
    },
    materials=[M('bed, wheels', 'jp_m_wood_weathered', 'timber_weathered'), M('tyres, hub bands', 'jp_m_metal_iron', 'iron_black'),
               M('load ropes', 'jp_m_straw_rope', 'straw_aged')],
    connectors=['proxy_base on terrain; wheels touch at two points, handle end on the ground or propped on a stone'],
    variants=[V('_empty', 'empty, handles down'), V('_load_bales', 'rice bales roped on (reuses jp_s_straw_stack _tawara)'),
              V('_load_barrels', 'sake or soy barrels (reuses jp_s_oke _taru)'), V('_small', 'niguruma, one person'),
              V('_ab_tipped', 'ABANDONED: tipped on its side, load spilled'), V('_ab_broken', 'ABANDONED: one wheel broken, bed on the ground')],
    abandoned='Carts stand where the owners left them: half loaded, handles on the ground, one in three tipped or with a broken wheel; wood grey, tyres rusted.',
    families=['Handcart (daihachi / niguruma)'],
    placement='In streets along the house line, in yards by the kura, at bridge ends and on the highway shoulder; never blocking a door. The DayZ car-wreck role: cover in open streets.',
    lod_budget='medium site object <=1,500 faces LOD0 (decision 9); wheels 12 spokes as flat bars',
    open_questions=['Is it a cover object only, or should Stephen want a pushable cart later (vehicle scripting, out of scope)?'],
    banned_tells_to_watch=['rubber tyres', 'metal spokes', 'wheelbarrow (late Edo-Meiji)'])

# ================================================================= WATER
add('Water', id='jp_s_well_tsurube', name='Pulley well (tsurube-ido): curb, frame, pulley, two buckets; roofed variant',
    what='The town and yard well: a curb with a crossbeam frame and a pulley, two buckets on one rope; the roofed version is dwelling shell 28.',
    importance='standard', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.8,
    period_evidence='two buckets alternating over an upper pulley (futamata tsurube) [O23]; Edo dug wells about 1 m across, lined with stacked bottomless tubs or dry stone [O22]; pulley well at a yard in Harunobu, 1760s [k32]',
    refs=[R('k10_morse_well_frame', 'wooden well-frame with pulley (Morse 1885)'), R('k12_morse_well_kaga', 'well at the Kaga yashiki, Tokyo: roofed frame (Morse 1885)'),
          R('k14_morse_well_curb_stone', 'stone well-curb (Morse 1885)'), R('k13_morse_well_curb_old', 'ancient form of wooden well-curb, igeta (Morse 1885)'),
          R('k32_harunobu_well', 'pulley well, buckets and a tub, Suzuki Harunobu (d. 1770), 1760s', True)],
    dimensions={
        'shaft_diameter_m': D('0.9-1.0 inside', 'O22', None),
        'curb_m': D('outside d 1.05-1.20 (round tub curb) or 1.20 x 1.20 (square igeta), h 0.60-0.75', None, 'shaft plus a 0.08-0.10 wall; height from Morse figs 287-288 (k13, k14) read against a figure'),
        'frame_height_m': D('2.2-2.4 to the pulley axle', None, 'read off Morse fig 289 (k10); keeps the rope clear of a standing head'),
        'bucket_m': D('d 0.26 x h 0.28 with an iron band (tsurube-oke)', 'O23 (iron fittings); size assumed', None),
        'roof_m': D('small gable, 1.6 x 1.8 plan, eave 2.1, board or shingle (roofed variant)', None, 'Morse fig 293 (k12); matches dwelling shell 28'),
    },
    materials=[M('tub curb, frame', 'jp_m_wood_weathered', 'timber_weathered'), M('stone curb', 'jp_m_stone_cut', 'stone_granite'),
               M('pulley, bucket bands', 'jp_m_metal_iron', 'iron_black'), M('rope', 'jp_m_straw_rope', 'straw_aged'),
               M('roof (roofed variant)', 'jp_m_roof_kureita', 'roof_board_silver'), M('wash slab', 'jp_m_stone_field', 'stone_granite')],
    connectors=['proxy_base on terrain; wash slab (nagashi-ishi) ring at grade', 'memory point "well" at the curb top centre for the drink/wash actions'],
    variants=[V('_curb_tub', 'round wooden tub curb with bamboo hoops'), V('_curb_igeta', 'square timber igeta curb'), V('_curb_stone', 'stone curb (T3, temples)'),
              V('_roofed', 'with a small board gable roof = dwelling shell 28'), V('_lid', 'curb with a board lid only, no frame (well curb and lid; old well in the woods)'),
              V('_ab_open', 'ABANDONED: rope gone, one bucket on the curb, one at the bottom; lid askew; leaves in the wash slab')],
    abandoned='Frames stand; the rope has rotted and one bucket sits on the curb; lids are askew or gone; the wash slab is silted with leaves. Water is still there (decision 3).',
    families=['Well, pulley or lever (tsurube-ido / hanetsurube)', 'Communal well (mura-ido / idobata)', 'Well curb and lid', 'Old well in the woods', 'Well-god offering'],
    placement='Yards: 3-8 m behind the house, near the kitchen door; towns: in the back-alley court (one per nagaya court); never in the street itself.',
    lod_budget='medium site object <=1,500 faces LOD0 (decision 9)',
    open_questions=['Engine: config class inherits the vanilla Well script class (4_world/entities/building/well.c: drink + wash hands) through a one-line 4_World class in our asset PBO; confirm the action targets a static map object of ours in the first in-game check.'],
    banned_tells_to_watch=['hand pump (vanilla Chernarus well pump)', 'concrete ring curb', 'metal chain'])

add('Water', id='jp_s_well_hanetsurube', name='Lever well (hanetsurube): counterweighted sweep on a post over a curb',
    what='The village well and field sweep: a long pole pivoting on a forked post, stone counterweight at one end, bucket on a bamboo pole at the other.',
    importance='standard', tiers=[1, 2], region='rural', priority='P1', wave=1, effort=0.6,
    period_evidence='hane-tsurube named among the tsurube types [O23]; lever well mostly rural, also at town edges and temple yards [OUTDOOR_LIST §2 R §6, S157]; T1 exteriors have a lever well [PLAYBOOK §2.1]',
    refs=[R('k11_morse_well_rustic', 'rustic well-frame (Morse 1885)'), R('k13_morse_well_curb_old', 'wooden igeta curb (Morse 1885)'),
          R('c20_minkaen_c', 'farmhouse yard context (open-air museum)')],
    dimensions={
        'post_m': D('2.4-3.0 high, forked or with a through-pin, d 0.15', None, 'no period measurement found; read as "twice a man" in later photos'),
        'sweep_pole_m': D('5.5-7.0 long, pivot at 1/3 from the weight end', None, 'lever ratio lets the weight lift a full bucket; assumed'),
        'counterweight_m': D('river stone or bundle of stones d 0.35-0.45, lashed', None, 'assumed'),
        'bucket_pole_m': D('bamboo 3.5-4.5 reaching into the shaft', None, 'shallow Kanto/Kinai water tables (O23)'),
        'curb_m': D('as jp_s_well_tsurube _curb_tub / _curb_igeta', None, 'shared mesh'),
    },
    materials=[M('post, sweep', 'jp_m_wood_weathered', 'timber_weathered'), M('bucket pole', 'jp_m_bamboo_weathered', 'bamboo_weathered'),
               M('counterweight', 'jp_m_stone_river', 'stone_lantern'), M('lashing', 'jp_m_straw_rope', 'straw_aged')],
    connectors=['proxy_base on terrain; reuses the tsurube curb meshes; memory point "well" as the pulley well'],
    variants=[V('_well', 'over a well curb (yard)'), V('_field', 'field sweep over a ditch or pit, no curb (R §2 field version)'),
              V('_ab_down', 'ABANDONED: sweep lashing rotted, pole dropped with the bucket end on the ground, weight end up')],
    abandoned='The lashing of the bucket pole has rotted: the sweep rests weight-down with the bamboo lying across the curb; post standing.',
    families=['Well, pulley or lever (tsurube-ido / hanetsurube)'],
    placement='Farm yards and village commons, 5-15 m from the house; field version at a ditch corner. Its tall sweep is a skyline tell: at most 1 per farmstead.',
    lod_budget='medium site object <=1,500 faces LOD0; the sweep must keep its silhouette in every LOD (PLAYBOOK T7b spirit)',
    banned_tells_to_watch=['metal pivot hardware', 'concrete curb'])

add('Water', id='jp_s_fire_tub', name='Corner fire tub with bucket pyramid (tsuji no oo-oke) and eave buckets',
    what='The big wooden fire tub at town crossings with small hand buckets stacked on its lid, plus buckets hung at the eaves: the 1730 fire kit, NOT a tub at every house.',
    importance='standard', tiers=[2, 3], priority='P1', wave=1, effort=0.5,
    period_evidence='large tubs of about 6 koku at town crossings with hand buckets stacked on top [O03]; eave buckets required after the Meireki fire (FDM) [OUTDOOR_LIST §2 U Fire]; a tensui-oke at every house is 1789+ (period trap, KEEP_OUTDOOR)',
    refs=[R('k21_edo_bousui', 'reconstructed Edo fire tub with a bucket pyramid (Fukagawa Edo Museum street set)'), R('k22_hirakata_jinja', 'donated shrine fire tub (tensui-oke) with a donor mark, Hirakata shrine (photo)'),
          R('x31_masanobu_ryogoku_1748', 'Edo riverside town, c.1748 (context only: no tub visible)', True)],
    open_questions=['No pre-1750 image of a corner tub with a bucket pyramid was found; the form rests on O03 and museum reconstructions (k21). Check a Kyoho-era print before calling it final.'],
    dimensions={
        'capacity': D('6 koku = about 1,080 L', 'O03 (6 koku; 1 koku = 180.4 L)', None),
        'tub_m': D('d 1.25 x h 1.00 outside (1,080 L needs about d 1.15 x 1.0 inside)', None, 'derived from the 6-koku capacity'),
        'teoke_pyramid': D('10 hand buckets in 3 tiers (6+3+1) on a board lid; bucket d 0.26', None, 'pyramid read off reconstructions (k21); count assumed'),
        'stand_m': D('stone or timber base 0.15-0.30 high', None, 'keeps the tub off the mud; assumed'),
        'eave_bucket': D('1-2 teoke hung on a peg at 1.9-2.1 m', None, 'assumed'),
    },
    materials=[M('tub staves', 'jp_m_wood_weathered', 'timber_weathered'), M('hoops', 'jp_m_bamboo_weathered', 'bamboo_weathered'),
               M('house-mark on buckets', 'jp_m_decal_sumi_text', 'sumi_black'), M('base stone', 'jp_m_stone_cut', 'stone_granite'),
               M('leaf litter and silt', 'jp_m_ground_leaf_litter', 'leaf_litter_autumn')],
    connectors=['proxy_base on terrain at a crossing corner, against a house corner post line', 'eave bucket: proxy on a building peg memory point'],
    variants=[V('_full', 'tub + lid + 10-bucket pyramid'), V('_open', 'tub, no lid, 3 buckets on the ground'), V('_eave', 'single bucket on an eave peg (proxy for building fronts)'),
              V('_rural', 'smaller rain barrel under an eave (rural, R §6; about 1 koku)'),
              V('_ab_scattered', 'ABANDONED: pyramid collapsed, buckets scattered, lid off, tub half full of leaves and dark water')],
    abandoned='Pyramids have fallen in wind; buckets lie scattered round the tub; the tub holds rotting leaves and a skin of dark rainwater (not a water source).',
    families=['Corner fire tub with bucket pyramid + eave buckets', 'Rain barrel / water jar'],
    placement='At street crossings and alley mouths, 1 per corner, against the corner house; eave buckets on every 2nd-3rd town front. Never one tub per house (trap).',
    lod_budget='small prop set: tub <=300, pyramid <=300 (buckets merged) LOD0',
    banned_tells_to_watch=['per-house rain tub on every front (1789+)', 'hand fire pump (1750s+)', 'cast-iron or bronze tub outside temples'])

add('Water', id='jp_s_gutter', name='Street gutter kit (omote-dobu): stone-lined segment, slab crossing, dobu-ita cover, outfall',
    what='The drain along town house fronts and down back alleys, in snap-to-ken pieces laid on the terrain ditch: stone-lined run, stone slab crossing at doors, board cover (dobu-ita), corner and outfall.',
    importance='standard', tiers=[2, 3], priority='P1', wave=1, effort=0.6,
    period_evidence='roadside ditch and street gutter carrying rain and wash water [OUTDOOR_LIST §2 U / W, S058]; Edo drains along lot boundaries in stone or wood, 3-6 shaku, boards rot fast [O24]; alley centre drain with board covers (dobu-ita) [OUTDOOR_LIST §2 U]',
    refs=[R('x38_morse_gutter', 'bamboo eave gutter and downpipe feeding a street drain (Morse 1885)'),
          R('x27_morse_village_yamashiro', 'Kansai village street with a stone-edged drain (Morse 1885)'),
          R('c01_narai_street', 'post-town street edge with a gutter (surviving street)')],
    dimensions={
        'segment_length_m': D('1.82 (1 ken) and 0.91 pieces', None, 'snaps to the house grid (PLAYBOOK rule 9) so every front gets whole pieces'),
        'channel_m': D('omote-dobu inside 0.30 wide x 0.25-0.30 deep; alley dobu 0.20 x 0.20', None, 'O24 gives 3-6 shaku for the big lot-boundary drains; the street-front gutter is narrower (step-over width); assumed'),
        'lining_m': D('dressed stones 0.15-0.20 thick, top flush with grade', None, 'assumed'),
        'slab_crossing_m': D('granite slab 0.60-0.90 x 0.45 x 0.12 bridging the gutter at each door', None, 'assumed'),
        'dobu_ita_m': D('boards 0.91 long x 0.24-0.30 wide x 0.03, laid across', None, 'assumed; boards rattle (noise hook)'),
    },
    materials=[M('lining, slabs', 'jp_m_stone_cut', 'stone_granite'), M('earth-bank variant', 'jp_m_stone_field', 'stone_granite'),
               M('dobu-ita boards', 'jp_m_wood_weathered', 'timber_weathered'), M('silt and leaves in the bed', 'jp_m_ground_leaf_litter', 'leaf_litter_autumn')],
    connectors=['post: segment ends on half-ken lines along the front sill line, 0.30 in front of the pent posts', 'terrain: seated in a terrain-tool ditch (the linear ditch is terrain work, OUTDOOR_LIST §7.5)'],
    variants=[V('_stone_1ken', 'stone-lined straight, 1 ken'), V('_stone_half', 'stone-lined straight, half ken'), V('_corner', '90-degree corner'),
              V('_slab', 'slab crossing piece'), V('_board_1ken', 'alley run with dobu-ita covers'), V('_outfall', 'outfall into a canal or ditch'),
              V('_earth_1ken', 'earth-banked rural gutter with field-stone edge'), V('_ab_silted', 'ABANDONED: bed silted and leaf-filled, one lining stone tipped in; boards missing or broken')],
    abandoned='Silted to half depth with leaves and mud; weeds along the joints; a few dobu-ita boards gone or snapped so the drain gapes.',
    families=['Earth street with gutters and slab crossings', 'Roadside ditch / street gutter', 'Alley drain boards (dobu-ita)'],
    placement='Continuous along every town street front, 0.3 m outside the house line, a slab at each door; down the centre of back alleys with boards; highway ditches are terrain only.',
    lod_budget='small prop <=300 faces LOD0 per piece; Geometry only on slabs and boards (the channel stays walkable), Roadway on slabs and boards',
    open_questions=['Terrain: the ditch the pieces sit in is T\'s terrain-tool work; the lead must decide who cuts it (placement agent or terrain agent).'],
    banned_tells_to_watch=['concrete U-channel', 'iron grates', 'kerbstones'])

add('Water', id='jp_s_chozubachi', name='Purification basin (chozubachi) with ladle; roofless shrine form',
    what='The stone ablution basin before a shrine, often donated and dated; many village shrines had no roof over it.',
    importance='standard', tiers=[1, 2, 3], status_overlay='religious', priority='P2', wave=2, effort=0.4,
    period_evidence='stone basin inscribed Tenna 2 (1682): h 0.57, w 0.82, d 0.48 [O14]; Omononushi shrine granite basin 1.50 x 0.75 x 0.75, basin depth 0.35 [O14]; many village shrines unroofed [OUTDOOR_LIST §2 U, S185]',
    refs=[R('k15_morse_chozubachi', 'stone water basin (Morse 1885)'), R('k24_chozubachi', 'chozubachi with ladles at a shrine (photo)'),
          R('c22_kasuga_lanterns', 'weathered granite + moss colour context')],
    dimensions={
        'basin_small_m': D('0.82 x 0.48 x 0.57 high', 'O14 (Tenna 2 = 1682 basin)', None),
        'basin_large_m': D('1.50 x 0.75 x 0.75 high; water hollow 0.35 deep; rim 0.107', 'O14 (Omononushi shrine)', None),
        'plinth_m': D('one or two flat stones 0.15-0.25 under the basin', None, 'assumed'),
        'ladle_m': D('bamboo or wood cup d 0.08 on a 0.45 handle', None, 'assumed'),
    },
    materials=[M('basin, plinth', 'jp_m_stone_carved', 'stone_lantern'), M('carved donor text and date', 'jp_m_decal_carved_text', 'stone_lantern'),
               M('ladle', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('moss', 'jp_m_decal_moss', 'moss_on_stone'),
               M('leaves in the hollow', 'jp_m_ground_leaf_litter', 'leaf_litter_autumn')],
    connectors=['proxy_base on terrain at the sando side, 3-6 m before the torii or hall; can sit under a temizuya shell (KEEP_CIVIC Shinto 5)'],
    variants=[V('_small', 'Tenna-size basin (village)'), V('_large', 'long basin (town shrines)'), V('_natural', 'natural stone with a cut hollow (mountain shrine)'),
              V('_ab_dry', 'ABANDONED (default): dry, leaves and moss in the hollow, ladles fallen')],
    abandoned='Dry, leaf-filled hollow with green algae stains; ladles fallen and split; moss on the north side.',
    families=['Purification basin (chōzubachi) + ladle', 'Courtyard garden kit (lantern, basin, stones)'],
    placement='Beside the approach, right-hand side walking in, 3-6 m before the hall; one per shrine; garden variant by a veranda.',
    lod_budget='small prop <=300 faces LOD0', checks=CK_STONE,
    banned_tells_to_watch=['bamboo spout fountain running water in a dead world', 'dragon spout (mostly later)'])

# ================================================================= ROADSIDE STONES AND SHRINES
add('Roadside stones and shrines', id='jp_s_stone_jizo', name='Stone Jizo figure (tsuji-jizo): standing monk on a lotus or plinth, 3 sizes',
    what='The roadside guardian at crossroads, bridges and village entrances; the same figure makes the six-Jizo row and small child graves.',
    importance='standard', tiers=[1, 2, 3], status_overlay='religious', priority='P1', wave=1, effort=0.8,
    period_evidence='roadside Jizo at crossroads and village entrances [OUTDOOR_LIST §2 W §5, S078]; Edo-period standing stone Jizo total 1.78 m, figure 1.36 m [O27]; boat-halo figure stones made from the 1640s, large ones until Kyoho [O06]',
    refs=[R('c24_jizo_cemetery', 'Jizo and grave stones, weathered stone'), R('k30_rokujizo', 'six-Jizo row of stone figures (photo)')],
    dimensions={
        'figure_m': D('small 0.45, standard 0.90, large 1.36 (figure only)', 'O27 (1.36 m figure on a 1.78 m total)', None),
        'plinth_m': D('lotus or plain square base 0.20-0.42 high', 'O27 (total minus figure = 0.42)', None),
        'staff': D('shakujo staff in the right hand, jewel in the left; head shaven', 'OUTDOOR_LIST §2 W §5', None),
    },
    materials=[M('figure, plinth', 'jp_m_stone_carved', 'stone_lantern'), M('moss and lichen', 'jp_m_decal_moss', 'moss_on_stone'),
               M('bib and cap (variant)', 'jp_m_textile_kinari', 'kinari_cloth'), M('offering cup, coins', 'jp_m_stone_river', 'stone_lantern')],
    connectors=['proxy_base on terrain or on a jp_s_stele base; fits inside jp_s_jizo_hut'],
    variants=[V('_s', 'small (0.45) for child graves and the six-Jizo row'), V('_m', 'standard (0.90) roadside'), V('_l', 'large (1.36) on a lotus plinth, pass tops and town edges'),
              V('_halo', 'figure in relief on a boat-shaped halo (funagata) = also a gravestone'), V('_bib', 'with a faded cloth bib and cap (decision 6)'),
              V('_offer', 'offering set: stone cup, small stones piled, withered flowers'), V('_ab_tipped', 'ABANDONED: toppled face-down or leaning, head cracked (rare, 1 in 10)')],
    abandoned='Stone does not rot: the figures stand, greener with moss and lichen, offerings withered, bibs rotted to rags; a few toppled by a quake or a flood.',
    families=['Roadside Jizō (+ Jizō hut)', 'Six-Jizō row', 'Pass-top Jizō + offering heap', 'Landslide scar with Jizō', 'Sulphur workings + hell-valley Jizō', 'Stone Buddha / stone Buddha rows'],
    placement='At crossroads, bridge ends, village entrances and pass tops, facing the road; six in a row at graveyard gates; never in the middle of a road.',
    lod_budget='small prop <=300 faces LOD0 (the carving is in the normal map; silhouette: head, shoulders, staff)', checks=CK_STONE,
    banned_tells_to_watch=['bright new red bibs everywhere', 'cute modern Jizo faces'])

add('Roadside stones and shrines', id='jp_s_jizo_hut', name='Jizo hut and street-corner box (Jizo-do / tsuji-jizo box)',
    what='A waist-to-head-high roofed wooden box or tiny open hall sheltering a Jizo at a street corner or roadside; one per ward in Kyoto.',
    importance='standard', tiers=[1, 2, 3], status_overlay='religious', priority='P1', wave=1, effort=0.4,
    period_evidence='roofed box or tiny hall sheltering a Jizo, one per Kyoto ward [OUTDOOR_LIST §2 W §5, S079]',
    refs=[R('c24_jizo_cemetery', 'Jizo stones context'), R('x27_morse_village_yamashiro', 'Kansai village street context (Morse 1885)')],
    dimensions={
        'box_m': D('0.9 x 0.9 plan (half ken), 1.5-1.8 high, raised floor 0.6', None, 'fits jp_s_stone_jizo _s/_m; on the half-ken grid'),
        'hall_m': D('1.82 x 1.82 open front, eave 1.9, ridge 2.8 (walk-under shelter)', None, 'one ken; a tiny rain shelter hook'),
        'lattice_front_m': D('bars 0.03 at 0.09, opening leaf', None, 'reuses the koshi part style; assumed'),
    },
    materials=[M('frame, boards', 'jp_m_wood_weathered', 'timber_weathered'), M('roof boards', 'jp_m_roof_kureita', 'roof_board_silver'),
               M('lattice', 'jp_m_wood_street_dark', 'timber_street_dark'), M('stone base', 'jp_m_stone_field', 'stone_granite')],
    connectors=['proxy_base on terrain or a stone base; Jizo figure as a child proxy on the floor board'],
    variants=[V('_box', 'waist-to-head box on a post or stone base (Kyoto street corner)'), V('_hall', 'one-ken open hall (roadside)'),
              V('_stone_roof', 'stone slab roof over a figure, no box (mountain)'), V('_ab_open', 'ABANDONED: lattice door fallen off, roof boards lifted, leaves inside')],
    abandoned='Roof boards lifted and mossy, the lattice door hanging or fallen; the figure inside untouched; dead flowers and leaves on the floor.',
    families=['Roadside Jizō (+ Jizō hut)'],
    placement='At street corners (towns, against a corner house) and at village entrances; 1 per 2-3 roadside Jizo.',
    lod_budget='small building class is too big: medium site object <=1,500 faces LOD0 (hall), box <=600')

add('Roadside stones and shrines', id='jp_s_stele', name='Inscribed stone family: Koshin pillar and roadside steles with text decals',
    what='Six stone shapes carrying carved relief or text: the Koshin stone, dosojin, bato Kannon, direction and boundary stones, nenbutsu and memorial stones, all one family.',
    importance='standard', tiers=[1, 2, 3], status_overlay='religious', priority='P1', wave=1, effort=0.9,
    period_evidence='Koshin pillar with Shomen Kongo, 1.22 m, 1698 [O07]; round-carved Koshin 1.48 m, 1727 [O08]; Koshin 1.225 m (shaft 0.945, base 0.28), andesite [O09]; Koshin stones from 1664, common in 1730 [OUTDOOR_LIST §2 W §5, S085; §3.3]',
    refs=[R('k41_koshin_sendabori', 'Koshin stones by a village road, Matsudo (photo)'), R('k19_koshinto', 'inscribed (text-type) Koshin stone, Nikko (photo)'), R('c24_jizo_cemetery', 'weathered stone and lichen'),
          R('k02_bunken_ezu_p12', 'roadside marker post and mile mound on the Tokaido, 1690 (schematic)', True)],
    dimensions={
        'koshin_pillar_m': D('shaft 0.95 x 0.35 x 0.25 + base 0.28 = 1.22 total', 'O07, O09', None),
        'koshin_relief': D('Shomen Kongo (4 or 6 arms) with sun and moon above, 3 monkeys below, sometimes 2 cocks', 'O07 (1698), O07b (1727: sun, moon, 2 cocks)', None),
        'natural_slab_m': D('0.6-1.4 high, 0.4-0.8 wide, 0.15-0.30 thick', None, 'dosojin, nenbutsu, mountain-god stones are natural slabs; assumed'),
        'arched_slab_m': D('0.5-0.9 high x 0.30-0.40, rounded top', None, 'shared with the kushigata gravestone; assumed'),
        'direction_post_m': D('square pillar 0.9-1.5 x 0.20-0.25', None, 'michi-shirube; assumed'),
        'text': D('carved decals: Koshin, namu amida butsu, dosojin, bato Kannon, "right: Edo road", boundary names, era dates (Genroku, Hoei, Shotoku, Kyoho)', 'OUTDOOR_LIST §7.7', None),
    },
    materials=[M('stone', 'jp_m_stone_carved', 'stone_lantern'), M('carved text', 'jp_m_decal_carved_text', 'stone_lantern'),
               M('moss and lichen', 'jp_m_decal_moss', 'moss_on_stone'), M('mound earth (Koshin mound)', 'jp_m_ground_leaf_litter', 'leaf_litter_autumn')],
    connectors=['proxy_base on terrain; 1-3 stones may share one base stone; decals are separate geometry faces 2 mm proud'],
    variants=[V('_koshin', 'Koshin square pillar with Shomen Kongo relief'), V('_relief_panel', 'relief panel (bato Kannon horse head, dosojin couple)'),
              V('_natural_slab', 'natural slab with deep-cut characters'), V('_arched', 'arched-top slab'), V('_pillar', 'square direction / boundary post'),
              V('_round', 'round stone (dosojin, water god)'), V('_group3', 'three stones on one base (a roadside cluster)'),
              V('_ab_tipped', 'ABANDONED: leaning 10-20 degrees, half sunk, lichen over the text')],
    abandoned='As the Jizo: stones endure. Leaning, sunk, lichen blotting the text; grass tufts at the base; offerings gone.',
    families=['Kōshin stone / mound', 'Dōsojin (character / couple / round-stone)', 'Batō Kannon', 'Direction stone / wooden signpost', 'Village boundary post / stone',
              'Nenbutsu / daimoku stone', 'Water-god stone', 'Mountain-god stone / hokora', 'Pilgrim-club stone (kō-hi)', 'Execution-ground memorial stones', 'Inscribed stele / memorial stupa'],
    placement='Road forks, village boundaries and crossroads, facing the road; Koshin stones singly or on a low mound (terrain); direction stones at every fork of a main road.',
    lod_budget='small prop <=300 faces LOD0 per stone', checks=CK_STONE,
    banned_tells_to_watch=['paired dosojin everywhere (mostly 1804-30: a few only)', 'Fuji-ko or Ontake-ko stones (1779+/1785+)', 'Tokuhon-style nenbutsu stones (c.1800)'])

add('Roadside stones and shrines', id='jp_s_shimenawa', name='Straw rope (shimenawa) with paper streamers: lengths and wraps',
    what='The sacred straw rope with white zigzag streamers, in straight lengths and tree or rock wraps: marks sacred trees, rocks, wells, torii and village boundaries.',
    importance='filler', tiers=[1, 2, 3], status_overlay='religious', priority='P1', wave=1, effort=0.3,
    period_evidence='sacred tree with shimenawa [OUTDOOR_LIST §2 W §7]; New Year straw rope over doors, gates and wells [OUTDOOR_LIST §2 R §9, S176]; village boundary rope (kanjo-nawa, Kinai) [R §13]',
    refs=[R('k37_shimenawa_tree', 'sacred tree wrapped with a shimenawa (photo)'), R('c10_inari_torii', 'torii context')],
    dimensions={
        'rope_d_m': D('0.04-0.08 (well, gate) to 0.15-0.25 (sacred tree)', None, 'read off k37; assumed'),
        'shide_m': D('paper streamers 0.20-0.30 long, 4 zigzag folds, every 0.4-0.6', None, 'assumed'),
        'wrap_m': D('tree wraps for trunk d 0.6 / 1.0 / 1.6', None, 'matches the flora list sacred-tree sizes (assumed until F sets them)'),
    },
    materials=[M('rope', 'jp_m_straw_rope', 'straw_aged'), M('shide paper', 'jp_m_paper_shoji', 'washi_shoji')],
    connectors=['straight lengths hang between two memory points (torii tie-beam, gate posts, trees); wraps as proxies at trunk height 1.5-2.5'],
    variants=[V('_len_1ken', 'straight hanging length, 1 ken, sagging'), V('_len_2ken', '2 ken'), V('_wrap_d06', 'tree wrap for a 0.6 m trunk'),
              V('_wrap_d10', '1.0 m trunk'), V('_wrap_d16', '1.6 m trunk (landmark tree)'), V('_ab_tattered', 'ABANDONED (default): grey, frayed, shide gone or brown shreds')],
    abandoned='A year unrenewed: grey-brown, frayed ends, most paper streamers gone; one end of a hanging length dropped.',
    families=['Sacred tree with shimenawa', 'Seasonal door dressing (kadomatsu, shimenawa, Bon altar, fires)', 'Village boundary rope (kanjō-nawa)', 'Well-god offering', 'Sacred rock (iwakura)'],
    placement='On the wooden or stone torii tie-beam, around one old tree per shrine grove, over a well or a gate; boundary ropes across village-entry roads at 3 m.',
    lod_budget='small prop <=300 faces LOD0 (twisted rope as an 8-sided sweep with a twist texture)')

add('Roadside stones and shrines', id='jp_s_kosatsu', name="Official notice board (kosatsuba): roofed frame on a stone base with a fence",
    what='The shogunate edict board at bridge ends, crossings and every post town: a roofed frame holding inscribed boards, on a stone or earth base, fenced.',
    importance='standard', tiers=[2, 3], status_overlay='official', priority='P1', wave=1, effort=0.6,
    period_evidence='the Shotoku kosatsu boards of 1711 [PLAYBOOK §1, T23]; roofed boards at bridge ends and main crossings [OUTDOOR_LIST §2 U]; Fuchu kosatsuba (Koshu road, surviving Edo structure) 4.6 m wide, about 5 m high [O01]',
    refs=[R('k20_kosatsuba_kashiwabara', 'site of the Kashiwabara-juku kosatsuba on the Nakasendo (context photo)'), R('k29_hiroshige_numazu', 'notice board at Numazu on the Tokaido (1838-42 print; depiction only)', True),
          R('c16_hakone_sekisho', 'official black-board context (reconstruction)')],
    dimensions={
        'frame_m': D('3.6-4.6 wide x 3.0-5.0 high to the ridge', 'O01 (Fuchu 4.6 x ~5; typical 3-5 wide x 3-4 high)', None),
        'boards_m': D('5-7 boards, each 0.9-1.2 wide x 0.35-0.55 high, hung in two rows under the roof', None, 'assumed from prints'),
        'base_m': D('stone-faced earth base 0.6-0.9 high, 0.9 wider than the frame each side', None, 'assumed from k20 and prints'),
        'fence_m': D('palisade or bamboo fence 0.9-1.2 high, 0.9-1.8 in front', None, 'assumed'),
    },
    materials=[M('frame', 'jp_m_wood_weathered', 'timber_weathered'), M('boards', 'jp_m_wood_street_dark', 'timber_street_dark'),
               M('edict text', 'jp_m_decal_sumi_text', 'sumi_black'), M('roof', 'jp_m_roof_kureita', 'roof_board_silver'),
               M('base', 'jp_m_stone_cut', 'stone_granite'), M('fence', 'jp_m_bamboo_weathered', 'bamboo_weathered')],
    connectors=['proxy_base on terrain; base is part of the mesh (Geometry + Roadway on the base top)'],
    variants=[V('_std', 'post-town size, 3.6 wide'), V('_large', 'bridge-end size, 4.6 wide (Fuchu type)'), V('_forest', 'single roofed board on two posts (forest / hunting-ground notice)'),
              V('_ab_boards_down', 'ABANDONED: two boards fallen and split, text faded, fence gaps')],
    abandoned='Boards bleached, ink faded to ghosts, two fallen from their pegs; roof mossy; the fence has gaps.',
    families=['Notice board (kōsatsuba, BL site)', 'Forest markers (tomeyama stakes, brands, claim stakes, notice board)'],
    placement='At bridge ends, the main crossing of a post town and town entrances, facing the road; 1 per post town or ward; also serves KEEP_CIVIC Government 6 (decision 2).',
    lod_budget='medium site object <=1,500 faces LOD0',
    open_questions=['Board text: real 1711 Shotoku edict wording (public-domain law text) as decals? Readable in-game lore (see decision 5).'])

# ================================================================= STREET AND SHOP FRONT
add('Street and shop front', id='jp_s_bench', name='Bench (shogi / endai): plank bench with legs, 2 lengths',
    what='The low wide plank bench outside tea houses and shops, by farmhouse doors, under mile-mound trees: rest and a loot surface.',
    importance='standard', tiers=[1, 2, 3], priority='P1', wave=1, effort=0.3,
    period_evidence='a low board bench in front of a Yoshiwara shop, c.1680 [k06]; benches at tea stands [OUTDOOR_LIST §2 U, S063]; endai general in the Edo period [O17]',
    refs=[R('k06_moronobu_ageyamachi', 'low plank platform-bench in front of a shop with goods on it, c.1680', True),
          R('c18_hiroshige_mariko', 'roadside tea-house benches (c.1833)', True), R('x36_hiroshige_ishibe', 'tea-house benches under the pent (c.1833)', True)],
    dimensions={
        'endai_m': D('1.60-1.82 long x 0.45-0.60 wide x 0.42-0.45 high', 'O17 (about 1.60 x 0.45 x 0.45)', None),
        'long_m': D('2.73 (1.5 ken) x 0.75 x 0.42, 3 leg frames (tea-stand platform bench)', None, 'k06 shows a deeper platform bench; assumed'),
        'boards': D('2-3 boards 0.03 thick on two leg frames with a stretcher', None, 'assumed'),
    },
    materials=[M('boards, legs', 'jp_m_wood_weathered', 'timber_weathered'), M('mat cover (variant)', 'jp_m_straw_mushiro', 'thatch_new')],
    connectors=['proxy_base on terrain; seat top = loot surface (Roadway face)'],
    variants=[V('_1ken', 'endai 1.82'), V('_long', 'deep tea-stand bench 2.73'), V('_mat', 'with a straw mat thrown over'),
              V('_ab_tipped', 'ABANDONED: tipped on its side'), V('_ab_broken', 'ABANDONED: one leg frame collapsed, seat sloping to the ground')],
    abandoned='Grey boards cupped and split, a straw mat rotted on top; one in four tipped or collapsed at one end.',
    families=['Bench (shōgi / endai)'],
    placement='In front of tea houses, shops and inns under the pent, along the wall; by farmhouse doors; under a tree at mile mounds and passes. 1-3 per front.',
    lod_budget='small prop <=300 faces LOD0',
    banned_tells_to_watch=['bright red felt covers: any cloth cover has rotted in the dead world; one faded rag at most', 'back rests'])

add('Street and shop front', id='jp_s_shopfront', name='Shop-front kit: noren, mizuhiki-noren, sudare, hanging and standing signboards, shape signs',
    what='The dressing that makes a street read as a shopping street: split door curtains, the shallow eave curtain, rolled blinds, signboards and 3D shape signs.',
    importance='standard', tiers=[2, 3], priority='P1', wave=1, effort=1.0,
    period_evidence='split noren with crests along a shop eave, c.1680 [k06]; short noren at a Yoshiwara house, c.1680 [k05]; rolled sudare tied up at eaves, 1740 [k09]; bookseller front and signboard 1690 [x33]; shape signs (katachi-kanban) [OUTDOOR_LIST §2 U]',
    refs=[R('k06_moronobu_ageyamachi', 'mizuhiki/split noren with crests along the eave, c.1680', True), R('k05_moronobu_street_1680', 'short noren at a doorway, c.1680', True),
          R('k09_masanobu_ishiyama_1740', 'rolled sudare tied up under the eaves, 1740', True), R('x33_jinrin_bookseller_1690', 'shop front and signboard, 1690', True)],
    dimensions={
        'noren_m': D('3 panels x 0.34 = 1.02 wide per door; long 1.60, standard 1.13, half 0.56', 'O19 (modern trade sizes on the old kujira shaku; panel width 1 haba)', None),
        'mizuhiki_m': D('0.30-0.40 deep, full front width, unsplit', 'O19', None),
        'sudare_m': D('0.91 or 1.82 wide x 0.9-1.8 long, rolled d 0.10-0.12 when up', None, 'on the half-ken grid; assumed'),
        'kake_kanban_m': D('0.9-1.5 long x 0.25-0.35 x 0.04, hung under the eave', None, 'assumed from prints'),
        'oki_kanban_m': D('0.45 x 1.2 high on feet', None, 'assumed'),
        'shape_signs': D('6: giant brush 1.2, geta 0.6, tabi 0.7, medicine gourd 0.6, umbrella 1.0, fan 0.8', None, 'OUTDOOR_LIST §7.13 picks; sizes assumed'),
    },
    materials=[M('noren', 'jp_m_textile_noren', 'aizome_kon'), M('mizuhiki / plain noren', 'jp_m_textile_kinari', 'kinari_cloth'),
               M('noren pole', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('sudare', 'jp_m_reed_yoshizu', 'sudare_reed'),
               M('signboards', 'jp_m_wood_street_dark', 'timber_street_dark'), M('sign text', 'jp_m_decal_sumi_text', 'sumi_black'),
               M('shape signs', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['head: noren poles hook on the door-head (2.00) of jp_p_open_* parts; mizuhiki on the pent eave line', 'as proxies in the furnished shop variant p3d (decision 8)'],
    variants=[V('_noren_long', 'long noren, 3 panels, shop mark'), V('_noren_half', 'half noren (eating houses)'), V('_mizuhiki', 'eave curtain, 1 or 2 ken'),
              V('_sudare_up', 'sudare rolled up'), V('_sudare_down', 'sudare down'), V('_kanban_hang', 'hanging signboard'), V('_kanban_stand', 'standing signboard'),
              V('_shape_x6', 'six shape signs (brush, geta, tabi, gourd, umbrella, fan)'),
              V('_ab_noren_torn', 'ABANDONED (default for noren): faded to grey-blue, one panel torn off, hem shredded'),
              V('_ab_fallen', 'ABANDONED: pole dropped, noren in a heap on the threshold; signboard hanging from one cord')],
    abandoned='Cloth goes first: noren faded from indigo to grey-blue and shredded, some fallen with their poles; sudare slumped and holed; signboards hanging askew from one cord, text bleached.',
    families=['Shop front kit (noren, kanban, shape signs, sudare)'],
    placement='Noren only on open shop and eating-house doors (not on houses or kura); one sign type per shop; shape signs only on the matching trade (KEEP_TRADES dressing sets).',
    lod_budget='small prop <=300 faces LOD0 per piece; noren as 3 slightly bent quads per panel, two-sided',
    banned_tells_to_watch=['big sun-curtain noren on dry-goods fronts (19th c.)', 'beckoning cat (c.1850s)', 'shop names in modern type'])

add('Street and shop front', id='jp_s_lantern_sign', name='Shop lanterns and sign lamps: hanging chochin, box lamp (kake-, oki-, tsuji-andon)',
    what='One hanging paper-lantern mesh with swapped paper and text (shop, inn, gate, festival), and one framed box lamp at three heights: hung, standing, on a crossroads post.',
    importance='standard', tiers=[2, 3], priority='P1', wave=1, effort=0.6,
    period_evidence='hanging lanterns with crests and a standing andon in an Okumura Masanobu uki-e, c.1748 [x31]; kake-andon as shop signs; tsuji-andon before ward guard posts [O25]; bow and box lanterns 17th c. on [OUTDOOR_LIST §2 U]',
    refs=[R('x31_masanobu_ryogoku_1748', 'hanging chochin with crests and a standing andon, c.1748', True), R('x30_shinagawa_1726', 'standing paper andon on a Shinagawa tea-house floor, 1726', True),
          R('c18_hiroshige_mariko', 'tea-house sign lamp context (c.1833)', True)],
    dimensions={
        'chochin_m': D('oblong d 0.30 x 0.55 (shop), d 0.45 x 0.80 (inn, gate), top and bottom rings of wood', None, 'read off x31 against figures; assumed'),
        'kake_andon_m': D('box 0.30 x 0.15 x 0.45, bracket from the wall at 1.9-2.2', None, 'assumed'),
        'oki_andon_m': D('0.35 x 0.35 x 0.9-1.0 on legs', 'O25 (Enshu andon about 0.81 high; street sign lamps a little taller, assumed)', None),
        'tsuji_andon_m': D('box 0.40 x 0.40 x 0.60 on a 2.0 m post with a small roof', None, 'assumed'),
    },
    materials=[M('lantern paper', 'jp_m_paper_chochin', 'washi_shoji'), M('text and crests', 'jp_m_decal_sumi_text', 'sumi_black'),
               M('rings, frames, posts', 'jp_m_wood_street_dark', 'timber_street_dark'), M('roof (tsuji)', 'jp_m_roof_kureita', 'roof_board_silver'),
               M('hook', 'jp_m_metal_iron', 'iron_black')],
    connectors=['chochin: hangs from an eave memory point or a gate beam; kake-andon: bracket on a post connector at 2.0', 'as proxies in shop/inn variants (decision 8); tsuji-andon as a map object'],
    variants=[V('_chochin_shop', 'shop lantern with shop name'), V('_chochin_inn', 'inn lantern with name and association badge'), V('_chochin_gate', 'large ward-gate lantern'),
              V('_kake', 'hanging box sign lamp'), V('_oki', 'standing sign lamp'), V('_tsuji', 'crossroads lamp on a post'),
              V('_ab_torn', 'ABANDONED (default): paper split and holed, frame showing, faded text'), V('_ab_fallen', 'ABANDONED: lantern on the ground, crushed; oki-andon tipped')],
    abandoned='Paper rots in a year: lanterns hang as split, holed husks with the bamboo ribs showing; some on the ground; box lamps with the paper panels gone, frames intact. No light anywhere.',
    families=['Shop and inn lanterns / sign lamps (kake-andon)', 'Crossroads lamp (tsuji-andon)', 'Ward gate (kido, BL) + gate lantern', 'Festival layer (nobori, lanterns, mikoshi, stages)'],
    placement='One chochin or kake-andon per shop or inn front at the entrance; oki-andon only at eating houses and inns; tsuji-andon at crossings and ward gates.',
    lod_budget='small prop <=300 faces LOD0 (chochin as a 12-sided lathe; ribs in texture)',
    banned_tells_to_watch=['glass', 'giant red gate lantern (1795)', 'Akiba lanterns along the Tokaido (mostly 19th c.)', 'electric glow'])

add('Street and shop front', id='jp_s_stall', name='Stall family: reed-screen stall, board booth (kake-mise), roofed street stall (yatai)',
    what='Temporary stalls from one set of poles, reed panels, board counters and mat roofs: tea stands, market booths and the night yatai.',
    importance='standard', tiers=[2, 3], priority='P1', wave=1, effort=0.7,
    period_evidence='reed-screen tea stands and stalls on the riverbank in an uki-e of c.1748 [x31]; yatai 6 shaku wide x 3 shaku deep, no wheels [O18, a late (1837-53) text]; reed-screen stall and kake-mise [OUTDOOR_LIST §2 U Festivals]',
    refs=[R('x31_masanobu_ryogoku_1748', 'reed-screened stalls along the riverbank, c.1748 (background)', True), R('x36_hiroshige_ishibe', 'roadside stands with reed screens (c.1833)', True),
          R('c18_hiroshige_mariko', 'tea-stand context (c.1833)', True)],
    dimensions={
        'yatai_m': D('1.82 wide x 0.91 deep, roof to 2.2, counter 0.85', 'O18 (6 x 3 shaku; late source, used for size only)', None),
        'reed_stall_m': D('1 ken x 1 ken (1.82 x 1.82) poles, reed panels 0.91 x 1.8, board counter 0.8 high', None, 'on the ken grid; assumed'),
        'kake_mise_m': D('1.5 ken x 1 ken plank booth, mat roof at 2.1-2.4', None, 'assumed'),
        'pole_d_m': D('0.06-0.08 (bamboo or thin log)', None, 'assumed'),
    },
    materials=[M('poles', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('reed screens', 'jp_m_reed_yoshizu', 'sudare_reed'),
               M('counters, yatai body', 'jp_m_wood_weathered', 'timber_weathered'), M('mat roof', 'jp_m_straw_mushiro', 'thatch_new'),
               M('lashings', 'jp_m_straw_rope', 'straw_aged')],
    connectors=['proxy_base on terrain; counter top = loot surface; parts snap on a 0.91 grid so stalls join into market rows'],
    variants=[V('_reed', 'reed-screen stall with counter'), V('_booth', 'plank booth (kake-mise)'), V('_yatai', 'roofed yatai, no wheels'),
              V('_row3', 'three reed stalls joined (market row)'), V('_ab_collapsed', 'ABANDONED: roof mat fallen in, one pole snapped, screens flattened'),
              V('_ab_frame', 'ABANDONED: bare pole frame, screens gone (the hai-chaya ruin state)')],
    abandoned='Temporary structures collapse first: mats fallen in, screens flattened or blown away, frames leaning; yatai stand but with rotted counters.',
    families=['Stall family (yoshizu stall, yatai, kake-mise)', 'Reed screens (yoshizu) at stands', 'Reed fence / yoshizu screens', 'Periodic market set'],
    placement='At bridge ends, riverbanks, temple approaches and post-town edges; in rows of 3-8 on market days; yatai at street corners. Never in front of a permanent shop door.',
    lod_budget='medium site object <=1,500 faces LOD0 for the yatai; reed stall <=600')

add('Street and shop front', id='jp_s_nobori', name='Banner pole (nobori): cloth banner on a bamboo pole with a crossbar, shop and shrine',
    what='The tall narrow banner on a bamboo pole: shops, shrine approaches and festivals; a leftover of the autumn festival in the dead world.',
    importance='filler', tiers=[1, 2, 3], priority='P2', wave=1, effort=0.3,
    period_evidence='shop and shrine banners on bamboo poles with a sideways crossbar [OUTDOOR_LIST §2 U / R §14, S206]; carp streamers are a period trap (KEEP_OUTDOOR)',
    refs=[R('k39_nobori_hiko', 'row of shrine nobori (photo)'), R('x36_hiroshige_ishibe', 'roadside context (c.1833)', True)],
    dimensions={
        'banner_m': D('0.45 x 3.0-4.5', None, 'shop banners about 1.5 shaku wide; assumed'),
        'pole_m': D('bamboo 5.0-7.0, crossbar 0.5 at the top', None, 'assumed'),
        'socket': D('pole in a stone socket pair (nobori-tate ishi) or lashed to a post', 'OUTDOOR_LIST §2 W §5', None),
    },
    materials=[M('banner', 'jp_m_textile_kinari', 'kinari_cloth'), M('text', 'jp_m_decal_sumi_text', 'sumi_black'),
               M('indigo banner (variant)', 'jp_m_textile_noren', 'aizome_kon'), M('pole', 'jp_m_bamboo_weathered', 'bamboo_weathered'),
               M('socket stones', 'jp_m_stone_carved', 'stone_lantern')],
    connectors=['proxy_base on terrain in a socket stone or against a post'],
    variants=[V('_shop', 'shop banner'), V('_shrine', 'shrine banner, pair'), V('_socket_stones', 'socket stones only (banner taken down)'),
              V('_ab_tattered', 'ABANDONED (default): banner shredded to a strip, pole leaning'), V('_ab_down', 'ABANDONED: pole fallen across the approach')],
    abandoned='Left up after the autumn festival: shredded to strips, poles leaning in their sockets, some fallen across the approach.',
    families=['Festival layer (nobori, lanterns, mikoshi, stages)', 'Banner-pole socket stones'],
    placement='Pairs at shrine approaches and ward entrances; singly at shop fronts; rows along a sando only at the hero shrine.',
    lod_budget='small prop <=300 faces LOD0; cloth two-sided',
    banned_tells_to_watch=['carp streamers (koinobori)', 'printed synthetic banners'])

# ================================================================= SHRINE, TEMPLE, GRAVEYARD (wave 2)
add('Shrine, temple and graveyard', id='jp_s_torii_wood', name='Wooden torii (ki-no-torii): shinmei and myojin forms, plain or vermilion',
    what='The unpainted wooden gate at a village shrine approach; the vermilion myojin form for Inari and Hachiman; a miniature for yard shrines.',
    importance='standard', tiers=[1, 2, 3], status_overlay='religious', priority='P2', wave=2, effort=0.7,
    period_evidence='unpainted shinmei or myojin wooden torii at village shrines [OUTDOOR_LIST §2 R §10]; vermilion torii at Inari and Hachiman [U]; wooden torii at Hida (photo) [k27]',
    refs=[R('k27_hida_torii', 'unpainted wooden torii (photo)'), R('c10_inari_torii', 'shu vermilion and sumi black on torii'),
          R('k02_bunken_ezu_p12', 'roadside shrine torii marks on the 1690 Tokaido map', True)],
    dimensions={
        'village_m': D('post span 1.8-2.7 (1-1.5 ken), height 2.7-3.6, post d 0.20-0.25', 'O11, O12 (stone torii of the same village class: 1.82 span x 2.71 h; 2.5 x 2.8)', None),
        'mini_m': D('span 0.6, height 0.9 (yard shrine)', None, 'assumed'),
        'kasagi_overhang_m': D('0.35-0.50 past each post', None, 'assumed from proportion drawings'),
        'grid': D('span in half-ken steps so the sando kit lines up', None, 'PLAYBOOK rule 9'),
    },
    materials=[M('posts, beams', 'jp_m_wood_weathered', 'timber_weathered'), M('vermilion (variant)', 'jp_m_paint_shu', 'shu_vermilion'),
               M('kasagi top black (vermilion variant)', 'jp_m_wood_kuro', 'kuro_board'), M('plaque', 'jp_m_decal_sumi_text', 'sumi_black'),
               M('moss', 'jp_m_decal_moss', 'moss_on_stone'), M('post footing stones', 'jp_m_stone_field', 'stone_granite')],
    connectors=['proxy_base on terrain, posts on footing stones; memory points on the tie-beam for jp_s_shimenawa'],
    variants=[V('_shinmei', 'straight lintel, no overhanging tie-beam (plain wood)'), V('_myojin', 'upswept kasagi, tie-beam with centre strut'),
              V('_myojin_shu', 'vermilion myojin with black kasagi (Inari, Hachiman; restricted colour)'), V('_mini', 'yard-shrine miniature'),
              V('_ab_leaning', 'ABANDONED: vermilion peeled to grey wood, one post rotted at the foot and leaning, kasagi sagging')],
    abandoned='Wood torii weather fast: vermilion peeled in patches, the plain ones silver-grey with moss on the kasagi; one in five leans on a rotted post.',
    families=['Wooden torii', 'Vermilion torii (Inari)', 'Yard shrine + mini torii + offering stand', 'Numbered mountain-path torii / lone forest torii'],
    placement='At the start of a shrine approach, square to the path; vermilion only at Inari and Hachiman shrines; mini torii only before a yard shrine.',
    lod_budget='medium site object <=1,500 faces LOD0 (decision 9); kasagi curve and silhouette in every LOD',
    banned_tells_to_watch=['dense senbon torii tunnels (mostly later)', 'three-legged torii (1831)', 'modern bright paint'])

add('Shrine, temple and graveyard', id='jp_s_torii_stone', name='Stone torii (ishi-torii): granite myojin form with donor inscription',
    what='The granite torii donated by villagers or pilgrim groups, usually myojin form with names and a date on a post.',
    importance='standard', tiers=[2, 3], status_overlay='religious', priority='P2', wave=2, effort=0.6,
    period_evidence='Okazaki myojin stone torii: 2.71 m high, 1.815 m span, granite, one-piece kasagi [O11]; Kawataka Sumiyoshi: span 2.5, height 2.8 [O12]; Motoki stone torii (Heian, 3.51 m) still standing [O13]; Toshogu stone torii repaired Kyoho 19 (1734) [O15]',
    refs=[R('k40_motoki_torii', 'Motoki stone torii, Yamagata: Heian myojin form still standing (photo)'), R('c09_himeji', 'granite colour context')],
    dimensions={
        'small_m': D('span 1.82, height 2.71', 'O11', None),
        'medium_m': D('span 2.5, height 2.8 (posts nearly as thick as the span suggests: squat)', 'O12', None),
        'large_m': D('span 2.7-3.6, height 3.5-4.5 (town shrines)', 'O13 (3.51 m high)', None),
        'post_d_m': D('0.30-0.40, slight batter inward', None, 'assumed from k22'),
    },
    materials=[M('stone', 'jp_m_stone_cut', 'stone_granite'), M('weathered stone (old)', 'jp_m_stone_carved', 'stone_lantern'),
               M('donor text', 'jp_m_decal_carved_text', 'stone_lantern'), M('moss and lichen', 'jp_m_decal_moss', 'moss_on_stone')],
    connectors=['proxy_base on terrain; tie-beam memory points for jp_s_shimenawa'],
    variants=[V('_s', 'span 1.82 (village)'), V('_m', 'span 2.5'), V('_l', 'span 3.6 (town)'),
              V('_ab_broken', 'ABANDONED (rare): kasagi fallen in two pieces beside the posts (quake)')],
    abandoned='Unchanged but for lichen streaks under the kasagi and moss on its top; one broken by a quake as a landmark oddity.',
    families=['Stone torii', 'Sea torii'],
    placement='At town shrine approaches and at the first torii of a sando; a village shrine gets either stone or wood, not both.',
    lod_budget='medium site object <=1,500 faces LOD0', checks=CK_STONE,
    banned_tells_to_watch=['shrine-name stone pillars and donor stone fences (mostly Meiji; use names on the torii post instead)'])

add('Shrine, temple and graveyard', id='jp_s_stone_lantern', name='Stone lantern (ishi-doro): Kasuga, square standing and small placed types, 3 heights',
    what='The donated stone lantern flanking shrine and temple approaches, in pairs or rows; also the courtyard-garden lantern and the tall always-lit lantern.',
    importance='standard', tiers=[2, 3], status_overlay='religious', priority='P2', wave=2, effort=0.8,
    period_evidence='Kasuga-type lanterns flanking approaches, commoner donation in the Edo period [OUTDOOR_LIST §2 R §10, S100]; Kasuga proportions (10 shaku): hoju+ukebana 2.0, kasa 1.3, hibukuro 1.7, chudai 1.0, sao 3.6, kiso 0.5 [O10]; always-lit lantern type in by 1625 (Miya) [§3.3]',
    refs=[R('c22_kasuga_lanterns', 'Kasuga lanterns: weathered granite and moss'), R('k23_kasuga_lanterns', 'row of Kasuga Taisha stone lanterns (photo)'),
          R('k16_morse_toro_tokio', 'stone lantern in Tokyo (Morse 1885)'), R('k17_morse_toro_utsunomiya', 'stone lantern in Utsunomiya (Morse 1885)')],
    dimensions={
        'kasuga_proportion': D('of total height: hoju 0.20, kasa 0.13, hibukuro 0.17, chudai 0.10, sao 0.36, kiso 0.05', 'O10', None),
        'heights_m': D('1.8 (6 shaku), 2.4 (8 shaku), 3.0 (10 shaku)', None, 'standard mason sizes by the shaku; the 3 heights of OUTDOOR_LIST §7.7'),
        'square_m': D('square standing lantern 1.8-2.4, square fire box', None, 'OUTDOOR_LIST §2 U (assumed common Edo form)'),
        'oki_m': D('placed lantern 0.6-0.9 on a stone', None, 'assumed'),
    },
    materials=[M('stone', 'jp_m_stone_carved', 'stone_lantern'), M('donor text and date', 'jp_m_decal_carved_text', 'stone_lantern'),
               M('moss and lichen', 'jp_m_decal_moss', 'moss_on_stone'), M('fire-box paper screen (rare)', 'jp_m_paper_shoji', 'washi_shoji')],
    connectors=['proxy_base on terrain; pairs mirrored across the approach centreline'],
    variants=[V('_kasuga_18', 'Kasuga 1.8'), V('_kasuga_24', 'Kasuga 2.4'), V('_kasuga_30', 'Kasuga 3.0'), V('_square_24', 'square standing 2.4'),
              V('_oki', 'small placed lantern (courtyard)'), V('_joyato', 'tall always-lit lantern on a 2-step base, 4.0 (jōyatō; not the very tall 19th-c. towers)'),
              V('_ab_toppled', 'ABANDONED: hoju and kasa fallen beside the post (quake), the most common stone-lantern ruin')],
    abandoned='Stone lanterns shed their top parts in quakes: 1 in 6 has its hoju or kasa on the ground beside it; the rest are dark, lichen-streaked and mossy on the roof.',
    families=['Stone lantern pair / approach lanterns', 'Always-lit lantern (jōyatō)', 'Courtyard garden kit (lantern, basin, stones)'],
    placement='In mirrored pairs at the torii and the hall steps; rows of 4-20 on town approaches (landmark only); single oki-doro in courtyard gardens.',
    lod_budget='small prop <=300 faces LOD0 (1.8), <=600 (3.0 and joyato)', checks=CK_STONE,
    banned_tells_to_watch=['very tall stone night-lamp towers (19th c.)', 'Konpira lantern boom (later)', 'lit lanterns'])

add('Shrine, temple and graveyard', id='jp_s_stone_steps', name='Stone steps (ishidan): straight flight modules, landing, side stones; rough and dressed',
    what='Modular stone flights for shrine hills, temple approaches, stepped lanes and pass pitches: terrain-matched segments with a Roadway ramp.',
    importance='standard', tiers=[1, 2, 3], priority='P2', wave=2, effort=0.6,
    period_evidence='rough or dressed stone flights on pass pitches, shrine hills and stepped lanes [OUTDOOR_LIST §2 W §2, S060]; Hakone paving 1680 [PLAYBOOK §1]',
    refs=[R('k38_shrine_steps', 'stone steps in a shrine precinct (photo)'), R('k40_motoki_torii', 'torii on a rural approach: ground and step context')],
    dimensions={
        'rise_m': D('0.15-0.18', None, 'comfortable for players and infected; matches shrine stairs'),
        'tread_m': D('0.30-0.36', None, 'rise/tread 0.18/0.30 = 31 deg, under the 38 deg walk limit (PLAYBOOK T9)'),
        'width_m': D('0.91, 1.82, 2.73 (half, 1, 1.5 ken)', None, 'grid (rule 9)'),
        'module': D('flights of 3 and 6 steps, landing 1.82 deep, side cheek stones', None, 'assumed; chains up any slope'),
    },
    materials=[M('dressed steps', 'jp_m_stone_cut', 'stone_granite'), M('rough steps', 'jp_m_stone_field', 'stone_granite'),
               M('moss in joints', 'jp_m_decal_moss', 'moss_on_stone'), M('leaf litter on treads', 'jp_m_ground_leaf_litter', 'leaf_litter_autumn')],
    connectors=['stair_foot / stair_head connectors like the building stair parts (PLAYBOOK §10.2); Roadway ramp <=38 deg'],
    variants=[V('_dressed_3', 'dressed, 3 steps'), V('_dressed_6', 'dressed, 6 steps'), V('_rough_3', 'rough field stones, 3 steps'),
              V('_landing', 'landing slab'), V('_cheek', 'side cheek stones'), V('_ab_heaved', 'ABANDONED: treads tilted by roots, one step missing, leaves drifted')],
    abandoned='Treads tilted by roots and frost, leaves drifted on every step, moss in the joints, grass up the sides.',
    families=['Stone steps', 'Switchbacks / log steps / cross drains', 'Shrine approach (sandō)'],
    placement='Only where the terrain rises more than 0.5 m between an approach and its hall or between lane levels; seated into the terrain, never floating.',
    lod_budget='small prop <=300 faces LOD0 per module', checks=['C1', 'C2', 'C4', 'C5', 'C6', 'C7', 'C8'],
    open_questions=['C7 applies: stairs <=38 deg and Roadway continuous across module joins (walkability).'])

add('Shrine, temple and graveyard', id='jp_s_grave_stones', name='Graveyard stones: the 1730 mix (board-shaped, boat-halo, round-headed, square pillar, gorinto, hokyointo)',
    what='The gravestone family that dresses temple, village and roadside graveyards in the 1730 proportions, sharing shapes with the stele family.',
    importance='standard', tiers=[1, 2, 3], status_overlay='religious', priority='P2', wave=2, effort=0.8,
    period_evidence='board-shaped stones (itabi-gata) peak 1660s-90s and decline in the Kyoho era (1720s); round-headed stones from Kyoho on; pointed pillars appear Kyoho, peak c.1800 [O05]; boat-halo figure stones from the late Kan-ei era, large until Kyoho [O06]; no family-name stones (Meiji) [OUTDOOR_LIST §6]',
    refs=[R('c24_jizo_cemetery', 'Jizo and gravestones, weathered stone'), R('k25_gorinto', 'gorinto five-ring stupa (photo)'),
          R('k26_gorinto_gamou', 'large gorinto grave (photo)')],
    dimensions={
        'board_shaped_m': D('0.6-0.9 high x 0.30 x 0.15, pointed-arch top, on 1-2 bases', None, 'O05 gives the dating, not sizes; sizes assumed from surveyed examples'),
        'boat_halo_m': D('0.5-0.9 high, figure in relief', 'O06 (form, dating); size assumed', None),
        'round_headed_m': D('0.6-0.9 high x 0.30 x 0.20 (kushigata)', None, 'assumed'),
        'square_pillar_m': D('0.6-0.9 shaft + 2-3 bases 0.15 each', None, 'rising, rare in 1730 (OUTDOOR_LIST §3.3)'),
        'gorinto_m': D('0.6 (commoner) to 2.0 (samurai)', None, 'assumed'),
        'mix_1730': D('board 35 %, boat-halo 30 %, round-headed 20 %, square pillar 5 %, gorinto / hokyointo 10 %', 'O05, O06, OUTDOOR_LIST §3.3 (reading)', None),
    },
    materials=[M('stone', 'jp_m_stone_carved', 'stone_lantern'), M('carved names and dates', 'jp_m_decal_carved_text', 'stone_lantern'),
               M('moss and lichen', 'jp_m_decal_moss', 'moss_on_stone'), M('base stones', 'jp_m_stone_cut', 'stone_granite')],
    connectors=['proxy_base on terrain; stones on a 0.9 x 0.9 plot grid in rows, paths 0.9'],
    variants=[V('_board', 'board-shaped (itabi-gata)'), V('_boat_halo', 'boat-halo with Jizo or Amida relief'), V('_round', 'round-headed (kushigata)'),
              V('_pillar', 'square pillar on bases (rare)'), V('_gorinto_s', 'gorinto 0.6'), V('_gorinto_l', 'gorinto 2.0'), V('_hokyointo', 'hokyointo 1.5 (samurai / priest)'),
              V('_ab_leaning', 'ABANDONED: leaning, sunk, a gorinto with its top rings fallen')],
    abandoned='Graves are the one place that looks almost as before: lichen and moss heavier, some stones leaning, gorinto top rings fallen; weeds between plots.',
    families=['Graveyard kit (stones, sotoba, buckets, flower tubes, incense)', 'Gorintō / hōkyōin-tō', "Traveller's grave / horse grave"],
    placement='Behind or beside temples on slopes, in rows facing the path; family graves at field edges in the Kanto (2-6 stones); single traveller graves by roads.',
    lod_budget='small prop <=300 faces LOD0 per stone', checks=CK_STONE,
    banned_tells_to_watch=['"X family grave" inscriptions (Meiji)', 'polished black granite', 'dense square-pillar rows (a later look)'])

add('Shrine, temple and graveyard', id='jp_s_grave_wood', name='Graveyard wood set: sotoba slats and rack, flower tubes, incense stand, bucket rack',
    what='The wooden and small furniture of a graveyard: tall notched memorial slats behind stones, their rack, bamboo flower tubes, stone incense stands and the bucket-and-ladle rack.',
    importance='filler', tiers=[1, 2, 3], status_overlay='religious', priority='P2', wave=2, effort=0.4,
    period_evidence='sotoba slats behind graves and in racks [OUTDOOR_LIST §2 R §11, S102]; bucket and ladle rack, flower tubes, incense stands [S197-S199]; itatoba 0.6-1.8 m, about 1 cm thick [O16]',
    refs=[R('c24_jizo_cemetery', 'graveyard context'), R('k30_rokujizo', 'six-Jizo row at a graveyard edge (photo)')],
    dimensions={
        'sotoba_m': D('1.05 x 0.075 x 0.009 (3.5 shaku); range 0.6-1.8', 'O16 (modern practice; form unchanged)', None),
        'rack_m': D('1.82 long x 1.0 high rail frame', None, 'assumed'),
        'flower_tube_m': D('bamboo d 0.06 x 0.30, in pairs', None, 'assumed'),
        'bucket_rack_m': D('0.91 x 0.3 shelf on posts, 1.0 high, 4-6 teoke', None, 'reuses jp_s_oke _teoke'),
    },
    materials=[M('sotoba', 'jp_m_wood_weathered', 'timber_weathered'), M('sotoba text', 'jp_m_decal_sumi_text', 'sumi_black'),
               M('flower tubes', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('incense stand', 'jp_m_stone_carved', 'stone_lantern')],
    connectors=['proxy_base on terrain behind or before jp_s_grave_stones'],
    variants=[V('_sotoba_x3', '3 slats behind a stone'), V('_rack', 'slat rack with 6-12 slats'), V('_tubes', 'flower tube pair with dead shikimi'),
              V('_incense', 'stone incense stand'), V('_bucket_rack', 'bucket and ladle rack'), V('_ab_fallen', 'ABANDONED (default): slats grey, split, half fallen; tubes empty')],
    abandoned='Slats grey, split and fallen across the stones, their ink gone; flower tubes empty or holding dead black stems; rack leaning.',
    families=['Graveyard kit (stones, sotoba, buckets, flower tubes, incense)'],
    placement='Slats behind about 1 grave in 3; one rack and one bucket rack per graveyard by its water point.',
    lod_budget='small prop <=300 faces LOD0 per piece')

# ------------------------------------------------------------------------------------------------ materials
# status: 'existing' = already in src/JP/common/materials; 'new' = the materials agent makes it (materials_needed.json)
MAT = {
 # existing jp_common (reused as is)
 'jp_m_wood_weathered': dict(status='existing', family='wood', palette='timber_weathered'),
 'jp_m_wood_street_dark': dict(status='existing', family='wood', palette='timber_street_dark'),
 'jp_m_wood_kuro': dict(status='existing', family='wood', palette='kuro_board'),
 'jp_m_bamboo_weathered': dict(status='existing', family='bamboo', palette='bamboo_weathered'),
 'jp_m_metal_iron': dict(status='existing', family='metal', palette='iron_black'),
 'jp_m_stone_cut': dict(status='existing', family='stone', palette='stone_granite'),
 'jp_m_stone_field': dict(status='existing', family='stone', palette='stone_granite'),
 'jp_m_stone_river': dict(status='existing', family='stone', palette='stone_lantern'),
 'jp_m_roof_kureita': dict(status='existing', family='roof', palette='roof_board_silver'),
 'jp_m_straw_mushiro': dict(status='existing', family='straw', palette='thatch_new'),
 'jp_m_paper_shoji': dict(status='existing', family='paper', palette='washi_shoji'),
 # new
 'jp_m_stone_carved': dict(status='new', family='stone', palette='stone_lantern', tile=1.0, ppm=512, grain='none; softened tool marks', pen='granite', finish='matte',
     wear=('fresh-cut grey granite/andesite, crisp chisel marks', 'darkened, lichen spots (grey-green, orange), grime in carving', 'heavy moss on tops and north faces (W6), black lichen streaks'),
     source='Poly Haven rock_surface / worn_rock_natural_01 (already downloaded for jp_m_stone_cut) regraded to stone_lantern; or an ambientCG CC0 granite',
     note='THE weathered stone for figures, steles, lanterns, gravestones and basins; the palette entry was sampled from Kasuga lanterns (c22)'),
 'jp_m_decal_moss': dict(status='new', family='stone', palette='moss_on_stone', tile=0.5, ppm=512, grain='none; alpha-tested patches', pen='(visual only)', finish='matte, alpha test',
     wear=('thin lichen spots', 'moss cushions on top faces', 'thick moss with dead leaves caught in it'),
     source='procedural (numpy noise masks) over an ambientCG CC0 moss colour, like make_textures.py',
     note='Moss and lichen as separate alpha decal geometry laid on tops of stones, torii kasagi, lantern roofs and north faces: variety without a second UV set (decision 10)'),
 'jp_m_decal_carved_text': dict(status='new', family='stone', palette='stone_lantern', tile=1.0, ppm=1024, grain='none', pen='(visual only)', finish='matte, alpha test + normal',
     wear=('sharp V-cut characters', 'softened, grime in the cuts', 'lichen over half the text'),
     source='rendered from an SIL OFL brush font into height -> normal + AO (decision 5); the text list is the jp_s_stele "text" dimension',
     note='Carved inscriptions (Koshin, namu amida butsu, directions, donor names, era dates Genroku-Kyoho) as 2 mm proud decal faces'),
 'jp_m_decal_sumi_text': dict(status='new', family='paint', palette='sumi_black', tile=1.0, ppm=1024, grain='brush strokes', pen='(visual only)', finish='matte, alpha test',
     wear=('crisp black ink', 'faded to grey-brown', 'ghost of text, flaking'),
     source='rendered from an SIL OFL brush font (decision 5)',
     note='Ink text atlas: shop names, inn names, house marks, edict lines, sotoba text, banner text'),
 'jp_m_straw_rope': dict(status='new', family='straw', palette='straw_aged', tile=0.5, ppm=512, grain='twist along the rope', pen='hay', finish='matte',
     wear=('golden new straw', 'grey-gold', 'grey-brown, frayed, dark ends'),
     source='procedural twist over a Poly Haven / ambientCG CC0 straw or hay scan',
     note='shimenawa, well ropes, bundle ties, lashings, bale ropes'),
 'jp_m_straw_stack': dict(status='new', family='straw', palette='straw_aged', tile=1.0, ppm=256, grain='stalks down the stack face; heads inward', pen='hay', finish='matte',
     wear=('fresh harvest gold', 'grey-gold weathered top', 'grey-black top with moss, slumped'),
     source='Poly Haven reed_roof_04 (already downloaded) regraded lighter, or a CC0 hay scan',
     note='straw stacks, stooks, bundles, bale ends'),
 'jp_m_textile_noren': dict(status='new', family='textile', palette='aizome_kon', tile=1.0, ppm=512, grain='plain cotton weave', pen='cloth (vanilla penetration for textiles; B to confirm the rvmat name)', finish='matte, two-sided, alpha for tears',
     wear=('deep indigo with white resist marks', 'faded, sun-bleached folds', 'grey-blue, torn hem (alpha), stains'),
     source='procedural weave + indigo from the aizome palette; 4 shop-mark resist designs',
     note='noren, indigo banners, indigo laundry'),
 'jp_m_textile_kinari': dict(status='new', family='textile', palette='kinari_cloth', tile=1.0, ppm=512, grain='plain cotton / hemp weave', pen='cloth (as above)', finish='matte, two-sided, alpha for tears',
     wear=('undyed cream', 'grey, mildew spots', 'grey-brown, shredded (alpha)'),
     source='procedural weave, or an ambientCG CC0 fabric regraded',
     note='nobori, laundry, Jizo bibs (plus a faded red tint variant), mizuhiki noren'),
 'jp_m_paper_chochin': dict(status='new', family='paper', palette='washi_shoji', tile=1.0, ppm=512, grain='fibres; rib shadows', pen='fabric_thin', finish='matte, alpha for holes',
     wear=('oiled warm white with black text', 'yellowed, water-stained', 'split and holed (alpha), ribs showing'),
     source='procedural from jp_m_paper_shoji plus a rib-shadow pass',
     note='chochin and andon paper; never emissive (no light in the dead world)'),
 'jp_m_reed_yoshizu': dict(status='new', family='straw', palette='sudare_reed', tile=1.0, ppm=512, grain='vertical reeds, tied every 0.3', pen='hay', finish='matte, alpha for gaps',
     wear=('pale reed', 'grey reed', 'broken reeds, holes'),
     source='procedural reed strips over the jp_m_roof_thatch source; palette sudare_reed already sampled',
     note='reed screens (stalls, fences) and sudare blinds'),
 'jp_m_paint_shu': dict(status='new', family='paint', palette='shu_vermilion', tile=2.0, ppm=512, grain='along member under the paint', pen='wood', finish='matte',
     wear=('even vermilion', 'chalky, darkened, edges worn to wood', 'peeling in patches to grey wood (toward timber_weathered, max 0.4)'),
     source='jp_m_wood_weathered grain under a vermilion layer (like jp_m_wood_bengara)',
     note='RESTRICTED: shrines only (PLAYBOOK §8): vermilion torii, yard-shrine mini torii'),
 'jp_m_wood_endgrain': dict(status='new', family='wood', palette='timber_weathered', tile=0.5, ppm=512, grain='growth rings, radial checks', pen='wood', finish='matte',
     wear=('fresh cut, pale rings', 'greyed rings, checks', 'dark, split, lichen'),
     source='Poly Haven or ambientCG CC0 log end-grain scan',
     note='firewood ends, post tops, beam ends'),
 'jp_m_ground_leaf_litter': dict(status='new', family='ground', palette='leaf_litter_autumn', tile=1.0, ppm=256, grain='none', pen='dirt', finish='matte',
     wear=('fresh autumn leaves (red, yellow, brown)', 'brown leaves in silt', 'black rotted leaves and mud'),
     source='ambientCG CC0 forest-floor / leaves scan regraded to autumn (maple, zelkova, ginkgo colours)',
     note='The abandoned layer: gutter beds, tub bottoms, basin hollows, step treads, Jizo huts; AUTUMN'),
}

REQ_PAL = [
 dict(id='straw_aged', method='sampled', tolerance_dE76=14, ref='k34_straw_rice', box=[0.30, 0.35, 0.70, 0.75], select='mid 70 % luminance',
      fallback_srgb=[150, 131, 98],
      why='Straw rope, stacks and bundles one season old: lighter and warmer than roof thatch_weathered (70,60,58), greyer than thatch_new (176,150,98, assumed). Sampled from an October photo of rice straw (PD, k34) once it is downloaded.'),
 dict(id='leaf_litter_autumn', srgb=[96, 70, 46], method='assumed', tolerance_dE76=14, samples=[],
      why='Mean of mixed wet autumn leaf litter; needs a licensed sample (an ambientCG CC0 leaf scan will do) before the material ships.'),
]

# ------------------------------------------------------------------------------------------------ refs
IMG_NOTE = ''
IMG_SUPPORTS = {
 'k02_bunken_ezu_p12': 'Tokaido bunken ezu (1690, Hishikawa Moronobu): the road near Hara with pine avenue, mile mound and a roadside marker (schematic)',
 'k05_moronobu_street_1680': 'Hishikawa Moronobu, Yoshiwara street scene, c.1680 (MET, CC0): lattice front, short noren, a porter with a load',
 'k06_moronobu_ageyamachi': 'Hishikawa Moronobu, entrance to Ageya-machi, c.1680: split noren with crests along the eave, a low plank bench-platform with goods, two baskets from a carrying pole, stone-weighted board roofs',
 'k09_masanobu_ishiyama_1740': 'Okumura Masanobu, perspective print, 1740 (Cleveland, CC0): rolled sudare tied up under the eaves',
 'k10_morse_well_frame': 'Morse 1885 fig. 289: wooden well-frame with pulley',
 'k11_morse_well_rustic': 'Morse 1885 fig. 290: rustic well-frame',
 'k12_morse_well_kaga': 'Morse 1885 fig. 293: roofed well at the Kaga yashiki, Tokyo',
 'k13_morse_well_curb_old': 'Morse 1885 fig. 287: ancient form of wooden well-curb (igeta)',
 'k14_morse_well_curb_stone': 'Morse 1885 fig. 288: stone well-curb in a private garden',
 'k15_morse_chozubachi': 'Morse 1885 fig. 240: stone water basin (chozubachi)',
 'k16_morse_toro_tokio': 'Morse 1885 fig. 264: stone lantern in Tokyo',
 'k17_morse_toro_utsunomiya': 'Morse 1885 fig. 267: stone lantern in Utsunomiya',
 'k19_koshinto': 'inscribed Koshin stone, Nikko (photo, PD)',
 'k40_motoki_torii': 'Motoki stone torii, Yamagata, Heian period, still standing (photo, CC BY 4.0)',
 'k41_koshin_sendabori': 'Sendabori Koshin stones, Kanegasaku, Matsudo (photo, CC0)',
 'k20_kosatsuba_kashiwabara': 'site of the Kashiwabara-juku kosatsuba (photo, CC0)',
 'k21_edo_bousui': 'fire tub with a bucket pyramid, Fukagawa Edo Museum street reconstruction (photo, CC BY 2.5)',
 'k22_hirakata_jinja': 'Hirakata shrine, Matsudo: donated fire tub (tensui-oke) with a donor mark (photo, CC0)',
 'k23_kasuga_lanterns': 'stone lanterns at Kasuga Taisha (photo, CC BY 4.0)',
 'k24_chozubachi': 'chozubachi with ladles at a shrine (photo, CC BY 3.0)',
 'k25_gorinto': 'gorinto five-ring stupa (photo, PD)',
 'k26_gorinto_gamou': 'large gorinto grave of Gamo Ujisato, Kotoku-ji (photo, CC0)',
 'k27_hida_torii': 'unpainted wooden torii, Hida (photo, PD)',
 'k28_kusakabe_peddler': 'Kusakabe Kimbei, vegetable peddler with pole and baskets, 1880s (PD)',
 'k29_hiroshige_numazu': 'Utagawa Hiroshige, Numazu (Kyoka Tokaido), 1838-42 (San Diego Museum of Art, PD): Tokaido post station with a notice board and a tea house',
 'k30_rokujizo': 'six stone Jizo figures in a row (rokujizo sekibutsu; photo, CC0)',
 'k31_daihachi_uzumasa': 'daihachi-guruma on the Toei Uzumasa Edo street set (photo, PD)',
 'k32_harunobu_well': "Suzuki Harunobu (d. 1770), At the well on New Year's morning (MET, PD; the Commons date '1799' cannot be right): well frame with pulley, wooden buckets, a tub",
 'k33_harunobu_araihari_1767': 'Suzuki Harunobu, Araihari (cloth stretching), 1767 (LoC, PD): laundry yard, tubs',
 'k34_straw_rice': 'rice straw drying in a harvested field, 9 October 2008 (photo, PD): straw_aged sample',
 'k35_firewood_hoshigaki': 'firewood stacked under an eave with persimmons drying, Iwate, November (photo, CC BY 2.0)',
 'k36_firewood_motai': 'Motai-juku, Saku (Nakasendo): firewood along a house (photo, CC BY 2.0)',
 'k37_shimenawa_tree': 'sacred tree with shimenawa, Shikaumi shrine (photo, CC BY 4.0)',
 'k38_shrine_steps': 'stone steps, Kashima Daijingu, Koriyama (photo, CC BY 4.0)',
 'k39_nobori_hiko': 'shrine banners, Hiko shrine (photo, CC BY 4.0)',
}
EXT_REUSED = ['x27_morse_village_yamashiro', 'x30_shinagawa_1726', 'x31_masanobu_ryogoku_1748', 'x33_jinrin_bookseller_1690',
              'x36_hiroshige_ishibe', 'x37_eisen_narai', 'x38_morse_gutter']
TEXT = [
 ('O01', 'https://www.gotokyo.org/jp/spot/968/index.html', 'Fuchu kosatsuba (Koshu road x Kawagoe road), a surviving Edo-period notice board: 4.6 m wide, about 5 m high, roofed; general kosatsuba 3-4 m high, 3-5 m wide (with jinriki.info/kaidolist/yogo/kosatsuba.html). Read via search summary'),
 ('O03', 'https://www.gakken.jp/kagakusouken/spread/oedo/06/kaisetsu1.html', 'Edo town fire-fighting: big tubs of about 6 koku at street crossings with hand buckets stacked on top; houses keep tensui-oke and buckets filled. Read via search summary (it misstates 6 koku as 108 L; 6 koku = about 1,080 L)'),
 ('O04', 'https://www.chiba-muse.or.jp/MURA/digitalmuseum/machinami/all_8.html', 'Chiba prefectural museum, street facilities: daihachi-guruma bed 8 shaku x 2.5 shaku, wheel 3.5 shaku, from after the 1657 fire; carts branded at Denmacho 1700-03 (2,239 carts); roads 4 ken; wells, tensui-oke, kosatsuba, kido listed'),
 ('O05', 'https://www.lib.city.funabashi.lg.jp/viewer/info.html?idSubTop=2&id=396', 'Funabashi library: gravestone chronology. Board-shaped (itabi-gata) from the 1620s, peak 1660s-90s, declining in the Kyoho era (1720s); round-headed from Kyoho, peak mid-late 18th c.; pointed pillar appears Kyoho, peak late 18th-early 19th c.'),
 ('O06', 'https://www.ris.ac.jp/museum/profile/lvhgqo0000004877-att/magechi20_compressed.pdf', 'Rissho University museum: boat-halo (funagata kohai) figure gravestones from the late Kan-ei era to the late Edo period; large and well carved until about Kyoho, smaller and cruder after; later mostly child graves (Jizo). Read via search summary'),
 ('O07', 'https://www.city.edogawa.tokyo.jp/e_bunkazai/bunkazai/toroku/minzokushiryo106.html', 'Edogawa ward: Shinzo-in standing Shomen Kongo Koshin stone, Genroku 11 (1698), 122 cm, four arms, two attendants, four yasha; Tofuku-in stone said to be Kyoho 12 (1727): sun, moon, Shomen Kongo, demon, two cocks (minzokushiryo107.html). Read via search summary'),
 ('O08', 'https://www.city.nerima.tokyo.jp/kankomoyoshi/annai/rekishiwoshiru/rekishibunkazai/bunkazai/b039.html', 'Nerima ward: round-carved Shomen Kongo Koshin stone, Kyoho 12 (1727), 148 cm. Read via search summary'),
 ('O09', 'https://www.city.hirosaki.aomori.jp/gaiyou/bunkazai/shi/shi83.html', 'Hirosaki: Shomen Kongo Koshin stone, andesite square pillar, 122.5 cm (shaft 94.5 cm, base 28 cm). Read via search summary'),
 ('O10', 'https://www.weblio.jp/content/%E6%98%A5%E6%97%A5%E7%81%AF%E7%B1%A0', 'Kasuga lantern parts (hoju, kasa, hibukuro, chudai, sao, kiso) and a mason\'s proportion for a 10-shaku lantern: 2.0 / 1.3 / 1.7 / 1.0 / 3.6 / 0.5 shaku. Read via search summary'),
 ('O11', 'https://www.city.okazaki.lg.jp/bunka/torikumi_bunka/1004568/1004592/1004595/1004634.html', 'Okazaki city: myojin stone torii, total height 271.0 cm, post span 181.5 cm, granite, one-piece kasagi. Read via search summary'),
 ('O12', 'https://www.city.kato.lg.jp/kakukanogoannai/kyouikushinkoubu/shogaigakushuka/bunkazai/siteibunkazai/kensiteibunkazai/1510384600965.html', 'Kato city: Kawataka Sumiyoshi shrine myojin stone torii, span 2.5 m, height 2.8 m. Read via search summary'),
 ('O13', 'https://ja.wikipedia.org/wiki/%E5%85%83%E6%9C%A8%E3%81%AE%E7%9F%B3%E9%B3%A5%E5%B1%85', 'Motoki stone torii, Yamagata: the oldest surviving torii (Heian), myojin form, 351 cm high'),
 ('O14', 'https://online.bunka.go.jp/heritages/detail/249273', 'Chozubachi inscribed Tenna 2 (1682): height 56.9 cm, top 82.3 x 48.4 cm; with city.takahashi.lg.jp/bunkazai/map/0048.html: Omononushi shrine granite basin 150 x 75 x 75 cm, hollow 35 cm deep, rim 10.7 cm. Read via search summary'),
 ('O15', 'https://online.bunka.go.jp/heritages/detail/184686', 'Toshogu stone myojin torii: donated Kan-ei 10 (1633), repair inscription Kyoho 19 (1734). Read via search summary'),
 ('O16', 'https://sotouba.net/blog/knowledge/stupa/sotouba-size/', 'Sotoba sizes: board sotoba about 1 cm thick, 60-180 cm; a 3.5-shaku slat is 1050 x 75 x 9 mm (modern trade source; the form is old). Read via search summary'),
 ('O17', 'https://ja.wikipedia.org/wiki/%E7%B8%81%E5%8F%B0', 'Endai: bench about 45 cm wide, 160 cm long, 45 cm high, wood or bamboo, general in the Edo period (ukiyo-e); called shogi-dai in Kansai. Read via search summary'),
 ('O18', 'https://nichimen.or.jp/know/zatsugaku/29/', 'Edo yatai after Morisada manko (1837-53, a late source): 6 shaku wide, 3 shaku deep; carried (katsugi) and stand (tachi-uri) types; no wheels. Read via search summary'),
 ('O19', 'https://www.order-noren.com/support/knowledge/', 'Noren sizes (trade source on the old kujira shaku): standard 3 shaku (113 cm), long about 160 cm, half about 56 cm, mizuhiki 30-40 cm unsplit; one panel (haba) about 34 cm, 3 panels usual. Read via search summary'),
 ('O20', 'https://kotobank.jp/word/%E8%97%81%E5%A1%9A-665655', 'Warazuka / nio: threshed straw stacked into a cylinder or cone round a centre pole in the stubble; many regional names (niho, nigo, nyu, noguro). Read via search summary'),
 ('O21', 'https://ja.wikipedia.org/wiki/%E5%A4%A9%E7%A7%A4%E6%A3%92', 'Tenbin-bo: museum poles 152 cm (2.4-6.0 cm wide, 1.5-3.0 thick) and 137 cm; 6 shaku (182 cm) common; loads hung by rope at both ends (with online.bunka.go.jp/heritages/detail/145206). Read via search summary'),
 ('O22', 'https://www.geolab.jp/documents/science/science-159/', 'Wells: dug wells about 1 m across; Edo excavations show shafts lined with stacked bottomless tubs, or dry stone. Read via search summary'),
 ('O23', 'https://ja.wikipedia.org/wiki/%E9%87%A3%E7%93%B6', 'Tsurube: rope tsurube, two buckets on one rope over an upper pulley, pole tsurube, counterweighted hane-tsurube; wooden buckets with iron fittings from the Nara period'),
 ('O24', 'https://www.mizu.gr.jp/kikanshi/no18/02.html', 'Mizkan water culture: Edo drains on lot boundaries in stone or wood, 3-6 shaku wide, covered; wood boards and pipes rot fast and needed regular cleaning. Read via search summary'),
 ('O25', 'https://ja.wikipedia.org/wiki/%E8%A1%8C%E7%81%AF', 'Andon: oki-, kake-, tsuri-, tsuji-andon; kake-andon hung at shop fronts as signs with the shop name; tsuji-andon in front of guard posts as street lights; an Enshu andon about 81 cm high. Read via search summary'),
 ('O27', 'https://www.city.kurashiki.okayama.jp/5407.htm', 'Kurashiki city: Edo-period stone standing Jizo, total 178.0 cm, figure 136.0 cm. Read via search summary'),
]

# ------------------------------------------------------------------------------------------------ settings (§4 of OUTDOOR_LIST)
def read_settings():
    p = os.path.join(ROOT, 'research', 'outdoor', 'OUTDOOR_LIST.md')
    lines = open(p, encoding='utf-8').read().split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('# 4. Setting kits'))
    end = next(i for i, l in enumerate(lines) if l.startswith('# 5. Shared outdoor core kit'))
    S, cur = {}, None
    for l in lines[start:end]:
        m = re.match(r'### (.+)', l)
        if m: cur = m.group(1).strip(); S[cur] = {'core': set(), 'flavour': set()}; continue
        m = re.match(r'- \*\*(Core|Flavour):\*\* (.*)', l)
        if m and cur:
            S[cur][m.group(1).lower()] |= {x.strip() for x in m.group(2).split(' · ')}
    return S

SHORT = {'Rice-farming village (hirachi no mura)': 'rice village', 'New-field village (shinden-mura)': 'new-field village', 'Mountain village (sanson)': 'mountain village',
         'Fishing village (gyoson / ura)': 'fishing village', 'Salt village (coast variant)': 'salt village', 'Post town (shukuba-machi)': 'post town',
         'Intermediate stop (ai-no-shuku, tateba)': 'intermediate stop', 'Castle town (jōkamachi)': 'castle town', 'Jinya town (jinya-machi)': 'jinya town',
         'Great city: Edo, Kyoto, Osaka': 'great city', 'Temple town / shrine-gate town (monzen-machi)': 'temple town', 'Port town (minato-machi)': 'port town',
         'Mining town (kōzan-machi)': 'mining town', 'River-crossing town': 'river-crossing town', 'Hot-spring town (onsen-machi)': 'hot-spring town',
         'Outcast and marginal settlements (neutral)': 'marginal settlement', 'Highway between towns': 'highway', 'Deep wilderness: mountain and forest': 'wild mountain',
         'Deep wilderness: empty coast and river': 'wild coast'}

# ------------------------------------------------------------------------------------------------ build
def validate(bl):
    """Built-in check of the schema's required keys and enums (jsonschema is used as well if installed)."""
    sch = json.load(open(os.path.join(ROOT, 'playbook', 'templates', 'build_list_schema.json'), encoding='utf-8'))
    errs = []
    try:
        import jsonschema
        for e in jsonschema.Draft202012Validator(sch).iter_errors(bl): errs.append('schema: %s at %s' % (e.message, list(e.path)))
        return errs, 'jsonschema'
    except ImportError:
        pass
    for k in sch['required']:
        if k not in bl: errs.append('missing %s' % k)
    it = sch['properties']['entries']['items']
    for e in bl['entries']:
        for k in it['required']:
            if k not in e: errs.append('%s missing %s' % (e.get('id'), k))
        if not re.match(it['properties']['id']['pattern'], e['id']): errs.append('bad id %s' % e['id'])
        for k in ('importance', 'region', 'status_overlay', 'priority'):
            if k in e and e[k] not in it['properties'][k]['enum']: errs.append('%s bad %s' % (e['id'], k))
        for c in e.get('checks', []):
            if not re.match(r'^C[1-9]$', c): errs.append('%s bad check %s' % (e['id'], c))
        for d in e['dimensions'].values():
            if 'value' not in d: errs.append('%s dimension without value' % e['id'])
        if not e['refs'] or not e['variants']: errs.append('%s empty refs/variants' % e['id'])
    if bl['stage'] not in sch['properties']['stage']['enum']: errs.append('bad stage')
    return errs, 'built-in'

def sample_palette(meta_okit):
    """Median of the mid-70 % luminance pixels in a box (the palette method of PLAYBOOK §8)."""
    from PIL import Image
    import numpy as np
    out = {}
    for p in REQ_PAL:
        if p['method'] != 'sampled': continue
        f = meta_okit.get(p['ref'], {}).get('file')
        if not f or not os.path.exists(os.path.join(ROOT, f)):
            continue   # image not downloaded yet (rate limit): the fallback stays, marked pending
        im = Image.open(os.path.join(ROOT, f)).convert('RGB')
        w, h = im.size; b = p['box']
        a = np.asarray(im.crop((int(b[0] * w), int(b[1] * h), int(b[2] * w), int(b[3] * h))), dtype=np.float64).reshape(-1, 3)
        lum = a @ [0.2126, 0.7152, 0.0722]
        lo, hi = np.percentile(lum, [15, 85])
        sel = a[(lum >= lo) & (lum <= hi)]
        out[p['id']] = [int(round(x)) for x in np.median(sel, axis=0)]
    return out

def main():
    meta = json.load(open(os.path.join(ROOT, 'data', 'research_okit', 'meta.json'), encoding='utf-8'))
    meta_ext = json.load(open(os.path.join(ROOT, 'data', 'research_ext', 'meta.json'), encoding='utf-8'))
    pb = json.load(open(os.path.join(ROOT, 'playbook', 'refs_index.json'), encoding='utf-8'))
    pb_ids = {i['id'] for i in pb['images']} | {t['id'] for t in pb['text']}
    errs = []
    images = []
    for rid in sorted(IMG_SUPPORTS):
        if rid not in meta: errs.append('image %s not downloaded (meta.json)' % rid); continue
        m = dict(meta[rid]); m.pop('bytes', None); m['supports'] = IMG_SUPPORTS[rid]
        m['date'] = re.sub(r'date QS.*$', '', m['date']).strip() or 'unknown'
        m.setdefault('status', 'downloaded')
        images.append(m)
    img_ids = {i['id'] for i in images}
    ext_ids = set(EXT_REUSED)
    for x in EXT_REUSED:
        if x not in meta_ext: errs.append('exterior ref %s missing' % x)
    txt_ids = {t[0] for t in TEXT}
    settings = read_settings()
    all_fams = set().union(*[v['core'] | v['flavour'] for v in settings.values()])
    used_refs = set()
    for e in E:
        for r in e['refs']:
            used_refs.add(r['id'])
            if r['id'] not in img_ids | ext_ids | pb_ids: errs.append('unknown ref %s in %s' % (r['id'], e['id']))
        for tok in re.findall(r'\[([^\]]+)\]', e.get('period_evidence', '')):
            for t in re.split(r'[,;]\s*', tok):
                t = t.strip().split(' ')[0]
                if re.match(r'^(O\d\d|T\d\d|k\d\d|x\d\d)$', t) and not (t in txt_ids or t in pb_ids or any(i.startswith(t + '_') for i in img_ids | ext_ids)):
                    errs.append('unknown evidence id %s in %s' % (t, e['id']))
        for d in e['dimensions'].values():
            for t in re.findall(r'\bO\d\db?\b', d.get('source', '')):
                if t.rstrip('b') not in txt_ids: errs.append('unknown dim source %s in %s' % (t, e['id']))
        for m in e['materials']:
            if m['material'] not in MAT: errs.append('material %s missing (%s)' % (m['material'], e['id']))
            elif MAT[m['material']]['palette'] != m['palette_id']: errs.append('palette mismatch %s in %s' % (m['material'], e['id']))
        for f in e['families']:
            if f not in all_fams: errs.append('unknown §4 family "%s" in %s' % (f, e['id']))
    for rid in IMG_SUPPORTS:
        if rid not in used_refs and rid not in [p.get('ref') for p in REQ_PAL]: errs.append('image %s unused' % rid)
    if errs: print('\n'.join(errs)); sys.exit(1)

    # settings per entry, from the §4 kits
    for e in E:
        core, flav = [], []
        for s, v in settings.items():
            fam = set(e['families'])
            if fam & v['core']: core.append(SHORT.get(s, s))
            elif fam & v['flavour']: flav.append(SHORT.get(s, s))
        e['_settings'] = {'core': core, 'flavour': flav}
    sampled = sample_palette(meta)
    for p in REQ_PAL:
        if p['id'] in sampled: p['srgb'] = sampled[p['id']]; p['samples'] = [{'ref': p['ref'], 'box': p['box'], 'select': p['select'], 'value': sampled[p['id']]}]
        elif 'fallback_srgb' in p:
            p['srgb'] = p['fallback_srgb']; p['method'] = 'assumed (sample pending: %s not downloaded yet; rerun fetch_refs.py then this script)' % p['ref']; p['samples'] = []
        p.pop('fallback_srgb', None)

    entries = []
    for e in E:
        d = {k: v for k, v in e.items() if not k.startswith('_') and k not in ('families', 'abandoned', 'placement', 'wave', 'effort')}
        d['abandoned_state'] = e['abandoned']
        d['settings'] = e['_settings']
        d['setting_kit_families'] = e['families']
        d['placement_rule'] = e['placement']
        d['wave'] = e['wave']
        d['effort_sessions'] = e['effort']
        d['research_level'] = e['importance']
        entries.append(d)
    bl = {'category': 'site-outdoor-core-kit', 'version': 1, 'author': AUTHOR, 'date': DATE, 'stage': 'S',
          'scope_note': 'The ~25 most-reused outdoor site objects (OUTDOOR_LIST §5, KEEP_OUTDOOR build-first list): props placed as map objects (JP\\site\\<group>\\, jp_s_*) or as proxies on building variants. Dead world: every entry has an abandoned state. Out of scope: trees and flora (F), fences and walls (later outdoor group), bridges and wells-as-buildings beyond this kit (KEEP_CIVIC), setting-specific props (built with their shell), terrain work.',
          'entries': entries}
    verrs, how = validate(bl)
    if verrs: print('\n'.join(verrs)); sys.exit(1)

    used = {}
    for e in E:
        for m in e['materials']: used.setdefault(m['material'], set()).add(e['id'])
    pal = json.load(open(os.path.join(ROOT, 'playbook', 'palette.json'), encoding='utf-8'))
    pal_ids = {p['id'] for p in pal['entries']}
    req_ids = {p['id'] for p in REQ_PAL}
    new, reused = [], []
    for mid, m in MAT.items():
        if mid not in used: errs.append('material %s unused' % mid)
        if m['palette'] not in pal_ids | req_ids: errs.append('palette %s unknown' % m['palette'])
        lib = os.path.join(ROOT, 'src', 'JP', 'common', 'materials', m['family'], mid + '.json')
        if m['status'] == 'existing' and not os.path.exists(lib): errs.append('existing material %s not in jp_common' % mid)
        if m['status'] == 'new' and os.path.exists(lib): errs.append('new material %s already exists' % mid)
        if m['status'] == 'existing':
            reused.append({'id': mid, 'family': m['family'], 'palette_id': m['palette'], 'used_by': sorted(used.get(mid, []))})
        else:
            w1 = sorted({e['id'] for e in E if e['wave'] == 1 and mid in {x['material'] for x in e['materials']}})
            new.append({'id': mid, 'family': m['family'], 'palette_id': m['palette'],
                        'palette_status': 'existing' if m['palette'] in pal_ids else 'REQUESTED (see requested_palette_entries)',
                        'tile_size_m': m['tile'], 'px_per_m': m['ppm'], 'grain': m['grain'], 'penetration_rvmat': m['pen'], 'finish': m['finish'],
                        'wear': {'_w0': m['wear'][0], '_w1': m['wear'][1], '_w2': m['wear'][2]}, 'source_plan': m['source'], 'note': m['note'],
                        'needed_in_wave': 1 if w1 else 2, 'used_by': sorted(used.get(mid, []))})
    if errs: print('\n'.join(errs)); sys.exit(1)
    mn = {'version': 1, 'date': DATE, 'author': AUTHOR,
          'note': 'Materials jp_common LACKS for the outdoor core kit: one canonical set each, 3 wear levels (_w0 clean, _w1 normal, _w2 heavy), path JP\\common\\materials\\<family>\\ (PLAYBOOK §9). Matte finish per PLAYBOOK T12 (black env, low fresnel). Decals are alpha-tested geometry, not a second UV set. The dead world places _w1/_w2 by default. Check PA2 (interior) for textile and paper duplicates before building.',
          'counts': {'new_materials': len(new), 'texture_sets': 3 * len(new), 'reused_existing': len(reused)},
          'materials': new, 'reused_from_jp_common': reused, 'requested_palette_entries': REQ_PAL}

    refs_index = {'version': 1, 'category': 'site-outdoor-core-kit', 'date': DATE,
                  'note': 'Images local only in data/research_okit/refs/ (never shipped). Ids x.. are in research/exterior/refs_index.json (data/research_ext/refs/); c.., m.., T.. in playbook/refs_index.json. O.. are text sources (cited, not copied). Many O entries were read through a search-engine summary only, which is marked; verify before a hero build.',
                  'download_policy': 'PD / CC0 / CC BY only (no -SA), Wikimedia Commons API, generic User-Agent "JapanDevResearch/1.0 (DayZ mod research)", thumbnails <=1600 px. Credits: research/outdoor_kit/CREDITS.md.',
                  'exterior_ids_reused': sorted(EXT_REUSED), 'playbook_ids_reused': sorted(used_refs & pb_ids),
                  'images': images, 'text': [{'id': a, 'url': b, 'supports': c} for a, b, c in TEXT]}

    wb = lambda p, s: open(os.path.join(OUT, p), 'wb').write(s.encode('utf-8'))
    wb('build_list.json', json.dumps(bl, ensure_ascii=False, indent=1) + '\n')
    wb('materials_needed.json', json.dumps(mn, ensure_ascii=False, indent=1) + '\n')
    wb('refs_index.json', json.dumps(refs_index, ensure_ascii=False, indent=1) + '\n')
    global IMG_NOTE
    nd = sum(1 for m in images if m['status'] == 'downloaded')
    IMG_NOTE = '' if nd == len(images) else (' **Images: %d downloaded, %d picked and licence-checked but linked only:** upload.wikimedia.org rate-limited our generic User-Agent (HTTP 429). `tools/fetch_refs.py` resumes; then rerun this generator (it samples `straw_aged` from k34 then).' % (nd, len(images) - nd))
    wb('BUILD_LIST.md', md(bl, mn, settings))
    wb('CREDITS.md', credits(images))
    nv = sum(len(e['variants']) for e in E)
    print('entries', len(E), 'variants', nv, 'new materials', len(new), 'images', len(images), 'text', len(TEXT), 'validated by', how,
          'straw_aged', sampled.get('straw_aged'))

def fmt_dims(d, n=3):
    out = []
    for k, v in list(d.items())[:n]:
        s = '%s %s' % (k, v['value'])
        s += ' (assumed)' if v.get('assumed') else (' [%s]' % v['source'] if v.get('source') else '')
        out.append(s)
    more = len(d) - n
    return '; '.join(out) + ('; +%d more in JSON' % more if more > 0 else '')

def esc(s):
    return str(s).replace('|', '/').replace('\n', ' ')

def md(bl, mn, settings):
    L = []
    A = L.append
    n_w1 = sum(1 for e in E if e['wave'] == 1)
    A('# BUILD LIST: outdoor core kit (site objects), v1\n')
    A('**Stage:** S (site objects, `JP\\site\\<group>\\`, `jp_s_*`); built in Phase B3 (wave 1) and with the shrine and temple ladder (wave 2)\n')
    A('**Author and date:** %s, %s\n' % (AUTHOR, DATE))
    A('**Scope:** the %d most-reused outdoor items: OUTDOOR_LIST §5 and the KEEP_OUTDOOR build-first list, with two swaps (see "What changed from the §5 list"). Trees, fences, bridges and setting-specific props are out.\n' % len(E))
    A('**Files:** `build_list.json` (validates against `playbook/templates/build_list_schema.json`; the builders read it), `materials_needed.json` (what jp_common lacks), `refs_index.json` (images k.., text O..), `CREDITS.md` (every download and its licence). Images: `data/research_okit/refs/`. All five files come from `tools/gen_build_list.py`: edit the data there and rerun it.%s\n' % IMG_NOTE)
    A('**Reading the tables:** `[O07]`, `[T54]`, `k06` or `x31` are sources. `(assumed)` means no source gives the value; the reason is in the JSON. **W1** = wave 1 (Phase B3, for the B4 pilot and Phase C wave 1); **W2** = wave 2 (with the shrine and temple ladder).\n')
    A(DECISIONS)
    A(DEAD_WORLD)
    # overview table
    A('\n## The kit at a glance (%d items, %d in wave 1)\n' % (len(E), n_w1))
    A('| # | ID | Item | Level | Wave | Settings (core + flavour, of 19) | Models (variants) | Effort (sessions) |')
    A('|---|---|---|---|---|---|---|---|')
    for i, e in enumerate(E, 1):
        s = e['_settings']
        A('| %d | `%s` | %s | %s | W%d | %d + %d | %d | %.1f |' % (i, e['id'], esc(e['name'].split(':')[0].split(' (')[0]), e['importance'], e['wave'],
          len(s['core']), len(s['flavour']), len(e['variants']), e['effort']))
    A('\n**Totals:** %d items, %d variant models, about %.0f agent sessions for the models (materials extra, see "Order of work").\n' %
      (len(E), sum(len(e['variants']) for e in E), sum(e['effort'] for e in E)))
    A(CHANGES)
    groups = []
    for e in E:
        if e['_group'] not in groups: groups.append(e['_group'])
    n = 0
    for g in groups:
        A('\n## %s\n' % g)
        A('| # | ID | Name | What and where | Level | Tier | Pri | Wave | Period evidence | Key dimensions | Materials (library -> palette) | Variants | Abandoned state | Settings | Placement rule |')
        A('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for e in E:
            if e['_group'] != g: continue
            n += 1
            mats = '<br>'.join('%s: `%s`%s -> %s' % (m['surface'], m['material'], ' **(new)**' if MAT[m['material']]['status'] == 'new' else '', m['palette_id']) for m in e['materials'])
            var = '<br>'.join('`%s` %s' % (v['id'], v['differs_by']) for v in e['variants'])
            tiers = ','.join(str(t) for t in e['tiers']) + ('' if e.get('region', 'all') == 'all' else ' (%s)' % e['region'])
            s = e['_settings']
            st = 'core: %s; flavour: %s' % (', '.join(s['core']) or '-', ', '.join(s['flavour']) or '-')
            A('| %d | `%s` | %s | %s | %s | %s | %s | W%d | %s | %s | %s | %s | %s | %s | %s |' % (n, e['id'], esc(e['name']), esc(e['what']), e['importance'], tiers,
              e['priority'], e['wave'], esc(e['period_evidence']), esc(fmt_dims(e['dimensions'])), esc(mats), esc(var), esc(e['abandoned']), esc(st), esc(e['placement'])))
    A('\n## Notes per entry (only where the table is not enough)\n')
    for e in E:
        bits = []
        if e.get('banned_tells_to_watch'): bits.append('- **Banned tells to watch:** ' + '; '.join(e['banned_tells_to_watch']))
        if e.get('open_questions'): bits.append('- **Open questions:** ' + '; '.join(e['open_questions']))
        if e.get('lod_budget'): bits.append('- **LOD:** ' + e['lod_budget'])
        if bits:
            A('**`%s`**' % e['id']); A('\n'.join(bits)); A('')
    A(WAVE1)
    A(ENGINE)
    A('\n## Materials jp_common lacks (%d new materials, %d texture sets)\n' % (mn['counts']['new_materials'], mn['counts']['texture_sets']))
    A('| Material | Family | Palette ID | Tile (m) | px/m | Finish | _w0 / _w1 / _w2 | Source plan | Wave | Used by |')
    A('|---|---|---|---|---|---|---|---|---|---|')
    for m in mn['materials']:
        A('| `%s` | %s | %s%s | %s | %s | %s | %s / %s / %s | %s | W%d | %d items |' % (m['id'], m['family'], m['palette_id'], ' **(new)**' if m['palette_status'] != 'existing' else '',
          m['tile_size_m'], m['px_per_m'], esc(m['finish']), esc(m['wear']['_w0']), esc(m['wear']['_w1']), esc(m['wear']['_w2']), esc(m['source_plan']), m['needed_in_wave'], len(m['used_by'])))
    A('\n**Reused from jp_common as is (%d):** %s.\n' % (len(mn['reused_from_jp_common']), ', '.join('`%s`' % m['id'] for m in mn['reused_from_jp_common'])))
    A('\n## Requested new palette entries\n')
    A('| Palette ID | sRGB | Method | Why | Sample |')
    A('|---|---|---|---|---|')
    for p in REQ_PAL:
        src = ', '.join('%s box %s (%s) -> %s' % (s['ref'], s['box'], s['select'], s['value']) for s in p.get('samples', [])) or 'none yet (assumed)'
        A('| %s | %s | %s | %s | %s |' % (p['id'], p.get('srgb'), p['method'], esc(p['why']), esc(src)))
    A('\n## Checks the builder must run\n')
    A('- C1, C2, C4, C5, C6 and C8 on every item (PLAYBOOK §12); C9 compare sheets on the stone family (Jizo, stele, lanterns, torii, graves); C7 on stone steps.')
    A('- C6 placement: every item seated 0-2 cm into terrain; wall-backed items (firewood, laundry pole, eave buckets) 5 cm off the wall line.')
    A('- C8 specials: no glass, no metal hoops on ordinary tubs, no bright unfaded cloth or paper in the shipped default, no emissive lanterns, no per-house fire tub.')
    A('- C19 matte: every jp_s_ rvmat uses the matte recipe (PLAYBOOK T12); only iron keeps a fresnel sheen.')
    A(ORDER)
    A(LATER)
    return '\n'.join(L) + '\n'

def credits(images):
    L = ['# Outdoor core kit: credits and licences', '',
         'Written by `research/outdoor_kit/tools/gen_build_list.py` from `data/research_okit/meta.json` (the download log of `tools/fetch_refs.py`).',
         'All images are local research references in `data/research_okit/refs/`, downloaded from Wikimedia Commons as thumbnails of at most 1600 px with a generic User-Agent (`JapanDevResearch/1.0 (DayZ mod research)`). **None is shipped** in any PBO. Only public-domain, CC0 and CC BY files were taken (no share-alike).',
         '', '| Id | Title | Author | Date | Licence | Page |', '|---|---|---|---|---|---|']
    for m in images:
        if m['status'] != 'downloaded': continue
        L.append('| %s | %s | %s | %s | %s | %s |' % (m['id'], esc(m['title'].replace('File:', '')), esc(m['author']), esc(m['date']), m['licence'], m['page_url']))
    linked = [m for m in images if m['status'] != 'downloaded']
    if linked:
        L += ['', '## Picked and licence-checked, not yet downloaded (%d)' % len(linked), '',
              'upload.wikimedia.org answered HTTP 429 to our generic User-Agent after the first files (2026-09-29). These refs are cited by page URL; `python research/outdoor_kit/tools/fetch_refs.py` resumes and downloads them, then rerun `gen_build_list.py`.',
              '', '| Id | Title | Author | Date | Licence | Page |', '|---|---|---|---|---|---|']
        for m in linked:
            L.append('| %s | %s | %s | %s | %s | %s |' % (m['id'], esc(m['title'].replace('File:', '')), esc(m['author']), esc(m['date']), m['licence'], m['page_url']))
    L += ['', 'CC BY images need attribution if they ever appear in anything public (a devlog, a Workshop page): credit the author and licence as above.',
          '', 'Reused without a new download: exterior refs `%s` (credits in `research/exterior/refs_index.json`) and playbook refs (`playbook/refs_index.json`).' % '`, `'.join(EXT_REUSED),
          '', 'Text sources (O01-O27) are cited in `refs_index.json`; nothing was copied from them beyond single numbers.', '']
    return '\n'.join(L)

DECISIONS = '''
## Decisions for Stephen (one line each, with my recommendation)

1. **How long abandoned?** Recommend **about one to two years**: cloth and paper rotted and torn, straw grey and slumped, wood silvered but standing, stone unchanged but mossier, leaf litter everywhere; not ruins.
2. **One build, two lists:** the pulley and lever wells here ARE KEEP_CIVIC civic 6-7, the roofed well (dwelling 28) is the pulley well's `_roofed` variant, and the notice board is KEEP_CIVIC government 6. Recommend **build them once, here, in wave 1**.
3. **Working wells:** recommend **yes**, both wells drink and wash like vanilla wells (the vanilla `Well` script class, one line of script in our PBO); fire tubs and basins stay dry or leaf-filled, not water sources.
4. **Jizo red bibs** (the date is disputed, OUTDOOR_LIST §3.3): recommend a **faded rag bib on about 1 Jizo in 3**, never bright red, the rest bare stone.
5. **Readable text** on signs, lanterns, notice boards and stones, rendered from an **SIL OFL brush font** (free licence, fine for textures): recommend **yes**, with real period wording (Koshin, directions, the 1711 edict lines, era dates).
6. **Add the handcart** (daihachi-guruma, 1,273 counted in Edo in 1703) as the dead world's abandoned-vehicle prop, in place of the festival layer's floats and stages: recommend **yes, wave 1**.
7. **Festival layer:** in a dead autumn world only its leftovers show (tattered banners, fallen lanterns); recommend **nobori + lanterns now**, mikoshi, floats and stages later with the landmarks.
8. **Shop-front dressing** (noren, signs, lanterns, eave buckets) goes on as **proxies in the furnished shop variant p3d** (PLAYBOOK §10.4), not as loose map objects; street objects (tub, bench, gutter, cart) are map objects: recommend **yes**.
9. **Face budget for medium site objects:** PLAYBOOK §12 jumps from small prop (300) to small building (3,000); recommend a new class **"medium site object" <=1,500 / 600 / 200** for wells, torii, carts, stalls and notice boards.
10. **Moss and lichen as alpha decal geometry** (a new material laid on stone tops and north faces) on top of the baked `_w2` wear: recommend **yes**; cheap variety without the unproven second UV set.
11. **Village torii are "standard"**, not "hero" (PLAYBOOK §11 lists torii under both): recommend **standard** for these kit torii, hero only for a later landmark torii.
'''

DEAD_WORLD = '''
## The dead-world rule for every item

Every item ships in its **abandoned** look, because nobody lives here any more (Stephen: "as it was left"). How each
material ages in about one to two years (decision 1):

| Material | Abandoned look | How it is built |
|---|---|---|
| Cloth (noren, banners, laundry, bibs) | Faded, torn, partly fallen | The default mesh is torn (alpha holes) on `_w2` cloth; a `_ab_fallen` variant lies on the ground |
| Paper (lanterns, shide, andon) | Split and holed, ribs showing; no light anywhere | `_ab_torn` is the default; never emissive |
| Straw (stacks, ropes, bundles) | Grey on top, slumped, caps blown off | `_w1`/`_w2` straw + a slumped variant |
| Wood (tubs, benches, carts, torii) | Silvered, split; a minority tipped, broken or leaning | `_w1`/`_w2` wood + 1-2 pose variants per item |
| Stone (figures, steles, lanterns, graves) | Unchanged, but mossier, leaning or sunk; quake-toppled tops | `_w1`/`_w2` stone + moss decals + a rare toppled variant |
| Water (wells, tubs, basins) | Wells still hold water; tubs and basins hold leaves and silt | Leaf-litter material in every open vessel |

**Placement ratio (a starting point for the map agent):** about 60 % of placements use the standing variant with heavy
wear, 30 % the mild abandoned pose (tipped, fallen, leaning), 10 % the broken pose. No setting shows a fresh, tidy
object. The autumn leaf-litter material ties every item to the season.
'''

CHANGES = '''
### What changed from the §5 list
- **In:** the handcart (§5 #52; decision 6) and the straw rope (shimenawa: §5 #21 "sacred tree with shimenawa" and
  #23 "seasonal door dressing" are both a rope, and wells, torii and boundaries use it too).
- **Merged into one family each:** Kōshin stone + dōsojin + batō Kannon + direction, boundary, nenbutsu and god
  stones = `jp_s_stele` (OUTDOOR_LIST §7.7); gorintō / hōkyōin-tō sit inside the graveyard stones; the six-Jizō row is
  six placements of `jp_s_stone_jizo`; the rain barrel is a variant of the fire tub; night-soil buckets are a
  tenbin load.
- **Out (built elsewhere):** plank bridge (KEEP_CIVIC bridges), sacred tree itself (flora), seasonal door dressing
  beyond the rope (festival stretch), palanquin (with the landmark procession sets), mikoshi, floats and stages
  (decision 7).
- **Setting counts** in the tables are computed from OUTDOOR_LIST §4 by the generator: an item counts in a setting if
  any kit family it covers is core (or else flavour) there.
'''

WAVE1 = '''
## Wave 1: what Phase B3 builds first (20 items)

For the **B4 pilot** (dressing the yard and street round `buildings/machiya_t3_01`, the Kamigata shop:general at
(1024, 1045), front south) and **Phase C wave 1** (farmhouses, poor huts, townhouse units, post-town house, inn, kura,
shed, toilet, roofed well):

| Wave-1 item | B4 pilot (machiya t3, street + yard) | Phase C wave 1 |
|---|---|---|
| `jp_s_gutter` | stone gutter along the front, slab at the door | townhouse units, post-town house, inn |
| `jp_s_shopfront` | long noren on the entrance, mizuhiki, hanging sign, sudare upstairs | townhouse units, inn |
| `jp_s_lantern_sign` | kake-andon at the door (torn) | inn (chochin), post-town house |
| `jp_s_bench` | one endai under the pent, tipped | inn, post-town house, farmhouses |
| `jp_s_fire_tub` | a corner tub with a fallen pyramid at the street corner; eave bucket | townhouse units |
| `jp_s_oke` | wash tub and buckets by the back door | every dwelling, toilet, well |
| `jp_s_well_tsurube` | pulley well in the back yard (`_roofed` = dwelling 28) | roofed well, back-alley court |
| `jp_s_firewood_stack` | stack against the kitchen wall | every dwelling, shed |
| `jp_s_laundry_pole` | back yard, fallen cloth | every dwelling |
| `jp_s_tenbin` | leaning by the shop door | farmhouses, poor huts |
| `jp_s_handcart` | half-loaded cart in the street | kura, post-town house |
| `jp_s_nobori` | one tattered shop banner | inn |
| `jp_s_stall` | (not at the pilot) | post-town edge, inn surroundings |
| `jp_s_kosatsu` | (not at the pilot) | post-town centre |
| `jp_s_well_hanetsurube` | (not at the pilot) | farmhouses, poor huts |
| `jp_s_straw_stack` | (not at the pilot) | farmhouses, shed, poor huts |
| `jp_s_stone_jizo` | one small Jizo at the street corner | village entrances round the farmhouses |
| `jp_s_jizo_hut` | Kyoto-style corner box for that Jizo | village entrances |
| `jp_s_stele` | (not at the pilot) | village roads, post-town ends |
| `jp_s_shimenawa` | rope over the well | farmhouse wells and yard shrines |

**Wave 2 (7 items), with the Phase C wave-2 shrine and temple ladder:** stone lantern, chozubachi, wooden torii, stone
torii, stone steps, graveyard stones, graveyard wood set. They are "build with the shell that needs them" items
(PRODUCTION_PLAN) and share the carved-stone material wave 1 already makes.
'''

ENGINE = '''
## Engine and gameplay notes (all items)

- **Class and placement:** every item gets a static config class `Land_JP_S_<Name>_<Variant>` (HouseNoDestruct, scope
  1, like vanilla map objects) so it can be baked into the .wrp through `test/placements/` or spawned through the
  object spawner. Proxied shop dressing (decision 8) needs no class.
- **LODs:** Resolution 1-3, Geometry (closed convex components; thin cloth and rope get none), View Geometry
  (so bullets and sight stop at stone, tubs and carts, not at noren or reed screens), Fire Geometry (vanilla
  penetration rvmats: stone `granite`, wood `wood`, straw `hay`, cloth and paper `fabric_thin`), Memory. Roadway only
  where players stand: bench tops, stall counters, notice-board base, steps, gutter slabs and boards.
- **Soft cover:** noren, reed screens, sudare and straw stacks block sight but not bullets (View Geometry only on
  straw stacks, none on cloth): the "hide inside the straw stack" hook from OUTDOOR_LIST.
- **Wells:** a 4_World class `class Land_JP_S_Well_Tsurube extends Well {}` (and the lever well) inherits the vanilla
  drink and wash-hands actions (`4_world/entities/building/well.c`); it lives in our asset PBO (allowed: actions on
  our own objects). The action target needs a memory point near the curb top; confirm in the first in-game check.
- **Loot:** props are dressing (PRODUCTION_PLAN). Bench tops, stall counters and cart beds are natural loot surfaces
  if Stephen later wants outdoor loot points; that needs a mapgroupproto group per class, not a container.
- **No light:** no lantern is emissive; the dead world is dark at night.
- **Grid:** every module that meets a building (gutter pieces, firewood stacks, stall panels, torii spans, steps)
  snaps to the half-ken grid (PLAYBOOK rule 9), so the placement agent can lay them along any house front.
'''

ORDER = '''
## Order of work after G1 (rough effort in agent sessions)

| Step | What | Items | Effort |
|---|---|---|---|
| 0 | **Materials (with B1):** the 11 wave-1 materials + `straw_aged` / `leaf_litter_autumn` palette entries; the OFL font decal atlases | materials_needed.json | 1.5 |
| 1 | **Round wood and poles:** cooperage family, fire tub, firewood, bench, laundry pole, tenbin, handcart | 7 | 2.8 |
| 2 | **Wells:** pulley (+ roofed = dwelling 28) and lever; the Well script class; C9 sheet | 2 | 1.4 |
| 3 | **Stone, wave 1:** Jizo, stele family, Jizo hut; compare sheets against the dated Koshin and Jizo sizes | 3 | 2.1 |
| 4 | **Street:** gutter kit, shop-front kit, lanterns and sign lamps, nobori, stall family, notice board | 6 | 3.8 |
| 5 | **Straw:** stacks and bales, shimenawa | 2 | 0.8 |
| 6 | **B4 pilot:** dress the machiya yard and street (and the proxies on a shop variant); one contact sheet; Stephen's G4 walk | - | 1.0 |
| 7 | **Wave 2 (with the shrine and temple ladder):** stone lanterns, chozubachi, both torii, stone steps, graveyard stones and wood set | 7 | 4.3 |

**Total: about 18 sessions** (13.4 up to the G4 pilot walk, 4.3 for wave 2). Steps 1, 3 and 5 can run in parallel with step 2 once
step 0 has made the straw, stone and textile materials.
'''

LATER = '''
## Later (out of this list)

- **Next outdoor groups** (their own build lists): fences, hedges and garden walls (14), farmyard and harvest beyond
  straw (hasa racks, scarecrows, boar fences), shore and salt kits, garden stones and garden lanterns, canal edge,
  wild work sites.
- **Seasonal extras:** kadomatsu and Bon dressing, the festival floats and stages (decision 7).
- **Verify before a hero build:** most O-sources were read through a search summary; the Kasuga proportion (O10) and
  the gutter widths (O24) deserve a primary check; the board-shaped gravestone sizes are assumed.
- **Period traps enforced here:** no per-house fire tub, no hand pump, no glass, no carp streamers, no stone Inari
  foxes, no family-name graves, no Fuji-ko or Ontake-ko stones, no tall 19th-c. lantern towers, no giant red gate
  lantern, no wheelbarrow, no washboard.
'''

if __name__ == '__main__':
    main()
