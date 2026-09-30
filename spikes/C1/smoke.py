"""C1 smoke test: new template variants build, closed convex, C12, faces."""
import os
import sys

DEV = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(DEV, "parts", "kit"))
from jpparts.templates import townhouse  # noqa: E402
from jpparts import mlod, raycheck  # noqa: E402

CASES = {
    "post_det_tile_nuriya": dict(frontage=3, region="tokaido", position="detached", tori="left"),
    "post_det_board_board": dict(frontage=3, region="tokaido", position="detached", tori="right", covering="itabuki",
                                 upper="board", shopfront="_kyo"),
    "post_det_stable": dict(frontage=3, region="tokaido", position="detached", tori="left", geya_ken=2,
                            stable="_umaya", shopfront="_komeya"),
    "post_row_end": dict(frontage=3, region="tokaido", position="end", free="left", tori="left"),
    "inn_std": dict(frontage=5, region="tokaido", position="detached", tori="left", geya_ken=2, split=True),
    "inn_grand": dict(frontage=5, region="tokaido", position="detached", tori="left", geya_ken=2, upper="full", shopfront="_kyo",
                      pent="board"),
}
for k, kw in CASES.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]:
        continue
    H, info = townhouse.build(**kw)
    L = {mlod.lod_name(l.resolution): l for l in H.lods()}
    probs = []
    for w in ("Geometry", "View Geometry", "Fire Geometry"):
        comps = [c for c in L[w].selections if c.startswith("Component")]
        bad = [c for c in comps if mlod.component_report(L[w], c)]
        if bad:
            probs.append("%s: %d bad" % (w, len(bad)))
    pk = raycheck.roof_pokes(H.solids)
    if pk:
        probs.append("C12 %d: %s" % (len(pk), pk[:3]))
    f = [len(L["Resolution %d" % i].faces) for i in (1, 2, 3)]
    print("%-24s %s doors %d %s %s" % (k, f, len(H.doors), townhouse.budget_class(**kw), probs or "OK"))
