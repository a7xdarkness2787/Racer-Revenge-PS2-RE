# Current work

## Active target

`SLUS_202.68` — North American retail PS2 executable.

## Immediate goals

1. Establish ELF layout, entry point, load addresses, sections, and symbol-table state.
2. Recover a first-pass function map from strings, cross-references, RTTI-like names, assertions, and source-file diagnostics.
3. Identify resource-loading entry points for `.RES`, `.PST`, `.CAM`, and related data.
4. Trace pod and track loading from filename construction to parsed runtime structures.
5. Build subsystem maps for race logic, physics, collision, camera, audio, rendering, and UI.
6. Add PCSX2 runtime experiments once static addresses are stable.

## High-value executable evidence already observed

The executable retains numerous class names, source filenames, assertions, parameter labels, and format strings. Examples include:

- `PodPhysicsObject`
- `PodPhysicsObjectGroup`
- `PodCameraController`
- `PodTVCamera`
- `PodRaceStartCamera`
- `PodAnnouncer`
- `PodJukebox`
- `VisibilityQuadTree`
- `WaterObject`
- `PSXRenderStateBlock`
- `SurfaceGeometryInstance`
- `PSXSignatureWave`

Compiler-identification text includes `MW MIPS C Compiler (2.4.1.01)`.

## Next checkpoint

Produce an address-backed executable map rather than relying only on strings.
