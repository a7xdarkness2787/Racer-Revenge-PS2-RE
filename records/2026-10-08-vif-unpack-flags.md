# 2026-10-08 — VIF UNPACK control-bit validation

## Question

Are the recovered PSG attribute streams signed or unsigned, and are their UNPACK destinations absolute or relative to the VIF1 double-buffer base?

## Public specification

PS2SDK's UNPACK helpers define:

- immediate bits 0..9 as the VU address
- bit 14 as USN
- bit 15 as FLG
- USN=0 sign-extends source values
- USN=1 zero-extends source values
- FLG=1 adds VIF1_TOPS to the address

See `reference/ps2-vif.md`.

## VERIFIED — complete detailed sample

Across all 18,965 geometry batches in the 881-file POD01/TA/TB sample:

| Stream | Count | FLG | USN |
| --- | ---: | ---: | ---: |
| V4-32 batch header | 18,965 | 1 | 0 |
| position | 18,965 | 1 | 0 |
| V3-8 normal | 18,965 | 1 | 0 |
| V2-16 coordinate | 18,965 | 1 | 0 |
| optional V4-8 | 17,787 | 1 | 1 |

Failures: 0.

This sharpens two earlier findings:

1. the contiguous UNPACK ADDR values are **VIF1_TOPS-relative**, not absolute VU addresses;
2. the optional V4-8 stream is **unsigned byte data** under VIF semantics.

The existing signed position, normal and V2-16 decoders agree with USN=0.

## OBSERVED — material-block flag correlation

Across all 1,216 sampled material blocks:

- flag bit `0x8` is set if and only if a V4-8 stream is present
- failures: 0

The two observed full flag values remain:

- `0x00ff010f` — 1,162 blocks, V4-8 present
- `0x00000107` — 54 blocks, V4-8 absent

This is strong evidence that bit `0x8` advertises the optional V4-8 attribute. The meanings of the remaining bits and the `0xff` field remain open.

## V4-8 value range

Decoded as unsigned bytes across 234,318 sampled V4-8 records:

- channel maxima: 127, 127, 127, 79
- channel minima: 0, 0, 0, 0

The stream remains described as color-like rather than definitively named RGBA until it is tied to the material/GS path.

## Correction

Earlier documentation described the destination sequence as VU addresses 0, 1, and so on. The numerical ADDR fields were correct, but the wording was incomplete: FLG=1 means those ADDR fields are relative to VIF1_TOPS.

Stable documentation now uses TOPS-relative terminology.
