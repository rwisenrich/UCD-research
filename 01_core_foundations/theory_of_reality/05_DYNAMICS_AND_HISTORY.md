# 05 — Dynamics, Hnet, Holonomy, and Reversible History

UCD separates local state algebra from network adjacency and from realized link history.

## Canonical internal transport

A legal internal edge label has

\[
m_{ij}\in Z_3,
\qquad
g_{ij}\in {\rm Dic}_6,
\]

with link operator

\[
\boxed{W_{ij}=S_{Z_3}^{m_{ij}}\otimes L(g_{ij}).}
\]

The reverse edge is

\[
\boxed{W_{ji}=W_{ij}^{-1}=W_{ij}^\dagger.}
\]

With a right-gauge shift `q`, define

\[
U(m,g,q)=R(q)[S_3^m\otimes L(g)],
\qquad
T=UP_{420}.
\]

The exact routed-sector identities are

\[
\boxed{T^\dagger T=P_{420}},
\qquad
\boxed{TT^\dagger=P_{420}},
\qquad
\boxed{P_{84}TP_{420}=0}.
\]

Thus the legal transport is a partial isometry on the 420-dimensional detail sector.

## Hnet graph construction versus physical promotion

Relative to the typed primitive Q72 operations `z,a,x` and inverses,

\[
S=\{z,z^{-1},a,a^{-1},x,x^{-1}\},
\]

the canonical left-translation-invariant graph is

\[
\boxed{\operatorname{Cay}(Q_{72},S).}
\]

For this named generator set the graph has 72 vertices, degree 6, 216 undirected edges, and diameter 5.

This exact graph construction is distinct from the physical locality premise `NET-PRIM`: the mathematical registration data alone do not prove that exactly these primitive operations, and only these operations, are one-step physical links.

## Holonomy

For a path

\[
\gamma=(e_1,\ldots,e_N),
\]

define

\[
\boxed{U_\gamma=T_{e_N}\cdots T_{e_1}.}
\]

A nontrivial loop may satisfy

\[
U_\gamma\neq P_{420}
\]

while preserving

\[
\boxed{U_\gamma^\dagger U_\gamma=P_{420}.}
\]

Therefore

\[
\boxed{\text{nontrivial holonomy}\neq\text{dissipation}.}
\]

The reverse path obeys

\[
U_{\bar\gamma}=U_\gamma^\dagger,
\qquad
\boxed{U_{\bar\gamma}U_\gamma=P_{420}.}
\]

## Lossless detail memory

No linear map from `C^420` to `C^84` can be injective. Rank-nullity gives

\[
\dim\ker F\ge420-84=336.
\]

The repaired structure keeps the missing detail explicitly:

\[
\boxed{H_{420}\cong H_{84}\otimes M_5.}
\]

This is the address-preserving memory principle: coarse-visible data and five-component detail data remain jointly reconstructive.

## Global causal-layer update

For a layer `N` of mutually disjoint active edges,

\[
\boxed{
U_N(\Omega)=
\left(\prod_{e\in M_N}U_e\right)
\left(\prod_v e^{-i\Delta n H(v)}\right).
}
\]

Then

\[
\boxed{|\Psi_{N+1}\rangle=U_N(\Omega)|\Psi_N\rangle}
\]

and, for unitary/reversible layers,

\[
\boxed{|\Psi_N\rangle=U_N^\dagger(\Omega)|\Psi_{N+1}\rangle.}
\]

For the full history

\[
U_{0:N}=U_N\cdots U_0,
\]

\[
\boxed{U_{0:N}^{-1}=U_0^\dagger\cdots U_N^\dagger.}
\]

This supplies the exact forward/reverse history relation used in the realized-state reconstruction.