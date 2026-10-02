#!/usr/bin/env python3
r"""build_l2.py - L2, the outdoor life layer (research/interior/LIFE_LAYER.md, items 51-74) -> jp_site.pbo

  python build_l2.py [prop ...] [--list] [--no-binarize] [--pack] [--config-only]

Builds INTO B3b's site pipeline (spikes/B3b/build.py): the L2 props_l2_*.py modules are appended to B3b's MODULES.
Config (CA1, 2026-10-01): L2 writes ONLY its own classes to src/JP/site/_frags/L2.json; tools/assemble_config.py merges
every builder's fragment (B3b, L2, ...) into config.cpp / model.cfg / jp_site_wells.c, so jp_site.pbo carries them all.
--config-only: no model build / binarize, just re-emit L2's fragment from spikes/L2/out + assemble (+ --pack).
What differs from a plain B3b run (the wrapped functions below):
  - L2's MLOD masters go to spikes/L2/out/<cat>/ (B3b's stay in spikes/B3b/out/); only L2's models are binarized
    (B3b's ODOLs in src/JP/site are left as they are)
  - checks -> spikes/L2/checks.json (B3b's checks.json is not touched): B3b's check set + TXT (spikes/L2/textface.py:
    every text decal faces out of its host and reads left to right in game); logs and the PBO stage -> spikes/L2/_build
  - every L2 sidecar model entry also carries: "master" (the MLOD master, DEV-relative, for the decorator), "mount"
    (yard | street | eaves | road | shore | field | surface: where the decorator may put it), "mount_note", "tiers"
Frames and anchors are B3b's (skit.py): 'floor' base centre on the terrain; 'wall' the wall plane is z = 0, y = 0 at
the wall foot (eaves pieces hang from 'hang_y'). (The old "rerun this after a B3b rebuild" pitfall is gone since CA1:
B3b now writes only its own fragment.)
Never starts or stops the server, the game or any GUI program.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
B3B = os.path.join(DEV, "spikes", "B3b")
sys.path[:0] = [HERE, B3B]
import build as B  # noqa: E402
import textface  # noqa: E402

L2_MODULES = ["props_l2_yard", "props_l2_street"]
L2_CATS = {"yard_life", "street_life"}
OUT_L2 = os.path.join(HERE, "out")
OUT_B3B = os.path.join(B3B, "out")
B.MODULES = B.MODULES + [m for m in L2_MODULES if m not in B.MODULES]
B.CHECKS = os.path.join(HERE, "checks.json")
B.TEMP = os.path.join(HERE, "_build")
B.HERE = HERE                    # binarize.log -> spikes/L2
MOUNTS = ("yard", "street", "eaves", "road", "shore", "field", "surface")
MOUNT_NOTE = {
    "yard": "in a house yard (back or side yard, by a door or wall): base centre on the ground",
    "street": "in a town street or at a shop front: base centre on the ground (wall pieces: the facade is z = 0)",
    "eaves": "under the eaves of a house or shop: the facade is z = 0, y = 0 at the wall foot, hangs from hang_y "
             "(move y to the real eave / beam), or stands on the veranda edge",
    "road": "on a road or highway, dropped: base centre on the ground (visual; never across a building door)",
    "shore": "on a beach, river bank or landing: base centre on the ground above the water line",
    "field": "in a field or at a field edge (paddy stubble): base centre on the ground",
    "surface": "on a placed prop's loot surface (B3b's bench seats): decor.on_surface(name, bench); base centre on "
               "the seat",
}


def out_dir(cat):
    return OUT_L2 if cat in L2_CATS else OUT_B3B


def l2_props(reg):
    return [p for p in reg if p["cat"] in L2_CATS]


def sidecar(prop, built):
    sc = B.sidecar(prop, built)
    sc["frame"] += "; mount = where the decorator may place it (see 'mount_note')"
    sc["made_by"] = "spikes/L2/build_l2.py (agent L2, 2026-09-30) on spikes/B3b/build.py"
    sc["life_layer"] = prop.get("ll")
    sc["refs_local"] = prop.get("refs", [])
    for (m, P, faces), row in zip(built, sc["models"]):
        mount = m.get("mount") or prop.get("mount")
        assert mount in MOUNTS, (prop["id"], mount)
        row["master"] = os.path.relpath(os.path.join(OUT_L2, prop["cat"], m["p3d"] + ".p3d"), DEV).replace("\\", "/")
        row["mount"] = mount
        row["mount_note"] = MOUNT_NOTE[mount]
        row["tiers"] = m.get("tiers") or prop.get("tiers")
    return sc


def txt_check(mp):
    res = textface.check_file(mp)
    bad = [r for r in res if not (r["reads"] and r["host_behind"])]
    return {"id": "TXT", "name": "text decals face out of their host and read left to right in game (%d faces)" %
            len(res), "pass": not bad, "detail": bad[:4]}


def write_all(sel):
    results = json.load(open(B.CHECKS, encoding="utf-8")) if os.path.isfile(B.CHECKS) else {"models": {}}
    for prop in sel:
        built = []
        for m in prop["models"]:
            P = m["build"]()
            P.pid = m["p3d"]
            lods = P.lods()
            mp = os.path.join(OUT_L2, prop["cat"], m["p3d"] + ".p3d")
            os.makedirs(os.path.dirname(mp), exist_ok=True)
            B.mlod.write_mlod(mp, lods)
            res, faces, L = B.check_model(P, mp, m)
            res.append(txt_check(mp))
            fails = [c for c in res if not c["pass"]]
            results["models"][m["p3d"]] = {"prop": prop["id"], "cat": prop["cat"], "state": m["state"],
                                           "variant": m["variant"], "pass": not fails, "faces": faces, "checks": res}
            print("%-40s %-6s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), "PASS" if not fails else "FAIL " + ", ".join(
                    "%s(%s)" % (c["id"], json.dumps(c["detail"], ensure_ascii=False)[:300]) for c in fails)))
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
    return out


def write_fragment(models):
    """CA1: L2's own classes (L2_CATS, master in spikes/L2/out) -> _frags/L2.json, then assemble jp_site."""
    return B.write_fragment([(p, m) for p, m in models if p["cat"] in L2_CATS], builder="L2",
                            writer="spikes/L2/build_l2.py", order=20)


def binarize(models):
    """B3b's binarize, but copying the masters from spikes/L2/out (L2 models only)."""
    save = B.OUT
    B.OUT = OUT_L2
    try:
        return B.binarize(models)
    finally:
        B.OUT = save


def main(argv):
    reg = B.registry()
    mine = l2_props(reg)
    if "--list" in argv:
        n = 0
        for p in mine:
            print(p["id"], p["cat"], [m["p3d"] for m in p["models"]])
            n += len(p["models"])
        print(len(mine), "props,", n, "models")
        return 0
    if "--config-only" in argv:     # CA1: re-emit the fragment from the masters + assemble (+ --pack)
        asm = write_fragment(built_models(reg))
        ok = all(B.B3A.cfgconvert(os.path.join(B.SRC, f))[0] for f in ("config.cpp", "model.cfg"))
        print("CFG", "PASS" if ok else "FAIL", "; classes in config.cpp: %d" % asm["classes"])
        if "--pack" in argv:
            print("packed:", *B.pack())
        return 0 if ok else 1
    sel = B.select(mine, argv)
    results = write_all(sel)
    models = built_models(reg)
    names = [m["p3d"] for _, m in models]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        raise SystemExit("duplicate p3d names: %s" % dup)
    asm = write_fragment(models)
    glob = {}
    conv = [B.B3A.cfgconvert(os.path.join(B.SRC, "config.cpp")), B.B3A.cfgconvert(os.path.join(B.SRC, "model.cfg"))]
    glob["CFG"] = {"pass": all(c[0] for c in conv), "detail": [c[1] for c in conv]}
    if "--no-binarize" not in argv:
        mm = [(p, m) for p, m in models if p["cat"] in L2_CATS]
        ok, det = binarize(mm)
        glob["BIN"] = {"pass": ok, "detail": det}
    if "--pack" in argv:
        ok, det = B.pack()
        glob["PBO"] = {"pass": ok, "detail": det}
        print("packed:", ok, det)
    results["global"] = glob
    results["summary"] = {"models": len(results["models"]),
                          "pass": sum(1 for r in results["models"].values() if r["pass"]),
                          "classes_in_config": asm["classes"]}
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("L2 models: %d, all checks pass: %d; classes in config.cpp (all builders): %d" % (
        results["summary"]["models"], results["summary"]["pass"], asm["classes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
