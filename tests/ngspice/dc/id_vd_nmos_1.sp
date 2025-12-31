* NMOS Id-Vd

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params

vg 1 0 1.2
vd 2 0 1.2

N1 2 1 0 0 NMOS W={WN} L={L}

.control
set wr_vecnames
set wr_singlescale
pre_osdi `echo "$OSDI"`
dc vd 0.0 1.2 0.02 vg 0.2 1.2 0.2
wrdata `echo "$FILEPATH"` v(1) i(vd)
.endc
.end