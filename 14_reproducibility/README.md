# UCD Reproducibility

This branch is the exact execution layer for the public UCD monorepo. It is not a substitute for the papers; it is the code-and-certificate companion to them.

## Required contents

- `python/` — exact maintained derivation and verification scripts.
- `notebooks/` — complete Jupyter/Colab notebooks, not reduced placeholders.
- `results/` — CSV/JSON result certificates and small deterministic outputs.
- `MANIFEST_SHA256.txt` — reference checksums for the frozen release.
- `REPRODUCIBILITY_STATUS.json` — machine-readable verifier/release status.
- environment/requirements files and deterministic run instructions.

The root `scripts/`, `notebooks/`, `results/`, `run_python_suite.py`, `requirements.txt`, and public Colab URLs remain compatibility launchers. Where a root script had previously been compacted, it must be replaced by the exact maintained original from the frozen release before that computational result is considered fully migrated.

## Scientific-category copies

Exact reproducibility assets are also copied to their scientific branches so that a reader does not have to hunt through a global scripts directory:

- Core foundations → `01_core_foundations/python/`, `notebooks/`, `results/`.
- H504/Hnet → `02_h504_hnet/python/`, `notebooks/`, `results/`.
- Gauge/Yang-Mills → `04_gauge_yang_mills/python/`, `notebooks/`, `results/`.
- Gravity/cosmology → `05_gravity_cosmology/python/`, `notebooks/`, `results/`.
- Matter/flavor/QCD → `06_matter_flavor_qcd/python/`, `notebooks/`, `results/`.

## Large artifacts

Hundreds-of-megabytes generated arrays are not treated as the source of truth when deterministic code regenerates them. Store the generator, shape/dtype metadata, reference SHA-256 and regeneration command. Use a large-asset mechanism only for irreplaceable public binary data.

## Verification gate

A computational claim is fully migrated only when its exact script, input assumptions, result certificate, paper/theorem pointer and provenance are all recoverable from the repository. The project-wide gate is tracked in `00_project_control/manifests/PUBLIC_ASSET_MIGRATION.md`.
