"""FX2 reference fetch: the picked CC0 / public-domain images (Met isPublicDomain, Cleveland CC0) from the survey
(data/refs/fx2/_survey.json, refs_survey.py) -> data/refs/fx2/<museum>_<id>_<k>.jpg + research/statues/REFS.md.

Neutral User-Agent, nothing personal; sequential with a pause; web-size images only.
"""
import json
import os
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(DEV, "data", "refs", "fx2")
MD = os.path.join(DEV, "research", "statues", "REFS.md")
UA = {"User-Agent": "japan-dev-reference-fetch/1.0"}

# (museum, object id, how many images: primary + n-1 alternates, used for)
PICKS = [
    ("cma", 136319, 3, "Amida (altar image): seated, jobon-josho mudra, curls, robe folds, lotus pedestal, halo"),
    ("met", 44890, 2, "Amida (altar image): seated Amida, face, curls, robe over both shoulders"),
    ("cma", 153384, 2, "Shaka (Zen altar image): seated, face, robe folds"),
    ("cma", 147588, 1, "Seated Buddha: proportions of a seated image on its pedestal"),
    ("cma", 147591, 1, "Lotus pedestal (rengeza): petal tiers and the stacked base"),
    ("cma", 147590, 1, "Mandorla (kohai): boat-shaped halo with its border"),
    ("cma", 152018, 2, "Standing Sho Kannon: crown, topknot, scarves, skirt folds, hands"),
    ("met", 49257, 2, "Standing Sho Kannon (12th c.): proportions, drapery"),
    ("met", 53175, 3, "Jizo (altar + stone Jizo face / robe): shaven head, jewel in the left hand, staff in the right"),
    ("met", 76084, 2, "Jizo (1291): standing monk proportions, shakujo staff head with rings"),
    ("cma", 106263, 2, "Komainu pair: open-mouth (a) karashishi, mane curls, seated pose"),
    ("cma", 106262, 2, "Komainu pair: closed-mouth (un) komainu with the horn, seated pose"),
    ("met", 53190, 2, "Guardian lion-dogs (pair): pose, mane, tail, a/un mouths"),
    ("met", 60375, 1, "Fox anatomy (netsuke): muzzle, ears, tail (no stone Inari fox in either collection)"),
    ("cma", 149100, 1, "Okina mask (kagura / noh): old man, cut chin, eyebrow tufts"),
    ("cma", 147048, 1, "Ko-beshimi mask: demon, clenched mouth, bulging eyes"),
    ("cma", 147046, 1, "Waka-onna mask: the plain woman's face (okame / onna form)"),
    ("cma", 148010, 1, "Kyogen usobuki (whistler): the hyottoko pursed mouth"),
    ("cma", 125787, 1, "Gong (bronze): the cast gong form and boss"),
    ("met", 36108, 1, "Ema (1631): early-Edo votive board shape and painted panel"),
]


def get(url, **kw):
    time.sleep(0.8)
    r = requests.get(url, headers=UA, timeout=60, **kw)
    r.raise_for_status()
    return r


def met_small(u):
    return u.replace("/original/", "/web-large/") if u else u


def main():
    os.makedirs(OUT, exist_ok=True)
    sv = json.load(open(os.path.join(OUT, "_survey.json"), encoding="utf-8"))
    idx = {}
    for mus in ("met", "cma"):
        for rows in sv[mus].values():
            if isinstance(rows, list):
                for r in rows:
                    if "id" in r and "error" not in r:
                        idx[(mus, r["id"])] = r
    rows_md = []
    n = 0
    for mus, oid, k, use in PICKS:
        r = idx.get((mus, oid))
        if r is None:
            print("not in survey:", mus, oid)
            continue
        urls = [r["img"]] + [u for u in r.get("more", []) if u]
        urls = urls[:k]
        files = []
        for i, u in enumerate(urls):
            if mus == "met":
                u = met_small(u)
            fn = "%s_%s_%d.jpg" % (mus, oid, i)
            fp = os.path.join(OUT, fn)
            if not os.path.isfile(fp):
                try:
                    data = get(u).content
                except Exception as e:  # noqa: BLE001
                    print("FAILED", u, e)
                    continue
                with open(fp, "wb") as f:
                    f.write(data)
                n += 1
            files.append(fn)
            print(fn, os.path.getsize(fp))
        lic = "Met Open Access, public domain (CC0; isPublicDomain = true)" if mus == "met" else \
            "Cleveland Museum of Art Open Access, CC0 (share_license_status = CC0)"
        rows_md.append("| %s | %s | %s | %s | %s | %s | [object](%s) | %s | %s |" % (
            "The Met" if mus == "met" else "Cleveland", oid, (r.get("title") or "").replace("|", "/"), r.get("date"),
            r.get("medium") or "", lic, r.get("url"), ", ".join(files), use))
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    head = ("# FX2 statue / prop references (fetched 2026-10-01)\n\n"
            "Downloaded by `spikes/FX2/refs_fetch.py` through the museums' official open-access APIs (Stephen's option "
            "B): The Metropolitan Museum of Art Collection API (`collectionapi.metmuseum.org`, v1.1 search + objects; "
            "only `isPublicDomain = true`; the web-large image size) and the Cleveland Museum of Art Open Access API "
            "(`openaccess-api.clevelandart.org`; only `share_license_status = CC0`; the web image). Neutral User-Agent "
            "`japan-dev-reference-fetch/1.0`, sequential requests with a pause. Images: `data/refs/fx2/` (git-ignored). "
            "The metadata survey (all candidates, no images) is `data/refs/fx2/_survey.json`.\n\n"
            "Note: the Met's v1 `/search` endpoint was retired on 2026-10-01 (HTTP 410 with a pointer to v1.1); the "
            "v1.1 search was used.\n\n"
            "| Museum | Object | Title | Date | Medium | Licence | URL | Files | Used for |\n"
            "|---|---|---|---|---|---|---|---|---|\n")
    with open(MD, "wb") as f:
        f.write((head + "\n".join(rows_md) + "\n").encode("utf-8"))
    print("downloaded", n, "images;", len(rows_md), "objects")


if __name__ == "__main__":
    main()
