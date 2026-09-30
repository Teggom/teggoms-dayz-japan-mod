"""C3 render jobs (spikes/C3/render_c3.py): (out, caption, spec) per sheet; cameras in the MODEL frame of the key
(x, y up, z = front), or scene frame (world - the scene origin) for 'street' / 'hamlet'."""

K = "Kura (DW22, 3 x 2 ken, two floors): "
JOBS = {
    "kura": [
        ("kura_namako_3q", K + "Land_JP_Kura_Namako: diagonal namako on the front and gables, plastered eave bands and "
         "soffit, the door with its stepped surround, static open plaster leaves and tile pent, stone landing + step.",
         {"key": "kura_namako", "view": "3q"}),
        ("kura_namako_back", K + "Land_JP_Kura_Namako from the back: plain plaster with a grime band, the small ground "
         "window, the gable window and vent upstairs.", {"key": "kura_namako", "view": "back"}),
        ("kura_kuro_3q", K + "Land_JP_Kura_Kuro_Hinged: black lapped boards (shitami) on the lower walls, the plaster "
         "door leaves as ROTATION doors (engine test), hinged window shutters.", {"key": "kura_kuro_hinged", "view": "3q"}),
        ("kura_kuro_shut", K + "Land_JP_Kura_Kuro_Hinged with every door shut (outer leaves closed over the doorway).",
         {"key": "kura_kuro_hinged", "cam": [3.6, 1.7, 6.8], "look": [0.0, 1.8, 1.8], "lens": 22, "open": 0.0,
          "fill": False}),
        ("kura_plain_3q", K + "Land_JP_Kura_Plain: plain plaster with grime bands (rural / cheap).",
         {"key": "kura_plain", "view": "3q"}),
        ("kura_in_ground", K + "Ground floor from the door: boards on the footing, interior plaster (shikkui_int), "
         "the open stair (jp_p_stair _open) along the back wall up to the upper floor.",
         {"key": "kura_namako", "cam": [1.9, 2.05, 1.45], "look": [-1.2, 1.5, -1.3], "lens": 13, "open": 1.0}),
        ("kura_in_upper", K + "Upper floor: the stairwell with its rim and guard rail, the ridge beam and purlins, the "
         "gable windows (bars) and vent.", {"key": "kura_namako", "cam": [2.3, 4.45, 1.2], "look": [-1.4, 3.6, -0.9],
                                              "lens": 13}),
        ("kura_cut", K + "Cut at 4.6 m: the upper floor from above, the stairwell over the flight.",
         {"key": "kura_namako", "view": "3q", "cut_y": 4.6}),
    ],
}
SHEETS = {
    "kura": ("C3 kura (DW22): three shells, two floors by stair", "", 4, 480, 360, 76, 58),
}
