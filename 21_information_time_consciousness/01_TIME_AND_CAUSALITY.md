# 01 — Time and Causality

UCD distinguishes ordinal succession, causal scheduling, and physical proper time.

## Ordinal succession

At the primitive relational level, one may have an ordered sequence

$$
n=0,1,2,\ldots
$$

without having selected a metric duration. Replacing `n` by

$$
t_n=\alpha n,\qquad \alpha>0
$$

preserves the order for every positive `alpha`. Therefore order alone does not determine a clock scale.

## Finite causal layers

For local asynchronous dynamics, a payload propagates at most one graph edge per causal layer:

$$
\boxed{d_{\rm graph}(x_N,x_{N+1})\le1.}
$$

If observables are initially supported at vertices `x` and `y` and the circuit depth `N` is smaller than their graph distance,

$$
d(x,y)>N,
$$

then the finite-depth local dynamics gives an exact causal-cone statement of the form

$$
\boxed{[A_x(N),B_y]=0.}
$$

for the modeled local circuit.

The integer layer label `N` is a causal scheduling coordinate. It is not by itself a universal physical second.

## Scale-calibrated proper time

Once the one physical scale representative is fixed,

$$
T_*={\hbar\over E_*}.
$$

If a local worldline accumulates `Delta n_v` admitted causal steps, the corresponding calibrated increment is

$$
\boxed{
\Delta t_v=T_*\Delta n_v={\hbar\over E_*}\Delta n_v.
}
$$

Thus `tau=1/72` is a registration ratio in the finite architecture; it is not identified with one second or with a universal cosmic clock.

## Continuum truth boundary

A physical relativistic causal order is stronger than mere update ordering. The current continuum program therefore keeps `CONT-ORDER` separate from ordinal succession and combines it with manifold, volume, dimension, and scale gates before promoting a continuum metric.