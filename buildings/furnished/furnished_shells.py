"""C3 family recipe: every furnished variant in this folder is buildings/furnishkit.py (a registry shell + fittings +
a buildings/furnish_sets.py dressing) with the parameters of its buildings/registry.py entry. The module IS furnishkit
(its D / EXTRA_OPENINGS / proxies() change with every model() call, so a re-export copy would go stale)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import furnishkit as _fk  # noqa: E402

sys.modules[__name__] = _fk
