# UCD Research

[![UCD reproducibility](https://github.com/rwisenrich/UCD-research/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/rwisenrich/UCD-research/actions/workflows/reproducibility.yml)

This is the single public monorepo for the UCD research program. It is being expanded from the already-public executable mathematical-physics layer into the complete owner-approved public corpus: mathematics, physics, QEC, gauge theory, gravity/cosmology, matter/flavor/QCD, materials, discovery engines, software, neuroscience, archaeology, theology/source-text, experiments, publications, reproducibility and immutable historical lineages.

Owner-designated private or nonpublic research is outside this repository and outside the public zero-loss reconciliation target.

## Start with the UCD Theory of Reality

The foundational theory is now being populated first rather than leaving the numbered branches as placeholders.

1. [`01_core_foundations/theory_of_reality/`](01_core_foundations/theory_of_reality/) — relational floor, realized state, finite registration, H504, dynamics/history, measurement/time/continuum, theorem frontier, and dependency chain.
2. [`01_core_foundations/CANON.md`](01_core_foundations/CANON.md) — compact current core equation ledger.
3. [`02_h504_hnet/`](02_h504_hnet/) — H504/H84/H420, projector and H14/D84 status, Hamiltonian/ring gap, Hnet transport, holonomy, memory, causal many-body program.
4. [`19_algorithms_of_reality/`](19_algorithms_of_reality/) — discovery loop, Operator Cartography, shared law ledger, no-cheat promotion rules, and forensic recovery.
5. [`21_information_time_consciousness/`](21_information_time_consciousness/) — time/causality, entropy/information, identity/memory/observer models, biological organization, and consciousness status boundary.

The public foundation keeps exact theorems, conditional reductions, physical-promotion premises, realized-state data, failed branches, and historical formulations distinct so later applications cannot silently import a superseded or unproved premise.

## Whole-project structure

- `00_project_control/` — canon, forensic baseline, corpus coverage, manifests, provenance and releases
- `01_core_foundations/`
- `02_h504_hnet/`
- `03_qec_control/`
- `04_gauge_yang_mills/`
- `05_gravity_cosmology/`
- `06_matter_flavor_qcd/`
- `07_origin_matter_knot7/`
- `08_pure_math_ude/`
- `10_biophysics_neuro/`
- `11_source_text_theology/`
- `12_experiments_holdouts/`
- `13_publications/`
- `14_reproducibility/`
- `15_archive/`
- `16_ucdos_native_os/`
- `17_matter_genesis_plasma_energy/`
- `18_archaeology_metrology/`
- `19_algorithms_of_reality/`
- `20_future_mathematics/`
- `21_information_time_consciousness/`
- `22_historical_geometry_kcm/`

See [`PROJECT_MAP.md`](PROJECT_MAP.md), [`00_project_control/CORPUS_COVERAGE_INDEX.md`](00_project_control/CORPUS_COVERAGE_INDEX.md), and [`00_project_control/FORENSIC_BASELINE.md`](00_project_control/FORENSIC_BASELINE.md).

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

The existing root-level `scripts/`, `notebooks/`, `results/`, and workflows remain live while source material is migrated into canonical branch locations, so public Colab and CI links continue working throughout the zero-loss reconciliation.