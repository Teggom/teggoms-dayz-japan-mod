# DOSSIER: <Class or asset id>, <era, e.g. c.1730>

<!--
Template: the katana v2 research process (spikes/A_arms/katana_v2/DOSSIER.md), generalised to any asset.

How deep to go (PLAYBOOK §11):
- Hero: fill every section.
- Standard: sections 0-3, 5, 7-9, plus a short 4.
- Filler: don't use a dossier. Put a build-list entry with one reference check instead.

Put the dossier in the agent's working folder:
- spikes/<X>/<asset>/DOSSIER.md
- next to it: spec.json, which must validate against playbook/templates/spec_schema.json
- next to it: refs_index.json

Images go in data/<X>/refs/ only. They are never shipped.
-->

**Importance:** hero | standard

**Tier(s):** 1 | 2 | 3

**Region:** Kamigata | Edo | rural | all

**Status:** researched | built | verified offline | seen in game

**Verification:** <N of M checklist items pass>, from `checklist.json`

<One paragraph: what the thing is, the single primary reference it is built on, and why that reference.>

## 0. Method

1. **Research.** Use open sources only (PLAYBOOK download limits). Prefer dated museum objects and surviving
   period buildings. Prints and later rebuilds only support proportion and colour.
2. **Record every choice**, with its source, in `spec.json`. Mark anything no source gives as `assumed`, with a
   reason.
3. **Draw the blueprint from the spec by script.** Output: `<asset>_spec_drawing.png`.
4. **Build.** The generator reads only `spec.json`. Materials are library paths (PLAYBOOK §9). Colours are palette
   IDs (§8).
5. **Verify** with checks C1–C9 (PLAYBOOK §12):
   - measure our renders with the same code used on the reference photos
   - read the dimensions back from the binarized ODOL
   - make the compare sheet

## 1. Sources

**Images** (N, all in `refs_index.json`; local only):
- <id>: <museum or site, object number, date>, <licence>. **Primary for <what>.**

**Text** (N, with URLs in `refs_index.json`):
- <id>: <title>, which supports <what>.

**Period check.**
- The earliest and latest attested dates for this form: <…>.
- Is it inside 1680–1750? <yes / no, and why that is acceptable>

## 2. Form and dimensions

| Feature | Finding for the era | Source | Value chosen |
|---|---|---|---|
| <overall size> | <range across the sources> | <ids> | **<value + unit>** |
| <on the ken grid?> | | | **<n ken / half-ken>** |

## 3. Construction and details

| Part | Finding | Source | Choice (library part or material path) |
|---|---|---|---|
| | | | |

## 4. Colours (measured)

| Surface | sRGB | Palette ID and ΔE76 | Where measured |
|---|---|---|---|
| | | | |

Note any sample you dropped because of neighbour contamination, lighting or colour cast.

## 5. Engine frame and constraints (kept, not researched)

- **Class and parent:**
- **Origin and axes:**
  - `autocenter=0`
  - origin at <base centre / left post centreline, floor level>
  - front along <axis>
- **LOD set:** as the vanilla class. Budgets: PLAYBOOK §12.
- **Gameplay deviations used:** D1–D10, each with a reason.
- **Doors, roadway, loot, memory points, proxies:**

## 6. Tier and variant plan

| Variant | Tier | What changes (materials, parts, furnishing) | Shared with |
|---|---|---|---|
| | | | |

## 7. Verification

- **ODOL read-back against the spec:**
- **Renders against the photos (the same measuring code):**
- **Checks C1–C9:** <pass/fail per check, with a link to `checks.json`>
- **Compare sheet:** `<asset>_compare_sheet.png`

## 8. Unresolved

- Not yet seen in game.
- <N of M> spec entries are assumed.
- <Conflicts between sources, and which one you followed.>

## 9. Lessons for future models

- <Anything the next agent should reuse or avoid. The lead may copy these into the playbook.>

## 10. Files

- **In `spikes/<X>/<asset>/`:**
  - `spec.json`
  - `refs_index.json`
  - `ref_measurements.json`
  - `<asset>_spec_drawing.png`
  - `compare_sheet.png`
  - `checks.json`
  - `checklist.json`
- **Tools:** <scripts, and what each one does>
- **Game data:** <p3d, paa, rvmat, config>

## In-game check

- <Where to stand, what to do, and what "pass" looks like. One line each.>
