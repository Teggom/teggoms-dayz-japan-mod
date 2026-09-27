#!/usr/bin/env python3
r"""build_world.py - build the 2048 m JapanTestIsland terrain and pack @Japan\addons\jp_worlds_testisland.pbo.

    python japan_dev\spikes\T_terrain\build_world.py                 # full build (terrain, layers, wrp, binarize, pack)
    python japan_dev\spikes\T_terrain\build_world.py --no-pack       # everything except writing the PBO
    python japan_dev\spikes\T_terrain\build_world.py --previews      # terrain + previews + route B set only
    python japan_dev\spikes\T_terrain\build_world.py --pack-only     # route B: binarize + pack what Terrain Builder
                                                                     # exported into src (no generation at all)

Route A (no GUI at all): heightmap + surfaces + satellite + layer tiles + objects are generated here, the source
world is written as 8WVR (tools/wrp8.py), binarize.exe turns it into OPRW v29, tools/common/pbo.py packs it.
Re-reads japan_dev/test/placements/*.csv on every run; missing p3ds are skipped with a warning.
Needs P: (subst P: D:\DayZToolsExtract) with P:\JP -> japan_dev\src\JP. Never touches the server or game.

Outputs:
  src/JP/worlds/testisland/            config.cpp, world/japantestisland.wrp (8WVR source), data/layers/*,
                                       data/*.paa, data/pond/jp_pond.p3d (MLOD), ce/ (generated, git-ignored)
  data/T_terrain/bin/                  binarize output (OPRW wrp, ODOL pond) + binarize logs
  data/T_terrain/pbo_stage/            exactly what goes into the PBO
  @Japan/addons/jp_worlds_testisland.pbo
  spikes/T_terrain/previews/*.png      heightmap, satellite, surface mask, objects
  spikes/T_terrain/world_info.json     positions build_mission.py needs (house, pond, spawn, ...)
"""
import json
import math
import os
import shutil
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tools"))
import gsi_dem  # noqa: E402
import layers  # noqa: E402
import objects  # noqa: E402
import pond  # noqa: E402
import route_b  # noqa: E402
import terrain  # noqa: E402
import wrp8  # noqa: E402

DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
SERVER = os.path.dirname(DEV)
SRC = os.path.join(DEV, "src", "JP", "worlds", "testisland")
DATA = os.path.join(DEV, "data", "T_terrain")
TEST = os.path.join(DEV, "test")
PREV = os.path.join(HERE, "previews")
PBO_OUT = os.path.join(SERVER, "@Japan", "addons", "jp_worlds_testisland.pbo")
PREFIX = r"JP\worlds\testisland"
WORLD_NAME = "japantestisland"
BINARIZE = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\Binarize\binarize.exe"
PBO_PY = os.path.join(DEV, "tools", "common", "pbo.py")

WORLD = 2048
LAND_RANGE = 128                 # 16 m land (material) cells; tile step 480 m = 30 cells
LAND_CELL = WORLD / LAND_RANGE
SEED = 20260926

# the Hakone patch: GSI DEM5A (5 m lidar) z15 tiles around 35.1939 N 139.0739 E, Hakone's south-east outer rim
# (Shiroganeyama / Yugawara side), holes filled from DEM10B z14; 462 x 462 px at 3.90 m = 1.8 km square
PATCH_CENTRE_PX = (7434960, 3317188)      # global z15 pixel coordinates of the patch centre
PATCH_HALF_PX = 231

LAYOUT = {
    "patch_origin": (1024.0, 1300.0),     # world position of the patch centre (north of the yard)
    "patch_rotate": 0.0,
    "road_half_width": 3.0,
    "road_max_grade": 0.13,
    "canal_half_width": 7.0,
    "pond": (800.0, 905.0, 16.0, None),   # x, z, radius, water level (None = natural ground - 0.4 m)
    "pads": [(1235.0, 915.0, 9.0, 12.0)],  # control house pad: x, z, half size, blend
}
ROAD_START, ROAD_YAW = (1100.0, 1100.0), 10.0
ROAD_STEPS = [("S", 25.0), ("S", 25.0), ("L", 10.0, 75.0), ("S", 25.0), ("S", 25.0), ("R", 15.0, 75.0),
              ("S", 25.0), ("S", 25.0), ("END",)]
HOUSE_POS, HOUSE_YAW = (1235.0, 915.0), 200.0
PADDIES = [(610.0, 705.0, 770.0, 825.0, 40.0, 30.0)]
SPAWN = (1024.0, 985.0)

LOG = []


def log(msg):
    LOG.append(msg)
    print(msg, flush=True)


# ------------------------------------------------------------------------------------------------------
def load_patch():
    """Fetch (cached) and stitch the DEM5A patch, filling holes from DEM10B."""
    cache = os.path.join(gsi_dem.CACHE, "patch_%d_%d_%d.npy" % (PATCH_CENTRE_PX + (PATCH_HALF_PX,)))
    if os.path.isfile(cache):
        return np.load(cache)
    gx0, gy0 = PATCH_CENTRE_PX[0] - PATCH_HALF_PX, PATCH_CENTRE_PX[1] - PATCH_HALF_PX
    gx1, gy1 = gx0 + 2 * PATCH_HALF_PX, gy0 + 2 * PATCH_HALF_PX
    tx0, ty0, tx1, ty1 = gx0 // 256, gy0 // 256, (gx1 - 1) // 256, (gy1 - 1) // 256
    a, _, _, _ = gsi_dem.mosaic("dem5a_png", 15, tx0, ty0, tx1 - tx0 + 1, ty1 - ty0 + 1)
    b, _, _, _ = gsi_dem.mosaic("dem_png", 14, tx0 // 2, ty0 // 2, tx1 // 2 - tx0 // 2 + 1, ty1 // 2 - ty0 // 2 + 1)
    b2 = np.kron(b, np.ones((2, 2), np.float32))
    ox, oy = tx0 * 256 - (tx0 // 2) * 512, ty0 * 256 - (ty0 // 2) * 512
    b2 = b2[oy:oy + a.shape[0], ox:ox + a.shape[1]]
    a = np.where(np.isfinite(a), a, b2)
    patch = a[gy0 - ty0 * 256:gy1 - ty0 * 256, gx0 - tx0 * 256:gx1 - tx0 * 256].astype(np.float32)
    assert np.isfinite(patch).all()
    np.save(cache, patch)
    return patch


def canal_line():
    """Canal from 60 m offshore to 110 m inland, on the east coast at z = 900."""
    xs = np.arange(1024.0, 2048.0, 1.0)
    d, _ = terrain.coast_distance(xs, np.full_like(xs, 900.0))
    xc = float(xs[np.argmax(d < 0)])
    return [(xc + 60.0, 900.0), (xc - 110.0, 903.0)], xc


# ------------------------------------------------------------------------------------------------------
def hillshade_rgb(h, cell):
    gz, gx = np.gradient(h.astype(np.float64), cell)
    sl = np.arctan(np.hypot(gx, gz))
    asp = np.arctan2(-gx, gz)
    hs = np.sin(np.radians(45)) * np.cos(sl) + np.cos(np.radians(45)) * np.sin(sl) * np.cos(np.radians(315) - asp)
    return np.clip(hs, 0, 1)


def write_previews(T, s, sat, pl, road_line):
    os.makedirs(PREV, exist_ok=True)
    h = T["h"]
    # heightmap: hypsometric tint x hillshade, 10 m contours, yard square
    hs = hillshade_rgb(h, terrain.CELL)[::-1]
    hh = h[::-1].astype(np.float64)
    t = np.clip(hh / 200.0, 0, 1)[..., None]
    rgb = np.where(hh[..., None] > 0, (1 - t) * np.array([90, 150, 80]) + t * np.array([200, 180, 140]),
                   np.array([40, 80, 140]) * (1 + np.clip(hh, -40, 0)[..., None] / 80))
    rgb = rgb * (0.35 + 0.65 * hs[..., None])
    lvl = np.floor(hh / 10.0)
    edge = (np.diff(lvl, axis=0, prepend=lvl[:1]) != 0) | (np.diff(lvl, axis=1, prepend=lvl[:, :1]) != 0)
    rgb[edge] *= 0.6
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((1024, 1024), Image.BILINEAR)
    dr = ImageDraw.Draw(img)
    k = 1024 / WORLD
    dr.rectangle([(924 * k, (WORLD - 1124) * k), (1124 * k, (WORLD - 924) * k)], outline=(255, 255, 0))
    dr.line([(x * k, (WORLD - z) * k) for x, z in road_line], fill=(255, 60, 0), width=2)
    img.save(os.path.join(PREV, "heightmap.png"))
    Image.fromarray(np.clip(hh, -40, 250).astype(np.float64).__sub__(-40).__mul__(255 / 290).astype(np.uint8)).save(
        os.path.join(PREV, "heightmap_raw_grey.png"))
    # satellite and mask (downscaled 2048 -> 1024)
    Image.fromarray(sat[::-1].astype(np.uint8)).resize((1024, 1024), Image.BILINEAR).save(os.path.join(PREV, "satellite.png"))
    # vanilla-style satellites are dark by design (the shader brightens them); a x2.4 copy for human eyes
    Image.fromarray(np.clip(sat[::-1] * 2.4, 0, 255).astype(np.uint8)).resize((1024, 1024), Image.BILINEAR).save(
        os.path.join(PREV, "satellite_bright.png"))
    col = np.array(layers.PREVIEW_COLOURS, np.uint8)[s[::-1]]
    Image.fromarray(col).resize((1024, 1024), Image.NEAREST).save(os.path.join(PREV, "surface_mask.png"))
    # objects over the satellite
    img = Image.fromarray(sat[::-1].astype(np.uint8)).resize((1024, 1024), Image.BILINEAR)
    dr = ImageDraw.Draw(img)
    colours = {"tree": (20, 60, 20), "bush": (120, 160, 40), "rock": (255, 255, 255), "road": (255, 80, 0),
               "house": (255, 0, 255), "pond": (0, 200, 255)}
    for o in pl.objects:
        x, z = o["pos"][0] * k, (WORLD - o["pos"][2]) * k
        c = colours.get(o["kind"], (255, 0, 0))
        r = 1 if o["kind"] in ("tree", "bush") else 3
        dr.ellipse([(x - r, z - r), (x + r, z + r)], fill=c)
    img.save(os.path.join(PREV, "objects.png"))
    # yard close-up (200 m + margin) of the objects preview at full satellite resolution
    crop = sat[::-1][WORLD - 1180:WORLD - 868, 868:1180].astype(np.uint8)
    img = Image.fromarray(crop).resize((624, 624), Image.NEAREST)
    dr = ImageDraw.Draw(img)
    for o in pl.objects:
        x, z = (o["pos"][0] - 868) * 2, (1180 - o["pos"][2]) * 2
        if 0 <= x < 624 and 0 <= z < 624:
            c = colours.get(o["kind"], (255, 0, 0))
            dr.ellipse([(x - 3, z - 3), (x + 3, z + 3)], fill=c)
    dr.rectangle([((924 - 868) * 2, (1180 - 1124) * 2), ((1124 - 868) * 2, (1180 - 924) * 2)], outline=(255, 255, 0))
    dr.ellipse([((SPAWN[0] - 868) * 2 - 4, (1180 - SPAWN[1]) * 2 - 4), ((SPAWN[0] - 868) * 2 + 4, (1180 - SPAWN[1]) * 2 + 4)],
               outline=(255, 0, 0), width=2)
    img.save(os.path.join(PREV, "yard_closeup.png"))


def normal_map(h, out_png):
    """World-space normal map for terrainNormalTexture (R = east, G = north, B = up)."""
    up = layers.upsample(h.astype(np.float64), 2)          # 1024 px, 2 m
    gz, gx = np.gradient(up, 2.0)
    n = np.stack([-gx, -gz, np.ones_like(gx)], axis=-1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    img = ((n * 0.5 + 0.5) * 255).astype(np.uint8)[::-1]
    Image.fromarray(img).save(out_png)


def config_cpp(names):
    nm = []
    for cls, name, x, z, typ in names:
        nm.append("\t\t\tclass %s\n\t\t\t{\n\t\t\t\tname=\"%s\";\n\t\t\t\tposition[]={%.1f,%.1f};\n\t\t\t\ttype=\"%s\";\n\t\t\t};" % (cls, name, x, z, typ))
    mats = "\n".join("\t\t\tmaterial%d=\"%s\";" % (i, s[1]) for i, s in enumerate(layers.SURFACES))
    own_nm = os.path.join(SRC, "navmesh", WORLD_NAME + ".nm")
    if os.path.isfile(own_nm):
        navmesh = "\\JP\\worlds\\testisland\\navmesh\\%s.nm" % WORLD_NAME
    else:
        navmesh = "\\DZ\\worlds\\enoch\\navmesh\\navmesh.nm"   # stopgap: a missing navmesh is fatal
    return (CONFIG_TEMPLATE.replace("@NAMES@", "\n".join(nm)).replace("@MATERIALS@", mats)
            .replace("@NAVMESH@", navmesh))


CONFIG_TEMPLATE = r"""// JapanTestIsland - 2048 m test world for the feudal Japan project (japan_dev/, spike T).
// GENERATED by japan_dev/spikes/T_terrain/build_world.py - edit the template there, not this file.
// Inherits ChernarusPlus for sky, weather, lighting, ambient life and sounds; overrides everything map-specific.
class CfgPatches
{
	class JP_Worlds_TestIsland
	{
		units[]={};
		weapons[]={};
		requiredVersion=0.1;
		requiredAddons[]=
		{
			"DZ_Data",
			"DZ_Surfaces",
			"DZ_Worlds_Chernarusplus_World"
		};
	};
};
class CfgWorldList
{
	class JapanTestIsland
	{
	};
};
class CfgWorlds
{
	class CAWorld;
	class ChernarusPlus;
	class JapanTestIsland: ChernarusPlus
	{
		description="Japan Test Island";
		worldName="JP\worlds\testisland\world\japantestisland.wrp";
		ceFiles="JP\worlds\testisland\ce";
		cutscenes[]={};
		// A missing navmesh is FATAL ("Unable to load navmesh", server dies - Stephen's first boot, 2026-09-27).
		// Until NavMeshGenerator has produced our own .nm, build_world.py points navmeshName at vanilla Livonia's
		// navmesh as a stopgap so the world boots; AI then paths on Livonia's mesh (wrong, irrelevant for dummies).
		// GenParams are the vanilla ones, ready for NavMeshGenerator - see spikes/T_terrain/REPORT.md.
		class Navmesh
		{
			navmeshName="@NAVMESH@";
			filterIsolatedIslandsOnLoad=1;
			visualiseOffset=0;
			class GenParams
			{
				tileWidth=50;
				cellSize1=0.25;
				cellSize2=0.1;
				cellSize3=0.1;
				filterIsolatedIslands=1;
				seedPosition[]={1024,0,1024};
				class Agent
				{
					diameter=0.60000002;
					standHeight=1.5;
					crouchHeight=1;
					proneHeight=0.5;
					maxStepHeight=0.44999999;
					maxSlope=60;
				};
				class Links
				{
					class ZedJump387_050
					{
						jumpLength=1.5;
						jumpHeight=0.5;
						minCenterHeight=0.30000001;
						jumpDropdownMin=0.5;
						jumpDropdownMax=-0.5;
						areaType="jump0";
						flags[]={"jumpOver"};
						color=1728004096;
					};
					class ZedJump388_050
					{
						jumpLength=1.5;
						jumpHeight=0.5;
						minCenterHeight=-0.5;
						jumpDropdownMin=0.5;
						jumpDropdownMax=-0.5;
						areaType="jump0";
						flags[]={"jumpOver"};
						color=1725781248;
					};
					class ZedJump387_110
					{
						jumpLength=3.9000001;
						jumpHeight=1.1;
						minCenterHeight=0.5;
						jumpDropdownMin=0.5;
						jumpDropdownMax=-0.5;
						areaType="jump0";
						flags[]={"jumpOver"};
						color=1711308800;
					};
					class ZedJump420_160
					{
						jumpLength=4;
						jumpHeight=1.6;
						minCenterHeight=1.1;
						jumpDropdownMin=0.5;
						jumpDropdownMax=-0.5;
						areaType="jump0";
						flags[]={"jumpOver"};
						color=1711276287;
					};
					class ZedJump265_210
					{
						jumpLength=2.45;
						jumpHeight=2.5;
						minCenterHeight=1.8;
						jumpDropdownMin=0.5;
						jumpDropdownMax=-0.5;
						areaType="jump0";
						flags[]={"climb"};
						color=1721024723;
					};
				};
			};
		};
		// Hakone, Japan (the DEM patch). latitude: positive is SOUTH in this engine (Chernarus is -56)
		longitude=139.07;
		latitude=-35.19;
		startTime="10:00";
		startDate="5/4/2026";
		centerPosition[]={1024,1024,300};
		ilsPosition[]={1024,1024};
		ilsDirection[]={1,0.079999998,0};
		ilsTaxiIn[]={};
		ilsTaxiOff[]={};
		drawTaxiway=0;
		class SecondaryAirports
		{
		};
		// repeated from ChernarusPlus so binarize finds them even when it cannot resolve the base class
		soundMapAttenCoef=0.0099999998;
		class SoundMapValues
		{
			treehard=0.029999999;
			treesoft=0.029999999;
			bushhard=0;
			bushsoft=0;
			forest=1;
			house=0.30000001;
			church=0.5;
		};
		minTreesInForestSquare=10;
		minRocksInRockSquare=5;
		clutterGrid=1;
		clutterDist=125;
		noDetailDist=40;
		fullDetailDist=15;
		midDetailTexture="DZ\worlds\chernarusplus\data\middle_sat_mco.paa";
		terrainNormalTexture="JP\worlds\testisland\data\japantestisland_normal_nohq.paa";
		class UsedTerrainMaterials
		{
@MATERIALS@
		};
		class OutsideTerrain
		{
			satellite="JP\worlds\testisland\data\outside_sat_co.paa";
			enableTerrainSynth=0;
			class Layers
			{
				class Layer0
				{
					nopx="DZ\surfaces\data\terrain\cp_gravel_nopx.paa";
					texture="DZ\surfaces\data\terrain\cp_gravel_ca.paa";
				};
			};
		};
		class Grid
		{
			offsetX=0;
			offsetY=0;
			class Zoom1
			{
				zoomMax=0.15000001;
				format="XY";
				formatX="000";
				formatY="000";
				stepX=100;
				stepY=100;
			};
			class Zoom2
			{
				zoomMax=0.85000002;
				format="XY";
				formatX="00";
				formatY="00";
				stepX=1000;
				stepY=1000;
			};
			class Zoom3
			{
				zoomMax=1e+30;
				format="XY";
				formatX="0";
				formatY="0";
				stepX=10000;
				stepY=10000;
			};
		};
		class Names
		{
@NAMES@
		};
	};
};
"""


# ------------------------------------------------------------------------------------------------------
def run_binarize(src_rel, out_dir, pattern, addon=True):
    os.makedirs(out_dir, exist_ok=True)
    cmd = [BINARIZE, "-always", "-silent", "-binpath=P:\\"]
    if addon:
        cmd.append("-addon=P:\\" + PREFIX)
    cmd += ["P:\\" + src_rel, out_dir, pattern]
    t0 = time.time()
    res = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    text = " ".join(cmd) + "\n\n" + res.stdout + "\n" + res.stderr
    return res.returncode, text, time.time() - t0


def summarize_binarize_log(text):
    lines = text.splitlines()
    bad = [l for l in lines if ("error" in l.lower() or "cannot" in l.lower() or "not found" in l.lower()
                                or "missing" in l.lower() or "failed" in l.lower())
           and "No entry" not in l and "PreloadConfig" not in l]
    noentry = sorted(set(l.strip() for l in lines if "No entry" in l))
    return bad, noentry


def main(argv):
    previews_only = "--previews" in argv
    do_pack = "--no-pack" not in argv and not previews_only
    t_start = time.time()
    if not os.path.isdir("P:\\DZ"):
        print("P: is not mapped. Run:  subst P: D:\\DayZToolsExtract")
        return 2
    if not os.path.isdir("P:\\JP\\worlds\\testisland"):
        print("P:\\JP\\worlds\\testisland missing - P:\\JP must be a junction to japan_dev\\src\\JP")
        return 2
    rng = np.random.default_rng(SEED)
    os.makedirs(DATA, exist_ok=True)
    if "--pack-only" in argv:
        return binarize_and_pack(do_pack, t_start, from_tb=True)

    # 1. terrain -----------------------------------------------------------------------------------
    patch = load_patch()
    mpp = gsi_dem.metres_per_pixel(35.1939, 15)
    road_pieces, road_line = objects.plan_road(ROAD_START, ROAD_YAW, ROAD_STEPS)
    canal, coast_x = canal_line()
    layout = dict(LAYOUT)
    layout["road"] = road_line
    layout["canal"] = canal
    T = terrain.compose(patch, mpp, layout)
    h = T["h"]
    log("terrain: %dx%d at %.1f m, heights %.1f .. %.1f m, DEM vertical scale %.2f, land %.2f km2"
        % (terrain.N, terrain.N, terrain.CELL, h.min(), h.max(), T["vscale"], (h > 0).sum() * terrain.CELL ** 2 / 1e6))
    yard = h[231:282, 231:282]
    log("yard: %d vertices, min %.4f max %.4f (must be exactly 25.0)" % (yard.size, yard.min(), yard.max()))
    s_, prof, nat = T["road_profile"]
    log("road: %d pieces, %.0f m, height %.1f -> %.1f m, max grade %.1f%%, deepest cut %.1f m"
        % (len(road_pieces), s_[-1], prof[0], prof[-1], 100 * np.max(np.abs(np.diff(prof))) / 2.0, np.max(nat - prof)))
    log("canal: coast at x=%.0f on z=900, cut from (%.0f, %.0f) to (%.0f, %.0f), floor -2.5 m"
        % (coast_x, canal[0][0], canal[0][1], canal[1][0], canal[1][1]))
    log("pond: centre (%.0f, %.0f) r=%.0f m, water level %.2f m" % (layout["pond"][0], layout["pond"][1], T["pond_r"], T["pond_level"]))

    # 2. objects ------------------------------------------------------------------------------------
    pl = objects.Placer(h, log)
    for p3d, x, z, yaw in road_pieces:
        pl.place(p3d, x, z, yaw, kind="road")
    noise4 = layers.value_noise(h.shape, 30, SEED + 3)
    F = objects.forest_density(T, noise4)
    pads_xyz = [(p[0], p[1], p[2]) for p in LAYOUT["pads"]]
    nt, nb = objects.place_vegetation(pl, T, F, rng, pads_xyz)
    ncp = objects.place_coastal_pines(pl, T, rng)
    nr = objects.place_rocks(pl, T, rng)
    house = pl.place(objects.HOUSE, HOUSE_POS[0], HOUSE_POS[1], HOUSE_YAW, kind="house")
    pond_p3d = PREFIX + r"\data\pond\jp_pond.p3d"
    pond_path = os.path.join(SRC, "data", "pond", "jp_pond.p3d")
    pond.write_pond(pond_path, T["pond_r"] + 1.0)
    pl.bc_cache.pop(pond_p3d, None)
    pobj = pl.place(pond_p3d, layout["pond"][0], layout["pond"][1], 0.0, kind="pond", y_abs=T["pond_level"])
    rows = objects.read_placements(TEST, log)
    log("placements: %d rows in test/placements/*.csv" % len(rows))
    nplaced = objects.place_placements(pl, rows, log)
    if pl.missing:
        log("WARNING: models not found: %s" % sorted(set(pl.missing)))
    counts = {}
    for o in pl.objects:
        counts[o["kind"]] = counts.get(o["kind"], 0) + 1
    log("objects: %d total - trees %d (+%d coastal pines), bushes %d, rocks %d, road pieces %d, house 1, pond 1, placements %d"
        % (len(pl.objects), nt, ncp, nb, nr, len(road_pieces), nplaced))

    # 3. surfaces + satellite --------------------------------------------------------------------------
    pads_mask = [(HOUSE_POS[0], HOUSE_POS[1], 8.0)]
    s, h1, slope1 = layers.classify(T, F, pads_mask, PADDIES)
    F1 = layers.upsample(F, 4)
    # every placed tree / bush also darkens the satellite under its crown, so the far view matches the objects
    crown = np.zeros_like(F1)
    yy, xx = np.mgrid[-5:6, -5:6]
    for o in pl.objects:
        if o["kind"] in ("tree", "bush"):
            r = (3.8 if o["kind"] == "tree" else 1.8) * float(np.linalg.norm(o["up"]))
            cx, cz = int(o["pos"][0]), int(o["pos"][2])
            if 5 <= cx < WORLD - 5 and 5 <= cz < WORLD - 5:
                disc = np.clip(1.2 - np.hypot(xx, yy) / r, 0, 1)
                win = crown[cz - 5:cz + 6, cx - 5:cx + 6]
                np.maximum(win, disc, out=win)
    sat = layers.satellite(s, h1, slope1, np.maximum(F1 * 0.85, crown * 0.95))
    frac = np.bincount(s.ravel(), minlength=6) / s.size
    log("surfaces: " + ", ".join("%s %.1f%%" % (layers.SURFACES[i][0], 100 * frac[i]) for i in range(6)))
    write_previews(T, s, sat, pl, road_line)
    info = {
        "world": WORLD, "yard_centre": [1024, 1024], "yard_half": 100, "yard_height": 25.0, "spawn": list(SPAWN),
        "house": {"class": "Land_House_1W01", "p3d": objects.HOUSE, "pos": [float(v) for v in house["pos"]],
                  "yaw": HOUSE_YAW} if house else None,
        "pond": {"pos": [layout["pond"][0], T["pond_level"], layout["pond"][1]], "radius": T["pond_r"]},
        "canal": canal, "road_start": list(ROAD_START), "road_end": list(road_line[-1]),
        "summit": None,
        # every building-like object baked into the wrp, with its ENGINE position (= what mapgrouppos needs)
        "placed": [{"p3d": o["p3d"], "pos": [float(v) for v in o["pos"]], "yaw": float(o["yaw"]), "src": o["kind"]}
                   for o in pl.objects if o["kind"] == "house" or o["kind"].startswith("placement:")],
    }
    route_b.export(os.path.join(DATA, "route_b"), T, s, sat, pl, log)
    # inputs for the optional Blender oblique render (tools/render_island.py)
    Image.fromarray(np.clip(sat[::-1] * 2.4, 0, 255).astype(np.uint8)).save(os.path.join(DATA, "satellite_bright_full.png"))
    trees = np.array([[o["pos"][0], o["pos"][2], o["origin"][1], float(np.linalg.norm(o["up"]))] for o in pl.objects
                      if o["kind"] == "tree"], np.float32)
    np.savez_compressed(os.path.join(DATA, "render_input.npz"), h=h, trees=trees)
    j, i = np.unravel_index(np.argmax(h), h.shape)
    info["summit"] = [float(i * terrain.CELL), float(h[j, i]), float(j * terrain.CELL)]
    with open(os.path.join(HERE, "world_info.json"), "wb") as f:
        f.write(json.dumps(info, indent=1).encode("utf-8"))
    if previews_only:
        log("previews only - done in %.0f s" % (time.time() - t_start))
        return 0

    # 4. layer tiles, rvmats, extra textures -----------------------------------------------------------
    lay_dir = os.path.join(SRC, "data", "layers")
    rvmats, ntiles = layers.make_tiles(s, sat, lay_dir, PREFIX + r"\data\layers", WORLD, log)
    log("layers: %d x %d tiles of 512 px (1 m/px, 16 px overlap)" % (ntiles, ntiles))
    normal_map(h, os.path.join(SRC, "data", "japantestisland_normal_nohq.png"))
    layers.to_paa(os.path.join(SRC, "data", "japantestisland_normal_nohq.png"), os.path.join(SRC, "data", "japantestisland_normal_nohq.paa"))
    out_png = os.path.join(SRC, "data", "outside_sat_co.png")
    Image.new("RGB", (64, 64), (58, 72, 78)).save(out_png)
    layers.to_paa(out_png, out_png[:-4] + ".paa")

    # 5. 8WVR -------------------------------------------------------------------------------------------
    w = wrp8.Wrp8(LAND_RANGE, terrain.N, LAND_CELL)
    w.elevation[:] = h
    layers.cell_materials(LAND_RANGE, LAND_CELL, WORLD, rvmats, w)
    for o in pl.objects:
        w.add_object(o["p3d"], o["pos"], o["aside"], o["up"], o["dir"])
    os.makedirs(os.path.join(SRC, "world"), exist_ok=True)
    wrp_src = os.path.join(SRC, "world", WORLD_NAME + ".wrp")
    n = w.write(wrp_src)
    back = wrp8.read_8wvr(wrp_src)
    assert np.array_equal(back["elev"], h.astype(np.float32)) and len(back["objects"]) == len(pl.objects) + 1
    log("8WVR: %s (%d bytes, %d materials, %d objects + dummy) - read back OK" % (wrp_src, n, len(w.materials), len(pl.objects)))

    # 6. config + ce -------------------------------------------------------------------------------------
    names = [("JP_Yard", "Shiken-jima (test yard)", 1024.0, 1024.0, "Village"),
             ("JP_Summit", "Hakone-dake", info["summit"][0], info["summit"][2], "Hill"),
             ("JP_Canal", "Unga", canal[1][0], canal[1][1], "Local"),
             ("JP_Pond", "Ike", layout["pond"][0], layout["pond"][1], "Local")]
    with open(os.path.join(SRC, "config.cpp"), "wb") as f:
        f.write(config_cpp(names).encode("ascii"))
    write_world_ce()
    with open(os.path.join(SRC, ".gitignore"), "wb") as f:
        f.write(b"# generated by spikes/T_terrain/build_world.py - rebuild instead of committing\n"
                b"data/layers/\ndata/*.paa\ndata/*.png\ndata/pond/\nworld/\nce/\nnavmesh/\n_smoke/\n")
    # CfgConvert parse test
    cfgc = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\CfgConvert\CfgConvert.exe"
    tmpbin = os.path.join(DATA, "config_test.bin")
    r = subprocess.run([cfgc, "-bin", "-dst", tmpbin, os.path.join(SRC, "config.cpp")], capture_output=True, text=True)
    log("CfgConvert -bin config.cpp: exit %d %s" % (r.returncode, (r.stdout + r.stderr).strip()[:300]))

    return binarize_and_pack(do_pack, t_start, from_tb=False, n_objects=sum(1 for o in pl.objects if o["kind"] != "road"))


def binarize_and_pack(do_pack, t_start, from_tb=False, n_objects=None):
    pond_path = os.path.join(SRC, "data", "pond", "jp_pond.p3d")
    if from_tb:
        # Terrain Builder writes PNG layer tiles and rvmats that point at them: convert to paa, repoint the rvmats
        lay = os.path.join(SRC, "data", "layers")
        n = 0
        for fn in os.listdir(lay):
            if fn.lower().endswith(".png") and fn.lower()[:2] in ("s_", "m_", "n_"):
                layers.to_paa(os.path.join(lay, fn), os.path.join(lay, fn[:-4] + ".paa"))
                n += 1
            if fn.lower().endswith(".rvmat"):
                t = open(os.path.join(lay, fn), "rb").read().decode("latin-1")
                t2 = t.replace(".png\"", ".paa\"")
                if t2 != t:
                    open(os.path.join(lay, fn), "wb").write(t2.encode("latin-1"))
        log("pack-only (route B): %d TB layer PNGs converted to paa" % n)
    # 7. binarize ------------------------------------------------------------------------------------------
    bin_dir = os.path.join(DATA, "bin")
    shutil.rmtree(bin_dir, ignore_errors=True)
    code, text, dt = run_binarize(PREFIX + r"\data\pond", os.path.join(bin_dir, "pond"), "*.p3d", addon=False)
    open(os.path.join(DATA, "binarize_pond.log"), "wb").write(text.encode("utf-8"))
    pond_odol = os.path.join(bin_dir, "pond", "jp_pond.p3d")
    log("binarize pond: exit %d, %.1f s, ODOL=%s" % (code, dt, os.path.isfile(pond_odol) and open(pond_odol, "rb").read(4) == b"ODOL"))
    code, text, dt = run_binarize(PREFIX + r"\world", os.path.join(bin_dir, "world"), "*.wrp")
    open(os.path.join(DATA, "binarize_world.log"), "wb").write(text.encode("utf-8"))
    oprw = os.path.join(bin_dir, "world", WORLD_NAME + ".wrp")
    bad, noentry = summarize_binarize_log(text)
    log("binarize world: exit %d, %.1f s, log data/T_terrain/binarize_world.log" % (code, dt))
    for l in bad[:30]:
        log("  binarize: " + l.strip())
    if noentry:
        log("  binarize config lookups that fell back to defaults: %d distinct (see log)" % len(noentry))
    if not os.path.isfile(oprw):
        log("FAILED: no OPRW produced")
        return 1
    oi = wrp8.read_oprw_summary(oprw)
    log("OPRW: %s v%s tag %s appId %s, land %s, terrain %s, cell %.1f, %d models, %d rvmats, %d bytes"
        % (oi["sig"], oi.get("version"), oi.get("tag"), oi.get("appid"), oi.get("land"), oi.get("terrain"), oi.get("cell", 0),
           len(oi.get("models", [])), len(oi.get("rvmats", [])), oi["size"]))
    data = open(oprw, "rb").read()
    arr = wrp8.oprw_objects(data, len(oi["models"]), oi.get("models_end", 0), min_run=100)
    if arr is not None:
        log("OPRW object records: %d (non-road objects in the 8WVR: %s)" % (len(arr), n_objects))

    # 8. stage + pack ---------------------------------------------------------------------------------------
    stage = os.path.join(DATA, "pbo_stage")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(os.path.join(stage, "world"))
    shutil.copyfile(os.path.join(SRC, "config.cpp"), os.path.join(stage, "config.cpp"))
    shutil.copyfile(oprw, os.path.join(stage, "world", WORLD_NAME + ".wrp"))
    for root, _, files in os.walk(os.path.join(SRC, "data")):
        for fn in files:
            if fn.endswith((".paa", ".rvmat")):
                rel = os.path.relpath(os.path.join(root, fn), SRC)
                os.makedirs(os.path.dirname(os.path.join(stage, rel)), exist_ok=True)
                shutil.copyfile(os.path.join(root, fn), os.path.join(stage, rel))
    os.makedirs(os.path.join(stage, "data", "pond"), exist_ok=True)
    shutil.copyfile(pond_odol if os.path.isfile(pond_odol) else pond_path, os.path.join(stage, "data", "pond", "jp_pond.p3d"))
    shutil.copytree(os.path.join(SRC, "ce"), os.path.join(stage, "ce"))
    # a navmesh saved by NavMeshGenerator to P:\JP\worlds\testisland\navmesh\japantestisland.nm is packed as-is
    # (it goes stale on every terrain / object change - see REPORT.md)
    nm = os.path.join(SRC, "navmesh", WORLD_NAME + ".nm")
    if os.path.isfile(nm):
        os.makedirs(os.path.join(stage, "navmesh"), exist_ok=True)
        shutil.copyfile(nm, os.path.join(stage, "navmesh", WORLD_NAME + ".nm"))
        log("navmesh: packed %s (%d bytes) - regenerate it after any terrain/object change" % (nm, os.path.getsize(nm)))
    else:
        log("navmesh: none (AI will stand still; fine for this test)")
    # texture headers (optional load-time speed-up; vanilla data PBOs ship one): binarize -texheader
    th = os.path.join(DATA, "texheaders")
    shutil.rmtree(th, ignore_errors=True)
    os.makedirs(th)
    r = subprocess.run([BINARIZE, "-texheader", "-silent", "P:\\" + PREFIX, th], cwd="P:\\", capture_output=True, text=True,
                       errors="replace")
    thb = [f for f in os.listdir(th) if f.lower() == "texheaders.bin"]
    if thb:
        shutil.copyfile(os.path.join(th, thb[0]), os.path.join(stage, "texHeaders.bin"))
        log("texHeaders.bin: %d bytes" % os.path.getsize(os.path.join(stage, "texHeaders.bin")))
    else:
        log("texHeaders.bin: not produced (optional) - exit %d" % r.returncode)
    if do_pack:
        try:
            r = subprocess.run([sys.executable, PBO_PY, "pack", stage, PBO_OUT, "--prefix", PREFIX], capture_output=True, text=True)
            log(r.stdout.strip() or r.stderr.strip())
            if r.returncode != 0:
                log("PACK FAILED (is the Japan test server or the game running? it locks the PBO): " + r.stderr.strip()[-300:])
                return 1
        except OSError as e:
            log("PACK FAILED: %s" % e)
            return 1
    log("done in %.0f s" % (time.time() - t_start))
    with open(os.path.join(DATA, "build_world.log"), "wb") as f:
        f.write("\n".join(LOG).encode("utf-8"))
    return 0


def write_world_ce():
    """ceFiles folder inside the PBO: the vanilla Chernarus core CE files (the mission overrides all of them)."""
    ce = os.path.join(SRC, "ce")
    shutil.rmtree(ce, ignore_errors=True)
    os.makedirs(os.path.join(ce, "db"))
    van = r"P:\DZ\worlds\chernarusplus\ce"
    for fn in ("cfgeconomycore.xml", "cfglimitsdefinition.xml", "cfglimitsdefinitionuser.xml", "cfgrandompresets.xml",
               "cfgspawnabletypes.xml", "mapgroupproto.xml", "mapclusterproto.xml", "cfgignorelist.xml"):
        shutil.copyfile(os.path.join(van, fn), os.path.join(ce, fn))
    for fn in ("economy.xml", "globals.xml", "types.xml"):
        shutil.copyfile(os.path.join(van, "db", fn), os.path.join(ce, "db", fn))
    with open(os.path.join(ce, "db", "events.xml"), "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<events>\n</events>\n')
    with open(os.path.join(ce, "cfgeventspawns.xml"), "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<eventposdef>\n</eventposdef>\n')
    with open(os.path.join(ce, "mapgrouppos.xml"), "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<map>\n</map>\n')
    with open(os.path.join(ce, "cfgenvironment.xml"), "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<env>\n\t<territories>\n\t</territories>\n</env>\n')


def run_placecheck():
    """Float/sink check of everything baked or spawned on the island (japan_dev/tools/placecheck, cached)."""
    dev = os.path.dirname(os.path.dirname(HERE))
    r = subprocess.run([sys.executable, os.path.join(dev, "tools", "placecheck", "check.py"), "island"])
    return r.returncode


if __name__ == "__main__":
    rc = main(sys.argv[1:])
    if rc in (0, None) and "--previews" not in sys.argv:
        run_placecheck()
    sys.exit(rc)
