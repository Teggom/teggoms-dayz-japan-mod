"""peek.py - quick clay renders of statue meshes (Blender Workbench, studio light) for modelling iterations.

  python peek.py <name> [lod] [--views front,q,side,back] [--zoom y0,y1]   -> renders/peek_<name>.png
  (name = spikes/FX2/meshes/<name>.json)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
REN = os.path.join(HERE, "renders")

BL = r'''
import bpy, json, sys, math
from mathutils import Vector
job = json.load(open(sys.argv[sys.argv.index("--") + 1]))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "SINGLE"
sc.display.shading.single_color = (0.62, 0.55, 0.45)
sc.display.shading.show_cavity = True
sc.display.shading.cavity_type = "BOTH"
sc.render.resolution_x, sc.render.resolution_y = job["res"]
sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("w")
sc.world.color = (0.25, 0.25, 0.27)
me = bpy.data.meshes.new("m")
V = job["v"]; F = job["f"]
me.from_pydata([(v[0], -v[2], v[1]) for v in V], [], F)
me.update()
for p in me.polygons: p.use_smooth = True
ob = bpy.data.objects.new("o", me)
sc.collection.objects.link(ob)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
lo, hi = job["lo"], job["hi"]
c = Vector(((lo[0]+hi[0])/2, -(lo[2]+hi[2])/2, (lo[1]+hi[1])/2))
size = max(hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]) * 1.08
if job.get("zoom"):
    y0, y1 = job["zoom"]; c.z = (y0+y1)/2; size = (y1-y0)*1.1
cam.data.ortho_scale = size
for i, (name, yaw, pitch) in enumerate(job["views"]):
    a = math.radians(yaw); p = math.radians(pitch)
    d = Vector((math.sin(a)*math.cos(p), -math.cos(a)*math.cos(p), math.sin(p))) * 10
    cam.location = c + d
    cam.rotation_euler = (d * -1).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = job["out"] + "_%d.png" % i
    bpy.ops.render.render(write_still=True)
'''

VIEWS = {"front": ("front", 0, 5), "q": ("q", 35, 10), "side": ("side", 90, 5), "back": ("back", 180, 5),
         "q2": ("q2", -35, 10), "top": ("top", 0, 60)}


def main(argv):
    name = argv[0]
    lod = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 0
    views = "front,q,side,back"
    zoom = None
    if "--views" in argv:
        views = argv[argv.index("--views") + 1]
    if "--zoom" in argv:
        zoom = [float(x) for x in argv[argv.index("--zoom") + 1].split(",")]
    d = json.load(open(os.path.join(HERE, "meshes", name + ".json"), encoding="utf-8"))
    V, F = [], []
    for p in d["parts"]:
        L = p["lods"][min(lod, len(p["lods"]) - 1)]
        o = len(V)
        V += L["v"]
        F += [[i + o for i in f] for f in L["f"]]
    xs = [v[0] for v in V]
    ys = [v[1] for v in V]
    zs = [v[2] for v in V]
    os.makedirs(os.path.join(HERE, "_build"), exist_ok=True)
    os.makedirs(REN, exist_ok=True)
    tag = name + ("_l%d" % lod) + ("_z" if zoom else "")
    out = os.path.join(HERE, "_build", "peek_" + tag)
    vs = [VIEWS[v] for v in views.split(",")]
    job = {"v": V, "f": F, "lo": [min(xs), min(ys), min(zs)], "hi": [max(xs), max(ys), max(zs)], "views": vs,
           "res": [520, 640], "out": out, "zoom": zoom}
    jp = out + ".json"
    with open(jp, "wb") as f:
        f.write(json.dumps(job).encode())
    sp = os.path.join(HERE, "_build", "peek_bl.py")
    with open(sp, "wb") as f:
        f.write(BL.encode())
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", sp, "--", jp], capture_output=True,
                       text=True)
    from PIL import Image
    ims = []
    for i in range(len(vs)):
        fp = out + "_%d.png" % i
        if not os.path.isfile(fp):
            print(r.stdout[-2000:], r.stderr[-2000:])
            return 1
        # DayZ model space is left-handed (skit 'text facing'): the game shows the mirror image of this right-handed
        # render, so the render is flipped left-right to show what a player sees
        ims.append(Image.open(fp).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT))
    W = sum(im.width for im in ims)
    S = Image.new("RGB", (W, ims[0].height))
    x = 0
    for im in ims:
        S.paste(im, (x, 0))
        x += im.width
    fp = os.path.join(REN, "peek_%s.png" % tag)
    S.save(fp)
    print(fp, "faces", len(F))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
