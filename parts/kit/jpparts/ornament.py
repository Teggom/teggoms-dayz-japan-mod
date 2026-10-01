"""Ridge ornaments for shrine and temple halls (W2P1, 2026-10-01; jp_p_roof_ornament; PARTS_GAP_AUDIT §3 part 15,
the village-grade subset). Period form and choices: parts/W2P1_NOTES.md.

  chigi(part, x, apex_y, zr, t, cut)        crossed finials at a gable end (okichigi: placed astride the ridge, the
                                             lower ends lying on the slopes). cut 'soto' = the tips cut vertical,
                                             'uchi' = cut horizontal
  katsuogi(part, x0, x1, y, zr, n)           n logs lying across the ridge (Ise convention: odd with soto chigi, even
                                             with uchi)
  oniita(part, x, y, zr, sg)                 wooden ridge-end board for board / bark ridges
  oni_hall(part, x, y, zr, sg)               the large onigawara of a tiled hall ridge (kawara.onigawara, hall size)
  hoju(part, base, kind)                     the apex finial of a hogyo roof: roban base, fukubachi, lotus seat, jewel
Everything that forms the outline keeps a simplified version in every LOD (PLAYBOOK §15 T7b). Visual only: they sit on
a roof whose collision is the roof's.
"""
import math

from .core import Part, Solid, box, prism, rings, ngon, KEN, HALF, add, mul
from .shapes import tube
from . import kawara as K

MAT = "wood_weathered"
METAL = "metal_iron"            # stand-in for bronze (parts/W2P1_NOTES.md: missing material)


def chigi(part, x, apex_y, zr, t=None, cut="soto", w=0.20, th=0.06, angle=50.0, foot=0.16, foot_y=0.04, up=0.55,
          mat=MAT, vis=(1, 2, 3)):
    """Okichigi: two crossed boards placed astride the ridge at the gable end x. Each board's lower end rests on the
    ridge cap's side (foot m out from the ridge line zr, foot_y over the covering's apex line apex_y), it rises at
    `angle` through the crossing over the ridge and runs `up` m past it; the tip is cut vertical (soto) or horizontal
    (uchi). The boards stand side by side in x (no shared faces). Nothing reaches down into the roof slopes (C12).
    t (the roof pitch) is unused: okichigi keep their own angle. Returns the top height."""
    a = math.radians(angle)
    c, s = math.cos(a), math.sin(a)
    tops = []
    for k, sgz in enumerate((1.0, -1.0)):             # board whose foot is on the +z side rises towards -z, then mirror
        dz, dy = -sgz * c, s
        nz, ny = sgz * s, c                            # upward normal of the board's lower edge
        z0, y0 = zr + sgz * foot, apex_y + foot_y
        L = lambda u, o: (z0 + u * dz + o * nz, y0 + u * dy + o * ny)      # noqa: E731  (z, y)
        uc = foot / c                                   # the crossing over the ridge line
        utip = uc + up
        if cut == "soto":                               # vertical cut through the centreline tip
            zc = L(utip, w / 2)[0]
            ul = (zc - z0) / dz
            uu = (zc - z0 - w * nz) / dz
        else:                                           # horizontal cut
            yc = L(utip, w / 2)[1]
            ul = (yc - y0) / dy
            uu = (yc - y0 - w * ny) / dy
        poly = [L(0.0, 0.0), L(ul, 0.0), L(uu, w), L(0.0, w)]
        x0 = x - th if k == 0 else x + 0.002
        part.add(prism([(y, z) for z, y in poly], "x", x0, x0 + th, mat, vis=vis, tag="chigi", grain="long"))
        tops.append(max(p[1] for p in poly))
    return max(tops)


def katsuogi(part, x0, x1, y, zr, n=3, r=0.07, length=0.80, mat=MAT, inset=0.35, vis=(1, 2, 3)):
    """n round logs across the ridge between x0 + inset and x1 - inset, their axis along z, lying on the ridge top y
    (sunk 2 cm into the ridge cap). Ends taper slightly (frustum caps)."""
    xs = [x0 + inset] if n == 1 else [x0 + inset + (x1 - x0 - 2 * inset) * k / (n - 1) for k in range(n)]
    yc = y + r - 0.02
    for x in xs:
        part.add(tube((x, yc, zr - length / 2 + 0.05), (x, yc, zr + length / 2 - 0.05), r, mat, n=8, vis=vis,
                      tag="katsuogi", grain="long"))
        for sg in (-1, 1):
            a = (x, yc, zr + sg * (length / 2 - 0.05))
            b = (x, yc, zr + sg * length / 2)
            part.add(tube(a, b, r, mat, n=8, r1=r * 0.82, vis=(1,), tag="katsuogi_end"))
    return yc + r


def oniita(part, x, y, zr, sg, w=0.46, h=0.48, th=0.045, mat=MAT, vis=(1, 2, 3)):
    """Wooden ridge-end board (oni-ita) standing at the ridge end x, its face towards sg (x), foot at the ridge line
    y: a shield outline (square foot, stepped shoulders, pointed top) and a raised border on its face."""
    prof = [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, h * 0.55), (w * 0.30, h * 0.78), (0.0, h), (-w * 0.30, h * 0.78),
            (-w / 2, h * 0.55)]
    xa, xb = (x, x + sg * th)
    part.add(prism([(y + yy, zr + zz) for zz, yy in prof], "x", min(xa, xb), max(xa, xb), mat, vis=vis, tag="oniita"))
    xc = xb + sg * 0.012
    part.add(box(min(xb, xc), max(xb, xc), y + 0.06, y + h * 0.50, zr - w * 0.36, zr + w * 0.36, mat, vis=(1,),
                 tag="oniita_panel"))
    return y + h


def oni_hall(part, x, y, zr, sg, height=0.62, width=0.52):
    """The large onigawara of a tiled hall ridge (kawara.onigawara at hall size, with the far-LOD block)."""
    K.onigawara(part, (x, y, zr), (float(sg), 0.0, 0.0), height=height, width=width, sui=False)
    return y + height


def hoju(part, base, kind="hoju_bronze", s=1.0):
    """Apex finial on `base` (x, y, z): square roban base with a sloped top, inverted bowl (fukubachi), lotus seat
    (ukebana), the jewel (hoju) with its flame tip. kind 'hoju_bronze' (iron stand-in) | 'hoju_kawara' (tile).
    Returns the top height."""
    bx, by, bz = base
    m = METAL if kind == "hoju_bronze" else "roof_kawara"
    # roban: square box + sloped top (frustum)
    a, b = 0.20 * s, 0.13 * s
    part.add(rings(([(bx - a, bz - a), (bx + a, bz - a), (bx + a, bz + a), (bx - a, bz + a)],
                    [(by, 1.0), (by + 0.14 * s, 1.0), (by + 0.20 * s, b / a)]), m, vis=(1, 2, 3), tag="roban"))
    y = by + 0.20 * s
    n = 10
    # fukubachi: inverted bowl (radius profile concave: convex solid)
    part.add(rings((ngon(bx, bz, 0.16 * s, n), [(y, 1.0), (y + 0.05 * s, 0.98), (y + 0.10 * s, 0.82),
                                                 (y + 0.13 * s, 0.45)]), m, vis=(1, 2, 3), tag="fukubachi"))
    y += 0.13 * s
    part.add(rings((ngon(bx, bz, 0.035 * s, 8), [(y - 0.01 * s, 1.0), (y + 0.10 * s, 1.0)]), m, vis=(1, 2),
                   tag="hoju_stem"))
    y += 0.10 * s
    # ukebana: lotus seat widening upwards (frustum: convex)
    part.add(rings((ngon(bx, bz, 0.15 * s, n), [(y, 0.45), (y + 0.05 * s, 0.85), (y + 0.08 * s, 1.0)]), m,
                   vis=(1, 2, 3), tag="ukebana"))
    y += 0.08 * s
    # the jewel: a bulb (concave radius profile) and its pointed flame tip
    part.add(rings((ngon(bx, bz, 0.15 * s, n), [(y, 0.62), (y + 0.08 * s, 0.96), (y + 0.14 * s, 1.0),
                                                 (y + 0.22 * s, 0.80), (y + 0.29 * s, 0.38), (y + 0.32 * s, 0.10)]),
                   m, vis=(1, 2, 3), tag="hoju"))
    part.add(tube((bx, y + 0.315 * s, bz), (bx, y + 0.41 * s, bz), 0.014 * s, m, n=6, r1=0.002, vis=(1,),
                  tag="hoju_tip"))
    return y + 0.41 * s


# ------------------------------------------------------------------------------------------------ parts
VARIANTS = {
    "_chigi_soto": ("okichigi pair at one gable end, tips cut VERTICAL (soto-sogi; male kami by the Ise convention): "
                    "two crossed boards astride the ridge, lower ends on the slopes", [1, 2, 3]),
    "_chigi_uchi": ("okichigi pair, tips cut HORIZONTAL (uchi-sogi; female kami)", [1, 2, 3]),
    "_katsuogi_2": ("2 katsuogi logs across a 1-ken ridge (even: with uchi-sogi chigi)", [1, 2, 3]),
    "_katsuogi_3": ("3 katsuogi logs across a 1-ken ridge (odd: with soto-sogi chigi); generator takes n 2-9", [1, 2, 3]),
    "_katsuogi_5": ("5 katsuogi logs across a 3-ken ridge", [2, 3]),
    "_oniita": ("wooden ridge-end board (oni-ita) for board / bark ridges", [1, 2, 3]),
    "_oni_hall": ("large onigawara (0.62 m) for a tiled hall ridge (kawara.onigawara at hall size)", [2, 3]),
    "_hoju_bronze": ("hoju finial for a hogyo hall: roban, fukubachi, lotus seat, jewel; bronze type (iron "
                     "stand-in: no bronze material)", [1, 2, 3]),
    "_hoju_kawara": ("hoju finial in tile (kawara) for tiled / thatched hogyo halls", [1, 2, 3]),
}


def part_ornament(variant):
    used, tiers = VARIANTS[variant]
    p = Part("jp_p_roof_ornament", variant, "roof", tiers=tiers, used_for=used,
             recipe="ornament.chigi / katsuogi / oniita / oni_hall / hoju (see the module docstring)",
             datum="ridge apex (covering top at the ridge) at the origin; ridge along x; pitch 0.45 (24.2 deg)")
    t = 0.45
    if variant.startswith("_chigi"):
        top = chigi(p, 0.0, 0.0, 0.0, t, cut=variant[7:])
        p.dim("chigi_rise_over_ridge_m", "0.6-0.8 (A)", round(top, 3))
        p.dims[-1]["ok"] = 0.5 <= top <= 0.9
    elif variant.startswith("_katsuogi"):
        n = int(variant[-1])
        L = KEN if n <= 3 else 3 * KEN
        katsuogi(p, 0.0, L, 0.0, 0.0, n)
        p.dim("katsuogi_count", n, n, tol=0)
        p.conn("ridge", (0, 0, 0))
        p.conn("ridge", (L, 0, 0))
    elif variant == "_oniita":
        oniita(p, 0.0, 0.0, 0.0, 1)
    elif variant == "_oni_hall":
        oni_hall(p, 0.0, 0.0, 0.0, 1)
    else:
        top = hoju(p, (0.0, 0.0, 0.0), kind=variant[1:])
        p.dim("hoju_height_m", "0.9-1.2 (A)", round(top, 3))
        p.dims[-1]["ok"] = 0.8 <= top <= 1.25
    p.conn("ridge", (0, 0, 0), note="datum on the ridge / apex")
    return p


def register(reg):
    reg("jp_p_roof_ornament", list(VARIANTS), part_ornament)
