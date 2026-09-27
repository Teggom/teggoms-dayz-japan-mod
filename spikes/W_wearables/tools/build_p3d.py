"""W build: garments -> MLOD p3ds (+ model.cfg, rvmats, config.cpp) -> binarize -> jp_characters.pbo

usage: python build_p3d.py [--no-binarize] [--no-pack] [--items kasa,kimono_short,kimono_long,tabi]

Writes game-ready files into src/JP/characters (= P:\\JP\\characters), MLOD copies into data/W/work/mlod,
binarize logs into data/W/work, and packs @Japan/addons/jp_characters.pbo with tools/common/pbo.py.
Never touches the server or the game.
"""
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mlod_w as mlod  # noqa: E402
from modelcfg import model_cfg  # noqa: E402
from wlib import SRC, WORK, DEV, BINARIZE, CFGCONVERT  # noqa: E402

REL = "JP\\characters"
PBO_OUT = os.path.join(os.path.dirname(DEV), "@Japan", "addons", "jp_characters.pbo")
SKIN_TEX = "#(argb,8,8,3)color(0.843137,0.768627,0.658824,1.0,co)"
SKIN_MAT = "dz\\characters\\heads\\data\\hhl_dummy_skin_material.rvmat"
PEN_CLOTH = "dz\\data\\data\\penetration\\fabric_thin.rvmat"

# item -> folder, texture stem, damage macro textures (vanilla, by slot), physics mass (kg)
ITEMS = {
    "kasa": {"dir": "kasa", "tex": "jp_kasa", "mass": 0.37,
             "mc": ("dz\\characters\\vests\\data\\vests_damage_mc.paa", "dz\\characters\\data\\generic_destruct_mc.paa")},
    "kimono_short": {"dir": "kimono", "tex": "jp_kimono_short", "mass": 0.8,
                     "mc": ("dz\\characters\\tops\\data\\tops_damage_mc.paa", "dz\\characters\\tops\\data\\tops_destruct_mc.paa")},
    "kimono_long": {"dir": "kimono", "tex": "jp_kimono_long", "mass": 1.3,
                    "mc": ("dz\\characters\\tops\\data\\tops_damage_mc.paa", "dz\\characters\\tops\\data\\tops_destruct_mc.paa")},
    "tabi": {"dir": "tabi", "tex": "jp_tabi_waraji", "mass": 0.6,
             "mc": ("dz\\characters\\shoes\\data\\shoes_damage_mc.paa", "dz\\characters\\shoes\\data\\shoes_destruct_mc.paa")},
}

RVMAT = """ambient[]={1,1,1,1};
diffuse[]={1,1,1,1};
forcedDiffuse[]={0,0,0,1};
emmisive[]={0,0,0,1};
specular[]={%(spec)s,%(spec)s,%(spec)s,0};
specularPower=%(power)d;
PixelShaderID="Super";
VertexShaderID="Super";
class Stage1
{
	texture="%(nohq)s";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage2
{
	texture="#(argb,8,8,3)color(0.5,0.5,0.5,0.5,DT)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage3
{
	texture="%(mc)s";
	uvSource="tex";
	class uvTransform
	{
		aside[]={%(mcscale)s,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage4
{
	texture="#(argb,8,8,3)color(1,1,1,1,AS)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage5
{
	texture="%(smdi)s";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
class Stage6
{
	texture="%(fresnel)s";
	uvSource="none";
};
class Stage7
{
	texture="dz\\data\\data\\env_land_co.paa";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
};
"""


def data_rel(item, name):
    return "%s\\%s\\data\\%s" % (REL, ITEMS[item]["dir"], name)


def write_rvmats(item):
    it = ITEMS[item]
    d = os.path.join(SRC, it["dir"], "data")
    base = {"nohq": data_rel(item, it["tex"] + "_nohq.paa"), "smdi": data_rel(item, it["tex"] + "_smdi.paa")}
    variants = {
        "": dict(spec="0.2", power=30, mc="#(argb,8,8,3)color(0,0,0,0,MC)", mcscale="1", fresnel="#(ai,32,128,1)fresnel(1.5,0.7)"),
        "_damage": dict(spec="0.15", power=30, mc=it["mc"][0], mcscale="2", fresnel="#(ai,32,128,1)fresnel(1.5,0.7)"),
        "_destruct": dict(spec="0.35", power=30, mc=it["mc"][1], mcscale="2", fresnel="#(ai,64,64,1)fresnel(1.37,0.25)"),
    }
    out = {}
    for suf, v in variants.items():
        p = os.path.join(d, it["tex"] + suf + ".rvmat")
        with open(p, "wb") as f:
            f.write((RVMAT % dict(base, **v)).encode())
        out[suf] = data_rel(item, it["tex"] + suf + ".rvmat")
    return out


def add_box(lod, lo, hi, sel="Component01", material=""):
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    corners = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    pis = [lod.add_point(c) for c in corners]
    # MLOD winding (outward = -cross): same quads as pokemon build_item.add_box, which is proven in game
    quads = [((0, 1, 2, 3), (0, 0, -1)), ((7, 6, 5, 4), (0, 0, 1)), ((4, 5, 1, 0), (0, -1, 0)),
             ((3, 2, 6, 7), (0, 1, 0)), ((0, 3, 7, 4), (-1, 0, 0)), ((5, 6, 2, 1), (1, 0, 0))]
    fis = []
    for q, n in quads:
        ni = lod.add_normal(n)
        fis.append(lod.add_face([(pis[i], ni, 0.0, 0.0) for i in q], material=material))
    lod.select(sel, {pi: 1.0 for pi in pis}, fis)
    return pis


def garment_lod(g, resolution, looks, camo, weighted):
    """looks: material key -> (texture, rvmat, selection)"""
    lod = mlod.Lod(resolution)
    P = g.arrays()
    N = g.normals()
    for p in P:
        lod.add_point(p)
    for n in N:
        lod.add_normal(n)
    sel_faces = {}
    for fi, (f, uv, m) in enumerate(zip(g.F, g.FUV, g.FM)):
        tex, mat, sel = looks[m]
        lod.add_face([(v, v, u_[0], u_[1]) for v, u_ in zip(f, uv)], texture=tex, material=mat)
        sel_faces.setdefault(sel, []).append(fi)
    for sel, fis in sel_faces.items():
        if sel == "camo":
            sel = camo
        pts = {v: 1.0 for fi in fis for v in g.F[fi]}
        lod.select(sel, pts, fis)
    if weighted:
        for i, ws in enumerate(g.W):
            for b, w in ws.items():
                lod.select(b, {i: w})
    lod.properties["lodnoshadow"] = "1"
    return lod


def bbox(g):
    P = g.arrays()
    return P.min(0), P.max(0)


def worn_p3d(path, lods_g, looks, camo, geo_box, mass):
    lods = [garment_lod(g, float(i + 1), looks, camo, True) for i, g in enumerate(lods_g)]
    geo = mlod.Lod(mlod.LOD_GEOMETRY)
    pis = add_box(geo, *geo_box)
    geo.mass = [mass / len(pis)] * len(pis)
    geo.properties["autocenter"] = "0"
    lods.append(geo)
    mlod.write_mlod(path, lods)
    return lods


def ground_p3d(path, lods_g, looks, mass):
    lods = [garment_lod(g, float(i + 1), looks, "camoGround", False) for i, g in enumerate(lods_g)]
    lo, hi = bbox(lods_g[0])
    geo = mlod.Lod(mlod.LOD_GEOMETRY)
    pis = add_box(geo, lo, hi)
    geo.mass = [mass / len(pis)] * len(pis)
    geo.properties["autocenter"] = "0"
    mem = mlod.Lod(mlod.LOD_MEMORY)
    c = (lo + hi) / 2
    r = float(np.linalg.norm(hi - lo) / 2)
    for name, p in (("invview", c + np.array([0.0, r * 1.2, -r * 1.6])), ("ce_center", c),
                    ("ce_radius", c + np.array([r, 0, 0])), ("boundingbox_min", lo), ("boundingbox_max", hi)):
        i = mem.add_point(p)
        mem.select(name, {i: 1.0})
    view = mlod.Lod(mlod.LOD_VIEW_GEOMETRY)
    add_box(view, lo, hi)
    fire = mlod.Lod(mlod.LOD_FIRE_GEOMETRY)
    add_box(fire, lo, hi, material=PEN_CLOTH)
    lods += [geo, mem, view, fire]
    mlod.write_mlod(path, lods)
    return lods


# ------------------------------------------------------------------------------------------ items
def build_kasa(rv):
    import kasa
    it = ITEMS["kasa"]
    tex = data_rel("kasa", it["tex"] + "_co.paa")
    looks = {"straw": (tex, rv[""], "camo")}
    lods = [kasa.build(48, 10), kasa.build(24, 5, knob=True), kasa.build(12, 3, knob=False)]
    lo, hi = bbox(lods[0])
    out = {}
    for sex, camo in (("m", "camoMale"), ("f", "camoFemale")):
        name = "jp_kasa_" + sex
        worn_p3d(os.path.join(SRC, it["dir"], name + ".p3d"), lods, looks, camo, (lo, hi), it["mass"])
        out[name] = "worn"
    import ground
    ground_p3d(os.path.join(SRC, it["dir"], "jp_kasa_g.p3d"), [ground.kasa_g(g) for g in lods[:2]], looks, it["mass"])
    out["jp_kasa_g"] = "ground"
    return out, lods[0]


def build_kimono(rv, length):
    import kimono_parts
    import ground
    item = "kimono_" + length
    it = ITEMS[item]
    tex = data_rel(item, it["tex"] + "_co.paa")
    out = {}
    first = None
    for sex, camo in (("m", "camoMale"), ("f", "camoFemale")):
        # long robe: skirt mode B (below the knee it also follows the shins) - chosen from the pose renders,
        # see REPORT.md "the long robe"
        mode = "B" if length == "long" else "A"
        lods = [kimono_parts.build_full(sex, length, lod, mode) for lod in (0, 1, 2)]
        looks = {m: (tex, rv[""], "camo") for m in set(lods[0].FM) | set(lods[2].FM)}
        looks["skin"] = (SKIN_TEX, SKIN_MAT, "personality")
        P = lods[0].arrays()
        core = P[(np.abs(P[:, 0]) < 0.2) & (P[:, 1] > 0.98) & (P[:, 1] < 1.55)]
        name = "jp_%s_%s" % (item, sex)
        worn_p3d(os.path.join(SRC, it["dir"], name + ".p3d"), lods, looks, camo, (core.min(0), core.max(0)), it["mass"])
        out[name] = "worn"
        first = first or lods[0]
    g = ground.kimono_g(length)
    looks = {m: (tex, rv[""], "camo") for m in set(g.FM)}
    ground_p3d(os.path.join(SRC, it["dir"], "jp_%s_g.p3d" % item), [g], looks, it["mass"])
    out["jp_%s_g" % item] = "ground"
    return out, first


def build_tabi(rv):
    import tabi
    import ground
    it = ITEMS["tabi"]
    tex = data_rel("tabi", it["tex"] + "_co.paa")
    looks = {"tabi": (tex, rv[""], "camo")}
    out = {}
    worn_m = None
    for sex, camo in (("m", "camoMale"), ("f", "camoFemale")):
        lods = [tabi.build_item(sex, lod) for lod in (0, 1, 2)]
        name = "jp_tabi_waraji_" + sex
        lo, hi = bbox(lods[0])
        worn_p3d(os.path.join(SRC, it["dir"], name + ".p3d"), lods, looks, camo, (lo, hi), it["mass"])
        out[name] = "worn"
        if sex == "m":
            worn_m = lods
    ground_p3d(os.path.join(SRC, it["dir"], "jp_tabi_waraji_g.p3d"), [ground.tabi_g(worn_m[0]), ground.tabi_g(worn_m[1])], looks, it["mass"])
    out["jp_tabi_waraji_g"] = "ground"
    return out, worn_m[0]


# ------------------------------------------------------------------------------------------ binarize
def binarize_dir(sub):
    src_dir = os.path.join(SRC, sub)
    mlod_dir = os.path.join(WORK, "mlod", sub)
    os.makedirs(mlod_dir, exist_ok=True)
    for f in os.listdir(src_dir):
        if f.endswith(".p3d"):
            data = open(os.path.join(src_dir, f), "rb").read(4)
            if data == b"MLOD":
                shutil.copyfile(os.path.join(src_dir, f), os.path.join(mlod_dir, f))
    out = os.path.join(WORK, "bin_" + sub)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    cmd = [BINARIZE, "-always", "-silent", "-addon=P:\\JP", "-binpath=P:\\bin", "P:\\%s\\%s" % (REL, sub), out, "*.p3d"]
    r = subprocess.run(cmd, cwd="P:\\", capture_output=True, text=True, errors="replace")
    log = " ".join(cmd) + "\n\n" + r.stdout + "\n" + r.stderr
    open(os.path.join(WORK, "binarize_%s.log" % sub), "wb").write(log.encode())
    bad = [l for l in log.splitlines() if ("rror" in l or "Cannot" in l or "arning" in l) and "Trying to access" not in l
           and "No entry" not in l]
    ok = []
    for root, _, files in os.walk(out):
        for f in files:
            if f.endswith(".p3d"):
                p = os.path.join(root, f)
                if open(p, "rb").read(4) == b"ODOL":
                    shutil.copyfile(p, os.path.join(src_dir, f))
                    ok.append(f)
    return ok, bad


def cfgconvert_check():
    out = os.path.join(WORK, "config_check.bin")
    r = subprocess.run([CFGCONVERT, "-bin", "-dst", out, os.path.join(SRC, "config.cpp")], capture_output=True, text=True, errors="replace")
    return r.returncode == 0 and os.path.isfile(out), (r.stdout + r.stderr).strip()


def main(argv):
    items = ["kasa", "kimono_short", "kimono_long", "tabi"]
    if "--items" in argv:
        items = argv[argv.index("--items") + 1].split(",")
    import configgen
    models = {}
    for item in items:
        rv = write_rvmats(item)
        if item == "kasa":
            m, _ = build_kasa(rv)
        elif item.startswith("kimono"):
            m, _ = build_kimono(rv, item.split("_")[1])
        else:
            m, _ = build_tabi(rv)
        models.update(m)
        print("built", item, sorted(m))
    # model.cfg per folder (every model of W listed; binarize reads the nearest one)
    allm = configgen.all_models()
    cfg = model_cfg([m for m, k in allm.items() if k == "worn"], [m for m, k in allm.items() if k == "ground"])
    for sub in {"kasa", "kimono", "tabi"}:
        with open(os.path.join(SRC, sub, "model.cfg"), "wb") as f:
            f.write(cfg.encode())
    configgen.write_config()
    ok, msg = cfgconvert_check()
    print("CfgConvert:", "OK" if ok else "FAILED", msg[-400:])
    if "--no-binarize" not in argv:
        for sub in sorted({ITEMS[i]["dir"] for i in items}):
            done, bad = binarize_dir(sub)
            print("binarize %s: %d ODOL %s" % (sub, len(done), sorted(done)))
            for l in bad[:20]:
                print("   ", l.strip())
    if "--no-pack" not in argv:
        r = subprocess.run([sys.executable, os.path.join(DEV, "tools", "common", "pbo.py"), "pack", SRC, PBO_OUT, "--prefix", REL],
                           capture_output=True, text=True)
        print(r.stdout.strip(), r.stderr.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
