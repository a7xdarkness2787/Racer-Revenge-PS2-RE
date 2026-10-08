# PS2 surface geometry (.psg)

Status: **VERIFIED for the fixed tables and first VIF payload block**. Later multi-block payload structures remain under investigation.

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

`0xffffffff` is the no-parent/root value. Every retail PSG has exactly one root; non-root parents are in range, refer to earlier descriptors, and form an acyclic hierarchy. Maximum observed depth is 7.

The two vec3 fields and following float are structurally verified but their final culling/bounds names remain inferred pending runtime confirmation.

## Material-name table

After the object descriptors:

```text
u32 material_count
char material_name[material_count][0x40]
```

Complete-corpus totals:

- material-name records: **22,175**
- material count per PSG: 1..15

Names are ASCII, NUL-terminated and zero-padded.

## Fixed-table payload boundary

```text
payload_offset =
    0x0c
  + object_count * 0xe0
  + 0x04
  + material_count * 0x40
```

All 9,917 files contain data after this point.

## First PS2 render block

A focused sample consisting of every PSG embedded in canonical `POD01.RES`, `TA.RES` and `TB.RES` contains **881 PSG files**.

Every one begins its post-table payload with:

```text
+0x00  descriptor[0x40]
+0x40  VIF packet
```

Within this first descriptor:

| Offset | Size | Verified meaning |
| --- | ---: | --- |
| `+0x3c` | 4 | byte size of the following first VIF packet |

The declared packet size is 16-byte aligned and in-bounds in all 881 files.

For this sample:

- 687 files end exactly after the first 0x40-byte descriptor and its VIF packet;
- 7 contain a further 16 bytes;
- 187 contain larger additional structures.

The other 0x40 descriptor fields are deliberately not assigned semantic names yet.

## VIF stream

The first VIF word in all 881 sampled PSG files is:

`0x6c018000`

The current bounded VIF parser consumes all 881 first packets without an unknown command or size overrun.

Only these command bytes occur in the sampled first packets:

- `0x6c` — UNPACK V4-32
- `0x6d` — UNPACK V4-16
- `0x6a` — UNPACK V3-8
- `0x65` — UNPACK V2-16
- `0x6e` — UNPACK V4-8
- `0x17` — MSCNT
- `0x00` — NOP/padding

A common batch sequence is:

```text
UNPACK V4-32
UNPACK V4-16
UNPACK V3-8
UNPACK V2-16
UNPACK V4-8
MSCNT
```

This is a recurring pattern, not a claim that every batch has every command.

## Executable agreement

The PS2 surface-geometry implementation contains `PSXSurfaceGeometry` type metadata.

At `0x00246a58..0x00246a9c`, executable code constructs VIF data and emits the same `0x6c018000` command constant seen at the beginning of all 881 sampled first packets.

The generic SurfaceGeometry load path also calls the PS2 packet helper `0x00246300` from `0x0026e34c`.

See `executable/psx_surface_geometry.md`.

## What remains open

- semantic names for the remaining 0x40 descriptor fields;
- later payload record layouts in the 194 sampled files that continue after the first packet;
- hierarchy-object ownership of draw packets;
- material indices per draw batch;
- UNPACK destination semantics in VU memory;
- VU microprogram identity;
- GIF/GS state and submission behavior;
- independent mesh reconstruction.

Use:

- `scripts/psg_inspect.py` for fixed-table validation;
- `scripts/psg_vif_inspect.py` for the first VIF payload block.
