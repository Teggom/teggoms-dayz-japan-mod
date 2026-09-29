"""Search Wikimedia Commons (and list a category) for PD / CC0 / CC BY reference images; optionally build a numbered
contact sheet of the hits so they can be judged by eye in one look.

Usage:
  python int_search.py search "query" [...]            -> prints title | licence | size | artist | date
  python int_search.py cat "Category:Name" [limit]      -> same, for the files of a category
  python int_search.py sheet OUT.jpg "File:A.jpg" ...    -> downloads 300 px thumbs, numbered contact sheet

User-Agent is exactly the project tag (README rule 4: no personal information in any request).
Research agent PA2, 2026-09-29.
"""
import io, re, sys, time
import requests

UA = "JapanDevResearch/1.0 (DayZ mod research)"
API = "https://commons.wikimedia.org/w/api.php"


def ok_licence(short):
    low = (short or "").strip().lower()
    if low.startswith("public domain") or low.startswith("pd") or low.startswith("cc0"):
        return True
    if low.startswith("cc by") or low.startswith("cc-by"):
        tail = low.replace("cc-by", "").replace("cc by", "")
        return not re.search(r"\b(sa|nc|nd)\b|-sa|-nc|-nd", tail)
    return False


def get(params):
    params = dict(params, format="json")
    for _ in range(6):
        r = requests.get(API, params=params, headers={"User-Agent": UA}, timeout=40)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("retry-after", "10")))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limited")


def rows(d, width=1600):
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not ok_licence(lic) or not ii.get("mime", "").startswith("image/"):
            continue
        artist = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:40].strip()
        date = re.sub(r"<[^>]+>", "", md.get("DateTimeOriginal", {}).get("value", ""))[:24].strip()
        desc = re.sub(r"<[^>]+>", "", md.get("ImageDescription", {}).get("value", ""))[:90].strip().replace("\n", " ")
        out.append({"title": p["title"], "licence": lic, "size": "%dx%d" % (ii.get("width", 0), ii.get("height", 0)),
                    "artist": artist, "date": date, "desc": desc, "thumb": ii.get("thumburl", ii.get("url")),
                    "page": ii.get("descriptionurl", "")})
    return out


IIPROP = {"prop": "imageinfo", "iiprop": "url|extmetadata|size|mime"}


def search(q, limit=30, width=1600):
    return rows(get(dict(IIPROP, action="query", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=limit,
                         iiurlwidth=width)))


def category(cat, limit=200, width=1600):
    return rows(get(dict(IIPROP, action="query", generator="categorymembers", gcmtitle=cat, gcmtype="file",
                         gcmlimit=limit, iiurlwidth=width)))


def info(titles, width=1600):
    return rows(get(dict(IIPROP, action="query", titles="|".join(titles), iiurlwidth=width)))


def sheet(out, titles):
    from PIL import Image, ImageDraw
    res = []
    for k in range(0, len(titles), 40):
        res += info(titles[k:k + 40], width=300)
    order = {t: i for i, t in enumerate(titles)}
    res.sort(key=lambda r: order.get(r["title"], 999))
    cols, cw, ch = 6, 300, 250
    img = Image.new("RGB", (cols * cw, ((len(res) + cols - 1) // cols) * ch), "white")
    dr = ImageDraw.Draw(img)
    for i, r in enumerate(res):
        try:
            b = requests.get(r["thumb"], headers={"User-Agent": UA}, timeout=40).content
            t = Image.open(io.BytesIO(b)).convert("RGB")
            t.thumbnail((cw - 6, ch - 26))
            x, y = (i % cols) * cw, (i // cols) * ch
            img.paste(t, (x + 3, y + 3))
            dr.rectangle([x + 3, y + ch - 22, x + cw - 3, y + ch - 2], fill="black")
            dr.text((x + 6, y + ch - 20), "%d %s" % (order.get(r["title"], -1), r["title"][5:40]), fill="white")
        except Exception as ex:  # noqa: BLE001
            print("thumb failed", r["title"], ex)
        time.sleep(0.5)
    img.save(out, quality=85)
    print("sheet", out, len(res), "images (licence-checked)")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "sheet":
        sheet(sys.argv[2], sys.argv[3:])
        sys.exit(0)
    if mode == "cat":
        lim = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        for r in category(sys.argv[2], lim):
            print(" | ".join([r["title"], r["licence"], r["size"], r["artist"], r["date"], r["desc"]]))
        sys.exit(0)
    for q in sys.argv[2:]:
        print("=== %s" % q)
        for r in search(q)[:15]:
            print(" | ".join([r["title"], r["licence"], r["size"], r["artist"], r["date"], r["desc"][:60]]))
        time.sleep(1.5)
