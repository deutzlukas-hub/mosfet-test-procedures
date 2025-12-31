* MOSFET thermal noise test (common-source + resistor load)

.include ../tmp/modelcard.nmos
.include ../tmp/technology.params

.option temp=125.0
.option plotwinsize=0


Vdd dd 0 1.2

* Gate DC bias; AC=1 is only used for .noise input reference
Vg g 0 0.7 AC 1
N1 out g 0 0 NMOS W=10.0u L=0.09u
RL dd out 10k

.control
pre_osdi `echo "$OSDI"`
set wr_vecnames
set wr_singlescale
op
noise v(out) Vg dec 50 1 1e6
* active noise1 scope
setplot noise1
wrdata `echo "$FILEPATH"` frequency onoise_spectrum inoise_spectrum
.endc
.end






