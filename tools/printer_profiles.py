"""Load printer profiles from printer_profiles.yaml."""
from __future__ import annotations

import dataclasses
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILES_FILE = REPO_ROOT / "printer_profiles.yaml"


@dataclasses.dataclass
class PrinterProfile:
    id: str
    display_name: str
    motion_axes: tuple[str, str]
    bed_axis: str
    build_volume: dict[str, float]
    default_margin: float
    max_speed_mm_s: float
    max_accel_mm_s2: float
    start_template: Path
    end_template: Path

    def axis_limits(self, axis: str) -> tuple[float, float]:
        return 0.0, float(self.build_volume[axis])


def load_profile(printer_id: str, profiles_file: Path = PROFILES_FILE) -> PrinterProfile:
    with open(profiles_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if printer_id not in data:
        known = ", ".join(sorted(data))
        raise KeyError(f"Unknown printer '{printer_id}'. Known printers: {known}")

    entry = data[printer_id]
    return PrinterProfile(
        id=printer_id,
        display_name=entry["display_name"],
        motion_axes=tuple(entry["motion_axes"]),
        bed_axis=entry["bed_axis"],
        build_volume=entry["build_volume"],
        default_margin=float(entry["default_margin"]),
        max_speed_mm_s=float(entry["max_speed_mm_s"]),
        max_accel_mm_s2=float(entry["max_accel_mm_s2"]),
        start_template=profiles_file.parent / entry["start_template"],
        end_template=profiles_file.parent / entry["end_template"],
    )


def list_profiles(profiles_file: Path = PROFILES_FILE) -> list[str]:
    with open(profiles_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return sorted(data)
