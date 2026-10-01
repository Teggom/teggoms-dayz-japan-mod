"""FP2 render tool: close-up renders FROM THE WRITTEN MLOD MASTERS, drawn the way the game draws them (back faces
culled, alpha-tested _ca textures), for the before / after sheet.

  python spikes/FP2/render_fp2.py before <group> [...]   copy the current masters of the group's shots to
                                                        spikes/FP2/before/ (first copy kept) and render them
  python spikes/FP2/render_fp2.py after <group> [...]    render the current masters
  python spikes/FP2/render_fp2.py look <group> [...]     like after, written as look_<shot>.png (work renders)
  python spikes/FP2/render_fp2.py head <group> [...]     'before' renders from HEAD masters rebuilt in a scratch copy
Shots live in spikes/FP2/shots.py (SHOTS[group] = [(shot, [master p3d, ...], view, tight, lod, offsets)]).
Renders -> spikes/FP2/renders/<mode>_<shot>.png. Blender runs --background (no GUI).
"""
import importlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
KIT = os.path.join(DEV, "parts", "kit")
TEXPNG = os.path.join(DEV, "data", "materials", "textures")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
REN = os.path.join(HERE, "renders")
BEFORE = os.path.join(HERE, "before")
JOBS = os.path.join(HERE, "_build", "render_jobs.json")
# 'head' mode: masters rebuilt from `git archive HEAD` in the session scratchpad (the masters are not in git)
HEADCOPY = os.environ.get("FP2_HEAD", os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp", "claude",
                                                   "D--DayZ-Server-AI-20260907-MultiMap",
                                                   "a9f726c9-9127-4763-904a-88b248cb50f6", "scratchpad", "head"))


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
        m.use_backface_culling = True                      # the game draws single-sided faces
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
                try:
                    m.surface_render_method = "DITHERED"
                except Exception:
                    m.blend_method = "CLIP"
        else:
            bsdf.inputs["Base Color"].default_value = (1, 0, 1, 1)
        mats[tex] = m
        return m

    def lod_mesh(lod, name, off=(0.0, 0.0)):
        verts, polys, uvs, mids, ml, lnor = [], [], [], [], [], []
        for fi, (fv, fl, tex, mat) in enumerate(lod.faces):
            pts = [lod.points[v[0]] for v in fv]
            bp = [(p[0] + off[0], p[2] + off[1], p[1]) for p in pts]
            inward = lod.normals[fv[0][1]]
            # the MLOD stores the face wound with its formula normal pointing inward; in Blender (x, z, y) the
            # handedness flips, so keep the stored order when its Newell normal agrees with -inward
            want = (-inward[0], -inward[2], -inward[1])
            nx = ny = nz = 0.0
            for i in range(len(bp)):
                x0, y0, z0 = bp[i]
                x1, y1, z1 = bp[(i + 1) % len(bp)]
                nx += (y0 - y1) * (z0 + z1)
                ny += (z0 - z1) * (x0 + x1)
                nz += (x0 - x1) * (y0 + y1)
            order = list(range(len(bp)))
            if nx * want[0] + ny * want[1] + nz * want[2] < 0:
                order = order[::-1]
            base = len(verts)
            verts += [bp[i] for i in order]
            polys.append(list(range(base, base + len(bp))))
            uvs += [(fv[i][2], 1.0 - fv[i][3]) for i in order]
            for i in order:
                nn = lod.normals[fv[i][1]]
                lnor.append((-nn[0], -nn[2], -nn[1]))
            if tex not in ml:
                ml.append(tex)
            mids.append(ml.index(tex))
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], polys)
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index]
        for k in ml:
            me.materials.append(mat_for(k))
        for i, mi in enumerate(mids):
            me.polygons[i].material_index = mi
        me.update()
        try:
            me.shade_smooth()
            me.normals_split_custom_set([lnor[l.vertex_index] for l in me.loops])
        except Exception as e:
            print("custom normals failed", e)
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    os.makedirs(REN, exist_ok=True)

    def shoot(out, lo, hi, view, lens, tight):
        c = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
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
                w = k - (c + v * d)
                depth = w.dot(-v)
                if depth <= 0.05 or abs(w.dot(rx)) / depth > th or abs(w.dot(uy)) / depth > tv:
                    ok = False
                    break
            if ok:
                break
            d *= 1.1
        cam.location = c + v * d * tight
        cam.rotation_mode = "QUATERNION"
        cam.rotation_quaternion = q
        cam.data.type = "PERSP"
        cam.data.lens = lens
        cam.data.clip_start = 0.02
        cam.data.clip_end = 300
        bpy.context.scene.render.filepath = os.path.join(REN, out + ".png")
        bpy.ops.render.render(write_still=True)
        print("rendered", out)

    for job in jobs:
        g["clear_objects"]()
        lo, hi = [1e9] * 3, [-1e9] * 3
        for item in job["items"]:
            lods = mlod.read_mlod(item["p3d"])
            lod = next(l for l in lods if abs(l.resolution - item.get("lod", 1.0)) < 1e-3)
            ox, oz = item["off"]
            lod_mesh(lod, "m", (ox, oz))
            for p in lod.points:
                q = (p[0] + ox, p[2] + oz, p[1])
                lo = [min(a, b) for a, b in zip(lo, q)]
                hi = [max(a, b) for a, b in zip(hi, q)]
        if job.get("ground", True):
            bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, min(lo[2], 0.0) - 0.002))
            bpy.context.active_object.data.materials.append(ground)
        hi[2] = max(hi[2], lo[2] + 0.2)
        shoot(job["out"], lo, hi, tuple(job["view"]), job.get("lens", 50), job.get("tight", 1.0))


def main(argv):
    mode, groups = argv[0], argv[1:]
    sys.path.insert(0, HERE)
    shots = importlib.import_module("shots").SHOTS
    jobs = []
    for gname in groups:
        for shot in shots[gname]:
            name, p3ds, view, tight, lod = shot[:5]
            offs = shot[5] if len(shot) > 5 else [(0.0, 0.0)] * len(p3ds)
            items = []
            for p, off in zip(p3ds, offs):
                src = os.path.join(DEV, p)
                if mode == "head":                   # the HEAD masters rebuilt in the scratch copy (git archive HEAD)
                    src = os.path.join(HEADCOPY, p)
                elif mode == "before":
                    os.makedirs(BEFORE, exist_ok=True)
                    keep = os.path.join(BEFORE, os.path.basename(p))
                    if not os.path.isfile(keep):
                        shutil.copyfile(src, keep)
                    src = keep
                items.append({"p3d": src, "off": list(off), "lod": lod})
            jobs.append({"out": "%s_%s" % ("before" if mode == "head" else mode, name), "view": view, "tight": tight, "items": items})
    os.makedirs(os.path.dirname(JOBS), exist_ok=True)
    with open(JOBS, "wb") as fh:
        fh.write(json.dumps(jobs, indent=1).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__)],
                       capture_output=True, text=True, errors="replace")
    with open(os.path.join(HERE, "_build", "render_%s.log" % mode), "wb") as fh:
        fh.write((r.stdout + "\n" + r.stderr).replace("\r\n", "\n").encode("utf-8"))
    done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
    print("blender exit", r.returncode, "; rendered:", len(done), "of", len(jobs))
    if r.returncode or len(done) < len(jobs):
        print(r.stderr[-1500:])


if __name__ == "__main__":
    if "bpy" in sys.modules:
        blender_main()
    else:
        main(sys.argv[1:])
