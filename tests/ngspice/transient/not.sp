* Not-gate (tran)

.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.pmos
.include ../tmp/technology.params

.include not.sub

.option trtol=0.001;

Vdd vdd gnd {VNOM}
Vin in gnd PULSE(0 {VNOM} 1n 0.1n 0.1n 0.5n 1.4n)
X1 in out vdd gnd NOT L={L} WN={WN} WP={WP}
Cload out gnd 10f

.control
pre_osdi `echo "$OSDI"`
tran 0.01n 4n
set wr_vecnames
set wr_singlescale
wrdata `echo "$FILEPATH"` v(in) v(out)
.endc
.end

