"""Compose RH-50 two-pole Hardy, residue, and no-go ledgers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
PILOT = ROOT / "results" / "two_pole_hardy_pilot.json"
OUTPUT = ROOT / "results" / "two_pole_hardy_certificate.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        "vanishing_exponent": float(max(0.0, slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(values),
    }


def residue_values(rows, side: str, mode: str):
    ledger_name = "fine_left" if side == "left" else "coarse_right"
    field = (
        "left_residue_action_over_B_hilbert_schmidt"
        if side == "left"
        else "right_residue_action_over_C_hilbert_schmidt"
    )
    values = []
    for row in rows:
        item = next(
            record
            for record in row["residue_action_ledgers"][ledger_name]
            if record["mode"] == mode
        )
        values.append(float(item[field]))
    return values


def main() -> None:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = pilot["rows"]
    sigmas = [float(row["sigma"]) for row in rows]
    residue_fits = {}
    for side in ("left", "right"):
        for mode in ("perron", "parity"):
            values = residue_values(rows, side, mode)
            if max(values) < 1.0e-12:
                residue_fits[f"{side}_{mode}"] = {
                    "values": values,
                    "numerically_zero": True,
                    "fit": None,
                }
            else:
                residue_fits[f"{side}_{mode}"] = {
                    "values": values,
                    "numerically_zero": False,
                    "fit": fit_power(sigmas, values),
                }

    merged_rows = []
    for row in rows:
        maximum_bulk_product = max(
            float(branch["maximum_bulk_gain_product_candidate"])
            for branch in row["branches"].values()
        )
        maximum_hardy_left = max(
            float(branch["hardy_bounds"]["r=0.85"][
                "left_bulk_gain_upper_candidate"
            ])
            for branch in row["branches"].values()
        )
        maximum_hardy_right = max(
            float(branch["hardy_bounds"]["r=0.85"][
                "right_bulk_gain_upper_candidate"
            ])
            for branch in row["branches"].values()
        )
        merged_rows.append(
            {
                "sigma": float(row["sigma"]),
                "fine_dimension": int(row["fine_dimension"]),
                "fine_bulk_radius_candidate": float(
                    row["fine_bulk_radius_candidate"]
                ),
                "left_tail_decay_base": float(
                    row["left_tail_fit"]["decay_base"]
                ),
                "right_tail_decay_base": float(
                    row["right_tail_fit"]["decay_base"]
                ),
                "left_hardy_energy_r085": float(
                    row["hardy_energies"]["r=0.85"][
                        "left_truncated_hardy_energy"
                    ]
                ),
                "right_hardy_energy_r085": float(
                    row["hardy_energies"]["r=0.85"][
                        "right_truncated_hardy_energy"
                    ]
                ),
                "maximum_two_pole_bulk_product_candidate": maximum_bulk_product,
                "maximum_left_hardy_upper_candidate_r085": maximum_hardy_left,
                "maximum_right_hardy_upper_candidate_r085": maximum_hardy_right,
                "left_perron_residue_gain": residue_values(
                    [row], "left", "perron"
                )[0],
                "left_parity_residue_gain": residue_values(
                    [row], "left", "parity"
                )[0],
                "right_perron_residue_gain": residue_values(
                    [row], "right", "perron"
                )[0],
                "right_parity_residue_gain": residue_values(
                    [row], "right", "parity"
                )[0],
                "left_power_at_maximum_horizon": float(
                    row["left_power_gain_sequence"][-1]
                ),
                "right_power_at_maximum_horizon": float(
                    row["right_power_gain_sequence"][-1]
                ),
            }
        )

    dependencies = {
        "rh14_boundary_layer_manuscript": entry(RH14 / "main.tex"),
        "rh47_logarithmic_conditioning_manuscript": entry(RH47 / "main.tex"),
        "rh49_quarter_power_manuscript": entry(RH49 / "main.tex"),
        "rh49_directional_certificate": entry(
            RH49 / "results" / "directional_reduced_resolvent_certificate.json"
        ),
        "local_two_pole_hardy_pilot": entry(PILOT, local=True),
    }
    payload = {
        "status": (
            "rigorous_two_pole_hardy_stein_reduction_with_global_contraction_no_go_and_directional_energy_gate"
        ),
        "scope": (
            "Perron/parity two-pole bulk Hilbert-Schmidt range resolvents for adjacent Haar compressions of the folded-Gaussian quadratic operator"
        ),
        "evidence_level": {
            "analytic": (
                "exact two-pole Laurent decomposition, Hardy-energy contour upper, positive Stein supersolution certificate, sharp square-root-spike derivative scale, exact residue block identity, two-sided outgoing coupling scale, and deterministic global-contraction no-go"
            ),
            "numerical": (
                "binary64 exact-Haar two-pole power audit with Hutchinson Hilbert-Schmidt traces through time 64; not interval validated"
            ),
        },
        "two_pole_decomposition": {
            "projection": "P_per=P_++P_-, Q=I-P_per",
            "bulk": "N=T-lambda_+ P_+-lambda_- P_-",
            "resolvent": (
                "(z-T)^-1=P_+/(z-lambda_+)+P_-/(z-lambda_-)+(z-N)^-1 Q"
            ),
            "bulk_spectral_radius_below_contour_required": True,
        },
        "hardy_energy_theorem": {
            "left_energy": (
                "E_B(r)^2=sum_(m>=0) r^(-2m)||U^* N^m Q U B||_S2^2/||B||_S2^2"
            ),
            "right_energy": (
                "E_C(r)^2=sum_(m>=0) r^(-2m)||C N_A^m Q_A||_S2^2/||C||_S2^2"
            ),
            "condition": "rho(N)<r<inf_(z in Gamma)|z|",
            "upper": (
                "sup_Gamma ||U^*(z-N)^-1QUB||_S2/||B||_S2 <= E_B(r)/sqrt(d_Gamma^2-r^2), and symmetrically on the right"
            ),
            "proof_mechanism": "Laurent series followed by weighted Cauchy-Schwarz",
        },
        "stein_certificate": {
            "controllability_equation": (
                "G=X X^*+r^(-2)N G N^*"
            ),
            "observability_equation": (
                "O=C^* C+r^(-2)N^* O N"
            ),
            "validated_supersolution": (
                "H-r^(-2)N H N^* >= X X^* implies G<=H and gives a trace upper"
            ),
            "global_inverse_or_global_power_contraction_required": False,
        },
        "sharp_spike_derivative": {
            "law": "||pi_sigma'||_2+||g_sigma'||_2=Theta(sigma^(-1))",
            "mechanism": (
                "each finite postcritical square-root spike has derivative majorant C(t+sigma)^(-3/2), while the endpoint profile gives the matching lower"
            ),
            "improvement_over_previous_coarse_envelope": "sigma^(-3/2) -> sigma^(-1)",
        },
        "outgoing_hilbert_schmidt_scale": {
            "law": "c h sigma^(-3/2)<=||B||_S2<=C h sigma^(-3/2)",
            "regime": "h/sigma sufficiently small",
            "upper_mechanism": "target-cell Poincare inequality",
            "lower_mechanism": (
                "interior Gaussian row derivative lower followed by the leading Haar Taylor coefficient"
            ),
        },
        "fine_side_residue_suppression": {
            "block_identity": (
                "P_cc B=r_c tensor ((conj(lambda)-D^*) l_d)^*"
            ),
            "detail_left_factor": "||l_d||=O(h sigma^(-1))",
            "coupling_lower": "||B||_S2>=c h sigma^(-3/2)",
            "conditional_normalized_residue_action": "O(sigma^(1/2))",
            "compressed_continuum_detail_estimate_proved": True,
            "dyadically_uniform_intrinsic_finite_factor_transfer_proved_here": False,
        },
        "global_contraction_no_go": {
            "deterministic_fact": (
                "the deterministic Koopman operator is an isometry on L2(mu_0), including the complement of the Perron/parity modes"
            ),
            "small_noise_consequence": (
                "for every fixed m, ||Q_sigma^o K_sigma^m Q_sigma^o|| -> 1 in the stationary Hilbert geometry"
            ),
            "ruled_out_route": (
                "a sigma-uniform fixed-step global contraction q<1 on the two-pole complement"
            ),
            "directional_gramian_route_ruled_out": False,
        },
        "conditional_hilbert_schmidt_closure": {
            "premises": [
                "dyadically uniform polylogarithmic left and right Hardy energies",
                "dyadically polylogarithmic intrinsic coarse parity projector norm",
                "dyadically polylogarithmic fine residue range actions, supplied in particular by a uniform intrinsic factor-detail transfer",
                "bulk spectral radius uniformly below one Hardy radius r<min_Gamma|z|",
            ],
            "conclusion": "F_(n,sigma)=O((log(1/sigma))^m) for some fixed m",
            "rh49_consequence": (
                "the quarter-power bridge then preserves the strict p>2 intrinsic-identification mesh range"
            ),
            "premises_proved_for_full_small_noise_family_here": False,
        },
        "floating_five_scale_audit": {
            "rows": merged_rows,
            "fits": pilot["fits"],
            "residue_fits": residue_fits,
            "noise_levels": len(rows),
            "largest_dimension": max(row["fine_dimension"] for row in rows),
            "maximum_power": pilot["maximum_power"],
            "probe_count": pilot["probe_count"],
            "hardy_radius": 0.85,
            "hardy_tail_validated": False,
            "hutchinson_values_are_validated_uppers": False,
        },
        "dependencies": dependencies,
        "limitations": [
            "The uniform small-noise Hardy-energy premise is not proved; the five-scale plateau is floating evidence.",
            "The archived Hardy sums stop at time 64 and do not carry an interval tail enclosure.",
            "Hutchinson trace estimates and binary64 eigendata are not validated norm uppers.",
            "A dyadically uniform transfer of the compressed-continuum O(sqrt(sigma)) residue estimate to the finite matrix's own left factors remains an explicit premise.",
            "A dyadically uniform intrinsic coarse parity projector bound remains an explicit premise of the full closure corollary.",
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
                "hardy_fits": pilot["fits"],
                "residue_fits": residue_fits,
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
