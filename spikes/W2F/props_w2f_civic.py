"""W2F specialty props, smithy / swordsmith / guard post / shrine basin (spikes/W2F/W2F_NOTES.md), built into
jp_furniture.pbo by spikes/W2F/build_w2f.py. Frames as fkit / lkit ('floor' base centre on the floor, +z = front;
'wall' wall face z = 0; 'hang' beam underside). Dead world: the forges are cold, the trough dry."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import props_w2f_sacred as SC  # noqa: E402
from props_w2f_sacred import (core, box, prism, lathe, xf, xfs, W, col, cyl_col, LPart, stain, pole, cord, lod_box,  # noqa
                              wear_all, peg, rng, M, mv, rot, WOOD, WEATH, IRON, DARK, PALE, BAMBOO, ASH, LITTER, ROPE,
                              KINARI, BRONZE, KURO, NEW, SILVER, CUTSTONE)
import fkit  # noqa: E402
import w2kit  # noqa: E402  (B3b / W2, read-only: torii_rope)

CAT = "civicfit"
CLAY = "wall_nakanuri_int"        # warm interior clay (PLAYBOOK T6): the forge hearth
SOOTW = "wood_sooted"
EARTH = "ground_doma_earth"
ENDG = "wood_endgrain"


# ================================================================================================ forge
def forge(w=1.10, d=0.90, h=0.55):
    """Hodo: a clay hearth box, the fire pot sunk at the bellows (-x) end, ash and dead charcoal, the clay tuyere on
    the -x side; the +x rim is a ledge where the smith laid his work (loot)."""
    P = LPart("forge", budget="furniture", mass=400.0, anchor="floor")
    px0, px1 = -w / 2 + 0.10, -w / 2 + 0.55
    pz0, pz1 = -d / 2 + 0.18, d / 2 - 0.22
    out = [W(-w / 2, w / 2, 0.0, h - 0.18, -d / 2, d / 2, CLAY),
           W(-w / 2, px0, h - 0.18, h, -d / 2, d / 2, CLAY),
           W(px1, w / 2, h - 0.18, h, -d / 2, d / 2, CLAY),
           W(px0, px1, h - 0.18, h, -d / 2, pz0, CLAY),
           W(px0, px1, h - 0.18, h, pz1, d / 2, CLAY),
           W(px0, px1, h - 0.18, h - 0.17, pz0, pz1, ASH, vis=(1,))]
    r = rng("forge%.2f" % w)
    for i in range(14):                                                  # dead charcoal in the pot
        x = r.uniform(px0 + 0.05, px1 - 0.05)
        z = r.uniform(pz0 + 0.04, pz1 - 0.04)
        s = r.uniform(0.025, 0.045)
        out.append(xf(box(-s, s, 0.0, s * 0.8, -s * 0.7, s * 0.7, SOOTW, vis=(1,)), ry=r.uniform(0, 180),
                      t=(x, h - 0.17, z)))
    out.append(pole((-w / 2 - 0.12, h - 0.10, (pz0 + pz1) / 2), (px0 + 0.02, h - 0.10, (pz0 + pz1) / 2), 0.045, CLAY,
                    n=6, vis=(1,)))                                      # the tuyere
    P.adds(out)
    P.add(W(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, CLAY, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, CLAY))
    P.loot_rect("ledge", h, px1 + 0.06, w / 2 - 0.06, -d / 2 + 0.10, d / 2 - 0.10, rng=0.2)
    P.dim("w", w, w, tol=0.005)
    P.dim("h", h, h, tol=0.005)
    P.notes.append("cold forge hearth (hodo): fire pot at -x (bellows side, tuyere through the -x face), the +x ledge "
                   "carries loot")
    return P


def fuigo(w=0.45, L=1.10, h=0.55, ab=False):
    """Box bellows: a long box along z, the pull rod out of the back (-z) end, the nozzle out of the +x side near the
    front end (towards the forge). Its lid is a loot surface."""
    P = LPart("fuigo", budget="furniture", mass=45.0, anchor="floor")
    t = 0.03
    out = [W(-w / 2, w / 2, 0.0, 0.05, -L / 2, L / 2, SOOTW),
           W(-w / 2, -w / 2 + t, 0.05, h - 0.03, -L / 2, L / 2, SOOTW),
           W(w / 2 - t, w / 2, 0.05, h - 0.03, -L / 2, L / 2, SOOTW),
           W(-w / 2 + t, w / 2 - t, 0.05, h - 0.03, -L / 2, -L / 2 + t, SOOTW),
           W(-w / 2 + t, w / 2 - t, 0.05, h - 0.03, L / 2 - t, L / 2, SOOTW)]
    for sz in (-1, 1):                                                   # iron bands
        out.append(W(-w / 2 - 0.004, w / 2 + 0.004, 0.05, h - 0.03, sz * L * 0.3 - 0.02, sz * L * 0.3 + 0.02, IRON,
                     vis=(1,)))
    lid = W(-w / 2, w / 2, h - 0.03, h, -L / 2, L / 2, SOOTW)
    rod_y = h * 0.55
    if ab:                                                               # the lid knocked askew, the rod pulled out
        lid = xf(lid, ry=12.0, t=(0.04, 0.0, 0.05))
        rod = [pole((0.0, 0.03, -L / 2 - 0.10), (0.25, 0.03, -L / 2 - 0.85), 0.018, WOOD, n=5, vis=(1,)),
               pole((0.10, 0.03, -L / 2 - 0.88), (0.40, 0.03, -L / 2 - 0.82), 0.02, WOOD, n=5, vis=(1,))]
    else:
        rod = [pole((0.0, rod_y, -L / 2), (0.0, rod_y, -L / 2 - 0.30), 0.018, WOOD, n=5, vis=(1,)),
               pole((-0.16, rod_y, -L / 2 - 0.30), (0.16, rod_y, -L / 2 - 0.30), 0.022, WOOD, n=5, vis=(1,))]
    out.append(lid)
    out += rod
    out.append(pole((w / 2, 0.18, L / 2 - 0.20), (w / 2 + 0.20, 0.20, L / 2 - 0.20), 0.035, IRON, n=6, vis=(1,)))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(W(-w / 2, w / 2, 0.0, h, -L / 2, L / 2, SOOTW, vis=(2,)))
    cols = [col(-w / 2, w / 2, 0.0, h, -L / 2, L / 2, SOOTW)]
    P.adds(cols)
    fkit.road_tops(P, cols, surf="boards")
    m = 0.06
    P.loot_rect("lid", h, -w / 2 + m, w / 2 - m, -L / 2 + 0.15, L / 2 - 0.15, rng=0.2)
    P.dim("L", L, L, tol=0.005)
    P.notes.append("box bellows (fuigo): nozzle on +x near the +z end (towards the forge), pull rod out of -z; %s"
                   % ("lid knocked askew, rod pulled out and dropped (ransacked)" if ab else "as left"))
    return P


def anvil(r=0.25, h=0.42):
    P = LPart("anvil", budget="furniture", mass=120.0, anchor="floor")
    out = [lathe([(0.0, 0.0), (r + 0.02, 0.0), (r, 0.05), (r, h - 0.01), (r - 0.01, h), (0.0, h)], 10, WEATH,
                 vis=(1,)),
           xf(lathe([(0.0, 0.0), (r - 0.01, 0.0), (r - 0.01, 0.003), (0.0, 0.003)], 10, ENDG, vis=(1,)), t=(0.0, h, 0.0)),
           W(-0.14, 0.14, h - 0.04, h + 0.12, -0.06 - 0.03, 0.06 - 0.03, IRON),
           W(-0.16, 0.16, h + 0.10, h + 0.14, -0.08 - 0.03, 0.08 - 0.03, IRON, vis=(1,))]
    out.append(pole((-0.05, h + 0.004, 0.12), (0.18, h + 0.004, 0.17), 0.008, IRON, n=4, vis=(1,)))   # tongs
    out.append(pole((-0.05, h + 0.004, 0.14), (0.18, h + 0.004, 0.11), 0.008, IRON, n=4, vis=(1,)))
    P.adds(out)
    P.add(lathe([(0.0, 0.0), (r, 0.0), (r, h + 0.14), (0.0, h + 0.14)], 6, WEATH, vis=(2,), smooth=False))
    P.add(cyl_col(r, 0.0, h, n=8, mat=WEATH))
    P.add(col(-0.16, 0.16, h, h + 0.14, -0.11, 0.05, IRON))
    P.loot_rect("stump", h + 0.003, -0.20, -0.08, 0.08, 0.20, rng=0.12, points=[(-0.15, h + 0.003, 0.14)])
    P.dim("h", h + 0.14, h + 0.14, tol=0.005)
    P.notes.append("anvil (kanatoko) set in a stump, tongs left on the stump top (loot beside them)")
    return P


def mizubune(L=1.40, w=0.40, h=0.45):
    P = LPart("mizubune", budget="furniture", mass=40.0, anchor="floor")
    t = 0.035
    out = [W(-w / 2, w / 2, 0.06, 0.10, -L / 2, L / 2, WEATH, vis=(1,)),
           W(-w / 2, -w / 2 + t, 0.06, h, -L / 2, L / 2, WEATH, vis=(1,)),
           W(w / 2 - t, w / 2, 0.06, h, -L / 2, L / 2, WEATH, vis=(1,)),
           W(-w / 2 + t, w / 2 - t, 0.06, h, -L / 2, -L / 2 + t, WEATH, vis=(1,)),
           W(-w / 2 + t, w / 2 - t, 0.06, h, L / 2 - t, L / 2, WEATH, vis=(1,))]
    for sz in (-1, 1):
        out.append(W(-w / 2 - 0.03, w / 2 + 0.03, 0.0, 0.06, sz * L * 0.35 - 0.04, sz * L * 0.35 + 0.04, WEATH, vis=(1,)))
    # FX1 (2026-10-01): no leaf litter in the trough (it stands indoors, in a forge room without any)
    P.adds(out)
    P.add(W(-w / 2, w / 2, 0.0, h, -L / 2, L / 2, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -L / 2, L / 2, WEATH))
    P.loot_rect("trough", 0.10, -w / 2 + 0.08, w / 2 - 0.08, -L / 2 + 0.15, L / 2 - 0.15, rng=0.15, per=0.6)
    P.dim("L", L, L, tol=0.005)
    P.notes.append("the swordsmith's long quench trough (mizubune), dry and stained (abandoned); loot inside it")
    return P


def tongs_wall(taken=False):
    P = LPart("tongs_wall", budget="furniture", mass=6.0, anchor="wall", flat=True)
    y = 1.30
    out = [W(-0.60, 0.60, y, y + 0.12, 0.0, 0.022, SOOTW)]
    items = [("tongs", -0.48), ("tongs", -0.32), ("hammer", -0.14), ("hammer", 0.02), ("sickle", 0.20),
             ("sickle", 0.34), ("hoe", 0.50)]
    if taken:
        items = [it for k, it in enumerate(items) if k not in (1, 3, 5)]
    for kind, x in items:
        out.append(peg(x, y + 0.06, L=0.07, z0=0.0))
        z = 0.06
        if kind == "tongs":
            for s in (-1, 1):
                out.append(pole((x, y + 0.04, z), (x + s * 0.05, y - 0.45, z + 0.01), 0.007, IRON, n=4, vis=(1,)))
        elif kind == "hammer":
            out.append(pole((x, y + 0.04, z), (x, y - 0.32, z), 0.012, WOOD, n=5, vis=(1,)))
            out.append(W(x - 0.06, x + 0.06, y - 0.38, y - 0.32, z - 0.025, z + 0.025, IRON, vis=(1,)))
        elif kind == "sickle":
            out.append(pole((x, y + 0.04, z), (x, y - 0.24, z), 0.011, WOOD, n=5, vis=(1,)))
            for k in range(3):
                a = math.radians(-10 + 35 * k)
                x0 = x + 0.09 * math.sin(a) * k / 2
                out.append(xf(W(0.0, 0.08, -0.008, 0.008, -0.002, 0.002, IRON, vis=(1,)), rz=-25 - 30 * k,
                              t=(x + 0.02 + 0.06 * k, y - 0.24 + 0.015 * k * k, z)))
        else:
            out.append(pole((x, y + 0.04, z), (x, y - 0.30, z), 0.012, WOOD, n=5, vis=(1,)))
            out.append(W(x - 0.07, x + 0.07, y - 0.46, y - 0.30, z - 0.004, z + 0.004, IRON, vis=(1,)))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(W(-0.60, 0.60, y - 0.46, y + 0.12, 0.0, 0.08, SOOTW, vis=(2,)))
    P.dim("w", 1.20, 1.20, tol=0.005)
    P.notes.append("smith's tongs, hammers and finished sickles / a hoe on pegs (mount wall)%s"
                   % ("; half of them taken" if taken else ""))
    return P


def tsuchioki():
    P = LPart("tsuchioki", budget="furniture", mass=30.0, anchor="floor")
    w, d, h = 0.90, 0.45, 0.30
    out = [W(-w / 2, w / 2, h - 0.03, h, -d / 2, d / 2, WEATH)]
    for sx in (-1, 1):
        out.append(W(sx * (w / 2 - 0.06) - 0.03, sx * (w / 2 - 0.06) + 0.03, 0.0, h - 0.03, -d / 2 + 0.03,
                     d / 2 - 0.03, WEATH))
    rim = [W(-w / 2, w / 2, h, h + 0.06, -d / 2, -d / 2 + 0.025, WEATH, vis=(1,)),
           W(-w / 2, w / 2, h, h + 0.06, d / 2 - 0.025, d / 2, WEATH, vis=(1,)),
           W(-w / 2, -w / 2 + 0.025, h, h + 0.06, -d / 2 + 0.025, d / 2 - 0.025, WEATH, vis=(1,)),
           W(-0.10, -0.075, h, h + 0.06, -d / 2 + 0.025, d / 2 - 0.025, WEATH, vis=(1,))]
    out += rim
    out.append(W(-w / 2 + 0.025, -0.10, h, h + 0.03, -d / 2 + 0.025, d / 2 - 0.025, "ground_earth_bare", vis=(1,)))     # clay
    out.append(W(0.05, 0.27, h, h + 0.06, -0.12, -0.02, CUTSTONE, vis=(1,)))                              # whetstones
    out.append(W(0.10, 0.30, h, h + 0.05, 0.05, 0.13, CUTSTONE, vis=(1,)))
    P.adds(out)
    P.add(W(-w / 2, w / 2, 0.0, h + 0.06, -d / 2, d / 2, WEATH, vis=(2,)))
    P.add(col(-w / 2, w / 2, 0.0, h, -d / 2, d / 2, WEATH))
    P.loot_rect("bench", h, 0.32, w / 2 - 0.04, -d / 2 + 0.08, d / 2 - 0.08, rng=0.12, points=[(0.37, h, 0.0)])
    P.dim("w", w, w, tol=0.005)
    P.notes.append("clay-coating trough (tsuchioki) with whetstones; loot on its free end")
    return P


def blade_rack(empty=False):
    P = LPart("blade_rack", budget="furniture", mass=4.0, anchor="wall", flat=True)
    out = []
    for y in (1.00, 1.30):
        out.append(W(-0.65, 0.65, y, y + 0.05, 0.0, 0.025, KURO))
        for x in (-0.45, 0.45):
            out.append(peg(x, y + 0.025, L=0.10, z0=0.0))
    if not empty:
        for k, y in enumerate((1.06, 1.105, 1.36, 1.405)):
            L = 0.95 - 0.08 * k
            segs = 3
            for i in range(segs):
                xa = -L / 2 + L * i / segs
                xb = -L / 2 + L * (i + 1) / segs
                ya = y + 0.02 * math.sin(math.pi * i / segs)
                yb = y + 0.02 * math.sin(math.pi * (i + 1) / segs)
                out.append(core.hexa([(xa, ya, 0.05), (xb, yb, 0.05), (xb, yb, 0.056), (xa, ya, 0.056),
                                      (xa, ya + 0.03, 0.05), (xb, yb + 0.03, 0.05), (xb, yb + 0.03, 0.056),
                                      (xa, ya + 0.03, 0.056)], IRON, vis=(1,)))
            out.append(W(L / 2, L / 2 + 0.18, y + 0.005, y + 0.025, 0.048, 0.058, DARK, vis=(1,)))      # tang
    wear_all(out, "_w1")
    P.adds(out)
    P.add(W(-0.65, 0.65, 1.0, 1.35, 0.0, 0.06, KURO, vis=(2,)))
    P.dim("w", 1.30, 1.30, tol=0.005)
    P.notes.append("rack of bare blades before polishing (mount wall)%s" % ("; emptied" if empty else ""))
    return P


def shimenawa_hang(L=1.60):
    P = LPart("shimenawa_hang", budget="medium", mass=2.0, anchor="hang", flat=True)
    y = -0.22
    out = w2kit.torii_rope(-L / 2, L / 2, y, 0.0, r=0.03, drop=0.075 * L / 1.82, with_shide=True, wear="_w2", seed=7)  # FX2 sag
    for x in (-L / 2, L / 2):
        out.append(cord((x, y + 0.02, 0.0), (x, 0.0, 0.0), 0.005))
    for s in out:
        s.vis = {1}
    P.adds(out)
    P.add(box(-L / 2, L / 2, y - 0.30, y + 0.04, -0.04, 0.04, ROPE, vis=(2,)))
    P.finish_hang()
    P.dim("L", L, L, tol=0.01)
    P.notes.append("straw rope with paper streamers hung from the tie beam over the forge (mount beam)")
    return P


# ================================================================================================ guard post
def mitsudogu(taken=False):
    P = LPart("mitsudogu", budget="furniture", mass=8.0, anchor="wall", flat=True)
    out = []
    for y in (1.15, 1.85):
        out.append(W(-0.45, 0.45, y, y + 0.05, 0.0, 0.03, WEATH))
        for x in (-0.38, 0.38):
            out.append(W(x - 0.02, x + 0.02, y - 0.08, y + 0.05, 0.0, 0.06, WEATH, vis=(1,)))
    tools = [("sasumata", -0.25, 2.15), ("tsukubo", 0.0, 2.25), ("sodegarami", 0.25, 2.30)]
    if taken:
        tools = tools[:1] + tools[2:]
    for kind, x, L in tools:
        z = 0.06
        top = L
        out.append(pole((x, 0.02, z), (x, top - 0.18, z + 0.01), 0.016, WEATH, n=5, vis=(1,)))
        if kind == "sasumata":                                           # the U fork
            out.append(W(x - 0.13, x + 0.13, top - 0.20, top - 0.17, z - 0.01, z + 0.02, IRON, vis=(1,)))
            for s in (-1, 1):
                out.append(W(x + s * 0.13 - 0.012, x + s * 0.13 + 0.012, top - 0.20, top, z - 0.01, z + 0.02, IRON,
                             vis=(1,)))
        elif kind == "tsukubo":                                          # the T rake with spikes
            out.append(W(x - 0.17, x + 0.17, top - 0.20, top - 0.14, z - 0.015, z + 0.025, WEATH, vis=(1,)))
            for k in range(5):
                xx = x - 0.14 + 0.07 * k
                out.append(W(xx - 0.005, xx + 0.005, top - 0.14, top - 0.08, z, z + 0.01, IRON, vis=(1,)))
        else:                                                            # barbed head
            out.append(W(x - 0.02, x + 0.02, top - 0.45, top - 0.15, z - 0.02, z + 0.025, IRON, vis=(1,)))
            for k in range(4):
                yy = top - 0.42 + 0.08 * k
                for s in (-1, 1):
                    out.append(xf(W(0.0, 0.09, -0.005, 0.005, -0.004, 0.004, IRON, vis=(1,)), rz=s * 35.0 if s > 0 else
                                  180.0 - 35.0, t=(x, yy, z)))
    wear_all(out, "_w1")
    P.adds(out)
    P.add(W(-0.45, 0.45, 0.0, 2.3, 0.0, 0.08, WEATH, vis=(2,)))
    P.dim("h", 2.18, max(v[1] for s in out for v in s.verts), tol=0.05)
    P.notes.append("the three capture tools (sasumata, tsukubo, sodegarami) on a wall rack (mount wall)%s"
                   % ("; the tsukubo gone" if taken else ""))
    return P


def ridge_ladder():
    """A fire ladder standing on the jishin-ban ridge with a small alarm bell under a tiny roof. Origin = the ridge
    top (place as a front proxy at the fitting's y)."""
    P = LPart("ridge_ladder", budget="furniture", mass=20.0, anchor="floor", flat=True)
    Hl = 2.40
    out = []
    for sx in (-1, 1):
        out.append(pole((sx * 0.28, 0.012, 0.0), (sx * 0.20, Hl, 0.0), 0.03, WEATH, n=5, vis=(1, 2)))
        out.append(pole((sx * 0.28, 0.012, 0.0), (sx * 0.24, 0.9, -0.55), 0.022, WEATH, n=4, vis=(1,)))   # braces
        out.append(pole((sx * 0.28, 0.012, 0.0), (sx * 0.24, 0.9, 0.55), 0.022, WEATH, n=4, vis=(1,)))
    for k in range(1, 8):
        y = 0.30 * k
        hw = 0.28 - 0.08 * y / Hl
        out.append(pole((-hw, y, 0.0), (hw, y, 0.0), 0.016, WEATH, n=4, vis=(1,)))
    yt = Hl
    for sx in (-1, 1):                                                   # the little gable roof
        s = W(0.0, 0.30, -0.012, 0.012, -0.22, 0.22, WEATH)
        s = xf(s, rz=-28.0)
        if sx < 0:
            s = xf(s, ry=180.0)
        out.append(xf(s, t=(0.0, yt + 0.05, 0.0)))
    # FX4 (2026-10-01): the alarm bell was traversed down the outside (inside out) with a flat closing disc: now a
    # hollow casting (inside crown, inner wall facing the cavity, a lip with a flat underside, up the outside)
    bell = lathe([(0.0, -0.045), (0.065, -0.055), (0.088, -0.12), (0.098, -0.205), (0.10, -0.23), (0.12, -0.23),
                  (0.11, -0.20), (0.09, -0.02), (0.0, 0.0)], 10, BRONZE, vis=(1,))
    out.append(xf(bell, t=(0.0, yt - 0.02, 0.0)))
    out.append(pole((0.0, yt - 0.24, 0.0), (0.0, yt - 0.60, 0.0), 0.006, ROPE, n=3, vis=(1,)))
    wear_all(out, "_w1")
    P.adds(out)
    P.dim("h", Hl, Hl, tol=0.01)
    P.notes.append("fire ladder with an alarm bell (hansho) on the guard house ridge: a FRONT proxy at the ridge top")
    return P


def hishaku_rack():
    P = LPart("hishaku_rack", budget="furniture", mass=2.0, anchor="floor", flat=True)
    out = []
    for sx in (-1, 1):
        out.append(pole((sx * 0.30, 0.0, 0.0), (sx * 0.30, 0.62, 0.0), 0.02, BAMBOO, n=5, vis=(1, 2)))
    out.append(pole((-0.34, 0.60, 0.0), (0.34, 0.60, 0.0), 0.015, BAMBOO, n=5, vis=(1, 2)))
    for k, x in enumerate((-0.18, 0.0, 0.18)):
        cup = lathe([(0.0, 0.0), (0.038, 0.0), (0.038, 0.07), (0.033, 0.07), (0.033, 0.006), (0.0, 0.006)], 8,
                    BAMBOO, vis=(1,))
        out.append(xf(cup, rx=-70.0 + 10 * k, t=(x, 0.38, 0.10)))
        out.append(pole((x, 0.40, 0.08), (x, 0.62, -0.04), 0.006, BAMBOO, n=4, vis=(1,)))
    wear_all(out, "_w2")
    P.adds(out)
    P.dim("w", 0.68, 0.68, tol=0.01)
    P.notes.append("bamboo ladles (hishaku) on their rack beside the basin (visual)")
    return P


PROPS = [
    {"id": "jp_f_forge", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_forge", "smithy", "cold", "Forge hearth (hodo), cold", lambda: forge(1.10, 0.90, 0.55)),
        M("jp_f_forge_l", "sword", "cold", "Forge hearth (hodo), swordsmith, cold", lambda: forge(1.30, 1.00, 0.50)),
    ]},
    {"id": "jp_f_fuigo", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_fuigo", "smithy", "intact", "Box bellows (fuigo)", lambda: fuigo(0.45, 1.10, 0.55)),
        M("jp_f_fuigo_l", "sword", "intact", "Box bellows (fuigo), large", lambda: fuigo(0.50, 1.20, 0.60)),
        M("jp_f_fuigo_ab", "smithy", "ransacked", "Box bellows, lid askew, rod pulled out",
          lambda: fuigo(0.45, 1.10, 0.55, ab=True)),
    ]},
    {"id": "jp_f_anvil", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_anvil", "std", "intact", "Anvil in its stump, tongs on the stump", lambda: anvil(0.25, 0.42)),
        M("jp_f_anvil_l", "sword", "intact", "Anvil in its stump, large", lambda: anvil(0.28, 0.40)),
    ]},
    {"id": "jp_f_mizubune", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_mizubune", "std", "dry", "Long quench trough, dry", lambda: mizubune())]},
    {"id": "jp_f_tongs_wall", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_tongs_wall", "std", "intact", "Smith's tongs, hammers and sickles on pegs", lambda: tongs_wall()),
        M("jp_f_tongs_wall_taken", "std", "taken", "Smith's tool wall, half taken", lambda: tongs_wall(True)),
    ]},
    {"id": "jp_f_tsuchioki", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_tsuchioki", "std", "intact", "Clay-coating trough with whetstones", tsuchioki)]},
    {"id": "jp_f_blade_rack", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_blade_rack", "std", "intact", "Rack of bare blades", lambda: blade_rack()),
        M("jp_f_blade_rack_empty", "std", "taken", "Blade rack, emptied", lambda: blade_rack(True)),
    ]},
    {"id": "jp_f_shimenawa_hang", "cat": CAT, "mount": "beam", "models": [
        M("jp_f_shimenawa_hang", "std", "intact", "Straw rope with streamers, hung from a beam", lambda: shimenawa_hang())]},
    {"id": "jp_f_mitsudogu", "cat": CAT, "mount": "wall", "models": [
        M("jp_f_mitsudogu", "std", "intact", "The three capture tools on their rack", lambda: mitsudogu()),
        M("jp_f_mitsudogu_taken", "std", "taken", "Capture tools rack, one gone", lambda: mitsudogu(True)),
    ]},
    {"id": "jp_f_ridge_ladder", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_ridge_ladder", "std", "intact", "Fire ladder with alarm bell on a ridge", ridge_ladder)]},
    {"id": "jp_f_hishaku_rack", "cat": CAT, "mount": "floor", "models": [
        M("jp_f_hishaku_rack", "std", "intact", "Bamboo ladles on their rack", hishaku_rack)]},
]
