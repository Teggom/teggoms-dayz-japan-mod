r"""checkcache.py - skip a building's checks when nothing they depend on has changed (V1, 2026-10-01).

pipeline.py (--verify-only, the verify step of a build, verify_parallel) and buildings/verify_all.py look a building
up here first. A HIT reuses its last PASSING checks.json (rewritten from the cache if the file on disk differs) and
prints "RESULT <key>: PASS (n checks, 0 failures) [cached]"; a MISS runs build + checks as before, and a PASS is
stored. A FAIL is never stored. --full (pipeline / verify_all) ignores the cache (and stores the fresh passes).

What a stored pass depends on (all must be unchanged for a hit):
  fingerprint  - the building's registry entry (and its base entry for a furnished variant: params.base) + its budget
               - the source of every .py the checks and the model use: pipeline.py, bindcheck.py, the recipe module
                 (and the base recipe of a furnished variant), the verify module (shellcheck.py / <dir>/verify.py),
                 and transitively every module they import (AST of every import statement, also inside functions;
                 plus spec_from_file_location paths given as literals) under buildings/, parts/kit/,
                 spikes/B_building/kit/ and tools/common/. buildings/registry.py itself is NOT hashed (its entries
                 are), so adding a building does not invalidate the others.
               - the ray / z-fight engine switches (JP_RAY_ENGINE, JP_ZFIGHT_ENGINE), the Python and numpy versions
  data deps    - recorded while the building was built + checked (an audit hook on open / listdir / scandir / glob
                 and wrappers on os.path.isfile / exists / isdir): every non-Python file it read (material sidecars
                 and rvmats, prop sidecars and prop masters, the ODOL, ...) by content hash; every existence probe;
                 every directory listing and glob result. Files the window itself wrote (out/ MLOD, checks.json) are
                 outputs, not inputs. Reads during module imports (core's material library) count for every later
                 building of the process. Shared generated files count only by this building's part: its class
                 block in config.cpp, its loot group in C_mapgroupproto.xml, its bones' animation classes in
                 model.cfg (the same regexes the checks use).
               - lazy file caches (decor._CAT / _COMPS, shop_sets._AB) are emptied before each building so its reads
                 are seen; a NEW module-level cache of file data must be added to LAZY_CACHES below.
Cache files: data/C/_build/check_cache/<key>.json (data/ is git-ignored: the cache is machine-local, it holds hashes of
this machine's generated files - ODOLs, .paa materials - that are not all in git).
"""
import ast
import contextlib
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, ".."))
CACHE_DIR = os.path.join(DEV, "data", "C", "_build", "check_cache")
VERSION = 1
SEARCH = [HERE, os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "tools", "common"),
          os.path.join(DEV, "spikes", "B_building", "kit")]
NOT_HASHED = {os.path.normcase(os.path.join(HERE, "registry.py")), os.path.normcase(os.path.abspath(__file__))}
LAZY_CACHES = (("jpparts.decor", "_CAT", None), ("jpparts.decor", "_COMPS", dict), ("shop_sets", "_AB", None))
ENGINE_ENV = ("JP_RAY_ENGINE", "JP_ZFIGHT_ENGINE")
_SKIP_PREFIX = tuple({os.path.normcase(p) for p in (sys.prefix, sys.base_prefix, sys.exec_prefix)} |
                     {os.path.normcase(p) for p in sys.path if "site-packages" in p.lower()})


def _rel(p):
    p = os.path.abspath(p)
    try:
        r = os.path.relpath(p, DEV)
    except ValueError:
        return p.replace("\\", "/")
    return p.replace("\\", "/") if r.startswith("..") else r.replace("\\", "/")


def _abs(r):
    return r if os.path.isabs(r) else os.path.join(DEV, r)


# ------------------------------------------------------------------------------------------------ hashing
_HASH = {}


def file_hash(p):
    """sha1 of a file's bytes (None = missing), memoised per process on (mtime, size)."""
    try:
        st = os.stat(p)
    except OSError:
        return None
    k = os.path.normcase(os.path.abspath(p))
    m = _HASH.get(k)
    if m and m[0] == st.st_mtime_ns and m[1] == st.st_size:
        return m[2]
    _T.busy += 1
    try:
        with open(p, "rb") as f:
            h = hashlib.sha1(f.read()).hexdigest()
    except OSError:
        h = None
    finally:
        _T.busy -= 1
    _HASH[k] = (st.st_mtime_ns, st.st_size, h)
    return h


def _listing(d):
    try:
        return hashlib.sha1("\n".join(sorted(os.listdir(d))).encode("utf-8")).hexdigest()
    except OSError:
        return None


def _glob(pat, rec):
    import glob
    return hashlib.sha1("\n".join(sorted(glob.glob(pat, recursive=rec))).encode("utf-8")).hexdigest()


# shared generated files: only this building's part counts (the regexes of shellcheck / machiya verify)
def _frag(rel, args):
    p = _abs(rel)
    if not os.path.isfile(p):
        return None
    _T.busy += 1
    try:
        with open(p, "rb") as f:
            t = f.read().decode("utf-8", "replace")
    finally:
        _T.busy -= 1
    kind = args[0]
    if kind == "config":
        m = re.search(r"\tclass %s: HouseNoDestruct\n\t\{.*?\n\t\};\n" % args[1], t, re.S)
        part = m.group(0) if m else ""
    elif kind == "ce":
        m = re.search(r'<group name="%s">.*?</group>' % args[1], t, re.S)
        part = m.group(0) if m else ""
    else:                                            # model.cfg: every animation class named like one of the bones
        names = "|".join(re.escape(b[0].upper() + b[1:]) for b in args[1]) or "(?!)"
        part = "\n".join(m.group(0) for m in re.finditer(r"class (?:%s)\s*\{[^}]*\}" % names, t))
    return hashlib.sha1(part.encode("utf-8")).hexdigest()


def _frag_kind(rel, cls, bones):
    if rel == "src/JP/buildings/config.cpp":
        return ["config", cls]
    if rel == "test/ce/C_mapgroupproto.xml":
        return ["ce", cls]
    if rel.startswith("src/JP/buildings/") and rel.endswith("/model.cfg"):
        return ["mcfg", sorted(bones)]
    return None


# ------------------------------------------------------------------------------------------------ source closure
_IMPORTS = {}


def _resolve(name, level, curfile, fromnames=()):
    """Files a (possibly relative) import can load: module.py or package/__init__.py (+ package/<fromname>.py)."""
    out = []
    if level:
        base = os.path.dirname(curfile)
        for _ in range(level - 1):
            base = os.path.dirname(base)
        bases = [base]
    else:
        bases = [os.path.dirname(curfile)] + SEARCH
    parts = name.split(".") if name else []
    for b in bases:
        d = b
        hit = []
        ok = True
        for i, part in enumerate(parts):
            pkg = os.path.join(d, part)
            if os.path.isfile(os.path.join(pkg, "__init__.py")):
                hit.append(os.path.join(pkg, "__init__.py"))
                d = pkg
            elif i == len(parts) - 1 and os.path.isfile(pkg + ".py"):
                hit.append(pkg + ".py")
                d = None
            else:
                ok = False
                break
        if not ok:
            continue
        if d is not None:
            for fn in fromnames:
                if os.path.isfile(os.path.join(d, fn + ".py")):
                    hit.append(os.path.join(d, fn + ".py"))
                elif os.path.isfile(os.path.join(d, fn, "__init__.py")):
                    hit.append(os.path.join(d, fn, "__init__.py"))
        out += hit
        if hit and not level:
            break
    return out


def _literal_paths(node, curfile):
    """spec_from_file_location(..., os.path.join(X, 'a', 'b.py')): the literal segments, looked up from the
    module's folder, the dev root and buildings/."""
    segs = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
    if not segs or not segs[-1].endswith(".py"):
        return []
    rel = os.path.join(*segs)
    for b in (os.path.dirname(curfile), DEV, HERE):
        p = os.path.join(b, rel)
        if os.path.isfile(p):
            return [p]
    return []


def direct_imports(path):
    k = os.path.normcase(path)
    st = os.stat(path)
    m = _IMPORTS.get(k)
    if m and m[0] == (st.st_mtime_ns, st.st_size):
        return m[1]
    _T.busy += 1
    try:
        with open(path, "rb") as f:
            tree = ast.parse(f.read(), path)
    finally:
        _T.busy -= 1
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                out += _resolve(a.name, 0, path)
        elif isinstance(n, ast.ImportFrom):
            out += _resolve(n.module or "", n.level, path, [a.name for a in n.names])
        elif isinstance(n, ast.Call) and getattr(n.func, "attr", getattr(n.func, "id", "")) == \
                "spec_from_file_location" and len(n.args) > 1 and isinstance(n.args[1], ast.Call):
            out += _literal_paths(n.args[1], path)
    out = sorted({os.path.abspath(p) for p in out})
    _IMPORTS[k] = ((st.st_mtime_ns, st.st_size), out)
    return out


def closure(roots):
    seen, todo = {}, [os.path.abspath(r) for r in roots if os.path.isfile(r)]
    while todo:
        p = todo.pop()
        k = os.path.normcase(p)
        if k in seen:
            continue
        seen[k] = p
        if k in NOT_HASHED:
            continue
        todo += direct_imports(p)
    return [seen[k] for k in sorted(seen) if k not in NOT_HASHED]


# ------------------------------------------------------------------------------------------------ fingerprint
def _bdir(b):
    return os.path.join(HERE, b.get("dir", b["key"]))


def roots(b):
    import registry
    r = [os.path.join(HERE, "pipeline.py"), os.path.join(HERE, "bindcheck.py"),
         os.path.join(_bdir(b), b["module"] + ".py")]
    base = (b.get("params") or {}).get("base")
    if base:                                  # furnishkit imports the base shell's recipe by name (importlib)
        bb = registry.get(base)
        r.append(os.path.join(_bdir(bb), bb["module"] + ".py"))
    v = b.get("verify")
    if v == "shellcheck":
        r.append(os.path.join(HERE, "shellcheck.py"))
    elif v:
        r.append(os.path.join(_bdir(b), v + ".py"))
    return r


def fingerprint(b):
    import registry
    h = hashlib.sha1()
    import numpy
    h.update(("v%d|%s|py%d.%d|np%s|" % (VERSION, "|".join(os.environ.get(e, "") for e in ENGINE_ENV),
                                        sys.version_info[0], sys.version_info[1], numpy.__version__)).encode())
    h.update(json.dumps(b, sort_keys=True, default=repr).encode("utf-8"))
    base = (b.get("params") or {}).get("base")
    if base:
        h.update(json.dumps(registry.get(base), sort_keys=True, default=repr).encode("utf-8"))
    h.update(repr(registry.BUDGETS.get(b.get("budget"))).encode())
    srcs = closure(roots(b))
    for p in srcs:
        h.update(("\n%s %s" % (_rel(p).lower(), file_hash(p))).encode())
    return h.hexdigest(), [_rel(p) for p in srcs]


# ------------------------------------------------------------------------------------------------ tracker
class _Tracker:
    def __init__(self):
        self.installed = False
        self.busy = 0
        self.key = None
        self.win = {}
        self.ambient = {"reads": set(), "dirs": set(), "globs": set()}

    def rec(self):
        return self.win.setdefault(self.key, {"reads": set(), "writes": set(), "probes": {}, "dirs": set(),
                                              "globs": set()})


_T = _Tracker()
_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC


def _keep(p):
    pl = os.path.normcase(p)
    return not (pl.endswith((".py", ".pyc", ".pyd")) or pl.startswith(_SKIP_PREFIX) or "__pycache__" in pl)


def _by_importer():
    """The event comes straight from the import machinery (its directory scans of sys.path)."""
    return sys._getframe(2).f_code.co_filename.startswith("<frozen importlib")


def _in_import():
    f = sys._getframe(2)
    while f is not None:
        if f.f_code.co_filename.startswith("<frozen importlib"):
            return True
        f = f.f_back
    return False


def _hook(event, args):
    if _T.busy or (event != "open" and event not in ("os.listdir", "os.scandir", "glob.glob")):
        return
    try:
        if event == "open":
            p, mode, flags = args
            if not isinstance(p, str) or not _keep(p):
                return
            p = os.path.abspath(p)
            write = (any(c in mode for c in "wax+") if isinstance(mode, str) else bool((flags or 0) & _WRITE_FLAGS))
            if write:
                if _T.key is not None:
                    _T.rec()["writes"].add(p)
                return
            if _in_import():
                _T.ambient["reads"].add(p)
            elif _T.key is not None:
                r = _T.rec()
                if p not in r["writes"]:
                    r["reads"].add(p)
        elif event == "glob.glob":
            item = (args[0], bool(args[1]) if len(args) > 1 else False)
            if _in_import():
                _T.ambient["globs"].add(item)
            elif _T.key is not None:
                _T.rec()["globs"].add(item)
        else:
            d = args[0] if args and isinstance(args[0], str) else (os.getcwd() if not args or args[0] is None else
                                                                    None)
            if d is None or _by_importer() or not _keep(d + os.sep):
                return
            d = os.path.abspath(d)
            if _in_import():
                _T.ambient["dirs"].add(d)
            elif _T.key is not None:
                _T.rec()["dirs"].add(d)
    except Exception:
        pass


def _wrap_probe(fn, nm):
    def w(p):
        r = fn(p)
        if _T.key is not None and not _T.busy and isinstance(p, str) and _keep(p):
            _T.rec()["probes"][os.path.abspath(p)] = (nm, r)
        return r
    w.__name__ = getattr(fn, "__name__", nm)
    w._v1 = True
    return w


def install():
    """Start recording (pipeline.py calls this before importing the kit, so import-time reads are seen)."""
    if _T.installed:
        return
    _T.installed = True
    sys.addaudithook(_hook)
    for nm in ("isfile", "exists", "isdir"):
        f = getattr(os.path, nm)
        if not getattr(f, "_v1", False):
            setattr(os.path, nm, _wrap_probe(f, nm))


@contextlib.contextmanager
def window(key):
    """Record the reads of one building (build and checks). Re-entering the same key adds to its record."""
    for mod, attr, fresh in LAZY_CACHES:
        m = sys.modules.get(mod)
        if m is not None and hasattr(m, attr):
            setattr(m, attr, fresh() if fresh else None)
    prev = _T.key
    _T.key = key
    _T.rec()["writes"] = set()        # a file this segment writes is an output of this segment only (a staged MLOD
    try:                                # copy later replaced by its ODOL is an input of the checks segment)
        yield _T.rec()
    finally:
        _T.key = prev


_OUT_RX = re.compile(r"^buildings/.*(/out/|/(checks|records|rooms)/[^/]+\.json$|/(checks|record|rooms)\.json$)")


def _is_output(rel):
    """A building's own products (out/ MLOD + logs, checks / record / rooms json): never inputs of its checks."""
    return bool(_OUT_RX.match(rel))


def _deps(key, cls, bones):
    r = _T.win.get(key) or {"reads": set(), "writes": set(), "probes": {}, "dirs": set(), "globs": set()}
    reads = (r["reads"] | _T.ambient["reads"]) - r["writes"]
    files, frags = {}, []
    for p in sorted(reads):
        rel = _rel(p)
        if _is_output(rel):
            continue
        fk = _frag_kind(rel, cls, bones)
        if fk:
            frags.append([rel, fk, _frag(rel, fk)])
        else:
            files[rel] = file_hash(p)
    probes = {}
    for p, (nm, v) in sorted(r["probes"].items()):
        if p not in r["writes"] and not _is_output(_rel(p)):
            probes[_rel(p)] = [nm, v]
    dirs = {_rel(d): _listing(d) for d in sorted(r["dirs"] | _T.ambient["dirs"])}
    globs = [[pat, rec_, _glob(pat, rec_)] for pat, rec_ in sorted(r["globs"] | _T.ambient["globs"])]
    return {"files": files, "frags": frags, "probes": probes, "dirs": dirs, "globs": globs}


def _deps_ok(d):
    for rel, h in d["files"].items():
        if file_hash(_abs(rel)) != h:
            return "changed %s" % rel
    for rel, fk, h in d["frags"]:
        if _frag(rel, fk) != h:
            return "changed %s (%s part)" % (rel, fk[0])
    for rel, (nm, v) in d["probes"].items():
        if getattr(os.path, nm)(_abs(rel)) != v:
            return "%s %s changed" % (nm, rel)
    for rel, h in d["dirs"].items():
        if _listing(_abs(rel)) != h:
            return "listing of %s changed" % rel
    for pat, rec_, h in d["globs"]:
        if _glob(pat, rec_) != h:
            return "glob %s changed" % pat
    return None


# ------------------------------------------------------------------------------------------------ lookup / store
def _entry_path(key):
    return os.path.join(CACHE_DIR, key + ".json")


def lookup(b, checks_path, why=None):
    """The stored pass of building b if still valid (and its checks file restored), else None. why: a list that gets
    the miss reason."""
    p = _entry_path(b["key"])
    if not os.path.isfile(p):
        why is not None and why.append("no cache entry")
        return None
    try:
        with open(p, "rb") as f:
            e = json.loads(f.read().decode("utf-8"))
    except (OSError, ValueError):
        why is not None and why.append("unreadable cache entry")
        return None
    fp, _ = fingerprint(b)
    if e.get("version") != VERSION or e.get("fp") != fp:
        why is not None and why.append("sources / registry entry changed")
        return None
    bad = _deps_ok(e["deps"])
    if bad:
        why is not None and why.append(bad)
        return None
    data = e["checks"].encode("utf-8")
    cur = None
    if os.path.isfile(checks_path):
        with open(checks_path, "rb") as f:
            cur = f.read()
    if cur != data:
        os.makedirs(os.path.dirname(checks_path), exist_ok=True)
        with open(checks_path, "wb") as f:
            f.write(data)
    return e


def store(b, bd, checks_path, fp_info=None):
    """Store a PASS of building b (call only when its checks passed). bd: the build dict (class, doors)."""
    with open(checks_path, "rb") as f:
        text = f.read().decode("utf-8")
    doc = json.loads(text)
    nf = doc.get("failures")
    if nf is None:
        nf = sum(1 for r in doc.get("checks", []) if not r.get("ok"))
    if nf:
        return False
    fp, srcs = fp_info or fingerprint(b)
    bones = [a["bone"] for d in bd["M"].doors for a in d.anims]
    e = {"version": VERSION, "key": b["key"], "fp": fp, "stored": time.strftime("%Y-%m-%d %H:%M:%S"),
         "n_checks": len(doc.get("checks", [])), "checks_path": _rel(checks_path), "sources": srcs,
         "deps": _deps(b["key"], bd["rec"]["class"], bones), "checks": text}
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = _entry_path(b["key"]) + ".tmp%d" % os.getpid()
    with open(tmp, "wb") as f:
        f.write(json.dumps(e, indent=0).encode("utf-8"))
    os.replace(tmp, _entry_path(b["key"]))
    return True


def forget(key):
    _T.win.pop(key, None)
