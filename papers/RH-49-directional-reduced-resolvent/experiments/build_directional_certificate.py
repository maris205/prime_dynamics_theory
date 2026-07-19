"""Compose the RH-49 analytic and floating quarter-power ledgers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
RH46 = PAPERS / "RH-46-small-noise-mesh-double-pole"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"

FROBENIUS = ROOT / "results" / "reduced_directional_pilot.json"
MIXED = ROOT / "results" / "mixed_operator_gain_pilot.json"
STABLE = ROOT / "results" / "coupling_stable_rank_pilot.json"
OUTPUT = ROOT / "results" / "directional_reduced_resolvent_certificate.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def entry(path: Path, *, local: bool = False):
    base = ROOT if local else REPOSITORY
    return {
        "path": str(path.relative_to(base)),
        "sha256": sha256_file(path),
    }


def fit_power(sigmas, values):
    x = np.log(np.asarray(sigmas, dtype=np.float64))
    y = np.log(np.asarray(values, dtype=np.float64))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(values),
    }


def main() -> None:
    frobenius = load(FROBENIUS)
    mixed = load(MIXED)
    stable = load(STABLE)
    by_sigma_f = {float(row["sigma"]): row for row in frobenius["rows"]}
    by_sigma_m = {float(row["sigma"]): row for row in mixed["rows"]}
    merged = []
    for stable_row in stable["rows"]:
        sigma = float(stable_row["sigma"])
        frobenius_row = by_sigma_f[sigma]
        mixed_row = by_sigma_m[sigma]
        reduced_hs_sum = sum(
            float(branch["maximum_left_reduced_frobenius_gain"])
            * float(branch["maximum_right_reduced_frobenius_gain"])
            for branch in frobenius_row["branches"].values()
        )
        full_hs_sum = sum(
            float(branch["maximum_left_full_frobenius_gain"])
            * float(branch["maximum_right_full_frobenius_gain"])
            for branch in frobenius_row["branches"].values()
        )
        direct_mixed_sum = sum(
            float(branch["mixed_directional_product_candidate"])
            for branch in mixed_row["branches"].values()
        )
        rank_factor = float(
            stable_row["minimum_sqrt_stable_rank_candidate"]
        )
        merged.append(
            {
                "sigma": sigma,
                "fine_dimension": int(stable_row["fine_dimension"]),
                "B_hilbert_schmidt_norm": float(
                    stable_row["B_hilbert_schmidt_norm"]
                ),
                "B_operator_candidate": float(
                    stable_row["B_operator_candidate"]["singular_candidate"]
                ),
                "B_sqrt_stable_rank_candidate": float(
                    stable_row["B_sqrt_stable_rank_candidate"]
                ),
                "C_hilbert_schmidt_norm": float(
                    stable_row["C_hilbert_schmidt_norm"]
                ),
                "C_operator_candidate": float(
                    stable_row["C_operator_candidate"]["singular_candidate"]
                ),
                "C_sqrt_stable_rank_candidate": float(
                    stable_row["C_sqrt_stable_rank_candidate"]
                ),
                "selected_sqrt_stable_rank_candidate": rank_factor,
                "reduced_hilbert_schmidt_gain_sum": reduced_hs_sum,
                "full_hilbert_schmidt_gain_sum": full_hs_sum,
                "stable_rank_transferred_reduced_candidate": (
                    rank_factor * reduced_hs_sum
                ),
                "stable_rank_transferred_full_candidate": (
                    rank_factor * full_hs_sum
                ),
                "direct_mixed_gain_sum_candidate": direct_mixed_sum,
                "direct_mixed_gain_maximum_branch_candidate": float(
                    mixed_row["maximum_mixed_directional_product_candidate"]
                ),
                "critical_half_power_normalized_full_candidate": (
                    rank_factor * full_hs_sum * np.sqrt(sigma)
                ),
                "maximum_gmres_iterations": max(
                    int(branch["maximum_gmres_iterations"])
                    for branch in mixed_row["branches"].values()
                ),
                "maximum_gmres_relative_residual": max(
                    float(branch["maximum_gmres_relative_residual"])
                    for branch in mixed_row["branches"].values()
                ),
                "maximum_branch_leakage": max(
                    float(branch["maximum_branch_leakage"])
                    for branch in mixed_row["branches"].values()
                ),
            }
        )

    sigmas = [row["sigma"] for row in merged]
    fields = (
        "B_hilbert_schmidt_norm",
        "B_operator_candidate",
        "B_sqrt_stable_rank_candidate",
        "C_hilbert_schmidt_norm",
        "C_operator_candidate",
        "C_sqrt_stable_rank_candidate",
        "reduced_hilbert_schmidt_gain_sum",
        "full_hilbert_schmidt_gain_sum",
        "stable_rank_transferred_reduced_candidate",
        "stable_rank_transferred_full_candidate",
        "direct_mixed_gain_sum_candidate",
    )
    fits = {
        field: fit_power(sigmas, [row[field] for row in merged])
        for field in fields
    }
    tail_fits = {
        field: fit_power(
            sigmas[-3:], [row[field] for row in merged[-3:]]
        )
        for field in (
            "reduced_hilbert_schmidt_gain_sum",
            "full_hilbert_schmidt_gain_sum",
            "stable_rank_transferred_full_candidate",
            "direct_mixed_gain_sum_candidate",
        )
    }

    dependencies = {
        "rh38_haar_decay_manuscript": entry(RH38 / "main.tex"),
        "rh46_small_noise_mesh_manuscript": entry(RH46 / "main.tex"),
        "rh48_intrinsic_identification_manuscript": entry(RH48 / "main.tex"),
        "rh48_intrinsic_identification_certificate": entry(
            RH48 / "results" / "intrinsic_riesz_identification_certificate.json"
        ),
        "local_frobenius_directional_pilot": entry(FROBENIUS, local=True),
        "local_mixed_directional_pilot": entry(MIXED, local=True),
        "local_coupling_stable_rank_pilot": entry(STABLE, local=True),
    }
    payload = {
        "status": (
            "rigorous_quarter_power_stable_rank_reduction_with_hilbert_schmidt_directional_gate"
        ),
        "scope": (
            "adjacent Haar couplings and Perron/parity directional resolvents for the small-noise folded-Gaussian quadratic map"
        ),
        "evidence_level": {
            "analytic": (
                "exact rank-one residue deflation, exact stable-rank norm-placement inequality, endpoint packet lower theorem for the canonical cell-average coupling, and residual a-posteriori gain certificate"
            ),
            "numerical": (
                "binary64 sparse exact-Haar Frobenius sums, Hutchinson-GMRES directional estimates, and power-iteration operator candidates; not interval validated"
            ),
        },
        "exact_residue_deflation": {
            "projector": "P=r tensor l*, l*r=1, Q=I-P",
            "identity": (
                "R_circ(z)=(z-T)^-1-P/(z-lambda)=(z-T+lambda P)^-1 Q"
            ),
            "adjoint_identity": (
                "R_circ(z)^*=Q^*(conj(z)-T^*+conj(lambda)P^*)^-1"
            ),
            "branch_pole_removed_exactly": True,
        },
        "stable_rank_transfer": {
            "hilbert_schmidt_gain": (
                "F=sum_s ell_B,s^(2) ell_C,s^(2)"
            ),
            "mixed_gain": (
                "L=sum_s min(ell_B,s^(2)ell_C,s^(infinity), ell_B,s^(infinity)ell_C,s^(2))"
            ),
            "inequality": (
                "L <= F min(||B||_S2/||B||, ||C||_S2/||C||)"
            ),
            "global_resolvent_norm_needed_for_the_inequality": False,
        },
        "critical_endpoint_coupling_theorem": {
            "mesh": "h=1/n with h/sigma -> 0",
            "coupling": "B=E_n K_sigma (E_2n-E_n)",
            "hilbert_schmidt_upper": "||B||_S2=O(h sigma^(-3/2))",
            "operator_lower": "||B|| >= c h sigma^(-5/4)",
            "sqrt_stable_rank_upper": (
                "||B||_S2/||B||=O(sigma^(-1/4))"
            ),
            "mechanism": (
                "a target Haar packet at width sigma is amplified on the source critical layer x=sqrt(sigma) xi"
            ),
            "stored_sparse_cutoff_family_proved_by_this_theorem": False,
        },
        "quarter_power_closure": {
            "premise": (
                "sup_j F_(2^j n,sigma)=O(sigma^(-delta))"
            ),
            "conclusion": (
                "sup_j L_(2^j n,sigma)=O(sigma^(-1/4-delta))"
            ),
            "rh48_gamma": "gamma=1/4+delta",
            "preserves_every_strict_p_greater_than_2_when": "delta<=1/4",
            "uniform_or_polylog_hilbert_schmidt_gain_is_sufficient": True,
            "hilbert_schmidt_gain_bound_proved_for_full_family_here": False,
        },
        "residual_certificate": {
            "identity": "R_circ E-X=(z-T+lambda P)^-1(QE-(z-T+lambda P)X)",
            "upper": (
                "||R_circ E||_S2 <= ||X||_S2 + M ||QE-(z-T+lambda P)X||_S2"
            ),
            "dual_version": (
                "apply the same estimate to the adjoint solve for C R_circ"
            ),
            "finite_matrix_validation_route": (
                "validated reduced-inverse budget plus outward primal/adjoint residual and norm bounds"
            ),
        },
        "floating_five_scale_audit": {
            "rows": merged,
            "fits": fits,
            "last_three_level_fits": tail_fits,
            "noise_levels": len(merged),
            "largest_dimension": max(row["fine_dimension"] for row in merged),
            "quarter_power_target": 0.25,
            "rh48_critical_exponent": 0.5,
            "operator_candidates_are_validated_uppers": False,
            "hutchinson_gains_are_validated_uppers": False,
        },
        "dependencies": dependencies,
        "limitations": [
            "The endpoint packet theorem is analytic for the canonical conditioned cell-average kernel; a uniform hard-cutoff and stored-matrix transfer is not proved here.",
            "The five-scale Hilbert-Schmidt directional plateau is a Hutchinson-GMRES diagnostic, not a validated asymptotic upper.",
            "Power iteration gives operator-norm lower candidates, not validated uppers; the resulting floating stable-rank ratios are diagnostics.",
            "Only an empirically worst real contour node is used in the direct mixed operator audit; the all-node audit is the Hilbert-Schmidt one.",
            "No arithmetic trace formula, prime-power identity, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, or Riemann-hypothesis conclusion is claimed.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "B_sqrt_stable_rank_fit": fits[
                    "B_sqrt_stable_rank_candidate"
                ],
                "full_hilbert_schmidt_fit": fits[
                    "full_hilbert_schmidt_gain_sum"
                ],
                "transferred_full_fit": fits[
                    "stable_rank_transferred_full_candidate"
                ],
                "direct_mixed_fit": fits[
                    "direct_mixed_gain_sum_candidate"
                ],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
