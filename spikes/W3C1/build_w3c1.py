#!/usr/bin/env python3
r"""build_w3c1.py - W3C1 specialty props (brewery, water mill, dyer, paper mill) -> jp_furniture.pbo

  python build_w3c1.py [prop ...] [--list] [--no-binarize] [--pack] [--config-only]

Copied from spikes/W3B/build_w3b.py (W3C1, 2026-10-02): chains after W3B (its module list), cat 'brewfit', fragment
'W3C1' (order 60), masters in spikes/W3C1/out. The original W3B notes follow.

Builds INTO the furniture pipeline the way spikes/W2F/build_w2f.py does (B3a's build.py + L1 + S1 + W2F): the W3B
props_w3b.py module is appended after their MODULES.
  - W3B masters -> spikes/W3B/out/<cat>/ ; only W3B models are binarized
  - checks -> spikes/W3B/checks.json (B3a's check set + TXT); logs + PBO stage -> spikes/W3B/_build
  - sidecars (src/JP/furniture/<cat>/<prop>.prop.json) carry master + mount like L1 / S1's
  - config (CA1, 2026-10-01): ONLY W2F's classes -> src/JP/furniture/_frags/W2F.json; tools/assemble_config.py merges
    every builder's fragment into config.cpp / model.cfg, so a later B3a / L1 / S1 build keeps the W2F classes
  --config-only: no model build / binarize, just re-emit W2F's fragment from spikes/W2F/out + assemble (+ --pack).
Never starts or stops the server, the game or any GUI program.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [HERE, os.path.join(DEV, "spikes", "W2F"), os.path.join(DEV, "spikes", "S1"),
                os.path.join(DEV, "spikes", "L1"), os.path.join(DEV, "spikes", "L2")]
sys.path.insert(1, os.path.join(DEV, "spikes", "W3B"))
import build_w3b as W3  # noqa: E402  (sets B.MODULES = B3a + L1 + S1 + W2F + W3B)
import textface  # noqa: E402

W2 = W3
B = W3.B
S1 = W3.S1
W2F_MODULES = ["props_w3c1"]
W2F_CATS = {"brewfit"}
OUT_W2F = os.path.join(HERE, "out")
B.MODULES = B.MODULES + [m for m in W2F_MODULES if m not in B.MODULES]
B.CHECKS = os.path.join(HERE, "checks.json")
B.TEMP = os.path.join(HERE, "_build")
B.HERE = HERE
MOUNT_NOTE = dict(S1.MOUNT_NOTE)


def mine(reg):
    return [p for p in reg if p["cat"] in W2F_CATS]


def sidecar(prop, built):
    sc = B.sidecar(prop, built)
    sc["frame"] += "; mount = where the decorator may place it (see 'mount_note')"
    sc["made_by"] = "spikes/W3C1/build_w3c1.py (agent W3C1, 2026-10-02) on spikes/B3a/build.py"
    for (m, P, faces), row in zip(built, sc["models"]):
        mount = m.get("mount") or prop.get("mount") or ("wall" if P.anchor == "wall" else
                                                          "beam" if P.anchor == "hang" else "floor")
        assert mount in MOUNT_NOTE, mount
        row["master"] = os.path.relpath(os.path.join(OUT_W2F, prop["cat"], m["p3d"] + ".p3d"), DEV).replace("\\", "/")
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
            mp = os.path.join(OUT_W2F, prop["cat"], m["p3d"] + ".p3d")
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
            print("%-34s %-9s R1 %4d R2 %4d R3 %4s  %s" % (
                m["p3d"], P.budget, faces.get("Resolution 1", 0), faces.get("Resolution 2", 0),
                faces.get("Resolution 3", "-"), ("PASS" + B.over_note(res)) if not fails else "FAIL " + ", ".join(
                    "%s(%s)" % (c["id"], json.dumps(c["detail"], ensure_ascii=False)[:400]) for c in fails)))
            built.append((m, P, faces))
        B.wb(os.path.join(B.SRC, prop["cat"], prop["id"] + ".prop.json"), json.dumps(sidecar(prop, built), indent=1,
                                                                                     ensure_ascii=False))
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    return results


def built_models(reg):
    out = W2.built_models([p for p in reg if p["cat"] not in W2F_CATS])
    for prop in reg:
        if prop["cat"] in W2F_CATS:
            for m in prop["models"]:
                if os.path.isfile(os.path.join(OUT_W2F, prop["cat"], m["p3d"] + ".p3d")):
                    out.append((prop, m))
    return out


def write_fragment(models):
    """CA1: W3C1's own classes (cat brewfit, masters in spikes/W3C1/out) -> _frags/W3C1.json, then assemble."""
    mine = [(p, m) for p, m in models if p["cat"] in W2F_CATS]
    B.ASM.write_fragment(B.PBO, "W3C1", "spikes/W3C1/build_w3c1.py", 60, B.frag_classes(mine),
                         [m["p3d"] for _, m in mine], required=("DZ_Data", "JP_Common"))
    return B.ASM.assemble(B.PBO)


def binarize(models):
    for prop, _ in models:
        os.makedirs(os.path.join(B.SRC, prop["cat"]), exist_ok=True)
    save = B.OUT
    B.OUT = OUT_W2F
    try:
        return B.binarize(models)
    finally:
        B.OUT = save


def main(argv):
    reg = B.registry()
    my = mine(reg)
    if "--list" in argv:
        n = 0
        for p in my:
            print(p["id"], p["cat"], [m["p3d"] for m in p["models"]])
            n += len(p["models"])
        print(len(my), "props,", n, "models")
        return 0
    if "--config-only" in argv:     # CA1: re-emit the fragment from the masters + assemble (+ --pack)
        asm = write_fragment(built_models(reg))
        ok = all(B.cfgconvert(os.path.join(B.SRC, f))[0] for f in ("config.cpp", "model.cfg"))
        print("CFG", "PASS" if ok else "FAIL", "; classes in config.cpp: %d" % asm["classes"])
        if "--pack" in argv:
            print("packed:", *B.pack())
        return 0 if ok else 1
    sel = B.select(my, argv)
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
        mm = [(p, m) for p, m in models if p["cat"] in W2F_CATS and p in sel]
        ok, det = binarize(mm)
        glob["BIN"] = {"pass": ok, "detail": det}
    if "--pack" in argv:
        ok, det = B.pack()
        glob["PBO"] = {"pass": ok, "detail": det}
        print("packed:", ok, det)
    results["global"] = glob
    mine_names = {m["p3d"] for p in my for m in p["models"]}
    results["summary"] = {"models": len([k for k in results["models"] if k in mine_names]),
                          "pass": sum(1 for k, r in results["models"].items() if r["pass"] and k in mine_names),
                          "w3c1_registered": len(mine_names), "classes_in_config": asm["classes"]}
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("W3C1 models: %d, all checks pass: %d; classes in config.cpp (all builders): %d" % (
        results["summary"]["models"], results["summary"]["pass"], asm["classes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
