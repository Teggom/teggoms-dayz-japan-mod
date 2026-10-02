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
    f = FS._hut_living(c, "xmax", 0.0, bed="jp_f_straw_bed_pile")
    c.free("living", "jp_f_kama_nabe_rusted", 0.20, 0.90, 0, why="a pot by the hearth")
    c.free("living", "jp_f_mushiro_torn", 0.30, 1.30, 0, why="a torn straw mat")
    c.free("living", "jp_f_basket_back", -0.30, -1.30, 0, why="a back basket for the bales")
    c.free("living", "jp_f_tabakobon_spilled", 1.10, -1.20, 0, why="a tobacco tray")
    c.free("living", "jp_f_box_s", 2.30, 1.30, 0, why="a small box")
    hx, hy, hz = f["hook"]
    c.hang("living", "jp_f_drying_daikon_shrivelled", hx, 1.30, hy, over="corner", why="daikon drying, shrivelled")
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


SETS_W3C2 = {
    "w3c2_sumiyaki": {"tier": 1, "fn": sumiyaki},
    "w3c2_toki": {"tier": 1, "fn": toki},
    "w3c2_kawara": {"tier": 1, "fn": kawara},
    "w3c2_kawara_dry": {"tier": 1, "fn": kawara_dry},
    "w3c2_ishibai": {"tier": 1, "fn": ishibai},
}


def sets():
    return {k: dict(v, fn=D3._wrap(v["fn"])) for k, v in SETS_W3C2.items()}
