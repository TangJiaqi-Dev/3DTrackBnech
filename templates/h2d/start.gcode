; HEADER_BLOCK_START
; BambuStudio 02.04.00.70
; model printing time: 11s; total estimated time: 6m 45s
; total layer number: 3
; total filament length [mm] : 20.51
; total filament volume [cm^3] : 49.33
; total filament weight [g] : 0.07
; filament_density: 1.32
; filament_diameter: 1.75
; max_z_height: 0.68
; filament: 1
; HEADER_BLOCK_END

; CONFIG_BLOCK_START
default_acceleration = 10000,10000
default_jerk = 0
machine_max_acceleration_extruding = 10000,10000,10000,20000
machine_max_acceleration_retracting = 10000,10000,10000,10000
machine_max_acceleration_travel = 10000,10000,10000,10000
machine_max_acceleration_x = 10000,10000,10000,10000
machine_max_acceleration_y = 10000,10000,10000,10000
machine_max_acceleration_z = 500,500,500,500
machine_max_jerk_x = 0,0,0,0
machine_max_jerk_y = 0,0,0,0
machine_max_jerk_z = 0,0,0,0
machine_max_speed_x = 500,500,500,500
machine_max_speed_y = 500,500,500,500
machine_max_speed_z = 30,30,30,30
travel_acceleration = 10000,10000
travel_jerk = 0
travel_speed = 500,500
travel_speed_z = 30,30
; CONFIG_BLOCK_END

; EXECUTABLE_BLOCK_START
M73 P0 R8
M201 X10000 Y10000 Z10000 E5000
M203 X500 Y500 Z30 E50
M204 P10000 R5000 T10000
M205 X0 Y0 Z0 E0
M106 S0
M106 P2 S0
M104 S1 ; set nozzle temperature
; FEATURE: Custom
;===== machine: H2D start ======
;===== date: 20251022 =====================

M400 ; Wait for moves to finish

;===== reset machine status =================
M204 S10000 ; Set acceleration
M630 S0 P0 ; Reset leveling data

G90 ; Absolute positioning
M17 D ; reset motor current to default
M960 S5 P1 ; turn on logo lamp
G90 ; Absolute positioning
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate
M73.2   R1.0 ;Reset left time magnitude
G29.1 Z{+0.0} ; clear z-trim value first
M983.1 M1 ; Reset toolhead offset
M901 D4 ; Set motor drive mode
M481 S0 ; turn off cutter pos comp
;===== reset machine status =================


;===== avoid end stop =================
G91 ; Relative positioning
G380 S2 Z27 F1200 ; Move Z to avoid endstop
G380 S2 Z-12 F1200 ; Move Z back
G90 ; Absolute positioning
;===== avoid end stop =================

;==== set airduct mode ==== 
M106 P2 S0 ; turn off auxiliary fan
M106 P3 S0 ; turn off chamber fan
;==== set airduct mode ====

;====== cog noise reduction=================
M982.2 S1 ; turn on cog noise reduction

;===== first homing start =====
M1002 gcode_claim_action : 13 ; Set action status
G28 X T300 ; Home X
M972 S24 P0 T2000 ; Bed leveling sensor check

{if curr_bed_type=="Textured PEI Plate"}
M972 S26 P0 C0 ; Sensor check
{else}
M972 S36 P0 C0 X1 ; Sensor check
{endif}
M972 S35 P0 C0 ; Sensor check

M1009 Q1 L1 ; Service mode enter
G90 ; Absolute positioning
G1 X175 Y160 F30000 ; Move to center
G28 Z P0 T250 ; Home Z
M1009 Q1 L0 ; Service mode exit

;===== first homing end =====

M400 ; Wait for moves to finish

M1002 gcode_claim_action : 0 ; Set action status
M400 ; Wait for moves to finish



;========turn off light and fans =============
M960 S1 P0 ; turn off laser
M960 S2 P0 ; turn off laser
M106 S0 ; turn off fan
M106 P2 S0 ; turn off big fan

;============set motor current==================


M975 S0 ; turn off mech mode supression
M983.4 S1 ; turn on deformation compensation 
G29.7 S1 ; Enable mesh fade
M400 ; Wait for moves to finish


M211 Z1 ; Enable Z soft endstop
G29.99 ; End leveling
