"""FX4 check: spikes/FX3/uvdiff.py with the stone atlases added: only atlas wood / moss / stone uv may move.
Models whose geometry FX4 changed (bells, gong, tower, lids, hat, tassel collars) are reported as face-count changes.

  python spikes/FX4/uvdiff.py OLD_DIR NEW_DIR
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "FX3"))
import uvdiff as U  # noqa: E402

U.ATLAS = re.compile(r"\\jp_m_(wood_weathered|wood_street_dark|wood_kuro|wood_sooted|wood_bengara|wood_new|wood_silver|"
                     r"wood_interior|ceil_boards|floor_boards_int|floor_boards_rough|decal_moss|"
                     r"stone_carved|stone_carved_aged|stone_cut)_w\d_c[oa]\.paa$", re.I)

if __name__ == "__main__":
    sys.exit(U.main(sys.argv[1], sys.argv[2]))
