"""Gates (W2C, Phase C wave 2, 2026-10-01): the ward gate (kido) kit. A NEW module (PARTS_GAP_AUDIT #2 open_gate_leaf
+ #3 gate, the kido subset); nothing else in the kit changes. Used by parts/kit/jpparts/templates/civic.py.

Period form (BUILDING_LIST 'Ward gate (kido)': posts, beam, two leaves plus a wicket; closed about 10 pm, after that
people passed through the wicket [T11]): two heavy posts with a head tie beam (kashira-nuki) through them and a cap
beam (kasagi) on top, two hinged leaves (lattice over a board base, or boards) swinging into the ward, and beside them
a narrow bay with the wicket (kuguri) under a board panel.

Gate frame (local): x along the gate line, z = 0 the gate plane (the post centres), +z = the street side (outside the
ward), -z = the ward side; y = grade. The main posts stand at x = 0 and x = span.

    p = gate_leaves("_lattice", span)        # one DoorsTwin, two rotation bones, leaves on the ward face, swing in
    kido_head(part, x0, x1, ...)             # tie beam + kasagi cap over the gate line (the bare kido)
    kido_roof(part, x0, x1, ...)             # or a small board gable roof on two cross pieces (the roofed kido)

Leaves (PLAYBOOK §15 T2-T4, the kura '_hinged' rotation convention, core.ROT_SIGN): each leaf hangs behind its post
(it overlaps the post's back face by OVERLAP, so no slit shows at the hinge jamb), is hinged on a vertical axis at its
back outer corner and turns 90 deg into the ward; the two meet with a MEET-wide astragal on the left leaf's face (no
slit at the meeting stile, C17). One door action opens both (the DoorsTwinN convention). The open leaves stand square
to the gate line against the posts' back faces: clear = span - post (2.55 m on a 1.5-ken span with 0.18 posts, D1).
Engine-untested like every hinged leaf (the kura's are the only others).
"""
import math

from .core import Part, box, Door, HALF, rng_for
from .shapes import board_run
from .openings import LEAF_GAP

POST_K = 0.18            # kido main post (heavier than a house post: ~6 sun)
LEAF_T = 0.05            # leaf thickness
OVERLAP = 0.05           # leaf behind its post (hinge jamb seal)
GAP = 0.004              # air between a leaf and the post back face / the other leaf
LEAF_Y0 = 0.03           # leaf bottom over grade (no sill: the street runs through)
LEAF_H = 2.22            # leaf height (top 2.25 over grade; the template lifts the leaves over its 5 cm threshold)
MEET = 0.05              # astragal overlap at the meeting stiles (as openings.MEET)
BEAM_Y = 2.40            # tie beam underside (head room over the passage 2.40 - grade)
BEAM_D = 0.18            # tie beam depth
POST_TOP = 2.95          # main posts' top (the kasagi sits on it)


def _leaf_solids(x0, x1, y0, y1, z0, z1, variant, rng, astragal=0, hinge=None):
    """Visual + collision solids of one leaf (closed, in gate-local coordinates). variant '_lattice': board base up to
    0.90 + vertical bars above (tategoshi), see-through by design (door kind 'lattice'); '_board': battened boards."""
    fm = "wood_street_dark"
    out = [box(x0, x1, y0, y1, z0, z1, fm, vis=(), geo=True, view=True, fire=True, tag="gate_leaf_geo")]
    st = 0.07
    # frame: two stiles, top / middle / bottom rails (every LOD keeps the frame: the far silhouette)
    out.append(box(x0, x0 + st, y0, y1, z0, z1, fm, vis=(1, 2, 3), tag="gate_stile"))
    out.append(box(x1 - st, x1, y0, y1, z0, z1, fm, vis=(1, 2, 3), tag="gate_stile"))
    out.append(box(x0 + st, x1 - st, y1 - 0.09, y1, z0, z1, fm, vis=(1, 2, 3), tag="gate_rail"))
    out.append(box(x0 + st, x1 - st, y0, y0 + 0.10, z0, z1, fm, vis=(1, 2, 3), tag="gate_rail"))
    if variant == "_lattice":
        yb = y0 + 0.90
        out.append(box(x0 + st, x1 - st, yb - 0.08, yb, z0, z1, fm, vis=(1, 2, 3), tag="gate_rail"))
        # the board base: boards butt tight (LEAF_GAP) on the leaf's mid plane
        zm0, zm1 = z0 + 0.015, z1 - 0.015
        out += board_run(x0 + st, x1 - st, y0 + 0.10, yb - 0.08, zm0, zm1, rng, 0.18, 0.26, fm, vis=(1,),
                         tag="gate_board", gap=LEAF_GAP)
        out.append(box(x0 + st, x1 - st, y0 + 0.10, yb - 0.08, zm0, zm1, fm, vis=(2, 3), tag="gate_board_lod"))
        # vertical bars over the base, 0.03 square at ~0.12 m centres
        n = max(3, int(round((x1 - x0 - 2 * st) / 0.12)))
        for k in range(1, n):
            x = x0 + st + k * (x1 - x0 - 2 * st) / n
            v = (1, 2) if k % 2 == 0 else (1,)
            out.append(box(x - 0.015, x + 0.015, yb, y1 - 0.09, z0 + 0.01, z1 - 0.01, fm, vis=v, tag="gate_bar"))
        # one horizontal tie bar through the bars
        ym = (yb + y1 - 0.09) / 2
        out.append(box(x0 + st, x1 - st, ym - 0.02, ym + 0.02, z0 + 0.005, z1 - 0.005, fm, vis=(1, 2), tag="gate_rail"))
    else:
        zm0, zm1 = z0 + 0.01, z1 - 0.01
        out += board_run(x0 + st, x1 - st, y0 + 0.10, y1 - 0.09, zm0, zm1, rng, 0.20, 0.28, fm, vis=(1,),
                         tag="gate_board", gap=LEAF_GAP)
        out.append(box(x0 + st, x1 - st, y0 + 0.10, y1 - 0.09, zm0, zm1, fm, vis=(2, 3), tag="gate_board_lod"))
        for yy in (y0 + 0.45, (y0 + y1) / 2, y1 - 0.50):
            out.append(box(x0 + st, x1 - st, yy - 0.05, yy + 0.05, z0 - 0.004, z0, fm, vis=(1, 2), tag="gate_batten"))
    # iron hinge straps on the hinge side, on the ward face. FX1 (2026-10-01): the hinge edge is passed in; it used
    # to follow `astragal`, which is 0 on the RIGHT leaf, so that leaf's straps sat at its free (meeting) edge
    if hinge is None:
        hinge = "l" if astragal >= 0 else "r"
    xh = x0 if hinge == "l" else x1
    for yy in (y0 + 0.30, y1 - 0.40):
        a, b = (xh, xh + 0.40) if hinge == "l" else (xh - 0.40, xh)
        out.append(box(a, b, yy, yy + 0.05, z0 - 0.006, z0, "metal_iron", vis=(1,), tag="hinge"))
    if astragal:
        # the meeting-stile astragal (C17): a strip on the street face of the LEFT leaf, over the gap
        xa = x1 if astragal > 0 else x0
        out.append(box(xa - 0.01, xa + MEET - 0.01, y0 + 0.02, y1 - 0.02, z1, z1 + 0.012, fm, vis=(1, 2),
                       tag="astragal"))
    return out


def gate_leaves(variant, span, post=POST_K, y0=LEAF_Y0, height=LEAF_H, swing_deg=90.0, y_floor=0.0):
    """The hinged leaf pair of a gate between main posts centred at x = 0 and x = span (gate-local frame). Returns a
    Part with ONE door (twin selection 'doorstwin1', bones doors1 / doors2, rotation, both on source DoorsTwin1);
    Builder.place_door renames the twin for the building. Leaves on the ward face (z < -post / 2), swing to -z."""
    p = Part("jp_p_open_gate_leaf", variant, "open", tiers=[2, 3],
             used_for="hinged gate leaves (kido): one action swings both into the ward",
             datum="gate line z = 0 through the main post centres x = 0 and x = %.3f; y 0 = grade" % span)
    rng = rng_for("gate_leaf" + variant)
    zf = -post / 2 - GAP                     # leaf street face
    zb = zf - LEAF_T                         # leaf ward face
    xm = span / 2
    yt = y0 + height
    xa0 = post / 2 - OVERLAP                 # left leaf hinge edge (behind the left post)
    xa1 = span - post / 2 + OVERLAP          # right leaf hinge edge
    twin = "doorstwin1"
    anims = []
    specs = [(xa0, xm - GAP / 2, +1), (xm + GAP / 2, xa1, -1)]
    ang = math.radians(swing_deg)
    for (l0, l1, sg) in specs:
        bone = "doors%d" % (len(anims) + 1)
        for s in _leaf_solids(l0, l1, y0, yt, zb, zf, variant, rng, astragal=(+1 if sg > 0 else 0),
                              hinge=("l" if sg > 0 else "r")):
            s.door = bone
            s.sel = twin
            p.add(s)
        xh = l0 if sg > 0 else l1
        # right-hand rule about axis0 -> axis1 (core.anim_point_fn, PLAYBOOK §15): the left leaf turns about +y, the
        # right one about -y, so both free edges go to -z (into the ward)
        axis = [(xh, y0, zb), (xh, yt, zb)] if sg > 0 else [(xh, yt, zb), (xh, y0, zb)]
        p.memory[bone + "_axis"] = axis
        p.memory[bone] = [((l0 + l1) / 2, y0 + 1.0, (zb + zf) / 2)]
        anims.append({"bone": bone, "type": "rotation", "axis": axis, "amount": ang,
                      "note": "%s leaf, swings into the ward" % ("left" if sg > 0 else "right")})
    action = (xm, y_floor + 1.0, zf)
    p.memory[twin + "_action"] = [action]
    kind = "lattice" if variant == "_lattice" else "plank"
    d = Door(kind=kind, anims=anims, action=action, centre=(xm, y0 + height / 2, (zb + zf) / 2), twin=twin,
             anim_period=2.0, init_opened=1.0, sound="doorWoodSlide", display="gate", style="hinged_gate",
             note="kido leaves (rotation pair)", engine_tested=False, passable=True, has_view=True, act_h=1.0,
             opening=(post / 2, span - post / 2, y0, yt), z_face=zf, side=-1, leaf_z=(zb, zf), sweep=(0.0, span),
             stub=0.0, hinged=True, swing_deg=swing_deg)
    p.doors.append(d)
    for x in (0.0, span):
        p.conn("post", (x, 0, 0), size=post)
    p.dim("clear_open_m", ">=1.00 (D1)", span - post - 2 * LEAF_T)
    p.dim("leaf_height_m", "2.1-2.3", height)
    return p


def kido_head(part, x0, x1, post=POST_K, beam_y=BEAM_Y, top=POST_TOP, proj=0.42, kasagi=True):
    """The bare kido's head: a tie beam (kashira-nuki) through the posts between x0 and x1 (centres) and a cap beam
    (kasagi) on the post tops, projecting `proj` past the outer posts, its ends cut on a slant."""
    m = "wood_street_dark"
    part.add(box(x0 - post / 2 - 0.10, x1 + post / 2 + 0.10, beam_y, beam_y + BEAM_D, -0.06, 0.06, m, vis=(1, 2, 3),
                 geo=True, view=True, fire=True, tag="kido_beam"))
    if not kasagi:
        return part
    # kasagi: 0.21 deep, 0.24 wide on the post tops
    part.add(box(x0 - proj, x1 + proj, top, top + 0.17, -0.12, 0.12, m, vis=(1, 2, 3), geo=True, view=True, fire=True,
                 tag="kasagi"))
    part.add(box(x0 - proj + 0.04, x1 + proj - 0.04, top + 0.17, top + 0.21, -0.13, 0.13, "wood_weathered",
                 vis=(1, 2), tag="kasagi_cap"))
    return part


def kido_roof(part, x0, x1, post=POST_K, top=POST_TOP, half=HALF):
    """The roofed kido: a cross piece (hijiki) on each main post top carries two purlins (keta) half a ken either side
    of the gate line; the template builds the small gable roof over them with roofs.roof (so the roof kit's checks
    see a normal roof). Returns the keta top (the roof's eave line)."""
    m = "wood_street_dark"
    for x in (x0, x1):
        part.add(box(x - 0.07, x + 0.07, top, top + 0.15, -half - 0.20, half + 0.20, m, vis=(1, 2, 3), geo=True,
                     view=True, fire=True, tag="hijiki"))
    ky = top + 0.15 + 0.12
    for z in (-half, half):
        part.add(box(x0 - 0.30, x1 + 0.30, top + 0.15, ky, z - 0.06, z + 0.06, m, vis=(1, 2, 3), geo=True, view=True,
                     fire=True, tag="keta"))
    return ky
