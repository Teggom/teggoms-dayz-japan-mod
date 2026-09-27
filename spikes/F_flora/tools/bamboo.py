r"""bamboo.py - procedural bamboo clump (terrain object, cuttable as BushHard) and the JP_BambooPole item.

    python spikes/F_flora/tools/bamboo.py          (both; then build.py binarizes)

jp_bamboo_clump_01.p3d  ~20 culms 4.5-10 m in a 0.75 m radius clump, leaning out and nodding at the tips,
                        leafy from half height up. LODs 1-3 (culm tubes on TreeAdvTrunk so they sway, leaf
                        cards on TreeAdv), LOD4 impostor, Geometry (one convex frustum per culm, 0-2.6 m,
                        class=bushhard), Memory (action, sound_TreeMediumLeaves), View/Fire Geometry.
jp_bamboo_pole.p3d      2.5 m green-to-yellow pole with node ridges and cut ends. Frame copied from vanilla
                        LongWoodenStick (Wooden_stick_blunt.p3d): long axis +Y, grip at the origin with the
                        butt end below it, autocenter=0, so the inherited in-hands IK holds it the same way.
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mlod  # noqa: E402
from common import WORK_MESH, P_BAMBOO, P_ITEMS, src_dir  # noqa: E402
from meshlib import (Mesh, tube, card, convex_frustum, convex_blob, memory_lod, check_winding, basis_from,  # noqa: E402
                     rotate_about, v_add, v_sub, v_mul, v_norm, v_len, v_dot, v_cross, v_lerp)
from sprites import load_atlas  # noqa: E402
from sakura import grow, dir_from, build_impostor, UP  # noqa: E402
from textures import POLE_LEN, POLE_NODES  # noqa: E402

D = P_BAMBOO + "\\data\\"
CULM_TEX = D + "jp_bamboo_culm_co.paa"
CULM_MAT = D + "jp_bamboo_culm.rvmat"
LEAF_TEX = D + "jp_bamboo_leaves_ca.paa"
LEAF_MAT = {1: D + "jp_bamboo_leaves.rvmat", 2: D + "jp_bamboo_leaves_lod2.rvmat", 3: D + "jp_bamboo_leaves_lod3.rvmat"}
WOOD_PEN = "dz\\data\\data\\penetration\\wood.rvmat"
FOLIAGE_PEN = "dz\\data\\data\\penetration\\foliage.rvmat"

CLUMP = dict(seed=3, culms=21, radius=0.75, h=(6.5, 10.0), young=0.2)

GEO_PROPS = {  # vanilla plum set, with class=bushhard (hazel b_corylusavellana_2s uses the same class)
    "autocenter": "0", "canocclude": "0", "dammage": "tree", "map": "tree", "class": "bushhard", "style": "plant",
    "frequent": "1", "drawimportance": "0.5",
}


class Culm:
    pass


def make_culms(cfg):
    rng = random.Random(cfg["seed"])
    culms = []
    spots = []
    tries = 0
    while len(spots) < cfg["culms"] and tries < 5000:
        tries += 1
        a = rng.uniform(0, 2 * math.pi)
        r = cfg["radius"] * math.sqrt(rng.random())
        p = (r * math.cos(a), r * math.sin(a))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.13 ** 2 for q in spots):
            spots.append(p)
    for i, (x, z) in enumerate(spots):
        c = Culm()
        dist = math.hypot(x, z) / cfg["radius"]
        c.young = rng.random() < cfg["young"]
        h0, h1 = cfg["h"]
        c.H = (h0 + (h1 - h0) * (1 - 0.6 * dist) * rng.uniform(0.75, 1.0)) if not c.young else rng.uniform(4.5, 6.0)
        c.r0 = rng.uniform(0.024, 0.03) if c.young else rng.uniform(0.034, 0.05)
        az = math.degrees(math.atan2(x, z)) + rng.uniform(-25, 25)
        lean = rng.uniform(1.5, 4.0) + 7.0 * dist
        d = dir_from(az, 90 - lean)
        out = v_norm((d[0], 0.0, d[2]))
        b = grow((x, -0.1, z), d, c.H + 0.1, c.r0, 0.011, 0.6, rng, bend_to=out, bend=math.radians(rng.uniform(6, 16)),
                 wobble=0.012)
        c.path, c.radii = b.path, b.radii
        c.branch = b
        c.col = 0 if c.young else rng.choice((1, 1, 1, 2, 3, 3))
        c.internode = rng.uniform(0.3, 0.4)
        culms.append(c)
    return culms


def canopy_frame(culms):
    pts = [p for c in culms for p in c.path if p[1] > 0.45 * c.H]
    xs, ys, zs = zip(*pts)
    cen = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2 + 0.3, (min(zs) + max(zs)) / 2)
    rad = ((max(xs) - min(xs)) / 2 + 0.8, (max(ys) - min(ys)) / 2 + 0.8, (max(zs) - min(zs)) / 2 + 0.8)
    return cen, rad


def plan_leaf_cards(culms, cfg):
    rng = random.Random(cfg["seed"] + 500)
    cards = []
    for c in culms:
        L = c.branch.length()
        s = 0.47 * c.H + rng.uniform(0, 0.4)
        while s < L - 0.25:
            if rng.random() < 0.62:
                p, d, r = c.branch.at(s / L)
                cx, cz = p[0], p[2]
                # sprays leave the culm outward from the clump centre (with plenty of spread), drooping a little
                base_az = math.atan2(cx, cz) if math.hypot(cx, cz) > 0.05 else rng.uniform(0, 2 * math.pi)
                az = base_az + rng.uniform(-1.6, 1.6)
                side = v_norm((math.sin(az), -rng.uniform(0.0, 0.25), math.cos(az)))
                up = v_norm(v_sub(UP, v_mul(side, v_dot(UP, side))))
                roll = math.radians(rng.uniform(-40, 40))
                up = rotate_about(up, side, roll)
                kind = rng.choice((0, 1))
                frac = s / L
                pri = rng.random() + 0.6 * frac
                cards.append((kind, p, up, side, rng.uniform(1.15, 1.6) * (0.85 if c.young else 1.0), pri))
            s += c.internode * rng.uniform(0.9, 1.4)
        # crown tuft: two crossed upright fans at the tip
        p, d, r = c.branch.at(1.0)
        a0 = rng.uniform(0, math.pi)
        for k in range(2):
            az = a0 + k * math.pi / 2
            side = v_norm(v_cross(d, (math.sin(az), 0.0, math.cos(az))))
            cards.append((3, v_sub(p, v_mul(d, 0.2)), d, side, rng.uniform(0.75, 1.0), 1.5 + rng.random()))
    return cards


def culm_uv(c, sides_frac_scale=0.25):
    def fn(ring, f, dist):
        return (c.col * 0.25 + f * 0.25 * 0.999, -dist / c.internode)
    return fn


def build_resolution(culms, cards, sprites, canopy, lod, cfg):
    rng = random.Random(cfg["seed"] * 11 + lod)
    mesh = Mesh()
    sides = {1: 7, 2: 5, 3: 3}[lod]
    step = {1: 1, 2: 2, 3: 3}[lod]
    for c in culms:
        path, radii = c.path, c.radii
        if step > 1:
            keep = list(range(0, len(path), step))
            if keep[-1] != len(path) - 1:
                keep.append(len(path) - 1)
            path, radii = [path[i] for i in keep], [radii[i] for i in keep]
        tube(mesh, path, radii, sides, CULM_TEX, CULM_MAT, culm_uv(c), cap_top=False)
    cen, rad = canopy

    def shade_n(p):
        g = ((p[0] - cen[0]) / rad[0] ** 2, (p[1] - cen[1]) / rad[1] ** 2, (p[2] - cen[2]) / rad[2] ** 2)
        return v_norm(g)

    keep = {1: 1.0, 2: 0.55, 3: 0.24}[lod]
    grow_k = {1: 1.0, 2: 1.3, 3: 1.85}[lod]
    ordered = sorted(cards, key=lambda x: -x[5])
    n = int(len(ordered) * keep)
    count = 0
    for kind, p, up, side, sc, pri in ordered[:n]:
        sp = sprites[kind]
        corners, uvs = [], []
        for x, y, u, v in sp.corners_local(sc * (grow_k if kind != 3 else min(grow_k, 1.4))):
            corners.append(v_add(p, v_add(v_mul(side, x), v_mul(up, y))))
            uvs.append((u, v))
        card(mesh, corners, uvs, shade_n, LEAF_TEX, LEAF_MAT[lod])
        count += 1
    # volume filler: dense tufts in the upper canopy
    n_fill = {1: 16, 2: 26, 3: 34}[lod]
    tips = [x[1] for x in cards if x[0] != 3]
    sp = sprites[2]
    for i in range(n_fill):
        p = v_lerp(rng.choice(tips), cen, rng.uniform(0.05, 0.3))
        up = v_norm((rng.uniform(-0.6, 0.6), 1.0, rng.uniform(-0.6, 0.6)))
        side, _ = basis_from(up, (1.0, 0.0, 0.0))
        rot = rng.uniform(0, 2 * math.pi)
        side = rotate_about(side, up, rot)
        s = rng.uniform(1.2, 1.6) * {1: 1.0, 2: 1.3, 3: 1.7}[lod]
        corners, uvs = [], []
        for x, y, u, v in sp.corners_local(s):
            corners.append(v_add(p, v_add(v_mul(side, x), v_mul(up, y))))
            uvs.append((u, v))
        card(mesh, corners, uvs, shade_n, LEAF_TEX, LEAF_MAT[lod])
        count += 1
    return mesh, count


def build_clump(name="jp_bamboo_clump_01", cfg=CLUMP):
    culms = make_culms(cfg)
    canopy = canopy_frame(culms)
    sprites = load_atlas("jp_bamboo_leaves_ca", [(0.015, 0.15), (0.515, 0.15), (0.25, 0.725), (0.75, 0.95)], 1.2)
    cards = plan_leaf_cards(culms, cfg)
    lods, meshes, stats = [], {}, {}
    for lod in (1, 2, 3):
        m, nc = build_resolution(culms, cards, sprites, canopy, lod, cfg)
        meshes[lod] = m
        stats["lod%d" % lod] = dict(tris=m.tri_count(), cards=nc, points=len(m.points), bad_winding=check_winding(m))
        lods.append(m.to_lod(float(lod), props={"lodnoshadow": "1"}))
    bounds = meshes[1].bbox()
    lod4_tex = D + name + "_lod4_ca.paa"
    imp, imp_info = build_impostor(bounds, lod4_tex, D + "jp_bamboo_lod4.rvmat")
    meshes[4] = imp
    lods.append(imp.to_lod(4.0, props={"lodnoshadow": "1"}))
    # geometry: one convex frustum per culm over its lowest 2.6 m (thin culms still block a walker)
    geo = Mesh()
    for i, c in enumerate(culms):
        L = c.branch.length()
        pa, _, ra = c.branch.at(0.0)
        pb, _, rb = c.branch.at(min(1.0, 2.6 / L))
        convex_frustum(geo, pa, pb, max(ra, 0.03), max(rb, 0.028), 6, sel="Component%02d" % (i + 1))
    lods.append(geo.to_lod(mlod.LOD_GEOMETRY, props=GEO_PROPS, mass=800.0))
    cen, rad = canopy
    lods.append(memory_lod({"action": (0.0, 0.8, 0.0), "sound_TreeMediumLeaves": cen}, props={"lodnoshadow": "1"}))
    for res, fire in ((mlod.LOD_VIEW_GEOMETRY, False), (mlod.LOD_FIRE_GEOMETRY, True)):
        m = Mesh()
        k = 0
        for c in culms:
            L = c.branch.length()
            pa, _, ra = c.branch.at(0.0)
            pb, _, rb = c.branch.at(min(1.0, 4.0 / L))
            k += 1
            convex_frustum(m, pa, pb, max(ra, 0.03), max(rb, 0.025), 5, mat=WOOD_PEN if fire else "", sel="Component%02d" % k)
        k += 1
        convex_blob(m, cen, (rad[0] * 0.7, rad[1] * 0.6, rad[2] * 0.7), mat=FOLIAGE_PEN if fire else "", sel="Component%02d" % k)
        lods.append(m.to_lod(res))
    stats["geometry_components"] = len(geo.selections)
    stats["bounds"] = bounds
    p3d = os.path.join(src_dir(P_BAMBOO), name + ".p3d")
    mlod.write_mlod(p3d, lods)
    for lod, m in meshes.items():
        m.write_obj(os.path.join(WORK_MESH, "%s_lod%d.obj" % (name, lod)), {CULM_TEX: "culm", LEAF_TEX: "leaves", lod4_tex: "impostor"})
    geo.write_obj(os.path.join(WORK_MESH, "%s_geo.obj" % name), {})
    info = dict(name=name, impostor=imp_info, bounds=bounds, canopy=canopy, stats=stats,
                culms=[dict(base=c.path[0], H=c.H, r0=c.r0, young=c.young) for c in culms])
    with open(os.path.join(WORK_MESH, name + ".json"), "wb") as f:
        f.write(json.dumps(info, indent=1).encode())
    return p3d, stats


# ---------------------------------------------------------------------------------------------------------------
# JP_BambooPole
# ---------------------------------------------------------------------------------------------------------------
PI = P_ITEMS + "\\data\\"
POLE_TEX = PI + "jp_bamboo_pole_co.paa"
POLE_MAT = PI + "jp_bamboo_pole.rvmat"
POLE_TOP = 1.6               # +Y end (the "business" end, like the stick's melee end)
POLE_BUTT = POLE_TOP - POLE_LEN   # -0.9: the grip sits 0.9 m from the butt, as LongWoodenStick's sits 0.34 m from its own
POLE_R = (0.036, 0.031)      # butt, top


def pole_radius(y):
    t = (y - POLE_BUTT) / POLE_LEN
    return POLE_R[0] + (POLE_R[1] - POLE_R[0]) * t


def build_pole_lod(sides, ridges):
    mesh = Mesh()
    ys = [POLE_BUTT, POLE_TOP]
    node_ys = [POLE_TOP - n for n in POLE_NODES]
    if ridges:
        for ny in node_ys:
            ys += [ny - 0.014, ny, ny + 0.014]
    ys = sorted(set(round(y, 5) for y in ys))
    path = [(0.0, y, 0.0) for y in ys]
    radii = []
    for y in ys:
        r = pole_radius(y)
        if ridges and any(abs(y - ny) < 1e-4 for ny in node_ys):
            r += 0.0035
        radii.append(r)

    def uv(ring, f, dist):
        y = path[ring][1]
        return (f * 0.75 * 0.998, (POLE_TOP - y) / POLE_LEN)
    tube(mesh, path, radii, sides, POLE_TEX, POLE_MAT, uv, hint=(0.0, 0.0, 1.0))
    # end caps (the cut face of the culm), mapped to the cap square u 0.75..1, v 0..0.0625
    for y, nrm in ((POLE_TOP, (0.0, 1.0, 0.0)), (POLE_BUTT, (0.0, -1.0, 0.0))):
        r = pole_radius(y)
        c = mesh.point((0.0, y, 0.0))
        ring = []
        for s in range(sides):
            th = 2 * math.pi * s / sides
            ring.append((mesh.point((r * math.cos(th), y, r * math.sin(th))), th))
        cu, cv = 0.875, 0.03125
        for s in range(sides):
            (a, ta), (b, tb) = ring[s], ring[(s + 1) % sides]
            uva = (cu + 0.124 * math.cos(ta), cv + 0.0309 * math.sin(ta))
            uvb = (cu + 0.124 * math.cos(tb), cv + 0.0309 * math.sin(tb))
            mesh.face([a, b, c], [nrm] * 3, [uva, uvb, (cu, cv)], POLE_TEX, POLE_MAT, outward=nrm)
    return mesh


def build_pole(name="jp_bamboo_pole"):
    lods, meshes, stats = [], {}, {}
    for lod, (sides, ridges) in ((1, (12, True)), (2, (7, False)), (3, (4, False))):
        m = build_pole_lod(sides, ridges)
        meshes[lod] = m
        stats["lod%d" % lod] = dict(tris=m.tri_count(), bad_winding=check_winding(m))
        lods.append(m.to_lod(float(lod)))
    geo = Mesh()
    convex_frustum(geo, (0.0, POLE_BUTT, 0.0), (0.0, POLE_TOP, 0.0), POLE_R[0], POLE_R[1], 8, sel="Component01")
    lods.append(geo.to_lod(mlod.LOD_GEOMETRY, props={"autocenter": "0"}, mass=1.8))
    mid = (POLE_TOP + POLE_BUTT) / 2
    lods.append(memory_lod({
        # names and roles copied from vanilla wooden_stick_blunt.p3d's memory LOD, scaled to 2.5 m
        "boundingbox_min": (-0.04, POLE_BUTT, -0.04),
        "boundingbox_max": (0.04, POLE_TOP, 0.04),
        "ce_center": (0.0, mid, 0.0),
        "ce_radius": (0.03, POLE_TOP, 0.03),
        "meleerangestart": (0.0, -0.3, 0.0),
        "meleerangeend": (0.0, POLE_TOP, 0.0),
        "invview": (1.25, mid, -0.3),
        "throwingimpulseposition": (0.0, 0.1, 0.0),
    }))
    view = Mesh()
    convex_frustum(view, (0.0, POLE_BUTT, 0.0), (0.0, POLE_TOP, 0.0), POLE_R[0], POLE_R[1], 6, sel="Component01")
    lods.append(view.to_lod(mlod.LOD_VIEW_GEOMETRY))
    fire = Mesh()
    convex_frustum(fire, (0.0, POLE_BUTT, 0.0), (0.0, POLE_TOP, 0.0), POLE_R[0], POLE_R[1], 6, mat=WOOD_PEN, sel="Component01")
    lods.append(fire.to_lod(mlod.LOD_FIRE_GEOMETRY))
    p3d = os.path.join(src_dir(P_ITEMS), name + ".p3d")
    mlod.write_mlod(p3d, lods)
    for lod, m in meshes.items():
        m.write_obj(os.path.join(WORK_MESH, "%s_lod%d.obj" % (name, lod)), {POLE_TEX: "pole"})
    return p3d, stats


def main(argv):
    if not argv or "clump" in argv:
        p3d, st = build_clump()
        print("jp_bamboo_clump_01 ->", p3d)
        for k, v in st.items():
            print("   ", k, v)
    if not argv or "pole" in argv:
        p3d, st = build_pole()
        print("jp_bamboo_pole ->", p3d)
        for k, v in st.items():
            print("   ", k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
