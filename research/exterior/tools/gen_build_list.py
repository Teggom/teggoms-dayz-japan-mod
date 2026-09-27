"""Generates the exterior build list (JSON + MD), the materials list and the refs index from ONE data source,
so the markdown and the JSON always say the same thing (BUILD_LIST_TEMPLATE rule).

Run:  python research/exterior/tools/gen_build_list.py
Reads: data/research_ext/meta.json (download log), playbook/refs_index.json (for id checks)
Writes (binary, LF): research/exterior/build_list.json, materials_needed.json, refs_index.json, BUILD_LIST.md
Research agent A-EXT, 2026-09-27.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'exterior')
DATE = '2026-09-27'

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

STD_CHECKS = ['C1', 'C2', 'C3', 'C4', 'C5', 'C8', 'C9']

# ------------------------------------------------------------------------------------------------ entries
E = []
def add(family, **k):
    k['_family'] = family
    k.setdefault('checks', STD_CHECKS)
    E.append(k)

# ================================================================= ROOFS
add('Roofs', id='jp_p_roof_forms', name='Roof forms and footprint rules (kirizuma / yosemune / irimoya)',
    what='The roof generator spec: which form and covering each tier and region uses, pitches, overhangs and spans.',
    importance='hero', tiers=[1, 2, 3], region='all', status_overlay='commoner', priority='P1',
    period_evidence='Kitamura house 1687, yosemune thatch [E01]; Kiyomiya late 17th c. yosemune thatch [E01]; Ito late 17th-early 18th c. irimoya thatch [E01]; Hirose late 17th c. kirizuma thatch [x08]; Sasaki 1731/32 yosemune thatch with stone-weighted board eaves [E02]; Ioka late 17th-early 18th c. kirizuma sangawara machiya [E03]; tile banned in Edo 1657 except storehouses, encouraged 1720 [E09]',
    refs=[R('x08_hirose_earthwall', 'kirizuma thatch, late 17th c. building (Koshu)', True), R('x07_sasaki_1985', 'Sasaki house 1732: thatch with board pent eave', True),
          R('x01_ioka_a', 'Ioka machiya: kirizuma sangawara, gable pent roof', True), R('x04_misawa_a', 'kirizuma stone-weighted board roof (mid-19th c.)', True),
          R('x22_morse_thatch_kanto', 'Kanto hip thatch near Tokyo (1880s)'), R('x36_hiroshige_ishibe', 'roadside tea house: thatch kirizuma + board pents', True)],
    dimensions={
        'grid_m': D('1.820 ken / 0.910 half-ken; footprints are unions of ken rectangles', 'PLAYBOOK §3-4'),
        'pitch_kawara_sun': D('4.5 default (4-5.5) = 24.2 deg', 'PLAYBOOK §4'),
        'pitch_ishioki_sun': D('3-3.5 (16.7-19.3 deg); steeper and the stones slide', 'T40, PLAYBOOK §4'),
        'pitch_itabuki_sun': D('4-5', None, 'PLAYBOOK §4 value, no period source'),
        'pitch_thatch_deg': D('45 (50-60 only gassho, not on our map)', 'T41'),
        'eave_overhang_m': D('tile 0.90; thatch 0.80-1.20; ishioki 0.90-1.20; board 0.60-0.90; gable/verge 0.30-0.45', 'PLAYBOOK §4 (board: assumed)'),
        'main_span_townhouse_ken': D('<=3 between main-roof walls (Edo townsmen rule 1668); extra depth by lean-to', 'T48'),
        'main_span_farmhouse_m': D('8.2-10.0 (Kiyomiya 8.2, Kitamura 8.9, Ito 9.1, Sasaki 10.0) = 4.5-5.5 ken; the 3-ken rule is urban, not rural', 'E01, E02'),
        'plan_examples_m': D('Kitamura 15.6x8.9; Kiyomiya 13.6x8.2; Ito 16.4x9.1; Sasaki 24.7x10.0; Ioka 7.9 wide x 12.7 deep; Misawa 13.6x12.7', 'E01-E03'),
        'wall_plate_keta_m': D('machiya ground storey 2.90-3.20 at the street eave edge; T1-2 thatch: see decision 6', 'PLAYBOOK §4'),
    },
    materials=[],
    connectors=['footprint: rectangle or L/T union on the ken grid', 'eave line = keta top outer edge', 'ridge line centred on the span',
                'kawara columns 0.260 m = 7 per ken, so a column edge lands on every ken line', 'lean-to (geya/hisashi) roofs attach below the main eave at a wall line'],
    variants=[V('kirizuma', 'gable: machiya, nagaya, kura, Kiso post town, Koshu farmhouse, tea house'),
              V('yosemune', 'hip: Kanto farmhouse (Kitamura 1687, Kiyomiya), headman house (Sasaki)', 1),
              V('irimoya', 'hip-and-gable with a smoke opening in the small gable: Kansai/Kanto farmhouse (Ito), bigger inns', 2),
              V('kabuto', 'Sasaki-type gable cut into a hip (kabuto-zukuri) at one end; P2', 2)],
    deviations=['Tier and region rules: T1 thatch or ishioki, never tile; T2 ishioki/board/thatch, tile only on kura and big inns; T3 Kamigata sangawara, T3 Edo about half board (see kakigara decision) and half new sangawara (PLAYBOOK §2.1, E09)'],
    lod_budget='roof share of the building budget: machiya roof <=3k faces LOD0 (PLAYBOOK §6.1)',
    banned_tells_to_watch=['kawara as a flat textured plane', 'chimneys, dormers, metal', 'Chinese upturned corners', 'curb (mansard) roofs: Morse says never seen'],
    open_questions=['Decision 6: thatch eave height versus the 2.20 m soffit rule'])

add('Roofs', id='jp_p_roof_eave_soffit', name='Eave soffit: rafters, sheathing and fascia (noki-ura)',
    what='The visible underside and edge of every eave: exposed rafters, sheathing boards and the fascia the eave tiles or boards sit on.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Surviving period buildings all show exposed rafter soffits [x01, x08, x07]',
    refs=[R('x08_hirose_earthwall', 'pole rafters and bamboo lath under thatch verge', True), R('x01_ioka_a', 'square rafters under tile eave', True),
          R('x29_morse_hisashi', 'thin boards on slender brackets')],
    dimensions={
        'rafter_section_m': D('0.045 x 0.060 (tile/board); thatch: round poles d 0.06-0.08', None, 'typical 1.5 x 2 sun; not measured'),
        'rafter_spacing_m': D('0.303 (ken/6)', None, 'about 1 shaku, a common spacing; ken/6 keeps rafters on the grid'),
        'sheathing_m': D('boards 0.012 thick visible between rafters; thatch: bamboo lath at 0.10', None, 'visual, x08'),
        'fascia_m': D('0.030 x 0.120 (tile: carries the eave tiles); none on thatch', None, 'assumed'),
        'keta_m': D('0.120 x 0.180 wall plate; ends project 0.15 at gables', None, 'assumed'),
    },
    materials=[M('rafters, fascia, sheathing', 'jp_m_wood_weathered', 'timber_weathered'), M('thatch lath', 'jp_m_bamboo_weathered', 'bamboo_weathered')],
    connectors=['eave: rafter seats on keta top; rafter feet on the eave line', 'soffit follows the roof pitch; the generator emits it for every eave run'],
    variants=[V('_tile', 'square rafters + boards + fascia'), V('_board', 'thinner rafters, no fascia, boards overhang 0.03'), V('_thatch', 'pole rafters + bamboo lath', 1)],
    lod_budget='LOD0 every rafter; LOD1 every 2nd; LOD2 flat textured soffit',
    banned_tells_to_watch=['flat untextured soffit at LOD0', 'painted white timber'])

add('Roofs', id='jp_p_roof_sangawara_field', name='Sangawara field tiles',
    what='The corrugated one-piece S-tile field of every tiled town roof, kura and inn.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Sangawara invented 1674 [T07, E06]; Ioka machiya (Nara, late 17th-early 18th c.) is sangawara [E03]; Kyoto commoner tile spreads after sangawara, standard look by the 18th c. [E10]; Edo tile encouraged 1720 [E09]',
    refs=[R('c08_kyomachiya', 'sangawara on a Kyoto machiya'), R('x03_ioka_c', 'sangawara roof on the dated Ioka house', True),
          R('x18_morse_yedogawara', 'Yedo-gawara (sangawara) profile at the eave'), R('x16_morse_tile_eaves', 'eave tiles and field')],
    dimensions={
        'working_width_m': D(0.260, 'PLAYBOOK §4 (ken/7)'),
        'exposure_m': D(0.235, 'PLAYBOOK §4'),
        'roll_height_m': D('0.05-0.06', 'PLAYBOOK §4'),
        'tile_thickness_m': D(0.018, None, 'fired clay 15-20 mm; for edge silhouette only'),
        'bedding_m': D('tile surface 0.08 above sheathing (mud bed)', None, 'Morse [T59]: tiles bedded in a thick mud layer; thickness not given'),
        'lod0_segments_per_column': D('>=4', 'PLAYBOOK §6.1'),
    },
    materials=[M('tiles', 'jp_m_roof_kawara', 'kawara_ibushi'), M('white pointing (variant)', 'jp_m_wall_shikkui', 'shikkui_white')],
    connectors=['eave: first course overhangs the fascia by 0.06', 'ridge: last course tucks under the ridge noshi', 'verge: field stops 0.13 inside the verge line for jp_p_roof_sangawara_verge', 'columns 0.260 aligned to ken lines'],
    variants=[V('_std', 'plain field; per-row tint offset (W8)'), V('_pointed', 'white mortar pointing on the 2-3 rows at the eave and ridge; Morse: common on better roofs [T59]', 3)],
    lod_budget='<=3k faces for a machiya roof incl. ridge and ends; LOD1 2 segments/column; LOD2 plane',
    banned_tells_to_watch=['flat textured plane', 'identical rows (no W8 variation)', 'glazed or coloured tiles'])

add('Roofs', id='jp_p_roof_sangawara_eave', name='Sangawara eave tiles (noki-gawara, manju type)',
    what='The first course of a tiled roof: small round end plus a turned-down lip carrying a relief band.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Special eave tile named with sangawara [E06]; form drawn by Morse [x16, x18]',
    refs=[R('x16_morse_tile_eaves', 'eave tiles: round end + turned-down lip'), R('x18_morse_yedogawara', 'Yedo eave tile profile'), R('c08_kyomachiya', 'eave line in photo')],
    dimensions={
        'lip_depth_m': D(0.045, None, 'measured by eye from Morse fig. 71 proportions against the 0.26 tile'),
        'round_end_diameter_m': D(0.075, None, 'small manju end; Morse fig. 71 proportion'),
        'overhang_past_fascia_m': D(0.06, None, 'assumed'),
    },
    materials=[M('tile', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['eave: one per column (0.260), placed by the generator on the eave line'],
    variants=[V('_tomoe', 'round end with a mitsudomoe relief'), V('_plain', 'round end plain'), V('_lod1_strip', 'LOD1: the whole eave as one extruded strip')],
    banned_tells_to_watch=['family crests of status on commoner eaves; the Tokugawa crest (Morse: rarely seen)'],
    open_questions=['Straight-cut ichimonji eave tiles are common in Kyoto today; their first date is unverified, so they are not listed'])

add('Roofs', id='jp_p_roof_sangawara_verge', name='Verge tiles (sode-gawara / keraba)',
    what='Tiles that turn down over the bargeboard along every tiled gable edge.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Named among the sangawara special tiles [E06]',
    refs=[R('x01_ioka_a', 'verge line on the Ioka gable', True), R('c08_kyomachiya', 'verge tiles in photo')],
    dimensions={'flange_drop_m': D(0.07, None, 'covers the bargeboard top; visual'), 'module_m': D('0.235 per course (matches exposure)', 'PLAYBOOK §4')},
    materials=[M('tile', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['verge: one per course along the gable line, over jp_p_roof_hafu', 'meets the eave tile at the corner and the ridge end below the onigawara'],
    variants=[V('_L', 'left hand'), V('_R', 'right hand')])

add('Roofs', id='jp_p_roof_kawara_ridge', name='Tiled ridge (noshi courses + ganburi cap) and hip ridge',
    what='Stacked flat noshi courses capped by a round tile along the ridge, and the same build-up down the hips of hipped tile roofs.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Noshi and ganburi named with sangawara [E06]; course count rises with status [PLAYBOOK §6.1]; Morse on ridges [T59]',
    refs=[R('c26_morse_tile_ridge', 'stacked ridge build-up'), R('x17_morse_hongawara', 'ridge and field relation'), R('c08_kyomachiya', 'machiya ridge, photo')],
    dimensions={
        'noshi_course_m': D('0.025 thick each, 0.22 wide', None, 'assumed from c26 proportions'),
        'courses': D('T2 kura/inn 3; T3 machiya 3-5; hongawara elite 7 (later)', 'PLAYBOOK §6.1'),
        'cap_diameter_m': D(0.16, None, 'assumed'),
        'height_above_field_m': D('3 courses 0.30; 5 courses 0.38', None, 'derived from the values above'),
        'hip_ridge': D('same section minus 1 course; ends in a small round end tile', 'Morse [T59]'),
    },
    materials=[M('tiles', 'jp_m_roof_kawara', 'kawara_ibushi'), M('mortar bedding lines', 'jp_m_wall_shikkui', 'shikkui_white')],
    connectors=['ridge: runs the ridge line between the two onigawara', 'hip: from the ridge end to the eave corner on yosemune/irimoya'],
    variants=[V('_c3', '3 noshi courses', 2), V('_c5', '5 noshi courses', 3), V('_hip', 'hip ridge (kudarimune) with an end tile')],
    banned_tells_to_watch=['plaster wave reliefs (Morse saw them on big fire-proof buildings of the 1880s; not on 1730 commoner houses)'])

add('Roofs', id='jp_p_roof_onigawara', name='Ridge-end tile (onigawara)',
    what='The shouldered end block at each end of a tiled ridge.',
    importance='standard', tiers=[2, 3], region='all', status_overlay='commoner', priority='P1',
    period_evidence='Onigawara named among sangawara special tiles [E06]; Morse: ridges always end in a shouldered mass [T59]',
    refs=[R('c26_morse_tile_ridge', 'ridge end'), R('c08_kyomachiya', 'machiya ridge end')],
    dimensions={'height_m': D('T2 0.30; T3 0.38 (scales with the ridge)', None, 'about 1x ridge height; not measured'), 'width_m': D('0.30-0.36', None, 'assumed')},
    materials=[M('tile', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['ridge: one at each ridge end, over the verge'],
    variants=[V('_plain', 'plain shouldered block'), V('_sui', 'with the character for water in relief (fire charm; Morse notes it on ridge ends) ')],
    banned_tells_to_watch=['demon faces and crests of temple scale on commoner houses'])

add('Roofs', id='jp_p_roof_hongawara', name='Hongawara set (flat pans + round covers, eave and ridge)',
    what='The two-piece true tile for rich kura and, later, temples, gates and samurai elite.',
    importance='standard', tiers=[3], region='all', priority='P3',
    period_evidence='Hongawara is the older tile, on temples, castles and rich kura [T10, PLAYBOOK §6.1]',
    refs=[R('x17_morse_hongawara', 'pans + covers, round eave ends'), R('c09_himeji', 'hongawara on a castle')],
    dimensions={'column_m': D('0.303 (ken/6)', None, 'real pans are about 1 shaku wide; ken/6 keeps the grid'), 'cover_diameter_m': D(0.15, None, 'assumed')},
    materials=[M('tiles', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['same eave, ridge and verge connectors as sangawara, 6 columns per ken'],
    variants=[V('_field', 'field'), V('_eave', 'round-end + flat eave with karakusa lip'), V('_ridge', 'taller ridge, 5-7 courses')])

add('Roofs', id='jp_p_roof_ishioki_field', name='Stone-weighted board roof: board field (ishioki-yane, kureita)',
    what='Split boards in overlapping courses at a low pitch, the roof of Kiso post towns, mountain and coast villages.',
    importance='hero', tiers=[1, 2], region='rural', priority='P1',
    period_evidence='Stone-weighted board roofs in Kyoto in the early Edo period [E14]; Sasaki house 1731/32 has stone-weighted board eaves [E02]; Kiso post towns [c01-c03]',
    refs=[R('x04_misawa_a', 'surviving ishioki roof, chestnut boards (mid-19th c.)', True), R('c01_narai_street', 'Narai board roofs'),
          R('c03_tsumago_street', 'Tsumago board roofs'), R('x37_eisen_narai', 'Narai c.1835: boards and stones (lower left)', True)],
    dimensions={
        'board_length_m': D('0.30-0.50', 'E18 (low-grade web source)'),
        'board_width_m': D('0.09-0.21, random per board (W8)', 'E18 figure read as cm; assumed'),
        'board_thickness_m': D('0.004 real; model course edge 0.012', 'E18; model value for silhouette (reason)'),
        'course_exposure_m': D(0.15, None, 'about 1/3 of the board length, triple lap; not sourced'),
        'eave_edge_stack_m': D('0.05-0.08 visible thickness', None, 'visual, x04'),
        'pitch_sun': D('3-3.5', 'T40'),
    },
    materials=[M('boards', 'jp_m_roof_kureita', 'roof_board_silver')],
    connectors=['eave: first course overhangs the rafter feet by 0.05', 'ridge: jp_p_roof_board_ridge', 'verge: jp_p_roof_hafu _ishioki', 'battens and stones: jp_p_roof_ishioki_battens'],
    variants=[V('_std', 'standard'), V('_worn', 'missing/lifted boards, moss (W6) on north slope')],
    lod_budget='courses as geometry steps only within 3 rows of the eave and ridge (as kawara); rest normal map',
    banned_tells_to_watch=['pitch steeper than 3.5 sun', 'uniform brown boards (they weather silver-grey, x04)'])

add('Roofs', id='jp_p_roof_ishioki_battens', name='Stone-weighted roof: battens and stones (osae-gi + ishi)',
    what='Split-pole battens laid across the boards parallel to the eave, with river stones resting on them.',
    importance='hero', tiers=[1, 2], region='rural', priority='P1',
    period_evidence='as jp_p_roof_ishioki_field',
    refs=[R('x04_misawa_a', 'battens + stones, photo', True), R('c02_narai_facade', 'Narai roofs'), R('x37_eisen_narai', 'stones in a grid on a roof, c.1835', True)],
    dimensions={
        'batten_diameter_m': D('0.06-0.08 split pole', None, 'visual, x04'),
        'batten_spacing_m': D('0.60 up the slope', None, 'counted roughly on x04; PLAYBOOK §6.1 gives 0.45-0.60 (assumed)'),
        'stone_size_m': D('0.15-0.30', 'PLAYBOOK §6.1 [T40, c01-c03]'),
        'stone_spacing_m': D('0.30-0.45 along each batten, jittered', None, 'visual, x04'),
    },
    materials=[M('battens', 'jp_m_wood_weathered', 'timber_weathered'), M('stones', 'jp_m_stone_river', 'stone_lantern')],
    connectors=['battens run eave-parallel between verges; stones sit on the upslope side of each batten', 'generator scatters stones from the 8-shape set with random yaw'],
    variants=[V('_stoneset8', '8 stone shapes'), V('_sparse', 'fewer stones (poor / neglected)', 1)],
    lod_budget='stones: LOD0 ~20 faces each, LOD1 merged lumps, LOD2 texture only')

add('Roofs', id='jp_p_roof_itabuki_field', name='Thin shingle / board roof (itabuki, kokera)',
    what='Thin split-shingle roofs: Edo townhouses before tile, back-alley nagaya, T2 houses and sheds.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Board and kokera roofs on early machiya [T05]; in Edo tile was banned 1657-1720 except storehouses, board roofs with oyster shells recommended, still in use in the Kyoho era [E09]',
    refs=[R('x14_morse_shingle_laid', 'shingles laid in courses'), R('x15_morse_shingle_ridge', 'shingle roof ridge'), R('c18_hiroshige_mariko', 'board-roofed houses c.1833', True)],
    dimensions={
        'shingle_thickness_m': D('0.002-0.003 (kokera)', 'E17'),
        'course_exposure_m': D(0.09, None, 'about 3 sun; Morse marks courses with a measure but gives no value'),
        'eave_edge_m': D('0.03-0.05 visible stack', None, 'assumed'),
        'pitch_sun': D('4-5', None, 'PLAYBOOK §4'),
    },
    materials=[M('shingles', 'jp_m_roof_kokera', 'roof_board_silver'), M('bamboo strips (variant)', 'jp_m_bamboo_weathered', 'bamboo_weathered'),
               M('oyster shells (variant)', 'jp_m_roof_kakigara', 'kakigara_shell')],
    connectors=['as ishioki: eave, board ridge, verge'],
    variants=[V('_plain', 'plain courses'), V('_bamboo', 'bamboo strips nailed obliquely ridge to eave against gales (Morse fig. 63)'),
              V('_kakigara', 'Edo only: oyster shells over the boards (fire measure 1657-Kyoho) - only if decision 3 is yes', 3)],
    banned_tells_to_watch=['temple-style thick curved kokera on houses (PLAYBOOK §6.1)'],
    open_questions=['Decision 3: kakigara-buki for Edo T3'])

add('Roofs', id='jp_p_roof_board_ridge', name='Board ridge (for ishioki and shingle roofs)',
    what='Thin strips nailed over the ridge in a mass, held by battens; on ishioki roofs weighted with stones.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Morse fig. 65 (1880s); form follows from the board roof [E14]',
    refs=[R('x15_morse_shingle_ridge', 'ridge of shingle roof, Musashi'), R('x04_misawa_a', 'ishioki ridge', True)],
    dimensions={'width_m': D('0.30-0.40', None, 'visual, x15'), 'height_m': D('0.06-0.10', None, 'visual')},
    materials=[M('strips', 'jp_m_roof_kureita', 'roof_board_silver'), M('stones', 'jp_m_stone_river', 'stone_lantern')],
    connectors=['ridge: full ridge length, ends flush with the verge boards'],
    variants=[V('_strips', 'shingle roof ridge'), V('_stoned', 'ishioki ridge with a stone row')])

add('Roofs', id='jp_p_roof_thatch_body', name='Thatch roof body (kaya-buki): field, cut eave, verge and hips',
    what='The thick thatch mass generated over any footprint, with the squared eave cut that shows its thickness.',
    importance='hero', tiers=[1, 2], region='rural', priority='P1',
    period_evidence='Kitamura 1687, Kiyomiya late 17th c. (yosemune), Ito (irimoya), Hirose (kirizuma), Sasaki 1731/32: all thatch [E01, E02, x08]',
    refs=[R('x08_hirose_earthwall', 'kirizuma thatch: thick verge, cut edge', True), R('x06_suzuki_a', 'hip thatch with board lower eave (early 19th c.)', True),
          R('c05_ouchi_thatch', 'thatch colour, hip roofs'), R('x22_morse_thatch_kanto', 'Kanto hip thatch'), R('x26_morse_farmhouse_kabutoyama', 'old farmhouse, Musashi')],
    dimensions={
        'eave_cut_thickness_m': D('0.60 (0.40-0.80)', 'Morse: eaves trimmed square or slightly rounded, often two feet or more [T59]; PLAYBOOK §6.1'),
        'field_thickness_m': D('0.35-0.45', None, 'Morse: not the same thickness throughout [T59]'),
        'verge_overhang_m': D('0.30-0.45', 'PLAYBOOK §4, x08'),
        'pitch_deg': D(45, 'T41'),
        'eave_cut_profile': D('square or slightly rounded; 2-3 visible light/dark layer bands', 'T59'),
    },
    materials=[M('thatch surface', 'jp_m_roof_thatch', 'thatch_weathered'), M('eave cut face', 'jp_m_roof_thatch_cut', 'thatch_weathered')],
    connectors=['eave: rests on the rafter feet; cut face vertical at the eave line + overhang', 'ridge: jp_p_roof_thatch_ridge', 'hips rounded (radius 0.3)'],
    variants=[V('_yosemune', 'Kanto hip (Kitamura type)', 1), V('_kirizuma', 'Koshu gable (Hirose type)', 1), V('_irimoya', 'hip-and-gable (Ito type)', 2),
              V('_new', 'freshly re-thatched (thatch_new tint via _w0), 1 roof in 10')],
    lod_budget='LOD0 surface undulation low; cut edge 2-3 steps; LOD2 single shell',
    banned_tells_to_watch=['thin flat thatch plane', 'clean uniform colour: north slopes carry moss (W6)'])

add('Roofs', id='jp_p_roof_thatch_ridge', name='Thatch ridge treatments (bamboo, tiled, turf, umanori)',
    what='The ridge caps that close the top of a thatch roof; each region has its own style.',
    importance='standard', tiers=[1, 2], region='rural', priority='P1',
    period_evidence='Kiyomiya house, late 17th c.: iris growing on the (turf) ridge [E01]; ridge members count up with status [T17]',
    refs=[R('c27_morse_thatch_ridge', 'bamboo ridge, Musashi'), R('x21_morse_thatch_tile_ridge', 'tiled ridge on thatch, Musashi'),
          R('x22_morse_thatch_kanto', 'Kanto thatch ridge'), R('x06_suzuki_a', 'ridge with vent', True)],
    dimensions={'height_above_thatch_m': D('0.50-0.80', None, 'visual, c27/x21'), 'umanori_spacing_m': D('0.91 (half-ken)', None, 'grid choice'),
                'umanori_count': D('T1 3-5, T2 5-7 per ridge', None, 'T17 says the count rises with status; numbers assumed')},
    materials=[M('bamboo binding', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('tiles (variant)', 'jp_m_roof_kawara', 'kawara_ibushi'),
               M('thatch/turf cap', 'jp_m_roof_thatch', 'thatch_weathered'), M('crossed members', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['ridge: full ridge length; ends flush with the thatch verge or hip apex'],
    variants=[V('_bamboo', 'bamboo-bound ridge (Kanto)', 1), V('_tile', 'noshi/round tiles over the thatch ridge (Musashi)', 2),
              V('_shiba', 'turf ridge with iris (Kiyomiya type)', 1), V('_umanori', 'grass ridge with crossed timbers')])

add('Roofs', id='jp_p_roof_kemuridashi', name='Smoke vents (ridge smoke hood, raised ridge vent, irimoya smoke gable)',
    what='How hearth smoke leaves a roof with no chimney: a hood on a thatch ridge, a raised louvred ridge on board/tile roofs, or the open irimoya gable.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='No chimneys; smoke leaves by roof vents and gable openings [PLAYBOOK §6.1]; Morse: triangular latticed opening at the gable [T59]',
    refs=[R('x20_morse_thatch_end', 'smoke hood at a thatch ridge end, Iwaki'), R('x06_suzuki_a', 'small raised vent on a thatch ridge', True), R('x26_morse_farmhouse_kabutoyama', 'farmhouse vent')],
    dimensions={'hood_width_m': D('0.60-0.90', None, 'visual, x20'), 'koshiyane_lift_m': D('0.30-0.45 above the main ridge', None, 'visual, x06'),
                'koshiyane_length_m': D('1.82 (1 ken) or 3.64', None, 'grid choice'), 'irimoya_gable_opening_m': D('triangle 0.9-1.4 wide, lattice 0.03 bars', None, 'assumed')},
    materials=[M('frame, louvres', 'jp_m_wood_weathered', 'timber_weathered'), M('inner soot faces', 'jp_m_wood_sooted', 'timber_sooted'),
               M('covering', 'jp_m_roof_thatch', 'thatch_weathered')],
    connectors=['ridge: placed by the generator at a ridge position over the doma/kamado bay', 'irimoya variant is part of the irimoya roof form'],
    variants=[V('_hood', 'thatch ridge hood', 1), V('_koshiyane', 'raised ridge vent on board/tile roofs (smithy, kitchens)', 2), V('_irimoya', 'latticed triangle in the small gable')],
    banned_tells_to_watch=['chimneys, stove pipes'])

add('Roofs', id='jp_p_roof_hafu', name='Bargeboards and gable edge (hafu-ita, purlin ends)',
    what='The plain boards finishing every gable edge, with the purlin ends that show under the verge.',
    importance='standard', tiers=[1, 2, 3], region='all', status_overlay='commoner', priority='P1',
    period_evidence='Gable rule 5 [PLAYBOOK §6.2]; visible on the dated Ioka and Hirose gables [x01, x08]',
    refs=[R('x01_ioka_a', 'tile gable edge', True), R('x08_hirose_earthwall', 'thatch verge', True), R('x04_misawa_a', 'board-roof verge', True)],
    dimensions={'board_m': D('0.030 x 0.24', None, 'assumed'), 'purlin_end_projection_m': D('0.30', None, 'visual'), 'purlin_section_m': D('0.10 x 0.12', None, 'assumed')},
    materials=[M('boards, purlins', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['verge: follows the verge line from eave to ridge; purlin ends at each purlin (every 0.91 up the slope)'],
    variants=[V('_tile', 'under sode-gawara'), V('_board', 'with a verge batten for shingle/ishioki roofs'), V('_thatch', 'hidden; only purlin ends show under the thatch verge', 1)],
    banned_tells_to_watch=['kengyo (hanging gable ornament) on commoner houses (status)', 'painted boards'])

add('Roofs', id='jp_p_roof_hisashi', name='Pent roofs (hisashi): street pent, board pent, farmhouse board skirt, gable pent',
    what='The light lean-to roofs below the main eave: over the machiya shopfront, over verandas, as the board skirt of thatch houses and along tiled gables.',
    importance='hero', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Sasaki 1731/32: stone-weighted board eaves front and rear of the thatch roof [E02]; Suzuki: board-shingled eaves [E03]; Ioka: pent roofs front and side [E03]; Morse: hisashi of wide thin boards on slender brackets or posts [T59]',
    refs=[R('x29_morse_hisashi', 'board hisashi'), R('x07_sasaki_1985', 'board pent eave under thatch, 1732 house', True), R('x01_ioka_a', 'tiled gable pent', True),
          R('c08_kyomachiya', 'tiled street pent'), R('x33_jinrin_bookseller_1690', 'shop front of 1690 (context)', True)],
    dimensions={
        'projection_m': D('0.91 (half-ken); veranda hisashi to 1.2 on posts', None, 'Morse calls them narrow; grid choice'),
        'street_eave_edge_m': D('2.90-3.20; soffit >=2.20 where walked under', 'PLAYBOOK §4'),
        'pitch': D('tile 4 sun; board 2.5-3 sun; ishioki 3 sun', None, 'assumed'),
        'bracket_udegi_m': D('0.06 x 0.09 arm, from each post (0.91 or 1.82 c/c)', None, 'Morse: slender brackets at right angles to the uprights'),
        'gable_pent_height_m': D('at upper-floor line, 0.45 projection', None, 'visual, x01'),
    },
    materials=[M('tile variant', 'jp_m_roof_kawara', 'kawara_ibushi'), M('board variants', 'jp_m_roof_kureita', 'roof_board_silver'),
               M('brackets, fascia', 'jp_m_wood_weathered', 'timber_weathered'), M('stones (ishioki variant)', 'jp_m_stone_river', 'stone_lantern')],
    connectors=['post: udegi bracket plugs into each post at the pent height', 'eave: pent eave line parallel to the wall', 'top: flashed under the upper wall or main eave'],
    variants=[V('_tile', 'sangawara street pent (T3 machiya)', 3), V('_board', 'thin boards on brackets (Morse)'), V('_ishioki', 'Kiso stone-weighted pent', 2),
              V('_skirt', 'board skirt under a thatch roof, low pitch (Sasaki/Suzuki type)', 2), V('_gable', 'small tiled pent along a gable (Ioka)', 3)],
    banned_tells_to_watch=['metal flashing', 'thick heavy fascia'],
    open_questions=['Decision 6: the _skirt pent is also the period-correct way to keep a thatch house entrance above 2.20 m'])

add('Roofs', id='jp_p_roof_kura_eave', name='Kura plastered eave and wall-head band',
    what='The fire-proof kura eave: rafters and soffit plastered over, with a thick plaster band at the wall head.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Kura as the only tiled building allowed in Edo 1657-1720 [E09]; kura form [T59, c11]',
    refs=[R('x13_morse_kura', 'Tokyo kura'), R('c11_kurashiki', 'Kurashiki kura'), R('x23_morse_kura_door', 'old Kyoto kura')],
    dimensions={'band_height_m': D('0.30-0.45', None, 'visual, c11/x13'), 'band_projection_m': D('0.05-0.10 per step, 2 steps', None, 'visual'), 'eave_overhang_m': D('0.45-0.60', None, 'kura eaves are short; visual')},
    materials=[M('plaster', 'jp_m_wall_shikkui', 'shikkui_white'), M('tiles above', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['eave: sits on the okabe wall top; tile eave course on top'],
    variants=[V('_std', 'plain stepped band'), V('_okiyane', 'separate roof raised on posts above a plastered roof: region/date unverified, P3')],
    open_questions=['Oki-yane (detached kura roof): date and region not checked; do not build before verified'])

add('Roofs', id='jp_p_roof_gutter', name='Bamboo gutter and downpipe',
    what='A split-bamboo half-pipe on hooks along an eave, draining into a bamboo downpipe with a wooden funnel.',
    importance='filler', tiers=[3], region='all', priority='P3',
    period_evidence='Morse fig. 66 (1880s) only; 1730 use assumed',
    refs=[R('x38_morse_gutter', 'bamboo water-conductor with wooden funnel')],
    dimensions={'gutter_diameter_m': D('0.10', None, 'assumed'), 'hook_spacing_m': D('0.91', None, 'grid')},
    materials=[M('bamboo', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('hooks', 'jp_m_metal_iron', 'iron_black')],
    connectors=['eave: hangs 0.05 below the eave edge on hooks at post positions'],
    variants=[V('_std', 'gutter + one downpipe')],
    banned_tells_to_watch=['metal gutters (PLAYBOOK §7)'], checks=['C1', 'C2', 'C4', 'C8'])

# ================================================================= WALLS AND FRAME
add('Walls and frame', id='jp_p_wall_shinkabe', name='Earthen wall between exposed posts (shinkabe), with header panel (kokabe)',
    what='The default house wall recipe: posts and rails visible, earth or plaster infill, generated for any run of half-ken bays.',
    importance='hero', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Hirose late 17th c.: earth infill between exposed posts and rails [x08]; Sasaki 1732 [x07]',
    refs=[R('x08_hirose_earthwall', 'earth panels between posts and rails', True), R('x06_suzuki_a', 'earth panels, board base', True), R('c29_earthen_wall', 'earth colour (sunlit)')],
    dimensions={
        'infill_thickness_m': D('0.075 (0.06 T1 arakabe)', 'PLAYBOOK §6.2'),
        'infill_setback_m': D('0.02 behind the post face, both sides', None, 'posts 0.12, wall 0.075'),
        'panel_max': D('1 ken x 1 storey', 'PLAYBOOK §6.2'),
        'rail_heights_m': D('sill 0 / door head 2.00 / wall plate', 'PLAYBOOK §4'),
        'kokabe_band_m': D('from the 2.00 door head to the beam (0.6-1.1)', 'follows from D2'),
    },
    materials=[M('T1 exterior', 'jp_m_wall_arakabe', 'earth_wall_aged'), M('T2 exterior', 'jp_m_wall_nakanuri', 'earth_wall_aged'),
               M('T3 upper storey', 'jp_m_wall_shikkui', 'shikkui_white'), M('posts, rails', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: panels span between post connectors on any half-ken run', 'sill: bottom on dodai or grade', 'head: door heads at 2.00; above = kokabe', 'eave: top under the keta'],
    variants=[V('_arakabe', 'rough, straw showing', 1), V('_nakanuri', 'smoother, T2', 2), V('_shikkui', 'white lime finish, T3 upper storeys', 3),
              V('_kokabe_ranma', 'header band as a plain lattice transom instead of plaster', 2)],
    deviations=['D2/D6 raise openings; the kokabe band absorbs the difference'],
    banned_tells_to_watch=['pure-white untextured plaster', 'any blank plane > 2 x 2 m', 'bright ochre (see requested palette entry earth_wall_aged)'])

add('Walls and frame', id='jp_p_wall_okabe', name='Thick plastered wall, posts hidden (okabe): kura, nuriya fronts',
    what='Fire-proof walls with the frame buried in plaster: kura, the post-1720 plastered town fronts, udatsu.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Edo encouraged plastered (dozo/nuriya) fronts from 1720 [T05, E09]; kura [c11]',
    refs=[R('c11_kurashiki', 'kura plaster + namako'), R('x13_morse_kura', 'kura in Tokyo'), R('c09_himeji', 'shikkui texture')],
    dimensions={'thickness_m': D('kura 0.24 (0.20-0.30); nuriya front 0.15', 'PLAYBOOK §6.2 (kura); nuriya assumed'), 'corner': D('sharp arris, slight irregularity', None, 'visual')},
    materials=[M('plaster', 'jp_m_wall_shikkui', 'shikkui_white')],
    connectors=['post: wall hides posts but still snaps to post connectors; openings cut on half-ken bays'],
    variants=[V('_kura', '0.24 thick', 2), V('_nuriya', 'Edo plastered townhouse front, 0.15', 3)],
    banned_tells_to_watch=['glowing white: author the mean at <=192, houses default _w1'])

add('Walls and frame', id='jp_p_wall_board_vertical', name='Vertical board cladding (tate-ita-bari) with cover battens',
    what='Vertical boards on posts: Kiso street fronts, nagaya, farmhouse lower walls, gables.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Ioka house (late 17th-early 18th c.) lower walls are vertical dark boards [x01]',
    refs=[R('x01_ioka_a', 'vertical boards on the dated Ioka house', True), R('c02_narai_facade', 'Narai front boards'), R('x04_misawa_a', 'board front', True)],
    dimensions={'board_width_m': D('0.24-0.30 random', None, 'visual'), 'board_thickness_m': D(0.015, None, 'assumed'), 'batten_m': D('0.036 x 0.018 at each joint', None, 'visual')},
    materials=[M('boards', 'jp_m_wood_weathered', 'timber_weathered'), M('town fronts', 'jp_m_wood_street_dark', 'timber_street_dark')],
    connectors=['post: boards fixed to the outer face of posts/rails; runs any half-ken length'],
    variants=[V('_battened', 'with cover battens'), V('_plain', 'butt boards, T1')],
    banned_tells_to_watch=['identical repeated boards (W8)', 'perfectly straight new timber'])

add('Walls and frame', id='jp_p_wall_shitami', name='Lapped horizontal boards with battens (shitami-ita-bari)',
    what='Horizontal overlapping boards held by vertical battens: lower walls and gables in T2-3.',
    importance='standard', tiers=[2, 3], region='all', priority='P2',
    period_evidence='Widely used through the Edo period (black form on official buildings [c16]); unpainted on houses (assumed)',
    refs=[R('c16_hakone_sekisho', 'black shitami (official form)'), R('x05_misawa_b', 'board walls, museum', True)],
    dimensions={'exposure_m': D('0.20', None, 'assumed'), 'lap_m': D('0.025', None, 'assumed'), 'batten_spacing_m': D('0.455 (ken/4)', None, 'grid')},
    materials=[M('boards', 'jp_m_wood_street_dark', 'timber_street_dark'), M('kura variant', 'jp_m_wood_kuro', 'kuro_board')],
    connectors=['post: as board cladding'],
    variants=[V('_house', 'unpainted/dark weathered'), V('_kura', 'black-stained, kura only (restricted colour)', 3)],
    banned_tells_to_watch=['kuro_board on ordinary houses (restricted: official, kura)'])

add('Walls and frame', id='jp_p_wall_koshiita', name='Board wainscot on earth walls (koshi-ita)',
    what='A band of boards protecting the bottom of earth and plaster walls from splash.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Board lower panels on the Hirose (late 17th c.) and Suzuki houses [x08, x06]',
    refs=[R('x08_hirose_earthwall', 'board lower panels', True), R('x06_suzuki_a', 'board base', True)],
    dimensions={'height_m': D('0.60 or 0.90', 'PLAYBOOK §6.2'), 'drip_cap_m': D('0.02 x 0.04 top rail', None, 'assumed')},
    materials=[M('boards', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: between posts, bottom at sill'],
    variants=[V('_h060', '0.60 high'), V('_h090', '0.90 high')])

add('Walls and frame', id='jp_p_wall_namako', name='Namako tile wall (namako-kabe)',
    what='Square dark tiles with raised half-round white plaster joints on kura lower walls.',
    importance='standard', tiers=[2, 3], region='all', priority='P2',
    period_evidence='Appears from the Edo period; imo-bari (grid) is the oldest laying, shihan-bari (diagonal) the most widespread [E15]',
    refs=[R('c11_kurashiki', 'namako on a kura'), R('x12_morse_namako', 'square tiles on the side of a house')],
    dimensions={'tile_side_m': D(0.2145, None, 'about 7 sun; chosen so the diagonal (0.303) gives 3 per half-ken'), 'joint_width_m': D('0.035', None, 'visual, c11'),
                'joint_relief_m': D('0.02', None, 'half-round'), 'height_m': D('0.9-1.8 (kura lower wall)', None, 'visual, c11')},
    materials=[M('tiles', 'jp_m_wall_namako_tile', 'namako_tile'), M('joints', 'jp_m_wall_shikkui', 'shikkui_white')],
    connectors=['post: on okabe walls, bottom on the kura footing'],
    variants=[V('_imo', 'square grid (oldest form)'), V('_shihan', 'diagonal (most common)')],
    banned_tells_to_watch=['flat texture only: joints are geometry at LOD0'])

add('Walls and frame', id='jp_p_wall_gable', name='Gable end: frame, infill and vent (rule 5)',
    what='Every gable built up from exposed posts, ties and panels, with the right infill for its roof family.',
    importance='hero', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Hirose (late 17th c.) thatch gable [x08]; Ioka tile gable with pent roof [x01]',
    refs=[R('x08_hirose_earthwall', 'thatch gable frame', True), R('x01_ioka_a', 'tile gable: plaster above, boards below', True), R('x36_hiroshige_ishibe', 'tea house gable frame', True)],
    dimensions={'panel_max': D('1 ken x 1 storey', 'PLAYBOOK §6.2'), 'tie_beam_m': D('0.12 x 0.21', None, 'assumed'), 'vent_m': D('0.6-0.9 wide, lattice 0.03', None, 'assumed')},
    materials=[M('frame', 'jp_m_wood_weathered', 'timber_weathered'), M('T1 infill', 'jp_m_wall_arakabe', 'earth_wall_aged'),
               M('T3 infill', 'jp_m_wall_shikkui', 'shikkui_white'), M('board infill', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: gable posts on the ken grid up to the ridge post', 'verge: meets jp_p_roof_hafu', 'eave: sits on the end tie beam'],
    variants=[V('_thatch', 'earth panels, thick thatch verge (Hirose)', 1), V('_tile', 'plaster above the pent, boards below (Ioka)', 3), V('_board', 'all boards (Kiso)', 2), V('_kura', 'plain okabe, small vent', 2)],
    banned_tells_to_watch=['a flat plain gable (machiya v1 mistake)'])

add('Walls and frame', id='jp_p_wall_udatsu', name='Udatsu fire wing walls (sode-udatsu, hon-udatsu)',
    what='Plastered wing walls with a small tile cap between adjoining town houses.',
    importance='standard', tiers=[3], region='kamigata', status_overlay='commoner', priority='P2',
    period_evidence='Mid-Edo onward the udatsu became mainly decorative (a wealth sign) [E04]; T08',
    refs=[R('x09_udatsu_mino', 'Mino udatsu street (late Edo/Meiji buildings; form only)'), R('c07_gion_machiya', 'Kyoto machiya front')],
    dimensions={'projection_m': D('0.45-0.60 beyond the facade', None, 'visual, x09'), 'thickness_m': D('0.18', None, 'assumed'),
                'height': D('sode: from the ground-floor pent to the upper eave (1.3-1.6); hon: 0.3-0.5 above the roof plane', None, 'E04 describes the forms; heights assumed'),
                'cap_width_m': D('0.30-0.35 tile cap', None, 'assumed')},
    materials=[M('plaster', 'jp_m_wall_shikkui', 'shikkui_white'), M('cap', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['post: on the party-wall post line at the facade', 'eave: bottom on the ground-floor pent, top under the main eave'],
    variants=[V('_sode', 'wing wall at the upper storey (default)'), V('_hon', 'parapet on the gable with its own roof (rich, P3)')])

add('Walls and frame', id='jp_p_frame_post', name='Exterior posts',
    what='Corner and wall posts that the walls, doors and pents all snap to.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Kitamura 1687: adze-marked posts between the main room and doma [E01]; post sizes [T46]',
    refs=[R('x08_hirose_earthwall', 'irregular farmhouse posts', True), R('c02_narai_facade', 'town posts')],
    dimensions={'section_m': D('0.120 (T2-3); 0.150 farmhouse main posts', 'PLAYBOOK §4 [T46]'), 'position': D('centred on grid nodes', 'PLAYBOOK §4')},
    materials=[M('posts', 'jp_m_wood_weathered', 'timber_weathered'), M('town fronts', 'jp_m_wood_street_dark', 'timber_street_dark')],
    connectors=['post: the grid node itself; bottom on soseki or dodai'],
    variants=[V('_planed', 'straight, T2-3'), V('_adzed', 'adze facets, slight irregularity (Kitamura)', 1)],
    banned_tells_to_watch=['perfectly straight new timber on old buildings'])

add('Walls and frame', id='jp_p_frame_beam', name='Exposed beams and rails (keta, hari ends, nuki, dodai)',
    what='The horizontal members visible outside: wall plates, beam ends at gables, rails and sills.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='as jp_p_wall_gable',
    refs=[R('x11_morse_frame_2storey', 'frame of an ordinary two-storey house (from a Japanese drawing)'), R('x08_hirose_earthwall', 'rails and beam ends', True)],
    dimensions={'keta_m': D('0.12 x 0.18', None, 'assumed'), 'nuki_m': D('0.03 x 0.105', None, 'assumed'), 'dodai_m': D('0.12 x 0.12', None, 'equal to the post'), 'hari_end_projection_m': D('0.15-0.25', None, 'visual')},
    materials=[M('timber', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: members span post to post; beam ends project at gables'],
    variants=[V('_sawn', 'sawn'), V('_log', 'log beam ends (farmhouse)', 1)])

add('Walls and frame', id='jp_p_frame_dashigeta', name='Cantilevered eave purlin (dashigeta) / projecting upper floor',
    what='Arms from the posts carrying a purlin that holds a deep street eave; Edo shop fronts and Kiso post towns.',
    importance='standard', tiers=[2, 3], region='edo', priority='P3',
    period_evidence='Surviving examples are late Edo (Kagiya 1856); the form spread in Edo shops from late Edo [E11]. NOT verified for 1730',
    refs=[R('c01_narai_street', 'Narai: projecting upper fronts (late Edo buildings)')],
    dimensions={'cantilever_m': D('0.45-0.90', None, 'assumed')},
    materials=[M('timber', 'jp_m_wood_street_dark', 'timber_street_dark')],
    connectors=['post: arms plug into the front posts at the upper floor line'],
    variants=[V('_std', 'dashigeta arm + purlin')],
    open_questions=['Decision 4: build only if a pre-1750 source is found or Stephen accepts it as a deviation'])

# ================================================================= OPENINGS
DOOR_NOTES = 'translation door, one bone per leaf, memory axis exactly 1.00 m, doorWoodSlide sounds (PLAYBOOK §6.3)'
add('Openings', id='jp_p_open_itado', name='Plank sliding door (itado), incl. oodo with wicket',
    what='The exterior plank door of every tier; the main entrance is one wide leaf sliding along the outside of the next bay.',
    importance='hero', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='T1 doors are plank itado [PLAYBOOK §2.1]; shop fronts of 1690 [x33]',
    refs=[R('x04_misawa_a', 'plank doors on a post-town house', True), R('c02_narai_facade', 'town plank doors'), R('x33_jinrin_bookseller_1690', 'open shop front 1690', True)],
    dimensions={'bay': D('1 half-ken leaf; main entrance: one leaf on a 1.5-ken opening, >=1.00 clear', 'PLAYBOOK §6.3, D1'),
                'head_m': D(2.00, 'D2'), 'leaf_thickness_m': D('frame 0.033, boards 0.012', None, 'assumed'), 'battens': D('3-5 horizontal', None, 'visual'),
                'kuguri_m': D('0.60 x 1.20 decorative wicket', 'D9')},
    materials=[M('leaf', 'jp_m_wood_weathered', 'timber_weathered'), M('town leaf', 'jp_m_wood_street_dark', 'timber_street_dark'), M('fittings', 'jp_m_metal_iron', 'iron_black')],
    connectors=['post: between post connectors, 0.5/1/1.5/2 ken', 'sill: runs in a grooved sill at floor level', 'head: 2.00'],
    variants=[V('_plain', 'boards only', 1), V('_battened', 'frame + battens', 2), V('_oodo', 'big leaf with a decorative kuguri wicket (D9)', 2), V('_pair', 'two leaves in a 1-ken bay')],
    deviations=['D1', 'D2', 'D9'], banned_tells_to_watch=['hinged doors, knobs, butt hinges'],
    open_questions=['Engine: ' + DOOR_NOTES])

add('Openings', id='jp_p_open_koshido', name='Lattice sliding door (koshi-do)',
    what='A day door of vertical bars used at T2-3 entrances behind the itado.',
    importance='standard', tiers=[2, 3], region='all', priority='P2',
    period_evidence='Koshi fronts on hatago and machiya [T30, E10]',
    refs=[R('c07_gion_machiya', 'lattice door, Kyoto'), R('c02_narai_facade', 'lattice, Narai')],
    dimensions={'bar_face_m': D(0.03, 'E16 (1 sun face)'), 'bar_gap_m': D(0.03, None, 'assumed'), 'lower_board_m': D(0.30, None, 'assumed'), 'head_m': D(2.00, 'D2')},
    materials=[M('lattice', 'jp_m_wood_street_dark', 'timber_street_dark')],
    connectors=['post/sill/head as jp_p_open_itado'],
    variants=[V('_open', 'bars only'), V('_papered', 'paper behind the bars')],
    open_questions=['Engine: ' + DOOR_NOTES + '; Fire Geometry wood'])

add('Openings', id='jp_p_open_shoji_ext', name='Exterior paper doors (koshidaka-shoji, akari-shoji)',
    what='Paper sliding doors facing outside: the board-bottomed door of nagaya and doma entrances, and the shoji line behind amado.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Shoji at T2-3 [PLAYBOOK §2.1]; paper shop doors in 1830s road prints [x35]',
    refs=[R('x35_hiroshige_goyu', 'inn fronts with shoji and lattice (c.1833)', True), R('x28_morse_inn_mishima', 'inn front, 1880s'), R('x07_sasaki_1985', 'shoji behind the eave, 1732 house', True)],
    dimensions={'lower_board_m': D('koshidaka 0.60; akari 0.15', None, 'assumed'), 'kumiko_m': D('3 verticals per leaf, horizontals at 0.25', None, 'assumed'), 'head_m': D(2.00, 'D2')},
    materials=[M('paper', 'jp_m_paper_shoji', 'washi_shoji'), M('frame', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post/sill/head as jp_p_open_itado'],
    variants=[V('_koshidaka', 'board-bottomed door (nagaya, doma)', 1), V('_akari', 'plain shoji behind amado', 2)],
    banned_tells_to_watch=['glass panes', 'pure white paper'],
    open_questions=['Engine: ' + DOOR_NOTES + '; Fire Geometry fabric_thin (bullets pass)'])

add('Openings', id='jp_p_open_amado', name='Storm shutters (amado)',
    what='Thin board shutters on one outer track that close a veranda or window line at night.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Amado from 1587 (Jurakudai) [E07]',
    refs=[R('x25_morse_amado_box', 'veranda with the rain-door closet'), R('x07_sasaki_1985', 'closed facade, 1732 house', True)],
    dimensions={'leaf_m': D('0.91 wide x door head', 'half-ken bay (PLAYBOOK §6.3)'), 'board_m': D('0.009 boards on a light frame with a few bars', 'Morse [T59] (thickness assumed)'),
                'track': D('single groove on the outer edge of the veranda', 'Morse [T59]')},
    materials=[M('leaf', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['sill: outer groove of jp_p_porch_engawa', 'head: 2.00 under a small transom band', 'stows into jp_p_open_tobukuro at one end'],
    variants=[V('_stowed', 'static: all leaves in the box (default)'), V('_closed', 'static closed line (abandoned houses; blocks the opening)')],
    open_questions=['Gameplay: amado are static, not doors (a run of 6-10 leaves would be 6-10 door bones)'])

add('Openings', id='jp_p_open_tobukuro', name='Shutter box (tobukuro)',
    what='The board box at the end of an amado run that holds the stowed leaves.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Box types named with amado [E07]; Morse swinging closet [x25] (1880s)',
    refs=[R('x25_morse_amado_box', 'rain-door closet')],
    dimensions={'inner_width_m': D('leaf + 0.05', None, 'assumed'), 'depth_m': D('n leaves x 0.03 + 0.05', None, 'assumed'), 'height_m': D('leaf + 0.10', None, 'assumed')},
    materials=[M('box', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: outside the end post of the run, on the veranda edge line'],
    variants=[V('_box', 'covered box (to-bako)'), V('_swing', 'Morse swinging closet, P3')])

add('Openings', id='jp_p_open_kura_door', name='Kura doors (hinged plastered doors + inner sliding doors)',
    what='The only hinged doors: thick stepped plaster leaves, an inner lattice/board sliding door and a small pent roof above.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Kura doors [PLAYBOOK §6.3]; old Kyoto kura doorway [x23] (1880s drawing of an old kura)',
    refs=[R('x23_morse_kura_door', 'open hinged leaves, inner lattice, pent roof'), R('c11_kurashiki', 'kura doors')],
    dimensions={'clear_m': D('>=1.00 x 2.00', 'D1, D2'), 'leaf_thickness_m': D('0.15-0.20', None, 'visual, x23'), 'jamb_steps': D('3-5 steps of 0.03-0.04', None, 'visual'),
                'door_pent_m': D('0.60 deep on 2 brackets', None, 'visual, x23')},
    materials=[M('leaves, jambs', 'jp_m_wall_shikkui', 'shikkui_white'), M('inner doors', 'jp_m_wood_weathered', 'timber_weathered'), M('hinges, hasp', 'jp_m_metal_iron', 'iron_black'), M('pent', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['post: centred on a 1-ken bay of an okabe wall', 'sill: raised stone threshold 0.15'],
    variants=[V('_open', 'outer leaves static open; inner sliding door is the game door (P1)'), V('_hinged', 'outer leaves as rotation doors (P2, engine test)')],
    open_questions=['Engine: hinged rotation doors are untested in this kit'])

add('Openings', id='jp_p_open_kura_window', name='Kura window (barred, plaster shutters, tiny pent)',
    what='Small barred kura window with thick plaster shutters and a mini tile pent.',
    importance='standard', tiers=[2, 3], region='all', priority='P2',
    period_evidence='as kura',
    refs=[R('x13_morse_kura', 'kura windows'), R('c11_kurashiki', 'kura windows')],
    dimensions={'opening_m': D('0.60 x 0.75', None, 'assumed'), 'bars_m': D('0.03 at 0.09', None, 'assumed'), 'shutter_thickness_m': D(0.12, None, 'assumed')},
    materials=[M('shutters', 'jp_m_wall_shikkui', 'shikkui_white'), M('bars', 'jp_m_metal_iron', 'iron_black'), M('pent', 'jp_m_roof_kawara', 'kawara_ibushi')],
    connectors=['post: centred in a half-ken or 1-ken bay; sill at 1.2 (ground) or 0.6 (upper)'],
    variants=[V('_slide', 'sliding plaster shutter'), V('_hinged', 'pair of hinged shutters (static open)')])

add('Openings', id='jp_p_open_mushiko', name='Mushiko window, 1730 form (small oval)',
    what='The plastered slatted window of the low upper storey of Kamigata machiya; in 1730 small and oval, not the later rectangle.',
    importance='hero', tiers=[3], region='kamigata', priority='P1',
    period_evidence='Early mushiko-mado were small and oval; they became larger and rectangular in the Meiji period [E05]; standard on 18th c. Kyoto machiya [E10]',
    refs=[R('c08_kyomachiya', 'mushiko construction (later rectangular form: slats and plaster only)'), R('c07_gion_machiya', 'low upper storey')],
    dimensions={'opening_m': D('0.90 wide x 0.45 high, round ends', None, 'E05 says small and oval; size assumed to fit a half-ken bay and the <=1.30 street wall'),
                'slat_face_m': D(0.045, None, 'assumed'), 'slat_gap_m': D(0.045, None, 'assumed'), 'depth_m': D('wall thickness 0.15', None, 'okabe'),
                'placement': D('upper street wall, sill 0.40 above the upper floor', None, 'fits PLAYBOOK D3 street wall <=1.30')},
    materials=[M('plaster', 'jp_m_wall_shikkui', 'shikkui_white')],
    connectors=['post: centred on a half-ken bay of the upper okabe front; 1 per 1-2 bays'],
    variants=[V('_oval', 'single oval'), V('_oval_pair', 'two ovals in one 1-ken bay')],
    banned_tells_to_watch=['large rectangular mushiko (Meiji form)', 'see-through: View Geometry closed, Fire Geometry dirt'])

add('Openings', id='jp_p_open_koshi', name='Koshi lattice fronts and windows (incl. de-goshi)',
    what='Wooden lattice modules for street fronts and windows, with trade variants and the projecting de-goshi.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='De-goshi part of the 18th c. standard Kyoto front [E10]; lattice fronts on hatago [T30]',
    refs=[R('c07_gion_machiya', 'bengara koshi'), R('c08_kyomachiya', 'koshi front'), R('c02_narai_facade', 'Narai lattice'), R('x35_hiroshige_goyu', 'inn lattice fronts (c.1833)', True)],
    dimensions={'module_widths': D('0.5 / 1 / 1.5 / 2 ken', 'PLAYBOOK §10.2'), 'bar_face_m': D(0.03, 'E16'), 'bar_depth_m': D(0.05, None, 'assumed'),
                'degoshi_projection_m': D(0.30, None, 'about 1 shaku; assumed'), 'oyako_cut_gap_m': D('children stop 0.30 below the head rail', None, 'E16 describes cut-top children; gap assumed'),
                'sill_m': D('on koshi-ita or plinth at 0.45; head 2.00', None, 'assumed / D2')},
    materials=[M('lattice', 'jp_m_wood_street_dark', 'timber_street_dark'), M('Kamigata finish', 'jp_m_wood_bengara', 'bengara_lattice')],
    connectors=['post: between post connectors', 'sill: own sill rail on the dodai or a board base', 'head: 2.00 rail'],
    variants=[V('_kyo', 'fine bars, few rails'), V('_oyako', 'parent bars + cut-top children (cloth/thread shops)', 3), V('_komeya', 'thick bars (rice, charcoal)', 2),
              V('_degoshi', 'projecting lattice on its own sill', 3), V('_bengara', 'bengara finish (Kamigata, sparingly)', 3)],
    banned_tells_to_watch=['bengara outside Kamigata T2-3', 'glass behind the lattice'])

add('Openings', id='jp_p_open_renji', name='Barred and slatted windows (renji-mado, muso-mado)',
    what='Plain barred windows with a sliding board shutter; the everyday window of farmhouses and kitchens.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Lattice windows on the Ito house (late 17th-early 18th c.) [E01]; renji-mado for rural T1 [PLAYBOOK §2.1]',
    refs=[R('x07_sasaki_1985', 'lattice window, 1732 house', True), R('x04_misawa_a', 'lattice window', True), R('x26_morse_farmhouse_kabutoyama', 'farmhouse windows')],
    dimensions={'opening_m': D('0.91 x 0.60-0.90', None, 'grid + assumed'), 'sill_m': D(0.90, None, 'assumed'), 'bars_m': D('bamboo d 0.028 or wood 0.03 square at 0.08 c/c', None, 'assumed'),
                'muso_slat_m': D('0.045 slats, 0.045 gaps, one panel slides', None, 'assumed; period of muso-mado not verified')},
    materials=[M('bars', 'jp_m_bamboo_weathered', 'bamboo_weathered'), M('frame, shutter', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: half-ken or 1-ken bay; the shutter slides inside the wall line'],
    variants=[V('_bamboo', 'bamboo bars', 1), V('_wood', 'square wood bars', 2), V('_muso', 'double slatted panels (kitchens; date unverified)', 2)])

add('Openings', id='jp_p_open_suriagedo', name='Vertical-sliding shop shutters (suriage-do / agedo)',
    what='The night closure of an open shop front: stacked boards that slide up in post grooves into a box behind the upper beam.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Standard through the Edo period to mid-Meiji (Seki-juku) [E12]; agedo on the Suzuki house front [E03]; Inoue house, Kurashiki (1721 renovation) has shitomi and suriage shutters [E13]',
    refs=[R('x06_suzuki_a', 'Suzuki house (agedo front)', True), R('x33_jinrin_bookseller_1690', 'fully open shop front of 1690', True), R('x37_eisen_narai', 'open post-town shop front c.1835', True)],
    dimensions={'boards': D('3 per opening, each ~0.68 high (2.04 / 3)', 'E12 (3 boards); height derived from D2'), 'bay': D('1 ken per stack', None, 'grid'),
                'storage': D('box behind the upper beam inside, occupying the upper front wall', 'E12'), 'groove_m': D('0.03 wide in the posts', None, 'assumed')},
    materials=[M('boards', 'jp_m_wood_street_dark', 'timber_street_dark'), M('box', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: grooves in the two posts of a 1-ken bay', 'head: stack top under the 2.00 beam; box above it inside'],
    variants=[V('_closed', 'static closed'), V('_part', 'static, one board lowered'), V('_door', 'animated: whole stack as one leaf, vertical translation (engine test)')],
    open_questions=['Engine: a vertical translation door is untested; fall back to static states'])

add('Openings', id='jp_p_open_shitomido', name='Hinged-up shop shutter (shitomido)',
    what='Kamigata shop closure: an upper panel hinged at the top and hooked up by day, a lower panel lifted out.',
    importance='standard', tiers=[3], region='kamigata', priority='P2',
    period_evidence='Inoue house, Kurashiki (1721 renovation) has shitomido [E13]; upper panel larger than the lower [E08]',
    refs=[R('c08_kyomachiya', 'Kyoto machiya front (context)'), R('x33_jinrin_bookseller_1690', 'open shop front, 1690', True)],
    dimensions={'bay': D('1 ken', None, 'grid'), 'upper_panel_m': D('1.1 high', None, 'E08 says upper larger; value assumed'), 'lower_panel_m': D('0.8 high', None, 'assumed'),
                'panel_build': D('lattice with boards behind', 'E08')},
    materials=[M('panels', 'jp_m_wood_street_dark', 'timber_street_dark'), M('hooks', 'jp_m_metal_iron', 'iron_black')],
    connectors=['post: between the posts of a 1-ken bay; hinge at the 2.00 head rail'],
    variants=[V('_up', 'static: upper hooked up under the pent, lower removed'), V('_closed', 'static closed')])

add('Openings', id='jp_p_open_battari', name='Fold-down shop bench (battari-shogi)',
    what='A bench hinged to the Kamigata shop front, folded up at night.',
    importance='filler', tiers=[2, 3], region='kamigata', priority='P2',
    period_evidence='Kamigata signature detail [PLAYBOOK §3]; no pre-1750 image found',
    refs=[R('c07_gion_machiya', 'Kyoto front (context only)')],
    dimensions={'size_m': D('1.82 x 0.50, seat 0.42', None, 'assumed')},
    materials=[M('boards', 'jp_m_wood_street_dark', 'timber_street_dark')],
    connectors=['post: hinged on the facade between two posts, under a lattice window'],
    variants=[V('_down', 'static down'), V('_up', 'static folded')],
    open_questions=['Catalogue lists it as street furniture (S); moved to the shell because it hinges on the facade. First date unverified'])

add('Openings', id='jp_p_open_upper_rail', name='Upper-floor front rail (tesuri) for inns and tea houses',
    what='A low plain wooden rail along an upper-floor opening or veranda of an inn or tea house.',
    importance='standard', tiers=[2, 3], region='all', priority='P2',
    period_evidence='Railed tea-house rooms in prints of 1726 and c.1748 [x30, x31]',
    refs=[R('x30_shinagawa_1726', 'railed room open to the sea, Shinagawa 1726', True), R('x31_masanobu_ryogoku_1748', 'railed riverside room c.1748', True), R('x35_hiroshige_goyu', 'inn upper front (c.1833)', True)],
    dimensions={'rail_height_m': D('0.60 visible', None, 'sitting height; assumed'), 'baluster_m': D('0.03 square at 0.12', None, 'assumed'), 'geometry_blocker_m': D('1.00', None, 'reason: fall protection in Geometry only')},
    materials=[M('rail', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['post: between upper-floor posts at the upper floor level'],
    variants=[V('_plain', 'plain verticals')],
    banned_tells_to_watch=['Western turned balusters, balconies'],
    open_questions=['Decision 5: full-height upper storeys on T2 hatago'])

add('Openings', id='jp_p_open_mushiro', name='Hung straw mat door (mushiro, rolled up)',
    what='The poorest doorway closure: a straw mat hung over an opening, shown rolled up.',
    importance='filler', tiers=[1], region='rural', priority='P3',
    period_evidence='T1 doors include hung mushiro [PLAYBOOK §2.1]',
    refs=[R('c18_hiroshige_mariko', 'poor roadside house (c.1833)', True)],
    dimensions={'roll_m': D('d 0.15 x 0.91-1.82', None, 'assumed')},
    materials=[M('mat', 'jp_m_straw_mushiro', 'thatch_new')],
    connectors=['head: hangs from the head rail above an open bay; no collision'],
    variants=[V('_rolled', 'rolled up, static')], checks=['C1', 'C2', 'C4'])

# ================================================================= FOUNDATIONS AND OTHER
add('Foundations and other', id='jp_p_found_soseki', name='Foundation stones (soseki, ishiba-date)',
    what='Individual rounded field stones under each post of rural houses and verandas.',
    importance='hero', tiers=[1, 2], region='all', priority='P1',
    period_evidence='Rural posts on single stones [PLAYBOOK §6.4]; Morse foundation stone [x10]',
    refs=[R('x10_morse_foundation_stone', 'post on a foundation stone'), R('x08_hirose_earthwall', 'farmhouse base', True), R('x06_suzuki_a', 'stone base', True)],
    dimensions={'stone_m': D('0.30-0.50 across, 0.15-0.30 tall', None, 'assumed'), 'exposed_m': D('0.05-0.20', 'PLAYBOOK §6.4'), 'shapes': D('8 distinct', None, 'W8 variety')},
    materials=[M('stone', 'jp_m_stone_field', 'stone_granite')],
    connectors=['post: one per post node, top at post base; buried to grade - exposed height'],
    variants=[V('_set8', '8 shapes'), V('_mossy', 'north-side moss (W6)')],
    banned_tells_to_watch=['continuous smooth plinth (rule 3)', 'cement mortar'])

add('Foundations and other', id='jp_p_found_dodai_stones', name='Sill on a course of individual stones (dodai + ishi)',
    what='Town-house base: a timber sill on a low course of separate cut stones with irregular joints.',
    importance='hero', tiers=[2, 3], region='all', priority='P1',
    period_evidence='PLAYBOOK §6.4 (rule 3); Ioka base [x01]',
    refs=[R('x01_ioka_a', 'sill line of the dated Ioka house', True), R('c02_narai_facade', 'town base'), R('c08_kyomachiya', 'machiya base')],
    dimensions={'stone_m': D('0.30-0.60 long x 0.25-0.35 deep; 0.10-0.20 showing', None, 'assumed'), 'joint_m': D('0.005-0.02 irregular', None, 'assumed'), 'sill_m': D('0.12 x 0.12', 'PLAYBOOK §4')},
    materials=[M('stones', 'jp_m_stone_cut', 'stone_granite'), M('sill', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['sill: dodai top = finished grade + stone height; posts stand on it', 'runs any half-ken length; stone joints never align with posts on purpose'],
    variants=[V('_rough', 'roughly dressed, T2', 2), V('_dressed', 'better dressed, T3', 3)],
    banned_tells_to_watch=['continuous smooth plinth', 'uniform block courses'])

add('Foundations and other', id='jp_p_found_kura_footing', name='Kura footing course (cut granite)',
    what='The 0.3-0.6 m cut-stone footing under kura walls, in individual blocks.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='PLAYBOOK §6.4',
    refs=[R('c11_kurashiki', 'kura footing'), R('x13_morse_kura', 'kura base')],
    dimensions={'height_m': D('0.30-0.60 (1-2 courses)', 'PLAYBOOK §6.4'), 'block_m': D('0.6-0.9 long', None, 'assumed'), 'projection_m': D('0.05-0.10 beyond the wall', None, 'assumed')},
    materials=[M('stone', 'jp_m_stone_cut', 'stone_granite')],
    connectors=['sill: under the okabe wall; grade to wall bottom'],
    variants=[V('_c1', 'one course'), V('_c2', 'two courses')])

add('Foundations and other', id='jp_p_found_yukashita', name='Under-floor zone (raised floor gap, tsuka posts)',
    what='The dark ventilated gap under raised floors and verandas, open or closed by boards.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='Raised floors on short posts over small stones [PLAYBOOK §6.4, T17]',
    refs=[R('x07_sasaki_1985', 'raised floor edge, 1732 house', True), R('x04_misawa_a', 'raised front', True)],
    dimensions={'floor_m': D('+0.50 above grade (doma +0.05, step +0.45)', 'PLAYBOOK §4'), 'tsuka_m': D('0.09 square on small stones at 0.91', None, 'assumed')},
    materials=[M('posts, boards', 'jp_m_wood_weathered', 'timber_weathered'), M('stones', 'jp_m_stone_field', 'stone_granite')],
    connectors=['floor: under every raised-floor edge that faces outside'],
    variants=[V('_open', 'open dark gap (T1-2, verandas)'), V('_boarded', 'vertical boards with vent gaps (T2-3)')])

add('Foundations and other', id='jp_p_found_step', name='Entrance stones and steps (kutsunugi-ishi, threshold stone, veranda step)',
    what='The stones and steps at doors and verandas that also hide the walk ramps.',
    importance='standard', tiers=[1, 2, 3], region='all', priority='P1',
    period_evidence='B spike; Morse steps to verandah (fig. 179)',
    refs=[R('x04_misawa_a', 'entrance stones', True), R('x25_morse_amado_box', 'veranda edge')],
    dimensions={'kutsunugi_m': D('0.60 x 0.40 x 0.15-0.20', 'B spike'), 'step_rise_m': D('0.15-0.18', None, 'assumed'), 'tread_m': D('0.30-0.40', None, 'assumed'), 'ramp_deg': D('<=34 hidden under the stone', 'PLAYBOOK §4')},
    materials=[M('stone', 'jp_m_stone_field', 'stone_granite'), M('cut stone', 'jp_m_stone_cut', 'stone_granite'), M('wood step', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['sill: at door sills and veranda edges; ramp in Geometry/Roadway'],
    variants=[V('_natural', 'natural slab'), V('_cut', 'cut slab', 3), V('_wood', 'wooden step box at a veranda')],
    banned_tells_to_watch=['poured-looking steps'])

add('Foundations and other', id='jp_p_porch_engawa', name='Veranda (engawa)',
    what='The raised board veranda along garden and yard sides of better houses, closed by amado.',
    importance='standard', tiers=[2, 3], region='all', priority='P1',
    period_evidence='Engawa on T2-3 [PLAYBOOK §10.3]; railed tea-house engawa in 1726 and c.1748 prints [x30, x31]',
    refs=[R('x25_morse_amado_box', 'veranda + rain-door closet'), R('x30_shinagawa_1726', 'tea-house engawa, 1726', True), R('x07_sasaki_1985', 'veranda line, 1732 house', True)],
    dimensions={'width_clear_m': D('>=1.00 (1.00-1.20)', 'PLAYBOOK §4 (reason)'), 'height_m': D(0.50, 'PLAYBOOK §4'), 'edge_beam_m': D('0.09 x 0.15', None, 'assumed'),
                'boards': D('kure-en: boards along the wall inside the amado line; kiri-en: boards across, exposed', None, 'assumed from common practice')},
    materials=[M('boards', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['floor: level ID of the raised floor', 'post: veranda posts on the outer line carry the eave or hisashi (Morse)', 'outer edge carries the amado groove'],
    variants=[V('_kure', 'lengthwise boards, inside the amado', 2), V('_kiri', 'crosswise boards, exposed', 2)],
    deviations=['D5 (>=1.00 clear)'])

add('Foundations and other', id='jp_p_porch_nureen', name='Open deck (nure-en)',
    what='A narrow unroofed board deck outside a room.',
    importance='filler', tiers=[1, 2, 3], region='all', priority='P3',
    period_evidence='assumed common; no dated source gathered',
    refs=[R('x25_morse_amado_box', 'veranda boards')],
    dimensions={'width_m': D('0.45-0.60', None, 'assumed'), 'height_m': D(0.45, None, 'assumed')},
    materials=[M('boards', 'jp_m_wood_weathered', 'timber_weathered')],
    connectors=['floor: against a raised-floor edge'],
    variants=[V('_std', 'plain')], checks=['C1', 'C2', 'C3', 'C4'])

# ------------------------------------------------------------------------------------------------ materials
MAT = {
 'jp_m_wood_weathered': dict(family='wood', palette='timber_weathered', tile=2.0, ppm=512, grain='along member', pen='wood',
     wear=('warm brown, crisp grain', 'sun faces silvering (W3), grime band (W1)', 'grey toward stone_lantern (max 0.35), splits, heavy grime'), note='the default exterior timber'),
 'jp_m_wood_street_dark': dict(family='wood', palette='timber_street_dark', tile=2.0, ppm=512, grain='along member', pen='wood',
     wear=('oiled dark brown', 'edge wear on lattice corners (W7)', 'dusty, raised grain, pale edge wear'), note='town fronts, lattice, shop shutters'),
 'jp_m_wood_bengara': dict(family='paint', palette='bengara_lattice', tile=2.0, ppm=512, grain='along member', pen='wood',
     wear=('even red-brown', 'worn to wood on edges', 'patchy, wood showing'), note='RESTRICTED: Kamigata T2-3 lattice, sparingly'),
 'jp_m_wood_kuro': dict(family='wood', palette='kuro_board', tile=2.0, ppm=512, grain='along member', pen='wood',
     wear=('matte black', 'grey bloom', 'grey, wood showing on edges'), note='RESTRICTED: kura lower boards only in this list'),
 'jp_m_wood_sooted': dict(family='wood', palette='timber_sooted', tile=2.0, ppm=512, grain='along member', pen='wood',
     wear=('dark brown-black, albedo >=30', 'soot streaks', 'crusted soot'), note='inside smoke vents; exterior soot halo = weathering'),
 'jp_m_wall_arakabe': dict(family='wall', palette='earth_wall_aged', tile=2.0, ppm=512, grain='none; straw flecks', pen='dirt',
     wear=('fresh clay, straw visible', 'rain streaks (W2), splash band (W1)', 'eroded, straw and lath showing in patches'), note='T1 exterior earth; NEW palette entry requested'),
 'jp_m_wall_nakanuri': dict(family='wall', palette='earth_wall_aged', tile=2.0, ppm=512, grain='none; fine trowel marks', pen='dirt',
     wear=('smooth clay', 'streaks, splash', 'cracks, patched areas'), note='T2 exterior earth; fallback palette earth_wall_ochre if the new entry is refused'),
 'jp_m_wall_shikkui': dict(family='wall', palette='shikkui_white', tile=2.0, ppm=512, grain='none; trowel', pen='dirt',
     wear=('clean lime, mean <=192 (never 217)', 'default on houses: grey streaks under eaves and sills', 'toward earth_wall_ochre (max 0.25), grime band, hairline cracks'),
     note='T3 upper storeys, kura, udatsu, mushiko, namako joints'),
 'jp_m_wall_namako_tile': dict(family='wall', palette='namako_tile', tile=0.91, ppm=512, grain='none', pen='pottery',
     wear=('dark even tile', 'lime wash drips', 'chipped tiles, stained joints'), note='texture = tiles only; joints are shikkui geometry'),
 'jp_m_roof_kawara': dict(family='roof', palette='kawara_ibushi', tile=2.0, ppm=256, grain='per tile column', pen='pottery',
     wear=('silver-grey ibushi', 'darker, per-tile tint (W8)', 'toward kawara_weathered, lichen on north (W6)'), note='all tile parts'),
 'jp_m_roof_thatch': dict(family='roof', palette='thatch_weathered', tile=2.0, ppm=256, grain='stalks down-slope', pen='hay',
     wear=('thatch_new golden (recent re-thatch, 1 in 10)', 'grey-brown', 'dark, moss on north slopes (W6), sagging patches'), note='surface'),
 'jp_m_roof_thatch_cut': dict(family='roof', palette='thatch_weathered', tile=1.0, ppm=512, grain='stalk ends facing out', pen='hay',
     wear=('fresh cut, light', '2-3 light/dark layer bands (Morse)', 'ragged, dark'), note='eave cut face'),
 'jp_m_roof_kureita': dict(family='roof', palette='roof_board_silver', tile=2.0, ppm=256, grain='down-slope, split texture', pen='wood',
     wear=('pale new wood (rare)', 'silver-grey', 'dark grey, moss, lifted boards'), note='ishioki boards, board ridges, board hisashi; NEW palette entry requested'),
 'jp_m_roof_kokera': dict(family='roof', palette='roof_board_silver', tile=2.0, ppm=256, grain='down-slope, fine courses 0.09', pen='wood',
     wear=('pale', 'silver-grey', 'curled, dark'), note='thin shingle roofs'),
 'jp_m_roof_kakigara': dict(family='roof', palette='kakigara_shell', tile=2.0, ppm=256, grain='scattered shells over kokera', pen='wood',
     wear=('pale shells', 'grey shells, dirt', 'sparse shells, moss'), note='ONLY if decision 3 is yes; NEW palette entry (assumed)'),
 'jp_m_stone_field': dict(family='stone', palette='stone_granite', tile=1.0, ppm=512, grain='none', pen='granite',
     wear=('clean', 'splash band, lichen spots', 'moss (W6)'), note='soseki, natural steps, under-floor stones'),
 'jp_m_stone_cut': dict(family='stone', palette='stone_granite', tile=1.0, ppm=512, grain='tool marks', pen='granite',
     wear=('crisp tool marks', 'rounded arrises, grime', 'moss in joints'), note='dodai stones, kura footing, cut steps'),
 'jp_m_stone_river': dict(family='stone', palette='stone_lantern', tile=1.0, ppm=256, grain='none', pen='granite',
     wear=('grey cobbles', 'lichen', 'moss'), note='ishioki roof stones'),
 'jp_m_paper_shoji': dict(family='paper', palette='washi_shoji', tile=1.0, ppm=512, grain='fibres', pen='fabric_thin',
     wear=('clean warm white', 'yellowed, patched squares', 'torn squares, stains'), note='translucency per B'),
 'jp_m_bamboo_weathered': dict(family='bamboo', palette='bamboo_weathered', tile=1.0, ppm=512, grain='along culm, nodes', pen='wood',
     wear=('pale', 'grey-beige', 'split, dark'), note='renji bars, thatch ridges, gutters, strips'),
 'jp_m_metal_iron': dict(family='metal', palette='iron_black', tile=0.5, ppm=512, grain='none', pen='iron',
     wear=('dark iron', 'rust bloom', 'rust streaks on plaster below'), note='kura fittings, bars, hooks'),
 'jp_m_straw_mushiro': dict(family='straw', palette='thatch_new', tile=1.0, ppm=512, grain='woven straw', pen='hay',
     wear=('golden', 'grey-gold', 'dark, frayed'), note='P3 hung mat only'),
}

REQ_PAL = [
 dict(id='earth_wall_aged', srgb=[115, 98, 80], method='sampled', tolerance_dE76=14,
      samples=[{'ref': 'x08_hirose_earthwall', 'box': [0.20, 0.52, 0.29, 0.64], 'select': 'mid 70 % luminance', 'value': [116, 100, 80]},
               {'ref': 'x08_hirose_earthwall', 'box': [0.52, 0.64, 0.64, 0.74], 'select': 'mid 70 % luminance', 'value': [114, 96, 79]}],
      check='x06_suzuki_a in evening shade gives (99,97,96)',
      why='Exterior earth walls of surviving 17th-18th c. farmhouses are grey-brown, not the sunlit ochre of c29 (215,180,115). The v1 walls read too bright; vanilla white walls sit at ~150.'),
 dict(id='roof_board_silver', srgb=[123, 128, 134], method='sampled', tolerance_dE76=14,
      samples=[{'ref': 'x04_misawa_a', 'box': [0.25, 0.22, 0.55, 0.30], 'select': 'mid 70 % luminance', 'value': [123, 128, 134]}],
      check='includes some stones; evening light',
      why='Weathered roof boards go silver-grey; timber_weathered (118,82,73) is the brown of wet facade boards and is wrong for roofs.'),
 dict(id='kakigara_shell', srgb=[172, 168, 158], method='assumed', tolerance_dE76=12, samples=[],
      check='needs a licensed sample of weathered oyster shells',
      why='Only if decision 3 (Edo oyster-shell board roofs) is yes.'),
]

# ------------------------------------------------------------------------------------------------ refs
IMG_SUPPORTS = {
 'x01_ioka_a': 'Ioka machiya (Nara, late 17th-early 18th c.; Nihon Minka-en): kirizuma sangawara, gable pent roof, vertical boards, under repair',
 'x03_ioka_c': 'Ioka machiya: sangawara roof, plaster gable, board lower walls, side pent (backlit; colour not usable)',
 'x04_misawa_a': 'Misawa house (Ina, mid-19th c.): stone-weighted chestnut board roof, battens, stones, plank doors, lattice window',
 'x05_misawa_b': 'Misawa house: long side, board and plaster walls, deep eaves',
 'x06_suzuki_a': 'Suzuki house (Fukushima, early 19th c., horse inn): hip thatch with board-shingled lower eave, earth walls, small ridge vent',
 'x07_sasaki_1985': 'Sasaki house (Nagano, 1731/32, village headman): thatch, board pent eave, lattice window, shoji (1985 photo)',
 'x08_hirose_earthwall': 'Hirose house (Koshu, late 17th c.): kirizuma thatch gable, exposed frame, earth panels, board base; earth colour sample',
 'x09_udatsu_mino': 'Mino-machi: udatsu wing walls between town houses (late Edo/Meiji buildings; form only)',
 'x10_morse_foundation_stone': 'post on a foundation stone', 'x11_morse_frame_2storey': 'frame of an ordinary two-storey house (from a Japanese drawing)',
 'x12_morse_namako': 'square tiles on the side of a house (namako)', 'x13_morse_kura': 'kura (fire-proof storehouses), Tokyo',
 'x14_morse_shingle_laid': 'shingle roof partly laid', 'x15_morse_shingle_ridge': 'ridge of a shingle roof, Musashi',
 'x16_morse_tile_eaves': 'eaves of a tiled roof: eave tiles', 'x17_morse_hongawara': 'hongawara (true tile)', 'x18_morse_yedogawara': 'Yedo-gawara (sangawara) eaves',
 'x19_morse_stone_roof': 'stone-slab kura roof (Shimotsuke; not used, context)', 'x20_morse_thatch_end': 'thatch ridge end with smoke hood, Iwaki',
 'x21_morse_thatch_tile_ridge': 'tiled ridge on thatch, Musashi', 'x22_morse_thatch_kanto': 'thatched roof near Tokyo',
 'x23_morse_kura_door': 'doorway of an old kura, Kyoto: hinged plaster doors, inner lattice, pent', 'x24_morse_window': 'window with board wall (context)',
 'x25_morse_amado_box': 'veranda with swinging closet for rain-doors', 'x26_morse_farmhouse_kabutoyama': 'old farmhouse, Kabutoyama (Musashi)',
 'x27_morse_village_yamashiro': 'village street, Nagaike (Yamashiro): Kansai village fronts', 'x28_morse_inn_mishima': 'old inn, Mishima (Tokaido)',
 'x29_morse_hisashi': 'hisashi of thin boards on brackets', 'x38_morse_gutter': 'bamboo gutter and downpipe with wooden funnel',
 'x30_shinagawa_1726': 'uki-e 1726: tea-house room with railed engawa at Shinagawa (Tokaido)', 'x31_masanobu_ryogoku_1748': 'Okumura Masanobu uki-e c.1748: riverside tea-house room, rails',
 'x32_shigenaga_kamo_1740s': 'Nishimura Shigenaga 1740s: Kyoto tea house by the Kamo river (mostly interior)', 'x33_jinrin_bookseller_1690': 'Jinrin kinmo zui 1690: bookseller shop front, raised display floor',
 'x35_hiroshige_goyu': 'Hiroshige c.1833: Goyu inn fronts, lattice, shoji, upper floor', 'x36_hiroshige_ishibe': 'Hiroshige c.1833: Megawa roadside tea houses, thatch + board pents, gable frame',
 'x37_eisen_narai': 'Eisen c.1835: Narai post-town shop, roofs with stones',
}
TEXT = [
 ('E01', 'https://www.nihonminkaen.jp/kanagawa.html', 'Nihon Minka-en: Kitamura house 1687 (ink date), village headman, yosemune thatch, 15.6 x 8.9 m, adze-marked posts; Kiyomiya late 17th c., yosemune thatch 13.6 x 8.2, iris on the ridge; Ito late 17th-early 18th c., irimoya thatch 16.4 x 9.1, lattice windows'),
 ('E02', 'https://www.city.kawasaki.jp/880/page/0000000269.html', 'Kawasaki city: Sasaki house, building petition 1731, built 1732, headman of Kamihata village (Nagano); yosemune thatch partly stone-weighted boards; board eaves front and rear; kabuto gable; 24.7 x 10.0 m; 1747 extension'),
 ('E03', 'https://www.nihonminkaen.jp/shukuba.html', 'Nihon Minka-en: Ioka house (Nara, late 17th-early 18th c.) kirizuma sangawara, pent eaves front and side, partial upper floor, 7.9 x 12.7 m; Suzuki (early 19th c.) thatch with board-shingled eaves, agedo front; Misawa (mid-19th c.) stone-weighted chestnut board roof'),
 ('E04', 'https://ja.wikipedia.org/wiki/卯建', 'Udatsu: hon-udatsu (small roof on the gable wall) and sode-udatsu (wing wall between the storeys); black tile caps; mainly decorative from mid-Edo; Mino, Wakimachi'),
 ('E05', 'https://ja.wikipedia.org/wiki/虫籠窓', 'Mushiko-mado: early examples small and oval; larger and rectangular in the Meiji period; Kyoto sphere'),
 ('E06', 'https://ja.wikipedia.org/wiki/桟瓦', 'Sangawara 1674 (Nishimura Hanbei); special tiles noki, sode, noshi, ganburi, onigawara; widespread only in late Edo'),
 ('E07', 'https://ja.wikipedia.org/wiki/雨戸', 'Amado first recorded at the Jurakudai (1587); run in sill/head grooves from a tobukuro; box and plate types; saru locks'),
 ('E08', 'https://ja.wikipedia.org/wiki/蔀', 'Shitomi: lattice with boards; upper part larger than the lower'),
 ('E09', 'https://roofstyle.niscs.nipponsteel.com/archives/661', 'Edo: tile banned after the 1657 Meireki fire (falling tiles in demolition fire-fighting), oyster-shell roofs recommended; 1720 tile promoted from samurai down to commoners, sangawara made it spread'),
 ('E10', 'https://www.hachise.jp/kyomachiya/history/edo.html', 'Kyoto machiya: after sangawara, commoner tile spread; in the 18th c. a unified look: one-row three-room plan, zushi-nikai, mushiko-mado, de-goshi; surviving machiya mostly post-1864'),
 ('E11', 'https://www.tatemonoen.jp/restore/intro/east.php', 'Dashigeta-zukuri: Edo-Taisho shop form, common in Edo/Tokyo from late Edo; Kagiya (1856). Read via search summary'),
 ('E12', 'https://matinamigurashi.com/guide-20190309', 'Seki-juku suriage-do: 3 boards in post grooves, stored in a box behind the upper beam inside; standard Edo to mid-Meiji'),
 ('E13', 'https://kuratoco.com/inoueke/', 'Inoue house, Kurashiki: major renovation 1721; shitomido and suriage shutters (present appearance Tenpo)'),
 ('E14', 'https://kotobank.jp/word/%E7%9F%B3%E7%BD%AE%E5%B1%8B%E6%A0%B9-1268128', 'Ishioki-yane: boards weighted with stones; still in Kyoto in the early Edo period (Rakuchu rakugai-zu); before tile spread'),
 ('E15', 'https://ja.wikipedia.org/wiki/なまこ壁', 'Namako-kabe: from the Edo period; imo-bari oldest, shihan-bari most widespread; kura, nuriya, daimyo nagaya. Read via search summary'),
 ('E16', 'https://kominkai.net/kousi/', 'Koshi by trade; oyako-goshi (cut-top children) for cloth/thread shops; lattice bars about 1 sun face. Read via search summary'),
 ('E17', 'https://ja.wikipedia.org/wiki/杮葺', 'Kokera 2-3 mm, tokusa 4-7 mm, tochi 1-3 cm'),
 ('E18', 'https://machiyane-kagoshima.com/column/yane-isi.html', 'Roofing-company column (low grade): ishioki boards (kiba) about 300-500 mm long, 3-5 mm thick; split battens across the boards with stones. Read via search summary'),
]

# ------------------------------------------------------------------------------------------------ build
def main():
    meta = json.load(open(os.path.join(ROOT, 'data', 'research_ext', 'meta.json'), encoding='utf-8'))
    pb = json.load(open(os.path.join(ROOT, 'playbook', 'refs_index.json'), encoding='utf-8'))
    pb_ids = {i['id'] for i in pb['images']} | {t['id'] for t in pb['text']}
    images = []
    for rid in sorted(IMG_SUPPORTS):
        m = dict(meta[rid]); m.pop('bytes', None); m.pop('description', None)
        m['supports'] = IMG_SUPPORTS[rid]
        images.append(m)
    img_ids = {i['id'] for i in images}
    txt_ids = {t[0] for t in TEXT}
    refs_index = {'version': 1, 'category': 'exterior (dwellings and shops)', 'date': DATE,
                  'note': 'Images local only in data/research_ext/refs/ (git-ignored, never shipped). Ids without a prefix listed here (c.., m.., T..) are in playbook/refs_index.json. Text is cited, not copied.',
                  'download_policy': 'PD / CC0 / CC BY only. Commons API (descriptive User-Agent, retry-after honoured), Project Gutenberg (Morse figures), Met Open Access, Cleveland Open Access, Library of Congress.',
                  'playbook_ids_reused': sorted({r['id'] for e in E for r in e['refs']} & pb_ids),
                  'images': images, 'text': [{'id': a, 'url': b, 'supports': c} for a, b, c in TEXT]}
    # checks
    errs = []
    for e in E:
        for r in e['refs']:
            if r['id'] not in img_ids | pb_ids: errs.append('unknown ref %s in %s' % (r['id'], e['id']))
        for tok in re.findall(r'\[([^\]]+)\]', e.get('period_evidence', '')):
            for t in re.split(r'[,;]\s*', tok):
                t = t.strip()
                if re.match(r'^(E\d\d|T\d\d|x\d\d)$', t) and not (t in txt_ids or t in pb_ids or any(i.startswith(t + '_') for i in img_ids)):
                    errs.append('unknown evidence id %s in %s' % (t, e['id']))
        for m in e['materials']:
            if m['material'] not in MAT: errs.append('material %s missing' % m['material'])
    if errs: print('\n'.join(errs)); sys.exit(1)

    entries = []
    for e in E:
        d = {k: v for k, v in e.items() if not k.startswith('_')}
        entries.append(d)
    bl = {'category': 'parts-exterior-dwellings-shops', 'version': 1, 'author': 'research agent A-EXT', 'date': DATE, 'stage': 'B',
          'scope_note': 'Exteriors of dwellings and shops for tiers 1-3 (minka, machiya, nagaya, shop fronts, hatago, tea houses, family kura). Parts only: the architect (C) assembles buildings from them. Out of scope (see BUILD_LIST.md, Later): temples/shrines, government/castle, street dressing, gardens/site sets, interiors.',
          'entries': entries}

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
        mats.append({'id': mid, 'family': m['family'], 'palette_id': m['palette'],
                     'palette_status': 'existing' if m['palette'] in pal_ids else 'REQUESTED (see requested_palette_entries)',
                     'tile_size_m': m['tile'], 'px_per_m': m['ppm'], 'grain': m['grain'], 'penetration_rvmat': m['pen'],
                     'wear': {'_w0': m['wear'][0], '_w1': m['wear'][1], '_w2': m['wear'][2]}, 'note': m['note'],
                     'used_by': sorted(used.get(mid, []))})
    if errs: print('\n'.join(errs)); sys.exit(1)
    mn = {'version': 1, 'date': DATE, 'author': 'research agent A-EXT',
          'note': 'Full task list for the materials agent: one canonical set per material, 3 wear levels each (_w0 clean, _w1 normal, _w2 heavy), path JP\\common\\materials\\<family>\\ (PLAYBOOK §9). Weathering W1-W8 per PLAYBOOK §6.5. Resolution 1024^2 tileable; px_per_m per PLAYBOOK §9.',
          'counts': {'materials': len(mats), 'texture_sets': 3 * len(mats)},
          'materials': mats, 'requested_palette_entries': REQ_PAL}

    wb = lambda p, s: open(os.path.join(OUT, p), 'wb').write(s.encode('utf-8'))
    wb('build_list.json', json.dumps(bl, ensure_ascii=False, indent=1) + '\n')
    wb('materials_needed.json', json.dumps(mn, ensure_ascii=False, indent=1) + '\n')
    wb('refs_index.json', json.dumps(refs_index, ensure_ascii=False, indent=1) + '\n')
    wb('BUILD_LIST.md', md(bl, mn))
    nv = sum(len(e['variants']) for e in E)
    print('entries', len(E), 'variants', nv, 'materials', len(mats), 'images', len(images), 'text', len(TEXT))

def fmt_dims(d, n=4):
    out = []
    for k, v in list(d.items())[:n]:
        s = '%s %s' % (k, v['value'])
        s += ' (assumed)' if v.get('assumed') else (' [%s]' % v['source'] if v.get('source') else '')
        out.append(s)
    more = len(d) - n
    return '; '.join(out) + ('; +%d more in JSON' % more if more > 0 else '')

def esc(s):
    return str(s).replace('|', '/').replace('\n', ' ')

def md(bl, mn):
    L = []
    A = L.append
    A('# BUILD LIST: exterior parts for dwellings and shops, v1\n')
    A('**Stage:** B (materials, then parts), then C (architect)\n')
    A('**Author and date:** research agent A-EXT, %s\n' % DATE)
    A('**Scope:** exteriors of dwellings and shops, tiers 1-3: minka farmhouses, machiya, nagaya, shop fronts, hatago, tea houses and the family kura. Every part the architect needs to assemble them. Temples, government buildings, street dressing, gardens and interiors are in "Later".\n')
    A('**Files:** `build_list.json` (validates against `playbook/templates/build_list_schema.json`; the builders read it), `materials_needed.json` (the materials agent\'s task list), `refs_index.json` (new sources x01-x38 and E01-E18). Images are in `data/research_ext/refs/`. All four files come from `tools/gen_build_list.py`. Edit the data there and rerun it, so the markdown and the JSON stay identical.\n')
    A('**Reading the tables:** `[E03]`, `[T59]` or `x08` are sources. `(assumed)` means no source gives the value. D1-D10 are PLAYBOOK §5 deviations.\n')
    A(OVERVIEW)
    fams = []
    for e in E:
        if e['_family'] not in fams: fams.append(e['_family'])
    n = 0
    for f in fams:
        A('\n## %s\n' % f)
        A('| # | ID | Name | What and where | Imp. | Tier | Pri | Period evidence | Key dimensions | Materials (library -> palette) | Connectors | Variants |')
        A('|---|---|---|---|---|---|---|---|---|---|---|---|')
        for e in E:
            if e['_family'] != f: continue
            n += 1
            mats = '<br>'.join('%s: `%s` -> %s' % (m['surface'], m['material'], m['palette_id']) for m in e['materials']) or '(generator spec)'
            con = '<br>'.join(e.get('connectors', []))
            var = '<br>'.join('`%s` %s' % (v['id'], v['differs_by']) for v in e['variants'])
            tiers = ','.join(str(t) for t in e['tiers']) + ('' if e.get('region', 'all') == 'all' else ' (%s)' % e['region'])
            A('| %d | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (n, e['id'], esc(e['name']), esc(e.get('what', '')), e['importance'], tiers, e['priority'],
              esc(e.get('period_evidence', '')), esc(fmt_dims(e['dimensions'])), esc(mats), esc(con), esc(var)))
    A('\n## Notes per entry (only where the table is not enough)\n')
    for e in E:
        bits = []
        if e.get('banned_tells_to_watch'): bits.append('- **Banned tells to watch:** ' + '; '.join(e['banned_tells_to_watch']))
        if e.get('deviations'): bits.append('- **Deviations / rules used:** ' + '; '.join(e['deviations']))
        if e.get('open_questions'): bits.append('- **Open questions:** ' + '; '.join(e['open_questions']))
        if e.get('lod_budget'): bits.append('- **LOD:** ' + e['lod_budget'])
        if bits:
            A('**`%s`**' % e['id']); A('\n'.join(bits)); A('')
    A('## Engine and gameplay notes (all parts)\n')
    A(ENGINE)
    A('\n## Materials the materials agent must make (%d materials, %d texture sets)\n' % (mn['counts']['materials'], mn['counts']['texture_sets']))
    A('| Material | Family | Palette ID | Tile (m) | px/m | Fire | _w0 / _w1 / _w2 | Used by |')
    A('|---|---|---|---|---|---|---|---|')
    for m in mn['materials']:
        A('| `%s` | %s | %s%s | %s | %s | %s | %s / %s / %s | %d parts |' % (m['id'], m['family'], m['palette_id'], ' **(new)**' if m['palette_status'] != 'existing' else '',
          m['tile_size_m'], m['px_per_m'], m['penetration_rvmat'], esc(m['wear']['_w0']), esc(m['wear']['_w1']), esc(m['wear']['_w2']), len(m['used_by'])))
    A('\n## Requested new materials or palette entries\n')
    A('| Palette ID | sRGB | Method | Why | Sample source |')
    A('|---|---|---|---|---|')
    for p in REQ_PAL:
        src = ', '.join('%s box %s -> %s' % (s['ref'], s['box'], s['value']) for s in p['samples']) or p['check']
        A('| %s | %s | %s | %s | %s |' % (p['id'], p['srgb'], p['method'], esc(p['why']), esc(src)))
    A('\n## Checks the builder must run\n')
    A('- C1-C5, C8 and C9 on every part (PLAYBOOK §12); C3 grid snap is the one that makes "any wall fits any post spacing" true.')
    A('- C8 specials: kawara LOD0 corrugation density; ishioki and thatch eave edges modelled (not flat); plinth and soseki made of separate stones; no rectangular mushiko; no bengara or kuro_board outside their tiers.')
    A('- C1: shikkui mean must be <=192 (the v1 machiya plaster was about 217).')
    A(LATER)
    return '\n'.join(L) + '\n'

OVERVIEW = '''
## What a house looks like, tier by tier (1730)

**Tier 1, rural and poor.** A low house under a heavy thatch roof. In the Kanto the roof is hipped, like the Kitamura
house of 1687; in Koshu it is a gable, like the Hirose house. The thatch is cut square at the eave and shows about
0.6 m of thickness. Walls are grey-brown earth between adzed posts and rails, with a plank skirt at the bottom. The
posts stand on single field stones. There are few openings: one wide plank door into the earth-floored doma, a
barred window or two, and a smoke hood on the ridge. There is no tile, no white plaster and no veranda. In mountain
and coast villages the same house has a low-pitched board roof, held down by rows of river stones on battens.
Back-alley tenements in towns are the urban tier 1: shingle roofs, board walls and board-bottomed paper doors.

**Tier 2, village and post town.** The Kiso post-town house has a low stone-weighted board roof with the eave
side to the street. The street front is dark vertical boards and lattice, with plank doors. By night the shop front
closes with vertical-sliding board shutters (suriage-do). The upper storey stays low. The village headman's house,
like the Sasaki house of 1731-32, is a big hipped thatch roof with stone-weighted board pent eaves front and back.
It has earth walls with board wainscots, a veranda with storm shutters and a shutter box, and shoji behind them.
Tile appears only on the family kura or a big inn.

**Tier 3, town and main road.** The Kamigata machiya, like the Ioka house of the late 17th or early 18th century,
has a gable roof of sangawara tiles. The ridge is stacked, with an end tile at each end, and the eave tiles have
small round ends. A tiled pent roof runs over the ground floor. The upper storey is low and plastered, pierced by
small oval mushiko windows. The ground floor is dark lattice, with bengara used sparingly, and a plank front door.
Plastered udatsu wing walls stand between neighbours. The sill rests on a course of separate stones. Edo in 1730
looks different. Tile was banned there from 1657 to 1720 except on storehouses, so about half the roofs are still
boards, possibly strewn with oyster shells (decision 3), and half are new tile. Fronts are boards or the new
plastered nuriya. The kura behind has thick plaster walls, a namako lower wall, a tile roof and hinged plaster doors.

**What changes from machiya v1:** the roof is corrugated tile geometry with real eave, verge and ridge parts
(`jp_p_roof_sangawara_*`, `jp_p_roof_kawara_ridge`, `jp_p_roof_onigawara`). The upper storey is low, with oval
mushiko (`jp_p_open_mushiko`). The plaster is darker and mostly earth rather than white (`earth_wall_aged`; shikkui
<=192 and only at tier 3). The base is separate stones under a timber sill (`jp_p_found_dodai_stones`,
`jp_p_found_soseki`).

## Decisions only Stephen can make

1. **Wall colour:** approve the new sampled palette entry `earth_wall_aged` (115,98,80) as the default exterior
   earth wall for tiers 1-2, with shikkui (<=192) only on tier-3 upper storeys and kura.
2. **Board roof colour:** approve `roof_board_silver` (123,128,134) for board and stone-weighted roofs.
3. **Edo oyster-shell roofs (kakigara-buki), 1657 to the Kyoho era:** add them as the Edo tier-3 board-roof
   variant? It is cheap: one extra material.
4. **Dashigeta and projecting upper fronts:** the surviving examples date from after 1750 (Kagiya, 1856).
   Drop them, or keep them as a flagged deviation for Edo and Kiso?
5. **Full-height upper storey on tier-2 hatago:** the only evidence is 1830s prints (Goyu) and an undated text
   source [T30]. Allow a 2.40 m upper storey, or keep hatago low like the machiya?
6. **Thatch eave height:** a 45 deg thatch eave that keeps the 2.20 m soffit needs a wall plate of about
   3.0 m, where the real value is about 2.4-2.7 m. Accept the taller wall, or use the period board pent eave
   (the Sasaki type) over every entrance side?
'''

ENGINE = '''- **Doors:** every sliding leaf follows B's convention: `type="translation"`, one bone per leaf, a memory axis of
  exactly 1.00 m, and `doorWoodSlide` sounds. Heads are at 2.00 (D2). Clear widths are >=0.80 inside and >=1.00 at
  main entrances (D1). The kuguri wicket is decorative only (D9).
- **Static by design:** amado runs, shitomido and battari-shogi come as static open or closed variants.
  Suriage-do is static first; a vertical-translation door is an engine test.
- **Hinged:** only the kura outer leaves are hinged. They ship static open in P1; rotation doors come in P2 after an
  engine test.
- **Sealed lofts:** low upper storeys (zushi-nikai) are sealed by default (G0 decision 4). Mushiko are closed in View
  Geometry, so nobody sees or shoots into a sealed loft.
- **Fire Geometry:** plaster and earth use `dirt`, timber and bamboo `wood`, tile and namako `pottery`, thatch
  `hay`, paper `fabric_thin`, stone `granite`, iron `iron`. All are vanilla penetration rvmats.
- **Soffits:** keep >=2.20 m under any walked eave (PLAYBOOK §4). The thatch eave is decision 6.
- **LOD:** roof geometry detail only within 3 rows of the eave and ridge. Stones and battens are merged at LOD1 and
  become texture at LOD2. Lattice becomes a panel at LOD1 (B spike). Building budgets are in PLAYBOOK §12.
- **Grid:** walls are recipes over any run of half-ken bays. Fixed details come in 0.5, 1, 1.5 and 2 ken widths
  between post connectors. Roofs are generated from any footprint on the ken grid, with kawara columns at ken/7
  (PLAYBOOK §10.2).'''

LATER = '''
## Later (out of scope for this list)

- **Temples and shrines (stage R):** hongawara temple roofs with a 7-course ridge, curved kokera and bark roofs,
  shu vermilion, torii, halls, gates and bell towers.
- **Government, status and castle:** honjin (gate, shikidai genkan, jodan-no-ma), toiyaba, sekisho, jinya,
  bugyosho, bansho, kido and kidoban, fire towers, samurai nagaya-mon and yashiki, castle walls and keeps.
  They reuse these parts, plus kuro_board and status features that are banned for commoners.
- **Street dressing (stage S):** noren, kanban, chochin, andon signs, sudare, yoshizu, inuyarai, komayose,
  tensuioke with buckets, benches, carts and seasonal dressing.
- **Gardens and site sets (stage S):** fences, hedges, tsuijibei and neribei walls, gates, wells, tsubo-niwa,
  stepping stones, drying racks, stone lanterns and yards.
- **Interiors (stage D):** fusuma, interior shoji, ceilings, tatami layouts, stairs and furniture proxies.
- **Unverified or rejected for 1730:** rectangular mushiko (Meiji), dashigeta (decision 4), kura oki-yane (date
  and region not checked), ichimonji eave tiles (date not checked), plaster wave reliefs on ridges (1880s), and
  Morse's stone-slab kura roofs (Shimotsuke, outside the map region).
- **Housekeeping:** `playbook/refs_index.json` labels `c14_minkaen_b` as an Edo farmhouse. It is the museum's
  modern main building. Its kawara colour sample is still usable, but don't use it to date anything.
'''

if __name__ == '__main__':
    main()
