"""Minimal writer (and reader, for round-trip checks) for Bohemia MLOD .p3d files.

parts agent copy (2026-09-27) of spikes/B_building/tools/mlod_b.py, unchanged except this line.

mlod_b.py: agent B's copy of japan_dev/tools/common/mlod.py (2026-09-26), extended for buildings:
  - verified conventions (from Bohemia's DayZ-Samples Test_Building MLOD, see REPORT.md):
      * closed components: the formula normal (b-a)x(c-a) of every face points INTO the solid
        (= faces clockwise seen from outside); Roadway faces therefore have formula normal pointing DOWN;
      * Object Builder stores that same formula normal as the face-vertex normal;
      * door leaves: one ComponentNN each in Geometry, plus the bone selection (doorsN) on the same faces.
  - Lod.add_closed_solid(): adds a closed convex polyhedron with shared points and fixes the winding.
  - Lod.add_flat_face(): adds one face with its own points (flat-shaded visual LODs), winding fixed from
    the wanted outward normal.
  - lod_name(), approx resolution matching, component_report() (closed + convex test) used by verify_b.py.

Coordinate convention inside a p3d: X right, Y up, Z forward (left-handed). Faces are
listed clockwise when seen from the outside. UV origin is top-left (v grows downward).

Layout written here (matches Object Builder's own output well enough that O2Script's
loadP3D reads it back - see validate_p3d.bio2s):

  "MLOD" u32 version=257  u32 lodCount
  per LOD:
    "P3DM" u32 28  u32 256  u32 nPoints  u32 nNormals  u32 nFaces  u32 flags=0
    nPoints  x { f32 x,y,z  u32 pointFlags }
    nNormals x { f32 x,y,z }
    nFaces   x { u32 nVerts  4 x { u32 pointIdx  u32 normalIdx  f32 u  f32 v }  u32 faceFlags  asciiz texture  asciiz material }
    "TAGG"
    taggs: { u8 active=1  asciiz name  u32 size  u8 data[size] }  ...  "#EndOfFile#" (size 0)
    f32 resolution
Tagg payloads:
  named selection : nPoints bytes of weight (0 = out, 1 = 100 %, 2..255 = (256-b)/255) then nFaces bytes (1 = face in selection)
  #Property#      : 64-byte zero-padded name + 64-byte zero-padded value
  #Mass#          : nPoints x f32
  #SharpEdges#    : pairs of u32 point indices
"""
import math
import struct

LOD_VISUAL_1 = 1.0
LOD_GEOMETRY = 1.0e13
LOD_MEMORY = 1.0e15
LOD_LANDCONTACT = 2.0e15
LOD_ROADWAY = 3.0e15
LOD_PATHS = 4.0e15
LOD_HITPOINTS = 5.0e15
LOD_VIEW_GEOMETRY = 6.0e15
LOD_FIRE_GEOMETRY = 7.0e15


def encode_weight(w):
    if w <= 0.0:
        return 0
    if w >= 0.998:
        return 1
    v = int(round(256.0 - 255.0 * w))
    return max(2, min(255, v))


def decode_weight(b):
    if b == 0:
        return 0.0
    if b == 1:
        return 1.0
    return (256 - b) / 255.0


class Lod:
    def __init__(self, resolution):
        self.resolution = float(resolution)
        self.points = []        # [(x, y, z)]
        self.point_flags = []   # [u32]
        self.normals = []       # [(x, y, z)]
        self.faces = []         # [(verts, flags, texture, material)] verts = [(pointIdx, normalIdx, u, v), ...] 3 or 4 entries
        self.selections = {}    # name -> ({pointIdx: weight}, set(faceIdx))
        self.properties = {}    # name -> value (str)
        self.mass = None        # [f32] per point
        self.sharp_edges = []   # [(a, b)]

    # -- building helpers -------------------------------------------------
    def add_point(self, xyz, flags=0):
        self.points.append((float(xyz[0]), float(xyz[1]), float(xyz[2])))
        self.point_flags.append(flags)
        return len(self.points) - 1

    def add_normal(self, xyz):
        self.normals.append((float(xyz[0]), float(xyz[1]), float(xyz[2])))
        return len(self.normals) - 1

    def add_face(self, verts, texture="", material="", flags=0):
        assert len(verts) in (3, 4), "faces must be tris or quads"
        self.faces.append((list(verts), flags, texture, material))
        return len(self.faces) - 1

    def select(self, name, point_weights=None, face_indices=None):
        pw, fs = self.selections.setdefault(name, ({}, set()))
        if point_weights:
            for pi, w in point_weights.items():
                if w > 0:
                    pw[pi] = max(pw.get(pi, 0.0), float(w))
        if face_indices:
            fs.update(face_indices)

    # -- building helpers (agent B) ----------------------------------------
    def add_flat_face(self, pts, outward, uvs, texture="", material="", flags=0):
        """One planar face with its own points. `outward` = the geometric normal the face should show to.
        Returns (face index, [point indices])."""
        pts = [tuple(float(c) for c in p) for p in pts]
        n = _face_formula_normal(pts)
        if _dot(n, outward) > 0:           # p3d wants the formula normal pointing inward
            pts = pts[::-1]
            uvs = uvs[::-1]
            n = (-n[0], -n[1], -n[2])
        nn = _normalize(n)
        ni = self.add_normal(nn)
        pis = [self.add_point(p) for p in pts]
        verts = [(pi, ni, uv[0], uv[1]) for pi, uv in zip(pis, uvs)]
        return self.add_face(verts, texture, material, flags), pis

    def add_closed_solid(self, verts, faces, texture="", material="", face_materials=None):
        """A closed convex polyhedron with shared points (Geometry / View / Fire LODs).
        verts: [(x,y,z)]; faces: [[i,..]] (3 or 4 each, any winding). Returns (point indices, face indices)."""
        c = tuple(sum(v[k] for v in verts) / len(verts) for k in range(3))
        pis = [self.add_point(v) for v in verts]
        fis = []
        for k, f in enumerate(faces):
            fp = [verts[i] for i in f]
            n = _face_formula_normal(fp)
            fc = tuple(sum(p[j] for p in fp) / len(fp) for j in range(3))
            out = _sub(fc, c)
            order = list(f)
            if _dot(n, out) > 0:
                order = order[::-1]
                n = (-n[0], -n[1], -n[2])
            ni = self.add_normal(_normalize(n))
            mat = face_materials[k] if face_materials else material
            fis.append(self.add_face([(pis[i], ni, 0.0, 0.0) for i in order], texture, mat))
        return pis, fis

    def faces_fully_inside(self, name):
        """Mark faces whose every point is in selection `name` as selected faces."""
        pw, fs = self.selections[name]
        for fi, (verts, _, _, _) in enumerate(self.faces):
            if all(v[0] in pw for v in verts):
                fs.add(fi)

    # -- serialisation ----------------------------------------------------
    def write(self, f):
        f.write(b"P3DM")
        f.write(struct.pack("<IIIIII", 28, 256, len(self.points), len(self.normals), len(self.faces), 0))
        for p, fl in zip(self.points, self.point_flags):
            f.write(struct.pack("<fffI", p[0], p[1], p[2], fl))
        for n in self.normals:
            f.write(struct.pack("<fff", n[0], n[1], n[2]))
        for verts, flags, tex, mat in self.faces:
            f.write(struct.pack("<I", len(verts)))
            for i in range(4):
                if i < len(verts):
                    pi, ni, u, v = verts[i]
                    f.write(struct.pack("<IIff", pi, ni, u, v))
                else:
                    f.write(struct.pack("<IIff", 0, 0, 0.0, 0.0))
            f.write(struct.pack("<I", flags))
            f.write(tex.encode("ascii") + b"\x00")
            f.write(mat.encode("ascii") + b"\x00")
        f.write(b"TAGG")

        def tagg(name, data):
            f.write(b"\x01" + name.encode("ascii") + b"\x00" + struct.pack("<I", len(data)) + data)

        if self.sharp_edges:
            tagg("#SharpEdges#", b"".join(struct.pack("<II", a, b) for a, b in self.sharp_edges))
        for name, (pw, fs) in self.selections.items():
            data = bytearray(len(self.points) + len(self.faces))
            for pi, w in pw.items():
                data[pi] = encode_weight(w)
            for fi in fs:
                data[len(self.points) + fi] = 1
            tagg(name, bytes(data))
        for k, v in self.properties.items():
            tagg("#Property#", k.encode("ascii").ljust(64, b"\x00")[:64] + str(v).encode("ascii").ljust(64, b"\x00")[:64])
        if self.mass is not None:
            assert len(self.mass) == len(self.points)
            tagg("#Mass#", struct.pack("<%df" % len(self.mass), *self.mass))
        tagg("#EndOfFile#", b"")
        f.write(struct.pack("<f", self.resolution))


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _normalize(a):
    l = math.sqrt(_dot(a, a)) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def _face_formula_normal(pts):
    """Newell's method: robust (b-a)x(c-a)-direction normal for a planar polygon (not normalised)."""
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[(i + 1) % len(pts)]
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    return (nx, ny, nz)


LOD_NAMES = [(LOD_GEOMETRY, "Geometry"), (LOD_MEMORY, "Memory"), (LOD_LANDCONTACT, "LandContact"),
             (LOD_ROADWAY, "Roadway"), (LOD_PATHS, "Paths"), (LOD_HITPOINTS, "HitPoints"),
             (LOD_VIEW_GEOMETRY, "View Geometry"), (LOD_FIRE_GEOMETRY, "Fire Geometry")]


def same_res(a, b):
    return abs(a - b) <= abs(b) * 1e-5 + 1e-6


def lod_name(res):
    for v, n in LOD_NAMES:
        if same_res(res, v):
            return n
    if res < 1e4:
        return "Resolution %g" % res
    return "LOD %g" % res


def find_lod(lods, res):
    for l in lods:
        if same_res(l.resolution, res):
            return l
    return None


def component_report(lod, name):
    """Closed-and-convex test for one ComponentNN selection. Returns list of problems (empty = OK)."""
    pw, fs = lod.selections[name]
    probs = []
    pts = sorted(pw)
    # closed: every edge used by exactly two faces, in opposite directions
    edges = {}
    for fi in fs:
        vs = [v[0] for v in lod.faces[fi][0]]
        for i in range(len(vs)):
            e = (vs[i], vs[(i + 1) % len(vs)])
            edges[e] = edges.get(e, 0) + 1
    for (a, b), cnt in edges.items():
        if cnt != 1 or edges.get((b, a), 0) != 1:
            probs.append("open or non-manifold edge %d-%d" % (a, b))
            break
    # convex: every point on or behind every face plane (formula normal points inward -> points must be on
    # the positive side of the inward normal)
    for fi in fs:
        fp = [lod.points[v[0]] for v in lod.faces[fi][0]]
        n = _normalize(_face_formula_normal(fp))
        for pi in pts:
            d = _dot(_sub(lod.points[pi], fp[0]), n)
            if d < -1e-3:
                probs.append("not convex: point %d is %.4f m outside face %d" % (pi, -d, fi))
                break
        if len(probs) > 3:
            break
    # planar faces
    for fi in fs:
        fp = [lod.points[v[0]] for v in lod.faces[fi][0]]
        if len(fp) == 4:
            n = _normalize(_face_formula_normal(fp))
            if abs(_dot(_sub(fp[3], fp[0]), n)) > 1e-3:
                probs.append("non-planar quad %d" % fi)
    return probs


def write_mlod(path, lods):
    with open(path, "wb") as f:
        f.write(b"MLOD" + struct.pack("<II", 257, len(lods)))
        for lod in lods:
            lod.write(f)


# ---------------------------------------------------------------------------
# reader (used only for self-checks)
# ---------------------------------------------------------------------------
def _cstr(data, off):
    e = data.index(b"\x00", off)
    return data[off:e].decode("latin-1"), e + 1


def read_mlod(path):
    data = open(path, "rb").read()
    assert data[:4] == b"MLOD", "not MLOD"
    version, n = struct.unpack_from("<II", data, 4)
    off = 12
    lods = []
    for _ in range(n):
        assert data[off:off + 4] == b"P3DM", "bad LOD header at %d" % off
        maj, mino, npt, nnm, nfc, flags = struct.unpack_from("<IIIIII", data, off + 4)
        off += 28
        lod = Lod(0)
        for _ in range(npt):
            x, y, z, fl = struct.unpack_from("<fffI", data, off); off += 16
            lod.points.append((x, y, z)); lod.point_flags.append(fl)
        for _ in range(nnm):
            lod.normals.append(struct.unpack_from("<fff", data, off)); off += 12
        for _ in range(nfc):
            nv = struct.unpack_from("<I", data, off)[0]; off += 4
            verts = []
            for i in range(4):
                pi, ni, u, v = struct.unpack_from("<IIff", data, off); off += 16
                if i < nv:
                    verts.append((pi, ni, u, v))
            fl = struct.unpack_from("<I", data, off)[0]; off += 4
            tex, off = _cstr(data, off)
            mat, off = _cstr(data, off)
            lod.faces.append((verts, fl, tex, mat))
        assert data[off:off + 4] == b"TAGG"; off += 4
        while True:
            active = data[off]; off += 1
            name, off = _cstr(data, off)
            size = struct.unpack_from("<I", data, off)[0]; off += 4
            payload = data[off:off + size]; off += size
            if name == "#EndOfFile#":
                break
            if name == "#Property#":
                k = payload[:64].split(b"\x00")[0].decode("latin-1"); v = payload[64:128].split(b"\x00")[0].decode("latin-1")
                lod.properties[k] = v
            elif name == "#Mass#":
                lod.mass = list(struct.unpack_from("<%df" % (size // 4), payload))
            elif name == "#SharpEdges#":
                lod.sharp_edges = [struct.unpack_from("<II", payload, i) for i in range(0, size, 8)]
            elif name.startswith("#"):
                pass
            else:
                pw = {i: decode_weight(b) for i, b in enumerate(payload[:npt]) if b}
                fs = {i for i, b in enumerate(payload[npt:npt + nfc]) if b}
                lod.selections[name] = (pw, fs)
        lod.resolution = struct.unpack_from("<f", data, off)[0]; off += 4
        lods.append(lod)
    assert off == len(data), "trailing bytes: %d" % (len(data) - off)
    return lods


if __name__ == "__main__":
    import sys
    for lod in read_mlod(sys.argv[1]):
        print("LOD %.6g: %d points, %d normals, %d faces, props=%s, mass=%s" % (
            lod.resolution, len(lod.points), len(lod.normals), len(lod.faces), lod.properties,
            None if lod.mass is None else round(sum(lod.mass), 2)))
        texs = sorted({(f[2], f[3]) for f in lod.faces})
        for t in texs:
            print("   texture=%r material=%r" % t)
        for name, (pw, fs) in lod.selections.items():
            print("   sel %-20s points=%5d faces=%5d wsum=%.1f" % (name, len(pw), len(fs), sum(pw.values())))
