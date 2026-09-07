# UCD Submission Research — Python + Colab Reproducibility Release

This repository is the public reproducibility companion to the UCD mathematical-physics manuscript suite. It contains the papers, LaTeX sources, deterministic Python constructions, numerical theorem certificates, and Google Colab notebooks needed to rerun the finite calculations.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run_python_suite.py
```

The quick suite reruns the parent projection, central vacuum selector, many-body Hnet finite diagnostics, SU(2) quantum-link plaquette, Maxwell bridge, one-loop RG refinement, and regulator-scaled gap criterion.

Run every Python derivation with:

```bash
python run_python_suite.py --full
```

## Google Colab

Run the public calculations directly in Google Colab:

[![Open master notebook in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/UCD_All_Toy_Simulations_Colab.ipynb)

Focused notebooks:

- [Parent Projection + Vacuum Selector](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/01_Parent_Projection_and_Vacuum_Selector.ipynb)
- [Many-Body Hnet](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/02_ManyBody_Hnet.ipynb)
- [SU(2) Quantum-Link Plaquette](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/03_SU2_Quantum_Link_Plaquette.ipynb)
- [Maxwell + RG + Gap](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/04_Maxwell_RG_Gap.ipynb)

The master notebook is self-contained and reproduces the core public toy calculations without requiring a local checkout.

## Repository layout

- `papers/` — 18 peer-review-style manuscript PDFs
- `source_tex/` — LaTeX source for the manuscripts
- `scripts/` — deterministic Python derivations and verification code
- `results/` — CSV/JSON theorem certificates produced by the scripts
- `notebooks/` — Colab-ready interactive reproductions
- `collected/` — collected manuscript volume
- `docs/` — theorem index and literature ledger

## Reproducibility boundary

The scripts reproduce the finite algebraic constructions and numerical diagnostics stated in the corresponding papers. Each manuscript states the mathematical hypotheses used for continuum or asymptotic theorems. Numerical toy models are labeled as such in the notebooks so that the executable layer and theorem layer remain traceable.

## Python versions

Tested with Python 3.11. The code uses NumPy, SciPy, mpmath, and Matplotlib.

## Citation

Until a journal DOI is assigned, cite the individual paper title and repository release/version. A `CITATION.cff` can be finalized with the repository owner/author metadata before publication.
