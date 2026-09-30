"""Dead-world floor litter (BUILD_LIST row 48): alpha decals + a few 3D bits, no collision, <= 100 faces.

The litter decal (jp_m_decal_litter) is one mixed texture (leaves, straw, paper scraps, shards, dust); the
variants differ by outline, wear (density) and the 3D bits laid on top."""
import math
import random

import fkit
import bits
from fkit import core, box, sheet, xf, xfs, flat_poly, W, FPart, LITTER, TAWARA, PAPER, PALE, DARK
from bits import shards, blob

CAT = "debris"


def patch(seed, cx, cz, rx, rz, wear, y=0.003, vis=(1, 2), n=10, jitter=0.3):
    pts = [(cx + x, cz + z) for x, z in blob(seed, 1.0, n=n, jitter=jitter, sx=rx, sz=rz)]
    r = random.Random(seed)
    return flat_poly(pts, y, LITTER, vis=vis, wear=wear, uvoff=(r.random(), r.random()))


def straws(seed, cx, cz, spread, n, y=0.004):
    """Loose straw stalks: thin up-facing quads (visual only)."""
    r = random.Random(seed)
    quads, normals, uvs = [], [], []
    for i in range(n):
        L, w = r.uniform(0.12, 0.25), r.uniform(0.004, 0.007)
        a = r.uniform(0, math.pi)
        x, z = cx + r.uniform(-spread, spread), cz + r.uniform(-spread, spread)
        dx, dz = math.cos(a) * L / 2, math.sin(a) * L / 2
        px, pz = -math.sin(a) * w / 2, math.cos(a) * w / 2
        q = [(x - dx - px, y + 0.001 * i, z - dz - pz), (x + dx - px, y + 0.001 * i, z + dz - pz),
             (x + dx + px, y + 0.001 * i, z + dz + pz), (x - dx + px, y + 0.001 * i, z - dz + pz)]
        quads.append(q)
        normals.append((0.0, 1.0, 0.0))
        uvs.append([(0.0, 0.0), (0.4, 0.0), (0.4, 0.02), (0.0, 0.02)])
    s = sheet(quads, TAWARA, normals, vis=(1,), uvs=uvs)
    s.wear = "_w2"
    return s


def paper_scraps(seed, cx, cz, spread, n):
    """Torn paper and shoji squares: flat pieces, some with a curled edge (2 quads)."""
    r = random.Random(seed)
    out = []
    for i in range(n):
        w, d = r.uniform(0.06, 0.16), r.uniform(0.06, 0.14)
        s = fkit.rotated_box(cx + r.uniform(-spread, spread), cz + r.uniform(-spread, spread), w, d, 0.002 + 0.001 * i,
                             0.004 + 0.001 * i, r.uniform(0, 180), PAPER, vis=(1,))
        s.finalize()
        keep = [k for k in range(len(s.faces)) if s.fn[k][1] > 0.5]
        s.faces = [s.faces[k] for k in keep]
        s.fn = [s.fn[k] for k in keep]
        s.fm = [s.fm[k] for k in keep]
        s.fuv = [s.fuv[k] for k in keep]
        s.normals = s.fn
        s.wear = "_w2"
        out.append(s)
    return out


def debris(kind="leaves"):
    P = FPart("debris", budget=100, mass=0.0, flat=True)
    if kind == "leaves":
        # autumn leaves blown in at a door: a fan from the sill (at z = +0.3) into the room
        P.add(patch(1, 0.0, 0.0, 0.55, 0.32, "_w2", n=10))
        P.add(patch(2, 0.35, -0.30, 0.30, 0.22, "_w1", y=0.0035, vis=(1,)))
        P.add(patch(3, -0.40, -0.25, 0.22, 0.18, "_w1", y=0.004, vis=(1,)))
        P.notes.append("at door sills and engawa edges; the sill side is +z")
    elif kind == "straw":
        P.add(patch(11, 0.0, 0.0, 0.50, 0.40, "_w1", n=9))
        P.add(straws(12, 0.0, 0.0, 0.35, 22))
    elif kind == "paper":
        P.add(patch(21, 0.0, 0.0, 0.45, 0.35, "_w0", n=9))
        for s in paper_scraps(22, 0.0, 0.0, 0.30, 7):
            P.add(s)
    else:   # shards: broken bowls under a shelf
        P.add(patch(31, 0.0, 0.0, 0.40, 0.25, "_w1", n=8))
        for s in shards(32, 0.0, 0.0, 0.25, 10, PALE, size=(0.03, 0.07)):
            P.add(s)
        for s in shards(33, 0.1, -0.05, 0.15, 3, DARK, size=(0.04, 0.08)):
            P.add(s)
    P.notes.append("no Geometry; does not subtract from floor loot; Resolution 1 only in a house (Q5 rule 1)")
    return P


def M(p3d, variant, state, display, fn):
    return {"p3d": p3d, "variant": variant, "state": state, "display": display, "build": fn}


PROPS = [
    {"id": "jp_f_debris", "cat": CAT, "notes": ["this IS the abandoned layer (no separate abandoned states)"],
     "models": [
        M("jp_f_debris_leaves", "leaves", "intact", "Litter: autumn leaves blown in", lambda: debris("leaves")),
        M("jp_f_debris_straw", "straw", "intact", "Litter: straw and dust", lambda: debris("straw")),
        M("jp_f_debris_paper", "paper", "intact", "Litter: torn paper and shoji squares", lambda: debris("paper")),
        M("jp_f_debris_shards", "shards", "intact", "Litter: broken bowls", lambda: debris("shards")),
    ]},
]
