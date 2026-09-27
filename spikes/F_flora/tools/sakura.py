r"""sakura.py - procedural Somei-yoshino cherry in full bloom -> MLOD p3d (+ OBJ previews for Blender).

    python spikes/F_flora/tools/sakura.py            (both variants; then build.py binarizes)

Variants:  jp_sakura_01  hero tree, ~8 m tall, ~10 m crown, 4 scaffold limbs
           jp_sakura_02  younger size variant, ~6 m tall, ~7.5 m crown, 3 scaffold limbs

LOD chain mirrors vanilla t_prunusdomestica_2s (the plum, a close relative):
  1, 2, 3   resolution LODs: bark tubes (TreeAdvTrunk) + blossom cards (TreeAdv), thinning out
  4         impostor: 2 crossed vertical billboards + 1 horizontal, texture rendered by render_blender.py
  Geometry  trunk + scaffold frusta, class=treehard etc. (named properties copied from the plum), autocenter=0
  Memory    action, sound_TreeLargeLeavesDomestic
  View / Fire Geometry   trunk + limbs (wood) + crown blobs (foliage penetration material)
The p3d origin is the trunk base on the ground (autocenter=0), so a placement's y_offset is just the sink depth.
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mlod  # noqa: E402
from common import WORK_MESH, P_TREE, src_dir  # noqa: E402
from meshlib import (Mesh, tube, card, convex_frustum, convex_blob, memory_lod, check_winding, basis_from,  # noqa: E402
                     rotate_about, v_add, v_sub, v_mul, v_norm, v_len, v_dot, v_cross, v_lerp)
from sprites import load_atlas  # noqa: E402

D = P_TREE + "\\data\\"
BARK_TEX = D + "jp_sakura_bark_co.paa"
BARK_MAT = D + "jp_sakura_trunk.rvmat"
BLOSSOM_TEX = D + "jp_sakura_blossom_ca.paa"
BLOSSOM_MAT = {1: D + "jp_sakura_blossom.rvmat", 2: D + "jp_sakura_blossom_lod2.rvmat", 3: D + "jp_sakura_blossom_lod3.rvmat"}
WOOD_PEN = "dz\\data\\data\\penetration\\wood.rvmat"
FOLIAGE_PEN = "dz\\data\\data\\penetration\\foliage.rvmat"
BARK_TILE_M = 1.6          # the Poly Haven scan covers 1.6 x 1.6 m

VARIANTS = {
    "jp_sakura_01": dict(seed=21, trunk_h=2.1, trunk_r=0.21, scaffolds=5, scaf_len=(4.2, 5.3), scaf_elev=(32, 48),
                         scaf_r=0.12, leader=3.2, sec_len=(1.4, 2.5), cards=1.0),
    "jp_sakura_02": dict(seed=5, trunk_h=1.6, trunk_r=0.14, scaffolds=4, scaf_len=(3.0, 3.8), scaf_elev=(36, 52),
                         scaf_r=0.085, leader=2.4, sec_len=(1.0, 1.8), cards=0.8),
}

UP = (0.0, 1.0, 0.0)


# ---------------------------------------------------------------------------------------------------------------
# skeleton
# ---------------------------------------------------------------------------------------------------------------
class Branch:
    def __init__(self, path, radii, level):
        self.path, self.radii, self.level = path, radii, level
        self.droop = False

    def length(self):
        return sum(v_len(v_sub(self.path[i + 1], self.path[i])) for i in range(len(self.path) - 1))

    def at(self, t):
        """point, direction, radius at fraction t of the length"""
        segs = [v_len(v_sub(self.path[i + 1], self.path[i])) for i in range(len(self.path) - 1)]
        d = t * sum(segs)
        for i, s in enumerate(segs):
            if d <= s or i == len(segs) - 1:
                f = min(1.0, d / s) if s else 0.0
                p = v_lerp(self.path[i], self.path[i + 1], f)
                r = self.radii[i] + (self.radii[i + 1] - self.radii[i]) * f
                return p, v_norm(v_sub(self.path[i + 1], self.path[i])), r
            d -= s
        return self.path[-1], v_norm(v_sub(self.path[-1], self.path[-2])), self.radii[-1]


def dir_from(az_deg, elev_deg):
    az, el = math.radians(az_deg), math.radians(elev_deg)
    return (math.cos(el) * math.sin(az), math.sin(el), math.cos(el) * math.cos(az))


def grow(start, d0, length, r0, r1, step, rng, bend_to=None, bend=0.0, wobble=0.06, level=0):
    """Polyline from `start` in direction d0; each step the direction drifts towards `bend_to` by `bend`
    (radians over the whole length) plus a little random wobble."""
    n = max(2, int(round(length / step)))
    pts, d = [start], v_norm(d0)
    for i in range(n):
        if bend_to is not None and bend:
            axis = v_cross(d, bend_to)
            if v_len(axis) > 1e-6:
                d = v_norm(rotate_about(d, axis, bend / n))
        a, b = basis_from(d)
        d = v_norm(v_add(d, v_add(v_mul(a, rng.uniform(-wobble, wobble)), v_mul(b, rng.uniform(-wobble, wobble)))))
        pts.append(v_add(pts[-1], v_mul(d, length / n)))
    radii = [r0 + (r1 - r0) * (i / n) ** 0.85 for i in range(n + 1)]
    return Branch(pts, radii, level)


def skeleton(cfg):
    rng = random.Random(cfg["seed"])
    branches = []
    # trunk: short, slight lean, buried 15 cm, root flare in the radius profile
    lean_az = rng.uniform(0, 360)
    trunk = grow((0.0, -0.15, 0.0), dir_from(lean_az, 86), cfg["trunk_h"] + 0.15, cfg["trunk_r"], cfg["trunk_r"] * 0.78,
                 0.3, rng, wobble=0.03)
    trunk.radii = [r * (1.0 + 0.45 * math.exp(-max(0.0, p[1] + 0.15) / 0.25)) for p, r in zip(trunk.path, trunk.radii)]
    branches.append(trunk)
    top = trunk.path[-1]
    top_r = trunk.radii[-1]
    # scaffold limbs: broad spreading vase, arching towards horizontal at the tips; they leave the trunk
    # over its top half-metre, not all from one point
    n = cfg["scaffolds"]
    az0 = rng.uniform(0, 360)
    scaffolds = []
    for i in range(n):
        az = az0 + i * 360.0 / n + rng.uniform(-14, 14)
        el = rng.uniform(*cfg["scaf_elev"])
        ln = rng.uniform(*cfg["scaf_len"])
        d = dir_from(az, el)
        out = v_norm((d[0], 0.0, d[2]))
        p0, _, _ = trunk.at(rng.uniform(0.8, 0.97))
        b = grow(p0, d, ln, cfg["scaf_r"], 0.03, 0.35, rng, bend_to=out,
                 bend=math.radians(rng.uniform(22, 38)), wobble=0.08, level=1)
        scaffolds.append(b)
    # a central leader, shorter and more upright
    leader = grow(v_sub(top, (0, 0.1, 0)), dir_from(az0 + 180.0 / n, 74), cfg["leader"], cfg["scaf_r"] * 0.75, 0.025,
                  0.35, rng, wobble=0.1, level=1)
    scaffolds.append(leader)
    branches += scaffolds
    # secondaries along each scaffold: lateral ones fill the gaps between scaffolds, "droopers" on the outer
    # half hang out and down and bring the blossom down to head height at the rim of the crown
    down = (0.0, -1.0, 0.0)
    for sc in scaffolds:
        L = sc.length()
        t = 0.1
        side = 1
        while t < 0.97:
            p, d, r = sc.at(t)
            a, b = basis_from(d, UP)            # a: horizontal-ish sideways, b: "up" side of the limb
            if t > 0.45 and rng.random() < 0.38:
                hor = v_norm(v_add(v_mul(v_norm((d[0], 0.0, d[2])), 0.8), v_mul(a, side * 0.6)))
                sd = v_norm(v_add(hor, (0, -math.tan(math.radians(rng.uniform(10, 30))), 0)))
                ln = rng.uniform(1.2, 2.2) * cfg["sec_len"][1] / 2.5
                sec = grow(p, sd, ln, max(0.014, r * 0.55), 0.007, 0.26, rng, bend_to=down,
                           bend=math.radians(rng.uniform(15, 35)), wobble=0.12, level=2)
                sec.droop = True
            else:
                roll = side * math.radians(rng.uniform(30, 120))
                sd = v_norm(v_add(v_mul(d, 0.45), v_add(v_mul(a, math.sin(abs(roll)) * side), v_mul(b, math.cos(roll) * 0.8))))
                sd = v_norm(v_add(sd, (0, 0.15, 0)))
                ln = rng.uniform(*cfg["sec_len"]) * (1.2 - 0.5 * t)
                hor = v_norm((sd[0], 0.0, sd[2]))
                sec = grow(p, sd, ln, max(0.014, r * 0.62), 0.008, 0.28, rng, bend_to=hor,
                           bend=math.radians(rng.uniform(5, 25)), wobble=0.12, level=2)
                sec.droop = False
            branches.append(sec)
            side = -side
            t += rng.uniform(0.35, 0.55) / L
    # tertiaries: short twigs off the secondaries (bark tubes only in LOD1, but they carry cards in every LOD)
    for sec in [b for b in branches if b.level == 2]:
        L = sec.length()
        t = 0.3
        side = 1
        while t < 0.9:
            p, d, r = sec.at(t)
            a, b = basis_from(d, UP)
            roll = side * math.radians(rng.uniform(40, 100))
            td = v_norm(v_add(v_mul(d, 0.7), v_add(v_mul(a, math.cos(roll)), v_mul(b, math.sin(abs(roll))))))
            if sec.droop:
                td = v_norm(v_add(td, (0, -0.3, 0)))
            ln = rng.uniform(0.35, 0.75)
            tw = grow(p, td, ln, max(0.007, r * 0.7), 0.004, 0.2, rng, wobble=0.15, level=3)
            tw.droop = sec.droop
            branches.append(tw)
            side = -side
            t += rng.uniform(0.3, 0.45) / L
    return branches


# ---------------------------------------------------------------------------------------------------------------
# cards
# ---------------------------------------------------------------------------------------------------------------
def crown_frame(branches):
    pts = [p for b in branches if b.level >= 1 for p in b.path]
    xs, ys, zs = zip(*pts)
    c = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2 - 0.3, (min(zs) + max(zs)) / 2)
    r = ((max(xs) - min(xs)) / 2 + 0.6, (max(ys) - min(ys)) / 2 + 0.6, (max(zs) - min(zs)) / 2 + 0.6)
    return c, r


def plan_cards(branches, cfg, seed):
    """Every card the tree could carry: (kind, anchor, dir_up, dir_side, scale, priority). Lower LODs keep the
    high-priority subset and scale those cards up."""
    rng = random.Random(seed + 1000)
    cards = []
    for b in branches:
        if b.level < 2 and not (b.level == 1):
            continue
        L = b.length()
        if b.level == 1:
            ts = [0.45, 0.6, 0.75, 0.9, 1.0]
        elif b.level == 2:
            ts = [0.2 + i * 0.28 / max(0.28, L) for i in range(int(L / 0.28) + 1)]
            ts = [t for t in ts if t < 1.0] + [1.0]
        else:
            ts = [0.5, 1.0]
        for t in ts:
            p, d, r = b.at(min(1.0, t))
            # tilt the spray off the branch axis, a bit towards the sky
            a, bb = basis_from(d, UP)
            tilt = math.radians(rng.uniform(-45, 45))
            lift = rng.uniform(-0.45, 0.05) if b.droop else rng.uniform(-0.15, 0.45)
            up = v_norm(v_add(v_add(v_mul(d, math.cos(tilt)), v_mul(a, math.sin(tilt))), (0, lift, 0)))
            roll = rng.uniform(0, math.pi)
            sa, sb = basis_from(up, UP)
            side = v_norm(v_add(v_mul(sa, math.cos(roll)), v_mul(sb, math.sin(roll))))
            kind = rng.choice((0, 1))
            pri = rng.random() + (0.5 if t >= 0.99 else 0.0) + (0.3 if b.level == 2 else 0.0)
            cards.append((kind, p, up, side, rng.uniform(0.9, 1.2), pri))
            # radial spray (seen from above) near the tips of the outer twigs, facing out of the crown
            if b.level >= 2 and t >= 0.99 and rng.random() < 0.5:
                cards.append(("radial", p, None, None, rng.uniform(0.9, 1.25), rng.random() + 0.4))
    return cards


def build_cards(mesh, cards, sprites, crown, lod, cfg, rng):
    c, rad = crown
    keep = {1: 1.0, 2: 0.5, 3: 0.18}[lod] * cfg["cards"]
    grow_k = {1: 1.0, 2: 1.35, 3: 2.0}[lod]
    ordered = sorted(cards, key=lambda x: -x[5])
    n = int(len(ordered) * min(1.0, keep))
    mat = BLOSSOM_MAT[lod]

    def shade_n(p):
        # ellipsoidal crown normal: soft, volumetric lighting on the cards
        g = ((p[0] - c[0]) / rad[0] ** 2, (p[1] - c[1]) / rad[1] ** 2, (p[2] - c[2]) / rad[2] ** 2)
        return v_norm(g)

    count = 0
    for kind, p, up, side, sc, pri in ordered[:n]:
        if kind == "radial":
            sp = sprites[3]
            out = shade_n(p)
            up_axis = v_norm(v_add(out, (0, 0.8, 0)))            # mostly facing the sky, leaning out
            s1, s2 = basis_from(up_axis, (1.0, 0.0, 0.0))
            rot = rng.uniform(0, 2 * math.pi)
            side = v_norm(v_add(v_mul(s1, math.cos(rot)), v_mul(s2, math.sin(rot))))
            up = v_norm(v_cross(up_axis, side))
        else:
            sp = sprites[kind]
        corners = []
        uvs = []
        for x, y, u, v in sp.corners_local(sc * grow_k):
            corners.append(v_add(p, v_add(v_mul(side, x), v_mul(up, y))))
            uvs.append((u, v))
        card(mesh, corners, uvs, shade_n, BLOSSOM_TEX, mat)
        count += 1
    # volume filler: dense clump cards inside the crown shell (more of them in the lower LODs)
    n_fill = {1: 40, 2: 70, 3: 90}[lod] * cfg["cards"]
    sp = sprites[2]
    tips = [x[1] for x in cards]
    for i in range(int(n_fill)):
        p = rng.choice(tips)
        p = v_lerp(p, c, rng.uniform(0.1, 0.35))
        up = v_norm((rng.uniform(-1, 1), rng.uniform(-0.3, 1), rng.uniform(-1, 1)))
        side, _ = basis_from(up, UP)
        sc = rng.uniform(1.1, 1.5) * (1.0 if lod == 1 else 1.3 if lod == 2 else 1.65)
        corners, uvs = [], []
        for x, y, u, v in sp.corners_local(sc):
            corners.append(v_add(p, v_add(v_mul(side, x), v_mul(up, y))))
            uvs.append((u, v))
        card(mesh, corners, uvs, shade_n, BLOSSOM_TEX, mat)
        count += 1
    return count


# ---------------------------------------------------------------------------------------------------------------
# LODs
# ---------------------------------------------------------------------------------------------------------------
def bark_uv(radius_at):
    def fn(ring, f, dist):
        circ = 2 * math.pi * radius_at(ring)
        reps = circ / BARK_TILE_M
        reps = max(1.0, round(reps)) if reps >= 0.75 else reps
        return (f * reps, dist / BARK_TILE_M)
    return fn


def build_resolution(branches, cards, sprites, crown, lod, cfg):
    rng = random.Random(cfg["seed"] * 7 + lod)
    mesh = Mesh()
    sides = {1: {0: 12, 1: 8, 2: 5, 3: 3}, 2: {0: 8, 1: 6, 2: 4, 3: 0}, 3: {0: 6, 1: 4, 2: 3, 3: 0}}[lod]
    step = {1: {0: 1, 1: 1, 2: 2, 3: 3}, 2: {0: 1, 1: 2, 2: 3, 3: 1}, 3: {0: 2, 1: 3, 2: 4, 3: 1}}[lod]
    for b in branches:
        n = sides[b.level]
        if n == 0:
            continue
        if lod == 3 and b.level == 2 and b.length() < 1.2:
            continue
        path, radii = b.path, b.radii
        k = step[b.level]
        if k > 1 and len(path) > 2:               # decimate the polyline
            keep = list(range(0, len(path), k))
            if keep[-1] != len(path) - 1:
                keep.append(len(path) - 1)
            path = [path[i] for i in keep]
            radii = [radii[i] for i in keep]
        tube(mesh, path, radii, n, BARK_TEX, BARK_MAT, bark_uv(lambda i, rr=radii: rr[i]), cap_top=(b.level <= 1))
    n_cards = build_cards(mesh, cards, sprites, crown, lod, cfg, rng)
    return mesh, n_cards


def build_impostor(bounds, lod4_tex, lod4_mat):
    """LOD4: vertical billboards in the XY and ZY planes + one horizontal at crown height.
    Atlas layout (render_blender.py renders it): TL = top view, BL = view along +Z, BR = view along -X."""
    (x0, y0, z0), (x1, y1, z1) = bounds
    S = max(2 * max(abs(x0), abs(x1), abs(z0), abs(z1)), y1) * 1.03    # frame centred on the trunk axis
    h = S
    mesh = Mesh()
    n_up = (0.0, 1.0, 0.0)
    # XY plane (seen along Z): u 0..0.5, v 0.5..1
    c = [(-S / 2, h, 0.0), (S / 2, h, 0.0), (S / 2, 0.0, 0.0), (-S / 2, 0.0, 0.0)]
    card(mesh, c, [(0.0, 0.5), (0.5, 0.5), (0.5, 1.0), (0.0, 1.0)], lambda p: n_up, lod4_tex, lod4_mat, (0.0, 0.0, -1.0))
    # ZY plane (seen along X): u 0.5..1, v 0.5..1
    c = [(0.0, h, S / 2), (0.0, h, -S / 2), (0.0, 0.0, -S / 2), (0.0, 0.0, S / 2)]
    card(mesh, c, [(0.5, 0.5), (1.0, 0.5), (1.0, 1.0), (0.5, 1.0)], lambda p: n_up, lod4_tex, lod4_mat, (1.0, 0.0, 0.0))
    # horizontal: top view at the crown's lower-middle height
    yh = y0 + (y1 - y0) * 0.62
    c = [(-S / 2, yh, S / 2), (S / 2, yh, S / 2), (S / 2, yh, -S / 2), (-S / 2, yh, -S / 2)]
    card(mesh, c, [(0.0, 0.0), (0.5, 0.0), (0.5, 0.5), (0.0, 0.5)], lambda p: n_up, lod4_tex, lod4_mat, (0.0, 1.0, 0.0))
    return mesh, dict(S=S, yh=yh)


def frusta_for(branches, levels, max_len_per_branch, pieces):
    """Straight convex pieces approximating the thick parts of the branch set."""
    segs = []
    for b in branches:
        if b.level not in levels:
            continue
        L = min(b.length(), max_len_per_branch[b.level])
        k = pieces[b.level]
        for i in range(k):
            ta, tb = (L * i / k) / b.length(), (L * (i + 1) / k) / b.length()
            pa, _, ra = b.at(ta)
            pb, _, rb = b.at(tb)
            segs.append((pa, pb, ra, rb))
    return segs


def build_geometry(branches, mass):
    mesh = Mesh()
    segs = frusta_for(branches, (0, 1), {0: 99, 1: 2.4}, {0: 2, 1: 2})
    for i, (pa, pb, ra, rb) in enumerate(segs):
        convex_frustum(mesh, pa, pb, ra * 0.95, rb * 0.95, 8, sel="Component%02d" % (i + 1))
    return mesh


def build_view_fire(branches, crown, fire):
    mesh = Mesh()
    segs = frusta_for(branches, (0, 1), {0: 99, 1: 4.5}, {0: 2, 1: 3})
    k = 0
    for pa, pb, ra, rb in segs:
        k += 1
        convex_frustum(mesh, pa, pb, ra, rb, 6, mat=WOOD_PEN if fire else "", sel="Component%02d" % k)
    # crown: a central blob plus one over each scaffold's outer half
    c, r = crown
    k += 1
    convex_blob(mesh, (c[0], c[1] + r[1] * 0.1, c[2]), (r[0] * 0.55, r[1] * 0.55, r[2] * 0.55), mat=FOLIAGE_PEN if fire else "",
                sel="Component%02d" % k)
    for b in branches:
        if b.level != 1:
            continue
        p, _, _ = b.at(0.8)
        k += 1
        convex_blob(mesh, p, (1.5, 1.2, 1.5), mat=FOLIAGE_PEN if fire else "", sel="Component%02d" % k)
    return mesh


GEO_PROPS = {  # vanilla t_prunusdomestica_2s Geometry LOD, plus autocenter=0 (origin = trunk base)
    "autocenter": "0", "canocclude": "0", "dammage": "tree", "map": "tree", "class": "treehard", "style": "plant",
    "frequent": "1", "drawimportance": "0.3", "canclimb": "0",
}


def build(name, cfg, out_dir):
    branches = skeleton(cfg)
    crown = crown_frame(branches)
    sprites = load_atlas("jp_sakura_blossom_ca", [(0.25, 0.4925), (0.75, 0.4925), (0.25, 0.75), (0.75, 0.75)], 0.9)
    cards = plan_cards(branches, cfg, cfg["seed"])
    lods, stats = [], {}
    meshes = {}
    for lod in (1, 2, 3):
        m, nc = build_resolution(branches, cards, sprites, crown, lod, cfg)
        meshes[lod] = m
        bad = check_winding(m)
        stats["lod%d" % lod] = dict(tris=m.tri_count(), cards=nc, points=len(m.points), bad_winding=bad)
        lods.append(m.to_lod(float(lod), props={"lodnoshadow": "1"}))
    bounds = meshes[1].bbox()
    lod4_tex = D + name + "_lod4_ca.paa"
    lod4_mat = D + "jp_sakura_lod4.rvmat"
    imp, imp_info = build_impostor(bounds, lod4_tex, lod4_mat)
    meshes[4] = imp
    lods.append(imp.to_lod(4.0, props={"lodnoshadow": "1"}))
    stats["lod4"] = dict(tris=imp.tri_count())
    geo = build_geometry(branches, 6000.0)
    lods.append(geo.to_lod(mlod.LOD_GEOMETRY, props=GEO_PROPS, mass=6000.0))
    c, r = crown
    lods.append(memory_lod({"action": (0.0, 1.0, 0.0), "sound_TreeLargeLeavesDomestic": (c[0], c[1], c[2])},
                           props={"lodnoshadow": "1"}))
    view = build_view_fire(branches, crown, fire=False)
    lods.append(view.to_lod(mlod.LOD_VIEW_GEOMETRY))
    fire = build_view_fire(branches, crown, fire=True)
    lods.append(fire.to_lod(mlod.LOD_FIRE_GEOMETRY))
    stats["geometry_components"] = len([k for k in geo.selections])
    stats["view_components"] = len(view.selections)
    stats["bounds"] = bounds
    p3d = os.path.join(out_dir, name + ".p3d")
    mlod.write_mlod(p3d, lods)
    # previews for Blender (visual LODs + the collision shapes)
    for lod, m in meshes.items():
        m.write_obj(os.path.join(WORK_MESH, "%s_lod%d.obj" % (name, lod)), {BARK_TEX: "bark", BLOSSOM_TEX: "blossom", lod4_tex: "impostor"})
    geo.write_obj(os.path.join(WORK_MESH, "%s_geo.obj" % name), {})
    info = dict(name=name, impostor=imp_info, bounds=bounds, crown=crown, stats=stats,
                textures={"bark": "jp_sakura_bark_co.png", "blossom": "jp_sakura_blossom_ca.png",
                          "impostor": name + "_lod4_ca.png"})
    with open(os.path.join(WORK_MESH, name + ".json"), "wb") as f:
        f.write(json.dumps(info, indent=1).encode())
    return p3d, stats


def main(argv):
    names = [a for a in argv if a in VARIANTS] or list(VARIANTS)
    out = src_dir(P_TREE)
    for n in names:
        p3d, st = build(n, VARIANTS[n], out)
        print(n, "->", p3d)
        for k, v in st.items():
            print("   ", k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
