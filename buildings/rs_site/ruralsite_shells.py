"""W3C2 family recipe: every shell in this folder is buildings/ruralsitekit.py (the rural-site template,
parts/kit/jpparts/templates/ruralsite.py) with the parameters of its buildings/registry.py entry."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ruralsitekit import model, POSTS, PASSAGES, PORTALS, STAIRS, INFO, FRAME_NOTE, PASSAGE_LABEL  # noqa: E402,F401
