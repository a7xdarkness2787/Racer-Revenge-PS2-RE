#!/usr/bin/env python3
"""Inspect the first PS2 VIF payload block in Racer Revenge .PSG resources."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


class PsgVifError(ValueError):
    pass


COMMAND_NAMES = {
    0x00: "NOP",
    0x01: "STCYCL",
    0x02: "OFFSET",
    0x03: "BASE",
    0x04: "ITOP",
    0x05: "STMOD",
    0x06: "MSKPATH3",
    0x07: "MARK",
    0x10: "FLUSHE",
    0x11: "FLUSH",
    0x13: "FLUSHA",
    0x14: "MSCAL",
    0x15: "MSCALF",
    0x17: "MSCNT",
    0x20: "STMASK",
    0x30: "STROW",
    0x31: "STCOL",
    0x4A: "MPG",
    0x50: "DIRECT",
    0x51: "DIRECTHL",
}


def unpack_source_bytes(command: int, num: int) -> int:
    base = command & 0x7F
    if not 0x60 <= base <= 0x7F:
        raise PsgVifError(f"{base:#x} is not an UNPACK command")

    components = ((base >> 2) & 3) + 1
    vector_length = base & 3
    count = 256 if num == 0 else num

    if vector_length == 0:
        bits_per_vector = components * 32
    elif vector_length == 1:
        bits_per_vector = components * 16
    elif vector_length == 2:
        bits_per_vector = components * 8
    else:
        if components != 4:
            raise PsgVifError(f"invalid packed UNPACK command {base:#x}")
        bits_per_vector = 16

    return (count * bits_per_vector + 7) // 8


def parse_vif(packet: bytes) -> list[dict]:
    pos = 0
    commands: list[dict] = []

    while pos + 4 <= len(packet):
        word = struct.unpack_from("<I", packet, pos)[0]
        immediate = word & 0xFFFF
        num = (word >> 16) & 0xFF
        command = (word >> 24) & 0xFF
        base = command & 0x7F
        start = pos
        pos += 4

        if 0x60 <= base <= 0x7F:
            source_bytes = unpack_source_bytes(command, num)
            name = f"UNPACK_{base:02X}"
        elif base == 0x20:
            source_bytes = 4
            name = "STMASK"
        elif base in (0x30, 0x31):
            source_bytes = 16
            name = COMMAND_NAMES[base]
        elif base == 0x4A:
            source_bytes = (256 if num == 0 else num) * 8
            name = "MPG"
        elif base in (0x50, 0x51):
            source_bytes = immediate * 16
            name = COMMAND_NAMES[base]
        elif base in COMMAND_NAMES:
            source_bytes = 0
            name = COMMAND_NAMES[base]
        else:
            raise PsgVifError(
                f"unknown VIF command {base:#x} at packet +{start:#x}"
            )

        padded = (source_bytes + 3) & ~3
        if pos + padded > len(packet):
            raise PsgVifError(
                f"VIF command at +{start:#x} exceeds declared packet size"
            )

        commands.append(
            {
                "offset": start,
                "word": word,
                "command": base,
                "name": name,
                "num": num,
                "immediate": immediate,
                "source_bytes": source_bytes,
            }
        )
        pos += padded

    if pos != len(packet):
        raise PsgVifError(f"{len(packet) - pos} unexplained packet bytes")

    return commands


def fixed_tables_end(blob: bytes) -> int:
    if len(blob) < 12 or blob[:4] != b"psg\0":
        raise PsgVifError("not a PSG file")

    version, object_count = struct.unpack_from("<II", blob, 4)
    if version != 3:
        raise PsgVifError(f"unsupported PSG version {version}")

    pos = 12 + object_count * 0xE0
    if pos + 4 > len(blob):
        raise PsgVifError("object table exceeds file")

    material_count = struct.unpack_from("<I", blob, pos)[0]
    pos += 4 + material_count * 0x40
    if pos > len(blob):
        raise PsgVifError("material table exceeds file")
    return pos


def inspect(blob: bytes) -> dict:
    descriptor_offset = fixed_tables_end(blob)
    if descriptor_offset + 0x40 > len(blob):
        raise PsgVifError("missing first 0x40-byte payload descriptor")

    descriptor = blob[descriptor_offset : descriptor_offset + 0x40]
    packet_size = struct.unpack_from("<I", descriptor, 0x3C)[0]

    if packet_size == 0:
        raise PsgVifError("first VIF packet has zero size")
    if packet_size & 0xF:
        raise PsgVifError(
            f"first VIF packet size {packet_size:#x} is not 16-byte aligned"
        )

    packet_offset = descriptor_offset + 0x40
    packet_end = packet_offset + packet_size
    if packet_end > len(blob):
        raise PsgVifError("first VIF packet exceeds file")

    packet = blob[packet_offset:packet_end]
    commands = parse_vif(packet)

    if not commands or commands[0]["word"] != 0x6C018000:
        raise PsgVifError(
            "first VIF command does not match the observed retail 0x6c018000 anchor"
        )

    return {
        "payload_offset": descriptor_offset,
        "descriptor_size": 0x40,
        "descriptor_words": [
            struct.unpack_from("<I", descriptor, offset)[0]
            for offset in range(0, 0x40, 4)
        ],
        "vif_packet_offset": packet_offset,
        "vif_packet_size": packet_size,
        "vif_commands": commands,
        "remaining_bytes": len(blob) - packet_end,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("psg", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = []
    for path in args.psg:
        row = inspect(path.read_bytes())
        row["source"] = str(path)
        rows.append(row)

    if args.json:
        print(json.dumps(rows if len(rows) > 1 else rows[0], indent=2))
    else:
        for row in rows:
            print(
                f"{row['source']}: first VIF packet "
                f"{row['vif_packet_size']} bytes @ "
                f"{row['vif_packet_offset']:#x}, "
                f"commands={len(row['vif_commands'])}, "
                f"remaining={row['remaining_bytes']}"
            )
            names = [command["name"] for command in row["vif_commands"][:24]]
            suffix = " ..." if len(row["vif_commands"]) > 24 else ""
            print("  " + ", ".join(names) + suffix)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, PsgVifError, ValueError) as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
