# Generates research/waterways/WATERWAYS.md, waterways.json and CREDITS.md from ww_types.py + ww_settlements.py.
# Research agent WW, 2026-09-29. Run: python research/waterways/tools/gen_waterways.py   (from japan_dev)
# Also checks that every settlement on the map sketch is mapped, and that cited kit part ids exist.
import json, os, sys, unicodedata, collections
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
WW = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(WW))           # japan_dev
sys.path.insert(0, HERE)
from ww_types import TYPES, PARTS
from ww_settlements import parse

SOURCES = {
 "S-TAK": ("Takase River: canal 1611, ~10 km; ~8 m channel, ~30 cm water; takasebune ~13 x 2 m, 15 koku; ~200 boats, ~700 haulers; 9 funairi, Ichi-no-funairi 55 x 6 ken, stone-walled",
           "https://en.wikipedia.org/wiki/Takase_River ; https://ja.wikipedia.org/wiki/%E9%AB%98%E7%80%AC%E5%B7%9D_(%E4%BA%AC%E9%83%BD%E5%BA%9C) ; https://www.keihan.co.jp/navi/kyoto_tsu/tsu201902.html ; https://ja.wikipedia.org/wiki/%E9%AB%98%E7%80%AC%E5%B7%9D%E4%B8%80%E4%B9%8B%E8%88%B9%E5%85%A5"),
 "S-OSK": ("Osaka canals: Higashi-yokobori 1585, Nishi-yokobori 1600, Dotonbori 1612-15 (30-50 m today), Edobori 1617, Nagahori ~40 m",
           "https://ja.wikipedia.org/wiki/%E9%81%93%E9%A0%93%E5%A0%80 ; https://ja.wikipedia.org/wiki/%E8%A5%BF%E6%A8%AA%E5%A0%80%E5%B7%9D ; https://www.city.osaka.lg.jp/kensetsu/page/0000009775.html"),
 "S-KURA": ("Hiroshima domain kura-yashiki, Nakanoshima, Osaka (excavated 1995-2018): stone revetment ~3 m high, gangi, boat basin 51 x 47 m cut into the plot",
            "https://nakka-art.jp/en/nakka-news/13-en/ ; https://www.let.osaka-u.ac.jp/kouko/nakanoshima_top.htm"),
 "S-30K": ("Sanjukkenbori (Edo): dug 1612, ~30 ken (~55 m) wide, quays both sides; narrowed to 19 ken in 1828",
           "https://ja.wikipedia.org/wiki/%E4%B8%89%E5%8D%81%E9%96%93%E5%A0%80%E5%B7%9D"),
 "S-KAMO": ("Kamo River: Kanbun new levee completed 1670, river narrowed to ~100 m, straightened, stone revetment; Sanjo Ohashi 61 x 3 ken (1780 record)",
            "https://www.ritsumei.ac.jp/acd/cg/lt/rb/593PDF/yosikosi.pdf ; https://www.city.kyoto.lg.jp/kensetu/cmsfiles/contents/0000149/149842/hashishirube22.pdf"),
 "S-YAH": ("Yahagi-bashi, Okazaki: 208 ken (~378 m), a shogunal bridge, first built 1601; longest on the Tokaido",
           "https://ja.wikipedia.org/wiki/%E7%9F%A2%E4%BD%9C%E6%A9%8B"),
 "S-SUMI": ("Sumida levee (Bokutei) cherries planted by Yoshimune, usually dated 1717 (other dates proposed)",
            "https://www.edo-tokyo-museum.or.jp/purpose/library/reference/alphabet/4975/"),
 "S-NGY": ("Nagoya Horikawa: dug 1610 by Fukushima Masanori, castle to Atsuta, ~6 km, 12-48 ken (22-87 m); merchant kura upstream of Nayabashi, domain rice stores below",
           "https://www.city.nagoya.jp/kurashi/douro/1014806/1034763/1014833/1014838.html"),
 "S-OGK": ("Ogaki: Suimon-gawa boats via the Ibi to Kuwana; Funamachi river port; Sumiyoshi lantern ~8 m, built 1688-1704; Basho left by boat in 1689",
           "https://www.city.ogaki.lg.jp/0000037028.html ; https://ja.wikipedia.org/wiki/%E4%BD%8F%E5%90%89%E7%81%AF%E5%8F%B0_(%E5%B2%90%E9%98%9C%E7%9C%8C)"),
 "S-ISE": ("Ise Kawasaki: kura and townhouses on both banks of the Seta River, goods moved straight from boats into the kura; Isuzu mitarashi stone paving given by Keishoin",
           "http://www.isekawasaki.jp/about/ ; https://travel.yahoo.co.jp/kanko/spot-00003569/"),
 "S-NKT": ("Nakatsugawa post town: a water channel down the centre of the main street past the honjin, for fire; washing forbidden; filled and moved in 1880; shown on the Nakasendo survey map",
           "https://www.city.nakatsugawa.lg.jp/museum/n/nakatsugawa_juku/4812.html"),
 "S-NRI": ("Narai post town: spring-water stations along the street for drinking and fire; one roofed with stone-weighted boards",
           "https://fdkt.sakura.ne.jp/yusui/category2/entry123.html"),
 "S-MSM": ("Mishima: Genbei-gawa, a 1.5 km channel from Kohama pond dug for paddies in the late 16th c.; on the shogunate's road survey map",
           "https://water-pub.env.go.jp/water-pub/mizu-site/newmeisui/data/index.asp?info=54"),
 "S-FSM": ("Fushimi: jikkoku and sanjikkoku boats between Fushimi and Osaka; sanjikkoku-bune ~17 x 2.5 m (another source: 11-15 x ~2 m in the Genroku era)",
           "https://ja.wikipedia.org/wiki/%E4%BC%8F%E8%A6%8B%E5%8D%81%E7%9F%B3%E8%88%9F ; https://www.kyoto-wel.com/yomoyama/yomoyama10/059/059.htm"),
 "S-YODO": ("Yodo castle waterwheels: two, 8 and 6 ken across, lifting river water into the castle",
            "https://www2.city.kyoto.lg.jp/somu/rekishi/fm/ishibumi/html/hu047.html ; https://www.arc.ritsumei.ac.jp/artwiki/index.php/%E6%B7%80%E3%81%AE%E6%B0%B4%E8%BB%8A"),
 "S-KRG": ("Kuragano kashi on the Karasu River: the uppermost Tone river port, shogunate-approved in the early Edo period; takasebune to Edo",
           "https://kotobank.jp/word/%E5%80%89%E8%B3%80%E9%87%8E-56256 ; https://ja.wikipedia.org/wiki/%E5%80%89%E8%B3%80%E9%87%8E%E5%AE%BF"),
 "S-NMZ": ("Numazu castle built 1777-79 by Mizuno Tadatomo; Sanmaibashi castle abandoned 1614",
           "https://ja.wikipedia.org/wiki/%E6%B2%BC%E6%B4%A5%E5%9F%8E ; https://www.city.numazu.shizuoka.jp/shisei/profile/bunkazai/siro/sanmai.htm"),
 "S-TNK": ("Tanaka castle, Fujieda: concentric circular plan ~600 m across, four moat rings; Honda lords from 1730",
           "https://ja.wikipedia.org/wiki/%E7%94%B0%E4%B8%AD%E5%9F%8E"),
 "S-HMJ": ("Himeji castle moats: average 20 m, max 34.5 m, depth ~2.7 m (a generic Edo-period wet-moat benchmark)",
           "https://en.wikipedia.org/wiki/Himeji_Castle"),
 "S-MTM": ("Matsumoto castle: three rings of wide moats, ~50 m wide east of the main gate",
           "https://www.walkigram.net/matsumoto/castlewater-chart.html"),
 "S-EDOM": ("Edo castle outer moat (1636): stone wall ~6 m high on the Nihonbashi River's south bank; excavated moat walls stand on timber sills with piles ~1 m apart",
            "https://www.edo-chiyoda.jp/knainobunkazai/bunkazaisign_hyochu_setsumeiban/1/1/116.html ; https://www.mext.go.jp/b_menu/soshiki2/ishigaki/index.htm"),
 "S-YUKA": ("Kamo riverbed cooling platforms: from the early modern period; by the mid-Edo ~400 tea shops with benches on the flats and shallows (kawara no suzumi). Summer only",
            "https://www.kyoto-yuka.com/about/history.html"),
 "S-HARIE": ("Harie (Takashima, Omi) kabata spring-water house basins; origin date not given",
             "https://harie-syozu.jp/about/"),
 "S-KST": ("Kusatsu River: a raised-bed (tenjo) river; the bed built up mostly from the late 1700s to 1886; the road climbed over it until the 1886 tunnel",
           "https://ja.wikipedia.org/wiki/%E8%8D%89%E6%B4%A5%E5%B7%9D ; https://www.city.kusatsu.shiga.jp/shisei/keikaku/miryoku/kihonnkousou.files/4e94dcb3004.pdf"),
 "S-SMG": ("Samegai: the Jizo-gawa from the Isame spring runs ~500 m through the post town, ~14 C all year, baikamo waterweed",
           "https://www.city.maibara.lg.jp/soshiki/keizai_kankyo/shoko_kanko/kanko_info/spot/14398.html"),
 "S-KYD": ("Kamiyoshida oshi town: founded 1572; 86 oshi lodges on ~750 m of road at the peak; the Yana-gawa stream in front of each house where Fuji pilgrims purified",
           "https://www.mt-fuji.gr.jp/jyunrei/oshi/ ; https://www.driveplaza.com/trip/michinohosomichi/ver153/02.html"),
 "OL": ("research/outdoor/OUTDOOR_LIST.md (U water, R 2, W 4, W 12, N U, section 4 setting kits, section 7)", "local"),
 "KL": ("research/catalogue/KEEP_LANDMARKS.md", "local"),
 "GAP": ("research/GAP_AUDIT.md (Miya: Shirotori timber yard)", "local"),
 "VJ": ("research/map_sketch/villages.json (the village's own note)", "local"),
 "mem": ("general knowledge, not re-checked this session: verify before a build list relies on it", "-"),
 "(assumed)": ("no source; reasoned", "-"),
}

REFS = [
 # file, title, maker, date, what it shows, licence, url
 ("m033_morse_fig033.jpg", "Fig. 33, Street in Kanda Ku, Tokio", "Edward S. Morse, Japanese Homes", "1886",
  "stone-edged house-front gutter with a slab at the gate (d1)", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig033.jpg"),
 ("m034_morse_fig034.jpg", "Fig. 34, Street in Kanda Ku, Tokio", "Edward S. Morse", "1886",
  "gutter along a board fence and house, board bridge to the gate (d1)", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig034.jpg"),
 ("m052_morse_fig052.jpg", "Fig. 52, Village street in Nagaike, Yamashiro (between Nara and Kyoto)", "Edward S. Morse", "1886",
  "a village street on our map's Nara-Kyoto road: no street channel, flat earth", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig052.jpg"),
 ("m066_morse_fig066.jpg", "Fig. 66, Water-conductor", "Edward S. Morse", "1886",
  "split-bamboo eave gutter and downpipe that feeds the street gutter", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig066.jpg"),
 ("m268_morse_fig268.jpg", "Fig. 268, Stone foot-bridge", "Edward S. Morse", "1886",
  "two slabs side by side but offset, on stone posts, over a stream (slab bridge variant)", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig268.jpg"),
 ("m269_morse_fig269.jpg", "Fig. 269, Stone foot-bridge", "Edward S. Morse", "1886",
  "single slab spanning 10-12 ft (3-3.6 m)", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig269.jpg"),
 ("m270_morse_fig270.jpg", "Fig. 270, Garden brook and foot-bridge", "Edward S. Morse", "1886",
  "unwrought rock slab over a brook", "Public domain (Project Gutenberg #52868)", "https://www.gutenberg.org/files/52868/52868-h/images/fig270.jpg"),
 ("l01_toyoharu_naniwa_tenma_river.jpg", "Ukie Naniwa Tenma Tenjin yomatsuri no zu", "Utagawa Toyoharu", "1764-1772",
  "Osaka's Okawa at the Tenma festival: long trestle bridge, riverside houses, many boat types (earliest print here)", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660030/"),
 ("l02_eiri_nihonbashi_uogashi_ukie.jpg", "Ukie Edo Nihonbashi Odawara-cho sakana ichi no zu", "Chokyosai Eiri", "1796-1801",
  "Nihonbashi fish quay: open kashi strip, sheds, kura across the canal, landing stages on piles", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660149/"),
 ("l04_hokusai_okazaki_1804.jpg", "Okazaki (Tokaido series)", "Katsushika Hokusai", "1804",
  "Yahagi-bashi as a long, low-arched trestle", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660874/"),
 ("l05_hiroshige_okazaki_yahagi.jpg", "Okazaki: Yahagi bridge (Tokaido 53 stations, Hoeido)", "Utagawa Hiroshige", "1833-1836",
  "trestle bents, reed beds, sand bar, castle behind (form only)", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660222/"),
 ("l06_hiroshige_keishi_sanjo.jpg", "Keishi: Sanjo Ohashi (Tokaido 53 stations)", "Utagawa Hiroshige", "1833-1836",
  "long bridge over gravel flats and a low-water channel (real piers were stone: form only)", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660700/"),
 ("l07_hiroshige_yatsumi_no_hashi.jpg", "Yatsumi no hashi (100 Views of Edo)", "Utagawa Hiroshige", "1856",
  "dressed-stone canal walls, plank bridge, willow at the corner, cargo boats", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2009631868/"),
 ("l08_hiroshige_onagigawa.jpg", "Onagigawa gohonmatsu (100 Views of Edo)", "Utagawa Hiroshige", "1856",
  "pile-and-board revetment on the far bank, old pine over the canal, a stone edge near side", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660275/"),
 ("l09_hiroshige_sumida_tsutsumi.jpg", "Toto meisho: Sumida tsutsumi hanami no zu", "Utagawa Hiroshige", "1848-1854",
  "levee-top path with cherries, earth steps down the levee side, river and far bank", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2009615472/"),
 ("l10_hiroshige_fukagawa_kiba.jpg", "Fukagawa kiba (100 Views of Edo)", "Utagawa Hiroshige", "1856",
  "timber ponds: floating logs penned by stakes, a plank bridge behind", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2009631892/"),
 ("l11_hiroshige_benkeibori_moat.jpg", "Soto-Sakurada Benkeibori Kojimachi (100 Views of Edo)", "Utagawa Hiroshige", "1856",
  "wet moat with turfed earth banks, low toe revetment, pines on the rampart", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660270/"),
 ("l14_harunobu_ryogokubashi.jpg", "Ryogokubashi no sekisho (Furyu Edo hakkei)", "Suzuki Harunobu", "design c.1767, printed later",
  "Ryogoku trestle bridge, houses on stilts at the riverbank, boats", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2008660744/"),
 ("l16_hiroshige_ochanomizu.jpg", "Toto Ochanomizu (36 Views of Fuji)", "Utagawa Hiroshige", "1858",
  "the Kanda River cut with stone walls and the aqueduct trough bridge over it", "No known restrictions on publication (LOC jpd)", "https://www.loc.gov/pictures/collection/jpd/item/2004666334/"),
]

LINKED_ONLY = [
 ("Yodo castle waterwheel picture (Miyako meisho zue type, Nichibun database)", "https://www.nichibun.ac.jp/meisyozue/gafu/page7/KM_07_01_009F.html"),
 ("Met: An Actor's Boating Party on the Sumida River, Torii Kiyomasu I, c.1705 (the only print found from before 1730)", "https://www.metmuseum.org/art/collection/search/37101"),
 ("Met: Panoramic Views of Both Banks of the Sumida River, Hokusai, 1801 (levees, landings)", "https://www.metmuseum.org/art/collection/search/78637"),
 ("Met: Ommayagashi, Sumida River, Hiroshige, c.1857 (a ferry quay)", "https://www.metmuseum.org/art/collection/search/55712"),
 ("Met: Pleasure Boats beneath Shin-Ohashi Bridge, Eishi, c.1792", "https://www.metmuseum.org/art/collection/search/36481"),
 ("LOC: Tokaido Okazaki / Mishima / Nihonbashi series (more views)", "https://www.loc.gov/pictures/search/?q=Okazaki&co=jpd"),
]

DECISIONS = [
 ("Seven types, not six", "add g, shore landing (harbour, beach, lake shore): {G} settlements (ports, fishing and salt villages, lake towns) fit none of a-f. Recommend YES."),
 ("Split c", "c1 levee river / c2 braided, unbridged gravel river / c3 town river. The Oi, Abe, Sakawa and Fuji crossings have no bridge by shogunal policy and are a Tokaido signature. Recommend YES."),
 ("b stays a Kyoto hero", "the Takase gets its own look (8 m, 30 cm of water, funairi basins), but it is built from a's wall, step and bridge parts at low heights; Fushimi and Ogaki reuse it. Recommend YES."),
 ("Where the water comes from", "coastal canal towns (Edo, Osaka, Sakai, Nagoya if on the bay) sit at 1-3 m and their canals are cut below sea level, so real sea water fills them; everything inland uses pond models. Recommend YES, and a map rule: every a-type city touches the coast."),
 ("Abandoned water levels", "sea-level canals full, with exposed silt at the wall foot; the Takase and d2 street channels near-dry (no one keeps the intakes); moats full but green and lotus-choked; springs (d3) keep running. Recommend YES."),
 ("Street channels", "d1 gutters everywhere by default; a d2 mid-street channel only where sourced (Nakatsugawa, Narai, Tsumago, Magome, Suhara, Kamiyoshida's plot streams, Sakamoto). Recommend YES: a channel in every post town would be a modern Gujo / Tsuwano look."),
 ("Planting", "willow at canal corners and bridge ends; pines on levees and moat banks; wild cherries only on the Sumida levee (1717) and at temples; no cherry rows along canals (Kiyamachi and Ogaki rows are modern Somei-yoshino). Recommend YES."),
 ("Numazu", "had NO castle in 1730 (built 1777). Drop it from CASTLE_TOWNS and build a post town + river port. Recommend YES."),
 ("Two missing small castles", "Kano (Nakasendo, 1601) and Minakuchi (Tokaido, domain seat from 1682) were castle towns in 1730 but are not in CASTLE_TOWNS. Recommend: give each a small moat (f1) and gate, no keep. Low priority."),
 ("Engine test before any river", "a stepped pond-model river and a pond moat need one small test (swim depth, the joins at each step, drinking) on the test island before the c/b/f build lists. Recommend YES, one short agent session."),
]


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def check_coverage(rows):
    """Every map-sketch settlement must map to a row. Returns (missing, total)."""
    names = {fold(r["name"]).split(" (")[0]: r for r in rows}
    full = {fold(r["name"]): r for r in rows}
    alias = {"nihonbashi": "edo", "sanjo ohashi": "kyoto", "koraibashi": "osaka", "fuchu|TOKAIDO_ST": "sunpu",
             "fuchu|KOSHU": "fuchu", "kanagawa port": "kanagawa", "miya harbour": "miya", "koya": "koya",
             "ise (uji-yamada)": "ise", "seki|VILLAGES": "seki", "wada|VILLAGES": "wada", "warabi|VILLAGES": "warabi",
             "akasaka|NAKASENDO_ST": "akasaka", "fushimi|NAKASENDO_ST": "fushimi", "sakamoto|TEMPLE_TOWNS": "sakamoto", "kamiyoshida (fuji pilgrims)": "kamiyoshida"}
    sys.argv = ["x", "diag"]
    sys.path.insert(0, os.path.join(ROOT, "research", "map_sketch"))
    import map_sketch as M
    items = [(n, "CITIES") for n, *_ in M.CITIES]
    for t in ("CASTLE_TOWNS", "TOKAIDO_ST", "KYOKAIDO", "NAKASENDO_ST", "KOSHU", "ONSEN", "TEMPLE_TOWNS", "PORTS", "SALT"):
        items += [(n, t) for n, *_ in getattr(M, t)]
    vj = json.load(open(os.path.join(ROOT, "research", "map_sketch", "villages.json"), encoding="utf-8"))
    items += [(v["name"], "VILLAGES") for v in vj["villages"]]
    items += [("Nara", "L"), ("Ise (Uji-Yamada)", "L"), ("Koya", "L")]
    missing = []
    for n, t in items:
        k = fold(n)
        if k in full or k in names:
            continue
        a = alias.get(k + "|" + t) or alias.get(k)
        if a and (a in names or a in full):
            continue
        # rows carrying a disambiguating suffix, e.g. "Seki (Tokaido)"
        if any(fold(r["name"]).startswith(k + " (") for r in rows):
            continue
        missing.append((n, t))
    return missing, len(items)


def check_kit_ids():
    m = json.load(open(os.path.join(ROOT, "parts", "manifest.json"), encoding="utf-8"))
    ids = {p["id"] for p in m["parts"]}
    want = ["jp_p_found_step_natural", "jp_p_found_step_cut", "jp_p_found_dodai_stones_rough", "jp_p_found_dodai_stones_dressed",
            "jp_p_wall_okabe_kura", "jp_p_wall_namako_imo", "jp_p_wall_namako_shihan", "jp_p_open_kura_door_open",
            "jp_p_open_kura_door_hinged"]
    water_like = sorted(i for i in ids if any(w in i for w in ("canal", "quay", "gangi", "moat", "bridge", "revet", "water", "weir", "sluice")))
    return [w for w in want if w not in ids], water_like, len(ids)


def md_escape(s):
    return s.replace("|", "/")


def main():
    rows = parse()
    missing, n_items = check_coverage(rows)
    kit_missing, kit_water, n_kit = check_kit_ids()
    tname = {t["code"]: t["name"] for t in TYPES}

    prim = collections.Counter(r["primary"] for r in rows)
    anyc = collections.Counter()
    for r in rows:
        for c in {t[0] for t in r["types"]}:
            anyc[c] += 1
    varc = collections.Counter(t for r in rows for t in r["types"])
    waterc = collections.Counter(r["water"] for r in rows)
    FLAGWORDS = ("NO castle", "NOT A SETTLEMENT", "FITS NONE", "missing from")
    for r in rows:
        r["is_flag"] = any(k in r["flag"] for k in FLAGWORDS)
    flags = [r for r in rows if r["is_flag"]]

    # ---------------------------------------------------------------- JSON
    data = {
        "version": 1, "date": "2026-09-29", "author": "research agent WW",
        "note": "Town waterway types for 1730, the parts they need and every map-sketch settlement mapped to types. "
                "Generated by research/waterways/tools/gen_waterways.py from ww_types.py and ww_settlements.py.",
        "decisions": [{"n": i + 1, "topic": a, "recommendation": b.replace("{G}", str(prim.get("g", 0)))} for i, (a, b) in enumerate(DECISIONS)],
        "types": TYPES,
        "parts": PARTS,
        "settlements": rows,
        "counts": {"settlements": len(rows), "map_sketch_items_checked": n_items, "unmapped": missing,
                   "primary": dict(sorted(prim.items())), "any": dict(sorted(anyc.items())),
                   "variants": dict(sorted(varc.items())), "water": dict(waterc)},
        "sources": {k: {"what": v[0], "url": v[1]} for k, v in SOURCES.items()},
        "refs": [dict(file=f, title=t, maker=m, date=d, shows=s, licence=l, url=u) for f, t, m, d, s, l, u in REFS],
        "kit_check": {"cited_ids_missing": kit_missing, "waterway_parts_in_kit": kit_water, "kit_parts": n_kit},
    }
    open(os.path.join(WW, "waterways.json"), "wb").write(json.dumps(data, ensure_ascii=False, indent=1).encode("utf-8"))

    # ---------------------------------------------------------------- MD
    L = []
    w = L.append
    w("# Town waterways, 1730: types, parts and every settlement mapped")
    w("")
    w("Research agent WW, 2026-09-29. Research only: nothing is modelled. Data: `waterways.json` (types, parts, settlement "
      "-> types). Generated by `tools/gen_waterways.py`: edit `tools/ww_types.py` / `tools/ww_settlements.py` and rerun. "
      "Images: `data/research_ww/refs/` (licences in `CREDITS.md`).")
    w("")
    w("**Binding rules applied:** the era test (existed or still standing in 1730); a dead world 0-2 years abandoned; autumn; "
      "loot tiers ignored. **Dating caution (PLAYBOOK 1):** Hiroshige (1830s-50s), Morse (1886) and the surviving 'old canals' "
      "(Kurashiki, Kyoto Shirakawa, Kanazawa) are used for form and mood only, never to date a feature. The prints dated before "
      "1730 are scarce: the Toyoharu (1764-72), Harunobu (c.1767) and Eiri (1796-1801) prints are the closest.")
    w("")
    w("## Decisions for Stephen (one line each, with my recommendation)")
    w("")
    for i, (a, b) in enumerate(DECISIONS):
        w("%d. **%s:** %s" % (i + 1, a, b.replace("{G}", str(prim.get("g", 0)))))
    w("")
    w("## The seven types at a glance")
    w("")
    w("| Type | Name | Variants | Settlements (primary / any) | Water |")
    w("|---|---|---|---|---|")
    for t in TYPES:
        c = t["code"]
        w("| **%s** | %s | %s | %d / %d | %s |" % (c, md_escape(t["name"]), "<br>".join(md_escape(v) for v in t["variants"]),
                                              prim.get(c, 0), anyc.get(c, 0), md_escape(t["water_short"])))
    w("")
    w("Counts are over **%d settlements** (the %d map-sketch entries with duplicates merged: e.g. Nihonbashi = Edo, Fuchu = Sunpu, "
      "Kanagawa port = Kanagawa). 'Primary' = the waterway that defines the place; 'any' = the type appears there at all. "
      "Every town also has **d1** house-front gutters (the existing `jp_s_gutter` kit), so d's 'any' count understates it. "
      "Water surface needed: %s." % (len(rows), n_items, ", ".join("%s %d" % (k, v) for k, v in waterc.most_common())))
    w("")
    w("Variant counts (any): " + ", ".join("%s %d" % (k, v) for k, v in sorted(varc.items())) + ".")
    w("")
    w("### What changed from the starting set")
    w("- **(g) added:** ports, fishing and salt villages and lake towns had no home in a-f.")
    w("- **(c) split in three:** the levee river, the unbridged braided river and the small town river look and play differently "
      "(long bridge / porters / one plank bridge).")
    w("- **(d) widened:** it now covers spring streams (Mishima, Samegai, Tarui), hot-water gutters (spa towns) and "
      "Kamiyoshida's plot streams, which are all 'water that runs with the street'.")
    w("- **(f) gained dry and round moats:** the five hill and spur castles have dry moats; Tanaka's four round moats are unique.")
    w("- **(b) kept but small:** it is really one place (Kyoto), plus Fushimi and Ogaki.")
    w("")
    w("## The types in detail")
    w("")
    for t in TYPES:
        w("### (%s) %s" % (t["code"], t["name"]))
        w("")
        w(t["what"])
        w("")
        for v in t["variants"]:
            w("- " + v)
        w("")
        w("**Cross-section**")
        w("")
        w("| Dimension | Value | Source or reason |")
        w("|---|---|---|")
        for a, b, c in t["cross_section"]:
            w("| %s | %s | %s |" % (md_escape(a), md_escape(b), md_escape(c)))
        w("")
        for key, lab in (("edges", "Edges and revetment"), ("steps_landings", "Steps and landings"), ("mooring", "Mooring"),
                         ("outfalls", "Outfalls"), ("bridges", "Bridges"), ("planting", "Planting"),
                         ("buildings", "How buildings meet the water"), ("boats", "Boats"), ("abandoned", "Abandoned state (0-2 years, autumn)"),
                         ("terrain", "[terrain] work"), ("placeable", "Placeable models"), ("water", "Water surface")):
            w("- **%s:** %s" % (lab, t[key]))
        if t["refs"]:
            w("- **Refs:** " + ", ".join("`%s`" % r for r in t["refs"]) + " (see References)")
        w("")
    # parts
    w("## Parts list")
    w("")
    w("Status: **kit** = exists in `parts/manifest.json` or the outdoor core kit build list; **catalogued** = named in a KEEP "
      "list or OUTDOOR_LIST section 7 but no build list yet; **new** = in no list (or only as a `[terrain]` tag). The parts "
      "kit (`parts/manifest.json`, %d parts) is building parts only: it holds **no waterway part** (checked by name: %s). "
      "Suggested ids use `jp_s_ww_*` (site objects, waterway group)." % (n_kit, ", ".join(kit_water) or "none"))
    w("")
    w("| Id | Part | Status | Cross-reference | Sizes | Variants (incl. abandoned) | Types |")
    w("|---|---|---|---|---|---|---|")
    for p in PARTS:
        w("| `%s` | %s | %s | %s | %s | %s | %s |" % (p["id"], md_escape(p["name"]), p["status"], md_escape(p["xref"]),
                                                   md_escape(p["sizes"]), md_escape(p["variants"]), ", ".join(p["types"])))
    w("")
    sc = collections.Counter(p["status"] for p in PARTS)
    w("**Totals:** %d entries: %d new, %d catalogued, %d kit. The new ones are the **rough bank wall, the timber revetment, "
      "the landing stage, the wash step, debris and levee steps**; the catalogued ones most needed first are the dressed wall, gangi, "
      "mooring set, slab bridge and the boats. KEEP_OUTDOOR's budget covers them: 'canals and boats' (8), 'wells, water control, "
      "river works' (15), 'bridges and crossings (unbuilt)' (8)." % (len(PARTS), sc["new"], sc["catalogued"], sc["kit"]))
    w("")
    w("**Materials this adds** (beyond `jp_common` and the outdoor kit's 13): a wet-stone waterline band (dark wet stone + algae "
      "green, as a decal), a silt / mud ground texture for exposed canal beds, a rotten wet-timber variant, a floating leaf-mat "
      "decal, and clutter for reeds, water celery and dead lotus (flora list).")
    w("")
    w("**Build order (suggested):** 1) the engine test (decision 10); 2) dressed + rough wall modules, gangi, mooring, outfall, slab "
      "bridge (they serve a, b, d, e, f, g); 3) timber revetment, landing, wash step; 4) boats with dead states; 5) debris; "
      "6) the river-works kit and levee steps with the first c build.")
    w("")
    # settlements
    w("## Every settlement mapped to a type")
    w("")
    w("Grouped by **primary** type. `Listed`: C cities, CT castle towns, T Tokaido, K Kyokaido, N Nakasendo, KO Koshu, "
      "O onsen, TT temple towns, P ports, S salt, V villages.json (kind), L KEEP_LANDMARKS; `*` = KEY_POST. `Water`: sea = "
      "sea-level water (free), pond = pond models, lake = a lake pond, none = no water surface needed (dry beds, gutters, "
      "thin decals). Source `mem` = general knowledge not re-checked: verify before a build list relies on it.")
    w("")
    if missing:
        w("**Unmapped map-sketch entries: %s**" % ", ".join("%s (%s)" % m for m in missing))
    else:
        w("Coverage check: all %d map-sketch entries map to a row (the generator checks this)." % n_items)
    w("")
    order = [t["code"] for t in TYPES] + ["none"]
    for c in order:
        grp = [r for r in rows if r["primary"] == c]
        if not grp:
            continue
        w("### Primary (%s) %s: %d" % (c, tname.get(c, "fits no type"), len(grp)))
        w("")
        w("| Settlement | Listed | Types | Real waterway(s) | Source | Water |")
        w("|---|---|---|---|---|---|")
        for r in grp:
            nm = r["name"] + (" **[FLAG]**" if r["is_flag"] else "")
            ww = r["waterway"] + ((" *Note: %s*" % r["flag"]) if r["flag"] and not r["is_flag"] else "")
            w("| %s | %s | %s | %s | %s | %s |" % (md_escape(nm), r["listed"], ", ".join(r["types"]) or "-",
                                               md_escape(ww), " ".join(r["sources"]), r["water"]))
        w("")
    w("### Flags (settlements that fit no type, or where the map sketch is wrong for 1730)")
    w("")
    for r in flags:
        w("- **%s:** %s" % (r["name"], r["flag"]))
    w("")
    w("## References")
    w("")
    w("Images in `data/research_ww/refs/` (period prints first; dates matter: only form, never dating, from anything after 1750).")
    w("")
    w("| File | Title | Maker | Date | Shows |")
    w("|---|---|---|---|---|")
    for f, t, m, d, s, l, u in REFS:
        w("| `%s` | %s | %s | %s | %s |" % (f, md_escape(t), md_escape(m), d, md_escape(s)))
    w("")
    w("Linked only (read, not downloaded):")
    w("")
    for t, u in LINKED_ONLY:
        w("- %s: %s" % (t, u))
    w("")
    w("Text sources (keys used above):")
    w("")
    w("| Key | What | Where |")
    w("|---|---|---|")
    for k, (a, b) in SOURCES.items():
        w("| %s | %s | %s |" % (k, md_escape(a), md_escape(b)))
    w("")
    w("## Open questions")
    w("")
    w("- **Engine:** can a player swim in a pond model, how deep must it be, and do stepped pond segments join cleanly? "
      "(FEASIBILITY 2.3 lists this as unverified; the test pond only proved 'visible and drinkable'.)")
    w("- **Kusatsu-onsen's yubatake** trough field: its 1730 form (verify before d4 copies it).")
    w("- **Omi kabata** (spring house-basins): start date unknown; kept as lake-village flavour only.")
    w("- **Canal depths and the back-canal width** are assumed; a primary Edo or Osaka survey (e.g. the Osaka sanjugo-machi "
      "maps or the Edo kiriezu) would pin them.")
    w("- **Every `mem` row**: the rivers named for ordinary post towns come from general knowledge. They only change which "
      "c3 or e piece goes where, not the type counts much.")
    w("")
    open(os.path.join(WW, "WATERWAYS.md"), "wb").write(("\n".join(L) + "\n").encode("utf-8"))

    # ---------------------------------------------------------------- CREDITS
    C = ["# Credits: waterway research images (agent WW, 2026-09-29)", "",
         "Every downloaded image, with its licence. Downloaded with the generic User-Agent `JapanDevResearch/1.0 (DayZ mod research)`; "
         "no personal information was sent. Nothing was downloaded from upload.wikimedia.org.", "",
         "| File (data/research_ww/refs/) | Title | Maker | Date | Licence | Source |", "|---|---|---|---|---|---|"]
    for f, t, m, d, s, l, u in REFS:
        C.append("| %s | %s | %s | %s | %s | %s |" % (f, md_escape(t), md_escape(m), d, l, u))
    C += ["", "Library of Congress Prints & Photographs, Japanese Fine Prints (jpd): the collection states 'No known restrictions on "
          "publication'. Morse figures: Project Gutenberg #52868, public domain in the USA; the 1886 originals are public domain worldwide.", "",
          "Linked only, not downloaded: see WATERWAYS.md 'References'. The Met Open Access search was tried (CC0) but its search "
          "returned mostly off-topic objects and then failed mid-run, so no Met image was kept.", ""]
    open(os.path.join(WW, "CREDITS.md"), "wb").write("\n".join(C).encode("utf-8"))

    print("rows", len(rows), "items", n_items, "missing", missing)
    print("primary", dict(prim)); print("any", dict(anyc)); print("water", dict(waterc))
    print("kit missing", kit_missing, "kit water-like", kit_water)
    print("parts", dict(sc))


if __name__ == "__main__":
    main()
