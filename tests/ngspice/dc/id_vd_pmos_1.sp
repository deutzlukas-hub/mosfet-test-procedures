* PMOS Id-Vd

.include ../tmp/modelcard.pmos
.include ../tmp/technology.params

vg 1 0 -1.2
vd 2 0 -1.2

N1 2 1 0 0 PMOS W={WP} L={L} NF=5

.control
pre_osdi `echo "$OSDI"`
dc vd 0.0 -1.2 -0.02 vg -0.2 -1.2 -0.2
set wr_vecnames
set wr_singlescale
wrdata `echo "$FILEPATH"` v(1) i(vd)
.endc
.end