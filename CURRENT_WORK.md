# Current Work

## Active investigation

Decode the PS2-specific PSG payload beyond the already verified hierarchy and material tables, then correlate visible geometry with collision and pod/track structures.

## Current evidence base

- RES container loader: `0x0012cea0..0x0012dca0`
- collision dispatcher: `0x00124f80`
- pod configuration loader: `0x002146c0`
- PSG create/validation path: around `0x0026e820`
- PSG material reader: `0x0026e640`
- PSG hierarchy reader: `0x0028cac0`
- TunnelTrack spline loader: `0x002a1260..0x002a1d70`

The fixed PSG region is known exactly:

```text
psg\0
u32 version
u32 object_count
object_count * 0xe0 hierarchy descriptors
u32 material_count
material_count * 0x40 material names
PS2 geometry payload
```

Across 9,917 retail PSG files there are 17,942 hierarchy objects and 22,175 material-name records.

## Immediate queue

- determine the first PSG payload record structure;
- determine how geometry payload records map to hierarchy objects;
- identify material references inside payload records;
- identify VIF/VU/GIF/DMA boundaries rather than assuming a PC-style mesh layout;
- correlate one pod PSG object's transform/bounds with its matching COL component;
- decode the s16 collision-vertex dequantization path;
- retain an Emotion Engine-aware disassembly where generic LLVM decoding is insufficient;
- begin a PCSX2 runtime capture once geometry object addresses are stable.

## Documentation contract

A meaningful development is not complete until it has been recorded in the appropriate stable subsystem document and the same work cycle updates any affected current-state files.

Detailed research history belongs in `records/` or `analysis/`; current state belongs here and in `STATUS.md`.

See `UPDATE_PROTOCOL.md`.
