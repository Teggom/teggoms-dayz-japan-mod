#!/usr/bin/env python3
r"""build_materials.py - regenerate the jp_common material library, its checks, the swatch wall and the contact sheets.

  python build_materials.py [--no-render] [--no-binarize] [--no-pack] [--sheets-only] [--only ID[,ID...]]
  python build_materials.py --rvmats-only [--no-pack]

  --rvmats-only (G3 fix 2, 2026-09-29): rewrite every library rvmat and the plaque rvmat from SPEC / FINISH (no
  textures, no matcheck), then repack. make_part_materials.py and make_fix_materials.py take the same flag for theirs.

  --only (parts agent, 2026-09-27): regenerate just these materials (textures, PAAs, rvmats, sidecars), then run
  matcheck over the whole library, repack and refresh the sheets; the swatch wall is not rebuilt (it references the
  library by path).

Steps (one run, everything from sources):
  1. fetch_sources.py  : CC0 Poly Haven maps -> data/materials/polyhaven (skipped when present)
  2. make_textures.py  : 22 materials x 3 wear levels -> data/materials/textures/*.png (+ detail masks)
  3. ImageToPAA        : -> src/JP/common/materials/<family>/jp_m_<name>_w<n>_{co,nohq,smdi}.paa
  4. rvmat per wear level (B's proven Super-shader layout, library paths) + one sidecar jp_m_<name>.json per material
  5. matcheck (C1)     : PNG sources and the shipped PAAs -> src/JP/common/materials/checks.json; FAIL stops the build
  6. swatch wall       : plaque atlas + MLOD p3d (Res 1-3, Geometry, View, Fire) -> binarize (cwd P:\) -> ODOL in src
  7. config.cpp (CfgPatches JP_Common, Land_JP_Swatch_Wall), CfgConvert check, pack @Japan\addons\jp_common.pbo
  8. test/placements/M.csv (terrain-baked swatch wall)
  9. contact sheets    : Blender sphere renders + flat tiles -> research/materials/contact_sheets/*.jpg
Never starts or stops the server or any GUI program.
"""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(DEV, ".."))
SRC = os.path.join(DEV, "src", "JP", "common")
MATDIR = os.path.join(SRC, "materials")
SWDIR = os.path.join(SRC, "swatch")
DATA = os.path.join(DEV, "data", "materials")
TEX = os.path.join(DATA, "textures")
BUILD = os.path.join(DATA, "_build")
SHEETS = os.path.join(HERE, "contact_sheets")
TOOLS = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin"
IMAGE_TO_PAA = os.path.join(TOOLS, "ImageToPAA", "ImageToPAA.exe")
BINARIZE = os.path.join(TOOLS, "Binarize", "binarize.exe")
CFGCONVERT = os.path.join(TOOLS, "CfgConvert", "CfgConvert.exe")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
PBO_OUT = os.path.join(ROOT, "@Japan", "addons", "jp_common.pbo")
FONT = r"C:\Windows\Fonts\arial.ttf"
FONTB = r"C:\Windows\Fonts\arialbd.ttf"

sys.path[:0] = [HERE, os.path.join(DEV, "tools", "common"), os.path.join(DEV, "tools", "matcheck")]
import make_textures as MT  # noqa: E402
import matcheck  # noqa: E402
import mlod_mat as mlod  # noqa: E402

ORDER = list(MT.RECIPES)                     # swatch column numbers 1..22 follow materials_needed.json
WEARS = [("_w0", "clean"), ("_w1", "normal"), ("_w2", "heavy")]
SHORT = {
    "jp_m_wood_weathered": "wood weathered", "jp_m_wood_street_dark": "wood street dark",
    "jp_m_wood_bengara": "wood bengara", "jp_m_wood_kuro": "wood kuro (black)", "jp_m_wood_sooted": "wood sooted",
    "jp_m_wall_arakabe": "earth arakabe", "jp_m_wall_nakanuri": "earth nakanuri", "jp_m_wall_shikkui": "shikkui plaster",
    "jp_m_wall_namako_tile": "namako tile", "jp_m_roof_kawara": "kawara tile", "jp_m_roof_thatch": "thatch",
    "jp_m_roof_thatch_cut": "thatch cut face", "jp_m_roof_kureita": "kureita boards", "jp_m_roof_kokera": "kokera shingle",
    "jp_m_roof_kakigara": "kakigara shells", "jp_m_stone_field": "field stone", "jp_m_stone_cut": "cut granite",
    "jp_m_stone_river": "river stone", "jp_m_paper_shoji": "shoji paper", "jp_m_bamboo_weathered": "bamboo",
    "jp_m_metal_iron": "iron", "jp_m_straw_mushiro": "mushiro straw mat",
}
# plain words from BUILD_LIST.md (parts in materials_needed.json used_by)
USED_ON = {
    "jp_m_wood_weathered": "The default outdoor timber of every tier: posts, beams, sills and plank walls; plank doors, "
                           "storm shutters and shutter boxes; verandas and open decks; eave rafters, bargeboards, gable "
                           "framing and board wainscots; battens on stone-weighted roofs.",
    "jp_m_wood_street_dark": "Dark street fronts of post-town and town houses (tier 2-3): lattice fronts and lattice "
                             "doors, shop shutters and fold-down benches, front posts, cantilevered eave beams, lapped "
                             "horizontal boards.",
    "jp_m_wood_bengara": "Red-brown bengara lattice on Kamigata shop fronts, tier 2-3. Restricted: use sparingly.",
    "jp_m_wood_kuro": "Black lapped lower boards on kura storehouses. Restricted.",
    "jp_m_wood_sooted": "Soot-blackened timber inside smoke vents and smoke hoods (the soot halo outside is weathering).",
    "jp_m_wall_arakabe": "Rough earth walls of poor and village houses (tier 1-2): walls between exposed posts, farmhouse "
                         "gables.",
    "jp_m_wall_nakanuri": "Smoother second-coat earth walls between exposed posts on better tier 2 houses.",
    "jp_m_wall_shikkui": "White lime plaster, tier 3: kura walls and doors, plastered town fronts, the low upper storey "
                         "with mushiko windows, udatsu fire walls, plastered kura eaves, gables, namako joints and the "
                         "mortar of tile ridges.",
    "jp_m_wall_namako_tile": "The dark square tiles of namako walls on kura lower walls (the white joints are separate "
                             "plaster geometry).",
    "jp_m_roof_kawara": "Every fired-clay roof tile (tier 2-3): sangawara field, eave and verge tiles, stacked ridges and "
                        "end tiles, hongawara, pent roofs, kura roofs and windows, udatsu caps, tiled thatch ridges.",
    "jp_m_roof_thatch": "Thatch roof surface of farmhouses (tier 1-2): roof field, hips and verges, smoke hoods, thatch "
                        "ridges.",
    "jp_m_roof_thatch_cut": "The squared-off cut face of thick thatch at the eaves (about 0.6 m thick).",
    "jp_m_roof_kureita": "Stone-weighted split-board roofs of Kiso post towns and mountain and coast villages (tier 1-2); "
                         "board ridges; board pent roofs.",
    "jp_m_roof_kokera": "Thin shingle roofs: Edo townhouses before tile, back-alley tenements, tier 2 houses and sheds.",
    "jp_m_roof_kakigara": "Oyster-shell-strewn shingle roofs, the Edo-side tier 3 variant (G1 decision 3).",
    "jp_m_stone_field": "Rounded field stones under the posts of rural houses and verandas; natural step stones; stones "
                        "in the under-floor zone.",
    "jp_m_stone_cut": "Cut granite: the stone course under town-house sills, kura footings, cut steps and threshold stones.",
    "jp_m_stone_river": "River stones that hold down board roofs (ishioki), on board ridges and board pent roofs.",
    "jp_m_paper_shoji": "Paper of exterior shoji: the board-bottomed doors of tenements and doma entrances, shoji behind "
                        "verandas.",
    "jp_m_bamboo_weathered": "Bamboo bars in barred windows, eave soffit poles, split-bamboo gutters and downpipes, "
                             "battens on shingle roofs, bamboo on thatch ridges.",
    "jp_m_metal_iron": "Iron fittings: kura door and window hardware and bars, hooks on plank doors, shutters and gutters.",
    "jp_m_straw_mushiro": "The rolled straw mat hung over the doorway of the poorest tier 1 houses.",
}
# rvmat specular, specularPower (w1; w0 x1.1, w2 x0.8)
# G3 fix 2 (2026-09-29): the effective sun specular is specular x SMDI green. Vanilla matte wood sits at about 0.01-0.02
# (misc_bench* 0.27 x 0.05, misc_deerstand1_wood* 0.27 x 0.00-0.07, logs 0.5 x 0). Five matte materials were 2-3x that
# and were lowered (texture untouched): wood_street_dark 0.35 -> 0.15 (x SMDI 0.13), wood_bengara 0.3 -> 0.15 (x 0.15),
# bamboo 0.35 -> 0.2 (x 0.10), roof_kakigara 0.3 -> 0.2 (x 0.09), stone_river 0.3 -> 0.2 (x 0.08).
SPEC = {
    "jp_m_wood_weathered": (0.2, 40), "jp_m_wood_street_dark": (0.15, 60), "jp_m_wood_bengara": (0.15, 50),
    "jp_m_wood_kuro": (0.25, 40), "jp_m_wood_sooted": (0.15, 25), "jp_m_wall_arakabe": (0.1, 20),
    "jp_m_wall_nakanuri": (0.12, 25), "jp_m_wall_shikkui": (0.15, 30), "jp_m_wall_namako_tile": (0.35, 60),
    "jp_m_roof_kawara": (0.6, 90), "jp_m_roof_thatch": (0.08, 15), "jp_m_roof_thatch_cut": (0.08, 15),
    "jp_m_roof_kureita": (0.2, 35), "jp_m_roof_kokera": (0.2, 35), "jp_m_roof_kakigara": (0.2, 50),
    "jp_m_stone_field": (0.25, 40), "jp_m_stone_cut": (0.25, 40), "jp_m_stone_river": (0.2, 50),
    "jp_m_paper_shoji": (0.08, 20), "jp_m_bamboo_weathered": (0.2, 60), "jp_m_metal_iron": (0.5, 70),
    "jp_m_straw_mushiro": (0.1, 20),
}
ROADWAY = {"wood": "wood_planks_ext", "stone": "stone_ext", "straw": "textile_carpet_ext"}
ROADWAY_BY_ID = {"jp_m_roof_kawara": "ceramic_tiles_roof_ext", "jp_m_roof_thatch": "grass_dry_ext",
                 "jp_m_roof_kureita": "wood_planks_ext", "jp_m_roof_kokera": "wood_planks_ext",
                 "jp_m_roof_kakigara": "gravel_small_ext", "jp_m_wood_bengara": "wood_planks_ext"}
SOURCES = {
    "jp_m_wood_weathered": ["weathered_planks"], "jp_m_wood_street_dark": ["japanese_cedar_planks"],
    "jp_m_wood_bengara": ["japanese_cedar_planks"], "jp_m_wood_kuro": ["black_painted_planks"],
    "jp_m_wood_sooted": ["japanese_cedar_planks"], "jp_m_wall_arakabe": ["clay_plaster"],
    "jp_m_wall_nakanuri": ["clay_plaster"], "jp_m_wall_shikkui": ["white_plaster_02"], "jp_m_roof_thatch": ["reed_roof_04"],
    "jp_m_roof_kureita": ["wood_planks_grey"], "jp_m_roof_kokera": ["wood_planks_grey"],
    "jp_m_roof_kakigara": ["wood_planks_grey"], "jp_m_stone_field": ["worn_rock_natural_01"],
    "jp_m_stone_cut": ["rock_surface"], "jp_m_stone_river": ["seaside_rock"], "jp_m_metal_iron": ["rust_coarse_01"],
}
GROUPS = [("1_wood", "Wood", ORDER[0:5]), ("2_walls", "Walls", ORDER[5:9]), ("3_roofs", "Roofs", ORDER[9:15]),
          ("4_stone", "Stone", ORDER[15:18]), ("5_paper_bamboo_iron_straw", "Paper, bamboo, iron, straw", ORDER[18:22])]

RVMAT = """ambient[]={1,1,1,1};
diffuse[]={1,1,1,1};
forcedDiffuse[]={0,0,0,0};
emmisive[]={0,0,0,1};
specular[]={%(s)g,%(s)g,%(s)g,1};
specularPower=%(p)d;
PixelShaderID="Super";
VertexShaderID="Super";
""" + "".join("""class Stage%d
{
	texture="%%(t%d)s";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
""" % (k, k) for k in range(1, 8))
STAGES = {2: "#(argb,8,8,3)color(0.5,0.5,0.5,1,DT)", 3: "#(argb,8,8,3)color(0,0,0,0,MC)",
          4: "#(argb,8,8,3)color(1,1,1,1,AS)"}
# Stage6 (fresnel) + Stage7 (environment map) per finish. G3 fix 2 (2026-09-29, Stephen: "every material is too
# reflective"; interior clay went green at glancing angles with the normal-map swirls in the sheen, although its SMDI
# specular is only ~0.01). Until then every rvmat used fresnel(1.3,0.7) + the outdoor (green) env_land_co.paa.
# The vanilla analogues, read from P:\DZ (PLAYBOOK §15 T12):
#   wall   : vanilla house plaster walls use the Multi shader, which has NO environment map at all (177 of 177 rvmats
#            that use dz\structures\data\plaster\*); vanilla Super walls (dz\structures\walls\data\wall_*.rvmat) use
#            #(ai,32,128,1)fresnel(0.49,0.14). -> that fresnel + a black env.
#   matte  : vanilla matte Super wood / straw / plinth rvmats (industrial\misc\data\planks.rvmat, logs*.rvmat,
#            slama.rvmat, stoh_slama.rvmat, podezdivka_beton.rvmat, misc_deerstand1_wood*.rvmat, 65 in all) use
#            #(ai,32,128,1)fresnel(0.01,0.01) + a black env #(argb,8,8,3)color(0,0,0,1,CO): no env reflection.
#   glossy : fired / glazed ceramic and iron keep the env map (vanilla glazed tiles houvev_*_kitchentiles fresnel(1.42,0),
#            metal_white_lightrust fresnel(1.3,2.83), both with env_land_co). Only kawara (ibushi, silvered), namako
#            tile and iron are glossy; Stephen passed the roof as is, so their Stage6/7 are unchanged.
ENV_LAND = "dz\\data\\data\\env_land_co.paa"
ENV_NONE = "#(argb,8,8,3)color(0,0,0,1,CO)"
FINISH = {
    "wall": ("#(ai,32,128,1)fresnel(0.49,0.14)", ENV_NONE),
    "matte": ("#(ai,32,128,1)fresnel(0.01,0.01)", ENV_NONE),
    "glossy": ("#(ai,64,64,1)fresnel(1.3,0.7)", ENV_LAND),
}
FINISH_BY_ID = {"jp_m_roof_kawara": "glossy", "jp_m_roof_kawara_field": "glossy", "jp_m_roof_kawara_far": "glossy",
                "jp_m_wall_namako_tile": "glossy", "jp_m_metal_iron": "glossy"}


def finish_for(mid):
    """'glossy' for the listed ceramics / iron, 'wall' for earth and plaster walls, 'matte' for everything else."""
    if mid in FINISH_BY_ID:
        return FINISH_BY_ID[mid]
    return "wall" if mid.startswith("jp_m_wall_") else "matte"


def wb(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def fam(mid):
    return MT.MATS[mid]["family"]


def ppath(mid, wear, suf):
    """P:-relative library path (no leading backslash), as written into p3ds and rvmats."""
    return "JP\\common\\materials\\%s\\%s%s%s" % (fam(mid), mid, wear, suf)


def rvmat_text(nohq, smdi, s, p, finish="matte"):
    t = dict(("t%d" % k, v) for k, v in STAGES.items())
    t.update(t1=nohq, t5=smdi, s=s, p=p, t6=FINISH[finish][0], t7=FINISH[finish][1])
    return RVMAT % t


def write_rvmats(only=None):
    """The library rvmats only (no textures): 3 wear levels per material, specular x1.1 / x1.0 / x0.8."""
    for mid in (only or ORDER):
        s, p = SPEC[mid]
        for k, (wear, _) in enumerate(WEARS):
            f = [1.1, 1.0, 0.8][k]
            wb(os.path.join(MATDIR, fam(mid), mid + wear + ".rvmat"),
               rvmat_text(ppath(mid, wear, "_nohq.paa"), ppath(mid, wear, "_smdi.paa"), round(s * f, 3), int(p * f),
                          finish_for(mid)))


def write_plaque_rvmat():
    wb(os.path.join(SWDIR, "data", "jp_swatch_plaques.rvmat"),
       rvmat_text("#(rgb,8,8,3)color(0.5,0.5,1,1,NOHQ)", "#(argb,8,8,3)color(1,0.05,0.05,1,SMDI)", 0.05, 10, "matte"))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace", **kw)


# ----------------------------------------------------------------------------------------------------------------
def to_paa(pairs):
    todo = [(png, paa) for png, paa in pairs if not (os.path.isfile(paa) and os.path.getmtime(paa) >= os.path.getmtime(png))]

    def one(pp):
        png, paa = pp
        os.makedirs(os.path.dirname(paa), exist_ok=True)
        r = run([IMAGE_TO_PAA, png, paa])
        if r.returncode != 0 or not os.path.isfile(paa):
            raise RuntimeError("ImageToPAA failed for %s: %s" % (png, (r.stdout + r.stderr).strip()))
        return paa
    with cf.ThreadPoolExecutor(6) as ex:
        list(ex.map(one, todo))
    print("paa: %d converted, %d up to date" % (len(todo), len(pairs) - len(todo)))


def library(info, only=None):
    pairs = []
    for mid in (only or ORDER):
        for wear, _ in WEARS:
            for suf in ("_co", "_nohq", "_smdi"):
                pairs.append((os.path.join(TEX, mid + wear + suf + ".png"),
                              os.path.join(MATDIR, fam(mid), mid + wear + suf + ".paa")))
    to_paa(pairs)
    man = json.load(open(os.path.join(DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    write_rvmats(only)
    for mid in (only or ORDER):
        m = MT.MATS[mid]
        wears = {}
        for k, (wear, name) in enumerate(WEARS):
            i = info.get(mid, [{}] * 3)[k]
            wears[wear] = {"name": name, "look": m["wear"][wear], "co": ppath(mid, wear, "_co.paa"),
                           "rvmat": ppath(mid, wear, ".rvmat"), "target_srgb": i.get("target_srgb"),
                           "masked_frac": i.get("masked_frac")}
        side = {
            "id": mid, "family": fam(mid), "palette_id": m["palette_id"],
            "palette_by_wear": MT.PALETTE_BY_WEAR.get(mid, {}), "tile_size_m": m["tile_size_m"],
            "texture_px": MT.size_for(m["tile_size_m"]),
            "px_per_m": round(MT.size_for(m["tile_size_m"]) / m["tile_size_m"], 1),
            "uv": "world-scale: u, v = metres / tile_size_m; v runs down the texture = along the grain / down-slope",
            "grain": m["grain"],
            "penetration_rvmat": "dz\\data\\data\\penetration\\%s.rvmat" % m["penetration_rvmat"],
            "roadway_surface": ("dz\\surfaces\\data\\roadway\\%s.paa" % (ROADWAY_BY_ID.get(mid) or ROADWAY.get(fam(mid))))
            if (ROADWAY_BY_ID.get(mid) or ROADWAY.get(fam(mid))) else None,
            "wear": wears, "used_by": m["used_by"], "used_on": USED_ON[mid],
            "sources": [{"asset": a, "name": man[a]["name"], "page": man[a]["page"], "licence": "CC0 1.0",
                         "authors": man[a]["authors"]} for a in SOURCES.get(mid, [])] or [{"procedural": "make_textures.py"}],
            "normal_convention": "DirectX (green = down), like the machiya v1 maps; make_textures.GREEN_DX flips all",
            "made_by": "research/materials/build_materials.py (materials agent, 2026-09-27)",
        }
        if mid == "jp_m_wall_namako_tile":
            side["note"] = "4 x 4 tiles of 0.2275 m per 0.91 m tile, square to the UVs; rotate the UVs 45 deg for diagonal namako."
        if mid == "jp_m_roof_kawara":
            side["note"] = ("A ceramic surface, not a tile pattern (rule 1: the tiles are geometry). W8 per-tile tint: "
                            "give each tile a random UV offset.")
        wb(os.path.join(MATDIR, fam(mid), mid + ".json"), json.dumps(side, indent=1, ensure_ascii=False))
    print("library: %d materials, %d rvmats, sidecars written" % (len(ORDER), 3 * len(ORDER)))


def checks():
    pal = matcheck.load_palette()
    res = []
    for mid in ORDER:
        for wear, _ in WEARS:
            png = os.path.join(TEX, mid + wear + "_co.png")
            paa = os.path.join(MATDIR, fam(mid), mid + wear + "_co.paa")
            pid = MT.PALETTE_BY_WEAR.get(mid, {}).get(wear) or MT.MATS[mid]["palette_id"]
            a = matcheck.check(png, pal, pid, TEX)
            b = matcheck.check(paa, pal, None, TEX)                # sidecar route, the way other agents will run it
            a["shipped_paa"] = {k: b.get(k) for k in ("mean_srgb", "dE", "verdict", "warnings")}
            if b["verdict"] == "FAIL":
                a["verdict"] = "FAIL"
            res.append(a)
    wb(os.path.join(MATDIR, "checks.json"), json.dumps({"check": "C1 palette (tools/matcheck)", "results": res}, indent=1))
    nf = [r for r in res if r["verdict"] == "FAIL"]
    nw = [r for r in res if r["verdict"] == "WARN"]
    for r in res:
        print("  %-4s %-30s %-17s mean %-15s dE %4.1f/%-2g  paa dE %4.1f  %s" % (
            r["verdict"], os.path.basename(r["file"])[:-7], r["palette_id"], "(%d,%d,%d)" % tuple(r["mean_srgb"]),
            r["dE"], r["tol"], r["shipped_paa"]["dE"], "; ".join(r["warnings"])))
    print("matcheck: %d sets, %d FAIL, %d WARN" % (len(res), len(nf), len(nw)))
    return res


# ----------------------------------------------------------------------------------------------------------------
# swatch wall
# ----------------------------------------------------------------------------------------------------------------
P_ = 1.2          # panel size
G_ = 0.1          # gap
NCOL = len(ORDER) + 1                     # + the row-label column at the left
W_ = NCOL * P_ + (NCOL + 1) * G_          # 30.0 m
ROWS_Y = {"_w2": 1.0, "_w1": 1.0 + P_ + G_, "_w0": 1.0 + 2 * (P_ + G_)}   # bottom of each row
TOP = 1.0 + 3 * P_ + 2 * G_ + G_          # 4.9 m
PLQ = (0.30, 0.80)                        # plaque band (y)
BACK_Z = -0.25
ATLAS = (4, 8)                            # atlas cells (cols, rows), 256 x 128 px each
PLAQUE_TEX = "JP\\common\\swatch\\data\\jp_swatch_plaques_co.paa"
PLAQUE_MAT = "JP\\common\\swatch\\data\\jp_swatch_plaques.rvmat"


def col_x(c):
    """Column c (0 = label column, 1..22 materials) -> (x_left_as_seen, x_right_as_seen) in model x.
    Seen from the front (+z) model +x is on the viewer's LEFT, so column 0 sits at +x."""
    xl = W_ / 2 - G_ - c * (P_ + G_)
    return xl, xl - P_


def plaque_atlas():
    cw, chh = 256, 128
    im = Image.new("RGB", (ATLAS[0] * cw, ATLAS[1] * chh), (60, 52, 44))
    d = ImageDraw.Draw(im)
    fb, fn, fs = ImageFont.truetype(FONTB, 62), ImageFont.truetype(FONTB, 25), ImageFont.truetype(FONT, 22)
    cells = [("%d" % (i + 1), SHORT[m]) for i, m in enumerate(ORDER)]
    cells += [("w0", "clean"), ("w1", "normal"), ("w2", "heavy"), ("jp_common", "swatch 2026-09-27")]
    for k, (big, small) in enumerate(cells):
        x0, y0 = (k % ATLAS[0]) * cw, (k // ATLAS[0]) * chh
        d.rectangle([x0 + 3, y0 + 3, x0 + cw - 4, y0 + chh - 4], fill=(182, 170, 146), outline=(40, 34, 28), width=4)
        f = fb if len(big) <= 3 else fn
        d.text((x0 + cw / 2, y0 + 48), big, fill=(28, 24, 20), font=f, anchor="mm")
        d.text((x0 + cw / 2, y0 + 100), small, fill=(28, 24, 20), font=fs, anchor="mm")
    return im, {c: k for k, c in enumerate([c[0] for c in cells])}


def atlas_uv(k):
    cx, cy = k % ATLAS[0], k // ATLAS[0]
    return cx / ATLAS[0], (cx + 1) / ATLAS[0], cy / ATLAS[1], (cy + 1) / ATLAS[1]


def box_faces(lod, x0, x1, y0, y1, z0, z1, tex, mat, uvf, front_only=False, skip_bottom=True):
    """Visual box as flat faces. x0 = seen-left (larger x). uvf(face, pts) -> uvs."""
    xa, xb = min(x0, x1), max(x0, x1)
    faces = {"front": ([(xb, y0, z1), (xa, y0, z1), (xa, y1, z1), (xb, y1, z1)], (0, 0, 1))}
    if not front_only:
        faces.update({
            "back": ([(xa, y0, z0), (xb, y0, z0), (xb, y1, z0), (xa, y1, z0)], (0, 0, -1)),
            "top": ([(xb, y1, z1), (xa, y1, z1), (xa, y1, z0), (xb, y1, z0)], (0, 1, 0)),
            "left": ([(xb, y0, z0), (xb, y0, z1), (xb, y1, z1), (xb, y1, z0)], (1, 0, 0)),
            "right": ([(xa, y0, z1), (xa, y0, z0), (xa, y1, z0), (xa, y1, z1)], (-1, 0, 0)),
        })
        if not skip_bottom:
            faces["bottom"] = ([(xb, y0, z0), (xa, y0, z0), (xa, y0, z1), (xb, y0, z1)], (0, -1, 0))
    for name, (pts, n) in faces.items():
        lod.add_flat_face(pts, n, uvf(name, pts), tex, mat)


def world_uv(tile):
    def f(name, pts):
        if name in ("front", "back"):
            return [((-p[0]) / tile, -p[1] / tile) for p in pts]
        if name == "top":
            return [((-p[0]) / tile, p[2] / tile) for p in pts]
        return [(p[2] / tile, -p[1] / tile) for p in pts]
    return f


def plaque_uv(k):
    u0, u1, v0, v1 = atlas_uv(k)

    def f(name, pts):
        if name != "front":
            return [(u0 + 0.01, v0 + 0.01)] * len(pts)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        return [(u0 + (max(xs) - p[0]) / (max(xs) - min(xs)) * (u1 - u0),
                 v0 + (max(ys) - p[1]) / (max(ys) - min(ys)) * (v1 - v0)) for p in pts]
    return f


def lib(mid, wear):
    return ppath(mid, wear, "_co.paa"), ppath(mid, wear, ".rvmat")


def visual_lod(res, amap):
    lod = mlod.Lod(res)
    frame = lib("jp_m_wood_street_dark", "_w1")
    base = lib("jp_m_stone_cut", "_w1")
    # backing slab and stone plinth (library materials)
    box_faces(lod, W_ / 2, -W_ / 2, -0.15, TOP, BACK_Z, 0.0, frame[0], frame[1], world_uv(2.0), skip_bottom=True)
    box_faces(lod, W_ / 2 + 0.05, -W_ / 2 - 0.05, -0.15, 0.2, BACK_Z - 0.05, 0.08, base[0], base[1], world_uv(1.0))
    detail = res < 3
    for c, mid in enumerate(ORDER, start=1):
        xl, xr = col_x(c)
        tile = MT.MATS[mid]["tile_size_m"]
        for wear, _ in WEARS:
            y0 = ROWS_Y[wear]
            t, m = lib(mid, wear)
            box_faces(lod, xl, xr, y0, y0 + P_, 0.0, 0.03, t, m, world_uv(tile), front_only=not detail)
        if res < 3:
            px = (xl + xr) / 2
            box_faces(lod, px + 0.5, px - 0.5, PLQ[0], PLQ[1], 0.0, 0.02, PLAQUE_TEX, PLAQUE_MAT,
                      plaque_uv(amap[str(c)]), front_only=res > 1)
    if res < 3:
        xl, xr = col_x(0)
        px = (xl + xr) / 2
        for wear, _ in WEARS:
            y0 = ROWS_Y[wear] + (P_ - 0.5) / 2
            box_faces(lod, px + 0.5, px - 0.5, y0, y0 + 0.5, 0.0, 0.02, PLAQUE_TEX, PLAQUE_MAT,
                      plaque_uv(amap[wear[1:]]), front_only=res > 1)
        box_faces(lod, px + 0.5, px - 0.5, PLQ[0], PLQ[1], 0.0, 0.02, PLAQUE_TEX, PLAQUE_MAT,
                  plaque_uv(amap["jp_common"]), front_only=res > 1)
    return lod


def box_solid(x0, x1, y0, y1, z0, z1):
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    f = [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]]
    return v, f


def component_lod(res, fire=False):
    lod = mlod.Lod(res)
    solids = [(box_solid(-W_ / 2, W_ / 2, -0.15, TOP, BACK_Z, 0.03), "wood"),
              (box_solid(-W_ / 2 - 0.05, W_ / 2 + 0.05, -0.15, 0.2, BACK_Z - 0.05, 0.08), "granite")]
    for k, ((v, f), pen) in enumerate(solids, start=1):
        mat = "dz\\data\\data\\penetration\\%s.rvmat" % pen if fire else ""
        pis, fis = lod.add_closed_solid(v, f, "", mat)
        lod.select("Component%02d" % k, {pi: 1.0 for pi in pis}, fis)
    return lod


MODEL_CFG = """class CfgSkeletons
{
	class Default
	{
		isDiscrete=1;
		skeletonInherit="";
		skeletonBones[]={};
	};
};
class CfgModels
{
	class Default
	{
		sectionsInherit="";
		sections[]={};
		skeletonName="";
	};
	class jp_swatch_wall: Default
	{
	};
};
"""

CONFIG = """// JP_Common - the shared material library (jp_m_*) and the material swatch wall.
// GENERATED by japan_dev/research/materials/build_materials.py - edit the generator, not this file.
// One CfgPatches class for this PBO, declared once. Every area lists JP_Common in requiredAddons.
class CfgPatches
{
	class JP_Common
	{
		units[]={};
		weapons[]={};
		requiredVersion=0.1;
		requiredAddons[]=
		{
			"DZ_Data",
			"DZ_Structures_Residential"
		};
	};
};
class CfgVehicles
{
	class HouseNoDestruct;
	class Land_JP_Swatch_Wall: HouseNoDestruct
	{
		scope=1;
		displayName="JP material swatch wall";
		model="\\JP\\common\\swatch\\jp_swatch_wall.p3d";
	};
};
"""


def swatch(do_binarize):
    im, amap = plaque_atlas()
    os.makedirs(os.path.join(BUILD, "swatch"), exist_ok=True)
    png = os.path.join(BUILD, "swatch", "jp_swatch_plaques_co.png")
    im.save(png)
    to_paa([(png, os.path.join(SWDIR, "data", "jp_swatch_plaques_co.paa"))])
    write_plaque_rvmat()
    geo = component_lod(mlod.LOD_GEOMETRY)
    geo.properties.update({"class": "house", "map": "house", "damage": "no", "autocenter": "0"})
    geo.mass = [5000.0 / len(geo.points)] * len(geo.points)
    lods = [visual_lod(1.0, amap), visual_lod(2.0, amap), visual_lod(3.0, amap), geo,
            component_lod(mlod.LOD_VIEW_GEOMETRY), component_lod(mlod.LOD_FIRE_GEOMETRY, fire=True)]
    mpath = os.path.join(BUILD, "swatch", "jp_swatch_wall.p3d")
    mlod.write_mlod(mpath, lods)
    print("swatch MLOD: %s faces per LOD" % [len(l.faces) for l in lods])
    shutil.copyfile(mpath, os.path.join(SWDIR, "jp_swatch_wall.p3d"))
    wb(os.path.join(SWDIR, "model.cfg"), MODEL_CFG)
    wb(os.path.join(SRC, "config.cpp"), CONFIG)
    for f in (os.path.join(SRC, "config.cpp"), os.path.join(SWDIR, "model.cfg")):
        dst = os.path.join(BUILD, os.path.basename(f) + ".bin")
        r = run([CFGCONVERT, "-bin", "-dst", dst, f])
        ok = r.returncode == 0 and os.path.isfile(dst)
        print("  CfgConvert %s: %s" % (os.path.basename(f), "OK" if ok else "FAILED " + (r.stdout + r.stderr).strip()))
        if not ok:
            raise RuntimeError("CfgConvert failed on " + f)
    if not do_binarize:
        return True
    if not os.path.isdir("P:\\DZ") or not os.path.isdir("P:\\JP\\common\\swatch"):
        raise RuntimeError(r"P:\DZ or P:\JP\common missing (subst P: D:\DayZToolsExtract; P:\JP junction)")
    out = os.path.join(BUILD, "binarized")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-addon=P:\\JP\\common", "-binpath=P:\\bin", "P:\\JP\\common\\swatch", out, "*.p3d"]
    r = run(cmd, cwd="P:\\")
    log = os.path.join(BUILD, "binarize.log")
    wb(log, (" ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr).replace("\r\n", "\n"))
    bad = [l.strip() for l in (r.stdout + r.stderr).splitlines()
           if any(k in l for k in ("Error", "error", "Warning", "warning", "not loaded", "Cannot", "cannot"))]
    for l in bad[:20]:
        print("  binarize:", l)
    for root, _, files in os.walk(out):
        if "jp_swatch_wall.p3d" in files:
            p = os.path.join(root, "jp_swatch_wall.p3d")
            if open(p, "rb").read(4) == b"ODOL":
                shutil.copyfile(p, os.path.join(SWDIR, "jp_swatch_wall.p3d"))
                print("  binarized OK (%d bytes), log %s, %d warning/error lines" % (os.path.getsize(p), log, len(bad)))
                return True
    print("  binarize FAILED - MLOD left in src (see %s)" % log)
    return False


def pack():
    stage = os.path.join(BUILD, "pbo_stage")
    shutil.rmtree(stage, ignore_errors=True)
    shutil.copytree(SRC, stage, ignore=shutil.ignore_patterns("model.cfg", "*.json", "*.png", "*.log"))
    import pbo
    try:
        pbo.cmd_pack(stage, PBO_OUT, "JP\\common")
    except PermissionError as e:
        print("PBO write FAILED (is the Japan test server running and holding the file?):", e)
        return False
    print("packed %s (%.1f MB)" % (PBO_OUT, os.path.getsize(PBO_OUT) / 1e6))
    return True


def placement():
    # bare README format, like F.csv: header + one row; ground is the flat yard (25.0 m); front (+z) faces south
    wb(os.path.join(DEV, "test", "placements", "M.csv"),
       "p3d,x,z,yaw_deg,y_offset\nJP\\common\\swatch\\jp_swatch_wall.p3d,957.5,1100.0,180,0.0\n")


# ----------------------------------------------------------------------------------------------------------------
# contact sheets
# ----------------------------------------------------------------------------------------------------------------
def renders(do_render):
    rd = os.path.join(BUILD, "render")
    os.makedirs(rd, exist_ok=True)
    jobs = []
    for mid in ORDER:
        for wear, _ in WEARS:
            stem = mid + wear
            out = os.path.join(rd, stem + "_sphere.png")
            co = os.path.join(TEX, stem + "_co.png")
            if os.path.isfile(out) and os.path.getmtime(out) >= os.path.getmtime(co):
                continue
            n = np.asarray(Image.open(os.path.join(TEX, stem + "_nohq.png")).convert("RGB")).copy()
            if MT.GREEN_DX:
                n[..., 1] = 255 - n[..., 1]
            gl = os.path.join(rd, stem + "_nohq_gl.png")
            Image.fromarray(n).save(gl)
            jobs.append({"co": co, "nohq_gl": gl, "smdi": os.path.join(TEX, stem + "_smdi.png"),
                         "tile_m": MT.MATS[mid]["tile_size_m"], "out": out})
    if jobs and do_render:
        jf = os.path.join(rd, "jobs.json")
        wb(jf, json.dumps(jobs, indent=1))
        r = run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_spheres.py"),
                 "--", jf])
        done = sum(os.path.isfile(j["out"]) for j in jobs)
        print("blender: %d/%d spheres rendered" % (done, len(jobs)))
        if done < len(jobs):
            print((r.stdout + r.stderr)[-3000:])
    return rd


def fonts():
    return {k: ImageFont.truetype(f, s) for k, (f, s) in
            {"h1": (FONTB, 34), "h2": (FONTB, 24), "b": (FONT, 18), "s": (FONT, 16), "sb": (FONTB, 16)}.items()}


def tile_img(mid, wear, px):
    return Image.open(os.path.join(TEX, mid + wear + "_co.png")).convert("RGB").resize((px, px), Image.LANCZOS)


def sphere_img(rd, mid, wear, px):
    p = os.path.join(rd, mid + wear + "_sphere.png")
    if os.path.isfile(p):
        return Image.open(p).convert("RGB").resize((px, px), Image.LANCZOS)
    return Image.new("RGB", (px, px), (90, 90, 90))


def wrap(d, xy, text, font, width, fill=(20, 20, 20), gap=4):
    x, y = xy
    for line in textwrap.wrap(text, width):
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def sheets(rd, res):
    os.makedirs(SHEETS, exist_ok=True)
    F = fonts()
    by = {(os.path.basename(r["file"])[:-7]): r for r in res}
    T, LW, CW, RH = 250, 600, 2 * 250 + 30, 250 + 92
    for key, title, mids in GROUPS:
        H = 90 + len(mids) * (RH + 18)
        W = LW + 3 * CW + 20
        im = Image.new("RGB", (W, H), (236, 234, 229))
        d = ImageDraw.Draw(im)
        d.text((20, 18), "jp_common material library - %s" % title, font=F["h1"], fill=(20, 20, 20))
        d.text((20, 58), "Each wear level: flat tile (one full texture tile = its real size) and a lit 1 m sphere "
                         "(real texel scale). Mean colour checked against palette.json by tools/matcheck.",
               font=F["s"], fill=(60, 60, 60))
        for i, mid in enumerate(mids):
            m = MT.MATS[mid]
            y = 90 + i * (RH + 18)
            d.rectangle([10, y - 6, W - 10, y + RH + 6], outline=(190, 186, 178), width=2)
            n = ORDER.index(mid) + 1
            d.text((20, y), "%d  %s" % (n, mid), font=F["h2"], fill=(20, 20, 20))
            e = MT.PAL[m["palette_id"]]
            pw = MT.PALETTE_BY_WEAR.get(mid, {})
            ptxt = "Palette: %s %s, tolerance dE %g%s" % (m["palette_id"], tuple(e["srgb"]), e["tolerance_dE76"],
                                                          ("; _w0 uses %s" % pw["_w0"]) if pw else "")
            d.rectangle([20, y + 36, 44, y + 60], fill=tuple(e["srgb"]), outline=(0, 0, 0))
            yy = wrap(d, (52, y + 38), ptxt, F["s"], 62)
            yy = wrap(d, (20, yy + 6), "Used on: " + USED_ON[mid], F["b"], 58)
            wrap(d, (20, yy + 6), "Tile %.2f m, %d px (%d px/m), grain: %s. Swatch column %d." % (
                m["tile_size_m"], MT.size_for(m["tile_size_m"]), MT.size_for(m["tile_size_m"]) / m["tile_size_m"],
                m["grain"], n), F["s"], 66, fill=(70, 70, 70))
            for k, (wear, wname) in enumerate(WEARS):
                x = LW + k * CW
                r = by.get(mid + wear, {})
                d.text((x, y), "%s %s: %s" % (wear, wname, m["wear"][wear])[:62], font=F["sb"], fill=(20, 20, 20))
                im.paste(tile_img(mid, wear, T), (x, y + 24))
                im.paste(sphere_img(rd, mid, wear, T), (x + T + 10, y + 24))
                if r:
                    col = {"PASS": (20, 110, 40), "WARN": (170, 110, 0), "FAIL": (190, 20, 20)}[r["verdict"]]
                    d.text((x, y + T + 30), "mean %s  dE %.1f / %g  %s" % (tuple(int(v) for v in r["mean_srgb"]), r["dE"],
                                                                         r["tol"], r["verdict"]), font=F["sb"], fill=col)
                    if r["masked_frac"]:
                        d.text((x, y + T + 50), "detail mask %.0f %% (moss, cracks... excluded from mean)" % (
                            100 * r["masked_frac"]), font=F["s"], fill=(80, 80, 80))
        out = os.path.join(SHEETS, "%s.jpg" % key)
        im.save(out, quality=90)
        print("sheet", out, im.size)
    # overview: all 22 at _w1
    cols, T2 = 4, 190
    cw, ch = 2 * T2 + 30, T2 + 50
    rows = (len(ORDER) + cols - 1) // cols
    im = Image.new("RGB", (cols * cw + 30, rows * ch + 80), (236, 234, 229))
    d = ImageDraw.Draw(im)
    d.text((20, 16), "jp_common - all 22 materials at _w1 (normal wear); numbers = swatch wall columns", font=F["h2"],
           fill=(20, 20, 20))
    for i, mid in enumerate(ORDER):
        x, y = 20 + (i % cols) * cw, 60 + (i // cols) * ch
        im.paste(tile_img(mid, "_w1", T2), (x, y))
        im.paste(sphere_img(rd, mid, "_w1", T2), (x + T2 + 6, y))
        r = by.get(mid + "_w1", {})
        d.text((x, y + T2 + 4), "%d %s  (%s)" % (i + 1, SHORT[mid], MT.MATS[mid]["palette_id"]), font=F["sb"],
               fill=(20, 20, 20))
        if r:
            d.text((x, y + T2 + 24), "dE %.1f/%g %s" % (r["dE"], r["tol"], r["verdict"]), font=F["s"], fill=(60, 60, 60))
    out = os.path.join(SHEETS, "0_overview_w1.jpg")
    im.save(out, quality=90)
    print("sheet", out, im.size)


def credits():
    man = json.load(open(os.path.join(DATA, "polyhaven", "manifest.json"), encoding="utf-8"))
    rows = ["| %s | %s | %s | %.2f m | %s | %s |" % (a, e["name"], ", ".join(e["authors"]),
                                                     (e["dimensions_mm"] or [0])[0] / 1000.0, e["page"], e["used_for"])
            for a, e in sorted(man.items())]
    txt = """# jp_common material library: credits and licences

Written by `build_materials.py` from `data/materials/polyhaven/manifest.json`.

## Downloaded (all CC0 1.0, public domain; credited anyway)

Fetched by `fetch_sources.py` from the Poly Haven API (1k JPG: diffuse, `nor_dx` normal, roughness) into
`data/materials/polyhaven/` (git-ignored), with a generic User-Agent only. Licence: https://polyhaven.com/license

| Asset | Name | Authors | Real size | Page | Became |
|---|---|---|---|---|---|
""" + "\n".join(rows) + """

Downloaded and not used: `patterned_clay_plaster` (its scalloped trowel pattern is decorative, wrong for nakanuri;
deleted from `data/materials/`).

## Procedural (no outside source)

Made by `make_textures.py` with numpy/PIL: `jp_m_wall_namako_tile`, `jp_m_roof_kawara` (ceramic surface only; the
tiles are geometry), `jp_m_roof_thatch_cut`, the board courses of `jp_m_roof_kureita` / `jp_m_roof_kokera` (grain
from Wood Planks Grey), the shells of `jp_m_roof_kakigara`, `jp_m_paper_shoji`, `jp_m_bamboo_weathered`,
`jp_m_metal_iron` (rust colour from Rust Coarse 01), `jp_m_straw_mushiro`, every wear overlay (moss, lichen, cracks,
splits, drips, rust, edge wear, streaks), and the swatch plaques (Arial from Windows, rendered to a texture).

## Vanilla DayZ referenced, not shipped

`dz\\data\\data\\env_land_co.paa` (rvmat stage 7), `dz\\data\\data\\penetration\\*.rvmat` and
`dz\\surfaces\\data\\roadway\\*.paa` (named in the sidecars), class `HouseNoDestruct`.
"""
    wb(os.path.join(HERE, "CREDITS.md"), txt)


def main(argv):
    if "--rvmats-only" in argv:                  # G3 fix 2: rewrite the rvmats (finish / specular), no texture work
        write_rvmats()
        write_plaque_rvmat()
        print("library: %d rvmats + the plaque rvmat rewritten" % (3 * len(ORDER)))
        return 0 if ("--no-pack" in argv or pack()) else 1
    only_sheets = "--sheets-only" in argv
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    if not only_sheets:
        import fetch_sources
        fetch_sources.main()
        info = MT.main(only or [])
        library(info, only)
    res = checks()
    if any(r["verdict"] == "FAIL" for r in res):
        print("C1 FAIL - fix the texture targets before shipping")
        return 1
    ok = True
    if not only_sheets and not only:
        ok = swatch("--no-binarize" not in argv) and ok
    if not only_sheets:
        if "--no-pack" not in argv:
            ok = pack() and ok
        placement()
        credits()
    rd = renders("--no-render" not in argv)
    sheets(rd, res)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
