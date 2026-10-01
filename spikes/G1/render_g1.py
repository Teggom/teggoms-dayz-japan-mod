"""G1 close-up renders of the gorinto family (ring seating fix), from the B3b MLOD masters, with B3b's Blender
renderer (spikes/B3b/render.py blender_main, imported read-only; JOBS / REN pointed into spikes/G1).

  python spikes/G1/render_g1.py before    copy the current masters to spikes/G1/before/ and render them
  python spikes/G1/render_g1.py after     render the rebuilt masters in spikes/B3b/out/grave
Renders -> spikes/G1/renders/<mode>_<model>_<view>.png. Blender runs --background (no GUI).
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3B_OUT = os.path.join(DEV, "spikes", "B3b", "out", "grave")
REN = os.path.join(HERE, "renders")
JOBS = os.path.join(HERE, "_build", "render_jobs.json")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
MODELS = ["gorinto_s", "gorinto_l", "gorinto_stack", "ab_gorinto_fallen", "gorinto_heap"]
# (suffix, view (x, front, up) in model terms, tight): side views at ring height (where the gap under the roof showed)
VIEWS = {"gorinto_s": [("side", (1.0, 0.30, 0.03), 0.85), ("front", (0.30, 1.0, 0.10), 0.85)],
         "gorinto_l": [("side", (1.0, 0.30, 0.03), 0.80)],
         "gorinto_stack": [("side", (1.0, 0.30, 0.03), 0.85), ("front", (0.30, 1.0, 0.10), 0.85)],
         "ab_gorinto_fallen": [("low", (0.35, 1.0, 0.25), 0.85)],
         "gorinto_heap": [("low", (0.35, 1.0, 0.25), 0.85)]}


def blender_side():
    sp = importlib.util.spec_from_file_location("b3b_render", os.path.join(DEV, "spikes", "B3b", "render.py"))
    r = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(r)
    r.JOBS = JOBS
    r.REN = REN
    r.blender_main()


def main(mode):
    src = B3B_OUT
    if mode == "before":
        src = os.path.join(HERE, "before")
        os.makedirs(src, exist_ok=True)
        for m in MODELS:
            if os.path.isfile(os.path.join(src, "jp_s_grave_stones_%s.p3d" % m)):
                continue                       # keep the first (pre-fix) copy
            shutil.copyfile(os.path.join(B3B_OUT, "jp_s_grave_stones_%s.p3d" % m),
                            os.path.join(src, "jp_s_grave_stones_%s.p3d" % m))
    jobs = []
    for m in MODELS:
        for suf, view, tight in VIEWS[m]:
            jobs.append({"out": "%s_%s_%s" % (mode, m, suf), "view": view, "lens": 50, "tight": tight,
                         "items": [{"p3d": os.path.join(src, "jp_s_grave_stones_%s.p3d" % m), "off": [0.0, 0.0],
                                    "lod": 1.0, "geo": False, "wall": False}]})
    os.makedirs(os.path.dirname(JOBS), exist_ok=True)
    os.makedirs(REN, exist_ok=True)
    with open(JOBS, "wb") as fh:
        fh.write(json.dumps(jobs, indent=1).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__)],
                       capture_output=True, text=True, errors="replace")
    with open(os.path.join(HERE, "_build", "render_%s.log" % mode), "wb") as fh:
        fh.write((r.stdout + "\n" + r.stderr).replace("\r\n", "\n").encode("utf-8"))
    print("blender exit", r.returncode, "; rendered:", sum(1 for l in r.stdout.splitlines() if l.startswith("rendered")))


if __name__ == "__main__":
    if "bpy" in sys.modules:
        blender_side()
    else:
        main(sys.argv[1])
