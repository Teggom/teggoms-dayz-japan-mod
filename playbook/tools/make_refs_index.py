"""Write playbook/refs_index.json: every text source and image used by the playbook v1.

Images come from data/playbook/refs_images.json (written by fetch_refs.py). Text sources are listed here.
IDs: T## = text, image ids = the local file stem (c## Commons, m## Met).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PB = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(PB, ".."))

W = "https://en.wikipedia.org/wiki/"
J = "https://ja.wikipedia.org/wiki/"
TEXT = [
    ("T01", W + "Tatami", "CC BY-SA (text, cited not copied)", "Tatami sizes: kyoma 1.91x0.955 m, chukyoma 1.82x0.91, edoma 1.76x0.88; reached commoners' homes toward the end of the 17th c."),
    ("T02", W + "Ken_(unit)", "CC BY-SA", "Ken = 6 shaku = 1.82 m; ~1.97 m under Hideyoshi; reduced to 1.818 m c.1650"),
    ("T03", J + "京間", "CC BY-SA", "Kyoma: ken 6.5 shaku, tatami 6.3 x 3.15 shaku, tatami-based planning vs Edo column-based (inakama); term attested 1608"),
    ("T04", W + "Machiya", "CC BY-SA", "Plot 5.4-6 m wide x ~20 m deep; mushiko-mado; 1, 1.5 or 2 storeys; bengara koshi"),
    ("T05", J + "町屋_(商家)", "CC BY-SA", "Low tsushi-nikai (regulated), board/kokera roofs early, 1720 (Kyoho 5) tile + dozo encouragement, udatsu, facade elements, Kyoto vs Edo (dashigeta) differences"),
    ("T06", "https://www.aisf.or.jp/~jaanus/deta/s/sangawara.htm", "JAANUS (reference)", "Sangawara = pan and roll combined in one tile"),
    ("T07", J + "桟瓦", "CC BY-SA", "Sangawara invented 1674 by Nishimura Hanbei (Miidera); lighter than hongawara; commoner tile roofs first restricted, later encouraged"),
    ("T08", "https://www.aisf.or.jp/~jaanus/deta/u/udatsu.htm", "JAANUS", "Udatsu: machiya gable parapet; Edo-period fireproof tiled and plastered form, status symbol"),
    ("T09", "https://www.aisf.or.jp/~jaanus/deta/m/mushikomado.htm", "JAANUS", "Mushiko-mado: plastered slatted window lighting the low upper storey (zushi)"),
    ("T10", "https://www.aisf.or.jp/~jaanus/deta/h/hongawarabuki.htm", "JAANUS", "Hongawara: flat pans + semicylindrical covers; special eave, ridge, verge tiles"),
    ("T11", J + "木戸番", "CC BY-SA", "Kido gates at both ends of each cho in Edo/Kyoto/Osaka; guard hut 6 x 9 shaku, eave 10 shaku; closed about 10 pm, wicket door after"),
    ("T12", "https://kotobank.jp/word/%E7%81%AB%E3%81%AE%E8%A6%8B%E6%AB%93-120594", "Kotobank (reference)", "Jobikeshi towers from 1658, 3 jo (~9 m), plain wood; daimyo and town towers black and lower; Kyoho: one tower per ~10 cho, ladders on jishinban"),
    ("T13", "http://www.hetima.net/firetower/reference/history/", "web page", "Fire-tower history (corroborates T12)"),
    ("T14", J + "御土居", "CC BY-SA", "Kyoto Odoi 1591: 22.5 km, base ~20 m, top ~5 m, height ~5 m, moat 10-15 m, bamboo on top, 10 gates, opened up in the Edo period"),
    ("T15", J + "箱根関所", "CC BY-SA", "Hakone checkpoint c.1619-1869: two gates ~18 m apart, guard houses, palisades, lookout; 'iri-deppo ni de-onna'; 1686 staffing"),
    ("T16", W + "J%C5%8Dkamachi", "CC BY-SA", "Castle-town zoning (samurai, chonin, temple districts); walls mostly only around the castle, some sogamae; masugata gates, cranked streets"),
    ("T17", W + "Minka", "CC BY-SA", "Doma earth floor, hiroma raised ~50 cm, roof types, irori, status markers (ridge members, udatsu)"),
    ("T18", W + "Shukuba", "CC BY-SA", "Post-station facilities: honjin, waki-honjin, hatago, kichin-yado, chaya, toiyaba, kosatsu"),
    ("T19", J + "本陣", "CC BY-SA", "Honjin reserved features: front gate, shikidai genkan, jodan-no-ma; system from 1634-35"),
    ("T20", J + "伝馬制", "CC BY-SA", "Tokaido 100 porters + 100 horses per station (1638); Kiso/Nakasendo 50 + 50"),
    ("T21", J + "問屋場", "CC BY-SA", "Toiyaba = relay office for horses/porters; surviving examples Fuchu, Narai, Samegai"),
    ("T22", J + "一里塚", "CC BY-SA", "Ichirizuka ordered 1604; paired mounds ~5 ken square, 1 jo high, every ri (~3.9 km); trees: enoki 55 %, pine 27 %, cedar 8 %"),
    ("T23", J + "高札", "CC BY-SA", "Kosatsu boards at kosatsuba (Nihonbashi, Sanjo bridge...); 1711 Shotoku boards stayed up to the end of Edo"),
    ("T24", J + "見附", "CC BY-SA", "Mitsuke: guarded gates (Edo castle's 36 mitsuke) and guard posts on roads"),
    ("T25", J + "杉玉", "CC BY-SA", "Sugidama at sake breweries from the early Edo period; green when new, browns with age"),
    ("T26", J + "曲り家", "CC BY-SA", "Magariya: L-plan farmhouse with stable, 18th c., Nanbu (Iwate)"),
    ("T27", J + "銭湯", "CC BY-SA", "First Edo bathhouse 1591; zakuro-guchi; upper-floor rest room for men; 1791 mixed-bathing ban"),
    ("T28", J + "陣屋", "CC BY-SA", "Jinya: single-compound administrative seat (office, residence, storehouses, walls, gate); Takayama Jinya"),
    ("T29", J + "長屋門", "CC BY-SA", "Nagaya-mon: plaster walls allowed for samurai residences, boards for commoners"),
    ("T30", J + "旅籠", "CC BY-SA", "Hatago: two-storey, lattice fronts, 200-300 mon/night, ~3,000 on the Tokaido"),
    ("T31", J + "町奉行", "CC BY-SA", "Edo north/south machi-bugyo; ~250 staff for 500,000 townspeople"),
    ("T32", W + "T%C5%8Dr%C5%8D", "CC BY-SA", "Stone lantern parts and types (kasuga, yukimi, ikekomi, oki)"),
    ("T33", W + "Torii", "CC BY-SA", "Torii parts; shinmei vs myojin families; vermilion pillars, black only on kasagi/nemaki; stone torii since the 12th c."),
    ("T34", J + "石垣", "CC BY-SA", "Nozura-zumi, uchikomi-hagi, kirikomi-hagi; less stone walling in east Japan"),
    ("T35", J + "道祖神", "CC BY-SA", "Dosojin at village edges, passes, crossroads; most surviving are Edo/Meiji; Nagano densest"),
    ("T36", J + "墓石", "CC BY-SA", "Commoner stone grave markers spread in the Edo period (danka system); family graves from mid-Meiji"),
    ("T37", J + "登り窯", "CC BY-SA", "Multi-chamber climbing kiln standard in the Edo period"),
    ("T38", J + "水車", "CC BY-SA", "Waterwheels widespread in the Edo period for rice polishing/milling"),
    ("T39", "https://wafujyutaku.jp/japanese-style-room-cat/uchinori", "web page", "Uchinori (door-head) height traditionally 5 shaku 7 sun (~1.73 m); 8 shaku (2.42 m) ceilings"),
    ("T40", "http://amenomichi.com/nihon/kioka13.html", "web page (Kioka Takao)", "Stone-weighted board roofs ~3.5 sun (~20 deg); late 17th c. sangawara displaced board roofs in Edo"),
    ("T41", "https://online.bunka.go.jp/suisensyo/shirakawago/MAINTEXT/outline4-j.html", "Agency for Cultural Affairs", "Ordinary thatched minka mostly <= 45 deg; gassho near 60 deg (read via search summary)"),
    ("T42", J + "勾配", "CC BY-SA", "Sun-kobai: rise in sun per 1 shaku run; 3 sun ~17 deg"),
    ("T43", "https://www.kenohare.com/kyo-machiya-5features/", "web page", "Zushi-nikai: street-side upper storey 1.5-1.8 m high; storage/servants; mushiko windows"),
    ("T44", "https://crd.ndl.go.jp/reference/detail?page=ref_view&id=1000270298", "NDL Collaborative Reference DB", "Why the Edo-period zushi-nikai ceiling was low (question record)"),
    ("T45", "https://www.hachise.jp/kyomachiya/isho/isho_1.html", "web page (Hachise)", "Zushi-nikai design notes (Kyoto machiya)"),
    ("T46", "https://solidwood.jp/iroha/timber/timber-size-name", "web page", "Post sizes: 3.5 sun (10.5 cm) and 4 sun (12 cm) standard"),
    ("T47", "https://sakujigumi.com/sakujiwiki/daikokubashira", "Kyomachiya Sakujigumi glossary", "Daikokubashira: larger central post on the toriniwa side"),
    ("T48", "https://www.touken-world.jp/tips/51221/", "web page", "1668 (Kanbun 8) Edo townsmen house rules: no nageshi, sugito, tsuke-shoin, carving, karakami; 3-ken beam-span limit"),
    ("T49", J + "奢侈禁止令", "CC BY-SA", "1683 ban on gold thread, embroidery, so-kanoko for townspeople; 1745 townspeople limited to silk, tsumugi, cotton, hemp; 'shijuhacha hyakunezumi'"),
    ("T50", W + "Obi_(sash)", "CC BY-SA", "Women's obi ~25 cm in the 1730s; men's widest ~16 cm in the 1730s; tied at the back by the end of the 17th c."),
    ("T51", W + "Kosode", "CC BY-SA", "Kosode: small sleeve openings, sleeves sewn to the body, rounded outer edges"),
    ("T52", J + "日本の色の一覧", "CC BY-SA", "Dictionary hex values for traditional colour names (used only where no photo sample)"),
    ("T53", "https://japan-heritage.bunka.go.jp/ja/culturalproperties/result/3884/", "Agency for Cultural Affairs", "Hakone road paved with stone in 1680, 2 ken (~3.6 m) wide, kerb stones 30-70 cm (read via search summary)"),
    ("T54", "https://kotobank.jp/word/%E5%A4%A7%E5%85%AB%E8%BB%8A-558136", "Kotobank", "Daihachiguruma handcart after the 1657 fire; bed 8 x 2.5 shaku, wheels 3.5 shaku; 1,273 in Edo in 1703"),
    ("T55", W + "Koi", "CC BY-SA", "Coloured nishikigoi arose in Niigata in the early 19th c. (so: none in a 1730 world)"),
    ("T56", J + "長屋", "CC BY-SA", "Nagaya form: shared walls, own entrance, kitchen at the door, 1-2 rooms"),
    ("T57", W + "Honjin", "CC BY-SA", "Honjin for daimyo/officials only; waki-honjin could take others"),
    ("T58", "https://www.woodtec.co.jp/lab/flooring/history/02/", "web page", "Tatami reached ordinary commoners' homes by the late Edo period"),
    ("T59", "https://www.gutenberg.org/ebooks/author/2436", "Public domain (1886 book)", "E. S. Morse, 'Japanese Homes and Their Surroundings': drawings of ridges, gables, kura, inns (images c26-c28)"),
    ("T60", "spikes/A_arms/katana_v2/DOSSIER.md", "internal", "Research process template; iron colour (76,72,69); photo-sampling lessons"),
    ("T61", "spikes/B_building/REPORT.md", "internal", "Engine facts: LOD set, doors (translation), roadway, fire materials, 0.8/1.0 m doors, 38-40 deg stair, house_1w01 face counts 2019/777/262"),
    ("T62", "spikes/W_wearables/REPORT.md", "internal", "DayzTemporarySkeleton, worn/ground LOD sets, long robe fails in motion, hakama per-leg method, kimono tri counts"),
    ("T63", "spikes/F_flora/REPORT.md", "internal", "TreeAdv rvmats copy vanilla blocks, autocenter=0, sakura LOD1 7.1k tris heavy"),
]


def main():
    with open(os.path.join(ROOT, "data", "playbook", "refs_images.json"), "rb") as f:
        imgs = json.loads(f.read().decode("utf-8"))
    doc = {
        "version": 1,
        "note": "Images are local only (data/playbook/refs/, git-ignored, never shipped). Text sources are cited, not copied.",
        "download_policy": "Only PD / CC0 / CC BY images (no SA/NC/ND). Commons via API with a descriptive User-Agent; Met via Open Access API, <= 1 request / 3 s.",
        "images": imgs,
        "text": [{"id": i, "url": u, "licence": l, "supports": s} for i, u, l, s in TEXT],
    }
    with open(os.path.join(PB, "refs_index.json"), "wb") as f:
        f.write(json.dumps(doc, indent=1, ensure_ascii=False).encode("utf-8"))
    print(len(imgs), "images,", len(TEXT), "text")


if __name__ == "__main__":
    main()
