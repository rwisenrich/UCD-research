# 03 — Hnet Transport and Boundary Overlap

## Internal link algebra

For a legal oriented edge `i -> j`,

$$
m_{ij}\in Z_3,
\qquad
g_{ij}\in {\rm Dic}_6,
$$

and

$$
\boxed{W_{ij}=S_{Z_3}^{m_{ij}}\otimes L(g_{ij}).}
$$

The reversed link is

$$
\boxed{W_{ji}=W_{ij}^{-1}=W_{ij}^\dagger.}
$$

Left and right Dic6 regular actions commute:

$$
\boxed{[L(g),R(h)]=0.}
$$

This permits the established logical/transport versus gauge/syndrome separation.

## Gauge-assisted routed sector

With a right-gauge shift `q`, define

$$
U(m,g,q)=R(q)[S_3^m\otimes L(g)]
$$

and

$$
\boxed{T=U(m,g,q)P_{420}.}
$$

The exact routed-sector identities are

$$
\boxed{T^\dagger T=P_{420},\qquad TT^\dagger=P_{420}}
$$

and

$$
\boxed{P_{84}TP_{420}=0.}
$$

The canonical finite test family contains `3 x 24 x 24 = 1,728` link/gauge combinations.

## V7 boundary admission

Let

$$
|r_0\rangle={1\over\sqrt6}\sum_{j=1}^{6}|j\rangle
$$

be the uniform six-boundary mode and `|c>` the center. Define

$$
\boxed{E=|c\rangle\langle r_0|.}
$$

Then

$$
\boxed{E^\dagger E=P_{r_0},\qquad EE^\dagger=P_c.}
$$

Any ring mode orthogonal to `r_0` is refused by this map.

## Boundary-overlap tensor

For a directed intercell edge,

$$
\boxed{
\mathcal B_{j\leftarrow i}
=|c_j\rangle\langle r_{0,i}|\otimes W_{ij}.
}
$$

Hence

$$
\mathcal B^\dagger\mathcal B=P_{r_0}\otimes I_{72},
\qquad
\mathcal B\mathcal B^\dagger=P_c\otimes I_{72}.
$$

The edge generator

$$
K_e=|j\rangle\langle i|\otimes\mathcal B_e+|i\rangle\langle j|\otimes\mathcal B_e^\dagger
$$

is Hermitian, so

$$
\boxed{U_e(\theta)=e^{-i\theta K_e}}
$$

is unitary. Any factor such as `e^{-tau}` multiplying the Hermitian generator changes the evolution rate; it is not automatically a norm attenuation factor.