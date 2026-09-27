"""Object placement for the test island: road pieces, vegetation, rocks, the control house, the pond and the other
agents' test/placements/*.csv. Every object ends up as (p3d, engine position, aside, up, dir).

Engine position rule (see odol.py): pos = origin + bc.x*aside + bc.y*up + bc.z*dir, where origin is where the
model's MLOD origin should be (x, ground + y_offset, z) and aside/up/dir already carry the scale.
"""
import csv
import glob
import math
import os

import numpy as np

import terrain
import wrp8
from odol import model_center

P = "P:\\"

# ---- vanilla models ---------------------------------------------------------------------------------
PINES = [(r"dz\plants\tree\t_pinussylvestris_2s.p3d", 3), (r"dz\plants\tree\t_pinussylvestris_2sb.p3d", 2),
         (r"dz\plants\tree\t_pinussylvestris_3s.p3d", 1), (r"dz\plants\tree\t_pinussylvestris_2f.p3d", 3),
         (r"dz\plants\tree\t_pinussylvestris_3f.p3d", 2), (r"dz\plants\tree\t_pinussylvestris_1s.p3d", 1)]
BROADLEAF = [(r"dz\plants\tree\t_fagussylvatica_2f.p3d", 3), (r"dz\plants\tree\t_fagussylvatica_3f.p3d", 2),
             (r"dz\plants\tree\t_fagussylvatica_2s.p3d", 2), (r"dz\plants\tree\t_quercusrobur_2f.p3d", 2),
             (r"dz\plants\tree\t_quercusrobur_3f.p3d", 1), (r"dz\plants\tree\t_quercusrobur_2s.p3d", 1),
             (r"dz\plants\tree\t_carpinus_2s.p3d", 2), (r"dz\plants\tree\t_fraxinusexcelsior_2f.p3d", 1)]
SPRUCE = [(r"dz\plants\tree\t_piceaabies_2f.p3d", 3), (r"dz\plants\tree\t_piceaabies_3f.p3d", 2),
          (r"dz\plants\tree\t_piceaabies_2s.p3d", 1), (r"dz\plants\tree\t_piceaabies_1f.p3d", 1)]
BUSHES = [(r"dz\plants\bush\b_corylusavellana_1f.p3d", 2), (r"dz\plants\bush\b_corylusavellana_2s.p3d", 2),
          (r"dz\plants\bush\b_sambucusnigra_1s.p3d", 1), (r"dz\plants\bush\b_sambucusnigra_2s.p3d", 1),
          (r"dz\plants\bush\b_crataeguslaevigata_1s.p3d", 1), (r"dz\plants\bush\b_crataeguslaevigata_2s.p3d", 1),
          (r"dz\plants\bush\b_rosacanina_2s.p3d", 1), (r"dz\plants\bush\b_prunusspinosa_2s.p3d", 1),
          (r"dz\plants\bush\b_betulahumilis_1s.p3d", 1)]
ROCKS = [r"dz\rocks\rock_bright_apart1.p3d", r"dz\rocks\rock_bright_apart2.p3d", r"dz\rocks\rock_bright_monolith1.p3d",
         r"dz\rocks\rock_bright_monolith2.p3d", r"dz\rocks\rock_bright_monolith3.p3d", r"dz\rocks\rock_apart1.p3d",
         r"dz\rocks\rock_apart2.p3d"]
HOUSE = r"dz\structures\residential\houses\house_1w01.p3d"      # Land_House_1W01, vanilla loot house

# gravel road parts (dz\structures\roads\parts): straights by length, right-hand arcs by (degrees, radius)
ROAD_STRAIGHT = {6.25: "grav_6", 12.5: "grav_12", 25.0: "grav_25"}
ROAD_ARC = {(10.0, 25.0): "grav_10 25", (10.0, 50.0): "grav_10 50", (10.0, 75.0): "grav_10 75",
            (10.0, 100.0): "grav_10 100", (15.0, 75.0): "grav_15 75", (22.5, 50.0): "grav_22 50",
            (30.0, 25.0): "grav_30 25", (60.0, 10.0): "grav_60 10", (7.5, 100.0): "grav_7 100"}
ROAD_END = "grav_6konec"


class Placer:
    def __init__(self, h, log):
        self.h = h
        self.log = log
        self.bc_cache = {}
        self.objects = []          # dicts: p3d, pos, aside, up, dir, kind
        self.missing = []

    def bc(self, p3d):
        if p3d not in self.bc_cache:
            self.bc_cache[p3d] = model_center(os.path.join(P, p3d))
        return self.bc_cache[p3d]

    def ground(self, x, z):
        return terrain.bilinear(self.h, x, z)

    def place(self, p3d, x, z, yaw, y_offset=0.0, scale=1.0, pitch=0.0, roll=0.0, kind="object", y_abs=None):
        bc, how = self.bc(p3d)
        if bc is None:
            self.missing.append(p3d)
            return None
        aside, up, dirv = wrp8.yaw_matrix(yaw, scale, pitch, roll)
        gy = self.ground(x, z) if y_abs is None else y_abs
        origin = np.array([x, gy + y_offset, z])
        pos = origin + bc[0] * aside + bc[1] * up + bc[2] * dirv
        o = {"p3d": p3d, "pos": pos, "aside": aside, "up": up, "dir": dirv, "kind": kind, "yaw": yaw,
             "origin": origin, "bc_kind": how}
        self.objects.append(o)
        return o


# ---- road -------------------------------------------------------------------------------------------
def plan_road(start, yaw, steps):
    """steps: ('S', length) | ('R', deg, radius) | ('L', deg, radius) | ('END',).
    Returns (pieces [(p3d, x, z, yaw)], dense centre line [(x, z)])."""
    x, z = start
    psi = yaw
    pieces = []
    line = [(x, z)]

    def fwd(yw):
        t = math.radians(yw)
        return math.sin(t), math.cos(t)

    def right(yw):
        t = math.radians(yw)
        return math.cos(t), -math.sin(t)

    for st in steps:
        if st[0] == "S" or st[0] == "END":
            L = st[1] if st[0] == "S" else 6.25
            name = ROAD_STRAIGHT[L] if st[0] == "S" else ROAD_END
            pieces.append((r"dz\structures\roads\parts\%s.p3d" % name, x, z, psi))
            fx, fz = fwd(psi)
            for k in range(1, 6):
                line.append((x + fx * L * k / 5, z + fz * L * k / 5))
            x, z = x + fx * L, z + fz * L
        else:
            turn, deg, rad = st
            name = ROAD_ARC[(float(deg), float(rad))]
            a = math.radians(deg)
            ex, ez = rad * (1 - math.cos(a)), rad * math.sin(a)        # local end of a right-hand arc
            if turn == "R":
                ax, az = x, z
                apsi = psi
                pieces.append((r"dz\structures\roads\parts\%s.p3d" % name, ax, az, apsi))
                for k in range(1, 9):
                    t = a * k / 8
                    lx, lz = rad * (1 - math.cos(t)), rad * math.sin(t)
                    rx, rz = right(apsi)
                    fx, fz = fwd(apsi)
                    line.append((ax + rx * lx + fx * lz, az + rz * lx + fz * lz))
                rx, rz = right(apsi)
                fx, fz = fwd(apsi)
                x, z = ax + rx * ex + fx * ez, az + rz * ex + fz * ez
                psi = psi + deg
            else:
                apsi = psi - deg - 180.0
                rx, rz = right(apsi)
                fx, fz = fwd(apsi)
                ax, az = x - (rx * ex + fx * ez), z - (rz * ex + fz * ez)
                pieces.append((r"dz\structures\roads\parts\%s.p3d" % name, ax, az, apsi))
                for k in range(7, -1, -1):
                    t = a * k / 8
                    lx, lz = rad * (1 - math.cos(t)), rad * math.sin(t)
                    line.append((ax + rx * lx + fx * lz, az + rz * lx + fz * lz))
                x, z = ax, az
                psi = psi - deg
    return pieces, line


# ---- vegetation -------------------------------------------------------------------------------------
def pick(rng, table):
    names = [t[0] for t in table]
    w = np.array([t[1] for t in table], float)
    return names[rng.choice(len(names), p=w / w.sum())]


def forest_density(T, noise):
    h = T["h"].astype(np.float64)
    sl = terrain.slope_deg(h)
    hill = terrain.smoothstep(28.0, 70.0, h)
    grove = terrain.smoothstep(0.62, 0.75, noise) * terrain.smoothstep(6.0, 14.0, h) * 0.9
    F = np.maximum(hill * (0.55 + 0.6 * noise), grove)
    F *= np.where(sl > 43.0, 0.35, 1.0)
    excl = ((T["yard_d"] < 30.0) | (T["road_d"] < T["road_half_width"] + 7.0)
            | (T["canal_d"] < T["canal_half_width"] + 16.0) | (T["pond_d"] < T["pond_r"] + 14.0) | (h < 4.5))
    F[excl] = 0.0
    return np.clip(F, 0, 1)


def place_vegetation(pl, T, F, rng, pads, spacing=10.0):
    h = T["h"].astype(np.float64)
    blur = terrain.gauss_blur(h, 10.0)
    ridge = h - blur                                   # >0 ridge, <0 valley
    gz, gx = np.gradient(h, terrain.CELL)
    n_tree = n_bush = 0
    for zc in np.arange(spacing / 2, terrain.WORLD, spacing):
        for xc in np.arange(spacing / 2, terrain.WORLD, spacing):
            x = xc + rng.uniform(-0.45, 0.45) * spacing
            z = zc + rng.uniform(-0.45, 0.45) * spacing
            i, j = int(x / terrain.CELL), int(z / terrain.CELL)
            if not (0 <= i < terrain.N and 0 <= j < terrain.N):
                continue
            f = F[j, i]
            if f <= 0.02:
                continue
            if any(abs(x - px) < hw + 12 and abs(z - pz) < hw + 12 for (px, pz, hw) in pads):
                continue
            r = rng.random()
            if r < f * 0.92:
                north_facing = gz[j, i] < -0.15
                if ridge[j, i] > 1.5 or (h[j, i] > 120 and rng.random() < 0.5):
                    p3d = pick(rng, PINES)
                elif north_facing and h[j, i] > 60 and rng.random() < 0.6:
                    p3d = pick(rng, SPRUCE)
                else:
                    p3d = pick(rng, BROADLEAF)
                pl.place(p3d, x, z, rng.uniform(0, 360), scale=rng.uniform(0.82, 1.08), kind="tree")
                n_tree += 1
            elif r < f * 0.92 + 0.10 * (1 - abs(f - 0.4) * 1.5):
                pl.place(pick(rng, BUSHES), x, z, rng.uniform(0, 360), scale=rng.uniform(0.8, 1.15), kind="bush")
                n_bush += 1
    return n_tree, n_bush


def place_coastal_pines(pl, T, rng):
    """A black-pine style belt behind the southern beach (vanilla Scots pine standing in)."""
    n = 0
    d, h = T["d"], T["h"]
    for zc in np.arange(300, 1000, 9.0):
        for xc in np.arange(300, 1800, 9.0):
            x = xc + rng.uniform(-3, 3)
            z = zc + rng.uniform(-3, 3)
            i, j = int(x / terrain.CELL), int(z / terrain.CELL)
            if not (0 <= i < terrain.N and 0 <= j < terrain.N):
                continue
            if 42.0 < d[j, i] < 85.0 and h[j, i] > 2.6 and T["canal_d"][j, i] > T["canal_half_width"] + 14 \
                    and T["road_d"][j, i] > 12 and rng.random() < 0.55:
                p3d = rng.choice([r"dz\plants\tree\t_pinussylvestris_2s.p3d", r"dz\plants\tree\t_pinussylvestris_3s.p3d",
                                  r"dz\plants\tree\t_pinussylvestris_2sb.p3d"])
                pl.place(str(p3d), x, z, rng.uniform(0, 360), scale=rng.uniform(0.8, 1.05), kind="tree")
                n += 1
    return n


def place_rocks(pl, T, rng, n_slope=28, n_beach=8):
    h = T["h"].astype(np.float64)
    sl = terrain.slope_deg(h)
    js, is_ = np.nonzero((sl > 34) & (h > 20) & (T["road_d"] > 15) & (T["yard_d"] > 40))
    placed = 0
    if len(js):
        for k in rng.choice(len(js), size=min(n_slope, len(js)), replace=False):
            x = is_[k] * terrain.CELL + rng.uniform(-1.5, 1.5)
            z = js[k] * terrain.CELL + rng.uniform(-1.5, 1.5)
            p3d = str(rng.choice(ROCKS))
            _place_rock(pl, p3d, x, z, rng)
            placed += 1
    d = T["d"]
    js, is_ = np.nonzero((d > 4) & (d < 30) & (T["canal_d"] > 40) & (T["X"] > 1024))
    if len(js):
        for k in rng.choice(len(js), size=min(n_beach, len(js)), replace=False):
            _place_rock(pl, str(rng.choice(ROCKS[:2] + ROCKS[5:])), is_[k] * terrain.CELL, js[k] * terrain.CELL, rng, 0.55)
            placed += 1
    return placed


def _place_rock(pl, p3d, x, z, rng, scale=None):
    from odol import odol_info
    info = odol_info(os.path.join(P, p3d))
    s = scale if scale else rng.uniform(0.5, 0.9)
    height = (info["bmax"][1] - info["bmin"][1]) * s if info else 3.0
    # sink so the rock sits in the slope rather than on it: origin = ground - 25..40 % of its height,
    # measured from the bounding-box bottom
    bottom = (info["bc"][1] + info["bmin"][1]) * s if info else 0.0
    sink = rng.uniform(0.25, 0.4) * height
    pl.place(p3d, x, z, rng.uniform(0, 360), y_offset=-bottom - sink, scale=s,
             pitch=rng.uniform(-8, 8), roll=rng.uniform(-8, 8), kind="rock")


# ---- other agents' placements --------------------------------------------------------------------------
def read_placements(test_dir, log):
    rows = []
    for path in sorted(glob.glob(os.path.join(test_dir, "placements", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            for n, rec in enumerate(csv.reader(f)):
                if not rec or rec[0].strip().startswith("#"):
                    continue
                if rec[0].strip().lower() == "p3d":
                    continue
                try:
                    p3d = rec[0].strip().replace("/", "\\")
                    x, z, yaw = float(rec[1]), float(rec[2]), float(rec[3])
                    yoff = float(rec[4]) if len(rec) > 4 and rec[4].strip() else 0.0
                except (ValueError, IndexError):
                    log("  WARNING %s line %d unreadable: %r" % (os.path.basename(path), n + 1, rec))
                    continue
                rows.append((os.path.basename(path), p3d, x, z, yaw, yoff))
    return rows


def place_placements(pl, rows, log):
    ok = 0
    for src, p3d, x, z, yaw, yoff in rows:
        full = os.path.join(P, p3d)
        if not os.path.isfile(full):
            log("  WARNING %s: %s not on P: yet - skipped (rerun build_world.py once it exists)" % (src, p3d))
            continue
        o = pl.place(p3d, x, z, yaw, y_offset=yoff, kind="placement:" + src)
        if o is None:
            log("  WARNING %s: %s unreadable - skipped" % (src, p3d))
            continue
        log("  placed %s from %s at (%.1f, %.2f, %.1f) yaw %.0f, centre from %s" % (p3d, src, x, o["origin"][1], z, yaw, o["bc_kind"]))
        ok += 1
    return ok
