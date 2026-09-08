# Public UCD Asset Migration Ledger

This is the active no-loss migration ledger for the public monorepo. A branch is not considered populated merely because a README exists. Each scientific category must receive its human-readable papers/reports, exact source, executable Python, notebooks, result certificates, and provenance.

## Presentation rule

For each major research result, publish all applicable layers together:

1. `papers/` — compiled PDF intended for human reading.
2. `source_tex/` — exact LaTeX source used to build the PDF.
3. `python/` — maintained/exact derivation and verification scripts.
4. `notebooks/` — runnable Colab/Jupyter entry points.
5. `results/` — generated CSV/JSON certificates and small reference outputs.
6. `workbenches/` — recovered full workbench source packages or curated public equivalents.
7. `provenance/` or branch documentation — source package, version, checksum, supersession status.

Markdown is navigation and GitHub-native exposition. Display mathematics in Markdown must use GitHub-supported `$...$`, `$$...$$`, or fenced `math` blocks. Do not use raw `\[` / `\]` delimiters in public Markdown.

## Current 18-paper publication set

| # | Paper | Branch |
|---:|---|---|
| 01 | Native gauge-matter representation | `06_matter_flavor_qcd/` |
| 02 | Addressed quantum-link refinement | `04_gauge_yang_mills/` |
| 03 | Gauge-covariant parent completion | `04_gauge_yang_mills/` |
| 04 | Addressed parent projection | `01_core_foundations/` |
| 05 | Central vacuum selector | `01_core_foundations/` |
| 06 | Native many-body Hnet | `02_h504_hnet/` |
| 07 | Native locality refinement | `04_gauge_yang_mills/` |
| 08 | Relational Omega reconstruction | `01_core_foundations/` |
| 09 | Native flavor/Yukawa algebra | `06_matter_flavor_qcd/` |
| 10 | Regge volume functional | `05_gravity_cosmology/` |
| 11 | Color-singlet/atomic spectral chain | `06_matter_flavor_qcd/` |
| 12 | Addressed Maxwell bridge | `04_gauge_yang_mills/` |
| 13 | Dark-sector Schur kernel | `05_gravity_cosmology/` |
| 14 | Native one-loop RG | `06_matter_flavor_qcd/` |
| 15 | Native scalar/family bundle | `06_matter_flavor_qcd/` |
| 16 | Parent Regge projection | `05_gravity_cosmology/` |
| 17 | Frozen cosmology holdout | `05_gravity_cosmology/` |
| 18 | Regulator-scaled mass-gap criterion | `04_gauge_yang_mills/` |

The canonical paper-to-branch mapping consumed by the PDF workflow is `13_publications/PAPER_MAP.tsv`.

## Exact Python placement

- `01_core_foundations/python/`: `derive_parent_projection.py`, `derive_vacuum_selector.py`, `derive_omega_reconstruction.py`.
- `02_h504_hnet/python/`: `ucd_504_master_hamiltonian.py`, `derive_manybody_hnet.py`.
- `04_gauge_yang_mills/python/`: `build_su2_qlm_plaquette.py`, `derive_maxwell_bridge.py`, `derive_locality_refinement.py`, `derive_gap_criterion.py`, `derive_gauge_covariant_parent.py`.
- `05_gravity_cosmology/python/`: `derive_gravity_projection.py`, `derive_regge_volume_functional.py`, `derive_dark_kernel_theorem.py`, `derive_frozen_cosmology_test.py`.
- `06_matter_flavor_qcd/python/`: `derive_native_sm_representation.py`, `verify_native_sm_representation.py`, `derive_native_flavor_completion.py`, `derive_rg_flow.py`, `derive_scalar_bundle.py`, `derive_color_atomic_spectral_chain.py`.
- `14_reproducibility/python/`: `verify_submission_build.py`.

The existing root `scripts/` remains a compatibility execution surface, but it must contain the exact maintained originals, not compact substitutes.

## Notebook placement

The public root notebook paths remain stable for Colab compatibility. Exact notebook copies are also filed by branch:

- Core: `01_Parent_Projection_and_Vacuum_Selector.ipynb`.
- H504/Hnet: `02_ManyBody_Hnet.ipynb`.
- Gauge/Yang-Mills: `03_SU2_Quantum_Link_Plaquette.ipynb`, `04_Maxwell_RG_Gap.ipynb`.
- Reproducibility: `UCD_All_Toy_Simulations_Colab.ipynb`.

## Deep workbench migration after the publication layer

The publication/reproducibility set is only the first migration layer. The following public UCD families are then reconciled into their scientific branches rather than left as opaque archive names:

- H504 master-Hamiltonian, ring-gap, missing-operator, subsystem-factorization and Hnet connection workbenches.
- QEC: subsystem gauge code, Knill-Laflamme/OAQEC, Dic6 syndrome, noisy dynamics, echo/dynamical decoupling, driven dynamics, readout/control and leakage stress.
- Gauge/closure: addressed parent QLM, boundary-action, spectral closure, weak-basis RG and completion-gate packages.
- Gravity/cosmology: Regge, dark-kernel, cosmology and black-hole/bridge material approved for public release.
- Matter/flavor: Yukawa/vacuum, found-formula audit, weak-basis transport, fermionic gap and color/atomic work.
- Origin Matter/KNOT-7, pure mathematics/UDE, biophysics/neuro, source-text/theology, experiments, UCDOS, Algorithms of Reality, Future Mathematics and historical KCM geometry.

Large reproducible generated arrays are represented by generators, shape/dtype metadata and reference SHA-256 rather than being committed as opaque hundreds-of-megabytes matrices. Irreplaceable large public binaries use an appropriate large-asset route.

## Completion gates

The migration is not complete until all owner-approved public assets satisfy:

- `unmapped_public_source_files = 0`
- `published_papers_missing_pdf = 0`
- `published_papers_missing_source = 0`
- `computational_results_missing_exact_script = 0`
- `computational_results_missing_result_certificate = 0`
- `category_assets_only_present_at_root = 0` except intentional compatibility launchers
- `raw_latex_delimiters_in_public_markdown = 0`
- `owner_excluded_private_material_in_public_repo = 0`
