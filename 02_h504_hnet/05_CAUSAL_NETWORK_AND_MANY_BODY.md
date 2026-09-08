# 05 — Causal Network and Many-Body Program

## Layered local dynamics

For a set `M_N` of mutually disjoint active edges in causal layer `N`, a finite update may be written

$$
\boxed{
U_N(\Omega)=
\left(\prod_{e\in M_N}U_e\right)
\left(\prod_v e^{-i\Delta n H(v)}\right).
}
$$

The universe/network state evolves by

$$
\boxed{|\Psi_{N+1}\rangle=U_N(\Omega)|\Psi_N\rangle.}
$$

Disjoint/local scheduling yields finite causal cones rather than requiring a single physically fundamental simultaneous cosmic clock.

## Many-cell Hilbert algebra

For a finite cell set `Lambda`, before explicit edge/controller ancillas,

$$
\boxed{\mathcal H_\Lambda=\bigotimes_{v\in\Lambda}\mathbb C^{504}.}
$$

The local observable algebra is

$$
\boxed{\mathcal A_\Lambda=M_{504^{|\Lambda|}}(\mathbb C).}
$$

A thermodynamic/continuum program requires a compatible family of finite regions and embeddings, not one fixed 504-dimensional cell alone.

## Sector-mixing problem

Simple tensor copies of the local Hamiltonian can inherit too many extensive conserved quantities. The native many-body program therefore asks for the smallest intercell operator algebra that:

- preserves required address/gauge/locality structure;
- couples cells nontrivially;
- breaks accidental extensive conservation laws;
- preserves exact global constraints intentionally retained;
- produces testable spectral/transport/thermal behavior as cell number grows.

## CES / chaos / thermal observables

The sector-mixing cartography program uses diagnostics such as:

- level statistics within symmetry-resolved sectors;
- connected spectral observables;
- operator spreading and OTOC-type quantities;
- entanglement growth;
- transport/relaxation observables;
- finite-size scaling of conserved-sector dimensions and gaps.

These diagnostics classify the constructed many-body model. They do not by themselves prove that the model is the realized physical Hnet.

## Parent-action coefficient problem

Intercell sector-mixing coefficients should ultimately be inherited from a parent action/source functional using the same projection discipline as the local seven-operator coefficients, rather than selected by retrospective fitting to desired chaos/thermodynamic behavior.