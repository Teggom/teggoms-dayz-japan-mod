#!/usr/bin/env python3
r"""render_fx2.py - FX2 close-up renders of prop MLOD masters (textured, smooth normals from the MLOD), for the FX2
contact sheets. Blender in the background (parts/kit/render_parts.py sky + sun helpers).

  python render_fx2.py <jobs.json>      jobs: [{"out": name, "items": [[master, x, y, z, yaw_deg]], "cam": [x, y, z],
                                                 "look": [x, y, z], "lens": mm, "res": [w, h], "lod": 1}]
-> spikes/FX2/renders/<out>.png. DayZ model space is left-handed; render_parts.to_b (x, y, z) -> (x, z, y) is itself a
mirror, so these renders already show what a player sees (a statue's right hand, +x, on the viewer's left).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUT = os.path.join(HERE, "renders")


def blender_main(jobs):
    import bpy
    import math
    from mathutils import Vector
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    sys.path.insert(0, KIT)
    exec(compile(src, "render_parts.py", "exec"), g)
    from jpparts import mlod
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"]((1000, 1000))
    gm = g["plain"]("ground", (0.36, 0.37, 0.33))
    mats = {}

    def mat_for(tex):
        if tex in mats:
            return mats[tex]
        m = bpy.data.materials.new(os.path.basename(tex))
        m.use_nodes = True
        nt = m.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        bsdf.inputs["Roughness"].default_value = 0.75 if "gilt" in tex else 0.88
        if "gilt" in tex or "bronze" in tex:
            bsdf.inputs["Metallic"].default_value = 0.35
        png = os.path.join(TEXPNG, os.path.basename(tex).replace(".paa", ".png"))
        if os.path.isfile(png):
            t = nt.nodes.new("ShaderNodeTexImage")
            t.image = bpy.data.images.load(png, check_existing=True)
            nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
            if tex.endswith("_ca.paa"):
                out = nt.nodes.get("Material Output")
                tr = nt.nodes.new("ShaderNodeBsdfTransparent")
                mix = nt.nodes.new("ShaderNodeMixShader")
                gt = nt.nodes.new("ShaderNodeMath")
                gt.operation = "GREATER_THAN"
                gt.inputs[1].default_value = 0.5
                nt.links.new(t.outputs["Alpha"], gt.inputs[0])
                nt.links.new(gt.outputs[0], mix.inputs[0])
                nt.links.new(tr.outputs[0], mix.inputs[1])
                nt.links.new(bsdf.outputs[0], mix.inputs[2])
                nt.links.new(mix.outputs[0], out.inputs["Surface"])
                try:
                    m.surface_render_method = "DITHERED"
                except Exception:
                    m.blend_method = "CLIP"
        else:
            bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        mats[tex] = m
        return m

    cache = {}

    def add(master, x, y, z, yaw, lodres):
        key = (master, lodres)
        if key not in cache:
            cache[key] = next(l for l in mlod.read_mlod(master) if abs(l.resolution - lodres) < 1e-3)
        lod = cache[key]
        c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))

        def w(p):
            return (x + p[0] * c + p[2] * s, y + p[1], z - p[0] * s + p[2] * c)

        def wn(n):
            return (n[0] * c + n[2] * s, n[1], -n[0] * s + n[2] * c)
        verts, polys, uvs, nrm, mids, ml = [], [], [], [], [], []
        for fv, fl, tex, mat in lod.faces:
            pts = [g["to_b"](w(lod.points[v[0]])) for v in fv]
            ns = [g["to_b"](wn(tuple(-q for q in lod.normals[v[1]]))) for v in fv]
            # winding: Blender's polygon normal must agree with the MLOD (outward) normal
            nx = ny = nz = 0.0
            for i in range(len(pts)):
                x0, y0, z0 = pts[i]
                x1, y1, z1 = pts[(i + 1) % len(pts)]
                nx += (y0 - y1) * (z0 + z1)
                ny += (z0 - z1) * (x0 + x1)
                nz += (x0 - x1) * (y0 + y1)
            ws = (sum(q[0] for q in ns), sum(q[1] for q in ns), sum(q[2] for q in ns))
            order = list(range(len(pts)))
            if nx * ws[0] + ny * ws[1] + nz * ws[2] < 0:
                order = order[::-1]
            base = len(verts)
            verts += [pts[i] for i in order]
            nrm += [ns[i] for i in order]
            polys.append(list(range(base, base + len(pts))))
            uvs += [(fv[i][2], 1.0 - fv[i][3]) for i in order]
            if tex not in ml:
                ml.append(tex)
            mids.append(ml.index(tex))
        me = bpy.data.meshes.new("m")
        me.from_pydata(verts, [], polys)
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index]
        for k in ml:
            me.materials.append(mat_for(k))
        for i, mi in enumerate(mids):
            me.polygons[i].material_index = mi
            me.polygons[i].use_smooth = True
        me.update()
        try:
            me.normals_split_custom_set([nrm[l.vertex_index] for l in me.loops])
        except Exception as e:  # noqa: BLE001
            print("normals", e)
        ob = bpy.data.objects.new("o", me)
        bpy.context.scene.collection.objects.link(ob)

    os.makedirs(OUT, exist_ok=True)
    for j in jobs:
        g["clear_objects"]()
        sc = bpy.context.scene
        sc.render.resolution_x, sc.render.resolution_y = j.get("res", [900, 900])
        for it in j["items"]:
            add(it[0], it[1], it[2], it[3], it[4] if len(it) > 4 else 0.0, j.get("lod", 1.0))
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.002))
        bpy.context.active_object.data.materials.append(gm)
        cpos = Vector(g["to_b"](j["cam"]))
        t = Vector(g["to_b"](j["look"]))
        cam.location = cpos
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = (t - cpos).to_track_quat("-Z", "Y")
        cam.data.type = "PERSP"
        cam.data.lens = j.get("lens", 50)
        cam.data.clip_start = 0.02
        lamp = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "SUN"))
        lamp.data.energy = j.get("fill_w", 2.2)
        lamp.location = cpos
        d = (t - cpos).normalized()
        lamp.rotation_mode = "QUATERNION"
        lamp.rotation_quaternion = (d + Vector((0.7, 0.0, -1.1))).normalized().to_track_quat("-Z", "Y")
        sc.collection.objects.link(lamp)
        sc.render.filepath = os.path.join(OUT, j["out"] + ".png")
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(lamp, do_unlink=True)
        print("rendered", j["out"])


def run(jobs, nproc=3):
    """Render jobs in up to nproc Blender processes (README rule 2b: <= 4)."""
    os.makedirs(os.path.join(HERE, "_build"), exist_ok=True)
    chunks = [jobs[i::nproc] for i in range(nproc) if jobs[i::nproc]]
    procs = []
    for k, ch in enumerate(chunks):
        jp = os.path.join(HERE, "_build", "rjobs_%d.json" % k)
        with open(jp, "wb") as f:
            f.write(json.dumps(ch).encode())
        procs.append(subprocess.Popen([BLENDER, "--background", "--factory-startup", "--python", __file__, "--", jp],
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
    for p in procs:
        p.communicate()
    for j in jobs:
        fp = os.path.join(OUT, j["out"] + ".png")
        if not os.path.isfile(fp):
            print("MISSING", fp)


if __name__ == "__main__":
    if "--" in sys.argv:
        blender_main(json.load(open(sys.argv[sys.argv.index("--") + 1], encoding="utf-8")))
    else:
        run(json.load(open(sys.argv[1], encoding="utf-8")))
