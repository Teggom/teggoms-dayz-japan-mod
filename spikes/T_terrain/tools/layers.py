"""Surface mask, satellite image and the per-tile layer set (s_/m_ .paa + p_ .rvmat) Terrain Builder would make.

Tile layout (measured on vanilla chernarusplus / enoch and on DayZ-Samples Test_Terrain):
  * a tile is 512 x 512 px with a 16 px overlap on each side, so tiles step 480 px; at 1 m/px that is 480 m
  * tile (c, r): c = column from the WEST, r = row from the NORTH edge; its pixel window starts at
    x = c*480 - 16 and at image row r*480 - 16 (image row 0 = north edge, z = world size)
  * rvmat TexGen3/4 (worldPos): aside = up = 1/512, dir y = -1/512,
    pos = ( -(c*480 - 16)/512 , (W - r*480 + 16)/512 , 0 )
  * a land-grid cell uses the rvmat of the tile containing its centre (tile step must be a multiple of the
    land cell size - 480 / 16 m = 30 here)
Mask encoding (6 surfaces per tile, decoded 2026-09-26 by correlating vanilla m_*_lca tiles with the
engine-reported surface on a 10 m grid over Chernarus, pokemon surface scan):
  slot 0 = black, slot 1 = red, slot 2 = green, slot 3 = blue with alpha 255,
  slot 4 = blue with alpha 128, slot 5 = blue with alpha 0. Other pixels keep alpha 255, except near slot 4/5
  pixels, where Terrain Builder spreads the alpha into the neighbours so bilinear filtering does not blend
  alpha across a blue edge; we dilate the same way (4 px).
The rvmat always carries 6 slot stage pairs (Stage3..Stage14 = nopx/ca per slot); unused slots get texture=""
exactly like vanilla's "_n_" variants.
"""
import os
import subprocess

import numpy as np
from PIL import Image

IMAGE_TO_PAA = r"C:\Program Files (x86)\Steam\steamapps\common\DayZ Tools\Bin\ImageToPAA\ImageToPAA.exe"

# the six surfaces (global layer ids l00..l05) - all base-game Chernarus surfaces, no DLC data
SURFACES = [
    # name, rvmat, nopx, ca
    ("cp_grass", r"dz\surfaces\data\terrain\cp_grass.rvmat"),
    ("cp_grass_tall", r"dz\surfaces\data\terrain\cp_grass_tall.rvmat"),
    ("cp_broadleaf_sparse1", r"dz\surfaces\data\terrain\cp_broadleaf_sparse1.rvmat"),
    ("cp_rock", r"dz\surfaces\data\terrain\cp_rock.rvmat"),
    ("cp_gravel", r"dz\surfaces\data\terrain\cp_gravel.rvmat"),
    ("cp_dirt", r"dz\surfaces\data\terrain\cp_dirt.rvmat"),
]
S_GRASS, S_TALL, S_FOREST, S_ROCK, S_GRAVEL, S_DIRT = range(6)
PREVIEW_COLOURS = [(120, 170, 80), (190, 200, 90), (40, 100, 45), (130, 130, 130), (200, 190, 160), (150, 110, 70)]
SLOT_RGBA = [(0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (0, 0, 255, 128), (0, 0, 255, 0)]

TILE = 512
STEP = 480
OVER = 16


def surface_textures(i):
    name = SURFACES[i][0]
    return r"dz\surfaces\data\terrain\%s_nopx.paa" % name, r"dz\surfaces\data\terrain\%s_ca.paa" % name


def to_paa(png, paa):
    subprocess.run([IMAGE_TO_PAA, png, paa], check=True, capture_output=True)
    return os.path.getsize(paa)


def texture_means(cache_dir):
    """Mean RGB of each surface's _ca texture (converted once with ImageToPAA, cached)."""
    os.makedirs(cache_dir, exist_ok=True)
    out = []
    for i in range(len(SURFACES)):
        ca = surface_textures(i)[1]
        png = os.path.join(cache_dir, os.path.basename(ca).replace(".paa", ".png"))
        if not os.path.isfile(png):
            subprocess.run([IMAGE_TO_PAA, os.path.join("P:\\", ca), png], check=True, capture_output=True)
        a = np.asarray(Image.open(png).convert("RGB")).astype(np.float64)
        out.append(a.reshape(-1, 3).mean(axis=0))
    return np.array(out)


def value_noise(shape, cell, seed, octaves=4):
    """Smooth fractal value noise in [0, 1] (numpy only)."""
    rng = np.random.default_rng(seed)
    h, w = shape
    total = np.zeros(shape)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        c = max(2, cell / (2 ** o))
        gh, gw = int(h / c) + 3, int(w / c) + 3
        g = rng.random((gh, gw))
        yy = np.arange(h) / c
        xx = np.arange(w) / c
        y0 = np.floor(yy).astype(int)
        x0 = np.floor(xx).astype(int)
        fy = (yy - y0)[:, None]
        fx = (xx - x0)[None, :]
        fy = fy * fy * (3 - 2 * fy)
        fx = fx * fx * (3 - 2 * fx)
        a = g[y0][:, x0]
        b = g[y0][:, x0 + 1]
        cc = g[y0 + 1][:, x0]
        d = g[y0 + 1][:, x0 + 1]
        total += amp * ((a * (1 - fx) + b * fx) * (1 - fy) + (cc * (1 - fx) + d * fx) * fy)
        norm += amp
        amp *= 0.5
    return total / norm


def upsample(a, factor):
    """Bilinear upsample of a (row = z) grid defined at vertices k*cell to pixel centres (k + 0.5)/factor."""
    n = a.shape[0]
    m = n * factor
    t = (np.arange(m) + 0.5) / factor
    i0 = np.clip(np.floor(t).astype(int), 0, n - 2)
    f = np.clip(t - i0, 0, 1)
    rows = a[i0] * (1 - f)[:, None] + a[i0 + 1] * f[:, None]
    return rows[:, i0] * (1 - f)[None, :] + rows[:, i0 + 1] * f[None, :]


def classify(T, forest4, pads, paddies, factor=4):
    """Surface index per 1 m pixel, world orientation (row 0 = south). T = terrain.compose() result."""
    h = upsample(T["h"].astype(np.float64), factor)
    gz, gx = np.gradient(h, 1.0)
    slope = np.degrees(np.arctan(np.hypot(gx, gz)))
    d = upsample(T["d"], factor)
    road_d = upsample(T["road_d"], factor)
    canal_d = upsample(T["canal_d"], factor)
    pond_d = upsample(T["pond_d"], factor)
    yard_d = upsample(T["yard_d"], factor)
    forest = upsample(forest4, factor)
    n = h.shape[0]
    Z, X = (np.mgrid[0:n, 0:n] + 0.5)
    s = np.full(h.shape, S_GRASS, np.uint8)
    nz = value_noise(h.shape, 90, 11)
    s[(nz > 0.56) & (h < 90)] = S_TALL
    s[forest > 0.45] = S_FOREST
    rockn = value_noise(h.shape, 25, 12)
    s[(slope > 31 + 8 * rockn) & (h > 3)] = S_ROCK
    s[(d < 95) & (h < 2.6)] = S_GRAVEL
    s[h < 0.3] = S_GRAVEL
    s[canal_d < T["canal_half_width"] + 5.0] = S_GRAVEL
    # paddies: tall-grass fields with dirt bunds
    for (x0, z0, x1, z1, fw, fl) in paddies:
        inside = (X >= x0) & (X < x1) & (Z >= z0) & (Z < z1)
        bund = ((np.mod(X - x0, fw) < 2.0) | (np.mod(Z - z0, fl) < 2.0))
        s[inside & ~bund] = S_TALL
        s[inside & bund] = S_DIRT
    s[road_d < T["road_half_width"] + 1.5] = S_DIRT
    s[(pond_d > T["pond_r"] - 1.0) & (pond_d < T["pond_r"] + 3.0)] = S_DIRT
    for (px, pz, half) in pads:
        s[(np.abs(X - px) < half) & (np.abs(Z - pz) < half)] = S_DIRT
    s[yard_d <= 0.0] = S_DIRT
    return s, h, slope


def sat_colours():
    """Per-surface satellite colour, calibrated on vanilla Chernarus (tools/calibrate_sat.py -> sat_colours.json:
    medians of the vanilla satellite under each decoded mask slot). Vanilla satellites are DARK (grass ~52,52,25);
    the terrain shader brightens them, so matching vanilla values keeps the far view consistent with vanilla maps."""
    import json
    v = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sat_colours.json")))
    return np.array([
        v["cp_grass"],
        [v["cp_grass_tall"][0] + 3, v["cp_grass_tall"][1] + 2, v["cp_grass_tall"][2]],   # a touch lusher than grass
        v["cp_broadleaf_sparse1"],
        [58.0, 55.0, 44.0],                 # rock: vanilla cp_rock (55,49,27) greyed for Hakone andesite
        [70.0, 66.0, 52.0],                 # gravel on land = the grey volcanic shingle beach
        v["cp_dirt"],
    ], float), np.array(v["cp_gravel"], float)


def satellite(s, h, slope, forest, seed=5):
    """1 m/px satellite (world orientation, row 0 = south), float RGB 0..255."""
    cols, seabed = sat_colours()
    base = cols[s]
    nz = value_noise(s.shape, 60, seed) - 0.5
    nz2 = value_noise(s.shape, 12, seed + 1) - 0.5
    nz3 = value_noise(s.shape, 3, seed + 3) - 0.5
    rgb = base * (1.0 + 0.22 * nz[..., None] + 0.14 * nz2[..., None] + 0.10 * nz3[..., None])
    # forest canopy seen from above: dark, varied green where the trees stand (vanilla forest ~30,28,11)
    canopy = np.array([31.0, 33.0, 14.0])
    cf = np.clip((forest - 0.3) / 0.4, 0, 1)[..., None]
    cn = value_noise(s.shape, 6, seed + 2)[..., None]
    rgb = rgb * (1 - cf * 0.9) + canopy * (0.7 + 0.6 * cn) * cf * 0.9
    # gentle baked lighting (vanilla satellites carry a little relief shading)
    gz, gx = np.gradient(h, 1.0)
    sl = np.arctan(np.hypot(gx, gz))
    asp = np.arctan2(-gx, gz)
    hs = np.sin(np.radians(50)) * np.cos(sl) + np.cos(np.radians(50)) * np.sin(sl) * np.cos(np.radians(315) - asp)
    rgb *= (0.85 + 0.2 * np.clip(hs, 0, 1))[..., None]
    # under water: fade to the vanilla sea-floor colour with depth
    depth = np.clip((0.5 - h) / 4.0, 0, 1)[..., None]
    rgb = rgb * (1 - depth) + seabed * (1.0 + 0.15 * nz[..., None]) * depth
    return np.clip(rgb, 0, 255)


def make_tiles(s_world, rgb_world, out_dir, prefix_path, world_size, log):
    """Write s_/m_ tiles (png -> paa) and one rvmat per tile; return {(c, r): rvmat path (P:-relative)}."""
    os.makedirs(out_dir, exist_ok=True)
    s_img = s_world[::-1]                      # image orientation: row 0 = north
    rgb_img = rgb_world[::-1]
    n = s_img.shape[0]
    ntiles = int(np.ceil((world_size - OVER) / STEP))
    pad = TILE
    s_pad = np.pad(s_img, pad, mode="edge")
    rgb_pad = np.pad(rgb_img, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
    rvmats = {}
    stats = []
    for r in range(ntiles):
        for c in range(ntiles):
            y0 = r * STEP - OVER + pad
            x0 = c * STEP - OVER + pad
            st = s_pad[y0:y0 + TILE, x0:x0 + TILE]
            col = rgb_pad[y0:y0 + TILE, x0:x0 + TILE]
            present, counts = np.unique(st, return_counts=True)
            order = [int(p) for p in present[np.argsort(-counts)]]
            assert len(order) <= 6, "more than 6 surfaces in tile %d,%d" % (c, r)
            slot_lut = np.zeros(len(SURFACES), int)
            for k, surf in enumerate(order):
                slot_lut[surf] = k
            mask = np.zeros((TILE, TILE, 4), np.uint8)
            slots = slot_lut[st]
            lut = np.array(SLOT_RGBA, np.uint8)
            mask[:] = lut[slots]
            # alpha spread next to slot 4/5 pixels (TB "gimmick"): non-blue pixels take the alpha of a
            # nearby slot-4/5 pixel
            for sl, a in ((4, 128), (5, 0)):
                near = slots == sl
                if near.any():
                    grown = near.copy()
                    for _ in range(4):
                        g = grown.copy()
                        g[1:] |= grown[:-1]
                        g[:-1] |= grown[1:]
                        g[:, 1:] |= grown[:, :-1]
                        g[:, :-1] |= grown[:, 1:]
                        grown = g
                    notblue = slots < 3
                    mask[grown & notblue, 3] = a
            tag = "%03d_%03d" % (c, r)
            sp = os.path.join(out_dir, "s_%s_lco.png" % tag)
            mp = os.path.join(out_dir, "m_%s_lca.png" % tag)
            Image.fromarray(col.astype(np.uint8)).save(sp)
            Image.fromarray(mask, "RGBA").save(mp)
            to_paa(sp, sp[:-4] + ".paa")
            to_paa(mp, mp[:-4] + ".paa")
            ids = ["l%02d" % order[k] if k < len(order) else "n" for k in range(6)]
            name = "p_%03d-%03d_%s.rvmat" % (c, r, "_".join(ids))
            for old in os.listdir(out_dir):
                if old.startswith("p_%03d-%03d_" % (c, r)) and old.endswith(".rvmat") and old != name:
                    os.remove(os.path.join(out_dir, old))
            with open(os.path.join(out_dir, name), "wb") as f:
                f.write(rvmat_text(c, r, order, prefix_path, tag, world_size).encode("ascii"))
            rvmats[(c, r)] = prefix_path + "\\" + name
            stats.append((tag, [SURFACES[o][0] for o in order]))
    for tag, surf in stats:
        log("  tile %s: %s" % (tag, ", ".join(surf)))
    return rvmats, ntiles


def rvmat_text(c, r, order, prefix_path, tag, world_size):
    px = -(c * STEP - OVER) / float(TILE)
    py = (world_size - r * STEP + OVER) / float(TILE)
    k = 1.0 / TILE
    L = []
    L.append("ambient[]={0.89999998,0.89999998,0.89999998,1};")
    L.append("diffuse[]={0.89999998,0.89999998,0.89999998,1};")
    L.append("forcedDiffuse[]={0.02,0.02,0.02,1};")
    L.append("emmisive[]={0,0,0,0};")
    L.append("specular[]={0,0,0,0};")
    L.append("specularPower=0;")
    L.append("class Stage0\n{\n\ttexture=\"%s\\s_%s_lco.paa\";\n\ttexGen=3;\n};" % (prefix_path, tag))
    L.append("class Stage1\n{\n\ttexture=\"%s\\m_%s_lca.paa\";\n\ttexGen=4;\n};" % (prefix_path, tag))
    for g in (3, 4):
        L.append("class TexGen%d\n{\n\tuvSource=\"worldPos\";\n\tclass uvTransform\n\t{\n\t\taside[]={%.9g,0,0};\n"
                 "\t\tup[]={0,0,%.9g};\n\t\tdir[]={0,%.9g,0};\n\t\tpos[]={%.9g,%.9g,0};\n\t};\n};" % (g, k, k, -k, px, py))
    L.append("class TexGen0\n{\n\tuvSource=\"tex\";\n\tclass uvTransform\n\t{\n\t\taside[]={1,0,0};\n\t\tup[]={0,1,0};\n"
             "\t\tdir[]={0,0,1};\n\t\tpos[]={0,0,0};\n\t};\n};")
    for g in (1, 2):
        L.append("class TexGen%d\n{\n\tuvSource=\"tex\";\n\tclass uvTransform\n\t{\n\t\taside[]={10,0,0};\n\t\tup[]={0,10,0};\n"
                 "\t\tdir[]={0,0,10};\n\t\tpos[]={0,0,0};\n\t};\n};" % g)
    L.append("PixelShaderID=\"TerrainX\";")
    L.append("VertexShaderID=\"Terrain\";")
    L.append("class Stage2\n{\n\ttexture=\"#(rgb,1,1,1)color(0.5,0.5,0.5,1,cdt)\";\n\ttexGen=0;\n};")
    for slot in range(6):
        if slot < len(order):
            nopx, ca = surface_textures(order[slot])
        else:
            nopx, ca = "", ""
        L.append("class Stage%d\n{\n\ttexture=\"%s\";\n\ttexGen=1;\n};" % (3 + 2 * slot, nopx))
        L.append("class Stage%d\n{\n\ttexture=\"%s\";\n\ttexGen=2;\n};" % (4 + 2 * slot, ca))
    return "\n".join(L) + "\n"


def cell_materials(land_range, cell_size, world_size, rvmats, wrp):
    """Fill wrp.material_index: each land cell takes the rvmat of the tile holding its centre."""
    idx = {}
    for (c, r), path in rvmats.items():
        idx[(c, r)] = wrp.add_material(path)
    for j in range(land_range):
        zc = (j + 0.5) * cell_size
        r = int((world_size - zc) // STEP)
        for i in range(land_range):
            xc = (i + 0.5) * cell_size
            c = int(xc // STEP)
            wrp.material_index[j, i] = idx[(c, r)]
