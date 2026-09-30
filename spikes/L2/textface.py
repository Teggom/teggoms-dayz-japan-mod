#!/usr/bin/env python3
r"""textface.py - the TXT check: does every text decal face out of its host and read left to right in game?

Reads the written MLOD (Resolution 1). For every face whose texture is a text atlas (*_text*):
  - outward = minus the stored normal (MLOD stores normals inward; the writer winds the face to match)
  - FACE: a ray from the face centre along -outward meets another (non-text) face within 5 cm: the decal lies ON a
    host surface and faces away from it, so the game (single-sided faces, back faces culled) draws it
  - READ: the texture's +u runs to the viewer's RIGHT. DayZ model space is left-handed (x east, y up, z north), so
    for a viewer looking along f = -outward with up = the texture's -v direction, right = cross(up, f) in the
    plain component formula (check: up +y, f +z -> right +x = east, correct for a viewer facing north)
  python textface.py <p3d or folder> ...   prints per-file PASS/FAIL; exit 1 if any fail
"""
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts import mlod  # noqa: E402


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    L = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / L, a[1] / L, a[2] / L)


def ray_tri(o, d, a, b, c):
    e1, e2 = sub(b, a), sub(c, a)
    p = cross(d, e2)
    det = dot(e1, p)
    if abs(det) < 1e-12:
        return None
    inv = 1.0 / det
    t0 = sub(o, a)
    u = dot(t0, p) * inv
    if u < -1e-6 or u > 1 + 1e-6:
        return None
    q = cross(t0, e1)
    v = dot(d, q) * inv
    if v < -1e-6 or u + v > 1 + 1e-6:
        return None
    t = dot(e2, q) * inv
    return t if t > 0 else None


def check_lod(lod):
    tris = []
    for fv, fl, tex, mat in lod.faces:
        if "decal_" in tex and "_text" in tex:
            continue
        P = [lod.points[v[0]] for v in fv]
        tris.append((P[0], P[1], P[2]))
        if len(P) == 4:
            tris.append((P[0], P[2], P[3]))
    out = []
    for fi, (fv, fl, tex, mat) in enumerate(lod.faces):
        if not ("decal_" in tex and "_text" in tex):
            continue
        P = [lod.points[v[0]] for v in fv]
        UV = [(v[2], v[3]) for v in fv]
        n_in = lod.normals[fv[0][1]]
        outw = norm((-n_in[0], -n_in[1], -n_in[2]))
        e1, e2 = sub(P[1], P[0]), sub(P[2], P[0])
        du1, dv1 = UV[1][0] - UV[0][0], UV[1][1] - UV[0][1]
        du2, dv2 = UV[2][0] - UV[0][0], UV[2][1] - UV[0][1]
        det = du1 * dv2 - du2 * dv1
        if abs(det) < 1e-12:
            continue
        T = tuple((dv2 * e1[k] - dv1 * e2[k]) / det for k in range(3))      # d position / d u
        Bv = tuple((-du2 * e1[k] + du1 * e2[k]) / det for k in range(3))   # d position / d v (v runs down)
        up = norm((-Bv[0], -Bv[1], -Bv[2]))
        right = cross(up, (-outw[0], -outw[1], -outw[2]))
        reads = dot(norm(T), right) > 0.3
        c = tuple(sum(p[k] for p in P) / len(P) for k in range(3))
        o = (c[0] - outw[0] * 0.0001, c[1] - outw[1] * 0.0001, c[2] - outw[2] * 0.0001)
        back = (-outw[0], -outw[1], -outw[2])
        hits = [t for a, b, cc in tris for t in [ray_tri(o, back, a, b, cc)] if t is not None and t < 0.05]
        out.append({"face": fi, "tex": os.path.basename(tex), "reads": reads, "host_behind": bool(hits),
                    "centre": [round(x, 3) for x in c]})
    return out


def check_file(p):
    lods = mlod.read_mlod(p)
    r1 = next(l for l in lods if abs(l.resolution - 1.0) < 1e-3)
    return check_lod(r1)


def main(args):
    files = []
    for a in args:
        files += sorted(glob.glob(os.path.join(a, "**", "*.p3d"), recursive=True)) if os.path.isdir(a) else [a]
    bad = 0
    n_text = 0
    for p in files:
        res = check_file(p)
        if not res:
            continue
        n_text += 1
        fr = [r for r in res if not r["reads"]]
        fh = [r for r in res if not r["host_behind"]]
        ok = not fr and not fh
        bad += 0 if ok else 1
        print("%-4s %-52s text faces %3d  read-wrong %3d  no-host-behind %3d" % (
            "PASS" if ok else "FAIL", os.path.relpath(p, DEV), len(res), len(fr), len(fh)))
    print("files with text: %d, failing: %d" % (n_text, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
