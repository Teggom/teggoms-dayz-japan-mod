import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "parts", "kit"))
def tagcount(p):
    c = {1: collections.Counter(), 2: collections.Counter(), 3: collections.Counter()}
    for s in p.solids:
        for k in (1, 2, 3):
            if k in s.vis:
                c[k][s.tag] += len(s.faces)
    for k in (1, 2, 3):
        print("R%d" % k, sum(c[k].values()), c[k].most_common(14))
