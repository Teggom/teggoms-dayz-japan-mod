"""Procedural textures for the spike-A arms (numpy + Pillow only, no downloads: all original work).

Writes PNGs into src/JP/weapons/data/ (pbo.py skips .png) and converts each to _co.paa with ImageToPAA.
Also writes the rvmats (Super shader, procedural SMDI per material).

  jp_blade_co      256x2048  u: mune(0) -> ha(1), v: tip(0) -> base(1). Itame grain, shinogi-ji, notare hamon, boshi
  jp_tsuka_co      512x1024  u: round the tsuka (0.25 = edge side), v: tsuba(0) -> kashira(1). Samegawa + silk diamonds
  jp_fittings_co   256x256   quadrants: iron | brass / hemp | horn
  jp_lacquer_co    256x512   black urushi with a warm sheen, thin gold bands at the top
  jp_yumi_co       256x2048  u: round the limb, v: top tip(0) -> bottom tip(1). Lacquered bamboo, rattan bands, leather grip
  jp_ya_co         256x1024  u<0.5: bamboo shaft (v: tip(0) -> nock(1)), u>=0.5: feather (v: front(0) -> back(1))
"""
import os
import subprocess

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(HERE)
JAPAN = os.path.dirname(os.path.dirname(SPIKE))
DATA = os.path.join(JAPAN, "src", "JP", "weapons", "data")
IMAGE_TO_PAA = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\ImageToPAA\ImageToPAA.exe"
RNG = np.random.default_rng(20260926)

# rvmat name -> (smdi spec, smdi gloss, specularPower, specular rgb)
MATERIALS = {
    "jp_steel": (0.95, 0.90, 120, 0.55),
    "jp_iron": (0.45, 0.45, 40, 0.25),
    "jp_brass": (0.80, 0.70, 80, 0.45),
    "jp_silk": (0.15, 0.25, 12, 0.08),
    "jp_lacquer": (0.70, 0.75, 70, 0.35),
    "jp_bow": (0.55, 0.60, 50, 0.28),
    "jp_hemp": (0.05, 0.10, 6, 0.03),
    "jp_bamboo": (0.35, 0.45, 30, 0.18),
    "jp_feather": (0.05, 0.10, 6, 0.03),
}


def noise(h, w, scale_h, scale_w, seed=None):
    """smooth value noise in [-1, 1]: low-res random grid upsampled bicubic"""
    r = np.random.default_rng(seed) if seed is not None else RNG
    lo = r.uniform(-1, 1, (max(2, h // scale_h), max(2, w // scale_w))).astype(np.float32)
    im = Image.fromarray(((lo + 1) * 127.5).astype(np.uint8), "L").resize((w, h), Image.BICUBIC)
    return np.asarray(im, np.float32) / 127.5 - 1.0


def save(name, arr):
    os.makedirs(DATA, exist_ok=True)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    png = os.path.join(DATA, name + ".png")
    Image.fromarray(arr, "RGB").save(png)
    return png


def to_paa(png):
    paa = png[:-4] + ".paa"
    r = subprocess.run([IMAGE_TO_PAA, png, paa], cwd=os.path.dirname(png), capture_output=True, text=True)
    if r.returncode != 0 or not os.path.isfile(paa):
        raise SystemExit("ImageToPAA failed for %s: %s %s" % (png, r.stdout, r.stderr))
    return paa


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ katana blade
def blade(kissaki_frac=0.047):
    H, W = 2048, 256
    v = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    u = np.ones((H, 1)) * np.linspace(0, 1, W)[None, :]
    grain = 0.6 * noise(H, W, 64, 6, 1) + 0.4 * noise(H, W, 16, 3, 2)  # itame: stretched along the length
    fine = noise(H, W, 2, 2, 3)
    jigane = np.stack([128 + 10 * grain + 4 * fine, 134 + 10 * grain + 4 * fine, 142 + 11 * grain + 4 * fine], -1)
    # shinogi-ji and mune: burnished darker, fewer grain
    dark = np.stack([98 + 4 * grain, 104 + 4 * grain, 114 + 5 * grain], -1)
    # hamon boundary (notare with gunome), boshi in the kissaki
    b = 0.74 + 0.045 * np.sin(2 * np.pi * v * 11 + 0.4) + 0.025 * np.sin(2 * np.pi * v * 31 + 1.3) + 0.012 * noise(H, W, 32, 256, 4)
    tipzone = v < kissaki_frac
    boshi = 0.62 + 0.25 * (1 - v / kissaki_frac) ** 2
    b = np.where(tipzone, np.minimum(b, boshi), b)
    hard = smoothstep(b - 0.012, b + 0.012, u)
    nioi = np.exp(-((u - b) / 0.012) ** 2)
    frost = np.stack([205 + 8 * fine, 208 + 8 * fine, 214 + 8 * fine], -1)
    col = jigane * (1 - hard[..., None]) + frost * hard[..., None]
    col += (nioi * 35)[..., None]
    # nie sparkles along the boundary
    sp = (RNG.random((H, W)) > 0.985) & (np.abs(u - b) < 0.05)
    col[sp] += 40
    # shinogi-ji / mune zone
    sz = smoothstep(0.26, 0.31, u)
    col = dark * (1 - sz[..., None]) + col * sz[..., None]
    # polished cutting edge
    col = col * (1 - smoothstep(0.965, 0.99, u)[..., None]) + np.array([228, 230, 234]) * smoothstep(0.965, 0.99, u)[..., None]
    # yokote line and ko-shinogi
    yl = np.exp(-((v - kissaki_frac) / 0.0012) ** 2) * (u > 0.28)
    col -= (yl * 45)[..., None]
    return save("jp_blade_co", col)


# ------------------------------------------------------------------ tsuka wrap
def tsuka(n_diamonds=9):
    H, W = 1024, 512
    v = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    u = np.ones((H, 1)) * np.linspace(0, 1, W)[None, :]
    # samegawa: off-white with nodules
    same = np.stack([228 + 0 * u, 224 + 0 * u, 210 + 0 * u], -1) + (6 * noise(H, W, 4, 4, 5))[..., None]
    nod = RNG.random((H // 6, W // 6)) > 0.55
    nod = np.asarray(Image.fromarray((nod * 255).astype(np.uint8)).resize((W, H), Image.NEAREST), np.float32) / 255
    nod = np.asarray(Image.fromarray((nod * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    same += (nod * 14 - 7)[..., None]
    # silk: very dark navy with a diagonal braid
    P = 1.0 / n_diamonds
    vv = (v % P) / P
    braid = 0.5 + 0.5 * np.sin(2 * np.pi * (u * 60 + vv * 12)) * np.sin(2 * np.pi * (u * 60 - vv * 12))
    silk = np.stack([22 + 14 * braid, 24 + 14 * braid, 34 + 18 * braid], -1)
    # diamond windows centred on the two flats (u=0 and 0.5, where the menuki sit), between wrap crossings
    col = silk.copy()
    for uc in (0.0, 0.5):
        du = np.abs(((u - uc + 0.5) % 1.0) - 0.5)
        dv = np.abs(vv - 0.5)
        dia = du / 0.11 + dv / 0.40
        win = dia < 1.0
        edge = np.clip((1.0 - dia) / 0.08, 0, 1)
        col = np.where(win[..., None], same * edge[..., None] + silk * (1 - edge[..., None]), col)
    # crossing twists on the edge and back sides (u = 0.25, 0.75): slightly lighter ridges
    for uc in (0.25, 0.75):
        du = np.abs(((u - uc + 0.5) % 1.0) - 0.5)
        ridge = np.exp(-(du / 0.05) ** 2) * (0.5 + 0.5 * np.cos(2 * np.pi * vv))
        col += (ridge * 18)[..., None]
    # menuki: gold ornaments under the wrap on both flats, seen through two neighbouring windows
    for uc, vc in ((0.0, 0.40), (0.5, 0.52)):
        du = np.abs(((u - uc + 0.5) % 1.0) - 0.5)
        m = ((du / 0.05) ** 2 + ((v - vc) / 0.07) ** 2) < 1.0
        gold = np.stack([175 + 30 * braid, 135 + 25 * braid, 55 + 10 * braid], -1)
        col = np.where((m & (np.sum(col, -1) > 400))[..., None], gold, col)
    return save("jp_tsuka_co", col)


# ------------------------------------------------------------------ fittings atlas
def fittings():
    S = 256
    h = S // 2
    n1 = noise(h, h, 8, 8, 6)
    n2 = noise(h, h, 2, 2, 7)
    iron = np.stack([58 + 10 * n1 + 5 * n2, 54 + 9 * n1 + 5 * n2, 52 + 8 * n1 + 5 * n2], -1)
    rust = (RNG.random((h, h)) > 0.97)
    iron[rust] += np.array([30, 12, 0])
    brass = np.stack([182 + 14 * n1 + 6 * n2, 140 + 12 * n1 + 6 * n2, 62 + 8 * n1 + 4 * n2], -1)
    fib = noise(h, h, 1, 12, 8)
    hemp = np.stack([196 + 14 * fib, 176 + 12 * fib, 128 + 10 * fib], -1)
    horn = np.stack([226 + 8 * n1, 214 + 8 * n1, 180 + 10 * n1], -1)
    top = np.concatenate([iron, brass], 1)
    bot = np.concatenate([hemp, horn], 1)
    return save("jp_fittings_co", np.concatenate([top, bot], 0))


def lacquer():
    H, W = 512, 256
    v = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    n = noise(H, W, 32, 16, 9)
    col = np.stack([26 + 6 * n, 20 + 5 * n, 18 + 4 * n], -1)
    for vc in (0.03, 0.06):  # gold bands just below the collar (top of the shaft = v 0)
        band = np.exp(-((v - vc) / 0.004) ** 2)
        col = col * (1 - band[..., None]) + np.array([185, 145, 60]) * band[..., None]
    return save("jp_lacquer_co", col)


def yumi(bands=(0.035, 0.10, 0.20, 0.30, 0.52, 0.595, 0.79, 0.90, 0.965), grip=(0.628, 0.697)):
    """v: top tip (0) -> bottom tip (1); grip centred at 2/3 of the way down"""
    H, W = 2048, 256
    v = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    u = np.ones((H, 1)) * np.linspace(0, 1, W)[None, :]
    g = noise(H, W, 48, 4, 10)
    # bamboo back/belly faces (u 0..0.25 = back, 0.5..0.75 = belly) natural lacquered, sides darker
    bam = np.stack([150 + 18 * g, 108 + 14 * g, 52 + 8 * g], -1)
    side = np.stack([46 + 6 * g, 32 + 5 * g, 24 + 4 * g], -1)
    s = 0.5 + 0.5 * np.cos(2 * np.pi * u * 2)
    col = bam * s[..., None] + side * (1 - s[..., None])
    for vc in bands:  # rattan wraps
        band = smoothstep(0.0, 0.002, 0.011 - np.abs(v - vc))
        stripes = 0.85 + 0.15 * np.sin(2 * np.pi * v * 900)
        col = col * (1 - band[..., None]) + (np.array([118, 34, 26]) * stripes[..., None]) * band[..., None]
    gz = (v > grip[0]) & (v < grip[1])
    wrap = 0.8 + 0.2 * np.sin(2 * np.pi * (v * 180 + u * 1.0))
    leather = np.stack([92 * wrap, 50 * wrap, 30 * wrap], -1)
    col = np.where(gz[..., None], leather, col)
    return save("jp_yumi_co", col)


def ya(nodes=(0.30, 0.62, 0.90)):
    H, W = 1024, 256
    h = W // 2
    v = np.linspace(0, 1, H)[:, None] * np.ones((1, h))
    u = np.ones((H, 1)) * np.linspace(0, 1, h)[None, :]
    g = noise(H, h, 40, 8, 11)
    shaft = np.stack([196 + 14 * g, 162 + 12 * g, 96 + 8 * g], -1)
    for vc in nodes:  # bamboo nodes
        nb = np.exp(-((v - vc) / 0.004) ** 2)
        shaft -= (nb * 70)[..., None]
    for a, b in ((0.02, 0.05), (0.73, 0.75), (0.88, 0.94)):  # black thread wraps (behind head, around fletching, nock)
        m = (v > a) & (v < b)
        shaft[m] = np.array([30, 24, 22])
    # feather: white vane with dark bars (v along the feather), quill line at u=0
    fu = u
    bars = 0.5 + 0.5 * np.sin(2 * np.pi * (v * 7 + fu * 0.8))
    feather = np.stack([228 - 170 * (bars > 0.72), 224 - 168 * (bars > 0.72), 214 - 160 * (bars > 0.72)], -1).astype(np.float32)
    feather += (noise(H, h, 2, 6, 12) * 10)[..., None]
    quill = np.exp(-(fu / 0.04) ** 2)
    feather = feather * (1 - quill[..., None]) + np.array([240, 236, 226]) * quill[..., None]
    return save("jp_ya_co", np.concatenate([shaft, feather], 1))


RVMAT = """ambient[]={1,1,1,1};
diffuse[]={1,1,1,1};
forcedDiffuse[]={0,0,0,0};
emmisive[]={0,0,0,1};
specular[]={%(sp)s,%(sp)s,%(sp)s,1};
specularPower=%(pw)d;
PixelShaderID="Super";
VertexShaderID="Super";
class Stage1
{
	texture="#(argb,8,8,3)color(0.5,0.5,1,1,NOHQ)";
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
	texture="#(argb,8,8,3)color(0.5,0.5,0.5,1,DT)";
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
	texture="#(argb,8,8,3)color(0,0,0,0,MC)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
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
	texture="#(argb,8,8,3)color(1,%(sm)s,%(gl)s,1,SMDI)";
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
	texture="#(ai,64,64,1)fresnel(0.7,0.8)";
	uvSource="tex";
	class uvTransform
	{
		aside[]={1,0,0};
		up[]={0,1,0};
		dir[]={0,0,0};
		pos[]={0,0,0};
	};
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


def rvmats():
    out = []
    for name, (sm, gl, pw, sp) in MATERIALS.items():
        p = os.path.join(DATA, name + ".rvmat")
        with open(p, "wb") as f:
            f.write((RVMAT % {"sm": sm, "gl": gl, "pw": pw, "sp": sp}).encode("ascii"))
        out.append(p)
    return out


def main():
    pngs = [blade(), tsuka(), fittings(), lacquer(), yumi(), ya()]
    for p in pngs:
        to_paa(p)
        print("texture", os.path.basename(p), Image.open(p).size, "-> paa")
    for p in rvmats():
        print("rvmat", os.path.basename(p))


if __name__ == "__main__":
    main()
