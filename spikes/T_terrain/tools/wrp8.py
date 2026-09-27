"""8WVR (Terrain Builder source world) writer and reader, plus a light OPRW header/object reader.

8WVR layout (community wiki "Wrp File Format - 8WVR", cross-checked against jetelain/bis-file-formats
EditableWrp.cs (MIT) and against Bohemia's own DayZ-Samples Test_Terrain/world/utes.wrp, which this
module reads back byte-exactly):

    char[4]  "8WVR"
    int32    LandRangeX, LandRangeY        material grid (cells), row 0 = SOUTH edge
    int32    TerrainRangeX, TerrainRangeY  heightmap grid (vertices), row 0 = SOUTH edge
    float    CellSize                      metres per LAND cell
    float    Elevation[TerrainRangeY][TerrainRangeX]
    uint16   MaterialIndex[LandRangeY][LandRangeX]   index into the name list below
    int32    nMaterials                    entry 0 is the empty dummy
    nMaterials x { (int32 len, char[len])...  int32 0 }   (a chain of strings; in practice one)
    objects until EOF: { float m[12] (aside, up, dir, position), int32 id, int32 len, char[len] p3d }
    the last object is a dummy with an empty name (NaN matrix)

Verified facts on utes.wrp (2026-09-26):
  * cell (i, j) of the material grid covers x in [i*cs, (i+1)*cs), z in [j*cs, (j+1)*cs)
  * cell -> layer tile: column = floor(x_centre / 480), row = floor((W - z_centre) / 480) (tiles are
    512 px at 1 m/px with a 16 px overlap, counted from the NORTH-west corner)
  * object position y = terrain height + scale * ODOL boundingCenter.y for an upright object whose MLOD
    origin sits on the ground (median error < 0.02 m over 30 vanilla models)
"""
import math
import struct

import numpy as np


def yaw_matrix(yaw_deg, scale=1.0, pitch_deg=0.0, roll_deg=0.0):
    """(aside, up, dir) for a yaw clockwise from north (DayZ convention), optional pitch/roll."""
    t = math.radians(yaw_deg)
    c, s = math.cos(t), math.sin(t)
    aside = np.array([c, 0.0, -s])
    up = np.array([0.0, 1.0, 0.0])
    dirv = np.array([s, 0.0, c])
    if pitch_deg or roll_deg:
        # pitch: rotate up/dir about aside; roll: rotate aside/up about dir
        p = math.radians(pitch_deg)
        up, dirv = up * math.cos(p) - dirv * math.sin(p), up * math.sin(p) + dirv * math.cos(p)
        r = math.radians(roll_deg)
        aside, up = aside * math.cos(r) + up * math.sin(r), -aside * math.sin(r) + up * math.cos(r)
    return aside * scale, up * scale, dirv * scale


class Wrp8:
    def __init__(self, land_range, terrain_range, cell_size):
        self.land_range = int(land_range)
        self.terrain_range = int(terrain_range)
        self.cell_size = float(cell_size)
        self.elevation = np.zeros((self.terrain_range, self.terrain_range), np.float32)
        self.material_index = np.zeros((self.land_range, self.land_range), np.uint16)
        self.materials = [""]          # entry 0 = dummy
        self.objects = []              # (aside, up, dir, pos, id, p3d)

    def add_material(self, path):
        if path in self.materials:
            return self.materials.index(path)
        self.materials.append(path)
        return len(self.materials) - 1

    def add_object(self, p3d, pos, aside, up, dirv):
        oid = len(self.objects)
        self.objects.append((tuple(aside), tuple(up), tuple(dirv), tuple(pos), oid, p3d))
        return oid

    def write(self, path):
        out = bytearray()
        out += b"8WVR"
        out += struct.pack("<4if", self.land_range, self.land_range, self.terrain_range, self.terrain_range,
                           self.cell_size)
        out += np.ascontiguousarray(self.elevation, dtype="<f4").tobytes()
        out += np.ascontiguousarray(self.material_index, dtype="<u2").tobytes()
        out += struct.pack("<i", len(self.materials))
        for m in self.materials:
            if m:
                b = m.encode("latin-1")
                out += struct.pack("<i", len(b)) + b
            out += struct.pack("<i", 0)
        for aside, up, dirv, pos, oid, p3d in self.objects:
            out += struct.pack("<12f", *aside, *up, *dirv, *pos)
            b = p3d.encode("latin-1")
            out += struct.pack("<ii", oid, len(b)) + b
        # dummy terminator, as Terrain Builder and WrpUtil write it
        nan = float("nan")
        out += struct.pack("<12f", nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan)
        out += struct.pack("<ii", 2147483647, 0)
        with open(path, "wb") as f:
            f.write(out)
        return len(out)


def read_8wvr(path):
    d = open(path, "rb").read()
    assert d[:4] == b"8WVR", "not 8WVR"
    lx, ly, tx, ty = struct.unpack_from("<4i", d, 4)
    cs = struct.unpack_from("<f", d, 20)[0]
    off = 24
    elev = np.frombuffer(d, "<f4", tx * ty, off).reshape(ty, tx)
    off += tx * ty * 4
    mat = np.frombuffer(d, "<u2", lx * ly, off).reshape(ly, lx)
    off += lx * ly * 2
    nm = struct.unpack_from("<i", d, off)[0]
    off += 4
    names = []
    for _ in range(nm):
        parts = []
        while True:
            n = struct.unpack_from("<i", d, off)[0]
            off += 4
            if n == 0:
                break
            parts.append(d[off:off + n].decode("latin-1"))
            off += n
        names.append("".join(parts))
    objs = []
    while off < len(d):
        m = struct.unpack_from("<12f", d, off)
        off += 48
        oid, n = struct.unpack_from("<ii", d, off)
        off += 8
        objs.append((m, oid, d[off:off + n].decode("latin-1")))
        off += n
    return dict(land=(lx, ly), terrain=(tx, ty), cell=cs, elev=elev, mat=mat, names=names, objects=objs)


def read_oprw_summary(path):
    """Header, model table and object records of a binarized DayZ OPRW (v29 layout checked on
    chernarusplus.wrp / enoch.wrp): 'OPRW', int version, char[4] tag ('0FNE'), int appId, byte, int
    LandRangeX/Y, TerrainRangeX/Y, float CellSize. Objects are 60-byte records (id, model index,
    float[12]) found by shape (same method as pokemon_dev/tools/spawns/extract_world_objects.py)."""
    import re
    d = open(path, "rb").read()
    info = {"sig": d[:4].decode("latin-1"), "size": len(d)}
    if d[:4] != b"OPRW":
        return info
    info["version"] = struct.unpack_from("<i", d, 4)[0]
    info["tag"] = d[8:12].decode("latin-1", "replace")
    info["appid"] = struct.unpack_from("<i", d, 12)[0]
    lx, ly, tx, ty = struct.unpack_from("<4i", d, 17)
    info["land"] = (lx, ly)
    info["terrain"] = (tx, ty)
    info["cell"] = struct.unpack_from("<f", d, 33)[0]
    m = re.search(rb"[\x20-\x7e]{3,}\.p3d\x00", d)
    models = []
    if m:
        start = m.start()
        count = struct.unpack_from("<I", d, start - 4)[0]
        off = start
        for _ in range(count):
            end = d.index(b"\x00", off)
            models.append(d[off:end].decode("latin-1"))
            off = end + 1
        info["models_end"] = off
    info["models"] = models
    # rvmat names (asciiz + major byte) - just list every rvmat string in the file
    info["rvmats"] = sorted(set(x.decode("latin-1") for x in re.findall(rb"[\x20-\x7e]{4,}\.rvmat", d)))
    return info


def oprw_objects(data, n_models, search_from, min_run=1):
    """(model index, x, y, z, up_y) arrays of the placed objects - longest run of plausible 60-byte records."""
    rec = 15
    best = (0, 0)
    for phase in range(4):
        base = search_from + phase
        nw = (len(data) - base) // 4
        u = np.frombuffer(data, dtype="<u4", count=nw, offset=base)
        f = np.frombuffer(data, dtype="<f4", count=nw, offset=base)
        n = nw - rec
        if n <= 0:
            continue
        ok = u[1:n + 1] < n_models
        for k in range(2, 11):
            av = np.abs(f[k:n + k])
            ok &= (av <= 100.0) & ((av == 0) | (av >= 1e-20))
        x, y, z = f[11:n + 11], f[12:n + 12], f[13:n + 13]
        ok &= (x > -5000.0) & (x < 60000.0) & (z > -5000.0) & (z < 60000.0) & (y > -2000.0) & (y < 10000.0)
        for r in range(rec):
            v = ok[r::rec].astype(np.int8)
            if not v.any():
                continue
            dd = np.diff(np.concatenate(([0], v, [0])))
            starts = np.where(dd == 1)[0]
            ends = np.where(dd == -1)[0]
            k = int(np.argmax(ends - starts))
            length = int(ends[k] - starts[k])
            if length > best[0]:
                best = (length, base + 4 * (r + rec * int(starts[k])))
    count, off = best
    if count < min_run:
        return None
    dt = np.dtype([("id", "<u4"), ("mi", "<u4"), ("m", "<f4", (12,)), ("sp", "<u4")])
    a = np.frombuffer(data, dtype=dt, count=count, offset=off)
    return a
