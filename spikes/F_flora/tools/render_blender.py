r"""render_blender.py - headless Blender renders for the F spike (run by build.py, or by hand):

  blender --background --factory-startup --python render_blender.py -- impostor <model>
      renders the LOD4 impostor views of <model>_lod1.obj (orthographic, albedo, transparent) to
      data/F/work/tex/<model>_imp_{top,front,left}.png; build.py composes them into <model>_lod4_ca.png
  blender --background --factory-startup --python render_blender.py -- views <model> [<model> ...]
      eye-height (1.7 m) views at 5 / 30 / 150 m, each with the LOD the engine would plausibly pick there,
      plus one sheet per model with every LOD side by side, into spikes/F_flora/renders/
  blender ... -- item <model>     a close-up of an item mesh (the bamboo pole)

Meshes come from data/F/work/mesh/<model>_lod<N>.obj (written by sakura.py / bamboo.py in Blender axes, Z up).
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
WORK = os.path.join(os.path.dirname(os.path.dirname(SPIKE)), "data", "F", "work")
TEX = os.path.join(WORK, "tex")
MESH = os.path.join(WORK, "mesh")
RENDERS = os.path.join(SPIKE, "renders")

TEXMAP = {  # obj material name -> texture png (in data/F/work/tex)
    "bark": "jp_sakura_bark_co.png",
    "blossom": "jp_sakura_blossom_ca.png",
    "culm": "jp_bamboo_culm_co.png",
    "leaves": "jp_bamboo_leaves_ca.png",
    "pole": "jp_bamboo_pole_co.png",
}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def set_engine(scene):
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            scene.render.engine = eng
            return eng
        except TypeError:
            continue
    scene.render.engine = "CYCLES"
    return "CYCLES"


def make_material(name, png, albedo_only):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    img = nt.nodes.new("ShaderNodeTexImage")
    img.image = bpy.data.images.load(os.path.join(TEX, png), check_existing=True)
    img.interpolation = "Linear"
    # alpha test at 0.5, like the engine's alpha-tested foliage
    gt = nt.nodes.new("ShaderNodeMath")
    gt.operation = "GREATER_THAN"
    gt.inputs[1].default_value = 0.5
    nt.links.new(img.outputs["Alpha"], gt.inputs[0])
    if albedo_only:
        em = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(img.outputs["Color"], em.inputs["Color"])
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(gt.outputs[0], mix.inputs[0])
        nt.links.new(tr.outputs[0], mix.inputs[1])
        nt.links.new(em.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs["Surface"])
    else:
        bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
        nt.links.new(img.outputs["Color"], bs.inputs["Base Color"])
        nt.links.new(gt.outputs[0], bs.inputs["Alpha"])
        bs.inputs["Roughness"].default_value = 0.85
        if name in ("blossom", "leaves"):
            # thin petals / leaves let light through
            try:
                bs.inputs["Subsurface Weight"].default_value = 0.0
                bs.inputs["Transmission Weight"].default_value = 0.0
            except KeyError:
                pass
        nt.links.new(bs.outputs[0], out.inputs["Surface"])
    try:
        mat.surface_render_method = "DITHERED"
    except AttributeError:
        mat.blend_method = "HASHED"
    mat.use_backface_culling = False
    return mat


def import_obj(path, albedo_only=False, loc=(0, 0, 0), imp_png=None):
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=path, forward_axis="Y", up_axis="Z")
    objs = [o for o in bpy.data.objects if o not in before]
    for o in objs:
        o.location = loc
        for slot in o.material_slots:
            base = slot.material.name.split(".")[0] if slot.material else "default"
            png = TEXMAP.get(base)
            if base == "impostor" and imp_png:
                png = imp_png
            if png is None:
                continue
            key = base + ("_albedo" if albedo_only else "") + ("_" + png)
            m = bpy.data.materials.get(key) or make_material(key, png, albedo_only)
            m.name = key
            slot.material = m
    return objs


def ortho_camera(loc, rot, scale):
    cam = bpy.data.cameras.new("cam")
    cam.type = "ORTHO"
    cam.ortho_scale = scale
    cam.clip_end = 1000
    ob = bpy.data.objects.new("cam", cam)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = rot
    bpy.context.scene.camera = ob
    return ob


def persp_camera(loc, target, hfov_deg):
    cam = bpy.data.cameras.new("cam")
    cam.sensor_fit = "HORIZONTAL"
    cam.angle = math.radians(hfov_deg)
    cam.clip_end = 3000
    ob = bpy.data.objects.new("cam", cam)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = ob
    return ob


def render(path, w, h, transparent=False, samples=32):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    if transparent or path.endswith(".png"):
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    else:
        sc.render.image_settings.file_format = "JPEG"
        sc.render.image_settings.color_mode = "RGB"
        sc.render.image_settings.quality = 90
    try:
        sc.eevee.taa_render_samples = samples
    except AttributeError:
        pass
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


def outdoor_scene():
    sc = bpy.context.scene
    eng = set_engine(sc)
    sc.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("sky")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.55, 0.68, 0.85, 1.0)
    bg.inputs[1].default_value = 0.55
    sc.world = world
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 4.0
    sun.angle = math.radians(2.0)
    so = bpy.data.objects.new("sun", sun)
    so.rotation_euler = (math.radians(50), 0, math.radians(35))
    sc.collection.objects.link(so)
    # ground
    bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, 0))
    g = bpy.context.active_object
    gm = bpy.data.materials.new("ground")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.16, 0.22, 0.07, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    g.data.materials.append(gm)
    # a 1.8 m person-sized post for scale
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.8, location=(0, 0, 0.9))
    post = bpy.context.active_object
    pm = bpy.data.materials.new("post")
    pm.use_nodes = True
    pm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.1, 0.1, 1)
    post.data.materials.append(pm)
    return eng, post


# ---------------------------------------------------------------------------------------------------------------
def do_impostor(model):
    reset()
    sc = bpy.context.scene
    set_engine(sc)
    sc.view_settings.view_transform = "Standard"
    info = json.load(open(os.path.join(MESH, model + ".json")))
    S = info["impostor"]["S"]
    import_obj(os.path.join(MESH, model + "_lod1.obj"), albedo_only=True)
    world = bpy.data.worlds.new("w")
    sc.world = world
    res = 512
    # front: camera at Blender -Y (= p3d -Z) looking +Y; frame x in [-S/2, S/2], z in [0, S]
    ortho_camera((0, -100, S / 2), (math.radians(90), 0, 0), S)
    render(os.path.join(TEX, model + "_imp_front.png"), res, res, transparent=True)
    # left: camera at Blender -X looking +X (image left = +Y_blender = p3d +Z)
    bpy.data.objects.remove(sc.camera)
    ortho_camera((-100, 0, S / 2), (math.radians(90), 0, math.radians(-90)), S)
    render(os.path.join(TEX, model + "_imp_left.png"), res, res, transparent=True)
    # top: camera above looking down, image up = +Y_blender (= p3d +Z / north), right = +X
    bpy.data.objects.remove(sc.camera)
    ortho_camera((0, 0, 200), (0, 0, 0), S)
    render(os.path.join(TEX, model + "_imp_top.png"), res, res, transparent=True)


def do_views(models):
    for model in models:
        info = json.load(open(os.path.join(MESH, model + ".json")))
        (x0, y0, z0), (x1, y1, z1) = info["bounds"]
        H = y1
        imp_png = model + "_lod4_ca.png"
        for dist, lods in ((5, (1,)), (30, (1, 2)), (150, (3, 4))):
            for lod in lods:
                reset()
                eng, post = outdoor_scene()
                import_obj(os.path.join(MESH, "%s_lod%d.obj" % (model, lod)), imp_png=imp_png)
                post.location = (1.6, -1.0, 0.9)
                # stand south of the tree (Blender -Y), eye height 1.7 m, look at the crown
                target = (0, 0, min(H * 0.55, 1.7 + dist * 0.35))
                if dist == 5:
                    target = (0, 0, 3.2)
                persp_camera((0.8, -dist, 1.7), target, 74)
                name = "%s_%03dm_lod%d.jpg" % (model, dist, lod)
                render(os.path.join(RENDERS, name), 1280, 720)
                print("RENDERED", name, eng)
        # LOD sheet: every LOD side by side, same camera
        reset()
        eng, post = outdoor_scene()
        post.location = (0, -6, 0.9)
        W = max(x1 - x0, z1 - z0) + 1.5
        for i, lod in enumerate((1, 2, 3, 4)):
            import_obj(os.path.join(MESH, "%s_lod%d.obj" % (model, lod)), loc=((i - 1.5) * W, 0, 0), imp_png=imp_png)
        persp_camera((0, -W * 4.4, H * 0.6), (0, 0, H * 0.5), 45)
        render(os.path.join(RENDERS, "%s_lods.jpg" % model), 1600, 560)
        print("RENDERED lods", model)


def do_item(model):
    reset()
    eng, post = outdoor_scene()
    bpy.data.objects.remove(post)
    for i, lod in enumerate((1, 2, 3)):
        objs = import_obj(os.path.join(MESH, "%s_lod%d.obj" % (model, lod)), loc=(i * 0.35 - 0.35, 0, 1.0))
    persp_camera((0.9, -2.4, 1.55), (0, 0, 1.3), 50)
    render(os.path.join(RENDERS, "%s_lods.jpg" % model), 1280, 720)
    # close-up of the node / end cap
    reset()
    eng, post = outdoor_scene()
    bpy.data.objects.remove(post)
    import_obj(os.path.join(MESH, "%s_lod1.obj" % model), loc=(0, 0, 1.0))
    persp_camera((0.45, -0.7, 2.95), (0, 0, 2.5), 40)
    render(os.path.join(RENDERS, "%s_closeup.jpg" % model), 1280, 720)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    mode, models = argv[0], argv[1:]
    if mode == "impostor":
        for m in models:
            do_impostor(m)
    elif mode == "views":
        do_views(models)
    elif mode == "item":
        for m in models:
            do_item(m)


main()
