"""Stone, wave 1 (BUILD_LIST order of work, step 3): stone Jizo, the inscribed-stone family (stele), the Jizo hut.
Stone endures (dead-world rule): standing, mossier (jp_m_decal_moss patches on tops and north faces), text carved
(jp_m_decal_carved_text cells, Yuji Syuku), a rare toppled or sunk variant. Bibs: jp_m_textile_bib_red (added by B3b)
on about 1 in 3 (the `_bib` variant; G1 A3 answer 4)."""
import math
import os
import random
import sys

import skit
from skit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam, rope_path,
                  grid_sheet, text_on, moss_top, moss_face, leaves, litter, add_all, ground, hull3, CARVED, CUT, FIELD,
                  RIVER, WOOD, DARK, ROOFB, CTEXT, BIB, BAMBOO, LEAF)
from props_wood import M

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)


# ================================================================================================ the Jizo figure
def jizo_figure(H, vis_hi=(1,), vis_lo=(2,), vis_3=(3,), wear=None, relief=False, n=10, kind="jizo_stone"):
    """Standing monk (tsuji-jizo) of figure height H, base on y = 0, facing +z. FX2 (2026-10-01, Stephen: 'even the
    Jizo statues are bare bones; the staff has a see-through top'): the sculpted stone Jizo of spikes/FX2 (photo
    references research/statues/REFS.md: Met 53175 / 76084; proportions research/statues/NOTES.md): shaven head with
    a face, robe with the kesa, the jewel in the left hand, the ringed staff (closed loop, beads) in the right (the
    figure's right = +x, the viewer's left in game). kind: 'jizo_stone' (roadside), 'jizo_child' (a child's grave:
    hands in prayer), 'kannon' (the bato Kannon relief). relief=True: the depth halved (boat-halo / panel relief).
    Res 1 / 2 / 3 = the mesh's three LODs (vis_lo / vis_3 empty skips one). n is unused (kept for callers)."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "FX2"))
    import fx2props as FX
    # the aged carved stone (FP1's irregular lichen, 2 m tile), not stone_carved's dot pattern (which reads as
    # camouflage on a sculpted surface)
    return FX.figure(kind, H, "stone_carved_aged", vis=(vis_hi, vis_lo, vis_3), sz=0.5 if relief else 1.0, wear=wear)


def scale_z(s, k):
    s.finalize()
    s.verts = [(v[0], v[1], v[2] * k) for v in s.verts]
    s.center = (s.center[0], s.center[1], s.center[2] * k)
    s.fn = [core.norm((n[0] * k, n[1], n[2])) for n in s.fn]
    if getattr(s, "vn", None) is not None:
        s.vn = [[core.norm((q[0] * k, q[1], q[2])) for q in f] for f in s.vn]
    if s.normals is not None:
        s.normals = s.fn
    return s


def plinth(kind, w, h, wear=None):
    """Square two-tier base, or a lotus seat (a flared lathe) on a square block. Returns (solids, top_y)."""
    out = []
    if kind == "square":
        out.append(W(-w / 2, w / 2, -0.05, h * 0.55, -w / 2, w / 2, CARVED, vis=(1, 2, 3)))
        out.append(W(-w * 0.4, w * 0.4, h * 0.55, h, -w * 0.4, w * 0.4, CARVED, vis=(1, 2, 3)))
    else:
        out.append(W(-w / 2, w / 2, -0.05, h * 0.45, -w / 2, w / 2, CARVED, vis=(1, 2, 3)))
        out.append(lathe([(0.0, h * 0.45), (w * 0.30, h * 0.45), (w * 0.28, h * 0.62), (w * 0.44, h * 0.92),
                          (w * 0.36, h), (0.0, h)], 12, CARVED, vis=(1,), wear=wear))
        out.append(lathe([(0.0, h * 0.45), (w * 0.3, h * 0.45), (w * 0.42, h), (0.0, h)], 6, CARVED, vis=(2, 3),
                         smooth=False, wear=wear))
    if wear:
        for s in out:
            s.wear = wear
    return out, h


def bib_and_cap(H, zs=0.78, wear="_w2", form="stone"):
    """A faded rag bib tied at the neck, hanging over the chest, and a knitted-cloth cap (jp_m_textile_bib_red).
    FX2: fitted to the sculpted figures: form 'stone' (the roadside Jizo mesh: neck 0.79 H, chest 0.145 H) or
    'child' (the child's Jizo: neck 0.70 H, robe 0.17-0.19 H, a round head 0.116 H)."""
    if form == "child":
        ny, r0, r1, drop, zs, cap = 0.705 * H, 0.08 * H, 0.20 * H, 0.22 * H, 0.82, (0.125, 0.80, 0.995)
    else:
        ny, r0, r1, drop, zs, cap = 0.795 * H, 0.062 * H, 0.165 * H, 0.21 * H, 0.80, (0.088, 0.885, 1.0)

    def f(u, v):
        a = math.pi * (u - 0.5) * 1.3
        rr = r0 + (r1 - r0) * v
        y = ny - drop * v * (1 - 0.35 * abs(u - 0.5))
        return (rr * math.sin(a), y, rr * zs * math.cos(a) + 0.006 + 0.012 * v)
    out = [grid_sheet(f, 6, 3, BIB, vis=(1,), wear=wear)]
    cr, cy0, ctop = cap
    cap = lathe([(cr * H, cy0 * H), (cr * 0.98 * H, (cy0 + 0.06) * H), (cr * 0.55 * H, (ctop - 0.005) * H),
                 (0.0, (ctop + 0.012) * H)], 10, BIB, vis=(1,), wear=wear)
    out.append(xf(scale_z(cap, 0.95), t=(0.0, 0.0, -0.01 * H)))
    return out


def jizo(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    size = {"s": 0.45, "m": 0.90, "l": 1.36}.get(kind, 0.90)
    if kind == "halo":
        size = 0.62
    P = SPart("stone_jizo", budget="statue", res3=True, mass={0.45: 60.0, 0.90: 300.0, 1.36: 900.0}.get(size, 250.0),
              bury=0.06)   # FX2: a sculpted statue (PLAYBOOK §12)
    pk = "lotus" if kind == "l" else "square"
    pw = {0.45: 0.36, 0.62: 0.50, 0.90: 0.50, 1.36: 0.72}[size]
    ph = {0.45: 0.20, 0.62: 0.22, 0.90: 0.30, 1.36: 0.42}[size]
    ps, top = plinth(pk, pw, ph, wear)
    fig = []
    if kind == "halo":
        # boat-shaped halo stone (funagata): a pointed-arch slab with the figure in relief on its face
        hh = 0.95
        pts = [(-0.21, 0.0), (0.21, 0.0), (0.24, 0.45), (0.19, 0.72), (0.08, 0.90), (0.0, hh), (-0.08, 0.90),
               (-0.19, 0.72), (-0.24, 0.45)]
        slab = prism(pts, "z", -0.09, 0.03, CARVED, vis=(1, 2, 3))
        fig.append(xf(slab, t=(0.0, top, 0.0)))
        fig += xfs(jizo_figure(size * 0.82, relief=True, vis_3=()), t=(0.0, top + 0.03, 0.03))
        fig.append(text_on((0.16, top + 0.45, 0.03), X, Y, 0.30, CTEXT, "enmei_jizo", wear="_w2", off=0.003))
        fig.append(moss_top(21, 0.0, -0.03, 0.05, top + 0.88, wear="_w2"))
        cols = [col_solid(xf(prism(pts, "z", -0.09, 0.03, CARVED), t=(0.0, top, 0.0)))]
        total = top + hh
    else:
        fig = xfs(jizo_figure(size, wear=wear), t=(0.0, top, 0.0))
        cols = [cyl_col(0.19 * size, top, top + size, n=8, mat=CARVED)]
        total = top + size
        if kind in ("m", "l", "bib", "offer", "ab_tipped"):
            fig.append(text_on((0.0, ph * 0.28, pw / 2), X, Y, min(0.22, ph * 0.5), CTEXT, "enmei_jizo",
                               wear="_w1" if not ab else "_w2"))
    cols.append(col(-pw / 2, pw / 2, 0.0, top, -pw / 2, pw / 2, CARVED))
    ps.append(moss_top(3, pw * 0.2, -pw * 0.2, pw * 0.18, ph if pk == "square" else ph * 0.45, wear="_w1"))
    ps.append(moss_face((0.0, ph * 0.25, -pw / 2), (-1.0, 0.0, 0.0), Y, pw * 0.8, ph * 0.4, seed=5))
    if kind == "bib":
        fig += xfs(bib_and_cap(size), t=(0.0, top, 0.0))
    if kind == "offer":
        # a stone cup, a pile of small stones, withered flowers in a bamboo tube
        fx = pw / 2 + 0.12
        fig.append(lathe([(0.0, 0.0), (0.06, 0.0), (0.07, 0.07), (0.05, 0.07), (0.045, 0.02), (0.0, 0.02)], 6, CARVED,
                         vis=(1,)))
        fig[-1] = xf(fig[-1], t=(0.08, 0.0, fx))
        rr = random.Random(9)
        for k in range(3):
            fig.append(core.stone(rr, -0.12 + rr.uniform(-0.05, 0.05), fx + rr.uniform(-0.04, 0.04), 0.05, 0.04, 0.04,
                                  0.03 + (k // 3) * 0.035, RIVER, bury=0.0, n=5, vis=(1,)))
        fig.append(pole((0.22, 0.0, fx - 0.02), (0.22, 0.22, fx - 0.02), 0.025, BAMBOO, n=6, vis=(1,)))
        for k in range(3):
            fig.append(pole((0.22, 0.2, fx - 0.02), (0.22 + rr.uniform(-0.08, 0.08), 0.36, fx + rr.uniform(-0.05, 0.1)),
                            0.004, "wood_sooted", n=3, vis=(1,), wear="_w2"))
        fig.append(litter(7, 0.0, fx, 0.25))
    if kind == "ab_tipped":
        # toppled face-down beside the plinth (quake), the head cracked off
        head = [s for s in fig if getattr(s, "fx2part", None) == "head"]                 # FX2: the head part
        body = [s for s in fig if not any(s is h for h in head)]
        body = [s for s in body if s.mats != CTEXT]
        fall = xfs(xfs(body, t=(0.0, -top, 0.0)), rx=92.0)
        fall = xfs(fall, ry=25.0, t=(0.10, 0.155 * size * 0.78 + 0.01, pw / 2 + 0.05))
        hd = xfs(xfs(head, t=(0.0, -top - 0.86 * size, 0.0)), rx=40.0, rz=70.0)
        hd = xfs(hd, t=(0.62, 0.09 * size, 0.55))
        tx = [s for s in fig if s.mats == CTEXT]
        fig = fall + hd + tx
        cols = [cols[-1], col_solid(xf(xf(box(-0.15 * size, 0.15 * size, 0.0, 0.8 * size, -0.1 * size, 0.1 * size,
                                                 CARVED), rx=92.0), ry=25.0, t=(0.10, 0.12 * size, pw / 2 + 0.05)))]
        fig.append(litter(8, 0.2, 0.5, 0.6, sx=1.3))
        total = top
    add_all(P, ps + fig + cols)
    ground(P, keep=-0.05)
    P.dim("figure_h", size, size, tol=0.01)
    P.dim("plinth_h", ph, top, tol=0.01)
    P.dim("total_h", round(ph + size if kind not in ("halo", "ab_tipped") else total, 3), total, tol=0.01)
    return P


# ================================================================================================ stele family
def slab_prism(pts, t0, t1, mat=CARVED, vis=(1, 2, 3), wear=None):
    s = prism(pts, "z", t0, t1, mat, vis=vis)
    if wear:
        s.wear = wear
    return s


def koshin_pillar(wear=None, h_shaft=0.95, w=0.35, d=0.25, base_h=0.28, text_w=None):
    """Koshin square pillar: shaft 0.95 x 0.35 x 0.25 with a low pointed top, on a 0.28 two-step base; the front has a
    recessed panel with the Shomen Kongo in relief, sun and moon above, three monkeys below."""
    out, cols = [], []
    out.append(W(-w / 2 - 0.10, w / 2 + 0.10, -0.06, base_h * 0.5, -d / 2 - 0.10, d / 2 + 0.10, CARVED, vis=(1, 2, 3)))
    out.append(W(-w / 2 - 0.05, w / 2 + 0.05, base_h * 0.5, base_h, -d / 2 - 0.05, d / 2 + 0.05, CARVED, vis=(1, 2, 3)))
    y0 = base_h
    pts = [(-w / 2, y0), (w / 2, y0), (w / 2, y0 + h_shaft - 0.08), (0.0, y0 + h_shaft), (-w / 2, y0 + h_shaft - 0.08)]
    out.append(slab_prism(pts, -d / 2, d / 2 - 0.03))
    # front: frame rim around a recessed panel (the panel face 3 cm back)
    fz = d / 2
    out.append(W(-w / 2, w / 2, y0, y0 + 0.08, fz - 0.03, fz, CARVED, vis=(1,)))
    out.append(W(-w / 2, w / 2, y0 + h_shaft - 0.20, y0 + h_shaft - 0.10, fz - 0.03, fz, CARVED, vis=(1,)))
    for sx in (-1, 1):
        out.append(W(sx * w / 2 - 0.04 * (sx > 0) - 0.0, sx * w / 2 + 0.04 * (sx < 0), y0 + 0.08, y0 + h_shaft - 0.20,
                     fz - 0.03, fz, CARVED, vis=(1,)))
    out.append(W(-w / 2, w / 2, y0, y0 + h_shaft - 0.08, fz - 0.03, fz, CARVED, vis=(2, 3)))
    # relief: the deity (a flattened figure), sun and moon discs, three monkeys
    fig = jizo_figure(0.50, relief=True, vis_3=(), vis_lo=())
    fig = [scale_z(s, 0.55) for s in fig]
    out += xfs(fig, t=(0.0, y0 + 0.16, fz - 0.03))
    for sx in (-1, 1):
        dsc = lathe([(0.0, 0.0), (0.035, 0.0), (0.035, 0.012), (0.0, 0.012)], 6, CARVED, vis=(1,), smooth=False)
        out.append(xf(dsc, rx=90.0, t=(sx * 0.10, y0 + h_shaft - 0.27, fz - 0.03 + 0.012)))
    for k in (-1, 0, 1):
        out.append(core.stone(random.Random(30 + k), k * 0.09, fz - 0.015, 0.07, 0.03, 0.06, y0 + 0.14, CARVED, bury=0.0,
                              n=5, vis=(1,)))
    out.append(text_on((w / 2, y0 + h_shaft * 0.55, 0.0), (0.0, 0.0, -1.0), Y, h_shaft * 0.62, CTEXT, "koshin_kuyoto",
                       wear=wear or "_w1"))
    out.append(moss_top(40, 0.05, 0.0, 0.10, base_h, wear="_w1"))
    out.append(moss_face((0.0, y0 + 0.4, -d / 2), (-1.0, 0.0, 0.0), Y, w * 0.9, 0.5, seed=41))
    if wear:
        for s in out:
            if s.mats == CARVED:
                s.wear = wear
    cols.append(col(-w / 2 - 0.1, w / 2 + 0.1, 0.0, base_h, -d / 2 - 0.1, d / 2 + 0.1, CARVED))
    cols.append(col_solid(slab_prism(pts, -d / 2, d / 2)))
    return out, cols, y0 + h_shaft


def arched(w=0.36, h=0.78, t=0.15, cellname="namuamidabutsu", wear=None, base=True):
    out, cols = [], []
    y0 = 0.14 if base else 0.0
    if base:
        out.append(W(-w / 2 - 0.08, w / 2 + 0.08, -0.05, y0, -t / 2 - 0.08, t / 2 + 0.08, CARVED, vis=(1, 2, 3)))
        cols.append(col(-w / 2 - 0.08, w / 2 + 0.08, 0.0, y0, -t / 2 - 0.08, t / 2 + 0.08, CARVED))
    pts = [(-w / 2, y0), (w / 2, y0), (w / 2, y0 + h - w / 2)]
    for k in range(1, 6):
        a = math.pi * k / 6
        pts.append((w / 2 * math.cos(a), y0 + h - w / 2 + w / 2 * math.sin(a)))
    pts.append((-w / 2, y0 + h - w / 2))
    out.append(slab_prism(pts, -t / 2, t / 2, wear=wear))
    cols.append(col_solid(slab_prism(pts, -t / 2, t / 2)))
    out.append(text_on((0.0, y0 + h * 0.48, t / 2), X, Y, h * 0.72, CTEXT, cellname, wear=wear or "_w1"))
    out.append(moss_face((0.0, y0 + h * 0.3, -t / 2), (-1.0, 0.0, 0.0), Y, w * 0.8, h * 0.4, seed=len(cellname)))
    return out, cols, y0 + h


def natural_slab(seed=3, h=1.10, w=0.62, t=0.24, cellname="koshin_kuyoto", wear=None):
    rr = random.Random(seed)
    pts = [(-w / 2 * rr.uniform(0.85, 1.0), -0.12), (w / 2 * rr.uniform(0.85, 1.0), -0.12),
           (w / 2 * rr.uniform(0.9, 1.05), h * 0.45), (w / 2 * rr.uniform(0.6, 0.8), h * 0.82),
           (w * 0.1, h), (-w / 2 * rr.uniform(0.5, 0.7), h * 0.9), (-w / 2 * rr.uniform(0.9, 1.05), h * 0.5)]
    pts = core.hull2d(pts)
    back = [(x * 0.9, y) for x, y in pts]
    verts = [(x, y, t / 2) for x, y in pts] + [(x, y, -t / 2 + 0.03 * math.sin(x * 9)) for x, y in back]
    s = hull3(verts, CARVED, geo=False, view=False, fire=False)
    s.vis = {1, 2, 3}
    if wear:
        s.wear = wear
    c = hull3(verts, CARVED)
    tx = text_on((0.0, h * 0.5, t / 2), X, Y, h * 0.62, CTEXT, cellname, wear=wear or "_w1", off=0.004)
    mo = moss_top(seed + 5, 0.0, 0.0, 0.08, h * 0.9, wear="_w1")
    return [s, tx, mo], [c], h


def round_stone(seed=6, d=0.55, h=0.60, cellname="dosojin", wear=None):
    rr = random.Random(seed)
    base = [(x, z) for x, z in core.rand_convex(rr, 9, d / 2, d * 0.38)]
    prof = [(-0.08, 0.85), (h * 0.35, 1.0), (h * 0.75, 0.82), (h, 0.35)]
    s = core.rings((base, prof), CARVED, vis=(1, 2, 3))
    if wear:
        s.wear = wear
    c = core.rings((base, prof), CARVED, vis=(), geo=True, view=True, fire=True)
    fz = max(z for x, z in base) * 0.97
    tx = text_on((0.0, h * 0.45, fz), X, Y, h * 0.45, CTEXT, cellname, wear=wear or "_w1", off=0.02)
    return [s, tx, moss_top(seed, 0.0, 0.0, 0.08, h - 0.005)], [c], h


def stele(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    fig = kind in ("koshin", "ab_tipped", "relief_panel")             # FX2: the sculpted relief figure
    P = SPart("stele", budget="statue" if fig else "small", res3=False, mass=250.0, bury=0.13)
    if kind == "koshin" or kind == "ab_tipped":
        ss, cs, top = koshin_pillar(wear=wear)
        if ab:
            ss = xfs(ss + cs, rx=-14.0, rz=6.0, t=(0.0, -0.18, 0.0))
            cs = [s for s in ss if s.geo]
            ss = [s for s in ss if not s.geo]
            ss.append(moss_top(44, 0.0, 0.2, 0.3, 0.0, wear="_w2"))
            ss.append(litter(45, 0.0, 0.3, 0.6))
            P.bury = 0.34
        P.dim("koshin_total_h", 1.22, 0.28 + 0.95, tol=0.02)
        P.dim("shaft_w", 0.35, 0.35, tol=0.01)
    elif kind == "relief_panel":
        # bato Kannon: an arched panel with a niche and the figure in relief, the name carved beside it
        ss, cs, top = arched(w=0.46, h=0.85, t=0.18, cellname="bato_kanzeon", wear=wear)
        ss += xfs([scale_z(s, 0.5) for s in jizo_figure(0.50, relief=True, vis_3=(), vis_lo=(), kind="kannon")],
                  t=(-0.06, 0.26, 0.09))                               # FX2: a Kannon, not a Jizo
        ss = [s for s in ss if not (s.mats == CTEXT)]
        ss.append(text_on((0.15, 0.14 + 0.85 * 0.5, 0.09), X, Y, 0.36, CTEXT, "bato_kanzeon", wear="_w1"))
        P.dim("panel_h", 0.85, 0.85, tol=0.01)
    elif kind == "natural_slab":
        ss, cs, top = natural_slab()
        P.dim("slab_h", 1.10, top, tol=0.01)
    elif kind == "arched":
        ss, cs, top = arched()
        P.dim("arched_h", 0.78, 0.78, tol=0.01)
    elif kind == "pillar":
        # square direction post with a pyramidal top: 'right Edo road / left Oyama road' on the front
        h, w = 1.20, 0.22
        pts = [(-w / 2, -0.25), (w / 2, -0.25), (w / 2, h - 0.08), (0.0, h), (-w / 2, h - 0.08)]
        ss = [W(-w / 2, w / 2, -0.25, h - 0.08, -w / 2, w / 2, CARVED, vis=(1, 2, 3))]
        pyr = core.Solid([(-w / 2, h - 0.08, -w / 2), (w / 2, h - 0.08, -w / 2), (w / 2, h - 0.08, w / 2),
                          (-w / 2, h - 0.08, w / 2), (0.0, h, 0.0)], [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]],
                         CARVED, vis=(1, 2, 3))
        ss.append(pyr)
        ss.append(text_on((0.0, h * 0.52, w / 2), X, Y, 0.62, CTEXT, "michishirube_edo_oyama", wear="_w1",
                          width=0.20))
        ss.append(text_on((w / 2, h * 0.55, 0.0), (0.0, 0.0, -1.0), Y, 0.55, CTEXT, "sakai_kore_yori_higashi",
                          wear="_w1", width=0.20))
        ss.append(moss_face((0.0, 0.25, -w / 2), (-1.0, 0.0, 0.0), Y, 0.2, 0.4, seed=3))
        cs = [col(-w / 2, w / 2, 0.0, h - 0.08, -w / 2, w / 2, CARVED)]
        P.bury = 0.26
        P.dim("post_h", 1.20, h, tol=0.01)
        P.dim("post_w", 0.22, w, tol=0.01)
    elif kind == "round":
        ss, cs, top = round_stone()
        P.dim("round_h", 0.60, top, tol=0.01)
    else:   # group3: three stones on one rough base
        ss = [core.stone(random.Random(2), 0.0, 0.0, 1.5, 0.75, 0.16, 0.10, FIELD, bury=0.06, n=9, vis=(1, 2, 3))]
        cs = [col(-0.62, 0.62, 0.0, 0.10, -0.3, 0.3, FIELD)]
        a, ac, _ = arched(w=0.30, h=0.62, t=0.13, cellname="namuamidabutsu", base=False)
        b, bc, _ = round_stone(seed=8, d=0.40, h=0.42, cellname="dosojin")
        c, cc, _ = natural_slab(seed=11, h=0.80, w=0.40, t=0.18, cellname="koshin_kuyoto")
        ss += xfs(a, t=(-0.42, 0.10, 0.0)) + xfs(b, t=(0.45, 0.18, 0.02)) + xfs(c, ry=-4.0, t=(0.0, 0.22, -0.02))
        cs += xfs(ac, t=(-0.42, 0.10, 0.0)) + xfs(bc, t=(0.45, 0.18, 0.02)) + xfs(cc, ry=-4.0, t=(0.0, 0.22, -0.02))
        ss.append(litter(4, 0.0, 0.4, 0.7, sx=1.5))
        P.dim("group_n", 3, 3, tol=0)
    for q in ss:
        q.vis.discard(3)
    add_all(P, ss + cs)
    return P


# ================================================================================================ Jizo hut
def gable_roof(L, D, eave, ridge, wear=None, vis=(1, 2, 3), battens=True, lift=0.0):
    """Board gable roof, ridge along x (L), eaves at +-D/2 (z). lift: the +z plane's boards lifted (abandoned)."""
    out, cols = [], []
    for sz in (-1, 1):
        c = [(-L / 2, ridge, 0.0), (L / 2, ridge, 0.0), (L / 2, eave, sz * D / 2), (-L / 2, eave, sz * D / 2)]
        c2 = [(p[0], p[1] + 0.03, p[2]) for p in c]
        s = core.hexa(c + c2, ROOFB, vis=vis)
        if lift and sz > 0:
            s = xf(s, rx=-lift, pivot=(0.0, ridge, 0.0))
        out.append(s)
        cols.append(col_solid(core.hexa(c + c2, ROOFB)))
        if battens:
            for k in (1, 3):
                t = k / 4
                y, z = ridge + (eave - ridge) * t + 0.03, sz * D / 2 * t
                b = W(-L / 2, L / 2, y, y + 0.015, z - 0.01, z + 0.01, ROOFB, vis=(1,))
                if lift and sz > 0:
                    b = xf(b, rx=-lift, pivot=(0.0, ridge, 0.0))
                out.append(b)
    out.append(W(-L / 2 - 0.02, L / 2 + 0.02, ridge + 0.015, ridge + 0.07, -0.05, 0.05, ROOFB, vis=vis))
    if wear:
        for s in out:
            s.wear = wear
    return out, cols


def lattice_door(w, h, wear=None, vis=(1,)):
    """Lattice front leaf: frame + vertical bars 0.03 at 0.09 (list)."""
    out = [W(-w / 2, w / 2, 0.0, 0.04, -0.015, 0.015, DARK, vis=vis), W(-w / 2, w / 2, h - 0.04, h, -0.015, 0.015, DARK,
                                                                          vis=vis)]
    for sx in (-1, 1):
        out.append(W(sx * w / 2 - 0.02, sx * w / 2 + 0.02, 0.0, h, -0.015, 0.015, DARK, vis=vis))
    n = int((w - 0.04) / 0.09)
    for k in range(1, n + 1):
        x = -w / 2 + 0.02 + k * (w - 0.04) / (n + 1)
        out.append(W(x - 0.015, x + 0.015, 0.04, h - 0.04, -0.01, 0.01, DARK, vis=vis))
    out.append(W(-w / 2, w / 2, h * 0.5 - 0.02, h * 0.5 + 0.02, -0.013, 0.013, DARK, vis=vis))
    if wear:
        for s in out:
            s.wear = wear
    return out


def jizo_hut(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    if kind in ("box", "ab_open"):
        P = SPart("jizo_hut", budget="statue", res3=True, mass=120.0, bury=0.12)   # FX2: holds a statue
        S, FL, WH = 0.90, 0.60, 1.40            # half-ken plan, raised floor 0.6, walls to 1.4, ridge ~1.75
        # stone base under a board box
        P.add(core.stone(random.Random(3), 0.0, 0.0, 1.0, 1.0, 0.25, 0.20, FIELD, bury=0.06, n=8, vis=(1, 2, 3)))
        P.add(W(-S / 2, S / 2, 0.20, FL, -S / 2, S / 2, WOOD, vis=(1, 2, 3)))
        for sx in (-1, 1):
            P.add(W(sx * S / 2 - 0.02 * (sx > 0), sx * S / 2 + 0.02 * (sx < 0), FL, WH, -S / 2, S / 2, WOOD,
                    vis=(1, 2)))
        P.add(W(-S / 2, S / 2, FL, WH, -S / 2, -S / 2 + 0.02, WOOD, vis=(1, 2)))
        P.add(W(-S / 2, S / 2, FL, WH, -S / 2, S / 2, WOOD, vis=(3,)))
        P.add(W(-S / 2 + 0.02, S / 2 - 0.02, FL - 0.02, FL + 0.02, -S / 2 + 0.02, S / 2 - 0.02, WOOD, vis=(1, 2)))
        rs, rc = gable_roof(S + 0.30, S + 0.36, WH, WH + 0.33, wear=wear, lift=8.0 if ab else 0.0)
        add_all(P, rs)
        # gable infill boards (triangles)
        for sx in (-1, 1):
            tri = core.Solid([(sx * S / 2, WH, -S / 2), (sx * S / 2, WH, S / 2), (sx * S / 2, WH + 0.33, 0.0),
                              (sx * (S / 2 - 0.02), WH, -S / 2), (sx * (S / 2 - 0.02), WH, S / 2),
                              (sx * (S / 2 - 0.02), WH + 0.33, 0.0)], [[0, 1, 2], [3, 4, 5], [0, 1, 4, 3], [1, 2, 5, 4],
                                                                     [2, 0, 3, 5]], WOOD, vis=(1, 2))
            P.add(tri)
        # the small Jizo inside, on the floor
        add_all(P, xfs(jizo_figure(0.45, vis_lo=(2,), vis_3=()), t=(0.0, FL + 0.02, -0.08)))
        if not ab:
            add_all(P, xfs(lattice_door(S - 0.04, WH - FL - 0.04), t=(0.0, FL + 0.02, S / 2 - 0.02)))
            P.add(leaves(4, 0.1, 0.1, 0.25, FL + 0.025, wear="_w1"))
        else:
            dr = lattice_door(S - 0.04, WH - FL - 0.04, wear="_w2")
            add_all(P, xfs(xfs(dr, rx=-90.0), ry=15.0, t=(0.1, 0.02, S / 2 + 0.55)))
            P.add(leaves(4, 0.0, 0.1, 0.35, FL + 0.025, wear="_w2"))
            P.add(litter(6, 0.1, 0.8, 0.6, sx=1.3))
        P.add(col(-S / 2, S / 2, 0.0, WH, -S / 2, S / 2))
        add_all(P, rc)
        P.dim("plan", 0.90, S, tol=0.01)
        P.dim("floor_h", 0.60, FL, tol=0.01)
        P.dim("height", 1.75, WH + 0.33 + 0.07, tol=0.1)
    elif kind == "hall":
        P = SPart("jizo_hut", budget="statue", res3=True, mass=900.0, bury=0.15)
        S, EV, RG = 1.82, 1.90, 2.80
        for sx in (-1, 1):
            for sz in (-1, 1):
                x, z = sx * (S / 2 - 0.06), sz * (S / 2 - 0.06)
                P.add(W(x - 0.06, x + 0.06, -0.05, EV, z - 0.06, z + 0.06, WOOD, vis=(1, 2, 3)))
                P.add(core.stone(random.Random(int(7 + sx + 3 * sz)), x, z, 0.28, 0.28, 0.14, 0.08, FIELD, bury=0.08,
                                 n=6, vis=(1,)))
                P.add(col(x - 0.06, x + 0.06, 0.0, EV, z - 0.06, z + 0.06))
            # side wall boards, lower 1.2 m, and eave beams
            P.add(W(sx * (S / 2 - 0.06) - 0.012, sx * (S / 2 - 0.06) + 0.012, 0.10, 1.20, -S / 2 + 0.12, S / 2 - 0.12,
                    WOOD, vis=(1, 2)))
            P.add(col(sx * (S / 2 - 0.06) - 0.02, sx * (S / 2 - 0.06) + 0.02, 0.10, 1.20, -S / 2 + 0.12, S / 2 - 0.12))
            P.add(W(sx * (S / 2 - 0.06) - 0.06, sx * (S / 2 - 0.06) + 0.06, EV, EV + 0.12, -S / 2 - 0.1, S / 2 + 0.1,
                    WOOD, vis=(1, 2)))
        P.add(W(-S / 2 + 0.12, S / 2 - 0.12, 0.10, EV, -S / 2 + 0.05, -S / 2 + 0.075, WOOD, vis=(1, 2)))
        P.add(col(-S / 2 + 0.12, S / 2 - 0.12, 0.10, EV, -S / 2 + 0.04, -S / 2 + 0.08))
        for sz in (-1, 1):
            P.add(W(-S / 2 - 0.1, S / 2 + 0.1, EV, EV + 0.12, sz * (S / 2 - 0.06) - 0.06, sz * (S / 2 - 0.06) + 0.06,
                    WOOD, vis=(1,)))
        P.add(W(-0.05, 0.05, EV + 0.12, RG, -0.05, 0.05, WOOD, vis=(1,)))
        # roof: ridge along z (the gable faces the road, +z), plan with a 0.45 overhang
        rs, rc = gable_roof(S + 0.9, S + 1.0, EV + 0.12, RG, wear=wear)
        rs = xfs(rs, ry=90.0)
        rc = xfs(rc, ry=90.0)
        add_all(P, rs + rc)
        # the altar: a stone step with a standard Jizo, offerings
        P.add(W(-0.55, 0.55, 0.0, 0.35, -S / 2 + 0.1, -S / 2 + 0.75, CUT, vis=(1, 2, 3)))
        P.add(col(-0.55, 0.55, 0.0, 0.35, -S / 2 + 0.1, -S / 2 + 0.75, CUT))
        ps, top = plinth("square", 0.46, 0.25)
        add_all(P, xfs(ps, t=(0.0, 0.35, -S / 2 + 0.42)))
        add_all(P, xfs(jizo_figure(0.90, vis_3=()), t=(0.0, 0.35 + top, -S / 2 + 0.42)))
        P.add(col(-0.23, 0.23, 0.35, 0.35 + top + 0.9, -S / 2 + 0.19, -S / 2 + 0.65, CARVED))
        P.add(pole((0.35, 0.35, -0.2), (0.35, 0.57, -0.2), 0.025, BAMBOO, n=6, vis=(1,)))
        P.add(leaves(5, 0.0, 0.2, 0.7, 0.004, wear="_w1", sx=1.2))
        P.dim("plan", 1.82, S, tol=0.01)
        P.dim("eave_h", 1.90, EV, tol=0.01)
        P.dim("ridge_h", 2.80, RG, tol=0.1)
    else:   # stone_roof: two upright slabs and a flat stone roof over a small figure (mountain)
        P = SPart("jizo_hut", budget="statue", res3=True, mass=700.0, bury=0.10)
        for sx in (-1, 1):
            sl = core.stone(random.Random(20 + sx), sx * 0.34, 0.0, 0.14, 0.55, 0.70, 0.70, FIELD, bury=0.08, n=6,
                            flat_top=0.9, vis=(1, 2, 3))
            P.add(sl)
            b = sl.bbox()
            P.add(col(b[0] + 0.02, b[1] - 0.02, 0.0, b[3] - 0.02, b[4] + 0.03, b[5] - 0.03, FIELD))
        top = core.stone(random.Random(25), 0.0, 0.0, 1.05, 0.80, 0.14, 0.86, FIELD, bury=0.0, n=8, flat_top=0.8,
                         vis=(1, 2, 3))
        top = xf(top, t=(0.0, 0.02, 0.0))
        P.add(top)
        b = top.bbox()
        P.add(col(b[0] + 0.05, b[1] - 0.05, b[3] - 0.10, b[3] - 0.01, b[4] + 0.05, b[5] - 0.05, FIELD))
        P.add(moss_top(26, 0.1, -0.1, 0.25, 0.88, wear="_w2"))
        add_all(P, xfs(jizo_figure(0.45, vis_3=(3,)), t=(0.0, 0.0, 0.02)))
        P.add(text_on((0.0, 0.08, 0.10), X, Y, 0.10, CTEXT, "enmei_jizo", wear="_w1", off=0.02, crop=(0, 0, 1, 0.4)))
        P.add(leaves(27, 0.0, 0.1, 0.3, 0.004, wear="_w2"))
        P.dim("figure_h", 0.45, 0.45, tol=0.01)
        P.dim("roof_h", 0.88, 0.88, tol=0.05)
    return P


PROPS = [
    {"id": "jp_s_stone_jizo", "cat": "roadside", "notes": ["about 1 in 3 placements use _bib (faded rag bib + cap, "
                                                           "G1 A3 answer 4)", "six in a row at graveyard gates = six _s "
                                                           "or _m placements"],
     "models": [
         M("jp_s_stone_jizo_s", "s", "intact", "Stone Jizo, small (0.45)", lambda: jizo("s")),
         M("jp_s_stone_jizo_m", "m", "intact", "Stone Jizo, standard (0.90)", lambda: jizo("m")),
         M("jp_s_stone_jizo_l", "l", "intact", "Stone Jizo, large on a lotus (1.36)", lambda: jizo("l")),
         M("jp_s_stone_jizo_halo", "halo", "intact", "Boat-halo Jizo stone (funagata)", lambda: jizo("halo")),
         M("jp_s_stone_jizo_bib", "m", "intact", "Stone Jizo with a faded rag bib and cap", lambda: jizo("bib")),
         M("jp_s_stone_jizo_offer", "m", "intact", "Stone Jizo with offerings (cup, stones, dead flowers)",
           lambda: jizo("offer")),
         M("jp_s_stone_jizo_ab_tipped", "m", "abandoned", "Stone Jizo toppled, head broken off", lambda: jizo("ab_tipped")),
     ]},
    {"id": "jp_s_jizo_hut", "cat": "roadside", "models": [
        M("jp_s_jizo_hut_box", "box", "intact", "Jizo box (street corner), small Jizo inside", lambda: jizo_hut("box")),
        M("jp_s_jizo_hut_hall", "hall", "intact", "Jizo hall, one ken, open front", lambda: jizo_hut("hall")),
        M("jp_s_jizo_hut_stone_roof", "stone_roof", "intact", "Stone-roofed Jizo niche (mountain)",
          lambda: jizo_hut("stone_roof")),
        M("jp_s_jizo_hut_ab_open", "box", "abandoned", "Jizo box, lattice door fallen, roof lifted",
          lambda: jizo_hut("ab_open")),
    ]},
    {"id": "jp_s_stele", "cat": "roadside", "notes": ["carved text cells (jp_m_decal_carved_text): koshin_kuyoto, "
                                                      "bato_kanzeon, namuamidabutsu, dosojin, michishirube_edo_oyama, "
                                                      "sakai_kore_yori_higashi"],
     "models": [
         M("jp_s_stele_koshin", "koshin", "intact", "Koshin pillar with Shomen Kongo relief", lambda: stele("koshin")),
         M("jp_s_stele_relief_panel", "relief_panel", "intact", "Bato Kannon relief panel", lambda: stele("relief_panel")),
         M("jp_s_stele_natural_slab", "natural_slab", "intact", "Natural slab with deep-cut characters",
           lambda: stele("natural_slab")),
         M("jp_s_stele_arched", "arched", "intact", "Arched-top nenbutsu stone", lambda: stele("arched")),
         M("jp_s_stele_pillar", "pillar", "intact", "Direction / boundary post", lambda: stele("pillar")),
         M("jp_s_stele_round", "round", "intact", "Round road-god stone (dosojin)", lambda: stele("round")),
         M("jp_s_stele_group3", "group3", "intact", "Three roadside stones on one base", lambda: stele("group3")),
         M("jp_s_stele_ab_tipped", "koshin", "abandoned", "Koshin pillar leaning and half sunk, lichen",
           lambda: stele("ab_tipped")),
     ]},
]
