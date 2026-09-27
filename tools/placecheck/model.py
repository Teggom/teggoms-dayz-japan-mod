"""placecheck: per-model grounding profiles, the class -> p3d index and category assignment.

A profile is extracted once from a binarized (ODOL) p3d and cached by the file's SHA-1 in
data/placecheck/profiles/<sha1>.npz, so it is recomputed only when the model file changes. It holds:
  * bbox, boundingCenter (bc) and the MLOD origin in the ODOL frame (= -bc; the model's design ground line)
  * the ODOL named property "class" (tree, bush, road, house, ...), if any
  * low_<lod>: contact candidates per LOD kind (landcontact / visual / geometry): the vertices and edge samples
    (0.25 m) of the bottom part of that LOD, in the ODOL frame (= the engine frame of a placed object)
  * memory points (selection centroids of the memory LOD) and a "top" point (fallback hang point)
  * roadway and geometry meshes (triangles) for object-on-object tests
All coordinates are ODOL-frame metres: x right, y up, z forward. A placed object's world point is
pos + x*aside + y*up + z*dir (aside/up/dir carry the scale), which is how the .wrp stores it and how
CreateObjectEx + SetOrientation place a spawner object.
"""
import hashlib
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import odol_read  # noqa: E402  (copy of spikes/A_arms/tools/odol.py)

DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = os.path.join(DEV, "data", "placecheck")
PROFILE_VERSION = 2
LOD_KINDS = {"geometry": 1e13, "memory": 1e15, "landcontact": 2e15, "roadway": 3e15}
EXTRACT_ROOT = r"D:\DayZToolsExtract"


def wb(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def norm_p3d(p3d):
    s = p3d.strip().strip('"').replace("/", "\\").lstrip("\\")
    if s and not s.lower().endswith(".p3d"):
        s += ".p3d"
    return s


def p3d_file(p3d):
    """P:-relative p3d -> file on disk (P:, then japan_dev/src for JP\\, then the extract for DZ\\)."""
    s = norm_p3d(p3d)
    cands = [os.path.join("P:\\", s)]
    low = s.lower()
    if low.startswith("jp\\"):
        cands.append(os.path.join(DEV, "src", s))
    else:
        cands.append(os.path.join(EXTRACT_ROOT, s))
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


# ------------------------------------------------------------------------------------------ hashing
class HashMemo:
    """SHA-1 of model files, memoised by (size, mtime) so unchanged files are not re-read every run."""

    def __init__(self):
        self.path = os.path.join(CACHE, "file_hashes.json")
        try:
            self.d = json.load(open(self.path, "rb"))
        except (OSError, ValueError):
            self.d = {}
        self.dirty = False

    def sha1(self, full):
        st = os.stat(full)
        k = os.path.abspath(full).lower()
        e = self.d.get(k)
        if e and e[0] == st.st_size and e[1] == st.st_mtime_ns:
            return e[2]
        h = hashlib.sha1(open(full, "rb").read()).hexdigest()
        self.d[k] = [st.st_size, st.st_mtime_ns, h]
        self.dirty = True
        return h

    def save(self):
        if self.dirty:
            wb(self.path, json.dumps(self.d, indent=0))
            self.dirty = False


# ------------------------------------------------------------------------------------------ geometry helpers
def fps(pts, k):
    """Farthest-point subsample (indices), deterministic, starting from the lowest point."""
    n = len(pts)
    if n <= k:
        return np.arange(n)
    first = int(np.argmin(pts[:, 1]))
    chosen = [first]
    d = ((pts - pts[first]) ** 2).sum(1)
    for _ in range(k - 1):
        j = int(d.argmax())
        chosen.append(j)
        d = np.minimum(d, ((pts - pts[j]) ** 2).sum(1))
    return np.array(chosen)


def tris(faces):
    out = []
    for f in faces:
        if len(f) == 3:
            out.append(f)
        elif len(f) == 4:
            out.append((f[0], f[1], f[2]))
            out.append((f[0], f[2], f[3]))
    return np.array(out, np.int32).reshape(-1, 3)


def low_points(V, faces, keep, step=0.25, cap=1024):
    """Vertices + edge samples of the part of a LOD within `keep` m of its lowest point."""
    V = np.asarray(V, np.float64)
    ymin = V[:, 1].min()
    inb = V[:, 1] <= ymin + keep
    pts = [V[inb]]
    edges = set()
    for f in faces:
        k = len(f)
        for i in range(k):
            a, b = f[i], f[(i + 1) % k]
            if inb[a] and inb[b]:
                edges.add((a, b) if a < b else (b, a))
    for a, b in edges:
        L = float(np.linalg.norm(V[a] - V[b]))
        n = int(L / step)
        if n >= 1:
            t = (np.arange(1, n + 1) / (n + 1))[:, None]
            pts.append(V[a] + t * (V[b] - V[a]))
    P = np.unique(np.round(np.vstack(pts), 3), axis=0)
    if len(P) > cap:
        P = P[fps(P, cap)]
    return P.astype(np.float32)


# ------------------------------------------------------------------------------------------ profiles
class Profiles:
    def __init__(self):
        self.memo = HashMemo()
        self.mem = {}
        self.by_p3d = {}

    def get(self, p3d):
        """Profile dict for a P:-relative p3d, or None if the file is missing or unreadable."""
        key = norm_p3d(p3d).lower()
        if key in self.by_p3d:
            return self.by_p3d[key]
        full = p3d_file(p3d)
        prof = None
        if full:
            sha = self.memo.sha1(full)
            prof = self.mem.get(sha) or self._load(sha)
            if prof is None:
                try:
                    prof = extract(full, sha)
                except Exception as ex:  # noqa: BLE001
                    prof = {"sha1": sha, "error": "%s: %s" % (type(ex).__name__, ex)}
                self._save(prof)
            prof["p3d"] = norm_p3d(p3d)
            self.mem[sha] = prof
        self.by_p3d[key] = prof
        return prof

    def _file(self, sha):
        return os.path.join(CACHE, "profiles", sha + ".npz")

    def _load(self, sha):
        try:
            z = np.load(self._file(sha), allow_pickle=False)
        except (OSError, ValueError):
            return None
        meta = json.loads(str(z["meta"]))
        if meta.get("profile_version") != PROFILE_VERSION:
            return None
        for k in z.files:
            if k != "meta":
                meta[k] = z[k]
        return meta

    def _save(self, prof):
        meta = {k: v for k, v in prof.items() if not isinstance(v, np.ndarray)}
        arrs = {k: v for k, v in prof.items() if isinstance(v, np.ndarray)}
        os.makedirs(os.path.join(CACHE, "profiles"), exist_ok=True)
        with open(self._file(prof["sha1"]), "wb") as f:
            np.savez_compressed(f, meta=np.array(json.dumps(meta)), **arrs)

    def save(self):
        self.memo.save()


def extract(full, sha):
    info = odol_read.read_odol(full)
    raw = open(full, "rb").read()
    m = re.search(rb"\x00class\x00([A-Za-z0-9_]+)\x00", raw)
    prof = {"profile_version": PROFILE_VERSION, "sha1": sha, "file": full,
            "odol_version": info["version"], "odol_class": m.group(1).decode().lower() if m else "",
            "bmin": [float(v) for v in info["bboxMin"]], "bmax": [float(v) for v in info["bboxMax"]],
            "bc": [float(v) for v in info["boundingCenter"]],
            "autocenter": int(info["autoCenter"]), "lods": [], "memory": {}}
    prof["mlod_origin"] = [-v for v in prof["bc"]]
    kinds = {}
    for lod in info["lods"]:
        r = lod.resolution
        ok = bool(lod.vertices)
        prof["lods"].append([float(r), int(len(lod.vertices) if ok else 0), int(len(lod.faces))])
        if not ok:
            continue
        if r < 1e4 and "visual" not in kinds:
            kinds["visual"] = lod
        for name, res in LOD_KINDS.items():
            if abs(r - res) < res * 1e-3 and name not in kinds:
                kinds[name] = lod
    vis = kinds.get("visual") or kinds.get("geometry")
    if vis is None:
        prof["error"] = "no readable visual or geometry LOD"
        return prof
    V = np.array(vis.vertices)
    prof["height"] = float(V[:, 1].max() - V[:, 1].min())
    prof["size"] = float(max(V[:, 0].max() - V[:, 0].min(), V[:, 2].max() - V[:, 2].min(), prof["height"]))
    top = V[V[:, 1] >= V[:, 1].max() - 0.02]
    prof["top"] = top.mean(0).astype(np.float32)
    keep = min(max(0.5, 0.3 * prof["height"]), 3.0)
    prof["contact_kinds"] = []
    for name in ("landcontact", "visual", "geometry"):
        lod = kinds.get(name)
        if lod is None:
            continue
        Vl = np.array(lod.vertices)
        if name == "landcontact":
            P = Vl.astype(np.float32)          # the author's own contact points: all of them
        else:
            P = low_points(Vl, lod.faces, keep)
        prof["low_" + name] = P
        prof["contact_kinds"].append(name)
    mem = kinds.get("memory")
    if mem is not None:
        Vm = np.array(mem.vertices)
        for name, vs in mem.selections.items():
            if vs:
                prof["memory"][name] = [float(v) for v in Vm[vs].mean(0)]
    for name, lod in (("rw", kinds.get("roadway")), ("geo", kinds.get("geometry"))):
        if lod is not None and lod.faces:
            prof[name + "_v"] = np.array(lod.vertices, np.float32)
            prof[name + "_f"] = tris(lod.faces)
    return prof


# ------------------------------------------------------------------------------------------ class index
class ClassIndex:
    """CfgVehicles class -> model p3d, from every config.cpp under P:\\DZ and japan_dev/src/JP (cached)."""
    TOKEN = re.compile(r'class\s+(\w+)\s*(?::\s*(\w+))?\s*(\{|;)|(\{)|(\})|\bmodel\s*=\s*"([^"]*)"', re.I)

    def __init__(self, roots=None):
        self.roots = roots or [os.path.join(EXTRACT_ROOT, "DZ"), os.path.join(DEV, "src", "JP")]
        self.path = os.path.join(CACHE, "class_index.json")
        self.classes = None

    def _files(self):
        out = {}
        for r in self.roots:
            for dp, _, fs in os.walk(r):
                for f in fs:
                    if f.lower() == "config.cpp":
                        p = os.path.join(dp, f)
                        out[p] = os.stat(p).st_mtime_ns
        return out

    def load(self):
        if self.classes is not None:
            return
        files = self._files()
        try:
            c = json.load(open(self.path, "rb"))
            if c.get("files") == {k: v for k, v in files.items()}:
                self.classes = c["classes"]
                return
        except (OSError, ValueError):
            pass
        classes = {}
        for p in sorted(files):
            txt = open(p, "rb").read().decode("latin-1")
            txt = re.sub(r"//[^\n]*", "", txt)
            stack = []
            for m in self.TOKEN.finditer(txt):
                name, base, term, ob, cb, model = m.groups()
                if name:
                    if term == "{":
                        if stack and stack[-1] == "cfgvehicles":
                            e = classes.setdefault(name.lower(), [None, None, name])
                            if base:
                                e[0] = base.lower()
                        stack.append(name.lower())
                elif ob:
                    stack.append(None)
                elif cb:
                    if stack:
                        stack.pop()
                elif model is not None:
                    if len(stack) >= 2 and stack[-2] == "cfgvehicles" and stack[-1]:
                        classes[stack[-1]][1] = model
        self.classes = classes
        wb(self.path, json.dumps({"files": files, "classes": classes}))

    def model(self, cls):
        self.load()
        c = cls.lower()
        for _ in range(40):
            e = self.classes.get(c)
            if not e:
                return None
            if e[1]:
                return norm_p3d(e[1]) if e[1].strip() else None
            if not e[0]:
                return None
            c = e[0]
        return None


# ------------------------------------------------------------------------------------------ categories
def load_rules(path=None):
    path = path or os.path.join(HERE, "rules.json")
    rules = json.load(open(path, "rb"))
    rules["_hash"] = {c: hashlib.sha1(json.dumps(v, sort_keys=True).encode()).hexdigest()[:16]
                      for c, v in rules["categories"].items()}
    rules["_naming_rx"] = [(c, re.compile(rx, re.I)) for c, rx in rules["naming"]]
    return rules


def categorize(rules, cls, p3d, prof):
    """(category, reason) from overrides, then class/p3d naming, then the ODOL class property, then size."""
    ov = {k.lower(): v for k, v in rules.get("overrides", {}).items() if not k.startswith("_")}
    names = [n for n in ((cls or "").lower(), "\\" + norm_p3d(p3d).lower()) if n and n != "\\"]
    for n in names:
        if n in ov or n.lstrip("\\") in ov:
            return ov.get(n, ov.get(n.lstrip("\\"))), "override"
    size = (prof or {}).get("size", 0.0)
    small = size and size < rules["size_fallback"]["prop_max_size"]
    for cat, rx in rules["_naming_rx"]:
        if any(rx.search(n) for n in names):
            if cat == "building" and small:
                return "prop", "name+size"
            return cat, "name"
    oc = (prof or {}).get("odol_class", "")
    if oc in rules.get("odol_class", {}):
        return rules["odol_class"][oc], "odol class=" + oc
    return ("prop" if small else "building"), "size"
