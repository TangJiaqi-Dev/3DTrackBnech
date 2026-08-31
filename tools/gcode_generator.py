#!/usr/bin/env python
"""Generate a 3DTrackBench benchmark .gcode file with an adjustable travel
range and speed range.

Example:
    python tools/gcode_generator.py --printer a1_mini \\
        --x-range 1 179 --z-range 1 179 \\
        --speed-range 6000 30000 --speed-step 3000 \\
        --out out.gcode

Run with --printer alone (no range flags) to reproduce the shipped file's
default range and speed sweep.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sections
from printer_profiles import list_profiles, load_profile


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--printer", default="a1_mini", help="printer id from printer_profiles.yaml")
    parser.add_argument("--x-range", nargs=2, type=float, metavar=("MIN", "MAX"), help="X travel range in mm")
    parser.add_argument("--y-range", nargs=2, type=float, metavar=("MIN", "MAX"), help="Y travel range in mm")
    parser.add_argument("--z-range", nargs=2, type=float, metavar=("MIN", "MAX"), help="Z travel range in mm")
    parser.add_argument("--speed-range", nargs=2, type=float, metavar=("START", "END"),
                         help="Section speed_sweep's feedrate sweep range in mm/min (F units)")
    parser.add_argument("--speed-step", type=float, help="Section speed_sweep's feedrate step in mm/min (default 3000)")
    parser.add_argument("--speed-sweep-warmup", type=float,
                         help="Section speed_sweep's warm-up feedrate in mm/min (default 3000)")
    parser.add_argument("--calibration-speed", type=float,
                         help="Section calibration's corner-move feedrate in mm/min (default 3000)")
    parser.add_argument("--linear-speed", type=float, help="Section linear's feedrate in mm/min (default 6000)")
    parser.add_argument("--circular-travel-speed", type=float,
                         help="Section circular's approach-move feedrate in mm/min (default 2000)")
    parser.add_argument("--circular-speed", type=float,
                         help="Section circular's arc-tracing feedrate in mm/min (default 6000)")
    parser.add_argument("--complex-speed", type=float, help="Section complex's feedrate in mm/min (default 6000)")
    parser.add_argument("--drift-speeds", nargs="+", type=float,
                         help="Section drift's feedrates, one shuttle pass per value in mm/min (default 3000 6000)")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for the scattered-point sections")
    parser.add_argument("--out", required=True, type=Path, help="output .gcode path")
    return parser.parse_args(argv)


def resolve_axis_range(flag_value, profile, axis: str) -> tuple[float, float]:
    lo, hi = profile.axis_limits(axis)
    if flag_value is None:
        return lo + profile.default_margin, hi - profile.default_margin
    lo_req, hi_req = flag_value
    if lo_req >= hi_req:
        raise ValueError(f"--{axis.lower()}-range min must be less than max, got {lo_req} {hi_req}")
    if lo_req < lo or hi_req > hi:
        raise ValueError(
            f"--{axis.lower()}-range [{lo_req}, {hi_req}] exceeds {profile.display_name} "
            f"build volume [{lo}, {hi}] for axis {axis}"
        )
    return lo_req, hi_req


def resolve_speed(value: float | None, default: float, profile, flag_name: str) -> float:
    v = value if value is not None else default
    max_speed_mm_min = profile.max_speed_mm_s * 60
    if v <= 0 or v > max_speed_mm_min:
        raise ValueError(
            f"--{flag_name} {v:g} exceeds {profile.display_name} max speed "
            f"{profile.max_speed_mm_s} mm/s ({max_speed_mm_min:g} mm/min)"
        )
    return v


def build_gcode(args: argparse.Namespace) -> str:
    profile = load_profile(args.printer)
    a1, a2 = profile.motion_axes

    range_flags = {"X": args.x_range, "Y": args.y_range, "Z": args.z_range}
    for axis, value in range_flags.items():
        if value is not None and axis not in (a1, a2):
            raise ValueError(
                f"{profile.display_name}'s toolhead does not move in {axis} "
                f"(it's the bed axis) — --{axis.lower()}-range has no effect. "
                f"This printer's travel axes are {a1} and {a2}."
            )
    bounds = {axis: resolve_axis_range(range_flags[axis], profile, axis) for axis in (a1, a2)}

    max_speed_mm_min = profile.max_speed_mm_s * 60
    speed_start, speed_end = args.speed_range if args.speed_range else (6000, max_speed_mm_min)
    speed_step = args.speed_step if args.speed_step else 3000
    if speed_start <= 0 or speed_end > max_speed_mm_min:
        raise ValueError(
            f"--speed-range [{speed_start}, {speed_end}] exceeds {profile.display_name} "
            f"max speed {profile.max_speed_mm_s} mm/s ({max_speed_mm_min:g} mm/min)"
        )
    if speed_step <= 0 or speed_start >= speed_end:
        raise ValueError(f"invalid speed range/step: start={speed_start} end={speed_end} step={speed_step}")

    speed_sweep_warmup = resolve_speed(args.speed_sweep_warmup, 3000, profile, "speed-sweep-warmup")
    calibration_speed = resolve_speed(args.calibration_speed, 3000, profile, "calibration-speed")
    linear_speed = resolve_speed(args.linear_speed, 6000, profile, "linear-speed")
    circular_travel_speed = resolve_speed(args.circular_travel_speed, 2000, profile, "circular-travel-speed")
    circular_speed = resolve_speed(args.circular_speed, 6000, profile, "circular-speed")
    complex_speed = resolve_speed(args.complex_speed, 6000, profile, "complex-speed")
    drift_speeds = tuple(
        resolve_speed(v, v, profile, "drift-speeds") for v in (args.drift_speeds or [3000, 6000])
    )

    for axis in (a1, a2):
        margin_lo = bounds[axis][0] - profile.axis_limits(axis)[0]
        margin_hi = profile.axis_limits(axis)[1] - bounds[axis][1]
        if min(margin_lo, margin_hi) < profile.default_margin:
            print(
                f"warning: {axis} range {bounds[axis]} leaves less than the "
                f"recommended {profile.default_margin}mm margin from the physical limit",
                file=sys.stderr,
            )

    bed_value = profile.default_margin
    body = [
        f"; Generated by tools/gcode_generator.py for {profile.display_name}",
        f"; {a1} range: {bounds[a1]}  {a2} range: {bounds[a2]}  "
        f"speed sweep: F{speed_start:g}-F{speed_end:g} step {speed_step:g}",
        sections.move(6000, {a1: bounds[a1][0], profile.bed_axis: bed_value, a2: bounds[a2][0]}),
    ]
    body += sections.calibration_points(a1, a2, bounds, corner_feed=calibration_speed, seed=args.seed)
    body += sections.linear_ramp(a1, a2, bounds, feed=linear_speed)
    body += sections.circular_arc(a1, a2, bounds, f_travel=circular_travel_speed, feed=circular_speed)
    body += sections.speed_sweep(
        a1, a2, bounds, speed_start, speed_end, speed_step, warmup_feed=speed_sweep_warmup
    )
    body += sections.complex_points(a1, a2, bounds, feed=complex_speed, seed=args.seed + 1)
    body += sections.drift_shuttle(a1, a2, bounds, feeds=drift_speeds)

    start_text = profile.start_template.read_text(encoding="utf-8")
    end_text = profile.end_template.read_text(encoding="utf-8")
    return "\n".join([start_text.rstrip("\n"), "", *body, "", end_text.rstrip("\n"), ""])


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        gcode = build_gcode(args)
    except (KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        print(f"known printers: {', '.join(list_profiles())}", file=sys.stderr)
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(gcode, encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
