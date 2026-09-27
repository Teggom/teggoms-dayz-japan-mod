"""JP_Katana geometry, derived ONLY from spikes/A_arms/katana_v2/katana_spec.json.

Used by models.build_katana (mesh), katana_textures (UV-space features) and katana_v2/draw_spec.py (blueprint),
so the drawing, the mesh and the textures all come from the same numbers. No katana dimension is set anywhere else.

Frame (p3d numbers, metres): tsuka axis = +Y through x = z = 0, point towards +Y, edge towards +Z (see spec.frame).
Blade coordinates: s = arc length along the mune from the munemachi (0) to the point (L_arc);
d = distance from the mune towards the edge, measured square to the mune; x = half-thickness (+-X).
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_PATH = os.path.join(os.path.dirname(HERE), "katana_v2", "katana_spec.json")


# texture layout (not a dimension): katana fittings atlas rectangles (u0, u1, v0, v1), shared by models + katana_textures
ATLAS = {
    "iron": (0.01, 0.49, 0.01, 0.49), "shakudo": (0.51, 0.99, 0.01, 0.49),
    "horn_side": (0.01, 0.49, 0.51, 0.71), "horn_cap": (0.01, 0.24, 0.75, 0.98),
    "gold": (0.51, 0.74, 0.51, 0.99), "copper": (0.76, 0.99, 0.51, 0.99),
}


def V(node):
    """value of a spec entry ({'value': ...} or a bare value)"""
    return node["value"] if isinstance(node, dict) and "value" in node else node


def load_spec(path=SPEC_PATH):
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


class KatanaGeom:
    def __init__(self, spec=None):
        sp = spec or load_spec()
        self.spec = sp
        b, k, m, fr = sp["blade"], sp["kissaki"], sp["mounts"], sp["frame"]
        cm = 0.01
        # ---------------------------------------------------------------- blade
        self.nagasa = V(b["nagasa_cm"]) * cm
        self.sori = V(b["sori_cm"]) * cm
        self.motohaba = V(b["motohaba_cm"]) * cm
        self.sakihaba = V(b["sakihaba_cm"]) * cm
        self.motokasane = V(b["motokasane_cm"]) * cm
        self.sakikasane = V(b["sakikasane_cm"]) * cm
        self.shin_ratio = V(b["shinogi_thickness_over_kasane"])
        self.shin_d = V(b["shinogi_from_mune_over_width"])
        self.mune_top = V(b["mune_top_over_kasane"])
        self.mune_bevel = V(b["mune_bevel_depth_over_kasane"])
        self.niku = V(b["niku"])
        self.L_k = V(k["length_over_sakihaba"]) * self.sakihaba
        self.k_tip = V(k["thickness_tip_frac"])
        self.k_exp = V(k["thickness_exp"])
        fk = np.array(V(k["fukura_profile_t_w"]), np.float64)
        self.fuk_t, self.fuk_w = fk[:, 0], fk[:, 1]
        ks = np.array(V(k["ko_shinogi_profile_t_d"]), np.float64)
        self.kos_t, self.kos_d = ks[:, 0], ks[:, 1]
        # mune line = circular arc through the munemachi and the point, chord = nagasa, sagitta = sori (torii-zori),
        # tangent to the tsuka axis (+Y) at the machi
        c, s_ = self.nagasa, self.sori
        self.R = (c * c / 4 + s_ * s_) / (2 * s_)
        self.alpha = math.asin(c / (2 * self.R))
        self.L_arc = 2 * self.alpha * self.R
        self.s_yokote = self.L_arc - self.L_k
        self.y_machi = V(fr["guard_base_y_m"])
        self.z_mune0 = -self.motohaba / 2          # blade centred on the tsuka axis at the machi
        # ---------------------------------------------------------------- mounts (y positions along the tsuka axis)
        hb, se, ts, fu, ka, tk = m["habaki"], m["seppa"], m["tsuba"], m["fuchi"], m["kashira"], m["tsuka"]
        self.habaki_len = V(hb["length_cm"]) * cm
        self.habaki_wall = V(hb["wall_cm"]) * cm
        self.seppa_t = V(se["thickness_cm"]) * cm
        self.seppa_margin = V(se["margin_cm"]) * cm
        self.tsuba_r = V(ts["diameter_cm"]) * cm / 2
        self.tsuba_t = V(ts["thickness_cm"]) * cm
        self.tsuba_round = V(ts["rim_round_cm"]) * cm
        self.fuchi_h = V(fu["height_cm"]) * cm
        self.fuchi_flare = V(fu["flare"])
        self.kashira_len = V(ka["length_cm"]) * cm
        self.tsuka_len = V(tk["length_cm"]) * cm
        self.tsuka_depth = V(tk["height_cm"]) * cm      # edge-mune (Z)
        self.tsuka_width = V(tk["width_cm"]) * cm       # side-side (X)
        self.waist = V(tk["waist_scale"])
        self.waist_at = V(tk["waist_from_fuchi_frac"])
        self.kashira_scale = V(tk["kashira_end_scale"])
        self.tsuka_sori = V(tk["tsuka_sori_cm"]) * cm
        wr = m["wrap"]
        self.wrap_pitch = V(wr["pitch_cm"]) * cm
        self.win_half_len = V(wr["window_half_length_over_pitch"])
        self.win_half_h = V(wr["window_half_height_over_depth"])
        mn = m["menuki"]
        self.menuki_len = V(mn["length_cm"]) * cm
        self.menuki_w = V(mn["width_cm"]) * cm
        mk = m["mekugi"]
        self.mekugi_below_machi = V(mk["below_machi_cm"]) * cm
        self.mekugi_d = V(mk["diameter_cm"]) * cm
        # stack along -Y from the machi: seppa, tsuba, seppa, fuchi, wrap, kashira
        self.y_seppa_a = (self.y_machi - self.seppa_t, self.y_machi)                       # blade-side seppa
        self.y_tsuba = (self.y_seppa_a[0] - self.tsuba_t, self.y_seppa_a[0])
        self.y_seppa_b = (self.y_tsuba[0] - self.seppa_t, self.y_tsuba[0])
        self.y_tsuka_top = self.y_seppa_b[0]                                                # fuchi face
        self.y_fuchi = (self.y_tsuka_top - self.fuchi_h, self.y_tsuka_top)
        self.y_end = self.y_tsuka_top - self.tsuka_len                                      # end of the kashira
        self.y_kashira = (self.y_end, self.y_end + self.kashira_len)
        self.y_wrap = (self.y_kashira[1], self.y_fuchi[0])
        self.y_habaki = (self.y_machi, self.y_machi + self.habaki_len)
        self.y_mekugi = self.y_machi - self.mekugi_below_machi
        # wrap windows: centred between crossings, counted from the fuchi end of the wrap
        wl = self.y_wrap[1] - self.y_wrap[0]
        self.n_windows = int(round(wl / self.wrap_pitch))
        self.pitch_eff = wl / self.n_windows
        mw = V(mn["window_from_end"])
        self.y_menuki_omote = self.y_wrap[1] - (mw - 0.5) * self.pitch_eff
        self.y_menuki_ura = self.y_wrap[0] + (mw - 0.5) * self.pitch_eff
        self.omote_sign = -1.0 if V(fr["omote_face"]) == "-X" else 1.0

    # ------------------------------------------------------------------ blade line
    def theta(self, s):
        return s / self.R

    def mune_point(self, s):
        th = self.theta(s)
        return np.array([0.0, self.y_machi + self.R * math.sin(th), self.z_mune0 - self.R * (1 - math.cos(th))])

    def normal(self, s):
        """unit vector square to the mune, towards the edge (in the YZ plane)"""
        th = self.theta(s)
        return np.array([0.0, math.sin(th), math.cos(th)])

    def tangent(self, s):
        th = self.theta(s)
        return np.array([0.0, math.cos(th), -math.sin(th)])

    def t_kissaki(self, s):
        """0 at the point, 1 at the yokote (only meaningful for s >= s_yokote)"""
        return max(0.0, min(1.0, (self.L_arc - s) / self.L_k))

    def width(self, s):
        if s <= self.s_yokote:
            f = s / self.s_yokote
            return self.motohaba + (self.sakihaba - self.motohaba) * f
        return self.sakihaba * float(np.interp(self.t_kissaki(s), self.fuk_t, self.fuk_w))

    def kasane(self, s):
        if s <= self.s_yokote:
            f = s / self.s_yokote
            return self.motokasane + (self.sakikasane - self.motokasane) * f
        t = self.t_kissaki(s)
        return self.sakikasane * (self.k_tip + (1 - self.k_tip) * t ** self.k_exp)

    def shinogi_d(self, s):
        """distance of the shinogi (body) or ko-shinogi (kissaki) from the mune"""
        if s <= self.s_yokote:
            return self.shin_d * self.width(s)
        t = self.t_kissaki(s)
        return self.shin_d * self.sakihaba * float(np.interp(t, self.kos_t, self.kos_d))

    def section(self, s):
        """cross-section points (d, x) going round: mune top +, mune bevel +, shinogi +, hira +, hira +, EDGE,
        hira -, hira -, shinogi -, mune bevel -, mune top -   (11 points) and the texture u (= d / width) of each"""
        w = self.width(s)
        k = self.kasane(s)
        if w < 1e-6:
            return [(0.0, 0.0)] * 11, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ks = self.shin_ratio * k
        ds = min(self.shinogi_d(s), 0.9 * w)
        mb = min(self.mune_bevel * k, 0.8 * ds) if ds > 0 else 0.0
        mt = 0.5 * self.mune_top * k

        def h(u):   # hira-ji half-thickness: straight from the shinogi to the edge plus a low niku bulge
            return 0.5 * ks * ((1 - u) + self.niku * 4 * u * (1 - u))
        d4, d5 = ds + 0.45 * (w - ds), ds + 0.80 * (w - ds)
        half = [(0.0, mt), (mb, 0.5 * k), (ds, 0.5 * ks), (d4, h(0.45)), (d5, h(0.80))]
        pts = half + [(w, 0.0)] + [(d, -x) for d, x in half[::-1]]
        us = [d / w for d, _ in pts]
        return pts, us

    def to_model(self, s, d, x):
        return self.mune_point(s) + d * self.normal(s) + np.array([x, 0.0, 0.0])

    def edge_point(self, s):
        return self.to_model(s, self.width(s), 0.0)

    def tip(self):
        return self.mune_point(self.L_arc)

    def body_stations(self, n):
        return [self.s_yokote * i / n for i in range(n + 1)]

    def kissaki_stations(self, n):
        """from the yokote (t = 1) to the point (t = 0), packed towards the point"""
        return [self.L_arc - self.L_k * (1 - i / n) ** 1.6 for i in range(n + 1)]

    # ------------------------------------------------------------------ vectorised blade zones (texture + drawing)
    ZONES = {"outside": 0, "mune": 1, "shinogi_ji": 2, "ji": 3, "hamon": 4, "kissaki": 5}

    def width_v(self, s):
        s = np.asarray(s, np.float64)
        f = np.clip(s / self.s_yokote, 0, 1)
        body = self.motohaba + (self.sakihaba - self.motohaba) * f
        t = np.clip((self.L_arc - s) / self.L_k, 0, 1)
        kis = self.sakihaba * np.interp(t, self.fuk_t, self.fuk_w)
        return np.where(s <= self.s_yokote, body, kis)

    def shinogi_d_v(self, s):
        s = np.asarray(s, np.float64)
        t = np.clip((self.L_arc - s) / self.L_k, 0, 1)
        kis = self.shin_d * self.sakihaba * np.interp(t, self.kos_t, self.kos_d)
        return np.where(s <= self.s_yokote, self.shin_d * self.width_v(s), kis)

    def _hamon_terms(self):
        h = self.spec["hamon"]
        return (V(h["height_over_width"]), V(h["notare_wavelength_cm"]) * 0.01, V(h["notare_amplitude_over_width"]),
                V(h["gunome_wavelength_cm"]) * 0.01, V(h["gunome_amplitude_over_width"]), V(h["boshi_kaeri_over_kissaki"]),
                V(h["kaeri_width_over_boshi"]), V(h["pointed_every_n_gunome"]), V(h["calm_before_yokote_cm"]) * 0.01)

    def hamon_depth_v(self, s):
        """body hamon: depth of the hardened zone measured from the edge (m). Low shallow notare + ko-gunome with
        occasional pointed peaks; the waves calm over the last 3 cm before the yokote (sugu boshi)."""
        hh, ln, an, lg, ag, _, _, every, calm_len = self._hamon_terms()
        s = np.asarray(s, np.float64)
        w = self.width_v(s)
        notare = an * np.sin(2 * np.pi * s / ln + 0.7)
        ph = (s / lg) % 1.0
        g = 1.0 - np.abs(2 * ph - 1)                               # 0..1 triangle per gunome
        k = np.floor(s / lg)
        pointed = (k % every == every // 2)                        # a minority of peaks pointed (togari)
        gun = np.where(pointed, g ** 3.0 * 1.6, np.sqrt(np.clip(g, 0, 1)) * 0.8) - 0.5
        calm = np.clip((self.s_yokote - s) / calm_len, 0, 1)
        return w * (hh + calm * (notare + ag * gun))

    def boshi_depth(self):
        hh = self._hamon_terms()[0]
        return hh * self.sakihaba

    def hardened_v(self, s, d):
        """True where the steel is hardened (hamon in the body, boshi in the kissaki)"""
        s = np.asarray(s, np.float64)
        d = np.asarray(d, np.float64)
        w = self.width_v(s)
        body = d >= w - self.hamon_depth_v(s)
        # boshi: within Db of the edge curve (runs along the fukura, turns round short of the point = komaru),
        # plus a very shallow kaeri hugging the mune
        Db = self.boshi_depth()
        ss = np.concatenate([np.linspace(self.s_yokote - 0.02, self.s_yokote, 20),
                             self.L_arc - self.L_k * (1 - np.linspace(0, 1, 240)) ** 1.6])
        ww = self.width_v(ss)
        near = np.full(s.shape, np.inf)
        for a, b in zip(ss, ww):
            near = np.minimum(near, (s - a) ** 2 + (d - b) ** 2)
        kis = near <= Db * Db
        terms = self._hamon_terms()
        kaeri = (self.L_arc - s <= Db + terms[5] * self.L_k) & (d <= terms[6] * Db)
        return np.where(s <= self.s_yokote, body, kis | kaeri)

    def zone_v(self, s, d):
        s = np.asarray(s, np.float64)
        d = np.asarray(d, np.float64)
        w = self.width_v(s)
        k = np.where(s <= self.s_yokote, self.motokasane + (self.sakikasane - self.motokasane) * np.clip(s / self.s_yokote, 0, 1),
                     self.sakikasane * (self.k_tip + (1 - self.k_tip) * np.clip((self.L_arc - s) / self.L_k, 0, 1) ** self.k_exp))
        ds = np.minimum(self.shinogi_d_v(s), 0.9 * w)
        mb = np.minimum(self.mune_bevel * k, 0.8 * ds)
        z = np.full(s.shape, self.ZONES["ji"], np.int8)
        z = np.where(s > self.s_yokote, self.ZONES["kissaki"], z)
        z = np.where(self.hardened_v(s, d), self.ZONES["hamon"], z)
        z = np.where(d < ds, self.ZONES["shinogi_ji"], z)
        z = np.where(d < mb, self.ZONES["mune"], z)
        z = np.where((d < 0) | (d > w) | (s < 0) | (s > self.L_arc), self.ZONES["outside"], z)
        return z

    def model_to_sd(self, y, z):
        """inverse of to_model in the side plane: (y, z) -> (s, d)"""
        cy, cz = self.y_machi, self.z_mune0 - self.R
        dy, dz = np.asarray(y) - cy, np.asarray(z) - cz
        th = np.arctan2(dy, dz)
        rho = np.hypot(dy, dz)
        return th * self.R, rho - self.R

    # ------------------------------------------------------------------ tsuka
    def tsuka_scale(self, y):
        """ryugo: 1 at the fuchi end of the wrap, waist, kashira_scale at the kashira end"""
        top, bot = self.y_wrap[1], self.y_wrap[0]
        f = (top - y) / (top - bot)             # 0 at the fuchi, 1 at the kashira
        a = self.waist_at
        if f <= a:
            return 1 + (self.waist - 1) * math.sin(0.5 * math.pi * f / a)
        return self.waist + (self.kashira_scale - self.waist) * math.sin(0.5 * math.pi * (f - a) / (1 - a))

    def tsuka_offset_z(self, y):
        """tsuka sori: the kashira end moves towards the mune (-Z), parabolic from the fuchi"""
        f = (self.y_tsuka_top - y) / self.tsuka_len
        return -self.tsuka_sori * f * f

    def summary(self):
        return {
            "R_m": self.R, "L_arc_m": self.L_arc, "s_yokote_m": self.s_yokote, "kissaki_m": self.L_k,
            "tip": self.tip().tolist(), "y_tsuka_top": self.y_tsuka_top, "y_end": self.y_end,
            "windows": self.n_windows, "pitch_eff_cm": self.pitch_eff * 100,
            "y_menuki_omote": self.y_menuki_omote, "y_menuki_ura": self.y_menuki_ura, "y_mekugi": self.y_mekugi,
        }


if __name__ == "__main__":
    g = KatanaGeom()
    for k_, v_ in g.summary().items():
        print(k_, v_)
    # checks: chord length and sori of the mune line
    p0, p1 = g.mune_point(0), g.tip()
    chord = np.linalg.norm(p1 - p0)
    ss = np.linspace(0, g.L_arc, 2001)
    pts = np.array([g.mune_point(s) for s in ss])
    dirv = (p1 - p0) / chord
    dev = [np.linalg.norm(np.cross(p - p0, dirv)) for p in pts]
    i = int(np.argmax(dev))
    print("chord %.4f m (nagasa %.4f)  sori %.4f m at %.3f of the chord" % (chord, g.nagasa, max(dev), np.dot(pts[i] - p0, dirv) / chord))
