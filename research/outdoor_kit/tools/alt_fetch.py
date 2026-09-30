"""Fetch outdoor-kit reference images from non-Wikimedia sources (lead, 2026-09-29).

upload.wikimedia.org blocks our generic User-Agent (slow_fetch.log: HTTP 429 for 70 min on one file). These picks exist
at their original institutions, which serve them freely:
  - Project Gutenberg #52868, E. S. Morse, "Japanese Homes and Their Surroundings" (1886), public domain: 8 figures
  - The Metropolitan Museum of Art Open Access (CC0): Harunobu, "Drawing the First Water of the New Year" (object 36635)
  - Library of Congress, Prints & Photographs (no known restrictions): "Araihari" (LCCN 2008660584)
Saved as <=1600 px JPEGs into data/research_okit/refs/<id>.jpg; meta.json is updated; then gen_build_list.py is rerun.
Generic User-Agent only (README rule 4).
"""
import io, json, os, subprocess, sys, time
import requests
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DST = os.path.join(ROOT, "data", "research_okit")
UA = {"User-Agent": "JapanDevResearch/1.0 (DayZ mod research)"}
GUT = "https://www.gutenberg.org/files/52868/52868-h/images/fig%03d.jpg"
GUT_PAGE = "https://www.gutenberg.org/ebooks/52868"
MORSE = dict(source="Project Gutenberg #52868", licence="Public domain",
             author="Edward S. Morse", date="1886", page_url=GUT_PAGE)

PICKS = {
    "k10_morse_well_frame": (GUT % 289, dict(MORSE, title="Fig. 289, Wooden well-frame")),
    "k11_morse_well_rustic": (GUT % 290, dict(MORSE, title="Fig. 290, Rustic well-frame")),
    "k12_morse_well_kaga": (GUT % 293, dict(MORSE, title="Fig. 293, Well at Kaga Yashiki, Tokio")),
    "k13_morse_well_curb_old": (GUT % 287, dict(MORSE, title="Fig. 287, Ancient form of well-curb")),
    "k14_morse_well_curb_stone": (GUT % 288, dict(MORSE, title="Fig. 288, Stone well-curb in private garden")),
    "k15_morse_chozubachi": (GUT % 240, dict(MORSE, title="Fig. 240, Chōdzu-bachi")),
    "k16_morse_toro_tokio": (GUT % 264, dict(MORSE, title="Fig. 264, Ishi-dōrō in Tokio")),
    "k17_morse_toro_utsunomiya": (GUT % 267, dict(MORSE, title="Fig. 267, Ishi-dōrō in Utsunomiya")),
    "k32_harunobu_well": ("https://images.metmuseum.org/CRDImages/as/original/DP114903.jpg",
                          dict(source="The Metropolitan Museum of Art, Open Access", licence="CC0",
                               author="Suzuki Harunobu", date="c. 1766-70",
                               title="Drawing the First Water of the New Year (object 36635)",
                               page_url="https://www.metmuseum.org/art/collection/search/36635")),
    "k33_harunobu_araihari_1767": ("https://tile.loc.gov/storage-services/service/pnp/jpd/01900/01958v.jpg",
                                   dict(source="Library of Congress, Prints & Photographs",
                                        licence="No known restrictions on publication", author="Suzuki Harunobu",
                                        date="c. 1767", title="Araihari (LCCN 2008660584)",
                                        page_url="https://www.loc.gov/item/2008660584/")),
}


def main():
    os.makedirs(os.path.join(DST, "refs"), exist_ok=True)
    mp = os.path.join(DST, "meta.json")
    meta = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
    for rid, (url, info) in PICKS.items():
        fn = os.path.join(DST, "refs", rid + ".jpg")
        for attempt in range(5):
            try:
                r = requests.get(url, headers=UA, timeout=120)
                if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
                    break
                print("retry", rid, r.status_code, flush=True)
            except Exception as e:
                print("retry", rid, e, flush=True)
            time.sleep(20 * (attempt + 1))
        else:
            print("FAILED", rid, flush=True)
            continue
        im = Image.open(io.BytesIO(r.content)).convert("RGB")
        im.thumbnail((1600, 1600))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=90)
        open(fn, "wb").write(buf.getvalue())
        meta[rid] = dict(id=rid, file="data/research_okit/refs/%s.jpg" % rid, status="downloaded",
                         bytes=len(buf.getvalue()), **info)
        open(mp, "wb").write((json.dumps(meta, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
        print("ok", rid, im.size, flush=True)
        time.sleep(3)
    rc = subprocess.call([sys.executable, os.path.join(HERE, "gen_build_list.py")], cwd=ROOT)
    print("gen_build_list.py exit", rc)


if __name__ == "__main__":
    main()
