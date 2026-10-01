#!/usr/bin/env python3
r"""Render sheets for W2P1's shrine / temple parts and offline assemblies (render_b2.py's Blender side and composer).

  python render_w2p1.py <sheet> [job ...] [--compose]

Sheets -> parts/contact_sheets/<sheet>.jpg; PNGs -> parts/_render/<sheet>/. Builds: 'part:<id>' (a registry part),
'x:w2p1_assembly.<fn>' (an offline assembly builder, parts/kit/w2p1_assembly.py). Parts whose grade sits below y 0
are lifted with 'move' so the ground plane meets their grade.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_b2 as RB  # noqa: E402

DEV = RB.DEV
CHECKS = os.path.join(DEV, "parts", "w2p1_assembly_checks.json")


def P(name, cap, view="3q", target=(0.9, 0.6, 0.6), dist=7.0, move=1.0, persp=30, open_=0.0, human=None, **kw):
    v = {"build": "part:" + name, "view": view, "persp": persp, "target": list(target), "dist": dist,
         "move": [0.0, move, 0.0]}
    if open_:
        v["open"] = open_
    if human:
        v["human"] = list(human)
    v.update(kw)
    return (name.replace("jp_p_", ""), cap, v)


SHEETS = {
    "w2p1_koran": ("W2P1 jp_p_porch_koran: en (kirime-en) + kumi-koran, corners, kizahashi, wakishoji", [
        P("jp_p_porch_koran_plain", "1-ken en run, plain kumi-koran: jifuku, struts, hirageta, totsuka + to, round "
          "hokogi; en posts on stones, edge beam; floor +1.00", human=[2.6, 1.6, 0.0]),
        P("jp_p_porch_koran_giboshi", "Giboshi koran: octagonal end post with the onion finial (iron stands in for "
          "bronze)"),
        P("jp_p_porch_koran_corner_plain", "Corner, plain: the runs cross and run out 0.10 past the corner (the "
          "crossing run sits 1.5 cm higher: no shared planes, C20)", target=(0.6, 0.5, 0.6)),
        P("jp_p_porch_koran_corner_giboshi", "Corner with a giboshi corner post", target=(0.6, 0.5, 0.6)),
        P("jp_p_porch_koran_kizahashi", "Kizahashi in the koran gap: 5 risers of 0.20, 36.2 deg hidden walk ramp, "
          "1.10 clear between the stair rails, giboshi posts at the gap and the foot, foot stone",
          target=(0.9, 0.3, 1.8), dist=8.0, human=[2.6, 3.4, 0.0]),
        P("jp_p_porch_koran_kizahashi_plain", "The same stair with plain cut-top posts (village)",
          target=(0.9, 0.3, 1.8), dist=8.0),
        P("jp_p_porch_koran_wakishoji", "Side en run ending in the wakishoji board screen", target=(1.2, 0.9, 0.6)),
    ]),
}


def register(extra):
    SHEETS.update(extra)


def notes():
    if not os.path.isfile(CHECKS):
        return ""
    res = json.load(open(CHECKS, encoding="utf-8"))
    return "Assembly checks (parts/w2p1_assembly_checks.json): " + ", ".join(
        "%s %d/%d" % (nm, sum(1 for c in r["checks"] if c["ok"]), len(r["checks"])) for nm, r in sorted(res.items()))


def main(argv):
    try:
        import w2p1_sheets  # noqa: F401  (more sheet definitions, if present)
    except ImportError:
        pass
    sheet = argv[0]
    title, jobs = SHEETS[sheet]
    only = [a for a in argv[1:] if not a.startswith("--")]
    if "--compose" not in argv:
        todo = [j for j in jobs if not only or j[0] in only]
        jf = os.path.join(RB.RENDER, sheet + "_jobs.json")
        os.makedirs(RB.RENDER, exist_ok=True)
        with open(jf, "wb") as f:
            f.write(json.dumps({"out_dir": os.path.join(RB.RENDER, sheet), "res": list(RB.RES), "jobs": todo},
                               indent=1).encode("utf-8"))
        r = subprocess.run([RB.BLENDER, "--background", "--factory-startup", "--python",
                            os.path.join(HERE, "render_b2.py"), "--", "--blender", jf], capture_output=True, text=True,
                           errors="replace")
        done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
        print("%d/%d rendered" % (len(done), len(todo)))
        if len(done) < len(todo):
            print((r.stdout + r.stderr)[-4000:])
    RB.compose(sheet, title, jobs, notes() if "asm" in sheet else "Part checks: src/JP/parts/<group>/checks.json "
               "(C2 C3 C4 C5 C7 + C20 by spikes/W2P1/ptest.py). Grade = the ground plane; parts lifted onto it.")


if __name__ == "__main__":
    main(sys.argv[1:])
