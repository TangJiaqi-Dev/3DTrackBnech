; HEADER_BLOCK_START
; BambuStudio 02.04.00.70
; model printing time: 19s; total estimated time: 8m 28s
; total layer number: 3
; total filament length [mm] : 110.22
; total filament volume [cm^3] : 265.11
; total filament weight [g] : 0.35
; filament_density: 1.32
; filament_diameter: 1.75
; max_z_height: 0.68
; filament: 1
; HEADER_BLOCK_END

; CONFIG_BLOCK_START
default_acceleration = 10000
default_jerk = 0
machine_max_acceleration_extruding = 10000,10000
machine_max_acceleration_retracting = 10000,10000
machine_max_acceleration_travel = 10000,10000
machine_max_acceleration_x = 10000,10000
machine_max_acceleration_y = 10000,10000
machine_max_acceleration_z = 500,500
machine_max_jerk_x = 0
machine_max_jerk_y = 0
machine_max_jerk_z = 0
machine_max_speed_x = 500,500
machine_max_speed_y = 500,500
machine_max_speed_z = 20,20
travel_acceleration = 10000
travel_jerk = 0
travel_speed = 500
travel_speed_z = 20
; CONFIG_BLOCK_END

; EXECUTABLE_BLOCK_START
M73 P0 R8
M201 X10000 Y10000 Z500 E5000
M203 X500 Y500 Z20 E30
M204 P10000 R5000 T10000
M205 X0 Y0 Z0 E0
M106 S0
M106 P2 S0
M104 S1 ; set nozzle temperature

; FEATURE: Custom

;===== machine: X1-0.4 ====================
;===== date: 20251031 ==================
;===== start printer sound ================
M17 ; Enable stepper motors
M400 S1 ; Wait for moves to finish


;===== reset machine status =================
M290 X40 Y40 Z2.6666666 ; Set baby stepping / offset
G91 ; Set relative positioning
M17 Z0.4 ; lower the z-motor current
G380 S2 Z30 F300 ; G380 is same as G38; lower the hotbed , to prevent the nozzle is below the hotbed
G380 S2 Z-25 F300 ; Probe bed downwards
G1 Z5 F300 ; Move Z up 5mm
G90 ; Set absolute positioning
M17 X1.2 Y1.2 Z0.75 ; reset motor current to default
G90 ; Set absolute positioning
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate
M73.2   R1.0 ;Reset left time magnitude
M1002 set_gcode_claim_speed_level : 5 ; Set speed claim level
G29.1 Z{+0.0} ; clear z-trim value first
M204 S10000 ; init ACC set to 10m/s^2
M106 P1 S0 ; Turn off part fan


;========turn off light and wait extrude temperature =============
M1002 gcode_claim_action : 0 ; Claim action 0 (Start print)
M973 S4 ; Turn off scanner
M400 ; Wait all motion done before implement the emprical L parameters
M960 S1 P0 ; Turn off laser
M960 S2 P0 ; Turn off laser
M106 S0 ; Turn off fan
M106 P2 S0 ; Turn off big fan
M106 P3 S0 ; Turn off chamber fan

M975 S0 ; Turn off mech mode supression
G90 ; Set absolute positioning
M83 ; Set extruder relative mode
T1000 ; Select tool 1000
G92 X128 Y128



; Time to print!!!!!
; GCode created with FullControl - tell us what you're printing!
; info@fullcontrol.xyz or tag FullControlXYZ on Twitter/Instagram/LinkedIn/Reddit/TikTok
G0 F6000 X41 Y51 Z1
; Fastest axis bed size: 260, Slowest Axis bed size280
G4 P2000 ; pause for 2 seconds
G0 F3000 X219
G4 P2000 ; pause for 2 seconds
G0 Y229
G4 P2000 ; pause for 2 seconds
G0 X41
G4 P2000 ; pause for 2 seconds
G0 X129.5 Y139.5
G4 P20000 ; pause for 10 seconds
G0 X41 Y51
G4 P2000 ; pause for 2 seconds
G0 X219
G4 P2000 ; pause for 2 seconds
G0 Y229
G4 P2000 ; pause for 2 seconds
G0 X41
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
