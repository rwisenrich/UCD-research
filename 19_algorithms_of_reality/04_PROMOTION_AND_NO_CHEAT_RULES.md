# 04 — Promotion and No-Cheat Rules

The discovery engine separates successful execution from successful science.

## Promotion firewall

A candidate law is not promoted merely because code compiles, a notebook runs, or a score improves. Promotion requires the exact gate appropriate to the claim.

Core rules include:

- **Compile-before-Claim:** compilation/smoke success validates the harness, not the theorem.
- **Duplicate Evidence:** byte-identical outputs count once as evidence; alias/upload history is preserved separately.
- **Guard-vs-Discovery Separation:** a valid anti-cheat or constraint guard may be retained even when autonomous law rediscovery fails.
- **Small-Seed Significance:** a positive signal with inadequate seed count or weak significance remains `WORK`.
- **Harness Smoke Gate:** one-step/one-epoch execution validates plumbing only.
- **Reduction-Survival:** if direct projection removes structure but legal effective reduction restores it, the failed diagnostic is not automatically a no-go for the underlying structure.
- **Diagnostic Migration:** once a diagnostic is saturated at machine precision, move to a genuinely discriminating observable.
- **Algebraic Completion vs Realization:** exact algebra does not by itself establish physical realization or threshold performance.
- **Random-Control Validity:** if a random or broken control matches/exceeds the candidate, audit score leakage before promotion.

## Negative-result preservation

A failed branch is stored with its tested scope. The update rule is

\[
\boxed{
\text{failure of candidate family }F
\not\Rightarrow
\text{failure of every parent structure used by }F.
}
\]

The ledger records precisely what was falsified.

## Holdout rule

When a model has tunable structure, discovery and evaluation datasets must be separated. A branch cannot promote by fitting the same observations used to define its architecture and then reporting those same observations as validation.

## Source-lock rule

A target value is not allowed to appear upstream inside a derivation that later claims to predict that target unless its role is explicitly labeled calibration/input. Parent-action coefficient derivation, for example, must use

\[
J_a={1\over504}\operatorname{Tr}(T_a^\dagger K_{\rm parent}),
\qquad
Gc=J
\]

without importing historical coefficient targets into `K_parent` by construction.