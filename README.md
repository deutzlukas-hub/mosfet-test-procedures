# MOSFET Test Procedures

This project focuses on validating Verilog-A compact device models used in open 
Process Design Kits (PDKs). Open PDKs lower barriers to IC design and 
manufacturing by providing open, standardized design resources and reducing 
reliance on proprietary EDA formats. The goal is to enable reliable model 
quality assurance across open-source circuit simulators such as ngspice and
Gnucap. 

To achieve this, the project provides a modular and automated framework for 
validating the implementation of industry-standard MOSFET models [1] across 
two open-source toolchains:

1. **Gnucap** [2] + `modelgen-verilog` [3]
2. **ngspice** [4] + `OpenVAF` (OSDI) [5]

Using this framework, the project demonstrates quantitative agreement between the
Gnucap and ngspice simulators for different technology parameters and MOSFET
device models across a wide range of test cases (see report.pdf).

The modular framework is designed to be easily extensible to support additional 
toolchains, technologies, device models, and test cases.

## Project Structure

The repository structure is organized in `models`, `technology`, `tests`,
`results` and `python` subdirectories.
```
repo/
├─ models/                 # Compiled MOSFET device models
│  ├─ gnucap/              # Gnucap-generated shared libraries (.so) + parametersets
│  └─ ngspice/             # OpenVAF-generated OSDI files (.osdi) + modelcards
│
├─ technology/             # Global technology parameter files (e.g. cmos90.params)
│  ├─ gnucap/              # Gnucap-format parameters
│  └─ ngspice/             # ngspice-format parameters
│
├─ tests/                  # Test suite
│  ├─ gnucap/              # Verilog-AMS testbenches (.gc)
│  └─ ngspice/             # SPICE netlist testbenches (.sp)
│  # Test categories: DC, AC, transient, noise
│
├─ results/                # Simulation outputs
│  ├─ data/                # Raw simulation data (mirrors tests/)
│  │  ├─ gnucap/           # Gnucap outputs (.gc.out)
│  │  └─ ngspice/          # ngspice outputs (.sp.out)
│  ├─ figures/             # Plots generated from raw test data
│  ├─ reference/           # Reference outputs generated with stable version
│     ├─ data              # Reference simulation outputs (.gc.out, .sp.out)
│     └─ figures           # Figures generated from reference outputs
├─ python/                 # Scripts for parsing data and generating plots
│
├─ run_tests.sh            # Run full test suite
├─ run_tests_gnucap.sh     # Run Verilog-AMS test cases with Gnucap
└─ run_tests_ngspice.sh    # Run SPICE netlist test cases with ngspice
```

### Test suite

The test suite is organized into four categories: **DC sweeps**, **AC
analysis**, **transient analysis**, and **noise analysis**.

- DC sweeps include ID-VD and ID-VG characterization for NMOS and PMOS devices,
  based on reference test cases from Berkley BSIM group 
- AC tests include small-signal frequency response for common single-stage
  MOSFET amplifier topologies 
- Transient test cases analyse time-domain behaviour and include simple CMOS
  logic gates and basic analog circuits
- Noise test cases anaylse the built-in noise models of the MOSFET devices.

The test suite aims to provide a set of standard test cases for analog
simulation of MOSFET device models that can be built upon.

## Prerequisites

- **Gnucap** (reference files and figures were produced with version
  2025.12.18)
- **Ngspice** (reference files and figures were produced with version 45.2).
- **Python 3** (with `numpy` and `matplotlib`) for plotting.

## Running Tests

To run tests, clone the repository, and execute the main bash script from the
project's root directory:
```bash
./run_tests.sh <TECHNOLOGY=cmos90>
```
To run tests for a specific technology, model, with gnucap or ngspice use:
```bash
./run_tests_gnucap.sh <TECHNOLOGY> <model>
./run_tests_ngspice.sh <TECHNOLOGY> <model>
```
Currently, the models that are both supported in Gnucap and ngspice are bsim4
and psp104.

To regenerate the figures from exisisting raw data, run:
```
cd python
python plot_all_tests.py`.
```
## MOSFET device models

The Verilog-A source code for analog MOSFET transistor models is obtained from
the cmc standard [1]. The source code is compiled with the Gnucap
modelgen-verilog and OpenVAF compilers. Compiled model files and procedures for
building models from source are provided in the gnucap-models [5] and VA-Models
repositories [6]. Both repositories provide a good entry point to work with
MOSFET device models in Gnucap and ngspice, respectively.

The table below summarizes the CMC-standard MOSFET device models and their 
support status in Gnucap and ngspice.

| **Category**               | **Model**  | **Version**       | **Notes**                          | **Gnucap**             | **ngspice** |
| -------------------------- | ---------- | ----------------- | ---------------------------------- | ---------------------- |-------------|
| **Bulk MOSFET**            | BSIM-BULK  | v107.2.1          | Standard planar bulk MOSFET        | Smoke test fails       | Runs        |
|                            | BSIM4      | v4.8.0            | Legacy bulk MOSFET model           | Runs                   | Runs        |
|                            | PSP        | v104.0.1          | Surface-potential bulk CMOS        | Runs                   | Runs        |
|                            | HiSIM2     | v3.2.0            | Surface-potential model            | Model generation fails | Runs        |
| **SOI MOSFET**             | BSIM-SOI   | v4.7.0 / v100.1.1 | Standard SOI MOSFET                | WIP                    | Runs        |
|                            | HiSIM-SOI  | v1.5.0            | Surface-potential SOI MOSFET       | Model generation fails | Runs        |
|                            | HiSIM-SOTB | v1.3.0            | Ultra-low-power SOI MOSFET         | Model generation fails | Runs        |
|                            | L-UTSOI    | v102.x            | Fully-depleted SOI (FDSOI) MOSFET  | Model generation fails | Runs        |
| **Multi-Gate / 3D MOSFET** | BSIM-CMG   | latest            | Multi-gate / FinFET                | Smoke test fails       | Runs        |
|                            | BSIM-IMG   | latest            | Independent-gate multi-gate MOSFET | Smoke test fails       | Runs        |
| **High-Voltage MOSFET**    | HiSIM-HV   | latest            | High-voltage / LDMOS variants      | WIP                    | Runs        |

## Working with MOSFET device models

Gnucap allows MOSFET device models, parametersets, and technology files to be
loaded dynamically via command-line flags, enabling the same test suite to be
easily rerun with different configurations. Loaging models dynamically is
currently not supported in ngspice; as a workaround, we use environment
variables and placeholder technology and device modelcards that are automatically
updated during test execution. See`docs.md` for more details.

## Acknowledgements

This project was funded through the NGI0 Commons Fund, a fund established by 
NLnet with financial support from the European Commission's Next Generation 
Internet programme, under the aegis of DG Communications Networks, 
Content and Technology under grant agreement No 101135429. Additional funding 
is made available by the Swiss State Secretariat for Education, 
Research and Innovation (SERI).

## References
[1] Compact Model Coalition: https://si2.org/compact-model-coalition/
[2] GNU Circuit Analysis Package (Gnucap): http://www.gnucap.org/dokuwiki/doku.php?id=gnucap:start
[3] Gnucap modelgen-verilog: https://github.com/gnucap/modelgen-verilog
[4] ngspice simulator https://ngspice.sourceforge.io/
[5] OpenVAF compiler: https://openvaf.github.io/
[6] Gnucap models repository: https://codeberg.org/gnucap/gnucap-models.git
[7] Verilog-A Models respository: https://github.com/dwarning/VA-Models

