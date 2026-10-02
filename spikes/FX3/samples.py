#!/usr/bin/env python3
r"""FX3 sample set: the SHIPPED recipes, built in memory and written ONLY to spikes/FX3/out/<mode>/ (copies; nothing
in B3a / B3b / buildings / src is written). Two separate processes so the 'after' hook is installed before the prop
modules bind fkit.band_fit:

  python spikes/FX3/samples.py before     today's UVs
  python spikes/FX3/samples.py after      uvwood.remap_part on every model (Part.lods hook; the building: explicit
                                          remap BEFORE zfight.resolve, exactly as phase 2 will do in pipeline.py)

Writes out/<mode>/*.p3d and out/<mode>/stats.json (faces remapped, uv groups, C20 'same' pairs for the building).
"""
import importlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B3a"), os.path.join(DEV, "spikes", "B3b"),
          os.path.join(DEV, "buildings"), HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

# (pipeline, prop id, model index) -> sample name
PROPS = [("b3b", "jp_s_torii_wood", 0, "torii"), ("b3b", "jp_s_bench", 0, "bench"),
         ("b3b", "jp_s_firewood_stack", 0, "woodpile"), ("b3a", "jp_f_nagamochi", 0, "chest"),
         ("b3a", "jp_f_tansu", 0, "tansu")]
BUILDING = dict(name="jp_teahouse_shop_thatch", kind="teahouse", size="shop", roof="thatch")   # K2


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    sp.loader.exec_module(m)
    return m


def main(mode):
    out = os.path.join(HERE, "out", mode)
    os.makedirs(out, exist_ok=True)
    from jpparts import core, mlod, zfight as ZF
    import fkit
    import uvwood
    if mode == "after":
        uvwood.install(core, fkit)
    stats = {}
    B3b = load(os.path.join(DEV, "spikes", "B3b", "build.py"), "fx3_b3b_build")
    regs = {"b3b": B3b.registry(), "b3a": B3b.B3A.registry()}
    for pipe, pid, k, nick in PROPS:
        prop = next(p for p in regs[pipe] if p["id"] == pid)
        m = prop["models"][k]
        P = m["build"]()
        P.pid = m["p3d"]
        lods = P.lods()
        mlod.write_mlod(os.path.join(out, nick + ".p3d"), lods)
        nb = sum(len(getattr(s, "uvband", ())) for s in P.solids)
        stats[nick] = {"p3d": m["p3d"], "faces_r1": len(lods[0].faces), "band_faces": nb}
        print(mode, nick, m["p3d"], stats[nick])
    import civickit
    M, floors, rooms = civickit.model(**BUILDING)
    if mode == "after":
        r = uvwood.remap_part(M, salt=BUILDING["name"])
        stats["teahouse_remap"] = r
    ZF.resolve(M)
    zr = ZF.coplanar(M)
    stats["teahouse_C20_same"] = len(zr["same"])
    stats["teahouse_hidden_pairs"] = len(zr["hidden"])
    lods = M.lods()
    mlod.write_mlod(os.path.join(out, "teahouse.p3d"), lods)
    print(mode, "teahouse", stats.get("teahouse_remap"), "C20 same", len(zr["same"]), "hidden", len(zr["hidden"]))
    with open(os.path.join(out, "stats.json"), "wb") as f:
        f.write(json.dumps(stats, indent=1).encode("utf-8"))


if __name__ == "__main__":
    main(sys.argv[1])
