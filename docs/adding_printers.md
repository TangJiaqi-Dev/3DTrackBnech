# Adding Custom Printers

If your printer is not in `/gcode`, you must generate a compatible motion file.

## Constraints
1.  **Build Volume:** Must accommodate $X: 0 \to 180$, $Y: 0 \to 180$ mm.
2.  **Velocity:** Max speed for benchmark consistency is $500$ mm/s.
3.  **Acceleration:** Set default printer acceleration to $10000$ mm/s².

## Generating G-Code
This is just a placeholder documentation. Will be published when the project is online.

## Submitting New Printers
If you successfully validate a new printer model:
1.  Fork the repository.
2.  Add your G-code to `/gcode`.
3.  Add your profile to `printer_profiles.yaml`.
4.  Submit a Pull Request with the tag `[NEW PRINTER]`.