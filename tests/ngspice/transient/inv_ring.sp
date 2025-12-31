* Ring-oscillator (tran)
.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.pmos
.include ../tmp/technology.params
.include ./not.sub
.include ./inv_ring.sub

.option trtol=0.001;

* Power supply
Vdd vdd 0 {VNOM}

* Trigger gate pulse and NMOS to kick-start oscillation
Vin g_pulse 0 PULSE(0 {VNOM} 0.1n 0.01n 0.01n 0.2n)
Ntrig n1 g_pulse 0 0 NMOS W={WN} L={L}

* Ring oscillator DUT
XRING n1 vdd 0 INV_RING L={L} WN={WN} WP={WP}

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
tran 0.01n 4n
wrdata `echo "$FILEPATH"` v(g_pulse) v(n1)
.endc















