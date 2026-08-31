; HEADER_BLOCK_START
; BambuStudio 02.00.01.50
; model printing time: 36s; total estimated time: 5m 49s
; total layer number: 3
; total filament length [mm] : 3.24
; total filament volume [cm^3] : 7.80
; total filament weight [g] : 0.01
; filament_density: 1.26
; filament_diameter: 1.75
; max_z_height: 1.20
; HEADER_BLOCK_END

; CONFIG_BLOCK_START
default_acceleration = 10000
default_jerk = 0
machine_max_acceleration_travel = 10000,10000
machine_max_acceleration_x = 10000,10000
machine_max_acceleration_y = 10000,10000
machine_max_acceleration_z = 10000,10000
machine_max_jerk_x = 0
machine_max_jerk_y = 0
machine_max_jerk_z = 0
machine_max_speed_x = 500,200
machine_max_speed_y = 500,200
machine_max_speed_z = 100,200
travel_acceleration = 10000
travel_jerk = 0
travel_speed = 500
travel_speed_z = 100
; CONFIG_BLOCK_END

; EXECUTABLE_BLOCK_START
M73 P0 R8
M201 X10000 Y10000 Z10000 E5000
M203 X500 Y500 Z100 E30
M204 P10000 R10000 T10000
M205 X0 Y0 Z0 E0
M106 S0
M106 P2 S0
M104 S1 ; set nozzle temperature
; FEATURE: Custom
;===== machine: A1 mini =========================
;===== date: 20240620 =====================

;===== start to heat heatbead&hotend==========
M1002 gcode_claim_action : 2
M1002 set_filament_type:PLA

G392 S0 ;turn off clog detect
M9833.2
;=====start printer sound ===================

;=====avoid end stop =================
G91
G380 S2 Z30 F1200
G380 S3 Z-20 F1200
G1 Z5 F1200
G90

;===== reset machine status =================
M204 S10000

M630 S0 P0
G91
M17 Z0.3 ; lower the z-motor current

G90
M17 X0.7 Y0.9 Z0.5 ; reset motor current to default
M960 S5 P1 ; turn on logo lamp
G90
M83
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate
M73.2   R1.0 ;Reset left time magnitude
;====== cog noise reduction=================
M982.2 S1 ; turn on cog noise reduction

;===== prepare print temperature and material ==========
M400
M18
M400
M17
M17 X0.9 Y0.9 Z1.4 ; Set higher motor currents
M400
G28 X

M211 X0 Y0 Z0 ;turn off soft endstop ; turn off soft endstop to prevent protential logic problem

M975 S0 ; turn on


M620 M ;enable remap
M620 S0A   ; switch material if AMS exist
    G392 S0 ;turn on clog detect
    M1002 gcode_claim_action : 4
    M400
    M1002 set_filament_type:UNKNOWN
    M400
    T0
    M400
    M620.1 E F12.4725 T0
    ;M109 S250 ;set nozzle to common flush temp
    M106 P1 S0
    G92 E0
M73 P8 R5
    M400
    M1002 set_filament_type:PLA
    ;M104 S0
    G92 E0
    M400
    M106 P1 S178
    G92 E0
M73 P12 R5
    G92 E0

M73 P81 R1
    G392 S0 ;turn off clog detect
M621 S0A

M400
M106 P1 S0


;===== wait heatbed  ====================
M1002 gcode_claim_action : 2


M73 P89 R0
G1 Z5 F3000
G29.2 S1
;===== bed leveling ==================================

;===== bed leveling end ================================

;===== home after wipe mouth============================
M1002 judge_flag g29_before_print_flag
M622 J0

    M1002 gcode_claim_action : 13
    G28 T145

M623

;===== home after wipe mouth end =======================

M975 S0 ; turn on vibration supression
;===== nozzle load line ===============================

;===== extrude cali test ===============================

;========turn off light and wait extrude temperature =============
M1002 gcode_claim_action : 0

M400 ; wait all motion done before implement the emprical L parameters

;===== for Textured PEI Plate , lower the nozzle as the nozzle was touching topmost of the texture when homing ==
;curr_bed_type=Textured PEI Plate

G29.1 Z-0.02 ; for Textured PEI Plate


M960 S1 P0 ; turn off laser
M960 S2 P0 ; turn off laser
M106 S0 ; turn off fan
M106 P2 S0 ; turn off big fan
M106 P3 S0 ; turn off chamber fan

M975 S0 ; turn on mech mode supression
G90
M83
T1000

M211 X0 Y0 Z0 ;turn off soft endstop
M1007 S1

; xxxxx - End of start code
