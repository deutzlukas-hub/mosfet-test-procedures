* =============================================================================
* Circuit    : CMOS NAND2 Gate
* Description: 2 PMOS + 2 NMOS
*
* Author     : Wuqiong Zhao (me@wqzhao.org)
* Date       : 2023-06-01
* License    : MIT
* =============================================================================

.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.pmos
.include ../tmp/technology.params
.include ./or2.sub

.option trtol=0.001;

Vdd vdd 0 {VNOM}

* Input in1: rises later than in2
Vin1 in1 0 PULSE(0 {VNOM} 0.1n 0.1n 0.1n 2.0n 4.0n)
Vin2 in2 0 PULSE(0 {VNOM} 1.1n 0.1n 0.1n 2.0n 4.0n)

XOR in1 in2 out vdd 0 OR2 L={L} WN={WN} WP={WP}
Cload out 0 10f

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
tran 0.01n 4n
wrdata `echo "$FILEPATH"` v(in1) v(in2) v(out)
.endc







