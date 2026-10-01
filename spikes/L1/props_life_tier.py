"""Life layer F (research/interior/LIFE_LAYER.md items 45-50): tier markers and the rest.

Sword rack, armour chest, bow rack and tea set are upper-house markers (U; the bow rack also tier 2). None of them is
tokonoma dressing (commoner houses have no tokonoma, G1). Stable corner and fallen door leaves close the list. The
'as left' state of the weapon racks is EMPTY: the weapons were taken (they are loot, not dressing).
"""
import math
import random

import lkit
from lkit import (core, box, prism, lathe, xf, xfs, flat_poly, W, board, pole, beam, rope_path, grid_sheet, col, disc,
                  stain, mound, soft_slab, text, LPart, M, rng, bipyramid, lod_box, wear_all, rest, cyl_col,
                  place_group, peg, WOOD, WEATH, IRON, PALE, DARK, LACQ, BAMBOO, WEAVE, MUSHIRO, TAWARA, STACK, ROPE,
                  PAPER, FUSUMA, INDIGO, KINARI, RED, LITTER, LIFE)

CAT = "tier"


# ================================================================================================ 45 sword rack
# FP1 remake (2026-10-01, Stephen: "just squares"): curved swords in full mounts (scabbard with horn cap, mouth band,
# cord knob and wound sageo; round tsuba between washers; the hilt's crossed cord diamonds over white rayskin, collar,
# pommel cap, menuki) on a stand with shaped uprights and arms that curl up to cradle the scabbards
# (spikes/L1/fp1sword.py). Display: edge up, hilt to the viewer's left (+x), the katana below, the wakizashi above.
import fp1sword as FS  # noqa: E402


def sword(L=1.00, wear=None):
    return FS.sword(L, sori=0.018 if L > 0.8 else 0.012, wear=wear)


def _rest_y(arm_top, L, sori, xs):
    """Centre-line y of a sword (local x from its scabbard end) so it rests on arms at local x positions xs."""
    h = 0.029
    cys = [sori * 4 * (x / L) * (1 - x / L) for x in xs]
    return arm_top + h / 2 - sum(cys) / len(cys)


def katanakake(kind):
    wall = kind.startswith("wall")
    empty = kind.endswith("empty")
    wr = "_w2" if empty else None
    th = 0.022
    if wall:
        P = LPart("katanakake", budget="furniture", mass=4.0, anchor="wall", flat=True)
        y = 1.45
        xb = 0.20
        for sx in (-1, 1):                              # two lacquered wall plates, each with two curled arms
            x = sx * xb
            P.add(W(x - 0.03, x + 0.03, y - 0.22, y + 0.12, 0.0, 0.018, LACQ, vis=(1, 2)))
            for yy in (y - 0.12, y + 0.02):
                P.add(FS.arm(x, yy, zf=0.11, th=th, w=0.036))
        if not empty:
            # katana on the lower arms (cradles at local x 0.12 / 0.52), wakizashi above (0.03 / 0.43)
            P.adds(xfs(sword(1.00), t=(-xb - 0.12, _rest_y(y - 0.12 + th / 2, 1.00, 0.018, (0.12, 0.52)), 0.085)))
            P.adds(xfs(sword(0.65), t=(-xb - 0.03, _rest_y(y + 0.02 + th / 2, 0.65, 0.012, (0.03, 0.43)), 0.085)))
        else:
            P.add(stain(451, 0.0, 0.30, 0.25, sx=1.5))
        P.dim("y", 1.45, y, tol=0.005)
    else:
        P = LPart("katanakake", budget="furniture", mass=5.0, anchor="floor")
        h = 0.48
        base = prism([(-0.28, 0.0), (0.28, 0.0), (0.26, 0.028), (-0.26, 0.028)], "z", -0.12, 0.12, LACQ, vis=(1, 2))
        P.add(base)
        for sx in (-1, 1):
            x = sx * 0.18
            P.add(FS.upright(x, h))
            for yy in (0.20, 0.34):
                P.add(FS.arm(x, yy, zf=0.11, th=th, w=0.036))
        if not empty:
            # katana on the lower arms (cradles at local x 0.32 / 0.68), wakizashi above (0.07 / 0.43)
            P.adds(xfs(sword(1.00), t=(-0.50, _rest_y(0.20 + th / 2, 1.00, 0.018, (0.32, 0.68)), 0.085)))
            P.adds(xfs(sword(0.65), t=(-0.25, _rest_y(0.34 + th / 2, 0.65, 0.012, (0.07, 0.43)), 0.085)))
        else:                                           # the swords taken; the rack knocked askew
            P.solids = xfs(P.solids, ry=12.0)
            P.add(stain(452, 0.1, 0.25, 0.25, sx=1.5))
        P.add(col(-0.28, 0.28, 0.0, h, -0.12, 0.12, LACQ) if not empty else
              lkit.fkit.col_solid(xf(box(-0.28, 0.28, 0.0, h, -0.12, 0.12, LACQ), ry=12.0)))
        P.dim("h", 0.48, h, tol=0.005)
    P.add(box(-0.5, 0.5, 0.0 if not wall else 1.25, 0.48 if not wall else 1.57, 0.0, 0.11, LACQ, vis=(2,)))
    for s in P.solids:
        if wr and not getattr(s, "wear", None):
            s.wear = wr
    P.notes.append("sword rack, upper houses only (samurai, headman); the as-left rack is empty: the swords were "
                   "taken; no loot")
    return P


# ================================================================================================ 46 armour chest
def yoroibitsu(kind):
    P = LPart("yoroibitsu", budget="furniture", res3=True, mass=25.0, anchor="floor")
    mat = LACQ if kind != "plain" else WOOD
    wr = "_w2" if kind == "open" else None
    w, d, h = 0.50, 0.40, 0.55
    out = [W(-w / 2, w / 2, 0.02, h - 0.06, -d / 2, d / 2, mat, vis=(1, 2)),
           W(-w / 2 + 0.03, w / 2 - 0.03, 0.0, 0.02, -d / 2 + 0.03, d / 2 - 0.03, mat, vis=(1,))]
    for sx in (-1, 1):                                  # iron rings for the carrying pole, corner irons
        out.append(lathe([(0.03, -0.006), (0.04, -0.006), (0.04, 0.006), (0.03, 0.006)], 6, IRON, vis=(1,)))
        out[-1] = xf(out[-1], rz=90.0, t=(sx * (w / 2 + 0.006), h - 0.16, 0.0))
        for sz in (-1, 1):
            out.append(W(sx * w / 2 - 0.03 * sx - 0.03 * (sx < 0) + 0.0, sx * w / 2 + 0.003 * sx, 0.02, 0.08,
                         sz * d / 2 - 0.01 * sz - 0.01, sz * d / 2 + 0.003 * sz + 0.01, IRON, vis=(1,)))
    out.append(text((0.0, 0.30, d / 2 + 0.001), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.14, LIFE, "crest_mitsubiki",
                    wear="_w1", off=0.002))
    lid = [W(-w / 2 - 0.01, w / 2 + 0.01, 0.0, 0.07, -d / 2 - 0.01, d / 2 + 0.01, mat, vis=(1, 2))]
    for sx in (-0.12, 0.12):                            # rope ties over the lid
        lid.append(W(sx - 0.01, sx + 0.01, 0.07, 0.078, -d / 2 - 0.012, d / 2 + 0.012, RED, vis=(1,)))
    if kind != "open":
        out += xfs(lid, t=(0.0, h - 0.07, 0.0))
        top = h + 0.008
        P.loot_rect("lid", h + 0.0, -w / 2 + 0.05, w / 2 - 0.05, -d / 2 + 0.05, d / 2 - 0.05, rng=0.2,
                    points=[(0.0, h, 0.0)])
    else:                                               # as left: the lid thrown off, the chest empty
        out.append(flat_poly([(-w / 2 + 0.03, -d / 2 + 0.03), (w / 2 - 0.03, -d / 2 + 0.03), (w / 2 - 0.03, d / 2 - 0.03),
                              (-w / 2 + 0.03, d / 2 - 0.03)][::-1], h - 0.061, mat, vis=(1,)))
        out += rest(xfs(lid, rx=-80.0, ry=30.0, t=(0.40, 0.0, 0.40)), 0.0)
        out.append(stain(461, 0.3, 0.4, 0.3, sx=1.5))
        top = h - 0.06
    out.append(W(-w / 2, w / 2, 0.0, top, -d / 2, d / 2, mat, vis=(3,)))
    P.adds(wear_all(out, wr))
    import fkit                                          # F1: a sturdy chest a player may stand on (vanilla practice)
    fkit.road_tops(P, [P.add(col(-w / 2, w / 2, 0.0, top, -d / 2, d / 2, mat))], "boards")
    P.dim("w", 0.50, w, tol=0.005)
    P.dim("h", 0.55, h, tol=0.01)
    P.notes.append("armour chest (yoroi-bitsu), upper tier marker, the crest on its front (life atlas); loot on the "
                   "lid; the open chest is empty (as left)")
    return P


# ================================================================================================ 47 bow rack
def bow(L=2.20, strung=True, snapped=False, wear=None):
    """A Japanese longbow along +x (grip at the lower third), laminated bamboo lacquered; its string."""
    pts = []
    for k in range(9):
        t = k / 8
        x = L * t
        bend = 0.10 * math.sin(math.pi * t) + 0.02 * math.sin(2 * math.pi * t)
        pts.append((x, -bend, 0.0))
    out = []
    for i in range(8):
        out.append(beam(pts[i], pts[i + 1], 0.025, 0.018, LACQ if i not in (2, 3) else BAMBOO, up=(0, 0, 1),
                        vis=(1,)))
    if strung and not snapped:
        out.append(lkit.cord((0.02, 0.0, 0.0), (L - 0.02, 0.0, 0.0), 0.002, KINARI))
    elif snapped:
        out.append(lkit.cord((L - 0.02, 0.0, 0.0), (L - 0.35, -0.30, 0.02), 0.002, KINARI))
    out.append(box(0.0, L, -0.12, 0.01, -0.015, 0.015, LACQ, vis=(2,)))
    return wear_all(out, wear)


def quiver(wear=None):
    """A quiver (utsubo-style box) with arrow shafts and white fletching showing at the top."""
    out = [W(-0.06, 0.06, -0.80, 0.0, -0.04, 0.04, LACQ, vis=(1,))]
    for k in range(5):
        x = -0.04 + 0.02 * k
        out.append(box(x - 0.004, x + 0.004, 0.0, 0.14, -0.004, 0.004, BAMBOO, vis=(1,)))
        out.append(prism([(x, 0.02), (x + 0.012, 0.03), (x + 0.012, 0.10), (x, 0.11)], "z", -0.001, 0.001, PAPER,
                         vis=(1,)))
    return wear_all(out, wear)


def yumi_rack(kind):
    if kind == "stand":
        P = LPart("yumi_rack", budget="small", mass=8.0, anchor="floor")
        P.add(W(-0.25, 0.25, 0.0, 0.06, -0.15, 0.15, LACQ, vis=(1, 2)))
        P.add(W(-0.25, 0.25, 0.0, 2.25, -0.15, -0.12, LACQ, vis=(1, 2)))
        P.add(W(-0.25, 0.25, 1.60, 1.64, -0.15, 0.08, LACQ, vis=(1,)))
        for x in (-0.08, 0.08):
            P.adds(xfs(bow(2.20), rz=90.0, t=(x, 0.06, -0.02)))
        P.adds(xfs(quiver(), t=(0.18, 0.86, -0.06)))
        P.add(col(-0.25, 0.25, 0.0, 2.25, -0.15, 0.10, LACQ))
        P.add(box(-0.25, 0.25, 0.0, 2.25, -0.15, 0.1, LACQ, vis=(2,)))
        P.dim("h", 2.25, 2.25, tol=0.005)
        P.notes.append("upright bow stand (yumi-tate): needs a room >= 2.40 high (samurai / headman houses)")
        return P
    P = LPart("yumi_rack", budget="small", mass=4.0, anchor="wall", flat=True)
    empty = kind == "wall_empty"
    y = 1.80
    for x in (-0.70, 0.70):                             # J hooks
        P.add(W(x - 0.02, x + 0.02, y - 0.22, y + 0.04, 0.0, 0.02, LACQ, vis=(1, 2)))
        P.add(W(x - 0.02, x + 0.02, y - 0.22, y - 0.18, 0.02, 0.12, LACQ, vis=(1,)))
        P.add(W(x - 0.02, x + 0.02, y - 0.18, y - 0.12, 0.10, 0.12, LACQ, vis=(1,)))
    if not empty:
        P.adds(xfs(bow(2.20), t=(-1.10, y - 0.08, 0.07)))
        P.adds(xfs(bow(2.10), t=(-1.05, y - 0.13, 0.10)))
        P.add(peg(0.95, 1.45, z0=0.0))
        P.adds(xfs(quiver(), t=(0.95, 1.40, 0.06)))
    else:                                               # as left: one bow left, its string snapped; the quiver gone
        P.adds(xfs(bow(2.20, snapped=True, wear="_w2"), t=(-1.10, y - 0.08, 0.07)))
        P.add(peg(0.95, 1.45, z0=0.0))
    P.dim("hook_y", 1.80, y, tol=0.005)
    P.notes.append("bows on wall hooks and a quiver (U, and tier 2 village headmen); the as-left rack is nearly empty")
    return P


# ================================================================================================ 48 tea
def chawan(cx, cz, mat=PALE, wear=None):
    return [xf(lathe([(0.0, 0.0), (0.03, 0.0), (0.03, 0.01), (0.06, 0.03), (0.063, 0.075), (0.056, 0.075),
                      (0.05, 0.03), (0.0, 0.015)], 7, mat, vis=(1,), wear=wear), t=(cx, 0.0, cz))]


def natsume(cx, cz):
    return [xf(lathe([(0.0, 0.0), (0.03, 0.0), (0.035, 0.03), (0.034, 0.055), (0.0, 0.065)], 7, LACQ, vis=(1,)),
               t=(cx, 0.0, cz))]


def chasen(cx, cz, lying=False):
    s = lathe([(0.0, 0.0), (0.012, 0.0), (0.012, 0.05), (0.028, 0.07), (0.03, 0.10), (0.0, 0.095)], 7, BAMBOO, vis=(1,))
    ss = [s]
    if lying:
        ss = rest(xfs(ss, rz=90.0), 0.0)
    return xfs(ss, t=(cx, 0.0, cz))


def dobin(cx, cz, wear=None):
    """A top-handled earthenware pot for boiled tea (no side-handled kyusu: LIFE_LAYER_ERA 48), bamboo bail."""
    out = [lathe([(0.0, 0.0), (0.06, 0.0), (0.085, 0.05), (0.08, 0.10), (0.05, 0.125), (0.04, 0.13), (0.0, 0.135)], 8,
                 DARK, vis=(1,), wear=wear),
           pole((0.08, 0.06, 0.0), (0.15, 0.10, 0.0), 0.012, DARK, n=4, vis=(1,), r1=0.007)]
    for k in range(3):
        a0, a1 = math.pi * k / 3, math.pi * (k + 1) / 3
        out.append(pole((0.07 * math.cos(a0), 0.13 + 0.09 * math.sin(a0), 0.0),
                        (0.07 * math.cos(a1), 0.13 + 0.09 * math.sin(a1), 0.0), 0.006, BAMBOO, n=3, vis=(1,)))
    return xfs(out, t=(cx, 0.0, cz))


def tea(kind):
    P = LPart("tea", budget="small", mass=1.5, anchor="floor", flat=True)
    tray = [W(-0.18, 0.18, 0.0, 0.015, -0.13, 0.13, LACQ, vis=(1, 2))]
    if kind == "matcha":
        P.adds(tray)
        P.adds(xfs(chawan(-0.07, 0.02, DARK), t=(0.0, 0.015, 0.0)))
        P.adds(xfs(natsume(0.07, -0.05), t=(0.0, 0.015, 0.0)))
        P.adds(xfs(chasen(0.08, 0.06), t=(0.0, 0.015, 0.0)))
        P.add(xf(box(-0.09, 0.09, 0.0, 0.004, -0.005, 0.005, BAMBOO, vis=(1,)), ry=20.0, t=(-0.02, 0.095, 0.02)))
    elif kind == "dobin":
        P.adds(tray)
        P.adds(xfs(dobin(-0.06, 0.0), t=(0.0, 0.015, 0.0)))
        P.adds(xfs(chawan(0.10, 0.06, PALE), t=(0.0, 0.015, 0.0)))
        P.adds(xfs(chawan(0.10, -0.07, PALE), t=(0.0, 0.015, 0.0)))
    else:                                               # as left: the bowl broken, the pot tipped, the whisk rolled
        P.adds(xfs(tray, ry=15.0))
        P.adds(lkit.shards(481, 0.25, 0.20, 0.08, 7, DARK))
        P.adds(rest(xfs(dobin(0.0, 0.0, wear="_w2"), rz=80.0, ry=40.0, t=(-0.30, 0.0, 0.15)), 0.0))
        P.adds(chasen(0.10, 0.30, lying=True))
        P.adds(xfs(natsume(0.0, 0.0), t=(0.05, 0.015, -0.02)))
        P.add(stain(482, -0.25, 0.20, 0.20, sx=1.5))
    P.add(lod_box([s for s in P.solids if 1 in s.vis], LACQ, vis=(2,)))
    P.dim("tray_w", 0.36, 0.36, tol=0.005)
    P.notes.append("tea utensils of an upper house: the matcha set (bowl, lacquer caddy, whisk, scoop) and a "
                   "top-handled clay pot for boiled tea; no tetsubin (A2 decision 10), no kyusu; mount surface")
    return P


# ================================================================================================ 49 manger (★)
def manger(kind):
    ab = kind.endswith("empty") or kind.endswith("rotted")
    wr = "_w2" if ab else None
    if kind.startswith("straw"):
        P = LPart("manger", budget="small", mass=20.0, anchor="floor", flat=True)
        rr = random.Random(491)
        h = 0.50 if kind == "straw" else 0.22
        base = [(0.60 * math.cos(2 * math.pi * k / 9) * rr.uniform(0.85, 1.1),
                 0.50 * math.sin(2 * math.pi * k / 9) * rr.uniform(0.85, 1.1)) for k in range(9)]
        prof = [(0.0, 1.0), (h * 0.5, 0.85), (h * 0.85, 0.5), (h, 0.15)]
        st = core.rings((core.hull2d(base), prof), STACK, vis=(1, 2))
        st.wear = wr or "_w1"
        P.add(st)
        for k in range(8):                              # loose straws round the foot
            a = rr.uniform(0, 2 * math.pi)
            P.add(xf(box(-0.15, 0.15, 0.0, 0.004, -0.004, 0.004, STACK, vis=(1,)), ry=rr.uniform(0, 180),
                     t=(0.70 * math.cos(a), 0.0, 0.60 * math.sin(a))))
            P.solids[-1].wear = wr or "_w1"
        P.dim("h", 0.50 if kind == "straw" else 0.22, h, tol=0.005)
        P.notes.append("straw pile of the stable corner; no Geometry (you wade through it)")
        return P
    if kind == "cutter":
        P = LPart("manger", budget="small", mass=12.0, anchor="floor", flat=True)
        P.add(board(-0.35, 0.35, 0.0, 0.06, -0.09, 0.09, k=3, vis=(1, 2)))
        P.add(W(0.30, 0.34, 0.06, 0.16, -0.04, 0.04, WEATH, vis=(1,)))
        blade = [prism([(0.0, 0.0), (-0.45, 0.10), (-0.45, 0.14), (0.0, 0.05)], "z", -0.003, 0.003, IRON, vis=(1,)),
                 pole((-0.45, 0.12, 0.0), (-0.70, 0.18, 0.0), 0.02, WEATH, n=5, vis=(1,))]
        P.adds(xfs(blade, t=(0.32, 0.13, 0.0)))
        import props_life_work as PW
        P.adds(xfs(PW.straw_bundle(0.8, 0.07), ry=80.0, t=(-0.05, 0.0, 0.35)))
        P.add(lkit.bits.mound(492, -0.1, -0.25, 0.20, 0.025, STACK, sx=1.5, vis=(1,)))
        P.dim("board_L", 0.70, 0.70, tol=0.005)
        P.notes.append("fodder cutter (oshikiri): a lever blade on a block, cut straw beside it")
        return P
    P = LPart("manger", budget="small", mass=30.0, anchor="floor")
    L, Wd, H = 1.20, 0.45, 0.40
    out = [W(-L / 2, L / 2, 0.18, 0.22, -Wd / 2, Wd / 2, WEATH, vis=(1,)),                          # the bottom
           W(-L / 2, L / 2, 0.18, H, Wd / 2 - 0.03, Wd / 2 + 0.02, WEATH, vis=(1,)),                # front board, splayed
           W(-L / 2, L / 2, 0.18, H, -Wd / 2 - 0.02, -Wd / 2 + 0.03, WEATH, vis=(1,)),
           W(-L / 2, -L / 2 + 0.03, 0.18, H, -Wd / 2, Wd / 2, WEATH, vis=(1,)),
           W(L / 2 - 0.03, L / 2, 0.18, H, -Wd / 2, Wd / 2, WEATH, vis=(1,))]
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * (L / 2 - 0.08) - 0.03, sx * (L / 2 - 0.08) + 0.03, 0.0, 0.18, sz * (Wd / 2 - 0.06) - 0.03,
                         sz * (Wd / 2 - 0.06) + 0.03, WEATH, vis=(1,)))
    out.append(W(-L / 2, L / 2, 0.0, H, -Wd / 2, Wd / 2, WEATH, vis=(2,)))
    P.adds(wear_all(out, wr))
    if kind == "trough":                                # a little fodder left in it
        P.add(xf(lkit.bits.mound(493, 0.25, 0.0, 0.18, 0.04, STACK, sx=1.8, vis=(1,)), t=(0.0, 0.22, 0.0)))
    else:
        P.add(lkit.bits.stain(494, 0.0, 0.0, 0.20, y=0.222, sx=2.2, mat=LITTER, wear="_w2"))
        P.add(lkit.bits.mound(495, 0.3, 0.45, 0.25, 0.02, STACK, sx=1.6, wear="_w2", vis=(1,)))
    P.add(col(-L / 2, L / 2, 0.0, H, -Wd / 2, Wd / 2, WEATH))
    P.loot_rect("bottom", 0.22, -L / 2 + 0.05, -0.05, -Wd / 2 + 0.05, Wd / 2 - 0.05, rng=0.2,
                points=[(-0.30, 0.22, 0.0)])
    P.dim("L", 1.20, L, tol=0.005)
    P.dim("h", 0.40, H, tol=0.005)
    P.notes.append("manger (kaiba-oke) on legs for the inside stable (BUILD_LIST jp_f_manger); loot on its bottom")
    return P


# ================================================================================================ 50 fallen leaf (★)
def leaf(kind, broken=False, torn=False, wear=None):
    """A sliding leaf 0.91 x 1.95 x 0.03 lying face up (x across, z along its height): shoji = frame + kumiko +
    paper; fusuma = frame + paper both faces + a round pull."""
    w, L, t = 0.91, 1.95, 0.03
    out = [W(-w / 2, w / 2, 0.0, t, -L / 2, -L / 2 + 0.04, WOOD, vis=(1, 2)),
           W(-w / 2, w / 2, 0.0, t, L / 2 - 0.05, L / 2, WOOD, vis=(1, 2)),
           W(-w / 2, -w / 2 + 0.03, 0.0, t, -L / 2 + 0.04, L / 2 - 0.05, WOOD, vis=(1, 2)),
           W(w / 2 - 0.03, w / 2, 0.0, t, -L / 2 + 0.04, L / 2 - 0.05, WOOD, vis=(1, 2))]
    pap = PAPER if kind == "shoji" else FUSUMA
    miss = set()
    if torn or broken:
        r = random.Random(501 + (kind == "fusuma"))
        miss = {r.randrange(12) for _ in range(5)}
    cells = []
    for i in range(3):
        for j in range(4):
            if i * 4 + j in miss:
                continue
            x0 = -w / 2 + 0.03 + (w - 0.06) * i / 3
            z0 = -L / 2 + 0.04 + (L - 0.09) * j / 4
            cells.append([(x0, z0), (x0 + (w - 0.06) / 3, z0), (x0 + (w - 0.06) / 3, z0 + (L - 0.09) / 4),
                          (x0, z0 + (L - 0.09) / 4)])
    for c in cells:
        out.append(flat_poly(c[::-1], t * 0.5 + (0.012 if kind == "fusuma" else 0.0), pap, vis=(1,),
                             wear="_w2" if (torn or broken) else "_w1"))
    if kind == "shoji":
        for k in (1, 2):
            x = -w / 2 + 0.03 + (w - 0.06) * k / 3
            out.append(W(x - 0.006, x + 0.006, 0.004, t - 0.004, -L / 2 + 0.04, L / 2 - 0.05, WOOD, vis=(1,)))
        for k in range(1, 8):
            z = -L / 2 + 0.04 + (L - 0.09) * k / 8
            out.append(W(-w / 2 + 0.03, w / 2 - 0.03, 0.004, t - 0.004, z - 0.006, z + 0.006, WOOD, vis=(1,)))
    else:
        out.append(lathe([(0.0, t), (0.03, t), (0.03, t + 0.003), (0.0, t + 0.003)], 8, LACQ, vis=(1,)))
        out[-1] = xf(out[-1], t=(w / 2 - 0.12, 0.0, 0.0))
        if torn:                                        # the lattice core shows through the tear
            for k in range(3):
                out.append(W(-0.2, 0.2, 0.006, 0.014, -0.4 + 0.2 * k - 0.006, -0.4 + 0.2 * k + 0.006, WOOD, vis=(1,)))
    out.append(W(-w / 2, w / 2, 0.0, t, -L / 2, L / 2, pap, vis=(2,)))
    return wear_all(out, wear)


def fallen_leaf(kind):
    P = LPart("fallen_leaf", budget="small", mass=4.0, anchor="floor", flat=True)
    if kind == "shoji":
        P.adds(xfs(leaf("shoji"), ry=8.0))
    elif kind == "fusuma":
        P.adds(xfs(leaf("fusuma"), ry=-6.0))
    elif kind == "shoji_broken":                        # snapped across: two halves at an angle, one half propped
        half = leaf("shoji", broken=True, wear="_w2")
        a = [q for q in half if max(v[2] for v in q.verts) <= 0.05]
        b = [q for q in half if max(v[2] for v in q.verts) > 0.05 and 2 not in q.vis]
        P.adds(xfs(a, ry=10.0))
        P.adds(rest(xfs(b, rx=8.0, ry=-18.0, t=(0.15, 0.0, 0.10)), 0.0))
        P.add(W(-0.46, 0.46, 0.0, 0.06, -0.98, 0.98, PAPER, vis=(2,)))
    else:
        P.adds(xfs(leaf("fusuma", torn=True, wear="_w2"), ry=14.0))
    P.dim("w", 0.91, 0.91, tol=0.005)
    P.notes.append("a sliding leaf off its track, flat on the floor, paper torn: no Geometry, never a working door "
                   "(BUILD_LIST jp_f_fallen_leaf)")
    return P


PROPS = [
    {"id": "jp_f_katanakake", "cat": CAT, "ll": 45, "mount": "floor", "tiers": ["U"], "refs": [], "models": [
        M("jp_f_katanakake_stand", "stand", "intact", "Sword rack with a pair of swords", lambda: katanakake("stand")),
        M("jp_f_katanakake_wall", "wall", "intact", "Wall sword rack with a pair of swords", lambda: katanakake("wall"),
          mount="wall"),
        M("jp_f_katanakake_stand_empty", "stand", "empty", "Sword rack, the swords taken",
          lambda: katanakake("stand_empty")),
        M("jp_f_katanakake_wall_empty", "wall", "empty", "Wall sword rack, the swords taken",
          lambda: katanakake("wall_empty"), mount="wall"),
    ]},
    {"id": "jp_f_yoroibitsu", "cat": CAT, "ll": 46, "mount": "floor", "tiers": ["U"], "refs": [], "models": [
        M("jp_f_yoroibitsu", "lacquer", "intact", "Armour chest, lacquered, crested", lambda: yoroibitsu("closed")),
        M("jp_f_yoroibitsu_plain", "plain", "intact", "Armour chest, plain wood", lambda: yoroibitsu("plain")),
        M("jp_f_yoroibitsu_open", "lacquer", "open", "Armour chest thrown open, empty", lambda: yoroibitsu("open")),
    ]},
    {"id": "jp_f_yumi_rack", "cat": CAT, "ll": 47, "mount": "wall", "tiers": ["U", 2], "refs": [], "models": [
        M("jp_f_yumi_rack_wall", "wall", "intact", "Bows on wall hooks and a quiver", lambda: yumi_rack("wall")),
        M("jp_f_yumi_rack_stand", "stand", "intact", "Upright bow stand with bows and a quiver",
          lambda: yumi_rack("stand"), mount="floor"),
        M("jp_f_yumi_rack_wall_empty", "wall", "empty", "Bow hooks, one bow left, the string snapped",
          lambda: yumi_rack("wall_empty")),
    ]},
    {"id": "jp_f_tea", "cat": CAT, "ll": 48, "mount": "surface", "tiers": [3, "U"], "refs": [],
     "notes": ["no tetsubin, no kyusu (LIFE_LAYER_ERA 48)"], "models": [
        M("jp_f_tea_matcha", "matcha", "intact", "Tea set: bowl, caddy, whisk, scoop on a tray", lambda: tea("matcha")),
        M("jp_f_tea_dobin", "dobin", "intact", "Clay tea pot and two bowls on a tray", lambda: tea("dobin")),
        M("jp_f_tea_broken", "matcha", "broken", "Tea set: the bowl broken, the pot tipped", lambda: tea("broken"),
          mount="floor"),
    ]},
    {"id": "jp_f_manger", "cat": CAT, "ll": 49, "mount": "floor", "tiers": [1, 2], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_manger"], "models": [
        M("jp_f_manger_trough", "trough", "intact", "Manger (kaiba-oke) on legs, some fodder", lambda: manger("trough")),
        M("jp_f_manger_cutter", "cutter", "intact", "Fodder cutter and a straw bundle", lambda: manger("cutter")),
        M("jp_f_manger_straw", "straw", "intact", "Straw pile of the stable corner", lambda: manger("straw")),
        M("jp_f_manger_trough_empty", "trough", "empty", "Manger, empty, stained", lambda: manger("trough_empty")),
        M("jp_f_manger_straw_rotted", "straw", "rotted", "Straw pile, rotted dark and flattened",
          lambda: manger("straw_rotted")),
    ]},
    {"id": "jp_f_fallen_leaf", "cat": CAT, "ll": 50, "mount": "floor", "tiers": [2, 3], "refs": [],
     "notes": ["★ BUILD_LIST jp_f_fallen_leaf; the abandoned layer"], "models": [
        M("jp_f_fallen_leaf_shoji", "shoji", "fallen", "A shoji leaf fallen flat", lambda: fallen_leaf("shoji")),
        M("jp_f_fallen_leaf_fusuma", "fusuma", "fallen", "A fusuma leaf fallen flat", lambda: fallen_leaf("fusuma")),
        M("jp_f_fallen_leaf_shoji_broken", "shoji", "broken", "A shoji leaf snapped, paper torn",
          lambda: fallen_leaf("shoji_broken")),
        M("jp_f_fallen_leaf_fusuma_torn", "fusuma", "torn", "A fusuma leaf, the paper torn open",
          lambda: fallen_leaf("fusuma_torn")),
    ]},
]
