"""Debug: for each body of a prop, its nearest other body (distance, centres).  python spikes/FX6/nearest.py <stem>"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import propfloat as F  # noqa: E402
from jpparts import decor as DC  # noqa: E402

inf = DC.catalog()[sys.argv[1]]
PS = [p for p in F.pieces(F.res1(inf["master"])) if F.tri_area_centroid(p[1])[0] >= F.MIN_AREA]
n = len(PS)
nb = {i: set() for i in range(n)}
for i in range(n):
    for j in range(i + 1, n):
        if F.contact(PS[i], PS[j]) is not None:
            nb[i].add(j)
            nb[j].add(i)
body = [-1] * n
k = 0
for s in range(n):
    if body[s] >= 0:
        continue
    st = [s]
    body[s] = k
    while st:
        i = st.pop()
        for j in nb[i]:
            if body[j] < 0:
                body[j] = k
                st.append(j)
    k += 1
for b in range(k):
    V = np.concatenate([PS[i][0] for i in range(n) if body[i] == b])
    best = (9, None)
    for b2 in range(k):
        if b2 == b:
            continue
        for j in range(n):
            if body[j] != b2:
                continue
            d = float(F.pt_tri_dist(V, PS[j][1]).min())
            if d < best[0]:
                best = (d, b2)
    print("body %d: %d pieces, x %.2f..%.2f y %.2f..%.2f z %.2f..%.2f; nearest body %s at %.3f m" % (
        b, sum(1 for i in range(n) if body[i] == b), V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max(),
        V[:, 2].min(), V[:, 2].max(), best[1], best[0]))
