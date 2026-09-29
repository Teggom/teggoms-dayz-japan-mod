"""Download the interior reference images into data/research_int/refs/ and write data/research_int/meta.json
(the download log that gen_build_list.py turns into refs_index.json and CREDITS.md).

Commons: resolved through the API at <= 1600 px wide; licence re-checked (PD / CC0 / CC BY only, never SA/NC/ND).
Met: object record re-checked for isPublicDomain; primaryImageSmall is downloaded. One Met call per 3 s.
User-Agent is exactly the project tag (README rule 4). Skips files already on disk.
Run: python research/interior/tools/fetch_int_refs.py        Research agent PA2, 2026-09-29.
"""
import json, os, re, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from int_search import UA, info, ok_licence  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "research_int", "refs")
META = os.path.join(ROOT, "data", "research_int", "meta.json")
MOR = "File:『和国諸職絵尽 諸織 絵本鏡』-A Picture Book Mirror of Various Occupations (Wakoku shoshoku ezukushi) MET 2013 786 a c a 0%d.jpg"

COMMONS = [
    ("i01_kasuya_irori", "File:Former Kasuya Family House irori 2025-11-03.jpg"),
    ("i02_kasuya_kamado", "File:Former Kasuya Family House kamado 2025-11-03.jpg"),
    ("i03_tenmyo_irori", "File:Farmhouse of Tenmyo Family 20130323-01.jpg"),
    ("i04_tsunashima_irori", "File:Farmhouse of Tsunashima Family 20130323-03.jpg"),
    ("i05_tsunashima_kamado", "File:Farmhouse of Tsunashima Family 20130323-02.jpg"),
    ("i06_tsunashima_doma", "File:Farmhouse of Tsunashima Family 20130323-06.jpg"),
    ("i07_edo_nagaya_room", "File:Japanese Edo Nagaya.jpg"),
    ("i08_edo_nagaya_kitchen", "File:Edo Kamado.JPG"),
    ("i09_edo_nagaya_hibachi", "File:Edo Hibachi.JPG"),
    ("i10_hearth_boards", "File:Japanese Traditional Hearth L4817.jpg"),
    ("i11_kamado_plastered", "File:Kamado-M1685.jpg"),
    ("i12_tsubaki_honjin", "File:Koriyamajuku Tsubakihonjin in Ibaraki City Osaka04-r.jpg"),
    ("i13_echigoya_1768", "File:Interior in Mitsui Echigoya at Suruga-chō.jpg"),
    # i14 dropped: same file as the exterior x33_jinrin_bookseller_1690
    ("i15_moronobu_1685_p5", MOR % 5),
    ("i16_moronobu_1685_p6", MOR % 6),
    ("i17_moronobu_1685_p7", MOR % 7),
    ("i18_moronobu_1685_p9", MOR % 9),
    ("i19_moronobu_tub", "File:Hishikawa Buch.jpg"),
    ("i20_hachioji_kamado", "File:House of Leader of Hachioji Guards 20120323-05.jpg"),
    ("i21_jizai_kettle", "File:Hanging kettle in Japan.jpg"),
    ("i22_kamado_firewood", "File:Kamado (26736484990).jpg"),
    ("i23_kendan_tokonoma", "File:Alcove of Kendan Yashiki.jpg"),
    ("i24_hida_farmhouse", "File:Hida Folk Village - HidaFolkVillage6453.jpg"),
    ("i30_morse_kitchen_farmhouse", "File:JapanHomes 167 Kitchen in old farmhouse at Kabutoyama.jpg"),
    ("i31_morse_kitchen_range", "File:JapanHomes 168 Kitchen range.jpg"),
    ("i32_morse_city_kitchen", "File:JapanHomes 170 Kitchen in city house.jpg"),
    ("i33_morse_jizai", "File:JapanHomes 173 Ji-zai.jpg"),
    ("i34_morse_fireplace_country", "File:JapanHomes 174 Fireplace in country house.jpg"),
    ("i35_morse_kitchen_closet", "File:JapanHomes 177 Kitchen closet, drawers, cupboard, and stairs combined.jpg"),
    ("i36_morse_hibachi", "File:JapanHomes 197 Common hibachi.jpg"),
    ("i37_morse_hibachi_wood", "File:JapanHomes 198 Hibachi.jpg"),
    ("i38_morse_tabakobon", "File:JapanHomes 201 Tabako-bon.jpg"),
    ("i39_morse_andon", "File:JapanHomes 206 Lamp.jpg"),
    ("i40_morse_andon2", "File:JapanHomes 207 Lamp.jpg"),
    ("i41_morse_ceiling", "File:JapanHomes019 SECTION OF CEILING.jpg"),
    ("i42_morse_guestroom_hachiishi", "File:JapanHomes096 GUEST-ROOM AT HACHI-ISHI.jpg"),
    ("i43_morse_guestroom", "File:JapanHomes119 GUEST-ROOM.jpg"),
    ("i44_morse_country_guestroom", "File:JapanHomes128 GUEST-ROOM OF A COUNTRY HOUSE.jpg"),
]
MET = [
    ("i50_met_tokkuri_stoneware", 666591),
    ("i51_met_tokkuri_porcelain", 50328),
]


def strip(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    meta = json.load(open(META, encoding="utf-8")) if os.path.exists(META) else {}
    titles = [t for _, t in COMMONS]
    rows = {}
    for k in range(0, len(titles), 40):
        d = requests.get("https://commons.wikimedia.org/w/api.php", headers={"User-Agent": UA}, timeout=40, params={
            "action": "query", "format": "json", "titles": "|".join(titles[k:k + 40]), "prop": "imageinfo",
            "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 1600}).json()
        norm = {n["to"]: n["from"] for n in d.get("query", {}).get("normalized", [])}
        for p in d.get("query", {}).get("pages", {}).values():
            rows[norm.get(p["title"], p["title"])] = p
    for rid, title in COMMONS:
        path = os.path.join(OUT, rid + ".jpg")
        p = rows.get(title)
        if not p or "imageinfo" not in p:
            print("MISSING", rid, title)
            continue
        ii = p["imageinfo"][0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not ok_licence(lic):
            print("LICENCE REFUSED", rid, lic)
            continue
        if not os.path.exists(path):
            url = ii.get("thumburl") or ii["url"]
            b = requests.get(url, headers={"User-Agent": UA}, timeout=60).content
            open(path, "wb").write(b)
            time.sleep(1.0)
        meta[rid] = {"id": rid, "file": "data/research_int/refs/%s.jpg" % rid, "source": "Wikimedia Commons",
                     "title": title, "page_url": ii.get("descriptionurl", ""), "licence": lic,
                     "author": strip(md.get("Artist", {}).get("value", ""))[:80],
                     "date": strip(md.get("DateTimeOriginal", {}).get("value", ""))[:40],
                     "bytes": os.path.getsize(path)}
        print("ok", rid, lic)
    for rid, oid in MET:
        path = os.path.join(OUT, rid + ".jpg")
        time.sleep(3.0)
        o = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects/%d" % oid,
                         headers={"User-Agent": UA}, timeout=40).json()
        if not o.get("isPublicDomain"):
            print("NOT PD", rid)
            continue
        if not os.path.exists(path):
            time.sleep(3.0)
            open(path, "wb").write(requests.get(o["primaryImageSmall"], headers={"User-Agent": UA}, timeout=60).content)
        meta[rid] = {"id": rid, "file": "data/research_int/refs/%s.jpg" % rid, "source": "The Met Open Access",
                     "title": o.get("title", ""), "page_url": o.get("objectURL", ""), "licence": "CC0 (Met Open Access, public domain)",
                     "author": o.get("artistDisplayName", "") or o.get("culture", ""), "date": o.get("objectDate", ""),
                     "medium": o.get("medium", ""), "dimensions": o.get("dimensions", ""), "bytes": os.path.getsize(path)}
        print("ok", rid)
    open(META, "wb").write((json.dumps(meta, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print("meta", len(meta))


if __name__ == "__main__":
    main()
