#!/usr/bin/env python3
"""One-off (idempotent): add the palette entries Stephen approved at gate G1 (2026-09-27) to playbook/palette.json.

Values and samples come from research/exterior/materials_needed.json (requested_palette_entries), BUILD_LIST.md.
- earth_wall_aged   : G1 decision 1 (default tier 1-2 exterior wall)
- roof_board_silver : G1 decision 2 (board and stone-weighted roofs)
- kakigara_shell    : G1 decision 3 approves the oyster-shell roof; its colour is 'assumed' until a licensed sample
Re-running changes nothing. Writes with 'wb', LF, same formatting as the file (indent 1, no trailing newline).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
PAL = os.path.join(DEV, "playbook", "palette.json")
REQ = os.path.join(DEV, "research", "exterior", "materials_needed.json")

EXTRA = {
    "earth_wall_aged": {
        "name": "Earthen wall, aged grey-brown (arakabe / nakanuri, exterior)",
        "material": "clay + straw over bamboo lath, weathered",
        "group": "wall", "tiers": [1, 2],
        "use": "default tier 1-2 exterior earth wall (G1 decision 1)",
        "after": "earth_wall_interior", "weathering": None,
    },
    "roof_board_silver": {
        "name": "Weathered roof boards, silver-grey (kureita / kokera)",
        "material": "split sugi / sawara / kuri boards and shingles, sun and rain aged",
        "group": "roof", "tiers": [1, 2, 3],
        "use": "stone-weighted board roofs, shingle roofs, board ridges and pents (G1 decision 2)",
        "after": "kawara_weathered", "weathering": None,
    },
    "kakigara_shell": {
        "name": "Oyster shells on a board roof (kakigara-buki), weathered",
        "material": "oyster shells strewn over thin shingles",
        "group": "roof", "tiers": [3],
        "use": "Edo-side tier-3 board-roof variant (G1 decision 3)",
        "after": "roof_board_silver", "weathering": None,
    },
}


def main():
    raw = open(PAL, "rb").read()
    pal = json.loads(raw)
    req = {e["id"]: e for e in json.load(open(REQ, encoding="utf-8"))["requested_palette_entries"]}
    ids = [e["id"] for e in pal["entries"]]
    added = []
    for pid, meta in EXTRA.items():
        if pid in ids:
            continue
        r = req[pid]
        e = {"id": pid, "name": meta["name"], "material": meta["material"], "group": meta["group"],
             "tiers": meta["tiers"], "use": meta["use"],
             "note": "Added 2026-09-27 by the materials agent after Stephen's G1 approval. Source: "
                     "research/exterior/materials_needed.json (A-EXT). Check: " + r.get("check", "") + " Why: " + r.get("why", ""),
             "srgb": r["srgb"], "hex": "#%02X%02X%02X" % tuple(r["srgb"]), "method": r["method"],
             "tolerance_dE76": r["tolerance_dE76"]}
        if r.get("samples"):
            e["samples"] = [{"ref": s["ref"], "box": s["box"], "select": s["select"]} for s in r["samples"]]
        pos = [e2["id"] for e2 in pal["entries"]].index(meta["after"]) + 1
        pal["entries"].insert(pos, e)
        added.append(pid)
    if added:
        with open(PAL, "wb") as f:
            f.write(json.dumps(pal, indent=1, ensure_ascii=False).encode("utf-8"))
    print("palette entries added:", added or "none (already present)")


if __name__ == "__main__":
    main()
