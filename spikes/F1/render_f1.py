#!/usr/bin/env python3
r"""render_f1.py - F1 (G4 walk fixes) before/after renders FROM WRITTEN MLOD MASTERS, as the game draws them.

  python render_f1.py <jobs.json>     renders every job -> spikes/F1/renders/<out>.png

A copy of the L2 renderer's Blender side (spikes/L2/render_l2.py; that file is not changed) with:
  - DayZ (x, y, z) -> Blender (x, z, y): a reflection, so the left-handed model space renders as the game shows it
  - "cull": true  -> back faces hidden (the game draws single-sided faces from their outward side only)
  - "cam" / "look": an explicit camera position and target in DayZ model metres (else "view" = auto fit)
  - items: {"p3d", "lod" (1.0 | "geo" | "road" ...), "off": [x, y, z], "yaw": deg (+x -> -z seen from above,
    the proxies.frame convention), "tint": "red" | "green" (translucent overlay: collision / roadway)}
  - "boxes": [[x0, x1, y0, y1, z0, z1, [r, g, b]], ...] plain stand-in blocks (a kamado, a wall)
Never starts or stops the server, the game or any GUI program.
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
REN = os.path.join(HERE, "renders")
JOBS = os.environ.get("F1_JOBS", "")
LODRES = {"geo": 1e13, "view": 6e15, "fire": 7e15, "road": 3e15}


def blender_main():
    import bpy
    from mathutils import Vector
    src = open(os.path.join(KIT, "render_parts.py"), encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    g = {"__name__": "rp", "__file__": os.path.join(KIT, "render_parts.py")}
    sys.path.insert(0, KIT)
    exec(compile(src, "render_parts.py", "exec"), g)
    from jpparts import mlod
    jobs = json.load(open(JOBS, encoding="utf-8"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam = g["setup"]((1200, 900))
    ground = g["plain"]("ground", (0.30, 0.29, 0.26))
    mats = {}

    def mat_for(tex):
        if tex in mats:
            return mats[tex]
        m = bpy.data.materials.new(os.path.basename(tex))
        m.use_nodes = True
        nt = m.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        iron = "metal" in tex
        glossy = "ceramic" in tex or "lacquer" in tex
        bsdf.inputs["Roughness"].default_value = 0.5 if iron else (0.35 if glossy else 0.88)
        bsdf.inputs["Metallic"].default_value = 0.45 if iron else 0.0
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
                bsdf.inputs["Specular IOR Level"].default_value = 0.1
                try:
                    m.surface_render_method = "DITHERED"
                except Exception:
                    m.blend_method = "CLIP"
        else:
            bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        mats[tex] = m
        return m

    def tint_mat(name, rgb):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        b.inputs["Base Color"].default_value = rgb + (1,)
        b.inputs["Alpha"].default_value = 0.40
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            m.blend_method = "BLEND"
        return m

    tints = {"red": tint_mat("geo", (0.9, 0.05, 0.03)), "green": tint_mat("road", (0.05, 0.85, 0.1))}

    def tf(p, off, yaw):
        a = math.radians(yaw)
        x = p[0] * math.cos(a) + p[2] * math.sin(a)
        z = -p[0] * math.sin(a) + p[2] * math.cos(a)
        return (x + off[0], p[1] + off[1], z + off[2])

    def lod_mesh(lod, name, off=(0.0, 0.0, 0.0), yaw=0.0, solid_mat=None):
        verts, polys, uvs, mids, ml, lnor = [], [], [], [], [], []
        for fi, (fv, fl, tex, mat) in enumerate(lod.faces):
            pts = [tf(lod.points[v[0]], off, yaw) for v in fv]
            bp = [(p[0], p[2], p[1]) for p in pts]
            inward = lod.normals[fv[0][1]] if lod.normals else (0.0, -1.0, 0.0)
            iw = tf(inward, (0.0, 0.0, 0.0), yaw)
            want = (-iw[0], -iw[2], -iw[1])
            nx = ny = nz = 0.0
            for i in range(len(bp)):
                x0, y0, z0 = bp[i]
                x1, y1, z1 = bp[(i + 1) % len(bp)]
                nx += (y0 - y1) * (z0 + z1)
                ny += (z0 - z1) * (x0 + x1)
                nz += (x0 - x1) * (y0 + y1)
            order = list(range(len(bp)))
            if solid_mat is None and nx * want[0] + ny * want[1] + nz * want[2] < 0:
                order = order[::-1]
            base = len(verts)
            verts += [bp[i] for i in order]
            polys.append(list(range(base, base + len(bp))))
            uvs += [(fv[i][2], 1.0 - fv[i][3]) for i in order]
            for i in order:
                nn = tf(lod.normals[fv[i][1]], (0.0, 0.0, 0.0), yaw) if lod.normals else (0.0, 1.0, 0.0)
                lnor.append((-nn[0], -nn[2], -nn[1]))
            key = solid_mat or tex
            if key not in ml:
                ml.append(key)
            mids.append(ml.index(key))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], polys)
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index]
        for k in ml:
            me.materials.append(k if not isinstance(k, str) else mat_for(k))
        for i, mi in enumerate(mids):
            me.polygons[i].material_index = mi
        me.update()
        if lnor and solid_mat is None:
            try:
                me.shade_smooth()
            except Exception:
                for poly in me.polygons:
                    poly.use_smooth = True
            try:
                me.normals_split_custom_set([lnor[l.vertex_index] for l in me.loops])
            except Exception as e:
                print("custom normals failed", e)
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    def block(b, name):
        x0, x1, y0, y1, z0, z1, rgb = b
        me = bpy.data.meshes.new(name)
        v = [(x, z, y) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
        # indices: x*4 + y*2 + z ; faces wound so normals point out after the (x, z, y) swap
        f = [ff[::-1] for ff in ([0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3])]
        me.from_pydata(v, [], f)
        me.update()
        me.materials.append(g["plain"](name + "c", tuple(rgb)))
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    os.makedirs(REN, exist_ok=True)

    def shoot(job, lo, hi):
        lens = job.get("lens", 50)
        if job.get("cam"):
            c = job["cam"]
            t = job["look"]
            loc = Vector((c[0], c[2], c[1]))
            tgt = Vector((t[0], t[2], t[1]))
            q = (tgt - loc).to_track_quat("-Z", "Y")
        else:
            view = job.get("view", (0.45, 1.0, 0.6))
            cc = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
            v = Vector((view[0], view[1], view[2])).normalized()
            q = (-v).to_track_quat("-Z", "Y")
            rx = q @ Vector((1, 0, 0))
            uy = q @ Vector((0, 1, 0))
            th = 18.0 / lens * 0.92
            tv = th * 3 / 4
            corners = [Vector((a, b, e)) for a in (lo[0], hi[0]) for b in (lo[1], hi[1]) for e in (lo[2], hi[2])]
            d = 0.3
            for _ in range(80):
                ok = True
                for k in corners:
                    w = k - (cc + v * d)
                    depth = w.dot(-v)
                    if depth <= 0.05 or abs(w.dot(rx)) / depth > th or abs(w.dot(uy)) / depth > tv:
                        ok = False
                        break
                if ok:
                    break
                d *= 1.08
            loc = cc + v * d * job.get("tight", 1.0)
        cam.location = loc
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = q
        cam.data.type = "PERSP"
        cam.data.lens = lens
        cam.data.clip_start = 0.01
        cam.data.clip_end = 200
        bpy.context.scene.render.filepath = os.path.join(REN, job["out"] + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", job["out"])

    for job in jobs:
        g["clear_objects"]()
        lo, hi = [1e9] * 3, [-1e9] * 3
        for k, item in enumerate(job["items"]):
            lods = mlod.read_mlod(item["p3d"])
            want = item.get("lod", 1.0)
            want = LODRES.get(want, want)
            cand = [l for l in lods if abs(l.resolution - want) <= max(1e-3, want * 1e-6)]
            if not cand:
                print("no LOD", want, "in", item["p3d"])
                continue
            lod = cand[0]
            off = item.get("off", [0.0, 0.0, 0.0])
            if len(off) == 2:
                off = [off[0], 0.0, off[1]]
            yaw = item.get("yaw", 0.0)
            tint = item.get("tint")
            lod_mesh(lod, "m%d" % k, off, yaw, solid_mat=tints[tint] if tint else None)
            if not tint:
                for p in lod.points:
                    q = tf(p, off, yaw)
                    q = (q[0], q[2], q[1])
                    lo = [min(a, b) for a, b in zip(lo, q)]
                    hi = [max(a, b) for a, b in zip(hi, q)]
        for k, b in enumerate(job.get("boxes", [])):
            block(b, "blk%d" % k)
        if not job.get("noground"):
            bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, job.get("ground_y", 0.0) - 0.001))
            bpy.context.active_object.data.materials.append(ground)
        for m in bpy.data.materials:
            m.use_backface_culling = bool(job.get("cull", True))
        hi[2] = max(hi[2], lo[2] + 0.3)
        shoot(job, lo, hi)


def run(jobs, path=None):
    path = path or os.path.join(HERE, "_build", "jobs.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(json.dumps(jobs, indent=1).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__)],
                       capture_output=True, text=True, errors="replace", env=dict(os.environ, F1_JOBS=path))
    with open(os.path.join(HERE, "_build", "render.log"), "wb") as fh:
        fh.write((r.stdout + "\n" + r.stderr).replace("\r\n", "\n").encode("utf-8"))
    n = sum(1 for l in r.stdout.splitlines() if l.startswith("rendered"))
    print("blender exit", r.returncode, "; rendered:", n)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:])
    return n


if __name__ == "__main__":
    if "bpy" in sys.modules or any(a.lower().endswith("blender.exe") for a in sys.argv[:1]):
        blender_main()
    else:
        run(json.load(open(sys.argv[1], encoding="utf-8")), os.path.abspath(sys.argv[1]))
