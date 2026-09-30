"""C1 family recipe: every shell in this folder is buildings/shellkit.py (the townhouse template) with the
parameters of its buildings/registry.py entry."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shellkit import model, POSTS, PASSAGES, STAIRS, INFO, FRAME_NOTE  # noqa: E402,F401
