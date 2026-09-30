"""Koyagumi: the visible roof framing of rooms open to the roof (B2 part 1, jp_p_frame_koyagumi; PARTS_GAP_AUDIT §3
part 1, §5 part 1). It reads a roof from the generator (roofs.roof(part, W, D, form, family) -> (slopes, info)) and
frames the space under it, so the room shows beams, struts, purlins and rafters instead of a flat sheathing slab.

    sls, info = roofs.roof(rp, W, D, "yosemune", "thatch", eave_y=ey)
    K = koyagumi.koyagumi(rp, W, D, info, eave_y=ey, geya=(KEN, KEN), members="log")

Frame: the roof's (roofs.py docstring): x 0..W along the ridge, z 0 = front wall line .. -D = back wall line, y 0 =
floor. Pass the ROOF part itself as `part`: the continued rafters lie inside the roof body (rafter underside plane up
to the covering), and the C12 roof-poke check only allows that for solids of the roof's own sub-part.

Two systems, by covering (PLAYBOOK §6.1; BUILDING_LIST 'big smoke-black beams', 'open to soot-black thatch'):
  wagoya (tile / board roofs): tie beams (koyabari) across the span on every frame line, struts (koyazuka) on them
      carrying purlins (moya) every half ken up the slope and the ridge beam (munagi), longitudinal ties (koyanuki), and
      the rafters (taruki) continued from the eave soffit to the ridge. Hipped forms add hip rafters (sumigi), the end
      purlins and a short end beam carrying their struts.
  sasu (thatch): A-frame pairs of round poles (sasu) on the tie-beam ends, crossed and lashed at the ridge with the
      ridge pole (munagi) in the crotch, round purlins on the sasu; the rafters and bamboo lath are the roof's own.
      Hipped forms add hip and end sasu.
The joya / geya split (G1 A1 ruling 4: the 3-ken span rule is urban-only; farmhouses carry their aisles under one
sweeping roof): geya=(front, back) aisle depths. The joya (core) then has its own posts (joya-bashira) on the aisle
lines, a plate (keta) on them under the rafters, and the big tie beams (ushibari) across the core; low aisle beams
(geya-bari) tie the outer wall heads to the joya posts. The roof itself stays ONE plane per side from the outer eave
to the ridge (roofs.roof on the full W x D).

Members: 'sawn' (squared, town and work buildings) or 'log' (round, cambered ushibari, farmhouses and huts).
Wear: materials at the instance's wear (_w0 / _w1 / _w2, core.Part.wear) or soot=True: the sooted level (W5; kitchens,
farmhouses with an irori, smithies), which also re-materials the roof's inside faces (rafters, lath, sheathing,
thatch underside) with soot_roof().
Frame lines: every `bay` (default 1 ken) strictly inside the roof's length; ends=True also frames the two end lines of
a kirizuma roof (open gables: sheds, the test pavilion). Gable and hip-end WALLS keep their own tie beams.
"""
import math

from .core import Part, box, hexa, KEN, HALF, EAVE_Y, KETA_H, add, sub, mul, norm, cross
from .shapes import tube, oriented_box, frame_of
from . import roofs as R

SOOT = {"wood_weathered": "wood_sooted", "bamboo_weathered": "bamboo_sooted", "wood_street_dark": "wood_sooted"}
SOOT_TAGS = ("rafter", "lath", "sheathing", "thatch_body", "pole_rafter", "lath_lod", "eave_stack", "hafu")

# member sections (m): squared 'sawn' and round 'log' (radius); sasu poles, purlins and lashings
SAWN = {"beam": (0.15, 0.27), "geya_beam": (0.12, 0.21), "plate": (0.12, 0.18), "purlin": (0.105, 0.105),
        "strut": 0.105, "ridge": (0.12, 0.15), "nuki": (0.021, 0.09), "post": 0.18, "hip": (0.12, 0.15)}
LOG = {"beam": 0.15, "geya_beam": 0.11, "plate": 0.10, "purlin": 0.06, "strut": 0.065, "ridge": 0.09, "post": 0.18,
       "hip": 0.08}
SASU = {"sasu": 0.075, "moya": 0.045, "ridge": 0.075, "rope": 0.10}
CAMBER = 0.06          # rise of a cambered log tie beam (ushibari) at mid span, per 3 ken


def sooted(m, soot):
    return SOOT.get(m, m) if soot else m


def soot_solid(s):
    """Re-material one (finalized) solid to the sooted level and resolve its faces again (UVs follow the new tile)."""
    if isinstance(s.mats, str):
        s.mats = SOOT.get(s.mats, s.mats)
    else:
        s.mats = {k: SOOT.get(v, v) for k, v in s.mats.items()}
    if s.fm is not None:
        s.fm = None
        s.finalize()
    return s


def soot_roof(part, tags=SOOT_TAGS):
    """The sooted wear level for the roof above a koyagumi: every inside-facing roof solid (rafters, lath, sheathing,
    the thatch underside, eave soffits) goes wood / bamboo sooted. Returns the number of solids changed."""
    n = 0
    for s in part.solids:
        if s.tag in tags:
            soot_solid(s)
            n += 1
    return n


# ------------------------------------------------------------------------------------------------ slope geometry
def _pt(sl, u, s):
    """Plan point on slope sl at u (along its eave) and s (inward from its wall line)."""
    ex, ez = sl.eave_point(u)
    d = s + sl.ov
    return (ex + sl.inw[0] * d, ez + sl.inw[1] * d)


def _y(sl, x, z, off=0.0):
    """Rafter underside plane of slope sl at (x, z), plus a vertical offset."""
    return sl.y(x, z, off)


def line_range(sl, s, fp=None, margin=0.0):
    """u interval of the line 'inward distance s' on slope sl inside the slope's pieces (and inside the plan box
    fp = (x0, x1, z0, z1)), shrunk by margin at both ends. None if empty."""
    lo, hi = None, None
    ex0, ez0 = _pt(sl, 0.0, s)
    ux, uz = sl.udir
    for pc in sl.pieces:
        a0, a1 = -1e9, 1e9
        n = len(pc)
        ok = True
        for i in range(n):
            ax, az = pc[i]
            bx, bz = pc[(i + 1) % n]
            # inside: (bx-ax)*(z-az) - (bz-az)*(x-ax) >= 0 with x = ex0 + ux u, z = ez0 + uz u
            c0 = (bx - ax) * (ez0 - az) - (bz - az) * (ex0 - ax)
            c1 = (bx - ax) * uz - (bz - az) * ux
            if abs(c1) < 1e-12:
                if c0 < -1e-9:
                    ok = False
                    break
                continue
            r = -c0 / c1
            if c1 > 0:
                a0 = max(a0, r)
            else:
                a1 = min(a1, r)
        if ok and a1 > a0 + 1e-6:
            lo = a0 if lo is None else min(lo, a0)
            hi = a1 if hi is None else max(hi, a1)
    if lo is None:
        return None
    if fp:
        for (k, v, sg) in ((0, fp[0], 1), (0, fp[1], -1), (1, fp[2], 1), (1, fp[3], -1)):
            p0 = (ex0, ez0)[k]
            d = (ux, uz)[k]
            if abs(d) < 1e-12:
                if sg * (p0 - v) < -1e-9:
                    return None
                continue
            r = (v - p0) / d
            if sg * d > 0:
                lo = max(lo, r)
            else:
                hi = min(hi, r)
    lo, hi = lo + margin, hi - margin
    return (lo, hi) if hi > lo + 0.05 else None


def s_extent(sl, x_or_u, is_u=False):
    """How far inward (from the wall line) slope sl reaches at u (the ridge, or a hip line)."""
    return sl.depth_at(x_or_u) - sl.ov


def roof_under(sls, x, z):
    """Rafter underside of the roof over the plan point (x, z): the slope whose piece contains it (None outside)."""
    ys = []
    for sl in sls:
        for pc in sl.pieces:
            if R._inside(pc, x, z, 1e-6):
                ys.append(sl.y(x, z, 0.0))
                break
    return min(ys) if ys else None


# ------------------------------------------------------------------------------------------------ members
def under_member(part, sl, s, u0, u1, w, h, mat, drop=0.0, vis=(1, 2), geo=False, tag="moya"):
    """A squared member along slope sl's eave direction at inward distance s, from u0 to u1: its top face lies IN the
    rafter plane (minus drop), bottom horizontal h under the top's low edge (convex hexahedron)."""
    c = []
    for (uu, ds) in ((u0, -w / 2), (u1, -w / 2), (u1, w / 2), (u0, w / 2)):
        x, z = _pt(sl, uu, s + ds)
        c.append((x, z))
    ylow = min(sl.y(x, z, -drop) for x, z in c) - h
    bot = [(x, ylow, z) for x, z in c]
    top = [(x, sl.y(x, z, -drop), z) for x, z in c]
    return part.add(hexa(bot + top, mat, vis=vis, geo=geo, view=geo, fire=True if geo else None, tag=tag, grain="long"))


def round_under(part, sl, s, u0, u1, r, mat, gap=0.0, vis=(1, 2), n=6, geo=False, tag="moya"):
    """A round member (pole) along slope sl at inward distance s, tangent under the rafter plane (+gap)."""
    x0, z0 = _pt(sl, u0, s)
    x1, z1 = _pt(sl, u1, s)
    dv = (r + gap) / sl.cos
    return part.add(tube((x0, sl.y(x0, z0, -dv), z0), (x1, sl.y(x1, z1, -dv), z1), r, mat, n=n, vis=vis, geo=geo,
                         view=geo, fire=True if geo else None, tag=tag))


def cross_beam(part, x, z0, z1, ytop, sec, members, mat, vis=(1, 2), tag="hari", camber=0.0):
    """A tie beam across the span (along z) on the frame line x, top at ytop: squared (sec = (w, h)) or a round log
    (sec = radius) that rises by `camber` at mid span (two straight halves, each a convex component)."""
    za, zb = max(z0, z1), min(z0, z1)
    if members == "sawn":
        w, h = sec
        return [part.add(box(x - w / 2, x + w / 2, ytop - h, ytop, zb, za, mat, vis=vis, geo=True, view=True, fire=True,
                             tag=tag))]
    r = sec
    yc = ytop - r * 0.92
    if camber <= 1e-4:
        return [part.add(tube((x, yc, za), (x, yc, zb), r, mat, n=10, vis=vis, geo=True, view=True, fire=True, tag=tag,
                              squash=0.92))]
    zm = (za + zb) / 2
    return [part.add(tube((x, yc, za), (x, yc + camber, zm), r, mat, n=10, vis=vis, geo=True, view=True, fire=True,
                          tag=tag, squash=0.92)),
            part.add(tube((x, yc + camber, zm), (x, yc, zb), r, mat, n=10, vis=vis, geo=True, view=True, fire=True,
                          tag=tag, squash=0.92))]


def along_beam(part, z, x0, x1, ytop, sec, members, mat, vis=(1, 2), tag="hari", geo=True):
    if members == "sawn":
        w, h = sec
        return part.add(box(x0, x1, ytop - h, ytop, z - w / 2, z + w / 2, mat, vis=vis, geo=geo, view=geo,
                            fire=True if geo else None, tag=tag))
    r = sec
    return part.add(tube((x0, ytop - r * 0.92, z), (x1, ytop - r * 0.92, z), r, mat, n=10, vis=vis, geo=geo,
                         view=geo, fire=True if geo else None, tag=tag, squash=0.92))


def strut(part, x, z, y0, y1, members, mat, vis=(1, 2), tag="tsuka"):
    if y1 - y0 < 0.04:
        return None
    if members == "sawn":
        a = SAWN["strut"] / 2
        return part.add(box(x - a, x + a, y0, y1, z - a, z + a, mat, vis=vis, tag=tag, grain="long"))
    return part.add(tube((x, y0, z), (x, y1, z), LOG["strut"], mat, n=7, vis=vis, tag=tag))


def post(part, x, z, y0, y1, members, mat, size=None, tag="joya_post"):
    a = (size or SAWN["post"]) / 2
    if members == "sawn":
        return part.add(box(x - a, x + a, y0, y1, z - a, z + a, mat, vis=(1, 2, 3), geo=True, view=True, fire=True,
                            tag=tag, grain="long"))
    # an adzed farmhouse post: octagon-chamfered square (convex)
    c = 0.025
    poly = [(x - a + c, z - a), (x + a - c, z - a), (x + a, z - a + c), (x + a, z + a - c), (x + a - c, z + a),
            (x - a + c, z + a), (x - a, z + a - c), (x - a, z - a + c)]
    from .core import prism
    return part.add(prism(poly, "y", y0, y1, mat, vis=(1, 2, 3), geo=True, view=True, fire=True, tag=tag,
                          grain="long"))


def purlin_bottom(t, yr, s, members):
    """Underside of the wagoya purlin at inward distance s (under_member / round_under geometry)."""
    if members == "sawn":
        w, hh = SAWN["purlin"]
        return yr(s - w / 2) - hh
    r = LOG["purlin"]
    return yr(s) - r / math.cos(math.atan(t)) - r


def pole(part, p0, p1, r, mat, vis=(1, 2), n=8, geo=False, tag="sasu"):
    return part.add(tube(p0, p1, r, mat, n=n, vis=vis, geo=geo, view=geo, fire=True if geo else None, tag=tag))


# ------------------------------------------------------------------------------------------------ the generator
def koyagumi(part, W, D, info, eave_y=EAVE_Y, system=None, members="sawn", geya=(0.0, 0.0), bay=KEN, ends=False,
             joya_posts=True, floor_y=0.0, outer_plates=False, soot=False, rafters=True, rafters_from="eave",
             moya_step=None, nuki=True, xs=None):
    """Frame the roof described by `info` (roofs.roof's info dict: t, ov, gov, form, fam) over x 0..W, z 0..-D, eave
    line (keta top) at eave_y. Adds everything to `part` (pass the roof Part, see the module docstring). Returns a
    dict: system, members, frame lines, post nodes [(x, z, y0, y1)], levels, member counts."""
    t, ov, gov, form, fam = info["t"], info["ov"], info["gov"], info["form"], info["fam"]
    system = system or ("sasu" if fam == "thatch" else "wagoya")
    if system not in ("wagoya", "sasu"):
        raise ValueError("system %r: wagoya or sasu" % system)
    if members not in ("sawn", "log"):
        raise ValueError("members %r: sawn or log" % members)
    sls = R.slopes_for(W, D, form, eave_y, t, ov, gov)
    S = {sl.name: sl for sl in sls}
    F, B = S["front"], S["back"]
    h = D / 2
    gf, gb = geya
    if gf + gb > D - KEN + 1e-6:
        raise ValueError("geya %s leave less than 1 ken of joya in a %.2f span" % (geya, D))
    m_wood = sooted("wood_weathered", soot)
    m_bamboo = sooted("bamboo_weathered", soot)
    m_rope = "straw_rope"
    SEC = SAWN if members == "sawn" else LOG
    cos = F.cos
    fp = (-0.07, W + 0.07, -D - 0.07, 0.07)             # plan box of the walls (members stay inside it)
    yr = lambda s: eave_y + t * s                        # noqa: E731  rafter underside at s in from a wall line
    out = {"system": system, "members": members, "form": form, "geya": [gf, gb], "posts": [], "counts": {}}
    cnt = out["counts"]

    def bump(k, n=1):
        cnt[k] = cnt.get(k, 0) + n

    # frame lines: every bay inside the roof's length (+ the end lines of an open-gable kirizuma)
    if xs is None:
        xs = []
        k = 1
        while k * bay < W - 0.30:
            xs.append(round(k * bay, 4))
            k += 1
        if ends and form == "kirizuma":
            xs = [0.0] + xs + [W]
    out["frame_lines"] = xs

    def reach(sl, x):
        """How far in from its wall line slope sl (front / back) reaches on the frame line x (the ridge, or a hip)."""
        return sl.depth_at(sl.u_of(x, 0.0)) - ov

    def side_z(side, s):
        return -s if side == "front" else -D + s

    sj = {"front": gf, "back": gb}
    plate_top = {sd: yr(sj[sd]) for sd in ("front", "back")}          # joya plate top (touches the rafters)
    seat = {sd: yr(sj[sd]) - KETA_H for sd in ("front", "back")}       # beam top / plate underside on that line
    y_beam = min(seat.values())                                        # main tie beam top (horizontal)
    y_geya = eave_y - KETA_H                                           # aisle beam top = outer keta underside
    out["levels"] = {"eave": eave_y, "beam_top": round(y_beam, 3), "geya_beam_top": round(y_geya, 3),
                     "joya_plate_top": {k: round(v, 3) for k, v in plate_top.items()}, "floor": floor_y}

    # ------------------------------------------------------------------ outer plates (sample context only)
    if outer_plates:
        for sl in sls:
            rg = line_range(sl, 0.0, (-0.30, W + 0.30, -D - 0.30, 0.30)) if sl.name in ("front", "back") else \
                line_range(sl, 0.0, (-0.07, W + 0.07, -D - 0.07, 0.07))
            if rg:
                under_member(part, sl, 0.0, rg[0], rg[1], 0.12, KETA_H - 0.0, m_wood, drop=0.0, vis=(1, 2, 3),
                             geo=True, tag="keta")
                bump("keta")

    # ------------------------------------------------------------------ joya: plates, posts, aisle beams
    for sd, sl in (("front", F), ("back", B)):
        if sj[sd] <= 1e-6:
            continue
        rg = line_range(sl, sj[sd], fp, margin=0.0)
        if rg:
            if members == "sawn":
                under_member(part, sl, sj[sd], rg[0], rg[1], SAWN["plate"][0], SAWN["plate"][1], m_wood,
                             vis=(1, 2), geo=True, tag="joya_plate")
            else:
                round_under(part, sl, sj[sd], rg[0], rg[1], LOG["plate"], m_wood, n=8, geo=True, tag="joya_plate")
            bump("joya_plate")
        z = side_z(sd, sj[sd])
        lines = list(xs)
        if rg:                                     # the plate's own ends (hip corners) stand on posts too
            for uu in rg:
                xx, _ = _pt(sl, uu, sj[sd])
                xx = round(xx / HALF) * HALF
                if all(abs(xx - q) > 0.2 for q in lines) and 0.0 < xx < W:
                    lines.append(xx)
        for x in sorted(lines):
            if joya_posts:
                post(part, x, z, floor_y, seat[sd], members, m_wood)
                out["posts"].append((x, z, floor_y, seat[sd]))
                bump("joya_post")
            # aisle beam from the outer wall head into the joya post
            z_out = 0.06 if sd == "front" else -D - 0.06
            if x in xs:
                cross_beam(part, x, z_out, z, y_geya, SEC["geya_beam"], members, m_wood, tag="geya_bari")
                bump("geya_bari")

    # ------------------------------------------------------------------ main tie beams on the frame lines
    zf = -gf + (SAWN["post"] / 2 if gf > 0 else 0.06)
    zb = -D + gb - (SAWN["post"] / 2 if gb > 0 else 0.06)
    span_ken = (zf - zb) / KEN
    for x in xs:
        cross_beam(part, x, zf, zb, y_beam, SEC["beam"], members, m_wood, tag="ushibari" if members == "log" else "hari",
                   camber=CAMBER * span_ken / 3 if members == "log" else 0.0)
        bump("tie_beam")

    def beam_top(sd, s):
        return y_beam if s >= sj[sd] - 1e-6 else y_geya

    # ------------------------------------------------------------------ WAGOYA
    if system == "wagoya":
        step = moya_step or HALF
        struts_by_s = {}
        for sd, sl in (("front", F), ("back", B)):
            s = step
            while s < h - 0.25:
                if abs(s - sj[sd]) > 0.10:
                    rg = line_range(sl, s, fp, margin=0.05)
                    if rg:
                        ps = SAWN["purlin"]
                        if members == "sawn":
                            under_member(part, sl, s, rg[0], rg[1], ps[0], ps[1], m_wood, tag="moya")
                        else:
                            round_under(part, sl, s, rg[0], rg[1], LOG["purlin"], m_wood, n=7, tag="moya")
                        bump("moya")
                        xa, _ = _pt(sl, rg[0], s)
                        xb, _ = _pt(sl, rg[1], s)
                        x_lo, x_hi = min(xa, xb), max(xa, xb)
                        z = side_z(sd, s)
                        ytop = purlin_bottom(t, yr, s, members)
                        for x in xs:
                            if x_lo + 0.05 <= x <= x_hi - 0.05:
                                if strut(part, x, z, beam_top(sd, s), ytop, members, m_wood):
                                    bump("tsuka")
                                    struts_by_s.setdefault((sd, round(s, 3)), []).append((x, beam_top(sd, s), ytop))
                s += step
        # ridge beam + ridge struts
        if form == "kirizuma":
            xr0, xr1 = -0.06, W + 0.06
        else:
            xr0, xr1 = info["ridge"][0][0], info["ridge"][1][0]
        yrt = yr(h)
        rw, rh = SAWN["ridge"] if members == "sawn" else (2 * LOG["ridge"], 2 * LOG["ridge"])
        if members == "sawn":
            from .core import prism
            sec = [(-h - rw / 2, yrt - rh - t * rw / 2), (-h + rw / 2, yrt - rh - t * rw / 2),
                   (-h + rw / 2, yrt - t * rw / 2), (-h, yrt), (-h - rw / 2, yrt - t * rw / 2)]
            part.add(prism([(y, z) for z, y in sec][::-1], "x", xr0, xr1, m_wood, vis=(1, 2), geo=True, view=True,
                           fire=True, tag="munagi", grain="long"))
        else:
            pole(part, (xr0, yrt - LOG["ridge"] / cos, -h), (xr1, yrt - LOG["ridge"] / cos, -h), LOG["ridge"], m_wood,
                 n=10, geo=True, tag="munagi")
        bump("munagi")
        ridge_struts = []
        for x in xs:
            if xr0 + 0.05 <= x <= xr1 - 0.05:
                if strut(part, x, -h, y_beam, yrt - rh - t * rw / 2, members, m_wood, tag="munazuka"):
                    bump("munazuka")
                    ridge_struts.append((x, y_beam, yrt - rh))
        struts_by_s[("ridge", round(h, 3))] = ridge_struts
        # longitudinal ties (koyanuki) through the struts of one line, at mid height
        if nuki:
            for key, ss in struts_by_s.items():
                if len(ss) < 2:
                    continue
                hgt = min(y1 - y0 for _, y0, y1 in ss)
                if hgt < 0.55:
                    continue
                z = -h if key[0] == "ridge" else side_z(key[0], key[1])
                yy = min(y0 for _, y0, _ in ss) + hgt * 0.5
                nw, nh = SAWN["nuki"]
                part.add(box(ss[0][0] - 0.10, ss[-1][0] + 0.10, yy - nh / 2, yy + nh / 2, z - nw / 2, z + nw / 2,
                             m_wood, vis=(1,), tag="koyanuki", grain="long"))
                bump("koyanuki")
        # hipped forms: hip rafters, end purlins, end beams + struts
        if form != "kirizuma":
            _hips_wagoya(part, sls, S, W, D, info, eave_y, t, members, m_wood, xs, y_beam, fp, step, bump)
        # the rafters continued from the eave soffit to the ridge (inside the roof body: pass the roof part)
        if rafters:
            for sl in sls:
                d0 = sl.ov + 0.25 if rafters_from == "eave" else sl.ov + 0.03
                R.rafters(part, sl, spacing=0.303, only_eave=False, mat=m_wood, vis=(1,), d_start=d0, tag="rafter_in")
            bump("rafter_runs", len(sls))
    # ------------------------------------------------------------------ SASU
    else:
        rs, rm = SASU["sasu"], SASU["moya"]
        d = 2 * rm + rs + 0.004                           # sasu axis below the rafter plane (perpendicular)
        step = moya_step or 0.60
        ext = 0.30                                        # crossed tips past the ridge (inside the thatch)
        for x in xs:
            full = reach(F, x) >= h - 1e-3 and reach(B, x) >= h - 1e-3
            for sd, sl, off in (("front", F, -rs * 1.02), ("back", B, rs * 1.02)):
                s_top = reach(sl, x)
                if s_top < sj[sd] + 0.4:
                    continue
                s_foot = max(sj[sd], (seat[sd] + 0.5 * rs + d / cos - eave_y) / t)
                s_end = h + ext if full else s_top - 0.10
                xx = x + off if full else x
                p0 = (xx, yr(s_foot) - d / cos, side_z(sd, s_foot))
                p1 = (xx, yr(s_end) - d / cos, side_z(sd, s_end))
                pole(part, p0, p1, rs, m_wood, n=8, geo=True, tag="sasu")
                bump("sasu")
            if full:
                # the crossing, lashed with straw rope
                yc = yr(h) - d / cos
                part.add(box(x - 0.17, x + 0.17, yc - 0.10, yc + 0.10, -h - 0.09, -h + 0.09, m_rope, vis=(1,),
                             tag="lashing"))
                bump("lashing")
        # ridge pole in the crotch (tangent under both rafter planes)
        if form == "kirizuma":
            xr0, xr1 = -0.06, W + 0.06
        else:
            xr0, xr1 = info["ridge"][0][0] + 0.02, info["ridge"][1][0] - 0.02
        yrp = yr(h) - SASU["ridge"] / cos
        pole(part, (xr0, yrp, -h), (xr1, yrp, -h), SASU["ridge"], m_wood, n=8, geo=True, tag="munagi")
        bump("munagi")
        # purlins (moya) on the sasu, both long slopes, then the hip / end slopes
        for sd, sl in (("front", F), ("back", B)):
            s_foot = max(sj[sd], (seat[sd] + 0.5 * rs + d / cos - eave_y) / t)
            s = s_foot + 0.30
            while s < h - 0.20:
                rg = line_range(sl, s, fp, margin=0.06)
                if rg:
                    round_under(part, sl, s, rg[0], rg[1], rm, m_wood, n=6, tag="moya")
                    bump("moya")
                s += step
        if form != "kirizuma":
            _hips_sasu(part, sls, S, W, D, info, eave_y, t, m_wood, sj, seat, d, rs, rm, step, fp, bump)

    out["slopes"] = [sl.name for sl in sls]
    part.meta.setdefault("koyagumi", {k: v for k, v in out.items() if k != "posts"})
    return out


def _hips_wagoya(part, sls, S, W, D, info, eave_y, t, members, m_wood, xs, y_beam, fp, step, bump):
    """Hip rafters (sumigi) under the hip lines, purlins on the end slopes, and a short end beam (tsunagi) along the
    ridge line from each hipped end wall to the first frame line, with struts under the end purlins."""
    h = D / 2
    for (e, tp) in R.hip_lines(sls, W, D, info["form"], info["ov"]):
        # from the wall corner (the hip line's point nearest the eave corner inside the walls) to the hip top
        corner = min(((0.0, 0.0), (W, 0.0), (0.0, -D), (W, -D)), key=lambda c: math.dist(c, e))
        ya = eave_y
        sl = next(s for s in sls if s.name in ("left", "right") and any(math.dist(tp, q) < 1e-6 for q in s.poly))
        yb = sl.y(tp[0], tp[1], 0.0)
        a = (corner[0], ya, corner[1])
        b = (tp[0], yb, tp[1])
        dv, e1, e2 = frame_of(sub(b, a))
        up = e2 if e2[1] > 0 else mul(e2, -1.0)
        hw, hh = SAWN["hip"]
        c = add(mul(add(a, b), 0.5), mul(up, -hh / 2 - 0.01))
        part.add(oriented_box(c, dv, up, norm(cross(dv, up)), math.dist(a, b) / 2, hh / 2, hw / 2, m_wood, vis=(1, 2),
                              tag="sumigi", grain="long"))
        bump("sumigi")
    ends = [sl for sl in sls if sl.name in ("left", "right")]
    for sl in ends:
        # end purlins at s = k * step in from the end wall, up to the top of the hip slope
        top = max(sl.s(x, z) for x, z in sl.poly)
        s = step
        while s < top - 0.10:
            rg = line_range(sl, s, fp, margin=0.08)
            if rg:
                ps = SAWN["purlin"]
                if members == "sawn":
                    under_member(part, sl, s, rg[0], rg[1], ps[0], ps[1], m_wood, tag="moya")
                else:
                    round_under(part, sl, s, rg[0], rg[1], LOG["purlin"], m_wood, n=7, tag="moya")
                bump("moya")
            s += step
        # the end beam along the ridge line, from the end wall to the first frame line, and struts on it
        if not xs:
            continue
        left = sl.name == "left"
        xa = -0.06 if left else W + 0.06
        xb = xs[0] if left else xs[-1]
        along_beam(part, -h, min(xa, xb), max(xa, xb), y_beam, SAWN["beam"] if members == "sawn" else LOG["beam"],
                   members, m_wood, tag="tsunagi")
        bump("tsunagi")
        s = step
        while s < min(top, abs(xb - xa)) - 0.10:
            x = s if left else W - s
            ytop = purlin_bottom(t, lambda q: eave_y + t * q, s, members)
            if strut(part, x, -h, y_beam, ytop, members, m_wood):
                bump("tsuka")
            s += step


def _hips_sasu(part, sls, S, W, D, info, eave_y, t, m_wood, sj, seat, d, rs, rm, step, fp, bump):
    """Hip sasu under each hip line (from the joya plate corner, or the wall corner, to the hip top), an end sasu up
    the middle of each fully hipped end, and round purlins on the end slopes."""
    h = D / 2
    cos = S["front"].cos
    form = info["form"]
    yr = lambda s: eave_y + t * s                    # noqa: E731
    for (e, tp) in R.hip_lines(sls, W, D, form, info["ov"]):
        corner = min(((0.0, 0.0), (W, 0.0), (0.0, -D), (W, -D)), key=lambda c: math.dist(c, e))
        side = "front" if abs(corner[1]) < 1e-6 else "back"
        L = math.dist(corner, tp)                    # plan length of the hip inside the walls
        s_top = abs(tp[1] - corner[1])               # the hip top's s from the long wall (45 deg hips: = along x)
        s0 = max(sj[side], (seat[side] + 0.5 * rs + d / cos - eave_y) / t)
        if s_top - s0 < 0.4:
            continue
        f0, f1 = s0 / s_top, min(1.0, (s_top + 0.12) / s_top)
        pa = (corner[0] + (tp[0] - corner[0]) * f0, corner[1] + (tp[1] - corner[1]) * f0)
        pb = (corner[0] + (tp[0] - corner[0]) * f1, corner[1] + (tp[1] - corner[1]) * f1)
        pole(part, (pa[0], yr(s0) - d / cos, pa[1]), (pb[0], yr(s_top * f1) - d / cos, pb[1]), rs, m_wood, n=8,
             geo=True, tag="sumi_sasu")
        bump("sumi_sasu")
    for sl in [s for s in sls if s.name in ("left", "right")]:
        left = sl.name == "left"
        top = max(sl.s(x, z) for x, z in sl.poly)
        full_hip = form == "yosemune" or (form == "kabuto" and not left)
        if full_hip:
            s0 = (eave_y - KETA_H + 0.5 * rs + d / cos - eave_y) / t
            s1 = top + 0.12
            x0, x1 = (s0, s1) if left else (W - s0, W - s1)
            pole(part, (x0, yr(s0) - d / cos, -h), (x1, yr(s1) - d / cos, -h), rs, m_wood, n=8, geo=True,
                 tag="tsuma_sasu")
            bump("tsuma_sasu")
        s = 0.45
        while s < top - 0.15:
            rg = line_range(sl, s, fp, margin=0.06)
            if rg:
                round_under(part, sl, s, rg[0], rg[1], rm, m_wood, n=6, tag="moya")
                bump("moya")
            s += step


# ------------------------------------------------------------------------------------------------ the part variants
VARIANTS = {
    # variant: (W ken, D ken, form, covering, system, members, geya ken (front, back), soot, used for, tiers)
    "_wagoya": (4, 3, "kirizuma", "sangawara", "wagoya", "sawn", (0, 0), False,
                "tile / board roof framing of rooms open to the roof: kuri kitchens, workshops, smithy, sake and soy "
                "works (TR09-TR24), the shed; sawn beams, struts, purlins, ridge beam, rafters to the ridge", [2, 3]),
    "_wagoya_log": (3, 3, "kirizuma", "itabuki", "wagoya", "log", (0, 0), False,
                    "rustic framing of barns, sheds and work buildings (DW24, TR-S): round log tie beams, round struts "
                    "and purlins under a board roof", [1, 2]),
    "_wagoya_hip": (4, 3, "yosemune", "sangawara", "wagoya", "sawn", (0, 0), False,
                    "hipped tile roof framing (inns, big houses, temple kuri): hip rafters, end purlins, end beams",
                    [2, 3]),
    "_sasu": (3, 2, "kirizuma", "thatch", "sasu", "log", (0, 0), False,
              "poor hut / tenant house open to the thatch (DW01, DW30): sasu A-frames on log tie beams, crossed and "
              "lashed at the ridge, round purlins", [1]),
    "_sasu_sooted": (3, 2, "kirizuma", "thatch", "sasu", "log", (0, 0), True,
                     "the same hut, SOOTED wear level: 'no ceiling, open to soot-black thatch' (BUILDING_LIST §3 poor)",
                     [1]),
    "_sasu_geya": (7, 5, "yosemune", "thatch", "sasu", "log", (1, 1), False,
                   "Kanto farmhouse (DW06) and big thatch houses: JOYA core (3 ken) with its posts, plates and cambered "
                   "ushibari, GEYA aisles (1 ken) front and back under the same sweeping thatch slope (G1 A1-4)",
                   [1, 2]),
    "_sasu_geya_sooted": (7, 5, "yosemune", "thatch", "sasu", "log", (1, 1), True,
                          "the joya / geya farmhouse frame, SOOTED wear level (W5; Hida 'big smoke-black beams', "
                          "irori smoke)", [1, 2]),
}


def part_koyagumi(variant):
    Wk, Dk, form, fam, system, members, gk, soot, used, tiers = VARIANTS[variant]
    W, D = Wk * KEN, Dk * KEN
    p = Part("jp_p_frame_koyagumi", variant, "frame", tiers=tiers, used_for=used,
             recipe="koyagumi.koyagumi(roof_part, W, D, roofs.roof(...) info, eave_y, system, members, geya, soot)",
             datum="%d x %d ken footprint as the roof generator: x 0..%.2f along the ridge, z 0 (front wall line) .. "
                   "%.2f; y 0 = floor, eave line (keta top) 2.88. The sample carries the outer keta (outer_plates) "
                   "for context; buildings pass outer_plates=False (their walls own the keta)" % (Wk, Dk, W, -D))
    info = {"t": R.PITCH[fam], "ov": R.EAVE_OV[fam], "gov": R.GABLE_OV[fam], "form": form, "fam": fam}
    if form != "kirizuma":
        info["ridge"] = (({"yosemune": D / 2, "irimoya": D / 4}.get(form, D / 6), 0, -D / 2),
                         (W - ({"yosemune": D / 2, "irimoya": D / 4}.get(form, D / 2)), 0, -D / 2))
    K = koyagumi(p, W, D, info, eave_y=EAVE_Y, system=system, members=members, geya=(gk[0] * KEN, gk[1] * KEN),
                 outer_plates=True, soot=soot, rafters_from="wall")
    if soot:
        p.notes.append("sooted wear level: wood / bamboo sooted materials; the building calls koyagumi.soot_roof(roof) "
                       "so the rafters, lath and thatch underside above match")
    p.meta["koyagumi"] = {k: v for k, v in K.items() if k != "posts"}
    p.meta["wear_levels"] = ["_w0 new", "_w1 weathered (sample)", "_w2 old", "sooted (soot=True)"]
    # dims
    t = info["t"]
    p.dim("pitch_deg", round(math.degrees(math.atan(t)), 1), math.degrees(math.atan(t)), tol=0.1,
          source="roofs.PITCH (the frame follows the roof)")
    p.dim("frame_line_spacing_m", KEN, K["frame_lines"][1] - K["frame_lines"][0] if len(K["frame_lines"]) > 1 else KEN,
          source="PLAYBOOK §4 (1 ken bays)")
    bt = [s for s in p.solids if s.tag in ("hari", "ushibari")]
    if bt:
        b = bt[0].bbox()
        p.dim("tie_beam_depth_m", "0.24-0.32" if members == "sawn" else "0.26-0.32 (log dia.)",
              round(b[3] - b[2], 3) if members == "sawn" else 2 * LOG["beam"],
              source="period sections (A): koyabari 8-10 sun; ushibari logs 25-35 cm")
    if system == "wagoya":
        p.dim("purlin_spacing_m", 0.91, HALF, source="3 shaku (A)")
        p.dim("purlin_section_m", 0.105 if members == "sawn" else 0.12, 0.105 if members == "sawn" else
              2 * LOG["purlin"], source="3.5 sun sawn / 4 sun round (A)")
    else:
        p.dim("sasu_diameter_m", "0.12-0.18", 2 * SASU["sasu"], source="(A) minka sasu 4-6 sun")
        p.dim("moya_spacing_m", "0.45-0.90", 0.60, source="(A)")
    if gk[0] or gk[1]:
        p.dim("joya_span_ken", 3, (D - gk[0] * KEN - gk[1] * KEN) / KEN, tol=0.01, source="G1 A1-4: joya 3 ken + geya")
        p.dim("geya_depth_front_ken", 1, gk[0], tol=0.0, source="G1 A1-4")
        p.dim("geya_depth_back_ken", 1, gk[1], tol=0.0, source="G1 A1-4")
    for x in K["frame_lines"]:
        p.conn("post", (x, 0, 0), note="frame line at the front wall (the wall post carries the tie / aisle beam)")
        p.conn("post", (x, 0, -D), note="frame line at the back wall")
    for (x, z, y0, y1) in K["posts"]:
        p.conn("post", (x, 0, z), note="joya post (in the part), %.2f high" % (y1 - y0))
    p.conn("eave", (0, EAVE_Y, 0), note="keta top on the front wall")
    p.conn("ridge", (0, EAVE_Y + t * D / 2, -D / 2), note="rafter apex over the ridge line")
    return p


def register(reg):
    reg("jp_p_frame_koyagumi", list(VARIANTS), part_koyagumi)
