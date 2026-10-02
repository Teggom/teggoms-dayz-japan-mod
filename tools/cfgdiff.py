#!/usr/bin/env python3
r"""cfgdiff.py - compare the CLASSES of two DayZ configs (config.cpp / model.cfg), ignoring comments, whitespace and
the order of properties and classes. Agent CA1, 2026-10-01.

  python tools/cfgdiff.py A B [--quiet]

A and B are each a config.cpp / model.cfg file, or a .pbo (every *config.cpp inside it is read, keyed by its path in
the PBO). Prints the class count of both sides and every difference: a class only in A, only in B, or in both with a
different base or a different set of property statements (whitespace outside strings removed). Forward declarations
('class HouseNoDestruct;') are compared too. Exit 0 = no differences, 1 = differences.

Library use: parse(text) -> {"classes": {path: {"base", "props"}}, "decls": set(paths)}; diff(pa, pb) -> [lines];
pbo_configs(pbo_path) -> {path_in_pbo: text}.
"""
import os
import struct
import sys


def strip_comments(t):
    """Remove // and /* */ comments outside double-quoted strings (config strings double a quote to escape it)."""
    out = []
    i, n = 0, len(t)
    while i < n:
        c = t[i]
        if c == '"':
            j = i + 1
            while j < n:
                if t[j] == '"':
                    if j + 1 < n and t[j + 1] == '"':
                        j += 2
                        continue
                    break
                j += 1
            out.append(t[i:j + 1])
            i = j + 1
        elif t.startswith("//", i):
            j = t.find("\n", i)
            i = n if j < 0 else j
        elif t.startswith("/*", i):
            j = t.find("*/", i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _norm(stmt):
    """Whitespace removed outside strings."""
    out, i, n = [], 0, len(stmt)
    while i < n:
        c = stmt[i]
        if c == '"':
            j = i + 1
            while j < n:
                if stmt[j] == '"':
                    if j + 1 < n and stmt[j + 1] == '"':
                        j += 2
                        continue
                    break
                j += 1
            out.append(stmt[i:j + 1])
            i = j + 1
        elif c.isspace():
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


class _P:
    def __init__(self, t):
        self.t, self.i, self.n = t, 0, len(t)

    def ws(self):
        while self.i < self.n and self.t[self.i].isspace():
            self.i += 1

    def word(self):
        self.ws()
        j = self.i
        while j < self.n and (self.t[j].isalnum() or self.t[j] in "_"):
            j += 1
        w = self.t[self.i:j]
        self.i = j
        return w

    def statement(self):
        """Up to the ';' at brace depth 0 (array values hold braces), strings respected."""
        j, depth = self.i, 0
        while j < self.n:
            c = self.t[j]
            if c == '"':
                j += 1
                while j < self.n:
                    if self.t[j] == '"':
                        if j + 1 < self.n and self.t[j + 1] == '"':
                            j += 2
                            continue
                        break
                    j += 1
            elif c == "{":
                depth += 1
            elif c == "}":
                if depth == 0:
                    break
                depth -= 1
            elif c == ";" and depth == 0:
                s = self.t[self.i:j]
                self.i = j + 1
                return s
            j += 1
        s = self.t[self.i:j]
        self.i = j
        return s


def _block(p, path, res):
    """Parse entries until the closing '}' (or EOF) of the current block; fills res."""
    props = []
    while True:
        p.ws()
        if p.i >= p.n:
            return props
        c = p.t[p.i]
        if c == "}":
            p.i += 1
            p.ws()
            if p.i < p.n and p.t[p.i] == ";":
                p.i += 1
            return props
        if c == "#":                                    # preprocessor line
            j = p.t.find("\n", p.i)
            j = p.n if j < 0 else j
            props.append(_norm(p.t[p.i:j]))
            p.i = j
            continue
        if c == ";":
            p.i += 1
            continue
        save = p.i
        w = p.word()
        if w == "class":
            name = p.word()
            p.ws()
            base = None
            if p.i < p.n and p.t[p.i] == ":":
                p.i += 1
                base = p.word()
                p.ws()
            full = (path + "/" + name) if path else name
            if p.i < p.n and p.t[p.i] == ";":
                p.i += 1
                res["decls"].add(full)
                continue
            if p.i < p.n and p.t[p.i] == "{":
                p.i += 1
                key = full
                k = 2
                while key in res["classes"]:            # a class declared twice at one level: keep both
                    key = "%s#%d" % (full, k)
                    k += 1
                res["classes"][key] = {"base": base, "props": None}
                sub = _block(p, full, res)
                res["classes"][key]["props"] = sorted(sub)
                continue
            raise ValueError("config parse error near %r" % p.t[save:save + 80])
        p.i = save
        st = p.statement()
        if st.strip():
            props.append(_norm(st))


def parse(text):
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    res = {"classes": {}, "decls": set()}
    top = _block(_P(strip_comments(text)), "", res)
    if top:
        res["classes"]["<top>"] = {"base": None, "props": sorted(top)}
    return res


def diff(a, b, la="A", lb="B"):
    out = []
    ca, cb = a["classes"], b["classes"]
    for k in sorted(set(ca) - set(cb)):
        out.append("only in %s: class %s" % (la, k))
    for k in sorted(set(cb) - set(ca)):
        out.append("only in %s: class %s" % (lb, k))
    for k in sorted(set(ca) & set(cb)):
        x, y = ca[k], cb[k]
        if x["base"] != y["base"]:
            out.append("class %s: base %s (%s) vs %s (%s)" % (k, x["base"], la, y["base"], lb))
        if x["props"] != y["props"]:
            px, py = set(x["props"]), set(y["props"])
            out.append("class %s: body differs: only %s %s; only %s %s" % (
                k, la, sorted(px - py)[:4], lb, sorted(py - px)[:4]))
    for k in sorted(a["decls"] - b["decls"]):
        out.append("only in %s: declaration class %s;" % (la, k))
    for k in sorted(b["decls"] - a["decls"]):
        out.append("only in %s: declaration class %s;" % (lb, k))
    return out


def _cstr(f):
    out = bytearray()
    while True:
        c = f.read(1)
        if not c or c == b"\x00":
            return out.decode("latin-1")
        out += c


def pbo_list(path):
    """[(name, size)] of a PBO's entries (header only)."""
    out = []
    with open(path, "rb") as f:
        while True:
            name = _cstr(f)
            method, orig, reserved, ts, size = struct.unpack("<5I", f.read(20))
            if name == "" and method == 0x56657273:
                while _cstr(f):
                    _cstr(f)
                continue
            if name == "":
                return out
            out.append((name, size))


def pbo_entries(path, want=lambda name: True):
    """{name: bytes} for the entries of an uncompressed PBO (tools/common/pbo.py layout) that want(name)."""
    res = {}
    with open(path, "rb") as f:
        entries = []
        while True:
            name = _cstr(f)
            method, orig, reserved, ts, size = struct.unpack("<5I", f.read(20))
            if name == "" and method == 0x56657273:
                while _cstr(f):
                    _cstr(f)
                continue
            if name == "":
                break
            entries.append((name, method, size))
        off = f.tell()
        for name, method, size in entries:
            if want(name):
                f.seek(off)
                res[name] = f.read(size)
            off += size
    return res


def pbo_configs(path):
    return {k: v for k, v in pbo_entries(path, lambda n: n.lower().replace("/", "\\").endswith("config.cpp")).items()}


def load(path):
    """A file -> parse; a .pbo -> one merged parse with the classes keyed '<config path in pbo>:<class path>'."""
    if path.lower().endswith(".pbo"):
        res = {"classes": {}, "decls": set()}
        for name, data in sorted(pbo_configs(path).items()):
            p = parse(data)
            pre = "" if name.lower() == "config.cpp" else name.replace("/", "\\") + ":"   # the root config: bare keys
            res["classes"].update({pre + k: v for k, v in p["classes"].items()})
            res["decls"].update(pre + k for k in p["decls"])
        return res
    return parse(open(path, "rb").read())


def count(res, top="CfgVehicles"):
    """Classes directly under <top> (any config path in a PBO)."""
    return sum(1 for k in res["classes"] if k.split(":")[-1].count("/") == 1 and k.split(":")[-1].startswith(top + "/"))


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    a, b = load(args[0]), load(args[1])
    d = diff(a, b, "A", "B")
    print("A: %d classes (%d CfgVehicles, %d declarations)  %s" % (len(a["classes"]), count(a), len(a["decls"]), args[0]))
    print("B: %d classes (%d CfgVehicles, %d declarations)  %s" % (len(b["classes"]), count(b), len(b["decls"]), args[1]))
    if "--quiet" not in argv:
        for line in d[:200]:
            print("  " + line)
    print("differences: %d" % len(d))
    return 1 if d else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
