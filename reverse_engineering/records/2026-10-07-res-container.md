# 2026-10-07 — RES container investigation

## Question

Can the retail `.RES` directory and compressed payload be reconstructed from observed bytes, and does one rule hold across the full extracted corpus?

## Inputs

Private retail inputs used for analysis only:

- `SLUS_202.68` — SHA-256 `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`
- `APPSTART.RES` — SHA-256 `04eb376a507d0745925e4351903a8ef7a1024d37d8250b78892cba0c74220b89`
- `LOC.RES` — SHA-256 `b02e9c437311fd18b9dcd52c0d02222320be4eb7e5bfa17a60f564b05e6d4a0e`
- `UI/PODPHYS.RES` — SHA-256 `8361cb484ea841e1772cc0ddec2223fa923e397c1cc9a89f06ab06b1cd7ca2c8`
- `PODS/POD01/POD01.RES` — SHA-256 `08b4d7655cb796da8a29d9b9a5318c0364561c659794ac9de6c9dfed7416eca3`
- `TRACKS/TA.RES` — SHA-256 `b491e34bf6cbd27869d5b9dc8db394b101ebaf4ac7f5e0d44fcca33a00d41ab8`
- `TRACKS/TB.RES` — SHA-256 `1188206d7b1f64910c119192829fc357b9d4a9f021d64e8a2b7561f2c113a09b`
- the complete extracted RES corpus supplied privately in the PODS, TRACKS, UI and AUDIO directory bundles

Retail payloads are not committed.

## Tools

- Python 3 runtime for structural parsing, zlib verification and SHA-256 comparison
- GNU `readelf` / Binutils for ELF metadata
- LLVM `llvm-objdump` generic MIPS disassembly for static address checks

The generic LLVM backend does not decode every R5900 instruction correctly. Only standard instructions used by the claims below are relied on.

## VERIFIED — full outer-container structural pass

A parser derived from the file bytes was run over all **103** extracted retail `.RES` files.

Result: **103 passed / 0 failed**.

The pass validated:

- version 3 in every file;
- `+0x08 == 0x340` and `+0x0c == 0` in every file;
- `+0x04 == (+0x10) + 0x0c` in every file;
- the u16 chunk-length table and zero terminator;
- exact declared resource-directory lengths;
- NUL-terminated ASCII resource names;
- 24-bit little-endian resource offsets scaled by `0x100`;
- 34,128 resource records, all beginning on `0x6000` virtual boundaries;
- 44,861 zlib chunks, each decoding to exactly `0x6000` bytes;
- a `0xff` separator after every compressed chunk;
- resource ranges staying inside the reconstructed virtual stream;
- no overlapping resource ranges;
- no unexplained trailing bytes after the final chunk.

## VERIFIED — representative counts

- `APPSTART.RES`: 6 resources / 31 chunks / payload at `0x11b`
- `LOC.RES`: 10 resources / 10 chunks / payload at `0x178`
- `UI/PODPHYS.RES`: 23 resources / 23 chunks / payload at `0x32c`
- `PODS/POD01/POD01.RES`: 96 resources / 115 chunks / payload at `0xe0f`
- `TRACKS/TA.RES`: 383 resources / 533 chunks / payload at `0x3829`
- `TRACKS/TB.RES`: 1,465 resources / 1,556 chunks / payload at `0xe101`

## VERIFIED — pod physics copies

The 23 `.phy` files in `UI/PODPHYS.RES` were reconstructed from the virtual stream and compared by SHA-256 against the `.phy` file embedded in each matching `PODS/PODxx/PODxx.RES` container.

Result: **23/23 byte-identical matches**.

This establishes that the consolidated pod-physics bundle and the pod-local copies duplicate the same logical `.phy` data in this build.

## OBSERVED — executable loader

The executable string at file offset `0x289370` maps to virtual address `0x003892f0` and begins the `LoadResourceFile` diagnostic cluster. Cross-references place those diagnostics inside the routine at `0x0012cea0..0x0012dca0`.

Important code anchors include:

- `0x0012d330` — read-error diagnostic
- `0x0012d370` — wrong-version diagnostic
- `0x0012d5cc` — comparison with `0x6000`
- `0x0012d740` — add `0x6000` to the active buffer boundary

The loader therefore independently supports the `0x6000` block behavior found by the corpus parser.

## OPEN

- semantic names for header fields `+0x08` and `+0x0c`
- exact purpose of `+0x04` beyond its corpus-wide arithmetic relationship
- precise helper-function names in the loader
- version-2 layout differences
- runtime cache/lifetime behavior
- error handling for malformed chunk sizes, names and offsets under the retail executable

## Next test

Use the recovered directory to follow one `POD01.RES` geometry/material chain and `UI/PODPHYS.RES` physics entry into their executable consumers, then challenge the same rules with `TA.RES` and `TB.RES` runtime loads.
