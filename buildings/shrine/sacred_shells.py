"""W2S family recipe: every shell in this folder is buildings/sacredkit.py (the shrine + temple template,
parts/kit/jpparts/templates/sacred.py) with the parameters of its buildings/registry.py entry."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sacredkit import model, POSTS, PASSAGES, PORTALS, STAIRS, INFO, FRAME_NOTE, PASSAGE_LABEL  # noqa: E402,F401
