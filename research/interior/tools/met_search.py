"""Search The Met Open Access API for public-domain Japanese objects with images (one request per 3 s).

Usage: python met_search.py N "query" ...   (N = objects checked per query)
User-Agent is exactly the project tag (README rule 4). Research agent PA2, 2026-09-29.
"""
import sys, time
import requests

UA = "JapanDevResearch/1.0 (DayZ mod research)"
BASE = "https://collectionapi.metmuseum.org/public/collection/v1/"


def get(path, params=None):
    time.sleep(3.0)
    r = requests.get(BASE + path, params=params, headers={"User-Agent": UA}, timeout=40)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    n = int(sys.argv[1])
    for q in sys.argv[2:]:
        print("=== %s" % q)
        ids = (get("search", {"q": q, "hasImages": "true"}).get("objectIDs") or [])[:n]
        for i in ids:
            try:
                o = get("objects/%d" % i)
            except Exception as ex:  # noqa: BLE001
                print(i, "ERR", ex)
                continue
            if not o.get("isPublicDomain") or not o.get("primaryImageSmall"):
                continue
            if "Japan" not in (o.get("culture", "") + o.get("country", "")):
                continue
            print("%d | %s | %s | %s | %s" % (i, o.get("title", "")[:50], o.get("objectDate", ""),
                                             o.get("medium", "")[:40], o.get("dimensions", "")[:80].replace("\n", " ")))
