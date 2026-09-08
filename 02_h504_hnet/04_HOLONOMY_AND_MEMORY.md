# 04 — Holonomy, Reverse History, and Memory Dilation

## Path product

For an oriented path

$$
\gamma=(e_1,e_2,\ldots,e_N),
$$

set

$$
\boxed{U_\gamma=T_{e_N}\cdots T_{e_1}.}
$$

On a flat closed cycle the product can return the legal sector to itself. A curved/nontrivial loop may instead satisfy

$$
U_\gamma\neq P_{420}
$$

while still obeying

$$
\boxed{U_\gamma^\dagger U_\gamma=P_{420}.}
$$

Therefore

$$
\boxed{\text{nontrivial holonomy}\neq\text{dissipation}.}
$$

The reverse path is

$$
\boxed{U_{\bar\gamma}=U_\gamma^\dagger}
$$

and consequently

$$
\boxed{U_{\bar\gamma}U_\gamma=P_{420}.}
$$

## Compression obstruction

For any linear map

$$
F:\mathbb C^{420}\to\mathbb C^{84},
$$

rank-nullity gives

$$
\boxed{\dim\ker F\ge420-84=336.}
$$

So direct one-cell 420-to-84 lossless compression is impossible.

## Minimal detail memory

The six-sheet decomposition provides the repaired factorization

$$
\boxed{H_{420}\cong H_{84}\otimes M_5.}
$$

With a `6 x 5` orthonormal zero-sum basis `B`,

$$
B^TB=I_5,
\qquad
B^Tu_0=0,
$$

and

$$
BB^T=I_6-{1\over6}\mathbf1\mathbf1^T.
$$

The detail coordinates retain the five nonuniform modes that a quotient-only representation would lose.

## Full history reconstruction

For causal layers

$$
U_{0:N}=U_NU_{N-1}\cdots U_0,
$$

reversibility gives

$$
\boxed{U_{0:N}^{-1}=U_0^\dagger\cdots U_{N-1}^\dagger U_N^\dagger.}
$$

Thus, if the complete state and retained reversible history are available, prior states are reconstructible by the adjoint history. This is the mathematical basis of the realized-state inverse relation used in the Theory-of-Reality branch.