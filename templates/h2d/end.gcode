;===== date: 2025/05/16 =====================
;===== H2D =====================
G392 S0 ;turn off nozzle clog detect
M993 A0 B0 C0 ; nozzle cam detection not allowed.

M400 ; wait for buffer to clear

G90 ; absolute positioning
M141 S0 ; turn off chamber heating
M140 S0 ; turn off bed
M106 S0 ; turn off fan
M106 P2 S0 ; turn off remote part cooling fan
M106 P3 S0 ; turn off chamber cooling fan


M104 S0 T0; turn off hotend
M104 S0 T1; turn off hotend

M400 ; wait all motion done
M17 S ; enable steppers
M17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom
{if (max_layer_z + 100.0) < 320} ; check height limit
    G1 Z{max_layer_z + 100.0} F600 ; move Z up
    G1 Z{max_layer_z +98.0} ; move Z down slightly
{else} ; otherwise
    G1 Z320 F600 ; move Z to max
    G1 Z320 ; ensure Z at max
{endif} ; end check
M400 P100 ; wait 100ms
M17 R ; restore z current

M220 S100  ; Reset feedrate magnitude
M201.2 K1.0 ; Reset acc magnitude
M73.2   R1.0 ;Reset left time magnitude
M1002 set_gcode_claim_speed_level : 0 ; reset speed claim

M1015.4 S0 K0 ;disable air printing detect

M400 ; wait for buffer
M18 ; disable steppers
