#!/usr/bin/env python3
"""
Plot all available tests for all supported models using the existing plotting modules:
- plot_dc
- plot_ac
- plot_transient
- plot_noise

This script iterates through supported models and invokes the plotting functions for
all standard test names, saving figures under results/figures/... per the existing
module conventions.

Usage examples:
  python plot_all_tests.py               # plot everything for all supported models
  python plot_all_tests.py --models bsim4 psp104
  python plot_all_tests.py --categories dc ac
"""
from __future__ import annotations

import argparse
import sys
from typing import Iterable, List

from util import supported_models

# Import plotting modules
import plot_dc as dc
import plot_ac as ac
import plot_transient as tr
import plot_noise as nz


DC_TESTS: List[str] = list(dc.dc_tests_dict.keys())
AC_TESTS: List[str] = ["cs_amp", "cd_amp", "cg_amp"]
TRANSIENT_LOGIC_GATES: List[str] = ["nand2", "nor2", "and2", "or2"]
# Transient standalone tests that have dedicated functions
TRANSIENT_TEST_FUNCS = [
    (tr.plot_not, {}),
    (tr.plot_inv_chain, {}),
    (tr.plot_inv_ring, {}),
    (tr.plot_comprt, {}),
    # (tr.plot_input_switch, {}),
]

def _run_safely(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except FileNotFoundError as e:
        print(f"[SKIP] Missing data for {fn.__name__}{args}: {e}")
    except AssertionError as e:
        # Many plotting functions assert that gnucap and ngspice sweeps match; skip if not.
        print(f"[SKIP] Assertion failed in {fn.__name__}{args}: {e}")
    except Exception as e:
        print(f"[WARN] Plot failed in {fn.__name__}{args}: {e}")

def plot_all_for_model(technology: str, model: str, categories: Iterable[str]):
    cats = set(c.lower() for c in categories)

    if "dc" in cats:
        print(f"== DC plots for {model} ==")
        for test in DC_TESTS:
            _run_safely(dc.plot_dc_sweeps, technology, model, test)

    if "ac" in cats:
        print(f"== AC plots for {model} ==")
        for test in AC_TESTS:
            _run_safely(ac.plot_amplifier, technology, model, test)

    if "transient" in cats:
        print(f"== Transient plots for {model} ==")
        # Logic gates with shared plotting function
        for gate in TRANSIENT_LOGIC_GATES:
            _run_safely(tr.plot_logic_gate, technology, model, gate)
        # Dedicated transient tests
        for fn, kw in TRANSIENT_TEST_FUNCS:
            _run_safely(fn, technology, model, **kw)

    if "noise" in cats:
        print(f"== Noise plots for {model} ==")
        # _run_safely(nz.plot_resistor_noise, model)
        _run_safely(nz.plot_nmos, technology, model)

def parse_args(argv: List[str]):
    p = argparse.ArgumentParser(description="Plot all tests for supported models.")
    p.add_argument(
        "--models",
        nargs="*",
        default=supported_models,
        help=f"Subset of models to plot (default: {supported_models})",
    )
    p.add_argument(
        "--categories",
        nargs="*",
        default=["dc", "ac", "transient", "noise"],
        choices=["dc", "ac", "transient", "noise"],
        help="Categories to plot (default: all)",
    )
    return p.parse_args(argv)


def main(argv: List[str] | None = None):
    args = parse_args(sys.argv[1:] if argv is None else argv)

    technology = 'cmos90'
    # Validate models intersection with supported_models
    chosen_models = [m for m in args.models if m in supported_models]
    unknown = [m for m in args.models if m not in supported_models]
    if unknown:
        print(f"[WARN] Unknown/unsupported models skipped: {unknown}")
    if not chosen_models:
        print("[ERROR] No valid models selected.")
        return 1

    for model in chosen_models:
        print(f"\n==== Plotting all selected categories for model: {model} ====")
        plot_all_for_model(technology, model, args.categories)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
