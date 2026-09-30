"""One-off (L1): add mounts, the life-layer placement helpers and checks D15/D16 to parts/kit/jpparts/decor.py."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "..", "..", "parts", "kit", "jpparts", "decor.py")
s = open(p, "rb").read().decode("utf-8")
assert "\r\n" not in s
rep = [
    ('''Props come from the B3a / B3b sidecars (src/JP/furniture/*/*.prop.json, src/JP/site/*/*.prop.json); their collision
components are read from the MLOD masters (spikes/B3a/out, spikes/B3b/out; rebuild with the B3a / B3b build.py).
''', '''Props come from the B3a / B3b / L1 sidecars (src/JP/furniture/*/*.prop.json, src/JP/site/*/*.prop.json); their
collision components are read from the MLOD masters (spikes/B3a/out, spikes/B3b/out; an L1 sidecar names its own
master, spikes/L1/out; rebuild with the B3a / B3b build.py or spikes/L1/build_l1.py).

Where a prop goes (L1, 2026-09-30): every catalogue entry has a `mount`: wall | post | beam | doorway | surface |
floor | kamado (sidecar 'mount'; B3a / B3b props without one get it from their anchor: 'wall' -> wall, 'hang' ->
beam, else floor). Place wall / post items with on_wall(), beam items with on_beam(), doorway items with in_doorway()
and small things on another prop's loot surface with on_surface(); floor items with item() as before. The helpers set
the flags the checks read (on_floor, hung, host) and do not count visual-only life items against the 5-7 props of a
room (they hang on walls and beams or sit on surfaces: LIFE_LAYER.md "the rule that makes it fit"). When any such
item is placed, check_all adds D15 (surface items rest on their host's surface) and D16 (hanging items keep 2.00 m
head room over the floor unless placed over a hearth / corner / furniture / doorway: it["over"]).
'''),
    ('''                cat[name] = dict(name=name, area=area, folder=folder, p3d=m["p3d"], cls=m.get("class"),
                                 anchor=m.get("anchor", "floor"), bbox=m["bbox"], footprint=m.get("footprint_xz"),
                                 geo=geo, view=view, roadway=bool(m.get("roadway")), loot=m.get("loot_surfaces") or [],
                                 master=os.path.join(DEV, out, folder, name + ".p3d"), hang_y=m.get("hang_y"),
                                 wall_gap=m.get("wall_gap"), state=m.get("state"), well=bool(m.get("well")))''',
     '''                anchor = m.get("anchor", "floor")
                mount = m.get("mount") or {"wall": "wall", "hang": "beam"}.get(anchor, "floor")
                master = os.path.join(DEV, m["master"]) if m.get("master") else os.path.join(DEV, out, folder,
                                                                                            name + ".p3d")
                cat[name] = dict(name=name, area=area, folder=folder, p3d=m["p3d"], cls=m.get("class"),
                                 anchor=anchor, bbox=m["bbox"], footprint=m.get("footprint_xz"),
                                 geo=geo, view=view, roadway=bool(m.get("roadway")), loot=m.get("loot_surfaces") or [],
                                 master=master, hang_y=m.get("hang_y"),
                                 wall_gap=m.get("wall_gap"), state=m.get("state"), well=bool(m.get("well")),
                                 mount=mount, hang_len=m.get("hang_len"), seat_y=m.get("seat_y"), tiers=m.get("tiers"))'''),
    ('''def lods_for(it):''', '''def by_mount(mount, area=None):
    """Catalogue names that mount on a wall / post / beam / doorway / surface / floor / kamado."""
    return sorted(n for n, e in catalog().items() if e["mount"] == mount and (area is None or e["area"] == area))


def _mount_ok(name, allowed):
    m = catalog()[name]["mount"]
    if m not in allowed:
        raise ValueError("%s mounts on %r, not %s" % (name, m, "/".join(allowed)))


def on_wall(name, room, x, z, yaw, floor_y=None, why="", count=None):
    """A wall or post item: (x, z) = the point on the wall / post face (the prop's z = 0 plane), yaw so the prop's +z
    points into the room. Its heights are built in, so y = the room floor (resolved by Decor.place when None).
    Visual-only items do not count against the room's props (count=None)."""
    _mount_ok(name, ("wall", "post"))
    it = item(name, room, x, z, yaw, y=floor_y, why=why)
    it["count"] = bool(catalog()[name]["geo"]) if count is None else count
    it["mounted"] = catalog()[name]["mount"]
    return it


def on_beam(name, room, x, z, yaw, beam_y, why="", over=None, count=False):
    """A beam item: (x, beam_y, z) = the beam (or loft joist) underside where it hangs. over: what it hangs over when
    it drops below the 2.00 m head-room line ('hearth', 'corner', 'furniture', ...): D16 then lets it pass."""
    _mount_ok(name, ("beam",))
    it = item(name, room, x, z, yaw, y=beam_y, why=why, count=count)
    it.update(on_floor=False, hung=True, mounted="beam", over=over)
    return it


def in_doorway(name, room, x, z, yaw, head_y, why=""):
    """A doorway item (inner noren): origin at the door head underside, centred in the opening, in its plane."""
    _mount_ok(name, ("doorway",))
    it = item(name, room, x, z, yaw, y=head_y, why=why, count=False)
    it.update(on_floor=False, hung=True, mounted="doorway", over="doorway")
    return it


def on_surface(name, host, surface=None, dx=0.0, dz=0.0, yaw=0.0, why="", count=False):
    """A small item on another placed prop's loot surface (a shelf board, chest lid, desk top): (dx, dz) in the
    host's frame from the surface's centre; yaw relative to the host. The surface keeps its loot points: leave them
    room (the checks do not test that)."""
    _mount_ok(name, ("surface", "floor"))
    ss = host["info"]["loot"]
    if not ss:
        raise ValueError("%s has no loot surface to put %s on" % (host["name"], name))
    s = next((q for q in ss if q["name"] == surface), None) if surface else ss[0]
    if s is None:
        raise KeyError("%s has no surface %r" % (host["name"], surface))
    x0, z0, x1, z1 = s["rect"]
    local = ((x0 + x1) / 2 + dx, s["y"], (z0 + z1) / 2 + dz)
    m = to_model(host, local)
    it = item(name, host["room"], m[0], m[2], host["yaw"] + yaw, y=m[1], why=why, count=count)
    it.update(on_floor=False, mounted="surface", host=host, surface=s["name"], local=local)
    return it


def lods_for(it):'''),
    ('''    rec("D10 C6 bases on the floor (0-2 cm), wall-hung props against a wall", not bad,
        "%d props" % len(D.items) if not bad else "BAD %s" % bad[:4])''', '''    rec("D10 C6 bases on the floor (0-2 cm), wall-hung props against a wall", not bad,
        "%d props" % len(D.items) if not bad else "BAD %s" % bad[:4])
    # ---- life-layer items (L1): only when some are placed, so earlier buildings keep their check count
    surf = [it for it in D.items if it.get("mounted") == "surface"]
    if surf:
        bad = []
        for it in surf:
            h = it["host"]
            s = next(q for q in h["info"]["loot"] if q["name"] == it["surface"])
            x0, z0, x1, z1 = s["rect"]
            lx, ly, lz = it["local"]
            if abs(ly - s["y"]) > 0.02 or not (x0 - 0.02 <= lx <= x1 + 0.02 and z0 - 0.02 <= lz <= z1 + 0.02):
                bad.append((it["name"], "off %s/%s" % (h["name"], s["name"])))
        rec("D15 surface items rest on their host's surface (+-2 cm, inside its rect)", not bad,
            "%d items" % len(surf) if not bad else "BAD %s" % bad[:4])
    hung = [it for it in D.items if it.get("mounted") in ("beam", "doorway")]
    if hung:
        bad = []
        for it in hung:
            fy = D.floors[it["room"]]["y"] if it["room"] in D.floors else 0.0
            low = it["y"] - (it["info"].get("hang_len") or 0.0)
            if low - fy < 2.00 - 1e-6 and not it.get("over"):
                bad.append((it["name"], "bottom %.2f over the floor" % (low - fy)))
        rec("D16 hanging items keep 2.00 m head room (or hang over a hearth / corner / furniture / doorway)", not bad,
            "%d items" % len(hung) if not bad else "BAD %s" % bad[:4])'''),
]
for a, b in rep:
    assert a in s, a[:80]
    s = s.replace(a, b)
with open(p, "wb") as f:
    f.write(s.encode("utf-8"))
print("patched")
