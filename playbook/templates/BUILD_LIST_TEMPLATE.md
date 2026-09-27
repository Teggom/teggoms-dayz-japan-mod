# BUILD LIST: <category>, v<N>

<!--
The research agent (A) writes this for the builder (B, C, D or S).
- One entry per part or asset.
- The machine-readable twin is build_lists/<category>.json. It must validate against
  playbook/templates/build_list_schema.json.
- The markdown and the JSON must say the same thing; the JSON is the one the builders' scripts read.

Stephen approves it at gate G1. Nothing on it is built before that.

Keep it short: one table row per entry, plus a reference strip image per entry in refs/.
-->

**Stage:** B | C | D | S | R | W | F

**Author and date:**

**Scope:** <what is in, what is out, and why>

**Reference strip:** `build_lists/<category>_refs.png`. Each entry gets a row of 2–4 thumbnails, labelled with the
ref IDs.

## Entries

| # | ID (file stem) | Name (English / romaji) | What and where | Importance | Tier | Pri | Period evidence (ref IDs) | Key dimensions (source or `assumed`) | Materials (library → palette ID) | Connectors | Variants (ID: how it differs) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `jp_p_roof_sangawara_field` | Sangawara field tiles | Tier 2–3 town roofs | standard | 2, 3 | P1 | [T07] 1674, [c08] | working width 0.260 m (reason: ken ÷ 7); exposure 0.235 (assumed) | `jp_m_roof_kawara_ibushi` → kawara_ibushi | eave, ridge, verge | `_w1` normal, `_w2` weathered |
| 2 | | | | | | | | | | | |

## Notes per entry (only where the table isn't enough)

**1. <ID>**
- **Must show:** <the look that matters, e.g. "corrugation visible at the eave line and in silhouette">
- **Banned tells to watch:** <from PLAYBOOK §7>
- **Deviations used:** <D#, and why>
- **Open questions:** <anything the builder must not guess>

## Requested new materials or palette entries

| Material | Why | Sample source | Palette ID (new or existing) |
|---|---|---|---|
| | | | |

## Checks the builder must run

- C1–C9 as applicable (PLAYBOOK §12).
- List anything special, e.g. "C8: roof vertex density".
