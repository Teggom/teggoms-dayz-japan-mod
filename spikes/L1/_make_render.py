"""One-off: derive spikes/L1/render_l1.py from spikes/B3a/render.py (B3a's file is only read)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "..", "B3a", "render.py"), "rb").read().decode("utf-8").replace("\r\n", "\n")
rep = [
    ('r"""render.py - look renders and contact sheets for the B3a props, FROM THE WRITTEN MLOD MASTERS (out/<cat>/*.p3d).',
     'r"""render_l1.py - L1 (life layer) look renders and contact sheets: a copy of spikes/B3a/render.py (B3a\'s file is\n'
     'not changed) pointed at spikes/L1/out, with a backdrop wall for wall / post props and a beam over hanging props,\n'
     'FROM THE WRITTEN MLOD MASTERS (out/<cat>/*.p3d).'),
    ('research/interior/contact_sheets/b3a_<group>.jpg', 'research/interior/contact_sheets/l1_<group>.jpg'),
    ('''GROUPS = [
    ("kitchen", "Kitchen, hearth and water", ["jp_f_kama", "jp_f_jizai_kagi", "jp_f_mizugame", "jp_f_oke",
                                              "jp_f_tana", "jp_f_firewood", "jp_f_jar"]),
    ("heat_shop", "Heat and light, office and shop", ["jp_f_andon", "jp_f_hibachi", "jp_f_tabakobon", "jp_f_zukue",
                                                      "jp_f_choba_goshi", "jp_f_misedana", "jp_f_goods_general"]),
    ("storage", "Storage and packing", ["jp_f_nagamochi", "jp_f_tansu", "jp_f_kori", "jp_f_box", "jp_f_tawara",
                                        "jp_f_rack"]),
    ("bedding_debris", "Bedding, mats and dead-world litter", ["jp_f_futon_stack", "jp_f_futon_laid", "jp_f_mushiro",
                                                               "jp_f_debris"]),
]''', '''GROUPS = [   # (key, title, category): every L1 prop of the category, in life-layer order; sheets of up to 7 props
    ("a_wall", "A. On the walls, posts and beams", "wall"),
    ("b_religious", "B. The religious corner", "religious"),
    ("c_meal", "C. Meals and kitchen life", "meal"),
    ("d_living", "D. Living rooms and bedrooms", "living"),
    ("e_work", "E. Work at home", "work"),
    ("f_tier", "F. Tier markers and the rest", "tier"),
]'''),
    ('''            if item.get("wall"):''', '''            if item.get("beam"):
                xs = [p[0] for p in lod.points]
                bo = bpy.data.objects.new("beam", bpy.data.meshes.new("beam"))
                bpy.context.scene.collection.objects.link(bo)
                x0b, x1b = min(xs) + ox - 0.10, max(xs) + ox + 0.10
                vb = [(x, y, z) for x in (x0b, x1b) for y in (oz - 0.07, oz + 0.07) for z in (lift, lift + 0.14)]
                bo.data.from_pydata(vb, [], [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4],
                                             [1, 5, 7, 3]])
                bo.data.materials.append(g["plain"]("beamc", (0.20, 0.15, 0.11)))
            if item.get("wall"):'''),
    ('''            lod_mesh(lod, "m", (ox, oz))''', '''            lift = item.get("lift", 0.0)
            lod_mesh(lod, "m", (ox, oz), lift=lift)'''),
    ('''                    ob = lod_mesh(ge[0], "geo", (ox, oz), solid_mat=red)''',
     '''                    ob = lod_mesh(ge[0], "geo", (ox, oz), solid_mat=red, lift=lift)'''),
    ('''    def lod_mesh(lod, name, off=(0.0, 0.0), solid_mat=None):''',
     '''    def lod_mesh(lod, name, off=(0.0, 0.0), solid_mat=None, lift=0.0):'''),
    ('''            bp = [(p[0] + off[0], p[2] + off[1], p[1]) for p in pts]''',
     '''            bp = [(p[0] + off[0], p[2] + off[1], p[1] + lift) for p in pts]'''),
    ('''            for p in lod.points:
                q = (p[0] + ox, p[2] + oz, p[1])''', '''            for p in lod.points:
                q = (p[0] + ox, p[2] + oz, p[1] + lift)'''),
    ('''def load_props(ids=None):
    sys.path.insert(0, HERE)
    import build
    reg = build.registry()''', '''def load_props(ids=None):
    sys.path.insert(0, HERE)
    import build_l1
    reg = build_l1.l1_props(build_l1.B.registry())'''),
    ('''def row_items(prop, gap=0.25, lod=1.0, geo=False, only=None, per_row=6, wall=False):''',
     '''def row_items(prop, gap=0.25, lod=1.0, geo=False, only=None, per_row=6, wall=False, anchors=None):'''),
    ('''            row.append({"p3d": p, "off": [x - x1, zc - (z1 + z0) / 2 if not wall else zc], "lod": lod, "geo": geo,
                        "wall": wall})''', '''            an = (anchors or {}).get(p, "floor")
            row.append({"p3d": p, "off": [x - x1, zc - (z1 + z0) / 2 if an != "wall" else zc], "lod": lod, "geo": geo,
                        "wall": an == "wall", "beam": an == "hang", "lift": 2.2 if an == "hang" else 0.0})'''),
    ('''        items = row_items(prop, per_row=prop.get("per_row", 6), wall=prop.get("wall", False))''',
     '''        items = row_items(prop, per_row=prop.get("per_row", 6), anchors=anchors_of(prop))'''),
    ('''            lodrow.append({"p3d": p, "off": [x - mx, 0.0], "lod": rr, "geo": False, "wall": prop.get("wall", False)})''',
     '''            an = anchors_of(prop).get(p, "floor")
            lodrow.append({"p3d": p, "off": [x - mx, 0.0], "lod": rr, "geo": False, "wall": an == "wall",
                           "beam": an == "hang", "lift": 2.2 if an == "hang" else 0.0})'''),
    ('''                lodrow.append({"p3d": pa, "off": [x - max(q[0] for q in ra.points), 0.0], "lod": 1.0, "geo": True})''',
     '''                lodrow.append({"p3d": pa, "off": [x - max(q[0] for q in ra.points), 0.0], "lod": 1.0, "geo": True,
                               "wall": anchors_of(prop).get(pa) == "wall"})'''),
    ('''    chk = json.load(open(os.path.join(HERE, "checks.json"), encoding="utf-8"))["models"]''',
     '''    chk = json.load(open(os.path.join(HERE, "checks.json"), encoding="utf-8"))["models"]
    groups = []
    for key, title, cat in GROUPS:
        ids = [p["id"] for p in props_all if p["cat"] == cat]
        for k in range(0, len(ids), 7):
            groups.append((key + ("" if k == 0 else "_%d" % (k // 7 + 1)), title, ids[k:k + 7]))'''),
    ('''    for key, title, ids in GROUPS:
        ids = [i for i in ids if i in byid]''', '''    for key, title, ids in groups:
        ids = [i for i in ids if i in byid]'''),
    ('''            refs = (build.BL.get(pid, {}).get("refs") or [])''',
     '''            refs = [{"id": r} for r in prop.get("refs", [])] + (build.BL.get(pid, {}).get("refs") or [])'''),
    ('''        d.text((14, 14), "B3a interior props, wave 1: %s. Left: build-list references. Middle: every model of the "
               "prop (intact first, abandoned after), Resolution 1, from the written MLOD. Right: LOD 1-2(-3) + "
               "collision (red) of an abandoned state." % title, fill=(235, 235, 235), font=fb)''',
     '''        d.text((14, 14), "L1 life layer, interior: %s. Left: local references. Middle: every model (intact first, "
               "as left after), Resolution 1 from the written MLOD, on a wall or under a beam where it mounts. Right: "
               "LOD 1-2(-3) + collision (red)." % title, fill=(235, 235, 235), font=fb)'''),
    ('''            name = (build.BL.get(pid, {}).get("name") or "")[:70]''',
     '''            name = ("#%s " % prop.get("ll", "") + (prop["models"][0]["display"] or ""))[:70]'''),
    ('''        out = os.path.join(SHEETS, "b3a_%s.jpg" % key)''', '''        out = os.path.join(SHEETS, "l1_%s.jpg" % key)'''),
    ('''def make_jobs(props):''', '''_ANCH = {}


def anchors_of(prop):
    """{master path: anchor} of every model of the prop (from the sidecar written by build_l1)."""
    if prop["id"] not in _ANCH:
        sc = json.load(open(os.path.join(DEV, "src", "JP", "furniture", prop["cat"], prop["id"] + ".prop.json"),
                            encoding="utf-8"))
        _ANCH[prop["id"]] = {os.path.join(HERE, "out", prop["cat"], os.path.basename(m["p3d"])): m["anchor"]
                             for m in sc["models"]}
    return _ANCH[prop["id"]]


def make_jobs(props):'''),
]
for a, b in rep:
    assert a in s, a[:90]
    s = s.replace(a, b)
with open(os.path.join(HERE, "render_l1.py"), "wb") as f:
    f.write(s.encode("utf-8"))
print("ok")
