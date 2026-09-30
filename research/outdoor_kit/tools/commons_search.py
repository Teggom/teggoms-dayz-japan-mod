"""Search Wikimedia Commons (File namespace) and print candidates with licence, so refs can be picked by hand.

Run:  python research/outdoor_kit/tools/commons_search.py "query one" "query two" ...
Generic User-Agent only (README rule 4: no personal information in any request).
Research agent PA3, 2026-09-29.
"""
import sys, time, requests

UA = {'User-Agent': 'JapanDevResearch/1.0 (DayZ mod research)'}
API = 'https://commons.wikimedia.org/w/api.php'
OK = ('public domain', 'pd', 'cc0', 'cc by', 'cc-by')


def search(q, n=8):
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': q, 'gsrnamespace': 6, 'gsrlimit': n,
         'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiextmetadatafilter': 'LicenseShortName|DateTimeOriginal|Artist'}
    for i in range(4):
        r = requests.get(API, params=p, headers=UA, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get('retry-after', 5))); continue
        r.raise_for_status(); break
    pages = r.json().get('query', {}).get('pages', {})
    out = []
    for pg in sorted(pages.values(), key=lambda x: x.get('index', 0)):
        ii = pg.get('imageinfo', [{}])[0]; em = ii.get('extmetadata', {})
        lic = em.get('LicenseShortName', {}).get('value', '?')
        date = em.get('DateTimeOriginal', {}).get('value', '')[:40]
        ok = any(lic.lower().startswith(o) for o in OK) and '-sa' not in lic.lower()
        out.append((ok, pg['title'], lic, date, ii.get('width'), ii.get('height')))
    return out


if __name__ == '__main__':
    for q in sys.argv[1:]:
        print('###', q)
        for ok, t, lic, d, w, h in search(q):
            print('  %s %s | %s | %s | %sx%s' % ('OK ' if ok else '-- ', t, lic, d.replace('\n', ' '), w, h))
        time.sleep(1)
