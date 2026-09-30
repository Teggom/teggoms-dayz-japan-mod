"""Building assembly on wall-line frames (B0, promoted from buildings/machiya_t3_01, where these were private helpers).

A building is assembled in its KIT FRAME (x along the street, z 0 = street wall line with +z towards the street, y 0 =
grade) from sub-parts placed on WALL-LINE FRAMES: fr = (yaw, origin), where the sub-part's +x runs along the wall and
its +z faces 'out' (core.rot_y convention). Examples (a W x D house): front (0, (0, 0, 0)); back (180, (W, 0, -D));
left gable (90, (0, 0, -D)); right gable (-90, (W, 0, 0)).

    B = Builder(H)                 # H = the building Part
    B.posts_on(fr, [0, KEN], y0, y1)
    B.wall(fr, "front_b1", "shinkabe", 0, KEN, y0, y1, openings_=[...])
    B.place_door(openings.part_itado("_twin"), fr, 0, y0, label="Entrance")
    B.interior = True              # what is merged now is interior-only (dropped from Resolution 3)

B.posts collects every post node (x, z, y0, y1) for the C3 grid check; B.log what went where.
"""
import copy

from .core import Part, box, POST, rot_y
from . import walls, frame, found, trim


def to_world(fr, lx, lz=0.0):
    """Kit-frame (x, z) of the local point (lx, 0, lz) on the wall frame fr."""
    yaw, o = fr
    p = rot_y((lx, 0.0, lz), yaw)
    return (o[0] + p[0], o[2] + p[2])


class Builder:
    def __init__(self, H, posts=None, log=None):
        self.H = H
        self.interior = False          # while True, merged solids are interior-only (dropped from Resolution 3)
        self.posts = posts if posts is not None else []
        self.log = log if log is not None else []

    @staticmethod
    def P(name):
        return Part(name, "", "")

    to_world = staticmethod(to_world)

    def merge(self, part):
        n0 = len(self.H.solids)
        self.H.merge(part)
        if self.interior:
            for s in self.H.solids[n0:]:
                s.interior = True

    def put(self, sub_, fr, dx=0.0, dy=0.0, mirror=False, what=None):
        """Place a sub-part (built in its wall-local frame) on the wall frame fr, dx along the wall, dy up."""
        yaw, o = fr
        off = rot_y((dx, 0.0, 0.0), yaw)
        self.merge(sub_.transformed(yaw, (o[0] + off[0], o[1] + dy, o[2] + off[2]), mirror))
        if what:
            self.log.append(what)

    def place_door(self, door_part, fr, dx, dy, mirror=False, label=""):
        """A registry door / window part placed on a wall frame; its twin selection and action point are renamed to
        doorstwin<k> (k = the building's next door), the DoorsTwinN convention (PLAYBOOK §15 T3)."""
        H = self.H
        k = len(H.doors) + 1
        dp = copy.copy(door_part)
        dp.solids = [copy.copy(s) for s in door_part.solids]
        dp.memory = dict(door_part.memory)
        dp.doors = [copy.copy(d) for d in door_part.doors]
        old = dp.doors[0].twin
        new = "doorstwin%d" % k
        for s in dp.solids:
            if s.sel == old:
                s.sel = new
        dp.memory[new + "_action"] = dp.memory.pop(old + "_action")
        dp.doors[0].twin = new
        dp.doors[0].label = label
        self.put(dp, fr, dx, dy, mirror, what="%s: %s%s" % (new, door_part.name, " (mirrored)" if mirror else ""))
        return H.doors[-1]

    def posts_on(self, fr, xs, y0, y1, size=POST):
        """Posts at the local nodes xs of the wall frame fr (a node already holding a post is skipped)."""
        for lx in xs:
            x, z = to_world(fr, lx)
            if any(abs(x - a) < 1e-4 and abs(z - b) < 1e-4 for a, b, _, _ in self.posts):
                continue
            self.posts.append((x, z, y0, y1))
            p_ = frame.post(self.H, x, z=z, y0=y0, y1=y1, size=size)
            if self.interior:
                p_.interior = True

    def grime_post(self, x, z, y0):
        g = trim.part_grime("_post")
        self.H.merge(g.transformed(0.0, (x, y0, z)))

    def grime_exterior_posts(self, is_exterior):
        """Grime decal at the foot of every post for which is_exterior(x, z) is true."""
        for (x, z, y0, y1) in self.posts:
            if is_exterior(x, z):
                self.grime_post(x, z, y0)

    def dodai_stones(self, fr, x0, x1, seed, sill_y, show=0.15, out=0.10):
        """found.dodai_stones (dressed) under a wall run: the sill stays on the wall line; the stone course is set
        `out` outwards so its inner face is flush with the inside of the wall (no kerb inside the doma, no stone under
        a doorway). sill_y = the dodai top."""
        s = self.P("dodai_%d" % seed)
        found.dodai_stones(s, x0, x1, dressed=True, show=show, seed=seed)
        s.solids = [x.transformed(0.0, (0.0, 0.0, out)) if x.tag in ("dodai_stone", "dodai_stone_lod") else x
                    for x in s.solids]
        self.put(s, fr, 0.0, sill_y, what="found.dodai_stones _dressed (jp_p_found_dodai_stones_dressed recipe)")

    def wall(self, fr, name, kind, x0, x1, y0, y1, finish="nakanuri", head=True, openings_=(), grime=None,
             koshiita=None, kokabe="plaster", internal_posts=False, mat=None, board_opts=None, thick=None,
             head_clip=None, interior=None):
        """walls.wall_run placed on fr, plus koshiita [(a, b, h)] and grime bands [(a, b, face_z or None)].
        interior: 'back' = an exterior wall (its -z face looks into a room), 'both' = a partition (the default while
        self.interior is on), see PLAYBOOK §15 T6: interior faces never use the exterior-weathered earth.
        head_clip (lo, hi): the head rail (kamoi) stops short of a perpendicular door line's leaves."""
        if interior is None:
            interior = "both" if self.interior else "back"
        s = self.P(name)
        walls.wall_run(s, kind, x0, x1, y0=y0, y1=y1, openings=openings_, finish=finish, head=head, kokabe=kokabe,
                       internal_posts=internal_posts, mat=mat, board_opts=board_opts, thick=thick, interior=interior)
        if head_clip:
            lo, hi = head_clip
            for i, x in enumerate(s.solids):
                if x.tag == "head_rail":
                    b = x.bbox()
                    s.solids[i] = box(max(b[0], lo), min(b[1], hi), b[2], b[3], b[4], b[5], "wood_weathered",
                                      vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head_rail").finalize()
        t = walls.FINISH[finish][1] if kind == "shinkabe" else 0.075
        if koshiita:
            for (a, b, h) in koshiita:
                walls.koshiita(s, a, b, h, t / 2, y0=y0)
        if grime:
            for (a, b, face) in grime:
                trim.grime_band(s, a, b, face if face is not None else t / 2 + (0.015 if koshiita else 0.0), y0=y0)
        self.put(s, fr, what="walls.wall_run %s %s (%s)" % (kind, finish if kind == "shinkabe" else (mat or ""), name))
        return s

    def sloped_wall(self, fr, name, nodes, y0, ytop, what=None, **kw):
        """leanto.sloped_wall placed on fr (a wall under a lean-to verge; ytop(local x) = the roof line)."""
        from . import leanto
        s = leanto.sloped_wall(name, nodes, y0, ytop, **kw)
        self.put(s, fr, what=what or "leanto.sloped_wall (%s)" % name)
        return s

    def lod_policy(self):
        """The building-level LOD policy: Resolution 3 = the exterior shell only (interior solids leave it); koshiita /
        board walls show as one slab from Resolution 2 on."""
        for s_ in self.H.solids:
            if getattr(s_, "interior", False) and 3 in s_.vis:
                s_.vis = set(s_.vis) - {3}
            if s_.tag == "board" and set(s_.vis) == {1, 2}:
                s_.vis = {1}
            if s_.tag in ("koshiita_lod", "board_lod") and set(s_.vis) == {3}:
                s_.vis = {2, 3}


def model_frame(H, cx, cz):
    """Kit frame -> model frame: origin moved to (cx, 0, cz) (the footprint centre at grade, autocenter=0)."""
    return H.transformed(0.0, (-cx, 0.0, -cz))
