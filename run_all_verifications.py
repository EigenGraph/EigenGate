#!/usr/bin/env python3
"""
run_all_verifications.py
========================
Unified single-entry-point verification runner for the dissertation research repository
"Adjusted Redundancy Index (ARI)" — Harids Irawan (2026).

Executes the full deterministic test and layered verification suite:
  1. Axial Truss Reference Solver Verification (Table 13 / Table 4.1)
  2. Two-Bar Computational Chain Tutorial (Table 25 / Table 4.11)
  3. ARI Core Engine & Unit Invariance Test (Table 15 / Table 4.3)
  4. SVD Kinematic Guard Verification (Eqs. 4.1–4.7 & Table 16 / Table 4.4)
  5. Pre-Analysis Bound & Anti-Information Leakage Audit
  6. Full Canonical Verification Suite (68/68 Automated Checks)
  7. Safeguard Package & 16 Parametric Models Verification (272 Scenarios)
  8. Multi-Family Finite Element Solver Test Suite (S1–S5)

How to run from repository root:
    python3 run_all_verifications.py
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
EXAMPLES_DIR = ROOT_DIR / "examples"

VERIFICATION_SUITE = [
    ("1. Axial Truss Reference Solver (M1–M4)", "test_truss_reference.py"),
    ("2. Analytical Two-Bar Parallel Tutorial", "ari_tutorial.py"),
    ("3. ARI Core Engine & Unit Invariance", "test_ari.py"),
    ("4. SVD Kinematic Guard (h_e)", "mechanical_guard.py"),
    ("5. Pre-Analysis Bounds (Bound Enhancement)", "test_bound_enhancement.py"),
    ("6. Information Anti-Leakage Audit", "test_leakage_audit.py"),
    ("7. Full Canonical Verification (68/68 Checks)", "run_verification.py"),
    ("8. Safeguard Diagnostics & 16 Parametric Models (272 Scenarios)", "run_guard_verification.py"),
    ("9. Multi-Family Finite Element Solver (S1–S5)", "test_structural_solvers.py"),
    ("10. Full Validation of ARI v2 on 300 Parent Models (S1–S5)", "run_screening_v2.py"),
    ("11. Screening Integration ARI v2–GNN (StructGNN-CRC v1.0)", "run_gnn_integration_s6.py"),
]


def main() -> int:
    print("=" * 78)
    print("UNIFIED VERIFICATION SUITE — ADJUSTED REDUNDANCY INDEX (ARI)")
    print("=" * 78)

    results = []
    t0_all = time.perf_counter()

    for label, script_name in VERIFICATION_SUITE:
        script_path = EXAMPLES_DIR / script_name
        print(f"\n>>> Running {label} ({script_name})...")
        t0 = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(EXAMPLES_DIR),
            capture_output=True,
            text=True,
        )
        dt = time.perf_counter() - t0
        passed = proc.returncode == 0
        status_str = "PASSED" if passed else f"FAILED (EXIT {proc.returncode})"
        print(f"    Status: {status_str} [{dt:.2f} s]")
        if not passed:
            print("    --- STDOUT ---")
            print(proc.stdout[-1200:] if proc.stdout else "(empty)")
            print("    --- STDERR ---")
            print(proc.stderr[-1200:] if proc.stderr else "(empty)")
        results.append((label, script_name, passed, dt))

    total_dt = time.perf_counter() - t0_all
    n_pass = sum(1 for _, _, ok, _ in results if ok)
    n_total = len(results)

    print("\n" + "=" * 78)
    print("VERIFICATION RESULTS SUMMARY — ARI REPOSITORY")
    print("=" * 78)
    print(f"{'Verification Stage':<52} | {'Status':<12} | {'Time':>8}")
    print("-" * 78)
    for label, _, ok, dt in results:
        st = "PASSED" if ok else "FAILED"
        print(f"{label:<52} | {st:<12} | {dt:>6.2f} s")
    print("-" * 78)
    print(f"Total Passed Stages: {n_pass}/{n_total} | Total Execution Time: {total_dt:.2f} seconds")
    print("=" * 78)

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
