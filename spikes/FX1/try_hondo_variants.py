"""FX1: face counts of the town hondo with (a) the side en one bay deep + wakishoji, (b) koran returns only."""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path[:0] = [os.path.join(DEV, "spikes", "W2S"), os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit")]
import try_sacred as TS  # noqa: E402
from jpparts import koran as KR  # noqa: E402
from jpparts.templates import sacred  # noqa: E402

print("(a) side en one bay + wakishoji")
TS.one("hondo", {"grade": "town"})
orig, orig_rooms = KR.en_wrap, sacred.en_rooms


def ret_only(part, W, D, **kw):
    if kw.get("side_len"):
        kw.update(sides=("front",), waki=False, returns=True)
        kw.pop("side_len")
    return orig(part, W, D, **kw)


def rooms(S, W, D, drop, sides, **kw):
    if kw.get("side_len"):
        sides = ("front",)
        kw.pop("side_len")
        kw["returns"] = True
    return orig_rooms(S, W, D, drop, sides, **kw)


KR.en_wrap, sacred.en_rooms = ret_only, rooms
print("(b) koran returns only")
TS.one("hondo", {"grade": "town"})
