# PS2 surface geometry (.psg)

Status: **VERIFIED fixed tables across 9,917 retail resources; VERIFIED detailed render payload for the 881-file POD01/TA/TB sample**.

The full retail corpus and the detailed payload sample are intentionally distinguished throughout this document.

## Fixed tables — full retail corpus

```text
char tag[4]      // "psg\0"
u32  version     // 3
u32  object_count
object_descriptor objects[object_count]
u32  material_count
char material_name[material_count][0x40]
```

Complete-corpus totals:

- PSG resources: **9,917**
- object descriptors: **17,942**
- material-name records: **22,175**
- object count per file: 1..33
- material count per file: 1..15

### Object descriptor — 0xe0 bytes

```text
char  name[0x80]
float matrix[16]
float center_like[3]
float half_extent_like[3]
float radius_like
u32   parent_index
```

The executable reads these fields in exactly 0x80, 0x40, 0x0c, 0x0c, 0x04 and 0x04 byte pieces.

`0xffffffff` is the no-parent/root value. Every full-corpus PSG has exactly one root; all non-root parent indices are valid and acyclic.

## Detailed render payload — 881-file sample

The current detailed sample is every PSG embedded in canonical POD01, TA and TB RES containers.

All 881 payloads are parsed end-to-end with no unexplained bytes.

### Render header — 0x24 bytes

Immediately after the fixed material-name table:

```text
+0x00  f32 position_scale
+0x04  f32 normal_scale
+0x08  f32 uv_scale_u
+0x0c  f32 uv_scale_v
+0x10  f32 position_origin[3]
+0x1c  u32 origin_present
+0x20  u32 lod_group_count
```

Verified sample invariants:

- `normal_scale == 1/127`
- `uv_scale_u == uv_scale_v == 1/2047`
- `origin_present` is 0 or 1
- the flag is 1 exactly when `position_origin` is nonzero

### LOD group

```text
f32 threshold
u32 material_block_count
MaterialBlock blocks[material_block_count]
```

878 sampled files contain one group with threshold `FLT_MAX`.

Three POD01 main models contain four groups with thresholds:

`0.18, 0.36, 0.50, FLT_MAX`.

Triangle counts decrease through those groups, establishing their LOD role. The runtime quantity compared against the finite thresholds is still open.

### Material block

```text
+0x00  u32 material_slot
+0x04  u32 flags
+0x08  f32 metric
+0x0c  u32 packed_counts
+0x10  u32 vif_packet_size
        u8 vif_packet[vif_packet_size]
```

Across 1,216 blocks:

- group-local material slots are sequential
- flattened groups consume exactly the fixed material-name table
- low 16 bits of `packed_counts` equal submitted vertex count in every block
- high 16 bits behave as a declared strip count but are not promoted to an exact semantic equality yet
- packet size is 16-byte aligned and bounded

Flags have a perfect observed split:

- `0x00000107` — multi-object PSG blocks
- `0x00ff010f` — single-object PSG blocks

Across all 1,216 blocks, flag bit `0x8` is set if and only if the optional V4-8 stream is present. This correlation has zero failures and strongly identifies bit `0x8` as the V4-8 attribute-presence flag.

The remaining flag bits, the `0xff` field in the single-object value, and the `metric` field remain open.

## VIF geometry batches

Across the 881-file sample:

- material blocks: 1,216
- MSCNT geometry batches: **18,965**
- submitted positions: **250,514**

Every batch begins with a one-vector V4-32 header UNPACK whose ADDR field is 0. FLG=1, so this and the following attribute destinations are relative to VIF1_TOPS rather than absolute VU addresses.

Its payload is:

```text
u32 0x8000 | N
u32 0x30024000
u32 0x00000412
u32 0x00000000
```

where `N` is the following per-element count.

Most batches then use:

```text
V4-16  N elements
V3-8   N elements
V2-16  N elements
V4-8   N elements   // optional
MSCNT
```

135 batches use V4-32 rather than V4-16 for their position stream.

The UNPACK ADDR fields are contiguous for the per-element streams. All sampled geometry UNPACKs use FLG=1, so the sequence is VIF1_TOPS-relative.

## Position decoding

Position source values are signed integers:

- V4-16 -> four signed s16 values
- V4-32 -> four signed s32 values

XYZ decode as:

```text
position = position_origin + raw_xyz * position_scale
```

This rule reproduces fixed PSG bounds within one position quantization unit for all 865 single-object files in the detailed sample and also reproduces multi-object V4-32 bounds.

### W component

For all 250,514 sampled submitted positions:

```text
object_index = abs(W) / 16 - 1
```

W is never zero, is always a multiple of 16 in magnitude, and always resolves to a valid hierarchy object.

The magnitude therefore provides object ownership.

## Ordinary triangle strips

For 877 ordinary PSGs:

- two consecutive negative W records of the same object magnitude establish/restart a strip
- each following positive W record emits the next triangle from the prior two positions
- winding alternates
- object ownership remains consistent

The reconstruction produces zero structural topology warnings across those ordinary files.

The four `CableShadow*.psg` files do not obey this ordinary primitive rule and remain a special case.

## Other vertex streams

### V3-8

All sampled V3-8 UNPACK commands use FLG=1 and USN=0. Decode as signed s8 xyz multiplied by `normal_scale`.

Geometric triangle normals align with averaged decoded vectors in ~99.775% of nondegenerate ordinary-triangle comparisons, strongly validating this as the normal stream.

### V2-16

All sampled V2-16 UNPACK commands use FLG=1 and USN=0. Signed 16-bit pairs multiplied by `1/2047` produce plausible tiled coordinate ranges.

Current semantic status: **INFERRED texture-coordinate stream**.

### V4-8

Optional four-byte per-vertex stream.

All 17,787 sampled V4-8 UNPACK commands use FLG=1 and USN=1. Under the standard VIF UNPACK contract this means the source is zero-extended unsigned byte data.

Across 234,318 records, observed channel minima are 0/0/0/0 and maxima are 127/127/127/79.

Current semantic status: **VERIFIED unsigned V4-8 attribute; INFERRED color-like meaning**.

## Material ownership

A material block owns its VIF packet.

The material name is:

```text
fixed_material_index =
    sum(previous_lod_group_block_counts)
  + material_slot
```

This mapping is structurally verified in every sampled payload.

## Multi-object tail

All 16 sampled multi-object PSGs and only those files carry a final remap record:

```text
u32 kind                  // 1
u32 aligned_index_bytes   // align4(object_count)
u8  object_indices[aligned_index_bytes]
u32 object_count
```

The active mapping bytes are the identity sequence `0..object_count-1` followed by zero padding.

Its precise runtime purpose remains open.

## Cross-format validation

Reconstructed render bounds for six POD01 engine subcomponents agree with:

1. their PSG fixed-table bounds within one position quantization unit; and
2. their matching type-0 COL bounds to approximately `7.2e-7` maximum error.

This independently validates the position scale/origin reconstruction.

## Tooling

- `scripts/psg_inspect.py` — fixed-table validation
- `scripts/psg_vif_inspect.py` — first VIF block inspection
- `scripts/psg_mesh_extract.py` — detailed payload parsing and ordinary mesh reconstruction

## Open questions

- full 9,917-file detailed payload validation
- material-block flag semantics
- material-block `+0x08` metric
- exact LOD selection metric
- direct proof of V2-16 UV semantics
- V4-8 channel semantics
- CableShadow primitive format
- VU microprogram
- GIF/GS output and material render state

## VIF control-bit reference

The UNPACK FLG/USN interpretation used here is recorded in `reference/ps2-vif.md`. Earlier notes that described ADDR 0/1/... as absolute VU addresses are superseded by the TOPS-relative interpretation.
