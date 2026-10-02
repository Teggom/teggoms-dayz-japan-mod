"""W3C2 specialty props for the wave-3c-2 rural / industrial sites (spikes/W3C2/W3C2_NOTES.md): the potter (kick wheel,
wedging board, ware-drying rack, wares in straw, kiln furniture), the tile works (green-tile rack, tile stack, the
moulding bench), lime / quarry / mine (limestone heap, spoil heap, cut blocks, the stone sledge on rollers, the ore
sorting table, the washing sluice, the windlass), the salt works (the sieve stand, the salt draining baskets, the
pine-needle fuel heap). Built into jp_furniture.pbo by spikes/W3C2/build_w3c2.py (after W3C1). Frames as fkit / lkit:
'floor' base centre on the floor, +z = front; 'wall' origin on the floor below, wall face z = 0, the prop at +z.

Dead world, autumn: every kiln cold, the clay dry and cracked, the camps left; the work where it lay.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "W3B"))
sys.path.insert(0, os.path.join(DEV, "spikes", "W2F"))
import props_w3b as P3  # noqa: E402  (W3B helpers, read-only)
from props_w2f_sacred import (core, box, prism, lathe, xf, xfs, W, col, cyl_col, LPart, pole, cord,  # noqa
                              wear_all, rng, M, WOOD, WEATH, IRON, DARK, PALE, BAMBOO, ASH, ROPE, KINARI, INDIGO,
                              PAPER, KURO, CUTSTONE)
from bits import stain, mound, disc  # noqa: E402
from skit import beam  # noqa: E402
from jpparts.shapes import oriented_box  # noqa: E402

CAT = "sitefit"
SOOTW = "wood_sooted"
CLAY = "wall_nakanuri_int"          # wet / dry clay
EARTH = "ground_earth_bare"
FIRED = "ceramic_earthenware"
STONEW = "ceramic_stoneware_pale"
GLAZED = "ceramic_stoneware_dark"
STRAW = "straw_tawara"
STRAWS = "straw_stack"
FIELD = "stone_field"
RIVER = "stone_river"
LIME = "wall_shikkui"
LITTER = "ground_leaf_litter"
tub_shell, hoops, adds1 = P3.tub_shell, P3.hoops, P3.adds1


def ocol(p0, p1, w, h, mat=WEATH, up=(0.0, 1.0, 0.0)):
    """An oriented collision member (Geometry / View / Fire)."""
    return beam(p0, p1, w, h, mat, up=up, vis=(), geo=True, view=True, fire=True)


def lump(r_, cx, cy, cz, s, mat=FIELD, n=7, flat=0.6):
    """A small rounded stone / clay lump of size s resting with its foot at cy."""
    return core.stone(r_, cx, cz, s, s * 0.85, s * 0.70, cy + s * 0.70, mat, bury=0.0, n=n, flat_top=flat, vis=(1,))


def bowl(r, h, mat, y=0.0, x=0.0, z=0.0, n=10):
    """A small thrown bowl / cup (lathe, open cup)."""
    s = lathe([(0.0, 0.0), (r * 0.55, 0.0), (r, h), (r - 0.008, h), (r * 0.55 - 0.008, 0.008), (0.0, 0.008)], n, mat,
              vis=(1,))
    return xf(s, t=(x, y, z))


# ================================================================================================ 2 potter
def keri_rokuro(ab=False):
    """The kick wheel (keri-rokuro): a heavy wooden flywheel (0.80 across) at foot height on a pivot stone, the shaft,
    the wheelhead (0.42) at 0.55 with a half-thrown jar gone dry on it; the potter's seat board behind (-z).
    ab: the wheelhead knocked off, the jar broken on the floor."""
    P = LPart("keri_rokuro", budget="furniture", mass=90.0, anchor="floor")
    r_ = rng("rokuro" + str(ab))
    out = [lump(r_, 0.0, 0.0, 0.0, 0.22, FIELD)]                                      # the pivot stone
    out.append(lathe([(0.0, 0.14), (0.40, 0.14), (0.40, 0.24), (0.0, 0.24)], 14, WEATH, vis=(1,)))   # flywheel
    for k in range(4):                                                                # its spokes (kicked)
        a = k * math.pi / 2 + 0.3
        out.append(W(-0.025, 0.025, 0.24, 0.27, 0.06, 0.36, SOOTW, vis=(1,)))
        out[-1] = xf(out[-1], ry=math.degrees(a))
    out.append(pole((0.0, 0.24, 0.0), (0.0, 0.55, 0.0), 0.035, WEATH, n=6, vis=(1,)))
    head = [lathe([(0.0, 0.55), (0.21, 0.55), (0.21, 0.60), (0.0, 0.60)], 12, WEATH, vis=(1,))]
    jar = lathe([(0.0, 0.0), (0.10, 0.0), (0.13, 0.12), (0.09, 0.22), (0.08, 0.22), (0.12, 0.12), (0.09, 0.01),
                 (0.0, 0.01)], 12, CLAY, vis=(1,))
    if ab:
        out += [xf(s, rx=80.0, pivot=(0.0, 0.575, 0.0), t=(0.45, 0.21 - 0.575, 0.35)) for s in head]
        for k in range(4):
            out.append(lump(r_, -0.35 + 0.12 * k, 0.0, 0.42 + 0.05 * (k % 2), 0.07, CLAY, n=5, flat=0.9))
    else:
        out += head
        out.append(xf(jar, t=(0.0, 0.60, 0.0)))
    # the seat board on two blocks behind the wheel
    out.append(W(-0.35, 0.35, 0.0, 0.28, -0.78, -0.62, WEATH, vis=(1,)))
    out.append(W(-0.40, 0.40, 0.28, 0.32, -0.82, -0.52, WEATH, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(lathe([(0.0, 0.0), (0.40, 0.0), (0.40, 0.27), (0.0, 0.27)], 8, WEATH, vis=(2,)))
    P.add(W(-0.40, 0.40, 0.0, 0.32, -0.82, -0.52, WEATH, vis=(2,)))
    P.add(cyl_col(0.40, 0.0, 0.27, n=8, mat=WEATH))
    P.add(col(-0.40, 0.40, 0.0, 0.32, -0.82, -0.52, WEATH))
    if not ab:
        P.add(W(-0.21, 0.21, 0.27, 0.60, -0.21, 0.21, WEATH, vis=(2,)))
        P.add(col(-0.21, 0.21, 0.27, 0.60, -0.21, 0.21, WEATH))
    P.dim("wheel_d", 0.80, 0.80, tol=0.01)
    P.notes.append("kick wheel (keri-rokuro)%s" % (", the wheelhead knocked off, the jar broken" if ab else
                                                  ", a half-thrown jar gone dry on the head"))
    return P


def neri_ban():
    """The wedging board: a heavy plank (1.10 x 0.60) on two blocks at 0.40 with a lump of clay half wedged (the
    chrysanthemum kneading), a wire cutter, beside it the clay heap on the floor under a wet mat gone dry."""
    P = LPart("neri_ban", budget="furniture", mass=60.0, anchor="floor")
    r_ = rng("neri")
    out = [W(-0.55, 0.55, 0.34, 0.42, -0.30, 0.30, WEATH, vis=(1,))]
    for sx in (-0.42, 0.42):
        out.append(W(sx - 0.10, sx + 0.10, 0.0, 0.34, -0.26, 0.26, WEATH, vis=(1,)))
    out.append(lathe([(0.0, 0.42), (0.17, 0.42), (0.15, 0.52), (0.06, 0.57), (0.0, 0.57)], 9, CLAY, vis=(1,)))
    out.append(cord((-0.40, 0.425, 0.20), (-0.10, 0.425, 0.24), 0.002))
    for sx in (-0.42, -0.08):
        out.append(W(sx - 0.015, sx + 0.015, 0.42, 0.45, 0.17, 0.27, WEATH, vis=(1,)))
    # the clay heap on the floor (+x), a straw mat over half of it
    out.append(mound("neri_heap", 0.95, 0.05, 0.38, 0.32, CLAY, sx=1.1, vis=(1,)))
    out.append(xf(W(-0.32, 0.32, 0.0, 0.012, -0.28, 0.28, "straw_mushiro", vis=(1,)), rz=-18.0, t=(0.86, 0.22, 0.05)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.55, 0.55, 0.0, 0.42, -0.30, 0.30, WEATH, vis=(2,)))
    P.add(W(0.60, 1.30, 0.0, 0.30, -0.30, 0.38, CLAY, vis=(2,)))
    P.add(col(-0.55, 0.55, 0.0, 0.42, -0.30, 0.30, WEATH))
    P.add(col(0.62, 1.28, 0.0, 0.28, -0.28, 0.36, CLAY))
    P.dim("board_h", 0.42, 0.42, tol=0.01)
    P.notes.append("wedging board with clay half wedged, the clay heap under a dried mat")
    return P


def ware_rack(fallen=False):
    """The ware-drying rack: two posts each end (1.80 m apart) carrying three plank shelves (0.35, 0.95, 1.55), rows
    of unfired bowls on them (free-standing on its four posts; set against a wall or in the yard). fallen: the top plank down at one end, its bowls broken on the floor."""
    P = LPart("ware_rack", budget="furniture", mass=60.0, anchor="floor")
    r_ = rng("warerack" + str(fallen))
    out = []
    for sx in (-0.92, 0.92):
        for sz in (0.05, 0.40):
            out.append(W(sx - 0.03, sx + 0.03, 0.0, 1.70, sz - 0.03, sz + 0.03, WEATH, vis=(1,)))
    ys = (0.35, 0.95, 1.55)
    for k, y in enumerate(ys):
        for sx in (-0.92, 0.92):
            out.append(W(sx - 0.035, sx + 0.035, y - 0.06, y - 0.03, 0.02, 0.43, WEATH, vis=(1,)))
        top = (k == 2 and fallen)
        plank = W(-1.00, 1.00, y - 0.03, y, 0.03, 0.42, WEATH, vis=(1,))
        if top:
            # the right end dropped to the middle plank's bar: the plank leans from its left bracket down to the right
            a = math.degrees(math.atan2(0.57, 1.84))
            out.append(xf(plank, rz=-a, pivot=(-0.92, y, 0.2)))
            for j in range(5):
                out.append(lump(r_, -0.30 + 0.28 * j, 0.0, 0.62 + 0.08 * (j % 2), 0.07, CLAY, n=5, flat=0.9))
            continue
        for j in range(6):
            out.append(bowl(0.075, 0.07, CLAY, y=y, x=-0.80 + 0.32 * j, z=0.24))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.95, 0.95, 0.0, 1.70, 0.02, 0.43, WEATH, vis=(2,)))
    P.add(col(-0.95, 0.95, 0.0, 1.70, 0.02, 0.43, WEATH))
    P.dim("w", 2.0, 2.0, tol=0.01)
    P.notes.append("ware-drying rack with rows of unfired bowls%s" % (", the top plank fallen, bowls broken" if fallen
                                                                       else ""))
    return P


def wares_straw():
    """Finished wares packed for the road: stacks of bowls tied in straw rope (four bundles) and two jars in straw
    jackets, on the floor."""
    P = LPart("wares_straw", budget="furniture", mass=40.0, anchor="floor")
    out = []
    for k, (x, z) in enumerate(((-0.40, -0.10), (-0.10, -0.12), (0.20, -0.08), (-0.25, 0.22))):
        out.append(lathe([(0.0, 0.0), (0.13, 0.0), (0.15, 0.30), (0.12, 0.34), (0.0, 0.34)], 9, STRAW, vis=(1,)))
        out[-1] = xf(out[-1], t=(x, 0.0, z))
        for y in (0.08, 0.20):
            out.append(xf(lathe([(0.145, y - 0.012), (0.158, y - 0.012), (0.158, y + 0.012), (0.145, y + 0.012)], 9,
                                ROPE, vis=(1,), closed_ends=False), t=(x, 0.0, z)))
    for (x, z) in ((0.42, 0.18), (0.10, 0.28)):
        out.append(xf(lathe([(0.0, 0.0), (0.12, 0.0), (0.18, 0.18), (0.13, 0.40), (0.08, 0.42), (0.0, 0.42)], 10,
                            STRAW, vis=(1,)), t=(x, 0.0, z)))
        out.append(xf(lathe([(0.0, 0.42), (0.075, 0.42), (0.075, 0.46), (0.0, 0.46)], 8, GLAZED, vis=(1,)),
                      t=(x, 0.0, z)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.55, 0.60, 0.0, 0.40, -0.25, 0.45, STRAW, vis=(2,)))
    P.add(col(-0.55, 0.60, 0.0, 0.40, -0.25, 0.45, STRAW))
    P.dim("h", 0.46, 0.46, tol=0.02)
    P.notes.append("finished wares tied in straw for the road")
    return P


def kiln_shelves():
    """Kiln furniture by the kiln: stacks of fired-clay shelves (tana-ita, 0.40 sq) and the round props (tsuku) set
    out on the ground, a few broken."""
    P = LPart("kiln_shelves", budget="furniture", mass=80.0, anchor="floor")
    r_ = rng("kshelves")
    out = []
    for (x, z, n) in ((-0.35, 0.0, 6), (0.15, -0.05, 4)):
        for k in range(n):
            out.append(xf(W(-0.20, 0.20, 0.03 * k, 0.03 * k + 0.028, -0.20, 0.20, FIRED, vis=(1,)),
                          ry=r_.uniform(-6, 6), t=(x, 0.0, z)))
    for j in range(7):
        x, z = 0.45 + 0.10 * (j % 3), -0.20 + 0.14 * (j // 3)
        out.append(lathe([(0.0, 0.0), (0.045, 0.0), (0.04, 0.12), (0.0, 0.12)], 7, FIRED, vis=(1,)))
        out[-1] = xf(out[-1], t=(x, 0.0, z))
    out.append(xf(W(-0.20, 0.0, 0.0, 0.028, -0.20, 0.05, FIRED, vis=(1,)), ry=30.0, t=(0.0, 0.0, 0.35)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.55, 0.70, 0.0, 0.18, -0.25, 0.30, FIRED, vis=(2,)))
    P.add(col(-0.55, 0.36, 0.0, 0.18, -0.25, 0.25, FIRED))
    P.dim("shelf", 0.40, 0.40, tol=0.01)
    P.notes.append("kiln shelves and props stacked by the kiln")
    return P


# ================================================================================================ 3 tile works
KAWARA = "roof_kawara"


def tile(mat, x=0.0, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0):
    """One sangawara pan tile (~0.28 x 0.30, its S-wave as two shallow planes), lying flat at (x, y, z)."""
    a = W(-0.14, 0.02, 0.0, 0.016, -0.15, 0.15, mat, vis=(1,))
    b = xf(W(0.0, 0.13, 0.0, 0.016, -0.15, 0.15, mat, vis=(1,)), rz=14.0, t=(0.02, 0.0, 0.0))
    return [xf(s_, rx=rx, ry=ry, rz=rz, t=(x, y, z)) for s_ in (a, b)]


def kawara_rack(collapsed=False):
    """The green-tile drying rack (free-standing): four posts, three slatted shelves (0.30, 0.80, 1.30) 1.80 long, the
    unfired tiles standing on edge in a row on each, leaning a little. collapsed: the top shelf down, tiles broken."""
    P = LPart("kawara_rack", budget="furniture", mass=90.0, anchor="floor")
    r_ = rng("kawararack" + str(collapsed))
    out = []
    for sx in (-0.90, 0.90):
        for sz in (-0.20, 0.20):
            out.append(W(sx - 0.035, sx + 0.035, 0.0, 1.50, sz - 0.035, sz + 0.035, WEATH, vis=(1,)))
    for k, y in enumerate((0.30, 0.80, 1.30)):
        for sx in (-0.90, 0.90):
            out.append(W(sx - 0.04, sx + 0.04, y - 0.06, y - 0.025, -0.24, 0.24, WEATH, vis=(1,)))
        if collapsed and k == 2:
            out.append(xf(W(-0.95, 0.95, 0.0, 0.025, -0.22, 0.22, WEATH, vis=(1,)), rz=-17.0, pivot=(-0.90, 0.0, 0.0),
                          t=(0.0, y - 0.025, 0.0)))
            for j in range(6):
                out += tile(CLAY, -0.60 + 0.25 * j, 0.0, 0.45 + 0.10 * (j % 2), ry=r_.uniform(-40, 40))
            continue
        for sz in (-0.12, 0.12):
            out.append(W(-0.95, 0.95, y - 0.025, y, sz - 0.08, sz + 0.08, WEATH, vis=(1,)))
        for j in range(7):
            out += tile(CLAY, -0.75 + 0.25 * j, y + 0.15, 0.0, rx=0.0, rz=78.0)
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.95, 0.95, 0.0, 1.50, -0.24, 0.24, WEATH, vis=(2,)))
    P.add(col(-0.95, 0.95, 0.0, 1.50, -0.24, 0.24, WEATH))
    P.dim("l", 1.90, 1.90, tol=0.01)
    P.notes.append("green-tile drying rack%s" % (", the top shelf collapsed, tiles broken" if collapsed else ""))
    return P


def kawara_stack(scattered=False):
    """Fired tiles stacked on edge in two long rows on a plank pallet (1.40 x 0.70, 0.55 high) for the carts.
    scattered: one row pushed over, tiles slid and broken on the ground."""
    P = LPart("kawara_stack", budget="furniture", mass=400.0, anchor="floor")
    r_ = rng("kawarastack" + str(scattered))
    out = [W(-0.72, 0.72, 0.0, 0.06, -0.36, 0.36, WEATH, vis=(1,))]
    for row, z in enumerate((-0.17, 0.17)):
        if scattered and row == 1:
            for j in range(8):
                out += tile(KAWARA, -0.60 + 0.17 * j + r_.uniform(-0.05, 0.05), 0.0, 0.55 + r_.uniform(0, 0.35),
                            ry=r_.uniform(-60, 60))
            continue
        for j in range(16):
            out += tile(KAWARA, -0.64 + 0.085 * j, 0.06 + 0.15, z, rz=82.0)
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.72, 0.72, 0.0, 0.36, -0.36, 0.36, KAWARA, vis=(2,)))
    P.add(col(-0.72, 0.72, 0.0, 0.36, -0.36, 0.36 if not scattered else 0.0, KAWARA))
    P.dim("w", 1.44, 1.44, tol=0.01)
    P.notes.append("fired tiles stacked on edge on a pallet%s" % (", one row pushed over" if scattered else ""))
    return P


def kawara_bench():
    """The tile maker's moulding bench (1.60 x 0.70 at 0.70): the wooden mould (kata) with a clay slab in it, the
    bow-wire cutter, a slab block waiting, the burnishing spatula; at the right end a half-carved ridge-end tile
    (onigawara) on its board."""
    P = LPart("kawara_bench", budget="furniture", mass=70.0, anchor="floor")
    r_ = rng("kbench")
    out = [W(-0.80, 0.80, 0.64, 0.70, -0.35, 0.35, WEATH, vis=(1,))]
    for sx in (-0.70, 0.70):
        for sz in (-0.28, 0.28):
            out.append(W(sx - 0.04, sx + 0.04, 0.0, 0.64, sz - 0.04, sz + 0.04, WEATH, vis=(1,)))
    # the mould: a shaped board frame with a clay slab
    for (a, b, c, d) in ((-0.55, -0.20, -0.20, -0.17), (-0.55, -0.20, 0.17, 0.20), (-0.55, -0.52, -0.17, 0.17),
                         (-0.23, -0.20, -0.17, 0.17)):
        out.append(W(a, b, 0.70, 0.74, c, d, SOOTW, vis=(1,)))
    out.append(W(-0.52, -0.23, 0.70, 0.725, -0.17, 0.17, CLAY, vis=(1,)))
    # the slab block (a clay loaf) and the bow-wire cutter
    out.append(W(-0.10, 0.25, 0.70, 0.86, -0.16, 0.16, CLAY, vis=(1,)))
    out.append(pole((-0.05, 0.71, 0.24), (0.40, 0.71, 0.24), 0.008, BAMBOO, n=4, vis=(1,)))
    out.append(cord((-0.03, 0.715, 0.24), (0.38, 0.715, 0.24), 0.001))
    out.append(W(0.30, 0.42, 0.70, 0.71, -0.30, -0.22, WEATH, vis=(1,)))           # the spatula
    # the onigawara: a thick shaped plaque, half carved, on its board
    out.append(W(0.46, 0.78, 0.70, 0.72, -0.20, 0.20, WEATH, vis=(1,)))
    oni = prism([(-0.13, 0.0), (0.13, 0.0), (0.13, 0.22), (0.07, 0.32), (0.0, 0.35), (-0.07, 0.32), (-0.13, 0.22)],
                "z", -0.05, 0.05, CLAY, vis=(1,))
    out.append(xf(oni, t=(0.62, 0.72, 0.0)))
    out.append(xf(W(-0.05, 0.05, 0.0, 0.05, 0.05, 0.065, CLAY, vis=(1,)), t=(0.62, 0.86, 0.0)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.80, 0.80, 0.0, 0.72, -0.35, 0.35, WEATH, vis=(2,)))
    P.add(col(-0.80, 0.80, 0.0, 0.70, -0.35, 0.35, WEATH))
    P.dim("h", 0.70, 0.70, tol=0.01)
    P.notes.append("tile moulding bench: mould, wire cutter, slab, a half-carved onigawara")
    return P


# ================================================================================================ 4-6 heaps (lime, quarry, mine)
def _heap_solid(r_, rx, rz, h, mat, vis=(1,), geo=False, n=10):
    base = [(rx * (1 + r_.uniform(-0.12, 0.12)) * math.cos(2 * math.pi * k / n),
             rz * (1 + r_.uniform(-0.12, 0.12)) * math.sin(2 * math.pi * k / n)) for k in range(n)]
    base = core.hull2d(base)
    prof = [(0.0, 1.0), (h * 0.45, 0.70), (h * 0.80, 0.38), (h, 0.10)]
    kw = dict(geo=True, view=True, fire=True) if geo else {}
    return core.rings((base, prof), mat, vis=vis, **kw)


def heap(kind="limestone"):
    """A heap of broken stone on the ground: 'limestone' (pale limestone lumps waiting for the kiln, 2.2 x 1.6, 0.9
    high) or 'spoil' (a mine's spoil: earth and grey rock, 3.4 x 2.4, 1.3 high). Lumps lie on its slopes."""
    big = kind == "spoil"
    P = LPart(kind + "_heap", budget="furniture", mass=5000.0 if big else 2000.0, anchor="floor")
    r_ = rng("heap" + kind)
    rx, rz, h = (1.70, 1.20, 1.30) if big else (1.10, 0.80, 0.90)
    body = EARTH if big else LIME
    out = [_heap_solid(r_, rx, rz, h, body)]
    lm = FIELD if big else LIME
    for k in range(14 if big else 12):
        a = r_.uniform(0, 2 * math.pi)
        f = r_.uniform(0.15, 0.95)
        x, z = rx * f * math.cos(a), rz * f * math.sin(a)
        y = h * (1.0 - f) * 0.92
        out.append(lump(r_, x, max(0.0, y - 0.06), z, r_.uniform(0.18, 0.34), lm if k % 3 else FIELD, n=6))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(_heap_solid(r_, rx, rz, h, body, vis=(2,), n=8))
    P.add(_heap_solid(rng("heapcol" + kind), rx * 0.9, rz * 0.9, h * 0.9, body, vis=(), geo=True, n=8))
    P.dim("h", h, h, tol=0.25)
    P.notes.append("%s heap" % ("mine spoil" if big else "limestone"))
    return P


# ================================================================================================ 5 quarry
def ishi_blocks():
    """Cut building blocks (andesite / granite) waiting by the face: three squared blocks on skid timbers, one on top
    showing its row of wedge holes (ya-ana) along a split edge, a fourth with the lord's mark cut on its face."""
    P = LPart("ishi_blocks", budget="furniture", mass=6000.0, anchor="floor")
    r_ = rng("ishiblocks")
    from jpparts.shapes import rough_block
    out = []
    for sz in (-0.45, 0.45):
        out.append(W(-1.10, 1.10, 0.0, 0.12, sz - 0.07, sz + 0.07, WEATH, vis=(1,)))
    blocks = [(-0.55, 0.12, 0.0, 0.95, 0.60, 0.80), (0.50, 0.12, 0.0, 1.00, 0.55, 0.85), (0.0, 0.67, 0.0, 1.20, 0.50, 0.70)]
    for (x, y, z, w, h, d) in blocks:
        out.append(rough_block(r_, x - w / 2, x + w / 2, y, y + h, z - d / 2, z + d / 2, CUTSTONE, chamfer=0.03,
                               top_jit=0.01, vis=(1,)))
    for k in range(5):
        x = -0.45 + 0.22 * k
        out.append(W(x - 0.035, x + 0.035, 1.12, 1.172, 0.33, 0.352, DARK, vis=(1,)))
    # the fourth block on the ground in front, the lord's mark (a cut circle-and-bar) on its face
    out.append(rough_block(r_, -0.40, 0.40, 0.0, 0.55, 0.85, 1.45, CUTSTONE, chamfer=0.03, top_jit=0.01, vis=(1,)))
    out.append(W(-0.12, 0.12, 0.25, 0.27, 1.45, 1.455, DARK, vis=(1,)))
    out.append(W(-0.01, 0.01, 0.14, 0.38, 1.45, 1.455, DARK, vis=(1,)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-1.10, 1.10, 0.0, 1.17, -0.52, 0.52, CUTSTONE, vis=(2,)))
    P.add(W(-0.40, 0.40, 0.0, 0.55, 0.85, 1.45, CUTSTONE, vis=(2,)))
    P.add(col(-1.05, 1.05, 0.0, 1.17, -0.52, 0.52, CUTSTONE))
    P.add(col(-0.40, 0.40, 0.0, 0.55, 0.85, 1.45, CUTSTONE))
    P.dim("h", 1.17, 1.17, tol=0.02)
    P.notes.append("cut blocks on skids, wedge holes along one, the lord's mark on another")
    return P


def ishi_shura(ab=False):
    """The stone sledge (shura): a heavy oak sledge 2.4 m long, its two runners turned up at the front, cross-pieces,
    a squared block lashed on it, resting on three log rollers on two plank skids; the hauling rope coiled at the front.
    ab: the lashing cut, the block slid half off, a roller rolled away."""
    P = LPart("ishi_shura", budget="furniture", mass=3000.0, anchor="floor")
    r_ = rng("shura" + str(ab))
    from jpparts.shapes import rough_block
    out = []
    for sx in (-0.55, 0.55):
        out.append(W(sx - 0.10, sx + 0.10, 0.0, 0.05, -1.50, 1.50, WEATH, vis=(1,)))          # the skids
    for k, z in enumerate((-0.80, 0.0, 0.80)):
        zz = z + (0.9 if (ab and k == 2) else 0.0)
        xx = 0.35 if (ab and k == 2) else 0.0
        out.append(pole((-0.80 + xx, 0.13, zz), (0.80 + xx, 0.13, zz), 0.08, WEATH, n=7, vis=(1,)))
    yb = 0.21
    for sx in (-0.42, 0.42):
        out.append(W(sx - 0.09, sx + 0.09, yb, yb + 0.16, -1.20, 0.95, WEATH, vis=(1,)))
        out.append(xf(W(sx - 0.09, sx + 0.09, 0.0, 0.16, 0.0, 0.40, WEATH, vis=(1,)), rx=-35.0,
                      t=(0.0, yb, 0.95)))
    for z in (-0.95, -0.30, 0.35):
        out.append(W(-0.55, 0.55, yb + 0.16, yb + 0.24, z - 0.07, z + 0.07, WEATH, vis=(1,)))
    yt = yb + 0.24
    if ab:
        out.append(xf(rough_block(r_, -0.45, 0.45, 0.0, 0.60, -0.45, 0.45, CUTSTONE, chamfer=0.03, top_jit=0.01,
                                  vis=(1,)), rz=-12.0, t=(0.55, yt - 0.10, -0.30)))
    else:
        out.append(rough_block(r_, -0.45, 0.45, yt, yt + 0.60, -0.75, 0.15, CUTSTONE, chamfer=0.03, top_jit=0.01,
                               vis=(1,)))
        for z in (-0.55, -0.05):
            out.append(cord((-0.47, yt + 0.61, z), (0.47, yt + 0.61, z), 0.012))
            for sx in (-0.47, 0.47):
                out.append(cord((sx, yt + 0.61, z), (sx, yt, z), 0.012))
    out.append(lathe([(0.10, 0.0), (0.26, 0.0), (0.26, 0.10), (0.10, 0.10)], 10, ROPE, vis=(1,)))
    out[-1] = xf(out[-1], t=(0.0, 0.0, 1.65))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.65, 0.65, 0.0, yt, -1.50, 1.30, WEATH, vis=(2,)))
    P.add(col(-0.65, 0.65, 0.0, yt, -1.40, 1.20, WEATH))
    if not ab:
        P.add(W(-0.45, 0.45, yt, yt + 0.60, -0.75, 0.15, CUTSTONE, vis=(2,)))
        P.add(col(-0.45, 0.45, yt, yt + 0.60, -0.75, 0.15, CUTSTONE))
    P.dim("l", 2.6, 2.6, tol=0.5)
    P.notes.append("stone sledge (shura) on log rollers%s" % (", the block slid off, a roller gone" if ab else
                                                             " with a block lashed on"))
    return P


# ================================================================================================ 6 mine
def senko_dai():
    """The ore sorting table (the women's work in the sorting shed): a low plank bench (1.80 x 0.70 at 0.40) with two
    flat anvil stones, small hand hammers, a heap of broken ore, sorted piles in shallow baskets beside it."""
    P = LPart("senko_dai", budget="furniture", mass=120.0, anchor="floor")
    r_ = rng("senko")
    out = [W(-0.90, 0.90, 0.34, 0.40, -0.35, 0.35, WEATH, vis=(1,))]
    for sx in (-0.78, 0.78):
        out.append(W(sx - 0.08, sx + 0.08, 0.0, 0.34, -0.30, 0.30, WEATH, vis=(1,)))
    for x in (-0.45, 0.35):
        out.append(lump(r_, x, 0.40, 0.0, 0.28, FIELD, n=7, flat=0.85))
        out.append(W(x + 0.10, x + 0.32, 0.40, 0.43, 0.15, 0.19, WEATH, vis=(1,)))     # hammer handle
        out.append(W(x + 0.06, x + 0.12, 0.40, 0.46, 0.13, 0.21, IRON, vis=(1,)))      # its head
    for k in range(9):
        out.append(lump(r_, -0.05 + r_.uniform(-0.25, 0.25), 0.40, r_.uniform(-0.25, 0.20), r_.uniform(0.05, 0.10),
                        FIELD if k % 2 else "stone_cut", n=5, flat=0.7))
    for (x, z) in ((-0.55, 0.65), (0.35, 0.68)):
        out.append(xf(lathe([(0.0, 0.0), (0.22, 0.0), (0.26, 0.10), (0.24, 0.10), (0.20, 0.015), (0.0, 0.015)], 10,
                            BAMBOO, vis=(1,)), t=(x, 0.0, z)))
        for j in range(4):
            out.append(lump(r_, x + r_.uniform(-0.10, 0.10), 0.015, z + r_.uniform(-0.10, 0.10), 0.07, FIELD, n=5))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.90, 0.90, 0.0, 0.42, -0.35, 0.35, WEATH, vis=(2,)))
    P.add(col(-0.90, 0.90, 0.0, 0.40, -0.35, 0.35, WEATH))
    P.dim("h", 0.40, 0.40, tol=0.01)
    P.notes.append("ore sorting bench with anvil stones, hammers, ore; sorted ore in baskets")
    return P


def nekonagashi():
    """The washing sluice (neko-nagashi): a board trough 2.4 m long on two trestles, sloping (0.75 -> 0.45), lined with
    straw mats that caught the gold, a wooden pan (yuri-ita) on its lower end, a tub under the spout; dry."""
    P = LPart("nekonagashi", budget="furniture", mass=50.0, anchor="floor")
    a = math.degrees(math.atan2(0.30, 2.40))
    tr = [W(-1.20, 1.20, 0.0, 0.03, -0.20, 0.20, WEATH, vis=(1,)),
          W(-1.20, 1.20, 0.03, 0.16, -0.22, -0.20, WEATH, vis=(1,)),
          W(-1.20, 1.20, 0.03, 0.16, 0.20, 0.22, WEATH, vis=(1,)),
          W(1.17, 1.20, 0.03, 0.16, -0.20, 0.20, WEATH, vis=(1,)),
          W(-1.10, 1.10, 0.03, 0.036, -0.19, 0.19, "straw_mushiro", vis=(1,))]
    out = [xf(s_, rz=a, t=(0.0, 0.60, 0.0)) for s_ in tr]
    for (x, h) in ((-0.95, 0.60 - 0.95 * math.tan(math.radians(a)) - 0.01), (0.95, 0.60 + 0.95 * math.tan(math.radians(a)) - 0.01)):
        for sz in (-0.18, 0.18):
            out.append(W(x - 0.03, x + 0.03, 0.0, h, sz - 0.03, sz + 0.03, WEATH, vis=(1,)))
        out.append(W(x - 0.035, x + 0.035, h - 0.04, h, -0.24, 0.24, WEATH, vis=(1,)))
    out.append(xf(tub_shell(0.24, 0.26, 0.02, WEATH, n=10), t=(-1.40, 0.0, 0.0)))
    out.append(xf(W(-0.28, 0.28, 0.0, 0.03, -0.18, 0.18, WEATH, vis=(1,)), rz=8.0, t=(-1.45, 0.27, 0.0)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-1.65, 1.20, 0.0, 0.75, -0.24, 0.24, WEATH, vis=(2,)))
    P.add(col(-1.20, 1.20, 0.0, 0.70, -0.24, 0.24, WEATH))
    P.dim("l", 2.40, 2.40, tol=0.01)
    P.notes.append("the gold-washing sluice with straw mats, dry")
    return P


def makiage():
    """The windlass (makiage-guruma) over a prospect shaft, the shaft boarded over: a frame of two A-shaped trestles
    1.60 apart carrying the drum (0.26 across) with its two crank handles, the rope wound on it running down to a
    bucket set on the boards; the board cover (1.6 x 1.4) lies flush on a timber collar."""
    P = LPart("makiage", budget="furniture", mass=150.0, anchor="floor")
    out = []
    # the collar and the board cover over the shaft
    for (a, b, c, d) in ((-0.85, 0.85, -0.75, -0.62), (-0.85, 0.85, 0.62, 0.75), (-0.85, -0.72, -0.62, 0.62),
                         (0.72, 0.85, -0.62, 0.62)):
        out.append(W(a, b, 0.0, 0.14, c, d, SOOTW, vis=(1,)))
    for k in range(6):
        z = -0.60 + 0.20 * k + 0.10
        out.append(W(-0.80, 0.80, 0.14, 0.17, z - 0.095, z + 0.095, WEATH, vis=(1,)))
    # the trestles
    yd = 1.05
    for sx in (-0.80, 0.80):
        for sz in (-0.55, 0.55):
            out.append(pole((sx, 0.0, sz), (sx, yd, 0.0), 0.05, WEATH, n=6, vis=(1,)))
        out.append(W(sx - 0.06, sx + 0.06, yd - 0.08, yd + 0.06, -0.12, 0.12, WEATH, vis=(1,)))
    out.append(pole((-0.95, yd, 0.0), (0.95, yd, 0.0), 0.13, WEATH, n=8, vis=(1,)))
    out.append(xf(lathe([(0.135, -0.25), (0.165, -0.25), (0.165, 0.25), (0.135, 0.25)], 8, ROPE, vis=(1,),
                        closed_ends=False), rz=90.0, t=(0.0, yd, 0.0)))
    for sx, sg in ((-0.95, -1), (0.95, 1)):
        out.append(W(sx + sg * 0.0, sx + sg * 0.04, yd - 0.02, yd + 0.34, -0.03, 0.03, WEATH, vis=(1,)))
        out.append(pole((sx + sg * 0.02, yd + 0.32, 0.0), (sx + sg * 0.25, yd + 0.32, 0.0), 0.02, WEATH, n=5, vis=(1,)))
    out.append(cord((0.10, yd - 0.15, 0.0), (0.10, 0.48, 0.0), 0.012))
    out.append(xf(tub_shell(0.17, 0.30, 0.02, WEATH, n=10), t=(0.10, 0.17, 0.0)))
    wear_all(out, "_w2")
    adds1(P, out)
    P.add(W(-0.85, 0.85, 0.0, 0.17, -0.75, 0.75, WEATH, vis=(2,)))
    P.add(W(-0.95, 0.95, yd - 0.13, yd + 0.13, -0.13, 0.13, WEATH, vis=(2,)))
    for sx in (-0.80, 0.80):
        P.add(W(sx - 0.06, sx + 0.06, 0.17, yd, -0.45, 0.45, WEATH, vis=(2,)))
        P.add(col(sx - 0.06, sx + 0.06, 0.17, yd - 0.13, -0.50, 0.50, WEATH))
    P.add(col(-0.85, 0.85, 0.0, 0.17, -0.75, 0.75, WEATH))
    P.add(col(-0.95, 0.95, yd - 0.13, yd + 0.13, -0.13, 0.13, WEATH))
    P.dim("drum_y", yd, yd, tol=0.01)
    P.notes.append("the windlass over a boarded-over prospect shaft, rope wound, the bucket on the boards")
    return P


PROPS = [
    {"id": "jp_f_keri_rokuro", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_keri_rokuro", "std", "intact", "Potter's kick wheel with a dry half-thrown jar", lambda: keri_rokuro()),
        M("jp_f_keri_rokuro_ab", "std", "broken", "Potter's kick wheel, the head knocked off", lambda: keri_rokuro(True))]},
    {"id": "jp_f_neri_ban", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_neri_ban", "std", "intact", "Wedging board with clay and the clay heap", neri_ban)]},
    {"id": "jp_f_ware_rack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_ware_rack", "std", "intact", "Ware-drying rack with unfired bowls", lambda: ware_rack()),
        M("jp_f_ware_rack_fallen", "std", "fallen", "Ware-drying rack, the top plank fallen", lambda: ware_rack(True))]},
    {"id": "jp_f_wares_straw", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_wares_straw", "std", "intact", "Wares packed in straw for the road", wares_straw)]},
    {"id": "jp_f_kiln_shelves", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kiln_shelves", "std", "intact", "Kiln shelves and props stacked", kiln_shelves)]},
    {"id": "jp_f_kawara_rack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kawara_rack", "std", "intact", "Green-tile drying rack", lambda: kawara_rack()),
        M("jp_f_kawara_rack_collapsed", "std", "broken", "Green-tile drying rack, top shelf collapsed",
          lambda: kawara_rack(True))]},
    {"id": "jp_f_kawara_stack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kawara_stack", "std", "intact", "Fired roof tiles stacked on a pallet", lambda: kawara_stack()),
        M("jp_f_kawara_stack_scattered", "std", "scattered", "Fired roof tiles, a row pushed over",
          lambda: kawara_stack(True))]},
    {"id": "jp_f_kawara_bench", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_kawara_bench", "std", "intact", "Tile moulding bench with a half-carved onigawara", kawara_bench)]},
    {"id": "jp_f_limestone_heap", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_limestone_heap", "std", "intact", "Heap of broken limestone for the kiln", lambda: heap("limestone"))]},
    {"id": "jp_f_spoil_heap", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_spoil_heap", "std", "intact", "Mine spoil heap (earth and rock)", lambda: heap("spoil"))]},
    {"id": "jp_f_ishi_blocks", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_ishi_blocks", "std", "intact", "Cut stone blocks on skids", ishi_blocks)]},
    {"id": "jp_f_ishi_shura", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_ishi_shura", "std", "intact", "Stone sledge (shura) on rollers with a block", lambda: ishi_shura()),
        M("jp_f_ishi_shura_ab", "std", "broken", "Stone sledge, the block slid off", lambda: ishi_shura(True))]},
    {"id": "jp_f_senko_dai", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_senko_dai", "std", "intact", "Ore sorting bench with hammers and ore", senko_dai)]},
    {"id": "jp_f_nekonagashi", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_nekonagashi", "std", "intact", "Gold-washing sluice on trestles, dry", nekonagashi)]},
    {"id": "jp_f_makiage", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_makiage", "std", "intact", "Windlass over a boarded-over prospect shaft", makiage)]},
]
