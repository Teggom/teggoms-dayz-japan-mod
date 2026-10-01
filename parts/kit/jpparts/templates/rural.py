"""The rural shell template (C2, Phase C wave 1, 2026-09-30): farmhouses, poor huts and sheds from kit parts, framed
inside by koyagumi (B2 jp_p_frame_koyagumi) under thatch or boards. Bare shells: no furniture (C3 furnishes); every
shell leaves room for its fittings and lists them in info['fittings'] (irori pit + hook point, kamado spot).

    H, info = rural.build("kanto", stable=True)          # kit frame, see below
    M, floors, rooms, info = rural.model(kind="hut_east", size="s", floor="earth", door="mushiro")

Kinds and parameters
  kanto     DW06 Kanto farmhouse, hiroma type (3 rooms): W 7 x D 5 ken, ONE sweeping thatch roof over the joya core
            (3 ken) and the geya aisles (1 ken front and back, G1 A1 ruling 4: the 3-ken span rule is urban-only),
            koyagumi sasu on log ushibari with the joya posts inside, sooted. Doma 3 ken (43 %, PLAYBOOK T1 >= 40 %),
            hiroma (boards, irori pit 0.91 x 1.365 under the ushibari on its frame line), dei (tatami: T2 best room)
            and nando (boards). Front ooto (big plank door), back door (katabiki), two room doors.
              form      'yosemune' | 'irimoya'          ridge  thatch ridge kind: bamboo | shiba | umanori | tile
              stable    True: jp_p_frame_stall _umaya in the doma's back corner (the inside stable)
              doma      'left' (canonical) | 'right' (mirrored): the doma end in STREET VIEW, seen from the front
                        (DayZ is left-handed: the street-view left is the kit frame's high-x side)
  kinai     DW07 Kinai farmhouse, yotsuma-dori (4 rooms) with the ox: joya W 7 x D 4 ken under a steep thatch roof
            (keta 4.30), the Kinai LOWER ROOFS as pents along both long walls (tile or board, at 3.30; the pent over
            the entrance side is G1 decision 6's porch eave); niwa (doma) 3 ken with the ox stall (jp_p_frame_stall
            _ox, required); mise, daidokoro (irori), zashiki (tatami), nando.
              form      'kirizuma' | 'irimoya'          lower  'tile' | 'board'
              takahe    True (kirizuma only): yamato-mune, plastered tile-capped parapets flanking the thatch gables
              doma      'right' (canonical) | 'left' (mirrored), street view
  hut_east  DW01 poor hut, east type: thatch yosemune, earth walls (arakabe), keta 3.10 (thatch soffit >= 2.20)
              size      's' (3 x 2 ken) | 'l' (4 x 3 ken)
              floor     'earth' (all doma, stone-ringed irori_doma pit) | 'board' (doma 1 ken + boards 0.40 with
                        the irori pit) | 'sunoko' (doma 1 ken + split-bamboo take-yuka at 0.40 with the pit)
              door      'itado' (jp_p_open_itado _plain, one big leaf) | 'mushiro' (open bay, rolled straw mat)
  hut_west  DW30 poor hut, west / mountain type: kirizuma, board walls, 3 x 2 ken, optional side lean-to (1 ken,
            open woodshed-style, on a gable end)
              roof      'thatch' | 'ishioki' | 'itabuki'   leanto  None | 'left' | 'right'
              floor, door as hut_east
  shed      DW24 shed / barn, kirizuma on soseki, earth floor, not sooted
              size 's' (3 x 2) | 'l' (4 x 3)   roof 'itabuki' | 'thatch' | 'ishioki'
              open      True: the front long side open on posts (enclosed False: C11 skips it)
              leanto    None | 'left' | 'right': a woodshed lean-to on a gable end

Frame (the townhouse template's): kit frame x 0..W along the ridge, z 0 = front wall line (+z = out, the entrance
side), z -D = back wall line, y 0 = grade; every post node on the half-ken grid. model() puts the origin on the
footprint centre (W/2, -D/2) at grade, +z = front.

Levels (m): doma 0.05; farmhouse raised floor 0.50 (PLAYBOOK §4: +0.45 over the doma), hut floor 0.40; keta (eave
line) 3.30 Kanto, 4.30 Kinai (lower roofs at 3.50), 3.10 huts / sheds. Thatch overhang 0.90 at 45 deg (Kinai 0.60
over its lower roofs): the thatch soffit stays >= 2.20 all round (PLAYBOOK §4 'soffit >= 2.20 where people walk
underneath'), and no thatch slab's bounding box drops into a door column over a raised floor (the D2 head check).

Kit parts used: frame.post, found.soseki, walls.wall_run / gable / kawara_cap, openings (itado _plain / _battened /
_single, shoji _single / _hikiwake, window_slide _board, tsukiage, amado window, mushiro), floors.doma / boards /
tatami, pits.pit_fn / sunoko, roofs.roof, koyagumi.koyagumi + soot_roof, roofparts.pent, leanto.roof, stall.
"""
import math

from ..core import Part, box, prism, KEN, HALF, POST, KETA_H, LIBRARY
from .. import walls, frame, found, openings, roofs as R, roofparts, floors as FL, leanto, koyagumi as KY, pits as PI
from .. import stall as SL, trim
from ..assemble import Builder, to_world
from ..shapes import clip_poly, clean_poly

DOMA = 0.05
FARM_FLOOR = 0.50
HUT_FLOOR = 0.40
A_ = POST / 2
JOYA_POST = 0.18
KAMACHI_M = "wood_interior" if "wood_interior" in LIBRARY else "wood_sooted"
BOARDS_ROUGH = {"board": "floor_boards_rough", "base": "wood_sooted", "lod": "floor_boards_rough", "slab": True}
KINDS = ("kanto", "kinai", "hut_east", "hut_west", "shed")
# thatch-roof outline pieces the kit draws in Resolution 1-2 only (the thatch eave bands, hip rolls, ridge dressing,
# smoke-gable rims, bargeboards): a rural shell keeps them in every LOD (PLAYBOOK §15 T7b, C15)
SILHOUETTE_TAGS = ("thatch_band", "hip_roll", "ridge_bamboo", "umanori", "umanori_pole", "turf", "iris",
                   "ridge_tile_skirt", "kemuri_sill", "small_hafu", "hafu", "verge_batten", "ridge_batten", "lashing")


def _r(x0, x1, z0, z1):
    return FL.floor_rect(x0, x1, z0, z1)


def big_leaf(variant="_plain"):
    """jp_p_open_itado _plain / _battened / _oodo: ONE 1.74 m plank leaf in a 1-ken bay that parks outside over the
    next 1-ken bay (PLAYBOOK §15 T3 'single big leaf: poor houses, barns'). The part keeps B's older one-leaf format
    (core.sliding_leaf); this adapter gives it the DoorsTwinN convention every building uses (twin selection over the
    leaf, <twin>_action memory point), so assemble.Builder.place_door can place it."""
    p = openings.part_itado(variant)
    d = p.doors[0]
    bone = d.anims[0]["bone"]
    twin = "doorstwin1"
    for s in p.solids:
        if s.door == bone:
            s.sel = twin
    p.memory[twin + "_action"] = p.memory.pop(bone + "_action")
    d.twin = twin
    d.park_end = d.sweep[1]
    d.passable = True
    d.act_h = d.action[1]
    d.engine_tested = False
    # C17 (T11): the far jamb's lip is a 3-face strip; a grazing ray from the park side threads through its open ends
    # and behind the closed leaf. A closed filler over the far post, from the wall face to the leaf's back face.
    zf = POST / 2
    p.add(box(KEN - POST / 2, KEN + POST / 2, 0.0, 2.035, zf, zf + 0.0125, "wood_weathered", vis=(1, 2),
              tag="jamb_filler"))
    # the leaf's boards lie on its outer 2.8 cm and its battens only in bands: two end stiles close the void behind
    # the boards (a grazing ray ran behind them past the batten ends), moving with the leaf
    lz = [s.bbox() for s in p.solids if s.tag == "leaf" and s.door == bone][0]
    bz = min(s.bbox()[4] for s in p.solids if s.tag == "leaf_board" and s.door == bone)
    for (a, b) in ((lz[0], lz[0] + 0.05), (lz[1] - 0.05, lz[1])):
        st = p.add(box(a, b, lz[2], lz[3], lz[4], bz + 0.001, "wood_weathered", vis=(1,), tag="leaf_stile"))
        st.door = bone
        st.sel = twin
    return p


# ------------------------------------------------------------------------------------------------ the shell builder
class Shell:
    """One rural shell in its kit frame: posts on soseki, wall lines with openings, floors, roof + koyagumi, and the
    bookkeeping the pipeline needs (rooms, floor obstacles, portals, fittings)."""

    def __init__(self, name, W, D, tiers, used, wear="_w1"):
        self.W, self.D = W, D
        self.H = Part(name, "", "buildings", tiers=tiers, used_for=used)
        self.H.wear = wear
        self.posts, self.log = [], []
        self.B = Builder(self.H, posts=self.posts, log=self.log)
        self.rooms, self.obst, self.portals, self.fittings, self.passages = [], [], [], [], []
        self.windows = []
        self.dn = {}
        self.F = {"front": (0.0, (0.0, 0.0, 0.0)), "back": (180.0, (W, 0.0, -D)), "left": (90.0, (0.0, 0.0, -D)),
                  "right": (-90.0, (W, 0.0, 0.0))}
        self.L = {"front": W, "back": W, "left": D, "right": D}
        self.seed = 0

    # ---------------------------------------------------------------- posts
    def has_post(self, x, z):
        return any(abs(x - a) < 1e-4 and abs(z - b) < 1e-4 for a, b, _, _ in self.posts)

    def post(self, x, z, y1, y0=0.0, size=POST, mat="wood_weathered", adzed=False, interior=False, stone=True):
        """A post standing on a field stone (soseki, top at grade 0). Wall posts are planed boxes (the door jambs
        close against their faces, C17); the joya posts are adzed and sooted."""
        if self.has_post(x, z):
            return
        self.posts.append((x, z, y0, y1))
        if adzed:
            s = frame.post(self.H, x, z=z, y0=y0, y1=y1, size=size, adzed=True, mat=mat, vis=(1,))
            lo = self.H.add(box(x - size / 2, x + size / 2, y0, y1, z - size / 2, z + size / 2, mat,
                                vis=(2,) if interior else (2, 3), tag="post_lod"))
            s.interior = interior
            lo.interior = interior
        else:
            s = frame.post(self.H, x, z=z, y0=y0, y1=y1, size=size, mat=mat)
            s.interior = interior
        if stone:
            self.seed += 1
            found.soseki(self.H, x, z, self.seed % 8)

    def side_post(self, side, lx, y1, **kw):
        x, z = to_world(self.F[side], lx)
        self.post(round(x, 4), round(z, 4), y1, **kw)

    # ---------------------------------------------------------------- walls
    def wall_line(self, side, zones, y_top, feats=(), kind="shinkabe", finish="arakabe", koshiita=None, mat=None,
                  grime=True, post_top=None, interior=None, nodes_extra=()):
        """An exterior (or partition) wall line on `side` (a frame name or an explicit frame (yaw, origin) + length
        given as side=(fr, L)). zones: [(a, b, base_y)] local runs and the level each stands on (doma 0.05, raised
        floor, 0 for a shed floor); every run is closed from grade to base_y by an earth / board base. feats:
        [(a, b, y0, y1, 'door'|'window'|'open')] openings in local x (a, b = the opening's bay nodes). Posts at every
        ken node, every zone / feature node, up to post_top (default y_top)."""
        if isinstance(side, str):
            fr, L, nm = self.F[side], self.L[side], side
        else:
            fr, L, nm = side
        ns = {0.0, round(L, 4)}
        k = 1
        while k * KEN < L - 0.05:
            ns.add(round(k * KEN, 4))
            k += 1
        for (a, b, _) in zones:
            ns |= {round(a, 4), round(b, 4)}
        for f in feats:
            ns |= {round(f[0], 4), round(f[1], 4)}
        ns |= {round(v, 4) for v in nodes_extra}
        # no post inside a doorway (a ken node falling inside a door bay would stand in the opening)
        ns = sorted(v for v in ns if -1e-6 <= v <= L + 1e-6 and
                    not any(f[4] in ("door", "open") and f[0] + 1e-6 < v < f[1] - 1e-6 for f in feats))
        for lx in ns:
            x, z = to_world(fr, lx)
            self.post(round(x, 4), round(z, 4), post_top or y_top, interior=bool(interior == "both"),
                      stone=(interior != "both"))
        for i in range(len(ns) - 1):
            a, b = ns[i], ns[i + 1]
            base = None
            for (za, zb, zy) in zones:
                if za - 1e-6 <= a and b <= zb + 1e-6:
                    base = zy
            if base is None:
                continue
            ops = [(max(f[0], a) + (A_ if f[0] >= a - 1e-6 else 0.0), min(f[1], b) - (A_ if f[1] <= b + 1e-6 else 0.0),
                    f[2], f[3]) for f in feats if f[0] < b - 1e-6 and f[1] > a + 1e-6]
            is_door = any(f[4] in ("door", "open") for f in feats if f[0] < b - 1e-6 and f[1] > a + 1e-6)
            nm_ = "%s_%d" % (nm, int(a * 100))
            if base > 0.02:
                # the run's base from grade to its floor (under-floor enclosure / threshold), wall-thick
                s = self.B.P(nm_ + "_base")
                t_ = 0.075 if kind != "shinkabe" else walls.FINISH[finish][1]
                if kind == "board_vertical":
                    s.add(box(a - POST / 2 if i > 0 else a, b + POST / 2 if i < len(ns) - 2 else b, 0.0, base,
                              0.0, POST / 2 + 0.015, mat or "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
                              fire=True, tag="board_base"))
                else:
                    s.add(box(a + A_, b - A_, 0.0, base, -t_ / 2, t_ / 2,
                              walls.interior_mats("wall_" + finish, interior or "back"), vis=(1, 2, 3), geo=True,
                              view=True, fire=True, tag="infill_base"))
                self.B.put(s, fr)
            kosh = [(a + A_, b - A_, koshiita)] if koshiita and not is_door else None
            gr = [(a + A_, b - A_, None)] if grime and not is_door and kind == "shinkabe" else None
            self.B.wall(fr, nm_, kind, a, b, base, y_top, openings_=ops, finish=finish, koshiita=kosh, grime=gr,
                        mat=mat, interior=interior)
        return ns

    # ---------------------------------------------------------------- doors / windows
    def door(self, part, side, lx, dy, label, key=None, mirror=False):
        fr = self.F[side] if isinstance(side, str) else side
        d = self.B.place_door(part, fr, lx, dy, mirror=mirror, label=label)
        if key:
            self.dn[key] = "DoorsTwin%d" % len(self.H.doors)
        return d

    def window(self, part, side, lx, dy, label):
        self.windows.append((part, side, lx, dy, label))

    def place_windows(self):
        for (part, side, lx, dy, label) in self.windows:
            fr = self.F[side] if isinstance(side, str) else side
            self.B.place_door(part, fr, lx, dy, label=label)
            self.dn.setdefault("windows", []).append("DoorsTwin%d" % len(self.H.doors))

    # ---------------------------------------------------------------- kamachi (raised-floor edge) + step
    def kamachi(self, fr, L, floor_y, step_at, doma_name, soot=True):
        """The agari-kamachi along a raised floor's open edge: fr's local x runs along the edge (0..L), its local +z
        points into the doma. Under-floor boards (yukashita) close the void; a kutsunugi stone with the hidden walk
        ramp (<= 34 deg, found.step) at step_at; the ramp's footprint is an obstacle of the doma floor."""
        s = self.B.P("kamachi")
        s.add(box(0.0, L, DOMA, floor_y - 0.15, -0.03, 0.03, "wood_sooted", vis=(1, 2), geo=True, view=True, fire=True,
                  tag="yukashita_boards"))
        s.add(box(0.0, L, floor_y - 0.15, floor_y, -0.06, 0.06, KAMACHI_M if not soot else "wood_sooted",
                  vis=(1, 2, 3), geo=True, view=True, fire=True, tag="agari_kamachi"))
        self.B.interior = True
        self.B.put(s, fr)
        for cx in step_at:
            st = self.B.P("step_%d" % int(cx * 100))
            run = found.step(st, cx, "natural", drop=floor_y - DOMA, width=1.04)
            self.B.put(st, fr, 0.0, floor_y, what="jp_p_found_step_natural (kutsunugi + hidden ramp)")
            p0 = to_world(fr, cx - 0.54, 0.0)
            p1 = to_world(fr, cx + 0.54, run + 0.06)
            self.obst.append((doma_name, _r(p0[0], p1[0], p0[1], p1[1])))
        self.B.interior = False

    # ---------------------------------------------------------------- roof + koyagumi
    def roof(self, W, D, form, fam, E, ov=None, gov=None, soot=True, geya=(0.0, 0.0), ridge=None, joya_floor=0.0,
             members="log", xs=None, joya_posts=True, name="roof_main", stone_fn=None, slim_x=()):
        rp = self.B.P(name)
        sls, info = R.roof(rp, W, D, form, fam, eave_y=E, ov=ov, gov=gov, walkable=(fam != "thatch"),
                           ridge_kind=ridge)
        K = KY.koyagumi(rp, W, D, info, eave_y=E, members=members, geya=geya, floor_y=joya_floor, soot=soot, xs=xs)
        if soot:
            K["sooted_roof_solids"] = KY.soot_roof(rp)
        # the joya posts: re-placed as house posts (on soseki, registered for the C3 grid check, sooted, adzed)
        rp.solids = [s for s in rp.solids if s.tag != "joya_post"]
        if fam == "thatch":
            keep, k = [], 0
            for s in rp.solids:
                if s.tag == "rafter":
                    k += 1
                    if k % 2 == 0:
                        continue
                keep.append(s)
            rp.solids = keep
        if fam == "ishioki":
            ishioki_lod(rp, sls, info)
        self.H.merge(rp)
        if joya_posts:
            for (x, z, y0, y1) in K["posts"]:
                slim = any(abs(x - xs_) < 1e-4 for xs_ in slim_x)
                # a joya post on a partition line with doors is a planed 0.12 wall post (the door parts close
                # against 0.12 post faces); elsewhere an adzed 0.18 main post
                self.post(round(x, 4), round(z, 4), y1, y0=0.0, size=POST if slim else JOYA_POST,
                          mat="wood_sooted" if soot else "wood_weathered", adzed=not slim, interior=True,
                          stone=bool(stone_fn and stone_fn(x, z)))
        if form == "irimoya":
            # the sasu / ridge pole seen from above through an irimoya smoke gable stay in every LOD (C15)
            xg = (D / 4, W - D / 4)
            for s in self.H.solids:
                if s.tag in ("sasu", "sumi_sasu", "tsuma_sasu", "munagi", "lashing") and s.vis:
                    b_ = s.bbox()
                    if any(b_[0] - 0.3 < x_ < b_[1] + 0.3 for x_ in xg):
                        s.vis = set(s.vis) | {3}
        if fam != "thatch":
            rw = R.ridge_walk(info)
            if rw:
                self.H.merge(rw)
        self.log.append("roofs.roof %s %s eave %.2f + koyagumi %s (%s)" % (form, fam, E, K["system"], K["counts"]))
        return sls, info, K

    def keta_ring(self, W, D, E, hip):
        """Keta (wall plates) on the eave walls, and on the end walls of a hipped roof."""
        s = self.B.P("keta")
        ext = 0.06 if hip else 0.30
        frame.keta(s, -ext, W + ext, z=0.0, y_top=E)
        frame.keta(s, -ext, W + ext, z=-D, y_top=E)
        if hip:
            for x in (0.0, W):
                s.add(box(x - 0.06, x + 0.06, E - KETA_H, E, -D - 0.06, 0.06, "wood_weathered", vis=(1, 2, 3),
                          geo=True, view=True, fire=True, tag="keta"))
        self.H.merge(s)

    def gable(self, side, D, t, E, variant, thatch=False):
        g = self.B.P("gable_" + side)
        walls.gable(g, D, t, E, variant)
        if variant == "_board":
            # the gable boards have 4 mm gaps with nothing behind them (the panel slab is collision only): show the
            # slab in Resolution 1 as the boards' inner face, so no ray sees daylight between two boards (C11)
            for s in g.solids:
                if s.tag == "gable_geo":
                    s.vis = {1}
        if thatch:
            # under a thatch roof the gable panels stop at the rafter plane and the lath lies 5.5 cm above it: a
            # closing board along both roof lines seals that slot (C11: rays ran out under the thatch verge)
            h = D / 2
            for (a, b) in ((0.0, h), (h, D)):
                yr = lambda x: E + t * min(x, D - x)       # noqa: E731
                g.add(prism([(a, yr(a) - 0.03), (b, yr(b) - 0.03), (b, yr(b) + 0.07), (a, yr(a) + 0.07)], "z", -0.03,
                            0.03, "wood_weathered", vis=(1, 2), tag="gable_closer"))
        self.B.put(g, self.F[side], what="walls.gable %s (%s)" % (variant, side))
        # the gable's barred vent (a declared opening: the smoke / air vent) is a C11 portal
        yaw, o = self.F[side]
        for s in g.transformed(yaw, o).solids:
            if s.tag == "vent_geo":
                b = s.bbox()
                self.portals.append(("gable vent %s" % side, (b[0] - 0.25, b[1] + 0.25, b[2] - 0.05, b[3] + 0.05,
                                                              b[4] - 0.25, b[5] + 0.25)))

    # ---------------------------------------------------------------- rooms / info
    def room(self, name, tag, floor, y, rect, doors, note="", enclosed=True):
        self.rooms.append({"name": name, "tag": tag, "floor": floor, "level_m": y, "rect_kit": _r(*rect),
                           "doors": doors, "note": note, "enclosed": enclosed})

    def post_obstacles(self, pad=0.16):
        """Every post standing inside a room's rect becomes an obstacle of that room (loot points, floor samples)."""
        for r in self.rooms:
            x0, x1, z0, z1 = r["rect_kit"]
            for (x, z, _, _) in self.posts:
                if x0 + 0.05 < x < x1 - 0.05 and z0 + 0.05 < z < z1 - 0.05:
                    self.obst.append((r["name"], _r(x - pad, x + pad, z - pad, z + pad)))

    def finish(self, info_extra=None, exterior=None):
        B = self.B
        # every vanilla house has a Memory LOD; a shell without doors (an open shed) gets one harmless point
        self.H.memory.setdefault("ce_center", [(self.W / 2, 1.0, -self.D / 2)])
        if exterior:
            B.grime_exterior_posts(exterior)
        B.lod_policy()
        # rural far LOD (face budget, PLAYBOOK §12): the field stones and the posts / head rails that stand a few cm
        # proud of the walls leave Resolution 3 (the wall slabs carry the far silhouette); stones stay in Resolution 2
        for s in self.H.solids:
            if s.tag in ("soseki_lod", "post", "post_lod", "head_rail") and 3 in s.vis:
                s.vis = set(s.vis) - {3}
            if s.tag == "soseki_lod":
                s.vis = set(s.vis) - {2}          # the stones sit at grade (a few cm show): Resolution 1 only
            if s.tag in SILHOUETTE_TAGS and s.vis:
                s.vis = set(s.vis) | {1, 2, 3}    # §15 T7b / C15: what forms the roof outline stays in every LOD
        self.post_obstacles()
        fls = [{"name": r["name"], "tag": r["tag"], "rect": tuple(r["rect_kit"]), "y": r["level_m"],
                "obstacles": [rc for (n_, rc) in self.obst if n_ == r["name"]], "enclosed": r["enclosed"]}
               for r in self.rooms]
        info = {"W": self.W, "D": self.D, "rooms": self.rooms, "floors": fls, "posts": list(self.posts),
                "log": self.log, "portals": self.portals, "fittings": self.fittings, "passages": self.passages,
                "doors": dict(self.dn)}
        info.update(info_extra or {})
        return self.H, info


def ishioki_lod(part, sls, info=None):
    """Stone-weighted boards (ishioki) on a small shell (face budget + C15): keep every third field stone and every
    other ridge stone in Resolution 1, drop the kit's Resolution 2 stones, and give Resolution 2 / 3 a thin stone
    layer (0.07 over the boards) and a ridge band instead, so the far silhouette stays within 0.10 m of the stones."""
    from ..shapes import slab
    keep, k, kr = [], 0, 0
    for s in part.solids:
        if s.tag == "roof_stone":
            if 1 not in s.vis:
                continue
            k += 1
            if k % 3:
                continue
        if s.tag == "ridge_stone":
            kr += 1
            if kr % 2 == 0:
                continue
        keep.append(s)
    part.solids = keep
    st = R.STACK["ishioki"]
    for sl in sls:
        for pc in sl.pieces:
            part.add(slab(pc, lambda x, z, s_=sl: s_.y(x, z, st + 0.005), lambda x, z, s_=sl: s_.y(x, z, st + 0.07),
                          "roof_kureita", vis=(2, 3), tag="stone_layer_lod"))
    if info and "ridge" in info:
        (x0, yr, zr), (x1, _, _) = info["ridge"]
        part.add(box(x0 + 0.05, x1 - 0.05, yr, yr + 0.13, zr - 0.13, zr + 0.13, "roof_kureita", vis=(2, 3),
                     tag="ridge_stone_lod"))


def _mirror(H, info):
    """The finished shell mirrored about x = W / 2 (x -> W - x): the doma on the other end."""
    W = info["W"]
    M = H.transformed(0.0, (W, 0.0, 0.0), mirror=True)
    M.meta = dict(H.meta)

    def mx(r):
        return (W - r[1], W - r[0], r[2], r[3])
    info = dict(info)
    info["rooms"] = [dict(r, rect_kit=mx(r["rect_kit"])) for r in info["rooms"]]
    info["floors"] = [dict(f, rect=mx(f["rect"]), obstacles=[mx(o) for o in f["obstacles"]]) for f in info["floors"]]
    info["posts"] = [(round(W - x, 4), z, y0, y1) for (x, z, y0, y1) in info["posts"]]
    info["portals"] = [(n, (W - b[1], W - b[0], b[2], b[3], b[4], b[5])) for n, b in info["portals"]]
    info["passages"] = [(W - x, z, y) for (x, z, y) in info["passages"]]
    fits = []
    for f in info["fittings"]:
        g = dict(f)
        if "rect" in g:
            g["rect"] = mx(g["rect"])
        if "centre" in g:
            g["centre"] = (W - g["centre"][0], g["centre"][1])
        if "hook" in g:
            g["hook"] = (W - g["hook"][0], g["hook"][1], g["hook"][2])
        if "yaw" in g:
            g["yaw"] = (-g["yaw"]) % 360.0
        fits.append(g)
    info["fittings"] = fits
    return M, info


def _irori(S, room, cx, cz, along_x, floor_y, K_levels, kind="irori", size=(0.91, 1.365)):
    """The irori pit rect (x0, x1, z0, z1) centred on (cx, cz) + its fitting record (hook point under the tie beam
    of the frame line it is centred on)."""
    a, b = (size[1], size[0]) if along_x else (size[0], size[1])
    rect = (cx - a / 2, cx + a / 2, cz - b / 2, cz + b / 2)
    hook_y = K_levels.get("beam_top", 3.0) - 0.30
    S.fittings.append({"kind": "irori", "room": room, "rect": rect, "floor_y": floor_y, "pit": kind,
                       "hook": (cx, round(hook_y, 3), cz), "note": "jp_p_fit_irori pit; jizai-kagi hangs from the "
                       "tie beam on this frame line (hook y = beam underside)"})
    pad = 0.12 if kind == "irori" else 0.30
    S.obst.append((room, _r(rect[0] - pad, rect[1] + pad, rect[2] - pad, rect[3] + pad)))
    return rect


def _kamado(S, room, cx, cz, yaw, size=(1.30, 0.70)):
    """A kamado spot on the doma (jp_p_fit_kamado _2: 0.70 x 1.30): kept clear of loot points; C3 places the stove."""
    w, d = size
    ca, sa = abs(math.cos(math.radians(yaw))), abs(math.sin(math.radians(yaw)))
    hx, hz = (w * ca + d * sa) / 2, (w * sa + d * ca) / 2
    S.fittings.append({"kind": "kamado", "room": room, "centre": (cx, cz), "yaw": yaw, "size": size,
                       "note": "jp_p_fit_kamado _2 spot (mouths face along yaw: 0 = +z); back to the wall"})
    S.obst.append((room, _r(cx - hx - 0.25, cx + hx + 0.25, cz - hz - 0.25, cz + hz + 0.25)))


# ------------------------------------------------------------------------------------------------ DW06 Kanto
def kanto(name=None, form="yosemune", ridge="bamboo", stable=False, doma="left", wear="_w1"):
    W, D, g = 7 * KEN, 5 * KEN, KEN
    E, FLOOR = 3.30, FARM_FLOOR
    YT = E - KETA_H                          # wall top = keta underside
    XR, XD = 2 * KEN, 4 * KEN                # small rooms 0..XR | hiroma XR..XD | doma XD..W (canonical: doma right)
    ZS = -D / 2                              # dei (front) / nando (back) split
    S = Shell(name or "jp_farmhouse_kanto", W, D, [1, 2], "Kanto farmhouse, hiroma type (DW06)", wear)
    B = S.B
    # ------------------------------------------------ roof + koyagumi first (its joya posts are house posts)
    sls, info_r, K = S.roof(W, D, form, "thatch", E, ov=0.90, geya=(g, g), ridge=ridge, joya_floor=0.0,
                           stone_fn=lambda x, z: x > XD + 0.1, slim_x=(XR,))
    S.keta_ring(W, D, E, hip=True)
    if form == "irimoya":
        for xg, sg in ((D / 4, -1), (W - D / 4, 1)):
            S.portals.append(("smoke gable %s" % ("L" if sg < 0 else "R"),
                              (xg - 0.6, xg + 0.6, E + 0.5, E + D / 2 + 1.2, -D / 2 - D / 4 - 0.2, -D / 2 + D / 4 + 0.2)))
    # ------------------------------------------------ exterior walls (nakanuri + koshiita: a landed farmer, T2)
    fin, kosh = "nakanuri", 0.90
    front_feats = [(0.5 * KEN, 1.0 * KEN, FLOOR + 0.90, FLOOR + 1.65, "window"),
                   (4.0 * KEN, 4.5 * KEN, DOMA + 0.90, DOMA + 1.65, "window"),
                   (5.0 * KEN, 6.0 * KEN, DOMA, DOMA + 2.0, "door")]
    S.wall_line("front", [(0.0, XD, FLOOR), (XD, W, DOMA)], YT, front_feats, finish=fin, koshiita=kosh,
                nodes_extra=(1.5 * KEN, 2.5 * KEN, 3.0 * KEN, 3.5 * KEN, 4.5 * KEN))
    S.door(big_leaf("_battened"), "front", 5.0 * KEN, DOMA, "Front door (ooto, doma)", "front")
    S.window(openings.part_window_slide("_board"), "front", 0.5 * KEN, FLOOR, "Dei window (front)")
    S.window(openings.part_window_slide("_board"), "front", 4.0 * KEN, DOMA, "Doma window (front)")
    # back wall: local lx = W - x
    back_feats = [(2.0 * KEN, 3.0 * KEN, DOMA, DOMA + 2.0, "door"),
                  (4.0 * KEN, 4.5 * KEN, FLOOR + 0.90, FLOOR + 1.65, "window"),
                  (6.0 * KEN, 6.5 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window")]
    S.wall_line("back", [(0.0, W - XD, DOMA), (W - XD, W, FLOOR)], YT, back_feats, finish=fin, koshiita=kosh,
                nodes_extra=(3.5 * KEN, 5.0 * KEN, 5.5 * KEN))
    S.door(openings.part_itado("_single"), "back", 2.0 * KEN, DOMA, "Back door (doma)", "back")
    S.window(openings.part_window_slide("_board"), "back", 4.0 * KEN, FLOOR, "Hiroma window (back)")
    S.window(openings.part_tsukiage("_board"), "back", 6.0 * KEN, FLOOR, "Nando window (back, push-up shutter)")
    # left end (small rooms): local lx = z + D
    left_feats = [(1.0 * KEN, 1.5 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window")]
    S.wall_line("left", [(0.0, D, FLOOR)], YT, left_feats, finish=fin, koshiita=kosh, nodes_extra=(2.5 * KEN,))
    S.window(openings.part_tsukiage("_board"), "left", 1.0 * KEN, FLOOR, "Nando window (end, push-up shutter)")
    # right end (doma): local lx = -z
    right_feats = [(0.5 * KEN, 1.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")]
    S.wall_line("right", [(0.0, D, DOMA)], YT, right_feats, finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN,))
    S.window(openings.part_window_slide("_board"), "right", 0.5 * KEN, DOMA, "Doma window (end)")
    # ------------------------------------------------ partitions (interior, open above to the koyagumi)
    PT = FLOOR + walls.HEAD_T + 2.0 + 0.45                   # partition top (a head rail + a kokabe band)
    B.interior = True
    F_P = (90.0, (XR, 0.0, -D))                              # x = XR, local lx = z + D
    S.wall_line((F_P, D, "part_x"), [(0.0, D, FLOOR)], PT,
                [(1.0 * KEN, 2.0 * KEN, FLOOR, FLOOR + 2.0, "door"), (3.0 * KEN, 4.0 * KEN, FLOOR, FLOOR + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(2.5 * KEN, 4.5 * KEN))
    S.door(openings.part_itado("_single"), F_P, 1.0 * KEN, FLOOR, "Hiroma -> nando", "nando")
    S.door(openings.part_shoji_ext("_single"), F_P, 3.0 * KEN, FLOOR, "Hiroma -> dei", "dei")
    F_Z = (0.0, (0.0, 0.0, ZS))
    S.wall_line((F_Z, XR, "part_z"), [(0.0, XR, FLOOR)], PT, (), finish="nakanuri", grime=False, interior="both")
    B.interior = False
    # ------------------------------------------------ floors
    B.interior = True
    B.merge(FL.doma("doma", XD, W, -D, 0.0, road=(XD + 0.07, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    pit = _irori(S, "hiroma", 3.0 * KEN, -D / 2, False, FLOOR, K["levels"])
    B.merge(FL.boards("hiroma", XR + A_, XD - 0.06, -D + A_, -A_, FLOOR, holes=[pit + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    # M1 (2026-09-30): brown (cha) heri in the T2 farmhouse best room (A2 BUILD_LIST "Heri colour")
    B.merge(FL.tatami("dei", A_, XR - A_, ZS + A_, -A_, top=FLOOR, base=0.0, mats=FL.MATS_TATAMI_CHA))
    B.merge(FL.boards("nando", A_, XR - A_, -D + A_, ZS - A_, FLOOR, mats=BOARDS_ROUGH))
    B.interior = False
    F_K = (-90.0, (XD, 0.0, 0.0))                            # kamachi: local x = -z, local +z -> +x (the doma)
    S.kamachi(F_K, D, FLOOR, [1.5 * KEN], "doma")
    _kamado(S, "doma", W - 0.50, -2.0 * KEN, 270.0)
    if stable:
        wst, dst = SL.VARIANTS["_umaya"][0] * KEN, SL.VARIANTS["_umaya"][1] * KEN
        x0s = W - A_ - 0.06 - wst
        B.interior = True
        B.merge(SL.part_stall("_umaya").transformed(0.0, (x0s, DOMA, -D + dst)))
        B.interior = False
        S.obst.append(("doma", _r(x0s - 0.12, W, -D, -D + dst + 0.14)))
        S.fittings.append({"kind": "stall", "room": "doma", "rect": (x0s, W - A_, -D + A_, -D + dst),
                           "note": "jp_p_frame_stall _umaya (inside stable), bars down"})
        S.log.append("jp_p_frame_stall _umaya in the doma's back corner x %.2f..%.2f" % (x0s, x0s + wst))
    S.place_windows()
    # ------------------------------------------------ rooms
    S.room("doma", "doma", "earth", DOMA, (XD + 0.07, W - A_, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "doma: entry, kamado spot on the end wall" + (", the inside stable (umaya)" if stable else ""))
    S.room("hiroma", "daidokoro", "boards", FLOOR, (XR + A_, XD - 0.07, -D + A_, -A_), [S.dn["nando"], S.dn["dei"]],
           "hiroma with the irori, open to the doma over the agari-kamachi")
    S.room("dei", "zashiki", "tatami", FLOOR, (A_, XR - A_, ZS + A_, -A_), [S.dn["dei"]], "dei (best room)")
    S.room("nando", "sleeping", "boards", FLOOR, (A_, XR - A_, -D + A_, ZS - A_), [S.dn["nando"]], "nando")
    H, info = S.finish({"params": {"kind": "kanto", "form": form, "ridge": ridge, "stable": stable, "doma": doma},
                        "levels": {"doma": DOMA, "floor": FLOOR, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    if doma == "right":
        H, info = _mirror(H, info)
    return H, info


# ------------------------------------------------------------------------------------------------ DW07 Kinai
def _takahe(S, x, D, E, t, sg, stack_top, pent_top):
    """Yamato-mune gable (takahe): a plastered wing wall on the gable line x standing proud of the thatch (0.12 over
    its top), both slopes, capped with kawara (walls.kawara_cap) and cut clear of the lower roofs (pent_top)."""
    s = S.B.P("takahe_%d" % int(x * 10))
    h = D / 2
    th = 0.30
    # FB1 (2026-10-01, Stephen: "a weird thick something below the roof"): the band used to hang 0.45 m below the
    # slope line all the way out to the thatch eave, so at each corner a 0.3 m x ~1 m white block stood out under the
    # eave, and the thatch ridge bundle (0.55 high, run 0.25 past the gable) rose over the wall's top and poked out
    # of it. Now: over the eave overhang (outside the wall line) the takahe starts at the thatch underside, so its end
    # is a thatch-thick plastered cheek; only inside the wall line does it reach down onto the gable wall; its top
    # rises from 0.12 over the thatch at the eave to 0.12 over the ridge bundle at the ridge (yamato-mune: the
    # takahe stands proud of the whole thatch), and the ridge bundle stops inside it (kinai(), after the roof).
    ridge_extra = 0.55 + 0.10 - 0.12           # thatch_ridge 'bamboo' H 0.55 over the ridge line + 0.10, minus the 0.12
    for zsgn in (1.0, -1.0):
        ov = 0.60
        z_e = ov if zsgn > 0 else -D - ov
        z_w = 0.0 if zsgn > 0 else -D          # the wall line
        z_r = -h
        slope = lambda z: E + t * (min(-z, D + z))                           # noqa: E731
        run = abs(z_r - z_e)
        y_top = lambda z: slope(z) + stack_top + 0.12 + ridge_extra * (1.0 - abs(z - z_r) / run)  # noqa: E731
        y_low = lambda z: slope(z) + R.STACK["thatch"]                       # noqa: E731  (thatch underside)
        y_bot = lambda z: slope(z) - 0.45                                    # noqa: E731
        for poly in ([(z_e, y_low(z_e)), (z_e, y_top(z_e)), (z_w, y_top(z_w)), (z_w, y_low(z_w))],
                     [(z_w, y_bot(z_w)), (z_w, y_top(z_w)), (z_r, y_top(z_r)), (z_r, y_bot(z_r))]):
            poly = clean_poly(clip_poly(poly, 0.0, -1.0, -(pent_top + 0.08)))    # keep y >= pent_top + 0.08
            if len(poly) >= 3:
                s.add(prism([(yy, zz) for zz, yy in poly], "x", x - th / 2, x + th / 2, "wall_shikkui",
                             vis=(1, 2, 3), geo=True, view=True, fire=True, tag="takahe"))
        walls.kawara_cap(s, (x, y_top(z_e), z_e), (x, y_top(z_r), z_r), width=0.38, courses=2)
    S.H.merge(s)


def kinai(name=None, form="kirizuma", lower="tile", takahe=False, doma="right", wear="_w1"):
    W, D = 7 * KEN, 4 * KEN
    E, FLOOR = 4.30, FARM_FLOOR
    t = R.PITCH["thatch"]
    YT = E - (KETA_H if form != "kirizuma" else 0.0)
    XN = 3 * KEN                                 # niwa 0..XN (canonical: doma left) | rooms XN..W
    XM = 5 * KEN                                 # mise / daidokoro | zashiki / nando split
    ZS = -D / 2                                  # front / back rooms
    PENT_Y, PENT_P = 3.50, 1.20             # the lower roofs: wall line height, projection
    kind = "tile" if lower == "tile" else "board"
    S = Shell(name or "jp_farmhouse_kinai", W, D, [1, 2], "Kinai farmhouse, yotsuma-dori with the ox (DW07)", wear)
    B = S.B
    # ------------------------------------------------ roof (no geya: the lower roofs are pents), koyagumi, sooted
    gov = 0.05 if takahe else None
    sls, info_r, K = S.roof(W, D, form, "thatch", E, ov=0.60, gov=gov, ridge="bamboo")
    if takahe and form == "kirizuma":
        # FB1 (2026-10-01): the thatch ridge bundle stops inside the takahe walls (it ran 0.25 m past each gable line
        # and showed over / outside the plastered gable, Stephen's "weird thick something"); its end bindings go
        keep = []
        for s_ in S.H.solids:
            if s_.tag in ("thatch_ridge", "ridge_bamboo"):
                s_.verts = [(min(max(v[0], 0.0), W), v[1], v[2]) for v in s_.verts]
                s_.center = tuple(sum(v[k] for v in s_.verts) / len(s_.verts) for k in range(3))
            elif s_.tag == "binding" and s_.center[1] > E + 1.0 and not (0.16 < s_.center[0] < W - 0.16):
                continue
            keep.append(s_)
        S.H.solids = keep
    hip = form != "kirizuma"
    if hip:
        S.keta_ring(W, D, E, hip=True)
        for xg, sg in ((D / 4, -1), (W - D / 4, 1)):
            S.portals.append(("smoke gable %s" % ("L" if sg < 0 else "R"),
                              (xg - 0.6, xg + 0.6, E + 0.5, E + D / 2 + 1.2, -D / 2 - D / 4 - 0.2, -D / 2 + D / 4 + 0.2)))
    else:
        S.keta_ring(W, D, E, hip=False)
    ytop_long = E - KETA_H
    y_end = E - KETA_H if hip else E - 0.21
    fin = "nakanuri"
    # ------------------------------------------------ long walls, the lower roofs (pents) on them
    front_feats = [(1.0 * KEN, 2.0 * KEN, DOMA, DOMA + 2.0, "door"),
                   (3.5 * KEN, 4.0 * KEN, FLOOR + 0.90, FLOOR + 1.65, "window"),
                   (5.0 * KEN, 6.0 * KEN, FLOOR + 0.70, FLOOR + 2.0, "window")]
    S.wall_line("front", [(0.0, XN, DOMA), (XN, W, FLOOR)], ytop_long, front_feats, finish=fin, koshiita=0.90,
                nodes_extra=(4.5 * KEN, 6.5 * KEN))
    S.door(big_leaf("_battened"), "front", 1.0 * KEN, DOMA, "Front door (niwa)", "front")
    S.window(openings.part_window_slide("_board"), "front", 3.5 * KEN, FLOOR, "Mise window (front)")
    S.window(openings.part_amado_window("_twin"), "front", 5.0 * KEN, FLOOR, "Zashiki window (front, amado)")
    # back: lx = W - x; niwa x 0..3K -> lx 4K..7K
    back_feats = [(4.5 * KEN, 5.5 * KEN, DOMA, DOMA + 2.0, "door"),
                  (2.5 * KEN, 3.0 * KEN, FLOOR + 0.90, FLOOR + 1.65, "window"),
                  (0.5 * KEN, 1.0 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window")]
    S.wall_line("back", [(0.0, W - XN, FLOOR), (W - XN, W, DOMA)], ytop_long, back_feats, finish=fin, koshiita=0.90,
                nodes_extra=(3.5 * KEN, 6.0 * KEN))
    S.door(openings.part_itado("_single"), "back", 4.5 * KEN, DOMA, "Back door (niwa)", "back")
    S.window(openings.part_window_slide("_board"), "back", 2.5 * KEN, FLOOR, "Daidokoro window (back)")
    S.window(openings.part_tsukiage("_board"), "back", 0.5 * KEN, FLOOR, "Nando window (back, push-up shutter)")
    for side in ("front", "back"):
        s = B.P("pent_" + side)
        roofparts.pent(s, 0.0, W, PENT_Y, PENT_P, 0.40 if kind == "tile" else 0.30, kind)
        B.put(s, S.F[side], what="roofparts.pent %s: the Kinai lower roof (%s)" % (kind, side))
        # the pent's wall plate: a beam across the tall wall at the pent line (no plaster panel over 2 x 2 m, §6.2)
        s = B.P("pent_beam_" + side)
        s.add(box(0.0, W, PENT_Y - 0.34, PENT_Y - 0.18, POST / 2 - 0.02, POST / 2 + 0.03, "wood_weathered",
                  vis=(1, 2), tag="pent_plate"))
        B.put(s, S.F[side])
    # ------------------------------------------------ end walls (+ thatch gables on a kirizuma roof)
    left_feats = [(2.5 * KEN, 3.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")]
    S.wall_line("left", [(0.0, D, DOMA)], y_end, left_feats, finish=fin, koshiita=0.90,
                nodes_extra=(1.5 * KEN, 3.5 * KEN))
    S.window(openings.part_window_slide("_board"), "left", 2.5 * KEN, DOMA, "Niwa window (end)")
    right_feats = [(2.5 * KEN, 3.0 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window")]
    S.wall_line("right", [(0.0, D, FLOOR)], y_end, right_feats, finish=fin, koshiita=0.90)
    S.window(openings.part_tsukiage("_board"), "right", 2.5 * KEN, FLOOR, "Nando window (end, push-up shutter)")
    if not hip:
        for side in ("left", "right"):
            S.gable(side, D, t, E, "_thatch", thatch=True)
        if takahe:
            st = R.STACK["thatch"] + 0.60
            for x, sg in ((0.0, -1), (W, 1)):
                _takahe(S, x, D, E, t, sg, st, PENT_Y + 0.25)
            S.log.append("takahe (yamato-mune) parapets on both gables")
    # ------------------------------------------------ partitions
    PT = FLOOR + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F_PX = (90.0, (XM, 0.0, -D))                 # x = XM, lx = z + D: nando/daidokoro (lx 0..2K), zashiki/mise (2K..4K)
    S.wall_line((F_PX, D, "part_xm"), [(0.0, D, FLOOR)], PT,
                [(0.5 * KEN, 1.5 * KEN, FLOOR, FLOOR + 2.0, "door"), (2.5 * KEN, 3.5 * KEN, FLOOR, FLOOR + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both")
    S.door(openings.part_itado("_single"), F_PX, 0.5 * KEN, FLOOR, "Daidokoro -> nando", "nando")
    S.door(openings.part_shoji_ext("_single"), F_PX, 2.5 * KEN, FLOOR, "Mise -> zashiki", "zashiki")
    F_ZM = (0.0, (XN, 0.0, ZS))                  # z = ZS, lx = x - XN: mise | daidokoro (0..2K), zashiki | nando
    S.wall_line((F_ZM, W - XN, "part_zs"), [(0.0, W - XN, FLOOR)], PT,
                [(0.5 * KEN, 1.5 * KEN, FLOOR, FLOOR + 2.0, "door")], finish="nakanuri", grime=False,
                interior="both")
    S.door(openings.part_shoji_ext("_hikiwake"), F_ZM, 0.5 * KEN, FLOOR, "Mise <-> daidokoro", "mid")
    B.interior = False
    # ------------------------------------------------ floors
    B.interior = True
    B.merge(FL.doma("niwa", 0.0, XN, -D, 0.0, road=(A_, XN - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    pit = _irori(S, "daidokoro", 4.0 * KEN, -3.0 * KEN, True, FLOOR, K["levels"])
    B.merge(FL.boards("daidokoro", XN + 0.06, XM - A_, -D + A_, ZS - A_, FLOOR, holes=[pit + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    B.merge(FL.boards("mise", XN + 0.06, XM - A_, ZS + A_, -A_, FLOOR, mats=BOARDS_ROUGH))
    # M1 (2026-09-30): brown (cha) heri in the T2 farmhouse best room (A2 BUILD_LIST "Heri colour")
    B.merge(FL.tatami("zashiki", XM + A_, W - A_, ZS + A_, -A_, top=FLOOR, base=0.0, mats=FL.MATS_TATAMI_CHA))
    B.merge(FL.boards("nando", XM + A_, W - A_, -D + A_, ZS - A_, FLOOR, mats=BOARDS_ROUGH))
    B.interior = False
    F_K = (90.0, (XN, 0.0, -D))                  # kamachi x = XN: lx = z + D, local +z -> -x (the niwa)
    S.kamachi(F_K, D, FLOOR, [1.0 * KEN, 3.0 * KEN], "niwa")
    # ------------------------------------------------ the ox stall (required) in the niwa's back corner, the kamado
    wst, dst = SL.VARIANTS["_ox"][0] * KEN, SL.VARIANTS["_ox"][1] * KEN
    x0s = A_ + 0.06
    B.interior = True
    B.merge(SL.part_stall("_ox").transformed(0.0, (x0s, DOMA, -D + dst)))
    B.interior = False
    S.obst.append(("niwa", _r(0.0, x0s + wst + 0.14, -D, -D + dst + 0.14)))
    S.fittings.append({"kind": "stall", "room": "niwa", "rect": (x0s, x0s + wst, -D + A_, -D + dst),
                       "note": "jp_p_frame_stall _ox (the ox, required), bars down"})
    _kamado(S, "niwa", 0.50, -0.9 * KEN, 90.0)
    S.fittings.append({"kind": "kabata", "room": "niwa", "note": "not built: the kabata washing pit needs running "
                       "water (a new pit kind + water material); left for later"})
    S.place_windows()
    S.room("niwa", "doma", "earth", DOMA, (A_, XN - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "niwa: entry, kamado spot, the ox stall")
    S.room("mise", "living", "boards", FLOOR, (XN + 0.07, XM - A_, ZS + A_, -A_), [S.dn["zashiki"], S.dn["mid"]],
           "mise (front living room), open to the niwa")
    S.room("daidokoro", "daidokoro", "boards", FLOOR, (XN + 0.07, XM - A_, -D + A_, ZS - A_),
           [S.dn["nando"], S.dn["mid"]], "daidokoro with the irori, open to the niwa")
    S.room("zashiki", "zashiki", "tatami", FLOOR, (XM + A_, W - A_, ZS + A_, -A_), [S.dn["zashiki"]], "zashiki")
    S.room("nando", "sleeping", "boards", FLOOR, (XM + A_, W - A_, -D + A_, ZS - A_), [S.dn["nando"]], "nando")
    H, info = S.finish({"params": {"kind": "kinai", "form": form, "lower": lower, "takahe": takahe, "doma": doma},
                        "levels": {"doma": DOMA, "floor": FLOOR, "eave": E, "pent": PENT_Y}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    if doma == "left":
        H, info = _mirror(H, info)
    return H, info


# ------------------------------------------------------------------------------------------------ lean-to (gable end)
def _gable_leanto(S, side, fam, E, t_main, depth=KEN, t_lt=0.30):
    """An open lean-to (woodshed / work space) on a gable end: posts on soseki on its outer line every ken, the
    lean-to roof (leanto.roof: board coverings) sloping away from the gable wall, its top kept under the main roof's
    eave corners (the lean-to runs the whole gable). Floor: doma, not enclosed (C11 skips it)."""
    D = S.D
    gl = 0.05
    top = E - t_main * gl - 0.25                   # lean-to covering top at the gable wall, clear of the main eave
    #                                                corners, keta ends and bargeboards (C12)
    stack = R.STACK[fam]
    y_wall = top - stack                           # rafter underside at the gable wall
    eave = y_wall - t_lt * depth                   # keta top at the outer line
    zw = -(POST / 2 + 0.02)                        # against the gable wall's outer face (clear of its posts, C12)
    s, sl = leanto.roof("leanto_" + side, 0.0, D, zw, -depth, eave, fam, t=t_lt, gov=gl,
                        flash_top=top + 0.10, keta_ext=0.06)
    if fam == "ishioki":
        ishioki_lod(s, [sl])
    if side == "left":
        fr = (-90.0, (0.0, 0.0, 0.0))              # local x -> -z (0..-D), local -z -> -x
        xo = -depth
    else:
        fr = (90.0, (S.W, 0.0, -D))                # local x -> +z (-D..0), local -z -> +x
        xo = S.W + depth
    S.B.put(s, fr, what="leanto.roof %s on the %s gable (open lean-to)" % (fam, side))
    for k in range(int(round(D / KEN)) + 1):
        z = -k * KEN
        S.post(round(xo, 4), round(z, 4), eave - KETA_H)
    x0, x1 = (xo, 0.0) if side == "left" else (S.W, xo)
    nm = "leanto"
    S.B.interior = True
    S.B.merge(FL.doma(nm, x0 - (0.3 if side == "left" else 0.0), x1 + (0.3 if side == "right" else 0.0), -D - 0.3,
                      0.3, road=_r(x0 + (0.15 if side == "left" else 0.07), x1 - (0.07 if side == "left" else 0.15),
                                   -D + 0.15, -0.15), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    S.B.interior = False
    S.room(nm, "workshop", "earth", DOMA, _r(x0 + (0.15 if side == "left" else 0.07),
                                             x1 - (0.07 if side == "left" else 0.15), -D + 0.15, -0.15), [],
           "open lean-to on the %s gable (woodshed / work space)" % side, enclosed=False)
    S.log.append("lean-to %s: eave %.2f, top at the wall %.2f (main eave %.2f)" % (side, eave, top, E))
    return eave


# ------------------------------------------------------------------------------------------------ huts and sheds
def _hut_floor(S, floor, x_doma, W, D, FLOOR, soot=True, K=None):
    """Hut floors: 'earth' (one doma, stone-ringed irori_doma pit), 'board' / 'sunoko' (doma x 0..x_doma, a raised
    floor x_doma..W at FLOOR with the irori pit, the agari-kamachi and a step)."""
    B = S.B
    lv = K["levels"] if K else {}
    if floor == "earth":
        cx = (W + x_doma) / 2 if W > 3.5 * KEN else 2.0 * KEN
        cx = round(cx / KEN) * KEN
        pit = _irori(S, "doma", cx, -D / 2, False, DOMA, lv, kind="irori_doma", size=(0.72, 0.72))
        B.interior = True
        B.merge(FL.doma("doma", 0.0, W, -D, 0.0, road=(A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH,
                        holes=[pit + ("pit",)], hole_fn=PI.pit_fn("irori_doma")))
        B.interior = False
        return {"doma": _r(A_, W - A_, -D + A_, -A_)}
    B.interior = True
    B.merge(FL.doma("doma", 0.0, x_doma, -D, 0.0, road=(A_, x_doma - 0.07, -D + A_, -A_), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    cx = round(((x_doma + W) / 2) / KEN) * KEN
    pit = _irori(S, "living", cx, -D / 2, False, FLOOR, lv, size=(0.91, 0.91))
    if floor == "board":
        B.merge(FL.boards("living", x_doma + 0.06, W - A_, -D + A_, -A_, FLOOR, holes=[pit + ("pit",)],
                          hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    else:
        B.merge(PI.sunoko("living", x_doma + 0.06, W - A_, -D + A_, -A_, FLOOR, "take", holes=[pit + ("pit",)],
                          hole_fn=PI.pit_fn("irori")))
    B.interior = False
    F_K = (90.0, (x_doma, 0.0, -D))                # kamachi x = x_doma: lx = z + D, local +z -> -x (the doma)
    S.kamachi(F_K, D, FLOOR, [D / 2 + (0.35 if D > 2.5 * KEN else 0.0)], "doma", soot=soot)
    return {"doma": _r(A_, x_doma - 0.07, -D + A_, -A_), "living": _r(x_doma + 0.07, W - A_, -D + A_, -A_)}


def hut_east(name=None, size="s", floor="earth", door="itado", wear="_w2"):
    W, D = (3 * KEN, 2 * KEN) if size == "s" else (4 * KEN, 3 * KEN)
    E = 3.10
    YT = E - KETA_H
    FLOOR = HUT_FLOOR
    XD = KEN if size == "s" else 1.5 * KEN
    S = Shell(name or "jp_hut_east", W, D, [1], "poor hut, east type (DW01), thatch hipped", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "yosemune", "thatch", E, ov=0.90, ridge="bamboo" if size == "s" else "shiba")
    S.keta_ring(W, D, E, hip=True)
    raised = floor != "earth"
    lv_room = FLOOR if raised else DOMA
    zones_front = [(0.0, XD, DOMA), (XD, W, lv_room)] if raised else [(0.0, W, DOMA)]
    feats = [(0.0, KEN, DOMA, DOMA + 2.0, "door" if door == "itado" else "open")]
    S.wall_line("front", zones_front, YT, feats, finish="arakabe", nodes_extra=(2.0 * KEN,))
    if door == "itado":
        S.door(big_leaf("_plain"), "front", 0.0, DOMA, "Door (itado)", "front")
    else:
        B.put(openings.part_mushiro("_rolled"), S.F["front"], 0.0, DOMA, what="jp_p_open_mushiro _rolled (open door)")
        # the open doorway is the room's portal (C11) and a passage (clear >= 1.00, head >= 2.00)
        S.portals.append(("mushiro doorway", (A_ - 0.05, KEN - A_ + 0.05, DOMA - 0.1, DOMA + 2.1, -0.25, 0.25)))
        S.passages.append((KEN / 2, 0.0, DOMA))
    # back wall: lx = W - x; a board-shutter window behind renji bars into the living part
    bw = (0.5 * KEN, 1.0 * KEN, lv_room + 0.90, lv_room + 1.65, "window")
    zones_back = [(0.0, W - XD, lv_room), (W - XD, W, DOMA)] if raised else [(0.0, W, DOMA)]
    S.wall_line("back", zones_back, YT, [bw], finish="arakabe")
    S.window(openings.part_window_slide("_board"), "back", 0.5 * KEN, lv_room, "Window (back)")
    S.wall_line("left", [(0.0, D, DOMA)], YT, (), finish="arakabe")
    rf = [(1.0 * KEN, 1.5 * KEN, lv_room + 0.90, lv_room + 1.60, "window")] if size == "l" else []
    S.wall_line("right", [(0.0, D, lv_room)], YT, rf, finish="arakabe")
    if rf:
        S.window(openings.part_tsukiage("_board"), "right", 1.0 * KEN, lv_room, "Window (end, push-up shutter)")
    rects = _hut_floor(S, floor, XD, W, D, FLOOR, K=K)
    kx = 0.45
    _kamado(S, "doma", kx, -D + 0.45 if raised else -D + 0.55, 0.0, size=(0.60, 0.60))
    S.place_windows()
    doors = [S.dn["front"]] if "front" in S.dn else []
    S.room("doma", "doma", "earth", DOMA, rects["doma"], doors, "doma" + ("" if raised else " (the whole hut: "
           "earth floor, straw mats on it are C3's; the stone-ringed hearth)"))
    if raised:
        S.room("living", "living", "boards" if floor == "board" else "bamboo slats", FLOOR, rects["living"], [],
               "living floor with the irori, open to the doma")
    H, info = S.finish({"params": {"kind": "hut_east", "size": size, "floor": floor, "door": door},
                        "levels": {"doma": DOMA, "floor": FLOOR, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


def hut_west(name=None, roof="thatch", leanto=None, floor="board", door="itado", wear="_w2"):
    W, D = 3 * KEN, 2 * KEN
    E = 3.10
    t = R.PITCH[roof]
    YT = E - KETA_H
    YG = E - 0.21
    FLOOR = HUT_FLOOR
    XD = KEN
    S = Shell(name or "jp_hut_west", W, D, [1], "poor hut, west / mountain type (DW30), gable, board walls", wear)
    B = S.B
    ov = 0.90 if roof == "thatch" else None
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, ov=ov, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    raised = floor != "earth"
    lv_room = FLOOR if raised else DOMA
    bw_ = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    zones_front = [(0.0, XD, DOMA), (XD, W, lv_room)] if raised else [(0.0, W, DOMA)]
    feats = [(0.0, KEN, DOMA, DOMA + 2.0, "door" if door == "itado" else "open")]
    S.wall_line("front", zones_front, YT, feats, nodes_extra=(2.0 * KEN,), **bw_)
    if door == "itado":
        S.door(big_leaf("_plain"), "front", 0.0, DOMA, "Door (itado)", "front")
    else:
        B.put(openings.part_mushiro("_rolled"), S.F["front"], 0.0, DOMA, what="jp_p_open_mushiro _rolled (open door)")
        S.portals.append(("mushiro doorway", (A_ - 0.05, KEN - A_ + 0.05, DOMA - 0.1, DOMA + 2.1, -0.25, 0.25)))
        S.passages.append((KEN / 2, 0.0, DOMA))
    zones_back = [(0.0, W - XD, lv_room), (W - XD, W, DOMA)] if raised else [(0.0, W, DOMA)]
    S.wall_line("back", zones_back, YT, [(0.5 * KEN, 1.0 * KEN, lv_room + 0.90, lv_room + 1.65, "window")], **bw_)
    S.window(openings.part_window_slide("_board"), "back", 0.5 * KEN, lv_room, "Window (back)")
    for side in ("left", "right"):
        zl = [(0.0, D, DOMA if side == "left" else lv_room)]
        S.wall_line(side, zl, YG, (), **bw_)
        S.gable(side, D, t, E, "_board", thatch=(roof == "thatch"))
    rects = _hut_floor(S, floor, XD, W, D, FLOOR, K=K)
    _kamado(S, "doma", 0.45, -D + 0.45 if raised else -D + 0.55, 0.0, size=(0.60, 0.60))
    if leanto:
        _gable_leanto(S, leanto, "ishioki" if roof == "ishioki" else "itabuki", E, t)
    S.place_windows()
    doors = [S.dn["front"]] if "front" in S.dn else []
    S.room("doma", "doma", "earth", DOMA, rects["doma"], doors, "doma")
    if raised:
        S.room("living", "living", "boards" if floor == "board" else "bamboo slats", FLOOR, rects["living"], [],
               "living floor with the irori, open to the doma")
    H, info = S.finish({"params": {"kind": "hut_west", "roof": roof, "leanto": leanto, "floor": floor, "door": door},
                        "levels": {"doma": DOMA, "floor": FLOOR, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


def shed(name=None, size="s", roof="itabuki", open=False, leanto=None, wear="_w2"):
    W, D = (3 * KEN, 2 * KEN) if size == "s" else (4 * KEN, 3 * KEN)
    E = 3.10
    t = R.PITCH[roof]
    YT = E - KETA_H
    YG = E - 0.21
    S = Shell(name or "jp_shed", W, D, [1, 2], "shed / barn (DW24)", wear)
    B = S.B
    ov = 0.90 if roof == "thatch" else None
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, ov=ov, soot=False, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw_ = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    if open:
        # the front long side open on its posts (a head beam at door height stiffens it)
        for k in range(int(round(W / KEN)) + 1):
            S.post(round(k * KEN, 4), 0.0, YT)
        s = B.P("open_front_beam")
        s.add(box(-0.06, W + 0.06, YT - 0.40, YT - 0.25, -0.06, 0.06, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="nuki"))
        H_ = s
        B.merge(H_)
    else:
        S.wall_line("front", [(0.0, W, DOMA)], YT, [(KEN, 2 * KEN, DOMA, DOMA + 2.0, "door")], **bw_)
        S.door(big_leaf("_plain"), "front", KEN, DOMA, "Door (itado)", "front")
    S.wall_line("back", [(0.0, W, DOMA)], YT, (), **bw_)
    for side in ("left", "right"):
        S.wall_line(side, [(0.0, D, DOMA)], YG, (), **bw_)
        S.gable(side, D, t, E, "_board", thatch=(roof == "thatch"))
    B.interior = True
    B.merge(FL.doma("floor", -0.06 if open else 0.0, W + (0.06 if open else 0.0), -D, 0.3 if open else 0.0,
                    road=(A_, W - A_, -D + A_, -0.15 if open else -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    if leanto:
        _gable_leanto(S, leanto, "ishioki" if roof == "ishioki" else "itabuki", E, t)
    S.place_windows()
    doors = [S.dn["front"]] if "front" in S.dn else []
    S.room("floor", "storage" if not open else "workshop", "earth", DOMA,
           _r(A_, W - A_, -D + A_, -0.15 if open else -A_), doors,
           "shed floor" + (" (open front)" if open else ""), enclosed=not open)
    H, info = S.finish({"params": {"kind": "shed", "size": size, "roof": roof, "open": open, "leanto": leanto},
                        "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


BUILDERS = {"kanto": kanto, "kinai": kinai, "hut_east": hut_east, "hut_west": hut_west, "shed": shed}


def build(kind, **params):
    if kind not in BUILDERS:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return BUILDERS[kind](**params)


def budget_class(kind, **params):
    """PLAYBOOK §12 class: farmhouses 'large', huts and sheds 'standard'."""
    return "large" if kind in ("kanto", "kinai") else "standard"


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front). Returns (M, floors, rooms,
    info); floors / rooms / portals / passages / fittings in model coordinates, info['posts'] in the kit frame."""
    H, info = build(kind, name=name, **params)
    cx, cz = info["W"] / 2, -info["D"] / 2
    M = H.transformed(0.0, (-cx, 0.0, -cz))
    M.meta = dict(H.meta)

    def mr(r):
        return (r[0] - cx, r[1] - cx, r[2] - cz, r[3] - cz)
    floors = [dict(f, rect=mr(f["rect"]), obstacles=[mr(o) for o in f["obstacles"]]) for f in info["floors"]]
    rooms = [dict(r, rect_model=[round(v, 3) for v in mr(r["rect_kit"])]) for r in info["rooms"]]
    fits = []
    for f in info["fittings"]:
        g = dict(f)
        if "rect" in g:
            g["rect"] = [round(v, 3) for v in mr(g["rect"])]
        if "centre" in g:
            g["centre"] = [round(g["centre"][0] - cx, 3), round(g["centre"][1] - cz, 3)]
        if "hook" in g:
            g["hook"] = [round(g["hook"][0] - cx, 3), g["hook"][1], round(g["hook"][2] - cz, 3)]
        fits.append(g)
    info = dict(info, centre=(cx, cz), fittings_model=fits,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[(x - cx, z - cz, y) for (x, z, y) in info["passages"]])
    return M, floors, rooms, info
