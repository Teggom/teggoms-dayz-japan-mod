"""Heat and light props (BUILD_LIST rows 22-24): andon, hibachi, tabakobon. Andon ship unlit (decision 14)."""
import math
import random

import fkit
import bits
from fkit import (core, box, prism, ngon, sheet, lathe, xf, xfs, flat_poly, W, col, cyl_col, board, FPart, rest,
                  WOOD, IRON, DARK, PALE, PAPER, ASH, HOOP, LITTER)
from bits import disc, shards, stain, mound

CAT = "heat_light"


def add_all(P, ss):
    for s in ss:
        P.add(s)


def open_bar(x0, x1, y0, y1, z0, z1, mat=WOOD, vis=(1,)):
    """A thin bar without its end caps (4 faces): lattice and frame members (kit's open_bar idea)."""
    s = box(x0, x1, y0, y1, z0, z1, mat, vis=vis)
    s.finalize()
    L = sorted([(abs(x1 - x0), 0), (abs(y1 - y0), 1), (abs(z1 - z0), 2)])[-1][1]
    keep = [i for i in range(len(s.faces)) if abs(s.fn[i][L]) < 0.9]
    s.faces = [s.faces[i] for i in keep]
    s.fn = [s.fn[i] for i in keep]
    s.fm = [s.fm[i] for i in keep]
    s.fuv = [s.fuv[i] for i in keep]
    s.normals = s.fn
    return s


# ================================================================================================ andon
def andon_parts(kind="kaku", torn=False, wear=None):
    """Square standing andon (0.25 x 0.25 x 0.80): drawer base, four posts, a paper box (hi-bukuro) 0.35-0.75,
    an inner shelf with the oil dish, the carrying bar on top. ariake: a 0.35 box lamp on the floor."""
    out = []
    a = 0.125
    if kind == "kaku":
        H, pb0, pb1 = 0.80, 0.36, 0.74
        out.append(board(-a, a, 0.0, 0.10, -a, a, k=2, vis=(1, 2)))                            # base
        out.append(W(-0.09, 0.09, 0.02, 0.08, a, a + 0.004, vis=(1,)))                          # drawer front
        out.append(box(-0.012, 0.012, 0.045, 0.055, a + 0.004, a + 0.012, IRON, vis=(1,)))      # drawer pull
        for sx in (-1, 1):
            for sz in (-1, 1):
                out.append(open_bar(sx * a - 0.01 * (sx > 0), sx * a + 0.01 * (sx < 0) - 0.0,
                                    0.10, H, sz * a - 0.01 * (sz > 0), sz * a + 0.01 * (sz < 0)))
        out.append(W(-a, a, H - 0.02, H, -0.01, 0.01, vis=(1, 2)))                             # carrying bar
        # inner shelf and the oil dish (andon-zara) on its stand
        out.append(W(-a + 0.01, a - 0.01, 0.34, 0.355, -a + 0.01, a - 0.01, vis=(1,)))
        out.append(lathe([(0.0, 0.355), (0.03, 0.355), (0.03, 0.40), (0.045, 0.40), (0.05, 0.41), (0.0, 0.405)], 8,
                         PALE, vis=(1,)))
        out.append(W(-a, a, 0.10, H, -a, a, PAPER, vis=(2,)))
    else:
        H, pb0, pb1 = 0.35, 0.05, 0.31
        out.append(board(-a, a, 0.0, 0.05, -a, a, k=3, vis=(1, 2)))
        out.append(board(-a - 0.01, a + 0.01, 0.31, 0.335, -a - 0.01, a + 0.01, k=5, vis=(1, 2)))   # lid
        out.append(W(-0.03, 0.03, 0.335, 0.35, -0.012, 0.012, vis=(1,)))                        # knob
        for sx in (-1, 1):
            for sz in (-1, 1):
                out.append(open_bar(sx * a - 0.01 * (sx > 0), sx * a + 0.01 * (sx < 0), 0.05, 0.31,
                                    sz * a - 0.01 * (sz > 0), sz * a + 0.01 * (sz < 0)))
        out.append(lathe([(0.0, 0.05), (0.035, 0.05), (0.04, 0.065), (0.0, 0.06)], 8, PALE, vis=(1,)))
        out.append(W(-a, a, 0.05, 0.31, -a, a, PAPER, vis=(2,)))
    # paper panels (thin closed slabs, both faces show) with top / bottom rails and one mid kumiko bar per face
    sides = [((0, 0, 1), "front"), ((0, 0, -1), "back"), ((1, 0, 0), "right"), ((-1, 0, 0), "left")]
    for i, (n, nm) in enumerate(sides):
        if torn and i == 0:
            continue
        t0, t1 = a - 0.006, a - 0.004
        if n[2]:
            zz = (t0, t1) if n[2] > 0 else (-t1, -t0)
            p = W(-a + 0.01, a - 0.01, pb0, pb1, zz[0], zz[1], PAPER, vis=(1,), uv="fit")
            rails = [W(-a + 0.01, a - 0.01, y0, y0 + 0.018, zz[0] - 0.006, zz[1] + 0.004, vis=(1,))
                     for y0 in (pb0 - 0.018, pb1)]
            rails.append(open_bar(-0.004, 0.004, pb0, pb1, zz[0] - 0.004, zz[1] + 0.004))
        else:
            xx = (t0, t1) if n[0] > 0 else (-t1, -t0)
            p = W(xx[0], xx[1], pb0, pb1, -a + 0.01, a - 0.01, PAPER, vis=(1,), uv="fit")
            rails = [W(xx[0] - 0.006, xx[1] + 0.004, y0, y0 + 0.018, -a + 0.01, a - 0.01, vis=(1,))
                     for y0 in (pb0 - 0.018, pb1)]
            rails.append(open_bar(xx[0] - 0.004, xx[1] + 0.004, pb0, pb1, -0.004, 0.004))
        p.wear = "_w2" if (torn or wear) else "_w1"
        out.append(p)
        out += rails
    if torn:
        # the front panel torn: a ragged strip still hanging in the frame
        rag = W(-a + 0.01, -0.02, pb0 + 0.12, pb1, a - 0.006, a - 0.004, PAPER, vis=(1,), uv="fit")
        rag.wear = "_w2"
        out.append(rag)
        out.append(W(-a + 0.01, a - 0.01, pb1, pb1 + 0.018, a - 0.012, a, vis=(1,)))
    for s in out:
        if wear and not getattr(s, "wear", None):
            s.wear = wear
    return out, H


def andon(kind="kaku", state="intact"):
    P = FPart("andon", budget="small", res3=False, mass=3.0 if kind == "kaku" else 1.5)
    tipped = state != "intact"
    ss, H = andon_parts(kind, torn=tipped, wear="_w2" if tipped else None)
    a = 0.125
    if not tipped:
        add_all(P, ss)
        P.add(col(-a, a, 0.0, H, -a, a))
    else:
        # knocked over onto its back; the oil dish out and broken, an oil stain on the mat
        ss = [s for s in ss if not (s.fm and s.fm[0] == PALE)]
        ss = xfs(ss, rx=-90.0)
        ss = rest(xfs(ss, ry=25.0))
        add_all(P, ss)
        c = xf(xf(box(-a, a, 0.0, H, -a, a, WOOD), rx=-90.0), ry=25.0)
        lo = min(v[1] for v in c.verts)
        P.add(fkit.col_solid(xf(c, t=(0.0, -lo, 0.0))))
        add_all(P, shards(60 if kind == "kaku" else 61, 0.25, 0.30, 0.10, 5, PALE))
        P.add(stain(62, 0.22, 0.30, 0.22, sx=1.4, wear="_w2"))
    P.dim("w", 0.25, 0.25, tol=0.005)
    P.dim("h", 0.80 if kind == "kaku" else 0.35, H, tol=0.005)
    P.notes.append("unlit (no light point), decision 14")
    return P


# ================================================================================================ hibachi
def tongs(y, cx=0.0, cz=0.0, lying=False):
    """Hibashi: two iron rods 0.30, stuck in the ash at an angle (or lying on the mat)."""
    out = []
    for dx in (-0.008, 0.008):
        r = box(-0.003, 0.003, 0.0, 0.30, -0.003, 0.003, IRON, vis=(1,))
        if lying:
            r = xf(r, rz=-88.0, t=(0.0, 0.004, 0.0))
            out.append(xf(r, ry=20.0, t=(cx + dx * 2, 0.0, cz + dx * 3)))
        else:
            out.append(xf(r, rz=18.0, rx=-8.0, t=(cx + dx, y - 0.05, cz)))
    return out


def trivet(y, r=0.08):
    """Gotoku: an iron ring on three legs standing in the ash."""
    out = [bits.rope_ring(r, y + 0.07, 0.01, IRON, 8, proud=0.004)]
    for k in range(3):
        a = 2 * math.pi * k / 3
        out.append(box(r * math.cos(a) - 0.004, r * math.cos(a) + 0.004, y - 0.01, y + 0.075, r * math.sin(a) - 0.004,
                       r * math.sin(a) + 0.004, IRON, vis=(1,)))
    return out


def hibachi(kind="round", state="intact"):
    P = FPart("hibachi", budget="small", mass=6.0 if kind == "round" else 9.0)
    tipped = state != "intact"
    wear = "_w2" if tipped else None
    if kind == "round":
        R, H, ash_y = 0.19, 0.28, 0.20
        body = lathe([(0.0, 0.0), (0.13, 0.0), (0.15, 0.02), (0.18, 0.08), (R, 0.17), (0.18, 0.25),
                      (0.172, H), (0.155, H), (0.16, 0.22), (0.16, ash_y)], 12, PALE, vis=(1,), wear=wear)
        parts = [body, lathe([(0.0, 0.0), (0.15, 0.0), (R, 0.15), (0.165, H), (0.0, H - 0.02)], 7, PALE, vis=(2,),
                             wear=wear)]
        if not tipped:
            parts.append(disc(0.16, ash_y - 0.01, ash_y, ASH, n=10, vis=(1, 2)))
            parts += trivet(ash_y) + tongs(ash_y, 0.06, 0.03)
        else:
            parts.append(disc(0.16, ash_y - 0.03, ash_y - 0.02, ASH, n=10, vis=(1,), wear="_w2"))
        add_all(P, parts if not tipped else rest(xfs(parts, rx=90.0, ry=-30.0)))
        c = cyl_col(R, 0.0, H, n=8, mat=PALE)
        if not tipped:
            P.add(c)
        else:
            c2 = xf(xf(c, rx=90.0), ry=-30.0)
            lo = min(v[1] for v in c2.verts)
            P.add(fkit.col_solid(xf(c2, t=(0.0, -lo, 0.0))))
        P.dim("d", 0.38, 0.38, tol=0.005)
        P.dim("h", 0.28, H, tol=0.005)
    else:
        w, d, H = 0.45, 0.35, 0.30
        t = 0.02
        ash_y = 0.22
        parts = [board(-w / 2, w / 2, 0.0, 0.02, -d / 2, d / 2, k=1, vis=(1,)),
                 board(-w / 2, w / 2, 0.0, H - 0.02, d / 2 - t, d / 2, k=2, vis=(1,)),
                 board(-w / 2, w / 2, 0.0, H - 0.02, -d / 2, -d / 2 + t, k=3, vis=(1,)),
                 board(-w / 2, -w / 2 + t, 0.0, H - 0.02, -d / 2 + t, d / 2 - t, k=4, vis=(1,)),
                 board(w / 2 - t, w / 2, 0.0, H - 0.02, -d / 2 + t, d / 2 - t, k=5, vis=(1,))]
        # top frame: narrow on three sides, a wide board on the right (the loot surface, where the kettle sat)
        wide = 0.10
        parts += [board(-w / 2, w / 2 - wide, H - 0.02, H, d / 2 - 0.035, d / 2, k=6, vis=(1,)),
                  board(-w / 2, w / 2 - wide, H - 0.02, H, -d / 2, -d / 2 + 0.035, k=7, vis=(1,)),
                  board(-w / 2, -w / 2 + 0.035, H - 0.02, H, -d / 2 + 0.035, d / 2 - 0.035, k=8, vis=(1,)),
                  board(w / 2 - wide, w / 2, H - 0.02, H, -d / 2, d / 2, k=9, vis=(1,))]
        # iron liner (otoshi) and the ash
        lx0, lx1 = -w / 2 + 0.035, w / 2 - wide
        parts.append(W(lx0, lx1, 0.05, H - 0.02, -d / 2 + 0.035, d / 2 - 0.035, IRON, vis=(1,)))
        parts.append(W(-w / 2, w / 2, 0.0, H, -d / 2, d / 2, vis=(2,)))
        if not tipped:
            cx = (lx0 + lx1) / 2
            parts.append(W(lx0 + 0.003, lx1 - 0.003, H - 0.021, ash_y + 0.03, -d / 2 + 0.04, d / 2 - 0.04, ASH,
                           vis=(1,)))
            parts = [p for p in parts]
            parts += xfs(trivet(ash_y + 0.03, 0.07), t=(cx, 0.0, 0.0)) + tongs(ash_y + 0.03, cx + 0.06, 0.05)
            add_all(P, parts)
            P.add(col(-w / 2, w / 2, 0.0, H, -d / 2, d / 2))
            P.loot_rect("rim", H, w / 2 - wide + 0.01, w / 2 - 0.01, -d / 2 + 0.03, d / 2 - 0.03, rng=0.12,
                        points=[(w / 2 - wide / 2, H, 0.0)])
        else:
            parts = rest(xfs(parts, rx=90.0, ry=15.0))
            add_all(P, parts)
            c = xf(xf(box(-w / 2, w / 2, 0.0, H, -d / 2, d / 2, WOOD), rx=90.0), ry=15.0)
            lo = min(v[1] for v in c.verts)
            P.add(fkit.col_solid(xf(c, t=(0.0, -lo, 0.0))))
        P.dim("w", w, w, tol=0.005)
        P.dim("h", H, H, tol=0.005)
    if tipped:
        # ash spilled across the mat, tongs lying beside
        P.add(mound(70, 0.0, 0.40, 0.26, 0.03, ASH, sx=1.5, wear="_w2", vis=(1, 2)))
        P.add(stain(71, 0.05, 0.45, 0.26, sx=1.4, mat=ASH, wear="_w1"))
        add_all(P, tongs(0.0, -0.25, 0.35, lying=True))
    P.notes.append("cold ash; one in five tipped with the ash spilled (decision 11)")
    return P


# ================================================================================================ tabakobon
def tabakobon(state="std"):
    P = FPart("tabakobon", budget="small", mass=1.2)
    w, d = 0.30, 0.20
    parts = [board(-w / 2, w / 2, 0.0, 0.012, -d / 2, d / 2, k=1, vis=(1,)),
             W(-w / 2, w / 2, 0.012, 0.06, d / 2 - 0.01, d / 2, vis=(1,)),
             W(-w / 2, w / 2, 0.012, 0.06, -d / 2, -d / 2 + 0.01, vis=(1,)),
             W(-w / 2, -w / 2 + 0.01, 0.012, 0.06, -d / 2 + 0.01, d / 2 - 0.01, vis=(1,)),
             W(w / 2 - 0.01, w / 2, 0.012, 0.06, -d / 2 + 0.01, d / 2 - 0.01, vis=(1,)),
             # the handle: two uprights and the bar at 0.18
             W(-0.012, 0.012, 0.012, 0.18, -d / 2 + 0.01, -d / 2 + 0.025, vis=(1,)),
             W(-0.012, 0.012, 0.012, 0.18, d / 2 - 0.025, d / 2 - 0.01, vis=(1,)),
             W(-0.015, 0.015, 0.16, 0.18, -d / 2 + 0.01, d / 2 - 0.01, vis=(1, 2)),
             W(-w / 2, w / 2, 0.0, 0.06, -d / 2, d / 2, vis=(2,))]
    pot = [lathe([(0.0, 0.012), (0.03, 0.012), (0.04, 0.03), (0.042, 0.075), (0.036, 0.075), (0.034, 0.06),
                  (0.0, 0.058)], 8, PALE, vis=(1,))]
    tube = [fkit.lcyl("y", 0.0, 0.0, 0.025, 0.012, 0.10, HOOP, n=6, vis=(1,), caps=HOOP)]
    pipe = [box(-0.10, 0.10, -0.003, 0.003, -0.003, 0.003, HOOP, vis=(1,)),
            box(-0.12, -0.10, -0.004, 0.006, -0.004, 0.004, IRON, vis=(1,)),
            box(0.10, 0.125, -0.004, 0.004, -0.004, 0.004, IRON, vis=(1,))]
    if state == "std":
        add_all(P, parts)
        add_all(P, xfs(pot, t=(-0.08, 0.0, 0.0)))
        add_all(P, xfs(tube, t=(0.085, 0.0, 0.03)))
        add_all(P, xfs(pipe, ry=-15.0, t=(0.0, 0.066, 0.045)))
        P.add(disc(0.03, 0.055, 0.058, ASH, n=6, vis=(1,), cx=-0.08))
        P.add(col(-w / 2, w / 2, 0.0, 0.18, -d / 2, d / 2))
    else:
        add_all(P, rest(xfs(parts, rx=80.0, ry=10.0, t=(0.0, 0.0, 0.0))))
        add_all(P, rest(xfs(pot, rx=90.0, ry=40.0, t=(0.20, 0.0, 0.18))))
        add_all(P, rest(xfs(tube, rz=90.0, ry=-20.0, t=(-0.22, 0.0, 0.20))))
        add_all(P, rest(xfs(pipe, ry=35.0, t=(0.05, 0.0, 0.30))))
        P.add(mound(80, 0.12, 0.22, 0.12, 0.015, ASH, sx=1.4, wear="_w2", vis=(1,)))
        c = xf(xf(box(-w / 2, w / 2, 0.0, 0.18, -d / 2, d / 2, WOOD), rx=80.0), ry=10.0)
        lo = min(v[1] for v in c.verts)
        P.add(fkit.col_solid(xf(c, t=(0.0, -lo, 0.0))))
    P.dim("w", w, w, tol=0.005)
    P.dim("h", 0.18, 0.18, tol=0.005)
    return P


def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_andon", "cat": CAT, "notes": ["unlit (decision 14)"], "models": [
        M("jp_f_andon_kaku", "kaku", "intact", "Standing paper lamp (andon)", lambda: andon("kaku")),
        M("jp_f_andon_kaku_tipped", "kaku", "tipped", "Andon, knocked over, paper torn", lambda: andon("kaku", "tipped")),
        M("jp_f_andon_ariake", "ariake", "intact", "Bedside lamp (ariake andon)", lambda: andon("ariake")),
        M("jp_f_andon_ariake_tipped", "ariake", "tipped", "Bedside lamp, knocked over", lambda: andon("ariake", "tipped")),
    ]},
    {"id": "jp_f_hibachi", "cat": CAT, "models": [
        M("jp_f_hibachi_round", "round", "intact", "Round ceramic brazier (hibachi)", lambda: hibachi("round")),
        M("jp_f_hibachi_round_tipped", "round", "tipped", "Round brazier, tipped, ash spilled",
          lambda: hibachi("round", "tipped")),
        M("jp_f_hibachi_box", "box", "intact", "Wooden box brazier", lambda: hibachi("box")),
        M("jp_f_hibachi_box_tipped", "box", "tipped", "Box brazier, tipped, ash spilled", lambda: hibachi("box", "tipped")),
    ]},
    {"id": "jp_f_tabakobon", "cat": CAT, "models": [
        M("jp_f_tabakobon", "std", "intact", "Tobacco tray (tabako-bon)", lambda: tabakobon("std")),
        M("jp_f_tabakobon_spilled", "std", "spilled", "Tobacco tray on its side, ash spilled",
          lambda: tabakobon("spilled")),
    ]},
]
