"""Blueprint of JP_Katana, drawn only from katana_spec.json (through tools/katana_geom.py).

    python spikes/A_arms/katana_v2/draw_spec.py

Writes katana_spec_drawing.png: side view with dimensions, edge (mune) view, kissaki detail, cross-sections,
tsuka wrap. compare.py calls main(overlay_hook=...) to draw the shipped mesh outline over it
(katana_spec_overlay.png).
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
from katana_geom import KatanaGeom, V  # noqa: E402

G = KatanaGeom()
SP = G.spec
C = SP["colours_rgb"]
COL = {
    "outside": None, "mune": (70, 80, 88), "shinogi_ji": tuple(V(C["shinogi_ji"])), "ji": tuple(V(C["ji"])),
    "hamon": tuple(V(C["hamon"])), "kissaki": tuple(int(0.5 * a + 0.5 * b) for a, b in zip(V(C["ji"]), V(C["hamon"]))),
}
ZCOL = {v: COL[k] for k, v in G.ZONES.items()}
INK = (20, 20, 30)
DIM = (170, 30, 30)
PAPER = (250, 248, 240)


def font(size):
    for f in ("arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


F_T, F_L, F_S = font(40), font(24), font(19)


class Panel:
    """maps model-plane coordinates (a = along, b = across) to pixels"""

    def __init__(self, img, box, a0, b0, scale, flip_b=True):
        self.img, self.box, self.a0, self.b0, self.k, self.flip = img, box, a0, b0, scale, flip_b
        self.d = ImageDraw.Draw(img, "RGBA")

    def P(self, a, b):
        x = self.box[0] + (a - self.a0) * self.k
        y = self.box[1] + (b - self.b0) * self.k * (1 if self.flip else -1)
        return (x, y)

    def poly(self, pts, fill=None, outline=INK, width=2):
        q = [self.P(a, b) for a, b in pts]
        if fill:
            self.d.polygon(q, fill=fill)
        if outline:
            self.d.line(q + [q[0]], fill=outline, width=width)

    def line(self, pts, fill=INK, width=2):
        self.d.line([self.P(a, b) for a, b in pts], fill=fill, width=width)

    def text(self, a, b, s, f=None, fill=INK, anchor="la"):
        self.d.text(self.P(a, b), s, font=f or F_S, fill=fill, anchor=anchor)

    def dim(self, p1, p2, label, off=0.0, horizontal=None):
        """dimension line between two model points, offset along the perpendicular (model units)"""
        (a1, b1), (a2, b2) = p1, p2
        da, db = a2 - a1, b2 - b1
        L = math.hypot(da, db) or 1
        na, nb = -db / L, da / L
        q1 = (a1 + na * off, b1 + nb * off)
        q2 = (a2 + na * off, b2 + nb * off)
        self.line([p1, q1], fill=DIM, width=1)
        self.line([p2, q2], fill=DIM, width=1)
        self.line([q1, q2], fill=DIM, width=2)
        for q, sgn in ((q1, 1), (q2, -1)):
            x, y = self.P(*q)
            ux, uy = (self.P(*q2)[0] - self.P(*q1)[0]), (self.P(*q2)[1] - self.P(*q1)[1])
            ul = math.hypot(ux, uy) or 1
            ux, uy = ux / ul * sgn, uy / ul * sgn
            self.d.polygon([(x, y), (x + 12 * ux - 5 * uy, y + 12 * uy + 5 * ux), (x + 12 * ux + 5 * uy, y + 12 * uy - 5 * ux)], fill=DIM)
        m = ((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2)
        x, y = self.P(*m)
        self.d.text((x + 6, y + 4), label, font=F_S, fill=DIM, anchor="la")


def raster_blade(panel, a_range, b_range, a_of, to_sd, step=1):
    """colour every pixel of the panel inside the blade by its zone. a_of(ya, zb) -> model (y, z)"""
    x0, y0 = panel.P(a_range[0], b_range[0])
    x1, y1 = panel.P(a_range[1], b_range[1])
    xs = np.arange(int(min(x0, x1)), int(max(x0, x1)), step)
    ys = np.arange(int(min(y0, y1)), int(max(y0, y1)), step)
    X, Y = np.meshgrid(xs, ys)
    A = panel.a0 + (X - panel.box[0]) / panel.k
    B = panel.b0 + (Y - panel.box[1]) / panel.k * (1 if panel.flip else -1)
    s, d = to_sd(A, B)
    z = G.zone_v(s.ravel(), d.ravel()).reshape(s.shape)
    arr = np.array(panel.img)
    for code, col in ZCOL.items():
        if col is None:
            continue
        m = z == code
        arr[Y[m], X[m]] = col
    panel.img.paste(Image.fromarray(arr))
    panel.d = ImageDraw.Draw(panel.img, "RGBA")


def blade_outline_side():
    """mune line out, edge line back: (y, z) polygon of the blade silhouette"""
    ss = G.body_stations(200)[:-1] + G.kissaki_stations(120)
    mune = [G.mune_point(s) for s in ss]
    edge = [G.edge_point(s) for s in ss]
    return [(p[1], p[2]) for p in mune] + [(p[1], p[2]) for p in edge[::-1]]


def side_view(img, box, scale):
    """panel A: whole sword, tsuka axis horizontal, point right, edge (+Z) down"""
    a0 = G.y_end - 0.03
    b0 = -G.tsuba_r - 0.03
    P = Panel(img, box, a0, b0, scale, flip_b=True)
    # blade zones (raster), then outlines
    tip = G.tip()
    raster_blade(P, (G.y_machi, tip[1] + 0.002), (-0.09, 0.03), None, lambda A, B: G.model_to_sd(A, B), step=1)
    P.poly(blade_outline_side(), outline=INK, width=2)
    # shinogi / ko-shinogi and yokote lines
    ss = np.linspace(0, G.L_arc, 400)
    P.line([(G.to_model(s, G.shinogi_d(s), 0)[1], G.to_model(s, G.shinogi_d(s), 0)[2]) for s in ss], fill=(40, 40, 60), width=1)
    ye = G.edge_point(G.s_yokote)
    ysh = G.to_model(G.s_yokote, G.shinogi_d(G.s_yokote), 0)
    P.line([(ye[1], ye[2]), (ysh[1], ysh[2])], fill=INK, width=2)
    # mounts
    hb = []
    for s in np.linspace(0, G.habaki_len, 12):
        p = G.mune_point(s) - G.habaki_wall * G.normal(s)
        hb.append((p[1], p[2]))
    for s in np.linspace(G.habaki_len, 0, 12):
        p = G.edge_point(s) + G.habaki_wall * G.normal(s)
        hb.append((p[1], p[2]))
    gold = tuple(V(C["gold_foil"]))
    P.poly(hb, fill=gold + (255,), outline=INK)
    sep_r = 0.5 * G.tsuka_depth * G.fuchi_flare + G.seppa_margin + 0.001
    cu = tuple(V(C["copper"]))
    for y0_, y1_ in (G.y_seppa_a, G.y_seppa_b):
        P.poly([(y0_, -sep_r), (y1_, -sep_r), (y1_, sep_r), (y0_, sep_r)], fill=cu + (255,), outline=INK, width=1)
    iron = tuple(V(C["tsuba_iron"]))
    P.poly([(G.y_tsuba[0], -G.tsuba_r), (G.y_tsuba[1], -G.tsuba_r), (G.y_tsuba[1], G.tsuba_r), (G.y_tsuba[0], G.tsuba_r)], fill=iron + (255,), outline=INK)
    shak = tuple(V(C["shakudo"]))
    fz0, fz1 = 0.5 * G.tsuka_depth * G.fuchi_flare + 0.001, 0.5 * G.tsuka_depth + 0.001
    P.poly([(G.y_fuchi[1], -fz0), (G.y_fuchi[0], -fz1), (G.y_fuchi[0], fz1), (G.y_fuchi[1], fz0)], fill=shak + (255,), outline=INK)
    ys = np.linspace(G.y_wrap[1], G.y_wrap[0], 80)
    top = [(y, -0.5 * G.tsuka_depth * G.tsuka_scale(y) + G.tsuka_offset_z(y)) for y in ys]
    bot = [(y, 0.5 * G.tsuka_depth * G.tsuka_scale(y) + G.tsuka_offset_z(y)) for y in ys[::-1]]
    P.poly(top + bot, fill=tuple(V(C["wrap_leather"])) + (255,), outline=INK)
    draw_windows(P, face_centre=0.0, show_menuki="omote")
    kz = 0.5 * G.tsuka_depth * G.kashira_scale + 0.0008
    horn = tuple(V(C["horn_lacquer"]))
    kpts = [(G.y_kashira[1], -kz), (G.y_kashira[0] + 0.004, -kz), (G.y_kashira[0], -0.6 * kz), (G.y_kashira[0], 0.6 * kz),
            (G.y_kashira[0] + 0.004, kz), (G.y_kashira[1], kz)]
    P.poly([(a, b + G.tsuka_offset_z(a)) for a, b in kpts], fill=horn + (255,), outline=INK)
    # hands (vanilla IK grip centres) for reference
    for y, lab in ((V(SP["frame"]["right_hand_y_m"]), "R hand (IK)"), (V(SP["frame"]["left_hand_y_m"]), "L hand (IK)")):
        P.line([(y, -0.030), (y, 0.030)], fill=(30, 120, 30), width=2)
        P.text(y, 0.033, lab, fill=(30, 120, 30), anchor="ma")
    # dimensions
    m0, mt = G.mune_point(0), G.tip()
    P.dim((m0[1], m0[2]), (mt[1], mt[2]), "nagasa %.1f cm (chord, munemachi - point)" % (G.nagasa * 100), off=0.036)
    sm = G.L_arc / 2
    pm = G.mune_point(sm)
    t = (mt - m0) / np.linalg.norm(mt - m0)
    foot = m0 + np.dot(pm - m0, t) * t
    P.line([(m0[1], m0[2]), (mt[1], mt[2])], fill=(120, 120, 140), width=1)
    P.line([(pm[1], pm[2]), (foot[1], foot[2])], fill=DIM, width=3)
    P.text(pm[1], pm[2] - 0.006, "sori %.1f cm, deepest at %.2f (torii-zori)" % (G.sori * 100, V(SP["blade"]["sori_peak_from_machi_frac"])), fill=DIM, anchor="mb")
    e0 = G.edge_point(0.04)
    mm0 = G.mune_point(0.04)
    P.dim((mm0[1], mm0[2]), (e0[1], e0[2]), "", off=-0.012)
    P.text(e0[1] + 0.004, e0[2] + 0.010, "motohaba %.2f" % (G.motohaba * 100), fill=DIM, anchor="la")
    ey, my = G.edge_point(G.s_yokote), G.mune_point(G.s_yokote)
    P.dim((my[1], my[2]), (ey[1], ey[2]), "sakihaba %.2f" % (G.sakihaba * 100), off=0.004)
    P.dim((G.y_end, 0.045), (G.y_tsuka_top, 0.045), "tsuka %.1f cm" % (G.tsuka_len * 100), off=0.0)
    P.dim((G.y_tsuba[0] - 0.008, -G.tsuba_r), (G.y_tsuba[0] - 0.008, G.tsuba_r), "", off=0.0)
    P.text(G.y_tsuba[0] - 0.010, G.tsuba_r + 0.004, "tsuba %.1f" % (2 * G.tsuba_r * 100), fill=DIM, anchor="ra")
    P.text(G.y_habaki[1] + 0.004, G.mune_point(0.03)[2] - 0.012, "habaki %.1f (gold foil)" % (G.habaki_len * 100), anchor="la")
    P.text(a0 + 0.005, b0 + 0.004, "A  SIDE VIEW (edge down, point right)   %d px/cm, units cm" % round(scale / 100), f=F_L)
    return P


def draw_windows(P, face_centre, show_menuki=None, along_axis=True):
    """hineri-maki windows on one face of the tsuka (side view): diamonds of black same between crossings"""
    same = tuple(V(C["same_lacquered"]))
    for i in range(G.n_windows):
        yc = G.y_wrap[1] - (i + 0.5) * G.pitch_eff
        hl = G.win_half_len * G.pitch_eff
        hh = G.win_half_h * G.tsuka_depth * G.tsuka_scale(yc)
        zc = face_centre + G.tsuka_offset_z(yc)
        P.poly([(yc - hl, zc), (yc, zc - hh), (yc + hl, zc), (yc, zc + hh)], fill=same + (255,), outline=(90, 80, 60), width=1)
    # crossings (tape twists) between the windows
    for i in range(G.n_windows + 1):
        yc = G.y_wrap[1] - i * G.pitch_eff
        zc = face_centre + G.tsuka_offset_z(yc)
        P.line([(yc - 0.002, zc - 0.004), (yc + 0.002, zc + 0.004)], fill=(120, 100, 70), width=1)
        P.line([(yc + 0.002, zc - 0.004), (yc - 0.002, zc + 0.004)], fill=(120, 100, 70), width=1)
    if show_menuki:
        y = G.y_menuki_omote if show_menuki == "omote" else G.y_menuki_ura
        zc = face_centre + G.tsuka_offset_z(y)
        P.d.ellipse([P.P(y - G.menuki_len / 2, zc - G.menuki_w / 2), P.P(y + G.menuki_len / 2, zc + G.menuki_w / 2)],
                    outline=(200, 150, 40), width=3)
    zc = face_centre + G.tsuka_offset_z(G.y_mekugi)
    r = G.mekugi_d / 2
    P.d.ellipse([P.P(G.y_mekugi - r, zc - r), P.P(G.y_mekugi + r, zc + r)], fill=(190, 160, 100), outline=INK)


def edge_view(img, box, scale):
    """panel B: looking at the mune; thickness (X) across"""
    a0 = G.y_end - 0.03
    P = Panel(img, box, a0, -0.03, scale, flip_b=True)
    ss = np.linspace(0, G.L_arc, 300)
    ys = [G.mune_point(s)[1] for s in ss]
    ks = [0.5 * G.kasane(s) for s in ss]
    ksh = [0.5 * G.shin_ratio * G.kasane(s) for s in ss]
    P.poly([(y, -k) for y, k in zip(ys, ksh)] + [(y, k) for y, k in zip(ys[::-1], ksh[::-1])], fill=tuple(V(C["ji"])) + (255,))
    P.poly([(y, -k) for y, k in zip(ys, ks)] + [(y, k) for y, k in zip(ys[::-1], ks[::-1])], fill=tuple(V(C["shinogi_ji"])) + (255,))
    P.line([(G.mune_point(G.s_yokote)[1], -0.006), (G.mune_point(G.s_yokote)[1], 0.006)], fill=DIM, width=1)
    P.text(G.mune_point(G.s_yokote)[1], -0.007, "yokote", fill=DIM, anchor="mb")
    hx = 0.5 * G.shin_ratio * G.motokasane + G.habaki_wall
    P.poly([(G.y_habaki[0], -hx), (G.y_habaki[1], -hx * 0.9), (G.y_habaki[1], hx * 0.9), (G.y_habaki[0], hx)], fill=tuple(V(C["gold_foil"])) + (255,))
    P.poly([(G.y_tsuba[0], -G.tsuba_r), (G.y_tsuba[1], -G.tsuba_r), (G.y_tsuba[1], G.tsuba_r), (G.y_tsuba[0], G.tsuba_r)], fill=tuple(V(C["tsuba_iron"])) + (255,))
    yy = np.linspace(G.y_wrap[1], G.y_wrap[0], 60)
    P.poly([(y, -0.5 * G.tsuka_width * G.tsuka_scale(y)) for y in yy] + [(y, 0.5 * G.tsuka_width * G.tsuka_scale(y)) for y in yy[::-1]],
           fill=tuple(V(C["wrap_leather"])) + (255,))
    P.poly([(G.y_fuchi[1], -0.5 * G.tsuka_width * G.fuchi_flare), (G.y_fuchi[0], -0.5 * G.tsuka_width), (G.y_fuchi[0], 0.5 * G.tsuka_width),
            (G.y_fuchi[1], 0.5 * G.tsuka_width * G.fuchi_flare)], fill=tuple(V(C["shakudo"])) + (255,))
    kw = 0.5 * G.tsuka_width * G.kashira_scale
    P.poly([(G.y_kashira[1], -kw), (G.y_kashira[0], -0.7 * kw), (G.y_kashira[0], 0.7 * kw), (G.y_kashira[1], kw)], fill=tuple(V(C["horn_lacquer"])) + (255,))
    P.dim((0.20, -0.5 * G.shin_ratio * G.motokasane), (0.20, 0.5 * G.shin_ratio * G.motokasane), "", off=0)
    P.text(0.205, 0.0, "kasane %.2f at the mune / %.2f at the shinogi (machi)  ->  %.2f / %.2f (yokote)" % (
        G.motokasane * 100, G.shin_ratio * G.motokasane * 100, G.sakikasane * 100, G.shin_ratio * G.sakikasane * 100), anchor="lm")
    P.text(a0 + 0.005, -0.028, "B  EDGE VIEW (looking at the mune, thickness true scale)", f=F_L)
    return P


def kissaki_detail(img, box, scale):
    """panel C: kissaki, enlarged; blade straightened locally (a = s, b = d)"""
    s0 = G.s_yokote - 0.03
    P = Panel(img, box, s0, -0.004, scale, flip_b=True)
    raster_blade(P, (s0, G.L_arc + 0.001), (-0.001, G.sakihaba + 0.002), None, lambda A, B: (A, B), step=1)
    ss = np.concatenate([np.linspace(s0, G.s_yokote, 40), np.array(G.kissaki_stations(200))])
    P.line([(s, 0) for s in ss], width=3)
    P.line([(s, G.width(s)) for s in ss], width=3)
    P.line([(s, G.shinogi_d(s)) for s in ss], fill=(30, 30, 50), width=2)
    P.line([(G.s_yokote, G.shinogi_d(G.s_yokote)), (G.s_yokote, G.width(G.s_yokote))], width=3)
    P.text(G.s_yokote - 0.001, G.width(G.s_yokote) + 0.0012, "yokote", anchor="ra")
    P.text(G.L_arc - 0.012, G.width(G.L_arc - 0.012) + 0.0016, "fukura (measured on Met 27600/27601)", anchor="ma")
    P.text(G.L_arc - 0.024, G.shinogi_d(G.L_arc - 0.024) - 0.0006, "ko-shinogi", anchor="rb")
    P.text(s0 + 0.003, G.shinogi_d(s0) - 0.0006, "shinogi", anchor="lb")
    P.text(G.L_arc + 0.0005, -0.0005, "point on the mune line", anchor="lb")
    P.text(G.L_arc - G.L_k * 0.5, G.width(G.L_arc - G.L_k * 0.5) - G.boshi_depth() - 0.0012, "boshi: sugu, komaru, shallow kaeri", fill=(40, 40, 40), anchor="mb")
    P.text(s0 + 0.004, G.sakihaba - 0.0045, "hamon (notare + ko-gunome, calming)", fill=(40, 40, 40), anchor="lb")
    P.dim((G.s_yokote, -0.0003), (G.L_arc, -0.0003), "kissaki %.1f cm = %.1f x sakihaba" % (G.L_k * 100, G.L_k / G.sakihaba), off=-0.0022)
    P.dim((s0 + 0.001, 0), (s0 + 0.001, G.width(s0 + 0.001)), "", off=0)
    P.text(s0 + 0.0015, G.width(s0) / 2, "%.2f" % (G.width(s0) * 100), fill=DIM, anchor="lm")
    P.text(s0, -0.0042, "C  KISSAKI DETAIL (%d px/cm; blade straightened; mune at top, edge below)" % round(scale / 100), f=F_L)
    return P


def sections(img, box, scale):
    """panel D: cross-sections (d across, x thickness)"""
    d = ImageDraw.Draw(img, "RGBA")
    x = box[0]
    for s, lab in ((0.0, "at the machi"), (G.s_yokote / 2, "mid-blade"), (G.s_yokote, "at the yokote"), (G.L_arc - 0.4 * G.L_k, "kissaki t=0.4")):
        pts, us = G.section(s)
        w = G.width(s)
        P = Panel(img, (x, box[1] + 40), -0.001, -0.006, scale, flip_b=True)
        q = [(dd, xx) for dd, xx in pts]
        P.poly(q, fill=tuple(V(C["ji"])) + (255,), outline=INK, width=2)
        ds = min(G.shinogi_d(s), 0.9 * w)
        P.line([(ds, -0.0055), (ds, 0.0055)], fill=(80, 80, 200), width=1)
        P.text(w / 2, 0.0058, "%s: width %.2f, kasane %.2f" % (lab, w * 100, G.kasane(s) * 100), anchor="ma")
        x += int((w + 0.004) * scale) + 20
    d.text((box[0], box[1]), "D  CROSS-SECTIONS (%d px/cm): mitsu-mune left, edge right, blue = shinogi" % round(scale / 100), font=F_L, fill=INK)


def tsuka_panel(img, box, scale):
    """panel E: tsuka, omote face (upper) and ura face (lower), with the IK hand centres"""
    a0 = G.y_end - 0.004
    for row, (face, menu) in enumerate((("omote (-X)", "omote"), ("ura (+X)", "ura"))):
        P = Panel(img, (box[0], box[1] + 60 + row * int(0.06 * scale)), a0, -0.025, scale, flip_b=True)
        ys = np.linspace(G.y_wrap[1], G.y_wrap[0], 80)
        top = [(y, -0.5 * G.tsuka_depth * G.tsuka_scale(y) + G.tsuka_offset_z(y)) for y in ys]
        bot = [(y, 0.5 * G.tsuka_depth * G.tsuka_scale(y) + G.tsuka_offset_z(y)) for y in ys[::-1]]
        P.poly(top + bot, fill=tuple(V(C["wrap_leather"])) + (255,), outline=INK)
        draw_windows(P, 0.0, show_menuki=menu)
        fz0, fz1 = 0.5 * G.tsuka_depth * G.fuchi_flare, 0.5 * G.tsuka_depth
        P.poly([(G.y_fuchi[1], -fz0), (G.y_fuchi[0], -fz1), (G.y_fuchi[0], fz1), (G.y_fuchi[1], fz0)], fill=tuple(V(C["shakudo"])) + (255,), outline=INK)
        kz = 0.5 * G.tsuka_depth * G.kashira_scale
        P.poly([(G.y_kashira[1], -kz), (G.y_kashira[0], -0.7 * kz), (G.y_kashira[0], 0.7 * kz), (G.y_kashira[1], kz)], fill=tuple(V(C["horn_lacquer"])) + (255,), outline=INK)
        P.poly([(G.y_tsuba[0], -G.tsuba_r * 0.55), (G.y_tsuba[1], -G.tsuba_r * 0.55), (G.y_tsuba[1], G.tsuba_r * 0.55), (G.y_tsuba[0], G.tsuba_r * 0.55)],
               fill=tuple(V(C["tsuba_iron"])) + (255,), outline=INK)
        P.text(a0 + 0.001, -0.022, "%s face: %d windows, pitch %.2f cm; menuki (gold ring) %s; mekugi %.1f cm below the machi" % (
            face, G.n_windows, G.pitch_eff * 100, menu, G.mekugi_below_machi * 100), anchor="la")
        if row == 0:
            for y, lab in ((V(SP["frame"]["right_hand_y_m"]), "R hand"), (V(SP["frame"]["left_hand_y_m"]), "L hand")):
                P.line([(y, -0.02), (y, 0.02)], fill=(30, 120, 30), width=3)
                P.text(y, 0.021, lab + " (IK)", fill=(30, 120, 30), anchor="ma")
    ImageDraw.Draw(img).text((box[0], box[1]), "E  TSUKA (%d px/cm): hineri-maki leather over black lacquered same, ryugo shape" % round(scale / 100), font=F_L, fill=INK)


def legend(img, box):
    d = ImageDraw.Draw(img)
    x, y = box
    d.text((x, y), "JP_Katana c.1600 (Keicho shinto)  -  spec drawing generated from katana_spec.json", font=F_T, fill=INK)
    y += 56
    for name in ("shinogi_ji", "ji", "hamon", "kissaki"):
        d.rectangle([x, y, x + 40, y + 24], fill=COL[name], outline=INK)
        d.text((x + 50, y), {"shinogi_ji": "shinogi-ji (burnished)", "ji": "hira-ji (jigane)", "hamon": "hamon / boshi (hardened)", "kissaki": "kissaki (narume polish)"}[name], font=F_S, fill=INK)
        x += 330
    rows = [
        ("nagasa / sori", "%.1f / %.1f cm" % (G.nagasa * 100, G.sori * 100), "tsuruginoya_F00247"),
        ("motohaba / sakihaba", "%.2f / %.2f cm" % (G.motohaba * 100, G.sakihaba * 100), "tsuruginoya_F00247"),
        ("kasane (mune) moto / saki", "%.2f / %.2f cm" % (G.motokasane * 100, G.sakikasane * 100), "tsuruginoya_F00247"),
        ("kissaki", "extended chu, %.1f cm" % (G.L_k * 100), "met27600, met27601, F00247"),
        ("tsuka / tsuba", "%.1f cm / round iron %.1f x %.1f cm" % (G.tsuka_len * 100, G.tsuba_r * 200, G.tsuba_t * 100), "F00247, met30091"),
        ("wrap", "leather hineri-maki, pitch %.2f cm, %d windows" % (G.pitch_eff * 100, G.n_windows), "TNM F-19992"),
    ]
    y += 40
    x = box[0]
    for i, (a, b, c) in enumerate(rows):
        xx = x + (i % 3) * 1060
        yy = y + (i // 3) * 30
        d.text((xx, yy), "%s: %s  [%s]" % (a, b, c), font=F_S, fill=INK)


def main(overlay_hook=None, out_name="katana_spec_drawing.png"):
    W, H = 3300, 2950
    img = Image.new("RGB", (W, H), PAPER)
    legend(img, (40, 30))
    k_side = 3000          # px per metre (1:~ scale on this sheet)
    PA = side_view(img, (60, 230), k_side)
    PB = edge_view(img, (60, 640), k_side)
    PC = kissaki_detail(img, (60, 930), 20000)
    sections(img, (1640, 900), 15000)
    tsuka_panel(img, (60, 1960), 9000)
    if overlay_hook is not None:
        overlay_hook(img, PA, PC)          # compare.py: the shipped mesh outline in red
    out = os.path.join(HERE, out_name)
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
