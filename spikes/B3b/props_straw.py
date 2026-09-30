"""Straw (BUILD_LIST order of work, step 5): straw stacks, stooks, bundles and rice bales (the AUTUMN signature), and
the sacred straw rope (shimenawa) with paper streamers. Straw stacks are soft cover: View Geometry only (they block
sight, not bullets, and a player can push into them: OUTDOOR_LIST's 'hide in the straw stack'). Ropes have no collision.
Reuses B3a's props_storage.tawara_bale for the bales."""
import math
import random

from skit import (core, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, rope_path, sag, grid_sheet,
                  litter, add_all, ground, WOOD, ROPE, STACK, PAPER)
from bits import jag_rim
from props_wood import M
import props_storage as S     # B3a (read-only): tawara_bale(), tawara_col()


def view_cyl(r, y0, y1, n=8):
    c = cyl_col(r, y0, y1, n=n, mat=STACK)
    c.geo, c.fire = False, None
    return c


def view_cone(r, y0, y1, n=8):
    s = lathe([(0.0, y0), (r, y0), (r * 0.15, y1), (0.0, y1)], n, STACK, vis=(), smooth=False)
    # a closed convex prism-like solid for View Geometry: build from rings
    base = [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    c = core.rings((base, [(y0, 1.0), (y1, 0.12)]), STACK, vis=(), geo=False, view=True, fire=None)
    return c


def nio(kind):
    """kind 'cyl' (Kinai), 'cone' (Kanto), 'slumped' (abandoned: cap blown off, sheared, grey-black top)."""
    ab = kind == "slumped"
    wear = "_w2" if ab else "_w1"
    out = []
    if kind in ("cyl", "slumped"):
        R, H1, H2 = 0.90, 1.70, 2.40
        body = [(0.0, 0.0), (R * 0.92, 0.0), (R, 0.35), (R * 1.02, 1.0), (R * 0.97, H1), (R * 1.08, H1 + 0.06)]
        cap = [(R * 1.08, H1 + 0.06), (R * 0.55, H1 + 0.40), (0.12, H2 - 0.05), (0.0, H2)]
        if ab:
            body = body[:-1] + [(R * 0.8, H1 - 0.1), (0.0, H1 + 0.05)]
            cap = []
        s = lathe(body + cap[1:] if cap else body, 12, STACK, vis=(1,), wear=wear)
        if not ab:
            jag_rim(s, H1 + 0.06, 0.08, 3)
        out.append(s)
        out.append(lathe([(0.0, 0.0), (R, 0.0), (R, H1), (0.0, H2 if not ab else H1)], 6, STACK, vis=(2,), wear=wear,
                         smooth=False))
        if not ab:
            out.append(pole((0.0, H2 - 0.2, 0.0), (0.02, H2 + 0.30, 0.0), 0.04, WOOD, n=5, vis=(1, 2)))
            for y in (H1 + 0.18, H1 + 0.40):
                rr = R * 1.08 - (R * 1.08 - R * 0.55) * (y - H1 - 0.06) / 0.34 + 0.01
                out += rope_path([(rr * math.cos(a), y, rr * math.sin(a)) for a in
                                  [2 * math.pi * k / 10 for k in range(11)]], 0.012, ROPE)
            top = H2 + 0.30
        else:
            # sheared: the upper third slid to one side; loose straw on the ground; the pole leaning
            out = [xf(s, rz=-6.0, pivot=(R, 0.0, 0.0)) if i == 0 else s for i, s in enumerate(out)]
            out.append(pole((0.0, H1 - 0.3, 0.0), (0.4, H1 + 0.45, 0.1), 0.04, WOOD, n=5, vis=(1, 2), wear="_w2"))
            cp = lathe([(R * 1.0, 0.0), (R * 0.5, 0.25), (0.0, 0.30)], 10, STACK, vis=(1,), wear="_w2")
            out.append(xf(cp, rz=12.0, t=(R + 1.0, 0.20, 0.4)))
            out.append(litter(3, R + 0.6, 0.0, 1.0, sx=1.3))
            top = H1 + 0.45
        vc = [view_cyl(R, 0.0, H1, n=8)] + ([view_cone(R, H1, H2 - 0.1)] if not ab else [])
        dims = [("nio_d", 1.8, 2 * R, 0.1), ("nio_h", 2.4, H2, 0.1)]
    else:
        R, H = 1.00, 2.60
        prof = [(0.0, 0.0), (R * 0.9, 0.0), (R, 0.25), (R * 0.95, 0.9), (R * 0.72, 1.6), (R * 0.40, 2.2), (0.10, H - 0.08),
                (0.0, H)]
        s = lathe(prof, 12, STACK, vis=(1,), wear=wear)
        out.append(s)
        out.append(lathe([(0.0, 0.0), (R, 0.0), (R * 0.9, 1.0), (0.0, H)], 6, STACK, vis=(2,), wear=wear, smooth=False))
        out.append(pole((0.0, H - 0.2, 0.0), (0.0, H + 0.3, 0.0), 0.04, WOOD, n=5, vis=(1, 2)))
        for y in (1.9, 2.3):
            rr = R * (0.40 + (0.72 - 0.40) * (2.2 - y) / 0.6) + 0.01 if y < 2.2 else 0.28
            out += rope_path([(rr * math.cos(a), y, rr * math.sin(a)) for a in [2 * math.pi * k / 8 for k in range(9)]],
                             0.012, ROPE)
        vc = [view_cone(R, 0.0, H - 0.2)]
        top = H + 0.3
        dims = [("nio_d", 2.0, 2 * R, 0.1), ("nio_h", 2.6, H, 0.1)]
    return out, vc, dims, top


def sheaf(rr, base, top, r=0.07):
    """One rice sheaf: a tapered straw bundle, heads up (a little fuller at the top), tied at 1/3."""
    out = [pole(base, top, r * 0.8, STACK, n=5, vis=(1,), r1=r * 1.15)]
    m = core.add(base, core.mul(core.sub(top, base), 0.35))
    out.append(pole(core.add(m, (0.0, -0.02, 0.0)), core.add(m, (0.0, 0.02, 0.0)), r * 0.95, "straw_rope", n=5, vis=(1,)))
    return out


def straw_stack(kind):
    ab = kind.startswith("ab")
    if kind in ("nio_cyl", "nio_cone", "ab_slumped"):
        P = SPart("straw_stack", budget="small", mass=300.0, need=("view",))
        ss, vc, dims, top = nio({"nio_cyl": "cyl", "nio_cone": "cone", "ab_slumped": "slumped"}[kind])
        add_all(P, ss + vc)
        for d in dims:
            P.dim(d[0], d[1], d[2], tol=d[3])
        P.notes.append("soft cover: View Geometry only (blocks sight, not bullets; walk-in)")
    elif kind == "stook":
        P = SPart("straw_stack", budget="small", mass=40.0, need=("view",))
        rr = random.Random(5)
        n = 8
        for k in range(n):
            a = 2 * math.pi * k / n + rr.uniform(-0.1, 0.1)
            base = (0.30 * math.cos(a), 0.0, 0.30 * math.sin(a))
            topp = (0.07 * math.cos(a), 1.10 + rr.uniform(-0.05, 0.05), 0.07 * math.sin(a))
            add_all(P, sheaf(rr, base, topp))
        P.add(lathe([(0.0, 0.0), (0.38, 0.0), (0.12, 1.12), (0.0, 1.12)], 6, STACK, vis=(2,), smooth=False))
        P.add(view_cone(0.36, 0.0, 1.05, n=6))
        P.dim("stook_h", 1.1, 1.1, tol=0.1)
        P.dim("footprint_d", 0.6, 0.6, tol=0.15)
    elif kind == "bundle":
        P = SPart("straw_stack", budget="small", mass=4.0, flat=True)
        s = pole((-0.5, 0.125, 0.0), (0.5, 0.125, 0.0), 0.125, STACK, n=7, vis=(1,), caps="straw_rope")
        P.add(s)
        for x in (-0.22, 0.22):
            P.add(pole((x - 0.02, 0.125, 0.0), (x + 0.02, 0.125, 0.0), 0.132, "straw_rope", n=7, vis=(1,)))
        P.add(pole((-0.5, 0.12, 0.0), (0.5, 0.12, 0.0), 0.12, STACK, n=4, vis=(2,)))
        ground(P)
        P.dim("bundle_d", 0.25, 0.25, tol=0.01)
        P.dim("bundle_L", 1.0, 1.0, tol=0.1)
    else:   # tawara_stack: rice bales 3 + 2 under an eave (B3a's tawara_bale)
        P = SPart("straw_stack", budget="small", mass=300.0)
        dy = 0.2 * math.sqrt(3)
        for i, (x, y) in enumerate(((-0.40, 0.0), (0.0, 0.0), (0.40, 0.0), (-0.20, dy), (0.20, dy))):
            ss = S.tawara_bale(n=6, segs="lo", bands=1, rope=ROPE)
            add_all(P, xfs(ss, ry=90.0, t=(x, y, 0.0)))
            P.add(S.tawara_col(x, y, 0.0, 90.0, n=6))
        P.add(W(-0.6, 0.6, 0.0, 0.4, -0.375, 0.375, "straw_tawara", vis=(2,)))
        P.add(W(-0.4, 0.4, 0.4, 0.4 + dy, -0.375, 0.375, "straw_tawara", vis=(2,)))
        P.add(litter(4, 0.0, 0.55, 0.5, sx=1.5, wear="_w1"))
        P.dim("bales", 5, 5, tol=0)
        P.dim("bale_L", 0.75, 0.75, tol=0.02)
        P.dim("bale_d", 0.45, 0.40, tol=0.06)
        P.notes.append("bales under an eave or in a shed doorway only, never in the open field")
    return P


# ================================================================================================ shimenawa
def rope_twist(pts, r, n=6, wear="_w1"):
    out = rope_path(pts, r, ROPE, n=n, wear=wear)
    return out


def shide(p, s=0.26, wear="_w1", rr=None, yaw=0.0):
    """Paper streamer: a 4-fold zigzag strip hanging from p (two-sided quads)."""
    out = []
    w = 0.045
    k = 4
    x, y = 0.0, 0.0
    quads = []
    for i in range(k):
        dx = w * (1 if i % 2 == 0 else -1)
        q = [(x, y, 0.0), (x + 0.03, y, 0.0), (x + 0.03 + dx, y - s / k, 0.0), (x + dx, y - s / k, 0.0)]
        quads.append(q)
        x, y = x + dx, y - s / k
    g = core.sheet(quads + [q[::-1] for q in quads], PAPER,
                   [(0.0, 0.0, 1.0)] * len(quads) + [(0.0, 0.0, -1.0)] * len(quads), vis=(1,))
    g.wear = wear
    return xf(g, ry=yaw, t=p)


def shimenawa(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else "_w1"
    P = SPart("shimenawa", budget="small", mass=3.0, flat=True)
    P.hung = True
    rr = random.Random(len(kind))
    if kind.startswith("len") or ab:
        L = 3.64 if kind == "len_2ken" else 1.82
        Y = 2.50
        r = 0.035 if L < 2 else 0.045
        a, b = (-L / 2, Y, 0.0), (L / 2, Y, 0.0)
        if not ab:
            pts = sag(a, b, 0.12 * L / 1.82, 8)
        else:
            # one end dropped: the rope hangs from the left anchor down to the ground, frayed
            pts = [a, (-L / 2 + 0.25, Y - 0.45, 0.02), (-L / 2 + 0.40, Y - 1.2, 0.05), (-L / 2 + 0.55, 0.9, 0.1),
                   (-L / 2 + 0.75, 0.25, 0.2), (-L / 2 + 1.2, 0.03, 0.35)]
        add_all(P, rope_twist(pts, r, n=6, wear=wear))
        add_all(P, rope_twist([core.add(p, (0.0, 0.01, 0.012)) for p in pts], r * 0.55, n=4, wear=wear))
        if not ab:
            # straw tassels (the hanging tufts) and shide between them
            ns = int(L / 0.5)
            for i in range(ns):
                t = (i + 0.5) / ns
                p = pts[int(t * (len(pts) - 1))]
                q = pts[min(len(pts) - 1, int(t * (len(pts) - 1)) + 1)]
                c = core.add(p, core.mul(core.sub(q, p), t * (len(pts) - 1) - int(t * (len(pts) - 1))))
                if i % 2 == 0:
                    P.add(pole(core.add(c, (0.0, -r, 0.0)), core.add(c, (0.0, -r - 0.22, 0.0)), 0.025, "straw_rope", n=4,
                               vis=(1,), r1=0.012, wear=wear))
                else:
                    P.add(shide(core.add(c, (0.0, -r, 0.01)), wear="_w2"))
        else:
            P.add(shide((0.2, Y - 0.1, 0.02), s=0.12, wear="_w2"))
            P.add(litter(3, -L / 2 + 1.0, 0.3, 0.4))
            P.hung = False
        P.add(W(-L / 2, L / 2, Y - 0.12 * L / 1.82 - r, Y + r, -r, r, ROPE, vis=(2,)) if not ab else
              W(-L / 2, -L / 2 + 1.2, 0.0, Y, -0.02, 0.02, ROPE, vis=(2,)))
        P.solids[-1].wear = wear
        P.dim("span", L, L, tol=0.01)
        P.dim("rope_d", 0.07 if L < 2 else 0.09, 2 * r, tol=0.03)
        P.extra["hang_y"] = Y
        P.notes.append("anchors at y = 2.50 (torii tie beam, gate, well frame): move to the real anchor height")
    else:
        D = {"wrap_d06": 0.6, "wrap_d10": 1.0, "wrap_d16": 1.6}[kind]
        r = {0.6: 0.05, 1.0: 0.08, 1.6: 0.12}[D]
        Y = 1.6
        R = D / 2 + r * 0.7
        n = 14
        ring = [(R * math.cos(2 * math.pi * k / n), Y + 0.03 * math.sin(3 * 2 * math.pi * k / n), R * math.sin(2 * math.pi * k / n))
                for k in range(n + 1)]
        add_all(P, rope_twist(ring, r, n=6))
        # the knot and hanging ends at the front, shide round the tree
        add_all(P, rope_twist([(0.0, Y, R + r), (0.05, Y - 0.35, R + r + 0.03), (0.02, Y - 0.6, R + r + 0.05)], r * 0.6, n=5))
        ns = 6 if D < 1.5 else 8
        for i in range(ns):
            a = 2 * math.pi * (i + 0.5) / ns
            P.add(shide((R * 1.02 * math.cos(a), Y - r, R * 1.02 * math.sin(a)), s=0.28, wear="_w2",
                        yaw=-math.degrees(a) + 90.0))
        P.add(lathe([(R + r, Y - r), (R + r, Y + r)], 8, ROPE, vis=(2,), smooth=False))
        P.hung = True          # tied round a trunk at 1.6 m, nothing on the ground
        P.anchor = "floor"
        P.dim("trunk_d", D, D, tol=0.001)
        P.dim("rope_d", 2 * r, 2 * r, tol=0.001)
        P.extra["trunk_d"] = D
        P.notes.append("origin = the trunk centre at the ground; the rope rings the trunk at 1.6 m")
    return P


PROPS = [
    {"id": "jp_s_straw_stack", "cat": "yard", "notes": ["AUTUMN signature; nio at field edges and threshing yards, "
                                                        "bales under an eave only"],
     "models": [
         M("jp_s_straw_stack_nio_cyl", "nio_cyl", "intact", "Straw stack, cylinder with conical cap (Kinai)",
           lambda: straw_stack("nio_cyl")),
         M("jp_s_straw_stack_nio_cone", "nio_cone", "intact", "Straw stack, conical (Kanto)", lambda: straw_stack("nio_cone")),
         M("jp_s_straw_stack_stook", "stook", "intact", "Rice sheaves leaning in a stook", lambda: straw_stack("stook")),
         M("jp_s_straw_stack_bundle", "bundle", "intact", "Tied straw bundle", lambda: straw_stack("bundle")),
         M("jp_s_straw_stack_tawara_stack", "tawara_stack", "intact", "Rice bales stacked (5)",
           lambda: straw_stack("tawara_stack")),
         M("jp_s_straw_stack_ab_slumped", "nio_cyl", "abandoned", "Straw stack slumped, cap blown off",
           lambda: straw_stack("ab_slumped")),
     ]},
    {"id": "jp_s_shimenawa", "cat": "roadside", "notes": ["no collision (rope); lengths hang between two anchors at "
                                                          "2.50 m, wraps ring a trunk at 1.6 m"],
     "models": [
         M("jp_s_shimenawa_len_1ken", "len_1ken", "intact", "Straw rope with streamers, 1 ken", lambda: shimenawa("len_1ken")),
         M("jp_s_shimenawa_len_2ken", "len_2ken", "intact", "Straw rope with streamers, 2 ken", lambda: shimenawa("len_2ken")),
         M("jp_s_shimenawa_wrap_d06", "wrap", "intact", "Straw rope round a 0.6 m trunk", lambda: shimenawa("wrap_d06")),
         M("jp_s_shimenawa_wrap_d10", "wrap", "intact", "Straw rope round a 1.0 m trunk", lambda: shimenawa("wrap_d10")),
         M("jp_s_shimenawa_wrap_d16", "wrap", "intact", "Straw rope round a 1.6 m trunk (landmark tree)",
           lambda: shimenawa("wrap_d16")),
         M("jp_s_shimenawa_ab_tattered", "len_1ken", "abandoned", "Straw rope grey and frayed, one end dropped",
           lambda: shimenawa("ab_tattered")),
     ]},
]
