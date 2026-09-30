"""Which types.xml entries can spawn on the test island (nominal > 0), and which of them fit the pilot's containers
(tag shelves / floor, category tools / containers / clothes / food, usage Town)."""
import re, os
DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
d = open(os.path.join(DEV, "mission", "japantest.japantestisland", "db", "types.xml"), encoding="utf-8",
         errors="replace").read()
ts = re.findall(r'<type name="([^"]+)">(.*?)</type>', d, re.S)
live = [(n, b) for n, b in ts if re.search(r"<nominal>([1-9]\d*)</nominal>", b)]
print(len(ts), "types,", len(live), "with nominal > 0")
cats = {"tools", "containers", "clothes", "food"}
for n, b in live:
    tags = re.findall(r'<tag name="(\w+)"', b)
    us = re.findall(r'<usage name="(\w+)"', b)
    cs = re.findall(r'<category name="(\w+)"', b)
    nom = re.search(r"<nominal>(\d+)</nominal>", b).group(1)
    fits = bool(set(cs) & cats) and ("Town" in us or not us)
    print("%-28s nom %s tags %s usage %s cat %s %s" % (n, nom, tags, us, cs, "FITS" if fits else ""))
