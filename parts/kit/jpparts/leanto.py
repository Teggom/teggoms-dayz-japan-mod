"""Lean-to (geya / hisashi-ya) roof and the sloped wall under its verge (B0 step 0a, promoted from
buildings/machiya_t3_01, where it only knew sangawara).

Kit frame of roof(): the lean-to runs along x from x0 to x1 against a higher wall whose face is at z = z_wall; its
eave wall line is z = z_eave (< z_wall); the slope falls towards -z. Build it in this frame and transform the returned
Part to any side of a building (Part.transformed). y = grade.

All six coverings of the roof generator (roofs.PITCH): sangawara, hongawara (kawara, walkable 'tile_roof'), itabuki,
kakigara, ishioki (boards, walkable 'board_roof'; ishioki adds battens and stones) and thatch (thick slab, not walkable,
PLAYBOOK §15 T9). Every tiled lean-to has the clay bed and the fascia (§15 T1, C13).

With fam='sangawara' and the machiya's numbers, roof() builds exactly the machiya's geya roof (same solids, same
order), so the machiya did not change when it moved here.
"""
import math

from .core import Part, box, prism, POST, rng_for, add, mul, norm, cross, sub
from .shapes import oriented_box, frame_of, tube
from . import roofs as R, kawara as K, frame, walls, trim

KAWARA = ("sangawara", "hongawara")
BOARDS = ("itabuki", "kakigara", "ishioki")
COVERINGS = KAWARA + BOARDS + ("thatch",)
PITCH = {"sangawara": 0.40, "hongawara": 0.40, "ishioki": 0.30, "itabuki": 0.40, "kakigara": 0.40, "thatch": 1.0}
# lean-to pitches: tiled 4 sun (the machiya geya), boards a little flatter than the main-roof table, stone-weighted
# boards 3 sun (stones slide on steeper slopes), thatch never under 45 degrees (it leaks)


def roof(name, x0, x1, z_wall, z_eave, eave_y, fam="sangawara", t=None, ov=None, gov=None, flash_top=None,
         keta=True, keta_ext=0.30, verges=(True, True), slope_name="geya", worn=False):
    """The lean-to roof: Slope + collision + sheathing + covering + verges + a flashing strip against the higher wall
    + bargeboards + the eave keta. Returns (part, slope).

    eave_y: keta top (roof bed) at the eave wall line z_eave. ov: eave overhang past z_eave; gov: verge overhang past
    x0 / x1 (a number or (left, right)). flash_top: top of the flashing board against the higher wall (default: 0.40
    above the roof line there). verges: (left, right) build a verge (tiles / bargeboard) at that end; False = the end
    is left plain for a neighbouring roof or a party-roof-end part (B2) to close."""
    if fam not in COVERINGS:
        raise ValueError("lean-to covering %r (one of %s)" % (fam, ", ".join(COVERINGS)))
    t = PITCH[fam] if t is None else t
    ov = R.EAVE_OV[fam] if ov is None else ov
    gov = R.GABLE_OV[fam] if gov is None else gov
    gl, gr = gov if isinstance(gov, (tuple, list)) else (gov, gov)
    s = Part(name, "", "")
    zw = z_wall
    poly = [(x0 - gl, z_eave - ov), (x0 - gl, zw), (x1 + gr, zw), (x1 + gr, z_eave - ov)]
    sl = R.Slope(slope_name, poly, (0.0, 1.0), (0.0, z_eave), (-1.0, 0.0), (x1, z_eave - ov), eave_y, t, ov, True)
    sl.verges = (sl.u_of(x1 + gr, z_eave - ov), sl.u_of(x0 - gl, z_eave - ov))
    stack = R.STACK[fam]
    if fam in KAWARA:
        h_top = stack + 0.05
        R.collision(s, sl, h_top, "pottery", "tile_roof")
        R.sheathing(s, sl)
        R.tile_bed(s, sl, stack)                  # tiles seated on the clay bed (PLAYBOOK §15 T1)
        R.kawara_fascia(s, sl, stack)             # eave board under the eave tiles
        R.rafters(s, sl, only_eave=True)
        # kawara cover as roofs.cover_kawara, but one modelled eave row (the pent recipe's setting; a lean-to is a
        # deep pent) instead of two: rule 1 keeps the corrugation, eave-tile ends, verge tiles and the top row
        F = sl.frame(stack)
        u0, u1 = sl.u_range()
        vw = 0.13
        fu0 = sl.verges[0] + vw if verges[1] else u0          # u runs -x: verges[0] is the x1 (right) end
        fu1 = sl.verges[1] - vw if verges[0] else u1
        rl = sl.depth_at((u0 + u1) / 2) / sl.cos
        if fam == "hongawara":
            K.hongawara_field(s, F, fu0, fu1, K.EXPO, rl)
        else:
            K.field(s, F, fu0, fu1, K.EXPO, rl, rows_eave=1, rows_ridge=1)
        K.eave_tiles(s, F, fu0, fu1, style="plain")
        if verges[1]:
            K.verge(s, F, sl.verges[0], 0.0, rl, -1)
        if verges[0]:
            K.verge(s, F, sl.verges[1], 0.0, rl, +1)
        yw = sl.y(0.0, zw - 0.10, stack) + 0.02
        # a verge end left plain (a party end, B2) keeps the flashing course inside the lot (noshi run 1 cm past p)
        K.ridge(s, (x0 - gl + (0.012 if not verges[0] else 0.0), yw, zw - 0.10),
                (x1 + gr - (0.012 if not verges[1] else 0.0), yw, zw - 0.10), courses=1, width=0.16, cap_d=0.0001,
                mortar=True, end_tiles=False)
        y_flash0 = yw - 0.02
    elif fam in BOARDS:
        R.collision(s, sl, stack + 0.012, "wood", "board_roof")
        R.sheathing(s, sl)
        R.rafters(s, sl, only_eave=True)
        R.cover_boards(s, sl, fam, worn=worn, rows_eave=2, rows_ridge=0)
        if fam == "ishioki":
            R.battens_stones(s, sl, stack - 0.02, spacing=0.55, first=0.35)
        y_flash0 = sl.y(0.0, zw - 0.03, stack) - 0.02
    else:                                           # thatch: the body slab is the collision (not walkable)
        R.cover_thatch(s, sl)
        R.rafters(s, sl, spacing=0.303, round_=True, only_eave=False, vis=(1,))
        for pc in sl.pieces:
            s.add(R.slab(pc, lambda x, z: sl.y(x, z, 0.055), lambda x, z: sl.y(x, z, 0.06), "bamboo_weathered",
                         vis=(1, 2), tag="lath", uvscale=(0.5, 0.5)))
        yt = sl.y(0.0, zw - 0.15, stack + 0.60)
        s.add(tube((x0 - gl - 0.1, yt, zw - 0.15), (x1 + gr + 0.1, yt, zw - 0.15), 0.18, "roof_thatch", n=8,
                   vis=(1, 2, 3), tag="thatch_roll", uvscale=(2.0, 2.0)))
        y_flash0 = None
    if y_flash0 is not None:
        top = flash_top if flash_top is not None else y_flash0 + 0.42
        s.add(box(x0 - gl, x1 + gr, y_flash0, top, zw - 0.03, zw, "wood_weathered", vis=(1, 2), tag="flashing"))
    if keta:
        ke0, ke1 = keta_ext if isinstance(keta_ext, (tuple, list)) else (keta_ext, keta_ext)
        frame.keta(s, x0 - ke0, x1 + ke1, z=z_eave, y_top=eave_y)
    if fam != "thatch":
        for x, sg, on in ((x0 - gl, -1.0, verges[0]), (x1 + gr, 1.0, verges[1])):
            if not on:
                continue
            a = (x, sl.y(x, z_eave - ov, stack) - 0.02, z_eave - ov)
            b = (x, sl.y(x, zw, stack) + 0.02, zw)
            d, e1, e2 = frame_of(sub(b, a))
            up = norm(cross((1.0, 0.0, 0.0), d))
            if up[1] < 0:
                up = mul(up, -1.0)
            c = add(tuple((a[k] + b[k]) / 2 for k in range(3)), mul(up, -0.12 + 0.03))
            L = math.dist(a, b)
            s.add(oriented_box(add(c, (sg * 0.015, 0.0, 0.0)), d, up, (1.0, 0.0, 0.0), L / 2 + 0.03, 0.12, 0.015,
                               "wood_weathered", vis=(1, 2, 3), tag="hafu"))
            if fam in BOARDS:
                cc = add(c, add((sg * 0.05, 0.0, 0.0), mul(up, 0.10)))
                s.add(oriented_box(cc, d, up, (1.0, 0.0, 0.0), L / 2 + 0.03, 0.025, 0.02, "wood_weathered",
                                   vis=(1, 2, 3), tag="verge_batten"))
    s.meta["leanto"] = {"fam": fam, "t": t, "ov": ov, "gov": (gl, gr), "eave_y": eave_y, "z_wall": zw,
                        "z_eave": z_eave, "x": (x0, x1)}
    return s, sl


def sloped_wall(name, nodes, y0, ytop, mat="wall_nakanuri", t=0.075, head_y=None, door_bays=(), koshiita_h=None,
                grime=False, window=None, interior="back"):
    """Wall under a lean-to verge (or any sloped roof line): infill between post faces from y0 up to the roof line
    ytop(x) (local x), a head rail at head_y, and a sloped wall plate under the roof bed. The shinkabe recipe
    (walls.wall_run) cut to the roof line. Local frame: x along the wall (post nodes at `nodes`), +z = out.
    door_bays: node x of bays left open (a door goes there); window: (x0, x1, y0, y1) hole in the bay starting at x0.
    interior: 'back' (exterior wall) or 'both' (partition): the room faces get the interior clay (§15 T6)."""
    mat = walls.interior_mats(mat, interior)
    s = Part(name, "", "")
    fm = "wood_weathered"
    rng = rng_for(name)
    for i in range(len(nodes) - 1):
        a, b = nodes[i] + POST / 2, nodes[i + 1] - POST / 2
        is_door = any(abs(nodes[i] - d) < 1e-6 for d in door_bays)
        ylo = y0
        if head_y is not None:
            if not is_door:
                holes = [window] if window and abs(window[0] - a) < 1e-6 else []
                for (r0, r1, s0, s1) in walls._split(a, b, y0, head_y, holes):
                    s.add(box(r0, r1, s0, s1, -t / 2, t / 2, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                              tag="infill", uvoff=(rng.random(), rng.random())))
            s.add(box(a, b, head_y, head_y + walls.HEAD_T, -POST / 2, POST / 2, fm, vis=(1, 2, 3), geo=True, view=True,
                      fire=True, tag="head_rail"))
            ylo = head_y + walls.HEAD_T
        poly = [(a, ylo), (b, ylo), (b, ytop(b) - 0.12), (a, ytop(a) - 0.12)]
        s.add(prism(poly, "z", -t / 2, t / 2, mat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="infill_sloped",
                    uvoff=(rng.random(), rng.random())))
        if koshiita_h and not is_door:
            walls.koshiita(s, a, b, koshiita_h, t / 2, y0=y0)
        if grime and not is_door:
            trim.grime_band(s, a, b, t / 2 + (0.015 if koshiita_h else 0.0), y0=y0)
    x0, x1 = nodes[0] - POST / 2, nodes[-1] + POST / 2
    s.add(prism([(x0, ytop(x0) - 0.12), (x1, ytop(x1) - 0.12), (x1, ytop(x1)), (x0, ytop(x0))], "z", -POST / 2,
                POST / 2, fm, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="wall_plate"))
    return s
