"""W2F: write the W2F section of spikes/SH1/SHOWCASE_MAP.md from spikes/W2F/w2f_items.json (between markers; the SH1
sections are left as they are). python spikes/W2F/map_md.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
MD = os.path.join(DEV, "spikes", "SH1", "SHOWCASE_MAP.md")
A, B = "<!-- W2F BEGIN -->", "<!-- W2F END -->"
AREAS = [("P", "Town shrine precinct (map w2f_map_precinct.jpg): the SH1 hall site + west of the approach"),
         ("V", "Village shrine north of the C2 hamlet (map w2f_map_village.jpg)"),
         ("T", "Village temple, Jodo, west of the graveyard (map w2f_map_village.jpg)"),
         ("U", "Town temple, Zen, east of the street end (map w2f_map_east.jpg)"),
         ("K", "Civic set at both street ends (maps w2f_map_east.jpg = K1-K4, w2f_map_village.jpg = K5-K7)")]


def main():
    with open(os.path.join(HERE, "w2f_items.json"), "rb") as f:
        items = json.loads(f.read().decode("utf-8"))
    out = [A, "", "## W2F wave 2: furnished shrine, temples and civic buildings (agent W2F, 2026-10-01)", "",
           "Regenerate: `python spikes/W2F/layout_w2f.py` then `python spikes/W2F/map_md.py`. Buildings are the "
           "furnished variants (`buildings/w2f_sets.py`); `.sN` = a site object that belongs to that building; `t` = "
           "the stone terrace under it. y_off is over the ground at the object.", ""]
    for code, title in AREAS:
        out += ["### %s" % title, "", "| ID | Class / p3d | x | z | yaw | y_off | What |", "|---|---|---|---|---|---|---|"]
        for it in items:
            if it["area"] != code:
                continue
            name = it["class"] or os.path.basename(it["p3d"])
            out.append("| %s | `%s` | %.2f | %.2f | %.0f | %.2f | %s |" % (it["id"], name, it["x"], it["z"], it["yaw"],
                                                                         it["y_off"], it["label"]))
        out.append("")
    out.append(B)
    with open(MD, "rb") as f:
        s = f.read().decode("utf-8")
    block = "\n".join(out)
    if A in s:
        s = s[:s.index(A)] + block + s[s.index(B) + len(B):]
    else:
        s = s.rstrip("\n") + "\n\n" + block + "\n"
    with open(MD, "wb") as f:
        f.write(s.encode("utf-8"))
    print("SHOWCASE_MAP.md: W2F section, %d rows" % len(items))


if __name__ == "__main__":
    main()
