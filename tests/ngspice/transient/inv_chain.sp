* Inverter chain (tran)

.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.pmos
.include ../tmp/technology.params
.include ./not.sub
.include ./inv_chain.sub

.option trtol=0.01;

Vdd vdd 0 {VNOM}
Vin in 0 PULSE(0 {VNOM} 1n 0.1n 0.1n 0.5n 1.4n)

XCHAIN in out vdd 0 INV_CHAIN L={L} WN={WN} WP={WP}

* Optional load capacitor
Cload out 0 10f

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
tran 0.001n 4n
wrdata `echo "$FILEPATH"` v(in) v(out)
.endc

.end












