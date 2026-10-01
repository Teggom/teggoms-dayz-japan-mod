"""M1: one-off patch of spikes/B3b/props_grave.py (grave names, bare-earth mounds, new / silver wood posts)."""
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B3b", "props_grave.py")
s = open(P, "rb").read().decode()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''                  leaves, litter, moss_top, moss_face, CARVED, CUT, FIELD, RIVER, BAMBOO, WOOD, MOSS, LEAF, CTEXT, SUMI)''',
    '''                  leaves, litter, moss_top, moss_face, CARVED, CUT, FIELD, RIVER, BAMBOO, WOOD, MOSS, LEAF, CTEXT, SUMI,
                  GTEXT, GSUMI, EARTH, NEWWOOD, SILVER)''')
rep('''WOMAN = "grave_shakuni_myoshin"       # Hoei 2 (1705), a woman (Shin sect)
''', '''WOMAN = "grave_shakuni_myoshin"       # Hoei 2 (1705), a woman (Shin sect)
# M1 (2026-09-30): the grave-names atlas jp_m_decal_carved_text_grave (13 cells, 14 kaimyo, 1670-1729; forms and dates
# in spikes/M1/M1_PROGRESS.md "Text"). Its three-column cells keep the columns at fixed fractions:
GNAME = (0.26, 0.0, 0.74, 1.0)        # the kaimyo column
GDATE_R = (0.70, 0.0, 1.0, 1.0)       # the era-year column
# kind -> (atlas material, cell, crop): every inscribed stone its own person; older forms on older stone types
KAIMYO = {
    "board": (GTEXT, "kaimyo_joshin_shinji_genroku8", None),
    "board_s": (GTEXT, "kaimyo_myotei_shinnyo_hoei4", GNAME),
    "board_tall_moss": (GTEXT, "kaimyo_myoju_zenjoni_kanbun10", None),
    "ab_leaning": (GTEXT, "kaimyo_soen_zenjomon_enpo6", None),
    "ab_board_broken": (CTEXT, WOMAN, (0.0, 0.42, 1.0, 1.0)),
    "boat_halo": (GTEXT, "kaimyo_kigen_dokaku_shinji_genroku11", GNAME),
    "boat_halo_child": (GTEXT, "kaimyo_shunko_doji_kyoho5", GNAME),
    "ab_boat_halo_sunk": (GTEXT, "kaimyo_enjaku_myosho_shinnyo_kyoho12", GNAME),
    "round": (GTEXT, "kaimyo_ryozen_shinji_kyoho14", None),
    "ab_round_lean": (GTEXT, "kaimyo_shaku_ryonen_kyoho8", None),
    "pillar": (GTEXT, "kaimyo_hozan_zenjomon_shotoku1", None),
    "pillar_pointed": (GTEXT, "kaimyo_chisei_shinnyo_kyoho10", None),
}
''')
rep('''        w, h, t, bases, cell, crop = {
            "board": (0.30, 0.62, 0.14, [(0.48, 0.32, 0.13)], MEN, None),
            "board_s": (0.24, 0.48, 0.12, [], WOMAN, NAME),
            "board_tall_moss": (0.32, 0.80, 0.15, [(0.56, 0.36, 0.12), (0.44, 0.28, 0.10)], WOMAN, None),
            "ab_leaning": (0.30, 0.64, 0.14, [(0.48, 0.32, 0.13)], MEN, None),
            "ab_board_broken": (0.30, 0.66, 0.14, [(0.48, 0.32, 0.13)], WOMAN, (0.0, 0.42, 1.0, 1.0)),
        }[kind]''', '''        w, h, t, bases = {
            "board": (0.30, 0.62, 0.14, [(0.48, 0.32, 0.13)]),
            "board_s": (0.24, 0.48, 0.12, []),
            "board_tall_moss": (0.32, 0.80, 0.15, [(0.56, 0.36, 0.12), (0.44, 0.28, 0.10)]),
            "ab_leaning": (0.30, 0.64, 0.14, [(0.48, 0.32, 0.13)]),
            "ab_board_broken": (0.30, 0.66, 0.14, [(0.48, 0.32, 0.13)]),
        }[kind]
        tmat, cell, crop = KAIMYO[kind]''')
rep('''        tx.append(K.carved((0.0, tc, t / 2), X, Y, th, cell, wear=wear, crop=crop))
        top = y0 + hh''', '''        tx.append(K.carved((0.0, tc, t / 2), X, Y, th, cell, wear=wear, crop=crop, mat=tmat))
        top = y0 + hh''')
rep('''        if kind != "boat_halo_child":
            tx.append(K.carved((w * 0.30, y0 + h * 0.45, t / 2), X, Y, h * 0.44, MEN if kind == "boat_halo" else WOMAN,
                               wear=wear, crop=NAME))''', '''        tmat, cell, crop = KAIMYO[kind]
        if kind != "boat_halo_child":
            tx.append(K.carved((w * 0.30, y0 + h * 0.45, t / 2), X, Y, h * 0.44, cell, wear=wear, crop=crop, mat=tmat))
        else:   # M1: later boat-halo stones are mostly children's graves: the child's name beside the Jizo
            tx.append(K.carved((w * 0.31, y0 + h * 0.42, t / 2), X, Y, h * 0.40, cell, wear=wear, crop=crop, mat=tmat))''')
rep('''        w, h, t, bases, cell = {
            "round": (0.30, 0.70, 0.20, [(0.46, 0.36, 0.14)], MEN),
            "round_s_plain": (0.26, 0.50, 0.16, [], None),
            "ab_round_lean": (0.30, 0.72, 0.19, [(0.46, 0.36, 0.14)], WOMAN),
        }[kind]''', '''        w, h, t, bases = {
            "round": (0.30, 0.70, 0.20, [(0.46, 0.36, 0.14)]),
            "round_s_plain": (0.26, 0.50, 0.16, []),
            "ab_round_lean": (0.30, 0.72, 0.19, [(0.46, 0.36, 0.14)]),
        }[kind]
        tmat, cell, _ = KAIMYO.get(kind, (None, None, None))''')
rep('''            tx.append(K.carved((0.0, y0 + (h - w / 2) * 0.55, t / 2), X, Y, min(0.42, h - w / 2 - 0.06), cell, wear=wear))''',
    '''            tx.append(K.carved((0.0, y0 + (h - w / 2) * 0.55, t / 2), X, Y, min(0.42, h - w / 2 - 0.06), cell, wear=wear,
                               mat=tmat))''')
rep('''        tx.append(K.carved((0.0, y0 + h * 0.52, a / 2), X, Y, h * 0.80, MEN, wear=wear, crop=NAME))
        tx.append(K.carved((a / 2, y0 + h * 0.55, 0.0), (0.0, 0.0, -1.0), Y, h * 0.62, MEN, wear=wear, crop=DATE_R))''',
    '''        tmat, cell, _ = KAIMYO[kind]
        tx.append(K.carved((0.0, y0 + h * 0.52, a / 2), X, Y, h * 0.80, cell, wear=wear, crop=GNAME, mat=tmat))
        tx.append(K.carved((a / 2, y0 + h * 0.55, 0.0), (0.0, 0.0, -1.0), Y, h * 0.62, cell, wear=wear, crop=GDATE_R,
                           mat=tmat))''')
rep('''            m = lathe([(0.0, -0.03), (0.58, -0.03), (0.45, 0.06), (0.22, 0.12), (0.0, 0.13)], 8, LEAF, vis=(1, 2),
                      smooth=True)''', '''            m = lathe([(0.0, -0.03), (0.58, -0.03), (0.45, 0.06), (0.22, 0.12), (0.0, 0.13)], 8, EARTH, vis=(1, 2),
                      smooth=True)''')
rep('''            P.notes.append("the mound is turned earth under leaves; no collision on it (walk over)")''',
    '''            lt = xf(litter(45, 0.0, 0.05, 0.30, sx=0.9, sz=1.3), t=(0.0, 0.12, 0.0))
            vis.append(lt)
            P.notes.append("the mound is bare earth (M1: jp_m_ground_earth_bare) with a little litter; no collision on "
                           "it (walk over)")''')
rep('''    """W3: the earth mound under a grave post (leaf-litter material, as W2). sunk: the coffin has collapsed, so the
    rim stands higher than the middle. Returns visual solids (mound + a litter patch on its top)."""''',
    '''    """W3: the earth mound under a grave post (M1: bare earth, jp_m_ground_earth_bare; _w0 = fresh moist clods). sunk:
    the coffin has collapsed, so the rim stands higher than the middle. Returns visual solids (mound + a litter patch
    on its top)."""''')
rep('''    m = lathe(prof, 8, LEAF, vis=(1, 2))
    m.verts = [(v[0], v[1], v[2] * sz) for v in m.verts]''', '''    m = lathe(prof, 8, EARTH, vis=(1, 2))
    m.verts = [(v[0], v[1], v[2] * sz) for v in m.verts]''')
rep('''def bohyo_post(a, h, z0, mat=WOOD, wear="_w1", tip=0.06, text=True, th=None, crop=None, ink="_w2", cap=False):''',
    '''def bohyo_post(a, h, z0, mat=WOOD, wear="_w1", tip=0.06, text=True, th=None, crop=None, ink="_w2", cap=False,
               cell=None):''')
rep('''    if text:
        th = th or min(0.40, (y1 - 0.12) * 0.62)
        yc = y1 - 0.06 - th / 2
        out.append(K.inked((0.0, yc, z0 + a / 2), X, Y, th, "sotoba_namuamida", wear=ink, width=a * 0.78, crop=crop))''',
    '''    if text and cell:
        # M1: a posthumous name in ink (jp_m_decal_sumi_text_grave): the kaimyo column on the front, the era year on
        # the right-hand side face (as on the square-pillar stones), each at the cell's own aspect (no squeezing)
        cw, ch = skit.cell_size(GSUMI, cell)
        nw = cw * (GNAME[2] - GNAME[0])
        th = th or min(0.42, (y1 - 0.12) * 0.70, a * 0.85 * ch / nw)
        yc = y1 - 0.05 - th / 2
        out.append(K.inked((0.0, yc, z0 + a / 2), X, Y, th, cell, wear=ink, crop=GNAME, mat=GSUMI))
        dw = cw * (GDATE_R[2] - GDATE_R[0])
        dh = min(th, a * 0.85 * ch / dw)
        out.append(K.inked((a / 2, y1 - 0.05 - dh / 2, z0), (0.0, 0.0, -1.0), Y, dh, cell, wear=ink, crop=GDATE_R,
                           mat=GSUMI))
    elif text:
        th = th or min(0.40, (y1 - 0.12) * 0.62)
        yc = y1 - 0.06 - th / 2
        out.append(K.inked((0.0, yc, z0 + a / 2), X, Y, th, "sotoba_namuamida", wear=ink, width=a * 0.78, crop=crop))''')
rep('''        m = lathe([(0.0, -0.03), (0.50, -0.03), (0.40, 0.05), (0.20, 0.10), (0.0, 0.11)], 8, LEAF, vis=(1, 2))
        m.verts = [(v[0], v[1], v[2] * 1.4) for v in m.verts]''', '''        m = lathe([(0.0, -0.03), (0.50, -0.03), (0.40, 0.05), (0.20, 0.10), (0.0, 0.11)], 8, EARTH, vis=(1, 2))
        m.verts = [(v[0], v[1], v[2] * 1.4) for v in m.verts]''')
rep('''        post = [W(-a / 2, a / 2, -0.20, 0.80, z0 - a / 2, z0 + a / 2, WOOD, vis=(1, 2)),
                core.Solid([(-a / 2, 0.80, z0 - a / 2), (a / 2, 0.80, z0 - a / 2), (a / 2, 0.80, z0 + a / 2),
                            (-a / 2, 0.80, z0 + a / 2), (0.0, 0.86, z0)], [[0, 1, 2, 3], [0, 1, 4], [1, 2, 4], [2, 3, 4],
                                                                          [3, 0, 4]], WOOD, vis=(1,))]
        post.append(K.inked((0.0, 0.48, z0 + a / 2), X, Y, 0.40, "sotoba_namuamida", wear="_w2", width=0.07))
        pc = col(-a / 2, a / 2, 0.0, 0.80, z0 - a / 2, z0 + a / 2, WOOD)''',
    '''        # M1: a silver-grey post (a few years old) with a faded posthumous name and its year
        post, pc = bohyo_post(a, 0.86, z0, SILVER, "_w1", 0.06, ink="_w2", cell="bohyo_chiko_shinnyo_kyoho12")''')
rep('''        spec = {  # a, h, z0, wood, wear, tip, text crop (None = whole), tilt rx / rz, sink, mound (r, h, sz, sunk)
            "bohyo_new": (0.105, 1.15, -0.70, WOOD, "_w0", 0.07, None, -1.0, 0.5, 0.0, (0.55, 0.17, 1.4, False)),
            "bohyo_s": (0.06, 0.52, -0.40, WOOD, "_w2", 0.04, (0.0, 0.0, 1.0, 0.5), -3.0, -5.0, 0.0,
                        (0.32, 0.08, 1.35, False)),
            "bohyo_roof": (0.10, 1.00, -0.62, WOOD, "_w1", 0.0, None, -2.0, 2.0, 0.0, (0.50, 0.11, 1.4, False)),
            "ab_bohyo_lean": (0.09, 0.85, -0.60, WOOD, "_w2", 0.06, (0.0, 0.5, 1.0, 1.0), 9.0, -17.0, 0.05,
                              (0.48, 0.07, 1.4, False)),
        }''', '''        # M1: the new post in pale NEW wood with crisp ink, older ones silver-grey (jp_m_wood_silver) with fading ink;
        # each carries a posthumous name (jp_m_decal_sumi_text_grave): name on the front, year on the side
        spec = {  # a, h, z0, wood, wear, tip, text crop (None = whole), tilt rx / rz, sink, mound (r, h, sz, sunk)
            "bohyo_new": (0.105, 1.15, -0.70, NEWWOOD, "_w0", 0.07, None, -1.0, 0.5, 0.0, (0.55, 0.17, 1.4, False)),
            "bohyo_s": (0.06, 0.52, -0.40, SILVER, "_w1", 0.04, None, -3.0, -5.0, 0.0,
                        (0.32, 0.08, 1.35, False)),
            "bohyo_roof": (0.10, 1.00, -0.62, SILVER, "_w0", 0.0, None, -2.0, 2.0, 0.0, (0.50, 0.11, 1.4, False)),
            "ab_bohyo_lean": (0.09, 0.85, -0.60, SILVER, "_w2", 0.06, None, 9.0, -17.0, 0.05,
                              (0.48, 0.07, 1.4, False)),
        }
        names = {"bohyo_new": ("bohyo_jonen_shinji_kyoho15", "_w0"), "bohyo_s": ("bohyo_shungaku_doji_kyoho14", "_w2"),
                 "bohyo_roof": ("bohyo_soshin_shinji_kyoho13", "_w1"),
                 "ab_bohyo_lean": ("bohyo_dosen_zenjomon_kyoho9", "_w2")}''')
rep('''            post, pc = bohyo_post(a, h, z0, mat, wr, tip, th=th, crop=crop, cap=(kind == "bohyo_roof"),
                                  ink="_w1" if wr == "_w0" else "_w2")''', '''            post, pc = bohyo_post(a, h, z0, mat, wr, tip, th=th, crop=crop, cap=(kind == "bohyo_roof"),
                                  ink=names[kind][1], cell=names[kind][0])''')
rep('''            "bohyo_s": "a small post (a child's or a very poor grave), silver-grey, half the nenbutsu "
                                       "left",''', '''            "bohyo_s": "a small post (a child's grave), silver-grey, the child's name faded",''')
rep('''                            "ab_bohyo_lean": "grey post leaning hard back and aside, the mound slumped, ink half "
                                             "gone"}[kind])''', '''                            "ab_bohyo_lean": "grey post leaning hard back and aside, the mound slumped, the name "
                                             "a ghost"}[kind])''')
rep('''               "inscriptions: two posthumous names (1705, 1724) from the carved-text atlas, cropped for variety; no "
               "family-name stones (Meiji)",''', '''               "inscriptions (M1): a posthumous name and date per stone from jp_m_decal_carved_text_grave (1670-1729: "
               "-shinji / -shinnyo, -zenjomon / -zenjoni, -doji, shaku-, kigen / enjaku prefixes) + B1's two; no "
               "family-name stones (Meiji); gorinto / hokyointo stay blank (no Siddham font for the seed syllables)",''')
open(P, "wb").write(s.encode())
print("patched")
