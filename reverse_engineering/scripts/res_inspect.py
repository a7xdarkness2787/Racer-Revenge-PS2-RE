#!/usr/bin/env python3
"""Inspect and optionally extract Racer Revenge PS2 .RES containers.

This tool is based on the North American retail SLUS_202.68 corpus. It does
not contain game data. Extraction is only performed from a file supplied by
the user at runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath

OUTPUT_CHUNK_SIZE = 0x6000
OFFSET_UNIT = 0x100
CHUNK_SEPARATOR = 0xFF


class ResFormatError(ValueError):
    pass


@dataclass(frozen=True)
class ResourceEntry:
    name: str
    offset_units: int
    offset: int
    size: int


@dataclass
class ResContainer:
    version: int
    field_04: int
    field_08: int
    field_0c: int
    chunk_table_bytes: int
    chunk_sizes: list[int]
    resource_count: int
    directory_size: int
    payload_offset: int
    entries: list[ResourceEntry]
    virtual_data: bytes | None = None


def _u24le(data: bytes) -> int:
    if len(data) != 3:
        raise ResFormatError("u24 read requires exactly three bytes")
    return data[0] | (data[1] << 8) | (data[2] << 16)


def parse_res(blob: bytes, *, decode_payload: bool = True) -> ResContainer:
    if len(blob) < 20:
        raise ResFormatError("file is too small for the observed v3 header")

    version, field_04, field_08, field_0c, table_bytes = struct.unpack_from(
        "<IIIII", blob, 0
    )
    if version != 3:
        raise ResFormatError(f"unsupported RES version {version}; retail corpus uses 3")
    if table_bytes < 2 or table_bytes & 1:
        raise ResFormatError("chunk table length is invalid")
    if field_04 != table_bytes + 0x0C:
        raise ResFormatError(
            f"field_04 invariant failed: {field_04:#x} != {table_bytes + 0x0C:#x}"
        )

    table_start = 0x14
    table_end = table_start + table_bytes
    if table_end + 8 > len(blob):
        raise ResFormatError("chunk table exceeds file bounds")

    raw_sizes = list(
        struct.unpack_from("<" + "H" * (table_bytes // 2), blob, table_start)
    )
    if raw_sizes[-1] != 0:
        raise ResFormatError("chunk table is missing its zero terminator")
    chunk_sizes = raw_sizes[:-1]
    if any(size == 0 for size in chunk_sizes):
        raise ResFormatError("chunk table contains an unexpected embedded zero")

    resource_count, directory_size = struct.unpack_from("<II", blob, table_end)
    directory_start = table_end + 8
    payload_offset = directory_start + directory_size
    if payload_offset > len(blob):
        raise ResFormatError("directory exceeds file bounds")

    entries: list[ResourceEntry] = []
    cursor = directory_start
    for index in range(resource_count):
        if cursor + 4 > payload_offset:
            raise ResFormatError(f"entry {index}: missing name length")
        name_length = struct.unpack_from("<I", blob, cursor)[0]
        cursor += 4

        fixed_tail = 1 + 3 + 4
        if cursor + name_length + fixed_tail > payload_offset:
            raise ResFormatError(f"entry {index}: record exceeds directory")

        name_bytes = blob[cursor : cursor + name_length]
        cursor += name_length
        try:
            name = name_bytes.decode("ascii")
        except UnicodeDecodeError as exc:
            raise ResFormatError(f"entry {index}: non-ASCII resource name") from exc

        if blob[cursor] != 0:
            raise ResFormatError(f"entry {index}: resource name is not NUL terminated")
        cursor += 1

        offset_units = _u24le(blob[cursor : cursor + 3])
        cursor += 3
        size = struct.unpack_from("<I", blob, cursor)[0]
        cursor += 4
        entries.append(
            ResourceEntry(
                name=name,
                offset_units=offset_units,
                offset=offset_units * OFFSET_UNIT,
                size=size,
            )
        )

    if cursor != payload_offset:
        raise ResFormatError(
            f"directory consumed {cursor - directory_start:#x} bytes, "
            f"header declares {directory_size:#x}"
        )

    virtual_data = None
    payload_cursor = payload_offset
    if decode_payload:
        chunks: list[bytes] = []

    for index, compressed_size in enumerate(chunk_sizes):
        end = payload_cursor + compressed_size
        if end >= len(blob):
            raise ResFormatError(f"chunk {index}: compressed data exceeds file bounds")
        compressed = blob[payload_cursor:end]

        if decode_payload:
            try:
                decoded = zlib.decompress(compressed)
            except zlib.error as exc:
                raise ResFormatError(f"chunk {index}: zlib decode failed: {exc}") from exc
            if len(decoded) != OUTPUT_CHUNK_SIZE:
                raise ResFormatError(
                    f"chunk {index}: decoded {len(decoded):#x} bytes, "
                    f"expected {OUTPUT_CHUNK_SIZE:#x}"
                )
            chunks.append(decoded)

        if blob[end] != CHUNK_SEPARATOR:
            raise ResFormatError(
                f"chunk {index}: missing {CHUNK_SEPARATOR:#04x} separator"
            )
        payload_cursor = end + 1

    if payload_cursor != len(blob):
        raise ResFormatError(
            f"container has {len(blob) - payload_cursor} unexplained trailing bytes"
        )

    if decode_payload:
        virtual_data = b"".join(chunks)
        for index, entry in enumerate(entries):
            if entry.offset + entry.size > len(virtual_data):
                raise ResFormatError(f"entry {index}: resource range exceeds decoded data")

    return ResContainer(
        version=version,
        field_04=field_04,
        field_08=field_08,
        field_0c=field_0c,
        chunk_table_bytes=table_bytes,
        chunk_sizes=chunk_sizes,
        resource_count=resource_count,
        directory_size=directory_size,
        payload_offset=payload_offset,
        entries=entries,
        virtual_data=virtual_data,
    )


def _safe_output_path(root: Path, resource_name: str) -> Path:
    normalized = resource_name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        raise ResFormatError(f"unsafe resource path: {resource_name!r}")
    return root.joinpath(*path.parts)


def extract(container: ResContainer, output_dir: Path) -> None:
    if container.virtual_data is None:
        raise ResFormatError("payload was not decoded")
    for entry in container.entries:
        target = _safe_output_path(output_dir, entry.name)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = container.virtual_data[entry.offset : entry.offset + entry.size]
        target.write_bytes(data)


def summary(container: ResContainer, source: Path) -> dict:
    return {
        "source": str(source),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "version": container.version,
        "field_04": container.field_04,
        "field_08": container.field_08,
        "field_0c": container.field_0c,
        "chunk_table_bytes": container.chunk_table_bytes,
        "chunk_count": len(container.chunk_sizes),
        "resource_count": container.resource_count,
        "directory_size": container.directory_size,
        "payload_offset": container.payload_offset,
        "decoded_size": len(container.chunk_sizes) * OUTPUT_CHUNK_SIZE,
        "entries": [asdict(entry) for entry in container.entries],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("res", type=Path, help="retail .RES file to inspect")
    parser.add_argument("--extract", type=Path, help="extract logical resources here")
    parser.add_argument("--json", action="store_true", help="print machine-readable metadata")
    args = parser.parse_args()

    blob = args.res.read_bytes()
    container = parse_res(blob, decode_payload=True)
    info = summary(container, args.res)

    if args.extract:
        extract(container, args.extract)

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"{args.res}: RES v{container.version}")
        print(f"chunks: {len(container.chunk_sizes)} x {OUTPUT_CHUNK_SIZE:#x} decoded bytes")
        print(f"resources: {container.resource_count}")
        print(f"directory: {container.directory_size:#x} bytes")
        print(f"payload offset: {container.payload_offset:#x}")
        for entry in container.entries:
            print(f"{entry.offset:08x} {entry.size:8d} {entry.name}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ResFormatError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
