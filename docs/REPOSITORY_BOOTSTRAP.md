# UCD Monorepo Bootstrap Plan

`rwisenrich/UCD-research` is the single public repository for the owner-approved UCD corpus.

The repository uses numbered scientific branches with consistent internal structure and provenance. Owner-designated private or nonpublic work is excluded from this monorepo.

## Standard branch layout

```text
README.md
CANON.md
PROVENANCE.md
papers/
source_tex/
src/
notebooks/
tests/
results/
data/
figures/
protocols/
docs/
archive_manifest/
```

Not every branch needs every directory.

`src/` contains maintained source code. `tests/` contains deterministic algebraic and numerical regression tests. `results/` contains generated small certificates. `data/` contains only source data required for public reproducibility and legally redistributable. `archive_manifest/` contains checksums and pointers to immutable public historical packages.

## Promotion contract

A result moves into a branch's canonical index only when its record identifies:

- theorem/claim identifier;
- exact mathematical statement;
- source paper or derivation section;
- verifying script/test where computational;
- generated result certificate where applicable;
- source/provenance package;
- superseded statement, if any;
- version/commit hash.

## Data and binary policy

Do not commit large generated matrices when deterministic code reproduces them. Store the generator, shape/dtype metadata, SHA-256 of a reference output, and a regeneration command. Use Git LFS or GitHub release assets for irreplaceable public binaries.

## Versioning

Use semantic research releases such as `v0.1.0`, `v0.2.0`, and stable manuscript tags such as `paper-h504-ring-gap-v1`. Publications should cite a tag/commit rather than an unfrozen `main` state.

## Colab and CI

Each public computational manuscript should have a notebook that either contains the complete toy calculation or checks out a frozen repository tag and runs the exact source. Lightweight GitHub Actions run on push/pull request; heavy calculations use manually triggered workflows with artifacts.

## Migration order

Migrate in dependency order: project control and core mathematics first, then H504/Hnet, QEC, gauge/matter/gravity, materials and experimental branches, software/discovery branches, publications/reproducibility, and finally public historical archive reconciliation.

The completion gate is defined in `00_project_control/CORPUS_COVERAGE_INDEX.md` and applies only to owner-approved public material.