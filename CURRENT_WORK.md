# Current Work

## Active investigation

Move from fully parsed PSG serialization into assembled hierarchy transforms and the VU/material/GIF/GS execution path.

## Latest development

Detailed PSG validation is now complete across all **9,917** retail PSG resources.

The complete corpus confirms:

- 0x24-byte render header
- one or four LOD groups
- 0x14-byte material-block headers
- exactly four VIF geometry batch grammars
- signed V4-16/V4-32 position decoding
- per-vertex hierarchy transform indices in W magnitude
- strip seed/restart state in W sign
- signed V3-8 and V2-16 streams
- unsigned optional V4-8 stream
- identity remap tails on every multi-object file
- no unexplained payload bytes

The corrected sign-only strip rule reconstructs **3,124,861 triangles** with zero topology warnings.

A previous same-transform restriction was invalidated by full-corpus cutscene/rider/cable geometry. Mixed-transform triangles are valid serialized geometry.

## Current evidence

- `formats/PSG.md`
- `analysis/2026-10-08-psg-full-corpus.md`
- `records/2026-10-08-psg-full-corpus.md`
- `raw/2026-10-08-psg-full-corpus-summary.txt`
- `scripts/psg_mesh_extract.py`
- `scripts/psg_corpus_verify.py`
- `reference/ps2-vif.md`
- `executable/psx_surface_geometry.md`

## Immediate queue

- determine hierarchy matrix multiplication/order for transform-indexed vertices
- reconstruct an articulated rider/cutscene model in bind pose
- identify the VU microprogram reached by MSCNT
- map the material-block `+0x08` float
- determine the runtime metric compared with the pod LOD thresholds
- tie V2-16 coordinates directly to material/texture state
- identify V4-8 channel semantics
- trace GIF/GS output
- start a retained PCSX2 runtime capture once the hierarchy/VU path is stable

## Documentation contract

Every meaningful development is recorded in the same work cycle according to `UPDATE_PROTOCOL.md`.
