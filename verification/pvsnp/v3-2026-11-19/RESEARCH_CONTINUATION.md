# UCD P-versus-NP, 3-SAT v3: review checkpoint 2026-11-19

This is a source-preservation and research audit checkpoint, not a claim that P=NP is solved. Existing proof files and main branch remain unchanged.

## New Google Drive input
UCD Lean 4 Audit & 3-SAT Benchmark Report (2026-11-19):
https://docs.google.com/document/d/1mcJlHvKHUOUvJlkmixl6eEevLWXk058pFSwh_4mI2D0/edit

Two reported benchmarks: A (48 selected SAT formulas, n=30..100), and B/v3 (40 selected SAT formulas, n=75,100,150,200, alpha approximately 4.267). No original hard_unplanted_3sat_v3_benchmark.py, 40 DIMACS CNFs or per-instance seeds were found in accessible connected Drive/GitHub searches. Consequently B is a **reported table, not an independently rerun solver benchmark**.

## Benchmark B
- WalkSAT: 39/40; pure adaptive flow: 15/40; flow-to-WalkSAT: 39/40.
- Hybrid median flip changes vs WalkSAT by n=75,100,150,200: -79.8%, +82.6%, -40.2%, -8.3%.
- Hybrid median wall time changes at the same n: +116.9%, -13.4%, +19.8%, +46.2%.
- Handoff satisfaction per n based on mean residual violated clauses: 99.750%, 99.672%, 99.563%, 99.672%. "More than 99.6%" is not true at n=150.
- Selected satisfiable instances, small cohorts and unpaired medians cannot establish polynomial worst-case 3-SAT complexity or a general speed advantage.

## Independent continuation: exact residual repair
New Python pilot delivered as a downloadable ZIP in the user's conversation: UCD_PvsNP_V3_FULL_RESEARCH_AND_VERIFICATION_2026-11-19.zip (SHA-256 manifest). Contains original Drive report, preserved research PDFs, executable code, all 18 fresh uniform unplanted 3-CNF instances and verified SAT witnesses, per-instance CSV, raw states, and output logs.

Three SAT-filtered instances at each n=75,100,150,200,300,400 (18 total); a separate WalkSAT trajectory was stopped on first reaching <=3 violated clauses. At most 9 variables occur in those clauses. Exact enumeration of all assignments to these variables with the exterior fixed repaired 0/18 states. Continuing WalkSAT 2,500 additional flips from the same handoff repaired 8/18; exact repair+fallback also 8/18. A SciPy/HiGHS integer-feasibility formulation allowing 12,20,32,48 selected free variables returned infeasible status for all 18 at each cap. Full-free-variable sanity tests found valid solutions on selected cases. These are finite solver outputs, not general lower bound proofs or independently checked UNSAT certificates.

Proof scope: the restricted local search uses at most 2^(3k) trials for k violated 3-clauses. That is fixed-parameter finite search, not polynomial time for arbitrary 3-SAT unless additional universal hypotheses are proved.

## Existing exact mathematics
Earlier independent checks retained: Round7 simplex determinant magnitude 1; Round6 local Boolean bivector clause 8/8; Round7 parity 8/8; Round4 Lucas finite identity 16/16. Known scope errors remain flagged: Round6 abstract polarity mismatch; an algebraic tunnel dimension bound contradicted by one-clause example; a Newton-rate counterexample; the v35 stated Dic6/D ~ S3 isomorphism contradicts group orders 4 versus 6.

## Next reproducible steps
Recover original v3 benchmark code, CNFs and seeds; paired identical-instance tests against modern CDCL, WalkSAT, original flow, stall-aware restart and original hybrid, under equal end-to-end time. Store per-instance SAT witness verification, censored time, final residual histogram, amplitude history, hardware and seeds. Keep all source claims and counterexamples; do not replace broad theorem statements with narrower compiled checks.
