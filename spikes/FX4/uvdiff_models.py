"""List the distinct models with uvdiff violations (FX3 uvdiff + FX4's stone-aware ATLAS):
  python spikes/FX4/uvdiff_models.py OLD NEW"""
import contextlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FX3 = os.path.join(HERE, "..", "FX3", "uvdiff.py")
ATLAS = re.compile(r"\\jp_m_(wood_weathered|wood_street_dark|wood_kuro|wood_sooted|wood_bengara|wood_new|wood_silver|"
                   r"wood_interior|ceil_boards|floor_boards_int|floor_boards_rough|decal_moss|"
                   r"stone_carved|stone_carved_aged|stone_cut)_w\d_c[oa]\.paa$", re.I)


def main(old, new):
    src = open(FX3, encoding="utf-8").read().replace("bad[:15]", "bad")
    g = {"__name__": "uvd", "__file__": FX3}
    exec(compile(src, FX3, "exec"), g)
    g["ATLAS"] = ATLAS
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        g["main"](old, new)
    lines = buf.getvalue().splitlines()
    print(lines[0])
    print("  models with violations:", sorted({ln.strip().split(" ")[0].rstrip(":") for ln in lines[1:]}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
