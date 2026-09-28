#!/usr/bin/env python3
r"""Contact sheets for gate G2: one sheet per family, every part variant at ONE scale per sheet, a 1.8 m figure,
the id, a one-line "used for" and its check result.

  python render_sheets.py [sheet ...] [--no-render]

Renders (Blender, background) -> parts/_render/<sheet>/<name>.png; sheets -> parts/contact_sheets/<sheet>.jpg.
"""
import json
import os
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, registry  # noqa: E402

DEV = core.DEV
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
RENDER = os.path.join(DEV, "parts", "_render")
SHEETS = os.path.join(DEV, "parts", "contact_sheets")
FONT, FONTB = r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf"
CELL = (480, 400)

# sheet -> (title, scale m, filter(part id) -> bool, view)
KAWARA_PARTS = ("jp_p_roof_sangawara", "jp_p_roof_kawara_ridge", "jp_p_roof_onigawara", "jp_p_roof_hongawara")
SHEET_DEFS = [
    ("1_frame", "Frame: posts, beams, dashigeta (G1 d4: flagged deviation)", 6.5,
     lambda p: p.startswith("jp_p_frame_"), "3q"),
    ("2a_walls", "Walls: recipes (1-ken samples), wainscot, shitami, namako", 5.5,
     lambda p: p.startswith("jp_p_wall_") and not p.startswith(("jp_p_wall_gable", "jp_p_wall_udatsu")), "3q"),
    ("2b_gables", "Gable ends (3-ken span, from the eave line up) and udatsu", 9.0,
     lambda p: p.startswith(("jp_p_wall_gable", "jp_p_wall_udatsu")), "3q"),
    ("3_openings", "Openings: sliding doors (shown 60 % open), windows, lattices, shop closures", 7.5,
     lambda p: p.startswith("jp_p_open_") and not p.endswith("_twin"), "3q"),
    ("3b_openings_twin", "Openings: twin-leaf sliding doors (added by architect C, 2026-09-27), 60 % open", 7.5,
     lambda p: p.startswith("jp_p_open_") and p.endswith("_twin"), "3q"),
    ("4_foundations", "Foundations, sills, steps, verandas", 6.0,
     lambda p: p.startswith("jp_p_found_") or p.startswith("jp_p_porch_"), "3q"),
    ("5a_roof_kawara", "Kawara as geometry: field, eave, verge, ridges, onigawara, hongawara", 3.6,
     lambda p: p.startswith(KAWARA_PARTS), "3q"),
    ("5b_roof_parts", "Board and thatch roof parts, eaves, pents, vents, bargeboards, gutter", 8.0,
     lambda p: p.startswith("jp_p_roof_") and not p.startswith(KAWARA_PARTS + ("jp_p_roof_forms",
                                                                               "jp_p_roof_thatch_body")), "3q"),
    ("6_roof_forms", "Roof forms and thatch bodies from the generator (whole roofs, 4 x 3 ken)", 15.0,
     lambda p: p.startswith(("jp_p_roof_forms", "jp_p_roof_thatch_body")), "3q"),
    ("7_trim", "Trim: W1 grime decal band (jp_m_wall_grime), shown on its context wall / post", 3.0,
     lambda p: p.startswith("jp_p_trim_"), "3q"),
]
OVERRIDES = {}      # name -> dict of job overrides (set by family modules via registry.RENDER_HINTS)


def jobs_for(sheet):
    key, title, scale, filt, view = sheet
    out = []
    for pid, var, fn in registry.ALL:
        name = pid + var
        if not filt(name):
            continue
        part = fn(var)
        ctx = []
        for c in part.connectors:
            if c["type"] == "post" and not c.get("hidden") and (part.group in ("wall", "open") or (
                    part.group == "frame" and part.pid != "jp_p_frame_post")):
                ctx.append(["jp_p_frame_post_planed", 0.0, [c["pos"][0], c["pos"][1], c["pos"][2]]])
        job = {"name": name, "scale": scale, "view": view, "context": ctx}
        if key in ("5a_roof_kawara", "5b_roof_parts"):
            job["drop"] = True
        g = [c["pos"][1] for c in part.connectors if c["type"] == "grade"]
        if g:
            job["ground_y"] = g[0] - 0.002
            job["human_y"] = g[0]
        if part.doors and any(a["type"] == "translation" for d in part.doors for a in d.anims):
            job["open"] = 0.6
        job.update(getattr(registry, "RENDER_HINTS", {}).get(name, {}))
        out.append(job)
    return out


def run_blender(sheet, jobs):
    d = os.path.join(RENDER, sheet)
    jf = os.path.join(RENDER, sheet + "_jobs.json")
    os.makedirs(RENDER, exist_ok=True)
    with open(jf, "wb") as f:
        f.write(json.dumps({"out_dir": d, "res": list(CELL), "jobs": jobs}, indent=1).encode("utf-8"))
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_parts.py"),
                        "--", jf], capture_output=True, text=True, errors="replace")
    done = sum(os.path.isfile(os.path.join(d, j.get("out", j["name"]) + ".png")) for j in jobs)
    print("%s: %d/%d rendered" % (sheet, done, len(jobs)))
    if done < len(jobs):
        print((r.stdout + r.stderr)[-3000:])


def load_checks():
    res = {}
    base = os.path.join(DEV, "src", "JP", "parts")
    for g in os.listdir(base) if os.path.isdir(base) else []:
        f = os.path.join(base, g, "checks.json")
        if os.path.isfile(f):
            for p in json.load(open(f, encoding="utf-8"))["parts"]:
                res[p["id"]] = p["checks"]
    return res


def compose(sheet, jobs, extra_note="", captions_top=None):
    key, title, scale, _, _ = sheet
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (FONTB, 30), "s": (FONT, 15), "b": (FONTB, 15),
                                                          "t": (FONT, 14)}.items()}
    chk = load_checks()
    cols = 4
    cap = 78
    rows = (len(jobs) + cols - 1) // cols
    W = cols * CELL[0] + (cols + 1) * 10
    H = 96 + rows * (CELL[1] + cap + 10) + 10
    im = Image.new("RGB", (W, H), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((14, 12), "JP parts - " + title, font=F["h1"], fill=(20, 20, 20))
    if captions_top:
        yy = 52
        for line in textwrap.wrap(" ".join(captions_top), 250)[:2]:
            d.text((14, yy), line, font=F["s"], fill=(60, 60, 60))
            yy += 20
    else:
        d.text((14, 52), "Same scale for every cell on this sheet: %.1f m across a cell; the dark figure is 1.8 m. "
                         "Resolution-1 LOD, library textures at the part's wear. Grey-tinted posts are context "
                         "(jp_p_frame_post). %s" % (scale, extra_note), font=F["s"], fill=(60, 60, 60))
    if not captions_top:
        d.text((14, 72), "Checks = C2 library paths, C3 grid, C4 dimensions, C5 LODs, C7 convex/closed components, doors "
                     "(sweep, >= 1.00 m clear, 2.00 m head), Roadway on Geometry.", font=F["s"], fill=(60, 60, 60))
    for i, j in enumerate(jobs):
        x = 10 + (i % cols) * (CELL[0] + 10)
        y = 96 + (i // cols) * (CELL[1] + cap + 10)
        p = os.path.join(RENDER, key, j.get("out", j["name"]) + ".png")
        if os.path.isfile(p):
            im.paste(Image.open(p).convert("RGB").resize(CELL), (x, y))
        name = j.get("out", j["name"])
        cs = chk.get(name, [])
        nok = sum(1 for c in cs if c["ok"])
        col = (20, 110, 40) if cs and nok == len(cs) else (170, 30, 30)
        d.rectangle([x, y + CELL[1], x + CELL[0], y + CELL[1] + cap], fill=(250, 249, 246))
        d.text((x + 6, y + CELL[1] + 4), name, font=F["b"], fill=(20, 20, 20))
        if cs:
            d.text((x + CELL[0] - 110, y + CELL[1] + 4), "checks %d/%d" % (nok, len(cs)), font=F["b"], fill=col)
        used = j.get("caption") or ""
        yy = y + CELL[1] + 24
        for line in textwrap.wrap(used, 62)[:3]:
            d.text((x + 6, yy), line, font=F["t"], fill=(50, 50, 50))
            yy += 17
    os.makedirs(SHEETS, exist_ok=True)
    out = os.path.join(SHEETS, key + ".jpg")
    im.save(out, quality=88)
    print("sheet", out, im.size)
    return out


ASSEMBLY_JOBS = [
    {"out": "asm_all", "scale": 26.0, "view": "3q", "target": [11.5, 1.8, -1.0], "no_human": False,
     "human_at": [1.2, 2.2], "caption": "The whole test assembly: the 2 x 2 ken frame (sangawara kirizuma) and one roof "
     "corner per other family on its own post frame: ishioki, kokera, thatch (hip)."},
    {"out": "asm_front", "scale": 8.0, "view": "3q", "target": [1.82, 1.9, -1.0], "open": 0.6, "human_at": [4.3, 1.2],
     "caption": "Front: itado leaf 60 % open, parking over bay 2 (plain shinkabe + grime band); dodai on dressed stones; "
     "cut step hiding the ramp; keta, tile gable, kawara roof on the eave line."},
    {"out": "asm_left", "scale": 8.0, "view": "3q_left", "target": [0.5, 1.9, -1.8], "human_at": [-1.0, 1.2],
     "caption": "Left gable wall: koshi lattice over a 0.39 wainscot in bay 1, battened boards in bay 2, tile gable "
     "(board band, plastered purlin bosses) under the verge tiles and bargeboard."},
    {"out": "asm_back", "scale": 8.0, "view": "back", "target": [1.8, 1.9, -3.2], "human_at": [-0.8, -4.4],
     "caption": "Back: wood renji window in a half-ken bay (extra post on the 0.91 node); right: arakabe with a 0.90 "
     "koshi-ita."},
    {"out": "asm_pavilions", "scale": 15.0, "view": "3q", "target": [13.8, 1.8, -0.9], "human_at": [8.2, 1.0],
     "caption": "Roof corners: ishioki (boards, battens, stones), kokera shingle, thatch hip (0.60 cut eave, hip roll, "
     "bamboo ridge) on adzed 0.15 posts and soseki stones."},
    {"out": "asm_door_open_front", "scale": 5.0, "view": "front", "target": [1.6, 1.2, 0.5], "open": 1.0,
     "human_at": [0.9, 0.9], "human_y": -0.27, "caption": "Front, door fully open: the 1.74 m leaf has parked over bay 2; "
     "the doorway is clear post face to post face (1.70 m; the check measures 1.68 m on 1 cm steps), head 2.00."},
]


def assembly_sheet(render=True):
    key = "8_test_assembly"
    jobs = []
    for j in ASSEMBLY_JOBS:
        jj = dict(j, name="jp_p_test_assembly", assembly=True)
        jobs.append(jj)
    if render:
        run_blender(key, jobs)
    res = json.load(open(os.path.join(DEV, "data", "parts_test", "assembly_checks.json"), encoding="utf-8"))
    note = "Checks on the assembled MLOD: " + "; ".join("%s %s" % ("OK" if c["ok"] else "FAIL", c["check"])
                                                        for c in res["checks"])
    compose((key, "Test assembly (connector proof, not an island building)", 0.0, None, None), jobs,
            extra_note="", captions_top=[note])


def main(argv):
    want = [a for a in argv if not a.startswith("--")]
    if "8_test_assembly" in want or not want:
        assembly_sheet("--no-render" not in argv)
    for sheet in SHEET_DEFS:
        if want and sheet[0] not in want:
            continue
        jobs = jobs_for(sheet)
        if not jobs:
            continue
        for j in jobs:
            p, v, fn = next(r for r in registry.ALL if r[0] + r[1] == j["name"])
            part = fn(v)
            j["caption"] = (part.meta.get("used_for") or "") + (
                "  [DEVIATION: %s]" % part.meta["deviation"] if part.meta.get("deviation") else "")
        if "--no-render" not in argv:
            run_blender(sheet[0], jobs)
        compose(sheet, jobs)


if __name__ == "__main__":
    main(sys.argv[1:])
