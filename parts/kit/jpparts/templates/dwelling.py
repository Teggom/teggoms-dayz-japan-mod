"""The wave-3a dwelling template (D3, Phase C wave 3a, 2026-10-01): the mountain and coastal houses, the foot-soldier
row, the small samurai house, the two headman houses, the great merchant residence, the samurai mansion in three plot
sizes, the tea hut, the board storehouse, the stable, the bath hut, the gatehouse with rooms (nagaya-mon) and the
lords' inns (honjin omote + oku, waki-honjin). Bare shells (a furnisher dresses them); every shell lists its fixed-prop
spots in info['fittings']. Research per building: spikes/D3/D3_NOTES.md.

Built on templates/rural.py's Shell (posts on soseki, wall lines with openings, koyagumi under the roof, floors, the
kamachi) and the civic / sacred helpers. New here (built-in fittings, not props):
  ceiling()        a board ceiling (tenjo) with sao-buchi battens over the formal / family rooms (partitions close
                   up to it, FB2 C21)
  interior_gable() the plastered-board gable over a partition line perpendicular to the ridge, so a ceilinged zone and
                   an open-roofed kitchen zone are separate (no view into the attic)
  tokonoma()       the status alcove: toko board + lacquered tokogamachi, toko-bashira, otoshigake lintel + hanging
                   wall, and beside it the chigaidana (staggered shelves + fukurodana cupboard). PLAYBOOK §2.2: samurai,
                   honjin and the tea hut only (G1 A2: no tokonoma in commoner houses)
  genkan_porch()   the formal entrance porch on a gable end (the kuri pattern, W2S): kirizuma roof on two posts, a
                   cut-stone pad and the shikidai board step up to the door (status: samurai, honjin)
  shikidai_genkan() a recessed formal entrance INSIDE the envelope: its own door into a small genkan doma and the
                   shikidai board step up to the genkan room (the headman's "by permission" genkan, under the eave)
  hidana()         the slatted drying rack hung over a Hida / Kiso irori (sooted wood)
  jodan()          a raised tatami floor (+0.15) with its lacquered front edge (jodan-kamachi) and a hidden step ramp

    M, floors, rooms, info = dwelling.model(kind="mountain", roof="ishioki")

Kit frame (as rural.py): x 0..W along the front, z 0 = the front wall line, +z = out, z -D = back, y 0 = grade.
Levels (m): doma 0.05; raised floors 0.45 (rural) / 0.50 (samurai, headman, merchant, honjin); ceilings at the floor
+ 2.55 (tea room + 2.15).
"""
import math

from ..core import Part, box, prism, KEN, HALF, POST, KETA_H, LIBRARY, DOOR_H
from .. import walls, openings, roofs as R, roofparts, floors as FL, found, frame, gates as G, pits as PI, stall as SL
from .. import stilts as STL
from ..assemble import to_world
from .rural import (Shell, big_leaf, _gable_leanto, _kamado, _irori, ishioki_lod, _r, DOMA, A_, BOARDS_ROUGH,
                    _takahe, TAKAHE_MAT)
from .civic import fit, trim_lods, koshiyane
from .sacred import paving, stones_as_soseki

KINDS = ("mountain", "coastal", "kumi", "doshin", "headman_east", "headman_kinai", "merchant", "samurai", "chashitsu",
         "itagura", "stable", "furoba", "nagayamon", "honjin_omote", "honjin_oku", "wakihonjin")
FLOOR_R = 0.45                 # rural raised floor (mountain / coastal)
FLOOR = 0.50                   # samurai / headman / merchant / honjin raised floor (PLAYBOOK §4)
CEIL_H = 2.42                  # room height to the board ceiling (~8 shaku: 6-10 mat rooms; under the wagoya tie beams)
WOOD_I = "wood_interior" if "wood_interior" in LIBRARY else "wood_weathered"
PLASTER = "wall_shikkui_aged" if "wall_shikkui_aged" in LIBRARY else "wall_shikkui"
ATTIC_TAGS = ("ushibari", "tie_beam_k", "tsuka", "munazuka", "moya", "munagi", "sasu", "sumi_sasu", "tsuma_sasu",
              "collar", "nuki", "kaiko", "lashing", "hiuchi", "beam", "koya_beam", "koyabari", "tie")


# ================================================================================================ helpers
def ceiling(S, name, rect, y, battens=True):
    """A board ceiling (sao-buchi tenjo) over the kit-frame rect at height y (its underside): the boards + thin battens
    (sao-buchi, every ~0.45 m, along x). Interior, visual LODs 1-2 (no collision: nobody reaches it)."""
    x0, x1, z0, z1 = rect
    p = S.B.P(name)
    p.add(box(x0, x1, y, y + 0.03, z0, z1, "ceil_boards", vis=(1, 2), tag="tenjo"))
    if battens:
        n = max(2, int(round((z1 - z0) / 0.91)))
        for k in range(1, n):
            z = z0 + k * (z1 - z0) / n
            p.add(box(x0, x1, y - 0.025, y, z - 0.0125, z + 0.0125, WOOD_I, vis=(1,), tag="saobuchi"))
    S.B.interior = True
    S.B.merge(p)
    S.B.interior = False
    S.ceilings.append((rect, y))


def hide_attic(S, x0, x1, z0, z1, y):
    """Roof-frame members wholly inside the closed attic over ceilinged rooms (plan box x0..x1, z0..z1, above y) leave
    the visual LODs: nobody sees them (budget, PLAYBOOK §12). Members that reach the eaves or the open zone stay."""
    n = 0
    for s in S.H.solids:
        if not s.vis or s.geo or s.view or s.fire:
            continue
        b = s.bbox()
        if b[0] >= x0 - 1e-3 and b[1] <= x1 + 1e-3 and b[4] >= z0 - 1e-3 and b[5] <= z1 + 1e-3 and b[2] >= y - 1e-3:
            if s.tag in ("rafter", "kawara_field", "tile_bed", "board_field", "thatch_body"):
                continue
            s.vis = set()
            n += 1
    S.log.append("hide_attic: %d roof-frame solids over the ceilings left the visual LODs" % n)
    S.H.solids = [s for s in S.H.solids if s.vis or s.geo or s.view or s.fire]


def interior_gable(S, x, D, t, E, name, variant="_plain"):
    """walls.gable over the interior line x = const (perpendicular to the ridge), facing -x: closes the roof space above
    a full-height partition (the kitchen side stays open to the roof, the ceilinged side gets a closed attic)."""
    g = S.B.P(name)
    if variant == "_plain":
        # a plain plastered gable (interior clay): walls.gable _tile minus its outside dressing (boards, bosses, band)
        walls.gable(g, D, t, E, "_tile")
        g.solids = [s for s in g.solids if s.tag not in ("boss", "board_band", "band")]
        from .sacred import remat
        remat(g, "wall_shikkui", "wall_nakanuri_int")
    else:
        walls.gable(g, D, t, E, variant)
    for s in g.solids:
        if s.tag == "gable_geo":
            s.vis = {1}
    # the infill runs up to the roof line: tagged as a roof-closing panel (parttop C21 reads a panel's bbox top, which
    # over a sloped top is above the roof at the low end of each column)
    for s in g.solids:
        if s.tag == "gable_infill":
            s.tag = "roof_gable"
    S.B.interior = True
    S.B.put(g, (90.0, (x, 0.0, -D)), what="walls.gable %s over the interior line x %.2f (%s)" % (variant, x, name))
    S.B.interior = False


def wall_frame(x=None, z=None, L=None, D=None):
    """Frames for interior lines: x = const (local lx = z + D, local +z -> -x) or z = const (local lx = x - x0)."""
    if x is not None:
        return (90.0, (x, 0.0, -D))
    return (0.0, (0.0, 0.0, z))


def tokonoma(S, room, fr, a, b, c, floor_y, ceil_y, depth=HALF, wall_a=True, wall_c=True, chigai=True, post_at="b"):
    """The tokonoma (a..b) + the chigaidana (b..c) along a wall: fr = that wall's frame (local x along the wall, local
    +z OUT of the room: the alcove lies at local z -depth..0 inside the room). a, b, c local x (clear of the wall
    posts). wall_a / wall_c: side walls (fukurokabe) at a / c (False where a room wall already stands there)."""
    p = S.B.P("tokonoma_%s" % room)
    zf = -depth
    zb = -0.045                                    # just inside the wall's inner face (infill 0.075 / 2)
    kw = dict(geo=True, view=True, fire=True)
    yl = floor_y + 1.85                            # otoshigake / chigaidana lintel underside
    if post_at == "a" and not chigai:
        # a single toko whose post stands on the open side `a` (the tea room's alcove): the post at a, the board
        # from it to b (a wall / corner), its side wall at the post
        p.add(box(a + 0.055, b, floor_y, floor_y + 0.12, zf + 0.03, zb, {"top": "floor_boards_int", "default": WOOD_I},
                  vis=(1, 2), tag="toko_board", **kw))
        p.add(box(a + 0.055, b, floor_y, floor_y + 0.13, zf - 0.03, zf + 0.03, "lacquer_black", vis=(1, 2),
                  tag="tokogamachi", **kw))
        p.add(box(a - 0.055, a + 0.055, floor_y, ceil_y, zf - 0.055, zf + 0.055, WOOD_I, vis=(1, 2), tag="tokobashira",
                  **kw))
        p.add(box(a - 0.015, a + 0.015, floor_y, ceil_y, zf + 0.055, zb, "wall_nakanuri_int", vis=(1, 2),
                  tag="toko_side_wall", **kw))
        yl = floor_y + 1.70
        p.add(box(a + 0.055, b, yl, yl + 0.06, zf - 0.03, zf + 0.03, WOOD_I, vis=(1, 2), tag="otoshigake"))
        p.add(box(a + 0.055, b, yl + 0.06, ceil_y, zf - 0.015, zf + 0.015, "wall_nakanuri_int", vis=(1, 2),
                  tag="toko_kokabe"))
        S.B.interior = True
        S.B.put(p, fr, what="tokonoma, post on the open side (%s)" % room)
        S.B.interior = False
        p0 = to_world(fr, a - 0.08, 0.0)
        p1 = to_world(fr, b + 0.05, zf - 0.10)
        rect = _r(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1]))
        S.obst.append((room, rect))
        S.fittings.append({"kind": "tokonoma", "room": room, "rect": rect, "y": round(floor_y + 0.12, 3),
                           "note": "tokonoma (one scroll, one flower)"})
        return
    # the toko: board floor + lacquered front edge (tokogamachi)
    p.add(box(a, b - 0.055, floor_y, floor_y + 0.12, zf + 0.03, zb, {"top": "floor_boards_int", "default": WOOD_I},
              vis=(1, 2), tag="toko_board", **kw))
    p.add(box(a, b - 0.055, floor_y, floor_y + 0.13, zf - 0.03, zf + 0.03, "lacquer_black", vis=(1, 2),
              tag="tokogamachi", **kw))
    # the toko-bashira between the toko and the shelves (often a natural log in the period; planed here)
    p.add(box(b - 0.055, b + 0.055, floor_y, ceil_y, zf - 0.055, zf + 0.055, WOOD_I, vis=(1, 2), tag="tokobashira",
              **kw))
    p.add(box(b - 0.015, b + 0.015, floor_y, ceil_y, zf + 0.055, zb, "wall_nakanuri_int", vis=(1, 2),
              tag="toko_side_wall", **kw))
    if wall_a:
        p.add(box(a - 0.03, a, floor_y, ceil_y, zf, zb, "wall_nakanuri_int", vis=(1, 2), tag="toko_side_wall", **kw))
    x_end = c if chigai else b
    if chigai and wall_c:
        p.add(box(c, c + 0.03, floor_y, ceil_y, zf, zb, "wall_nakanuri_int", vis=(1, 2), tag="toko_side_wall", **kw))
    # the lintel (otoshigake) over the alcove front + the hanging wall above it to the ceiling
    p.add(box(a, b - 0.055, yl, yl + 0.07, zf - 0.03, zf + 0.03, WOOD_I, vis=(1, 2), tag="otoshigake"))
    p.add(box(a, b - 0.055, yl + 0.07, ceil_y, zf - 0.015, zf + 0.015, "wall_nakanuri_int", vis=(1, 2),
              tag="toko_kokabe"))
    if chigai:
        m = (b + c) / 2
        p.add(box(b + 0.055, c, floor_y, floor_y + 0.10, zf + 0.03, zb, {"top": "floor_boards_int", "default": WOOD_I},
                  vis=(1, 2), tag="jidana", **kw))
        p.add(box(b + 0.055, m + 0.06, floor_y + 0.95, floor_y + 0.98, zf + 0.06, zb, WOOD_I, vis=(1, 2),
                  tag="chigaidana"))
        p.add(box(m - 0.06, c, floor_y + 1.17, floor_y + 1.20, zf + 0.06, zb, WOOD_I, vis=(1, 2), tag="chigaidana"))
        p.add(box(m - 0.012, m + 0.012, floor_y + 0.98, floor_y + 1.17, zf + 0.08, zf + 0.104, "lacquer_black",
                  vis=(1,), tag="ebizuka"))
        p.add(box(b + 0.055, c, floor_y + 1.55, yl, zf + 0.06, zb, WOOD_I, vis=(1, 2), tag="fukurodana"))
        p.add(box(b + 0.075, c - 0.02, floor_y + 1.58, yl - 0.03, zf + 0.055, zf + 0.06, "paper_fusuma", vis=(1,),
                  tag="fukurodana_door"))
        p.add(box(b + 0.055, c, yl, yl + 0.07, zf - 0.03, zf + 0.03, WOOD_I, vis=(1, 2), tag="otoshigake"))
        p.add(box(b + 0.055, c, yl + 0.07, ceil_y, zf - 0.015, zf + 0.015, "wall_nakanuri_int", vis=(1, 2),
                  tag="toko_kokabe"))
    S.B.interior = True
    S.B.put(p, fr, what="tokonoma%s (%s)" % (" + chigaidana" if chigai else "", room))
    S.B.interior = False
    p0 = to_world(fr, a - 0.05, 0.0)
    p1 = to_world(fr, x_end + 0.05, zf - 0.10)
    rect = _r(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1]))
    S.obst.append((room, rect))
    S.fittings.append({"kind": "tokonoma", "room": room, "rect": rect, "y": round(floor_y + 0.12, 3),
                       "note": "tokonoma (hanging scroll + flower / incense on the toko board)" +
                               (" + chigaidana (staggered shelves, fukurodana)" if chigai else "")})


def hidana(S, room, cx, cz, y_bottom, y_beam, w=1.25, d=1.10):
    """A slatted drying rack (hidana) hung over the irori (Hida / Kiso): a frame + slats at y_bottom, four hangers up to
    the tie beam underside y_beam. Sooted. Visual only (it hangs over the hearth, a floor obstacle)."""
    p = S.B.P("hidana")
    m = "wood_sooted"
    x0, x1, z0, z1 = cx - w / 2, cx + w / 2, cz - d / 2, cz + d / 2
    y0, y1 = y_bottom, y_bottom + 0.05
    for (a, b, c, e) in ((x0, x1, z0, z0 + 0.05), (x0, x1, z1 - 0.05, z1)):
        p.add(box(a, b, y0, y1, c, e, m, vis=(1, 2), tag="hidana_frame"))
    for (a, b) in ((x0, x0 + 0.05), (x1 - 0.05, x1)):
        p.add(box(a, b, y0 - 0.04, y0 + 0.01, z0, z1, m, vis=(1, 2), tag="hidana_frame"))
    k = x0 + 0.13
    while k < x1 - 0.10:
        p.add(box(k - 0.02, k + 0.02, y1, y1 + 0.025, z0 + 0.01, z1 - 0.01, "bamboo_sooted", vis=(1,), tag="hidana_slat"))
        k += 0.11
    for (x, z) in ((x0 + 0.03, z0 + 0.03), (x1 - 0.03, z0 + 0.03), (x0 + 0.03, z1 - 0.03), (x1 - 0.03, z1 - 0.03)):
        p.add(box(x - 0.012, x + 0.012, y1, y_beam + 0.02, z - 0.012, z + 0.012, m, vis=(1,), tag="hidana_hanger"))
    S.B.interior = True
    S.B.merge(p)
    S.B.interior = False
    S.fittings.append({"kind": "hidana", "room": room, "rect": (round(x0, 3), round(x1, 3), round(z0, 3), round(z1, 3)),
                       "y": round(y1 + 0.025, 3), "note": "the drying rack over the irori (built in): firewood, "
                       "chestnuts, straw boots dry here (visual only)"})


def plaster_exterior(S, W, D, mat=PLASTER, tags=("infill", "kokabe", "infill_base", "gable_infill")):
    """White plaster OUTSIDE (shikkui), the interior clay inside (T6): every face of an exterior wall-infill solid that
    looks out of the footprint becomes `mat` (the kinai takahe gables' method, FB2)."""
    from ..core import face_uvs
    n = 0
    cx, cz = W / 2, -D / 2
    for s_ in S.H.solids:
        if s_.tag not in tags or not s_.fn or s_.fm is None:
            continue
        b = s_.bbox()
        on_line = (abs(b[4] - 0.0) < 0.10 or abs(b[5] - 0.0) < 0.10 or abs(b[4] + D) < 0.10 or abs(b[5] + D) < 0.10 or
                   abs(b[0]) < 0.10 or abs(b[1]) < 0.10 or abs(b[0] - W) < 0.10 or abs(b[1] - W) < 0.10)
        if not on_line or getattr(s_, "interior", False):
            continue
        for fi, n_ in enumerate(s_.fn):
            if abs(n_[1]) > 0.5:
                continue
            fc = s_.center
            out = (n_[0] * (fc[0] - cx) + n_[2] * (fc[2] - cz)) > 0.0
            near = (abs(fc[2]) < 0.15 and n_[2] > 0.9) or (abs(fc[2] + D) < 0.15 and n_[2] < -0.9) or \
                   (abs(fc[0]) < 0.15 and n_[0] < -0.9) or (abs(fc[0] - W) < 0.15 and n_[0] > 0.9)
            if out and near:
                s_.fm[fi] = mat
                s_.fuv[fi] = face_uvs(s_, fi, n_, mat)
                n += 1
    S.log.append("plaster_exterior: %d outward wall faces -> %s" % (n, mat))


def genkan_porch(S, side, zc, floor_y, fam, E_main, door_part=None, label="Genkan door", room="genkan"):
    """The formal entrance porch on a gable end (W2S kuri pattern): two posts 1 ken out, a kirizuma roof (ridge
    square to the wall), a cut-stone pad, the shikidai board step up to a door in the gable wall at floor_y. zc = the
    door's centre z (kit frame). Returns the door key 'genkan'. The wall_line of that gable must leave the door bay
    (lx0, lx0 + 1 ken) open with a plain half-ken after it (single door)."""
    W, D = S.W, S.D
    sg = 1 if side == "right" else -1
    xw = W if side == "right" else 0.0
    xp = xw + sg * KEN
    zf, zb = zc + 0.75 * KEN, zc - 0.75 * KEN
    ye = 2.95
    for z in (zf, zb):
        S.post(round(xp, 4), round(z, 4), ye - KETA_H)
    pk = Part("genkan_keta_%s" % side, "", "")
    xa, xb = (xw + 0.06, xp + 0.30) if sg > 0 else (xp - 0.30, xw - 0.06)
    for z in (zf, zb):
        pk.add(box(xa, xb, ye - KETA_H, ye, z - 0.06, z + 0.06, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
                   fire=True, tag="keta"))
    pk.add(box(xp - 0.06, xp + 0.06, ye - KETA_H - 0.25, ye - KETA_H, zb, zf, "wood_weathered", vis=(1, 2), geo=True,
               view=True, fire=True, tag="genkan_beam"))
    S.H.merge(pk)
    gp = Part("genkan_roof_%s" % side, "", "")
    gov = R.GABLE_OV[fam]
    if sg > 0:
        x_in = xw + 0.08 + gov
        Lr = xp + 0.30 - x_in - gov
        x_org = x_in
    else:
        x_org = xp - 0.30 + gov
        Lr = (xw - 0.08 - gov) - x_org
    R.roof(gp, Lr, zf - zb, "kirizuma", fam, eave_y=ye, ov=0.55, gov=gov)
    S.H.merge(gp.transformed(0.0, (x_org, 0.0, zf)))
    pa, pb = (xw + 0.10, xp + 0.45) if sg > 0 else (xp - 0.45, xw - 0.10)
    paving(S.H, pa, pb, zb - 0.45, zf + 0.45, y=DOMA, name="genkan_pad_%s" % side)
    lx_c = (-zc) if sg > 0 else (zc + D)
    st = Part("shikidai_%s" % side, "", "")
    found.step(st, lx_c, "wood", drop=floor_y - DOMA, width=1.20)
    S.B.put(st, S.F[side], 0.0, floor_y, what="found.step (wood): the shikidai board step (%s gable)" % side)
    S.door(door_part or openings.part_shoji_ext("_single"), side, lx_c - 0.5 * KEN, floor_y, label, "genkan")
    ra, rb = (xw + 0.70, xp + 0.38) if sg > 0 else (xp - 0.38, xw - 0.70)
    S.room("genkan_porch", "yard", "stone", DOMA, (ra, rb, zb - 0.38, zf + 0.38), [S.dn["genkan"]],
           "the genkan porch: stone pad, the shikidai board step up to the formal entrance", enclosed=False)
    oa, ob = (xw, xw + 0.80) if sg > 0 else (xw - 0.80, xw)
    S.obst.append(("genkan_porch", _r(oa, ob, zc - 0.65, zc + 0.65)))
    S.log.append("genkan porch on the %s gable, door centre z %.2f, posts x %.2f" % (side, zc, xp))
    return "genkan"


def shikidai_edge(S, fr, L, floor_y, step_at, doma_room, width=1.20):
    """An open raised-floor edge onto a small genkan doma with the SHIKIDAI (a wide board step, not a stone): the
    kamachi (lacquered on status houses) + the found.step 'wood' box with its hidden ramp. fr: local x along the edge
    (0..L), local +z into the doma."""
    s = S.B.P("shikidai_kamachi")
    s.add(box(0.0, L, DOMA, floor_y - 0.15, -0.03, 0.03, "wood_weathered", vis=(1, 2), geo=True, view=True, fire=True,
              tag="yukashita_boards"))
    s.add(box(0.0, L, floor_y - 0.15, floor_y, -0.06, 0.06, "lacquer_black", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="agari_kamachi"))
    S.B.interior = True
    S.B.put(s, fr)
    for cx in step_at:
        st = S.B.P("shikidai_%d" % int(cx * 100))
        run = found.step(st, cx, "wood", drop=floor_y - DOMA, width=width)
        S.B.put(st, fr, 0.0, floor_y, what="found.step (wood): the shikidai inside the genkan")
        p0 = to_world(fr, cx - width / 2 - 0.04, 0.0)
        p1 = to_world(fr, cx + width / 2 + 0.04, run + 0.06)
        S.obst.append((doma_room, _r(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1]))))
    S.B.interior = False


def hidden_ramp(S, fr, cx, width, drop, top_y, room=None, angle=34.0):
    """An invisible walk ramp (found.step's hidden ramp without the visible step): from the sill at local z 0 (y top_y)
    down `drop` towards local +z; Geometry + Roadway only. Its footprint is an obstacle of `room` (the low side)."""
    run = drop / math.tan(math.radians(angle))
    p = S.B.P("ramp_%d" % int(cx * 100))
    x0, x1 = cx - width / 2, cx + width / 2
    p.add(prism([(0.0, 0.0), (-drop, 0.0), (-drop, run)], "x", x0, x1, "stone_field", vis=(), geo=True, view=False,
                fire=None, tag="ramp"))
    p.road([(x0, 0.0, 0.0), (x1, 0.0, 0.0), (x1, -drop, run), (x0, -drop, run)], "boards_ext")
    S.B.put(p, fr, 0.0, top_y, what="hidden ramp (drop %.2f) at %.2f" % (drop, cx))
    if room:
        p0 = to_world(fr, x0 - 0.05, 0.0)
        p1 = to_world(fr, x1 + 0.05, run + 0.08)
        S.obst.append((room, _r(min(p0[0], p1[0]), max(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[1], p1[1]))))
    return run


# ------------------------------------------------------------------------------------------------ fusuma
def leaf_fusuma(frame_mat="lacquer_black"):
    """A fusuma leaf (opaque paper panel in a thin black-lacquered rim): the room-to-room sliding door of samurai and
    upper houses (shoji stay on the outside walls). Collision / far LODs = the kit's one-box leaf."""
    def build(l0, l1, bot, top, z0, z1, bone, dirn=+1):
        pm = {"front": "paper_fusuma", "back": "paper_fusuma", "default": frame_mat}
        out = [box(l0, l1, bot, top, z0, z1, pm, vis=(2, 3), geo=True, view=True, fire="fabric_thin", uv="fit",
                   tag="leaf")]
        fw = 0.022
        out += [box(l0, l0 + fw, bot, top, z0, z1, frame_mat, vis=(1,), tag="fusuma_frame"),
                box(l1 - fw, l1, bot, top, z0, z1, frame_mat, vis=(1,), tag="fusuma_frame"),
                box(l0 + fw, l1 - fw, top - fw, top, z0, z1, frame_mat, vis=(1,), tag="fusuma_frame"),
                box(l0 + fw, l1 - fw, bot, bot + fw, z0, z1, frame_mat, vis=(1,), tag="fusuma_frame"),
                box(l0 + fw, l1 - fw, bot + fw, top - fw, z0 + 0.002, z1 - 0.002,
                    {"front": "paper_fusuma", "back": "paper_fusuma", "default": "paper_fusuma"}, vis=(1,), uv="fit",
                    tag="fusuma_leaf_panel")]
        return out
    return build


def part_fusuma(variant="_hikiwake"):
    """Fusuma doors as DoorsTwin parts (openings' hikiwake / single builders with the fusuma leaf)."""
    if variant == "_hikiwake":
        return openings.hikiwake_door_part("jp_p_open_fusuma", "_hikiwake", [3],
                                           "fusuma pair parting in the middle between tatami rooms (samurai / upper)",
                                           leaf_fusuma(), "shoji", -1, 0.03, note="paper panels, lacquered rims")
    return openings.single_door_part("jp_p_open_fusuma", "_single", [3],
                                     "single fusuma beside a fixed panel between tatami rooms",
                                     leaf_fusuma(), "shoji", -1, 0.03, note="paper panel, lacquered rim", panel="shoji")


# ------------------------------------------------------------------------------------------------ small parts
def nijiriguchi(S, side, lx, y_sill, w=0.66, h=0.72):
    """The tea room's crawl-in door as a static (closed) board door with its frame on the wall face (decorative, D9:
    the way in is a normal door)."""
    p = S.B.P("nijiriguchi")
    zf = POST / 2 + 0.002
    m = "wood_weathered"
    p.add(box(lx - 0.04, lx + w + 0.04, y_sill - 0.04, y_sill, zf, zf + 0.04, m, vis=(1, 2), tag="nijiri_frame"))
    p.add(box(lx - 0.04, lx + w + 0.04, y_sill + h, y_sill + h + 0.04, zf, zf + 0.04, m, vis=(1, 2), tag="nijiri_frame"))
    for xx in (lx - 0.04, lx + w):
        p.add(box(xx, xx + 0.04, y_sill, y_sill + h, zf, zf + 0.04, m, vis=(1, 2), tag="nijiri_frame"))
    k = 0.0
    while k < w - 1e-3:
        e = min(w, k + 0.16)
        p.add(box(lx + k + 0.002, lx + e - 0.002, y_sill, y_sill + h, zf + 0.01, zf + 0.03, m, vis=(1,), tag="nijiri_board"))
        k = e
    p.add(box(lx, lx + w, y_sill, y_sill + h, zf, zf + 0.01, "wood_sooted", vis=(1, 2), tag="nijiri_back"))
    S.B.put(p, S.F[side], what="nijiri-guchi (static, closed) on the %s wall at %.2f" % (side, lx))


# ================================================================================================ DW08 mountain house
def mountain(name=None, roof="ishioki", leanto=None, doma="left", wear="_w2"):
    """Kiso / Hida mountain house: W 6 x D 4 ken, low-pitched kirizuma of stone-weighted boards (ishioki, T40), board
    walls, sooted log koyagumi. Doma x 0..2 ken (front big door, back door, kamado), the oe (irori room, boards, the
    hidana over the irori) x 2..4 ken full depth open to the doma, dei (front) / nando (back) x 4..6 ken."""
    W, D = 6 * KEN, 4 * KEN
    E = 3.20
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[roof]
    FL_ = FLOOR_R
    XD, XR, ZS = 2 * KEN, 4 * KEN, -2 * KEN
    S = Shell(name or "jp_mountain", W, D, [1, 2], "mountain board-roof house (DW08)", wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, soot=True, members="log", slim_x=(XR,))
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    S.wall_line("front", [(0.0, XD, DOMA), (XD, W, FL_)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (2.5 * KEN, 3.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"),
                 (4.5 * KEN, 5.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window")],
                nodes_extra=(2.5 * KEN, 3.0 * KEN, 4.5 * KEN, 5.0 * KEN), **bw)
    S.door(big_leaf("_battened"), "front", 0.0, DOMA, "Front door (ooto, doma)", "front")
    S.window(openings.part_window_slide("_board"), "front", 2.5 * KEN, FL_, "Oe window (front)")
    S.window(openings.part_window_slide("_board"), "front", 4.5 * KEN, FL_, "Dei window (front)")
    # back: lx = W - x; doma lx 4K..6K (back door lx 4.5K..5.5K, parks 5.5K..6K), oe lx 2K..4K, nando lx 0..2K
    S.wall_line("back", [(0.0, W - XD, FL_), (W - XD, W, DOMA)], YT,
                [(4.5 * KEN, 5.5 * KEN, DOMA, DOMA + 2.0, "door"), (2.5 * KEN, 3.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"),
                 (0.5 * KEN, 1.0 * KEN, FL_ + 0.90, FL_ + 1.60, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 2.5 * KEN, 3.0 * KEN, 4.5 * KEN, 5.5 * KEN), **bw)
    S.door(openings.part_itado("_single"), "back", 4.5 * KEN, DOMA, "Back door (doma)", "back")
    S.window(openings.part_window_slide("_board"), "back", 2.5 * KEN, FL_, "Oe window (back)")
    S.window(openings.part_tsukiage("_board"), "back", 0.5 * KEN, FL_, "Nando window (back, push-up shutter)")
    # left gable (doma, lx = z + D): a window; right gable (rooms, lx = -z): dei window, nando push-up
    S.wall_line("left", [(0.0, D, DOMA)], YG, [(2.5 * KEN, 3.0 * KEN, DOMA + 0.95, DOMA + 1.70, "window")],
                nodes_extra=(2.5 * KEN, 3.0 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "left", 2.5 * KEN, DOMA + 0.05, "Doma window (end)")
    S.wall_line("right", [(0.0, D, FL_)], YG, [(0.5 * KEN, 1.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"),
                                              (2.5 * KEN, 3.0 * KEN, FL_ + 0.90, FL_ + 1.60, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 2.5 * KEN, 3.0 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "right", 0.5 * KEN, FL_, "Dei window (end)")
    S.window(openings.part_tsukiage("_board"), "right", 2.5 * KEN, FL_, "Nando window (end, push-up shutter)")
    for side in ("left", "right"):
        S.gable(side, D, t, E, "_board")
    # partitions: x = XR (oe | dei, nando) with two doors; z = ZS (dei | nando)
    PT = FL_ + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F_P = (90.0, (XR, 0.0, -D))
    yb = S.beam_over(F_P, D)
    PT_X = yb + 0.10 if yb else PT
    S.wall_line((F_P, D, "part_x"), [(0.0, D, FL_)], PT_X,
                [(0.5 * KEN, 1.5 * KEN, FL_, FL_ + 2.0, "door"), (2.5 * KEN, 3.5 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both")
    S.door(openings.part_itado("_single"), F_P, 0.5 * KEN, FL_, "Oe -> nando", "nando")
    S.door(openings.part_shoji_ext("_single"), F_P, 2.5 * KEN, FL_, "Oe -> dei", "dei")
    F_Z = (0.0, (XR, 0.0, ZS))
    S.wall_line((F_Z, W - XR, "part_z"), [(0.0, W - XR, FL_)], PT, (), finish="nakanuri", grime=False, interior="both")
    B.interior = False
    S.head_beam(F_Z, W - XR, PT, "part_z_head")
    if not yb:
        S.head_beam(F_P, D, PT, "part_x_head")
    # floors
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XD, -D, 0.0, road=(A_, XD - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    pit = _irori(S, "oe", 3.0 * KEN, -2.0 * KEN, False, FL_, K["levels"])
    B.merge(FL.boards("oe", XD + 0.06, XR - A_, -D + A_, -A_, FL_, holes=[pit + ("pit",)], hole_fn=PI.pit_fn("irori"),
                      mats=BOARDS_ROUGH))
    B.merge(FL.boards("dei", XR + A_, W - A_, ZS + A_, -A_, FL_, mats=BOARDS_ROUGH))
    B.merge(FL.boards("nando", XR + A_, W - A_, -D + A_, ZS - A_, FL_, mats=BOARDS_ROUGH))
    B.interior = False
    S.kamachi((90.0, (XD, 0.0, -D)), D, FL_, [1.0 * KEN, 3.0 * KEN], "doma")
    _kamado(S, "doma", 0.50, -2.5 * KEN, 90.0)
    hook = [f for f in S.fittings if f["kind"] == "irori"][0]["hook"]
    hidana(S, "oe", 3.0 * KEN, -2.0 * KEN, FL_ + 1.80, hook[1] + 0.30)
    if leanto:
        _gable_leanto(S, "left" if doma == "left" else "right", "ishioki" if roof == "ishioki" else "itabuki", E, t)
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, (A_, XD - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "doma: entry, the kamado on the end wall, snow gear and firewood")
    S.room("oe", "daidokoro", "boards", FL_, (XD + 0.07, XR - A_, -D + A_, -A_), [S.dn["nando"], S.dn["dei"]],
           "oe: the irori room with the hidana rack, open to the doma")
    S.room("dei", "living", "boards", FL_, (XR + A_, W - A_, ZS + A_, -A_), [S.dn["dei"]], "dei (front room)")
    S.room("nando", "sleeping", "boards", FL_, (XR + A_, W - A_, -D + A_, ZS - A_), [S.dn["nando"]], "nando")
    trim_lods(S.H, stones_keep=2)
    H, info = S.finish({"params": {"kind": "mountain", "roof": roof, "leanto": leanto},
                        "levels": {"doma": DOMA, "floor": FL_, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


# ================================================================================================ DW09 coastal house
def coastal(name=None, roof="ishioki", netstore=True, wear="_w2"):
    """Fisherman's house: W 4 x D 3 ken, board walls, kirizuma (stone-weighted boards or thatch); a big doma x 0..1.5
    ken for the nets, two board rooms (front living with the irori, back sleeping); the net store as an open lean-to on
    the doma gable."""
    W, D = 4 * KEN, 3 * KEN
    E = 3.30 if roof == "thatch" else 3.10          # thatch: the log ushibari sit lower (door head >= 2.00, D2)
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[roof]
    FL_ = FLOOR_R
    XD, ZS = 1.5 * KEN, -1.5 * KEN
    S = Shell(name or "jp_coastal", W, D, [1, 2], "coastal house (DW09)", wear)
    S.ceilings = []
    B = S.B
    ov = 0.90 if roof == "thatch" else None
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, ov=ov, soot=True, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    S.wall_line("front", [(0.0, XD, DOMA), (XD, W, FL_)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (3.0 * KEN, 3.5 * KEN, FL_ + 0.90, FL_ + 1.65, "window")],
                nodes_extra=(1.5 * KEN, 3.0 * KEN, 3.5 * KEN), **bw)
    S.door(big_leaf("_plain"), "front", 0.0, DOMA, "Front door (doma)", "front")
    S.window(openings.part_window_slide("_board"), "front", 3.0 * KEN, FL_, "Living window (front)")
    # back (lx = W - x): rooms lx 0..2.5K, doma lx 2.5K..4K: back door lx 2.5K..3.5K? its leaf parks over 3.5K..4K
    S.wall_line("back", [(0.0, W - XD, FL_), (W - XD, W, DOMA)], YT,
                [(2.5 * KEN, 3.5 * KEN, DOMA, DOMA + 2.0, "door"), (0.5 * KEN, 1.0 * KEN, FL_ + 0.90, FL_ + 1.60, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 2.5 * KEN, 3.5 * KEN), **bw)
    S.door(openings.part_itado("_single"), "back", 2.5 * KEN, DOMA, "Back door (doma)", "back")
    S.window(openings.part_tsukiage("_board"), "back", 0.5 * KEN, FL_, "Back room window (push-up shutter)")
    S.wall_line("left", [(0.0, D, DOMA)], YG, (), **bw)
    S.wall_line("right", [(0.0, D, FL_)], YG, [(0.5 * KEN, 1.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN), **bw)
    S.window(openings.part_window_slide("_board"), "right", 0.5 * KEN, FL_, "Living window (end)")
    for side in ("left", "right"):
        S.gable(side, D, t, E, "_board", thatch=(roof == "thatch"))
    PT = FL_ + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F_Z = (0.0, (XD, 0.0, ZS))
    S.wall_line((F_Z, W - XD, "part_z"), [(0.0, W - XD, FL_)], PT, [(0.5 * KEN, 1.5 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.0 * KEN))
    S.door(openings.part_itado("_single"), F_Z, 0.5 * KEN, FL_, "Living -> back room", "back_room")
    B.interior = False
    S.head_beam(F_Z, W - XD, PT, "part_z_head")
    B.interior = True
    B.merge(FL.doma("doma", 0.0, XD, -D, 0.0, road=(A_, XD - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    pit = _irori(S, "living", 2.75 * KEN, -0.75 * KEN, True, FL_, K["levels"], size=(0.91, 0.91))
    B.merge(FL.boards("living", XD + 0.06, W - A_, ZS + A_, -A_, FL_, holes=[pit + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    B.merge(FL.boards("back_room", XD + 0.06, W - A_, -D + A_, ZS - A_, FL_, mats=BOARDS_ROUGH))
    B.interior = False
    S.kamachi((90.0, (XD, 0.0, -D)), D, FL_, [2.25 * KEN], "doma")
    _kamado(S, "doma", 0.50, -2.2 * KEN, 90.0, size=(0.70, 0.70))
    fit(S, "net_hooks", "doma", rect=(A_ + 0.02, A_ + 0.12, -1.6 * KEN, -0.4 * KEN), obstacle=False,
        note="nets, floats and the octopus pots hung on the doma end wall (wall-hung props)")
    if netstore:
        _gable_leanto(S, "left", "ishioki" if roof == "ishioki" else "itabuki", E, t)
        S.rooms[-1]["note"] = "the net store: an open lean-to on the doma gable (net racks, floats, tar tub)"
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, (A_, XD - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "the big doma for the nets: the kamado, net-mending space")
    S.room("living", "daidokoro", "boards", FL_, (XD + 0.07, W - A_, ZS + A_, -A_), [S.dn["back_room"]],
           "front board room with the irori, open to the doma")
    S.room("back_room", "sleeping", "boards", FL_, (XD + 0.07, W - A_, -D + A_, ZS - A_), [S.dn["back_room"]],
           "back board room")
    trim_lods(S.H, stones_keep=2)
    H, info = S.finish({"params": {"kind": "coastal", "roof": roof, "netstore": netstore},
                        "levels": {"doma": DOMA, "floor": FL_, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


# ================================================================================================ town residences
G455 = 0.455


def _snap(v):
    return round(round(v / G455) * G455, 4)


def _residence(S, W, D, XD, XK, cols, ZS, fam, E, names, tags, notes, floor_y=FLOOR, porch="porch", toko=True,
               chigai=True, jodan=False, engawa=True, irori=True, side_door=None, plaster=True, kamado_n=2,
               gable="_tile", porch_fam=None, front_windows=True):
    """The shared plan of the samurai houses, the merchant residence and the honjin blocks (kit frame):
       x 0..XD   the kitchen doma (front ooto, back door, the kamado on the end wall)         [XD = 0: no kitchen]
       x XD..XK  the daidokoro (boards, irori), open to the doma over the kamachi and to the sooted roof
       x = XK    a full-height partition + an interior gable (the attic over the rooms is closed)    [XK = 0: none]
       x XK..W   ceilinged tatami rooms on a grid: columns `cols` (x nodes XK..W), rows front (z 0..ZS) / back (ZS..-D)
    names / tags / notes: {"f0": .., "b0": ..} per grid cell (f = front row, b = back row, index from the left).
    The back-right cell is the formal room (tokonoma + chigaidana on the right gable; raised jodan if jodan), the
    front-right cell the genkan room (porch = 'porch': the genkan porch + shikidai on the right gable; 'step': a door
    with a cut stone step, the lower samurai's plain entrance; None). engawa: a veranda along the back (garden) wall of
    the rooms, roofed by the main eave (ov 1.45), a stone step down at its kitchen end. side_door 'left' | 'right': a
    door at floor level on that gable's front row (the covered corridor to another block attaches there)."""
    B = S.B
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    CEIL = floor_y + CEIL_H
    nf = len(cols) - 1
    kitchen = XD > 0
    xs = []
    k = 1
    while k * KEN < W - 0.30:
        if abs(k * KEN - XK) > 0.05:
            xs.append(round(k * KEN, 4))
        k += 1
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=1.45 if engawa else None, soot=kitchen, members="sawn", xs=xs)
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    rd, fd = D + ZS, -ZS                   # back-row depth, front-row depth
    # ------------------------------------------------ front wall (z 0, lx = x)
    ff, nodes = [], [c for c in cols]
    d0 = None
    if kitchen:
        d0 = 0.0 if XD <= 1.5 * KEN + 1e-6 else 0.5 * KEN
        ff.append((d0, d0 + KEN, DOMA, DOMA + 2.0, "door"))
        nodes += [d0, d0 + KEN, d0 + 2 * KEN, XD]
    wins_f = []
    if front_windows:
        for i in range(nf):
            a = cols[i]
            if cols[i + 1] - a >= 1.5 * KEN - 1e-6:
                ff.append((a + 0.5 * KEN, a + 1.0 * KEN, floor_y + 0.45, floor_y + 2.0, "window"))
                nodes += [a + 0.5 * KEN, a + 1.0 * KEN]
                wins_f.append(a + 0.5 * KEN)
    zones = [(0.0, XD, DOMA), (XD, W, floor_y)] if kitchen else [(0.0, W, floor_y)]
    S.wall_line("front", zones, YT, ff, finish=fin, koshiita=kosh,
                nodes_extra=tuple(sorted(set(round(n, 4) for n in nodes))))
    if kitchen:
        S.door(big_leaf("_battened"), "front", d0, DOMA, "Kitchen door (ooto, doma)", "front")
    for a in wins_f:
        S.window(openings.part_window_slide("_shoji"), "front", a, floor_y, "Window (front, koshi + shoji)")
    # ------------------------------------------------ back wall (z -D, lx = W - x)
    bf, nodes = [], [W - c for c in cols]
    en_doors = []
    if kitchen:
        if XD < 1.5 * KEN - 1e-6:
            raise ValueError("kitchen doma narrower than 1.5 ken: no room for the back door")
        bf.append((W - XD, W - XD + KEN, DOMA, DOMA + 2.0, "door"))
        nodes += [W - XD, W - XD + KEN, W - XD + 1.5 * KEN]
        if XK - XD >= 1.25 * KEN - 1e-6:
            lw = W - XK + 0.25 * KEN
            bf.append((lw, lw + 0.5 * KEN, floor_y + 0.90, floor_y + 1.65, "window"))
            nodes += [lw, lw + 0.5 * KEN, lw + KEN]
    jodan_y = floor_y + 0.15 if jodan else floor_y
    for i in range(nf):
        la, lb = W - cols[i + 1], W - cols[i]
        if engawa:
            lx0 = la + (0.25 * KEN if lb - la < 2.5 * KEN - 1e-6 else 0.5 * KEN)
            if i == nf - 1 and toko:
                lx0 = lb - 1.5 * KEN               # clear of the tokonoma / chigaidana in the corner
            if lx0 + 1.5 * KEN > lb + 1e-6 or lx0 < la - 1e-6:
                raise ValueError("back-row room %d too narrow for the engawa door" % i)
            yy = jodan_y if (jodan and i == nf - 1) else floor_y
            bf.append((lx0, lx0 + KEN, yy, yy + 2.0, "door"))
            nodes += [lx0, lx0 + KEN, lx0 + 1.5 * KEN]
            en_doors.append((i, lx0))
        else:
            bf.append((la + 0.5 * KEN, la + KEN, floor_y + 0.45, floor_y + 2.0, "window"))
            nodes += [la + 0.5 * KEN, la + KEN]
    zones = [(0.0, W - XD, floor_y), (W - XD, W, DOMA)] if kitchen else [(0.0, W, floor_y)]
    if jodan:
        zones = [(0.0, W - cols[nf - 1], jodan_y)] + [(max(a, W - cols[nf - 1]), b, y) for (a, b, y) in zones
                                                      if b > W - cols[nf - 1] + 1e-6]
    S.wall_line("back", zones, YT, bf, finish=fin, koshiita=kosh,
                nodes_extra=tuple(sorted(set(round(n, 4) for n in nodes))))
    if kitchen:
        S.door(openings.part_itado("_single"), "back", W - XD, DOMA, "Back door (doma)", "back")
        if XK - XD >= 1.25 * KEN - 1e-6:
            S.window(openings.part_window_slide("_board"), "back", W - XK + 0.25 * KEN, floor_y,
                     "Daidokoro window (back)")
    for (i, lx0) in en_doors:
        cell = names["b%d" % i]
        yy = jodan_y if (jodan and i == nf - 1) else floor_y
        S.door(openings.part_shoji_ext("_twin"), "back", lx0, yy, "%s -> engawa (shoji)" % cell, "en%d" % i)
    if not engawa:
        for i in range(nf):
            S.window(openings.part_window_slide("_shoji"), "back", W - cols[i + 1] + 0.5 * KEN, floor_y,
                     "Window (back, koshi + shoji)")
    # ------------------------------------------------ left gable (lx = z + D)
    lf, nodes = [], [rd]
    if kitchen:
        lf.append((D - 1.0 * KEN, D - 0.5 * KEN, DOMA + 0.95, DOMA + 1.70, "window"))
        nodes += [D - 1.0 * KEN, D - 0.5 * KEN]
        S.wall_line("left", [(0.0, D, DOMA)], YG, lf, finish=fin, koshiita=kosh, nodes_extra=tuple(nodes))
        S.window(openings.part_window_slide("_board"), "left", D - 1.0 * KEN, DOMA + 0.05, "Doma window (end)")
    else:
        if side_door == "left":
            if fd < 1.75 * KEN - 1e-6:
                raise ValueError("front row too shallow for the corridor door")
            lf.append((rd + 0.25 * KEN, rd + 1.25 * KEN, floor_y, floor_y + 2.0, "door"))
            nodes += [rd + 0.25 * KEN, rd + 1.25 * KEN, rd + 1.75 * KEN]
        lf.append((0.5 * KEN, 1.0 * KEN, floor_y + 0.45, floor_y + 2.0, "window"))
        nodes += [0.5 * KEN, 1.0 * KEN]
        S.wall_line("left", [(0.0, D, floor_y)], YG, lf, finish=fin, koshiita=kosh, nodes_extra=tuple(nodes))
        if side_door == "left":
            S.door(openings.part_shoji_ext("_single"), "left", rd + 0.25 * KEN, floor_y, "Corridor door (left)",
                   "corridor")
        S.window(openings.part_window_slide("_shoji"), "left", 0.5 * KEN, floor_y, "Window (left end)")
    # ------------------------------------------------ right gable (lx = -z)
    rf, nodes = [], [fd]
    if porch or side_door == "right":
        rf.append((0.5 * KEN, 1.5 * KEN, floor_y, floor_y + 2.0, "door"))
        nodes += [0.5 * KEN, 1.5 * KEN, 2.0 * KEN]
    else:
        rf.append((0.5 * KEN, 1.0 * KEN, floor_y + 0.45, floor_y + 2.0, "window"))
        nodes += [0.5 * KEN, 1.0 * KEN]
    if not toko:
        rf.append((fd + 0.5 * KEN, fd + 1.0 * KEN, floor_y + 0.45, floor_y + 2.0, "window"))
        nodes += [fd + 0.5 * KEN, fd + 1.0 * KEN]
    S.wall_line("right", [(0.0, D, floor_y)], YG, rf, finish=fin, koshiita=kosh, nodes_extra=tuple(nodes))
    if side_door == "right" and not porch:
        S.door(openings.part_shoji_ext("_single"), "right", 0.5 * KEN, floor_y, "Corridor door (right)", "corridor")
    elif not porch:
        S.window(openings.part_window_slide("_shoji"), "right", 0.5 * KEN, floor_y, "Window (right end)")
    if not toko:
        S.window(openings.part_window_slide("_shoji"), "right", fd + 0.5 * KEN, floor_y, "Window (right end, back)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, gable)
    # ------------------------------------------------ partitions
    B.interior = True
    if XK > 0:
        FX = (90.0, (XK, 0.0, -D))
        px = []
        if fd >= 2.0 * KEN - 1e-6:
            px.append(("k_f", rd + 0.5 * KEN, names["f0"]))
        if rd >= 2.0 * KEN - 1e-6:
            px.append(("k_b", 0.5 * KEN, names["b0"]))
        S.wall_line((FX, D, "part_xk"), [(0.0, D, floor_y)], YG,
                    [(lx, lx + KEN, floor_y, floor_y + 2.0, "door") for (_, lx, _) in px],
                    finish="nakanuri", grime=False, interior="both",
                    nodes_extra=tuple(v for (_, lx, _) in px for v in (lx, lx + KEN, lx + 1.5 * KEN)) + (rd,))
        for (key, lx, nm) in px:
            S.door(openings.part_shoji_ext("_single"), FX, lx, floor_y, "Daidokoro -> %s" % nm, key)
        B.interior = False
        interior_gable(S, XK, D, t, E, "gable_xk")
        B.interior = True
    ramps = []
    for i in range(1, nf):
        x = cols[i]
        FC = (90.0, (x, 0.0, -D))
        hb = _snap(rd / 2 - 0.5 * KEN)
        if hb < 0.5 * KEN - 0.06 or hb + 1.5 * KEN > rd + 0.06:
            raise ValueError("back row too shallow for a hikiwake on x %.2f" % x)
        sf = rd + 0.5 * KEN
        up = jodan and i == nf - 1
        yb = jodan_y if up else floor_y
        S.wall_line((FC, D, "part_c%d" % i), [(0.0, rd, yb), (rd, D, floor_y)], CEIL,
                    [(hb, hb + KEN, yb, yb + 2.0, "door"), (sf, sf + KEN, floor_y, floor_y + 2.0, "door")],
                    finish="nakanuri", grime=False, interior="both",
                    nodes_extra=(hb - 0.5 * KEN, hb, hb + KEN, hb + 1.5 * KEN, sf, sf + KEN, sf + 1.5 * KEN, rd))
        S.door(part_fusuma("_hikiwake"), FC, hb, yb,
               "%s <-> %s (fusuma)" % (names["b%d" % (i - 1)], names["b%d" % i]), "c%db" % i)
        S.door(part_fusuma("_single"), FC, sf, floor_y,
               "%s <-> %s" % (names["f%d" % (i - 1)], names["f%d" % i]), "c%df" % i)
        if up:
            ramps.append((FC, hb + 0.5 * KEN, names["b%d" % (i - 1)]))
    FR = (0.0, (XK, 0.0, ZS))
    rfe, nodes_r, rdoors = [], [], []
    for i in range(nf):
        a, w = cols[i] - XK, cols[i + 1] - cols[i]
        up = jodan and i == nf - 1
        if i == nf - 1 and w >= 3.0 * KEN - 1e-6:
            lx0 = _snap(a + w / 2 - 0.5 * KEN)
            rdoors.append(("r%d" % i, lx0, "_hikiwake", up))
            nodes_r += [lx0 - 0.5 * KEN, lx0, lx0 + KEN, lx0 + 1.5 * KEN]
        elif i == nf - 1 and toko:
            continue                                   # a 2-ken formal room: no door to the front room (the
            #                                            tokonoma takes the far corner; reached through the tsugi)
        else:
            lx0 = a + 0.5 * KEN if w >= 2.0 * KEN - 1e-6 else a
            rdoors.append(("r%d" % i, lx0, "_single", up))
            nodes_r += [lx0, lx0 + KEN, lx0 + 1.5 * KEN]
        yy = jodan_y if up else floor_y
        rfe.append((lx0, lx0 + KEN, yy, yy + 2.0, "door"))
    zr = [(0.0, cols[nf - 1] - XK, floor_y), (cols[nf - 1] - XK, W - XK, jodan_y)] if jodan else         [(0.0, W - XK, floor_y)]
    S.wall_line((FR, W - XK, "part_zs"), zr, CEIL, rfe, finish="nakanuri", grime=False,
                interior="both", nodes_extra=tuple(nodes_r) + tuple(c - XK for c in cols))
    for (key, lx0, v, up) in rdoors:
        i = int(key[1:])
        S.door(part_fusuma(v), FR, lx0, jodan_y if up else floor_y,
               "%s <-> %s" % (names["f%d" % i], names["b%d" % i]), key)
        if up:
            ramps.append((FR, lx0 + 0.5 * KEN, names["f%d" % i]))
    B.interior = False
    # ------------------------------------------------ floors
    B.interior = True
    if kitchen:
        B.merge(FL.doma("doma", 0.0, XD, -D, 0.0, road=(A_, XD - 0.07, -D + A_, -A_), y=DOMA,
                        mats=FL.MATS_DOMA_EARTH))
        holes = []
        if irori and XK - XD >= 1.5 * KEN - 1e-6:
            pit = _irori(S, "daidokoro", _snap((XD + XK) / 2), -D / 2, False, floor_y, K["levels"])
            holes = [pit + ("pit",)]
        B.merge(FL.boards("daidokoro", XD + 0.06, XK - A_, -D + A_, -A_, floor_y, holes=holes,
                          hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    for i in range(nf):
        x0, x1 = cols[i] + A_, cols[i + 1] - A_
        B.merge(FL.tatami(names["f%d" % i], x0, x1, ZS + A_, -A_, top=floor_y, base=DOMA, mats=FL.MATS_TATAMI_B1))
        up = jodan and i == nf - 1
        B.merge(FL.tatami(names["b%d" % i], x0, x1, -D + A_, ZS - A_, top=jodan_y if up else floor_y, base=DOMA,
                          mats=FL.MATS_TATAMI_B1))
    B.interior = False
    for (fr, cx, low) in ramps:
        hidden_ramp(S, fr, cx, 1.10, 0.15, jodan_y, room=low)
    if kitchen:
        S.kamachi((90.0, (XD, 0.0, -D)), D, floor_y, [D / 2], "doma")
        for k_ in range(kamado_n):
            _kamado(S, "doma", 0.50, -D + 0.9 * KEN + k_ * 0.85 * KEN, 90.0)
    ceiling(S, "ceiling", (XK + A_, W - A_, -D + A_, -A_), CEIL)
    hide_attic(S, XK + 0.05, W - 0.05, -D + 0.05, -0.05, CEIL + 0.03)
    if toko:
        toko_w = KEN if rd < 2.4 * KEN else 1.5 * KEN
        a = fd + 0.06
        b = fd + toko_w
        if chigai and rd - toko_w >= KEN - 1e-6:
            c = min(b + KEN, D - 0.06)
            wall_c = c < D - 0.07
        else:
            c, wall_c = b, False
        tokonoma(S, names["b%d" % (nf - 1)], S.F["right"], a, b, c, jodan_y, CEIL, wall_a=False, wall_c=wall_c,
                 chigai=chigai and c > b + 0.5)
    if porch == "porch":
        genkan_porch(S, "right", -1.0 * KEN, floor_y, porch_fam or fam, E)
    elif porch == "step":
        st = Part("genkan_step", "", "")
        found.step(st, 1.0 * KEN, "cut", drop=floor_y - 0.0, width=1.20)
        S.B.put(st, S.F["right"], 0.0, floor_y, what="found.step (cut): the plain entrance step (no shikidai)")
        S.door(openings.part_shoji_ext("_single"), "right", 0.5 * KEN, floor_y, "Entrance (genkan, no shikidai)",
               "genkan")
    if engawa:
        ep = Part("engawa", "", "")
        zo = found.engawa(ep, 0.0, W - XK, kure=True, depth=1.365, drop=floor_y)
        B.put(ep, S.F["back"], 0.0, floor_y, what="found.engawa (kure-en) along the garden wall")
        st = Part("engawa_step", "", "")
        cx = W - XK - 0.70
        found.step(st, cx, "natural", drop=floor_y, width=1.04)
        B.put(st, (180.0, (W, 0.0, -D - zo - 0.07)), 0.0, floor_y, what="found.step (natural): down from the engawa")
        if jodan:
            for (i, lx0) in en_doors:
                if i == nf - 1:
                    hidden_ramp(S, S.F["back"], lx0 + 0.5 * KEN, 1.40, 0.15, jodan_y, room="engawa")
        S.room("engawa", "veranda", "boards", floor_y, (XK + 0.15, W - 0.15, -D - zo + 0.10, -D - 0.12),
               [S.dn["en%d" % i] for (i, _) in en_doors], "the engawa along the garden: open, under the eave",
               enclosed=False)
        S.obst.append(("engawa", _r(XK + 0.15, XK + 1.40, -D - zo - 0.10, -D - zo + 0.25)))
    if plaster:
        plaster_exterior(S, W, D)
    S.place_windows()
    # ------------------------------------------------ rooms
    dn = S.dn
    if kitchen:
        S.room("doma", "doma", "earth", DOMA, (A_, XD - 0.07, -D + A_, -A_), [dn["front"], dn["back"]],
               notes.get("doma", "the kitchen doma: the kamado, water jars, the service entrance"))
        S.room("daidokoro", "daidokoro", "boards", floor_y, (XD + 0.07, XK - A_, -D + A_, -A_),
               [dn[k_] for k_ in ("k_f", "k_b") if k_ in dn],
               notes.get("daidokoro", "the board kitchen room, open to the doma and the sooted roof"))
    for i in range(nf):
        x0, x1 = cols[i] + A_, cols[i + 1] - A_
        for row, (z0, z1) in (("f", (ZS + A_, -A_)), ("b", (-D + A_, ZS - A_))):
            key = "%s%d" % (row, i)
            ds = []
            if row == "f" and i == 0 and "k_f" in dn:
                ds.append(dn["k_f"])
            if row == "b" and i == 0 and "k_b" in dn:
                ds.append(dn["k_b"])
            if i > 0:
                ds.append(dn["c%d%s" % (i, row)])
            if i < nf - 1:
                ds.append(dn["c%d%s" % (i + 1, row)])
            if "r%d" % i in dn:
                ds.append(dn["r%d" % i])
            if row == "b" and "en%d" % i in dn:
                ds.append(dn["en%d" % i])
            if row == "f" and i == nf - 1 and "genkan" in dn:
                ds.append(dn["genkan"])
            if row == "f" and i == 0 and "corridor" in dn and side_door == "left":
                ds.append(dn["corridor"])
            if row == "f" and i == nf - 1 and "corridor" in dn and side_door == "right":
                ds.append(dn["corridor"])
            up = jodan and row == "b" and i == nf - 1
            S.room(names[key], tags.get(key, "zashiki"), "tatami", jodan_y if up else floor_y, (x0, x1, z0, z1), ds,
                   notes.get(key, ""))
    return K


R2_DROP = ("tsuka_stone", "track", "grime", "boss", "drip_cap", "purlin_end", "saobuchi", "tsuka", "groove",
           "wall_ledger", "dark_void", "fusuma_frame", "toko_side_wall", "chigaidana", "fukurodana", "jidana")
R3_DROP = ("verge", "hafu")


def far_trim_res(H):
    """Far-LOD trim of the big residences (PLAYBOOK §12): small details under the eaves and inside (engawa stones and
    posts, door tracks, grime, gable bosses, drip caps, purlin ends, ceiling battens, the alcove shelves) leave
    Resolution 2; they are Resolution 1 dressing."""
    for s in H.solids:
        if s.tag in R2_DROP and 2 in s.vis:
            s.vis = set(s.vis) - {2}
        if getattr(s, "interior", False) and s.tag in R2_INTERIOR and 2 in s.vis:
            s.vis = set(s.vis) - {2}


R2_INTERIOR = ("infill", "infill_base", "head_rail", "kokabe", "post", "part_head", "tenjo", "koshiita", "board",
               "gable_infill", "roof_gable", "gable_post", "collar", "tie_beam", "toko_kokabe", "otoshigake", "tokobashira",
               "toko_board", "tokogamachi", "gable_geo")


def cut_stones(H):
    """Town residences stand on squared stones (PLAYBOOK §6.4 rule 3, separate stones): every field soseki / engawa
    stone becomes a cut block (0.30 square, 2 cm proud of grade; ~6 faces instead of ~30)."""
    out = []
    for s_ in H.solids:
        if s_.tag in ("soseki", "tsuka_stone") and s_.vis and 1 in s_.vis and not s_.geo:
            b = s_.bbox()
            cx, cz = (b[0] + b[1]) / 2, (b[4] + b[5]) / 2
            hw = min(0.16, (b[1] - b[0]) / 2)
            top = b[3] if s_.tag == "tsuka_stone" else 0.02
            nb = box(cx - hw, cx + hw, top - 0.20, top, cz - hw, cz + hw, "stone_cut", vis=tuple(sorted(s_.vis)),
                     tag=s_.tag).finalize()
            nb.interior = getattr(s_, "interior", False)
            out.append(nb)
            continue
        out.append(s_)
    H.solids = out


def _finish_res(S, kind, params, K, W, D, E, extra=None):
    lv = {"doma": DOMA, "floor": FLOOR, "eave": E, "ceiling": FLOOR + CEIL_H}
    lv.update(extra or {})
    cut_stones(S.H)
    trim_lods(S.H)
    far_trim_res(S.H)
    return S.finish({"params": dict(params, kind=kind), "levels": lv, "koyagumi": K["counts"]},
                    exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)


def samurai(name=None, size="s", wear="_w1"):
    """DW19 samurai mansion (mid-rank / hatamoto / karo): genkan porch with the shikidai on the right gable, the
    formal suite (genkan room -> tsugi -> zashiki with tokonoma + chigaidana), ceilings, the engawa on the garden side,
    the kitchen doma + daidokoro at the left end. Sizes s (7 x 4.5 ken), m (8 x 5), l (9 x 5: a 3-ken formal room)."""
    if size == "s":
        W, D, XD, XK, ZS, fam = 7 * KEN, 4.5 * KEN, 1.5 * KEN, 3 * KEN, -2.5 * KEN, "sangawara"
        cols = [3 * KEN, 5 * KEN, 7 * KEN]
        names = {"f0": "chanoma", "f1": "genkan_ma", "b0": "tsugi", "b1": "zashiki"}
    elif size == "m":
        W, D, XD, XK, ZS, fam = 8 * KEN, 5 * KEN, 1.5 * KEN, 3 * KEN, -2.5 * KEN, "sangawara"
        cols = [3 * KEN, 5 * KEN, 8 * KEN]
        names = {"f0": "chanoma", "f1": "genkan_ma", "b0": "tsugi", "b1": "zashiki"}
    else:
        # karo: hongawara would be the status roof (PLAYBOOK §2.1 T3), but the straight-roof hongawara has no far-LOD field
        # yet (C15 / C16 fail): sangawara for now (noted in D3_NOTES)
        # (10 ken with three columns ran past binarize's vertex limit: the karo's extra rooms belong in a wing, linked
        # by a covered corridor at the compound step)
        W, D, XD, XK, ZS, fam = 9 * KEN, 5 * KEN, 2 * KEN, 4 * KEN, -2.5 * KEN, "sangawara"
        cols = [4 * KEN, 6 * KEN, 9 * KEN]
        names = {"f0": "chanoma", "f1": "genkan_ma", "b0": "tsugi", "b1": "zashiki"}
    tags = {k: "zashiki" for k in names}
    tags.update({"f0": "living"})
    notes = {"f0": "chanoma (family room)", "f1": "genkan room (shikidai-no-ma): the crested screen faces the door",
             "b0": "tsugi-no-ma (ante-room before the zashiki)", "b1": "zashiki: tokonoma + chigaidana, ceiling"}
    E = 3.45
    S = Shell(name or "jp_samurai", W, D, [3], "samurai mansion (DW19), %s" % size, wear)
    S.ceilings = []
    K = _residence(S, W, D, XD, XK, cols, ZS, fam, E, names, tags, notes, porch="porch", toko=True, engawa=True,
                   porch_fam="sangawara")
    return _finish_res(S, "samurai", {"size": size}, K, W, D, E)


def doshin(name=None, roof="itabuki", wear="_w1"):
    """DW15 small samurai house (doshin / kachi): W 6.5 x D 4.5 ken; the plain entrance (a door with a cut stone step, no
    porch, no shikidai) on the right gable; four tatami rooms with ceilings; the kitchen doma + a board room; no
    engawa (windows), no tokonoma (kept plain)."""
    W, D, XD, XK, ZS = 6.5 * KEN, 4.5 * KEN, 1.5 * KEN, 2.5 * KEN, -2.0 * KEN
    cols = [2.5 * KEN, 4.5 * KEN, 6.5 * KEN]
    names = {"f0": "chanoma", "f1": "genkan_ma", "b0": "nando", "b1": "zashiki"}
    tags = {"f0": "living", "f1": "zashiki", "b0": "sleeping", "b1": "zashiki"}
    notes = {"f0": "chanoma (family room)", "f1": "the entrance room (genkan, no shikidai)", "b0": "sleeping room",
             "b1": "zashiki (the best room, plain: no tokonoma)"}
    E = 3.45
    S = Shell(name or "jp_doshin", W, D, [2, 3], "small samurai house (DW15)", wear)
    S.ceilings = []
    K = _residence(S, W, D, XD, XK, cols, ZS, roof, E, names, tags, notes, porch="step", toko=False, engawa=False,
                   irori=False, gable="_board" if roof == "itabuki" else "_tile", kamado_n=1)
    return _finish_res(S, "doshin", {"roof": roof}, K, W, D, E)


def merchant(name=None, wear="_w1"):
    """DW18 great merchant residence (odana no oku): W 7.5 x D 5 ken, sangawara; the kitchen doma (2 ken, a three-mouth
    kamado bank) + a board daidokoro (1.5 ken); ceilinged tatami rooms (chanoma, butsuma, tsugi, oku-zashiki) with the
    engawa on the garden. Commoner: no genkan, no tokonoma, no nageshi (T48, G1 A2); plain outside (earth walls)."""
    W, D, XD, XK, ZS = 7.5 * KEN, 5 * KEN, 2 * KEN, 3.5 * KEN, -2.5 * KEN
    cols = [3.5 * KEN, 5.5 * KEN, 7.5 * KEN]
    names = {"f0": "chanoma", "f1": "butsuma", "b0": "tsugi", "b1": "oku_zashiki"}
    tags = {"f0": "living", "f1": "zashiki", "b0": "zashiki", "b1": "zashiki"}
    notes = {"f0": "chanoma (family room, the long hibachi)", "f1": "butsuma (the family altar room)",
             "b0": "tsugi-no-ma", "b1": "oku-zashiki on the garden (plain: no tokonoma, G1 A2)"}
    E = 3.45
    S = Shell(name or "jp_merchant", W, D, [3], "great merchant residence (DW18)", wear)
    S.ceilings = []
    K = _residence(S, W, D, XD, XK, cols, ZS, "sangawara", E, names, tags, notes, porch=None, toko=False, engawa=True,
                   plaster=False, kamado_n=3)
    return _finish_res(S, "merchant", {}, K, W, D, E)


def honjin_omote(name=None, wear="_w1"):
    """Honjin, the formal block (omote): W 9 x D 5 ken, no kitchen; the genkan porch + shikidai on the right gable, the
    genkan room, two attendants' rooms, the san-no-ma -> tsugi-no-ma -> JODAN-NO-MA (raised 0.15, tokonoma +
    chigaidana), ceilings, the engawa on the garden; a corridor door on the left gable to the oku (K3's corridor)."""
    W, D, ZS = 9 * KEN, 5 * KEN, -2.5 * KEN
    cols = [0.0, 3 * KEN, 6 * KEN, 9 * KEN]
    names = {"f0": "attendants_2", "f1": "attendants_1", "f2": "genkan_ma", "b0": "san_no_ma", "b1": "tsugi_no_ma",
             "b2": "jodan_no_ma"}
    tags = {k: "zashiki" for k in names}
    notes = {"f0": "attendants' room", "f1": "attendants' room", "f2": "genkan room (shikidai-no-ma)",
             "b0": "san-no-ma", "b1": "tsugi-no-ma", "b2": "jodan-no-ma: the lord's raised room (+0.15), tokonoma + "
             "chigaidana (T19)"}
    E = 3.45
    S = Shell(name or "jp_honjin_omote", W, D, [3], "honjin, formal block", wear)
    S.ceilings = []
    K = _residence(S, W, D, 0.0, 0.0, cols, ZS, "sangawara", E, names, tags, notes, porch="porch", toko=True,
                   jodan=True, engawa=True, side_door="left")
    return _finish_res(S, "honjin_omote", {}, K, W, D, E, {"jodan": FLOOR + 0.15})


def honjin_oku(name=None, wear="_w1"):
    """Honjin, the family / kitchen block (oku): W 8 x D 5 ken; the big kitchen doma (3 ken, a kamado bank), the board
    daidokoro with the irori (2 ken), two family rooms (ceilings); the family's own entrance = the doma door; a
    corridor door on the right gable to the omote."""
    W, D, XD, XK, ZS = 8 * KEN, 5 * KEN, 3 * KEN, 5 * KEN, -2.5 * KEN
    cols = [5 * KEN, 8 * KEN]
    names = {"f0": "family_room", "b0": "family_oku"}
    tags = {"f0": "living", "b0": "sleeping"}
    notes = {"f0": "the honjin family's living room", "b0": "the family's back room",
             "doma": "the big kitchen doma: the kamado bank cooks for the lord's train"}
    E = 3.45
    S = Shell(name or "jp_honjin_oku", W, D, [2, 3], "honjin, family / kitchen block", wear)
    S.ceilings = []
    K = _residence(S, W, D, XD, XK, cols, ZS, "sangawara", E, names, tags, notes, porch=None, toko=False, engawa=False,
                   side_door="right", kamado_n=3, plaster=False)
    return _finish_res(S, "honjin_oku", {}, K, W, D, E)


def wakihonjin(name=None, wear="_w1"):
    """Waki-honjin (deputy lords' inn): one block, W 9 x D 4.5 ken; the kitchen doma + daidokoro, the genkan porch +
    shikidai, a smaller jodan-no-ma (raised, tokonoma + chigaidana) behind the tsugi, family and attendants' rooms;
    NO gate (KEEP_TRADES 6)."""
    W, D, XD, XK, ZS = 9 * KEN, 4.5 * KEN, 1.5 * KEN, 3 * KEN, -2.5 * KEN
    cols = [3 * KEN, 5 * KEN, 7 * KEN, 9 * KEN]
    names = {"f0": "chanoma", "f1": "attendants", "f2": "genkan_ma", "b0": "family_oku", "b1": "tsugi_no_ma",
             "b2": "jodan_no_ma"}
    tags = {k: "zashiki" for k in names}
    tags.update({"f0": "living", "b0": "sleeping"})
    notes = {"f0": "chanoma", "f1": "attendants' room", "f2": "genkan room (shikidai-no-ma)", "b0": "the family's room",
             "b1": "tsugi-no-ma", "b2": "jodan-no-ma (smaller, raised 0.15): tokonoma + chigaidana"}
    E = 3.45
    S = Shell(name or "jp_wakihonjin", W, D, [3], "waki-honjin", wear)
    S.ceilings = []
    K = _residence(S, W, D, XD, XK, cols, ZS, "sangawara", E, names, tags, notes, porch="porch", toko=True,
                   jodan=True, engawa=True)
    return _finish_res(S, "wakihonjin", {}, K, W, D, E, {"jodan": FLOOR + 0.15})


# ================================================================================================ DW14 ashigaru row
def kumi(name=None, units=3, roof="itabuki", wear="_w2"):
    """DW14 foot-soldier row (ashigaru nagaya / kumi-yashiki), ONE storey (G1 A1-3): `units` units of 3 x 2.5 ken under
    one kirizuma roof; each unit: a doma 1 x 1.5 ken by its front door (kamado), a 6-mat front room and a 6-mat back
    room (tatami; the period's 6 + 4.5 mats need half mats the kit's shugi layout lacks); full-height party walls with board gables up to the roof between units."""
    UW, D = 3 * KEN, 2.5 * KEN
    W = units * UW
    E = 3.10
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[roof]
    FL_ = FLOOR_R
    ZS = -1.5 * KEN
    S = Shell(name or "jp_kumi", W, D, [2], "foot-soldier row (DW14), %d units" % units, wear)
    S.ceilings = []
    B = S.B
    party = [round(k * UW, 4) for k in range(1, units)]
    xs = []
    k = 1
    while k * KEN < W - 0.30:
        if all(abs(k * KEN - p) > 0.30 for p in party):
            xs.append(round(k * KEN, 4))
        k += 1
    sls, info_r, K = S.roof(W, D, "kirizuma", roof, E, soot=True, members="sawn", xs=xs)
    S.keta_ring(W, D, E, hip=False)
    fin, kosh = "nakanuri", 0.90
    ff, bf, nf_, nb_ = [], [], [], []
    zf = []
    for u in range(units):
        u0 = u * UW
        ff += [(u0, u0 + KEN, DOMA, DOMA + 2.0, "door"),
               (u0 + 1.75 * KEN, u0 + 2.25 * KEN, FL_ + 0.90, FL_ + 1.65, "window")]
        nf_ += [u0, u0 + KEN, u0 + 1.5 * KEN, u0 + 1.75 * KEN, u0 + 2.25 * KEN]
        zf += [(u0, u0 + KEN, DOMA), (u0 + KEN, u0 + UW, FL_)]
        lb = W - u0 - 2.0 * KEN
        bf.append((lb, lb + 0.5 * KEN, FL_ + 0.90, FL_ + 1.65, "window"))
        nb_ += [lb, lb + 0.5 * KEN]
    S.wall_line("front", zf, YT, ff, finish=fin, koshiita=kosh, nodes_extra=tuple(nf_))
    S.wall_line("back", [(0.0, W, FL_)], YT, bf, finish=fin, koshiita=kosh, nodes_extra=tuple(nb_))
    S.wall_line("left", [(0.0, D, FL_)], YG, (), finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN,))
    S.wall_line("right", [(0.0, D, FL_)], YG, (), finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN,))
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board" if roof == "itabuki" else "_tile")
    for u in range(units):
        u0 = u * UW
        S.door(openings.part_itado("_single"), "front", u0, DOMA, "Unit %d door" % (u + 1), "u%d_door" % u)
        S.window(openings.part_window_slide("_board"), "front", u0 + 1.75 * KEN, FL_, "Unit %d window (front)" % (u + 1))
        S.window(openings.part_window_slide("_board"), "back", W - u0 - 2.0 * KEN, FL_,
                 "Unit %d window (back)" % (u + 1))
    PT = FL_ + walls.HEAD_T + 2.0 + 0.45
    for p in party:
        B.interior = True
        S.wall_line(((90.0, (p, 0.0, -D)), D, "party_%d" % int(p * 100)), [(0.0, D, FL_)], YG, (), finish="nakanuri",
                    grime=False, interior="both", nodes_extra=(1.5 * KEN,))
        B.interior = False
        interior_gable(S, p, D, t, E, "party_gable_%d" % int(p * 100))
    for u in range(units):
        u0 = u * UW
        B.interior = True
        FZ = (0.0, (u0 + KEN, 0.0, ZS))
        S.wall_line((FZ, UW - KEN, "u%d_part" % u), [(0.0, UW - KEN, FL_)], PT,
                    [(0.0, KEN, FL_, FL_ + 2.0, "door")], finish="nakanuri", grime=False, interior="both")
        S.door(openings.part_shoji_ext("_single"), FZ, 0.0, FL_, "Unit %d front room <-> back room" % (u + 1),
               "u%d_in" % u)
        B.interior = False
        S.head_beam(FZ, UW - KEN, PT, "u%d_part_head" % u)
        B.interior = True
        B.merge(FL.doma("u%d_doma" % u, u0, u0 + KEN, ZS, 0.0, road=(u0 + A_, u0 + KEN - 0.07, ZS + 0.07, -A_), y=DOMA,
                        mats=FL.MATS_DOMA_EARTH))
        B.merge(FL.tatami("u%d_front" % u, u0 + KEN + 0.06, u0 + UW - A_, ZS + A_, -A_, top=FL_, base=DOMA,
                          mats=FL.MATS_TATAMI_B1))
        B.merge(FL.tatami("u%d_back" % u, u0 + A_, u0 + UW - A_, -D + A_, ZS - 0.06, top=FL_, base=DOMA,
                          mats=FL.MATS_TATAMI_B1))
        B.interior = False
        S.kamachi((90.0, (u0 + KEN, 0.0, ZS)), -ZS, FL_, [0.75 * KEN], "u%d_doma" % u)
        S.kamachi((0.0, (u0, 0.0, ZS)), KEN - 0.06, FL_, [], "u%d_doma" % u)
        # the stove against the side wall, back from the door (D5: nothing in the doorway zone)
        _kamado(S, "u%d_doma" % u, u0 + 0.40, ZS + 0.55, 90.0, size=(0.60, 0.60))
    S.place_windows()
    for u in range(units):
        u0 = u * UW
        S.room("u%d_doma" % u, "doma", "earth", DOMA, (u0 + A_, u0 + KEN - 0.07, ZS + 0.07, -A_),
               [S.dn["u%d_door" % u]], "unit %d: the doma by the door, the kamado" % (u + 1))
        S.room("u%d_front" % u, "living", "tatami", FL_, (u0 + KEN + 0.07, u0 + UW - A_, ZS + A_, -A_),
               [S.dn["u%d_in" % u]], "unit %d: the 6-mat front room" % (u + 1))
        S.room("u%d_back" % u, "sleeping", "tatami", FL_, (u0 + A_, u0 + UW - A_, -D + A_, ZS - 0.07),
               [S.dn["u%d_in" % u]], "unit %d: the 6-mat back room" % (u + 1))
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "kumi", "units": units, "roof": roof},
                        "levels": {"doma": DOMA, "floor": FL_, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


# ================================================================================================ DW16 Kanto headman
def headman_east(name=None, ridge="umanori", wear="_w1"):
    """DW16 east (Kanto) headman house (nanushi): W 10 x D 5 ken under ONE hipped thatch with geya aisles (the C2 Kanto
    frame, G1 A1-4); doma x 7..10 ken (the stove bank, the ooto), hiroma x 5..7 (irori), dei (tatami) / nando x 3..5,
    and the FORMAL end x 0..3: a recessed genkan doma (its own front door) with the SHIKIDAI up to the genkan room, the
    15-mat zashiki behind it ("by permission", BL; no tokonoma: commoner, G1 A2). No porch: a gabled porch would need a
    roof union the kit lacks; the genkan sits under the thatch eave."""
    W, D, g = 10 * KEN, 5 * KEN, KEN
    E, FL_ = 3.30, FLOOR
    YT = E - KETA_H
    XG, XF, XR, XD = 1 * KEN, 3 * KEN, 5 * KEN, 7 * KEN      # genkan doma | formal | dei+nando | hiroma | doma
    ZS = -2.5 * KEN
    S = Shell(name or "jp_headman_east", W, D, [2], "Kanto headman house (DW16)", wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "yosemune", "thatch", E, ov=0.90, geya=(g, g), ridge=ridge, joya_floor=0.0,
                           stone_fn=lambda x, z: x > XD + 0.1 or x < XG - 0.1, slim_x=(XF, XR))
    S.keta_ring(W, D, E, hip=True)
    fin, kosh = "nakanuri", 0.90
    # front: genkan door lx 0..1K (parks 1K..1.5K), genkan room window 2K..2.5K, dei window 3.5K..4K, hiroma window
    # 5.5K..6K, doma window 7K..7.5K, ooto 8K..9K (parks 9K..10K)
    ff = [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (2.0 * KEN, 2.5 * KEN, FL_ + 0.45, FL_ + 2.0, "window"),
          (3.5 * KEN, 4.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"), (5.5 * KEN, 6.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"),
          (7.0 * KEN, 7.5 * KEN, DOMA + 0.90, DOMA + 1.65, "window"), (8.0 * KEN, 9.0 * KEN, DOMA, DOMA + 2.0, "door")]
    S.wall_line("front", [(0.0, XG, DOMA), (XG, XD, FL_), (XD, W, DOMA)], YT, ff, finish=fin, koshiita=kosh,
                nodes_extra=(1.5 * KEN, 2.0 * KEN, 2.5 * KEN, 3.5 * KEN, 4.0 * KEN, 5.5 * KEN, 6.0 * KEN, 7.5 * KEN))
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Genkan door (formal entrance)", "genkan")
    S.window(openings.part_window_slide("_shoji"), "front", 2.0 * KEN, FL_, "Genkan room window (front)")
    S.window(openings.part_window_slide("_board"), "front", 3.5 * KEN, FL_, "Dei window (front)")
    S.window(openings.part_window_slide("_board"), "front", 5.5 * KEN, FL_, "Hiroma window (front)")
    S.window(openings.part_window_slide("_board"), "front", 7.0 * KEN, DOMA, "Doma window (front)")
    S.door(big_leaf("_battened"), "front", 8.0 * KEN, DOMA, "Front door (ooto, doma)", "front")
    # back (lx = W - x): doma back door x 8.5K..7.5K (lx 1.5K..2.5K, parks to 3K), hiroma window lx 4K..4.5K, nando
    # push-up lx 5.5K..6K, zashiki windows lx 7.5K..8K and 8.5K..9K
    bf = [(1.5 * KEN, 2.5 * KEN, DOMA, DOMA + 2.0, "door"), (4.0 * KEN, 4.5 * KEN, FL_ + 0.90, FL_ + 1.65, "window"),
          (5.5 * KEN, 6.0 * KEN, FL_ + 0.90, FL_ + 1.60, "window"), (7.5 * KEN, 8.0 * KEN, FL_ + 0.45, FL_ + 2.0, "window"),
          (8.5 * KEN, 9.0 * KEN, FL_ + 0.45, FL_ + 2.0, "window")]
    S.wall_line("back", [(0.0, W - XD, DOMA), (W - XD, W, FL_)], YT, bf, finish=fin, koshiita=kosh,
                nodes_extra=(1.5 * KEN, 2.5 * KEN, 3.0 * KEN, 4.5 * KEN, 5.5 * KEN, 6.0 * KEN, 7.5 * KEN, 8.0 * KEN,
                             8.5 * KEN, 9.0 * KEN))
    S.door(openings.part_itado("_single"), "back", 1.5 * KEN, DOMA, "Back door (doma)", "back")
    S.window(openings.part_window_slide("_board"), "back", 4.0 * KEN, FL_, "Hiroma window (back)")
    S.window(openings.part_tsukiage("_board"), "back", 5.5 * KEN, FL_, "Nando window (back, push-up shutter)")
    S.window(openings.part_window_slide("_shoji"), "back", 7.5 * KEN, FL_, "Zashiki window (back)")
    S.window(openings.part_window_slide("_shoji"), "back", 8.5 * KEN, FL_, "Zashiki window (back, 2)")
    # left end (formal end, lx = z + D): zashiki window lx 0.5K..1K; genkan doma window lx 3.5K..4K
    S.wall_line("left", [(0.0, D + ZS, FL_), (D + ZS, D, DOMA)], YT,
                [(0.5 * KEN, 1.0 * KEN, FL_ + 0.45, FL_ + 2.0, "window"),
                 (3.5 * KEN, 4.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")], finish=fin, koshiita=kosh,
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 1.5 * KEN, 3.5 * KEN, 4.0 * KEN, 4.5 * KEN))
    S.window(openings.part_window_slide("_shoji"), "left", 0.5 * KEN, FL_, "Zashiki window (end)")
    S.window(openings.part_window_slide("_board"), "left", 3.5 * KEN, DOMA, "Genkan doma window (end)")
    # right end (doma, lx = -z): window lx 0.5K..1K
    S.wall_line("right", [(0.0, D, DOMA)], YT, [(0.5 * KEN, 1.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                finish=fin, koshiita=kosh, nodes_extra=(1.5 * KEN,))
    S.window(openings.part_window_slide("_board"), "right", 0.5 * KEN, DOMA, "Doma window (end)")
    # partitions (open above to the koyagumi, head beams, FB2 C21)
    PT = FL_ + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F_Z = (0.0, (0.0, 0.0, ZS))                      # z = ZS, lx = x: genkan doma | zashiki (0..1K), genkan_ma |
    S.wall_line((F_Z, XR, "part_zs"), [(0.0, XG, FL_), (XG, XR, FL_)], PT,          # zashiki (1K..3K), dei | nando
                [(1.5 * KEN, 2.5 * KEN, FL_, FL_ + 2.0, "door")], finish="nakanuri", grime=False, interior="both",
                nodes_extra=(XG, 1.5 * KEN, 2.5 * KEN, XF))
    S.door(part_fusuma("_single"), F_Z, 1.5 * KEN, FL_, "Genkan room <-> zashiki", "zashiki")
    F_F = (90.0, (XF, 0.0, -D))                      # x = XF, lx = z + D: zashiki | nando (0..2.5K), genkan_ma | dei
    S.wall_line((F_F, D, "part_xf"), [(0.0, D, FL_)], PT,
                [(1.0 * KEN, 2.0 * KEN, FL_, FL_ + 2.0, "door"), (3.0 * KEN, 4.0 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(D + ZS,))
    S.door(part_fusuma("_single"), F_F, 1.0 * KEN, FL_, "Zashiki <-> nando", "z_nando")
    S.door(part_fusuma("_single"), F_F, 3.0 * KEN, FL_, "Genkan room <-> dei", "g_dei")
    F_R = (90.0, (XR, 0.0, -D))                      # x = XR: nando | hiroma (0..2.5K), dei | hiroma
    S.wall_line((F_R, D, "part_xr"), [(0.0, D, FL_)], PT,
                [(1.0 * KEN, 2.0 * KEN, FL_, FL_ + 2.0, "door"), (3.0 * KEN, 4.0 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(D + ZS,))
    S.door(openings.part_itado("_single"), F_R, 1.0 * KEN, FL_, "Hiroma -> nando", "nando")
    S.door(openings.part_shoji_ext("_single"), F_R, 3.0 * KEN, FL_, "Hiroma -> dei", "dei")
    B.interior = False
    S.head_beam(F_Z, XR, PT, "part_zs_head")
    S.head_beam(F_F, D, PT, "part_xf_head")
    S.head_beam(F_R, D, PT, "part_xr_head")
    # floors
    B.interior = True
    B.merge(FL.doma("doma", XD, W, -D, 0.0, road=(XD + 0.07, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.doma("genkan", 0.0, XG, ZS, 0.0, road=(A_, XG - 0.07, ZS + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_T3))
    pit = _irori(S, "hiroma", 6.0 * KEN, -D / 2, False, FL_, K["levels"])
    B.merge(FL.boards("hiroma", XR + A_, XD - 0.06, -D + A_, -A_, FL_, holes=[pit + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    B.merge(FL.tatami("dei", XF + A_, XR - A_, ZS + A_, -A_, top=FL_, base=0.0, mats=FL.MATS_TATAMI_CHA))
    B.merge(FL.boards("nando", XF + A_, XR - A_, -D + A_, ZS - A_, FL_, mats=BOARDS_ROUGH))
    B.merge(FL.boards("genkan_ma", XG + 0.06, XF - A_, ZS + A_, -A_, FL_, mats=FL.MATS_BOARDS_B1))
    B.merge(FL.tatami("zashiki", A_, XF - A_, -D + A_, ZS - A_, top=FL_, base=0.0, mats=FL.MATS_TATAMI_B1))
    B.interior = False
    S.kamachi((-90.0, (XD, 0.0, 0.0)), D, FL_, [1.5 * KEN, 3.5 * KEN], "doma")
    shikidai_edge(S, (90.0, (XG, 0.0, ZS)), -ZS, FL_, [0.75 * KEN], "genkan")
    for k_ in range(3):
        _kamado(S, "doma", W - 0.50, -1.4 * KEN - k_ * 0.85 * KEN, 270.0)
    S.place_windows()
    S.room("doma", "doma", "earth", DOMA, (XD + 0.07, W - A_, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "the big doma: the stove bank (three kamado) on the end wall, the ooto")
    S.room("genkan", "doma", "stone", DOMA, (A_, XG - 0.07, ZS + A_, -A_), [S.dn["genkan"]],
           "the formal genkan doma (its own door) with the shikidai step up to the genkan room")
    S.room("genkan_ma", "zashiki", "boards", FL_, (XG + 0.07, XF - A_, ZS + A_, -A_), [S.dn["zashiki"], S.dn["g_dei"]],
           "the genkan room (officials are received here)")
    S.room("zashiki", "zashiki", "tatami", FL_, (A_, XF - A_, -D + A_, ZS - A_), [S.dn["zashiki"], S.dn["z_nando"]],
           "the formal zashiki (15 mats; no tokonoma: commoner, G1 A2)")
    S.room("dei", "living", "tatami", FL_, (XF + A_, XR - A_, ZS + A_, -A_), [S.dn["g_dei"], S.dn["dei"]], "dei")
    S.room("nando", "sleeping", "boards", FL_, (XF + A_, XR - A_, -D + A_, ZS - A_), [S.dn["z_nando"], S.dn["nando"]],
           "nando")
    S.room("hiroma", "daidokoro", "boards", FL_, (XR + A_, XD - 0.07, -D + A_, -A_), [S.dn["nando"], S.dn["dei"]],
           "hiroma with the irori, open to the doma")
    trim_lods(S.H)
    return S.finish({"params": {"kind": "headman_east", "ridge": ridge},
                     "levels": {"doma": DOMA, "floor": FL_, "eave": E}, "koyagumi": K["counts"]},
                    exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)


# ================================================================================================ DW17 Kinai headman
def headman_kinai(name=None, wear="_w1"):
    """DW17 Kinai headman house (shoya): W 9 x D 4 ken, the Kinai thatch kirizuma with yamato-mune takahe gables and
    TILED lower roofs (pents) along both long walls (C2's Kinai frame); white plaster outside (the shoya marker); niwa x
    0..3 ken with the kamado row; six rooms on two rows: mise | tsugi | genkan room (front), daidokoro (irori) | nando |
    zashiki (back); the formal entrance on the right gable under a tiled lean-to: a door + the shikidai board step.
    No tokonoma (commoner, G1 A2)."""
    W, D = 9 * KEN, 4 * KEN
    E, FL_ = 4.30, FLOOR
    t = R.PITCH["thatch"]
    YT = E
    XN, X2, X3 = 3 * KEN, 5 * KEN, 7 * KEN
    ZS = -2 * KEN
    PENT_Y, PENT_P = 3.50, 1.20
    S = Shell(name or "jp_headman_kinai", W, D, [2], "Kinai headman house (DW17)", wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", "thatch", E, ov=0.60, gov=0.05, ridge="bamboo")
    # the thatch ridge bundle kept low between the takahe (rural.kinai, FB1 / FB2)
    from .rural import TAKAHE_RISE
    apex = E + t * D / 2 + R.STACK["thatch"] + 0.60
    rs = [s_ for s_ in S.H.solids if s_.tag in ("thatch_ridge", "ridge_bamboo") or
          (s_.tag == "binding" and s_.center[1] > E + 1.0)]
    if rs:
        y0 = min(v[1] for s_ in rs for v in s_.verts if s_.tag == "thatch_ridge")
        y1 = max(v[1] for s_ in rs for v in s_.verts)
        f = (apex + TAKAHE_RISE - 0.04 - y0) / (y1 - y0)
        keep = []
        for s_ in S.H.solids:
            if s_ in rs:
                s_.verts = [(v[0], y0 + (v[1] - y0) * f if v[1] > y0 else v[1], v[2]) for v in s_.verts]
            if s_.tag in ("thatch_ridge", "ridge_bamboo"):
                s_.verts = [(min(max(v[0], 0.0), W), v[1], v[2]) for v in s_.verts]
            if s_ in rs:
                s_.center = tuple(sum(v[k] for v in s_.verts) / len(s_.verts) for k in range(3))
                s_.fn = [s_._outward(fi) for fi in range(len(s_.faces))]
                if s_.normals is not None:
                    s_.normals = s_.fn
            if s_.tag == "binding" and s_.center[1] > E + 1.0 and not (0.16 < s_.center[0] < W - 0.16):
                continue
            keep.append(s_)
        S.H.solids = keep
    S.keta_ring(W, D, E, hip=False)
    ytop_long = E - KETA_H
    y_end = E - 0.21
    fin = "nakanuri"
    # front: niwa door lx 1K..2K (parks 2K..3K: plain), windows mise 3.5K..4K, tsugi 5.5K..6K, genkan room 7.5K..8K
    ff = [(1.0 * KEN, 2.0 * KEN, DOMA, DOMA + 2.0, "door"), (3.5 * KEN, 4.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"),
          (5.5 * KEN, 6.0 * KEN, FL_ + 0.45, FL_ + 2.0, "window"), (7.5 * KEN, 8.0 * KEN, FL_ + 0.45, FL_ + 2.0, "window")]
    S.wall_line("front", [(0.0, XN, DOMA), (XN, W, FL_)], ytop_long, ff, finish=fin, koshiita=0.90,
                nodes_extra=(3.5 * KEN, 4.0 * KEN, 5.5 * KEN, 6.0 * KEN, 7.5 * KEN, 8.0 * KEN))
    S.door(big_leaf("_battened"), "front", 1.0 * KEN, DOMA, "Front door (niwa)", "front")
    S.window(openings.part_window_slide("_board"), "front", 3.5 * KEN, FL_, "Mise window (front)")
    S.window(openings.part_window_slide("_shoji"), "front", 5.5 * KEN, FL_, "Tsugi window (front)")
    S.window(openings.part_window_slide("_shoji"), "front", 7.5 * KEN, FL_, "Genkan room window (front)")
    # back (lx = W - x): zashiki x 9K..7K lx 0..2K (window 0.5K..1K), nando lx 2K..4K (push-up 2.5K..3K), daidokoro
    # lx 4K..6K (window 4.5K..5K), niwa lx 6K..9K (back door 6.5K..7.5K, parks to 8K)
    bf = [(0.5 * KEN, 1.0 * KEN, FL_ + 0.45, FL_ + 2.0, "window"), (2.5 * KEN, 3.0 * KEN, FL_ + 0.90, FL_ + 1.60, "window"),
          (4.5 * KEN, 5.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window"), (6.5 * KEN, 7.5 * KEN, DOMA, DOMA + 2.0, "door")]
    S.wall_line("back", [(0.0, W - XN, FL_), (W - XN, W, DOMA)], ytop_long, bf, finish=fin, koshiita=0.90,
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 2.5 * KEN, 3.0 * KEN, 4.5 * KEN, 5.0 * KEN, 6.5 * KEN, 7.5 * KEN,
                             8.0 * KEN))
    S.window(openings.part_window_slide("_shoji"), "back", 0.5 * KEN, FL_, "Zashiki window (back)")
    S.window(openings.part_tsukiage("_board"), "back", 2.5 * KEN, FL_, "Nando window (back, push-up shutter)")
    S.window(openings.part_window_slide("_board"), "back", 4.5 * KEN, FL_, "Daidokoro window (back)")
    S.door(openings.part_itado("_single"), "back", 6.5 * KEN, DOMA, "Back door (niwa)", "back")
    for side in ("front", "back"):
        s = B.P("pent_" + side)
        roofparts.pent(s, 0.0, W, PENT_Y, PENT_P, 0.40, "tile")
        B.put(s, S.F[side], what="roofparts.pent tile: the Kinai lower roof (%s)" % side)
        s = B.P("pent_beam_" + side)
        s.add(box(0.0, W, PENT_Y - 0.34, PENT_Y - 0.18, POST / 2 - 0.02, POST / 2 + 0.03, "wood_weathered",
                  vis=(1, 2), tag="pent_plate"))
        B.put(s, S.F[side])
    # gables: left (niwa) window; right (rooms): the formal door into the genkan room (lx 0.5K..1.5K, parks to 2K)
    S.wall_line("left", [(0.0, D, DOMA)], y_end, [(2.5 * KEN, 3.0 * KEN, DOMA + 0.90, DOMA + 1.65, "window")],
                finish=fin, koshiita=0.90, nodes_extra=(1.5 * KEN, 3.5 * KEN))
    S.window(openings.part_window_slide("_board"), "left", 2.5 * KEN, DOMA, "Niwa window (end)")
    S.wall_line("right", [(0.0, D, FL_)], y_end, [(0.5 * KEN, 1.5 * KEN, FL_, FL_ + 2.0, "door")], finish=fin,
                koshiita=0.90, nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.0 * KEN))
    for side in ("left", "right"):
        S.gable(side, D, t, E, "_thatch", thatch=True)
    st = R.STACK["thatch"] + 0.60
    for x, sg in ((0.0, -1), (W, 1)):
        _takahe(S, x, D, E, t, sg, st, PENT_Y + 0.25)
    from ..core import face_uvs
    for s_ in S.H.solids:
        if s_.tag != "gable_infill" or not s_.fn:
            continue
        for fi, n_ in enumerate(s_.fn):
            out = (n_[0] < -0.9 and s_.center[0] < W / 2) or (n_[0] > 0.9 and s_.center[0] > W / 2)
            if out:
                s_.fm[fi] = TAKAHE_MAT
                s_.fuv[fi] = face_uvs(s_, fi, n_, TAKAHE_MAT)
    # partitions
    PT = FL_ + walls.HEAD_T + 2.0 + 0.45
    B.interior = True
    F2 = (90.0, (X2, 0.0, -D))                       # x = X2 (lx = z + D): daidokoro | nando (0..2K), mise | tsugi
    S.wall_line((F2, D, "part_x2"), [(0.0, D, FL_)], PT,
                [(0.5 * KEN, 1.5 * KEN, FL_, FL_ + 2.0, "door"), (2.5 * KEN, 3.5 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both")
    S.door(openings.part_itado("_single"), F2, 0.5 * KEN, FL_, "Daidokoro -> nando", "nando")
    S.door(openings.part_shoji_ext("_single"), F2, 2.5 * KEN, FL_, "Mise -> tsugi", "tsugi")
    F3 = (90.0, (X3, 0.0, -D))                       # x = X3: nando | zashiki (hikiwake), tsugi | genkan room
    S.wall_line((F3, D, "part_x3"), [(0.0, D, FL_)], PT,
                [(0.5 * KEN, 1.5 * KEN, FL_, FL_ + 2.0, "door"), (2.5 * KEN, 3.5 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both")
    S.door(part_fusuma("_hikiwake"), F3, 0.5 * KEN, FL_, "Nando <-> zashiki", "z_nando")
    S.door(part_fusuma("_single"), F3, 2.5 * KEN, FL_, "Tsugi <-> genkan room", "g_tsugi")
    FZ = (0.0, (XN, 0.0, ZS))                        # z = ZS (lx = x - XN): mise | daidokoro, tsugi | nando, genkan | zashiki
    S.wall_line((FZ, W - XN, "part_zs"), [(0.0, W - XN, FL_)], PT,
                [(0.5 * KEN, 1.5 * KEN, FL_, FL_ + 2.0, "door"), (4.5 * KEN, 5.5 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(2.0 * KEN, 4.0 * KEN))
    S.door(openings.part_shoji_ext("_hikiwake"), FZ, 0.5 * KEN, FL_, "Mise <-> daidokoro", "mid")
    S.door(part_fusuma("_single"), FZ, 4.5 * KEN, FL_, "Genkan room <-> zashiki", "zashiki")
    B.interior = False
    S.head_beam(F2, D, PT, "part_x2_head")
    S.head_beam(F3, D, PT, "part_x3_head")
    S.head_beam(FZ, W - XN, PT, "part_zs_head")
    # floors
    B.interior = True
    B.merge(FL.doma("niwa", 0.0, XN, -D, 0.0, road=(A_, XN - 0.07, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    pit = _irori(S, "daidokoro", 4.0 * KEN, -3.0 * KEN, True, FL_, K["levels"])
    B.merge(FL.boards("daidokoro", XN + 0.06, X2 - A_, -D + A_, ZS - A_, FL_, holes=[pit + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=BOARDS_ROUGH))
    B.merge(FL.boards("mise", XN + 0.06, X2 - A_, ZS + A_, -A_, FL_, mats=BOARDS_ROUGH))
    B.merge(FL.tatami("tsugi", X2 + A_, X3 - A_, ZS + A_, -A_, top=FL_, base=0.0, mats=FL.MATS_TATAMI_CHA))
    B.merge(FL.boards("nando", X2 + A_, X3 - A_, -D + A_, ZS - A_, FL_, mats=BOARDS_ROUGH))
    B.merge(FL.tatami("genkan_ma", X3 + A_, W - A_, ZS + A_, -A_, top=FL_, base=0.0, mats=FL.MATS_TATAMI_B1))
    B.merge(FL.tatami("zashiki", X3 + A_, W - A_, -D + A_, ZS - A_, top=FL_, base=0.0, mats=FL.MATS_TATAMI_B1))
    B.interior = False
    S.kamachi((90.0, (XN, 0.0, -D)), D, FL_, [1.0 * KEN, 3.0 * KEN], "niwa")
    for k_ in range(3):
        _kamado(S, "niwa", 0.50, -0.9 * KEN - k_ * 0.85 * KEN, 90.0)
    # the formal entrance: a tiled lean-to on the right gable over the door, the shikidai inside it
    _gable_leanto(S, "right", "sangawara", E, t)
    S.rooms[-1]["name"] = "genkan_porch"
    S.rooms[-1]["tag"] = "yard"
    S.rooms[-1]["note"] = "the formal entrance under a tiled lean-to: the shikidai board step up to the genkan room"
    for i, (n_, r_) in enumerate(S.obst):
        if n_ == "leanto":
            S.obst[i] = ("genkan_porch", r_)
    stp = Part("shikidai_r", "", "")
    found.step(stp, 1.0 * KEN, "wood", drop=FL_ - DOMA, width=1.20)
    B.put(stp, S.F["right"], 0.0, FL_, what="found.step (wood): the shikidai board step (right gable)")
    S.door(openings.part_shoji_ext("_single"), "right", 0.5 * KEN, FL_, "Genkan door (formal entrance)", "genkan")
    S.obst.append(("genkan_porch", _r(W, W + 0.80, -1.6 * KEN, -0.4 * KEN)))
    S.rooms[-1]["doors"] = [S.dn["genkan"]]
    plaster_exterior(S, W, D)
    S.place_windows()
    S.room("niwa", "doma", "earth", DOMA, (A_, XN - 0.07, -D + A_, -A_), [S.dn["front"], S.dn["back"]],
           "the niwa: the kamado row (kudo), water jars")
    S.room("mise", "living", "boards", FL_, (XN + 0.07, X2 - A_, ZS + A_, -A_), [S.dn["tsugi"], S.dn["mid"]],
           "mise (the village-business room), open to the niwa")
    S.room("daidokoro", "daidokoro", "boards", FL_, (XN + 0.07, X2 - A_, -D + A_, ZS - A_), [S.dn["nando"], S.dn["mid"]],
           "daidokoro with the irori, open to the niwa")
    S.room("tsugi", "zashiki", "tatami", FL_, (X2 + A_, X3 - A_, ZS + A_, -A_), [S.dn["tsugi"], S.dn["g_tsugi"]],
           "tsugi-no-ma")
    S.room("nando", "sleeping", "boards", FL_, (X2 + A_, X3 - A_, -D + A_, ZS - A_), [S.dn["nando"], S.dn["z_nando"]],
           "nando")
    S.room("genkan_ma", "zashiki", "tatami", FL_, (X3 + A_, W - A_, ZS + A_, -A_),
           [S.dn["genkan"], S.dn["g_tsugi"], S.dn["zashiki"]], "the genkan room (shikidai-no-ma)")
    S.room("zashiki", "zashiki", "tatami", FL_, (X3 + A_, W - A_, -D + A_, ZS - A_), [S.dn["zashiki"], S.dn["z_nando"]],
           "the formal zashiki (no tokonoma: commoner, G1 A2)")
    trim_lods(S.H)
    return S.finish({"params": {"kind": "headman_kinai"}, "levels": {"doma": DOMA, "floor": FL_, "eave": E,
                     "pent": PENT_Y}, "koyagumi": K["counts"]},
                    exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)


# ================================================================================================ DW21 tea hut
def chashitsu(name=None, roof="thatch", wear="_w1"):
    """DW21 tea hut (soan): W 3 x D 2 ken; the 4.5-mat tea room x 0..1.5 ken (3 + 1 mats and the board half-mat with the
    ro, a low ceiling, the tokonoma at the back with its toko-bashira on the open side), the mizuya (prep room, boards)
    x 1.5..3 ken with the normal door (D9); the nijiri-guchi on the tea-room front is decorative (static, closed);
    earth walls, thatch or kokera (shingle) kirizuma."""
    W, D = 3 * KEN, 2 * KEN
    fam = "thatch" if roof == "thatch" else "itabuki"
    E = 3.30 if fam == "thatch" else 2.90        # thatch: the eave slab's bbox stays over the door column (D2)
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    FL_ = 0.40
    XT = 1.5 * KEN
    ZT = -1.5 * KEN                                   # tea room z 0..ZT, the tokonoma strip ZT..-D
    CL = FL_ + 2.15                                   # the tea room's low ceiling
    S = Shell(name or "jp_chashitsu", W, D, [3], "tea hut (DW21)", wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=0.75 if fam == "thatch" else None, soot=False,
                           members="sawn", ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    fin = "nakanuri"
    # front: closed (the nijiri-guchi is decorative); the way in is the mizuya door on the right gable
    S.wall_line("front", [(0.0, W, FL_)], YT, [], finish=fin, nodes_extra=(0.5 * KEN, 1.5 * KEN))
    nijiriguchi(S, "front", 0.25 * KEN, FL_ + 0.05)
    # back (lx = W - x): the mizuya window lx 0.5K..1K
    S.wall_line("back", [(0.0, W, FL_)], YT, [(0.5 * KEN, 1.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window")], finish=fin,
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 1.5 * KEN))
    S.window(openings.part_window_slide("_board"), "back", 0.5 * KEN, FL_, "Mizuya window (back)")
    # left gable (tea room, lx = z + D): the window (renji + shoji) lx 1K..1.5K (parks 1.5K..2K)
    S.wall_line("left", [(0.0, D, FL_)], YG, [(1.0 * KEN, 1.5 * KEN, FL_ + 0.45, FL_ + 2.0, "window")], finish=fin,
                nodes_extra=(0.5 * KEN, 1.0 * KEN, 1.5 * KEN))
    S.window(openings.part_window_slide("_shoji"), "left", 1.0 * KEN, FL_, "Tea room window (end)")
    S.wall_line("right", [(0.0, D, FL_)], YG, [(0.25 * KEN, 1.25 * KEN, FL_, FL_ + 2.0, "door")], finish=fin,
                nodes_extra=(0.25 * KEN, 1.25 * KEN, 1.75 * KEN))
    S.door(openings.part_shoji_ext("_single"), "right", 0.25 * KEN, FL_, "Mizuya door (the way in)", "door")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_thatch" if fam == "thatch" else "_board", thatch=(fam == "thatch"))
    # partition x = XT (tea room | mizuya): the sadoguchi (a fusuma) lx 0.5K..1.5K (z -1.5K..-0.5K), parks to 2K
    B.interior = True
    FX = (90.0, (XT, 0.0, -D))
    S.wall_line((FX, D, "part_x"), [(0.0, D, FL_)], YG, [(0.25 * KEN, 1.25 * KEN, FL_, FL_ + 2.0, "door")],
                finish="nakanuri", grime=False, interior="both", nodes_extra=(0.25 * KEN, 1.25 * KEN, 1.75 * KEN))
    S.door(part_fusuma("_single"), FX, 0.25 * KEN, FL_, "Mizuya <-> tea room (sadoguchi)", "sado")
    B.interior = False
    # the tea room above its low ceiling is closed by an interior gable over x = XT (the mizuya is open to the roof)
    interior_gable(S, XT, D, t, E, "gable_xt")
    # floors: 3 mats (x 0..1.5K, z ZT..-0.5K), 1 mat (x 0..1K, z -0.5K..0), the board half-mat with the ro (x 1K..1.5K),
    # the tokonoma strip (toko x 0..1K + a board 1K..1.5K)
    B.interior = True
    B.merge(FL.tatami("chashitsu", A_, XT - A_, ZT, -0.5 * KEN, top=FL_, base=0.0, mats=FL.MATS_TATAMI_B1,
                      cells=(3, 2)))
    B.merge(FL.tatami("chashitsu_1", A_, KEN, -0.5 * KEN, -A_, top=FL_, base=0.0, mats=FL.MATS_TATAMI_B1, cells=(2, 1)))
    ro = (1.25 * KEN - 0.21, 1.25 * KEN + 0.21, -0.25 * KEN - 0.21, -0.25 * KEN + 0.21)
    B.merge(FL.boards("chashitsu_ro", KEN, XT - A_, -0.5 * KEN, -A_, FL_, holes=[ro + ("pit",)],
                      hole_fn=PI.pit_fn("irori"), mats=FL.MATS_BOARDS_B1))
    B.merge(FL.boards("toko_strip", A_, XT - A_, -D + A_, ZT, FL_, mats=FL.MATS_BOARDS_B1))
    B.merge(FL.boards("mizuya", XT + A_, W - A_, -D + A_, -A_, FL_, mats=BOARDS_ROUGH))
    B.interior = False
    S.fittings.append({"kind": "ro", "room": "chashitsu", "rect": ro, "floor_y": FL_,
                       "note": "the sunken hearth (ro) for the tea kettle, in the board half-mat"})
    S.obst.append(("chashitsu", _r(ro[0] - 0.10, ro[1] + 0.10, ro[2] - 0.10, ro[3] + 0.10)))
    # the tokonoma: back wall (lx = W - x): x 0..1K -> lx 2K..3K; its post on the open side (x = 1K, lx 2K)
    ceiling(S, "ceiling", (A_, XT - A_, -D + A_, -A_), CL)
    tokonoma(S, "chashitsu", S.F["back"], W - KEN, W - A_, W - A_, FL_, CL, depth=0.5 * KEN, wall_a=False,
             wall_c=False, chigai=False, post_at="a")
    st = Part("tea_step", "", "")
    found.step(st, 0.75 * KEN, "natural", drop=FL_, width=1.04)
    B.put(st, S.F["right"], 0.0, FL_, what="found.step (natural): the stepping stone at the mizuya door")
    fit(S, "tsukubai", None, centre=(0.40, 1.60), size=(0.6, 0.6), yaw=0.0, obstacle=False,
        note="stone basin (tsukubai) + lantern by the nijiri-guchi: site props")
    fit(S, "mizuya_shelf", "mizuya", rect=(W - A_ - 0.40, W - A_, -D + 0.20, -0.30), y=FL_, obstacle=False,
        note="the mizuya's shelves + sink (sunoko drain): props")
    S.place_windows()
    S.room("chashitsu", "zashiki", "tatami", FL_, (A_, XT - A_, -D + A_, -A_), [S.dn["sado"]],
           "the tea room (4.5 mats, the ro, the tokonoma at the back, the low ceiling)")
    S.room("mizuya", "storage", "boards", FL_, (XT + A_, W - A_, -D + A_, -A_), [S.dn["door"], S.dn["sado"]],
           "the mizuya (prep room): the way in")
    trim_lods(S.H)
    return S.finish({"params": {"kind": "chashitsu", "roof": roof}, "levels": {"floor": FL_, "eave": E, "ceiling": CL},
                     "koyagumi": K["counts"]},
                    exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)


# ================================================================================================ DW23 itagura
def itagura(name=None, roof="itabuki", wear="_w2"):
    """DW23 board storehouse (itagura): W 2 x D 1.5 ken on posts with rat guards (stilts.platform 'ratguard', floor
    +0.60), board walls, a kirizuma board or tile roof, one plank door + a wooden step."""
    W, D = 2 * KEN, 1.5 * KEN
    DROP = 0.60
    fam = roof if roof in ("itabuki", "sangawara") else "itabuki"
    E = DROP + 2.70                                  # the wagoya tie beams clear the floor by >= 2.10
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_itagura", W, D, [1, 2], "board storehouse (DW23)", wear)
    S.ceilings = []
    B = S.B
    pl = Part("stilts", "", "")
    r = STL.platform(pl, W, D, drop=DROP, kind="ratguard")
    B.put(pl, (0.0, (0.0, 0.0, 0.0)), 0.0, DROP, what="stilts.platform ratguard (+%.2f)" % DROP)
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn", joya_posts=False)
    S.keta_ring(W, D, E, hip=False)
    for side, L in (("front", W), ("back", W), ("left", D), ("right", D)):
        xs = [k * HALF for k in range(int(round(L / HALF)) + 1)] if side in ("front", "back") else \
            [k * HALF for k in range(int(round(L / HALF)) + 1)]
        B.posts_on(S.F[side], [v for v in xs if abs(v % KEN) < 1e-6 or abs(v - L) < 1e-6], DROP,
                   YT if side in ("front", "back") else YG)
    bw = dict(mat="wood_weathered")
    B.wall(S.F["front"], "front", "board_vertical", 0.0, W, DROP, YT, openings_=[(A_, KEN - A_, DROP, DROP + 2.0)], **bw)
    B.wall(S.F["back"], "back", "board_vertical", 0.0, W, DROP, YT, **bw)
    B.wall(S.F["left"], "left", "board_vertical", 0.0, D, DROP, YG, **bw)
    B.wall(S.F["right"], "right", "board_vertical", 0.0, D, DROP, YG, **bw)
    from .sacred import line_board_walls
    line_board_walls(S.H)
    S.door(openings.part_itado("_single"), "front", 0.0, DROP, "Door (itagura)", "door")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    st = Part("itagura_step", "", "")
    found.step(st, 0.5 * KEN, "wood", drop=DROP, width=1.20)
    B.put(st, S.F["front"], 0.0, DROP, what="found.step (wood): the step up to the door")
    S.room("kura", "storage", "boards", DROP, (A_, W - A_, -D + A_, -A_), [S.dn["door"]],
           "the board storehouse: grain bales, straw bags, tools, seed (rat guards on the posts)")
    S.obst.append(("kura", _r(A_, KEN + 0.10, -0.50, -A_)))
    stones_as_soseki(S.H)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "itagura", "roof": roof}, "levels": {"floor": DROP, "eave": E},
                        "koyagumi": K["counts"]}, exterior=lambda x, z: False)
    return H, info


# ================================================================================================ DW25 stable
def stable(name=None, animal="horse", wear="_w2"):
    """DW25 detached stable: horse (W 3 x D 2.5 ken, two stalls side by side, a tack corner, board walls, board roof) or
    ox (W 2 x D 2.5 ken, one ox stall + the fodder corner, thatch). Earth floor; a big plank door; a barred window."""
    horse = animal == "horse"
    W, D = (3 * KEN if horse else 2 * KEN), 2.5 * KEN
    fam = "itabuki" if horse else "thatch"
    E = 3.10
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_stable", W, D, [1, 2], "stable (DW25), %s" % animal, wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=0.90 if fam == "thatch" else None, soot=False, ridge="bamboo")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    ff = [(0.0, KEN, DOMA, DOMA + 2.0, "door")]
    if horse:
        ff.append((2.0 * KEN, 2.5 * KEN, DOMA + 1.00, DOMA + 1.75, "window"))
    S.wall_line("front", [(0.0, W, DOMA)], YT, ff, nodes_extra=(2.0 * KEN, 2.5 * KEN) if horse else (), **bw)
    S.door(big_leaf("_battened"), "front", 0.0, DOMA, "Stable door", "door")
    if horse:
        S.window(openings.part_window_slide("_board"), "front", 2.0 * KEN, DOMA + 0.10, "Window (front)")
    S.wall_line("back", [(0.0, W, DOMA)], YT, (), **bw)
    for side in ("left", "right"):
        S.wall_line(side, [(0.0, D, DOMA)], YG, (), **bw)
        S.gable(side, D, t, E, "_board", thatch=(fam == "thatch"))
    B.interior = True
    B.merge(FL.doma("floor", 0.0, W, -D, 0.0, road=(A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    v = "_row2" if horse else "_ox"
    wst, dst = SL.VARIANTS[v][0] * KEN, SL.VARIANTS[v][1] * KEN
    x0s = 0.5 * KEN if horse else KEN - A_ - 0.06 + A_
    if not horse:
        x0s = W - A_ - 0.06 - wst
    B.interior = True
    B.merge(SL.part_stall(v).transformed(0.0, (x0s, DOMA, -D + dst)))
    B.interior = False
    S.obst.append(("floor", _r(x0s - 0.12, x0s + wst + 0.12, -D, -D + dst + 0.14)))
    S.fittings.append({"kind": "stall", "room": "floor", "rect": (x0s, x0s + wst, -D + A_, -D + dst),
                       "note": "jp_p_frame_stall %s, bars down (as left)" % v})
    if horse:
        fit(S, "tack", "floor", rect=(W - A_ - 0.35, W - A_, -D + 0.30, -1.0 * KEN), obstacle=False,
            note="the tack corner: pack saddles, harness, straw horseshoes on the end wall")
    else:
        fit(S, "fodder", "floor", rect=(A_ + 0.05, KEN - 0.10, -D + 0.20, -1.2 * KEN), obstacle=False,
            note="the fodder corner: straw, the fodder cutter, the plough")
    S.place_windows()
    S.room("floor", "storage", "earth", DOMA, (A_, W - A_, -D + A_, -A_), [S.dn["door"]],
           "the stable: %s, the aisle by the door" % ("two stalls side by side" if horse else "the ox stall"))
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "stable", "animal": animal}, "levels": {"doma": DOMA, "eave": E},
                        "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


# ================================================================================================ DW27 bath hut
def furoba(name=None, wear="_w2"):
    """DW27 bath hut (furoba / yudono): W 1.5 x D 1 ken, board walls, board roof with a small koshiyane steam vent; a
    slatted washing floor (sunoko) by the door, the tub spot (the tub is a prop: goemon vs teppo-buro is a late source,
    BL 'verify') with its firing side on the back wall (outside)."""
    W, D = 1.5 * KEN, 1.0 * KEN
    fam = "itabuki"
    E = 2.95
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    S = Shell(name or "jp_furoba", W, D, [1, 2], "bath hut (DW27)", wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    bw = dict(kind="board_vertical", mat="wood_weathered", grime=False)
    S.wall_line("front", [(0.0, W, DOMA)], YT, [(0.0, KEN, DOMA, DOMA + 2.0, "door")], **bw)
    S.door(openings.part_itado("_single"), "front", 0.0, DOMA, "Door (bath hut)", "door")
    S.wall_line("back", [(0.0, W, DOMA)], YT, (), **bw)
    S.wall_line("left", [(0.0, D, DOMA)], YG, (), **bw)
    S.wall_line("right", [(0.0, D, DOMA)], YG, [(0.0, 0.5 * KEN, DOMA + 1.40, DOMA + 1.85, "window")],
                nodes_extra=(0.5 * KEN,), **bw)
    S.window(openings.part_window_slide("_board"), "right", 0.0, DOMA + 0.50, "Steam window (end)")
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_board")
    koshiyane(S, 0.25 * KEN, 1.0 * KEN, info_r, E, D, fam)
    B.interior = True
    B.merge(FL.doma("furoba", 0.0, W, -D, 0.0, road=(A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    SU = (A_ + 0.10, KEN - 0.40, -D + A_ + 0.10, -A_ - 0.65)
    B.merge(PI.sunoko("sunoko", SU[0], SU[1], SU[2], SU[3], DOMA + 0.10, "slat"))
    B.interior = False
    S.obst.append(("furoba", _r(SU[0] - 0.05, SU[1] + 0.05, SU[2] - 0.05, SU[3] + 0.05)))
    fit(S, "tub", "furoba", rect=(KEN + 0.02, W - A_ - 0.02, -D + A_ + 0.02, -0.30), y=DOMA, obstacle=False,
        note="the bath tub (prop; firebox through the back wall outside): the furnisher keeps loot off it")
    S.place_windows()
    S.room("furoba", "storage", "earth", DOMA, (A_, W - A_, -D + A_, -A_), [S.dn["door"]],
           "the bath hut: the tub spot, the door")
    S.room("sunoko", "storage", "slats", DOMA + 0.10, (SU[0] + 0.02, SU[1] - 0.02, SU[2] + 0.02, SU[3] - 0.02), [],
           "the slatted washing floor")
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "furoba"}, "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


# ================================================================================================ DW29 nagaya-mon
def nagayamon(name=None, rank="samurai", wear="_w1"):
    """DW29 gatehouse with rooms (nagaya-mon): W 7 x D 2 ken, one storey; the gate passage x 2.75..4.25 ken with the
    hinged leaf pair (gates.gate_leaves) on the street line; the servants' room on the left (a 1-ken doma + a raised
    board room, its door to the yard), a storage doma on the right (door to the yard). rank 'samurai': plaster
    (shikkui) with a namako lower front, sangawara (T29: plaster allowed for samurai); 'headman': board walls, a board
    roof (commoners use boards, T29)."""
    W, D = 7 * KEN, 2 * KEN
    sam = rank == "samurai"
    fam = "sangawara" if sam else "itabuki"
    E = 3.30
    YT, YG = E - KETA_H, E - 0.21
    t = R.PITCH[fam]
    FL_ = FLOOR_R
    XL, XP0, XP1 = 1.75 * KEN, 2.75 * KEN, 4.25 * KEN    # raised room | doma | passage | storage
    S = Shell(name or "jp_nagayamon", W, D, [2, 3], "gatehouse with rooms (DW29), %s" % rank, wear)
    S.ceilings = []
    B = S.B
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, soot=False, members="sawn")
    S.keta_ring(W, D, E, hip=False)
    for x in (XP0, XP1):
        S.post(x, 0.0, YT, size=G.POST_K, mat="wood_street_dark" if sam else "wood_weathered")
    for s_ in S.H.solids:
        if s_.tag == "post":
            s_.tag = "gate_post"
    wk = dict(finish="nakanuri") if sam else dict(kind="board_vertical", mat="wood_weathered", grime=False)
    # front (street): left part (room + doma), the passage left open, right part (storage); barred windows
    S.wall_line(((0.0, (0.0, 0.0, 0.0)), XP0, "front_l"), [(0.0, XL, FL_), (XL, XP0, DOMA)], YT,
                [(0.75 * KEN, 1.25 * KEN, FL_ + 0.90, FL_ + 1.65, "window")], nodes_extra=(0.75 * KEN, 1.25 * KEN), **wk)
    S.window(openings.part_window_slide("_board"), "front", 0.75 * KEN, FL_, "Servants' room window (street)")
    S.wall_line(((0.0, (XP1, 0.0, 0.0)), W - XP1, "front_r"), [(0.0, W - XP1, DOMA)], YT,
                [(1.0 * KEN, 1.5 * KEN, DOMA + 1.00, DOMA + 1.75, "window")], nodes_extra=(1.0 * KEN, 1.5 * KEN), **wk)
    S.window(openings.part_window_slide("_board"), (0.0, (XP1, 0.0, 0.0)), 1.0 * KEN, DOMA + 0.10,
             "Storage window (street)")
    # back (yard, lx = W - x): storage door lx 0.5K..1.5K (parks to 2K), the passage open, the doma door
    # lx 4.25K..5.25K (x 2.75K..1.75K, parks to 5.75K), room window lx 6K..6.5K
    S.wall_line(((180.0, (W, 0.0, -D)), W - XP1, "back_r"), [(0.0, W - XP1, DOMA)], YT,
                [(0.5 * KEN, 1.5 * KEN, DOMA, DOMA + 2.0, "door")], nodes_extra=(0.5 * KEN, 1.5 * KEN, 2.0 * KEN), **wk)
    S.door(openings.part_itado("_single"), (180.0, (W, 0.0, -D)), 0.5 * KEN, DOMA, "Storage door (yard)", "storage")
    FBL = (180.0, (XP0, 0.0, -D))                     # back wall of the left part: lx = XP0 - x
    S.wall_line((FBL, XP0, "back_l"), [(0.0, XP0 - XL, DOMA), (XP0 - XL, XP0, FL_)], YT,
                [(0.0, KEN, DOMA, DOMA + 2.0, "door"), (1.5 * KEN, 2.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window")],
                nodes_extra=(0.0, KEN, 1.5 * KEN, 2.0 * KEN, 2.5 * KEN), **wk)
    S.door(openings.part_itado("_single"), FBL, 0.0, DOMA, "Servants' room door (yard)", "room")
    S.window(openings.part_window_slide("_board"), FBL, 1.5 * KEN, FL_, "Servants' room window (yard)")
    # the passage side walls (x = XP0: the doma's wall, x = XP1: the storage wall), closed
    # the passage side walls are earth (shinkabe) on both ranks: a board wall hangs its boards and collision slab on
    # the passage face, where the gate leaves park when open
    S.wall_line(((-90.0, (XP0, 0.0, 0.0)), D, "pass_l"), [(0.0, D, DOMA)], YT, (), finish="nakanuri")
    S.wall_line(((90.0, (XP1, 0.0, -D)), D, "pass_r"), [(0.0, D, DOMA)], YT, (), finish="nakanuri")
    S.wall_line("left", [(0.0, D, FL_)], YG, [(0.5 * KEN, 1.0 * KEN, FL_ + 0.90, FL_ + 1.65, "window")],
                nodes_extra=(0.5 * KEN, 1.0 * KEN), **wk)
    S.window(openings.part_window_slide("_board"), "left", 0.5 * KEN, FL_, "Servants' room window (end)")
    S.wall_line("right", [(0.0, D, DOMA)], YG, (), **wk)
    for g_ in ("left", "right"):
        S.gable(g_, D, t, E, "_tile" if sam else "_board")
    # over the gate: a head beam on the gate posts + the wall above to the eave (street side and yard side beams)
    hd = B.P("gate_head")
    for z in (0.0, -D):
        hd.add(box(XP0, XP1, G.BEAM_Y, G.BEAM_Y + 0.18, z - 0.09, z + 0.09, "wood_street_dark" if sam else
                   "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kamoi_beam"))
    B.merge(hd)
    B.wall((0.0, (0.0, 0.0, 0.0)), "gate_over", "shinkabe" if sam else "board_vertical", XP0, XP1, G.BEAM_Y + 0.18,
           YT, finish="nakanuri", head=False, mat=None if sam else "wood_weathered")
    gp = G.gate_leaves("_board", XP1 - XP0, y0=DOMA + 0.03, y_floor=DOMA, swing_deg=70.0)
    S.door(gp, (0.0, (XP0, 0.0, 0.0)), 0.0, 0.0, "Gate leaves (nagaya-mon)", "gate")
    # floors
    B.interior = True
    B.merge(FL.boards("room", A_, XL - 0.06, -D + A_, -A_, FL_, mats=BOARDS_ROUGH))
    B.merge(FL.doma("doma", XL, XP0, -D, 0.0, road=(XL + 0.07, XP0 - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.doma("storage", XP1, W, -D, 0.0, road=(XP1 + A_, W - A_, -D + A_, -A_), y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.merge(FL.doma("gate", XP0 - 0.10, XP1 + 0.10, -D - 0.30, 0.30, road=(XP0 + 0.12, XP1 - 0.12, -D - 0.15, 0.15),
                    y=DOMA, mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.kamachi((90.0, (XL, 0.0, -D)), D, FL_, [1.0 * KEN], "doma")
    S.obst.append(("gate", _r(XP0, XP1, -1.40, 0.10)))
    if sam:
        plaster_exterior(S, W, D)
        for (fr, a, b) in (((0.0, (0.0, 0.0, 0.0)), 0.06, 0.75 * KEN - 0.06), ((0.0, (0.0, 0.0, 0.0)), 1.25 * KEN + 0.06,
                                                                               XP0 - 0.15),
                           ((0.0, (XP1, 0.0, 0.0)), 0.15, 1.0 * KEN - 0.06),
                           ((0.0, (XP1, 0.0, 0.0)), 1.5 * KEN + 0.06, W - XP1 - 0.06)):
            nm = B.P("namako_%d" % int(a * 100 + fr[1][0] * 10))
            walls.namako(nm, a, b, 0.05, 0.95, 0.0375 + 0.002, diagonal=True)
            B.put(nm, fr, what="walls.namako (diagonal) on the street face")
    S.place_windows()
    S.room("room", "sleeping", "boards", FL_, (A_, XL - 0.07, -D + A_, -A_), [],
           "the servants' room (chugen-beya), raised boards, open to its doma")
    S.room("doma", "doma", "earth", DOMA, (XL + 0.07, XP0 - A_, -D + A_, -A_), [S.dn["room"]],
           "the servants' doma by the yard door")
    S.room("storage", "storage", "earth", DOMA, (XP1 + A_, W - A_, -D + A_, -A_), [S.dn["storage"]],
           "storage / a stable bay")
    S.room("gate", "yard", "earth", DOMA, (XP0 + 0.12, XP1 - 0.12, -D - 0.15, 0.15), [S.dn["gate"]],
           "the gate passage (street +z, yard -z)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "nagayamon", "rank": rank}, "levels": {"doma": DOMA, "floor": FL_, "eave": E},
                        "koyagumi": K["counts"]},
                       exterior=lambda x, z: abs(z) < 1e-6 or abs(z + D) < 1e-6 or abs(x) < 1e-6 or abs(x - W) < 1e-6)
    return H, info


# ================================================================================================ compounds (K3's kits)
def _wall_path(nodes, kind, ends=("end", "end"), gaps=(), closed=False, name="walls", abut=(0.0, 0.0), **opt):
    """K3's sitewall.run_wall module loop, with chosen path-end types and gate GAPS [(segment, offset, span)]: the
    walls either side of a gap end 'post' (the gates themselves are placed by the caller as doors). Walk the plot
    clockwise seen from above (x east, z north): +z of every module = outside.
    abut=(d0, d1) (FX5): an open path end that butts against another wall continues d m past its grid node (off the
    half-ken grid) to that wall's face, so the two meet with no gap (its end post stands against the face)."""
    from .. import sitewall as W
    P = Part(name, "", "")
    n = len(nodes)
    segs = [(nodes[i], nodes[(i + 1) % n]) for i in range(n if closed else n - 1)]
    if not closed and (abut[0] > 0.01 or abut[1] > 0.01):
        rseed_ = W.run_seed(name)
        for which, d in ((0, abut[0]), (1, abut[1])):
            if d <= 0.01:
                continue
            a, b = (segs[0] if which == 0 else segs[-1])
            Ls_ = math.hypot(b[0] - a[0], b[1] - a[1])
            u_ = ((b[0] - a[0]) / Ls_, (b[1] - a[1]) / Ls_)
            deg_ = math.degrees(math.atan2(u_[1], u_[0]))
            if which == 0:
                q = W.wall(kind, d, (ends[0], "seam"), seed=7, pid=name + "_abut0", run=(-d, rseed_), **opt)
                o = (a[0] - u_[0] * d, a[1] - u_[1] * d)
            else:
                tot = sum(math.hypot(bb[0] - aa[0], bb[1] - aa[1]) for aa, bb in segs)
                q = W.wall(kind, d, ("seam", ends[1]), seed=8, pid=name + "_abut1", run=(tot, rseed_), **opt)
                o = b
            P.merge(q.transformed(deg_, (o[0], 0.0, o[1])))
        ends = ("seam" if abut[0] > 0.01 else ends[0], "seam" if abut[1] > 0.01 else ends[1])

    def turn(i, j):
        (a, b), (c, d) = segs[i], segs[j]
        d1 = ((b[0] - a[0]), (b[1] - a[1]))
        d2 = ((d[0] - c[0]), (d[1] - c[1]))
        cr = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(cr) < 1e-9:
            return "seam"
        return "corner+z" if cr > 0 else "corner-z"
    rseed = W.run_seed(name)
    s_seg = 0.0
    for i, (a, b) in enumerate(segs):
        dx, dz = b[0] - a[0], b[1] - a[1]
        Ls = math.hypot(dx, dz)
        deg = math.degrees(math.atan2(dz, dx))
        e0 = turn(i - 1, i) if (closed or i > 0) else ends[0]
        e1 = turn(i, (i + 1) % len(segs)) if (closed or i < len(segs) - 1) else ends[1]
        runs, x = [], 0.0
        for g in sorted([g for g in gaps if g[0] == i], key=lambda g: g[1]):
            runs.append((x, g[1], "post_end"))
            x = g[1] + g[2]
        runs.append((x, Ls, None))
        for ri, (x0, x1, tail) in enumerate(runs):
            if x1 - x0 < 0.05:
                continue
            mods = W._split(x1 - x0)
            xx = x0
            for mi, m in enumerate(mods):
                s0 = e0 if xx < 1e-6 else ("post" if (mi == 0 and ri > 0) else "seam")
                if abs(xx + m - Ls) < 1e-6:
                    s1 = e1
                elif mi == len(mods) - 1 and tail:
                    s1 = "post"
                else:
                    s1 = "seam"
                q = W.wall(kind, m, (s0, s1), seed=int(xx * 100) + i * 1000, pid=name + "_%d_%d_%d" % (i, ri, mi),
                           run=(s_seg + xx, rseed), **opt)
                P.merge(q.transformed(deg, (a[0] + math.cos(math.radians(deg)) * xx, 0.0,
                                            a[1] + math.sin(math.radians(deg)) * xx)))
                xx += m
        s_seg += Ls
    return P


def _gate_part(kind, span):
    from .. import sitewall as W
    ly0 = FL.SILL_TOP + 0.03                 # FX5: the leaves clear the raised sill pad of the passage
    if kind.startswith("kabuki"):
        return W.gate_kabuki(span, roofed=kind.endswith("roofed"), leaf_y0=ly0)
    if kind == "munemon":
        return W.gate_munemon(span, leaf_y0=ly0)
    p = W.wicket(kind.split("_", 1)[1] if "_" in kind else "itabei", span)
    # the wicket's one hinged leaf carries no twin name: give it the DoorsTwin convention (one selection, an
    # <twin>_action point) so Builder.place_door can number it
    d = p.doors[0]
    bones = {a_["bone"] for a_ in d.anims}
    d.twin = "doorstwin1"
    for s in p.solids:
        if s.door in bones:
            s.sel = "doorstwin1"
    for k in list(p.memory):
        if k.endswith("_action") and k[:-len("_action")] in bones:
            p.memory["doorstwin1_action"] = p.memory.pop(k)
    return p


# per compound: plot W x D (ken grid; kit frame x east 0..W, z north 0..D), wall runs [(nodes, kind, opts, ends)],
# gates [(run index, segment, offset, kind, span)]
COMPOUNDS = {
    # DW19 hatamoto mansion: the samurai nagaya-mon (a separate object, 7 ken) stands in the gap of the south line;
    # black board fence (itabei kuro) round the other three sides
    "samurai_m": dict(W=13 * KEN, D=17.5 * KEN, gate_obj=(4.5 * KEN, 11.5 * KEN),
                      runs=[([(4.5 * KEN, 0.0), (0.0, 0.0), (0.0, 17.5 * KEN), (13 * KEN, 17.5 * KEN), (13 * KEN, 0.0),
                              (11.5 * KEN, 0.0)], "itabei", dict(kuro=True, cap="none"), ("end", "end"))],
                      gates=[(0, 2, 6 * KEN, "kabuki", KEN)]),
    # DW16 Kanto headman: the board nagaya-mon in the south line, a tall clipped hedge (ikegaki) round the yard
    "headman_east": dict(W=20 * KEN, D=17 * KEN, gate_obj=(6.5 * KEN, 13.5 * KEN),
                         runs=[([(6.5 * KEN, 0.0), (0.0, 0.0), (0.0, 17 * KEN), (20 * KEN, 17 * KEN), (20 * KEN, 0.0),
                                 (13.5 * KEN, 0.0)], "ikegaki", dict(size="tall"), ("end", "end"))],
                         gates=[(0, 2, 9.5 * KEN, "kabuki", KEN)]),
    # the honjin: a plastered wall (dobei) along the street front (north) with the roofed kabuki-mon (T19: the
    # formal front gate), board fences round the sides and the back
    "honjin": dict(W=17 * KEN, D=26 * KEN,
                   runs=[([(0.0, 26 * KEN), (17 * KEN, 26 * KEN)], "dobei", dict(finish="shikkui"), ("end", "end")),
                         ([(17 * KEN, 25.5 * KEN), (17 * KEN, 0.0), (0.0, 0.0), (0.0, 25.5 * KEN)], "itabei",
                          dict(kuro=False, cap="none"), ("end", "end"))],
                   gates=[(0, 0, 4.5 * KEN, "kabuki_roofed", 1.5 * KEN), (1, 1, 8 * KEN, "kabuki", KEN)]),
    # the great merchant's garden: a plain board fence with a wicket to the lane behind the shop row
    "merchant": dict(W=16.5 * KEN, D=15 * KEN, closed=True,
                     runs=[([(0.0, 0.0), (0.0, 15 * KEN), (16.5 * KEN, 15 * KEN), (16.5 * KEN, 0.0)], "itabei",
                            dict(kuro=False, cap="none"), ("end", "end"))],
                     gates=[(0, 3, 3 * KEN, "kabuki", KEN)]),
    # the ashigaru row: a bamboo (yotsume) fence along the lane with a small board gate
    "kumi": dict(W=10 * KEN, D=1 * KEN,
                 runs=[([(0.0, 0.0), (10 * KEN, 0.0)], "yotsume", {}, ("end", "end"))],
                 gates=[(0, 0, 4.5 * KEN, "kabuki", KEN)]),
    # the doshin house: a plain board fence round the plot, a simple (unroofed) kabuki gate
    "doshin": dict(W=10 * KEN, D=8 * KEN, closed=True,
                   runs=[([(0.0, 0.0), (0.0, 8 * KEN), (10 * KEN, 8 * KEN), (10 * KEN, 0.0)], "itabei",
                          dict(kuro=False, cap="none"), ("end", "end"))],
                   gates=[(0, 1, 6.5 * KEN, "kabuki", 1.5 * KEN)]),
}


# FX5: half the thickness of each wall kind at its face (a run that butts against it stops at this face)
_HALF_THICK = {"dobei": 0.15, "tsuiji": 0.45, "itabei": 0.08, "yotsume": 0.06, "kenninji": 0.05, "shiba": 0.07,
               "takeho": 0.07}


def _half_thick(kind, opt):
    if kind == "ikegaki":
        return (0.70 if opt.get("size", "low") == "low" else 0.90) / 2
    return _HALF_THICK.get(kind, 0.10)


def _abut(runs, ri):
    """(d0, d1) for run ri's open ends (FX5, Stephen's 3a walk: the honjin's plastered street wall and its board
    fences stopped half a ken apart, a 0.70 m walk-through gap): if the line of the run, continued past an end node,
    meets another run's wall line within 1.5 ken, the run is extended to that wall's near face."""
    nodes = runs[ri][0]
    out = []
    for which in (0, 1):
        a, b = (nodes[0], nodes[1]) if which == 0 else (nodes[-1], nodes[-2])
        L = math.hypot(a[0] - b[0], a[1] - b[1])
        u = ((a[0] - b[0]) / L, (a[1] - b[1]) / L)                # pointing out of the run, past its end node
        best = 0.0
        for rj, (n2, k2, o2, _e) in enumerate(runs):
            if rj == ri:
                continue
            for c, d in zip(n2, n2[1:]):
                # the other segment's line (axis-aligned plots): distance t along u to it, within its extent
                if abs(c[1] - d[1]) < 1e-6 and abs(u[1]) > 0.5:
                    t = (c[1] - a[1]) / u[1]
                    x = a[0] + u[0] * t
                    ok = min(c[0], d[0]) - 1e-6 <= x <= max(c[0], d[0]) + 1e-6
                elif abs(c[0] - d[0]) < 1e-6 and abs(u[0]) > 0.5:
                    t = (c[0] - a[0]) / u[0]
                    zz = a[1] + u[1] * t
                    ok = min(c[1], d[1]) - 1e-6 <= zz <= max(c[1], d[1]) + 1e-6
                else:
                    continue
                if ok and 0.0 < t <= 1.5 * KEN:
                    best = max(best, t - _half_thick(k2, o2))
        out.append(best)
    return tuple(out)


def compound(name=None, plot="samurai_m", wear="_w1"):
    """A compound's walls / fences / hedges and its gate(s), from K3's wall kit (parts/K3_NOTES.md section 6), as one
    map object: the plot in the kit frame (x east, z north, origin at the south-west corner). Gate passages are
    open floors (loot may lie there); a gatehouse (nagaya-mon) is a separate building in the gap of the line."""
    spec = COMPOUNDS[plot]
    W, D = spec["W"], spec["D"]
    S = Shell(name or "jp_compound", W, D, [2, 3], "compound walls (%s)" % plot, wear)
    S.ceilings = []
    gaps = {}
    for (ri, si, off, kind, span) in spec["gates"]:
        gaps.setdefault(ri, []).append((si, off, span))
    for ri, (nodes, kind, opt, ends) in enumerate(spec["runs"]):
        ab = (0.0, 0.0) if spec.get("closed", False) else _abut(spec["runs"], ri)
        S.H.merge(_wall_path(nodes, kind, ends=ends, gaps=gaps.get(ri, ()), closed=spec.get("closed", False),
                             name="%s_run%d" % (plot, ri), abut=ab, **opt))
        for (x, z) in nodes:
            S.posts.append((round(x, 4), round(z, 4), 0.0, 1.8))
    for gi, (ri, si, off, kind, span) in enumerate(spec["gates"]):
        nodes = spec["runs"][ri][0]
        a, b = nodes[si], nodes[(si + 1) % len(nodes)]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        deg = math.degrees(math.atan2(u[1], u[0]))
        ox, oz = a[0] + u[0] * off, a[1] + u[1] * off
        S.door(_gate_part(kind, span), (deg, (ox, 0.0, oz)), 0.0, 0.0, "Gate (%s)" % kind.replace("_", " "),
               "gate%d" % gi)
        for t in (0.0, span):
            S.posts.append((round(ox + u[0] * t, 4), round(oz + u[1] * t, 4), 0.0, 2.9))
        # the gate passage: an earth strip through the opening (the inside is -z of the run = to the right of travel)
        px0, pz0 = ox + u[0] * 0.15, oz + u[1] * 0.15
        px1, pz1 = ox + u[0] * (span - 0.15), oz + u[1] * (span - 0.15)
        nx, nz = -u[1], u[0]                                  # local +z (outside)
        cs = [(px0 + nx * 1.1, pz0 + nz * 1.1), (px1 + nx * 1.1, pz1 + nz * 1.1), (px0 - nx * 1.3, pz0 - nz * 1.3),
              (px1 - nx * 1.3, pz1 - nz * 1.3)]
        rx0, rx1 = min(c[0] for c in cs), max(c[0] for c in cs)
        rz0, rz1 = min(c[1] for c in cs), max(c[1] for c in cs)
        nm = "gate%d" % gi
        # FX5: a packed-earth sill pad (top 0.10 over grade, sloped margins into the ground) instead of an earth slab
        # whose top lay exactly at grade and z-fought with the terrain (Stephen's 3a walk: every compound gate)
        prect = (rx0 - 0.30, rx1 + 0.30, rz0 - 0.30, rz1 + 0.30)
        S.B.interior = True
        pad = FL.sill_pad(nm, *prect)
        S.B.merge(pad)
        S.B.interior = False
        rx0, rx1, rz0, rz1 = pad.meta["top_rect"]
        # the leaves' swing (inside, 1.3 m) and the closed line stay clear of loot
        sw = [(px0 + nx * 0.30, pz0 + nz * 0.30), (px1 + nx * 0.30, pz1 + nz * 0.30),
              (px0 - nx * 0.30, pz0 - nz * 0.30), (px1 - nx * 0.30, pz1 - nz * 0.30)]
        S.obst.append((nm, _r(min(c[0] for c in sw), max(c[0] for c in sw), min(c[1] for c in sw),
                              max(c[1] for c in sw))))
        S.room(nm, "yard", "earth", FL.SILL_TOP, (rx0, rx1, rz0, rz1), [S.dn[nm]], "the gate passage (%s)" % kind,
               enclosed=False)
        # stepping stones (tobi-ishi) through the gate: separate flat stones at grade, one outside, two inside
        from ..core import stone as _stone, rng_for as _rng
        rr = _rng("tobi" + plot + str(gi))
        mx_, mz_ = ox + u[0] * span / 2, oz + u[1] * span / 2
        for k_, dd in enumerate((1.25, 0.75, -0.75, -1.25)):
            sx, sz = mx_ + nx * dd, mz_ + nz * dd
            # each stone's flat top 3.5 cm over the surface it lies in (the sill pad or the ground): never coplanar
            ty = FL.sill_height(sx, sz, prect) + 0.035
            st_ = _stone(rr, sx, sz, 0.42, 0.36, 0.10 + ty, ty, "stone_field", bury=0.08, n=7, flat_top=0.8,
                         vis=(1, 2), tag="soseki")
            S.H.add(st_)
    trim_lods(S.H)
    for s_ in S.H.solids:
        if s_.tag == "hedge_core":
            s_.fire = True                     # vanilla house LOD set: the hedge's core is its Fire Geometry too
        if s_.tag in ("board_field", "board_field_lod") and s_.vis and 1 in s_.vis:
            s_.vis = set(s_.vis) | {2, 3}      # C15: the small gate roof keeps its whole field in the far LODs
    H, info = S.finish({"params": {"kind": "compound", "plot": plot}, "levels": {"grade": 0.0},
                        "centre_kit": (W / 2, D / 2), "gate_obj": spec.get("gate_obj")})
    return H, info


# ------------------------------------------------------------------------------------------------ corridors
ROKA = {
    # the honjin: omote (left gable corridor door) <-> oku (right gable corridor door), 2 ken, half-walled, tiled
    "honjin": dict(path=[(0.0, 0.0), (0.0, 2 * KEN)], sides=("half", "half"), roof="sangawara", floor=0.50, stairs=(),
                   connect=(True, True), step=None),
    # the town temple U (W2F): from the hondo's side veranda (0.75) east to the kuri's genkan porch: the deck at the
    # veranda level, no rail on the north (the step down to the porch's stone pad at the open end), a koran on the
    # south (a 2-ken run has no room for K3's stair: the 0.70 step down is the level change)
    "temple_u": dict(path=[(2 * KEN, 0.0), (0.0, 0.0)], sides=("none", "open"), roof="itabuki", floor=0.75,
                     stairs=(), connect=(False, True), step=("start_right", 0.70)),
}


def roka(name=None, run="honjin", wear="_w1"):
    """A covered corridor (watari-roka) from K3's corridor kit (roka.run_roka) as one map object. Kit frame = the
    path's frame (grid nodes); the hosts' wall / veranda lines lie on the connected path ends."""
    from .. import roka as RK
    spec = ROKA[run]
    path = spec["path"]
    xs = [p[0] for p in path]
    zs = [p[1] for p in path]
    W = max(xs) - min(xs) + KEN
    D = max(zs) - min(zs) + KEN
    S = Shell(name or "jp_roka", W, D, [2, 3], "covered corridor (%s)" % run, wear)
    S.ceilings = []
    P = RK.run_roka(path, sides=spec["sides"], roof=spec["roof"], floor=spec["floor"], stairs=spec["stairs"],
                    connect=spec["connect"], name="roka_" + run)
    S.H.merge(P)
    for (x, z) in path:
        S.posts.append((round(x, 4), round(z, 4), 0.0, spec["floor"]))
    if spec.get("step"):
        where, drop = spec["step"]
        a, b = path[0], path[1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        # a step off the deck on the right of travel near the open start; its ramp runs out from the deck
        nx, nz = u[1], -u[0]
        cx, cz = a[0] + u[0] * 0.25 * KEN, a[1] + u[1] * 0.25 * KEN
        deg = math.degrees(math.atan2(-nx, nz))
        st = Part("roka_step", "", "")
        found.step(st, 0.0, "natural", drop=drop, width=1.04)
        S.B.put(st, (deg, (cx + nx * (KEN / 2 + 0.02), 0.0, cz + nz * (KEN / 2 + 0.02))), 0.0, spec["floor"],
                what="found.step: off the corridor deck at its open end")
    stones_as_soseki(S.H)
    trim_lods(S.H)
    for s_ in S.H.solids:
        if s_.tag == "kutsunugi" and s_.vis:
            s_.vis = set(s_.vis) | {2, 3}       # the step stone outside the roof keeps its far LODs (C15)
        if s_.tag == "board_field" and s_.vis and 1 in s_.vis:
            s_.vis = set(s_.vis) | {2, 3}       # C15: the board field overhangs the far sheathing at the eaves
    # the deck as a loot floor (the flat run at the corridor's start level; stairs and connectors excluded)
    a, b = path[0], path[1]
    L0 = math.hypot(b[0] - a[0], b[1] - a[1])
    u = ((b[0] - a[0]) / L0, (b[1] - a[1]) / L0)
    s0 = 0.5 * KEN if spec["connect"][0] else 0.0
    run0 = (spec["stairs"][0][1] if spec["stairs"] else L0 - (0.5 * KEN if spec["connect"][1] else 0.0)) - s0
    p0 = (a[0] + u[0] * (s0 + 0.10), a[1] + u[1] * (s0 + 0.10))
    p1 = (a[0] + u[0] * (s0 + run0 - 0.10), a[1] + u[1] * (s0 + run0 - 0.10))
    hw = 0.70
    rx0, rx1 = min(p0[0], p1[0]) - (hw if abs(u[1]) > 0.5 else 0.0), max(p0[0], p1[0]) + (hw if abs(u[1]) > 0.5 else 0.0)
    rz0, rz1 = min(p0[1], p1[1]) - (hw if abs(u[0]) > 0.5 else 0.0), max(p0[1], p1[1]) + (hw if abs(u[0]) > 0.5 else 0.0)
    S.room("deck", "veranda", "boards", spec["floor"], (rx0, rx1, rz0, rz1), [], "the corridor deck", enclosed=False)
    H, info = S.finish({"params": {"kind": "roka", "run": run}, "levels": {"floor": spec["floor"]},
                        "centre_kit": ((max(xs) + min(xs)) / 2, (max(zs) + min(zs)) / 2)})
    return H, info


BUILDERS = {"mountain": mountain, "coastal": coastal, "samurai": samurai, "doshin": doshin, "merchant": merchant,
            "honjin_omote": honjin_omote, "honjin_oku": honjin_oku, "wakihonjin": wakihonjin, "kumi": kumi,
            "headman_east": headman_east, "headman_kinai": headman_kinai, "chashitsu": chashitsu, "itagura": itagura,
            "stable": stable, "furoba": furoba, "nagayamon": nagayamon, "compound": compound, "roka": roka}


def build(kind, **params):
    if kind not in BUILDERS:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(sorted(BUILDERS))))
    return BUILDERS[kind](**params)


BUDGET = {"mountain": "large", "coastal": "standard", "kumi": "large", "doshin": "large",
          "headman_east": "large", "headman_kinai": "large", "merchant": "large", "samurai": "large",
          "chashitsu": "small", "itagura": "small", "stable": "standard", "furoba": "small", "nagayamon": "standard",
          "honjin_omote": "large", "honjin_oku": "large", "wakihonjin": "large", "compound": "large",
          "roka": "standard"}


def budget_class(kind, **params):
    """PLAYBOOK §12 class per kind (the house sizes decide: >20 m2 one storey = standard; the big compounds' houses
    'large'; the tea hut, storehouse and bath hut 'small')."""
    if kind == "samurai" and params.get("size") == "s":
        return "large"
    return BUDGET[kind]


def over_budget_ok(kind, **params):
    """CA1: a deliberate overage (<= +50 %, PLAYBOOK §12) and its reason, or None."""
    if kind == "coastal" and params.get("roof", "ishioki") == "ishioki":
        return "stone-weighted board roof: every weighting stone and batten is geometry (C2 huts: the same cost)"
    tiled = "tiled status residence: kawara geometry over a 7-10 ken house + the genkan porch, the engawa, the "             "tokonoma and the ceilings in one object"
    if kind in ("samurai", "wakihonjin", "honjin_omote"):
        return tiled
    if kind in ("merchant", "honjin_oku"):
        return "tiled 7.5-8 ken residence: kawara geometry + the kitchen + ceilinged rooms (+ the engawa)"
    if kind == "kumi" and params.get("roof") == "sangawara":
        return "a 9-ken tiled row of three dwellings in one object (kawara geometry)"
    if kind == "headman_east":
        return "the biggest thatched house (10 x 5 ken under one hipped roof with geya aisles): the thatch outline "                "pieces stay in every LOD (C15)"
    if kind == "headman_kinai":
        return "9 x 4 ken thatch with takahe gables + tiled lower roofs on both long walls + the tiled genkan lean-to"
    if kind == "chashitsu":
        return "a small hut with a full thatch / shingle outline kept in the far LODs (C15) + the built-in tokonoma"
    if kind == "itagura" and params.get("roof") == "sangawara":
        return "a 2 x 1.5 ken storehouse under a kawara roof (kawara geometry is the cost)"
    if kind == "nagayamon" and params.get("rank", "samurai") == "samurai":
        return "a 7-ken plastered gatehouse with namako lower walls (tile + joint geometry) and a kawara roof"
    if kind == "nagayamon":
        return "a 7-ken gatehouse (two rooms + the gate passage and its leaves) in one object"
    if kind == "compound" and params.get("plot") == "honjin":
        return "a 86-ken compound ring (plastered street wall + board fences) and two gates in one object"
    if kind == "compound" and params.get("plot") == "headman_east":
        return "a 67-ken ring of clipped hedge (every hedge lump is geometry in Resolution 1; the far LODs are one core)"
    return None


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as rural.model."""
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
