"""The KEEP_TRADES shop dressing sets (agent S1, 2026-09-30): research/interior/SHOP_SETS.md as code.

A trade = a declarative spec (TRADES[key]); apply_mise(c, key, ab) furnishes the shop room (mise) of ANY townhouse
unit through a furnishkit Ctx from the room's own geometry (rect, the toriniwa side, the shell's doors), so the same
set fits a 2, 3 or 4-ken unit, Kamigata or Edo, toriniwa left or right. dress(key, ab, kind) returns a whole-house
dressing for furnish_sets.SETS (the mise set + the toriniwa / oku / kitchen of the C3 townhouse kit for that shell
kind + the front signs and street objects).

The slots of the mise (model frame, street = +z; SHOP_SETS.md section 1):
  strip    pieces laid along the street edge (on the board strip when the shell has one: shell option mise_floor),
           from the party side to the toriniwa side: 'stand' = jp_f_misedana (1 ken, or half where 1 ken does not fit)
           with the trade's three goods clusters on its steps; or the trade's floor display (casks, bales, tubs)
  stock    the party wall, street end: the trade's stock furniture (shelf, drawer cabinet, bolt shelf, rack)
  choba    the party wall, back end: the account desk (ledgers, abacus, writing box on it), the coin box beside it,
           the clerk's cushion
  corner   the toriniwa-side wall, street end (between the toriniwa door's zone and the strip): one small piece
  floor    flat counted pieces (cushions, swept goods) in the free middle front
  wall     the trade's wall piece on the toriniwa-side wall (street end) or the back partition; kamidana high on the
           back partition (undisturbed); calendar over the desk
  beam     hung from the loft joists (3.00) over the strip
  front    facade proxies (noren on the entrance, kanban / shape sign / sugidama at the shop end); street objects
Abandoned level ab (G1 A2 "moderate as left"): 0 = as shut, 1 = one or two signs (the top step swept, the coin box
forced, the ledgers on the floor), 2 = the heavier room (stand toppled with its goods on the floor, stock in its
abandoned state, kanban askew, the beam goods rotted). Each intact prop's abandoned twin is read from its sidecar.
"""
import glob
import json
import os

from jpparts import decor as DC, mlod, checks as C

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
LOFT_CEIL = 3.00          # townhouse loft underside (templates/townhouse.py CEIL)
FACADE_Z = {"sign": 4.05, "noren": 3.96}     # C3's front proxy planes on the townhouse units
STREET_Z = 4.62           # street objects in front of the shop (benches, tubs), clear of the gutter line (5.10)
COVER_MAX = 0.22          # stay under decor D2's 25 % (footprint estimates from the sidecars)
TRADES = {}
_AB = None


# ------------------------------------------------------------------------------------------------ abandoned twins
def ab_of(name):
    """The abandoned twin of an intact catalogue model: same prop, same variant, same mount, the first non-intact
    state; None when the prop has none for that variant."""
    global _AB
    if _AB is None:
        _AB = {}
        for p in glob.glob(os.path.join(DEV, "src", "JP", "*", "*", "*.prop.json")):
            with open(p, "rb") as f:
                d = json.loads(f.read().decode("utf-8"))
            ms = d.get("models", [])
            for m in ms:
                if m.get("state") != "intact":
                    continue
                nm = os.path.basename(m["p3d"])[:-4]
                tw = [q for q in ms if q.get("state") != "intact" and q.get("variant") == m.get("variant")
                      and q.get("mount", m.get("mount")) == m.get("mount")]
                if tw:
                    _AB[nm] = os.path.basename(tw[0]["p3d"])[:-4]
    return _AB.get(name)


def pick(name, ab, level=1):
    """name at ab < level, its abandoned twin at ab >= level (when it has one)."""
    if name and ab >= level:
        return ab_of(name) or name
    return name


def trade(key, title, **kw):
    """Register a trade spec. Fields (all optional except title):
      steps   (front, middle, back) goods for the stand's three steps (intact names; ab picks the twins)
      strip   pieces along the strip, party side first: 'stand' or a catalogue name (yaw 0 = front to the street)
      stock   the party-wall stock piece; stock_top: small items on its first loot surface
      choba   True (desk + coin box + cushion) | 'desk' (desk only) | False
      corner  one small piece at the toriniwa-side street corner; floor: flat counted pieces
      wall    the trade's wall piece (toriniwa-side wall, street end, or the back partition); wall_on 'tori' | 'back'
      beam    pieces hung from the loft joists over the strip
      front   facade proxies at the shop end (kanban, shape sign); door: proxies at the entrance (noren, sugidama)
      street  street objects (catalogue names) in front of the shop
      tori    two extra counted toriniwa pieces (the C3 kit gives three)
      kura    True: the trade wants a kura behind (pawnbroker, moneychanger): a placement note for the map
      era / note  the verdict and its source (SHOP_SETS.md)"""
    TRADES[key] = dict(key=key, title=title, **kw)
    return TRADES[key]


# ------------------------------------------------------------------------------------------------ mise geometry
def _gcomps(c):
    if not hasattr(c, "_s1_gcomps"):
        L = {mlod.lod_name(l.resolution): l for l in c.M.lods()}
        c._s1_gcomps = C.components(L["Geometry"])
    return c._s1_gcomps


def _opening(c, dn):
    k = int(dn.replace("DoorsTwin", "")) - 1
    return DC.door_opening(c.M.doors[k], _gcomps(c))


def mise_geo(c):
    x0, x1, z0, z1 = c.R("mise")
    tx0, tx1, _, _ = c.R("toriniwa")
    tori = "xmax" if tx0 >= x1 - 0.30 else "xmin"
    party = "xmin" if tori == "xmax" else "xmax"
    s = 1.0 if party == "xmin" else -1.0
    g = {"rect": (x0, x1, z0, z1), "tori": tori, "party": party, "s": s, "px": x0 if s > 0 else x1,
         "tx": x1 if s > 0 else x0, "back": None, "tori_door": None, "entrance": None}
    for dn in c.room["mise"].get("doors", []):
        o = _opening(c, dn)
        if not o:
            continue
        along_x, (lo, hi), wall = o
        if along_x and abs(wall - z0) < 0.4:
            g["back"] = (lo, hi)
        elif not along_x:
            g["tori_door"] = (lo, hi)
    for dn in c.room["toriniwa"].get("doors", []):
        o = _opening(c, dn)
        if o and o[0] and o[2] > z1:
            g["entrance"] = ((o[1][0] + o[1][1]) / 2, o[2])
    return g


def _cat(name):
    return DC.catalog()[name]


def _fp_area(name):
    inf = _cat(name)
    if not inf["geo"]:
        return 0.0
    if inf["roadway"] and inf["bbox"][3] <= DC.WALK_ON_H:
        return 0.0
    fp = inf["footprint"] or [inf["bbox"][0], inf["bbox"][4], inf["bbox"][1], inf["bbox"][5]]
    return (fp[2] - fp[0]) * (fp[3] - fp[1])


# ------------------------------------------------------------------------------------------------ the mise set
def _flat(name):
    return not _cat(name)["geo"]


def _fits_box(name, wmax, dmax):
    bb = _cat(name)["bbox"]
    return bb[1] - bb[0] <= wmax and bb[5] - bb[4] <= dmax


def apply_mise(c, key, ab=1, tier=3):
    """Furnish the mise of townhouse ctx c with trade `key` at abandoned level ab. Returns the placed items by slot.
    Keeps decor's rules as it goes: collision cover under COVER_MAX of the room, 5-7 counted props (the optional
    corner and floor pieces are dropped first), the toriniwa door's zone and the room centre free."""
    T = TRADES[key]
    g = mise_geo(c)
    x0, x1, z0, z1 = g["rect"]
    s, px, tx, party, tori = g["s"], g["px"], g["tx"], g["party"], g["tori"]
    area = (x1 - x0) * (z1 - z0)
    wide = (x1 - x0) >= 2.5                    # a 3-ken (or wider) shop room; a 2-ken one gets no corner piece
    budget = COVER_MAX * area
    used = [0.0]
    n = [0]
    out = {}
    yaw_in = 90.0 if s > 0 else 270.0         # facing into the room from the party wall

    def fits(name):
        return used[0] + _fp_area(name) <= budget + 1e-9

    def take(name, counted=True):
        used[0] += _fp_area(name)
        n[0] += 1 if counted else 0

    def on_top(host, item, why):
        """A small item on the host's first loot surface, pushed to the surface's end so its loot point stays free."""
        ls = _cat(host["name"])["loot"]
        if not ls:
            return
        r = ls[0]["rect"]
        bb = _cat(item)["bbox"]
        hw = (bb[1] - bb[0]) / 2
        dx = max(0.0, (r[2] - r[0]) / 2 - hw - 0.02)
        c.surf(host, item, dx=dx, why=why)

    # ---- choba (desk + coin box + cushion): the party wall, back end
    choba = T.get("choba", True)
    if choba:
        desk = c.wall("mise", party, z0 + 0.50, "jp_f_zukue_choba", why="the account desk (choba) against the party "
                                                                          "wall")
        take("jp_f_zukue_choba")
        out["desk"] = desk
        c.surf(desk, "jp_f_choba_set_desk" if ab < 1 else "jp_f_writing_box_open",
               why="ledgers, abacus and writing box on the desk" if ab < 1 else "the writing box left open")
        if choba is True:
            zn = "jp_f_choba_set_zenibako_open" if ab >= 1 else "jp_f_choba_set_zenibako"
            c.free("mise", zn, px + s * 0.25, z0 + 1.20, yaw_in, why="the coin box beside the desk" +
                   (" (forced open, empty)" if ab >= 1 else ""))
            take(zn)
        if ab >= 1:
            c.free("mise", "jp_f_choba_set_scattered", px + s * 1.05, z0 + 1.15, 25.0, count=False,
                   why="ledgers splayed on the mats, the abacus upturned (disorder)")
    # ---- stock: the party wall, street end
    st = T.get("stock")
    if st:
        sn = pick(st, ab, 2)
        L = _cat(sn)["bbox"][1] - _cat(sn)["bbox"][0]
        if fits(sn) and L <= (z1 - z0) - 1.45:
            stock = c.wall("mise", party, z1 - 0.03 - L / 2, sn, why="the trade's stock against the party wall")
            take(sn)
            out["stock"] = stock
            for it in T.get("stock_top", [])[:1]:
                on_top(stock, it, "on the stock piece")
    # ---- strip: along the street edge, party side first
    sdepth = 0.0
    if "stock" in out:
        bb = _cat(out["stock"]["name"])["bbox"]
        sdepth = bb[5] - min(0.0, bb[4])
    xa = px + s * (sdepth + 0.08)
    xb = tx - s * 0.08
    room = abs(xb - xa)
    cur = xa
    steps = list(T.get("steps", ()))
    strip_items = []
    for tok in T.get("strip", ["stand"]):
        cand = ["jp_f_misedana_1ken", "jp_f_misedana_half"] if tok == "stand" else [tok]
        for nm in cand:
            nm2 = pick(nm, ab, 2)
            bb = _cat(nm2)["bbox"]
            w = bb[1] - bb[0]
            if abs(cur - xa) + w <= room + 1e-6 and fits(nm2) and n[0] < 7 and bb[5] - bb[4] <= 0.80:
                xc = cur + s * (-bb[0] if s > 0 else bb[1])
                zc = z1 - 0.01 - bb[5]
                it = c.free("mise", nm2, xc, zc, 0.0, why="on the display strip, facing the street")
                take(nm2)
                strip_items.append((nm, it))
                cur += s * (w + 0.06)
                break
    out["strip"] = strip_items
    # ---- goods on the stand steps (or, toppled, on the floor in front of it)
    for nm, it in strip_items:
        if not nm.startswith("jp_f_misedana") or not steps:
            continue
        half = nm.endswith("_half")
        if it["name"] == nm:                                         # the stand stands
            for k, gname in enumerate(steps[:3]):
                gn = (ab_of(gname) or gname) if (ab >= 1 and k == 2) else gname
                c.surf(it, gn, surface="step_%d" % (k + 1), dx=0.24 if half else 0.0,
                       why="goods on step %d" % (k + 1))
        else:                                                        # toppled: the goods lie on the floor behind it
            for k, gname in enumerate(steps[:2]):
                gn = ab_of(gname) or gname
                c.free("mise", gn, it["x"] + s * (k - 0.5) * 0.5, it["z"] - 0.70, 15.0 * (k + 1), count=False,
                       why="goods swept off the toppled stand")
        break
    # ---- corner (toriniwa-side wall, street end): 3-ken and wider rooms only
    cn = T.get("corner")
    if cn and wide and n[0] < 7:
        cn2 = pick(cn, ab, 2)
        bb = _cat(cn2)["bbox"]
        zc = z1 - 0.64 - bb[5] - 0.02
        lo_ok = g["tori_door"] is None or zc + bb[4] > g["tori_door"][1] + 0.42
        if lo_ok and fits(cn2) and _fits_box(cn2, 0.65, 0.45):
            c.free("mise", cn2, tx - s * ((bb[1] - bb[0]) / 2 + 0.06), zc, 0.0, why="small stock in the corner")
            take(cn2)
    # ---- flat counted pieces in the free middle front (no collision: the band and the centre stay free)
    for k, fn in enumerate(T.get("floor", [])):
        fn2 = pick(fn, ab, 1)
        if not _flat(fn2) or n[0] >= 7 or (not wide and k > 0):
            continue
        c.free("mise", fn2, (x0 + x1) / 2 + s * (0.35 - 0.5 * k), z1 - 0.95 - 0.1 * k, 20.0 + 35 * k,
               why="laid out on the mats")
        n[0] += 1
    cush = "jp_f_enza_zabuton" if tier >= 3 else "jp_f_enza"
    if choba:
        cc = n[0] < 5
        c.free("mise", cush, px + s * 0.78, z0 + 0.50, 8.0, count=cc, why="the clerk's cushion in front of the desk")
        n[0] += 1 if cc else 0
    while n[0] < 5:                                                  # a thin room: more flat dressing to count
        c.free("mise", "jp_f_debris_paper", (x0 + x1) / 2, (z0 + z1) / 2 + 0.2 * n[0], 30.0 * n[0],
               why="paper litter (disorder)")
        n[0] += 1
    # ---- wall pieces
    xk = px + s * 0.45
    c.onwall("mise", "zmin", xk, "jp_f_kamidana_plain", why="god shelf high on the back partition, undisturbed")
    if choba:
        c.onwall("mise", party, z0 + 0.50, "jp_f_koyomi" if ab < 1 else "jp_f_koyomi_curled",
                 why="the calendar over the desk")
    wn = T.get("wall")
    if wn:
        wn2 = pick(wn, ab, 2)
        bb = _cat(wn2)["bbox"]
        w = bb[1] - bb[0]
        lo = (g["tori_door"][1] + 0.08) if g["tori_door"] else z0 + 0.3
        if T.get("wall_on", "tori") == "tori" and z1 - 0.05 - lo >= w:
            c.onwall("mise", tori, (lo + z1 - 0.05) / 2, wn2, why="the trade's wall piece")
        else:
            bl = g["back"]
            if bl:                       # the back partition between the mise <-> oku door and the toriniwa wall
                seg = (bl[1] + 0.05, max(x0, x1) - 0.05) if s > 0 else (min(x0, x1) + 0.05, bl[0] - 0.05)
            else:
                seg = (x0 + 0.9, x1 - 0.05) if s > 0 else (x0 + 0.05, x1 - 0.9)
            if seg[1] - seg[0] >= w:
                c.onwall("mise", "zmin", (seg[0] + seg[1]) / 2, wn2, why="the trade's wall piece on the back "
                                                                         "partition")
    # ---- beam
    for k, bn in enumerate(T.get("beam", [])):
        bn2 = pick(bn, ab, 2)
        if _cat(bn2)["mount"] != "beam":
            bn2 = bn
        if strip_items:
            it = strip_items[0][1]
            c.hang("mise", bn2, it["x"] + s * (0.45 * k - 0.25), z1 - 0.40, LOFT_CEIL, over="furniture",
                   why="hung from the loft joists over the strip")
    out["count"] = n[0]
    return out


def front(c, key, ab=1):
    """The trade's facade proxies and street objects (the shop end = the party side of the mise)."""
    T = TRADES[key]
    g = mise_geo(c)
    x0, x1, z0, z1 = g["rect"]
    s, px = g["s"], g["px"]
    for k, fn in enumerate(T.get("front", [])):
        fn2 = pick(fn, ab, 2)
        c.front(fn2, px + s * (0.45 + 0.75 * k), FACADE_Z["sign"], 0.0, why="the trade's sign at the shop end")
    if g["entrance"]:
        ex = g["entrance"][0]
        for k, dn in enumerate(T.get("door", ["jp_s_shopfront_noren_long"])):
            dn2 = pick(dn, ab, 2)
            zz = FACADE_Z["noren"] if "noren" in dn else FACADE_Z["sign"]
            yy = 0.10 if dn == "jp_s_shopfront_noren_long" else 0.0
            c.front(dn2, ex + (0.0 if k == 0 else -s * 0.95), zz, yy, why="at the entrance")
    for k, sn in enumerate(T.get("street", [])):
        sn2 = pick(sn, ab, 2)
        if _cat(sn2)["bbox"][5] - _cat(sn2)["bbox"][4] > _cat(sn)["bbox"][5] - _cat(sn)["bbox"][4] + 0.02:
            sn2 = sn                             # a sprawled abandoned twin would reach the gutter line
        c.site(sn2, (x0 + x1) / 2 + s * 0.6 * (k - 0.5), STREET_Z, 0.0, why="in front of the shop")


# ------------------------------------------------------------------------------------------------ whole houses
def _oku_3k(c, ab):
    """The oku of a 3-ken ToriL unit (x -2.67..0.85, z -1.76..0.85): C3's T3 back room (the same at every ab level;
    the heavier state drops a robe on the mats)."""
    c.wall("oku", "zmin", -1.20, "jp_f_futon_laid", why="bedding laid out along the back wall")
    ts = c.wall("oku", "xmin", -0.30, "jp_f_tansu", why="clothing chest against the party wall")
    c.free("oku", "jp_f_andon_kaku", -2.45, -1.50, 0, why="standing lamp, unlit")
    c.free("oku", "jp_f_hibachi_round", -0.95, 0.10, 0, why="round brazier")
    c.wall("oku", "xmin", 0.52, "jp_f_butsudan_lacquer", why="lacquered Buddhist altar, undisturbed")
    c.free("oku", "jp_f_enza_zabuton", -0.95, -0.40, 12, why="a cotton cushion (T3)")
    c.surf(ts, "jp_f_tea_dobin", why="clay tea pot on the chest (T3 marker)")
    if ab >= 2:
        c.free("oku", "jp_f_clothes_kimono", -0.25, 0.15, 40, count=False, why="a kimono pulled out and dropped")
    c.hang("oku", "jp_f_kaya_bundle", -2.30, -1.35, LOFT_CEIL, over="corner", why="the mosquito net folded away")


def _oku_2k(c, ab):
    """The oku of a 2-ken ToriR unit (x 0.06..1.76, z -1.76..0.85): C3's T3 back room."""
    c.wall("oku", "xmax", -0.80, "jp_f_futon_laid", why="bedding laid out along the party wall")
    ts = c.wall("oku", "zmax", 0.62, "jp_f_tansu_single", why="a low chest against the shop partition")
    c.free("oku", "jp_f_andon_ariake", 0.35, 0.10, 0, why="night lamp by the chest, unlit")
    c.free("oku", "jp_f_mirror_stand_open", 0.45, -0.70, 30, why="mirror stand, its cover off")
    c.free("oku", "jp_f_enza_zabuton_folded", 0.35, -1.30, 0, why="a folded cushion (T3)")
    c.surf(ts, "jp_f_sewing_box", why="the sewing box on the chest")
    c.hang("oku", "jp_f_kaya_bundle", 1.45, -1.45, LOFT_CEIL, over="furniture", why="the mosquito net folded away")


def _house(c, key, ab, kind):
    import furnish_sets as FS
    T = TRADES[key]
    tori = T.get("tori", ())
    if kind == "3k":
        FS._tori_3k(c)
        spots = ((2.40, 2.55, 15.0, 0.42, 0.42), (2.45, -1.25, 0.0, 0.48, 0.48))
        defaults = ("jp_f_oke_bucket", "jp_f_basket_back")
    else:
        FS._tori_2k(c)
        spots = ((-1.10, -0.50, 40.0, 0.0, 0.0), (-1.52, -1.30, 0.0, 0.30, 0.30))
        defaults = ("jp_f_debris_straw", "jp_f_jar_m")
    for k, (x, z, yaw, wmax, dmax) in enumerate(spots):
        nm = pick(tori[k] if k < len(tori) else defaults[k], ab, 2)
        if (wmax == 0.0 and not _flat(nm)) or (wmax > 0.0 and not _fits_box(nm, wmax, dmax)):
            nm = defaults[k]                     # the toriniwa passage keeps its 1.00 m band: small pieces only
        c.free("toriniwa", nm, x, z, yaw, why="in the toriniwa (the trade's overflow)")
    apply_mise(c, key, ab, tier=3)
    if kind == "3k":
        _oku_3k(c, ab)
        FS._kitchen_3k(c)
    else:
        _oku_2k(c, ab)
        FS._kitchen_2k(c)
    front(c, key, ab)
    g = mise_geo(c)
    if g["entrance"]:
        c.site("jp_s_gutter_slab", g["entrance"][0], 5.10, 0, why="stone slab over the gutter at the door")
    x0, x1, _, _ = g["rect"]
    n = int((x1 - x0 + 0.05) // 1.82)                     # 1-ken gutter boards along the shop front
    xs = [(x0 + x1) / 2 + 1.82 * (k - (n - 1) / 2) for k in range(n)]
    FS._gutters(c, [x for x in xs if not g["entrance"] or abs(x - g["entrance"][0]) > 1.30], 5.10)


def dress(key, ab=1, kind="3k"):
    """A furnish_sets dressing function for trade `key` on a 3-ken ToriL ('3k') or 2-ken ToriR ('2k') unit."""
    def fn(c):
        _house(c, key, ab, kind)
    fn.__name__ = "shop_%s_ab%d_%s" % (key, ab, kind)
    fn.__doc__ = "%s (S1 shop set, ab %d, %s unit)" % (TRADES[key]["title"], ab, kind)
    return fn


def sets():
    """furnish_sets.SETS entries: shop_<trade>_<kind>_ab<level> for every trade, both shell kinds, ab 0-2. Each asks
    the shell for the board display strip (townhouse option mise_floor '_455')."""
    out = {}
    for key in TRADES:
        for kind in ("3k", "2k"):
            for ab in (0, 1, 2):
                out["shop_%s_%s_ab%d" % (key, kind, ab)] = {"tier": 3, "fn": dress(key, ab, kind),
                                                           "shell": {"mise_floor": "_455"}}
    return out


# ================================================================================================ the trades
# Everyday shops 1-5 (S1 group 1)
trade("aramono", "General household goods (ara-mono-ya)",
      steps=("jp_f_sg_aramono", "jp_f_sg_aramono", "jp_f_sg_lacquer"), strip=["stand", "jp_f_oke_tarai"],
      stock="jp_f_rack_half", corner="jp_f_basket_kago", floor=["jp_f_mushiro"],
      wall="jp_f_basket_zaru_wall", beam=["jp_f_sandals_hung_beam"], front=["jp_f_kanban_aramono"],
      tori=("jp_f_oke_bucket", "jp_f_mushiro_rolled"), era="KEPT: BTI 912-913")
trade("draper", "Draper (gofuku / futomono-dana)",
      steps=("jp_f_sg_bolts", "jp_f_sg_bolts", "jp_f_sg_bolts"), strip=["stand", "jp_f_box_s_lacquer"],
      stock="jp_f_bolt_shelf", floor=["jp_f_sg_bolts"],
      front=["jp_f_kanban_gofuku"], door=["jp_s_shopfront_noren_long"], tori=("jp_f_oke_bucket", "jp_f_box_m"),
      era="KEPT: BTI 919-923 (Echigoya 1683)")
trade("furugi", "Old clothes (furugi-ya)",
      steps=("jp_f_sg_folded", "jp_f_sg_folded", "jp_f_sg_folded"), strip=["stand", "jp_f_kori"],
      stock="jp_f_furugi_rack", floor=["jp_f_sg_folded"], front=["jp_f_kanban_furugi"],
      tori=("jp_f_kori_2", "jp_f_basket_back"), era="KEPT: BTI 924-925")
trade("kanamono", "Ironmonger (kanamono-ya)",
      steps=("jp_f_sg_ironware", "jp_f_sg_ironware", "jp_f_sg_ironware"), strip=["stand", "jp_f_kama_nabe"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_choba_set_tenbin"], wall="jp_f_kanamono_wall",
      front=["jp_f_kanban_kanamono"], tori=("jp_f_oke_bucket", "jp_f_box_m"), era="KEPT: BTI 914-915")
trade("setomono", "Ceramics and lacquerware (setomono-ya / nurimono-ya)",
      steps=("jp_f_sg_porcelain", "jp_f_sg_lacquer", "jp_f_sg_porcelain"), strip=["stand", "jp_f_ware_crate"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_jar_s_pale"], corner="jp_f_jar_m_pale",
      front=["jp_f_kanban_setomono", "jp_f_kanban_nurimono"], tori=("jp_f_ware_crate", "jp_f_debris_straw"),
      era="KEPT: BTI 916-918; no Banko ware (KEEP cut)")

# Everyday shops 6-10 (S1 group 2)
trade("kamiya", "Paper and brushes (kami-ya / fude-sumi-ya)",
      steps=("jp_f_sg_brushes", "jp_f_writing_box", "jp_f_sg_brushes"),
      strip=["stand", "jp_f_goods_general_paper"], stock="jp_f_tana_091_3", stock_top=["jp_f_writing_box"],
      corner="jp_f_box_s", front=["jp_f_kanban_hitsuboku", "jp_s_shopfront_shape_brush"],
      tori=("jp_f_box_m", "jp_f_debris_paper"), era="KEPT: BTI 928-929")
trade("abura", "Oil and candles (abura-ya / rousoku-ya)",
      steps=("jp_f_sg_oil", "jp_f_sg_candles", "jp_f_sg_oil"), strip=["stand", "jp_f_taru_cask"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_masu_set"], corner="jp_f_jar_m",
      front=["jp_f_kanban_abura", "jp_f_kanban_rousoku"], tori=("jp_f_taru_komo", "jp_f_jar_l"),
      era="KEPT: BTI 930-933, 540-542")
trade("sumiya", "Charcoal and firewood (sumi-ya / takigi-ya)",
      strip=["jp_f_charcoal_bale", "jp_f_charcoal_bale", "jp_f_charcoal_bale"],
      stock="jp_f_firewood_stack",
      corner="jp_f_box_m", floor=["jp_f_mi_furui", "jp_f_charcoal_scuttle"], front=["jp_f_kanban_sumimaki"],
      tori=("jp_f_charcoal_bale", "jp_f_firewood_bundle"), era="KEPT: BTI 934-935")
trade("tabako", "Tobacco (tabako-ya)",
      steps=("jp_f_sg_tobacco", "jp_f_sg_tobacco", "jp_f_sg_tobacco"), strip=["stand", "jp_f_tobacco_cutter"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_tabakobon"], corner="jp_f_box_m",
      front=["jp_f_kanban_tabako", "jp_f_kanban_shape_pipe"], tori=("jp_f_tawara", "jp_f_box_s"),
      era="KEPT: BTI 936-937, 487")
trade("tabidogu", "Travel goods and souvenirs (tabi-dogu-ya / meibutsu-ya)",
      steps=("jp_f_sg_travel", "jp_f_sg_odawara", "jp_f_sg_travel"), strip=["stand", "jp_f_basket_back"],
      stock="jp_f_tana_091_3", wall="jp_f_print_line_otsue", beam=["jp_f_sandals_hung_beam"],
      front=["jp_f_kanban_tabidogu", "jp_f_kanban_otsue"], door=["jp_s_shopfront_noren_half"],
      street=["jp_s_sandals_sale_stand"], tori=("jp_f_basket_back", "jp_f_kori"),
      era="KEPT: BTI 942-946; Otsu-e (general); Odawara chochin date uncertain (BTI 497-499)")

# Rice, fish and greens, tofu, soba, sweets (S1 group 3)
trade("komeya", "Rice dealer (kome-ya)",
      strip=["jp_f_rice_bin", "jp_f_tawara", "jp_f_tawara_kamasu"], stock="jp_f_tawara_stack6",
      stock_top=["jp_f_masu_to"], corner="jp_f_tawara_kamasu", floor=["jp_f_masu_set"], front=["jp_f_kanban_kome"],
      tori=("jp_f_tawara_kamasu_stack3", "jp_f_mi"), era="KEPT: BTI 713-714")
trade("sakana", "Fishmonger (sakana-ya)",
      strip=["jp_f_fish_tub", "jp_f_fish_board", "jp_f_fish_tub"], stock="jp_f_tana_091_3",
      stock_top=["jp_f_basket_zaru"], choba="desk", beam=["jp_f_drying_fish"], front=["jp_f_kanban_sakana"],
      door=["jp_s_shopfront_noren_half"], street=["jp_s_oke_tarai"], tori=("jp_f_oke_tarai", "jp_f_basket_back"),
      era="KEPT: BTI 715-717 (most fish came by peddlers)")
trade("yaoya", "Greengrocer (yaoya / aomono-ya)",
      strip=["jp_f_veg_basket", "jp_f_veg_basket", "jp_f_basket_kago"], stock="jp_f_rack_half",
      stock_top=["jp_f_basket_zaru_stack"], choba="desk", beam=["jp_f_drying_daikon"], front=["jp_f_kanban_aomono"],
      street=["jp_s_tenbin_baskets"], tori=("jp_f_basket_back", "jp_f_basket_kago"), era="KEPT: BTI 724-725")
trade("tofu", "Tofu and wet food (tofu-ya)",
      strip=["jp_f_tofu_tank", "jp_f_tofu_press"], stock="jp_f_tana_091_3", stock_top=["jp_f_basket_zaru"],
      choba="desk", corner="jp_f_usu_ishiusu", front=["jp_f_kanban_tofu"], door=["jp_s_shopfront_noren_half"],
      tori=("jp_f_oke_bucket", "jp_f_oke_tarai"), era="KEPT: BTI 608-611")
trade("soba", "Soba and rice eatery (soba-ya / meshi-ya)",
      strip=["jp_f_soba_board", "jp_f_seiro_stack"], stock="jp_f_tana_091_3", stock_top=["jp_f_tableware_bowls"],
      choba="desk", floor=["jp_f_meal_left_zen", "jp_f_enza"], front=["jp_f_kanban_soba"],
      door=["jp_s_shopfront_noren_half"], street=["jp_s_bench_1ken"], tori=("jp_f_oke_bucket", "jp_f_taru_cask"),
      era="KEPT: BTI 650-656 (soba steamed in seiro)")
trade("mochiya", "Sweets and rice cakes (mochi-ya / dango-ya)",
      steps=("jp_f_sg_sweets", "jp_f_sg_sweets", "jp_f_sg_sweets"), strip=["stand", "jp_f_konro_grill"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_seiro_stack"], corner="jp_f_jar_s",
      front=["jp_f_kanban_mochi", "jp_f_kanban_okashi"], door=["jp_s_shopfront_noren_half"],
      street=["jp_s_bench_1ken"], tori=("jp_f_usu_mallet", "jp_f_oke_bucket"),
      era="KEPT: BTI 630-639 (sakura-mochi 1717)")

# Drink and services (S1 group 4)
trade("sakaya", "Sake shop (saka-ya)",
      strip=["jp_f_taru_rack3", "jp_f_taru_komo"], stock="jp_f_tana_091_3", stock_top=["jp_f_tokkuri_large"],
      corner="jp_f_taru_cask", floor=["jp_f_masu_set"], front=["jp_f_kanban_miki"],
      door=["jp_s_shopfront_noren_long", "jp_f_sugidama"], tori=("jp_f_taru_komo", "jp_f_taru_cask"),
      era="KEPT: BTI 575-579 (casks, masu, flasks; the sugidama)")
trade("nimeuri", "Cooked-food and sake house (nimeuri-ya)",
      strip=["jp_f_konro_nabe3", "jp_f_taru_cask"], stock="jp_f_tana_091_3", stock_top=["jp_f_tableware_bowls"],
      choba="desk", corner="jp_f_taru_cask", floor=["jp_f_meal_left_two"], wall="jp_f_menu_board",
      door=["jp_s_shopfront_noren_half"], front=["jp_f_kanban_niuri"], street=["jp_s_bench_1ken"],
      tori=("jp_f_taru_komo", "jp_f_oke_bucket"), era="KEPT: BTI 659-661 (early 18th c.); no oden in broth")
trade("kusuri", "Apothecary and doctor (kusuri-ya / isha)",
      steps=("jp_f_sg_medicine", "jp_f_sg_medicine", "jp_f_sg_medicine"), strip=["stand", "jp_f_yagen"],
      stock="jp_f_yakudansu", corner="jp_f_jar_m_pale",
      front=["jp_f_kanban_yakushu", "jp_s_shopfront_shape_gourd"], tori=("jp_f_box_m", "jp_f_jar_s"),
      era="KEPT: BTI 806-820 (Toyama medicine c.1690); no Dutch-learning medicine (1770s)")
trade("shichiya", "Pawnbroker (shichi-ya)",
      steps=("jp_f_sg_pawn", "jp_f_sg_pawn", "jp_f_sg_coins"), strip=["stand", "jp_f_senryobako"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_sg_pawn"], wall="jp_f_pawn_board", front=["jp_f_kanban_shichi"],
      tori=("jp_f_box_m", "jp_f_kori"), kura=True, era="KEPT: BTI 831-833 (the kura is essential: place one behind)")
trade("ryogae", "Moneychanger (ryogae-ya)",
      steps=("jp_f_sg_coins", "jp_f_sg_coins", "jp_f_sg_coins"), strip=["stand", "jp_f_senryobako"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_choba_set_tenbin"], corner="jp_f_box_s_lacquer",
      front=["jp_f_kanban_ryogae", "jp_f_kanban_shape_fundo"], tori=("jp_f_box_m", "jp_f_jar_m"), kura=True,
      era="KEPT: BTI 826-830; sign: fundo outline (BTI says coin-shaped), flagged")
trade("honya", "Publisher and bookshop (hanmoto / shomotsu-ya)",
      steps=("jp_f_sg_books", "jp_f_sg_books", "jp_f_sg_books"), strip=["stand", "jp_f_box_m"],
      stock="jp_f_tana_091_3", stock_top=["jp_f_sg_books"], wall="jp_f_print_line_books", floor=["jp_f_sg_books"],
      front=["jp_f_kanban_shorin"], tori=("jp_f_box_m", "jp_f_debris_paper"),
      era="KEPT: BTI 500-512; ink-only prints (benizuri-e 1744, nishiki-e 1765 later)")
