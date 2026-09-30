"""The half-height hinged board door of toilets and booths (B2 part 7, jp_p_open_halfdoor; PARTS_GAP_AUDIT §3 part 35;
G1 A1 ruling 1: the toilet is a walk-in 1 x 1.5 ken outhouse with ONE door, D1 applies). BUILDING_LIST: 'urban shared
toilets with half doors'; 'shared toilet with half-height doors'.

Part frame (PLAYBOOK §10.2): a 1-ken bay between the post nodes x 0 and x 1.82; y 0 = the floor (sill); +z = out.
The wall recipe leaves the hole (walls.wall_run(openings=[(0.06, 1.76, 0.0, 2.0)])) and its head rail at 2.00; the
part fills the bay: a door post, a fixed board panel beside the door, the leaf and its hinges. The doorway is 1.04 m
clear (post face to door post, D1 >= 1.00), 2.00 high (D2); the leaf covers 0.25-1.45 m, the top of the doorway stays
open, as the period doors did.

The leaf is a ROTATION door (DoorsTwinN convention, model.cfg type rotation, right-hand rule about axis point
1 -> 2, PLAYBOOK §15 T4): it swings OUT by 90 degrees about its hinge edge. Rotation doors are still engine-untested
(audit §6 risk 4, the kura _hinged and the tsukiage wait on Stephen's check): engine_tested False. If it swings the
wrong way in game, swap the two axis points and change nothing else.
"""
import math

from .core import Part, box, Door, KEN, POST, DOOR_H, rng_for
from .shapes import board_run

A = POST / 2
OPEN_W = 1.04                  # clear doorway (D1 >= 1.00)
LEAF_Y = (0.25, 1.45)          # the half-height leaf
SWING = 90.0                   # degrees, outwards


def halfdoor(part, x0=0.0, hinged=True, mat="wood_weathered", swing=SWING, face_z=POST / 2):
    """The half door in the 1-ken bay starting at post node x0. face_z: the wall's outer face the leaf closes against
    (POST / 2 for an earth wall between posts, POST / 2 + 0.015 for boards on the posts' outer face). Returns the
    Door (or None for the static open leaf)."""
    rng = rng_for(part.name + "halfdoor")
    fm = mat
    xo0, xo1 = x0 + A, x0 + A + OPEN_W                     # the doorway, post face to door post face
    xd = xo1 + 0.03                                         # door post centre (0.06 square)
    # door post, fixed board panel beside the door (to the next post face), a low sill board
    part.add(box(xd - 0.03, xd + 0.03, 0.0, DOOR_H, -0.045, 0.045, fm, vis=(1, 2, 3), geo=True, view=True, fire=True,
                 tag="door_post", grain="long"))
    pa, pb = xd + 0.03, x0 + KEN - A
    part.add(box(pa, pb, 0.0, DOOR_H, -0.015, 0.015, fm, vis=(), geo=True, view=True, fire=True, tag="panel_geo"))
    part.extend(board_run(pa, pb, 0.0, DOOR_H, -0.015, 0.015, rng, 0.18, 0.26, fm, vis=(1, 2), tag="panel_board",
                          gap=0.0))
    part.add(box(pa, pb, 0.0, DOOR_H, -0.015, 0.015, fm, vis=(3,), tag="panel_lod"))
    for yy in (0.35, 1.55):
        part.add(box(pa, pb, yy, yy + 0.06, 0.015, 0.035, fm, vis=(1,), tag="panel_batten"))
    part.add(box(xo0, xo1, 0.0, 0.03, -0.05, 0.05, fm, vis=(1, 2), tag="sill_board"))
    # the leaf: boards + two battens + a diagonal brace, overlapping both jambs; its back 2 mm off the post faces
    l0, l1 = x0 + 0.02, xd + 0.02
    z0, z1 = face_z + 0.002, face_z + 0.030
    y0, y1 = LEAF_Y
    leaf = [box(l0, l1, y0, y1, z0, z1, fm, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
    leaf += board_run(l0, l1, y0, y1, z0, z1 - 0.004, rng, 0.16, 0.24, fm, vis=(1,), tag="leaf_board", gap=0.0)
    for yy in (y0 + 0.10, y1 - 0.16):
        leaf.append(box(l0 + 0.04, l1 - 0.04, yy, yy + 0.07, z1 - 0.004, z1 + 0.016, fm, vis=(1,), tag="leaf_batten"))
    # rope pull on the free edge (both faces)
    for zz in ((z1 + 0.016, z1 + 0.04), (z0 - 0.024, z0)):
        leaf.append(box(l1 - 0.12, l1 - 0.06, 0.95, 1.05, zz[0], zz[1], "straw_rope", vis=(1,), tag="pull_rope"))
    # stop on the door post the leaf closes against (inside the leaf's overlap, T11)
    part.add(box(xd - 0.03, xd + 0.03, y0, y1, 0.045, face_z, fm, vis=(1, 2), tag="jamb_stop"))
    hx, hz = l0 + 0.005, z1 + 0.004                        # hinge line: the leaf's outer face at its hinge edge
    for yy in (y0 + 0.12, y1 - 0.18):
        leaf.append(box(l0, l0 + 0.22, yy, yy + 0.05, z1, z1 + 0.006, "metal_iron", vis=(1,), tag="hinge_strap"))
        part.add(box(x0 - A + 0.035, x0 + A, yy, yy + 0.05, face_z - 0.004, face_z + 0.004, "metal_iron", vis=(1,),
                     tag="hinge_plate"))
    if not hinged:
        # static open: the leaf stands out from the wall, swung by `swing` about the hinge line (no animation)
        from .core import anim_point_fn
        a = {"type": "rotation", "axis": [(hx, y1 + 0.1, hz), (hx, y0 - 0.1, hz)], "amount": math.radians(swing)}
        f = anim_point_fn(a, 1.0)
        for s in leaf:
            s.verts = [f(v) for v in s.verts]
            s.center = f(s.center)
            s.fm = None
            part.add(s)
        return None
    bone = part.next_bone()
    for s in leaf:
        s.door = bone
        part.add(s)
    # axis pointing DOWN: + angle by the right-hand rule turns +x into +z, the leaf swings out (core.ROT_SIGN)
    axis = [(hx, y1 + 0.10, hz), (hx, y0 - 0.10, hz)]
    part.memory[bone + "_axis"] = axis
    # the leaf point (IsInReach) 0.30 from the hinge at hand height: it stays within 2 m of a player on either side
    # when the leaf is open (at the free edge it would swing 1.1 m out, out of reach from inside: C10)
    part.memory[bone] = [(l0 + 0.30, 1.00, (z0 + z1) / 2)]
    twin = "doorstwin%d" % (len(part.doors) + 1)
    act = ((xo0 + xo1) / 2, 1.0, face_z)
    part.memory[twin + "_action"] = [act]
    for s in part.solids:
        if s.door == bone:
            s.sel = twin
    d = Door(kind="plank", anims=[{"bone": bone, "type": "rotation", "axis": axis, "amount": math.radians(swing),
                                   "note": "half door, swings out"}],
             action=act, centre=((l0 + l1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), twin=twin, anim_period=0.9,
             init_opened=0.4, display="door", note="half-height hinged board door (toilet / booth), swings out %d deg"
             % swing, opening=(xo0, xo1, 0.0, DOOR_H), z_face=face_z, side=+1, passable=True, engine_tested=False,
             style="hinged_half", stub=None, act_h=1.0, half=True, half_top=DOOR_H - 1.0, clear=OPEN_W)
    part.doors.append(d)
    return d


def part_halfdoor(variant, face_z=POST / 2):
    hinged = variant == "_hinged"
    p = Part("jp_p_open_halfdoor", variant, "open", tiers=[1, 2, 3],
             used_for=("walk-in toilet / booth door (DW26, G1 A1-1): half-height hinged board leaf (rotation door, "
                       "swings out 90 deg; ENGINE-UNTESTED like every rotation door) in a 1-ken bay with a door post "
                       "and a fixed board panel; doorway 1.04 x 2.00" if hinged else
                       "the same half door as left: static, standing open (no animation) - dressing or a toilet "
                       "whose door is gone"),
             datum="1-ken bay between post nodes x=0 and x=1.82; y 0 = floor; +z = out (the leaf swings out)")
    halfdoor(p, 0.0, hinged=hinged, face_z=face_z)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0))
    p.conn("head", (0, DOOR_H, 0), note="the wall's head rail over the doorway (wall_run head=True)")
    p.dim("clear_width_m", ">=1.00", OPEN_W, source="PLAYBOOK D1 (G1 A1-1: D1 applies to the toilet)")
    p.dims[-1]["ok"] = OPEN_W >= 1.0
    p.dim("clear_height_m", ">=2.00", DOOR_H, source="PLAYBOOK D2")
    p.dims[-1]["ok"] = True
    p.dim("leaf_band_m", "0.25-1.45", 0.0, source="half door (A): the top of the doorway stays open")
    p.dims[-1].update(measured="%.2f-%.2f" % LEAF_Y, ok=True)
    p.notes.append("The wall recipe must leave the hole walls.wall_run(openings=[(0.06, 1.76, 0.0, 2.0)]) and keep its "
                   "head rail (head=True). C11 counts the open top of the doorway as part of the door's portal "
                   "(Door.half).")
    return p


def register(reg):
    reg("jp_p_open_halfdoor", ["_hinged", "_open"], part_halfdoor)
