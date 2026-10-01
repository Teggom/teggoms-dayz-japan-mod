r"""bindcheck.py - does every shipped building BIND in the engine? (FB1, 2026-10-01)

A building baked into the terrain (WRP / test/placements/C.csv) is matched to its config + script class ONLY through
the class named Land_<p3d file name> (case-insensitive), and only when its Geometry LOD carries the named property
class=house. Without both the game draws the model but never binds the class: no doors, no loot group, no actions
(Stephen's showcase walk, 2026-10-01: 97 of 128 classes failed the first rule; the server and client logs say
"<p3d>: house, config class missing"; F1's well, 2026-09-30, failed the second).

  B1  class name == "Land_" + p3d stem (case-insensitive)
  B2  the shipped p3d (src/JP/buildings/<model_dir>/<name>.p3d, ODOL or MLOD) has the Geometry property class=house

  python buildings/bindcheck.py        every shipped building with a record; exit 1 on any failure
Used by pipeline.combine() (the build FAILS on a problem) and by shellcheck / the generic checks (one line per building).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(DEV, "src", "JP", "buildings")

_ODOL_HOUSE = re.compile(rb"class\x00house\x00", re.I)                       # ODOL named property: two C strings
_MLOD_HOUSE = re.compile(rb"#Property#\x00\x80\x00\x00\x00class\x00{59}house\x00", re.I)   # MLOD: 64 + 64 bytes


def stem(model_path):
    return os.path.splitext(os.path.basename(model_path.replace("\\", "/")))[0]


def class_matches(cls, model_path):
    return cls.lower() == ("land_" + stem(model_path)).lower()


def has_class_house(p3d):
    with open(p3d, "rb") as f:
        data = f.read()
    rx = _ODOL_HOUSE if data[:4] == b"ODOL" else _MLOD_HOUSE
    return bool(rx.search(data))


def check(cls, model_path, model_dir, name):
    """-> list of problems for one building (empty = binds)."""
    probs = []
    if not class_matches(cls, model_path):
        probs.append("B1 class %s != Land_%s (the p3d stem): the engine will not bind it" % (cls, stem(model_path)))
    p = os.path.join(SRC, model_dir, name + ".p3d")
    if not os.path.isfile(p):
        probs.append("B2 %s missing" % p)
    elif not has_class_house(p):
        probs.append("B2 %s: no Geometry property class=house" % os.path.relpath(p, DEV))
    return probs


def check_records(recs):
    """recs: [(registry entry, record dict)] -> {class: [problems]} for the failing ones."""
    bad = {}
    seen = {}
    for b, r in recs:
        probs = check(r["class"], r["model"], r["model_dir"], r["name"])
        k = r["class"].lower()
        if k in seen:
            probs.append("class also shipped by %s" % seen[k])
        seen[k] = b["key"]
        if probs:
            bad[r["class"]] = probs
    return bad


def main():
    sys.path.insert(0, HERE)
    import registry
    import pipeline
    recs = []
    for b in registry.BUILDINGS:
        if b["ship"] and os.path.isfile(pipeline.record_path(b)):
            with open(pipeline.record_path(b), "rb") as f:
                recs.append((b, json.loads(f.read().decode("utf-8"))))
    bad = check_records(recs)
    for c, ps in sorted(bad.items()):
        for p in ps:
            print("FAIL %s: %s" % (c, p))
    print("bindcheck: %d shipped buildings, %d bind (B1 class == Land_<p3d stem>, B2 Geometry class=house), %d fail"
          % (len(recs), len(recs) - len(bad), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
