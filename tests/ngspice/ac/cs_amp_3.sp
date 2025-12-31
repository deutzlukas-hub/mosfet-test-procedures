* Single stage gate amplifier (ac)

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params
.include ./cs_amp.sub

Vdd dd 0 {VNOM}
Vin in 0 {0.6*VNOM} ac {0.05*VNOM}

Xcs in d dd 0 cs_stage W={WN} L={L}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
ac dec 10 100 1000Meg
wrdata `echo "$FILEPATH"` vdb(in) vdb(d)
.endc
.end


