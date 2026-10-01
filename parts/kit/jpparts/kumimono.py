"""Bracket sets (jp_p_frame_kumimono; agent W2P2, 2026-10-01; research and proportions in parts/W2P2_NOTES.md §3).

frame(part, W, D, nx, nz, col_h, form, ...) builds a temple / shrine frame on a column grid: round columns, the head
tie (kashiranuki) with kibana ends, a nageshi band, a bracket set on every perimeter column (corner sets at the
corners), inter-columnar supports (kaerumata / kentozuka), the continuous beams of each step line and the outer purlin
(gangyo) the curved roof's rafters rest on. It returns g_out / bear_y / keta_y for sori.roof(..., g_out=, bear_y=).

Forms (all sized from the column diameter c, kiwari, GK):
  funa      funa-hijiki: a boat-shaped arm on the column top carrying the keta
  oto       daito + one arm (ooto-hijiki)
  mitsudo   daito + an arm parallel to the wall + three makito (hira-mitsudo)
  degumi    one projecting step (demitsudo / degumi): gangyo 1.05 c outside the column line
  mitesaki  three steps with the tail rafter (odaruki) and an eave ceiling between steps 2 and 3: gangyo 3.15 c out

Local frame of a set: origin on the column axis at the column top, a = along the wall, o = outward, y up.
LODs: Resolution 1 every member; Resolution 2 the daito + one block per tier stack; Resolution 3 one block per set.
"""
import math

from .core import Part, Solid, box, hexa, KEN, HALF, add, sub, mul, norm, cross
from .shapes import tube, oriented_box, frame_of
from . import sori as S

WOOD = "wood_weathered"
UP = (0.0, 1.0, 0.0)
FORMS = ("funa", "oto", "mitsudo", "degumi", "mitesaki")
STEPS = {"funa": 0, "oto": 0, "mitsudo": 0, "degumi": 1, "mitesaki": 3}


def dims(c):
    return dict(dw=1.5 * c, dh=0.75 * c, aw=0.45 * c, ah=0.55 * c, mw=0.75 * c, mh=0.42 * c, step=1.05 * c,
                al=3.2 * c, mp=1.25 * c, beam_h=0.55 * c, beam_w=0.42 * c, gh=0.62 * c, gw=0.55 * c)


class Frame:
    """A local set frame: world = O + a * A + y * UP + o * Ov."""

    def __init__(self, O, A, Ov):
        self.O, self.A, self.Ov = O, norm(A), norm(Ov)

    def P(self, a, y, o):
        return add(self.O, add(mul(self.A, a), add(mul(UP, y), mul(self.Ov, o))))


# ------------------------------------------------------------------------------------------------ members
def block(part, F, a, o, y0, levels, mat=WOOD, vis=(1,), tag="masu", axis=None):
    """A square block (daito / makito) centred at (a, o) from y0: levels [(dy, half width)] bottom to top (the lower
    levels narrower = the bowl cut). Convex (half widths never shrink going up)."""
    A, Ov = F.A, F.Ov
    if axis is not None:                         # turned 45 deg (a corner set's diagonal blocks)
        A, Ov = norm(add(F.A, F.Ov)), norm(sub(F.Ov, F.A))
    c0 = F.P(a, y0, o)
    verts = []
    for dy, hw in levels:
        for sa, so in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(add(c0, add(mul(A, sa * hw), add(mul(UP, dy), mul(Ov, so * hw)))))
    n = len(levels)
    faces = [[3, 2, 1, 0], [4 * (n - 1), 4 * (n - 1) + 1, 4 * (n - 1) + 2, 4 * (n - 1) + 3]]
    for r in range(n - 1):
        for i in range(4):
            j = (i + 1) % 4
            faces.append([4 * r + i, 4 * r + j, 4 * (r + 1) + j, 4 * (r + 1) + i])
    part.add(Solid(verts, faces, mat, vis=vis, tag=tag))


def daito(part, F, d, mat=WOOD, vis=(1, 2)):
    block(part, F, 0.0, 0.0, 0.0, [(0.0, d["dw"] * 0.38), (d["dh"] * 0.40, d["dw"] / 2), (d["dh"], d["dw"] / 2)], mat,
          vis=vis, tag="daito")
    return d["dh"]


def masu(part, F, a, o, y0, d, mat=WOOD, vis=(1,), axis=None):
    """A makito: a tapered block (6 faces: the bowl cut read as a taper, budget)."""
    block(part, F, a, o, y0, [(0.0, d["mw"] * 0.40), (d["mh"], d["mw"] / 2)], mat, vis=vis, tag="makito", axis=axis)
    return y0 + d["mh"]


def arm(part, F, a0, a1, o, y0, d, along="a", mat=WOOD, vis=(1,), grow=0.0, h=None, w=None, tag="hijiki"):
    """A bracket arm (hijiki) from a0 to a1 along `along` ('a' = the wall, 'o' = outward, 'd' = the corner diagonal),
    centred across at `o`, bottom y0: the underside curves up toward both ends. grow: +/- top/bottom offset so two arms
    that cross at one level never share a plane (C20)."""
    h = (d["ah"] if h is None else h) + 2 * grow
    w = d["aw"] if w is None else w
    y0 = y0 - grow
    if along == "a":
        dv, cv = F.A, F.Ov
    elif along == "o":
        dv, cv = F.Ov, F.A
    else:
        dv, cv = norm(add(F.A, F.Ov)), norm(sub(F.Ov, F.A))
    L = a1 - a0
    prof = [(a0, 0.32 * h), (a0 + 0.22 * L, 0.0), (a1 - 0.22 * L, 0.0), (a1, 0.32 * h), (a1, h), (a0, h)]
    base = F.O
    verts = []
    for s in (-w / 2, w / 2):
        for (t, y) in prof:
            verts.append(add(base, add(mul(dv, t), add(mul(UP, y0 + y), mul(cv, o + s)))))
    n = len(prof)
    faces = [list(range(n)), list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    part.add(Solid(verts, faces, mat, vis=vis, tag=tag, grain="long"))
    return y0 + h - grow


def beam(part, p0, p1, w, h, mat=WOOD, vis=(1, 2), tag="tsunagi", geo=False):
    """A horizontal beam p0 -> p1 (bottom centre line), w wide, h tall."""
    dv, e1, _ = frame_of(sub(p1, p0))
    c = add(mul(add(p0, p1), 0.5), (0.0, h / 2, 0.0))
    part.add(oriented_box(c, dv, UP, e1, math.dist(p0, p1) / 2, h / 2, w / 2, mat, vis=vis, tag=tag, grain="long",
                          geo=geo, view=geo, fire=True if geo else None))


def column(part, x, z, y0, y1, c, mat=WOOD):
    """Round column (8 / 6 / 4 sides by LOD) with collision."""
    from .core import cyl
    part.add(cyl("y", x, z, c / 2, y0, y1, mat, n=8, vis=(1,), geo=True, view=True, fire=True, tag="hashira"))
    part.add(cyl("y", x, z, c / 2, y0, y1, mat, n=6, vis=(2,), tag="hashira"))
    part.add(cyl("y", x, z, c / 2 * 0.92, y0, y1, mat, n=4, phase=math.pi / 4, vis=(3,), tag="hashira"))


# ------------------------------------------------------------------------------------------------ one set
def bracket_set(part, F, form, c, corner_o2=None, mat=WOOD, wall=True, proj=True, g=0.0, diag=None):
    """One bracket set on the column at F (column top = y 0; a along the wall, o outward). A corner column gets the
    full set for its first side, the projecting members again for the second side (corner_o2, turned 90 deg) and the
    diagonal arms / tail rafter / blocks of the corner. wall / proj: build the wall-line members / the projecting
    members; g: extra height growth so members crossing at one level never share a plane (C20). Returns
    {top_wall, g_y (gangyo bottom), y_step, ...} relative to the column top."""
    d = dims(c)
    s = d["step"]
    n = STEPS[form]
    al = d["al"] / 2
    out = {"steps": n, "step": s}
    corner = corner_o2 is not None
    if corner and diag is None:
        # second side: the projecting members only, turned 90 deg about the column, grown so they cross cleanly
        F2 = Frame(F.O, mul(F.Ov, -1.0) if _left_handed(F, corner_o2) else F.Ov, corner_o2)
        bracket_set(part, F2, form, c, None, mat, wall=False, proj=True, g=0.006, diag=False)
        diag = True
    if form == "funa":
        h = 0.6 * c
        if wall:
            arm(part, F, -2.0 * c, 2.0 * c, 0.0, 0.0, d, "a", mat, vis=(1, 2), h=h, w=0.5 * c, tag="funa_hijiki")
            _lod3(part, F, d, -2.0 * c, 2.0 * c, -0.3 * c, 0.3 * c, 0.0, h, mat)
        if not wall and proj:
            arm(part, F, -2.0 * c, 2.0 * c, 0.0, 0.0, d, "a", mat, vis=(1, 2), h=h, w=0.5 * c - 0.01, grow=0.004 + g,
                tag="funa_hijiki")
        out.update(top_wall=h, g_y=None)
        return out
    y = d["dh"]
    if wall:
        daito(part, F, d, mat)
    if form in ("oto", "mitsudo"):
        if wall or proj:
            top = arm(part, F, -al, al, 0.0, y, d, "a", mat, grow=g, w=d["aw"] - (0.01 if not wall else 0.0))
        if form == "mitsudo":
            ym = top - g
            for a in ((-d["mp"], 0.0, d["mp"]) if wall else (-d["mp"], d["mp"])):
                top = masu(part, F, a, 0.0, ym, d, mat)
        if wall:
            _lod2(part, F, d, [(-al, al, -0.25 * c, 0.25 * c, y, top)], mat)
            _lod3(part, F, d, -al, al, -0.4 * c, 0.4 * c, 0.0, top, mat)
        out.update(top_wall=top, g_y=None)
        return out
    lod2 = []
    k2 = math.sqrt(2)
    # ---- tier 1: the wall arm crossed by the projecting arm (+ the diagonal arm at a corner)
    y1 = y + d["ah"]
    if wall:
        arm(part, F, -al, al, 0.0, y, d, "a", mat)
        for a in (-d["mp"], 0.0, d["mp"]):
            masu(part, F, a, 0.0, y1, d, mat)
    if proj:
        arm(part, F, -1.2 * c, s + 0.45 * c, 0.0, y, d, "o", mat, grow=0.004 + g)
        masu(part, F, 0.0, s, y1 + 0.004 + g, d, mat)
    if diag:
        arm(part, F, -1.2 * c * k2, s * k2 + 0.45 * c, 0.0, y, d, "d", mat, grow=0.010)
        block(part, F, s, s, y1 + 0.010, _mlev(d), mat, vis=(1,), tag="makito", axis="d")
    y2 = y1 + d["mh"]
    lod2.append((-al, al, -0.3 * c, s + 0.45 * c, y, y2))
    if form == "degumi":
        # ---- tier 2: the wall arm and the step arm, each with three makito: the keta / gangyo rest on them
        t2 = y2 + d["ah"]
        if wall:
            arm(part, F, -al, al, 0.0, y2, d, "a", mat)
            for a in (-d["mp"], 0.0, d["mp"]):
                masu(part, F, a, 0.0, t2, d, mat)
        if proj:
            arm(part, F, -al, al, s, y2 + g, d, "a", mat, w=d["aw"] - (0.01 if not wall else 0.0))
            for a in (-d["mp"], 0.0, d["mp"]):
                masu(part, F, a, s, t2 + g, d, mat)
        if diag:
            block(part, F, s, s, t2 + 0.010, _mlev(d), mat, vis=(1,), tag="makito", axis="d")
        top = t2 + d["mh"]
        lod2.append((-al, al, -0.3 * c, s + 0.4 * c, y2, top))
        out.update(top_wall=top, g_y=top, reach=n * s, y_step=[y2])
        if wall:
            _lod2(part, F, d, lod2, mat)
            _lod3(part, F, d, -al, al, -0.4 * c, s + 0.4 * c, 0.0, top, mat)
        return out
    # ---- mitesaki. tier 2: wall arm, step-1 arm, projecting arm to step 2
    t2 = y2 + d["ah"]
    if wall:
        arm(part, F, -al, al, 0.0, y2, d, "a", mat)
        for a in (-d["mp"], 0.0, d["mp"]):
            masu(part, F, a, 0.0, t2, d, mat)
    if proj:
        arm(part, F, -al, al, s, y2 + g, d, "a", mat, w=d["aw"] - (0.01 if not wall else 0.0))
        arm(part, F, -1.0 * c, 2 * s + 0.45 * c, 0.0, y2, d, "o", mat, grow=0.004 + g)
        for a in (-d["mp"], d["mp"]):
            masu(part, F, a, s, t2 + g, d, mat)
        masu(part, F, 0.0, 2 * s, t2 + 0.004 + g, d, mat)
    if diag:
        arm(part, F, -1.0 * c * k2, 2 * s * k2 + 0.45 * c, 0.0, y2, d, "d", mat, grow=0.010)
        block(part, F, 2 * s, 2 * s, t2 + 0.010, _mlev(d), mat, vis=(1,), tag="makito", axis="d")
    y3 = t2 + d["mh"]
    lod2.append((-al, al, -0.3 * c, 2 * s + 0.45 * c, y2, y3))
    # tier 3: wall arm, step-2 arm: their makito carry the wall stack and the odaruki
    t3 = y3 + d["ah"]
    if wall:
        arm(part, F, -al, al, 0.0, y3, d, "a", mat)
        for a in (-d["mp"], 0.0, d["mp"]):
            masu(part, F, a, 0.0, t3, d, mat)
    if proj:
        arm(part, F, -al, al, 2 * s, y3 + g, d, "a", mat, w=d["aw"] - (0.01 if not wall else 0.0))
        for a in (-d["mp"], 0.0, d["mp"]):
            masu(part, F, a, 2 * s, t3 + g, d, mat)
    y4 = t3 + d["mh"]
    # odaruki: the tail rafter, on the step-2 centre makito, sloping down outward at 25 deg
    tn = math.tan(math.radians(25.0))
    oh = 0.60 * c
    rails = ((("o", 1.0, 0.0),) if proj else ()) + ((("d", k2, 0.012),) if diag else ())
    for along, k, lift in rails:
        o_in, o_out = -1.4 * c * k, (3 * s + 0.75 * c) * k
        o_rest = 2 * s * k
        ybot = (lambda o, ors=o_rest, kk=k, lf=lift: y4 + g + lf + tn * (ors - o) / kk)
        _odaruki(part, F, along, o_in, o_out, ybot, oh, 0.50 * c - (0.01 if not wall else 0.0), mat)
    # tier 4 at step 3: a makito on the odaruki, the step-3 arm, its makito: the gangyo sits on them
    yo = y4 - tn * s + oh / math.cos(math.radians(25.0))
    m3 = yo + d["mh"]
    t4 = m3 + d["ah"]
    gy = t4 + d["mh"]
    if proj:
        masu(part, F, 0.0, 3 * s, yo + g, d, mat)
        arm(part, F, -al, al, 3 * s, m3 + g, d, "a", mat, w=d["aw"] - (0.01 if not wall else 0.0))
        for a in (-d["mp"], 0.0, d["mp"]):
            masu(part, F, a, 3 * s, t4 + g, d, mat)
    if diag:
        block(part, F, 3 * s, 3 * s, yo + 0.012, _mlev(d), mat, vis=(1,), tag="makito", axis="d")
        arm(part, F, 3 * s * k2 - 0.9 * c, 3 * s * k2 + 0.9 * c, 0.0, m3 + 0.012, d, "d", mat)
        block(part, F, 3 * s, 3 * s, t4 + 0.012, _mlev(d), mat, vis=(1,), tag="makito", axis="d")
    # the wall stack continues: one more wall arm and its makito
    tw = y4 + d["ah"]
    topw = tw + d["mh"]
    if wall:
        arm(part, F, -al, al, 0.0, y4, d, "a", mat)
        for a in (-d["mp"], 0.0, d["mp"]):
            masu(part, F, a, 0.0, tw, d, mat)
    lod2.append((-al, al, -0.3 * c, 2 * s + 0.4 * c, y3, y4))
    lod2.append((-al, al, 2.6 * s, 3 * s + 0.45 * c, yo, gy))
    lod2.append((-al, al, -0.3 * c, 0.3 * c, y4, topw))
    out.update(top_wall=topw, g_y=gy, reach=n * s, y_step=[y2, y3, y4], y_odaruki_step3=yo)
    if wall:
        _lod2(part, F, d, lod2, mat)
        _lod3(part, F, d, -al, al, -0.4 * c, 3 * s + 0.4 * c, 0.0, gy, mat)
    return out


def _mlev(d):
    return [(0.0, d["mw"] * 0.40), (d["mh"], d["mw"] / 2)]


def _left_handed(F, o2):
    """True when the second side's along-direction must be -Ov of the first side (keeps a consistent handedness)."""
    return False


def _odaruki(part, F, along, o_in, o_out, ybot, h, w, mat):
    dv = F.Ov if along == "o" else norm(add(F.A, F.Ov))
    cv = F.A if along == "o" else norm(sub(F.Ov, F.A))
    p_in = add(F.O, add(mul(dv, o_in), mul(UP, ybot(o_in))))
    p_out = add(F.O, add(mul(dv, o_out), mul(UP, ybot(o_out))))
    dd, e1, e2 = frame_of(sub(p_out, p_in))
    e2 = norm(cross(cv, dd))
    if e2[1] < 0:
        e2 = mul(e2, -1.0)
    c = add(mul(add(p_in, p_out), 0.5), mul(e2, h / 2))
    part.add(oriented_box(c, dd, e2, cv, math.dist(p_in, p_out) / 2, h / 2, w / 2, mat, vis=(1, 2), tag="odaruki",
                          grain="long"))


def _lod2(part, F, d, boxes, mat):
    """Resolution 2: one block per tier stack (a, o ranges)."""
    for (a0, a1, o0, o1, y0, y1) in boxes:
        c = F.P((a0 + a1) / 2, (y0 + y1) / 2, (o0 + o1) / 2)
        part.add(oriented_box(c, F.A, UP, F.Ov, (a1 - a0) / 2 * 0.92, (y1 - y0) / 2, (o1 - o0) / 2, mat, vis=(2,),
                              tag="kumi_lod"))


def _lod3(part, F, d, a0, a1, o0, o1, y0, y1, mat):
    c = F.P((a0 + a1) / 2, (y0 + y1) / 2, (o0 + o1) / 2)
    part.add(oriented_box(c, F.A, UP, F.Ov, (a1 - a0) / 2 * 0.85, (y1 - y0) / 2, (o1 - o0) / 2 * 0.9, mat, vis=(3,),
                          tag="kumi_lod"))


# ------------------------------------------------------------------------------------------------ inter-columnar
def kaerumata(part, F, a, y0, height, c, mat=WOOD, vis=(1,)):
    """Frog-leg strut (kaerumata) on the head tie between columns: two spreading legs + a crown + a makito."""
    d = dims(c)
    t = 0.40 * c
    W = 1.7 * c
    hl = height - d["mh"]
    for sg in (-1, 1):
        prof = [(a + sg * W / 2, 0.0), (a + sg * (W / 2 - 0.28 * c), 0.0), (a + sg * 0.12 * c, hl * 0.86),
                (a + sg * 0.40 * c, hl * 0.86)]
        _plate(part, F, prof, y0, t, mat, vis, "kaerumata")
    _plate(part, F, [(a - 0.42 * c, hl * 0.80), (a + 0.42 * c, hl * 0.80), (a + 0.36 * c, hl), (a - 0.36 * c, hl)], y0,
           t * 1.02, mat, vis, "kaerumata")
    masu(part, F, a, 0.0, y0 + hl, d, mat, vis=vis)


def kentozuka(part, F, a, y0, height, c, mat=WOOD, vis=(1,)):
    """Kentozuka: a short post with a makito (the plainer inter-columnar support)."""
    d = dims(c)
    hl = height - d["mh"]
    c0 = F.P(a, y0 + hl / 2, 0.0)
    part.add(oriented_box(c0, F.A, UP, F.Ov, 0.22 * c, hl / 2, 0.20 * c, mat, vis=vis, tag="kentozuka"))
    masu(part, F, a, 0.0, y0 + hl, d, mat, vis=vis)


def _plate(part, F, prof, y0, t, mat, vis, tag):
    """A flat convex plate in the wall plane (profile [(a, y)] counter-clockwise or not), t thick across o."""
    verts = []
    for so in (-t / 2, t / 2):
        for (a, y) in prof:
            verts.append(F.P(a, y0 + y, so))
    n = len(prof)
    faces = [list(range(n)), list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
    part.add(Solid(verts, faces, mat, vis=vis, tag=tag))


# ------------------------------------------------------------------------------------------------ the frame
def frame(part, W, D, nx, nz, col_h, form="degumi", c=None, y0=0.0, covering="hongawara", t_j=None,
          nakazonae="kaerumata", nageshi=True, mat=WOOD, inner=False):
    """Columns on an nx x nz bay grid over W x D (x 0..W, z 0..-D), the head tie, a bracket set on every perimeter
    column, inter-columnar supports, the step-line beams and the gangyo. Returns the dict sori.roof needs:
    g_out (gangyo outside the column line), bear_y (gangyo top) and keta_y (the wall-line purlin top that meets the
    rafters), plus c, form and the set heights."""
    bx, bz = W / nx, D / nz
    c = c or max(0.18, round(0.11 * min(bx, bz), 3))
    d = dims(c)
    s = d["step"]
    t_j = S.rafter_pitch(covering) if t_j is None else t_j
    yt = y0 + col_h
    nodes = []
    for i in range(nx + 1):
        for j in range(nz + 1):
            if inner or i in (0, nx) or j in (0, nz):
                nodes.append((i * bx, -j * bz))
    for (x, z) in nodes:
        column(part, x, z, y0, yt, c, mat)
    # head tie (kashiranuki) through the column tops on the four sides, kibana ends past the corners
    th, tw = 0.62 * c, 0.42 * c
    for (p0, p1) in (((-0.9 * c, 0.0), (W + 0.9 * c, 0.0)), ((-0.9 * c, -D), (W + 0.9 * c, -D)),
                     ((0.0, 0.9 * c), (0.0, -D - 0.9 * c)), ((W, 0.9 * c), (W, -D - 0.9 * c))):
        grow = 0.004 if p0[0] == p1[0] else 0.0
        beam(part, (p0[0], yt - th - grow, p0[1]), (p1[0], yt - th - grow, p1[1]), tw + 2 * grow, th + 2 * grow, mat,
             vis=(1, 2, 3), tag="kashiranuki")
    if nageshi:
        yn = y0 + min(2.25, col_h * 0.62)
        for (p0, p1, o) in (((0.0, 0.0), (W, 0.0), (0.0, 1.0)), ((0.0, -D), (W, -D), (0.0, -1.0)),
                            ((0.0, 0.0), (0.0, -D), (-1.0, 0.0)), ((W, 0.0), (W, -D), (1.0, 0.0))):
            off = c / 2 + 0.03
            q0 = (p0[0] + o[0] * off - abs(o[1]) * c / 2, yn, p0[1] + o[1] * off + abs(o[0]) * c / 2)
            q1 = (p1[0] + o[0] * off + abs(o[1]) * c / 2, yn, p1[1] + o[1] * off - abs(o[0]) * c / 2)
            beam(part, q0, q1, 0.06, 0.22 * c + 0.06, mat, vis=(1, 2), tag="nageshi")
    # bracket sets
    sides = {"front": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), "back": ((-1.0, 0.0, 0.0), (0.0, 0.0, -1.0)),
             "left": ((0.0, 0.0, 1.0), (-1.0, 0.0, 0.0)), "right": ((0.0, 0.0, -1.0), (1.0, 0.0, 0.0))}
    info = None
    for (x, z) in nodes:
        on = []
        if abs(z) < 1e-6:
            on.append("front")
        if abs(z + D) < 1e-6:
            on.append("back")
        if abs(x) < 1e-6:
            on.append("left")
        if abs(x - W) < 1e-6:
            on.append("right")
        if not on:
            continue
        A, Ov = sides[on[0]]
        o2 = sides[on[1]][1] if len(on) > 1 else None
        if o2 is not None:
            # corner: orient so that A runs toward the second side's outside (a = along o2)
            A = o2
        F = Frame((x, yt, z), A, Ov)
        r = bracket_set(part, F, form, c, corner_o2=o2, mat=mat)
        info = info or r
    n = STEPS[form]
    g_out = n * s
    top_wall = yt + info["top_wall"]
    # continuous beams: the wall line (on the top makito), each step line, and the gangyo (outer purlin)
    bh, bw = d["beam_h"], d["beam_w"]
    lines = []
    if n == 0:
        keta_y = top_wall + d["gh"]
        lines.append((0.0, top_wall, d["gw"], d["gh"], "keta"))
        bear_y = keta_y
    else:
        g_bot = yt + info["g_y"]
        bear_y = g_bot + d["gh"]
        keta_y = bear_y + t_j * g_out           # the rafters rise t_j per m from the gangyo to the wall line
        lines.append((g_out, g_bot, d["gw"], d["gh"], "gangyo"))
        # the wall-line purlin, packed up on a wall board (kabe-ita) to meet the rafters
        lines.append((0.0, top_wall, 0.40 * c, keta_y - top_wall, "keta"))
        if form == "mitesaki":
            ys = info["y_step"]
            lines.append((s, yt + ys[1], bw, bh, "torigeta"))
    for (o, yb, w, h, tag) in lines:
        for (p0, p1, ov) in (((0.0, 0.0), (W, 0.0), (0.0, 1.0)), ((0.0, -D), (W, -D), (0.0, -1.0)),
                             ((0.0, 0.0), (0.0, -D), (-1.0, 0.0)), ((W, 0.0), (W, -D), (1.0, 0.0))):
            # the gangyo runs 6 cm past its corner crossing, the keta stops on the corner column: further out they
            # would rise into the neighbouring slope's rafters, which fall toward the eave (C12 / S3)
            ext = o + (0.06 if o > 0 else 0.0)
            along = (p1[0] - p0[0], p1[1] - p0[1])
            L = math.hypot(*along)
            ux, uz = along[0] / L, along[1] / L
            q0 = (p0[0] + ov[0] * o - ux * ext, yb, p0[1] + ov[1] * o - uz * ext)
            q1 = (p1[0] + ov[0] * o + ux * ext, yb, p1[1] + ov[1] * o + uz * ext)
            grow = 0.005 if abs(ov[0]) > 0.5 else 0.0       # crossing beams at a corner never share a plane
            beam(part, (q0[0], yb - grow, q0[2]), (q1[0], yb - grow, q1[2]), w + 2 * grow, h + 2 * grow, mat,
                 vis=(1, 2, 3) if tag in ("gangyo", "keta") else (1, 2), tag=tag)
    # mitesaki: the eave ceiling (noki-tenjo) between steps 2 and 3, one board per side
    if form == "mitesaki":
        yc = yt + info["y_odaruki_step3"] - 0.02
        for (p0, p1, ov) in (((0.0, 0.0), (W, 0.0), (0.0, 1.0)), ((0.0, -D), (W, -D), (0.0, -1.0)),
                             ((0.0, 0.0), (0.0, -D), (-1.0, 0.0)), ((W, 0.0), (W, -D), (1.0, 0.0))):
            along = (p1[0] - p0[0], p1[1] - p0[1])
            L = math.hypot(*along)
            ux, uz = along[0] / L, along[1] / L
            om = 2.5 * s
            q0 = (p0[0] + ov[0] * om - ux * 2.0 * s, yc, p0[1] + ov[1] * om - uz * 2.0 * s)
            q1 = (p1[0] + ov[0] * om + ux * 2.0 * s, yc, p1[1] + ov[1] * om + uz * 2.0 * s)
            beam(part, (q0[0], yc - 0.03, q0[2]), (q1[0], yc - 0.03, q1[2]), 0.9 * s, 0.03, "ceil_boards", vis=(1,),
                 tag="noki_tenjo")
    # inter-columnar supports on the head tie, mid bay, under the wall line
    if nakazonae:
        hsup = (top_wall - yt) if n == 0 else (yt + info["y_step"][0] - yt if form == "mitesaki" else
                                               yt + info["g_y"] - yt - d["mh"] - d["ah"])
        hsup = max(hsup, 0.6 * c)
        for side, (A, Ov) in sides.items():
            if side in ("front", "back"):
                L, nb = W, nx
                o0 = (0.0, 0.0) if side == "front" else (W, -D)
            else:
                L, nb = D, nz
                o0 = (0.0, -D) if side == "left" else (W, 0.0)
            for k in range(nb):
                a = (k + 0.5) * L / nb
                F = Frame((o0[0], yt, o0[1]), A, Ov)
                if nakazonae == "kaerumata":
                    kaerumata(part, F, a, 0.0, hsup, c, mat)
                else:
                    kentozuka(part, F, a, 0.0, hsup, c, mat)
    return {"form": form, "c": c, "g_out": round(g_out, 4), "bear_y": round(bear_y, 4), "keta_y": round(keta_y, 4),
            "col_top": yt, "top_wall": round(top_wall, 4), "t_j": t_j, "nodes": nodes, "steps": n}


# ------------------------------------------------------------------------------------------------ samples (parts)
def sample(variant):
    """A one-bay sample of each form for the parts library: two columns 1.5 ken apart (a corner column at x 0 for
    the _corner variants), the head tie, sets, one nakazonae, beams. variant: funa | oto | mitsudo | degumi |
    mitesaki | mitesaki_corner | degumi_corner | kaerumata | kentozuka."""
    p = Part("jp_p_frame_kumimono", "_" + variant, "frame", tiers=[2, 3],
             used_for="temple / shrine bracket sets (W2P2): town-grade halls, gates, bell towers, pagodas",
             recipe="kumimono.frame / bracket_set", datum="column centre line x 0 at the column top y = 3.0")
    form = variant.split("_")[0]
    if form in ("kaerumata", "kentozuka"):
        c = 0.25
        F = Frame((0.0, 3.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        beam(p, (-0.4, 3.0 - 0.62 * c, 0.0), (2.6, 3.0 - 0.62 * c, 0.0), 0.42 * c, 0.62 * c, vis=(1, 2, 3),
             tag="kashiranuki")
        (kaerumata if form == "kaerumata" else kentozuka)(p, F, 1.1, 0.0, 0.9 * c * 1.6, c)
        beam(p, (-0.4, 3.0 + 0.9 * c * 1.6, 0.0), (2.6, 3.0 + 0.9 * c * 1.6, 0.0), 0.42 * c, 0.55 * c, vis=(1, 2, 3),
             tag="tsunagi")
        p.conn("post", (0.0, 0.0, 0.0), hidden=True)
        return p
    corner = variant.endswith("corner")
    bay = 2.73
    c = 0.30
    if corner:
        info = frame(p, bay, bay, 1, 1, 3.0, form, c=c, nakazonae="kaerumata", nageshi=False)
    else:
        info = _side_sample(p, bay, form, c)
    p.meta["kumimono"] = {k: v for k, v in info.items() if k != "nodes"}
    p.dim("column_diameter_m", "0.18-0.45", c)
    p.dim("gangyo_out_m", {"funa": 0.0, "oto": 0.0, "mitsudo": 0.0, "degumi": round(1.05 * c, 3),
                           "mitesaki": round(3.15 * c, 3)}[form], info["g_out"], tol=0.005)
    p.conn("post", (0.0, 0.0, 0.0), note="column centre", hidden=True)
    p.conn("eave", (0.0, info["bear_y"], info["g_out"]), note="gangyo top: sori.roof(bear_y=, g_out=)")
    return p


def _side_sample(p, bay, form, c):
    """One side bay: two columns (x 0, x bay) on the front line, sets facing +z, head tie, beams, a kaerumata."""
    yt = 3.0
    d = dims(c)
    s = d["step"]
    for x in (0.0, bay):
        column(p, x, 0.0, 0.0, yt, c)
    beam(p, (-0.9 * c, yt - 0.62 * c, 0.0), (bay + 0.9 * c, yt - 0.62 * c, 0.0), 0.42 * c, 0.62 * c, vis=(1, 2, 3),
         tag="kashiranuki")
    r = None
    for x in (0.0, bay):
        r = bracket_set(p, Frame((x, yt, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), form, c)
    n = STEPS[form]
    t_j = S.rafter_pitch("hongawara")
    top_wall = yt + r["top_wall"]
    if n:
        g_bot = yt + r["g_y"]
        bear_y = g_bot + d["gh"]
        beam(p, (-0.5 * c, g_bot, n * s), (bay + 0.5 * c, g_bot, n * s), d["gw"], d["gh"], vis=(1, 2, 3), tag="gangyo")
        keta_y = bear_y + t_j * n * s
        beam(p, (-0.5 * c, top_wall, 0.0), (bay + 0.5 * c, top_wall, 0.0), 0.5 * c, keta_y - top_wall, vis=(1, 2, 3),
             tag="keta")
        hsup = (r["y_step"][0] if form == "mitesaki" else r["g_y"] - d["mh"] - d["ah"])
    else:
        bear_y = keta_y = top_wall + d["gh"]
        beam(p, (-0.5 * c, top_wall, 0.0), (bay + 0.5 * c, top_wall, 0.0), d["gw"], d["gh"], vis=(1, 2, 3), tag="keta")
        hsup = r["top_wall"]
    if form != "funa":
        kaerumata(p, Frame((0.0, yt, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), bay / 2, 0.0, max(hsup, 0.6 * c), c)
    return {"form": form, "c": c, "g_out": n * s, "bear_y": round(bear_y, 4), "keta_y": round(keta_y, 4),
            "steps": n}
