# Reproducibility map

The Python layer is organized so that every finite computation can be rerun independently. The manuscript proofs and asymptotic arguments remain in `papers/` and `source_tex/`; the executable layer reproduces the finite matrix constructions, spectra, coefficient tables, and theorem certificates.

| Paper | Main Python module | Primary result files | Colab |
|---|---|---|---|
| 01 Native gauge/matter representation | `scripts/derive_native_sm_representation.py` | `results/02_native_species_table.csv`, `results/04_native_gauge_matter_theorem.json` | master |
| 02 Addressed quantum-link refinement | `scripts/build_su2_qlm_plaquette.py` | `results/K_su2_qlm_one_plaquette*.json/csv` | `03_SU2_Quantum_Link_Plaquette.ipynb` |
| 03 Gauge-covariant parent completion | `scripts/derive_gauge_covariant_parent.py` | `results/10_gauge_covariant_parent_completion.json` | master |
| 04 Parent projection | `scripts/derive_parent_projection.py` | `results/11_parent_gram_matrix.csv`, `results/12_parent_projection_theorem.json` | `01_Parent_Projection_and_Vacuum_Selector.ipynb` |
| 05 Central vacuum selector | `scripts/derive_vacuum_selector.py` | `results/13_*`, `14_*`, `15_*` | `01_Parent_Projection_and_Vacuum_Selector.ipynb` |
| 06 Native many-body Hnet | `scripts/derive_manybody_hnet.py` | `results/16_*`, `17_*`, `18_*` | `02_ManyBody_Hnet.ipynb` |
| 07 Native locality refinement | `scripts/derive_locality_refinement.py` | `results/19_*`, `20_*`, `21_*`, `22_*` | master |
| 08 Relational Omega reconstruction | `scripts/derive_omega_reconstruction.py` | `results/23_*`, `24_*` | master |
| 09 Flavor/Yukawa algebra | `scripts/derive_native_flavor_completion.py` | `results/25_*`, `26_*` | master |
| 10 Regge volume functional | `scripts/derive_regge_volume_functional.py` | `results/27_*`, `28_*` | master |
| 11 Color/atomic spectral chain | `scripts/derive_color_atomic_spectral_chain.py` | `results/29_*`, `30_*`, `31_*` | master |
| 12 Maxwell bridge | `scripts/derive_maxwell_bridge.py` | `results/32_*`, `33_*` | `04_Maxwell_RG_Gap.ipynb` |
| 13 Dark-sector Schur kernel | `scripts/derive_dark_kernel_theorem.py` | `results/34_*`, `35_*` | master |
| 14 One-loop RG | `scripts/derive_rg_flow.py` | `results/36_*`, `37_*` | `04_Maxwell_RG_Gap.ipynb` |
| 15 Scalar/family bundle | `scripts/derive_scalar_bundle.py` | `results/38_*`, `39_*` | master |
| 16 Parent Regge projection | `scripts/derive_gravity_projection.py` | `results/40_gravity_projection_theorem.json` | master |
| 17 Frozen cosmology holdout | `scripts/derive_frozen_cosmology_test.py` | `results/41_frozen_cosmology_theorem.json` | master |
| 18 Regulator-scaled gap criterion | `scripts/derive_gap_criterion.py` | `results/42_*`, `43_*` | `04_Maxwell_RG_Gap.ipynb` |

## Two execution modes

`python run_python_suite.py` runs the seven-module public toy/reproduction suite and is intended for laptops, Colab, and GitHub Actions.

`python run_python_suite.py --full` runs every derivation module. It is substantially heavier because several scripts construct and manipulate dense 504-dimensional and many-body operators.

## Determinism

The public scripts do not require network access or experimental-data downloads for their finite algebraic tests. The core numerical examples are deterministic; result files can therefore be compared byte-for-byte or numerically across environments, subject to ordinary floating-point formatting differences.
