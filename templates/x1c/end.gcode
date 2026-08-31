;===== date: 20240528 =====================
M400 ; wait for buffer to clear
G1 X128 Y128 F2000 ; move to safe pos

M140 S0 ; turn off bed
M106 S0 ; turn off fan
M106 P2 S0 ; turn off remote part cooling fan
M106 P3 S0 ; turn off chamber cooling fan
M104 S0 ; turn off hotend

M622.1 S1 ; for prev firmware, default turned on


M400 ; wait all motion done
M17 S ; enable steppers
M17 Z0.4 ; lower z motor current to reduce impact if there is something in the bottom
M400 P100 ; wait 100ms
M17 R ; restore z current

M220 S100  ; Reset feedrate magnitude
M201.2 K1.0 ; Reset acc magnitude
M73.2   R1.0 ;Reset left time magnitude
M1002 set_gcode_claim_speed_level : 0 ; reset speed claim

M17 X0.8 Y0.8 Z0.5 ; lower motor current to 45% power
M960 S5 P0 ; turn off logo lamp
