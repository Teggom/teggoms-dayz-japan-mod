"""Model -> MLOD p3d (every LOD) using agent B's mlod_b.py."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "tools")))
import mlod_b as mlod  # noqa: E402

from .geom import face_uvs  # noqa: E402
from .materials import MATS, ROADWAY, tex_path, rvmat_path, fire_rvmat  # noqa: E402

RES_VALUES = {1: 1.0, 2: 2.0, 3: 3.0}      # same resolution values as vanilla house_1w01


def _door_sels(lod, model):
    # door selections first, so they come before ComponentNN in every LOD (vanilla/sample order)
    for d in model.doors:
        lod.selections.setdefault(d.bone, ({}, set()))


def visual_lod(model, k):
    lod = mlod.Lod(RES_VALUES[k])
    _door_sels(lod, model)
    for s in model.solids:
        if k not in s.vis:
            continue
        for fi in range(len(s.faces)):
            mat = s.face_mat(fi)
            uvs = face_uvs(s, fi, MATS[mat])
            face, pis = lod.add_flat_face(s.face_points(fi), s.outward(fi), uvs, tex_path(mat), rvmat_path(mat))
            if s.door:
                lod.select(s.door, {pi: 1.0 for pi in pis}, [face])
    for d in model.doors:
        if not lod.selections[d.bone][1]:
            raise ValueError("door %s has no faces in resolution %d" % (d.bone, k))
    return lod


def component_lod(model, res, which):
    lod = mlod.Lod(res)
    _door_sels(lod, model)
    n = 0
    for s in model.solids:
        if which == "geo" and not s.geo:
            continue
        if which == "view" and not s.view:
            continue
        if which == "fire" and not s.fire:
            continue
        n += 1
        mat = fire_rvmat(s.fire) if which == "fire" else ""
        pis, fis = lod.add_closed_solid(s.verts, s.faces, "", mat)
        lod.select("Component%02d" % n, {pi: 1.0 for pi in pis}, fis)
        if s.door:
            lod.select(s.door, {pi: 1.0 for pi in pis}, fis)
    if which == "geo":
        lod.properties["class"] = "house"
        lod.properties["map"] = "house"
        lod.properties["damage"] = "no"
        lod.properties["autocenter"] = "0"
        total = model.params["mass"]
        lod.mass = [total / len(lod.points)] * len(lod.points)
    return lod


def memory_lod(model):
    lod = mlod.Lod(mlod.LOD_MEMORY)
    # axes first (their two points must keep their order: first -> second = slide direction)
    for name in sorted(model.memory):
        pts = model.memory[name]
        pis = [lod.add_point(pt) for pt in pts]
        lod.select(name, {pi: 1.0 for pi in pis})
    return lod


def roadway_lod(model):
    lod = mlod.Lod(mlod.LOD_ROADWAY)
    from .geom import newell, norm
    for pts, surf in model.roadway:
        n = norm(newell(pts))
        if n[1] < 0:
            n = (-n[0], -n[1], -n[2])
        lod.add_flat_face(pts, n, [(0.0, 0.0)] * len(pts), ROADWAY[surf], "")
    return lod


def build_lods(model):
    lods = [visual_lod(model, 1), visual_lod(model, 2), visual_lod(model, 3),
            component_lod(model, mlod.LOD_GEOMETRY, "geo"),
            memory_lod(model),
            roadway_lod(model),
            component_lod(model, mlod.LOD_VIEW_GEOMETRY, "view"),
            component_lod(model, mlod.LOD_FIRE_GEOMETRY, "fire")]
    return lods


def write_p3d(model, path):
    lods = build_lods(model)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mlod.write_mlod(path, lods)
    return lods
