## Bambu Lab X1C Instructions

**CRITICAL WARNING:** The X1C toolhead travels beneath the top frame perimeter. You must follow this setup exactly. Deviating will cause the attached marker to collide with the printer frame.

### Setup and Execution Procedure

1. **Clear Toolhead:** Ensure the toolhead is free of any attachments before starting.
2. **Home Printer:** Select "Home" in the manual control interface.
3. **Verify Position:** Confirm the toolhead is strictly centered on the X and Y axes. Z-height does not matter. **Do not proceed if the head is not centered.**
4. **Maintain Lock:** Do not manually move the toolhead. The motors must remain engaged to hold the center position. The benchmark must always start and end at this coordinate. You cannot rerun 'home' with the attachment in place.
5. **Attach Marker:** Install the marker attachment now.
6. **Execute:** Run the positioning or benchmark script.
7. **Repeat:** Both scripts terminate with the toolhead centered. You may immediately rerun the benchmark from this state.

8. **Teardown:** Remove the marker attachment immediately after testing. **Do not** attempt standard printing or other operations with the attachment in place.
