"""statues.py - the FX2 statue catalogue: every sculpted mesh the prop builders use, with its LOD face targets.

  python statues.py [name ...] [--force]     builds (or loads from spikes/FX2/meshes/) and prints the face counts
  get(name)                                  -> the mesh data (statuekit.statue)

Targets are Res 1 / Res 2 / Res 3 triangles for the FIGURE ONLY (pedestals, halos and cabinets are kit geometry in
the props). PLAYBOOK §12: statues of people / deities 'as needed (aim <= 3,000)'; komainu / kitsune likewise.
"""
import sys

import figures as G
import statuekit as K

CAT = {
    # name: (build, params, (R1, R2, R3))
    "nyorai_jo": (G.seated_nyorai, {"mudra": "jo"}, (2800, 1000, 340)),        # Amida, jobon-josho-in
    "nyorai_semui": (G.seated_nyorai, {"mudra": "semui"}, (2800, 1000, 340)),  # Shaka, semui-in + yogan-in
    "kannon": (G.standing_kannon, {}, (2600, 950, 320)),
    "jizo": (G.standing_monk, {}, (2600, 950, 320)),                              # altar Jizo (wood)
    "jizo_stone": (G.standing_monk, {"stone": True}, (2400, 860, 290)),           # roadside stone Jizo
    "jizo_child": (G.child_jizo, {}, (1100, 420, 150)),
    "komainu_a_a": (G.komainu, {"mouth": "a", "style": "a"}, (2800, 1000, 340)),
    "komainu_a_un": (G.komainu, {"mouth": "un", "style": "a"}, (2800, 1000, 340)),
    "komainu_b_a": (G.komainu, {"mouth": "a", "style": "b"}, (2600, 950, 320)),
    "komainu_b_un": (G.komainu, {"mouth": "un", "style": "b"}, (2600, 950, 320)),
    "kitsune_key": (G.kitsune, {"item": "key"}, (2000, 750, 250)),
    "kitsune_jewel": (G.kitsune, {"item": "jewel"}, (2000, 750, 250)),
    "lotus": (G.lotus_seat, {}, (700, 260, 90)),
    "mask_okina": (G.kagura_mask, {"kind": "okina"}, (400, 150, 50)),
    "mask_oni": (G.kagura_mask, {"kind": "oni"}, (400, 150, 50)),
    "mask_okame": (G.kagura_mask, {"kind": "okame"}, (400, 150, 50)),
    "mask_hyottoko": (G.kagura_mask, {"kind": "hyottoko"}, (400, 150, 50)),
}


def get(name, force=False):
    b, p, lods = CAT[name]
    return K.statue(name, b, lods=lods, params=p, force=force)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for n in args or list(CAT):
        md = get(n, force="--force" in sys.argv)
        print("%-16s faces %s" % (n, md["faces"]), flush=True)
