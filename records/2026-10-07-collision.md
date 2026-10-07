# 2026-10-07 — collision format investigation

## Question

Can the embedded `.col` family be parsed across the complete retail corpus, and can the file structures be tied to the executable collision loader?

## Inputs

Private retail inputs only:

- `SLUS_202.68`
- reconstructed logical resources from all 103 retail `.RES` containers

No retail collision payload is committed.

## VERIFIED — corpus-wide parse

The RES corpus contains **2,505** `.col` resources.

A bounded parser consumed all 2,505 exactly:

- type 0: 2,292
- type 1: 9
- type 2: 204
- failures: 0
- unexplained trailing bytes: 0

Every file begins with the same `0x4d2 / col\0 / version 1 / type` header.

## VERIFIED — binary hierarchy

Across all serialized collision forms there are **222,577** 32-byte BVH nodes.

Each node contains:

- a float metric
- center vec3
- half-extents vec3
- two u16 child references

Every child reference is valid under the rule that bit 15 selects a leaf and the low 15 bits are the index.

The leading float is not an unknown arbitrary weight. Across all 222,577 nodes it equals:

`8 * max(hx, 0.005) * max(hy, 0.005) * max(hz, 0.005)`

within float precision.

This is the volume of the node AABB with a minimum half-extent of 0.005 per axis.

## VERIFIED — static triangle trees

Type 0 and the inline bodies used by type 1 share one static-body serialization.

There are 2,313 such static bodies when the 2,292 top-level type-0 files and 21 compound children are counted together.

The tree invariant is exact throughout the corpus:

`node_count == triangle_count - 1`

For the **2,302 uncompressed static bodies**, recursively following child links from every BVH node and recomputing bounds from descendant indexed triangle vertices reproduces every stored node center and half-extent.

The triangle record is 22 bytes and contains a plane equation followed by three u16 vertex indices.

Only 11 static bodies use the s16 vertex encoding; its executable-side dequantization rule remains open.

## VERIFIED — type 1 compound files

Nine track animation resources use type 1. Together they carry 21 inline static collision bodies.

The wrapper layout is:

- child count
- a second u32 that is zero in all nine retail files
- child index
- inline static body
- repeated for each child

The child counts are two or three.

## VERIFIED — type 2 two-point trees

All 204 type-2 resources satisfy:

- first count == leaf count
- node count == leaf count - 1
- exact file size `0x5c + nodes*32 + leaves*24`

The corpus contains 4,834 24-byte type-2 leaves. Each leaf is two vec3 values.

For every type-2 BVH node, recursively collecting the two points from descendant leaves reproduces the stored center and half-extents exactly within float precision.

This establishes the 24-byte record as a two-point geometric leaf. Its higher-level collision semantics remain open.

## OBSERVED — executable agreement

The executable validates:

- magic `0x4d2`
- tag `col\0`
- version `1`

and then dispatches at `0x00124f80` to three readers:

- type 0 -> `0x00125890`
- type 1 -> `0x00126450`
- type 2 -> `0x00126640`

The type-1 reader recursively uses the type-0 body reader, matching the serialized nesting discovered independently from the files.

## Correction from initial hypothesis

The first float in a 32-byte tree node initially looked like ordinary AABB volume from a small sample. Degenerate boxes disproved the naive formula. Full-corpus testing revealed the missing rule: each half-extent is clamped to at least 0.005 before volume is calculated.

The corrected formula passes all 222,577 nodes and is the one retained in the stable format note.

## Next

- decode the s16 vertex scale/dequantization path
- follow collision objects into pod/environment contact response
- connect static track collision trees to `TunnelTrack` zones/progression
- begin `.psg` geometry analysis and correlate visible mesh bounds with collision bounds
