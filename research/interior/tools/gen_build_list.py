"""Generates the INTERIOR build list (gate G1) from ONE data source, so the markdown and the JSON always say the same
thing (BUILD_LIST_TEMPLATE rule):

  research/interior/build_list.json       (validated here against playbook/templates/build_list_schema.json)
  research/interior/materials_needed.json (the materials agent's task list)
  research/interior/refs_index.json       (new sources i01-i51 and N01-N20)
  research/interior/q5_evidence.json      (Q5: the vanilla proxy-LOD and loot-point probes, summarised)
  research/interior/CREDITS.md            (every downloaded image with its source and licence)
  research/interior/BUILD_LIST.md

Run:  python research/interior/tools/gen_build_list.py
Reads: data/research_int/meta.json (download log from fetch_int_refs.py), data/research_int/q5_lods.json and
q5_loot.json (from q5_lods.py / q5_loot.py), playbook/refs_index.json, research/exterior/refs_index.json,
playbook/palette.json, playbook/templates/build_list_schema.json, sample_int.py (palette samples).
Writes binary, LF. Research agent PA2, 2026-09-29.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sample_int  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'interior')
DATE = '2026-09-29'
AUTHOR = 'research agent PA2'


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


# ================================================================================================ the kept shells
# Which room tags each KEEP shell has, and its tiers. My reading of KEEP_DWELLINGS / KEEP_TRADES / KEEP_CIVIC plus the
# room lists in BUILDING_LIST §3. Stretch (☆) shells are left out. Used only to COUNT how many shells / rooms a prop
# or fitting reaches, so the numbers are "about", not exact.
SHELLS = [
    # id, name, tiers, room tags
    ('D1', 'Rural hut, east', [1], ['doma', 'daidokoro', 'sleeping']),
    ('D30', 'Rural hut, west/mountain', [1], ['doma', 'daidokoro', 'sleeping']),
    ('D2', 'Field hut + lean-to', [1], ['doma', 'daidokoro']),
    ('D3', 'Back-alley tenement (ura-nagaya)', [1, 2], ['doma', 'living']),
    ('D4', 'Bunk hall', [1], ['doma', 'daidokoro', 'sleeping']),
    ('D5', 'Hermit hut', [1], ['daidokoro', 'living']),
    ('D6', 'Kanto farmhouse, 3-room', [1, 2], ['doma', 'daidokoro', 'living', 'sleeping', 'stable']),
    ('D7', 'Kinai farmhouse, 4-room', [2], ['doma', 'daidokoro', 'zashiki', 'living', 'sleeping', 'stable']),
    ('D8', 'Mountain board-roof house', [1, 2], ['doma', 'daidokoro', 'living', 'sleeping']),
    ('D9', 'Coastal house', [1, 2], ['doma', 'daidokoro', 'sleeping', 'storage']),
    ('D10', 'Tokaido post-town house', [2], ['doma', 'daidokoro', 'shop', 'living', 'sleeping', 'stable']),
    ('D11', 'Kamigata townhouse units', [2, 3], ['doma', 'shop', 'living', 'zashiki', 'storage', 'loft']),
    ('D12', 'Edo townhouse units', [2, 3], ['doma', 'shop', 'living', 'zashiki', 'storage', 'loft']),
    ('D13', 'Street-front row (omote-nagaya)', [2], ['doma', 'shop', 'living']),
    ('D14', 'Foot-soldier row', [2], ['doma', 'living', 'sleeping']),
    ('D15', 'Small samurai house', [2, 3], ['doma', 'daidokoro', 'zashiki', 'living', 'sleeping', 'engawa']),
    ('D16', 'East headman house', [2, 3], ['doma', 'daidokoro', 'zashiki', 'living', 'sleeping', 'office', 'storage', 'engawa']),
    ('D17', 'Kinai headman house', [2, 3], ['doma', 'daidokoro', 'zashiki', 'living', 'sleeping', 'office', 'storage', 'engawa']),
    ('D18', 'Great merchant residence', [3], ['doma', 'shop', 'office', 'zashiki', 'living', 'sleeping', 'storage', 'engawa', 'corridor', 'bath']),
    ('D19', 'Samurai mansion', [3], ['doma', 'daidokoro', 'zashiki', 'living', 'sleeping', 'office', 'engawa', 'corridor', 'guard', 'bath']),
    ('D20', 'Daimyo mansion', [3], ['daidokoro', 'zashiki', 'living', 'office', 'corridor', 'engawa', 'guard']),
    ('D21', 'Tea hut', [3], ['zashiki', 'doma']),
    ('D22', 'Plastered kura', [2, 3], ['storage', 'loft']),
    ('D23', 'Board storehouse', [1, 2], ['storage']),
    ('D24', 'Shed / barn', [1, 2], ['workshop', 'storage']),
    ('D25', 'Stable', [1, 2], ['stable']),
    ('D26', 'Toilet (setchin)', [1, 2, 3], ['toilet']),
    ('D27', 'Bath hut', [2, 3], ['bath']),
    ('D29', 'Gatehouse with rooms', [2, 3], ['guard', 'living', 'storage']),
    ('T1', 'Roadside tea house', [1, 2], ['doma', 'shop', 'daidokoro', 'zashiki']),
    ('T5', 'Inn (hatago)', [2, 3], ['doma', 'office', 'daidokoro', 'zashiki', 'sleeping', 'corridor', 'bath', 'toilet']),
    ('T6', 'Honjin', [3], ['doma', 'daidokoro', 'zashiki', 'office', 'corridor', 'engawa', 'bath']),
    ('T7', 'Hot-spring inn + bath house', [2, 3], ['doma', 'daidokoro', 'zashiki', 'sleeping', 'bath']),
    ('T8', 'Public bathhouse', [2, 3], ['doma', 'bath', 'office']),
    ('T9', 'Stable yard', [2], ['stable', 'office']),
    ('T11', 'Smithy', [1, 2, 3], ['workshop', 'doma', 'living']),
    ('T12', 'Foundry', [2], ['workshop', 'storage']),
    ('T13', 'Earth-floor workshop', [1, 2], ['workshop', 'doma', 'living']),
    ('T14', 'Raised-floor bench workshop', [2, 3], ['workshop', 'shop', 'living']),
    ('T3', 'Brewery complex', [3], ['workshop', 'storage', 'doma', 'office']),
    ('T4', 'Water mill', [1, 2], ['workshop', 'storage']),
    ('T23', 'Charcoal kiln hut / field camps', [1], ['doma', 'daidokoro']),
    ('C1', 'Guard hut', [2, 3], ['guard']),
    ('C2', 'Official compound', [3], ['guard', 'office', 'zashiki', 'doma', 'daidokoro', 'storage']),
    ('C3', 'Open-front office (toiya-ba)', [2], ['office', 'doma']),
    ('C4', 'Priests\' quarters (kuri)', [2, 3], ['doma', 'daidokoro', 'zashiki', 'sleeping', 'storage']),
]
SHOP_SETS = 22   # KEEP_TRADES section A: dressing sets on shells D11/D12/D13 (+3 stretch)
PILOT = {'toriniwa': 'doma', 'mise': 'shop', 'zashiki': 'zashiki', 'kitchen': 'doma', 'storage': 'storage'}


def reach(tags, tiers):
    shells = [s for s in SHELLS if set(s[3]) & set(tags) and set(s[2]) & set(tiers)]
    rooms = sum(len(set(s[3]) & set(tags)) for s in shells)
    return len(shells), rooms, [s[0] for s in shells]


# ================================================================================================ entries
E = []
STD_CHECKS = ['C1', 'C2', 'C4', 'C5', 'C6', 'C8', 'C9']


def add(family, **k):
    k['_family'] = family
    k.setdefault('checks', STD_CHECKS)
    k.setdefault('region', 'all')
    k.setdefault('status_overlay', 'commoner')
    E.append(k)


# ------------------------------------------------------------------------------------------------ BUILT-IN FITTINGS
FIT = 'Built-in fittings (parts of the shell, merged like any kit part)'
add(FIT, id='jp_p_fit_floor', name='Room floor recipes: tatami room, board floor, bamboo-slat floor, doma (promoted from the machiya build)',
    what='The floor of every room by its tag and tier: tatami (T2 best room, T3 living rooms), boards (daidokoro, storage, T1 living), split bamboo (poorest huts), earth doma. The machiya code already has tatami_room / board_floor / doma_floor; they move into the kit and get the real materials.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro', 'living', 'zashiki', 'sleeping', 'shop', 'office', 'workshop', 'storage', 'stable', 'engawa', 'corridor', 'guard', 'toilet'],
    period_evidence='Tatami reach townspeople by the end of the 17th c. [T01], widespread among commoners mid-Edo, rural later [N01]; no tatami in T1 [T58, PLAYBOOK §2.1]; tataki doma general in the Edo period [N16]; surviving floors [i01, i03, i24]',
    refs=[R('c21_tatami', 'tatami facing weave and heri edge'), R('i03_tenmyo_irori', 'board room beside a tatami room (farmhouse)', True), R('i01_kasuya_irori', 'dark polished board floor', True),
          R('i06_tsunashima_doma', 'earth doma (colour sample)', True), R('i02_kasuya_kamado', 'earth doma, sunlit (colour sample)', True)],
    dimensions={
        'tatami_m': D('fills the room between post faces: about 1.78 x 0.87 on the 1.82 grid (Inakama); 0.055 thick; heri 0.03', 'PLAYBOOK §3-4 [T01, N01]; machiya build'),
        'layout': D('shugi (no four corners meet); half mat in the centre of 4.5-mat rooms', 'PLAYBOOK §3 (convention)'),
        'boards_m': D('0.20-0.30 wide, 0.03 thick top boards on a 0.15 base', 'machiya build'),
        'levels_m': D('doma = grade + 0.05; raised floors +0.45 over the doma; storage boards +0.03', 'PLAYBOOK §4; machiya build'),
    },
    materials=[M('tatami facing', 'jp_m_floor_tatami', 'tatami_aged'), M('heri', 'jp_m_floor_tatami_heri', 'tatami_heri'), M('boards', 'jp_m_floor_boards_int', 'timber_interior'),
               M('rough boards (T1, stable, shed)', 'jp_m_floor_boards_rough', 'timber_interior'), M('bamboo slats (T1)', 'jp_m_floor_takeyuka', 'bamboo_weathered'),
               M('doma T1 / farm', 'jp_m_ground_doma_earth', 'doma_earth'), M('doma T2-3 (tataki)', 'jp_m_ground_doma_tataki', 'doma_earth'),
               M('under-floor', 'jp_m_wood_sooted', 'timber_sooted')],
    connectors=['floor: one recipe per room rect from rooms.json (tag, floor, level)', 'roadway: textile_carpet_int (tatami), wood_planks_int (boards), dirt_int (doma) (PLAYBOOK §9)'],
    variants=[V('_tatami', 'tatami room (shugi solver)', 2), V('_boards', 'board floor'), V('_rough', 'rough adzed boards', 1), V('_takeyuka', 'bamboo slats under mats', 1),
              V('_doma', 'earth / tataki'), V('_tatami_lifted', 'one or two mats lifted or missing, base boards showing (abandoned; a 0.055 step)', 3)],
    structural='NONE (recipes over the room rect); the machiya needs a rebuild to swap its stand-in materials',
    loot_surface='the floor itself: lootFloor points on the Roadway minus prop footprints + 0.4 m',
    abandoned_state='_w2 mats in one room in three, dust lanes, a lifted mat; doma with leaf litter at the doors',
    deviations=['D10: tatami are a floor mesh with a mat layout, loot on the floor'], lod_budget='part of the building budget (machiya: mats modelled per mat in LOD0, one slab in LOD2-3)')

add(FIT, id='jp_p_fit_irori', name='Sunken hearth (irori) with frame (robuchi), ash bed and hook beam',
    what='The square hearth cut into the board floor of the daidokoro / hiroma: wooden frame, ash bed, and a beam or hook point overhead for the jizai-kagi.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['daidokoro', 'living', 'guard'],
    period_evidence='Kitamura house 1687 hiroma with irori [BL §3, E01]; irori with jizai-kagi and fish-shaped yokogi, hidana rack [N12]; surviving farmhouse hearths [i01, i03, i04, i10]',
    refs=[R('i03_tenmyo_irori', 'irori in a board room, jizai-kagi from the beam, tatami room behind (Edo-Tokyo museum farmhouse)', True),
          R('i04_tsunashima_irori', 'ash bed, wood frame, kettle on the hook, firewood (Tsunashima farmhouse)', True),
          R('i01_kasuya_irori', 'irori flush in a dark polished board floor, kettle on a hook (Kasuya house, Itabashi)', True),
          R('i10_hearth_boards', 'frame and ash bed in a board floor'), R('i33_morse_jizai', 'Morse 1885: simple peasant ji-zai')],
    dimensions={
        'pit_m': D('0.91 x 0.91 (half-ken square, small houses) or 0.91 x 1.365 / 1.82 (farmhouses, headman)', None, 'common museum sizes; snaps to the half-ken grid (rule 9); no period source read'),
        'frame_m': D('robuchi 0.09 wide x 0.09 deep, top flush with the floor', None, 'typical; hardwood'),
        'ash_bed_m': D('0.12 below the floor (walkable step, Roadway on the ash)', None, 'reason: a player who steps in must not fall or stick'),
        'hook_point_m': D('beam or hook batten 2.30-2.60 above the floor, over the pit centre', None, 'reason: carries jp_f_jizai_kagi; clears D2 head room at the pit edge'),
    },
    materials=[M('frame', 'jp_m_wood_interior', 'timber_interior'), M('ash bed', 'jp_m_ground_ash', 'ash_grey'), M('hook beam, soot above', 'jp_m_wood_sooted', 'timber_sooted')],
    connectors=['floor: cut into a raised board floor (not tatami); the floor recipe leaves the opening and a Roadway at -0.12', 'post: centred between grid lines; the hook beam spans post to post'],
    variants=[V('_s', '0.91 square (huts, tenement-size rooms, guard huts)', 1), V('_l', '0.91 x 1.365 (farmhouse hiroma)', 2), V('_hidana', 'adds a slatted smoke/drying rack (hidana) hung above, sooted', 1)],
    structural='FLOOR OPENING in the raised board floor + a hook beam overhead (and a smoke outlet in the roof: exterior jp_p_roof_kemuridashi)',
    loot_surface='none on the frame; the ash bed is a floor point (range <=0.3)',
    abandoned_state='cold grey ash, a few charred sticks, the pot hook empty or with a rusted pot; soot on everything above',
    deviations=['Ash bed walkable at -0.12 (reason)'], lod_budget='part of the building budget: <=200 faces',
    banned_tells_to_watch=['brick or cut-stone hearth (modern)', 'a chimney'])

add(FIT, id='jp_p_fit_kamado', name='Clay cooking stove (kamado / kudo / hettsui), promoted from the machiya build',
    what='The built-in clay stove on the doma: one mouth in tenements, two or three in farmhouses and townhouses, a long plastered row in inns and headman kitchens.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['doma'],
    period_evidence='Kamado built by plasterers; Edo stoves face the room with their back to the outer wall; tenements use a two-mouth stove [N11]; nagaya kitchen reconstruction [N10, i08]; farmhouse stoves [i02, i05, i20]; the machiya already has one [machiya_t3_01 REPORT §2]',
    refs=[R('i05_tsunashima_kamado', 'two rough clay kamado on stones in a farmhouse doma', True), R('i02_kasuya_kamado', 'large round clay kamado with an iron rim on the doma (Kasuya house)', True),
          R('i20_hachioji_kamado', 'two-mouth kamado with iron pot and wooden lid (samurai guard leader house)', True), R('i11_kamado_plastered', 'white plastered kamado by the raised floor'),
          R('i08_edo_nagaya_kitchen', 'tenement kitchen: stove, sink, water jar (c.1840 reconstruction)'), R('i31_morse_kitchen_range', 'Morse 1885: the usual kitchen range')],
    dimensions={
        'height_m': D('0.60-0.75 top (machiya build: 0.72)', 'machiya_t3_01 build; i05, i20'),
        'mouth_m': D('pot rim d 0.30-0.45 per mouth; fire mouth 0.30 x 0.26', 'machiya_t3_01 build (0.44 rims)'),
        'footprint_m': D('1 mouth 0.60 x 0.60; 2 mouths 0.70 x 1.30; row of 3-5 at 0.75 per mouth', None, 'from the photos; snapped to 0.05'),
        'clearance_m': D('>=1.00 walkable doma beside it (tori-niwa rule)', 'PLAYBOOK §4'),
    },
    materials=[M('clay body (T1-2)', 'jp_m_wall_nakanuri_int', 'earth_wall_aged'), M('plastered body (T3, Kamigata okudo)', 'jp_m_wall_shikkui_int', 'shikkui_white'),
               M('base course', 'jp_m_stone_cut', 'stone_granite'), M('rims', 'jp_m_metal_iron', 'iron_black'), M('soot boards behind', 'jp_m_wood_sooted', 'timber_sooted')],
    connectors=['floor: stands on the doma at doma level', 'wall: back against an outer wall or the lean-to wall; soot boards and smoke vent above'],
    variants=[V('_1', 'one mouth (tenement, hut)', 1), V('_2', 'two mouths (townhouse, farmhouse; the machiya one)', 2), V('_row', 'plastered row of 3-5 mouths (inn, headman, kuri)', 3)],
    structural='NONE in the walls; needs the smoke outlet in the roof and sooted material above (already done on the machiya)',
    loot_surface='top between the rims (0.72): 1 small point (range 0.15) per 2 mouths',
    abandoned_state='cold; one wooden lid fallen, ash spill at the fire mouth, cracked clay face, soot',
    deviations=[], lod_budget='part of the building budget: <=400 faces (machiya: already inside its 12k)')

add(FIT, id='jp_p_fit_agarikamachi', name='Raised-floor edge beam (agari-kamachi) and under-floor boards (yukashita)',
    what='The polished beam that finishes the raised floor where it meets the doma, with the boards closing the void underneath: the step you sit on to take off your sandals.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'shop', 'daidokoro', 'living'],
    period_evidence='Raised living floor ~0.45-0.5 m above the doma [T17]; step (agari-kamachi) at every inn and house entrance [BL §3 hatago]; machiya build [machiya_t3_01: kamachi_lip + yukashita_boards]',
    refs=[R('i24_hida_farmhouse', 'raised board floor edge over an earth doma (Hida farmhouse)', True), R('i03_tenmyo_irori', 'board floor edge'), R('i42_morse_guestroom_hachiishi', 'Morse 1885: inn room edges')],
    dimensions={'beam_m': D('0.12 wide x 0.15 deep, top = finished floor (+0.45 over the doma)', None, 'section like a sill (dodai 0.12); PLAYBOOK §4 floor'),
                'rise_m': D('0.45 (with the hidden ramp under the kutsunugi stone)', 'PLAYBOOK §4')},
    materials=[M('beam (polished)', 'jp_m_wood_interior', 'timber_interior'), M('under-floor boards', 'jp_m_wood_sooted', 'timber_sooted')],
    connectors=['floor: the raised floor recipe emits it on every edge that faces a doma', 'post: runs post to post'],
    variants=[V('_std', 'plain beam'), V('_shikidai', 'wide board step (shikidai) in front: honjin and samurai only (PLAYBOOK §2.2)', 3)],
    structural='NONE: part of the raised-floor recipe (promote the machiya kamachi_lip + yukashita_boards into the kit)',
    loot_surface='the beam top is a sit-edge: 1 small point per 1.8 m (range 0.15) on shop and inn entrances',
    abandoned_state='dust band on the beam, scuffed centre, a sandal or two left on the doma below', deviations=['D-none'], lod_budget='part of the floor recipe')

add(FIT, id='jp_p_fit_kutsunugi', name='Shoe-removal stone (kutsunugi-ishi) with the hidden ramp',
    what='The flat stepping stone in front of every raised floor edge; in our kit it hides the 0.45 walk ramp. Already built as jp_p_found_step_natural.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'engawa'],
    period_evidence='Standard at raised-floor entrances [T17]; built and walked in game [machiya_t3_01 REPORT_FIX2, G3 passed]',
    refs=[R('i24_hida_farmhouse', 'stone at the raised floor edge'), R('c15_farmhouse_interior', 'farmhouse interior, board floor over earth')],
    dimensions={'stone_m': D('0.9-1.0 x 0.45-0.55, top 0.15-0.20 above the doma', 'machiya build (width 1.04)'), 'ramp_deg': D('<=34 under the stone', 'machiya build')},
    materials=[M('stone', 'jp_m_stone_field', 'stone_granite')],
    connectors=['floor: in front of each door or open edge between a doma and a raised floor'],
    variants=[V('_natural', 'field stone (exists)'), V('_cut', 'dressed stone (T3, samurai)', 3)],
    structural='NONE (exists: reuse)', loot_surface='none (keep it clear: it is the walking path)',
    abandoned_state='a pair of worn straw sandals left on it, dust', deviations=[], lod_budget='exists')

add(FIT, id='jp_p_fit_nagashi', name='Kitchen sink (nagashi / hashiri): wooden trough, stone in T3',
    what='A shallow sink on the doma beside the water jar: a wooden trough on legs in town houses, a low sink at the floor edge in farmhouses, a cut stone sink in rich houses; drains through the wall.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['doma'],
    period_evidence='Nagaya kitchen: shallow sink, water drawn by ladle from the water jar [N10, i08]; sink board in every home kitchen [BL §5.1]; city kitchen with sink and shelves [i32]',
    refs=[R('i08_edo_nagaya_kitchen', 'sink, water jar and stove in a tenement kitchen (c.1840 reconstruction)'), R('i32_morse_city_kitchen', 'Morse 1885: city kitchen with sink and racks'),
          R('i30_morse_kitchen_farmhouse', 'Morse 1885: old farmhouse kitchen, Kabutoyama')],
    dimensions={'trough_m': D('0.90-1.20 x 0.45, 0.08 deep', None, 'from the reconstruction photo; N10 says shallow'),
                'top_m': D('standing type 0.75 above the doma; floor type = the raised floor edge', None, 'reason: standing height for the doma kitchens we build'),
                'drain_m': D('bamboo or wooden spout 0.05 through the wall at sill level', None, 'form only')},
    materials=[M('trough, legs', 'jp_m_wood_interior', 'timber_interior'), M('stone sink (T3)', 'jp_m_stone_cut', 'stone_granite'), M('spout', 'jp_m_bamboo_weathered', 'bamboo_weathered')],
    connectors=['wall: against an outer wall of the doma, beside the kamado or water jar', 'floor: doma level'],
    variants=[V('_wood', 'wooden trough on legs (T1-2)', 1), V('_floor', 'low sink at the raised-floor edge (farmhouse)', 1), V('_stone', 'cut stone sink (T3)', 3)],
    structural='a small DRAIN HOLE through the wall at the sill (optional; visual only)',
    loot_surface='trough bottom: 1 small point (range 0.2)', abandoned_state='dry, a cracked bowl and a ladle left in it, leaf litter blown in',
    deviations=[], lod_budget='<=250 faces (merged into the building)')

add(FIT, id='jp_p_fit_kamidana', name='God shelf (kamidana) with a small shrine box (miya)',
    what='A plain board shelf high on the wall of the shop, kitchen or living room, holding a small shrine box, a sakaki pot and paper charms.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['shop', 'daidokoro', 'living', 'workshop', 'doma'],
    period_evidence='The Ise oshi devised and spread the daijingu shelf; by mid-Edo most households kept one [N14]; "almost every workshop and shop" [BL §5.5]',
    refs=[R('i09_edo_nagaya_hibachi', 'tenement room with a god shelf high on the wall (c.1840 reconstruction)'), R('i07_edo_nagaya_room', 'tenement room dressing')],
    dimensions={'shelf_m': D('0.90 x 0.30, underside 1.95-2.05', None, 'reason: sits on the 2.00 head rail (D2) so nobody walks into it'), 'miya_m': D('0.45 x 0.25 x 0.40 high', None, 'small single-door shrine box; typical')},
    materials=[M('shelf, brackets', 'jp_m_wood_interior', 'timber_interior'), M('shrine box (plain wood)', 'jp_m_wood_interior', 'timber_interior'), M('charms', 'jp_m_paper_shoji', 'washi_shoji')],
    connectors=['head: on the 2.00 head rail or a beam, in a room corner'],
    variants=[V('_plain', 'shelf + miya'), V('_ebisu', 'shop version with an Ebisu/Daikoku pair (shop sets)', 2)],
    structural='NONE (hangs on the head rail)', loot_surface='none (too high to reach; keep it dressing)',
    abandoned_state='left undisturbed: dusty, the sakaki dead and brown, charms yellowed (respectful: never smashed)',
    deviations=[], lod_budget='<=300 faces')

add(FIT, id='jp_p_fit_mise_floor', name='Shop front floor: board display strip (mise-ita) along the street edge of the shop room',
    what='The shop room is the raised floor; its street edge is a 0.45-0.91 m board strip where goods are laid out and customers sit on the edge; the rest is tatami (T3) or boards (T2).',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['shop'],
    period_evidence='Bookseller of 1690: goods laid out on the raised floor at the open front [x33]; Mitsui Echigoya interior (1768, just past the window): clerks on the raised tatami floor, goods on shelves behind [i13]; shop = doma + choba [N18]; the standard shop kit in ~61 entries [BL §5]',
    refs=[R('x33_jinrin_bookseller_1690', 'Jinrin kinmo zui 1690: bookseller, goods on the raised floor at the shop front', True),
          R('i13_echigoya_1768', 'Utagawa Toyoharu 1768: Echigoya dry-goods shop, raised floor, clerks, shelves (18 years past the window)', True),
          R('i15_moronobu_1685_p5', 'Moronobu 1685: lattice shop front and a board bench outside', True)],
    dimensions={'strip_m': D('0.455 (quarter ken) or 0.91 deep x the room width, top = the room floor (+0.45)', None, 'reason: snaps to the grid; replaces one tatami row'),
                'edge_m': D('front edge = agari-kamachi beam', 'jp_p_fit_agarikamachi')},
    materials=[M('boards', 'jp_m_floor_boards_int', 'timber_interior')],
    connectors=['floor: part of the shop floor recipe (floor=tatami|boards, strip=0.455|0.91 along the street wall)'],
    variants=[V('_455', 'narrow strip behind a lattice front (the pilot: degoshi)'), V('_910', 'wide strip behind an open suriage-do front', 2)],
    structural='FLOOR RECIPE change only (a board strip instead of the front tatami row); the machiya pilot needs its mise floor regenerated',
    loot_surface='the strip is a floor loot zone (range 0.3-0.5) and the display stands on it carry shelf points',
    abandoned_state='goods knocked over along the strip, empty stands, a torn noren fallen inside, dust',
    deviations=[], lod_budget='part of the floor recipe')

add(FIT, id='jp_p_fit_tokonoma', name='Picture alcove (tokonoma) with alcove post (toko-bashira) and raised base (toko-gamachi)',
    what='The recess in the best room for a scroll and a vase. In 1730 commoners were forbidden it; headmen (to receive officials), samurai, honjin and a few great merchants had it.',
    importance='standard', tiers=[2, 3], priority='P2', room_tags=['zashiki'], status_overlay='samurai',
    period_evidence='Commoners forbidden tokonoma in the Edo period; spreads in sitting rooms from the mid-18th c.; installed by upper farmers and townsmen, general only after Meiji; about 1 ken wide, ~3 shaku deep [N04]; built in headman houses to receive lords and intendants [N05]',
    refs=[R('i23_kendan_tokonoma', 'alcove with a toko-bashira and hanging scroll (Kendan yashiki)', True), R('i43_morse_guestroom', 'Morse 1885: guest room, tokonoma beside the shelves'),
          R('i44_morse_country_guestroom', 'Morse 1885: guest room of a country house'), R('i12_tsubaki_honjin', 'Tsubaki honjin (Koriyama-juku, 1718 rebuild): formal tatami rooms', True)],
    dimensions={'width_m': D('1.82 (1 ken); 0.91 in small rooms', 'N04'), 'depth_m': D('0.91 (3 shaku) or 0.455', 'N04'),
                'base_m': D('toko-gamachi top +0.10-0.15 over the tatami', None, 'typical'), 'post_m': D('toko-bashira 0.12 square or a round log', 'PLAYBOOK §4 post')},
    materials=[M('toko-bashira, gamachi', 'jp_m_wood_interior', 'timber_interior'), M('floor board (toko-ita) or tatami', 'jp_m_floor_boards_int', 'timber_interior'), M('back wall', 'jp_m_wall_nakanuri_int', 'earth_wall_aged')],
    connectors=['post: the recess adds one bay 0.91 deep beyond the room wall line (or takes it from the room)', 'head: otoshi-gake lintel at ~1.9-2.0'],
    variants=[V('_1ken', '1 ken wide'), V('_half', 'half ken (small zashiki, T2 headman)', 2)],
    structural='YES: a RECESS in the shell wall (one extra 0.91 bay + a post); decide it per shell at the architect stage, not by the decorator',
    loot_surface='the toko-ita / tatami of the alcove: 1 shelf-type point (range 0.3)',
    abandoned_state='scroll hanging askew or fallen, vase tipped, dust', deviations=['Status feature: never in ordinary commoner shells (PLAYBOOK rule 11, N04)'], lod_budget='part of the building budget: <=250 faces')

add(FIT, id='jp_p_fit_chigaidana', name='Staggered shelves (chigaidana) beside the tokonoma',
    what='The shoin-style staggered shelves with small cupboards, beside a tokonoma. Samurai, honjin and official rooms only.',
    importance='standard', tiers=[3], priority='P3', room_tags=['zashiki'], status_overlay='samurai',
    period_evidence='Tokonoma of upper farmers and townsmen paired with shelves and a writing alcove [search summary of kotobank/touken-world, see N04]; the 1668 Edo rules bar tsuke-shoin for townsmen [T48]',
    refs=[R('i43_morse_guestroom', 'Morse 1885: guest room with shelves beside the tokonoma'), R('i44_morse_country_guestroom', 'Morse 1885: country house guest room')],
    dimensions={'width_m': D('0.91-1.82 (the toko-waki bay)', None, 'matches the tokonoma bay'), 'depth_m': D('0.455', None, 'half of a 0.91 recess'), 'shelves_m': D('two boards at 0.9 / 1.1, stagger 0.15; top cupboard (tenbukuro) under the head', None, 'typical')},
    materials=[M('shelves, cupboards', 'jp_m_wood_interior', 'timber_interior'), M('cupboard doors (plain paper)', 'jp_m_paper_fusuma', 'gofun_white')],
    connectors=['post: in the bay beside a tokonoma'], variants=[V('_std', 'two staggered boards + upper cupboard')],
    structural='YES: RECESS (the toko-waki bay)', loot_surface='both shelf boards: 2 shelf points (range 0.15-0.2)',
    abandoned_state='cupboard doors open, one torn; small lacquer box on the floor', deviations=['Status feature (PLAYBOOK §2.2)'], lod_budget='<=300 faces')

add(FIT, id='jp_p_fit_oshiire', name='Bedding closet (oshiire) with a middle shelf',
    what='A built-in closet behind sliding doors. Rare in 1730: it enters plans mid-to-late Edo and becomes general after Meiji; before it, bedding went into the nando storeroom.',
    importance='filler', tiers=[3], priority='P2', room_tags=['sleeping', 'zashiki'],
    period_evidence='Oshiire appear in plans mid-to-late Edo, general after Meiji; bedding was kept in the nando before [N09]',
    refs=[R('i35_morse_kitchen_closet', 'Morse 1885: closets, drawers and cupboards built into the wall'), R('N09', 'oshiire history (text)')],
    dimensions={'bay_m': D('0.91 or 1.82 wide x 0.80 deep', None, 'modern standard; period form unverified'), 'shelf_m': D('middle shelf at 0.75', None, 'modern standard')},
    materials=[M('carcass', 'jp_m_wood_interior', 'timber_interior'), M('doors (plain fusuma)', 'jp_m_paper_fusuma', 'gofun_white')],
    connectors=['post: fills one wall bay; doors are a normal fusuma twin (no player passage)'], variants=[V('_1ken', '1 ken wide')],
    structural='YES: a RECESS or a bay taken from the room (0.80 deep) + fusuma leaves', loot_surface='middle shelf + floor of the closet: 2 points',
    abandoned_state='doors half open, bedding pulled half out onto the floor', deviations=['Late for 1730: inns and samurai houses only if Stephen allows (decision 8)'], lod_budget='<=250 faces')

add(FIT, id='jp_p_fit_ceiling', name='Ceiling recipes: sao-buchi board ceiling, joist-and-board loft floor, exposed sooted rafters, bamboo slat (sunoko) over the hearth',
    what='What you see overhead, by tier: exposed sooted roof structure in T1 and farm kitchens, the loft floor on joists in townhouses (as built), a batten-and-board ceiling in T2-3 best rooms, slatted bamboo over an irori.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['zashiki', 'living', 'sleeping', 'daidokoro', 'shop', 'office'],
    period_evidence='Sao-buchi: boards on parallel battens; ceilings were once for high-status buildings and spread to houses [N17]; Morse ceiling section [i41]; machiya loft floor as ceiling [machiya_t3_01: sao_joist]; farm kitchens open to the smoked roof [i04, i05]',
    refs=[R('i41_morse_ceiling', 'Morse 1885: section of an ordinary ceiling (battens and boards)'), R('i42_morse_guestroom_hachiishi', 'Morse 1885: inn guest room with a board ceiling'),
          R('i06_tsunashima_doma', 'farmhouse doma open to the dark roof structure', True)],
    dimensions={'height_m': D('2.50-2.70 clear (D6)', 'PLAYBOOK §4'), 'batten_m': D('sao 0.04 x 0.045 at 0.45 (quarter ken)', None, 'typical sao-buchi spacing ~1.5 shaku'),
                'board_m': D('0.30-0.45 wide, 0.009 thick, lapped', None, 'typical'), 'sunoko_m': D('split bamboo 0.03 at 0.05 c/c', None, 'form only')},
    materials=[M('ceiling boards', 'jp_m_ceil_boards', 'timber_interior'), M('battens', 'jp_m_wood_interior', 'timber_interior'), M('exposed rafters (T1, kitchens)', 'jp_m_wood_sooted', 'timber_sooted'),
               M('bamboo slats over the hearth', 'jp_m_bamboo_sooted', 'timber_sooted')],
    connectors=['head: ceiling line 2.50-2.70 over the room floor; the room rect from rooms.json'],
    variants=[V('_saobuchi', 'batten-and-board ceiling: T2-3 zashiki, inn rooms, samurai', 2), V('_neda', 'loft floor seen from below (exists in the machiya)', 2),
              V('_open', 'no ceiling: sooted rafters and thatch underside (T1, farm doma and daidokoro)', 1), V('_sunoko', 'bamboo slats over an irori room', 1)],
    structural='NONE (head room stays >=2.10 everywhere; D6 heights)', loot_surface='none',
    abandoned_state='a few boards sagging or missing (dark gap), cobwebs as decal, water stain', deviations=['D6 ceiling height'], lod_budget='part of the building budget (flat quads)')

add(FIT, id='jp_p_fit_setchin', name='Privy floor (setchin): board floor with a slot over a buried jar',
    what='Inside the toilet shell: a board floor with a long slot, a buried pottery jar under it, a small hand-wash bowl outside.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['toilet'],
    period_evidence='Toilet shell kept [KEEP_DWELLINGS 26]; privy interiors drawn by Morse (1885) [BL §3]; night-soil was collected and sold (form assumed)',
    refs=[R('N20', 'BUILDING_LIST shared kit and the toilet entries (text)')],
    dimensions={'floor_m': D('0.91 x 1.365 (half ken x 0.75 ken)', None, 'reason: grid; a door >=1.00 cannot fit a half-ken shell, see open question'),
                'slot_m': D('0.15 x 0.45', None, 'typical')},
    materials=[M('floor boards', 'jp_m_floor_boards_rough', 'timber_interior'), M('jar rim', 'jp_m_ceramic_stoneware_dark', 'stoneware_dark')],
    connectors=['floor: the toilet shell floor recipe'], variants=[V('_std', 'slot + jar')],
    structural='YES: FLOOR SLOT (visual only; Geometry stays closed so nobody falls in)', loot_surface='1 floor point (range 0.25)',
    abandoned_state='door ajar, straw on the floor', deviations=['D1: a real privy door is ~0.6 m; the shell must still give >=1.00 if loot is inside (open question for the architect)'], lod_budget='<=150 faces')

# ------------------------------------------------------------------------------------------------ PROPS
KIT = 'Kitchen, hearth and water (props)'
HEAT = 'Heat and light (props)'
STO = 'Storage and packing (props)'
BED = 'Bedding and seating (props)'
SHOP = 'Office and shop (props)'
REL = 'Religious (props)'
FARM = 'Farm, stable and work (props)'
ABD = 'Dead-world dressing (props)'

add(KIT, id='jp_f_kama', name='Iron cooking pot (kama) with wooden lid, and small pot (nabe) with a bail handle',
    what='The rice pot that sits in a kamado rim, and the smaller hanging pot for the irori hook.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro'],
    period_evidence='Pot (nabe) in 63 and cauldron in 20 building entries [BL §5.1]; pot on the kamado with a thick wooden lid [i20]; spouted kettle in a 1685 print [i16]',
    refs=[R('i20_hachioji_kamado', 'iron pot with a heavy wooden lid on a kamado', True), R('i31_morse_kitchen_range', 'Morse 1885: pots on the range'), R('i04_tsunashima_irori', 'pot hanging over the irori', True)],
    dimensions={'kama_m': D('rim d 0.36-0.44 (fits the kamado rim), body d 0.42, h 0.28, flange ring', 'machiya build rims 0.44'), 'lid_m': D('d 0.46, 0.04 thick, two cleats', None, 'i20'), 'nabe_m': D('d 0.28, h 0.16, bail handle', None, 'typical')},
    materials=[M('pot', 'jp_m_metal_iron', 'iron_black'), M('lid', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: in a kamado rim (kama) or on the jizai-kagi hook (nabe) or on the floor'],
    variants=[V('_kama', 'rice pot with lid'), V('_kama_nolid', 'lid off, lying beside (abandoned)'), V('_nabe', 'small pot with bail')],
    loot_surface='none (too small; the kamado top carries the point)', abandoned_state='lid knocked off, rust bloom, burnt crust; one rim left empty',
    wave=1, pilot=['kitchen'], blocks_path='', lod_budget='small prop <=300 faces')

add(KIT, id='jp_f_jizai_kagi', name='Pot hook (jizai-kagi) with fish-shaped lever (yokogi)',
    what='The adjustable bamboo-and-iron hook over every irori, with the carved fish lever; hangs from the hook beam of jp_p_fit_irori.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['daidokoro', 'living', 'guard'],
    period_evidence='Jizai-kagi and fish yokogi at the irori [N12]; in the Kitamura 1687 set [BL §3]; Morse sketch of a peasant ji-zai [i33]',
    refs=[R('i33_morse_jizai', 'Morse 1885: simple peasant ji-zai'), R('i21_jizai_kettle', 'kettle on a jizai over an irori (Boso-no-mura)'), R('i03_tenmyo_irori', 'long bamboo jizai from the beam', True)],
    dimensions={'length_m': D('1.2-1.8 (bamboo tube + iron hook), bottom 0.6-0.9 above the ash', None, 'from the photos'), 'yokogi_m': D('0.35 x 0.10 x 0.05 fish', None, 'from the photos')},
    materials=[M('bamboo tube (sooted)', 'jp_m_bamboo_sooted', 'timber_sooted'), M('hook', 'jp_m_metal_iron', 'iron_black'), M('fish lever', 'jp_m_wood_sooted', 'timber_sooted')],
    connectors=['proxy_base: at the hook point of jp_p_fit_irori (hangs; no floor contact)'], variants=[V('_std', 'with fish lever'), V('_plain', 'plain bar lever (poor)', 1)],
    loot_surface='none', abandoned_state='hook empty or holding a rusted nabe, lever jammed high', wave=1, pilot=[], blocks_path='', lod_budget='small prop <=300 faces',
    open_questions=['No Geometry: it hangs over the pit, the player cannot bump it'])

add(KIT, id='jp_f_mizugame', name='Water jar (mizugame) with a wooden lid and a dipper',
    what='The big stoneware jar beside the sink that held the day\'s water; the dipper (hishaku) rests on the lid.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma'],
    period_evidence='Water jar in 15 building entries [BL §5.1]; nagaya kitchen water jar, drawn by ladle [N10]; big jar on a raised floor in a 1685 print [i18]',
    refs=[R('i08_edo_nagaya_kitchen', 'water jar beside the stove and sink (c.1840 reconstruction)'), R('i18_moronobu_1685_p9', 'Moronobu 1685: large jar, buckets and a spouted pot on a board floor', True),
          R('i50_met_tokkuri_stoneware', 'stoneware of 1700-1750: body and glaze colour', True)],
    dimensions={'jar_m': D('d 0.55, h 0.60 (about 90 litres)', None, 'from the reconstruction photo; one kitchen day of water'), 'lid_m': D('d 0.60 boards, 0.03', None, 'i08')},
    materials=[M('jar', 'jp_m_ceramic_stoneware_dark', 'stoneware_dark'), M('lid, dipper', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: on the doma, against a wall beside jp_p_fit_nagashi'], variants=[V('_lid', 'lid on, dipper on top'), V('_open', 'lid off leaning against it, dry inside'), V('_broken', 'cracked, a shard missing (abandoned)')],
    loot_surface='the lid top at 0.63: 1 shelf point (range 0.2)', abandoned_state='lid off and leaning, empty and dusty, or cracked with a shard on the floor',
    wave=1, pilot=['kitchen'], blocks_path='keep >=1.00 m past it in a tori-niwa', lod_budget='small prop <=300 faces')

add(KIT, id='jp_f_oke', name='Wooden tubs and buckets (oke, tarai, pickle tub with stone)',
    what='The coopered family: a handled bucket, a shallow washing tub, a tall pickle tub weighted with a stone. The most common kitchen and workshop items of all.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro', 'workshop', 'storage', 'bath'],
    period_evidence='Wooden tubs in 64 and buckets in 38 building entries [BL §5.1]; tubs in Moronobu\'s 1685 workshops (sword polisher, dyer) [i16, i17]; tub scene before 1694 [i19]',
    refs=[R('i16_moronobu_1685_p6', 'Moronobu 1685: sword polisher with two big tubs and a box', True), R('i17_moronobu_1685_p7', 'Moronobu 1685: dyer treading cloth in round tubs', True),
          R('i19_moronobu_tub', 'Moronobu (before 1694): large shallow round tub', True), R('i05_tsunashima_kamado', 'bucket and tub in a farmhouse doma', True)],
    dimensions={'bucket_m': D('d 0.30, h 0.30, handle ears to 0.45', None, 'typical coopered bucket'), 'tarai_m': D('d 0.60, h 0.20', None, 'i19'), 'pickle_m': D('d 0.45, h 0.50 + lid + stone 0.20', None, 'typical')},
    materials=[M('staves', 'jp_m_wood_interior', 'timber_interior'), M('hoops (bamboo)', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('stone', 'jp_m_stone_river', 'stone_lantern')],
    connectors=['proxy_base: on any floor'], variants=[V('_bucket', 'handled bucket'), V('_tarai', 'shallow tub'), V('_pickle', 'tall tub, lid, stone'), V('_tipped', 'bucket on its side (abandoned)')],
    loot_surface='tarai bottom (floor point r 0.25); pickle-tub lid at 0.55 (shelf point r 0.15)', abandoned_state='tipped over, hoop sprung, staves gapped and dry; pickle stone on the floor',
    wave=1, pilot=['kitchen', 'toriniwa'], blocks_path='never inside a door clear zone', lod_budget='small prop <=300 faces')

add(KIT, id='jp_f_tana', name='Open wall shelf (tana) on brackets, 1-3 boards',
    what='Plain board shelves on the kitchen, shop or storage wall: bowls, jars, boxes. The main raised loot surface of a Japanese interior.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro', 'storage', 'shop', 'workshop', 'living'],
    period_evidence='Racks and shelves in 80 building entries [BL §5.3]; "one shelf" even in the poorest tenement [BL §3 ura-nagaya]; kitchen shelves [i32, i08]',
    refs=[R('i32_morse_city_kitchen', 'Morse 1885: shelves and racks in a city kitchen'), R('i08_edo_nagaya_kitchen', 'tenement kitchen shelf'), R('i35_morse_kitchen_closet', 'Morse 1885: shelves built into a kitchen')],
    dimensions={'width_m': D('0.91 / 1.365 / 1.82 (half-ken steps)', 'PLAYBOOK rule 9'), 'depth_m': D('0.30', None, 'fits a bowl stack; stays out of the walking band'),
                'boards_m': D('at 0.90 / 1.30 / 1.70 (one to three)', None, 'reason: reachable heights; vanilla shelves carry loot 0.11-1.24 (Q5)')},
    materials=[M('boards, brackets', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: on the floor against a wall (legs) or wall-mounted (base point at the lowest board, footprint on the floor for loot subtraction)'],
    variants=[V('_1', 'one board'), V('_3', 'three boards'), V('_sag', 'one bracket gone, board hanging (abandoned)')],
    loot_surface='each board: 1 shelf point per 0.9 m (range 0.15-0.2)', abandoned_state='a few bowls left, most fallen and broken on the floor below (debris decal), one board sagging',
    wave=1, pilot=['kitchen', 'storage', 'mise'], blocks_path='', lod_budget='furniture <=1000 faces')

add(KIT, id='jp_f_firewood', name='Firewood stack (maki) and brushwood bundle',
    what='Split logs stacked beside the kamado or under the eaves, and tied brushwood bundles (soda).',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro', 'workshop', 'storage'],
    period_evidence='Firewood stacks in 18 building entries [BL §5.2]; firewood beside a kamado [i22]',
    refs=[R('i22_kamado_firewood', 'split firewood stacked beside a clay kamado'), R('i04_tsunashima_irori', 'firewood at the hearth', True)],
    dimensions={'stack_m': D('0.91 x 0.40 x 0.60 high (half-ken)', None, 'reason: grid'), 'log_m': D('0.40-0.45 long, d 0.06-0.12', None, 'typical split wood'), 'bundle_m': D('d 0.35 x 0.9', None, 'typical')},
    materials=[M('split wood', 'jp_m_wood_weathered', 'timber_weathered'), M('bindings', 'jp_m_straw_tawara', 'thatch_new')],
    connectors=['proxy_base: doma floor against a wall'], variants=[V('_stack', 'neat stack'), V('_low', 'half used'), V('_bundle', 'brushwood bundles')],
    loot_surface='stack top at 0.60: 1 point (range 0.2)', abandoned_state='half used, a few logs rolled across the floor', wave=1, pilot=['kitchen'], blocks_path='', lod_budget='small prop <=300 faces')

add(KIT, id='jp_f_jar', name='Storage jars (miso, oil, salt, pickles), 3 sizes, with lids',
    what='Stoneware jars on the kitchen or storage floor and shelves.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro', 'storage', 'shop'],
    period_evidence='Jars in 40 building entries [BL §5.3]; stoneware of 1700-1750 [i50]; large jar in a 1685 print [i18]',
    refs=[R('i50_met_tokkuri_stoneware', 'The Met: stoneware sake bottle, 1700-1750 (glaze and body colour)', True), R('i18_moronobu_1685_p9', 'Moronobu 1685: large jar', True),
          R('i51_met_tokkuri_porcelain', 'The Met: blue-and-white porcelain bottle, early 18th c. (T3 accent)', True)],
    dimensions={'small_m': D('d 0.18, h 0.22', None, 'typical'), 'medium_m': D('d 0.30, h 0.40', None, 'typical'), 'large_m': D('d 0.45, h 0.60', None, 'typical')},
    materials=[M('jar', 'jp_m_ceramic_stoneware_dark', 'stoneware_dark'), M('pale-glaze variant', 'jp_m_ceramic_stoneware_pale', 'stoneware_pale'), M('lid', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: floor or a tana board'], variants=[V('_s', 'small'), V('_m', 'medium'), V('_l', 'large'), V('_broken', 'shards (abandoned)')],
    loot_surface='large jar lid at 0.62: 1 point (range 0.15)', abandoned_state='lids off, one broken in shards on the floor, dried spill stain', wave=1, pilot=['kitchen', 'storage'], blocks_path='', lod_budget='small prop <=300 faces')

add(KIT, id='jp_f_tableware', name='Tableware clutter: box trays (hakozen) and legged trays (zen), bowls, dishes, chopsticks',
    what='The meal set of a household: stacked box trays, bowls in lacquer and ceramic. Used as clutter on shelves, floors and trays.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['daidokoro', 'doma', 'living', 'zashiki', 'shop'],
    period_evidence='Trays in 58 and bowls/dishes in 44 building entries [BL §5.1]; hakozen stack in the Kitamura-type set [BL §3]',
    refs=[R('i07_edo_nagaya_room', 'tenement room dressing with trays and bowls'), R('N20', 'BL §5.1 (text)')],
    dimensions={'hakozen_m': D('0.30 x 0.30 x 0.20', None, 'typical box tray'), 'zen_m': D('0.36 x 0.36 x 0.15', None, 'typical'), 'bowl_m': D('d 0.12, h 0.07', None, 'typical')},
    materials=[M('trays', 'jp_m_lacquer_black', 'sumi_black'), M('plain wood trays (T1)', 'jp_m_wood_interior', 'timber_interior'), M('bowls', 'jp_m_ceramic_stoneware_pale', 'stoneware_pale')],
    connectors=['proxy_base: floor, shelf or tray'], variants=[V('_stack', 'hakozen stack'), V('_meal', 'a zen with bowls, left mid-meal (abandoned)'), V('_scatter', 'bowls scattered')],
    loot_surface='none (clutter)', abandoned_state='a meal left out, bowls overturned', wave=2, pilot=[], blocks_path='', lod_budget='small prop <=300 faces')

add(HEAT, id='jp_f_andon', name='Standing paper lamp (andon), square type, and the small bedside type (ariake)',
    what='The oil lamp in a paper box that lit every room after dark; unlit in our dead world.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['living', 'zashiki', 'sleeping', 'shop', 'office', 'guard'],
    period_evidence='Andon spread in the Edo period: wood/bamboo frame, paper cover, oil dish, rush or cotton wick; types oki, ariake, enshu [N13]; lamps in 74 building entries [BL §5.2]',
    refs=[R('i39_morse_andon', 'Morse 1885: andon, saucer lamp in a paper frame'), R('i40_morse_andon2', 'Morse 1885: another andon'), R('i07_edo_nagaya_room', 'andon in a tenement room (c.1840 reconstruction)')],
    dimensions={'kaku_m': D('0.25 x 0.25 x 0.80 high, open top, a drawer in the base', None, 'Morse fig. 206 proportions; typical museum pieces'), 'ariake_m': D('0.25 x 0.25 x 0.35', None, 'typical bedside box')},
    materials=[M('frame', 'jp_m_wood_interior', 'timber_interior'), M('paper', 'jp_m_paper_shoji', 'washi_shoji'), M('oil dish', 'jp_m_ceramic_stoneware_pale', 'stoneware_pale')],
    connectors=['proxy_base: floor, usually a room corner or beside bedding'], variants=[V('_kaku', 'square standing'), V('_ariake', 'small bedside'), V('_tipped', 'on its side, paper torn (abandoned)')],
    loot_surface='none (too small and tall)', abandoned_state='tipped over, paper torn and oil-stained, dish broken', wave=1, pilot=['zashiki', 'mise'], blocks_path='',
    lod_budget='small prop <=300 faces', open_questions=['Lit lamps are a later decision (light points); ship unlit'])

add(HEAT, id='jp_f_hibachi', name='Charcoal brazier (hibachi): round ceramic/wood, and the square wooden box type',
    what='The portable charcoal heater of every town room, shop and inn room, with metal tongs in the ash.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['living', 'zashiki', 'shop', 'office', 'sleeping', 'guard'],
    period_evidence='Braziers in 33 entries plus the ~61 shops [BL §5.2]; hibachi on the town-only core list [BL §5.9]',
    refs=[R('i36_morse_hibachi', 'Morse 1885: common hibachi'), R('i37_morse_hibachi_wood', 'Morse 1885: wooden hibachi'), R('i09_edo_nagaya_hibachi', 'box hibachi in a tenement room (c.1840 reconstruction)')],
    dimensions={'round_m': D('d 0.38, h 0.28', None, 'typical'), 'box_m': D('0.45 x 0.35 x 0.30', None, 'typical box brazier'), 'tongs_m': D('0.30 iron chopsticks', None, 'typical')},
    materials=[M('round body', 'jp_m_ceramic_stoneware_pale', 'stoneware_pale'), M('box body', 'jp_m_wood_interior', 'timber_interior'), M('ash', 'jp_m_ground_ash', 'ash_grey'), M('tongs, trivet', 'jp_m_metal_iron', 'iron_black')],
    connectors=['proxy_base: tatami or boards, near the room centre or the choba'], variants=[V('_round', 'round'), V('_box', 'square wooden box'), V('_tipped', 'tipped, ash spilled (abandoned)')],
    loot_surface='box rim at 0.30: 1 small point (range 0.12)', abandoned_state='cold ash, tongs lying on the mat; one in five tipped with an ash spill decal', wave=1, pilot=['mise', 'zashiki'], blocks_path='', lod_budget='small prop <=300 faces',
    open_questions=['Naga-hibachi (long brazier with drawers) date not checked: left out'])

add(HEAT, id='jp_f_tabakobon', name='Tobacco tray (tabako-bon) with fire pot, ash tube and pipe (kiseru)',
    what='The small wooden tray set out for customers and guests; part of the standard shop kit.',
    importance='filler', tiers=[2, 3], priority='P1', room_tags=['shop', 'zashiki', 'living', 'office', 'guard'],
    period_evidence='Tobacco tray / pipes in 18 entries plus the ~61 shops [BL §5.6]',
    refs=[R('i38_morse_tabakobon', 'Morse 1885: tabako-bon')], dimensions={'tray_m': D('0.30 x 0.20 x 0.18 with handle', None, 'Morse fig. 201 proportions')},
    materials=[M('tray', 'jp_m_wood_interior', 'timber_interior'), M('fire pot', 'jp_m_ceramic_stoneware_pale', 'stoneware_pale'), M('pipe', 'jp_m_metal_iron', 'iron_black')],
    connectors=['proxy_base: tatami or boards'], variants=[V('_std', 'tray'), V('_spilled', 'on its side, ash spilled')],
    loot_surface='none', abandoned_state='on its side, ash and a pipe on the mat', wave=1, pilot=['mise'], blocks_path='', lod_budget='small prop <=300 faces')

add(STO, id='jp_f_nagamochi', name='Long chest (nagamochi)',
    what='The big lidded clothes and bedding chest with iron fittings for a carrying pole; in storage rooms, nando and kura.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['storage', 'sleeping', 'loft'],
    period_evidence='Chests in 36 entries [BL §5.3]; nagamochi ~1.74 x 0.75 x 0.75 m, carried on a pole, spread from samurai to commoners as cotton bedding grew [N19]; tansu were still dear, so the nagamochi is the everyday big chest [N06]',
    refs=[R('N19', 'nagamochi size and use (text)'), R('i07_edo_nagaya_room', 'storage chests in a town room')],
    dimensions={'size_m': D('1.70 x 0.72 x 0.75 high', 'N19 (about 1.74 x 0.75 x 0.75)'), 'lid_m': D('flat lid 0.03, iron corner fittings and pole brackets', 'N19')},
    materials=[M('body', 'jp_m_wood_interior', 'timber_interior'), M('fittings', 'jp_m_metal_iron', 'iron_black')],
    connectors=['proxy_base: floor, long side against a wall'], variants=[V('_shut', 'lid shut'), V('_open', 'lid thrown back against the wall, cloth spilling (abandoned)')],
    loot_surface='lid top at 0.75: 2 shelf points (range 0.3); the open variant: 1 point inside at 0.10',
    abandoned_state='lid open, clothes pulled out and dropped, one fitting torn', wave=1, pilot=['storage'],
    blocks_path='1.70 m long: only along a wall, never across a path; a 3-mat room gets at most one', lod_budget='furniture <=1000 faces')

add(STO, id='jp_f_tansu', name='Clothing chest of drawers (isho-dansu), two stacked parts',
    what='The drawer chest of better town houses: two stacked boxes with iron handles. In 1730 still costly, so T2-3 only.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['sleeping', 'zashiki', 'living', 'office', 'storage'],
    period_evidence='Tansu appear in Osaka in the Kanbun era (1661-73) and spread from the Shotoku era (1711-16); costly, reaching poor commoners only in late Edo [N06]',
    refs=[R('i01_kasuya_irori', 'chest with iron fittings beside the hearth room (Kasuya house)', True), R('i07_edo_nagaya_room', 'drawer chest in a town room (c.1840 reconstruction)'), R('N06', 'tansu history (text)')],
    dimensions={'size_m': D('1.00 x 0.45 x 1.00 high (two parts of 0.50)', None, 'typical Edo isho-dansu proportions (about 3.3 x 1.5 x 3.3 shaku)'), 'drawers': D('4-5 drawers, iron ring pulls, carrying handles on the sides', None, 'typical')},
    materials=[M('body', 'jp_m_wood_interior', 'timber_interior'), M('fittings', 'jp_m_metal_iron', 'iron_black')],
    connectors=['proxy_base: floor against a wall; back 0.02 off the wall'], variants=[V('_shut', 'drawers shut'), V('_ransacked', 'two drawers pulled out, one on the floor, clothes spilled (abandoned)'), V('_single', 'one part only (T2)', 2)],
    loot_surface='top at 1.00: 2 points (range 0.2); ransacked: 1 point in the dropped drawer (floor)',
    abandoned_state='ransacked: drawers out, one on the floor', wave=1, pilot=['zashiki'], blocks_path='the dropped drawer lies inside the tansu front zone, never in a path', lod_budget='furniture <=1000 faces')

add(STO, id='jp_f_kori', name='Wicker trunk (kori), lidded, stackable',
    what='The light woven travel and clothes trunk of townspeople and tenants.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['sleeping', 'living', 'storage', 'loft'],
    period_evidence='Kori on the town-only core list [BL §5.9]; wicker trunk in the tenement set [BL §3 ura-nagaya]',
    refs=[R('N20', 'BL §3/§5 (text)'), R('i07_edo_nagaya_room', 'tenement room dressing')],
    dimensions={'size_m': D('0.60 x 0.40 x 0.30 (lid over the base)', None, 'typical')},
    materials=[M('wicker', 'jp_m_bamboo_weave', 'bamboo_weathered'), M('cord', 'jp_m_straw_tawara', 'thatch_new')],
    connectors=['proxy_base: floor or on another kori'], variants=[V('_1', 'single'), V('_2', 'stack of two'), V('_open', 'lid off beside it')],
    loot_surface='lid top at 0.30 (0.60 stacked): 1 point (range 0.2)', abandoned_state='lid off, empty or a garment hanging out', wave=1, pilot=['storage', 'zashiki'], blocks_path='', lod_budget='small prop <=300 faces')

add(STO, id='jp_f_box', name='Lidded wooden boxes (hako): 3 sizes, stacked',
    what='The most-named item in the whole building list: document, letter, meal, goods and tool boxes.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['storage', 'shop', 'office', 'living', 'zashiki', 'workshop', 'loft'],
    period_evidence='Wooden boxes in 93 building entries, the top item of the kit [BL §5.3]; boxes beside workers in 1685 [i16]',
    refs=[R('i16_moronobu_1685_p6', 'Moronobu 1685: lidded box beside the polisher', True), R('x33_jinrin_bookseller_1690', 'Jinrin kinmo zui 1690: stacked boxes and books at a shop', True)],
    dimensions={'small_m': D('0.30 x 0.20 x 0.12', None, 'letter/document box'), 'medium_m': D('0.45 x 0.30 x 0.25', None, 'typical'), 'large_m': D('0.60 x 0.40 x 0.40', None, 'goods box')},
    materials=[M('box', 'jp_m_wood_interior', 'timber_interior'), M('lacquer variant (T3, elite)', 'jp_m_lacquer_black', 'sumi_black')],
    connectors=['proxy_base: floor, shelf, or on another box'], variants=[V('_s', 'small'), V('_m', 'medium'), V('_l', 'large'), V('_stack3', 'stack of three'), V('_open', 'lid off, spilled')],
    loot_surface='large box / stack top: 1 point (range 0.2)', abandoned_state='lids off, contents (paper, cloth) spilled, one box on its side', wave=1, pilot=['storage', 'mise'], blocks_path='', lod_budget='small prop <=300 faces')

add(STO, id='jp_f_tawara', name='Straw rice bale (tawara) and straw bag (kamasu)',
    what='Rice, salt and charcoal came in straw bales; stacked in storage, kura, shops and farm doma.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['storage', 'doma', 'shop', 'loft', 'workshop'],
    period_evidence='Straw bales in 30 and straw bags in 20 entries [BL §5.3]; rural core item [BL §5.9]',
    refs=[R('N20', 'BL §5.3 (text)'), R('i06_tsunashima_doma', 'straw goods on a farmhouse doma', True)],
    dimensions={'tawara_m': D('d 0.40, L 0.75 (about 4 to of rice, 60 kg)', None, 'typical Edo rice bale'), 'kamasu_m': D('0.60 x 0.40 x 0.15 flat bag', None, 'typical')},
    materials=[M('straw', 'jp_m_straw_tawara', 'thatch_new')],
    connectors=['proxy_base: floor; stacks as a pyramid 3-2-1'], variants=[V('_1', 'single bale'), V('_stack6', 'pyramid of six'), V('_burst', 'burst bale, rice/straw spilled (abandoned)'), V('_kamasu', 'straw bag')],
    loot_surface='stack top: 1 point (range 0.25)', abandoned_state='one burst with a spill decal, rats\' work', wave=1, pilot=['storage'], blocks_path='a 6-stack is 1.2 x 0.75: along walls only', lod_budget='small prop <=300 faces')

add(STO, id='jp_f_rack', name='Free-standing board shelving (kura / storage shelves), 3 boards',
    what='Plain post-and-board shelving along storage and kura walls, and the goods shelves behind a shop.',
    importance='standard', tiers=[1, 2, 3], priority='P1', room_tags=['storage', 'loft', 'shop', 'workshop'],
    period_evidence='Racks in 80 entries; kura shelving on the T3 storage list [BL §5.3, WORLD_CATALOGUE §2.10]; goods shelves in the 1768 Echigoya [i13]',
    refs=[R('i13_echigoya_1768', 'shelves of goods behind the clerks (1768)', True), R('i35_morse_kitchen_closet', 'Morse 1885: built-in shelving')],
    dimensions={'size_m': D('1.82 (or 0.91) x 0.45 x 1.80 high', None, 'reason: grid; stays under the 2.00 head rail'), 'boards_m': D('at 0.10 / 0.70 / 1.25', None, 'reason: like vanilla case_d loot levels 0.11/0.48/0.86/1.24 (Q5)')},
    materials=[M('posts, boards', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: floor against a wall'], variants=[V('_1ken', '1.82 wide'), V('_half', '0.91 wide'), V('_collapsed', 'one board down at an angle (abandoned)')],
    loot_surface='each board: 1-2 shelf points (range 0.15-0.25); the vanilla lootshelves pattern', abandoned_state='half emptied, boxes and jars on the floor in front, one board collapsed',
    wave=1, pilot=['storage'], blocks_path='0.45 deep along walls only; in a 2 x 2 ken storage keep the centre clear', lod_budget='furniture <=1000 faces')

add(STO, id='jp_f_taru', name='Casks (taru): sake, soy and oil barrels, with a low rack',
    what='Coopered casks with rope bindings; the sake shop set racks them, kitchens and storerooms hold one or two.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['storage', 'shop', 'doma', 'workshop'],
    period_evidence='Casks and barrels in 22 entries [BL §5.3]; sake shop dressing, casks on a rack [KEEP_TRADES A]',
    refs=[R('N20', 'BL §5.3 (text)'), R('i16_moronobu_1685_p6', 'coopered tubs of 1685 (same craft)', True)],
    dimensions={'taru_m': D('d 0.45, h 0.50 (4-to cask)', None, 'typical'), 'rack_m': D('1.82 x 0.60 x 0.30', None, 'reason: grid')},
    materials=[M('staves', 'jp_m_wood_interior', 'timber_interior'), M('rope, straw wrap', 'jp_m_straw_tawara', 'thatch_new')],
    connectors=['proxy_base: floor or rack'], variants=[V('_1', 'single'), V('_rack3', 'three on a rack'), V('_stove', 'staved-in, dry (abandoned)')],
    loot_surface='cask top at 0.50: 1 point (range 0.15)', abandoned_state='one staved in, a dry stain', wave=2, pilot=[], blocks_path='', lod_budget='small prop <=300 faces')

add(STO, id='jp_f_basket', name='Baskets (zaru, kago, back basket)',
    what='Bamboo baskets for rice washing, vegetables and carrying; hung on pegs or on the floor.',
    importance='filler', tiers=[1, 2, 3], priority='P2', room_tags=['doma', 'daidokoro', 'storage', 'workshop'],
    period_evidence='Baskets in 34 entries [BL §5.3]', refs=[R('N20', 'BL §5.3 (text)'), R('i18_moronobu_1685_p9', 'Moronobu 1685: carrier with stacked vessels on a pole', True)],
    dimensions={'zaru_m': D('d 0.40, h 0.08', None, 'typical'), 'kago_m': D('d 0.35, h 0.30', None, 'typical'), 'back_m': D('0.45 x 0.35 x 0.60', None, 'typical')},
    materials=[M('weave', 'jp_m_bamboo_weave', 'bamboo_weathered')], connectors=['proxy_base: floor or a wall peg'],
    variants=[V('_zaru', 'flat sieve'), V('_kago', 'deep basket'), V('_back', 'back basket')], loot_surface='none', abandoned_state='crushed or on its side',
    wave=2, pilot=[], blocks_path='', lod_budget='small prop <=300 faces')

add(BED, id='jp_f_futon_stack', name='Folded bedding stack (sleeping mat futon + sleeved quilt yogi)',
    what='Bedding folded in a corner or in the nando, often behind a low screen.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['sleeping', 'zashiki', 'living'],
    period_evidence='Yogi (sleeved quilt) and futon from the Edo period; Kamigata used futon from Genroku, Edo kept the yogi; cotton was costly [N08]; bedding in 44 entries [BL §5.4]; no oshiire yet, bedding in the nando [N09]',
    refs=[R('N08', 'Edo bedding (text)'), R('i07_edo_nagaya_room', 'bedding in a tenement room (c.1840 reconstruction)')],
    dimensions={'stack_m': D('0.95 x 0.65 x 0.45 (two futon + one yogi)', None, 'folded in thirds; typical'), 'futon_m': D('1.85 x 0.95 x 0.06 unfolded', None, 'fits one mat')},
    materials=[M('covers', 'jp_m_textile_cotton_indigo', 'aizome_kon'), M('plain lining', 'jp_m_textile_cotton_plain', 'kinari_cloth')],
    connectors=['proxy_base: tatami or boards, in a corner'], variants=[V('_stack', 'folded stack'), V('_slumped', 'stack slumped over (abandoned)')],
    loot_surface='top at 0.45: 1 point (range 0.25)', abandoned_state='slumped, one quilt dragged half off, mildew patches', wave=1, pilot=['zashiki'], blocks_path='', lod_budget='furniture <=1000 faces')

add(BED, id='jp_f_futon_laid', name='Laid-out bedding (futon with the quilt thrown back)',
    what='A bed still laid out as its sleeper left it: the dead-world signature of a sleeping room.',
    importance='filler', tiers=[2, 3], priority='P1', room_tags=['sleeping', 'zashiki', 'living'],
    period_evidence='As jp_f_futon_stack [N08]', refs=[R('N08', 'Edo bedding (text)')],
    dimensions={'size_m': D('1.85 x 0.95 x 0.08; quilt thrown back 0.15 thick', None, 'one mat')},
    materials=[M('covers', 'jp_m_textile_cotton_indigo', 'aizome_kon'), M('lining', 'jp_m_textile_cotton_plain', 'kinari_cloth')],
    connectors=['proxy_base: flat on tatami, aligned with a mat'], variants=[V('_thrown', 'quilt thrown back'), V('_dragged', 'dragged aside, pillow apart (never across a door band)')],
    loot_surface='the whole futon is a loot zone: 1-2 points (range 0.4), like vanilla beds (Q5: points at 0.34-0.52 on beds)',
    abandoned_state='as left; stained, flattened', wave=1, pilot=['zashiki'], blocks_path='no: a thin 0.08 Geometry slab you step over (vanilla beds have Geometry and Roadway)', lod_budget='small prop <=300 faces',
    open_questions=['G4 check: items spawned on the quilt stay on it (vanilla bed points sit 0.33-0.52 up)'])

add(BED, id='jp_f_mushiro', name='Straw floor mats (mushiro / goza): flat, rolled, and a small pile',
    what='The floor covering of every T1 room and every work floor; rolled and stacked in storage.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['daidokoro', 'living', 'sleeping', 'doma', 'storage', 'workshop', 'stable'],
    period_evidence='Straw or rush mats in 49 entries [BL §5.4]; T1 rooms: boards or earth with straw and mushiro mats, no tatami [PLAYBOOK §2.1, T58]; mat draped over a bench in a farmhouse doma [i06]',
    refs=[R('i06_tsunashima_doma', 'straw mat draped over a bench in a farmhouse doma', True), R('c15_farmhouse_interior', 'farmhouse board floor')],
    dimensions={'flat_m': D('1.82 x 0.91 x 0.01', None, 'reason: one tatami module'), 'roll_m': D('d 0.18 x 0.91', None, 'typical')},
    materials=[M('straw', 'jp_m_straw_mushiro', 'thatch_new')],
    connectors=['proxy_base: flat on boards or earth (no Geometry; decal-like)'], variants=[V('_flat', 'flat mat'), V('_rolled', 'rolled'), V('_torn', 'torn, corner curled')],
    loot_surface='flat mats are floor loot zones (they do not subtract from floor loot)', abandoned_state='curled, torn, straw litter around', wave=1, pilot=['storage'], blocks_path='flat: none (no Geometry)', lod_budget='small prop <=300 faces')

add(BED, id='jp_f_enza', name='Round straw cushion (enza) and cotton cushion (zabuton)',
    what='Seating: round straw cushions everywhere; cotton zabuton only for guests in T3 shops, inns and samurai rooms.',
    importance='filler', tiers=[1, 2, 3], priority='P2', room_tags=['daidokoro', 'living', 'zashiki', 'shop', 'office'],
    period_evidence='Round straw cushions (enza) in the Kitamura-type set [BL §3]; cotton-filled zabuton develop from the shitone in mid-Edo, commoners widely only after Meiji [N07]; contradiction 2 of BL §4.2 resolved this way',
    refs=[R('N07', 'zabuton history (text)'), R('N20', 'BL §3 (text)')], dimensions={'enza_m': D('d 0.40, 0.03', None, 'typical'), 'zabuton_m': D('0.55 x 0.60 x 0.06', None, 'typical Edo size, smaller than modern')},
    materials=[M('straw', 'jp_m_straw_mushiro', 'thatch_new'), M('cotton (T3)', 'jp_m_textile_cotton_indigo', 'aizome_kon')],
    connectors=['proxy_base: flat on the floor (no Geometry)'], variants=[V('_enza', 'straw'), V('_zabuton', 'cotton (T3 only)', 3)],
    loot_surface='none', abandoned_state='scattered, one kicked against the wall', wave=2, pilot=[], blocks_path='none (no Geometry)', lod_budget='small prop <=300 faces')

add(BED, id='jp_f_byobu', name='Low bedding screen (makura-byobu, 2 panels) and entrance screen (tsuitate)',
    what='The low two-panel screen that hid folded bedding in one-room homes; the single standing screen at an entrance.',
    importance='standard', tiers=[1, 2, 3], priority='P2', room_tags=['living', 'sleeping', 'zashiki', 'doma'],
    period_evidence='Folding screens / entrance screens in 21 entries; makura-byobu hides bedding in the tenement [BL §3, §5.4]',
    refs=[R('N20', 'BL §3/§5.4 (text)'), R('i07_edo_nagaya_room', 'tenement room dressing')],
    dimensions={'makura_m': D('2 panels of 0.60 x 0.90 high', None, 'typical low screen'), 'tsuitate_m': D('1.20 x 1.40 high on two feet', None, 'typical')},
    materials=[M('frame', 'jp_m_wood_interior', 'timber_interior'), M('paper (plain)', 'jp_m_paper_fusuma', 'gofun_white')],
    connectors=['proxy_base: floor'], variants=[V('_makura', 'low 2-panel'), V('_tsuitate', 'entrance screen'), V('_fallen', 'flat on the floor, torn (abandoned)')],
    loot_surface='none', abandoned_state='fallen flat and torn', wave=2, pilot=[], blocks_path='YES when standing: place only against walls or across a corner; the fallen variant has no Geometry', lod_budget='small prop <=300 faces')

add(BED, id='jp_f_iko', name='Clothes rack (iko) with a robe hung over it',
    what='A standing frame over which a kimono is draped; bedrooms and inn rooms.',
    importance='standard', tiers=[2, 3], priority='P2', room_tags=['sleeping', 'zashiki', 'living'],
    period_evidence='Clothes rack / robe on a rack in 38 entries [BL §5.4]; town-only core [BL §5.9]', refs=[R('N20', 'BL §5.4 (text)')],
    dimensions={'size_m': D('1.50 wide x 0.40 deep x 1.50 high', None, 'typical')},
    materials=[M('frame', 'jp_m_lacquer_black', 'sumi_black'), M('plain frame (T2)', 'jp_m_wood_interior', 'timber_interior'), M('robe', 'jp_m_textile_cotton_indigo', 'aizome_kon')],
    connectors=['proxy_base: floor, parallel to a wall'], variants=[V('_robe', 'with a robe'), V('_bare', 'bare'), V('_fallen', 'fallen with the robe (abandoned)')],
    loot_surface='none', abandoned_state='fallen, the robe on the mat', wave=2, pilot=[], blocks_path='1.5 m wide: along walls only', lod_budget='furniture <=1000 faces')

add(SHOP, id='jp_f_zukue', name='Low writing / account desk (fuzukue, choba-zukue)',
    what='The low desk at which the shopkeeper kept accounts, and the writing desk of offices and study rooms.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['shop', 'office', 'zashiki', 'living', 'guard'],
    period_evidence='Low writing desk in 30 entries [BL §5.6]; the choba desk behind the lattice [N18]; a craftsman at a low board in 1685 [i16]',
    refs=[R('N18', 'merchant-house tools: choba desk, lattice, coin box (text)'), R('i16_moronobu_1685_p6', 'Moronobu 1685: seated work at a low board', True), R('i13_echigoya_1768', 'clerks at low desks (1768)', True)],
    dimensions={'size_m': D('0.90 x 0.40 x 0.33 high', None, 'seated-on-the-floor height'), 'drawer': D('one shallow drawer', None, 'typical')},
    materials=[M('desk', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: tatami or boards'], variants=[V('_choba', 'account desk with a drawer'), V('_plain', 'plain writing desk'), V('_tipped', 'on its side (abandoned)')],
    loot_surface='top at 0.33: 1 point (range 0.25)', abandoned_state='ledger open and scattered, ink box upset', wave=1, pilot=['mise'], blocks_path='', lod_budget='small prop <=300 faces')

add(SHOP, id='jp_f_choba_goshi', name='Counting-desk lattice (choba-goshi / kekkai), 2-3 folds',
    what='The low folding lattice that fences the shopkeeper\'s desk corner from the customers.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['shop', 'office'],
    period_evidence='A foldable low lattice at the choba of Edo merchant houses, separating customers from the clerk [N18]; counting desk with a lattice screen at T3 shops [WORLD_CATALOGUE §2.10]',
    refs=[R('N18', 'choba-goshi (text)'), R('i13_echigoya_1768', 'counter areas of a big shop (1768)', True)],
    dimensions={'height_m': D('0.45-0.55', None, 'museum pieces; low enough to see over when seated'), 'panels_m': D('3 folds of 0.60-0.90', None, 'typical')},
    materials=[M('lattice', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: tatami, three sides round the zukue'], variants=[V('_3', 'three folds'), V('_2', 'two folds'), V('_knocked', 'knocked flat (abandoned)')],
    loot_surface='none', abandoned_state='one fold knocked flat', wave=1, pilot=['mise'], blocks_path='low (0.5): walkable around; keep it out of the door-to-door band', lod_budget='small prop <=300 faces')

add(SHOP, id='jp_f_choba_set', name='Account clutter: ledgers (daifukucho), abacus, coin box (zenibako), scales, inkstone box',
    what='The small things on and around the counting desk.',
    importance='filler', tiers=[2, 3], priority='P1', room_tags=['shop', 'office', 'guard'],
    period_evidence='Ledgers 57 + ~61 shops, scales 33, abacus 10 + shops, inkstone 29 [BL §5.6]; coin box with a lock, coin tally board [N18]',
    refs=[R('N18', 'merchant-house tools (text)'), R('N20', 'BL §5.6 (text)')],
    dimensions={'ledger_m': D('0.24 x 0.17 x 0.03', None, 'typical'), 'coinbox_m': D('0.40 x 0.30 x 0.25', None, 'typical'), 'steelyard_m': D('0.60 beam', None, 'typical')},
    materials=[M('wood', 'jp_m_wood_interior', 'timber_interior'), M('paper', 'jp_m_paper_shoji', 'washi_shoji'), M('iron', 'jp_m_metal_iron', 'iron_black')],
    connectors=['proxy_base: on the zukue or the floor beside it'], variants=[V('_desk', 'on the desk'), V('_scattered', 'scattered on the mat')],
    loot_surface='none (clutter)', abandoned_state='coin box open and empty, ledgers scattered', wave=2, pilot=['mise'], blocks_path='', lod_budget='small prop <=300 faces')

add(SHOP, id='jp_f_misedana', name='Stepped goods stand (misedana / hinadan) for shop display',
    what='A low stepped board stand on the display strip that shows goods to the street; the generic display for the shop sets.',
    importance='standard', tiers=[2, 3], priority='P1', room_tags=['shop'],
    period_evidence='Goods displayed on the raised floor at the shop front in 1690 [x33]; shelves of goods in 1768 [i13]; raised display floor is the main shop rule [KEEP_TRADES A]',
    refs=[R('x33_jinrin_bookseller_1690', 'goods laid out and stacked at the raised shop front, 1690', True), R('i13_echigoya_1768', 'goods on shelves and floor (1768)', True)],
    dimensions={'size_m': D('1.82 or 0.91 wide x 0.60 deep x 0.45 high, 2-3 steps', None, 'reason: grid; low so the shop can be seen from the street'), 'step_m': D('0.15 rise, 0.20 tread', None, 'reason')},
    materials=[M('boards', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: on the jp_p_fit_mise_floor strip, parallel to the street'], variants=[V('_1ken', '1.82 wide'), V('_half', '0.91 wide'), V('_toppled', 'toppled forward (abandoned)')],
    loot_surface='each step: 1 point per 0.9 m (range 0.15)', abandoned_state='goods swept off, stand toppled or half empty', wave=1, pilot=['mise'], blocks_path='only on the display strip, never in the door band', lod_budget='small prop <=300 faces')

add(SHOP, id='jp_f_goods_general', name='General-goods dressing set: cloth bolts, paper bundles, wrapped packages, straw sandals, small boxes',
    what='The goods of the "general" shop set (the pilot\'s shop:general): stacked on the stand and floor. Dressing only; loot lies on and around it.',
    importance='filler', tiers=[2, 3], priority='P1', room_tags=['shop'],
    period_evidence='General goods shop in the KEEP dressing sets [KEEP_TRADES A]; paper in 51 entries, straw sandals in 24 [BL §5.7-5.8]; goods at the 1690 shop front [x33]',
    refs=[R('x33_jinrin_bookseller_1690', 'stacked goods at a shop front, 1690', True), R('i13_echigoya_1768', 'cloth goods (1768)', True)],
    dimensions={'bolt_m': D('0.36 x 0.10 x 0.10 (one tan of cloth rolled)', None, 'typical tan bolt'), 'bundle_m': D('0.30 x 0.25 x 0.10 paper', None, 'typical'), 'sandals_m': D('0.24 long pairs tied in strings', None, 'typical')},
    materials=[M('cloth', 'jp_m_textile_cotton_indigo', 'aizome_kon'), M('paper wrap', 'jp_m_paper_shoji', 'washi_shoji'), M('straw', 'jp_m_straw_mushiro', 'thatch_new')],
    connectors=['proxy_base: on the misedana or the strip'], variants=[V('_stacked', 'neat stacks'), V('_swept', 'swept off onto the floor (abandoned)')],
    loot_surface='none (dressing)', abandoned_state='swept off, bolts unrolled across the strip', wave=1, pilot=['mise'], blocks_path='', lod_budget='small prop <=300 faces (per cluster)')

add(REL, id='jp_f_butsudan', name='Household Buddhist cabinet (butsudan) or Buddhist shelf',
    what='A small closed cabinet with the family memorial tablets; T2-3 living rooms, a shelf in poorer homes.',
    importance='standard', tiers=[2, 3], priority='P2', room_tags=['living', 'zashiki', 'daidokoro'],
    period_evidence='Butsudan in 34 entries (19 homes) [BL §5.5]; small butsudan in the Kitamura-type set [BL §3]',
    refs=[R('i09_edo_nagaya_hibachi', 'tenement room with a butsudan and god shelf (c.1840 reconstruction)'), R('N20', 'BL §5.5 (text)')],
    dimensions={'size_m': D('0.50 x 0.40 x 0.80 on a low stand or shelf', None, 'typical household size')},
    materials=[M('cabinet', 'jp_m_lacquer_black', 'sumi_black'), M('plain (T2)', 'jp_m_wood_interior', 'timber_interior')],
    connectors=['proxy_base: floor or a shelf in a room corner'], variants=[V('_closed', 'doors shut'), V('_open', 'doors open, tablets inside')],
    loot_surface='none (respect: nothing spawns on it)', abandoned_state='undisturbed, dusty, doors shut (respectful; decision 12)', wave=2, pilot=[], blocks_path='', lod_budget='small prop <=300 faces')

add(FARM, id='jp_f_mino_pegs', name='Wall pegs with straw raincoat (mino), hat (kasa) and tools (hoe, sickle)',
    what='The rural wall: rain gear and tools hung on pegs by the doma door.',
    importance='filler', tiers=[1, 2], priority='P1', room_tags=['doma', 'stable', 'workshop', 'storage'], region='rural',
    period_evidence='Mino and kasa on pegs in the Kitamura-type set; mino in 18, hats in 12, hoe/sickle in the farm set [BL §3, §5.7]',
    refs=[R('N20', 'BL §3/§5.7 (text)'), R('i05_tsunashima_kamado', 'farmhouse doma walls', True)],
    dimensions={'board_m': D('0.91 peg board at 1.60', None, 'reason: grid; above hip height'), 'mino_m': D('0.90 long', None, 'typical')},
    materials=[M('straw', 'jp_m_straw_mushiro', 'thatch_new'), M('pegs, handles', 'jp_m_wood_weathered', 'timber_weathered'), M('blades', 'jp_m_metal_iron', 'iron_black')],
    connectors=['proxy_base: wall-mounted; footprint 0.15 deep'], variants=[V('_rain', 'mino + kasa'), V('_tools', 'hoe, sickle, rope coil')],
    loot_surface='none', abandoned_state='one peg empty, the hat on the floor', wave=2, pilot=[], blocks_path='', lod_budget='small prop <=300 faces')

add(FARM, id='jp_f_manger', name='Manger (kaiba-oke), fodder cutter and straw pile for the stable corner',
    what='Stable dressing inside farmhouses (uchi-umaya) and stable shells.',
    importance='filler', tiers=[1, 2], priority='P2', room_tags=['stable'], region='rural',
    period_evidence='Manger, fodder cutter, trough in 20 entries [BL §5.7]; inside stable of the Kanto farmhouse variant [KEEP_DWELLINGS 6]',
    refs=[R('N20', 'BL §5.7 (text)')], dimensions={'manger_m': D('1.20 x 0.45 x 0.40 trough on legs', None, 'typical'), 'straw_m': D('1.2 x 1.0 x 0.5 pile', None, 'typical')},
    materials=[M('wood', 'jp_m_wood_weathered', 'timber_weathered'), M('straw', 'jp_m_straw_tawara', 'thatch_new')],
    connectors=['proxy_base: stable floor'], variants=[V('_manger', 'manger'), V('_straw', 'straw pile'), V('_cutter', 'fodder cutter')],
    loot_surface='manger bottom: 1 point (range 0.2)', abandoned_state='empty, straw rotted dark', wave=2, pilot=[], blocks_path='', lod_budget='small prop <=300 faces')

add(FARM, id='jp_f_usu', name='Wooden rice mortar and pounder (usu, kine), hand mill (ishi-usu)',
    what='The pounding set on the farm and food-shop doma.',
    importance='filler', tiers=[1, 2, 3], priority='P2', room_tags=['doma', 'workshop'],
    period_evidence='Mortar and pestle / pounder in 22 entries, stone hand mill in 10 [BL §5.1]; one pounding set serves many trades [BL §5.10]',
    refs=[R('N20', 'BL §5.1/§5.10 (text)')], dimensions={'usu_m': D('d 0.50, h 0.55', None, 'typical'), 'kine_m': D('0.90 long', None, 'typical'), 'millstone_m': D('d 0.40 pair, h 0.25', None, 'typical')},
    materials=[M('wood', 'jp_m_wood_interior', 'timber_interior'), M('stone', 'jp_m_stone_cut', 'stone_granite')],
    connectors=['proxy_base: doma floor'], variants=[V('_usu', 'wooden mortar + pounder'), V('_mill', 'stone hand mill')],
    loot_surface='usu top at 0.55: 1 point (range 0.2)', abandoned_state='pounder fallen, dust in the bowl', wave=2, pilot=[], blocks_path='d 0.5: keep out of tori-niwa bands', lod_budget='small prop <=300 faces')

add(ABD, id='jp_f_debris', name='Dead-world floor litter: blown leaves, straw, torn paper, bowl shards, dust patches (decal atlas)',
    what='Flat alpha decals laid on floors and at door sills: the "as it was left" layer. No collision.',
    importance='filler', tiers=[1, 2, 3], priority='P1', room_tags=['doma', 'daidokoro', 'living', 'zashiki', 'sleeping', 'shop', 'office', 'storage', 'workshop', 'engawa', 'corridor', 'guard', 'stable', 'bath', 'toilet'],
    period_evidence='Stephen\'s dead-world rule (PRODUCTION_PLAN standing decisions); autumn season: maple and ginkgo leaves blow in through open doors [KEEP_OUTDOOR]',
    refs=[R('i02_kasuya_kamado', 'dusty doma surface (look reference)', True)],
    dimensions={'decal_m': D('0.5-1.5 patches, 0.002 above the floor', None, 'reason: no z-fighting, no collision'), 'shards_m': D('0.03-0.08 pieces', None, 'typical')},
    materials=[M('atlas', 'jp_m_decal_litter', 'grime_splash')],
    connectors=['proxy_base: on any floor; the decorator scatters 2-5 per room, more at open doors'], variants=[V('_leaves', 'autumn leaves (at doors, engawa)'), V('_straw', 'straw and dust'), V('_paper', 'torn paper and shoji squares'), V('_shards', 'broken bowls under shelves')],
    loot_surface='none (does not subtract from floor loot)', abandoned_state='this IS the abandoned state', wave=1, pilot=['toriniwa', 'mise', 'zashiki', 'kitchen', 'storage'], blocks_path='none (no Geometry)', lod_budget='small prop <=100 faces (quads)')

add(ABD, id='jp_f_fallen_leaf', name='Fallen door leaf: a shoji or fusuma lying on the floor, paper torn',
    what='A sliding leaf off its track, flat on the mats: a cheap strong dead-world signal. Never a working door.',
    importance='filler', tiers=[2, 3], priority='P2', room_tags=['zashiki', 'living', 'sleeping', 'corridor', 'shop'],
    period_evidence='Shoji and fusuma leaves at T2-3 [PLAYBOOK §2.1]', refs=[R('i42_morse_guestroom_hachiishi', 'Morse 1885: shoji leaves of an inn room')],
    dimensions={'leaf_m': D('0.91 x 1.95 x 0.03', 'kit leaf size (D2 head 2.00)')},
    materials=[M('frame', 'jp_m_wood_interior', 'timber_interior'), M('paper', 'jp_m_paper_shoji', 'washi_shoji')],
    connectors=['proxy_base: flat on the floor, never over a door opening'], variants=[V('_shoji', 'shoji'), V('_fusuma', 'fusuma')],
    loot_surface='none', abandoned_state='torn', wave=2, pilot=[], blocks_path='none: no Geometry (visual only)', lod_budget='small prop <=200 faces')

WAVE1_NOTE = 'Wave 1 = what the B4 pilot (machiya_t3_01) and Phase C wave 1 (Kanto/Kinai farmhouses, huts, Edo and Kamigata townhouse units, post-town house, hatago, kura, shed, toilet, roofed well) need first.'

# ================================================================================================ materials
MAT = {
 'jp_m_floor_tatami': dict(status='new', family='floor', palette='tatami_aged', tile=1.82, ppm=512, grain='rush weave along the mat length; UV one texture per mat, turned with the mat', pen='textile_carpet_int (roadway) / wood (fire)',
     wear=('re-faced mat: paler, faint green (rare accent, 1 room in 10)', 'aged gold-brown, worn lanes along paths', 'stained, mildew blooms, frayed rush, one torn corner: the default for abandoned rooms'),
     note='T2-3 only (no tatami in T1, PLAYBOOK §2.1). Mat = one texture (1.76-1.82 x 0.87-0.91 fills the room between post faces). Matte recipe (T12: fresnel 0.01, black env). Replaces straw_mushiro stand-in in the machiya'),
 'jp_m_floor_tatami_heri': dict(status='new', family='floor', palette='tatami_heri', tile=1.0, ppm=512, grain='plain hemp weave along the edge', pen='textile_carpet_int',
     wear=('even black', 'faded to dark grey-brown, frayed edge', 'faded, torn, rush showing'),
     note='The 0.03 edge band (PLAYBOOK §4). Commoners: plain black or dark brown hemp/cotton (N02, N03); a _cha brown tint of the same set gives the second colour. Patterned korai-beri is later/elite (P3)'),
 'jp_m_floor_boards_int': dict(status='new', family='floor', palette='timber_interior', tile=2.0, ppm=512, grain='along the boards, 0.24-0.30 wide, random offsets', pen='wood / wood_planks_int',
     wear=('oiled, wiped sheen (matte recipe, sheen from the texture only)', 'darker traffic lanes, scratches', 'dusty grey film, water rings, raised grain'),
     note='Itajiki of daidokoro, living, shop strips, corridors, engawa, storage. Surviving polished floors sample much darker (Kasuya: 42,25,20, i01); keep timber_interior and let _w1 darken'),
 'jp_m_floor_boards_rough': dict(status='new', family='floor', palette='timber_interior', tile=2.0, ppm=512, grain='adzed, wide uneven boards', pen='wood / wood_planks_int',
     wear=('fresh adze marks', 'worn smooth in lanes', 'split, dirt in the joints'), note='T1 houses, stables, sheds, toilets'),
 'jp_m_floor_takeyuka': dict(status='new', family='floor', palette='bamboo_weathered', tile=1.0, ppm=512, grain='split bamboo slats 0.03-0.04, lashed', pen='wood / wood_planks_int',
     wear=('pale slats', 'grey-beige, darkened lanes', 'split, a few slats missing'), note='Bamboo-slat floor of the poorest huts (KEEP_DWELLINGS 1 floor option); covered with mushiro'),
 'jp_m_ground_doma_earth': dict(status='new', family='ground', palette='doma_earth', tile=2.0, ppm=512, grain='packed earth, straw bits, uneven', pen='dirt / dirt_int',
     wear=('fresh swept', 'trodden lanes, ash near the stove', 'damp patches, leaf litter'), note='T1 doma and all farm doma. Replaces wall_arakabe stand-in'),
 'jp_m_ground_doma_tataki': dict(status='new', family='ground', palette='doma_earth', tile=2.0, ppm=512, grain='hard lime-earth (tataki), faint trowel/tamp marks, fine gravel', pen='dirt / dirt_int',
     wear=('smooth, even', 'mottled, darker lanes', 'cracked, crumbled at the sill'), note='T2-3 town doma and tori-niwa (tataki: earth + slaked lime + bittern, general in the Edo period in Mikawa and western Japan, N16)'),
 'jp_m_ground_ash': dict(status='new', family='ground', palette='ash_grey', tile=1.0, ppm=512, grain='fine ash, raked lines', pen='dirt / dirt_int',
     wear=('raked', 'charcoal bits, ember marks', 'damp crust, fallen soot'), note='Irori ash bed and hibachi ash'),
 'jp_m_wall_shikkui_int': dict(status='new', family='wall', palette='shikkui_white', tile=2.0, ppm=512, grain='none; trowel', pen='dirt',
     wear=('clean lime, mean <=192', 'faint smoke tint near the ceiling', 'hairline cracks, damp stain at the base'), note='OPEN_ISSUES/T6: the interior twin of shikkui; earth/plaster recipe fresnel(0.49,0.14), black env (T12)'),
 'jp_m_ceil_boards': dict(status='new', family='wood', palette='timber_interior', tile=2.0, ppm=512, grain='wide sugi boards, straight grain, laps every 0.30-0.45', pen='wood',
     wear=('pale sugi', 'smoke-darkened toward the walls', 'water stains, one board missing (geometry)'), note='Sao-buchi ceilings (jp_p_fit_ceiling)'),
 'jp_m_wood_interior': dict(status='new', family='wood', palette='timber_interior', tile=2.0, ppm=512, grain='along member', pen='wood',
     wear=('clean planed wood', 'hand-polished edges, grime at hand height', 'dust film, scratches, pale edge wear'), note='Interior joinery and ALL furniture bodies (tansu, desks, shelves, boxes, frames). Interior posts currently use wood_weathered: swap at the next machiya build'),
 'jp_m_bamboo_sooted': dict(status='new', family='bamboo', palette='timber_sooted', tile=1.0, ppm=512, grain='culm with nodes', pen='wood',
     wear=('smoked brown', 'glossy black-brown (susu-dake)', 'crusted soot'), note='Jizai-kagi tubes, sunoko ceilings over hearths'),
 'jp_m_paper_fusuma': dict(status='new', family='paper', palette='gofun_white', tile=1.0, ppm=512, grain='plain paper sheets, faint seams', pen='fabric_thin',
     wear=('plain warm paper', 'yellowed, hand marks by the pulls', 'torn, stained, patched'), note='Commoner fusuma, screens and cupboard doors: PLAIN paper only (karakami barred for townsmen, T48). The fusuma leaf part is for PA1'),
 'jp_m_textile_cotton_indigo': dict(status='new', family='textile', palette='aizome_kon', tile=0.5, ppm=512, grain='cotton weave, faint stripe or kasuri variant', pen='fabric_thin',
     wear=('even indigo', 'faded folds', 'faded, mildew, torn seams'), note='Futon, yogi, zabuton, goods bolts, robes on racks'),
 'jp_m_textile_cotton_plain': dict(status='new', family='textile', palette='kinari_cloth', tile=0.5, ppm=512, grain='coarse cotton/hemp weave', pen='fabric_thin',
     wear=('unbleached', 'grey-yellow', 'stained, mildew'), note='Bedding linings, cloth wraps (furoshiki), kori lining'),
 'jp_m_ceramic_stoneware_dark': dict(status='new', family='ceramic', palette='stoneware_dark', tile=0.5, ppm=512, grain='wheel lines, glaze drips', pen='pottery',
     wear=('glossy iron-brown glaze', 'dust on the shoulders', 'crazed, chipped, dry film'), note='GLOSSY by design (T12): glazed-tile analogue fresnel(1.42,0). Water jars, storage jars, privy jar'),
 'jp_m_ceramic_stoneware_pale': dict(status='new', family='ceramic', palette='stoneware_pale', tile=0.5, ppm=512, grain='wheel lines, ash glaze', pen='pottery',
     wear=('pale ash glaze', 'dust', 'crazed, chipped'), note='GLOSSY (fresnel 1.42,0). Bowls, bottles, round hibachi, lamp dishes. Porcelain (blue-and-white) accents later if wanted'),
 'jp_m_lacquer_black': dict(status='new', family='paint', palette='sumi_black', tile=0.5, ppm=512, grain='none; brush marks', pen='wood',
     wear=('deep black gloss', 'rubbed to red-brown at edges', 'flaking, wood showing'), note='GLOSSY: needs a vanilla analogue (glazed fresnel 1.42,0 proposed). Trays, clothes racks, butsudan, elite boxes. No gold (elite only, PLAYBOOK §8)'),
 'jp_m_straw_tawara': dict(status='new', family='straw', palette='thatch_new', tile=1.0, ppm=512, grain='bound straw bundles, rope bands', pen='hay',
     wear=('golden', 'grey-gold', 'dark, frayed, burst'), note='Rice bales, straw bags, rope, firewood bindings'),
 'jp_m_bamboo_weave': dict(status='new', family='bamboo', palette='bamboo_weathered', tile=0.5, ppm=512, grain='woven strips (twill/hex)', pen='wood',
     wear=('pale', 'grey-beige', 'broken strips'), note='Kori trunks, baskets, zaru'),
 'jp_m_decal_litter': dict(status='new', family='ground', palette='grime_splash', tile=2.0, ppm=512, grain='alpha atlas: autumn leaves, straw, paper scraps, shards, dust patches', pen='(no collision)',
     wear=('light litter', 'normal', 'heavy'), note='Alpha-tested decal like jp_m_wall_grime; mean colour check on the opaque pixels only'),
 # existing, reused as they are
 'jp_m_wall_nakanuri_int': dict(status='existing', family='wall', palette='earth_wall_aged', note='interior clay walls and clay kamado (T6)'),
 'jp_m_wood_sooted': dict(status='existing', family='wood', palette='timber_sooted', note='hearth beams, under-floor boards, levers'),
 'jp_m_wood_weathered': dict(status='existing', family='wood', palette='timber_weathered', note='firewood, farm pegs and tools'),
 'jp_m_metal_iron': dict(status='existing', family='metal', palette='iron_black', note='pots, rims, fittings'),
 'jp_m_stone_cut': dict(status='existing', family='stone', palette='stone_granite', note='kamado base, stone sink, mills'),
 'jp_m_stone_field': dict(status='existing', family='stone', palette='stone_granite', note='kutsunugi stones'),
 'jp_m_stone_river': dict(status='existing', family='stone', palette='stone_lantern', note='pickle-tub stones'),
 'jp_m_paper_shoji': dict(status='existing', family='paper', palette='washi_shoji', note='andon paper, paper goods, charms'),
 'jp_m_straw_mushiro': dict(status='existing', family='straw', palette='thatch_new', note='mushiro mats, enza, mino'),
 'jp_m_bamboo_weathered': dict(status='existing', family='bamboo', palette='bamboo_weathered', note='tub hoops, drain spouts'),
}

SAMPLES = sample_int.run()
REQ_PAL = [
 dict(id='doma_earth', srgb=SAMPLES['doma_earth']['srgb'], method='sampled', tolerance_dE76=14, samples=SAMPLES['doma_earth']['samples'],
      check='WIDE SPREAD: sunlit Kasuya doma %s vs shaded Tsunashima doma %s. Palette note says earth_road darkened 20-30 %% = about (156,143,125); the photo mean is greyer. Re-sample from a third doma before B1 if Stephen wants' % (SAMPLES['doma_earth']['samples'][0]['value'], SAMPLES['doma_earth']['samples'][1]['value']),
      why='Interior earth floors are grey-brown and darker than the road; the machiya uses the arakabe wall clay as a stand-in.'),
 dict(id='stoneware_pale', srgb=SAMPLES['stoneware_brown']['srgb'], method='sampled', tolerance_dE76=14, samples=SAMPLES['stoneware_brown']['samples'],
      check='one museum object (studio light)', why='Pale ash-glazed stoneware of 1700-1750 (The Met 666591) for bowls, bottles, braziers and lamp dishes.'),
 dict(id='stoneware_dark', srgb=[74, 52, 38], method='assumed', tolerance_dE76=12, samples=[],
      check='needs a licensed photo of an Edo-period iron-glazed jar (Tamba / Seto kitchen ware)', why='Iron-brown glazed storage and water jars; no licensed sample found in this pass.'),
 dict(id='ash_grey', srgb=[150, 146, 140], method='assumed', tolerance_dE76=12, samples=[],
      check='sample the ash bed of i04 or i01 at the materials stage (small, lit by fire in i04)', why='Irori ash beds and hibachi ash.'),
]

# ================================================================================================ rooms, tier by tier
ROOMS = [
 ('doma', 'earth (T1 packed earth, T2-3 tataki)', 'Earth wall, board wainscot; posts and the underside of the raised floor (sooted boards); open to the roof in farmhouses',
  'Open to the sooted roof (T1, farm); the loft floor on joists (town)',
  'Kamado, nagashi sink, water jar, shelf; kutsunugi stone at each raised edge; kamidana over the kitchen in shops',
  '**T1:** a dark earth floor, a rough clay stove on stones, a bucket and tub, firewood, a water jar with a dipper, straw sandals and a straw mat thrown over a bench; mino and a hat on pegs by the door. **T2:** the same with a plank shelf of bowls, a pickle tub with its stone, jars. **T3 (tori-niwa):** hard grey tataki, a two-mouth plastered stove, a wooden or stone sink, a long passage kept clear to the back door.',
  'Floor loot along the walls and by the stove; the stove top, the shelf and the jar lid carry small raised points'),
 ('daidokoro', 'boards (itajiki), mushiro over them in T1', 'Earth walls, the big sooted beams overhead', 'None: smoke-blackened rafters and thatch; bamboo slats (sunoko) over the hearth in T2',
  'Irori with the fish-lever hook; hidana rack in mountain houses; kamidana; a low shelf',
  '**T1:** the living room of a poor house: boards or earth under straw mats, the irori in the middle with a pot on the hook, a low shelf, a tub. **T2:** a bigger irori, the kamidana, a small butsudan, box trays stacked, the andon. **T3 (headman, samurai kitchen):** a large board room, a row of jars, a cupboard; tansu and hibachi move in.',
  'Floor points round the hearth (not in the ash), the shelf boards'),
 ('living', 'T1-2 boards (+ mushiro); T3 tatami', 'Earth walls (nakanuri_int); shoji to the veranda or street in T2-3', 'Open (T1), loft joists (townhouse), sao-buchi (T3)',
  'Kamidana or butsudan corner; nothing built-in otherwise',
  '**T1 (tenement 4.5-6 mats):** one room for everything: a low screen with folded bedding behind it, a wicker trunk, an andon, a small hibachi, a box of the tenant\'s trade tools. **T2:** add a small tansu, a Buddhist shelf, a clothes rack. **T3:** tatami, tansu, byobu, hibachi and tobacco tray.',
  'Floor points in the room, 1-2 raised on chest or trunk tops'),
 ('zashiki', 'tatami (T2 best room; T3), plain black/brown heri', 'Earth walls (T2), smoother clay or plaster (T3); fusuma and shoji, plain paper; no nageshi for commoners (rule 11)',
  'Sao-buchi board ceiling (T2-3); loft joists in townhouses', 'Tokonoma ONLY in headman, samurai, honjin and great-merchant shells; chigaidana samurai/honjin only; no oshiire in 1730 (decisions 7-8)',
  '**T2 (farmhouse best room):** a few mats, an andon, a box of lacquered festival trays, maybe a hanging scroll on the wall. **T3 (merchant zashiki, the pilot):** 9 mats, a tansu, a hibachi, an andon, bedding folded in the corner or still laid out, a box or two. **Samurai / honjin:** the tokonoma with a fallen scroll, a sword rack, a writing desk.',
  'Floor points on the mats; the tansu top, the bedding and the chest lids carry raised points'),
 ('sleeping', 'T1 boards + straw bedding; T2-3 tatami', 'Closed earth walls (the nando was the dark inner room)', 'As the living room',
  'None (no oshiire; bedding lives here)',
  '**T1 (nando):** straw bedding on boards, a paper quilt, a wicker trunk. **T2:** folded futon and yogi, a nagamochi, a clothes rack. **T3:** tansu, bedding laid out as left, an ariake lamp, a mirror stand (later).',
  'Loot on the bedding (like vanilla beds) and on chest lids'),
 ('shop', 'tatami (T3) or boards (T2), with a board display strip at the street edge', 'Street side: lattice or open shutters; inner side fusuma/shoji', 'Loft joists', 'Mise-floor strip; kamidana with Ebisu; the choba corner',
  '**T2 (post town, omote-nagaya):** boards, goods on a low stand, a tobacco tray, a desk. **T3 (the pilot, shop:general):** the display strip with stepped stands of cloth, paper and sandals; the chōba corner at the back with its low lattice, desk, ledgers, abacus and coin box; a hibachi; shelves of stock on the side wall. The 22 shop sets swap the goods.',
  'The stand steps and shelves carry raised points; the strip and the mats carry floor points'),
 ('office', 'tatami', 'As zashiki', 'Sao-buchi', 'None; inns: the chōba at the entrance',
  '**T2-3:** the chōba of an inn or a toiya-ba: desk, register, abacus, lattice screen, lamp, tobacco tray; official compounds add document boxes and a seal box.',
  'Desk top and document boxes; floor'),
 ('workshop', 'earth or boards by trade', 'Earth or boards; tools on the walls', 'Open to the roof', 'Kamidana (almost every workshop); trade fixtures come with their shell',
  'Trade kits (smithy, cooper, weaver...) are built with their shells (PRODUCTION_PLAN: specialty props with the shell). The core kit here gives the shelves, tubs, boxes, baskets and mats they all share.',
  'Bench tops and shelves; floor'),
 ('storage', 'boards (monooki, kura)', 'Earth or thick plaster (kura: shikkui_int)', 'Open joists / the kura loft', 'None',
  '**All tiers:** shelving along the walls, straw bales, chests, boxes, jars and casks; in kura, long chests and stacked boxes. The best loot room in vanilla terms: many raised surfaces.',
  'Shelf boards, chest lids, bale stacks; floor between'),
 ('loft', 'boards', '-', 'Roof underside', 'None', 'SEALED by default (G0-4): no access, no loot, no furniture. Kura lofts reached by ladder get the storage set.', 'None when sealed'),
 ('stable', 'earth + straw', 'Boards, pegs', 'Open', 'None', 'Manger, straw pile, fodder cutter, harness and pack saddle on pegs (wave 2).', 'Floor; the manger'),
 ('bath', 'boards over stone', 'Boards', 'Open, vented', 'The tub is a trade/shell prop (P2)', 'Bath huts and inns: a wooden tub, a bucket, a stool (later with those shells).', 'Floor'),
 ('toilet', 'boards with a slot', 'Boards', 'Open', 'jp_p_fit_setchin', 'A slot over a jar, straw on the floor.', '1 floor point'),
 ('engawa / corridor', 'boards', '-', 'Eave soffit / boards', 'Amado and tobukuro (exterior list)', 'Clear by rule (D5 >=1.00 m): only litter and a fallen leaf; leaves blown in.', 'Floor points only'),
 ('guard', 'earth or boards', 'Boards', 'Open', 'Small irori in huts', 'Lamp, desk, clapper, weapon rack (civic props later), tobacco tray, hibachi.', 'Desk top; floor'),
]

# ================================================================================================ decisions
DECISIONS = [
 ('Tatami module', 'The kit is **Inakama (column-based)**: mats fill the room between post faces on the 1.82 m grid, so a mat is about 1.78 x 0.87 m (Edoma 1.76 x 0.88 [T01]). Keep it for Kamigata buildings too (no Kyoma 1.91 x 0.955 mats); only the texture differs. **Recommend: keep.**'),
 ('Tatami layout per room', 'Shugi layout (no four corners meeting) in every tatami room, as the machiya solver already does; 4.5-mat rooms get the half mat in the centre. Tatami only in T2 best rooms and T3 living rooms; T1 gets boards + straw mats. **Recommend: yes.**'),
 ('Heri colour', 'Plain black or dark-brown hemp edges for every commoner and most samurai rooms [N02, N03]; patterned korai-beri only for later elite/temple rooms (P3). **Recommend: black default, brown as the second tint.**'),
 ('Clutter vs walking paths', 'Hard rule for the decorator: a 1.00 m clear band from every door to every other door and to the room centre (D1/D5); no collision prop within 0.4 m of a door\'s clear opening; collision furniture covers at most 25 % of a living room\'s floor, 40 % of storage; flat litter, mats, laid bedding and fallen leaves have NO Geometry and may lie anywhere except sills. **Recommend: yes; checked by C6 + a new clear-band check.**'),
 ('Furniture density and loot surfaces', 'Japanese rooms were sparse, but in vanilla about two thirds of the loot points of a house are raised and about half sit on proxied furniture (Q5). Give every room at least ONE raised surface (shelf, chest lid, tansu top, stand) and 2-4 collision props, plus clutter. **Recommend: yes; the pilot gets 5-7 props per room.**'),
 ('How the shop front room displays goods', 'A board strip (0.455 behind a lattice, 0.91 behind an open front) along the street edge of the raised floor, with low stepped stands of goods; the choba corner at the back with its low lattice, desk and account clutter; stock shelves on a side wall. Goods are dressing; loot lies on the stand steps and strip. For the pilot this means regenerating the mise floor with a board strip. **Recommend: yes.**'),
 ('Tokonoma', 'Commoners were forbidden it in 1730; headmen, samurai, honjin and some great merchants had it; it spreads after the mid-18th c. [N04, N05]. **Recommend: none in ordinary townhouses and farmhouses (the pilot stays plain); a 1-ken tokonoma in headman, samurai, honjin and great-merchant best rooms.** It is a shell recess, so it is decided per shell.'),
 ('Oshiire (bedding closet)', 'Enters plans mid-to-late Edo; general only after Meiji [N09]. **Recommend: no oshiire in P1 shells; bedding stacked in the room or nando (optionally behind a low screen). Allow it only in inns/samurai houses if you want the loot shelf.**'),
 ('Cushions', 'Cotton zabuton reach commoners after Meiji [N07]. **Recommend: round straw enza everywhere; zabuton only in T3 shops, inns and samurai rooms.**'),
 ('Kettle', 'The name tetsubin first appears in 1816 and the kettle develops in the Tenpo era [N15]: late. **Recommend: pots (kama/nabe) on the hook and stove, and the spouted kettle (yakan, since the Kamakura era) - no tetsubin.** This settles BUILDING_LIST contradiction 1.'),
 ('How "abandoned" it looks', '"As left", lightly disturbed: in each room one or two signs (a drawer out, a tipped lamp, a burst bale, a meal left out), dust and litter decals, leaves at open doors. No blood, bodies or smashed shrines. **Recommend: this moderate level; one room in five more heavily ransacked.**'),
 ('Shrines inside the house', 'Kamidana and butsudan stay undisturbed and carry no loot. **Recommend: yes (respectful).**'),
 ('Doma colour', 'New palette entry doma_earth from two photos that disagree (sunlit vs shade). **Recommend: accept the sampled mean for B1 and judge it in game; or re-sample first.**'),
 ('Lamps', 'Andon ship unlit (no light points) for the dead world. **Recommend: yes; lit lamps later if ever wanted.**'),
]

TEXT = [
 ('N01', 'https://ja.wikipedia.org/wiki/畳', 'Tatami spread among commoners in the mid-Edo period, rural areas later; Kyoma 1.91x0.955, Chukyoma 1.82x0.91, Edoma/Inakama 1.76x0.88; column-centre (east) vs tatami-apportioned (west) planning'),
 ('N02', 'https://ja.wikipedia.org/wiki/畳縁', 'Heri status ladder: ungen-beri (emperor, deities), dai-mon / sho-mon korai-beri (princes, ministers, court nobles); rules loosened over time; edges of narrow dyed hemp cloth'),
 ('N03', 'https://sawahata-tatami.jp/?p=3502', 'Tatami-maker histories (low-grade web source, via search summary): commoner heri plain black or tea-brown hemp/cotton; tatami craftsmen established and townspeople using tatami mid-to-late Edo'),
 ('N04', 'https://kotobank.jp/word/%E5%BA%8A%E3%81%AE%E9%96%93-105027', 'Tokonoma: commoners forbidden in the Edo period; from the mid-18th c. many houses installed one in the sitting room; upper farmers and townsmen had them, general only after Meiji; about 1 ken wide, ~3 shaku deep (World Encyclopedia; Yamakawa dictionary)'),
 ('N05', 'https://ja.wikipedia.org/wiki/床の間', 'Tokonoma built in headman (shoya) houses to receive lords and intendants; general in urban guest rooms after Meiji'),
 ('N06', 'https://ja.wikipedia.org/wiki/箪笥', 'Tansu appear in Osaka in the Kanbun era (1661-73), spread from the Shotoku era (1711-16); costly, reaching poor commoners only in late Edo; clothes kept in kori, nagamochi and chests before (via search summary)'),
 ('N07', 'https://crd.ndl.go.jp/GENERAL/servlet/detail.reference?id=1000106499', 'NDL reference record: zabuton developed from the shitone and spread gradually in the Edo period; common among ordinary people from Meiji (Nipponica, Heibonsha)'),
 ('N08', 'https://www.arc.ritsumei.ac.jp/artwiki/index.php/%E6%B1%9F%E6%88%B8%E6%99%82%E4%BB%A3%E3%81%AE%E5%AF%9D%E5%85%B7%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6', 'Edo bedding (via search summary): straw bundles for commoners early in the period; yogi (sleeved quilt) and futon; Kamigata used quilts from Genroku, Edo kept the yogi; cotton costly'),
 ('N09', 'https://ja.wikipedia.org/wiki/押入れ', 'Oshiire enter house plans mid-to-late Edo and become general after Meiji; bedding was stored in the nando before (via search summary)'),
 ('N10', 'https://cleanup.jp/life/edo/06.shtml', 'Edo tenement kitchen (Tenpo-era reconstruction): ~2 m wide doma kitchen, standing and squatting stoves, shallow sink without a drain hole, water jar and ladle'),
 ('N11', 'https://kotobank.jp/word/%E7%AB%88-466236', 'Kamado / kudo / hettsui: clay stoves built by plasterers; Edo stoves with the fire mouth to the room and the back to the outer wall; two-mouth stoves in tenements (with s-kent.jp column, via search summary)'),
 ('N12', 'https://ja.wikipedia.org/wiki/囲炉裏', 'Irori: square pit in the floor filled with ash; robuchi frame; jizai-kagi with a (fish-shaped) yokogi; hidana drying rack; seating order (yokoza)'),
 ('N13', 'https://ja.wikipedia.org/wiki/行灯', 'Andon: spread in the Edo period; paper on a wood/bamboo frame; oil dish, rush or cotton wick; types oki, ariake, enshu, kake, tsuji'),
 ('N14', 'https://ja.wikipedia.org/wiki/神棚', 'Kamidana: devised and spread by the Ise oshi; by mid-Edo most households kept one; ~90 % of households received Ise charms by late Edo (via search summary)'),
 ('N15', 'https://ja.wikipedia.org/wiki/鉄瓶', 'Tetsubin: the name first recorded 1816, derived from the tea kettle around the Tenpo era; spouted yakan since the Kamakura era (via search summary)'),
 ('N16', 'https://ja.wikipedia.org/wiki/三和土', 'Tataki: earth with slaked lime and bittern, tamped; generalized as the doma floor in the Edo period in Mikawa and western Japan (via search summary)'),
 ('N17', 'https://suumo.jp/yougo/s/saobuchitenjou/', 'Sao-buchi ceiling: boards on parallel battens; ceilings were first for high-status buildings, later in houses (via search summary)'),
 ('N18', 'https://www.city.adachi.tokyo.jp/hakubutsukan/chiikibunka/hakubutsukan/shiryo-shoka.html', 'Adachi city museum, merchant-house tools: shop = doma + choba; choba-goshi a foldable low lattice; choba desk, account books, abacus, coin tally (zeni-masu), locked coin box'),
 ('N19', 'https://ja.wikipedia.org/wiki/長持', 'Nagamochi: about 1.74 m long, 0.75 wide and high, carried on a pole by two; spread from samurai to commoners as cotton bedding grew (via search summary)'),
 ('N20', 'research/buildings/BUILDING_LIST.md', 'This project: §3 room lists per building type and §5 shared-core-kit counts (682 entries)'),
]

IMG_SUPPORTS = {
 'i01_kasuya_irori': 'Former Kasuya house (Itabashi, Tokyo farmhouse): irori in a dark polished board floor, chest, kettle',
 'i02_kasuya_kamado': 'Former Kasuya house: large clay kamado on the earth doma (doma colour sample, sunlit)',
 'i03_tenmyo_irori': 'Tenmyo farmhouse (Edo-Tokyo Open Air Museum): irori, jizai-kagi, board and tatami rooms',
 'i04_tsunashima_irori': 'Tsunashima farmhouse (Edo-Tokyo Open Air Museum): irori ash bed and frame, kettle, firewood',
 'i05_tsunashima_kamado': 'Tsunashima farmhouse: two rough clay kamado on stones, tubs',
 'i06_tsunashima_doma': 'Tsunashima farmhouse: doma, kamado row, straw mat over a bench (doma colour sample, shade)',
 'i07_edo_nagaya_room': 'Fukagawa Edo Museum tenement reconstruction (Tenpo era): room dressing, chests, lamp, tubs',
 'i08_edo_nagaya_kitchen': 'Fukagawa Edo Museum tenement kitchen: stove, sink, water jar',
 'i09_edo_nagaya_hibachi': 'Fukagawa Edo Museum tenement room: kamidana, butsudan, box hibachi',
 'i10_hearth_boards': 'Irori frame in a board floor',
 'i11_kamado_plastered': 'White plastered kamado beside a raised floor',
 'i12_tsubaki_honjin': 'Tsubaki honjin, Koriyama-juku (rebuilt 1718): formal tatami rooms',
 'i13_echigoya_1768': 'Utagawa Toyoharu, 1768: interior of the Mitsui Echigoya shop, Suruga-cho (18 years past the window)',
 'i15_moronobu_1685_p5': 'Hishikawa Moronobu, Wakoku shoshoku ezukushi (1685), The Met: roofer and a lattice shop front',
 'i16_moronobu_1685_p6': 'Moronobu 1685: lacquerer with a spouted kettle; sword polisher with tubs and a box',
 'i17_moronobu_1685_p7': 'Moronobu 1685: weaver at a loom on a board floor; dyer treading cloth in tubs',
 'i18_moronobu_1685_p9': 'Moronobu 1685: woman at buckets and a large jar on a board floor; pole carrier with vessels',
 'i19_moronobu_tub': 'Moronobu (before 1694): large shallow round tub',
 'i20_hachioji_kamado': 'House of a Hachioji guard leader (Edo-Tokyo Open Air Museum): two-mouth kamado, iron pot, wooden lid',
 'i21_jizai_kettle': 'Boso-no-mura: kettle on a jizai-kagi over an irori',
 'i22_kamado_firewood': 'Clay kamado with split firewood stacked beside it',
 'i23_kendan_tokonoma': 'Kendan yashiki: tokonoma with toko-bashira and scroll',
 'i24_hida_farmhouse': 'Hida Folk Village: farmhouse interior, raised board floor over the doma',
 'i30_morse_kitchen_farmhouse': 'Morse 1885 fig. 167: kitchen in an old farmhouse, Kabutoyama',
 'i31_morse_kitchen_range': 'Morse 1885 fig. 168: the usual kitchen range',
 'i32_morse_city_kitchen': 'Morse 1885 fig. 170: kitchen in a city house, sink and racks',
 'i33_morse_jizai': 'Morse 1885 fig. 173: ji-zai in a peasant hut',
 'i34_morse_fireplace_country': 'Morse 1885 fig. 174: fireplace (irori) in a country house',
 'i35_morse_kitchen_closet': 'Morse 1885 fig. 177: kitchen closet, drawers, cupboard and stairs combined',
 'i36_morse_hibachi': 'Morse 1885 fig. 197: common hibachi',
 'i37_morse_hibachi_wood': 'Morse 1885 fig. 198: wooden hibachi',
 'i38_morse_tabakobon': 'Morse 1885 fig. 201: tabako-bon',
 'i39_morse_andon': 'Morse 1885 fig. 206: andon lamp',
 'i40_morse_andon2': 'Morse 1885 fig. 207: andon lamp',
 'i41_morse_ceiling': 'Morse 1885 fig. 19: section of an ordinary ceiling',
 'i42_morse_guestroom_hachiishi': 'Morse 1885 fig. 96: inn guest room at Hachi-ishi',
 'i43_morse_guestroom': 'Morse 1885 fig. 119: guest room with tokonoma and shelves',
 'i44_morse_country_guestroom': 'Morse 1885 fig. 128: guest room of a country house',
 'i50_met_tokkuri_stoneware': 'The Met 666591: stoneware sake bottle, ca. 1700-1750 (palette sample stoneware_pale)',
 'i51_met_tokkuri_porcelain': 'The Met 50328: porcelain sake bottle, early 18th c.',
}


# ================================================================================================ Q5
def q5_summary():
    lods = json.load(open(os.path.join(ROOT, 'data', 'research_int', 'q5_lods.json'), encoding='utf-8'))
    loot = json.load(open(os.path.join(ROOT, 'data', 'research_int', 'q5_loot.json'), encoding='utf-8'))
    houses = []
    for f in lods:
        row = {'file': f['file'].replace('\\', '/').split('/')[-1]}
        for L in f['lods']:
            if L['n_furniture_records'] or L['lod'] in ('Res 1', 'Res 2', 'Geometry', 'Memory', 'Roadway', 'ViewGeometry', 'FireGeometry'):
                row[L['lod']] = L['n_furniture_records']
        others = [L['lod'] for L in f['lods'] if L['n_furniture_records'] and L['lod'] not in ('Res 1', 'Geometry', 'ViewGeometry', 'FireGeometry')]
        row['furniture_in_other_lods'] = others
        houses.append(row)
    tot = {'raised': 0, 'raised_on_furniture': 0, 'floor': 0, 'floor_in_footprint': 0, 'range_furniture': [], 'range_floor': []}
    per = []
    for c in loot:
        if not c['points']:
            continue
        r = {'class': c['class'], 'points': len(c['points']), 'raised': 0, 'raised_on_furniture': 0, 'floor': 0}
        for p in c['points']:
            if p['above_floor_m'] > 0.05:
                r['raised'] += 1; tot['raised'] += 1
                if p['furniture']:
                    r['raised_on_furniture'] += 1; tot['raised_on_furniture'] += 1
                    tot['range_furniture'].append(p['range'])
            else:
                r['floor'] += 1; tot['floor'] += 1
                tot['range_floor'].append(p['range'])
                if p['furniture']:
                    tot['floor_in_footprint'] += 1
        per.append(r)
    tot['range_furniture'] = [min(tot['range_furniture']), max(tot['range_furniture'])]
    tot['range_floor'] = [min(tot['range_floor']), max(tot['range_floor'])]
    heights = {}
    for c in loot:
        for p in c['points']:
            if p['furniture'] and p['above_floor_m'] > 0.05:
                heights.setdefault(p['furniture'][0], set()).add(p['above_floor_m'])
    return {'houses': houses, 'loot_classes': per, 'loot_totals': tot,
            'surface_heights_by_furniture': {k: sorted(v) for k, v in sorted(heights.items())},
            'furniture_p3d_lods': 'case_d: Res1-2, Geometry, View, Fire; kitchen_table_a and postel_manz_kov: + Roadway; almara_open: Res1-3, Geometry, View, Fire; no Memory LOD; vanilla LOD0 faces 72-586 (q5_lods.py on P:/DZ/structures/furniture)',
            'config': 'P:/DZ/structures/furniture/config.cpp: every furniture p3d also has a class StaticObj_Furniture_<name> : HouseNoDestruct, scope 1',
            'tools': 'research/interior/tools/q5_scan.py, q5_lods.py, q5_loot.py; raw output data/research_int/q5_lods.json, q5_loot.json'}


# ================================================================================================ schema validation
def validate(inst, schema, path='$'):
    errs = []
    t = schema.get('type')
    tmap = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool}
    if t and t in tmap and not isinstance(inst, tmap[t]):
        return ['%s: expected %s' % (path, t)]
    if 'enum' in schema and inst not in schema['enum']:
        errs.append('%s: %r not in enum' % (path, inst))
    if 'pattern' in schema and isinstance(inst, str) and not re.search(schema['pattern'], inst):
        errs.append('%s: %r does not match pattern' % (path, inst))
    if isinstance(inst, dict):
        for r in schema.get('required', []):
            if r not in inst:
                errs.append('%s: missing %s' % (path, r))
        for k, v in inst.items():
            if k in schema.get('properties', {}):
                errs += validate(v, schema['properties'][k], path + '.' + k)
            elif isinstance(schema.get('additionalProperties'), dict):
                errs += validate(v, schema['additionalProperties'], path + '.' + k)
    if isinstance(inst, list):
        if len(inst) < schema.get('minItems', 0):
            errs.append('%s: fewer than %d items' % (path, schema['minItems']))
        if 'items' in schema:
            for i, v in enumerate(inst):
                errs += validate(v, schema['items'], '%s[%d]' % (path, i))
    return errs


# ================================================================================================ build
def main():
    meta = json.load(open(os.path.join(ROOT, 'data', 'research_int', 'meta.json'), encoding='utf-8'))
    pb = json.load(open(os.path.join(ROOT, 'playbook', 'refs_index.json'), encoding='utf-8'))
    ext = json.load(open(os.path.join(ROOT, 'research', 'exterior', 'refs_index.json'), encoding='utf-8'))
    known = {i['id'] for i in pb['images']} | {t['id'] for t in pb['text']} | {i['id'] for i in ext['images']} | {t['id'] for t in ext['text']}
    img_ids = set(IMG_SUPPORTS)
    txt_ids = {t[0] for t in TEXT}
    errs = []
    for rid in IMG_SUPPORTS:
        if rid not in meta: errs.append('image %s not downloaded (meta.json)' % rid)
    for rid in meta:
        if rid not in IMG_SUPPORTS: errs.append('downloaded image %s has no IMG_SUPPORTS line' % rid)
    all_ids = known | img_ids | txt_ids
    for e in E:
        for r in e['refs']:
            if r['id'] not in all_ids: errs.append('unknown ref %s in %s' % (r['id'], e['id']))
        for tok in re.findall(r'\[([^\]]+)\]', e.get('period_evidence', '')):
            for t in re.split(r'[,;]\s*', tok):
                t = t.strip()
                if re.match(r'^(N\d\d|E\d\d|T\d\d)$', t) and t not in all_ids: errs.append('unknown evidence %s in %s' % (t, e['id']))
                if re.match(r'^(i\d\d|x\d\d)$', t) and not any(i.startswith(t + '_') for i in all_ids): errs.append('unknown image %s in %s' % (t, e['id']))
        for m in e['materials']:
            if m['material'] not in MAT: errs.append('material %s missing (%s)' % (m['material'], e['id']))
            elif MAT[m['material']]['palette'] != m['palette_id']: errs.append('palette mismatch %s %s' % (m['material'], e['id']))
    if errs: print('\n'.join(errs)); sys.exit(1)

    # reach per entry
    for e in E:
        n_sh, n_rooms, ids = reach(e['room_tags'], e['tiers'])
        e['reach'] = {'shells': n_sh, 'rooms': n_rooms, 'shell_ids': ids, 'shop_sets': SHOP_SETS if 'shop' in e['room_tags'] else 0}

    entries = []
    for e in E:
        d = {k: v for k, v in e.items() if not k.startswith('_')}
        d['stage'] = 'B' if d['id'].startswith('jp_p_') else 'D'
        entries.append(d)
    bl = {'category': 'interiors-dwellings-trades', 'version': 1, 'author': AUTHOR, 'date': DATE, 'stage': 'D',
          'scope_note': 'Interiors of the KEEP shells (dwellings, trade shells and townhouse shop sets; civic shells counted where they share rooms): room-by-tier contents, interior materials, built-in fittings (jp_p_fit_*, merged into shells like kit parts) and the interior core props (jp_f_*, proxies). Trade-specific props (brewery, smithy, kilns, looms) are built with their shells (PRODUCTION_PLAN). Loot tiers ignored. Extra keys per entry: structural (fittings), loot_surface, abandoned_state, wave, pilot, blocks_path, reach.',
          'entries': entries}
    schema = json.load(open(os.path.join(ROOT, 'playbook', 'templates', 'build_list_schema.json'), encoding='utf-8'))
    verr = validate(bl, schema)
    if verr: print('\n'.join(verr)); sys.exit(1)

    used = {}
    for e in E:
        for m in e['materials']:
            used.setdefault(m['material'], set()).add(e['id'])
    pal = json.load(open(os.path.join(ROOT, 'playbook', 'palette.json'), encoding='utf-8'))
    pal_ids = {p['id'] for p in pal['entries']}
    req_ids = {p['id'] for p in REQ_PAL}
    mats = []
    for mid, m in MAT.items():
        if mid not in used: errs.append('material %s unused' % mid)
        if m['palette'] not in pal_ids | req_ids: errs.append('palette %s unknown' % m['palette'])
        row = {'id': mid, 'status': m['status'], 'family': m['family'], 'palette_id': m['palette'],
               'palette_status': 'existing' if m['palette'] in pal_ids else 'REQUESTED (see requested_palette_entries)',
               'note': m['note'], 'used_by': sorted(used.get(mid, []))}
        if m['status'] == 'new':
            row.update({'tile_size_m': m['tile'], 'px_per_m': m['ppm'], 'grain': m['grain'], 'penetration_rvmat': m['pen'],
                        'wear': {'_w0': m['wear'][0], '_w1': m['wear'][1], '_w2': m['wear'][2]}})
        mats.append(row)
    if errs: print('\n'.join(errs)); sys.exit(1)
    new = [m for m in mats if m['status'] == 'new']
    mn = {'version': 1, 'date': DATE, 'author': AUTHOR,
          'note': 'Interior materials for the materials agent (Phase B1): one canonical set per NEW material, 3 wear levels (_w0 clean, _w1 normal, _w2 heavy / abandoned), path JP\\common\\materials\\<family>\\ (PLAYBOOK §9). Finish per PLAYBOOK §15.3 T12: matte = fresnel(0.01,0.01) + black env; earth/plaster = fresnel(0.49,0.14) + black env; glossy only where noted (ceramic, lacquer: glazed analogue fresnel(1.42,0)). Interior faces never use exterior weathering (T6). Status "existing" rows need no work; they are listed so used_by is complete.',
          'counts': {'new_materials': len(new), 'texture_sets': 3 * len(new), 'existing_reused': len(mats) - len(new)},
          'materials': mats, 'requested_palette_entries': REQ_PAL}

    images = []
    for rid in sorted(IMG_SUPPORTS):
        m = dict(meta[rid]); m.pop('bytes', None)
        m['supports'] = IMG_SUPPORTS[rid]
        images.append(m)
    refs_index = {'version': 1, 'category': 'interior (dwellings, trades, shop sets)', 'date': DATE,
                  'note': 'Images local only in data/research_int/refs/ (git-ignored, never shipped). Ids x.., E.. are in research/exterior/refs_index.json; c.., m.., T.. in playbook/refs_index.json. Text is cited, not copied.',
                  'download_policy': 'PD / CC0 / CC BY only (never SA/NC/ND), licence re-checked through the Commons API and the Met API at download; User-Agent "JapanDevResearch/1.0 (DayZ mod research)", no personal information.',
                  'reused_ids': sorted({r['id'] for e in E for r in e['refs']} & known),
                  'images': images, 'text': [{'id': a, 'url': b, 'supports': c} for a, b, c in TEXT]}
    q5 = q5_summary()

    wb = lambda p, s: open(os.path.join(OUT, p), 'wb').write(s.encode('utf-8'))
    wb('build_list.json', json.dumps(bl, ensure_ascii=False, indent=1) + '\n')
    wb('materials_needed.json', json.dumps(mn, ensure_ascii=False, indent=1) + '\n')
    wb('refs_index.json', json.dumps(refs_index, ensure_ascii=False, indent=1) + '\n')
    wb('q5_evidence.json', json.dumps(q5, ensure_ascii=False, indent=1) + '\n')
    wb('CREDITS.md', credits(images))
    wb('BUILD_LIST.md', md(bl, mn, q5))
    w1 = [e['id'] for e in E if e.get('wave') == 1]
    print('entries', len(E), '(fittings %d, props %d)' % (sum(1 for e in E if e['id'].startswith('jp_p_')), sum(1 for e in E if e['id'].startswith('jp_f_'))),
          'wave1', len(w1), 'materials new', len(new), 'images', len(images), 'text', len(TEXT), 'schema OK')


def credits(images):
    L = ['# CREDITS: interior research images (agent PA2, %s)' % DATE, '',
         'Every image downloaded for the interior build list. Stored locally in `data/research_int/refs/` (git-ignored) as',
         'research references only: **never shipped** in a PBO. Licences were re-checked through the Wikimedia Commons API or',
         'The Met Open Access API at download time (PD / CC0 / CC BY only; nothing Share-Alike, Non-Commercial or No-Derivatives).',
         'Requests used the User-Agent `JapanDevResearch/1.0 (DayZ mod research)`. Generated by `tools/gen_build_list.py` from',
         '`data/research_int/meta.json` (written by `tools/fetch_int_refs.py`).', '',
         'CC BY images require attribution if they are ever shown outside this project (for example in a compare sheet that is',
         'published): use the author and licence below.', '',
         '| Id | Title | Author | Licence | Date | Source page |', '|---|---|---|---|---|---|']
    for m in images:
        L.append('| `%s` | %s | %s | %s | %s | %s |' % (m['id'], esc(m['title'][:90]), esc(m.get('author', ''))[:60] or '-', esc(m['licence']), esc(m.get('date', ''))[:30], m['page_url']))
    L += ['', 'Not downloaded (read only, cited as text ids N01-N20 in `refs_index.json`): Wikipedia (ja), Kotobank, the NDL',
          'reference database, the Adachi city museum, and other web pages. Nothing was copied from them.']
    return '\n'.join(L) + '\n'


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


def md(bl, mn, q5):
    L = []
    A = L.append
    A('# BUILD LIST: interiors (rooms, materials, built-in fittings, core props), v1\n')
    A('**Stage:** B1 (materials), B2 (fittings as kit parts), B3 (props), then D (the decorator furnishes by room tag)\n')
    A('**Author and date:** %s, %s. Gate **G1** (Stephen, about 10 minutes).\n' % (AUTHOR, DATE))
    A('**Scope:** the rooms of the KEEP shells (dwellings, trade shells, the 22 townhouse shop sets), tiers 1-3. Trade-specific props (brewery, smithy, kilns, looms) are built with their shells (PRODUCTION_PLAN). Loot tiers are ignored. Every prop is dressing: loot lies OUT on floors and surfaces; no container.\n')
    A('**Files:** `build_list.json` (validates against `playbook/templates/build_list_schema.json`), `materials_needed.json`, `refs_index.json` (images i01-i51 and text N01-N20), `q5_evidence.json`, `CREDITS.md`. All from `tools/gen_build_list.py`: edit the data there and rerun. Images: `data/research_int/refs/`.\n')
    A('**Reading:** `[N04]`, `[T01]`, `i03`, `x33` are sources. `(assumed)` = no source gives the value. D1-D10 = PLAYBOOK §5. "Reach" = how many kept shells / rooms can use the item (counted from the shell-room table in the script).\n')

    A('\n## Decisions for Stephen (one line each, with my recommendation)\n')
    for i, (k, v) in enumerate(DECISIONS, 1):
        A('%d. **%s:** %s' % (i, k, v))

    A('\n## What the rooms look like, tier by tier (1730, abandoned)\n')
    A('The same rule everywhere: a Japanese room of 1730 is sparse. What makes it read as lived-in (and then abandoned) is a few')
    A('right objects, the floor, the smoke on the timber and the litter. What a DayZ player finds is loot lying on the floor,')
    A('on shelves, chest lids and stands, never inside furniture.\n')
    A('| Room tag | Floor | Walls | Ceiling | Built-in fittings | What is in it, tier by tier | Where loot lies |')
    A('|---|---|---|---|---|---|---|')
    for r in ROOMS:
        A('| `%s` | %s |' % (r[0], ' | '.join(esc(x) for x in r[1:])))
    A('\n**The pilot (machiya_t3_01, T3 Kamigata):** tori-niwa `doma` (tataki, kept clear: a bucket, sandals on the stones, litter); `mise` = shop:general (display strip + stands + goods, choba corner, hibachi, tobacco tray, shelf); `zashiki` (tansu, andon, hibachi, laid bedding + folded stack, a box); kitchen `doma` (two pots on the kamado, sink, water jar, tubs, shelf, jars, firewood, kamidana); `storage` (shelving, long chest, bales, boxes, kori, jars, a mat). Loft stays sealed.')

    fams = []
    for e in E:
        if e['_family'] not in fams: fams.append(e['_family'])
    n = 0
    for f in fams:
        A('\n## %s\n' % f)
        fit = f.startswith('Built-in')
        if fit:
            A('| # | ID | Name | What and where | Imp. | Tier | Pri | Period evidence | Key dimensions | Materials (library -> palette) | Needs in the shell | Variants | Reach |')
            A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        else:
            A('| # | ID | Wave | Name | What and where | Level | Tier | Key dimensions | Materials (library -> palette) | Loot surface | Abandoned state | Blocks paths? | Reach | Evidence |')
            A('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for e in E:
            if e['_family'] != f: continue
            n += 1
            mats = '<br>'.join('%s: `%s` -> %s' % (m['surface'], m['material'], m['palette_id']) for m in e['materials'])
            var = '<br>'.join('`%s` %s' % (v['id'], v['differs_by']) for v in e['variants'])
            tiers = ','.join(str(t) for t in e['tiers']) + ('' if e.get('region', 'all') == 'all' else ' (%s)' % e['region'])
            rc = e['reach']
            reach = '%d shells / %d rooms%s' % (rc['shells'], rc['rooms'], (' + %d shop sets' % rc['shop_sets']) if rc['shop_sets'] else '')
            if fit:
                A('| %d | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (n, e['id'], esc(e['name']), esc(e['what']), e['importance'], tiers, e['priority'],
                  esc(e['period_evidence']), esc(fmt_dims(e['dimensions'])), esc(mats), esc(e['structural']), esc(var), reach))
            else:
                wv = '**1**' + (' (pilot)' if e.get('pilot') else '') if e.get('wave') == 1 else str(e.get('wave', 2))
                A('| %d | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (n, e['id'], wv, esc(e['name']), esc(e['what']), e['importance'], tiers,
                  esc(fmt_dims(e['dimensions'])), esc(mats), esc(e['loot_surface']), esc(e['abandoned_state']), esc(e.get('blocks_path') or '-'), reach, esc(e['period_evidence'])))

    A('\n## Wave 1: the props to build first\n')
    A(WAVE1_NOTE + '\n')
    A('| Prop | Pilot rooms | Why first |')
    A('|---|---|---|')
    for e in E:
        if e.get('wave') == 1:
            A('| `%s` %s | %s | %d shells / %d rooms%s |' % (e['id'], esc(e['name'].split('(')[0].strip()), ', '.join(e.get('pilot') or ['- (Phase C wave 1)']),
              e['reach']['shells'], e['reach']['rooms'], (' + shop sets' if e['reach']['shop_sets'] else '')))
    A('\nPlus the fittings the pilot needs: `jp_p_fit_kamado` and `jp_p_fit_agarikamachi` (promote from the machiya code), `jp_p_fit_nagashi`, `jp_p_fit_kamidana`, `jp_p_fit_mise_floor`, `jp_p_fit_ceiling` (`_neda` exists). `jp_p_fit_irori` and `jp_p_fit_setchin` come with Phase C wave 1 (farmhouses, huts, toilet).')

    A('\n## Notes per entry (only where the table is not enough)\n')
    for e in E:
        bits = []
        if e.get('banned_tells_to_watch'): bits.append('- **Banned tells:** ' + '; '.join(e['banned_tells_to_watch']))
        if e.get('deviations'): bits.append('- **Deviations / rules:** ' + '; '.join(d for d in e['deviations'] if d != 'D-none'))
        if e.get('open_questions'): bits.append('- **Open questions:** ' + '; '.join(e['open_questions']))
        bits = [b for b in bits if not b.endswith(':** ')]
        if bits:
            A('**`%s`**' % e['id']); A('\n'.join(bits)); A('')

    A('## Q5 answered offline: which LODs carry vanilla furniture proxies, and how proxies relate to loot\n')
    A('**The rule:** vanilla houses put furniture proxies in **Resolution 1 (LOD0) only** among the visual LODs, plus **Geometry,')
    A('View Geometry and Fire Geometry**. Never in Resolution 2+, Memory, Roadway or Paths. Small wall items (pictures, lamps) are')
    A('Resolution 1 only (sometimes View/Fire), never Geometry. **Loot points are not generated from proxies at run time**: they')
    A('are authored per class in `mapgroupproto.xml` (the Diag loot editor retraces them onto surfaces), and vanilla authors most')
    A('of them ON the proxied furniture: shelf and table points sit exactly at the furniture\'s surface heights, while floor')
    A('points avoid furniture footprints.\n')
    A('**Evidence 1, furniture proxy records per LOD** (ODOL v54, `q5_lods.py`, read-only on `P:\\DZ\\structures\\residential\\houses`):\n')
    A('| House | Res 1 | Res 2 | Geometry | View Geometry | Fire Geometry | Memory | Roadway | in any other LOD |')
    A('|---|---|---|---|---|---|---|---|---|')
    for h in q5['houses']:
        A('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (h['file'], h.get('Res 1', 0), h.get('Res 2', 0), h.get('Geometry', 0), h.get('ViewGeometry', 0),
          h.get('FireGeometry', 0), h.get('Memory', 0), h.get('Roadway', 0), ', '.join(h['furniture_in_other_lods']) or 'none'))
    t = q5['loot_totals']
    A('\n**Evidence 2, loot points against the proxies** (`q5_loot.py`: Res 1 proxy transforms + each furniture p3d\'s bounding box + the')
    A('class\'s points in the vanilla Chernarus `mapgroupproto.xml`, model frame (mx,my,mz) = (-lz,ly,lx) from pokemon_dev WORLD_BUILDINGS §0):\n')
    A('| Class | Points | Raised (>5 cm above the floor) | Raised and on a proxied piece | Floor |')
    A('|---|---|---|---|---|')
    for r in q5['loot_classes']:
        A('| %s | %d | %d | %d | %d |' % (r['class'], r['points'], r['raised'], r['raised_on_furniture'], r['floor']))
    A('\n- **%d of %d raised points** lie inside a proxied piece\'s footprint at one of its surface heights; the other %d matched no proxy box' % (t['raised_on_furniture'], t['raised'], t['raised'] - t['raised_on_furniture']))
    A('  (built-in surfaces of the shell, or pieces whose box the script missed). **%d of %d floor points** fall inside a furniture footprint.' % (t['floor_in_footprint'], t['floor']))
    A('- Surface heights found (m above the floor): ' + '; '.join('%s %s' % (k, '/'.join('%.2f' % x for x in v)) for k, v in q5['surface_heights_by_furniture'].items()) + '.')
    A('- Point size: range %.2f-%.2f on furniture, %.2f-%.2f on floors; height = 2.5 x range, capped at 2.0 (container `lootshelves`,' % (t['range_furniture'][0], t['range_furniture'][1], t['range_floor'][0], t['range_floor'][1]))
    A('  tag `shelves`, for furniture; `lootFloor`, tag `floor`, for floors).')
    A('- Furniture p3ds: %s. %s.' % (q5['furniture_p3d_lods'], q5['config']))
    A('\n**What we do (binding for B3/B4):**')
    A('1. A furnished variant p3d = the shell parts + furniture proxies in **Resolution 1, Geometry, View Geometry and Fire')
    A('   Geometry** (PLAYBOOK §10.4 "same LODs as vanilla"). Purely visual flat props (mats, litter, cushions, fallen leaves)')
    A('   and hanging ones (jizai-kagi, kamidana miya) go in Resolution 1 only. Laid bedding carries loot, so it keeps a thin')
    A('   Geometry slab like the vanilla beds (in all four LODs).')
    A('2. Each prop p3d has its own LODs like vanilla: Res 1-2 (3 for furniture), Geometry, View, Fire; no Memory. **Roadway')
    A('   only where a player may stand** (vanilla tables and beds have it; the vanilla shelf case_d has none yet carries four loot levels). Each gets a `StaticObj_JP_F_<Name>` class')
    A('   (HouseNoDestruct, scope 1) in `jp_furniture.pbo`, as vanilla does.')
    A('3. Each prop sidecar lists `loot_surfaces` (height, rectangle, range). The loot generator writes them as `lootshelves`')
    A('   points and subtracts every collision footprint + 0.4 m from the `lootFloor` points (PLAYBOOK §10.4, now confirmed).')
    A('4. Proxied furniture does not count against the house face budget (it is a separate p3d): good news for the machiya at')
    A('   11,931 / 12,000. Side effect: furniture vanishes when the house drops to Resolution 2, which only shows through open')
    A('   shop fronts at a distance (accepted by vanilla).')

    A('\n## Engine and gameplay notes for the decorator\n')
    A(ENGINE)

    A('\n## Order of work after G1 (rough effort in agent sessions)\n')
    A(ORDER)

    A('\n## Interior materials (%d new materials, %d texture sets; %d existing reused)\n' % (mn['counts']['new_materials'], mn['counts']['texture_sets'], mn['counts']['existing_reused']))
    A('| Material | Status | Family | Palette ID | Tile (m) | px/m | Fire / roadway | _w0 / _w1 / _w2 | Used by | Note |')
    A('|---|---|---|---|---|---|---|---|---|---|')
    for m in mn['materials']:
        new = m['status'] == 'new'
        A('| `%s` | %s | %s | %s%s | %s | %s | %s | %s | %d | %s |' % (m['id'], m['status'], m['family'], m['palette_id'], ' **(new)**' if m['palette_status'] != 'existing' else '',
          m.get('tile_size_m', '-'), m.get('px_per_m', '-'), esc(m.get('penetration_rvmat', '-')),
          esc('%s / %s / %s' % (m['wear']['_w0'], m['wear']['_w1'], m['wear']['_w2'])) if new else '-', len(m['used_by']), esc(m['note'])))
    A('\n**Tatami size and module for our grid (the question asked):** Kyoma is tatami-based, 1.91 x 0.955 m mats; Inakama/Edoma')
    A('is column-based, 1.76 x 0.88 m [N01, T01, T03]. **Our kit is column-based (Inakama):** 1 ken = 1.820 m centre to centre,')
    A('and the machiya\'s mats fill the room between post faces, so a 3 x 1.5 ken room gets mats of about 1.78 x 0.87 m. The')
    A('tatami material is one mat per texture, so the size difference never touches the kit (PLAYBOOK §3). Thickness 0.055, heri')
    A('0.03 (PLAYBOOK §4).')
    A('\n**Requested palette entries:**\n')
    A('| Palette ID | sRGB | Method | Why | Samples / check |')
    A('|---|---|---|---|---|')
    for p in REQ_PAL:
        src = '; '.join('%s box %s -> %s' % (s['ref'], s['box'], s['value']) for s in p['samples'])
        A('| %s | %s | %s | %s | %s |' % (p['id'], p['srgb'], p['method'], esc(p['why']), esc((src + '. ' if src else '') + p['check'])))

    A('\n## Checks the builders must run\n')
    A('- Props: C1, C2, C4, C5 (furniture <=1000 / small prop <=300 faces LOD0), C6 (base within 0-2 cm of the floor, no')
    A('  interpenetration > 1 cm, loot clearance), C8, C9.')
    A('- NEW for the decorator: **clear band** (1.00 m door-to-door and door-to-centre, sampled on the Roadway minus footprints),')
    A('  **door clear zone** (no collision prop within 0.4 m of any door\'s clear opening, leaves open and closed), and')
    A('  **floor coverage** (collision footprints <= 25 % living / 40 % storage).')
    A('- Fittings: the part checks (C1-C5, C8) plus C7 head room over the hearth hook beam and the kamidana (>= 2.00 underside).')
    A('- Materials: C1 palette, C19 matte finish (T12); ceramics and lacquer are the only glossy interior materials.')
    A(LATER)
    return '\n'.join(L) + '\n'


ENGINE = '''- **Proxies:** base centre at the prop origin, standing on its floor (PLAYBOOK §10.4); Geometry closed and convex (one
  or a few boxes); View and Fire Geometry like vanilla. Fire uses vanilla penetration rvmats (wood, pottery, fabric_thin,
  hay, iron).
- **Walking:** D1 doors >= 1.00 m clear and D5 corridors >= 1.00 m stay true WITH the furniture in. The tori-niwa passage
  keeps >= 1.00 m beside every prop (it has 1.15 m today beside the step). Infected path along the navmesh: regenerate it
  after furnishing (NAVMESH_STEPS.md), because collision props change it.
- **Stairs and low lofts (D3, D4):** nothing on a stair flight, and a 1.10 x 1.00 m clear landing at every stair foot and
  head; no collision prop in a D3 crouch band (1.40-2.10 m head room) so nobody gets wedged; sealed lofts get nothing.
- **Flat props have no Geometry:** mats, litter decals, fallen leaves, cushions. Laid bedding is the exception: a thin
  (0.08) Geometry slab so items rest on it, like vanilla beds; a player steps over it.
- **Hanging props** (jizai-kagi, kamidana miya) have no Geometry; head room under them stays >= 2.00 except over the irori
  pit, where nobody stands.
- **Loot heights:** follow vanilla: shelf points 0.10-1.25 m, never above 1.40 m (the fridge top is the vanilla maximum
  found); nothing on the kamidana.
- **Abandoned variants are separate proxies** (`_tipped`, `_ransacked`, `_open`...), so a furnished variant picks its own
  mix; the shell never changes.
- **Doors:** no prop inside a door leaf's sweep or park zone; C10 must still pass with the furniture proxied in (the camera
  ray must not hit a prop before the leaf).'''

ORDER = '''| Step | What | Output | Effort |
|---|---|---|---|
| 1. Materials (B1) | The 21 new interior materials x 3 wear levels through `research/materials/` (make_textures + build_materials, T12 finishes), 4 palette entries after Stephen's decision 13 | `src/JP/common/materials/{floor,ground,ceramic,textile,...}`, contact sheet | 1 session |
| 2. Fittings (B2) | Promote kamado + agari-kamachi from the machiya code into `parts/kit`; build nagashi, kamidana, mise-floor strip, ceiling recipes (P1); irori + setchin for Phase C wave 1; tokonoma / chigaidana / oshiire only when a shell asks | kit parts + sidecars + contact sheet | 1 session |
| 3. Props wave 1 (B3) | The 24 wave-1 props with LODs, sidecars (`loot_surfaces`, abandoned variants), `jp_furniture.pbo` + StaticObj classes, contact sheet vs references | `src/JP/furniture/...` | 2 sessions (can run as 2 parallel agents: kitchen/storage and rooms/shop) |
| 4. Pilot (B4) | Furnished variant of machiya_t3_01: regenerate the mise floor with the display strip, proxies in Res 1 / Geo / View / Fire, loot generator with `lootshelves` from the sidecars, the new decorator checks, navmesh note, one bundled walk for Stephen (G4) | `buildings/machiya_t3_01` furnished variant + REPORT | 1 session |

Total about 5 agent sessions, about 3 in wall-clock if steps 2 and 3 overlap after step 1. Wave-2 props (casks, baskets,
screens, racks, butsudan, stable and farm sets) follow with Phase C wave 1 shells.'''

LATER = '''
## Later (out of scope for this list)

- **Trade kits:** every workshop and shop-set specific prop (brewery vats and press, smithy forge and bellows, kilns,
  looms and wheels, dyer's vats, sake-shop cask rack fill, apothecary drawers...) is built with its shell or set.
- **Elite interiors:** karakami paper, lacquer and gold, korai-beri heri, chigaidana with painted doors, noh-style
  panels: honjin jodan-no-ma and daimyo mansion only (status overlay), P3.
- **Religious interiors:** temple and shrine halls (stage R).
- **Interior openings:** fusuma leaves, interior shoji, ranma transoms, stairs: parts, owned by the parts-kit audit (PA1);
  this list only supplies `jp_m_paper_fusuma`.
- **Unverified for 1730 and left out:** naga-hibachi (long brazier with drawers), mizuya-dansu kitchen cabinets, kaidan-dansu
  (stair chest), side-handled teapots, tetsubin, zaguri reeler (BUILDING_LIST contradictions 1, 4, 9).
- **Lighting:** lit andon and hearth fires (light points, particles) are a later decision.'''

if __name__ == '__main__':
    main()
