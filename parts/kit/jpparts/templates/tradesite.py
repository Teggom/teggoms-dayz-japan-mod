"""The wave-3c-1 trade-site template (W3C1, Phase C wave 3c-1, 2026-10-02): the sake brewery complex (TR03: the
kasane-gura = the o-kura + the mae-gura, the rice-polishing shed), the water mill (TR04), the dyer's workshop with its
sunk indigo vats (TR17), the paper mill (TR21) and their yards (K3's wall kit through templates/dwelling.compound).
Bare shells: every shell lists its fixed-prop spots in info['fittings'] for the furnisher (buildings/w3c1_sets.py).
Research, sizes and every recorded choice: spikes/W3C1/W3C1_NOTES.md.

    M, floors, rooms, info = tradesite.model(kind="okura")

Kinds (kit frame as rural.py: x 0..W along the front, z 0 = front wall line, +z = out, z -D = back, y 0 = grade)
  okura     W 9 x D 4 ken, the large brewery kura (north half of the kasane-gura): okabe walls, black board skirt,
            sangawara, eave 5.40, exposed log truss; earth floor 0.30 on the granite footing; the moto-ba loft over
            the west 2.5 ken (2.85, the kura's open stair); kura doors on both gables; 3 barred windows in the back
            (north) wall + a loft window. The front (south) wall is blind: the mae-gura stands 0.20 off it.
  maegura   W 9 x D 3 ken, the front kura: eave 3.70 (its ridge under the o-kura's eave), the back eave cut short
            (roofs.roof ov=(front, back)) + the gutter / flashing of jp_p_roof_union _gutter against the o-kura;
            araiba + kamaba (one earth floor, a koshiyane steam vent), the koji block (ante-room + the muro behind it:
            two doors in series, mat-lined, ceiled), the kaishoba (raised board room + entrance doma)
  seimai    W 4 x D 2 ken, the rice-polishing shed: board walls on three sides, open front, earth floor
  suisha    W 3 x D 2 ken, the water mill hut: board walls, earth floor, itabuki | thatch; the overshot wheel on the
            right gable (jp_p_mech_waterwheel), its axle through the gable driving 3 vertical pestles (cams + tappets)
            over 3 mortars; a 2-module flume (jp_p_water_flume _run + _head) on trestles feeding the wheel's top
  konya     W 4 x D 3 ken, the indigo dyer: the shop doma along the street (open front), behind it the vat room on a
            raised earth floor (0.30, stone kerb + step) with the four ai-game sunk to the rim round the fire pit;
            sangawara | itabuki; back door to the drying yard
  kamisuki  W 4 x D 2.5 ken, the paper mill: board walls, earth floor, open window bays on the front, a lean-to on the
            right gable over the bark steamer; itabuki | thatch
  compound  plot 'brewery' | 'dyersyard' | 'paperyard' (registered into dwelling.COMPOUNDS)
"""
import math

from ..core import Part, box, prism, hexa, KEN, HALF, POST, KETA_H, DOOR_H
from .. import walls, openings, roofs as R, floors as FL, found, stair as ST, koyagumi as KY, mech
from ..assemble import to_world
from ..shapes import slab, clip_rect, tube
from .rural import Shell, _gable_leanto, _kamado, _r, DOMA, A_, BOARDS_ROUGH
from .civic import fit, trim_lods, koshiyane, open_front, _ext
from .kura import (_okabe, _to_int, _recolour, kura_door, T_WALL, FACE, OKABE_IN, PLASTER_OUT)
from . import dwelling as DW

KINDS = ("okura", "maegura", "seimai", "suisha", "konya", "kamisuki", "compound")
FAM = "sangawara"
FOOT = 0.30                 # the kura footing top = the brewery's earth floors (tataki on the footing course)
OV_K, GOV_K = 0.60, 0.30    # the kura eave (plastered) and verge
GAP_KURA = 0.20             # between the o-kura's south wall face and the mae-gura's back wall face
OV_BACK_M = 0.16            # the mae-gura's short back eave (ends 0.04 short of the o-kura wall face)
LOFT, LOFT_CEIL = 2.85, 2.70
STAIR_W = 1.10
FLR = 0.75                  # the kaishoba's raised boards (0.45 over the 0.30 earth floor)
VAT_Y = 0.30                # the dyer's raised vat-room floor


# ================================================================================================ kura pieces
def _kura_posts(S, W, D, E):
    k = 0
    while k * KEN <= W + 1e-6:
        for z in (0.0, -D):
            S.posts.append((round(k * KEN, 4), z, FOOT, E))
        k += 1
    k = 1
    while k * KEN < D - 1e-6:
        for x in (0.0, W):
            S.posts.append((x, round(-k * KEN, 4), FOOT, E))
        k += 1


def _kura_walls(S, W, D, E, holes, bands=("front", "back"), lower=("front", "back", "left", "right")):
    """Footing, okabe walls (eave walls up under the roof + their wall-head wedge; gables to E + the plaster gable),
    the kura eave bands on `bands`, the black shitami skirt on `lower` (cut round the low openings)."""
    B, F = S.B, S.F
    t = R.PITCH[FAM]
    for side, (a, b), seed in (("front", (-FACE, W + FACE), 1), ("back", (-FACE, W + FACE), 2),
                               ("left", (0.28, D - 0.28), 3), ("right", (0.28, D - 0.28), 4)):
        p = B.P("footing_" + side)
        found.kura_footing(p, a, b, 1, wall_t=T_WALL, seed=seed)
        B.put(p, F[side], 0.0, FOOT, what="found.kura_footing _c1 (%s)" % side)
    _kura_posts(S, W, D, E)
    YE = E - t * (FACE + 0.02) - 0.02
    for side in ("front", "back"):
        _okabe(S, "okabe_" + side, F[side], 0.0, W, FOOT, YE, holes.get(side, []), ext=FACE)
        p = B.P("wall_head_" + side)
        p.add(prism([(YE, -FACE), (YE, FACE), (E - t * FACE - 0.01, FACE), (E + t * FACE - 0.01, -FACE)], "x",
                    -FACE, W + FACE, OKABE_IN, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="wall_head"))
        if side in bands:
            b2 = E - t * (FACE + 0.14) - 0.105
            for (y0_, y1_, pr) in ((b2 - 0.14, b2, 0.14), (b2 - 0.30, b2 - 0.14, 0.07)):
                p.add(box(-FACE - pr, W + FACE + pr, y0_, y1_, FACE, FACE + pr, "wall_shikkui", vis=(1, 2, 3),
                          geo=True, view=True, fire=True, tag="kura_band"))
        B.put(p, F[side], what="kura wall head%s (%s)" % (" + eave bands" if side in bands else "", side))
    for side in ("left", "right"):
        _okabe(S, "okabe_" + side, F[side], FACE, D - FACE, FOOT, E, holes.get(side, []))
        g = B.P("gable_" + side)
        walls.gable(g, D, t, E, "_kura")
        _to_int(g, ("gable_infill",))
        _recolour(g, ("tie_beam",), "wall_shikkui")
        B.put(g, F[side], what="walls.gable _kura (%s)" % side)
        yaw, o = F[side]
        for s in g.transformed(yaw, o).solids:
            if s.tag == "vent_geo":
                b_ = s.bbox()
                S.portals.append(("gable vent %s" % side, (b_[0] - 0.25, b_[1] + 0.25, b_[2] - 0.05, b_[3] + 0.05,
                                                           b_[4] - 0.25, b_[5] + 0.25)))
    # the black board skirt (shitami, wood_kuro) to 1.80 over the footing
    for side in lower:
        L = W if side in ("front", "back") else D
        a, b = (-FACE - 0.03, L + FACE + 0.03) if side in ("front", "back") else (-FACE, L + FACE)
        p = B.P("shitami_" + side)
        ops = [(x0 - 0.02, x1 + 0.02, y0 - FOOT, min(y1, FOOT + 1.80) - FOOT) if (x1 - x0) < 1.0 else
               (x0 - 0.29 - 0.02, x0 - 0.29 + KEN + 0.02, -0.01, 1.81)
               for (x0, x1, y0, y1) in holes.get(side, []) if y0 < FOOT + 1.80]
        sub = B.P("sh")
        walls.wall_run(sub, "shitami", a, b, y0=0.0, y1=1.80, openings=ops, mat="wood_kuro", thick=FACE,
                       internal_posts=False)
        for s in sub.solids:
            if s.tag == "shitami":
                s.vis = {1}
            if s.tag == "shitami_lod":
                s.vis = {2, 3}
        p.merge(sub.transformed(0.0, (0.0, FOOT, 0.0)))
        B.put(p, F[side], what="walls.wall_run shitami _kura (%s)" % side)


def _kura_roof(S, W, D, E, ov, gov=GOV_K, koya=True, members="log"):
    """kirizuma sangawara with the plastered kura eave (soffit, fascia, bargeboards) over the overhangs; with koya the
    log wagoya truss under it (the kura's open interior)."""
    rp = S.B.P("roof_main")
    sls, info_r = R.roof(rp, W, D, "kirizuma", FAM, eave_y=E, ov=ov, gov=gov, soffit=False, courses=3,
                         eave_style="tomoe")
    K = None
    if koya:
        K = KY.koyagumi(rp, W, D, info_r, eave_y=E, members=members, soot=False, joya_posts=False)
    _recolour(rp, ("kawara_fascia", "hafu", "verge_batten", "purlin_end"), "wall_shikkui")
    for sl in sls:
        for pc in sl.pieces:
            for (a, b, c, d) in ((-99, -FACE, -99, 99), (W + FACE, 99, -99, 99), (-FACE, W + FACE, FACE, 99),
                                 (-FACE, W + FACE, -99, -D - FACE)):
                q = clip_rect(pc, a, b, c, d)
                if len(q) >= 3:
                    rp.add(slab(q, lambda x, z, s_=sl: s_.y(x, z, -0.10), lambda x, z, s_=sl: s_.y(x, z, -0.001),
                                "wall_shikkui", vis=(1, 2, 3), tag="kura_soffit"))
    S.H.merge(rp)
    rw = R.ridge_walk(info_r)
    if rw:
        S.H.merge(rw)
    S.log.append("roofs.roof kirizuma %s eave %.2f ov %s (plastered kura eave)%s" % (FAM, E, ov,
                                                                                     " + koyagumi log" if koya else ""))
    return sls, info_r, K


def _kura_door(S, side, dx, y, label, key):
    """A kura doorway (jp_p_open_kura_door _open) on a wall frame at bay dx, floor y (= FOOT), and the cut-granite
    landing + step down to grade outside over a hidden walk ramp (<= 34 deg). Returns the hole rect for the walls."""
    S.door(kura_door("_open"), side, dx, y, label, key)
    fr = S.F[side]
    cx = dx + HALF
    z0r = 0.54
    run = y / math.tan(math.radians(34.0))
    st = S.B.P("kura_step_%s_%d" % (side, int(dx * 100)))
    xa, xb = cx - 0.67, cx + 0.67
    from ..core import rng_for
    from ..shapes import rough_block
    st.add(prism([(y, z0r), (0.0, z0r + run), (0.0, z0r)], "x", xa, xb, "stone_cut", vis=(), geo=True, view=False,
                 fire="granite", tag="ramp"))
    st.road([(xa, y, z0r), (xb, y, z0r), (xb, 0.0, z0r + run), (xa, 0.0, z0r + run)], "stone_ext")
    rng = rng_for("kura_step" + S.H.name + side + str(dx))
    st.add(rough_block(rng, cx - 0.78, cx + 0.78, -0.05, y, FACE, 0.62, "stone_cut", chamfer=0.02, top_jit=0.002,
                       vis=(1, 2, 3), tag="step_slab"))
    st.add(rough_block(rng, cx - 0.70, cx + 0.70, -0.05, y * 0.5, 0.62, 0.95, "stone_cut", chamfer=0.02,
                       top_jit=0.002, vis=(1, 2, 3), tag="step_slab"))
    S.B.put(st, fr, what="kura landing + step (%s)" % side)
    # the door's inner ramp (the 0.15 threshold) is a floor obstacle
    p0 = to_world(fr, dx + 0.29, -0.42)
    p1 = to_world(fr, dx + 1.53, -FACE)
    return (dx + 0.29, dx + 1.53, y, y + 2.15), _r(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]),
                                                     max(p0[1], p1[1]))


def _kura_window(S, side, dx, dy):
    wp = openings.part_kura_window("_slide")
    for s in wp.solids:
        if s.tag in ("surround", "shutter"):
            s.vis = set(s.vis) - {3}
        if s.tag in ("bar", "shutter_track"):
            s.vis = {1}
    S.B.put(wp, S.F[side], dx, dy, what="jp_p_open_kura_window _slide (%s)" % side)
    a0, a1, b0, b1 = _wh(dx, dy)
    p0 = to_world(S.F[side], a0, -0.40)
    p1 = to_world(S.F[side], a1, 0.40)
    S.portals.append(("kura window %s %.2f %.2f" % (side, dx, dy), (min(p0[0], p1[0]), max(p0[0], p1[0]), b0 - 0.02,
                                                                    b1 + 0.02, min(p0[1], p1[1]), max(p0[1], p1[1]))))


def _wh(dx, dy):
    return (dx + HALF / 2 - 0.30, dx + HALF / 2 + 0.30, dy + 1.20, dy + 1.95)


def _plaster_out(H):
    """FB1: every exterior shikkui face takes FP1's aged plaster (the kura template's rule)."""
    for s_ in H.solids:
        if isinstance(s_.mats, str):
            if s_.mats == "wall_shikkui":
                s_.mats = PLASTER_OUT
        elif isinstance(s_.mats, dict):
            s_.mats = {k: (PLASTER_OUT if v == "wall_shikkui" else v) for k, v in s_.mats.items()}
        if s_.fm:
            s_.fm = [PLASTER_OUT if m == "wall_shikkui" else m for m in s_.fm]


def _earth(S, name, x0, x1, z0, z1, y, holes=()):
    """An earth (tataki) floor slab at y on the footing (rect_minus round any holes)."""
    S.B.interior = True
    S.B.merge(FL.doma(name, x0, x1, z0, z1, road=(x0, x1, z0, z1), y=y,
                      holes=holes, mats=FL.MATS_DOMA_EARTH))
    S.B.interior = False


def _kamachi(S, fr, L, floor_y, step_at, doma_name, doma_y):
    """rural.Shell.kamachi for a doma that is not at DOMA (the brewery's earth floors lie at 0.30)."""
    s = S.B.P("kamachi")
    s.add(box(0.0, L, doma_y, floor_y - 0.15, -0.03, 0.03, "wood_sooted", vis=(1, 2), geo=True, view=True, fire=True,
              tag="yukashita_boards"))
    s.add(box(0.0, L, floor_y - 0.15, floor_y, -0.06, 0.06, "wood_interior", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="agari_kamachi"))
    S.B.interior = True
    S.B.put(s, fr)
    for cx in step_at:
        st = S.B.P("step_%d" % int(cx * 100))
        run = found.step(st, cx, "natural", drop=floor_y - doma_y, width=1.04)
        S.B.put(st, fr, 0.0, floor_y, what="jp_p_found_step_natural (kutsunugi + hidden ramp)")
        p0 = to_world(fr, cx - 0.54, 0.0)
        p1 = to_world(fr, cx + 0.54, run + 0.06)
        S.obst.append((doma_name, _r(p0[0], p1[0], p0[1], p1[1])))
    S.B.interior = False


def _mat_faces(part, mat, side_fn):
    """Re-material the faces of a part's solids for which side_fn(face centre, normal) is true (the koji-muro's straw
    lining on the inner faces of its walls)."""
    for s in part.solids:
        if not s.fm:
            continue
        nf = []
        for fi, m in enumerate(s.fm):
            pts = s.face_points(fi)
            c = tuple(sum(p[k] for p in pts) / len(pts) for k in range(3))
            nf.append(mat if side_fn(c, s.fn[fi]) else m)
        s.fm = nf


# ================================================================================================ TR03 o-kura
def okura(name=None, wear="_w1"):
    W, D, E = 9 * KEN, 4 * KEN, 5.40
    S = Shell(name or "jp_sakagura_okura", W, D, [2, 3], "sake brewery: the large kura (o-kura) of the kasane-gura",
              wear)
    B = S.B
    xi0, xi1, zi0, zi1 = FACE, W - FACE, -D + FACE, -FACE
    LX = 3.25 * KEN                                  # the loft (moto-ba) over x 0..LX
    XF = 5.5 * KEN                                   # fermentation | funaba (one open floor, two fitting zones)
    holes = {"front": [], "back": [], "left": [], "right": []}
    # doors on both gables (bay 1.5..2.5 ken, parking over 2.5..3.5 inside)
    hl, ol = _kura_door(S, "left", 1.5 * KEN, FOOT, "Kura door (west gable: the starter end)", "west")
    hr, orr = _kura_door(S, "right", 1.5 * KEN, FOOT, "Kura door (east gable: the press end)", "east")
    holes["left"].append(hl)
    holes["right"].append(hr)
    S.obst.append(("moto", ol))
    S.obst.append(("kura", orr))
    # windows: three in the back (north) wall (lx = W - x), one in the west gable at the loft
    wins = [("back", 1.0 * KEN, FOOT + 0.60), ("back", 3.5 * KEN, FOOT + 0.60), ("back", 5.5 * KEN, FOOT + 0.60),
            ("left", D / 2 - HALF / 2 + KEN, LOFT)]
    for (sd, dx, dy) in wins:
        holes[sd].append(_wh(dx, dy))
    _kura_walls(S, W, D, E, holes, bands=("back",), lower=("back", "left", "right", "front"))
    for (sd, dx, dy) in wins:
        _kura_window(S, sd, dx, dy)
    sls, info_r, K = _kura_roof(S, W, D, E, OV_K)
    # floors: the earth floor on the footing; the loft (moto-ba) over the west end, reached by the kura's open stair
    # along the back wall (rising +x, through a well cut in the loft)
    _earth(S, "floor", xi0, xi1, zi0, zi1, FOOT)
    rise = LOFT - FOOT
    stp = Part("stair_okura", "", "")
    SS = ST.stair(stp, STAIR_W, rise, "open")
    srun = SS["run"]
    x_foot, oz = 1.15, zi0
    B.interior = True
    B.merge(stp.transformed(180.0, (x_foot, FOOT, oz), mirror=True))
    wx0, wx1, wz0, wz1 = ST.well_rect(srun, STAIR_W, rise)
    well = (x_foot + wx0, x_foot + wx1, zi0, oz - wz0)
    B.merge(FL.loft("loft", xi0, LX, zi0, zi1, LOFT_CEIL, LOFT, walkable=True,
                    holes=[{"rect": well, "kind": "stair", "open": "x1", "wall": "z0"}], hole_fn=ST.well_fn()))
    # the loft's open edge (x = LX): a girder on three posts (on stones) + a guard rail
    lp = B.P("loft_edge")
    lp.add(box(LX - 0.12, LX + 0.02, LOFT_CEIL - 0.24, LOFT_CEIL, zi0, zi1, "wood_weathered", vis=(1, 2, 3),
               geo=True, view=True, fire=True, tag="loft_girder"))
    for k in (1, 2, 3):
        z = -k * KEN
        lp.add(box(LX - 0.10, LX + 0.02, FOOT, LOFT_CEIL - 0.24, z - 0.06, z + 0.06, "wood_weathered", vis=(1, 2, 3),
                   geo=True, view=True, fire=True, tag="loft_post"))
        S.obst.append(("moto", _r(LX - 0.25, LX + 0.17, z - 0.20, z + 0.20)))
        S.obst.append(("kura", _r(LX - 0.25, LX + 0.17, z - 0.20, z + 0.20)))
    for (z0_, z1_) in ((zi0 + 0.02, zi1 - 0.02),):
        lp.add(box(LX - 0.07, LX - 0.01, LOFT + 0.80, LOFT + 0.88, z0_, z1_, "wood_weathered", vis=(1, 2), geo=True,
                   view=True, fire=True, tag="loft_rail"))
        lp.add(box(LX - 0.07, LX - 0.01, LOFT + 0.40, LOFT + 0.46, z0_, z1_, "wood_weathered", vis=(1,), geo=True,
                   view=True, fire=True, tag="loft_rail"))
        for k in range(5):
            z = z0_ + 0.05 + k * (z1_ - z0_ - 0.10) / 4
            lp.add(box(LX - 0.08, LX, LOFT, LOFT + 0.88, z - 0.04, z + 0.04, "wood_weathered", vis=(1, 2), geo=True,
                       view=True, fire=True, tag="loft_rail_post"))
    B.put(lp, (0.0, (0.0, 0.0, 0.0)), what="loft edge: girder, posts, rail")
    B.interior = False
    S.obst.append(("moto", _r(x_foot - 0.05, x_foot + srun + 0.05, zi0, oz + STAIR_W + 0.06)))
    S.obst.append(("loft", _r(well[0] - 0.10, well[1] + 0.10, zi0, well[3] + 0.10)))
    stair_info = {"foot": (x_foot, oz), "run": srun, "width": STAIR_W, "y_low": FOOT, "y_up": LOFT, "well": well}
    # fittings: the four big tubs (two rows), the press along the north wall at the east end, the starter tubs
    zt_n, zt_s = zi0 + 0.15 + 0.91, zi1 - 0.15 - 0.91
    tubs = [(LX + 1.08, zt_n), (LX + 3.02, zt_n), (LX + 1.08, zt_s), (LX + 3.02, zt_s)]
    for k, (x, z) in enumerate(tubs):
        fit(S, "tub", "kura", centre=(x, z), size=(1.95, 1.95), yaw=0.0,
            note="a big fermentation tub (shikomi-oke, 1.82 x 1.70) on the earth floor (#%d)" % (k + 1))
    fit(S, "press", "kura", rect=(W - FACE - 6.20, W - FACE - 0.06, zi0 + 0.05, zi0 + 1.65), obstacle=True,
        note="the lever press (fune + tenbin beam + stones): the box head and posts at the east end, the beam west")
    fit(S, "casks", "kura", rect=(XF + 0.40, W - 2.6, zi1 - 0.95, zi1 - 0.05), obstacle=False,
        note="casks and tubs along the south wall of the press bay")
    fit(S, "starter", "moto", rect=(xi0 + 0.10, LX - 0.40, zi1 - 1.6, zi1 - 0.10), obstacle=False,
        note="starter tubs and the stirring poles under the loft")
    fit(S, "moto_loft", "loft", rect=(xi0 + 0.20, LX - 0.30, -D / 2 - 1.0, zi1 - 0.20), obstacle=False,
        note="the moto-ba upstairs: shallow starter tubs (hangiri) stacked and set out")
    S.place_windows()
    S.room("moto", "storage", "earth", FOOT, (xi0, LX - 0.13, zi0, zi1), [S.dn["west"]],
           "under the loft: the starter end, the stair up (west door)", enclosed=False)
    S.room("kura", "storage", "earth", FOOT, (LX + 0.03, xi1, zi0, zi1), [S.dn["east"]],
           "the brewing floor: four big tubs in two rows (west), the press bay (funaba) with the lever press, casks "
           "(east door)", enclosed=False)
    S.room("loft", "storage", "boards", LOFT, (xi0, LX - 0.08, zi0, zi1), [],
           "the moto-ba loft (the yeast-starter work; G1-5: a kura loft by stair)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "okura"}, "levels": {"floor": FOOT, "loft": LOFT, "eave": E},
                        "koyagumi": K["counts"] if K else {}, "stair": stair_info, "stairwell": well})
    _plaster_out(H)
    return H, info


# ================================================================================================ TR03 mae-gura
def maegura(name=None, wear="_w1"):
    W, D, E = 9 * KEN, 3 * KEN, 3.70
    S = Shell(name or "jp_sakagura_maegura", W, D, [2, 3], "sake brewery: the front kura (mae-gura) of the kasane-gura",
              wear)
    B = S.B
    xi0, xi1, zi0, zi1 = FACE, W - FACE, -D + FACE, -FACE
    XK, XK1, XS = 5 * KEN, 7 * KEN, 7 * KEN          # koji block x 5..7 ken; kaishoba x 7..9 ken
    ZM = -1.5 * KEN                                    # ante-room | muro
    ZE = -1.0 * KEN                                    # kaishoba doma | raised room
    holes = {"front": [], "back": [], "left": [], "right": []}
    h1, o1 = _kura_door(S, "front", 0.5 * KEN, FOOT, "Kura door (araiba)", "araiba")
    h2, o2 = _kura_door(S, "front", 2.5 * KEN, FOOT, "Kura door (kamaba)", "kamaba")
    h3, o3 = _kura_door(S, "front", 7.0 * KEN, FOOT, "Kura door (kaishoba)", "kaisho")
    holes["front"] += [h1, h2, h3]
    S.obst += [("kama", o1), ("kama", o2), ("kaidoma", o3)]
    wins = [("left", 1.0 * KEN, FOOT + 0.20), ("right", 1.5 * KEN, FOOT + 0.20)]
    for (sd, dx, dy) in wins:
        holes[sd].append(_wh(dx, dy))
    _kura_walls(S, W, D, E, holes, bands=("front",), lower=("front", "left", "right"))
    for (sd, dx, dy) in wins:
        _kura_window(S, sd, dx, dy)
    sls, info_r, K = _kura_roof(S, W, D, E, (0.90, OV_BACK_M))
    koshiyane(S, 3.25 * KEN, KEN, info_r, E, D, FAM)
    # the roof union: the gutter on brackets under the short back eave, against the o-kura's wall, and the slot
    # between the two kura closed at both gable ends
    t = R.PITCH[FAM]
    y_lip = E - t * OV_BACK_M - 0.13
    g = B.P("roof_union")
    zw = -D - FACE - GAP_KURA                            # the o-kura's wall face (kit z)
    gi = mech.gutter(g, W + 2 * FACE, y_lip, w=GAP_KURA - 0.03, depth=0.10, gap=0.012, flash_h=0.30, downpipe="x1")
    B.put(g, (0.0, (-FACE, 0.0, zw)), what="jp_p_roof_union _gutter (the kasane-gura join)")
    for xe in (-FACE, W + FACE - 0.03):
        g2 = B.P("slot_end_%d" % int(xe * 100))
        g2.add(box(xe, xe + 0.03, FOOT, y_lip - 0.13, zw + 0.004, -D - FACE - 0.004, "wood_kuro", vis=(1, 2, 3),
                   geo=True, view=True, fire=True, tag="slot_board"))
        B.put(g2, (0.0, (0.0, 0.0, 0.0)), what="the slot between the kura closed at the gable end")
    # floors: one earth floor at 0.30 through araiba + kamaba, the koji block, the kaishoba doma; the raised boards
    _earth(S, "floor_kama", xi0, XK - 0.06, zi0, zi1, FOOT)
    _earth(S, "floor_mae", XK + 0.06, XK1 - 0.06, ZM + 0.06, zi1, FOOT)
    _earth(S, "floor_muro", XK + 0.06, XK1 - 0.06, zi0, ZM - 0.06, FOOT)
    _earth(S, "floor_kaidoma", XS + 0.06, xi1, ZE + 0.06, zi1, FOOT)
    _earth(S, "floor_under_kaisho", XS + 0.06, xi1, zi0, ZE + 0.06, FOOT - 0.01)
    B.interior = True
    B.merge(FL.boards("kaisho", XS + 0.06, xi1, zi0, ZE - 0.06, FLR, mats=FL.MATS_BOARDS_B1))
    B.interior = False
    _kamachi(S, (0.0, (XS, 0.0, ZE)), xi1 - XS, FLR, [0.5 * KEN], "kaidoma", FOOT)
    # partitions: x = XK (kamaba | koji block, with the ante-room door), x = XK1 (koji block | kaishoba, solid),
    # z = ZM (ante-room | muro, with the muro door), z = ZE x XS..W (the kaishoba's kamachi line: open)
    PT = FOOT + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F1 = (90.0, (XK, 0.0, -D))
    S.wall_line((F1, D, "part_koji_w"), [(0.0, D, FOOT)], PT, [(1.5 * KEN, 2.5 * KEN, FOOT, FOOT + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(1.5 * KEN, 2.5 * KEN))
    S.door(openings.part_itado("_single"), F1, 1.5 * KEN, FOOT, "Kamaba -> koji ante-room (first door)", "mae")
    F2 = (90.0, (XK1, 0.0, -D))
    S.wall_line((F2, D, "part_koji_e"), [(0.0, D, FOOT)], PT, (), finish="nakanuri", grime=False, interior="both")
    F3 = (0.0, (XK, 0.0, ZM))
    S.wall_line((F3, XK1 - XK, "part_muro"), [(0.0, XK1 - XK, FOOT)], PT,
                [(0.5 * KEN, 1.5 * KEN, FOOT, FOOT + 2.0, "door")], finish="nakanuri", grime=False, interior="both",
                nodes_extra=(0.5 * KEN, 1.5 * KEN))
    S.door(openings.part_itado("_single"), F3, 0.5 * KEN, FOOT, "Ante-room -> koji-muro (second door)", "muro")
    B.interior = False
    for (fr, L, nm) in ((F1, D, "head_koji_w"), (F2, D, "head_koji_e")):
        S.head_beam(fr, L, PT, nm)
    # the koji block's ceiling (the muro's insulated ceiling + the ante-room), at the partition tops
    B.interior = True
    B.merge(FL.loft("koji_ceil", XK + 0.065, XK1 - 0.065, zi0, zi1, PT - 0.10, PT + 0.05, walkable=False))
    B.interior = False
    # the muro's straw lining: every face inside the muro (walls + ceiling underside) takes straw mats
    mx0, mx1, mz0, mz1 = XK + 0.06, XK1 - 0.06, zi0, ZM - 0.06
    lining = []
    for s in S.H.solids:
        b = s.bbox()
        if b[1] < mx0 - 0.3 or b[0] > mx1 + 0.3 or b[5] < mz0 - 0.3 or b[4] > mz1 + 0.3 or not s.fm:
            continue
        if s.tag in ("infill", "kokabe", "okabe", "floor_loft_under", "loft_under", "ceiling", "gable_infill") or \
                s.tag.startswith("loft"):
            lining.append(s)
    lp = Part("lining", "", "")
    lp.solids = lining

    def inside(c, n):
        if not (mx0 - 0.10 <= c[0] <= mx1 + 0.10 and mz0 - 0.10 <= c[2] <= mz1 + 0.10 and FOOT < c[1] < PT + 0.2):
            return False
        cx, cz = (mx0 + mx1) / 2, (mz0 + mz1) / 2
        # a face looks into the muro when its normal points towards the room's centre (or down, for the ceiling)
        return (n[0] * (cx - c[0]) + n[2] * (cz - c[2]) > 0.05) or n[1] < -0.7
    _mat_faces(lp, "straw_mushiro", inside)
    # fittings
    hx, hz = 3.75 * KEN, zi0 + 0.06 + 1.00
    fit(S, "hearth", "kama", centre=(hx, hz), size=(2.30, 2.10), yaw=0.0,
        note="the kamaba hearth: clay-and-stone kamado with the iron cauldron and the cedar koshiki on it, under the "
             "steam vent (specialty prop, fire mouth to the front)")
    fit(S, "wash", "kama", rect=(xi0 + 0.15, 2.0 * KEN - 0.2, zi0 + 0.10, zi0 + 1.40), obstacle=False,
        note="the araiba: washing tubs and the draining trough along the back wall")
    fit(S, "toko", "muro", centre=((XK + XK1) / 2, (mz0 + mz1) / 2), size=(1.85, 1.25), yaw=0.0, obstacle=False,
        note="the koji bed (toko) in the middle of the muro, cloths over it")
    fit(S, "koji_shelf", "muro", rect=(mx0 + 0.02, mx1 - 0.02, mz0 + 0.02, mz0 + 0.45), obstacle=False,
        note="shelves of koji trays (koji-buta) along the muro's back wall")
    fit(S, "mae", "mae", rect=(XK + 0.25, XK1 - 0.25, ZM + 0.30, zi1 - 0.20), obstacle=False,
        note="the ante-room: trays, cloths, the warming jar")
    S.place_windows()
    S.room("kama", "kitchen", "earth", FOOT, (xi0, XK - 0.06, zi0, zi1), [S.dn["araiba"], S.dn["kamaba"], S.dn["mae"]],
           "araiba + kamaba: washing tubs, the great hearth with the steamer under the steam vent")
    S.room("mae", "storage", "earth", FOOT, (XK + 0.06, XK1 - 0.06, ZM + 0.06, zi1), [S.dn["mae"], S.dn["muro"]],
           "the koji ante-room (between the two doors)")
    S.room("muro", "storage", "earth", FOOT, (mx0, mx1, mz0, mz1), [S.dn["muro"]],
           "the koji-muro: straw-lined, ceiled, the koji bed and the tray shelves")
    S.room("kaidoma", "doma", "earth", FOOT, (XS + 0.06, xi1, ZE + 0.06, zi1), [S.dn["kaisho"]],
           "the kaishoba's entrance doma")
    S.room("kaisho", "living", "boards", FLR, (XS + 0.06, xi1, zi0, ZE - 0.06), [],
           "the kaishoba: the brewers' rest room (raised boards)")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "maegura"}, "levels": {"floor": FOOT, "kaisho": FLR, "eave": E},
                        "koyagumi": K["counts"] if K else {}, "union": {"gutter_lip": y_lip, "wall_face_z": zw}})
    _plaster_out(H)
    return H, info


# ================================================================================================ TR03 rice-polishing shed
def seimai(name=None, wear="_w2"):
    """The seimai-goya: board walls back + both ends, the front open (posts + head beam), earth floor; four
    foot-treadle mortars side by side, their levers running front to back (the mortars at the front)."""
    W, D, E = 4 * KEN, 2 * KEN, 3.20
    fam = "itabuki"
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_sakagura_seimai", W, D, [1, 2], "sake brewery: the rice-polishing shed (seimai-goya)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    open_front(S, 0.0, W, YT)
    S.wall_line("back", [(0.0, W, DOMA)], YT, (), **bw)
    for side in ("left", "right"):
        S.wall_line(side, [(0.0, D, DOMA)], YG, (), **bw)
        S.gable(side, D, t, E, "_board")
    B.interior = True
    B.merge(FL.doma("floor", -0.06, W + 0.06, -D, 0.30, road=(A_, W - A_, -D + A_, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    for k in range(4):
        x = (k + 0.5) * KEN
        fit(S, "karausu", "floor", rect=(x - 0.42, x + 0.42, -D + A_ + 0.10, -0.25), obstacle=False,
            note="a foot-treadle mortar (kara-usu): the mortar at the front, the lever and the treader's end at the "
                 "back (#%d)" % (k + 1))
    S.place_windows()
    S.room("floor", "storage", "earth", DOMA, (A_, W - A_, -D + A_, -0.15), [],
           "the polishing shed: four treadle mortars in a row, rice bales", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "seimai"}, "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"]},
                       exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR04 water mill
def _stamps(S, xs, zA, yA, zP):
    """The mill's works inside the hut: on the axle (y yA, z zA) four cams per pestle; vertical pestles (0.15 sq) at
    z zP in a guide frame (two pairs of rails on four posts) over mortars set in the floor with a 0.25 rim."""
    p = S.B.P("stamps")
    W_ = "wood_weathered"
    DK = "wood_sooted"
    for x in xs:
        # the pestle with its iron-shod foot and the tappet board (hago-ita) towards the axle
        p.add(box(x - 0.075, x + 0.075, DOMA + 0.12, 2.92, zP - 0.075, zP + 0.075, W_, vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="pestle", grain="long"))
        p.add(box(x - 0.08, x + 0.08, DOMA + 0.10, DOMA + 0.30, zP - 0.08, zP + 0.08, "metal_iron", vis=(1,),
                  tag="pestle_shoe"))
        sg = 1.0 if zA > zP else -1.0
        p.add(box(x - 0.03, x + 0.03, yA - 0.42, yA - 0.30, zP + sg * 0.075, zP + sg * 0.28, W_, vis=(1, 2), geo=True,
                  view=True, fire=True, tag="tappet"))
        # four cams (nade-bo) through the axle
        for k in range(4):
            a = math.radians(25.0 + 90.0 * k)
            r0, r1 = 0.10, 0.40
            p0 = (x, yA + r0 * math.sin(a), zA + r0 * math.cos(a))
            p1 = (x, yA + r1 * math.sin(a), zA + r1 * math.cos(a))
            p.add(tube(p0, p1, 0.035, DK, n=4, vis=(1, 2), tag="cam"))
        # the mortar (usu): a stone ring with a 0.25 rim over the floor, bran at the bottom
        for k in range(10):
            a0, a1 = 2 * math.pi * k / 10, 2 * math.pi * (k + 1) / 10
            q = [(x + 0.30 * math.cos(a0), zP + 0.30 * math.sin(a0)), (x + 0.30 * math.cos(a1), zP + 0.30 * math.sin(a1)),
                 (x + 0.18 * math.cos(a1), zP + 0.18 * math.sin(a1)), (x + 0.18 * math.cos(a0), zP + 0.18 * math.sin(a0))]
            p.add(prism(q, "y", DOMA, DOMA + 0.25, "stone_cut", vis=(1, 2), tag="mortar"))
        ring_o = [(x + 0.30 * math.cos(2 * math.pi * k / 10), zP + 0.30 * math.sin(2 * math.pi * k / 10))
                  for k in range(10)]
        p.add(prism(ring_o, "y", DOMA, DOMA + 0.25, "stone_cut", vis=(3,), geo=True, view=True, fire=True,
                    tag="mortar_geo"))
        p.add(prism([(x + 0.19 * math.cos(2 * math.pi * k / 10), zP + 0.19 * math.sin(2 * math.pi * k / 10))
                     for k in range(10)], "y", DOMA, DOMA + 0.09, "food_rice", vis=(1,), tag="mortar_bran"))
    # the guide frame: posts at both ends, rails front and back of the pestles at two heights
    xa, xb = xs[0] - 0.55, xs[-1] + 0.55
    for xx in (xa, xb):
        for dz in (-0.16, 0.16):
            p.add(box(xx - 0.06, xx + 0.06, 0.0, 2.92, zP + dz - 0.06, zP + dz + 0.06, W_, vis=(1, 2, 3), geo=True,
                      view=True, fire=True, tag="guide_post"))
    for yy in (1.25, 2.62):
        for dz in (-0.16, 0.16):
            p.add(box(xa - 0.06, xb + 0.06, yy, yy + 0.12, zP + dz - 0.04, zP + dz + 0.04, W_, vis=(1, 2), geo=True,
                      view=True, fire=True, tag="guide_rail"))
    p.add(box(xa - 0.06, xb + 0.06, 2.92, 3.02, zP - 0.22, zP + 0.22, W_, vis=(1, 2), geo=True, view=True, fire=True,
              tag="guide_cap"))
    S.B.interior = True
    S.B.put(p, (0.0, (0.0, 0.0, 0.0)), what="the stamp mill: cams on the axle, 3 pestles in their guide frame, mortars")
    S.B.interior = False
    for x in xs:
        S.obst.append(("floor", _r(x - 0.42, x + 0.42, zP - 0.42, zP + 0.42)))
    S.obst.append(("floor", _r(xa - 0.12, xb + 0.12, zP - 0.26, zP + 0.26)))


def suisha(name=None, roof="itabuki", wear="_w2"):
    fam = roof
    W, D = 3 * KEN, 2 * KEN
    E = 3.60
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_suisha_goya", W, D, [1, 2], "water mill hut (suisha-goya, TR04), %s" % fam, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=0.90 if fam == "thatch" else None, soot=False,
                            ridge="bamboo", members="log")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    yA, zA = 2.30, -1.0                       # the axle: height (clear head room under it), kit z
    S.wall_line("front", [(0.0, W, DOMA)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door"),
                                                (2.0 * KEN, 2.5 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(2.5 * KEN,), **bw)
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Mill door", "front")
    S.window(openings.part_tsukiage("_board"), "front", 2.0 * KEN, DOMA, "Window (front, push-up)")
    S.wall_line("back", [(0.0, W, DOMA)], YT, [(1.0 * KEN, 1.5 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(1.0 * KEN, 1.5 * KEN), **bw)
    S.window(openings.part_tsukiage("_board"), "back", 1.0 * KEN, DOMA, "Window (back, push-up)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(0.5 * KEN, 1.0 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, DOMA, "Window (end)")
    S.wall_line("right", [(0.0, D, DOMA)], YG, (), **bw)        # the axle runs through the boards (a fitted hole)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board", thatch=(fam == "thatch"))
    B.interior = True
    B.merge(FL.doma("floor", 0.0, W, -D, 0.0, road=(A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    # the wheel outside the right gable + its axle into the hut, the inner bearing post
    gov = R.GABLE_OV[fam]
    wp = B.P("wheel")
    xo = W + 0.10
    wi = mech.waterwheel(wp, y_axle=yA, gap=gov + 0.12, inner=xo - 0.45, outer=0.45)
    B.put(wp, (0.0, (xo, 0.0, zA)), what="jp_p_mech_waterwheel _overshot (stopped)")
    ib = B.P("inner_bearing")
    ib.add(box(0.33, 0.57, 0.0, yA - 0.14, zA - 0.12, zA + 0.12, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
               fire=True, tag="bearing_post"))
    ib.add(box(0.30, 0.60, yA - 0.26, yA - 0.14, zA - 0.20, zA + 0.20, "wood_sooted", vis=(1, 2), geo=True, view=True,
               fire=True, tag="bearing_block"))
    B.interior = True
    B.put(ib, (0.0, (0.0, 0.0, 0.0)), what="the inner bearing post")
    B.interior = False
    S.obst.append(("floor", _r(0.20, 0.70, zA - 0.30, zA + 0.30)))
    # the stamps
    zP = zA - 0.42
    xs = (1.45, 2.55, 3.65)
    _stamps(S, xs, zA, yA, zP)
    # the flume: two modules on trestles along +z from over the wheel's top, the head (sluice shut) at the far end
    xw = xo + wi["centre"][0]
    bed = yA + wi["R"] + 0.12
    z0 = zA + 0.25
    L = 1.5 * KEN
    f1 = B.P("flume_run")
    mech.flume(f1, L, bed, trestle_at=[L * 0.62])
    B.put(f1, (90.0, (xw, 0.0, z0)), what="jp_p_water_flume _run")
    f2 = B.P("flume_head")
    mech.flume(f2, L, bed, trestle_at=[L * 0.45], head=True)
    B.put(f2, (-90.0, (xw, 0.0, z0 + 2 * L)), what="jp_p_water_flume _head (sluice shut)")
    # fittings: the hand quern (the stone mill), sacks and sieves
    fit(S, "quern", "floor", centre=(0.95, -0.55), size=(0.70, 0.70), yaw=0.0,
        note="the stone hand mill (ishi-usu) on the floor by the door: grinding by hand (gears: late Edo, W3C1_NOTES)")
    fit(S, "sacks", "floor", rect=(W - 1.30, W - A_ - 0.05, -0.75, -A_ - 0.05), obstacle=False,
        note="rice bales and grain sacks by the front wall")
    S.place_windows()
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -A_), [S.dn["front"]],
           "the mill floor: three pestles on the wheel's cam shaft over their mortars, the hand quern")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "suisha", "roof": roof}, "levels": {"doma": DOMA, "eave": E, "axle": yA},
                        "koyagumi": K["counts"], "wheel": {"centre": [xo + wi["centre"][0], yA, zA], "R": wi["R"]}},
                       exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR17 dyer
def _vat_bank(S, cx, cz, y, lids=(0, 3)):
    """The four indigo vats (ai-game) sunk to the rim in the raised earth floor round the fire pit (hi-tsubo): a
    2.30 square bank centred (cx, cz), floor top y. Each vat: a 0.80 board frame flush with the floor, the stoneware
    jar's rim (mouth 0.62) inside it, clay fillets in the corners, the dye surface 0.15 under the rim (dark, a
    coppery skin); `lids`: vats covered with their wooden lids. Returns the bank rect (for the floor's hole)."""
    p = S.B.P("vat_bank")
    from ..core import rng_for
    rng = rng_for(S.H.name + "vats")
    hb = 1.15
    jar_c = [(cx + sx * 0.75, cz + sz * 0.75) for sz in (-1, 1) for sx in (-1, 1)]
    n = 12
    rm, rr = 0.31, 0.36                      # mouth (inner) and rim (outer) radius
    yr = y + 0.02                            # rim top, 2 cm proud of the floor
    ys = yr - 0.15                           # dye surface
    cells = [(jx - 0.40, jx + 0.40, jz - 0.40, jz + 0.40) for (jx, jz) in jar_c]
    pit = (cx - 0.225, cx + 0.225, cz - 0.225, cz + 0.225)
    for (a, b, c, d) in FL.rect_minus((cx - hb, cx + hb, cz - hb, cz + hb), cells + [pit]):
        p.add(box(a, b, -0.10, y, c, d, {"top": "ground_doma_earth", "default": "stone_cut"}, vis=(1, 2, 3), geo=True,
                  view=True, fire="dirt", tag="bank_earth"))
        p.road([(a, y, c), (b, y, c), (b, y, d), (a, y, d)], "doma")
    for k, (jx, jz) in enumerate(jar_c):
        # board frame (kame-buchi) round the cell, 1 cm over the floor
        for (a, b, c, d) in ((jx - 0.40, jx + 0.40, jz - 0.40, jz - 0.33), (jx - 0.40, jx + 0.40, jz + 0.33, jz + 0.40),
                             (jx - 0.40, jx - 0.33, jz - 0.33, jz + 0.33), (jx + 0.33, jx + 0.40, jz - 0.33, jz + 0.33)):
            p.add(box(a, b, y - 0.10, y + 0.01, c, d, "wood_sooted", vis=(1, 2, 3), geo=True, view=True, fire=True,
                      tag="vat_frame", grain="long"))
            p.road([(a, y + 0.01, c), (b, y + 0.01, c), (b, y + 0.01, d), (a, y + 0.01, d)], "boards")
        # clay fillets: fans from the frame's inner corners to the rim circle (convex triangles)
        for (qx, qz, a0) in ((0.33, 0.33, 0.0), (-0.33, 0.33, 90.0), (-0.33, -0.33, 180.0), (0.33, -0.33, 270.0)):
            for j in range(3):
                b0, b1 = math.radians(a0 + 30.0 * j), math.radians(a0 + 30.0 * (j + 1))
                tri = [(jx + qx, jz + qz), (jx + rr * math.cos(b0), jz + rr * math.sin(b0)),
                       (jx + rr * math.cos(b1), jz + rr * math.sin(b1))]
                p.add(prism(tri, "y", y - 0.10, y - 0.005, "wall_nakanuri_int", vis=(1,), tag="vat_fillet"))
        # the jar: rim ring (n segments) down to the dye
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            q = [(jx + rr * math.cos(a0), jz + rr * math.sin(a0)), (jx + rr * math.cos(a1), jz + rr * math.sin(a1)),
                 (jx + rm * math.cos(a1), jz + rm * math.sin(a1)), (jx + rm * math.cos(a0), jz + rm * math.sin(a0))]
            p.add(prism(q, "y", ys - 0.03, yr, "ceramic_stoneware_dark", vis=(1,), tag="vat_rim"))
        # far LODs: the cell as one dark square inside its frame
        p.add(box(jx - 0.33, jx + 0.33, ys - 0.03, ys + 0.01, jz - 0.33, jz + 0.33, "lacquer_black", vis=(2, 3),
                  tag="vat_lod"))
        disc = [(jx + rm * math.cos(2 * math.pi * i / n), jz + rm * math.sin(2 * math.pi * i / n)) for i in range(n)]
        p.add(prism(disc, "y", ys - 0.03, ys, "lacquer_black", vis=(1,), geo=True, view=True, fire="water",
                    tag="dye"))
        # the coppery skin (ai-bana, dried) on part of the surface
        sk = [(jx + 0.6 * rm * math.cos(2 * math.pi * i / 8 + 0.4) + 0.05, jz + 0.5 * rm * math.sin(2 * math.pi * i / 8))
              for i in range(8)]
        p.add(prism(sk, "y", ys, ys + 0.004, "textile_cotton_indigo", vis=(1,), tag="dye_skin"))
        if k in lids:
            lid = [(jx + 0.345 * math.cos(2 * math.pi * i / 12), jz + 0.345 * math.sin(2 * math.pi * i / 12))
                   for i in range(12)]
            p.add(prism(lid, "y", yr, yr + 0.03, "wood_weathered", vis=(1, 2), geo=True, view=True, fire=True,
                        tag="vat_lid"))
            p.add(box(jx - 0.05, jx + 0.05, yr + 0.03, yr + 0.07, jz - 0.25, jz + 0.25, "wood_weathered", vis=(1,),
                      tag="vat_lid_grip"))
        S.obst.append(("aiba", _r(jx - 0.42, jx + 0.42, jz - 0.42, jz + 0.42)))
    # the fire pit: clay walls, ash at the bottom (cold), a few charred sticks; a board cover half over it
    (a, b, c, d) = pit
    ya = y - 0.25
    for (a0, a1, b0, b1) in ((a, a + 0.04, c, d), (b - 0.04, b, c, d), (a + 0.04, b - 0.04, c, c + 0.04),
                             (a + 0.04, b - 0.04, d - 0.04, d)):
        p.add(box(a0, a1, ya, y, b0, b1, "wall_nakanuri_int", vis=(1, 2), geo=True, view=True, fire="dirt",
                  tag="pit_wall"))
    p.add(box(a + 0.04, b - 0.04, -0.10, ya, c + 0.04, d - 0.04, {"top": "ground_ash", "default": "wall_arakabe"},
              vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag="pit_ash"))
    p.road([(a + 0.04, ya, c + 0.04), (b - 0.04, ya, c + 0.04), (b - 0.04, ya, d - 0.04), (a + 0.04, ya, d - 0.04)],
           "doma")
    for j in range(3):
        L = rng.uniform(0.18, 0.28)
        aa = rng.uniform(0, math.pi)
        px, pz = cx + rng.uniform(-0.08, 0.08), cz + rng.uniform(-0.08, 0.08)
        p.add(tube((px - L / 2 * math.cos(aa), ya + 0.03, pz - L / 2 * math.sin(aa)),
                   (px + L / 2 * math.cos(aa), ya + 0.03, pz + L / 2 * math.sin(aa)), 0.025, "wood_sooted", n=5,
                   vis=(1,), tag="firewood"))
    p.add(box(a - 0.02, cx + 0.05, y, y + 0.025, c - 0.02, d + 0.02, "wood_sooted", vis=(1, 2), tag="pit_cover"))
    S.B.interior = True
    S.B.put(p, (0.0, (0.0, 0.0, 0.0)), what="four sunk indigo vats round the fire pit (shell floor pits)")
    S.B.interior = False
    S.obst.append(("aiba", _r(a - 0.05, b + 0.05, c - 0.05, d + 0.05)))
    return (cx - hb, cx + hb, cz - hb, cz + hb)


def konya(name=None, roof="sangawara", wear="_w2"):
    fam = roof
    W, D = 4 * KEN, 3 * KEN
    ZK = -1.0 * KEN                                      # shop doma | vat room
    E = 3.40
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_konya", W, D, [2, 3], "indigo dyer's workshop (kon'ya, TR17)", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    # front: the shop open over three bays; the right bay walled with a window
    open_front(S, 0.0, 3 * KEN, YT)
    S.wall_line("front", [(3 * KEN, W, DOMA)], YT, [(3.0 * KEN, 3.5 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(3.5 * KEN,))
    S.window(openings.part_window_slide("_board"), "front", 3.0 * KEN, DOMA, "Window (shop, front R)")
    # back (lx = W - x): the vat room at VAT_Y; the back door to the drying yard lx 0.5..1.5 ken (x 2.5..3.5 ken)
    S.wall_line("back", [(0.0, W, VAT_Y)], YT, [(0.5 * KEN, 1.5 * KEN, VAT_Y, VAT_Y + 2.0, "door"),
                                                 (2.5 * KEN, 3.0 * KEN, VAT_Y + 0.90, VAT_Y + 1.60, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.5 * KEN, 3.0 * KEN))
    S.door(openings.part_itado("_single"), "back", 0.5 * KEN, VAT_Y, "Back door (vat room -> drying yard)", "back")
    S.window(openings.part_tsukiage("_board"), "back", 2.5 * KEN, VAT_Y, "Window (vat room, back, push-up)")
    st = B.P("back_step")
    found.step(st, 1.0 * KEN, "natural", drop=VAT_Y, width=1.04)
    B.put(st, S.F["back"], 0.0, VAT_Y, what="the back door's stone step down to the yard")
    # the gables: the vat room part at VAT_Y, the shop part at DOMA
    S.wall_line("left", [(0.0, D + ZK, VAT_Y), (D + ZK, D, DOMA)], YG,
                [(0.5 * KEN, 1.0 * KEN, VAT_Y + 0.90, VAT_Y + 1.65, "window")], finish=fin, koshiita=kosh,
                nodes_extra=(0.5 * KEN, 1.0 * KEN, D + ZK))
    S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, VAT_Y, "Window (vat room, west)")
    S.wall_line("right", [(0.0, -ZK, DOMA), (-ZK, D, VAT_Y)], YG,
                [(2.0 * KEN, 2.5 * KEN, VAT_Y + 0.90, VAT_Y + 1.65, "window")], finish=fin, koshiita=kosh,
                nodes_extra=(-ZK, 2.0 * KEN, 2.5 * KEN))
    S.window(openings.part_window_slide("_board"), "right", 2.0 * KEN, VAT_Y, "Window (vat room, east)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    # floors: the shop doma; the vat room's raised earth floor with its stone kerb and the step up; the vat bank
    B.interior = True
    B.merge(FL.doma("mise", 0.0, W, ZK, 0.30, road=(A_, W - A_, ZK + 0.02, -0.15), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    bx, bz = 1.75 * KEN, -2.0 * KEN
    bank = _vat_bank(S, bx, bz, VAT_Y)
    vr = (A_, W - A_, -D + A_, ZK - 0.12)
    vp = B.P("vat_floor")
    for (a, b, c, d) in FL.rect_minus(vr, [bank]):
        vp.add(box(a, b, -0.10, VAT_Y, c, d, {"top": "ground_doma_earth", "default": "stone_cut"}, vis=(1, 2, 3),
                   geo=True, view=True, fire="dirt", tag="doma"))
        vp.road([(a, VAT_Y, c), (b, VAT_Y, c), (b, VAT_Y, d), (a, VAT_Y, d)], "doma")
    vp.add(box(A_, W - A_, -0.10, VAT_Y + 0.012, ZK - 0.12, ZK, "stone_cut", vis=(1, 2, 3), geo=True, view=True,
               fire="granite", tag="kerb"))
    vp.road([(A_, VAT_Y + 0.012, ZK - 0.12), (W - A_, VAT_Y + 0.012, ZK - 0.12), (W - A_, VAT_Y + 0.012, ZK),
             (A_, VAT_Y + 0.012, ZK)], "stone_ext")
    B.interior = True
    B.put(vp, (0.0, (0.0, 0.0, 0.0)), what="the vat room's raised earth floor (0.30) + the stone kerb")
    st2 = B.P("kerb_step")
    run2 = found.step(st2, 2.0 * KEN, "natural", drop=VAT_Y - DOMA, width=1.04)
    B.put(st2, (0.0, (0.0, 0.0, ZK)), 0.0, VAT_Y, what="the step up from the shop doma to the vat room")
    B.interior = False
    S.obst.append(("mise", _r(2.0 * KEN - 0.54, 2.0 * KEN + 0.54, ZK, ZK + run2 + 0.06)))
    # fittings
    fit(S, "bales", "aiba", rect=(A_ + 0.05, A_ + 1.20, -D + A_ + 0.05, -D + A_ + 0.90), obstacle=False,
        note="sukumo (fermented indigo) in straw bales in the corner")
    fit(S, "lye", "aiba", rect=(W - A_ - 1.10, W - A_ - 0.05, ZK - 1.50, ZK - 0.25), obstacle=False,
        note="the lye drip tubs (akumizu) and the bran / lime tubs")
    fit(S, "poles", "aiba", rect=(A_ + 0.02, A_ + 0.40, ZK - 1.5, ZK - 0.30), obstacle=False,
        note="stirring poles and dripping cloth on a rack by the west wall")
    fit(S, "shop", "mise", rect=(A_ + 0.20, W - A_ - 0.20, ZK + 0.15, ZK + 0.75), obstacle=False,
        note="the shop doma: bolts of dyed cloth on a shelf, the counting desk")
    S.place_windows()
    S.room("mise", "shop", "earth", DOMA, (A_, W - A_, ZK + 0.02, -0.15), [],
           "the shop doma, open to the street: dyed cloth, Arimatsu shibori hung at the front", enclosed=False)
    S.room("aiba", "workshop", "earth", VAT_Y, vr, [S.dn["back"]],
           "the vat room: four sunk indigo vats round the fire pit, sukumo bales, lye tubs; back door to the yard; "
           "open to the shop over the kerb", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "konya", "roof": roof}, "levels": {"doma": DOMA, "vat_floor": VAT_Y,
                                                                             "eave": E},
                        "koyagumi": K["counts"], "vat_bank": bank}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR21 paper mill
def kamisuki(name=None, roof="itabuki", wear="_w2"):
    fam = roof
    W, D = 4 * KEN, 2.5 * KEN
    E = 3.30
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_kamisuki", W, D, [1, 2], "paper mill (kami-suki-ba, TR21), %s" % fam, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=0.90 if fam == "thatch" else None, soot=False,
                            ridge="bamboo", members="log")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    S.wall_line("front", [(0.0, W, DOMA)], YT, [(0.5 * KEN, 1.0 * KEN, DOMA + 0.80, DOMA + 1.70, "window"),
                                                (1.5 * KEN, 2.0 * KEN, DOMA + 0.80, DOMA + 1.70, "window"),
                                                (2.5 * KEN, 3.5 * KEN, DOMA, DOMA + 2.0, "door")],
                nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.5 * KEN, 3.5 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "front", 0.5 * KEN, DOMA - 0.10, "Window (vat, front L)")
    S.window(openings.part_window_slide("_board"), "front", 1.5 * KEN, DOMA - 0.10, "Window (vat, front R)")
    S.door(openings.part_itado("_single"), "front", 2.5 * KEN, DOMA, "Workshop door", "front")
    S.wall_line("back", [(0.0, W, DOMA)], YT, [(2.5 * KEN, 3.0 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(2.5 * KEN, 3.0 * KEN), **bw)
    S.window(openings.part_tsukiage("_board"), "back", 2.5 * KEN, DOMA, "Window (back, push-up)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(1.0 * KEN, 1.5 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(1.0 * KEN, 1.5 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "left", 1.0 * KEN, DOMA, "Window (end)")
    S.wall_line("right", [(0.0, D, DOMA)], YG, (), **bw)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board", thatch=(fam == "thatch"))
    _gable_leanto(S, "right", fam if fam != "thatch" else "itabuki", E, t)
    B.interior = True
    B.merge(FL.doma("floor", 0.0, W, -D, 0.0, road=(A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    fit(S, "vat", "floor", centre=(1.25 * KEN, -0.95), size=(2.0, 1.1), yaw=0.0,
        note="the paper vat (suki-bune) under the front windows, the mould hung from its bamboo spring pole")
    fit(S, "chiritori", "floor", centre=(0.55, -D + 0.85), size=(0.80, 0.80), yaw=0.0,
        note="the picking tub (chiri-tori) by the west wall")
    fit(S, "beat", "floor", centre=(3.1 * KEN, -D + 0.85), size=(1.30, 0.80), yaw=0.0,
        note="the beating board with the mallets and bark bundles")
    fit(S, "press", "floor", centre=(1.9 * KEN, -D + 0.70), size=(1.60, 0.90), yaw=0.0,
        note="the couching stack under its small lever press with stones")
    fit(S, "steamer", "leanto", centre=(W + 0.95, -D / 2), size=(1.10, 1.10), yaw=90.0,
        note="the bark steamer (koshiki over a cauldron on a hearth) under the lean-to")
    S.place_windows()
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -A_), [S.dn["front"]],
           "the paper workshop: the vat by the light, the picking tub, the beating board, the press")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "kamisuki", "roof": roof}, "levels": {"doma": DOMA, "eave": E},
                        "koyagumi": K["counts"]}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ yards
YARDS = {
    # the brewery: a black board fence round the plot (12 x 13 ken), the wide gate in the south (lane) line; the
    # kasane-gura stands along the north line, the polishing shed and the cask kura in the yard
    "brewery": dict(W=12 * KEN, D=13 * KEN, closed=True,
                    runs=[([(0.0, 0.0), (0.0, 13 * KEN), (12 * KEN, 13 * KEN), (12 * KEN, 0.0)], "itabei",
                           dict(kuro=True, cap="none"), ("end", "end"))],
                    # FX6: a two-leaf board yard gate for the cask carts (was a 1.5-ken kabuki-mon)
                    gates=[(0, 3, 6.0 * KEN) + DW.pick_gate("itabei", dict(kuro=True), status="work", carts=True)]),
    # the dyer's drying yard behind the workshop: a board fence, the gate in its south line facing the back door
    "dyersyard": dict(W=8 * KEN, D=6 * KEN, closed=True,
                      runs=[([(0.0, 0.0), (0.0, 6 * KEN), (8 * KEN, 6 * KEN), (8 * KEN, 0.0)], "itabei",
                             dict(kuro=False, cap="none"), ("end", "end"))],
                      # FX6: a single-leaf board gate behind the back door (was a 1.5-ken kabuki-mon)
                      gates=[(0, 3, 5.5 * KEN) + DW.pick_gate("itabei", status="work")]),
    # the paper mill's drying yard (behind the mill): an open bamboo fence (yotsume), the gate at the south-east corner
    "paperyard": dict(W=9 * KEN, D=6 * KEN, closed=True,
                      runs=[([(0.0, 0.0), (0.0, 6 * KEN), (9 * KEN, 6 * KEN), (9 * KEN, 0.0)], "yotsume", {},
                             ("end", "end"))],
                      # FX6 (Stephen: "waaaay too big for that fence"): a shiorido in the 1.05 m bamboo fence (was a
                      # 1.5-ken kabuki-mon, 3.15 m tall)
                      gates=[(0, 3, 1.0 * KEN) + DW.pick_gate("yotsume", status="work")]),
}
DW.COMPOUNDS.update(YARDS)


def compound(name=None, plot="brewery", wear="_w1"):
    return DW.compound(name=name, plot=plot, wear=wear)


# ================================================================================================ dispatch
def _builders():
    return {"okura": okura, "maegura": maegura, "seimai": globals().get("seimai"), "suisha": globals().get("suisha"),
            "konya": globals().get("konya"), "kamisuki": globals().get("kamisuki"),
            "compound": globals().get("compound")}


def build(kind, **params):
    fn = _builders().get(kind)
    if fn is None:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return fn(**params)


def budget_class(kind, **params):
    """PLAYBOOK §12: the two brewery kura and the yards are 'large'; the polishing shed 'standard'; the rest
    'standard'."""
    if kind in ("okura", "maegura", "compound"):
        return "large"
    return "standard"


def over_budget_ok(kind, **params):
    """CA1: a deliberate overage (<= +50 %, PLAYBOOK §12) and its reason, or None."""
    if kind == "suisha":
        return ("the overshot wheel's rims, sole and open buckets stay in every LOD (C15: seen from above the bucket "
                "gaps are part of the silhouette) + the flume and its trestles")
    if kind == "konya" and params.get("roof", "sangawara") == "sangawara":
        return ("a tiled 4 x 3 ken town workshop with the sunk vat bank built into its floor (four jars in their "
                "frames, clay fillets, the fire pit)")
    if False:
        return ("a 9 x 4 ken tiled kura (kawara geometry over 160 m2 of roof) with the exposed log truss, the loft, its "
                "stair and rail: the brewery hero")
    if kind == "maegura":
        return ("a 9 x 4 ken tiled kura with three kura doorways (stepped plaster surrounds + tile pents), the steam "
                "vent, the koji block and the roof-union gutter")
    return None


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as trade.model."""
    H, info = build(kind, name=name, **params)
    cx, cz = info.get("centre_kit", (info["W"] / 2, -info["D"] / 2))
    M = H.transformed(0.0, (-cx, 0.0, -cz))
    M.meta = dict(H.meta)

    def mr(r):
        return (r[0] - cx, r[1] - cx, r[2] - cz, r[3] - cz)
    floors = [dict(f, rect=mr(f["rect"]), obstacles=[mr(o) for o in f["obstacles"]]) for f in info["floors"]]
    rooms = [dict(r, rect_model=[round(v, 3) for v in mr(r["rect_kit"])]) for r in info["rooms"]]
    fits = []
    for f in info["fittings"]:
        g = dict(f)
        if "rect" in g:
            g["rect"] = [round(v, 3) for v in mr(g["rect"])]
        if "centre" in g:
            g["centre"] = [round(g["centre"][0] - cx, 3), round(g["centre"][1] - cz, 3)]
        fits.append(g)
    extra = {}
    if info.get("stair"):
        st = info["stair"]
        extra["stair_model"] = dict(st, foot=(st["foot"][0] - cx, st["foot"][1] - cz), dir=1.0, well=mr(st["well"]))
    info = dict(info, centre=(cx, cz), fittings_model=fits,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[(x - cx, z - cz, y) for (x, z, y) in info["passages"]], **extra)
    return M, floors, rooms, info
