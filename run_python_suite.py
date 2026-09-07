#!/usr/bin/env python3
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"

QUICK = [
    "derive_parent_projection.py",
    "derive_vacuum_selector.py",
    "derive_manybody_hnet.py",
    "build_su2_qlm_plaquette.py",
    "derive_maxwell_bridge.py",
    "derive_rg_flow.py",
    "derive_gap_criterion.py",
]

FULL = [
    "derive_native_sm_representation.py",
    "verify_native_sm_representation.py",
    "build_su2_qlm_plaquette.py",
    "derive_gauge_covariant_parent.py",
    "derive_parent_projection.py",
    "derive_vacuum_selector.py",
    "derive_manybody_hnet.py",
    "derive_locality_refinement.py",
    "derive_omega_reconstruction.py",
    "derive_native_flavor_completion.py",
    "derive_regge_volume_functional.py",
    "derive_color_atomic_spectral_chain.py",
    "derive_maxwell_bridge.py",
    "derive_dark_kernel_theorem.py",
    "derive_rg_flow.py",
    "derive_scalar_bundle.py",
    "derive_gravity_projection.py",
    "derive_frozen_cosmology_test.py",
    "derive_gap_criterion.py",
]

def main() -> int:
    p = argparse.ArgumentParser(description="Run the UCD Python reproducibility suite.")
    p.add_argument("--full", action="store_true", help="Run all derivation scripts instead of the quick public demo suite.")
    args = p.parse_args()
    suite = FULL if args.full else QUICK
    mode = "FULL" if args.full else "QUICK"
    print(f"UCD {mode} Python suite: {len(suite)} modules")
    for i, name in enumerate(suite, 1):
        path = SCRIPTS / name
        print(f"[{i:02d}/{len(suite):02d}] {name}", flush=True)
        cp = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), text=True, capture_output=True)
        if cp.returncode != 0:
            print(cp.stdout)
            print(cp.stderr, file=sys.stderr)
            return cp.returncode
    print("All selected modules completed successfully.")
    print(f"Results: {ROOT / 'results'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
