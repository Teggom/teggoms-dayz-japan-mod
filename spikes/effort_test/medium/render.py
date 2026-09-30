"""Blender (background) preview of the built MLODs: blender --background --python render.py
Renders the Resolution-1 LOD (and Res 2/3 for one view) of both states as they ship, from out/*.p3d."""
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402

OUT = os.path.join(HERE, "out")
REN = os.path.join(HERE, "renders")
TEX = os.path.join(HERE, "tex")
_M = {}


def material(tex):
    if tex in _M:
        return _M[tex]
    m = bpy.data.materials.new(os.path.basename(tex))
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    png = os.path.join(TEX, os.path.splitext(os.path.basename(tex.replace("\\", "/")))[0] + ".png")
    iron = "iron" in tex
    b.inputs["Roughness"].default_value = 0.55 if iron else 0.85
    if iron:
        b.inputs["Metallic"].default_value = 0.4
    if os.path.isfile(png):
        t = m.node_tree.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(png, check_existing=True)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (1, 0, 1, 1)
    _M[tex] = m
    return m


def plain(name, rgb, rough=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = rgb + (1.0,)
    b.inputs["Roughness"].default_value = rough
    return m


def load(p3d, res):
    lod = [l for l in mlod.read_mlod(os.path.join(OUT, p3d)) if mlod.same_res(l.resolution, res)][0]
    verts, polys, uvs, mids, mats, mi = [], [], [], [], [], {}
    for fverts, _, tex, _ in lod.faces:
        base = len(verts)
        for pi, ni, u, v in fverts:
            p = lod.points[pi]
            verts.append((p[0], p[2], p[1]))            # p3d (x, y up, z fwd) -> blender (x, y fwd, z up)
            uvs.append((u, 1.0 - v))
        polys.append(list(range(base, base + len(fverts))))
        if tex not in mi:
            mi[tex] = len(mats)
            mats.append(material(tex))
        mids.append(mi[tex])
    me = bpy.data.meshes.new(p3d)
    me.from_pydata(verts, [], polys)
    uv = me.uv_layers.new(name="UVMap")
    for i, loop in enumerate(me.loops):
        uv.data[i].uv = uvs[loop.vertex_index]
    for m in mats:
        me.materials.append(m)
    for i, k in enumerate(mids):
        me.polygons[i].material_index = k
    me.update()
    ob = bpy.data.objects.new(p3d, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob, len(lod.faces)


def setup():
    sc = bpy.context.scene
    for ob in list(bpy.data.objects):          # the factory cube, camera and light
        bpy.data.objects.remove(ob, do_unlink=True)
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            pass
    sc.render.resolution_x, sc.render.resolution_y = 640, 640
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("sky")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.78, 0.80, 0.83, 1.0)
    bg.inputs[1].default_value = 0.8
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))
    sc.collection.objects.link(sun)
    bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(plain("floor", (0.42, 0.38, 0.28)))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def look(cam, target, az, el, dist, lens=50):
    a, e = math.radians(az), math.radians(el)
    d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
    cam.location = Vector(target) + d * dist
    cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = (-d).to_track_quat("-Z", "Y")
    cam.data.lens = lens
    cam.data.clip_start = 0.02


VIEWS = [  # name, target, azimuth (0 = front), elevation, distance, lens, lod
    ("front", (0, 0.2, 0.55), 0, 8, 3.6, 50, 1),
    ("3q", (0, 0.2, 0.5), 35, 22, 3.6, 50, 1),
    ("back", (0, 0, 0.5), 200, 20, 3.4, 50, 1),
    ("closeup", (0.30, 0.22, 0.78), 20, 14, 1.25, 50, 1),
    ("side_handle", (0.5, 0.0, 0.62), 78, 14, 1.4, 50, 1),
    ("lod2_3q", (0, 0.2, 0.5), 35, 22, 3.6, 50, 2),
    ("lod3_3q", (0, 0.2, 0.5), 35, 22, 3.6, 50, 3),
]


def main():
    os.makedirs(REN, exist_ok=True)
    cam = setup()
    for state, p3d in (("intact", "jp_efftest_medium_tansu.p3d"), ("ransacked", "jp_efftest_medium_tansu_ransacked.p3d")):
        for name, tgt, az, el, dist, lens, res in VIEWS:
            ob, nf = load(p3d, res)
            look(cam, tgt, az, el, dist, lens)
            bpy.context.scene.render.filepath = os.path.join(REN, "%s_%s.png" % (state, name))
            bpy.ops.render.render(write_still=True)
            print("rendered", state, name, "faces", nf)
            bpy.data.objects.remove(ob, do_unlink=True)


main()
