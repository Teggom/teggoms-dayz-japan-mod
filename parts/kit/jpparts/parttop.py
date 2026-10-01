"""parttop.py - interior partitions end at a beam or a ceiling, and their ends meet something (FB2, 2026-10-01).

Stephen's re-check: "the interior walls rise to ~3 m and just end below the open roof structure" (Kinai farmhouse),
and upstairs in the grand inn "the divider wall doesn't reach the sloping ceiling". Period partitions end at a
horizontal member carried on posts (a head beam / sashigamoi / tie beam) or rise to a ceiling, floor or roof.

top_ends(M): for every interior wall panel (Resolution 1, interior solids whose footprint is a thin slab: tags in
WALL_TAGS), sample its top edge every 0.25 m; from each sample climb through the solids stacked directly on it (gap
<= 2 cm: rails, kokabe, beams). The stack is CLOSED when it ends against something within 2 cm above (a ceiling,
floor, roof underside, beam) or when its top member is a beam (tag in BEAM_TAGS) running at least 0.6 m along the
wall. Otherwise the wall stops in the open: returns [(tag, src, (x, y, z), open_gap_m)] for those samples.
"""
import math

WALL_TAGS = ("infill", "kokabe", "panel", "board", "wall", "okabe", "infill_base", "board_base", "fusuma_panel")
BEAM_TAGS = ("part_head", "ushibari", "tie_beam", "keta", "floor_beam", "beam", "sashigamoi", "nageshi", "head_beam",
             "loft_beam", "joya_plate", "geya_bari", "wall_plate", "well_rim", "rim", "upper_beam", "pent_plate",
             "open_front_beam", "nuki", "kamoi_beam", "ceiling", "tenjo", "loft_boards", "loft_lod", "floor_board",
             "sao_joist", "ceiling_board", "upper_floor", "noki_keta", "dobari", "sashigamoi_beam")
ROOF_TAGS = ("sasu", "sumi_sasu", "tsuma_sasu", "rafter", "sheathing", "tile_bed", "thatch_body", "moya", "munagi",
             "roof", "kawara_field", "leanto", "verge", "board_roof", "lath", "taruki", "soffit", "eave")
GAP = 0.025


def _planes(s):
    return [(s.fn[fi], s.fn[fi][0] * s.verts[f[0]][0] + s.fn[fi][1] * s.verts[f[0]][1] + s.fn[fi][2] * s.verts[f[0]][2])
            for fi, f in enumerate(s.faces)]


def _ray_up(sol, p):
    """First entry height of a vertical ray from p upward into the convex solid (None if missed)."""
    s, bb, pl = sol
    if not (bb[0] - 1e-6 <= p[0] <= bb[1] + 1e-6 and bb[4] - 1e-6 <= p[2] <= bb[5] + 1e-6) or bb[3] < p[1]:
        return None
    t0, t1 = -1e9, 1e9
    for n, d in pl:
        a = n[0] * p[0] + n[1] * p[1] + n[2] * p[2] - d
        if abs(n[1]) < 1e-9:
            if a > 1e-6:
                return None
            continue
        t = -a / n[1]
        if n[1] < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 <= t1 + 1e-6 and t1 > 1e-4:
        return max(t0, 0.0)
    return None


def top_ends(M, lod=1, wall_tags=WALL_TAGS):
    sols = []
    for s in M.solids:
        if lod not in s.vis or not s.closed or len(s.faces) < 4:
            continue
        sols.append((s, s.bbox(), _planes(s)))
    cell = {}
    for i, (s, bb, _) in enumerate(sols):
        for cx in range(int(math.floor(bb[0] / 2)), int(math.floor(bb[1] / 2)) + 1):
            for cz in range(int(math.floor(bb[4] / 2)), int(math.floor(bb[5] / 2)) + 1):
                cell.setdefault((cx, cz), []).append(i)
    bad = []
    for s, bb, _ in sols:
        if not getattr(s, "interior", False) or s.tag not in wall_tags:
            continue
        dx, dz, dy = bb[1] - bb[0], bb[5] - bb[4], bb[3] - bb[2]
        if dy < 0.4 or min(dx, dz) > 0.25 or max(dx, dz) < 0.3:
            continue
        along_x = dx >= dz
        L = dx if along_x else dz
        n = max(1, int(L / 0.25))
        for k in range(n):
            u = (k + 0.5) / n
            x = bb[0] + dx * u if along_x else (bb[0] + bb[1]) / 2
            z = (bb[4] + bb[5]) / 2 if along_x else bb[4] + dz * u
            y = bb[3]
            top, path = s, [s.tag]
            for _ in range(12):
                p = (x, y - 0.01, z)
                best = None
                for i in cell.get((int(math.floor(x / 2)), int(math.floor(z / 2))), ()):
                    o = sols[i]
                    if o[0] is top:
                        continue
                    h = _ray_up(o, p)
                    if h is not None and (best is None or h < best[0]):
                        best = (h, o)
                if best is None:
                    gap = 99.0
                    break
                gap = best[0] - 0.01
                if gap > GAP:
                    break
                top = best[1][0]
                path.append(top.tag)
                y = best[1][1][3]
            else:
                gap = 0.0
            if gap <= GAP or any(t.startswith(ROOF_TAGS) for t in path[1:]):
                continue
            tb = top.bbox()
            run = (tb[1] - tb[0]) if along_x else (tb[5] - tb[4])
            if top is not s and top.tag in BEAM_TAGS and run >= 0.6:
                continue
            bad.append((s.tag, getattr(s, "src", ""), (round(x, 2), round(y, 2), round(z, 2)), round(min(gap, 9.9), 2),
                        "/".join(path[-3:])))
    return bad


def summary(bad, top=8):
    g = {}
    for t, src, p, gap, path in bad:
        k = (src, path)
        n, ex = g.get(k, (0, (p, gap)))
        g[k] = (n + 1, ex)
    return ["%s [%s]: %d samples (e.g. %s, open %.2f m above)" % (k[0], k[1], n, ex[0], ex[1])
            for k, (n, ex) in sorted(g.items(), key=lambda kv: -kv[1][0])[:top]]


END_TAGS = ("infill", "kokabe", "panel", "infill_base", "board", "okabe")


def free_ends(M, lod=1):
    """FB2: interior wall panels whose vertical END is free (a point 1.5 cm past the end, at 3+ of 5 heights, inside no
    other solid): a see-through slot at a wall end or a missing post (the grand inn's "vertical gaps").
    Returns [(src, tag, (x, y, z))]."""
    from . import zfight as Z
    occ = Z._Occ(M, lod)
    idx = {id(s): i for i, s in enumerate(M.solids)}
    out = []
    for s in M.solids:
        if lod not in s.vis or s.tag not in END_TAGS or not getattr(s, "interior", False) or not s.closed:
            continue
        bb = s.bbox()
        dx, dz, dy = bb[1] - bb[0], bb[5] - bb[4], bb[3] - bb[2]
        if dy < 0.3 or min(dx, dz) > 0.2 or max(dx, dz) < 0.2:
            continue
        ax = 0 if dx >= dz else 2
        c = ((bb[0] + bb[1]) / 2, (bb[2] + bb[3]) / 2, (bb[4] + bb[5]) / 2)
        for end, sg in ((bb[1] if ax == 0 else bb[5], 1), (bb[0] if ax == 0 else bb[4], -1)):
            free = 0
            for k in range(5):
                p = [c[0], bb[2] + dy * (k + 0.5) / 5, c[2]]
                p[ax] = end + sg * 0.015
                if not occ.inside(tuple(p), (idx[id(s)],)):
                    free += 1
            if free >= 3:
                q = [c[0], c[1], c[2]]
                q[ax] = end
                out.append((getattr(s, "src", ""), s.tag, tuple(round(v, 2) for v in q)))
    return out
