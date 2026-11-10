#!/usr/bin/env python3
"""
UCD 504-State Master Hamiltonian Workbench

Self-contained reconstruction of the 504-state UCD Hamiltonian:
    H_504 = exp(-tau) * (T1 + eta*T2 + kappa*T3 + gamma*T4 + mu*T5 + nu*T6 + delta*T7)

Hilbert space:
    H_504 = V7 \otimes C^3 \otimes C[Dic_6]
    dim = 7 * 3 * 24 = 504

This script verifies:
  1. Dic_6 group construction and regular representations.
  2. Hermiticity of H_504.
  3. Right-regular Dic_6 symmetry of H_504.
  4. Irrep projector ranks and resolution of identity.
  5. Universal ring gap Delta = 2*kappa*exp(-tau) in all Dic_6 irrep blocks.
  6. Direct center projection kills the leaf-ring term.
  7. Center-leaf Schur reduction inherits kappa-dependence.

Outputs CSV/JSON files in the selected output directory.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Tuple

import numpy as np

GroupElement = Tuple[int, int]  # (k,e) = a^k x^e, k mod 12, e in {0,1}

TAU = 1.0 / 72.0
EXP = math.exp(-TAU)
DEFAULT_COEFFICIENTS = {
    "c1": 1.0,
    "eta": 0.50,
    "kappa": 0.10,
    "gamma": 0.10,
    "mu": 1.10,
    "nu": 0.10,
    "delta": 0.30,
}


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def E(n: int, i: int, j: int) -> np.ndarray:
    M = np.zeros((n, n), dtype=complex)
    M[i, j] = 1.0
    return M


# -----------------------------------------------------------------------------
# Dic_6 group: a^12 = 1, x^2 = a^6, x a x^-1 = a^-1
# Elements represented as a^k x^e, e=0 or 1.
# Multiplication rule:
#   (a^k x^e)(a^l x^f) = a^{k + (-1)^e l + 6 e f} x^{e+f mod 2}
# -----------------------------------------------------------------------------

def dic6_mul(g: GroupElement, h: GroupElement) -> GroupElement:
    k, e = g
    l, f = h
    new_e = (e + f) % 2
    new_k = (k + ((-1) ** e) * l + 6 * e * f) % 12
    return (new_k, new_e)


def dic6_inv(g: GroupElement) -> GroupElement:
    for h in ELEMS:
        if dic6_mul(g, h) == (0, 0) and dic6_mul(h, g) == (0, 0):
            return h
    raise ValueError(f"No inverse found for {g}")


ELEMS: List[GroupElement] = [(k, e) for k in range(12) for e in range(2)]
IDX: Dict[GroupElement, int] = {g: i for i, g in enumerate(ELEMS)}


def left_regular(g: GroupElement) -> np.ndarray:
    L = np.zeros((24, 24), dtype=complex)
    for j, h in enumerate(ELEMS):
        gh = dic6_mul(g, h)
        L[IDX[gh], j] = 1.0
    return L


def right_regular(g: GroupElement) -> np.ndarray:
    # Representation convention: R(g)|h> = |h g^-1>
    R = np.zeros((24, 24), dtype=complex)
    inv_g = dic6_inv(g)
    for j, h in enumerate(ELEMS):
        hg = dic6_mul(h, inv_g)
        R[IDX[hg], j] = 1.0
    return R


def one_dim_character(eps_a: int, eps_b: int) -> Callable[[GroupElement], complex]:
    # Abelianized characters: chi(a)=eps_a, chi(x)=eps_b.
    # Since a becomes order 2 in abelianization, chi(a^k x^e)=eps_a^k eps_b^e.
    def chi(g: GroupElement) -> complex:
        k, e = g
        return (eps_a ** k) * (eps_b ** e)
    return chi


def two_dim_character(j: int) -> Callable[[GroupElement], complex]:
    # Dicyclic 2D irreps for j=1..5:
    # chi_j(a^k)=2 cos(pi*j*k/6), chi_j(a^k x)=0.
    def chi(g: GroupElement) -> complex:
        k, e = g
        if e == 1:
            return 0.0
        return 2.0 * math.cos(math.pi * j * k / 6.0)
    return chi


@dataclass
class Irrep:
    kind: str
    name: str
    dim: int
    chi: Callable[[GroupElement], complex]


def irreps() -> List[Irrep]:
    out: List[Irrep] = []
    for eps_a in [1, -1]:
        for eps_b in [1, -1]:
            out.append(Irrep("1d", f"eps_a={eps_a},eps_b={eps_b}", 1, one_dim_character(eps_a, eps_b)))
    for j in range(1, 6):
        out.append(Irrep("2d", f"j={j}", 2, two_dim_character(j)))
    return out


def isotypic_projector(ir: Irrep) -> np.ndarray:
    P = np.zeros((24, 24), dtype=complex)
    for g in ELEMS:
        P += np.conj(ir.chi(g)) * right_regular(g)
    return (ir.dim / len(ELEMS)) * P


# -----------------------------------------------------------------------------
# V7 and family operators
# -----------------------------------------------------------------------------

def V7_ops() -> Dict[str, np.ndarray]:
    I7 = np.eye(7, dtype=complex)
    Pc = E(7, 0, 0)
    R7 = I7 - Pc
    A7 = np.zeros((7, 7), dtype=complex)
    for i in range(1, 7):
        A7[0, i] = 1.0
        A7[i, 0] = 1.0
    Tp = np.zeros((7, 7), dtype=complex)
    Tm = np.zeros((7, 7), dtype=complex)
    for i in range(1, 7):
        # Leaf labels 1..6, cyclic ring.
        Tp[1 + (i % 6), i] = 1.0
        Tm[1 + ((i - 2) % 6), i] = 1.0
    return {"I7": I7, "Pc": Pc, "R7": R7, "A7": A7, "Rring": Tp + Tm, "Tp": Tp, "Tm": Tm}


def F3_ops() -> Dict[str, np.ndarray]:
    I3 = np.eye(3, dtype=complex)
    R = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    XZ = R + R.conj().T
    JZ = (R - R.conj().T) / (1j * math.sqrt(3.0))
    H = np.diag([-1, 0, 1]).astype(complex)
    H2 = np.diag([1, 0, 1]).astype(complex)
    P0_minus_P2 = E(3, 0, 0) - E(3, 2, 2)
    return {"I3": I3, "R": R, "XZ": XZ, "JZ": JZ, "H": H, "H2": H2, "P0_minus_P2": P0_minus_P2}


def kron3(A: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(A, B), C)


@dataclass
class HamiltonianTerms:
    names: List[str]
    terms: List[np.ndarray]


def build_terms(rho_curr_mode: str = "reflection") -> HamiltonianTerms:
    v = V7_ops()
    f = F3_ops()
    I24 = np.eye(24, dtype=complex)
    La = left_regular((1, 0))
    Lx = left_regular((0, 1))
    La6 = left_regular((6, 0))
    rho_orient = 0.5 * (La + La.conj().T)
    if rho_curr_mode == "reflection":
        rho_curr = 0.5 * (Lx + Lx.conj().T)
    elif rho_curr_mode == "rotation_sine":
        rho_curr = (La - La.conj().T) / (2j)
    else:
        raise ValueError("rho_curr_mode must be 'reflection' or 'rotation_sine'")
    terms = [
        kron3(v["A7"], f["I3"], I24),
        kron3(v["I7"], f["XZ"], I24),
        kron3(v["Rring"], f["I3"], I24),
        kron3(v["A7"], f["I3"], La6),
        kron3(v["I7"], f["XZ"], rho_orient),
        kron3(v["I7"], f["JZ"], rho_curr),
        kron3(v["R7"], f["P0_minus_P2"], I24),
    ]
    names = ["T1_star", "T2_family_XZ", "T3_leaf_ring", "T4_central_parity", "T5_orientation_mix", "T6_current", "T7_leaf_family_selector"]
    return HamiltonianTerms(names, terms)


def build_H504(coeffs: Dict[str, float] | None = None, rho_curr_mode: str = "reflection") -> np.ndarray:
    c = DEFAULT_COEFFICIENTS.copy()
    if coeffs:
        c.update(coeffs)
    ht = build_terms(rho_curr_mode)
    scalars = [c["c1"], c["eta"], c["kappa"], c["gamma"], c["mu"], c["nu"], c["delta"]]
    H = np.zeros_like(ht.terms[0])
    for s, T in zip(scalars, ht.terms):
        H += s * T
    return EXP * H


def projector_basis(P: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    # Hermitian projector; use eigh for a stable orthonormal range basis.
    vals, vecs = np.linalg.eigh((P + P.conj().T) / 2.0)
    idx = np.where(vals > 1.0 - tol)[0]
    return vecs[:, idx]


def irrep_block(H: np.ndarray, P24: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # Use a small 24-dimensional basis first, then tensor it up.
    # This avoids a 504-dimensional projector eigendecomposition.
    I7 = np.eye(7, dtype=complex)
    I3 = np.eye(3, dtype=complex)
    U24 = projector_basis(P24)
    B = np.kron(np.kron(I7, I3), U24)
    Hb = B.conj().T @ H @ B
    return Hb, B


def unique_clusters(evals: np.ndarray, tol: float = 1e-8) -> List[Tuple[float, int]]:
    vals = sorted(float(x) for x in evals.real)
    clusters: List[Tuple[float, int]] = []
    for x in vals:
        if not clusters or abs(x - clusters[-1][0]) > tol:
            clusters.append((x, 1))
        else:
            old, n = clusters[-1]
            clusters[-1] = ((old * n + x) / (n + 1), n + 1)
    return clusters


def closest_gap(clusters: List[Tuple[float, int]], target: float) -> Tuple[int, float, float, int, int, float, float]:
    gaps = []
    for i in range(len(clusters) - 1):
        gap = clusters[i + 1][0] - clusters[i][0]
        gaps.append((i, gap, abs(gap - target), clusters[i][1], clusters[i + 1][1], clusters[i][0], clusters[i + 1][0]))
    return min(gaps, key=lambda row: row[2])


def hellmann_sensitivity_for_cluster_gap(H: np.ndarray, terms: HamiltonianTerms, B: np.ndarray, lower: float, upper: float, tol: float = 1e-8) -> Dict[str, float]:
    Hb = B.conj().T @ H @ B
    vals, vecs = np.linalg.eigh(Hb)
    lower_idx = np.where(np.abs(vals - lower) < tol)[0]
    upper_idx = np.where(np.abs(vals - upper) < tol)[0]
    out: Dict[str, float] = {}
    for name, T in zip(terms.names, terms.terms):
        Tb = B.conj().T @ (EXP * T) @ B  # derivative wrt coefficient includes exp(-tau)
        if len(lower_idx) == 0 or len(upper_idx) == 0:
            out[name] = float("nan")
            continue
        Plo = vecs[:, lower_idx]
        Pup = vecs[:, upper_idx]
        elo = np.trace(Plo.conj().T @ Tb @ Plo).real / len(lower_idx)
        eup = np.trace(Pup.conj().T @ Tb @ Pup).real / len(upper_idx)
        out[name] = float(eup - elo)
    return out


def direct_center_projection_blocks(H: np.ndarray) -> Dict[str, np.ndarray]:
    # Project to center anchor and one-dimensional Dic_6 character projectors.
    e0 = np.zeros((7, 1), dtype=complex); e0[0, 0] = 1.0
    I3 = np.eye(3, dtype=complex)
    blocks = {}
    for ir in irreps():
        if ir.dim != 1:
            continue
        U24 = projector_basis(isotypic_projector(ir))
        B = np.kron(np.kron(e0, I3), U24)
        blocks[ir.name] = B.conj().T @ H @ B
    return blocks


def schur_center_blocks(H: np.ndarray, z: float = 0.0) -> Dict[str, np.ndarray]:
    # Sector-wise Schur reduction onto center anchor for each 1D character sector.
    e0 = np.zeros((7, 1), dtype=complex); e0[0, 0] = 1.0
    leaf = np.zeros((7, 6), dtype=complex)
    for i in range(6):
        leaf[i + 1, i] = 1.0
    I3 = np.eye(3, dtype=complex)
    blocks = {}
    for ir in irreps():
        if ir.dim != 1:
            continue
        U24 = projector_basis(isotypic_projector(ir))
        Bc = np.kron(np.kron(e0, I3), U24)
        Bl = np.kron(np.kron(leaf, I3), U24)
        Hcc = Bc.conj().T @ H @ Bc
        Hcl = Bc.conj().T @ H @ Bl
        Hlc = Bl.conj().T @ H @ Bc
        Hll = Bl.conj().T @ H @ Bl
        inv = np.linalg.pinv(Hll - z * np.eye(Hll.shape[0]))
        blocks[ir.name] = Hcc - Hcl @ inv @ Hlc
    return blocks

def write_csv(path: str, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def matrix_to_nested_real_imag(M: np.ndarray) -> List[List[Dict[str, float]]]:
    return [[{"re": float(z.real), "im": float(z.imag)} for z in row] for row in M]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="/mnt/data/ucd_504_master_hamiltonian")
    parser.add_argument("--rho-curr-mode", default="reflection", choices=["reflection", "rotation_sine"])
    args = parser.parse_args()
    out = args.out
    ensure_dir(out)

    H = build_H504(rho_curr_mode=args.rho_curr_mode)
    ht = build_terms(args.rho_curr_mode)

    # Basic checks
    herm_resid = float(np.linalg.norm(H - H.conj().T))
    I7 = np.eye(7, dtype=complex)
    I3 = np.eye(3, dtype=complex)
    Ra = kron3(I7, I3, right_regular((1, 0)))
    Rx = kron3(I7, I3, right_regular((0, 1)))
    comm_Ra = float(np.linalg.norm(H @ Ra - Ra @ H))
    comm_Rx = float(np.linalg.norm(H @ Rx - Rx @ H))

    # Projector checks and gap blocks
    totalP = np.zeros((24, 24), dtype=complex)
    projector_rows = []
    gap_rows = []
    sens_rows = []
    target_gap = 2.0 * DEFAULT_COEFFICIENTS["kappa"] * EXP
    max_gap_dev = 0.0
    max_non_ring_sens = 0.0
    for ir in irreps():
        P24 = isotypic_projector(ir)
        totalP += P24
        rank24 = int(round(np.trace(P24).real))
        idem = float(np.linalg.norm(P24 @ P24 - P24))
        projector_rows.append({
            "kind": ir.kind,
            "name": ir.name,
            "irrep_dim": ir.dim,
            "projector_rank_24": rank24,
            "projector_rank_504": 21 * rank24,
            "idempotency_residual": idem,
        })
        Hb, B = irrep_block(H, P24)
        evals = np.linalg.eigvalsh(Hb)
        clusters = unique_clusters(evals, tol=1e-7)
        idx, gap, dev, nlo, nhi, lower, upper = closest_gap(clusters, target_gap)
        max_gap_dev = max(max_gap_dev, dev)
        gap_rows.append({
            "kind": ir.kind,
            "name": ir.name,
            "block_dim": Hb.shape[0],
            "num_unique_clusters": len(clusters),
            "target_gap_2kappa_exp_minus_tau": target_gap,
            "closest_gap": gap,
            "deviation": dev,
            "lower_cluster_value": lower,
            "upper_cluster_value": upper,
            "lower_cluster_multiplicity": nlo,
            "upper_cluster_multiplicity": nhi,
        })
        sens = hellmann_sensitivity_for_cluster_gap(H, ht, B, lower, upper, tol=1e-7)
        for term_name, value in sens.items():
            if term_name != "T3_leaf_ring":
                max_non_ring_sens = max(max_non_ring_sens, abs(value))
            sens_rows.append({
                "kind": ir.kind,
                "name": ir.name,
                "term": term_name,
                "sensitivity_d_gap_d_coefficient": value,
            })

    projector_sum_resid = float(np.linalg.norm(totalP - np.eye(24)))

    # Direct center derivative wrt kappa and Schur derivative wrt kappa
    eps = 1e-5
    coeff_plus = DEFAULT_COEFFICIENTS.copy(); coeff_plus["kappa"] += eps
    coeff_minus = DEFAULT_COEFFICIENTS.copy(); coeff_minus["kappa"] -= eps
    H_plus = build_H504(coeff_plus, args.rho_curr_mode)
    H_minus = build_H504(coeff_minus, args.rho_curr_mode)
    direct_plus = direct_center_projection_blocks(H_plus)
    direct_minus = direct_center_projection_blocks(H_minus)
    schur_plus = schur_center_blocks(H_plus)
    schur_minus = schur_center_blocks(H_minus)
    proj_rows = []
    for name in direct_plus:
        d_deriv = (direct_plus[name] - direct_minus[name]) / (2 * eps)
        s_deriv = (schur_plus[name] - schur_minus[name]) / (2 * eps)
        proj_rows.append({
            "sector_character": name,
            "direct_dH_dkappa_frobenius": float(np.linalg.norm(d_deriv)),
            "schur_dH_dkappa_frobenius": float(np.linalg.norm(s_deriv)),
            "direct_block_trace_real": float(np.trace(direct_center_projection_blocks(H)[name]).real),
            "schur_block_trace_real": float(np.trace(schur_center_blocks(H)[name]).real),
        })

    # Save CSVs
    write_csv(os.path.join(out, "irrep_projector_checks.csv"), projector_rows, list(projector_rows[0].keys()))
    write_csv(os.path.join(out, "ring_gap_by_irrep.csv"), gap_rows, list(gap_rows[0].keys()))
    write_csv(os.path.join(out, "ring_gap_sensitivities.csv"), sens_rows, list(sens_rows[0].keys()))
    write_csv(os.path.join(out, "projection_kappa_inheritance.csv"), proj_rows, list(proj_rows[0].keys()))

    # Operator spec
    spec = {
        "tau": TAU,
        "exp_minus_tau": EXP,
        "hilbert_space": "V7 tensor C^3 tensor C[Dic_6]",
        "dimension": 504,
        "dic6_presentation": "<a,x | a^12=1, x^2=a^6, x a x^-1=a^-1>",
        "coefficients": DEFAULT_COEFFICIENTS,
        "rho_orient": "0.5*(L(a)+L(a)^*)",
        "rho_curr_mode": args.rho_curr_mode,
        "rho_curr": "0.5*(L(x)+L(x)^*)" if args.rho_curr_mode == "reflection" else "(L(a)-L(a)^*)/(2i)",
        "terms": [
            {"name": "T1_star", "formula": "A7 tensor I3 tensor I24"},
            {"name": "T2_family_XZ", "formula": "I7 tensor XZ tensor I24"},
            {"name": "T3_leaf_ring", "formula": "R_ring tensor I3 tensor I24"},
            {"name": "T4_central_parity", "formula": "A7 tensor I3 tensor L(a^6)"},
            {"name": "T5_orientation_mix", "formula": "I7 tensor XZ tensor rho_orient"},
            {"name": "T6_current", "formula": "I7 tensor JZ tensor rho_curr"},
            {"name": "T7_leaf_family_selector", "formula": "R7 tensor (P0-P2) tensor I24"},
        ],
    }
    with open(os.path.join(out, "h504_master_operator_spec.json"), "w") as f:
        json.dump(spec, f, indent=2)

    # Projected blocks JSON
    direct_blocks = direct_center_projection_blocks(H)
    schur_blocks = schur_center_blocks(H)
    blocks_json = {
        "direct_center_projection_blocks": {k: matrix_to_nested_real_imag(v) for k, v in direct_blocks.items()},
        "schur_center_reduction_blocks_z0": {k: matrix_to_nested_real_imag(v) for k, v in schur_blocks.items()},
    }
    with open(os.path.join(out, "h504_projected_blocks.json"), "w") as f:
        json.dump(blocks_json, f, indent=2)

    summary = {
        "dimension": 504,
        "tau": TAU,
        "exp_minus_tau": EXP,
        "canonical_kappa": DEFAULT_COEFFICIENTS["kappa"],
        "target_ring_gap": target_gap,
        "hermiticity_residual": herm_resid,
        "right_regular_commutator_norm_a": comm_Ra,
        "right_regular_commutator_norm_x": comm_Rx,
        "projector_sum_residual": projector_sum_resid,
        "max_ring_gap_deviation_across_irreps": max_gap_dev,
        "expected_d_gap_d_kappa": 2 * EXP,
        "max_non_ring_sensitivity_abs": max_non_ring_sens,
        "direct_projection_max_dH_dkappa_norm": max(r["direct_dH_dkappa_frobenius"] for r in proj_rows),
        "schur_projection_min_dH_dkappa_norm": min(r["schur_dH_dkappa_frobenius"] for r in proj_rows),
        "schur_projection_max_dH_dkappa_norm": max(r["schur_dH_dkappa_frobenius"] for r in proj_rows),
    }
    with open(os.path.join(out, "h504_master_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
