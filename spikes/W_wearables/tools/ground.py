"""Ground (_g) models: what lies in the world and in the inventory preview. Unweighted, no skeleton.

  kasa     the worn hat itself, resting on its rim
  kimono   folded the traditional way: a flat rectangular bundle, the back with the crest on top, collar and obi
           visible (vanilla tops use a crumpled heap; a folded kimono is the period-correct look and costs
           ~40 faces)
  tabi     both feet (tabi + waraji) from the male mesh, side by side
"""
import numpy as np

from garment import Garment
import kimono as KM


def kasa_g(worn):
    g = worn.copy("kasa_g")
    P = g.arrays()
    rim = P[:, 1].min()
    c = np.array([0.0, rim, np.mean(P[:, 2])])
    g.P = [p - c for p in P]
    g.W = [{} for _ in g.P]
    return g


def kimono_g(length="short"):
    """a folded kimono: 0.42 x 0.30 m, 5 cm thick (long: 7 cm), slightly rounded edges"""
    g = Garment("kimono_g_" + length)
    W_, D_ = 0.30, 0.42
    H = 0.05 if length == "short" else 0.07
    # top face: back panel with the crest (trunk region around u = 0.5)
    def trunk_uv(s, t):
        u0, v0, u1, v1 = KM.A_TRUNK
        u = 0.37 + 0.26 * s
        v = 0.01 + (0.28 if length == "short" else 0.17) * t   # keeps the crest mid-bundle on both textures
        return (u0 + (u1 - u0) * u, v0 + (v1 - v0) * v)

    def region(r, s, t):
        u0, v0, u1, v1 = r
        return (u0 + (u1 - u0) * s, v0 + (v1 - v0) * t)
    x0, x1, z0, z1 = -W_ / 2, W_ / 2, -D_ / 2, D_ / 2
    y1 = H
    b = 0.012  # bevel
    top = g.add_points(np.array([[x0 + b, y1, z0 + b], [x1 - b, y1, z0 + b], [x1 - b, y1, z1 - b], [x0 + b, y1, z1 - b]]))
    mid = g.add_points(np.array([[x0, y1 - b, z0], [x1, y1 - b, z0], [x1, y1 - b, z1], [x0, y1 - b, z1]]))
    bot = g.add_points(np.array([[x0, 0.0, z0], [x1, 0.0, z0], [x1, 0.0, z1], [x0, 0.0, z1]]))
    # top (seen from above: x to the right, z toward the viewer's top... orient() fixes winding afterwards)
    g.add_face([top + 0, top + 1, top + 2, top + 3], [trunk_uv(0, 1), trunk_uv(1, 1), trunk_uv(1, 0), trunk_uv(0, 0)], "trunk")
    f_top = len(g.F)
    for k in range(4):
        k1 = (k + 1) % 4
        g.add_face([top + k, mid + k, mid + k1, top + k1], [trunk_uv(0.5, 0.5)] * 4, "trunk")
        g.add_face([mid + k, bot + k, bot + k1, mid + k1],
                   [region(KM.A_TRUNK, 0.1, 0.9), region(KM.A_TRUNK, 0.1, 1.0), region(KM.A_TRUNK, 0.3, 1.0), region(KM.A_TRUNK, 0.3, 0.9)], "trunk")
    g.add_face([bot + 3, bot + 2, bot + 1, bot + 0], [trunk_uv(0.5, 0.5)] * 4, "trunk")
    # the collar crossing the top as a raised band near one short end, and the obi folded on top
    def strip(zc, width, lift, reg_, mat):
        p = g.add_points(np.array([[x0 + 0.01, y1 + lift, zc - width / 2], [x1 - 0.01, y1 + lift, zc - width / 2],
                                   [x1 - 0.01, y1 + lift, zc + width / 2], [x0 + 0.01, y1 + lift, zc + width / 2]]))
        g.add_face([p, p + 1, p + 2, p + 3], [region(reg_, 0, 0.2), region(reg_, 1, 0.2), region(reg_, 1, 0.9), region(reg_, 0, 0.9)], mat)
    strip(z0 + 0.05, 0.045, 0.004, KM.A_COLLAR, "collar")
    strip(z1 - 0.09, 0.10, 0.012, KM.A_OBI, "obi")
    c = np.array([0.0, H / 2, 0.0])
    g.orient(range(len(g.F)), lambda q: q - c if abs(q[1] - (y1 + 0.004)) > 0.001 and abs(q[1] - (y1 + 0.012)) > 0.001 else np.array([0, 1.0, 0]))
    g.W = [{} for _ in g.P]
    return g


def tabi_g(worn_m):
    g = worn_m.copy("tabi_g")
    P = g.arrays()
    # bring the feet 12 cm apart (they stand 33 cm apart in the bind pose) and centre
    P[:, 0] = np.where(P[:, 0] > 0, P[:, 0] - 0.105, P[:, 0] + 0.105)
    P[:, 1] -= P[:, 1].min()
    P[:, 2] -= P[:, 2].mean()
    g.P = [p for p in P]
    g.W = [{} for _ in g.P]
    return g
