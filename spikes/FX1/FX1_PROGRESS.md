# FX1 progress: wave-2 geometry + placement fixes from Stephen's walk (agent FX1, 2026-10-01)

Brief: fixes 1-6 from test/feedback/2026-10-01_wave2/NOTES.md (door handles, offering box, hanging things, U1 veranda,
rope torii head room, woodpile support). Time log `japan_dev/TIMELOG_FX1.md` (logger
`python spikes/FX1/tlog.py "<event>" FX1 "<tag>" <5h> <wk>`).

## Tools (spikes/FX1)
- `probe_front.py <mlod> [zmin]`: Roadway faces in front of a hall (en + kizahashi extents).
- `probe_geo.py <mlod> x0 x1 z0 z1 [y0 y1] [lod]`: Geometry components (bbox) inside a model-frame box.
- `hangcheck.py [mlod ...]`: every hung prop (mount beam) in the wave-2 furnished MLODs: its attachment points
  (top vertices) must meet a building face within 3 cm straight above. Before FX1: 16 failing.

## Status
- [ ] 1 handles  - [ ] 2 offering box + litter  - [ ] 3 hanging things  - [ ] 4 U1 veranda  - [ ] 5 torii head room
- [ ] 6 woodpile support  - [ ] rebuild + pack  - [ ] world + mission  - [ ] checks  - [ ] sheet  - [ ] checklist
- [ ] pushed

## Findings / causes
1. tobira.py ring pull: `rx = free - side * 0.12` put each leaf's pull 0.12 m PAST its free edge, i.e. on the other
   leaf, while it stayed in its own leaf's bone/selection: closed it sat on the wrong leaf, open it swung with its
   own leaf and floated in the air. gates.py: the right leaf's hinge straps sat at its FREE edge (`xh = x0 if
   astragal >= 0`: the right leaf has astragal 0). Kura plaster leaves: no handles; hinge pins static at the axis (ok).
