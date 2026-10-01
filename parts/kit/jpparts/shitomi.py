"""Grid-lattice shutters (shitomido) and fixed lattice fronts for worship halls (W2P1, 2026-10-01;
jp_p_open_shitomi_grid; PARTS_GAP_AUDIT §3 part 52). Period form and choices: parts/W2P1_NOTES.md.

Hall shitomido: a square grid (koshi) on a backing board in a frame; the upper leaf (jo-shitomi) is hinged at the head
and hooked up under the eave (tsuri-gane), the lower leaf (shimo-shitomi) is lifted out to open the bay. The town
shop's shitomido (openings.part_shitomido) is the plain-board relative.

Part frame (PLAYBOOK §10.2): a 1-ken bay between post nodes x 0 and x 1.82; y 0 = the sill / floor; +z = outside. The
leaves hang on the outside of the posts (they overlap the post faces 2 cm: no slit at the jambs, T11); the part brings
its head beam (nageshi-like kamoi at 2.00) and sill.
  _hinged   the upper leaf is a ROTATION window (DoorsTwinN, one bone, top-hinged: swings out and up 90 deg; PLAYBOOK
            §15 T4, engine-untested like the tsukiage); the lower leaf fixed: the bay is a window, not a door
  _closed   both leaves down (static)
  _open     upper leaf hooked up level under the eave, lower leaf removed: an open bay you can walk through (static)
  _fixed    a fixed see-through lattice front (koshi) over a board base: worship-hall side bays (blocks passage)
"""
import math

from .core import Part, box, Door, KEN, POST, DOOR_H, rng_for, anim_point_fn
from .openings import open_bar

A = POST / 2
MAT = "wood_weathered"
from .core import LIBRARY as _LIB  # noqa: E402
# W2S (2026-10-01): patinated bronze now exists (jp_m_metal_bronze); iron stays the fallback
METAL = "metal_bronze" if "metal_bronze" in _LIB else "metal_iron"
SPLIT = 0.86            # upper / lower leaf joint over the floor
SILL = 0.04
PITCH = 0.115           # grid pitch (A: ~4 sun squares)
LEAF_T = 0.05


def grid_leaf(x0, x1, y0, y1, z0, z1, mat=MAT, frame=0.06, pitch=PITCH, backed=True, tag="shitomi"):
    """Solids of one grid leaf, closed: the leaf box (LOD 2/3 + Geometry / View / Fire) first, then the LOD-1 detail:
    frame, backing board (if backed), the square grid bars on the outer face (z1), battens on the inner face."""
    out = [box(x0, x1, y0, y1, z0, z1, mat, vis=(2, 3), geo=True, view=True, fire=True, tag=tag)]
    for (a, b) in ((x0, x0 + frame), (x1 - frame, x1)):
        out.append(box(a, b, y0, y1, z0, z1, mat, vis=(1,), tag="shitomi_stile"))
    for (a, b) in ((y0, y0 + frame), (y1 - frame, y1)):
        out.append(box(x0 + frame, x1 - frame, a, b, z0, z1, mat, vis=(1,), tag="shitomi_rail"))
    ix0, ix1, iy0, iy1 = x0 + frame, x1 - frame, y0 + frame, y1 - frame
    zb0, zb1 = z0 + 0.012, z0 + 0.026
    if backed:
        out.append(box(ix0, ix1, iy0, iy1, zb0, zb1, mat, vis=(1,), tag="shitomi_board"))
    nx = max(2, int(round((ix1 - ix0) / pitch)))
    ny = max(2, int(round((iy1 - iy0) / pitch)))
    zg0, zg1 = zb1 + 0.002, z1 - 0.006
    for k in range(1, nx):
        x = ix0 + (ix1 - ix0) * k / nx
        out.append(open_bar(x - 0.011, x + 0.011, iy0, iy1, zg0, zg1, mat, "y", tag="grid_bar"))
    for k in range(1, ny):
        y = iy0 + (iy1 - iy0) * k / ny
        out.append(open_bar(ix0, ix1, y - 0.011, y + 0.011, zg0 + 0.003, zg1 + 0.003, mat, "x", tag="grid_bar"))
    return out


def shitomi(part, x0=0.0, bay=KEN, variant="_hinged", mat=MAT, head=DOOR_H, deg=90.0):
    """The shitomido (or fixed lattice) in the bay between post nodes x0 and x0 + bay. Returns the Door or None."""
    rng = rng_for(part.name + "shitomi")
    xa, xb = x0 + A, x0 + bay - A
    part.add(box(xa, xb, head, head + 0.13, -0.052, 0.052, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                 tag="kamoi", grain="long"))
    part.add(box(xa, xb, 0.0, SILL, -0.055, 0.055, mat, vis=(1, 2, 3), geo=True, view=False, fire=True, tag="sill",
                 grain="long"))
    lx0, lx1 = xa - 0.02, xb + 0.02                           # leaves overlap the posts' outer faces 2 cm
    z0, z1 = POST / 2 + 0.003, POST / 2 + 0.003 + LEAF_T
    if variant == "_fixed":
        # see-through fixed lattice: board base to 0.62, kumiko lattice above; one thin Geometry slab (no View: you see
        # in, players can't pass)
        fz0, fz1 = -0.025, 0.025
        part.add(box(xa, xb, SILL, 0.62, fz0 + 0.008, fz1 - 0.008, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                     tag="koshi_board"))
        part.add(box(xa, xb, 0.62, 0.68, fz0, fz1, mat, vis=(1, 2, 3), tag="koshi_rail"))
        part.add(box(xa, xb, 0.68, head, -0.012, 0.012, mat, vis=(), geo=True, view=False, fire=None,
                     tag="lattice_geo"))
        n = int(round((xb - xa) / 0.09))
        for k in range(1, n):
            x = xa + (xb - xa) * k / n
            part.add(open_bar(x - 0.014, x + 0.014, 0.68, head, -0.020, 0.020, mat, "y", tag="lattice_bar"))
        m = int(round((head - 0.68) / 0.30))
        for k in range(1, m):
            y = 0.68 + (head - 0.68) * k / m
            part.add(open_bar(xa, xb, y - 0.012, y + 0.012, -0.016, 0.016, mat, "x", tag="lattice_bar"))
        part.add(box(xa, xb, 0.68, head, -0.006, 0.006, mat, vis=(3,), tag="lattice_lod"))
        return None
    upper = grid_leaf(lx0, lx1, SPLIT + 0.003, head - 0.006, z0, z1, mat)
    lower = grid_leaf(lx0, lx1, SILL + 0.004, SPLIT - 0.003, z0, z1, mat, tag="shitomi_low")
    hy, hz = head - 0.006, z1                                # hinge line: the upper leaf's top outer edge
    # hinge straps on the head (visual), above the leaf
    for xx in (lx0 + 0.20, lx1 - 0.26):
        part.add(box(xx, xx + 0.06, head - 0.004, head + 0.05, POST / 2 - 0.004, z1 + 0.012, METAL, vis=(1,),
                     tag="hinge"))
    if variant == "_closed":
        part.extend(upper + lower)
        return None
    if variant == "_open":
        # upper leaf swung up level (static), hooked to two iron hooks; the lower leaf is out (the bay is open)
        f = anim_point_fn({"type": "rotation", "axis": [(lx1, hy, hz), (lx0, hy, hz)], "amount": math.radians(deg)}, 1.0)
        for s in upper:
            s.verts = [f(v) for v in s.verts]
            s.center = f(s.center)
            s.fm = None
            part.add(s)
        L = head - 0.006 - (SPLIT + 0.003)
        for xx in (lx0 + 0.25, lx1 - 0.25):
            part.add(box(xx - 0.006, xx + 0.006, hy + LEAF_T, hy + LEAF_T + 0.45, z1 + L - 0.10, z1 + L - 0.088, METAL,
                         vis=(1,), tag="tsurigane"))
        return None
    # _hinged: the upper leaf is a top-hinged rotation window; the lower leaf stays (fixed)
    part.extend(lower)
    bone = part.next_bone()
    twin = "doorstwin%d" % (len(part.doors) + 1)
    for s in upper:
        s.door = bone
        s.sel = twin
        part.add(s)
    axis = [(lx1, hy, hz), (lx0, hy, hz)]                    # along -x: + angle swings the bottom edge out and up
    part.memory[bone + "_axis"] = axis
    part.memory[bone] = [((lx0 + lx1) / 2, SPLIT + 0.10, (z0 + z1) / 2)]
    act = ((xa + xb) / 2, 1.30, 0.0)
    part.memory[twin + "_action"] = [act]
    d = Door(kind="plank", anims=[{"bone": bone, "type": "rotation", "axis": axis, "amount": math.radians(deg),
                                   "note": "top-hinged grid shutter, swings out and up"}],
             action=act, centre=((lx0 + lx1) / 2, (SPLIT + head) / 2, (z0 + z1) / 2), twin=twin, anim_period=1.6,
             init_opened=0.0, display="window", note="hall shitomido: upper grid leaf top-hinged (rotation %d deg)" % deg,
             opening=(xa, xb, SPLIT, head), z_face=POST / 2, side=+1, passable=False, engine_tested=False,
             style="shitomi", stub=None, act_h=1.30)
    part.doors.append(d)
    return d


VARIANTS = {
    "_hinged": ("worship / temple hall bay: grid shitomido, the upper leaf a top-hinged rotation window (out and up 90 "
                "deg; engine-untested), the lower leaf fixed", [1, 2, 3]),
    "_closed": ("grid shitomido closed, both leaves down (static)", [1, 2, 3]),
    "_open": ("grid shitomido open: upper leaf hooked up level on iron hooks, lower leaf removed: an open bay (static)",
              [1, 2, 3]),
    "_fixed": ("fixed see-through lattice front (koshi) over a board base for worship-hall side bays (players can see "
               "in, not pass)", [1, 2, 3]),
}


def part_shitomi(variant):
    used, tiers = VARIANTS[variant]
    p = Part("jp_p_open_shitomi_grid", variant, "open", tiers=tiers, used_for=used,
             recipe="shitomi.shitomi(part, x0, bay, variant)",
             datum="1-ken bay between post nodes x 0 and x 1.82; y 0 = floor; +z = out; leaves on the posts' outer faces")
    shitomi(p, 0.0, KEN, variant)
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0))
    p.conn("sill", (0, 0, 0))
    p.conn("head", (0, DOOR_H, 0), note="kamoi; the wall's head rail continues past it")
    if variant != "_fixed":
        p.dim("upper_leaf_m", "1.10-1.20", round(DOOR_H - SPLIT, 3))
        p.dims[-1]["ok"] = 1.05 <= DOOR_H - SPLIT <= 1.20
        p.dim("grid_pitch_m", "0.10-0.13 (A)", PITCH)
        p.dims[-1]["ok"] = True
    if variant == "_open":
        clear = KEN - 2 * A
        p.dim("open_bay_clear_m", ">=1.00", round(clear, 3), source="PLAYBOOK D1 (the bay is open)")
        p.dims[-1]["ok"] = clear >= 1.0
    return p


def register(reg):
    reg("jp_p_open_shitomi_grid", list(VARIANTS), part_shitomi)
