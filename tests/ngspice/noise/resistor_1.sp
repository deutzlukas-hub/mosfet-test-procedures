* MOSFET thermal noise test (common-source + resistor load)

.option temp=-40

* Resistor under test
R1 n1 gnd 1k
* Reference input source .noise
Iin n1 0 AC 1 DC 0

.control
set wr_vecnames
set wr_singlescale

op
noise v(n1) Iin dec 20 1 1e6

setplot noise1
wrdata `echo "$FILEPATH"` frequency onoise_spectrum inoise_spectrum
.endc
.end






