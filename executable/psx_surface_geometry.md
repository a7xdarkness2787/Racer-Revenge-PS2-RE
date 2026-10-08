# PSXSurfaceGeometry executable map

**Build:** North American retail `SLUS_202.68`  
**SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

Status: **OBSERVED / address-backed**.

## Type ownership

The executable contains `PSXSurfaceGeometry` type metadata. A related virtual-function table is anchored around `0x003d20c0` and points into the `0x00246260..` implementation family.

The exact inheritance and every virtual slot have not yet been named.

## Serialized packet helper

`0x00246300`

This helper is called from the surface-geometry load path at `0x0026e34c`.

The routine performs repeated file reads, allocation, 16-byte size alignment and packet-buffer construction. It is part of the PS2-specific serialized geometry path rather than the generic hierarchy/material-name reader.

Because several R5900 register-transfer instructions are not decoded reliably by generic LLVM MIPS output, the complete field-by-field calling convention remains open.

## VIF packet construction

A separate PS2 geometry path around `0x002469c0` constructs VIF data in memory.

At `0x00246a58..0x00246a9c`, it emits words including:

```text
0x11000000
0x03000000
0x02000000
0x6c018000 | value
<float>
<float>
<float>
<float>
```

The constant `0x6c018000` is significant because every first VIF packet in the current 881-PSG POD01/TA/TB sample begins with exactly `0x6c018000`.

That gives direct executable support for interpreting the PSG payload as VIF command data.

## Related generic SurfaceGeometry code

The higher-level create/load path remains around `0x0026e820`.

Known helpers:

- `0x0026e640` — material-name table reader
- `0x0028cac0` — hierarchy descriptor reader
- `0x0026e34c` — call into the PS2-specific serialized packet helper at `0x00246300`

## Open work

- identify every field consumed by `0x00246300`;
- identify the owner/object type passed to the helper;
- map the 0x40 PSG payload descriptor fields to runtime fields;
- map VIF UNPACK destinations to VU memory semantics;
- identify the VU microprogram and GIF/GS submission path;
- distinguish file-owned packet bytes from runtime-generated DMA/VIF wrappers.
