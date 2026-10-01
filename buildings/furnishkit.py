"""Furnished variants of the wave-1 shells (C3, 2026-09-30): the B4 pattern (buildings/machiya_t3_01_shop) for ANY
registry shell. A furnished variant is its own p3d = the base shell's recipe (the SAME registry params, so the shell
geometry is identical) + built-in fittings the shell left a spot for (the kamado, jpparts.fittings) + the props as
proxies in the vanilla LODs (jpparts.decor / proxies) + loot on the floors and the props' surfaces + its street / yard
objects (site(), map objects in C.csv). The dressings (one per type) are in buildings/furnish_sets.py.

  model(name=..., base=<registry key of the bare shell>, dress=<furnish_sets.SETS key>) -> (M, floors, rooms)

Module state after model() (read by the pipeline and buildings/shellcheck.py): POSTS, PASSAGES, PORTALS, STAIRS, INFO,
PASSAGE_LABEL, DOOR_CHECK_OTHERS_OPEN (forwarded from the base recipe); D (the Decor), EXTRA_OPENINGS, FIXED_BAND
(for decor.check_all), SITE_BOUNDS. proxies() / loot_points(floors) / site() as the machiya shop.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
sys.path.insert(0, os.path.join(DEV, "spikes", "B_building", "kit"))
from jpparts import decor as DC, fittings as FT  # noqa: E402
from jpkit import loot as bloot  # noqa: E402

POSTS, PASSAGES, PORTALS, STAIRS = [], [], [], []
INFO = {}
PASSAGE_LABEL = "C7 open passage clear >= 1.00 + head >= 2.00"
DOOR_CHECK_OTHERS_OPEN = False
FRAME_NOTE = "model: the base shell's frame (origin = footprint / lot centre at grade, +z = front); furnished by C3"
D = None
EXTRA_OPENINGS, FIXED_BAND = {}, {}
SITE_BOUNDS = (-60.0, 60.0, -60.0, 60.0)
BASE = {}
WALL_INSET = 0.005        # a wall-anchored prop's plane 5 mm inside the room rect (the post face): its Roadway lookup
#                           and the 'wall behind' test (decor D10) both land on the right side of the edge


class Ctx:
    """What a dressing function gets: the base model, its rooms and floors (model frame), the Decor, and helpers that
    place props against walls, on beams, on surfaces and outside."""

    def __init__(self, M, floors, rooms, info, key, tier):
        self.M, self.info, self.key, self.tier = M, info, key, tier
        self.floor = {f["name"]: f for f in floors}
        self.room = {r["name"]: r for r in rooms}
        self.D = DC.Decor(rooms, floors)
        self.extra, self.fixed = {}, {}
        self.kam = {}
        self.info_passage = tuple(PASSAGES[0][:2]) if PASSAGES else None     # townhouse toriniwa -> kitchen
        self.stairs = list(STAIRS)

    # ------------------------------------------------ geometry
    def R(self, room):
        return tuple(self.room[room]["rect_model"])

    def y(self, room):
        return self.room[room]["level_m"]

    def fit(self, room, kind):
        return [f for f in self.room[room].get("fittings", []) if f["kind"] == kind]

    # ------------------------------------------------ placement helpers
    def _wall_pose(self, room, side, at, back, off):
        x0, x1, z0, z1 = self.R(room)
        if side == "zmin":
            return at, z0 + back + off, 0.0
        if side == "zmax":
            return at, z1 - back - off, 180.0
        if side == "xmin":
            return x0 + back + off, at, 90.0
        if side == "xmax":
            return x1 - back - off, at, 270.0
        raise ValueError(side)

    def wall(self, room, side, at, name, gap=0.03, off=0.0, y=None, why="", count=True, yaw_extra=0.0):
        """A floor prop with its back against the room's `side` wall ('xmin' | 'xmax' | 'zmin' | 'zmax'), centred at
        `at` along the wall, facing into the room; a wall-anchored prop (shelf, sink) with its plane on the wall."""
        inf = DC.catalog()[name]
        if inf["anchor"] == "wall":
            back, gap = WALL_INSET, 0.0
        else:
            back = -inf["bbox"][4]
        x, z, yaw = self._wall_pose(room, side, at, back + gap, off)
        it = DC.item(name, room, x, z, (yaw + yaw_extra) % 360.0, y=y, why=why, count=count)
        if y is not None and inf["anchor"] == "wall":
            it["on_floor"] = False
        return self.D.place(it)

    def free(self, room, name, x, z, yaw=0.0, y=None, why="", count=True):
        return self.D.place(DC.item(name, room, x, z, yaw, y=y, why=why, count=count))

    def onwall(self, room, side, at, name, why="", count=None):
        """A wall / post life item (pegs, calendar, charms, kamidana): its plane on the wall, facing into the room."""
        x, z, yaw = self._wall_pose(room, side, at, WALL_INSET, 0.0)
        return self.D.place(DC.on_wall(name, room, x, z, yaw, why=why, count=count))

    def hang(self, room, name, x, z, beam_y, yaw=0.0, over=None, why=""):
        return self.D.place(DC.on_beam(name, room, x, z, yaw, beam_y, why=why, over=over))

    def doorway(self, room, name, x, z, yaw, head_y, why=""):
        return self.D.place(DC.in_doorway(name, room, x, z, yaw, head_y, why=why))

    def surf(self, host, name, surface=None, dx=0.0, dz=0.0, yaw=0.0, why=""):
        return self.D.place(DC.on_surface(name, host, surface, dx, dz, yaw, why=why))

    # ------------------------------------------------ outside (separate map objects, model frame)
    def site(self, name, x, z, yaw=0.0, y=None, why="", setting=None):
        m = DC.catalog()[name]["mount"]
        if m in DC.OUTDOOR_MOUNTS:
            it = DC.on_site(name, x, z, yaw, setting=setting, y=y, why=why)
        else:
            it = DC.item(name, setting or "yard", x, z, yaw, y=y, why=why, count=False)
        return self.D.place_site(it)

    def eaves(self, name, x, z, yaw, eave_y, why=""):
        return self.D.place_site(DC.under_eaves(name, x, z, yaw, eave_y, why=why))

    def front(self, name, x, z, y, yaw=0.0, why=""):
        """Shop-front dressing hung on the building as a Resolution-1 proxy (G1 A3-8), like the machiya's noren."""
        it = self.D.place(DC.item(name, "street", x, z, yaw, y=y, why=why, count=False))
        it["hung"] = True
        return it

    # ------------------------------------------------ fittings
    def kamado(self, room, rect, mouth, n=2, soot_wall=None):
        """jp_p_fit_kamado merged into the variant on its spot; its rect (+0.25) keeps floor loot and the band away."""
        k = FT.kamado(self.M, rect, self.y(room), mouth=mouth, n=n, tier=3 if self.tier >= 3 else 2,
                      soot_wall=soot_wall)
        x0, x1, z0, z1 = rect
        ob = (x0 - 0.25, x1 + 0.25, z0 - 0.25, z1 + 0.25)
        self.floor[room]["obstacles"].append(ob)
        self.fixed.setdefault(room, []).append(rect)
        self.kam[room] = k
        return k

    def pot(self, room, name, k, yaw=0.0, why=""):
        """A pot / steamer seated in the kamado's rim k (seat_y from the sidecar)."""
        kd = self.kam[room]
        x, z = kd["rims"][k]
        sy = DC.catalog()[name]["seat_y"] or 0.168
        return self.D.place(DC.item(name, room, x, z, yaw, y=kd["rim_top"] - sy, seat=kd["seat"], why=why))

    def passage(self, rooms, x, z, label="passage"):
        for r in rooms:
            self.extra.setdefault(r, []).append((label, (x, z)))

    def band_block(self, room, rect):
        self.fixed.setdefault(room, []).append(rect)


def _base_module(b):
    d = os.path.join(HERE, b["dir"])
    if d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module(b["module"])


def model(name=None, base=None, dress=None, **kw):
    global D, DOOR_CHECK_OTHERS_OPEN
    import registry
    import furnish_sets
    b = registry.get(base)
    bm = _base_module(b)
    spec = furnish_sets.SETS[dress]
    params = dict(b["params"])
    params.update(spec.get("shell", {}))      # S1: a dressing may ask the shell for an option (the shop board strip)
    M, floors, rooms = bm.model(name=name, **params)
    POSTS[:] = list(getattr(bm, "POSTS", []))
    PASSAGES[:] = list(getattr(bm, "PASSAGES", []))
    PORTALS[:] = list(getattr(bm, "PORTALS", []))
    STAIRS[:] = list(getattr(bm, "STAIRS", []))
    INFO.clear()
    INFO.update(getattr(bm, "INFO", {}))
    DOOR_CHECK_OTHERS_OPEN = bool(getattr(bm, "DOOR_CHECK_OTHERS_OPEN", False))
    globals()["PASSAGE_LABEL"] = getattr(bm, "PASSAGE_LABEL", PASSAGE_LABEL)
    BASE.clear()
    BASE.update(key=base, cls=b["class"])
    ctx = Ctx(M, floors, rooms, INFO, base, spec["tier"])
    spec["fn"](ctx)
    D = ctx.D
    # walk-on props with collision (laid bedding, straw beds, low slabs) do not block walking, but floor loot must not
    # spawn under them (decor D11 'inside geometry'): their footprints join the floor's loot obstacles
    for it in D.items:
        if it["info"]["geo"] and not DC.blocks(it) and it["room"] in ctx.floor:
            bx = DC.aabb(DC.footprint(it))
            ctx.floor[it["room"]]["obstacles"].append((bx[0] - 0.05, bx[1] + 0.05, bx[2] - 0.05, bx[3] + 0.05))
    EXTRA_OPENINGS.clear()
    EXTRA_OPENINGS.update(ctx.extra)
    FIXED_BAND.clear()
    FIXED_BAND.update(ctx.fixed)
    return M, floors, rooms


def proxies():
    return DC.proxies(D.items)


def loot_points(floors):
    return D.loot_points(bloot.floor_points)


def site():
    return [{"p3d": s["info"]["p3d"], "x": round(s["x"], 4), "z": round(s["z"], 4), "yaw": s["yaw"],
             "y": round(s["y"], 4), "why": s["why"]} for s in D.site]
