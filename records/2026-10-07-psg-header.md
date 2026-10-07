# 2026-10-07 — PSG fixed-table investigation

## Question

Can the 9,917 embedded `.psg` resources be given a reproducible top-level structure before decoding the PS2 geometry command payload?

## VERIFIED — complete corpus

A fixed-table parser was run over all **9,917** retail PSG resources.

Result: **9,917 passed / 0 failed**.

The corpus contains:

- 17,942 object descriptors
- 22,175 material-name records
- object count 1..33 per file
- material count 1..15 per file

Every file has nonempty payload after the fixed tables.

## VERIFIED — descriptor stride

The header is:

`psg\0`, version 3, object count.

The object count is followed by exactly `count * 0xe0` bytes of object descriptors.

Each 0xe0 descriptor consists of:

- 0x80-byte zero-padded ASCII name
- 16 floats
- 3 floats
- 3 floats
- 1 float
- 1 u32 parent index

All matrices have the observed affine homogeneous form.

All 17,942 names are valid NUL-terminated ASCII with zero padding.

## VERIFIED — hierarchy

`0xffffffff` is the root/no-parent value.

Across all 9,917 PSG files:

- exactly one root occurs in every file
- every non-root parent index is in range
- every non-root parent refers to an earlier descriptor
- no hierarchy cycle occurs
- maximum observed depth is 7

The executable routine at `0x0028cac0` independently reads the same field sizes and subsequently constructs parent/child/sibling links from the parent-index list.

## VERIFIED — material names

After the descriptor array is:

- u32 material count
- `material_count` fixed 0x40-byte names

All 22,175 material names are ASCII, NUL-terminated and zero-padded.

The executable helper at `0x0026e640` independently reads the same count/name table and resolves each string through the material system.

## OBSERVED — geometry payload boundary

The fixed-table end is exactly:

`0x0c + object_count*0xe0 + 4 + material_count*0x40`.

Payload sizes range from 160 to 264,432 bytes. The total remaining PSG payload across the retail corpus is 113,595,080 bytes.

The bytes after this boundary are not yet assigned a stable mesh/VIF/VU layout.

## Executable connection

The create path around `0x0026e820` recognizes `.psg`, opens the file, reads its four-byte format and version, and compares against `psg` / `dxg` and related format strings.

This ties the corpus structure to the game's actual SurfaceGeometry-family loader rather than relying only on visual byte patterns.

## Next

- determine the first payload record type and how many records belong to each object
- identify material indices inside payload records
- find VIF/VU/GIF packet boundaries
- correlate one pod PSG object's bounds and transform with its matching COL component
- render one recovered mesh independently as a format-validation test
