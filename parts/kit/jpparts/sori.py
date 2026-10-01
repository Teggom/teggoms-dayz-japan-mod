"""Curved temple / shrine roofs: jp_p_roof_sori (agent W2P2, 2026-10-01; research in parts/W2P2_NOTES.md).

roof(part, W, D, form, covering, ...) covers the column grid x 0..W (along the ridge), z 0 (front column line) ..
-D (back), like roofs.roof, with a CURVED roof:
  - sori profile: the slope rate rises from t0 at the eave edge to t1 at the main ridge, t(d) = t0 + (t1-t0)(d/R)^p,
    d = plan distance in from each slope's own eave edge, R the main run. Every slope of a hipped form uses the same
    function of d, so the front and side slopes meet exactly on the hip;
  - nokizori: the eave lifts toward each corner (or verge end), lift = L f(e) f(d), f(x) = (1 - x/Ls)^2, e = distance
    along the eave from the corner: symmetric in e and d, so the hip line stays shared;
  - two-tier rafters (jidaruki on the bearing line, an eave beam kioi, hiendaruki flying rafters to the kayaoi fascia),
    pivoting on the bearing so the tips rise with the eave; two-tier sumigi on hipped corners;
  - coverings: hongawara (pans + round covers per 0.303 column on the curve, tomoe round ends, karakusa lips, clay bed
    + urako fascia = PLAYBOOK T1), kokera / hiwada (curved field + the thick layered eave edge, koba), copper (seam
    ribs + a thin copper-clad edge);
  - ridge (7-course noshi + onigawara, or a box ridge), corner ridges down the curved hips, descending ridges down
    the upper gable verges, curved hafu with a gegyo, the irimoya gable face, a tsutsumi strip at the gable foot;
  - silhouette LODs (T7b): Resolution 2 / 3 keep the eave strip, kayaoi, ridges, hips, oni, hafu, a far-material
    field (C16) and a closed far body; Geometry / View / Fire = one convex slab per plan cell (least-squares planes),
    Roadway on their tops (tile and board roofs are walkable, T9).

Forms: irimoya | yosemune (hipped; hogyo when W == D) | kirizuma | nagare (kirizuma with a long front slope over the
steps: front_ext; the hook for W2P1's jp_p_roof_nagare, see nagare_curved()).

Coordinates as roofs.py: x along the ridge, z 0 = front column line, -D back; y 0 = floor. bear_y = the top of the
outermost support the rafters rest on (keta, or the gangyo g_out outside the column line on a bracketed hall).
"""
import math

from .core import Part, Solid, box, prism, hexa, KEN, HALF, EAVE_Y, LIBRARY, add, sub, mul, norm, cross, dot
from .shapes import slab, tube, half_tube, oriented_box, clip_poly, clean_poly, frame_of
from . import kawara as K
from . import roofs as R


def _mk(key, fallback):
    return key if key in LIBRARY else fallback


MISSING = [k for k in ("roof_hiwada", "roof_copper") if k not in LIBRARY]

COVER = {
    # t0 / t1: slope rate at the eave edge / at the ridge (GK: temple roofs ~3-5 sun at the eave, 7-10 sun at the top)
    # Te: eave stack from the flying-rafter top at the tip to the covering base; top: covering top over its base
    "hongawara": dict(t0=0.42, t1=0.80, Te=0.22, top=0.06, surf="tile_roof", fire="pottery"),
    "kokera": dict(t0=0.40, t1=0.90, Te=0.30, top=0.025, surf="board_roof", fire="wood", koba=0.30, expo=0.10),
    "hiwada": dict(t0=0.42, t1=0.95, Te=0.26, top=0.025, surf="board_roof", fire="wood", koba=0.24, expo=0.06),
    "copper": dict(t0=0.40, t1=0.85, Te=0.16, top=0.02, surf="board_roof", fire="metalplate", koba=0.12, expo=0.45),
}


def cover_mat(cov):
    return {"hongawara": K.FIELD, "kokera": "roof_kokera", "hiwada": _mk("roof_hiwada", "roof_kureita"),
            "copper": _mk("roof_copper", "roof_kureita")}[cov]


def params(covering="hongawara", **kw):
    """The full parameter set (COVER defaults + rafter sizes). kw None values are ignored."""
    c = dict(COVER[covering])
    c.update(p=1.6, L=0.30, span=None, tiers=2, rw=0.085, rdj=0.10, rdh=0.09, hk=0.10, kfrac=0.42, sp=None, g_out=0.0,
             Tv=0.30, covering=covering)
    for k, v in kw.items():
        if v is not None:
            c[k] = v
    c.setdefault("t_j", None)
    c.setdefault("t_h", None)
    if c["t_j"] is None:
        c["t_j"] = c["t0"] - 0.06            # base rafters flatter than the covering at the eave: the gap only grows
    if c["t_h"] is None:
        c["t_h"] = c["t0"] - 0.14            # flying rafters flatter still (GK)
    return c


def rafter_pitch(covering="hongawara", t0=None):
    """The base-rafter slope rate a bracket set must match (kumimono.frame uses it for the wall-line keta)."""
    return params(covering, t0=t0)["t_j"]


# ------------------------------------------------------------------------------------------------ small maths
def _solve3(m, v):
    def det(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    d = det(m)
    if abs(d) < 1e-12:
        return None
    out = []
    for i in range(3):
        mi = [[v[r] if c == i else m[r][c] for c in range(3)] for r in range(3)]
        out.append(det(mi) / d)
    return out


def _samples(poly):
    n = len(poly)
    cx = sum(p[0] for p in poly) / n
    cz = sum(p[1] for p in poly) / n
    pts = list(poly) + [(cx, cz)]
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        pts.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
        pts.append(((a[0] + cx) / 2, (a[1] + cz) / 2))
    return pts


def plane(poly, fn, mode="under", pad=0.0):
    """A plane y = A x + B z + C fitted (least squares) to fn over a plan polygon, then moved so it is under (or
    over) every sample (mode 'under' | 'over' | 'mean'). Returns (fn(x, z), max deviation)."""
    pts = _samples(poly)
    ys = [fn(x, z) for x, z in pts]
    sxx = sum(x * x for x, _ in pts); sxz = sum(x * z for x, z in pts); szz = sum(z * z for _, z in pts)
    sx = sum(x for x, _ in pts); sz = sum(z for _, z in pts); n = len(pts)
    sxy = sum(x * y for (x, _), y in zip(pts, ys)); szy = sum(z * y for (_, z), y in zip(pts, ys)); sy = sum(ys)
    abc = _solve3([[sxx, sxz, sx], [sxz, szz, sz], [sx, sz, n]], [sxy, szy, sy])
    if abc is None:
        abc = [0.0, 0.0, sy / n]
    A, B, C = abc
    res = [y - (A * x + B * z + C) for (x, z), y in zip(pts, ys)]
    if mode == "under":
        C += min(res) - pad
    elif mode == "over":
        C += max(res) + pad
    dev = max(res) - min(res)
    return (lambda x, z, A=A, B=B, C=C: A * x + B * z + C), dev


def _area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2


def _pairs(xs):
    return list(zip(xs[:-1], xs[1:]))


def _uniq(xs, eps=0.12):
    out = []
    for x in sorted(xs):
        if not out or x - out[-1] > eps:
            out.append(x)
        else:
            out[-1] = max(out[-1], x) if x == xs[-1] else out[-1]
    return out


# ------------------------------------------------------------------------------------------------ the curved slope
class SoriSlope:
    """One slope of a curved roof: the plan geometry of a roofs.Slope plus the sori surface and the rafter lines."""

    def __init__(self, b, ov, run, P, Ls, hipped, d_b, bear_y, wall_u=None, run_E=None, curved=False):
        self.b, self.name, self.pieces, self.poly = b, b.name, b.pieces, b.poly
        self.ov, self.R, self.P, self.Ls, self.hipped = ov, run, P, Ls, hipped
        self.RE = run_E or run                  # the run the profile is normalised to (shared by a hipped roof)
        ue = [b.u_of(x, z) for x, z in b.poly if abs(b.s(x, z) + ov) < 1e-6]
        self.u_lo, self.u_hi = min(ue), max(ue)
        self.ix, self.iz = b.inw
        self.ux, self.uz = b.udir
        self.wall_u = wall_u                    # kirizuma: u of the two gable column lines (verge zone outside)
        self.d_b, self.bear_y = d_b, bear_y
        t_j, t_h = P["t_j"], P["t_h"]
        self.sj, self.sh = math.sqrt(1 + t_j * t_j), math.sqrt(1 + t_h * t_h)
        self.d_k = min(P["kfrac"] * ov, d_b - 0.30) if P["tiers"] == 2 else 0.0
        # curved rafters (nagare porches, thin shrine roofs): every rafter line follows the covering curve at a fixed
        # depth, so the roof stays thin over an open porch; straight (temple halls): rafters pivot on the bearing
        self.curved = curved
        self.set_bear(bear_y)

    def stack(self):
        """Curved mode: covering base above the base-rafter underside (constant)."""
        P = self.P
        if P["tiers"] == 2:
            return P["Te"] + P["rdh"] * self.sh + P["hk"] + P["rdj"] * self.sj
        return P["Te"] + P["rdj"] * self.sj

    def set_bear(self, bear_y):
        self.bear_y = bear_y
        if self.curved:
            self.ye = bear_y + self.stack() - self.E(self.d_b)
        else:
            self.ye = bear_y + self.chain() + self.P["Te"]

    # ---- profile
    def chain(self):
        """Flying (or single-tier) rafter top at the tip above bear_y (no lift)."""
        P = self.P
        if P["tiers"] == 2:
            kt = P["t_j"] * (self.d_k - self.d_b) + P["rdj"] * self.sj + P["hk"]
            return kt + P["t_h"] * (0.0 - self.d_k) + P["rdh"] * self.sh
        return P["t_j"] * (0.0 - self.d_b) + P["rdj"] * self.sj

    def set_eave(self, ye):
        """Re-anchor the slope on a given covering eave height (nagare front): moves the bearing to match."""
        self.ye = ye
        if self.curved:
            self.bear_y = ye + self.E(self.d_b) - self.stack()
        else:
            self.bear_y = ye - self.P["Te"] - self.chain()

    def E(self, d):
        P = self.P
        if d <= 0:
            return P["t0"] * d
        return P["t0"] * d + (P["t1"] - P["t0"]) * self.RE / (P["p"] + 1) * (d / self.RE) ** (P["p"] + 1)

    def rate(self, d):
        P = self.P
        return P["t0"] + (P["t1"] - P["t0"]) * (max(d, 0.0) / self.RE) ** P["p"]

    def fe(self, x):
        return (1.0 - x / self.Ls) ** 2 if x < self.Ls else 0.0

    def e(self, u):
        return max(0.0, min(u - self.u_lo, self.u_hi - u))

    def lift(self, u, d):
        return self.P["L"] * self.fe(self.e(u)) * self.fe(max(d, 0.0))

    def lift_r(self, u, d):
        return self.P["L"] * self.fe(self.e(u)) * max(0.0, 1.0 - d / self.d_b)

    def cs(self, u, d):
        """Covering base (clay bed / board underside) height."""
        return self.ye + self.E(d) + self.lift(u, d)

    # ---- rafters (no-lift lines + the pivot lift)
    def base_bot(self, u, d):
        if self.curved:
            return self.cs(u, d) - self.stack()
        return self.bear_y + self.P["t_j"] * (d - self.d_b) + self.lift_r(u, d)

    def base_top(self, u, d):
        return self.base_bot(u, d) + self.P["rdj"] * self.sj

    def hien_bot(self, u, d):
        P = self.P
        if self.curved:
            return self.cs(u, d) - P["Te"] - P["rdh"] * self.sh
        kt = self.bear_y + P["t_j"] * (self.d_k - self.d_b) + P["rdj"] * self.sj + P["hk"]
        return kt + P["t_h"] * (d - self.d_k) + self.lift_r(u, d)

    def hien_top(self, u, d):
        return self.hien_bot(u, d) + self.P["rdh"] * self.sh

    def raft_top(self, u, d):
        if self.P["tiers"] == 2 and d < self.d_k:
            return self.hien_top(u, d)
        return self.base_top(u, d)

    # ---- plan
    def xz(self, u, d):
        ex, ez = self.b.eave_point(u)
        return (ex + self.ix * d, ez + self.iz * d)

    def ud(self, x, z):
        return self.b.u_of(x, z), self.b.s(x, z) + self.ov

    def at(self, fn):
        """Plan-coordinate version of a (u, d) function."""
        return lambda x, z: fn(*self.ud(x, z))

    def normal(self, u, d):
        h = 0.01
        gu = (self.cs(u + h, d) - self.cs(u - h, d)) / (2 * h)
        gd = (self.cs(u, d + h) - self.cs(u, d - h)) / (2 * h)
        tu = (self.ux, gu, self.uz)
        td = (self.ix, gd, self.iz)
        n = norm(cross(td, tu))
        return n if n[1] > 0 else mul(n, -1.0)

    def P3(self, u, d, h=0.0):
        x, z = self.xz(u, d)
        y = self.cs(u, d)
        if h == 0.0:
            return (x, y, z)
        n = self.normal(u, d)
        return (x + n[0] * h, y + n[1] * h, z + n[2] * h)

    def up(self, u, d):
        """Unit vector up the slope (in the d direction, on the surface)."""
        h = 0.01
        gd = (self.cs(u, d + h) - self.cs(u, d - h)) / (2 * h)
        return norm((self.ix, gd, self.iz))

    def top(self, u):
        """Plan depth of the slope at u (to the ridge / hip / gable foot)."""
        if u < self.u_lo - 1e-6 or u > self.u_hi + 1e-6:
            return 0.0
        return self.b.depth_at(min(max(u, self.u_lo + 1e-5), self.u_hi - 1e-5))

    def clip(self, pc, ua, ub, da, db):
        """A convex plan piece cut to u in [ua, ub], d in [da, db]."""
        ox, oz = self.b.uo
        wx, wz = self.b.wall
        poly = list(pc)
        for a, b, c in ((self.ux, self.uz, ub + ox * self.ux + oz * self.uz),
                        (-self.ux, -self.uz, -(ua + ox * self.ux + oz * self.uz)),
                        (self.ix, self.iz, db - self.ov + wx * self.ix + wz * self.iz),
                        (-self.ix, -self.iz, -(da - self.ov + wx * self.ix + wz * self.iz))):
            poly = clip_poly(poly, a, b, c)
            if len(poly) < 3:
                return []
        return poly if _area(poly) > 1e-4 else []

    def dmax(self):
        return max(self.ud(x, z)[1] for x, z in self.poly)

    def piece_us(self):
        """u of every piece vertex (where the slope's depth jumps: the irimoya gable foot, hip tops)."""
        return sorted({round(self.b.u_of(x, z), 6) for pc in self.pieces for x, z in pc})

    def u_breaks(self, step, corner_step=None, extra=()):
        """Cell breaks along the eave: the slope ends, the piece vertices (depth jumps) and `extra` always; then every
        `step` from the middle and every `corner_step` from each end, each only when >= 0.15 m from a kept break."""
        um = (self.u_lo + self.u_hi) / 2
        lo, hi = self.u_lo - 1e-6, self.u_hi + 1e-6
        req = sorted({round(x, 6) for x in [self.u_lo, self.u_hi] + list(extra) + self.piece_us() if lo <= x <= hi})
        opt = []
        k = 0
        while um + k * step < self.u_hi:
            opt += [um + k * step, um - k * step]
            k += 1
        if corner_step:
            k = 1
            while k * corner_step < min(self.Ls, (self.u_hi - self.u_lo) / 2):
                opt += [self.u_lo + k * corner_step, self.u_hi - k * corner_step]
                k += 1
        out = list(req)
        for x in sorted(opt):
            if lo <= x <= hi and all(abs(x - y) > 0.15 for y in out):
                out.append(x)
        return sorted(out)

    def d_breaks(self, first, step, extra=()):
        top = self.dmax()
        xs = [first] + [x for x in extra if first < x < top]
        d = (max(xs) if xs else first)
        while d + step < top - 0.2:
            d += step
            xs.append(d)
        xs.append(top + 0.01)
        out = []
        for x in sorted(xs):
            if not out or x - out[-1] > 0.1:
                out.append(x)
        return out

    def in_verge_zone(self, ua, ub):
        if not self.wall_u:
            return False
        return ub <= self.wall_u[0] + 1e-6 or ua >= self.wall_u[1] - 1e-6


# ------------------------------------------------------------------------------------------------ slopes of a form
def _gable_slopes(W, D, ovf, ovb, gl, gr, zr):
    fr = R.Slope("front", [(-gl, ovf), (W + gr, ovf), (W + gr, zr), (-gl, zr)], (0.0, -1.0), (0.0, 0.0), (1.0, 0.0),
                 (0.0, ovf), 0.0, 0.5, ovf, True, verges=(-gl, W + gr))
    bk = R.Slope("back", [(-gl, -D - ovb), (-gl, zr), (W + gr, zr), (W + gr, -D - ovb)], (0.0, 1.0), (0.0, -D),
                 (-1.0, 0.0), (W, -D - ovb), 0.0, 0.5, ovb, True)
    bk.verges = (bk.u_of(W + gr, -D - ovb), bk.u_of(-gl, -D - ovb))
    return fr, bk


# ------------------------------------------------------------------------------------------------ the generator
def roof(part, W, D, form="irimoya", covering="hongawara", bear_y=EAVE_Y, g_out=0.0, ov=None, gov=None, pitch=None,
         curve=None, corner_lift=None, lift_span=None, tiers=2, spacing=None, ridge_courses=7, front_ext=0.0,
         ridge_z=None, walkable=True, inside_rafters=False, hafu_mat="wood_weathered", hafu_h=0.42, paint=None,
         curved_rafters=None, front_bear_z=None):
    """Build a curved roof into `part`. Returns (slopes, info).

    W, D       column grid (x 0..W along the ridge, z 0..-D)
    form       irimoya | yosemune | kirizuma | nagare
    covering   hongawara | kokera | hiwada | copper
    bear_y     top of the support the base rafters rest on, g_out outside the column line (0: a keta on the line)
    ov         eave depth from the column line to the eave edge (default g_out + 1.25)
    gov        verge overhang (kirizuma / nagare), default 0.95
    pitch      (t0, t1) slope rate at the eave edge / at the ridge; curve = the profile exponent p (1 = straight-ish
               rise of the rate, 2-3 = the curve gathers toward the ridge)
    corner_lift / lift_span   L and Ls of the eave sweep
    tiers      2 (jidaruki + hiendaruki) or 1
    front_ext  nagare: the front slope runs this much further out (over the steps)
    """
    t0, t1 = pitch if pitch else (None, None)
    if corner_lift is None and form in ("kirizuma", "nagare"):
        corner_lift = 0.20                       # gable roofs: a gentler sweep at the verge ends (GK)
    curved = (form == "nagare") if curved_rafters is None else bool(curved_rafters)
    P = params(covering, t0=t0, t1=t1, p=curve, L=corner_lift, span=lift_span, tiers=tiers, g_out=g_out)
    if t0 is not None and pitch:
        P["t_j"], P["t_h"] = P["t0"] - 0.06, P["t0"] - 0.14
    ov = g_out + 1.25 if ov is None else ov
    d_b = ov - g_out
    sp = spacing or 0.26                    # ~ KEN / 7 (GK: 1 shi ~ 0.2-0.26 m on a town hall)
    P["sp"] = sp
    hipped = form in ("irimoya", "yosemune")
    if hipped:
        bases = R.slopes_for(W, D, form, 0.0, 0.5, ov, 0.0)
        run = ov + D / 2
        Ls = P["span"] or 0.30 * (min(W, D) + 2 * ov)
        Ls = min(max(Ls, 2 * d_b + 0.1), 0.92 * run)
        sls = [SoriSlope(b, ov, run, P, Ls, True, d_b, bear_y, curved=curved) for b in bases]
        gl = gr = 0.0
        zr = -D / 2
    else:
        gov = 0.95 if gov is None else gov
        gl, gr = gov if isinstance(gov, (tuple, list)) else (gov, gov)
        zr = -D / 2 if ridge_z is None else ridge_z
        ovf = ov + (front_ext if form == "nagare" else 0.0)
        fr, bk = _gable_slopes(W, D, ovf, ov, gl, gr, zr)
        run_b = zr + D + ov
        run_f = ovf - zr
        Ls = P["span"] or 0.30 * (D + 2 * ov)
        Ls = min(max(Ls, 2 * d_b + 0.1), 0.92 * min(run_b, run_f))
        bks = SoriSlope(bk, ov, run_b, P, Ls, False, d_b, bear_y, wall_u=(bk.u_of(W, 0), bk.u_of(0, 0)), curved=curved)
        fbz = (front_ext if front_bear_z is None else front_bear_z) + g_out
        frs = SoriSlope(fr, ovf, run_f, P, Ls, False, ovf - fbz if form == "nagare" else d_b, bear_y,
                        wall_u=(0.0, W), curved=curved)
        y_ridge = bks.cs(0.0, run_b) if False else bks.ye + bks.E(run_b)
        frs.set_eave(y_ridge - frs.E(run_f))
        sls = [frs, bks]
    info = {"form": form, "covering": covering, "W": W, "D": D, "ov": ov, "g_out": g_out, "bear_y": bear_y,
            "t0": P["t0"], "t1": P["t1"], "p": P["p"], "L": P["L"], "Ls": Ls, "tiers": tiers, "spacing": sp,
            "t_j": P["t_j"], "t_h": P["t_h"], "slopes": [s.name for s in sls], "missing_materials": list(MISSING),
            "eave_y": sls[0].ye, "zr": zr, "gov": (gl, gr), "front_ext": front_ext, "curved_rafters": curved}
    if not hipped:
        info["front_bear_y"] = sls[0].bear_y
        info["front_eave_y"] = sls[0].ye
    fire = P["fire"]
    for ss in sls:
        _body(part, ss, P, fire, walkable)
        _rafters(part, ss, P, inside_rafters)
        _eave_front(part, ss, P)
        if covering == "hongawara":
            _kawara_field(part, ss, P)
        else:
            _board_field(part, ss, P)
    if hipped:
        _sumigi(part, sls, P)
    _ridges(part, sls, P, info, form, W, D, gl, gr, zr, ridge_courses, walkable)
    _verges(part, sls, P, info, form, W, D, gl, gr, zr, hafu_mat if not paint else paint, hafu_h)
    # sag of the curve (how far the curved front slope sits under its eave-to-ridge chord)
    s0 = sls[0]
    Rr = s0.R
    chord = s0.E(Rr) / Rr
    info["curve_depth_m"] = round(max(chord * d - s0.E(d) for d in [Rr * k / 40 for k in range(41)]), 3)
    info["y_ridge"] = round(s0.cs((s0.u_lo + s0.u_hi) / 2, Rr), 3)
    info["corner_lift_m"] = round(P["L"], 3)
    info["sori"] = sls
    part.meta.setdefault("roof", {k: v for k, v in info.items() if k != "sori"})
    return sls, info


# ------------------------------------------------------------------------------------------------ body, collision
def _body(part, ss, P, fire, walkable):
    cov = P["covering"]
    kawara = cov == "hongawara"
    top_mat = R.BED_MAT if kawara else "wood_weathered"
    bed = 0.006 if kawara else 0.0
    soffit = "wood_weathered"
    d_ext = (ss.d_k,) if P["tiers"] == 2 else ()
    ub = ss.u_breaks(KEN, HALF, extra=ss.wall_u or ())
    db = ss.d_breaks(0.10, 2.0, extra=d_ext + (ss.ov,))
    for pc in ss.pieces:
        for (ua, ub_) in _pairs(ub):
            verge = ss.in_verge_zone(ua, ub_)
            for (da, db_) in _pairs(db):
                poly = ss.clip(pc, ua, ub_, da, db_)
                if not poly:
                    continue
                eave_zone = db_ <= ss.ov + 1e-6
                topf, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d) + bed), "under", pad=0.0 if kawara else 0.004)
                if verge and not eave_zone:
                    lowf, _ = plane(poly, ss.at(lambda u, d: max(ss.raft_top(u, d), ss.cs(u, d) - P["Tv"])), "under")
                else:
                    lowf, _ = plane(poly, ss.at(ss.raft_top), "under")
                board = 0.02 if eave_zone else 0.0
                if eave_zone:
                    part.add(slab(poly, lowf, lambda x, z, f=lowf: f(x, z) + board, soffit, vis=(1,), tag="sheathing"))
                part.add(slab(poly, lambda x, z, f=lowf: f(x, z) + board, topf,
                              {"top": top_mat, "bottom": soffit, "default": "wood_weathered"}, vis=(1,),
                              tag="tile_bed" if kawara else "noyane"))
    # far body (Resolution 2 / 3): closed, under the far field, so the eave underside never opens at distance
    for lods, us, dstep in (((2,), ss.u_breaks(KEN, HALF, extra=ss.wall_u or ()), 2.2),
                            ((3,), ss.u_breaks(4 * KEN, None, extra=ss.wall_u or ()), 5.0)):
        dbs = ss.d_breaks(0.0, dstep, extra=(ss.ov,))
        for pc in ss.pieces:
            for (ua, ub_) in _pairs(us):
                verge = ss.in_verge_zone(ua, ub_)
                for (da, db_) in _pairs(dbs):
                    poly = ss.clip(pc, ua, ub_, da, db_)
                    if not poly:
                        continue
                    topf, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d) + bed), "under", pad=0.004)
                    if verge:
                        lowf, _ = plane(poly, ss.at(lambda u, d: max(ss.raft_top(u, d), ss.cs(u, d) - P["Tv"])), "under")
                    else:
                        lowf, _ = plane(poly, ss.at(ss.raft_top), "under")
                    part.add(slab(poly, lowf, topf, {"top": top_mat, "bottom": soffit, "default": "wood_weathered"},
                                  vis=lods, tag="far_body"))
    # collision + Roadway: rafter top .. covering top, one convex slab per coarse cell
    us = ss.u_breaks(KEN, HALF, extra=ss.wall_u or ())
    dbs = ss.d_breaks(0.0, 2.0, extra=(ss.d_b, ss.ov))
    for pc in ss.pieces:
        for (ua, ub_) in _pairs(us):
            verge = ss.in_verge_zone(ua, ub_)
            for (da, db_) in _pairs(dbs):
                poly = ss.clip(pc, ua, ub_, da, db_)
                if not poly:
                    continue
                topf, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d) + P["top"]), "mean")
                if verge:
                    lowf, _ = plane(poly, ss.at(lambda u, d: max(ss.raft_top(u, d), ss.cs(u, d) - P["Tv"])), "over")
                else:
                    lowf, _ = plane(poly, ss.at(ss.raft_top), "over")
                part.add(slab(poly, lowf, topf, "roof_kawara" if P["covering"] == "hongawara" else "wood_weathered",
                              vis=(), geo=True, view=True, fire=fire, tag="roof_geo_" + ss.name))
                if walkable:
                    ins = _inset(poly, 0.03)
                    if ins:
                        part.road([(x, topf(x, z), z) for x, z in ins], P["surf"])


# ------------------------------------------------------------------------------------------------ rafters, beams
def _beam_cells(ss, d0, d1, step, corner_step):
    """Plan cells of an eave-parallel band d0..d1, cut by u breaks (mitred on a hip by the slope piece)."""
    out = []
    for pc in ss.pieces:
        for (ua, ub) in _pairs(ss.u_breaks(step, corner_step)):
            poly = ss.clip(pc, ua, ub, d0, d1)
            if poly:
                out.append(poly)
    return out


def _eave_band(ss, d0, d1, step, mitre=True):
    """Plan cells of an eave-parallel band that may start in front of the eave edge (d0 < 0): mitred round a hipped
    corner (the band runs out |d| past the eave end, so the two sides meet on the hip line), square at a verge."""
    out = []
    for (ua, ub) in _pairs(ss.u_breaks(step, None)):
        pts = []
        for d, rev in ((d0, False), (d1, True)):
            a, b = ua, ub
            if ss.hipped and (mitre or d > 0):
                if abs(ua - ss.u_lo) < 1e-6:
                    a = ss.u_lo + d
                if abs(ub - ss.u_hi) < 1e-6:
                    b = ss.u_hi - d
            row = [ss.xz(a, d), ss.xz(b, d)]
            pts += row[::-1] if rev else row
        poly = clean_poly(R._ccw(pts))
        if len(poly) >= 3 and _area(poly) > 1e-4:
            out.append(poly)
    return out


def _rafter(part, ss, u, d0, d1, bot, top, w, mat="wood_weathered", tag="rafter"):
    """Open-topped rafter (bottom, two sides, foot) along d at u, under the boards; in segments when it curves."""
    ux, uz = ss.ux, ss.uz
    hw = w / 2

    def p(d, sg, which):
        x, z = ss.xz(u + sg * hw, d)
        return (x, (top if which else bot)(u + sg * hw, d), z)
    n = max(1, int(math.ceil((d1 - d0) / 0.9))) if ss.curved else 1
    dd = [d0 + (d1 - d0) * k / n for k in range(n + 1)]
    qs, hint = [], []
    for a, b in _pairs(dd):
        qs += [[p(a, -1, 0), p(a, 1, 0), p(b, 1, 0), p(b, -1, 0)],
               [p(a, -1, 0), p(b, -1, 0), p(b, -1, 1), p(a, -1, 1)],
               [p(a, 1, 0), p(b, 1, 0), p(b, 1, 1), p(a, 1, 1)]]
        hint += [(0.0, -1.0, 0.0), (-ux, 0.0, -uz), (ux, 0.0, uz)]
    qs.append([p(d0, -1, 0), p(d0, 1, 0), p(d0, 1, 1), p(d0, -1, 1)])
    hint.append((-ss.ix, 0.0, -ss.iz))
    part.add(Solid([q for qq in qs for q in qq], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(qs))],
                   mat, vis=(1,), normals=hint, tag=tag, grain="long"))


def _rafters(part, ss, P, inside):
    sp, w = P["sp"], P["rw"]
    um = (ss.u_lo + ss.u_hi) / 2
    k = 0
    us = []
    while um + (k + 0.5) * sp < ss.u_hi:
        us += [um + (k + 0.5) * sp, um - (k + 0.5) * sp]
        k += 1
    sumi_half = 0.08 * math.sqrt(2) + w / 2 + 0.01
    for u in sorted(us):
        if u - w < ss.u_lo + 0.06 or u + w > ss.u_hi - 0.06:
            continue
        lim = ss.top(u) - (sumi_half if ss.hipped else 0.02)
        if ss.hipped:
            lim = min(lim, ss.e(u) - sumi_half)
        inside_walls = not ss.wall_u or ss.wall_u[0] + 0.1 < u < ss.wall_u[1] - 0.1
        if P["tiers"] == 2:
            d1 = min(ss.d_k, lim)
            if d1 > 0.05:
                _rafter(part, ss, u, 0.015, d1, ss.hien_bot, ss.hien_top, w * 0.94, tag="hiendaruki")
            d0 = ss.d_k - 0.045
        else:
            d0 = 0.015
        dend = (ss.top(u) - 0.05 if inside else ss.ov + 0.30) if inside_walls else ss.ov - 0.05
        d1 = min(dend, lim)
        if d1 > d0 + 0.05:
            _rafter(part, ss, u, d0, d1, ss.base_bot, ss.base_top, w, tag="jidaruki")
    # kioi (eave beam on the base-rafter ends) and kayaoi (fascia on the tips): curved, mitred at the hips
    if P["tiers"] == 2:
        for poly in _beam_cells(ss, ss.d_k - 0.06, ss.d_k - 0.002, KEN, HALF):
            b, _ = plane(poly, ss.at(ss.base_top), "under")
            part.add(slab(poly, b, lambda x, z, b=b: b(x, z) + P["hk"], "wood_weathered", vis=(1,), tag="kioi",
                          grain="long"))
    tipf = ss.hien_top if P["tiers"] == 2 else ss.base_top
    for lods, st, cst in (((1,), KEN, HALF), ((2,), KEN, None)):
        for poly in _beam_cells(ss, 0.0, 0.10, st, cst):
            b, _ = plane(poly, ss.at(tipf), "under")
            part.add(slab(poly, b, lambda x, z, b=b: b(x, z) + 0.11, "wood_weathered", vis=lods, tag="kayaoi",
                          grain="long"))


def _sumigi(part, sls, P):
    """Two-tier corner rafters along each hip in the eave zone (hipped forms): top flush with the soffit."""
    for ss in sls:
        if ss.name not in ("front", "back"):
            continue
        for end in (0, 1):
            u_c = ss.u_lo if end == 0 else ss.u_hi
            sg = 1.0 if end == 0 else -1.0
            # along the hip: plan point at (u_c + sg * t, t), t = distance in from the eave edge
            tiers = ([("hien", -0.12, ss.d_k + 0.25, ss.hien_top)] if P["tiers"] == 2 else []) + \
                    [("ji", (ss.d_k - 0.10) if P["tiers"] == 2 else -0.12, ss.d_b + 0.55, ss.base_top)]
            for nm, t0, t1, topf in tiers:
                n = 3
                for k in range(n):
                    ta = t0 + (t1 - t0) * k / n
                    tb = t0 + (t1 - t0) * (k + 1) / n
                    pts = []
                    for t in (ta, tb):
                        x, z = ss.xz(u_c + sg * t, t)
                        yt = topf(u_c + sg * max(t, 0.0) + 1e-4 * sg, max(t, 0.0)) + 0.005
                        if t < 0:
                            yt += (topf(u_c + sg * 1e-3, 0.0) - topf(u_c + sg * 0.05, 0.05)) * (-t / 0.05)
                        pts.append((x, yt, z))
                    hx, hz = (ss.ux * sg + ss.ix) / math.sqrt(2), (ss.uz * sg + ss.iz) / math.sqrt(2)
                    px, pz = -hz, hx
                    hw, dp = 0.08, 0.22
                    c = []
                    for yo in (-dp, 0.0):
                        for (p, s) in ((pts[0], -1), (pts[1], -1), (pts[1], 1), (pts[0], 1)):
                            c.append((p[0] + px * hw * s, p[1] + yo, p[2] + pz * hw * s))
                    part.add(hexa(c, "wood_weathered", vis=(1,), tag="sumigi_" + nm, grain="long"))
                    if k == 0 and t0 < 0:
                        # the protruding tip in the far LODs too (C15: it stands past the eave corner)
                        tt = min(tb, 0.12)
                        x2, z2 = ss.xz(u_c + sg * tt, tt)
                        y2 = pts[0][1] + (pts[1][1] - pts[0][1]) * (tt - ta) / (tb - ta)
                        q = [pts[0], (x2, y2, z2)]
                        cf = []
                        for yo in (-dp, 0.0):
                            for (p_, s_) in ((q[0], -1), (q[1], -1), (q[1], 1), (q[0], 1)):
                                cf.append((p_[0] + px * hw * s_, p_[1] + yo, p_[2] + pz * hw * s_))
                        part.add(hexa(cf, "wood_weathered", vis=(2, 3), tag="sumigi_far", grain="long"))


# ------------------------------------------------------------------------------------------------ eave front
def _eave_front(part, ss, P):
    cov = P["covering"]
    tipf = ss.hien_top if P["tiers"] == 2 else ss.base_top
    if cov == "hongawara":
        # urako / kawara-zan board above the kayaoi up to the tile underside (T1 fascia, C13)
        for lods, st, cst in (((1,), KEN, HALF), ((2,), KEN, None)):
            for poly in _beam_cells(ss, 0.015, 0.035, st, cst):
                b, _ = plane(poly, ss.at(tipf), "under")
                t, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d) + 0.018), "over")
                part.add(slab(poly, lambda x, z, b=b: b(x, z) + 0.11, t, "wood_weathered", vis=lods,
                              tag="kawara_fascia", grain="long"))
        return
    # koba: the thick layered eave edge (bands step forward going up), open front + underside per segment
    mat = cover_mat(cov)
    H = P["koba"]
    nb = 3
    us = ss.u_breaks(KEN, HALF)
    quads, nrm, uvl = [], [], []
    for k in range(nb):
        df, dbk = -0.015 * (k + 1), -0.015 * k
        for (ua, ub) in _pairs(us):
            def yb(u, kk=k):
                return tipf(u, 0.0) + 0.11 + (ss.cs(u, 0.0) - tipf(u, 0.0) - 0.11) * kk / nb

            def ext(u, d):
                # mitre around a hipped corner: the band runs out by |d| past the eave end
                if ss.hipped:
                    if abs(u - ss.u_lo) < 1e-6:
                        return u + d
                    if abs(u - ss.u_hi) < 1e-6:
                        return u - d
                return u
            a0, b0 = ext(ua, df), ext(ub, df)
            a1, b1 = ext(ua, dbk), ext(ub, dbk)
            ya0, yb0 = yb(ua), yb(ub)
            ya1, yb1 = yb(ua, k + 1), yb(ub, k + 1)
            fa, fb = ss.xz(a0, df), ss.xz(b0, df)
            quads.append([(fa[0], ya0, fa[1]), (fb[0], yb0, fb[1]), (fb[0], yb1, fb[1]), (fa[0], ya1, fa[1])])
            nrm.append((-ss.ix, 0.0, -ss.iz))
            ga, gb = ss.xz(a1, dbk), ss.xz(b1, dbk)
            quads.append([(ga[0], ya0, ga[1]), (gb[0], yb0, gb[1]), (fb[0], yb0, fb[1]), (fa[0], ya0, fa[1])])
            nrm.append((0.0, -1.0, 0.0))
            for q in quads[-2:]:
                uvl.append([(q[i][0] * ss.ux + q[i][2] * ss.uz, -q[i][1] / 0.5) for i in range(4)])
    part.add(Solid([p for q in quads for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(quads))],
                   mat, vis=(1,), normals=nrm, uv=uvl, tag="koba"))
    # far koba: one block per coarse segment
    for lods, st in (((2,), KEN), ((3,), 2 * KEN)):
        for poly in _eave_band(ss, -0.045, 0.10, st, mitre=True):
            b, _ = plane(poly, ss.at(lambda u, d: tipf(u, max(d, 0.0)) + (0.11 if lods == (2,) else 0.0)), "under")
            t, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d)), "under")
            part.add(slab(poly, b, t, mat, vis=lods, tag="koba_far"))


# ------------------------------------------------------------------------------------------------ coverings
class _Sheet:
    """Open visual faces (tris / quads) with explicit uvs and outward hints, built band by band."""

    def __init__(self):
        self.v, self.f, self.uv, self.n = [], [], [], []

    def add(self, pts, uvs, n):
        kp, ku = [], []
        for q, w in zip(pts, uvs):
            if kp and math.dist(q, kp[-1]) < 1e-5:
                continue
            kp.append(q)
            ku.append(w)
        if len(kp) > 3 and math.dist(kp[0], kp[-1]) < 1e-5:
            kp.pop()
            ku.pop()
        if len(kp) < 3:
            return False
        self.f.append(list(range(len(self.v), len(self.v) + len(kp))))
        self.v += kp
        self.uv.append(ku)
        self.n.append(n)
        return True

    def band(self, ss, u0, u1, da, db, t0, t1, h0, h1, uvs, n, lo=0.0):
        """The face between u0 and u1 from d = da up to db, each side clipped at its top t (hip / ridge): a quad, a
        triangle where one side runs out, nothing above both tops. lo lifts the lower edge (a course step)."""
        a0, a1 = min(da, t0), min(da, t1)
        b0, b1 = min(db, t0), min(db, t1)
        if b0 - a0 < 1e-4 and b1 - a1 < 1e-4:
            return False
        su, sv = uvs
        pts = [ss.P3(u0, a0, h0 + lo), ss.P3(u1, a1, h1 + lo), ss.P3(u1, b1, h1), ss.P3(u0, b0, h0)]
        uv = [(u0 / su, -a0 / sv), (u1 / su, -a1 / sv), (u1 / su, -b1 / sv), (u0 / su, -b0 / sv)]
        return self.add(pts, uv, n)

    def solid(self, mat, vis, tag):
        return Solid(self.v, self.f, mat, vis=vis, uv=self.uv, normals=self.n, tag=tag)


def _dnodes(ss, first, eave_rows, step):
    top = ss.dmax()
    xs = [first] + list(eave_rows)
    d = xs[-1]
    while d + step < top:
        d += step
        xs.append(d)
    xs.append(top + 0.01)
    return xs


def _col_tops(ss, u):
    return ss.top(u)


def _kawara_field(part, ss, P):
    HC = K.HONG_COL
    um = (ss.u_lo + ss.u_hi) / 2
    covers = []
    k = 0
    while um + k * HC < ss.u_hi + HC:
        covers += [um + k * HC, um - k * HC]
        k += 1
    covers = sorted(set(round(c, 6) for c in covers))
    seams = [ss.u_lo] + [c for c in covers if ss.u_lo + 0.04 < c < ss.u_hi - 0.04] + [ss.u_hi]
    # the slope's depth jumps at the piece vertices (irimoya gable foot): a pan never straddles one
    seams = sorted(set(seams) | {u for u in ss.piece_us() if ss.u_lo < u < ss.u_hi})
    dn = _dnodes(ss, -0.06, (0.47,), 1.3)
    sh = _Sheet()
    lips = []
    pull = 0.06 if ss.hipped else 0.0
    for (a, b) in _pairs(seams):
        m = (a + b) / 2
        ta, tb, tm = ss.top(a + 1e-4) - pull, ss.top(b - 1e-4) - pull, ss.top(m) - pull
        for (da, db) in _pairs(dn):
            # one flat pan quad per column and segment (budget): the covers on the seams carry the relief
            sh.band(ss, a, b, da, db, ta, tb, 0.02, 0.02, (K.UVU, K.UVV), ss.normal(m, (da + db) / 2))
        # karakusa lip of the flat eave tile
        lo = mul(ss.up(m, 0.0), -1.0)
        lips.append(([ss.P3(a, -0.06, 0.03), ss.P3(b, -0.06, 0.03), ss.P3(b, -0.06, -0.035), ss.P3(a, -0.06, -0.035)],
                     lo))
    part.add(sh.solid(K.FIELD, (1,), "hongawara"))
    part.add(Solid([p for q, _ in lips for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(lips))],
                   K.TILE, vis=(1,), uv="fit", normals=[n for _, n in lips], tag="eave_tile"))
    # round covers (marugawara) on every seam: half-hexagon section along the curve, tomoe round ends at the eave
    r, hc = 0.075, 0.025
    cq, cn, discs = [], [], []
    breaks = set(ss.piece_us())
    for u in seams[1:-1]:
        if u in breaks:
            continue
        top = ss.top(u) - 0.03
        if top < 0.15:
            continue
        ds = [-0.045] + [d for d in dn[2:-1] if d < top] + [top]
        rings = []
        for d in ds:
            c = ss.P3(u, d, hc)
            n = ss.normal(u, d)
            a3 = norm((ss.ux, 0.0, ss.uz))
            a3 = norm(sub(a3, mul(n, dot(a3, n))))
            rings.append([add(c, add(mul(a3, r * math.cos(math.pi * j / 3)), mul(n, r * math.sin(math.pi * j / 3))))
                          for j in range(4)])
            if d == ds[0]:
                fwd = mul(ss.up(u, 0.0), -1.0)
                discs.append(([add(c, add(mul(a3, (r + 0.005) * math.cos(math.pi * j / 3)),
                                          mul(n, (r + 0.005) * math.sin(math.pi * j / 3)))) for j in range(6)], fwd))
        for i in range(len(rings) - 1):
            for j in range(3):
                cq.append([rings[i][j], rings[i + 1][j], rings[i + 1][j + 1], rings[i][j + 1]])
                ph = math.pi * (j + 0.5) / 3
                nn = ss.normal(u, ds[i])
                a3 = norm((ss.ux, 0.0, ss.uz))
                cn.append(norm(add(mul(a3, math.cos(ph)), mul(nn, math.sin(ph)))))
    if cq:
        part.add(Solid([p for q in cq for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(cq))],
                       K.TILE, vis=(1,), normals=cn, tag="cover", uv="fit"))
    if discs:
        part.add(Solid([p for q, _ in discs for p in q], [list(range(6 * i, 6 * i + 6)) for i in range(len(discs))],
                       K.TILE, vis=(1,), uv="fit", normals=[n for _, n in discs], tag="manju"))
    # far field (Res 2: ~1 ken x 1.4 m, Res 3: 2 ken x 2 m), matte far material (C16), between pans and cover tops
    for lods, st, cst, dstep in (((2,), KEN / 2, KEN / 4, 1.0), ((3,), KEN, KEN / 2, 1.4)):
        _far_field(part, ss, ss.u_breaks(st, cst), _dnodes(ss, -0.06, (), dstep), K.far_mat(), 0.05, lods,
                   "kawara_far", (K.UVU, K.UVV))
        # eave strip (the eave-tile row as one block) in the far LODs
        tipf = ss.hien_top if P["tiers"] == 2 else ss.base_top
        for poly in _eave_band(ss, -0.06, 0.22, st * 2 if lods == (3,) else st, mitre=False):
            if lods == (3,):           # Res 3: one block from the rafter tips (kayaoi + urako + eave tiles)
                b, _ = plane(poly, ss.at(lambda u, d: tipf(u, max(d, 0.0))), "under")
            else:
                b, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d) - 0.01), "under")
            t, _ = plane(poly, ss.at(lambda u, d: ss.cs(u, d) + 0.085), "under")
            part.add(slab(poly, b, t, K.TILE, vis=lods, tag="eave_strip"))


def _far_field(part, ss, us, dn, mat, h, lods, tag, uvs_):
    sh = _Sheet()
    for (a, b) in _pairs(us):
        ta, tb = ss.top(a + 1e-4), ss.top(b - 1e-4)     # each column's own side of a depth jump
        for (da, db) in _pairs(dn):
            sh.band(ss, a, b, da, db, ta, tb, h, h, uvs_, ss.normal((a + b) / 2, (da + db) / 2))
    if sh.f:
        part.add(sh.solid(mat, lods, tag))


def _board_field(part, ss, P):
    cov = P["covering"]
    mat = cover_mat(cov)
    from .core import mat_info
    su = sv = mat_info(mat)["tile"]
    us = ss.u_breaks(0.6, 0.45)
    expo = P["expo"]
    front = -0.045
    rows = [front + expo * (k + 1) for k in range(3)] if cov != "copper" else []
    dn = _dnodes(ss, front, rows, 0.70)
    sh = _Sheet()
    for (a, b) in _pairs(us):
        ta, tb = ss.top(a + 1e-4), ss.top(b - 1e-4)     # each column's own side of a depth jump
        for i, (da, db) in enumerate(_pairs(dn)):
            stepped = i < len(rows)
            lo = 0.012 if stepped else 0.0
            n = ss.normal((a + b) / 2, (da + db) / 2)
            if not sh.band(ss, a, b, da, db, ta, tb, 0.0, 0.0, (su, sv), n, lo=lo):
                continue
            if stepped and i > 0 and min(ta, tb) > da + 0.02:
                sh.add([ss.P3(a, da, 0.0), ss.P3(b, da, 0.0), ss.P3(b, da, lo), ss.P3(a, da, lo)],
                       [(a / su, -da / sv + 0.01), (b / su, -da / sv + 0.01), (b / su, -da / sv), (a / su, -da / sv)],
                       mul(ss.up((a + b) / 2, da), -1.0))
    part.add(sh.solid(mat, (1,), "board_field"))
    for lods, st, cst, dstep in (((2,), KEN / 2, KEN / 4, 1.0), ((3,), KEN, KEN / 2, 1.4)):
        _far_field(part, ss, ss.u_breaks(st, cst), _dnodes(ss, front, (), dstep), mat, 0.006, lods,
                   "board_field_lod", (su, sv))
    if cov == "copper":
        # standing-seam / batten ribs every 0.45 m (Res 1)
        rq, rn = [], []
        um = (ss.u_lo + ss.u_hi) / 2
        k = 0
        while um + k * 0.45 < ss.u_hi:
            for u in {um + k * 0.45, um - k * 0.45}:
                top = ss.top(u) - 0.03
                if top < 0.2 or u < ss.u_lo + 0.1 or u > ss.u_hi - 0.1:
                    continue
                ds = [front] + [d for d in dn[1:-1] if d < top][::2] + [top]
                for (da, db) in _pairs(ds):
                    a3 = (ss.ux, 0.0, ss.uz)
                    pa, pb = ss.P3(u, da, 0.0), ss.P3(u, db, 0.0)
                    na, nb = ss.normal(u, da), ss.normal(u, db)
                    w, hh = 0.015, 0.025
                    A = [add(pa, mul(a3, -w)), add(pa, mul(a3, w)), add(add(pa, mul(a3, w)), mul(na, hh)),
                         add(add(pa, mul(a3, -w)), mul(na, hh))]
                    B = [add(pb, mul(a3, -w)), add(pb, mul(a3, w)), add(add(pb, mul(a3, w)), mul(nb, hh)),
                         add(add(pb, mul(a3, -w)), mul(nb, hh))]
                    rq += [[A[0], B[0], B[3], A[3]], [A[1], A[2], B[2], B[1]], [A[3], B[3], B[2], A[2]]]
                    rn += [mul(a3, -1.0), a3, na]
            k += 1
        if rq:
            part.add(Solid([p for q in rq for p in q], [[4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3] for i in range(len(rq))],
                           mat, vis=(1,), normals=rn, tag="copper_seam", uv="fit"))


# ------------------------------------------------------------------------------------------------ ridges and hips
def _inset(poly, d):
    """A convex plan polygon moved in by d on every edge (Roadway kept off the shared cell edges)."""
    out = list(poly)
    n = len(poly)
    a2 = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    sg = 1.0 if a2 > 0 else -1.0
    for i in range(n):
        ax, az = poly[i]
        bx, bz = poly[(i + 1) % n]
        L = math.hypot(bx - ax, bz - az)
        if L < 1e-9:
            continue
        nx, nz = sg * (bz - az) / L, -sg * (bx - ax) / L           # outward normal
        out = clip_poly(out, nx, nz, nx * ax + nz * az - d)
        if len(out) < 3:
            return []
    return out


def small_oni(part, base, facing, height=0.34, width=0.28, vis=(1, 2, 3)):
    """A small ridge-end tile (sumi-oni / kudari-oni): ONE shouldered prism + a back block, in every LOD (cheap)."""
    f = norm(facing)
    side = norm(cross((0.0, 1.0, 0.0), f))
    t = 0.07
    h1 = height * 0.6
    prof = [(-width / 2, 0.0), (width / 2, 0.0), (width / 2, h1), (width * 0.3, height), (-width * 0.3, height),
            (-width / 2, h1)]
    verts = []
    for dz in (-t / 2, t / 2):
        for (x, y) in prof:
            verts.append(add(base, add(mul(side, x), add((0.0, y, 0.0), mul(f, dz)))))
    m = len(prof)
    faces = [list(range(m)), list(range(m, 2 * m))] + [[i, (i + 1) % m, m + (i + 1) % m, m + i] for i in range(m)]
    part.add(Solid(verts, faces, K.TILE, vis=vis, tag="small_oni"))
    c = add(base, add((0.0, height * 0.35, 0.0), mul(f, -t / 2 - 0.07)))
    part.add(oriented_box(c, side, (0.0, 1.0, 0.0), f, width * 0.3, height * 0.35, 0.07, K.TILE, vis=vis,
                          tag="small_oni"))


def _seg_box(part, a, b, w, h, mat, vis, tag, drop=0.0, ext=0.02):
    d, e1, e2 = frame_of(sub(b, a))
    L = math.dist(a, b) / 2 + ext
    c = add(mul(add(a, b), 0.5), mul(e2, h / 2 - drop))
    part.add(oriented_box(c, d, e2, e1, L, h / 2, w / 2, mat, vis=vis, tag=tag))
    return d, e1, e2


def _polyline_ridge(part, pts, kawara, mat, lods_cap=(1,), w=0.24, h=0.15, cap=0.085, tag="hip"):
    """A ridge stack along a curved polyline: one box per segment (every LOD) + a half-round cap (Res 1 / 2)."""
    segs = _pairs(pts)
    coarse = pts[::2] if (len(pts) - 1) % 2 == 0 else pts[::2] + [pts[-1]]
    for a, b in _pairs(coarse):
        _seg_box(part, a, b, w, h, K.TILE if kawara else mat, (3,), tag, drop=0.06)
    for i, (a, b) in enumerate(segs):
        d, e1, e2 = _seg_box(part, a, b, w, h, K.TILE if kawara else mat, (1, 2), tag, drop=0.06)
        if kawara and cap > 0:
            aa = add(a, mul(e2, h - 0.06))
            bb = add(b, mul(e2, h - 0.06))
            # the cap overlaps its neighbours at the kinks but never runs past the stack's ends (C15: the far LODs
            # keep the stack only)
            e0 = 0.0 if i == 0 else 0.02
            e1_ = 0.0 if i == len(segs) - 1 else 0.02
            part.add(half_tube(add(aa, mul(d, -e0)), add(bb, mul(d, e1_)), cap, K.TILE, n=3, vis=lods_cap,
                               tag=tag + "_cap"))


def _ridges(part, sls, P, info, form, W, D, gl, gr, zr, courses, walkable):
    cov = P["covering"]
    kawara = cov == "hongawara"
    mat = cover_mat(cov) if not kawara else K.TILE
    fr = sls[0]
    lift_top = 0.06 if kawara else P["top"]
    if form in ("kirizuma", "nagare"):
        x0, x1 = -gl, W + gr
    elif form == "irimoya":
        x0, x1 = D / 4, W - D / 4
    else:
        x0, x1 = D / 2, W - D / 2
    yb = max(fr.cs(fr.ud(x, zr)[0], fr.ud(x, zr)[1]) for x in (x0, (x0 + x1) / 2, x1)) + lift_top - 0.02
    info["ridge"] = ((x0, yb, zr), (x1, yb, zr))
    part.memory["sori_ridge"] = [(x0, yb, zr), (x1, yb, zr)]
    if x1 - x0 > 0.3:
        if kawara:
            # the mortar bed in every LOD at the stack's width (the kit's wider Res 1 / 2 mortar stands 3 cm past the
            # far block; on a steep sori ridge that drop is > 0.10 m: C15)
            part.add(box(x0 + 0.03, x1 - 0.03, yb, yb + 0.04, zr - 0.15, zr + 0.15, "wall_shikkui", vis=(1, 2, 3),
                         tag="mortar"))
            top = K.ridge(part, (x0 + 0.04, yb + 0.04, zr), (x1 - 0.04, yb + 0.04, zr), courses=courses, width=0.30,
                          cap_d=0.22, mortar=False) + 0.04
            oh = 0.40 + 0.03 * courses
            for x, f in ((x0, (-1.0, 0.0, 0.0)), (x1, (1.0, 0.0, 0.0))):
                K.onigawara(part, (x + (0.04 if f[0] < 0 else -0.04), yb - 0.02, zr), f, height=oh, width=0.48)
            info["ridge_top_y"] = round(yb + top, 3)
        else:
            hb = 0.36
            poly = [(yb - 0.12, zr - 0.22), (yb + hb - 0.06, zr - 0.22), (yb + hb, zr - 0.12), (yb + hb, zr + 0.12),
                    (yb + hb - 0.06, zr + 0.22), (yb - 0.12, zr + 0.22)]
            part.add(prism(poly, "x", x0, x1, {"default": mat}, vis=(1, 2, 3), tag="box_ridge", uvscale=(1.0, 1.0)))
            info["ridge_top_y"] = round(yb + hb, 3)
        if walkable:
            yt = info["ridge_top_y"] - (0.05 if kawara else 0.0)
            part.add(box(x0 + 0.05, x1 - 0.05, yb - 0.30, yt, zr - 0.14, zr + 0.14, "roof_kawara" if kawara else
                         "wood_weathered", vis=(), geo=True, view=True, fire=P["fire"], tag="ridge_geo"))
            part.road([(x0 + 0.05, yt, zr - 0.12), (x1 - 0.05, yt, zr - 0.12), (x1 - 0.05, yt, zr + 0.12),
                       (x0 + 0.05, yt, zr + 0.12)], P["surf"])
    else:
        # hogyo (W == D yosemune): a finial block at the apex (W2P1's hoju can stand on it)
        part.add(box(x0 - 0.22, x0 + 0.22, yb - 0.10, yb + 0.30, zr - 0.22, zr + 0.22, mat, vis=(1, 2, 3),
                     tag="apex_block"))
        info["ridge_top_y"] = round(yb + 0.30, 3)
        info["apex"] = (x0, yb + 0.30, zr)
    # corner ridges (sumimune) down the curved hips + small oni at the eave corners
    if form in ("irimoya", "yosemune"):
        for ss in sls:
            if ss.name not in ("front", "back"):
                continue
            for end in (0, 1):
                u_c = ss.u_lo if end == 0 else ss.u_hi
                sg = 1.0 if end == 0 else -1.0
                tmax = (ss.ov + (D / 4 if form == "irimoya" else D / 2))
                ts = [0.05 + (tmax - 0.05) * k / 4 for k in range(5)]
                pts = []
                for t in ts:
                    x, z = ss.xz(u_c + sg * t, t)
                    pts.append((x, ss.cs(u_c + sg * t, t) + lift_top, z))
                _polyline_ridge(part, pts[::-1], kawara, mat, tag="sumimune")
                if kawara:
                    hx, hz = -(ss.ux * sg + ss.ix) / math.sqrt(2), -(ss.uz * sg + ss.iz) / math.sqrt(2)
                    small_oni(part, (pts[0][0] + hx * 0.02, pts[0][1] - 0.02, pts[0][2] + hz * 0.02), (hx, 0.0, hz),
                              height=0.36, width=0.30)
        if form == "irimoya":
            # tsutsumi: the strip at the foot of each upper gable, over the top edge of the side slope
            for ss in sls:
                if ss.name not in ("left", "right"):
                    continue
                dtop = ss.ov + D / 4
                ua, ub = ss.u_lo + dtop, ss.u_hi - dtop
                a = ss.P3(ua + 0.05, dtop - 0.12, 0.0)
                b = ss.P3(ub - 0.05, dtop - 0.12, 0.0)
                y = max(a[1], b[1]) + lift_top
                a, b = (a[0], y, a[2]), (b[0], y, b[2])
                if kawara:
                    K.ridge(part, a, b, courses=2, width=0.26, cap_d=0.16, mortar=False, end_tiles=False, tag="tsutsumi")
                else:
                    _seg_box(part, a, b, 0.28, 0.12, mat, (1, 2, 3), "tsutsumi", drop=0.04, ext=0.0)


def _verges(part, sls, P, info, form, W, D, gl, gr, zr, hmat, hh):
    """Curved hafu boards (+ gegyo at the apex) on the gable verges; kawara: descending ridges along the verges."""
    cov = P["covering"]
    kawara = cov == "hongawara"
    lift_top = 0.06 if kawara else P["top"]
    if form == "yosemune":
        return
    verges = []                 # (slope, u at the verge, outward sign along u, d from, d to)
    for ss in sls:
        if ss.name not in ("front", "back"):
            continue
        if form == "irimoya":
            dfoot = ss.ov + D / 4
            a = ss.u_lo + dfoot
            b = ss.u_hi - dfoot
            verges += [(ss, a, -1.0, dfoot - 0.30, ss.R), (ss, b, 1.0, dfoot - 0.30, ss.R)]
        else:
            verges += [(ss, ss.u_lo, -1.0, -0.10, ss.R), (ss, ss.u_hi, 1.0, -0.10, ss.R)]
    th = 0.05
    for ss, uv, sg, d0, d1 in verges:
        ds = [d0 + (d1 - d0) * k / 6 for k in range(7)]
        a3 = (ss.ux * sg, 0.0, ss.uz * sg)

        def pt(d, off_u, dy):
            x, z = ss.xz(uv, max(min(d, d1), -0.2))
            y = ss.cs(uv - sg * 0.02, max(d, 0.0)) + (ss.P["t0"] * d if d < 0 else 0.0) + lift_top + 0.04 + dy
            return (x + a3[0] * off_u, y, z + a3[2] * off_u)
        for lods, step in (((1, 2), 1), ((3,), 3)):
            for i in range(0, 6, step):
                da, db = ds[i], ds[min(i + step, 6)]
                c = [pt(da, 0.0, -hh), pt(db, 0.0, -hh), pt(db, th, -hh), pt(da, th, -hh),
                     pt(da, 0.0, 0.0), pt(db, 0.0, 0.0), pt(db, th, 0.0), pt(da, th, 0.0)]
                part.add(hexa(c, hmat, vis=lods, tag="hafu", grain="long"))
        # gegyo: the hanging fin under the apex (only on the front slope's verges: one per gable)
        if ss.name == "front":
            apex = pt(d1, th / 2, 0.0)
            ax, az = ss.ix, ss.iz
            prof = [(-0.30, -hh + 0.02), (0.30, -hh + 0.02), (0.22, -hh - 0.40), (0.0, -hh - 0.55), (-0.22, -hh - 0.40)]
            verts = []
            for o in (-th / 2 + 0.005, th / 2 - 0.005):
                for (s_, y_) in prof:
                    verts.append((apex[0] + ax * s_ + a3[0] * o, apex[1] + y_, apex[2] + az * s_ + a3[2] * o))
            n = len(prof)
            faces = [list(range(n)), list(range(n, 2 * n))] + [[i, (i + 1) % n, n + (i + 1) % n, n + i] for i in range(n)]
            part.add(Solid(verts, faces, hmat, vis=(1, 2, 3), tag="gegyo"))
        if kawara:
            # kudarimune: the descending ridge along the verge strip, small oni at its foot
            ui = uv - sg * 0.15
            dd = [d for d in ds if d >= max(d0 + 0.30, 0.35)]
            if form in ("kirizuma", "nagare"):
                dd = [d for d in dd if d <= d1 - 0.30]
            else:
                dd = [d for d in dd if d <= d1 - 0.30]
            pts = [(ss.xz(ui, d)[0], ss.cs(ui, d) + lift_top, ss.xz(ui, d)[1]) for d in dd]
            if len(pts) >= 2:
                _polyline_ridge(part, pts[::-1], True, K.TILE, w=0.24, h=0.17, tag="kudarimune")
                f = mul(ss.up(ui, dd[0]), -1.0)
                fh = norm((f[0], 0.0, f[2]))
                small_oni(part, (pts[0][0] + fh[0] * 0.02, pts[0][1] - 0.01, pts[0][2] + fh[2] * 0.02), fh,
                          height=0.34, width=0.28)


# ------------------------------------------------------------------------------------------------ hooks
def under(info, x, z):
    """The lowest roof member (rafter underside) over a plan point, or None outside the roof: for walls, brackets and
    gables that must stay under the roof (C12)."""
    best = None
    for ss in info["sori"]:
        for pc in ss.pieces:
            if R._inside(pc, x, z):
                u, d = ss.ud(x, z)
                y = (ss.hien_bot(u, d) if (ss.P["tiers"] == 2 and d < ss.d_k) else ss.base_bot(u, d))
                best = y if best is None else min(best, y)
    return best


def _cov_of(fam):
    return {"hongawara": "hongawara", "sangawara": "hongawara", "hiwada": "hiwada", "copper": "copper"}.get(fam, "kokera")


def nagare(part, S):
    """W2P1's curve hook (nagare.nagare(..., curve=sori.nagare)): the curved nagare roof from W2P1's nagare_spec S
    (W, D, front, back_ov, gov, fam, t, eave_y, drop, kohai_xs, kohai_z). The planar pitch t becomes the sori pair
    (0.93 t at the eave, t + 0.35 at the ridge); itabuki -> thick kokera, sangawara / hongawara -> hongawara; the back
    rafters bear on the keta at eave_y, the front rafters (curved, thin over the porch) on the kohai beam at kohai_z,
    which W2P1's kohai_frame builds under the tangent of the front rafters there. Returns (slopes, info)."""
    t = S["t"]
    ov = S["back_ov"]
    sls, info = roof(part, S["W"], S["D"], form="nagare", covering=_cov_of(S["fam"]), bear_y=S["eave_y"], ov=ov,
                     gov=S["gov"], pitch=(round(0.93 * t, 3), round(t + 0.35, 3)), front_ext=S["front"] - ov,
                     front_bear_z=S.get("kohai_z"))
    if S.get("kohai_xs") and S.get("kohai_z") is not None:
        from . import nagare as NG
        fs = sls[0]
        zp = S["kohai_z"]
        um = (fs.u_lo + fs.u_hi) / 2
        d = fs.ov - zp
        y = fs.base_bot(um, d)
        slope = (fs.base_bot(um, d + 0.01) - fs.base_bot(um, d - 0.01)) / 0.02     # rise per m inward (-z)
        # W2P1's rafter plane y = eave_y - t z: the tangent of the curved front rafters at the kohai line (under the
        # convex curve everywhere, so its beam and tie beams never poke into the roof)
        info["kohai"] = NG.kohai_frame(part, S["kohai_xs"], zp, slope, y + slope * zp, S["drop"])
    info["spec"] = S
    return sls, info


def kohai_fit(info, slope="front"):
    """The planar stand-in of a curved roof's eave for W2P1's straight kohai canopy (nagare.kohai(main_t=, main_ov=,
    eave_y=)): the flying-rafter underside plane of the slope's middle (the curve only rises inward of it, so a canopy
    tucked under this plane stays under the curved roof). Returns dict(main_t, main_ov, eave_y)."""
    ss = next(q for q in info["sori"] if q.name == slope)
    um = (ss.u_lo + ss.u_hi) / 2
    f = ss.hien_bot if ss.P["tiers"] == 2 else ss.base_bot
    y0, y1 = f(um, 0.0), f(um, 0.3)
    t = (y1 - y0) / 0.3
    return {"main_t": round(t, 4), "main_ov": round(ss.ov, 4), "eave_y": round(y0 + t * ss.ov, 4)}


def nagare_curved(part, W, D, front_ext=None, covering="hiwada", **kw):
    """Hook for W2P1's jp_p_roof_nagare (curved version): a nagare roof is a kirizuma whose front slope runs on over
    the steps. W2P1's module can call this when asked for a curved roof, e.g.
        if curved: return sori.nagare_curved(part, W, D, front_ext=porch_depth, covering=covering)
    (front_ext default 1 ken). The front slope shares the ridge, its eave falls lower; info['front_bear_y'] is the
    height its porch beam (kohai) must carry at z = front_ext."""
    return roof(part, W, D, form="nagare", covering=covering, front_ext=KEN if front_ext is None else front_ext,
                **kw)


# ------------------------------------------------------------------------------------------------ parts library
SORI_VARIANTS = {
    "_irimoya_hongawara": ("irimoya", "hongawara", "town temple / shrine hall: curved irimoya, hongawara, 7-course ridge"),
    "_irimoya_kokera": ("irimoya", "kokera", "shrine haiden / temple hall: curved irimoya, thick kokera with the koba edge"),
    "_irimoya_hiwada": ("irimoya", "hiwada", "high-rank shrine hall: curved irimoya, hiwada bark (stand-in material)"),
    "_irimoya_copper": ("irimoya", "copper", "rich hall / castle-grade: curved irimoya, copper (stand-in material)"),
    "_kirizuma_hongawara": ("kirizuma", "hongawara", "temple gate / sutra store: curved kirizuma, hongawara"),
    "_kirizuma_hiwada": ("kirizuma", "hiwada", "shrine gate / honden: curved kirizuma, hiwada (stand-in material)"),
    "_hogyo_copper": ("yosemune", "copper", "small square hall (hogyo pyramid): curved hip roof, copper (stand-in)"),
    "_nagare_hiwada": ("nagare", "hiwada", "nagare honden (W2P1 hook): the front slope runs 1 ken on over the steps"),
}


def part_sori(variant):
    form, cov, used = SORI_VARIANTS[variant]
    W, D = (2 * KEN, 2 * KEN) if form in ("yosemune", "nagare") else (3 * KEN, 2 * KEN)
    p = Part("jp_p_roof_sori", variant, "roof", tiers=[2, 3], used_for=used,
             recipe="sori.roof(part, W, D, form, covering, bear_y, g_out, ov, gov, pitch=(t0, t1), curve=p, "
                    "corner_lift, lift_span, tiers)  [nagare: sori.nagare_curved / sori.nagare(part, W2P1 spec)]",
             datum="%.2f x %.2f column grid, x along the ridge, z 0 front column line .. -D; y 0 = floor; rafters "
                   "bear on a keta at the column line, top %.2f" % (W, D, EAVE_Y))
    if form == "nagare":
        sls, info = nagare_curved(p, W, D, covering=cov, bear_y=EAVE_Y)
    else:
        sls, info = roof(p, W, D, form=form, covering=cov, bear_y=EAVE_Y)
    p.dim("pitch_eave_rate", "0.30-0.50", info["t0"], tol=0.0, source="W2P2_NOTES §2 (GK: 3-5 sun at the eave)")
    p.dim("pitch_ridge_rate", "0.70-1.00", info["t1"], tol=0.0, source="W2P2_NOTES §2 (GK: 7-10 sun at the top)")
    p.dim("curve_depth_m", "0.10-0.40", info["curve_depth_m"], tol=0.0, source="sag under the eave-ridge chord")
    p.dim("corner_lift_m", "0.15-0.50", info["corner_lift_m"], tol=0.0, source="W2P2_NOTES §2 (GK)")
    p.dim("eave_overhang_m", "1.0-2.6", info["ov"], tol=0.0, source="W2P2_NOTES §2 (GK)")
    for x, z in ((0, 0), (W, 0), (0, -D), (W, -D)):
        p.conn("post", (x, 0, z), note="column grid corner")
    p.conn("eave", (0, EAVE_Y, 0), note="bear_y: the keta (or gangyo, g_out outside) the rafters rest on")
    a, b = info["ridge"]
    p.conn("ridge", a, note="ridge start")
    p.conn("ridge", b, note="ridge end")
    if MISSING and cov in ("hiwada", "copper"):
        p.notes.append("Stand-in material (missing from the library: %s); the generator switches automatically."
                       % ", ".join(MISSING))
    return p


def register(reg):
    reg("jp_p_roof_sori", list(SORI_VARIANTS), part_sori)
