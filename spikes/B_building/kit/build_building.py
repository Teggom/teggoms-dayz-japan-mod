"""Blender entry point of the Japanese building kit.

  blender --background --python kit/build_building.py -- jp_machiya_01 [jp_machiya_02 ...] [--no-render]

Per variant (kit/variants.py):
  1. jpkit.machiya.generate(params)         -> the model (solids, roadway, memory, doors, floors)
  2. jpkit.p3d.write_p3d                    -> out/<name>/<name>.p3d  (MLOD, every LOD)
  3. model.cfg / config.cpp class / CE proto group / summary JSON -> out/<name>/
  4. a Blender scene with one collection per LOD, saved as out/<name>/<name>.blend
  5. renders -> renders/<name>_*.jpg (street, back, plan cut, section cut, stair, doors open, every LOD)
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
B = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(B, "out")
RENDERS = os.path.join(B, "renders")
TEXTURES = os.path.abspath(os.path.join(B, "..", "..", "data", "B", "textures"))

from jpkit import machiya, p3d, cfg, loot  # noqa: E402
from jpkit.geom import face_uvs, newell, norm, dot  # noqa: E402
from jpkit.materials import MATS, PREVIEW  # noqa: E402
from variants import VARIANTS  # noqa: E402

try:
    import bpy
    import bmesh  # noqa: F401
    from mathutils import Vector
except ImportError:          # plain python: files only
    bpy = None


def model_path(name):
    return "\\JP\\structures\\machiya\\%s.p3d" % name


def write_files(name, model):
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    lods = p3d.write_p3d(model, os.path.join(d, name + ".p3d"))
    sk, mdl = cfg.modelcfg_parts(model)
    with open(os.path.join(d, "modelcfg_part.txt"), "wb") as f:
        f.write((sk + "\n//--\n" + mdl).encode("ascii"))
    with open(os.path.join(d, "config_class.txt"), "wb") as f:
        f.write(cfg.config_class(model, model_path(name)).encode("ascii"))
    grp, pts = loot.proto_group(model)
    with open(os.path.join(d, "proto_group.xml"), "wb") as f:
        f.write(grp.encode("ascii"))
    summary = {
        "name": name, "class": model.params["class"], "params": model.params,
        "doors": [{"cfg": x.cfg, "bone": x.bone, "kind": x.kind, "width": x.width, "slide": x.slide,
                   "direction": x.direction, "centre": x.centre, "action": x.action, "note": x.note,
                   "leaf_bbox": x.leaf.bbox()} for x in model.doors],
        "floors": model.floors,
        "loot": pts,
        "stair": getattr(model, "stair", None),
        "roadway": [{"pts": r[0], "surface": r[1]} for r in model.roadway],
        "memory": model.memory,
        "lods": [{"res": l.resolution, "points": len(l.points), "faces": len(l.faces),
                  "components": len([s for s in l.selections if s.startswith("Component")])} for l in lods],
        "bbox": _bbox(model),
    }
    with open(os.path.join(d, name + "_summary.json"), "wb") as f:
        f.write(json.dumps(summary, indent=1).encode("ascii"))
    print("wrote", d, "-", ", ".join("%g:%d" % (l.resolution, len(l.faces)) for l in lods))
    return summary


def _bbox(model):
    xs, ys, zs = [], [], []
    for s in model.solids:
        if s.vis:
            b = s.bbox()
            xs += [b[0], b[1]]
            ys += [b[2], b[3]]
            zs += [b[4], b[5]]
    return [min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)]


# ------------------------------------------------------------------------------------------------------
# Blender scene
# ------------------------------------------------------------------------------------------------------
def to_b(p):
    """p3d (x right, y up, z forward) -> Blender (x right, y forward, z up)."""
    return (p[0], p[2], p[1])


_MAT_CACHE = {}


def bl_material(key, color=None, image=None):
    if key in _MAT_CACHE:
        return _MAT_CACHE[key]
    mat = bpy.data.materials.new(key)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 0.8
    if image and os.path.isfile(image):
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(image, check_existing=True)
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        c = color or (0.7, 0.7, 0.7)
        bsdf.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1.0)
    _MAT_CACHE[key] = mat
    return mat


def vis_material(mat):
    return bl_material("vis_" + mat, PREVIEW.get(mat), os.path.join(TEXTURES, MATS[mat]["tex"] + "_co.png"))


def mesh_from_faces(name, faces, coll):
    """faces: [(pts_p3d, outward_p3d, uvs, material)] -> object."""
    verts, polys, uvs_all, mats = [], [], [], []
    mat_index = {}
    for pts, outward, uvs, mat in faces:
        bp = [to_b(p) for p in pts]
        n = newell(bp)
        ob = to_b(outward)
        order = list(range(len(bp)))
        if dot(n, ob) < 0:
            order = order[::-1]
        base = len(verts)
        verts.extend(bp[i] for i in order)
        polys.append(list(range(base, base + len(bp))))
        uvs_all.extend((uvs[i][0], 1.0 - uvs[i][1]) for i in order)
        if mat.name not in mat_index:
            mat_index[mat.name] = len(mat_index)
            mats.append(mat)
        polys[-1] = (polys[-1], mat_index[mat.name])
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], [p for p, _ in polys])
    uv = me.uv_layers.new(name="UVMap")
    for i, loop in enumerate(me.loops):
        uv.data[i].uv = uvs_all[loop.vertex_index]
    for m in mats:
        me.materials.append(m)
    for i, (_, mi) in enumerate(polys):
        me.polygons[i].material_index = mi
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def solid_faces(s, matfn):
    out = []
    for fi in range(len(s.faces)):
        mat = s.face_mat(fi)
        out.append((s.face_points(fi), s.outward(fi), face_uvs(s, fi, MATS[mat]), matfn(s, mat)))
    return out


PALETTE = [(0.85, 0.33, 0.25), (0.25, 0.55, 0.85), (0.35, 0.75, 0.35), (0.9, 0.75, 0.2), (0.65, 0.4, 0.8),
           (0.2, 0.75, 0.75), (0.9, 0.5, 0.15), (0.55, 0.55, 0.55)]
FIRE_COL = {"dirt": (0.75, 0.55, 0.3), "wood": (0.55, 0.3, 0.12), "pottery": (0.7, 0.2, 0.2),
            "fabric_thin": (0.95, 0.95, 0.6), "granite": (0.5, 0.5, 0.55)}
ROAD_COL = {"doma": (0.6, 0.4, 0.2), "tatami": (0.6, 0.8, 0.3), "boards": (0.8, 0.6, 0.3),
            "stair": (0.9, 0.2, 0.2), "stone_ext": (0.55, 0.55, 0.6)}


def build_scene(name, model):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _MAT_CACHE.clear()
    scene = bpy.context.scene
    colls = {}

    def coll(cname):
        if cname not in colls:
            c = bpy.data.collections.new(cname)
            scene.collection.children.link(c)
            colls[cname] = c
        return colls[cname]

    # resolution LODs: one object per (lod, tag, door) so renders can hide groups
    for k in (1, 2, 3):
        groups = {}
        for s in model.solids:
            if k in s.vis:
                key = s.door or s.tag or "misc"
                groups.setdefault(key, []).append(s)
        for key, ss in groups.items():
            faces = []
            for s in ss:
                faces += solid_faces(s, lambda s_, m_: vis_material(m_))
            ob = mesh_from_faces("Res%d_%s" % (k, key), faces, coll("Res%d" % k))
            ob["tag"] = key
    # component LODs
    for lname, flag in (("Geometry", "geo"), ("ViewGeometry", "view"), ("FireGeometry", "fire")):
        n = 0
        for s in model.solids:
            if (flag == "geo" and s.geo) or (flag == "view" and s.view) or (flag == "fire" and s.fire):
                n += 1
                if flag == "fire":
                    col = FIRE_COL.get(s.fire, (1, 0, 1))
                else:
                    col = (0.95, 0.85, 0.1) if s.door else PALETTE[n % len(PALETTE)]
                m = bl_material("%s_%s" % (lname, col), col)
                faces = [(s.face_points(fi), s.outward(fi), [(0, 0)] * len(s.faces[fi]), m)
                         for fi in range(len(s.faces))]
                ob = mesh_from_faces("%s_%02d_%s" % (lname, n, s.door or s.tag), faces, coll(lname))
                ob["tag"] = s.door or s.tag
    # roadway, one object per level so the upper floor can be hidden
    levels = {}
    for pts, surf in model.roadway:
        n = norm(newell(pts))
        if n[1] < 0:
            n = (-n[0], -n[1], -n[2])
        lvl = "road_upper" if min(p[1] for p in pts) > 2.0 else "road_ground"
        levels.setdefault(lvl, []).append((pts, n, [(0, 0)] * len(pts), bl_material("road_" + surf, ROAD_COL[surf])))
    for lvl, faces in levels.items():
        ob = mesh_from_faces("Roadway_" + lvl, faces, coll("Roadway"))
        ob["tag"] = lvl
    # memory: small spheres, axes as thin boxes
    mc = coll("Memory")
    red = bl_material("mem_axis", (1.0, 0.1, 0.1))
    blue = bl_material("mem_action", (0.1, 0.3, 1.0))
    grn = bl_material("mem_leaf", (0.1, 0.9, 0.2))
    for sel, pts in model.memory.items():
        mat = red if sel.endswith("_axis") else (blue if sel.endswith("_action") else grn)
        for i, p in enumerate(pts):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12 if i == 0 else 0.08, location=to_b(p), segments=12,
                                                 ring_count=6)
            ob = bpy.context.active_object
            ob.name = "mem_%s_%d" % (sel, i)
            if not sel.endswith(("_axis", "_action")):
                ob["tag"] = sel          # leaf-centre point moves with its door (bone doorsN)
            ob.data.materials.append(mat)
            for c in ob.users_collection:
                c.objects.unlink(ob)
            mc.objects.link(ob)
        if sel.endswith("_axis"):
            a, b_ = Vector(to_b(pts[0])), Vector(to_b(pts[1]))
            mid = (a + b_) / 2
            bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=(b_ - a).length, location=mid, vertices=8)
            ob = bpy.context.active_object
            ob.rotation_mode = "QUATERNION"
            ob.rotation_quaternion = (b_ - a).to_track_quat("Z", "Y")
            ob.data.materials.append(red)
            for c in ob.users_collection:
                c.objects.unlink(ob)
            mc.objects.link(ob)
    # loot points: small green discs on the floors (in Memory-ish helper collection)
    lc = coll("Loot")
    lm = bl_material("loot", (0.1, 1.0, 0.4))
    for pnt in loot.all_points(model):
        bpy.ops.mesh.primitive_cylinder_add(radius=pnt["range"], depth=0.02, location=to_b(
            (pnt["model"][0], pnt["model"][1] + 0.02, pnt["model"][2])), vertices=24)
        ob = bpy.context.active_object
        ob.data.materials.append(lm)
        for c in ob.users_collection:
            c.objects.unlink(ob)
        lc.objects.link(ob)
    # ground
    gc = coll("Ground")
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.002))
    g = bpy.context.active_object
    g.data.materials.append(bl_material("ground", (0.32, 0.36, 0.26)))
    for c in g.users_collection:
        c.objects.unlink(g)
    gc.objects.link(g)
    return colls


def setup_render(scene):
    try:
        scene.render.engine = "BLENDER_EEVEE"
    except TypeError:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 800
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    try:
        scene.eevee.taa_render_samples = 32
    except AttributeError:
        pass
    world = bpy.data.worlds.new("sky")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.62, 0.72, 0.85, 1.0)
    bg.inputs[1].default_value = 0.9
    sun_d = bpy.data.lights.new("sun", "SUN")
    sun_d.energy = 3.5
    sun_d.angle = math.radians(3)
    sun = bpy.data.objects.new("sun", sun_d)
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(150))
    scene.collection.objects.link(sun)
    cam_d = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cam_d)
    scene.collection.objects.link(cam)
    scene.camera = cam
    return cam, sun


def look_at(cam, loc, target, lens=28, ortho=None, clip_start=0.1):
    cam.location = Vector(loc)
    d = Vector(target) - Vector(loc)
    cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = d.to_track_quat("-Z", "Y")
    if ortho:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho
    else:
        cam.data.type = "PERSP"
        cam.data.lens = lens
    cam.data.clip_start = clip_start
    cam.data.clip_end = 500


def show(colls, names, hide_tags=()):
    for cname, c in colls.items():
        c.hide_render = cname not in names
        for ob in c.objects:
            ob.hide_render = ob.get("tag", "") in hide_tags


def render(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("render", path)


def add_point_lights(model, names=()):
    lights = []
    for f in model.floors:
        x0, x1, z0, z1 = f["rect"]
        ld = bpy.data.lights.new("pl_" + f["name"], "POINT")
        ld.energy = 250
        ld.shadow_soft_size = 0.5
        ob = bpy.data.objects.new("pl_" + f["name"], ld)
        ob.location = to_b(((x0 + x1) / 2, f["y"] + 1.9, (z0 + z1) / 2))
        bpy.context.scene.collection.objects.link(ob)
        lights.append(ob)
    return lights


def set_doors_open(colls, model, amount):
    for d in model.doors:
        off = Vector(to_b(tuple(c * d.slide * amount for c in d.direction)))
        for cname in ("Res1", "Res2", "Res3"):
            ob = bpy.data.objects.get("%s_%s" % (cname, d.bone))
            if ob:
                ob.location = off


def renders(name, model, colls):
    scene = bpy.context.scene
    cam, sun = setup_render(scene)
    os.makedirs(RENDERS, exist_ok=True)
    R = lambda tag: os.path.join(RENDERS, "%s_%s.jpg" % (name, tag))
    b = _bbox(model)
    h = b[3]
    far = max(b[1] - b[0], b[5] - b[4])
    # street view (front = +z p3d = +y blender), eye height 1.7
    show(colls, {"Res1", "Ground"})
    look_at(cam, (4.0, b[5] + 11.0, 1.7), (0.0, 0.0, h * 0.42), lens=24)
    render(scene, R("res1_street"))
    look_at(cam, (-3.5, b[4] - 11.0, 1.7), (0.0, 0.0, h * 0.42), lens=24)
    render(scene, R("res1_back"))
    three_q = ((far * 1.25, far * 1.45, h * 1.25), (0, 0, h * 0.35))
    look_at(cam, three_q[0], three_q[1], lens=30)
    render(scene, R("res1_3q"))
    # every LOD from the same 3/4 camera
    for cname in ("Res2", "Res3"):
        show(colls, {cname, "Ground"})
        render(scene, R(cname.lower() + "_3q"))
    lights = add_point_lights(model)
    for cname in ("Geometry", "ViewGeometry", "FireGeometry"):
        show(colls, {cname, "Ground"})
        render(scene, R(cname.lower() + "_3q"))
    # plan views (portrait, street front at the bottom): everything above floor + 1.6 m clipped away
    top = h + 5.0
    scene.render.resolution_x, scene.render.resolution_y = 800, 1280
    oscale = max((b[5] - b[4]) * 1.08, (b[1] - b[0]) * 1.08 * 1280 / 800)
    cut_y = model.params["floor_room"] + 1.6
    look_at(cam, (0.0, 0.001, top), (0.0, 0.0, 0.0), ortho=oscale, clip_start=top - cut_y)
    show(colls, {"Res1", "Ground", "Loot"})
    render(scene, R("plan_ground_loot"))
    show(colls, {"Res1", "Ground"})
    set_doors_open(colls, model, 1.0)
    render(scene, R("plan_ground_doors_open"))
    set_doors_open(colls, model, 0.0)
    render(scene, R("plan_ground_doors_closed"))
    show(colls, {"Geometry", "Ground"})
    render(scene, R("plan_ground_geometry"))
    show(colls, {"Res1", "Memory", "Ground"})
    render(scene, R("plan_ground_memory"))
    if model.params["storeys"] == 2:
        FU = model.params["floor_upper"]
        cut_y = FU + 1.6
        look_at(cam, (0.0, 0.001, top), (0.0, 0.0, 0.0), ortho=oscale, clip_start=top - cut_y)
        show(colls, {"Res1", "Ground", "Loot"})
        render(scene, R("plan_upper_loot"))
        show(colls, {"Res1", "Ground"})
        set_doors_open(colls, model, 1.0)
        render(scene, R("plan_upper_doors_open"))
        set_doors_open(colls, model, 0.0)
        show(colls, {"Res1", "Memory", "Ground"})
        render(scene, R("plan_upper_memory"))
    scene.render.resolution_x, scene.render.resolution_y = 1280, 800
    # roadway from the 3/4 camera: ground level alone, then everything
    look_at(cam, three_q[0], three_q[1], lens=30)
    show(colls, {"Roadway", "Ground"}, hide_tags=("road_upper",))
    render(scene, R("roadway_ground_3q"))
    show(colls, {"Roadway", "Ground"})
    render(scene, R("roadway_all_3q"))
    # section: camera west of the house looking east, cut through the rooms column
    xcut = -1.3 if model.params["toriniwa_side"] == "east" else 1.3
    sx = -30.0 if xcut < 0 else 30.0
    look_at(cam, (sx, 0.0, h * 0.45), (0.0, 0.0, h * 0.45), ortho=max(b[5] - b[4], h) * 1.15,
            clip_start=abs(sx - xcut))
    show(colls, {"Res1", "Ground"})
    render(scene, R("section_res1"))
    set_doors_open(colls, model, 1.0)
    render(scene, R("section_res1_doors_open"))
    set_doors_open(colls, model, 0.0)
    show(colls, {"Geometry", "Ground"})
    render(scene, R("section_geometry"))
    # interior: the stair from the toriniwa-side shoji of the stair room, roof and upper floor visible
    st = getattr(model, "stair", None)
    if st:
        show(colls, {"Res1", "Ground"})
        eye = to_b((st["foot"] + 0.35, model.params["floor_room"] + 1.65, st["z1"] + 1.9))
        tgt = to_b(((st["x_t"] + st["foot"]) / 2, model.params["floor_room"] + 1.2, (st["z0"] + st["z1"]) / 2))
        look_at(cam, eye, tgt, lens=16)
        render(scene, R("interior_stair"))
        # upper floor looking back at the stairwell
        eye = to_b((0.8, model.params["floor_upper"] + 1.65, 3.5))
        tgt = to_b((st["x_t"], model.params["floor_upper"] + 0.3, st["z1"]))
        look_at(cam, eye, tgt, lens=16)
        render(scene, R("interior_upper"))
    # interior of the doma looking to the back
    XT = model.dims["XT"]
    X1 = model.dims["X1"]
    sgn = 1 if model.params["toriniwa_side"] == "east" else -1
    xm = sgn * (XT + X1) / 2
    show(colls, {"Res1", "Ground"})
    look_at(cam, to_b((xm, 1.6, model.dims["Z1"] - 0.6)), to_b((xm - sgn * 0.3, 1.4, 0.0)), lens=16)
    render(scene, R("interior_toriniwa"))
    for l in lights:
        bpy.data.objects.remove(l)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    names = [a for a in argv if not a.startswith("--")] or ["jp_machiya_01"]
    do_render = "--no-render" not in argv
    for name in names:
        model = machiya.generate(VARIANTS[name])
        write_files(name, model)
        if bpy is None:
            continue
        colls = build_scene(name, model)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, name, name + ".blend"))
        if do_render:
            renders(name, model, colls)
            bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, name, name + ".blend"))


if __name__ == "__main__":
    main()
