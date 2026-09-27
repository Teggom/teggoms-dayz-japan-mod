"""Loot points generated from the model's own walkable floors (WORLD_BUILDINGS.md section 4.2).

Recipe: keep points 0.4 m from walls and obstacles, about one per 4-6 m2, range 0.3-1.2 m, height = 2.5 x range
capped at 2.0 (the vanilla floor-point ratio). Points are written in the CE loot frame:
a model point (mx, my, mz) is stored as (lx, ly, lz) = (mz, my, -mx)  (WORLD_BUILDINGS section 0).
"""
import math

MARGIN = 0.40
AREA_PER_POINT = 5.0    # m2 of room floor per loot point (recipe: one per ~4-6 m2)
MIN_SEP = 1.3           # minimum distance between two points of the same floor
RANGE_MIN, RANGE_MAX = 0.30, 1.20


def _clear(x, z, rect, obstacles):
    x0, x1, z0, z1 = rect
    d = min(x - x0, x1 - x, z - z0, z1 - z)
    for (a0, a1, b0, b1) in obstacles:
        dx = max(a0 - x, 0.0, x - a1)
        dz = max(b0 - z, 0.0, z - b1)
        if dx == 0.0 and dz == 0.0:
            return -1.0
        d = min(d, math.hypot(dx, dz))
    return d


def floor_points(floor):
    x0, x1, z0, z1 = floor["rect"]
    ix0, ix1, iz0, iz1 = x0 + MARGIN, x1 - MARGIN, z0 + MARGIN, z1 - MARGIN
    if ix1 <= ix0 or iz1 <= iz0:
        return []
    # about one point per AREA_PER_POINT m2 of the room, one in the middle of each grid cell
    w, d = x1 - x0, z1 - z0
    n = max(1.0, w * d / AREA_PER_POINT)
    nx = max(1, int(round(math.sqrt(n * w / d))))
    nz = max(1, int(round(n / nx)))
    pts = []
    cw, cd = (ix1 - ix0) / nx, (iz1 - iz0) / nz
    for i in range(nx):
        for j in range(nz):
            # the cell centre, or the most open spot of the cell when an obstacle is in the way
            best = None
            for a in range(7):
                for b in range(7):
                    x = ix0 + (i + 0.5 + (a - 3) / 7.0) * cw
                    z = iz0 + (j + 0.5 + (b - 3) / 7.0) * cd
                    d = _clear(x, z, floor["rect"], floor["obstacles"])
                    score = d - 0.05 * math.hypot(a - 3, b - 3)      # prefer the centre
                    if any(math.hypot(x - q["model"][0], z - q["model"][2]) < MIN_SEP for q in pts):
                        score -= 10.0                                  # keep points apart
                    if best is None or score > best[0]:
                        best = (score, x, z, d)
            score, x, z, d = best
            if d < MARGIN - 1e-6 or score < -5.0:
                continue
            cell = min((ix1 - ix0) / nx, (iz1 - iz0) / nz)
            rng = max(RANGE_MIN, min(RANGE_MAX, d - 0.1, cell / 2 + 0.2))
            pts.append(dict(model=(x, floor["y"], z), range=rng, height=min(2.0, 2.5 * rng), floor=floor["name"]))
    return pts


def model_to_ce(p):
    mx, my, mz = p
    return (mz, my, -mx)


def all_points(model):
    out = []
    for f in model.floors:
        out.extend(floor_points(f))
    return out


def proto_group(model, usages=("Town", "Village")):
    pts = all_points(model)
    lines = ['\t\t<group name="%s">' % model.params["class"]]
    for u in usages:
        lines.append('\t\t\t\t<usage name="%s" />' % u)
    lines.append('\t\t\t\t<container name="lootFloor">')
    for c in ("tools", "containers", "clothes", "food"):
        lines.append('\t\t\t\t\t\t<category name="%s" />' % c)
    lines.append('\t\t\t\t\t\t<tag name="floor" />')
    for p in pts:
        lx, ly, lz = model_to_ce(p["model"])
        lines.append('\t\t\t\t\t\t<point pos="%.6f %.6f %.6f" range="%.6f" height="%.6f" />'
                     % (lx, ly, lz, p["range"], p["height"]))
    lines.append("\t\t\t\t</container>")
    lines.append("\t\t</group>")
    return "\n".join(lines) + "\n", pts


def ce_to_world(l, pos, yaw_deg):
    """WORLD_BUILDINGS section 0, used by verify to cross-check the transform."""
    lx, ly, lz = l
    y = math.radians(yaw_deg)
    return (pos[0] + lx * math.sin(y) - lz * math.cos(y), pos[1] + ly, pos[2] + lx * math.cos(y) + lz * math.sin(y))


def model_to_world(mp, pos, yaw_deg):
    """Model point -> world for a flat placement: world = pos + Ry(yaw) * m, yaw clockwise from north."""
    mx, my, mz = mp
    y = math.radians(yaw_deg)
    # +z (north at yaw 0) turns clockwise towards +x (east)
    return (pos[0] + mx * math.cos(y) + mz * math.sin(y), pos[1] + my, pos[2] - mx * math.sin(y) + mz * math.cos(y))
