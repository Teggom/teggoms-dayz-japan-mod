#!/usr/bin/env python3
r"""build_w2f.py - W2F specialty props (shrine / temple / smithy / guard post) -> jp_furniture.pbo

  python build_w2f.py [prop ...] [--list] [--no-binarize] [--pack]

Builds INTO the furniture pipeline the way spikes/S1/build_s1.py does (B3a's build.py + L1 + S1, none edited): the
W2F props_w2f_*.py modules are appended after B3a's, L1's and S1's MODULES, so config.cpp / model.cfg /
jp_furniture.pbo carry all of them together.
  - W2F masters -> spikes/W2F/out/<cat>/ ; only W2F models are binarized
  - checks -> spikes/W2F/checks.json (B3a's check set + TXT); logs + PBO stage -> spikes/W2F/_build
  - sidecars (src/JP/furniture/<cat>/<prop>.prop.json) carry master + mount like L1 / S1's
PITFALL: a later B3a / L1 / S1 build rewrites config.cpp without the W2F classes: run this with --pack afterwards.
Never starts or stops the server, the game or any GUI program.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [HERE, os.path.join(DEV, "spikes", "S1"), os.path.join(DEV, "spikes", "L1"),
                os.path.join(DEV, "spikes", "L2")]
import build_s1 as S1  # noqa: E402  (sets B.MODULES = B3a + L1 + S1)
import textface  # noqa: E402

B = S1.B
W2F_MODULES = ["props_w2f_sacred", "props_w2f_civic"]
W2F_CATS = {"sacred", "civicfit"}
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
    sc["made_by"] = "spikes/W2F/build_w2f.py (agent W2F, 2026-10-01) on spikes/B3a/build.py"
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
                faces.get("Resolution 3", "-"), "PASS" if not fails else "FAIL " + ", ".join(
                    "%s(%s)" % (c["id"], json.dumps(c["detail"], ensure_ascii=False)[:400]) for c in fails)))
            built.append((m, P, faces))
        B.wb(os.path.join(B.SRC, prop["cat"], prop["id"] + ".prop.json"), json.dumps(sidecar(prop, built), indent=1,
                                                                                     ensure_ascii=False))
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    return results


def built_models(reg):
    out = S1.built_models([p for p in reg if p["cat"] not in W2F_CATS])
    for prop in reg:
        if prop["cat"] in W2F_CATS:
            for m in prop["models"]:
                if os.path.isfile(os.path.join(OUT_W2F, prop["cat"], m["p3d"] + ".p3d")):
                    out.append((prop, m))
    return out


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
    sel = B.select(my, argv)
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
                          "w2f_registered": len(mine_names), "classes_in_config": len(models)}
    B.wb(B.CHECKS, json.dumps(results, indent=1, ensure_ascii=False))
    for k, v in glob.items():
        print(k, "PASS" if v["pass"] else "FAIL", json.dumps(v["detail"])[:300])
    print("W2F models: %d, all checks pass: %d; classes in config.cpp: %d" % (
        results["summary"]["models"], results["summary"]["pass"], len(models)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
