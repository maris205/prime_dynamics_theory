"""Compose the intrinsic parity-kernel, Schur, factor, and cutoff ledgers."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

from flint import ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
sys.path[:0] = [str(ROOT / "src"), str(RH42 / "src")]

from euclidean_contour import (  # noqa: E402
    HilbertEnvelope,
    continuum_galerkin_defect,
    discrete_normalization_defect,
    hilbert_haar_bounds,
    hilbert_schur_step,
    midpoint_galerkin_defect,
    neumann_transfer,
    relaxed_cutoff_defect,
)
from weighted_kernel import (  # noqa: E402
    deflated_cutoff_upper,
    factor_correction_ledger,
    intrinsic_kernel_envelope,
    weighted_lipschitz_upper,
    weighted_schur_transport,
)
from weighted_kernel.bounds import upper_add, upper_multiply  # noqa: E402


MULTILEVEL_PATH = ROOT / "results" / "multilevel_euclidean_grushin.json"
OUTPUT = ROOT / "results" / "validated_weighted_parity_kernel.json"
RH42_UNIFORM_PATH = (
    RH42 / "results" / "uniform_euclidean_parity_certificate.json"
)
RH42_HILBERT_PATH = (
    RH42 / "results" / "hilbert_schmidt_envelope_certificate.json"
)
RH40_CERTIFICATE_PATH = (
    RH40 / "results" / "weighted_riesz_projector_bridge_certificate.json"
)
SNAPSHOT_36 = (
    RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
)
SNAPSHOT_37 = (
    RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
)
FAMILY_THRESHOLD = 65536


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def load_rh40_builder():
    path = RH40 / "experiments" / "build_projector_certificate.py"
    specification = importlib.util.spec_from_file_location(
        "rh40_projector_builder", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the RH-40 projector builder")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def parity_tuple(data, prefix: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return (
        np.asarray(data[f"{prefix}_right_modes"][:, 1:2]),
        np.asarray(data[f"{prefix}_left_modes"][:, 1:2]),
        np.asarray(data[f"{prefix}_peripheral_values"][1:2]),
    )


def outward_interval(
    lower: float, upper: float, error: float
) -> dict[str, float]:
    return {
        "lower": math.nextafter(max(0.0, float(lower) - error), -math.inf),
        "upper": math.nextafter(float(upper) + error, math.inf),
        "factor_to_spectral_frobenius_error_upper": error,
    }


def corrected_parity_haar(
    corrections: dict[str, dict[str, object]]
) -> dict[str, object]:
    builder = load_rh40_builder()
    previous = ctx.prec
    ctx.prec = 224
    try:
        with np.load(SNAPSHOT_36) as first, np.load(SNAPSHOT_37) as second:
            levels = {
                "2048": parity_tuple(first, "coarse"),
                "4096": parity_tuple(first, "fine"),
                "8192": parity_tuple(second, "fine"),
            }
            first_blocks = builder.block_intervals(
                levels["2048"], levels["4096"]
            )
            second_blocks = builder.block_intervals(
                levels["4096"], levels["8192"]
            )
    finally:
        ctx.prec = previous

    errors = {
        dimension: float(row["weighted_term_error_upper"])
        for dimension, row in corrections.items()
    }
    corrected_levels: dict[str, dict[str, dict[str, float]]] = {
        "2048_to_4096": {},
        "4096_to_8192": {},
    }
    ratios = {}
    targets = {
        "coarse_consistency": 0.25,
        "coarse_to_detail": 0.5,
        "detail_to_coarse": 0.5,
        "detail_block": 0.25,
    }
    for name in first_blocks:
        first_error = (
            upper_multiply(
                math.sqrt(2.0), errors["2048"] + errors["4096"]
            )
            if name == "coarse_consistency"
            else upper_multiply(math.sqrt(2.0), errors["4096"])
        )
        second_error = (
            upper_multiply(
                math.sqrt(2.0), errors["4096"] + errors["8192"]
            )
            if name == "coarse_consistency"
            else upper_multiply(math.sqrt(2.0), errors["8192"])
        )
        first_interval = outward_interval(
            first_blocks[name]["frobenius_lower"],
            first_blocks[name]["frobenius_upper"],
            first_error,
        )
        second_interval = outward_interval(
            second_blocks[name]["frobenius_lower"],
            second_blocks[name]["frobenius_upper"],
            second_error,
        )
        corrected_levels["2048_to_4096"][name] = first_interval
        corrected_levels["4096_to_8192"][name] = second_interval
        ratio_lower = math.nextafter(
            second_interval["lower"] / first_interval["upper"],
            -math.inf,
        )
        ratio_upper = math.nextafter(
            second_interval["upper"] / first_interval["lower"],
            math.inf,
        )
        target = targets[name]
        ratios[name] = {
            "lower": ratio_lower,
            "upper": ratio_upper,
            "asymptotic_target": target,
            "maximum_target_deviation": max(
                abs(ratio_lower - target), abs(ratio_upper - target)
            ),
        }
    mechanism_closed = all(
        row["maximum_target_deviation"] < 1.0e-3
        for row in ratios.values()
    )
    return {
        "status": (
            "rigorous_actual_stored_parity_quarter_half_mechanism"
            if mechanism_closed
            else "stored_parity_quarter_half_mechanism_not_closed"
        ),
        "arb_precision_bits": 224,
        "exact_factor_frobenius_blocks": {
            "2048_to_4096": first_blocks,
            "4096_to_8192": second_blocks,
        },
        "actual_spectral_frobenius_intervals": corrected_levels,
        "actual_spectral_ratios": ratios,
        "all_ratio_targets_within_one_thousandth": mechanism_closed,
    }


def main() -> None:
    multilevel = load(MULTILEVEL_PATH)
    rh42 = load(RH42_UNIFORM_PATH)
    rh40 = load(RH40_CERTIFICATE_PATH)
    if multilevel["status"] != (
        "rigorous_multilevel_exact_stored_euclidean_parity_factors"
    ):
        raise RuntimeError("multilevel stored-factor gate is not closed")
    if rh42["status"] != (
        "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
    ):
        raise RuntimeError("RH-42 Euclidean contour gate is not closed")

    center = float(rh42["contour"]["center"])
    radius = float(rh42["contour"]["radius"])
    minimum_modulus = float(rh42["contour"]["minimum_modulus_lower"])
    maximum_modulus = float(rh42["contour"]["maximum_modulus_upper"])

    factor_corrections = {}
    for dimension, row in multilevel["levels"].items():
        correction = factor_correction_ledger(
            contour_radius=float(row["radius"]),
            contour_maximum_modulus=math.nextafter(
                abs(float(row["center"])) + float(row["radius"]),
                math.inf,
            ),
            contour_resolvent_upper=float(
                row["contour_ledger"]["contour_resolvent_upper"]
            ),
            approximate_eigenvalue_modulus=abs(float(row["center"])),
            right_norm_upper=float(row["right_mode_two_upper"]),
            left_norm_upper=float(row["left_mode_two_upper"]),
            right_residual_upper=float(row["right_residual_two_upper"]),
            left_residual_upper=float(row["left_residual_two_upper"]),
            gram_lower=float(row["left_right_gram_lower"]),
            gram_upper=float(row["left_right_gram_upper"]),
            grushin_scalar_error_upper=float(
                row["contour_ledger"]["scalar_error_upper"]
            ),
        )
        factor_corrections[dimension] = correction.as_dict()
    all_factors = all(
        row["admissible"] for row in factor_corrections.values()
    )
    parity_haar = corrected_parity_haar(factor_corrections)

    envelope = HilbertEnvelope(**rh42["hilbert_schmidt_envelope"])
    coarse_resolvent = float(
        rh42["galerkin_to_continuum_L2"][
            "galerkin_matrix_resolvent_upper"
        ]
    )
    complement_blocks = hilbert_haar_bounds(FAMILY_THRESHOLD, envelope)
    complement_step = hilbert_schur_step(
        coarse_resolvent, minimum_modulus, complement_blocks
    )
    complement_weighted = weighted_schur_transport(
        coarse_dimension=FAMILY_THRESHOLD,
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        coarse_resolvent_upper=coarse_resolvent,
        detail_to_coarse_upper=complement_blocks.detail_to_coarse,
        coarse_to_detail_upper=complement_blocks.coarse_to_detail,
        detail_resolvent_upper=complement_step.detail_resolvent_upper,
        schur_inverse_upper=complement_step.schur_inverse_upper,
    )

    continuum_resolvent = complement_step.fine_resolvent_upper
    family_defect = math.nextafter(
        continuum_galerkin_defect(FAMILY_THRESHOLD, envelope)
        + midpoint_galerkin_defect(FAMILY_THRESHOLD, envelope),
        math.inf,
    )
    midpoint_family = neumann_transfer(
        continuum_resolvent, family_defect
    )
    normalizer_lower = float(
        rh42["uniform_matrix_family"]["normalizer_lower"]
    )
    normalization = discrete_normalization_defect(
        FAMILY_THRESHOLD,
        0.01,
        normalizer_lower,
        envelope.kernel,
        midpoint_galerkin_defect(FAMILY_THRESHOLD, envelope),
    )
    full_family = neumann_transfer(
        midpoint_family.transferred_resolvent_upper,
        normalization.spectral_norm_defect_upper,
    )
    cutoff = relaxed_cutoff_defect(FAMILY_THRESHOLD, 0.01, 8.0)
    sparse_family = neumann_transfer(
        full_family.transferred_resolvent_upper,
        cutoff.spectral_norm_upper,
    )
    weighted_cutoff = weighted_lipschitz_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=full_family.transferred_resolvent_upper,
        second_resolvent_upper=sparse_family.transferred_resolvent_upper,
        perturbation_upper=cutoff.spectral_norm_upper,
    )
    deflated_cutoff = deflated_cutoff_upper(
        cutoff.spectral_norm_upper, weighted_cutoff
    )

    kernel_envelope = intrinsic_kernel_envelope(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        contour_minimum_modulus=minimum_modulus,
        contour_resolvent_upper=continuum_resolvent,
        kernel_source_first_upper=envelope.source_first,
        kernel_target_first_upper=envelope.target_first,
        kernel_source_second_upper=envelope.source_second,
        kernel_source_target_upper=envelope.source_target,
        kernel_target_second_upper=envelope.target_second,
        midpoint_dimension=FAMILY_THRESHOLD,
    )

    stored_to_midpoint = weighted_lipschitz_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=float(
            rh42["stored_euclidean_theorem"]["contour_resolvent_upper"]
        ),
        second_resolvent_upper=float(
            rh42["stored_to_exact_midpoint_4096"]["neumann_transfer"][
                "transferred_resolvent_upper"
            ]
        ),
        perturbation_upper=float(
            rh42["stored_to_exact_midpoint_4096"][
                "spectral_norm_defect_upper"
            ]
        ),
    )
    midpoint_to_galerkin = weighted_lipschitz_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=float(
            rh42["stored_to_exact_midpoint_4096"]["neumann_transfer"][
                "transferred_resolvent_upper"
            ]
        ),
        second_resolvent_upper=float(
            rh42["midpoint_to_galerkin_4096"]["neumann_transfer"][
                "transferred_resolvent_upper"
            ]
        ),
        perturbation_upper=float(
            rh42["midpoint_to_galerkin_4096"][
                "spectral_norm_defect_upper"
            ]
        ),
    )
    ordered_steps = (
        "4096_to_8192",
        "8192_to_16384",
        "16384_to_32768",
        "32768_to_65536",
    )
    weighted_steps = {}
    current_resolvent = float(
        rh42["midpoint_to_galerkin_4096"]["neumann_transfer"][
            "transferred_resolvent_upper"
        ]
    )
    for name in ordered_steps:
        row = rh42["dyadic_hilbert_galerkin_steps"][name]
        transport = weighted_schur_transport(
            coarse_dimension=int(row["blocks"]["coarse_dimension"]),
            contour_radius=radius,
            contour_maximum_modulus=maximum_modulus,
            coarse_resolvent_upper=current_resolvent,
            detail_to_coarse_upper=float(
                row["blocks"]["detail_to_coarse"]
            ),
            coarse_to_detail_upper=float(
                row["blocks"]["coarse_to_detail"]
            ),
            detail_resolvent_upper=float(
                row["resolvent_step"]["detail_resolvent_upper"]
            ),
            schur_inverse_upper=float(
                row["resolvent_step"]["schur_inverse_upper"]
            ),
        )
        weighted_steps[name] = transport.as_dict()
        current_resolvent = float(
            row["resolvent_step"]["fine_resolvent_upper"]
        )
    construction_distance = upper_add(
        float(factor_corrections["4096"]["weighted_term_error_upper"]),
        stored_to_midpoint,
        midpoint_to_galerkin,
        *(row["weighted_term_difference_upper"] for row in weighted_steps.values()),
        complement_weighted.weighted_term_difference_upper,
    )
    construction_hilbert_schmidt = upper_multiply(
        math.sqrt(2.0), construction_distance
    )

    all_gates = bool(
        all_factors
        and parity_haar["all_ratio_targets_within_one_thousandth"]
        and complement_step.count_transfers
        and midpoint_family.admissible
        and full_family.admissible
        and sparse_family.admissible
    )
    status = (
        "rigorous_intrinsic_continuum_parity_kernel_and_adaptive_deflation"
        if all_gates
        else "intrinsic_continuum_parity_kernel_gate_not_closed"
    )
    payload = {
        "status": status,
        "scope": (
            "intrinsic negative-parity weighted Riesz kernel, exact stored "
            "parity factors, and full/fixed/adaptive exact-real midpoint "
            "families at sigma=1/100"
        ),
        "evidence_level": (
            "analytic_weighted_riesz_and_haar_theorems_plus_outward_arb_and_binary64_certificates"
        ),
        "contour": rh42["contour"],
        "stored_factor_validation": {
            "all_three_levels_are_actual_spectral_factors": all_factors,
            "levels": factor_corrections,
        },
        "stored_parity_haar_law": parity_haar,
        "continuum_complement_schur": {
            "coarse_dimension": FAMILY_THRESHOLD,
            "blocks": complement_blocks.as_dict(),
            "resolvent_step": complement_step.as_dict(),
            "weighted_riesz_transport": complement_weighted.as_dict(),
            "continuum_inside_count": 1 if complement_step.count_transfers else None,
            "improved_continuum_L2_resolvent_upper": continuum_resolvent,
        },
        "intrinsic_continuum_kernel": {
            "definition": (
                "Q_-(K;Gamma)=(2 pi i)^-1 integral_Gamma z(z-K)^-1 dz"
            ),
            "rank": 1,
            "real_smooth_kernel": True,
            "kernel_lower_norm_from_eigenvalue_modulus": minimum_modulus,
            "envelope": kernel_envelope.as_dict(),
            "piecewise_constant_4096_center": (
                "stored binary64 lambda_0 r_0 l_0^T/(l_0^T r_0) lifted to V_4096"
            ),
            "continuum_operator_distance_from_center_upper": construction_distance,
            "continuum_kernel_L2_distance_from_center_upper": (
                construction_hilbert_schmidt
            ),
        },
        "weighted_transport_chain": {
            "stored_factor_to_exact_stored_weighted_term": factor_corrections[
                "4096"
            ]["weighted_term_error_upper"],
            "stored_to_exact_midpoint": stored_to_midpoint,
            "midpoint_to_galerkin": midpoint_to_galerkin,
            "dyadic_schur_steps": weighted_steps,
            "finite_rank_to_continuum_complement": (
                complement_weighted.weighted_term_difference_upper
            ),
            "total_operator_distance_upper": construction_distance,
        },
        "improved_uniform_matrix_family": {
            "certified_threshold_dimension": FAMILY_THRESHOLD,
            "applies_to_every_larger_dimension": True,
            "continuum_to_midpoint_defect_upper_at_threshold": family_defect,
            "midpoint_transfer": midpoint_family.as_dict(),
            "normalization": normalization.as_dict(),
            "full_transfer": full_family.as_dict(),
            "cutoff": cutoff.as_dict(),
            "sparse_transfer": sparse_family.as_dict(),
            "uniform_full_resolvent_upper": (
                full_family.transferred_resolvent_upper
            ),
            "uniform_fixed_and_adaptive_sparse_resolvent_upper": (
                sparse_family.transferred_resolvent_upper
            ),
            "uniform_weighted_riesz_cutoff_upper": weighted_cutoff,
            "uniform_intrinsically_deflated_cutoff_upper": deflated_cutoff,
            "full_weighted_term_to_continuum_midpoint_kernel_rate": "O(n^-2)",
            "adaptive_weighted_term_to_continuum_midpoint_kernel_rate": (
                "O(n^-2 (log n)^-1/4)"
            ),
            "adaptive_deflated_operator_rate": (
                "O(n^-2 (log n)^-1/4) relative to the full deflated family"
            ),
            "fixed_eight_sigma_convergence_to_full_claimed": False,
        },
        "intrinsic_deflation": {
            "continuum_operator": "K_perp=K-Q_-(K;Gamma)",
            "parity_eigenvalue_is_replaced_by_zero": True,
            "remaining_spectrum_is_unchanged_away_from_zero": True,
            "matrix_operator": "P_n_perp=P_n-Q_-(P_n;Gamma)",
        },
        "analytic_haar_limits": {
            "coarse_consistency": (
                "h^-2 E_h -> (q_xx+q_yy)/32 in Hilbert-Schmidt sampling"
            ),
            "coarse_to_detail": "h^-1 C_h -> q_x/4",
            "detail_to_coarse": "h^-1 B_h -> q_y/4",
            "detail_block": "h^-2 D_h -> q_xy/16",
            "ratio_consequence": (
                "nonzero leading tensors give ratios 1/4,1/2,1/2,1/4"
            ),
        },
        "rh40_condition_status": {
            "previous_status": rh40["status"],
            "simple_isolated_continuum_parity_premise_closed": True,
            "uniform_euclidean_cutoff_premise_closed": True,
            "stored_factor_spectral_status_closed_at_2048_4096_8192": (
                all_factors
            ),
        },
        "dependencies": {
            "multilevel_grushin_certificate": repository_entry(MULTILEVEL_PATH),
            "rh36_factor_snapshot": repository_entry(SNAPSHOT_36),
            "rh37_factor_snapshot": repository_entry(SNAPSHOT_37),
            "rh39_cutoff_certificate": repository_entry(
                RH39
                / "results"
                / "uniform_gaussian_cutoff_bridge_certificate.json"
            ),
            "rh40_weighted_riesz_certificate": repository_entry(
                RH40_CERTIFICATE_PATH
            ),
            "rh40_weighted_riesz_manuscript": repository_entry(
                RH40 / "main.tex"
            ),
            "rh40_projector_builder": repository_entry(
                RH40 / "experiments" / "build_projector_certificate.py"
            ),
            "rh42_uniform_euclidean_certificate": repository_entry(
                RH42_UNIFORM_PATH
            ),
            "rh42_hilbert_envelope": repository_entry(RH42_HILBERT_PATH),
            "rh42_hilbert_source": repository_entry(
                RH42 / "src" / "euclidean_contour" / "hilbert.py"
            ),
        },
        "limitations": [
            "The theorem is at the fixed positive noise width sigma=1/100.",
            "The intrinsic kernel is enclosed in L2 and derivative Hilbert-Schmidt norms; no pointwise interval plot of the exact continuum kernel is claimed.",
            "The explicit all-dimension theorem concerns exact-real Gaussian formulas, while the three stored factor certificates concern their archived binary64 matrices.",
            "The Perron weighted term is not included in the validated rank-one construction; rank-two deflation is a later step.",
            "The fixed eight-sigma family is uniformly stable but is not claimed to converge to the full kernel in row norm.",
            "No zero-noise limit, arithmetic trace formula, zeta-zero identification, self-adjoint Hilbert-Polya operator, or Riemann-hypothesis claim is made.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not all_gates:
        raise RuntimeError("the validated weighted parity-kernel gates failed")


if __name__ == "__main__":
    main()
