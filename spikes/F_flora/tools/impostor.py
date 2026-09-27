"""impostor.py - compose the three orthographic renders of a tree into its LOD4 atlas (<model>_lod4_ca.png)
and convert it to PAA. Layout matches build_impostor() in sakura.py / bamboo.py:
    top-left = top view, bottom-left = front view (along +Z), bottom-right = left view (along +X)."""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import WORK_TEX, src_dir, to_paa  # noqa: E402
from textures import bleed  # noqa: E402


def compose(model, p_rel, size=1024):
    half = size // 2
    atlas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for view, (x, y) in (("top", (0, 0)), ("front", (0, half)), ("left", (half, half))):
        im = Image.open(os.path.join(WORK_TEX, "%s_imp_%s.png" % (model, view))).convert("RGBA")
        if im.size != (half, half):
            im = im.resize((half, half), Image.LANCZOS)
        # colour first (bleed with the true alpha), so the thickened edge below is not black
        arr = bleed(np.asarray(im).copy()).astype(np.float64)
        # far away, alpha-tested thin twigs vanish in the mips: thicken the silhouette a little
        a = Image.fromarray(arr[..., 3].astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
        a = np.asarray(a).astype(np.float64)
        rgb = arr[..., :3]
        if view != "top":
            # a touch of vertical shading (crowns are darker underneath) - the engine lights the flat card
            ramp = np.linspace(1.0, 0.8, half)[:, None, None]
            rgb = rgb * ramp
        out = np.dstack([rgb, a]).clip(0, 255).astype(np.uint8)
        atlas.paste(Image.fromarray(out, "RGBA"), (x, y))
    arr = bleed(np.asarray(atlas).copy())
    img = Image.fromarray(arr, "RGBA")
    png = os.path.join(WORK_TEX, model + "_lod4_ca.png")
    img.save(png)
    paa = os.path.join(src_dir(p_rel), "data", model + "_lod4_ca.paa")
    to_paa(png, paa)
    print("  impostor %s -> %s (%d bytes)" % (model, paa, os.path.getsize(paa)))
    return png


if __name__ == "__main__":
    compose(sys.argv[1], sys.argv[2])
