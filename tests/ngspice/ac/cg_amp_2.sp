* Common-gate amplifier AC test 2

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params
.include ./cg_amp.sub

Vdd dd 0 {VNOM}
* Drive the source node; gate is at ground in subckt
Vin in 0 {-0.5*VNOM} ac {0.05*VNOM}

Xcg in out dd 0 cg_stage W={WN} L={L}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
ac dec 10 100 1000Meg
wrdata `echo "$FILEPATH"` vdb(in) vdb(out)
.endc
.end
