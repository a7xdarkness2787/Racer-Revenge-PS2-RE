#!/usr/bin/env python3
"""Inspect fixed header tables in Racer Revenge PS2 .PSG resources."""

from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path


class PsgFormatError(ValueError):
    pass


def fixed_string(block: bytes, what: str) -> str:
    try:
        end = block.index(0)
    except ValueError as exc:
        raise PsgFormatError(f"{what} is not NUL terminated") from exc
    if any(block[end + 1 :]):
        raise PsgFormatError(f"{what} has non-zero padding")
    try:
        return block[:end].decode("ascii")
    except UnicodeDecodeError as exc:
        raise PsgFormatError(f"{what} is not ASCII") from exc


def parse(blob: bytes) -> dict:
    if len(blob) < 12:
        raise PsgFormatError("file is too small")

    tag = blob[:4]
    version, object_count = struct.unpack_from("<II", blob, 4)
    if tag != b"psg\0":
        raise PsgFormatError(f"bad tag {tag!r}")
    if version != 3:
        raise PsgFormatError(f"unsupported version {version}")

    descriptor_end = 12 + object_count * 0xE0
    if descriptor_end + 4 > len(blob):
        raise PsgFormatError("descriptor table exceeds file")

    objects = []
    roots = 0
    for index in range(object_count):
        rec = blob[12 + index * 0xE0 : 12 + (index + 1) * 0xE0]
        name = fixed_string(rec[:0x80], f"object {index} name")
        matrix = list(struct.unpack_from("<16f", rec, 0x80))
        vec_a = list(struct.unpack_from("<3f", rec, 0xC0))
        vec_b = list(struct.unpack_from("<3f", rec, 0xCC))
        radius_like = struct.unpack_from("<f", rec, 0xD8)[0]
        parent_raw = struct.unpack_from("<I", rec, 0xDC)[0]
        parent = None if parent_raw == 0xFFFFFFFF else parent_raw

        if parent is None:
            roots += 1
        elif parent >= index:
            raise PsgFormatError(
                f"object {index}: parent {parent} is not an earlier object"
            )

        numeric = matrix + vec_a + vec_b + [radius_like]
        if not all(math.isfinite(value) for value in numeric):
            raise PsgFormatError(f"object {index}: non-finite descriptor value")

        if not (
            abs(matrix[3]) < 1e-5
            and abs(matrix[7]) < 1e-5
            and abs(matrix[11]) < 1e-5
            and abs(matrix[15] - 1.0) < 1e-5
        ):
            raise PsgFormatError(
                f"object {index}: matrix is not in the observed affine form"
            )

        objects.append(
            {
                "name": name,
                "matrix": matrix,
                "vec_a": vec_a,
                "vec_b": vec_b,
                "radius_like": radius_like,
                "parent": parent,
            }
        )

    if roots != 1:
        raise PsgFormatError(f"expected one hierarchy root, found {roots}")

    pos = descriptor_end
    material_count = struct.unpack_from("<I", blob, pos)[0]
    pos += 4

    material_bytes = material_count * 0x40
    if pos + material_bytes > len(blob):
        raise PsgFormatError("material-name table exceeds file")

    materials = []
    for index in range(material_count):
        start = pos + index * 0x40
        materials.append(
            fixed_string(blob[start : start + 0x40], f"material {index} name")
        )
    pos += material_bytes

    if pos >= len(blob):
        raise PsgFormatError("PSG has no payload after fixed tables")

    return {
        "version": version,
        "object_count": object_count,
        "objects": objects,
        "material_count": material_count,
        "materials": materials,
        "payload_offset": pos,
        "payload_size": len(blob) - pos,
        "size": len(blob),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("psg", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = []
    for path in args.psg:
        row = parse(path.read_bytes())
        row["source"] = str(path)
        rows.append(row)

    if args.json:
        print(json.dumps(rows if len(rows) > 1 else rows[0], indent=2))
    else:
        for row in rows:
            print(
                f"{row['source']}: objects={row['object_count']} "
                f"materials={row['material_count']} "
                f"payload={row['payload_size']} bytes @ {row['payload_offset']:#x}"
            )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, PsgFormatError, ValueError) as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
