"""s1kit - the S1 shop-set kit: L1's lkit (B3a fkit + bits, B3b skit), imported read-only, plus what the shop sets
add: the shop text atlas (jp_m_decal_sumi_text_shop) with correctly faced text, the hanging kanban builder, goods
helpers (bowls, stacks, packets, skewers) and the M() model spec with mounts.

Frames (B3a fkit.py; the sidecar 'anchor'):
  'floor'  base centre on the supporting surface (floor, stand step, shelf board)
  'wall'   origin on the floor / ground below; the wall or FACADE face is z = 0, the prop at +z; heights built in
  'hang'   origin at the beam underside, the prop hangs down (-y)
Text: DayZ model space is left-handed. stext() lays a decal on a plane given (right, up) as the READER sees it; the
quad faces out along right x up (component formula) and +u runs to the reader's right (the L2 TXT check,
spikes/L2/textface.py, verifies every model).
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
import lkit  # noqa: E402
from lkit import (core, box, prism, ngon, sheet, Solid, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col,  # noqa
                  lcyl, rest, auto_smooth, rotated_box, board, FPart, LPart, disc, stain, shards, mound, pillow,
                  rope_ring, soft_slab, blob, pole, beam, rope_path, sag, grid_sheet, hull3, hull_col, bipyramid,
                  lod_box, wear_all, only_vis, place_group, cord, peg, rng,
                  WOOD, WEATH, SOOTW, IRON, PALE, DARK, LACQ, BAMBOO, SOOTB, WEAVE, MUSHIRO, TAWARA, ROPE, STACK,
                  PAPER, FUSUMA, CHOCHIN, INDIGO, KINARI, KINARI_CUT, NOREN, RED, ASH, LEAF, LITTER, STONE, CUT, SUMI,
                  LIFE, RICE, KAKI, KAYA)
import skit  # noqa: E402

SHOP = "decal_sumi_text_shop"       # S1 atlas (research/materials/make_s1_materials.py)
SHU = "lacquer_shu"                 # S1
PORC = "ceramic_porcelain"          # S1
LEATHER = "leather_tan"             # S1
TOFU = "food_tofu"                  # S1
FOLIAGE = "plant_foliage"           # L2 (alpha cut leaves / needles)
ENDG = "wood_endgrain"
FISH = WEATH                        # salt / dried fish: the weathered wood brown (as L1's mezashi)


def M(p3d, variant, state, display, fn, **kw):
    d = {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}
    d.update(kw)
    return d


def SP(name, budget="small", res3=False, mass=2.0, anchor="floor", flat=False, wear="_w1"):
    return LPart(name, budget=budget, res3=res3, mass=mass, anchor=anchor, flat=flat, wear=wear)


# ------------------------------------------------------------------------------------------------ text
def stext(center, right, up, h, cellname, mat=SHOP, wear=None, off=0.002, vis=(1,), width=None, crop=None):
    """A text / picture decal on a plane the reader sees with `right` to his right and `up` up: faces out along
    right x up (component formula), u runs to the reader's right (skit.text_ok's result for any atlas)."""
    s = skit.text_on(center, right, up, h, mat, cellname, wear=wear, off=off, vis=vis, width=width, crop=crop)
    s.finalize()
    us = [a for f in s.fuv for a, _ in f]
    lo, hi = min(us), max(us)
    s.fuv = [[(lo + hi - a, b) for a, b in f] for f in s.fuv]
    s.fn = [core.mul(n, -1.0) for n in s.fn]
    if s.normals is not None:
        s.normals = s.fn
    s._text_faced = True
    return s


def cell_aspect(cellname, mat=SHOP):
    w, h = skit.cell_size(mat, cellname)
    return w / h


# ------------------------------------------------------------------------------------------------ small goods
def bowl(cx, cz, r, h, mat, y0=0.0, n=8, vis=(1,), wear=None, foot=True):
    """An open bowl (outside, rim, inside to a flat bottom), smooth normals."""
    prof = [(0.0, y0), (r * 0.45, y0), (r * 0.5, y0 + 0.01), (r, y0 + h), (r - 0.006, y0 + h), (r * 0.42, y0 + 0.016),
            (0.0, y0 + 0.016)] if foot else [(0.0, y0), (r * 0.6, y0), (r, y0 + h), (r - 0.006, y0 + h),
                                             (0.0, y0 + 0.01)]
    s = lathe(prof, n, mat, vis=vis, wear=wear)
    return xf(s, t=(cx, 0.0, cz))


def bowl_stack(cx, cz, r, h, k, mat, y0=0.0, n=8, vis=(1,), wear=None):
    """k nested bowls read as one stepped column (a closed lathe: cheap)."""
    prof = [(0.0, y0), (r * 0.5, y0)]
    y = y0
    for i in range(k):
        prof += [(r * 0.55, y + 0.005), (r, y + h * 0.75)]
        y += h * 0.35
    prof += [(r, y + h * 0.42), (r - 0.006, y + h * 0.42), (0.0, y + h * 0.3)]
    s = lathe(prof, n, mat, vis=vis, wear=wear)
    return xf(s, t=(cx, 0.0, cz))


def dish_stack(cx, cz, r, k, mat, y0=0.0, n=8, vis=(1,), wear=None, t=0.012):
    prof = [(0.0, y0), (r * 0.7, y0), (r, y0 + t * 0.6), (r, y0 + t * k), (0.0, y0 + t * k)]
    return xf(lathe(prof, n, mat, vis=vis, wear=wear), t=(cx, 0.0, cz))


def jug(cx, cz, r, h, mat, y0=0.0, n=8, vis=(1,), wear=None):
    """A closed bottle / oil jug (tokkuri form): belly, neck, lip."""
    prof = [(0.0, y0), (r * 0.7, y0), (r, y0 + h * 0.35), (r * 0.9, y0 + h * 0.6), (r * 0.3, y0 + h * 0.82),
            (r * 0.28, y0 + h * 0.95), (r * 0.36, y0 + h), (0.0, y0 + h)]
    return xf(lathe(prof, n, mat, vis=vis, wear=wear), t=(cx, 0.0, cz))


def packet(cx, cz, w, d, h, mat=PAPER, ry=0.0, y0=0.0, wear=None, vis=(1,)):
    s = W(-w / 2, w / 2, y0, y0 + h, -d / 2, d / 2, mat, vis=vis)
    if wear:
        s.wear = wear
    return xf(s, ry=ry, t=(cx, 0.0, cz))


def tray(cx, cz, w, d, mat=LACQ, y0=0.0, h=0.025, ry=0.0, vis=(1,), wear=None):
    """A shallow tray: a bottom and four low rims (5 boxes)."""
    t = 0.008
    out = [W(-w / 2, w / 2, y0, y0 + 0.006, -d / 2, d / 2, mat, vis=vis),
           W(-w / 2, w / 2, y0, y0 + h, d / 2 - t, d / 2, mat, vis=vis),
           W(-w / 2, w / 2, y0, y0 + h, -d / 2, -d / 2 + t, mat, vis=vis),
           W(-w / 2, -w / 2 + t, y0, y0 + h, -d / 2 + t, d / 2 - t, mat, vis=vis),
           W(w / 2 - t, w / 2, y0, y0 + h, -d / 2 + t, d / 2 - t, mat, vis=vis)]
    return [xf(wear_all([s], wear)[0], ry=ry, t=(cx, 0.0, cz)) for s in out]


def skewer(p0, p1, r=0.002, vis=(1,)):
    return pole(p0, p1, r, BAMBOO, n=3, vis=vis)


def ball(c, r, mat, n=6, vis=(1,), wear=None, sy=1.0):
    """A small closed round lump (mochi, dango, a fruit): a lathe sphere."""
    prof = [(0.0, -r * sy)] + [(r * math.sin(math.pi * k / 4), -r * sy * math.cos(math.pi * k / 4)) for k in (1, 2, 3)] \
        + [(0.0, r * sy)]
    return xf(lathe(prof, n, mat, vis=vis, wear=wear), t=c)


def garment_folded(cx, cz, w=0.30, d=0.22, h=0.04, mat=INDIGO, ry=0.0, y0=0.0, wear=None, collar=KINARI):
    """A folded kimono: a soft slab with the collar band across one end."""
    out = [W(-w / 2, w / 2, y0, y0 + h, -d / 2, d / 2, mat, vis=(1,)),
           W(-w / 2 + 0.02, w / 2 - 0.02, y0 + h, y0 + h + 0.004, d / 2 - 0.05, d / 2 - 0.02, collar, vis=(1,))]
    return [xf(s, ry=ry, t=(cx, 0.0, cz)) for s in wear_all(out, wear)]


def kimono_t(cx, cy, cz, mat=INDIGO, wear=None, w_sl=1.20, body_w=0.60, body_h=1.25, sleeve_h=0.45, ry=0.0):
    """A kimono hung by its sleeves on a pole (T shape, two-sided thin slabs, the pole along x at y = cy)."""
    t = 0.006
    out = [W(-w_sl / 2, w_sl / 2, cy - sleeve_h, cy, -t, t, mat, vis=(1, 2)),
           W(-body_w / 2, body_w / 2, cy - body_h, cy - sleeve_h, -t, t, mat, vis=(1, 2)),
           W(-0.06, 0.06, cy - 0.55, cy, t, t + 0.004, KINARI, vis=(1,))]
    return [xf(s, ry=ry, t=(cx, 0.0, cz)) for s in wear_all(out, wear)]


# ------------------------------------------------------------------------------------------------ kanban
KB_W, KB_H, KB_T = 0.30, 0.90, 0.03       # hanging board
ARM_Y = 2.72                              # bracket arm under a townhouse eave (B3b shopfront_kanban_hang: 2.75 hang_y)
ARM_L = 0.55


def kanban_parts(cell, mat_text=SHOP, wear=None, text_wear=None, board_mat=WOOD, roof=True):
    """A hanging signboard (sage-kanban) perpendicular to the facade: an L bracket (wall plate + arm along +z) and the
    board hung on two cords from the arm, text on BOTH faces (read from either way along the street). Frame: facade
    plane z = 0, y = 0 at the wall foot. Returns (solids, board solids for the askew state, board centre)."""
    out = [W(-0.04, 0.04, ARM_Y - 0.30, ARM_Y + 0.06, 0.0, 0.03, WEATH, vis=(1, 2)),           # wall plate
           W(-0.025, 0.025, ARM_Y, ARM_Y + 0.05, 0.03, 0.03 + ARM_L, WEATH, vis=(1, 2)),       # arm
           pole((0.0, ARM_Y - 0.25, 0.035), (0.0, ARM_Y, 0.30), 0.012, WEATH, n=4, vis=(1,))]  # brace
    zc = 0.03 + ARM_L / 2 + 0.02
    top = ARM_Y - 0.10
    brd = [W(-KB_T / 2, KB_T / 2, top - KB_H, top, zc - KB_W / 2, zc + KB_W / 2, board_mat, vis=(1, 2))]
    if roof:                                                                                   # the little cap board
        brd.append(W(-KB_T / 2 - 0.02, KB_T / 2 + 0.02, top, top + 0.02, zc - KB_W / 2 - 0.02, zc + KB_W / 2 + 0.02,
                     WEATH, vis=(1,)))
    for dz in (-0.09, 0.09):
        brd.append(cord((0.0, ARM_Y, zc + dz), (0.0, top + 0.02, zc + dz), 0.004))
    asp = cell_aspect(cell, mat_text)
    th = KB_H * 0.86
    tw = min(KB_W * 0.86, th * asp)
    th = tw / asp
    for sx in (-1, 1):            # +x face read with the facade on the reader's left... both faces: right = -/+z
        right = (0.0, 0.0, -1.0) if sx > 0 else (0.0, 0.0, 1.0)
        brd.append(stext((sx * KB_T / 2, top - KB_H / 2, zc), right, (0.0, 1.0, 0.0), th, cell, mat_text,
                         wear=text_wear or wear, width=tw))
    wear_all(out, wear)
    wear_all([s for s in brd if not getattr(s, "_text_faced", False)], wear)
    return out, brd, (0.0, top - KB_H / 2, zc)


def kanban(cell, state="hang", mat_text=SHOP):
    """jp_f_kanban_<trade>: 'hang' as left in use; 'askew' hanging from one cord, swung round, text faded (_w2)."""
    P = SP("kanban", budget="small", mass=4.0, anchor="wall", flat=True)
    if state == "hang":
        out, brd, c = kanban_parts(cell, mat_text)
        P.adds(out + brd)
    else:
        out, brd, c = kanban_parts(cell, mat_text, wear="_w2", text_wear="_w2")
        P.adds(out)
        # one cord gone: the board pivots on the remaining cord's top corner and swings out of plumb
        piv = (0.0, ARM_Y - 0.10, c[2] + 0.09)
        keep = [s for s in brd if not (isinstance(s.mats, str) and s.mats == ROPE and s.bbox()[4] < c[2])]
        P.adds([xf(s, rx=-22.0, ry=0.0, rz=8.0, pivot=piv) for s in keep])
    P.add(lod_box([s for s in P.solids if 1 in s.vis and not getattr(s, "_text_faced", False)], WEATH, vis=(2,)))
    P.dim("board_h", KB_H, KB_H)
    P.notes.append("hanging signboard on a bracket under the eave (front proxy, facade plane z = 0); text both faces")
    P.extra["hang_y"] = ARM_Y + 0.05
    return P


def kanban_prop(key, cell, display, trades, mat=SHOP, era=None):
    """PROPS entry for one trade's hanging sign: intact + askew (one cord gone, text faded)."""
    return {"id": "jp_f_kanban_" + key, "cat": "shopsign", "mount": "wall", "trades": list(trades),
            "era": era or "shop kanban: the standard shop-front kit (B_TRADE_INDUSTRY 41)", "models": [
                M("jp_f_kanban_" + key, key, "intact", "Hanging signboard: %s" % display,
                  lambda c=cell, m=mat: kanban(c, "hang", m)),
                M("jp_f_kanban_" + key + "_askew", key, "askew", "Hanging signboard (%s), one cord gone, faded" % display,
                  lambda c=cell, m=mat: kanban(c, "askew", m)),
            ]}


def finish_goods(P, mat=WOOD, note=None):
    """Close a visual-only goods cluster: a Res 2 box round it and the dressing note."""
    P.add(lod_box([s for s in P.solids if 1 in s.vis], mat, vis=(2,)))
    P.notes.append(note or "dressing only (mount surface: a stand step, shelf board or the floor); loot lies around it")
    return P


def furn_lods(P, mat=WOOD):
    """Res 2 and Res 3 stand-ins for a furniture piece: one box each (Res 2 keeps the outline, Res 3 a block)."""
    vis1 = [s for s in P.solids if 1 in s.vis and not getattr(s, "_text_faced", False)]
    P.add(lod_box(vis1, mat, vis=(3,)))
    return P
