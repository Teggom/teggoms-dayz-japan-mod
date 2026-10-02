#!/usr/bin/env python3
r"""build_s1.py - S1, the KEEP_TRADES shop sets (research/interior/SHOP_SETS.md) -> jp_furniture.pbo

  python build_s1.py [prop ...] [--list] [--no-binarize] [--pack] [--config-only]

Builds INTO B3a's furniture pipeline (spikes/B3a/build.py) the way spikes/L1/build_l1.py does: the S1 props_s1_*.py
modules are appended after B3a's and L1's MODULES. Config (CA1, 2026-10-01): S1 writes ONLY its own classes to
src/JP/furniture/_frags/S1.json; tools/assemble_config.py merges every builder's fragment into config.cpp / model.cfg.
--config-only: no model build / binarize, just re-emit S1's fragment from spikes/S1/out + assemble (+ --pack).
  - S1's MLOD masters go to spikes/S1/out/<cat>/ (B3a's stay in spikes/B3a/out, L1's in spikes/L1/out); only S1's
    models are binarized
  - checks -> spikes/S1/checks.json (B3a's check set + TXT: spikes/L2/textface.py on every model with text);
    logs and the PBO stage -> spikes/S1/_build
  - every sidecar model entry carries "master", "mount" (wall | post | beam | doorway | surface | floor | kamado) and
    "mount_note", like L1's, so the decorator (parts/kit/jpparts/decor.py) can place it at once
Never starts or stops the server, the game or any GUI program.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [HERE, os.path.join(DEV, "spikes", "L1"), os.path.join(DEV, "spikes", "L2")]
import build_l1 as L1  # noqa: E402  (sets B.MODULES = B3a + L1 and redirects; we redirect again below)
import textface  # noqa: E402
import s1kit  # noqa: E402,F401

B = L1.B
S1_MODULES = ["props_s1_g1", "props_s1_g2", "props_s1_g3", "props_s1_g4", "props_s1_g5", "props_s1_g6"]
S1_CATS = {"shopgoods", "shopfit", "shopsign"}
OUT_S1 = os.path.join(HERE, "out")
B.MODULES = B.MODULES + [m for m in S1_MODULES if m not in B.MODULES]
B.CHECKS = os.path.join(HERE, "checks.json")
B.TEMP = os.path.join(HERE, "_build")
B.HERE = HERE                    # binarize.log -> spikes/S1
MOUNT_NOTE = dict(L1.MOUNT_NOTE)
MOUNT_NOTE["wall"] += "; a shop-front piece (kanban, sugidama, shape sign): the FACADE plane z = 0, +z = the street"


def s1_props(reg):
    return [p for p in reg if p["cat"] in S1_CATS]


def sidecar(prop, built):
    sc = B.sidecar(prop, built)
    sc["frame"] += "; mount = where the decorator may place it (see 'mount_note')"
    sc["made_by"] = "spikes/S1/build_s1.py (agent S1, 2026-09-30) on spikes/B3a/build.py"
    sc["trades"] = prop.get("trades", [])
    sc["era"] = prop.get("era")
    for (m, P, faces), row in zip(built, sc["models"]):
        mount = m.get("mount") or prop.get("mount") or ("wall" if P.anchor == "wall" else
                                                          "beam" if P.anchor == "hang" else "floor")
        assert mount in MOUNT_NOTE, mount
        row["master"] = os.path.relpath(os.path.join(OUT_S1, prop["cat"], m["p3d"] + ".p3d"), DEV).replace("\\", "/")
        row["mount"] = mount
        row["mount_note"] = MOUNT_NOTE[mount]
        if getattr(P, "hang_len", None):
            row["hang_len"] = round(P.hang_len, 3)
    return sc


def write_all(sel):
    results = json.load(open(B.CHECKS, encoding="utf-8")) if os.path.isfile(B.CHECKS) else {"models": {}}
    for prop in sel:
        built = []
        for m in prop["models"]:
            P = m["build"]()
            P.pid = m["p3d"]
            lods = P.lods()
            mp = os.path.join(OUT_S1, prop["cat"], m["p3d"] + ".p3d")
            os.makedirs(os.path.dirname(mp), exist_ok=True)
            B.mlod.write_mlod(mp, lods)
            res, faces, L = B.check_model(P, mp, m)
            tx = textface.check_file(mp)
            if tx:
                bad = [r for r in tx if not (r["reads"] and r["host_behind"])]
                res.append({"id": "TXT", "name": "text decals face out of their host and read left to right in game "
                            "(%d faces)" % len(tx), "pass": not bad, "detail": bad[:4]})
            fails = [c for c in res if not c["pass"]]
            results["models"][m["p3d"]] = {"prop": prop["id"], "cat": prop["cat"], "state": m["state"],
                                           "variant": m["variant"], "pass": not fails, "faces": faces, "checks": res}
            print("%-40s %-9s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), ("PASS" + B.over_note(res)) if not fails else "FAIL " + ", ".join(
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
            if prop["cat"] in S1_CATS:
                if os.path.isfile(os.path.join(OUT_S1, prop["cat"], m["p3d"] + ".p3d")):
                    out.append((prop, m))
            elif os.path.isfile(os.path.join(L1.out_dir(prop["cat"]), prop["cat"], m["p3d"] + ".p3d")):
                out.append((prop, m))
            elif os.path.isfile(os.path.join(B.SRC, prop["cat"], m["p3d"] + ".p3d")):
                out.append((prop, m))          # a B3a / B4 / L1 model whose master is not here: keep it
    return out


def write_fragment(models):
    """CA1: S1's own classes (S1_CATS, master in spikes/S1/out) -> _frags/S1.json, then assemble jp_furniture."""
    mine = [(p, m) for p, m in models if p["cat"] in S1_CATS]
    B.ASM.write_fragment(B.PBO, "S1", "spikes/S1/build_s1.py", 30, B.frag_classes(mine), [m["p3d"] for _, m in mine],
                         required=("DZ_Data", "JP_Common"))
    return B.ASM.assemble(B.PBO)


def binarize(models):
    for prop, _ in models:
        os.makedirs(os.path.join(B.SRC, prop["cat"]), exist_ok=True)
    save = B.OUT
    B.OUT = OUT_S1
    try:
        return B.binarize(models)
    finally:
        B.OUT = save


def main(argv):
    reg = B.registry()
    mine = s1_props(reg)
    if "--list" in argv:
        n = 0
        for p in mine:
            print(p["id"], p["cat"], [m["p3d"] for m in p["models"]])
            n += len(p["models"])
        print(len(mine), "props,", n, "models")
        return 0
    if "--config-only" in argv:     # CA1: re-emit the fragment from the masters + assemble (+ --pack)
        asm = write_fragment(built_models(reg))
        ok = all(B.cfgconvert(os.path.join(B.SRC, f))[0] for f in ("config.cpp", "model.cfg"))
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
    conv = [B.cfgconvert(os.path.join(B.SRC, "config.cpp")), B.cfgconvert(os.path.join(B.SRC, "model.cfg"))]
    glob["CFG"] = {"pass": all(c[0] for c in conv), "detail": [c[1] for c in conv]}
    if "--no-binarize" not in argv:
        mm = [(p, m) for p, m in models if p["cat"] in S1_CATS]
        ok, det = binarize(mm)
        glob["BIN"] = {"pass": ok, "detail": det}
    if "--pack" in argv:
        ok, det = B.pack()
        glob["PBO"] = {"pass": ok, "detail": det}
        print("packed:", ok, det)
    results["global"] = glob
    mine_names = {m["p3d"] for p in mine for m in p["models"]}
    results["summary"] = {"models": len(results["models"]),
                          "pass": sum(1 for r in results["models"].values() if r["pass"]),
                          "s1_registered": len(mine_names), "classes_in_config": asm["classes"]}
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("S1 models: %d, all checks pass: %d; classes in config.cpp (all builders): %d" % (
        results["summary"]["models"], results["summary"]["pass"], asm["classes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
