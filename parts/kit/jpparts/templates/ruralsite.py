"""The wave-3c-2 rural / industrial site template (W3C2, Phase C wave 3c-2, 2026-10-02): the charcoal kiln under its
roof (TR23), the climbing kiln (TR18), the daruma tile kiln (TR19), the lime kiln (TR26), the quarry face (TR25), the
mine adit (TR27), the timber slide (TR24), the salt bed (TR22), and the two new huts: the bunk hall (KEEP_DWELLINGS 4:
miners, loggers) and the salt-boiling hut (kamaya) with its shell pan; the yards through templates/dwelling.compound.
Research, sizes and every recorded choice: spikes/W3C2/W3C2_NOTES.md. The huts and sheds a site reuses (the west
hut, the open sheds, W3B's earth-floor workshops and saw shed) are earlier shells, furnished in buildings/w3c2_sets.py.

    M, floors, rooms, info = ruralsite.model(kind="sumigama")

Kinds (kit frame as rural.py: x 0..W along the front, z 0 = front line, +z = out, z -D = back, y 0 = grade)
  sumigama     the charcoal kiln (jp_p_site_kiln_dome) under its board roof on six posts (3 x 3 ken, open sides)
  noborigama   the climbing kiln (jp_p_site_kiln_climbing) on its bank + the stoking floor before the fire mouth
  bunkhall     W 6 x D 3 ken, board walls: the entrance doma (2 ken, front + back doors, the hearth) and the long
               raised sleeping floor (0.40, one irori); roof itabuki | ishioki
"""
import math

from ..core import Part, box, prism, KEN, HALF, POST, KETA_H, DOOR_H
from .. import walls, openings, roofs as R, floors as FL, found, ruralsite_parts as RS
from .rural import Shell, _r, DOMA, A_, _kamado, _irori, big_leaf
from .civic import fit, trim_lods, koshiyane, open_front, _ext
from . import dwelling as DW

KINDS = ("sumigama", "noborigama", "bunkhall", "compound")


def _open_roof(S, W, D, E, fam="itabuki", ov=None, ridge="bamboo"):
    """An open roof on its corner posts (+ a post at every 2 ken of the eave lines): the kiln roofs."""
    YT = E - KETA_H
    sls, info_r, K = S.roof(W, D, "kirizuma", fam, E, ov=ov, soot=True, ridge=ridge, joya_posts=False)
    S.keta_ring(W, D, E, hip=False)
    nx = max(1, int(round(W / (2 * KEN))))
    for k in range(nx + 1):
        x = round(W * k / nx, 4)
        for z in (0.0, -D):
            S.post(x, z, YT + KETA_H - 0.02)
    return sls, info_r, K


# ================================================================================================ TR23 charcoal kiln
def sumigama(name=None, wear="_w2"):
    W, D, E = 3 * KEN, 3 * KEN, 2.70
    S = Shell(name or "jp_sumigama", W, D, [1, 2], "charcoal kiln under its roof (sumi-gama, TR23)", wear)
    B = S.B
    sls, info_r, K = _open_roof(S, W, D, E)
    # the work floor round the kiln (packed earth), the kiln in the middle, its mouth to the front
    cx, cz = W / 2, -D / 2 - 0.10
    B.interior = True
    B.merge(FL.doma("floor", -0.10, W + 0.10, -D - 0.10, 0.25, road=(A_, W - A_, -D + A_, -0.10), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    kp = B.P("kiln")
    ki = RS.kiln_dome(kp, cx, cz)
    B.put(kp, (0.0, (0.0, 0.0, 0.0)), what="jp_p_site_kiln_dome _charcoal (cold, opened)")
    S.obst.append(("floor", _r(cx - ki["rx"] - 0.05, cx + ki["rx"] + 0.05, cz - ki["rz"] - 0.40,
                               ki["front"] + 0.15)))
    S.obst.append(("floor", _r(cx - 1.25, cx + 1.25, ki["front"], ki["front"] + 0.50)))     # the mouth's stones
    fit(S, "rake", "floor", rect=(A_ + 0.05, A_ + 0.60, -D + A_ + 0.05, -D + A_ + 0.80), obstacle=False,
        note="the kiln rake and long hoe leaning on a back post")
    S.room("floor", "workshop", "earth", DOMA, (A_, W - A_, -D + A_, -0.10), [],
           "the kiln floor under the roof: the earth-dome kiln, its fire mouth to the front, the flue at the back",
           enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "sumigama"}, "levels": {"doma": DOMA, "eave": E}, "koyagumi": K["counts"],
                        "kiln": ki}, exterior=_ext(W, D))
    return H, info


# ================================================================================================ TR18 climbing kiln
def noborigama(name=None, wear="_w2"):
    """The climbing kiln on its bank (jp_p_site_kiln_climbing _4ch) + the stoking floor before its fire mouth."""
    K = RS.NOBORI
    W = 2 * KEN
    LF = KEN                                     # the stoking floor in front of the fire mouth
    D = LF + K["lf"] + K["n"] * K["lc"] + K["lflue"] + 0.40
    S = Shell(name or "jp_noborigama", W, D, [2, 3], "climbing kiln (noborigama, TR18), Seto / Mino type", wear)
    B = S.B
    kp = B.P("kiln")
    ki = RS.kiln_climbing(kp, open_door=0)
    B.put(kp, (0.0, (W / 2, 0.0, -LF)), what="jp_p_site_kiln_climbing _4ch (cold, the lowest loading door open)")
    # the stokers' shelter: a board roof on four posts over the stoking floor (its back eave over the firebox vault)
    sls, info_r, K_ = _open_roof(S, W, LF, 2.75)
    B.interior = True
    B.merge(FL.doma("stoke", 0.0, W, -LF, 0.0, road=(0.15, W - 0.15, -LF + 0.02, -0.15), y=DOMA,
                    mats=FL.MATS_DOMA_EARTH))
    B.interior = False
    S.obst.append(("stoke", _r(W / 2 - 0.80, W / 2 + 0.80, -LF, -LF + 0.85)))       # the mouth's jambs + ash
    S.room("stoke", "workshop", "earth", DOMA, (0.15, W - 0.15, -LF + 0.02, -0.15), [],
           "the stoking floor before the fire mouth under the stokers' shelter (the kiln itself is solid: its doors "
           "are look-ins)", enclosed=False)
    trim_lods(S.H)
    H, info = S.finish({"params": {"kind": "noborigama"}, "levels": {"doma": DOMA}, "kiln": ki,
                        "koyagumi": K_["counts"]}, exterior=None)
    return H, info


# ================================================================================================ yards
YARDS = {
    # the potter's yard: a light bamboo fence (yotsume) round the work shed and the drying racks; the gate (by the
    # picker: a 1.5-ken opening for the firewood carts) in the south line towards the kiln
    "potteryyard": dict(W=7 * KEN, D=6 * KEN, closed=True,
                        runs=[([(0.0, 0.0), (0.0, 6 * KEN), (7 * KEN, 6 * KEN), (7 * KEN, 0.0)], "yotsume", {},
                               ("end", "end"))],
                        gates=[(0, 3, 1.0 * KEN) + DW.pick_gate("yotsume", status="work", carts=True)]),
}
DW.COMPOUNDS.update(YARDS)


def compound(name=None, plot="tileyard", wear="_w1"):
    return DW.compound(name=name, plot=plot, wear=wear)


# ================================================================================================ dispatch
def _builders():
    return {k: globals().get(k) for k in KINDS}


def build(kind, **params):
    fn = _builders().get(kind)
    if fn is None:
        raise ValueError("kind %r: one of %s" % (kind, ", ".join(KINDS)))
    return fn(**params)


def budget_class(kind, **params):
    """PLAYBOOK §12: the site objects and yards 'large' where they carry their own ground mass; huts 'standard'."""
    if kind in ("compound",):
        return "large"
    return "standard"


def over_budget_ok(kind, **params):
    """CA1: a deliberate overage (<= +50 %, PLAYBOOK §12) and its reason, or None."""
    return None


def model(kind, name=None, **params):
    """The shell in the MODEL frame (origin = footprint centre at grade, +z = front), as tradesite.model."""
    H, info = build(kind, name=name, **params)
    cx, cz = info.get("centre_kit", (info["W"] / 2, -info["D"] / 2))
    M = H.transformed(0.0, (-cx, 0.0, -cz))
    M.meta = dict(H.meta)

    def mr(r):
        return (r[0] - cx, r[1] - cx, r[2] - cz, r[3] - cz)
    floors = [dict(f, rect=mr(f["rect"]), obstacles=[mr(o) for o in f["obstacles"]]) for f in info["floors"]]
    rooms = [dict(r, rect_model=[round(v, 3) for v in mr(r["rect_kit"])]) for r in info["rooms"]]
    fits = []
    for f in info["fittings"]:
        g = dict(f)
        if "rect" in g:
            g["rect"] = [round(v, 3) for v in mr(g["rect"])]
        if "centre" in g:
            g["centre"] = [round(g["centre"][0] - cx, 3), round(g["centre"][1] - cz, 3)]
        if "hook" in g:
            g["hook"] = [round(g["hook"][0] - cx, 3), g["hook"][1], round(g["hook"][2] - cz, 3)]
        fits.append(g)
    info = dict(info, centre=(cx, cz), fittings_model=fits,
                portals_model=[(n, (b[0] - cx, b[1] - cx, b[2], b[3], b[4] - cz, b[5] - cz)) for n, b in info["portals"]],
                passages_model=[(x - cx, z - cz, y) for (x, z, y) in info["passages"]])
    return M, floors, rooms, info
