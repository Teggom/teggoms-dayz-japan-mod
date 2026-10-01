"""M2 close-up renders of the gorinto / hokyointo, from the B3b MLOD masters, with B3b's Blender renderer
(spikes/B3b/render.py blender_main, imported read-only; its JOBS / REN paths are pointed into spikes/M2).

  python spikes/M2/render_m2.py before    copy the current masters to spikes/M2/before/ and render them (before_*.png)
  python spikes/M2/render_m2.py after     render the rebuilt masters in spikes/B3b/out/grave (after_*.png)
Renders -> spikes/M2/renders/. Blender runs --background (no GUI).
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
MODELS = ["gorinto_s", "gorinto_l", "gorinto_stack", "ab_gorinto_fallen", "hokyointo", "ab_hokyointo_broken"]
# (suffix, view (x, front, up) in model terms, tight): front views; the hokyointo also from its left (+x, south: TRAH)
# and the back (west: HRIH)
VIEWS = {"gorinto_s": [("front", (0.12, 1.0, 0.22), 1.0)],
         "gorinto_l": [("front", (0.12, 1.0, 0.18), 1.0), ("rings", (0.12, 1.0, 0.10), 0.45)],
         "gorinto_stack": [("front", (0.12, 1.0, 0.22), 1.0)],
         "ab_gorinto_fallen": [("front", (0.15, 1.0, 0.35), 1.0)],
         "hokyointo": [("front", (0.15, 1.0, 0.20), 1.0), ("left", (1.0, 0.25, 0.20), 1.0),
                       ("back", (-0.15, -1.0, 0.20), 1.0)],
         "ab_hokyointo_broken": [("front", (0.15, 1.0, 0.25), 1.0)]}


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
