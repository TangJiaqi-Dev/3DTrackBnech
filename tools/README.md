# G-code generator

Generates a 3DTrackBench benchmark `.gcode` file with an adjustable travel
range and speed range, instead of the fixed 180x180mm / F6000-F30000 ranges
baked into the files under `/Materials`.

Currently supports the **Bambu Lab A1 mini** only (`--printer a1_mini`).
Other printers use a different toolhead motion plane (see
`printer_profiles.yaml`) and need their own profile before they can be
generated this way.

## Setup

```
pip install pyyaml
```

## Usage

Reproduce the shipped file's default range and speed sweep:

```
python tools/gcode_generator.py --printer a1_mini --out out.gcode
```

Restrict the travel range and/or speed sweep:

```
python tools/gcode_generator.py --printer a1_mini \
  --x-range 40 140 --z-range 40 140 \
  --speed-range 6000 12000 --speed-step 3000 \
  --out out.gcode
```

Flags:
- `--printer` — printer id from `printer_profiles.yaml` (default `a1_mini`).
- `--x-range MIN MAX` / `--y-range MIN MAX` / `--z-range MIN MAX` — travel
  range in mm for whichever axes the printer's toolhead moves in (the A1
  mini uses X/Z; Y is the bed and isn't part of the traced path). Omit an
  axis to use the printer's full build volume minus its default safety
  margin.
- `--speed-range START END` — feedrate range in mm/min (G-code `F` units,
  e.g. `6000` = 100 mm/s) for the `speed_sweep` phase specifically.
- `--speed-step` — `speed_sweep`'s feedrate step size (default `3000`).
- `--seed` — RNG seed for the scattered-point sections (calibration,
  complex path). Same seed + same range always produces the same points.
- `--out` — output `.gcode` path (required).

`--speed-range`/`--speed-step` only control the `speed_sweep` phase (the
one that repeats a shuttle move at increasing feedrates). The other five
phases each move at their own fixed feedrate — these came from the shipped
A1 mini file with no documented rationale for the specific numbers, so
they're also exposed as flags rather than left hard-coded:

- `--speed-sweep-warmup` — `speed_sweep`'s warm-up feedrate (default `3000`).
- `--calibration-speed` — `calibration`'s corner-move feedrate (default `3000`).
- `--linear-speed` — `linear`'s feedrate (default `6000`).
- `--circular-travel-speed` — `circular`'s approach-move feedrate, before it
  starts tracing the arc (default `2000`).
- `--circular-speed` — `circular`'s arc-tracing feedrate (default `6000`).
- `--complex-speed` — `complex`'s feedrate (default `6000`).
- `--drift-speeds V1 V2 ...` — `drift`'s feedrates, one shuttle pass per
  value (default `3000 6000`).

All feedrate flags are validated against the printer's `max_speed_mm_s` and
rejected if they exceed it, same as `--speed-range`.

Requests that exceed the printer's build volume or max speed
(`printer_profiles.yaml`) are rejected with an error rather than silently
clamped, since running an out-of-range file risks a crash into the frame or
an endstop. A narrower range than the printer's default margin recommends
prints a warning but is still allowed.

## What it generates

The output has the same structure as the shipped files: printer-specific
start/end boilerplate (from `templates/<printer>/`, extracted verbatim from
Bambu Studio) wrapping a benchmark body with these phases, each ending in a
`G4` pause for static hold measurements:

1. **calibration** — static points scattered across the range (jitter).
2. **linear** — a corner-to-corner straight-line sweep (spatial accuracy).
3. **circular** — a full loop around the range's center (spatial accuracy).
4. **speed_sweep** — repeated shuttle moves at each feedrate in the
   configured speed range (robustness at speed).
5. **complex** — scattered points confined to a sub-region (stress test).
6. **drift** — repeated shuttle moves at increasing speed, single-axis then
   diagonal (drift / robustness).

The scattered-point sections use a seeded RNG rather than reproducing the
shipped file's exact coordinates (those came from an unpublished script),
so output is reproducible per seed but not byte-identical to the files
under `/Materials`.
