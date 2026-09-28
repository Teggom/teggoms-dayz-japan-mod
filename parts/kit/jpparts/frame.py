"""Frame parts: posts, beams and rails, dashigeta (build list jp_p_frame_*)."""
import math

from .core import (Part, box, rings, KEN, HALF, POST, POST_FARM, WALL_H, KETA_W, KETA_H, EAVE_Y, rng_for)
from .shapes import tube


# ------------------------------------------------------------------------------------------------ recipes
def post(part, x, z=0.0, y0=0.0, y1=WALL_H, size=POST, mat="wood_weathered", adzed=False, vis=(1, 2, 3), geo=True,
         rng=None, tag="post"):
    h = size / 2
    if not adzed:
        return part.add(box(x - h, x + h, y0, y1, z - h, z + h, mat, vis=vis, geo=geo, view=geo, fire=True if geo else None,
                            tag=tag))
    rng = rng or rng_for(part.name, int(x * 100))
    c = [rng.uniform(0.012, 0.028) for _ in range(4)]
    base = [(x - h + c[0], z - h), (x + h - c[1], z - h), (x + h, z - h + c[1]), (x + h, z + h - c[2]),
            (x + h - c[2], z + h), (x - h + c[3], z + h), (x - h, z + h - c[3]), (x - h, z - h + c[0])]
    n = 5
    prof = []
    for k in range(n + 1):
        t = k / n
        prof.append((y0 + (y1 - y0) * t, 1.0 - 0.018 * (2 * t - 1) ** 2 - rng.uniform(0, 0.006) * (0 < k < n)))
    return part.add(rings((base, prof), mat, vis=vis, geo=geo, view=geo, fire=True if geo else None, tag=tag))


def keta(part, x0, x1, z=0.0, y_top=EAVE_Y, mat="wood_weathered", w=KETA_W, h=KETA_H, vis=(1, 2, 3), geo=True):
    return part.add(box(x0, x1, y_top - h, y_top, z - w / 2, z + w / 2, mat, vis=vis, geo=geo, view=geo,
                        fire=True if geo else None, tag="keta"))


def nuki(part, x0, x1, y, z=0.0, mat="wood_weathered", vis=(1,)):
    return part.add(box(x0, x1, y, y + 0.105, z - 0.015, z + 0.015, mat, vis=vis, tag="nuki"))


def dodai(part, x0, x1, z=0.0, y_top=0.0, mat="wood_weathered", vis=(1, 2, 3), geo=True, size=0.12):
    return part.add(box(x0, x1, y_top - size, y_top, z - size / 2, z + size / 2, mat, vis=vis, geo=geo, view=geo,
                        fire=True if geo else None, tag="dodai"))


def hari_end(part, x, y, z0, z1, log=False, mat="wood_weathered", vis=(1, 2)):
    """Beam end projecting along z from z0 to z1 (gable ends); log = round farmhouse beam."""
    if log:
        return part.add(tube((x, y, z0), (x, y, z1), 0.13, mat, n=10, vis=vis, tag="hari", squash=0.92))
    return part.add(box(x - 0.06, x + 0.06, y - 0.12, y + 0.12, z0, z1, mat, vis=vis, tag="hari"))


# ------------------------------------------------------------------------------------------------ parts
def part_post(variant):
    adz = variant == "_adzed"
    size = POST_FARM if adz else POST
    p = Part("jp_p_frame_post", variant, "frame", tiers=[1] if adz else [2, 3],
             used_for="farmhouse main posts, adze-faceted (T1)" if adz else "every wall, door and pent node (T2-3)",
             datum="post node at sill level (y 0 = post foot on dodai or soseki)")
    post(p, 0.0, size=size, adzed=adz)
    p.conn("post", (0, 0, 0), note="grid node; bottom on soseki or dodai")
    p.conn("post_top", (0, WALL_H, 0), note="keta underside (eave line %.2f = keta top)" % EAVE_Y)
    b = p.solids[0].bbox()
    p.dim("section_m", size, b[1] - b[0])
    p.dim("height_m (sill to keta underside)", WALL_H, b[3] - b[2], source="PLAYBOOK §4 / kit standard")
    return p


def part_beam(variant):
    log = variant == "_log"
    p = Part("jp_p_frame_beam", variant, "frame", tiers=[1] if log else [1, 2, 3],
             used_for="log beam ends of farmhouses (T1)" if log else "wall plate, rails, sill and beam ends of every wall",
             datum="1-ken run from the left post node; y 0 = sill (dodai top)")
    k = keta(p, -0.15, KEN, y_top=EAVE_Y)                       # wall plate, gable end projecting 0.15
    nuki(p, 0.06, KEN - 0.06, 0.95)
    nuki(p, 0.06, KEN - 0.06, 1.85)
    d = dodai(p, 0.0, KEN)
    hari_end(p, 0.0, EAVE_Y + 0.14, 0.06, 0.26 if not log else 0.30, log=log)
    kb, db = k.bbox(), d.bbox()
    p.dim("keta_m", "0.12 x 0.18", 0.0, source="build_list")
    p.dims[-1]["measured"] = "%.3f x %.3f" % (kb[5] - kb[4], kb[3] - kb[2])
    p.dims[-1]["ok"] = abs(kb[5] - kb[4] - 0.12) < 0.01 and abs(kb[3] - kb[2] - 0.18) < 0.01
    p.dim("dodai_m", 0.12, db[3] - db[2])
    p.dim("nuki_depth_m", 0.105, 0.105)
    p.dim("hari_end_projection_m", "0.15-0.25", 0.20 if not log else 0.24, source="build_list (range)")
    p.conn("post", (0, 0, 0))
    p.conn("post", (KEN, 0, 0))
    p.conn("eave", (0, EAVE_Y, 0), note="keta top")
    return p


def dashigeta(part, x0, x1, y_arm=2.95, cant=0.60, mat="wood_street_dark", step=KEN):
    """Arms plugged into each post node from x0 to x1 (step), carrying the dashigeta purlin at the arm ends."""
    xs = []
    x = x0
    while x <= x1 + 1e-6:
        xs.append(x)
        x += step
    for x in xs:
        part.add(box(x - 0.05, x + 0.05, y_arm - 0.18, y_arm, 0.06, cant + 0.10, mat, vis=(1, 2, 3), geo=True, view=True,
                     fire=True, tag="arm"))
    part.add(box(x0 - 0.20, x1 + 0.20, y_arm, y_arm + 0.15, cant - 0.06, cant + 0.06, mat, vis=(1, 2, 3), geo=True,
                 view=True, fire=True, tag="dashigeta"))
    return xs


def part_dashigeta(variant):
    upper = variant == "_upper_front"
    p = Part("jp_p_frame_dashigeta", variant, "frame", tiers=[3],
             deviation="G1 decision 4: post-1750 feature, allowed sparingly on tier 3 only (flagged, optional part)",
             used_for=("projecting upper front on dashigeta arms (Edo shop fronts), tier 3, flagged deviation" if upper
                       else "cantilevered eave purlin carrying a deep street eave (Edo shops, Kiso), tier 3, flagged"),
             datum="2-ken run of the street front, y 0 = ground-floor sill; arms at the upper-floor line")
    cant = 0.45 if upper else 0.60
    y_arm = 2.95
    dashigeta(p, 0.0, 2 * KEN, y_arm=y_arm, cant=cant)
    if upper:
        # projecting upper front: floor boards over the arms, a low plastered front (nuriya) with two board windows
        top = y_arm + 0.15
        p.add(box(-0.1, 2 * KEN + 0.1, top, top + 0.04, 0.06, cant + 0.06, {"top": "wood_weathered",
              "default": "wood_street_dark"}, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="floor"))
        z0, z1 = cant - 0.03, cant + 0.09
        H = 1.30
        wins = [(0.55, 1.27), (2.37, 3.09)]
        xs = [-0.1] + [a for w in wins for a in w] + [2 * KEN + 0.1]
        for k in range(0, len(xs), 2):
            p.add(box(xs[k], xs[k + 1], top + 0.04, top + 0.04 + H, z0, z1, "wall_shikkui", vis=(1, 2, 3), geo=True,
                      view=True, fire=True, tag="upper_front"))
        for a, b in wins:
            p.add(box(a, b, top + 0.04, top + 0.60, z0, z1, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True))
            p.add(box(a, b, top + 1.10, top + 0.04 + H, z0, z1, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True,
                      fire=True))
            p.add(box(a, b, top + 0.60, top + 1.10, z0 + 0.03, z1 - 0.03, "wood_street_dark", vis=(1, 2, 3), geo=True,
                      view=True, fire=True, tag="shutter"))
            for xx in (a + 0.12, (a + b) / 2, b - 0.12):
                p.add(box(xx - 0.015, xx + 0.015, top + 0.60, top + 1.10, z1 - 0.01, z1 + 0.02, "wood_street_dark",
                          vis=(1,)))
        p.add(box(-0.12, 2 * KEN + 0.12, top + 0.04 + H - 0.10, top + 0.04 + H, z0 - 0.02, z1 + 0.03, "wood_street_dark",
                  vis=(1, 2), tag="rail"))
    p.conn("post", (0, 0, 0))
    p.conn("post", (KEN, 0, 0))
    p.conn("post", (2 * KEN, 0, 0))
    p.conn("eave", (0, y_arm + 0.15, cant), note="dashigeta purlin top: the street eave rafters bear here")
    p.dim("cantilever_m", "0.45-0.90", cant, source="build_list (range)")
    return p
