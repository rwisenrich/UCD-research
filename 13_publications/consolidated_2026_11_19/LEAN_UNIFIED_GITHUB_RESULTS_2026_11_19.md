# UCD Unified Lean Verification — GitHub Results (2026-11-19)

**Verification status:** source upload completed; full theorem compilation is **not all passing**. This document records observed GitHub Actions results and preserves the original theorem source files unchanged.

## Provenance and source scope
- Live run: https://github.com/rwisenrich/UCD-research/actions/runs/44647433354
- Review branch: `audit/ucd-adversarial-regression-2026-11-19` (main is unchanged).
- Original Google Drive theorem-source files (34 paths): `verification/unified_lean/google_drive/`.
- Historical proof-source files (74 paths): archived, SHA-256-pinned ZIP under `verification/adversarial/input/`.
- Established Mathlib v21 module library: `verification/ucd_v21/lean4/`.
- Original files and multiple historical versions are kept separately; 17 names appear in both the Drive and archival cohorts, but only one pair matches byte-for-byte after transport normalization.

## Compiler results: Lean 4.14.0

| Source cohort | Total theorem-source paths | PASS | FAIL |
| --- | ---: | ---: | ---: |
| Original historical ZIP (excluding Lake config) | 74 | 48 | 26 |
| Original Drive raw exports | 34 | 0 | 34 |
| Drive transport-normalized compiler copies | 34 | 13 | 21 |

The 34 Drive-source originals have **not** been rewritten. The compiler copies remove 31 leading UTF-8 BOMs, one Google Docs filename display heading, and a matching pair of Google Docs code block presentation markers. A JSON manifest records each original and normalized SHA-256 digest.

The archived cohort includes historical duplicate source paths. PASS counts concern individual source paths, **not** unique new theorems, complete manuscript claims, or predictions about the physical universe.

## Reproducible evidence

The GitHub Actions run uploaded two downloadable artifact archives:
- `ucd-drive-34-lean-compiler`: all original and normalized source logs, CSV/JSON summaries, source digests, normalization manifest.
- `ucd-archive-74-lean-compiler`: individual source logs, CSV/JSON summary, source digests.

The compiler command is `python3 verification/unified_lean/run_lean_audit.py`; the reproducible transport-only source copy builder is `verification/unified_lean/normalize_transport.py`. Both are committed and reviewable.

## Verified failure classes requiring distinct treatment

1. **Typing/natural subtraction:** `UCDCompleteTheoryOfEverything.lean` attempts integer-like expressions under `Nat` subtraction, where e.g. `24 - 36 + 14 = 2` is false in Lean's natural arithmetic. A correctly typed reformulation must be a separately audited theorem, not a silent source edit.
2. **Actual false assertion:** `UCDCommunicationAtlasAuditAndChallengeTheorems.lean` contains a 12-sector routing assertion evaluated false by `decide`. Historical Dic6 Bob-routing changes must be crosschecked by exact definitions.
3. **Undischarged goals/tactic errors:** multiple other Lean sources report unsolved `omega` goals, unknown `List.finRange`, recursion-depth errors, or missing imports, none of which are verified by the present run.
4. **Yang–Mills scope:** selected finite-source theorems compile, but `UCDYangMillsExistenceAndMassGap_v5_Master.lean` fails, and file compilation alone does not certify a full continuum mass-gap theorem.

## v21 Mathlib scope

In the same run, the v21 Mathlib `lake build` completed successfully (GitHub reported **8,659 jobs**). The independent `leanchecker` step then received a runner shutdown signal and was canceled. A targeted retry was requested. Until a successful checker result is observed, the fresh independent-checker result remains **interrupted**, not PASS.

## Publication and proof-status rule

Each broad physical theorem claim must be matched to its exact Lean statement and hypotheses. Compiler success, lexical absence of `sorry`, and numerical simulations are separate evidence categories. Any mathematical correction must preserve the original failed claim, an explicit refutation where appropriate, and a separately named corrected statement. Do not merge this review branch until the full claimed proof scope is examined.

## Complete downloadable Lean source bundle

The [GitHub source-bundle workflow](https://github.com/rwisenrich/UCD-research/actions/runs/44648247792) succeeded, bundling 74 archived, 34 original Google Drive, and 4 v21 Lean source paths plus 34 separate transport-normalized copies, manifest and toolchain configurations. The verified bundle SHA-256 is `570e7f9dbc24d7ccd6da042090438d7dd6375aab7946d8c4f893237ac37f7c6e`. No originals were rewritten.
