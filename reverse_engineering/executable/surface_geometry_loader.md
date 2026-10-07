# Surface geometry loader map

Build: North American retail `SLUS_202.68`

Status: **OBSERVED / address-backed** for the PSG fixed header and hierarchy/material tables.

Relevant executable strings include:

- `.psg`
- `psg`
- `dxg`
- `PSXSurfaceGeometry`
- `SurfaceGeometry`
- `SurfaceGeometry.cpp`
- `%s is not in the material table`
- `Create: %s invalid file (version (%d) wrong or format (%s) is not psg or dxg)`

## Create / format validation

The large create path beginning at approximately `0x0026e820` constructs the requested geometry filename, opens it and validates its format/version.

At `0x0026ebcc..` it reads two four-byte header words. The first is compared against the format strings `pgi`, `dgi`, `psg` and `dxg`. The second is the version value.

The retail PSG corpus uses format `psg` and version 3.

## Hierarchy descriptor reader

`0x0028cac0`

This routine matches the fixed PSG descriptor table independently recovered from the files.

It first reads a four-byte object count into runtime object offset `+0x1a0`.

For each object it then reads:

| Code area | Serialized bytes | Runtime destination |
| --- | ---: | --- |
| `0x0028cb50..` | `0x80` | object name at `+0x38` |
| `0x0028cb70..` | `0x40` | 4x4 matrix at `+0xc0` |
| `0x0028cbf4..` | `0x0c` | vec3 at `+0x140` |
| `0x0028cc04..` | `0x0c` | vec3 at `+0x150` |
| `0x0028cc24..` | `0x04` | float at `+0x194` |
| `0x0028cc44..` | `0x04` | parent index retained for hierarchy construction |

After all descriptors are read, the routine walks the parent indices. `-1` is treated as the root/no-parent value. Other values select an earlier object, and the code links runtime parent/child/sibling pointers.

This executable behavior confirms the 0xe0 serialized descriptor stride and the parent-index interpretation.

## Material-name reader

`0x0026e640`

This helper reads a four-byte material count into runtime offset `+0x1c0`, allocates an array at `+0x1c4`, and then loops over fixed 0x40-byte names.

Each name is resolved through the material system before its handle/pointer is stored.

This matches the independently derived table:

```text
u32 material_count
char material_name[material_count][0x40]
```

## Remaining payload

After the material-name helper returns, the create path dispatches into platform-specific geometry handling through a virtual call. That payload contains PS2-specific render data and is not yet fully decoded.

Work on the payload should distinguish:

- serialization boundaries
- VIF/VU/GIF/DMA command data
- material references
- mesh/strip boundaries
- vertex attributes

rather than assuming a conventional PC-style indexed mesh layout.

## R5900 caution

As with the collision work, generic LLVM MIPS output does not understand every Emotion Engine instruction. The fixed-size reads, constants, branches, offsets and string references described above are unambiguous; vector-operation semantics remain open where the disassembler is not reliable.
