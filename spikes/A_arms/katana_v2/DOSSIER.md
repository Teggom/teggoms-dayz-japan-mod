# DOSSIER: JP_Katana, c.1600

This is the template for every future model's research step. The agent returned it as text; the lead saved it on
2026-09-27. **Verification: all 35 checklist items pass** (`checklist.json`).

It is a Keichō-shintō katana. The dimension reference is a c.1603 Horikawa Kunihiro Jūyō blade (tsuruginoya F00247),
in a Tenshō-style mount.

## 0. Method

1. **Research** with open sources only.
2. **Record every choice**, with its source, in `katana_spec.json` (101 entries; 44 small details marked `assumed`).
3. **Draw the blueprint** from the spec by script (`draw_spec.py`, giving `katana_spec_drawing.png`).
4. **Build**: the generator reads only the spec (`tools/katana_geom.py`), and the mesh, textures and drawing all use
   it.
5. **Verify** in three ways:
   - measure our renders with the same code used on the museum photos (`measure_refs.py`, `compare.py`)
   - read dimensions back from the binarized ODOL
   - outline the mesh over the drawing (kissaki IoU 0.999)

## 1. Sources

**Images** (34, all logged in `refs_index.json`, local only in `data/A/refs`):
- Met Open Access, CC0:
  - 27600: Takahiro, dated 1622. Whole blade and kissaki. **Primary blade photos.**
  - 27601: Munetsugu, 17th c. Whole blade and kissaki.
  - 30091 / 30092: iron tsuba, late 16th–early 17th c.
- TNM F-19992, uchigatana koshirae, late 16th / early 17th c. (ColBase CC BY 4.0 via Commons). **Primary mount photo.**
- Commons context and appearance images (PD / CC0 / CC BY): the boshi photo, kissaki-types diagram, modern tsuka,
  Hōryū-ji koshirae, Walters blades, Auckland katana.

**Text** (16, with URLs in `refs_index.json`):
- The tsuruginoya F00247 listing: Kunihiro c.1603, full measurements and mount.
- Four Aoi Art listings of Keichō-era blades.
- Met records 27600, 27601 and 23983.
- The TNM e-Kokuhō record for F-19992.
- Markus Sesko (Keichō-shintō sugata).
- nihonto.com: a Tenshō Jūyō koshirae, and its uchigatana koshirae article.
- Cottontail Customs (menuki placement).
- NCJSC and Glossaria (how the measurements are defined).

## 2. Blade

| Feature | c.1600 finding | Source | Value chosen |
|---|---|---|---|
| Nagasa | Keichō blades 65–75 cm (Sesko: 70–75 for Momoyama smiths) | F00247 70.2; Tadayoshi 1615 75.15; Kanetoki 70.14; Kunihiro 1610 / 1611 69.7 / 68.1; Met 27600 71.5 | **70.2 cm** (chord from munemachi to point) |
| Sori | Shallow | F00247 1.6; Tadayoshi 1.5; Met 27600 1.5; Tadakuni 1.4 | **1.6 cm** |
| Sori position | Torii-zori; deepest at 0.507 of the length, measured on the Met 27600 photo | Met 27600 photo | Circular arc, peak at 0.50 |
| Motohaba / sakihaba | Wide, with little taper | F00247 3.05 / 2.5; cross-checks 3.08–3.11 / 2.09–2.36 | **3.05 / 2.50**, linear taper (assumed) |
| Kasane | Measured at the mune | F00247 0.75 / 0.55 | **0.75 / 0.55**; shinogi 1.15× thicker (assumed) |
| Section | Shinogi-zukuri, wide shinogi-ji, shinogi somewhat high | F00247 | Shinogi at 0.36 of the width from the mune (bounded by the photos) |
| Mune | Mitsu-mune | F00247, Sesko | Mitsu-mune; facet sizes assumed |
| Niku | Low | Sesko | Low (5 %, assumed) |
| Hi | None | F00247, Met photos | None |
| Funbari | Slight | F00247 | Not modelled (under the habaki) |

## 3. Kissaki

| Feature | c.1600 finding | Source | Value chosen |
|---|---|---|---|
| Size | Extended chū-kissaki | F00247, Sesko | **4.5 cm = 1.8 × sakihaba**; measured 1.68 and 1.81 on the Met photos |
| Fukura | Convex edge curve rising to the point | Profile measured on both Met close-ups (`ref_measurements.json`) | Their average, a 21-point profile |
| Point | Lies on the straight mune line | Both Met photos | Yes |
| Yokote | Straight, square to the mune | Met photos | Crease (duplicated ring) plus a texture line |
| Ko-shinogi | Curves into the point | Measured from 0.4 to 1.0 of the kissaki | Measured profile |
| Thickness inside the kissaki | Thins to the point | None | Assumed |

## 4. Hamon

| Feature | c.1600 finding | Source | Value chosen |
|---|---|---|---|
| Hamon | Low, shallow notare with ko-gunome, pointed elements, small ashi, nie | F00247 | Style sourced; numeric wave sizes assumed |
| Boshi | Sugu, komaru, very shallow kaeri | F00247 | Band within the hamon depth of the fukura; kaeri 0.1 × kissaki length |

## 5. Colours (RGB, measured)

| Surface | Value | Where measured |
|---|---|---|
| Hamon | 203, 214, 228 | Met 27600 / 27601 |
| Ji | 94, 108, 126 | Met 27600 / 27601 |
| Shinogi-ji | 60, 70, 74 | Met 27600 |
| Wrap | 184, 167, 129 | TNM F-19992 |
| Same | 63, 63, 60 | TNM F-19992 |
| Iron | 76, 72, 69 | Met 30091 / 30092 and TNM F-19992 |

The first iron sample (101, 69, 67) was tinted by the red saya behind the tsuba, so it was dropped.

## 6. Mounts

| Part | c.1600 finding | Source | Value chosen |
|---|---|---|---|
| Habaki | Gold-foiled copper, single | Tadayoshi 1615 listing | 3.3 cm (length assumed) |
| Seppa | Copper pair | None | 0.15 cm each (assumed) |
| Tsuba | Round iron, hammered, square rim with slight rounding, no hitsu-ana | F00247, Tenshō Jūyō koshirae, Met 30091 / 30092, TNM F-19992 | **8.0 × 0.5 cm** (8.0 from F00247; range 6.7–9.2) |
| Fuchi | Shakudō, low, angled sides | F00247, nihonto.com | 1.3 cm tall (assumed) |
| Kashira | Black lacquered horn, wrap passes over the top | Tenshō koshirae | 1.2 cm (assumed) |
| Tsuka | Waisted (ryūgo), slightly curved | Tenshō | **24.5 cm** (F00247; range 20.1–26.1), depth 3.2 (TNM), tsuka sori 0.2 cm; width and waist assumed |
| Same | Black lacquered, the norm up to Momoyama | TNM photo, nihonto.com | Black lacquered (F00247's is red) |
| Wrap | Leather hineri-maki | F00247, Tenshō, TNM | Buff, pitch 1.26 cm (TNM), 17 windows |
| Menuki | Crawling dragon, shakudō with gold | F00247 | Omote at the 3rd window from the fuchi, ura at the 3rd from the kashira (Cottontail) |
| Mekugi | One | Kanetoki listing | 6.4 cm below the machi (measured on the Met 27600 nakago) |

## 7. Engine frame (kept)

- Vanilla Sword IK frame; the tsuba stack ends at y 0.125.
- Edge on +Z (A's REPORT decision 4; nothing found in the IK contradicts it).
- Same LODs, 1.2 kg, same memory points.

## 8. Verification

- **Shipped ODOL:** read back, it matches the spec exactly (70.2 / 1.6 / 3.05 / 2.5 / 4.5 / 0.75, tsuba 8.0), and the
  point sits exactly on the mune line.
- **Against the photos:** our render's kissaki is 1.79 × sakihaba (Met 1.68 / 1.81). The fukura is within 0.013 of the
  Met profiles. Mesh vs spec outline IoU is 0.999.
- **Grip:** `grip_proof` gives 11.9 / 17.0 mm, as before.
- **Build:** binarize clean, CfgConvert OK, PBO packed.
- **Byte identity:** yari, yumi, ya and the shared files are identical (28 source files, 22 PBO entries).

## 9. Unresolved

- Not yet seen in game.
- 44 of the 101 spec entries are small details marked assumed.
- Tsuka (24.5 cm) and tsuba (8.0 cm) follow the Kunihiro mount; the TNM mount has 20.1 and 6.7.
- The old `jp_tsuka_co.paa` is unused but still in the PBO.

## 10. Lessons for future models

- **Met API:** it blocks bursts; fetch about one object every 3 s, and don't combine the department and date filters.
  The image host `images.metmuseum.org` is fine.
- **Commons API:** send a descriptive User-Agent and honour `retry-after` on a 429.
- **Match orientation to the photos:** blade photos stand the chord or the kissaki upright, while our renders hold the
  tsuka upright. Rotate before comparing or measuring; ignoring this skewed the kissaki ratio from 1.8 to 1.63.
- **Black backgrounds:** a dark shinogi-ji disappears against a black photo background, so the photo widths read low.
  Take dimensions from text sources; use photos for shape.
- **Colour samples pick up neighbours:** check what surrounds the sampled pixels.
- **Kasane is taken at the mune,** not at the shinogi.
- **Measure our own render with the photo code,** then check dimensions exactly from the ODOL. On the render the habaki
  biases the measured sori to 1.75; the ODOL gives exactly 1.6.

## 11. Files

**New, in `spikes/A_arms/katana_v2/`:**
- `katana_spec.json`, `refs_index.json`
- `ref_measurements.json` + `measure_refs.py` (with `measure/` for the annotated measurement images)
- `katana_spec_drawing.png` + `draw_spec.py`
- `compare_sheet.png`, `katana_spec_overlay.png`, `compare_metrics.json` + `compare.py`
- `checklist.json` + `make_checklist.py`
- `hashes_before_src.txt`, `hashes_after_src.txt`, `pbo_hashes_before.txt`, `pbo_hashes_after.txt`
- `renders/` and `renders_alpha/`

**Tools, in `spikes/A_arms/tools/`:**
- New: `katana_geom.py`, `katana_textures.py`
- Edited:
  - `models.py` (katana section only)
  - `build.py` (`--only`; katana mass and LODs read from the spec)
  - `meshkit.py` (per-ring UVs, backward compatible)
  - `render_blender.py` (katana views, `--alpha`)

**Game data:**
- `src/JP/weapons/katana/jp_katana.p3d`
- `src/JP/weapons/data/jp_katana_{blade,tsuka,fittings}_co.{paa,png}`
- `@Japan/addons/jp_weapons.pbo`

**Also updated:** `spikes/A_arms/CREDITS.md`, and `spikes/A_arms/renders/jp_katana_{side,edge,three_quarter,hilt}.png`.
The reference images are local only, in `data/A/refs/`.

## In-game check

- Take `JP_Katana` in hands. **Pass:** a pointed curved tip with a visible yokote, a buff wrap with black diamonds, a
  dark round tsuba and a gold habaki.
- Check the hands. **Pass:** they sit on the tsuka as before.
