"""W3D site object: the tall fire watchtower (hi-no-mi yagura), town type (spikes/W3D/W3D_NOTES.md site 5). Built into
jp_site.pbo by spikes/W3D/build_w3d_site.py on B3b's site pipeline (like L2's fire-watch ladder). Frame as skit: base
centre on the terrain, +z = the climb face.

Sources: kotobank "fire watchtower": shogunal towers 3 jo (~9 m), open on four sides; daimyo and TOWN towers black and
LOWER; towns rang the hansho bell; Kyoho (1716-36) one tower per ~10 cho. FX4's lesson: the roof's underside 2.20 m over
the deck. FP1's climbing convention (vanilla farm_watertower_small + ActionEnterLadder): a View component 'ladder1', the
Memory points ladder1 / _con / _con_dir / _dir / _bottom_front / _top_front, Geometry class=house + laddertype=wood,
the config class Land_JP_S_<p3d> (B3b build.py 'land').
"""
import math

import l2kit as K
from l2kit import (box, prism, lathe, xf, W, col, col_solid, SPart, pole, beam, add_all, cord, M, WOOD, IRON, CUT)
import props_l2_street as ST          # L2 (read-only): ladder_parts_h()

CAT = "gov_site"
KURO = "wood_kuro"
PROPS = []


def hinomi_yagura():
    """The town fire watchtower: four tapered legs (2.60 m square at the foot, 1.50 m at the deck) on cut-stone
    footings, ties and braces on the back and both sides (none across the ladder face), the ladder up the front (+z)
    face, the lookout deck at 6.40 m (black board parapet 0.95 on three sides + the front corners, the ladder bay open),
    four corner posts carrying a small board gable roof whose underside is 2.20 m over the deck (FX4), the hansho
    bell hung outside the back parapet from the roof's back overhang with its striker on the parapet. Climbable: climb
    the +z face, step off backwards onto the deck."""
    P = SPart("hinomi_yagura", budget="detail", res3=True, mass=900.0, bury=0.52, wear="_w2")
    P.keep_memory = True
    P.geo_props = {"class": "house", "laddertype": "wood"}
    PY = 6.40                                   # the deck (top of the boards)
    RT = PY + 2.20                              # roof underside / tie-beam underside (FX4 head room)
    F, T = 1.30, 0.75                           # leg half-spacing at the foot / at the deck
    ZL = 0.80                                   # the ladder's plane (just outside the deck's front edge)

    def leg_at(y, sx, sz):
        f = (y + 0.5) / (PY - 0.12 + 0.5)
        h = F + (T - F) * f
        return (sx * h, y, sz * h)
    # legs on cut-stone footings
    for sx in (-1, 1):
        for sz in (-1, 1):
            a, b = leg_at(-0.5, sx, sz), leg_at(PY - 0.12, sx, sz)
            P.add(pole(a, b, 0.09, WOOD, n=6, vis=(1, 2)))
            P.add(col_solid(beam(a, leg_at(PY - 0.17, sx, sz), 0.16, 0.16, WOOD)))
            fx, fz = sx * F, sz * F
            P.add(W(fx - 0.24, fx + 0.24, -0.20, 0.10, fz - 0.24, fz + 0.24, CUT, vis=(1, 2)))
    # ties (nuki) at three heights on the back and the sides; X braces on the back and the sides between them
    lv = (1.60, 3.30, 4.90)
    for y in lv:
        for (s0, s1) in (((-1, -1), (1, -1)), ((-1, -1), (-1, 1)), ((1, -1), (1, 1))):
            a, b = leg_at(y, *s0), leg_at(y, *s1)
            P.add(beam(a, b, 0.06, 0.10, WOOD, vis=(1, 2)))
    for (y0, y1) in ((0.10, lv[0]), (lv[0], lv[1]), (lv[1], lv[2])):
        for (s0, s1) in (((-1, -1), (1, -1)), ((-1, -1), (-1, 1)), ((1, -1), (1, 1))):
            P.add(beam(leg_at(y0, *s0), leg_at(y1, *s1), 0.05, 0.07, WOOD, vis=(1,)))
    # the deck: bearers on the leg tops, boards, Roadway; a front bearer under the deck edge (behind the ladder)
    for sx in (-1, 1):
        P.add(W(sx * T - 0.06, sx * T + 0.06, PY - 0.16, PY - 0.03, -T - 0.06, T + 0.06, WOOD, vis=(1, 2)))
    for sz in (-1, 1):
        P.add(W(-T - 0.06, T + 0.06, PY - 0.16, PY - 0.03, sz * T - 0.06, sz * T + 0.06, WOOD, vis=(1, 2)))
    n = 8
    for k in range(n):
        z0 = -T - 0.02 + (2 * T + 0.04) * k / n
        P.add(W(-T - 0.02, T + 0.02, PY - 0.03, PY, z0 + 0.003, z0 + (2 * T + 0.04) / n - 0.003, WOOD, vis=(1,)))
    P.add(W(-T - 0.02, T + 0.02, PY - 0.03, PY, -T - 0.02, T + 0.02, WOOD, vis=(2, 3)))
    P.add(col(-T - 0.06, T + 0.06, PY - 0.16, PY, -T - 0.06, T))
    P.road([(-T, PY, -T), (T, PY, -T), (T, PY, T - 0.02), (-T, PY, T - 0.02)], "boards_ext")
    # the ladder up the front face (rails rise 0.95 over the deck as handholds; no rungs above the deck)
    ls, lc, _ = ST.ladder_parts_h(PY + 0.95 + 0.5, y0=-0.5)
    rails = [q for q in ls if not (q.bbox()[2] > PY + 0.01 and q.bbox()[1] - q.bbox()[0] > 0.3)]
    add_all(P, [xf(q, t=(0.0, 0.0, ZL)) for q in rails])
    lcol = col(-0.25, 0.25, -0.5, PY - 0.03, ZL - 0.03, ZL + 0.03)
    lcol.view = False
    P.add(lcol)
    vt = col(-0.25, 0.25, 0.04, PY + 0.60, ZL - 0.04, ZL + 0.05)          # View-only 'ladder1' (the climb target)
    vt.geo, vt.fire, vt.sel = False, None, "ladder1"
    P.add(vt)
    # the parapet: black boards 0.95 on the back and the sides, short pieces on the front corners (ladder bay open)
    HP = PY + 0.95
    P.add(W(-T, T, PY, HP, -T - 0.03, -T + 0.01, KURO, vis=(1, 2)))
    for sx in (-1, 1):
        P.add(W(sx * T - 0.02 if sx > 0 else -T - 0.01, sx * T + 0.01 if sx > 0 else -T + 0.02, PY, HP, -T, T,
                KURO, vis=(1, 2)))
        P.add(W(min(sx * 0.32, sx * T), max(sx * 0.32, sx * T), PY, HP, T - 0.01, T + 0.03, KURO, vis=(1, 2)))
    for (x0, x1, z0, z1) in ((-T - 0.03, T + 0.03, -T - 0.05, -T + 0.03), (-T - 0.05, -T + 0.03, -T, T + 0.05),
                             (T - 0.03, T + 0.05, -T, T + 0.05)):
        P.add(W(x0, x1, HP, HP + 0.05, z0, z1, KURO, vis=(1, 2)))          # the parapet's cap rail
    P.add(col(-T - 0.03, T + 0.03, PY, HP + 0.05, -T - 0.05, -T + 0.03))
    for sx in (-1, 1):            # the collision pieces only touch (C6b): back | sides | front corners
        P.add(col(sx * T - 0.05, sx * T + 0.05, PY, HP + 0.05, -T + 0.03, T + 0.05))
        P.add(col(min(sx * 0.32, sx * (T - 0.05)), max(sx * 0.32, sx * (T - 0.05)), PY, HP, T - 0.01, T + 0.03))
    # four corner posts to the roof, tie beams under it, the small board gable roof (ridge along x)
    for sx in (-1, 1):
        for sz in (-1, 1):
            P.add(W(sx * (T - 0.03) - 0.05, sx * (T - 0.03) + 0.05, PY, RT, sz * (T - 0.03) - 0.05,
                    sz * (T - 0.03) + 0.05, WOOD, vis=(1, 2)))
            P.add(col(sx * (T - 0.03) - 0.05, sx * (T - 0.03) + 0.05, HP + 0.05, RT, sz * (T - 0.03) - 0.05,
                      sz * (T - 0.03) + 0.05))
    for sz in (-1, 1):
        P.add(W(-T, T, RT - 0.10, RT, sz * (T - 0.03) - 0.05, sz * (T - 0.03) + 0.05, WOOD, vis=(1, 2)))
    for sx in (-1, 1):
        P.add(W(sx * (T - 0.03) - 0.05, sx * (T - 0.03) + 0.05, RT - 0.10, RT, -T, T, WOOD, vis=(1, 2)))
    RZ, RH = 1.20, 0.50                         # the roof's half depth (front-back) and its rise
    for sg in (-1, 1):                           # axis x: poly in (y, z)
        P.add(prism([(RT, sg * RZ), (RT + 0.05, sg * RZ), (RT + RH + 0.05, 0.0), (RT + RH, 0.0)], "x", -1.05, 1.05,
                    WOOD, vis=(1, 2, 3)))
    P.add(W(-1.08, 1.08, RT + RH - 0.02, RT + RH + 0.10, -0.08, 0.08, KURO, vis=(1, 2)))     # ridge board
    P.add(W(-0.10, 0.10, RT, RT + RH, -0.05, 0.05, WOOD, vis=(1,)))                              # king post
    # the hansho bell outside the back parapet, hung from the roof's back overhang; the striker on the cap rail
    bz, by = -T - 0.30, PY + 1.05
    bell = lathe([(0.0, 0.0), (0.14, 0.0), (0.12, 0.08), (0.10, 0.27), (0.05, 0.32), (0.0, 0.33)], 10, IRON, vis=(1, 2))
    P.add(xf(bell, t=(0.0, by, bz)))
    zr = bz
    y_roof = RT + RH * (1.0 - abs(zr) / RZ)
    P.add(cord((0.0, by + 0.33, bz), (0.0, y_roof, bz), 0.008))
    P.add(pole((0.30, HP + 0.05, -T - 0.01), (0.36, HP + 0.40, -T - 0.10), 0.012, WOOD, n=4, vis=(1,)))
    # far LOD stand-ins
    for sx in (-1, 1):
        for sz in (-1, 1):
            P.add(beam(leg_at(-0.5, sx, sz), leg_at(PY - 0.12, sx, sz), 0.16, 0.16, WOOD, vis=(3,)))
    P.add(W(-T, T, PY, HP, -T, T, KURO, vis=(3,)))
    P.add(W(-0.25, 0.25, -0.5, PY + 0.9, ZL - 0.04, ZL + 0.04, WOOD, vis=(3,)))
    P.add(W(-T, T, PY, RT, -T, T, WOOD, vis=(3,)))
    P.dim("deck_head_room", 2.20, RT - PY, tol=0.001)
    P.dim("deck_y", 6.40, PY, tol=0.001)
    P.memory = {
        "ladder1": [(0.0, PY + 0.675, ZL + 0.03), (0.0, 0.54, ZL + 0.03)],
        "ladder1_con": [(0.0, PY, ZL), (0.0, 0.0, ZL + 0.10)],
        "ladder1_con_dir": [(0.0, PY, ZL - 0.45), (0.0, 0.0, ZL + 0.55)],
        "ladder1_dir": [(0.0, 0.0, ZL + 0.55)],
        "ladder1_bottom_front": [(0.0, 0.0, ZL + 0.10)],
        "ladder1_top_front": [(0.0, PY, ZL)],
    }
    P.notes.append("town fire watchtower (hi-no-mi yagura, Kyoho; black, lower than the 3-jo shogunal tower); CLIMBABLE "
                   "like the FP1 ladder: climb the +z face, step off onto the railed deck at 6.40; roof 2.20 m over the "
                   "deck (FX4); the hansho bell outside the back parapet")
    return P


PROPS.append({"id": "jp_s_hinomi_yagura", "cat": CAT, "mount": "yard", "tiers": [2, 3],
              "models": [M("jp_s_hinomi_yagura", "tall", "intact", "Fire watchtower (town, tall) with the alarm bell",
                           hinomi_yagura, land=True)]})
