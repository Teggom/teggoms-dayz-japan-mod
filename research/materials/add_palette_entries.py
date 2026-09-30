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


def _mb(ref, box, value):
    return {"ref": ref, "box": box, "select": "mid 70 % luminance", "value": value}


# B1 (Phase B materials agent, 2026-09-29): the palette entries requested by research/interior/materials_needed.json
# (A2) and research/outdoor_kit/materials_needed.json (A3), accepted at gate G1. Full entries (not from a request file).
B1 = [
    ("earth_road", {
        "id": "doma_earth", "name": "Interior earth floor (doma: tsuchi-doma / tataki), grey-brown",
        "material": "tamped earth; tataki = earth + slaked lime + bittern", "group": "ground", "tiers": [1, 2, 3],
        "use": "doma floors and tori-niwa (jp_m_ground_doma_earth, jp_m_ground_doma_tataki)",
        "note": "Added 2026-09-29 by B1. G1 asked for a re-sample before building. A2's two boxes disagreed widely "
                "(sunlit Kasuya 188,181,170 vs shaded Tsunashima 85,85,86). Re-sample: a third photo (i05, the lit "
                "part of the Tsunashima doma, 120,120,119) and a second, diffuse-lit Kasuya box (153,142,138); a "
                "shadowed Kasuya box (91,86,80), a deep-shade Tsunashima box (61,61,63) and the ash-covered, blue-cast "
                "i22 floor (132,143,161) were rejected. Value = mean of the 4 kept per-box medians: it confirms A2's "
                "request (136,133,128), dE 0.7. Neutral grey with a slight warm cast (a* ~1, b* ~3). Vanilla dirt "
                "floors measure 76-127 (tisybase_dirt_1 127,122,113), so the doma sits at the bright end of vanilla; "
                "judge in game. Images: data/research_int/refs (research/interior/refs_index.json).",
        "srgb": [137, 132, 128], "method": "sampled", "tolerance_dE76": 14,
        "samples": [_mb("i02_kasuya_kamado", [0.62, 0.72, 0.95, 0.95], [188, 181, 170]),
                    _mb("i02_kasuya_kamado", [0.0, 0.8, 0.35, 1.0], [153, 142, 138]),
                    _mb("i05_tsunashima_kamado", [0.62, 0.72, 0.98, 0.95], [120, 120, 119]),
                    _mb("i06_tsunashima_doma", [0.05, 0.72, 0.4, 0.95], [85, 85, 86])]}),
    ("doma_earth", {
        "id": "ash_grey", "name": "Hearth ash (irori bed, hibachi)", "material": "wood ash, raked", "group": "ground",
        "tiers": [1, 2, 3], "use": "irori ash beds, hibachi ash (jp_m_ground_ash)",
        "note": "Added 2026-09-29 by B1. Kept ASSUMED: the two usable ash beds sit under opposite colour casts - "
                "i01 Kasuya (warm spotlight, 211,173,133) and i04 Tsunashima (cool daylight / fire, 133,140,147); "
                "their mean (172,157,140) is dE ~8 from this value, inside tolerance, and would read brighter than "
                "vanilla white walls (~150). i03 is too dark to use (35-57).",
        "srgb": [150, 146, 140], "method": "assumed", "tolerance_dE76": 12,
        "samples": [_mb("i01_kasuya_irori", [0.34, 0.73, 0.42, 0.86], [213, 173, 133]),
                    _mb("i04_tsunashima_irori", [0.17, 0.26, 0.3, 0.4], [133, 140, 147])]}),
    ("thatch_new", {
        "id": "straw_aged", "name": "Rice straw, one season old (rope, stacks, bundles)",
        "material": "rice straw (wara)", "group": "roof", "tiers": [1, 2, 3],
        "use": "straw rope, stacks and bundles (jp_m_straw_rope, jp_m_straw_stack); _w0 of both uses thatch_new",
        "note": "Added 2026-09-29 by B1 from research/outdoor_kit/materials_needed.json (A3): an October photo of "
                "rice straw (PD). Lighter and warmer than thatch_weathered, greyer than thatch_new.",
        "srgb": [97, 83, 62], "method": "sampled", "tolerance_dE76": 14,
        "samples": [_mb("k34_straw_rice", [0.3, 0.35, 0.7, 0.75], [97, 83, 62])]}),
    ("moss_on_stone", {
        "id": "leaf_litter_autumn", "name": "Autumn leaf litter (mixed broadleaf, damp)",
        "material": "fallen maple / zelkova / ginkgo leaves", "group": "ground", "tiers": [1, 2, 3],
        "use": "the abandoned layer in gutters, tubs, basins, steps (jp_m_ground_leaf_litter)",
        "note": "Added 2026-09-29 by B1. A3 requested (96,70,46) as assumed until a licensed sample; sampled here "
                "from the CC0 Poly Haven scan dry_decay_leaves (Amal Kumar, the material's own source), median of "
                "the mid-70 % luminance pixels. dE ~8 from A3's guess.",
        "srgb": [112, 76, 52], "method": "sampled", "tolerance_dE76": 14,
        "samples": [{"ref": "polyhaven:dry_decay_leaves (diff 1k)", "box": [0, 0, 1, 1], "select": "mid 70 % luminance",
                     "value": [112, 76, 52]}]}),
    ("iron_black", {
        "id": "stoneware_pale", "name": "Pale ash-glazed stoneware", "material": "stoneware, ash / feldspathic glaze",
        "group": "ceramic", "tiers": [1, 2, 3],
        "use": "bowls, bottles, round hibachi, lamp dishes (jp_m_ceramic_stoneware_pale)",
        "note": "Added 2026-09-29 by B1 from research/interior/materials_needed.json (A2): The Met 666591 (CC0), a "
                "tokkuri of 1700-1750, studio light.",
        "srgb": [168, 149, 115], "method": "sampled", "tolerance_dE76": 14,
        "samples": [_mb("i50_met_tokkuri_stoneware", [0.35, 0.4, 0.65, 0.7], [168, 149, 115])]}),
    ("stoneware_pale", {
        "id": "stoneware_dark", "name": "Iron-brown glazed stoneware (kitchen jars)",
        "material": "stoneware, iron (tetsu-yu / ame) glaze", "group": "ceramic", "tiers": [1, 2, 3],
        "use": "water jars, storage jars, privy jar (jp_m_ceramic_stoneware_dark)",
        "note": "Added 2026-09-29 by B1 from A2. ASSUMED: still no licensed photo of an Edo-period iron-glazed "
                "jar (Tamba / Seto kitchen ware); upgrade when one is found.",
        "srgb": [74, 52, 38], "method": "assumed", "tolerance_dE76": 12, "samples": []}),
]


def add_b1(pal):
    added = []
    for after, e in B1:
        if e["id"] in [x["id"] for x in pal["entries"]]:
            continue
        e = dict(e)
        e["hex"] = "#%02X%02X%02X" % tuple(e["srgb"])
        pos = [x["id"] for x in pal["entries"]].index(after) + 1
        pal["entries"].insert(pos, e)
        added.append(e["id"])
    return added


def main():
    raw = open(PAL, "rb").read()
    pal = json.loads(raw)
    req = {e["id"]: e for e in json.load(open(REQ, encoding="utf-8"))["requested_palette_entries"]}
    ids = [e["id"] for e in pal["entries"]]
    added = add_b1(pal)
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
