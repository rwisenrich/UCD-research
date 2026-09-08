# UCD Research

[![UCD reproducibility](https://github.com/rwisenrich/UCD-research/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/rwisenrich/UCD-research/actions/workflows/reproducibility.yml)

This is the single public monorepo for the UCD research program. It is being expanded from the executable mathematical-physics layer into the complete owner-approved public corpus: mathematics, physics, QEC, gauge theory, gravity/cosmology, matter/flavor/QCD, materials, discovery engines, software, neuroscience, archaeology, theology/source-text, experiments, publications, reproducibility and immutable historical lineages.

Owner-designated private or nonpublic research is outside this repository and outside the public zero-loss reconciliation target.

## Start with the theory

The mathematical dependency chain begins in [`01_core_foundations/theory_of_reality/`](01_core_foundations/theory_of_reality/README.md), then proceeds through [`02_h504_hnet/`](02_h504_hnet/README.md) into the gauge, gravity, matter and other downstream branches.

The public presentation uses three layers rather than forcing one format to do every job:

1. **PDF papers and full reports** are the primary human-readable research documents.
2. **GitHub Markdown** provides readable navigation, abstracts, theorem indexes and cross-links. Math uses GitHub-supported `$...$`, `$$...$$`, or fenced `math` blocks.
3. **LaTeX + Python + Colab + result certificates** provide exact source and reproducibility beside the corresponding scientific category.

See [`13_publications/`](13_publications/README.md) for the paper library and [`00_project_control/manifests/PUBLIC_ASSET_MIGRATION.md`](00_project_control/manifests/PUBLIC_ASSET_MIGRATION.md) for the no-loss asset migration ledger.

## Whole-project structure

- `00_project_control/` — canon, corpus coverage, manifests, provenance and releases
- `01_core_foundations/` — Theory of Reality, Q72/Dic6, H504 foundations and parent projection
- `02_h504_hnet/` — H504/H84/H420, Hnet, holonomy, memory and many-body dynamics
- `03_qec_control/` — subsystem QEC, syndromes, recovery, control, noise and leakage
- `04_gauge_yang_mills/` — Maxwell, quantum links, Yang-Mills, locality/refinement and mass-gap work
- `05_gravity_cosmology/` — Regge gravity, cosmology, dark kernels, black holes and astronomy
- `06_matter_flavor_qcd/` — matter representation, scalar/Yukawa, flavor, RG, QCD and spectra
- `07_origin_matter_knot7/` — Origin Matter, KNOT-7 and manufacturing/metrology
- `08_pure_math_ude/` — Addressed Mathematics, UDE and pure-math branches
- `10_biophysics_neuro/` — MTC-6/7/8 and neuro quantum-witness work
- `11_source_text_theology/` — source-text, theology and philosophy
- `12_experiments_holdouts/` — registered physical, astronomical and archaeological tests
- `13_publications/` — compiled papers, full reports and exact publication source
- `14_reproducibility/` — exact code/notebooks/results/checksums and reproduction controls
- `15_archive/` — immutable public historical lineages and superseded work
- `16_ucdos_native_os/` — UCDOS and native computing
- `17_matter_genesis_plasma_energy/` — historical Matter Genesis, plasma and energy-device research
- `18_archaeology_metrology/` — archaeology and measurement/metrology work
- `19_algorithms_of_reality/` — Algorithms of Reality / Universe Engine / discovery architecture
- `20_future_mathematics/` — Mathematical Genesis / Future Mathematics
- `21_information_time_consciousness/` — information, time, entropy, observer and consciousness branches
- `22_historical_geometry_kcm/` — historical KCM/FCC/Kagome geometry lineage

See [`PROJECT_MAP.md`](PROJECT_MAP.md) and [`00_project_control/CORPUS_COVERAGE_INDEX.md`](00_project_control/CORPUS_COVERAGE_INDEX.md).

## Zero-loss migration rule

Nothing inside the owner-approved public UCD scope is discarded because it was superseded, repaired, failed, conditional, renamed, or split from another branch. Every recovered public object gets a canonical object identity plus aliases/version/provenance links. Current canon can change; historical public source objects remain immutable.

The public monorepo is not declared corpus-complete until orphan items, unmapped public source files, unresolved duplicate identities, missing historical provenance pointers, and promoted computational claims without code/verifier pointers are all zero.

## Quick reproducibility start

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run_python_suite.py
```

Run the complete currently public derivation suite with:

```bash
python run_python_suite.py --full
```

A manually triggered full GitHub-hosted run is available under **Actions → UCD full reproducibility → Run workflow**. Generated `results/` are saved as an Actions artifact.

## Google Colab

[![Open master notebook in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/UCD_All_Toy_Simulations_Colab.ipynb)

Focused notebooks:

- [Parent Projection + Vacuum Selector](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/01_Parent_Projection_and_Vacuum_Selector.ipynb)
- [Many-Body Hnet](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/02_ManyBody_Hnet.ipynb)
- [SU(2) Quantum-Link Plaquette](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/03_SU2_Quantum_Link_Plaquette.ipynb)
- [Maxwell + RG + Gap](https://colab.research.google.com/github/rwisenrich/UCD-research/blob/main/notebooks/04_Maxwell_RG_Gap.ipynb)

The root-level compatibility launchers remain available while exact assets are copied into their scientific-category homes, so public links do not break during the migration.
