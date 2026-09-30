"""l2kit - the L2 (outdoor life layer) kit: B3b's site kit (skit: SPart, poles, beams, cloth grids, hulls, text),
L1's life kit (lkit: pegs, cords, fruit, coils) and a few of their builders (imported read-only, never modified),
plus what the outdoor life layer adds: foliage cards, sheaf rows, shell sheets for open hulls, and M() with a mount.

Frames (skit.py): origin = base centre on the terrain, +y up, +z = the front (the road / the viewer); anchor 'wall':
the wall (facade) plane is z = 0, y = 0 at the wall foot. Text: skit.text_ok() (faces out, reads right in game).
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "spikes", "L1"), os.path.join(DEV, "spikes", "B3b"), os.path.join(DEV, "spikes", "B3a")):
    if p not in sys.path:
        sys.path.append(p)
import skit  # noqa: E402
import lkit  # noqa: E402
from skit import (core, box, prism, sheet, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole,  # noqa
                  beam, rope_path, sag, grid_sheet, text_ok, face_text, leaves, litter, add_all, ground, hull3,
                  hull_col, disc, rest, moss_top, frame)
from lkit import bipyramid, cord, coil, flat_coil, lod_box, only_vis  # noqa: E402,F401
from bits import stain, mound, blob  # noqa: E402,F401

# ------------------------------------------------------------------------------------------------ materials
WOOD = "wood_weathered"
DARK = "wood_street_dark"
INT = "wood_interior"
SOOTW = "wood_sooted"
BAMBOO = "bamboo_weathered"
WEAVE = "bamboo_weave"
IRON = "metal_iron"
PALE = "ceramic_stoneware_pale"
DARKC = "ceramic_stoneware_dark"
LACQ = "lacquer_black"
RIVER = "stone_river"
FIELD = "stone_field"
CUT = "stone_cut"
MUSHIRO = "straw_mushiro"
TAWARA = "straw_tawara"
ROPE = "straw_rope"
STACK = "straw_stack"
PAPER = "paper_shoji"
CHOCHIN = "paper_chochin"
KINARI = "textile_kinari"          # alpha cut (rags)
PLAIN = "textile_cotton_plain"
INDIGO = "textile_cotton_indigo"
LEAF = "ground_leaf_litter"
EARTH = "ground_doma_earth"
ASH = "ground_ash"
LITTER = "decal_litter"
SUMI = "decal_sumi_text"
LIFE = "decal_sumi_text_life"
RICE = "food_rice"
KAKI = "food_hoshigaki"
NET = "textile_net"                # L2 (research/materials/make_l2_materials.py)
FOLI = "plant_foliage"             # L2


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


def lod2_box(ss, mat, pad=0.0, wear=None, vis=(2,)):
    return lod_box(ss, mat, vis=vis, pad=pad, wear=wear)


# ------------------------------------------------------------------------------------------------ foliage cards
def card(c, w, h, yaw=0.0, kind="leaf", wear=None, tilt=0.0, vis=(1,), bottom=True):
    """A two-sided foliage card (jp_m_plant_foliage): w wide, h tall, standing on c (bottom centre) unless bottom=False
    (then c is the card centre), turned yaw about y and tilted about its own x. Needles map onto u 0-0.5, leaves onto
    u 0.5-1 (the atlas halves)."""
    u0 = 0.0 if kind == "needle" else 0.5
    du = min(0.5, w / 0.5 * 0.5)
    dv = min(1.0, h / 0.5)
    y0 = 0.0 if bottom else -h / 2
    s = grid_sheet(lambda u, v: ((u - 0.5) * w, y0 + h * (1 - v), 0.0), 1, 1, FOLI, vis=vis, two_sided=True,
                   uv=lambda u, v: (u0 + du * u, dv * v), wear=wear)
    s = xf(s, rx=tilt, ry=yaw, t=c)
    return s


def bush(c, R, H, kind="leaf", wear=None, n=3, seed=1, vis=(1,)):
    """A small bush of n crossed vertical cards + one horizontal cap card."""
    r = random.Random(seed)
    out = [card(c, 2 * R, H, yaw=180.0 * k / n + r.uniform(-10, 10), kind=kind, wear=wear, vis=vis) for k in range(n)]
    cap = grid_sheet(lambda u, v: ((u - 0.5) * 2 * R * 0.9, 0.0, (v - 0.5) * 2 * R * 0.9), 1, 1, FOLI, vis=vis,
                     two_sided=True, uv=lambda u, v: ((0.0 if kind == "needle" else 0.5) + 0.4 * u, 0.8 * v), wear=wear)
    out.append(xf(cap, ry=r.uniform(0, 90), t=(c[0], c[1] + H * 0.8, c[2])))
    return out


# ------------------------------------------------------------------------------------------------ shells (open hulls)
def quad_sheet(pts4, mat, normal, uvs=None, vis=(1,), wear=None):
    s = sheet([[tuple(p) for p in pts4]], mat, core.norm(normal), vis=vis, uvs=[uvs] if uvs else None)
    s.finalize()
    if wear:
        s.wear = wear
    return s


def strip(A, Bs, mat, out_hint, vis=(1,), wear=None, tile=None):
    """A sheet between two polylines A[i] and Bs[i] (same length); each quad's normal is chosen to point towards
    out_hint(p) (a function giving the wanted side at a point). World-ish uv along the strip."""
    t = tile or core.mat_info(mat)["tile"]
    quads, normals, uvs = [], [], []
    s_acc = 0.0
    for i in range(len(A) - 1):
        q = [A[i], A[i + 1], Bs[i + 1], Bs[i]]
        n = core.norm(core.newell(q))
        want = out_hint(tuple(sum(p[k] for p in q) / 4 for k in range(3)))
        if core.dot(n, want) < 0:
            n = core.mul(n, -1.0)
        L = core.length(core.sub(A[i + 1], A[i]))
        wv = core.length(core.sub(Bs[i], A[i]))
        quads.append(q)
        normals.append(n)
        uvs.append([(s_acc / t, 0.0), ((s_acc + L) / t, 0.0), ((s_acc + L) / t, wv / t), (s_acc / t, wv / t)])
        s_acc += L
    s = sheet(quads, mat, normals, vis=vis, uvs=uvs)
    s.finalize()
    if wear:
        s.wear = wear
    return s
