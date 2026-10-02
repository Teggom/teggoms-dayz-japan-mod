#!/usr/bin/env python3
r"""snapshot.py - CA1: freeze the class lists of every PBO in ..\@Japan\addons (and the src model.cfg / script files of
the multi-builder areas) so the config assembler can be proven equivalent.

  python spikes/CA1/snapshot.py <name>        -> spikes/CA1/_snap/<name>/
  python spikes/CA1/snapshot.py --compare A B  -> class-level diff of every PBO + model.cfg + scripts, 0 = identical

Per PBO it stores every *config.cpp, every *.c script and files.txt (path, size; ODOL byte noise is not compared).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
ADDONS = os.path.join(ROOT, "@Japan", "addons")
SNAP = os.path.join(HERE, "_snap")
sys.path.insert(0, os.path.join(DEV, "tools"))
import cfgdiff  # noqa: E402

SRC_EXTRA = {   # area -> src files outside the PBO's config that the builders generate (model.cfg is not packed)
    "furniture": ["model.cfg"],
    "site": ["model.cfg", "scripts/4_World/JP_Site/jp_site_wells.c"],
}


def wb(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)


def take(name):
    out = os.path.join(SNAP, name)
    summary = {}
    for f in sorted(os.listdir(ADDONS)):
        if not f.lower().endswith(".pbo"):
            continue
        ents = cfgdiff.pbo_list(os.path.join(ADDONS, f))
        files = ["%s\t%d" % (n, s) for n, s in sorted(ents)]
        keep = cfgdiff.pbo_entries(os.path.join(ADDONS, f),
                                   lambda n: n.lower().endswith("config.cpp") or n.lower().endswith(".c"))
        for n, data in sorted(keep.items()):
            wb(os.path.join(out, "pbo", f, n.replace("\\", "/")), data)
        wb(os.path.join(out, "pbo", f, "files.txt"), ("\n".join(files) + "\n").encode("utf-8"))
        res = cfgdiff.load(os.path.join(ADDONS, f))
        summary[f] = {"files": len(ents), "classes": len(res["classes"]), "cfgvehicles": cfgdiff.count(res)}
    for area, rels in SRC_EXTRA.items():
        for rel in rels:
            p = os.path.join(DEV, "src", "JP", area, rel)
            if os.path.isfile(p):
                wb(os.path.join(out, "src", area, rel), open(p, "rb").read())
    wb(os.path.join(out, "summary.json"), json.dumps(summary, indent=1).encode("utf-8"))
    for k, v in summary.items():
        print("%-28s files %5d  classes %5d  CfgVehicles %4d" % (k, v["files"], v["classes"], v["cfgvehicles"]))
    return summary


def compare(a, b):
    A, B = os.path.join(SNAP, a), os.path.join(SNAP, b)
    total = 0
    sa = json.load(open(os.path.join(A, "summary.json")))
    sb = json.load(open(os.path.join(B, "summary.json")))
    for pbo in sorted(set(sa) | set(sb)):
        if pbo not in sa or pbo not in sb:
            print("%s: only in %s" % (pbo, a if pbo in sa else b))
            total += 1
            continue
        lines = []
        cfgs = set()
        for side in (A, B):
            d = os.path.join(side, "pbo", pbo)
            for r, _, fs in os.walk(d):
                for f in fs:
                    if f.lower().endswith("config.cpp") or f.lower().endswith(".c"):
                        cfgs.add(os.path.relpath(os.path.join(r, f), d))
        for rel in sorted(cfgs):
            pa, pb = os.path.join(A, "pbo", pbo, rel), os.path.join(B, "pbo", pbo, rel)
            if not (os.path.isfile(pa) and os.path.isfile(pb)):
                lines.append("%s only in %s" % (rel, a if os.path.isfile(pa) else b))
                continue
            if rel.lower().endswith(".c"):
                ta = cfgdiff.strip_comments(open(pa, "rb").read().decode("utf-8"))
                tb = cfgdiff.strip_comments(open(pb, "rb").read().decode("utf-8"))
                if sorted(cfgdiff._norm(x) for x in ta.splitlines() if x.strip()) != \
                        sorted(cfgdiff._norm(x) for x in tb.splitlines() if x.strip()):
                    lines.append("%s: script differs" % rel)
                continue
            lines += ["%s: %s" % (rel, x) for x in cfgdiff.diff(cfgdiff.load(pa), cfgdiff.load(pb), a, b)]
        fa = {l.split("\t")[0] for l in open(os.path.join(A, "pbo", pbo, "files.txt"), encoding="utf-8").read().split("\n") if l}
        fb = {l.split("\t")[0] for l in open(os.path.join(B, "pbo", pbo, "files.txt"), encoding="utf-8").read().split("\n") if l}
        for x in sorted(fa - fb):
            lines.append("file only in %s: %s" % (a, x))
        for x in sorted(fb - fa):
            lines.append("file only in %s: %s" % (b, x))
        print("%-28s classes %5d -> %5d  CfgVehicles %4d -> %4d  files %5d -> %5d  differences %d" % (
            pbo, sa[pbo]["classes"], sb[pbo]["classes"], sa[pbo]["cfgvehicles"], sb[pbo]["cfgvehicles"],
            sa[pbo]["files"], sb[pbo]["files"], len(lines)))
        for x in lines[:40]:
            print("    " + x)
        total += len(lines)
    for area, rels in SRC_EXTRA.items():
        for rel in rels:
            pa, pb = os.path.join(A, "src", area, rel), os.path.join(B, "src", area, rel)
            if not (os.path.isfile(pa) and os.path.isfile(pb)):
                continue
            if rel.endswith(".c"):
                ta = cfgdiff.strip_comments(open(pa, "rb").read().decode("utf-8"))
                tb = cfgdiff.strip_comments(open(pb, "rb").read().decode("utf-8"))
                d = [] if sorted(x.strip() for x in ta.splitlines() if x.strip()) == \
                    sorted(x.strip() for x in tb.splitlines() if x.strip()) else ["script differs"]
            else:
                d = cfgdiff.diff(cfgdiff.load(pa), cfgdiff.load(pb), a, b)
            print("src/JP/%s/%s: %d classes -> %d, differences %d" % (
                area, rel, len(cfgdiff.load(pa)["classes"]) if not rel.endswith(".c") else 0,
                len(cfgdiff.load(pb)["classes"]) if not rel.endswith(".c") else 0, len(d)))
            for x in d[:20]:
                print("    " + x)
            total += len(d)
    print("TOTAL differences: %d" % total)
    return 1 if total else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--compare"]:
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    take(sys.argv[1])
