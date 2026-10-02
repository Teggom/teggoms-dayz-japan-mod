"""W3C1 (2026-10-02): the dressings of the wave-3c-1 furnished variants (the brewery's two kura, the polishing shed, the
cask kura, the brewer's shop, the water mill, the dyer, the paper mill) for buildings/furnishkit.py. SETS_W3C1 are
merged into buildings/furnish_sets.SETS (like d3_sets / w3b_sets).

Binding rules as w3b_sets.py (G1 A2, BUILD_LIST, LIFE_LAYER): 5-7 counted props a room, <= 25 % floor cover, the 1.00 m
bands, >= 1 raised loot surface a room, moderate "as left" disorder; rooms the machinery fills are sparse(). The placer
is D3's (d3_sets.Room); the specialty props sit on the shells' fitting spots (rooms json). Props:
spikes/W3C1/props_w3c1.py (brewfit) + the earlier libraries. Autumn, dead world: the brewery is between seasons
(brewing is winter work), everything dry, cold and still; the work left where it lay.
"""
import d3_sets as D3
from d3_sets import Room, sparse
from w3b_sets import fit1, fc, must, step_link

TOP_POOL = D3.TOP_POOL


def _stair_clear(c, low_room, up_room):
    """The kura stair (c.stairs[0]): its footprint and the well kept clear, passages at the foot and the head."""
    st = c.stairs[0]
    x0 = st["foot"][0]
    c.band_block(low_room, (x0, x0 + st["run"], st["foot"][1], st["foot"][1] + st["width"]))
    c.passage((low_room,), x0 - 0.50, st["foot"][1] + 0.55, "stair foot")
    c.band_block(up_room, st["well"])
    c.passage((up_room,), x0 + st["run"] + 0.45, st["foot"][1] + 0.55, "stair head")
    return st


# ------------------------------------------------------------------------------------------------ the o-kura
def okura(c):
    """The large kura: four big tubs on the fermentation floor (one with its ladder, one fallen apart), the lever press
    along the north wall of the press bay, casks and a Hatcho miso vat by the south wall; under the loft the starter
    tubs and the stirring poles; upstairs (the moto-ba) the shallow starter tubs set out and stacked."""
    _stair_clear(c, "moto", "loft")
    sparse(c, "kura", "the brewing floor: four 1.8 m tubs and the 6 m lever press fill it")
    T = Room(c, "kura", centre=False)
    names = ("jp_f_shikomi_oke", "jp_f_shikomi_oke_ladder", "jp_f_shikomi_oke_staved", "jp_f_shikomi_oke")
    zmid = (c.R("kura")[2] + c.R("kura")[3]) / 2
    for k, (f, nm) in enumerate(zip(c.fit("kura", "tub"), names)):
        x, z = fc(f)
        c.free("kura", nm, x, z, 0.0 if z < zmid else 180.0, why="big fermentation tub (#%d), dry" % (k + 1))
        T.used.append((x - 0.95, x + 0.95, z - 0.95, z + 0.95))
    p = fit1(c, "kura", "press")
    r = p["rect"]
    c.free("kura", "jp_f_fune_press", r[1] - 3.25, (r[2] + r[3]) / 2, 0.0,
           why="the lever press (fune + beam + weight stones), slack")
    T.used.append((r[0], r[1], r[2], r[3] + 0.10))
    cs = fit1(c, "kura", "casks")
    cr = cs["rect"]
    c.free("kura", "jp_f_taru_rack3", cr[0] + 1.00, (cr[2] + cr[3]) / 2 + 0.15, 180.0, why="new casks on their rack")
    c.free("kura", "jp_f_hatcho_oke", cr[1] + 1.10, (cr[2] + cr[3]) / 2 - 0.55, 0.0,
           why="a Hatcho-style miso vat under its stone cone (dressing)")
    T.free("jp_f_oke_bucket", 0.32, 0.50, 0, why="a bucket in the aisle", band=False)
    T.free("jp_f_debris_leaves", 0.30, 0.55, 20, why="leaves blown in", count=False, band=False)
    # under the loft
    M = Room(c, "moto", centre=False)
    M.wall("jp_f_hangiri", sides=("zmax", "xmin"), why="starter tubs stacked by the wall")
    M.wall("jp_f_kai_poles", sides=("zmax", "xmin"), why="stirring poles")
    M.wall("jp_f_hashigo", sides=("zmax", "xmin"), why="a ladder for the tub rims")
    M.wall("jp_f_oke_bucket", why="a bucket")
    M.wall("jp_f_jar_l", why="a water jar")
    M.free("jp_f_debris_leaves", 0.6, 0.5, 40, why="leaves", count=False, band=False)
    # the loft (moto-ba)
    L = Room(c, "loft", centre=False)
    L.free("jp_f_hangiri_scattered", 0.55, 0.62, 0, why="starter tubs knocked about")
    L.wall("jp_f_hangiri", sides=("zmax", "xmin"), why="starter tubs stacked")
    L.wall("jp_f_box_l", why="a box of cloth bags")
    L.wall("jp_f_tawara_kamasu_stack3", why="straw sacks")
    L.wall("jp_f_oke_tipped", why="a bucket on its side")


# ------------------------------------------------------------------------------------------------ the mae-gura
def maegura(c):
    """The front kura: the steaming hearth with its koshiki under the vent, the washing tubs of the araiba, firewood;
    the koji ante-room; the straw-lined muro with the koji bed and the tray shelves; the brewers' rest room."""
    h = fit1(c, "kama", "hearth")
    x, z = fc(h)
    c.free("kama", "jp_f_kamaba", x, z, 0.0, why="the steaming hearth: kamado + cauldron + koshiki, cold")
    K = Room(c, "kama", centre=False)
    K.used.append((x - 1.45, x + 1.45, z - 1.05, z + 1.30))
    K.wall("jp_f_firewood_stack", sides=("zmin",), why="firewood for the hearth")
    K.wall("jp_f_hangiri_scattered", sides=("zmin", "xmin"), why="washing tubs of the araiba, knocked about")
    K.wall("jp_f_oke_tarai", sides=("xmin", "zmin"), why="a washing tub")
    K.wall("jp_f_kai_poles", sides=("xmin", "zmin"), why="stirring poles and a broom")
    K.free("jp_f_oke_bucket", 0.20, 0.55, 0, why="a bucket")
    K.wall("jp_f_tawara_stack6", sides=("zmin", "xmin"), why="rice bales for the next season")
    K.free("jp_f_debris_leaves", 0.5, 0.7, 10, why="leaves", count=False, band=False)
    # the ante-room
    sparse(c, "mae", "the small ante-room between the two koji doors")
    A = Room(c, "mae", centre=False)
    A.wall("jp_f_box_m", why="a box of cloths")
    A.wall("jp_f_oke_bucket", why="a bucket")
    # the muro
    sparse(c, "muro", "the koji room: the bed and the shelves fill it")
    t = fit1(c, "muro", "toko")
    tx, tz = fc(t)
    c.free("muro", "jp_f_koji_toko_ab", tx, tz, 0.0, why="the koji bed, its cloth dragged off")
    U = Room(c, "muro", centre=False)
    U.used.append((tx - 0.95, tx + 0.95, tz - 0.65, tz + 0.65))
    U.wall("jp_f_kojibuta_tana_ab", sides=("zmin",), why="the tray shelves, half pulled down")
    # the kaishoba
    st = step_link(c, "kaidoma", "kaisho")
    sparse(c, "kaidoma", "the rest room's small entrance doma")
    E = Room(c, "kaidoma", points=st, centre=False)
    E.wall("jp_f_tana_091_1", why="a footwear shelf")
    R = Room(c, "kaisho", open_sides=("zmax",), points=st)
    R.wall("jp_f_kori", why="a brewer's trunk")
    R.wall("jp_f_futon_stack_slumped", why="bedding, the stack slumped")
    R.free("jp_f_tabakobon_spilled", 0.5, 0.5, 0, why="a tobacco tray")
    R.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")
    R.free("jp_f_enza", 0.3, 0.4, 0, why="a straw cushion")
    R.wall("jp_f_mino_pegs", why="rain capes on pegs")


# ------------------------------------------------------------------------------------------------ polishing shed
def seimai(c):
    """The rice-polishing shed: four foot-treadle mortars (one broken), rice bales and sacks, a sieve."""
    sparse(c, "floor", "the open polishing shed: four treadle mortars fill it")
    fs = c.fit("floor", "karausu")
    for k, f in enumerate(fs):
        x, z = fc(f)
        c.free("floor", "jp_f_karausu_broken" if k == 2 else "jp_f_karausu", x, z + 0.10, 0.0,
               why="foot-treadle mortar (#%d)%s" % (k + 1, ", the lever off its pivot" if k == 2 else ""))
    c.site("jp_f_tawara_stack6", 0.0, c.R("floor")[3] + 1.6, 0, why="rice bales waiting to be polished")
    c.site("jp_f_tawara_burst", 2.6, c.R("floor")[3] + 1.4, 30, why="a burst rice bale")


# ------------------------------------------------------------------------------------------------ cask kura
def kura_casks(c):
    """The brewery's cask kura (C3's kura_storage spots): casks on racks and loose on both floors, measures, sacks."""
    st = _stair_clear(c, "kura", "nikai")
    rk = c.wall("kura", "xmax", 0.00, "jp_f_taru_rack3", why="casks on a rack against the gable")
    c.wall("kura", "zmax", -1.90, "jp_f_taru_komo", why="a straw-wrapped cask by the front wall")
    c.free("kura", "jp_f_taru_cask", -1.20, 0.90, 0, why="a cask")
    c.free("kura", "jp_f_tawara_stack6", 0.90, 0.60, 0, why="rice bales")
    c.free("kura", "jp_f_taru_komo", -2.15, 0.90, 0, why="a straw-wrapped cask")
    if rk is not None:
        c.surf(rk, "jp_f_masu_set", why="measures left on the casks")
    c.wall("nikai", "zmax", -1.30, "jp_f_taru_rack3_ab", why="empty casks, two rolled off")
    c.wall("nikai", "zmax", 1.30, "jp_f_rack_1ken", why="shelving")
    c.free("nikai", "jp_f_taru_cask", -2.10, -0.30, 0, why="a cask")
    c.free("nikai", "jp_f_tawara_kamasu_stack3", 0.90, 0.90, 0, why="empty sacks")
    c.free("nikai", "jp_f_box_l", -2.20, -1.25, 0, why="a box of cloth bags")


# ------------------------------------------------------------------------------------------------ brewer's shop
def sakaya(c):
    """The brewer's shop at the lane (the earth-floor workshop shell): casks on racks, measures and flasks on a cask,
    the counting desk in the raised room; the big brown sugidama hung under the front beam."""
    st = step_link(c, "doma", "room")
    R = Room(c, "room", open_sides=("xmin",), points=st)
    R.wall("jp_f_zukue_plain", why="the counting desk")
    R.wall("jp_f_box_m", why="a ledger box")
    R.free("jp_f_enza", 0.5, 0.5, 0, why="a straw cushion")
    R.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")
    R.wall("jp_f_box_s", why="a box of tallies")
    D = Room(c, "doma", open_sides=("zmax",), points=st)
    D.wall("jp_f_taru_rack3", sides=("zmin",), why="casks on their rack")
    D.wall("jp_f_taru_rack3_ab", sides=("zmin", "xmin"), why="casks, two rolled off")
    k = D.free("jp_f_taru_komo", 0.30, 0.75, 0, why="a cask to sit on")
    if k is not None:
        c.surf(k, "jp_f_masu_set", why="measures left on the cask")
    D.wall("jp_f_oke_bucket", why="a bucket")
    # the sugidama under the open front's head beam (anchor 'hang'): beam underside = the shell's YT - 0.40
    from jpparts.core import KETA_H
    y_beam = 3.30 - KETA_H - 0.40
    x0, x1, z0, z1 = c.R("doma")
    c.front("jp_f_sakabayashi", x0 + 0.40, z1 + 0.15, y_beam, 0.0, why="the brewery's sugidama, brown")


# ------------------------------------------------------------------------------------------------ water mill
def suisha(c):
    """The mill floor: the hand quern, rice bales and sacks, sieves, a bucket; the stamps are the shell's."""
    sparse(c, "floor", "the mill floor: the stamps and their frame fill the middle")
    q = fit1(c, "floor", "quern")
    x, z = fc(q)
    c.free("floor", "jp_f_usu_ishiusu", x, z, 0.0, why="the stone hand mill (ishi-usu)")
    F = Room(c, "floor", centre=False)
    F.used.append((x - 0.40, x + 0.40, z - 0.40, z + 0.40))
    F.wall("jp_f_tawara_stack6", sides=("xmax", "zmax"), why="rice bales")
    F.wall("jp_f_tawara_kamasu_stack3", sides=("zmin", "xmin"), why="grain sacks")
    F.free("jp_f_mi_furui", 0.15, 0.70, 0, why="a sieve", band=False)
    F.free("jp_f_oke_bucket", 0.85, 0.70, 0, why="a bucket", band=False)


# ------------------------------------------------------------------------------------------------ dyer
def konya(c):
    """The dyer: the shop doma with dyed cloth on a shelf, the counting desk, the shop-front cloths hung under the front
    beam; the vat room round the sunk vats: sukumo bales, the lye tubs, the pole rack, buckets."""
    sparse(c, "aiba", "the vat room: the vat bank fills its middle")
    A = Room(c, "aiba", centre=False)
    b = fit1(c, "aiba", "bales")
    br = b["rect"]
    x, z = br[0] + 0.36, br[2] + 1.06
    c.free("aiba", "jp_f_sukumo_bales", x, z, 90.0, why="sukumo indigo in straw bales, along the west wall")
    A.used.append((x - 0.36, x + 0.36, z - 1.08, z + 1.08))
    l_ = fit1(c, "aiba", "lye")
    lx, lz = fc(l_)
    c.free("aiba", "jp_f_akumizu", lx + 0.05, lz, 0.0, why="the lye drip tubs and the lime tub")
    A.used.append((lx - 1.05, lx + 0.45, lz - 0.45, lz + 0.45))
    A.wall("jp_f_dye_rack", sides=("zmin",), why="stirring poles and a dripping length on the wringing bar")
    A.wall("jp_f_oke_bucket", why="a bucket")
    A.free("jp_f_oke_tipped", 0.75, 0.35, 0, why="a bucket on its side", band=False)
    S = Room(c, "mise", open_sides=("zmax",), centre=False)
    S.wall("jp_f_tana_091_3", sides=("xmin", "xmax"), why="the cloth shelf")
    S.wall("jp_f_goods_general_cloth_swept", sides=("zmin", "xmax"), why="bolts of dyed cloth swept to the floor")
    S.wall("jp_f_zukue_plain", sides=("xmax", "zmin"), why="the counting desk")
    S.wall("jp_f_box_m", why="a box of cloth")
    S.free("jp_f_debris_leaves", 0.5, 0.7, 10, why="leaves", count=False, band=False)
    from jpparts.core import KETA_H
    y_beam = 3.40 - KETA_H - 0.40
    x0, x1, z0, z1 = c.R("mise")
    c.front("jp_f_shibori_front", x0 + 1.55, z1 + 0.15, y_beam, 0.0, why="dyed cloths hung at the shop front "
            "(the Arimatsu flavour)")
    c.front("jp_f_shibori_front_torn", x0 + 4.20, z1 + 0.15, y_beam, 0.0, why="shop-front cloths, torn")


# ------------------------------------------------------------------------------------------------ paper mill
def kamisuki(c):
    """The paper workshop: the vat with its mould, the picking tub, the beating board, the couching press; the bark
    steamer under the lean-to."""
    sparse(c, "floor", "the paper workshop: vat, beating board and press fill the floor")
    for kind, nm, why, yaw in (("vat", "jp_f_sukibune", "the paper vat with the mould and its spring pole", 0.0),
                               ("chiritori", "jp_f_oke_tarai_dry", "the picking tub, dry", 0.0),
                               ("beat", "jp_f_kozo_beat_scattered", "the beating board, mallets strewn", 0.0),
                               ("press", "jp_f_shime_press", "the couching stack under its lever press", 0.0)):
        f = fit1(c, "floor", kind)
        x, z = fc(f)
        c.free("floor", nm, x, z, yaw, why=why)
    F = Room(c, "floor", centre=False)
    F.wall("jp_f_basket_kago", why="a basket of bark")
    sparse(c, "leanto", "the open lean-to: the bark steamer")
    s = fit1(c, "leanto", "steamer")
    x, z = fc(s)
    c.free("leanto", "jp_f_kozo_kama", x, z, 90.0, why="the bark steamer, cold")


SETS_W3C1 = {
    "w3c1_okura": {"tier": 2, "fn": okura},
    "w3c1_maegura": {"tier": 2, "fn": maegura},
    "w3c1_seimai": {"tier": 1, "fn": seimai},
    "w3c1_kura_casks": {"tier": 2, "fn": kura_casks},
    "w3c1_sakaya": {"tier": 2, "fn": sakaya},
    "w3c1_suisha": {"tier": 1, "fn": suisha},
    "w3c1_konya": {"tier": 2, "fn": konya},
    "w3c1_kamisuki": {"tier": 1, "fn": kamisuki},
}


def sets():
    return {k: dict(v, fn=D3._wrap(v["fn"])) for k, v in SETS_W3C1.items()}
