# Research Index

This is the fast path into the current Racer Revenge PS2 research.

## Canonical target and project state

- `reference/targets.json` — canonical media/executable identity
- `reference/disc_identity.md` — human-readable disc provenance
- `reference/corpus-summary.json` — machine-readable full-corpus and scoped-sample counts
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

Full-corpus fixed-table evidence:

- `formats/PSG.md`
- `records/2026-10-07-psg-header.md`
- `scripts/psg_inspect.py`
- `executable/surface_geometry_loader.md`

Detailed POD01/TA/TB render-payload evidence:

- `analysis/2026-10-08-psg-mesh-reconstruction.md`
- `records/2026-10-08-psg-render-payload.md`
- `scripts/psg_mesh_extract.py`
- `executable/psx_surface_geometry.md`
- `raw/2026-10-08-psg-render-summary.txt`

The 881-file detailed sample now has closed serialization, decoded position scale/origin, hierarchy object tags, ordinary strip topology, LOD/material grouping and independent PSG/COL bounds validation.

The active renderer frontier is VU/material/GIF/GS behavior, CableShadow special geometry, and expansion of detailed payload validation toward all 9,917 PSG resources.

## Runtime validation

- `runtime_oracle/README.md`
- `traces/README.md`

## Repository methods and policy

- `tooling/analysis-environment.md`
- `commands/README.md`
- `raw/README.md`
- `CONTRIBUTING.md`
