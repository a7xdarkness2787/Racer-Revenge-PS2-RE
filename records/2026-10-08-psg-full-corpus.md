# 2026-10-08 — complete PSG payload validation

## Question

Do the detailed PSG render rules recovered from POD01, TA and TB hold across the complete North American retail corpus?

## Result

**VERIFIED: yes.**

All **9,917 PSG resources** recovered from all **103 RES containers** pass the detailed render-payload parser with no unexplained bytes.

Key totals:

- 17,942 hierarchy descriptors
- 22,175 material blocks
- 366,935 VIF geometry batches
- 4,869,177 submitted positions
- 872,158 serialized strip starts
- 3,124,861 reconstructed triangles

## Correction retained

The smaller-sample mesh analysis incorrectly required one transform index for every vertex in a triangle and therefore treated CableShadow and animated character resources as topology exceptions.

The complete corpus disproves that restriction.

The general rule is:

- W sign controls strip seeding/restart
- W magnitude selects the per-vertex hierarchy transform

Using that rule produces zero topology warnings across all 9,917 PSG files.

This correction is retained explicitly rather than hiding the earlier interpretation.

## Additional complete-corpus results

- 9,846 files have one LOD group
- 71 files have four LOD groups
- all 1,035 multi-object PSGs have the identity remap tail
- all 8,882 single-object PSGs omit the tail
- block flag bit `0x8` exactly tracks V4-8 presence
- the `0x00ff0000` field occurs exactly on single-object blocks
- four and only four VIF batch grammars occur
- all W tags resolve to valid hierarchy indices

## Provenance

Private retail data was read locally. Only derived counts, format specifications and independently written verification tooling are committed.
