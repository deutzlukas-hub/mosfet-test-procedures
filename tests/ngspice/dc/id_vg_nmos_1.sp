* NMOS Id-Vg

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params

vg 1 0 1.2
vd 2 0 1.2

N1 2 1 0 0 NMOS W={WN} L={L}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
dc vg 0.0 1.2 0.02 vd 0.05 1.2 0.5
wrdata `echo "$FILEPATH"` v(2) i(vd)
.endc
.end



