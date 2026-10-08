# PSG VIF payload investigation — 2026-10-07

**Canonical executable:** `SLUS_202.68`  
**SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`  
**Status:** VERIFIED sample structure / OBSERVED executable linkage  
**Confidence:** high for the first payload block and batch grammar; medium for higher-level mesh semantics

## Question

What begins immediately after the verified PSG hierarchy/material tables, and how is the geometry staged into PS2 VIF/VU memory?

## Private inputs

Canonical retail files kept outside Git:

- `PODS/POD01/POD01.RES` — `08b4d7655cb796da8a29d9b9a5318c0364561c659794ac9de6c9dfed7416eca3`
- `TRACKS/TA.RES` — `b491e34bf6cbd27869d5b9dc8db394b101ebaf4ac7f5e0d44fcca33a00d41ab8`
- `TRACKS/TB.RES` — `1188206d7b1f64910c119192829fc357b9d4a9f021d64e8a2b7561f2c113a09b8`
- `SLUS_202.68` — canonical executable hash above

The three RES containers expose **881 PSG resources**.

## VERIFIED — first payload block

Every sampled PSG begins its post-table payload with:

```text
+0x00  descriptor[0x40]
+0x40  VIF packet
```

Descriptor `+0x3c` is the byte size of the following VIF packet.

All 881 packet sizes are:

- nonzero;
- 16-byte aligned;
- fully in bounds.

After the first descriptor + packet:

- 687 PSGs end exactly;
- 7 have exactly 16 additional bytes;
- 187 contain larger additional structures.

Those later structures are still open.

## VERIFIED — first VIF command

All 881 first packets begin with:

`0x6c018000`

Using the standard VIFcode layout this is an UNPACK V4-32 command with NUM=1 and immediate/address field `0x8000`.

Executable code at `0x00246a58..0x00246a9c` independently constructs VIF data using the same `0x6c018000` base constant.

## VERIFIED — batch grammar

The first packets contain **12,356 MSCNT-terminated batches**.

The 16-byte payload of the first V4-32 UNPACK in every batch is:

```text
u32 0x8000 | N
u32 0x30024000
u32 0x00000412
u32 0x00000000
```

where `N` exactly equals the element count of the following position UNPACK.

Across all 12,356 batches:

- `N` ranges from 3 to 16;
- the sum of batch element counts is 164,585;
- the low 15 bits of the first header word equal `N` in 12,356 / 12,356 cases.

Three batch forms occur:

### Compressed positions + color

**11,710 batches**

```text
UNPACK V4-32  count 1   -> VU addr 0
UNPACK V4-16  count N   -> VU addr 1
UNPACK V3-8   count N   -> VU addr 1 + N
UNPACK V2-16  count N   -> VU addr 1 + 2N
UNPACK V4-8   count N   -> VU addr 1 + 3N
MSCNT
```

### Compressed positions without color

**540 batches**

```text
UNPACK V4-32  count 1   -> VU addr 0
UNPACK V4-16  count N   -> VU addr 1
UNPACK V3-8   count N   -> VU addr 1 + N
UNPACK V2-16  count N   -> VU addr 1 + 2N
MSCNT
```

### 32-bit positions without color

**106 batches**

```text
UNPACK V4-32  count 1   -> VU addr 0
UNPACK V4-32  count N   -> VU addr 1
UNPACK V3-8   count N   -> VU addr 1 + N
UNPACK V2-16  count N   -> VU addr 1 + 2N
MSCNT
```

The UNPACK destinations are contiguous for **12,356 / 12,356** batches under the one-VU-vector-per-element interpretation.

That strongly supports the current attribute interpretation:

- first per-element stream: position-like data;
- second: 3-component byte data, consistent with normal-like data;
- third: 2-component 16-bit data, consistent with UV-like data;
- optional fourth: 4-component byte data, consistent with color-like data.

The serialized widths and destinations are verified. The semantic names remain **INFERRED** until they are checked against decoded geometry and runtime/VU behavior.

## VERIFIED — command population

Across the sampled first packets:

- `0x6c`: 12,462
- `0x6d`: 12,250
- `0x6a`: 12,356
- `0x65`: 12,356
- `0x6e`: 11,710
- `0x17`: 12,356
- `0x00`: 1,193

No other VIF command byte is needed to consume the first packet set.

## OBSERVED — PSXSurfaceGeometry executable ownership

The executable contains `PSXSurfaceGeometry` type metadata and a related virtual table around `0x003d20c0`.

The helper at `0x00246300` is called by the surface-geometry load family at `0x0026e34c` and performs file reads, alignment/allocation, and PS2 packet preparation.

Generic LLVM output does not decode every R5900 instruction, so field semantics that depend on those instructions remain intentionally unnamed.

## Interpretation

This closes the question of whether the first PSG payload is opaque arbitrary geometry data: it is a structured VIF upload stream arranged in repeated VU-memory batches.

It does **not** yet prove:

- primitive topology;
- whether the V4 position component is always homogeneous W or another packed field;
- exact normal/UV/color scaling;
- material selection per batch;
- VU microprogram behavior;
- GIF/GS state emitted after MSCNT;
- ownership of later payload structures.

## Reproduction

Use `scripts/psg_vif_inspect.py` on user-supplied PSG resources. The raw aggregate sample result is retained in `raw/2026-10-07-psg-vif-summary.txt`.

## Next

- decode position scaling for V4-16 batches and compare against V4-32 cases;
- identify primitive topology from batch ordering/output;
- correlate PSG vertex bounds with a matching POD01 COL object;
- locate material selection around each MSCNT batch;
- identify the VU microprogram reached by MSCNT;
- split the later payload structures in the 194 nontrivial sample files.
