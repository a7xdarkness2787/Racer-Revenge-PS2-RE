# Current work

## Active target

Recover visible geometry and connect it to the collision/world structures already mapped.

## Latest development

Collision data is now structurally reproducible across the complete embedded retail corpus.

All 2,505 `.col` resources pass the current parser. The common header, all three serialized collision types, the binary BVH representation, triangle leaves and type-2 two-point leaves are documented.

A full-corpus correction also identified the exact BVH metric:

`8 * max(hx, 0.005) * max(hy, 0.005) * max(hz, 0.005)`

This formula passes all 222,577 observed nodes. The high bit in each u16 child reference selects a leaf; unflagged values index internal nodes.

Executable agreement is now address-backed:

- COL header validation near `0x0011b920`
- type dispatcher `0x00124f80`
- type-0 reader `0x00125890`
- type-1 reader `0x00126450`
- type-2 reader `0x00126640`

## Current evidence files

- `formats/RES.md`
- `formats/PHY.md`
- `formats/SPL.md`
- `formats/COL.md`
- `executable/resource_loader.md`
- `executable/pod_track_loaders.md`
- `executable/collision_loader.md`
- `scripts/res_inspect.py`
- `scripts/phy_inspect.py`
- `scripts/spl_inspect.py`
- `scripts/col_inspect.py`
- dated records under `reverse_engineering/records/`

## Next targets

1. Recover the `.psg` geometry descriptor table and payload boundaries across the 9,917 embedded PSG resources.
2. Tie PSG loading to the `PSXSurfaceGeometry` / `SurfaceGeometry` executable code and identify mesh/material references.
3. Decode the s16 collision-vertex scale path used by 11 static collision bodies.
4. Correlate visible PSG bounds with matching COL bounds for a pod component and a track object.
5. Trace TunnelTrack branches and collision objects into checkpoint/progress and AI decisions.
6. Start retained PCSX2 runtime captures once geometry/collision object addresses are stable.

## Evidence rule

New findings are written into the dated record and stable subsystem note as soon as they change the current understanding. Failed hypotheses and corrected interpretations stay in the record instead of being silently removed.
