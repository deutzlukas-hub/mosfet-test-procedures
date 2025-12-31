* NMOS Id-Vg with Vb

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params

vg 1 0 1.2
vb 3 0 0
vd 2 0 0.1

N1 2 1 0 3 NMOS W={WN} L={L}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
dc vg -0.6 1.2 0.02 vb 0.0 -1.2 -0.3
wrdata `echo "$FILEPATH"` v(3) i(vd)
.endc
.end