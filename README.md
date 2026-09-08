# UCD Submission Research — Python + Colab Reproducibility

[![UCD reproducibility](https://github.com/rwisenrich/UCD-research/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/rwisenrich/UCD-research/actions/workflows/reproducibility.yml)

This public repository is the executable reproducibility layer for the UCD mathematical-physics research program. It contains deterministic Python constructions, numerical certificates, Google Colab runners, theorem indexes, and automated GitHub Actions checks.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run_python_suite.py
```

The quick suite reruns the parent projection, central vacuum selector, many-body Hnet finite diagnostics, SU(2) quantum-link plaquette, Maxwell bridge, one-loop RG refinement, and regulator-scaled gap calculation.

Run the complete public derivation suite with:

```bash
python run_python_suite.py --full
```

A manually triggered full GitHub-hosted run is also available under **Actions → UCD full reproducibility → Run workflow**. Its generated `results/` directory is uploaded as an Actions artifact.

## Google Colab

Run the public calculations directly in Google Colab:

[![Open master notebook in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/UCD_All_Toy_Simulations_Colab.ipynb)

Focused notebooks:

- [Parent Projection + Vacuum Selector](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/01_Parent_Projection_and_Vacuum_Selector.ipynb)
- [Many-Body Hnet](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/02_ManyBody_Hnet.ipynb)
- [SU(2) Quantum-Link Plaquette](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/03_SU2_Quantum_Link_Plaquette.ipynb)
- [Maxwell + RG + Gap](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/04_Maxwell_RG_Gap.ipynb)

Each notebook clones this repository at runtime, installs the pinned dependency ranges, and runs the public Python derivations from the repository itself.

## Live repository layout

- `scripts/` — Python derivations and finite-matrix constructions
- `results/` — baseline CSV/JSON numerical certificates
- `notebooks/` — Colab-ready runners
- `docs/THEOREM_INDEX.md` — theorem/result index
- `docs/EXTERNAL_LITERATURE.md` — external literature ledger
- `REPRODUCIBILITY.md` — paper-to-code/result map
- `.github/workflows/` — quick CI and manually triggered full-suite CI
- `requirements.txt` / `environment.yml` — reproducible environments

The manuscript PDFs and LaTeX source are maintained as a separate publication layer so that the executable repository can be cloned and tested independently of binary paper files.

## Reproducibility scope

The scripts reproduce the finite algebraic constructions and numerical diagnostics registered in the corresponding research calculations. The code writes machine-readable CSV/JSON results into `results/` so independent runs can be compared directly.

## Python versions

CI uses Python 3.11. The public code uses NumPy, SciPy, mpmath, and Matplotlib.
