# RES container format

Status: **OBSERVED / partially VERIFIED** for the North American retail build (`SLUS_202.68`).

The outer `.RES` container is now structurally decoded across the complete extracted retail corpus. This note describes only fields demonstrated by the files and the executable. Unknown header semantics remain deliberately unnamed.

## Corpus result

The current parser was run against all **103** extracted `.RES` files. All 103 passed the same structural checks:

- version `3`
- header field `+0x08 == 0x340`
- header field `+0x0c == 0`
- a zero-terminated table of compressed chunk byte lengths
- zlib-compressed chunks that each expand to exactly `0x6000` bytes
- one `0xff` byte after every compressed chunk
- a resource directory whose declared byte length matches exactly
- no resource range outside the reconstructed virtual stream
- no unexplained bytes after the final chunk

Across the corpus this accounts for **34,128 directory records** and **44,861 compressed chunks**. Every observed logical resource offset is aligned to `0x6000`. No overlapping logical resource ranges were found.

The largest directory in the current corpus is `TRACKS/TB.RES` with 1,465 resource records. It contains 1,556 compressed chunks.

## Version 3 layout

All integer values below are little-endian.

| Offset | Size | Observed meaning |
| --- | ---: | --- |
| `+0x00` | 4 | version; `3` in all 103 retail containers |
| `+0x04` | 4 | unknown header-span field; always `chunk_table_bytes + 0x0c` in the retail corpus |
| `+0x08` | 4 | unknown; `0x340` in all 103 retail containers |
| `+0x0c` | 4 | unknown; `0` in all 103 retail containers |
| `+0x10` | 4 | byte length of the u16 chunk-length table, including its terminating zero |
| `+0x14` | variable | u16 compressed sizes, followed by a zero u16 terminator |
| after table | 4 | resource count |
| next | 4 | resource-directory byte length |
| next | variable | packed resource directory |
| after directory | variable | concatenated compressed chunks |

The current evidence does not justify names for the two constant header fields at `+0x08` and `+0x0c`.

## Directory records

The directory contains exactly the declared resource count. Records are packed and are not padded to four-byte boundaries.

Each record is:

```text
u32 name_length
u8  name[name_length]     ASCII, length excludes terminator
u8  zero_terminator       must be 0
u24 offset_units          little-endian
u32 logical_size
```

The logical resource byte offset is:

```text
offset = offset_units * 0x100
```

Every retail record inspected lands on a `0x6000` boundary. Resources may span multiple decoded chunks; the stored `logical_size` selects only the meaningful bytes from the virtual stream.

## Compressed payload

The u16 table contains the byte length of each zlib stream. The final zero u16 is a table terminator and is not a chunk.

For each chunk:

1. read exactly the u16 compressed byte count;
2. zlib-decompress it;
3. require exactly `0x6000` output bytes;
4. consume a single `0xff` separator byte.

The chunks are concatenated in decoded form to create the virtual data space addressed by directory records.

For the 103-file retail corpus, the last `0xff` separator is also the final byte of the container. No trailing data remains.

## Representative containers

| Container | Resources | Chunks | First payload offset |
| --- | ---: | ---: | ---: |
| `APPSTART.RES` | 6 | 31 | `0x11b` |
| `LOC.RES` | 10 | 10 | `0x178` |
| `UI/PODPHYS.RES` | 23 | 23 | `0x32c` |
| `PODS/POD01/POD01.RES` | 96 | 115 | `0xe0f` |
| `TRACKS/TA.RES` | 383 | 533 | `0x3829` |
| `TRACKS/TB.RES` | 1,465 | 1,556 | `0xe101` |

## Embedded resource families

The 34,128 directory records expose a much larger internal corpus than the disc-level extension counts. The most common embedded extensions currently observed are:

- 9,917 `.psg`
- 6,545 `.mot`
- 6,448 `.psm`
- 5,281 `.pst`
- 2,505 `.col`
- 798 `.mcf`
- 661 `.emt`
- 629 `.vut`
- 424 `.vub`
- 213 `.ini`
- 135 `.tga`
- 132 `.atm`
- 46 `.phy`
- 26 `.spl`

These counts establish container contents, not the semantics of the embedded formats.

## Pod physics duplication

`UI/PODPHYS.RES` contains 23 `.phy` resources, one for each pod represented in the POD directories. Each of those 23 logical files is also present inside the corresponding `PODS/PODxx/PODxx.RES` bundle.

A byte-for-byte SHA-256 comparison of the extracted logical resources found **23/23 matches**. The consolidated physics bundle and the pod-local copies therefore carry identical `.phy` payloads in this retail build.

## Executable anchor

The executable contains a strong `LoadResourceFile` candidate at `0x0012cea0..0x0012dca0`. This function is anchored by multiple in-function diagnostic string references, including the read-error, version-error and `LoadResourceFile` assertion text in `DataAccess.cpp`.

Relevant static observations:

- `0x0012d33c..0x0012d37c` validates a resource-file version and accepts the observed version 3 path; version 2 has a separate branch.
- `0x0012d5cc` compares a decoded/read amount against `0x6000`.
- `0x0012d740` advances a buffer pointer by `0x6000`.
- the function uses the `rb` mode string while opening the resource file.

LLVM's generic MIPS disassembler does not understand every R5900 instruction in this routine. Unknown instructions remain unnamed until checked with an Emotion Engine-aware disassembler.

## Tool

`reverse_engineering/scripts/res_inspect.py` implements the observed v3 structure, validates boundaries and chunk separators, reconstructs the virtual stream, and can extract logical resources supplied by the user at runtime.

The parser intentionally rejects unsupported versions and unexplained trailing bytes rather than silently accepting them.
