r"""uvwood.py - the one shared texture-variety pass for wood (FX3, 2026-10-01; DRAFT in spikes/FX3, phase 2 moves it
to parts/kit/jpparts/uvwood.py).

Why: every wood face is mapped world-planar (u, v = metres / tile in the part's frame, v = along the grain), so every
torii pole, post and board of the same height range shows the same knot at the same height, and a 2 m tile repeats
on every long member.

What it does, on a finished Part (all solids finalized, in the MODEL frame, i.e. after parts are placed / merged):
  * Each wood material is ONE atlas texture (2048 x 1024 = 4 m across the grain x 2 m along it at 512 px/m): the old
    1024 px tile (rolled so a board joint sits at u = 0) beside a board-shuffled variant of it. The four 512 px
    columns are the four PATCHES (A, B = the original boards; C = the variant's weathered half, D = its fresher
    half). The whole strip tiles across u (both seams are board joints) and every column tiles along v.
  * Every UV GROUP gets one random affine map  u' = fu * u * (tile / W) + U0,  v' = fv * v * (tile_v / H) + V0
    (fu, fv = +-1 flips; U0 picks the patch and the offset across the grain, V0 the offset along it). Upstream code
    keeps computing UVs exactly as today (metres / sidecar tile); only this pass knows the atlas.
  * UV groups:
      plane  flat faces with auto UVs ('world' / 'grain' / 'fit'): all faces of the same material in the same plane
             (normal to 0.01, offset clustered within 2 mm). Coplanar overlapping faces therefore keep identical
             mappings, so jpparts.zfight's 'looks the same' verdicts stay true (no new C20 flicker).
             Posts in one wall line share the map but sit at different u (their x), so they still differ.
      solid  smooth solids (fkit lathe / skit tube: per-vertex normals) and explicit uv lists (grid / strip / moss
             strips / billets): one map for the whole solid, so the grain stays continuous round a turned post.
      band   faces fkit.band_fit put into one clean plank band of jp_m_wood_interior (pixel-locked): u' = u/2 + h/2
             with h = 0 / 1 (the same band in the original or the variant half; the variant keeps every groove at
             the same pixel), no u flip; v offset and flip are free.
  * Deterministic: the seed is FNV-1a of (salt = model name, group key); the group key is built from rounded
    geometry, never from build order, so a rebuild gives the same UVs and adding a prop elsewhere changes nothing.
  * Grain along the member is upstream's job (core.face_uvs 'grain' / sidecar 'along member'); this pass never
    swaps axes. Tile scale: 2 m along the grain per repeat, patches 1 m across.

Not touched: every material not in ATLAS (text decals, cells, stone, roofs ...), end grain (jp_m_wood_endgrain*:
centred discs), jp_m_wood_firewood (a semantic 2-band atlas, bark | split, already offset per billet by woodpile.py).
Moss decal (jp_m_decal_moss) is in ATLAS as a plain 2 m tile: solid groups, flips + offsets, no patches.

API:
  remap_part(P, salt=None)      in place, idempotent (solid._uvw); returns {'faces': n, 'groups': n}
  install(core_mod, fkit_mod)   phase 1 only: monkeypatch Part.lods / fkit.band_fit for the FX3 samples
"""
import bisect
import math
import random

# library key -> atlas: W, H = the atlas' real size (m); lock = 'band' for pixel-locked plank bands
ATLAS_WOOD = dict(W=4.0, H=2.0, patches=4, flip=True)
ATLAS = {
    "wood_weathered": ATLAS_WOOD, "wood_street_dark": ATLAS_WOOD, "wood_kuro": ATLAS_WOOD,
    "wood_sooted": ATLAS_WOOD, "wood_bengara": ATLAS_WOOD, "wood_new": ATLAS_WOOD, "wood_silver": ATLAS_WOOD,
    "wood_interior": dict(ATLAS_WOOD, lock="band"), "ceil_boards": ATLAS_WOOD,
    "floor_boards_int": ATLAS_WOOD, "floor_boards_rough": ATLAS_WOOD,
    "decal_moss": dict(W=2.0, H=2.0, patches=1, flip=True),
}
ALLOW_FLIP = True        # one switch: if the in-game check shows inverted bumps on flipped faces, set False
NQ = 100.0               # normal quantisation (as zfight)
DGAP = 0.002             # plane offsets closer than this share a group (zfight TOL is 1 mm)


def fnv(s):
    h = 2166136261
    for ch in s.encode("utf-8"):
        h = ((h ^ ch) * 16777619) & 0xFFFFFFFF
    return h


def _r(x, q=1000.0):
    return int(round(x * q))


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _solid_sig(s):
    xs = [v[0] for v in s.verts]
    ys = [v[1] for v in s.verts]
    zs = [v[2] for v in s.verts]
    return "%d,%d,%d|%d,%d,%d|%d" % (_r(sum(xs) / len(xs)), _r(sum(ys) / len(ys)), _r(sum(zs) / len(zs)),
                                     _r(max(xs) - min(xs)), _r(max(ys) - min(ys)), _r(max(zs) - min(zs)),
                                     len(s.faces))


def _is_solid_group(s):
    return getattr(s, "vn", None) is not None or isinstance(s.uv, list)


def spec(mat):
    return ATLAS.get(mat)


def _map(salt, key, sp, band=False):
    r = random.Random(fnv("%s|%s" % (salt, key)))
    U0, V0 = r.random(), r.random()
    fu = -1.0 if (sp.get("flip") and ALLOW_FLIP and not band and r.random() < 0.5) else 1.0
    fv = -1.0 if (sp.get("flip") and ALLOW_FLIP and r.random() < 0.5) else 1.0
    h = r.randrange(2)
    return U0, V0, fu, fv, h


def remap_part(P, salt=None, tile_of=None):
    """tile_of(mat) -> (tile_u, tile_v) of the UVs upstream computed (default: core.mat_info of the Part's module)."""
    salt = salt if salt is not None else P.name
    if tile_of is None:
        from jpparts import core              # the kit's library (sidecar tile_size_m / tile_size_v_m)
        tile_of = lambda m: (core.mat_info(m)["tile"], core.mat_info(m)["tile_v"])   # noqa: E731
    # pass 1: plane offsets per (material, quantised normal) for clustering
    planes = {}
    todo = []
    for s in P.solids:
        if getattr(s, "_uvw", False) or s.fuv is None:
            continue
        todo.append(s)
        if _is_solid_group(s):
            continue
        band = getattr(s, "uvband", ())
        for fi in range(len(s.faces)):
            m = s.fm[fi]
            if m not in ATLAS or fi in band:
                continue
            n = s.fn[fi]
            nq = (_r(n[0], NQ), _r(n[1], NQ), _r(n[2], NQ))
            d = _dot(n, s.verts[s.faces[fi][0]])
            planes.setdefault((m, nq), []).append(d)
    clusters = {}
    for k, ds in planes.items():
        ds = sorted(ds)
        starts = []
        prev = None
        for d in ds:
            if prev is None or d - prev > DGAP:
                starts.append(d)
            prev = d
        clusters[k] = starts

    def plane_key(m, n, d):
        nq = (_r(n[0], NQ), _r(n[1], NQ), _r(n[2], NQ))
        st = clusters[(m, nq)]
        i = max(0, bisect.bisect_right(st, d + 1e-9) - 1)
        return "p|%s|%d,%d,%d|%d" % (m, nq[0], nq[1], nq[2], _r(st[i]))

    nf, groups = 0, set()
    for s in todo:
        band = getattr(s, "uvband", ())
        sg = _is_solid_group(s)
        sig = _solid_sig(s) if sg else None
        new = []
        for fi in range(len(s.faces)):
            uv = s.fuv[fi]
            m = s.fm[fi]
            sp = ATLAS.get(m)
            if sp is None:
                new.append(uv)
                continue
            tu, tv = tile_of(m)
            if fi in band:
                n = s.fn[fi]
                d = _dot(n, s.verts[s.faces[fi][0]])
                key = "b|%s|%d,%d,%d|%d" % (m, _r(n[0], NQ), _r(n[1], NQ), _r(n[2], NQ), _r(d)) if not sg else                     "b|%s|%s" % (m, sig)
                U0, V0, fu, fv, h = _map(salt, key, sp, band=True)
                new.append([(a * 0.5 + 0.5 * h, fv * b + V0) for a, b in uv])
            else:
                if sg:
                    key = "s|%s|%s" % (m, sig)
                else:
                    n = s.fn[fi]
                    key = plane_key(m, n, _dot(n, s.verts[s.faces[fi][0]]))
                U0, V0, fu, fv, h = _map(salt, key, sp)
                ku, kv = tu / sp["W"], tv / sp["H"]
                new.append([(fu * a * ku + U0, fv * b * kv + V0) for a, b in uv])
            groups.add(key)
            nf += 1
        s.fuv = new                     # rebind (transformed / merged copies share the old list object)
        s._uvw = True
    return {"faces": nf, "groups": len(groups)}


# ------------------------------------------------------------------------------------------------ phase-1 install
def install(core_mod, fkit_mod=None):
    """FX3 samples only (no shared file is edited): Part.lods() runs remap_part first; fkit.band_fit records the
    pixel-locked faces it maps. Phase 2 does both in the source instead (see PHASE2_PLAN.md)."""
    if getattr(core_mod.Part, "_uvw_installed", False):
        return
    orig = core_mod.Part.lods

    def lods(self, *a, **kw):
        remap_part(self, tile_of=lambda m: (core_mod.mat_info(m)["tile"], core_mod.mat_info(m)["tile_v"]))
        return orig(self, *a, **kw)
    core_mod.Part.lods = lods
    core_mod.Part._uvw_installed = True
    if fkit_mod is not None:
        bf = fkit_mod.band_fit

        def band_fit(s, lo_px, hi_px, normal=(0.0, 0.0, 1.0), tex_px=1024, voff=0.0):
            out = bf(s, lo_px, hi_px, normal, tex_px, voff)
            hit = {fi for fi in range(len(s.faces)) if core_mod.dot(s.fn[fi], normal) > 0.9}
            s.uvband = set(getattr(s, "uvband", ())) | hit
            return out
        fkit_mod.band_fit = band_fit
