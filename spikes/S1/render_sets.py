#!/usr/bin/env python3
r"""render_sets.py - the S1 contact sheets: every shop set on the reference shell (Kamigata 3-ken middle, toriniwa
left, with the board display strip), rendered with C3's Blender side (spikes/C3/render_c3.py blender_main, read-only),
beside the local period references.

  python spikes/S1/render_sets.py [--jobs N] [--compose] [trade ...]
  -> spikes/S1/renders/sets/<view>_<trade>.png, research/interior/contact_sheets/s1_sets_<n>.jpg (6 trades a sheet)

Per trade: (1) the shop room from inside (toriniwa side, eye height), (2) the house cut at 2.3 m from the street side,
(3) the street front with the signs, (4) the nearest local reference + the set's signature items, sign and verdict.
The preview shells are temporary registry entries 's1pv_<trade>' made in the Blender process only (never shipped).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
C3 = os.path.join(DEV, "spikes", "C3")
OUT = os.path.join(HERE, "renders", "sets")
SHEETS = os.path.join(DEV, "research", "interior", "contact_sheets")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
BASE = "th_kamigata_3k_middle_toril"
REFS = {   # trade -> (reference image under data/, caption)
    "draper": ("research_int/refs/i13_echigoya_1768.jpg", "i13 Echigoya draper, 1768: clerks on the raised floor"),
    "furugi": ("research_ext/refs/x31_masanobu_ryogoku_1748.jpg", "x31 Masanobu, Ryogoku 1748: street shops"),
    "honya": ("research_ext/refs/x33_jinrin_bookseller_1690.jpg", "x33 Jinrin kinmozui 1690: bookseller, goods on "
              "the raised floor"),
    "kamiya": ("research_ext/refs/x33_jinrin_bookseller_1690.jpg", "x33 1690 shop front: goods on the floor edge"),
    "sakaya": ("research_int/refs/i50_met_tokkuri_stoneware.jpg", "i50 stoneware tokkuri (Met), 1700-1750"),
    "nimeuri": ("research_int/refs/i51_met_tokkuri_porcelain.jpg", "i51 porcelain tokkuri (Met)"),
    "tabako": ("research_ext/refs/x32_shigenaga_kamo_1740s.jpg", "x32 Shigenaga 1740s: street with shops"),
    "setomono": ("research_int/refs/i51_met_tokkuri_porcelain.jpg", "i51 blue-and-white porcelain (Met)"),
    "kanamono": ("research_int/refs/i16_moronobu_1685_p6.jpg", "i16 Moronobu 1685: craftsmen at work"),
    "nushi": ("research_int/refs/i17_moronobu_1685_p7.jpg", "i17 Moronobu 1685: workshop scene"),
    "kushiya": ("research_int/refs/i15_moronobu_1685_p5.jpg", "i15 Moronobu 1685: workshop scene"),
    "shitate": ("research_int/refs/i18_moronobu_1685_p9.jpg", "i18 Moronobu 1685: workshop scene"),
    "eshi": ("research_int/refs/i18_moronobu_1685_p9.jpg", "i18 Moronobu 1685: workshop scene"),
    "fukuromono": ("research_int/refs/i16_moronobu_1685_p6.jpg", "i16 Moronobu 1685: craftsmen at work"),
    "hataori": ("research_int/refs/i17_moronobu_1685_p7.jpg", "i17 Moronobu 1685: workshop scene"),
    "tabidogu": ("research_ext/refs/x30_shinagawa_1726.jpg", "x30 Shinagawa 1726: Tokaido street shops"),
    "soba": ("research_ext/refs/x32_shigenaga_kamo_1740s.jpg", "x32 Shigenaga 1740s: street with shops"),
    "mochiya": ("research_ext/refs/x30_shinagawa_1726.jpg", "x30 Shinagawa 1726: Tokaido street shops"),
}
DEFAULT_REF = ("research_ext/refs/x30_shinagawa_1726.jpg", "x30 Shinagawa 1726: Tokaido street shops")


def trades():
    sys.path[:0] = [os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit")]
    import shop_sets
    return shop_sets.TRADES


def jobs_for(keys):
    out = []
    for t in keys:
        k = "s1pv_" + t
        out.append(("in_" + t, t, {"key": k, "cam": [0.65, 1.95, 3.35], "look": [-2.3, 0.75, 1.9], "lens": 15,
                                   "site": False, "open": 1.0, "res": [960, 640]}))
        out.append(("cut_" + t, t, {"key": k, "cam": [-0.6, 8.8, 6.0], "look": [-0.9, 0.4, 2.0], "lens": 24,
                                    "cut_y": 2.3, "site": True, "res": [960, 640]}))
        out.append(("front_" + t, t, {"key": k, "cam": [-5.8, 1.7, 8.6], "look": [-0.6, 2.0, 4.0], "lens": 22,
                                      "site": True, "res": [960, 640]}))
    return out


def blender_side(jf):
    sys.path[:0] = [C3, os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"),
                    os.path.join(DEV, "spikes", "B_building", "kit")]
    import render_c3
    import registry
    jobs = json.load(open(jf, encoding="utf-8"))
    seen = {b["key"] for b in registry.BUILDINGS}
    for _, t, v in jobs:
        if v["key"] not in seen:
            b = registry._furn(v["key"], BASE, "shop_%s_3k_ab0" % t, "S1pv", "S1 set preview")
            b["ship"] = False
            registry.BUILDINGS.append(b)
            seen.add(v["key"])
    render_c3.OUT = OUT
    render_c3.blender_main([[o, c, v] for o, c, v in jobs])


def run(jobs, n):
    os.makedirs(OUT, exist_ok=True)
    procs = []
    for i in range(n):
        part = jobs[i::n]
        if not part:
            continue
        jf = os.path.join(OUT, "_jobs_%d.json" % i)
        with open(jf, "wb") as f:
            f.write(json.dumps(part).encode("utf-8"))
        lf = open(os.path.join(OUT, "_blender_%d.log" % i), "wb")
        procs.append((subprocess.Popen([BLENDER, "--background", "--factory-startup", "--python",
                                        os.path.abspath(__file__), "--", "--blender", jf], stdout=lf,
                                       stderr=subprocess.STDOUT, cwd=DEV), lf))
    for p, lf in procs:
        p.wait()
        lf.close()


def compose(keys, T):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    F = {k: ImageFont.truetype(f, s) for k, (f, s) in {"h1": (r"C:\Windows\Fonts\arialbd.ttf", 30),
                                                      "b": (r"C:\Windows\Fonts\arialbd.ttf", 19),
                                                      "s": (r"C:\Windows\Fonts\arial.ttf", 15)}.items()}
    sys.path.insert(0, os.path.join(DEV, "spikes", "S1"))
    sc = json.load(open(os.path.join(HERE, "setcheck.json"), encoding="utf-8")) if os.path.isfile(
        os.path.join(HERE, "setcheck.json")) else {}
    CW, CH, RW = 480, 320, 520
    outs = []
    for si in range(0, len(keys), 6):
        chunk = keys[si:si + 6]
        W = 3 * CW + RW + 5 * 8
        H = 100 + len(chunk) * (CH + 12)
        im = Image.new("RGB", (W, H), (236, 234, 229))
        d = ImageDraw.Draw(im)
        d.text((12, 10), "S1 shop sets %d: %s" % (si // 6 + 1, ", ".join(chunk)), font=F["h1"], fill=(20, 20, 20))
        d.text((12, 52), "Each set on the reference shell (Kamigata 3-ken middle, toriniwa left, board display strip), "
               "ab 0 (as shut). Left: the shop room from the toriniwa side. Middle: the house cut at 2.3 m from above. Right: the "
               "street front from the shop end, with the signs (hanging signs project from the facade). Last column: the nearest local reference, the signature items, the sign, "
               "the 1730 verdict and the set checks (3k + 2k, ab 0-2).", font=F["s"], fill=(60, 60, 60))
        for r, t in enumerate(chunk):
            y = 92 + r * (CH + 12)
            for c, view in enumerate(("in", "cut", "front")):
                p = os.path.join(OUT, "%s_%s.png" % (view, t))
                x = 8 + c * (CW + 8)
                if os.path.isfile(p):
                    im.paste(Image.open(p).convert("RGB").resize((CW, CH)), (x, y))
            x = 8 + 3 * (CW + 8)
            rp, cap = REFS.get(t, DEFAULT_REF)
            rp = os.path.join(DEV, "data", rp)
            try:
                ref = Image.open(rp).convert("RGB")
            except Exception:                # a saved HTML error page (B3a: i31, i35, i38)
                ref = None
            if ref is not None:
                ref.thumbnail((RW, 150))
                im.paste(ref, (x, y))
                d.text((x, y + ref.size[1] + 2), cap[:70], font=F["s"], fill=(70, 70, 70))
            yy = y + 172
            d.text((x, yy), T[t]["title"][:52], font=F["b"], fill=(20, 20, 20))
            yy += 24
            spec = T[t]
            items = list(dict.fromkeys(list(spec.get("steps", ())) + [s for s in spec.get("strip", []) if s != "stand"]
                                       + [spec.get("stock") or ""] + [spec.get("wall") or ""]))
            txt = "Set: " + ", ".join(i.replace("jp_f_", "").replace("jp_s_", "") for i in items if i)
            txt += ". Sign: " + ", ".join(f.replace("jp_f_", "").replace("jp_s_shopfront_", "") for f in
                                          spec.get("front", []) + [x_ for x_ in spec.get("door", []) if "sugi" in x_])
            txt += ". " + (spec.get("era") or "")
            ks = [k for k in sc if k.startswith("s1v_%s_" % t)]
            ok = sum(1 for k in ks if sc[k]["pass"])
            txt += " Set checks %d/%d." % (ok, len(ks))
            for ln in textwrap.wrap(txt, 68)[:7]:
                d.text((x, yy), ln, font=F["s"], fill=(40, 40, 40))
                yy += 17
        os.makedirs(SHEETS, exist_ok=True)
        dst = os.path.join(SHEETS, "s1_sets_%d.jpg" % (si // 6 + 1))
        im.save(dst, quality=86)
        outs.append(dst)
        print("sheet", dst, im.size)
    return outs


def main(argv):
    T = trades()
    keys = [a for a in argv if a in T] or list(T)
    n = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 6
    if "--compose" not in argv:
        run(jobs_for(keys), n)
    compose(keys, T)
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        blender_side(sys.argv[sys.argv.index("--blender") + 1])
    else:
        sys.exit(main(sys.argv[1:]))
