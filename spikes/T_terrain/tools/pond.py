"""Pond model (MLOD) modelled on vanilla dz\\water\\ponds\\lake_50x50.p3d, whose ODOL carries:
  LODs 1.0 (visual), 1e13 (geometry), 1e15 (memory), 3e15 (roadway); bbox flat at y = 0
  visual   : faces textured dz\\data\\data\\normalmap1_dxt5.paa + material dz\\water\\ponds\\data\\water_lake.rvmat
             (CalmWater shader), named property lodnoshadow = 1
  geometry : named properties class = pond, damage = no; no components (no closed solids)
  roadway  : faces textured dz\\surfaces\\data\\roadway\\water_ext.paa (the water surface type)
Ours is a flat 32-gon of radius R at y = 0 (origin = water level at the pond centre). Visual and roadway faces are
written in both windings (cheap insurance - a water plane seen from below while swimming is fine).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "common"))
import mlod  # noqa: E402

VIS_TEX = r"dz\data\data\normalmap1_dxt5.paa"
VIS_MAT = r"dz\water\ponds\data\water_lake.rvmat"
ROAD_TEX = r"dz\surfaces\data\roadway\water_ext.paa"


def disc(lod, radius, sides, tex, mat, both=True):
    c = lod.add_point((0.0, 0.0, 0.0))
    ring = [lod.add_point((radius * math.cos(2 * math.pi * k / sides), 0.0, radius * math.sin(2 * math.pi * k / sides)))
            for k in range(sides)]
    up = lod.add_normal((0.0, 1.0, 0.0))
    dn = lod.add_normal((0.0, -1.0, 0.0))

    def uv(p):
        x, _, z = lod.points[p]
        return 0.5 + x / (2 * radius) * 4, 0.5 - z / (2 * radius) * 4

    for k in range(sides):
        a, b = ring[k], ring[(k + 1) % sides]
        # clockwise seen from above (+y): centre -> b -> a  (angle increases counter-clockwise from +x to +z)
        lod.add_face([(c, up) + uv(c), (b, up) + uv(b), (a, up) + uv(a)], tex, mat)
        if both:
            lod.add_face([(c, dn) + uv(c), (a, dn) + uv(a), (b, dn) + uv(b)], tex, mat)


def write_pond(path, radius, sides=32):
    vis = mlod.Lod(1.0)
    disc(vis, radius, sides, VIS_TEX, VIS_MAT)
    vis.properties["lodnoshadow"] = "1"
    geo = mlod.Lod(mlod.LOD_GEOMETRY)
    for k in range(4):
        a = 2 * math.pi * k / 4
        geo.add_point((radius * math.cos(a), 0.0, radius * math.sin(a)))
    geo.properties["class"] = "pond"
    geo.properties["damage"] = "no"
    mem = mlod.Lod(mlod.LOD_MEMORY)
    mem.add_point((0.0, 0.0, 0.0))
    road = mlod.Lod(mlod.LOD_ROADWAY)
    disc(road, radius, sides, ROAD_TEX, "")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mlod.write_mlod(path, [vis, geo, mem, road])
    return path
