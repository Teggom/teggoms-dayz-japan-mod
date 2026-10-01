"""FP1: sample the aged shikkui (jp_m_wall_shikkui_aged) from the local references with M1's sampler
(spikes/M1/sample.py: mid 70 % luminance median per box, mean of the boxes). Writes look/aged_boxes.jpg."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(DEV, "spikes", "M1"))
import sample as S  # noqa: E402

BOXES = [
    # c25 (a tile-and-plaster wall, Tokyo, decades unpainted): sunlit lime plaster between the tile courses, greyed and
    # stained by rain; three clean patches beside the plaques (fine grid in spikes/FP1/look/c25_zoom.jpg)
    ("c25_tsuijibei", [0.755, 0.39, 0.80, 0.44], None),
    ("c25_tsuijibei", [0.67, 0.18, 0.71, 0.21], None),
    ("c25_tsuijibei", [0.61, 0.50, 0.66, 0.54], None),
    # c03 Tsumago (an old, maintained post-town wall in sun): the cleaner end of 'aged', so the value stays plaster-white
    ("c03_tsumago_street", [0.79, 0.33, 0.86, 0.45], None),
]

if __name__ == "__main__":
    srgb, spread, meds, crops, notes = S.sample(BOXES)
    print("aged shikkui", srgb, "spread dE75 %.1f" % spread, "per box", meds)
