"""Download the outdoor-kit reference images (PD / CC0 / CC BY only) from Wikimedia Commons as <=1600 px thumbnails.

Run:  python research/outdoor_kit/tools/fetch_refs.py [--meta-only]
Resumable: files already on disk are skipped. upload.wikimedia.org rate-limits generic User-Agents (HTTP 429);
a pick that cannot be downloaded is recorded as "linked only" with its licence and page, and a later rerun fills it.
Writes: data/research_okit/refs/<id>.jpg and data/research_okit/meta.json (the download log that
gen_build_list.py turns into refs_index.json and CREDITS.md).
Generic User-Agent only (README rule 4). Refs are local research copies: never shipped.
Research agent PA3, 2026-09-29.
"""
import json, os, re, sys, time, requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DST = os.path.join(ROOT, 'data', 'research_okit')
UA = {'User-Agent': 'JapanDevResearch/1.0 (DayZ mod research)'}
API = 'https://commons.wikimedia.org/w/api.php'

# id -> Commons file title (picked by hand from commons_search.py output; unused picks were viewed and dropped:
# three more Tokaido bunken ezu pages (too schematic), two Sukenobu ehon pages (a cover, a fable), a second Moronobu)
PICKS = {
 'k02_bunken_ezu_p12': 'File:NDL-DC 1287041 2 1287740 Tokaido Bunken Ezu 0012 0000crd.jpg',
 'k05_moronobu_street_1680': 'File:MET DP124572.jpg',
 'k06_moronobu_ageyamachi': 'File:The Entrance to Ageya-machi, from the series Scenes in the Yoshiwara (Yoshiwara no tei) (IA mma the entrance to ageyamachi from the series scenes in the yoshiwara yoshiw 37252).jpg',
 'k09_masanobu_ishiyama_1740': 'File:Okumura Masanobu - Lady Murasaki at Ishiyama Overlooking a Panorama with Seven Views of Lake B - 1916.1147 - Cleveland Museum of Art.jpg',
 'k10_morse_well_frame': 'File:JapanHomes 289 Wooden well-frame.jpg',
 'k11_morse_well_rustic': 'File:JapanHomes 290 Rustic well-frame.jpg',
 'k12_morse_well_kaga': 'File:JapanHomes 293 Well at Kaga Yashiki, Tokio.jpg',
 'k13_morse_well_curb_old': 'File:JapanHomes 287 Ancient form of well-curb.jpg',
 'k14_morse_well_curb_stone': 'File:JapanHomes 288 Stone well-curb in private garden.jpg',
 'k15_morse_chozubachi': 'File:JapanHomes 240 Chōdzu-bachi.jpg',
 'k16_morse_toro_tokio': 'File:JapanHomes 264 Ishi-dōrō in Tokio.jpg',
 'k17_morse_toro_utsunomiya': 'File:JapanHomes 267 Ishi-dōrō in Utsunomiya.jpg',
 'k19_koshinto': 'File:Kosinto0091.jpg',
 'k20_kosatsuba_kashiwabara': 'File:The ruin of Kōsatsuba in Kashiwabara 20210308.jpg',
 'k21_edo_bousui': 'File:Japanese Edo Bousui.jpg',
 'k22_hirakata_jinja': 'File:Hirakata-jinja (Matsudo, Matsudo) 04.jpg',
 'k23_kasuga_lanterns': 'File:Stone lanterns in Kasuga-taisha-1.jpg',
 'k24_chozubachi': 'File:Chozubachi chozuya water purification in Shinto shrine in Japan.jpg',
 'k25_gorinto': 'File:Gorinto.jpg',
 'k26_gorinto_gamou': 'File:Grave of Gamou Ujisato in Koutokuji.JPG',
 'k27_hida_torii': 'File:Hidatorii.jpg',
 'k28_kusakabe_peddler': 'File:Vegetable peddler Kusakabe Kimbei.jpg',
 'k29_hiroshige_numazu': 'File:Numazu (5765899882).jpg',
 'k30_rokujizo': 'File:六地蔵石仏.jpg',
 'k31_daihachi_uzumasa': 'File:Toei Uzumasa-0321.jpg',
 'k32_harunobu_well': "File:At the Well on New Year's Morning (IA mma at the well on new years morning 36635).jpg",
 'k33_harunobu_araihari_1767': 'File:Araihari LCCN2008660584.jpg',
 'k34_straw_rice': 'File:Straw of the rice.08Oct9.jpg',
 'k35_firewood_hoshigaki': 'File:岩手県 干し柿 薪 (45239013034).jpg',
 'k36_firewood_motai': 'File:Motai-juku, Saku, Nagano, Japan (3577074903).jpg',
 'k37_shimenawa_tree': 'File:Shikaumi Shrine Sacred Tree.jpg',
 'k38_shrine_steps': 'File:Kashima Daijingu Shrine, stone steps in the precincts. Niita district, Koriyama city, Fukushima prefecture.jpg',
 'k39_nobori_hiko': 'File:Hiko Shrine banners.jpg',
 'k40_motoki_torii': 'File:Motoki Stone Torii in 2026 01.jpg',
 'k41_koshin_sendabori': 'File:Sendabori no Kōshin-tō (Kanegasaku, Matsudo) 01.jpg',
}

def clean(s):
    return re.sub(r'<[^>]+>', '', s or '').strip()[:160]

def info(title):
    p = {'action': 'query', 'format': 'json', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size',
         'iiurlwidth': 1600}
    for i in range(5):
        r = requests.get(API, params=p, headers=UA, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get('retry-after', 5))); continue
        r.raise_for_status(); break
    pg = list(r.json()['query']['pages'].values())[0]
    return pg['imageinfo'][0]

META_ONLY = '--meta-only' in sys.argv   # record licence/author/page for every pick without downloading

def main():
    os.makedirs(os.path.join(DST, 'refs'), exist_ok=True)
    mp = os.path.join(DST, 'meta.json')
    meta = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}
    fails = 0
    for rid, title in PICKS.items():
        if fails >= 3:
            print('STOP: 3 files in a row rate-limited; rerun later', flush=True); break
        fn = os.path.join(DST, 'refs', rid + '.jpg')
        have = os.path.exists(fn) and os.path.getsize(fn) > 5000 and open(fn, 'rb').read(3) in (b'\xff\xd8\xff', b'\x89PN')
        if rid in meta and have:
            continue
        if META_ONLY and rid in meta:
            continue
        ii = info(title); em = ii.get('extmetadata', {})
        lic = clean(em.get('LicenseShortName', {}).get('value'))
        if not (lic.lower().startswith(('public domain', 'pd', 'cc0', 'cc by')) and '-sa' not in lic.lower()):
            print('SKIP licence', rid, lic, flush=True); continue
        # small originals: Commons refuses to upscale a thumbnail, so take the original file
        url = ii['url'] if (ii.get('width') or 0) <= 1600 else (ii.get('thumburl') or ii['url'])
        size = os.path.getsize(fn) if have else 0
        r = None
        if not have and not META_ONLY:
            for i in range(3):
                r = requests.get(url, headers=UA, timeout=60)
                if r.status_code == 429:
                    print('  429, waiting 60', flush=True); time.sleep(60); continue
                r.raise_for_status(); break
            if r.headers.get('content-type', '').startswith('image/'):
                open(fn, 'wb').write(r.content); size = len(r.content); have = True; fails = 0
            else:
                print('FAIL not an image (rate-limited), recorded as linked', rid, r.headers.get('content-type'), flush=True); fails += 1
        meta[rid] = {'id': rid, 'file': ('data/research_okit/refs/%s.jpg' % rid) if have else None,
                     'status': 'downloaded' if have else 'linked only (upload.wikimedia.org answered 429; rerun fetch_refs.py to download)',
                     'source': 'Wikimedia Commons', 'title': title,
                     'page_url': ii.get('descriptionurl'), 'licence': lic,
                     'author': clean(em.get('Artist', {}).get('value')) or 'unknown',
                     'date': clean(em.get('DateTimeOriginal', {}).get('value')) or 'unknown', 'bytes': size}
        open(mp, 'wb').write((json.dumps(meta, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
        print('ok', rid, lic, size, flush=True)
        time.sleep(0.5 if META_ONLY else 45)

if __name__ == '__main__':
    main()
