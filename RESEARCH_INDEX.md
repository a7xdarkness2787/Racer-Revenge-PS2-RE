# Research Index

This is the fast path into the current Racer Revenge PS2 research.

## Canonical target and project state

- `reference/targets.json` — canonical media/executable identity
- `reference/disc_identity.md` — human-readable disc provenance
- `reference/corpus-summary.json` — machine-readable corpus counts
- `STATUS.md` — current verified state and maturity
- `CURRENT_WORK.md` — active handoff
- `database/questions-current.json` — open technical frontier
- `DEVELOPMENT_LOG.md` — chronological milestone history
- `UPDATE_PROTOCOL.md` — mandatory evidence/update rules

## Executable navigation

- `EXECUTABLE_MAP.md`
- `executable/SLUS_202.68.md`
- `executable/resource_loader.md`
- `executable/pod_track_loaders.md`
- `executable/collision_loader.md`
- `executable/surface_geometry_loader.md`
- `executable/psx_surface_geometry.md`

## Resource containers

- `formats/RES.md`
- `records/2026-10-07-res-container.md`
- `scripts/res_inspect.py`

## Pod physics

- `formats/PHY.md`
- `records/2026-10-07-pod-track-config.md`
- `scripts/phy_inspect.py`

## Track routing graph

- `formats/SPL.md`
- `records/2026-10-07-pod-track-config.md`
- `scripts/spl_inspect.py`

## Collision

- `formats/COL.md`
- `records/2026-10-07-collision.md`
- `scripts/col_inspect.py`
- `executable/collision_loader.md`

## Surface geometry

Stable full-corpus evidence:

- `formats/PSG.md`
- `analysis/2026-10-08-psg-full-corpus.md`
- `records/2026-10-08-psg-full-corpus.md`
- `raw/2026-10-08-psg-full-corpus-summary.txt`
- `scripts/psg_mesh_extract.py`
- `scripts/psg_corpus_verify.py`
- `reference/ps2-vif.md`
- `executable/psx_surface_geometry.md`

Historical/sample evidence remains under the earlier PSG dated records and analysis notes.

Current state: all 9,917 retail PSG payloads parse end-to-end and reconstruct serialized strip topology without warnings.

The active renderer frontier is hierarchy matrix composition, VU execution, material/texture semantics and GIF/GS output.

## Runtime validation

- `runtime_oracle/README.md`
- `traces/README.md`

## Repository methods and policy

- `tooling/analysis-environment.md`
- `commands/README.md`
- `raw/README.md`
- `CONTRIBUTING.md`
