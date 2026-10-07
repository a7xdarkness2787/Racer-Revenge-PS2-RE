#!/usr/bin/env python3
"""Inspect Racer Revenge PS2 .phy pod configuration files."""

from __future__ import annotations

import argparse
import configparser
import json
from pathlib import Path

CORE_SECTIONS = [
    "Pod Setup",
    "Wreckage",
    "Physical Properties",
    "Repulsor",
    "Roll Control",
    "Engine",
    "Engine Aerodynamics",
    "Pod Animation",
    "Collisions",
    "Joystick",
    "CameraInfo",
    "DamageRepair",
    "Pod Audio",
    "BaseAbilities",
    "MaxAbilities",
    "Tuning",
]


def load(path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser(interpolation=None, strict=False)
    config.optionxform = str
    with path.open("r", encoding="latin1") as handle:
        config.read_file(handle)
    return config


def vec3(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",")]
    if len(values) != 3:
        raise ValueError("expected three comma-separated numbers")
    return values


def describe(config: configparser.ConfigParser) -> dict:
    setup = dict(config["Pod Setup"]) if "Pod Setup" in config else {}
    engine = dict(config["Engine"]) if "Engine" in config else {}
    damage = dict(config["DamageRepair"]) if "DamageRepair" in config else {}
    tuning = dict(config["Tuning"]) if "Tuning" in config else {}

    result = {
        "name": setup.get("Name"),
        "prefix": setup.get("Prefix"),
        "missing_core_sections": [
            section for section in CORE_SECTIONS if section not in config
        ],
        "sections": list(config.sections()),
        "engine": {
            key: engine.get(key)
            for key in (
                "MaxThrustA",
                "MaxThrustB",
                "MaxThrustC",
                "TheoreticalTopSpeedA",
                "TheoreticalTopSpeedB",
                "TheoreticalTopSpeedC",
                "BoostThrust",
                "RepairThrust",
                "BoostSpeed",
            )
        },
        "damage_repair": {
            key: damage.get(key)
            for key in (
                "DefenseA",
                "DefenseB",
                "DefenseC",
                "BaseRepairAmountA",
                "BaseRepairAmountB",
                "BaseRepairAmountC",
                "BaseCoolingTimeA",
                "BaseCoolingTimeB",
                "BaseCoolingTimeC",
            )
        },
        "tuning": {
            key: tuning.get(key)
            for key in (
                "UseValues",
                "UseAValues",
                "UseBValues",
                "UseCValues",
                "UpgradePercent",
            )
        },
    }

    if "CameraInfo" in config and config["CameraInfo"].get("FirstPersonCamOffset"):
        result["first_person_camera_offset"] = vec3(
            config["CameraInfo"]["FirstPersonCamOffset"]
        )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phy", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = []
    for path in args.phy:
        row = describe(load(path))
        row["source"] = str(path)
        rows.append(row)

    if args.json:
        print(json.dumps(rows if len(rows) > 1 else rows[0], indent=2))
    else:
        for row in rows:
            print(f"{row['source']}: {row['name']} prefix={row['prefix']}")
            print(" sections:", ", ".join(row["sections"]))
            print(" engine:", row["engine"])
            print(" damage/repair:", row["damage_repair"])
            print(" tuning:", row["tuning"])
            if row["missing_core_sections"]:
                print(" missing:", ", ".join(row["missing_core_sections"]))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
