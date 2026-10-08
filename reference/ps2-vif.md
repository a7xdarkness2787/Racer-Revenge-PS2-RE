# PlayStation 2 VIF UNPACK reference

This note records the public VIF bit definitions used when interpreting Racer Revenge PSG packets.

## Public reference

PS2SDK defines the UNPACK immediate field as:

- bits 0..9: VU address
- bit 14: USN
- bit 15: FLG

PS2SDK's packet2 helper describes:

- USN = 0: signed source values are sign-extended
- USN = 1: unsigned source values are zero-extended
- FLG = 1: VIF1_TOPS is added to the UNPACK address for double-buffered addressing

References:

- https://ps2dev.github.io/ps2sdk/vif__codes_8h.html
- https://ps2dev.github.io/ps2sdk/packet2__vif_8h_source.html
- https://ps2dev.github.io/ps2sdk/group__packet2__vif.html

## Racer Revenge observation

In the current 881-PSG POD01/TA/TB sample:

- batch-header V4-32 UNPACKs: FLG=1, USN=0 — 18,965 / 18,965
- position UNPACKs: FLG=1, USN=0 — 18,965 / 18,965
- V3-8 normal streams: FLG=1, USN=0 — 18,965 / 18,965
- V2-16 coordinate streams: FLG=1, USN=0 — 18,965 / 18,965
- optional V4-8 streams: FLG=1, USN=1 — 17,787 / 17,787

Therefore the previously observed destination sequence 0, 1, 1+N, 1+2N, 1+3N is TOPS-relative rather than an absolute VU-memory address sequence.

The V4-8 source must be decoded as unsigned bytes under VIF semantics. Its higher-level interpretation remains color-like until material/render-state correlation is complete.
