"""K3 contact sheets: the jobs (render_k3.py <sheet>). One sheet per kit (brief): k3_walls, k3_corridors."""


def _c(build, view, target, dist, persp=30, **kw):
    v = {"build": build, "view": view, "persp": persp, "target": list(target), "dist": dist}
    v.update(kw)
    return v


def _in(build, cam, look, lens=20):
    return {"build": build, "interior": {"cam": list(cam), "look": list(look), "lens": lens}}


def _top(build, target, scale):
    return {"build": build, "view": "top", "target": list(target), "scale": scale}


def _note(names):
    import json
    import os
    jp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "k3_assembly_checks.json")
    if not os.path.isfile(jp):
        return ""
    res = json.load(open(jp, encoding="utf-8"))
    return "Proof checks (parts/k3_assembly_checks.json): " + ", ".join(
        "%s %d/%d" % (n, sum(1 for c in res[n]["checks"] if c["ok"]), len(res[n]["checks"])) for n in names if n in res)


def sheets():
    return {
        "k3_walls": (
            "K3 wall kit: earth / plaster walls, board + bamboo fences, hedges, stone walls, gates, steps, ruins", [
                ("tsuiji_dobei", "tsuiji (battered rammed earth on a stone foot course): plaster + sangawara, bare earth "
                 "(lift lines) + hongawara, suji5 temple lines, neri (tile courses); dobei on cut stones: namako, kuro "
                 "board skirt. Caps are strip roofs with real kawara (rule 1), clay bed, fascia, verge tiles, oni.",
                 _c("case:walls_a", "3q", (9.0, 1.3, 0.0), 11.5)),
                ("tsuiji_close", "tsuiji _earth_hongawara: rammed-earth lifts, foot stones, the hongawara cap (pans + "
                 "round covers, 5-course ridge, rafters under the eave). 615 / 127 / 109 faces per ken.",
                 _c("part:jp_p_wall_site_tsuiji_earth_hongawara", "3q", (0.9, 1.7, 0.0), 5)),
                ("dobei_hikae", "dobei _hikae from the compound side: hikae-bashira buttress posts with two tie beams, "
                 "the cut-stone course, sangawara cap.",
                 _c("part:jp_p_wall_site_dobei_hikae", "back", (1.8, 1.3, -0.3), 7)),
                ("fences", "itabei (plain, kuro with a tile cap), yotsume-gaki (open grid, palm-rope ties), kenninji-gaki "
                 "(split bamboo + battens), shiba-gaki (brushwood), takeho-gaki, ikegaki (clipped hedge).",
                 _c("case:walls_b", "3q", (9.6, 1.0, 0.0), 12)),
                ("stones", "nozura-zumi free-standing (0.9) and retaining (1.8), uchikomi-hagi retaining (1.2), the "
                 "stone-toed earth bank, a tall ikegaki. Individual stones (rule 3); earth fill behind a revetment.",
                 _c("case:stones", "3q", (7.0, 0.9, 0.0), 9.5)),
                ("gates", "kabuki-mon (open), kabuki-mon roofed, mune-mon (hongawara), wicket doors in itabei, dobei, "
                 "kenninji (1.04 x 1.96 clear: D1 / D2). Hinged leaves swing into the compound (engine-untested).",
                 _c("case:gates", "3q", (12.0, 1.7, 0.0), 14)),
                ("wicket_open", "wicket _dobei with the leaf open (compound side): one hinged leaf, jambs, lintel, the "
                 "cap running on over the door.", dict(_c("part:jp_p_gate_wicket_dobei", "back", (0.9, 1.3, 0.0), 6),
                                                         open=1.0)),
                ("compound", "PROOF compound_corner: tsuiji L with a mitred corner (cap hip outside, valley inside), a "
                 "roofed kabuki-mon in the run, an inner itabei with a wicket. 24/24 checks.",
                 _c("k3:compound_corner", "3q", (5.0, 1.5, 5.0), 17)),
                ("compound_top", "compound_corner from above: the corner cap cell, the gate roof, the wall line closed "
                 "except at the gates (KW1).", _top("k3:compound_corner", (5.2, 0.0, 4.6), 14.5)),
                ("slope", "PROOF slope_fences: ikegaki, yotsume, kenninji climbing 0.30 steps (step pieces between level "
                 "modules; footings / Geometry 0.30-0.40 under grade close the steps, KW2). 19/19.",
                 _c("k3:slope_fences", "3q", (4.5, 1.0, -2.0), 11)),
                ("steps", "Terrain-step pieces: tsuiji +0.30 / +0.60 (flush gable cap ends, the riser, footing down to "
                 "the lower grade), dobei namako +0.30, kuro itabei with a tile cap +0.30.",
                 _c("case:steps", "3q", (5.6, 1.4, 0.0), 10)),
                ("abandoned", "Dead world: collapsed tsuiji (stubs, mound, shards), fallen cap tiles (bed shows), "
                 "overgrown earth wall, leaning itabei, broken yotsume, overgrown hedge, collapsed revetment.",
                 _c("case:walls_ab", "3q", (11.8, 1.1, 0.0), 14.5)),
            ], ["k3_compound_corner", "k3_slope_fences"]),
        "k3_corridors": (
            "K3 covered-corridor (watari-roka) + kairo kit: one strip-roof engine, corners / T / cross, stairs, connector",
            [
                ("court", "PROOF corridor_court: two stand-in halls (B 0.455 higher) linked round a courtyard: "
                 "connectors at both walls, two corners, a covered stair; sangawara; outer side plaster + renji. 24/24.",
                 _c("k3:corridor_court", "3q", (1.5, 2.0, 4.5), 23)),
                ("court_top", "corridor_court from above: valleys inside and hips outside at both corners, the stepped "
                 "roof at the stair, both connectors tucked under the hall eaves (KW7 connector_fit).",
                 _top("k3:corridor_court", (1.4, 0.0, 4.6), 17.5)),
                ("court_inside", "Inside the corridor (eye 1.6 m): board floor (Roadway continuous hall to hall, KW3), "
                 "koran rail on the court side, plaster + renji window outside, rafters + sheathing overhead.",
                 _in("k3:corridor_court", (1.4, 2.05, 0.25), (6.8, 2.0, 0.0))),
                ("stair_inside", "The covered stair (rise 0.455 over 1 ken: 6 risers, ramp 26.6 deg <= 38): the head tie "
                 "and roof at the upper level; head room >= 2.05 everywhere (KW5).",
                 _in("k3:corridor_court", (7.25, 2.05, 2.4), (7.3, 2.5, 8.2))),
                ("connector", "Connector at hall A: the corridor roof ends plain at the hall's wall face with a flashing "
                 "board, ridge under the hall eave (margin %s); floor flush with the hall's threshold.",
                 _c("k3:corridor_court", "back", (0.4, 2.4, 0.0), 8)),
                ("junctions", "Corner (itabuki), T (sangawara), cross (hongawara) and a hipped end: hips outside, "
                 "valleys inside (valley tiles / boards), ridges cut round each other.",
                 _c("case:roka_tx", "3q", (7.4, 1.8, 0.0), 13)),
                ("corner_top", "jp_p_roka_corner_open_sangawara from above: tile field clipped on the hip and valley, "
                 "the valley lining, the corner ridges.", _top("part:jp_p_roka_corner_open_sangawara", (0.4, 0.0, -0.4),
                                                               4.6)),
                ("sides", "Side kinds: open (koran), half (board koshi + cap), enclosed (plaster + renji + wainscot), "
                 "board (+ renji), blank; and _ab_decay (boards and rail pieces gone).",
                 _c("case:roka_sides", "3q", (13.3, 1.5, 0.0), 22)),
                ("sori", "Curved (sori) roofs: kokera, hongawara, hiwada (W2P2's profile; planar d-bands so hips and "
                 "valleys stay shared).", _c("case:roka_sori", "3q", (9.0, 2.0, 0.0), 15)),
                ("kairo", "PROOF kairo_segment: cloister turning a corner, curved hongawara, outer side plaster + renji, "
                 "inner side open to the court. 22/22.", _c("k3:kairo_segment", "3q", (5.0, 1.8, 2.0), 14)),
                ("kairo_court", "The kairo from the court side (inner side open).",
                 _c("k3:kairo_segment", "3q_left", (4.5, 1.8, 1.5), 13)),
                ("kairo_inside", "Inside the kairo: renji windows in the outer wall, the curved rafters and the corner "
                 "valley overhead.", _in("k3:kairo_segment", (1.0, 2.05, 0.3), (7.3, 2.3, 0.5))),
            ], ["k3_corridor_court", "k3_kairo_segment"]),
    }
