"""Density sketch of the 12.8 km Edo-Kyoto-Osaka map (lead, 2026-09-29).

Real lat/lon squashed into the square, so the geography is "close, not accurate". Everything is data in the tables
below: move a place by editing its (lat, lon), or add dx/dy pixel nudges. Rerun:
    python map_sketch.py        -> map_sketch.png next to this file
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 3600                       # map square, px  (12.8 km -> 3.56 m/px)
PANEL = 900                    # legend panel on the right
LON0, LON1 = 135.25, 140.0
LAT0, LAT1 = 34.45, 36.72      # bottom, top
KM = S / 12.8

def P(lat, lon):
    return ((lon - LON0) / (LON1 - LON0) * S, (LAT1 - lat) / (LAT1 - LAT0) * S)

FONT = "C:/Windows/Fonts/segoeui.ttf"
FONTB = "C:/Windows/Fonts/segoeuib.ttf"
def f(sz, b=False):
    return ImageFont.truetype(FONTB if b else FONT, sz)

# ---------------------------------------------------------------- colours
SEA = (150, 188, 214); LAND = (226, 220, 196); MOUNT = (184, 176, 150); HIGH = (160, 150, 124)
LAKE = (130, 175, 205); RIVER = (110, 160, 200)
TOKAIDO = (170, 40, 30); NAKASENDO = (40, 70, 150); SIDE = (120, 90, 50)
CITY = (70, 60, 60); CASTLE = (120, 30, 110); POST = (200, 120, 20); VIL_RICE = (90, 140, 60)
VIL_FISH = (40, 110, 160); VIL_MTN = (110, 90, 60); SALT_C = (230, 230, 230); ONSEN_C = (220, 90, 90)
LM_TOP = (200, 20, 20); LM_RES = (30, 30, 30); GAP = (0, 140, 140); CHECK = (0, 0, 0)

# ---------------------------------------------------------------- geography
SEA_POLYS = [
    # Osaka bay
    [(34.74, 135.25), (34.70, 135.30), (34.69, 135.43), (34.60, 135.44), (34.50, 135.36), (34.45, 135.33), (34.45, 135.25)],
    # Pacific with Ise, Mikawa, Suruga, Sagami and Edo bays
    [(34.45, 136.52), (34.72, 136.53), (34.96, 136.63), (35.07, 136.70), (35.09, 136.86), (35.00, 136.87), (34.85, 136.85),
     (34.70, 136.92), (34.85, 137.00), (34.82, 137.20), (34.72, 137.12), (34.60, 137.02), (34.63, 137.28), (34.67, 137.52),
     (34.66, 137.80), (34.63, 138.10), (34.60, 138.22), (34.75, 138.29), (34.87, 138.33), (35.00, 138.50), (35.10, 138.60),
     (35.13, 138.68), (35.08, 138.85), (34.95, 138.77), (34.75, 138.76), (34.60, 138.84), (34.55, 138.95), (34.70, 139.03),
     (34.97, 139.11), (35.10, 139.08), (35.24, 139.16), (35.30, 139.30), (35.31, 139.48), (35.29, 139.56), (35.20, 139.60),
     (35.14, 139.63), (35.28, 139.68), (35.45, 139.66), (35.53, 139.74), (35.63, 139.78), (35.67, 139.82), (35.64, 139.95),
     (35.60, 140.00), (34.45, 140.00)],
]
LAKES = [
    [(35.00, 135.87), (35.03, 135.93), (35.13, 136.07), (35.27, 136.23), (35.38, 136.27), (35.50, 136.20), (35.52, 136.13),
     (35.40, 136.03), (35.28, 135.99), (35.12, 135.92)],                                    # Biwa
    [(35.23, 139.00), (35.21, 139.03), (35.18, 139.02), (35.19, 138.99)],                    # Ashi
    [(36.07, 138.06), (36.06, 138.10), (36.03, 138.10), (36.04, 138.06)],                    # Suwa
    [(34.73, 137.55), (34.78, 137.60), (34.74, 137.62), (34.69, 137.58)],                    # Hamana
]
MOUNTAINS = [  # (lat, lon, rlat, rlon, colour) ellipses
    (35.95, 137.65, 0.45, 0.35, HIGH),   # Kiso / Hida / Alps
    (35.85, 138.20, 0.25, 0.20, MOUNT),  # Yatsugatake / Kirigamine
    (35.85, 138.95, 0.22, 0.30, MOUNT),  # Chichibu / Kai north
    (35.40, 138.30, 0.28, 0.18, MOUNT),  # Minami Alps / Minobu
    (35.45, 139.10, 0.12, 0.18, MOUNT),  # Tanzawa
    (35.20, 139.00, 0.09, 0.08, MOUNT),  # Hakone
    (34.85, 138.95, 0.15, 0.08, MOUNT),  # Izu
    (34.95, 136.35, 0.15, 0.07, MOUNT),  # Suzuka range
    (35.25, 135.85, 0.18, 0.08, MOUNT),  # Hira / Hiei
    (34.62, 135.95, 0.16, 0.30, MOUNT),  # Kii / Yamato hills
    (35.00, 137.60, 0.22, 0.20, MOUNT),  # Mikawa hills
    (36.10, 136.75, 0.55, 0.50, HIGH),   # Hida / Echizen / Ibuki (the empty north-west is mountains)
    (36.55, 139.05, 0.20, 0.25, MOUNT),  # Akagi / Haruna
    (36.55, 137.90, 0.20, 0.35, HIGH),   # north Alps edge
]
VOLCANOES = [("Fuji", 35.36, 138.73, 0.10), ("Asama", 36.40, 138.52, 0.06), ("Ontake", 35.89, 137.48, 0.05),
             ("Hakone", 35.23, 139.02, 0.03)]
RIVERS = [
    ("Ōi", [(34.78, 138.18), (34.95, 138.13), (35.20, 138.10)]),
    ("Tenryū", [(34.66, 137.80), (35.00, 137.85), (35.50, 137.90), (36.03, 138.07)]),
    ("Fuji R.", [(35.13, 138.66), (35.35, 138.47), (35.62, 138.47)]),
    ("Kiso", [(35.05, 136.72), (35.40, 136.88), (35.52, 137.45), (35.84, 137.69)]),
    ("Sakawa", [(35.25, 139.16), (35.38, 139.08)]),
    ("Yodo", [(34.69, 135.44), (34.90, 135.70), (35.00, 135.87)]),
    ("Tama", [(35.54, 139.75), (35.66, 139.30)]),
    ("Sumida", [(35.67, 139.80), (35.80, 139.72)]),
    ("Abe", [(34.95, 138.40), (35.20, 138.33)]),
]

# ---------------------------------------------------------------- roads (all real stations, in order)
TOKAIDO_ST = [
 ("Nihonbashi", 35.684, 139.774), ("Shinagawa", 35.62, 139.74), ("Kawasaki", 35.53, 139.70), ("Kanagawa", 35.47, 139.62),
 ("Hodogaya", 35.44, 139.60), ("Totsuka", 35.40, 139.53), ("Fujisawa", 35.34, 139.49), ("Hiratsuka", 35.33, 139.35),
 ("Ōiso", 35.31, 139.31), ("Odawara", 35.255, 139.155), ("Hakone", 35.19, 139.02), ("Mishima", 35.12, 138.92),
 ("Numazu", 35.10, 138.86), ("Hara", 35.13, 138.80), ("Yoshiwara", 35.16, 138.69), ("Kanbara", 35.12, 138.60),
 ("Yui", 35.10, 138.56), ("Okitsu", 35.05, 138.52), ("Ejiri", 35.02, 138.48), ("Fuchū", 34.975, 138.38),
 ("Mariko", 34.94, 138.33), ("Okabe", 34.92, 138.28), ("Fujieda", 34.87, 138.26), ("Shimada", 34.83, 138.18),
 ("Kanaya", 34.82, 138.13), ("Nissaka", 34.79, 138.07), ("Kakegawa", 34.77, 138.01), ("Fukuroi", 34.75, 137.92),
 ("Mitsuke", 34.72, 137.85), ("Hamamatsu", 34.71, 137.72), ("Maisaka", 34.69, 137.61), ("Arai", 34.69, 137.56),
 ("Shirasuka", 34.69, 137.49), ("Futagawa", 34.73, 137.43), ("Yoshida", 34.77, 137.39), ("Goyu", 34.84, 137.31),
 ("Akasaka", 34.85, 137.29), ("Fujikawa", 34.90, 137.22), ("Okazaki", 34.955, 137.16), ("Chiryū", 35.00, 137.05),
 ("Narumi", 35.08, 136.95), ("Miya", 35.125, 136.91), ("Kuwana", 35.065, 136.695), ("Yokkaichi", 34.965, 136.62),
 ("Ishiyakushi", 34.90, 136.55), ("Shōno", 34.88, 136.52), ("Kameyama", 34.855, 136.45), ("Seki", 34.85, 136.39),
 ("Sakanoshita", 34.88, 136.33), ("Tsuchiyama", 34.93, 136.28), ("Minakuchi", 34.97, 136.17), ("Ishibe", 35.00, 136.07),
 ("Kusatsu", 35.02, 135.96), ("Ōtsu", 35.005, 135.865), ("Sanjō Ōhashi", 35.009, 135.772),
]
KYOKAIDO = [("Sanjō Ōhashi", 35.009, 135.772), ("Fushimi", 34.93, 135.76), ("Yodo", 34.905, 135.72), ("Hirakata", 34.815, 135.65),
            ("Moriguchi", 34.735, 135.565), ("Kōraibashi", 34.69, 135.505)]
NAKASENDO_ST = [
 ("Nihonbashi", 35.684, 139.774), ("Itabashi", 35.75, 139.71), ("Warabi", 35.83, 139.68), ("Urawa", 35.86, 139.66),
 ("Ōmiya", 35.91, 139.63), ("Ageo", 35.97, 139.59), ("Okegawa", 36.00, 139.56), ("Kōnosu", 36.06, 139.52),
 ("Kumagaya", 36.15, 139.39), ("Fukaya", 36.20, 139.28), ("Honjō", 36.24, 139.19), ("Shinmachi", 36.28, 139.12),
 ("Kuragano", 36.31, 139.03), ("Takasaki", 36.32, 139.00), ("Itahana", 36.33, 138.93), ("Annaka", 36.33, 138.89),
 ("Matsuida", 36.32, 138.80), ("Sakamoto", 36.35, 138.72), ("Karuizawa", 36.35, 138.63), ("Kutsukake", 36.34, 138.58),
 ("Oiwake", 36.33, 138.55), ("Odai", 36.30, 138.47), ("Iwamurada", 36.27, 138.46), ("Shionada", 36.26, 138.40),
 ("Yawata", 36.245, 138.37), ("Mochizuki", 36.25, 138.35), ("Ashida", 36.22, 138.30), ("Nagakubo", 36.23, 138.26),
 ("Wada", 36.18, 138.20), ("Shimo-Suwa", 36.07, 138.08), ("Shiojiri", 36.11, 137.95), ("Seba", 36.07, 137.92),
 ("Motoyama", 36.04, 137.90), ("Niekawa", 35.98, 137.84), ("Narai", 35.97, 137.81), ("Yabuhara", 35.93, 137.77),
 ("Miyanokoshi", 35.88, 137.73), ("Fukushima", 35.84, 137.69), ("Agematsu", 35.78, 137.69), ("Suhara", 35.72, 137.64),
 ("Nojiri", 35.66, 137.60), ("Midono", 35.61, 137.58), ("Tsumago", 35.57, 137.59), ("Magome", 35.53, 137.56),
 ("Ochiai", 35.51, 137.53), ("Nakatsugawa", 35.49, 137.50), ("Ōi", 35.45, 137.41), ("Ōkute", 35.41, 137.30),
 ("Hosokute", 35.39, 137.25), ("Mitake", 35.43, 137.13), ("Fushimi", 35.44, 137.07), ("Ōta", 35.44, 137.02),
 ("Unuma", 35.40, 136.93), ("Kanō", 35.41, 136.77), ("Gōdo", 35.40, 136.68), ("Mieji", 35.39, 136.63),
 ("Akasaka", 35.38, 136.58), ("Tarui", 35.37, 136.53), ("Sekigahara", 35.36, 136.47), ("Imasu", 35.35, 136.41),
 ("Kashiwabara", 35.35, 136.37), ("Samegai", 35.33, 136.32), ("Banba", 35.32, 136.30), ("Toriimoto", 35.29, 136.26),
 ("Takamiya", 35.24, 136.24), ("Echigawa", 35.17, 136.20), ("Musa", 35.13, 136.10), ("Moriyama", 35.06, 136.00),
 ("Kusatsu", 35.02, 135.96),
]
KOSHU = [("Nihonbashi", 35.684, 139.774), ("Takaido", 35.68, 139.62), ("Fuchū", 35.67, 139.48), ("Hachiōji", 35.66, 139.33),
         ("Kobotoke", 35.64, 139.22), ("Sasago", 35.61, 138.80), ("Kōfu", 35.665, 138.57), ("Nirasaki", 35.70, 138.45),
         ("Shimo-Suwa", 36.07, 138.08)]
SIDE_ROADS = [
    ("Minoji", [(35.36, 136.47), (35.30, 136.60), (35.18, 136.75), (35.125, 136.91)]),
    ("Ise road", [(34.965, 136.62), (34.72, 136.51), (34.49, 136.72)]),
    ("Sayaji", [(35.125, 136.91), (35.17, 136.80), (35.065, 136.695)]),
    ("Himekaidō", [(34.69, 137.56), (34.80, 137.55), (34.77, 137.39)]),
    ("Hokkoku side road", [(36.33, 138.55), (36.66, 138.19)]),
    ("Ina road", [(36.11, 137.95), (35.83, 137.97), (35.51, 137.82), (35.20, 137.55), (34.955, 137.16)]),
]
KEY_POST = {"Shinagawa", "Kawasaki", "Totsuka", "Mishima", "Yoshiwara", "Yui", "Mariko", "Shimada", "Kanaya", "Fukuroi",
            "Arai", "Akasaka", "Chiryū", "Yokkaichi", "Seki", "Minakuchi", "Kusatsu", "Ōtsu", "Itabashi", "Kumagaya",
            "Honjō", "Karuizawa", "Oiwake", "Mochizuki", "Wada", "Shimo-Suwa", "Narai", "Tsumago", "Magome",
            "Nakatsugawa", "Tarui", "Toriimoto", "Hachiōji", "Fushimi", "Hirakata", "Moriguchi"}

# ---------------------------------------------------------------- settlements
CITIES = [("EDO", 35.69, 139.76, 200), ("KYOTO", 35.01, 135.76, 170), ("OSAKA", 34.69, 135.50, 160)]
CASTLE_TOWNS = [
 ("Odawara", 35.255, 139.155), ("Sunpu", 34.98, 138.38), ("Nagoya", 35.185, 136.90), ("Hikone", 35.276, 136.25),
 ("Kōfu", 35.665, 138.57), ("Hamamatsu", 34.71, 137.72), ("Okazaki", 34.955, 137.16), ("Kuwana", 35.065, 136.695),
 ("Takasaki", 36.32, 139.00), ("Matsumoto", 36.24, 137.97), ("Ōgaki", 35.36, 136.61), ("Yoshida", 34.77, 137.39),
 ("Kakegawa", 34.77, 138.01), ("Kameyama", 34.855, 136.45), ("Zeze", 34.99, 135.88), ("Iida", 35.51, 137.82),
 ("Takatō", 35.83, 138.06), ("Ueda", 36.40, 138.25), ("Komoro", 36.33, 138.43), ("Tanaka", 34.88, 138.24),
 ("Iga Ueno", 34.77, 136.13), ("Inuyama", 35.39, 136.94), ("Yodo", 34.905, 135.72), ("Numazu", 35.10, 138.86),
]
ONSEN = [("Hakone Yumoto", 35.23, 139.10), ("Atami", 35.10, 139.07), ("Shuzenji", 34.97, 138.93), ("Arima", 34.80, 135.25),
         ("Kusatsu-onsen", 36.62, 138.60), ("Ōjigoku", 35.245, 139.02)]
TEMPLE_TOWNS = [("Minobu", 35.38, 138.44), ("Kamiyoshida (Fuji pilgrims)", 35.48, 138.80), ("Zenkō-ji", 36.66, 138.19),
                ("Tanigumi-san", 35.52, 136.53), ("Taga", 35.22, 136.29), ("Sakamoto", 35.07, 135.87)]
PORTS = [("Shimizu", 35.02, 138.50), ("Uraga", 35.24, 139.72), ("Kanagawa port", 35.47, 139.64), ("Miya harbour", 35.11, 136.90),
         ("Sakai", 34.58, 135.47), ("Hyōgo", 34.68, 135.28), ("Katata", 35.12, 135.92), ("Ōminato (Ise)", 34.51, 136.74)]
SALT = [("Gyōtoku salt", 35.68, 139.92), ("Yoshida-hama salt", 34.78, 137.10), ("Yui-Kanbara salt beach", 35.11, 138.58)]

# ---------------------------------------------------------------- landmarks
TOP20 = [
 (1, "Hakone checkpoint", 35.19, 139.02), (2, "Seta bridge", 34.97, 135.90), (3, "Edo Castle (empty keep base)", 35.685, 139.75),
 (4, "Osaka Castle (keepless)", 34.687, 135.526), (5, "Mt Fuji + 1707 crater", 35.36, 138.73), (6, "Ōi River crossing", 34.83, 138.15),
 (7, "Kiso-Fukushima checkpoint", 35.84, 137.69), (8, "Great Buddha Hall", 34.99, 135.77), (9, "Nijō Castle (keep)", 35.014, 135.748),
 (10, "Kodenmachō jail", 35.69, 139.78), (11, "Mt Hiei / Enryaku-ji", 35.07, 135.84), (12, "Sekigahara battlefield", 35.365, 136.46),
 (13, "Nagoya Castle", 35.185, 136.90), (14, "Kunōzan Tōshōgū", 34.97, 138.47), (15, "Ōjigoku sulphur valley", 35.245, 139.02),
 (16, "Nihonbashi + fish market", 35.684, 139.774), (17, "Dōjima rice market", 34.698, 135.495), (18, "Kiso kakehashi + Nezame", 35.74, 137.66),
 (19, "Usui pass + checkpoint", 36.35, 138.68), (20, "Moto-Hakone stone Buddhas", 35.21, 139.04),
]
# pixel nudges so landmarks inside one city don't sit on top of each other
NUDGE = {3: (-70, -60), 10: (60, -80), 16: (40, 40), 8: (30, 60), 9: (-60, -40), 4: (60, 40), 17: (-60, 10),
         15: (-40, -55), 1: (-25, 30), 20: (45, 5)}
RESERVES = [
 ("Arai checkpoint", 34.69, 137.56), ("Yoshiwara quarter", 35.72, 139.79), ("Satta pass", 35.06, 138.53),
 ("Seven-Ri sea crossing", 35.09, 136.80), ("Suzuka pass", 34.88, 136.31), ("Yamanaka castle ruin", 35.14, 138.98),
 ("Kiyomizu stage", 34.995, 135.785), ("Tō-ji pagoda", 34.98, 135.747), ("Azuchi ruins", 35.155, 136.14),
 ("Chikubushima", 35.42, 136.14), ("Asama (smoking)", 36.40, 138.52), ("Hitoana cave", 35.38, 138.58),
 ("Suwa upper shrine", 35.99, 138.12), ("Yōrō falls", 35.29, 136.53), ("Kobotoke checkpoint", 35.64, 139.22),
 ("Sengaku-ji", 35.64, 139.74), ("Nishijin (burned 1730)", 35.035, 135.745), ("Kōfuku-ji, Nara (off-map)", 34.68, 135.83),
]
NUDGE_RES = {"Kiyomizu stage": (70, 20), "Tō-ji pagoda": (-40, 70), "Nishijin (burned 1730)": (-20, -70),
             "Yoshiwara quarter": (30, -50), "Sengaku-ji": (-30, 60)}
GAP_AREAS = [("Kai / Kōfu basin (gap audit #1)", 35.66, 138.55, 0.13, 0.22),
             ("Ina valley (gap #7)", 35.65, 137.90, 0.30, 0.08),
             ("Kawachi cotton fields (gap #8)", 34.62, 135.62, 0.08, 0.10)]


def main():
    img = Image.new("RGB", (S + PANEL, S), LAND)
    d = ImageDraw.Draw(img, "RGBA")
    xy = lambda pts: [P(a, b) for a, b in pts]

    # mountains
    for lat, lon, rl, ro, col in MOUNTAINS:
        cx, cy = P(lat, lon)
        rx = ro / (LON1 - LON0) * S; ry = rl / (LAT1 - LAT0) * S
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col + (150,))
    for name, lat, lon, r in VOLCANOES:
        cx, cy = P(lat, lon); rr = r / (LON1 - LON0) * S * 1.6
        d.polygon([(cx, cy - rr), (cx - rr, cy + rr * 0.8), (cx + rr, cy + rr * 0.8)], fill=(130, 110, 100, 220),
                  outline=(60, 50, 40))
        d.text((cx, cy + rr * 0.8 + 6), name, font=f(30, True), fill=(60, 45, 35), anchor="mt")
    # sea, lakes, rivers
    for poly in SEA_POLYS:
        d.polygon(xy(poly), fill=SEA)
    for poly in LAKES:
        d.polygon(xy(poly), fill=LAKE, outline=(90, 130, 170))
    for name, pts in RIVERS:
        d.line(xy(pts), fill=RIVER, width=10, joint="curve")
    # 1 km grid
    for i in range(1, 13):
        v = i * KM
        d.line([(v, 0), (v, S)], fill=(0, 0, 0, 28), width=2)
        d.line([(0, v), (S, v)], fill=(0, 0, 0, 28), width=2)
    # gap areas
    for name, lat, lon, rl, ro in GAP_AREAS:
        cx, cy = P(lat, lon); rx = ro / (LON1 - LON0) * S; ry = rl / (LAT1 - LAT0) * S
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=GAP + (255,), width=6)
        d.text((cx, cy - ry - 8), name, font=f(28, True), fill=GAP, anchor="mb")

    # roads + station ticks
    def road(sts, col, w):
        d.line([P(a, b) for _, a, b in sts], fill=col, width=w, joint="curve")
    road(TOKAIDO_ST, TOKAIDO, 12); road(KYOKAIDO, TOKAIDO, 9); road(NAKASENDO_ST, NAKASENDO, 12); road(KOSHU, SIDE, 8)
    for name, pts in SIDE_ROADS:
        d.line(xy(pts), fill=SIDE + (200,), width=6, joint="curve")
    for sts in (TOKAIDO_ST, KYOKAIDO, NAKASENDO_ST, KOSHU):
        for name, a, b in sts[1:-1]:
            x, y = P(a, b)
            if name in KEY_POST:
                d.rectangle([x - 11, y - 11, x + 11, y + 11], fill=POST, outline=(90, 50, 0), width=2)
                d.text((x + 16, y - 16), name, font=f(24), fill=(90, 50, 0))
            else:
                d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(90, 50, 0))

    # villages: procedural, by zone (coast -> fishing, mountains -> mountain village, else rice)
    rnd = random.Random(1730)
    sea_mask = Image.new("L", (S, S), 0); md = ImageDraw.Draw(sea_mask)
    for poly in SEA_POLYS + LAKES:
        md.polygon(xy(poly), fill=255)
    mtn_mask = Image.new("L", (S, S), 0); mm = ImageDraw.Draw(mtn_mask)
    for lat, lon, rl, ro, col in MOUNTAINS:
        cx, cy = P(lat, lon); rx = ro / (LON1 - LON0) * S; ry = rl / (LAT1 - LAT0) * S
        mm.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    taken = [P(a, b) for _, a, b in TOKAIDO_ST + NAKASENDO_ST + KOSHU + KYOKAIDO] + \
            [P(a, b) for _, a, b in CASTLE_TOWNS] + [P(a, b) for _, a, b, _ in CITIES]
    vills = []
    road_pts = []
    for sts in (TOKAIDO_ST, NAKASENDO_ST, KOSHU, KYOKAIDO):
        pts = [P(a, b) for _, a, b in sts]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            for t in range(0, 10):
                road_pts.append((x1 + (x2 - x1) * t / 10, y1 + (y2 - y1) * t / 10))
    def clear(x, y, gap):
        return min(math.hypot(x - a, y - b) for a, b in taken + [v[:2] for v in vills]) >= gap
    def on_land(x, y):
        return 0 <= x < S and 0 <= y < S and not sea_mask.getpixel((int(x), int(y)))
    # 1) fishing villages: on the shore, not on lakes' far side of the map edge
    tries = 0
    while sum(1 for v in vills if v[2] == "fish") < 16 and tries < 40000:
        tries += 1
        x, y = rnd.uniform(60, S - 60), rnd.uniform(60, S - 60)
        if not on_land(x, y) or not clear(x, y, 200):
            continue
        if any(0 <= x + dx < S and 0 <= y + dy < S and sea_mask.getpixel((int(x + dx), int(y + dy)))
               for dx, dy in ((70, 0), (-70, 0), (0, 70), (0, -70))):
            vills.append((x, y, "fish"))
    # 2) farm and mountain villages: within about 1.7 km of a road (people live along the routes)
    tries = 0
    while len(vills) < 60 and tries < 40000:
        tries += 1
        x, y = rnd.uniform(60, S - 60), rnd.uniform(60, S - 60)
        if not on_land(x, y) or not clear(x, y, 190):
            continue
        if min(math.hypot(x - a, y - b) for a, b in road_pts[::3]) > 1.7 * KM:
            continue
        vills.append((x, y, "mtn" if mtn_mask.getpixel((int(x), int(y))) else "rice"))
    counts = {"fish": 0, "mtn": 0, "rice": 0}
    for x, y, kind in vills:
        counts[kind] += 1
        col = {"fish": VIL_FISH, "mtn": VIL_MTN, "rice": VIL_RICE}[kind]
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col, outline=(30, 30, 30), width=2)

    # settlements
    for name, lat, lon, r in CITIES:
        x, y = P(lat, lon)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(90, 80, 80, 120), outline=CITY, width=6)
        d.text((x, y - r - 12), name, font=f(56, True), fill=CITY, anchor="mb")
    for name, lat, lon in CASTLE_TOWNS:
        x, y = P(lat, lon)
        d.rectangle([x - 22, y - 22, x + 22, y + 22], fill=CASTLE, outline=(40, 0, 40), width=3)
        d.text((x, y + 26), name, font=f(28, True), fill=CASTLE, anchor="mt")
    for group, col, shape in ((ONSEN, ONSEN_C, "d"), (TEMPLE_TOWNS, (150, 100, 0), "d"), (PORTS, VIL_FISH, "a"),
                              (SALT, (120, 120, 120), "s")):
        for name, lat, lon in group:
            x, y = P(lat, lon)
            if shape == "d":
                d.polygon([(x, y - 18), (x + 18, y), (x, y + 18), (x - 18, y)], fill=col, outline=(30, 30, 30))
            elif shape == "a":
                d.line([(x, y - 18), (x, y + 16)], fill=col, width=6); d.arc([x - 16, y - 4, x + 16, y + 20], 0, 180, fill=col, width=6)
            else:
                d.rectangle([x - 14, y - 10, x + 14, y + 10], fill=SALT_C, outline=(90, 90, 90), width=3)
            d.text((x + 22, y), name, font=f(24), fill=(40, 40, 40), anchor="lm")

    # landmarks
    for name, lat, lon in RESERVES:
        x, y = P(lat, lon); dx, dy = NUDGE_RES.get(name, (0, 0)); x += dx; y += dy
        d.regular_polygon((x, y, 14), 3, fill=(255, 255, 255), outline=LM_RES)
        d.text((x + 18, y), name, font=f(22), fill=LM_RES, anchor="lm")
    for n, name, lat, lon in TOP20:
        x, y = P(lat, lon); dx, dy = NUDGE.get(n, (0, 0)); x += dx; y += dy
        pts = []
        for k in range(10):
            r = 30 if k % 2 == 0 else 13
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((x + r * math.cos(a), y + r * math.sin(a)))
        d.polygon(pts, fill=LM_TOP, outline=(80, 0, 0))
        d.text((x, y + 2), str(n), font=f(20, True), fill=(255, 255, 255), anchor="mm")

    # scale bar
    d.rectangle([80, S - 110, 80 + 2 * KM, S - 90], fill=(0, 0, 0))
    d.rectangle([80 + KM, S - 108, 80 + 2 * KM - 2, S - 92], fill=(255, 255, 255))
    d.text((80, S - 120), "0          1 km          2 km   (grid = 1 km, map = 12.8 km)", font=f(28), fill=(0, 0, 0), anchor="lb")
    d.text((S - 60, 60), "N ↑", font=f(60, True), fill=(0, 0, 0), anchor="rt")

    # ---------------------------------------------------------------- legend panel
    x0 = S + 40; y = 50
    d.rectangle([S, 0, S + PANEL, S], fill=(248, 246, 240))
    d.text((x0, y), "Edo – Kyoto – Osaka, 12.8 km", font=f(46, True), fill=(0, 0, 0)); y += 64
    d.text((x0, y), "Density sketch v0, 2026-09-29. Real places,", font=f(28), fill=(60, 60, 60)); y += 36
    d.text((x0, y), "squashed; close, not accurate.", font=f(28), fill=(60, 60, 60)); y += 60

    def row(draw_fn, label, n=None):
        nonlocal y
        draw_fn(x0 + 25, y + 18)
        d.text((x0 + 70, y + 18), label + ("  (%d)" % n if n is not None else ""), font=f(30), fill=(20, 20, 20), anchor="lm")
        y += 50
    row(lambda x, yy: d.ellipse([x - 22, yy - 22, x + 22, yy + 22], fill=(90, 80, 80, 120), outline=CITY, width=4), "City", len(CITIES))
    row(lambda x, yy: d.rectangle([x - 16, yy - 16, x + 16, yy + 16], fill=CASTLE), "Castle town", len(CASTLE_TOWNS))
    npost = sum(1 for s in TOKAIDO_ST + NAKASENDO_ST + KOSHU + KYOKAIDO if s[0] in KEY_POST)
    row(lambda x, yy: d.rectangle([x - 11, yy - 11, x + 11, yy + 11], fill=POST), "Post town, named", npost)
    nst = len(TOKAIDO_ST) + len(NAKASENDO_ST) + len(KOSHU) + len(KYOKAIDO) - 8
    row(lambda x, yy: d.ellipse([x - 5, yy - 5, x + 5, yy + 5], fill=(90, 50, 0)), "Other real station (dot)", nst - npost)
    row(lambda x, yy: d.ellipse([x - 13, yy - 13, x + 13, yy + 13], fill=VIL_RICE), "Rice village", counts["rice"])
    row(lambda x, yy: d.ellipse([x - 13, yy - 13, x + 13, yy + 13], fill=VIL_MTN), "Mountain village", counts["mtn"])
    row(lambda x, yy: d.ellipse([x - 13, yy - 13, x + 13, yy + 13], fill=VIL_FISH), "Fishing village", counts["fish"])
    row(lambda x, yy: d.polygon([(x, yy - 16), (x + 16, yy), (x, yy + 16), (x - 16, yy)], fill=ONSEN_C), "Hot-spring town", len(ONSEN))
    row(lambda x, yy: d.polygon([(x, yy - 16), (x + 16, yy), (x, yy + 16), (x - 16, yy)], fill=(150, 100, 0)), "Temple / pilgrim town", len(TEMPLE_TOWNS))
    row(lambda x, yy: (d.line([(x, yy - 16), (x, yy + 14)], fill=VIL_FISH, width=5)), "Port", len(PORTS))
    row(lambda x, yy: d.rectangle([x - 14, yy - 10, x + 14, yy + 10], fill=SALT_C, outline=(90, 90, 90), width=3), "Salt village", len(SALT))
    row(lambda x, yy: d.regular_polygon((x, yy, 22), 5, fill=LM_TOP), "Top-20 landmark (numbered)", 20)
    row(lambda x, yy: d.regular_polygon((x, yy, 14), 3, fill=(255, 255, 255), outline=LM_RES), "Reserve landmark", len(RESERVES))
    row(lambda x, yy: d.ellipse([x - 22, yy - 14, x + 22, yy + 14], outline=GAP, width=5), "Gap-audit area (nearly blank)", len(GAP_AREAS))
    y += 10
    for col, label in ((TOKAIDO, "Tōkaidō (coast road)"), (NAKASENDO, "Nakasendō (mountain road)"), (SIDE, "Kōshū road + side roads")):
        d.line([(x0, y + 18), (x0 + 50, y + 18)], fill=col, width=10)
        d.text((x0 + 70, y + 18), label, font=f(30), fill=(20, 20, 20), anchor="lm"); y += 48
    y += 20
    nset = len(CITIES) + len(CASTLE_TOWNS) + npost + len(vills) + len(ONSEN) + len(TEMPLE_TOWNS) + len(PORTS) + len(SALT)
    d.text((x0, y), "Settlements drawn: %d" % nset, font=f(34, True), fill=(0, 0, 0)); y += 46
    for line in ["Chernarus (15.4 km): 2 capitals, 16 cities,",
                 "59 villages = 77. Same density on 12.8 km",
                 "would be about 53 settlements.",
                 "",
                 "Villages are random placeholders (60):",
                 "16 on the shore, the rest near roads. Top-20 numbers match",
                 "research/landmarks/LANDMARKS_RANKED.md.",
                 "",
                 "Top 20:"]:
        d.text((x0, y), line, font=f(28), fill=(40, 40, 40)); y += 36
    for n, name, _, _ in TOP20:
        d.text((x0 + 10, y), "%2d  %s" % (n, name), font=f(26), fill=(120, 0, 0)); y += 33

    out = os.path.join(HERE, "map_sketch.png")
    img.save(out, optimize=True)
    print("wrote", out, "settlements", nset, "villages", counts, "y_end", y)


if __name__ == "__main__":
    main()
