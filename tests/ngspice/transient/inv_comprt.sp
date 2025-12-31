* 1-bit Digital Comparator Test Circuit A > B, A = B, A < B

.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.pmos
.include ../tmp/technology.params
.include ./not.sub
.include ./nand2.sub
.include ./nor2.sub
.include ./or2.sub
.include ./comprt.sub

* Power supply
Vdd vdd 0 {VNOM}

* Input sources (digital pulses)
VA A 0 PULSE(0 {VNOM} 0.1n 0.1n 0.1n 2.0n 4.0n)
VB B 0 PULSE(0 {VNOM} 1.1n 0.1n 0.1n 2.0n 4.0n)

* DUT
XCOMP A B A_GT_B A_LT_B A_EQ_B vdd 0 COMPRT L={L} WN={WN} WP={WP}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
tran 0.01n 4n
wrdata `echo "$FILEPATH"` v(A) v(B) v(A_GT_B) v(A_LT_B) v(A_EQ_B)
.endc

.end

