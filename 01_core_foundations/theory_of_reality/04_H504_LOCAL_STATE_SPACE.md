# 04 — H504 Local State Space and Exact Finite Operator Structure

Once a one-center-plus-six-boundary local cell `V7` is licensed, the local finite state space is

\[
\boxed{
H_{504}=V_7\otimes\mathbb C[Z_3]\otimes\mathbb C[{\rm Dic}_6]
=V_7\otimes\mathbb C[Q_{72}]
}
\]

with

\[
\boxed{\dim H_{504}=7\times3\times24=504.}
\]

## 84 + 420 quotient/detail split

Using the exact `12 x 6` quotient/detail factorization and

\[
\mathbb C^6=\mathbb C u_0\oplus M_5,
\]

we obtain

\[
\boxed{
H_{84}=V_7\otimes\mathbb C^{12}\otimes\mathbb C u_0,
\qquad
\dim H_{84}=84,
}
\]

\[
\boxed{
H_{420}=V_7\otimes\mathbb C^{12}\otimes M_5,
\qquad
\dim H_{420}=420,
}
\]

and therefore

\[
\boxed{H_{504}=H_{84}\oplus H_{420}},
\qquad
\boxed{504=84+420=84(1+5)}.
\]

For the derived subgroup `D=<a^2>` of order six,

\[
Q=\sum_{h\in D}L_h=6P_{84},
\qquad
J=6I-Q=6P_{420},
\]

with

\[
Q^2=6Q,
\qquad
J^2=6J,
\qquad
QJ=0.
\]

## Seven-term finite Hamiltonian basis

The historical local Hamiltonian is represented on seven fixed operators as

\[
\boxed{
H_{\rm hist}=e^{-\tau}
(T_1+\eta T_2+\kappa T_3+\gamma T_4+\mu T_5+\nu T_6+\delta T_7).
}
\]

The exact Hilbert-Schmidt Gram matrix for this operator basis is

\[
\boxed{
G_{ab}={1\over504}\operatorname{Tr}(T_a^\dagger T_b)
=\operatorname{diag}\!\left({12\over7},2,{12\over7},{12\over7},1,{1\over3},{4\over7}\right).
}
\]

For a parent/source operator `K`, the coefficient projection is

\[
J_a={1\over504}\operatorname{Tr}(T_a^\dagger K),
\qquad
\boxed{Gc=J}.
\]

This is the current source-projection law. Historical coefficient values are not reinterpreted as being derived by a primitive-counting argument unless an independent parent action supplies that derivation.

## Ring-gap theorem

The six-ring adjacency contributes the exact local gap

\[
\boxed{\Delta_{\rm ring}=2\kappa e^{-\tau}.}
\]

For the frozen historical `kappa=1/10` and `tau=1/72`,

\[
\Delta_{\rm ring}={1\over5}e^{-1/72}.
\]

Direct center projection removes explicit ring adjacency, while Schur/Feshbach elimination retains its effect:

\[
\boxed{
H_{\rm eff}(E)
=H_{cc}-H_{c\ell}(H_{\ell\ell}-E)^{-1}H_{\ell c}.
}
\]

## Central selector and family orientation

The nontrivial central selector on the relevant restricted algebra has eigenvalues `+1` and `-1`. A selector defect

\[
S_{\rm sel}={\tau\over2}\langle\psi,(S_x-\sigma I)^2\psi\rangle
\]

gives, up to an additive constant,

\[
\boxed{H_{\rm sel}=-\tau\sigma S_x}
\]

with splitting `2 tau = 1/36`.

For the Z3 family orientation,

\[
X_Z=R+R^\dagger,
\qquad
J_Z={R-R^\dagger\over i\sqrt3},
\]

and reversal acts by

\[
CX_ZC=X_Z,
\qquad
CJ_ZC=-J_Z.
\]

Thus the degree-one orientation-odd family direction is proportional to `sigma J_Z`.