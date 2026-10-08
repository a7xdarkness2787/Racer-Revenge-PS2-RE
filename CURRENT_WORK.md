# Current Work

## Active investigation

Continue decoding PSG render payloads now that the first PS2 VIF block is verified, then connect draw batches to hierarchy objects, materials and collision geometry.

## Latest development

A canonical sample of **881 PSG files** from POD01, TA and TB now has a verified first post-table render block:

```text
0x40-byte descriptor
VIF packet
```

Descriptor `+0x3c` is the byte size of the following first VIF packet.

Every sampled first packet:

- is 16-byte aligned and in bounds;
- begins with `0x6c018000`;
- can be walked command-by-command with the current VIF decoder.

Observed command families are V4-32, V4-16, V3-8, V2-16 and V4-8 UNPACK plus MSCNT and NOP/padding.

Executable code at `0x00246a58..0x00246a9c` independently constructs VIF data using the same `0x6c018000` command constant.

The generic surface loader calls the PS2-specific packet helper `0x00246300` from `0x0026e34c`.

## Current evidence

- `formats/PSG.md`
- `analysis/2026-10-07-psg-vif-payload.md`
- `executable/psx_surface_geometry.md`
- `scripts/psg_vif_inspect.py`
- `raw/2026-10-07-psg-vif-summary.txt`

## Immediate queue

- identify the remaining 0x40 descriptor fields;
- parse the additional structures in the 194 sampled PSGs that continue after the first packet;
- map VIF UNPACK destinations to VU memory;
- locate material indices around batch boundaries;
- identify the VU microprogram and GIF/GS submission path;
- correlate one POD01 render object with its corresponding COL resource;
- decode the s16 collision vertex dequantization path;
- begin a retained PCSX2 runtime capture once draw-object addresses are stable.

## Documentation contract

Every meaningful development is recorded in the same work cycle according to `UPDATE_PROTOCOL.md`.
