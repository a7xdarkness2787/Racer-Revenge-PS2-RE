# PSG VIF payload investigation — 2026-10-07

**Canonical executable:** `SLUS_202.68`  
**SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`  
**Status:** VERIFIED sample structure / OBSERVED executable linkage  
**Confidence:** high for the first payload block; medium for higher-level mesh semantics

## Question

What begins immediately after the already verified PSG hierarchy/material tables, and is the remaining data genuinely PlayStation 2 VIF command data rather than an ordinary PC-style vertex/index stream?

## Private inputs

The investigation used canonical retail files kept outside Git:

- `PODS/POD01/POD01.RES`
  - SHA-256 `08b4d7655cb796da8a29d9b9a5318c0364561c659794ac9de6c9dfed7416eca3`
- `TRACKS/TA.RES`
  - SHA-256 `b491e34bf6cbd27869d5b9dc8db394b101ebaf4ac7f5e0d44fcca33a00d41ab8`
- `TRACKS/TB.RES`
  - SHA-256 `1188206d7b1f64910c119192829fc357b9d4a9f021d64e8a2b7561f2c113a09b`
- `SLUS_202.68`
  - canonical hash above

Those three RES containers expose **881 PSG resources** in the current sample.

## VERIFIED — first payload block

For every one of the 881 sampled PSG resources, the first bytes after the fixed hierarchy/material region obey the same outer rule:

```text
+0x00  0x40-byte descriptor
+0x40  VIF packet
```

Within the 0x40-byte descriptor:

```text
+0x3c  u32 vif_packet_size
```

The packet size is 16-byte aligned and places the packet end inside the PSG resource in all 881 files.

File behavior in this three-container sample:

- 687 PSG files end exactly at the end of this first descriptor + VIF packet
- 7 have exactly 16 bytes after it
- 187 contain additional payload structures after it

The additional structures are not yet assigned stable semantics.

## VERIFIED — VIF command stream

The first u32 at the start of every sampled VIF packet is:

```text
0x6c018000
```

Using the standard PS2 VIFcode field layout this is an UNPACK-family command with:

- command byte `0x6c`
- NUM `1`
- immediate `0x8000`

The next command after its 16-byte source payload is always another UNPACK command from the same observed geometry sequence.

A bounded decoder consumed every first VIF packet in all 881 sampled PSGs without encountering an unknown command or overrunning the descriptor-declared packet size.

Observed command bytes across those first packets are limited to:

| Command | Current interpretation |
| ---: | --- |
| `0x00` | NOP/padding |
| `0x17` | MSCNT |
| `0x65` | UNPACK V2-16 |
| `0x6a` | UNPACK V3-8 |
| `0x6c` | UNPACK V4-32 |
| `0x6d` | UNPACK V4-16 |
| `0x6e` | UNPACK V4-8 |

Observed command counts in the 881 first packets:

- `0x6c`: 12,462
- `0x6d`: 12,250
- `0x6a`: 12,356
- `0x65`: 12,356
- `0x6e`: 11,710
- `0x17`: 12,356
- `0x00`: 1,193

A common draw-batch pattern is:

```text
UNPACK V4-32
UNPACK V4-16
UNPACK V3-8
UNPACK V2-16
UNPACK V4-8
MSCNT
```

Not every batch contains every UNPACK family, so this is a recurring pattern rather than a universal fixed record.

## VERIFIED — executable-side VIF construction

The executable contains a strong independent PS2 rendering anchor around `0x002469c0`.

At `0x00246a58..0x00246a9c`, code writes a small VIF packet into memory. Among the emitted words is:

```text
0x6c018000 | value
```

followed by four floating-point words.

The exact base constant `0x6c018000` is the same first VIF command found in all 881 sampled PSG first packets.

This establishes a direct connection between the serialized PSG payload and the game's Emotion Engine/VIF-side geometry path.

## OBSERVED — PSXSurfaceGeometry ownership

The executable contains RTTI/type metadata for `PSXSurfaceGeometry`. A related table at approximately `0x003d20c0` points into the `0x00246260..` implementation family.

The helper at `0x00246300` is called from the surface-geometry load path at `0x0026e34c` and performs file reads, allocation/alignment and PS2 packet preparation. Its full serialized-field contract is still being separated from surrounding higher-level geometry data.

## Interpretation

The PSG payload is now proven to contain executable VIF command streams. It should no longer be described merely as an unknown PS2-specific blob.

What is **not** yet closed:

- the semantic names of the other fields in the 0x40 descriptor;
- how later payload structures relate to hierarchy objects;
- exact vertex/normal/UV/color meaning of each UNPACK stream;
- material assignment per draw batch;
- VU microprogram identity and expected VU memory layout;
- GIF/GS state generated after MSCNT;
- the meaning of the extra 16-byte tails seen in seven sampled PSGs.

## Reproduction

Use `scripts/psg_vif_inspect.py` on a user-supplied extracted PSG resource.

The script:

1. verifies the existing fixed PSG tables;
2. locates the first payload descriptor;
3. validates the descriptor's packet size;
4. walks the first VIF packet command-by-command;
5. reports source-byte lengths and remaining payload.

No retail PSG payload is stored in Git.

## Next

- identify the remaining 0x40 descriptor fields by correlating them against command counts and executable reads;
- split the 187 multi-block sample files into their additional serialized records;
- map UNPACK destinations to VU memory usage;
- identify material indices around batch boundaries;
- correlate one POD01 render object with its matching COL bounds.
