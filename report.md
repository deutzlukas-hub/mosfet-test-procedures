---
title: "Report: MOSFET Test Procedures"
author: Lukas Deutz 
date: 2025-12
geometry: margin=1in
header-includes:
  - \usepackage{microtype}
  - \setlength{\parindent}{0pt}
  - \setlength{\parskip}{6pt}
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \usepackage{graphicx}
  - \usepackage{booktabs}
---
\newcommand{\erel}{$\varepsilon_{\text{rel}}$ }

This report presents simulation results from the project's test suite using the
Gnucap and ngspice circuit simulators. Simulation outputs from both simulators
are quantitatively compared for cross-validation. The report covers individual
test cases including DC sweeps, AC analysis, transient analysis, and noise
analysis for different MOSFET device models using the cmos90 technology defined
in the cmos90.params file (L=0.9u W=10u and VNOM=1.2V).

All figures in this report are generated from the raw data included in the 
`results/reference` directory of this project. The data was produced using 
the simulator versions Gnucap 2025.12.18 and ngspice 45.2.

# Postprocessing

To compare simulation outputs from Gnucap and ngspice, the relative error \erel
as:

$$
\tag{1}
\varepsilon_{\text{rel}}=\frac{|x_{\text{Gnucap}} - x_{\text{ngspice}}|}{\max({|x_{\text{ngspice}}|, \, \text{atol}})}
\label{eq: rel_err}
$$

Here, $x$ denotes an output quantity such as node voltage or through current.
The absolute tolerance $\text{atol}=10^{-10}$ sets a lower bound for the
denominator, preventing division by zero when the reference approaches zero.

# DC Sweeps

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/bsim4/dc/id_vd_nmos_1.png}
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/psp104/dc/id_vd_nmos_1.png}
  \caption{NMOS Id-Vd characteristics for BSIM4 and PSP104 MOSFET models.
  (A) Drain current I(d) versus drain voltage V(d) for different gate voltages
  V(g) illustrating the impact of gate bias on NMOS behavior. Colored lines
  represent Gnucap results, overlaid by ngspice results shown as black dashed
  lines. (B) Relative error \erel between Gnucap and ngspice drain currents I(d)
  over V(d) for different gate voltages.}
  \label{fig:dc-compare}
\end{figure}

DC sweeps include single-device NMOS and PMOS I–V characterization across
varying gate, drain, and bulk voltages under nominal, low, and high temperature
conditions. Id-Vd curves obtained from the test case `id_vd_nmos_1` using the
BSIM4 and PSP104 MOSFET models are shown in Figure \ref{fig:dc-compare}. The
simulated characteristics exhibit the expected linear and saturation regions,
with cutoff behavior for gate voltages below threshold.

The relative error \erel between Gnucap and ngspice remains in the range of
$10^{-4}$ and $10^{-7}$, well within numerical tolerances for circuit
simulations. Figures for additional DC test cases are included in project's
repository. Across device models and test cases, Gnucap and ngspice produce
consistent characteristics within numerical tolerance.

# AC analysis

AC test cases include small-signal characterization for single-stage MOSFET
common-source, common-drain and common-gate amplifiers evaluated at different DC
operating points. The small-signal voltage gain $A_v=v_{out}/v_{in}$ of a common
source amplifier is examined as a function of frequency for different bias
conditions in Figure \ref{fig:ac-compare}. The results show a bias-dependent
flat midband gain followed by a high-frequency roll-off, limiting the amplifier
bandwidth.

Across the frequency range the relative error \erel in voltage gain between
Gnucap and ngspice remains on the order of $10^{-5}$. Figures for common-drain
and common-gate amplifiers are included in the project's repository. Consistent
with the DC analysis, Gnucap and ngspice produce matching AC characteristics
across device models and test cases within numerical tolerances.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/bsim4/ac/cs_amp.png}
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/psp104/ac/cs_amp.png}
  \caption{AC analysis of a single-stage common-source MOSFET amplifier with a
  passive resistor load for BSIM4 and PSP104 MOSFET models. (A) Small-signal
  voltage gain $A_v$ as a function of the AC input frequency for different gate
  bias $V_{\text{DC,in}}$ illustrating the impact of operating point on the
  transfer characteristics. Colored lines represent Gnucap results, overlaid by
  black dashed lines for ngspice results. (B) Relative error \erel in voltage
  gain $A_v$ between Gnucap and ngspice for different $V_{\text{DC,in}}$.}
  \label{fig:ac-compare}
\end{figure}

# Transient analysis

Transient test cases include basic logic gates — NOT, NAND, NOR, AND, and OR —
as well as inverter chains, ring oscillators, and comparators. The transient
simulation of a CMOS NAND gate is shown for BSIM4 and PSP104 MOSFET models in
Figure \ref{fig:trans-nand}. The output voltage demonstrates correct logical
behavior. The relative error \erel between Gnucap and ngspice output voltages is
in the order of $10^{-2}$, which is notably larger than for the DC and AC
analysis.

Figure \ref{fig:trans-inv_ring} shows the voltage waveform of a five-stage ring
oscillator. The output voltage is probed at the first inverter stage. Both
Gnucap and ngspice produce similar oscillatory behavior, with a relative error
of the order of $10^{-2}$.

Overall, transient simulations show good agreement between Gnucap and ngspice.
Logical gates exhibit correct logical behavior, with comparable rise times, fall
times, and propagation delays in both simulators (TODO). Notably, the relative
error for transient cases is larger, which can be attributed to differences in
time-step control and numerical integration between the two simulators.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/bsim4/transient/nand2.png}
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/psp104/transient/nand2.png}

  \caption{NAND gate transient analysis for BSIM4 and PSP104 MOSFET models. (A)
  Input voltages in Gnucap, overlaid with black dashed lines for ngspice. (B)
  Output voltage demonstrating correct NAND logic operation. (C) Relative error
  \erel in output voltage between Gnucap and ngspice.}
\label{fig:trans-nand}
\end{figure}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/bsim4/transient/inv_ring.png}
  \includegraphics[width=0.495\textwidth]{./results/reference/figures/cmos90/psp104/transient/inv_ring.png}
    \caption{5-stage ring oscillator transient analysis for BSIM4 and PSP104
    MOSFET models. (A) Voltage input trigger in Gnucap, overlaid with black
    dashed lines for ngspice. (B) Output voltage demonstrating sustained
    oscillation. (C) Relative error \erel in output voltage between Gnucap and
    ngspice.}
\label{fig:trans-inv_ring}
\end{figure}

# Noise analysis

Noise test cases analyze the power spectral density (PSD) of the built-in noise
models for a given MOSFET device as a function of input frequency. The voltage
noise PSD of PSP104 NMOS devices under low, nominal and high temperature
conditions is compared in Figure \ref{fig:noise-nmos}. At low frequencies, noise
is dominated by 1/f flicker noise, and PSD decreases with increasing frequency.
At mid to high frequencies, thermal noise dominates, and PSD becomes
approximately flat (white noise plateau). As expected, the noise contribution is
generally larger with higher temperatures. Both Gnucap and ngspice produce
similar noise PSD, with the relative error \erel between $10^{-5}$ and $10^{-7}$
across the entire frequency range for different temperatures.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{./results/reference/figures/cmos90/psp104/noise/nmos.png}
  \caption{Noise characteristics for PSP104. (A) Power spectral density (PSD) as
  a function of frequency for different temperatures illustrating thermal and
  flicker noise contributions. Colored lines represent Gnucap results, overlaid
  by black dashed lines for ngspice results. (B) Relative error \erel of the PSD
  between Gnucap and ngspice over frequency for different temperatures.}
\label{fig:noise-nmos}
\end{figure}



