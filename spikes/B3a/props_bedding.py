"""Bedding and mats (BUILD_LIST rows 33-35): futon_stack, futon_laid, mushiro."""
import math
import random

import fkit
import bits
from fkit import (core, box, sheet, lathe, xf, xfs, flat_poly, W, col, FPart, rest,
                  WOOD, INDIGO, KINARI, MUSHIRO, TAWARA, LITTER)
from bits import pillow, stain

CAT = "bedding"
ROPE = "straw_rope"


def add_all(P, ss):
    for s in ss:
        P.add(s)


# ================================================================================================ futon stack
def folded(w, d, h, mat, wear=None, vis=(1,), sag=0.0, edge=None):
    """One folded futon / quilt: a soft slab with rounded folds front and back (bits.soft_slab)."""
    return [bits.soft_slab(w, d, h, mat, wear=wear, vis=vis)]


def makura(wear=None):
    """Tube pillow (kukuri-makura), 0.30 long, d 0.12, cotton."""
    s = fkit.lcyl("x", 0.06, 0.0, 0.06, -0.15, 0.15, KINARI, n=8, vis=(1,), caps=INDIGO)
    if wear:
        s.wear = wear
    return s


def futon_stack(state="stack"):
    P = FPart("futon_stack", budget="furniture", res3=False, mass=18.0)
    w, d = 0.95, 0.65
    layers = [(INDIGO, KINARI, 0.15, "_w1"), (KINARI, INDIGO, 0.14, "_w1"), (INDIGO, KINARI, 0.16, "_w0")]
    y = 0.0
    slump = state != "stack"
    for i, (m, e, h, wr) in enumerate(layers):
        wear = "_w2" if slump else wr
        if slump and i == 2:
            continue
        dx = [0.0, 0.02, -0.015][i] + (0.04 * i if slump else 0.0)
        yaw = [0.0, 2.0, -3.0][i] + (5.0 * i if slump else 0.0)
        add_all(P, xfs(folded(w, d, h, m, wear, sag=0.03 if slump else 0.0, edge=e), ry=yaw, t=(dx, y, 0.0)))
        y += h - 0.005
    if not slump:
        P.add(xf(makura(), ry=8.0, t=(0.18, y, -0.12)))
        top = y
    else:
        # the top quilt dragged half off: one fold still on the stack, the rest slumped down the side to the floor
        q1 = bits.soft_slab(0.60, d, 0.12, INDIGO, wear="_w2", vis=(1,))
        P.add(xf(q1, rz=-8.0, t=(0.25, y - 0.02, 0.0)))
        slope = bits.soft_slab(0.55, d, 0.10, INDIGO, wear="_w2", vis=(1,))
        P.add(xf(slope, rz=-58.0, t=(0.72, 0.235, 0.03)))
        floor = bits.soft_slab(0.50, d + 0.05, 0.08, INDIGO, wear="_w2", vis=(1,))
        P.add(xf(floor, ry=6.0, t=(1.02, 0.0, 0.02)))
        P.add(rest([xf(makura("_w2"), ry=60.0, t=(-0.62, 0.0, 0.30))])[0])
        P.add(col(0.62, 1.30, 0.0, 0.08, -0.33, 0.35))
        top = y
    P.add(W(-w / 2, w / 2, 0.0, top, -d / 2, d / 2, INDIGO, vis=(2,)))
    P.add(col(-w / 2 + 0.02, w / 2 - 0.02, 0.0, top - 0.01, -d / 2 + 0.02, d / 2 - 0.02, INDIGO))
    # loot on top of the stack (on the pillow-free side)
    ty = top_point_y(P, -0.20, 0.10)
    P.loot_rect("top", ty, -0.4, 0.4, -0.25, 0.25, rng=0.25, points=[(-0.20, ty, 0.10)])
    P.dim("stack_w", 0.95, 0.95, tol=0.01)
    P.dim("stack_h", 0.45 if not slump else 0.29, top, tol=0.02)
    return P


def top_point_y(P, x, z):
    """Highest Res 1 surface at (x, z) (for loot on soft shapes)."""
    import build
    lod = P._visual(1)
    hit = build._ray_down(lod, x, z, 5.0)
    return round(hit[0], 4) if hit else 0.0


# ================================================================================================ futon laid
FL, FW = 1.85, 0.95


def futon_laid(state="thrown"):
    P = FPart("futon_laid", budget="small", mass=8.0)
    dragged = state != "thrown"
    wear = "_w2" if dragged else None
    # the mattress (shikibuton): 0.08 slab, the head at -x
    mat = bits.soft_slab(FL, FW, 0.08, KINARI, n=3, wear=wear, vis=(1,))
    P.add(mat)
    # indigo cover band along the edges (the ticking shows at the sides)
    for sz in (-1, 1):
        e = W(-FL / 2 + 0.02, FL / 2 - 0.02, 0.0, 0.045, sz * FW / 2 - 0.004, sz * FW / 2 + 0.004, INDIGO, vis=(1,))
        if wear:
            e.wear = wear
        P.add(e)
    P.add(W(-FL / 2, FL / 2, 0.0, 0.07, -FW / 2, FW / 2, KINARI, vis=(2,)))
    if not dragged:
        # the quilt (kakebuton) over the foot half, its top end thrown back on itself
        q = bits.soft_slab(FW + 0.04, 1.00, 0.07, INDIGO, n=3, vis=(1,))
        P.add(xf(q, ry=90.0, t=(0.42, 0.072, 0.0)))
        fold = bits.soft_slab(FW + 0.04, 0.45, 0.08, INDIGO, n=3, vis=(1,))
        P.add(xf(fold, ry=90.0, t=(0.17, 0.138, 0.0)))
        P.add(W(-0.08, 0.92, 0.07, 0.22, -FW / 2, FW / 2, INDIGO, vis=(2,)))
        P.add(xf(makura(), ry=90.0, t=(-0.80, 0.075, 0.0)))
        pts = [(-0.45, 0.08, 0.20), (-0.45, 0.08, -0.20)]
    else:
        # quilt dragged aside onto the floor, crumpled; the pillow apart
        q = bits.soft_slab(1.10, 0.90, 0.10, INDIGO, n=3, wear="_w2", vis=(1,))
        P.add(xf(q, ry=25.0, t=(0.55, 0.0, 0.85)))
        P.add(xf(W(-0.5, 0.5, 0.0, 0.08, -0.4, 0.4, INDIGO, vis=(2,)), ry=25.0, t=(0.55, 0.0, 0.85)))
        P.add(rest([xf(makura("_w2"), ry=20.0, t=(-1.25, 0.0, -0.25))])[0])
        P.add(stain(90, -0.2, 0.0, 0.25, y=0.083, mat=LITTER, wear="_w1"))
        pts = [(-0.45, 0.08, 0.05), (0.40, 0.08, -0.10)]
    # thin Geometry slab + Roadway (like vanilla beds): items rest on it, a player steps over it
    P.add(col(-FL / 2, FL / 2, 0.0, 0.08, -FW / 2, FW / 2, KINARI))
    P.road([(-FL / 2, 0.08, -FW / 2), (FL / 2, 0.08, -FW / 2), (FL / 2, 0.08, FW / 2), (-FL / 2, 0.08, FW / 2)],
           "tatami")
    fixed = []
    for x, y, z in pts:
        fixed.append((x, top_point_y(P, x, z), z))
    P.loot_rect("mattress", fixed[0][1], -FL / 2 + 0.1, FL / 2 - 0.1, -FW / 2 + 0.1, FW / 2 - 0.1, rng=0.4,
                kind="shelf", points=fixed)
    P.dim("L", FL, FL, tol=0.01)
    P.dim("W", FW, FW, tol=0.01)
    P.notes.append("0.08 Geometry slab + Roadway (textile_carpet_int) like vanilla beds; never across a door band")
    return P


# ================================================================================================ mushiro
MW, MD = 1.82, 0.91


def mat_flat(w=MW, d=MD, y=0.0, t=0.008, wear=None, cut=None, vis=(1,)):
    """A flat straw mat: top face, thin edges, bound long edges (straw rope). cut = drop the +x+z corner
    (the torn / curled variant)."""
    x0, x1, z0, z1 = -w / 2, w / 2, -d / 2, d / 2
    if cut:
        pts = [(x0, z0), (x1, z0), (x1, z1 - cut), (x1 - cut, z1), (x0, z1)]
    else:
        pts = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    top = flat_poly(pts, y + t, MUSHIRO, vis=vis, wear=wear)
    out = [top]
    n = len(pts)
    quads, normals = [], []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        q = [(a[0], y, a[1]), (b[0], y, b[1]), (b[0], y + t, b[1]), (a[0], y + t, a[1])]
        nn = core.norm((b[1] - a[1], 0.0, -(b[0] - a[0])))
        quads.append(q)
        normals.append(nn)
    sd = sheet(quads, MUSHIRO, normals, vis=vis)
    if wear:
        sd.wear = wear
    out.append(sd)
    for sz in (-1, 1):
        xe = x1 - (cut if (cut and sz > 0) else 0.0)
        e = W(x0, xe, y, y + t + 0.004, sz * d / 2 - 0.012 * (sz > 0), sz * d / 2 + 0.012 * (sz < 0), ROPE, vis=(1,))
        if wear:
            e.wear = wear
        out.append(e)
    return out


def mushiro(state="flat"):
    P = FPart("mushiro", budget="small", mass=3.0, flat=state in ("flat", "torn", "pile", "pile_spread"))
    if state == "flat":
        add_all(P, mat_flat())
        P.add(flat_poly([(-MW / 2, -MD / 2), (MW / 2, -MD / 2), (MW / 2, MD / 2), (-MW / 2, MD / 2)], 0.008, MUSHIRO,
                        vis=(2,)))
        P.dim("w", MW, MW, tol=0.005)
    elif state == "torn":
        cut = 0.35
        add_all(P, mat_flat(wear="_w2", cut=cut))
        # the curled corner: a triangle bent up off the floor, both sides visible
        a, b = (MW / 2, MD / 2 - cut), (MW / 2 - cut, MD / 2)
        tip = (MW / 2 - 0.02, 0.16, MD / 2 - 0.02)
        mid = ((a[0] + b[0]) / 2 + 0.03, 0.05, (a[1] + b[1]) / 2 + 0.03)
        tris = [[(a[0], 0.008, a[1]), (b[0], 0.008, b[1]), mid], [(a[0], 0.008, a[1]), mid, tip],
                [(b[0], 0.008, b[1]), tip, mid]]
        quads, normals = [], []
        for t_ in tris:
            n = core.norm(core.newell(t_))
            quads += [t_, t_[::-1]]
            normals += [n, core.mul(n, -1.0)]
        c = sheet(quads, MUSHIRO, normals, vis=(1,))
        c.wear = "_w2"
        P.add(c)
        # a torn hole: dark straw litter over it, straw bits around
        P.add(stain(95, -0.3, 0.05, 0.30, y=0.011, sx=1.4))
        P.add(stain(96, 0.95, 0.30, 0.35, y=0.003, wear="_w1"))
        P.add(flat_poly([(-MW / 2, -MD / 2), (MW / 2, -MD / 2), (MW / 2, MD / 2 - cut), (MW / 2 - cut, MD / 2),
                         (-MW / 2, MD / 2)], 0.008, MUSHIRO, vis=(2,)))
        P.dim("w", MW, MW, tol=0.005)
    elif state in ("rolled", "rolled_loose"):
        # a mat rolled up along its short side: d 0.18 x 0.91, the loose end lying out on the floor;
        # rolled_loose: half unrolled, a longer tail, straw litter
        loose = state == "rolled_loose"
        r = 0.09 if not loose else 0.065
        roll = lathe([(0.0, -MD / 2), (0.07, -MD / 2), (r, -MD / 2 + 0.01), (r, MD / 2 - 0.01), (0.07, MD / 2),
                      (0.0, MD / 2)], 10, MUSHIRO, vis=(1,))
        roll = xf(roll, rx=90.0, t=(0.0, r + 0.006, 0.0))
        P.add(roll)
        for zc in (-0.25, 0.25):
            s = bits.rope_ring(r, zc, 0.02, ROPE, 10, proud=0.006)
            P.add(xf(s, rx=90.0, t=(0.0, r + 0.006, 0.0)))
        tw = 0.22 if not loose else 0.95
        tail = mat_flat(w=tw, d=MD - 0.02, t=0.006, wear="_w2" if loose else None)
        add_all(P, xfs(tail, t=(r + tw / 2 - 0.01, 0.0, 0.0)))
        if loose:
            P.add(stain(97, 0.5, 0.35, 0.35, y=0.012, wear="_w1"))
            for s in P.solids:
                if not getattr(s, "wear", None):
                    s.wear = "_w2"
        P.add(fkit.lcyl("z", 0.0, r + 0.006, r, -MD / 2, MD / 2, MUSHIRO, n=6, vis=(2,)))
        P.add(fkit.col_solid(fkit.lcyl("z", 0.0, r, r, -MD / 2, MD / 2, MUSHIRO, n=8)))
        P.dim("roll_d", 0.18 if not loose else 0.13, 2 * r, tol=0.005)
        P.dim("roll_L", 0.91, 0.91, tol=0.005)
    else:   # pile: three mats folded in half, stacked a little askew; pile_spread: slid apart (abandoned)
        spread = state == "pile_spread"
        offs = ((0.0, 0.0, 0.0), (6.0, 0.02, -0.01), (-4.0, 0.04, -0.02)) if not spread else             ((0.0, 0.0, 0.0), (25.0, 0.35, 0.10), (-15.0, -0.30, 0.25))
        for i, (yaw, dx, dz) in enumerate(offs):
            m = mat_flat(w=MD, d=MD, y=0.02 * i if not spread else 0.019 * (i > 0), t=0.018,
                         wear="_w2" if spread else None)
            add_all(P, xfs(m, ry=yaw, t=(dx, 0.0, dz)))
        if spread:
            P.add(stain(98, 0.2, 0.5, 0.35, y=0.003, wear="_w1"))
        P.add(flat_poly([(-MD / 2, -MD / 2), (MD / 2, -MD / 2), (MD / 2, MD / 2), (-MD / 2, MD / 2)], 0.058, MUSHIRO,
                        vis=(2,)))
        P.dim("pile_w", MD, MD, tol=0.005)
    P.notes.append("flat mats have no Geometry (BUILD_LIST Q5 rule 1) and do not subtract from floor loot")
    return P


def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_futon_stack", "cat": CAT, "models": [
        M("jp_f_futon_stack", "stack", "intact", "Folded bedding stack (futon, yogi)", lambda: futon_stack("stack")),
        M("jp_f_futon_stack_slumped", "stack", "slumped", "Bedding stack slumped, quilt dragged off",
          lambda: futon_stack("slumped")),
    ]},
    {"id": "jp_f_futon_laid", "cat": CAT, "models": [
        M("jp_f_futon_laid", "thrown", "intact", "Laid-out bedding, quilt thrown back", lambda: futon_laid("thrown")),
        M("jp_f_futon_laid_dragged", "thrown", "dragged", "Laid-out bedding, quilt dragged aside, stained",
          lambda: futon_laid("dragged")),
    ]},
    {"id": "jp_f_mushiro", "cat": CAT, "models": [
        M("jp_f_mushiro", "flat", "intact", "Straw floor mat (mushiro)", lambda: mushiro("flat")),
        M("jp_f_mushiro_torn", "flat", "torn", "Straw mat, torn, corner curled", lambda: mushiro("torn")),
        M("jp_f_mushiro_rolled", "rolled", "intact", "Straw mat, rolled", lambda: mushiro("rolled")),
        M("jp_f_mushiro_rolled_loose", "rolled", "loose", "Straw mat, half unrolled", lambda: mushiro("rolled_loose")),
        M("jp_f_mushiro_pile", "pile", "intact", "Straw mats, small pile", lambda: mushiro("pile")),
        M("jp_f_mushiro_pile_spread", "pile", "spread", "Straw mats, pile slid apart", lambda: mushiro("pile_spread")),
    ]},
]
