# Star Wars: Racer Revenge — PS2 Reverse Engineering

Standalone reverse-engineering research for the North American PlayStation 2 release of **Star Wars: Racer Revenge**.

This repository is an evidence-first research archive containing independently derived format specifications, executable maps, structure notes, corpus statistics, verification tools, chronological research records, and runtime-validation plans.

It does **not** contain the original disc image, boot executable, extracted models, textures, audio, movies, or other proprietary retail payloads.

## Canonical target

- boot executable: `SLUS_202.68`
- executable size: `2,972,720` bytes
- executable SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`
- source BIN SHA-256: `208eb5f13f88e9a39eba64cb883d8f0ba523745a48386ec70b96bb073879deb9`
- converted filesystem ISO SHA-256: `0f12c08fe9c7cbed988e826a40a6b982884668fc9816f085ad71d3312924ad67`
- disc volume: `M11`

See `reference/targets.json` and `reference/disc_identity.md`.

## Current research state

Current documented maturity is approximately **34%** toward a reproducible technical specification of the retail game.

Strongest current results:

- all **103** retail RES containers structurally reproduced;
- **34,128** embedded resource records and **44,861** compressed chunks validated;
- all **23** pod PHY resources parsed and connected to executable-side configuration code;
- all **26** SPL track graphs parsed, covering **4,999** nodes and **5,108** explicit edges;
- all **2,505** COL resources parsed across three serialized collision types;
- **222,577** collision BVH nodes structurally verified;
- all **9,917** PSG resources now pass the complete render-payload parser;
- PSG totals include **22,175 material blocks**, **366,935 VIF geometry batches**, **4,869,177 submitted positions**, and **3,124,861 reconstructed strip triangles**;
- PSG position scaling, hierarchy transform tags, LOD organization, material ownership and VIF attribute serialization are reproducible.

The active renderer frontier is hierarchy-matrix assembly, the VU microprogram, material/texture semantics and GIF/GS output.

## Repository layout

```text
analysis/         dated technical investigations and deep dives
behavior/         stable gameplay/runtime behavior specifications
commands/         reproducible command recipes and session notes
database/         machine-readable questions and research state
executable/       SLUS-specific loader and executable analysis
formats/          independently derived file-format specifications
mapping/          address/cross-reference/correlation notes
raw/              safe text-only generated evidence and verifier output
records/          chronological research records and corrections
reference/        canonical hashes, corpus metadata and public format references
runtime_oracle/   PCSX2/runtime capture and differential-validation design
scripts/          parsers, inspectors, verifiers and reconstruction tools
structures/       runtime field/offset/type maps
symbols/          named executable functions/globals and address ownership
tooling/          analysis environment and tool limitations
traces/           runtime trace schemas, policies and captured metadata
```

## Read first

- `RESEARCH_INDEX.md`
- `STATUS.md`
- `CURRENT_WORK.md`
- `ROADMAP.md`
- `DEVELOPMENT_LOG.md`
- `EXECUTABLE_MAP.md`
- `database/questions-current.json`
- `UPDATE_PROTOCOL.md`
- `CONTRIBUTING.md`

## Evidence policy

Use **VERIFIED**, **OBSERVED**, **INFERRED**, **HYPOTHESIS**, **TODO**, **BLOCKED**, and **INVALIDATED** consistently.

Failed probes and superseded interpretations remain part of the permanent research record.

## Proprietary-data rule

Do not commit original retail payloads or reconstructed retail assets. Tools operate on user-supplied private fixtures and retain only independently derived metadata/specifications in Git.
