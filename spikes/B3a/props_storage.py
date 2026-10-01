"""Storage and packing props (BUILD_LIST rows 25-30): nagamochi, tansu, kori, box, tawara, rack.

Reuse by B3b: tawara_bale() / tawara_stack() / kamasu() take their material and wear as arguments (outdoor bales
under eaves, at the rice store, on carts).
"""
import math
import random

import fkit
import bits
import tansu
from fkit import (core, box, prism, ngon, sheet, lathe, xf, xfs, flat_poly, W, col, cyl_col, board, FPart, rest,
                  WOOD, IRON, DARK, PALE, TAWARA, MUSHIRO, PAPER, INDIGO, KINARI, LACQUER, WEAVE, LITTER, WICKER)
from bits import disc, shards, stain, rope_ring, mound, pillow

CAT = "storage"
ROPE = "straw_rope"


def add_all(P, ss):
    for s in ss:
        P.add(s)


# ================================================================================================ nagamochi
NL, ND, NH = 1.70, 0.72, 0.75
NT = 0.025          # board thickness
NB = 0.10           # inner floor height (the open variant's loot point)
LID_T = 0.03


def naga_iron(torn=False):
    """Corner straps on the 8 vertical edges, the lock plate, the pole brackets on the two ends."""
    out = []
    x0, x1, z0, z1 = -NL / 2, NL / 2, -ND / 2, ND / 2
    for i, (sx, sz) in enumerate(((-1, -1), (-1, 1), (1, -1), (1, 1))):
        if torn and i == 3:
            continue
        xe, ze = (x0 if sx < 0 else x1), (z0 if sz < 0 else z1)
        for y0, y1 in ((0.02, 0.14), (NH - LID_T - 0.13, NH - LID_T - 0.01)):
            out.append(box(xe - sx * 0.08, xe + sx * 0.003, y0, y1, ze - 0.0015 * sz, ze + 0.003 * sz, IRON, vis=(1,)))
            out.append(box(xe - sx * 0.0015, xe + sx * 0.003, y0, y1, ze - sz * 0.08, ze + sz * 0.003, IRON, vis=(1,)))
    # pole brackets (sao-toshi): a staple on each end near the top
    for sx in (-1, 1):
        xe = x1 if sx > 0 else x0
        for zc in (-0.13, 0.13):
            out.append(box(xe, xe + sx * 0.05, NH - LID_T - 0.13, NH - LID_T - 0.10, zc - 0.012, zc + 0.012, IRON,
                           vis=(1,)))
            out.append(box(xe + sx * 0.04, xe + sx * 0.055, NH - LID_T - 0.20, NH - LID_T - 0.10, zc - 0.012,
                           zc + 0.012, IRON, vis=(1,)))
        out.append(box(xe, xe + sx * 0.012, NH - LID_T - 0.22, NH - LID_T - 0.07, -0.17, 0.17, IRON, vis=(1, 2)))
    # the lock plate on the front
    out.append(box(-0.07, 0.07, NH - LID_T - 0.14, NH - LID_T - 0.02, z1, z1 + 0.003, IRON, vis=(1, 2)))
    if torn:
        # one pole bracket torn, hanging askew
        b = box(0.0, 0.012, -0.075, 0.075, -0.17, 0.17, IRON, vis=(1,))
        out.append(xf(b, rx=35.0, t=(x1 + 0.012, NH - LID_T - 0.23, 0.10)))
    return out


def naga_lid(wear=None):
    out = [board(-NL / 2 - 0.01, NL / 2 + 0.01, 0.0, LID_T, -ND / 2 - 0.01, ND / 2 + 0.01, k=4, vis=(1, 2))]
    for x in (-NL / 2 + 0.05, NL / 2 - 0.05):      # end battens under the lid, inside the box
        out.append(W(x - 0.04, x + 0.04, -0.03, 0.0, -ND / 2 + NT + 0.005, ND / 2 - NT - 0.005, vis=(1,)))
    for s in out:
        if wear:
            s.wear = wear
    return out


def nagamochi(state="shut"):
    P = FPart("nagamochi", budget="furniture", res3=True, mass=40.0)
    x0, x1, z0, z1 = -NL / 2, NL / 2, -ND / 2, ND / 2
    yt = NH - LID_T
    body = [board(x0, x1, 0.0, NB, z0, z1, k=0, vis=(1, 2)),                            # bottom block
            board(x0, x1, NB, yt, z1 - NT, z1, k=1, vis=(1, 2)),                        # front
            board(x0, x1, NB, yt, z0, z0 + NT, k=2, vis=(1, 2)),                        # back
            board(x0, x0 + NT, NB, yt, z0 + NT, z1 - NT, k=3, vis=(1, 2)),              # ends
            board(x1 - NT, x1, NB, yt, z0 + NT, z1 - NT, k=5, vis=(1, 2))]
    add_all(P, body)
    add_all(P, naga_iron(torn=state != "shut"))
    P.add(W(x0, x1, 0.0, NH if state == "shut" else yt, z0, z1, vis=(3,)))
    if state == "shut":
        add_all(P, xfs(naga_lid(), t=(0.0, yt, 0.0)))
        fkit.road_tops(P, [P.add(col(x0, x1, 0.0, NH, z0, z1))], "boards")    # F1: stand on the lid
        P.loot_rect("lid", NH, x0 + 0.1, x1 - 0.1, z0 + 0.1, z1 - 0.1, rng=0.3,
                    points=[(-0.42, NH, 0.0), (0.42, NH, 0.0)])
    else:
        # lid thrown back against the wall (hinged on the back edge, 100 deg), clothes spilling over the front
        lid = xfs(naga_lid(wear="_w2"), rx=-100.0, pivot=(0.0, LID_T, -ND / 2 - 0.01))
        add_all(P, xfs(lid, t=(0.0, yt, 0.0)))
        P.add(W(x0, x1, yt, yt + 0.73, z0 - 0.06, z0 - 0.01, vis=(3,)))
        P.add(col(x0 - 0.01, x1 + 0.01, yt, yt + 0.72, z0 - 0.07, z0 - 0.01))
        bottom = P.add(col(x0, x1, 0.0, NB, z0, z1))
        P.add(col(x0, x1, NB, yt, z1 - NT, z1))
        P.add(col(x0, x1, NB, yt, z0, z0 + NT))
        P.add(col(x0, x0 + NT, NB, yt, z0 + NT, z1 - NT))
        P.add(col(x1 - NT, x1, NB, yt, z0 + NT, z1 - NT))
        # F1: a player who climbs in stands on the inner floor (the rims are 2.5 cm: no Roadway there)
        P.road([(x0 + NT, NB, z0 + NT), (x1 - NT, NB, z0 + NT), (x1 - NT, NB, z1 - NT), (x0 + NT, NB, z1 - NT)],
               "boards")
        # cloth inside and spilling out
        P.add(xf(bits.cloth_patch(-0.45, -0.05, 0.50, 0.45, 8.0, INDIGO, h=0.06, vis=(1,)), t=(0.0, NB, 0.0)))
        # F1: the pale cloth lies against the front wall (x 0.08-0.48, z -0.12-0.30), the garment rises from it up the
        # inside of the front board, over the rim and down the outside, clear of the lock plate (x +-0.07)
        P.add(xf(bits.cloth_patch(0.28, 0.09, 0.40, 0.42, -4.0, KINARI, h=0.04, vis=(1,)), t=(0.0, NB, 0.0)))
        P.add(tansu.cloth_drape(0.12, 0.44, z1, yt, 0.45, ft=NT, land_y=NB + 0.04))
        add_all(P, tansu.garment(0.30, z1 + 0.30, -20.0))
        P.loot_rect("inside", NB, 0.3, x1 - NT - 0.05, z0 + 0.1, z1 - 0.1, rng=0.25, kind="floor",
                    points=[(0.55, NB, 0.0)])
        P.extra["needs_behind_m"] = 0.08
        P.notes.append("open: the lid stands 0.08 m behind the back face, so place the back >= 0.08 m off the wall")
    P.dim("length", NL, NL, tol=0.01)
    P.dim("depth", ND, ND, tol=0.01)
    P.dim("height", NH, NH, tol=0.01)
    P.notes.append("1.70 m long: along a wall only, never across a path; a 3-mat room gets at most one")
    return P


# ================================================================================================ kori
KW, KD, KH = 0.60, 0.40, 0.30


def kori_parts(lid_on=True, wear=None, lod2=True):
    """Wicker trunk: a woven base 0.58 x 0.38 x 0.27 (open box), a lid 0.60 x 0.40 x 0.12 over it, cord ties."""
    w, d, h, t = KW - 0.02, KD - 0.02, 0.27, 0.012
    out = [W(-w / 2, w / 2, 0.0, t, -d / 2, d / 2, WICKER, vis=(1,)),
           W(-w / 2, w / 2, 0.0, h, d / 2 - t, d / 2, WICKER, vis=(1,)),
           W(-w / 2, w / 2, 0.0, h, -d / 2, -d / 2 + t, WICKER, vis=(1,)),
           W(-w / 2, -w / 2 + t, 0.0, h, -d / 2 + t, d / 2 - t, WICKER, vis=(1,)),
           W(w / 2 - t, w / 2, 0.0, h, -d / 2 + t, d / 2 - t, WICKER, vis=(1,))]
    lid = [W(-KW / 2, KW / 2, KH - 0.012, KH, -KD / 2, KD / 2, WICKER, vis=(1,)),
           W(-KW / 2, KW / 2, KH - 0.12, KH, KD / 2 - 0.01, KD / 2, WICKER, vis=(1,)),
           W(-KW / 2, KW / 2, KH - 0.12, KH, -KD / 2, -KD / 2 + 0.01, WICKER, vis=(1,)),
           W(-KW / 2, -KW / 2 + 0.01, KH - 0.12, KH, -KD / 2 + 0.01, KD / 2 - 0.01, WICKER, vis=(1,)),
           W(KW / 2 - 0.01, KW / 2, KH - 0.12, KH, -KD / 2 + 0.01, KD / 2 - 0.01, WICKER, vis=(1,))]
    # rim bindings (darker bamboo edge strips) on the lid
    lid.append(W(-KW / 2 - 0.003, KW / 2 + 0.003, KH - 0.125, KH - 0.105, -KD / 2 - 0.003, KD / 2 + 0.003,
                 fkit.HOOP, vis=(1,)))
    cords = []
    for x in (-0.16, 0.16):        # two cords round the whole trunk
        cords.append(W(x - 0.008, x + 0.008, KH, KH + 0.006, -KD / 2 - 0.004, KD / 2 + 0.004, ROPE, vis=(1,)))
        cords.append(W(x - 0.008, x + 0.008, 0.0, KH + 0.006, KD / 2, KD / 2 + 0.006, ROPE, vis=(1,)))
    res = out + ((lid + cords) if lid_on else [])
    if lod2:
        res.append(W(-KW / 2, KW / 2, 0.0, KH if lid_on else h, -KD / 2, KD / 2, WICKER, vis=(2,)))
    for s in res:
        if wear:
            s.wear = wear
    return res, lid


def kori(state="1"):
    P = FPart("kori", budget="small", mass=4.0 if state != "2" else 8.0)
    if state == "1":
        ss, _ = kori_parts()
        add_all(P, ss)
        P.add(col(-KW / 2, KW / 2, 0.0, KH, -KD / 2, KD / 2))
        P.loot_rect("lid", KH, -0.25, 0.25, -0.15, 0.15, rng=0.2, points=[(0.0, KH, 0.0)])
    elif state == "2":
        ss, _ = kori_parts()
        add_all(P, ss)
        top, _ = kori_parts()
        add_all(P, xfs(top, ry=6.0, t=(0.02, KH, -0.01)))
        P.add(col(-KW / 2, KW / 2, 0.0, KH, -KD / 2, KD / 2))
        P.add(fkit.col_solid(xf(box(-KW / 2, KW / 2, 0.0, KH, -KD / 2, KD / 2, WICKER), ry=6.0, t=(0.02, KH, -0.01))))
        P.loot_rect("lid", 2 * KH, -0.2, 0.2, -0.12, 0.12, rng=0.2, points=[(0.02, 2 * KH, -0.01)])
    else:
        ss, lid = kori_parts(lid_on=False, wear="_w2")
        add_all(P, ss)
        # the lid lying upside down beside it, a garment hanging over the base's front edge
        add_all(P, rest(xfs(lid, rz=180.0, ry=-12.0, t=(0.66, 0.0, 0.05))))
        P.add(tansu.cloth_drape(-0.15, 0.12, KD / 2 - 0.01, 0.27, 0.22, ft=0.012, land_y=0.062))   # F1: onto the cloth
        P.add(bits.cloth_patch(0.0, 0.0, 0.50, 0.30, 0.0, KINARI, h=0.05, vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], t=(0.0, 0.012, 0.0))
        P.add(col(-KW / 2, KW / 2, 0.0, 0.27, -KD / 2, KD / 2))
        P.add(col(0.36, 0.96, 0.0, 0.12, -0.15, 0.25))
        P.loot_rect("inside", 0.062, -0.2, 0.2, -0.1, 0.1, rng=0.15, kind="floor", points=[(0.1, 0.062, -0.05)])
    P.dim("w", KW, KW, tol=0.005)
    P.dim("h", KH, KH, tol=0.005)
    return P


# ================================================================================================ box (hako)
BOX = {"s": (0.30, 0.20, 0.12), "m": (0.45, 0.30, 0.25), "l": (0.60, 0.40, 0.40)}


def hako(size="m", mat=WOOD, lid=True, open_body=False, wear=None, k=0, cord=False, vis=(1,)):
    """A lidded board box: body (closed, or open with 12 mm walls) and a cap lid 0.01 larger, 0.04 deep."""
    w, d, h = BOX[size]
    t = 0.012
    lh = min(0.04, h * 0.3)
    out = []
    bh = h - (0.0 if not lid else 0.004)
    if not open_body:
        out.append(board(-w / 2 + 0.004, w / 2 - 0.004, 0.0, bh, -d / 2 + 0.004, d / 2 - 0.004, k=k, mat=mat, vis=vis))
    else:
        out += [W(-w / 2 + 0.004, w / 2 - 0.004, 0.0, t, -d / 2 + 0.004, d / 2 - 0.004, mat, vis=vis),
                board(-w / 2 + 0.004, w / 2 - 0.004, 0.0, bh, d / 2 - 0.004 - t, d / 2 - 0.004, k=k, mat=mat, vis=vis),
                board(-w / 2 + 0.004, w / 2 - 0.004, 0.0, bh, -d / 2 + 0.004, -d / 2 + 0.004 + t, k=k + 1, mat=mat,
                      vis=vis),
                board(-w / 2 + 0.004, -w / 2 + 0.004 + t, 0.0, bh, -d / 2 + 0.004 + t, d / 2 - 0.004 - t, k=k + 2,
                      mat=mat, vis=vis),
                board(w / 2 - 0.004 - t, w / 2 - 0.004, 0.0, bh, -d / 2 + 0.004 + t, d / 2 - 0.004 - t, k=k + 3,
                      mat=mat, vis=vis)]
    lidp = [board(-w / 2, w / 2, h - 0.01, h, -d / 2, d / 2, k=k + 4, mat=mat, vis=vis),
            W(-w / 2, w / 2, h - lh, h - 0.01, d / 2 - 0.006, d / 2, mat, vis=vis),
            W(-w / 2, w / 2, h - lh, h - 0.01, -d / 2, -d / 2 + 0.006, mat, vis=vis),
            W(-w / 2, -w / 2 + 0.006, h - lh, h - 0.01, -d / 2 + 0.006, d / 2 - 0.006, mat, vis=vis),
            W(w / 2 - 0.006, w / 2, h - lh, h - 0.01, -d / 2 + 0.006, d / 2 - 0.006, mat, vis=vis)]
    if cord:
        lidp.append(W(-0.006, 0.006, h, h + 0.005, -d / 2 - 0.004, d / 2 + 0.004, KINARI, vis=(1,)))
        lidp.append(W(-w / 2 - 0.004, w / 2 + 0.004, h, h + 0.005, -0.006, 0.006, KINARI, vis=(1,)))
    if lid:
        out += lidp
    for s in out + lidp:
        if wear:
            s.wear = wear
    return out, lidp


def papers(seed, cx, cz, n, spread=0.25, vis=(1,)):
    """Spilled paper sheets and a cloth wrap on the floor (visual only)."""
    r = random.Random(seed)
    out = []
    for i in range(n):
        s = fkit.rotated_box(cx + r.uniform(-spread, spread), cz + r.uniform(-spread, spread), r.uniform(0.18, 0.26),
                             r.uniform(0.24, 0.32), 0.001 + 0.002 * i, 0.003 + 0.002 * i, r.uniform(0, 180), PAPER,
                             vis=vis)
        s.wear = "_w2"
        out.append(s)
    return out


def hako_model(size="m", state="intact", mat=WOOD):
    P = FPart("box", budget="small", mass={"s": 0.8, "m": 2.5, "l": 6.0}[size])
    w, d, h = BOX[size]
    if state == "intact":
        ss, _ = hako(size, mat, cord=(mat == LACQUER or size == "s"), k=2 if size == "m" else 0)
        add_all(P, ss)
        P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, mat, vis=(2,)))
        cb = P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, mat))
        if size == "l":
            fkit.road_tops(P, [cb], "boards")      # F1: the big lidded box is sturdy enough to stand on
            P.loot_rect("lid", h, -w / 2 + 0.05, w / 2 - 0.05, -d / 2 + 0.05, d / 2 - 0.05, rng=0.2,
                        points=[(0.0, h, 0.0)])
    else:   # open: lid off leaning on the side, contents spilled
        ss, lid = hako(size, mat, lid=False, open_body=True, wear="_w2")
        add_all(P, ss)
        lidw = [xf(s, t=(0.0, -h + 0.01, 0.0)) for s in lid]
        lidw = xfs(lidw, rz=180.0)
        add_all(P, rest(xfs(lidw, rx=-70.0, ry=90.0, t=(w / 2 + 0.06, 0.0, 0.0))))
        add_all(P, papers(size + "open", 0.0, d / 2 + 0.22, 4))
        P.add(bits.cloth_patch(0.0, 0.0, w * 0.7, d * 0.6, 12.0, INDIGO, h=0.05, vis=(1,)))
        P.solids[-1] = xf(P.solids[-1], t=(0.0, 0.012, 0.0))
        P.add(W(-w / 2, w / 2, 0.0, h - 0.04, -d / 2, d / 2, mat, vis=(2,)))
        P.add(col(-w / 2, w / 2, 0.0, h - 0.04, -d / 2, d / 2, mat))
        P.loot_rect("inside", 0.062, -w / 2 + 0.05, w / 2 - 0.05, -d / 2 + 0.05, d / 2 - 0.05, rng=0.2, kind="floor",
                    points=[(0.0, 0.062, 0.0)])
    P.dim("w", w, w, tol=0.005)
    P.dim("h", h, h, tol=0.005)
    return P


def hako_stack(state="intact"):
    P = FPart("box_stack", budget="small", mass=9.3)
    y = 0.0
    stack_cols = []
    sizes = ("l", "m", "s")
    yaws = (0.0, 5.0, -8.0)
    offs = ((0.0, 0.0), (-0.04, 0.02), (0.05, -0.01))
    for i, sz in enumerate(sizes):
        w, d, h = BOX[sz]
        if state != "intact" and sz == "s":
            # the small box knocked off: on its side on the floor, lid off, papers out
            ss, lid = hako("s", lid=False, open_body=True, wear="_w2")
            add_all(P, rest(xfs(ss, rx=90.0, ry=-30.0, t=(0.45, 0.0, 0.20))))
            add_all(P, rest(xfs(lid, rz=180.0, ry=40.0, t=(0.25, 0.0, 0.45))))
            add_all(P, papers(77, 0.45, 0.45, 3, 0.12))
            P.add(col(0.35, 0.58, 0.0, 0.20, 0.05, 0.34))
            continue
        ss, _ = hako(sz, cord=(sz == "s"), k=i * 2)
        add_all(P, xfs(ss, ry=yaws[i], t=(offs[i][0], y, offs[i][1])))
        P.add(xf(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, vis=(2,)), ry=yaws[i], t=(offs[i][0], y, offs[i][1])))
        stack_cols.append(P.add(fkit.col_solid(xf(box(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WOOD), ry=yaws[i],
                                                  t=(offs[i][0], y, offs[i][1])))))
        y += h
    fkit.road_tops(P, stack_cols, "boards")        # F1: the top of the stack (covered lids skipped)
    top = y
    if state == "intact":
        P.loot_rect("stack_top", top, -0.1, 0.1, -0.06, 0.06, rng=0.2, points=[(0.05, top, -0.01)])
    else:
        P.loot_rect("stack_top", top, -0.15, 0.15, -0.1, 0.1, rng=0.2, points=[(-0.04, top, 0.02)])
    P.dim("stack_h", 0.77 if state == "intact" else 0.65, top, tol=0.005)
    return P


# ================================================================================================ tawara / kamasu
def tawara_bale(n=10, segs="full", mat=TAWARA, rope=ROPE, wear=None, bands=3, vis=(1,), top_facet=True):
    """A straw rice bale lying along x (d 0.40, L 0.75), centre at y 0.20: barrel body, round end lids
    (sanbawara) a little proud, rope bands. Built about +y, then turned (+y -> +x)."""
    L, R = 0.75, 0.20
    ph = (math.pi - (math.floor((n - 1) / 2) + 0.5) * 2 * math.pi / n) if top_facet else None
    if segs == "full":
        prof = [(0.0, -L / 2 + 0.01), (0.13, -L / 2), (0.175, -L / 2 + 0.02), (0.19, -L / 2 + 0.06),
                (R, -0.15), (R, 0.15), (0.19, L / 2 - 0.06), (0.175, L / 2 - 0.02), (0.13, L / 2), (0.0, L / 2 - 0.01)]
    else:
        prof = [(0.0, -L / 2), (0.18, -L / 2 + 0.01), (R, -L / 2 + 0.09), (R, L / 2 - 0.09), (0.18, L / 2 - 0.01),
                (0.0, L / 2)]
    out = [lathe(prof, n, mat, vis=vis, phase=ph, wear=wear)]
    ys = {3: (-0.24, 0.0, 0.24), 2: (-0.2, 0.2), 1: (0.0,)}[bands]
    for y in ys:
        out.append(rope_ring(R, y, 0.025, rope, n, vis=vis, proud=0.008))
    out = xfs(out, rz=-90.0)          # +y -> +x
    return xfs(out, t=(0.0, R, 0.0))


def tawara_col(x=0.0, y=0.0, z=0.0, yaw=0.0, n=8):
    c = fkit.cyl_col(0.2, -0.375, 0.375, n=n, mat=TAWARA)
    c = xf(c, rz=-90.0, t=(0.0, 0.2, 0.0))
    return xf(c, ry=yaw, t=(x, y, z))


def tawara(state="1"):
    P = FPart("tawara", budget="small", mass=60.0 if state in ("1", "burst") else 360.0)
    if state in ("1", "burst"):
        ss = tawara_bale(wear="_w2" if state == "burst" else None)
        if state == "burst":
            # one end lid gone and a band broken: rice spilling out onto the floor, straw litter round it
            ss = [ss[0], ss[1], ss[3]]
            P.add(disc(0.15, 0.0, 0.03, TAWARA, n=8, vis=(1,), wear="_w2", cx=-0.62, cz=0.30))
            P.add(mound(3, -0.52, 0.05, 0.22, 0.05, PAPER, sx=1.2, wear="_w0"))
            P.add(stain(4, -0.40, 0.10, 0.45, sx=1.3, wear="_w2"))
        add_all(P, ss)
        P.add(fkit.lcyl("x", 0.2, 0.0, 0.2, -0.375, 0.375, TAWARA, n=6, vis=(2,)))
        fkit.road_tops(P, [P.add(tawara_col())], "tatami")     # F1: the bale's top facet (straw: carpet sound)
        yt = 0.2 + 0.2 * math.cos(math.pi / 10)
        P.loot_rect("top", yt, -0.25, 0.25, -0.05, 0.05, rng=0.25, points=[(0.12, yt, 0.0)])
        P.dim("d", 0.40, 0.40, tol=0.02)
        P.dim("L", 0.75, 0.75, tol=0.02)
    else:
        # pyramid of six, bales along z (end lids to the front): 3 + 2 + 1
        dy = 0.2 * math.sqrt(3)
        spots = [(-0.40, 0.0), (0.0, 0.0), (0.40, 0.0), (-0.20, dy), (0.20, dy), (0.0, 2 * dy)]
        bale_cols = []
        for i, (x, y) in enumerate(spots):
            burst = state == "stack6_burst" and i == 5
            ss = tawara_bale(n=6, segs="lo", bands=1, wear="_w2" if burst else None)
            if burst:
                ss = [ss[0]]
            add_all(P, xfs(ss, ry=90.0, t=(x, y, 0.0)))
            bale_cols.append(P.add(tawara_col(x, y, 0.0, 90.0, n=8)))
        fkit.road_tops(P, bale_cols, "tatami")     # F1: the exposed top facets of the pyramid
        P.add(W(-0.6, 0.6, 0.0, 0.4, -0.375, 0.375, TAWARA, vis=(2,)))
        P.add(W(-0.4, 0.4, 0.4, 0.4 + dy, -0.375, 0.375, TAWARA, vis=(2,)))
        P.add(W(-0.2, 0.2, 0.4 + dy, 0.4 + 2 * dy, -0.375, 0.375, TAWARA, vis=(2,)))
        top = 2 * dy + 0.4
        if state == "stack6_burst":
            P.add(mound(9, 0.1, 0.50, 0.25, 0.04, PAPER, sx=1.4, wear="_w0"))
            P.add(stain(10, 0.05, 0.50, 0.40, sx=1.5, wear="_w2"))
        # the top facet of the top bale (7-gon, a facet up at 0.2*cos(pi/7) above its axis)
        yt = 2 * dy + 0.2 + 0.2 * math.cos(math.pi / 6)
        P.loot_rect("top", yt, -0.05, 0.05, -0.25, 0.25, rng=0.25, points=[(0.0, yt, 0.15)])
        P.dim("footprint_w", 1.2, 1.2, tol=0.01)
        P.notes.append("6-stack 1.2 x 0.75: along walls only; the back ends face the wall")
    return P


def kamasu_bag(wear=None, sag=0.0, vis=(1,)):
    s = pillow(0.60, 0.40, 0.15, MUSHIRO, nx=4, nz=3, pinch=0.2, wear=wear, vis=vis, sag=sag)
    # the sewn seam along one edge (straw rope)
    seam = W(-0.30, 0.30, 0.0, 0.035, 0.195, 0.205, ROPE, vis=(1,))
    if wear:
        seam.wear = wear
    return [s, seam]


def kamasu(state="1"):
    P = FPart("kamasu", budget="small", mass=30.0 if state != "stack3" else 90.0)
    if state == "stack3":
        bag_cols = []
        for i, (dx, dz, yaw) in enumerate(((0.0, 0.0, 0.0), (0.03, -0.02, 7.0), (-0.02, 0.02, -5.0))):
            add_all(P, xfs(kamasu_bag(), ry=yaw, t=(dx, i * 0.14, dz)))
            bag_cols.append(P.add(fkit.col_solid(xf(box(-0.29, 0.29, 0.0, 0.14, -0.19, 0.19, MUSHIRO), ry=yaw,
                                                    t=(dx, i * 0.14, dz)))))
        fkit.road_tops(P, bag_cols, "tatami")      # F1: the top bag
        P.add(W(-0.3, 0.3, 0.0, 0.43, -0.2, 0.2, MUSHIRO, vis=(2,)))
        top = 2 * 0.14 + 0.15
        P.loot_rect("top", top, -0.1, 0.1, -0.06, 0.06, rng=0.25, points=[(-0.02, top, 0.02)])
    else:
        burst = state == "burst"
        add_all(P, kamasu_bag("_w2" if burst else None, sag=0.05 if burst else 0.0))
        P.add(W(-0.3, 0.3, 0.0, 0.14, -0.2, 0.2, MUSHIRO, vis=(2,)))
        P.add(col(-0.29, 0.29, 0.0, 0.12 if burst else 0.14, -0.19, 0.19, MUSHIRO))
        if burst:
            P.add(mound(21, 0.10, 0.38, 0.22, 0.035, PAPER, sx=1.3, wear="_w0"))
            P.add(stain(22, 0.05, 0.35, 0.40, sx=1.4, wear="_w2"))
        else:
            P.loot_rect("top", 0.15, -0.1, 0.1, -0.05, 0.05, rng=0.25, points=[(0.0, 0.15, 0.0)])
    P.dim("w", 0.60, 0.60, tol=0.01)
    return P


# ================================================================================================ rack
RACK_Y = (0.10, 0.70, 1.25)
RD, RH = 0.45, 1.80


def rack(width=1.82, state="intact"):
    P = FPart("rack", budget="furniture", res3=True, mass=25.0 if width > 1 else 14.0)
    ab = state != "intact"
    x0, x1 = -width / 2, width / 2
    z0, z1 = -RD / 2, RD / 2
    ps = 0.06
    xs = [x0 + ps / 2, x1 - ps / 2] + ([0.0] if width > 1 else [])
    for x in xs:
        for z in (z0 + ps / 2, z1 - ps / 2):
            P.add(W(x - ps / 2, x + ps / 2, 0.0, RH, z - ps / 2, z + ps / 2, vis=(1, 2)))
            P.add(col(x - ps / 2, x + ps / 2, 0.0, RH, z - ps / 2, z + ps / 2))
        # side rails under each board + top
        for y in RACK_Y + (RH - 0.04,):
            P.add(W(x - 0.025, x + 0.025, y - 0.065, y - 0.02, z0 + ps, z1 - ps, vis=(1,)))
    for y in (0.40, 1.55):          # back rails
        P.add(W(x0 + ps, x1 - ps, y, y + 0.05, z0, z0 + 0.03, vis=(1,)))
    P.add(W(x0 + ps, x1 - ps, RH - 0.05, RH, z1 - 0.05, z1, vis=(1,)))          # front top rail
    collapse = 1 if ab else None
    for bi, y in enumerate(RACK_Y):
        bd = board(x0 + 0.005, x1 - 0.005, y - 0.02, y, z0 + 0.005, z1 - 0.005, k=bi * 3, vis=(1, 2))
        cb = col(x0 + 0.01, x1 - 0.01, y - 0.02, y, z0 + ps, z1 - ps)
        if bi == collapse:
            # one board down at an angle: its left end dropped onto the board below
            drop = y - RACK_Y[bi - 1] - 0.055
            ang = math.degrees(math.asin(min(0.95, drop / (width - 0.1))))
            piv = (x1 - 0.05, y, 0.0)
            bd, cb = xf(bd, rz=ang, pivot=piv), xf(cb, rz=ang, pivot=piv)
            bd.wear = "_w2"
            P.add(bd)
            P.add(cb)
            continue
        P.add(bd)
        P.add(cb)
        per = 2 if width > 1 else 1
        pts = [(x0 + (i + 0.5) * width / per, y, 0.0) for i in range(per)]
        if not ab and bi == 2:
            pts = [(p[0] + (0.25 if p[0] < 0 else -0.25), p[1], p[2]) for p in pts] if width > 1 else                 [(0.15, y, 0.0)]
        if not ab and bi == 0 and width < 1:
            pts = [(-0.15, y, 0.0)]
        P.loot_rect("board_%d" % (bi + 1), y, x0 + 0.05, x1 - 0.05, z0 + 0.05, z1 - 0.05, rng=0.2 if per == 1 else 0.25,
                    points=pts)
    for y in RACK_Y:
        P.add(W(x0, x1, y - 0.02, y, z0, z1, vis=(3,)))
    for x in (x0 + 0.03, x1 - 0.03):
        P.add(W(x - 0.03, x + 0.03, 0.0, RH, z0, z1, vis=(3,)))
    # goods: boxes and jars at the board ends (the middle stays free for loot)
    if not ab:
        js, _ = bits.jar(0.30, 0.40, DARK, n=8, lid=True, vis=(1,))
        add_all(P, xfs(js[:2], t=(x1 - 0.22, RACK_Y[0], 0.0)))
        if width > 1:
            ss, _ = hako("m", k=3)
            add_all(P, xfs(ss, t=(x0 + 0.30, RACK_Y[2], 0.0)))
            ss, _ = hako("s", k=5, cord=True)
            add_all(P, xfs(ss, ry=10.0, t=(x0 + 0.30, RACK_Y[2] + 0.25, 0.0)))
            js, _ = bits.jar(0.18, 0.22, PALE, n=8, lid=True, vis=(1,))
            add_all(P, xfs(js[:2], t=(x1 - 0.25, RACK_Y[2], 0.05)))
        else:
            ss, _ = hako("s", k=5, cord=True)
            add_all(P, xfs(ss, ry=10.0, t=(x0 + 0.22, RACK_Y[2], 0.0)))
    else:
        # what fell: a box on its side and a broken jar on the floor in front
        ss, _ = hako("m", open_body=True, lid=False, wear="_w2")
        add_all(P, rest(xfs(ss, rx=90.0, ry=20.0, t=(x0 + 0.35, 0.0, z1 + 0.30))))
        add_all(P, shards(55, x1 - 0.35, z1 + 0.25, 0.2, 7, DARK, size=(0.04, 0.10), wear="_w2"))
        P.add(stain(56, x1 - 0.3, z1 + 0.3, 0.35, sx=1.3))
        P.add(col(x0 + 0.13, x0 + 0.58, 0.0, 0.30, z1 + 0.14, z1 + 0.46))
    P.dim("width", width, width, tol=0.005)
    P.dim("depth", RD, RD, tol=0.005)
    P.dim("height", RH, RH, tol=0.005)
    P.notes.append("0.45 deep, along walls only; loot points on each board (the vanilla lootshelves pattern)")
    return P


# ================================================================================================ registry
def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_nagamochi", "cat": CAT, "models": [
        M("jp_f_nagamochi", "shut", "intact", "Long chest (nagamochi)", lambda: nagamochi("shut")),
        M("jp_f_nagamochi_open", "shut", "open", "Long chest, lid thrown back, cloth spilling",
          lambda: nagamochi("open")),
    ]},
    tansu.PROP,
    {"id": "jp_f_kori", "cat": CAT, "models": [
        M("jp_f_kori", "1", "intact", "Wicker trunk (kori)", lambda: kori("1")),
        M("jp_f_kori_2", "2", "intact", "Wicker trunks, stack of two", lambda: kori("2")),
        M("jp_f_kori_open", "1", "open", "Wicker trunk, lid off, garment out", lambda: kori("open")),
    ]},
    {"id": "jp_f_box", "cat": CAT, "models": [
        M("jp_f_box_s", "s", "intact", "Wooden box, small", lambda: hako_model("s")),
        M("jp_f_box_m", "m", "intact", "Wooden box, medium", lambda: hako_model("m")),
        M("jp_f_box_l", "l", "intact", "Wooden box, large", lambda: hako_model("l")),
        M("jp_f_box_stack3", "stack3", "intact", "Wooden boxes, stack of three", lambda: hako_stack("intact")),
        M("jp_f_box_s_lacquer", "s_lacquer", "intact", "Lacquered box, small (T3)", lambda: hako_model("s", mat=LACQUER)),
        M("jp_f_box_m_lacquer", "m_lacquer", "intact", "Lacquered box, medium (T3)",
          lambda: hako_model("m", mat=LACQUER)),
        M("jp_f_box_open", "l", "open", "Wooden box, lid off, spilled", lambda: hako_model("l", "open")),
        M("jp_f_box_stack3_toppled", "stack3", "toppled", "Box stack, small box knocked off",
          lambda: hako_stack("toppled")),
    ]},
    {"id": "jp_f_tawara", "cat": CAT, "notes": ["rice/salt spills use jp_m_paper_shoji (_w0) as the pale grain: "
                                                "no grain material in the library"], "models": [
        M("jp_f_tawara", "1", "intact", "Straw rice bale (tawara)", lambda: tawara("1")),
        M("jp_f_tawara_burst", "1", "burst", "Rice bale, burst, rice spilled", lambda: tawara("burst")),
        M("jp_f_tawara_stack6", "stack6", "intact", "Rice bales, pyramid of six", lambda: tawara("stack6")),
        M("jp_f_tawara_stack6_burst", "stack6", "burst", "Rice bales, top one burst", lambda: tawara("stack6_burst")),
        M("jp_f_tawara_kamasu", "kamasu", "intact", "Straw bag (kamasu)", lambda: kamasu("1")),
        M("jp_f_tawara_kamasu_stack3", "kamasu", "intact", "Straw bags, stack of three", lambda: kamasu("stack3")),
        M("jp_f_tawara_kamasu_burst", "kamasu", "burst", "Straw bag, split and slumped", lambda: kamasu("burst")),
    ]},
    {"id": "jp_f_rack", "cat": CAT, "models": [
        M("jp_f_rack_1ken", "1ken", "intact", "Board shelving 1.82 m (kura shelves)", lambda: rack(1.82)),
        M("jp_f_rack_1ken_collapsed", "1ken", "collapsed", "Board shelving 1.82 m, board down, goods on the floor",
          lambda: rack(1.82, "collapsed")),
        M("jp_f_rack_half", "half", "intact", "Board shelving 0.91 m", lambda: rack(0.91)),
        M("jp_f_rack_half_collapsed", "half", "collapsed", "Board shelving 0.91 m, board down",
          lambda: rack(0.91, "collapsed")),
    ]},
]
