# 2026-10-08 — PSG render payload and mesh reconstruction

## Question

Can the PSG data after the fixed hierarchy/material tables be parsed end-to-end and independently reconstructed into geometry?

## Inputs

Private canonical retail inputs:

- `PODS/POD01/POD01.RES`
- `TRACKS/TA.RES`
- `TRACKS/TB.RES`
- canonical `SLUS_202.68`
- matching POD01 collision resources for cross-format validation

No retail payload or reconstructed retail mesh is committed.

## VERIFIED — sample closure

Detailed render-payload parsing now covers all **881 PSG files** in POD01, TA and TB.

The parser consumes:

- a 0x24-byte render header
- one or more LOD groups
- 1,216 material/VIF blocks
- 18,965 MSCNT-terminated geometry batches
- 250,514 submitted position records
- an optional identity object-remap tail in the 16 multi-object files

No unexplained bytes remain in the 881-file sample.

This is sample closure, not yet a claim that all 9,917 retail PSG payloads have been validated.

## VERIFIED — position reconstruction

The render header supplies:

- position scale
- fixed normal scale 1/127
- fixed UV-like scale 1/2047
- position origin
- origin-presence flag
- LOD-group count

Position xyz is reconstructed as:

`origin + signed_raw_position * position_scale`.

The rule validates against all 865 single-object PSG fixed bounds to within one position quantization unit and against a multi-object V4-32 example.

## VERIFIED — hierarchy object tag

For all 250,514 positions:

`object_index = abs(W)/16 - 1`

with zero invalid tags.

Negative W participates in strip restart/setup; positive W emits ordinary strip triangles.

## VERIFIED — ordinary mesh topology

The ordinary triangle-strip reconstruction has zero structural warnings in 877 PSGs.

Four `CableShadow*.psg` resources do not obey the ordinary primitive rule and are retained as a special-case open question.

## VERIFIED — material and LOD organization

Material blocks map directly to the fixed material-name table by group-local slot.

Three main POD01 PSGs use four LOD groups at thresholds 0.18, 0.36, 0.50 and FLT_MAX. Triangle counts fall with successive groups, independently supporting the LOD interpretation.

## VERIFIED — cross-format bounds

Six POD01 render components were reconstructed and compared with matching type-0 COL resources.

PSG decoded bounds -> PSG fixed bounds -> COL bounds agree within quantization/float precision.

This provides independent evidence that the render position scaling is correct.

## Tooling

`scripts/psg_mesh_extract.py` contains the independently written parser/mesh reconstruction logic.

Generated OBJ files are private validation products and are intentionally excluded from the repository.

## Remaining work

- identify the material-block flag bits and metric
- establish exact UV/color semantics
- decode CableShadow geometry
- locate the VU microprogram and GIF/GS output
- run the detailed payload parser over all 9,917 PSG resources
