"""FX2 (2026-10-01; Stephen: 'komainu wanted, + paired lanterns'): stone guardian pairs for the shrine approaches.
Komainu ('a' open mouth / 'un' closed) in two period forms + a mossy pair, and the Inari foxes (kitsune) with the key
and the jewel. The figures are the sculpted FX2 meshes (spikes/FX2: figures.komainu / kitsune; references and the
era / pair rules: research/statues/REFS.md, NOTES.md); the pedestals are kit stone.

Frame (B3b): origin = the pedestal's base centre on the terrain, +z = the figure's front. In a pair the 'a' stands on
the right and the 'un' on the left as one faces the shrine; both face down the approach, toed in a little
(placement, not the model). Collision: pedestal + a body box + a head box (Geometry / View / Fire).
"""
import os
import sys

from skit import (core, W, col, SPart, add_all, moss_top, moss_face, CARVED)
from props_wood import M

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
AGED = "stone_carved_aged"
X, Y = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)


def _fx():
    sys.path.insert(0, os.path.join(DEV, "spikes", "FX2"))
    import fx2props as FX
    return FX


def pedestal(base, die, cap, wear, moss=False):
    """Three dressed stones: a wide base slab, the die (sao-ishi), a cap slab with a chamfer. Each (w, d, h).
    Returns (visual solids, collision solids, top y)."""
    out, cols = [], []
    y = -0.06
    (bw, bd, bh), (dw, dd, dh), (cw, cd, ch) = base, die, cap
    out.append(W(-bw / 2, bw / 2, y, bh, -bd / 2, bd / 2, AGED, vis=(1, 2, 3)))
    out.append(W(-bw / 2 + 0.03, bw / 2 - 0.03, bh, bh + 0.03, -bd / 2 + 0.03, bd / 2 - 0.03, AGED, vis=(1,)))
    y1 = bh + 0.03
    out.append(W(-dw / 2, dw / 2, y1, y1 + dh, -dd / 2, dd / 2, AGED, vis=(1, 2, 3)))
    y2 = y1 + dh
    out.append(W(-cw / 2 + 0.03, cw / 2 - 0.03, y2, y2 + 0.03, -cd / 2 + 0.03, cd / 2 - 0.03, AGED, vis=(1,)))
    out.append(W(-cw / 2, cw / 2, y2 + 0.03, y2 + ch, -cd / 2, cd / 2, AGED, vis=(1, 2, 3)))
    top = y2 + ch
    for s in out:
        s.wear = wear
    cols.append(col(-bw / 2, bw / 2, 0.0, y1, -bd / 2, bd / 2, AGED))
    cols.append(col(-cw / 2, cw / 2, y1, top, -cd / 2, cd / 2, AGED))
    out.append(moss_top(51, bw * 0.3, bd * 0.32, 0.10, bh, wear="_w1"))
    out.append(moss_top(52, -bw * 0.32, -bd * 0.30, 0.12, bh, wear="_w2"))
    if moss:
        out.append(moss_top(53, cw * 0.22, -cd * 0.25, 0.12, top, wear="_w2"))
        out.append(moss_top(54, -cw * 0.25, cd * 0.30, 0.09, top, wear="_w2"))
        out.append(moss_face((0.0, y1 + 0.12, -dd / 2), (-1.0, 0.0, 0.0), Y, dw * 0.8, 0.22, seed=55, wear="_w2"))
        out.append(moss_face((dw / 2, y1 + 0.10, 0.0), (0.0, 0.0, -1.0), Y, dd * 0.7, 0.18, seed=56, wear="_w2"))
    return out, cols, top


def guardian(kind, style="a", mouth="a", moss=False):
    """kind 'komainu' | 'kitsune' (mouth = 'key' | 'jewel' for the foxes)."""
    FX = _fx()
    wear = "_w2" if moss else "_w0"
    P = SPart("guardian", budget="statue", res3=True, mass=1500.0, bury=0.06)
    P.wear = wear
    if kind == "komainu":
        H = 1.00 if style == "a" else 0.88
        if style == "a":
            ped = ((0.90, 1.12, 0.20), (0.62, 0.86, 0.52), (0.72, 1.00, 0.10))
        else:
            ped = ((0.84, 1.04, 0.18), (0.58, 0.80, 0.38), (0.68, 0.92, 0.09))
        name = "komainu_%s_%s" % (style, mouth)
        body = (0.24, 0.0, 0.70, -0.46, 0.30)      # half-width, y0, y1, z0, z1 (x H)
        headb = (0.26, 0.705, 1.02, -0.20, 0.42)
    else:
        H = 0.88
        ped = ((0.62, 0.74, 0.18), (0.40, 0.56, 0.55), (0.48, 0.66, 0.08))
        name = "kitsune_" + mouth
        body = (0.16, 0.0, 0.60, -0.42, 0.20)
        headb = (0.10, 0.60, 0.99, -0.02, 0.31)
    vis, cols, top = pedestal(*ped, wear=wear, moss=moss)
    fig = FX.figure(name, H, AGED, vis=((1,), (2,), (3,)), t=(0.0, top - 0.005, 0.0), wear=wear)
    vis += fig
    for (hw, y0, y1, z0, z1) in (body, headb):
        cols.append(col(-hw * H, hw * H, top + y0 * H, top + y1 * H, z0 * H, z1 * H, AGED))
    add_all(P, vis + cols)
    P.dim("figure_h", H, H, tol=0.01)
    P.dim("total_h", round(top + H, 3), top + H, tol=0.05)
    P.notes.append("%s on a three-stone pedestal (top %.2f m), figure %.2f m; FX2 sculpted mesh (%s)%s" % (
        kind, top, H, name, ", mossy (aged _w2 + moss)" if moss else ""))
    return P


def G(sfx, display, **kw):
    return M("jp_s_" + sfx, kw.get("mouth", "a"), "intact", display, lambda: guardian(**kw), mount="shrine")


PROPS = [
    {"id": "jp_s_komainu", "cat": "shrine", "mount": "shrine", "per_row": 6,
     "notes": ["IN PAIRS flanking an approach (at the torii foot or before the hall steps): the 'a' (open) on the right "
               "and the 'un' (closed) on the left as one faces the shrine, both facing down the approach, toed in "
               "~15 deg (research/statues/NOTES.md)",
               "style a: the upright form of the references (CMA 106262 / 106263, Met 53190), heavy curls, the un with "
               "a horn; style b: the compact Edo stone form, no horn; _moss: style a weathered (old village shrines)"],
     "models": [
         G("komainu_a_a", "Stone komainu, open mouth (a), upright form", kind="komainu", style="a", mouth="a"),
         G("komainu_a_un", "Stone komainu, closed mouth (un) with horn, upright form", kind="komainu", style="a",
           mouth="un"),
         G("komainu_b_a", "Stone komainu, open mouth (a), compact Edo form", kind="komainu", style="b", mouth="a"),
         G("komainu_b_un", "Stone komainu, closed mouth (un), compact Edo form", kind="komainu", style="b",
           mouth="un"),
         G("komainu_a_a_moss", "Stone komainu (a), upright form, mossy and weathered", kind="komainu", style="a",
           mouth="a", moss=True),
         G("komainu_a_un_moss", "Stone komainu (un), upright form, mossy and weathered", kind="komainu", style="a",
           mouth="un", moss=True),
     ]},
    {"id": "jp_s_kitsune", "cat": "shrine", "mount": "shrine", "per_row": 2,
     "notes": ["Inari shrines only, IN PAIRS like komainu: the fox with the rice-store key and the fox with the jewel; "
               "no stone-fox photo in the open-access sets (proportions from Met 60375 + general knowledge)"],
     "models": [
         G("kitsune_key", "Stone Inari fox with the key in its mouth", kind="kitsune", mouth="key"),
         G("kitsune_jewel", "Stone Inari fox with the jewel in its mouth", kind="kitsune", mouth="jewel"),
     ]},
]
