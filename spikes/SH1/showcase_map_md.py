"""Write spikes/SH1/SHOWCASE_MAP.md: every showcase ID -> class -> world position -> what it is (from
showcase_items.json and the street table in map_labels.py). Classes: the config class of each prop (StaticObj_JP_*);
vanilla trees have none (p3d given).

  python spikes/SH1/showcase_map_md.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import map_labels  # noqa: E402

items = json.load(open(os.path.join(HERE, "showcase_items.json"), encoding="utf-8"))
L = ["# SH1 showcase map: ID -> class -> position", "",
     "Resolve any ID Stephen names (TEST_CHECKLIST.md, the maps `research/production/contact_sheets/sh1_map_*.jpg`).",
     "Positions are world metres (x east, z north), y_offset over the ground; yaw clockwise from north (180 = faces south).",
     "Regenerate: `python spikes/SH1/layout_sh1.py` then `python spikes/SH1/showcase_map_md.py`.", "",
     "## Street (map sh1_map_street.jpg)", "", "| ID | What | x | z |", "|---|---|---|---|"]
cls = {"D1": "Land_JP_Townhouse_Edo_3ken_Middle_ToriL_Kanamono", "D2": "Land_JP_Townhouse_Kamigata_2ken_Middle_ToriR_Tabako",
       "D3": "Land_JP_Townhouse_Kamigata_3ken_EndR_ToriL_Mochiya", "D4": "Land_JP_Townhouse_Edo_3ken_EndL_ToriL_Kusuri",
       "D5": "Land_JP_Townhouse_Edo_2ken_Middle_ToriR_Board_Shitate",
       "D6": "Land_JP_Townhouse_Kamigata_3ken_Middle_ToriL_Kyo_Ningyo"}
for i, lab, x, z in map_labels.STREET:
    L.append("| %s | %s%s | %.1f | %.1f |" % (i, lab, (" `%s`" % cls[i]) if i in cls else "", x, z))
titles = {"shrine": "Shrine (map sh1_map_shrine.jpg; K = hill-stair modules, I = Inari-stair modules)",
          "graveyard": "Graveyard (map sh1_map_graveyard.jpg; G<row>-<col>, row 1 = south / front, col 1 = west; s/t/i = slats / flower tubes / incense of that grave)",
          "gallery": "Life-layer gallery (map sh1_map_gallery.jpg; L<n> = LIFE_LAYER.md item n; LS = shed, LH = host prop)"}
for area in ("shrine", "graveyard", "gallery"):
    L += ["", "## " + titles[area], "", "| ID | Class | x | z | yaw | y_off | What |", "|---|---|---|---|---|---|---|"]
    for it in items:
        if it["area"] != area:
            continue
        c = it["class"] or it["p3d"]
        L.append("| %s | `%s` | %.2f | %.2f | %.0f | %.2f | %s |" % (it["id"], c, it["x"], it["z"], it["yaw"],
                                                                   it["y_offset"], it["label"].strip().replace("|", "/")))
with open(os.path.join(HERE, "SHOWCASE_MAP.md"), "wb") as f:
    f.write(("\n".join(L) + "\n").encode("utf-8"))
print("SHOWCASE_MAP.md", len(L), "lines")
