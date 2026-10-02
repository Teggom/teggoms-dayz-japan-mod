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
]
