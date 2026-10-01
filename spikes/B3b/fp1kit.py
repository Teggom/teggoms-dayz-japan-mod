"""fp1kit - FP1 (2026-10-01, Stephen's showcase walk) remakes shared by the site (B3b / L2) and furniture (L1 / S1)
pipelines: the Japanese brooms (hoki), rice-straw sheaves (inaba), potted plants and bonsai, the sword-rack swords.

Research (general knowledge, no web request; choices recorded in spikes/FP1/FP1_PROGRESS.md 'Forms'):
- take-boki (outdoor yard broom): a bundle of thin bamboo branchlets ~0.5-0.6 m long bound round the foot of a
  bamboo handle (~1.2 m, d ~2.5 cm, nodes every ~0.3 m) with two or three straw-rope / cane bindings; the twigs fan out
  flat to ~0.45 m at the tip, a little thicker in the middle.
- zashiki-boki (indoor / shop broom): sorghum or millet straw (hoki-kibi) flattened into a fan and sewn through with
  three or four rows of cord, the end cut square; a short bamboo or wooden handle.
- rice sheaf (inaba): a sheaf tied at the neck (about a third up from the cut end); on a hasa rack it is split in two
  below the tie and hung astride the pole, the cut ends up at the pole, the two halves hanging down either side, ears
  (heads) down and spread; in a stook the sheaves stand butts down, ears up, leaning together.
Frames: as skit (y up, +z front). All visual only; callers add collision.
"""
import math
import random

import skit
from skit import core, xf, xfs, pole, lathe, add_all  # noqa: F401

BAMBOO = "bamboo_weathered"
ROPE = "straw_rope"
STACK = "straw_stack"
TAWARA = "straw_tawara"


def _wear(ss, wear):
    if wear:
        for s in ss:
            s.wear = wear
    return ss


def bundle(p0, p1, w0, d0, w1, d1, mat, n=6, vis=(1,), mid=None, rot=0.0, caps=(True, True)):
    """A closed tapered bundle from p0 to p1 (any direction): an n-gon section, w (across, the bundle's x after
    `rot`) by d (thickness), w0/d0 at p0 and w1/d1 at p1; mid = (t, wm, dm) adds a middle ring. Smooth normals."""
    rings_ = [(0.0, w0, d0)] + ([mid] if mid else []) + [(1.0, w1, d1)]
    axis = core.sub(p1, p0)
    L = core.length(axis)
    t = core.norm(axis)
    ref = (0.0, 0.0, 1.0) if abs(t[2]) < 0.9 else (1.0, 0.0, 0.0)
    a = core.norm(core.cross(ref, t))
    b = core.norm(core.cross(t, a))
    ca, sa = math.cos(rot), math.sin(rot)
    a, b = core.add(core.mul(a, ca), core.mul(b, sa)), core.add(core.mul(b, ca), core.mul(a, -sa))
    verts, faces = [], []
    for (tt, w, d) in rings_:
        c = core.add(p0, core.mul(axis, tt))
        for k in range(n):
            ang = math.pi / n + 2 * math.pi * k / n
            verts.append(core.add(c, core.add(core.mul(a, w / 2 * math.cos(ang)), core.mul(b, d / 2 * math.sin(ang)))))
    nr = len(rings_)
    if caps[0]:
        faces.append(list(range(n))[::-1])
    if caps[1]:
        faces.append(list(range(n * (nr - 1), n * nr)))
    for r in range(nr - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append([r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i])
    if all(caps):
        s = core.Solid(verts, faces, mat, vis=vis)
    else:                                   # open at an end hidden inside another bundle: explicit outward normals
        cen = core.mul(core.add(p0, p1), 0.5)
        nrm = []
        for f in faces:
            fp = [verts[i] for i in f]
            nn = core.norm(core.newell(fp))
            fc = tuple(sum(p[k] for p in fp) / len(fp) for k in range(3))
            if len(f) == n:                 # a cap: along the axis
                nn = core.mul(t, 1.0 if core.dot(core.sub(fc, cen), t) > 0 else -1.0)
            else:
                rc = core.add(p0, core.mul(t, core.dot(core.sub(fc, p0), t)))
                if core.dot(nn, core.sub(fc, rc)) < 0:
                    nn = core.mul(nn, -1.0)
            nrm.append(nn)
        s = core.Solid(verts, faces, mat, vis=vis, normals=nrm)
    s.uv = "grain"
    s.finalize()
    import fkit
    fkit.auto_smooth(s, 75.0)
    return s


# ------------------------------------------------------------------------------------------------ brooms
TWIG = "wood_weathered"            # the branchlets: brown-grey, darker than the pale bamboo handle


def take_boki(seed=1, wear=None, vis=(1,), twigs=22):
    """Outdoor bamboo-twig broom, built standing (handle butt at the origin, head up +y, the fan spread along x, thin
    in z). Length 1.78: handle 0-1.45 (d 0.026, three nodes), the twig bundle bound at 1.18 and 1.36, twigs fanning to
    0.46 wide at 1.62-1.80. Lay it down with xfs(..., rx=90) (+y -> +z) and skit.rest()."""
    rg = random.Random(seed)
    out = [pole((0.0, 0.0, 0.0), (0.0, 1.45, 0.0), 0.013, BAMBOO, n=6, vis=vis, r1=0.012)]
    for y in (0.32, 0.66, 0.98):                                      # bamboo nodes
        out.append(lathe([(0.0135, y - 0.008), (0.0150, y), (0.0135, y + 0.008)], 6, BAMBOO, vis=vis, smooth=True))
    # the bound neck of the twig bundle round the handle, flaring into the fan
    out.append(bundle((0.0, 1.12, 0.0), (0.0, 1.50, 0.0), 0.052, 0.040, 0.15, 0.050, BAMBOO, n=6, vis=vis,
                      mid=(0.55, 0.085, 0.046)))
    for y, w, d in ((1.18, 0.0615, 0.0417), (1.36, 0.097, 0.0467)):  # straw-rope bindings, a little proud
        out.append(bundle((0.0, y - 0.013, 0.0), (0.0, y + 0.013, 0.0), w + 0.010, d + 0.008, w + 0.010, d + 0.008,
                          ROPE, n=6, vis=vis))
    # the dense inner mass of the fan (the twigs packed together), thinning towards the tip
    out.append(bundle((0.0, 1.46, 0.0), (0.0, 1.66, 0.0), 0.15, 0.048, 0.36, 0.020, TWIG, n=6, vis=vis))
    # twigs: from the neck out to the fan edge, each with a side branchlet
    for i in range(twigs):
        u = (i + 0.5) / twigs * 2 - 1                                # -1 .. 1 across the fan
        x0 = 0.055 * u + rg.uniform(-0.01, 0.01)
        y0 = 1.44 + rg.uniform(-0.03, 0.03)
        z0 = rg.uniform(-0.018, 0.018)
        x1 = 0.24 * u + rg.uniform(-0.03, 0.03)
        y1 = 1.72 + 0.08 * (1 - abs(u)) + rg.uniform(-0.05, 0.04)
        z1 = rg.uniform(-0.03, 0.03)
        out.append(pole((x0, y0, z0), (x1, y1, z1), 0.0065, TWIG, n=3, vis=vis, r1=0.0025))
        t = rg.uniform(0.35, 0.65)
        bx, by, bz = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z0 + (z1 - z0) * t
        side = 1 if (u > 0) == (rg.random() < 0.75) else -1
        L = rg.uniform(0.09, 0.16)
        ang = math.radians(rg.uniform(18, 32)) * side
        dx, dy = math.sin(ang), math.cos(ang)
        out.append(pole((bx, by, bz), (bx + dx * L, by + dy * L, bz + rg.uniform(-0.02, 0.02)), 0.0035, TWIG, n=3,
                        vis=vis, r1=0.0015))
    return _wear(out, wear)


def lying_boki(seed=1, wear=None, vis=(1,)):
    """take_boki laid on the ground along +z (the twigs at +z), resting on the fan and the handle butt."""
    ss = xfs(take_boki(seed, wear, vis), rx=90.0)
    return skit.rest(ss, 0.0)


def zashiki_boki(x0, x1, z, y0=0.0, wear=None, vis=(1,), seed=3):
    """Indoor / shop broom of sorghum straw lying along x on its flat side: handle x0 -> 60 %, a flat fan head sewn
    with three rows of cord, the end cut square with a few stray straws."""
    rg = random.Random(seed)
    L = x1 - x0
    hx = x0 + L * 0.55
    out = [pole((x0, y0 + 0.011, z), (hx + 0.03, y0 + 0.011, z), 0.010, BAMBOO, n=5, vis=vis)]
    # the head: a flat bundle widening from the binding to the cut end (thin in y)
    head = bundle((hx, y0 + 0.012, z), (x1, y0 + 0.012, z), 0.034, 0.022, 0.16, 0.014, TAWARA, n=4, vis=vis,
                  mid=(0.45, 0.10, 0.020), rot=math.pi / 2)
    head = _orient_flat(head, y0)
    out.append(head)
    for t in (0.12, 0.42, 0.70):                                     # sewn cord rows across the fan (on its top)
        x = hx + (x1 - hx) * t
        w = (0.034 + (0.16 - 0.034) * t) * 0.72
        yt = y0 + 0.012 + (0.011 - 0.004 * t) + 0.0015
        q = core.sheet([[(x - 0.004, yt, z - w / 2), (x + 0.004, yt, z - w / 2), (x + 0.004, yt, z + w / 2),
                         (x - 0.004, yt, z + w / 2)]], "wood_kuro", (0.0, 1.0, 0.0), vis=vis)
        q.finalize()
        out.append(q)
    out.append(core.box(hx - 0.01, hx + 0.02, y0, y0 + 0.026, z - 0.02, z + 0.02, ROPE, vis=vis))   # the binding
    for k in range(2):                                               # stray straws at the cut end
        zz = z + rg.uniform(-0.07, 0.07)
        out.append(pole((x1 - 0.01, y0 + 0.010, zz), (x1 + rg.uniform(0.02, 0.05), y0 + 0.006, zz + rg.uniform(-0.02, 0.02)),
                        0.0025, TAWARA, n=3, vis=vis))
    return _wear(out, wear)


def _orient_flat(s, y0):
    """bundle() along x puts its width in z and thickness in y when built with rot 0 about x: check and keep the
    lowest point on y0."""
    lo = min(v[1] for v in s.verts)
    return xf(s, t=(0.0, y0 - lo, 0.0))


# ------------------------------------------------------------------------------------------------ rice sheaves
def sheaf_half(top, length, side, rg, wear=None, ear_wear=None, vis=(1,), splay=0.10):
    """One half of a sheaf hung astride a pole: from `top` (just beside the pole) down `length`, leaning out to
    `side` (+1 / -1 along z), stalks narrow at the neck, the ear end wider and golden, the heads drooping."""
    x, y, z = top
    lean = splay + rg.uniform(-0.03, 0.04)
    mid = (x + rg.uniform(-0.01, 0.01), y - length * 0.55, z + side * lean * 0.55)
    end = (x + rg.uniform(-0.03, 0.03), y - length, z + side * lean)
    w = rg.uniform(0.13, 0.155)
    rot = math.pi / 4 + rg.uniform(-0.2, 0.2)          # a 4-gon turned 45 deg, smooth-shaded: reads round
    stalk = bundle(top, mid, w * 0.50, w * 0.40, w * 0.85, w * 0.52, STACK, n=4, vis=vis, rot=rot, caps=(False, False))
    ears = bundle(mid, end, w * 0.85, w * 0.52, w * 1.10, w * 0.58, STACK, n=4, vis=vis, mid=(0.6, w * 1.18, w * 0.62),
                  rot=rot, caps=(False, True))
    return _wear([stalk], wear or "_w0") + _wear([ears], ear_wear or "_w0")


def hung_sheaf(x, y_pole, z_pole, r_pole, length, rg, wear=None, vis=(1,)):
    """A rice sheaf hung astride a horizontal pole along x at (y_pole, z_pole): the tied neck and cut ends sit on
    top of the pole (nothing clips the pole: the neck rides over it), the halves hang down both sides."""
    out = []
    yt = y_pole + r_pole * 0.35
    for side in (-1, 1):
        top = (x, yt, z_pole + side * (r_pole + 0.030))
        out += sheaf_half(top, length * rg.uniform(0.9, 1.05), side, rg, wear=wear,
                          ear_wear=None if not wear else wear, vis=vis)
    # the neck over the pole: a short saddle bundle across the top (the cut stalk ends and the tie)
    neck = bundle((x, y_pole + r_pole + 0.020, z_pole - r_pole - 0.045), (x, y_pole + r_pole + 0.020, z_pole + r_pole + 0.045),
                  0.055, 0.050, 0.055, 0.050, ROPE, n=4, vis=vis, rot=math.pi / 4)     # the tied neck (straw rope)
    out += _wear([neck], wear)
    return out


def standing_sheaf(base, top, rg, wear=None, vis=(1,)):
    """A sheaf standing in a stook: butt (cut end) on the ground at `base`, ears up at `top`, tied a third up."""
    w = rg.uniform(0.13, 0.16)
    m = core.add(base, core.mul(core.sub(top, base), 0.40))
    stalk = bundle(base, m, w * 0.95, w * 0.85, w * 0.62, w * 0.55, STACK, n=5, vis=vis, rot=rg.uniform(0, 1))
    ears = bundle(m, top, w * 0.62, w * 0.55, w * 1.05, w * 0.80, STACK, n=5, vis=vis, mid=(0.55, w * 1.2, w * 0.85),
                  rot=rg.uniform(0, 1))
    tie = bundle(core.add(m, core.mul(core.norm(core.sub(top, base)), -0.02)),
                 core.add(m, core.mul(core.norm(core.sub(top, base)), 0.02)), w * 0.70, w * 0.62, w * 0.70, w * 0.62,
                 ROPE, n=5, vis=vis)
    return _wear([stalk], wear or "_w0") + _wear([ears], wear or "_w0") + _wear([tie], wear)
