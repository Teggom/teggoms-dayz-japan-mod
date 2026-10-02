"""FX2 reference survey: metadata only (no images) from the Met + Cleveland open-access APIs.

  python refs_survey.py            -> data/refs/fx2/_survey.json (candidates per query)

Rules (Stephen, option B): neutral User-Agent, nothing personal; sequential with a pause; Met isPublicDomain only;
Cleveland share_license_status CC0 only. Images are fetched later by refs_fetch.py for the picks only.
"""
import json
import os
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "data", "refs", "fx2")
UA = {"User-Agent": "japan-dev-reference-fetch/1.0"}
PAUSE = 0.8
NREQ = [0]

MET_Q = ["Jizo", "Amida", "Amitabha", "Shaka", "Kannon", "Bodhisattva Japan", "Buddha Japan Edo",
         "komainu", "lion dog", "guardian lion Japan", "Inari fox", "fox Japan sculpture",
         "noh mask", "gigaku mask", "kagura mask", "temple bell Japan", "gong Japan", "ema votive"]
CMA_Q = ["Jizo", "Amida", "Shaka", "Kannon", "Buddha", "Bodhisattva", "komainu", "lion-dog", "lion",
         "fox", "noh mask", "gigaku mask", "mask", "bell", "gong", "ema"]


def get(url, params=None):
    time.sleep(PAUSE)
    NREQ[0] += 1
    r = requests.get(url, params=params, headers=UA, timeout=40)
    r.raise_for_status()
    return r.json()


def met():
    out = {}
    seen = set()
    for q in MET_Q:
        try:
            ids = get("https://collectionapi.metmuseum.org/public/collection/v1.1/search",
                      {"q": q, "hasImages": "true", "departmentId": 6, "limit": 14}).get("objectIDs") or []
        except Exception as e:  # noqa: BLE001
            out[q] = {"error": str(e)}
            continue
        rows = []
        for oid in ids[:14]:
            if oid in seen:
                continue
            seen.add(oid)
            try:
                o = get("https://collectionapi.metmuseum.org/public/collection/v1/objects/%d" % oid)
            except Exception as e:  # noqa: BLE001
                rows.append({"id": oid, "error": str(e)})
                continue
            if not o.get("isPublicDomain"):
                continue
            if "Japan" not in (o.get("culture") or "") + (o.get("country") or ""):
                continue
            rows.append({"id": oid, "title": o.get("title"), "date": o.get("objectDate"),
                         "medium": o.get("medium"), "classification": o.get("classification"),
                         "dims": o.get("dimensions"), "img": o.get("primaryImage"),
                         "more": o.get("additionalImages") or [], "url": o.get("objectURL")})
        out[q] = rows
        print("met", q, len(ids), "->", len(rows), "req", NREQ[0], flush=True)
        if NREQ[0] > 220:
            break
    return out


def cma():
    out = {}
    for q in CMA_Q:
        try:
            d = get("https://openaccess-api.clevelandart.org/api/artworks/",
                    {"q": q, "cc0": 1, "has_image": 1, "department": "Japanese Art", "limit": 25})
        except Exception as e:  # noqa: BLE001
            out[q] = {"error": str(e)}
            continue
        rows = []
        for o in d.get("data", []):
            if o.get("share_license_status") != "CC0":
                continue
            im = (o.get("images") or {})
            rows.append({"id": o.get("id"), "acc": o.get("accession_number"), "title": o.get("title"),
                         "date": o.get("creation_date"), "type": o.get("type"), "medium": o.get("technique"),
                         "dims": o.get("measurements"),
                         "img": ((im.get("web") or {}).get("url")),
                         "more": [((a.get("web") or {}).get("url")) for a in (o.get("alternate_images") or [])],
                         "url": o.get("url")})
        out[q] = rows
        print("cma", q, "->", len(rows), "req", NREQ[0], flush=True)
    return out


def main():
    import sys
    os.makedirs(OUT, exist_ok=True)
    fp = os.path.join(OUT, "_survey.json")
    old = json.load(open(fp, encoding="utf-8")) if os.path.isfile(fp) else {}
    if "--met" in sys.argv and old.get("cma"):
        res = {"cma": old["cma"], "met": met(), "requests": NREQ[0]}   # the v1 search was retired 2026-10-01: v1.1
    else:
        res = {"cma": cma(), "met": met(), "requests": NREQ[0]}
    with open(os.path.join(OUT, "_survey.json"), "wb") as f:
        f.write(json.dumps(res, indent=1, ensure_ascii=False).encode("utf-8"))
    print("done, requests", NREQ[0])


if __name__ == "__main__":
    main()
