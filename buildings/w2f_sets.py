"""W2F (2026-10-01): the dressings of the wave-2 furnished variants (shrine, temple, tea house, smithy, guard posts)
for buildings/furnishkit.py. SETS are merged into buildings/furnish_sets.SETS (like shop_sets).

Binding rules as furnish_sets.py (G1 A2, BUILD_LIST, LIFE_LAYER): 5-7 counted props a room, <= 25 % floor cover, a
1.00 m band door-to-door and door-to-centre, >= 1 raised loot surface a room, moderate "as left" disorder; shrines,
altars and their offerings UNDISTURBED (dust, dried sakaki, no loot on them). Autumn, dead world.
W2F adds (decor.py): a space that is not a living room (a shrine en, a pavilion, a gate passage, a bell platform, a
dance stage kept clear) is marked sparse(): D1 takes 0-7 props there, D3 is not required and D4 has no centre target.
The new specialty props are spikes/W2F/props_w2f_*.py (jp_furniture); the spots are the shells' rooms-json fittings
(W2S / W2C). Research: spikes/W2F/W2F_NOTES.md.
"""
import math

ROPE_NOTE = "visual only, no collision"


# ------------------------------------------------------------------------------------------------ helpers
def sparse(c, room, why):
    c.room[room]["sparse"] = why


def fit1(c, room, kind):
    f = c.fit(room, kind)
    if not f:
        raise KeyError("%s has no %s fitting in %s" % (c.key, kind, room))
    return f[0]


def ceil_y(c, x, z, y_from, clear=1.2):
    """Lowest visual solid bottom above (x, z) higher than y_from + clear (the hall ceiling / beam over a spot)."""
    best = None
    for s in c.M.solids:
        if 1 not in s.vis:
            continue
        b = s.bbox()
        if b[0] <= x <= b[1] and b[4] <= z <= b[5] and b[2] > y_from + clear:
            best = b[2] if best is None else min(best, b[2])
    return best


def face_off(c, room, side, at, h=1.2, reach=0.6):
    """How far the real wall face lies behind the room rect edge on `side` at `at` (the halls' board walls sit
    between round columns, behind the column-face rect): the nearest visual solid behind the edge at h over the floor
    that spans `at`."""
    x0, x1, z0, z1 = c.R(room)
    y = c.y(room) + h
    best = None
    for s in c.M.solids:
        if not s.geo:
            continue
        b = s.bbox()
        if not (b[2] <= y <= b[3]):
            continue
        if side in ("zmin", "zmax"):
            if not (b[0] <= at <= b[1]):
                continue
            d = (z0 - b[5]) if side == "zmin" else (b[4] - z1)
        else:
            if not (b[4] <= at <= b[5]):
                continue
            d = (x0 - b[1]) if side == "xmin" else (b[0] - x1)
        if -0.02 <= d <= reach and (best is None or d < best):
            best = d
    best = best or 0.0
    return best if best > 0.03 else 0.0          # a few cm: the D10 wall test reaches it from the rect edge


def onw(c, room, side, at, name, why=""):
    """c.onwall, its plane on the real wall face (face_off)."""
    from jpparts import decor as DC
    import furnishkit as FK
    x, z, yaw = c._wall_pose(room, side, at, FK.WALL_INSET - face_off(c, room, side, at), 0.0)
    it = c.D.place(DC.on_wall(name, room, x, z, yaw, why=why))
    it["on_floor"] = False           # heights built in; the open sheds' earth floors stop short of the wall plane
    return it


def wallp(c, room, side, at, name, why="", y=None, gap=0.03, push=0.0):
    """c.wall; a wall-anchored prop (shelf) goes on the real wall face, a floor prop keeps its gap off the rect edge
    (the columns stand proud of the board walls)."""
    from jpparts import decor as DC
    if DC.catalog()[name]["anchor"] == "wall":
        return c.wall(room, side, at, name, off=push - face_off(c, room, side, at), y=c.y(room) if y is None else y,
                      why=why)
    return c.wall(room, side, at, name, gap=gap, y=y, why=why)


def kamado_spot(c, room, n=1, k=0):
    f = c.fit(room, "kamado")[k]
    (cx, cz), yaw, (w, d) = f["centre"], f["yaw"], f["size"]
    if round(yaw) % 180 == 0:
        rect = (cx - w / 2, cx + w / 2, cz - d / 2, cz + d / 2)
    else:
        rect = (cx - d / 2, cx + d / 2, cz - w / 2, cz + w / 2)
    mouth = {0: "+z", 90: "+x", 180: "-z", 270: "-x"}[int(round(yaw)) % 360]
    if k == 0:
        return c.kamado(room, rect, mouth, n=n)
    # a second kamado in the same room: furnishkit keeps one per room (c.kam[room]); keep both rect obstacles
    from jpparts import fittings as FT
    kk = FT.kamado(c.M, rect, c.y(room), mouth=mouth, n=n, tier=2)
    x0, x1, z0, z1 = rect
    c.floor[room]["obstacles"].append((x0 - 0.25, x1 + 0.25, z0 - 0.25, z1 + 0.25))
    c.fixed.setdefault(room, []).append(rect)
    return kk


def pot_in(c, room, kd, name, k, why):
    from jpparts import decor as DC
    x, z = kd["rims"][k]
    sy = DC.catalog()[name]["seat_y"] or 0.168
    return c.D.place(DC.item(name, room, x, z, 0.0, y=kd["rim_top"] - sy, seat=kd["seat"], why=why))


def stair_foot_z(c, room):
    """z just past the foot of the front kizahashi of an en at floor y (38 deg stair)."""
    x0, x1, z0, z1 = c.R(room)
    return z1 + c.y(room) / math.tan(math.radians(37.0)) + 0.30


# ================================================================================================ SHINTO
def shrine_haiden_town(c):
    """Town haiden (Hachimangu): the worship floor with the big drum, the offering table under the god shelf, the
    ritual chest; the en with the bell rope; the offering box at the foot of the steps (the en is too shallow in front
    of the one door: on the ground, as at many shrines); the name board over the worship bay."""
    f = fit1(c, "haiden", "drum")
    c.free("haiden", "jp_f_odaiko", f["centre"][0] + 0.05, f["centre"][1] + 0.05, 90.0, why="the big drum on its stand")
    wallp(c, "haiden", "zmin", 0.0, "jp_f_hassokuan_l", why="offering table under the god shelf, offerings as left")
    for sx in (-1, 1):
        c.free("haiden", "jp_f_shokudai_tall", sx * 0.95, -1.80, 0.0, why="tall candle stand beside the offerings")
    n = wallp(c, "haiden", "xmax", -0.95, "jp_f_nagamochi", why="the chest of ritual robes and implements")
    c.free("haiden", "jp_f_enza_stack3", -2.80, 1.35, 10.0, why="straw cushions stacked for the elders")
    onw(c, "haiden", "zmin", 0.0, "jp_f_kamidana_plain", why="offering shelf on the back wall, undisturbed")
    onw(c, "haiden", "zmin", 0.0, "jp_f_kamidana_set_shimenawa_old", why="its sacred rope")
    onw(c, "haiden", "xmin", 0.40, "jp_f_ema_rail", why="votive boards on the side wall")
    onw(c, "haiden", "xmax", 1.10, "jp_f_ema_rail", why="votive boards on the side wall")
    f = fit1(c, "en", "suzu")
    c.hang("en", "jp_f_suzu_rope_faded", f["centre"][0], f["centre"][1], f["y"], over=ROPE_NOTE,
           why="the bell and its pull rope from the kohai beam")
    sparse(c, "en", "the veranda before the worship bay")
    sparse(c, "en_left", "side veranda")
    sparse(c, "en_right", "side veranda")
    c.front("jp_f_gaku_hachimangu", 0.0, 2.43, 3.04, why="the shrine name board over the worship bay")
    c.site("jp_f_saisen_bako_l", 0.0, stair_foot_z(c, "en") + 0.90, 0.0, why="the offering box at the foot of the steps")


def shrine_haiden_village(c):
    f = fit1(c, "haiden", "drum")
    c.free("haiden", "jp_f_odaiko", f["centre"][0] + 0.10, f["centre"][1] + 0.12, 90.0, why="the drum on its stand")
    wallp(c, "haiden", "zmin", 0.0, "jp_f_hassokuan_s", why="offering table under the god shelf")
    c.free("haiden", "jp_f_shokudai_tall", 0.85, -1.45, 0.0, why="a candle stand beside the offerings")
    wallp(c, "haiden", "xmax", -0.70, "jp_f_nagamochi", why="the village's festival chest")
    c.free("haiden", "jp_f_enza_stack3", -2.20, 1.15, 10.0, why="straw cushions for the village elders")
    onw(c, "haiden", "zmin", 0.0, "jp_f_kamidana_plain", why="offering shelf, undisturbed")
    onw(c, "haiden", "xmin", 0.60, "jp_f_ema_rail", why="votive boards")
    f = fit1(c, "en", "suzu")
    c.hang("en", "jp_f_suzu_rope_faded", f["centre"][0], f["centre"][1], f["y"], over=ROPE_NOTE,
           why="the bell and its rope")
    sparse(c, "en", "the veranda before the doors")
    c.site("jp_f_saisen_bako_m", 0.0, stair_foot_z(c, "en") + 0.90, 0.0, why="the offering box at the foot of the steps")


def _sanctum(c, n, w):
    f = fit1(c, "en", "sanctum")
    x0, x1, z0, z1 = f["rect"]
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        c.front("jp_f_shintai_zushi_s" if n > 1 else "jp_f_shintai_zushi", x, z0 + 0.32, f["y"],
                why="the sealed sanctum: shrine cabinet, mirror, gohei (seen through the doors only)")


def shrine_honden_town(c):
    f = fit1(c, "en", "offering_table")
    c.free("en", "jp_f_hassokuan_l", f["centre"][0], f["centre"][1], 0.0, why="offering table before the sealed doors")
    _sanctum(c, 3, 0.42)
    for r, why in (("en", "the front veranda (the sanctum is sealed)"), ("en_left", "side veranda"),
                   ("en_right", "side veranda")):
        sparse(c, r, why)


def shrine_honden_village(c):
    f = fit1(c, "en", "offering_table")
    c.free("en", "jp_f_hassokuan_s", f["centre"][0], f["centre"][1], 0.0, why="offering table before the sealed doors")
    _sanctum(c, 1, 0.55)
    for r, why in (("en", "the front veranda (the sanctum is sealed)"), ("en_left", "side veranda"),
                   ("en_right", "side veranda")):
        sparse(c, r, why)


def shrine_temizuya(c):
    f = fit1(c, "pavilion", "basin")
    c.free("pavilion", "jp_s_chozubachi_large", f["centre"][0], f["centre"][1], 0.0,
           why="the stone basin (dry, leaf-filled)")
    c.free("pavilion", "jp_f_hishaku_rack", 0.0, -0.85, 0.0, count=True, why="the ladle rack behind the basin")
    sparse(c, "pavilion", "open purification pavilion")


def shrine_shamusho(c):
    """The priests' office: the amulet counter under the push-up shutter, the talisman desk, robes, the god shelf;
    the entry doma."""
    a = fit1(c, "office", "amulet_counter")
    x0, x1, z0, z1 = a["rect"]
    d = wallp(c, "office", "zmax", (x0 + x1) / 2, "jp_f_zukue_plain", gap=0.06, why="the amulet counter under the shutter")
    c.surf(d, "jp_f_ofuda_stack", why="talismans and amulets left on the counter")
    f = fit1(c, "office", "desk")
    d2 = wallp(c, "office", "zmin", f["centre"][0], "jp_f_zukue_choba", why="the talisman-making desk and registers")
    c.surf(d2, "jp_f_writing_box_open", why="brushes and ink, open")
    c.free("office", "jp_f_iko_robe", 0.20, -1.30, 0.0, why="the priest's robes on their rack")
    wallp(c, "office", "xmax", 0.10, "jp_f_tansu_single", why="a low chest")
    c.free("office", "jp_f_enza", 0.95, 0.55, 15.0, why="a straw cushion at the counter")
    c.free("office", "jp_f_box_s_lacquer", -0.30, 0.65, 20.0, why="a lacquered box of seals")
    onw(c, "office", "zmin", (fit1(c, "office", "kamidana")["rect"][0] + fit1(c, "office", "kamidana")["rect"][1]) / 2,
             "jp_f_kamidana_plain", why="the god shelf, undisturbed")
    # entry doma
    wallp(c, "doma", "zmin", -1.80, "jp_f_tana_091_1", why="a shelf by the entry")
    c.free("doma", "jp_f_oke_bucket", -2.35, 1.20, 15.0, why="a bucket by the door")
    c.free("doma", "jp_f_mizugame", -2.35, -0.50, 0.0, why="the water jar")
    c.free("doma", "jp_f_debris_leaves", -1.75, 0.60, 30.0, why="leaves blown in")
    c.free("doma", "jp_f_basket_kago", -1.30, -1.20, 0.0, why="a basket")
    onw(c, "doma", "xmin", 0.60, "jp_f_sandals_hung_wall", why="spare straw sandals")


def shrine_kagura(c):
    f = fit1(c, "stage", "drum")
    c.free("stage", "jp_f_kagura_drums", f["centre"][0], f["centre"][1], 200.0, why="the kagura drum and flute")
    wallp(c, "stage", "xmin", -0.70, "jp_f_nagamochi", why="the costume chest")
    c.free("stage", "jp_f_enza_stack3", 1.20, 0.40, 20.0, why="the musicians' cushions")
    m = fit1(c, "stage", "masks")
    onw(c, "stage", "zmin", (m["rect"][0] + m["rect"][1]) / 2, "jp_f_kagura_masks", why="masks and the bell tree")
    sparse(c, "stage", "the dance stage, kept clear")


# ================================================================================================ BUDDHIST
def _hall_props(c, room, dais, desk=True, zen=False):
    a = fit1(c, room, "altar")
    x0, x1, z0, z1 = a["rect"]
    d = wallp(c, room, "zmin", (x0 + x1) / 2, dais, why="the altar dais with the image, undisturbed")
    zf = d["z"] + 0.45
    for sx in (-1, 1):
        c.free(room, "jp_f_shokudai_tall", sx * ((x1 - x0) / 2 + 0.05), z1 + 0.25, 0.0, why="candle stand before the "
               "altar, burnt down")
    if desk:
        s = fit1(c, room, "sutra_desk")
        c.free(room, "jp_f_sutra_desk", s["centre"][0], s["centre"][1], 0.0, why="the sutra desk with bowl gong")
    hy = ceil_y(c, 0.0, (z0 + z1) / 2, c.y(room))
    if hy:
        c.hang(room, "jp_f_tengai", 0.0, (z0 + z1) / 2 + 0.10, hy, over="furniture (the altar)",
               why="the canopy over the image")
    return d


def temple_hondo_village(c):
    """Village hondo, Jodo: Amida in the zushi on the dais, the sutra desk, candle stands, the chest, cushions."""
    _hall_props(c, "hall", "jp_f_dais_amida")
    wallp(c, "hall", "xmin", -0.40, "jp_f_nagamochi", why="the chest of ritual vestments")
    c.free("hall", "jp_f_enza_stack3", -2.70, 2.40, 15.0, why="cushions for the congregation")
    f = fit1(c, "en", "saisen_bako")
    c.free("en", "jp_f_saisen_bako_m", f["centre"][0], f["centre"][1], 0.0, why="the donation box on the en")
    f = fit1(c, "en", "gong")
    c.hang("en", "jp_f_waniguchi", f["centre"][0], f["centre"][1], f["y"], over=ROPE_NOTE, why="the gong and rope")
    sparse(c, "en", "the veranda before the hall")


def temple_hondo_town(c):
    """Town hondo, Zen (Soto): Shaka in the zushi, the sutra desk, the big mokugyo, the drum, the chest."""
    _hall_props(c, "hall", "jp_f_dais_shaka")
    c.free("hall", "jp_f_mokugyo_l", 1.20, -0.95, 0.0, why="the big mokugyo (Zen)")
    c.free("hall", "jp_f_odaiko", -2.55, -2.55, 45.0, why="the hall drum")
    wallp(c, "hall", "xmax", 0.60, "jp_f_nagamochi", why="the chest of vestments")
    f = fit1(c, "en", "gong")
    c.hang("en", "jp_f_waniguchi", f["centre"][0], f["centre"][1], f["y"], over=ROPE_NOTE, why="the gong and rope")
    sparse(c, "en", "the veranda before the hall")
    c.site("jp_f_saisen_bako_l", 0.0, stair_foot_z(c, "en") + 0.90, 0.0, why="the donation box at the foot of the steps")


def temple_do(c, image, room_w):
    """Small sacred hall (Jizo / Kannon): the dais, candle stand, the village's chest and brazier (it is also the
    assembly hall), cushions, a lamp."""
    a = fit1(c, "hall", "altar")
    wallp(c, "hall", "zmin", (a["rect"][0] + a["rect"][1]) / 2, image, why="the dais with the image, undisturbed")
    c.free("hall", "jp_f_shokudai_tall", 0.95, a["rect"][3] + 0.20, 0.0, why="a candle stand, burnt down")
    wallp(c, "hall", "xmin", 0.10, "jp_f_box_l", why="the assembly's box of records")
    c.free("hall", "jp_f_hibachi_box", room_w / 2 - 0.60, 0.40, 0.0, why="a brazier (the hall is also the meeting place)")
    c.free("hall", "jp_f_enza_stack3", -(room_w / 2 - 0.55), -1.00 if room_w < 4 else 0.80, 10.0, why="cushions")
    c.free("hall", "jp_f_andon_kaku", room_w / 2 - 0.45, -0.80, 0.0, why="a standing lamp, unlit")
    if room_w < 4:
        f = fit1(c, "en", "saisen_bako")
        c.free("en", "jp_f_saisen_bako_s", f["centre"][0], f["centre"][1], 0.0, why="the donation box")
    else:                            # one front door: the en is too shallow before it, the box goes to the stair foot
        c.site("jp_f_saisen_bako_s", 0.0, stair_foot_z(c, "en") + 0.90, 0.0, why="the donation box at the stair foot")
    f = fit1(c, "en", "gong")
    c.hang("en", "jp_f_waniguchi", f["centre"][0], f["centre"][1], f["y"], over=ROPE_NOTE, why="the gong and rope")
    sparse(c, "en", "the veranda before the hall")


def temple_do_jizo(c):
    temple_do(c, "jp_f_dais_jizo", 3.52)


def temple_do_kannon(c):
    temple_do(c, "jp_f_dais_kannon", 5.34)


def temple_kuri(c, zen=False):
    """Priests' quarters + kitchen: the kamado row with the big pots, the water jar, shelves, firewood; the board
    daidokoro round the irori with the account desk; the guest room."""
    k0 = kamado_spot(c, "doma", n=2, k=0)
    pot_in(c, "doma", k0, "jp_f_kama", 0, "the big rice pot")
    pot_in(c, "doma", k0, "jp_f_seiro_kama2", 1, "a steamer stack")
    k1 = kamado_spot(c, "doma", n=2, k=1)
    pot_in(c, "doma", k1, "jp_f_kama_nolid", 0, "a pot, lid off")
    c.free("doma", "jp_f_mizugame", -3.80, -2.60, 0.0, why="the water jar")
    wallp(c, "doma", "zmin", -1.67, "jp_f_tana_136_3", why="the kitchen shelves")
    wallp(c, "doma", "xmin", 2.20, "jp_f_firewood_stack", why="split wood by the stoves")
    c.free("doma", "jp_f_oke_pickle", -2.40, 0.90, 0.0, why="a pickle tub")
    c.passage(("doma",), -1.50, 2.70, "kamachi step doma <-> daidokoro")
    if zen:
        c.hang("doma", "jp_f_gyoban", -3.76, 3.20, 3.0 if not ceil_y(c, -3.76, 3.2, 0.05) else
               min(3.0, ceil_y(c, -3.76, 3.2, 0.05)), over="by the entrance (Zen signal board)",
               why="the wooden fish board that calls the meals")
        c.hang("doma", "jp_f_umpan", -2.10, 3.30, 3.0 if not ceil_y(c, -2.10, 3.3, 0.05) else
               min(3.0, ceil_y(c, -2.10, 3.3, 0.05)), over="by the entrance (Zen signal gong)", why="the cloud gong")
    # daidokoro
    f = fit1(c, "daidokoro", "irori")
    hx, hy, hz = f["hook"]
    c.hang("daidokoro", "jp_f_jizai_kagi", hx, hz, hy, over="hearth", why="the pot hook over the irori")
    c.hang("daidokoro", "jp_f_hoshigaki_5", hx, hz + 0.95, hy, over="hearth", why="persimmons drying over the smoke")
    t = wallp(c, "daidokoro", "xmax", 1.67, "jp_f_tana_182_3", why="the meal-tray shelves")
    c.surf(t, "jp_f_tableware_hakozen_stack", surface="board_1", why="the stacked box trays")
    d = wallp(c, "daidokoro", "zmax", 3.60, "jp_f_zukue_choba", why="the temple's account desk")
    c.surf(d, "jp_f_choba_set_desk", why="the registers and abacus")
    c.free("daidokoro", "jp_f_kama_nabe_rusted", 2.95, 1.60, 0.0, why="a pot by the hearth, rusting")
    c.free("daidokoro", "jp_f_enza", 1.82, 2.75, 0.0, why="a straw cushion")
    c.free("daidokoro", "jp_f_andon_kaku", 0.00, 0.90, 0.0, why="a standing lamp, unlit")
    onw(c, "daidokoro", "zmax", 0.40, "jp_f_kamidana_plain", why="the kitchen god shelf")
    # guest room
    wallp(c, "guest", "zmin", 0.60, "jp_f_tansu_single", why="a chest")
    c.free("guest", "jp_f_futon_stack", 4.70, -3.00, 0.0, why="guest bedding folded in the corner")
    c.free("guest", "jp_f_andon_ariake", 0.10, -2.90, 0.0, why="night lamp, unlit")
    c.free("guest", "jp_f_byobu_makura", -0.25, -1.40, 90.0, why="a low screen")
    c.free("guest", "jp_f_tabakobon", 3.60, -2.10, 20.0, why="a tobacco tray")
    c.free("guest", "jp_f_enza", 2.90, -2.40, 0.0, why="a cushion")
    sparse(c, "genkan", "the entrance porch")


def temple_kuri_village(c):
    temple_kuri(c, zen=False)


def temple_kuri_town(c):
    temple_kuri(c, zen=True)


def temple_shoro(c):
    room = "platform" if "platform" in c.room else "upper"
    f = fit1(c, room, "bell")
    name = "jp_f_bonsho_s" if room == "platform" else "jp_f_bonsho_l"
    c.hang(room, name, f["centre"][0], f["centre"][1], f["y"], yaw=0.0 if room == "platform" else 90.0,
           over="the bell (walk round it)", why="the temple bell and its striker log")
    sparse(c, room, "the bell platform")


def temple_gate(c):
    f = fit1(c, "gate", "gaku")
    c.front("jp_f_gaku_worn_h", f["centre"][0], f["centre"][1] + 0.10, f["y"], why="the name board, weathered blank")
    sparse(c, "gate", "the gate passage")


# ================================================================================================ civic
def _benches(c, room, spot, k, inside=True):
    x0, x1, z0, z1 = spot["rect"]
    out = []
    n = 2 if (x1 - x0) > 2.4 else 1
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        b = c.free(room, "jp_s_bench_1ken", x, (z0 + z1) / 2, 0.0, why="a tea bench (shogi)")
        out.append(b)
    return out


def teahouse_bench(c):
    """Kake-jaya: the kettle hearth, a bench along the open front and one under the bench roof, the tea things left
    on a bench."""
    kd = kamado_spot(c, "doma", n=1)
    pot_in(c, "doma", kd, "jp_f_kama", 0, "the kettle pot left on the hearth")
    b = c.free("doma", "jp_s_bench_1ken", -0.80, 1.95, 0.0, why="a tea bench (shogi) along the open front")
    c.surf(b, "jp_s_bench_dress_tea", why="tea bowls and a pot left on the bench")
    c.free("doma", "jp_s_bench_1ken", 0.70, 2.66, 0.0, why="a bench under the bench roof")
    c.free("doma", "jp_f_mizugame", 1.35, -0.95, 0.0, why="the water jar")
    c.free("doma", "jp_s_stool_std", 1.20, 1.40, 30.0, why="a stool")
    c.free("doma", "jp_f_debris_leaves", 0.50, 0.20, 40.0, why="leaves blown in")


def teahouse_shop(c):
    kd = kamado_spot(c, "doma", n=1)
    pot_in(c, "doma", kd, "jp_f_kama", 0, "the kettle pot left on the hearth")
    b = c.free("doma", "jp_s_bench_1ken", -1.50, 1.05, 0.0, why="a tea bench by the open front")
    c.surf(b, "jp_s_bench_dress_tea", why="tea bowls left on the bench")
    c.free("doma", "jp_s_stool_std", 0.35, 1.30, 30.0, why="a stool")
    c.free("doma", "jp_f_mizugame", -2.30, -0.35, 0.0, why="the water jar")
    wallp(c, "doma", "zmin", -1.25, "jp_f_tana_091_1", push=0.025, why="a shelf of cups")
    if c.fit("doma", "bench_spot"):
        sp = c.fit("doma", "bench_spot")[0]
        c.free("doma", "jp_s_bench_long", (sp["rect"][0] + sp["rect"][1]) / 2, (sp["rect"][2] + sp["rect"][3]) / 2,
               0.0, why="the long bench under the bench roof")
    # agari
    c.free("agari", "jp_f_hibachi_box", 1.85, -1.10, 0.0, why="a box brazier")
    c.free("agari", "jp_f_tabakobon_spilled", 1.30, 0.20, 25.0, why="a tobacco tray knocked over")
    c.free("agari", "jp_f_enza", 2.20, 0.60, 0.0, why="a straw cushion")
    c.free("agari", "jp_f_meal_left_two", 1.75, 1.20, 10.0, why="two trays of food left")
    c.free("agari", "jp_f_andon_kaku", 2.35, -1.45, 0.0, why="a standing lamp, unlit")


def teahouse_tateba(c):
    kd = kamado_spot(c, "doma", n=1)
    pot_in(c, "doma", kd, "jp_f_kama", 0, "the big kettle")
    b = c.free("doma", "jp_s_bench_1ken", -3.50, 1.60, 0.0, why="a bench by the open front")
    c.surf(b, "jp_s_bench_dress_tea", why="tea things left on the bench")
    c.free("doma", "jp_f_mizugame", -3.20, -2.25, 0.0, why="the water jar")
    wallp(c, "doma", "xmin", 0.40, "jp_f_taru_rack3", why="sake casks on their rack (it serves sake)")
    c.free("doma", "jp_f_firewood_bundle", -3.30, -0.90, 80.0, why="brushwood")
    sp = c.fit("doma", "bench_spot")
    if sp:
        c.free("doma", "jp_s_bench_long", (sp[0]["rect"][0] + sp[0]["rect"][1]) / 2,
               (sp[0]["rect"][2] + sp[0]["rect"][3]) / 2, 0.0, why="the long bench under the bench roof")
    c.free("agari", "jp_f_hibachi_box", 3.80, 2.10, 0.0, why="a box brazier")
    c.free("agari", "jp_f_tabakobon", 0.30, 2.10, 15.0, why="a tobacco tray")
    c.free("agari", "jp_f_meal_left_two", 1.60, 1.80, 10.0, why="two trays left")
    c.free("agari", "jp_f_enza", 2.60, 1.90, 0.0, why="a straw cushion")
    c.free("agari", "jp_f_tableware_scattered", 3.20, 0.60, 30.0, why="bowls scattered")
    c.free("zashiki", "jp_f_byobu_makura", 3.90, -2.20, 0.0, why="a low screen")
    c.free("zashiki", "jp_f_hibachi_round", 1.40, -1.30, 0.0, why="a round brazier")
    c.free("zashiki", "jp_f_meal_left_zen", 2.40, -1.00, 10.0, why="a tray meal left")
    c.free("zashiki", "jp_f_enza", 0.60, -1.80, 0.0, why="a cushion")
    wallp(c, "zashiki", "xmax", -1.20, "jp_f_tansu_single", why="a low chest")
    c.free("zashiki", "jp_f_andon_ariake", 3.30, -2.20, 0.0, why="a night lamp, unlit")


def smithy(c):
    f = fit1(c, "doma", "forge")
    c.free("doma", "jp_f_forge", f["centre"][0] + 0.18, f["centre"][1], 0.0, why="the cold forge hearth")
    b = fit1(c, "doma", "bellows")
    c.free("doma", "jp_f_fuigo", b["centre"][0] - 0.02, b["centre"][1], 0.0, why="the box bellows beside the forge")
    a = fit1(c, "doma", "anvil")
    c.free("doma", "jp_f_anvil", a["centre"][0] + 0.05, a["centre"][1] + 0.10, 0.0, why="the anvil in its stump")
    q = fit1(c, "doma", "quench_tub")
    c.free("doma", "jp_f_oke_tarai_dry", q["centre"][0] + 0.25, q["centre"][1] + 0.05, 0.0, why="the quench tub, dry")
    c.free("doma", "jp_f_charcoal_bale", 0.50, -1.40, 90.0, why="a bale of pine charcoal (the bin spot is the back "
           "door's approach)")
    t = fit1(c, "doma", "tool_wall")
    onw(c, "doma", "zmax", (t["rect"][0] + t["rect"][1]) / 2, "jp_f_tongs_wall_taken", why="tongs and finished tools, "
             "half taken")
    c.free("doma", "jp_f_rack_half", 2.35, 0.85, 270.0, why="a rack of hoe blanks and scrap")
    c.site("jp_s_charcoal_bales_stack", 1.50, -2.40, 180.0, why="charcoal bales against the back wall outside")


def swordsmith(c):
    f = fit1(c, "forge", "forge")
    c.free("forge", "jp_f_forge_l", f["centre"][0], f["centre"][1], 0.0, why="the forge hearth")
    b = fit1(c, "forge", "bellows")
    c.free("forge", "jp_f_fuigo_l", b["centre"][0] - 0.38, b["centre"][1], 0.0, why="the big box bellows")
    c.free("forge", "jp_f_anvil_l", -2.30, -2.10, 0.0, why="the anvil (its W2C spot is the partition door's "
           "landing)")
    q = fit1(c, "forge", "quench_trough")
    c.free("forge", "jp_f_mizubune", q["centre"][0], q["centre"][1], 0.0, why="the long quench trough, dry")
    c.free("forge", "jp_f_charcoal_bale", 3.00, -2.25, 90.0, why="pine charcoal")
    s = fit1(c, "forge", "shimenawa")
    c.hang("forge", "jp_f_shimenawa_hang", s["centre"][0], s["centre"][1], s["y"], over="hearth",
           why="the sacred rope over the forge")
    onw(c, "forge", "zmin", -2.40, "jp_f_kamidana_plain", why="the god shelf of the forge, undisturbed")
    # work room
    ct = fit1(c, "work", "clay_trough")
    c.free("work", "jp_f_tsuchioki", ct["centre"][0], ct["centre"][1], 0.0, why="the clay-coating trough")
    br = fit1(c, "work", "blade_rack")
    onw(c, "work", "zmin", (br["rect"][0] + br["rect"][1]) / 2, "jp_f_blade_rack", why="bare blades on the rack")
    c.free("work", "jp_f_zukue_plain", -1.10, 0.55, 0.0, why="the work bench")
    c.free("work", "jp_f_box_m", 1.20, 1.90, 20.0, why="a box of fittings")
    c.free("work", "jp_f_oke_bucket", -2.90, 2.10, 0.0, why="a bucket")
    c.free("work", "jp_f_rack_half", 3.10, 1.90, 270.0, why="a rack of tools")


def guardhut_m(c):
    """Jishin-ban (self-watch post): capture tools and fire gear in the doma, the brazier and the sundries counter on
    the platform; the fire ladder on the ridge, the ward lantern by the door."""
    tr = fit1(c, "doma", "tool_rack")
    onw(c, "doma", "xmin", (tr["rect"][2] + tr["rect"][3]) / 2, "jp_f_mitsudogu", why="the three capture tools")
    wallp(c, "doma", "zmin", -0.90, "jp_f_tana_091_1", why="a shelf")
    c.free("doma", "jp_f_oke_bucket", -1.35, 0.85, 0.0, why="a fire bucket")
    c.free("doma", "jp_f_mizugame", -0.45, -0.95, 0.0, why="the water jar")
    c.free("doma", "jp_f_debris_leaves", -0.90, 0.40, 20.0, why="leaves blown in")
    c.free("doma", "jp_f_chochin_fallen", -1.20, -0.10, 40.0, why="the round lantern dropped")
    br = fit1(c, "floor", "brazier")
    h = c.free("floor", "jp_f_hibachi_box", br["centre"][0], br["centre"][1], 0.0, why="the night watch's brazier")
    c.surf(h, "jp_f_tea_dobin", why="the clay kettle on it")
    co = fit1(c, "floor", "counter")
    d = wallp(c, "floor", "xmax", (co["rect"][2] + co["rect"][3]) / 2, "jp_f_zukue_plain", why="the sundries counter")
    c.surf(d, "jp_f_sg_candles", why="candles left for sale")
    c.free("floor", "jp_f_enza", 0.70, 0.75, 0.0, why="a straw cushion")
    c.free("floor", "jp_f_tabakobon", 0.75, -0.40, 15.0, why="a tobacco tray")
    c.free("floor", "jp_f_andon_kaku", 0.45, 1.00, 0.0, why="the watch lamp, unlit")
    onw(c, "floor", "zmin", 1.10, "jp_f_fire_gear", why="fire hook and buckets")
    lf = fit1(c, "doma", "lantern_post")
    c.site("jp_s_lantern_sign_tsuji", lf["centre"][0] - 0.10, lf["centre"][1] + 0.30, 0.0, why="the ward lantern")
    fl = fit1(c, "doma", "fire_ladder")
    c.front("jp_f_ridge_ladder", (fl["rect"][0] + fl["rect"][1]) / 2, (fl["rect"][2] + fl["rect"][3]) / 2, fl["y"],
            why="the fire ladder with its alarm bell on the ridge (Kyoho)")


def kido_bantaya(c):
    f = fit1(c, "gate", "lantern")
    c.hang("gate", "jp_f_chochin_shop", f["centre"][0], f["centre"][1], 2.40, over="gate passage (visual)",
           why="the ward lantern under the tie beam")
    sparse(c, "gate", "the gate passage")
    lp = fit1(c, "gate", "lantern_post")
    c.site("jp_s_lantern_sign_tsuji", 3.30, -2.40, 90.0, why="the ward lantern beside the keeper's hut")
    tr = fit1(c, "hut_doma", "tool_rack")
    onw(c, "hut_doma", "zmin", (tr["rect"][0] + tr["rect"][1]) / 2, "jp_f_mitsudogu_taken", why="the capture tools, "
             "one gone")
    wallp(c, "hut_doma", "xmax", -3.70, "jp_f_tana_091_1", why="a shelf")
    c.free("hut_doma", "jp_f_oke_bucket", 5.40, -4.10, 0.0, why="a bucket")
    c.free("hut_doma", "jp_f_debris_leaves", 5.00, -3.70, 30.0, why="leaves")
    c.free("hut_doma", "jp_f_debris_straw", 5.40, -3.30, 60.0, why="straw")
    c.free("hut_doma", "jp_f_chochin_fallen", 4.55, -3.90, 120.0, why="a dropped lantern")
    br = fit1(c, "hut_floor", "brazier")
    c.free("hut_floor", "jp_f_hibachi_box", br["centre"][0], br["centre"][1], 90.0, why="the brazier")
    co = fit1(c, "hut_floor", "counter")
    c.free("hut_floor", "jp_f_sg_candles", (co["rect"][0] + co["rect"][1]) / 2 - 0.35, (co["rect"][2] + co["rect"][3]) / 2,
           0.0, why="candles and sundries for sale on the counter boards")
    c.free("hut_floor", "jp_f_enza", 4.55, -2.25, 0.0, why="the keeper's cushion")
    sparse(c, "hut_floor", "the 0.8 m sitting platform under the counter shutter")


SETS_W2F = {
    "w2f_haiden_town": {"tier": 3, "fn": shrine_haiden_town},
    "w2f_haiden_village": {"tier": 2, "fn": shrine_haiden_village},
    "w2f_honden_town": {"tier": 3, "fn": shrine_honden_town},
    "w2f_honden_village": {"tier": 2, "fn": shrine_honden_village},
    "w2f_temizuya": {"tier": 3, "fn": shrine_temizuya},
    "w2f_shamusho": {"tier": 3, "fn": shrine_shamusho},
    "w2f_kagura": {"tier": 3, "fn": shrine_kagura},
    "w2f_hondo_village": {"tier": 2, "fn": temple_hondo_village},
    "w2f_hondo_town": {"tier": 3, "fn": temple_hondo_town},
    "w2f_do_jizo": {"tier": 2, "fn": temple_do_jizo},
    "w2f_do_kannon": {"tier": 2, "fn": temple_do_kannon},
    "w2f_kuri_village": {"tier": 2, "fn": temple_kuri_village},
    "w2f_kuri_town": {"tier": 3, "fn": temple_kuri_town},
    "w2f_shoro": {"tier": 2, "fn": temple_shoro},
    "w2f_gate": {"tier": 2, "fn": temple_gate},
    "w2f_teahouse_bench": {"tier": 2, "fn": teahouse_bench},
    "w2f_teahouse_shop": {"tier": 2, "fn": teahouse_shop},
    "w2f_teahouse_tateba": {"tier": 2, "fn": teahouse_tateba},
    "w2f_smithy": {"tier": 2, "fn": smithy},
    "w2f_swordsmith": {"tier": 3, "fn": swordsmith},
    "w2f_guardhut_m": {"tier": 2, "fn": guardhut_m},
    "w2f_kido_bantaya": {"tier": 3, "fn": kido_bantaya},
}


def sets():
    return dict(SETS_W2F)
