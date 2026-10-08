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

## Surface geometry and PS2 render payload

Stable fixed-table entry points:

- `formats/PSG.md`
- `records/2026-10-07-psg-header.md`
- `scripts/psg_inspect.py`
- `executable/surface_geometry_loader.md`

Current payload frontier:

- `analysis/2026-10-07-psg-vif-payload.md`
- `executable/psx_surface_geometry.md`
- `scripts/psg_vif_inspect.py`
- `raw/2026-10-07-psg-vif-summary.txt`

The first VIF block is verified in an 881-file canonical POD01/TA/TB sample. Later multi-block structures, material ownership and VU/GIF/GS semantics remain active work.

## Runtime validation

- `runtime_oracle/README.md`
- `traces/README.md`

## Repository methods and policy

- `tooling/analysis-environment.md`
- `commands/README.md`
- `raw/README.md`
- `CONTRIBUTING.md`
