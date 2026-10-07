# Current work

## Active target

Decode the PSG payload beyond its now-verified hierarchy and material tables, then correlate visible geometry with collision and pod/track structures.

## Latest development

The fixed part of the retail PSG format is now reproducible across all 9,917 embedded PSG files.

The verified top-level layout is:

- `psg\0`
- version 3
- object count
- `object_count * 0xe0` hierarchy descriptors
- material count
- `material_count * 0x40` material names
- PS2-specific geometry payload

The corpus contains 17,942 object descriptors and 22,175 material-name records.

Each object descriptor contains a 0x80-byte name, 4x4 affine matrix, two vec3 fields, a radius-like float and a parent index. Every PSG has exactly one root, parent links are valid and acyclic, and the maximum observed hierarchy depth is 7.

Executable confirmation:

- geometry create/format path around `0x0026e820`
- object hierarchy reader `0x0028cac0`
- material-name reader `0x0026e640`

The hierarchy reader performs the same 0x80/0x40/0x0c/0x0c/0x04/0x04 serialized reads independently observed in the files and then builds parent/child/sibling links from the parent indices.

## Current evidence files

- `formats/RES.md`
- `formats/PHY.md`
- `formats/SPL.md`
- `formats/COL.md`
- `formats/PSG.md`
- `executable/resource_loader.md`
- `executable/pod_track_loaders.md`
- `executable/collision_loader.md`
- `executable/surface_geometry_loader.md`
- format inspection scripts under `reverse_engineering/scripts/`
- dated evidence records under `reverse_engineering/records/`

## Next targets

1. Determine the first PSG payload record structure and how payload records are assigned to hierarchy objects.
2. Identify material indices and VIF/VU/GIF/DMA boundaries in the payload.
3. Correlate one pod PSG object's transform/bounds with its matching COL component.
4. Decode the s16 collision-vertex dequantization path used by 11 static collision bodies.
5. Trace TunnelTrack branch/collision data into checkpoint, progress and AI decisions.
6. Start retained PCSX2 runtime captures once geometry object addresses are stable.

## Evidence rule

New findings are written into the dated record and stable subsystem note as soon as they change the current understanding. Failed hypotheses and corrected interpretations stay in the record instead of being silently removed.
