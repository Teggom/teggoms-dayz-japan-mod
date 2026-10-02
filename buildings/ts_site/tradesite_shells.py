"""W3C1 family recipe: every shell in this folder is buildings/tradesitekit.py (the trade-site template,
parts/kit/jpparts/templates/tradesite.py) with the parameters of its buildings/registry.py entry."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from tradesitekit import model, POSTS, PASSAGES, PORTALS, STAIRS, INFO, FRAME_NOTE, PASSAGE_LABEL  # noqa: E402,F401
