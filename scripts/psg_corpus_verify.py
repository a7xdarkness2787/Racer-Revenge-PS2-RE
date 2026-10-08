#!/usr/bin/env python3
"""Validate PSG render payloads across user-supplied Racer Revenge RES files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from psg_mesh_extract import parse as parse_psg
from res_inspect import parse_res


def input_res_files(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if path.is_dir():
            found.extend(
                item for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() == ".res"
            )
        elif path.is_file() and path.suffix.lower() == ".res":
            found.append(path)
        else:
            raise ValueError(f"not a RES file or directory: {path}")
    return sorted(set(found))


def verify(paths: list[Path]) -> dict:
    totals = Counter()
    flag_counts = Counter()
    lod_counts = Counter()
    failures: list[dict] = []

    for res_path in input_res_files(paths):
        container = parse_res(res_path.read_bytes(), decode_payload=True)
        assert container.virtual_data is not None
        totals["res_files"] += 1

        for entry in container.entries:
            if not entry.name.lower().endswith(".psg"):
                continue

            totals["psg_files"] += 1
            blob = container.virtual_data[entry.offset:entry.offset + entry.size]

            try:
                result = parse_psg(blob)
            except Exception as exc:
                failures.append({
                    "res": str(res_path),
                    "resource": entry.name,
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue

            totals["object_descriptors"] += len(result["objects"])
            totals["material_names"] += len(result["materials"])
            totals["lod_groups"] += len(result["lods"])
            lod_counts[len(result["lods"])] += 1
            totals["multi_object_remap_tails"] += result["object_remap"] is not None

            for lod in result["lods"]:
                for block in lod["blocks"]:
                    totals["material_blocks"] += 1
                    totals["vif_batches"] += block["batch_count"]
                    totals["submitted_positions"] += len(block["vertices"])
                    totals["triangles"] += len(block["faces"])
                    totals["serialized_strip_starts"] += block["strip_starts"]
                    totals["topology_warnings"] += len(block["topology_warnings"])
                    totals["mixed_transform_triangles"] += sum(
                        1 for face in block["faces"] if face["mixed_transforms"]
                    )
                    flag_counts[f"0x{block['flags']:08x}"] += 1

    return {
        "totals": dict(totals),
        "lod_count_distribution": {
            str(key): value for key, value in sorted(lod_counts.items())
        },
        "material_block_flags": dict(sorted(flag_counts.items())),
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        type=Path,
        nargs="+",
        help="RES files and/or directories containing RES files",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = verify(args.paths)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        totals = result["totals"]
        for key in (
            "res_files",
            "psg_files",
            "object_descriptors",
            "material_names",
            "lod_groups",
            "material_blocks",
            "vif_batches",
            "submitted_positions",
            "serialized_strip_starts",
            "triangles",
            "mixed_transform_triangles",
            "multi_object_remap_tails",
            "topology_warnings",
        ):
            print(f"{key}: {totals.get(key, 0)}")
        print("LOD count distribution:", result["lod_count_distribution"])
        print("material block flags:", result["material_block_flags"])
        print("failures:", len(result["failures"]))

    return 1 if result["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
