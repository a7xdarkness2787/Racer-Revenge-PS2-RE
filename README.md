# Star Wars: Racer Revenge — PS2 Reverse Engineering

Standalone reverse-engineering research for the North American PlayStation 2 release of **Star Wars: Racer Revenge**.

This repository is an evidence-first research archive. It contains independently derived format specifications, executable maps, structure notes, corpus statistics, verification/inspection tools, chronological research records, and plans for runtime validation.

It does **not** contain the original disc image, boot executable, extracted models, textures, audio, movies, or other proprietary retail payloads.

## Canonical target

- boot executable: `SLUS_202.68`
- executable size: `2,972,720` bytes
- executable SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`
- source BIN size: `577,312,512` bytes
- source BIN SHA-256: `208eb5f13f88e9a39eba64cb883d8f0ba523745a48386ec70b96bb073879deb9`
- CUE SHA-256: `7a7ac8c09417c6871963cd4e6f08b7b6fd1dbc39f704a0ab45359aeb96452e5e`
- converted filesystem ISO size: `502,693,888` bytes
- converted ISO SHA-256: `0f12c08fe9c7cbed988e826a40a6b982884668fc9816f085ad71d3312924ad67`
- disc volume: `M11`

See `reference/targets.json` and `reference/disc_identity.md`.

## Current research state

Current documented maturity is approximately **30%** toward a reproducible technical specification of the retail game.

Strongest current results include:

- all **103** retail `.RES` containers structurally reproduced;
- **34,128** embedded resource records and **44,861** compressed chunks validated;
- all **23** pod `.phy` resources parsed and connected to an address-backed pod configuration loader;
- all **26** track `.spl` graphs parsed, covering **4,999** nodes and **5,108** explicit edges;
- all **2,505** embedded `.col` resources parsed across three serialized collision types;
- **222,577** collision BVH nodes structurally verified;
- all **9,917** embedded `.psg` resources pass the recovered fixed-table parser;
- a detailed **881-PSG** POD01/TA/TB render sample now parses end-to-end with no unexplained bytes;
- that render sample contains **890 LOD groups**, **1,216 material/VIF blocks**, **18,965 MSCNT geometry batches**, and **250,514 submitted positions**;
- signed position dequantization, hierarchy object ownership, ordinary triangle-strip topology and material-block ownership are independently reconstructed;
- six POD01 PSG components cross-check against matching type-0 COL bounds to quantization/floating-point precision.

The highest-value renderer frontier is now the VU microprogram/material/GIF/GS path, CableShadow special geometry, and expansion of detailed PSG payload validation beyond the current 881-file sample.

## Repository layout

```text
analysis/         dated technical investigations and deep dives
behavior/         stable gameplay/runtime behavior specifications
commands/         reproducible command recipes and command-session notes
database/         machine-readable questions and research state
executable/       SLUS-specific loader and executable analysis
formats/          independently derived file-format specifications
mapping/          address/cross-reference/correlation notes
raw/              safe text-only generated evidence and verifier output
records/          chronological research records and corrections
reference/        canonical hashes, corpus metadata and target identities
runtime_oracle/   PCSX2/runtime capture and differential-validation design
scripts/          parsers, inspectors, verifiers and mesh reconstruction tools
structures/       runtime field/offset/type maps
symbols/          named executable functions/globals and address ownership
tooling/          analysis environment and tool limitations
traces/           runtime trace schemas, policies and captured metadata
```

## Read first

- `RESEARCH_INDEX.md` — subsystem map to the strongest evidence
- `STATUS.md` — current verified state and maturity
- `CURRENT_WORK.md` — active handoff and immediate queue
- `ROADMAP.md` — long-term research program
- `DEVELOPMENT_LOG.md` — concise chronological research history
- `EXECUTABLE_MAP.md` — current address navigation map
- `database/questions-current.json` — machine-readable open frontier
- `UPDATE_PROTOCOL.md` — mandatory documentation/evidence rules
- `CONTRIBUTING.md` — contribution and provenance standards

## Evidence policy

Use **VERIFIED**, **OBSERVED**, **INFERRED**, **HYPOTHESIS**, **TODO**, **BLOCKED**, and **INVALIDATED** consistently. Failed probes and superseded interpretations remain part of the permanent research record.

Detailed statistics are always scoped explicitly. Full-corpus PSG fixed-table results are not conflated with the current 881-file detailed render-payload sample.

## Proprietary-data rule

Do not commit original retail payloads or reconstructed retail mesh output. Scripts accept user-supplied private fixtures and emit independently derived metadata or private validation output.

See `UPDATE_PROTOCOL.md` for the full research-record standard.
