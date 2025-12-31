* NMOS Id-Vd @ 100C

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params

.options temp=100.0

vg 1 0 1.2
vd 2 0 1.2

N1 2 1 0 0 NMOS W={WN} L={L}

.control
pre_osdi `echo "$OSDI"`
dc vd 0 1.2 0.02 vg 0 1.2 0.2
set wr_vecnames
set wr_singlescale
wrdata `echo "$FILEPATH"` v(1) i(vd)
.endc
.end

