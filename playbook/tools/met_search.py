"""Search The Met Open Access API; list public-domain Japanese objects with images. One request per 3 s.

Usage: python met_search.py N "query one" "query two" ...   (N = objects checked per query)
"""
import sys, time
import requests

UA = "JapanDevPlaybook/0.1 (DayZ mod period-reference research; low volume; python-requests)"
BASE = "https://collectionapi.metmuseum.org/public/collection/v1/"


def get(path, params=None):
    time.sleep(3.0)
    r = requests.get(BASE + path, params=params, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    n = int(sys.argv[1])
    for q in sys.argv[2:]:
        print("=== %s" % q)
        ids = (get("search", {"q": q, "hasImages": "true"}).get("objectIDs") or [])[:n]
        for i in ids:
            o = get("objects/%d" % i)
            if not o.get("isPublicDomain") or not o.get("primaryImageSmall"):
                continue
            if o.get("culture", "") and "Japan" not in o.get("culture", ""):
                continue
            print("%d | %s | %s | %s | %s" % (i, o.get("title", "")[:60], o.get("objectDate", ""),
                                             o.get("medium", "")[:50], o.get("primaryImage", "")))
