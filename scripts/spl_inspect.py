#!/usr/bin/env python3
"""Inspect Racer Revenge PS2 .spl track graph files."""

from __future__ import annotations

import argparse
import configparser
import json
from pathlib import Path

BASE_NODE_KEYS = {
    "Position",
    "LeftTrackWidth",
    "RightTrackWidth",
    "SpeedLimit",
    "DistanceToFinish",
    "BranchID",
    "NumNextNodes",
}


def load(path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser(interpolation=None, strict=False)
    config.optionxform = str
    with path.open("r", encoding="ascii") as handle:
        config.read_file(handle)
    return config


def inspect(config: configparser.ConfigParser) -> dict:
    if "Track" not in config:
        raise ValueError("missing [Track] section")

    declared = int(config["Track"]["NumNodes"])
    node_sections = [
        section
        for section in config.sections()
        if section.startswith("Node") and section[4:].isdigit()
    ]
    ids = sorted(int(section[4:]) for section in node_sections)
    if ids != list(range(declared)):
        raise ValueError(f"node sections do not exactly cover 0..{declared - 1}")

    edge_count = 0
    branch_nodes: list[int] = []
    features: dict[str, int] = {}

    for node_id in ids:
        section = config[f"Node{node_id}"]
        num_next = int(section.get("NumNextNodes", "0"))
        if num_next > 1:
            branch_nodes.append(node_id)

        for next_index in range(num_next):
            key = f"Next{next_index}"
            if key not in section:
                raise ValueError(f"Node{node_id}: missing {key}")
            target = int(section[key])
            if not 0 <= target < declared:
                raise ValueError(
                    f"Node{node_id}: {key} target is out of range: {target}"
                )
            edge_count += 1

        for key in section:
            if key in BASE_NODE_KEYS or key.startswith("Next"):
                continue
            features[key] = features.get(key, 0) + 1

    shortcuts = []
    for section_name in config.sections():
        if section_name.startswith("Shortcut") and section_name[8:].isdigit():
            section = config[section_name]
            shortcuts.append(
                {
                    "section": section_name,
                    "PlayerTestNode": section.get("PlayerTestNode"),
                    "AIBlockNode": section.get("AIBlockNode"),
                }
            )

    track = config["Track"]
    return {
        "declared_nodes": declared,
        "node_sections": len(node_sections),
        "edges": edge_count,
        "branch_nodes": len(branch_nodes),
        "branch_node_indices": branch_nodes,
        "track_width": float(track["TrackWidth"]),
        "start_node": int(track["StartNode"]) if "StartNode" in track else None,
        "num_shortcuts_declared": (
            int(track["NumShortcuts"]) if "NumShortcuts" in track else 0
        ),
        "shortcut_sections": shortcuts,
        "optional_node_features": features,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spl", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = []
    for path in args.spl:
        row = inspect(load(path))
        row["source"] = str(path)
        rows.append(row)

    if args.json:
        print(json.dumps(rows if len(rows) > 1 else rows[0], indent=2))
    else:
        for row in rows:
            print(
                f"{row['source']}: nodes={row['declared_nodes']} "
                f"edges={row['edges']} branches={row['branch_nodes']} "
                f"shortcuts={row['num_shortcuts_declared']}"
            )
            if row["optional_node_features"]:
                print(" features:", row["optional_node_features"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
