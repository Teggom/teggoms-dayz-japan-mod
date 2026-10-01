#!/usr/bin/env python3
r"""Render sheets for W2P2's curved roofs, bracket sets and offline assemblies (render_b2's Blender side, own jobs).

  python render_w2p2.py <sheet> [job ...] [--compose]

A job's "build" is "w2:<assembly>" (w2p2_assembly.ASSEMBLIES), "part:<registry name>", or "case:<name>"
(CASES below: single generator runs). Sheets -> parts/contact_sheets/<sheet>.jpg; PNGs -> parts/_render/<sheet>/.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_b2 as RB  # noqa: E402

KEN = 1.82


def _case(name):
    from jpparts import sori
    from jpparts.core import Part
    p = Part("case_" + name, "", "roof")
    if name.startswith("roof_"):
        _, form, cov = name.split("_", 2)
        W, D = (3 * KEN, 2 * KEN) if form != "yosemune" else (2 * KEN, 2 * KEN)
        if form == "nagare":
            sori.nagare_curved(p, 2 * KEN, 2 * KEN, covering=cov, bear_y=3.0)
        else:
            sori.roof(p, W, D, form=form, covering=cov, bear_y=3.2)
        return p
    if name.startswith("kumi_"):
        from jpparts import kumimono
        return kumimono.sample(name[5:])
    raise KeyError(name)


def get_part(spec):
    kind, what = spec.split(":", 1)
    if kind == "w2":
        import w2p2_assembly
        a, _ = w2p2_assembly.ASSEMBLIES[what]()
        return a
    if kind == "case":
        return _case(what)
    return RB._orig_get_part(spec)


SHEETS_DEF = {
    "w2p2_1_sori": (
        "W2P2 jp_p_roof_sori: curved roofs (sori profile, corner sweep, two-tier rafters) in four coverings", [
            ("iri_hon", "Irimoya, hongawara: concave slopes (rate 0.42 at the eave -> 0.80 at the ridge), corners swept "
             "up 0.30 m, 7-course ridge with onigawara, curved corner ridges with small oni, descending ridges, hafu "
             "+ gegyo, boarded gable face, tsutsumi at the gable foot.",
             {"build": "case:roof_irimoya_hongawara", "view": "3q", "persp": 30, "target": [2.73, 4.2, -1.82],
              "dist": 17}),
            ("iri_hon_under", "The same from below: flying rafters (hiendaruki) on the kioi beam over the base rafters "
             "(jidaruki), kayaoi along the swept eave, two-tier sumigi at the corner, soffit boards.",
             {"build": "case:roof_irimoya_hongawara", "view": "under", "persp": 30, "target": [0.6, 3.4, 0.4],
              "dist": 7}),
            ("iri_kok", "Irimoya, thick kokera: the curved shingle field and the thick layered eave edge (koba, "
             "three bands each stepping out), box ridge.",
             {"build": "case:roof_irimoya_kokera", "view": "3q", "persp": 30, "target": [2.73, 4.2, -1.82],
              "dist": 17}),
            ("kiri_hiw", "Kirizuma, hiwada (cypress bark; stand-in material until roof_hiwada exists): curved hafu "
             "sweeping up at the eave ends, gegyo at the apex, verge soffit.",
             {"build": "case:roof_kirizuma_hiwada", "view": "3q", "persp": 30, "target": [2.73, 4.0, -1.82],
              "dist": 15}),
            ("yose_cu", "Yosemune on a square plan = hogyo (pyramid), copper (stand-in material until roof_copper "
             "exists): seam ribs, apex block for a hoju finial.",
             {"build": "case:roof_yosemune_copper", "view": "3q", "persp": 30, "target": [1.82, 4.0, -1.82],
              "dist": 13}),
            ("nagare_hiw", "Curved nagare (the W2P1 hook, sori.nagare_curved): the front slope runs 1 ken further "
             "out over the steps from the same ridge; its eave falls lower.",
             {"build": "case:roof_nagare_hiwada", "view": "side", "persp": 30, "target": [1.82, 3.6, -0.6],
              "dist": 14}),
        ]),
    "w2p2_2_kumimono": (
        "W2P2 jp_p_frame_kumimono: bracket sets (tokyo) sized from the column (c = 0.30 m), with the head tie, "
        "kaerumata and the step-line beams", [
            ("funa", "funa-hijiki: the boat-shaped arm on the column top carries the keta (village grade, honden).",
             {"build": "case:kumi_funa", "view": "3q", "persp": 30, "target": [1.36, 3.2, 0.2], "dist": 6}),
            ("mitsudo", "hira-mitsudo: daito + wall arm + three makito; kaerumata (frog-leg strut) mid bay.",
             {"build": "case:kumi_mitsudo", "view": "3q", "persp": 30, "target": [1.36, 3.4, 0.2], "dist": 6}),
            ("degumi", "degumi (one step): the projecting arm carries the gangyo 1.05 c out; the wall-line keta is "
             "packed up to meet the rafters (they rise from the gangyo).",
             {"build": "case:kumi_degumi", "view": "3q", "persp": 30, "target": [1.36, 3.5, 0.3], "dist": 6.5}),
            ("mitesaki", "mitesaki (three steps): odaruki tail rafter at 25 deg on the step-2 block, step-3 block "
             "and arm on its nose, gangyo 3.15 c (0.95 m) out.",
             {"build": "case:kumi_mitesaki", "view": "3q_low", "persp": 30, "target": [1.36, 3.9, 0.6], "dist": 7}),
            ("mitesaki_corner", "mitesaki corner set: both sides' projecting members, the diagonal arms and the "
             "corner odaruki; gangyo crossing at the corner (the sumigi bears here).",
             {"build": "case:kumi_mitesaki_corner", "view": "under", "persp": 30, "target": [0.2, 3.9, 0.2],
              "dist": 7}),
            ("kaerumata", "kaerumata on the head tie (and kentozuka, the plainer support, in the parts list).",
             {"build": "case:kumi_kaerumata", "view": "front", "persp": 30, "target": [1.1, 3.3, 0.0], "dist": 3}),
        ]),
    "w2p2_3_assemblies": (
        "W2P2 offline proofs: curved roof + bracket sets assembled (parts/kit/w2p2_assembly.py; not island buildings)", [
            ("hall", "Town-grade worship hall 3 x 2 bays (2.275 m): degumi sets + kaerumata, curved irimoya hongawara, "
             "board walls, open front, on a cut-stone platform. 8,174 / 2,675 / 1,131 faces.",
             {"build": "w2:hall", "view": "3q", "persp": 30, "target": [3.4, 3.2, -2.3], "dist": 21}),
            ("hall_eave", "Its eave from below: gangyo on the degumi sets, base rafters on the gangyo, kioi, flying "
             "rafters, kayaoi along the swept eave, sumigi at the corner, kaerumata on the head tie.",
             {"build": "w2:hall", "interior": {"cam": [-3.2, 1.7, 3.6], "look": [0.2, 3.7, -0.3], "lens": 22}}),
            ("hall_kokera", "The same hall as a shrine haiden: hira-mitsudo sets, kentozuka, curved irimoya thick "
             "kokera with the layered koba edge. 5,564 / 1,822 / 808.",
             {"build": "w2:hall_kokera", "view": "3q", "persp": 30, "target": [3.4, 3.2, -2.3], "dist": 21}),
            ("hondo", "Town temple main hall 3 x 3 bays: MITESAKI sets with odaruki tail rafters, gangyo 0.85 m out, "
             "eaves 2.15 m, curved irimoya hongawara. 11,259 / 3,023 / 1,183 (large: 12,000 / 4,600 / 1,600).",
             {"build": "w2:hondo", "view": "3q", "persp": 30, "target": [3.4, 3.6, -3.4], "dist": 24}),
            ("hondo_kumi", "The hondo's corner from below: three-step sets, odaruki, the eave ceiling between steps "
             "2 and 3, the corner set's diagonal arms carrying the sumigi.",
             {"build": "w2:hondo", "interior": {"cam": [-3.4, 1.7, 3.8], "look": [0.1, 4.0, -0.2], "lens": 22}}),
            ("shoro", "Bell tower (shoro): hakama skirt on a stone platform, upper deck with W2P1's koran railing, "
             "degumi corner sets, bell beam (memory bell_hook), curved irimoya hongawara. 5,807 / 2,135 / 1,047.",
             {"build": "w2:shoro", "view": "3q", "persp": 30, "target": [1.37, 3.9, -1.37], "dist": 17}),
        ]),
}


def main(argv):
    sheet = argv[0]
    title, jobs = SHEETS_DEF[sheet]
    only = [a for a in argv[1:] if not a.startswith("--")]
    if "--compose" not in argv:
        todo = [j for j in jobs if not only or j[0] in only]
        jf = os.path.join(RB.RENDER, sheet + "_jobs.json")
        os.makedirs(RB.RENDER, exist_ok=True)
        with open(jf, "wb") as f:
            f.write(json.dumps({"out_dir": os.path.join(RB.RENDER, sheet), "res": list(RB.RES), "jobs": todo},
                               indent=1).encode("utf-8"))
        r = subprocess.run([RB.BLENDER, "--background", "--factory-startup", "--python", os.path.abspath(__file__), "--",
                            "--blender", jf], capture_output=True, text=True, errors="replace")
        done = [l for l in r.stdout.splitlines() if l.startswith("rendered")]
        print("%d/%d rendered" % (len(done), len(todo)))
        if len(done) < len(todo):
            print((r.stdout + r.stderr)[-4000:])
    note = ""
    jp = os.path.join(RB.DEV, "parts", "w2p2_assembly_checks.json")
    if os.path.isfile(jp):
        res = json.load(open(jp, encoding="utf-8"))
        note = "Checks (parts/w2p2_assembly_checks.json): " + ", ".join(
            "%s %d/%d" % (nm, sum(1 for c in r["checks"] if c["ok"]), len(r["checks"])) for nm, r in sorted(res.items()))
    RB.compose(sheet, title, jobs, note)


RB._orig_get_part = RB.get_part
RB.get_part = get_part

if __name__ == "__main__":
    if "--blender" in sys.argv:
        RB.blender_main(json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8")))
    else:
        main(sys.argv[1:])
