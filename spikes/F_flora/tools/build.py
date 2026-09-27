r"""build.py - the whole F (flora) spike, end to end. Never touches the server or any GUI tool.

    python spikes/F_flora/tools/build.py [--tex] [--no-render] [--no-pack]

  1. (--tex)  textures.py        procedural atlases + bark -> PNG (data/F/work/tex) + PAA (src/JP/plants/*/data)
  2. models                      sakura.py + bamboo.py -> MLOD p3ds in src/JP/plants/*, OBJs in data/F/work/mesh
  3. impostors                   Blender (headless) renders each tree's LOD1 three ways -> *_lod4_ca.paa
  4. rvmats, config.cpp, script  written from the templates below
  5. CfgConvert -test            config syntax check
  6. binarize                    cwd P:\ (P:\JP is a junction to src/JP); ODOL replaces the MLOD in src,
                                 MLOD masters are kept in data/F/work/mlod; logs in data/F/work/binarize_*.log
  7. pack                        tools/common/pbo.py -> ..\@Japan\addons\jp_plants.pbo, prefix JP\plants
  8. test drop-ins               test/placements/F.csv, test/spawns/F.json, test/items/F.txt, test/types/F.xml
  9. (unless --no-render)        Blender preview renders -> spikes/F_flora/renders
"""
import os
import random
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (DEV, SPIKE, WORK, SRC, ADDONS, BINARIZE, CFGCONVERT, BLENDER, P_TREE, P_BAMBOO, P_ITEMS,  # noqa: E402
                    src_dir, write_text)

HERE = os.path.dirname(os.path.abspath(__file__))
UVT = """	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
"""


def stage(n, tex, uv="tex"):
    return "class Stage%d\n{\n\ttexture=\"%s\";\n\tuvSource=\"%s\";\n%s};\n" % (n, tex, uv, UVT)


def rvmat(header, stages):
    return header.strip("\n") + "\n" + "".join(stage(n, t) for n, t in stages)


# --- material parameter blocks, copied from vanilla (named in each comment) -------------------------------------
TRUNK_HDR = """ambient[]={0.02,0.56,0.15000001,0.15000001};
diffuse[]={0.69999999,0.69999999,0.69999999,1};
forcedDiffuse[]={1,1,1,0};
emmisive[]={0.5480004,1,0.46235326,1};
specular[]={0,0,0,8.1956386e-10};
specularPower=1;
PixelShaderID="TreeAdvTrunk";
VertexShaderID="TreeAdvTrunk";
plantWind[]={%s};
"""                       # DZ\plants\tree\data\t_prunusdomestica_2s_trunk.rvmat

LEAF_HDR = """ambient[]={0.059999999,0.55000001,0.5,0.050000001};
diffuse[]={%s};
forcedDiffuse[]={0.3764706,0.26274511,0.89411765,1};
emmisive[]={1.3,1,0.80000001,%s};
specular[]={0.031372551,0.031372551,0.031372551,0.2};
specularPower=300;
PixelShaderID="TreeAdv";
VertexShaderID="TreeAdv";
plantWind[]={%s};
"""                       # DZ\plants\tree\data\t_prunusdomestica_2s_leaves / _lod2 / _lod3.rvmat
LEAF_LOD = {1: ("0.40000001,0.40000001,0.30000001,1.1", "0.25"),
            2: ("0.30000001,0.30000001,0.2,1.3", "0.15000001"),
            3: ("0.2,0.2,0.1,1.5", "0.050000001")}

LOD4_HDR = """ambient[]={0.15000001,0.5,0.58099985,0.15000001};
diffuse[]={0.15000001,0.2,0.2,0.5};
forcedDiffuse[]={1,0.99999934,1,0.73000002};
emmisive[]={1,1,1,0.25};
specular[]={0,0,0,1};
specularPower=300;
PixelShaderID="TreeAdv";
VertexShaderID="TreeAdv";
plantWind[]={0.050000001,0.15000001,0.94999999,0.5};
"""                       # DZ\plants\tree\data\t_prunusdomestica_2s_lod4_ca.rvmat

SUPER_HDR = """ambient[]={1,1,1,1};
diffuse[]={1,1,1,1};
forcedDiffuse[]={0,0,0,0};
emmisive[]={0,0,0,1};
specular[]={0.5,0.5,0.5,1};
specularPower=40;
PixelShaderID="Super";
VertexShaderID="Super";
"""                       # DZ\gear\crafting\data\wooden_stick.rvmat (a little glossier: waxy culm skin)

WIND_PLUM_TRUNK = "0.050000001,0.15000001,0.94999999,0.5"
WIND_PLUM_LEAF = "0.050000001,0.15000001,20.950001,4.5"
WIND_TALL_TRUNK = "0.15000001,0.30000001,0.94999999,0.5"      # t_larixdecidua_3f_trunk: tall, whippy
WIND_BIRCH_LEAF = "0.050000001,0.15000001,40.950001,20.5"     # t_betulapendula_2s_leaves: fluttery
NOHQ_FLAT_LEAF = "#(argb,8,8,3)color(1,1,1,1,NOHQ)"            # what the plum's leaves use
NOHQ_FLAT = "#(argb,8,8,3)color(0.5,0.5,1,1,NOHQ)"
MCA_CONST = "#(argb,8,8,3)color(0.65,0.65,0.65,1,MCA)"         # plum LOD4 uses exactly this
MC_CONST = "#(argb,8,8,3)color(0.5,0.5,0.5,1,MC)"              # hazel trunk uses exactly this


def write_rvmats():
    t = src_dir(P_TREE) + "\\data\\"
    b = src_dir(P_BAMBOO) + "\\data\\"
    i = src_dir(P_ITEMS) + "\\data\\"
    T, B, I = P_TREE + "\\data\\", P_BAMBOO + "\\data\\", P_ITEMS + "\\data\\"
    out = {}
    out[t + "jp_sakura_trunk.rvmat"] = rvmat(TRUNK_HDR % WIND_PLUM_TRUNK, [(1, T + "jp_sakura_bark_nohq.paa"), (2, MC_CONST)])
    for lod, suffix in ((1, ""), (2, "_lod2"), (3, "_lod3")):
        d, e = LEAF_LOD[lod]
        out[t + "jp_sakura_blossom%s.rvmat" % suffix] = rvmat(LEAF_HDR % (d, e, WIND_PLUM_LEAF), [
            (1, NOHQ_FLAT_LEAF), (2, MCA_CONST), (4, T + "jp_sakura_blossom_windmask_co.paa")])
        out[b + "jp_bamboo_leaves%s.rvmat" % suffix] = rvmat(LEAF_HDR % (d, e, WIND_BIRCH_LEAF), [
            (1, NOHQ_FLAT_LEAF), (2, MCA_CONST), (4, B + "jp_bamboo_leaves_windmask_co.paa")])
    out[t + "jp_sakura_lod4.rvmat"] = rvmat(LOD4_HDR, [(1, NOHQ_FLAT), (2, MCA_CONST)])
    out[b + "jp_bamboo_lod4.rvmat"] = rvmat(LOD4_HDR, [(1, NOHQ_FLAT), (2, MCA_CONST)])
    out[b + "jp_bamboo_culm.rvmat"] = rvmat(TRUNK_HDR % WIND_TALL_TRUNK, [(1, B + "jp_bamboo_culm_nohq.paa"), (2, MC_CONST)])
    for name, dt, mc in (("", "0.5", "#(argb,8,8,3)color(0,0,0,0,MC)"),
                         ("_damage", "0.4", "dz\\characters\\data\\generic_wood_damage_mc.paa"),
                         ("_destruct", "0.3", "dz\\characters\\data\\generic_destruct_mc.paa")):
        out[i + "jp_bamboo_pole%s.rvmat" % name] = rvmat(SUPER_HDR, [
            (1, I + "jp_bamboo_pole_nohq.paa"), (2, "#(argb,8,8,3)color(%s,%s,%s,1,DT)" % (dt, dt, dt)), (3, mc),
            (4, "#(argb,8,8,3)color(1,1,1,1,AS)"), (5, "#(argb,8,8,3)color(1,0.35,0.45,1,SMDI)"),
            (6, "#(ai,64,64,1)fresnel(1,0.7)"), (7, "dz\\data\\data\\env_land_co.paa")])
    for path, text in out.items():
        write_text(path, text)
    print("rvmats: %d written" % len(out))


# --- config.cpp ----------------------------------------------------------------------------------------------------
CONFIG = r"""// JP_Plants - spike F (flora) of japan_dev. Generated by spikes/F_flora/tools/build.py; edit the generator.
// One CfgPatches class for this PBO, declared once.
class CfgPatches
{
	class JP_Plants
	{
		units[] = {"JP_Sakura_01_Static", "JP_Sakura_02_Static", "JP_BambooClump_01_Static", "JP_BambooPole"};
		weapons[] = {};
		requiredVersion = 0.1;
		requiredAddons[] = {"DZ_Data", "DZ_Plants", "DZ_Gear_Crafting", "DZ_Scripts"};
	};
};
class CfgMods
{
	class JP_Plants
	{
		dir = "Japan";
		picture = "";
		action = "";
		hideName = 1;
		hidePicture = 1;
		name = "JP Plants";
		credits = "";
		author = "japan_dev";
		authorID = "0";
		version = "0.1";
		extra = 0;
		type = "mod";
		dependencies[] = {"World"};
		class defs
		{
			class worldScriptModule
			{
				value = "";
				files[] = {"JP/plants/scripts/4_World"};
			};
		};
	};
};
class CfgVehicles
{
	class HouseNoDestruct;
	class LongWoodenStick;
	// Runtime-spawnable copies of the plants (object spawner / init.c). Visual fallback only: the engine
	// matches CfgNonAIVehicles by p3d name on TERRAIN objects, so these are never cuttable.
	class JP_Sakura_01_Static: HouseNoDestruct
	{
		scope = 1;
		model = "\JP\plants\tree\jp_sakura_01.p3d";
	};
	class JP_Sakura_02_Static: HouseNoDestruct
	{
		scope = 1;
		model = "\JP\plants\tree\jp_sakura_02.p3d";
	};
	class JP_BambooClump_01_Static: HouseNoDestruct
	{
		scope = 1;
		model = "\JP\plants\bamboo\jp_bamboo_clump_01.p3d";
	};
	// A green bamboo pole. Inherits LongWoodenStick so it gets the stick's in-hands profile (profiles follow
	// class inheritance), its Shoulder/Melee slots, melee modes and every recipe that takes a long stick.
	class JP_BambooPole: LongWoodenStick
	{
		scope = 2;
		displayName = "Bamboo Pole";
		descriptionShort = "A freshly cut length of madake bamboo, about two and a half metres long. Hollow, light for its size and very strong.";
		model = "\JP\plants\items\jp_bamboo_pole.p3d";
		weight = 1800;
		itemSize[] = {1, 10};
		absorbency = 0.2;
		class DamageSystem
		{
			class GlobalHealth
			{
				class Health
				{
					hitpoints = 100;
					healthLevels[] =
					{
						{1.0, {"JP\plants\items\data\jp_bamboo_pole.rvmat"}},
						{0.7, {"JP\plants\items\data\jp_bamboo_pole.rvmat"}},
						{0.5, {"JP\plants\items\data\jp_bamboo_pole_damage.rvmat"}},
						{0.3, {"JP\plants\items\data\jp_bamboo_pole_damage.rvmat"}},
						{0.0, {"JP\plants\items\data\jp_bamboo_pole_destruct.rvmat"}}
					};
				};
			};
		};
	};
};
class CfgNonAIVehicles
{
	class TreeHard;
	class BushHard;
	// <PlantType>_<p3d file name>: the engine gives terrain objects of that p3d this class (see
	// P:\scripts\4_world\entities\core\inherited\plant.c). Values follow vanilla's TreeHard_t_prunusDomestica_2s.
	class TreeHard_jp_sakura_01: TreeHard
	{
		isCuttable = 1;
		primaryDropsAmount = 1;
		secondaryDropsAmount = 1;
		toolDamage = 4;
		cycleTimeOverride = 3;
		primaryOutput = "WoodenLog";
		secondaryOutput = "LongWoodenStick";
	};
	class TreeHard_jp_sakura_02: TreeHard
	{
		isCuttable = 1;
		primaryDropsAmount = 1;
		secondaryDropsAmount = 1;
		toolDamage = 4;
		cycleTimeOverride = 3;
		primaryOutput = "WoodenLog";
		secondaryOutput = "LongWoodenStick";
	};
	// Bamboo as a HARD BUSH: every vanilla blade and axe can cut it (ActionMineBush: hatchet, wood axe,
	// firefighter axe, machete, knives, saws, sickle...), standing or crouched, and its geometry blocks walkers.
	// 3 cycles of 3 s each drop one pole; when it falls, the thin leafy tops drop as a stack of sticks.
	class BushHard_jp_bamboo_clump_01: BushHard
	{
		isCuttable = 1;
		primaryDropsAmount = 3;
		secondaryDropsAmount = 3;
		toolDamage = 4;
		cycleTimeOverride = 3;
		primaryOutput = "JP_BambooPole";
		secondaryOutput = "WoodenStick";
	};
};
"""

SCRIPT = """// JP_Plants script classes. Vanilla declares one script class per cuttable plant config
// (P:\\scripts\\4_world\\entities\\woodbase\\trees.c and bushes.c); these mirror that for our plants.
class TreeHard_jp_sakura_01: TreeHard {};
class TreeHard_jp_sakura_02: TreeHard {};
class BushHard_jp_bamboo_clump_01: BushHard {};
"""


def write_config():
    write_text(os.path.join(SRC, "config.cpp"), CONFIG)
    write_text(os.path.join(SRC, "scripts", "4_World", "JP_Plants", "jp_plants_classes.c"), SCRIPT)
    print("config.cpp + script written")


def cfgconvert_test():
    out = os.path.join(WORK, "config_test.bin")
    r = subprocess.run([CFGCONVERT, "-bin", "-dst", out, os.path.join(SRC, "config.cpp")], capture_output=True, text=True,
                       errors="replace")
    ok = os.path.isfile(out) and r.returncode == 0
    print("CfgConvert:", "OK" if ok else "FAILED", (r.stdout + r.stderr).strip()[-400:])
    if os.path.isfile(out):
        os.remove(out)
    return ok


# --- binarize -------------------------------------------------------------------------------------------------
def binarize(p_rel):
    src = src_dir(p_rel)
    area = p_rel.split("\\")[-1]
    master = os.path.join(WORK, "mlod", area)
    out = os.path.join(WORK, "bin", area)
    os.makedirs(master, exist_ok=True)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p3ds = [f for f in os.listdir(src) if f.lower().endswith(".p3d")]
    for f in p3ds:
        with open(os.path.join(src, f), "rb") as fh:
            if fh.read(4) == b"MLOD":
                shutil.copyfile(os.path.join(src, f), os.path.join(master, f))
    cmd = [BINARIZE, "-always", "-silent", "-addon=P:\\JP\\plants", "-binpath=P:\\bin", "P:\\" + p_rel, out, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = os.path.join(WORK, "binarize_%s.log" % area)
    with open(log, "wb") as fh:
        fh.write((" ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr).encode("utf-8", "replace"))
    bad = [l.strip() for l in (r.stdout + r.stderr).splitlines()
           if any(k in l for k in ("Error", "error", "not loaded", "Cannot", "Warning", "warning"))]
    ok = True
    for f in p3ds:
        o = os.path.join(out, f)
        if os.path.isfile(o) and open(o, "rb").read(4) == b"ODOL":
            shutil.copyfile(o, os.path.join(src, f))
            print("  binarized %-26s ODOL %7d bytes" % (f, os.path.getsize(o)))
        else:
            ok = False
            print("  binarize FAILED for %s (MLOD left in src)" % f)
    for l in bad[:30]:
        print("  log:", l)
    print("  log ->", log)
    return ok


def pack():
    os.makedirs(ADDONS, exist_ok=True)
    pbo = os.path.join(ADDONS, "jp_plants.pbo")
    r = subprocess.run([sys.executable, os.path.join(DEV, "tools", "common", "pbo.py"), "pack", SRC, pbo, "--prefix", "JP\\plants"],
                       capture_output=True, text=True, errors="replace")
    print((r.stdout + r.stderr).strip())
    return r.returncode == 0 and os.path.isfile(pbo)


# --- test drop-ins -----------------------------------------------------------------------------------------------
def write_tests():
    rng = random.Random(42)
    lines = ["p3d,x,z,yaw_deg,y_offset",
             "JP\\plants\\tree\\jp_sakura_01.p3d,985,1010,20,-0.05",
             "JP\\plants\\tree\\jp_sakura_02.p3d,1063,1010,200,-0.05"]
    # 7 bamboo clumps in the grove rectangle x 1080-1110, z 955-995, >= 8 m apart so a player can walk between
    spots = []
    while len(spots) < 7:
        p = (rng.uniform(1083, 1107), rng.uniform(958, 992))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= 8.0 ** 2 for q in spots):
            spots.append(p)
    for x, z in spots:
        lines.append("JP\\plants\\bamboo\\jp_bamboo_clump_01.p3d,%.1f,%.1f,%d,-0.05" % (x, z, rng.randint(0, 359)))
    write_text(os.path.join(DEV, "test", "placements", "F.csv"), "\n".join(lines) + "\n")
    spawns = """{"Objects":[
{"name":"JP_Sakura_01_Static","pos":[1110.0,24.95,1050.0],"ypr":[45,0,0],"scale":1},
{"name":"JP_BambooClump_01_Static","pos":[1110.0,24.95,1068.0],"ypr":[0,0,0],"scale":1}
]}
"""
    write_text(os.path.join(DEV, "test", "spawns", "F.json"), spawns)
    items = """# F (flora): the three vanilla tools that should cut the bamboo, plus two poles to handle
Hatchet
WoodAxe
Machete
JP_BambooPole 2
"""
    write_text(os.path.join(DEV, "test", "items", "F.txt"), items)
    types = """    <type name="JP_BambooPole">
        <nominal>0</nominal>
        <lifetime>14400</lifetime>
        <restock>0</restock>
        <min>0</min>
        <quantmin>-1</quantmin>
        <quantmax>-1</quantmax>
        <cost>100</cost>
        <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="1" deloot="0"/>
        <category name="tools"/>
    </type>
"""
    write_text(os.path.join(DEV, "test", "types", "F.xml"), types)
    print("test drop-ins written (placements %d rows)" % (len(lines) - 1))


def overview():
    """One contact sheet of the renders that matter (renders/F_overview.jpg)."""
    from PIL import Image, ImageDraw
    R = os.path.join(SPIKE, "renders")

    def crop150(n):
        im = Image.open(os.path.join(R, n + ".jpg"))
        w, h = im.size
        return im.crop((w // 2 - 160, h // 2 - 100, w // 2 + 160, h // 2 + 80)).resize((640, 360), Image.NEAREST)

    def fit(n, h=360):
        return Image.open(os.path.join(R, n + ".jpg")).resize((640, h), Image.LANCZOS)
    rows, labels = [], []
    for m in ("jp_sakura_01", "jp_sakura_02", "jp_bamboo_clump_01"):
        rows.append([fit(m + "_005m_lod1"), fit(m + "_030m_lod1"), crop150(m + "_150m_lod3"), crop150(m + "_150m_lod4")])
        labels.append([m + ": 5 m, eye height (LOD1)", m + ": 30 m (LOD1)", m + ": 150 m LOD3 (4x crop)", m + ": 150 m LOD4 impostor (4x crop)"])
    rows.append([fit("jp_bamboo_pole_lods"), fit("jp_bamboo_pole_closeup"), fit("jp_sakura_01_lods", 224), fit("jp_bamboo_clump_01_lods", 224)])
    labels.append(["JP_BambooPole LOD1-3", "pole node + cut end", "sakura_01 LOD1-4", "bamboo LOD1-4"])
    sheet = Image.new("RGB", (640 * 4, 360 * 4), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for r, row in enumerate(rows):
        for c, im in enumerate(row):
            sheet.paste(im, (c * 640, r * 360))
            d.rectangle((c * 640, r * 360, c * 640 + 340, r * 360 + 18), fill=(0, 0, 0))
            d.text((c * 640 + 4, r * 360 + 3), labels[r][c], fill=(255, 255, 255))
    sheet.save(os.path.join(R, "F_overview.jpg"), quality=90)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace", **kw)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit("failed: %s" % cmd)
    return r.stdout


def main(argv):
    py = sys.executable
    if "--tex" in argv:
        print(run([py, os.path.join(HERE, "textures.py")]))
    print(run([py, os.path.join(HERE, "sakura.py")]))
    print(run([py, os.path.join(HERE, "bamboo.py")]))
    run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_blender.py"), "--",
         "impostor", "jp_sakura_01", "jp_sakura_02", "jp_bamboo_clump_01"])
    for m, p in (("jp_sakura_01", P_TREE), ("jp_sakura_02", P_TREE), ("jp_bamboo_clump_01", P_BAMBOO)):
        print(run([py, os.path.join(HERE, "impostor.py"), m, p]).strip())
    write_rvmats()
    write_config()
    ok = cfgconvert_test()
    for p in (P_TREE, P_BAMBOO, P_ITEMS):
        ok = binarize(p) and ok
    if "--no-pack" not in argv:
        ok = pack() and ok
    write_tests()
    if "--no-render" not in argv:
        run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_blender.py"), "--",
             "views", "jp_sakura_01", "jp_sakura_02", "jp_bamboo_clump_01"])
        run([BLENDER, "--background", "--factory-startup", "--python", os.path.join(HERE, "render_blender.py"), "--",
             "item", "jp_bamboo_pole"])
        overview()
        print("renders ->", os.path.join(SPIKE, "renders"))
    print("BUILD", "OK" if ok else "HAD FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
