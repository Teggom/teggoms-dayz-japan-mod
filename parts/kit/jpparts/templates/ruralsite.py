"""The wave-3c-2 rural / industrial site template (W3C2, Phase C wave 3c-2, 2026-10-02): the charcoal kiln under its
roof (TR23), the climbing kiln (TR18), the daruma tile kiln (TR19), the lime kiln (TR26), the quarry face (TR25), the
mine adit (TR27), the timber slide (TR24), the salt bed (TR22), and the two new huts: the bunk hall (KEEP_DWELLINGS 4:
miners, loggers) and the salt-boiling hut (kamaya) with its shell pan; the yards through templates/dwelling.compound.
Research, sizes and every recorded choice: spikes/W3C2/W3C2_NOTES.md. The huts and sheds a site reuses (the west
hut, the open sheds, W3B's earth-floor workshops and saw shed) are earlier shells, furnished in buildings/w3c2_sets.py.

    M, floors, rooms, info = ruralsite.model(kind="sumigama")

Kinds (kit frame as rural.py: x 0..W along the front, z 0 = front line, +z = out, z -D = back, y 0 = grade)
  sumigama     the charcoal kiln (jp_p_site_kiln_dome) under its board roof on six posts (3 x 3 ken, open sides)
  noborigama   the climbing kiln (jp_p_site_kiln_climbing) on its bank + the stoking floor before the fire mouth
  darumagama   the daruma tile kiln (jp_p_site_kiln_updraught) under its board roof on six posts (3.5 x 2.5 ken)
  ishibaigama  the lime kiln pit on its bank (jp_p_site_kiln_shaft) + the draw floor under a small roof (2 x 1 ken)
  ishiba       the quarry face: a rock outcrop cut in two benches + the splitting floor and a small shelter
  mabu         the mine adit: a knoll with a 4-ken timbered drift (dead end), the mouth floor, the mine shrine
  shura        the timber slide's lowest 4 bays on trestles + the landing at its foot
  enden        a Gyotoku irihama salt-bed section on dry land: the raised raked bed, the dry ditch, the embankment + sluice
  kamaya       W 4 x D 3 ken salt-boiling hut: board walls, the shell pan on its clay firebox under a long smoke vent
  bunkhall     W 6 x D 3 ken, board walls: the entrance doma (2 ken, front + back doors, the hearth) and the long
               raised sleeping floor (0.40, one irori); roof itabuki | ishioki
"""
import math

from ..core import Part, box, prism, KEN, HALF, POST, KETA_H, DOOR_H
from .. import walls, openings, roofs as R, floors as FL, found, ruralsite_parts as RS
from .rural import Shell, _r, DOMA, A_, _kamado, _irori, big_leaf
from .civic import fit, trim_lods, koshiyane, open_front, _ext
from . import dwelling as DW

KINDS = ("sumigama", "noborigama", "darumagama", "ishibaigama", "ishiba", "mabu", "shura", "enden", "kamaya",
         "bunkhall", "compound")


def _open_roof(S, W, D, E, fam="itabuki", ov=None, ridge="bamboo"):
    """An open roof on its corner posts (+ a post at every 2 ken of the eave lines): the kiln roofs."""
    YT = E - KETA_H
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=ov, soot=True, ridge=ridge, joya_posts=False)
    S.keta_ring(W, D, E, hip=False)
    nx = max(1, int(round(W / (2 * KEN))))
    for k in range(nx + 1):
        x = round(W * k / nx, 4)
        for z in (0.0, -D):
            S.post(x, z, YT + KETA_H - 0.02)
    return sls, info_r, K


# ================================================================================================ TR23 charcoal kiln
def sumigama(name=None, wear="_w2"):
    W, D, E = 3 * KEN, 3 * KEN, 2.70
    S = Shell(name or "jp_sumigama", W, D, [1, 2], "charcoal kiln under its roof (sumi-gama, TR23)", wear)
    B = S.B
    sls, info_r, K = _open_roof(S, W, D, E)
    # the work floor round the kiln (packed earth), the kiln in the middle, its mouth to the front
    cx, cz = W / 2, -D / 2 - 0.10
    B.interior = True
    B.merge(FL.doma("floor", -0.10, W + 0.10, -D - 0.10, 0.25, road=(A_, W - A_, -D + A_, -0.10), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    kp = B.P("kiln")
    ki = RS.kiln_dome(kp, cx, cz)
    B.put(kp, (0.0, (0.0, 0.0, 0.0)), what="jp_p_site_kiln_dome _charcoal (cold, opened)")
    S.obst.append(("floor", _r(cx - ki["rx"] - 0.05, cx + ki["rx"] + 0.05, cz - ki["rz"] - 0.40,
                               ki["front"] + 0.15)))
    S.obst.append(("floor", _r(cx - 1.25, cx + 1.25, ki["front"], ki["front"] + 0.50)))     # the mouth's stones
    fit(S, "rake", "floor", rect=(A_ + 0.05, A_ + 0.60, -D + A_ + 0.05, -D + A_ + 0.80), obstacle=False,
        note="the kiln rake and long hoe leaning on a back post")
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -0.10), [],
           "the kiln floor under the roof: the earth-dome kiln, its fire mouth to the front, the flue at the back",
           enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "sumigama"}, "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"],
                        "kiln": ki}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR18 climbing kiln
def noborigama(name=None, wear="_w2"):
    """The climbing kiln on its bank (jp_p_site_kiln_climbing _4ch) + the stoking floor before its fire mouth."""
    K = RS.NOBORI
    W = 2 * KEN
    LF = KEN                                     # the stoking floor in front of the fire mouth
    D = LF + K["lf"] + K["n"] * K["lc"] + K["lflue"] + 0.40
    S = Shell(name or "jp_noborigama", W, D, [2, 3], "climbing kiln (noborigama, TR18), Seto / Mino type", wear)
    B = S.B
    kp = B.P("kiln")
    ki = RS.kiln_climbing(kp, open_door=0)
    B.put(kp, (0.0, (W / 2, 0.0, -LF)), what="jp_p_site_kiln_climbing _4ch (cold, the lowest loading door open)")
    # the stokers' shelter: a board roof on four posts over the stoking floor (its back eave over the firebox vault)
    sls, info_r, K_ = _open_roof(S, W, LF, 2.75)
    B.interior = True
    B.merge(FL.doma("stoke", 0.0, W, -LF, 0.0, road=(0.15, W - 0.15, -LF + 0.02, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.obst.append(("stoke", _r(W / 2 - 0.80, W / 2 + 0.80, -LF, -LF + 0.85)))       # the mouth's jambs + ash
    S.room("stoke", "workshop", "earth", DOMA, (0.15, W - 0.15, -LF + 0.02, -0.15), [],
           "the stoking floor before the fire mouth under the stokers' shelter (the kiln itself is solid: its doors "
           "are look-ins)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "noborigama"}, "levels": {"doma": DOMA}, "kiln": ki,
                        "koyagumi": K_["counts"]}, exterior=None)
    return H, info


# ================================================================================================ TR19 daruma tile kiln
def darumagama(name=None, wear="_w2"):
    """The daruma tile kiln (jp_p_site_kiln_updraught _daruma) under its board roof on six posts (3.5 x 2.5 ken), its
    long axis along the front, the loading door to the front, a stoking floor at each fire mouth."""
    W, D, E = 3.5 * KEN, 2.5 * KEN, 3.25
    S = Shell(name or "jp_kawara_gama", W, D, [1, 2], "daruma tile kiln under its roof (kawara-gama, TR19)", wear)
    B = S.B
    sls, info_r, K = _open_roof(S, W, D, E)
    B.interior = True
    B.merge(FL.doma("floor", -0.10, W + 0.10, -D - 0.10, 0.25, road=(A_, W - A_, -D + A_, -0.10), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    cx, cz = W / 2, -D / 2
    kp = B.P("kiln")
    ki = RS.kiln_daruma(kp)
    B.put(kp, (90.0, (cx, 0.0, cz)), what="jp_p_site_kiln_updraught _daruma (cold, the loading door walled up)")
    hx, hz = ki["L"] / 2, ki["w"] / 2
    S.obst.append(("floor", _r(cx - hx - 0.20, cx + hx + 0.20, cz - hz - 0.05, cz + hz + 0.65)))
    for sg in (-1, 1):                                       # the fire mouths' jambs + ash at both ends
        xm = cx + sg * (hx + 0.30)
        S.obst.append(("floor", _r(xm - 0.35, xm + 0.35, cz - 0.70, cz + 0.70)))
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -0.10), [],
           "the kiln floor under the roof: the daruma kiln, a stoking floor at each fire mouth", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "darumagama"}, "levels": {"doma": DOMA, "eave": E},
                        "koyagumi": K["counts"], "kiln": ki}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR26 lime kiln
def ishibaigama(name=None, wear="_w2"):
    """The lime kiln pit on its bank (jp_p_site_kiln_shaft _stone) + the draw floor before its draw hole under a small
    board roof on four posts (2 x 1 ken): where the burnt lime was drawn and the fire tended."""
    LF = KEN
    W = 2 * KEN
    S = Shell(name or "jp_ishibai_gama", W, LF + 8.0, [1, 2], "lime kiln (ishibai-gama, TR26), Nariki / Ome type", wear)
    B = S.B
    kp = B.P("kiln")
    ki = RS.kiln_pit(kp)
    B.put(kp, (0.0, (W / 2, 0.0, -LF - ki["front"])), what="jp_p_site_kiln_shaft _stone (burnt out, cold)")
    sls, info_r, K_ = _open_roof(S, W, LF, 2.70)
    B.interior = True
    B.merge(FL.doma("draw", 0.0, W, -LF, 0.0, road=(0.15, W - 0.15, -LF + 0.02, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.obst.append(("draw", _r(W / 2 - 0.80, W / 2 + 0.80, -LF, -LF + 0.85)))
    S.room("draw", "workshop", "earth", DOMA, (0.15, W - 0.15, -LF + 0.02, -0.15), [],
           "the draw floor before the kiln's draw hole, under its small roof (the kiln pit is solid; the heap shows "
           "over its rim)", enclosed=False)
    trim_lods(S.H)
    S.D = LF + 2 * ki["front"] + ki["bank"]
    H, info = S.finish({"params": {"kind": "ishibaigama"}, "levels": {"doma": DOMA}, "kiln": ki,
                        "koyagumi": K_["counts"]}, exterior=None)
    info["D"] = S.D
    return H, info


# ================================================================================================ TR25 quarry face
def _shelter(S, x0, z0, W, D, E):
    """A small open board roof on four posts (kit frame offset x0, z0: its front line at z0): the work shelters of the
    sites (the masons' splitting floor, the adit's mouth)."""
    from ..core import Part as _P
    sub = Shell(S.H.name + "_shelter", W, D, [1, 2], "", S.H.wear)
    sls, info_r, K = _open_roof(sub, W, D, E)
    S.B.merge(sub.H.transformed(0.0, (x0, 0.0, z0)))
    for (x, z, y0, y1) in sub.posts:
        S.posts.append((round(x + x0, 4), round(z + z0, 4), y0, y1))
    return K


def ishiba(name=None, wear="_w2"):
    """The quarry face (ishiba): a rock outcrop 11 x 6 m, 4.5 m high, its front cut in two benches with sheer split
    faces, wedge-hole rows (ya-ana) along the bench edges, a half-split block with its iron wedges on the lower bench,
    rubble at the foot; the masons' splitting floor before it under a small board roof (2 x 1 ken). Solid rock (not
    climbable)."""
    from ..core import rng_for, stone as _stone
    from ..shapes import rough_block
    W, D = 6 * KEN, 4.5 * KEN
    S = Shell(name or "jp_ishiba", W, D, [1, 2], "quarry face (ishiba, TR25): Izu andesite / Okazaki granite", wear)
    B = S.B
    rng = rng_for("ishiba")
    cx = W / 2
    zl, zu, zb = -D + 3.40, -D + 1.90, -D           # the lower face, the upper face, the back
    yl, yu = 2.10, 4.40
    rock = B.P("rock")
    M2 = {"top": "stone_field", "default": "stone_cut"}
    g = dict(vis=(1, 2, 3), geo=True, view=True, fire="granite")
    rock.add(rough_block(rng, cx - 5.0, cx + 5.0, -0.30, yu, zb + 0.20, zu, M2, chamfer=0.25, top_jit=0.20,
                         tag="rock_upper", **g))
    rock.add(rough_block(rng, cx - 5.0, cx + 4.0, -0.30, yl, zu - 0.02, zl, M2, chamfer=0.18, top_jit=0.10,
                         tag="rock_lower", **g))
    # weathered natural rock on the crown and the shoulders (the uncut hill)
    for (x, z, w, d, h, top) in ((cx - 2.5, zb + 1.2, 3.6, 2.4, 1.2, yu + 0.55), (cx + 1.8, zb + 1.0, 3.2, 2.2, 1.0,
                                                                                    yu + 0.40),
                                 (cx - 5.6, zb + 1.8, 2.2, 3.4, 3.0, 2.9), (cx + 5.3, zb + 1.6, 2.0, 3.0, 3.4, 3.3),
                                 (cx + 4.6, zl - 0.6, 1.6, 1.8, 1.6, 1.6)):
        rock.add(_stone(rng, x, z, w, d, h, top, "stone_field", bury=0.30, n=9, flat_top=0.55, tag="rock_natural", **g))
    # the wedge-hole rows (ya-ana) along both faces, 0.25 apart, just under the bench edges
    for (zf, y, xa, xb) in ((zl, yl - 0.28, cx - 4.4, cx + 3.4), (zu, yu - 0.45, cx - 4.4, cx + 4.4)):
        x = xa
        while x <= xb:
            rock.add(box(x - 0.045, x + 0.045, y - 0.03, y + 0.03, zf, zf + 0.004, "lacquer_black", vis=(1,),
                         tag="ya_ana"))
            x += 0.25
    # the half-split block on the lower bench: two halves 3 cm apart, iron wedges (ya) standing in the split
    bz = (zu + zl) / 2
    for (a, b) in ((cx - 1.6, cx - 0.82), (cx - 0.79, cx + 0.0)):
        rock.add(rough_block(rng, a, b, yl - 0.02, yl + 0.70, bz - 0.40, bz + 0.40, "stone_cut", chamfer=0.03,
                             top_jit=0.01, tag="split_block", vis=(1, 2, 3), geo=True, view=True, fire="granite"))
    for k in range(4):
        z = bz - 0.30 + 0.20 * k
        rock.add(prism([(-0.015, 0.0), (0.015, 0.0), (0.03, 0.14), (-0.03, 0.14)], "z", z - 0.03, z + 0.03,
                       "metal_iron", vis=(1,), tag="ya").transformed(0.0, (cx - 0.805, yl + 0.62, 0.0)))
    # rubble at the foot
    for k in range(9):
        x, z = cx - 4.5 + k * 1.05 + rng.uniform(-0.3, 0.3), zl + 0.45 + rng.uniform(0.0, 0.7)
        sz = rng.uniform(0.25, 0.55)
        rock.add(_stone(rng, x, z, sz, sz * 0.8, sz * 0.6, sz * 0.55, "stone_cut", bury=0.05, n=7, flat_top=0.6,
                        vis=(1, 2), tag="rubble"))
    B.put(rock, (0.0, (0.0, 0.0, 0.0)), what="the cut rock face, two benches, ya-ana rows, the half-split block")
    # the splitting floor before the face + the masons' shelter (2 x 1 ken) at its east end
    B.interior = True
    B.merge(FL.doma("floor", 0.0, W, zl + 1.30, 0.0, road=(0.15, W - 0.15, zl + 1.35, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    K = _shelter(S, W - 2 * KEN, 0.0, 2 * KEN, KEN, 2.70)
    S.room("floor", "workshop", "earth", DOMA, (0.15, W - 0.15, zl + 1.35, -0.15), [],
           "the splitting floor before the quarry face; the masons' small shelter at the east end", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "ishiba"}, "levels": {"doma": DOMA, "benches": [yl, yu]},
                        "koyagumi": K["counts"]}, exterior=None)
    return H, info


# ================================================================================================ TR27 mine adit
def mabu(name=None, wear="_w2"):
    """The mine adit (jp_p_site_adit _timbered): the knoll with the 4-ken timbered drift (a dead end at a rockfall,
    walkable), the mouth floor before the portal, the yama-no-kami shrine (the kit's wooden hokora on its base stones)
    beside the portal."""
    from .. import hokora as HK
    W, LM, DK = 5 * KEN, KEN, 10.0
    D = LM + DK
    S = Shell(name or "jp_mabu", W, D, [1, 2], "mine adit (mabu, TR27): timbered drift into a knoll", wear)
    B = S.B
    cx, zp = W / 2, -LM
    kp = B.P("adit")
    ai = RS.adit(kp, cx=cx, zp=zp, H=4.0, W=W, D=DK, floor_y=DOMA)
    B.put(kp, (0.0, (0.0, 0.0, 0.0)), what="jp_p_site_adit _timbered (the drift ends at a rockfall)")
    S.posts += ai["posts"]
    rw = ai["rw"]
    B.interior = True
    B.merge(FL.doma("drift", cx - rw, cx + rw, ai["z_end"], zp, road=(cx - rw + 0.03, cx + rw - 0.03, ai["z_end"] + 0.70,
                                                                       zp), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    B.merge(FL.doma("mouth", cx - 1.80, cx + 1.80, zp, 0.10, road=(cx - 1.70, cx + 1.70, zp, -0.10), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    # the mine shrine (yama-no-kami) on the mouth's right, facing out
    hp = B.P("yamanokami")
    HK.wood_hokora(hp, "shinmei")
    B.put(hp, (0.0, (cx + 2.55, 0.0, zp + 0.60)), what="jp_p_site_hokora _wood_shinmei (the mine's yama-no-kami)")
    xt = ai["trough_x"]
    hw = RS.ADIT["half"] - RS.ADIT["post"] / 2
    S.obst.append(("drift", _r(xt - 0.10, xt + 0.10, ai["z_end"], zp)))
    S.obst.append(("mouth", _r(xt - 0.10, xt + 0.10, zp, 0.10)))
    for (x, z, _, _) in ai["posts"]:
        if abs(z - zp) < 0.01:
            S.obst.append(("mouth", _r(x - 0.20, x + 0.20, zp, zp + 0.20)))
    S.passages.append((cx, zp, DOMA))
    S.room("mouth", "yard", "earth", DOMA, (cx - 1.70, cx + 1.70, zp, -0.10), [],
           "the mouth floor before the portal (the drainage trough runs out here; the mine shrine on the right)",
           enclosed=False)
    S.room("drift", "storage", "earth", DOMA, (cx - hw, cx + hw, ai["z_end"] + 0.75, zp), [],
           "the timbered drift: 4 ken in, a dead end at the rockfall (recorded: no long tunnel)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "mabu"}, "levels": {"doma": DOMA, "cap": ai["cap"]},
                        "adit": {"clear": ai["clear"], "z_end": ai["z_end"]}}, exterior=None)
    return H, info


# ================================================================================================ bunk hall (KEEP_DWELLINGS 4)
def bunkhall(name=None, roof="itabuki", wear="_w2"):
    """The bunk hall of a mine or a logging crew: W 6 x D 3 ken, board walls, eave 3.10; the entrance doma (x 0..2 ken:
    the front door, the back door, the one-mouth stove) and the long raised sleeping floor (0.40, boards, one irori with
    its hook) with the kamachi step; two windows front and back. roof itabuki | ishioki (the mountain roof)."""
    from .rural import _hut_floor, HUT_FLOOR
    W, D, E = 6 * KEN, 3 * KEN, 3.10
    t = R.PITCH[roof]
    YT, YG = E - KETA_H, E - 0.21
    XD = 2 * KEN
    S = Shell(name or "jp_bunkhall", W, D, [1, 2], "bunk hall for miners / loggers (KEEP_DWELLINGS 4), %s" % roof, wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, soot=True, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    FLOOR = HUT_FLOOR
    S.wall_line("front", [(0.0, XD, DOMA), (XD, W, FLOOR)], YT,
                [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door"),
                 (3.0 * KEN, 3.5 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window"),
                 (5.0 * KEN, 5.5 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window")],
                nodes_extra=(0.5 * KEN, 1.5 * KEN, 3.0 * KEN, 3.5 * KEN, 5.0 * KEN, 5.5 * KEN), **bw)
    S.door(big_leaf("_plain"), "front", 0.5 * KEN, DOMA, "Front door (itado)", "front")
    S.window(openings.part_window_slide("_board"), "front", 3.0 * KEN, FLOOR, "Window (front, sleeping floor W)")
    S.window(openings.part_window_slide("_board"), "front", 5.0 * KEN, FLOOR, "Window (front, sleeping floor E)")
    # back (lx = W - x): sleeping floor lx 0..4 ken, doma lx 4..6 ken with the back door
    S.wall_line("back", [(0.0, W - XD, FLOOR), (W - XD, W, DOMA)], YT,
                [(1.0 * KEN, 1.5 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window"),
                 (2.5 * KEN, 3.0 * KEN, FLOOR + 0.90, FLOOR + 1.60, "window"),
                 (4.5 * KEN, 5.5 * KEN, DOMA, DOMA + 2.0, "door")],
                nodes_extra=(1.0 * KEN, 1.5 * KEN, 2.5 * KEN, 3.0 * KEN, 4.5 * KEN, 5.5 * KEN), **bw)
    S.door(openings.part_itado("_single"), "back", 4.5 * KEN, DOMA, "Back door", "back")
    S.window(openings.part_window_slide("_board"), "back", 1.0 * KEN, FLOOR, "Window (back E)")
    S.window(openings.part_window_slide("_board"), "back", 2.5 * KEN, FLOOR, "Window (back W)")
    for side in ("left", "right"):
        S.wall_line(side, [(0.0, D, DOMA if side == "left" else FLOOR)], YG, (), **bw)
        S.gable(side, D, t, E, "_board")
    rects = _hut_floor(S, "board", XD, W, D, FLOOR, K=K)
    _kamado(S, "doma", 0.50, -D + 0.50, 0.0, size=(0.60, 0.60))
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, rects["doma"], [S.dn["front"], S.dn["back"]], "the entrance doma: stove, "
           "water jar, tools")
    S.room("living", "living", "boards", FLOOR, rects["living"], [], "the long sleeping floor with the irori")
    trim_lods(S.H, stones_keep=2 if roof == "ishioki" else 1)
    H, info = S.finish({"params": {"kind": "bunkhall", "roof": roof}, "levels": {"doma": DOMA, "floor": FLOOR,
                                                                               "eave": E}, "koyagumi": K["counts"]},
                       exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR24 timber slide
def shura(name=None, wear="_w2"):
    """The timber slide's lowest 4 bays (jp_p_site_shura _log4) on trestles (posts on stones, a cap, a brace) at every
    bay end, its foot on the landing floor (1.5 ken) where the logs came out."""
    K = RS.SHURA
    W, LL = 2 * KEN, 1.5 * KEN
    L = K["bays"] * K["bay"]
    D = LL + L + 0.30
    S = Shell(name or "jp_shura", W, D, [1, 2], "timber slide (shura, TR24): the lowest 4 bays + the landing", wear)
    B = S.B
    cx = W / 2
    kp = B.P("slide")
    si = RS.shura(kp, x0=cx, z0=-LL)
    B.put(kp, (0.0, (0.0, 0.0, 0.0)), what="jp_p_site_shura _log4 (a log stopped in it)")
    # the trestles: two posts (on stones) under each bay end but the foot, a cap under the sleeper, a cross brace
    tp = B.P("trestles")
    for b in range(1, K["bays"] + 1):
        z = round(-LL - b * K["bay"], 4)
        yb = si["ybed"](z) - 0.15
        for sx in (-1, 1):
            S.post(round(cx + sx * HALF, 4), z, yb)
        tp.add(box(cx - HALF - 0.10, cx + HALF + 0.10, yb, yb + 0.12, z - 0.07, z + 0.07, "wood_weathered",
                   vis=(1, 2, 3), geo=True, view=True, fire=True, tag="trestle_cap"))
        if yb > 1.0:
            from ..shapes import tube as _tube
            tp.add(_tube((cx - HALF, 0.25, z), (cx + HALF, yb - 0.15, z), 0.04, "wood_weathered", n=5, vis=(1, 2),
                         tag="trestle_brace"))
    B.put(tp, (0.0, (0.0, 0.0, 0.0)), what="the slide's trestles")
    B.interior = True
    B.merge(FL.doma("landing", 0.0, W, -LL, 0.0, road=(0.15, W - 0.15, -LL + 0.02, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.obst.append(("landing", _r(cx - 0.55, cx + 0.55, -LL, -LL + 0.40)))
    S.room("landing", "yard", "earth", DOMA, (0.15, W - 0.15, -LL + 0.02, -0.15), [],
           "the landing at the slide's foot (the log stack stands beside it)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "shura"}, "levels": {"doma": DOMA, "top": K["rise"]}}, exterior=None)
    return H, info


# ================================================================================================ TR22 salt works
def core_rings_heap(rng, x, z, r, y0, mat="ground_doma_tataki"):
    from ..core import rings as _rings
    base = [(x + r * (1 + rng.uniform(-0.1, 0.1)) * math.cos(2 * math.pi * k / 9),
             z + r * 0.8 * (1 + rng.uniform(-0.1, 0.1)) * math.sin(2 * math.pi * k / 9)) for k in range(9)]
    return _rings((base, [(y0 - 0.02, 1.0), (y0 + 0.18, 0.62), (y0 + 0.32, 0.25)]), mat, vis=(1, 2), tag="sand_heap")


def enden(name=None, wear="_w2"):
    """One section of a Gyotoku irihama salt field [GYO] on dry land (dead world: the bed dry, the ditch empty): a
    levelled bed of raked sand 7 x 4 ken raised 0.30 (its landward edge ramped), the tidal ditch (hama-mizo, 0.60
    wide, plank-lined, dry) along the sea side, the low embankment (tsutsumi) beyond it with a small timber sluice
    (posts on stones, the gate board shut), two heaps of scraped sand. Walkable bed."""
    from ..core import rng_for, stone as _stone
    W, D = 7 * KEN, 5 * KEN
    LB = 4 * KEN
    YB = 0.30
    S = Shell(name or "jp_enden", W, D, [1, 2], "salt field section (enden, irihama, TR22), dry", wear)
    B = S.B
    rng = rng_for("enden")
    SAND = {"top": "ground_doma_tataki", "default": "ground_earth_bare"}
    p = B.P("bed")
    p.add(box(0.0, W, -0.30, YB, -LB, -0.60, SAND, vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag="bed"))
    p.road([(0.0, YB, -LB), (W, YB, -LB), (W, YB, -0.60), (0.0, YB, -0.60)], "doma")
    p.add(prism([(-0.30, -0.60), (-0.30, 0.0), (0.0, 0.0), (YB, -0.60)], "x", 0.0, W, SAND, vis=(1, 2, 3), geo=True,
                view=True, fire="dirt", tag="bed_ramp"))
    p.road([(0.0, YB, -0.60), (W, YB, -0.60), (W, 0.0, 0.0), (0.0, 0.0, 0.0)], "doma")
    for k in range(12):
        z = -0.95 - k * 0.25
        p.add(box(0.25, W - 0.25, YB, YB + 0.012, z - 0.03, z + 0.03, "ground_earth_bare", vis=(1,), tag="rake_line"))
    for (x, z, r) in ((3.2, -2.6, 0.75), (8.9, -2.2, 0.60)):
        p.add(core_rings_heap(rng, x, z, r, YB))
    zd0, zd1 = -LB - 0.60, -LB
    YD = 0.10                      # the ditch's board floor 0.10 over grade (never at grade: no z-fight, FX5)
    p.add(box(0.0, W, -0.30, YD, zd0, zd1, "wood_sooted", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="ditch_floor"))
    p.road([(0.0, YD, zd0), (W, YD, zd0), (W, YD, zd1), (0.0, YD, zd1)], "boards_ext")
    p.add(box(0.0, W, YD, YB + 0.02, zd1 - 0.04, zd1, "wood_weathered", vis=(1, 2), tag="ditch_lining"))
    zk0, zk1 = -D, zd0
    p.add(prism([(-0.30, zk1), (-0.30, zk0), (0.10, zk0), (0.85, zk0 + 0.45), (0.85, zk1 - 0.30), (0.40, zk1)], "x",
                0.0, W, "ground_earth_bare", vis=(1, 2, 3), geo=True, view=True, fire="dirt", tag="dyke"))
    for k in range(16):
        x = 0.4 + k * (W - 0.8) / 15
        p.add(_stone(rng, x, zk0 + 0.15, 0.55, 0.35, 0.40, 0.42, "stone_field", bury=0.20, n=7, flat_top=0.6, vis=(1,),
                     tag="dyke_stone"))
    B.put(p, (0.0, (0.0, 0.0, 0.0)), what="the salt bed, the ditch, the embankment")
    xs0, xs1 = 12.5 * HALF, 13.5 * HALF          # (HALF = half a ken, 0.91)
    for x in (xs0, xs1):
        for z in (-9 * HALF, -9.5 * HALF):
            S.post(x, z, 1.25)
    sp = B.P("sluice")
    for z in (-9 * HALF, -9.5 * HALF):
        sp.add(box(xs0 - 0.10, xs1 + 0.10, 1.25, 1.37, z - 0.07, z + 0.07, "wood_weathered", vis=(1, 2, 3), geo=True,
                   view=True, fire=True, tag="sluice_cap"))
    sp.add(box(xs0 + 0.06, xs1 - 0.06, 0.10, 0.95, -9.25 * HALF - 0.03, -9.25 * HALF + 0.03, "wood_sooted",
               vis=(1, 2, 3), geo=True, view=True, fire=True, tag="sluice_gate"))
    B.put(sp, (0.0, (0.0, 0.0, 0.0)), what="the sluice (gate shut, dry)")
    S.obst.append(("bed", _r(2.4, 4.0, -3.4, -1.8)))
    S.obst.append(("bed", _r(8.2, 9.6, -2.9, -1.5)))
    S.room("bed", "yard", "sand", YB, (0.30, W - 0.30, -LB + 0.20, -0.65), [],
           "the salt bed (dry, raked); the sieve stands and rakes on it; the ditch and the embankment beyond",
           enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "enden"}, "levels": {"bed": YB}}, exterior=None)
    return H, info


def _pan(S, cx, cz, w=2.40, d=1.80):
    """The salt-boiling pan (a Gyotoku shell pan, kai-gama [GYO]: shell-lime plastered, shallow) on its clay firebox
    (shell geometry, like the dyer's vats): the firebox 0.55 high, its fire mouth to the front (+z), the pan's rim 0.15
    over it, a crust of salt dried in it; cold. Returns the footprint."""
    from ..core import rng_for
    p = S.B.P("pan")
    rng = rng_for("kamaya_pan")
    fw, fd, fh = w + 0.50, d + 0.50, 0.55
    p.add(box(cx - fw / 2, cx + fw / 2, 0.0, fh, cz - fd / 2, cz + fd / 2, "wall_nakanuri_int", vis=(1, 2, 3),
              geo=True, view=True, fire="dirt", tag="firebox"))
    t = 0.10
    for (a, b, c, d_) in ((cx - w / 2 - t, cx + w / 2 + t, cz - d / 2 - t, cz - d / 2),
                          (cx - w / 2 - t, cx + w / 2 + t, cz + d / 2, cz + d / 2 + t),
                          (cx - w / 2 - t, cx - w / 2, cz - d / 2, cz + d / 2),
                          (cx + w / 2, cx + w / 2 + t, cz - d / 2, cz + d / 2)):
        p.add(box(a, b, fh, fh + 0.15, c, d_, "wall_shikkui_aged", vis=(1, 2, 3), geo=True, view=True, fire="dirt",
                  tag="pan_rim"))
    p.add(box(cx - w / 2, cx + w / 2, fh, fh + 0.03, cz - d / 2, cz + d / 2, "wall_shikkui", vis=(1, 2, 3), geo=True,
              view=True, fire="dirt", tag="pan_crust"))
    RS.mouth(p, cx, 0.0, 0.55, 0.42, cz + fd / 2, rng=rng, jamb="ceramic_earthenware", header="ceramic_earthenware",
             tag="pan_mouth", svis=(1, 2, 3))
    p.add(prism(RS.ellipse(cx, cz + fd / 2 + 0.40, 0.60, 0.30, 10), "y", 0.035, 0.062, "ground_ash", vis=(1,),
                tag="ash_spill"))
    S.B.interior = True
    S.B.put(p, (0.0, (0.0, 0.0, 0.0)), what="the shell pan on its clay firebox (cold, a salt crust)")
    S.B.interior = False
    return (cx - fw / 2, cx + fw / 2, cz - fd / 2, cz + fd / 2 + 0.35)


def kamaya(name=None, wear="_w2"):
    """The salt-boiling hut (kamaya): W 4 x D 3 ken, board walls, earth floor, eave 3.30; the shell pan on its firebox
    in the middle under a long smoke vent; the front door (itado) at the left, a side door on the right gable, a
    push-up window at the back; room for the fuel heap, the brine tubs and the draining baskets."""
    W, D, E = 4 * KEN, 3 * KEN, 3.30
    fam = "itabuki"
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_kamaya", W, D, [1, 2], "salt-boiling hut (kamaya, TR22) with its shell pan", wear)
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=True, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    koshiyane(S, 1.0 * KEN, 2.0 * KEN, info_r, E, D, fam)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    S.wall_line("front", [(0.0, W, DOMA)], YT, [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door")],
                nodes_extra=(0.5 * KEN, 1.5 * KEN), **bw)
    S.door(big_leaf("_plain"), "front", 0.5 * KEN, DOMA, "Front door (itado)", "front")
    S.wall_line("back", [(0.0, W, DOMA)], YT, [(1.5 * KEN, 2.0 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(1.5 * KEN, 2.0 * KEN), **bw)
    S.window(openings.part_tsukiage("_board"), "back", 1.5 * KEN, DOMA, "Window (back, push-up)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(1.0 * KEN, 1.5 * KEN, DOMA + 0.90, DOMA + 1.60, "window")],
                nodes_extra=(1.0 * KEN, 1.5 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "left", 1.0 * KEN, DOMA, "Window (end)")
    S.wall_line("right", [(0.0, D, DOMA)], YG, [(1.0 * KEN, 2.0 * KEN, DOMA, DOMA + 2.0, "door")],
                nodes_extra=(1.0 * KEN, 2.0 * KEN), **bw)
    S.door(openings.part_itado("_single"), "right", 1.0 * KEN, DOMA, "Side door", "side")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    B.interior = True
    B.merge(FL.doma("floor", 0.0, W, -D, 0.0, road=(A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    pr = _pan(S, 2.0 * KEN, -1.55 * KEN)
    S.obst.append(("floor", _r(pr[0] - 0.10, pr[1] + 0.10, pr[2] - 0.10, pr[3])))
    fit(S, "fuel", "floor", rect=(A_ + 0.05, A_ + 2.15, -D + A_ + 0.05, -D + A_ + 1.75), obstacle=False,
        note="the fuel heap of pine needles and bamboo leaves [GYO]")
    S.place_windows()
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -A_), [S.dn["front"], S.dn["side"]],
           "the boiling floor: the shell pan on its firebox under the smoke vent, fuel, brine tubs, draining baskets")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "kamaya"}, "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"],
                        "pan": pr}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ yards
YARDS = {
    # the potter's yard: a light bamboo fence (yotsume) round the work shed and the drying racks; the gate (by the
    # picker: a 1.5-ken opening for the firewood carts) in the south line towards the kiln
    "potteryyard": dict(W=7 * KEN, D=6 * KEN, closed=True,
                        runs=[([(0.0, 0.0), (0.0, 6 * KEN), (7 * KEN, 6 * KEN), (7 * KEN, 0.0)], "yotsume", {},
                               ("end", "end"))],
                        gates=[(0, 3, 1.0 * KEN) + DW.pick_gate("yotsume", status="work", carts=True)]),
    # the tile works yard: a board fence (itabei) round the moulding shed, the drying shed and the kiln; the gate (by
    # the picker: a two-leaf board gate 1.5 ken for the tile carts) in the south line
    "tileyard": dict(W=10 * KEN, D=7 * KEN, closed=True,
                     runs=[([(0.0, 0.0), (0.0, 7 * KEN), (10 * KEN, 7 * KEN), (10 * KEN, 0.0)], "itabei",
                            dict(kuro=False, cap="none"), ("end", "end"))],
                     gates=[(0, 3, 2.0 * KEN) + DW.pick_gate("itabei", status="work", carts=True)]),
}
DW.COMPOUNDS.update(YARDS)


def compound(name=None, plot="tileyard", wear="_w1"):
    return DW.compound(name=name, plot=plot, wear=wear)


# ================================================================================================ dispatch
def _builders():
    return {k: globals().get(k) for k in KINDS}


def build(kind, **params):
    fn = _builders().get(kind)
    if fn is None:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return fn(**params)


def budget_class(kind, **params):
    """PLAYBOOK §12: the site objects and yards 'large' where they carry their own ground mass; huts 'standard'."""
    if kind in ("compound",):
        return "large"
    return "standard"


def over_budget_ok(kind, **params):
    """CA1: a deliberate overage (<= +50 %, PLAYBOOK §12) and its reason, or None."""
    if kind == "bunkhall":
        return ("a 6 x 3 ken board hall (the longest 'standard' hut: board walls + the raised floor, irori and stove over "
                "6 ken)%s" % (" under a stone-weighted roof: every weighting stone and batten is geometry"
                              if params.get("roof") == "ishioki" else ""))
    return None


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as tradesite.model."""
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
        if "hook" in g:
            g["hook"] = [round(g["hook"][0] - cx, 3), g["hook"][1], round(g["hook"][2] - cz, 3)]
        fits.append(g)
    info = dict(info, centre=(cx, cz), fittings_model=fits,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[(x - cx, z - cz, y) for (x, z, y) in info["passages"]])
    return M, floors, rooms, info
