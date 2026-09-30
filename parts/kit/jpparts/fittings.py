"""Built-in fittings merged into a furnished variant (C3, 2026-09-30): jp_p_fit_kamado (research/interior/BUILD_LIST.md
fitting 3), promoted from buildings/machiya_t3_01.kamado so any shell's furnished variant can get its stove on the
kamado spot C2 left (rural.py 'kamado' fittings) or in a townhouse / inn kitchen doma.

    info = kamado(part, rect, floor_y, mouth="+x", n=2, tier=3)   # rect = (x0, x1, z0, z1) plan, model frame

The stove: a cut-stone base course, a clay (T1-2 wall_nakanuri_int) or plastered (T3 wall_shikkui_int) body 0.72 high,
n fire mouths on the `mouth` side (sooted boards round each mouth), an iron rim per pot (the rim top = the pot seat:
jp_f_kama / jp_f_seiro_* seat_y), one Geometry box. Returns {top, rim_top, rims [(x, z)], seat box (x0, x1, y0, y1,
z0, z1), rect}. The caller adds the rect (+0.25) to the floor's obstacles (loot points, head-room samples).
"""
from .core import box
from .shapes import tube

HEIGHT = 0.72
RIM_H = 0.03


def kamado(part, rect, floor_y, mouth="+x", n=2, tier=3, soot_wall=None):
    x0, x1, z0, z1 = rect
    top = floor_y + HEIGHT
    body = "wall_shikkui_int" if tier >= 3 else "wall_nakanuri_int"
    part.add(box(x0, x1, floor_y, floor_y + 0.10, z0, z1, "stone_cut", vis=(1, 2, 3), tag="kamado_base"))
    part.add(box(x0, x1, floor_y, top, z0, z1, body, vis=(), geo=True, view=True, fire="dirt", tag="kamado_geo"))
    part.add(box(x0 + 0.02, x1 - 0.02, floor_y + 0.10, top - 0.04, z0 + 0.02, z1 - 0.02, body, vis=(1, 2, 3),
                 tag="kamado_body"))
    part.add(box(x0, x1, top - 0.04, top, z0, z1, body, vis=(1, 2, 3), tag="kamado_top"))
    along_z = mouth in ("+x", "-x")
    L = (z1 - z0) if along_z else (x1 - x0)
    cell = L / n
    rims = []
    r = min(0.22, cell / 2 - 0.05, ((x1 - x0) if along_z else (z1 - z0)) / 2 - 0.06)
    for k in range(n):
        c = (z0 if along_z else x0) + (k + 0.5) * cell
        xc, zc = ((x0 + x1) / 2, c) if along_z else (c, (z0 + z1) / 2)
        if mouth == "+x":
            m = box(x1 - 0.02, x1 + 0.005, floor_y + 0.16, floor_y + 0.42, c - 0.17, c + 0.17, "wood_sooted", vis=(1, 2),
                    tag="fire_mouth")
        elif mouth == "-x":
            m = box(x0 - 0.005, x0 + 0.02, floor_y + 0.16, floor_y + 0.42, c - 0.17, c + 0.17, "wood_sooted", vis=(1, 2),
                    tag="fire_mouth")
        elif mouth == "+z":
            m = box(c - 0.17, c + 0.17, floor_y + 0.16, floor_y + 0.42, z1 - 0.02, z1 + 0.005, "wood_sooted", vis=(1, 2),
                    tag="fire_mouth")
        else:
            m = box(c - 0.17, c + 0.17, floor_y + 0.16, floor_y + 0.42, z0 - 0.005, z0 + 0.02, "wood_sooted", vis=(1, 2),
                    tag="fire_mouth")
        part.add(m)
        part.add(tube((xc, top, zc), (xc, top + RIM_H, zc), r, "metal_iron", n=10, vis=(1,), tag="pot_rim"))
        rims.append((xc, zc))
    if soot_wall:
        # sooted boards on the wall behind the stove (W5): (x0, x1, z0, z1) of a thin plan strip on the wall face
        a, b, c, d = soot_wall
        part.add(box(a, b, top, floor_y + 2.2, c, d, "wood_sooted", vis=(1, 2), tag="soot_boards"))
    return {"top": top, "rim_top": top + RIM_H, "rims": rims, "rect": rect,
            "seat": (x0 - 0.01, x1 + 0.01, floor_y - 0.01, top + RIM_H + 0.10, z0 - 0.01, z1 + 0.01)}
