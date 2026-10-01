"""SH1 shrine: a village shrine (sato-miya) on the flat at the foot of the hill north of the town, an oku-miya stair
climbing the hillside to an upper shrine, and an Inari corner up a narrow vermilion stair. Dressing only: no shrine
building exists yet (the hall site is left empty and marked).

Every object: (id, p3d basename, x, z, yaw, y, label). y: None = seated on its lowest footprint corner (terrain_sh1.seat),
a float = the y_offset over the ground at (x, z) (stairs and things set on them). yaw clockwise from north; the props'
+z is their front, so yaw 180 faces south (towards the town), 90 faces east, 270 west.
"""
import math

import terrain_sh1 as T

AX = 1024.0                    # the main approach (sando) runs north along x = 1024
DZ = 15.0                      # the precinct (everything after the first torii) sits 15 m further north
OKU_X = 1042.0                 # the oku-miya stair
INARI_X = 1058.0               # the Inari stair

# ------------------------------------------------------------------------------------------------ stairs
W3, W3N, D3, R3, D6, D6W, HV, HVR = (
    ("jp_s_stone_steps_dressed_3_wide", 0.91, 0.48, 0.12), ("jp_s_stone_steps_dressed_3_narrow", 0.91, 0.48, 0.12),
    ("jp_s_stone_steps_dressed_3", 0.91, 0.48, 0.12), ("jp_s_stone_steps_rough_3", 0.91, 0.48, 0.13),
    ("jp_s_stone_steps_dressed_6", 1.82, 0.96, 0.12), ("jp_s_stone_steps_dressed_6_wide", 1.82, 0.96, 0.12),
    ("jp_s_stone_steps_ab_heaved", 1.82, 0.96, 0.13), ("jp_s_stone_steps_ab_heaved_rough", 0.91, 0.48, 0.13))
R3N = ("jp_s_stone_steps_rough_3_narrow", 0.91, 0.48, 0.13)
LAND = ("jp_s_stone_steps_landing", 1.82, 0.18)
LAND_W = ("jp_s_stone_steps_landing_wide", 1.82, 0.18)
WIDTH = {"dressed_3_wide": 2.73, "dressed_6_wide": 2.73, "landing_wide": 2.73, "dressed_3_narrow": 0.91,
         "rough_3_narrow": 0.91}


def width_of(name):
    for k, v in WIDTH.items():
        if name.endswith(k):
            return v
    return 1.82


def oku_pick(i, z):
    """The oku-miya stair: wide dressed flights at the bottom, then normal dressed / rough, the old heaved upper
    flights, and 6-step flights where the slope allows (top)."""
    if z < 1231.0:
        return [W3]
    if z < 1247.0:
        return [D3] if i % 2 else [R3]
    if z >= 1258.5:
        return [D6W + (0.06,), D6 + (0.06,), D3] if i % 2 else [D6 + (0.06,), D6W + (0.06,), D3]
    return [[D6 + (0.06,), HV + (0.06,), D3], [HVR, R3], [HV + (0.06,), D6 + (0.06,), R3], [D3]][i % 4]


def inari_pick(i, z):
    return [W3N] if i % 2 else [R3N]


def build_stair(x, z0, z_end, pick, tag, first_cheeks=0):
    """Fit the stair (terrain_sh1.fit_stair, one flight list per position) and return its objects. Landings follow
    the width of the flight below them. first_cheeks: cheek walls on both sides of the first N flights."""
    objs = []

    def picker(i, z):
        return pick(i, z)
    mods, worst = T.fit_stair(x, z0, z_end, [W3], LAND, pick=picker)
    prev_w = 1.82
    nfl = 0
    for k, (name, mx, mz, my, kind, length) in enumerate(mods):
        if kind == "landing":
            name = LAND_W[0] if prev_w > 2.0 else LAND[0]
        else:
            prev_w = width_of(name)
        yo = my - T.ground(mx, mz)
        objs.append(("%s%02d" % (tag, k + 1), name, mx, mz, 180.0, yo,
                     "%s %s (%s)" % (kind, name.replace("jp_s_stone_steps_", ""),
                                     "visible %.2f m" % length if kind == "landing" else "%.2f m run" % length)))
        if kind == "flight":
            if nfl < first_cheeks or name == D6[0]:
                half = width_of(name) / 2.0 + 0.10
                cheek = "jp_s_stone_steps_cheek_3" if length < 1.0 else "jp_s_stone_steps_cheek_6"
                for sgn, side in ((-1, "E"), (1, "W")):
                    # yaw 180: model +x -> world -x, so model -half (sgn -1) is world east
                    objs.append(("%s%02d%s" % (tag, k + 1, side), cheek, mx - sgn * half, mz, 180.0, yo,
                                 "cheek wall beside that flight"))
            nfl += 1
    return objs, mods, worst


def stair_point(mods, z):
    """(y_offset over the ground, kind) of the stair top surface at z (for torii / things standing on it)."""
    for name, mx, mz, my, kind, length in mods:
        if kind == "flight" and mz <= z <= mz + length:
            return None, "flight"
        if kind == "landing" and mz <= z <= mz + length:
            return my - T.ground(mx, z), "landing"
    return None, None


# ------------------------------------------------------------------------------------------------ the layout
def layout():
    O = []

    def add(i, name, x, z, yaw, label, y=None, grp=None):
        O.append((i, name, x, z, yaw, y, label, {"grp": grp} if grp else {}))

    # --- the main approach, south to north -------------------------------------------------------------
    add("S01", "jp_s_torii_stone_l", AX, 1099.5, 180, "ichi-no-torii: large stone torii, plain (at the town end of the approach)")
    add("S02", "jp_s_nobori_shrine", AX - 5.2, 1103.0, 180, "shrine banners (festival leftovers), west")
    add("S03", "jp_s_nobori_shrine", AX + 5.2, 1103.0, 180, "shrine banners, east")
    add("S04", "jp_s_stone_lantern_kasuga_18", AX - 3.0, DZ + 1107.0, 90, "Kasuga lantern 1.8 m, west of the pair")
    add("S05", "jp_s_stone_lantern_kasuga_18", AX + 3.0, DZ + 1107.0, 270, "Kasuga lantern 1.8 m, east of the pair")
    # the stele corner (roadside stones gathered at the shrine edge), west side
    add("S06", "jp_s_stele_group3", AX - 7.4, DZ + 1110.0, 90, "stele corner: three old stones on one base")
    add("S07", "jp_s_stele_koshin", AX - 6.8, DZ + 1112.6, 90, "stele corner: Koshin stone")
    add("S08", "jp_s_stele_relief_panel", AX - 6.9, DZ + 1114.2, 90, "stele corner: relief panel")
    add("S09", "jp_s_stele_arched", AX - 7.0, DZ + 1115.7, 90, "stele corner: arched stele")
    add("S10", "jp_s_stele_round", AX - 8.4, DZ + 1113.6, 90, "stele corner: round-topped stone")
    add("S11", "jp_s_stele_pillar", AX - 8.6, DZ + 1111.9, 90, "stele corner: pillar stone (waymark)")
    add("S12", "jp_s_stele_ab_tipped", AX - 9.0, DZ + 1116.6, 60, "stele corner: a stele tipped over")
    add("S13", "jp_s_stele_natural_slab", AX - 8.9, DZ + 1108.4, 100, "stele corner: natural slab")
    add("S14", "jp_s_torii_stone_l_rope_shide", AX, DZ + 1121.5, 180, "ni-no-torii: large stone torii with straw rope + paper streamers (the precinct boundary)")
    add("S15", "jp_s_chozubachi_large", AX - 5.0, DZ + 1125.5, 90, "the water basin (chozubachi), large, dry and leaf-filled")
    add("S16", "jp_s_stone_lantern_kasuga_24", AX - 3.0, DZ + 1128.5, 90, "Kasuga 2.4 m, west")
    add("S17", "jp_s_stone_lantern_kasuga_24", AX + 3.0, DZ + 1128.5, 270, "Kasuga 2.4 m, east")
    add("S18", "jp_s_stone_lantern_square_24", AX - 3.0, DZ + 1134.5, 90, "square lantern 2.4 m, west")
    add("S19", "jp_s_stone_lantern_square_24", AX + 3.0, DZ + 1134.5, 270, "square lantern 2.4 m, east")
    add("S20", "jp_s_stone_lantern_kasuga_24_moss", AX - 3.0, DZ + 1140.5, 90, "Kasuga 2.4 m mossy, west")
    add("S21", "jp_s_stone_lantern_kasuga_24_moss", AX + 3.0, DZ + 1140.5, 270, "Kasuga 2.4 m mossy, east")
    add("S22", "jp_s_torii_wood_myojin_moss_rope_shide", AX, DZ + 1146.0, 180, "san-no-torii: wooden myojin, mossy, rope + streamers")
    add("S23", "jp_s_stone_lantern_square_24_moss", AX - 3.0, DZ + 1151.0, 90, "square lantern 2.4 m mossy, west")
    add("S24", "jp_s_stone_lantern_square_24_moss", AX + 3.0, DZ + 1151.0, 270, "square lantern 2.4 m mossy, east")
    add("S25", "jp_s_stone_lantern_kasuga_18_moss", AX - 3.0, DZ + 1157.0, 90, "Kasuga 1.8 m mossy, west")
    add("S26", "jp_s_stone_lantern_ab_hoju_moss", AX + 3.0, DZ + 1157.0, 270, "Kasuga 1.8 m mossy, its top jewel fallen (abandoned), east")
    add("S27", "jp_s_stone_lantern_kasuga_30", AX - 3.2, DZ + 1163.0, 90, "Kasuga 3.0 m, west")
    add("S28", "jp_s_stone_lantern_kasuga_30", AX + 3.2, DZ + 1163.0, 270, "Kasuga 3.0 m, east")
    add("S29", "jp_s_stone_lantern_joyato", AX - 5.0, DZ + 1168.0, 90, "joyato (always-lit lantern on a two-step base), west")
    add("S30", "jp_s_stone_lantern_joyato", AX + 5.0, DZ + 1168.0, 270, "joyato, east")
    add("S31", "jp_s_stone_lantern_oki", AX - 2.2, DZ + 1169.6, 90, "small placed lantern (oki) at the hall front, west")
    add("S32", "jp_s_stone_lantern_oki_moss", AX + 2.2, DZ + 1169.6, 270, "small placed lantern (oki), mossy, east")
    # the hall site z 1186-1198 is left EMPTY (no shrine building yet)
    # the sacred tree beside the hall site: a vanilla beech with a straw rope round the trunk (S34)
    add("S33", "t_fagussylvatica_3f", 1033.0, DZ + 1183.0, 0, "the sacred tree: a vanilla beech (placement only)", y=-0.06)
    # trunk centre at 1.0-1.8 m: model (0.33, 0.12) (P:\dz\plants\tree\t_fagussylvatica_3f.p3d LOD 1, measured)
    add("S34", "jp_s_shimenawa_wrap_d06", 1033.0 + 0.33, DZ + 1183.0 + 0.12, 0, "straw rope (shimenawa) with streamers round the sacred tree", y=-0.06)

    # --- the east row of small sub-shrines (sessha / massha) facing the approach: every small torii form ------------
    row = [("jp_s_torii_wood_shinmei", "wooden shinmei torii, plain", "jp_s_jizo_hut_stone_roof"),
           ("jp_s_torii_wood_shinmei_rope", "wooden shinmei, straw rope", "jp_s_stele_natural_slab"),
           ("jp_s_torii_wood_shinmei_rope_shide", "wooden shinmei, rope + streamers", "jp_s_jizo_hut_stone_roof"),
           ("jp_s_torii_stone_s", "small stone torii, plain", "jp_s_stele_round"),
           ("jp_s_torii_stone_s_rope", "small stone torii, rope", "jp_s_jizo_hut_stone_roof"),
           ("jp_s_torii_stone_s_rope_shide", "small stone torii, rope + streamers", "jp_s_stele_natural_slab"),
           ("jp_s_torii_wood_shinmei_moss", "wooden shinmei, mossy", "jp_s_jizo_hut_stone_roof"),
           ("jp_s_torii_wood_shinmei_moss_rope", "wooden shinmei, mossy, rope", "jp_s_stele_arched"),
           ("jp_s_torii_wood_shinmei_moss_rope_shide", "wooden shinmei, mossy, rope + streamers", "jp_s_jizo_hut_stone_roof"),
           ("jp_s_torii_stone_s_moss", "small stone torii, mossy", "jp_s_stele_natural_slab"),
           ("jp_s_torii_stone_s_moss_rope_shide", "small stone torii, mossy, rope + streamers", "jp_s_jizo_hut_stone_roof"),
           ("jp_s_torii_wood_ab_rotted", "a rotted wooden torii (abandoned sub-shrine)", "jp_s_jizo_hut_ab_open")]
    for k, (tor, lab, back) in enumerate(row):
        z = DZ + 1130.0 + 4.0 * k
        x = 1036.0 + (0.25 if k % 3 == 1 else (-0.2 if k % 3 == 2 else 0.0))
        add("S%02d" % (40 + k), tor, x, z, 270, "sub-shrine row %d: %s" % (k + 1, lab))
        hut = "jp_s_jizo_hut_stone_roof" == back or back == "jp_s_jizo_hut_ab_open"
        add("S%02dh" % (40 + k), back, x + (2.2 if hut else 1.6), z, 270,
            "  behind it: %s (stand-in for a small shrine)" % back.replace("jp_s_", ""))
    # yard-shrine mini torii in front of two of the stone huts
    add("S52", "jp_s_torii_wood_mini", 1037.15, DZ + 1130.0, 270, "mini torii (yard shrine), plain, before row 1's hut")
    add("S53", "jp_s_torii_wood_mini_rope", 1036.65, DZ + 1146.0, 270, "mini torii, rope, before row 5's hut")

    # --- the path up to the oku-miya: a lantern pair, then the stair foot torii -------------------------------
    # the earth path from the hall site up to the stair foot, lined with lantern pairs
    p0, p1 = (1031.0, 1201.0), (OKU_X, 1223.5)
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dz)
    ux, uz = dx / ln, dz / ln
    nx, nz = uz, -ux                             # to the right (east) of the path, walking up
    yaw_l = (math.degrees(math.atan2(nx, nz))) % 360.0          # left lantern faces the path (east-ish)
    yaw_r = (yaw_l + 180.0) % 360.0
    for k, (t, left, right, lab) in enumerate([
            (0.18, "jp_s_stone_lantern_kasuga_30_moss", "jp_s_stone_lantern_ab_toppled",
             "Kasuga 3.0 m mossy / its twin toppled (abandoned)"),
            (0.50, "jp_s_stone_lantern_kasuga_18_moss", "jp_s_stone_lantern_kasuga_18_moss", "Kasuga 1.8 m mossy pair"),
            (0.80, "jp_s_stone_lantern_square_24_moss", "jp_s_stone_lantern_square_24_moss", "square 2.4 m mossy pair")]):
        cx, cz = p0[0] + dx * t, p0[1] + dz * t
        off = 2.4 if right != "jp_s_stone_lantern_ab_toppled" else 2.4
        add("S%02d" % (90 + 2 * k), left, cx - nx * 2.4, cz - nz * 2.4, yaw_l, "path to the hill stair: " + lab + " (west)")
        rx, rz = cx + nx * (3.4 if "toppled" in right else 2.4), cz + nz * (3.4 if "toppled" in right else 2.4)
        add("S%02d" % (91 + 2 * k), right, rx, rz, (yaw_r + (35 if "toppled" in right else 0)) % 360,
            "path to the hill stair: " + lab + " (east)")
    add("S62", "jp_s_torii_wood_ab_leaning", 1047.0, 1205.5, 195, "an old wooden torii leaning in the trees (abandoned)")
    stair, mods, worst = build_stair(OKU_X, 1215.0, 1262.0, oku_pick, "K", first_cheeks=2)
    z_foot = mods[0][2]
    # FB1 (2026-10-01): the medium stone torii's nuki is 1.93 m over its base (1.81 m clear on the path here, 1.66 at
    # the stair head: Stephen was blocked walking down). Walk-through torii need >= 2.20 m (spikes/FB1/toriiclear.py):
    # the stair line takes the large stone torii (nuki 2.94).
    add("S63", "jp_s_torii_stone_l_rope_shide", OKU_X, z_foot - 1.6, 180, "large stone torii, rope + streamers, at the foot of the hill stair (FB1: was medium, too low)")
    O += [(i, n, x, z, yaw, y, "hill stair " + lab, {}) for (i, n, x, z, yaw, y, lab) in stair]
    # wooden myojin torii spanning the stair on landings, every ~7 m
    myo = [("jp_s_torii_wood_myojin", "wooden myojin torii over the stair, plain"),
           ("jp_s_torii_wood_myojin_rope", "wooden myojin over the stair, rope"),
           ("jp_s_torii_wood_myojin_rope_shide", "wooden myojin over the stair, rope + streamers"),
           ("jp_s_torii_wood_myojin_moss", "wooden myojin over the stair, mossy"),
           ("jp_s_torii_wood_myojin_moss_rope", "wooden myojin over the stair, mossy, rope")]
    lands = []
    for k, m in enumerate(mods):
        if m[4] == "landing" and m[5] >= 0.40 and k > 0 and width_of(mods[k - 1][0]) == 1.82 \
                and (k + 1 >= len(mods) or width_of(mods[k + 1][0]) == 1.82):
            lands.append(m)
    targets = [max(z_foot + 5.0, 1233.0) + 5.5 * k for k in range(len(myo))]
    used = set()
    for k, (n, lab) in enumerate(myo):
        best = min((m for m in lands if id(m) not in used), key=lambda m: abs(m[2] - targets[k]), default=None)
        if best is None:
            break
        used.add(id(best))
        zz = best[2] + min(best[5], 0.6) / 2.0
        add("S%02d" % (64 + k), n, OKU_X, zz, 180, lab, grp="over:stairK")
    top_z = mods[-1][2] + mods[-1][5]
    top_y = mods[-1][3] + (0.48 if mods[-1][4] == "flight" else 0.0)
    # the oku-miya at the stair head (on the slope)
    add("S70", "jp_s_torii_stone_l", OKU_X, top_z + 1.2, 180, "large stone torii, plain, at the head of the stair (oku-miya; FB1: was medium, too low)", grp="over:stairK")
    add("S71", "jp_s_jizo_hut_stone_roof", OKU_X, top_z + 4.2, 180, "oku-miya: a stone-roofed hut (stand-in for the upper shrine)")
    add("S72", "jp_s_stone_lantern_oki_moss", OKU_X - 1.6, top_z + 2.8, 180, "oku-miya oki lantern, mossy, west")
    add("S73", "jp_s_stone_lantern_oki_moss", OKU_X + 1.6, top_z + 2.8, 180, "oku-miya oki lantern, mossy, east")
    add("S74", "jp_s_chozubachi_natural", OKU_X + 3.1, top_z + 0.6, 180, "a natural-stone basin at the oku-miya")   # FB1: clear of the larger S70

    # --- the Inari corner: a narrow stair through vermilion torii ------------------------------------------------
    istair, imods, iworst = build_stair(INARI_X, 1212.0, 1240.0, inari_pick, "I")
    iz = imods[0][2]
    add("S80", "jp_s_torii_wood_myojin_shu_rope_shide", INARI_X, iz - 1.2, 180, "Inari: vermilion myojin torii, rope + streamers, at the foot of the narrow stair")
    O += [(i, n, x, z, yaw, y, "Inari stair " + lab, {}) for (i, n, x, z, yaw, y, lab) in istair]
    ilands = [m for m in imods if m[4] == "landing" and m[5] >= 0.35]
    if ilands:
        m = ilands[len(ilands) // 2]
        add("S81", "jp_s_torii_wood_myojin_shu", INARI_X, m[2] + min(m[5], 0.5) / 2, 180, "Inari: vermilion myojin torii, plain, over the stair", grp="over:stairI")
    add("S82", "jp_s_torii_wood_ab_leaning_shu", INARI_X + 4.5, 1213.0, 165, "Inari: a vermilion torii leaning at the foot of the Inari path (abandoned)")
    itop = imods[-1][2] + imods[-1][5]
    add("S83", "jp_s_torii_wood_mini_shu", INARI_X, itop + 1.0, 180, "Inari: mini vermilion torii before the shrine", grp="over:stairI")
    add("S84", "jp_s_jizo_hut_stone_roof", INARI_X, itop + 2.2, 180, "Inari: stone-roofed hut (stand-in for the Inari shrine)")
    add("S85", "jp_s_chozubachi_ab_dry", INARI_X - 2.4, itop - 0.6, 180, "Inari: a basin cracked and dry (abandoned)")
    # --- FB1 (2026-10-01): FP1's collapsed torii (jp_site, mount 'shrine'; origin between the post feet, +z = the
    # approach side the wreck fell towards; the typhoon one lies behind its post line), on the flattest ground at the foot of the
    # hill (terrain relief <= 0.5 m over the wreck), off every path: the dead world's shrine has lost a few gates
    add("S100", "jp_s_torii_fallen_stone_quake", 1052.0, 1172.0, 270, "collapsed stone torii (the 1707 quake), behind the sub-shrine row")
    add("S101", "jp_s_torii_fallen_stone_quake_old", 1003.0, 1150.0, 180, "collapsed stone torii, mossy and sunk (a long-ago collapse), north of the graveyard")
    add("S102", "jp_s_torii_fallen_myojin_typhoon", 1008.0, 1178.0, 135, "wooden myojin torii blown over by a typhoon, west of the approach")
    add("S103", "jp_s_torii_fallen_shinmei_rot", 1056.0, 1188.0, 200, "wooden shinmei torii fallen with its feet rotted, in the trees east of the hall site")
    add("S104", "jp_s_torii_fallen_shu_snapped", 1066.0, 1190.0, 170, "Inari: a vermilion torii snapped at the posts, below the Inari path")
    return O, {"oku": (mods, worst), "inari": (imods, iworst)}
