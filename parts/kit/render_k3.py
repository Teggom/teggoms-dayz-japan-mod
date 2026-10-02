#!/usr/bin/env python3
r"""Render K3's contact sheets (the wall kit and the covered-corridor / kairo kit), render_b2's Blender side.

  python render_k3.py <sheet> [job ...] [--compose]        sheets: k3_walls, k3_corridors
  python render_k3.py try <build> [view] [dist] [tx ty tz]  one quick look -> spikes/K3/renders/try_<build>.png

A build is "k3:<assembly>" (k3_assembly.ASSEMBLIES), "case:<name>" (k3_assembly.CASES) or "part:<registry name>".
Sheets -> research/production/contact_sheets/<sheet>.jpg; PNGs -> parts/_render/<sheet>/.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_b2 as RB  # noqa: E402

DEV = RB.DEV
OUT_SHEETS = os.path.join(DEV, "research", "production", "contact_sheets")
TRY = os.path.join(DEV, "spikes", "K3", "renders")


def get_part(spec):
    kind, what = spec.split(":", 1)
    if kind in ("k3", "case"):
        import k3_assembly
        if kind == "k3":
            a, _ = k3_assembly.ASSEMBLIES[what]()
            return a
        return k3_assembly.CASES[what]()
    return RB._orig_get_part(spec)




def run_jobs(out_dir, jobs):
    jf = os.path.join(RB.RENDER, "k3_%d_jobs.json" % os.getpid())
    os.makedirs(RB.RENDER, exist_ok=True)
    with open(jf, "wb") as f:
        f.write(json.dumps({"out_dir": out_dir, "res": list(RB.RES), "jobs": jobs}, indent=1).encode("utf-8"))
    r = subprocess.run([RB.BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__), "--",
                        "--blender", jf], capture_output=True, text=True, errors="replace")
    done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
    print("%d/%d rendered" % (len(done), len(jobs)))
    if len(done) < len(jobs):
        print((r.stdout + r.stderr)[-4000:])
    os.remove(jf)


def main(argv):
    if argv[0] == "try":
        build = argv[1]
        view = argv[2] if len(argv) > 2 else "3q"
        dist = float(argv[3]) if len(argv) > 3 else 14.0
        tgt = [float(v) for v in argv[4:7]] if len(argv) > 6 else [0.0, 1.5, 0.0]
        name = "try_" + build.replace(":", "_")
        v = {"build": build, "view": view, "persp": 30, "target": tgt, "dist": dist}
        if view == "top":
            v = {"build": build, "view": "top", "target": tgt, "scale": dist}
        if view == "inside":
            v = {"build": build, "interior": {"cam": tgt, "look": [float(x) for x in argv[7:10]], "lens": 20}}
        run_jobs(TRY, [(name, "", v)])
        print(os.path.join(TRY, name + ".png"))
        return 0
    sheet = argv[0]
    import k3_sheets
    title, jobs, notes = k3_sheets.sheets()[sheet]
    note = k3_sheets._note(notes)
    if sheet == "k3_corridors":
        import json as _j
        res = _j.load(open(os.path.join(DEV, "parts", "k3_assembly_checks.json"), encoding="utf-8"))
        km = [c["detail"] for c in res.get("k3_corridor_court", {}).get("checks", []) if c["check"].startswith("KW7")]
        jobs = [(o, c.replace("(margin %s)", "(%s)" % (km[0] if km else "")), v) for o, c, v in jobs]
    only = [a for a in argv[1:] if not a.startswith("--")]
    if "--compose" not in argv:
        todo = [j for j in jobs if not only or j[0] in only]
        run_jobs(os.path.join(RB.RENDER, sheet), todo)
    dst = RB.compose(sheet, title, jobs, note)
    os.makedirs(OUT_SHEETS, exist_ok=True)
    shutil.move(dst, os.path.join(OUT_SHEETS, sheet + ".jpg"))
    print("sheet ->", os.path.join(OUT_SHEETS, sheet + ".jpg"))
    return 0


RB._orig_get_part = RB.get_part
RB.get_part = get_part

if __name__ == "__main__":
    if "--blender" in sys.argv:
        RB.blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        sys.exit(main(sys.argv[1:]))
