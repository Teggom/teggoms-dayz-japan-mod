"""Trim (jp_p_trim_*): the W1 splash / grime band as an alpha decal (jp_m_wall_grime, PLAYBOOK §6.5).
Visual only (never in Geometry / View / Fire); 3 mm proud of the surface it covers. Wear _w0/_w1/_w2 = dust / splash /
heavy mud, chosen per instance like every library material."""
from .core import Part, sheet, KEN, POST

BAND = 0.45          # decal height: the 0-0.4 m splash zone + a soft top edge


def grime_band(part, x0, x1, face_z, y0=0.0, h=BAND, off=0.003, normal=(0.0, 0.0, 1.0), axis="x"):
    """A band on a face of constant z (axis 'x') or constant x (axis 'z'), outward normal given."""
    z = face_z + off * (1 if (normal[2] if axis == "x" else normal[0]) >= 0 else -1)
    if axis == "x":
        q = [(x0, y0, z), (x1, y0, z), (x1, y0 + h, z), (x0, y0 + h, z)]
    else:
        q = [(z, y0, x0), (z, y0, x1), (z, y0 + h, x1), (z, y0 + h, x0)]
    uv = [(x0 / 2.0, 1.0), (x1 / 2.0, 1.0), (x1 / 2.0, 0.0), (x0 / 2.0, 0.0)]
    part.add(sheet([q], "wall_grime", normal, vis=(1, 2), uvs=[uv], tag="grime"))


def part_grime(variant):
    p = Part("jp_p_trim_grime", variant, "trim", tiers=[1, 2, 3],
             used_for={"_wall": "W1 splash band over the foot of a wall (shown on shikkui; on earth walls it is a "
                                "subtle ~10 % darkening, as sampled)",
                       "_post": "W1 splash band wrapped round the foot of a 0.12 post"}[variant],
             recipe="trim.grime_band(part, x0, x1, face_z, y0, h, normal, axis)",
             datum="y 0 = sill / grade the band starts at; band 0.45 high, 3 mm proud of the face")
    if variant == "_wall":
        grime_band(p, POST / 2, KEN - POST / 2, 0.0375)
        p.conn("post", (0, 0, 0))
        p.conn("post", (KEN, 0, 0))
    else:
        h = POST / 2
        grime_band(p, -h, h, h, normal=(0.0, 0.0, 1.0))
        grime_band(p, -h, h, -h, normal=(0.0, 0.0, -1.0))
        grime_band(p, -h, h, h, normal=(1.0, 0.0, 0.0), axis="z")
        grime_band(p, -h, h, -h, normal=(-1.0, 0.0, 0.0), axis="z")
        p.conn("post", (0, 0, 0))
    p.dim("band_height_m", "0-0.4 zone (W1)", BAND, tol=0.06)
    p.notes.append("palette grime_splash (sampled on x08_hirose_earthwall); matcheck in src/JP/common/materials/"
                   "checks_parts.json")
    return p


def register(reg):
    reg("jp_p_trim_grime", ["_wall", "_post"], part_grime)
