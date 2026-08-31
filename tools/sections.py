"""Parameterized benchmark section generators.

Each function returns the G-code lines for one test phase (a "Section" in
the shipped .gcode files), scaled to whatever axis1/axis2 travel range and
feedrates are passed in. Every phase follows the same shape as the shipped
A1 mini file: move to a target, then `G4 P<ms> ; pause for <n> seconds` to
hold for static measurement.
"""
from __future__ import annotations

import math
import random

Bounds = dict[str, tuple[float, float]]


def _num(v: float) -> str:
    if float(v).is_integer():
        return str(int(v))
    return f"{v:.3f}".rstrip("0").rstrip(".")


def move(feed: float | None, coords: dict[str, float]) -> str:
    parts = []
    if feed is not None:
        parts.append(f"F{_num(feed)}")
    parts.extend(f"{axis}{_num(val)}" for axis, val in coords.items())
    return "G0 " + " ".join(parts)


def pause(hold_ms: int = 6000) -> str:
    return f"G4 P{hold_ms} ; pause for {hold_ms // 1000} seconds"


def calibration_points(
    a1: str, a2: str, bounds: Bounds,
    n: int = 16, hold_ms: int = 6000,
    corner_feed: float = 3000, seed: int = 42,
) -> list[str]:
    a1_min, a1_max = bounds[a1]
    a2_min, a2_max = bounds[a2]
    rng = random.Random(seed)

    points: list[tuple[float | None, float, float]] = [(corner_feed, a1_min, a2_min)]
    points.append((None, a1_max, a2_max))
    for _ in range(max(n - 3, 0)):
        points.append((None, rng.uniform(a1_min, a1_max), rng.uniform(a2_min, a2_max)))
    points.append((None, a1_min, a2_min))

    lines = ["Section calibration"]
    for feed, x, z in points:
        lines.append(move(feed, {a1: round(x, 2), a2: round(z, 2)}))
        lines.append(pause(hold_ms))
    return lines


def linear_ramp(
    a1: str, a2: str, bounds: Bounds,
    feed: float = 6000, steps: int = 60, hold_ms: int = 6000,
) -> list[str]:
    a1_min, a1_max = bounds[a1]
    a2_min, a2_max = bounds[a2]

    lines = ["Section linear"]
    lines.append(move(feed, {a1: a1_min, a2: a2_min}))
    lines.append(pause(hold_ms))
    for i in range(1, steps + 1):
        t = i / steps
        x = a1_min + t * (a1_max - a1_min)
        z = a2_min + t * (a2_max - a2_min)
        lines.append(move(feed if i == 1 else None, {a1: round(x, 3), a2: round(z, 3)}))
    lines.append(pause(hold_ms))
    return lines


def circular_arc(
    a1: str, a2: str, bounds: Bounds,
    f_travel: float = 2000, feed: float = 6000, steps: int = 90, hold_ms: int = 6000,
) -> list[str]:
    a1_min, a1_max = bounds[a1]
    a2_min, a2_max = bounds[a2]
    cx, cz = (a1_min + a1_max) / 2, (a2_min + a2_max) / 2
    r = min(a1_max - a1_min, a2_max - a2_min) / 2

    lines = ["Section circular"]
    lines.append(move(f_travel, {a1: cx + r, a2: cz}))
    lines.append(pause(hold_ms))
    for i in range(1, steps + 1):
        theta = 2 * math.pi * i / steps
        x = cx + r * math.cos(theta)
        z = cz + r * math.sin(theta)
        lines.append(move(feed if i == 1 else None, {a1: round(x, 3), a2: round(z, 3)}))
    lines.append(pause(hold_ms))
    return lines


def speed_sweep(
    a1: str, a2: str, bounds: Bounds,
    speed_start: float, speed_end: float, speed_step: float,
    reps: int = 8, warmup_feed: float = 3000, warmup_reps: int = 5, hold_ms: int = 6000,
) -> list[str]:
    a1_min, a1_max = bounds[a1]
    a2_min, a2_max = bounds[a2]
    a2_mid = (a2_min + a2_max) / 2

    lines = ["Section speed_sweep"]
    lines.append(move(warmup_feed, {a2: round(a2_mid, 3)}))
    for i in range(warmup_reps * 2):
        x = a1_min if i % 2 == 0 else a1_max
        lines.append(move(warmup_feed if i == 0 else None, {a1: x}))
    lines.append(pause(hold_ms))

    speed = speed_start
    while speed <= speed_end:
        for i in range(reps * 2):
            x = a1_min if i % 2 == 0 else a1_max
            lines.append(move(speed if i == 0 else None, {a1: x}))
        lines.append(pause(hold_ms))
        speed += speed_step
    return lines


def complex_points(
    a1: str, a2: str, bounds: Bounds,
    n: int = 60, seed: int = 7, feed: float = 6000,
    region_fraction: float = 0.6, hold_ms: int = 6000,
) -> list[str]:
    a1_min, a1_max = bounds[a1]
    a2_min, a2_max = bounds[a2]
    cx, cz = (a1_min + a1_max) / 2, (a2_min + a2_max) / 2
    rx = (a1_max - a1_min) * region_fraction / 2
    rz = (a2_max - a2_min) * region_fraction / 2
    rng = random.Random(seed)

    lines = ["Section complex"]
    lines.append(move(feed, {a1: round(cx, 2), a2: round(cz, 2)}))
    for _ in range(max(n - 2, 0)):
        x = rng.uniform(cx - rx, cx + rx)
        z = rng.uniform(cz - rz, cz + rz)
        lines.append(move(None, {a1: round(x, 2), a2: round(z, 2)}))
    lines.append(move(None, {a1: a1_min, a2: a2_min}))
    lines.append(pause(hold_ms))
    return lines


def drift_shuttle(
    a1: str, a2: str, bounds: Bounds,
    feeds: tuple[float, ...] = (3000, 6000),
    reps: int = 5, hold_ms: int = 6000,
) -> list[str]:
    a1_min, a1_max = bounds[a1]
    a2_min, a2_max = bounds[a2]

    lines = ["Section drift"]
    lines.append(move(2000, {a1: a1_max}))
    lines.append(pause(hold_ms))

    for feed in feeds:
        for i in range(reps * 2):
            z = a2_max if i % 2 == 0 else a2_min
            lines.append(move(feed if i == 0 else None, {a2: z}))
        lines.append(pause(hold_ms))

    p1 = (a1_min + 0.3 * (a1_max - a1_min), a2_max - 0.05 * (a2_max - a2_min))
    p2 = (a1_max, a2_min)
    for feed in feeds:
        for i in range(reps * 2):
            x, z = p1 if i % 2 == 0 else p2
            lines.append(move(feed if i == 0 else None, {a1: round(x, 2), a2: round(z, 2)}))
        lines.append(pause(hold_ms))
    return lines
