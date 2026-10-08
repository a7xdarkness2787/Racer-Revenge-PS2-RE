# Current Work

## Active investigation

Turn the newly verified PSG VIF batch layout into independently reconstructed geometry and identify the VU/material path.

## Latest development

The 881-file POD01/TA/TB PSG sample contains **12,356 MSCNT-terminated VIF geometry batches**.

Each batch begins with a single V4-32 upload to VU address 0 whose four words are:

```text
0x8000 | N
0x30024000
0x00000412
0x00000000
```

`N` exactly matches the following element count.

All 12,356 batches then lay their per-element streams contiguously in VU memory.

Most use V4-16 positions; 106 batches use V4-32 positions. Every batch also carries V3-8 and V2-16 streams, and 11,710 carry an additional V4-8 stream.

The position/normal/UV/color semantic mapping is currently inferred from stream shape and layout rather than promoted as final fact.

## Current evidence

- `formats/PSG.md`
- `analysis/2026-10-07-psg-vif-payload.md`
- `executable/psx_surface_geometry.md`
- `scripts/psg_vif_inspect.py`
- `raw/2026-10-07-psg-vif-summary.txt`

## Immediate queue

- derive V4-16 position dequantization and compare against V4-32 batches;
- determine primitive topology;
- calculate decoded bounds and compare with PSG descriptor/COL bounds;
- identify material selection around MSCNT boundaries;
- locate the VU microprogram reached by the geometry batches;
- decode later records in the 194 sampled PSGs that continue beyond the first packet;
- start runtime capture after a stable geometry object can be reconstructed.

## Documentation contract

Every meaningful development is recorded in the same work cycle according to `UPDATE_PROTOCOL.md`.
