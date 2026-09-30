"""The decorator (B4 pilot, 2026-09-30): furnish a building with proxied props, dress its yard, generate its loot
points from the floors AND the props' surfaces, and check the result.

Binding rules (research/catalogue/G1_DECISIONS.md A2, research/interior/BUILD_LIST.md 'Engine notes' / 'Checks'):
  - 5-7 props per room; at least one raised loot surface per room
  - a 1.00 m clear band from every door to every other door and to the room centre (walled rooms)
  - no collision prop within 0.4 m of a door's clear opening; door sweeps, D1 clear width and C10 reach still hold
    with the furniture in
  - collision furniture covers at most 25 % of a living room's floor (40 % of storage)
  - loot lies OUT: floor points kept 0.4 m clear of every collision footprint, raised points on the props' sidecar
    surfaces (loot_surfaces), nothing above 1.40 m over the room floor
  - props are PROXIES in the LODs vanilla uses (Q5): collision props in Resolution 1 + Geometry + View + Fire, flat
    and hanging props in Resolution 1 only (jpparts/proxies.py)

Props come from the B3a / B3b / L1 sidecars (src/JP/furniture/*/*.prop.json, src/JP/site/*/*.prop.json); their
collision components are read from the MLOD masters (spikes/B3a/out, spikes/B3b/out; an L1 sidecar names its own
master, spikes/L1/out; rebuild with the B3a / B3b build.py or spikes/L1/build_l1.py).

Where a prop goes (L1, 2026-09-30): every catalogue entry has a `mount`: wall | post | beam | doorway | surface |
floor | kamado (sidecar 'mount'; B3a / B3b props without one get it from their anchor: 'wall' -> wall, 'hang' ->
beam, else floor). Place wall / post items with on_wall(), beam items with on_beam(), doorway items with in_doorway()
and small things on another prop's loot surface with on_surface(); floor items with item() as before. The helpers set
the flags the checks read (on_floor, hung, host) and do not count visual-only life items against the 5-7 props of a
room (they hang on walls and beams or sit on surfaces: LIFE_LAYER.md "the rule that makes it fit"). When any such
item is placed, check_all adds D15 (surface items rest on their host's surface) and D16 (hanging items keep 2.00 m
head room over the floor unless placed over a hearth / corner / furniture / doorway: it["over"]).

Outdoor life layer (L2, 2026-09-30): src/JP/site/yard_life and street_life sidecars carry mount yard | street | eaves |
road | shore | field (bench dressing: 'surface', on_surface on a B3b bench). Place them with on_site() (a site item for
D.place_site) and hung eaves pieces with under_eaves(); by_mount("shore") etc. lists them. No new checks.

An item is a dict made by item(): {name (p3d basename), room, x, z, y, yaw, info (the catalogue entry), why, seat}.
Frames: the building MODEL frame (x, y up, z = street front); yaw clockwise from +z seen from above (proxies.frame).
"""
import glob
import json
import math
import os

from . import core, mlod, proxies as PX, checks as C, raycheck as RC

DEV = core.DEV
SOURCES = (("furniture", os.path.join("src", "JP", "furniture"), os.path.join("spikes", "B3a", "out")),
           ("site", os.path.join("src", "JP", "site"), os.path.join("spikes", "B3b", "out")))
BAND = 1.00             # clear band width (G1 A2-4)
DOOR_ZONE = 0.40        # no collision prop this close to a door's clear opening
FLOOR_CLEAR = 0.40      # floor loot keeps this far from collision footprints (PLAYBOOK §10.4)
MAX_LOOT_Y = 1.40       # vanilla shelf maximum above the floor
COVER = {"storage": 0.40}
COVER_DEFAULT = 0.25
_CAT = None
_COMPS = {}


# ------------------------------------------------------------------------------------------------ catalogue
def catalog():
    """{p3d basename: entry} for every B3a / B3b model (sidecar data + the MLOD master path)."""
    global _CAT
    if _CAT is not None:
        return _CAT
    cat = {}
    for area, src, out in SOURCES:
        for p in sorted(glob.glob(os.path.join(DEV, src, "*", "*.prop.json"))):
            folder = os.path.basename(os.path.dirname(p))
            with open(p, "rb") as f:
                d = json.loads(f.read().decode("utf-8"))
            for m in d["models"]:
                name = os.path.basename(m["p3d"])[:-4]
                coll = m.get("collision")
                if isinstance(coll, list):
                    geo, view = "geo" in coll, "view" in coll
                else:
                    geo = view = bool(coll)
                anchor = m.get("anchor", "floor")
                mount = m.get("mount") or {"wall": "wall", "hang": "beam"}.get(anchor, "floor")
                master = os.path.join(DEV, m["master"]) if m.get("master") else os.path.join(DEV, out, folder,
                                                                                            name + ".p3d")
                cat[name] = dict(name=name, area=area, folder=folder, p3d=m["p3d"], cls=m.get("class"),
                                 anchor=anchor, bbox=m["bbox"], footprint=m.get("footprint_xz"),
                                 geo=geo, view=view, roadway=bool(m.get("roadway")), loot=m.get("loot_surfaces") or [],
                                 master=master, hang_y=m.get("hang_y"),
                                 wall_gap=m.get("wall_gap"), state=m.get("state"), well=bool(m.get("well")),
                                 mount=mount, hang_len=m.get("hang_len"), seat_y=m.get("seat_y"), tiers=m.get("tiers"))
    _CAT = cat
    return cat


def item(name, room, x, z, yaw=0.0, y=None, why="", seat=None, count=True):
    """One placement. y None = the room floor (resolved by Decor.place). seat: a model-frame box (x0,x1,y0,y1,z0,z1)
    inside which touching the building's own Geometry is intended (a pot seated in the kamado rim)."""
    info = catalog().get(name)
    if info is None:
        raise KeyError("no prop %r in the B3a / B3b sidecars" % name)
    return {"name": name, "room": room, "x": float(x), "z": float(z), "y": y, "yaw": float(yaw), "info": info,
            "why": why, "seat": seat, "count": count}


def by_mount(mount, area=None):
    """Catalogue names that mount on a wall / post / beam / doorway / surface / floor / kamado."""
    return sorted(n for n, e in catalog().items() if e["mount"] == mount and (area is None or e["area"] == area))


def _mount_ok(name, allowed):
    m = catalog()[name]["mount"]
    if m not in allowed:
        raise ValueError("%s mounts on %r, not %s" % (name, m, "/".join(allowed)))


def on_wall(name, room, x, z, yaw, floor_y=None, why="", count=None):
    """A wall or post item: (x, z) = the point on the wall / post face (the prop's z = 0 plane), yaw so the prop's +z
    points into the room. Its heights are built in, so y = the room floor (resolved by Decor.place when None).
    Visual-only items do not count against the room's props (count=None)."""
    _mount_ok(name, ("wall", "post"))
    it = item(name, room, x, z, yaw, y=floor_y, why=why)
    it["count"] = bool(catalog()[name]["geo"]) if count is None else count
    it["mounted"] = catalog()[name]["mount"]
    return it


def on_beam(name, room, x, z, yaw, beam_y, why="", over=None, count=False):
    """A beam item: (x, beam_y, z) = the beam (or loft joist) underside where it hangs. over: what it hangs over when
    it drops below the 2.00 m head-room line ('hearth', 'corner', 'furniture', ...): D16 then lets it pass."""
    _mount_ok(name, ("beam",))
    it = item(name, room, x, z, yaw, y=beam_y, why=why, count=count)
    it.update(on_floor=False, hung=True, mounted="beam", over=over)
    return it


def in_doorway(name, room, x, z, yaw, head_y, why=""):
    """A doorway item (inner noren): origin at the door head underside, centred in the opening, in its plane."""
    _mount_ok(name, ("doorway",))
    it = item(name, room, x, z, yaw, y=head_y, why=why, count=False)
    it.update(on_floor=False, hung=True, mounted="doorway", over="doorway")
    return it


def on_surface(name, host, surface=None, dx=0.0, dz=0.0, yaw=0.0, why="", count=False):
    """A small item on another placed prop's loot surface (a shelf board, chest lid, desk top): (dx, dz) in the
    host's frame from the surface's centre; yaw relative to the host. The surface keeps its loot points: leave them
    room (the checks do not test that)."""
    _mount_ok(name, ("surface", "floor"))
    ss = host["info"]["loot"]
    if not ss:
        raise ValueError("%s has no loot surface to put %s on" % (host["name"], name))
    s = next((q for q in ss if q["name"] == surface), None) if surface else ss[0]
    if s is None:
        raise KeyError("%s has no surface %r" % (host["name"], surface))
    x0, z0, x1, z1 = s["rect"]
    local = ((x0 + x1) / 2 + dx, s["y"], (z0 + z1) / 2 + dz)
    m = to_model(host, local)
    it = item(name, host["room"], m[0], m[2], host["yaw"] + yaw, y=m[1], why=why, count=count)
    it.update(on_floor=False, mounted="surface", host=host, surface=s["name"], local=local)
    return it


# ------------------------------------------------------------------------------------------------ outdoor (L2)
# L2 (2026-09-30): the outdoor life layer (src/JP/site/yard_life, street_life) carries a sidecar mount: yard | street |
# eaves | road | shore | field (and 'surface' for the bench dressing, placed with on_surface on a B3b bench). They are
# separate map objects (D.place_site), not proxies; B3b's own site props keep their anchor-derived mounts.
OUTDOOR_MOUNTS = ("yard", "street", "eaves", "road", "shore", "field")


def on_site(name, x, z, yaw=0.0, setting=None, y=None, why=""):
    """An outdoor life-layer object as a site item (base centre on the ground at (x, z); yaw so its +z faces the
    street / the viewer). setting: the place it goes (one of OUTDOOR_MOUNTS); it must match the sidecar mount, except
    that a 'yard' or 'street' object may go in either (they are interchangeable dressing)."""
    info = catalog().get(name)
    if info is None:
        raise KeyError("no prop %r in the sidecars" % name)
    m = info["mount"]
    if m not in OUTDOOR_MOUNTS:
        raise ValueError("%s mounts on %r (not an outdoor life-layer mount)" % (name, m))
    if setting and setting != m and not {setting, m} <= {"yard", "street"}:
        raise ValueError("%s is a %r object, not %r" % (name, m, setting))
    it = item(name, setting or m, x, z, yaw, y=y, why=why, count=False)
    it["mounted"] = m
    return it


def under_eaves(name, x, z, yaw, eave_y, why=""):
    """An eaves piece (persimmon curtain, bird cage, sandals for sale): (x, z) = the point on the facade (the prop's
    z = 0 plane), yaw so its +z faces the street, eave_y = the eave / bracket underside above the ground there. The
    prop is built for an eave at its sidecar hang_y, so it is lifted by eave_y - hang_y."""
    info = catalog().get(name)
    if info is None or info["mount"] != "eaves":
        raise ValueError("%s is not an eaves piece" % name)
    if not info.get("hang_y"):
        raise ValueError("%s stands on the veranda (no hang_y): on_site(..., y=the veranda floor)" % name)
    return on_site(name, x, z, yaw, "eaves", y=eave_y - info["hang_y"], why=why)


def lods_for(it):
    return PX.LODS_COLLISION if (it["info"]["geo"] or it["info"]["view"]) else PX.LODS_VISUAL


def proxies(items):
    return [{"p3d": it["info"]["p3d"], "pos": (it["x"], it["y"], it["z"]), "yaw": it["yaw"], "lods": lods_for(it)}
            for it in items]


# ------------------------------------------------------------------------------------------------ geometry helpers
def to_model(it, local):
    return PX.to_model(local, (it["x"], it["y"], it["z"]), it["yaw"])


def footprint(it):
    """Collision footprint polygon [(x, z)] in the model frame (None for flat / visual-only props)."""
    inf = it["info"]
    if not inf["geo"]:
        return None
    fp = inf["footprint"]
    if fp:
        x0, z0, x1, z1 = fp
    else:
        b = inf["bbox"]
        x0, x1, z0, z1 = b[0], b[1], b[4], b[5]
    out = []
    for (x, z) in ((x0, z0), (x1, z0), (x1, z1), (x0, z1)):
        p = to_model(it, (x, 0.0, z))
        out.append((p[0], p[2]))
    return out


def blocks(it):
    """Does the prop block walking (collision, not a walk-on slab like the laid futon)?"""
    return it["info"]["geo"] and not it["info"]["roadway"]


def aabb(poly):
    xs, zs = [p[0] for p in poly], [p[1] for p in poly]
    return (min(xs), max(xs), min(zs), max(zs))


def poly_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, z0 = poly[i]
        x1, z1 = poly[(i + 1) % len(poly)]
        a += x0 * z1 - x1 * z0
    return abs(a) / 2


def clip_area(poly, rect):
    """Area of a convex polygon inside an axis rect (Sutherland-Hodgman)."""
    x0, x1, z0, z1 = rect
    pts = list(poly)
    for axis, val, keep_ge in ((0, x0, True), (0, x1, False), (1, z0, True), (1, z1, False)):
        out = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            ina = (a[axis] >= val) if keep_ge else (a[axis] <= val)
            inb = (b[axis] >= val) if keep_ge else (b[axis] <= val)
            if ina:
                out.append(a)
            if ina != inb:
                t = (val - a[axis]) / (b[axis] - a[axis])
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        pts = out
        if not pts:
            return 0.0
    return poly_area(pts)


def point_poly_dist(p, poly):
    """Distance from a point to a convex polygon (0 inside)."""
    inside = True
    n = len(poly)
    sgn = 0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        c = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        s = 1 if c > 0 else (-1 if c < 0 else 0)
        if s:
            if sgn == 0:
                sgn = s
            elif s != sgn:
                inside = False
                break
    if inside:
        return 0.0
    best = 1e9
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dz = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dz * dz or 1e-12
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / L2))
        best = min(best, math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dz))
    return best


def polys_intersect(a, b):
    """SAT for two convex polygons (touching counts as apart)."""
    for poly in (a, b):
        for i in range(len(poly)):
            p, q = poly[i], poly[(i + 1) % len(poly)]
            nx, nz = -(q[1] - p[1]), q[0] - p[0]
            pa = [nx * v[0] + nz * v[1] for v in a]
            pb = [nx * v[0] + nz * v[1] for v in b]
            if max(pa) <= min(pb) + 1e-9 or max(pb) <= min(pa) + 1e-9:
                return False
    return True


def rect_poly(r):
    x0, x1, z0, z1 = r
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


# ------------------------------------------------------------------------------------------------ prop components
def _master_comps(name, lod_name):
    k = (name, lod_name)
    if k not in _COMPS:
        inf = catalog()[name]
        comps = []
        if os.path.isfile(inf["master"]):
            L = {mlod.lod_name(l.resolution): l for l in mlod.read_mlod(inf["master"])}
            if lod_name in L:
                comps = C.components(L[lod_name])
        _COMPS[k] = comps
    return _COMPS[k]


def comps(it, lod_name="Geometry"):
    """The prop's convex components (Geometry / View Geometry) moved into the model frame."""
    r, _, f = PX.frame(it["yaw"])
    t = (it["x"], it["y"], it["z"])

    def R(v):
        return (r[0] * v[0] + f[0] * v[2], v[1], r[2] * v[0] + f[2] * v[2])
    out = []
    for k, c in enumerate(_master_comps(it["name"], lod_name)):
        planes = []
        for n, d in c["planes"]:
            n2 = R(n)
            planes.append((n2, d + core.dot(n2, t)))
        pts = [core.add(R(p), t) for p in c["pts"]]
        xs, ys, zs = [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts]
        out.append(dict(name="%s#%d" % (it["name"], k), planes=planes, bbox=(min(xs), max(xs), min(ys), max(ys),
                                                                               min(zs), max(zs)),
                        door=None, pts=pts, prop=it["name"]))
    return out


# ------------------------------------------------------------------------------------------------ the decorator
class Decor:
    """Holds the rooms (model frame: [{name, tag, rect_model, level_m, doors}]) and the placed items."""

    def __init__(self, rooms, floors):
        self.rooms = {r["name"]: r for r in rooms}
        self.floors = {f["name"]: f for f in floors}
        self.items = []          # inside the building (proxies)
        self.site = []           # outside (separate map objects)

    def place(self, it):
        if it["y"] is None:
            it["y"] = self.floors[it["room"]]["y"] if it["room"] in self.floors else 0.0
        self.items.append(it)
        return it

    def place_site(self, it):
        if it["y"] is None:
            it["y"] = 0.0
        self.site.append(it)
        return it

    def by_room(self):
        out = {}
        for it in self.items:
            out.setdefault(it["room"], []).append(it)
        return out

    # -------------------------------------------------------------- loot
    def raised_points(self):
        pts = []
        for it in self.items:
            fy = self.floors[it["room"]]["y"] if it["room"] in self.floors else it["y"]
            for s in it["info"]["loot"]:
                for lp in s["points"]:
                    m = to_model(it, lp)
                    above = m[1] - fy
                    if above > MAX_LOOT_Y + 1e-6:
                        continue
                    rng = float(s.get("range", 0.2))
                    shelf = s.get("kind", "shelf") == "shelf" and above > 0.05
                    pts.append({"model": m, "range": rng, "height": min(2.0, 2.5 * rng), "floor": it["room"],
                                "container": "lootshelves" if shelf else "lootFloor",
                                "tag": "shelves" if shelf else "floor", "prop": it["name"], "surface": s["name"],
                                "above_floor": round(above, 3)})
        return pts

    def floor_obstacles(self, room):
        """Collision footprints (as boxes) of the props in a room: the loot generator keeps 0.4 m from them."""
        return [aabb(footprint(it)) for it in self.items if it["room"] == room and blocks(it)]

    def loot_points(self, floor_points_fn):
        """Floor points (the building's own generator, with the prop footprints as extra obstacles) first, then the
        raised points; each {model, range, height, floor, container, tag}."""
        pts = []
        for name, f in self.floors.items():
            f2 = dict(f, obstacles=list(f["obstacles"]) + self.floor_obstacles(name))
            for p in floor_points_fn(f2):
                p = dict(p, floor=name, container="lootFloor", tag="floor")
                pts.append(p)
        return pts + self.raised_points()


# ------------------------------------------------------------------------------------------------ checks
def door_opening(d, gcomps):
    """(u axis, (lo, hi) clear interval along it, wall line coordinate, wall normal axis) of a door, from its closed
    and open leaves: the closed leaves' span minus what the open leaves still cover (the stub)."""
    bones = {a["bone"] for a in d.anims}
    leaves = [c for c in gcomps if c.get("door") in bones]
    if not leaves:
        return None
    a0 = d.anims[0]
    lb = [c["bbox"] for c in leaves]
    bx = (min(b[0] for b in lb), max(b[1] for b in lb), min(b[4] for b in lb), max(b[5] for b in lb))
    along_x = (bx[1] - bx[0]) >= (bx[3] - bx[2])
    lo, hi = (bx[0], bx[1]) if along_x else (bx[2], bx[3])
    wall = (bx[2] + bx[3]) / 2 if along_x else (bx[0] + bx[1]) / 2
    if a0["type"] == "translation":
        op = RC.open_state(leaves, [d], 1.0)
        ob = [c["bbox"] for c in op]
        olo = min(b[0] for b in ob) if along_x else min(b[4] for b in ob)
        ohi = max(b[1] for b in ob) if along_x else max(b[5] for b in ob)
        # the part of [lo, hi] the open leaves do not cover (stub on one side)
        if ohi > hi - 1e-3 and olo > lo:
            hi = max(lo, olo)
        elif olo < lo + 1e-3 and ohi < hi:
            lo = min(hi, ohi)
    return along_x, (lo, hi), wall


def band_check(room, items, openings, fixed=(), step=0.05):
    """Is there a >= 1.00 m wide walking band from every door of the room to every other door and to the room
    centre? Grid over the room rect; a cell is free when it is >= 0.5 m from the walls (rect edges) and from every
    blocking prop footprint / fixed obstacle. openings: [(label, (x, z) of the opening centre)]. Returns (ok, detail)."""
    x0, x1, z0, z1 = room["rect_model"]
    half = BAND / 2
    polys = [footprint(it) for it in items if blocks(it)] + [rect_poly(r) for r in fixed]
    nx, nz = int((x1 - x0) / step) + 1, int((z1 - z0) / step) + 1

    def free(i, j):
        x, z = x0 + i * step, z0 + j * step
        if min(x - x0, x1 - x, z - z0, z1 - z) < half - 1e-6:
            return False
        return all(point_poly_dist((x, z), p) >= half - 1e-6 for p in polys)
    grid = [[free(i, j) for j in range(nz)] for i in range(nx)]

    def snap(pt, maxd=0.9):
        best = None
        for i in range(nx):
            for j in range(nz):
                if grid[i][j]:
                    d = math.hypot(x0 + i * step - pt[0], z0 + j * step - pt[1])
                    if d <= maxd and (best is None or d < best[0]):
                        best = (d, i, j)
        return best
    targets = [(lbl, p) for lbl, p in openings] + [("centre", ((x0 + x1) / 2, (z0 + z1) / 2))]
    starts = []
    for lbl, p in targets:
        s = snap(p, 0.9 if lbl != "centre" else 0.5)
        if s is None:
            return False, "%s: no free 1.00 m band cell near %s" % (lbl, tuple(round(v, 2) for v in p))
        starts.append((lbl, s))
    # flood fill from the first
    seen = set()
    stack = [(starts[0][1][1], starts[0][1][2])]
    while stack:
        i, j = stack.pop()
        if (i, j) in seen:
            continue
        seen.add((i, j))
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < nx and 0 <= b < nz and grid[a][b] and (a, b) not in seen:
                stack.append((a, b))
    miss = [lbl for lbl, s in starts if (s[1], s[2]) not in seen]
    nfree = sum(1 for i in range(nx) for j in range(nz) if grid[i][j])
    return not miss, ("%s joined by a 1.00 m band (%d free cells)" % (", ".join(l for l, _ in starts), nfree)
                      if not miss else "cut off: %s" % miss)


def dist3(a, b):
    return math.sqrt(sum((a[k] - b[k]) ** 2 for k in range(3)))


def _road_heights(road, x, z):
    hs = []
    for verts, _, tex, _ in road.faces:
        pts = [road.points[v[0]] for v in verts]
        if C._in_poly_xz(pts, x, z):
            n = mlod._face_formula_normal(pts)
            if abs(n[1]) < 1e-9:
                continue
            p0 = pts[0]
            hs.append(p0[1] - (n[0] * (x - p0[0]) + n[2] * (z - p0[2])) / n[1])
    return hs


def check_all(D, M, L, pts, rec, door_fn=None, extra_openings=None, fixed_band=None, count_range=(5, 7),
              site_bounds=None, mlod_lods=None):
    """Every decorator check (the new ones of B4). D: Decor; M: the building Part (model frame; doors, memory);
    L: {lod name: Lod} read back from the MLOD with the proxy triangles stripped; pts: the loot points written to the
    CE; rec(check, ok, detail). door_fn(d, gcomps) -> (ok, msg, clear) = the building's own door sweep / D1 / D2
    check (buildings/machiya_t3_01/verify.door_world), run with the prop components added. extra_openings:
    {room: [(label, (x, z))]} for open passages; fixed_band: {room: [rect]} built-in obstacles the band must go round
    (a kamado); site_bounds: (x0, x1, z0, z1) model-frame box the yard objects must stay inside; mlod_lods: the raw
    MLOD LODs (with proxies) for the proxy-LOD check."""
    rooms = D.rooms
    byr = D.by_room()
    gcomps = C.components(L["Geometry"])
    vcomps = C.components(L["View Geometry"])
    bgeo = [c for c in gcomps if not c["door"]]
    pgeo = {id(it): comps(it, "Geometry") for it in D.items + D.site}
    pview = [c for it in D.items for c in comps(it, "View Geometry")]
    allpgeo = [c for it in D.items for c in pgeo[id(it)]]
    road = L["Roadway"]
    # ---- per room: count, coverage, raised surface, band
    for rn, r in rooms.items():
        if r.get("tag") == "loft":
            continue
        its = byr.get(rn, [])
        n = sum(1 for it in its if it["count"])
        rec("D1 props per room %d-%d: %s" % (count_range[0], count_range[1], rn),
            count_range[0] <= n <= count_range[1], "%d props: %s" % (n, ", ".join(it["name"] for it in its)))
        rect = r["rect_model"]
        area = (rect[1] - rect[0]) * (rect[3] - rect[2])
        cov = sum(clip_area(footprint(it), rect) for it in its if blocks(it))
        lim = COVER.get(r["tag"], COVER_DEFAULT)
        rec("D2 floor coverage <= %d %%: %s" % (lim * 100, rn), cov <= lim * area + 1e-6,
            "%.2f of %.2f m2 = %.1f %% (collision footprints)" % (cov, area, 100 * cov / area))
        raised = [p for p in pts if p.get("floor") == rn and p.get("container") == "lootshelves"]
        rec("D3 at least one raised loot surface: %s" % rn, bool(raised),
            "%d raised points on %s" % (len(raised), ", ".join(sorted({p["prop"] for p in raised}))))
        ops = []
        for dn in r.get("doors", []):
            k = int(dn.replace("DoorsTwin", "")) - 1
            d = M.doors[k]
            if not getattr(d, "passable", True):
                continue
            o = door_opening(d, gcomps)
            if o:
                along_x, (lo, hi), wall = o
                ops.append((dn, ((lo + hi) / 2, wall) if along_x else (wall, (lo + hi) / 2)))
        ops += (extra_openings or {}).get(rn, [])
        ok, det = band_check(r, its, ops, (fixed_band or {}).get(rn, ()))
        rec("D4 1.00 m clear band door-to-door and door-to-centre: %s" % rn, ok, det)
    # ---- doors: clear zone, sweep / D1 with the furniture in, C10 reach with the furniture in
    fa = None
    try:
        from . import buildcheck as BC
        fa = BC.floor_fn(road)
    except Exception:
        pass
    for k, d in enumerate(M.doors, 1):
        label = getattr(d, "label", "")
        if getattr(d, "passable", True):
            o = door_opening(d, gcomps)
            bad = []
            if o:
                along_x, (lo, hi), wall = o
                bones = {a["bone"] for a in d.anims}
                lb = [c["bbox"] for c in gcomps if c.get("door") in bones]
                if along_x:
                    zr = (min(b[4] for b in lb) - DOOR_ZONE, max(b[5] for b in lb) + DOOR_ZONE)
                    zone = rect_poly((lo - DOOR_ZONE, hi + DOOR_ZONE, zr[0], zr[1]))
                else:
                    xr = (min(b[0] for b in lb) - DOOR_ZONE, max(b[1] for b in lb) + DOOR_ZONE)
                    zone = rect_poly((xr[0], xr[1], lo - DOOR_ZONE, hi + DOOR_ZONE))
                # the props of the rooms this door opens into (+ the yard / street objects for an outside door);
                # a zone reaching through a wall into a third room does not count
                drooms = {rn for rn, r in rooms.items() if "DoorsTwin%d" % k in r.get("doors", [])}
                cand = [it for it in D.items if it["room"] in drooms]
                if len(drooms) < 2:
                    cand += D.site + [it for it in D.items if it["room"] not in rooms]
                for it in cand:
                    fp = footprint(it)
                    if fp and blocks(it) and polys_intersect(fp, zone):
                        bad.append(it["name"])
            rec("D5 DoorsTwin%d: no collision prop within 0.4 m of the clear opening" % k, not bad,
                "%s: %s" % (label, "clear" if not bad else "BLOCKED by %s" % bad))
            if door_fn:
                ok, msg, clear = door_fn(d, gcomps + allpgeo + [c for it in D.site for c in pgeo[id(it)]])
                rec("D6 DoorsTwin%d sweep + clear >= 1.00 + head with the furniture in" % k, ok, "%s: %s" % (label, msg))
        for frac, state in ((1.0, "open"), (0.0, "closed")):
            rr = RC.door_reach(d, vcomps + pview, M.memory, floor_at=fa, frac=frac, others=M.doors)
            bad = [s_ for s_, (ok, _) in rr.items() if not ok]
            rec("D7 DoorsTwin%d reachable with the furniture in (%s)" % (k, state), not bad,
                "%s: %s" % (label, "; ".join("%s: %s" % (s_, v[1]) for s_, v in rr.items())))
    # ---- props vs walls, props vs props, base / wall contact
    hits = []
    for it in D.items + D.site:
        seat = it.get("seat")
        for c in pgeo[id(it)]:
            for b in bgeo:
                if seat and all(seat[2 * q] - 0.01 <= b["bbox"][2 * q] and b["bbox"][2 * q + 1] <= seat[2 * q + 1] + 0.01
                                for q in range(3)):
                    continue
                dd = RC.convex_overlap(c, b, 0.01)
                if dd > 0:
                    hits.append((it["name"], b["name"], round(dd, 3)))
    rec("D8 props clear of the building (no Geometry overlap > 1 cm; seated pots excepted)", not hits,
        "%d collision props checked against %d building components" % (sum(1 for it in D.items + D.site if pgeo[id(it)]),
                                                                        len(bgeo)) if not hits else "HITS %s" % hits[:4])
    hits = []
    allits = D.items + D.site
    for i in range(len(allits)):
        for j in range(i + 1, len(allits)):
            for a in pgeo[id(allits[i])]:
                for b in pgeo[id(allits[j])]:
                    dd = RC.convex_overlap(a, b, 0.01)
                    if dd > 0:
                        hits.append((allits[i]["name"], allits[j]["name"], round(dd, 3)))
    rec("D9 props clear of each other (no Geometry overlap > 1 cm)", not hits,
        "%d props pairwise" % len(allits) if not hits else "HITS %s" % hits[:4])
    bad = []
    for it in D.items:
        if it.get("seat") or it.get("hung"):          # seated pots; street cloth / lanterns hung over the doorway
            continue
        hs = _road_heights(road, it["x"], it["z"])
        if it.get("on_floor", True) and not any(abs(h - it["y"]) <= 0.02 for h in hs):
            bad.append((it["name"], "base %.3f, floor %s" % (it["y"], [round(h, 3) for h in hs])))
        if it["info"]["anchor"] == "wall":
            q = to_model(it, (0.0, 1.2, -0.05))
            if not any(RC.inside_depth(b, q) > -0.03 for b in bgeo):
                bad.append((it["name"], "no wall behind its wall plane"))
    rec("D10 C6 bases on the floor (0-2 cm), wall-hung props against a wall", not bad,
        "%d props" % len(D.items) if not bad else "BAD %s" % bad[:4])
    # ---- life-layer items (L1): only when some are placed, so earlier buildings keep their check count
    surf = [it for it in D.items if it.get("mounted") == "surface"]
    if surf:
        bad = []
        for it in surf:
            h = it["host"]
            s = next(q for q in h["info"]["loot"] if q["name"] == it["surface"])
            x0, z0, x1, z1 = s["rect"]
            lx, ly, lz = it["local"]
            if abs(ly - s["y"]) > 0.02 or not (x0 - 0.02 <= lx <= x1 + 0.02 and z0 - 0.02 <= lz <= z1 + 0.02):
                bad.append((it["name"], "off %s/%s" % (h["name"], s["name"])))
        rec("D15 surface items rest on their host's surface (+-2 cm, inside its rect)", not bad,
            "%d items" % len(surf) if not bad else "BAD %s" % bad[:4])
    hung = [it for it in D.items if it.get("mounted") in ("beam", "doorway")]
    if hung:
        bad = []
        for it in hung:
            fy = D.floors[it["room"]]["y"] if it["room"] in D.floors else 0.0
            low = it["y"] - (it["info"].get("hang_len") or 0.0)
            if low - fy < 2.00 - 1e-6 and not it.get("over"):
                bad.append((it["name"], "bottom %.2f over the floor" % (low - fy)))
        rec("D16 hanging items keep 2.00 m head room (or hang over a hearth / corner / furniture / doorway)", not bad,
            "%d items" % len(hung) if not bad else "BAD %s" % bad[:4])
    # ---- loot
    bad = []
    allc = bgeo + allpgeo
    for p in pts:
        x, y, z = p["model"]
        if p.get("container") == "lootFloor" and not p.get("prop"):
            for it in byr.get(p["floor"], []):
                fp = footprint(it)
                if fp and blocks(it) and point_poly_dist((x, z), fp) < FLOOR_CLEAR - 1e-6:
                    bad.append(("floor point near %s" % it["name"], (round(x, 2), round(z, 2))))
        else:
            if p.get("above_floor", 0) > MAX_LOOT_Y + 1e-6:
                bad.append(("above 1.40", p["prop"]))
        q = (x, y + 0.05, z)
        # a raised point may sit inside its OWN prop's collision block (a sink trough, a dropped drawer): by design
        inside = [c["name"] for c in allc if c.get("prop") != p.get("prop") and RC.inside_depth(c, q) > 0.01]
        if inside:
            bad.append(("point inside geometry %s" % inside[:2], (round(x, 2), round(y, 2), round(z, 2))))
    nf = sum(1 for p in pts if p.get("container") == "lootFloor")
    rec("D11 loot: floor points 0.4 m clear of footprints, raised points on prop surfaces <= 1.40 m, none inside "
        "geometry", not bad, "%d points (%d floor, %d raised)" % (len(pts), nf, len(pts) - nf) if not bad
        else "BAD %s" % bad[:4])
    # ---- proxies in the Q5 LODs, read back from the MLOD, at the intended poses
    if mlod_lods:
        LL = {mlod.lod_name(l.resolution): l for l in mlod_lods}
        want, got = {}, {}
        for it in D.items:
            for ln in lods_for(it):
                key = (ln, it["info"]["p3d"].lower().lstrip("\\")[:-4])
                want[key] = want.get(key, 0) + 1
        poses_bad = []
        for ln, lod in LL.items():
            for name, o, up, fw in PX.listed(lod):
                key = (ln, name[len("proxy:"):].lower().lstrip("\\").rsplit(".", 1)[0])
                got[key] = got.get(key, 0) + 1
                if ln == "Resolution 1":
                    m = [it for it in D.items if it["info"]["p3d"].lower().lstrip("\\")[:-4] == key[1] and
                         dist3((it["x"], it["y"], it["z"]), o) < 1e-3]
                    if not m or abs(core.dot(fw, PX.frame(m[0]["yaw"])[2]) - 1.0) > 1e-4 or abs(up[1] - 1.0) > 1e-4:
                        poses_bad.append(key[1])
        wrong_lod = [k for k in got if k[0] not in PX.LODS_COLLISION]
        rec("D12 proxies in the vanilla LODs (Q5: collision props Res 1 + Geometry + View + Fire, flat / hanging "
            "Res 1 only) at the planned poses", want == got and not wrong_lod and not poses_bad,
            "%d proxy records in %s" % (sum(got.values()), sorted({k[0] for k in got})) if want == got and not
            poses_bad and not wrong_lod else "want/got differ %s; poses %s; wrong LOD %s" % (
                sorted(set(want.items()) ^ set(got.items()))[:3], poses_bad[:3], wrong_lod[:3]))
    # ---- yard: inside the bounds, wells reachable (a free standing spot 0.6-1.0 m off the curb)
    if D.site:
        out = []
        if site_bounds:
            for it in D.site:
                fp = footprint(it) or [(it["x"], it["z"])]
                bx = aabb(fp)
                if bx[0] < site_bounds[0] or bx[1] > site_bounds[1] or bx[2] < site_bounds[2] or bx[3] > site_bounds[3]:
                    out.append(it["name"])
        rec("D13 yard / street objects inside the test pad", not out, "%d objects" % len(D.site) if not out
            else "OUTSIDE %s" % out)
        for it in D.site:
            if not it["info"]["well"]:
                continue
            spots = 0
            for a in range(16):
                ang = 2 * math.pi * a / 16
                ok_r = None
                for rr in (0.9, 1.1, 1.3):
                    q = to_model(it, (rr * math.sin(ang), 0.0, rr * math.cos(ang)))
                    col = (q[0] - 0.25, q[0] + 0.25, 0.1, 1.8, q[2] - 0.25, q[2] + 0.25)
                    if not any(C.comp_box_intersect(c, col, 0.0) for c in bgeo + allpgeo +
                               [c for s in D.site for c in pgeo[id(s)]]):
                        ok_r = rr
                        break
                spots += 1 if ok_r else 0
            rec("D14 %s: a player can stand at the curb" % it["name"], spots >= 4,
                "%d of 16 directions have a free 0.5 m standing column 0.9-1.3 m from the well centre" % spots)
