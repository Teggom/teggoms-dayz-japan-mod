#!/usr/bin/env python3
r"""build_l1.py - L1, the interior life layer (research/interior/LIFE_LAYER.md, items 1-50) -> jp_furniture.pbo

  python build_l1.py [prop ...] [--list] [--no-binarize] [--pack]

Builds INTO B3a's furniture pipeline (spikes/B3a/build.py) without editing it: the L1 props_life_*.py modules are
appended to B3a's MODULES, so config.cpp / model.cfg / jp_furniture.pbo carry B3a's 110 + B4's 2 + L1's models together.
What differs from a plain B3a run (the wrapped functions below):
  - L1's MLOD masters go to spikes/L1/out/<cat>/ (B3a's stay in spikes/B3a/out/); only L1's models are binarized
    (B3a's ODOLs in src/JP/furniture are left as they are)
  - checks -> spikes/L1/checks.json (B3a's checks.json is not touched); logs and the PBO stage -> spikes/L1/_build
  - every L1 sidecar model entry also carries: "master" (the MLOD master, DEV-relative, for the decorator), "mount"
    (wall | post | beam | doorway | surface | floor | kamado: where the decorator may put it) and "mount_note"
Frames and anchors are B3a's (fkit.py): 'floor' base centre; 'wall' origin on the floor below, wall (or post) face
z = 0; 'hang' origin at the beam / head underside, the prop hangs down (-y).
Never starts or stops the server, the game or any GUI program.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3A = os.path.join(DEV, "spikes", "B3a")
sys.path[:0] = [HERE, B3A]
import build as B  # noqa: E402

L1_MODULES = ["props_life_wall", "props_life_religious", "props_life_meal", "props_life_living", "props_life_work",
              "props_life_tier"]
L1_CATS = {"wall", "religious", "meal", "living", "work", "tier"}
OUT_L1 = os.path.join(HERE, "out")
OUT_B3A = os.path.join(B3A, "out")
B.MODULES = B.MODULES + [m for m in L1_MODULES if m not in B.MODULES]
B.CHECKS = os.path.join(HERE, "checks.json")
B.TEMP = os.path.join(HERE, "_build")
B.HERE = HERE                    # binarize.log -> spikes/L1
MOUNTS = ("wall", "post", "beam", "doorway", "surface", "floor", "kamado")
MOUNT_NOTE = {
    "wall": "on a wall: origin on the floor below, the wall face is z = 0 (anchor 'wall'); height is built in",
    "post": "on a post face: origin on the floor below, the post face is z = 0 (anchor 'wall'); height built in",
    "beam": "under a beam or the loft joists: origin = the beam underside (anchor 'hang'), the prop hangs down",
    "doorway": "in a doorway head: origin = the head (kamoi) underside at the opening centre, in the opening plane",
    "surface": "on a raised surface (a shelf board, chest lid, desk top or the floor): base centre on that surface",
    "floor": "on the floor: base centre on the floor",
    "kamado": "seated in a kamado rim like jp_f_kama: y = rim top - seat_y",
}


def out_dir(cat):
    return OUT_L1 if cat in L1_CATS else OUT_B3A


def l1_props(reg):
    return [p for p in reg if p["cat"] in L1_CATS]


def sidecar(prop, built):
    sc = B.sidecar(prop, built)
    sc["frame"] += "; mount = where the decorator may place it (see 'mount_note')"
    sc["made_by"] = "spikes/L1/build_l1.py (agent L1, 2026-09-30) on spikes/B3a/build.py"
    sc["life_layer"] = prop.get("ll")
    sc["refs_local"] = prop.get("refs", [])
    for (m, P, faces), row in zip(built, sc["models"]):
        mount = m.get("mount") or prop.get("mount") or ("wall" if P.anchor == "wall" else
                                                          "beam" if P.anchor == "hang" else "floor")
        assert mount in MOUNTS, mount
        row["master"] = os.path.relpath(os.path.join(OUT_L1, prop["cat"], m["p3d"] + ".p3d"), DEV).replace("\\", "/")
        row["mount"] = mount
        row["mount_note"] = MOUNT_NOTE[mount]
        row["tiers"] = m.get("tiers") or prop.get("tiers")
        if getattr(P, "hang_len", None):
            row["hang_len"] = round(P.hang_len, 3)       # how far the prop hangs below its beam (head room check)
        if getattr(P, "seat_y", None) is not None:
            row["seat_y"] = P.seat_y
    return sc


def write_all(sel):
    results = json.load(open(B.CHECKS, encoding="utf-8")) if os.path.isfile(B.CHECKS) else {"models": {}}
    for prop in sel:
        built = []
        for m in prop["models"]:
            P = m["build"]()
            P.pid = m["p3d"]
            lods = P.lods()
            mp = os.path.join(OUT_L1, prop["cat"], m["p3d"] + ".p3d")
            os.makedirs(os.path.dirname(mp), exist_ok=True)
            B.mlod.write_mlod(mp, lods)
            res, faces, L = B.check_model(P, mp, m)
            fails = [c for c in res if not c["pass"]]
            results["models"][m["p3d"]] = {"prop": prop["id"], "cat": prop["cat"], "state": m["state"],
                                           "variant": m["variant"], "pass": not fails, "faces": faces, "checks": res}
            print("%-38s %-9s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), "PASS" if not fails else "FAIL " + ", ".join(
                    "%s(%s)" % (c["id"], json.dumps(c["detail"])[:300]) for c in fails)))
            built.append((m, P, faces))
        B.wb(os.path.join(B.SRC, prop["cat"], prop["id"] + ".prop.json"), json.dumps(sidecar(prop, built), indent=1,
                                                                                     ensure_ascii=False))
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    return results


def built_models(reg):
    out = []
    for prop in reg:
        for m in prop["models"]:
            if os.path.isfile(os.path.join(out_dir(prop["cat"]), prop["cat"], m["p3d"] + ".p3d")):
                out.append((prop, m))
            elif prop["cat"] not in L1_CATS and os.path.isfile(os.path.join(B.SRC, prop["cat"], m["p3d"] + ".p3d")):
                out.append((prop, m))              # a B3a / B4 model whose master is not regenerated here: keep it
    return out


def binarize(models):
    """B3a's binarize, but copying the masters from spikes/L1/out (L1 models only)."""
    for prop, _ in models:
        os.makedirs(os.path.join(B.SRC, prop["cat"]), exist_ok=True)
    save = B.OUT
    B.OUT = OUT_L1
    try:
        # B3a's binarize() copies OUT -> SRC, then binarizes one category folder at a time
        return B.binarize(models)
    finally:
        B.OUT = save


def main(argv):
    reg = B.registry()
    mine = l1_props(reg)
    if "--list" in argv:
        n = 0
        for p in mine:
            print(p["id"], p["cat"], [m["p3d"] for m in p["models"]])
            n += len(p["models"])
        print(len(mine), "props,", n, "models")
        return 0
    sel = B.select(mine, argv)
    results = write_all(sel)
    models = built_models(reg)
    names = [m["p3d"] for _, m in models]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        raise SystemExit("duplicate p3d names: %s" % dup)
    B.wb(os.path.join(B.SRC, "config.cpp"), B.config_cpp(models))
    B.wb(os.path.join(B.SRC, "model.cfg"), B.model_cfg(models))
    glob = {}
    conv = [B.cfgconvert(os.path.join(B.SRC, "config.cpp")), B.cfgconvert(os.path.join(B.SRC, "model.cfg"))]
    glob["CFG"] = {"pass": all(c[0] for c in conv), "detail": [c[1] for c in conv]}
    if "--no-binarize" not in argv:
        mm = [(p, m) for p, m in models if p["cat"] in L1_CATS]
        ok, det = binarize(mm)
        glob["BIN"] = {"pass": ok, "detail": det}
    if "--pack" in argv:
        ok, det = B.pack()
        glob["PBO"] = {"pass": ok, "detail": det}
        print("packed:", ok, det)
    results["global"] = glob
    results["summary"] = {"models": len(results["models"]),
                          "pass": sum(1 for r in results["models"].values() if r["pass"]),
                          "classes_in_config": len(models)}
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("L1 models: %d, all checks pass: %d; classes in config.cpp: %d" % (
        results["summary"]["models"], results["summary"]["pass"], len(models)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
