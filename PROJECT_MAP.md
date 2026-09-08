# UCD Full Project Map

`UCD-research` is the single public monorepo for the owner-approved UCD research program. All public research branches, mathematics, papers, source code, notebooks, workbenches, result certificates, experiments, software, engineering programs, and historical archives live under this repository in controlled subfolders.

Owner-designated private or nonpublic research is intentionally excluded from this repository and is not counted as an omission in the public corpus reconciliation.

## Monorepo branches

- `00_project_control/` — canon, corpus coverage, manifests, provenance, aliases, release indexes, migration controls.
- `01_core_foundations/` — Q72/Dic6/Z3, H504 foundations, addressed mathematics, ring gap, parent action, exact decompositions, refinement.
- `02_h504_hnet/` — H504/H84/H420/H14/H406/D84, Hnet, holonomy, memory dilation, locality, many-body dynamics.
- `03_qec_control/` — subsystem QEC, KL/OAQEC, syndromes, recovery, logical gates, noise, decoupling, driven dynamics, readout, leakage.
- `04_gauge_yang_mills/` — Maxwell, quantum links, gauge-covariant parent, native refinement, Yang-Mills, finite-volume spectra, clustering, gap program.
- `05_gravity_cosmology/` — Regge gravity, nonlinear coefficients, dark kernels, cosmology, black holes, bridges, astronomy.
- `06_matter_flavor_qcd/` — gauge matter, charge, scalar/Yukawa, flavor, RG, fermions, QCD, hadrons, nuclei, atoms, chemistry.
- `07_origin_matter_knot7/` — carbyne/CNT/KNOT-7/Origin Stone, manufacturing inverse problem, metrology, digital twin.
- `08_pure_math_ude/` — Addressed Mathematics, Multi-Lens, Operator Cartography, Pascal/Singmaster, elliptic curves, UDE.
- `10_biophysics_neuro/` — MTC-6/7/8, molecular quantum witnesses, neuron compiler, matched controls.
- `11_source_text_theology/` — source-text, theology, philosophy, Genesis/Logos/restoration studies.
- `12_experiments_holdouts/` — registered physical tests, astronomical holdouts, hardware tests, discriminators and controls.
- `13_publications/` — manuscripts, collected volumes, LaTeX, theorem indexes, citation metadata, release tags.
- `14_reproducibility/` — cross-project runners, Colabs, CI, certificates, environments, checksums, regenerators.
- `15_archive/` — immutable historical public UCD documents, superseded models, workbenches, chats, binary artifacts and checksum ledgers.
- `16_ucdos_native_os/` — Whole-UCD Native OS, discrete kernel, self-verifying memory, routing, recursive intelligence, UCDFS, hardware/runtime chain.
- `17_matter_genesis_plasma_energy/` — Matter Genesis, Plasma Universe/Matter Phase programs, plasma hardware, historical energy and transport-device research.
- `18_archaeology_metrology/` — Taş Tepeler, regional geometry, metrological uncertainty, exact-discriminator archaeology, negative controls.
- `19_algorithms_of_reality/` — Algorithms of Reality, Universe Engine, GrowWorld, DeepMap, Atlas Recursive Master, Recursive Law Builder.
- `20_future_mathematics/` — Mathematical Genesis / Future Mathematics / MGL, typed kernels, scale/emergence/memory mathematics.
- `21_information_time_consciousness/` — measurement, entropy, proper time, information identity, observer/self-model, UCD-IIT/Phi lineage.
- `22_historical_geometry_kcm/` — KCM/FCC/Kagome/stacked-Kagome/pyrochlore and other historical geometry/cosmology lineages.

## Internal structure

Each branch may contain `papers/`, `source/`, `python/`, `colab/`, `results/`, `workbenches/`, `references/`, and `archive/`. Not every branch requires every subfolder.

## No-loss rule

Nothing inside the public UCD scope is discarded because it was superseded, repaired, failed, conditional, renamed, or separated from another project. It receives a provenance state and an immutable pointer. True byte-duplicates may share one stored object, but every public historical filename, alias and version remains represented.

## Promoted-result control rule

Every promoted computational result should resolve to: (1) a theorem/paper/registered statement, (2) exact source code or proof object, (3) machine-readable certificate where applicable, and (4) provenance/version/checksum metadata.

## Corpus completion condition

The public monorepo is not declared complete until every owner-approved public UCD item has exactly one canonical object identity plus aliases/version links and the counters satisfy:

- `orphan_items = 0`
- `unmapped_public_source_files = 0`
- `unresolved_duplicate_identities = 0`
- `historical_names_without_provenance_pointer = 0`
- `computational_claims_without_code_or_verifier_pointer = 0`

The current root-level `scripts/`, `notebooks/`, `results/`, and Actions remain live during migration so public Colab and CI links do not break.