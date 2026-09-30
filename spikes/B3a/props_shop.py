"""Office and shop props (BUILD_LIST rows 39-43): zukue, choba_goshi, misedana, goods_general."""
import math
import random

import fkit
import bits
from fkit import (core, box, sheet, lathe, xf, xfs, flat_poly, W, col, board, FPart, rest,
                  WOOD, IRON, PAPER, INDIGO, KINARI, MUSHIRO, LACQUER, LITTER)
from bits import stain
from props_heat import open_bar
from props_storage import papers

CAT = "shop"
ROPE = "straw_rope"


def add_all(P, ss):
    for s in ss:
        P.add(s)


# ================================================================================================ zukue
ZW, ZD, ZH = 0.90, 0.40, 0.33


def ledger(open_=False, wear=None):
    """Account book (daifukucho): a thick paper block with an indigo cover; open = two page spreads flat."""
    if not open_:
        out = [W(-0.12, 0.12, 0.0, 0.03, -0.085, 0.085, PAPER, vis=(1,)),
               W(-0.122, 0.122, 0.03, 0.034, -0.087, 0.087, INDIGO, vis=(1,))]
    else:
        out = [W(-0.24, 0.0, 0.0, 0.006, -0.085, 0.085, PAPER, vis=(1,)),
               W(0.0, 0.24, 0.0, 0.006, -0.085, 0.085, PAPER, vis=(1,)),
               W(-0.245, 0.245, -0.003, 0.0, -0.088, 0.088, INDIGO, vis=(1,))]
    for s in out:
        if wear:
            s.wear = wear
    return out


def inkbox(wear=None):
    """Suzuri-bako: a lacquered box 0.22 x 0.12 x 0.04 with its lid."""
    out = [W(-0.11, 0.11, 0.0, 0.04, -0.06, 0.06, LACQUER, vis=(1,))]
    if wear:
        out[0].wear = wear
    return out


def zukue_parts(kind="choba"):
    out = []
    t = 0.025
    out.append(board(-ZW / 2, ZW / 2, ZH - 0.03, ZH, -ZD / 2, ZD / 2, k=4, vis=(1, 2)))
    for sx in (-1, 1):
        x = sx * (ZW / 2 - 0.04)
        out.append(board(x - t / 2, x + t / 2, 0.03, ZH - 0.03, -ZD / 2 + 0.02, ZD / 2 - 0.02, k=6 + sx, vis=(1, 2)))
        out.append(board(x - 0.03, x + 0.03, 0.0, 0.03, -ZD / 2, ZD / 2, k=2, vis=(1,)))          # foot
    if kind == "choba":
        # back apron and the shallow drawer under the top
        out.append(W(-ZW / 2 + 0.055, ZW / 2 - 0.055, ZH - 0.10, ZH - 0.03, -ZD / 2 + 0.02, -ZD / 2 + 0.035, vis=(1,)))
        out.append(board(-0.30, 0.30, ZH - 0.09, ZH - 0.035, ZD / 2 - 0.03, ZD / 2 - 0.012, k=9, vis=(1,)))
        out.append(W(-0.30, 0.30, ZH - 0.095, ZH - 0.09, -ZD / 2 + 0.035, ZD / 2 - 0.03, vis=(1,)))
        out.append(box(-0.018, 0.018, ZH - 0.068, ZH - 0.058, ZD / 2 - 0.012, ZD / 2 - 0.004, IRON, vis=(1,)))
    else:
        # writing desk: turned-up end rails on the top (fude-gaeshi)
        for sx in (-1, 1):
            out.append(W(sx * ZW / 2 - (0.02 if sx > 0 else 0.0), sx * ZW / 2 + (0.02 if sx < 0 else 0.0), ZH, ZH + 0.018,
                         -ZD / 2, ZD / 2, vis=(1,)))
    out.append(W(-ZW / 2, ZW / 2, 0.0, ZH, -ZD / 2, ZD / 2, vis=(3,)))
    return out


def zukue(kind="choba", state="intact"):
    P = FPart("zukue", budget="small", res3=False, mass=8.0)
    parts = [s for s in zukue_parts(kind) if 3 not in s.vis]
    if state == "intact":
        add_all(P, parts)
        add_all(P, xfs(ledger(), ry=-8.0, t=(-0.22, ZH, 0.02)))
        add_all(P, xfs(inkbox(), ry=4.0, t=(0.28, ZH, -0.08)))
        P.add(col(-ZW / 2, ZW / 2, ZH - 0.03, ZH, -ZD / 2, ZD / 2))
        for sx in (-1, 1):
            x = sx * (ZW / 2 - 0.04)
            P.add(col(x - 0.03, x + 0.03, 0.0, ZH - 0.03, -ZD / 2, ZD / 2))
        P.loot_rect("top", ZH, -0.05, 0.40, -0.15, 0.15, rng=0.25, points=[(0.12, ZH, 0.08)])
    else:
        # on its side (top to the back), the ledger open and scattered, ink box upset with an ink stain
        tp = rest(xfs(parts, rx=-90.0, ry=12.0))
        add_all(P, tp)
        c = [xf(xf(box(-ZW / 2, ZW / 2, 0.0, ZH, -ZD / 2, ZD / 2, WOOD), rx=-90.0), ry=12.0)]
        lo = min(v[1] for v in c[0].verts)
        P.add(fkit.col_solid(xf(c[0], t=(0.0, -lo, 0.0))))
        add_all(P, xfs(ledger(open_=True, wear="_w2"), ry=25.0, t=(-0.15, 0.003, 0.45)))
        add_all(P, rest(xfs(inkbox("_w2"), rz=100.0, ry=-30.0, t=(0.35, 0.0, 0.40))))
        P.add(stain(101, 0.30, 0.52, 0.16, sx=1.5, wear="_w2"))
        add_all(P, papers(102, 0.0, 0.70, 3, 0.2))
    P.dim("w", ZW, ZW, tol=0.005)
    P.dim("h", ZH, ZH, tol=0.005)
    return P


# ================================================================================================ choba-goshi
GH = 0.50          # height
GW = 0.75          # panel width


def lattice_panel(w=GW, h=GH, bars=13, wear=None):
    """One fold: stiles, top and bottom rails, vertical koshi bars (open bars), in the panel's own frame:
    x along the panel from 0 to w, z = 0 its centre plane, base on y = 0."""
    out = [W(0.0, 0.025, 0.0, h, -0.0125, 0.0125, vis=(1, 2)), W(w - 0.025, w, 0.0, h, -0.0125, 0.0125, vis=(1, 2)),
           W(0.025, w - 0.025, h - 0.03, h, -0.0125, 0.0125, vis=(1, 2)),
           W(0.025, w - 0.025, 0.02, 0.06, -0.0125, 0.0125, vis=(1, 2))]
    sp = (w - 0.05) / (bars + 1)
    for i in range(bars):
        x = 0.025 + sp * (i + 1)
        out.append(open_bar(x - 0.006, x + 0.006, 0.06, h - 0.03, -0.007, 0.007))
    out.append(W(0.0, w, 0.0, h, -0.004, 0.004, WOOD, vis=(2,)))
    for s in out:
        if wear:
            s.wear = wear
    return out


def choba_goshi(folds=3, state="intact"):
    """Folding low lattice fencing the desk corner: 3 folds = a U (side, front, side), 2 folds = an L.
    Origin = the centre of the front fold's line on the floor, +z towards the customers."""
    P = FPart("choba_goshi", budget="small", mass=6.0 if folds == 3 else 4.0)
    knocked = state != "intact"
    wear = "_w2" if knocked else None
    # front fold along x, centred; side folds run back (-z) from its ends, hinged 1 mm apart
    front = xfs(lattice_panel(wear=wear), t=(-GW / 2, 0.0, 0.0))
    add_all(P, front)
    P.add(col(-GW / 2, GW / 2, 0.0, GH, -0.0125, 0.0125))
    sides = [(-1, "l"), (1, "r")] if folds == 3 else [(1, "r")]
    for sx, _ in sides:
        x = sx * (GW / 2 + 0.0135)
        pan = lattice_panel(wear=wear)
        if knocked and sx == 1:
            # this fold knocked flat: lying on the floor behind its hinge
            flat = xfs(pan, rx=90.0)                                   # up (+y) -> front (+z); lying face up
            flat = xfs(flat, ry=90.0, t=(x, 0.0125, -0.02))
            add_all(P, rest(flat, 0.0))
            continue
        add_all(P, xfs(pan, ry=90.0, t=(x, 0.0, -0.0135)))
        P.add(fkit.col_solid(xf(box(0.0, GW, 0.0, GH, -0.0125, 0.0125, WOOD), ry=90.0, t=(x, 0.0, -0.0135))))
    P.dim("h", GH, GH, tol=0.005)
    P.dim("fold_w", GW, GW, tol=0.005)
    P.notes.append("low (0.5): walkable around; keep it out of the door-to-door band")
    return P


# ================================================================================================ misedana
MS_D, MS_H = 0.60, 0.45
RISE, TREAD = 0.15, 0.20


def misedana_parts(width, steps=3):
    out = []
    x0, x1 = -width / 2, width / 2
    t = 0.02
    for i in range(steps):
        y = RISE * (i + 1)
        zf = MS_D / 2 - TREAD * i                  # front edge of this step
        out.append(board(x0, x1, y - t, y, zf - TREAD, zf, k=i * 2, vis=(1, 2)))            # tread
        out.append(board(x0, x1, y - RISE, y - t, zf - t, zf, k=i * 2 + 1, vis=(1,)))       # riser
    # side boards: stepped, as one board per step band (convex pieces)
    xs = [x0 + 0.01, x1 - 0.01] + ([0.0] if width > 1.2 else [])
    for x in xs:
        for i in range(steps):
            zf = MS_D / 2 - TREAD * i
            out.append(W(x - 0.01, x + 0.01, 0.0, RISE * (i + 1) - t, -MS_D / 2, zf - t, vis=(1,)))
    out.append(W(x0, x1, 0.0, MS_H - t, -MS_D / 2, -MS_D / 2 + t, vis=(1, 2)))         # back board
    # Res 3: three blocks
    for i in range(steps):
        zf = MS_D / 2 - TREAD * i
        out.append(W(x0, x1, 0.0, RISE * (i + 1), zf - TREAD, zf, vis=(3,)))
    return out


def misedana(width=1.82, state="intact"):
    P = FPart("misedana", budget="small", res3=True, mass=12.0 if width > 1 else 7.0)
    x0, x1 = -width / 2, width / 2
    parts = misedana_parts(width)
    cols = []
    for i in range(3):
        zf = MS_D / 2 - TREAD * i
        cols.append(box(x0, x1, 0.0, RISE * (i + 1), zf - TREAD, zf, WOOD))
    if state == "intact":
        add_all(P, parts)
        for c in cols:
            P.add(fkit.col_solid(c))
        per = 2 if width > 1.2 else 1
        for i in range(3):
            y = RISE * (i + 1)
            zc = MS_D / 2 - TREAD * i - TREAD / 2
            pts = [(x0 + width * (k + 0.5) / per, y, zc) for k in range(per)]
            P.loot_rect("step_%d" % (i + 1), y, x0 + 0.05, x1 - 0.05, zc - 0.07, zc + 0.07, rng=0.15, points=pts)
    else:
        # toppled forward: pivots on the front bottom edge, lies on its face with the back board up
        tp = xfs(parts, rx=90.0, pivot=(0.0, 0.0, MS_D / 2))
        tp = rest(xfs(tp, ry=6.0))
        add_all(P, tp)
        c = xf(xf(box(x0, x1, 0.0, MS_H, -MS_D / 2, MS_D / 2, WOOD), rx=90.0, pivot=(0.0, 0.0, MS_D / 2)), ry=6.0)
        lo = min(v[1] for v in c.verts)
        P.add(fkit.col_solid(xf(c, t=(0.0, -lo, 0.0))))
    P.dim("w", width, width, tol=0.005)
    P.dim("d", MS_D, MS_D, tol=0.005)
    P.dim("h", MS_H, MS_H, tol=0.005)
    P.notes.append("only on the display strip, never in the door band")
    return P


# ================================================================================================ goods (general)
def bolt(L=0.36, d=0.10, mat=INDIGO, wear=None):
    """A tan of cloth rolled: a 6-sided roll along x with a paper band."""
    s = fkit.lcyl("x", d / 2 + 0.003, 0.0, d / 2, -L / 2, L / 2, mat, n=6, vis=(1,), phase=0.0)
    fkit.auto_smooth(s, 70.0)
    b = fkit.lcyl("x", d / 2 + 0.003, 0.0, d / 2 + 0.003, -0.03, 0.03, PAPER, n=6, vis=(1,), phase=0.0)
    for x in (s, b):
        if wear:
            x.wear = wear
    return [s, b]


def paper_bundle(w=0.25, d=0.18, h=0.08, wear=None):
    out = [W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, PAPER, vis=(1,)),
           W(-0.006, 0.006, 0.0, h + 0.003, -d / 2 - 0.003, d / 2 + 0.003, ROPE, vis=(1,))]
    for s in out:
        if wear:
            s.wear = wear
    return out


def sandals(wear=None):
    """A pair of straw sandals (waraji) tied: two flat soles 0.24 x 0.09, a cord."""
    out = []
    for dz in (-0.05, 0.05):
        s = fkit.prism(fkit.ngon(0.0, dz, 0.045, 8, 0.0, rx=0.12), "y", 0.0, 0.018, MUSHIRO, vis=(1,))
        out.append(s)
    out.append(W(-0.004, 0.004, 0.0, 0.03, -0.10, 0.10, ROPE, vis=(1,)))
    for s in out:
        if wear:
            s.wear = wear
    return out


def package(w=0.20, d=0.16, h=0.10, mat=KINARI, wear=None):
    """A box wrapped in a furoshiki: the wrapped block and the knot on top."""
    out = [W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, mat, vis=(1,)),
           fkit.rotated_box(0.0, 0.0, 0.07, 0.05, h, h + 0.035, 20.0, mat, vis=(1,))]
    for s in out:
        if wear:
            s.wear = wear
    return out


def goods(kind="cloth", state="stacked"):
    """Clusters sized for a 0.91 m step (<= 0.20 deep) or the display strip. Dressing only: loot lies on the
    step / strip around them."""
    P = FPart("goods", budget="small", mass=4.0, flat=state != "stacked")
    swept = state != "stacked"
    if kind == "cloth":
        if not swept:
            y = 0.0
            for row, n in enumerate((3, 2, 1)):
                for k in range(n):
                    x = -0.10 * (n - 1) + 0.20 * k - 0.20
                    mat = INDIGO if (row + k) % 2 == 0 else KINARI
                    add_all(P, xfs(bolt(mat=mat), ry=90.0, t=(x, y, 0.0)))
                y += 0.087
            add_all(P, xfs(sandals(), ry=5.0, t=(0.25, 0.0, 0.0)))
            add_all(P, xfs(sandals(), ry=-8.0, t=(0.25, 0.018, 0.01)))
            add_all(P, xfs(sandals(), ry=3.0, t=(0.25, 0.036, -0.01)))
            P.add(col(-0.52, 0.12, 0.0, 0.26, -0.18, 0.18, INDIGO))
            P.add(W(-0.52, 0.12, 0.0, 0.26, -0.18, 0.18, INDIGO, vis=(2,)))
        else:
            # bolts rolled off and one unrolled across the strip, sandals kicked apart
            r = random.Random(5)
            for i in range(4):
                add_all(P, xfs(bolt(mat=INDIGO if i % 2 else KINARI, wear="_w2"), ry=r.uniform(0, 180),
                               t=(r.uniform(-0.5, 0.4), 0.0, r.uniform(-0.25, 0.3))))
            cloth = W(-0.60, 0.60, 0.0, 0.004, -0.18, 0.18, INDIGO, vis=(1, 2))
            cloth.wear = "_w2"
            P.add(xf(cloth, ry=12.0, t=(0.1, 0.0, 0.45)))
            add_all(P, xfs(bolt(L=0.36, d=0.05, mat=INDIGO, wear="_w2"), ry=102.0, t=(0.72, 0.0, 0.33)))
            for i in range(3):
                add_all(P, xfs(sandals("_w2"), ry=r.uniform(0, 180), t=(r.uniform(-0.6, 0.6), 0.0, r.uniform(0.6, 0.9))))
            P.add(W(-0.6, 0.6, 0.0, 0.1, -0.3, 0.3, INDIGO, vis=(2,)))
    else:   # paper goods: bundles, wrapped packages, small boxes
        if not swept:
            for i in range(3):
                add_all(P, xfs(paper_bundle(), ry=(-4.0, 3.0, -2.0)[i], t=(-0.25, 0.08 * i, 0.0)))
            add_all(P, xfs(package(mat=INDIGO), t=(0.02, 0.0, 0.0)))
            add_all(P, xfs(package(0.16, 0.14, 0.08), ry=12.0, t=(0.02, 0.10, 0.0)))
            import props_storage
            ss, _ = props_storage.hako("s", cord=True)
            add_all(P, xfs(ss, ry=90.0, t=(0.26, 0.0, 0.0)))
            P.add(col(-0.38, 0.37, 0.0, 0.24, -0.16, 0.16, PAPER))
            P.add(W(-0.38, 0.37, 0.0, 0.24, -0.16, 0.16, PAPER, vis=(2,)))
        else:
            r = random.Random(9)
            for i in range(2):
                add_all(P, xfs(paper_bundle(wear="_w2"), ry=r.uniform(0, 180), t=(r.uniform(-0.4, 0.4), 0.0,
                                                                               r.uniform(0.0, 0.4))))
            add_all(P, papers(111, 0.0, 0.5, 6, 0.4))
            add_all(P, rest(xfs(package(mat=INDIGO, wear="_w2"), rz=90.0, t=(0.45, 0.0, 0.20))))
            P.add(W(-0.5, 0.5, 0.0, 0.08, -0.1, 0.7, PAPER, vis=(2,)))
    P.notes.append("dressing only; loot lies on the step / strip around it")
    return P


def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_zukue", "cat": CAT, "models": [
        M("jp_f_zukue_choba", "choba", "intact", "Account desk (choba-zukue)", lambda: zukue("choba")),
        M("jp_f_zukue_choba_tipped", "choba", "tipped", "Account desk on its side, ledger scattered",
          lambda: zukue("choba", "tipped")),
        M("jp_f_zukue_plain", "plain", "intact", "Low writing desk (fuzukue)", lambda: zukue("plain")),
        M("jp_f_zukue_plain_tipped", "plain", "tipped", "Writing desk on its side", lambda: zukue("plain", "tipped")),
    ]},
    {"id": "jp_f_choba_goshi", "cat": CAT, "models": [
        M("jp_f_choba_goshi_3", "3", "intact", "Counting-desk lattice, three folds", lambda: choba_goshi(3)),
        M("jp_f_choba_goshi_3_knocked", "3", "knocked", "Counting-desk lattice, one fold knocked flat",
          lambda: choba_goshi(3, "knocked")),
        M("jp_f_choba_goshi_2", "2", "intact", "Counting-desk lattice, two folds", lambda: choba_goshi(2)),
        M("jp_f_choba_goshi_2_knocked", "2", "knocked", "Counting-desk lattice (two folds), one knocked flat",
          lambda: choba_goshi(2, "knocked")),
    ]},
    {"id": "jp_f_misedana", "cat": CAT, "models": [
        M("jp_f_misedana_1ken", "1ken", "intact", "Stepped goods stand 1.82 m", lambda: misedana(1.82)),
        M("jp_f_misedana_1ken_toppled", "1ken", "toppled", "Goods stand 1.82 m, toppled forward",
          lambda: misedana(1.82, "toppled")),
        M("jp_f_misedana_half", "half", "intact", "Stepped goods stand 0.91 m", lambda: misedana(0.91)),
        M("jp_f_misedana_half_toppled", "half", "toppled", "Goods stand 0.91 m, toppled forward",
          lambda: misedana(0.91, "toppled")),
    ]},
    {"id": "jp_f_goods_general", "cat": CAT, "notes": ["general-goods shop set (shop:general): clusters <= 300 faces"],
     "models": [
        M("jp_f_goods_general_cloth", "cloth", "intact", "Goods: cloth bolts and sandals, stacked",
          lambda: goods("cloth", "stacked")),
        M("jp_f_goods_general_cloth_swept", "cloth", "swept", "Goods: cloth swept off, a bolt unrolled",
          lambda: goods("cloth", "swept")),
        M("jp_f_goods_general_paper", "paper", "intact", "Goods: paper bundles, packages, a box",
          lambda: goods("paper", "stacked")),
        M("jp_f_goods_general_paper_swept", "paper", "swept", "Goods: paper and packages swept off",
          lambda: goods("paper", "swept")),
    ]},
]
