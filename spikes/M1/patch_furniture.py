"""M1: point B3a's kori at jp_m_wicker_aged and B3a's firewood (jp_f_firewood) at the i22 firewood materials.
Scoped: only kori_parts() / kori() in props_storage.py and firewood() in props_kitchen.py change."""
import os
import re

B3A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B3a")


def scoped(path, start, end, subs, imp):
    s = open(path, "rb").read().decode()
    i = s.index(start)
    j = s.index(end, i)
    body = s[i:j]
    for a, b in subs:
        n = body.count(a)
        assert n > 0, (path, a)
        body = body.replace(a, b)
    s = s[:i] + body + s[j:]
    a, b = imp
    assert s.count(a) == 1, (path, a)
    s = s.replace(a, b)
    open(path, "wb").write(s.encode())
    print("patched", path)


scoped(os.path.join(B3A, "props_storage.py"), "def kori_parts(", "\n# ======", [("WEAVE", "WICKER")],
       ("INDIGO, KINARI, LACQUER, WEAVE, LITTER)", "INDIGO, KINARI, LACQUER, WEAVE, LITTER, WICKER)"))
scoped(os.path.join(B3A, "props_kitchen.py"), "def firewood(kind=", "\ndef bundle(", [
    ("stack(rows_keep=3 if state != \"intact\" else None, seed=3)",
     "stack(rows_keep=3 if state != \"intact\" else None, seed=3, mats=(FIREWOOD, FIREEND))"),
    ("split_log(rng, 0.0, 0.05, 0.05, -0.21, 0.21, full=True)",
     "split_log(rng, 0.0, 0.05, 0.05, -0.21, 0.21, mats=(FIREWOOD, FIREEND), full=True)"),
    ("ss = bundle(rng, broken=broken)", "ss = bundle(rng, broken=broken, mats=(FIREWOOD, FIREEND))"),
    ("st = box(-0.012, 0.012, 0.0, 0.02, -0.40, 0.40, LOGWOOD, vis=(1,))",
     "st = box(-0.012, 0.012, 0.0, 0.02, -0.40, 0.40, FIREWOOD, vis=(1,))"),
], ("RIVER, LOGWOOD, ENDGRAIN, TAWARA, ASH,\n                  LITTER)",
    "RIVER, LOGWOOD, ENDGRAIN, TAWARA, ASH,\n                  LITTER, FIREWOOD, FIREEND)"))
