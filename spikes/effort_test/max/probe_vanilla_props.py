"""Print the named-property strings (autocenter, class, map, damage, ...) and rvmat/texture paths found in a few
vanilla furniture ODOL p3ds (read-only probe; ODOL stores properties as asciiz key/value pairs)."""
import re
import sys

FILES = [r"P:\DZ\structures\furniture\cases\case_bedroom_a\case_bedroom_a.p3d",
         r"P:\DZ\structures\furniture\cases\case_d\case_d.p3d",
         r"P:\DZ\structures\furniture\various\chest_dz.p3d",
         r"P:\DZ\structures\furniture\tables\table_drawer\table_drawer.p3d",
         r"P:\DZ\structures\furniture\cases\paperbox\paperbox_01_small_ransacked.p3d"]
KEYS = {"autocenter", "class", "map", "damage", "dammage", "lodnoshadow", "buoyancy", "canbeoccluded",
        "canocclude", "placement", "keyframe", "forcenotalpha", "sbsource", "prefershadowvolume", "shadowoffset",
        "frequent", "viewclass", "xcount", "ycount", "zcount", "aicovers"}
for f in FILES:
    try:
        data = open(f, "rb").read()
    except OSError as e:
        print(f, e)
        continue
    strs = [m.group().decode("latin-1") for m in re.finditer(rb"[\x20-\x7e]{3,}", data)]
    print("==", f, len(data), "bytes, magic", data[:4], "version", int.from_bytes(data[4:8], "little"))
    for i, s in enumerate(strs):
        if s.lower() in KEYS:
            print("   prop %s = %s" % (s, strs[i + 1] if i + 1 < len(strs) else "?"))
    mats = sorted({s for s in strs if s.lower().endswith((".rvmat", ".paa"))})
    for m in mats[:30]:
        print("   ", m)
