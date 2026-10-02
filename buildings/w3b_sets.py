"""W3B (2026-10-02): the dressings of the wave-3b furnished variants (bathhouse, stable row, booths, workshops, timber
sheds, foundry) for buildings/furnishkit.py. SETS_W3B are merged into buildings/furnish_sets.SETS (like d3_sets).

Binding rules as furnish_sets.py / d3_sets.py (G1 A2, BUILD_LIST, LIFE_LAYER): 5-7 counted props a room, <= 25 % floor
cover, the 1.00 m bands, >= 1 raised loot surface a room, moderate "as left" disorder; open sheds and the boiler
lean-to are sparse() spaces. The placer is D3's (d3_sets.Room: wall-backed props clear of the door zones and the
bands); the specialty props sit on the shells' fitting spots (rooms json). Props: spikes/W3B/props_w3b.py (tradefit)
+ the earlier libraries. Autumn, dead world: boiler and furnace cold, tub drained, work left where it lay.
"""
import d3_sets as D3
from d3_sets import Room, sparse

TOP_POOL = D3.TOP_POOL


def fit1(c, room, kind):
    f = c.fit(room, kind)
    if not f:
        raise KeyError("%s has no %s fitting in %s" % (c.key, kind, room))
    return f[0]


def fc(f):
    """The centre (model frame) of a fitting given by centre or rect."""
    if "centre" in f:
        return f["centre"][0], f["centre"][1]
    r = f["rect"]
    return (r[0] + r[1]) / 2, (r[2] + r[3]) / 2


def must(R, name, why, sides=(), spots=((0.5, 0.75), (0.3, 0.7), (0.7, 0.7), (0.5, 0.3), (0.75, 0.5), (0.25, 0.5),
                                              (0.8, 0.25), (0.2, 0.25)), yaws=(0.0, 90.0, 180.0, 270.0)):
    """A specialty prop that must be in the room: wall-backed on `sides` first, else the first free spot (the
    placer's band / door rules still hold); reports when it found no place."""
    for sd in sides:
        it = R.wall(name, sides=(sd,), why=why, frm="mid")
        if it is not None:
            return it
    for (fx, fz) in spots:
        for yw in yaws:
            it = R.free(name, fx, fz, yw, why=why, rad=0.8)
            if it is not None:
                R.miss = [m for m in R.miss if m != name]
                return it
    for (fx, fz) in spots:             # last resort: the band test off (the decor checks still judge the room)
        for yw in yaws:
            it = R.free(name, fx, fz, yw, why=why, rad=0.8, band=False)
            if it is not None:
                R.miss = [m for m in R.miss if m != name]
                print("[w3b_sets] %s: %s placed without the band test" % (R.c.key, name))
                return it
    print("[w3b_sets] %s: no place for %s" % (R.c.key, name))
    return None


def kamachi_point(c, a, b):
    """The kamachi step between rooms a (doma) and b (raised): the doma rect's edge facing b at the step."""
    ra, rb = c.R(a), c.R(b)
    if abs(ra[1] - rb[0]) < 0.4:
        x = (ra[1] + rb[0]) / 2
        z = (max(ra[2], rb[2]) + min(ra[3], rb[3])) / 2
    elif abs(rb[1] - ra[0]) < 0.4:
        x = (rb[1] + ra[0]) / 2
        z = (max(ra[2], rb[2]) + min(ra[3], rb[3])) / 2
    elif abs(ra[3] - rb[2]) < 0.4:
        z = (ra[3] + rb[2]) / 2
        x = (max(ra[0], rb[0]) + min(ra[1], rb[1])) / 2
    else:
        z = (rb[3] + ra[2]) / 2
        x = (max(ra[0], rb[0]) + min(ra[1], rb[1])) / 2
    return x, z


def step_link(c, a, b, label="kamachi step"):
    p = kamachi_point(c, a, b)
    c.passage((a, b), p[0], p[1], label)
    return [p]


# ------------------------------------------------------------------------------------------------ sento
def sento(c):
    """Bathhouse: the bandai at the step-up, the footwear shelf; the changing room's cubbies, the nagashi with the
    stools and buckets; the drained tub in the dim bath room; the cold boiler in the lean-to; the noren + lantern."""
    st = step_link(c, "doma", "datsuiba")
    D = Room(c, "doma", open_sides=("xmax",), points=st)
    b = fit1(c, "doma", "bandai")
    x, z = fc(b)
    c.free("doma", "jp_f_bandai", x, z, 270.0, why="the bandai (pay counter) with its cashbox, forced")
    D.used.append((x - 0.50, x + 0.50, z - 0.40, z + 0.40))
    D.wall("jp_f_tana_091_3", sides=("xmin",), why="the footwear shelf, empty")
    D.free("jp_f_debris_leaves", 0.5, 0.6, 20, why="leaves blown in under the noren", count=False, band=False)
    D.wall("jp_f_oke_bucket", why="a bucket")
    D.wall("jp_f_chochin_fallen", why="the night lantern, fallen")
    S = Room(c, "datsuiba", open_sides=("xmin",), points=st)
    S.wall("jp_f_datsui_dana_ransacked", sides=("zmin",), why="the clothes cubbies, ransacked")
    n = fit1(c, "datsuiba", "nagashi")
    nx, nz = fc(n)
    ng = c.free("datsuiba", "jp_f_nagashi_warped", nx, nz, 0.0, why="the washing floor over its drain, warped")
    S.used.append(tuple(n["rect"]))
    c.surf(ng, "jp_f_bath_stools_tipped", why="stools and buckets left on the washing floor")
    S.wall("jp_f_tabakobon_spilled", why="a tobacco tray")
    S.free("jp_f_goban_go_scattered", 0.35, 0.5, 15, why="a go board, stones scattered (bathers' talk and games)")
    S.wall("jp_f_basket_kago_tipped", why="a clothes basket, tipped")
    B = Room(c, "bath", centre=False)
    t = fit1(c, "bath", "tub")
    r = t["rect"]
    sparse(c, "bath", "the bath room: the tub fills it (not a living room)")
    c.free("bath", "jp_f_yubune", (r[0] + r[1]) / 2, r[2] + 1.05, 0.0, why="the bath tub, drained")
    B.used.append((r[0] - 0.05, r[1] + 0.05, r[2] - 0.05, r[2] + 2.48))
    B.wall("jp_f_oke_tipped", sides=("zmin", "zmax"), why="a bucket on its side")
    B.free("jp_f_debris_leaves", 0.3, 0.8, 50, why="leaves", count=False, band=False)
    L = Room(c, "leanto", centre=False)
    sparse(c, "leanto", "the open boiler lean-to (kama-ba)")
    bo = fit1(c, "leanto", "boiler")
    L.wall("jp_f_bath_boiler_ab", sides=("xmin",), why="the boiler's fire mouth, door torn off, ash raked out",
           count=False, band=False)
    L.wall("jp_f_firewood_stack", sides=("xmax",), why="demolition timber for the boiler", count=False, band=False)
    L.free("jp_f_firewood_bundle_loose", 0.5, 0.2, 30, why="brushwood, spilled", count=False, band=False)
    hz = c.R("doma")[3]
    c.front("jp_s_shopfront_noren_long", c.R("doma")[0] + 0.85, hz + 0.18, 0.10, why="the bathhouse noren on the "
            "entrance")
    c.front("jp_s_lantern_sign_chochin_inn", c.R("doma")[0] + 2.20, hz + 0.18, 0.0, why="the bathhouse lantern")


# ------------------------------------------------------------------------------------------------ stable row
def stablerow(c):
    """Stable row: the aisle (fodder cutter, buckets, straw, a dropped saddle pad), the tack room; the yard props."""
    A = Room(c, "stalls", open_sides=("zmax",))
    A.free("jp_f_manger_cutter", 0.15, 0.80, 0, why="the fodder cutter in the aisle")
    A.free("jp_f_manger_straw_rotted", 0.45, 0.75, 0, why="straw, rotting", band=False)
    A.free("jp_f_oke_bucket", 0.62, 0.85, 0, why="a water bucket")
    A.free("jp_f_tawara_kamasu", 0.80, 0.80, 20, why="a bag of fodder")
    A.free("jp_f_debris_straw", 0.30, 0.90, 30, why="straw", count=False, band=False)
    A.free("jp_f_box_m", 0.95, 0.80, 0, why="a feed box")
    T = Room(c, "tack")
    T.onwall("jp_f_tack_wall_taken", sides=("zmin",), why="tack on the pegs, half taken")
    T.wall("jp_f_kori", why="the groom's trunk")
    T.wall("jp_f_rack_half", why="a rack of harness")
    T.wall("jp_f_tawara", why="a rice bale (the groom's ration)")
    T.wall("jp_f_mino_pegs", why="rain capes")
    c.site("jp_s_stable_yard_trough_stone", -2.5, 3.9, 0, why="the stone water trough before the stalls")
    c.site("jp_s_stable_yard_tie_post", 0.0, 4.1, 0, why="tie posts in the yard")
    c.site("jp_s_stable_yard_saddle_rack", -4.2, 3.7, 0, why="the pack-saddle rack")


# ------------------------------------------------------------------------------------------------ booths
def barber(c):
    """Barber's booth: the kit box with its basin, the customer's stool, the hot-water brazier; the waiting bench
    with the shogi board and the tobacco tray."""
    st = step_link(c, "doma", "bench")
    D = Room(c, "doma", open_sides=("zmax",), points=st)
    k = fit1(c, "doma", "barber_kit")
    x, z = fc(k)
    c.free("doma", "jp_f_barber_kit_spilled", x, z, 0.0, why="the barber's kit box, a drawer pulled out")
    D.used.append((x - 0.40, x + 0.40, z - 0.40, z + 0.40))
    s = fit1(c, "doma", "stool")
    D.free("jp_s_stool_std", 0.45, 0.45, 15, why="the customer's stool")
    D.free("jp_f_hibachi_round", 0.15, 0.40, 0, why="the brazier that kept the water hot")
    D.free("jp_f_oke_bucket", 0.15, 0.80, 0, why="the water bucket")
    D.free("jp_f_debris_leaves", 0.6, 0.8, 20, why="leaves", count=False, band=False)
    sparse(c, "bench", "the narrow waiting bench")
    B = Room(c, "bench", open_sides=("zmax",), points=st, centre=False)
    B.free("jp_f_goban_shogi_scattered", 0.12, 0.5, 10, why="a shogi board for the waiting customers, pieces scattered")
    B.free("jp_f_tabakobon", 0.88, 0.5, 0, why="the tobacco tray")
    B.wall("jp_f_box_s", sides=("xmax", "xmin"), why="a box of paper cords and pomade")


def misemono(c):
    """Show booth: plank benches in the pit, the empty cage and the drum on the stage, the painted signboard + banners
    outside."""
    st = step_link(c, "pit", "stage")
    P = Room(c, "pit", points=st)
    P.free("jp_s_bench_1ken", 0.30, 0.55, 0, why="a plank bench")
    P.free("jp_s_bench_1ken", 0.72, 0.55, 0, why="a plank bench")
    P.free("jp_f_chochin_fallen", 0.15, 0.85, 30, why="a lantern, fallen")
    P.free("jp_f_debris_paper", 0.50, 0.85, 10, why="handbills", count=False, band=False)
    P.wall("jp_f_mushiro_pile", why="mats to sit on")
    P.wall("jp_f_oke_bucket", why="a bucket")
    S = Room(c, "stage", points=st, centre=False)
    S.free("jp_f_show_cage_open", 0.30, 0.45, 0, why="the animal cage, empty, bars broken out")
    S.free("jp_f_kagura_drums", 0.72, 0.40, 0, why="the barker's drums")
    S.wall("jp_f_byobu_tsuitate_fallen", why="a screen, fallen")
    S.wall("jp_f_box_m", why="a costume box")
    S.free("jp_f_mushiro_torn", 0.55, 0.65, 0, why="a torn mat", band=False)
    zf = c.R("pit")[3] + 0.06
    c.front("jp_f_misemono_sign_torn", 0.0, zf + 0.08, -0.08, why="the show's painted signboard, torn")
    c.site("jp_s_nobori_shop", -2.1, zf + 0.9, 0, why="a show banner")
    c.site("jp_s_nobori_shop", 2.1, zf + 0.9, 0, why="a show banner")


# ------------------------------------------------------------------------------------------------ workshops
def _ws_room(c, extra):
    st = step_link(c, "doma", "room")
    R = Room(c, "room", open_sides=("xmin",), points=st)
    R.wall("jp_f_zukue_plain", why="the master's desk")
    R.wall("jp_f_box_m", why="a box of finished work")
    R.free("jp_f_enza", 0.5, 0.5, 0, why="a straw cushion")
    R.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")
    for (nm, why) in extra:
        R.wall(nm, why=why)
    return st


def joinery(c):
    """Joiner (tategu-shi / sashimono): planing beam, sawhorses with a board, the open tool chest, frames on the wall,
    tools on the wall; the master's room."""
    st = _ws_room(c, [("jp_f_writing_box", "the plan board and brushes")])
    D = Room(c, "doma", open_sides=("zmax",), points=st)
    w = fit1(c, "doma", "work_centre")
    x, z = fc(w)
    must(D, "jp_f_kezuridai_knocked", "the planing beam, its plane knocked off", sides=("xmin",))
    D.wall("jp_f_frames_lean", sides=("zmin", "xmin"), why="shoji and door frames leaning on the wall")
    D.free("jp_f_sawhorses", 0.30, 0.80, 0, why="sawhorses with a board")
    D.wall("jp_f_dogubako_ransacked", why="the tool chest, tools strewn")
    D.onwall("jp_f_tool_wall_wood", sides=("xmin",), why="saws and planes on the end wall")
    D.free("jp_f_debris_leaves", 0.7, 0.9, 20, why="leaves", count=False, band=False)


def turner(c):
    """Woodturner + abacus maker: the strap lathe, the abacus tray, turned bowls; stock on the wall."""
    st = _ws_room(c, [("jp_f_tableware_bowls", "a stack of turned bowls, unlacquered")])
    D = Room(c, "doma", open_sides=("zmax",), points=st)
    w = fit1(c, "doma", "work_centre")
    x, z = fc(w)
    must(D, "jp_f_rokuro_broken", "the strap lathe, its strap snapped", sides=("xmin",))
    D.free("jp_f_soroban_tray", 0.25, 0.80, 0, why="the abacus maker's tray")
    D.wall("jp_f_rack_half", why="a rack of blanks")
    D.wall("jp_f_basket_kago", why="a basket of beads")
    D.onwall("jp_f_tool_wall", sides=("xmin",), why="gouges and knives on the wall")
    D.wall("jp_f_oke_bucket", why="a bucket")


def basket(c):
    """Bamboo + basket maker: the work place on its mat, poles on the wall, finished trays and baskets."""
    st = _ws_room(c, [("jp_f_basket_zaru_stack", "finished trays")])
    D = Room(c, "doma", open_sides=("zmax",), points=st)
    w = fit1(c, "doma", "work_centre")
    x, z = fc(w)
    D.free("jp_f_basket_work_abandoned", 0.30, 0.25, 0.0, why="the half-woven basket kicked over")
    D.wall("jp_f_bamboo_stock", sides=("xmin",), why="madake poles stood on the wall")
    D.wall("jp_f_basket_back", why="a carrying basket")
    D.wall("jp_f_mi", why="a winnowing basket")
    D.onwall("jp_f_basket_zaru_wall", sides=("zmin",), why="sieves hung on the wall")
    D.wall("jp_f_box_m", why="a box of strips")


def _bench_doma(c):
    D = Room(c, "doma", centre=False)
    D.wall("jp_f_mizugame", why="the water jar")
    D.wall("jp_f_oke_bucket", why="a bucket")
    D.wall("jp_f_firewood_bundle", why="brushwood")
    D.wall("jp_f_tana_091_1", why="a shelf")
    D.free("jp_f_debris_leaves", 0.5, 0.5, 20, why="leaves", count=False, band=False)
    return D


def _bench_kamado(c):
    import w2f_sets as W2
    kd = W2.kamado_spot(c, "doma", n=1)
    W2.pot_in(c, "doma", kd, "jp_f_kama_nolid", 0, "the hot-water pot, cold")


def polisher(c):
    """Sword polisher: the stone holder, water tub and blade stand by the lattice window; blade racks; the back room
    with the sword boxes."""
    _bench_kamado(c)
    st = step_link(c, "doma", "work")
    _bench_doma(c)
    W = Room(c, "work", open_sides=("xmin",), points=st)
    b = fit1(c, "work", "bench_spot")
    x, z = fc(b)
    must(W, "jp_f_togidai", "the polisher's stand by the lattice window", sides=("zmax",))
    W.onwall("jp_f_blade_rack_empty", sides=("xmax",), why="the blade rack, emptied")
    W.wall("jp_f_katanakake_stand_empty", why="a sword stand, empty")
    W.wall("jp_f_box_s", why="a box of finger stones and paper")
    W.wall("jp_f_andon_kaku", why="a lamp, unlit")
    W.free("jp_f_enza", 0.7, 0.3, 0, why="a cushion")
    K = Room(c, "back", centre=False)
    K.wall("jp_f_yoroibitsu_plain", why="a chest of sword mounts")
    K.wall("jp_f_tansu_single_ransacked", why="a chest, drawers pulled")
    K.wall("jp_f_box_l", why="a box of whetstones")
    K.wall("jp_f_kori", why="a trunk")
    K.free("jp_f_andon_ariake_tipped", 0.5, 0.5, 30, why="a night lamp, knocked over")


def lacquer(c):
    """Lacquerer: the work board by the window, wares drying; the dust-free back room with the drying cupboard."""
    _bench_kamado(c)
    st = step_link(c, "doma", "work")
    _bench_doma(c)
    W = Room(c, "work", open_sides=("xmin",), points=st)
    b = fit1(c, "work", "bench_spot")
    x, z = fc(b)
    must(W, "jp_f_urushi_tray_spilled", "the lacquerer's board by the window, a pot spilt", sides=("zmax",))
    r = W.wall("jp_f_rack_half", why="a drying rack")
    W.surf(r, "jp_f_sg_lacquer_scattered", why="lacquered bowls left to dry")
    W.wall("jp_f_box_m_lacquer", why="a lacquered box")
    W.free("jp_f_enza", 0.7, 0.3, 0, why="a cushion")
    W.wall("jp_f_andon_kaku", why="a lamp, unlit")
    K = Room(c, "back", centre=False)
    cb = fit1(c, "back", "cabinet")
    K.wall("jp_f_urushiburo_open", sides=("xmax", "zmin"), why="the drying cupboard (urushi-buro), doors open")
    K.wall("jp_f_box_s_lacquer", why="a lacquered box")
    K.wall("jp_f_rack_half", why="wares curing")
    K.wall("jp_f_jar_s", why="a jar of raw lacquer")
    K.free("jp_f_debris_paper", 0.5, 0.5, 20, why="straining paper", count=False, band=False)
    K.wall("jp_f_box_l", why="a store box")


def kinko(c):
    """Sword-fittings maker: the bench with the pitch bowl and the little forge; the back room store."""
    _bench_kamado(c)
    st = step_link(c, "doma", "work")
    _bench_doma(c)
    W = Room(c, "work", open_sides=("xmin",), points=st)
    b = fit1(c, "work", "bench_spot")
    x, z = fc(b)
    must(W, "jp_f_kinko_bench_taken", "the fittings bench by the window, the guards taken", sides=("zmax",))
    W.onwall("jp_f_kanamono_wall_taken", sides=("xmax",), why="fittings on the wall, half taken")
    W.wall("jp_f_box_s", why="a box of punches")
    W.wall("jp_f_writing_box_open", why="the design book")
    W.free("jp_f_enza", 0.7, 0.3, 0, why="a cushion")
    K = Room(c, "back", centre=False)
    K.wall("jp_f_tansu_ransacked", why="the store chest, ransacked")
    K.wall("jp_f_box_l", why="a box of copper and iron plate")
    K.wall("jp_f_kori", why="a trunk")
    K.wall("jp_f_charcoal_bale", why="charcoal for the little forge")
    K.free("jp_f_andon_ariake_tipped", 0.5, 0.5, 30, why="a night lamp, knocked over")


# ------------------------------------------------------------------------------------------------ timber yard
def saw_shed(c):
    sparse(c, "floor", "the open sawing shed")
    t = fit1(c, "floor", "trestle")
    x, z = fc(t)
    c.free("floor", "jp_f_saw_trestle", x + 0.40, z, 0.0, why="the sawing trestle, the log and the big saw in the kerf")
    c.free("floor", "jp_f_debris_leaves", x - 2.5, z + 0.9, 30, why="leaves", count=False)


def timber_store(c):
    sparse(c, "floor", "the open timber store")
    F = Room(c, "floor", open_sides=("zmax",), centre=False)
    F.wall("jp_f_timber_upright_half", sides=("zmin",), why="timber stood upright on the rack, half taken",
           count=False, band=False)
    p = fit1(c, "floor", "planks")
    x, z = fc(p)
    c.free("floor", "jp_f_plank_stack", x, z + 0.20, 0.0, why="planks air-drying")


def shingle_shed(c):
    sparse(c, "floor", "the shingle splitter's open shed")
    s = fit1(c, "floor", "split_block")
    x, z = fc(s)
    c.free("floor", "jp_f_shingle_split_scattered", x + 0.20, z + 0.20, 0.0, why="the splitting block, froe in a bolt")


# ------------------------------------------------------------------------------------------------ foundry
def foundry(c):
    """Foundry: the cold cupola, the treadle bellows, the sand bed with its moulds, new pots on the rack, scrap,
    ladles on the wall."""
    sparse(c, "doma", "the foundry floor: furnace, bellows and the casting bed fill it")
    F = Room(c, "doma", open_sides=("zmax",), centre=False)
    f = fit1(c, "doma", "furnace")
    fx, fz = fc(f)
    c.free("doma", "jp_f_koshikiro", fx, fz, 180.0, why="the cupola furnace, cold (tuyere towards the bellows)")
    F.used.append((fx - 0.60, fx + 0.60, fz - 0.60, fz + 0.60))
    bx = fx + 2.05
    c.free("doma", "jp_f_fumifuigo", bx, fz + 0.10, 90.0, why="the treadle bellows, its wind trunk to the tuyere")
    F.used.append((bx - 1.50, bx + 0.85, fz - 0.70, fz + 0.80))
    m = fit1(c, "doma", "casting_floor")
    mx, mz = fc(m)
    c.free("doma", "jp_f_imono_moulds_broken", mx - 0.4, mz + 0.1, 0.0, why="the sand bed, a mould knocked open")
    F.used.append((mx - 1.4, mx + 0.6, mz - 0.45, mz + 0.65))
    g = fit1(c, "doma", "goods")
    gx, gz = fc(g)
    F.free("jp_f_cast_pots_scattered", 0.85, 0.30, 90, why="new pots and kettles, two knocked off")
    F.free("jp_f_scrap_heap", 0.85, 0.75, 0, why="scrap iron for the melt")
    F.onwall("jp_f_toribe_rack", sides=("xmin", "zmin"), why="the casting ladles on the wall")
    F.wall("jp_f_charcoal_bales3", why="charcoal bales")


SETS_W3B = {
    "w3b_sento": {"tier": 3, "fn": sento},
    "w3b_stablerow": {"tier": 2, "fn": stablerow},
    "w3b_barber": {"tier": 2, "fn": barber},
    "w3b_misemono": {"tier": 2, "fn": misemono},
    "w3b_joinery": {"tier": 2, "fn": joinery},
    "w3b_turner": {"tier": 2, "fn": turner},
    "w3b_basket": {"tier": 2, "fn": basket},
    "w3b_polisher": {"tier": 3, "fn": polisher},
    "w3b_lacquer": {"tier": 2, "fn": lacquer},
    "w3b_kinko": {"tier": 3, "fn": kinko},
    "w3b_saw_shed": {"tier": 1, "fn": saw_shed},
    "w3b_timber_store": {"tier": 1, "fn": timber_store},
    "w3b_shingle_shed": {"tier": 1, "fn": shingle_shed},
    "w3b_foundry": {"tier": 2, "fn": foundry},
}


def sets():
    return {k: dict(v, fn=D3._wrap(v["fn"])) for k, v in SETS_W3B.items()}
