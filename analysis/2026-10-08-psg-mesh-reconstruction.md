# PSG mesh reconstruction — 2026-10-08

> **SUPERSEDED TOPOLOGY INTERPRETATION:** The same-transform-per-triangle restriction in this sample-era note was invalidated by the complete 9,917-file corpus. The corrected rule uses W sign for strip seeding/restart and W magnitude as a per-vertex hierarchy transform index. See `analysis/2026-10-08-psg-full-corpus.md` and `records/2026-10-08-psg-full-corpus.md`. The sample measurements below are retained as historical evidence.

**Canonical executable:** `SLUS_202.68`  
**SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`  
**Status:** VERIFIED for the 881-file POD01/TA/TB payload sample, except where explicitly marked INFERRED  
**Confidence:** high for serialization, position decoding, object ownership, ordinary strip topology, material-block ownership and PSG/COL bounds agreement

## Scope

This investigation continues the VIF work recorded in `analysis/2026-10-07-psg-vif-payload.md`.

Private retail inputs remained outside Git:

- `PODS/POD01/POD01.RES`
- `TRACKS/TA.RES`
- `TRACKS/TB.RES`
- matching privately reconstructed `.col` resources
- canonical `SLUS_202.68`

The three RES containers contain **881 PSG resources**. Fixed PSG tables remain validated across the full 9,917-resource corpus; the detailed render-payload results below currently apply to this 881-file canonical sample.

## VERIFIED — complete sampled payload grammar

All 881 PSGs are consumed without unexplained bytes after parsing the following structure:

```text
fixed PSG tables

RenderHeader
repeat lod_group_count:
    LodGroup
    repeat material_block_count:
        MaterialBlock
        VIF packet

optional multi-object remap tail
```

### RenderHeader — 0x24 bytes

```text
+0x00  f32 position_scale
+0x04  f32 normal_scale
+0x08  f32 uv_scale_u
+0x0c  f32 uv_scale_v
+0x10  f32 position_origin[3]
+0x1c  u32 origin_present
+0x20  u32 lod_group_count
```

Corpus-wide sample invariants:

- `normal_scale == 1/127` in 881/881 files
- `uv_scale_u == uv_scale_v == 1/2047` in 881/881 files
- `origin_present` is always 0 or 1
- `origin_present == 1` exactly when the origin vector is nonzero: 340 files
- `origin_present == 0` exactly when the origin is zero: 541 files

The field at `+0x1c` is therefore structurally verified as an origin-presence flag. The final runtime reason for switching origin handling remains open.

### LOD groups

Each group begins:

```text
f32 threshold
u32 material_block_count
```

Observed group counts:

- 878 PSGs have one group
- 3 PSGs have four groups

The three four-group files are the main POD01 `englt1.psg`, `engrt1.psg` and `chariot.psg` models.

Their thresholds are exactly:

```text
0.18
0.36
0.50
FLT_MAX
```

All one-group files use `FLT_MAX`.

Geometry complexity decreases monotonically through the finite-threshold groups. Examples:

- `englt1.psg`, material `01_1`: 873 -> 457 -> 194 -> 54 triangles
- `chariot.psg`, material `01_2`: 1330 -> 579 -> 263 -> 97 triangles

The group is therefore identified as an LOD group with high confidence. The exact runtime quantity compared with 0.18/0.36/0.50 remains open.

### MaterialBlock — 0x14-byte header

```text
+0x00  u32 material_slot
+0x04  u32 flags
+0x08  f32 metric
+0x0c  u32 packed_counts
+0x10  u32 vif_packet_size
        u8  vif_packet[vif_packet_size]
```

Sample totals:

- LOD groups: **890**
- material blocks: **1,216**
- fixed material-name records: **1,216**

For every sampled PSG:

- the sum of LOD material-block counts equals the fixed material-name count
- `material_slot` is exactly `0..block_count-1` inside each group
- the fixed material-name table is the flattened sequence of group-local material slots
- `vif_packet_size` is 16-byte aligned and bounded
- `packed_counts & 0xffff` equals the exact number of submitted VIF position records in 1,216/1,216 blocks

The high 16 bits of `packed_counts` behave as a declared strip count. They match directly observed strip starts in 979/1,216 blocks and never exceed the observed starts. Batch boundaries can create additional serialized restart pairs, so this semantic name remains **INFERRED**, not promoted to a universal equality.

Block flags have a perfect structural split:

- `0x00000107`: all 54 blocks from the 16 multi-object PSGs
- `0x00ff010f`: all 1,162 blocks from the 865 single-object PSGs

No exceptions occur.

A second pass over VIF control bits establishes one flag meaning: material-block bit `0x8` is set if and only if the optional V4-8 stream is present, with 0 failures across all 1,216 blocks.

The remaining flag bits and the float at `+0x08` remain unnamed.

## VERIFIED — VIF population

Across all 1,216 material packets:

- MSCNT-terminated VIF geometry batches: **18,965**
- submitted position records: **250,514**
- V4-16 position batches: **18,830**
- V4-32 position batches: **135**

Command totals:

| VIF command | Count |
| ---: | ---: |
| `0x00` NOP | 1,797 |
| `0x17` MSCNT | 18,965 |
| `0x65` V2-16 | 18,965 |
| `0x6a` V3-8 | 18,965 |
| `0x6c` V4-32 | 19,100 |
| `0x6d` V4-16 | 18,830 |
| `0x6e` V4-8 | 17,787 |

The extra 135 V4-32 commands are full-width position streams; the remaining 18,965 are the per-batch header upload.

### VIF UNPACK control bits

Using the standard PS2 VIF UNPACK immediate layout:

- ADDR: bits 0..9
- USN: bit 14
- FLG: bit 15

the complete sample shows:

- batch header: FLG=1, USN=0 — 18,965/18,965
- position: FLG=1, USN=0 — 18,965/18,965
- V3-8 normal: FLG=1, USN=0 — 18,965/18,965
- V2-16 coordinate: FLG=1, USN=0 — 18,965/18,965
- V4-8 optional attribute: FLG=1, USN=1 — 17,787/17,787

This corrects the earlier shorthand “VU address 0/1/...”: FLG=1 makes the observed ADDR sequence relative to VIF1_TOPS.

USN=1 also proves the V4-8 source is unsigned byte data.

## VERIFIED — position decoding

V4-16 positions are signed `s16 x,y,z,w`.

V4-32 positions are signed `s32 x,y,z,w`, not IEEE floating-point positions.

For xyz:

```text
decoded_xyz = position_origin + raw_signed_xyz * position_scale
```

Independent validation:

- all 865 single-object PSGs reconstruct root-object bounds to within one position quantization unit
- maximum observed bound error divided by `position_scale` is below 1.0
- no single-object file exceeds a 1.01-quantization-unit tolerance
- a V4-32 multi-object test (`anim\tb_doorframe.psg`) reconstructs all three fixed object bounds to approximately 6e-6

This moves the position scale/origin rule to **VERIFIED** for the sampled payload.

## VERIFIED — object ownership in position W

For every one of the **250,514** submitted position records:

- W is nonzero
- `abs(W)` is divisible by 16
- `object_index = abs(W) / 16 - 1` is a valid hierarchy index

Violations: **0**.

Examples:

- W magnitudes 16, 32, 48 map to hierarchy objects 0, 1, 2
- POD multi-object geometry uses the same encoding for component ownership

The sign is used by ordinary strip topology; the magnitude encodes object ownership.

## VERIFIED — ordinary triangle-strip topology

For **877 ordinary PSGs** in the sample:

- two consecutive negative W records of the same object magnitude establish/restart a strip
- each following positive W record emits the next triangle using the two previous positions
- triangle winding alternates per emitted triangle
- object ownership of the prior two records matches the current positive record

Structural topology warnings: **0** across all ordinary files, LODs and material blocks.

The four `CableShadow*.psg` resources are explicit exceptions and remain a separate special primitive/VU path. The ordinary rule is not forced onto them.

## VERIFIED / INFERRED — vertex attributes

The V3-8 stream decodes as signed `s8 xyz * (1/127)`.

Against reconstructed ordinary triangles:

- nondegenerate triangle-normal comparisons: 154,207
- positive alignment with averaged decoded vertex normals: 153,860 (~99.775%)
- dot product greater than 0.5: 153,443 (~99.505%)
- median dot product: ~0.98778
- mean dot product: ~0.95778

This strongly validates V3-8 as a normal vector stream.

The V2-16 stream, scaled by `1/2047`, produces plausible tiled coordinate ranges and remains **INFERRED** as texture coordinates pending material/texture correlation.

The optional V4-8 stream is **VERIFIED unsigned byte data** under VIF semantics and remains **INFERRED** as color-like data. Across 234,318 sampled records its four channel maxima are 127/127/127/79.

## VERIFIED — material ownership

Each material block owns its full VIF packet.

The fixed material table is a flattened sequence of LOD-group-local material names:

```text
material_table_index =
    sum(previous_lod_group_block_counts)
  + material_slot
```

This permits independent mesh export with stable `usemtl` boundaries without guessing per-triangle materials.

## VERIFIED — multi-object remap tail

All 16 multi-object PSGs and only those files contain a tail after the final LOD group.

The tail consumes the entire remaining file:

```text
u32 kind                  // 1
u32 aligned_index_bytes   // align4(object_count)
u8  object_indices[aligned_index_bytes]
u32 object_count
```

The active bytes are the identity sequence `0,1,2,...` followed by zero padding.

Single-object PSGs: 865, tail absent.  
Multi-object PSGs: 16, tail present.  
Validation failures: 0.

Its structural role as an object-index remap table is verified; its precise runtime use remains **INFERRED**.

## VERIFIED — independent mesh reconstruction

A private validation run reconstructed OBJ geometry from an extracted POD01 PSG using only the independently recovered serialization rules.

For `englt1a.psg`, LOD 0:

- material `01_1`: 428 submitted vertices, 86 strips, 256 triangles
- material `01_2`: 18 vertices, 4 strips, 10 triangles
- material `01_3`: 8 vertices, 2 strips, 4 triangles

The generated OBJ loaded successfully in an independent mesh library. Retail-derived OBJ output is not committed.

## VERIFIED — PSG/COL bounds agreement

Six POD01 render/collision component pairs were compared:

- `englt1a`
- `englt1b`
- `englt1c`
- `engrt1a`
- `engrt1b`
- `engrt1c`

For each pair:

1. reconstructed PSG geometry matches the PSG fixed root bounds within one position quantization step
2. matching type-0 `*f.COL` bounds match the PSG fixed root bounds to sub-micro-unit floating-point error

Across the six pairs, the maximum PSG-fixed vs type-0 COL center/half-extent error is approximately `7.2e-7`.

This is an independent cross-format validation of the recovered render coordinate scale.

Type-2 `*m.COL` bounds are close but can contain small expansions; their higher-level collision role remains separate.

Track PSG/COL pairs often differ in center because render data can carry a world origin while matching collision data remains in local coordinates. Their placement transform is still being mapped.

## Open questions

- exact semantics of material-block flag bits other than the verified V4-8-presence bit `0x8`
- semantic identity of the block `+0x08` float
- exact runtime LOD comparison metric
- proof of V2-16 texture coordinates through texture/material use
- proof and channel meaning of V4-8 color-like data
- CableShadow special topology
- VU microprogram identity
- GIF/GS state emitted by the geometry path
- whole-corpus payload validation over all 9,917 PSGs

## Reproduction

Use `scripts/psg_mesh_extract.py` against a user-supplied extracted PSG. It parses the payload, validates counts and ownership, reconstructs ordinary strip geometry, summarizes LOD/material blocks and can export a selected LOD as OBJ for private validation.

## Public VIF reference

The FLG/USN interpretation is sourced from the PS2SDK VIF definitions and is summarized in `reference/ps2-vif.md`.
