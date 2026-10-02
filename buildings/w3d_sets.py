"""W3D (2026-10-02): the dressings of the wave-3d furnished variants (the new government halls + the earlier shells each
site reuses) for buildings/furnishkit.py. SETS_W3D are merged into buildings/furnish_sets.SETS (like w3c2_sets).
Binding rules as w3c2_sets.py (G1 A2, BUILD_LIST, LIFE_LAYER): 5-7 counted props a room, <= 25 % floor cover, the
1.00 m bands, >= 1 raised loot surface a room, moderate "as left" disorder. Dead world, autumn: the offices left in a
hurry (ledgers spilled, a brazier tipped), the cells empty and open (neutral: no bodies, no gore). Props: spikes/W3D/
props_w3d.py (govfit) + the earlier libraries. Research + recorded choices: spikes/W3D/W3D_NOTES.md.
"""
import d3_sets as D3
from d3_sets import Room, sparse
from w3b_sets import must
import furnish_sets as FS
import w3c2_sets as W2
import w3c1_sets as W1


def _plinth(c, depth=0.55, top=0.046, w=0.26):
    """W3D: a cut-stone foundation band (kiso) round the wall lines, from `depth` under grade to `top`: the island's
    district slopes 3-4 %, so a building is seated on its high side (no terrain through a floor, spikes/W3D/
    floorcheck.py) and this band closes the gap under its walls on the low side (a building on a levelled stone
    plinth: honest for a slope). Visual only (the walls and floors keep the collision). The footprint = the post
    nodes' extent."""
    from jpparts.core import box
    pts = [s_ for s_ in c.M.solids if s_.tag in ("post", "gate_post") and 1 in s_.vis]
    xs = [v for s_ in pts for v in (s_.bbox()[0], s_.bbox()[1])]
    zs = [v for s_ in pts for v in (s_.bbox()[4], s_.bbox()[5])]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    h = w / 2
    for (a0, a1, b0, b1) in ((x0 - h, x1 + h, z0 - h, z0 + h), (x0 - h, x1 + h, z1 - h, z1 + h),
                             (x0 - h, x0 + h, z0 + h, z1 - h), (x1 - h, x1 + h, z0 + h, z1 - h)):
        c.M.add(box(a0, a1, -depth, top, b0, b1, "stone_cut", vis=(1, 2, 3), tag="kiso"))


# ------------------------------------------------------------------------------------------------ 1 checkpoint
def bansho(c):
    """The checkpoint guardhouse: on the officials' tatami the low desks facing the gravel court (the pass presented
    and compared with the ledger), a brazier, the cushions stacked; in the back office the pass ledgers, the seal box,
    a spilled writing box; in the kitchen doma the stove, the water jar, the capture tools on the wall."""
    _plinth(c)
    FS._kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama_nolid", 0, why="the guards' rice pot left in the stove")
    D = Room(c, "doma", centre=False)
    D.wall("jp_f_mitsudogu", sides=("xmin", "zmin"), why="the three capture tools on the wall (the gate's spare set)")
    D.wall("jp_f_mizugame", why="the water jar")
    D.wall("jp_f_oke_bucket", why="a bucket")
    D.wall("jp_f_tana_091_3", sides=("zmin", "xmin"), why="a shelf with the guards' bowls")
    sparse(c, "engawa", "the veranda of the inspection room (kept clear: the step from the gravel)")
    H = Room(c, "hall", open_sides=("zmax",), centre=False)
    d1 = must(H, "jp_f_zukue_choba", "the officials' low desk facing the gravel court", sides=("zmin",))
    if d1 is not None:
        c.surf(d1, "jp_f_choba_set_desk", dx=-0.035, dz=-0.04, why="the desk set: brush, inkstone, the pass being compared")
    d2 = H.wall("jp_f_zukue_plain", sides=("zmin",), why="a second desk (the clerk's)")
    if d2 is not None:
        c.surf(d2, "jp_f_sg_books", why="pass ledgers left open")
    H.free("jp_f_hibachi_box_tipped", 0.20, 0.55, 0, why="the brazier tipped over")
    H.wall("jp_f_enza_zabuton_stack3", sides=("xmin",), why="the officials' cushions stacked")
    H.free("jp_f_tabakobon_spilled", 0.75, 0.45, 20, why="a tobacco tray knocked over")
    O = Room(c, "office")
    O.wall("jp_f_box_stack3_toppled", why="document boxes (the old pass ledgers), toppled")
    t = O.wall("jp_f_tansu_single_ransacked", why="the ledger chest, drawers pulled")
    O.wall("jp_f_box_m_lacquer", why="the seal box")
    O.free("jp_f_writing_box_spilled", 0.5, 0.5, 30, why="a writing box spilled")
    O.wall("jp_f_andon_kaku_tipped", why="a lamp knocked over")
    if t is None:
        O.wall("jp_f_zukue_plain", why="a desk")


def bunk_ashigaru(c):
    """The foot-soldiers' guardhouse (W3C2's bunk hall, board roof): the stove and the water jar in the doma, the
    six-shaku staffs and the capture tools on the wall; on the raised floor the bedding rolled along the wall round the
    irori, coats and rain capes on the pegs, a lantern with the checkpoint's crest dropped."""
    _plinth(c)
    FS._kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama", 0, why="the pot, lid on, in the stove")
    c.passage(("doma", "living"), -1.82, 0.35, "kamachi step doma <-> living")
    D = Room(c, "doma", centre=False)
    D.wall("jp_f_jar_l", why="the water jar")
    D.wall("jp_f_mitsudogu", sides=("xmin",), why="the capture tools on the wall")
    D.wall("jp_f_oke_bucket", why="a bucket")
    D.wall("jp_f_firewood_stack", sides=("zmin",), why="split wood")
    W2._hut_living(c, "xmax", 0.0, bed="jp_f_futon_stack_slumped")
    c.wall("living", "zmin", 1.60, "jp_f_straw_bed_pile", why="a straw bed")
    L = Room(c, "living", centre=False)
    L.wall("jp_f_mino_pegs_rain", sides=("zmax", "zmin"), why="rain capes and hats on the pegs")
    L.wall("jp_f_katanakake_wall_empty", sides=("zmin", "zmax"), why="the sword rack, empty")
    L.wall("jp_f_kori", why="a wicker trunk")
    L.free("jp_f_hibachi_box", 0.60, 0.40, 0, why="a brazier", band=False)
    L.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")


# ------------------------------------------------------------------------------------------------ 2 post-station office
def toiyaba(c):
    """The post-station office: on the raised office the clerks' desks facing the yard (the relay ledgers, an abacus),
    the ledger boxes and the chest along the back wall, a brazier; the doma with the station's loads waiting."""
    _plinth(c)
    C = Room(c, "choba", open_sides=("zmax",), centre=False)
    d1 = must(C, "jp_f_zukue_choba", "the clerks' desk facing the yard", sides=("zmax",))
    if d1 is not None:
        c.surf(d1, "jp_f_choba_set_desk", dx=-0.035, dz=-0.04, why="the desk set (the relay ledger open)")
    d2 = C.wall("jp_f_zukue_plain", sides=("zmin",), why="a second desk")
    if d2 is not None:
        c.surf(d2, "jp_f_sg_books", why="the relay ledgers (tsugitate-cho) spilled")
    C.free("jp_f_soroban_tray", 0.30, 0.55, 15, why="the abacus tray")
    C.wall("jp_f_box_stack3", sides=("zmin", "xmin"), why="the register boxes")
    C.wall("jp_f_tansu_single_ransacked", sides=("zmin", "xmin"), why="the ledger chest, drawers pulled")
    C.free("jp_f_hibachi_box_tipped", 0.70, 0.40, 0, why="the brazier tipped")
    D = Room(c, "doma", open_sides=("zmax",), centre=False)
    D.wall("jp_f_mizugame", sides=("xmin",), why="the water jar")
    D.wall("jp_f_kori", sides=("xmin",), why="a wicker trunk left by a traveller")
    D.wall("jp_f_tool_wall_wood", sides=("xmax",), why="carrying poles and ropes on the wall")


# ------------------------------------------------------------------------------------------------ 3 jinya
def ginmisho(c):
    """The court room: the official's desk at the back of the tatami facing the gravel court, the clerk's desk at the
    side, the armrest cushion stack, a brazier; the office behind with the case records."""
    sparse(c, "engawa", "the veranda over the gravel court (kept clear: the step from the gravel)")
    H = Room(c, "hall", open_sides=("zmax",), centre=False)
    d1 = must(H, "jp_f_zukue_plain", "the official's desk facing the gravel court", sides=("zmin",))
    if d1 is not None:
        c.surf(d1, "jp_f_sg_books", why="the case record, closed")
    d2 = H.wall("jp_f_zukue_choba", sides=("xmin", "xmax"), why="the clerk's desk at the side (the record kept)")
    if d2 is not None:
        c.surf(d2, "jp_f_sg_books", why="the record book")
    H.wall("jp_f_enza_zabuton_stack3", sides=("xmax", "xmin"), why="cushions stacked")
    H.free("jp_f_hibachi_round", 0.30, 0.45, 0, why="the brazier")
    H.wall("jp_f_katanakake_stand_empty", sides=("zmin",), why="the sword stand, empty")
    O = Room(c, "office")
    O.wall("jp_f_box_stack3_toppled", why="case records in boxes, toppled")
    O.wall("jp_f_tansu_single_ransacked", why="a chest, drawers pulled")
    t = O.wall("jp_f_zukue_plain", why="a desk")
    if t is not None:
        c.surf(t, "jp_f_sg_books", why="papers spilled")
    O.wall("jp_f_box_m_lacquer", why="the seal box")
    O.free("jp_f_andon_kaku_tipped", 0.5, 0.5, 0, why="a lamp knocked over")


def _daidokoro(c, room, steps):
    """D3's daidokoro dressing with the pot hook hung from the REAL member over the irori (W3C2's _beam_over; D3's
    samurai houses hang it 1.2-1.3 m under the beam: hangcheck baseline, fixed here only)."""
    from d3_sets import Room as R_
    D = R_(c, room, open_sides=("xmin",), points=steps)
    if c.fit(room, "irori"):
        f = c.fit(room, "irori")[0]
        hx, hy, hz = f["hook"]
        c.hang(room, "jp_f_jizai_kagi", hx, hz, W2._beam_over(c, hx, hz, hy, reach=1.6), over="hearth",
               why="the pot hook over the irori")
        D.free("jp_f_enza", 0.55, 0.62, 0, why="straw cushion by the hearth")
    tn = D.wall("jp_f_tana_182_3", sides=("zmin", "zmax"), why="the dish shelf")
    D.surf(tn, "jp_f_tableware_bowls", surface="board_1", why="bowls on the shelf")
    D.wall("jp_f_rice_bin", sides=("zmax", "zmin", "xmax"), why="the rice bin")
    D.wall("jp_f_charcoal_scuttle", why="the charcoal scuttle")
    D.free("jp_f_tableware_scattered", 0.5, 0.25, 20, why="bowls scattered (disorder)", count=True)
    D.free("jp_f_kama_nabe", 0.5, 0.78, 0, why="a pot left on the boards")
    D.onwall("jp_f_ofuda_akiba", sides=("xmax", "zmax", "zmin"), why="the fire charm")
    return D


def jinya(c):
    """The intendant's office (D3's small samurai mansion): the genkan room with the screen and the sword stand, the
    clerks' offices (desks, ledgers, abacus, the tax-rice measures) in the chanoma and the tsugi, the intendant's room
    (the zashiki, its tokonoma undisturbed), the kitchen as it was."""
    _plinth(c)
    steps = [(c.R("doma")[1] + 0.05, 0.0)]
    c.passage(("doma", "daidokoro"), steps[0][0], steps[0][1], "kamachi step doma <-> daidokoro")
    D3._doma_kitchen(c, "doma", "xmax", steps, 3)
    _daidokoro(c, "daidokoro", steps)
    G = Room(c, "genkan_ma")
    G.free("jp_f_byobu_tsuitate", 0.80, 0.70, 90, why="the entrance screen facing the genkan door")
    G.wall("jp_f_katanakake_stand_empty", why="the sword stand, empty")
    G.wall("jp_f_box_l", why="a document box")
    G.free("jp_f_hibachi_box", 0.35, 0.40, 0, why="a box brazier")
    G.onwall("jp_f_mino_pegs", why="rain capes for the village rounds")
    ch = Room(c, "chanoma")
    d = ch.wall("jp_f_zukue_choba", why="a clerk's desk")
    if d is not None:
        ch.surf(d, "jp_f_choba_set_desk", dx=-0.035, dz=-0.04, why="the desk set (the tax allocation papers)")
    d2 = ch.wall("jp_f_zukue_plain", why="a second clerk's desk")
    if d2 is not None:
        ch.surf(d2, "jp_f_sg_books", why="village detail books spilled")
    ch.free("jp_f_soroban_tray", 0.55, 0.55, 10, why="the abacus tray")
    ch.wall("jp_f_box_stack3_toppled", why="register boxes toppled")
    ch.free("jp_f_masu_spilled", 0.35, 0.40, 0, why="the standard rice measures knocked over")
    ts = Room(c, "tsugi")
    t = ts.wall("jp_f_tansu_ransacked", why="the record chest, drawers pulled")
    ts.wall("jp_f_box_m_lacquer", why="the seal box")
    d3 = ts.wall("jp_f_zukue_plain", why="a desk")
    if d3 is not None:
        ts.surf(d3, "jp_f_masu_set", dx=-0.145, dz=-0.05, why="the measures on the desk")
    ts.free("jp_f_enza_zabuton_stack3", 0.5, 0.5, 0, why="cushions stacked")
    ts.free("jp_f_andon_kaku_tipped", 0.3, 0.7, 0, why="a lamp knocked over")
    if t is None:
        ts.wall("jp_f_box_l", why="a box")
    D3._formal(c, "zashiki", 3, toko=True)
    sparse(c, "engawa", "the veranda along the garden")
    sparse(c, "genkan_porch", "the genkan porch")


def kura_nengu(c):
    """The jinya's tax-rice store (C3's plain kura): rice bales stacked on both floors, one burst, the measures."""
    W1._stair_clear(c, "kura", "nikai")
    c.wall("kura", "xmax", 0.00, "jp_f_tawara_stack6", why="tax rice in bales against the gable")
    c.free("kura", "jp_f_tawara_stack6", 0.90, 0.60, 0, why="more bales")
    c.free("kura", "jp_f_tawara_burst", -1.20, 0.90, 0, why="a bale burst, the rice spilled")
    c.free("kura", "jp_f_masu_spilled", 0.80, 0.75, 0, why="the measures knocked over")
    c.free("kura", "jp_f_box_l", -2.15, -1.20, 0, why="a box of sampling spikes and seals")
    N = Room(c, "nikai")
    N.wall("jp_f_tawara_stack6", why="bales upstairs")
    N.wall("jp_f_box_m", why="a box of seals and sampling spikes")
    N.wall("jp_f_box_l", why="a box")
    N.wall("jp_f_tawara", why="a single bale")
    N.free("jp_f_tawara_burst", 0.25, 0.30, 30, why="a bale burst")


# ------------------------------------------------------------------------------------------------ 4 jail
def roya(c):
    """The cell block: in the corridor the guards' things (the capture tools on the end wall, a lantern dropped, a
    bucket); in each cell straw mats on the boards, the lidded toilet tub in the corner, a few wooden bowls. Empty,
    the doors open; nothing else (neutral)."""
    _plinth(c)
    K = Room(c, "corridor", centre=False)
    K.wall("jp_f_mitsudogu", sides=("xmin", "xmax"), why="the capture tools on the end wall")
    K.wall("jp_f_oke_bucket", sides=("xmax", "xmin"), why="a water bucket")
    K.wall("jp_f_mushiro_rolled", sides=("zmax",), why="spare mats, rolled")
    K.free("jp_f_chochin_fallen", 0.30, 0.50, 30, why="the guard's lantern, dropped")
    for cell in ("cell_a", "cell_b"):
        sparse(c, cell, "a small cell: mats, the tub and bowls only")
        R = Room(c, cell, centre=False)
        R.free("jp_f_mushiro", 0.5, 0.40, 0, why="a straw mat on the boards", band=False)
        R.wall("jp_f_oke_pickle", sides=("xmin", "xmax"), why="the lidded toilet tub in the corner")
        R.free("jp_f_tableware_bowls", 0.25, 0.25, 0, why="wooden bowls on the boards", band=False)
        R.free("jp_f_mushiro_torn", 0.5, 0.80, 90, why="a torn mat", band=False)


# ------------------------------------------------------------------------------------------------ 5 fire brigade
def hikeshi(c):
    """The fire brigade's tool shed (C2's open board shed): the matoi-nobori in its stand, buckets and fire hooks on
    the racks, ropes, the long hooks and ladders on the back wall; a bucket rolled."""
    sparse(c, "floor", "the open tool shed: the gear stands along the walls, the middle kept free to run out")
    F = Room(c, "floor", open_sides=("zmax",), centre=False)
    must(F, "jp_f_matoi_nobori", "the group's standard in its stand", sides=("zmin", "xmin"))
    F.wall("jp_f_fire_gear", sides=("zmin",), why="the fire hooks and buckets on the back wall")
    F.wall("jp_f_fire_gear_buckets", sides=("xmin", "xmax"), why="more buckets on the rack")
    F.wall("jp_f_rope_pegs_3", sides=("xmax", "zmin"), why="coils of rope")
    F.wall("jp_f_tool_wall_wood", sides=("zmin", "xmax"), why="the long hooks and rakes")
    F.free("jp_f_oke_tipped", 0.6, 0.6, 30, why="a bucket rolled", band=False)


def nagayamon(c):
    """The jinya's black nagaya-mon: D3's dressing of the servants' room and the store + the foundation band."""
    _plinth(c)
    D3.nagayamon(c)


SETS_W3D = {
    "w3d_bansho": {"tier": 2, "fn": bansho},
    "w3d_bunk_ashigaru": {"tier": 1, "fn": bunk_ashigaru},
    "w3d_toiyaba": {"tier": 2, "fn": toiyaba},
    "w3d_ginmisho": {"tier": 3, "fn": ginmisho},
    "w3d_jinya": {"tier": 3, "fn": jinya},
    "w3d_kura_nengu": {"tier": 2, "fn": kura_nengu},
    "w3d_roya": {"tier": 1, "fn": roya},
    "w3d_hikeshi": {"tier": 1, "fn": hikeshi},
    "w3d_nagayamon": {"tier": 2, "fn": nagayamon},
}


def sets():
    return {k: dict(v, fn=D3._wrap(v["fn"])) for k, v in SETS_W3D.items()}
