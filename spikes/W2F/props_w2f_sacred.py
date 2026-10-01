"""W2F specialty props, shrine + temple (spikes/W2F/W2F_NOTES.md): built into jp_furniture.pbo by
spikes/W2F/build_w2f.py (after B3a + L1 + S1). Frames as fkit / lkit: 'floor' base centre on the floor, +z = front;
'wall' origin on the floor below, wall face z = 0; 'hang' origin = the beam underside, hangs down (-y).

G1 A2-12: shrines, altars and their offerings are left UNDISTURBED and carry no loot: the 'as left' state is dust
(_w2), dried sakaki and burnt-down candles. Sacred props have no loot surface.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "spikes", "S1"), os.path.join(DEV, "spikes", "L1"), os.path.join(DEV, "spikes", "B3b"),
          os.path.join(DEV, "spikes", "B3a")):
    if p not in sys.path:
        sys.path.append(p)
import s1kit  # noqa: E402
from s1kit import (core, box, prism, ngon, lathe, xf, xfs, W, col, cyl_col, LPart, disc, stain, pole, cord,  # noqa
                   lod_box, wear_all, soft_slab, peg, rng, M, stext, cell_aspect, WOOD, WEATH, IRON, PALE, DARK, LACQ,
                   BAMBOO, PAPER, FUSUMA, INDIGO, KINARI, RED, ASH, LEAF, LITTER, ROPE, SUMI, LIFE, RICE)
import props_life_religious as LR  # noqa: E402  (L1, read-only: koro, candle_stand, vase_flowers, sanbo, heishi)
import props_straw as PS  # noqa: E402  (B3b, read-only: shide)

CAT = "sacred"
BRONZE = "metal_bronze"           # W2S (jp_m_metal_bronze, palette bronze_patina)
SHU = "lacquer_shu"
PAINT = "paint_shu"
KURO = "wood_kuro"
NEW = "wood_new"                  # M1: pale new / unpainted hinoki
SILVER = "wood_silver"
LEATHER = "leather_tan"
CUTSTONE = "stone_cut"


def rot(ss, **kw):
    return [xf(s, **kw) for s in ss]


def mv(ss, t):
    return [xf(s, t=t) for s in ss]


# ================================================================================================ offering box
def saisen_bako(w, d, h, wear="_w1"):
    P = LPart("saisen_bako", budget="furniture", mass=35.0, anchor="floor")
    t = 0.035
    out = [W(-w / 2, w / 2, 0.0, 0.07, -d / 2 + 0.03, -d / 2 + 0.09, WEATH),          # two runners
           W(-w / 2, w / 2, 0.0, 0.07, d / 2 - 0.09, d / 2 - 0.03, WEATH),
           W(-w / 2, w / 2, 0.07, h, d / 2 - t, d / 2, WEATH),                            # front
           W(-w / 2, w / 2, 0.07, h, -d / 2, -d / 2 + t, WEATH),                          # back
           W(-w / 2, -w / 2 + t, 0.07, h, -d / 2 + t, d / 2 - t, WEATH),                  # ends
           W(w / 2 - t, w / 2, 0.07, h, -d / 2 + t, d / 2 - t, WEATH),
           W(-w / 2 + t, w / 2 - t, 0.07, 0.10, -d / 2 + t, d / 2 - t, WEATH, vis=(1,)),   # bottom
           W(-w / 2 - 0.01, w / 2 + 0.01, h - 0.035, h, d / 2 - 0.005, d / 2 + 0.012, WEATH, vis=(1,)),   # top rail
           W(-w / 2 - 0.01, w / 2 + 0.01, h - 0.035, h, -d / 2 - 0.012, -d / 2 + 0.005, WEATH, vis=(1,))]
    # the slatted top: two rows of inclined slats falling to the middle line (coins drop in, nothing fishes out)
    inner = d / 2 - t
    k = 3
    pitch = inner / k
    for side in (-1, 1):
        for i in range(k):
            zc = side * (pitch * (i + 0.5))
            yc = h - 0.03 - (inner - abs(zc)) * 0.30
            s = W(-w / 2 + t, w / 2 - t, -0.008, 0.008, -pitch * 0.42, pitch * 0.42, WEATH, vis=(1,))
            out.append(xf(s, rx=side * 22.0, t=(0.0, yc, zc)))
    for sx in (-1, 1):                                                                   # iron corner straps
        for sz in (-1, 1):
            x0 = sx * w / 2
            z0 = sz * d / 2
            out.append(box(x0 - sx * 0.10 if sx > 0 else x0, x0 if sx > 0 else x0 + 0.10, h - 0.12, h,
                           z0 - 0.004 if sz > 0 else z0 - 0.004, z0 + 0.004, IRON, vis=(1,)))
            out.append(box(x0 - 0.004, x0 + 0.004, h - 0.12, h, z0 - sz * 0.08 if sz > 0 else z0,
                           z0 if sz > 0 else z0 + 0.08, IRON, vis=(1,)))
    wear_all(out, wear)
    P.adds(out)
    P.add(stain(301, 0.0, 0.0, w * 0.35, y=h + 0.002, sx=1.6, mat=LITTER, wear="_w2"))
    P.add(lod_box([s for s in out if 1 in s.vis], WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.dim("w", w, w, tol=0.005)
    P.dim("h", h, h, tol=0.005)
    P.notes.append("offering box (saisen-bako) on the en before the worship bay; undisturbed, no loot (G1 A2-12)")
    return P


# ================================================================================================ bell + rope
def suzu_rope(faded=False):
    P = LPart("suzu", budget="furniture", mass=2.0, anchor="hang", flat=True)
    wr = "_w2" if faded else "_w1"
    out = [box(-0.006, 0.006, -0.07, 0.0, -0.006, 0.006, IRON, vis=(1,)),
           pole((0.0, -0.07, 0.0), (0.0, -0.09, 0.0), 0.02, IRON, n=6, vis=(1,))]
    # the bell: a bronze crotal (sphere with a slot) and its top loop
    r = 0.12
    cy = -0.09 - 0.03 - r
    prof = [(0.0, -r)] + [(r * math.sin(math.pi * k / 6), -r * math.cos(math.pi * k / 6)) for k in range(1, 6)] + \
        [(0.0, r)]
    out.append(xf(lathe(prof, 10, BRONZE, vis=(1,)), t=(0.0, cy, 0.0)))
    out.append(box(-r * 0.75, r * 0.75, cy - r * 0.55, cy - r * 0.47, -r * 0.62, r * 0.62, DARK, vis=(1,)))    # slot
    out.append(pole((0.0, cy + r, 0.0), (0.0, -0.09, 0.0), 0.012, BRONZE, n=5, vis=(1,)))
    # the rope (suzu-no-o): two twisted cloth strands, red and white, a knot and a tassel
    y0, y1 = cy - r - 0.01, cy - r - 1.10
    seg = 12
    for k, mat in enumerate((RED, KINARI)):
        pts = []
        for i in range(seg + 1):
            a = math.pi * k + 2 * math.pi * i / 4.0
            y = y0 + (y1 - y0) * i / seg
            pts.append((0.016 * math.cos(a), y, 0.016 * math.sin(a)))
        for i in range(seg):
            out.append(pole(pts[i], pts[i + 1], 0.022, mat, n=5, vis=(1,), wear=wr))
    out.append(xf(lathe([(0.0, 0.0), (0.05, 0.02), (0.045, 0.07), (0.0, 0.09)], 8, KINARI, vis=(1,), wear=wr),
                  t=(0.0, y1 - 0.06, 0.0)))
    out.append(xf(lathe([(0.0, 0.0), (0.06, 0.0), (0.035, 0.30), (0.0, 0.30)], 8, RED, vis=(1,), wear=wr),
                  t=(0.0, y1 - 0.36, 0.0)))
    P.adds(out)
    P.add(box(-0.12, 0.12, cy - r, -0.07, -0.12, 0.12, BRONZE, vis=(2,)))
    P.add(box(-0.03, 0.03, y1 - 0.36, cy - r, -0.03, 0.03, RED, vis=(2,)))
    P.finish_hang()
    P.dim("bell_d", 0.24, 2 * r, tol=0.005)
    P.notes.append("the shrine bell with its cloth pull rope, hung from the kohai / eave beam over the offering box "
                   "(mount beam); hangs %.2f m; faded = the red gone pink-grey" % P.hang_len)
    return P


# ================================================================================================ drums
def odaiko():
    P = LPart("odaiko", budget="furniture", res3=False, mass=60.0, anchor="floor")
    R, L, cy = 0.35, 0.72, 0.86
    body = lathe([(0.0, 0.0), (R - 0.02, 0.0), (R + 0.03, L * 0.25), (R + 0.04, L * 0.5), (R + 0.03, L * 0.75),
                  (R - 0.02, L), (0.0, L)], 14, WOOD, vis=(1,))
    heads = [lathe([(0.0, -0.004), (R - 0.01, -0.004), (R - 0.01, 0.0), (0.0, 0.0)], 14, LEATHER, vis=(1,)),
             lathe([(0.0, L), (R - 0.01, L), (R - 0.01, L + 0.004), (0.0, L + 0.004)], 14, LEATHER, vis=(1,))]
    tacks = [lathe([(R - 0.012, y0), (R + 0.002, y0), (R + 0.002, y0 + 0.02), (R - 0.012, y0 + 0.02)], 14, IRON,
                   vis=(1,)) for y0 in (0.01, L - 0.03)]
    rings = [xf(pole((R + 0.035, L / 2 - 0.03, 0.0), (R + 0.035, L / 2 + 0.03, 0.0), 0.022, IRON, n=6, vis=(1,)),
                ry=a) for a in (0.0, 180.0)]
    drum = rot([body] + heads + tacks + rings, rx=90.0, t=(0.0, cy, -L / 2))
    drum = [xf(s, t=(0.0, 0.0, 0.0)) for s in drum]
    out = drum
    # the stand: a low frame with two cradle rails under the barrel
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * 0.30 - 0.035, sx * 0.30 + 0.035, 0.0, 0.58, sz * 0.27 - 0.035, sz * 0.27 + 0.035, KURO))
        out.append(W(sx * 0.30 - 0.035, sx * 0.30 + 0.035, 0.06, 0.12, -0.31, 0.31, KURO))
        out.append(xf(W(-0.035, 0.035, -0.04, 0.04, -0.34, 0.34, KURO), rz=sx * 30.0, t=(sx * 0.22, 0.54, 0.0)))
    out.append(W(-0.33, 0.33, 0.06, 0.12, -0.035, 0.035, KURO))
    P.adds(out)
    P.add(xf(lathe([(0.0, 0.0), (R + 0.04, 0.0), (R + 0.04, L), (0.0, L)], 6, WOOD, vis=(2,)), rx=90.0,
             t=(0.0, cy, -L / 2)))
    P.add(W(-0.34, 0.34, 0.0, 0.58, -0.31, 0.31, KURO, vis=(2,)))
    P.add(col(-0.40, 0.40, 0.0, cy + R + 0.05, -0.40, 0.40, WOOD))
    P.dim("drum_d", 0.70, 2 * R, tol=0.01)
    P.notes.append("odaiko on its stand (haiden / kagura corner); undisturbed, no loot")
    return P


def kagura_drums():
    P = LPart("kagura_drums", budget="furniture", mass=8.0, anchor="floor")
    r, h = 0.18, 0.15
    d = [lathe([(0.0, 0.0), (r, 0.0), (r, h), (0.0, h)], 12, LEATHER, vis=(1,)),
         lathe([(r - 0.02, 0.02), (r + 0.01, 0.025), (r + 0.01, h - 0.025), (r - 0.02, h - 0.02)], 12, LACQ, vis=(1,))]
    for k in range(6):                                                    # the lacing cords
        a = 2 * math.pi * k / 6
        d.append(pole((r * math.cos(a), 0.0, r * math.sin(a)), (r * math.cos(a + 0.5), h, r * math.sin(a + 0.5)),
                      0.004, SHU, n=3, vis=(1,)))
    d = rot(d, rx=-35.0, t=(0.0, 0.31, 0.0))
    stand = [pole((-0.13, 0.015, -0.12), (0.0, 0.30, 0.02), 0.015, KURO, n=5, vis=(1,)),
             pole((0.13, 0.015, -0.12), (0.0, 0.30, 0.02), 0.015, KURO, n=5, vis=(1,)),
             pole((0.0, 0.015, 0.16), (0.0, 0.30, 0.0), 0.015, KURO, n=5, vis=(1,))]
    flute = [pole((0.32, 0.012, -0.10), (0.32, 0.012, 0.30), 0.012, LACQ, n=6, vis=(1,)),
             xf(soft_slab(0.06, 0.46, 0.02, INDIGO, n=2, vis=(1,)), t=(0.42, 0.0, 0.10))]
    P.adds(d + stand + flute)
    P.add(W(-0.22, 0.22, 0.0, 0.45, -0.22, 0.22, LACQ, vis=(2,)))
    P.add(col(-0.22, 0.22, 0.0, 0.45, -0.20, 0.22, WOOD))
    P.dim("drum_d", 0.36, 2 * r, tol=0.005)
    P.notes.append("kagura small drum (shime-daiko) on its stand + the flute in its bag; undisturbed")
    return P


# ================================================================================================ name boards
def gaku(cell=None, mat=SUMI, w=0.55, h=0.95, worn=False):
    """A framed name board; the wall / beam face is z = 0, the board leans out 8 deg; centred on y = 0 (place the
    proxy at the fitting's centre height)."""
    P = LPart("gaku", budget="small", mass=6.0, anchor="wall", flat=True)
    t, f = 0.035, 0.05
    wr = "_w2" if worn else "_w1"
    out = [W(-w / 2 + f, w / 2 - f, -h / 2 + f, h / 2 - f, 0.0, t, SILVER if worn else NEW, vis=(1,)),
           W(-w / 2, w / 2, h / 2 - f, h / 2, 0.0, t + 0.02, LACQ, vis=(1,)),
           W(-w / 2, w / 2, -h / 2, -h / 2 + f, 0.0, t + 0.02, LACQ, vis=(1,)),
           W(-w / 2, -w / 2 + f, -h / 2 + f, h / 2 - f, 0.0, t + 0.02, LACQ, vis=(1,)),
           W(w / 2 - f, w / 2, -h / 2 + f, h / 2 - f, 0.0, t + 0.02, LACQ, vis=(1,))]
    wear_all(out, wr)
    if cell:
        asp = cell_aspect(cell, mat)
        th = (h - 2 * f) * 0.86
        tw = min((w - 2 * f) * 0.86, th * asp)
        th = tw / asp
        out.append(stext((0.0, 0.0, t + 0.0015), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), th, cell, mat,
                         wear="_w2" if worn else "_w1", width=tw))
    for sx in (-1, 1):                                                   # the two hanging irons to the beam
        out.append(box(sx * w * 0.3 - 0.006, sx * w * 0.3 + 0.006, h / 2, h / 2 + 0.08, 0.004, 0.012, IRON, vis=(1,)))
    out = rot(out, rx=-8.0, t=(0.0, 0.0, 0.0))
    lo = min(v[2] for s in out for v in s.verts)
    out = mv(out, (0.0, 0.0, -lo))
    P.adds(out)
    P.add(lod_box([s for s in out if not getattr(s, "_text_faced", False)], LACQ, vis=(2,)))
    P.dim("w", w, w, tol=0.005)
    P.notes.append("name board (gaku) over the worship bay / gate tie beam: a FRONT proxy (centre at the fitting's "
                   "y, the beam face z = 0); text %s" % (cell or "worn off (blank weathered board)"))
    return P


# ================================================================================================ offering table
def hassokuan(w=0.9):
    P = LPart("hassokuan", budget="furniture", mass=12.0, anchor="floor")
    d, h = 0.40, 0.45
    wr = "_w2"
    out = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, NEW, vis=(1, 2))]
    for sx in (-1, 1):
        x = sx * (w / 2 - 0.07)
        out.append(W(x - 0.03, x + 0.03, 0.0, 0.035, -d / 2 + 0.02, d / 2 - 0.02, NEW))                  # foot rail
        out.append(W(x - 0.02, x + 0.02, h - 0.07, h - 0.03, -d / 2 + 0.03, d / 2 - 0.03, NEW, vis=(1,)))
        for k in range(4):                                                                              # 4 legs
            z = -d / 2 + 0.06 + k * (d - 0.12) / 3
            out.append(W(x - 0.012, x + 0.012, 0.035, h - 0.07, z - 0.01, z + 0.01, NEW, vis=(1,)))
    wear_all(out, wr)
    P.adds(out)
    top = []
    off = w / 2 - 0.18
    top += LR.sanbo(-off * 0.45, 0.0, wear=wr, full=False)
    top += LR.sanbo(off * 0.45, 0.0, wear=wr, full=True)
    for sx in (-1, 1):
        top += LR.heishi(sx * (off * 0.45 + 0.13), -0.08, wear=wr)
        top += LR.vase_flowers(sx * (w / 2 - 0.07), 0.05, dry=True, wear=wr)
    P.adds(mv(top, (0.0, h, 0.0)))
    P.add(W(-w / 2, w / 2, h, h + 0.16, -0.12, 0.12, NEW, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, NEW))
    P.dim("w", w, w, tol=0.005)
    P.dim("h", h, h, tol=0.005)
    P.notes.append("eight-legged offering table (hassoku-an) with sanbo, white flasks and dried sakaki, as left: "
                   "undisturbed, dust, no loot")
    return P


# ================================================================================================ sanctum
def shintai_zushi(w=0.55):
    """The shrine cabinet inside a sealed honden (seen through lattice doors only): a gabled box on a stand, doors
    shut, a bronze mirror on its cloud stand and two gohei before it. Visual only (nobody gets in)."""
    P = LPart("shintai_zushi", budget="furniture", mass=10.0, anchor="floor", flat=True)
    d = w * 0.8
    cw, cd, ch = w * 0.82, d * 0.80, 0.50
    out = [W(-w / 2, w / 2, 0.0, 0.08, -d / 2, d / 2, NEW),
           W(-cw / 2, cw / 2, 0.08, 0.08 + ch, -cd / 2, cd / 2, NEW)]
    for sx in (-1, 1):                                                   # doors shut, bronze fittings
        out.append(W(-0.003 if sx < 0 else 0.003, sx * (cw / 2 - 0.03), 0.12, 0.08 + ch - 0.04, cd / 2,
                     cd / 2 + 0.006, NEW, vis=(1,)))
        out.append(box(sx * 0.012 - 0.01, sx * 0.012 + 0.01, 0.28, 0.33, cd / 2 + 0.006, cd / 2 + 0.012, BRONZE,
                       vis=(1,)))
    yr = 0.08 + ch
    for sx in (-1, 1):                                                   # gable roof
        out.append(xf(W(0.0, cw / 2 + 0.08, -0.012, 0.012, -cd / 2 - 0.07, cd / 2 + 0.07, NEW), rz=sx * 0.0,
                      t=(0.0, 0.0, 0.0)) if False else
                   xf(W(-0.005, cw / 2 + 0.09, -0.012, 0.012, -cd / 2 - 0.07, cd / 2 + 0.07, NEW),
                      ry=0.0 if sx > 0 else 180.0, rz=0.0, t=(0.0, 0.0, 0.0)))
    roof = []
    for sx in (-1, 1):
        s = W(0.0, cw / 2 + 0.09, -0.012, 0.012, -cd / 2 - 0.07, cd / 2 + 0.07, NEW)
        s = xf(s, rz=-24.0)
        if sx < 0:
            s = xf(s, ry=180.0)
        roof.append(xf(s, t=(0.0, yr + 0.02, 0.0)))
    out = out[:-2] + roof
    out.append(W(-0.025, 0.025, yr + 0.02, yr + 0.06, -cd / 2 - 0.07, cd / 2 + 0.07, NEW, vis=(1,)))    # ridge
    for sz in (-1, 1):                                                   # small chigi crossing at the gables
        for sx in (-1, 1):
            out.append(xf(W(-0.007, 0.007, 0.0, 0.10, -0.007, 0.007, NEW, vis=(1,)), rz=sx * 35.0,
                          t=(0.0, yr + 0.04, sz * (cd / 2 + 0.06))))
    # the mirror on its cloud stand, two gohei
    mz = d / 2 + 0.12
    mirror = lathe([(0.0, -0.006), (0.10, -0.006), (0.10, 0.006), (0.0, 0.006)], 12, BRONZE, vis=(1,))
    out.append(xf(mirror, rx=80.0, t=(0.0, 0.26, mz)))
    out.append(W(-0.08, 0.08, 0.0, 0.05, mz - 0.06, mz + 0.06, LACQ, vis=(1,)))
    out.append(W(-0.015, 0.015, 0.05, 0.17, mz - 0.01, mz + 0.01, LACQ, vis=(1,)))
    for sx in (-1, 1):
        gx = sx * (w / 2 - 0.02)
        out.append(W(gx - 0.035, gx + 0.035, 0.0, 0.03, mz - 0.035, mz + 0.035, NEW, vis=(1,)))
        out.append(pole((gx, 0.03, mz), (gx, 0.62, mz), 0.006, NEW, n=4, vis=(1,)))
        for side in (-1, 1):
            out.append(xf(PS.shide((0.0, 0.0, 0.0), s=0.22, wear="_w2"), ry=side * 70.0, t=(gx, 0.60, mz)))
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-w / 2, w / 2, 0.0, yr + 0.08, -d / 2, d / 2, NEW, vis=(2,)))
    P.dim("w", w, w, tol=0.005)
    P.notes.append("the sealed sanctum: shrine cabinet, mirror, gohei (visual only, inside the closed honden)")
    return P


# ================================================================================================ ema + masks
def ema_rail(n=9):
    P = LPart("ema_rail", budget="furniture", mass=3.0, anchor="wall", flat=True)
    L, y = 1.20, 1.55
    out = [W(-L / 2, L / 2, y, y + 0.05, 0.0, 0.035, WEATH)]
    for sx in (-1, 1):
        out.append(W(sx * L / 2 - 0.03, sx * L / 2 + 0.03 if sx > 0 else sx * L / 2 + 0.03, y - 0.06, y + 0.05,
                     0.0, 0.02, WEATH, vis=(1,)) if False else W(sx * (L / 2 - 0.03) - 0.025, sx * (L / 2 - 0.03)
                                                                  + 0.025, y - 0.06, y + 0.05, 0.0, 0.02, WEATH,
                                                                  vis=(1,)))
    r = rng("ema_rail")
    pent = [(-0.075, 0.0), (0.075, 0.0), (0.075, 0.075), (0.0, 0.105), (-0.075, 0.075)]
    for i in range(n):
        x = -L / 2 + 0.08 + i * (L - 0.16) / (n - 1) + r.uniform(-0.02, 0.02)
        mat = (NEW, SILVER, WEATH)[i % 3]
        top = y - 0.01
        e = prism(pent, "z", 0.0, 0.008, mat, vis=(1,))
        e = xf(e, t=(0.0, -0.105, 0.0))
        e = xf(e, rz=r.uniform(-8, 8), t=(x, top - 0.02, 0.04 + 0.01 * (i % 2)))
        out.append(e)
        out.append(W(x - 0.035, x + 0.035, top - 0.11, top - 0.06, 0.049 + 0.01 * (i % 2), 0.051 + 0.01 * (i % 2),
                     KURO, vis=(1,)))                                    # the faded painting
        out.append(pole((x, top - 0.02, 0.045 + 0.01 * (i % 2)), (x, y + 0.02, 0.036), 0.003, RED, n=3, vis=(1,)))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(W(-L / 2, L / 2, y - 0.13, y + 0.05, 0.0, 0.05, WEATH, vis=(2,)))
    P.dim("length", L, L, tol=0.005)
    P.notes.append("votive boards (ema) on a rail on the haiden wall (mount wall), weathered")
    return P


def mask(cx, cy, mat, kind, z0=0.03):
    r = 0.085
    prof = [(0.0, 0.0), (r, 0.004), (r * 0.95, 0.03), (r * 0.65, 0.06), (0.0, 0.07)]
    m = xf(lathe(prof, 10, mat, vis=(1,)), rx=90.0, t=(cx, cy, z0))
    out = [m]
    lo = min(v[2] for v in m.verts)
    if lo < z0 - 1e-6:
        out = [xf(m, t=(0.0, 0.0, z0 - lo))]
    zf = max(v[2] for v in out[0].verts)
    out.append(box(cx - 0.012, cx + 0.012, cy - 0.03, cy + 0.01, zf - 0.02, zf + 0.012, mat, vis=(1,)))   # nose
    for sx in (-1, 1):
        out.append(box(cx + sx * 0.035 - 0.015, cx + sx * 0.035 + 0.015, cy + 0.015, cy + 0.025, zf - 0.025, zf - 0.012,
                       DARK, vis=(1,)))
    if kind == "oni":
        for sx in (-1, 1):
            out.append(pole((cx + sx * 0.05, cy + 0.06, zf - 0.03), (cx + sx * 0.07, cy + 0.12, zf - 0.03), 0.01,
                            PALE, n=4, vis=(1,), r1=0.003))
    if kind == "okina":
        out.append(pole((cx, cy - 0.08, zf - 0.03), (cx, cy - 0.16, zf - 0.04), 0.03, KINARI, n=5, vis=(1,),
                        r1=0.01))
    return out


def kagura_masks():
    P = LPart("kagura_masks", budget="furniture", mass=3.0, anchor="wall", flat=True)
    y = 1.50
    out = [W(-0.55, 0.55, y + 0.08, y + 0.14, 0.0, 0.022, WEATH)]
    for k, (x, mat, kind) in enumerate(((-0.36, FUSUMA, "okina"), (-0.12, PAINT, "oni"), (0.12, KURO, "plain"))):
        out.append(peg(x, y + 0.11, L=0.05, z0=0.0))
        out += mask(x, y, mat, kind)
    # the kagura bell tree hung on the last peg
    bx = 0.36
    out.append(peg(bx, y + 0.11, L=0.05, z0=0.0))
    out.append(pole((bx, y + 0.11, 0.05), (bx, y - 0.25, 0.05), 0.012, KURO, n=5, vis=(1,)))
    for i, (dx, dy) in enumerate(((0.0, 0.10), (-0.04, 0.06), (0.04, 0.06), (-0.05, 0.01), (0.05, 0.01), (0.0, 0.0))):
        out.append(xf(lathe([(0.0, -0.018), (0.016, -0.008), (0.016, 0.008), (0.0, 0.018)], 6, BRONZE, vis=(1,)),
                      t=(bx + dx, y + dy - 0.05, 0.07)))
    out.append(xf(lathe([(0.0, 0.0), (0.03, 0.01), (0.0, 0.25)], 5, RED, vis=(1,)), rx=180.0,
                  t=(bx, y - 0.25, 0.05)))
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-0.55, 0.55, y - 0.25, y + 0.14, 0.0, 0.10, WEATH, vis=(2,)))
    P.dim("width", 1.10, 1.10, tol=0.005)
    P.notes.append("kagura masks (okina, oni, plain) on pegs + the kagura bell tree, stage back wall (mount wall)")
    return P


# ================================================================================================ altar dais + images
def seated_figure(mat):
    out = [lathe([(0.0, 0.0), (0.17, 0.0), (0.22, 0.06), (0.24, 0.10), (0.16, 0.12), (0.0, 0.12)], 10, mat, vis=(1,)),
           lathe([(0.0, 0.12), (0.24, 0.12), (0.22, 0.20), (0.13, 0.27), (0.12, 0.40), (0.08, 0.46), (0.0, 0.47)], 10,
                 mat, vis=(1,)),
           xf(lathe([(0.0, -0.07)] + [(0.07 * math.sin(math.pi * k / 4), -0.07 * math.cos(math.pi * k / 4))
                                      for k in (1, 2, 3)] + [(0.0, 0.07)], 8, mat, vis=(1,)), t=(0.0, 0.53, 0.0)),
           xf(lathe([(0.0, -0.03), (0.03, 0.0), (0.0, 0.03)], 6, mat, vis=(1,)), t=(0.0, 0.61, 0.0))]
    halo = lathe([(0.0, -0.005), (0.24, -0.005), (0.24, 0.005), (0.0, 0.005)], 14, mat, vis=(1,))
    out.append(xf(halo, rx=90.0, t=(0.0, 0.50, -0.20)))
    return out, 0.74


def standing_figure(mat, kind):
    out = [lathe([(0.0, 0.0), (0.12, 0.0), (0.15, 0.05), (0.15, 0.08), (0.10, 0.10), (0.0, 0.10)], 10, mat, vis=(1,)),
           lathe([(0.0, 0.10), (0.11, 0.10), (0.10, 0.45), (0.09, 0.70), (0.06, 0.76), (0.0, 0.77)], 10, mat,
                 vis=(1,)),
           xf(lathe([(0.0, -0.06)] + [(0.06 * math.sin(math.pi * k / 4), -0.065 * math.cos(math.pi * k / 4))
                                      for k in (1, 2, 3)] + [(0.0, 0.065)], 8, mat, vis=(1,)), t=(0.0, 0.83, 0.0))]
    if kind == "jizo":
        out.append(prism([(-0.08, 0.0), (0.08, 0.0), (0.0, -0.13)], "z", 0.0, 0.006, RED, vis=(1,)))
        out[-1] = xf(out[-1], t=(0.0, 0.73, 0.085))
        out.append(pole((0.15, 0.10, 0.04), (0.15, 0.98, 0.04), 0.008, BAMBOO, n=4, vis=(1,)))
        out.append(xf(lathe([(0.0, -0.035), (0.035, 0.0), (0.0, 0.035)], 6, IRON, vis=(1,)), t=(0.15, 1.00, 0.04)))
        h = 1.05
    else:
        halo = prism([(-0.13, 0.0), (0.13, 0.0), (0.15, 0.35), (0.0, 0.62), (-0.15, 0.35)], "z", -0.01, 0.0, mat,
                     vis=(1,))
        out.append(xf(halo, t=(0.0, 0.40, -0.12)))
        out.append(xf(lathe([(0.0, -0.02), (0.035, 0.0), (0.0, 0.05)], 6, mat, vis=(1,)), t=(0.0, 0.89, 0.0)))
        h = 1.02
    return out, h


def dais(kind, W_=2.4, D=0.85, H=0.85):
    """Sumeru dais (shumidan) with a zushi cabinet (doors open) holding the image, and the three altar pieces."""
    P = LPart("dais", budget="medium", mass=150.0, anchor="floor")
    out = [W(-W_ / 2, W_ / 2, 0.0, 0.12, -D / 2, D / 2, LACQ),
           W(-W_ / 2 + 0.04, W_ / 2 - 0.04, 0.12, 0.20, -D / 2 + 0.04, D / 2 - 0.04, LACQ, vis=(1,)),
           W(-W_ / 2 + 0.10, W_ / 2 - 0.10, 0.20, H - 0.16, -D / 2 + 0.10, D / 2 - 0.10, LACQ),
           W(-W_ / 2 + 0.04, W_ / 2 - 0.04, H - 0.16, H - 0.07, -D / 2 + 0.04, D / 2 - 0.04, LACQ, vis=(1,)),
           W(-W_ / 2, W_ / 2, H - 0.07, H, -D / 2, D / 2, LACQ)]
    np_ = max(2, int((W_ - 0.3) / 0.45))                                 # shu panels on the waist (koshi)
    for i in range(np_):
        x = -W_ / 2 + 0.10 + (i + 0.5) * (W_ - 0.2) / np_
        out.append(W(x - (W_ - 0.2) / np_ * 0.38, x + (W_ - 0.2) / np_ * 0.38, 0.26, H - 0.22, D / 2 - 0.10,
                     D / 2 - 0.095, SHU, vis=(1,)))
    figure = {"amida": "seated", "shaka": "seated", "kannon": "kannon", "jizo": "jizo"}[kind]
    if figure == "seated":
        fig, fh = seated_figure(BRONZE)
    else:
        fig, fh = standing_figure(KURO if kind == "jizo" else BRONZE, figure)
    zw, zd = (0.95, 0.55) if figure == "seated" else (0.70, 0.42)
    zh = fh + 0.30
    zz = -D / 2 + zd / 2 + 0.02
    zt = H + zh
    zc = [W(-zw / 2, zw / 2, H, H + 0.05, zz - zd / 2, zz + zd / 2, LACQ),                         # floor
          W(-zw / 2, zw / 2, H + 0.05, zt, zz - zd / 2, zz - zd / 2 + 0.03, LACQ),                 # back
          W(-zw / 2, -zw / 2 + 0.03, H + 0.05, zt, zz - zd / 2 + 0.03, zz + zd / 2, LACQ),         # sides
          W(zw / 2 - 0.03, zw / 2, H + 0.05, zt, zz - zd / 2 + 0.03, zz + zd / 2, LACQ),
          W(-zw / 2 - 0.08, zw / 2 + 0.08, zt, zt + 0.06, zz - zd / 2 - 0.06, zz + zd / 2 + 0.10, LACQ),   # roof slab
          W(-zw / 2 - 0.02, zw / 2 + 0.02, zt + 0.06, zt + 0.14, zz - zd / 2, zz + zd / 2 + 0.04, LACQ)]
    for sx in (-1, 1):                                                   # doors folded open against the sides
        L_ = zw / 2 - 0.02
        x0_, x1_ = sorted((sx * zw / 2, sx * (zw / 2 + 0.014)))
        out.append(W(x0_, x1_, H + 0.08, zt - 0.04, zz + zd / 2, zz + zd / 2 + min(L_, D / 2 - zz - zd / 2 - 0.01),
                     LACQ, vis=(1,)))
        out.append(box(sx * zw / 2 - 0.01, sx * zw / 2 + 0.01, H + 0.20, H + 0.26, zz + zd / 2, zz + zd / 2 + 0.01,
                       BRONZE, vis=(1,)))
    out += zc
    out += mv(fig, (0.0, H + 0.05, zz + 0.03))
    # the three altar pieces in front of the zushi, dusty and burnt down
    fz = D / 2 - 0.13
    out += mv(LR.koro(0.0, fz, r=0.06, wear="_w2"), (0.0, H, 0.0))
    out += mv(LR.candle_stand(-0.32, fz, h=0.22, candle=0.015, wear="_w2"), (0.0, H, 0.0))
    out += mv(LR.vase_flowers(0.32, fz, dry=True, wear="_w2"), (0.0, H, 0.0))
    if kind == "jizo":                                                   # small offerings left before Jizo
        out += mv(LR.sanbo(0.0, fz - 0.17, wear="_w2", full=False), (0.0, H, 0.0))
    P.adds(out)
    P.add(W(-W_ / 2, W_ / 2, 0.0, H, -D / 2, D / 2, LACQ, vis=(2,)))
    P.add(W(-zw / 2, zw / 2, H, zt + 0.14, zz - zd / 2, zz + zd / 2, LACQ, vis=(2,)))
    P.add(col(-W_ / 2, W_ / 2, 0.0, H, -D / 2, D / 2, LACQ))
    P.add(col(-zw / 2, zw / 2, H, zt + 0.14, zz - zd / 2, zz + zd / 2, LACQ))
    P.dim("w", W_, W_, tol=0.005)
    P.dim("h", H, H, tol=0.005)
    P.notes.append("Sumeru dais (shumidan) with the %s image in its zushi (doors open) and the three altar pieces; "
                   "undisturbed, dust, no loot (G1 A2-12); against the back wall (wall-side at -z)" % kind)
    return P


def tengai(s=1.10):
    P = LPart("tengai", budget="furniture", mass=8.0, anchor="hang", flat=True)
    out = [box(-0.006, 0.006, -0.20, 0.0, -0.006, 0.006, IRON, vis=(1,))]
    y0 = -0.20
    out.append(core.hexa([(-s / 2, y0 - 0.12, -s / 2), (s / 2, y0 - 0.12, -s / 2), (s / 2, y0 - 0.12, s / 2),
                          (-s / 2, y0 - 0.12, s / 2), (-0.15, y0, -0.15), (0.15, y0, -0.15), (0.15, y0, 0.15),
                          (-0.15, y0, 0.15)], LACQ, vis=(1, 2)))
    out.append(W(-s / 2 - 0.02, s / 2 + 0.02, y0 - 0.20, y0 - 0.12, -s / 2 - 0.02, s / 2 + 0.02, BRONZE, vis=(1,)))
    k = 5
    for i in range(k):
        for side in range(4):
            t = -s / 2 + (i + 0.5) * s / k
            x, z = [(t, -s / 2 - 0.025), (t, s / 2 + 0.025), (-s / 2 - 0.025, t), (s / 2 + 0.025, t)][side]
            out.append(pole((x, y0 - 0.20, z), (x, y0 - 0.48, z), 0.006, BRONZE, n=3, vis=(1,)))
            out.append(xf(lathe([(0.0, -0.02), (0.02, 0.0), (0.0, 0.02)], 4, BRONZE, vis=(1,)), t=(x, y0 - 0.50, z)))
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-s / 2, s / 2, y0 - 0.5, y0, -s / 2, s / 2, BRONZE, vis=(2,)))
    P.finish_hang()
    P.dim("size", s, s, tol=0.005)
    P.notes.append("canopy (tengai) over the image: mount beam (the hall ceiling over the dais); bronze fringe")
    return P


# ================================================================================================ sutra desk, mokugyo
def keisu(cx, cz, r=0.17):
    out = [W(cx - 0.20, cx + 0.20, 0.0, 0.14, cz - 0.20, cz + 0.20, LACQ, vis=(1,)),
           xf(soft_slab(0.34, 0.34, 0.06, SHU, n=2, vis=(1,)), t=(cx, 0.14, cz)),
           xf(lathe([(0.0, 0.0), (r * 0.7, 0.0), (r, r * 0.6), (r, r * 0.95), (r - 0.012, r * 0.95), (r * 0.7, 0.012),
                     (0.0, 0.012)], 12, BRONZE, vis=(1,)), t=(cx, 0.19, cz))]
    return out


def small_mokugyo(cx, cz, r=0.11):
    out = [xf(soft_slab(0.26, 0.26, 0.04, INDIGO, n=2, vis=(1,)), t=(cx, 0.0, cz)),
           xf(lathe([(0.0, 0.0), (r * 0.8, 0.0), (r, r * 0.6), (r * 0.9, r * 1.3), (r * 0.5, r * 1.6), (0.0, r * 1.65)],
                    8, SHU, vis=(1,)), t=(cx, 0.04, cz)),
           box(cx - r * 0.8, cx + r * 0.8, 0.04 + r * 0.55, 0.04 + r * 0.65, cz + r * 0.85, cz + r * 1.02, DARK, vis=(1,))]
    return out


def sutra_desk():
    P = LPart("sutra_desk", budget="furniture", mass=12.0, anchor="floor")
    w, d, h = 0.90, 0.42, 0.33
    out = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, LACQ)]
    for sx in (-1, 1):
        x = sx * (w / 2 - 0.08)
        out.append(W(x - 0.025, x + 0.025, 0.04, h - 0.03, -d / 2 + 0.05, d / 2 - 0.05, LACQ))
        out.append(W(x - 0.05, x + 0.05, 0.0, 0.04, -d / 2 + 0.02, d / 2 - 0.02, LACQ))
        out.append(W(x - 0.07, x + 0.07, h - 0.03, h + 0.025, -d / 2, -d / 2 + 0.03, LACQ, vis=(1,)))   # curled ends
    for i, (x, m) in enumerate(((-0.18, KINARI), (0.08, INDIGO))):      # folded sutra books
        out.append(W(x - 0.06, x + 0.06, h, h + 0.04 + 0.02 * i, -0.13, 0.13, m, vis=(1,)))
    out += mv(LR.koro(0.30, 0.0, r=0.045, wear="_w2"), (0.0, h, 0.0))
    out += keisu(0.75, 0.05)
    out += small_mokugyo(-0.72, 0.05)
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, LACQ, vis=(2,)))
    P.add(W(0.55, 0.95, 0.0, 0.36, -0.15, 0.25, BRONZE, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, LACQ))
    P.add(col(0.55, 0.95, 0.0, 0.19, -0.15, 0.25, LACQ))
    P.dim("w", w, w, tol=0.005)
    P.notes.append("sutra desk (kyozukue) with folded sutras + a small incense burner, the bowl gong (keisu) on its "
                   "cushion stand to its right, a small mokugyo to its left; undisturbed, no loot")
    return P


def mokugyo_l():
    P = LPart("mokugyo", budget="furniture", mass=15.0, anchor="floor")
    r = 0.24
    out = [xf(soft_slab(0.56, 0.56, 0.08, SHU, n=3, vis=(1,)), t=(0.0, 0.0, 0.0)),
           xf(lathe([(0.0, 0.0), (r * 0.75, 0.0), (r, r * 0.55), (r * 0.95, r * 1.15), (r * 0.55, r * 1.55),
                     (0.0, r * 1.62)], 12, SHU, vis=(1,)), t=(0.0, 0.08, 0.0)),
           box(-r * 0.85, r * 0.85, 0.08 + r * 0.5, 0.08 + r * 0.6, r * 0.62, r * 1.02, DARK, vis=(1,))]
    for sx in (-1, 1):                                                   # the two fish heads at the handle
        out.append(xf(lathe([(0.0, -0.05), (0.05, 0.0), (0.03, 0.05), (0.0, 0.06)], 6, SHU, vis=(1,)),
                      rz=sx * 40.0, t=(sx * 0.07, 0.08 + r * 1.5, -0.02)))
    out.append(pole((0.32, 0.09, -0.15), (0.32, 0.09, 0.15), 0.014, WOOD, n=5, vis=(1,)))
    out.append(xf(lathe([(0.0, -0.04), (0.04, 0.0), (0.0, 0.04)], 6, KINARI, vis=(1,)), t=(0.32, 0.09, 0.17)))
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-0.28, 0.28, 0.0, 0.08 + r * 1.6, -0.28, 0.28, SHU, vis=(2,)))
    P.add(col(-0.26, 0.26, 0.0, 0.08 + r * 1.6, -0.26, 0.26, WOOD))
    P.dim("d", 0.48, 2 * r, tol=0.005)
    P.notes.append("the big round mokugyo (Zen) on its cushion with the striker; undisturbed, no loot")
    return P


# ================================================================================================ gongs, bells
def waniguchi():
    P = LPart("waniguchi", budget="furniture", mass=6.0, anchor="hang", flat=True)
    out = [cord((-0.10, 0.0, 0.0), (-0.12, -0.10, 0.0), 0.006), cord((0.10, 0.0, 0.0), (0.12, -0.10, 0.0), 0.006)]
    gy = -0.10 - 0.22
    g = lathe([(0.0, -0.045), (0.19, -0.035), (0.22, 0.0), (0.19, 0.035), (0.0, 0.045)], 14, BRONZE, vis=(1,))
    out.append(xf(g, rx=90.0, t=(0.0, gy, 0.0)))
    out.append(box(-0.15, 0.15, gy - 0.20, gy - 0.17, -0.05, 0.05, DARK, vis=(1,)))       # the mouth slit
    for sx in (-1, 1):
        out.append(box(sx * 0.12 - 0.015, sx * 0.12 + 0.015, gy + 0.18, gy + 0.22, -0.015, 0.015, BRONZE, vis=(1,)))
    # the pull rope (cloth, faded) hanging in front of it
    z = 0.09
    pts = [(0.0, gy + 0.05, z), (0.03, gy - 0.40, z + 0.01), (0.01, gy - 0.90, z), (0.0, gy - 1.35, z)]
    for k in range(3):
        for i in range(3):
            a, b = pts[i], pts[i + 1]
            off = 0.012 * math.cos(2 * math.pi * k / 3)
            out.append(pole((a[0] + off, a[1], a[2] + 0.012 * math.sin(2 * math.pi * k / 3)),
                            (b[0] + off, b[1], b[2] + 0.012 * math.sin(2 * math.pi * k / 3)), 0.014,
                            (RED, KINARI, INDIGO)[k], n=4, vis=(1,), wear="_w2"))
    out.append(xf(lathe([(0.0, 0.0), (0.05, 0.0), (0.03, 0.25), (0.0, 0.25)], 6, KINARI, vis=(1,), wear="_w2"),
                  t=(0.0, gy - 1.60, z)))
    out.append(cord((0.0, gy + 0.05, z), (0.0, 0.0, 0.0), 0.006))
    P.adds(out)
    P.add(box(-0.22, 0.22, gy - 0.22, gy + 0.22, -0.05, 0.05, BRONZE, vis=(2,)))
    P.add(box(-0.03, 0.03, gy - 1.60, gy, z - 0.03, z + 0.03, KINARI, vis=(2,)))
    P.finish_hang()
    P.dim("d", 0.44, 0.44, tol=0.005)
    P.notes.append("the flat 'crocodile mouth' gong (waniguchi) + pull rope under the kohai (mount beam); hangs %.2f m"
                   % P.hang_len)
    return P


def bonsho(H=0.95, D=0.56):
    P = LPart("bonsho", budget="furniture", mass=400.0, anchor="hang")
    out = [pole((0.0, 0.0, 0.0), (0.0, -0.05, 0.0), 0.03, IRON, n=6, vis=(1,))]
    # the dragon-head lug (ryuzu): an arch of two heads
    out.append(W(-0.10, 0.10, -0.12, -0.05, -0.035, 0.035, BRONZE, vis=(1,)))
    for sx in (-1, 1):
        out.append(W(sx * 0.10 - 0.03 if sx > 0 else -0.13, 0.13 if sx > 0 else -0.07, -0.20, -0.08, -0.05, 0.05,
                     BRONZE, vis=(1,)))
    y0 = -0.20
    R = D / 2
    prof = [(0.0, y0), (R * 0.55, y0), (R * 0.85, y0 - 0.04), (R * 0.95, y0 - 0.10), (R * 0.97, y0 - H * 0.6),
            (R, y0 - H + 0.04), (R * 1.02, y0 - H), (R * 0.90, y0 - H), (0.0, y0 - H + 0.02)]
    out.append(lathe(prof, 16, BRONZE, vis=(1,)))
    for f in (0.30, 0.62):                                               # the belt bands (kesadasuki)
        yb = y0 - H * f
        out.append(lathe([(R * 0.965, yb - 0.02), (R * 0.99, yb - 0.02), (R * 0.99, yb + 0.02), (R * 0.965, yb + 0.02)],
                         16, BRONZE, vis=(1,)))
    ys = y0 - H * 0.78                                                   # the striking seats (tsukiza), both sides
    for sx in (-1, 1):
        out.append(xf(lathe([(0.0, 0.0), (0.07, 0.0), (0.06, 0.02), (0.0, 0.025)], 8, BRONZE, vis=(1,)),
                      rz=-90.0 * sx, t=(sx * R * 0.99, ys, 0.0)))
    # the striker log (shumoku) on two ropes, at the -x seat
    lx0, lx1 = -(R + 0.12), -(R + 1.25)
    out.append(pole((lx0, ys, 0.0), (lx1, ys, 0.0), 0.075, WEATH, n=8, vis=(1,), caps="wood_endgrain"))
    for x in (lx0 - 0.15, lx1 + 0.15):
        out.append(cord((x, ys + 0.075, 0.0), (x, 0.0, 0.0), 0.008))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(lathe([(0.0, y0), (R, y0 - 0.08), (R, y0 - H), (0.0, y0 - H)], 8, BRONZE, vis=(2,), smooth=False))
    P.add(box(lx1, lx0, ys - 0.07, ys + 0.07, -0.07, 0.07, WEATH, vis=(2,)))
    P.add(cyl_col(R, y0 - H, y0, n=8, mat=BRONZE))
    P.add(col(lx1, lx0, ys - 0.08, ys + 0.08, -0.08, 0.08, WEATH))
    P.finish_hang()
    P.dim("height", H, H, tol=0.005)
    P.dim("d", D, D, tol=0.005)
    P.notes.append("the temple bell (bonsho) on the shoro's bell_hook (mount beam: the memory point), the striker "
                   "log on its ropes at the -x side; bell bottom %.2f m under the hook" % (H - y0))
    return P


def gyoban():
    P = LPart("gyoban", budget="furniture", mass=8.0, anchor="hang", flat=True)
    y = -0.40
    t = 0.04
    pieces = [[(-0.42, 0.0), (-0.30, -0.10), (-0.20, -0.11), (-0.20, 0.11), (-0.30, 0.10)],                 # head
              [(-0.20, -0.11), (0.20, -0.09), (0.20, 0.09), (-0.20, 0.11)],                                  # body
              [(0.20, -0.09), (0.30, -0.05), (0.30, 0.05), (0.20, 0.09)],
              [(0.30, -0.05), (0.44, -0.13), (0.40, 0.0), (0.44, 0.13), (0.30, 0.05)]]                       # tail
    out = []
    for poly in pieces:
        out.append(xf(prism(poly, "z", -t, t, WEATH, vis=(1,)), t=(0.0, y, 0.0)))
    out.append(box(-0.33, -0.31, y + 0.02, y + 0.05, -t - 0.004, t + 0.004, DARK, vis=(1,)))               # eye
    out.append(xf(lathe([(0.0, -0.04), (0.04, 0.0), (0.0, 0.04)], 6, SHU, vis=(1,)), t=(-0.43, y, 0.0)))   # the jewel
    for x in (-0.15, 0.20):
        out.append(cord((x, y + 0.10, 0.0), (x, 0.0, 0.0), 0.006))
    out.append(cord((0.0, y - 0.09, 0.0), (0.0, y - 0.30, 0.0), 0.005))
    out.append(pole((0.0, y - 0.30, 0.0), (0.0, y - 0.55, 0.0), 0.014, WOOD, n=5, vis=(1,)))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(box(-0.44, 0.44, y - 0.13, y + 0.13, -t, t, WEATH, vis=(2,)))
    P.finish_hang()
    P.dim("length", 0.88, 0.88, tol=0.01)
    P.notes.append("Zen wooden fish board (gyoban / mokuhan) with its mallet, hung by the kuri entrance (mount beam)")
    return P


def umpan():
    P = LPart("umpan", budget="small", mass=6.0, anchor="hang", flat=True)
    y = -0.35
    out = []
    for (cx, cy, r) in ((0.0, 0.05, 0.13), (-0.14, -0.02, 0.10), (0.14, -0.02, 0.10)):
        out.append(xf(lathe([(0.0, -0.012), (r, -0.012), (r, 0.012), (0.0, 0.012)], 10, BRONZE, vis=(1,)), rx=90.0,
                      t=(cx, y + cy, 0.0)))
    out.append(W(-0.22, 0.22, y - 0.12, y - 0.04, -0.012, 0.012, BRONZE, vis=(1,)))
    out.append(cord((0.0, y + 0.18, 0.0), (0.0, 0.0, 0.0), 0.006))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(box(-0.24, 0.24, y - 0.12, y + 0.18, -0.012, 0.012, BRONZE, vis=(2,)))
    P.finish_hang()
    P.dim("width", 0.46, 0.46, tol=0.01)
    P.notes.append("Zen cloud-shaped bronze gong (umpan) hung at the kuri (mount beam)")
    return P


# ================================================================================================ amulets
def ofuda_stack():
    P = LPart("ofuda_stack", budget="small", mass=0.8, anchor="floor", flat=True)
    out = []
    for i, (x, h) in enumerate(((-0.14, 0.05), (-0.07, 0.03), (0.0, 0.06))):
        out.append(W(x - 0.03, x + 0.03, 0.0, h, -0.09, 0.09, PAPER, vis=(1,)))
        out.append(stext((x, h + 0.0015, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), 0.15, "ofuda_jingu", LIFE,
                         wear="_w2", width=0.045))
    for k, m in enumerate((RED, INDIGO, RED, KINARI)):                   # omamori bags
        out.append(W(0.07 + 0.045 * (k % 2), 0.105 + 0.045 * (k % 2), 0.0, 0.012, -0.08 + 0.06 * (k // 2),
                     -0.03 + 0.06 * (k // 2), m, vis=(1,)))
    out.append(W(0.10, 0.18, 0.0, 0.035, 0.05, 0.12, WOOD, vis=(1,)))   # print block
    wear_all(out, "_w2")
    P.adds(out)
    P.add(W(-0.18, 0.18, 0.0, 0.06, -0.09, 0.12, PAPER, vis=(2,)))
    P.dim("w", 0.36, 0.36, tol=0.01)
    P.notes.append("talismans (ofuda) in stacks, amulet bags, a print block: dressing for the amulet counter (mount "
                   "surface)")
    return P


PROPS = [
    {"id": "jp_f_saisen_bako", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_saisen_bako_l", "l", "intact", "Offering box (saisen-bako), large", lambda: saisen_bako(1.50, 0.55, 0.55)),
        M("jp_f_saisen_bako_m", "m", "intact", "Offering box, medium", lambda: saisen_bako(1.20, 0.50, 0.50)),
        M("jp_f_saisen_bako_s", "s", "intact", "Donation box, small", lambda: saisen_bako(1.00, 0.45, 0.45, "_w2")),
    ]},
    {"id": "jp_f_suzu_rope", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_suzu_rope", "rope", "intact", "Shrine bell with its pull rope", lambda: suzu_rope()),
        M("jp_f_suzu_rope_faded", "rope", "faded", "Shrine bell, the rope faded", lambda: suzu_rope(True)),
    ]},
    {"id": "jp_f_odaiko", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_odaiko", "stand", "intact", "Big drum (odaiko) on its stand", odaiko),
        M("jp_f_kagura_drums", "kagura", "intact", "Kagura drum on its stand + flute", kagura_drums),
    ]},
    {"id": "jp_f_gaku", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_gaku_hachimangu", "hachimangu", "intact", "Shrine name board: Hachimangu",
          lambda: gaku("gaku_hachimangu")),
        M("jp_f_gaku_nenbutsu", "nenbutsu", "intact", "Hall plaque: Namu Amida Butsu",
          lambda: gaku("sotoba_namuamida", w=0.45, h=1.05)),
        M("jp_f_gaku_worn_h", "worn", "worn", "Name board, text weathered off (horizontal)",
          lambda: gaku(None, w=1.00, h=0.40, worn=True)),
    ]},
    {"id": "jp_f_hassokuan", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_hassokuan_s", "s", "dusty", "Offering table (hassoku-an) with offerings, as left", lambda: hassokuan(0.9)),
        M("jp_f_hassokuan_l", "l", "dusty", "Offering table, wide, with offerings", lambda: hassokuan(1.2)),
    ]},
    {"id": "jp_f_shintai_zushi", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_shintai_zushi", "std", "dusty", "Sanctum cabinet with mirror and gohei", lambda: shintai_zushi(0.55)),
        M("jp_f_shintai_zushi_s", "s", "dusty", "Sanctum cabinet, small", lambda: shintai_zushi(0.42)),
    ]},
    {"id": "jp_f_ema_rail", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_ema_rail", "rail", "intact", "Votive boards (ema) on a rail", ema_rail)]},
    {"id": "jp_f_kagura_masks", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_kagura_masks", "masks", "intact", "Kagura masks and bell tree on pegs", kagura_masks)]},
    {"id": "jp_f_dais", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_dais_amida", "amida", "dusty", "Altar dais with Amida in its zushi (Jodo)",
          lambda: dais("amida", 2.4, 0.85, 0.85)),
        M("jp_f_dais_shaka", "shaka", "dusty", "Altar dais with Shaka in its zushi (Zen)",
          lambda: dais("shaka", 2.0, 0.85, 0.85)),
        M("jp_f_dais_kannon", "kannon", "dusty", "Altar dais with a standing Kannon", lambda: dais("kannon", 1.6, 0.70, 0.70)),
        M("jp_f_dais_jizo", "jizo", "dusty", "Altar dais with a standing Jizo", lambda: dais("jizo", 1.5, 0.70, 0.65)),
    ]},
    {"id": "jp_f_tengai", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_tengai", "std", "dusty", "Canopy (tengai) over the image", lambda: tengai())]},
    {"id": "jp_f_sutra_desk", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_sutra_desk", "std", "dusty", "Sutra desk with sutras, bowl gong and mokugyo", sutra_desk),
        M("jp_f_mokugyo_l", "big", "dusty", "Big round mokugyo on its cushion (Zen)", mokugyo_l),
    ]},
    {"id": "jp_f_waniguchi", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_waniguchi", "std", "intact", "Flat bronze gong (waniguchi) with its rope", waniguchi)]},
    {"id": "jp_f_bonsho", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_bonsho_s", "s", "intact", "Temple bell (bonsho), village size, with the striker log",
          lambda: bonsho(0.95, 0.56)),
        M("jp_f_bonsho_l", "l", "intact", "Temple bell (bonsho), town size, with the striker log",
          lambda: bonsho(1.20, 0.72)),
    ]},
    {"id": "jp_f_zen_signals", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_gyoban", "fish", "intact", "Zen fish board (gyoban) with mallet", gyoban),
        M("jp_f_umpan", "cloud", "intact", "Zen cloud gong (umpan)", umpan),
    ]},
    {"id": "jp_f_ofuda_stack", "cat": CAT, "mount": "surface", "models": [
        M("jp_f_ofuda_stack", "std", "intact", "Talisman stacks, amulets, print block", ofuda_stack)]},
]


# ================================================================================================ stone terrace
def terrace(W_=12.0, D=11.0, H=1.10):
    """A stone-faced hall terrace (ishidan / kidan) for a hall on a slope: cut-stone retaining faces front and sides,
    a packed-earth top with a Roadway, a dressed stone flight down the middle of the front (rise 0.16, tread 0.303,
    cheek stones). Origin = the centre of the platform at its FOOT (y 0 = the bottom of the front face); the back
    is meant to sink into the rising ground. The hall stands on the top (y = H)."""
    import skit
    P = LPart("terrace", budget="medium", mass=50000.0, anchor="floor")
    RISE, TREAD = 0.16, 0.91 / 3
    n = int(math.ceil(H / RISE))
    rise = H / n
    run = n * TREAD
    sw = 2.40
    r = rng("terrace%.1f" % W_)
    out = []
    ch = 0.55                                                            # course height
    k = int(math.ceil(H / ch))
    for side in ("front", "left", "right"):
        L = W_ if side == "front" else D
        m = max(2, int(round(L / 0.95)))
        for c_ in range(k):
            y0, y1 = c_ * H / k, (c_ + 1) * H / k
            off = 0.5 if c_ % 2 else 0.0
            edges = [0.0] + [min(L, (i + off) * L / m) for i in range(1, m + 1)]
            edges = sorted(set(edges))
            for a, b in zip(edges[:-1], edges[1:]):
                if b - a < 0.15:
                    continue
                if side == "front":
                    x0, x1 = -W_ / 2 + a + 0.003, -W_ / 2 + b - 0.003
                    if x1 > -sw / 2 - 0.25 and x0 < sw / 2 + 0.25:          # the flight's mouth
                        if x0 < -sw / 2 - 0.25:
                            x1 = -sw / 2 - 0.25
                        elif x1 > sw / 2 + 0.25:
                            x0 = sw / 2 + 0.25
                        else:
                            continue
                    bb = W(x0, x1, y0 + 0.003, y1, D / 2 - 0.35, D / 2, CUTSTONE, vis=(1,), uvoff=(r.random(), r.random()))
                else:
                    sx = -1 if side == "left" else 1
                    z0, z1 = -D / 2 + a + 0.003, -D / 2 + b - 0.003
                    x0, x1 = sorted((sx * W_ / 2, sx * (W_ / 2 - 0.35)))
                    bb = W(x0, x1, y0 + 0.003, y1, z0, z1, CUTSTONE, vis=(1,), uvoff=(r.random(), r.random()))
                out.append(bb)
    out.append(W(-W_ / 2 + 0.30, W_ / 2 - 0.30, H - 0.06, H, -D / 2, D / 2 - 0.30, "ground_earth_bare", vis=(1,)))
    out.append(W(-W_ / 2, W_ / 2, H - 0.06, H + 0.002, D / 2 - 0.36, D / 2, CUTSTONE, vis=(1,)))       # coping
    out.append(W(-W_ / 2, -W_ / 2 + 0.36, H - 0.06, H + 0.002, -D / 2, D / 2 - 0.36, CUTSTONE, vis=(1,)))
    out.append(W(W_ / 2 - 0.36, W_ / 2, H - 0.06, H + 0.002, -D / 2, D / 2 - 0.36, CUTSTONE, vis=(1,)))
    # the flight: dressed treads from the foot (z = D/2 + run) up to the coping (z = D/2), hidden ramp + Roadway
    zf = D / 2 + run
    for i in range(1, n + 1):
        za, zb = zf - (i - 1) * TREAD, zf - i * TREAD
        top = i * rise
        for j in range(3):
            x0 = -sw / 2 + sw * j / 3 + (0.002 if j else 0.0)
            x1 = -sw / 2 + sw * (j + 1) / 3 - (0.002 if j < 2 else 0.0)
            out.append(W(x0, x1, max(0.0, top - rise - 0.10), top, zb - (0.06 if i < n else 0.0), za, CUTSTONE,
                         vis=(1,), uvoff=(r.random(), r.random())))
    for sx in (-1, 1):                                                   # cheek stones
        x = sx * (sw / 2 + 0.12)
        c_ = core.hexa([(x - 0.12, 0.0, zf + 0.05), (x + 0.12, 0.0, zf + 0.05), (x + 0.12, 0.0, D / 2 - 0.30),
                        (x - 0.12, 0.0, D / 2 - 0.30), (x - 0.12, 0.30, zf + 0.05), (x + 0.12, 0.30, zf + 0.05),
                        (x + 0.12, H + 0.25, D / 2 - 0.30), (x - 0.12, H + 0.25, D / 2 - 0.30)], CUTSTONE, vis=(1, 2))
        out.append(c_)
    for i in range(4):                                                   # a few leaf drifts on the top
        out.append(skit.leaves(400 + i, r.uniform(-W_ / 2 + 1, W_ / 2 - 1), r.uniform(-D / 2 + 1, D / 2 - 1),
                               r.uniform(0.4, 0.9), H + 0.003, wear="_w2"))
    P.adds(out)
    P.add(W(-W_ / 2, W_ / 2, 0.0, H, -D / 2, D / 2, CUTSTONE, vis=(2,)))
    P.add(core.hexa([(-sw / 2, 0.0, zf), (sw / 2, 0.0, zf), (sw / 2, 0.0, D / 2), (-sw / 2, 0.0, D / 2),
                     (-sw / 2, 0.0, zf), (sw / 2, 0.0, zf), (sw / 2, H, D / 2), (-sw / 2, H, D / 2)], CUTSTONE,
                    vis=(2,)) if False else W(-sw / 2, sw / 2, 0.0, H * 0.5, D / 2, zf, CUTSTONE, vis=(2,)))
    cols = [col(-W_ / 2, W_ / 2, 0.0, H, -D / 2, D / 2, CUTSTONE)]
    wedge = core.Solid([(-sw / 2, 0.0, zf), (sw / 2, 0.0, zf), (sw / 2, 0.0, D / 2), (-sw / 2, 0.0, D / 2),
                        (-sw / 2, H, D / 2), (sw / 2, H, D / 2)],
                       [[0, 1, 2, 3], [3, 2, 5, 4], [0, 4, 5, 1], [0, 3, 4], [1, 5, 2]], CUTSTONE, vis=(), geo=True,
                       view=True, fire=True)
    cols.append(wedge)
    P.adds(cols)
    P.road([(-W_ / 2, H, D / 2), (W_ / 2, H, D / 2), (W_ / 2, H, -D / 2), (-W_ / 2, H, -D / 2)], "gravel")
    P.road([(-sw / 2, 0.0, zf), (sw / 2, 0.0, zf), (sw / 2, H, D / 2), (-sw / 2, H, D / 2)], "stone_ext")
    P.dim("W", W_, W_, tol=0.005)
    P.dim("H", H, H, tol=0.005)
    P.extra["terrace"] = {"W": W_, "D": D, "H": H, "flight_run": round(run, 3)}
    P.notes.append("stone hall terrace %.1f x %.1f, %.2f m at the front (its back sinks into the slope); the flight "
                   "down the front middle runs %.2f m out from the front face" % (W_, D, H, run))
    return P


PROPS.append({"id": "jp_f_terrace", "cat": CAT, "mount": "floor", "models": [
    M("jp_f_terrace_l", "l", "intact", "Stone hall terrace 12 x 11 x 1.35 with its front flight",
      lambda: terrace(12.0, 11.0, 1.35)),
    M("jp_f_terrace_m", "m", "intact", "Stone hall terrace 10 x 7.4 x 1.8 with its front flight",
      lambda: terrace(10.0, 7.4, 1.80)),
]})
