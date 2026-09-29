"""Openings (build list jp_p_open_*): sliding doors in B's proven format, windows, lattices, shop closures.

Every passable door is a 1-ken bay (posts at x = 0 and 1.82, clear 1.70 m between post faces): one leaf covers the
opening and parks along the facade over the NEXT bay (D1: never across a passage). Outside leaves (itado) run on a
track on the exterior face, inside leaves (koshido, shoji) on the interior face. The part carries its tracks over the
park bay; that bay must be a plain wall on the parking face (no wainscot / lattice there) - connector 'park'.
Opening parts fill a hole the wall recipe leaves (walls.wall_run(openings=[...])).
"""
import math

from .core import (Part, Door, box, prism, KEN, HALF, POST, DOOR_H, WALL_H, GAP, OV, STUB, sliding_leaf, rng_for, add,
                   mul)
from .shapes import board_run, tube, oriented_box, clip_rect
from . import kawara

A, B = POST / 2, KEN - POST / 2          # 1-ken bay opening between post faces


# ------------------------------------------------------------------------------------------------ shared bits
def tracks(part, x0, x1, z_face, side, thick=0.04, mat="wood_weathered", head_y=DOOR_H, sill_y=0.0):
    """Sill track (flush with the floor / window sill) and head track on the face the leaf runs on, over door + park
    bays."""
    tw = thick + 2 * GAP + 0.02
    z0, z1 = sorted((z_face, z_face + side * tw))
    part.add(box(x0, x1, sill_y - 0.03, sill_y, z0, z1, mat, vis=(1, 2), tag="track"))
    part.add(box(x0, x1, head_y + 0.035, head_y + 0.14, z0, z1, mat, vis=(1, 2, 3), tag="track"))


def threshold(part, a, b, mat="wood_weathered", depth=POST):
    part.add(box(a, b, -0.10, 0.0, -depth / 2, depth / 2, mat, vis=(1, 2), geo=True, view=False, fire=True,
                 tag="threshold"))
    part.road([(a, 0.0, -depth / 2), (b, 0.0, -depth / 2), (b, 0.0, depth / 2), (a, 0.0, depth / 2)], "boards_ext")


# G3 fix 2 (2026-09-29): Stephen, from inside the front door: "post on the left, closed leaf on the right, daylight
# between them". A closed leaf overlapped its post by only OV = 2 cm while it ran 1.2 cm (inner track) to 6.4 cm (outer
# track) in front of the post face, so the jamb was an open slot (PLAYBOOK §15 T11, check C17). Real doors close
# against a stop (todome) on the closing post and slide over a lip on the post they pass.
JAMB_CLEAR = 0.002       # air between a leaf (edge or face) and a stop / lip
STOP_W = 0.045           # closing-jamb stop width, on the post face beside the leaf edge
MEET = 0.05              # hikichigai meeting-stile overlap (was OV = 0.02: a 1.2 cm slot at 59 degrees, C17)
LEAF_GAP = 0.0           # boards of a door / shutter leaf butt tight: board_run's default 4 mm gap went right through
#                          the leaf (nothing behind it in Resolution 1), so every closed plank leaf showed daylight lines


def strip(x0, x1, y0, y1, z0, z1, zface, mat="wood_weathered", vis=(1, 2), tag="jamb_stop"):
    """A strip fixed to a post / stile face: only its two x ends and its z face away from the post (z0 or z1 = zface
    side is hidden against the post; top and bottom meet the tracks) - 3 faces, visual only."""
    zo = z1 if abs(z0 - zface) < abs(z1 - zface) else z0
    sz = 1.0 if zo == z1 else -1.0
    from .core import sheet
    q = [([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], (-1.0, 0.0, 0.0)),
         ([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], (1.0, 0.0, 0.0)),
         ([(x0, y0, zo), (x1, y0, zo), (x1, y1, zo), (x0, y1, zo)], (0.0, 0.0, sz))]
    return sheet([a for a, _ in q], mat, [n for _, n in q], vis=vis, tag=tag)


def jamb_stop(part, x_edge, dirn, y0, y1, z_face, z_far, mat="wood_weathered"):
    """CLOSING jamb (the leaf's trailing edge closes here and slides away in `dirn`): a stop on the post face, beside
    the closed leaf's edge, from the wall face out past the outermost leaf face z_far. Seals the jamb (C17)."""
    xa, xb = x_edge - dirn * JAMB_CLEAR, x_edge - dirn * (JAMB_CLEAR + STOP_W)
    part.add(strip(min(xa, xb), max(xa, xb), y0, y1, min(z_face, z_far), max(z_face, z_far), z_face, mat,
                   tag="jamb_stop"))


def jamb_lip(part, x0, x1, y0, y1, z_face, z_leaf, mat="wood_weathered"):
    """A post / stile the leaf SLIDES PAST: a lip on its face filling the gap under the leaf's inner face z_leaf (minus
    JAMB_CLEAR), so the leaf still slides over it but no ray gets between post and leaf (C17)."""
    zl = z_leaf - math.copysign(JAMB_CLEAR, z_leaf - z_face)
    part.add(strip(x0, x1, y0, y1, min(z_face, zl), max(z_face, zl), z_face, mat, tag="jamb_lip"))


def pull_x(l0, l1, dirn, w=0.08, inset=0.06):
    """Hikite / iron pull on the TRAILING edge (the edge that stays in the doorway, STUB, when the leaf is open), so
    the open leaf can be pulled shut (G3 fix 2, Stephen: "every door with a handle is backwards"). It used to sit at
    l1 on every leaf, i.e. on the LEADING edge of the +x sliding leaves, which parks behind the wall."""
    return (l0 + inset, l0 + inset + w) if dirn > 0 else (l1 - inset - w, l1 - inset)


def door_conns(part, bay=KEN, park=KEN, park_side=+1, face="exterior"):
    for x in (0.0, bay):
        part.conn("post", (x, 0, 0))
    part.conn("post", (bay + park if park_side > 0 else -park, 0, 0), note="far end of the park bay")
    part.conn("sill", (0, 0, 0), note="runs in a grooved sill at floor level")
    part.conn("head", (0, DOOR_H, 0))
    part.conn("park", ((bay if park_side > 0 else -park), 0, 0), length=park, face=face,
              note="the next bay must be a plain wall on the %s face: the open leaf parks there" % face)


def leaf_plank(style, mat, rng):
    def build(l0, l1, bot, top, z0, z1, bone, dirn=+1):
        out = [box(l0, l1, bot, top, z0, z1, mat, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
        W = l1 - l0
        zin, zout = (z0, z1)
        if style == "plain":
            for s in board_run(l0, l1, bot, top, z0 + 0.012, z1, rng, 0.20, 0.30, mat, vis=(1,), tag="leaf_board",
                               gap=LEAF_GAP):
                out.append(s)
            for yy in (bot + 0.25, (bot + top) / 2, top - 0.30):
                out.append(box(l0 + 0.05, l1 - 0.05, yy, yy + 0.09, z0, z0 + 0.012, mat, vis=(1,), tag="leaf_batten"))
        else:
            sw = 0.075
            out.append(box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,), tag="stile"))
            out.append(box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,), tag="stile"))
            out.append(box(l0 + sw, l1 - sw, bot, bot + 0.10, z0, z1, mat, vis=(1,), tag="rail"))
            out.append(box(l0 + sw, l1 - sw, top - 0.08, top, z0, z1, mat, vis=(1,), tag="rail"))
            for s in board_run(l0 + sw, l1 - sw, bot + 0.10, top - 0.08, z0 + 0.012, z1 - 0.01, rng, 0.22, 0.30, mat,
                               gap=LEAF_GAP,
                               vis=(1,), tag="leaf_board"):
                out.append(s)
            nb = 4
            for k in range(nb):
                yy = bot + 0.25 + k * (top - bot - 0.55) / (nb - 1)
                out.append(box(l0 + sw, l1 - sw, yy, yy + 0.07, z1 - 0.01, z1 + 0.008, mat, vis=(1,), tag="leaf_batten"))
            if style == "oodo":
                # decorative kuguri wicket (D9): its own frame, battens and iron fittings; not a working door
                kx0 = l0 + 0.30
                kx1 = kx0 + 0.60
                ky0, ky1 = bot + 0.12, bot + 0.12 + 1.20
                for (a, b, c, d) in ((kx0, kx0 + 0.05, ky0, ky1), (kx1 - 0.05, kx1, ky0, ky1), (kx0, kx1, ky1 - 0.05, ky1),
                                     (kx0, kx1, ky0, ky0 + 0.05)):
                    out.append(box(a, b, c, d, z1 - 0.01, z1 + 0.018, mat, vis=(1,), tag="kuguri"))
                for yy in (ky0 + 0.30, ky1 - 0.35):
                    out.append(box(kx0 + 0.05, kx1 - 0.05, yy, yy + 0.06, z1 - 0.01, z1 + 0.015, mat, vis=(1,),
                                   tag="kuguri"))
                for (xx, yy) in ((kx0 + 0.02, ky0 + 0.25), (kx0 + 0.02, ky1 - 0.25), (kx1 - 0.08, ky0 + 0.6)):
                    out.append(box(xx, xx + 0.06, yy, yy + 0.10, z1 + 0.015, z1 + 0.025, "metal_iron", vis=(1,),
                                   tag="iron"))
            # the pull on the trailing (stub) edge; 10 mm proud, clear of a leaf on the next track (GAP 12 mm)
            px0, px1 = pull_x(l0, l1, dirn)
            out.append(box(px0, px1, bot + 0.95, bot + 1.05, z1 - 0.004, z1 + 0.010, "metal_iron", vis=(1,),
                           tag="pull"))
        return out
    return build


def leaf_lattice(papered, mat):
    def build(l0, l1, bot, top, z0, z1, bone, dirn=+1):
        # View Geometry even when open-barred: DayZ targets a door only through a View Geometry component (G3 fix)
        out = [box(l0, l1, bot, top, z0, z1, mat, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
        sw = 0.05
        out += [box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,)), box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,)),
                box(l0 + sw, l1 - sw, top - 0.05, top, z0, z1, mat, vis=(1,)),
                box(l0 + sw, l1 - sw, bot, bot + 0.30, z0 + 0.008, z1 - 0.008, mat, vis=(1,), tag="lower_board"),
                box(l0 + sw, l1 - sw, bot + 0.30, bot + 0.35, z0, z1, mat, vis=(1,))]
        n = int((l1 - l0 - 2 * sw) / 0.06)
        for k in range(n):
            x = l0 + sw + (k + 0.5) * (l1 - l0 - 2 * sw) / n
            out.append(box(x - 0.015, x + 0.015, bot + 0.35, top - 0.05, z0 + 0.004, z1 - 0.004, mat, vis=(1,), tag="bar"))
        for yy in (bot + 1.0, bot + 1.55):
            out.append(box(l0 + sw, l1 - sw, yy, yy + 0.025, z0 + 0.002, z0 + 0.012, mat, vis=(1,), tag="nuki"))
        if papered:
            out.append(box(l0 + sw, l1 - sw, bot + 0.35, top - 0.05, z0 - 0.001, z0 + 0.002, "paper_shoji", vis=(1, 2),
                           tag="paper"))
        return out
    return build


def open_bar(x0, x1, y0, y1, z0, z1, mat, axis, tag="kumiko"):
    """A thin visual bar without its two hidden end faces (they butt into stiles / rails): 4 faces, not 6."""
    from .core import sheet
    if axis == "y":            # vertical bar: keep the x and z faces
        q = [([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], (-1.0, 0.0, 0.0)),
             ([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], (1.0, 0.0, 0.0)),
             ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0.0, 0.0, -1.0)),
             ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0.0, 0.0, 1.0))]
    else:                      # horizontal bar: keep the y and z faces
        q = [([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], (0.0, -1.0, 0.0)),
             ([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0.0, 1.0, 0.0)),
             ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0.0, 0.0, -1.0)),
             ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0.0, 0.0, 1.0))]
    return sheet([a for a, _ in q], mat, [n for _, n in q], vis=(1,), tag=tag)


def fixed_panel(kind, x0, x1, y0, y1, z0, z1, rng=None):
    """A light static panel beside a single sliding leaf (sode): one collision box + a frame, few faces (the R1
    budget of a house has room for about ten doors)."""
    fm = "wood_weathered" if kind == "shoji" else "wood_street_dark"
    out = [box(x0, x1, y0, y1, z0, z1, {"front": "paper_shoji", "back": "paper_shoji", "default": fm} if kind == "shoji"
               else fm, vis=(2, 3), geo=True, view=True, fire="fabric_thin" if kind == "shoji" else True, uv="fit",
               tag="fixed_panel")]
    if kind == "shoji":
        sw, low = 0.035, 0.30
        out += [box(x1 - sw, x1, y0, y1, z0, z1, fm, vis=(1,), tag="fixed_panel"),
                box(x0, x1, y1 - 0.04, y1, z0, z1, fm, vis=(1,), tag="fixed_panel"),
                box(x0, x1, y0, y0 + low + 0.035, z0 + 0.004, z1 - 0.004, fm, vis=(1,), tag="fixed_panel"),
                box(x0, x1 - sw, y0 + low + 0.035, y1 - 0.04, (z0 + z1) / 2 - 0.0015, (z0 + z1) / 2 + 0.0015,
                    "paper_shoji", vis=(1,), tag="fixed_panel")]
        xm = (x0 + x1 - sw) / 2
        out.append(open_bar(xm - 0.008, xm + 0.008, y0 + low + 0.035, y1 - 0.04, z0 + 0.003, z1 - 0.003, fm, "y"))
        y = y0 + low + 0.035 + 0.40
        while y < y1 - 0.2:
            out.append(open_bar(x0, x1 - sw, y - 0.008, y + 0.008, z0 + 0.003, z1 - 0.003, fm, "x"))
            y += 0.40
    else:
        out.append(box(x0, x1, y0, y1, z0, z1, fm, vis=(1,), uv="fit", tag="fixed_panel"))
        for yy in (y0 + 0.30, y1 - 0.40):
            out.append(box(x0 + 0.02, x1 - 0.02, yy, yy + 0.07, z1, z1 + 0.012, fm, vis=(1,), tag="fixed_panel"))
    return out


def leaf_shoji(low, mat="wood_weathered"):
    def build(l0, l1, bot, top, z0, z1, bone, dirn=+1):
        out = [box(l0, l1, bot, top, z0, z1, {"front": "paper_shoji", "back": "paper_shoji", "default": mat},
                   vis=(2, 3), geo=True, view=True, fire="fabric_thin", uv="fit", tag="leaf")]
        sw = 0.035
        mid = (l0 + l1) / 2
        out += [box(l0, l0 + sw, bot, top, z0, z1, mat, vis=(1,)), box(l1 - sw, l1, bot, top, z0, z1, mat, vis=(1,)),
                box(mid - sw / 2, mid + sw / 2, bot, top, z0, z1, mat, vis=(1,), tag="centre_stile"),
                box(l0, l1, top - 0.04, top, z0, z1, mat, vis=(1,)),
                box(l0, l1, bot, bot + low, z0 + 0.004, z1 - 0.004, mat, vis=(1,), tag="lower_board"),
                box(l0, l1, bot + low, bot + low + 0.035, z0, z1, mat, vis=(1,))]
        zc = (z0 + z1) / 2
        out.append(box(l0 + sw, l1 - sw, bot + low + 0.035, top - 0.04, zc - 0.0015, zc + 0.0015, "paper_shoji", vis=(1,),
                       uv="world", tag="paper"))
        for (a, b) in ((l0 + sw, mid - sw / 2), (mid + sw / 2, l1 - sw)):
            for k in (1, 2, 3):
                x = a + (b - a) * k / 4
                out.append(open_bar(x - 0.008, x + 0.008, bot + low + 0.035, top - 0.04, z0 + 0.003, z1 - 0.003, mat,
                                    "y"))
        y = bot + low + 0.035 + 0.25
        while y < top - 0.1:
            out.append(open_bar(l0 + sw, l1 - sw, y - 0.008, y + 0.008, z0 + 0.003, z1 - 0.003, mat, "x"))
            y += 0.25
        return out
    return build


def sliding_door_part(pid, variant, tiers, used, leaf_build, kind, side, thick, mat_track="wood_weathered",
                      bay=KEN, park=KEN, note=""):
    p = Part(pid, variant, "open", tiers=tiers, used_for=used,
             datum="1-ken door bay between post nodes x=0 and x=1.82 + its park bay to x=3.64; y 0 = sill/floor")
    zf = side * POST / 2
    sliding_leaf(p, A, bay - POST / 2, 0.0, DOOR_H, zf, side, +1, None, thick=thick, kind=kind, build=leaf_build,
                 park_span=(A - OV, bay + park - POST / 2), note=note)
    tracks(p, A, bay + park - POST / 2, zf, side, thick, mat_track)
    threshold(p, A, bay - POST / 2)
    door_conns(p, bay, park, +1, "exterior" if side > 0 else "interior")
    d = p.doors[0]
    zc = zf + side * (GAP + thick / 2)
    jamb_stop(p, A - OV, +1, 0.0, DOOR_H + 0.035, zf, zc + side * (thick / 2 + 0.010))      # C17 closing jamb
    jamb_lip(p, bay - POST / 2, bay + POST / 2, 0.0, DOOR_H + 0.035, zf, zf + side * GAP)   # C17 post it slides past
    p.dim("clear_opening_m", ">=1.00", (bay - POST / 2) - A, source="D1")
    p.dims[-1]["ok"] = (bay - POST) >= 1.0
    p.dim("head_m", DOOR_H, d.opening[3] - d.opening[2], source="D2")
    p.dim("leaf_slide_m (= leaf width - overlap - STUB)", round(d.width - OV - STUB, 4), d.slide)
    return p


# ------------------------------------------------------------------------------------------------ twin leaves
def _leaf_set(part, specs, y0, height, thick, leaf_build, mats, kind):
    """Leaves [(l0, l1, zc, direction, slide, what)] -> anims; every leaf a bone, memory point <bone> on its trailing
    edge at hand height (vanilla: the point stays in the doorway when open)."""
    anims = []
    bot, top = y0 + 0.004, y0 + height + 0.03
    for (l0, l1, zc, dirn, slide, what) in specs:
        bone = "doors%d" % (sum(len(d.anims) for d in part.doors) + len(anims) + 1)
        z0, z1 = zc - thick / 2, zc + thick / 2
        solids = leaf_build(l0, l1, bot, top, z0, z1, bone, dirn=dirn) if leaf_build else [
            box(l0, l1, bot, top, z0, z1, mats, vis=(1, 2, 3), geo=True, view=True, fire=True, uv="fit", tag="door")]
        for s in solids:
            s.door = bone
            part.add(s)
        centre = ((l0 + l1) / 2, (bot + top) / 2, zc)
        axis = [centre, (centre[0] + dirn, centre[1], centre[2])]
        part.memory[bone + "_axis"] = axis
        part.memory[bone] = [(l0 + 0.04, y0 + 1.0, zc) if dirn > 0 else (l1 - 0.04, y0 + 1.0, zc)]
        anims.append({"bone": bone, "type": "translation", "axis": axis, "amount": slide, "note": what})
    return anims


def _twin_door(part, anims, x0, x1, y0, height, z_face, side, kind, note, tr_in, thick, tr_out, sweep, style, stub,
               window=False):
    mid = (x0 + x1) / 2
    twin = "doorstwin%d" % (len(part.doors) + 1)
    action = (mid, y0 + min(1.0, height / 2), z_face)
    part.memory[twin + "_action"] = [action]
    d = Door(kind=kind, anims=anims, action=action, centre=(mid, y0 + height / 2, tr_in), twin=twin,
             width=None, slide=anims[0]["amount"], direction=(1.0, 0.0, 0.0),
             anim_period=1.0 if kind == "plank" else 0.8, init_opened=0.3 if kind == "plank" else 0.5,
             display="%s %s" % (kind, "window" if window else "door"), note=note, opening=(x0, x1, y0, y0 + height),
             z_face=z_face, side=side, leaf_z=tuple(sorted((tr_in - side * thick / 2, tr_out + side * thick / 2))),
             sweep=sweep, park_end=sweep[1], engine_tested=False, style=style, stub=stub, passable=not window,
             act_h=y0 + min(1.0, height / 2))
    bones = {a["bone"] for a in anims}
    for s in part.solids:
        if s.door in bones:
            s.sel = twin
    part.doors.append(d)
    return d


def twin_leaves(part, x0, x1, y0, height, z_face, side, leaf_build, thick, kind, note="", mats=None, stub=STUB,
                window=False):
    """HIKICHIGAI (main entrances only, PLAYBOOK §15): two period-size leaves (~0.89 m) on two tracks covering the
    opening [x0, x1]; ONE door action (vanilla 'DoorsTwinN': one config class, two bones on the same source) slides
    both into a stack over the next half-ken in +x. Both leaves stop with `stub` still in the opening (vanilla rule:
    the open leaf must stay aimable from the other side). Returns the Door (twin name, action point <twin>_action)."""
    mid = (x0 + x1) / 2
    tr_in = z_face + side * (GAP + thick / 2)
    tr_out = tr_in + side * (thick + GAP)
    far = (x0 - OV, mid + MEET / 2)         # far leaf: left half, outer track
    near = (mid - MEET / 2, x1 + OV)        # near leaf: right half, inner track (MEET overlap at the meeting stiles)
    stop = x1 - stub                        # both trailing edges end here, stacked
    park_end = stop + max(near[1] - near[0], far[1] - far[0])
    anims = _leaf_set(part, [(far[0], far[1], tr_out, +1, stop - far[0], "far leaf, outer track"),
                             (near[0], near[1], tr_in, +1, stop - near[0], "near leaf, inner track")],
                      y0, height, thick, leaf_build, mats, kind)
    d = _twin_door(part, anims, x0, x1, y0, height, z_face, side, kind, note, tr_in, thick, tr_out,
                   (far[0], park_end), "hikichigai", stub, window)
    d.width = near[1] - near[0]
    # C17: a stop on the closing post (the far leaf closes against it, out past the outer track) and a lip on the post
    # the near leaf slides past (fills the 12 mm under it)
    y1 = y0 + height + 0.035
    jamb_stop(part, far[0], +1, y0, y1, z_face, tr_out + side * (thick / 2 + 0.010))
    jamb_lip(part, x1, x1 + POST, y0, y1, z_face, tr_in - side * thick / 2)
    return d


def split_leaves(part, x0, x1, y0, height, z_face, side, leaf_build, thick, kind, note="", mats=None, stub=STUB):
    """HIKIWAKE (interior fusuma / shoji pairs, PLAYBOOK §15): two leaves part in the middle and slide in opposite
    directions, each over its own half-ken; one door action. Left leaf on the outer track, right leaf on the inner
    track (MEET = 0.05 overlap at the meeting stiles, G3 fix 2). Each stops with `stub` in the opening."""
    mid = (x0 + x1) / 2
    tr_in = z_face + side * (GAP + thick / 2)
    tr_out = tr_in + side * (thick + GAP)
    left = (x0 - OV, mid + MEET / 2)         # MEET overlap at the meeting stiles (C17; was OV = 2 cm)
    right = (mid - MEET / 2, x1 + OV)
    sl = left[1] - (x0 + stub)
    sr = (x1 - stub) - right[0]
    anims = _leaf_set(part, [(left[0], left[1], tr_out, -1, sl, "left leaf, slides left, outer track"),
                             (right[0], right[1], tr_in, +1, sr, "right leaf, slides right, inner track")],
                      y0, height, thick, leaf_build, mats, kind)
    d = _twin_door(part, anims, x0, x1, y0, height, z_face, side, kind, note, tr_in, thick, tr_out,
                   (left[0] - sl, right[1] + sr), "hikiwake", stub)
    d.width = left[1] - left[0]
    # C17: both leaves slide past a post: a lip under each (the left leaf runs on the outer track: fill up to it)
    y1 = y0 + height + 0.035
    jamb_lip(part, x0 - POST, x0, y0, y1, z_face, tr_out - side * thick / 2)
    jamb_lip(part, x1, x1 + POST, y0, y1, z_face, tr_in - side * thick / 2)
    return d


def twin_door_part(pid, variant, tiers, used, leaf_build, kind, side, thick, note=""):
    """1-ken door bay (posts x = 0 and 1.82) + a half-ken park bay to x = 2.73 on the leaves' face."""
    p = Part(pid, variant, "open", tiers=tiers, used_for=used,
             datum="1-ken door bay between post nodes x=0 and x=1.82 + a half-ken park bay to x=2.73; y 0 = sill/floor",
             note="two leaves, one door action (DoorsTwin); needs a plain wall on the park face of the half-ken bay")
    zf = side * POST / 2
    d = twin_leaves(p, A, KEN - POST / 2, 0.0, DOOR_H, zf, side, leaf_build, thick, kind, note=note)
    if d.park_end > KEN + HALF - POST / 2 + 1e-3:
        raise ValueError("%s: parked leaves [.., %.3f] leave the half-ken park bay" % (p.name, d.park_end))
    tracks(p, A, KEN + HALF - POST / 2, zf, side, 2 * thick + GAP)
    threshold(p, A, KEN - POST / 2)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("post", (KEN + HALF, 0, 0), note="far end of the half-ken park bay")
    p.conn("sill", (0, 0, 0), note="runs in a grooved sill at floor level")
    p.conn("head", (0, DOOR_H, 0))
    p.conn("park", (KEN, 0, 0), length=HALF, face="exterior" if side > 0 else "interior",
           note="the next half-ken must be a plain wall on this face: both leaves park there, stacked")
    p.dim("clear_opening_m", ">=1.00", (KEN - POST / 2) - A, source="D1")
    p.dims[-1]["ok"] = (KEN - POST) >= 1.0
    p.dim("leaf_width_m (period ~0.9)", "0.85-0.95", d.width, source="Stephen 2026-09-27")
    p.dim("head_m", DOOR_H, DOOR_H, source="D2")
    p.dim("open_stub_m (vanilla 0.22-0.30)", STUB, d.stub, source="G3 fix: vanilla sliding doors")
    return p


def hikiwake_door_part(pid, variant, tiers, used, leaf_build, kind, side, thick, note=""):
    """1-ken door bay (posts x = 0 and 1.82) + a half-ken park bay on EACH side (x -0.91..0 and 1.82..2.73)."""
    p = Part(pid, variant, "open", tiers=tiers, used_for=used,
             datum="1-ken door bay between post nodes x=0 and x=1.82 + half-ken park bays x=-0.91..0 and 1.82..2.73; "
                   "y 0 = sill/floor",
             note="hikiwake: two leaves part in the middle, one door action (DoorsTwin); plain wall on the park face "
                  "of BOTH neighbouring half-ken bays")
    zf = side * POST / 2
    d = split_leaves(p, A, KEN - POST / 2, 0.0, DOOR_H, zf, side, leaf_build, thick, kind, note=note)
    if d.sweep[0] < -HALF + POST / 2 - 1e-3 or d.sweep[1] > KEN + HALF - POST / 2 + 1e-3:
        raise ValueError("%s: parked leaves %s leave the half-ken park bays" % (p.name, d.sweep))
    tracks(p, -HALF + A, KEN + HALF - POST / 2, zf, side, 2 * thick + GAP)
    threshold(p, A, KEN - POST / 2)
    for x in (-HALF, 0.0, KEN, KEN + HALF):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0), note="runs in a grooved sill at floor level")
    p.conn("head", (0, DOOR_H, 0))
    face = "exterior" if side > 0 else "interior"
    p.conn("park", (-HALF, 0, 0), length=HALF, face=face, note="left leaf parks here: plain wall on this face")
    p.conn("park", (KEN, 0, 0), length=HALF, face=face, note="right leaf parks here: plain wall on this face")
    p.dim("clear_opening_m (both open)", ">=1.00", (KEN - POST / 2 - STUB) - (A + STUB), source="D1")
    p.dims[-1]["ok"] = (KEN - POST - 2 * STUB) >= 1.0
    p.dim("leaf_width_m (period ~0.9)", "0.85-0.95", d.width, source="Stephen 2026-09-27")
    p.dim("head_m", DOOR_H, DOOR_H, source="D2")
    p.dim("open_stub_m (vanilla 0.22-0.30)", STUB, d.stub, source="G3 fix: vanilla sliding doors")
    return p


SINGLE_OPEN = 1.30     # narrow single door: opening between the post face and the fixed panel's stile (clear 1.08)


def single_door_part(pid, variant, tiers, used, leaf_build, kind, side, thick, note="", panel="plank"):
    """KATABIKI narrow single door (side, back and kitchen doors, PLAYBOOK §15): a 1-ken bay narrowed by a fixed
    half-panel (sode, the same leaf build, in the wall plane) to a 1.30 m opening; ONE ~1.34 m leaf slides over the
    fixed panel and the next half-ken, stopping with STUB in the opening (clear 1.08 m, D1). Uses the DoorsTwin
    config convention with one bone, so buildings treat every door alike."""
    p = Part(pid, variant, "open", tiers=tiers, used_for=used,
             datum="1-ken door bay between post nodes x=0 and x=1.82 (opening x 0.06..1.36, fixed panel 1.36..1.76) + "
                   "a half-ken park bay to x=2.73; y 0 = sill/floor",
             note="one leaf, one door action (DoorsTwin with one bone); plain wall on the park face of the next "
                  "half-ken")
    zf = side * POST / 2
    ox1 = A + SINGLE_OPEN
    # fixed panel in the wall plane: a stile + the leaf build (a leaf look-alike that never moves)
    p.add(box(ox1, ox1 + 0.05, 0.0, DOOR_H, -0.03, 0.03, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="fixed_stile"))
    for s in fixed_panel(panel, ox1 + 0.05, B + 0.01, 0.004, DOOR_H + 0.01, -0.02, 0.02):
        p.add(s)
    tr = zf + side * (GAP + thick / 2)
    l0, l1 = A - OV, ox1 + OV
    slide = (ox1 - STUB) - l0
    anims = _leaf_set(p, [(l0, l1, tr, +1, slide, "single leaf")], 0.0, DOOR_H, thick, leaf_build, None, kind)
    d = _twin_door(p, anims, A, ox1, 0.0, DOOR_H, zf, side, kind, note, tr, thick, tr, (l0, l1 + slide), "katabiki",
                   STUB)
    d.width = l1 - l0
    if d.sweep[1] > KEN + HALF - POST / 2 + 1e-3:
        raise ValueError("%s: parked leaf ends at %.3f, beyond the half-ken park bay" % (p.name, d.sweep[1]))
    # C17: a stop on the closing post; a lip on the fixed stile the leaf slides past (its face is 3 cm off the wall
    # plane, the leaf 7.2 cm: a 4 cm slot under a 2 cm overlap before)
    jamb_stop(p, l0, +1, 0.0, DOOR_H + 0.035, zf, tr + side * (thick / 2 + 0.010))
    jamb_lip(p, ox1, ox1 + 0.05, 0.0, DOOR_H + 0.035, side * 0.03, tr - side * thick / 2)
    tracks(p, A, KEN + HALF - POST / 2, zf, side, thick)
    threshold(p, A, ox1)
    for x in (0.0, KEN, KEN + HALF):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0), note="runs in a grooved sill at floor level")
    p.conn("head", (0, DOOR_H, 0))
    p.conn("park", (KEN, 0, 0), length=HALF, face="exterior" if side > 0 else "interior",
           note="the next half-ken must be a plain wall on this face: the leaf parks over the fixed panel and there")
    p.dim("clear_opening_m", ">=1.00", SINGLE_OPEN - STUB, source="D1")
    p.dims[-1]["ok"] = SINGLE_OPEN - STUB >= 1.0
    p.dim("leaf_width_m", "1.30-1.40", d.width, source="D1 + STUB (period back doors ~0.9; gameplay wins)")
    p.dim("head_m", DOOR_H, DOOR_H, source="D2")
    p.dim("open_stub_m (vanilla 0.22-0.30)", STUB, d.stub, source="G3 fix: vanilla sliding doors")
    return p


# ------------------------------------------------------------------------------------------------ itado
def part_itado(variant):
    rng = rng_for("itado" + variant)
    mat = "wood_weathered"
    if variant == "_pair":
        return _itado_pair(rng)
    if variant == "_twin":
        return twin_door_part("jp_p_open_itado", "_twin", [2, 3],
                              "town plank door as two period leaves (~0.88 m) in a 1-ken bay; one action slides both "
                              "into a stack over the next half-ken (1.70 m clear, D1)",
                              leaf_plank("battened", "wood_street_dark", rng), "plank", +1, 0.04,
                              note="exterior leaves, two outside tracks, park stacked over the next half-ken")
    if variant == "_single":
        return single_door_part("jp_p_open_itado", "_single", [1, 2, 3],
                                "narrow single plank door (katabiki) for side, back and kitchen doors: one ~1.34 m "
                                "leaf beside a fixed half-panel, 1.08 m clear (PLAYBOOK §15 door styles)",
                                leaf_plank("battened", "wood_street_dark", rng), "plank", +1, 0.04,
                                note="exterior leaf, parks over the fixed panel and the next half-ken")
    style = {"_plain": "plain", "_battened": "battened", "_oodo": "oodo"}[variant]
    used = {"_plain": "plank sliding door of poor houses (T1), boards only; one 1.74 m leaf parks outside",
            "_battened": "framed and battened plank door, the everyday exterior door (T2)",
            "_oodo": "big entrance door with a decorative kuguri wicket (D9: the wicket does not open)"}[variant]
    p = sliding_door_part("jp_p_open_itado", variant, [1] if variant == "_plain" else [2, 3], used,
                          leaf_plank(style, mat, rng), "plank", +1, 0.04, note="exterior leaf, parks over the next bay")
    p.dims.append({"name": "leaf_thickness_m", "expected": 0.04, "measured": 0.04, "tol": 0.01, "source": "build_list"})
    return p


def _itado_pair(rng):
    """Two leaves, bi-parting, each parking over its own neighbour bay. Built on a 1.5-ken bay, not the build list's
    1-ken: a 1-ken pair gives 0.85 m per leaf, below D1 (logged as a deviation)."""
    bay = 1.5 * KEN
    p = Part("jp_p_open_itado", "_pair", "open", tiers=[2, 3],
             used_for="pair of plank leaves in a 1.5-ken bay, each opening >= 1.00 m (D1; build list said 1 ken)",
             deviation="bay 1.5 ken instead of the build list's 1 ken: a 1-ken pair opens 0.85 m per leaf (< D1)",
             datum="1.5-ken bay x 0..2.73; left leaf parks over x -1.82..0, right leaf over 2.73..4.55")
    mid = bay / 2
    zf = POST / 2
    mat = "wood_weathered"
    sliding_leaf(p, A, mid, 0.0, DOOR_H, zf, +1, -1, None, thick=0.04, kind="plank",
                 build=leaf_plank("battened", mat, rng), park_span=(-KEN + A, mid + OV), note="left leaf")
    sliding_leaf(p, mid, bay - POST / 2, 0.0, DOOR_H, zf + 0.05, +1, +1, None, thick=0.04, kind="plank",
                 build=leaf_plank("battened", mat, rng), park_span=(mid - OV, bay + KEN - POST / 2), note="right leaf")
    tracks(p, -KEN + A, bay + KEN - POST / 2, zf, +1, 0.09)
    threshold(p, A, bay - POST / 2)
    for x in (0.0, bay):
        p.conn("post", (x, 0, 0))
    p.conn("post", (-KEN, 0, 0), note="far end of the left park bay")
    p.conn("post", (bay + KEN, 0, 0), note="far end of the right park bay")
    p.conn("park", (-KEN, 0, 0), length=KEN, face="exterior")
    p.conn("park", (bay, 0, 0), length=KEN, face="exterior")
    p.conn("sill", (0, 0, 0))
    p.conn("head", (0, DOOR_H, 0))
    for d in p.doors:
        o = d.opening
        p.dim("clear_per_leaf_m (%s)" % d.note, ">=1.00", o[1] - o[0], source="D1")
        p.dims[-1]["ok"] = o[1] - o[0] >= 1.0
    return p


def part_koshido(variant):
    pap = variant == "_papered"
    p = sliding_door_part("jp_p_open_koshido", variant, [2, 3],
                          "lattice day door behind the itado, paper behind the bars" if pap
                          else "open-bar lattice day door behind the itado (T2-3 entrances)",
                          leaf_lattice(pap, "wood_street_dark"), "lattice", -1, 0.035,
                          note="interior leaf, parks inside over the next bay")
    p.doors[0].sound = "doorWoodSlide"
    return p


def part_shoji_ext(variant):
    if variant == "_twin":
        p = twin_door_part("jp_p_open_shoji_ext", "_twin", [2, 3],
                           "paper sliding door as two period leaves (~0.88 m) in a 1-ken bay (room fronts on the doma); "
                           "one action slides both into a stack over the next half-ken (1.70 m clear, D1)",
                           leaf_shoji(0.30), "shoji", -1, 0.03, note="paper leaves, two interior tracks")
        p.dim("lower_board_m", 0.30, 0.30)
        return p
    if variant == "_hikiwake":
        p = hikiwake_door_part("jp_p_open_shoji_ext", "_hikiwake", [2, 3],
                               "interior shoji / fusuma pair that parts in the middle (hikiwake): two ~0.88 m leaves "
                               "slide apart over a half-ken each side, 1.26 m clear (PLAYBOOK §15 door styles)",
                               leaf_shoji(0.30), "shoji", -1, 0.03, note="paper leaves, two interior tracks")
        p.dim("lower_board_m", 0.30, 0.30)
        return p
    if variant == "_single":
        p = single_door_part("jp_p_open_shoji_ext", "_single", [2, 3],
                             "narrow single shoji door beside a fixed shoji panel (room entrances off the doma): one "
                             "~1.34 m leaf, 1.08 m clear (PLAYBOOK §15 door styles)",
                             leaf_shoji(0.30), "shoji", -1, 0.03, note="paper leaf, interior track", panel="shoji")
        p.dim("lower_board_m", 0.30, 0.30)
        return p
    low = 0.60 if variant == "_koshidaka" else 0.15
    p = sliding_door_part("jp_p_open_shoji_ext", variant, [1] if variant == "_koshidaka" else [2, 3],
                          "board-bottomed paper door of nagaya and doma entrances (T1)" if variant == "_koshidaka"
                          else "plain shoji line behind the amado of a veranda (T2)",
                          leaf_shoji(low), "shoji", -1, 0.03, note="paper door, interior track")
    p.doors[0].kind = "shoji"
    p.doors[0].anim_period = 0.8
    p.doors[0].init_opened = 0.5
    p.dim("lower_board_m", low, low)
    return p


# ------------------------------------------------------------------------------------------------ amado + tobukuro
def amado_leaves(part, x0, x1, y0=0.0, z=0.0, mat="wood_weathered", geo=True):
    n = max(1, round((x1 - x0) / HALF))
    w = (x1 - x0) / n
    rng = rng_for(part.name + "amado")
    for k in range(n):
        a, b = x0 + k * w, x0 + (k + 1) * w
        part.add(box(a, b + 0.01, y0 + 0.005, y0 + DOOR_H + 0.03, z - 0.015, z + 0.015, mat, vis=(2, 3), geo=geo,
                     view=geo, fire=True if geo else None, tag="amado"))
        part.extend(board_run(a + 0.03, b - 0.03, y0 + 0.04, y0 + DOOR_H - 0.01, z - 0.009, z + 0.0, rng, 0.14, 0.22, mat,
                              vis=(1,), tag="amado_board"))
        for (c, d, e, f) in ((a, a + 0.03, y0, y0 + DOOR_H + 0.03), (b - 0.03, b, y0, y0 + DOOR_H + 0.03),
                             (a, b, y0, y0 + 0.04), (a, b, y0 + DOOR_H - 0.01, y0 + DOOR_H + 0.03)):
            part.add(box(c, d, e, f, z - 0.015, z + 0.015, mat, vis=(1,), tag="amado_frame"))
        for yy in (0.55, 1.05, 1.55):
            part.add(box(a + 0.03, b - 0.03, y0 + yy, y0 + yy + 0.025, z + 0.0, z + 0.012, mat, vis=(1,), tag="amado_bar"))


def part_amado(variant):
    closed = variant == "_closed"
    p = Part("jp_p_open_amado", variant, "open", tiers=[2, 3],
             used_for="storm shutters closed in a line (abandoned houses; blocks the opening)" if closed
             else "amado track and transom with the leaves stowed in the tobukuro (default, open)",
             datum="2-ken run along the veranda's outer groove line (z 0); y 0 = veranda floor",
             note="static, not doors: a run of 6-10 leaves would be 6-10 door bones (build list)")
    L = 2 * KEN
    if closed:
        amado_leaves(p, A, L - A)
    p.add(box(A - 0.06, L - A + 0.06, DOOR_H + 0.03, DOOR_H + 0.13, -0.05, 0.05, "wood_weathered", vis=(1, 2, 3),
              tag="head_rail"))
    p.add(box(A - 0.06, L - A + 0.06, DOOR_H + 0.13, DOOR_H + 0.40, -0.012, 0.0, "wood_weathered", vis=(1, 2),
              tag="transom_board"))
    p.add(box(A - 0.06, L - A + 0.06, DOOR_H + 0.40, DOOR_H + 0.45, -0.04, 0.03, "wood_weathered", vis=(1, 2),
              tag="transom_rail"))
    for x in (0.0, KEN, L):
        p.conn("post", (x, 0, 0), note="veranda outer posts")
    p.conn("sill", (0, 0, 0), note="outer groove of jp_p_porch_engawa")
    p.conn("head", (0, DOOR_H, 0))
    p.dim("leaf_m", "0.91 x 2.00", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % ((L - 2 * A) / 4, DOOR_H), ok=True)
    return p


def part_tobukuro(variant):
    p = Part("jp_p_open_tobukuro", variant, "open", tiers=[2, 3],
             used_for="board box holding the stowed amado at the end of a run" if variant == "_box"
             else "Morse's swinging shutter closet, shown swung clear of the veranda (P3)",
             datum="beside the end post of the amado run: x from the post face, z 0 = groove line, y 0 = veranda floor")
    iw, n = 0.91 + 0.05, 8
    dp = n * 0.03 + 0.05
    h = DOOR_H + 0.10 + 0.03
    x0, x1 = A, A + iw + 0.04
    z0, z1 = -dp / 2, dp / 2
    rng = rng_for("tobukuro" + variant)
    sol = []
    sol.append(box(x0, x1, 0.0, h, z0, z1, "wood_weathered", vis=(2, 3), geo=True, view=True, fire=True, tag="box"))
    sol += board_run(x0, x1, 0.0, h, z1 - 0.015, z1, rng, 0.18, 0.28, "wood_weathered", vis=(1,), tag="box_board")
    sol.append(box(x0, x1, 0.0, h, z0, z0 + 0.015, "wood_weathered", vis=(1,)))
    sol.append(box(x1 - 0.02, x1, 0.0, h, z0, z1, "wood_weathered", vis=(1,)))
    sol.append(box(x0 - 0.02, x1 + 0.03, h, h + 0.05, z0 - 0.03, z1 + 0.04, "wood_weathered", vis=(1, 2), tag="lid"))
    for yy in (0.4, 1.1, 1.8):
        sol.append(box(x0, x1, yy, yy + 0.06, z1, z1 + 0.018, "wood_weathered", vis=(1,), tag="batten"))
    if variant == "_swing":
        sol = [s.transformed(-90.0, (0, 0, 0)) for s in [s.finalize() for s in sol]]
        sol = [s.transformed(0.0, (A + dp / 2, 0.0, 0.05)) for s in sol]
        for s in sol:
            p.solids.append(s)
        p.add(box(A - 0.01, A + 0.02, 0.3, 0.45, 0.0, 0.05, "metal_iron", vis=(1,), tag="pivot"))
        p.add(box(A - 0.01, A + 0.02, 1.8, 1.95, 0.0, 0.05, "metal_iron", vis=(1,), tag="pivot"))
    else:
        p.extend(sol)
    p.conn("post", (0, 0, 0), note="outside the end post of the amado run")
    p.dim("inner_width_m", 0.96, iw)
    p.dim("depth_m (8 leaves)", round(dp, 3), dp)
    p.dim("height_m", 2.13, h, source="leaf + 0.10")
    return p


# ------------------------------------------------------------------------------------------------ kura door
def kura_surround(part, cx, clear_w, clear_h, face_z, steps=4, step=0.035, proj=0.16, border=0.30, mat="wall_shikkui"):
    """Stepped plaster door/window surround projecting from an okabe face; hole = clear at the wall, widening outward."""
    ow = clear_w + 2 * border
    oh_top = clear_h + border
    for k in range(steps):
        za, zb = face_z + k * proj / steps, face_z + (k + 1) * proj / steps
        hw = clear_w / 2 + k * step
        ht = clear_h + k * step
        for (a, b, c, d) in ((cx - ow / 2, cx - hw, 0.0, oh_top), (cx + hw, cx + ow / 2, 0.0, oh_top),
                             (cx - hw, cx + hw, ht, oh_top)):
            part.add(box(a, b, c, d, za, zb, mat, vis=(1, 2, 3) if k == 0 else (1, 2), geo=True, view=True, fire=True,
                         tag="surround"))
    return ow, oh_top, face_z + proj


def mini_pent(part, x0, x1, y_wall, z_wall, depth=0.60, t=0.40, brackets=True):
    """Small tiled pent (kura door / window): sheathing slab + a kawara course set + eave tiles."""
    y_edge = y_wall - depth * t
    part.add(prism([(y_wall, z_wall), (y_edge, z_wall + depth), (y_edge + 0.06, z_wall + depth), (y_wall + 0.06, z_wall)],
                   "x", x0, x1, {"default": "wood_weathered"}, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="pent"))
    # G3 fix: clay bed (fuki-tsuchi) between the pent slab and the tiles + a fascia board at the eave (PLAYBOOK §15 T1)
    part.add(prism([(y_wall + 0.06, z_wall), (y_edge + 0.06, z_wall + depth), (y_edge + 0.068, z_wall + depth),
                    (y_wall + 0.068, z_wall)], "x", x0, x1, "wall_arakabe", vis=(1, 2), tag="tile_bed"))
    part.add(prism([(y_edge - 0.01, z_wall + depth), (y_edge - 0.01, z_wall + depth + 0.03),
                    (y_edge + 0.08, z_wall + depth + 0.03), (y_edge + 0.08, z_wall + depth)], "x", x0, x1,
                   "wood_weathered", vis=(1, 2, 3), tag="kawara_fascia"))
    F = kawara.SlopeFrame((x0, y_edge + 0.06 + 0.012, z_wall + depth), (1.0, 0.0, 0.0), (0.0, 0.0, -1.0), t)
    rl = depth / F.cos
    kawara.eave_tiles(part, F, 0.0, x1 - x0, style="plain")
    kawara.field(part, F, 0.0, x1 - x0, kawara.EXPO, rl, rows_eave=1, rows_ridge=0)
    if brackets:
        for x in (x0 + 0.12, x1 - 0.12):
            part.add(box(x - 0.04, x + 0.04, y_edge - 0.16, y_edge + 0.02, z_wall, z_wall + depth - 0.08, "wood_weathered",
                         vis=(1, 2), tag="bracket"))


def part_kura_door(variant):
    hinged = variant == "_hinged"
    p = Part("jp_p_open_kura_door", variant, "open", tiers=[2, 3],
             used_for=("kura doorway with the thick plastered leaves as rotation doors (engine test, P2)" if hinged
                       else "kura doorway: stepped plaster surround, outer leaves static open, inner sliding door"),
             datum="1-ken bay of a 0.24 okabe wall (faces z +-0.12), centred at x 0.91; y 0 = approach level")
    th = 0.15                                  # raised stone threshold (hidden ramps both sides)
    cx, cw, ch = HALF, 1.24, DOOR_H + th       # 2.00 clear above the threshold; 1.24 wide so the open inner leaf keeps
    #                                            STUB in the opening and still clears 1.02 m (D1, G3 fix)
    fz = 0.12
    ow, oh, zf_out = kura_surround(p, cx, cw, ch, fz)
    p.add(box(cx - cw / 2 - 0.06, cx + cw / 2 + 0.06, -0.10, th, -0.12, zf_out, "stone_cut", vis=(1, 2, 3), geo=True,
              view=False, fire=True, tag="threshold"))
    p.road([(cx - cw / 2, th, -0.12), (cx + cw / 2, th, -0.12), (cx + cw / 2, th, zf_out), (cx - cw / 2, th, zf_out)],
           "stone_ext")
    for (za, zb) in ((zf_out, zf_out + 0.26), (-0.12, -0.38)):
        poly = [(za, th), (zb, 0.0), (za, 0.0)]
        if (zb - za) * 1 < 0:
            poly = [(za, th), (za, 0.0), (zb, 0.0)]
        s = prism([(y, z) for z, y in poly], "x", cx - cw / 2, cx + cw / 2, "stone_cut", vis=(), geo=True, tag="ramp")
        p.add(s)
        p.road([(cx - cw / 2, th, za), (cx + cw / 2, th, za), (cx + cw / 2, 0.0, zb), (cx - cw / 2, 0.0, zb)], "stone_ext")
    # inner sliding door (the game door), on the interior face, parks over the next bay inside
    rng = rng_for("kura_inner")

    def inner(l0, l1, bot, top, z0, z1, bone, dirn=+1):
        out = [box(l0, l1, bot, top, z0, z1, "wood_weathered", vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
        out += board_run(l0, l1, bot, bot + 1.0, z0, z1, rng, 0.2, 0.28, "wood_weathered", vis=(1,), tag="leaf_board",
                         gap=LEAF_GAP)
        out.append(box(l0, l1, bot + 1.0, top, z0, z0 + 0.012, "wood_weathered", vis=(1,), tag="leaf_back"))
        for k in range(12):
            x = l0 + 0.05 + k * (l1 - l0 - 0.1) / 11
            out.append(box(x - 0.018, x + 0.018, bot + 1.0, top, z0 + 0.012, z1, "wood_weathered", vis=(1,), tag="bar"))
        for (a, b) in ((l0, l0 + 0.05), (l1 - 0.05, l1)):
            out.append(box(a, b, bot, top, z0, z1 + 0.004, "wood_weathered", vis=(1,), tag="stile"))
        out.append(box(l0, l1, top - 0.05, top, z0, z1 + 0.004, "wood_weathered", vis=(1,)))
        px0, px1 = pull_x(l0, l1, dirn, w=0.10)
        out.append(box(px0, px1, bot + 0.95, bot + 1.10, z0 - 0.012, z0, "metal_iron", vis=(1,), tag="pull"))
        return out
    sliding_leaf(p, cx - cw / 2, cx + cw / 2, th, DOOR_H, -0.12, -1, +1, None, thick=0.04, kind="plank",
                 build=inner, park_span=(cx - cw / 2 - OV, KEN + KEN), note="inner sliding door (game door)")
    tracks(p, cx - cw / 2, cx + cw / 2 + cw + 0.2, -0.12, -1, 0.04, head_y=th + DOOR_H)
    # outer leaves: 0.16 thick plastered, stepped edge
    lw = cw / 2 + 4 * 0.035 + 0.03 - 0.002     # the two leaves meet at the centre (they overlapped 8 cm: G3 sweep check)
    lh = ch + 0.14 + 0.04 - th
    hinges = [(cx - cw / 2 - 4 * 0.035 - 0.03, -1), (cx + cw / 2 + 4 * 0.035 + 0.03, +1)]
    for hx, sg in hinges:
        def leaf_solids(closed):
            out = []
            if closed:
                x0, x1 = (hx, hx - sg * lw) if sg < 0 else (hx - lw, hx)
                x0, x1 = min(hx, hx - sg * lw), max(hx, hx - sg * lw)
                out.append(box(x0, x1, 0.0 + th, th + lh, zf_out, zf_out + 0.16, "wall_shikkui", vis=(1, 2, 3),
                               geo=True, view=True, fire=True, tag="kura_leaf"))
                out.append(box(x0 + 0.04, x1 - 0.04, th + 0.04, th + lh - 0.04, zf_out + 0.16, zf_out + 0.19,
                               "wall_shikkui", vis=(1,), tag="kura_leaf_step"))
            else:
                # static open ~100 degrees: the leaf stands out from the surround edge
                z0 = zf_out
                xa = hx + sg * 0.0
                out.append(box(min(xa, xa + sg * 0.16), max(xa, xa + sg * 0.16), th, th + lh, z0, z0 + lw, "wall_shikkui",
                               vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kura_leaf"))
                out.append(box(min(xa + sg * 0.16, xa + sg * 0.19), max(xa + sg * 0.16, xa + sg * 0.19), th + 0.04,
                               th + lh - 0.04, z0 + 0.04, z0 + lw - 0.04, "wall_shikkui", vis=(1,), tag="kura_leaf_step"))
            return out
        if hinged:
            bone = p.next_bone()
            for s in leaf_solids(True):
                s.door = bone
                p.add(s)
            # model.cfg rotation: +angle turns by the RIGHT-hand rule about axis point 1 -> 2 (vanilla vehicle doors,
            # G3 research, PLAYBOOK §15): these axes swing both plaster leaves OUT, away from the wall
            axis = [(hx, th + lh, zf_out), (hx, th, zf_out)] if sg < 0 else [(hx, th, zf_out), (hx, th + lh, zf_out)]
            ang = math.radians(90)          # 100 swung the leaf back into the stepped surround (G3 sweep check)
            centre = (hx - sg * lw / 2, th + lh / 2, zf_out + 0.08)
            p.memory[bone + "_axis"] = axis
            p.memory[bone + "_action"] = [(cx, 1.0 + th, zf_out)]
            p.memory[bone] = [centre]
            p.doors.append(Door(kind="kura", anims=[{"bone": bone, "type": "rotation", "axis": axis, "amount": ang}],
                                action=(cx, 1.0 + th, zf_out), centre=centre, anim_period=2.0, init_opened=1.0,
                                sound="doorWoodSlide", display="kura door", note="outer plaster leaf (rotation)",
                                engine_tested=False, passable=False, has_view=True, act_h=1.0 + th,
                                reach_sides=("leaf",), style="kura_hinged"))
        else:
            p.extend(leaf_solids(False))
        for yy in (th + 0.35, th + lh - 0.45):
            p.add(box(hx - 0.05, hx + 0.05, yy, yy + 0.12, zf_out - 0.01, zf_out + 0.02, "metal_iron", vis=(1,),
                      tag="hinge"))
    mini_pent(p, cx - ow / 2 - 0.05, cx + ow / 2 + 0.05, oh + 0.45, zf_out)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), hidden=True, note="okabe: posts hidden in the wall")
    p.conn("sill", (0, 0, 0), note="raised stone threshold 0.15 with hidden ramps")
    p.conn("park", (KEN, 0, 0), length=KEN, face="interior")
    p.dim("clear_m", ">=1.00 x 2.00", 0.0, source="build_list / D1")
    p.dims[-1].update(measured="%.2f x %.2f" % (cw - STUB, ch - th), ok=cw - STUB >= 1.0 and ch - th >= 2.0 - 1e-6)
    p.dim("leaf_thickness_m", "0.15-0.20", 0.16)
    p.dim("jamb_steps", "3-5", 4, tol=0)
    p.dim("door_pent_m", 0.60, 0.60)
    p.notes.append("Opening 1.24 x 2.15 from the approach level = 2.00 clear above the 0.15 threshold (1.02 clear once "
                   "the open inner leaf keeps its 0.22 stub); the okabe wall recipe must leave that hole "
                   "(walls.wall_run(kind='okabe', openings=[(0.29, 1.53, 0, 2.15)])).")
    return p


def part_kura_window(variant):
    p = Part("jp_p_open_kura_window", variant, "open", tiers=[2, 3],
             used_for="kura window with iron bars, sliding plaster shutter and a tiny tile pent" if variant == "_slide"
             else "kura window with a pair of hinged plaster shutters (static open)",
             datum="half-ken bay of a 0.24 okabe wall, opening centred at x 0.455, sill at 1.20; y 0 = kura floor")
    cx, w, h, sill = QK_, 0.60, 0.75, 1.20
    fz = 0.12
    # surround (2 steps) sits around the 0.60 x 0.75 hole
    for k in range(2):
        za, zb = fz + k * 0.05, fz + (k + 1) * 0.05
        hw, hh = w / 2 + k * 0.03, h / 2 + k * 0.03
        cy = sill + h / 2
        for (a, b, c, d) in ((cx - w / 2 - 0.20, cx - hw, sill - 0.20, sill + h + 0.20),
                             (cx + hw, cx + w / 2 + 0.20, sill - 0.20, sill + h + 0.20),
                             (cx - hw, cx + hw, cy + hh, sill + h + 0.20), (cx - hw, cx + hw, sill - 0.20, cy - hh)):
            p.add(box(a, b, c, d, za, zb, "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="surround"))
    for k in range(6):
        x = cx - w / 2 + (k + 0.5) * w / 6
        p.add(box(x - 0.015, x + 0.015, sill, sill + h, -0.015, 0.015, "metal_iron", vis=(1, 2), tag="bar"))
    p.add(box(cx - w / 2, cx + w / 2, sill, sill + h, -0.015, 0.015, "metal_iron", vis=(), geo=True, tag="bars_geo"))
    zo = fz + 0.10
    if variant == "_slide":
        p.add(box(cx - w / 2 + 0.30, cx + w / 2 + 0.36, sill - 0.04, sill + h + 0.04, zo, zo + 0.12, "wall_shikkui",
                  vis=(1, 2, 3), geo=True, view=True, fire=True, tag="shutter"))
        p.add(box(cx - w / 2 - 0.05, cx + w + 0.45, sill + h + 0.04, sill + h + 0.10, zo, zo + 0.13, "wall_shikkui",
                  vis=(1, 2), tag="shutter_track"))
        p.add(box(cx - w / 2 - 0.05, cx + w + 0.45, sill - 0.10, sill - 0.04, zo, zo + 0.13, "wall_shikkui",
                  vis=(1, 2), tag="shutter_track"))
    else:
        for sg in (-1, 1):
            hx = cx + sg * (w / 2 + 0.06)
            p.add(box(min(hx, hx + sg * 0.12), max(hx, hx + sg * 0.12), sill - 0.03, sill + h + 0.03, zo, zo + w / 2 + 0.06,
                      "wall_shikkui", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="shutter"))
    mini_pent(p, cx - w / 2 - 0.30, cx + w / 2 + 0.30, sill + h + 0.42, fz + 0.10, depth=0.35, brackets=False)
    p.conn("post", (0, 0, 0), hidden=True)
    p.conn("post", (HALF, 0, 0), hidden=True)
    p.dim("opening_m", "0.60 x 0.75", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (w, h), ok=True)
    p.dim("bars_m", "0.03 at 0.09", 0.0)
    p.dims[-1].update(measured="0.03 at %.3f" % (w / 6), ok=abs(w / 6 - 0.09) < 0.02)
    p.dim("shutter_thickness_m", 0.12, 0.12)
    return p


QK_ = HALF / 2


# ------------------------------------------------------------------------------------------------ mushiko
def stadium_panel(part, x0, x1, y0, y1, t, holes, mat="wall_shikkui", slat=0.045, gap=0.045):
    """Plaster panel with stadium (round-ended) holes [(cx, cy, w, h)], slatted with plastered vertical slats.
    Each plaster piece is a convex prism; one geometry box for the whole panel."""
    z0, z1 = -t / 2, t / 2
    part.add(box(x0, x1, y0, y1, z0, z1, mat, vis=(), geo=True, view=False, fire=True, tag="panel_geo"))
    xs = [x0]
    for (cx, cy, w, h) in sorted(holes):
        xs += [cx - w / 2, cx + w / 2]
    xs.append(x1)
    # vertical strips between holes (full height)
    for i in range(0, len(xs), 2):
        if xs[i + 1] - xs[i] > 1e-4:
            part.add(box(xs[i], xs[i + 1], y0, y1, z0, z1, mat, vis=(1, 2, 3), view=True, tag="panel"))
    for (cx, cy, w, h) in holes:
        r = h / 2
        a, b = cx - w / 2, cx + w / 2
        part.add(box(a, b, y0, cy - r, z0, z1, mat, vis=(1, 2, 3), view=True, tag="panel"))
        part.add(box(a, b, cy + r, y1, z0, z1, mat, vis=(1, 2, 3), view=True, tag="panel"))
        n = 6
        for side in (-1, 1):
            xe = a if side < 0 else b
            xc = a + r if side < 0 else b - r
            for q in (-1, 1):                      # lower / upper quarter
                for k in range(n):
                    th0 = math.pi / 2 * k / n
                    th1 = math.pi / 2 * (k + 1) / n
                    p0 = (xc + side * r * math.cos(th0), cy + q * r * math.sin(th0))
                    p1 = (xc + side * r * math.cos(th1), cy + q * r * math.sin(th1))
                    poly = [(xe, p0[1]), p0, p1, (xe, p1[1])]
                    area = sum(poly[i][0] * poly[(i + 1) % 4][1] - poly[(i + 1) % 4][0] * poly[i][1] for i in range(4))
                    if abs(area) < 1e-7:
                        continue
                    if area < 0:
                        poly = poly[::-1]
                    from .shapes import clean_poly
                    poly = clean_poly(poly)
                    if len(poly) >= 3:
                        part.add(prism(poly, "z", z0, z1, mat, vis=(1, 2), tag="panel_arc"))
        # slats (plastered) across the hole
        x = a + gap / 2
        while x + slat < b - 0.01:
            xm = x + slat / 2
            dx = max(0.0, max(a + r - xm, xm - (b - r)))
            hh = math.sqrt(max(0.0, r * r - dx * dx)) if dx > 0 else r
            if hh > 0.03:
                part.add(box(x, x + slat, cy - hh, cy + hh, -0.03, 0.03, mat, vis=(1, 2), tag="slat"))
            x += slat + gap
        part.add(box(a + r * 0.3, b - r * 0.3, cy - r * 0.9, cy + r * 0.9, -0.03, 0.03, "wood_sooted", vis=(3,),
                     tag="hole_lod"))


def part_mushiko(variant):
    pair = variant == "_oval_pair"
    p = Part("jp_p_open_mushiko", variant, "open", tiers=[3],
             used_for=("two small oval mushiko in one 1-ken bay of the low upper street wall (1730 form)" if pair
                       else "single small oval mushiko on the low upper street wall of Kamigata machiya (1730 form)"),
             deviation="oval pair: each oval 0.70 x 0.40 so two fit one 1-ken bay (build list single oval 0.90 x 0.45)"
             if pair else None,
             datum="1-ken bay of the upper plastered front (0.15 thick, hidden posts); y 0 = upper floor, wall to 1.30")
    H = 1.30
    if pair:
        holes = [(HALF / 2 + 0.02, 0.40 + 0.20, 0.70, 0.40), (HALF + HALF / 2 - 0.02, 0.40 + 0.20, 0.70, 0.40)]
    else:
        holes = [(HALF, 0.40 + 0.225, 0.90, 0.45)]
    stadium_panel(p, 0.0, KEN, 0.0, H, 0.15, holes)
    p.conn("post", (0, 0, 0), hidden=True)
    p.conn("post", (KEN, 0, 0), hidden=True)
    p.conn("floor", (0, 0, 0), note="upper floor level; street wall above it <= 1.30 (D3)")
    w, h = holes[0][2], holes[0][3]
    p.dim("opening_m", "0.90 x 0.45" if not pair else "0.70 x 0.40 (pair)", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (w, h), ok=True)
    p.dim("slat_face_m", 0.045, 0.045)
    p.dim("depth_m", 0.15, 0.15)
    p.dim("sill_above_upper_floor_m", 0.40, holes[0][1] - h / 2)
    return p


# ------------------------------------------------------------------------------------------------ koshi lattice
def koshi(part, x0, x1, variant, y0=0.45, y1=DOOR_H, z=0.0, paper=True):
    mat = "wood_bengara" if variant == "_bengara" else "wood_street_dark"
    zb = z + 0.05                      # bars stand proud of the frame line on the street side
    part.add(box(x0, x1, y0 - 0.06, y0, z - 0.03, zb + 0.03, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                 tag="koshi_sill"))
    part.add(box(x0, x1, y1 - 0.06, y1, z - 0.03, zb + 0.02, mat, vis=(1, 2, 3), tag="koshi_head"))
    part.add(box(x0, x1, y0, y1 - 0.06, z - 0.03, zb, mat, vis=(), geo=True, view=True, fire=True, tag="koshi_geo"))
    # paper of the static shoji behind (paper=False: an openable panel behind the lattice replaces it)
    if paper:
        part.add(box(x0, x1, y0, y1 - 0.06, z - 0.03, z - 0.027, "paper_shoji", vis=(1, 2, 3), tag="koshi_paper"))
    part.add(box(x0, x1, y0, y1 - 0.06, z - 0.027, zb, mat, vis=(3,), tag="koshi_lod", uv="fit"))
    if variant == "_komeya":
        face, cc = 0.06, 0.12
    else:
        face, cc = 0.03, 0.06
    n = max(2, int(round((x1 - x0) / cc)))
    ytop = y1 - 0.06
    for k in range(n):
        x = x0 + (k + 0.5) * (x1 - x0) / n
        top = ytop
        if variant == "_oyako" and k % 4:
            top = ytop - 0.30
        vis = (1, 2) if k % 2 == 0 else (1,)
        part.add(box(x - face / 2, x + face / 2, y0, top, z, zb, mat, vis=vis, tag="koshi_bar"))
    rails = [y0 + (ytop - y0) * f for f in ((0.35, 0.7) if variant != "_komeya" else (0.5,))]
    if variant == "_oyako":
        rails = [ytop - 0.30]
    for yy in rails:
        part.add(box(x0, x1, yy - 0.012, yy + 0.012, z - 0.012, z, mat, vis=(1,), tag="koshi_rail"))


def part_koshi(variant):
    used = {"_kyo": "fine-bar Kyoto lattice front / window", "_oyako": "parent bars + cut-top children (cloth, thread)",
            "_komeya": "thick bars for rice and charcoal shops (T2)", "_degoshi": "projecting lattice on its own sill (T3)",
            "_bengara": "bengara-red fine lattice (Kamigata, sparingly; restricted colour)"}[variant]
    p = Part("jp_p_open_koshi", variant, "open", tiers=[2] if variant == "_komeya" else [3], used_for=used,
             recipe="openings.koshi(part, x0, x1, variant) for 0.5 / 1 / 1.5 / 2-ken modules",
             datum="1-ken module between post faces; y 0 = sill level of the wall (lattice sill 0.45, head 2.00)")
    if variant == "_degoshi":
        pz = 0.30
        koshi(p, A + 0.02, B - 0.02, "_kyo", z=pz)
        for x in (A, B):
            p.add(box(x - 0.02 if x == A else x - 0.04, x + 0.04 if x == A else x + 0.02, 0.45 - 0.06, DOOR_H - 0.06,
                      0.0, pz + 0.08, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True, fire=True, tag="degoshi_side"))
            n = 5
            for k in range(n):
                zz = 0.03 + k * (pz - 0.02) / n
                p.add(box(x - 0.01, x + 0.01, 0.45, DOOR_H - 0.12, zz, zz + 0.03, "wood_street_dark", vis=(1,),
                          tag="side_bar"))
        # G3 fix (C11 envelope leak, Stephen: "from inside I can see outside"): the head board closes the whole
        # opening head - it runs up to the wall's head rail (2.00) and back to the wall's inner face, so no slit is
        # left between the lattice box and the wall above at standing eye height
        p.add(box(A - 0.04, B + 0.04, DOOR_H - 0.06, DOOR_H, -POST / 2, pz + 0.12, "wood_street_dark", vis=(1, 2, 3),
                  geo=True, view=True, fire=True, tag="degoshi_top"))
        p.add(box(A - 0.04, B + 0.04, 0.33, 0.39, 0.0, pz + 0.12, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True,
                  fire=True, tag="degoshi_sill"))
        p.dim("degoshi_projection_m", 0.30, pz)
    else:
        koshi(p, A, B, variant)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0.45, 0), note="own sill rail on the koshi-ita / plinth")
    p.conn("head", (0, DOOR_H, 0))
    p.dim("bar_face_m", 0.06 if variant == "_komeya" else 0.03, 0.06 if variant == "_komeya" else 0.03)
    p.dim("module_width_ken", "0.5 / 1 / 1.5 / 2", 1.0)
    return p


# ------------------------------------------------------------------------------------------------ renji
def part_renji(variant):
    p = Part("jp_p_open_renji", variant, "open", tiers={"_bamboo": [1], "_wood": [2], "_muso": [2]}[variant],
             used_for={"_bamboo": "bamboo-barred window with a sliding board shutter (farmhouses, T1)",
                       "_wood": "square wood-barred window with a sliding board shutter (T2)",
                       "_muso": "double slatted kitchen window, one panel slides (date unverified)"}[variant],
             datum="half-ken bay between post nodes x 0 and 0.91; sill 0.90, opening 0.75 high; y 0 = floor")
    a, b = A, HALF - POST / 2
    s0, s1 = 0.90, 1.65
    fm = "wood_weathered"
    p.add(box(a, b, s0 - 0.05, s0, -0.07, 0.07, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="sill"))
    p.add(box(a, b, s1, s1 + 0.05, -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head"))
    p.add(box(a, b, s0, s1, -0.01, 0.01, fm, vis=(), geo=True, tag="bars_geo"))
    if variant == "_muso":
        for zz, off in ((0.01, 0.0), (-0.02, 0.045)):
            x = a + off
            while x + 0.045 <= b + 1e-6:
                p.add(box(x, x + 0.045, s0, s1, zz, zz + 0.018, fm, vis=(1, 2), tag="slat"))
                x += 0.09
    else:
        n = int((b - a) / 0.08)
        for k in range(n):
            x = a + (k + 0.5) * (b - a) / n
            if variant == "_bamboo":
                p.add(tube((x, s0, 0.0), (x, s1, 0.0), 0.014, "bamboo_weathered", n=6, vis=(1, 2), tag="bar"))
            else:
                p.add(box(x - 0.015, x + 0.015, s0, s1, -0.015, 0.015, fm, vis=(1, 2), tag="bar"))
        # board shutter inside, half open (static), sliding inside the wall line
        p.add(box((a + b) / 2, b + 0.35, s0 - 0.02, s1 + 0.02, -0.075, -0.06, fm, vis=(1, 2), tag="shutter"))
        p.add(box(a - 0.02, b + 0.40, s1 + 0.02, s1 + 0.06, -0.09, -0.055, fm, vis=(1,), tag="shutter_track"))
    for x in (0.0, HALF):
        p.conn("post", (x, 0, 0))
    p.dim("opening_m", "0.91 bay x 0.60-0.90", 0.0)
    p.dims[-1].update(measured="%.2f bay (%.2f clear) x %.2f" % (HALF, b - a, s1 - s0), ok=True)
    p.dim("sill_m", 0.9, s0)
    return p


# ------------------------------------------------------------------------------------------------ suriagedo
def part_suriagedo(variant):
    p = Part("jp_p_open_suriagedo", variant, "open", tiers=[2, 3],
             used_for={"_closed": "shop front closed at night by 3 stacked boards in the post grooves (static)",
                       "_part": "shop front with one board left in the grooves (static)",
                       "_door": "animated: the 3 boards rise into the box behind the beam (one door, 3 bones; "
                                "engine test)"}[variant],
             datum="1-ken bay between post nodes; boards in grooves in the wall plane; box above 2.00 inside")
    bh = DOOR_H / 3
    fm = "wood_street_dark"
    rng = rng_for("suriage" + variant)
    zs = [0.03, 0.0, -0.03] if variant == "_door" else [0.0, 0.0, 0.0]
    boards = []
    for k in range(3):                         # k = 0 bottom .. 2 top
        y0, y1 = k * bh + 0.004, (k + 1) * bh
        boards.append((y0, y1, zs[k]))
    # storage box above the head, hollow (front and back boards + top) so the boards can rise into it
    p.add(box(A, B, DOOR_H, WALL_H, 0.045, 0.06, "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="box"))
    p.add(box(A, B, DOOR_H, WALL_H, -0.06, -0.045, "wood_weathered", vis=(1, 2, 3), geo=True, view=True, fire=True,
              tag="box"))
    p.add(box(A, B, WALL_H - 0.02, WALL_H, -0.045, 0.045, "wood_weathered", vis=(1, 2), geo=True, view=True, fire=True,
              tag="box"))
    for x in (A + 0.3, B - 0.3):
        p.add(box(x - 0.03, x + 0.03, DOOR_H + 0.1, WALL_H - 0.1, 0.06, 0.075, "wood_weathered", vis=(1,), tag="batten"))
    threshold(p, A, B)

    def board_solids(y0, y1, z, bone=None):
        t = 0.024
        # collision stops at the post faces; the visual board runs 12 mm into the post grooves
        out = [box(A + 0.002, B - 0.002, y0, y1, z - t / 2, z + t / 2, fm, vis=(), geo=True, view=True, fire=True,
                   tag="suriage_board_geo"),
               box(A - 0.012, B + 0.012, y0, y1, z - t / 2, z + t / 2, fm, vis=(2, 3), tag="suriage_board")]
        out += board_run(A - 0.012, B + 0.012, y0, y1, z - t / 2 + 0.004, z + t / 2, rng, 0.25, 0.4, fm, vertical=False,
                         vis=(1,), tag="suriage_plank")
        out.append(box(A + 0.1, B - 0.1, y1 - 0.08, y1 - 0.03, z + t / 2, z + t / 2 + 0.012, fm, vis=(1,), tag="cleat"))
        out.append(box((A + B) / 2 - 0.08, (A + B) / 2 + 0.08, y0 + 0.25, y0 + 0.33, z + t / 2, z + t / 2 + 0.02,
                       "metal_iron", vis=(1,), tag="grip"))
        for s in out:
            s.door = bone
        return out
    if variant == "_closed":
        for (y0, y1, z) in boards:
            p.extend(board_solids(y0, y1, z))
    elif variant == "_part":
        p.extend(board_solids(*boards[0]))
    else:
        anims = []
        for k, (y0, y1, z) in enumerate(boards):
            bone = "doors%d" % (k + 1)
            p.extend(board_solids(y0, y1, z, bone))
            amt = DOOR_H - y0 + 0.004 - STUB      # the bottom board keeps STUB in the opening (aimable, G3 fix)
            c = ((A + B) / 2, (y0 + y1) / 2, z)
            axis = [c, (c[0], c[1] + 1.0, c[2])]
            p.memory[bone + "_axis"] = axis
            p.memory[bone] = [c]
            anims.append({"bone": bone, "type": "translation", "axis": axis, "amount": amt})
        act = ((A + B) / 2, 1.0, 0.0)
        p.memory["doors1_action"] = [act]
        d = Door(kind="plank", anims=anims, action=act, centre=((A + B) / 2, 1.0, 0.0), anim_period=1.6, init_opened=1.0,
                 display="shop shutters", note="3 boards on one source; vertical translation (engine test); open, the "
                 "bottom board hangs STUB below the head (vanilla rule), so it is a shop window, not a walk-through",
                 engine_tested=False, opening=(A, B, 0.0, DOOR_H), z_face=0.0, passable=False, act_h=1.0,
                 style="suriage", stub=STUB)
        p.doors.append(d)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), note="grooved post (0.03 grooves)")
    p.conn("head", (0, DOOR_H, 0), note="stack top under the 2.00 beam; box above it")
    p.dim("boards", 3, 3, tol=0)
    p.dim("board_height_m", 0.68, bh, tol=0.02, source="build_list ~0.68 (2.04/3); here 2.00/3")
    return p


def part_shitomido(variant):
    up = variant == "_up"
    p = Part("jp_p_open_shitomido", variant, "open", tiers=[3],
             used_for="Kamigata shop shutter: upper panel hooked up under the pent, lower lifted out (static)" if up
             else "shitomido closed: upper panel down, lower panel in place (static)",
             datum="1-ken bay between post faces; hinge at the 2.00 head rail")
    fm = "wood_street_dark"
    rng = rng_for("shitomi" + variant)

    def panel(x0, x1, y0, y1, z0, z1, horiz=False):
        if horiz:
            p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="shitomi"))
            n = int((x1 - x0) / 0.12)
            for k in range(n + 1):
                x = x0 + k * (x1 - x0) / n
                p.add(box(x - 0.015, x + 0.015, y0 - 0.02, y0, z0, z1, fm, vis=(1,), tag="shitomi_bar"))
            for zz in (z0 + 0.3, z0 + 0.7):
                p.add(box(x0, x1, y0 - 0.02, y0, zz - 0.015, zz + 0.015, fm, vis=(1,), tag="shitomi_bar"))
            p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(1,), tag="shitomi_board"))
        else:
            p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="shitomi"))
            p.add(box(x0, x1, y0, y1, z0, z1 - 0.02, fm, vis=(1,), tag="shitomi_board"))
            n = int((x1 - x0) / 0.12)
            for k in range(n + 1):
                x = x0 + k * (x1 - x0) / n
                p.add(box(x - 0.015, x + 0.015, y0, y1, z1 - 0.02, z1, fm, vis=(1,), tag="shitomi_bar"))
            yy = y0 + 0.05
            while yy < y1:
                p.add(box(x0, x1, yy, yy + 0.03, z1 - 0.02, z1, fm, vis=(1,), tag="shitomi_bar"))
                yy += 0.30
    if up:
        panel(A, B, DOOR_H + 0.02, DOOR_H + 0.08, 0.07, 0.07 + 1.10, horiz=True)
        for x in (A + 0.15, B - 0.15):
            p.add(box(x - 0.006, x + 0.006, DOOR_H + 0.08, DOOR_H + 0.55, 1.05, 1.062, "metal_iron", vis=(1,), tag="hook"))
    else:
        panel(A, B, 0.9, DOOR_H, 0.06, 0.12)
        panel(A, B, 0.1, 0.9, 0.06, 0.12)
    p.add(box(A, B, DOOR_H, DOOR_H + 0.03, 0.06, 0.10, "metal_iron", vis=(1,), tag="hinge_bar"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("head", (0, DOOR_H, 0), note="hinge at the head rail")
    p.dim("upper_panel_m", 1.10, 1.10)
    p.dim("lower_panel_m", 0.80, 0.80)
    return p


def part_battari(variant):
    down = variant == "_down"
    p = Part("jp_p_open_battari", variant, "open", tiers=[2, 3],
             used_for="fold-down shop bench, down by day (walkable seat)" if down else "fold-down bench folded up at night",
             datum="between the post faces of a 1-ken bay on the street face; y 0 = street / sill level")
    fm = "wood_street_dark"
    rng = rng_for("battari" + variant)
    seat = 0.42
    if down:
        p.add(box(A, B, seat - 0.035, seat, 0.07, 0.57, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="seat"))
        p.extend(board_run(A, B, seat - 0.035, seat, 0.07, 0.57, rng, 0.15, 0.2, fm, vertical=False, vis=(1,),
                           tag="seat_board") if False else [])
        n = 4
        for k in range(n):
            z0 = 0.07 + k * 0.125
            p.add(box(A, B, seat - 0.035, seat, z0 + 0.004, z0 + 0.121, fm, vis=(1,), tag="seat_board",
                      uvoff=(rng.random(), rng.random())))
        for x in (A + 0.1, B - 0.14):
            p.add(box(x, x + 0.04, 0.0, seat - 0.035, 0.49, 0.53, fm, vis=(1, 2), geo=True, view=False, fire=True,
                      tag="leg"))
        p.road([(A, seat, 0.07), (B, seat, 0.07), (B, seat, 0.57), (A, seat, 0.57)], "boards_ext")
    else:
        p.add(box(A, B, seat, seat + 0.50, 0.07, 0.105, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="seat"))
        for x in (A + 0.1, B - 0.14):
            p.add(box(x, x + 0.04, seat + 0.05, seat + 0.45, 0.105, 0.125, fm, vis=(1,), tag="leg"))
    p.add(box(A, B, seat - 0.05, seat - 0.02, 0.06, 0.08, "metal_iron", vis=(1,), tag="hinge"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.dim("size_m", "1.82 x 0.50", 0.0)
    p.dims[-1].update(measured="%.2f (between post faces) x 0.50" % (B - A), ok=True)
    p.dim("seat_m", 0.42, seat)
    return p


def part_upper_rail(variant):
    p = Part("jp_p_open_upper_rail", variant, "open", tiers=[2, 3],
             used_for="low plain rail along an inn / tea-house upper opening; 1.00 m invisible blocker",
             datum="1-ken run between upper-floor posts; y 0 = upper floor")
    fm = "wood_weathered"
    p.add(box(A, B, 0.56, 0.60, -0.025, 0.025, fm, vis=(1, 2, 3), tag="top_rail"))
    p.add(box(A, B, 0.03, 0.07, -0.02, 0.02, fm, vis=(1, 2), tag="bottom_rail"))
    x = A + 0.06
    while x < B - 0.03:
        p.add(box(x - 0.015, x + 0.015, 0.07, 0.56, -0.015, 0.015, fm, vis=(1,), tag="baluster"))
        x += 0.12
    p.add(box(A, B, 0.0, 1.00, -0.02, 0.02, fm, vis=(), geo=True, tag="blocker"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("floor", (0, 0, 0), note="upper floor level")
    p.dim("rail_height_m", 0.60, 0.60)
    p.dim("baluster_m", "0.03 at 0.12", 0.0)
    p.dims[-1].update(measured="0.03 at 0.12", ok=True)
    p.dim("geometry_blocker_m", 1.00, 1.00)
    return p


def part_mushiro(variant):
    p = Part("jp_p_open_mushiro", variant, "open", tiers=[1],
             used_for="straw mat doorway of the poorest houses, rolled up (no collision)",
             datum="hangs from the head rail of an open 1-ken bay; y 0 = floor")
    y = DOOR_H - 0.12
    p.add(tube((A + 0.03, y, 0.10), (B - 0.03, y, 0.10), 0.075, "straw_mushiro", n=10, vis=(1, 2, 3), tag="roll"))
    for x in (A + 0.25, B - 0.25):
        p.add(box(x - 0.012, x + 0.012, y - 0.08, DOOR_H + 0.02, 0.02, 0.19, "straw_mushiro", vis=(1,), tag="tie"))
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("head", (0, DOOR_H, 0))
    p.dim("roll_m", "d 0.15 x 0.91-1.82", 0.0)
    p.dims[-1].update(measured="d 0.15 x %.2f" % (B - A - 0.06), ok=True)
    return p


# ------------------------------------------------------------------------------------------------ openable windows
# G3 fix pass (Stephen 2026-09-27: "as long as there's a few somewhere, in correct spots"). Animated exactly like the
# doors (config class DoorsTwinN, bones doorsN, memory <bone>_axis / <bone> / doorstwinN_action, doorWoodSlide sound);
# not passable. Where each type belongs: PLAYBOOK §15.
def part_window_slide(variant):
    """Half-ken window: a fixed lattice outside (koshi _kyo, no paper / renji bars) and ONE sliding panel on the inside
    face (shoji or board) that parks over the next half-ken inside and keeps STUB in the opening. Operated from inside
    (the lattice's View Geometry covers it from outside, as in a real house)."""
    shoji = variant == "_shoji"
    p = Part("jp_p_open_window_slide", variant, "open", tiers=[2, 3] if shoji else [1, 2, 3],
             used_for=("half-ken street / room window: fine koshi lattice outside, a sliding shoji panel inside "
                       "(T2-3 town fronts and rooms)" if shoji else
                       "half-ken kitchen / work window: wooden renji bars outside, a sliding board shutter inside "
                       "(T1-3 kitchens, stables, workshops)"),
             datum="half-ken bay between post nodes x=0 and x=0.91 + the next half-ken (0.91..1.82) as the inside park "
                   "bay; y 0 = floor; opening %s" % ("0.45-2.00 (koshi window)" if shoji else "0.90-1.65 (renji)"))
    a, b = A, HALF - POST / 2
    s0, s1 = (0.45, DOOR_H) if shoji else (0.90, 1.65)
    fm = "wood_weathered"
    if shoji:
        koshi(p, a, b, "_kyo", y0=s0, y1=s1, paper=False)
        build = leaf_shoji(0.05)
        thick, kind = 0.03, "shoji"
    else:
        p.add(box(a, b, s0 - 0.05, s0, -0.07, 0.07, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="sill"))
        p.add(box(a, b, s1, s1 + 0.05, -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head"))
        p.add(box(a, b, s0, s1, -0.01, 0.01, fm, vis=(), geo=True, tag="bars_geo"))     # Geometry only: rays pass
        n = int((b - a) / 0.08)
        for k in range(n):
            x = a + (k + 0.5) * (b - a) / n
            p.add(box(x - 0.015, x + 0.015, s0, s1, -0.015, 0.015, fm, vis=(1, 2), tag="bar"))
        p.add(box(a, b, s0, s1, -0.012, 0.012, fm, vis=(3,), tag="bars_lod"))
        build = leaf_plank("plain", "wood_weathered", rng_for("window_slide" + variant))
        thick, kind = 0.025, "plank"
    zf = -POST / 2
    tr = zf - (GAP + thick / 2)
    l0, l1 = a - OV, b + OV
    slide = (b - STUB) - l0
    height = s1 - s0 - 0.03
    anims = _leaf_set(p, [(l0, l1, tr, +1, slide, "window panel")], s0, height, thick, build, None, kind)
    d = _twin_door(p, anims, a, b, s0, height, zf, -1, kind, "sliding window panel, inside face", tr, thick, tr,
                   (l0, l1 + slide), "window_slide", STUB, window=True)
    d.reach_sides = ("leaf",)
    d.display = "window"
    d.anim_period, d.init_opened = 0.6, 0.4
    if d.sweep[1] > KEN - POST / 2 + 1e-3:
        raise ValueError("%s: parked panel beyond the next half-ken" % p.name)
    tracks(p, a, KEN - POST / 2, zf, -1, thick, head_y=s1 - 0.03, sill_y=s0)
    for x in (0.0, HALF, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("park", (HALF, 0, 0), length=HALF, face="interior",
           note="the next half-ken must be a plain wall on the inside face: the panel parks there")
    p.dim("opening_m", "0.79 x %.2f" % (s1 - s0), 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (b - a, s1 - s0), ok=True)
    p.dim("open_stub_m (vanilla 0.22-0.30)", STUB, d.stub, source="G3 fix: vanilla sliding doors")
    return p


def part_amado_window(variant):
    """1-ken window with two amado storm shutters on the outside tracks: one action slides both into a board box
    (tobukuro) over the next half-ken; both keep STUB in the opening, so it closes from inside and outside."""
    p = Part("jp_p_open_amado_window", variant, "open", tiers=[2, 3],
             used_for="1-ken room window (zashiki, inn rooms) closed by two amado storm shutters that stow in a "
                      "tobukuro box beside it (T2-3)",
             datum="1-ken bay between post nodes x=0 and x=1.82 + the tobukuro over the next half-ken (to 2.73); "
                   "y 0 = room floor; opening 0.70-2.00")
    s0, s1 = 0.70, DOOR_H
    thick = 0.025
    zf = POST / 2
    rng = rng_for("amado_window" + variant)
    build = leaf_plank("plain", "wood_weathered", rng)
    height = s1 - s0 - 0.03
    d = twin_leaves(p, A, B, s0, height, zf, +1, build, thick, "plank", note="amado storm shutters, outside tracks",
                    window=True)
    d.display = "window"
    d.anim_period, d.init_opened = 1.0, 0.5
    pe = d.park_end
    if pe > KEN + HALF - POST / 2 + 1e-3:
        raise ValueError("%s: stowed shutters end at %.3f, beyond the half-ken" % (p.name, pe))
    fm = "wood_weathered"
    # inside sill board and the frame the shutters close against
    p.add(box(A, B, s0 - 0.04, s0, -0.07, 0.07, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="sill"))
    tracks(p, A, B, zf, +1, 2 * thick + GAP, head_y=s1 - 0.03, sill_y=s0)
    # tobukuro: board box around the stowed leaves beyond the post face (x from the post face at 1.76)
    zo = zf + 2 * (GAP + thick) + 0.012
    bx0, bx1 = B, pe + 0.03
    for (x0, x1, y0, y1, z0, z1, tag) in ((bx0, bx1, s0 - 0.06, s1 + 0.10, zo, zo + 0.015, "box_front"),
                                          (bx1, bx1 + 0.015, s0 - 0.06, s1 + 0.10, zf, zo + 0.015, "box_end"),
                                          (bx0, bx1 + 0.015, s1 + 0.08, s1 + 0.10, zf, zo, "box_lid"),
                                          (bx0, bx1 + 0.015, s0 - 0.06, s0 - 0.04, zf, zo, "box_floor")):
        p.add(box(x0, x1, y0, y1, z0, z1, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag))
    p.extend(board_run(bx0 + 0.01, bx1 - 0.01, s0 - 0.04, s1 + 0.08, zo + 0.015, zo + 0.027, rng, 0.18, 0.28, fm,
                       vis=(1,), tag="box_board"))
    for x in (0.0, KEN, KEN + HALF):
        p.conn("post", (x, 0, 0))
    p.conn("park", (KEN, 0, 0), length=HALF, face="exterior",
           note="the tobukuro box covers the next half-ken on the outside: plain wall there")
    p.dim("opening_m", "1.70 x 1.30", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (B - A, s1 - s0), ok=True)
    p.dim("open_stub_m (vanilla 0.22-0.30)", STUB, d.stub, source="G3 fix: vanilla sliding doors")
    return p


TSUKIAGE_DEG = 75.0


def part_tsukiage(variant):
    """Half-ken window with wooden bars (Geometry only, so the camera ray passes) and a top-hinged board shutter
    outside that is pushed up and out (tsukiage / hanemage) by a rotation about its head: an animated door."""
    p = Part("jp_p_open_tsukiage", variant, "open", tiers=[1, 2, 3],
             used_for="half-ken storage / farmhouse / shop-side window: wooden bars and a board shutter hinged at the "
                      "top that is pushed up and out (tsukiage / hanemage)",
             datum="half-ken bay between post nodes x=0 and x=0.91; y 0 = floor; opening 0.90-1.60")
    a, b = A, HALF - POST / 2
    s0, s1 = 0.90, 1.60
    fm = "wood_weathered"
    p.add(box(a, b, s0 - 0.05, s0, -0.07, 0.07, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="sill"))
    p.add(box(a, b, s1, s1 + 0.06, -0.06, 0.06, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head"))
    p.add(box(a, b, s0, s1, -0.01, 0.01, fm, vis=(), geo=True, tag="bars_geo"))
    n = int((b - a) / 0.09)
    for k in range(n):
        x = a + (k + 0.5) * (b - a) / n
        p.add(box(x - 0.016, x + 0.016, s0, s1, -0.016, 0.016, fm, vis=(1, 2), tag="bar"))
    p.add(box(a, b, s0, s1, -0.012, 0.012, fm, vis=(3,), tag="bars_lod"))
    # shutter: boards + two battens, hinged at its top edge on the outside of the head
    hz = POST / 2 + 0.012
    hy = s1 + 0.05
    x0, x1 = a - 0.04, b + 0.04
    y0 = s0 - 0.05
    bone = p.next_bone()
    rng = rng_for("tsukiage" + variant)
    sol = [box(x0, x1, y0, hy, hz, hz + 0.028, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
    sol += board_run(x0, x1, y0, hy, hz, hz + 0.022, rng, 0.14, 0.22, fm, vis=(1,), tag="leaf_board", gap=LEAF_GAP)
    for yy in (y0 + 0.10, hy - 0.16):
        sol.append(box(x0 + 0.03, x1 - 0.03, yy, yy + 0.06, hz + 0.022, hz + 0.038, fm, vis=(1,), tag="leaf_batten"))
    for s in sol:
        s.door = bone
        p.add(s)
    for xx in (x0 + 0.08, x1 - 0.14):
        p.add(box(xx, xx + 0.06, hy - 0.01, hy + 0.03, POST / 2 - 0.005, hz + 0.03, "metal_iron", vis=(1,), tag="hinge"))
    # axis along -x: with the right-hand rule a positive angle swings the bottom edge OUT (+z) and up (core.ROT_SIGN)
    axis = [(x1, hy, hz), (x0, hy, hz)]
    p.memory[bone + "_axis"] = axis
    p.memory[bone] = [((x0 + x1) / 2, y0 + 0.06, hz + 0.014)]
    twin = "doorstwin1"
    act = ((a + b) / 2, (s0 + s1) / 2, 0.0)
    p.memory[twin + "_action"] = [act]
    for s in p.solids:
        if s.door == bone:
            s.sel = twin
    d = Door(kind="plank", anims=[{"bone": bone, "type": "rotation", "axis": axis,
                                   "amount": math.radians(TSUKIAGE_DEG), "note": "top-hinged shutter"}],
             action=act, centre=((x0 + x1) / 2, (y0 + hy) / 2, hz), twin=twin, anim_period=1.2, init_opened=0.5,
             display="window", note="top-hinged push-up shutter (rotation about the head, %d deg)" % TSUKIAGE_DEG,
             opening=(a, b, s0, s1), z_face=POST / 2, side=+1, passable=False, engine_tested=False,
             style="tsukiage", stub=None, act_h=(s0 + s1) / 2)
    p.doors.append(d)
    for x in (0.0, HALF):
        p.conn("post", (x, 0, 0))
    p.conn("head", (0, hy, 0), note="hinge line on the outside of the head rail")
    p.dim("opening_m", "0.79 x 0.70", 0.0)
    p.dims[-1].update(measured="%.2f x %.2f" % (b - a, s1 - s0), ok=True)
    p.dim("open_angle_deg", TSUKIAGE_DEG, TSUKIAGE_DEG, tol=0.5)
    return p


def register(reg):
    reg("jp_p_open_itado", ["_plain", "_battened", "_oodo", "_pair", "_twin", "_single"], part_itado)
    reg("jp_p_open_shoji_ext", ["_koshidaka", "_akari", "_twin", "_hikiwake", "_single"], part_shoji_ext)
    reg("jp_p_open_window_slide", ["_shoji", "_board"], part_window_slide)
    reg("jp_p_open_amado_window", ["_twin"], part_amado_window)
    reg("jp_p_open_tsukiage", ["_board"], part_tsukiage)
    reg("jp_p_open_amado", ["_stowed", "_closed"], part_amado)
    reg("jp_p_open_tobukuro", ["_box", "_swing"], part_tobukuro)
    reg("jp_p_open_kura_door", ["_open", "_hinged"], part_kura_door)
    reg("jp_p_open_mushiko", ["_oval", "_oval_pair"], part_mushiko)
    reg("jp_p_open_koshi", ["_kyo", "_oyako", "_komeya", "_degoshi", "_bengara"], part_koshi)
    reg("jp_p_open_renji", ["_bamboo", "_wood", "_muso"], part_renji)
    reg("jp_p_open_suriagedo", ["_closed", "_part", "_door"], part_suriagedo)
    reg("jp_p_open_koshido", ["_open", "_papered"], part_koshido)
    reg("jp_p_open_kura_window", ["_slide", "_hinged"], part_kura_window)
    reg("jp_p_open_shitomido", ["_up", "_closed"], part_shitomido)
    reg("jp_p_open_battari", ["_down", "_up"], part_battari)
    reg("jp_p_open_upper_rail", ["_plain"], part_upper_rail)
    reg("jp_p_open_mushiro", ["_rolled"], part_mushiro)
