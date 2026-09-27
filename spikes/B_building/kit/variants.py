"""The buildings this kit produces. Each entry is a parameter set for jpkit.machiya.generate()."""

VARIANTS = {
    # the spike building: 2 storeys, 4 x 6 ken, toriniwa on the east (+x) side, 3 rooms, box stair, 7 sliding doors
    "jp_machiya_01": {
        "name": "jp_machiya_01",
        "class": "Land_JP_Machiya_01",
        "display": "Machiya (town house)",
    },
    # kit proof: 1 storey, 3 x 4 ken, earth plaster, toriniwa on the west side, 2 rooms, no stair
    "jp_machiya_02": {
        "name": "jp_machiya_02",
        "class": "Land_JP_Machiya_02",
        "display": "Machiya, single storey",
        "width_ken": 3.0,
        "depth_ken": 4.0,
        "storeys": 1,
        "toriniwa_side": "west",
        "rooms": [
            {"ken": 2.0, "floor": "tatami", "toriniwa_door": True},
            {"ken": 2.0, "floor": "boards", "toriniwa_door": True, "irori": True, "window_back": True},
        ],
        "link_doors": [True],
        "roof_pitch": 0.50,
        "eave_overhang": 0.75,
        "hisashi": False,
        "walls": "earth",
        "kamado": False,
        "mass": 30000.0,
    },
}
