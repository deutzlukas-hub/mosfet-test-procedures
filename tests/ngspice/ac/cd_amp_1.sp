* Common-drain (source follower) amplifier AC test 1

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params
.include ./cd_amp.sub

Vdd dd 0 {VNOM}
Vin in 0 {0.4*VNOM} ac {0.05*VNOM}

Xcd in out dd 0 cd_stage W={WN} L={L}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
ac dec 10 100 1000Meg
wrdata `echo "$FILEPATH"` vdb(in) vdb(out)
.endc
.end
