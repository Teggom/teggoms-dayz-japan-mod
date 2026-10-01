"""Storey helpers for two-storey temple structures (agent W2P2, 2026-10-01): the cheap part of jp_p_frame_storey
(PARTS_GAP_AUDIT §3 part 10) that the bell tower (shoro) and the gate / drum tower need first.

  hakama(part, cx, cz, hb, ht, y0, y1)    the flared skirt (hakama-goshi): four battered board walls from a square
                                          base (half width hb) in to the upper floor (half width ht), a sill, a
                                          kasagi cap and corner posts; optional doorway on one side
  deck(part, cx, cz, half, y, ...)        the upper floor: a board deck with an edge beam (koshi-gumi bracket arms
                                          under it), Geometry + Roadway; the railing is W2P1's koran.rail
Frame: as the kit (x, y up, z); cx, cz = the plan centre.
"""
import math

from .core import Part, Solid, box, hexa, add, mul, norm
from .shapes import oriented_box

WOOD = "wood_weathered"


def hakama(part, cx, cz, hb, ht, y0, y1, t=0.08, mat=WOOD, door=None, door_w=1.10, door_h=1.95):
    """Four battered walls. Each side is one convex slab (plan trapezoid mitred at the corners, faces sloped by the
    batter) in every LOD, with Geometry. door = 'front' | 'back' | 'left' | 'right' leaves a doorway (two slabs
    beside it, a lintel slab over it) and returns its rectangle."""
    out = {}
    sides = {"front": (0.0, 1.0), "back": (0.0, -1.0), "left": (-1.0, 0.0), "right": (1.0, 0.0)}
    for name, (nx, nz) in sides.items():
        ax, az = -nz, nx                                 # along the side
        def P(a, y, inner):
            hw = hb + (ht - hb) * (y - y0) / (y1 - y0)   # outer half width at height y
            off = hw - (t if inner else 0.0)
            return (cx + nx * off + ax * a, y, cz + nz * off + az * a)

        def corners(a0, a1, ya, yb):
            # a0 / a1: along-limits as functions of the height (mitre at the corners: |a| <= offset)
            pts = []
            for y in (ya, yb):
                for inner in (False, True):
                    hw = hb + (ht - hb) * (y - y0) / (y1 - y0) - (t if inner else 0.0)
                    lo = max(-hw, a0) if a0 is not None else -hw
                    hi = min(hw, a1) if a1 is not None else hw
                    pts.append((P(lo, y, inner), P(hi, y, inner)))
            (o0l, o0h), (i0l, i0h), (o1l, o1h), (i1l, i1h) = pts
            return [o0l, o0h, i0h, i0l, o1l, o1h, i1h, i1l]

        if door == name:
            for a0, a1 in ((None, -door_w / 2), (door_w / 2, None)):
                part.add(hexa(corners(a0, a1, y0, y1), mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                              tag="hakama"))
            part.add(hexa(corners(-door_w / 2, door_w / 2, y0 + door_h, y1), mat, vis=(1, 2, 3), geo=True, view=True,
                          fire=True, tag="hakama"))
            out["door"] = (name, cx + nx * hb, cz + nz * hb, door_w, door_h)
        else:
            part.add(hexa(corners(None, None, y0, y1), mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                          tag="hakama"))
    # sill at the foot and a kasagi cap at the top (slightly proud), corner posts along the battered edges
    for (y, hw, h, tag) in ((y0, hb + 0.03, 0.12, "hakama_sill"), (y1 - 0.02, ht + 0.05, 0.10, "hakama_kasagi")):
        part.add(box(cx - hw, cx + hw, y, y + h, cz - hw, cz + hw, mat, vis=(1, 2, 3), tag=tag) if tag == "hakama_kasagi"
                 else _ring(cx, cz, hw, hw - 0.14, y, y + h, mat))
    for sx in (-1, 1):
        for sz in (-1, 1):
            a = (cx + sx * (hb + 0.012), y0 + 0.12, cz + sz * (hb + 0.012))
            b = (cx + sx * (ht + 0.012), y1 - 0.02, cz + sz * (ht + 0.012))
            d = norm((b[0] - a[0], b[1] - a[1], b[2] - a[2]))
            c = mul(add(a, b), 0.5)
            e1 = norm((sx, 0.0, -sz))
            e2 = norm((e1[1] * d[2] - e1[2] * d[1], e1[2] * d[0] - e1[0] * d[2], e1[0] * d[1] - e1[1] * d[0]))
            part.add(oriented_box(c, d, e1, e2, math.dist(a, b) / 2, 0.07, 0.07, mat, vis=(1, 2), tag="hakama_post",
                                  grain="long"))
    return out


def _ring(cx, cz, ho, hi, y0, y1, mat):
    """A square frame sill as ONE closed solid is not convex: return its outer box (the inside is the hakama)."""
    return box(cx - ho, cx + ho, y0 + 0.003, y1, cz - ho, cz + ho, mat, vis=(1, 2, 3), tag="hakama_sill")


def deck(part, cx, cz, half, y, t=0.10, mat=WOOD, beam=0.20):
    """Upper floor deck: a board slab (top y), an edge beam round it, Geometry + Roadway."""
    part.add(box(cx - half, cx + half, y - t, y, cz - half, cz + half, {"top": "floor_boards_rough", "default": mat},
                 vis=(1, 2, 3), geo=True, view=True, fire=True, tag="deck"))
    part.road([(cx - half + 0.02, y, cz - half + 0.02), (cx + half - 0.02, y, cz - half + 0.02),
               (cx + half - 0.02, y, cz + half - 0.02), (cx - half + 0.02, y, cz + half - 0.02)], "boards_ext")
    hb = half + 0.03
    for (x0, x1, z0, z1, grow) in ((cx - hb, cx + hb, cz + half - 0.05, cz + hb, 0.0),
                                   (cx - hb, cx + hb, cz - hb, cz - half + 0.05, 0.0),
                                   (cx - hb + 0.004, cx - half + 0.05, cz - half + 0.05, cz + half - 0.05, 0.004),
                                   (cx + half - 0.05, cx + hb - 0.004, cz - half + 0.05, cz + half - 0.05, 0.004)):
        part.add(box(x0, x1, y - t - beam - grow, y - t - 0.004 + grow * 0.0, z0, z1, mat, vis=(1, 2, 3),
                     tag="deck_beam", grain="long"))
    return {"y": y, "half": half}


def part_storey(variant):
    """jp_p_frame_storey_hakama: the bell-tower lower storey (hakama skirt) with the upper deck on it."""
    p = Part("jp_p_frame_storey", variant, "frame", tiers=[2, 3],
             used_for="bell tower / drum tower lower storey: flared hakama skirt + upper deck (W2P2, the cheap part of "
                      "PARTS_GAP_AUDIT #10)",
             recipe="storey.hakama(part, cx, cz, hb, ht, y0, y1, door=) + storey.deck(part, cx, cz, half, y)",
             datum="plan centre (1.365, -1.365) = a 1.5-ken upper bay; y 0 = platform top; deck top 2.80")
    cx, cz = 1.365, -1.365
    hakama(p, cx, cz, hb=2.05, ht=1.62, y0=0.0, y1=2.50, door="back")
    deck(p, cx, cz, 2.05, 2.80)
    p.dim("batter_deg", "8-15", round(math.degrees(math.atan((2.05 - 1.62) / 2.50)), 2), tol=0.0,
          source="W2P2_NOTES §4 (GK: ~12 deg)")
    p.notes.append("The doorway (back) leads to the stair / ladder W2S adds inside; the railing is W2P1's koran.rail.")
    return p


def register(reg):
    reg("jp_p_frame_storey", ["_hakama"], part_storey)
