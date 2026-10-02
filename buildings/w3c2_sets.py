"""W3C2 (2026-10-02): the dressings of the wave-3c-2 furnished variants (the earlier huts, sheds and workshops each site
reuses + the two new halls) for buildings/furnishkit.py. SETS_W3C2 are merged into buildings/furnish_sets.SETS (like
w3c1_sets). Binding rules as w3c1_sets.py (G1 A2, BUILD_LIST, LIFE_LAYER): 5-7 counted props a room, <= 25 % floor
cover, the 1.00 m bands, >= 1 raised loot surface a room, moderate "as left" disorder; rooms the machinery fills are
sparse(). Props: spikes/W3C2/props_w3c2.py (sitefit) + the earlier libraries. Autumn, dead world: every kiln cold, the
camps left, the work where it lay. Research + recorded choices: spikes/W3C2/W3C2_NOTES.md.
"""
import d3_sets as D3
from d3_sets import Room, sparse
from w3b_sets import fit1, fc, must, step_link
import furnish_sets as FS


def _beam_over(c, x, z, y, reach=0.60):
    """The underside of the lowest building face right over (x, z) above y (a vertical ray against the Resolution-1
    faces): the kit's irori hook height sits a few cm under the tie beam (hangcheck, the C2 huts' baseline); hang the
    pot hook from the real member instead."""
    best = None
    for s_ in c.M.solids:
        if 1 not in s_.vis:
            continue
        b = s_.bbox()
        if not (b[0] - 0.01 <= x <= b[1] + 0.01 and b[4] - 0.01 <= z <= b[5] + 0.01 and b[3] >= y - 0.02
                and b[2] <= y + reach):
            continue
        for fi in range(len(s_.faces)):
            P = s_.face_points(fi)
            n = s_.fn[fi]
            if abs(n[1]) < 1e-6:
                continue
            # the face plane's height at (x, z), then inside the face's plan polygon
            yy = P[0][1] - (n[0] * (x - P[0][0]) + n[2] * (z - P[0][2])) / n[1]
            if not (y - 0.02 <= yy <= y + reach):
                continue
            inside, k = True, len(P)
            sg = 0
            for a in range(k):
                p0, p1 = P[a], P[(a + 1) % k]
                cr = (p1[0] - p0[0]) * (z - p0[2]) - (p1[2] - p0[2]) * (x - p0[0])
                if abs(cr) < 1e-9:
                    continue
                if sg == 0:
                    sg = 1 if cr > 0 else -1
                elif (cr > 0) != (sg > 0):
                    inside = False
                    break
            if inside:
                best = yy if best is None else min(best, yy)
    return best if best is not None else y


def _hut_living(c, bed_side, bed_at, bed):
    """furnish_sets._hut_living with the pot hook hung from the real beam over the irori (W3C2: hangcheck)."""
    f = c.fit("living", "irori")[0]
    hx, hy, hz = f["hook"]
    c.hang("living", "jp_f_jizai_kagi_plain_abandoned", hx, hz, _beam_over(c, hx, hz, hy), over="hearth",
           why="the pot hook over the irori")
    c.wall("living", bed_side, bed_at, bed, why="the straw bed (no tatami, no futon)")
    return f


# ------------------------------------------------------------------------------------------------ 1 charcoal burner's hut
def sumiyaki(c):
    """The charcoal burner's hut (C2's west hut, thatch, board floor): the one-mouth stove, the water jar, axe and saw
    on the pegs, charcoal in bales by the door; the straw bed round the irori. Outside: billets and bales."""
    FS._kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama_nolid", 0, why="the pot left in the stove")
    c.onwall("doma", "xmin", 0.40, "jp_f_tool_wall_wood", why="axe, hatchet and saw on pegs")
    Dm = Room(c, "doma", centre=False)
    Dm.wall("jp_f_jar_l", why="the water jar")
    Dm.wall("jp_f_charcoal_bale", why="a bale of charcoal, ready to carry down")
    Dm.wall("jp_f_charcoal_scuttle", why="a charcoal scuttle")
    Dm.wall("jp_f_oke_bucket", why="a bucket")
    c.passage(("doma", "living"), -0.91, 0.0, "kamachi step doma <-> living")
    f = _hut_living(c, "xmax", 0.0, bed="jp_f_straw_bed_pile")
    c.free("living", "jp_f_kama_nabe_rusted", 0.20, 0.90, 0, why="a pot by the hearth")
    c.free("living", "jp_f_mushiro_torn", 0.60, 0.85, 0, why="a torn straw mat")
    c.free("living", "jp_f_basket_back", -0.30, -1.30, 0, why="a back basket for the bales")
    c.free("living", "jp_f_tabakobon_spilled", 1.10, -1.20, 0, why="a tobacco tray")
    c.free("living", "jp_f_box_s", 2.30, 1.30, 0, why="a small box")
    c.site("jp_f_charcoal_bales3", 0.90, 2.75, 0, why="charcoal in straw bales by the door, ready to carry down")
    c.site("jp_f_charcoal_burst", 2.40, 2.60, 20, why="a burst charcoal bale")
    c.site("jp_f_firewood_stack", -3.55, 0.0, 90, why="split wood stacked against the gable")


# ------------------------------------------------------------------------------------------------ 2 potter's workshop
def toki(c):
    """The potter's work shed (W3B's earth-floor workshop, board roof): the kick wheel by the open front's light, the
    wedging board with the clay heap, the ware-drying racks along the back wall, glaze tubs and jars; in the raised
    room the finished wares packed in straw and the master's desk."""
    st = step_link(c, "doma", "room")
    sparse(c, "doma", "the potter's floor: wheel, wedging board and racks fill it")
    D = Room(c, "doma", open_sides=("zmax",), points=st, centre=False)
    must(D, "jp_f_ware_rack", "the ware-drying rack: rows of unfired bowls", sides=("zmin",))
    must(D, "jp_f_neri_ban", "the wedging board with clay, the clay heap beside it", sides=("zmin",))
    must(D, "jp_f_keri_rokuro", "the kick wheel with a half-thrown jar gone dry")
    D.wall("jp_f_oke_tarai_dry", sides=("zmin", "zmax"), why="a glaze tub, dried out")
    D.wall("jp_f_jar_m_open", sides=("zmin", "zmax"), why="a glaze jar")
    R = Room(c, "room", open_sides=("xmin",), points=st)
    R.wall("jp_f_wares_straw", why="finished wares packed in straw for the road")
    R.wall("jp_f_zukue_plain", why="the master's desk")
    R.wall("jp_f_box_m", why="a box of brushes and tools")
    R.free("jp_f_enza", 0.5, 0.5, 0, why="a straw cushion")
    R.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")


# ------------------------------------------------------------------------------------------------ 3 tile works
def kawara(c):
    """The tile maker's moulding shed (W3B's tiled earth-floor workshop): the moulding bench with the mould, the wire
    cutter and a half-carved onigawara, the wedging board with the clay heap, a rack of green tiles; in the raised room
    the tally desk."""
    st = step_link(c, "doma", "room")
    sparse(c, "doma", "the moulding floor: bench, wedging board and a rack fill it")
    D = Room(c, "doma", open_sides=("zmax",), points=st, centre=False)
    must(D, "jp_f_kawara_bench", "the moulding bench: mould, wire cutter, a half-carved onigawara", sides=("zmin",))
    must(D, "jp_f_neri_ban", "the wedging board with the clay heap", sides=("zmin",))
    must(D, "jp_f_kawara_rack", "green tiles drying on the rack", sides=("zmin", "xmin"))
    D.wall("jp_f_oke_bucket", sides=("zmin", "zmax"), why="a water bucket")
    D.wall("jp_f_tawara_kamasu_stack3", sides=("zmin", "zmax"), why="sacks of sand for the moulds")
    R = Room(c, "room", open_sides=("xmin",), points=st)
    R.wall("jp_f_zukue_plain", why="the tally desk")
    R.wall("jp_f_box_m", why="a box of tallies")
    R.free("jp_f_enza", 0.5, 0.5, 0, why="a straw cushion")
    R.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")
    R.wall("jp_f_tabakobon_spilled", why="a tobacco tray")


def kawara_dry(c):
    """The tile drying shed (C2's open board shed): racks of green tiles along the back, one collapsed, a pallet of
    fired tiles waiting for the carts."""
    sparse(c, "floor", "the drying shed: tile racks fill it")
    F = Room(c, "floor", open_sides=("zmax",), centre=False)
    must(F, "jp_f_kawara_rack", "green tiles drying on the rack", sides=("zmin",))
    must(F, "jp_f_kawara_rack", "a second rack of green tiles", sides=("zmin",))
    must(F, "jp_f_kawara_rack_collapsed", "a rack collapsed, its top shelf of tiles broken", sides=("xmin", "xmax"))
    must(F, "jp_f_kawara_stack", "fired tiles stacked for the carts")
    F.wall("jp_f_oke_bucket", why="a bucket")
    F.wall("jp_f_basket_work", why="a work basket")


# ------------------------------------------------------------------------------------------------ 4 lime
def ishibai(c):
    """The lime burner's slaking and packing shed (C2's open thatch shed): the slaked lime sieved and packed in straw
    bales [OME], sacks waiting, the slaking tub, the sieves, shovels on the wall. Outside: the brushwood for the burn."""
    sparse(c, "floor", "the open slaking shed: bales and tubs")
    F = Room(c, "floor", open_sides=("zmax",), centre=False)
    must(F, "jp_f_tawara_stack6", "slaked lime packed in straw bales", sides=("zmin",))
    must(F, "jp_f_tawara_kamasu_stack3", "straw sacks of lime", sides=("zmin", "xmin"))
    F.wall("jp_f_oke_tarai_dry", why="the slaking tub, dry, white-crusted")
    F.wall("jp_f_mi_furui", why="the sieve")
    F.wall("jp_f_tool_wall", sides=("zmin",), why="shovels and rakes on the wall")
    F.wall("jp_f_oke_bucket", why="a water bucket")
    F.free("jp_f_tawara_burst", 0.70, 0.55, 20, why="a burst bale of lime")
    c.site("jp_f_firewood_bundle_loose", -3.70, 0.40, 90, why="brushwood bundles for the burn")
    c.site("jp_f_firewood_bundle", -3.70, -0.90, 90, why="brushwood bundles")


# ------------------------------------------------------------------------------------------------ 5 quarry
def ishiku(c):
    """The quarrymen's shed (C2's open board shed): the sharpening forge for the picks and wedges (W2F's forge and
    anvil), the quench tub, charcoal, chisels and wedges on the wall; the stonemason's finished lanterns stand outside
    (placed with the site)."""
    sparse(c, "floor", "the open shed: the sharpening forge fills one end")
    F = Room(c, "floor", open_sides=("zmax",), centre=False)
    must(F, "jp_f_forge", "the small sharpening forge for picks and wedges", sides=("zmin",))
    must(F, "jp_f_anvil", "the anvil")
    F.wall("jp_f_oke_tarai_dry", why="the quench tub, dry")
    F.wall("jp_f_charcoal_bale", why="charcoal for the forge")
    F.wall("jp_f_tool_wall", sides=("zmin",), why="chisels, points and wedges on the wall")
    F.wall("jp_f_basket_work", why="a basket of wedges")


# ------------------------------------------------------------------------------------------------ 6 mine
def senko(c):
    """The mine's sorting shed (C2's open board shed): the sorting bench with hammers and ore, the stone ore mill
    (the hand quern), ore baskets, the gold-washing sluice by the open front."""
    sparse(c, "floor", "the open sorting shed: bench, mill and sluice fill it")
    F = Room(c, "floor", open_sides=("zmax",), centre=False)
    must(F, "jp_f_senko_dai", "the ore sorting bench, hammers and broken ore", sides=("zmin",))
    must(F, "jp_f_nekonagashi", "the gold-washing sluice, dry", sides=("zmin",))
    must(F, "jp_f_usu_ishiusu", "the stone mill that ground the ore")
    F.wall("jp_f_basket_back", why="an ore basket")
    F.wall("jp_f_basket_work_abandoned", why="an ore basket, dropped")
    F.wall("jp_f_oke_bucket", why="a bucket")


def bunk_miners(c):
    """The miners' bunk hall (board roof): in the doma the stove, the water jar, picks and hammers on the wall, ore
    baskets; on the long sleeping floor the straw beds round the irori, clothes on pegs, the men's few things left."""
    FS._kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama_nolid", 0, why="the pot left in the stove")
    c.passage(("doma", "living"), -1.82, 0.35, "kamachi step doma <-> living")
    D = Room(c, "doma", centre=False)
    D.wall("jp_f_jar_l", why="the water jar")
    D.wall("jp_f_tool_wall", sides=("xmin",), why="picks, hammers and chisels on the wall")
    D.wall("jp_f_basket_back_crushed", why="an ore basket, crushed")
    D.wall("jp_f_oke_bucket", why="a bucket")
    D.wall("jp_f_firewood_bundle", why="firewood")
    f = _hut_living(c, "xmax", 0.0, bed="jp_f_straw_bed_pile")
    c.wall("living", "zmin", 1.60, "jp_f_straw_bed_scattered", why="another straw bed, kicked about")
    L = Room(c, "living", centre=False)
    L.wall("jp_f_mino_pegs", sides=("zmax", "zmin"), why="rain capes and hats on the pegs")
    L.wall("jp_f_kori", why="a wicker trunk")
    L.free("jp_f_kama_nabe_rusted", 0.45, 0.55, 0, why="a rusting pot by the hearth", band=False)
    L.free("jp_f_meal_left_hakozen", 0.60, 0.35, 0, why="a box-tray meal left", band=False)
    L.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")


# ------------------------------------------------------------------------------------------------ 7 logging camp
def bunk_loggers(c):
    """The loggers' bunk hall (stone-weighted roof): axes, felling saws and wedges on the wall, coils of rope, the stove
    and the water jar in the doma; straw beds round the irori, rain capes on pegs."""
    FS._kamado_on_spot(c, "doma", 1)
    c.pot("doma", "jp_f_kama", 0, why="the pot, lid on, in the stove")
    c.passage(("doma", "living"), -1.82, 0.35, "kamachi step doma <-> living")
    D = Room(c, "doma", centre=False)
    D.wall("jp_f_jar_l", why="the water jar")
    D.wall("jp_f_tool_wall_wood", sides=("xmin",), why="axes, felling saws and wedges on the pegs")
    D.wall("jp_f_rope_pegs_3", why="coils of hauling rope")
    D.wall("jp_f_firewood_stack", sides=("zmin",), why="split wood")
    D.wall("jp_f_oke_bucket", why="a bucket")
    f = _hut_living(c, "xmax", 0.0, bed="jp_f_straw_bed_quilt")
    c.wall("living", "zmin", 1.60, "jp_f_straw_bed_pile", why="another straw bed")
    L = Room(c, "living", centre=False)
    L.wall("jp_f_mino_pegs_rain", sides=("zmax", "zmin"), why="rain capes and hats on the pegs")
    L.wall("jp_f_kori", why="a wicker trunk")
    L.free("jp_f_kama_nabe", 0.45, 0.55, 0, why="a pot by the hearth", band=False)
    L.free("jp_f_tabakobon_spilled", 0.60, 0.35, 0, why="a tobacco tray", band=False)
    L.wall("jp_f_andon_kaku_tipped", why="a lamp, knocked over")


# ------------------------------------------------------------------------------------------------ 8 salt works
def kamaya(c):
    """The salt-boiling hut: the shell pan is the shell's; round it the fuel heap of pine needles and bamboo leaves
    [GYO] on its spot, the salt draining baskets, brine tubs and jars, salt in straw bags, rakes on the wall. Cold."""
    sparse(c, "floor", "the boiling floor: the pan and its firebox fill the middle")
    fu = fit1(c, "floor", "fuel")
    x, z = fc(fu)
    c.free("floor", "jp_f_matsuba", x, z, 0.0, why="the fuel heap of pine needles and bamboo leaves")
    F = Room(c, "floor", centre=False)
    r = fu["rect"]
    F.used.append((r[0] - 0.10, r[1] + 0.10, r[2] - 0.10, r[3] + 0.10))
    must(F, "jp_f_shio_zaru", "salt draining in baskets over the trough", sides=("zmin", "xmax"))
    F.wall("jp_f_tawara_stack6", sides=("xmax", "zmin"), why="salt in straw bags (shio-dawara)")
    F.wall("jp_f_oke_tarai_dry", why="a brine tub, dry, salt-crusted")
    F.wall("jp_f_jar_l_open", why="a brine jar")
    F.wall("jp_f_tool_wall_wood", sides=("zmin", "xmin"), why="rakes and the long pan scraper on the wall")
    F.wall("jp_f_oke_bucket", why="a bucket")


SETS_W3C2 = {
    "w3c2_sumiyaki": {"tier": 1, "fn": sumiyaki},
    "w3c2_toki": {"tier": 1, "fn": toki},
    "w3c2_kawara": {"tier": 1, "fn": kawara},
    "w3c2_kawara_dry": {"tier": 1, "fn": kawara_dry},
    "w3c2_ishibai": {"tier": 1, "fn": ishibai},
    "w3c2_ishiku": {"tier": 1, "fn": ishiku},
    "w3c2_senko": {"tier": 1, "fn": senko},
    "w3c2_bunk_miners": {"tier": 1, "fn": bunk_miners},
    "w3c2_bunk_loggers": {"tier": 1, "fn": bunk_loggers},
    "w3c2_kamaya": {"tier": 1, "fn": kamaya},
}


def sets():
    return {k: dict(v, fn=D3._wrap(v["fn"])) for k, v in SETS_W3C2.items()}
