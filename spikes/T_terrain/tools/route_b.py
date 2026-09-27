"""Route B (Terrain Builder fallback): write a complete TB input set from the same generated data.

Files (data/T_terrain/route_b/, git-ignored because they are big and regenerated):
  terrain.asc                 ESRI ASCII grid, 512 x 512 at 4 m, xllcorner 200000 (TB's usual easting offset)
  satellite_lco.png + .pgw    2048 x 2048 satellite, 1 m/px, world file puts it on the same frame
  mask_lco.png + .pgw         2048 x 2048 surface mask in the layers.cfg legend colours
  layers.cfg + mapLegend.png  six surfaces -> vanilla surface rvmats
  japantestisland.tml         template library (one template per model used)
  objects.txt                 TB object import: "name";X+200000;Z;yaw;pitch;roll;scale;height (height = ASL of the
                              MLOD origin, same convention as the DayZ-Editor TB exporter)
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

import layers
import terrain

LEGEND = [(172, 211, 115), (255, 240, 76), (0, 128, 0), (0, 0, 0), (127, 127, 127), (150, 90, 40)]
EAST = 200000.0


def export(out_dir, T, s, sat, pl, log):
    os.makedirs(out_dir, exist_ok=True)
    h = T["h"]
    n = h.shape[0]
    lines = ["ncols %d" % n, "nrows %d" % n, "xllcorner %.1f" % EAST, "yllcorner 0.0", "cellsize %.1f" % terrain.CELL,
             "NODATA_value -9999"]
    for j in range(n - 1, -1, -1):                      # ASC rows run north -> south
        lines.append(" ".join("%.2f" % v for v in h[j]))
    with open(os.path.join(out_dir, "terrain.asc"), "wb") as f:
        f.write(("\n".join(lines) + "\n").encode("ascii"))
    Image.fromarray(sat[::-1].astype(np.uint8)).save(os.path.join(out_dir, "satellite_lco.png"))
    lut = np.array(LEGEND, np.uint8)
    Image.fromarray(lut[s[::-1]]).save(os.path.join(out_dir, "mask_lco.png"))
    W = s.shape[0]
    for name in ("satellite_lco.pgw", "mask_lco.pgw"):
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(("1.0\n0.0\n0.0\n-1.0\n%.1f\n%.1f\n" % (EAST + 0.5, W - 0.5)).encode("ascii"))
    cfg = ["class Layers", "{"]
    for (name, rvmat) in layers.SURFACES:
        cfg += ["\tclass %s" % name, "\t{", '\t\tmaterial = "%s";' % rvmat, "\t};"]
    cfg += ["};", "", "class Legend", "{", '\tpicture = "JP\\worlds\\testisland\\source\\mapLegend.png";', "\tclass Colors", "\t{"]
    for (name, _), c in zip(layers.SURFACES, LEGEND):
        cfg.append("\t\t%s[] = {{%d,%d,%d}};" % (name, c[0], c[1], c[2]))
    cfg += ["\t};", "};", ""]
    with open(os.path.join(out_dir, "layers.cfg"), "wb") as f:
        f.write("\n".join(cfg).encode("ascii"))
    leg = Image.new("RGB", (256, 32 * len(LEGEND)), (255, 255, 255))
    d = ImageDraw.Draw(leg)
    for k, ((name, _), c) in enumerate(zip(layers.SURFACES, LEGEND)):
        d.rectangle([(0, 32 * k), (31, 32 * k + 31)], fill=c)
        d.text((40, 32 * k + 10), name, fill=(0, 0, 0))
    leg.save(os.path.join(out_dir, "mapLegend.png"))
    # template library + object import
    models = sorted(set(o["p3d"] for o in pl.objects))
    tml = ['<?xml version="1.0" ?>', '<Library name="JapanTestIsland" shape="rectangle" default_fill="-65408" default_outline="-1" tex="0">']
    for m in models:
        nm = os.path.splitext(os.path.basename(m.replace("\\", "/")))[0]
        tml += ["    <Template>", "        <Name>%s</Name>" % nm, "        <File>%s</File>" % m,
                "        <Date>09/26/26 00:00:00</Date>", "        <Archive></Archive>", "        <Fill>-65408</Fill>",
                "        <Outline>-1</Outline>", "        <Scale>1.000000</Scale>", "        <Hash>%d</Hash>" % (hash(m) & 0x7fffffff),
                "        <ScaleRandMin>0.000000</ScaleRandMin>", "        <ScaleRandMax>0.000000</ScaleRandMax>",
                "        <YawRandMin>0.000000</YawRandMin>", "        <YawRandMax>0.000000</YawRandMax>",
                "        <PitchRandMin>0.000000</PitchRandMin>", "        <PitchRandMax>0.000000</PitchRandMax>",
                "        <RollRandMin>0.000000</RollRandMin>", "        <RollRandMax>0.000000</RollRandMax>",
                "        <TexLLU>0.000000</TexLLU>", "        <TexLLV>0.000000</TexLLV>", "        <TexURU>1.000000</TexURU>",
                "        <TexURV>1.000000</TexURV>", "        <BBRadius>-1.000000</BBRadius>", "        <BBHScale>1.000000</BBHScale>",
                "        <AutoCenter>0</AutoCenter>", "        <XShift>0.000000</XShift>", "        <YShift>0.000000</YShift>",
                "        <ZShift>0.000000</ZShift>", "        <Height>0.000000</Height>",
                '        <BoundingMin X="999.000000" Y="999.000000" Z="999.000000" />',
                '        <BoundingMax X="-999.000000" Y="-999.000000" Z="-999.000000" />',
                '        <BoundingCenter X="-999.000000" Y="-999.000000" Z="-999.000000" />',
                "        <Placement></Placement>", "    </Template>"]
    tml.append("</Library>")
    with open(os.path.join(out_dir, "japantestisland.tml"), "wb") as f:
        f.write(("\n".join(tml) + "\n").encode("ascii"))
    obj = []
    for o in pl.objects:
        nm = os.path.splitext(os.path.basename(o["p3d"].replace("\\", "/")))[0]
        a, u, dv = o["aside"], o["up"], o["dir"]
        sc = float(np.linalg.norm(u))
        yaw = math.degrees(math.atan2(dv[0], dv[2])) % 360.0
        pitch = math.degrees(math.asin(max(-1.0, min(1.0, -dv[1] / sc))))
        roll = math.degrees(math.atan2(a[1], u[1]))
        obj.append('"%s";%.3f;%.3f;%.3f;%.3f;%.3f;%.4f;%.3f;' % (nm, EAST + o["origin"][0], o["origin"][2], yaw, pitch, roll, sc, o["origin"][1]))
    with open(os.path.join(out_dir, "objects.txt"), "wb") as f:
        f.write(("\n".join(obj) + "\n").encode("ascii"))
    log("route B: TB input set in %s (%d objects, %d templates)" % (out_dir, len(obj), len(models)))
