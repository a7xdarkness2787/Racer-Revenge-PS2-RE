# PS2 surface geometry (.psg)

Status: **VERIFIED for the fixed tables and first VIF geometry block**. Later multi-block structures and final rendering semantics remain under investigation.

The complete recovered retail corpus contains **9,917** embedded `.psg` resources. All 9,917 pass the fixed-table parser.

## Common header

```text
char tag[4]      // "psg\0"
u32  version     // 3
u32  object_count
```

Complete-corpus totals:

- object descriptors: **17,942**
- object count per PSG: 1..33

## Object descriptor

Immediately after the 12-byte header are `object_count` records of **0xe0 bytes**:

```text
char  name[0x80]
float matrix[16]
float vec_a[3]
float vec_b[3]
float radius_like
u32   parent_index
```

The executable reads those fields in exactly 0x80, 0x40, 0x0c, 0x0c, 0x04 and 0x04 byte pieces.

`0xffffffff` is the no-parent/root value. Every retail PSG has exactly one root; non-root parents are in range, refer to earlier descriptors, and form an acyclic hierarchy.

## Material-name table

After the object descriptors:

```text
u32 material_count
char material_name[material_count][0x40]
```

Complete-corpus total: **22,175** material-name records.

## Fixed-table payload boundary

```text
payload_offset =
    0x0c
  + object_count * 0xe0
  + 0x04
  + material_count * 0x40
```

## First PS2 geometry block

The current detailed payload sample contains all **881 PSG resources** from canonical POD01, TA and TB containers.

Every one begins:

```text
descriptor[0x40]
vif_packet[descriptor.u32_3c]
```

Descriptor `+0x3c` is therefore verified as the first VIF packet byte size.

The packet is 16-byte aligned and in-bounds in all 881 sampled files.

## VIF batch contract

The first packet set contains **12,356 MSCNT-terminated batches**.

Every batch starts with:

```text
UNPACK V4-32, NUM=1, VU destination 0

payload:
    u32 0x8000 | N
    u32 0x30024000
    u32 0x00000412
    u32 0x00000000
```

`N` is the count used by the following per-element stream and ranges from 3 to 16.

The low 15 bits of the first payload word equal `N` in all 12,356 sampled batches.

### Batch variants

| Count | Position source | Second stream | Third stream | Optional fourth | Terminator |
| ---: | --- | --- | --- | --- | --- |
| 11,710 | V4-16 | V3-8 | V2-16 | V4-8 | MSCNT |
| 540 | V4-16 | V3-8 | V2-16 | none | MSCNT |
| 106 | V4-32 | V3-8 | V2-16 | none | MSCNT |

For every batch, VU destinations are contiguous:

```text
header      -> 0
positions   -> 1
stream 2    -> 1 + N
stream 3    -> 1 + 2N
stream 4    -> 1 + 3N    // when present
```

This layout is **VERIFIED**.

The likely semantic mapping is currently **INFERRED** as:

- V4 position stream;
- V3 byte normal stream;
- V2 16-bit texture-coordinate stream;
- optional V4 byte color stream.

Those semantic names will be promoted only after independent geometry/runtime validation.

## Executable agreement

The executable contains `PSXSurfaceGeometry` type metadata.

- `0x0026e34c` calls PS2-specific packet helper `0x00246300`
- `0x00246a58..0x00246a9c` constructs VIF data using the same `0x6c018000` base word observed at every sampled first packet

See `executable/psx_surface_geometry.md`.

## Remaining payload

After the first descriptor + VIF packet in the 881-file sample:

- 687 files end;
- 7 contain exactly 16 bytes more;
- 187 contain larger additional structures.

Those later records are still open.

## Open questions

- remaining fields in the 0x40 descriptor;
- position dequantization/scaling for V4-16 data;
- primitive topology;
- hierarchy-object ownership of batches;
- material selection;
- exact normal/UV/color scaling;
- VU microprogram behavior;
- GIF/GS submission;
- later multi-block payload structures.

Use `scripts/psg_inspect.py` for fixed tables and `scripts/psg_vif_inspect.py` for the first VIF block.
