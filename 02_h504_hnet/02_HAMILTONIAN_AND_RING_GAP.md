# 02 — Hamiltonian, Parent Projection, and Ring Gap

## Seven-operator basis

The historical finite Hamiltonian is

\[
\boxed{
H_{\rm hist}=e^{-\tau}
(T_1+\eta T_2+\kappa T_3+\gamma T_4+\mu T_5+\nu T_6+\delta T_7),
\qquad \tau={1\over72}.
}
\]

The historical coefficient vector is retained as provenance,

\[
(1,1/2,1/10,1/10,11/10,1/10,3/10),
\]

but it is not labeled a first-principles primitive-count derivation.

## Exact operator metric

For the basis `T_a`,

\[
\boxed{
G_{ab}={1\over504}\operatorname{Tr}(T_a^\dagger T_b)
=\operatorname{diag}\!\left({12\over7},2,{12\over7},{12\over7},1,{1\over3},{4\over7}\right).
}
\]

Given a parent/source operator `K_parent`, define

\[
J_a={1\over504}\operatorname{Tr}(T_a^\dagger K_{\rm parent}).
\]

Then the least-squares/source projection coefficients satisfy

\[
\boxed{Gc=J.}
\]

This is the active coefficient-derivation interface: derive `K_parent` from allowed primitive invariants, then project it onto the seven-operator span without seeding the historical target coefficients upstream.

## Ring-gap theorem

The ring adjacency term produces

\[
\boxed{\Delta_{\rm ring}=2\kappa e^{-\tau}.}
\]

At `kappa=1/10`,

\[
\Delta_{\rm ring}={1\over5}e^{-1/72}.
\]

The derivative is

\[
\boxed{{\partial\Delta_{\rm ring}\over\partial\kappa}=2e^{-\tau}.}
\]

## Schur inheritance

Direct projection may remove an operator that still affects the retained sector through virtual/effective coupling. For block form

\[
H=\begin{pmatrix}H_{cc}&H_{c\ell}\\H_{\ell c}&H_{\ell\ell}\end{pmatrix},
\]

the effective operator is

\[
\boxed{
H_{\rm eff}(E)=H_{cc}-H_{c\ell}(H_{\ell\ell}-EI)^{-1}H_{\ell c}.
}
\]

The project therefore treats disappearance under direct projection as a diagnostic failure unless the legal effective reduction also removes the structure.