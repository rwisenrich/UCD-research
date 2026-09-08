# 02 — Realized State, Law, and Scale

UCD separates universal law from realized boundary/initial data.

## Realized state

The current realized-state object is

\[
\boxed{
\Omega_0=(\Gamma,\{W_e\},\sigma,\Pi_{\partial},\Psi_0)
}
\]

where `Gamma` denotes the realized carrier/network structure, `{W_e}` the realized link data, `sigma` the orientation/history selector data, `Pi_partial` the boundary realization, and `Psi_0` the initial state.

The local law does not choose its own initial state:

\[
U:\Psi_0\mapsto\Psi_1
\]

does not imply a map

\[
U\mapsto\Psi_0.
\]

Therefore

\[
\boxed{\text{LAW}\neq\text{REALIZED STATE}.}
\]

Given a complete later microstate together with the retained reversible history,

\[
\boxed{
\Omega_0=U_{0:N}^{\dagger}\Omega_N.
}
\]

This is an inverse-history statement, not a claim that present macroscopic observations contain complete microscopic information.

## One dimensional scale representative

The dimensionless UCD kernel is converted to physical units by one scale representative:

\[
\boxed{
H_{\rm phys}=E_*H_{\rm UCD},
\qquad
T_*={\hbar\over E_*},
\qquad
L_*={\hbar c\over E_*}.
}
\]

The dimensionless theory does not select an SI value for `E_*` internally. One physical calibration fixes the representative.

The executable specification is therefore written

\[
\boxed{
\mathcal U_{\rm UCD}=\mathcal L_{\rm UCD}+\Omega_0+[E_*].
}
\]

This prevents three different categories from being conflated:

- universal local law;
- realized state/history;
- dimensional calibration.

## State-dependent effective quantities

Downstream effective couplings and spectra are allowed to depend on the realized state through well-defined functionals. For example, the boundary/action metric is

\[
\boxed{
G_{AB}(\Omega)=\operatorname{Tr}(\rho_\Omega J_A^\dagger J_B).
}
\]

Once `Omega_0` is frozen, the corresponding effective quantities are determined by the specified functional. They are not licensed to be independently retuned sector by sector.