# PS2 surface geometry (.psg)

Status: **VERIFIED across the complete North American retail PSG corpus for fixed tables, render headers, LOD/material block serialization, VIF packet grammar, position decoding and serialized triangle-strip topology.**

Canonical build: `SLUS_202.68`  
Executable SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

## Complete retail coverage

The recovered retail dataset contains **9,917** embedded PSG resources across **103 RES containers**.

Detailed parser result:

- 9,917 / 9,917 payloads parsed
- 0 parser failures
- 0 unexplained payload bytes
- 17,942 hierarchy descriptors
- 22,175 material-name records
- 22,175 material/VIF blocks
- 366,935 VIF geometry batches
- 4,869,177 submitted position records

## Fixed header

```text
char tag[4]      // "psg\0"
u32  version     // 3
u32  object_count
```

### Hierarchy descriptor — 0xe0 bytes

```text
char  name[0x80]
float matrix[16]
float center[3]
float half_extents[3]
float radius_like
u32   parent_index
```

The executable reads these fields in exactly 0x80, 0x40, 0x0c, 0x0c, 0x04 and 0x04 byte pieces.

`0xffffffff` is the root/no-parent value.

All retail files have exactly one hierarchy root, valid parent indices and acyclic parent chains.

## Material-name table

After the hierarchy descriptors:

```text
u32 material_count
char material_name[material_count][0x40]
```

Every name is ASCII, NUL-terminated and zero-padded.

## Render header — 0x24 bytes

Immediately after the fixed material table:

```text
+0x00  f32 position_scale
+0x04  f32 normal_scale
+0x08  f32 uv_scale_u
+0x0c  f32 uv_scale_v
+0x10  f32 position_origin[3]
+0x1c  u32 origin_present
+0x20  u32 lod_group_count
```

Complete-corpus invariants:

- `normal_scale == 1/127` in 9,917 / 9,917 files
- `uv_scale_u == uv_scale_v == 1/2047` in 9,917 / 9,917 files
- `origin_present` is always 0 or 1
- flag 0 corresponds to zero origin: 8,565 files
- flag 1 corresponds to nonzero origin: 1,352 files
- no origin/flag mismatches

## LOD groups

Each group begins:

```text
f32 threshold
u32 material_block_count
MaterialBlock blocks[material_block_count]
```

Distribution:

- one LOD group: **9,846 PSGs**
- four LOD groups: **71 PSGs**

The 71 four-group files are exactly the major pod meshes:

- chariot + left engine + right engine for all 23 pods: 69
- POD02's additional left/right engine pair: 2

The finite threshold sequence is approximately:

```text
0.18
0.36
0.50
FLT_MAX
```

Three files differ only by the final representable float bit in the first two constants.

## Material block — 0x14-byte header

```text
+0x00  u32 material_slot
+0x04  u32 flags
+0x08  f32 metric
+0x0c  u32 packed_counts
+0x10  u32 vif_packet_size
        u8 vif_packet[vif_packet_size]
```

The 22,175 blocks exactly consume the 22,175 fixed material-name records.

`packed_counts & 0xffff` equals the exact submitted position count for every block.

The high 16 bits remain a strip-related count under investigation. They never exceed the number of serialized negative-pair strip starts.

### Flags

Exactly four values occur:

| Flags | Blocks | Hierarchy form | V4-8 |
| ---: | ---: | --- | --- |
| `0x00ff010f` | 18,614 | single-object | present |
| `0x00ff0107` | 318 | single-object | absent |
| `0x0000010f` | 7 | multi-object | present |
| `0x00000107` | 3,236 | multi-object | absent |

For every block:

```text
flags =
    0x00000107
  | (0x00000008 if V4-8 is present)
  | (0x00ff0000 if the PSG has exactly one hierarchy object)
```

Bit `0x8` is therefore verified as the optional V4-8 attribute-presence bit.

The engine-facing meaning of the `0xff` field and the `+0x08` float remain open.

## VIF geometry batches

Every batch begins with one V4-32 header UNPACK.

The per-batch 16-byte header payload is:

```text
u32 0x8000 | N
u32 0x30024000
u32 0x00000412
u32 0x00000000
```

`N` is the following element count.

Only four geometry grammars occur across all **366,935** batches:

| Position stream | V3-8 | V2-16 | V4-8 | Batches |
| --- | --- | --- | --- | ---: |
| V4-16 | yes | yes | yes | 126,732 |
| V4-16 | yes | yes | no | 104,583 |
| V4-32 | yes | yes | yes | 78,015 |
| V4-32 | yes | yes | no | 57,605 |

Totals:

- V4-16 position batches: **231,315**
- V4-32 position batches: **135,620**

All geometry UNPACKs use FLG=1, so ADDR fields are relative to VIF1_TOPS.

Header, position, V3-8 and V2-16 streams use USN=0. V4-8 uses USN=1.

See `reference/ps2-vif.md`.

## Position decoding

Position source values are signed integers:

- V4-16 -> signed s16 x/y/z/w
- V4-32 -> signed s32 x/y/z/w

XYZ decode as:

```text
position = position_origin + raw_xyz * position_scale
```

Across the complete corpus, 16,948 hierarchy descriptors receive submitted positions. Their decoded local bounds reproduce the stored center/half-extents within approximately **1.153 position quantization units** at worst.

994 hierarchy descriptors receive no submitted positions.

## W tag: transform index and strip control

All **4,869,177** position records satisfy:

- W is nonzero
- `abs(W)` is divisible by 16
- the resulting hierarchy index is in range

The transform index is:

```text
transform_index = abs(W) / 16 - 1
```

The sign controls triangle-strip seeding:

- two consecutive negative W values seed/restart a strip
- every subsequent positive W emits the next triangle
- winding alternates

Complete-corpus topology result:

- serialized strip starts: **872,158**
- reconstructed triangles: **3,124,861**
- topology warnings: **0**

W magnitude is a per-vertex hierarchy transform selector, not a rule that all vertices of one triangle must use the same transform.

Evidence:

- 10,243 strip seed pairs use different transform indices
- 85,981 reconstructed triangles span multiple transforms

This behavior occurs in articulated/cutscene/rider geometry and cable geometry.

## Other vertex streams

### V3-8

V3-8 uses signed expansion and scale `1/127`.

The earlier triangle-normal comparison strongly supports this as the normal-vector stream.

Status: **VERIFIED serialization and signed scaling; strongly supported normal semantics**.

### V2-16

V2-16 uses signed expansion and scale `1/2047`.

Status: **VERIFIED serialization and signed scaling; INFERRED texture-coordinate semantics**.

### V4-8

V4-8 uses unsigned expansion.

Full-corpus records: **2,709,497**.

All four byte channels reach both 0 and 255 somewhere in the corpus.

Status: **VERIFIED unsigned V4-8 attribute; INFERRED color-like semantics**.

## Multi-object remap tail

All **1,035** multi-object PSGs and only those files contain:

```text
u32 kind                  // 1
u32 aligned_index_bytes   // align4(object_count)
u8  object_indices[aligned_index_bytes]
u32 object_count
```

The active mapping is the identity sequence `0..object_count-1`, followed by zero padding.

All **8,882** single-object PSGs omit this tail.

## Material ownership

Each material block owns its following VIF packet.

Within each LOD group, `material_slot` is sequential. The fixed material table is the flattened sequence of group-local material slots.

## Cross-format validation

Earlier POD01 validation showed reconstructed PSG local bounds matching corresponding type-0 COL bounds to floating-point precision for six engine subcomponents.

The complete PSG corpus now independently validates the position scale/origin rule against stored PSG descriptor bounds.

## Tooling

- `scripts/psg_inspect.py` — fixed-table validation
- `scripts/psg_vif_inspect.py` — VIF packet inspection
- `scripts/psg_mesh_extract.py` — per-file render payload and strip reconstruction
- `scripts/psg_corpus_verify.py` — multi-RES corpus verification
- `raw/2026-10-08-psg-full-corpus-summary.txt` — complete retail aggregate

## Open questions

- hierarchy matrix composition for assembled/articulated geometry
- VU microprogram used by MSCNT
- GIF/GS submission and render-state generation
- exact semantic identity of material-block `+0x08`
- exact runtime LOD-selection metric
- direct proof of V2-16 texture coordinates
- V4-8 channel semantics
- exact meaning of the `0xff` single-object flag field
- exact pre-batching meaning of `packed_counts >> 16`
