"""Search Wikimedia Commons for candidate reference photos and list only PD / CC0 / CC-BY files.

Usage: python commons_search.py "query one" "query two" ...
Prints: title | licence | WxH | artist | url. Nothing is downloaded here.
"""
import sys, time, json, re
import requests

UA = "JapanDevPlaybook/0.1 (DayZ mod period-reference research; low volume; python-requests)"
API = "https://commons.wikimedia.org/w/api.php"
OK = re.compile(r"^(public domain|pd\b|pd-|cc0|cc by \d|cc-by-\d|cc by-\d|attribution)", re.I)
BAD = re.compile(r"sa|nc|nd", re.I)


def ok_licence(short):
    s = (short or "").strip()
    if not s:
        return False
    low = s.lower()
    if low.startswith("public domain") or low.startswith("pd") or low.startswith("cc0"):
        return True
    if low.startswith("cc by") or low.startswith("cc-by"):
        tail = low.replace("cc-by", "").replace("cc by", "")
        return not re.search(r"\b(sa|nc|nd)\b|-sa|-nc|-nd", tail)
    return False


def get(params):
    params = dict(params, format="json")
    for attempt in range(5):
        r = requests.get(API, params=params, headers={"User-Agent": UA}, timeout=30)
        if r.status_code == 429:
            wait = int(r.headers.get("retry-after", "10"))
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limited")


def search(q, limit=25):
    d = get({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6,
             "gsrlimit": limit, "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
             "iiurlwidth": 1600})
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if not ok_licence(lic):
            continue
        if not ii.get("mime", "").startswith("image/jpeg"):
            continue
        artist = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:40]
        date = re.sub(r"<[^>]+>", "", md.get("DateTimeOriginal", {}).get("value", ""))[:20]
        out.append((p["title"], lic, "%dx%d" % (ii.get("width", 0), ii.get("height", 0)), artist, date,
                    ii.get("thumburl", ii.get("url"))))
    return out


if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("=== %s" % q)
        for row in search(q)[:10]:
            print(" | ".join(row[:5]))
        time.sleep(1.5)
