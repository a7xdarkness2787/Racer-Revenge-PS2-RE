# PSXSurfaceGeometry executable map

**Build:** North American retail `SLUS_202.68`  
**SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

Status: **OBSERVED / address-backed**, with serialized behavior independently validated from PSG payloads.

## Type ownership

The executable contains `PSXSurfaceGeometry` type metadata. A related virtual-function table is anchored around `0x003d20c0` and points into the `0x00246260..` implementation family.

The exact inheritance and every virtual slot have not yet been named.

## PS2 serialized packet helper

`0x00246300`

This helper is called from the higher-level SurfaceGeometry load family at `0x0026e34c`.

The surrounding code performs repeated file reads, allocation/alignment and PS2 packet preparation. The independently recovered 881-file payload sample now shows that the serialized data being consumed consists of:

- a render header
- LOD groups
- material/VIF blocks
- VIF geometry batches
- an optional multi-object remap tail

The exact register-level correspondence for every serialized field remains open because generic LLVM MIPS output does not decode all R5900 instructions reliably.

## VIF packet construction

A PS2 geometry path around `0x002469c0` constructs VIF data in memory.

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

The `0x6c018000` base word independently matches the per-batch V4-32 header upload recovered from serialized PSG packets.

The sampled PSG stream now establishes 18,965 MSCNT-terminated batches, with V4-16 or V4-32 position streams followed by V3-8, V2-16 and optional V4-8 streams.

## Related generic SurfaceGeometry code

- around `0x0026e820` — higher-level create/open/format-validation path
- `0x0026e640` — material-name table reader
- `0x0028cac0` — hierarchy descriptor reader
- `0x0026e34c` — call into PS2-specific helper `0x00246300`

Fresh disassembly of the `0x0026e180..0x0026e380` region confirms nested serialized-data loops and the direct call to `0x00246300`. R5900-only operations in that region remain intentionally unnamed until checked with an Emotion Engine-aware disassembler.

## Current executable frontier

- identify the VU microprogram reached by MSCNT
- correlate the 0x24 render header and 0x14 material block fields with specific reads in `0x00246300`
- identify material/render-state setup around each VIF packet
- locate GIF/GS submission generated from the uploaded VU data
- determine the runtime use of the multi-object remap tail
- determine the exact LOD comparison metric
