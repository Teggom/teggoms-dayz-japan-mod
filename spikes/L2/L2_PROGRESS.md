# L2 progress: the outdoor life layer (research/interior/LIFE_LAYER.md, items 51-74) + the B3b text check

Agent L2 (opus-high), 2026-09-30. Time log: `japan_dev/TIMELOG_L2.md` (logger `spikes/L2/tlog.py`).

## Step 0: text mirroring — DONE (verdict: B3b's text was mirrored AND back-facing; L1's was back-facing)
- **Evidence.** `spikes/L2/textface.py` (the TXT check, reads the written MLOD): for every text-atlas face, outward =
  minus the stored normal; FACE = a host surface lies behind it (ray along -outward within 5 cm); READ = the texture
  +u runs to the viewer's right, right = cross(up, -outward) (left-handed: up +y, looking +z -> right +x = east).
  Before: B3b 37 of 37 text models FAIL FACE (read OK only from INSIDE the board = mirrored from outside), L1 23 of
  23 FAIL FACE (u already mirrored by lkit.text, but facing in). Renders with back faces culled, as the game draws
  single-sided faces: `research/outdoor_kit/contact_sheets/l2_textcheck_before.jpg` (the text is gone) and
  `..._after.jpg` (御酒, 御菓子所, 庚申供養塔, 用水 read correctly). An earlier unculled render of the old masters showed
  御酒 on the chochin mirrored.
- **Cause.** `skit.decal()` takes its normal from newell(tl, tr, br, bl), which for right x up = +z gives -z: the
  quad faces into its host. `text_on()` lays u along `right`, which a viewer outside sees as his left.
- **Fix (no class names changed).** `skit.face_text(solids, mirror_u)` flips every text-atlas solid's faces and
  (optionally) mirrors u inside the solid's own cell range; `skit.text_ok()` = text_on already fixed (for new code).
  B3b's `build.py` calls `face_text(mirror_u=True)` on every model after building; L1's `build_l1.py` calls it with
  `mirror_u=False`. B3b's chochin text strip lifted 4 -> 9 mm (it came within 0.02 mm of the paper: z-fight).
- **Rebuilt:** B3b all 129 (37 MLOD masters changed = exactly the text models; 92 byte-identical), jp_site.pbo
  repacked; L1 ofuda, koyomi, chochin, fire_gear, taru, choba_set, yoroibitsu, 185/185 binarized, jp_furniture.pbo
  repacked; machiya_t3_01_shop through `buildings/pipeline.py` (137/137, --no-pack and packed), jp_buildings.pbo.
- **Re-runs:** B3b 129/129; L1 185/185; TXT 60/60 text models pass (B3b 37 + L1 23); B3a/B4 prop checks 112/112,
  faces unchanged (`spikes/L2/check_b3a.py`); townhouse combos 60/60, 0 over budget (`spikes/L2/_combos.log`).

## Next
- Era checks (#53, #58, #59 + doubts) -> research/interior/LIFE_LAYER_ERA.md
- Build the 24 items (build_l2.py into B3b's pipeline), sidecars with mounts, decor registration, pack, sheets.

## How to resume
- `python spikes/L2/textface.py <p3d or folder>`; `python spikes/L2/textcheck.py <tag>`
