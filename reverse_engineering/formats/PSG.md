# PS2 surface geometry header (.psg)

Status: **VERIFIED for the fixed header tables** in the North American retail corpus. The variable geometry command payload is still under investigation.

The recovered RES corpus contains **9,917** embedded `.psg` resources. All 9,917 pass the current fixed-table parser.

## Common header

```text
char tag[4]      // "psg\0"
u32  version     // 3
u32  object_count
```

Observed across the complete corpus:

- tag `psg\0`: 9,917 / 9,917
- version 3: 9,917 / 9,917
- object count range: 1..33
- total object descriptors: **17,942**

## Object descriptor

Immediately after the 12-byte header are `object_count` fixed-size records.

Serialized stride: **0xe0 bytes**.

```text
char  name[0x80]
float matrix[16]
float vec_a[3]
float vec_b[3]
float radius_like
u32   parent_index
```

The executable reads the descriptor in exactly those pieces: 0x80, 0x40, 0x0c, 0x0c, 0x04 and 0x04 bytes.

### Name

The 0x80-byte object name is ASCII, NUL-terminated and zero-padded in every retail descriptor.

Longest observed name: 26 characters.

### Matrix

Every descriptor contains an affine 4x4 matrix in the observed storage convention. The positions corresponding to the non-translation final row/column are consistently zero with the homogeneous term equal to 1.0.

The matrix often carries local translation and may also carry scale/rotation.

### Bounds fields

The two vec3 fields and following float behave like object-bound data:

- the second vec3 is non-negative throughout the corpus and behaves like half-extents
- the final float is non-negative and radius-like
- the first vec3 behaves like a local bound center

The executable stores these values in the RenderableObject-family runtime object at stable offsets documented in `../executable/surface_geometry_loader.md`.

The serialization of these fields is verified. Their exact renderer/culling semantics remain marked as inferred until runtime checks are retained.

### Parent index

`0xffffffff` means no parent.

All 9,917 PSG files have exactly **one** root descriptor. Every other parent index refers to an earlier descriptor in the same file. No cycles or out-of-range parents occur.

Across the corpus:

- roots: 9,917
- non-root parent links: 8,025
- maximum observed hierarchy depth: 7

The executable uses this field to build parent/child/sibling links after reading the descriptor table.

## Material-name table

Immediately after the object descriptors:

```text
u32 material_count
char material_name[material_count][0x40]
```

Every material name is ASCII, NUL-terminated and zero-padded.

Corpus totals:

- material count per PSG: 1..15
- material-name records: **22,175**
- longest observed material name: 25 characters

The executable resolves these names against its material table. A diagnostic in the same subsystem reads `%s is not in the material table`.

## Payload boundary

The fixed-table end is therefore:

```text
payload_offset =
    0x0c
  + object_count * 0xe0
  + 0x04
  + material_count * 0x40
```

All 9,917 files have additional payload after this point.

Observed payload sizes range from 160 to 264,432 bytes, totaling 113,595,080 bytes across the retail PSG corpus.

The payload contains the PS2-specific geometry/render stream and is the next part of the format being decoded. It should not yet be described as a simple vertex/index buffer.

## Example hierarchy behavior

Pod and track PSG files show ordinary parented object trees. Child descriptors can represent named parts such as body pieces, arms, cables, damage objects and other transformable subobjects.

This makes the PSG hierarchy directly useful for correlating visible geometry with pod damage/animation structures and matching COL resources.

Use `scripts/psg_inspect.py` for the fixed header/table validation.
