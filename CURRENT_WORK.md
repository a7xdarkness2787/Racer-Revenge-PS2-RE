# Current Work

## Active investigation

Follow the independently reconstructed PSG mesh data into the VU/material submission path and close the remaining render-format exceptions.

## Latest development

The detailed POD01/TA/TB sample is now parsed end-to-end: **881 PSG files, 0 file-level failures, and no unexplained bytes after the known optional tail**.

The renderer-side serialization is substantially clearer:

- 0x24-byte render header
- one or more LOD groups
- 0x14-byte material-block headers
- VIF packets
- optional multi-object identity remap tail

Position reconstruction is now verified:

```text
xyz = position_origin + signed_raw_xyz * position_scale
object_index = abs(W) / 16 - 1
```

Ordinary triangle strips are reconstructed from the W sign with alternating winding. The rule validates with zero structural topology warnings in 877 ordinary PSGs.

V3-8 data is strongly validated as normal vectors. VIF control bits now independently confirm signed expansion for positions/normals/V2-16 and unsigned expansion for V4-8. All geometry UNPACK destinations are FLG=1 and therefore VIF1_TOPS-relative. V2-16 remains texture-coordinate-like and V4-8 remains color-like until direct render-state correlation is complete.

The four `CableShadow*.psg` files are the known special topology exception.

Six POD01 render components now cross-check against matching type-0 COL bounds to floating-point precision.

## Current evidence

- `formats/PSG.md`
- `analysis/2026-10-08-psg-mesh-reconstruction.md`
- `records/2026-10-08-psg-render-payload.md`
- `executable/psx_surface_geometry.md`
- `scripts/psg_mesh_extract.py`
- `raw/2026-10-08-psg-render-summary.txt`
- `reference/corpus-summary.json`
- `reference/ps2-vif.md`
- `records/2026-10-08-vif-unpack-flags.md`

## Immediate queue

- identify the VU microprogram reached by the geometry MSCNT path
- map the remaining material-block flag bits; bit `0x8` is now verified as V4-8-presence
- identify the material-block `+0x08` float
- prove V2-16 texture-coordinate semantics against texture/material use
- identify V4-8 channel semantics
- decode the four CableShadow PSGs without forcing the ordinary strip rule
- determine the runtime metric compared with 0.18/0.36/0.50 LOD thresholds
- expand detailed payload validation from the 881-file sample toward all 9,917 PSG resources
- start retained PCSX2 geometry/runtime capture once the VU/material path is stable

## Documentation contract

Every meaningful development is recorded in the same work cycle according to `UPDATE_PROTOCOL.md`.
