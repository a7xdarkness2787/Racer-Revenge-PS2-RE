# Collision loader map

Build: North American retail `SLUS_202.68`  
Executable SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

Status: **OBSERVED / address-backed**.

## Header validation

The wrapper beginning near `0x0011b920` opens and validates a collision resource before calling the main collision-object loader.

High-confidence checks:

| Address | Check |
| --- | --- |
| `0x0011bac8` | first u32 compared with `0x4d2` |
| `0x0011bad8..` | four-byte tag compared with `col\0` |
| `0x0011baf0..` | version compared with `1` |
| `0x0011bb8c` | calls `0x00124f80` |

Bad-header diagnostics in this path are associated with `CollisionObject.cpp`.

## Type dispatcher

The routine at `0x00124f80` reads the collision type and stores it at runtime object offset `+0x88`.

Its three observed branches match the complete 2,505-file corpus:

| Serialized type | Runtime allocation | Reader |
| ---: | ---: | --- |
| 0 | `0x130` bytes | `0x00125890` |
| 1 | `0x100` bytes | `0x00126450` |
| 2 | `0x60` bytes | `0x00126640` |

Other values reach an `Undefined collision type` diagnostic path.

## Type-0 reader

`0x00125890..0x00126414`

The routine reads the 3x4 serialized transform and expands it into a runtime 4x4 transform beginning at object `+0x40`, inserting zero elements and a final 1.0.

Other directly observed runtime fields include:

- `+0x11c`: vertex count
- `+0x108`: serialized vertex-encoding flag
- `+0x100`: primary vertex-array pointer
- `+0x104`: secondary vertex-array pointer when present
- `+0x114`: converted BVH-node array
- `+0x118`: converted triangle-leaf array

The serialized static body uses 32-byte BVH nodes and 22-byte triangle leaves. The loader converts these to runtime representations instead of retaining the file bytes unchanged.

## Type-1 reader

`0x00126450`

This routine reads the compound count, allocates a sequence of `0x130`-byte child objects, reads each child index, and calls the type-0 body reader at `0x00125890` for each inline child.

The child-object stride visible in the loop is `0x130`, matching the type-0 allocation size used by the dispatcher.

## Type-2 reader

`0x00126640`

This routine reads the serialized 4x4 transform and the three count words, then expands the serialized tree/leaves into runtime structures.

The file format uses:

- 32 bytes per BVH node
- 24 bytes per two-point leaf

The runtime conversion uses different strides, confirming that the on-disc structures are serialization formats rather than direct memory dumps.

## R5900 caution

Generic LLVM MIPS output does not decode every Emotion Engine instruction correctly. Addresses and structure claims here rely on unambiguous standard loads/stores, branches, constants, allocation arithmetic and file/corpus validation. R5900-only vector operations remain unnamed until checked with an EE-aware disassembler.
