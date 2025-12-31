* PMOS Id-Vg with Vb @ 100C

.include ../tmp/modelcard.pmos
.include ../tmp/technology.params

.options temp=100.0

vg 1 0 -1.2
vd 2 0 -0.1
vb 3 0  0.0

N1 2 1 0 3 PMOS W={WP} L={L}

.control
pre_osdi `echo "$OSDI"`
dc vg 0.6 -1.2 -0.02 vb 0 1.2 0.3
set wr_vecnames
set wr_singlescale
wrdata `echo "$FILEPATH"` v(3) i(vd)
.endc

.end

