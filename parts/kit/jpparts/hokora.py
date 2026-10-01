"""Micro-shrines (hokora): 4 stone + 4 wood (W2P1, 2026-10-01; jp_p_site_hokora; KEEP_CIVIC Shinto 1, PARTS_GAP_AUDIT
§3 part 42 + the wood variants of SH1). Site objects with no interior (D9: their doors are decorative). Period form
and choices: parts/W2P1_NOTES.md.

Stone shrines (sekishi): a roof stone on a body stone with carved double doors, on one or two base stones; gable,
hipped, nagare (front slope longer) and niche types. Wooden hokora: a miniature nagare or shinmei shrine on a stone
base; Inari ones painted shu; some stand inside a small shelter shed (saya-do).

Frame: x centred on 0 (left-right), +z = the front (the doors), y 0 = grade. Collision: one convex Geometry / View /
Fire solid per stone or roof slab; small detail is visual only. Faces <= 1,500 (G1 A3-9).
"""
import math

from .core import Part, box, prism, rings, ngon, stone, rng_for
from .shapes import rough_block, tube, board_run
from . import ornament as ORN

ST = "stone_carved_aged"
WD = "wood_weathered"
SHU = "paint_shu"
RF = "roof_kokera"


def _geo(**kw):
    return dict(geo=True, view=True, fire=True, **kw)


def base_stones(p, rng, w, d, h1=0.22, h2=0.14, mat=ST, rough=True):
    """Two stacked base stones (the lower wider). Returns the top height."""
    p.add(rough_block(rng, -w / 2, w / 2, -0.06, h1, -d / 2, d / 2, mat, chamfer=0.02, top_jit=0.004, vis=(1, 2, 3),
                      tag="base_stone", **_geo()))
    if h2:
        w2, d2 = w * 0.80, d * 0.80
        p.add(rough_block(rng, -w2 / 2, w2 / 2, h1 + 0.003, h1 + h2, -d2 / 2, d2 / 2, mat, chamfer=0.015, top_jit=0.003,
                          vis=(1, 2, 3), tag="base_stone", **_geo()))
        return h1 + h2
    return h1


def carved_doors(p, x0, x1, y0, y1, zf, mat=ST, proud=0.006):
    """Carved double doors on a stone face at zf: two panels standing `proud` out with a 1 cm parting line and a
    carved frame line round them (visual)."""
    xm = (x0 + x1) / 2
    for (a, b) in ((x0, xm - 0.005), (xm + 0.005, x1)):
        p.add(box(a, b, y0, y1, zf, zf + proud, mat, vis=(1,), tag="carved_door"))
    p.add(box(x0 - 0.02, x1 + 0.02, y1 + 0.004, y1 + 0.02, zf, zf + proud * 0.6, mat, vis=(1,), tag="carved_lintel"))


def gable_roof_stone(p, w, d, y0, h, front=None, mat=ST, ridge=True):
    """A gable roof stone over x -w/2..w/2, z -d/2..d/2 (front = the +z half-depth, None = symmetric: nagare when the
    front half is longer). Two convex halves (front and back slopes) and a ridge strip."""
    zf = d / 2 if front is None else front
    zb = -d / 2
    zr = 0.0 if front is None else -0.04                # nagare: the ridge sits back, the front slope runs out
    t_e = 0.05                                          # eave edge thickness
    # front half: profile in (y, z) from the eave edge up to the ridge
    for (ze, sg) in ((zf, 1.0), (zb, -1.0)):
        poly = [(y0, ze), (y0 + t_e, ze), (y0 + h, zr), (y0, zr)] if sg > 0 else [(y0, zr), (y0 + h, zr), (y0 + t_e, ze),
                                                                                  (y0, ze)]
        p.add(prism(poly, "x", -w / 2, w / 2, mat, vis=(1, 2, 3), tag="roof_stone", **_geo()))
    if ridge:
        p.add(box(-w / 2 - 0.01, w / 2 + 0.01, y0 + h - 0.035, y0 + h + 0.03, zr - 0.04, zr + 0.04, mat, vis=(1, 2, 3),
                  tag="ridge_stone"))
    return y0 + h + 0.03


def hip_roof_stone(p, w, d, y0, h, mat=ST):
    """A hipped roof stone: a square-based frustum to a short ridge, and a jewel knob on top."""
    r = rings(([(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)],
               [(y0, 1.0), (y0 + 0.05, 1.0), (y0 + h, 0.22)]), mat, vis=(1, 2, 3), tag="roof_stone", **_geo())
    p.add(r)
    p.add(rings((ngon(0.0, 0.0, 0.05, 8), [(y0 + h - 0.01, 0.9), (y0 + h + 0.04, 1.0), (y0 + h + 0.08, 0.7),
                                            (y0 + h + 0.11, 0.15)]), mat, vis=(1, 2), tag="knob"))
    return y0 + h + 0.11


# ------------------------------------------------------------------------------------------------ stone
def stone_hokora(p, kind):
    rng = rng_for(p.name)
    y = base_stones(p, rng, 0.74, 0.60, 0.22, 0.14)
    bw, bd, bh = 0.42, 0.36, 0.40
    if kind == "niche":
        bw, bd, bh = 0.46, 0.38, 0.58
    p.add(rough_block(rng, -bw / 2, bw / 2, y + 0.003, y + bh, -bd / 2, bd / 2, ST, chamfer=0.012, top_jit=0.0,
                      vis=(1, 2, 3), tag="body_stone", **_geo()))
    zf = bd / 2
    if kind == "niche":
        # an arched niche: a dark recess panel with a rounded head (visual), a small offering ledge
        p.add(box(-0.13, 0.13, y + 0.10, y + 0.38, zf - 0.005, zf + 0.002, "wood_sooted", vis=(1, 2), tag="niche"))
        p.add(box(-0.09, 0.09, y + 0.38, y + 0.44, zf - 0.005, zf + 0.002, "wood_sooted", vis=(1,), tag="niche_head"))
        p.add(box(-0.16, 0.16, y + 0.06, y + 0.10, zf, zf + 0.06, ST, vis=(1, 2), tag="ledge"))
        top = y + bh
        p.add(rough_block(rng, -0.32, 0.32, top + 0.003, top + 0.09, -0.27, 0.27, ST, chamfer=0.02, top_jit=0.01,
                          vis=(1, 2, 3), tag="roof_slab", **_geo()))
        return top + 0.09
    carved_doors(p, -0.13, 0.13, y + 0.06, y + 0.31, zf)
    top = y + bh + 0.003
    if kind == "kirizuma":
        return gable_roof_stone(p, 0.62, 0.56, top, 0.20)
    if kind == "nagare":
        return gable_roof_stone(p, 0.60, 0.62, top, 0.22, front=0.40)
    return hip_roof_stone(p, 0.62, 0.56, top, 0.20)


# ------------------------------------------------------------------------------------------------ wood
def mini_roof(p, w, d_front, d_back, y_eave_f, t, th=0.035, mat=RF, ridge_mat=WD, gov=0.08):
    """A miniature board gable over x -w/2..w/2: the front slope from z d_front up to the ridge at z 0, the back from
    the ridge down to -d_back, both at pitch t; board slabs (convex) + a ridge cap + bargeboards. Returns (ridge y,
    ridge z)."""
    yr = y_eave_f + t * d_front
    x0, x1 = -w / 2 - gov, w / 2 + gov
    for (ze, sg) in ((d_front, 1.0), (-d_back, -1.0)):
        ye = yr - t * abs(ze)
        poly = [(ye, ze), (ye + th, ze), (yr + th, 0.0), (yr, 0.0)]
        if sg < 0:
            poly = poly[::-1]
        p.add(prism(poly, "x", x0, x1, mat, vis=(1, 2, 3), tag="mini_roof", uvscale=(0.5, 0.5), **_geo()))
        p.add(prism(poly, "x", x0 - 0.018, x0 - 0.004, WD, vis=(1, 2), tag="mini_hafu"))
        p.add(prism(poly, "x", x1 + 0.004, x1 + 0.018, WD, vis=(1, 2), tag="mini_hafu"))
    p.add(box(x0 - 0.01, x1 + 0.01, yr + th - 0.01, yr + th + 0.045, -0.045, 0.045, ridge_mat, vis=(1, 2, 3),
              tag="mini_ridge"))
    return yr + th + 0.045, 0.0


def wood_hokora(p, kind, cx=0.0, cz=0.0, base=True):
    """A miniature wooden shrine. kind 'nagare' | 'shinmei' | 'inari'. Built at the origin (then moved by cx, cz when
    used inside a saya shed)."""
    q = Part("mini", "", "")
    rng = rng_for(p.name + kind)
    paint = SHU if kind == "inari" else WD
    y = base_stones(q, rng, 0.86, 0.80, 0.24, 0.0) if base else 0.0
    # stilts: four short legs, a floor box
    bw, bd = 0.56, 0.46
    y_floor = y + (0.20 if kind == "shinmei" else 0.14)
    for x in (-bw / 2 + 0.04, bw / 2 - 0.04):
        for z in (-bd / 2 + 0.04, bd / 2 - 0.04):
            q.add(box(x - 0.025, x + 0.025, y + 0.003, y_floor - 0.04, z - 0.025, z + 0.025, paint, vis=(1, 2),
                      tag="mini_leg"))
    q.add(box(-bw / 2 - 0.06, bw / 2 + 0.06, y_floor - 0.04, y_floor, -bd / 2 - 0.02, bd / 2 + 0.10, WD, vis=(1, 2, 3),
              tag="mini_floor", **_geo()))
    # body: boarded box with doors on the front, corner posts
    bh = 0.48 if kind != "shinmei" else 0.52
    q.add(box(-bw / 2, bw / 2, y_floor + 0.003, y_floor + bh, -bd / 2, bd / 2, paint, vis=(1, 2, 3), tag="mini_body",
              **_geo()))
    for x in (-bw / 2, bw / 2):
        for z in (-bd / 2, bd / 2):
            q.add(box(x - 0.03, x + 0.03, y_floor + 0.003, y_floor + bh + 0.02, z - 0.03, z + 0.03, paint, vis=(1, 2),
                      tag="mini_post"))
    zf = bd / 2
    xm = 0.0
    for (a, b) in ((-0.17, xm - 0.004), (xm + 0.004, 0.17)):
        q.add(box(a, b, y_floor + 0.06, y_floor + bh - 0.07, zf + 0.002, zf + 0.018, WD, vis=(1, 2), tag="mini_door"))
        for yy in (y_floor + 0.12, y_floor + bh - 0.16):
            q.add(box(a + 0.01, a + 0.09, yy, yy + 0.02, zf + 0.018, zf + 0.022, "metal_iron", vis=(1,), tag="hasso"))
    # front steps (decorative, three small treads)
    for k in range(3):
        q.add(box(-0.12, 0.12, y_floor - 0.04 - (k + 1) * 0.045, y_floor - 0.04 - k * 0.045, bd / 2 + 0.10 + k * 0.07,
                  bd / 2 + 0.17 + k * 0.07, WD, vis=(1,), tag="mini_step"))
    y_eave = y_floor + bh + 0.02
    if kind == "shinmei":
        yr, zr = mini_roof(q, bw, 0.40, 0.40, y_eave, 0.80)
        # chigi from the bargeboards and 3 katsuogi
        for xg in (-bw / 2 - 0.08, bw / 2 + 0.08):
            ORN.chigi(q, xg + (0.012 if xg < 0 else -0.012), yr - 0.04, zr, cut="soto", w=0.06, th=0.02, angle=48.0,
                      foot=0.07, foot_y=0.0, up=0.22, mat=WD)
        ORN.katsuogi(q, -bw / 2, bw / 2, yr - 0.005, zr, n=3, r=0.03, length=0.30, inset=0.10)
    else:
        yr, zr = mini_roof(q, bw, 0.62, 0.34, y_eave, 0.50)          # nagare: the front slope runs out
        ORN.katsuogi(q, -bw / 2, bw / 2, yr - 0.005, zr, n=2, r=0.028, length=0.26, inset=0.12)
    if cx or cz:
        q = q.transformed(0.0, (cx, 0.0, cz))
    p.merge(q)
    return yr


def saya(p):
    """A small shelter shed (saya-do) over a wooden nagare hokora: four posts, a board gable roof, side boards to
    half height at the back, the hokora on a stone inside."""
    rng = rng_for(p.name + "saya")
    W, D = 1.36, 1.10
    for x in (-W / 2, W / 2):
        for z in (-D / 2, D / 2):
            p.add(stone(rng, x, z, 0.24, 0.22, 0.10, 0.06, "stone_field", bury=0.06, vis=(1, 2), tag="saya_stone"))
            p.add(box(x - 0.05, x + 0.05, 0.06, 1.95, z - 0.05, z + 0.05, WD, vis=(1, 2, 3), tag="saya_post",
                      **_geo()))
    for z in (-D / 2, D / 2):
        p.add(box(-W / 2 - 0.12, W / 2 + 0.12, 1.95, 2.07, z - 0.05, z + 0.05, WD, vis=(1, 2, 3), tag="saya_keta"))
    # back and sides boarded to 1.10
    for (x0, x1, z0, z1) in ((-W / 2 + 0.05, W / 2 - 0.05, -D / 2 - 0.015, -D / 2 + 0.002),):
        p.extend(board_run(x0, x1, 0.10, 1.10, z0, z1, rng, 0.18, 0.26, WD, vis=(1, 2), tag="saya_board", gap=0.006))
    # roof: board gable, ridge along x, pitch 0.5, overhangs 0.45 (eaves) / 0.25 (verges)
    t, ov = 0.50, 0.45
    yr = 2.07 + t * (D / 2)
    for (sg) in (1.0, -1.0):
        ze = sg * (D / 2 + ov)
        ye = yr - t * (D / 2 + ov)
        poly = [(ye, ze), (ye + 0.04, ze), (yr + 0.04, 0.0), (yr, 0.0)]
        if sg < 0:
            poly = poly[::-1]
        p.add(prism(poly, "x", -W / 2 - 0.25, W / 2 + 0.25, RF, vis=(1, 2, 3), tag="saya_roof", uvscale=(0.6, 0.6),
                    **_geo()))
    p.add(box(-W / 2 - 0.27, W / 2 + 0.27, yr + 0.03, yr + 0.10, -0.06, 0.06, WD, vis=(1, 2, 3), tag="saya_ridge"))
    p.add(rough_block(rng, -0.50, 0.50, -0.06, 0.20, -0.42, 0.40, ST, chamfer=0.02, top_jit=0.004, vis=(1, 2, 3),
                      tag="base_stone", **_geo()))
    q = Part("inner", "", "")
    wood_hokora(q, "nagare", base=False)
    p.merge(q.transformed(0.0, (0.0, 0.203, -0.06)))
    return yr + 0.10


VARIANTS = {
    "_stone_kirizuma": ("stone shrine (sekishi): gable roof stone, body with carved double doors, two base stones",
                        [1, 2, 3]),
    "_stone_yosemune": ("stone shrine with a hipped roof stone and a jewel knob", [1, 2, 3]),
    "_stone_nagare": ("stone shrine whose roof stone runs out at the front (nagare form)", [1, 2, 3]),
    "_stone_niche": ("tall stone with an offering niche and a flat roof slab (roadside / summit kami stone)", [1, 2, 3]),
    "_wood_nagare": ("wooden hokora: miniature nagare-zukuri (front slope runs out), kokera roof, doors with iron "
                     "fittings, 2 katsuogi, on a stone base", [1, 2, 3]),
    "_wood_shinmei": ("wooden hokora in shinmei form: steep straight gable, chigi + 3 katsuogi, on short legs", [1, 2, 3]),
    "_wood_inari": ("alley / yard Inari hokora painted shu (nagare form); fox pair and torii are props", [1, 2, 3]),
    "_wood_saya": ("a wooden nagare hokora inside a shelter shed (saya-do): four posts, board gable roof, back boarded",
                   [1, 2, 3]),
}


def part_hokora(variant):
    used, tiers = VARIANTS[variant]
    p = Part("jp_p_site_hokora", variant, "site", tiers=tiers, used_for=used,
             recipe="hokora.stone_hokora(part, kind) / wood_hokora(part, kind) / saya(part)",
             datum="x centred, +z = front (doors), y 0 = grade; a site object with no interior (D9)")
    kind = variant.split("_", 2)[2]
    if variant.startswith("_stone"):
        top = stone_hokora(p, kind)
    elif kind == "saya":
        top = saya(p)
    else:
        top = wood_hokora(p, kind)
    p.dim("height_m", "0.7-1.5 (hokora) / 2.6 (saya)", round(top, 3), source="BUILDING_LIST hokora 0.3-1 m on a base")
    p.dims[-1]["ok"] = 0.6 <= top <= 2.8
    p.conn("grade", (0, 0, 0))
    return p


def register(reg):
    reg("jp_p_site_hokora", list(VARIANTS), part_hokora)
