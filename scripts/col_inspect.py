#!/usr/bin/env python3
"""Inspect Star Wars: Racer Revenge PS2 .COL collision resources."""

from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path

MAGIC = 0x4D2
TAG = b"col\x00"
VERSION = 1
MIN_HALF_EXTENT = 0.005


class ColFormatError(ValueError):
    pass


def need(blob: bytes, pos: int, size: int, what: str) -> None:
    if pos < 0 or size < 0 or pos + size > len(blob):
        raise ColFormatError(f"{what} exceeds file bounds")


def node_at(blob: bytes, pos: int) -> dict:
    need(blob, pos, 32, "BVH node")
    metric, cx, cy, cz, hx, hy, hz, child0, child1 = struct.unpack_from(
        "<fffffffHH", blob, pos
    )
    expected = (
        8.0
        * max(hx, MIN_HALF_EXTENT)
        * max(hy, MIN_HALF_EXTENT)
        * max(hz, MIN_HALF_EXTENT)
    )
    if not math.isclose(metric, expected, rel_tol=3e-5, abs_tol=2e-5):
        raise ColFormatError(
            f"BVH node metric mismatch: {metric} != clamped box volume {expected}"
        )
    return {
        "metric": metric,
        "center": [cx, cy, cz],
        "half_extents": [hx, hy, hz],
        "child0": child0,
        "child1": child1,
    }


def validate_child(child: int, node_count: int, leaf_count: int, where: str) -> None:
    if child & 0x8000:
        index = child & 0x7FFF
        if index >= leaf_count:
            raise ColFormatError(f"{where}: leaf index {index} >= {leaf_count}")
    elif child >= node_count:
        raise ColFormatError(f"{where}: node index {child} >= {node_count}")


def parse_static_body(blob: bytes, pos: int) -> tuple[dict, int]:
    start = pos
    need(blob, pos, 68, "static collision header")
    transform = list(struct.unpack_from("<12f", blob, pos))
    pos += 48
    field_40, vertex_count, node_count, triangle_count, compressed = struct.unpack_from(
        "<IIIII", blob, pos
    )
    pos += 20

    if compressed not in (0, 1):
        raise ColFormatError(f"unsupported vertex encoding flag {compressed}")
    if node_count != triangle_count - 1:
        raise ColFormatError(
            f"tree invariant failed: nodes={node_count}, triangles={triangle_count}"
        )

    vertex_stride = 6 if compressed else 12
    need(blob, pos, vertex_count * vertex_stride, "primary vertex array")
    pos += vertex_count * vertex_stride

    need(blob, pos, 4, "secondary vertex flag")
    secondary = struct.unpack_from("<I", blob, pos)[0]
    pos += 4
    if secondary not in (0, 1):
        raise ColFormatError(f"unexpected secondary vertex flag {secondary}")
    if secondary:
        need(blob, pos, vertex_count * vertex_stride, "secondary vertex array")
        pos += vertex_count * vertex_stride

    node_offset = pos
    need(blob, pos, node_count * 32, "BVH node array")
    for index in range(node_count):
        node = node_at(blob, pos + index * 32)
        validate_child(node["child0"], node_count, triangle_count, f"node {index} child0")
        validate_child(node["child1"], node_count, triangle_count, f"node {index} child1")
    pos += node_count * 32

    triangle_offset = pos
    need(blob, pos, triangle_count * 22, "triangle array")
    for index in range(triangle_count):
        _, _, _, _, i0, i1, i2 = struct.unpack_from(
            "<ffffHHH", blob, pos + index * 22
        )
        for vertex_index in (i0, i1, i2):
            if vertex_index >= vertex_count:
                raise ColFormatError(
                    f"triangle {index}: vertex index {vertex_index} >= {vertex_count}"
                )
    pos += triangle_count * 22

    return {
        "serialized_size": pos - start,
        "transform": transform,
        "field_40": field_40,
        "vertex_count": vertex_count,
        "node_count": node_count,
        "triangle_count": triangle_count,
        "compressed_vertices": bool(compressed),
        "secondary_vertices": bool(secondary),
        "vertex_stride": vertex_stride,
        "node_offset": node_offset,
        "triangle_offset": triangle_offset,
    }, pos


def parse(blob: bytes) -> dict:
    need(blob, 0, 16, "COL header")
    magic = struct.unpack_from("<I", blob, 0)[0]
    tag = blob[4:8]
    version, collision_type = struct.unpack_from("<II", blob, 8)

    if magic != MAGIC:
        raise ColFormatError(f"bad magic {magic:#x}; expected {MAGIC:#x}")
    if tag != TAG:
        raise ColFormatError(f"bad tag {tag!r}; expected {TAG!r}")
    if version != VERSION:
        raise ColFormatError(f"unsupported version {version}; expected {VERSION}")

    result = {
        "magic": magic,
        "tag": "col",
        "version": version,
        "type": collision_type,
        "size": len(blob),
    }

    if collision_type == 0:
        body, end = parse_static_body(blob, 0x10)
        result["static"] = body

    elif collision_type == 1:
        need(blob, 0x10, 8, "compound header")
        child_count, field_14 = struct.unpack_from("<II", blob, 0x10)
        pos = 0x18
        children = []
        for child_number in range(child_count):
            need(blob, pos, 4, f"compound child {child_number} index")
            child_index = struct.unpack_from("<I", blob, pos)[0]
            pos += 4
            child, pos = parse_static_body(blob, pos)
            children.append({"index": child_index, "static": child})
        end = pos
        result["compound"] = {
            "child_count": child_count,
            "field_14": field_14,
            "children": children,
        }

    elif collision_type == 2:
        need(blob, 0x10, 76, "two-point collision header")
        matrix = list(struct.unpack_from("<16f", blob, 0x10))
        count_copy, node_count, leaf_count = struct.unpack_from("<III", blob, 0x50)
        if count_copy != leaf_count:
            raise ColFormatError(f"type 2 count mismatch: {count_copy} != {leaf_count}")
        if node_count != leaf_count - 1:
            raise ColFormatError(
                f"type 2 tree invariant failed: nodes={node_count}, leaves={leaf_count}"
            )

        pos = 0x5C
        node_offset = pos
        need(blob, pos, node_count * 32, "type 2 BVH nodes")
        for index in range(node_count):
            node = node_at(blob, pos + index * 32)
            validate_child(node["child0"], node_count, leaf_count, f"node {index} child0")
            validate_child(node["child1"], node_count, leaf_count, f"node {index} child1")
        pos += node_count * 32

        leaf_offset = pos
        need(blob, pos, leaf_count * 24, "type 2 two-point leaf array")
        pos += leaf_count * 24
        end = pos
        result["two_point"] = {
            "matrix": matrix,
            "count_copy": count_copy,
            "node_count": node_count,
            "leaf_count": leaf_count,
            "node_offset": node_offset,
            "leaf_offset": leaf_offset,
            "leaf_stride": 24,
        }

    else:
        raise ColFormatError(f"unsupported collision type {collision_type}")

    if end != len(blob):
        raise ColFormatError(f"{len(blob) - end} unexplained trailing bytes")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("col", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = []
    for path in args.col:
        row = parse(path.read_bytes())
        row["source"] = str(path)
        rows.append(row)

    if args.json:
        print(json.dumps(rows if len(rows) > 1 else rows[0], indent=2))
    else:
        for row in rows:
            print(f"{row['source']}: type={row['type']} size={row['size']}")
            if row["type"] == 0:
                s = row["static"]
                print(
                    f"  vertices={s['vertex_count']} nodes={s['node_count']} "
                    f"triangles={s['triangle_count']} compressed={s['compressed_vertices']} "
                    f"secondary={s['secondary_vertices']}"
                )
            elif row["type"] == 1:
                c = row["compound"]
                print(f"  children={c['child_count']} field_14={c['field_14']}")
            else:
                t = row["two_point"]
                print(f"  nodes={t['node_count']} two_point_leaves={t['leaf_count']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ColFormatError, ValueError) as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
