"""Compose the RH-52 weak-factor and residue-transfer ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH51 = PAPERS / "RH-51-cyclic-rank-growing-horizon-stein"
PILOT = ROOT / "results" / "factor_transfer_pilot.json"
OUTPUT = ROOT / "results" / "factor_transfer_certificate.json"


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


def branch(row, section: str, mode: str):
    return next(item for item in row[section] if item["mode"] == mode)


def main() -> None:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    rows = pilot["rows"]
    merged = []
    for row in rows:
        perron = branch(row, "fine_factor_branches", "perron")
        parity = branch(row, "fine_factor_branches", "parity")
        adjacent_parity = branch(
            row, "adjacent_factor_transfer", "parity"
        )
        fine_perron = branch(
            row, "fine_left_residue_actions", "perron"
        )
        fine_parity = branch(
            row, "fine_left_residue_actions", "parity"
        )
        right_perron = branch(
            row, "coarse_right_residue_actions", "perron"
        )
        right_parity = branch(
            row, "coarse_right_residue_actions", "parity"
        )
        right_image = branch(
            row, "coarse_right_image_scales", "parity"
        )
        merged.append(
            {
                "sigma": float(row["sigma"]),
                "fine_dimension": int(row["fine_dimension"]),
                "coarse_dimension": int(row["coarse_dimension"]),
                "coarse_cell_width_over_sigma": float(
                    row["coarse_cell_width_over_sigma"]
                ),
                "B_scale_constant": float(
                    row[
                        "B_hilbert_schmidt_over_h_sigma_minus_three_halves"
                    ]
                ),
                "C_scale_constant": float(
                    row[
                        "C_hilbert_schmidt_over_h_sigma_minus_three_halves"
                    ]
                ),
                "perron_weak_condition_product": float(
                    perron["weak_condition_product"]
                ),
                "parity_weak_condition_product": float(
                    parity["weak_condition_product"]
                ),
                "perron_projector": float(
                    perron["projector_frobenius"]
                ),
                "parity_projector": float(
                    parity["projector_frobenius"]
                ),
                "perron_projector_square_over_log": float(
                    perron["projector_square_over_log"]
                ),
                "parity_projector_square_over_log": float(
                    parity["projector_square_over_log"]
                ),
                "perron_sharp_detail_ratio": float(
                    perron[
                        "left_detail_over_sharp_h_sigma_inverse"
                    ]
                ),
                "parity_sharp_detail_ratio": float(
                    parity[
                        "left_detail_over_sharp_h_sigma_inverse"
                    ]
                ),
                "perron_weak_detail_ratio": float(
                    perron[
                        "left_detail_over_weak_h_sigma_minus_three_halves"
                    ]
                ),
                "parity_weak_detail_ratio": float(
                    parity[
                        "left_detail_over_weak_h_sigma_minus_three_halves"
                    ]
                ),
                "fine_perron_residue": float(
                    fine_perron[
                        "left_residue_action_over_B_hilbert_schmidt"
                    ]
                ),
                "fine_parity_residue": float(
                    fine_parity[
                        "left_residue_action_over_B_hilbert_schmidt"
                    ]
                ),
                "right_perron_residue": float(
                    right_perron[
                        "right_residue_action_over_C_hilbert_schmidt"
                    ]
                ),
                "right_parity_residue": float(
                    right_parity[
                        "right_residue_action_over_C_hilbert_schmidt"
                    ]
                ),
                "right_parity_image_scale_ratio": float(
                    right_image[
                        "C_right_image_over_h_sigma_inverse_linf"
                    ]
                ),
                "parity_adjacent_left_l1_error": float(
                    adjacent_parity[
                        "left_l1_normalized_adjacent_error"
                    ]
                ),
                "parity_adjacent_right_linf_error": float(
                    adjacent_parity[
                        "right_linf_normalized_adjacent_error"
                    ]
                ),
                "parity_adjacent_eigenvalue_error": float(
                    adjacent_parity["eigenvalue_adjacent_error"]
                ),
                "parity_adjacent_projector_relative_defect": float(
                    adjacent_parity[
                        "projector_relative_adjacent_defect"
                    ]
                ),
            }
        )

    payload = {
        "status": (
            "rigorous_weak_factor_direct_residue_closure_with_sharp_detail_barrier"
        ),
        "scope": (
            "finite Perron/parity residue actions on the adjacent Haar coupling ranges of the small-noise folded-Gaussian operator"
        ),
        "evidence_level": {
            "analytic": (
                "uniform weak Ulam peripheral factors under the established strong-weak stability framework, direct L1-to-L2 and Linfinity-to-L2 kernel-detail bounds, two-sided B/C Hilbert-Schmidt coupling scales, O(1) normalized residue actions, and a sharp weak-information half-power barrier"
            ),
            "numerical": (
                "binary64 five-scale sparse intrinsic factor, Haar-detail, adjacent-transfer, and direct residue audit through dimension 40960; not interval validated"
            ),
        },
        "weak_finite_factor_theorem": {
            "schedule": "h=o(sigma^2), equivalently n sigma^2 -> infinity",
            "density_extension": (
                "the finite density matrix is the restriction of E_n P_sigma to Ran(E_n)"
            ),
            "conclusion": (
                "the two finite peripheral branches are simple and can be normalized with |lambda_-|>=1/2 and uniformly bounded right Linfinity and left L1 factors"
            ),
            "mechanism": (
                "uniform tower/spike Lasota-Yorke estimates, variation-diminishing cell averaging, weak Ulam convergence, and Keller-Liverani stability"
            ),
        },
        "direct_kernel_bounds": {
            "target_detail": (
                "||(E_2n-E_n) P_sigma||_(L1->L2) <= C h sigma^(-3/2)"
            ),
            "source_detail": (
                "||(E_2n-E_n) K_sigma||_(Linfinity->L2) <= C h sigma^(-1)"
            ),
            "density_smoothing": (
                "||P_sigma||_(L1->L2) <= C sigma^(-1/2)"
            ),
            "coupling_scales": (
                "c h sigma^(-3/2) <= ||B||_S2,||C||_S2 <= C h sigma^(-3/2)"
            ),
        },
        "direct_residue_closure": {
            "fine_perron_and_parity": (
                "||U^* P_(f,s) U B||_S2/||B||_S2=O(1), s=+,-"
            ),
            "coarse_perron": "C P_(c,+)=0 exactly",
            "coarse_parity": (
                "||C P_(c,-)||_S2/||C||_S2=O(1)"
            ),
            "sharp_finite_detail_transfer_required": False,
            "finite_projector_polylog_upper_required": False,
        },
        "sharp_detail_barrier": {
            "operator_law": (
                "||(E_2n-E_n) P_sigma||_(L1->L2)=Theta(h sigma^(-3/2)) when h/sigma is small"
            ),
            "consequence": (
                "uniform left L1 information alone cannot prove the sharper O(h sigma^(-1)) intrinsic detail estimate"
            ),
            "physical_sharp_transfer_proved_here": False,
            "program_impact": (
                "the sharp O(sqrt(sigma)) fine residue law remains optional because the weaker direct O(1) range-action theorem already closes the RH-50 residue premise"
            ),
        },
        "floating_five_scale_audit": {
            "rows": merged,
            "noise_levels": len(merged),
            "largest_dimension": max(
                row["fine_dimension"] for row in merged
            ),
            "fine_resolution_target": pilot["fine_resolution_target"],
            "fits": pilot["fits"],
            "maximum_parity_weak_condition_product": max(
                row["parity_weak_condition_product"] for row in merged
            ),
            "maximum_parity_sharp_detail_ratio": max(
                row["parity_sharp_detail_ratio"] for row in merged
            ),
            "maximum_parity_adjacent_left_l1_error": max(
                row["parity_adjacent_left_l1_error"] for row in merged
            ),
            "maximum_parity_adjacent_right_linf_error": max(
                row["parity_adjacent_right_linf_error"] for row in merged
            ),
            "maximum_parity_adjacent_projector_relative_defect": max(
                row["parity_adjacent_projector_relative_defect"]
                for row in merged
            ),
            "interval_validated": False,
        },
        "program_conclusion": {
            "stage_A2_sufficient_residue_gate_closed": True,
            "stage_A2_original_sharp_sqrt_sigma_target_closed": False,
            "remaining_small_noise_gates": [
                "A1: analytic growing-horizon Hardy/Stein trace budget",
                "A3: deterministic or interval infinite Hardy tail and sparse-cutoff transfer",
            ],
            "next_scheduled_paper": (
                "RH-53 infinite Hardy-tail and sparse-cutoff validation"
            ),
        },
        "dependencies": {
            "rh14_boundary_layer": entry(RH14 / "main.tex"),
            "rh47_log_conditioning": entry(RH47 / "main.tex"),
            "rh49_directional_resolvent": entry(RH49 / "main.tex"),
            "rh50_hardy_stein": entry(RH50 / "main.tex"),
            "rh51_structured_stein": entry(RH51 / "main.tex"),
            "local_pilot": entry(PILOT, local=True),
        },
        "limitations": [
            "The sharper O(h sigma^(-1)) intrinsic finite left-detail theorem and O(sqrt(sigma)) fine residue law are not proved; only the sufficient direct O(1) residue bound is analytic.",
            "The uniform weak finite-factor theorem uses the tower/spike strong-weak Ulam stability framework and does not provide an explicit interval constant at the stored matrices.",
            "The five-scale audit uses fixed N sigma=20.48 and therefore is not a numerical realization of the stronger n sigma^2 to infinity proof schedule.",
            "All finite eigendata, detail norms, and adjacent defects are binary64 and are not interval enclosures.",
            "Stage A1 Hardy-energy control and Stage A3 infinite-tail/cutoff validation remain open.",
            "No arithmetic trace formula, prime-power identity, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, Riemann-hypothesis proof, or twin-prime conclusion is claimed.",
            "The independent TPC twin-prime/correlation program is not an assumption in this RH result.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "residue_fits": {
                    key: pilot["fits"][key]
                    for key in (
                        "fine_perron_residue",
                        "fine_parity_residue",
                        "right_parity_residue",
                    )
                },
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
