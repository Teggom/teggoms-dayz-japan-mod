"""Material table for the Japanese building kit.

Every visual material maps to one texture set in JP\\structures\\data\\ (<tex>_co/_nohq/_smdi.paa + <tex>.rvmat).
The PNG sources are made by tools/make_textures.py from CC0 Poly Haven maps (see CREDITS.md) or procedurally.
"""

DATA_P3D = "JP\\structures\\data\\"          # P:-relative, as written into the p3d (no leading backslash)

# name: tex = texture set, scale = metres per tile (world UVs), grain = 'long' puts the texture's v axis along
# the solid's longest edge (timber), fire = default penetration material for Fire Geometry.
MATS = {
    "plaster_white": {"tex": "jp_plaster_white", "scale": 2.0, "fire": "dirt"},
    "plaster_earth": {"tex": "jp_plaster_earth", "scale": 2.0, "fire": "dirt"},
    "timber":        {"tex": "jp_timber_dark", "scale": 1.13, "grain": "long", "fire": "wood"},
    "boards_floor":  {"tex": "jp_boards_floor", "scale": 1.89, "fire": "wood"},
    "boards_ext":    {"tex": "jp_boards_ext", "scale": 2.0, "fire": "wood"},
    "kawara":        {"tex": "jp_kawara", "scale": 3.0, "fire": "pottery"},
    "kawara_ridge":  {"tex": "jp_kawara", "scale": 1.5, "fire": "pottery"},
    "tatami":        {"tex": "jp_tatami", "scale": 1.8, "fire": "wood"},
    "doma":          {"tex": "jp_doma", "scale": 2.0, "fire": "dirt"},
    "stone":         {"tex": "jp_stone", "scale": 1.9, "fire": "granite"},
    "shoji":         {"tex": "jp_shoji", "scale": 1.0, "fire": "fabric_thin"},
    "fusuma":        {"tex": "jp_fusuma", "scale": 1.0, "fire": "fabric_thin"},
    "plank_door":    {"tex": "jp_plankdoor", "scale": 1.0, "fire": "wood"},
    "koshi":         {"tex": "jp_koshi", "scale": 0.9, "fire": "wood"},
    "mushiko":       {"tex": "jp_mushiko", "scale": 0.9, "fire": "dirt"},
    "tansu":         {"tex": "jp_tansu", "scale": 1.0, "fire": "wood"},
    "ash":           {"tex": "jp_ash", "scale": 1.0, "fire": "dirt"},
}

# Blender preview colours (only used if a PNG is missing)
PREVIEW = {
    "plaster_white": (0.85, 0.84, 0.80), "plaster_earth": (0.55, 0.42, 0.28), "timber": (0.16, 0.10, 0.07),
    "boards_floor": (0.62, 0.45, 0.28), "boards_ext": (0.30, 0.29, 0.27), "kawara": (0.22, 0.23, 0.24),
    "kawara_ridge": (0.22, 0.23, 0.24), "tatami": (0.62, 0.58, 0.40), "doma": (0.42, 0.33, 0.22),
    "stone": (0.45, 0.45, 0.44), "shoji": (0.92, 0.90, 0.84), "fusuma": (0.80, 0.74, 0.60),
    "plank_door": (0.25, 0.18, 0.12), "koshi": (0.18, 0.12, 0.08), "mushiko": (0.8, 0.8, 0.78),
    "tansu": (0.28, 0.16, 0.09), "ash": (0.35, 0.33, 0.31),
}

# Roadway surfaces (vanilla dz\surfaces\data\roadway\*.paa decide footstep sound and surface type)
ROADWAY = {
    "doma": "dz\\surfaces\\data\\roadway\\dirt_int.paa",
    "tatami": "dz\\surfaces\\data\\roadway\\textile_carpet_int.paa",
    "boards": "dz\\surfaces\\data\\roadway\\wood_planks_int.paa",
    "stair": "dz\\surfaces\\data\\roadway\\wood_planks_stairs_int.paa",
    "stone_ext": "dz\\surfaces\\data\\roadway\\stone_ext.paa",
}


def tex_path(mat):
    return DATA_P3D + MATS[mat]["tex"] + "_co.paa"


def rvmat_path(mat):
    return DATA_P3D + MATS[mat]["tex"] + ".rvmat"


def fire_rvmat(fire):
    return "dz\\data\\data\\penetration\\%s.rvmat" % fire
