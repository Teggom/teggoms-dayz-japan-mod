"""Slow, never-give-up downloader for the outdoor-kit reference images (lead, 2026-09-29).

fetch_refs.py stops after 3 rate-limited files. This one takes the same PICKS and licence rule, fetches ONE image at a
time, waits 2 minutes between successes, and on a 429 / non-image / network error backs off (5 min, doubling to 30
min) and retries the SAME file until it succeeds. When every pick is on disk it updates meta.json and reruns
gen_build_list.py.

Run:  python research/outdoor_kit/tools/slow_fetch.py      (progress: data/research_okit/slow_fetch.log)
Generic User-Agent only (README rule 4).
"""
import json, os, subprocess, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_refs as fr   # PICKS, info(), clean(), UA, DST

GAP_OK = 120
BACKOFF0, BACKOFF_MAX = 300, 1800
LOG = os.path.join(fr.DST, "slow_fetch.log")


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "ab") as f:
        f.write((line + "\n").encode("utf-8"))


def have(fn):
    return os.path.exists(fn) and os.path.getsize(fn) > 5000 and open(fn, "rb").read(3) in (b"\xff\xd8\xff", b"\x89PN")


def licence_ok(lic):
    return lic.lower().startswith(("public domain", "pd", "cc0", "cc by")) and "-sa" not in lic.lower()


def main():
    os.makedirs(os.path.join(fr.DST, "refs"), exist_ok=True)
    mp = os.path.join(fr.DST, "meta.json")
    meta = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
    todo = [(rid, t) for rid, t in fr.PICKS.items() if not have(os.path.join(fr.DST, "refs", rid + ".jpg"))]
    log("start: %d of %d picks still to download" % (len(todo), len(fr.PICKS)))
    for n, (rid, title) in enumerate(todo, 1):
        fn = os.path.join(fr.DST, "refs", rid + ".jpg")
        wait = BACKOFF0
        while True:
            try:
                ii = fr.info(title)
                em = ii.get("extmetadata", {})
                lic = fr.clean(em.get("LicenseShortName", {}).get("value"))
                if not licence_ok(lic):
                    log("SKIP (licence %s) %s" % (lic, rid))
                    break
                url = ii["url"] if (ii.get("width") or 0) <= 1600 else (ii.get("thumburl") or ii["url"])
                r = requests.get(url, headers=fr.UA, timeout=90)
                if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
                    open(fn, "wb").write(r.content)
                    meta[rid] = {"id": rid, "file": "data/research_okit/refs/%s.jpg" % rid, "status": "downloaded",
                                 "source": "Wikimedia Commons", "title": title, "page_url": ii.get("descriptionurl"),
                                 "licence": lic, "author": fr.clean(em.get("Artist", {}).get("value")) or "unknown",
                                 "date": fr.clean(em.get("DateTimeOriginal", {}).get("value")) or "unknown",
                                 "bytes": len(r.content)}
                    open(mp, "wb").write((json.dumps(meta, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
                    log("ok %d/%d %s (%d bytes)" % (n, len(todo), rid, len(r.content)))
                    time.sleep(GAP_OK)
                    break
                log("not yet %s: HTTP %s %s; waiting %d s" % (rid, r.status_code, r.headers.get("content-type"), wait))
            except Exception as e:   # network hiccup, API 429 raised as an error, JSON error: just wait and retry
                log("error %s: %s; waiting %d s" % (rid, e, wait))
            time.sleep(wait)
            wait = min(wait * 2, BACKOFF_MAX)
    missing = [rid for rid in fr.PICKS if not have(os.path.join(fr.DST, "refs", rid + ".jpg"))]
    log("downloads finished; still missing (licence skips only): %s" % (missing or "none"))
    gen = os.path.join(HERE, "gen_build_list.py")
    rc = subprocess.call([sys.executable, gen], cwd=os.path.abspath(os.path.join(HERE, "..", "..", "..")))
    log("gen_build_list.py exit %d. DONE" % rc)


if __name__ == "__main__":
    main()
