"""Print sidecar notes / frames and per-model extra keys for a folder of prop sidecars."""
import json, sys, os, glob
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
folder = sys.argv[1]
keys = sys.argv[2].split(",") if len(sys.argv) > 2 else []
for p in sorted(glob.glob(os.path.join(DEV, folder, "*.prop.json"))):
    d = json.loads(open(p, "rb").read().decode("utf-8"))
    print("==", os.path.basename(p), "frame:", d.get("frame"))
    print("  notes:", d.get("notes"))
    for m in d["models"]:
        ex = {k: v for k, v in m.items() if k in keys}
        print("   ", os.path.basename(m["p3d"]), ex)
