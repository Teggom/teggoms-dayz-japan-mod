# W3B progress: wave 3b everyday workshops + services (agent W3B, 2026-10-02)

Time log `japan_dev/TIMELOG_W3B.md` (logger `python spikes/W3B/tlog.py "<event>" "<name>" "<tag>" <5h> <wk>`).
Research notes: `spikes/W3B/W3B_NOTES.md`. Stop rule: weekly usage 88 % -> checkpoint, commit + push, resume note here.

## Status
- [x] notes
- [x] shells: 18 (template parts/kit/jpparts/templates/trade.py, recipe buildings/tradekit.py, families buildings/tr_*,
  registry W3B_SHELLS), 813 checks pass; sheet research/production/contact_sheets/w3b_family.jpg
- [x] props: 34 props / 63 models (spikes/W3B/props_w3b.py, `python spikes/W3B/build_w3b.py [--pack]` -> jp_furniture
  fragment W3B, cat tradefit), all pass; jp_furniture 585 classes (NOT packed yet)
- [ ] furnished (buildings/w3b_sets.py)
- [ ] placement (spikes/W3B/layout_w3b.py) + world + mission
- [ ] checks, sheets, checklist, pushed

## How to resume
- Shells: `cd buildings && python pipeline.py <tr_key...> --no-pack --jobs 4` (logs data/C/_build/verify_logs).
- Props: `python spikes/W3B/build_w3b.py [prop ...] [--no-binarize] [--pack]`; previews `python spikes/W3B/render_w3b_props.py`.
- Quick try: `cd spikes/W3B && python try_tr.py sento '{}'`.
