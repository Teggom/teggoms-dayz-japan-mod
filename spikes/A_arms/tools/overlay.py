"""Tiny orthographic mesh renderer (Pillow + numpy only) for grip-frame overlays.

Draw several meshes in ONE model frame (p3d axes: X right, Y up, Z forward) from three views, flat-shaded
with a painter's sort, plus points/segments (memory points, hand bones) and labels.

  layers = [ {"verts": [...], "faces": [...], "color": (r,g,b), "alpha": 0.5, "label": "..."},
             {"points": [(xyz, "name")], "color": ...},
             {"segments": [(a, b)], "color": ..., "width": 2} ]
  render(layers, "out.png", views=("front", "side", "top"), title="...")
"""
import math

import numpy as np
from PIL import Image, ImageDraw

VIEWS = {
    # name: (u axis vector, v axis vector, depth axis vector (towards viewer), caption)
    "side": ((0, 0, 1), (0, 1, 0), (-1, 0, 0), "side: +Z right, +Y up (looking along +X)"),
    "front": ((1, 0, 0), (0, 1, 0), (0, 0, 1), "front: +X right, +Y up (looking along -Z)"),
    "top": ((1, 0, 0), (0, 0, 1), (0, 1, 0), "top: +X right, +Z up (looking down -Y)"),
}


def _proj(p, view):
    u, v, w, _ = VIEWS[view]
    return (p[0] * u[0] + p[1] * u[1] + p[2] * u[2],
            p[0] * v[0] + p[1] * v[1] + p[2] * v[2],
            p[0] * w[0] + p[1] * w[1] + p[2] * w[2])


def render(layers, path, views=("side", "front", "top"), title="", size=560, pad=0.08, bounds=None):
    # common bounds over all layers
    pts = []
    for L in layers:
        pts += [tuple(p) for p in L.get("verts", [])]
        pts += [tuple(p[0]) for p in L.get("points", [])]
        for a, b in L.get("segments", []):
            pts += [tuple(a), tuple(b)]
    P = np.array(pts)
    lo, hi = P.min(0), P.max(0)
    if bounds:
        lo, hi = np.array(bounds[0]), np.array(bounds[1])
    panels = []
    for view in views:
        img = Image.new("RGB", (size, size), (248, 248, 244))
        d = ImageDraw.Draw(img, "RGBA")
        corners = [_proj((x, y, z), view) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
        us = [c[0] for c in corners]
        vs = [c[1] for c in corners]
        span = max(max(us) - min(us), max(vs) - min(vs)) * (1 + 2 * pad) or 1.0
        cu, cv = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
        scale = size / span

        def S(p):
            q = _proj(p, view)
            return (size / 2 + (q[0] - cu) * scale, size / 2 - (q[1] - cv) * scale)
        # grid: 10 cm
        step = 0.1
        g0u = math.floor((cu - span / 2) / step) * step
        g0v = math.floor((cv - span / 2) / step) * step
        k = 0
        while g0u + k * step < cu + span / 2:
            x = size / 2 + (g0u + k * step - cu) * scale
            col = (215, 215, 210) if abs(g0u + k * step) > 1e-6 else (170, 170, 200)
            d.line([(x, 0), (x, size)], fill=col, width=1)
            k += 1
        k = 0
        while g0v + k * step < cv + span / 2:
            y = size / 2 - (g0v + k * step - cv) * scale
            col = (215, 215, 210) if abs(g0v + k * step) > 1e-6 else (170, 170, 200)
            d.line([(0, y), (size, y)], fill=col, width=1)
            k += 1
        # faces from all mesh layers, painter's order
        polys = []
        light = np.array([0.3, 0.8, 0.5])
        light /= np.linalg.norm(light)
        for L in layers:
            if "faces" not in L:
                continue
            V = [tuple(p) for p in L["verts"]]
            col = L.get("color", (120, 120, 120))
            a = int(255 * L.get("alpha", 1.0))
            for f in L["faces"]:
                ps = [V[i] for i in f]
                n = np.cross(np.subtract(ps[1], ps[0]), np.subtract(ps[2], ps[0]))
                nn = np.linalg.norm(n)
                sh = 0.55 + 0.45 * abs(float(np.dot(n / nn, light))) if nn > 0 else 0.7
                depth = sum(_proj(p, view)[2] for p in ps) / len(ps)
                polys.append((depth, [S(p) for p in ps], tuple(int(c * sh) for c in col) + (a,),
                              L.get("outline")))
        polys.sort(key=lambda t: t[0])
        for _, poly, fill, outline in polys:
            d.polygon(poly, fill=fill, outline=outline)
        for L in layers:
            col = L.get("color", (0, 0, 0))
            for a, b in L.get("segments", []):
                d.line([S(a), S(b)], fill=col + (255,), width=L.get("width", 2))
            for p, name in L.get("points", []):
                x, y = S(p)
                r = L.get("radius", 4)
                d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255,))
                if name:
                    d.text((x + 6, y - 6), name, fill=col + (255,))
        d.text((8, 8), VIEWS[view][3], fill=(40, 40, 40))
        d.text((8, size - 16), "grid 10 cm, blue lines = axes through origin", fill=(90, 90, 90))
        panels.append(img)
    W = size * len(panels)
    out = Image.new("RGB", (W, size + 40), (255, 255, 255))
    for i, p in enumerate(panels):
        out.paste(p, (i * size, 40))
    d = ImageDraw.Draw(out)
    d.text((10, 8), title, fill=(0, 0, 0))
    # legend
    x = 10
    for L in layers:
        if L.get("label"):
            d.rectangle([x, 24, x + 10, 34], fill=L.get("color", (0, 0, 0)))
            d.text((x + 14, 22), L["label"], fill=(0, 0, 0))
            x += 20 + 7 * len(L["label"])
    out.save(path)
    return path
