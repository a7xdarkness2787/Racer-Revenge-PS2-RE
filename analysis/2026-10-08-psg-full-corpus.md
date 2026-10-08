# Full PSG render-payload corpus validation — 2026-10-08

**Canonical build:** North American retail `SLUS_202.68`  
**Executable SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`  
**Status:** VERIFIED serialized structure and strip topology across the complete retail PSG corpus

## Scope

The detailed PSG parser was expanded from the POD01/TA/TB sample to every embedded PSG resource recovered from all **103 retail RES containers**.

No retail payload is committed.

## VERIFIED — complete detailed corpus

- RES containers: **103**
- PSG resources: **9,917**
- detailed payload parses: **9,917**
- failures: **0**
- unexplained payload bytes: **0**
- hierarchy descriptors: **17,942**
- material-name records: **22,175**
- material/VIF blocks: **22,175**
- VIF geometry batches: **366,935**
- submitted position records: **4,869,177**

The same RenderHeader -> LOD group -> MaterialBlock -> VIF packet -> optional remap-tail grammar applies to every retail PSG.

## VERIFIED — render header invariants

Across all 9,917 files:

- normal scale is `1/127`
- both V2-16 coordinate scales are `1/2047`
- `origin_present` is 0 or 1
- `origin_present == 1` if and only if the stored position origin is nonzero

Counts:

- zero origin / flag 0: **8,565**
- nonzero origin / flag 1: **1,352**

## VERIFIED — LOD organization

- one LOD group: **9,846 PSGs**
- four LOD groups: **71 PSGs**

The 71 four-group resources are exactly the major pod meshes:

- chariot, left engine and right engine for each of the 23 pods: 69 files
- POD02's additional left/right engine pair: 2 files

The finite thresholds are approximately:

`0.18, 0.36, 0.50, FLT_MAX`

Three files differ only by the final representable float bit for the first two constants.

## VERIFIED — material blocks and flags

The **22,175 material blocks** exactly match the **22,175 fixed material-name records**.

Only four flag values occur:

| Flags | Blocks | Object form | V4-8 stream |
| ---: | ---: | --- | --- |
| `0x00ff010f` | 18,614 | single-object | present |
| `0x00ff0107` | 318 | single-object | absent |
| `0x0000010f` | 7 | multi-object | present |
| `0x00000107` | 3,236 | multi-object | absent |

Across all 22,175 blocks:

```text
flags =
    0x00000107
  | (0x00000008 if V4-8 is present)
  | (0x00ff0000 if the PSG has one hierarchy object)
```

This is a structural decomposition, not yet a claim about the engine-facing semantic name of the `0xff` field.

Bit `0x8` is verified as the optional V4-8 attribute-presence bit.

## VERIFIED — four VIF geometry grammars

Exactly four MSCNT-terminated batch forms occur:

| Position stream | V4-8 | Batches |
| --- | --- | ---: |
| V4-16 | present | 126,732 |
| V4-16 | absent | 104,583 |
| V4-32 | present | 78,015 |
| V4-32 | absent | 57,605 |

Totals:

- V4-16 position batches: **231,315**
- V4-32 position batches: **135,620**
- all batches: **366,935**

Every geometry UNPACK uses FLG=1, making its ADDR field VIF1_TOPS-relative.

Header, position, V3-8 and V2-16 streams use USN=0. Optional V4-8 uses USN=1.

## VERIFIED — optional V4-8 range

The full corpus contains **2,709,497** V4-8 records.

Each of the four unsigned channels reaches the full observed range **0..255** somewhere in the corpus.

The serialization and unsigned interpretation are verified. The higher-level channel meaning remains under investigation.

## VERIFIED — remap tail

- single-object PSGs: **8,882**
- multi-object PSGs: **1,035**

All 1,035 multi-object files contain the identity remap tail already observed in the smaller sample. No single-object PSG contains it.

Tail validation failures: **0**.

## CORRECTION — W magnitude and strip topology

The earlier 881-file analysis required all vertices of a strip triangle to use the same W magnitude. Expanding to cutscene, rider and cable geometry invalidated that restriction.

The corrected rule is simpler and passes the entire corpus:

- two consecutive negative W values seed/restart a strip
- each later positive W emits the next triangle
- winding alternates
- the W magnitude selects a hierarchy transform for that individual vertex

Full-corpus results:

- submitted positions checked: **4,869,177**
- zero W values: **0**
- W magnitudes not divisible by 16: **0**
- out-of-range transform indices: **0**
- serialized strip starts: **872,158**
- reconstructed triangles: **3,124,861**
- topology warnings under the corrected rule: **0**

The transform index is:

```text
transform_index = abs(W) / 16 - 1
```

Evidence that this is a per-vertex transform selector rather than strict object ownership:

- **10,243** strip seed pairs reference different transforms
- **85,981** reconstructed triangles contain vertices from more than one transform

This behavior is prominent in animated riders/cutscene characters and cable geometry.

## VERIFIED — local bounds across hierarchy transforms

Of the 17,942 hierarchy descriptors:

- 16,948 receive at least one submitted position
- 994 receive no submitted positions

For populated descriptors, decoded local-space position bounds reproduce the stored descriptor center/half-extents within at most approximately **1.153 position quantization units** across the complete corpus.

This extends the position-scale/origin validation from the earlier sample to all retail PSGs.

## Packed high-count field

The high 16 bits of `packed_counts` remain **INFERRED** as a pre-batching strip-related count.

They never exceed the serialized negative-pair strip-start count:

- exact equality: 18,034 / 22,175 blocks
- smaller than serialized starts: 4,141 / 22,175 blocks
- maximum observed difference: 182

The difference is consistent with additional restart seeds inserted for VIF batching, but the exact exporter/runtime contract remains open.

## Tooling

- `scripts/psg_mesh_extract.py` — per-file payload parser and local mesh reconstruction
- `scripts/psg_corpus_verify.py` — multi-RES corpus validation
- `reference/ps2-vif.md` — public VIF control-bit reference
- `raw/2026-10-08-psg-full-corpus-summary.txt` — retained aggregate results

## Next

- validate hierarchy matrix composition for assembled/articulated geometry
- identify the VU microprogram reached by MSCNT
- identify the material-block `+0x08` float
- identify the exact runtime LOD-selection metric
- tie V2-16 directly to texture/material state
- identify V4-8 channel semantics
- trace GIF/GS submission
