#!/usr/bin/env python3
r"""build_parts.py - generate every JP part variant (build list order), write the MLOD sources, sidecars, manifest and
checks.

  python build_parts.py [--only substr[,substr]]

Per variant: src/JP/parts/<group>/<name>.p3d (MLOD, every LOD it contributes) + <name>.part.json (PLAYBOOK §10.2
sidecar); per group: src/JP/parts/<group>/checks.json; all: japan_dev/parts/manifest.json.
Parts are MLOD sources merged into buildings at build time; they are never packed.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from jpparts import core, checks, registry  # noqa: E402

DEV = core.DEV
OUT = os.path.join(DEV, "src", "JP", "parts")
BL = json.load(open(os.path.join(DEV, "research", "exterior", "build_list.json"), encoding="utf-8"))
BLE = {e["id"]: e for e in BL["entries"]}


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8") if isinstance(text, str) else text)


def contributes(lods):
    names = [core.mlod.lod_name(l.resolution) for l in lods]
    return names


def mats_of(part):
    keys = sorted({m for s in part.solids for m in s.fm})
    out = []
    for k in keys:
        mi = core.mat_info(k)
        out.append({"key": k, "id": mi["id"], "palette_id": mi["palette_id"],
                    "rvmat": core.rvmat_path(k, "<wear>"), "default_wear": part.wear_of(k),
                    "wear_selectable": ["_w0", "_w1", "_w2"]})
    return out


def sidecar(part, lods, counts, res, bl_entry, var_entry):
    ms = [s for s in part.solids]
    return {
        "id": part.name, "part": part.pid, "variant": part.variant, "group": part.group,
        "p3d": "JP\\parts\\%s\\%s.p3d" % (part.group, part.name),
        "build_list": {"entry": part.pid, "variant": var_entry.get("id") if var_entry else None,
                       "differs_by": var_entry.get("differs_by") if var_entry else None,
                       "priority": bl_entry.get("priority") if bl_entry else None,
                       "importance": bl_entry.get("importance") if bl_entry else None,
                       "refs": [r["id"] for r in bl_entry.get("refs", [])] if bl_entry else []},
        "tiers": part.meta.get("tiers"), "used_for": part.meta.get("used_for"), "datum": part.meta.get("datum"),
        "recipe": part.meta.get("recipe"), "deviation": part.meta.get("deviation"),
        "frame": "origin = left post centreline at finished floor/sill level; +x along the wall, +y up, +z exterior; "
                 "autocenter=0 (PLAYBOOK §10.2)",
        "bbox_m": [round(v, 3) for v in part.bbox()],
        "dims": part.dims, "connectors": part.connectors,
        "materials": mats_of(part),
        "lod_faces": counts, "contributes": contributes(lods),
        "walkable": part.walkable,
        "doors": [{"source": ("DoorsTwin%d" % (i + 1)) if getattr(d, "twin", None) else "Doors%d" % (i + 1), "kind": d.kind, "display": d.display,
                   "anims": [{"bone": a["bone"], "type": a["type"], "axis_memory": a["bone"] + "_axis",
                              "amount": round(a["amount"], 4),
                              "unit": "m (translation; axis 1.00 m)" if a["type"] == "translation" else "rad"}
                             for a in d.anims],
                   "anim_period": d.anim_period, "init_opened": d.init_opened, "sound": d.sound,
                   "clear_width_m": None if d.clear is None else round(d.clear, 3),
                   "engine_tested": getattr(d, "engine_tested", True), "note": d.note} for i, d in enumerate(part.doors)],
        "notes": part.notes, "extra": {k: v for k, v in part.meta.items()
                                       if k not in ("tiers", "used_for", "datum", "recipe", "deviation")},
        "checks": [{"check": c, "ok": bool(o), "detail": dt} for c, o, dt in res],
        "made_by": "parts/kit/build_parts.py (parts agent B-PARTS, 2026-09-27)",
    }


def main(argv):
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    t0 = time.time()
    manifest = {"version": 1, "date": "2026-09-27", "author": "parts agent B-PARTS",
                "kit": "japan_dev/parts/kit (python package jpparts; build_parts.py writes everything)",
                "frame": "origin at the left post centreline, finished floor / sill level; +x along the wall, +y up, "
                         "+z exterior; autocenter=0",
                "grid": {"ken_m": core.KEN, "half_ken_m": core.HALF, "trim_m": core.QK},
                "standards": {"post_m": core.POST, "door_head_m": core.DOOR_H, "wall_h_sill_to_keta_m": core.WALL_H,
                              "eave_line_keta_top_m": core.EAVE_Y, "min_door_clear_m": core.MIN_CLEAR},
                "wear": "every material's wear level (_w0/_w1/_w2) is chosen per instance (Part.wear, "
                        "Part.wear_by_mat); samples are written at _w1 unless the variant is a wear variant",
                "parts": []}
    if only and os.path.isfile(os.path.join(DEV, "parts", "manifest.json")):
        old = json.load(open(os.path.join(DEV, "parts", "manifest.json"), encoding="utf-8"))
        manifest["parts"] = [p for p in old.get("parts", []) if not any(o in p["id"] for o in only)]
    groups = {}
    nfail = 0
    for pid, var, fn in registry.ALL:
        name = pid + var
        if only and not any(o in name for o in only):
            continue
        part = fn(var)
        assert part.name == name, (part.name, name)
        path = os.path.join(OUT, part.group, name + ".p3d")
        part.write(path)
        lods = core.mlod.read_mlod(path)
        res, counts = checks.check_part(part, path, lods)
        bl = BLE.get(pid)
        ve = next((v for v in (bl or {}).get("variants", []) if v["id"] in (var, var.lstrip("_"))), None)
        sc = sidecar(part, lods, counts, res, bl, ve)
        wb(os.path.join(OUT, part.group, name + ".part.json"), json.dumps(sc, indent=1, ensure_ascii=False))
        fails = [r for r in res if not r[1]]
        nfail += len(fails)
        groups.setdefault(part.group, []).append({"id": name, "checks": sc["checks"]})
        manifest["parts"].append({k: sc[k] for k in ("id", "part", "variant", "group", "p3d", "build_list", "tiers",
                                                      "used_for", "dims", "connectors", "materials", "lod_faces",
                                                      "contributes", "walkable", "doors", "deviation", "datum",
                                                      "recipe")})
        print("%-4s %-44s %s%s" % ("OK" if not fails else "FAIL", name,
                                   " ".join("%s:%d" % (k.replace("Resolution ", "R").replace(" Geometry", "")[:6], v)
                                            for k, v in counts.items()),
                                   "" if not fails else "\n      " + "\n      ".join("%s: %s" % (c, d) for c, _, d in fails)))
    for g, items in groups.items():
        path = os.path.join(OUT, g, "checks.json")
        prev = []
        if only and os.path.isfile(path):
            prev = [i for i in json.load(open(path, encoding="utf-8"))["parts"] if i["id"] not in {x["id"] for x in items}]
        wb(path, json.dumps({"checks": "C2 C3 C4 C5 C7 (parts/kit/jpparts/checks.py)", "parts": prev + items}, indent=1))
    order = {n: i for i, n in enumerate(p + v for p, v, _ in registry.ALL)}
    manifest["parts"].sort(key=lambda p: order.get(p["id"], 9999))
    wb(os.path.join(DEV, "parts", "manifest.json"), json.dumps(manifest, indent=1, ensure_ascii=False))
    print("%d parts in manifest, %d check failures, %.1f s" % (len(manifest["parts"]), nfail, time.time() - t0))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
