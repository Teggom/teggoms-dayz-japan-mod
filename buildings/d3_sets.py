"""D3 (2026-10-01): the dressings of the wave-3a furnished variants (dwellings, outbuildings, the nagaya-mon, the
honjin) for buildings/furnishkit.py. SETS_D3 are merged into buildings/furnish_sets.SETS (like w2f_sets / shop_sets).

Binding rules as furnish_sets.py (G1 A2, BUILD_LIST, LIFE_LAYER): 5-7 counted props a room, <= 25 % floor cover, a
1.00 m band door-to-door and door-to-centre, >= 1 raised loot surface a room, moderate "as left" disorder; butsudan /
kamidana / tokonoma undisturbed and without loot; andon unlit; no tokonoma dressing in commoner houses (G1 A2: the
shells have none); zabuton and tea sets only in T3 houses; T1 = no tatami, no futon. Autumn, dead world.
Placement: a small placer (Room) puts wall-backed props along walls clear of the door zones (0.55 m each side of an
opening), the 1.00 m bands (door-to-door, door-to-centre, kamachi steps) and the floor obstacles (fittings), so the
decor checks D1-D10 pass by construction; the dressing names WHAT goes in each room, the placer finds WHERE.
"""
import math

from jpparts import decor as DC, mlod, checks as C

SIDES = ("zmin", "zmax", "xmin", "xmax")
GEO = {"class": "house", "map": "house", "damage": "no", "autocenter": "0"}
WALL_INSET = 0.005


def sparse(c, room, why):
    c.room[room]["sparse"] = why


def openings(c):
    """Door openings of the base model (model frame): {DoorsTwinN: (along_x, (lo, hi), wall)} (decor.door_opening)."""
    if getattr(c, "_d3_ops", None) is None:
        lods = c.M.lods(geo_props=GEO, mass=1000.0)
        L = {mlod.lod_name(l.resolution): l for l in lods}
        g = C.components(L["Geometry"])
        ops = {}
        for k, d in enumerate(c.M.doors, 1):
            if getattr(d, "passable", True):
                o = DC.door_opening(d, g)
                if o:
                    ops["DoorsTwin%d" % k] = o
        c._d3_ops = ops
    return c._d3_ops


def _overlap(a, b, m=0.0):
    return a[0] < b[1] + m and b[0] < a[1] + m and a[2] < b[3] + m and b[2] < a[3] + m


class Room:
    """The placer for one room (see the module docstring)."""

    def __init__(self, c, name, open_sides=(), points=(), centre=True):
        self.c, self.n = c, name
        if not hasattr(c, "_d3_rooms"):
            c._d3_rooms = []
        c._d3_rooms.append(self)
        self.open_sides = tuple(open_sides)
        self.r = c.R(name)
        x0, x1, z0, z1 = self.r
        self.cx, self.cz = (x0 + x1) / 2, (z0 + z1) / 2
        self.used = [tuple(o) for o in c.floor[name]["obstacles"]] if name in c.floor else []
        self.blk = {s: [] for s in SIDES}
        ends = []
        for dn in c.room[name].get("doors", []):
            o = openings(c).get(dn)
            if not o:
                continue
            ax, (lo, hi), wall = o
            if ax:
                dz0, dz1 = abs(wall - z0), abs(wall - z1)
                side = "zmin" if dz0 < dz1 else "zmax"
                if min(dz0, dz1) < 0.7:
                    self.blk[side].append((lo - 1.45, hi + 1.45))
                self.used.append((lo - 0.50, hi + 0.50, wall - 0.80, wall + 0.80))
                self.used.append((lo - 1.45, hi + 1.45, wall - 0.30, wall + 0.30))
                ends.append(((lo + hi) / 2, wall))
            else:
                dx0, dx1 = abs(wall - x0), abs(wall - x1)
                side = "xmin" if dx0 < dx1 else "xmax"
                if min(dx0, dx1) < 0.7:
                    self.blk[side].append((lo - 1.45, hi + 1.45))
                self.used.append((wall - 0.80, wall + 0.80, lo - 0.50, hi + 0.50))
                self.used.append((wall - 0.30, wall + 0.30, lo - 1.45, hi + 1.45))
                ends.append((wall, (lo + hi) / 2))
        for (px, pz) in points:
            ends.append((px, pz))
            # a kamachi step / passage on a side: no wall props in front of it either
            for side, d_, along in (("zmin", abs(pz - z0), px), ("zmax", abs(pz - z1), px), ("xmin", abs(px - x0), pz),
                                    ("xmax", abs(px - x1), pz)):
                if d_ < 0.8:
                    self.blk[side].append((along - 0.80, along + 0.80))
        for s in open_sides:
            self.blk[s].append((-99.0, 99.0))
        self.ends = ends
        self.oplist = [("e%d" % i, e) for i, e in enumerate(ends)]
        self.centre = centre
        self.miss = []

    # ---------------------------------------------------------------- tests
    def _band_ok(self, it):
        """decor.band_check (D4) with the room's props so far + `it`, on a 0.10 m grid."""
        c = self.c
        if not DC.blocks(it):
            return True
        if it.get("y") is None:
            it = dict(it, y=c.y(self.n))
        items = [x for x in c.D.items if x["room"] == self.n] + [it]
        room = dict(c.room[self.n], rect_model=list(self.r))
        ok, _ = DC.band_check(room, items, self.oplist, c.fixed.get(self.n, ()), step=0.10, centre=self.centre)
        return ok

    def _ok(self, fp, it=None, band=True):
        x0, x1, z0, z1 = self.r
        if fp[0] < x0 - 0.02 or fp[1] > x1 + 0.02 or fp[2] < z0 - 0.02 or fp[3] > z1 + 0.02:
            return False
        if any(_overlap(fp, u, 0.04) for u in self.used):
            return False
        if band and self.centre and it is not None and DC.blocks(it):
            # the centre cell needs a free 1.00 m band cell within 0.5 m
            dx = max(fp[0] - self.cx, 0.0, self.cx - fp[1])
            dz = max(fp[2] - self.cz, 0.0, self.cz - fp[3])
            if math.hypot(dx, dz) < 0.55:
                return False
        return not (band and it is not None and not self._band_ok(it))

    @staticmethod
    def _fp(it):
        try:
            p = DC.footprint(it)
        except Exception:
            p = None
        if not p:
            b = it["info"]["bbox"]
            ca, sa = math.cos(math.radians(it["yaw"])), math.sin(math.radians(it["yaw"]))
            pts = [(it["x"] + x * ca + z * sa, it["z"] - x * sa + z * ca) for x in (b[0], b[1]) for z in (b[4], b[5])]
            return (min(p_[0] for p_ in pts), max(p_[0] for p_ in pts), min(p_[1] for p_ in pts),
                    max(p_[1] for p_ in pts))
        return DC.aabb(p)

    # ---------------------------------------------------------------- placements
    def wall(self, name, sides=SIDES, why="", y=None, frm="lo", gap=0.03, count=True, step=0.05, band=True):
        """A floor prop with its back to a wall (or a wall-anchored prop), the first free spot along `sides`."""
        c = self.c
        if count and self.n_count() >= 7:
            self.miss.append(name)
            return None
        inf = DC.catalog()[name]
        x0, x1, z0, z1 = self.r
        if inf["anchor"] == "wall":
            back, g = WALL_INSET, 0.0
        else:
            back, g = -inf["bbox"][4], gap
        hw = (inf["bbox"][1] - inf["bbox"][0]) / 2 + 0.02
        for side in sides:
            lo, hi = (x0, x1) if side in ("zmin", "zmax") else (z0, z1)
            n = int((hi - lo - 2 * hw) / step)
            ats = [lo + hw + k * step for k in range(n + 1)]
            if frm == "hi":
                ats = ats[::-1]
            elif frm == "mid":
                m = (lo + hi) / 2
                ats.sort(key=lambda a: abs(a - m))
            for at in ats:
                if any(a < at + hw and at - hw < b for (a, b) in self.blk[side]):
                    continue
                x, z, yaw = c._wall_pose(self.n, side, at, back + g, 0.0)
                it = DC.item(name, self.n, x, z, yaw, y=y, why=why, count=count)
                if y is not None and inf["anchor"] == "wall":
                    it["on_floor"] = False
                fp = self._fp(it)
                if not self._ok(fp, it, band=band):
                    continue
                self.used.append(fp)
                return c.D.place(it)
        self.miss.append(name)
        return None

    def free(self, name, fx=0.5, fz=0.5, yaw=0.0, why="", count=True, y=None, band=True, rad=1.6):
        """A free-standing prop near the relative spot (fx, fz) of the room rect, the nearest free position."""
        c = self.c
        if count and self.n_count() >= 7:
            self.miss.append(name)
            return None
        x0, x1, z0, z1 = self.r
        tx, tz = x0 + (x1 - x0) * fx, z0 + (z1 - z0) * fz
        cands = []
        k = 0.0
        while k <= rad + 1e-6:
            for a in range(0, 360, 30 if k > 0 else 360):
                cands.append((tx + k * math.cos(math.radians(a)), tz + k * math.sin(math.radians(a))))
            k += 0.1
        for (x, z) in cands:
            it = DC.item(name, self.n, x, z, yaw, y=y, why=why, count=count)
            fp = self._fp(it)
            if not self._ok(fp, it, band=band):
                continue
            self.used.append(fp)
            return c.D.place(it)
        self.miss.append(name)
        return None

    def onwall(self, name, sides=SIDES, why="", frm="mid"):
        """A wall / post life item on a free stretch of wall (never over a door zone)."""
        c = self.c
        inf = DC.catalog()[name]
        x0, x1, z0, z1 = self.r
        hw = (inf["bbox"][1] - inf["bbox"][0]) / 2 + 0.05
        for side in sides:
            lo, hi = (x0, x1) if side in ("zmin", "zmax") else (z0, z1)
            ats = [lo + hw + k * 0.05 for k in range(int((hi - lo - 2 * hw) / 0.05) + 1)]
            if frm == "mid":
                m = (lo + hi) / 2
                ats.sort(key=lambda a: abs(a - m))
            for at in ats:
                if any(a < at + hw and at - hw < b for (a, b) in self.blk[side]):
                    continue
                return c.onwall(self.n, side, at, name, why=why)
        self.miss.append(name)
        return None

    def surf(self, host, name, why="", surface=None, dx=0.0, dz=0.0):
        if host is None:
            return None
        return self.c.surf(host, name, surface=surface, dx=dx, dz=dz, why=why)

    # ---------------------------------------------------------------- top-up (decor D1 5-7, D3 raised surface)
    def n_count(self):
        return sum(1 for x in self.c.D.items if x["room"] == self.n and x["count"])

    @staticmethod
    def _shelf(info):
        return any(sf.get("kind", "shelf") == "shelf" and sf.get("y", 0.0) > 0.08 and sf.get("y", 0.0) <= 1.40
                   for sf in info.get("loot", ()))

    def n_raised(self):
        return sum(1 for x in self.c.D.items if x["room"] == self.n and self._shelf(x["info"]))

    def top_up(self, pool):
        if self.c.room[self.n].get("sparse"):
            return
        spots = [(0.2, 0.2), (0.8, 0.8), (0.2, 0.8), (0.8, 0.2), (0.5, 0.2), (0.5, 0.8), (0.2, 0.5), (0.8, 0.5)]
        for name in pool:
            if self.n_count() >= 5 and self.n_raised() >= 1:
                return
            if self.n_count() >= 7:
                break
            if self.n_raised() == 0 and not self._shelf(DC.catalog()[name]):
                continue
            if self.wall(name, why="top-up: " + name.replace("jp_f_", "")) is not None:
                continue
            for (fx, fz) in spots:
                if self.free(name, fx, fz, 0, why="top-up: " + name.replace("jp_f_", ""), rad=0.6) is not None:
                    break


def _kamado_on_spot(c, room, n=2):
    import furnish_sets as FS
    return FS._kamado_on_spot(c, room, n)


def _irori(c, room, jizai="jp_f_jizai_kagi"):
    f = c.fit(room, "irori")[0]
    hx, hy, hz = f["hook"]
    c.hang(room, jizai, hx, hz, hy, over="hearth", why="the pot hook over the irori")
    return f


def _kamados(c, room, pots=("jp_f_kama", "jp_f_kama_nolid", "jp_f_seiro_kama2")):
    """Every kamado spot of the room gets its stove (+ a pot in each mouth)."""
    fs = c.fit(room, "kamado")
    import furnish_sets as FS
    for i, f in enumerate(fs):
        (cx, cz), yaw, (w, d) = f["centre"], f["yaw"], f["size"]
        rect = (cx - w / 2, cx + w / 2, cz - d / 2, cz + d / 2) if round(yaw) % 180 == 0 else \
            (cx - d / 2, cx + d / 2, cz - w / 2, cz + w / 2)
        mouth = {0: "+z", 90: "+x", 180: "-z", 270: "-x"}[int(round(yaw)) % 360]
        c.kamado(room, rect, mouth, n=2 if w > 1.0 else 1)
    return fs


# ================================================================================================ the dressings
def _doma_kitchen(c, room, open_side, steps, tier, firewood=True, extra=()):
    """A kitchen doma: its kamado (fitting), water jar, sink + shelf, firewood, a tub; wall life items."""
    fs = c.fit(room, "kamado")
    for i, f in enumerate(fs):
        (cx, cz), yaw, (w, d) = f["centre"], f["yaw"], f["size"]
        rect = (cx - w / 2, cx + w / 2, cz - d / 2, cz + d / 2) if round(yaw) % 180 == 0 else \
            (cx - d / 2, cx + d / 2, cz - w / 2, cz + w / 2)
        mouth = {0: "+z", 90: "+x", 180: "-z", 270: "-x"}[int(round(yaw)) % 360]
        n = 2 if w > 1.0 else 1
        c.kamado(room, rect, mouth, n=n)
        c.pot(room, ("jp_f_kama", "jp_f_kama_nolid", "jp_f_seiro_kama2")[i % 3], 0, why="a pot left in the stove")
    os_ = (open_side,) if isinstance(open_side, str) else tuple(open_side or ())
    R = Room(c, room, open_sides=os_, points=steps)
    R.wall("jp_f_mizugame", why="the water jar")
    sh = R.wall("jp_f_nagashi_wood", why="the wooden sink")
    if firewood:
        R.wall("jp_f_firewood_stack", why="split wood stacked against the wall")
    R.wall("jp_f_oke_pickle", why="a pickle tub")
    for nm in extra:
        R.wall(nm, why="kitchen gear")
    R.onwall("jp_f_utensil_board", why="ladles and knives on the wall")
    R.free("jp_f_debris_leaves", 0.5, 0.85, 20, why="leaves blown in under the door", count=False, band=False)
    return R, sh


def mountain(c):
    """Kiso / Hida mountain house (T2): the doma with the stove and snow gear, the oe round the irori under the hidana,
    the dei, the nando. Millet and chestnuts, straw boots: autumn before the snow."""
    steps = [(-1.82, -1.82), (-1.82, 1.82)]
    for (x, z) in steps:
        c.passage(("doma", "oe"), x, z, "kamachi step doma <-> oe")
    R, sh = _doma_kitchen(c, "doma", "xmax", steps, 2, extra=("jp_f_tawara_kamasu_stack3",))
    R.wall("jp_f_basket_back", why="the carrying frame (shoiko) by the door")
    R.onwall("jp_f_mino_pegs_rain", why="straw raincoat and hat")
    O = Room(c, "oe", open_sides=("xmin",), points=steps)
    f = _irori(c, "oe")
    O.free("jp_f_enza", 0.70, 0.62, 0, why="straw cushion by the hearth")
    O.free("jp_f_enza", 0.25, 0.40, 30, why="a cushion kicked aside (disorder)")
    O.free("jp_f_kama_nabe_rusted", 0.62, 0.40, 0, why="a pot left by the hearth, rusting")
    tn = O.wall("jp_f_tana_136_1", sides=("zmax", "zmin"), why="a plank shelf")
    O.surf(tn, "jp_f_tableware_bowls", why="bowls on the shelf")
    O.wall("jp_f_meal_left_hakozen", sides=("zmin", "zmax"), why="a box-tray meal left half eaten")
    O.free("jp_f_mushiro", 0.30, 0.75, 0, why="a straw mat over the boards")
    O.onwall("jp_f_kamidana_plain", sides=("zmax",), why="god shelf, undisturbed")
    O.onwall("jp_f_butsudan_shelf", sides=("zmin",), why="the Buddhist shelf, undisturbed")
    D = Room(c, "dei")
    D.wall("jp_f_tansu_single", why="a low chest")
    D.wall("jp_f_itoguruma", why="the spinning wheel")
    D.wall("jp_f_box_l", why="a lidded box")
    D.free("jp_f_andon_kaku", 0.80, 0.80, 0, why="standing lamp, unlit")
    D.free("jp_f_mushiro_rolled", 0.25, 0.25, 90, why="a rolled straw mat")
    D.onwall("jp_f_koyomi_curled", why="an old calendar curling")
    N = Room(c, "nando")
    N.wall("jp_f_futon_stack", why="bedding folded in the corner")
    N.wall("jp_f_kori_2", why="two wicker trunks")
    N.wall("jp_f_iko_plain", why="a clothes rack")
    N.free("jp_f_andon_ariake", 0.75, 0.75, 0, why="night lamp, unlit")
    N.free("jp_f_clothes_haori", 0.35, 0.45, 25, why="a jacket dropped on the floor")
    N.onwall("jp_f_bangasa_hung", why="an oiled umbrella")
    c.site("jp_s_firewood_stack_wall_1ken_h180", 2.60, -3.83, 180, why="winter firewood stacked high on the back wall")
    c.site("jp_s_hasa_low", 3.0, 5.6, 0, why="a low drying rack in the yard (autumn)")


def coastal(c):
    """Fisherman's house (T1): the big doma with the nets and tubs, the living room with the irori, the back room;
    the net store lean-to with the gear; outside the upturned boat and the net poles."""
    steps = [(-0.91, 0.455)]
    for (x, z) in steps:
        c.passage(("doma", "living"), x, z, "kamachi step doma <-> living")
    R, sh = _doma_kitchen(c, "doma", "xmax", steps, 1, firewood=False)
    R.wall("jp_f_fish_tub_empty", why="a fish tub, empty")
    R.onwall("jp_f_rope_pegs_3", why="rope coils for the nets")
    L = Room(c, "living", open_sides=("xmin",), points=steps)
    _irori(c, "living", jizai="jp_f_jizai_kagi_plain_abandoned")
    L.free("jp_f_enza", 0.20, 0.30, 0, why="straw cushion")
    L.free("jp_f_kama_nabe", 0.45, 0.75, 0, why="a pot by the hearth")
    L.wall("jp_f_tana_091_1", sides=("xmax", "zmax"), why="a plank shelf")
    L.wall("jp_f_jar_m", why="a jar of salted fish")
    L.free("jp_f_mushiro_torn", 0.30, 0.70, 0, why="a torn straw mat")
    L.onwall("jp_f_kamidana_plain", why="god shelf with Ebisu, undisturbed")
    B = Room(c, "back_room")
    B.wall("jp_f_straw_bed_quilt", why="the straw bed (T1: no futon)")
    B.wall("jp_f_kori", why="a wicker trunk")
    B.wall("jp_f_box_l", why="a box of net floats and sinkers")
    B.free("jp_f_andon_ariake", 0.80, 0.75, 0, why="night lamp, unlit")
    B.free("jp_f_mushiro_rolled", 0.70, 0.30, 90, why="a rolled mat")
    B.onwall("jp_f_mino_pegs", why="raincoat and hat")
    S = Room(c, "leanto", centre=False)
    sparse(c, "leanto", "the open net store (lean-to)")
    S.wall("jp_f_oke_tarai", sides=("xmin", "zmin", "zmax"), why="a tub of net tar (persimmon tannin)", band=False)
    S.wall("jp_f_basket_back", sides=("zmin", "xmin"), why="a carrying basket", band=False)
    S.wall("jp_f_jar_l", sides=("xmin", "zmax"), why="a jar", band=False)
    c.site("jp_s_fishnet_poles", -4.6, 5.0, 0, why="nets hung to dry on poles")
    c.site("jp_s_boat_upturned", 1.2, 5.6, 80, why="the boat hauled up and turned over")
    c.site("jp_s_fishnet_heap", -5.8, -3.6, 20, why="an old net heaped by the store")


def _unit(c, u, state):
    """One foot-soldier unit (T2): the doma, the front room (desk, side-job gear), the back room (bedding)."""
    x0d = c.R("u%d_doma" % u)
    steps = [(x0d[1] + 0.05, 0.91)]
    for (x, z) in steps:
        c.passage(("u%d_doma" % u, "u%d_front" % u if z > 0 else "u%d_back" % u), x, z, "kamachi step")
    sparse(c, "u%d_doma" % u, "the unit's small entry doma (the stove, a jar)")
    R, sh = _doma_kitchen(c, "u%d_doma" % u, ("xmax", "zmin"), steps, 2, firewood=(state != "empty"))
    F = Room(c, "u%d_front" % u, points=[steps[0]])
    if state == "empty":
        F.wall("jp_f_zukue_plain_tipped", why="a desk knocked over")
        F.free("jp_f_debris_paper", 0.5, 0.6, 30, why="papers scattered", band=False)
        F.wall("jp_f_bangasa_leaning", why="an umbrella frame leaning (the side job)")
        F.wall("jp_f_tansu_single_ransacked", why="a low chest, drawers pulled out")
        F.free("jp_f_andon_kaku_tipped", 0.7, 0.3, 40, why="a lamp knocked over")
        F.free("jp_f_enza", 0.3, 0.4, 10, why="a cushion kicked aside")
    else:
        d = F.wall("jp_f_zukue_plain", why="the writing desk")
        F.surf(d, "jp_f_writing_box", why="the writing box")
        F.wall("jp_f_katanakake_stand" if state == "sword" else "jp_f_bangasa_leaning",
               why="the sword stand" if state == "sword" else "umbrella frames (the side job)")
        F.wall("jp_f_box_l", why="a box of umbrella paper" if state != "sword" else "a lidded box")
        F.free("jp_f_hibachi_box", 0.6, 0.6, 0, why="box brazier")
        F.free("jp_f_andon_kaku", 0.85, 0.2, 0, why="standing lamp, unlit")
        F.free("jp_f_enza", 0.3, 0.45, 0, why="straw cushion")
    F.onwall("jp_f_kamidana_plain", why="god shelf")
    B = Room(c, "u%d_back" % u)
    B.wall("jp_f_futon_laid" if state != "empty" else "jp_f_futon_stack", sides=("zmin",),
           why="bedding" + (" left slumped" if state == "empty" else " laid out"))
    B.wall("jp_f_kori" if state != "empty" else "jp_f_kori_open", why="a wicker trunk")
    B.wall("jp_f_yoroibitsu_plain" if state == "sword" else "jp_f_tansu_single", why="the issue armour chest"
           if state == "sword" else "a low chest")
    B.wall("jp_f_iko_plain", why="a clothes rack")
    B.free("jp_f_andon_ariake", 0.85, 0.5, 0, why="night lamp, unlit")
    B.onwall("jp_f_bangasa_hung", why="an umbrella")


def kumi(c):
    """Foot-soldier row (T2): three units: one living with the sword stand and armour chest, one doing umbrella frames
    as the side job, one left in a hurry (desk over, papers, bedding slumped)."""
    for u, st in ((0, "sword"), (1, "umbrella"), (2, "empty")):
        _unit(c, u, st)
    c.site("jp_s_laundry_pole_crossed", -5.0, 4.4, 0, why="a laundry pole before the row")
    c.site("jp_s_potted_pair", 2.2, 3.6, 0, why="potted plants (the side job)")


# ------------------------------------------------------------------------------------------------ status houses
def _daidokoro(c, room, steps, tier, open_side="xmin"):
    D = Room(c, room, open_sides=(open_side,), points=steps)
    if c.fit(room, "irori"):
        _irori(c, room, jizai="jp_f_jizai_kagi")
        D.free("jp_f_enza", 0.55, 0.62, 0, why="straw cushion by the hearth")
    tn = D.wall("jp_f_tana_182_3", sides=("zmin", "zmax"), why="the dish shelf")
    D.surf(tn, "jp_f_tableware_hakozen_stack", surface="board_1", why="box trays stacked")
    D.wall("jp_f_rice_bin", sides=("zmax", "zmin", "xmax"), why="the rice bin")
    D.wall("jp_f_charcoal_scuttle", why="the charcoal scuttle")
    D.free("jp_f_tableware_scattered", 0.5, 0.25, 20, why="bowls scattered (disorder)", count=True)
    D.free("jp_f_kama_nabe", 0.5, 0.78, 0, why="a pot left on the boards")
    D.onwall("jp_f_ofuda_akiba", sides=("xmax", "zmax", "zmin"), why="the fire charm")
    return D


def _formal(c, room, tier, toko=False, jodan=False, crest=False):
    """A formal tatami room (zashiki / tsugi): screens, a cushion stack, a lamp, a brazier, a box; the tokonoma left
    undisturbed (its board takes a vase / scroll box, never loot)."""
    Z = Room(c, room)
    Z.wall("jp_f_byobu_makura", sides=("zmin", "xmin", "zmax"), why="a folding screen")
    Z.wall("jp_f_box_m_lacquer", why="a lacquered box of trays")
    t = Z.wall("jp_f_tansu_single", why="a low chest")
    Z.surf(t, "jp_f_tea_matcha" if tier >= 3 else "jp_f_masu_set", why="a tea bowl and caddy (T3)" if tier >= 3
           else "measures on the chest")
    Z.free("jp_f_hibachi_round", 0.45, 0.45, 0, why="a round brazier")
    Z.free("jp_f_andon_kaku", 0.15, 0.85, 0, why="standing lamp, unlit")
    Z.free("jp_f_enza_zabuton_stack3" if tier >= 3 else "jp_f_enza_stack3", 0.80, 0.20, 0, why="cushions stacked")
    if jodan:
        Z.free("jp_f_shokudai_tall", 0.75, 0.75, 0, why="a tall candle stand by the lord's seat")
    return Z


def samurai(c):
    """Samurai mansion (middle plot, T3): the genkan room with the crested screen and the sword stand, the chanoma, the
    tsugi, the zashiki (tokonoma undisturbed), the kitchen; the armour chest and the bow rack of a mounted rank."""
    steps = [(c.R("doma")[1] + 0.05, 0.0)]
    c.passage(("doma", "daidokoro"), steps[0][0], steps[0][1], "kamachi step doma <-> daidokoro")
    _doma_kitchen(c, "doma", "xmax", steps, 3, extra=("jp_f_taru_rack3",))
    _daidokoro(c, "daidokoro", steps, 3)
    G = Room(c, "genkan_ma")
    G.free("jp_f_byobu_tsuitate", 0.80, 0.70, 90, why="the crested entrance screen facing the genkan door")
    G.wall("jp_f_katanakake_stand", why="the sword stand for guests' swords")
    G.wall("jp_f_yoroibitsu", why="the armour chest")
    G.wall("jp_f_box_l", why="a document box")
    G.free("jp_f_hibachi_box", 0.35, 0.40, 0, why="a box brazier")
    G.onwall("jp_f_yumi_rack_wall", why="the bow rack")
    ch = Room(c, "chanoma")
    t = ch.wall("jp_f_tansu", why="the chest of drawers")
    ch.surf(t, "jp_f_tea_dobin", why="a clay tea pot")
    ch.wall("jp_f_butsudan_lacquer", why="the family altar, undisturbed")
    ch.wall("jp_f_mirror_stand", why="the mirror stand")
    ch.free("jp_f_hibachi_round", 0.55, 0.55, 0, why="the round brazier")
    ch.free("jp_f_tabakobon_spilled", 0.35, 0.65, 30, why="the tobacco tray knocked over (disorder)")
    ch.free("jp_f_enza_zabuton", 0.65, 0.35, 0, why="a cushion")
    ch.onwall("jp_f_kamidana_plain", why="god shelf, undisturbed")
    _formal(c, "tsugi", 3)
    Z = _formal(c, "zashiki", 3, toko=True)
    sparse(c, "engawa", "the veranda along the garden")
    E = Room(c, "engawa", centre=False)
    E.free("jp_f_enza_zabuton_folded", 0.3, 0.5, 0, why="a cushion left on the veranda", count=True, band=False)
    sparse(c, "genkan_porch", "the genkan porch")
    c.site("jp_s_footwear_pairs", 8.6, 1.6, 90, y=0.05, why="sandals left on the stone pad")
    c.site("jp_s_potted_stand", 2.5, -7.4, 0, why="bonsai on a stand in the garden")


def doshin(c):
    """Small samurai house (doshin, T2-3): the plain entrance room, the chanoma, the zashiki (plain), the sleeping room,
    the kitchen; the truncheon and crested coat of a town-police officer are the dressing (sword rack, writing box)."""
    steps = [(c.R("doma")[1] + 0.05, 0.0)]
    c.passage(("doma", "daidokoro"), steps[0][0], steps[0][1], "kamachi step doma <-> daidokoro")
    _doma_kitchen(c, "doma", "xmax", steps, 2)
    D = Room(c, "daidokoro", open_sides=("xmin",), points=steps)
    tn = D.wall("jp_f_tana_091_3", sides=("zmin", "zmax"), why="a two-board shelf")
    D.surf(tn, "jp_f_tableware_bowls", surface="board_1", why="bowls")
    D.wall("jp_f_rice_bin", sides=("zmax", "zmin"), why="the rice bin")
    D.wall("jp_f_charcoal_scuttle", sides=("zmax", "zmin"), why="charcoal")
    D.free("jp_f_enza", 0.5, 0.65, 0, why="a straw cushion")
    D.free("jp_f_kama_nabe_rusted", 0.5, 0.35, 0, why="a pot, rusting")
    G = Room(c, "genkan_ma")
    G.free("jp_f_byobu_tsuitate", 0.80, 0.70, 90, why="the entrance screen")
    G.wall("jp_f_katanakake_stand", why="the sword stand")
    G.wall("jp_f_box_l", why="a box")
    G.free("jp_f_hibachi_box", 0.4, 0.4, 0, why="a brazier")
    G.free("jp_f_andon_kaku", 0.2, 0.8, 0, why="standing lamp, unlit")
    G.onwall("jp_f_mino_pegs", why="a straw raincoat for the rounds")
    ch = Room(c, "chanoma")
    d = ch.wall("jp_f_zukue_plain", why="the writing desk")
    ch.surf(d, "jp_f_writing_box_open", why="the writing box, open (reports)")
    ch.wall("jp_f_butsudan_plain", why="the family altar, undisturbed")
    ch.free("jp_f_hibachi_round", 0.55, 0.5, 0, why="the brazier")
    ch.free("jp_f_enza", 0.35, 0.65, 0, why="a cushion")
    ch.free("jp_f_tabakobon", 0.7, 0.3, 0, why="the tobacco tray")
    ch.onwall("jp_f_koyomi", why="this year's calendar")
    N = Room(c, "nando")
    N.wall("jp_f_futon_laid", sides=("zmin", "xmin"), why="bedding laid out")
    N.wall("jp_f_tansu", why="the chest of drawers")
    N.wall("jp_f_iko_robe", why="the crested coat on its rack")
    N.free("jp_f_andon_ariake", 0.8, 0.8, 0, why="night lamp, unlit")
    N.free("jp_f_kori_open", 0.3, 0.6, 0, why="a wicker trunk, lid off (disorder)")
    Z = Room(c, "zashiki")
    Z.wall("jp_f_byobu_makura", why="a low screen")
    t = Z.wall("jp_f_tansu_single", why="a low chest")
    Z.surf(t, "jp_f_masu_set", why="measures")
    Z.free("jp_f_hibachi_box", 0.5, 0.5, 0, why="a brazier")
    Z.free("jp_f_andon_kaku", 0.2, 0.8, 0, why="a lamp")
    Z.free("jp_f_goban_go_scattered", 0.7, 0.3, 20, why="a go board, stones scattered")


def merchant(c):
    """Great merchant residence (T3): the kitchen with the three-mouth stove bank, the chanoma with the long brazier,
    the butsuma (the family altar), the tsugi, the oku-zashiki on the garden (plain: no tokonoma); money chests and
    ledgers, tea things, the go board."""
    steps = [(c.R("doma")[1] + 0.05, 0.0)]
    c.passage(("doma", "daidokoro"), steps[0][0], steps[0][1], "kamachi step doma <-> daidokoro")
    _doma_kitchen(c, "doma", "xmax", steps, 3, extra=("jp_f_taru_rack3",))
    _daidokoro(c, "daidokoro", steps, 3)
    ch = Room(c, "chanoma")
    t = ch.wall("jp_f_tansu", why="the chest of drawers")
    ch.surf(t, "jp_f_tea_dobin", why="a clay tea pot")
    ch.wall("jp_f_senryobako", why="the money chest")
    d = ch.wall("jp_f_zukue_choba", why="the master's account desk")
    ch.surf(d, "jp_f_choba_set_desk", why="ledgers and the abacus")
    ch.free("jp_f_hibachi_box", 0.5, 0.5, 0, why="the long brazier")
    ch.free("jp_f_enza_zabuton", 0.35, 0.6, 0, why="a cushion")
    ch.onwall("jp_f_kamidana_plain", why="god shelf, undisturbed")
    B = Room(c, "butsuma")
    B.wall("jp_f_butsudan_lacquer", why="the lacquered family altar, undisturbed")
    t = B.wall("jp_f_tansu_single", why="a low chest")
    B.surf(t, "jp_f_masu_set", why="measures")
    B.free("jp_f_shokudai_tall", 0.4, 0.4, 0, why="a candle stand")
    B.free("jp_f_enza_zabuton_stack3", 0.7, 0.7, 0, why="cushions stacked")
    B.free("jp_f_box_m_lacquer", 0.75, 0.35, 0, why="a box of lacquered trays")
    _formal(c, "tsugi", 3)
    _formal(c, "oku_zashiki", 3)
    sparse(c, "engawa", "the veranda along the garden")
    c.site("jp_s_potted_stand", 4.0, -7.4, 0, why="bonsai on a stand in the garden")


def honjin_omote(c):
    """Honjin formal block (T3): the genkan room (screen, sword stand, the stay placards), the attendants' rooms
    (bedding stacks, travel chests), the san-no-ma / tsugi-no-ma, the JODAN-NO-MA with the lord's place (cushions, the
    sword stand, the tall candle stands), the tokonoma undisturbed."""
    G = Room(c, "genkan_ma")
    G.free("jp_f_byobu_tsuitate", 0.85, 0.70, 90, why="the crested screen facing the genkan")
    G.wall("jp_f_katanakake_stand", why="the sword stand")
    G.wall("jp_f_box_l", why="the box of stay placards (sekifuda) and ledgers of stays")
    G.wall("jp_f_tansu_single", why="a low chest")
    G.free("jp_f_hibachi_box", 0.4, 0.4, 0, why="a brazier")
    G.free("jp_f_andon_kaku", 0.2, 0.85, 0, why="a lamp")
    for room, st in (("attendants_1", 0), ("attendants_2", 1)):
        A = Room(c, room)
        A.wall("jp_f_futon_stack" if st == 0 else "jp_f_futon_stack_slumped", why="the attendants' bedding stack")
        A.wall("jp_f_kori_2", why="travel trunks")
        A.wall("jp_f_nagamochi" if st == 0 else "jp_f_nagamochi_open", why="a long chest" + ("" if st == 0 else
                                                                                            ", lid thrown back"))
        A.free("jp_f_andon_kaku", 0.5, 0.75, 0, why="a lamp, unlit")
        A.free("jp_f_meal_left_two", 0.45, 0.35, 0, why="two trays left")
        A.free("jp_f_hibachi_box", 0.75, 0.45, 0, why="a brazier")
    _formal(c, "san_no_ma", 3)
    _formal(c, "tsugi_no_ma", 3)
    J = Room(c, "jodan_no_ma")
    J.wall("jp_f_katanakake_stand", why="the lord's sword stand")
    J.wall("jp_f_byobu_makura", why="a folding screen")
    J.wall("jp_f_box_l", why="a box of lacquered trays and bowls")
    J.free("jp_f_enza_zabuton", 0.55, 0.5, 90, why="the lord's cushion")
    J.free("jp_f_shokudai_tall", 0.35, 0.25, 0, why="a tall candle stand")
    J.free("jp_f_shokudai_tall", 0.35, 0.75, 0, why="a tall candle stand")
    J.free("jp_f_hibachi_round", 0.6, 0.8, 0, why="a round brazier")
    sparse(c, "engawa", "the veranda along the garden")
    sparse(c, "genkan_porch", "the genkan porch")
    c.site("jp_s_footwear_pairs", 9.5, 1.6, 90, y=0.05, why="sandals left on the stone pad")


def honjin_oku(c):
    """Honjin family / kitchen block (T3): the big kitchen (the stove bank cooks for the lord's train), the daidokoro
    with the irori, the family rooms."""
    steps = [(c.R("doma")[1] + 0.05, -1.5), (c.R("doma")[1] + 0.05, 1.5)]
    for (x, z) in steps:
        c.passage(("doma", "daidokoro"), x, z, "kamachi step doma <-> daidokoro")
    R, sh = _doma_kitchen(c, "doma", "xmax", steps, 3, extra=("jp_f_taru_rack3", "jp_f_tawara_stack6"))
    _daidokoro(c, "daidokoro", steps, 3)
    F = Room(c, "family_room")
    t = F.wall("jp_f_tansu", why="the chest of drawers")
    F.surf(t, "jp_f_tea_dobin", why="a clay tea pot")
    F.wall("jp_f_butsudan_lacquer", why="the family altar, undisturbed")
    d = F.wall("jp_f_zukue_choba", why="the account desk (the honjin's stay ledgers)")
    F.surf(d, "jp_f_choba_set_desk", why="ledgers")
    F.free("jp_f_hibachi_round", 0.5, 0.5, 0, why="a brazier")
    F.free("jp_f_enza_zabuton", 0.4, 0.65, 0, why="a cushion")
    F.onwall("jp_f_kamidana_plain", why="god shelf")
    O = Room(c, "family_oku")
    O.wall("jp_f_futon_laid", why="bedding laid out")
    O.wall("jp_f_tansu_single", why="a low chest")
    O.wall("jp_f_mirror_stand_open", why="the mirror stand, open")
    O.free("jp_f_box_m_lacquer", 0.5, 0.4, 0, why="a lacquered box")
    O.free("jp_f_andon_ariake", 0.75, 0.75, 0, why="night lamp, unlit")
    O.free("jp_f_toys_doll", 0.35, 0.65, 0, why="a child's doll on the mats", count=True)


def wakihonjin(c):
    """Waki-honjin (T3): as the honjin, smaller, with its own kitchen; the family takes ordinary travellers of standing
    between lords (the attendants' room doubles as a guest room)."""
    steps = [(c.R("doma")[1] + 0.05, 0.0)]
    c.passage(("doma", "daidokoro"), steps[0][0], steps[0][1], "kamachi step doma <-> daidokoro")
    _doma_kitchen(c, "doma", "xmax", steps, 3)
    _daidokoro(c, "daidokoro", steps, 3)
    ch = Room(c, "chanoma")
    t = ch.wall("jp_f_tansu", why="the chest of drawers")
    ch.surf(t, "jp_f_tea_dobin", why="a clay tea pot")
    d = ch.wall("jp_f_zukue_choba", why="the account desk")
    ch.surf(d, "jp_f_choba_set_desk", why="the guest register")
    ch.free("jp_f_hibachi_box", 0.5, 0.5, 0, why="a brazier")
    ch.free("jp_f_enza_zabuton", 0.4, 0.6, 0, why="a cushion")
    ch.free("jp_f_andon_kaku", 0.8, 0.8, 0, why="a lamp")
    O = Room(c, "family_oku")
    O.wall("jp_f_futon_stack", why="bedding folded")
    O.wall("jp_f_butsudan_plain", why="the family altar, undisturbed")
    O.wall("jp_f_tansu_single", why="a low chest")
    O.free("jp_f_andon_ariake", 0.7, 0.7, 0, why="night lamp")
    O.free("jp_f_kori_open", 0.35, 0.4, 0, why="a trunk open")
    A = Room(c, "attendants")
    A.wall("jp_f_futon_laid_dragged", why="a guest's bedding dragged half off (disorder)")
    A.wall("jp_f_kori", why="a traveller's trunk")
    A.free("jp_f_meal_left_zen", 0.5, 0.4, 0, why="a tray meal left")
    A.free("jp_f_andon_kaku", 0.75, 0.75, 0, why="a lamp")
    A.free("jp_f_hibachi_box", 0.3, 0.7, 0, why="a brazier")
    G = Room(c, "genkan_ma")
    G.free("jp_f_byobu_tsuitate", 0.85, 0.65, 90, why="the entrance screen")
    G.wall("jp_f_katanakake_stand", why="the sword stand")
    G.wall("jp_f_box_l", why="the box of stay placards")
    G.free("jp_f_hibachi_box", 0.4, 0.4, 0, why="a brazier")
    G.free("jp_f_andon_kaku", 0.2, 0.85, 0, why="a lamp")
    _formal(c, "tsugi_no_ma", 3)
    J = Room(c, "jodan_no_ma")
    J.wall("jp_f_katanakake_stand", why="the sword stand")
    J.wall("jp_f_byobu_makura", why="a screen")
    J.free("jp_f_enza_zabuton", 0.5, 0.5, 90, why="the seat of honour")
    J.free("jp_f_shokudai_tall", 0.3, 0.3, 0, why="a candle stand")
    J.free("jp_f_hibachi_round", 0.6, 0.8, 0, why="a brazier")
    sparse(c, "engawa", "the veranda")
    sparse(c, "genkan_porch", "the genkan porch")


def headman_east(c):
    """Kanto headman (T2): the big doma with the stove bank, rice bales and the village's tools; the hiroma round the
    irori; the dei and nando; the formal end: the genkan doma (shikidai), the genkan room with the village registers,
    the zashiki for officials (screens, cushions; commoner: no tokonoma)."""
    xd = c.R("doma")[0] - 0.05
    steps = [(xd, -1.82), (xd, 1.82)]
    for (x, z) in steps:
        c.passage(("doma", "hiroma"), x, z, "kamachi step doma <-> hiroma")
    R, sh = _doma_kitchen(c, "doma", "xmin", steps, 2, extra=("jp_f_tawara_stack6", "jp_f_usu"))
    R.onwall("jp_f_tool_wall", why="the farm tools on pegs")
    H = Room(c, "hiroma", open_sides=("xmax",), points=steps)
    _irori(c, "hiroma")
    H.free("jp_f_enza", 0.55, 0.62, 0, why="a straw cushion by the hearth")
    tn = H.wall("jp_f_tana_136_1", sides=("zmax", "zmin"), why="a shelf")
    H.surf(tn, "jp_f_tableware_hakozen_stack", why="trays stacked")
    H.free("jp_f_kama_nabe", 0.5, 0.35, 0, why="a pot by the hearth")
    H.free("jp_f_mushiro", 0.25, 0.75, 0, why="a straw mat")
    H.wall("jp_f_charcoal_scuttle", why="charcoal")
    H.onwall("jp_f_kamidana_plain", why="god shelf, undisturbed")
    gd = c.R("genkan")
    c.passage(("genkan", "genkan_ma"), gd[1] + 0.05, (gd[2] + gd[3]) / 2 - 0.4, "the shikidai step")
    sparse(c, "genkan", "the genkan doma (shikidai entrance)")
    G = Room(c, "genkan_ma", open_sides=("xmin",), points=[(gd[1] + 0.05, (gd[2] + gd[3]) / 2 - 0.4)])
    d = G.wall("jp_f_zukue_choba", why="the headman's desk")
    G.surf(d, "jp_f_choba_set_desk", why="the village registers and the tax ledgers")
    G.wall("jp_f_nagamochi", why="the long chest of village documents")
    G.wall("jp_f_senryobako", why="the tax money chest")
    G.free("jp_f_hibachi_box", 0.5, 0.5, 0, why="a brazier")
    G.free("jp_f_andon_kaku", 0.8, 0.2, 0, why="a lamp")
    Z = _formal(c, "zashiki", 2)
    D = Room(c, "dei")
    t = D.wall("jp_f_tansu", why="the chest of drawers")
    D.surf(t, "jp_f_masu_set", why="rice measures")
    D.wall("jp_f_butsudan_lacquer", why="the big family altar, undisturbed")
    D.free("jp_f_hibachi_round", 0.5, 0.5, 0, why="a brazier")
    D.free("jp_f_enza_stack3", 0.25, 0.25, 0, why="cushions stacked")
    D.free("jp_f_andon_kaku", 0.8, 0.8, 0, why="a lamp")
    N = Room(c, "nando")
    N.wall("jp_f_futon_laid", why="bedding")
    N.wall("jp_f_kori_2", why="trunks")
    N.wall("jp_f_iko_plain", why="a clothes rack")
    N.free("jp_f_itoguruma", 0.5, 0.5, 0, why="the spinning wheel")
    N.free("jp_f_andon_ariake", 0.8, 0.8, 0, why="night lamp")


def headman_kinai(c):
    """Kinai headman (shoya, T2): the niwa with the stove row (kudo), the mise (village business), the daidokoro with the
    irori, the tsugi, the nando, the genkan room and the zashiki for officials (commoner: no tokonoma)."""
    xn = c.R("niwa")[1] + 0.05
    steps = [(xn, 1.82), (xn, -1.82)]
    for (x, z), r in zip(steps, ("mise", "daidokoro")):
        c.passage(("niwa", r), x, z, "kamachi step niwa <-> %s" % r)
    R, sh = _doma_kitchen(c, "niwa", "xmax", steps, 2, extra=("jp_f_tawara_stack6",))
    M = Room(c, "mise", open_sides=("xmin",), points=[steps[0]])
    d = M.wall("jp_f_zukue_choba", why="the village-business desk")
    M.surf(d, "jp_f_choba_set_desk", why="registers and ledgers")
    M.wall("jp_f_senryobako", why="the money chest")
    M.wall("jp_f_nagamochi", why="a long chest of documents")
    M.free("jp_f_hibachi_box", 0.5, 0.5, 0, why="a brazier")
    M.free("jp_f_enza", 0.35, 0.65, 0, why="a straw cushion")
    M.onwall("jp_f_kamidana_plain", why="god shelf, undisturbed")
    Dd = Room(c, "daidokoro", open_sides=("xmin",), points=[steps[1]])
    _irori(c, "daidokoro", jizai="jp_f_jizai_kagi_abandoned")
    tn = Dd.wall("jp_f_tana_136_1", sides=("zmin", "xmax"), why="a plank shelf")
    Dd.surf(tn, "jp_f_tableware_bowls", why="bowls")
    Dd.free("jp_f_kama_nabe", 0.75, 0.75, 0, why="a pot")
    Dd.free("jp_f_enza", 0.25, 0.3, 0, why="a straw cushion")
    Dd.free("jp_f_tableware_scattered", 0.8, 0.25, 20, why="bowls scattered")
    Dd.wall("jp_f_charcoal_scuttle", why="charcoal")
    T = Room(c, "tsugi")
    t = T.wall("jp_f_tansu", why="the chest of drawers")
    T.surf(t, "jp_f_masu_set", why="measures")
    T.wall("jp_f_butsudan_lacquer", why="the family altar, undisturbed")
    T.free("jp_f_hibachi_round", 0.5, 0.5, 0, why="a brazier")
    T.free("jp_f_enza_stack3", 0.25, 0.75, 0, why="cushions stacked")
    T.free("jp_f_andon_kaku", 0.8, 0.25, 0, why="a lamp")
    N = Room(c, "nando")
    N.wall("jp_f_futon_laid", why="bedding")
    N.wall("jp_f_nagamochi_open", why="a long chest, lid thrown back")
    N.wall("jp_f_iko_plain", why="a clothes rack")
    N.free("jp_f_andon_ariake", 0.7, 0.7, 0, why="night lamp")
    N.free("jp_f_kori", 0.3, 0.4, 0, why="a trunk")
    G = Room(c, "genkan_ma")
    G.free("jp_f_byobu_tsuitate", 0.85, 0.5, 90, why="the entrance screen")
    G.wall("jp_f_box_l", why="a document box")
    t = G.wall("jp_f_tansu_single", why="a low chest")
    G.free("jp_f_hibachi_box", 0.4, 0.4, 0, why="a brazier")
    G.free("jp_f_andon_kaku", 0.2, 0.8, 0, why="a lamp")
    _formal(c, "zashiki", 2)
    sparse(c, "genkan_porch", "the formal entrance under the lean-to")


def chashitsu(c):
    """Tea hut (T3): the tea room as left after the last gathering (the kettle on the ro, the water jar, a bowl), the
    mizuya with its shelf of tea things."""
    sparse(c, "chashitsu", "the tea room: bare by its rules, as left after the last gathering")
    T = Room(c, "chashitsu", centre=False)
    T.free("jp_f_kama_nabe", 0.80, 0.85, 0, why="the kettle left beside the ro")
    T.free("jp_f_enza_zabuton", 0.35, 0.55, 0, why="a guest's cushion")
    T.free("jp_f_tabakobon", 0.20, 0.80, 0, why="the tobacco tray for the guests")
    T.free("jp_f_tea_broken", 0.55, 0.30, 0, why="a tea bowl dropped and broken", count=False)
    M = Room(c, "mizuya")
    tn = M.wall("jp_f_tana_136_3", sides=("xmax", "zmin"), why="the mizuya shelves")
    M.surf(tn, "jp_f_tea_dobin", surface="board_1", why="a pot")
    M.wall("jp_f_nagashi_wood", why="the sink (mizuya-nagashi)")
    M.wall("jp_f_oke_bucket", why="a bucket")
    M.wall("jp_f_box_l", why="a box of tea utensils")
    M.free("jp_f_charcoal_scuttle", 0.4, 0.4, 0, why="charcoal for the ro")
    c.site("jp_s_stone_lantern_kasuga_18_moss", -2.6, 3.3, 0, why="a small stone lantern by the path")
    c.site("jp_s_chozubachi_natural", -1.2, 2.9, 0, y=0.08, why="the stone basin (tsukubai) before the crawl-in door")


def itagura(c):
    """Board storehouse (storage): grain bales, straw bags, seed, tools."""
    K = Room(c, "kura")
    K.wall("jp_f_tawara_stack6", why="rice bales")
    K.wall("jp_f_tawara_kamasu_stack3", why="straw bags of grain")
    K.wall("jp_f_rack_half", why="a rack of tools and seed")
    K.free("jp_f_mi", 0.5, 0.5, 0, why="a winnowing basket")
    K.free("jp_f_tawara_burst", 0.75, 0.35, 30, why="a bale burst open (rats)")


def stable_horse(c):
    """Stable (two horse stalls): mangers, straw, the tack."""
    F = Room(c, "floor")
    F.wall("jp_f_manger_trough_empty", sides=("zmin",), why="a manger, empty", band=False)
    F.free("jp_f_manger_straw_rotted", 0.3, 0.3, 0, why="the straw, rotting", band=False)
    F.wall("jp_f_manger_cutter", sides=("xmax", "zmax"), why="the fodder cutter")
    F.wall("jp_f_tawara_kamasu", sides=("xmax", "zmax"), why="a bag of fodder")
    F.wall("jp_f_oke_bucket", why="a water bucket")
    F.onwall("jp_f_rope_pegs_3", why="halters and ropes on the pegs")
    c.site("jp_s_stable_yard_saddle_rack", 3.6, 1.0, 270, why="the pack-saddle rack outside")


def furoba(c):
    """Bath hut: the tub spot (a big tub: oke stands in for the bath tub), buckets, the bran bag."""
    F = Room(c, "furoba")
    F.wall("jp_f_oke_tarai", why="a wash tub")
    F.wall("jp_f_oke_bucket", why="a bucket")
    F.wall("jp_f_jar_m", why="a jar of water")
    F.free("jp_f_mizugame", 0.75, 0.5, 0, why="the big water jar standing in for the tub")
    F.free("jp_f_oke_tipped", 0.3, 0.6, 30, why="a bucket tipped over")
    sparse(c, "sunoko", "the slatted washing floor")


def nagayamon(c):
    """Samurai nagaya-mon: the servants' room (bedding, a dice box: the reputed gambling dens), its doma, the storage
    bay (palanquin gear, rice bales)."""
    xl = c.R("doma")[0] - 0.05
    st = [(xl, 0.0)]
    c.passage(("doma", "room"), xl, 0.0, "kamachi step doma <-> room")
    R = Room(c, "room", open_sides=("xmax",), points=st)
    R.wall("jp_f_futon_stack_slumped", why="the servants' bedding, slumped")
    R.wall("jp_f_kori", why="a trunk")
    R.free("jp_f_goban_shogi_scattered", 0.5, 0.5, 20, why="a shogi board, pieces scattered (the gambling dens)")
    R.free("jp_f_andon_ariake_tipped", 0.75, 0.75, 40, why="a night lamp knocked over")
    R.free("jp_f_hibachi_box", 0.3, 0.3, 0, why="a brazier")
    R.wall("jp_f_tana_091_1", why="a shelf")
    D = Room(c, "doma", open_sides=("xmin",), points=st)
    D.wall("jp_f_oke_bucket", why="a bucket")
    D.wall("jp_f_firewood_bundle", why="brushwood")
    D.wall("jp_f_jar_m", why="a jar")
    D.free("jp_f_debris_straw", 0.5, 0.5, 30, why="straw tracked in", count=False, band=False)
    D.wall("jp_f_basket_kago", why="a basket")
    D.onwall("jp_f_mino_pegs", why="raincoats")
    D.wall("jp_f_box_l", why="a box")
    S = Room(c, "storage")
    S.wall("jp_f_tawara_stack6", why="rice bales (the stipend)")
    S.wall("jp_f_rack_1ken", why="shelving")
    S.wall("jp_f_nagamochi", why="a long chest")
    S.free("jp_f_box_stack3_toppled", 0.6, 0.5, 0, why="boxes toppled")
    S.free("jp_f_kori_2", 0.3, 0.3, 0, why="trunks")
    sparse(c, "gate", "the gate passage")


SETS_D3 = {
    "d3_mountain": {"tier": 2, "fn": mountain},
    "d3_coastal": {"tier": 1, "fn": coastal},
    "d3_kumi": {"tier": 2, "fn": kumi},
    "d3_doshin": {"tier": 2, "fn": doshin},
    "d3_samurai": {"tier": 3, "fn": samurai},
    "d3_merchant": {"tier": 3, "fn": merchant},
    "d3_honjin_omote": {"tier": 3, "fn": honjin_omote},
    "d3_honjin_oku": {"tier": 3, "fn": honjin_oku},
    "d3_wakihonjin": {"tier": 3, "fn": wakihonjin},
    "d3_headman_east": {"tier": 2, "fn": headman_east},
    "d3_headman_kinai": {"tier": 2, "fn": headman_kinai},
    "d3_chashitsu": {"tier": 3, "fn": chashitsu},
    "d3_itagura": {"tier": 1, "fn": itagura},
    "d3_stable": {"tier": 1, "fn": stable_horse},
    "d3_furoba": {"tier": 2, "fn": furoba},
    "d3_nagayamon": {"tier": 2, "fn": nagayamon},
}


TOP_POOL = ("jp_f_box_l", "jp_f_kori", "jp_f_tansu_single", "jp_f_box_stack3", "jp_f_jar_l", "jp_f_hibachi_box",
            "jp_f_andon_kaku", "jp_f_enza", "jp_f_oke_bucket", "jp_f_basket_kago", "jp_f_charcoal_bale")


def _wrap(fn):
    def run(c):
        fn(c)
        for R in getattr(c, "_d3_rooms", []):
            R.top_up(TOP_POOL)
        bad = []
        for R in getattr(c, "_d3_rooms", []):
            if c.room[R.n].get("sparse"):
                continue
            if R.n_count() < 5 or R.n_raised() < 1:
                bad.append("%s %d/%d" % (R.n, R.n_count(), R.n_raised()))
        if bad:
            print("[d3_sets] %s: rooms short of props: %s" % (c.key, bad))
        c._d3_rooms = []
    run.__doc__ = fn.__doc__
    return run


def sets():
    return {k: dict(v, fn=_wrap(v["fn"])) for k, v in SETS_D3.items()}
