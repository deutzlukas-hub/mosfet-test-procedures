* CMOS NAND test circuit

.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.pmos
.include ../tmp/technology.params

.include and2.sub

.option trtol=0.01;

Vdd vdd 0 {VNOM}

Vin1 in1 0 PULSE(0 {VNOM} 0.1n 0.1n 0.1n 2.0n 4.0n)
Vin2 in2 0 PULSE(0 {VNOM} 1.1n 0.1n 0.1n 2.0n 4.0n)

XAND in1 in2 out vdd 0 AND2 L={L} WN={WN} WP={WP}
Cload out 0 10f

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
tran 0.01n 4n
wrdata `echo "$FILEPATH"` v(in1) v(in2) v(out)
.endc







