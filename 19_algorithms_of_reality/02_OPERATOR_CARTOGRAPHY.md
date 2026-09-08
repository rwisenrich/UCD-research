# 02 — Operator Cartography

Operator Cartography searches the same source object through multiple exact representations and records where structure is sparse, stable, forbidden, or connected.

## Core principle

Different representations do not create different mathematical facts. They expose different sparsity patterns, symmetries, residuals, commutants, and obstruction structures of the same source object.

The cartography engine therefore maintains a representation family

$$
\mathcal R_1,\ldots,\mathcal R_m
$$

for one source object `X`, together with operators

$$
\mathcal O_1,\ldots,\mathcal O_n.
$$

For each pair it records observables such as

$$
\boxed{
C_{ij}=\|[\mathcal R_i(X),\mathcal O_j]\|
}
$$

or the appropriate exact rank, spectrum, overlap, residual, connectivity, or invariant signature.

## Search roles

Cartography is used to:

- find invariant or approximately invariant subspaces;
- identify operators that connect otherwise isolated sectors;
- separate alive, flickering, and dead operator channels;
- map symmetry-protected exclusions;
- discover which projection loses information and which Schur/Feshbach reduction restores it;
- build projector-growth paths from measured residual directions rather than guessing a final projector;
- compare equivalent laws found independently in matrix, graph, polynomial, spectral, tensor, or combinatorial form.

## Cross-representation identity

If two discoveries in different lenses prove the same mathematical relation, they should map to one canonical law object:

$$
\boxed{
\text{same relation in different representations}
\Rightarrow
\text{one canonical theorem identity + multiple proof lenses}.
}
$$

This prevents the project from inflating its evidence count by rediscovering the same fact in several encodings.

## Negative cartography

A stable absence is itself informative. If every legal operator in a defined family fails to connect two sectors, that result is stored as an obstruction/no-go candidate with the tested family and scope stated explicitly.