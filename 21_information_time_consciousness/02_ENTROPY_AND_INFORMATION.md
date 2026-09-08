# 02 — Entropy, Correlation, and Information

## Global versus subsystem entropy

For a density operator `rho`,

\[
\boxed{S(\rho)=-\operatorname{Tr}(\rho\log\rho).}
\]

Under unitary evolution

\[
\rho'=U\rho U^\dagger,
\]

the spectrum is unchanged, so

\[
\boxed{S(\rho')=S(\rho).}
\]

For a bipartite state,

\[
\rho_A=\operatorname{Tr}_B\rho_{AB},
\]

subsystem entropy may increase even while the global entropy remains fixed. UCD therefore does not identify the observed thermodynamic/information arrow with microscopic norm loss by default; correlation and record growth can produce increasing local entropy inside reversible global dynamics.

## Reconstructive information and detail memory

The exact finite architecture contains the factorization

\[
\boxed{H_{420}\cong H_{84}\otimes M_5.}
\]

The five-component detail factor stores information that cannot be retained by a direct 420-to-84 injective compression. Reversible coarse-graining therefore means preserving sufficient detail/provenance to reconstruct the prior state, not merely projecting it away.

## Information repair debt

The project distinguishes:

- information/provenance loss;
- mathematical recoverability;
- a conditional minimum cost of an explicit irreversible reset under thermodynamic assumptions;
- actual measured heat in a specified physical environment.

These are not interchangeable quantities.

## Tau defect functional

For legal finite transport one can define algebraic defects such as

\[
D_{\rm leak}=\|P_{84}TP_{420}\|_F^2,
\]

\[
D_{\rm irr}=\|T^\dagger T-P_{420}\|_F^2+\|TT^\dagger-P_{420}\|_F^2,
\]

with analogous boundary-fracture and history-erasure defects. A defect functional can then be written

\[
\boxed{C_\tau=\tau D_{\rm total}.}
\]

For the exact ideal routing algebra,

\[
D_{\rm total}=0
\]

so

\[
\boxed{C_\tau=0.}
\]

This is an algebraic zero-defect statement. It is not a claim that a physical device has zero heat production or supplies energy without a reservoir.

## Arrow-of-time status

The current mathematical arrow is associated with oriented realized history, records, correlations, and coarse-grained accessibility. A complete physical thermodynamic arrow additionally requires the realized state, environmental couplings, coarse-graining choice, and statistical conditions.