"""python spikes/FB2/verify_all.py [jobs] [key ...] [--full]: kept for old command lines; V1 (2026-10-01) moved it to
buildings/verify_all.py (check cache, at most 4 processes, README rule 2b). jobs above 4 are capped."""
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "buildings"))
import verify_all  # noqa: E402

args = sys.argv[1:]
if args and args[0].isdigit():
    args = ["--jobs", str(min(int(args[0]), 4))] + args[1:]
sys.exit(verify_all.main(args))
