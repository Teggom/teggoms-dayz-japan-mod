#!/usr/bin/env python3
r"""W2F area renders + labelled maps, on spikes/SH1/render_sh1.py's Blender scene (imported, not edited).

  python spikes/W2F/render_w2f.py [precinct|temple|civic|maps ...] [--jobs N] [--compose] [--only a,b]

Scene: SH1's data (registry buildings + C3 / SH1 props + trees + terrain) PLUS the W2F placements
(spikes/W2F/w2f_items.json: the furnished buildings with their furniture and site objects, the terraces, the loose
dressing). Outputs: spikes/W2F/renders/*.png, research/production/contact_sheets/w2f_<set>.jpg and
w2f_map_<area>.jpg (IDs from w2f_items.json; table in spikes/SH1/SHOWCASE_MAP.md, W2F section).
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "SH1"))
import render_sh1 as R  # noqa: E402

R.OUT = os.path.join(HERE, "renders")
OUT = R.OUT
SHEETS = R.SHEETS
BLENDER = R.BLENDER
ITEMS = os.path.join(HERE, "w2f_items.json")


def items():
    with open(ITEMS, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def scene_data(region, pad=6.0):
    import terrain_sh1 as T
    d = R.scene_data(region, pad)
    x0, x1, z0, z1 = region
    for it in items():
        if not (x0 - pad - 8 <= it["x"] <= x1 + pad + 8 and z0 - pad - 8 <= it["z"] <= z1 + pad + 8):
            continue
        y = T.ground(it["x"], it["z"]) + it["y_off"]
        if it.get("key"):
            d["buildings"].append((it["key"], it["x"], y, it["z"], it["yaw"]))
        elif ".s" not in it["id"]:                    # site objects come with their building
            d["props"].append((os.path.basename(it["p3d"])[:-4], it["x"], y, it["z"], it["yaw"]))
    return d


def gy(x, z):
    import terrain_sh1 as T
    return T.ground(x, z)


def eye(x, z, h=1.7):
    return [x, gy(x, z) + h, z]


def at(x, z, h=1.2):
    return [x, gy(x, z) + h, z]


def jobs():
    P, T_, C, M = {}, {}, {}, {}
    r_p = (1000.0, 1040.0, 1140.0, 1214.0)
    r_t = (940.0, 992.0, 1098.0, 1132.0)
    r_u = (1076.0, 1124.0, 1090.0, 1124.0)
    r_e = (1056.0, 1100.0, 1066.0, 1094.0)
    r_w = (930.0, 984.0, 1056.0, 1094.0)
    data = {"p": scene_data(r_p), "t": scene_data(r_t), "u": scene_data(r_u), "e": scene_data(r_e),
            "w": scene_data(r_w)}

    def J(d, dk, out, cap, origin, **v):
        v["origin"] = list(origin)
        v["data"] = data[dk]
        d[out] = (out, cap, v)
    hb = gy(1024.0, 1192.0) + 0.0
    o = (1024.0, 1180.0)
    J(P, "p", "w2f_p1", "P1 + P2: up the approach to the town haiden on its stone terrace (P1t), the honden behind",
      o, cam=eye(1024, 1168), look=at(1024, 1196, 3.5), lens=24)
    J(P, "p", "w2f_p2", "P1 haiden front: the offering box at the stair foot, bell rope, Hachimangu name board",
      o, cam=eye(1023.0, 1182.4, 2.8), look=at(1024, 1191.0, 3.4), lens=22)
    hy = 28.343 + 0.75
    J(P, "p", "w2f_p3", "P1 inside the haiden: drum, offering table under the god shelf, candle stands, ritual chest, ema",
      o, cam=[1024.0, hy + 1.6, 1190.3], look=[1024.0, hy + 0.9, 1194.0], lens=14)
    J(P, "p", "w2f_p4", "P2 town honden (sealed sanctum, offering table on the en) on its higher terrace (P2t)",
      o, cam=eye(1030.0, 1196.0, 2.8), look=at(1024, 1206.5, 3.0), lens=20)
    J(P, "p", "w2f_p5", "West of the approach: P5 kagura stage, P4 shamusho, P3 temizuya", o,
      cam=eye(1019.0, 1194.0, 2.2), look=at(1011, 1170, 1.5), lens=22)
    J(P, "p", "w2f_p6", "P3 temizuya: the stone basin and the ladle rack", o, cam=eye(1018.2, 1149.0, 1.7),
      look=at(1014, 1147, 0.8), lens=22)
    J(P, "p", "w2f_p7", "Aerial of the precinct from the south-east", o, cam=[1058.0, 62.0, 1150.0],
      look=[1020.0, 28.0, 1184.0], lens=24)
    o = (965.0, 1115.0)
    J(T_, "t", "w2f_t1", "T4 gate (yakui-mon) and the village hondo T1 (Jodo) behind, lanterns T6/T7", o,
      cam=eye(972, 1098.5), look=at(972, 1122, 3.5), lens=22)
    J(T_, "t", "w2f_t2", "T1 inside: Amida in the zushi on the dais, canopy, sutra desk, candle stands", o,
      cam=[972.0, 25.6 + 1.6, 1120.4], look=[972.0, 26.4, 1126.6], lens=14)
    J(T_, "t", "w2f_t3", "T3 bell tower with the bell (struck from the platform), T2 kuri behind", o,
      cam=eye(989.5, 1104.5, 1.8), look=at(978, 1115, 2.5), lens=22)
    J(T_, "t", "w2f_t4", "T5 Jizo hall and the stone Jizo T8", o, cam=eye(969.5, 1105.5), look=at(962, 1109.5, 1.4),
      lens=22)
    J(T_, "t", "w2f_t5", "Aerial of the village temple (graveyard to the east)", o, cam=[1000.0, 48.0, 1090.0],
      look=[968.0, 25.0, 1116.0], lens=24)
    o = (1100.0, 1108.0)
    J(T_, "u", "w2f_u1", "U4 gate (shikyaku-mon), lanterns, the town hondo U1 (Zen)", o, cam=eye(1100, 1091.5),
      look=at(1100, 1112, 3.5), lens=22)
    J(T_, "u", "w2f_u2", "U1 inside: Shaka in the zushi, canopy, sutra desk, the big mokugyo, the drum", o,
      cam=[1100.0, 25.75 + 1.6, 1109.3], look=[1100.0, 26.6, 1114.7], lens=14)
    J(T_, "u", "w2f_u3", "U3 town bell tower (hakama, outside stair) and U5 Kannon hall", o, cam=eye(1092.5, 1099.0, 2.0),
      look=at(1084, 1112, 3.0), lens=22)
    J(T_, "u", "w2f_u4", "Aerial of the town temple", o, cam=[1128.0, 55.0, 1084.0], look=[1098.0, 25.0, 1110.0], lens=24)
    o = (1076.0, 1080.0)
    J(C, "e", "w2f_k1", "K1 the ward gate (kido) at the street's east end, hinged leaves, the keeper's hut", o,
      cam=eye(1059.5, 1079.0), look=at(1069, 1080, 2.0), lens=22)
    J(C, "e", "w2f_k2", "Outside the gate: K2 tea house (chamise), K3 bench tea house, K4 tateba", o,
      cam=eye(1072.0, 1079.0), look=at(1084, 1084, 1.8), lens=20)
    J(C, "e", "w2f_k3", "K2 inside: the kettle hearth, the bench with tea things, the raised room", o,
      cam=[1077.0, 25.0 + 1.65, 1084.4], look=[1075.0, 25.6, 1088.0], lens=14)
    J(C, "e", "w2f_k4", "Aerial of the east end", o, cam=[1100.0, 50.0, 1058.0], look=[1076.0, 25.0, 1082.0], lens=24)
    o = (965.0, 1078.0)
    J(C, "w", "w2f_k5", "K5 smithy: the cold forge, bellows, anvil, tool wall", o, cam=[968.0, 25.0 + 1.6, 1084.4],
      look=[971.2, 25.5, 1087.2], lens=14)
    J(C, "w", "w2f_k6", "West end: K7 jishin-ban with its ridge ladder, K6 swordsmith, K5 smithy", o,
      cam=eye(984.0, 1079.5, 1.8), look=at(970, 1078, 2.2), lens=20)
    J(C, "w", "w2f_k7", "K6 swordsmith forge room: forge, big bellows, anvil, quench trough, the rope over the forge", o,
      cam=[968.6, 25.0 + 1.6, 1071.9], look=[966.2, 25.4, 1069.3], lens=12)
    J(C, "w", "w2f_k8", "V1 + V2 village shrine north of the hamlet (torii V3, lanterns V4/V5)", o,
      cam=eye(945.0, 1055.0), look=at(945, 1074, 3.0), lens=22)
    J(C, "w", "w2f_k9", "Aerial of the west end (village shrine, smithies, guard house)", o, cam=[990.0, 50.0, 1050.0],
      look=[960.0, 25.0, 1076.0], lens=24)
    MAPS = {"precinct": ((1018.0, 1178.0), 76.0, [1200, 1600], "p"),
            "village": ((960.0, 1094.0), 84.0, [1500, 1700], "w"),
            "east": ((1090.0, 1097.0), 74.0, [1600, 1500], "e")}
    data["w"] = scene_data((928.0, 994.0, 1052.0, 1136.0))
    data["e"] = scene_data((1052.0, 1128.0, 1062.0, 1132.0))
    for k, (c, scale, res, dk) in MAPS.items():
        v = {"plan": True, "center": list(c), "scale": scale, "res": res, "origin": list(c), "data": data[dk],
             "trees": True, "bcut": None}
        M["w2f_map_%s_raw" % k] = ("w2f_map_%s_raw" % k, k, v)
    return {"precinct": P, "temple": T_, "civic": C, "maps": M}, MAPS


SHEET_META = {"precinct": ("W2F shrine precinct (town grade) on the SH1 hall site", 3),
              "temple": ("W2F village temple (Jodo) + town temple (Zen)", 3),
              "civic": ("W2F civic set: both street ends + the village shrine", 3)}


def compose(name, its):
    R.SHEET_META[name] = SHEET_META[name]
    R.compose(name, its)
    src = os.path.join(SHEETS, "sh1_%s.jpg" % name)
    dst = os.path.join(SHEETS, "w2f_%s.jpg" % name)
    os.replace(src, dst)
    print("->", dst)


def run_jobs(alljobs, jobs_n):
    os.makedirs(OUT, exist_ok=True)
    procs = []
    per = (len(alljobs) + jobs_n - 1) // jobs_n
    for i in range(jobs_n):
        part = alljobs[i * per:(i + 1) * per]
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


SPAWN = (1024.0, 985.0)


def draw_map(name, center, scale, area_ids):
    from PIL import Image, ImageDraw, ImageFont
    raw = os.path.join(OUT, "w2f_map_%s_raw.png" % name)
    if not os.path.isfile(raw):
        print("missing", raw)
        return
    im = Image.open(raw).convert("RGB")
    W, H = im.size
    ppm = max(W, H) / scale
    cx, cz = center

    def P(x, z):
        return (W / 2 + (x - cx) * ppm, H / 2 - (z - cz) * ppm)
    labels = [(it["id"], it["label"], it["x"], it["z"]) for it in items()
              if it["area"] in area_ids and ".s" not in it["id"] and not it["id"].endswith("t")
              and 0 < P(it["x"], it["z"])[0] < W and 0 < P(it["x"], it["z"])[1] < H]
    fs = 20
    F = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", fs)
    FS = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 17)
    im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.15)
    d = ImageDraw.Draw(im)
    boxes = []

    def free(b):
        return all(b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3] for o in boxes)
    pts = [P(x, z) for _, _, x, z in labels]
    for (px, py) in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(200, 30, 20))
        boxes.append((px - 4, py - 4, px + 4, py + 4))
    for (i, lab, x, z), (px, py) in zip(labels, pts):
        tw, th = d.textbbox((0, 0), i, font=F)[2:]
        placed = None
        for r in (8, 18, 30, 46, 64):
            for ang in (0, 180, 90, 270, 45, 135, 225, 315):
                a = math.radians(ang)
                lx = px + r * math.cos(a) + (0 if math.cos(a) >= -0.1 else -tw)
                ly = py - r * math.sin(a) - th / 2
                b = (lx - 2, ly - 2, lx + tw + 2, ly + th + 2)
                if 0 <= b[0] and b[2] < W and 0 <= b[1] and b[3] < H and free(b):
                    placed = (lx, ly, b, r)
                    break
            if placed:
                break
        if not placed:
            placed = (px + 6, py - th / 2, (px + 6, py - th / 2, px + 6 + tw, py + th / 2), 6)
        lx, ly, b, r = placed
        if r > 8:
            d.line([px, py, lx + (0 if lx > px else tw), ly + th / 2], fill=(200, 30, 20), width=2)
        d.rectangle(b, fill=(255, 255, 230))
        d.text((lx, ly), i, font=F, fill=(10, 10, 10))
        boxes.append(b)
    ax, ay = W - 60, 70
    d.polygon([(ax, ay - 40), (ax - 14, ay), (ax + 14, ay)], fill=(20, 20, 20))
    d.text((ax - 8, ay + 4), "N", font=F, fill=(20, 20, 20))
    dx, dz = SPAWN[0] - cx, SPAWN[1] - cz
    dist = math.hypot(dx, dz)
    ux, uy = dx / dist, -dz / dist
    tt = min((W / 2 - 70) / abs(ux) if abs(ux) > 1e-6 else 1e9, (H / 2 - 70) / abs(uy) if abs(uy) > 1e-6 else 1e9)
    bx, by = W / 2 + ux * tt, H / 2 + uy * tt
    d.line([bx - ux * 50, by - uy * 50, bx, by], fill=(0, 90, 200), width=5)
    t = "to the spawn (1024, 985): %d m" % round(dist)
    tw = d.textbbox((0, 0), t, font=F)[2]
    tx = min(max(8, bx - tw / 2), W - tw - 8)
    ty = by - 46 if uy > 0 else by + 18
    d.rectangle([tx - 2, ty - 2, tx + tw + 2, ty + fs + 4], fill=(255, 255, 255))
    d.text((tx, ty), t, font=F, fill=(0, 90, 200))
    sb = 10 * ppm
    d.rectangle([20, H - 40, 20 + sb, H - 32], fill=(20, 20, 20))
    d.text((20, H - 30), "10 m", font=FS, fill=(20, 20, 20))
    lh = 26
    colw = 640
    canvas = Image.new("RGB", (W + colw, max(H, 100 + len(labels) * lh)), (246, 244, 238))
    canvas.paste(im, (0, 0))
    dc = ImageDraw.Draw(canvas)
    dc.text((W + 12, 12), "W2F %s map" % name, font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28),
            fill=(20, 20, 20))
    dc.text((W + 12, 50), "ID  what (full table: spikes/SH1/SHOWCASE_MAP.md, W2F section)", font=FS, fill=(70, 70, 70))
    for k, (i, lab, x, z) in enumerate(sorted(labels)):
        y0 = 86 + k * lh
        dc.text((W + 12, y0), i, font=F, fill=(150, 20, 10))
        dc.text((W + 70, y0 + 2), lab[:68], font=FS, fill=(20, 20, 20))
    dst = os.path.join(SHEETS, "w2f_map_%s.jpg" % name)
    canvas.save(dst, quality=88)
    print("map", dst, canvas.size, "labels", len(labels))


MAP_AREAS = {"precinct": "P", "village": "VTK", "east": "UK"}


def main(argv):
    jobs_n = min(4, int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 4)
    J, MAPS = jobs()
    sets = [a for a in argv if a in J] or list(J)
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    if "--compose" not in argv:
        todo = [j for s in sets for j in J[s].values() if only is None or j[0] in only]
        run_jobs(todo, min(jobs_n, len(todo)))
    if only:
        return 0
    for s in sets:
        if s != "maps":
            compose(s, list(J[s].values()))
    if "maps" in sets:
        for k, (c, scale, res, dk) in MAPS.items():
            draw_map(k, c, scale, MAP_AREAS[k])
    return 0


if __name__ == "__main__":
    if "--blender" in sys.argv:
        spec = json.load(open(sys.argv[sys.argv.index("--blender") + 1], encoding="utf-8"))
        R.blender_main(spec)
    else:
        sys.exit(main(sys.argv[1:]))
