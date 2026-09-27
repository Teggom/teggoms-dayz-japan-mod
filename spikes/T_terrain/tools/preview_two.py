"""One-off: bigger contour previews of two candidate patches (E_east, F_se) to route the road."""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_dem  # noqa: E402
import terrain  # noqa: E402
from preview_candidates import colour, full, mpp, half, layout  # noqa: E402

OUT = os.path.join(gsi_dem.DEV, "spikes", "T_terrain", "previews")
for name, (cx, cy), rot in (("E_east", (2100, 1500), 0.0), ("F_se", (2000, 2500), 0.0), ("E_east_r20", (2100, 1500), 20.0)):
    patch = full[cy - half:cy + half, cx - half:cx + half]
    lay = dict(layout)
    lay["patch_rotate"] = rot
    r = terrain.compose(patch, mpp, lay)
    h = r["h"]
    img = colour(h).resize((1024, 1024), Image.BILINEAR)
    a = np.asarray(img).copy()
    hh = np.kron(h[::-1], np.ones((2, 2)))
    lvl = np.floor(hh / 10.0)
    edge = (np.diff(lvl, axis=0, prepend=lvl[:1]) != 0) | (np.diff(lvl, axis=1, prepend=lvl[:, :1]) != 0)
    a[edge] = (a[edge] * 0.55).astype(np.uint8)
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)
    for k in range(0, 2048, 256):
        d.line([(k // 2, 0), (k // 2, 1024)], fill=(255, 255, 255))
        d.line([(0, 1023 - k // 2), (1024, 1023 - k // 2)], fill=(255, 255, 255))
        d.text((k // 2 + 2, 1010), str(k), fill=(255, 255, 0))
        d.text((2, 1023 - k // 2 - 12), str(k), fill=(255, 255, 0))
    img.save(os.path.join(OUT, "island_%s.png" % name))
    print(name, "max %.1f" % h.max())
