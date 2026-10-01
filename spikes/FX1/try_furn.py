"""FX1 quick look at a furnished variant in memory (no files written): its site objects and hung props.
  python spikes/FX1/try_furn.py <registry key> [...]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(DEV, "buildings"), os.path.join(DEV, "parts", "kit"), os.path.join(DEV, "spikes", "B_building", "kit")):
    sys.path.insert(0, p)
import registry  # noqa: E402
import furnishkit  # noqa: E402


_orig = furnishkit.Ctx.__init__


def _init(self, *a, **k):
    _orig(self, *a, **k)
    furnishkit._LAST_CTX = self


furnishkit.Ctx.__init__ = _init


def main():
    for key in sys.argv[1:]:
        b = registry.get(key)
        kw = {k: v for k, v in b.get("params", {}).items()}
        M, floors, rooms = furnishkit.model(name=b.get("recipe_name") or b["name"], **kw)
        print(key)
        for it in furnishkit.D.site:
            print("  site %-28s x %.3f z %.3f yaw %.0f  %s" % (it["name"], it["x"], it["z"], it["yaw"], it.get("why", "")))
        ex = furnishkit._LAST_CTX.extra
        for h in ex.get("fx1_hangs", []):
            print("  fx1 hang %-24s on %s" % (h["prop"], h["members"]))
        for b_ in ex.get("fx1_bars", []):
            print("  fx1 bar  %s" % b_)
        for it in furnishkit.D.items:
            if it.get("mounted") == "beam":
                print("  hang %-28s x %.3f y %.3f z %.3f yaw %.0f" % (it["name"], it["x"], it["y"], it["z"], it["yaw"]))


if __name__ == "__main__":
    main()
