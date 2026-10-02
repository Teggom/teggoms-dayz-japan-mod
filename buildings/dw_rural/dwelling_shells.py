"""D3 family recipe: every shell in this folder is buildings/dwellingkit.py (the dwelling template,
parts/kit/jpparts/templates/dwelling.py) with the parameters of its buildings/registry.py entry."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from dwellingkit import model, POSTS, PASSAGES, PORTALS, STAIRS, INFO, FRAME_NOTE, PASSAGE_LABEL  # noqa: E402,F401
