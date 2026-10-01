"""M1: one-off patches pointing the firewood props (B3b jp_s_firewood_stack, B3a jp_f_firewood) at the i22 firewood
materials (jp_m_wood_firewood sides, jp_m_wood_endgrain_firewood ends), and the kori at jp_m_wicker_aged.
usage: python patch_firewood.py site|furniture"""
import os
import sys

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def patch(path, reps):
    s = open(path, "rb").read().decode()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:70], s.count(a))
        s = s.replace(a, b)
    open(path, "wb").write(s.encode())
    print("patched", path)


def site():
    patch(os.path.join(SP, "B3b", "props_wood.py"), [
        ("MUSHIRO, PAPER, NOREN, KINARI, ENDG, LEAF, SUMI, BENGARA)",
         "MUSHIRO, PAPER, NOREN, KINARI, ENDG, LEAF, SUMI, BENGARA, FIREWOOD, FIREEND)"),
        ("    s = sheet([q], ENDG, (0.0, 0.0, float(facing)), vis=vis, uvs=[uv])",
         "    s = sheet([q], FIREEND, (0.0, 0.0, float(facing)), vis=vis, uvs=[uv])   # M1: firewood ends (i22)"),
        ('        s = box(a, b, 0.0, hh, z0, z1, {"front": SOOT, "back": SOOT if both else WOOD, "default": WOOD}, vis=vis)',
         '        s = box(a, b, 0.0, hh, z0, z1, {"front": SOOT, "back": SOOT if both else FIREWOOD, "default": FIREWOOD},\n'
         '                vis=vis)'),
        ("        ss = K.bundle(random.Random(5), d=0.40, L=1.05, mats=(WOOD, ENDG), band=ROPE, core_mat=SOOT)",
         "        ss = K.bundle(random.Random(5), d=0.40, L=1.05, mats=(FIREWOOD, FIREEND), band=ROPE, core_mat=SOOT)"),
        ('        P.add(W(-L / 2, L / 2, 0.0, Hh, z0, z1, {"front": SOOT, "back": SOOT, "default": WOOD}, vis=(2,)))',
         '        P.add(W(-L / 2, L / 2, 0.0, Hh, z0, z1, {"front": SOOT, "back": SOOT, "default": FIREWOOD}, vis=(2,)))'),
        ('        s = box(a, b, 0.0, hh, z0, z1, {"front": SOOT, "default": WOOD}, vis=(2,))',
         '        s = box(a, b, 0.0, hh, z0, z1, {"front": SOOT, "default": FIREWOOD}, vis=(2,))'),
        ('            s, _ = K.split_log(rr, 0.0, 0.05, 0.05, -0.16, 0.16, mats=(WOOD, ENDG), full=True, wear="_w2")',
         '            s, _ = K.split_log(rr, 0.0, 0.05, 0.05, -0.16, 0.16, mats=(FIREWOOD, FIREEND), full=True, wear="_w2")'),
    ])


def furniture():
    B3A = os.path.join(SP, "B3a")
    patch(os.path.join(B3A, "fkit.py"), [
        ('WEAVE = "bamboo_weave"\n',
         'WEAVE = "bamboo_weave"\n'
         'WICKER = "wicker_aged"            # M1 (2026-09-30): warm kori wicker (bamboo_weave stays for grey bamboo)\n'
         'FIREWOOD = "wood_firewood"        # M1: split firewood sides, sampled from ref i22\n'
         'FIREEND = "wood_endgrain_firewood"  # M1: firewood log ends, ref i22\n'),
    ])


if __name__ == "__main__":
    {"site": site, "furniture": furniture}[sys.argv[1]]()
