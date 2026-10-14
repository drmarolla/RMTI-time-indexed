# Copyright 2026 Cesar Marolla
# Licensed under the Apache License, Version 2.0 (see LICENSE).
"""
reproduce.py -- regenerate every numerical result in this repository from code.

    python reproduce.py            # print the full report
    python reproduce.py --check    # compare with ../docs/reproduce_expected_output.txt
    python reproduce.py --write    # refresh the expected-output file (maintainers)

The report is deterministic: no random numbers, clocks or network access.
Sections:
  1. Disaster / climate cohort (module self-check against published tables)
  2. HCC oncology cohorts (module self-check against published tables)
  3. Time-indexed trajectory examples (synthetic) and filter gains

All trajectory examples are SYNTHETIC. No patient data are used anywhere.
"""
import contextlib
import io
import os
import runpy
import sys
from dataclasses import replace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
EXPECTED = os.path.join(HERE, "..", "docs", "reproduce_expected_output.txt")

from core.rmti_core import __version__                                   # noqa: E402
from dynamic.rmti_dynamic import (HCC_PARAMS, run_trajectory,            # noqa: E402
                                  steady_state_gains)


def _run_module(relpath):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(os.path.join(HERE, relpath), run_name="__main__")
    return buf.getvalue().rstrip("\n")


def _trajectory_section():
    out = []
    al, be = steady_state_gains()
    out.append(f"steady-state gains (q_level 0.05, q_slope 0.01, r_obs 0.8): "
               f"alpha = {al:.4f}, beta = {be:.4f}  (workbook: 0.41, 0.09)")
    examples = {
        "T-A (AL falling, adherence rising)": ([2, 1, 1, 0], [.40, .55, .70, .75]),
        "T-B (AL rising, adherence flat)":    ([2, 3, 4, 5], [.40, .40, .35, .35]),
    }
    out.append("fixed inputs: L = 0.30, E = 0.65, C = 3, rho(0) = 0.20; HCC parameters")
    for name, (y, d) in examples.items():
        on = run_trajectory(.30, .65, 3, .20, y, d, HCC_PARAMS)
        off = run_trajectory(.30, .65, 3, .20, y, d, replace(HCC_PARAMS, filter_on=False))
        out.append(f"\n{name}")
        out.append("  t   AL  adh    rho   V*(on)  R(off)   R(on)   tier(on)")
        for a, b in zip(on, off):
            out.append(f"  {a['t']}  {a['y']:>2}  {a['delivery']:.2f}  {a['rho']:.3f}  "
                       f"{a['V']:.4f}  {b['R']:.4f}  {a['R']:.4f}   {a['tier']}")
    return "\n".join(out)


def build_report():
    bar = "=" * 70
    parts = [f"RMTI reproduction report -- core v{__version__}", bar,
             "SECTION 1. Disaster / climate cohort", bar, _run_module("disaster_climate/rmti_ssa.py"),
             "", bar, "SECTION 2. HCC oncology cohorts", bar, _run_module("oncology/rmti_hcc.py"),
             "", bar, "SECTION 3. Time-indexed trajectory examples (synthetic)", bar,
             _trajectory_section(), ""]
    return "\n".join(parts)


def main(argv):
    report = build_report()
    if "--write" in argv:
        with open(EXPECTED, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
        print("wrote", os.path.normpath(EXPECTED))
        return 0
    if "--check" in argv:
        try:
            with open(EXPECTED, encoding="utf-8") as f:
                want = f.read()
        except FileNotFoundError:
            print("expected-output file not found:", os.path.normpath(EXPECTED))
            return 2
        if want.replace("\r\n", "\n") == report:
            print("OK: output matches docs/reproduce_expected_output.txt "
                  f"({len(report.splitlines())} lines)")
            return 0
        import difflib
        diff = difflib.unified_diff(want.splitlines(), report.splitlines(),
                                    "expected", "actual", lineterm="", n=1)
        print("MISMATCH:\n" + "\n".join(list(diff)[:40]))
        return 1
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
