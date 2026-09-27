"""Download the playbook reference images (<= 30) into data/playbook/refs/ and write refs_images.json.

Commons: files resolved through the API at 1600 px wide; licence re-checked (PD / CC0 / CC BY only).
Met: object records re-checked for isPublicDomain; primaryImageSmall is downloaded. One Met call per 3 s.
Run from anywhere: python fetch_refs.py
"""
import json, os, re, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))           # japan_dev
OUT = os.path.join(ROOT, "data", "playbook", "refs")
UA = "JapanDevPlaybook/0.1 (DayZ mod period-reference research; low volume; python-requests)"

COMMONS = [
    # (local id, Commons title, what it supports)
    ("c01_narai_street", "File:Narai-juku - Naraijuku6558.jpg", "Nakasendo post town: aged timber facades, board eaves, dashigeta"),
    ("c02_narai_facade", "File:Narai-juku - Naraijuku6579.jpg", "Nakasendo post town: timber colour, lattice, low upper storey"),
    ("c03_tsumago_street", "File:Looking down the Nakasendō in the central part of the village, Tsumago-juku, Nagiso, 2016.jpg", "Post town streetscape, board roofs, weathered sugi"),
    ("c04_tsumago_wakihonjin", "File:Entry to the Waki-Honjin, Tsumago-juku, Nagiso, 2016.jpg", "Waki-honjin gate/entry, dark timber"),
    ("c05_ouchi_thatch", "File:Ouchi-juku, Fukushima 01.jpg", "Thatched post town (Aizu): thatch colour, hip roofs"),
    ("c06_shirakawa_gassho", "File:Historic Village of Shirakawa-go (2016) - img 01.jpg", "Gassho thatch, steep pitch"),
    ("c07_gion_machiya", "File:150124 Gion Kyoto Japan01s3.jpg", "Kyoto machiya: bengara koshi, kawara, low upper storey"),
    ("c08_kyomachiya", "File:Kyō-machiya 01.JPG", "Kyoto machiya: mushiko-mado, plaster upper storey, sangawara"),
    ("c09_himeji", "File:Himeji - Himeji357.jpg", "Castle: shikkui white, ishigaki granite, ibushi kawara"),
    ("c10_inari_torii", "File:20181110 Fushimi Inari Torii 1.jpg", "Shu vermilion + sumi black on torii"),
    ("c11_kurashiki", "File:Kurashikikahan17nt3200.jpg", "Kura: namako-kabe, black/white plaster"),
    ("c12_higashi_chaya", "File:Higashi Chaya District (50153812728).jpg", "Bengara lattice, 1820 chaya district (later than window, colour only)"),
    ("c14_minkaen_b", "File:Nihon Minka-en 11.jpg", "Edo-period farmhouse (open-air museum)"),
    ("c15_farmhouse_interior", "File:Japanese traditional farmhouse - wooden floor and mud wall - 4373467409.jpg", "Farmhouse interior: board floor, earthen wall"),
    ("c16_hakone_sekisho", "File:Hakone Sekisho July 2018.jpg", "Reconstructed Hakone checkpoint (2007 rebuild from 1865 plans)"),
    ("c17_ichirizuka", "File:Koganei Ichirizuka, Tochigi.jpg", "Surviving ichirizuka milestone mound"),
    ("c18_hiroshige_mariko", "File:Hiroshige-53-Stations-Hoeido-21-Mariko-MFA-03.jpg", "Roadside tea house, thatch, travellers' dress (c.1833)"),
    ("c20_minkaen_c", "File:Nihon Minka-en 27.jpg", "Edo-period farmhouse (open-air museum)"),
    ("c21_tatami", "File:Tatami-detail-1.jpg", "Tatami omote weave and heri edge, colour"),
    ("c22_kasuga_lanterns", "File:Nara Kasuga-taisha Lanterns 03.jpg", "Stone toro (Kasuga type), weathered granite + moss"),
    ("c23_fukiya_katayama", "File:Fukiya katayama house03s3200.jpg", "Bengara maker's house (Fukiya): bengara lattice, Sekishu red tiles"),
    ("c24_jizo_cemetery", "File:Japan, Jizo statues at cemetery 1.jpg", "Jizo and grave stones, weathered stone"),
    ("c25_tsuijibei", "File:Kannon-ji Tsuijibei.JPG", "Tile-course clay wall (neribei type) with tile cap: wall type + weathered kawara"),
    ("c26_morse_tile_ridge", "File:JapanHomes067 RIDGE OF TILED ROOF.jpg", "Morse 1885: tiled ridge build-up (noshi courses)"),
    ("c27_morse_thatch_ridge", "File:JapanHomes082 BAMBOO RIDGE OF THATCHED ROOF IN MUSASHI.jpg", "Morse 1885: thatch ridge treatment"),
    ("c28_morse_country_inn", "File:JapanHomes039 COUNTRY INN IN RIKUZEN.jpg", "Morse 1885: country inn (hatago) elevation"),
    ("c29_earthen_wall", "File:Wall - Hōryū-ji - Ikaruga, Nara, Japan - DSC07605.jpg", "Tile-capped earthen wall (tsuijibei), earth ochre colour"),
]

MET = [
    ("m01_sashiko_jacket", 50805, "Aizome indigo on working cotton (sashiko)"),
    ("m02_indigo_piece", 70748, "Aizome indigo cotton, dark/light shades"),
    ("m03_kosode_stencil", 61840, "Stencil-dyed kosode, 18th-19th c."),
]


def ok_licence(short):
    low = (short or "").strip().lower()
    if low.startswith("public domain") or low.startswith("pd") or low.startswith("cc0"):
        return True
    if low.startswith("cc by") or low.startswith("cc-by"):
        tail = low.replace("cc-by", "").replace("cc by", "")
        return not re.search(r"\b(sa|nc|nd)\b|-sa|-nc|-nd", tail)
    return False


def http_get(url, params=None, pause=0.0):
    for _ in range(6):
        time.sleep(pause)
        r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=60)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("retry-after", "15")))
            continue
        r.raise_for_status()
        return r
    raise RuntimeError("429 loop on " + url)


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for lid, title, supports in COMMONS:
        path = os.path.join(OUT, lid + ".jpg")
        d = http_get("https://commons.wikimedia.org/w/api.php", {
            "action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata|size",
            "iiurlwidth": 1600, "format": "json"}, pause=1.0).json()
        page = list(d["query"]["pages"].values())[0]
        ii = page["imageinfo"][0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not ok_licence(lic):
            print("SKIP licence", lid, lic)
            continue
        artist = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()
        date = re.sub(r"<[^>]+>", "", md.get("DateTimeOriginal", {}).get("value", "")).strip()
        if not os.path.exists(path):
            img = http_get(ii.get("thumburl") or ii["url"], pause=6.0).content
            with open(path, "wb") as f:
                f.write(img)
        index.append({"id": lid, "file": "data/playbook/refs/%s.jpg" % lid, "source": "Wikimedia Commons",
                      "title": title, "page_url": ii.get("descriptionurl", ""), "licence": lic,
                      "author": artist[:120], "date": date[:40], "supports": supports})
        print("ok", lid, lic)
    for lid, oid, supports in MET:
        path = os.path.join(OUT, lid + ".jpg")
        o = http_get("https://collectionapi.metmuseum.org/public/collection/v1/objects/%d" % oid, pause=3.0).json()
        if not o.get("isPublicDomain"):
            print("SKIP not PD", lid)
            continue
        if not os.path.exists(path):
            img = http_get(o["primaryImageSmall"], pause=1.0).content
            with open(path, "wb") as f:
                f.write(img)
        index.append({"id": lid, "file": "data/playbook/refs/%s.jpg" % lid, "source": "The Met Open Access",
                      "title": o.get("title", ""), "page_url": o.get("objectURL", ""), "licence": "CC0 (Met Open Access)",
                      "author": o.get("artistDisplayName", ""), "date": o.get("objectDate", ""),
                      "medium": o.get("medium", ""), "supports": supports})
        print("ok", lid)
    with open(os.path.join(OUT, "..", "refs_images.json"), "wb") as f:
        f.write(json.dumps(index, indent=1, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
