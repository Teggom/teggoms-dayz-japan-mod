"""The townhouse unit template (B0 step 0c): one snap-together town house unit (machiya) of a street row, built from
kit parts for a set of parameters. It is the test bed for B2's party wall, party roof end and roof corner parts
(PARTS_GAP_AUDIT §5 parts 2-4, §6 risk 1). Those parts do not exist yet: the template calls HOOKS for them and, while
a hook is None, builds a clearly marked PLACEHOLDER and lists it in part.meta['placeholders'].

    H, info = townhouse.build(frontage=3, region="kamigata", position="end", free="right", tori="left")

Parameters
  frontage   2 | 3 | 4 ken along the street
  region     'kamigata' (DW11: tile roof and pent, udatsu, mushiko upper front) |
             'edo'      (DW12: plastered nuriya upper front, board pent and lean-to, no udatsu, main roof covering
                         sangawara | itabuki | kakigara, 1730 Edo about half tiled)
  position   'end'    one free gable side (its own gable wall, gable pent, udatsu on Kamigata), one party side
             'middle' two party sides
             'corner' one side on a side street (the street pent wraps round the corner: roof_corner), one party side
  free       'left' | 'right': the free / corner side for end and corner units, seen from the street facing the front
  tori       'left' | 'right': the toriniwa (earth-floored passage, entrance) side, seen from the street
             (DayZ's frame is left-handed: from the street, the street-view LEFT is the kit frame's HIGH-x side)
  covering   main roof covering (default: sangawara)
  geya_ken   1 | 2: depth of the rear lean-to kitchen (doma, back door)
  shopfront  koshi lattice variant of the shop bays (openings.part_koshi; default _degoshi, proven on the machiya)
  hooks      {name: fn} overrides of HOOKS for this build

Plan (the proven machiya_t3_01 plan, generalised; PLAYBOOK §2-4): omoya W x 3 ken (main span 3 ken, urban rule,
G1 A1-4) with a low sealed upper storey (G0-4): toriniwa (doma) 1 ken wide full depth with the street entrance;
raised tatami rooms mise (street) and oku (back) across the rest; geya lean-to kitchen (doma) behind; kirizuma main
roof, street pent.

Frames. The template builds in the canonical kit frame with the toriniwa on the LOW-x side (x 0..1 ken; that is the
street-view right): x along the street, z 0 = street wall line (+z = street), back = -z, y 0 = grade; every post on
the half-ken grid. tori='left' (street view) mirrors the finished unit (x -> W - x). Inside the template and in the
hook ctx, 'left' / 'right' mean the canonical kit frame's low-x / high-x sides; info['party'], info['free'] and
info['corner'] are given back in street-view terms. The LOT: a free side's lot line is its wall line; a party side's lot line is LOT_PAD outside the
wall line, so two neighbouring units' end posts stand PARTY_GAP apart and no two walls are coplanar (§6 risk 1: each
unit seals on its own, because a neighbour may be missing). Neighbours snap lot line to lot line: unit spacing =
info['lot_width']. model() puts the origin on the lot centre at grade.

Hooks: signature fn(B, ctx) -> None; ctx is described in ctx() (plus side, frame, part, roof_part, roof_info).
B2 (2026-09-29) filled them with the real parts (jpparts/party.py; HOOKS below). hooks={name: None} brings back B0's
placeholder for that hook.
  party_wall      one call per party side and part ('omoya' | 'geya'): jp_p_wall_party on the unit's end wall line
                  (stone course + dodai, earth wall with the interior clay on the room face, floor beam, upper wall,
                  a plain earth gable cut to the roof section and sealed to the rafter underside; the lean-to's sloped
                  wall); one far-LOD slab in Resolution 3.
  party_roof_end  one call per party side after the lean-to and before the main roof is merged. While it is set the
                  template builds the main roof and the lean-to with PLAIN party ends (roofs.roof plain_ends,
                  leanto.roof verges) running to LOT_GAP (2 mm) inside the lot line; the hook adds the closure bands
                  (main roof, street pent unless this unit's own udatsu stands on the seam, lean-to) and the ridge end
                  plate (jp_p_roof_party_end).
  roof_corner     corner units only: the hipped pent corner between the street pent and the side pent
                  (jp_p_roof_corner), mirrored for a right corner.
  seam_cap        one call per party side, both regions; only the seam's OWNER builds (ctx['owner'], the udatsu rule):
                  main roof + lean-to, and in Edo the street pent (jp_p_roof_seam_cap). Kamigata's udatsu covers the
                  pent seam.
Always (B2): keta, pent purlins, pent brackets and flashing stop inside the lot line on a party side (no face of one
unit is coplanar with its neighbour's); an udatsu owner's pent stops at its udatsu's inner face.
"""
import math

from ..core import Part, box, KEN, HALF, POST
from .. import walls, frame, found, openings, roofs as R, roofparts, trim, floors as FL, leanto, party as PT
from ..assemble import Builder, to_world

# B2 (2026-09-29): the real parts fill the hooks (jpparts/party.py). Pass hooks={name: None} to get B0's placeholder.
HOOKS = {"party_wall": PT.hook_party_wall, "party_roof_end": PT.hook_party_roof_end,
         "roof_corner": PT.hook_roof_corner, "seam_cap": PT.hook_seam_cap}
SV = {"left": "right", "right": "left"}      # street-view side <-> kit-frame x side (the DayZ frame is left-handed)

PARTY_GAP = 0.008            # between two neighbouring units' end posts (no coplanar faces)
LOT_PAD = POST / 2 + PARTY_GAP / 2     # party lot line outside the end wall line
HAFU_OUT = 0.035             # the placeholder verge's bargeboard stands this far outside the roof edge

# levels: the machiya_t3_01 section (walked in game at G3)
DOMA, SILL, FLOOR = 0.05, 0.27, 0.50
CEIL, LOFT = 3.00, 3.15
KETA_O = LOFT + 1.30
EAVE_O = KETA_O + 0.18
GTIE = EAVE_O - 0.21
PENT_Y, GPENT_Y = 3.30, 3.10
GEYA_EAVE = 2.69
KETA_G = GEYA_EAVE - 0.18
DO = 3 * KEN                 # omoya depth = main roof span (urban 3-ken rule, G1 A1-4)
A_, B_ = POST / 2, KEN - POST / 2

REGION = {
    "kamigata": {"covering": "sangawara", "pent": "tile", "gable_pent": "gable", "geya": "sangawara", "udatsu": True,
                 "upper": "mushiko", "courses": 5},
    "edo": {"covering": "sangawara", "pent": "board", "gable_pent": "board", "geya": "itabuki", "udatsu": False,
            "upper": "nuriya", "courses": 3},
    # C1 (2026-09-30): the Tokaido post-town house (DW10, home side) and the inn (TR05): a plain town house of the
    # highway towns, no udatsu, board pent, board lean-to; the upper front plastered (nuriya) or boarded
    "tokaido": {"covering": "sangawara", "pent": "board", "gable_pent": "board", "geya": "itabuki", "udatsu": False,
                "upper": "nuriya", "courses": 3},
}
# C1: upper = 'full' (the grand inn, G1 A1 ruling 3 / G0-5): a walkable upper storey, keta this far above its floor
FULL_UPPER_H = 2.55
PENT_CFG = {"tile": (0.91, 0.40), "board": (0.91, 0.275), "gable": (0.45, 0.40)}      # projection, pitch


def _other(side):
    return "right" if side == "left" else "left"


def budget_class(frontage=3, region="kamigata", position="end", **_):
    """Face budget class (PLAYBOOK §12, buildings/registry.BUDGETS) for a unit. Stephen 2026-09-30: the Kamigata 4-ken
    end and corner units may run over the townhouse budget (worst 10,468 faces), so they are 'large'."""
    if region == "kamigata" and frontage == 4 and position in ("end", "corner"):
        return "large"
    if frontage >= 5 or _.get("upper") == "full":
        return "large"              # C1: the inns (5-ken hatago, the two-storey grand inn)
    return "townhouse"


def build(frontage=3, region="kamigata", position="end", free="right", tori="left", covering=None, geya_ken=1,
          shopfront="_degoshi", hooks=None, name=None, upper=None, pent=None, stable=None, split=False,
          mise_floor=None):
    """C1 (2026-09-30) additions, all off by default (the 60 unit combinations build exactly as before):
      position 'detached'  both gables free (the post-town house and the inns: the machiya pattern, no party side)
      frontage 5           the inns
      upper                override the region's upper front: 'mushiko' | 'nuriya' | 'board' (itabari boards) |
                           'full' (a walkable upper storey: the grand inn, one per tier-3 town, G0-5 / G1 A1 ruling 3;
                           detached, frontage 5): upper floor with a stair (jp_p_stair _box) up from the oku, a front and
                           back room upstairs, sliding shoji windows on the street, amado windows on the gables
      pent                 override the street pent: 'tile' | 'board'
      stable               a jp_p_frame_stall variant ('_umaya') in the kitchen doma, needs geya_ken 2 (DW10 stable)
      split                the oku split into two rooms by a partition with a single door (the inn's guest rooms)
    S1 (2026-09-30), off by default:
      mise_floor           '_455' | '_910': the shop room gets the board display strip (jp_p_fit_mise_floor,
                           floors.mise) along its street edge instead of the front tatami row (G1 A2: shop display =
                           board strip + stepped stands); used by the shop-set variants (buildings/shop_sets.py)

    Build one unit. Returns (H, info): H in the kit frame (lot from info['lot'][0] to info['lot'][1] along x),
    info = {lot, lot_width, W, DO, DG, party, free, corner (street-view sides), kit_sides, rooms, floors, posts,
    placeholders (sides street-view), params}."""
    if frontage not in (2, 3, 4, 5):
        raise ValueError("frontage %r: 2, 3, 4 or 5 ken" % frontage)
    if region not in REGION:
        raise ValueError("region %r: kamigata, edo or tokaido" % region)
    if position not in ("end", "middle", "corner", "detached"):
        raise ValueError("position %r: end, middle, corner or detached" % position)
    if geya_ken not in (1, 2):
        raise ValueError("geya_ken %r: 1 or 2" % geya_ken)
    rg = dict(REGION[region])
    if upper:
        if upper not in ("mushiko", "nuriya", "board", "full"):
            raise ValueError("upper %r: mushiko, nuriya, board or full" % upper)
        rg["upper"] = upper
    if pent:
        if pent not in ("tile", "board"):
            raise ValueError("pent %r: tile or board" % pent)
        rg["pent"] = pent
    full = rg["upper"] == "full"
    if full and (position != "detached" or frontage < 5 or rg["udatsu"]):
        raise ValueError("upper 'full' (the grand inn): detached, frontage 5, no udatsu")
    if stable and geya_ken != 2:
        raise ValueError("stable: needs geya_ken 2 (the stall stands in the kitchen doma)")
    if split and frontage < 5:
        raise ValueError("split: frontage 5 (the inn)")
    # C1: the section's upper levels (a full upper storey raises the keta, eave and gable tie)
    keta_o = LOFT + FULL_UPPER_H if full else KETA_O
    eave_o = keta_o + 0.18 if full else EAVE_O
    gtie = eave_o - 0.21 if full else GTIE
    fam = covering or rg["covering"]
    if fam not in ("sangawara", "itabuki", "kakigara"):
        raise ValueError("covering %r: sangawara, itabuki or kakigara" % fam)
    hk = dict(HOOKS)
    hk.update(hooks or {})
    W = frontage * KEN
    DG = geya_ken * KEN
    ZB, ZG = -DO, -(DO + DG)
    XT = KEN
    if free not in ("left", "right") or tori not in ("left", "right"):
        raise ValueError("free / tori: 'left' or 'right' (seen from the street)")
    xfree, xtori = SV[free], SV[tori]              # street view -> kit x side ('left' = low x)
    # canonical frame: toriniwa on the low-x side. The free side in that frame:
    if position == "detached":                  # C1: both gables free
        cfree, frees = None, {"left", "right"}
    else:
        cfree = None if position == "middle" else (xfree if xtori == "left" else _other(xfree))
        frees = {cfree} if cfree else set()
    party = {"left", "right"} - frees
    corner = cfree if position == "corner" else None
    T_MAIN = R.PITCH[fam]

    def street(s):
        """A canonical kit side as the street-view side of the finished (possibly mirrored) unit."""
        return SV[s] if xtori == "left" else s
    gfam = rg["geya"]
    # verge overhang per side: free = the covering's gable overhang; party = the flush party end 2 mm inside the lot
    # line (B2 party_roof_end: roofs.roof plain_ends), or B0's placeholder verge cut so its bargeboard ends at the lot
    # line when that hook is off
    g_free = R.GABLE_OV[fam]
    flush_end = bool(hk["party_roof_end"])
    g_party = LOT_PAD - PT.LOT_GAP if flush_end else LOT_PAD - HAFU_OUT
    gov = (g_party if "left" in party else g_free, g_party if "right" in party else g_free)
    ggov = (g_party if "left" in party else R.GABLE_OV[gfam], g_party if "right" in party else R.GABLE_OV[gfam])
    plain = (flush_end and "left" in party, flush_end and "right" in party)
    lot = (-LOT_PAD if "left" in party else 0.0, W + LOT_PAD if "right" in party else W)
    # the seam this unit owns (udatsu in Kamigata, seam cap): the party line on its LOW-x side in the finished
    # (possibly mirrored) unit; a mirrored unit's final low-x side is its canonical high-x side
    useam = "left" if xtori == "left" else "right"
    keta_ext = lambda sd: (LOT_PAD - PT.LOT_GAP) if sd in party else 0.30      # noqa: E731  no keta into a neighbour
    pent_cfg = PENT_CFG[rg["pent"]]
    geya_cfg = {"z_wall": ZB - POST / 2, "z_eave": ZG, "eave_y": GEYA_EAVE, "t": leanto.PITCH[gfam],
                "ov": R.EAVE_OV[gfam], "fam": gfam}

    nm = name or "jp_townhouse_%s_%dk_%s" % (region, frontage, position)
    H = Part(nm, "", "buildings", tiers=[2, 3], used_for="snap-together townhouse unit (%s, %d ken, %s)"
             % (region, frontage, position))
    H.wear = "_w1"
    posts, log, placeholders = [], [], []
    B = Builder(H, posts=posts, log=log)
    rooms, floors_obst, windows = [], [], []

    # wall-line frames (yaw, origin): the sub-part's +x runs along the wall, its +z faces out
    F_FRONT = (0.0, (0.0, 0.0, 0.0))
    F_BACK_O = (180.0, (W, 0.0, ZB))
    F_LEFT_O = (90.0, (0.0, 0.0, ZB))
    F_RIGHT_O = (-90.0, (W, 0.0, 0.0))
    F_TORI = (90.0, (XT, 0.0, ZB))
    F_MID = (0.0, (0.0, 0.0, -DO / 2))
    F_BACK_G = (180.0, (W, 0.0, ZG))
    F_LEFT_G = (90.0, (0.0, 0.0, ZG))
    F_RIGHT_G = (-90.0, (W, 0.0, ZB))
    SIDE_O = {"left": F_LEFT_O, "right": F_RIGHT_O}
    SIDE_G = {"left": F_LEFT_G, "right": F_RIGHT_G}

    def ctx(**kw):
        c = {"W": W, "DO": DO, "DG": DG, "ZB": ZB, "ZG": ZG, "lot": lot, "party": sorted(party), "free": cfree,
             "corner": corner, "region": region, "covering": fam, "geya_covering": gfam, "gov": gov,
             "frames": {"front": F_FRONT, "back": F_BACK_O, "left": F_LEFT_O, "right": F_RIGHT_O,
                        "geya_back": F_BACK_G, "geya_left": F_LEFT_G, "geya_right": F_RIGHT_G},
             "levels": {"doma": DOMA, "sill": SILL, "floor": FLOOR, "ceil": CEIL, "loft": LOFT, "keta": keta_o,
                        "eave": eave_o, "gable_tie": gtie, "pent": PENT_Y, "geya_eave": GEYA_EAVE},
             "pitch": T_MAIN, "lot_pad": LOT_PAD, "party_gap": PARTY_GAP, "courses": rg["courses"],
             "pent": (rg["pent"],) + pent_cfg, "geya": geya_cfg, "udatsu": bool(rg["udatsu"])}
        if "side" in kw:
            c["owner"] = kw["side"] == useam
            c["udatsu_here"] = bool(rg["udatsu"]) and kw["side"] == useam and kw["side"] in party
        c.update(kw)
        return c

    itado_twin = openings.part_itado("_twin")
    itado_single = openings.part_itado("_single")
    shoji_single = openings.part_shoji_ext("_single")
    shoji_hikiwake = openings.part_shoji_ext("_hikiwake")

    # ================================================================== STREET FRONT (z = 0)
    s = B.P("front_lowsill")
    frame.dodai(s, -0.06, KEN + HALF + 0.06, z=0.0, y_top=DOMA)
    H.merge(s)
    B.dodai_stones(F_FRONT, KEN + HALF + 0.10, W, 11, SILL)
    B.posts_on(F_FRONT, [0.0, KEN, KEN + HALF], DOMA, keta_o)
    B.posts_on(F_FRONT, [k * KEN for k in range(2, frontage + 1)], SILL, keta_o)
    B.wall(F_FRONT, "front_b1", "shinkabe", 0.0, KEN, DOMA, CEIL, openings_=[(A_, B_, DOMA, DOMA + 2.0)])
    B.place_door(itado_twin, F_FRONT, 0.0, DOMA, label="Entrance (street)")
    dn = {"entrance": "DoorsTwin%d" % len(H.doors)}                # C1: door names for rooms.json
    B.wall(F_FRONT, "front_b2a", "shinkabe", KEN, KEN + HALF, DOMA, CEIL, grime=[(KEN + A_, KEN + HALF - A_, None)])
    B.wall(F_FRONT, "front_b2b", "shinkabe", KEN + HALF, 2 * KEN, SILL, CEIL,
           openings_=[(KEN + HALF + A_, 2 * KEN - A_, SILL + 0.45, SILL + 2.0)],
           koshiita=[(KEN + HALF + A_, 2 * KEN - A_, 0.39)], grime=[(KEN + HALF + A_, 2 * KEN - A_, None)])
    windows.append(("street window", F_FRONT, 2 * KEN, SILL, True, openings.part_window_slide("_shoji")))
    for k in range(2, frontage):
        x0 = k * KEN
        B.wall(F_FRONT, "front_b%d" % (k + 1), "shinkabe", x0, x0 + KEN, SILL, CEIL,
               openings_=[(x0 + A_, x0 + B_, SILL + 0.39, SILL + 2.0)], koshiita=[(x0 + A_, x0 + B_, 0.33)],
               grime=[(x0 + A_, x0 + B_, None)])
        B.put(openings.part_koshi(shopfront), F_FRONT, x0, SILL, what="jp_p_open_koshi%s (shop front)" % shopfront)
    H.add(box(-0.06, W + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_street_dark", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="floor_beam"))
    if rg["upper"] == "mushiko":
        B.wall(F_FRONT, "front_up_b1", "okabe", 0.0, KEN, LOFT, KETA_O, finish="shikkui", thick=0.15)
        for k in range(1, frontage):
            B.put(openings.part_mushiko("_oval"), F_FRONT, k * KEN, LOFT, what="jp_p_open_mushiko_oval")
    elif rg["upper"] == "board":
        # C1: the boarded upper front (itabari) of the post-town house: vertical boards on the posts
        B.wall(F_FRONT, "front_up", "board_vertical", 0.0, W, LOFT, KETA_O, mat="wood_street_dark")
    elif full:
        # C1: the grand inn's upper storey front: plastered between the posts, a sliding shoji window behind a fine
        # lattice every other ken (its panel parks over the next half-ken inside)
        up_wins = [k * KEN for k in range(1, frontage, 2)]           # 2 windows on a 5-ken front (face budget)
        B.posts_on(F_FRONT, [a + HALF for a in up_wins], LOFT, keta_o)
        B.wall(F_FRONT, "front_up", "shinkabe", 0.0, W, LOFT, keta_o, finish="shikkui", head=False,
               openings_=[(a + A_, a + HALF - POST / 2, LOFT + 0.45, LOFT + 2.0) for a in up_wins])
        for a in up_wins:
            windows.append(("upper street window", F_FRONT, a, LOFT, False, openings.part_window_slide("_shoji")))
    else:
        # Edo nuriya: the upper street front plastered all over (okabe), no mushiko
        B.wall(F_FRONT, "front_up", "okabe", 0.0, W, LOFT, KETA_O, finish="shikkui", thick=0.15)
    s = B.P("keta_front")
    frame.keta(s, -keta_ext("left"), W + keta_ext("right"), z=0.0, y_top=eave_o)
    H.merge(s)
    # street pent: to the lot line on a party side (meets the neighbour's), to the wall line at a corner (the corner
    # square is roof_corner's), 0.09 inside an udatsu'd free gable (machiya)
    proj, pt = PENT_CFG[rg["pent"]]

    def pent_end(side):
        if side in party:
            if rg["udatsu"] and side == useam:
                return LOT_PAD - 0.09          # this unit's own udatsu stands on the seam: stop at its inner face
            return LOT_PAD - PT.LOT_GAP
        if side == corner:
            return 0.0
        return -0.09 if rg["udatsu"] else 0.0
    px0, px1 = 0.0 - pent_end("left"), W + pent_end("right")
    s = B.P("pent_front")
    roofparts.pent(s, px0, px1, PENT_Y, proj, pt, rg["pent"], flush=("left" in party, "right" in party), node0=0.0)
    H.merge(s)
    log.append("roofparts.pent %s over the street front, x %.2f..%.2f" % (rg["pent"], px0, px1))
    if rg["udatsu"]:
        # one udatsu per seam: every unit carries the one on the party line that ends up on its LOW-x side in the
        # finished (possibly mirrored) unit, so a row has exactly one per seam; an end unit also carries one on its
        # free gable. A mirrored unit's final low-x side is its canonical high-x side.
        xs = []
        if useam in party:
            xs.append(-LOT_PAD if useam == "left" else W + LOT_PAD)
        for fs in sorted(frees):
            if fs != corner:
                xs.append(0.0 if fs == "left" else W)
        for x in xs:
            u = walls.udatsu_placed(x, PENT_Y, KETA_O, name="udatsu_%s" % ("L" if x <= 0 else "R"))
            H.merge(u)
            log.append("walls.udatsu_placed at x=%.3f" % x)

    # ================================================================== SIDE WALLS OF THE OMOYA
    for side in ("left", "right"):
        fr = SIDE_O[side]
        seed = 31 if side == "left" else 21
        if side in party:
            if hk["party_wall"]:
                hk["party_wall"](B, ctx(side=side, frame=fr, part="omoya"))
                continue
            placeholders.append("party_wall %s (omoya): footing + plain shinkabe + upper wall + tile gable" % street(side))
            s = B.P("party_footing_%s" % side)
            s.add(box(0.0, DO, DOMA - 0.20, SILL, -POST / 2, POST / 2, "stone_cut", vis=(1, 2, 3), geo=True, view=True,
                      fire=True, tag="party_footing"))
            B.put(s, fr, what="PLACEHOLDER party footing (%s)" % side)
            B.posts_on(fr, [KEN, KEN + HALF, 2 * KEN], SILL, GTIE)     # KEN + HALF: the mise / oku partition
            B.wall(fr, "party_%s" % side, "shinkabe", 0.0, DO, SILL, CEIL, head=False)
        elif side == "left":
            # the toriniwa gable (machiya left gable): board wall to door height, clay above, Ioka side pent
            B.dodai_stones(fr, 0.0, DO, seed, SILL)
            B.posts_on(fr, [KEN, 2 * KEN], SILL, gtie)
            B.wall(fr, "left_boards", "board_vertical", 0.0, DO, SILL, SILL + 2.0, mat="wood_street_dark",
                   grime=[(0.0, DO, POST / 2 + 0.015)])
            B.wall(fr, "left_kokabe", "shinkabe", 0.0, DO, SILL + 2.0, CEIL, head=False)
        else:
            # the rooms gable (machiya right gable): koshiita, clay, a window into the oku
            B.dodai_stones(fr, 0.0, DO, seed, SILL)
            B.posts_on(fr, [KEN, KEN + HALF, 2 * KEN, DO], SILL, gtie)
            s = B.P("right_lower")
            s.add(box(A_, DO - A_, SILL, FLOOR, -0.0375, 0.0375, "wall_nakanuri", vis=(1, 2, 3), geo=True, view=True,
                      fire=True, tag="infill"))
            rbays = ((0.0, KEN), (KEN, KEN + HALF), (KEN + HALF, 2 * KEN), (2 * KEN, DO))
            for (a, b) in rbays:
                walls.koshiita(s, a + A_, b - A_, 0.90, 0.0375, y0=SILL)
            B.put(s, fr, what="walls.koshiita h090 on the rooms gable")
            for (a, b) in rbays:
                # C1: the grand inn's oku (the stair hall) has no gable window (face budget: its upper rooms do)
                win = [(a + A_, b - A_, FLOOR + 0.75, FLOOR + 2.0)] if a == 2 * KEN and not full else []
                B.wall(fr, "right_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL, openings_=win)
            s = B.P("right_grime")
            trim.grime_band(s, A_, DO - A_, 0.0375 + 0.015, y0=SILL)
            B.put(s, fr)
            if not full:
                windows.append(("oku window", fr, DO, FLOOR, True, openings.part_amado_window("_twin")))
        # the side pent: the Ioka gable pent on a free toriniwa gable; the wrapped street pent on a corner side
        if side == corner:
            kind = rg["pent"]
            p_, t_ = PENT_CFG[kind]
            s = B.P("pent_side_%s" % side)
            # local x runs back -> front on the left frame, front -> back on the right one; stop at the street wall
            roofparts.pent(s, 0.0, DO, PENT_Y, p_, t_, kind)
            B.put(s, fr, what="roofparts.pent %s wrapped along the side street (%s)" % (kind, side))
        elif side == "left" and side in frees:
            kind = rg["gable_pent"]
            p_, t_ = PENT_CFG[kind]
            s = B.P("pent_gable")
            roofparts.pent(s, 0.0, DO, GPENT_Y, p_, t_, kind)
            B.put(s, fr, what="roofparts.pent %s (Ioka side pent)" % kind)
    for side in ("left", "right"):
        fr = SIDE_O[side]
        if side in party and hk["party_wall"]:
            continue
        s = B.P(side + "_beam")
        s.add(box(-0.06, DO + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
                  view=True, fire=True, tag="floor_beam"))
        B.put(s, fr)
        if full:
            # C1 grand inn: the upper storey's gable wall; one amado window per gable (face budget): the left gable
            # lights the back room (its local x runs back -> front), the right gable the front room (front -> back)
            ups = (0.0,)
            # (inner nodes only: the corners get their full-height posts from the front / back walls)
            B.posts_on(fr, [a + d for a in ups for d in (0.0, KEN) if 1e-6 < a + d < DO - 1e-6], LOFT, gtie)
            B.wall(fr, side + "_upper", "shinkabe", 0.0, DO, LOFT, gtie, finish="shikkui", head=False,
                   openings_=[(a + A_, a + B_, LOFT + 0.70, LOFT + 2.0) for a in ups])
            for a in ups:
                windows.append(("upper gable window", fr, a, LOFT, False, openings.part_amado_window("_twin")))
        else:
            B.wall(fr, side + "_upper", "shinkabe", 0.0, DO, LOFT, gtie, finish="shikkui", head=False)
        g = B.P(side + "_gable")
        walls.gable(g, DO, T_MAIN, eave_o, "_tile" if fam == "sangawara" else "_board")
        B.put(g, fr, what="walls.gable (%s)%s" % (side, " PLACEHOLDER for the party wall" if side in party else ""))
    if corner:
        if hk["roof_corner"]:
            hk["roof_corner"](B, ctx(side=corner))
        else:
            placeholders.append("roof_corner %s: the street pent and the side pent stop at the corner (open square)"
                                % street(corner))

    # ================================================================== OMOYA BACK WALL z = ZB (local x = W - x)
    B.posts_on(F_BACK_O, [k * KEN for k in range(frontage + 1)], DOMA, keta_o)
    B.interior = True
    s = B.P("back_o_sill")
    s.add(box(-0.06, W - KEN + 0.06, DOMA, SILL, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True,
              view=True, fire=True, tag="dodai"))
    s.add(box(A_, W - KEN - A_, SILL, FLOOR, -0.0375, 0.0375, "wall_nakanuri_int", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="infill"))
    B.put(s, F_BACK_O)
    if split:
        # C1: the split partition's single door also abuts the back wall: its head rail stops short of both door lines
        xs_l = W - (XT + 2 * KEN)
        B.wall(F_BACK_O, "back_o_rooms", "shinkabe", 0.0, xs_l, FLOOR, CEIL, head_clip=(-1.0, xs_l - POST / 2 - 0.12))
        B.wall(F_BACK_O, "back_o_rooms2", "shinkabe", xs_l, W - KEN, FLOOR, CEIL,
               head_clip=(xs_l + POST / 2 + 0.12, W - KEN - POST / 2 - 0.12))
    else:
        B.wall(F_BACK_O, "back_o_rooms", "shinkabe", 0.0, W - KEN, FLOOR, CEIL,
               head_clip=(-1.0, W - KEN - POST / 2 - 0.12))
    s = B.P("back_o_passage")               # the open toriniwa passage into the kitchen, head beam at door height
    s.add(box(W - KEN + A_, W - A_, DOMA + 2.0, DOMA + 2.0 + walls.HEAD_T, -POST / 2, POST / 2, "wood_weathered",
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="head_rail"))
    s.add(box(W - KEN + A_, W - A_, DOMA + 2.0 + walls.HEAD_T, CEIL, -0.0375, 0.0375, "wall_nakanuri_int",
              vis=(1, 2, 3), geo=True, view=True, fire=True, tag="kokabe"))
    B.put(s, F_BACK_O)
    B.interior = False
    s = B.P("back_o_beam")
    s.add(box(-0.06, W + 0.06, CEIL, LOFT, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3), geo=True, view=True,
              fire=True, tag="floor_beam"))
    B.put(s, F_BACK_O)
    B.wall(F_BACK_O, "back_o_upper", "shinkabe", 0.0, W, LOFT, keta_o, finish="shikkui", head=False)
    s = B.P("keta_back")
    frame.keta(s, -keta_ext("left"), W + keta_ext("right"), z=ZB, y_top=eave_o)
    H.merge(s)

    # ================================================================== ROOM EDGE x = 1 ken (toriniwa side)
    B.interior = True
    B.posts_on(F_TORI, [0.0, KEN, KEN + HALF, 2 * KEN + HALF, DO], DOMA, CEIL)
    s = B.P("tori_edge")
    s.add(box(0.0, DO, DOMA, FLOOR - 0.12, -0.03, 0.03, "wood_sooted", vis=(1, 2, 3), tag="yukashita_boards"))
    s.add(box(0.0, DO, FLOOR - 0.12, FLOOR - 0.10, -0.05, 0.05, "wood_weathered", vis=(1,), tag="kamachi_lip"))
    B.put(s, F_TORI)
    oc = A_ + (openings.SINGLE_OPEN - openings.STUB) / 2
    for (a, room) in ((0.0, "oku"), (KEN + HALF, "mise")):
        B.wall(F_TORI, "tori_door_%s" % room, "shinkabe", a, a + KEN, FLOOR, CEIL,
               openings_=[(a + A_, a + B_, FLOOR, FLOOR + 2.0)])
        B.place_door(shoji_single, F_TORI, a, FLOOR, label="Toriniwa -> %s" % room)
        dn["tori_" + room] = "DoorsTwin%d" % len(H.doors)
        st = B.P("step_%s" % room)
        found.step(st, oc, "natural", drop=FLOOR - DOMA, width=1.04)
        B.put(st, F_TORI, a, FLOOR, what="jp_p_found_step_natural at the %s" % room)
        ramp = (FLOOR - DOMA) / math.tan(math.radians(34.0))
        _, z0 = to_world(F_TORI, a + oc - 0.54)
        _, z1 = to_world(F_TORI, a + oc + 0.54)
        floors_obst.append(("toriniwa", FL.floor_rect(XT - POST / 2 - ramp - 0.05, XT, z0, z1)))
    for (a, b) in ((KEN, KEN + HALF), (2 * KEN + HALF, DO)):
        B.wall(F_TORI, "tori_park_%d" % int(a * 100), "shinkabe", a, b, FLOOR, CEIL)

    # ================================================================== MISE / OKU PARTITION z = -1.5 ken
    wr = W - XT
    XS = XT + 2 * KEN                                            # C1 split: the oku / oku 2 partition line
    if wr >= 2 * KEN - 1e-6:
        a = XT + round((wr - KEN) / 2 / HALF) * HALF            # hikiwake pair, half-ken park bays both sides
        if split:
            a = XT + HALF                                        # C1: clear of the split partition's end post
        B.posts_on(F_MID, [a, a + KEN], FLOOR, CEIL)
        segs = [(XT, a), (a + KEN, W)]
        B.wall(F_MID, "mid_door", "shinkabe", a, a + KEN, FLOOR, CEIL, openings_=[(a + A_, a + KEN - A_, FLOOR,
                                                                                     FLOOR + 2.0)])
        B.place_door(shoji_hikiwake, F_MID, a, FLOOR, label="Mise <-> oku")
        dn["mid"] = "DoorsTwin%d" % len(H.doors)
        mid_door = True
    else:
        segs = [(XT, W)]                                         # 2-ken unit: both rooms open off the toriniwa only
        mid_door = False
    for (s0, s1) in segs:
        if s1 - s0 > 1e-6:
            B.wall(F_MID, "mid_%d" % int(s0 * 100), "shinkabe", s0, s1, FLOOR, CEIL,
                   head_clip=(KEN + POST / 2 + 0.12, 99.0) if abs(s0 - XT) < 1e-6 else None)

    if split:
        # C1 (the inn): the oku split in two guest rooms, a single shoji door + a half-ken park bay (local x runs
        # from the back wall to the mise / oku partition)
        F_SPLIT = (90.0, (XS, 0.0, ZB))
        B.posts_on(F_SPLIT, [0.0, KEN, KEN + HALF], FLOOR, CEIL)
        B.wall(F_SPLIT, "split_door", "shinkabe", 0.0, KEN, FLOOR, CEIL, openings_=[(A_, B_, FLOOR, FLOOR + 2.0)])
        B.place_door(shoji_single, F_SPLIT, 0.0, FLOOR, label="Oku <-> oku 2")
        dn["split"] = "DoorsTwin%d" % len(H.doors)
        B.wall(F_SPLIT, "split_park", "shinkabe", KEN, KEN + HALF, FLOOR, CEIL)
    well = None
    stair_info = None
    if full:
        # C1 grand inn: the upper storey. The stair (jp_p_stair _box, the kaidan-dansu look of inns and shops) climbs
        # from the oku along the omoya back wall towards the rooms gable; the upper floor is walkable with the
        # stairwell cut into it (rim + guard rail, stair.well_fn); a partition with a hikiwake pair splits the storey
        # into a front and a back room
        from .. import stair as ST
        rise = LOFT - FLOOR
        stp = Part("stair_inn", "", "")
        SS = ST.stair(stp, 1.20, rise, "box")
        run = SS["run"]
        x_foot, oz = XT + 1.20, ZB + POST / 2
        if x_foot + run + 0.90 > W - POST / 2:
            raise ValueError("full upper: no landing room past the stair head (frontage %d)" % frontage)
        B.merge(stp.transformed(180.0, (x_foot, FLOOR, oz), mirror=True))      # flight +x, width towards +z
        log.append("jp_p_stair _box in the oku, foot x=%.2f, run %.2f, rise %.2f" % (x_foot, run, rise))
        wx0, wx1, wz0, wz1 = ST.well_rect(run, 1.20, rise)
        well = (x_foot + wx0, x_foot + wx1, ZB, oz - wz0)
        stair_info = {"foot": (x_foot, oz), "run": run, "width": 1.20, "y_low": FLOOR, "y_up": LOFT, "well": well}
        floors_obst.append(("oku", FL.floor_rect(x_foot - 0.05, x_foot + run + 0.05, ZB, oz + 1.20 + 0.06)))
        floors_obst.append(("nikai_back", FL.floor_rect(well[0] - 0.10, well[1] + 0.10, ZB, well[3] + 0.10)))
        au = round((W - KEN) / 2 / HALF) * HALF
        B.posts_on(F_MID, [au, au + KEN], LOFT, LOFT + 2.35)
        B.wall(F_MID, "up_mid_door", "shinkabe", au, au + KEN, LOFT, LOFT + 2.35,
               openings_=[(au + A_, au + KEN - A_, LOFT, LOFT + 2.0)])
        B.place_door(shoji_hikiwake, F_MID, au, LOFT, label="Upstairs front <-> back")
        dn["up_mid"] = "DoorsTwin%d" % len(H.doors)
        for (s0, s1) in ((0.0, au), (au + KEN, W)):
            B.wall(F_MID, "up_mid_%d" % int(s0 * 100), "shinkabe", s0, s1, LOFT, LOFT + 2.35)
        H.merge(FL.loft("loft", 0.0, W, ZB, 0.0, CEIL, LOFT, walkable=True,
                        holes=[{"rect": well, "kind": "stair", "open": "x1", "wall": "z0"}], hole_fn=ST.well_fn()))

    # ================================================================== LOFT (sealed, G0-4) + FLOORS
    if not full:
        H.merge(FL.loft("loft", 0.0, W, ZB, 0.0, CEIL, LOFT))
    B.merge(FL.doma("doma_tori", 0.0, XT, ZB, 0.0, road=(POST / 2, XT - POST / 2, ZB - POST / 2, -POST / 2), y=DOMA))
    B.merge(FL.doma("doma_kitchen", 0.0, W, ZG, ZB, road=(POST / 2, W - POST / 2, ZG + POST / 2, ZB - POST / 2),
                    y=DOMA))
    if mise_floor:                  # S1: board display strip along the street edge, tatami behind (floors.mise)
        B.merge(FL.mise("mise_floor", XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2, top=FLOOR,
                        base=DOMA, variant=mise_floor, street="+z"))
        log.append("floors.mise %s (jp_p_fit_mise_floor): board strip along the street edge of the shop room"
                   % mise_floor)
    else:
        B.merge(FL.tatami("tatami_mise", XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2, top=FLOOR,
                          base=DOMA))
    if split:
        B.merge(FL.tatami("tatami_oku", XT + POST / 2, XS - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2, top=FLOOR,
                          base=DOMA))
        B.merge(FL.tatami("tatami_oku2", XS + POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2, top=FLOOR,
                          base=DOMA))
    else:
        B.merge(FL.tatami("tatami_oku", XT + POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2, top=FLOOR,
                          base=DOMA))
    B.interior = False

    # ================================================================== GEYA (rear lean-to kitchen)
    ytop_left = lambda lx: GEYA_EAVE + leanto.PITCH[gfam] * lx           # noqa: E731  local x = z - ZG
    ytop_right = lambda lx: GEYA_EAVE + leanto.PITCH[gfam] * (DG - lx)   # noqa: E731  local x = ZB - z
    s = B.P("back_g_lowsill")
    s.add(box(W - KEN - HALF - 0.06, W + 0.06, DOMA - 0.12, DOMA, -POST / 2, POST / 2, "wood_weathered", vis=(1, 2, 3),
              geo=True, view=True, fire=True, tag="dodai"))
    B.put(s, F_BACK_G)
    B.dodai_stones(F_BACK_G, 0.0, W - KEN - HALF - 0.10, 41, SILL)
    B.posts_on(F_BACK_G, [W - KEN - HALF, W - KEN, W], DOMA, KETA_G)
    B.posts_on(F_BACK_G, [k * KEN for k in range(frontage) if k * KEN < W - KEN - HALF - 1e-6], SILL, KETA_G)
    B.wall(F_BACK_G, "back_g_door", "shinkabe", W - KEN, W, DOMA, KETA_G, openings_=[(W - KEN + A_, W - A_, DOMA,
                                                                                    DOMA + 2.0)])
    B.place_door(itado_single, F_BACK_G, W, DOMA, mirror=True, label="Kitchen back door (yard)")
    dn["back"] = "DoorsTwin%d" % len(H.doors)
    B.wall(F_BACK_G, "back_g_park", "shinkabe", W - KEN - HALF, W - KEN, DOMA, KETA_G,
           grime=[(W - KEN - HALF + A_, W - KEN - A_, None)])
    nodes = sorted({k * KEN for k in range(frontage) if k * KEN < W - KEN - HALF - 1e-6} | {W - KEN - HALF})
    for (a, b) in zip(nodes[:-1], nodes[1:]):
        B.wall(F_BACK_G, "back_g_%d" % int(a * 100), "shinkabe", a, b, SILL, KETA_G,
               koshiita=[(a + A_, b - A_, 0.90)], grime=[(a + A_, b - A_, None)])
    gnodes = [k * KEN for k in range(geya_ken + 1)]
    for side in ("left", "right"):
        fr = SIDE_G[side]
        yt = ytop_left if side == "left" else ytop_right
        for lx in gnodes[1:-1]:
            B.posts_on(fr, [lx], SILL, yt(lx))
        if side in party:
            if hk["party_wall"]:
                hk["party_wall"](B, ctx(side=side, frame=fr, part="geya", ytop=yt))
                continue
            placeholders.append("party_wall %s (geya): footing + sloped shinkabe" % street(side))
            s = B.P("party_footing_g_%s" % side)
            s.add(box(0.0, DG, DOMA - 0.20, SILL, -POST / 2, POST / 2, "stone_cut", vis=(1, 2, 3), geo=True,
                      view=True, fire=True, tag="party_footing"))
            B.put(s, fr, what="PLACEHOLDER party footing, geya (%s)" % side)
            B.sloped_wall(fr, "geya_party_%s" % side, gnodes, SILL, yt, head_y=SILL + 2.0)
        else:
            B.dodai_stones(fr, 0.0, DG, 51 if side == "left" else 61, SILL)
            B.sloped_wall(fr, "geya_%s" % side, gnodes, SILL, yt, head_y=SILL + 2.0, koshiita_h=0.90, grime=True)
    g, sl_g = leanto.roof("roof_geya", 0.0, W, ZB - POST / 2, ZG, GEYA_EAVE, gfam, gov=ggov,
                          flash_top=None if full else KETA_O - 0.02,
                          verges=(not plain[0], not plain[1]), keta_ext=(keta_ext("left"), keta_ext("right")))
    H.merge(g)
    log.append("leanto.roof %s over the kitchen" % gfam)
    if stable:
        # C1 (DW10 stable variant): the stall (jp_p_frame_stall) in the kitchen doma against the back wall, at the far
        # end from the passage and the back door; the building's own walls close its back and one side
        from .. import stall as SL
        wst, dst = SL.VARIANTS[stable][0] * KEN, SL.VARIANTS[stable][1] * KEN
        x0s = W - POST / 2 - 0.06 - wst
        B.interior = True
        B.merge(SL.part_stall(stable).transformed(0.0, (x0s, DOMA, ZG + dst)))
        B.interior = False
        floors_obst.append(("kitchen", FL.floor_rect(x0s - 0.10, W, ZG, ZG + dst + 0.12)))
        log.append("jp_p_frame_stall %s in the kitchen doma, x %.2f..%.2f" % (stable, x0s, x0s + wst))

    # ================================================================== WINDOWS (animated like doors, after them)
    for (label, fr, dx, dy, mirror, part) in windows:
        d_ = B.place_door(part, fr, dx, dy, mirror=mirror, label=label.capitalize())
        if label == "upper gable window":
            d_.reach_sides = ("far",)       # C1: an upper-storey window is worked from inside (no ground reach)
        dn.setdefault("windows", []).append("DoorsTwin%d" % len(H.doors))

    # ================================================================== MAIN ROOF + party roof ends
    s = B.P("roof_main")
    sls, rinfo = R.roof(s, W, DO, "kirizuma", fam, eave_y=eave_o, courses=rg["courses"], eave_style="plain", gov=gov,
                        plain_ends=plain)
    for side in sorted(party):
        if hk["party_roof_end"]:
            hk["party_roof_end"](B, ctx(side=side, roof_part=s, roof_info=rinfo))
        else:
            placeholders.append("party_roof_end %s: a normal verge, bargeboard cut back to the lot line" % street(side))
        # B2: the seam cap goes on in both regions (main roof + lean-to; Edo also the street pent, which Kamigata's
        # udatsu covers); only the seam's owner builds it
        if hk["seam_cap"]:
            hk["seam_cap"](B, ctx(side=side, roof_part=s, roof_info=rinfo))
        elif region == "edo":
            placeholders.append("seam_cap %s: none (Edo has no udatsu; the seam shows)" % street(side))
    H.merge(s)
    rw = R.ridge_walk(rinfo)
    if rw:
        H.merge(rw)

    # ================================================================== grime, LOD policy
    def exterior(x, z):
        return (abs(z) < 1e-6 or abs(z - ZG) < 1e-6 or (abs(x) < 1e-6 and "left" not in party) or
                (abs(x - W) < 1e-6 and "right" not in party))
    B.grime_exterior_posts(exterior)
    B.lod_policy()

    # ================================================================== rooms and floors (canonical kit frame)
    tori_doors = [dn["entrance"], dn["tori_oku"], dn["tori_mise"]]
    mid_ = [dn["mid"]] if mid_door else []
    rooms.append({"name": "toriniwa", "tag": "doma", "floor": "earth", "level_m": DOMA,
                  "rect_kit": FL.floor_rect(POST / 2, XT - POST / 2, ZB + POST / 2, -POST / 2), "doors": tori_doors,
                  "note": "entry passage, 1 ken, full omoya depth"})
    rooms.append({"name": "mise", "tag": "shop:general", "floor": "tatami", "level_m": FLOOR,
                  "rect_kit": FL.floor_rect(XT + POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2),
                  "doors": [dn["tori_mise"]] + mid_, "note": "shop room"})
    rooms.append({"name": "oku", "tag": "zashiki", "floor": "tatami", "level_m": FLOOR,
                  "rect_kit": FL.floor_rect(XT + POST / 2, (XS if split else W) - POST / 2, ZB + POST / 2,
                                            -DO / 2 - POST / 2),
                  "doors": [dn["tori_oku"]] + mid_ + ([dn["split"]] if split else []),
                  "note": "back room" + (" (the stair up)" if full else "")})
    if split:
        rooms.append({"name": "oku2", "tag": "zashiki", "floor": "tatami", "level_m": FLOOR,
                      "rect_kit": FL.floor_rect(XS + POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2),
                      "doors": [dn["split"]], "note": "second back room"})
    rooms.append({"name": "kitchen", "tag": "doma", "floor": "earth", "level_m": DOMA,
                  "rect_kit": FL.floor_rect(POST / 2, W - POST / 2, ZG + POST / 2, ZB - POST / 2),
                  "doors": [dn["back"]], "note": "hashiri kitchen (no kamado yet: B3a/B4)" +
                  (" with a stall (%s)" % stable if stable else "")})
    if full:
        rooms.append({"name": "nikai_front", "tag": "zashiki", "floor": "boards", "level_m": LOFT,
                      "rect_kit": FL.floor_rect(POST / 2, W - POST / 2, -DO / 2 + POST / 2, -POST / 2),
                      "doors": [dn["up_mid"]], "note": "upstairs front room (street windows)"})
        rooms.append({"name": "nikai_back", "tag": "zashiki", "floor": "boards", "level_m": LOFT,
                      "rect_kit": FL.floor_rect(POST / 2, W - POST / 2, ZB + POST / 2, -DO / 2 - POST / 2),
                      "doors": [dn["up_mid"]], "note": "upstairs back room (the stairwell)"})
    fls = [{"name": r["name"], "tag": r["tag"], "rect": tuple(r["rect_kit"]), "y": r["level_m"],
            "obstacles": [rc for (n_, rc) in floors_obst if n_ == r["name"]]} for r in rooms]
    info = {"lot": lot, "lot_width": lot[1] - lot[0], "W": W, "DO": DO, "DG": DG, "party": sorted(party),
            "free": cfree, "corner": corner, "rooms": rooms, "floors": fls, "posts": posts, "log": log,
            "placeholders": placeholders, "party_lines": [x for x in (0.0, W) if (x == 0.0 and "left" in party) or
                                                          (x == W and "right" in party)],
            "params": {"frontage": frontage, "region": region, "position": position, "free": free, "tori": tori,
                       "covering": fam, "geya_ken": geya_ken, "shopfront": shopfront}}
    if upper or pent or stable or split or position == "detached":      # C1 additions (absent = the 60 as before)
        info["params"].update(upper=rg["upper"], pent=rg["pent"], stable=stable, split=split)
        info["levels"] = {"keta": keta_o, "eave": eave_o, "gable_tie": gtie, "loft": LOFT, "floor": FLOOR}
        info["stairwell"] = well
        info["stair"] = stair_info          # canonical kit frame (flight +x from the foot, width +z from the wall)
    if mise_floor:                          # S1 addition (absent = every shell as before)
        info["params"]["mise_floor"] = mise_floor
    if xtori == "right":
        H, info = _mirror(H, info)
    info["kit_sides"] = {"party": info["party"], "free": info["free"], "corner": info["corner"]}
    info["party"] = sorted(SV[s] for s in info["party"])
    info["free"] = SV.get(info["free"])
    info["corner"] = SV.get(info["corner"])
    H.meta["placeholders"] = list(info["placeholders"])
    H.meta["townhouse"] = {k: v for k, v in info.items() if k in ("lot", "lot_width", "party", "free", "corner",
                                                                    "params")}
    return H, info


def _mirror(H, info):
    """tori='right': the canonical unit mirrored about its wall centre line (x -> W - x), so the posts stay on the
    half-ken grid of the kit frame; the lot is mirrored with it."""
    l0, l1 = info["lot"]
    c = info["W"]
    M = H.transformed(0.0, (c, 0.0, 0.0), mirror=True)
    M.meta = dict(H.meta)

    def mx(r):
        return (c - r[1], c - r[0], r[2], r[3])
    info = dict(info)
    info["lot"] = (c - l1, c - l0)
    info["rooms"] = [dict(r, rect_kit=mx(r["rect_kit"])) for r in info["rooms"]]
    info["floors"] = [dict(f, rect=mx(f["rect"]), obstacles=[mx(o) for o in f["obstacles"]]) for f in info["floors"]]
    info["posts"] = [(c - x, z, y0, y1) for (x, z, y0, y1) in info["posts"]]
    info["party_lines"] = [c - x for x in info["party_lines"]]
    info["party"] = sorted({"left": "right", "right": "left"}[s] for s in info["party"])
    info["free"] = {"left": "right", "right": "left"}.get(info["free"])
    info["corner"] = {"left": "right", "right": "left"}.get(info["corner"])
    return M, info


def model(**params):
    """The unit in the MODEL frame (origin = lot centre at grade, +z = street front) for the building pipeline.
    Returns (M, floors, rooms, info); floors / rooms rects in model coordinates."""
    H, info = build(**params)
    l0, l1 = info["lot"]
    cx, cz = (l0 + l1) / 2, -(info["DO"] + info["DG"]) / 2
    M = H.transformed(0.0, (-cx, 0.0, -cz))
    M.meta = dict(H.meta)

    def mr(r):
        return (r[0] - cx, r[1] - cx, r[2] - cz, r[3] - cz)
    floors = [dict(f, rect=mr(f["rect"]), obstacles=[mr(o) for o in f["obstacles"]]) for f in info["floors"]]
    rooms = [dict(r, rect_model=[round(v, 3) for v in mr(r["rect_kit"])]) for r in info["rooms"]]
    info = dict(info, posts_model=[(x - cx, z - cz, y0, y1) for (x, z, y0, y1) in info["posts"]],
                party_lines_model=[x - cx for x in info["party_lines"]], centre=(cx, cz))
    return M, floors, rooms, info
