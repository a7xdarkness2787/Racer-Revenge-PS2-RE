# Collision format (.col)

Status: **VERIFIED at the serialized-structure level** for the North American retail corpus.

The recovered RES directories contain **2,505** embedded `.col` resources. All 2,505 pass the same bounded parser with no unexplained trailing bytes.

## Common header

All integer values are little-endian.

| Offset | Size | Meaning |
| --- | ---: | --- |
| `+0x00` | 4 | magic `0x000004d2` |
| `+0x04` | 4 | ASCII tag `col\0` |
| `+0x08` | 4 | version; `1` in the retail corpus |
| `+0x0c` | 4 | collision type |

Observed type counts:

- type 0: **2,292**
- type 1: **9**
- type 2: **204**

The executable independently validates the magic, tag and version before dispatching on the type.

## Shared BVH node

All three serialized forms ultimately use the same 32-byte binary-tree node:

```text
float box_metric
float center_x
float center_y
float center_z
float half_x
float half_y
float half_z
u16   child0
u16   child1
```

Across **222,577** observed nodes, `box_metric` obeys this exact retail rule within normal float rounding:

```text
8 * max(half_x, 0.005)
  * max(half_y, 0.005)
  * max(half_z, 0.005)
```

This is the AABB volume after imposing a minimum half-extent of 0.005 on each axis.

Child references use bit 15 as a leaf tag:

- `child & 0x8000 == 0`: low 15 bits index another BVH node
- `child & 0x8000 != 0`: low 15 bits index a leaf record

Every child reference in the 2,505-file corpus is in range for that interpretation.

For every uncompressed static body checked, recursively collecting the triangles below each node reproduces the stored center and half-extents. The same test succeeds for every type-2 tree when its two-point leaf records are used as the leaf geometry.

## Type 0 — static triangle tree

Serialized body after the common header:

```text
float transform_3x4[12]
u32   field_40
u32   vertex_count
u32   node_count
u32   triangle_count
u32   compressed_vertices
vertex vertices[vertex_count]
u32   secondary_vertices
vertex secondary[vertex_count]   // only when secondary_vertices != 0
BVHNode nodes[node_count]
Triangle triangles[triangle_count]
```

The retail corpus obeys:

```text
node_count == triangle_count - 1
```

for all 2,292 top-level type-0 resources and for the 21 inline static bodies carried by type 1.

### Vertex encodings

`compressed_vertices == 0`:

```text
float x
float y
float z
```

12 bytes per vertex.

`compressed_vertices == 1`:

```text
s16 x
s16 y
s16 z
```

6 bytes per vertex. The executable-side scale/dequantization rule remains open.

Across the 2,292 top-level type-0 files:

- float, no secondary array: 1,512
- float, secondary array present: 769
- s16, no secondary array: 10
- s16, secondary array present: 1

The second array contains another `vertex_count` records in the same encoding. Its gameplay purpose is not named yet.

All observed top-level type-0 serialized 3x4 transforms are identity matrices.

### Triangle leaf

The serialized triangle record is exactly 22 bytes:

```text
float plane_d
float normal_x
float normal_y
float normal_z
u16   vertex0
u16   vertex1
u16   vertex2
```

The three indices are valid indices into the vertex array. In ordinary nondegenerate records, the normal is unit length to float precision and the indexed vertices satisfy the plane equation `n dot p + d = 0`.

## Type 1 — compound static collision

Only nine retail resources use type 1, all under track `anim\` paths:

- `GC: opening.col, windmill.col`
- `GB: Defensegate.col, opening.col, Defensegate2.col, windmill.col`
- `GA: Defensegate.col, opening.col`
- `MC: zbreak1floor.col`

Layout:

```text
common header
u32 child_count
u32 field_14
repeat child_count times:
    u32 child_index
    inline type-0 body beginning at transform_3x4
```

The nine retail files contain two or three children. `field_14` is zero in all nine. The inline bodies omit the common magic/version/type header.

All 21 serialized child transforms are identity in this build; placement/animation is therefore represented elsewhere.

## Type 2 — two-point leaf tree

Layout:

```text
common header
float matrix_4x4[16]
u32 leaf_count_copy
u32 node_count
u32 leaf_count
BVHNode nodes[node_count]
TwoPointLeaf leaves[leaf_count]
```

Retail invariants across all 204 type-2 files:

```text
leaf_count_copy == leaf_count
node_count == leaf_count - 1
file_size == 0x5c + node_count*32 + leaf_count*24
```

All 204 serialized 4x4 matrices are identity.

The 24-byte leaf is:

```text
float point0_x
float point0_y
float point0_z
float point1_x
float point1_y
float point1_z
```

There are **4,834** such leaves in the retail corpus. Recursively taking both points from descendant leaves reproduces every stored type-2 BVH center and half-extent.

The geometry proves these are two-point leaf primitives. The exact collision behavior assigned to those primitives is intentionally left unnamed until the runtime tests are complete.

Most type-2 resources are the pod-local `*m.COL` counterparts to type-0 `*f.COL` resources.

## Runtime connection

The executable collision loader is documented in `../executable/collision_loader.md`.

The current tooling is `../scripts/col_inspect.py`.
