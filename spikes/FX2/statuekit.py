"""statuekit.py - FX2 (2026-10-01): sculpted statue meshes for the prop kits.

Stephen (wave-2 walk): 'any humanoid statue should have a picture reference and more care'. Statues are modelled as
signed-distance shapes (sdf.py, numpy) from the photo references (research/statues/REFS.md, NOTES.md), meshed by
surface nets, every vertex projected onto the true surface, then reduced to the face budget by Blender's quadric
decimation (headless, symmetric about x), one target per LOD. Result: a closed, smooth-shaded triangle mesh.

  mesh(name, build, lods=(3000, 1100, 380), res=..., sym=True)  -> {lod_index: (verts, tris)}   (cached)
  solids(meshdata, mat, vis_map, t=..., s=..., ...)             -> kit Solids (smooth normals, world uvs)

Parts: a statue is a list of PARTS, each its own SDF + bounding box + voxel size (the face 2 mm, the robe 6 mm), so
fine detail costs nothing where it isn't. Parts may overlap (the neck sinks into the robe); each is a closed mesh.

Cache: spikes/FX2/meshes/<name>.json (verts + tris per LOD, 4-decimal metres), keyed by a hash of the part's
build source and parameters; committed, so the prop builds run without Blender when nothing changed.
"""
import hashlib
import inspect
import json
import math
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
MESHES = os.path.join(HERE, "meshes")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
KIT_VERSION = "fx2-2"
sys.path.insert(0, HERE)
import sdf  # noqa: E402,F401


# ================================================================================================ surface nets
def sample(node, lo, hi, h):
    lo = np.asarray(lo, float) - 2 * h
    hi = np.asarray(hi, float) + 2 * h
    n = np.maximum(np.ceil((hi - lo) / h).astype(int) + 1, 3)
    xs = lo[0] + h * np.arange(n[0])
    ys = lo[1] + h * np.arange(n[1])
    zs = lo[2] + h * np.arange(n[2])
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    P = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
    F = np.empty(len(P))
    step = 400000
    for i in range(0, len(P), step):
        F[i:i + step] = node(P[i:i + step])
    F = F.reshape(n)
    # the boundary is outside (closed meshes)
    F[0, :, :] = F[-1, :, :] = F[:, 0, :] = F[:, -1, :] = F[:, :, 0] = F[:, :, -1] = abs(h)
    return F, lo, h


def surface_nets(F, lo, h):
    nx, ny, nz = F.shape
    inside = F < 0
    acc = np.zeros((nx - 1, ny - 1, nz - 1, 3))
    cnt = np.zeros((nx - 1, ny - 1, nz - 1))
    edges = []
    for ax in range(3):
        sl0 = [slice(None)] * 3
        sl1 = [slice(None)] * 3
        sl0[ax] = slice(0, -1)
        sl1[ax] = slice(1, None)
        f0, f1 = F[tuple(sl0)], F[tuple(sl1)]
        m = (f0 < 0) != (f1 < 0)
        idx = np.argwhere(m)
        t = f0[m] / (f0[m] - f1[m])
        pos = idx.astype(float)
        pos[:, ax] += t
        pts = lo + pos * h
        edges.append((ax, idx, (f0[m] < 0)))
        # the four cells round this edge
        o = [a for a in range(3) if a != ax]
        for d0 in (0, 1):
            for d1 in (0, 1):
                c = idx.copy()
                c[:, o[0]] -= d0
                c[:, o[1]] -= d1
                ok = np.all(c >= 0, 1) & (c[:, 0] < nx - 1) & (c[:, 1] < ny - 1) & (c[:, 2] < nz - 1)
                cc = c[ok]
                np.add.at(acc, (cc[:, 0], cc[:, 1], cc[:, 2]), pts[ok])
                np.add.at(cnt, (cc[:, 0], cc[:, 1], cc[:, 2]), 1)
    act = cnt > 0
    vid = -np.ones(cnt.shape, int)
    vid[act] = np.arange(act.sum())
    V = acc[act] / cnt[act][:, None]
    quads = []
    flips = []
    for ax, idx, neg in edges:
        o = [a for a in range(3) if a != ax]
        cs = []
        okall = np.ones(len(idx), bool)
        for d0, d1 in ((0, 0), (1, 0), (1, 1), (0, 1)):
            c = idx.copy()
            c[:, o[0]] -= d0
            c[:, o[1]] -= d1
            ok = np.all(c >= 0, 1) & (c[:, 0] < nx - 1) & (c[:, 1] < ny - 1) & (c[:, 2] < nz - 1)
            okall &= ok
            cs.append(c)
        q = np.stack([vid[c[:, 0].clip(0, nx - 2), c[:, 1].clip(0, ny - 2), c[:, 2].clip(0, nz - 2)] for c in cs], 1)
        q = q[okall]
        quads.append(q)
        flips.append(neg[okall])
    Q = np.concatenate(quads)
    return V, Q


def grad(node, P, e):
    g = np.zeros_like(P)
    for a in range(3):
        d = np.zeros(3)
        d[a] = e
        g[:, a] = (node(P + d) - node(P - d)) / (2 * e)
    return g


def project(node, V, h, iters=3):
    for _ in range(iters):
        f = node(V)
        g = grad(node, V, h * 0.5)
        gg = np.maximum((g * g).sum(1), 1e-12)
        step = (f / gg)[:, None] * g
        nrm = np.linalg.norm(step, axis=1)
        k = np.minimum(1.0, (0.7 * h) / np.maximum(nrm, 1e-12))
        V = V - step * k[:, None]
    return V


def orient(node, V, Q, h):
    """Flip each quad so its normal points out of the shape (along the SDF gradient)."""
    c = V[Q].mean(1)
    n = np.cross(V[Q[:, 2]] - V[Q[:, 0]], V[Q[:, 3]] - V[Q[:, 1]])
    g = grad(node, c, h * 0.5)
    flip = (n * g).sum(1) < 0
    Q = Q.copy()
    Q[flip] = Q[flip][:, ::-1]
    return Q


def mesh_part(node, lo, hi, h):
    F, lo2, h = sample(node, lo, hi, h)
    V, Q = surface_nets(F, lo2, h)
    V = project(node, V, h)
    Q = orient(node, V, Q, h)
    # drop degenerate quads (two equal vertices)
    good = np.array([len(set(q)) == 4 for q in Q.tolist()]) if len(Q) else np.zeros(0, bool)
    return V, Q[good]


# ================================================================================================ Blender decimation
BLENDER_SCRIPT = r'''
import bpy, json, sys
jobs = json.load(open(sys.argv[sys.argv.index("--") + 1]))
for job in jobs:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=job["src"], forward_axis="NEGATIVE_Z", up_axis="Y")
    ob = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=job.get("merge", 1e-5))
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode="OBJECT")
    if job.get("remesh"):
        ob.data.remesh_voxel_size = job["remesh"]
        ob.data.remesh_voxel_adaptivity = 0.0
        bpy.ops.object.voxel_remesh()
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode="OBJECT")
    for tgt, out in zip(job["targets"], job["outs"]):
        cp = ob.copy()
        cp.data = ob.data.copy()
        bpy.context.collection.objects.link(cp)
        n = len(cp.data.polygons)
        if tgt < n:
            m = cp.modifiers.new("dec", "DECIMATE")
            m.decimate_type = "COLLAPSE"
            m.ratio = max(0.0005, tgt / float(n))
            m.use_symmetry = job.get("sym", True)
            m.symmetry_axis = "X"
            m.use_collapse_triangulate = True
        for o in bpy.context.selected_objects:
            o.select_set(False)
        cp.select_set(True)
        bpy.context.view_layer.objects.active = cp
        bpy.ops.wm.obj_export(filepath=out, export_selected_objects=True, apply_modifiers=True,
                              export_normals=False, export_uv=False, export_materials=False,
                              forward_axis="NEGATIVE_Z", up_axis="Y", export_triangulated_mesh=True)
        bpy.data.objects.remove(cp)
'''


def write_obj(fp, V, F):
    lines = ["v %.5f %.5f %.5f" % tuple(v) for v in V]
    lines += ["f " + " ".join(str(i + 1) for i in f) for f in F]
    with open(fp, "wb") as f:
        f.write(("\n".join(lines) + "\n").encode())


def read_obj(fp):
    V, F = [], []
    for ln in open(fp, encoding="utf-8"):
        if ln.startswith("v "):
            V.append([float(x) for x in ln.split()[1:4]])
        elif ln.startswith("f "):
            F.append([int(x.split("/")[0]) - 1 for x in ln.split()[1:]])
    return np.array(V), F


def decimate(jobs):
    """jobs: [(V, Q, [targets], sym, remesh_voxel)] -> [[(V, tris) per target]]"""
    tmp = tempfile.mkdtemp(prefix="fx2dec_", dir=os.path.join(HERE, "_build") if os.path.isdir(
        os.path.join(HERE, "_build")) else None)
    spec = []
    for i, job in enumerate(jobs):
        V, Q, targets, sym = job[:4]
        rem = job[4] if len(job) > 4 else None
        src = os.path.join(tmp, "in%d.obj" % i)
        write_obj(src, V, Q)
        spec.append({"src": src, "targets": list(targets), "sym": sym, "remesh": rem,
                     "outs": [os.path.join(tmp, "out%d_%d.obj" % (i, k)) for k in range(len(targets))]})
    jp = os.path.join(tmp, "jobs.json")
    with open(jp, "wb") as f:
        f.write(json.dumps(spec).encode())
    sp = os.path.join(tmp, "dec.py")
    with open(sp, "wb") as f:
        f.write(BLENDER_SCRIPT.encode())
    r = subprocess.run([BLENDER, "--background", "--factory-startup", "--python", sp, "--", jp],
                       capture_output=True, text=True)
    res = []
    for s in spec:
        outs = []
        for o in s["outs"]:
            if not os.path.isfile(o):
                raise RuntimeError("Blender decimation failed:\n" + r.stdout[-3000:] + r.stderr[-3000:])
            outs.append(read_obj(o))
        res.append(outs)
    for fn in os.listdir(tmp):
        os.remove(os.path.join(tmp, fn))
    os.rmdir(tmp)
    return res


# ================================================================================================ parts + cache
class Part:
    """One closed piece of a statue: node (sdf), box (lo, hi), voxel h, share = its fraction of each LOD's faces."""

    def __init__(self, key, node, lo, hi, h, share=1.0, sym=True, mat=None, min_faces=12):
        self.key, self.node, self.lo, self.hi, self.h = key, node, lo, hi, h
        self.share, self.sym, self.mat, self.min_faces = share, sym, mat, min_faces


def _hash(obj):
    return hashlib.sha1(repr(obj).encode()).hexdigest()[:16]


def statue(name, build, lods=(3000, 1100, 380), params=None, force=False):
    """build(**params) -> [Part]. Returns {"parts": [{"key", "mat", "lods": [(V, tris), ...]}], "faces": [...]}.
    Cached in meshes/<name>.json under a hash of (build source, params, lods, KIT_VERSION)."""
    params = params or {}
    src = inspect.getsource(build)
    key = _hash((KIT_VERSION, src, sorted(params.items()), tuple(lods), _deps_src()))
    fp = os.path.join(MESHES, name + ".json")
    if os.path.isfile(fp) and not force:
        d = json.load(open(fp, encoding="utf-8"))
        if d.get("key") == key:
            return _load(d)
    parts = build(**params)
    tot = sum(p.share for p in parts)
    jobs = []
    for p in parts:
        V, Q = mesh_part(p.node, p.lo, p.hi, p.h)
        tg = [max(p.min_faces, int(round(L * p.share / tot))) for L in lods]
        jobs.append((V, Q, tg, False, p.h))   # voxel remesh (manifold) then free (non-symmetric) decimation
        print("  %s.%s: %d verts %d quads -> %s" % (name, p.key, len(V), len(Q), tg), flush=True)
    dec = decimate(jobs)
    out = {"key": key, "name": name, "lods": list(lods), "parts": []}
    for p, d in zip(parts, dec):
        out["parts"].append({"key": p.key, "mat": p.mat,
                             "lods": [{"v": np.round(V, 4).tolist(), "f": [list(map(int, f)) for f in F]}
                                      for V, F in d]})
    os.makedirs(MESHES, exist_ok=True)
    with open(fp, "wb") as f:
        f.write(json.dumps(out, separators=(",", ":")).encode())
    return _load(out)


def _deps_src():
    # the whole modelling source: a change to a shared head / helper rebuilds every statue that might use it
    return "".join(open(os.path.join(HERE, f), encoding="utf-8").read() for f in ("sdf.py", "figures.py"))


def _load(d):
    parts = []
    for p in d["parts"]:
        parts.append({"key": p["key"], "mat": p["mat"],
                      "lods": [(np.array(l["v"], float), [tuple(f) for f in l["f"]]) for l in p["lods"]]})
    faces = [sum(len(p["lods"][i][1]) for p in parts) for i in range(len(d["lods"]))]
    return {"parts": parts, "faces": faces, "name": d["name"]}


# ================================================================================================ to kit solids
def smooth_normals(V, F, crease=80.0):
    V = np.asarray(V, float)
    Fa = np.array(F, int)
    fn = np.cross(V[Fa[:, 1]] - V[Fa[:, 0]], V[Fa[:, 2]] - V[Fa[:, 0]])
    area = np.linalg.norm(fn, axis=1)
    fnu = fn / np.maximum(area, 1e-12)[:, None]
    vn = np.zeros_like(V)
    for k in range(3):
        np.add.at(vn, Fa[:, k], fn)
    vn /= np.maximum(np.linalg.norm(vn, axis=1), 1e-12)[:, None]
    cosc = math.cos(math.radians(crease))
    out = []
    for i, f in enumerate(Fa):
        q = []
        for k in range(3):
            n = vn[f[k]]
            q.append(tuple(n) if float(n @ fnu[i]) > cosc else tuple(fnu[i]))
        out.append(q)
    return fnu, out


def to_solids(md, lod, mats, vis, M=None, t=(0.0, 0.0, 0.0), s=1.0, sz=1.0, wear=None, keep=None):
    """The statue's parts at LOD index `lod` as kit sheets (visual only) in LOD set `vis`.
    mats: one material or {part_key: material}; M: 3x3 rotation (sdf.rotm); s uniform scale; sz extra z scale
    (relief); keep: optional predicate on part key."""
    sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
    from jpparts import core
    t = np.asarray(t, float)
    Mr = np.eye(3) if M is None else np.asarray(M, float)
    out = []
    for p in md["parts"]:
        if keep and not keep(p["key"]):
            continue
        V, F = p["lods"][min(lod, len(p["lods"]) - 1)]
        if not len(F):
            continue
        W_ = V * np.array([s, s, s * sz])
        W_ = W_ @ Mr.T + t
        fnu, vnl = smooth_normals(W_, F)
        polys = [[tuple(W_[i]) for i in f] for f in F]
        mat = mats.get(p["key"], mats.get("*")) if isinstance(mats, dict) else mats
        sh = core.sheet(polys, mat, [tuple(n) for n in fnu], vis=vis)
        sh.finalize()
        sh.vn = vnl
        sh.fx2part = p["key"]
        if wear:
            sh.wear = wear
        out.append(sh)
    return out


def bbox(md, lod=0):
    allv = np.concatenate([p["lods"][lod][0] for p in md["parts"] if len(p["lods"][lod][1])])
    return allv.min(0), allv.max(0)
