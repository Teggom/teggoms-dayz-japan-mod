"""Street (BUILD_LIST order of work, step 4): gutter kit, shop-front kit, lanterns and sign lamps, nobori, stall family,
notice board (kosatsu). Readable text = B1's atlases (jp_m_decal_sumi_text: Yuji Syuku kanji, Yuji Hentaigana Akebono
kana). Cloth and paper ship torn and faded (dead-world rule); no lantern is emissive.

Shop-front dressing is made to be placed as PROXIES on shop buildings (G1 A3 answer 8): anchor 'wall' (the shop front
plane is z = 0, the piece hangs in front, +z = street), y = 0 = the floor / ground at the wall foot, door head (lintel)
assumed at 2.00 m (PLAYBOOK D2); eave-hung pieces at the heights recorded in the sidecar ('hang_y')."""
import math
import random

import skit
from skit import (core, box, prism, lathe, xf, xfs, flat_poly, W, col, col_solid, cyl_col, SPart, pole, beam, rope_path,
                  sag, grid_sheet, text_on, decal, moss_top, leaves, litter, add_all, ground, hull3, WOOD, DARK, BAMBOO,
                  IRON, CUT, FIELD, RIVER, CARVED, ROOFB, MUSHIRO, ROPE, PAPER, CHOCHIN, NOREN, KINARI, REED, SUMI, BENGARA,
                  LEAF)
from props_wood import M, basket
from props_stone import gable_roof

X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
LINTEL = 2.00
SOOT = "wood_sooted"


# ================================================================================================ gutter
GW, GD, LT = 0.30, 0.28, 0.18        # omote-dobu inside width / depth, lining thickness


def lining_run(x0, x1, wear=None, seed=1, tipped=False, vis=(1,)):
    """Dressed stone blocks both sides of a channel along x (tops flush with grade y = 0), 0.45-0.65 m stones."""
    rr = random.Random(seed)
    out = []
    for sz in (-1, 1):
        x = x0
        k = 0
        while x < x1 - 0.02:
            L = min(rr.uniform(0.45, 0.65), x1 - x)
            zin = sz * GW / 2
            zout = sz * (GW / 2 + LT)
            s = box(x + 0.004, x + L - 0.004, -GD - 0.06, rr.uniform(-0.012, 0.0), min(zin, zout), max(zin, zout), CUT,
                    vis=vis)
            if tipped and sz > 0 and k == 1:
                s = xf(s, rx=-38.0, pivot=(0.0, -GD, zin), t=(0.0, -0.04, 0.0))
            if wear:
                s.wear = wear
            out.append(s)
            x += L
            k += 1
    return out


def bed(x0, x1, y, wear="_w1", w=GW):
    return flat_poly([(x0, -w / 2), (x1, -w / 2), (x1, w / 2), (x0, w / 2)][::-1], y, LEAF, vis=(1, 2), wear=wear)


def gutter(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    flat = kind not in ("slab", "board_1ken")
    P = SPart("gutter", budget="small", res3=True, mass=150.0, bury=0.40, flat=flat)
    L = {"stone_half": 0.91, "slab": 0.91, "corner": 0.91, "outfall": 0.91}.get(kind, 1.82)
    x0, x1 = -L / 2, L / 2
    if kind in ("stone_1ken", "stone_half", "slab", "ab_silted", "outfall"):
        add_all(P, lining_run(x0, x1, wear=wear, seed=len(kind), tipped=ab))
        for sz in (-1, 1):
            P.add(W(x0, x1, -GD - 0.06, 0.0, sz * GW / 2 + (0 if sz > 0 else -LT), sz * GW / 2 + (LT if sz > 0 else 0),
                    CUT, vis=(2, 3)))
        P.add(bed(x0, x1, -GD + (0.14 if ab else 0.03), wear="_w2" if ab else "_w1"))
        if ab:
            P.add(litter(3, 0.0, 0.0, 0.6, sx=1.5, sz=0.6))
            P.solids[-1] = xf(P.solids[-1], t=(0.0, -GD + 0.14, 0.0))
        if kind == "slab":
            # a granite slab bridging the gutter at a door, resting on the linings
            s = W(-0.40, 0.40, -0.02, 0.10, -0.33, 0.33, CUT, vis=(1, 2, 3))
            P.add(s)
            P.add(col(-0.40, 0.40, -0.02, 0.10, -0.33, 0.33, CUT))
            P.road([(-0.40, 0.10, -0.33), (0.40, 0.10, -0.33), (0.40, 0.10, 0.33), (-0.40, 0.10, 0.33)], "stone_ext")
            P.dim("slab", 0.80, 0.80, tol=0.1)
        if kind == "outfall":
            # the channel ends at +x in a spout lip over a canal / ditch bank, a stone apron below
            P.add(W(x1 - 0.02, x1 + 0.25, -GD - 0.06, -GD + 0.02, -GW / 2 - 0.05, GW / 2 + 0.05, CUT, vis=(1, 2, 3)))
            P.add(W(x1 + 0.05, x1 + 0.75, -GD - 0.70, -GD - 0.52, -0.45, 0.45, FIELD, vis=(1, 2)))
            P.add(leaves(7, x1 + 0.4, 0.0, 0.3, -GD - 0.519, wear="_w2"))
            P.bury = 1.0
            P.dim("drop", 0.5, 0.52 - 0.06, tol=0.1)
    elif kind == "corner":
        # a 90-degree turn: outer lining on -z and +x, a corner block, the inner corner stone at (-,+)
        for s in lining_run(-L / 2, L / 2, wear=wear, seed=5):
            if s.bbox()[4] < 0:
                P.add(s)
        for s in lining_run(-L / 2, L / 2, wear=wear, seed=6):
            if s.bbox()[4] < 0:
                P.add(xf(s, ry=-90.0))
        P.add(W(-L / 2, -GW / 2, -GD - 0.06, 0.0, GW / 2, GW / 2 + LT, CUT, vis=(1,)))
        P.add(W(-GW / 2 - LT, -GW / 2, -GD - 0.06, 0.0, GW / 2, L / 2, CUT, vis=(1,)))
        P.add(W(-L / 2, L / 2, -GD - 0.06, 0.0, -GW / 2 - LT, -GW / 2, CUT, vis=(2, 3)))
        P.add(W(GW / 2, GW / 2 + LT, -GD - 0.06, 0.0, -GW / 2, L / 2, CUT, vis=(2, 3)))
        P.add(bed(-L / 2, GW / 2, -GD + 0.03))
        P.add(flat_poly([(-GW / 2, GW / 2), (GW / 2, GW / 2), (GW / 2, L / 2), (-GW / 2, L / 2)][::-1], -GD + 0.03, LEAF,
                        vis=(1, 2)))
    elif kind == "board_1ken":
        # back-alley dobu 0.20 x 0.20 with board sides, dobu-ita covers laid across (Geometry + Roadway on the boards)
        w, d = 0.20, 0.20
        for sz in (-1, 1):
            P.add(W(x0, x1, -d - 0.03, 0.0, sz * w / 2 - 0.02 * (sz < 0), sz * w / 2 + 0.02 * (sz > 0), WOOD, vis=(1, 2, 3)))
        P.add(bed(x0, x1, -d + 0.02, w=w))
        P.solids[-1].vis = {1}
        P.add(W(x0, x1, 0.0, 0.03, -0.14, 0.14, WOOD, vis=(3,)))
        rr = random.Random(4)
        for k in range(2):
            bx0 = x0 + k * 0.91 + 0.005
            b = W(bx0, bx0 + 0.90, 0.0, 0.03, -0.14, 0.14, WOOD, vis=(1, 2))
            b.uv = "grain"
            P.add(xf(b, ry=rr.uniform(-1.5, 1.5), pivot=(bx0 + 0.45, 0.0, 0.0)))
            P.add(col(bx0, bx0 + 0.90, 0.0, 0.03, -0.14, 0.14))
        P.road([(x0, 0.03, -0.14), (x1, 0.03, -0.14), (x1, 0.03, 0.14), (x0, 0.03, 0.14)], "boards_ext")
        P.bury = 0.25
        P.dim("alley_dobu_w", 0.20, w, tol=0.01)
        P.dim("dobu_ita", 0.91, 0.90, tol=0.02)
    else:   # earth_1ken: rural earth-banked gutter with a field-stone edge
        rr = random.Random(8)
        for sz in (-1, 1):
            x = x0
            while x < x1 - 0.05:
                d = rr.uniform(0.22, 0.32)
                P.add(core.stone(rr, x + d / 2, sz * 0.30, d, 0.16, 0.10, 0.05, FIELD, bury=0.08, n=5, vis=(1,)))
                x += d + 0.05
            P.add(W(x0, x1, -0.12, 0.05, sz * 0.22, sz * 0.38, FIELD, vis=(2, 3)) if sz > 0 else
                  W(x0, x1, -0.12, 0.05, -0.38, -0.22, FIELD, vis=(2, 3)))
        # the V earth bed (leaf litter over mud)
        for sz in (-1, 1):
            q = [(x0, 0.0, sz * 0.24), (x1, 0.0, sz * 0.24), (x1, -0.20, sz * 0.05), (x0, -0.20, sz * 0.05)]
            P.add(core.sheet([q], LEAF, core.norm((0.0, 1.0, -sz * 0.9)), vis=(1, 2)))
        P.add(bed(x0, x1, -0.20, w=0.10))
        P.bury = 0.22
    if kind in ("stone_1ken", "stone_half", "ab_silted", "slab", "outfall", "corner"):
        P.dim("channel_w", 0.30, GW, tol=0.01)
        P.dim("channel_d", 0.28, GD, tol=0.02)
    P.dim("segment", L, L, tol=0.005)
    P.extra["terrain"] = "sits in a terrain ditch (tops flush with grade); the ditch is the terrain / placement agent's cut"
    return P


# ================================================================================================ shop front (proxies)
def noren_panel_uv(i, n_pan, L):
    """uv for panel i: the middle panel carries the resist-dyed shop mark (one 0.5 m cell), the others plain cloth
    (the 6 cm strip between marks); below 0.5 m the cloth continues plain."""
    def uv(u, v):
        d = v * L
        vv = d if d <= 0.5 else 0.46 + 0.03 * (d - 0.5) / max(L - 0.5, 0.01)
        if i == n_pan // 2:
            uu = 0.08 + 0.34 * u
        else:
            uu = 0.47 + 0.06 * u
        return (uu, vv)
    return uv


def noren(L, wear="_w1", torn=False, top=LINTEL - 0.02, zc=0.10, missing=()):
    out = []
    pw = 0.34
    for i in range(3):
        if i in missing:
            continue
        xa = -0.51 + i * pw + 0.004
        rr = random.Random(i + int(L * 10))
        Lp = L * (rr.uniform(0.55, 0.8) if torn and i == 2 else 1.0)

        def f(u, v, xa=xa, rr=rr, Lp=Lp):
            x = xa + (pw - 0.008) * u
            y = top - Lp * v
            z = zc + 0.02 * math.sin(math.pi * u) * v + 0.03 * v * (i - 1) * 0.3
            return (x, y, z)
        out.append(grid_sheet(f, 1, 3, NOREN, vis=(1,), wear=wear, uv=noren_panel_uv(i, 3, Lp)))
    out.append(pole((-0.62, top + 0.02, zc), (0.62, top + 0.02, zc), 0.015, BAMBOO, n=5, vis=(1, 2)))
    out.append(W(-0.51, 0.51, top - L, top, zc - 0.003, zc + 0.003, NOREN, vis=(2,)))
    out[-1].wear = wear
    return out


def shopfront(kind):
    ab = kind.startswith("ab")
    P = SPart("shopfront", budget="small", mass=5.0, anchor="wall", wall_gap=0.0, flat=True)
    P.hung = True
    hang = None
    if kind in ("noren_long", "noren_half", "ab_noren_torn"):
        L = {"noren_long": 1.60, "noren_half": 0.56, "ab_noren_torn": 1.13}[kind]
        add_all(P, noren(L, wear="_w2" if ab else "_w1", torn=ab, missing=(0,) if ab else ()))
        # two hooks on the lintel
        for sx in (-1, 1):
            P.add(W(sx * 0.55 - 0.01, sx * 0.55 + 0.01, LINTEL - 0.02, LINTEL + 0.02, 0.0, 0.11, IRON, vis=(1,)))
        if ab:
            m = grid_sheet(lambda u, v: (-0.5 + 0.34 * u, 0.012 + 0.05 * math.sin(3 * u) * v, 0.20 + 0.35 * v), 2, 2, NOREN,
                           vis=(1,), wear="_w2")
            P.add(m)
            P.hung = False
        P.dim("noren_L", L, L, tol=0.01)
        P.dim("noren_W", 1.02, 1.02, tol=0.01)
        hang = LINTEL
    elif kind == "mizuhiki":
        W_, D_ = 1.82, 0.35
        top = LINTEL + 0.35
        P.add(grid_sheet(lambda u, v: (-W_ / 2 + W_ * u, top - D_ * v, 0.12 + 0.015 * math.sin(6 * math.pi * u)), 6, 1,
                         KINARI, vis=(1,), wear="_w1"))
        P.add(pole((-W_ / 2 - 0.05, top + 0.015, 0.12), (W_ / 2 + 0.05, top + 0.015, 0.12), 0.015, BAMBOO, n=5,
                   vis=(1, 2)))
        P.add(W(-W_ / 2, W_ / 2, top - D_, top, 0.118, 0.122, KINARI, vis=(2,)))
        P.dim("mizuhiki_d", 0.35, D_, tol=0.05)
        P.dim("width", 1.82, W_, tol=0.01)
        hang = top
    elif kind in ("sudare_up", "sudare_down"):
        W_ = 0.91
        top = LINTEL + 0.60           # an upstairs / eave sudare
        if kind == "sudare_up":
            ro = lathe([(0.055, -W_ / 2), (0.055, W_ / 2)], 8, REED, vis=(1, 2), smooth=True)
            P.add(xf(ro, rz=90.0, t=(0.0, top - 0.25, 0.08)))
            for sx in (-1, 1):
                add_all(P, rope_path([(sx * 0.3, top, 0.02), (sx * 0.3, top - 0.19, 0.14), (sx * 0.3, top - 0.31, 0.08),
                                      (sx * 0.3, top - 0.19, 0.02)], 0.005))
            P.dim("rolled_d", 0.11, 0.11, tol=0.01)
        else:
            Lh = 1.20
            P.add(grid_sheet(lambda u, v: (-W_ / 2 + W_ * u, top - Lh * v, 0.06 + 0.05 * v * v + 0.01 * math.sin(4 * u)),
                             2, 3, REED, vis=(1,), wear="_w2"))
            P.add(W(-W_ / 2, W_ / 2, top - Lh, top, 0.06, 0.065, REED, vis=(2,)))
            P.add(pole((-W_ / 2, top - Lh - 0.01, 0.11), (W_ / 2, top - Lh + 0.02, 0.11), 0.01, BAMBOO, n=4, vis=(1,)))
            P.dim("sudare_L", 1.20, Lh, tol=0.01)
        P.add(pole((-W_ / 2 - 0.03, top, 0.03), (W_ / 2 + 0.03, top, 0.03), 0.012, BAMBOO, n=4, vis=(1, 2)))
        P.dim("width", 0.91, W_, tol=0.01)
        hang = top
    elif kind in ("kanban_hang", "ab_kanban_askew"):
        # hanging signboard (kake-kanban) 0.30 x 1.20 x 0.04 from two cords under the eave, text down the board
        top = 2.75
        bw, bh = 0.30, 1.20
        br = [W(-0.03, 0.03, top, top + 0.06, 0.0, 0.40, WOOD, vis=(1, 2))]
        board = [W(-bw / 2, bw / 2, 0.0, bh, -0.02, 0.02, WOOD, vis=(1, 2)),
                 text_on((0.0, bh / 2, 0.02), X, Y, 1.0, SUMI, "kanban_okashidokoro", wear="_w1" if not ab else "_w2")]
        if not ab:
            board = xfs(board, t=(0.0, top - 0.25 - bh, 0.30))
            add_all(P, board)
            for sx in (-1, 1):
                add_all(P, rope_path([(0.0, top, 0.30), (sx * 0.12, top - 0.25, 0.30)], 0.005))
        else:
            # one cord rotted: the board hangs from a corner, swung round
            board = xfs(board, rz=-24.0, pivot=(-bw / 2, bh, 0.0))
            board = xfs(board, ry=12.0, t=(0.0, top - 0.30 - bh, 0.30))
            add_all(P, board)
            add_all(P, rope_path([(0.0, top, 0.30), (-0.15, top - 0.30, 0.30)], 0.005, wear="_w2"))
            add_all(P, rope_path([(0.0, top, 0.30), (0.03, top - 0.12, 0.31)], 0.005, wear="_w2"))
        add_all(P, br)
        P.dim("board", 1.20, bh, tol=0.01)
        hang = top
    elif kind == "kanban_stand":
        # standing signboard (oki-kanban) 0.45 x 1.20 on feet, text both faces; stands on the ground in front
        P.flat = False
        P.need = ("geo", "view", "fire")
        P.hung = False
        P.wall_gap = 0.25
        P.mass = 20.0
        z = 0.45
        P.add(W(-0.225, 0.225, 0.12, 1.20, z - 0.025, z + 0.025, WOOD, vis=(1, 2)))
        P.add(W(-0.25, 0.25, 1.18, 1.25, z - 0.05, z + 0.05, DARK, vis=(1, 2)))
        for sx in (-1, 1):
            P.add(W(sx * 0.2 - 0.03, sx * 0.2 + 0.03, 0.0, 0.14, z - 0.20, z + 0.20, DARK, vis=(1, 2)))
        P.add(text_on((0.0, 0.66, z + 0.025), X, Y, 0.95, SUMI, "kanban_osobakiri", wear="_w1"))
        P.add(text_on((0.0, 0.66, z - 0.025), (-1.0, 0.0, 0.0), Y, 0.95, SUMI, "kanban_osobakiri", wear="_w1"))
        P.add(col(-0.25, 0.25, 0.0, 1.25, z - 0.2, z + 0.2))
        P.dim("stand_h", 1.25, 1.25, tol=0.06)
        P.dim("stand_w", 0.45, 0.45, tol=0.01)
    elif kind.startswith("shape_"):
        shp = kind[6:]
        top = 2.55
        out = [beam((0.0, top, 0.0), (0.0, top, 0.55), 0.05, 0.05, WOOD, vis=(1, 2))]
        out += rope_path([(0.0, top, 0.48), (0.0, top - 0.15, 0.48)], 0.006)
        cy = top - 0.15
        size = {"brush": 1.2, "geta": 0.6, "tabi": 0.7, "gourd": 0.6, "umbrella": 1.0, "fan": 0.8}[shp]
        zz = 0.48
        if shp == "brush":
            out.append(pole((0.0, cy, zz), (0.0, cy - 0.80, zz), 0.05, BAMBOO, n=8, vis=(1, 2)))
            out.append(lathe([(0.06, 0.0), (0.09, -0.15), (0.06, -0.33), (0.0, -0.40)], 8, SOOT, vis=(1, 2)))
            out[-1] = xf(out[-1], t=(0.0, cy - 0.80, zz))
        elif shp == "geta":
            g = [W(-0.11, 0.11, 0.0, 0.035, -0.30, 0.30, WOOD, vis=(1, 2)),
                 W(-0.10, 0.10, -0.12, 0.0, 0.12, 0.17, WOOD, vis=(1, 2)),
                 W(-0.10, 0.10, -0.12, 0.0, -0.20, -0.15, WOOD, vis=(1, 2))]
            g += rope_path([(-0.08, 0.035, 0.05), (0.0, 0.07, -0.18), (0.08, 0.035, 0.05)], 0.008, NOREN)
            out += xfs(g, rx=-90.0, t=(0.0, cy - 0.30, zz))
        elif shp == "tabi":
            pts = [(-0.12, 0.0), (0.12, 0.0), (0.14, 0.12), (0.10, 0.62), (-0.10, 0.62), (-0.14, 0.14)]
            out.append(xf(prism(pts, "z", -0.03, 0.03, "textile_cotton_plain", vis=(1, 2)), t=(0.0, cy - 0.70, zz)))
        elif shp == "gourd":
            out.append(xf(lathe([(0.0, 0.0), (0.16, 0.12), (0.18, 0.22), (0.10, 0.34), (0.08, 0.38), (0.12, 0.46),
                                 (0.10, 0.54), (0.02, 0.6)], 8, BENGARA, vis=(1, 2)), t=(0.0, cy - 0.6, zz)))
        elif shp == "umbrella":
            out.append(xf(lathe([(0.0, 0.0), (0.02, 0.05), (0.09, 0.70), (0.06, 0.85), (0.0, 0.87)], 8, PAPER, vis=(1, 2),
                                wear="_w2"), t=(0.0, cy - 1.0, zz)))
            out.append(pole((0.0, cy - 1.0, zz), (0.0, cy, zz), 0.012, BAMBOO, n=4, vis=(1,)))
        else:   # fan: an open folding fan board
            pts = [(0.0, 0.0)] + [(0.42 * math.cos(math.radians(a)), 0.42 * math.sin(math.radians(a)))
                                  for a in range(20, 161, 20)]
            out.append(xf(prism(pts, "z", -0.02, 0.02, PAPER, vis=(1, 2)), t=(0.0, cy - 0.45, zz)))
            out[-1].wear = "_w2"
            out.append(xf(W(-0.015, 0.015, 0.0, 0.14, -0.022, 0.022, WOOD, vis=(1,)), t=(0.0, cy - 0.47, zz)))
        add_all(P, out)
        P.dim("shape_size", size, size, tol=0.25)
        hang = top
        P.extra["trade"] = {"brush": "brush / writing shop", "geta": "geta (clog) maker", "tabi": "tabi (sock) maker",
                            "gourd": "medicine seller", "umbrella": "umbrella maker", "fan": "fan maker"}[shp]
    else:   # ab_fallen: the noren pole dropped, the noren in a heap on the threshold
        P.hung = False
        P.wall_gap = 0.10
        P.add(pole((-0.62, 0.02, 0.12), (0.60, 0.02, 0.28), 0.015, BAMBOO, n=5, vis=(1, 2), wear="_w2"))
        for i in range(3):
            P.add(grid_sheet(lambda u, v, i=i: (-0.5 + 0.33 * i + 0.34 * u, 0.012 + 0.07 * math.sin(math.pi * u) *
                                                math.sin(math.pi * v) * (1 + i % 2), 0.15 + 0.5 * v + 0.05 * i), 2, 2,
                             NOREN, vis=(1,), wear="_w2"))
        P.add(W(-0.5, 0.5, 0.0, 0.03, 0.15, 0.70, NOREN, vis=(2,)))
        P.solids[-1].wear = "_w2"
        P.add(litter(5, 0.0, 0.62, 0.4, sx=1.6, sz=0.8))
        P.dim("noren_W", 1.02, 1.02, tol=0.01)
    if hang:
        P.extra["hang_y"] = hang
    P.extra["proxy"] = "shop-front proxy: wall plane z = 0, y = 0 at the wall foot, lintel 2.00 (move y to the real lintel)"
    return P


# ================================================================================================ lanterns
def chochin_prof(R, H, n=7):
    return [(R * (0.55 + 0.45 * math.sin(math.pi * k / (n - 1))), H * k / (n - 1)) for k in range(n)]


def chochin(R, H, cellname, wear="_w1", text_wear="_w1", vis=(1,), crushed=False):
    """Hanging paper lantern: oblong lathe (12 sides), wooden top and bottom rings, text wrapped round the front."""
    prof = chochin_prof(R, H)
    body = lathe(prof, 12, CHOCHIN, vis=vis, wear=wear)
    out = [body]
    for y in (0.0, H):
        out.append(lathe([(R * 0.58, y - 0.03), (R * 0.58, y + 0.03)], 12, DARK, vis=vis, smooth=True))
    out.append(lathe([(0.0, -0.03), (R * 0.58, -0.03)], 8, DARK, vis=vis))
    out.append(lathe([(R, 0.0), (R, H), (0.0, H)], 6, CHOCHIN, vis=(2,), wear=wear, smooth=False))
    # wrapped text: a curved strip following the paper, +-40 degrees round +z
    cw, ch = skit.cell_size(SUMI, cellname)
    th = H * 0.62
    span = th * cw / ch
    y0 = H * 0.19
    u0, v0, u1, v1 = skit.cell(SUMI, cellname)

    def rad(y):
        t = y / H
        return R * (0.55 + 0.45 * math.sin(math.pi * t)) + 0.004

    def f(u, v):
        y = y0 + th * (1 - v)
        r = rad(y)
        a = (u - 0.5) * span / max(r, 0.05)
        return (r * math.sin(a), y, r * math.cos(a))
    tx = grid_sheet(f, 3, 3, SUMI, vis=vis, two_sided=False, wear=text_wear,
                    uv=lambda u, v: (u0 + (u1 - u0) * u, v0 + (v1 - v0) * v))
    tx.cell = "%s:%s" % (SUMI, cellname)
    out.append(tx)
    return out


def bracket(top, reach=0.45, vis=(1, 2)):
    return [beam((0.0, top, 0.0), (0.0, top, reach), 0.05, 0.06, DARK, vis=vis),
            beam((0.0, top - 0.30, 0.0), (0.0, top - 0.02, reach * 0.7), 0.03, 0.03, DARK, vis=(1,))]


def box_lamp(w, d, h, cellname, wear="_w2", text_wear="_w1", panels=True, vis=(1,)):
    """Framed box lamp (andon): corner posts, top and bottom frames, paper panels, text on the front panel."""
    out = []
    for sx in (-1, 1):
        for sz in (-1, 1):
            out.append(W(sx * w / 2 - 0.02 * (sx > 0), sx * w / 2 + 0.02 * (sx < 0), 0.0, h, sz * d / 2 - 0.02 * (sz > 0),
                         sz * d / 2 + 0.02 * (sz < 0), DARK, vis=vis))
    for y in (0.0, h - 0.03):
        out.append(W(-w / 2, w / 2, y, y + 0.03, -d / 2, d / 2, DARK, vis=vis))
    if panels:
        for sz in (-1, 1):
            q = [(-w / 2 + 0.02, 0.03, sz * (d / 2 - 0.01)), (w / 2 - 0.02, 0.03, sz * (d / 2 - 0.01)),
                 (w / 2 - 0.02, h - 0.03, sz * (d / 2 - 0.01)), (-w / 2 + 0.02, h - 0.03, sz * (d / 2 - 0.01))]
            out.append(core.sheet([q, q[::-1]], CHOCHIN, [(0.0, 0.0, float(sz)), (0.0, 0.0, -float(sz))], vis=vis))
            out[-1].wear = wear
        for sx in (-1, 1):
            q = [(sx * (w / 2 - 0.01), 0.03, -d / 2 + 0.02), (sx * (w / 2 - 0.01), 0.03, d / 2 - 0.02),
                 (sx * (w / 2 - 0.01), h - 0.03, d / 2 - 0.02), (sx * (w / 2 - 0.01), h - 0.03, -d / 2 + 0.02)]
            out.append(core.sheet([q, q[::-1]], CHOCHIN, [(float(sx), 0.0, 0.0), (-float(sx), 0.0, 0.0)], vis=vis))
            out[-1].wear = wear
        out.append(text_on((0.0, h / 2, d / 2 - 0.01), X, Y, (h - 0.1) * 0.85, SUMI, cellname, wear=text_wear, off=0.004))
    out.append(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, CHOCHIN, vis=(2,)))
    out[-1].wear = wear
    return out


def lantern_sign(kind):
    ab = kind.startswith("ab")
    P = SPart("lantern_sign", budget="small", mass=4.0, anchor="wall", wall_gap=0.0, flat=True)
    P.hung = True
    if kind in ("chochin_shop", "chochin_inn", "chochin_gate", "ab_torn"):
        R, H, cellname = {"chochin_shop": (0.15, 0.55, "kanban_miki"), "chochin_inn": (0.225, 0.80, "kanban_oyado"),
                          "chochin_gate": (0.225, 0.80, "chochin_honcho"), "ab_torn": (0.15, 0.55, "kanban_miki")}[kind]
        top = 2.20
        add_all(P, bracket(top))
        ch = chochin(R, H, cellname, wear="_w2" if ab else "_w1", text_wear="_w2" if ab else "_w1")
        add_all(P, xfs(ch, t=(0.0, top - 0.12 - H, 0.40)))
        P.add(pole((0.0, top - 0.03, 0.40), (0.0, top - 0.12, 0.40), 0.006, IRON, n=3, vis=(1,)))
        P.dim("chochin_d", 2 * R, 2 * R, tol=0.005)
        P.dim("chochin_h", H, H, tol=0.005)
        P.extra["hang_y"] = top
        P.extra["paper"] = "never emissive; _w1 = yellowed and water-stained (the list's '_ab_torn default' is _ab_torn)"
    elif kind == "kake":
        top = 2.05
        add_all(P, bracket(top, reach=0.30))
        lamp = box_lamp(0.30, 0.15, 0.45, "kanban_oyasumidokoro")
        add_all(P, xfs(lamp, t=(0.0, top - 0.06 - 0.45, 0.25)))
        P.dim("kake_box_h", 0.45, 0.45, tol=0.01)
        P.extra["hang_y"] = top
    elif kind in ("oki", "ab_fallen"):
        P.flat = False
        P.need = ("geo", "view", "fire")
        P.hung = False
        P.wall_gap = 0.22 if kind == "oki" else 0.10
        P.mass = 8.0
        lamp = box_lamp(0.35, 0.35, 0.62, "kanban_oyado", wear="_w2")
        legs = []
        for sx in (-1, 1):
            for sz in (-1, 1):
                legs.append(W(sx * 0.15 - 0.02, sx * 0.15 + 0.02, 0.0, 0.33, sz * 0.15 - 0.02, sz * 0.15 + 0.02, DARK,
                              vis=(1, 2)))
        ss = xfs(lamp, t=(0.0, 0.33, 0.0)) + legs
        cols = [col(-0.18, 0.18, 0.0, 0.95, -0.18, 0.18, DARK)]
        if kind == "oki":
            ss = xfs(ss + cols, t=(0.0, 0.0, 0.40))
        else:
            # tipped over forward, one paper panel gone; a crushed hanging lantern beside it
            ss = xfs(ss + cols, rx=88.0, t=(0.0, 0.18, 0.12))
            ch = chochin(0.15, 0.55, "kanban_miki", wear="_w2", text_wear="_w2")
            ch = [skit.scale_z(s, 1.0) if False else s for s in ch]
            ch = xfs(ch, rz=80.0, t=(0.55, 0.10, 0.75))
            for s in ch:
                s.verts = [(v[0], v[1] * 0.55 + 0.02, v[2]) for v in s.verts]
            ss += ch
            ss.append(litter(3, 0.2, 0.7, 0.5, sx=1.4))
        cols = [s for s in ss if s.geo]
        ss = [s for s in ss if not s.geo]
        add_all(P, ss + cols)
        ground(P)
        P.dim("oki_h", 0.95, 0.95, tol=0.06)
    else:   # tsuji: crossroads lamp on a 2.0 m post with a small roof (free-standing)
        P.flat = False
        P.need = ("geo", "view", "fire")
        P.hung = False
        P.anchor = "floor"
        P.budget = "small"
        P.mass = 40.0
        P.bury = 0.32
        P.add(W(-0.07, 0.07, -0.30, 2.0, -0.07, 0.07, DARK, vis=(1, 2)))
        P.add(col(-0.07, 0.07, 0.0, 2.0, -0.07, 0.07, DARK))
        add_all(P, xfs(box_lamp(0.40, 0.40, 0.60, "chochin_honcho"), t=(0.0, 2.0, 0.0)))
        rs, rc = gable_roof(0.62, 0.62, 2.62, 2.85, vis=(1, 2), battens=False)
        add_all(P, rs)
        P.add(col(-0.2, 0.2, 2.0, 2.6, -0.2, 0.2, DARK))
        P.add(core.stone(random.Random(2), 0.0, 0.0, 0.40, 0.40, 0.10, 0.06, FIELD, bury=0.06, n=6, vis=(1,)))
        P.dim("post_h", 2.0, 2.0, tol=0.01)
        P.dim("tsuji_box", 0.60, 0.60, tol=0.01)
    return P


# ================================================================================================ nobori
def banner(h=3.4, w=0.45, x=0.0, top=5.4, wear="_w1", cellname="nobori_hono_inari", shred=1.0, mat=KINARI, lean=0.0,
           text=True):
    """A banner hanging from the crossbar at `top`, tied along the pole (x), cloth two-sided, text stretched up it."""
    hh = h * shred

    def f(u, v):
        y = top - hh * v
        return (x + 0.03 + w * u, y, 0.02 * math.sin(math.pi * u) + 0.03 * v * v)
    out = [grid_sheet(f, 2, 4, mat, vis=(1,), wear=wear)]
    out.append(W(x + 0.03, x + 0.03 + w, top - hh, top, -0.003, 0.003, mat, vis=(2,)))
    out[-1].wear = wear
    if text:
        th = min(hh - 0.3, h * 0.8)
        crop = (0.0, 0.0, 1.0, min(1.0, th / (h * 0.8)))
        out.append(decal((x + 0.03 + w * 0.12, top - 0.15, 0.028), (x + 0.03 + w * 0.88, top - 0.15, 0.028),
                         (x + 0.03 + w * 0.88, top - 0.15 - th, 0.028 + 0.02), (x + 0.03 + w * 0.12, top - 0.15 - th, 0.028 + 0.02),
                         SUMI, cellname, wear=wear, crop=crop))
    return out


def socket_pair(x=0.0, vis=(1, 2, 3)):
    """nobori-tate ishi: two carved stone posts either side of the pole, 0.5 high."""
    out, cols = [], []
    for sz in (-1, 1):
        out.append(W(x - 0.09, x + 0.09, -0.15, 0.50, sz * 0.05 + (0 if sz > 0 else -0.16), sz * 0.05 + (0.16 if sz > 0 else 0),
                     CARVED, vis=vis))
        cols.append(col(x - 0.09, x + 0.09, 0.0, 0.50, sz * 0.05 + (0 if sz > 0 else -0.16),
                        sz * 0.05 + (0.16 if sz > 0 else 0), CARVED))
    out.append(moss_top(x * 10 + 3, x, 0.13, 0.05, 0.50))
    return out, cols


def nobori(kind):
    ab = kind.startswith("ab")
    P = SPart("nobori", budget="small", mass=40.0, bury=0.16)
    PH = 6.0
    xs = (-0.9, 0.9) if kind == "shrine" else (0.0,)
    for x in xs:
        ss, cs = socket_pair(x)
        add_all(P, ss + cs)
        if kind == "socket_stones":
            continue
        if kind == "ab_down":
            p0, p1 = (x, 0.06, 0.25), (x + 0.6, 0.05, 6.1)
            P.add(pole(p0, p1, 0.035, BAMBOO, n=6, vis=(1, 2), r1=0.022, wear="_w2"))
            P.add(pole((x + 0.52, 0.05, 5.3), (x + 1.0, 0.05, 5.5), 0.012, BAMBOO, n=4, vis=(1,), wear="_w2"))
            bn = grid_sheet(lambda u, v: (x + 0.1 + 0.4 * u + 0.1 * v, 0.012 + 0.02 * math.sin(5 * v), 3.0 + 2.2 * v),
                            2, 4, KINARI, vis=(1,), wear="_w2")
            P.add(bn)
            P.add(col_solid(beam(p0, p1, 0.07, 0.07, BAMBOO)))
            continue
        lean = 7.0 if ab else 0.0
        parts = [pole((x, -0.10, 0.0), (x, PH, 0.0), 0.035, BAMBOO, n=6, vis=(1, 2, 3), r1=0.022, wear="_w2" if ab else None),
                 pole((x, PH - 0.55, 0.0), (x + 0.55, PH - 0.55, 0.0), 0.012, BAMBOO, n=4, vis=(1, 2))]
        cell = "nobori_hono_inari" if kind != "shop" else "kanban_osobakiri"
        mat = KINARI      # sumi text reads only on undyed cloth (an indigo shop banner would need resist-dyed text)
        parts += banner(h=3.4, x=x, top=PH - 0.55, wear="_w2" if ab else "_w1", cellname=cell,
                        shred=0.45 if ab else 1.0, mat=mat, text=not ab or True)
        parts += rope_path([(x, 3.2, 0.0), (x + 0.03, 3.2, 0.02)], 0.01)
        c = col(x - 0.035, x + 0.035, 0.0, PH, -0.035, 0.035, BAMBOO)
        if lean:
            parts = xfs(parts + [c], rz=-lean, pivot=(x, 0.4, 0.0))
            c = parts[-1]
            parts = parts[:-1]
        add_all(P, parts)
        P.add(c)
    if kind == "ab_down":
        P.add(litter(4, 0.3, 3.0, 1.0, sx=0.6, sz=2.0))
    for s in P.solids:
        s.vis.discard(3)
    P.dim("pole", 6.0, PH, tol=1.0)
    P.dim("banner", 3.4, 3.4, tol=1.1)
    P.extra["text"] = "banner text stretched up the cloth (B1's note on nobori_hono_inari)"
    return P


# ================================================================================================ stall family
def reed_screen(x0, x1, y0, y1, z, wear="_w1", sag_=0.0, vis=(1,)):
    return grid_sheet(lambda u, v: (x0 + (x1 - x0) * u, y1 - (y1 - y0) * v, z + sag_ * math.sin(math.pi * u) * v), 2, 2,
                      REED, vis=vis, wear=wear)


def reed_stall(dx=0.0, state="std", wear=None, share_left=False):
    """1 ken x 1 ken bamboo pole frame, reed screens back and sides, a board counter at 0.8 in front, a mat roof
    sloping to the back (2.1 front, 1.9 back)."""
    S = 1.82
    out, cols, road = [], [], []
    posts = [(-S / 2, -S / 2, 1.90), (S / 2, -S / 2, 1.90), (-S / 2, S / 2, 2.10), (S / 2, S / 2, 2.10)]
    for i, (x, z, h) in enumerate(posts):
        if share_left and x < 0:
            continue
        top = h
        if state == "collapsed" and i == 3:
            out.append(pole((dx + x, -0.05, z), (dx + x, 1.0, z), 0.035, BAMBOO, n=5, vis=(1, 2), wear="_w2"))
            out.append(pole((dx + x - 0.1, 0.03, z + 0.1), (dx + x - 0.9, 0.03, z + 0.5), 0.03, BAMBOO, n=5, vis=(1,),
                            wear="_w2"))
            cols.append(col(dx + x - 0.035, dx + x + 0.035, 0.0, 1.0, z - 0.035, z + 0.035, BAMBOO))
            continue
        out.append(pole((dx + x, -0.05, z), (dx + x, top, z), 0.035, BAMBOO, n=5, vis=(1, 2, 3), wear=wear))
        cols.append(col(dx + x - 0.035, dx + x + 0.035, 0.0, top, z - 0.035, z + 0.035, BAMBOO))
    # rails
    for (a, b) in ((0, 1), (2, 3), (0, 2), (1, 3)):
        if state == "collapsed" and 3 in (a, b):
            continue
        pa, pb = posts[a], posts[b]
        out.append(pole((dx + pa[0], pa[2] - 0.05, pa[1]), (dx + pb[0], pb[2] - 0.05, pb[1]), 0.02, BAMBOO, n=4,
                        vis=(1, 2), wear=wear))
    if state == "std":
        out.append(reed_screen(dx - S / 2, dx + S / 2, 0.05, 1.85, -S / 2 + 0.03))
        for sx in (-1, 1):
            if share_left and sx < 0:
                continue
            s = reed_screen(-S / 2, S / 2, 0.05, 1.85, 0.0)
            out.append(xf(s, ry=90.0, t=(dx + sx * (S / 2 - 0.03), 0.0, 0.0)))
        # roof mat
        out.append(grid_sheet(lambda u, v: (dx - S / 2 - 0.1 + (S + 0.2) * u, 2.12 - 0.24 * v - 0.05 * math.sin(math.pi * u) *
                                            math.sin(math.pi * v), S / 2 + 0.15 - (S + 0.3) * v), 3, 2, MUSHIRO, vis=(1,),
                              wear="_w2"))
        out.append(W(dx - S / 2, dx + S / 2, 1.88, 1.9, -S / 2, S / 2, MUSHIRO, vis=(2, 3)))
        out.append(W(dx - S / 2, dx + S / 2, 0.0, 1.8, -S / 2, -S / 2 + 0.02, REED, vis=(2,)))
    elif state == "collapsed":
        # the mat fallen in, sagging to the counter; screens flattened on the ground
        out.append(grid_sheet(lambda u, v: (dx - S / 2 + S * u, 1.9 - 1.0 * v * (0.3 + u) - 0.2 * math.sin(math.pi * v),
                                            S / 2 - S * v), 3, 2, MUSHIRO, vis=(1,), wear="_w2"))
        out.append(reed_screen(dx - S / 2, dx + S / 2, 0.0, 1.8, 0.0, wear="_w2"))
        out[-1] = xf(out[-1], rx=-88.0, t=(0.0, 0.03, -S / 2 - 1.75))
        out.append(W(dx - S / 2, dx + S / 2, 0.8, 1.9, -S / 2, S / 2, MUSHIRO, vis=(2,)))
    # counter: a board on two posts at 0.8 in front
    cz = S / 2 + 0.05
    if state != "frame":
        out.append(W(dx - S / 2 + 0.1, dx + S / 2 - 0.1, 0.77, 0.80, cz - 0.20, cz + 0.20, WOOD, vis=(1, 2, 3)))
        for sx in (-1, 1):
            out.append(W(dx + sx * 0.7 - 0.03, dx + sx * 0.7 + 0.03, 0.0, 0.77, cz - 0.03, cz + 0.03, WOOD, vis=(1, 2)))
        cols.append(col(dx - S / 2 + 0.1, dx + S / 2 - 0.1, 0.72, 0.80, cz - 0.20, cz + 0.20))
        road.append([(dx - S / 2 + 0.1, 0.80, cz - 0.20), (dx + S / 2 - 0.1, 0.80, cz - 0.20),
                     (dx + S / 2 - 0.1, 0.80, cz + 0.20), (dx - S / 2 + 0.1, 0.80, cz + 0.20)])
    if wear:
        for s in out:
            if not getattr(s, "wear", None):
                s.wear = wear
    return out, cols, road


def stall(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    if kind in ("reed", "ab_collapsed", "ab_frame"):
        P = SPart("stall", budget="box", res3=True, mass=60.0, bury=0.06)
        st = {"reed": "std", "ab_collapsed": "collapsed", "ab_frame": "frame"}[kind]
        ss, cs, rd = reed_stall(state=st, wear=wear)
        add_all(P, ss + cs)
        for r in rd:
            P.road(r, "boards_ext")
        if rd:
            P.loot_rect("counter", 0.80, -0.8, 0.8, 0.76, 1.14, rng=0.25,
                        points=[(-0.45, 0.80, 0.96), (0.45, 0.80, 0.96)])
        if ab:
            P.add(litter(3, 0.0, 0.0, 1.2, sx=1.2))
        P.dim("plan", 1.82, 1.82, tol=0.01)
        P.dim("counter_h", 0.80, 0.80, tol=0.01)
    elif kind == "row3":
        P = SPart("stall", budget="medium", res3=True, mass=180.0, bury=0.06)
        for i, dx in enumerate((-1.82, 0.0, 1.82)):
            ss, cs, rd = reed_stall(dx=dx, state="std", share_left=i > 0)
            add_all(P, ss + cs)
            for r in rd:
                P.road(r, "boards_ext")
            P.loot_rect("counter%d" % i, 0.80, dx - 0.8, dx + 0.8, 0.76, 1.14, rng=0.25, points=[(dx, 0.80, 0.96)])
        P.dim("row_L", 5.46, 3 * 1.82, tol=0.01)
    elif kind == "booth":
        # kake-mise: a 1.5 x 1 ken plank booth, board back and side walls to 1.2, a mat roof on posts at 2.1-2.3
        P = SPart("stall", budget="medium", res3=True, mass=250.0, bury=0.06)
        Wd, D = 2.73, 1.82
        for sx in (-1, 1):
            for sz in (-1, 1):
                x, z = sx * (Wd / 2 - 0.05), sz * (D / 2 - 0.05)
                h = 2.1 if sz < 0 else 2.3
                P.add(W(x - 0.045, x + 0.045, -0.05, h, z - 0.045, z + 0.045, WOOD, vis=(1, 2, 3)))
                P.add(col(x - 0.045, x + 0.045, 0.0, h, z - 0.045, z + 0.045))
        P.add(W(-Wd / 2 + 0.05, Wd / 2 - 0.05, 0.0, 1.2, -D / 2 + 0.02, -D / 2 + 0.05, WOOD, vis=(1, 2, 3)))
        P.add(col(-Wd / 2 + 0.10, Wd / 2 - 0.10, 0.0, 1.2, -D / 2 + 0.02, -D / 2 + 0.05))
        for sx in (-1, 1):
            P.add(W(sx * (Wd / 2 - 0.05) - 0.015, sx * (Wd / 2 - 0.05) + 0.015, 0.0, 1.2, -D / 2 + 0.10, D / 2 - 0.1, WOOD,
                    vis=(1, 2)))
            P.add(col(sx * (Wd / 2 - 0.05) - 0.015, sx * (Wd / 2 - 0.05) + 0.015, 0.0, 1.2, -D / 2 + 0.10, D / 2 - 0.1))
        # counter plank across the front, a low platform inside (goods shelf)
        P.add(W(-Wd / 2 + 0.1, Wd / 2 - 0.1, 0.80, 0.84, D / 2 - 0.35, D / 2 - 0.02, WOOD, vis=(1, 2, 3)))
        P.add(W(-Wd / 2 + 0.1, Wd / 2 - 0.1, 0.0, 0.80, D / 2 - 0.08, D / 2 - 0.05, WOOD, vis=(1, 2)))
        P.add(col(-Wd / 2 + 0.1, Wd / 2 - 0.1, 0.0, 0.84, D / 2 - 0.35, D / 2 - 0.02))
        P.road([(-Wd / 2 + 0.1, 0.84, D / 2 - 0.35), (Wd / 2 - 0.1, 0.84, D / 2 - 0.35), (Wd / 2 - 0.1, 0.84, D / 2 - 0.02),
                (-Wd / 2 + 0.1, 0.84, D / 2 - 0.02)], "boards_ext")
        P.loot_rect("counter", 0.84, -1.2, 1.2, D / 2 - 0.35, D / 2 - 0.02, rng=0.25,
                    points=[(-0.8, 0.84, D / 2 - 0.18), (0.0, 0.84, D / 2 - 0.18), (0.8, 0.84, D / 2 - 0.18)])
        # mat roof on rails
        for sz, h in ((-1, 2.1), (1, 2.3)):
            P.add(pole((-Wd / 2, h - 0.03, sz * (D / 2 - 0.05)), (Wd / 2, h - 0.03, sz * (D / 2 - 0.05)), 0.03, WOOD, n=5,
                       vis=(1, 2)))
        P.add(grid_sheet(lambda u, v: (-Wd / 2 - 0.1 + (Wd + 0.2) * u, 2.33 - 0.25 * v - 0.06 * math.sin(math.pi * u),
                                       D / 2 + 0.1 - (D + 0.2) * v), 3, 2, MUSHIRO, vis=(1,), wear="_w2"))
        P.add(W(-Wd / 2, Wd / 2, 2.15, 2.2, -D / 2, D / 2, MUSHIRO, vis=(2, 3)))
        P.add(xf(basket(fill=leaves(3, 0.0, 0.0, 0.17, 0.17, wear="_w2"))[0], t=(0.6, 0.0, -0.4)))
        P.add(litter(4, 0.0, 0.0, 1.1, sx=1.4))
        P.dim("plan_w", 2.73, Wd, tol=0.01)
        P.dim("roof_h", 2.2, 2.2, tol=0.2)
    else:   # yatai: roofed street stall 1.82 x 0.91, counter 0.85, roof to 2.2, no wheels
        P = SPart("stall", budget="medium", res3=True, mass=150.0, bury=0.02)
        Wd, D, C = 1.82, 0.91, 0.85
        P.add(W(-Wd / 2, Wd / 2, 0.0, C - 0.04, -D / 2, D / 2 - 0.25, WOOD, vis=(1, 2, 3)))
        P.add(col(-Wd / 2, Wd / 2, 0.0, C, -D / 2, D / 2))
        P.add(W(-Wd / 2 - 0.02, Wd / 2 + 0.02, C - 0.04, C, -D / 2 - 0.02, D / 2 + 0.02, WOOD, vis=(1, 2, 3)))
        # rotted counter: a split board end drooping
        br = W(Wd / 2 - 0.5, Wd / 2 + 0.02, C - 0.04, C, D / 2 - 0.25, D / 2 + 0.02, WOOD, vis=(1,))
        br.wear = "_w2"
        P.add(xf(br, rz=-4.0, pivot=(Wd / 2 - 0.5, C, 0.0), t=(0.0, 0.003, 0.0)))
        for sx in (-1, 1):
            P.add(W(sx * (Wd / 2 - 0.04) - 0.035, sx * (Wd / 2 - 0.04) + 0.035, C, 2.05, -D / 2 + 0.02, -D / 2 + 0.09, WOOD,
                    vis=(1, 2, 3)))
            P.add(col(sx * (Wd / 2 - 0.04) - 0.035, sx * (Wd / 2 - 0.04) + 0.035, C, 2.05, -D / 2 + 0.02, -D / 2 + 0.09))
            P.add(W(sx * (Wd / 2 - 0.04) - 0.03, sx * (Wd / 2 - 0.04) + 0.03, C, 1.95, D / 2 - 0.08, D / 2 - 0.02, WOOD,
                    vis=(1, 2)))
        P.add(W(-Wd / 2, Wd / 2, C, 1.5, -D / 2 + 0.02, -D / 2 + 0.04, WOOD, vis=(1, 2)))
        rs, rc = gable_roof(Wd + 0.4, D + 0.5, 1.98, 2.2, wear="_w1", vis=(1, 2, 3))
        add_all(P, rs + rc)
        P.add(pole((-0.3, 1.97, D / 2 + 0.05), (0.3, 1.97, D / 2 + 0.05), 0.012, BAMBOO, n=4, vis=(1,)))
        add_all(P, noren(0.35, wear="_w2", torn=True, top=1.95, zc=D / 2 + 0.05))
        P.road([(-Wd / 2, C, D / 2 - 0.25), (Wd / 2 - 0.5, C, D / 2 - 0.25), (Wd / 2 - 0.5, C, D / 2), (-Wd / 2, C, D / 2)],
               "boards_ext")
        P.loot_rect("counter", C, -0.8, 0.3, D / 2 - 0.25, D / 2, rng=0.2, points=[(-0.5, C, D / 2 - 0.12),
                                                                                  (0.1, C, D / 2 - 0.12)])
        P.add(litter(5, 0.0, 0.5, 0.8, sx=1.4))
        P.dim("yatai_w", 1.82, Wd, tol=0.01)
        P.dim("counter_h", 0.85, C, tol=0.01)
        P.dim("roof_h", 2.2, 2.2 + 0.07, tol=0.1)
    return P


# ================================================================================================ kosatsu
def kosatsu(kind):
    ab = kind.startswith("ab")
    wear = "_w2" if ab else None
    P = SPart("kosatsu", budget="medium", res3=True, mass=5000.0, bury=0.06)
    if kind == "forest":
        # a single roofed board on two posts (forest / hunting-ground notice)
        P.mass = 80.0
        for sx in (-1, 1):
            P.add(W(sx * 0.6 - 0.05, sx * 0.6 + 0.05, -0.05, 2.25, -0.05, 0.05, WOOD, vis=(1, 2)))
            P.add(col(sx * 0.6 - 0.05, sx * 0.6 + 0.05, 0.0, 2.25, -0.05, 0.05))
        P.add(W(-0.55, 0.55, 1.30, 1.80, 0.05, 0.08, WOOD, vis=(1, 2, 3)))
        P.add(col(-0.55, 0.55, 1.30, 1.80, 0.05, 0.08, DARK))
        P.add(text_on((0.0, 1.55, 0.08), X, Y, 0.42, SUMI, "kosatsu_chuko_1711", wear="_w2", crop=(0.0, 0.0, 1.0, 1.0)))
        rs, rc = gable_roof(1.55, 0.75, 2.10, 2.35, wear=wear)
        add_all(P, rs + rc)
        P.dim("board_w", 1.1, 1.1, tol=0.1)
        return P
    Fw = 3.6 if kind in ("std", "ab_boards_down") else 4.6
    Bw, Bd, Bh = Fw + 1.8, 2.0, 0.75
    # stone-faced earth base, earth top (leaf litter), Roadway on the top
    P.add(W(-Bw / 2, Bw / 2, -0.05, Bh, -Bd / 2, Bd / 2, {"top": LEAF, "default": CUT}, vis=(1, 2, 3)))
    P.add(col(-Bw / 2, Bw / 2, 0.0, Bh, -Bd / 2, Bd / 2, CUT))
    P.road([(-Bw / 2, Bh, -Bd / 2), (Bw / 2, Bh, -Bd / 2), (Bw / 2, Bh, Bd / 2), (-Bw / 2, Bh, Bd / 2)], "stone_ext")
    # courses on the stone face (visual strips)
    for y in (0.25, 0.5):
        P.add(W(-Bw / 2 - 0.005, Bw / 2 + 0.005, y - 0.01, y + 0.01, Bd / 2, Bd / 2 + 0.006, "wood_sooted", vis=(1,)))
    P.add(moss_top(3, -Bw / 2 + 0.4, Bd / 2 - 0.3, 0.3, Bh))
    # frame: two main posts, a tie beam, board roof (ridge along x)
    y0 = Bh
    EV, RG = y0 + 2.85, y0 + 3.45
    for sx in (-1, 1):
        x = sx * Fw / 2
        P.add(W(x - 0.09, x + 0.09, y0 - 0.1, EV, -0.09, 0.09, WOOD, vis=(1, 2, 3)))
        P.add(col(x - 0.09, x + 0.09, y0, EV, -0.09, 0.09))
        # back struts
        P.add(beam((x, y0, -0.8), (x, EV - 0.6, -0.05), 0.07, 0.07, WOOD, vis=(1, 2)))
        P.add(col_solid(beam((x, y0 + 0.02, -0.8), (x, EV - 0.65, -0.12), 0.07, 0.07, WOOD)))
    P.add(W(-Fw / 2 - 0.3, Fw / 2 + 0.3, EV - 0.15, EV, -0.08, 0.08, WOOD, vis=(1, 2, 3)))
    P.add(W(-Fw / 2, Fw / 2, y0 + 0.95, y0 + 1.05, -0.06, 0.06, WOOD, vis=(1, 2)))
    rs, rc = gable_roof(Fw + 1.0, 1.9, EV, RG, wear=wear)
    add_all(P, rs + rc)
    # the boards: 2 rows under the roof, each 1.0 x 0.42, text = the 1711 Shotoku edict (crops of the atlas cell)
    nb = 5 if Fw < 4 else 7
    rows = [(y0 + 2.20, (nb + 1) // 2), (y0 + 1.62, nb // 2)]
    bw, bh = 1.0, 0.44
    fallen = (1, 3) if ab else ()
    k = 0
    for yc, n in rows:
        for i in range(n):
            xc = (i - (n - 1) / 2) * (bw + 0.08)
            crop = [(0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 0.55, 1.0), (0.45, 0.0, 1.0, 1.0), (0.2, 0.0, 0.8, 1.0)][k % 4]
            board = [W(xc - bw / 2, xc + bw / 2, yc - bh / 2, yc + bh / 2, 0.10, 0.13, WOOD, vis=(1, 2)),
                     text_on((xc, yc, 0.13), X, Y, bh * 0.92, SUMI, "kosatsu_chuko_1711", wear="_w2" if ab else "_w1",
                             width=bw * 0.94, crop=crop),
                     W(xc - bw / 2 - 0.02, xc + bw / 2 + 0.02, yc + bh / 2, yc + bh / 2 + 0.03, 0.08, 0.15, DARK, vis=(1,))]
            if k in fallen:
                # fallen from its pegs and split, lying on the base in front
                board = board[:2]
                board = xfs(board, rx=-90.0, pivot=(xc, yc - bh / 2, 0.13))
                board = xfs(board, t=(0.2 * (k - 2), y0 - (yc - bh / 2) + 0.001 - 0.10 + 0.13, 0.55 + 0.1 * k))
                board = xfs(board, ry=8.0 * (k - 2), pivot=(xc, y0, 0.8))
                for s in board:
                    s.wear = "_w2"
            add_all(P, board)
            k += 1
    P.add(W(-Fw / 2, Fw / 2, y0 + 1.30, y0 + 2.50, 0.1, 0.13, DARK, vis=(3,)))
    P.add(col(-Fw / 2, Fw / 2, y0 + 1.30, y0 + 2.46, 0.1, 0.13, DARK))
    # bamboo fence in front, on the base, 1.0 high, 0.9 out
    fz = 0.85
    gaps = {3, 4, 9} if ab else set()
    npk = int(Fw / 0.15)
    for i in range(npk + 1):
        if i in gaps:
            continue
        x = -Fw / 2 + Fw * i / npk
        P.add(pole((x, y0 - 0.02, fz), (x, y0 + 1.0, fz), 0.018, BAMBOO, n=4, vis=(1,), wear=wear))
    for y in (y0 + 0.35, y0 + 0.85):
        P.add(pole((-Fw / 2 - 0.05, y, fz + 0.03), (Fw / 2 + 0.05, y, fz + 0.03), 0.018, BAMBOO, n=4, vis=(1, 2), wear=wear))
    P.add(W(-Fw / 2, Fw / 2, y0, y0 + 1.0, fz - 0.01, fz + 0.01, BAMBOO, vis=(2,)))
    P.add(col(-Fw / 2, Fw / 2, y0, y0 + 1.0, fz - 0.02, fz + 0.04, BAMBOO))
    if ab:
        P.add(litter(9, 0.5, 0.4, 1.4, sx=1.6))
    P.dim("frame_w", Fw, Fw, tol=0.01)
    P.dim("ridge_h", 3.0 if Fw < 4 else 4.2, RG, tol=1.3)
    P.dim("boards", nb, nb, tol=0)
    P.dim("base_h", 0.75, Bh, tol=0.15)
    return P


# ================================================================================================ registry
PROPS = [
    {"id": "jp_s_gutter", "cat": "street", "notes": ["pieces snap to the half-ken grid along a house front, 0.3 m out; "
                                                     "they sit in a terrain ditch (tops flush with grade): the ditch is "
                                                     "cut by the terrain / placement agent", "Geometry + Roadway only on "
                                                     "the slab and the dobu-ita boards: the channel stays walkable"],
     "models": [
         M("jp_s_gutter_stone_1ken", "stone_1ken", "intact", "Street gutter, stone-lined, 1 ken", lambda: gutter("stone_1ken")),
         M("jp_s_gutter_stone_half", "stone_half", "intact", "Street gutter, stone-lined, half ken",
           lambda: gutter("stone_half")),
         M("jp_s_gutter_corner", "corner", "intact", "Street gutter, 90-degree corner", lambda: gutter("corner")),
         M("jp_s_gutter_slab", "slab", "intact", "Street gutter with a slab crossing (door)", lambda: gutter("slab")),
         M("jp_s_gutter_board_1ken", "board_1ken", "intact", "Alley drain with dobu-ita covers, 1 ken",
           lambda: gutter("board_1ken")),
         M("jp_s_gutter_outfall", "outfall", "intact", "Gutter outfall into a canal or ditch", lambda: gutter("outfall")),
         M("jp_s_gutter_earth_1ken", "earth_1ken", "intact", "Rural earth-banked gutter, field-stone edge",
           lambda: gutter("earth_1ken")),
         M("jp_s_gutter_ab_silted", "stone_1ken", "abandoned", "Street gutter silted with leaves, a stone tipped in",
           lambda: gutter("ab_silted")),
     ]},
    {"id": "jp_s_shopfront", "cat": "street", "notes": ["PROXIES for the furnished shop variant p3d (PLAYBOOK 10.4, G1 A3 "
                                                        "answer 8); wall plane z = 0, y = 0 at the wall foot; noren on "
                                                        "open shop / eating-house doors only; shape signs only on the "
                                                        "matching trade", "the six shape signs are six models (one per "
                                                        "trade) rather than one _shape_x6 model"],
     "models": [
         M("jp_s_shopfront_noren_long", "noren_long", "intact", "Long noren, 3 panels, shop mark",
           lambda: shopfront("noren_long")),
         M("jp_s_shopfront_noren_half", "noren_half", "intact", "Half noren (eating house)", lambda: shopfront("noren_half")),
         M("jp_s_shopfront_mizuhiki", "mizuhiki", "intact", "Eave curtain (mizuhiki-noren), 1 ken",
           lambda: shopfront("mizuhiki")),
         M("jp_s_shopfront_sudare_up", "sudare_up", "intact", "Reed blind rolled up", lambda: shopfront("sudare_up")),
         M("jp_s_shopfront_sudare_down", "sudare_down", "abandoned", "Reed blind down, slumped and holed",
           lambda: shopfront("sudare_down")),
         M("jp_s_shopfront_kanban_hang", "kanban_hang", "intact", "Hanging signboard (confectioner)",
           lambda: shopfront("kanban_hang")),
         M("jp_s_shopfront_kanban_stand", "kanban_stand", "intact", "Standing signboard (soba)",
           lambda: shopfront("kanban_stand")),
         M("jp_s_shopfront_shape_brush", "shape", "intact", "Shape sign: giant brush", lambda: shopfront("shape_brush")),
         M("jp_s_shopfront_shape_geta", "shape", "intact", "Shape sign: geta", lambda: shopfront("shape_geta")),
         M("jp_s_shopfront_shape_tabi", "shape", "intact", "Shape sign: tabi", lambda: shopfront("shape_tabi")),
         M("jp_s_shopfront_shape_gourd", "shape", "intact", "Shape sign: medicine gourd", lambda: shopfront("shape_gourd")),
         M("jp_s_shopfront_shape_umbrella", "shape", "intact", "Shape sign: umbrella",
           lambda: shopfront("shape_umbrella")),
         M("jp_s_shopfront_shape_fan", "shape", "intact", "Shape sign: fan", lambda: shopfront("shape_fan")),
         M("jp_s_shopfront_ab_noren_torn", "noren", "abandoned", "Noren faded to grey-blue, a panel torn off",
           lambda: shopfront("ab_noren_torn")),
         M("jp_s_shopfront_ab_fallen", "noren", "abandoned", "Noren pole dropped, noren heaped on the threshold",
           lambda: shopfront("ab_fallen")),
         M("jp_s_shopfront_ab_kanban_askew", "kanban_hang", "abandoned", "Hanging signboard hanging from one cord",
           lambda: shopfront("ab_kanban_askew")),
     ]},
    {"id": "jp_s_lantern_sign", "cat": "street", "notes": ["never emissive (dead world, no light anywhere)",
                                                           "hung pieces are proxies / wall-backed: wall plane z = 0"],
     "models": [
         M("jp_s_lantern_sign_chochin_shop", "chochin_shop", "intact", "Shop lantern (sake)", lambda: lantern_sign("chochin_shop")),
         M("jp_s_lantern_sign_chochin_inn", "chochin_inn", "intact", "Inn lantern", lambda: lantern_sign("chochin_inn")),
         M("jp_s_lantern_sign_chochin_gate", "chochin_gate", "intact", "Ward-gate lantern (Honcho)",
           lambda: lantern_sign("chochin_gate")),
         M("jp_s_lantern_sign_kake", "kake", "intact", "Hanging box sign lamp (kake-andon)", lambda: lantern_sign("kake")),
         M("jp_s_lantern_sign_oki", "oki", "intact", "Standing sign lamp (oki-andon)", lambda: lantern_sign("oki")),
         M("jp_s_lantern_sign_tsuji", "tsuji", "intact", "Crossroads lamp on a post (tsuji-andon)",
           lambda: lantern_sign("tsuji")),
         M("jp_s_lantern_sign_ab_torn", "chochin_shop", "abandoned", "Shop lantern, paper split and holed",
           lambda: lantern_sign("ab_torn")),
         M("jp_s_lantern_sign_ab_fallen", "oki", "abandoned", "Standing lamp tipped, a lantern crushed on the ground",
           lambda: lantern_sign("ab_fallen")),
     ]},
    {"id": "jp_s_nobori", "cat": "street", "notes": ["festival leftovers (G1 A3 answer 7): weathered and messed up"],
     "models": [
         M("jp_s_nobori_shop", "shop", "intact", "Shop banner (soba) on a bamboo pole", lambda: nobori("shop")),
         M("jp_s_nobori_shrine", "shrine", "intact", "Shrine dedication banners, a pair", lambda: nobori("shrine")),
         M("jp_s_nobori_socket_stones", "socket", "intact", "Banner socket stones, banner taken down",
           lambda: nobori("socket_stones")),
         M("jp_s_nobori_ab_tattered", "shrine_single", "abandoned", "Banner shredded to a strip, pole leaning",
           lambda: nobori("ab_tattered")),
         M("jp_s_nobori_ab_down", "shrine_single", "abandoned", "Banner pole fallen across the approach",
           lambda: nobori("ab_down")),
     ]},
    {"id": "jp_s_stall", "cat": "street", "notes": ["counters are Roadway + loot surfaces"],
     "models": [
         M("jp_s_stall_reed", "reed", "intact", "Reed-screen stall with counter", lambda: stall("reed")),
         M("jp_s_stall_booth", "booth", "intact", "Plank booth (kake-mise)", lambda: stall("booth")),
         M("jp_s_stall_yatai", "yatai", "intact", "Roofed street stall (yatai), no wheels", lambda: stall("yatai")),
         M("jp_s_stall_row3", "row3", "intact", "Three reed stalls (market row)", lambda: stall("row3")),
         M("jp_s_stall_ab_collapsed", "reed", "abandoned", "Reed stall collapsed, mat fallen in", lambda: stall("ab_collapsed")),
         M("jp_s_stall_ab_frame", "reed", "abandoned", "Bare stall frame, screens gone", lambda: stall("ab_frame")),
     ]},
    {"id": "jp_s_kosatsu", "cat": "roadside", "notes": ["boards carry the 1711 Shotoku edict (jp_m_decal_sumi_text "
                                                        "kosatsu_chuko_1711, cropped for variety); also KEEP_CIVIC "
                                                        "government 6 (G1 A3 answer 2)"],
     "models": [
         M("jp_s_kosatsu_std", "std", "intact", "Notice board (kosatsuba), post-town size", lambda: kosatsu("std")),
         M("jp_s_kosatsu_large", "large", "intact", "Notice board, bridge-end size (Fuchu type)", lambda: kosatsu("large")),
         M("jp_s_kosatsu_forest", "forest", "intact", "Single roofed notice board (forest)", lambda: kosatsu("forest")),
         M("jp_s_kosatsu_ab_boards_down", "std", "abandoned", "Notice board, two boards fallen, fence gaps",
           lambda: kosatsu("ab_boards_down")),
     ]},
]
