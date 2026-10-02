"""fx2props.py - FX2 (2026-10-01): the sculpted statue meshes (statues.py) as kit solids, plus the kit pieces that go
with them: halos (wheel, boat, disc), octagonal pedestal tiers, the lotus seat. Imported by the prop builders
(spikes/W2F/props_w2f_sacred.py, spikes/B3b/props_stone.py, props_grave.py, props_fx2.py).

Frame as the kits: +y up, +z = the figure's front, origin on the floor under the figure's centre. DayZ model space is
left-handed: +x is the FIGURE'S RIGHT hand side (the viewer's left) in game; the renders flip to match.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
import statues as ST  # noqa: E402
import statuekit as K  # noqa: E402
from jpparts import core  # noqa: E402

GILT = "gilt_worn"


def figure(name, H, mats, vis=((1,), (2,), (3,)), t=(0.0, 0.0, 0.0), sz=1.0, wear=None, ry=0.0, keep=None):
    """Statue `name` scaled to height H (its canonical 1.0), placed at t, turned ry degrees about y.
    vis: the LOD sets for mesh LOD 0, 1, 2 (None / () skips one). mats: one material or {part key: material}."""
    md = ST.get(name)
    M = None
    if ry:
        import sdf
        M = sdf.rotm(0.0, ry, 0.0)
    out = []
    for lod, v in enumerate(vis):
        if not v:
            continue
        ss = K.to_solids(md, lod, mats, tuple(v), M=M, t=t, s=H, sz=sz, wear=wear, keep=keep)
        for s in ss:
            s.no_dust = True
        out += ss
    return out


def faces(name):
    return ST.get(name)["faces"]


def tag_parts(name, H, mats, vis, t=(0.0, 0.0, 0.0), wear=None):
    """As figure(), but returns {part key: [solids]} (e.g. to topple the head separately)."""
    md = ST.get(name)
    out = {}
    for p in md["parts"]:
        out[p["key"]] = figure(name, H, mats, vis=vis, t=t, wear=wear, keep=lambda k, pk=p["key"]: k == pk)
    return out


def lotus(R, mat, vis=((1,), (2,), (3,)), t=(0.0, 0.0, 0.0), wear=None):
    """Lotus seat of top radius R (petal tips reach ~1.2 R); its top (where the figure stands) is 0.60 R above t."""
    return figure("lotus", 2.0 * R, mat, vis=vis, t=t, wear=wear)


def lotus_top(R):
    return 0.60 * R


def octagon_tiers(tiers, mat, vis=(1, 2), wear=None, y0=0.0):
    """Stacked octagonal slabs [(radius, height), ...] from y0 up (the pedestal's base tiers). Returns (solids, top)."""
    out = []
    y = y0
    for r, h in tiers:
        out.append(_lathe([(0.0, y), (r, y), (r, y + h), (0.0, y + h)], 8, mat, vis, wear))
        y += h
    return out, y


def _lathe(prof, n, mat, vis, wear):
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    import fkit
    s = fkit.lathe(prof, n, mat, vis=vis, phase=math.pi / n, smooth=False)
    if wear:
        s.wear = wear
    return s


def ring(r_in, r_out, t, mat, n=24, vis=(1,), wear=None):
    """A flat annulus in the x-y plane (facing +z), thickness t, centred on the origin."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    import fkit
    s = fkit.lathe([(r_in, -t / 2), (r_out, -t / 2), (r_out, t / 2), (r_in, t / 2), (r_in, -t / 2)], n, mat, vis=vis,
                   smooth=False)
    s = fkit.xf(s, rx=90.0)
    if wear:
        s.wear = wear
    return s


def disc(r, t, mat, n=20, vis=(1,), wear=None):
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    import fkit
    s = fkit.lathe([(0.0, -t / 2), (r, -t / 2), (r, t / 2), (0.0, t / 2)], n, mat, vis=vis, smooth=False)
    s = fkit.xf(s, rx=90.0)
    if wear:
        s.wear = wear
    return s


def halo_wheel(cy, r_head, r_body, mat, z=0.0, vis=(1,), wear=None, cy_head=None):
    """Amida's halo (Met 44890): a large wheel (rinko) round the upper body, its rim openwork-like (a ring with knobs),
    eight spokes, and the head halo (a disc with a lotus centre) inside it. Faces +z, centre (0, cy, z)."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    import fkit
    ch = cy if cy_head is None else cy_head
    out = []
    out.append(fkit.xf(ring(r_body * 0.86, r_body, 0.014, mat, n=28, vis=vis, wear=wear), t=(0.0, cy, z)))
    for k in range(16):                                         # knobs on the rim (the openwork flames, simplified)
        a = 2 * math.pi * (k + 0.5) / 16
        out.append(fkit.xf(disc(r_body * 0.075, 0.014, mat, n=6, vis=vis, wear=wear),
                           t=(r_body * 1.02 * math.cos(a), cy + r_body * 1.02 * math.sin(a), z)))
    for k in range(8):                                          # spokes
        a = 2 * math.pi * k / 8 + math.pi / 8
        p0 = (r_head * 0.95 * math.cos(a), ch + r_head * 0.95 * math.sin(a))
        p1 = (r_body * 0.87 * math.cos(a), cy + r_body * 0.87 * math.sin(a))
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        b = core.box(-L / 2, L / 2, -0.008, 0.008, -0.005, 0.005, mat, vis=vis)
        b = fkit.xf(b, rz=ang, t=((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, z))
        if wear:
            b.wear = wear
        out.append(b)
    out.append(fkit.xf(ring(r_head * 0.80, r_head, 0.016, mat, n=24, vis=vis, wear=wear), t=(0.0, ch, z + 0.002)))
    out.append(fkit.xf(disc(r_head * 0.80, 0.008, mat, n=24, vis=vis, wear=wear), t=(0.0, ch, z - 0.004)))
    for k in range(8):                                          # the lotus centre of the head halo
        a = 2 * math.pi * k / 8
        out.append(fkit.xf(disc(r_head * 0.16, 0.012, mat, n=6, vis=vis, wear=wear),
                           t=(r_head * 0.32 * math.cos(a), ch + r_head * 0.32 * math.sin(a), z + 0.004)))
    return out


def boat_points(w, h, flames=True):
    """The boat-shaped halo (funagata kohai) outline, base on y 0: [(x, y)] counter-clockwise."""
    pts = []
    n = 14
    for i in range(n + 1):
        t = i / n
        y = h * t
        half = w / 2 * (math.sin(math.pi * (0.22 + 0.78 * t)) * (1.0 - 0.25 * t)) if t < 1 else 0.0
        if flames and 0 < i < n and i % 2:
            half *= 1.07
        pts.append((half, y))
    right = pts
    left = [(-x, y) for x, y in reversed(pts[:-1])]
    return [(0.0, 0.0)] + right[1:] + left[:-1] if False else right + left[1:]


def halo_boat(w, h, mat, z=-0.02, t=0.025, vis=(1,), wear=None, head=None):
    """Boat-shaped halo (Shaka, Kannon, Jizo; CMA 147590 frame, CMA 152018): a flat pointed slab with a flame edge, a
    raised inner border, and a round head halo (head = (cy, r))."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "B3a"))
    import fkit
    pts = boat_points(w, h)
    xs = [p[0] for p in pts]
    out = []
    # the slab as a fan of convex quads (prism needs a convex outline): strips between successive heights
    half = sorted({round(abs(x), 5) for x in xs})
    rows = [(abs(pts[i][0]), pts[i][1]) for i in range(len(pts)) if pts[i][0] >= 0]
    rows.sort(key=lambda r: r[1])
    for (x0, y0), (x1, y1) in zip(rows, rows[1:]):
        poly = [(-x0, y0), (x0, y0), (x1, y1), (-x1, y1)] if x1 > 1e-6 else [(-x0, y0), (x0, y0), (0.0, y1)]
        s = core.prism(poly, "z", z - t / 2, z + t / 2, mat, vis=vis)
        if wear:
            s.wear = wear
        out.append(s)
    if head:
        cy, r = head
        out.append(fkit.xf(ring(r * 0.82, r, 0.012, mat, n=22, vis=vis, wear=wear), t=(0.0, cy, z + t / 2 + 0.004)))
        out.append(fkit.xf(disc(r * 0.18, 0.012, mat, n=8, vis=vis, wear=wear), t=(0.0, cy, z + t / 2 + 0.004)))
    return out
