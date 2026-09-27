"""Heightmap composition for the 2048 m test island (numpy only).

Grid: 512 x 512 vertices at 4.0 m (vertex (i, j) at x = 4i, z = 4j; row 0 = south, as 8WVR stores it).

Layers, in order:
  1. coast      : an irregular island outline r(theta) around (1024, 1024); d = r(theta) - rho is the
                  (approximate) distance inland from the waterline, negative at sea
  2. base       : sea floor (down to ~-32 m at the map edge), a 1:14 beach, then a coastal terrace rising to
                  ~27 m around the yard
  3. hills      : a real GSI DEM5A patch from Hakone (relief above its 5th percentile, scaled so the
                  highest summit is ~HILL_TOP m), faded in away from the yard and away from the coast, full
                  strength on the north / west side of the island
  4. road bed   : terrain eased towards a smoothed profile along the gravel road centre line
  5. canal      : a sea-level canal cut (bottom -2.5 m) into the east coast
  6. pond basin : a flat-bottomed dip for the above-sea-level pond
  7. yard       : exactly 25.0 m on the 200 x 200 m square centred (1024, 1024), smooth blend around it
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

WORLD = 2048.0
N = 512
CELL = WORLD / N                       # 4.0 m
CENTRE = (1024.0, 1024.0)
YARD_HALF = 100.0
YARD_H = 25.0
YARD_BLEND = 70.0
HILL_TOP = 190.0


def grid():
    j, i = np.mgrid[0:N, 0:N].astype(np.float64)
    return i * CELL, j * CELL           # X, Z (row = z)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def gauss_blur(a, sigma_px):
    """Separable gaussian blur, reflect-padded (numpy only)."""
    if sigma_px <= 0:
        return a
    r = int(math.ceil(3 * sigma_px))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_px) ** 2)
    k /= k.sum()
    p = np.pad(a, r, mode="reflect")
    tmp = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, p)
    return np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 0, tmp)


def coast_radius(theta, seed=7):
    """Island outline in metres as a function of the polar angle (0 = east, counter-clockwise)."""
    rng = np.random.default_rng(seed)
    r = np.full_like(theta, 690.0)
    for k, amp in ((2, 55.0), (3, 45.0), (5, 22.0), (7, 14.0), (11, 8.0), (17, 5.0)):
        r += amp * np.cos(k * theta + rng.uniform(0, 2 * np.pi))
    return r


ISLAND_CENTRE = (1024.0, 1150.0)      # the island sits north of the yard: beach + plain south, hills north


def coast_distance(X, Z):
    dx, dz = X - ISLAND_CENTRE[0], Z - ISLAND_CENTRE[1]
    rho = np.hypot(dx, dz)
    theta = np.arctan2(dz, dx)
    return coast_radius(theta) - rho, theta


def seg_distance(X, Z, pts):
    """Distance from every grid point to a polyline, and the along-line parameter (metres) of the closest point."""
    best = np.full(X.shape, np.inf)
    along = np.zeros(X.shape)
    acc = 0.0
    for (x0, z0), (x1, z1) in zip(pts[:-1], pts[1:]):
        vx, vz = x1 - x0, z1 - z0
        L2 = vx * vx + vz * vz
        t = np.clip(((X - x0) * vx + (Z - z0) * vz) / L2, 0, 1)
        px, pz = x0 + t * vx, z0 + t * vz
        dd = np.hypot(X - px, Z - pz)
        m = dd < best
        best[m] = dd[m]
        along[m] = acc + t[m] * math.sqrt(L2)
        acc += math.sqrt(L2)
    return best, along


def resample_patch(patch, patch_mpp, X, Z, origin, rotate_deg=0.0):
    """Bilinear sample of a north-up DEM patch (row 0 = north) at world X/Z; origin = world (x, z) of the
    patch centre. Rotation turns the patch clockwise on the island."""
    ph, pw = patch.shape
    t = math.radians(rotate_deg)
    ux = (X - origin[0])
    uz = (Z - origin[1])
    lx = ux * math.cos(t) - uz * math.sin(t)
    lz = ux * math.sin(t) + uz * math.cos(t)
    col = lx / patch_mpp + pw / 2.0
    row = -lz / patch_mpp + ph / 2.0
    col = np.clip(col, 0, pw - 1.001)
    row = np.clip(row, 0, ph - 1.001)
    c0 = np.floor(col).astype(int)
    r0 = np.floor(row).astype(int)
    fc, fr = col - c0, row - r0
    a = patch
    return (a[r0, c0] * (1 - fc) * (1 - fr) + a[r0, c0 + 1] * fc * (1 - fr)
            + a[r0 + 1, c0] * (1 - fc) * fr + a[r0 + 1, c0 + 1] * fc * fr)


def yard_distance(X, Z):
    """Distance outside the yard square (0 inside)."""
    ax = np.maximum(np.abs(X - CENTRE[0]) - YARD_HALF, 0)
    az = np.maximum(np.abs(Z - CENTRE[1]) - YARD_HALF, 0)
    return np.hypot(ax, az)


def compose(patch, patch_mpp, layout):
    """Return dict of arrays: h (final heights), d (coast distance), masks used later for surfaces."""
    X, Z = grid()
    d, theta = coast_distance(X, Z)

    # -- 2. base: sea floor, beach, coastal terrace -------------------------------------------------
    sea = -2.0 * (1 - np.exp(d / 50.0)) - 30.0 * (1 - np.exp(d / 380.0))
    dl = np.clip(d, 0, None)
    land = 3.0 * (1 - np.exp(-dl / 40.0)) + 24.0 * smoothstep(30.0, 560.0, dl)   # ~1:13 beach, then the plain
    base = np.where(d < 0, sea, land)

    # -- 3. hills from the DEM patch ---------------------------------------------------------------
    dem = resample_patch(patch, patch_mpp, X, Z, layout["patch_origin"], layout.get("patch_rotate", 0.0))
    ref = np.percentile(patch, 5)
    top = np.percentile(patch, 99.5) - ref
    vscale = min(1.0, HILL_TOP / top)
    rel = np.clip(dem - ref, 0, None) * vscale
    dy = yard_distance(X, Z)
    away_from_yard = smoothstep(50.0, 420.0, dy)
    # full strength north of the yard, less on the flanks, little on the southern plain
    ang = np.arctan2(Z - CENTRE[1], X - CENTRE[0])            # 0 = east, pi/2 = north
    north = smoothstep(-0.9, 0.9, np.sin(ang))
    from_coast = smoothstep(5.0, 300.0, d)
    side = 0.1 + 0.9 * north
    hills = rel * away_from_yard * from_coast * side
    h = base + hills

    # -- 3b. pads: flatten small areas for placed buildings (level = natural height at the centre) ---
    pad_levels = []
    for (px, pz, half, blend) in layout.get("pads", []):
        lvl = bilinear(h, px, pz)
        ax = np.maximum(np.abs(X - px) - half, 0)
        az = np.maximum(np.abs(Z - pz) - half, 0)
        w = smoothstep(0.0, blend, np.hypot(ax, az))
        h = lvl + (h - lvl) * w
        pad_levels.append(lvl)

    # -- 4. road bed: a grade-limited profile along the centre line, cut / filled into the slope -------
    road = layout["road"]
    rd, along = seg_distance(X, Z, road)
    smooth = gauss_blur(h, 3.0)                                 # ~12 m smoothing of the natural ground
    pts = np.array(road, float)
    seg = np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1]))
    cum = np.concatenate(([0.0], np.cumsum(seg)))
    s = np.arange(0.0, cum[-1] + 1e-6, 2.0)
    px_ = np.interp(s, cum, pts[:, 0])
    pz_ = np.interp(s, cum, pts[:, 1])
    nat = np.array([bilinear(smooth, a, b) for a, b in zip(px_, pz_)])
    g = layout.get("road_max_grade", 0.13) * 2.0
    prof = nat.copy()
    prof[0] = YARD_H if yard_distance(np.array(px_[0]), np.array(pz_[0])) == 0 else nat[0]
    for k in range(1, len(prof)):
        prof[k] = min(max(nat[k], prof[k - 1] - g), prof[k - 1] + g)
    target = np.interp(along, s, prof)
    hw = layout["road_half_width"]
    rw = 1.0 - smoothstep(hw + 1.0, hw + 12.0, rd)
    h = h * (1 - rw) + target * rw
    road_profile = (s, prof, nat)

    # -- 5. canal: sea-level cut into the east coast ----------------------------------------------
    cd, _ = seg_distance(X, Z, layout["canal"])
    cw = layout["canal_half_width"]
    canal_floor = -2.5
    bank = smoothstep(cw, cw + 10.0, cd)                       # 0 in the canal, 1 on the banks
    canal_h = canal_floor + (h - canal_floor) * bank
    h = np.where(cd < cw + 10.0, np.minimum(h, canal_h), h)

    # -- 6. pond basin ----------------------------------------------------------------------------
    px, pz, pr, plevel = layout["pond"]
    if plevel is None:
        plevel = round(bilinear(h, px, pz) - 0.4, 1)
    pdist = np.hypot(X - px, Z - pz)
    # flatten a bench around the pond to the water level + 0.6 m, then dig the basin 1.8 m below water level
    bench = 1.0 - smoothstep(pr + 6.0, pr + 34.0, pdist)
    h = h * (1 - bench) + (plevel + 0.6) * bench
    basin = 1.0 - smoothstep(pr - 10.0, pr + 2.0, pdist)
    h = h - basin * (0.6 + 1.8)

    # -- 7. the yard: exactly 25.0 m, smooth blend -------------------------------------------------
    w = smoothstep(0.0, YARD_BLEND, dy)
    h = YARD_H + (h - YARD_H) * w
    h[dy == 0] = YARD_H

    return {"h": h.astype(np.float32), "d": d, "X": X, "Z": Z, "road_d": rd, "road_along": along,
            "canal_d": cd, "pond_d": pdist, "yard_d": dy, "hills": hills, "vscale": vscale, "ref": ref,
            "road_profile": road_profile, "pad_levels": pad_levels, "road_half_width": hw,
            "canal_half_width": cw, "pond_r": pr, "pond_level": plevel}


def bilinear(h, x, z):
    """Terrain height at world (x, z) - same interpolation as the engine on a regular grid (two triangles per
    cell differ from bilinear by a few cm on smooth ground)."""
    fx, fz = x / CELL, z / CELL
    i = min(max(int(math.floor(fx)), 0), N - 2)
    j = min(max(int(math.floor(fz)), 0), N - 2)
    u, v = fx - i, fz - j
    return float(h[j, i] * (1 - u) * (1 - v) + h[j, i + 1] * u * (1 - v) + h[j + 1, i] * (1 - u) * v
                 + h[j + 1, i + 1] * u * v)


def slope_deg(h):
    gz, gx = np.gradient(h.astype(np.float64), CELL)
    return np.degrees(np.arctan(np.hypot(gx, gz)))
