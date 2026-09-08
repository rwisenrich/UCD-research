# UCD Publications

This directory is the human-readable paper library for the public UCD monorepo. The publication layer is intentionally separate from short navigation Markdown: each paper should be available as a compiled PDF with its exact LaTeX source beside it, while the corresponding branch also carries the code, notebooks and result certificates used for reproduction.

## Publication layout

- `papers/` — compiled PDF papers and collected volumes.
- `source_tex/` — exact LaTeX used to build the PDFs.
- `PAPER_MAP.tsv` — canonical mapping from each paper to its scientific branch.

The GitHub workflow `.github/workflows/github-format-and-pdfs.yml` compiles publication source into PDFs and copies each paper into the `papers/` directory of its mapped scientific category.

## Current 18-paper research set

1. **Native Gauge-Matter Representation** → `06_matter_flavor_qcd/`
2. **Addressed Quantum-Link Refinement** → `04_gauge_yang_mills/`
3. **Gauge-Covariant Parent Completion** → `04_gauge_yang_mills/`
4. **Addressed Parent Projection** → `01_core_foundations/`
5. **Central Vacuum Selector** → `01_core_foundations/`
6. **Native Many-Body Hnet** → `02_h504_hnet/`
7. **Native Locality Refinement** → `04_gauge_yang_mills/`
8. **Relational Omega Reconstruction** → `01_core_foundations/`
9. **Native Flavor/Yukawa Algebra** → `06_matter_flavor_qcd/`
10. **Regge Volume Functional** → `05_gravity_cosmology/`
11. **Color-Singlet / Atomic Spectral Chain** → `06_matter_flavor_qcd/`
12. **Addressed Maxwell Bridge** → `04_gauge_yang_mills/`
13. **Dark-Sector Schur Kernel** → `05_gravity_cosmology/`
14. **Native One-Loop RG** → `06_matter_flavor_qcd/`
15. **Native Scalar / Family Bundle** → `06_matter_flavor_qcd/`
16. **Parent Regge Projection** → `05_gravity_cosmology/`
17. **Frozen Cosmology Holdout** → `05_gravity_cosmology/`
18. **Regulator-Scaled Mass-Gap Criterion** → `04_gauge_yang_mills/`

## Formatting rule

A paper is not replaced by a Markdown paraphrase. Markdown pages are indexes and readable GitHub-native exposition. Equations in Markdown use GitHub-supported math delimiters such as

$$
H_{504}=H_{84}\oplus H_{420}.
$$

The publication PDF remains the authoritative typeset reading copy for long derivations, proofs, tables and figures.

## Migration status

The paper library is being repopulated from the exact local release rather than from the earlier compact public placeholders. The migration ledger at `00_project_control/manifests/PUBLIC_ASSET_MIGRATION.md` controls completion: all 18 PDFs, all 18 exact sources, their branch copies, exact Python, notebooks and result certificates must be present before the publication layer is called complete.
