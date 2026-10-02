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


def _dx():
    """FX2's detail remakes (spikes/FX2/detail_fx2.py)."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "FX2"))
    import detail_fx2
    return detail_fx2


def rot(ss, **kw):
    return [xf(s, **kw) for s in ss]


def mv(ss, t):
    return [xf(s, t=t) for s in ss]


# ================================================================================================ offering box
def saisen_bako(w, d, h, wear="_w1"):
    """FX2 (2026-10-01): the detail remake (spikes/FX2/detail_fx2.py: slats, iron straps with nails, the bronze
    crest, a hasp). FX1's rule stays: no litter decal on the box."""
    return _dx().saisen_box(w, d, h, wear)


def suzu_rope(faded=False):
    """FX2: the detail remake (spikes/FX2/detail_fx2.py)."""
    return _dx().suzu_rope(faded)


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
    """FX2: the detail remake (spikes/FX2/detail_fx2.py: two rows + a framed gaku-ema)."""
    return _dx().ema_rail()


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
    """FX2 (Stephen: 'P5: masks etc. on the wall are too low resolution'): sculpted masks (spikes/FX2/detail_fx2.py)."""
    return _dx().kagura_masks()


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


def image(kind):
    """FX2: the altar image on its lotus seat and octagonal tiers, with its halo. Returns (Res 1 solids, Res 2 solids,
    total height). Amida: seated, jobon-josho-in, the wheel halo (Met 44890); Shaka: seated, semui-in + yogan-in, a
    boat halo with flames (CMA 153384, CMA 147590); Kannon: standing Sho Kannon, a boat halo (CMA 152018, Met 49257);
    Jizo: standing monk with the jewel and the ringed staff, no halo (Met 53175, Met 76084). Gilt (jp_m_gilt_worn)
    except Jizo (black-brown lacquered wood, a bronze staff)."""
    sys.path.insert(0, os.path.join(DEV, "spikes", "FX2"))
    import fx2props as FX
    hi, lo = [], []
    gilt = FX.GILT
    if kind in ("amida", "shaka"):
        b, by = FX.octagon_tiers([(0.27, 0.04), (0.235, 0.03)], LACQ, vis=(1, 2), wear="_w2")
        hi += b
        R = 0.22
        hi += FX.lotus(R, gilt, vis=((1,), (2,), ()), t=(0.0, by, 0.0), wear="_w1")
        ty = by + FX.lotus_top(R)
        Hs = 0.50
        name = "nyorai_jo" if kind == "amida" else "nyorai_semui"
        f = FX.figure(name, Hs, gilt, vis=((1,), (2,), ()), t=(0.0, ty - 0.01, 0.0), wear="_w1")
        hi += [q for q in f if 1 in q.vis]
        lo += [q for q in f if 2 in q.vis]
        head_y = ty + Hs * 0.80
        if kind == "amida":
            hi += FX.halo_wheel(ty + Hs * 0.52, 0.115, 0.30, gilt, z=-0.165, vis=(1,), wear="_w2", cy_head=head_y)
            lo.append(FX.disc(0.31, 0.014, gilt, n=10, vis=(2,), wear="_w2"))
            lo[-1] = xf(lo[-1], t=(0.0, ty + Hs * 0.52, -0.165))
            top = ty + Hs * 0.52 + 0.33
        else:
            bh = 0.66
            hi += mv(FX.halo_boat(0.62, bh, gilt, z=-0.17, vis=(1,), wear="_w2", head=(head_y - ty + 0.01, 0.12)),
                     (0.0, ty, 0.0))
            lo += mv(FX.halo_boat(0.62, bh, gilt, z=-0.17, vis=(2,), wear="_w2"), (0.0, ty, 0.0))
            top = ty + bh
        return hi, lo, top
    b, by = FX.octagon_tiers([(0.19, 0.035)], LACQ, vis=(1, 2), wear="_w2")
    hi += b
    R = 0.15
    hi += FX.lotus(R, gilt if kind == "kannon" else KURO, vis=((1,), (2,), ()), t=(0.0, by, 0.0), wear="_w1")
    ty = by + FX.lotus_top(R)
    Hf = 0.68 if kind == "kannon" else 0.66
    if kind == "kannon":
        f = FX.figure("kannon", Hf, gilt, vis=((1,), (2,), ()), t=(0.0, ty - 0.005, 0.0), wear="_w1")
        bh = 0.82
        hi += mv(FX.halo_boat(0.38, bh, gilt, z=-0.11, vis=(1,), wear="_w2", head=(Hf * 0.87, 0.085)), (0.0, ty, 0.0))
        lo += mv(FX.halo_boat(0.38, bh, gilt, z=-0.11, vis=(2,), wear="_w2"), (0.0, ty, 0.0))
        top = ty + bh
    else:
        f = FX.figure("jizo", Hf, {"*": KURO, "staff": BRONZE, "staffhead": BRONZE}, vis=((1,), (2,), ()),
                      t=(0.0, ty - 0.005, 0.0), wear="_w1")
        top = ty + Hf * 1.19
    hi += [q for q in f if 1 in q.vis]
    lo += [q for q in f if 2 in q.vis]
    return hi, lo, top


def dais(kind, W_=2.4, D=0.85, H=0.85):
    """Sumeru dais (shumidan) with a zushi cabinet (doors open) holding the image, and the three altar pieces."""
    P = LPart("dais", budget="statue", mass=150.0, anchor="floor")   # FX2: the image is a statue (PLAYBOOK §12)
    # CA1 (was FX2's ad-hoc class 'altar' 5,500): a statue is 'as needed (aim <= 3,000)'; 3,690-4,622 faces
    P.over_budget_ok = "the seated image (a statue, as needed) + its zushi cabinet, dais and three altar pieces in one model"
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
    # FX2 (2026-10-01, Stephen: 'the Buddha statue is a blob ... any humanoid statue should have a picture
    # reference'): the sculpted images (spikes/FX2, research/statues/NOTES.md) on lotus seats with their halos
    fig, fig_lo, fh = image(kind)
    zw, zd = (0.95, 0.55) if figure == "seated" else (0.70, 0.42)
    zh = fh + 0.18                                                     # FX2: was + 0.30
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
    out += mv(fig_lo, (0.0, H + 0.05, zz + 0.03))
    # the three altar pieces in front of the zushi, dusty and burnt down
    fz = D / 2 - 0.13
    out += mv(LR.koro(0.0, fz, r=0.06, wear="_w2"), (0.0, H, 0.0))
    out += mv(LR.candle_stand(-0.32, fz, h=0.22, candle=0.015, wear="_w2"), (0.0, H, 0.0))
    out += mv(LR.vase_flowers(0.32, fz, dry=True, wear="_w2"), (0.0, H, 0.0))
    if kind == "jizo":                                                   # small offerings left before Jizo
        out += mv(LR.sanbo(0.0, fz - 0.17, wear="_w2", full=False), (0.0, H, 0.0))
    P.adds(out)
    P.add(W(-W_ / 2, W_ / 2, 0.0, H, -D / 2, D / 2, LACQ, vis=(2,)))
    for q in (W(-zw / 2, zw / 2, H, H + 0.05, zz - zd / 2, zz + zd / 2, LACQ, vis=(2,)),      # FX2: the open cabinet at
              W(-zw / 2, zw / 2, H, zt + 0.14, zz - zd / 2, zz - zd / 2 + 0.03, LACQ, vis=(2,)),   # LOD 2 (the image
              W(-zw / 2, -zw / 2 + 0.03, H, zt + 0.14, zz - zd / 2, zz + zd / 2, LACQ, vis=(2,)),  # shows through)
              W(zw / 2 - 0.03, zw / 2, H, zt + 0.14, zz - zd / 2, zz + zd / 2, LACQ, vis=(2,)),
              W(-zw / 2 - 0.08, zw / 2 + 0.08, zt, zt + 0.14, zz - zd / 2 - 0.06, zz + zd / 2 + 0.10, LACQ, vis=(2,))):
        P.add(q)
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
    """FX2: the detail remake (spikes/FX2/detail_fx2.py)."""
    return _dx().waniguchi()


def bonsho(H=0.95, D=0.56):
    P = LPart("bonsho", budget="detail", mass=400.0, anchor="hang")   # FX2: bell + log + ropes (+30 %)
    P.over_budget_ok = "temple bell body + its striker log and ropes in one model (CA1: was FX2's 'detail_l' 2,250)"
    out = [pole((0.0, 0.0, 0.0), (0.0, -0.05, 0.0), 0.03, IRON, n=6, vis=(1,))]
    # the dragon-head lug (ryuzu): an arch of two heads
    out.append(W(-0.10, 0.10, -0.12, -0.05, -0.035, 0.035, BRONZE, vis=(1,)))
    for sx in (-1, 1):
        out.append(W(sx * 0.10 - 0.03 if sx > 0 else -0.13, 0.13 if sx > 0 else -0.07, -0.20, -0.08, -0.05, 0.05,
                     BRONZE, vis=(1,)))
    y0 = -0.20
    R = D / 2
    # FX2 (2026-10-01): the bell at detail fidelity (spikes/FX2/detail_fx2.bonsho_body: 32 sides, nyu, bands, lotus
    # seats, the two-headed dragon lug); FX1's hook, log and ropes below are unchanged
    body, ys = _dx().bonsho_body(H, D, y0, BRONZE)
    out = [pole((0.0, 0.0, 0.0), (0.0, -0.05, 0.0), 0.02, IRON, n=8, vis=(1,))] + body     # the hook into the lug
    # the striker log (shumoku) on two ropes, at the -x seat. FX1 (2026-10-01, Stephen: 'the rope hanging the log
    # floats in mid air, attached to nothing'): the log runs UNDER the bell beam (the shoro dressings hang the bell at
    # yaw 90, beam along the log), so both ropes rise straight to the beam's underside (y 0, as the hook) and end in
    # an iron eye driven into it; the log is 1.0 m so the outer rope stays under the beam (beam half-length >= 1.36)
    lx0, lx1 = -(R + 0.10), -(R + 1.10)
    out.append(pole((lx0, ys, 0.0), (lx1, ys, 0.0), 0.075, WEATH, n=8, vis=(1,), caps="wood_endgrain"))
    for x in (lx0 - 0.12, lx1 + 0.18):
        out.append(cord((x, ys + 0.075, 0.0), (x, -0.035, 0.0), 0.008))
        out.append(box(x - 0.012, x + 0.012, -0.035, 0.0, -0.012, 0.012, IRON, vis=(1,)))       # the eye
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
    # FX1 (2026-10-01): no leaf drifts on the top (the precinct has no leaf litter around it; see the offering box)
    for i in range(4):
        r.uniform(-W_ / 2 + 1, W_ / 2 - 1), r.uniform(-D / 2 + 1, D / 2 - 1), r.uniform(0.4, 0.9)   # keep the rng
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
