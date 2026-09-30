#!/usr/bin/env python3
r"""build.py - Land_JP_Machiya_T3_01 through the multi-building pipeline (B0, 2026-09-29).

  python build.py [--no-binarize] [--no-pack] [--no-verify]

Same as `python buildings/pipeline.py machiya_t3_01 ...`. The one-building build that lived here (it rewrote
config.cpp, C.csv and the CE files with this building alone) is now buildings/pipeline.py + buildings/registry.py:
this building's class, doors, loot and placement are one registry entry + record.json, and the shared outputs are
regenerated from every shipped building. Never touches the server, the game or any GUI program.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pipeline  # noqa: E402

if __name__ == "__main__":
    sys.exit(pipeline.main(["machiya_t3_01"] + sys.argv[1:]))
