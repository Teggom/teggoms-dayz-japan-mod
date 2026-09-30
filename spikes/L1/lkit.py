"""lkit - the L1 life-layer kit: B3a's furniture kit (fkit, bits) and B3b's site kit (skit: oriented poles and beams,
rope paths, cloth grids, atlas text decals, convex hulls), imported read-only, plus the few things the life layer
adds: pegs and peg boards, hanging strings, coils, small fruit, and the LPart that records how far a hanging prop
drops below its beam.

Frames (B3a fkit.py, the sidecar 'anchor'):
  'floor'  base centre on the supporting surface (floor, shelf board, chest lid)
  'wall'   origin on the floor below the prop; the wall (or post) face is z = 0, the prop sits at +z; height built in
  'hang'   origin at the beam (or door-head) underside; the prop hangs down (-y); z = 0 is the beam's centre line
Where it may go = the sidecar 'mount' (build_l1.MOUNT_NOTE): wall, post, beam, doorway, surface, floor, kamado.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "spikes", "B3b"), os.path.join(DEV, "spikes", "B3a")):
    if p not in sys.path:
        sys.path.append(p)
import fkit  # noqa: E402
import bits  # noqa: E402
import skit  # noqa: E402
from fkit import (core, box, prism, ngon, sheet, Solid, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col,  # noqa
                  lcyl, rest, auto_smooth, rotated_box, board, FPart)
from bits import disc, stain, shards, mound, pillow, jag_rim, rope_ring, soft_slab, blob  # noqa: E402,F401
from skit import pole, beam, rope_path, sag, grid_sheet, text_on, hull3, hull_col, frame, basis  # noqa: E402,F401

# ------------------------------------------------------------------------------------------------ materials
WOOD = "wood_interior"
WEATH = "wood_weathered"
SOOTW = "wood_sooted"
IRON = "metal_iron"
PALE = "ceramic_stoneware_pale"
DARK = "ceramic_stoneware_dark"
LACQ = "lacquer_black"
BAMBOO = "bamboo_weathered"
SOOTB = "bamboo_sooted"
WEAVE = "bamboo_weave"
MUSHIRO = "straw_mushiro"
TAWARA = "straw_tawara"
ROPE = "straw_rope"
STACK = "straw_stack"
PAPER = "paper_shoji"
FUSUMA = "paper_fusuma"
CHOCHIN = "paper_chochin"
INDIGO = "textile_cotton_indigo"
KINARI = "textile_cotton_plain"
KINARI_CUT = "textile_kinari"
NOREN = "textile_noren"
RED = "textile_bib_red"
ASH = "ground_ash"
LEAF = "ground_leaf_litter"
LITTER = "decal_litter"
STONE = "stone_river"
CUT = "stone_cut"
SUMI = "decal_sumi_text"            # B1's atlas (kanban, oke marks)
LIFE = "decal_sumi_text_life"       # L1's atlas (make_l1_materials.py): ofuda, calendar, lanterns, ledgers, cask mark
RICE = "food_rice"                  # L1
KAKI = "food_hoshigaki"             # L1
KAYA = "textile_kaya"               # L1


class LPart(FPart):
    """An FPart that can say how far it hangs below its beam (hang_len) and where a pot-seated prop sits (seat_y)."""

    def __init__(self, name, budget="small", res3=False, mass=2.0, anchor="floor", flat=False, wear="_w1"):
        super().__init__(name, budget=budget, res3=res3, mass=mass, anchor=anchor, flat=flat, wear=wear)
        self.hang_len = None
        self.seat_y = None

    def adds(self, ss):
        for s in ss:
            self.add(s)
        return ss

    def finish_hang(self):
        lo = min(v[1] for s in self.solids if s.vis for v in s.verts)
        self.hang_len = -lo
        return self


def M(p3d, variant, state, display, fn, **kw):
    d = {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}
    d.update(kw)
    return d


def rng(name):
    return random.Random(core.hash_str(name))


def wear_all(ss, w):
    for s in ss:
        if w and not getattr(s, "wear", None):
            s.wear = w
    return ss


# ------------------------------------------------------------------------------------------------ wall furniture
def peg(x, y, L=0.09, r=0.011, mat=WOOD, vis=(1,), up=0.02, z0=0.0):
    """A round wooden peg driven into the wall at (x, y), sticking out along +z, tipped up a little."""
    return pole((x, y, z0 + 0.003), (x, y + up, z0 + L), r, mat, n=5, vis=vis)     # tilted cap stays off z0


def peg_board(x0, x1, y0, y1, t=0.02, k=3, vis=(1, 2)):
    """The board nailed to the wall that carries the pegs (wall face z = 0)."""
    return board(x0, x1, y0, y1, 0.0, t, k=k, vis=vis)


def cord(p0, p1, r=0.004, mat=ROPE, vis=(1,), n=3):
    return pole(p0, p1, r, mat, n=n, vis=vis)


def hook_iron(x, y, z=0.0, drop=0.06, vis=(1,)):
    """A bent iron hook screwed into a beam underside: a short stem and the hook bar."""
    return [box(x - 0.004, x + 0.004, y - drop, y, z - 0.004, z + 0.004, IRON, vis=vis),
            box(x - 0.004, x + 0.004, y - drop, y - drop + 0.008, z - 0.004, z + 0.03, IRON, vis=vis)]


# ------------------------------------------------------------------------------------------------ small shapes
def bipyramid(c, rx, ry, rz, mat, n=4, vis=(1,), phase=0.0, wear=None, top=None):
    """A small closed double cone (fruit, pods, chilli): n-gon waist at c, tips at c +- ry (top may differ)."""
    top = ry if top is None else top
    ring = [(c[0] + rx * math.cos(phase + 2 * math.pi * k / n), c[1], c[2] + rz * math.sin(phase + 2 * math.pi * k / n))
            for k in range(n)]
    verts = ring + [(c[0], c[1] + top, c[2]), (c[0], c[1] - ry, c[2])]
    faces = []
    for k in range(n):
        j = (k + 1) % n
        faces.append([k, j, n])
        faces.append([j, k, n + 1])
    s = Solid(verts, faces, mat, vis=vis)
    if wear:
        s.wear = wear
    return s


def coil(cx, cy, R, r, mat=ROPE, sy=1.0, n=10, m=4, z0=0.0, vis=(1,), wear=None, turns_axis="z"):
    """A rope coil (torus, oval by sy) standing flat against a wall: ring in the x-y plane, tube radius r, its back
    touching z = z0. Closed tube, explicit normals."""
    quads, normals = [], []

    def P(i, j):
        a = 2 * math.pi * i / n
        b = 2 * math.pi * j / m
        cxp, cyp = cx + R * math.cos(a), cy + R * sy * math.sin(a)
        rad = (math.cos(a), sy * math.sin(a))
        L = math.hypot(*rad) or 1.0
        rad = (rad[0] / L, rad[1] / L)
        o = (rad[0] * r * math.cos(b), rad[1] * r * math.cos(b), r * math.sin(b))
        return (cxp + o[0], cyp + o[1], z0 + r + o[2]), (rad[0] * math.cos(b), rad[1] * math.cos(b), math.sin(b))
    for i in range(n):
        for j in range(m):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            quads.append([p for p, _ in q])
            nn = [sum(v[1][k] for v in q) / 4 for k in range(3)]
            normals.append(core.norm(nn))
    s = sheet(quads, mat, normals, vis=vis)
    s.finalize()
    if wear:
        s.wear = wear
    return s


def flat_coil(cx, cz, R, r, mat=ROPE, n=10, m=3, vis=(1,), wear=None, sx=1.0):
    """A rope coil lying on the floor (the wall coil turned face up)."""
    s = coil(0.0, 0.0, R, r, mat, sy=sx, n=n, m=m, z0=0.0, vis=vis, wear=wear)
    return xf(s, rx=-90.0, t=(cx, 0.0, cz))


def lod_box(ss, mat, vis=(2,), pad=0.0, wear=None):
    """A single box round the given solids (a lower-LOD stand-in)."""
    xs = [v[0] for s in ss for v in s.verts]
    ys = [v[1] for s in ss for v in s.verts]
    zs = [v[2] for s in ss for v in s.verts]
    b = box(min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad, min(zs) - pad, max(zs) + pad, mat, vis=vis)
    if wear:
        b.wear = wear
    return b


def only_vis(ss, vis):
    """Copies of solids shown in the given LODs only."""
    out = []
    for s in ss:
        n = xf(s)
        n.vis = set(vis)
        out.append(n)
    return out


# ------------------------------------------------------------------------------------------------ readable text
# DayZ model space is LEFT-handed (x right, y up, z forward, like the world: x east, z north, y up). Seen from the
# front (+z), the model's +x is on the VIEWER'S LEFT (B3a render.py's camera shows the same). A decal whose texture u
# runs along +x on a +z face therefore reads MIRRORED. text() and uvcell() run u against the face's 'right' vector
# (right x up = the outward normal, as skit.text_on), so the atlas reads as drawn when seen from outside the face.
# L2 (2026-09-30): text_on's quad itself faces INTO the host (outward = -(right x up)), so build_l1.py turns every
# text solid round after building (skit.face_text(mirror_u=False)); new code should use skit.text_ok().
def text(center, right, up, h, mat, cellname, wear="_w1", off=0.002, vis=(1,), width=None, crop=None):
    """skit.text_on with the texture u mirrored: reads correctly in game (see the note above)."""
    s = text_on(center, right, up, h, mat, cellname, wear=wear, off=off, vis=vis, width=width, crop=crop)
    us = [a for f in s.fuv for a, _ in f]
    lo, hi = min(us), max(us)
    s.fuv = [[(lo + hi - a, b) for a, b in f] for f in s.fuv]
    return s


def uvcell(mat, cellname):
    """uv(u, v) for a grid_sheet whose u runs along the face's +right (e.g. +x on a +z face): mirrored u, see above."""
    u0, v0, u1, v1 = skit.cell(mat, cellname)
    return lambda u, v: (u1 - (u1 - u0) * u, v0 + (v1 - v0) * v)


def wall_text(x, y, h, cellname, z=0.0, wear="_w1", mat=LIFE, width=None, off=0.002):
    """Text on a surface facing +z at height y (centre)."""
    return text((x, y, z), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), h, mat, cellname, wear=wear, off=off, width=width)


def place_group(vis_ss, col_ss, ops, floor=0.0):
    """Apply the same sequence of xf() calls (ops: [dict(rx=..., ry=..., rz=..., t=...)]) to visual solids and their
    collision primitives, then shift both so the lowest visual vertex sits at `floor` (a tipped prop and its hull)."""
    for op in ops:
        vis_ss = [xf(q, **op) for q in vis_ss]
        col_ss = [xf(q, **op) for q in col_ss]
    lo = min(v[1] for q in vis_ss for v in q.verts)
    t = (0.0, floor - lo, 0.0)
    out_c = []
    for q in col_ss:                                     # each collision block rests on the floor on its own
        lc = min(v[1] for v in q.verts)
        out_c.append(xf(q, t=(0.0, floor - lc, 0.0)))
    return [xf(q, t=t) for q in vis_ss], out_c
