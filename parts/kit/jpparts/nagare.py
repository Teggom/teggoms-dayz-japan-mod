"""Shrine / temple roof generators, straight (village) versions (W2P1, 2026-10-01): the nagare-zukuri gable
(jp_p_roof_nagare), the kohai step canopy for any hall front (jp_p_roof_kohai) and the hogyo pyramid roof of square
halls (jp_p_roof_forms_hogyo). PARTS_GAP_AUDIT §3 parts 23 and 54. Period form and choices: parts/W2P1_NOTES.md.

They reuse roofs.py's Slope, coverings, collision, sheathing and rafters unchanged (no behaviour of the existing roof
generator changes); only the slope plans are new.

Frames (as roofs.roof): x 0..W along the ridge, z 0 = the front wall line .. -D the back wall line, y 0 = the hall
floor; eave line = keta top (eave_y, 2.88 by default).

CURVE HOOK (for W2P2's sori generator): nagare(..., curve=fn) and kohai(..., curve=fn) build the spec dict
(nagare_spec / kohai_spec: footprint, overhangs, pitch, family, eave line, the kohai post stations and floor height)
and hand it to fn(part, spec) instead of building the straight slopes. fn returns (slopes, info) like roofs.roof. The
straight builder and the curved one take the same spec, so a shell switches from village to town grade by passing
curve=sori.nagare (or whatever W2P2 names it) and nothing else.
"""
import math

from .core import Part, box, KEN, HALF, QK, POST, EAVE_Y, rng_for, norm, cross, mul, add
from .shapes import tube, oriented_box, frame_of, slab
from . import roofs as R
from . import kawara as K
from . import koran as KR

FAM_DEFAULT = "itabuki"         # kokera shingle (hiwada bark is missing: parts/W2P1_NOTES.md)


# ------------------------------------------------------------------------------------------------ specs
def nagare_spec(W, D, front=None, fam=FAM_DEFAULT, t=None, back_ov=None, gov=0.60, eave_y=EAVE_Y, drop=1.0,
                kohai_xs=None, en_depth=KR.DEPTH, kohai_z=None):
    """Everything the straight or the curved nagare builder needs. The kohai post line defaults to the foot of a
    kizahashi from an en of depth en_depth at floor height drop; the front overhang to that line + 0.60."""
    t = R.PITCH[fam] if t is None else t
    if kohai_z is None:
        run = KR.stair_flight(drop)[0]
        kohai_z = en_depth + run
    if front is None:
        front = kohai_z + 0.60
    return {"form": "nagare", "W": W, "D": D, "front": front, "back_ov": R.EAVE_OV[fam] if back_ov is None else back_ov,
            "gov": gov, "fam": fam, "t": t, "eave_y": eave_y, "drop": drop,
            "kohai_xs": list(kohai_xs) if kohai_xs is not None else [0.0, W], "kohai_z": kohai_z}


def kohai_spec(xa, xb, z_post, main_t=0.45, main_ov=0.90, eave_y=EAVE_Y, fam=FAM_DEFAULT, drop=0.60, proj=0.60,
               dy=None, gov=0.35, tuck=0.50, t_k=None):
    """A step canopy over the bay xa..xb on a hall whose front slope has pitch main_t, overhang main_ov and eave line
    eave_y: posts at z_post, eave proj beyond them, the canopy plane dy under the main slope's plane, its top tucked
    `tuck` inside the main eave (under the main roof body: no C12 poke)."""
    if dy is None:          # at the main eave edge the canopy's covering top is 3 cm under the main rafter plane (C12)
        dy = R.STACK[fam] + (0.05 if fam in ("sangawara", "hongawara") else 0.012) + 0.03
    t_k = main_t * 0.8 if t_k is None else t_k      # kohai roofs run flatter than the hall roof (GK)
    # the canopy's rafter plane y = eave_k - t_k * z passes dy under the main rafter plane at the main eave edge
    eave_k = eave_y - main_t * main_ov - dy + t_k * main_ov
    return {"form": "kohai", "xa": xa, "xb": xb, "z_post": z_post, "t": main_t, "t_k": t_k, "eave_k": eave_k,
            "main_ov": main_ov,
            "eave_y": eave_y, "fam": fam, "drop": drop, "proj": proj, "dy": dy, "gov": gov, "tuck": tuck}


# ------------------------------------------------------------------------------------------------ coverings
def _cover(part, sls, fam, walkable=True, worn=False):
    fire = {"thatch": "hay"}.get(fam, "pottery" if fam in ("sangawara", "hongawara") else "wood")
    h_top = R.STACK[fam] + (0.05 if fam in ("sangawara", "hongawara") else 0.012)
    surf = "tile_roof" if fam in ("sangawara", "hongawara") else "board_roof"
    for sl in sls:
        R.collision(part, sl, h_top, fire, surf if walkable else None)
        R.sheathing(part, sl)
        R.rafters(part, sl, only_eave=True)
        if fam in ("sangawara", "hongawara"):
            R.cover_kawara(part, sl, fam, "tomoe")
        else:
            R.cover_boards(part, sl, fam, worn=worn)
    return h_top


def hafu_asym(part, x, t, eave_y, z_front, z_back, z_ridge, sg, fam, board=(0.03, 0.24), purlin_from=0.0,
              purlins=True, purlin_to=None):
    """Bargeboards on a gable end at x (outer face towards sg) whose two eaves differ: front eave edge z_front, back
    z_back, ridge at z_ridge (the roof's ridge line); slope planes y = eave_y + t * (distance in from the wall line).
    The roofs.hafu recipe with separate front / back overhangs."""
    stack = R.STACK.get(fam, 0.1)
    kind = "tile" if fam in ("sangawara", "hongawara") else "board"
    yr = eave_y + stack + t * (purlin_from - z_ridge)
    for (ze, wall) in ((z_front, purlin_from), (z_back, None)):
        if wall is None:
            # back slope: wall line at z_ridge - (z_ridge - z_back_wall); y rises from the back eave to the ridge
            ye = yr - t * abs(z_ridge - ze)
        else:
            ye = eave_y + stack - t * (ze - wall)
        a = (x, ye - 0.02, ze)
        b = (x, yr + 0.02, z_ridge)
        d, e1, e2 = frame_of(tuple(b[k] - a[k] for k in range(3)))
        up = norm(cross((1.0, 0.0, 0.0), d))
        if up[1] < 0:
            up = mul(up, -1.0)
        c = add(tuple((a[k] + b[k]) / 2 for k in range(3)), mul(up, -board[1] / 2 + 0.03))
        part.add(oriented_box(add(c, (sg * board[0] / 2, 0.0, 0.0)), d, up, (1.0, 0.0, 0.0), math.dist(a, b) / 2 + 0.03,
                              board[1] / 2, board[0] / 2, "wood_weathered", vis=(1, 2, 3), tag="hafu"))
        if kind == "board":
            cc = add(c, add((sg * (board[0] + 0.02), 0.0, 0.0), mul(up, board[1] / 2 - 0.02)))
            part.add(oriented_box(cc, d, up, (1.0, 0.0, 0.0), math.dist(a, b) / 2 + 0.03, 0.025, 0.02,
                                  "wood_weathered", vis=(1, 2, 3), tag="verge_batten"))
    if purlins:
        # purlin ends every half ken on both slopes inside the body (the wall lines purlin_from / purlin_to)
        zt = purlin_to if purlin_to is not None else z_ridge - (purlin_from - z_ridge)
        for (z0, z1) in ((purlin_from, z_ridge), (zt, z_ridge)):
            k = 1
            span = abs(z1 - z0)
            while k * HALF < span - 0.1:
                zz = z0 + math.copysign(k * HALF, z1 - z0)
                yy = eave_y + t * k * HALF - 0.10
                part.add(box(min(x, x - sg * 0.30), max(x, x - sg * 0.30), yy - 0.06, yy + 0.06, zz - 0.05, zz + 0.05,
                             "wood_weathered", vis=(1, 2), tag="purlin_end"))
                k += 1
        part.add(box(min(x, x - sg * 0.30), max(x, x - sg * 0.30), eave_y + t * (purlin_from - z_ridge) - 0.12,
                     eave_y + t * (purlin_from - z_ridge) + 0.02, z_ridge - 0.06, z_ridge + 0.06, "wood_weathered",
                     vis=(1, 2), tag="purlin_end"))


# ------------------------------------------------------------------------------------------------ nagare
def nagare(part, W, D, front=None, fam=FAM_DEFAULT, t=None, back_ov=None, gov=0.60, eave_y=EAVE_Y, drop=1.0,
           kohai_xs=None, kohai_z=None, curve=None, walkable=True, worn=False, posts=True, mat="wood_weathered"):
    """The nagare-zukuri roof over a W x D body: a gable whose front slope runs on over the en and the kizahashi to
    the kohai post line, carried there by kohai posts (on stones at grade, y = -drop), a kohai beam and tie beams
    (straight stand-ins for the curved ebi-koryo, parallel to the rafters) back to the body's front posts. Returns
    (slopes, info). posts=False leaves the kohai frame to the shell."""
    S = nagare_spec(W, D, front, fam, t, back_ov, gov, eave_y, drop, kohai_xs, kohai_z=kohai_z)
    if curve is not None:
        return curve(part, S)
    t, front, ovb, fam = S["t"], S["front"], S["back_ov"], S["fam"]
    gl = gr = S["gov"]
    h = D / 2
    fs = R.Slope("front", [(-gl, front), (W + gr, front), (W + gr, -h), (-gl, -h)], (0.0, -1.0), (0.0, 0.0),
                 (1.0, 0.0), (0.0, front), eave_y, t, front, True, verges=(-gl, W + gr))
    bs = R.Slope("back", [(-gl, -D - ovb), (-gl, -h), (W + gr, -h), (W + gr, -D - ovb)], (0.0, 1.0), (0.0, -D),
                 (-1.0, 0.0), (W, -D - ovb), eave_y, t, ovb, True)
    bs.verges = (bs.u_of(W + gr, -D - ovb), bs.u_of(-gl, -D - ovb))
    sls = [fs, bs]
    _cover(part, sls, fam, walkable, worn)
    stack_top = R.STACK[fam] + 0.03
    yr = eave_y + t * h + stack_top
    info = {"slopes": ["front", "back"], "t": t, "ov": front, "back_ov": ovb, "gov": (gl, gr), "form": "nagare",
            "fam": fam, "ridge": ((-gl, yr, -h), (W + gr, yr, -h)), "spec": S}
    if fam in ("sangawara", "hongawara"):
        K.ridge(part, (-gl + 0.04, yr - 0.02, -h), (W + gr - 0.04, yr - 0.02, -h), courses=5 if fam == "hongawara" else 3)
        for x, f in ((-gl, (-1.0, 0.0, 0.0)), (W + gr, (1.0, 0.0, 0.0))):
            K.onigawara(part, (x + (0.04 if f[0] < 0 else -0.04), yr - 0.03, -h), f, height=0.38, width=0.33)
    else:
        info["ridge_top"] = R.board_ridge(part, (-gl, yr, -h), (W + gr, yr, -h), t)
    for x, sg in ((-gl, -1), (W + gr, 1)):
        hafu_asym(part, x, t, eave_y, front, -D - ovb, -h, sg, fam, purlin_to=-D)
    if posts and S["kohai_xs"]:
        info["kohai"] = kohai_frame(part, S["kohai_xs"], S["kohai_z"], t, eave_y, drop, mat=mat)
    part.meta.setdefault("roof", {k: v for k, v in info.items() if k != "spec"})
    return sls, info


def kohai_frame(part, xs, zp, t, eave_y, drop, plane_dy=0.0, beam_d=0.20, tie_d=0.12, mat="wood_weathered", z_wall=0.06,
                wall_xs=None, head_z=1.30, min_head=2.00):
    """Kohai posts at (x, zp) for x in xs on stones at grade (y -drop), the kohai beam (koryo) across their heads under
    the rafters, and tie beams parallel to the rafters from each post back to the body's front post face (z_wall).
    Rafter underside plane: y = eave_y - plane_dy - t * z. Returns dict(post_top, beam=(y0, y1))."""
    rng = rng_for(part.name + "kohai")
    under = lambda z: eave_y - plane_dy - t * z            # noqa: E731
    yb1 = under(zp + 0.07) - 0.004                          # beam top under the rafters at its outer face
    yb0 = yb1 - beam_d
    x0, x1 = min(xs), max(xs)
    part.add(box(x0 - 0.16, x1 + 0.16, yb0, yb1, zp - 0.065, zp + 0.065, mat, vis=(1, 2, 3), geo=True, view=True,
                 fire=True, tag="kohai_beam", grain="long"))
    # kibana: carved beam ends past the posts (a rounded nose)
    for xe, sg in ((x0 - 0.16, -1), (x1 + 0.16, 1)):
        part.add(box(min(xe, xe + sg * 0.06), max(xe, xe + sg * 0.06), yb0 + 0.03, yb1 - 0.03, zp - 0.05, zp + 0.05,
                     mat, vis=(1,), tag="kibana"))
    for x in xs:
        part.add(KR.stone(rng, x, zp, 0.34, 0.34, 0.14, -drop + 0.08, "stone_cut", bury=0.06, flat_top=0.92, n=8,
                          vis=(1, 2, 3), tag="kohai_stone"))
        n = 8
        r = 0.075 / math.cos(math.pi / n)
        part.add(tube((x, -drop + 0.08, zp), (x, yb0, zp), r, mat, n=n, vis=(1, 2, 3), geo=True, view=True, fire=True,
                      tag="kohai_post", grain="long"))
        # tie beam: from the post (just under the beam) back to the body's front wall, parallel to the rafter plane
        za, zb = z_wall + 0.004, zp - 0.08
        ya_top, yb_top = under(za) - 0.03, under(zb) - 0.03
        # the tie beams cross the en: under them >= min_head at the en's rail line head_z, or they are left out (the
        # canopy then rests on the hall's front beam and the kohai beam alone)
        head = under(head_z) - 0.03 - tie_d
        if head >= min_head and ya_top - tie_d > yb0 - 0.02:
            c = [(x - 0.055, ya_top - tie_d, za), (x + 0.055, ya_top - tie_d, za), (x + 0.055, yb_top - tie_d, zb),
                 (x - 0.055, yb_top - tie_d, zb), (x - 0.055, ya_top, za), (x + 0.055, ya_top, za),
                 (x + 0.055, yb_top, zb), (x - 0.055, yb_top, zb)]
            from .core import hexa
            part.add(hexa(c, mat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag="tsunagi", grain="long"))
    return {"post_top": yb0, "beam": (yb0, yb1), "xs": list(xs), "z": zp}


# ------------------------------------------------------------------------------------------------ kohai
def kohai(part, xa, xb, z_post, main_t=0.45, main_ov=0.90, eave_y=EAVE_Y, fam=FAM_DEFAULT, drop=0.60, proj=0.60,
          dy=None, gov=0.35, tuck=0.50, curve=None, walkable=True, mat="wood_weathered", head_z=1.30, t_k=None):
    """Step canopy (kohai) over the bay xa..xb of any hall front: a single slope parallel to the hall's front slope,
    dy under its plane, from `tuck` inside the main eave (hidden under the main roof) out to z_post + proj; verges
    with bargeboards; kohai posts, beam and tie beams (kohai_frame). Returns (slope, info)."""
    S = kohai_spec(xa, xb, z_post, main_t, main_ov, eave_y, fam, drop, proj, dy, gov, tuck, t_k)
    if curve is not None:
        return curve(part, S)
    t, eave_k = S["t_k"], S["eave_k"]
    ze = z_post + proj
    ztop = main_ov - tuck
    x0, x1 = xa - gov, xb + gov
    sl = R.Slope("front", [(x0, ze), (x1, ze), (x1, ztop), (x0, ztop)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0),
                 (0.0, ze), eave_k, t, ze, False, verges=(x0, x1))
    h_top = _cover(part, [sl], fam, walkable)
    # the canopy's upper end: a closing board under the main eave (the top edge never shows daylight)
    yt = sl.y(0.0, ztop, 0.0)
    part.add(box(x0 + 0.14, x1 - 0.14, yt - 0.02, yt + h_top - 0.01, ztop - 0.04, ztop - 0.004, mat, vis=(1, 2),
                 tag="kohai_top_board"))
    for x, sg in ((x0, -1), (x1, 1)):
        _kohai_hafu(part, x, sl, ztop, ze, sg, fam)
    info = {"slope": sl, "t": t, "eave_z": ze, "top_z": ztop, "spec": S}
    info["frame"] = kohai_frame(part, [xa, xb], z_post, t, eave_k, drop, mat=mat, head_z=head_z)
    return sl, info


def _kohai_hafu(part, x, sl, ztop, ze, sg, fam, board=(0.03, 0.20)):
    stack = R.STACK.get(fam, 0.1)
    a = (x, sl.y(x, ze, stack) - 0.02, ze)
    b = (x, sl.y(x, ztop, stack) - 0.01, ztop + 0.02)
    d, e1, e2 = frame_of(tuple(b[k] - a[k] for k in range(3)))
    up = norm(cross((1.0, 0.0, 0.0), d))
    if up[1] < 0:
        up = mul(up, -1.0)
    c = add(tuple((a[k] + b[k]) / 2 for k in range(3)), mul(up, -board[1] / 2 + 0.03))
    part.add(oriented_box(add(c, (sg * board[0] / 2, 0.0, 0.0)), d, up, (1.0, 0.0, 0.0), math.dist(a, b) / 2,
                          board[1] / 2, board[0] / 2, "wood_weathered", vis=(1, 2, 3), tag="hafu"))


# ------------------------------------------------------------------------------------------------ hogyo
def hogyo(part, W, fam=FAM_DEFAULT, t=None, ov=None, eave_y=EAVE_Y, apex="hoju_bronze", walkable=True, worn=False):
    """Pyramid roof over a W x W square hall (the yosemune slopes of roofs.slopes_for with W = D meet at one apex):
    coverings, hip ridges (kawara) or hip rolls (boards), an apex cap and a finial (ornament.hoju) in every LOD.
    Returns (slopes, info)."""
    t = R.PITCH[fam] if t is None else t
    ov = R.EAVE_OV[fam] if ov is None else ov
    sls = R.slopes_for(W, W, "yosemune", eave_y, t, ov, ov)
    for sl in sls:
        sl.full_ridge = False          # four triangles meeting at a point: no ridge courses (cover_boards' top rows)
    _cover(part, sls, fam, walkable, worn)
    h = W / 2
    stack_top = R.STACK[fam] + 0.03
    ya = eave_y + t * h + R.STACK[fam]
    for (e, tp) in R.hip_lines(sls, W, W, "yosemune", ov):
        p0 = (tp[0], R._hip_y(sls, tp, stack_top) - 0.02, tp[1])
        p1 = (e[0], R._hip_y(sls, e, stack_top) + 0.02, e[1])
        # stop the hip 0.18 short of the apex (the apex cap covers the meeting)
        d = norm(tuple(p1[k] - p0[k] for k in range(3)))
        p0 = add(p0, mul(d, 0.18))
        if fam in ("sangawara", "hongawara"):
            K.ridge(part, p0, p1, courses=2, width=0.20, cap_d=0.14, mortar=True, end_tiles=(False, True))
        else:
            part.add(tube(add(p0, (0.0, 0.03, 0.0)), add(p1, (0.0, 0.03, 0.0)), 0.085, "roof_kokera" if fam == "itabuki"
                          else R.BOARD_MAT[fam][0], n=6, squash=0.55, vis=(1, 2, 3), tag="hip_roll", uvscale=(1.0, 1.0)))
    # apex cap: a low square pyramid block over the meeting of the four hips (every LOD)
    cap_mat = "roof_kawara" if fam in ("sangawara", "hongawara") else "wood_weathered"
    cw = 0.30
    from .core import Solid
    yc = ya + 0.02
    verts = [(h - cw, yc - cw * t, -h - cw), (h + cw, yc - cw * t, -h - cw), (h + cw, yc - cw * t, -h + cw),
             (h - cw, yc - cw * t, -h + cw), (h - 0.12, yc + 0.10, -h - 0.12), (h + 0.12, yc + 0.10, -h - 0.12),
             (h + 0.12, yc + 0.10, -h + 0.12), (h - 0.12, yc + 0.10, -h + 0.12)]
    part.add(Solid(verts, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]], cap_mat,
                   vis=(1, 2, 3), tag="apex_cap"))
    info = {"slopes": [s.name for s in sls], "t": t, "ov": ov, "form": "hogyo", "fam": fam, "apex": (h, yc + 0.10, -h)}
    if apex:
        from . import ornament as ORN
        info["finial_top"] = ORN.hoju(part, (h, yc + 0.10, -h), kind=apex)
    part.meta.setdefault("roof", info)
    return sls, info


# ------------------------------------------------------------------------------------------------ parts
NAGARE_VARIANTS = {
    "_1ken": (KEN, KEN, "issha (1-ken square body) nagare-zukuri honden roof, kokera: the front slope runs on over a "
              "1.365 en and the kizahashi (floor +1.00) to two kohai posts at the stair foot; kohai beam, tie beams "
              "parallel to the rafters; straight (village; curve hook for W2P2's sori)"),
    "_3ken": (3 * KEN, 2 * KEN, "sangen-sha (3 x 2 ken body) nagare roof: the front slope carried by four posts "
              "across the stair-foot line"),
    "_1ken_tile": (KEN, KEN, "issha nagare roof in sangawara (a later / town re-roofing; most village honden keep "
                   "shingle or bark)"),
}


def part_nagare(variant):
    W, D, used = NAGARE_VARIANTS[variant]
    fam = "sangawara" if variant.endswith("_tile") else FAM_DEFAULT
    p = Part("jp_p_roof_nagare", variant, "roof", tiers=[1, 2, 3], used_for=used,
             recipe="nagare.nagare(part, W, D, front, fam, drop, kohai_xs, curve=None|W2P2 sori)",
             datum="body x 0..W along the ridge, z 0 (front wall line) .. -D; y 0 = hall floor (+1.00 above grade); "
                   "eave line 2.88; kohai posts at the kizahashi foot")
    xs = [0.0, W] if W < 2 * KEN else [k * KEN for k in range(int(round(W / KEN)) + 1)]
    sls, info = nagare(p, W, D, fam=fam, kohai_xs=xs)
    S = info["spec"]
    p.dim("pitch_deg", 24.2, math.degrees(math.atan(info["t"])), tol=0.1, source="PLAYBOOK §4 (board 4-5 sun (A))")
    p.dim("front_overhang_m", round(S["front"], 3), S["front"], source="kohai line (en + kizahashi) + 0.60")
    kf = info["kohai"]
    head = kf["beam"][0] + S["drop"]
    p.dim("kohai_beam_head_over_grade_m", ">=2.05", round(head, 3), source="PLAYBOOK D4 (head room at the stair foot)")
    p.dims[-1]["ok"] = head >= 2.05
    # head room over the en under the tie beams (rail inner face) and the rafters
    zr = KR.DEPTH - 0.10
    under = info["t"] * zr
    p.dim("en_head_under_rafters_m", ">=2.05", round(S["eave_y"] - under, 3), source="PLAYBOOK D4 / D5")
    p.dims[-1]["ok"] = S["eave_y"] - under >= 2.05
    for x, z in ((0, 0), (W, 0), (0, -D), (W, -D)):
        p.conn("post", (x, 0, z), note="body corner node")
    for x in xs:
        p.conn("post", (x, -S["drop"], round(S["kohai_z"], 4)), note="kohai post (grade)", hidden=True)
    p.conn("eave", (0, EAVE_Y, 0), note="keta top (eave line) on the front wall")
    a, b = info["ridge"]
    p.conn("ridge", a)
    p.conn("ridge", b)
    p.notes.append("Curve hook: nagare.nagare(..., curve=fn) hands nagare_spec(...) to fn(part, spec) (W2P2's sori).")
    return p


KOHAI_VARIANTS = {
    "_board": ("itabuki", "kohai step canopy (kokera) over a 1-ken stair bay of any hall front: a slope parallel to "
               "the hall's front slope, its top tucked under the main eave, verges with bargeboards, two posts, beam "
               "and tie beams (haiden, village halls)"),
    "_tile": ("sangawara", "kohai step canopy in sangawara for tiled temple halls (clay bed + fascia, T1)"),
}


def part_kohai(variant):
    fam, used = KOHAI_VARIANTS[variant]
    p = Part("jp_p_roof_kohai", variant, "roof", tiers=[1, 2, 3], used_for=used,
             recipe="nagare.kohai(part, xa, xb, z_post, main_t, main_ov, eave_y, fam, drop)",
             datum="hall front wall line z 0, the stair bay x 0..1.82; y 0 = hall floor (+0.60 above grade); the main "
                   "roof's front slope (pitch 0.45, overhang 0.90) is the shell's")
    drop = 0.60
    zp = KR.DEPTH + KR.stair_flight(drop)[0]
    main_ov = R.EAVE_OV[fam]
    sl, info = kohai(p, 0.0, KEN, zp, R.PITCH[fam], main_ov, EAVE_Y, fam, drop)
    head = info["frame"]["beam"][0] + drop
    p.dim("kohai_beam_head_over_grade_m", ">=2.05", round(head, 3), source="PLAYBOOK D4")
    p.dims[-1]["ok"] = head >= 2.05
    h_top = R.STACK[fam] + (0.05 if fam in ("sangawara", "hongawara") else 0.012)
    tuck_gap = min((EAVE_Y - R.PITCH[fam] * z) - (sl.y(0.0, z, 0.0) + h_top)
                   for z in (info["top_z"], (info["top_z"] + main_ov) / 2, main_ov))
    p.dim("tuck_under_main_roof_m", ">=0.02", round(tuck_gap, 3), source="PLAYBOOK §15 T8 (no roof poke, C12)")
    p.dims[-1]["ok"] = tuck_gap >= 0.02
    for x in (0.0, KEN):
        p.conn("post", (x, 0, 0), note="hall front post (tie beam end)")
        p.conn("post", (x, -drop, round(zp, 4)), note="kohai post (grade)", hidden=True)
    p.conn("eave", (0, EAVE_Y, 0), note="the hall's keta top on the front wall")
    return p


HOGYO_VARIANTS = {
    "_board_2ken": (2 * KEN, "itabuki", "hoju_bronze", "hogyo pyramid roof, kokera, over a 2 x 2 ken hall (Jizo-do, "
                    "Kannon-do, village do), bronze-type hoju (iron stand-in)"),
    "_tile_3ken": (3 * KEN, "sangawara", "hoju_kawara", "hogyo roof in sangawara over a 3 x 3 ken hall, tile hip "
                   "ridges, tile hoju"),
    "_thatch_2ken": (2 * KEN, "thatch", "hoju_kawara", "thatched hogyo (rural do) with a tile cap and hoju"),
}


def part_hogyo(variant):
    W, fam, apex, used = HOGYO_VARIANTS[variant]
    p = Part("jp_p_roof_forms_hogyo", variant, "roof", tiers=[1, 2, 3], used_for=used,
             recipe="nagare.hogyo(part, W, fam, apex)",
             datum="square footprint x 0..W, z 0 .. -W; y 0 = floor; eave line 2.88")
    if fam == "thatch":
        sls, info = _hogyo_thatch(p, W)
    else:
        sls, info = hogyo(p, W, fam, apex=apex)
    p.dim("pitch_deg", 45.0 if fam == "thatch" else 24.2, math.degrees(math.atan(info["t"])), tol=0.1)
    for x, z in ((0, 0), (W, 0), (0, -W), (W, -W)):
        p.conn("post", (x, 0, z), note="footprint corner node")
    p.conn("apex", info["apex"])
    return p


def _hogyo_thatch(part, W):
    """Thatched hogyo: roofs.roof's thatch coverings on the four pyramid slopes, hip rolls, a tile apex cap + hoju."""
    t = R.PITCH["thatch"]
    ov = R.EAVE_OV["thatch"]
    sls = R.slopes_for(W, W, "yosemune", EAVE_Y, t, ov, ov)
    for sl in sls:
        R.cover_thatch(part, sl)
        R.rafters(part, sl, spacing=0.303, round_=True, only_eave=False, vis=(1,))
        for pc in sl.pieces:
            part.add(slab(pc, lambda x, z, s_=sl: s_.y(x, z, 0.055), lambda x, z, s_=sl: s_.y(x, z, 0.06),
                          "bamboo_weathered", vis=(1, 2), tag="lath", uvscale=(0.5, 0.5)))
    h = W / 2
    stack_top = R.STACK["thatch"] + 0.60
    for (e, tp) in R.hip_lines(sls, W, W, "yosemune", ov):
        p0 = (tp[0], R._hip_y(sls, tp, stack_top) - 0.08, tp[1])
        p1 = (e[0], R._hip_y(sls, e, stack_top) - 0.10, e[1])
        d = norm(tuple(p1[k] - p0[k] for k in range(3)))
        part.add(tube(add(p0, mul(d, 0.30)), p1, 0.26, "roof_thatch", n=8, vis=(1, 2), tag="hip_roll",
                      uvscale=(2.0, 2.0)))
    ya = EAVE_Y + t * h + stack_top
    from .core import Solid
    cw, yc = 0.55, ya - 0.20
    verts = [(h - cw, yc - 0.30, -h - cw), (h + cw, yc - 0.30, -h - cw), (h + cw, yc - 0.30, -h + cw),
             (h - cw, yc - 0.30, -h + cw), (h - 0.16, yc + 0.12, -h - 0.16), (h + 0.16, yc + 0.12, -h - 0.16),
             (h + 0.16, yc + 0.12, -h + 0.16), (h - 0.16, yc + 0.12, -h + 0.16)]
    part.add(Solid(verts, [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]],
                   "roof_kawara", vis=(1, 2, 3), tag="apex_cap"))
    from . import ornament as ORN
    top = ORN.hoju(part, (h, yc + 0.12, -h), kind="hoju_kawara")
    info = {"t": t, "ov": ov, "form": "hogyo", "fam": "thatch", "apex": (h, yc + 0.12, -h), "finial_top": top}
    part.meta.setdefault("roof", info)
    return sls, info


def register(reg):
    reg("jp_p_roof_nagare", list(NAGARE_VARIANTS), part_nagare)
    reg("jp_p_roof_kohai", list(KOHAI_VARIANTS), part_kohai)
    reg("jp_p_roof_forms_hogyo", list(HOGYO_VARIANTS), part_hogyo)
