"""Hinged double doors for honden and halls (W2P1, 2026-10-01; jp_p_open_tobira; PARTS_GAP_AUDIT §3 part 22).
Period form and choices: parts/W2P1_NOTES.md.

Honden: paired board doors (ita-tobira) turning on pivot blocks (waraza) top and bottom, iron (bronze in period)
strap fittings (hasso) and a ring pull; many village honden and haiden have latticed doors (koshi-tobira); temple
halls have framed panel doors (sankarado).

Part frame (PLAYBOOK §10.2): a 1-ken bay between post nodes x 0 and x 1.82 (posts 0.12: the doorway runs between the
post faces, 1.70 m); y 0 = the sill / floor top; +z = outside. The wall recipe leaves the hole
(walls.wall_run(openings=[(0.06, 1.76, 0.0, 2.0)]), head rail kept); the part adds the head beam (kamoi) with the
pivot blocks, the threshold (kehanashi), the jamb stops and the two leaves.

The leaves are ROTATION doors (DoorsTwinN: one config door, one animation source, two bones; PLAYBOOK §15 T3 / T4,
right-hand rule about axis point 1 -> 2, core.ROT_SIGN). 'out' leaves sit on the outer side of the opening, hinge on
their outer face at the jambs and turn 90 deg out; 'in' leaves the mirror. They close against stops on the posts
(T11: no slit at the jambs) and meet under a batten (jogi-buchi) on the left leaf's face on the swing side, so the
opening leaves move apart without touching. Engine-untested like every rotation door: if a pair swings the wrong way in
game, swap each bone's two axis points and change nothing else.
"""
import math

from .core import Part, box, Door, KEN, POST, DOOR_H, rng_for, anim_point_fn
from .shapes import board_run

A = POST / 2
LEAF_T = 0.045
SILL_H = 0.03
SWING = 90.0
MAT = "wood_weathered"
METAL = "metal_iron"            # stand-in for bronze fittings (parts/W2P1_NOTES.md: missing material)


def _leaf(x0, x1, y0, y1, z0, z1, style, rng, mat, outer):
    """Solids of one closed leaf spanning x0..x1, y0..y1, z0..z1. outer = +1 when the leaf's outer (street) face is
    z1. The first solid is the leaf's collision box (LOD 2/3 + Geometry / View / Fire)."""
    zo, zi = (z1, z0) if outer > 0 else (z0, z1)
    sg = 1.0 if outer > 0 else -1.0
    out = [box(x0, x1, y0, y1, z0, z1, mat, vis=(2, 3), geo=True, view=True, fire=True, tag="leaf")]
    w = x1 - x0
    if style == "board":
        out += board_run(x0, x1, y0, y1, z0, z1, rng, 0.22, 0.32, mat, vis=(1,), tag="leaf_board", gap=0.0)
        # battens (san) on the inner face
        for yy in (y0 + 0.18, (y0 + y1) / 2, y1 - 0.24):
            out.append(box(x0 + 0.04, x1 - 0.04, yy, yy + 0.07, min(zi, zi - sg * 0.022), max(zi, zi - sg * 0.022),
                           mat, vis=(1,), tag="leaf_batten"))
        # hasso strap fittings on the outer face (top and bottom), from the hinge side
        return out
    if style == "lattice":
        fw = 0.065
        out.append(box(x0 + fw - 0.01, x1 - fw + 0.01, y0 + 0.07, y0 + 0.63, min(zo - sg * 0.006, zo - sg * 0.026),
                       max(zo - sg * 0.006, zo - sg * 0.026), mat, vis=(1,), tag="koshi_board"))
        for (a, b) in ((x0, x0 + fw), (x1 - fw, x1)):
            out.append(box(a, b, y0, y1, z0, z1, mat, vis=(1,), tag="stile"))
        for (a, b) in ((y0, y0 + 0.08), (y0 + 0.62, y0 + 0.68), (y1 - fw, y1)):
            out.append(box(x0 + fw, x1 - fw, a, b, z0, z1, mat, vis=(1,), tag="rail"))
        n = max(3, int(round((w - 2 * fw) / 0.085)))
        for k in range(1, n):
            x = x0 + fw + (w - 2 * fw) * k / n
            out.append(box(x - 0.014, x + 0.014, y0 + 0.68, y1 - fw, z0 + 0.008, z1 - 0.008, mat, vis=(1,),
                           tag="lattice_bar"))
        for yy in (y0 + 0.68 + (y1 - fw - y0 - 0.68) / 3, y0 + 0.68 + 2 * (y1 - fw - y0 - 0.68) / 3):
            out.append(box(x0 + fw, x1 - fw, yy - 0.012, yy + 0.012, z0 + 0.012, z1 - 0.012, mat, vis=(1,),
                           tag="lattice_rail"))
        return out
    # sankarado: framed panel door (stiles, rails, recessed panels; the upper panel band latticed)
    fw = 0.075
    for (a, b) in ((x0, x0 + fw), (x1 - fw, x1)):
        out.append(box(a, b, y0, y1, z0, z1, mat, vis=(1,), tag="stile"))
    rails = [y0, y0 + 0.30, y0 + 1.05, y1 - 0.42, y1 - fw]
    for yy in rails:
        h = fw if yy not in (y0,) else 0.10
        out.append(box(x0 + fw, x1 - fw, yy, yy + h, z0, z1, mat, vis=(1,), tag="rail"))
    # recessed panels between the rails (kagami-ita), 12 mm in from both faces
    bands = [(y0 + 0.10, y0 + 0.30), (y0 + 0.30 + fw, y0 + 1.05), (y0 + 1.05 + fw, y1 - 0.42)]
    for (a, b) in bands:
        out.append(box(x0 + fw, x1 - fw, a, b, z0 + 0.012, z1 - 0.012, mat, vis=(1,), tag="panel"))
    # top band: vertical lattice (renji) in front of a dark backing
    a, b = y1 - 0.42 + fw, y1 - fw
    out.append(box(x0 + fw, x1 - fw, a, b, z0 + 0.018, z1 - 0.018, "wood_sooted", vis=(1,), tag="panel_dark"))
    n = max(3, int(round((w - 2 * fw) / 0.07)))
    for k in range(1, n):
        x = x0 + fw + (w - 2 * fw) * k / n
        out.append(box(x - 0.011, x + 0.011, a, b, z0 + 0.006, z1 - 0.006, mat, vis=(1,), tag="lattice_bar"))
    return out


def tobira(part, x0=0.0, bay=KEN, style="board", swing="out", height=DOOR_H, mat=MAT, deg=SWING, hinged=True,
           ajar=35.0):
    """The pair of hinged leaves in the bay between post nodes x0 and x0 + bay. Returns the Door (None if static)."""
    rng = rng_for(part.name + "tobira")
    xa, xb = x0 + A, x0 + bay - A                       # the doorway, post face to post face
    out = 1.0 if swing == "out" else -1.0
    # leaf plane: out -> on the outer half of the opening; in -> on the inner half (2 mm off the centreline)
    z0, z1 = (0.002, 0.002 + LEAF_T) if out > 0 else (-0.002 - LEAF_T, -0.002)
    y0, y1 = SILL_H + 0.006, height - 0.006
    zh = z1 if out > 0 else z0                          # hinge line on the swing-side face
    # head beam (kamoi) over the doorway, threshold (kehanashi), jamb stops on the far side of the leaves
    part.add(box(xa, xb, height, height + 0.13, -0.052, 0.052, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                 tag="kamoi", grain="long"))
    part.add(box(xa, xb, 0.0, SILL_H, -0.055, 0.055, mat, vis=(1, 2, 3), geo=True, view=False, fire=True,
                 tag="kehanashi", grain="long"))
    zs0, zs1 = sorted((z0 if out > 0 else z1, (z0 if out > 0 else z1) - out * 0.035))
    for (sa, sb) in ((xa, xa + 0.022), (xb - 0.022, xb)):
        part.add(box(sa, sb, SILL_H, height, zs0, zs1, mat, vis=(1, 2), tag="jamb_stop"))
    part.add(box(xa + 0.022, xb - 0.022, height - 0.035, height, zs0, zs1, mat, vis=(1, 2), tag="head_stop"))
    # pivot blocks (waraza) on the head beam and the threshold at each hinge corner, clear of the leaf's swing
    for hx in (xa, xb):
        zc = zh + out * 0.04
        for (ya, yb) in ((height + 0.005, height + 0.075), (0.0, SILL_H + 0.002)):
            part.add(box(hx - 0.045 if hx == xa else hx - 0.045, hx + 0.045, ya, yb, min(zc - 0.035, zc + 0.035),
                         max(zc - 0.035, zc + 0.035), METAL if yb > 1.0 else mat, vis=(1,), tag="waraza"))
    mid = (xa + xb) / 2
    leaves = []
    bones = []
    for side in (-1, 1):                                # left leaf (hinge xa), right leaf (hinge xb)
        la, lb = (xa + 0.003, mid - 0.002) if side < 0 else (mid + 0.002, xb - 0.003)
        sol = _leaf(la, lb, y0, y1, z0, z1, style, rng, mat, out)
        hx = xa if side < 0 else xb
        # strap fittings + ring pull on the swing face (board / sankarado)
        zf0, zf1 = sorted((zh, zh + out * 0.006))
        if style != "lattice":
            for yy in (y0 + 0.25, y1 - 0.32):
                ea = la if side < 0 else lb - 0.38
                sol.append(box(ea, ea + 0.38, yy, yy + 0.06, zf0, zf1, METAL, vis=(1,), tag="hasso"))
        free = lb if side < 0 else la
        rx = free - side * 0.12
        sol.append(box(rx - 0.035, rx + 0.035, 0.96, 1.04, zf0, zf1, METAL, vis=(1,), tag="ring_pull"))
        if side < 0:
            # meeting batten on the left leaf's swing face, overlapping the right leaf by 3 cm
            zb0, zb1 = sorted((zh, zh + out * 0.016))
            sol.append(box(lb - 0.03, lb + 0.035, y0 + 0.02, y1 - 0.02, zb0, zb1, mat, vis=(1, 2), tag="jogi_buchi"))
        leaves.append((side, hx, sol))
    if not hinged:
        # static, ajar: each leaf turned `ajar` degrees about its hinge (dressing: doors left open)
        for side, hx, sol in leaves:
            ax = [(hx, y1 + 0.1, zh), (hx, y0 - 0.1, zh)] if (side < 0) == (out > 0) else \
                 [(hx, y0 - 0.1, zh), (hx, y1 + 0.1, zh)]
            f = anim_point_fn({"type": "rotation", "axis": ax, "amount": math.radians(ajar * (1.0 if side < 0 else
                                                                                               0.6))}, 1.0)
            for s in sol:
                s.verts = [f(v) for v in s.verts]
                s.center = f(s.center)
                s.fm = None
                part.add(s)
        return None
    twin = "doorstwin%d" % (len(part.doors) + 1)
    anims = []
    for side, hx, sol in leaves:
        bone = part.next_bone() if not anims else "doors%d" % (int(anims[-1]["bone"][5:]) + 1)
        for s in sol:
            s.door = bone
            s.sel = twin
            part.add(s)
        # axis DOWN turns +x into +z (right-hand rule): the left leaf swings out with a down axis, the right leaf with
        # an up axis; 'in' reverses both
        down = (side < 0) == (out > 0)
        axis = [(hx, y1 + 0.10, zh), (hx, y0 - 0.10, zh)] if down else [(hx, y0 - 0.10, zh), (hx, y1 + 0.10, zh)]
        part.memory[bone + "_axis"] = axis
        part.memory[bone] = [(hx - side * 0.30, 1.00, (z0 + z1) / 2)]
        anims.append({"bone": bone, "type": "rotation", "axis": axis, "amount": math.radians(deg),
                      "note": "%s leaf, swings %s" % ("left" if side < 0 else "right", swing)})
    act = (mid, 1.0, (z0 + z1) / 2)
    part.memory[twin + "_action"] = [act]
    clear = (xb - xa) - 2 * max(LEAF_T, 0.022) - 0.008
    d = Door(kind="lattice" if style == "lattice" else "plank", anims=anims, action=act,
             centre=(mid, (y0 + y1) / 2, (z0 + z1) / 2), twin=twin, anim_period=1.4, init_opened=0.0,
             display="door", note="hinged double door (%s, swings %s %d deg)" % (style, swing, deg),
             opening=(xa, xb, 0.0, height), z_face=zh, side=out, passable=True, engine_tested=False,
             style="tobira", stub=None, act_h=1.0, clear=clear, sound="doorWoodSlide")
    part.doors.append(d)
    return d


VARIANTS = {
    "_board_out": ("board", "out", True, "honden / hall front: paired board doors (ita-tobira) with strap fittings "
                   "and ring pulls, opening OUT 90 deg (rotation; engine-untested)", [1, 2, 3]),
    "_board_in": ("board", "in", True, "the same board pair opening IN (halls whose doors swing into the room)",
                  [1, 2, 3]),
    "_lattice_out": ("lattice", "out", True, "latticed doors (koshi-tobira) over a board base: village honden and "
                     "haiden fronts; open OUT", [1, 2, 3]),
    "_lattice_in": ("lattice", "in", True, "latticed doors opening IN", [1, 2, 3]),
    "_sankara_in": ("sankara", "in", True, "temple hall framed panel doors (sankarado) with a latticed top band, "
                    "opening IN", [2, 3]),
    "_board_ajar": ("board", "out", False, "static board pair standing ajar (35 / 21 deg): dead-world dressing, a "
                    "honden left open", [1, 2, 3]),
}


def part_tobira(variant):
    style, swing, hinged, used, tiers = VARIANTS[variant]
    p = Part("jp_p_open_tobira", variant, "open", tiers=tiers, used_for=used,
             recipe="tobira.tobira(part, x0, bay, style, swing, height)",
             datum="1-ken bay between post nodes x 0 and x 1.82; y 0 = floor (sill); +z = out")
    d = tobira(p, 0.0, KEN, style, swing, hinged=hinged)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0))
    p.conn("head", (0, DOOR_H, 0), note="kamoi over the doorway; the wall's head rail continues past it")
    clear = (KEN - 2 * A) - 2 * LEAF_T - 0.008
    p.dim("clear_width_m", ">=1.00", round(clear, 3), source="PLAYBOOK D1 (leaves open, square to the wall)")
    p.dims[-1]["ok"] = clear >= 1.0
    p.dim("clear_height_m", ">=2.00", DOOR_H, source="PLAYBOOK D2")
    p.dims[-1]["ok"] = True
    p.notes.append("The wall recipe must leave the hole walls.wall_run(openings=[(0.06, 1.76, 0.0, 2.0)]); the part "
                   "brings its own kamoi (2.00-2.13) and threshold (0.03).")
    if d is not None:
        p.notes.append("Rotation leaves, engine-untested (PARTS_GAP_AUDIT §6 risk 4): if they swing the wrong way, "
                       "swap each bone's axis points.")
    return p


def register(reg):
    reg("jp_p_open_tobira", list(VARIANTS), part_tobira)
