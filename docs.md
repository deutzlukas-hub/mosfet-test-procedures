# Working with MOSFET Device Models

### In Gnucap

Gnucap supports dynamic loading of device models, `modules` and `parametersets` via the -a and -i command line flags. 
For example, to run the DC sweep `./tests/gnucap/dc/id_vd_nmos.gc` with the BSIM4 model, execute the following command 
from the project's root directory:
```
gnucap -a mgsim \
-a ./models/gnucap/bsim4/bsim4.so \ 
-i ./technology/gnucap/cmos90.params
-i ./models/gnucap/bsim483/modelcards/nmos.paramset \ 
./tests/gnucap/dc/id_vd_nmos.gc > ./results/gnucap/dc/id_vd_nmos.gc.out 
```
The `>` operator redirects the simulator output to the specified file. To run the same tests with a different device 
models, model parametersets, or technology parameters, simply replace the corresponding `-a` and `-i` paths. 
See `run_tests_gnucap.sh` for an example of automated execution. 

Alternatively, device models, model parametersets, and technology parameters could also be loaded from within the test 
files using the `load` and `include` commands: 
```
load ./models/bsim483/bsim483.so
include ./technology/gnucap/cmos90.params
include ./models/bsim483/modelcards/nmos.paramset
```
However, this approach reduces flexibility, as test files must be modified to change models or technologies. Note that 
all paths specified in the test files are interpreted relative to the directory from which the Guncap command is executed.  

### In ngspice

ngspice does not support loading OSDI device models and modelcards via command-line flags. Instead, OSDI device models 
must be loaded from within the SPICE netlist using the `pre_osdi` command within a `.control` block (see ngspice manual 
[3] for more details):
```
.control
pre_osdi `path/to/model.osdi`
```
To execute the same netlist with different device models, the `pre_osdi` command can be combined with system environment 
variables. For example, the relevant code from the `.control` block in `tests/ngspice/dc/id_vd_nmos.sp` is shown 
below:
```
.control
pre_osdi `echo "$OSDI"`
...
.endc
```
Here, the `OSDI` environment variable specifies the path to the `.osdi` device model file and must be defined before the test
is executed. 

Technology parameters and device modelcards are included via the `.include` command, which does not expand environment 
variables. As a workaround, all ngspice tests include fixed paths:
```
.include ../tmp/technology.params
.include ../tmp/modelcard.nmos
.include ../tmp/modelcard.nmos
```
The files in `tests/ngspice/tmp/` are generated automatically during test execution (see `run_tests_ngspice.sh`) and 
contain the include statements pointing to the appropriate technology parameter file and modelcards. 