"""SH1 graveyard: an old village graveyard west of the shrine approach (W2_ERA 'What this means for the build').

Seven rows (row 1 = the front, south) in two blocks either side of a north-south aisle, the 0.9-1.15 m plot grid
jittered (+-0.15 m, +-12 deg; abandoned stones more), gaps where a plot was never stoned. Stones face south. The back
rows are the old section (gorinto, hokyointo, mossy boards, square pillars), the front rows the newer stones
(round-headed, boat-halo) and the poor graves (field stones, earth mounds, wooden posts). Slats stand behind about one
stone in three, flower tubes before about one in four, incense stands before some. The water point (basin, bucket
rack, slat rack) and a row of six Jizo stand at the east gate onto the approach. Leaf litter in the aisles under an
old oak.

IDs: G<row>-<col> (col 1-16 from the west; 1-8 west block, 9-16 east block); accessories add a suffix
(s = slats, t = flower tubes, i = incense); GW = water point, GJ = the six Jizo, GL = leaf litter, GF = fallen slats,
GT = the tree.
"""
import random

import terrain_sh1 as T  # noqa: F401  (seating is done by layout_sh1)

Z0, PITCH_Z = 1110.0, 2.6
XW, XE, PITCH_X = 991.0, 1001.4, 1.15
_ = None
B, BS, BT, BH, BHC, R, RS, PL, PP = ("board", "board_s", "board_tall_moss", "boat_halo", "boat_halo_child", "round",
                                     "round_s_plain", "pillar", "pillar_pointed")
GS, GL, GST, GH, HK, JC, F, FM, FP = ("gorinto_s", "gorinto_l", "gorinto_stack", "gorinto_heap", "hokyointo",
                                      "jizo_child", "field", "field_mound", "field_pair")
AL, ABB, ABS, ARL, AGF, AHB = ("ab_leaning", "ab_board_broken", "ab_boat_halo_sunk", "ab_round_lean",
                               "ab_gorinto_fallen", "ab_hokyointo_broken")
WB, WBN, WBS, WBR, WAL, WAS, WAR = ("w:bohyo", "w:bohyo_new", "w:bohyo_s", "w:bohyo_roof", "w:ab_bohyo_lean",
                                    "w:ab_bohyo_split", "w:ab_bohyo_rotted")
# rows south (front, newest) to north (back, oldest); 8 west-block plots then 8 east-block plots, west to east
ROWS = [
    [WBN, WB, _, FM, WBS, RS, WAR, R, R, BHC, _, R, WBR, BH, RS, _],
    [F, FP, WBS, WAL, _, BH, FM, B, BH, R, ARL, BS, WB, _, BH, JC],
    [F, _, B, BH, BS, WB, FP, WAS, JC, BHC, JC, BHC, _, B, RS, BH],
    [B, BH, AL, B, _, F, BH, BS, B, BH, BH, _, JC, BS, ABS, FM],
    [BT, BH, B, PP, _, B, WAR, BH, B, ABB, BH, F, B, _, BH, BS],
    [BH, B, GS, _, BT, PL, BH, FP, BT, BH, AL, B, _, GST, ABS, WBS],
    [GH, _, GS, BT, AGF, PL, HK, _, B, GL, "+", AHB, BH, F, _, B],
]
LABEL = {
    B: "board-shaped stone (itabi), with a carved posthumous name", BS: "small board stone",
    BT: "tall board stone, mossy", BH: "boat-halo figure stone (funagata)", BHC: "small boat-halo stone (a child's)",
    R: "round-headed slab (kushigata, newer)", RS: "small round-headed slab, plain", PL: "square pillar, flat top with a water hollow (rare)",
    PP: "square pillar, pointed Kyoho top (rare)", GS: "gorinto 0.6 m (five rings, Sanskrit seed syllables)",
    GL: "gorinto 2.0 m on its platform (a samurai or priest's grave)", GST: "gorinto re-stacked from mismatched rings",
    GH: "a small heap of old gorinto fragments", HK: "hokyointo 1.5 m (four seed syllables on the body)",
    JC: "child's Jizo with a bib", F: "plain field stone (a poor grave)", FM: "earth mound with a field stone",
    FP: "two field stones", AL: "board stone leaning (abandoned)", ABB: "board stone, top broken off (abandoned)",
    ABS: "boat-halo stone sunk and tilted (abandoned)", ARL: "round-headed slab leaning (abandoned)",
    AGF: "gorinto with its top rings fallen (abandoned)", AHB: "hokyointo, finial fallen (abandoned)",
    WB: "wooden grave post (bohyo) on an earth mound, silver-grey", WBN: "new wooden grave post, fresh ink, high mound",
    WBS: "short wooden grave post", WBR: "wooden grave post with a little gabled roof (uncommon)",
    WAL: "grave post leaning (abandoned)", WAS: "grave post split and rotting black (abandoned)",
    WAR: "grave post rotted to a stump, the mound sunk (abandoned)"}
MOUND = {FM, WB, WBN, WBS, WBR, WAL, WAS, WAR}
STONE_FRONT = {B, BS, BT, BH, R, RS, PL, PP, GS, HK, BHC}


def model(t):
    return "jp_s_grave_wood_" + t[2:] if t.startswith("w:") else "jp_s_grave_stones_" + t


def layout():
    rnd = random.Random(1730)
    O = []

    def add(i, name, x, z, yaw, label, y=None, **extra):
        O.append((i, name, x, z, yaw, y, label, extra))
    n_s = n_t = n_i = 0
    for r, row in enumerate(ROWS):
        zr = Z0 + PITCH_Z * r + rnd.uniform(-0.12, 0.12)
        for c, t in enumerate(row):
            if t is None or t == "+":
                continue
            x0 = XW if c < 8 else XE
            x = x0 + PITCH_X * (c % 8) + rnd.uniform(-0.15, 0.15)
            if t == GL:
                x += PITCH_X / 2.0                # the large gorinto's platform takes two plots
            z = zr + rnd.uniform(-0.10, 0.10)
            ab = t.startswith("ab_") or t.startswith("w:ab_")
            yaw = 180.0 + rnd.uniform(-12, 12) * (2.0 if ab else 1.0)
            gid = "G%d-%02d" % (r + 1, c + 1)
            if t in MOUND:
                z -= 0.65                         # the mound lies in front; its post / stone stands on the row line
            add(gid, model(t), x, z, yaw, LABEL[t])
            if t in STONE_FRONT and t not in (GS, HK):
                if rnd.random() < 0.36:
                    add(gid + "s", "jp_s_grave_wood_sotoba_x3", x + rnd.uniform(-0.08, 0.08), z + 0.30, 180.0 + rnd.uniform(-8, 8),
                        "  memorial slats (sotoba) behind " + gid, grp="acc")
                    n_s += 1
                if rnd.random() < 0.28:
                    hd = 0.33 if t in (PL, PP) else 0.20       # half depth of the stone + a gap
                    add(gid + "t", "jp_s_grave_wood_tubes", x, z - hd - 0.13, 180.0, "  bamboo flower tubes before " + gid, grp="acc")
                    n_t += 1
                    if rnd.random() < 0.5:
                        add(gid + "i", "jp_s_grave_wood_incense", x + 0.02, z - hd - 0.42, 180.0, "  stone incense stand before " + gid, grp="acc")
                        n_i += 1
    # every accessory at least once even if the dice said no
    # the east gate onto the approach: water point and the six Jizo
    add("GW1", "jp_s_chozubachi_small", 1012.0, 1112.0, 90, "graveyard water point: small stone basin")
    add("GW2", "jp_s_grave_wood_bucket_rack", 1012.2, 1109.9, 90, "bucket-and-ladle rack by the water")
    add("GW3", "jp_s_grave_wood_rack", 1011.9, 1114.4, 90, "rack of spare memorial slats")
    for k, j in enumerate(["jp_s_stone_jizo_m", "jp_s_stone_jizo_bib", "jp_s_stone_jizo_m", "jp_s_stone_jizo_halo",
                           "jp_s_stone_jizo_bib", "jp_s_stone_jizo_m"]):
        add("GJ%d" % (k + 1), j, 1012.0, 1117.0 + 0.72 * k, 90, "the six Jizo at the gate (roku-jizo), %d of 6" % (k + 1))
    add("GJ7", "jp_s_stone_jizo_ab_tipped", 1013.2, 1121.9, 30, "a seventh Jizo knocked over (abandoned)")
    # fallen slats and leaf litter in the aisles
    for k, (x, z, yw) in enumerate([(996.4, 1113.9, 30), (1005.8, 1119.0, 200), (993.0, 1124.2, 110)]):
        add("GF%d" % (k + 1), "jp_s_grave_wood_ab_fallen", x, z, yw, "slats blown down into the aisle")
    for k, (n, x, z, yw) in enumerate([("jp_s_leaf_pile_ab_scattered", 1000.2, 1121.0, 0),
                                        ("jp_s_leaf_pile_ab_scattered", 994.8, 1126.7, 70),
                                        ("jp_s_leaf_pile_small", 1000.3, 1114.6, 20),
                                        ("jp_s_leaf_pile_small", 1006.6, 1124.1, 150),
                                        ("jp_s_leaf_pile_ab_scattered", 1004.8, 1129.2, 210),
                                        ("jp_s_leaf_pile_small", 990.0, 1118.6, 300)]):
        add("GL%d" % (k + 1), n, x, z, yw, "autumn leaf litter")
    add("GT1", "t_quercusrobur_2f", 987.3, 1129.6, 40, "an old oak over the back of the graveyard (vanilla tree, placement only)", y=-0.06)
    return O, {"slats": n_s, "tubes": n_t, "incense": n_i}
