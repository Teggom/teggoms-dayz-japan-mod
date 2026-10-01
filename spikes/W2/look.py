#!/usr/bin/env python3
r"""look.py - W2 close-up renders through spikes/B3b/render.py's Blender side (same scene, from the MLOD masters).

  python look.py <out> <view x,front,up> <lod> <cat/p3d> [<cat/p3d> ...]   (p3d names without .p3d, under spikes/B3b/out)
  e.g. python look.py tw_close 0.3,1,0.35 1 shrine/jp_s_torii_wood_myojin_rope_shide shrine/jp_s_torii_wood_shinmei
Models are laid side by side (gap 0.4 m). Output: spikes/B3b/renders/<out>.png
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3B = os.path.join(DEV, "spikes", "B3b")
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402

BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"


def main(a):
    out, view, lod = a[0], [float(v) for v in a[1].split(",")], float(a[2])
    items, x = [], 0.0
    geo = "--geo" in a
    names = [n for n in a[3:] if not n.startswith("--")]
    for n in names:
        p = os.path.join(B3B, "out", n.replace("/", os.sep) + ".p3d")
        r = next(l for l in mlod.read_mlod(p) if abs(l.resolution - lod) < 1e-3)
        xs = [q[0] for q in r.points]
        items.append({"p3d": p, "off": [x - max(xs), 0.0], "lod": lod, "geo": geo})
        x -= (max(xs) - min(xs)) + 0.4
    for it in items:
        it["off"][0] -= (x + 0.4) / 2
    jp = os.path.join(B3B, "_build", "render_jobs.json")
    with open(jp, "wb") as f:
        f.write(json.dumps([{"out": out, "items": items, "view": view, "lens": 50}], indent=1).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(B3B, "render.py")],
                       capture_output=True, text=True, errors="replace")
    print("blender exit", r.returncode, os.path.join(B3B, "renders", out + ".png"))


if __name__ == "__main__":
    main(sys.argv[1:])
