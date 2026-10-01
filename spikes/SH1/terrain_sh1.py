"""SH1 terrain helpers: the test island's heightmap (data/T_terrain/render_input.npz, written by T's build_world.py;
the placements never change the terrain) sampled exactly like T's Placer (bilinear on the 4 m grid), plus the stair
fitter for the hillside shrine stair.

Stair modules (W2, src/JP/site/shrine/jp_s_stone_steps.prop.json): foot connector (0,0,0), head (0, rise, -run);
blocks reach 0.12 (rough 0.13) under the ramp line; a landing is a 0.18 slab, top at 0. A flight's ramp line runs
through the inner tread corners, so the terrain must stay UNDER the ramp line (else it pokes through the treads) and
OVER ramp - 0.12 (else the blocks float). On this hill (12-40 %) the 52.7 % flights outrun the terrain, so every flight
is followed by a landing whose VISIBLE length lets the terrain catch up; the rest of that landing slab runs on under
the next flight and into the slope (hidden). The fitter picks the visible lengths.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "T_terrain", "tools"))
import terrain  # noqa: E402

_H = None


def H():
    global _H
    if _H is None:
        _H = np.load(os.path.join(DEV, "data", "T_terrain", "render_input.npz"))["h"]
    return _H


def ground(x, z):
    return float(terrain.bilinear(H(), x, z))


def trees():
    return np.load(os.path.join(DEV, "data", "T_terrain", "render_input.npz"))["trees"]


def seat(x, z, half_w, half_d, yaw, sink_frac=0.0):
    """y_offset that puts a footprint (half sizes in the model frame, yaw clockwise from north) on its LOWEST corner
    (nothing floats; the uphill side is buried by the slope). Returns (y_offset, rise across the footprint)."""
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    gs = []
    for ax in (-half_w, 0.0, half_w):
        for az in (-half_d, 0.0, half_d):
            # model x -> world (cos, -sin), model z -> world (sin, cos) for yaw clockwise from +z
            wx = x + ax * c + az * s
            wz = z - ax * s + az * c
            gs.append(ground(wx, wz))
    g0 = ground(x, z)
    lo, hi = min(gs), max(gs)
    return lo - g0 + sink_frac * (hi - lo), hi - lo


# ------------------------------------------------------------------------------------------------ stair fitter
STEP_RISE, STEP_RUN = 0.16, 0.303
SLOPE = STEP_RISE / STEP_RUN


def flight_fit(x, s, y, run, rise, dep, sample=0.05):
    """(float, poke_first_tread, poke_rest) of a flight whose foot is at (x, s) height y."""
    fl = pk0 = pk = -9.0
    n = int(round(run / sample))
    for i in range(n + 1):
        t = i * run / n
        g = ground(x, s + t)
        ramp = y + rise * t / run
        if t < STEP_RUN - 1e-6:
            pk0 = max(pk0, g - ramp)             # terrain over the first tread: its riser starts in the soil
        else:
            pk = max(pk, g - ramp)               # terrain above the ramp line: pokes through the treads
        fl = max(fl, (ramp - dep) - g)           # block bottom above the terrain: floats
    return fl, pk0, pk


def fit_stair(x, z0, z_end, flights, landing, max_float=0.03, max_poke=0.03, max_foot=0.10, sample=0.05,
              pick=None):
    """A stair climbing north (+z) along x, starting at the first z >= z0 where a flight can be seated. flights:
    [(name, run, rise, depth_under_ramp)]; pick(i, z) -> the flight list to try for the i-th flight at z (default:
    flights). landing: (name, run, depth). Returns ([(name, x, z_foot, y_world, kind, length)], worst)."""
    pick = pick or (lambda i, z: flights)

    def fits(s, y, f):
        fl, pk0, pk = flight_fit(x, s, y, f[1], f[2], f[3], sample)
        mf = f[4] if len(f) > 4 else max_float       # a flight may carry its own float tolerance
        return fl <= mf and pk0 <= max_foot and pk <= max_poke, (fl, pk0, pk)

    # the first flight: scan for a foot where one fits with its first riser sunk 0..max_foot
    s = z0
    y = None
    while s < z_end:
        g = ground(x, s)
        for sink in (max_foot, 0.08, 0.06, 0.04, 0.02, 0.0):
            if any(fits(s, g - sink, f)[0] for f in pick(0, s)):
                y = g - sink
                break
        if y is not None:
            break
        s += sample
    if y is None:
        return [], {"float": None, "poke": None}
    mods = []
    worst = {"float": 0.0, "poke": 0.0, "foot": 0.0}
    nflight = 0
    while s < z_end:
        cand = [f for f in pick(nflight, s) if fits(s, y, f)[0]]
        if cand:
            f = cand[0]
            fl, pk0, pk = fits(s, y, f)[1]
            mods.append((f[0], x, s, y, "flight", f[1]))
            worst["float"] = max(worst["float"], fl)
            worst["poke"] = max(worst["poke"], pk)
            worst["foot"] = max(worst["foot"], pk0)
            s += f[1]
            y += f[2]
            nflight += 1
            continue
        # a landing at height y: visible until a flight fits (the terrain catches up with the stair)
        lname, lrun, ldep = landing
        vis = None
        best = None
        # the preferred flight (first in the list) wins if it can start anywhere on this landing; else the next
        for want in range(len(pick(nflight, s))):
            t = sample
            while t <= lrun + 1e-6:
                fl = pick(nflight, s + t)
                f = fl[min(want, len(fl) - 1)]
                if fits(s + t, y, f)[0]:
                    vis = t
                    break
                g = ground(x, s + t)
                if g - y > max_foot:              # overshot: the terrain is above the landing
                    break
                sc = fits(s + t, y, f)[1][0]
                if best is None or sc < best[0]:
                    best = (sc, t)
                t += sample
            if vis is not None:
                break
        if vis is None:
            vis = best[1] if best else sample
        for i in range(int(round(vis / sample)) + 1):
            g = ground(x, s + i * sample)
            worst["float"] = max(worst["float"], (y - ldep) - g)
            worst["poke"] = max(worst["poke"], g - y)
        mods.append((lname, x, s, y, "landing", vis))
        s += vis
        # force the flight after a landing that could not find a perfect start
        if not [f for f in pick(nflight, s) if fits(s, y, f)[0]]:
            f = pick(nflight, s)[-1]
            fl, pk0, pk = fits(s, y, f)[1]
            mods.append((f[0], x, s, y, "flight", f[1]))
            worst["float"] = max(worst["float"], fl)
            worst["poke"] = max(worst["poke"], pk)
            worst["foot"] = max(worst["foot"], pk0)
            s += f[1]
            y += f[2]
            nflight += 1
        if len(mods) > 400:
            break
    return mods, worst
