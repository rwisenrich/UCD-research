# UCD external verification - November 19, 2026

Original submitted ZIP is preserved unchanged at `verification/adversarial/input/UCD_External_Testing_and_Lean4_CI_Kit.zip`.

The repaired kit is at `verification/adversarial/input/UCD_External_Testing_and_Lean4_CI_Kit_CORRECTED.zip`.
It includes portable regression scripts, an independent reference Wilson/overlap test,
a paired protein-decoy experiment requiring the missing folding engine, full static
Lean source inventory, and a strict Lean 4 compiler runner.

## Reproducible findings
- Original stress-test script fails with `ModuleNotFoundError: ucd_fold_v3_complete`.
- 76 `.lean` paths = 74 theorem-source files + 2 Lake configuration files; 8 of the
  74 source paths are byte-for-byte aliases. There are 66 distinct theorem-source bodies,
  579 theorem declarations across paths and 519 declarations across distinct bodies.
- Two existing Lean source files contained accidental nested-comment tokens `+/-`;
  the corrected kit changes only their comment strings to `plus-or-minus`.
- Original look-elsewhere null (tolerances 0.005, 0.005, 0.001): 337 / 501 = 67.27%.
  Uniform absolute 0.001 null and exact rational targets: 225 / 501 = 44.91%.
- Kelvin scalar Laplacian directional anisotropy is minimized at
  `w_hex = 2*w_square`. This is NOT a replacement for geometric cubature weights.
- Eight decoys do not establish a statistically significant native protein selector.
- The reference overlap calculation has a small Ginsparg-Wilson residual.
  This does NOT prove the production UCD overlap operator over the full BZ.

## Independent compiler
The workflow `.github/workflows/ucd-external-lean-ci.yml` extracts the
SHA-256-pinned corrected ZIP and runs the Lean 4.14.0 compiler on all 74 proof-source
paths, saving per-file logs. A static 'zero sorry' scan never substitutes for this.

This branch is for review; main is not modified. No broad theorem claims are
silently changed to match narrower Lean statements.

## Second repair after initial external compiler run

Actual GitHub Lean 4.14.0 compilation discovered an invalid `rec` field name in AddressedCalculusCore (it collides with the generated recursor) and a missing pair of commutativity hypotheses for its abstract discrete Leibniz theorem. The corrected ZIP renames that field to `record`, makes additive/multiplicative commutativity explicit fields of `DiffRing`, and repairs the proof using those hypotheses. An older v18 companion's unbound `State` type binders were also corrected. These amendments are documented in the ZIP README; no claimed noncommutative Leibniz theorem is certified. The compiler now attempts every proof source and saves individual logs even after a prerequisite failure.

## Third conservative repair pass (external Lean 4.14.0)
The second external run compiled **41/74** proof-source paths and reported 33 failures. Seven exact source files now receive narrowly scoped fixes:
- Natural-number subtraction expressions with negative intermediate quantities are correctly typed as `Int` for the graph-cycle, black-hole polynomial, and BCC scattering sign identities.
- Two elementary multiplication/parity theorems now use core Lean tactics compatible with Lean 4.14.0; the roadmap product identity uses explicit associativity.
- An unrelated inconsistent beta arithmetic claim `22*2 - 4*3 - 1 = 19` is **not** silently modified; its actual value is 31, and its physical coefficient needs independent reconciliation.
- Other existing theorem errors are still CI-failing, with diagnostics retained. Nothing is merged into main.
