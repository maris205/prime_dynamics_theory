"""Compose the validated Perron and rank-two peripheral-complement ledgers."""

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
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH42 / "src"),
    str(RH43 / "src"),
]

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
from rank_two_complement import (  # noqa: E402
    combine_kernel_envelopes,
    perron_kernel_envelope,
    rank_two_cutoff_upper,
)
from rank_two_complement.bounds import (  # noqa: E402
    upper_add,
    upper_multiply,
)
from weighted_kernel import (  # noqa: E402
    factor_correction_ledger,
    weighted_lipschitz_upper,
    weighted_schur_transport,
)


MULTILEVEL_PATH = ROOT / "results" / "multilevel_perron_grushin.json"
OUTPUT = ROOT / "results" / "validated_rank_two_peripheral_complement.json"
SNAPSHOT_36 = (
    RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
)
SNAPSHOT_37 = (
    RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
)
RH40_CERTIFICATE_PATH = (
    RH40 / "results" / "weighted_riesz_projector_bridge_certificate.json"
)
RH42_UNIFORM_PATH = (
    RH42 / "results" / "uniform_euclidean_parity_certificate.json"
)
RH42_MIDPOINT_PATH = (
    RH42 / "results" / "euclidean_stored_to_midpoint_bridge.json"
)
RH43_CERTIFICATE_PATH = (
    RH43 / "results" / "validated_weighted_parity_kernel.json"
)
PERRON_CENTER = 1.0
PERRON_RADIUS = 0.05
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


def peripheral_tuple(
    data, prefix: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return (
        np.asarray(data[f"{prefix}_right_modes"][:, :2]),
        np.asarray(data[f"{prefix}_left_modes"][:, :2]),
        np.asarray(data[f"{prefix}_peripheral_values"][:2]),
    )


def outward_interval(
    lower: float, upper: float, error: float
) -> dict[str, float]:
    return {
        "lower": math.nextafter(max(0.0, float(lower) - error), -math.inf),
        "upper": math.nextafter(float(upper) + error, math.inf),
        "factor_to_spectral_frobenius_error_upper": error,
    }


def corrected_rank_two_haar(
    perron_errors: dict[str, float],
    parity_errors: dict[str, float],
) -> dict[str, object]:
    builder = load_rh40_builder()
    previous = ctx.prec
    ctx.prec = 224
    try:
        with np.load(SNAPSHOT_36) as first, np.load(SNAPSHOT_37) as second:
            levels = {
                "2048": peripheral_tuple(first, "coarse"),
                "4096": peripheral_tuple(first, "fine"),
                "8192": peripheral_tuple(second, "fine"),
            }
            first_blocks = builder.block_intervals(
                levels["2048"], levels["4096"]
            )
            second_blocks = builder.block_intervals(
                levels["4096"], levels["8192"]
            )
    finally:
        ctx.prec = previous

    total_errors = {
        dimension: upper_add(
            perron_errors[dimension], parity_errors[dimension]
        )
        for dimension in ("2048", "4096", "8192")
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
                math.sqrt(2.0),
                upper_add(total_errors["2048"], total_errors["4096"]),
            )
            if name == "coarse_consistency"
            else upper_multiply(math.sqrt(2.0), total_errors["4096"])
        )
        second_error = (
            upper_multiply(
                math.sqrt(2.0),
                upper_add(total_errors["4096"], total_errors["8192"]),
            )
            if name == "coarse_consistency"
            else upper_multiply(math.sqrt(2.0), total_errors["8192"])
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
            "rigorous_actual_stored_rank_two_quarter_half_mechanism"
            if mechanism_closed
            else "stored_rank_two_quarter_half_mechanism_not_closed"
        ),
        "arb_precision_bits": 224,
        "perron_factor_errors": perron_errors,
        "parity_factor_errors": parity_errors,
        "combined_factor_errors": total_errors,
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
    rh40 = load(RH40_CERTIFICATE_PATH)
    rh42 = load(RH42_UNIFORM_PATH)
    midpoint = load(RH42_MIDPOINT_PATH)
    parity = load(RH43_CERTIFICATE_PATH)
    if multilevel["status"] != (
        "rigorous_multilevel_exact_stored_euclidean_perron_factors"
    ):
        raise RuntimeError("multilevel stored Perron gate is not closed")
    if rh42["status"] != (
        "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
    ):
        raise RuntimeError("RH-42 Euclidean infrastructure is not closed")
    if parity["status"] != (
        "rigorous_intrinsic_continuum_parity_kernel_and_adaptive_deflation"
    ):
        raise RuntimeError("RH-43 intrinsic parity gate is not closed")

    perron_corrections = {}
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
        perron_corrections[dimension] = correction.as_dict()
    all_perron_factors = all(
        row["admissible"] for row in perron_corrections.values()
    )
    perron_errors = {
        dimension: float(row["weighted_term_error_upper"])
        for dimension, row in perron_corrections.items()
    }
    parity_errors = {
        dimension: float(row["weighted_term_error_upper"])
        for dimension, row in parity["stored_factor_validation"][
            "levels"
        ].items()
    }
    rank_two_haar = corrected_rank_two_haar(
        perron_errors, parity_errors
    )

    envelope = HilbertEnvelope(**rh42["hilbert_schmidt_envelope"])
    minimum_modulus = math.nextafter(
        PERRON_CENTER - PERRON_RADIUS, 0.0
    )
    maximum_modulus = math.nextafter(
        PERRON_CENTER + PERRON_RADIUS, math.inf
    )
    stored_row = multilevel["levels"]["4096"]
    stored_resolvent = float(
        stored_row["contour_ledger"]["contour_resolvent_upper"]
    )
    center_shift = abs(float(stored_row["center"]) - PERRON_CENTER)
    center_shift_transfer = neumann_transfer(
        stored_resolvent, center_shift
    )
    stored_to_midpoint = neumann_transfer(
        center_shift_transfer.transferred_resolvent_upper,
        float(midpoint["spectral_norm_upper"]),
    )
    midpoint_galerkin = midpoint_galerkin_defect(4096, envelope)
    midpoint_to_galerkin = neumann_transfer(
        stored_to_midpoint.transferred_resolvent_upper,
        midpoint_galerkin,
    )
    stored_weighted = weighted_lipschitz_upper(
        contour_radius=PERRON_RADIUS,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=(
            center_shift_transfer.transferred_resolvent_upper
        ),
        second_resolvent_upper=(
            stored_to_midpoint.transferred_resolvent_upper
        ),
        perturbation_upper=float(midpoint["spectral_norm_upper"]),
    )
    midpoint_weighted = weighted_lipschitz_upper(
        contour_radius=PERRON_RADIUS,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=(
            stored_to_midpoint.transferred_resolvent_upper
        ),
        second_resolvent_upper=(
            midpoint_to_galerkin.transferred_resolvent_upper
        ),
        perturbation_upper=midpoint_galerkin,
    )

    dyadic_steps = {}
    weighted_steps = {}
    current_dimension = 4096
    current_resolvent = midpoint_to_galerkin.transferred_resolvent_upper
    while current_dimension < FAMILY_THRESHOLD:
        blocks = hilbert_haar_bounds(current_dimension, envelope)
        step = hilbert_schur_step(
            current_resolvent, minimum_modulus, blocks
        )
        transport = weighted_schur_transport(
            coarse_dimension=current_dimension,
            contour_radius=PERRON_RADIUS,
            contour_maximum_modulus=maximum_modulus,
            coarse_resolvent_upper=current_resolvent,
            detail_to_coarse_upper=blocks.detail_to_coarse,
            coarse_to_detail_upper=blocks.coarse_to_detail,
            detail_resolvent_upper=step.detail_resolvent_upper,
            schur_inverse_upper=step.schur_inverse_upper,
        )
        fine_dimension = 2 * current_dimension
        name = f"{current_dimension}_to_{fine_dimension}"
        dyadic_steps[name] = {
            "blocks": blocks.as_dict(),
            "resolvent_step": step.as_dict(),
            "inside_count_after_transfer": (
                1 if step.count_transfers else None
            ),
        }
        weighted_steps[name] = transport.as_dict()
        current_dimension = fine_dimension
        current_resolvent = step.fine_resolvent_upper

    complement_blocks = hilbert_haar_bounds(FAMILY_THRESHOLD, envelope)
    complement_step = hilbert_schur_step(
        current_resolvent, minimum_modulus, complement_blocks
    )
    complement_weighted = weighted_schur_transport(
        coarse_dimension=FAMILY_THRESHOLD,
        contour_radius=PERRON_RADIUS,
        contour_maximum_modulus=maximum_modulus,
        coarse_resolvent_upper=current_resolvent,
        detail_to_coarse_upper=complement_blocks.detail_to_coarse,
        coarse_to_detail_upper=complement_blocks.coarse_to_detail,
        detail_resolvent_upper=complement_step.detail_resolvent_upper,
        schur_inverse_upper=complement_step.schur_inverse_upper,
    )
    continuum_resolvent = complement_step.fine_resolvent_upper
    perron_envelope = perron_kernel_envelope(
        contour_radius=PERRON_RADIUS,
        contour_resolvent_upper=continuum_resolvent,
        kernel_target_first_upper=envelope.target_first,
        kernel_target_second_upper=envelope.target_second,
        midpoint_dimension=FAMILY_THRESHOLD,
    )
    perron_construction_distance = upper_add(
        perron_corrections["4096"]["weighted_term_error_upper"],
        stored_weighted,
        midpoint_weighted,
        *(
            row["weighted_term_difference_upper"]
            for row in weighted_steps.values()
        ),
        complement_weighted.weighted_term_difference_upper,
    )
    perron_construction_hilbert_schmidt = upper_multiply(
        math.sqrt(2.0), perron_construction_distance
    )

    family_defect = math.nextafter(
        continuum_galerkin_defect(FAMILY_THRESHOLD, envelope)
        + midpoint_galerkin_defect(FAMILY_THRESHOLD, envelope),
        math.inf,
    )
    midpoint_family = neumann_transfer(
        continuum_resolvent, family_defect
    )
    normalization = discrete_normalization_defect(
        FAMILY_THRESHOLD,
        0.01,
        float(rh42["uniform_matrix_family"]["normalizer_lower"]),
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
    perron_weighted_cutoff = weighted_lipschitz_upper(
        contour_radius=PERRON_RADIUS,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=full_family.transferred_resolvent_upper,
        second_resolvent_upper=sparse_family.transferred_resolvent_upper,
        perturbation_upper=cutoff.spectral_norm_upper,
    )
    parity_weighted_cutoff = float(
        parity["improved_uniform_matrix_family"][
            "uniform_weighted_riesz_cutoff_upper"
        ]
    )
    rank_two_weighted_cutoff, rank_two_deflated_cutoff = (
        rank_two_cutoff_upper(
            cutoff.spectral_norm_upper,
            perron_weighted_cutoff,
            parity_weighted_cutoff,
        )
    )

    parity_kernel = parity["intrinsic_continuum_kernel"]
    rank_two_envelope = combine_kernel_envelopes(
        perron_envelope, parity_kernel["envelope"]
    )
    rank_two_operator_distance = upper_add(
        perron_construction_distance,
        float(parity_kernel["continuum_operator_distance_from_center_upper"]),
    )
    rank_two_kernel_distance = upper_add(
        perron_construction_hilbert_schmidt,
        float(parity_kernel["continuum_kernel_L2_distance_from_center_upper"]),
    )
    parity_contour = parity["contour"]
    contours_disjoint = bool(
        abs(PERRON_CENTER - float(parity_contour["center"]))
        > PERRON_RADIUS + float(parity_contour["radius"])
    )

    all_dyadic = all(
        row["resolvent_step"]["count_transfers"]
        for row in dyadic_steps.values()
    )
    all_gates = bool(
        all_perron_factors
        and rank_two_haar["all_ratio_targets_within_one_thousandth"]
        and center_shift_transfer.admissible
        and stored_to_midpoint.admissible
        and midpoint_to_galerkin.admissible
        and all_dyadic
        and complement_step.count_transfers
        and midpoint_family.admissible
        and full_family.admissible
        and sparse_family.admissible
        and contours_disjoint
    )
    status = (
        "rigorous_intrinsic_rank_two_peripheral_kernel_and_bulk_deflation"
        if all_gates
        else "intrinsic_rank_two_peripheral_gate_not_closed"
    )
    payload = {
        "status": status,
        "scope": (
            "intrinsic Perron-plus-parity weighted Riesz kernel, exact "
            "stored rank-two factors, and full/fixed/adaptive exact-real "
            "midpoint families at sigma=1/100"
        ),
        "evidence_level": (
            "analytic_markov_riesz_trace_factorization_plus_outward_arb_and_binary64_certificates"
        ),
        "contours": {
            "perron": {
                "center": PERRON_CENTER,
                "radius": PERRON_RADIUS,
                "minimum_modulus_lower": minimum_modulus,
                "maximum_modulus_upper": maximum_modulus,
                "inside_count": 1,
                "enclosed_eigenvalue": 1.0,
            },
            "parity": parity_contour,
            "disjoint": contours_disjoint,
            "union_inside_count": 2 if contours_disjoint else None,
        },
        "stored_perron_factor_validation": {
            "all_three_levels_are_actual_spectral_factors": (
                all_perron_factors
            ),
            "levels": perron_corrections,
        },
        "stored_rank_two_haar_law": rank_two_haar,
        "perron_continuum_contour": {
            "stored_dimension": 4096,
            "stored_center": float(stored_row["center"]),
            "exact_center": PERRON_CENTER,
            "center_shift_upper": center_shift,
            "center_shift_transfer": center_shift_transfer.as_dict(),
            "stored_to_exact_midpoint": {
                "spectral_norm_defect_upper": float(
                    midpoint["spectral_norm_upper"]
                ),
                "neumann_transfer": stored_to_midpoint.as_dict(),
            },
            "midpoint_to_galerkin": {
                "spectral_norm_defect_upper": midpoint_galerkin,
                "neumann_transfer": midpoint_to_galerkin.as_dict(),
            },
            "dyadic_hilbert_galerkin_steps": dyadic_steps,
            "infinite_complement": {
                "blocks": complement_blocks.as_dict(),
                "resolvent_step": complement_step.as_dict(),
                "weighted_riesz_transport": complement_weighted.as_dict(),
            },
            "continuum_inside_count": (
                1 if complement_step.count_transfers else None
            ),
            "continuum_eigenvalue_is_exactly_one_and_simple": True,
            "continuum_L2_resolvent_upper": continuum_resolvent,
        },
        "intrinsic_perron_kernel": {
            "definition": (
                "Q_+(K;Gamma_+)=(2 pi i)^-1 integral_Gamma+ "
                "z(z-K)^-1 dz"
            ),
            "exact_form": "q_+(x,y)=pi(y), K^* pi=pi, integral pi=1",
            "rank": 1,
            "real_smooth_strictly_positive_kernel": True,
            "source_independent": True,
            "envelope": perron_envelope.as_dict(),
            "piecewise_constant_4096_center": (
                "stored binary64 lambda_+ r_+ l_+^T/(l_+^T r_+) "
                "lifted to V_4096"
            ),
            "continuum_operator_distance_from_center_upper": (
                perron_construction_distance
            ),
            "continuum_kernel_L2_distance_from_center_upper": (
                perron_construction_hilbert_schmidt
            ),
        },
        "perron_weighted_transport_chain": {
            "stored_factor_to_exact_stored_weighted_term": (
                perron_corrections["4096"]["weighted_term_error_upper"]
            ),
            "stored_contour_center_shift_changes_weighted_term": False,
            "stored_to_exact_midpoint": stored_weighted,
            "midpoint_to_galerkin": midpoint_weighted,
            "dyadic_schur_steps": weighted_steps,
            "finite_rank_to_continuum_complement": (
                complement_weighted.weighted_term_difference_upper
            ),
            "total_operator_distance_upper": (
                perron_construction_distance
            ),
        },
        "intrinsic_rank_two_kernel": {
            "definition": "Q_per=Q_++Q_-",
            "kernel": "q_per(x,y)=pi(y)+q_-(x,y)",
            "rank": 2,
            "spectral_orthogonality": "Q_+ Q_-=Q_- Q_+=0",
            "real_smooth_gauge_free": True,
            "envelope": rank_two_envelope,
            "continuum_operator_distance_from_combined_4096_center_upper": (
                rank_two_operator_distance
            ),
            "continuum_kernel_L2_distance_from_combined_4096_center_upper": (
                rank_two_kernel_distance
            ),
        },
        "uniform_perron_and_rank_two_families": {
            "certified_threshold_dimension": FAMILY_THRESHOLD,
            "applies_to_every_larger_dimension": True,
            "perron_continuum_to_midpoint_defect_upper_at_threshold": (
                family_defect
            ),
            "perron_midpoint_transfer": midpoint_family.as_dict(),
            "normalization": normalization.as_dict(),
            "perron_full_transfer": full_family.as_dict(),
            "cutoff": cutoff.as_dict(),
            "perron_sparse_transfer": sparse_family.as_dict(),
            "uniform_perron_full_resolvent_upper": (
                full_family.transferred_resolvent_upper
            ),
            "uniform_perron_fixed_and_adaptive_sparse_resolvent_upper": (
                sparse_family.transferred_resolvent_upper
            ),
            "uniform_union_contour_resolvent_upper": max(
                sparse_family.transferred_resolvent_upper,
                float(
                    parity["improved_uniform_matrix_family"][
                        "uniform_fixed_and_adaptive_sparse_resolvent_upper"
                    ]
                ),
            ),
            "uniform_perron_weighted_riesz_cutoff_upper": (
                perron_weighted_cutoff
            ),
            "uniform_rank_two_weighted_riesz_cutoff_upper": (
                rank_two_weighted_cutoff
            ),
            "uniform_rank_two_intrinsically_deflated_cutoff_upper": (
                rank_two_deflated_cutoff
            ),
            "full_rank_two_weighted_term_to_continuum_midpoint_kernel_rate": (
                "O(n^-2)"
            ),
            "adaptive_rank_two_weighted_term_rate": (
                "O(n^-2 (log n)^-1/4)"
            ),
            "adaptive_bulk_operator_rate": (
                "O(n^-2 (log n)^-1/4) relative to the full bulk family"
            ),
            "fixed_eight_sigma_convergence_to_full_claimed": False,
        },
        "intrinsic_bulk_operator": {
            "definition": "B=K-Q_+-Q_-",
            "matrix_definition": "B_n=P_n-Q_+(P_n)-Q_-(P_n)",
            "perron_and_parity_eigenvalues_are_replaced_by_zero": True,
            "remaining_spectrum_is_unchanged_away_from_zero": True,
            "right_markov_constraint": "B 1=0",
            "left_stationary_constraint": "pi B=0",
            "power_identity": (
                "B^m=K^m-Q_+-lambda_-^(m-1) Q_- for every m>=1"
            ),
            "two_step_identity": "B^2=K^2-Q_+-lambda_- Q_-",
            "trace_identity": (
                "tr(B^m)=tr(K^m)-1-lambda_-^m for every m>=1"
            ),
            "fredholm_determinant_factorization": (
                "det(I-zK)=(1-z)(1-z lambda_-) det(I-zB)"
            ),
            "factorization_is_structural_not_arithmetic": True,
        },
        "analytic_haar_limits": {
            "perron_source_independence": (
                "q_+(x,y)=pi(y), so its C and D Haar blocks vanish exactly"
            ),
            "rank_two_coarse_consistency": (
                "h^-2 E_h -> ((q_per)_xx+(q_per)_yy)/32"
            ),
            "rank_two_coarse_to_detail": (
                "h^-1 C_h -> (q_per)_x/4=(q_-)_x/4"
            ),
            "rank_two_detail_to_coarse": (
                "h^-1 B_h -> (q_per)_y/4"
            ),
            "rank_two_detail_block": (
                "h^-2 D_h -> (q_per)_xy/16=(q_-)_xy/16"
            ),
            "ratio_consequence": (
                "nonzero leading tensors give ratios 1/4,1/2,1/2,1/4"
            ),
        },
        "rh40_completion_status": {
            "previous_status": rh40["status"],
            "perron_analytic_premise_closed": True,
            "parity_analytic_premise_closed_by_rh43": True,
            "uniform_union_contour_closed": all_gates,
            "stored_rank_two_spectral_status_closed_at_2048_4096_8192": (
                all_perron_factors
                and parity["stored_factor_validation"][
                    "all_three_levels_are_actual_spectral_factors"
                ]
            ),
        },
        "dependencies": {
            "multilevel_perron_grushin_certificate": repository_entry(
                MULTILEVEL_PATH
            ),
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
            "rh40_projector_builder": repository_entry(
                RH40 / "experiments" / "build_projector_certificate.py"
            ),
            "rh42_uniform_euclidean_certificate": repository_entry(
                RH42_UNIFORM_PATH
            ),
            "rh42_midpoint_bridge": repository_entry(RH42_MIDPOINT_PATH),
            "rh43_intrinsic_parity_certificate": repository_entry(
                RH43_CERTIFICATE_PATH
            ),
            "rh43_weighted_kernel_source": repository_entry(
                RH43 / "src" / "weighted_kernel" / "bounds.py"
            ),
        },
        "limitations": [
            "The theorem is at the fixed positive noise width sigma=1/100.",
            "The intrinsic Perron and rank-two kernels are enclosed in Hilbert-Schmidt norms; no pointwise interval heat map of the exact continuum kernels is claimed.",
            "The explicit all-dimension theorem concerns exact-real Gaussian formulas, while the three stored Perron and parity factor certificates concern their archived binary64 matrices.",
            "The fixed eight-sigma family is uniformly stable but is not claimed to converge to the full kernel in row norm.",
            "The trace and Fredholm-determinant identities remove only the two validated peripheral factors; they are structural operator factorizations, not an arithmetic trace formula or prime-power identity.",
            "No zero-noise limit, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, or Riemann-hypothesis claim is made.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not all_gates:
        raise RuntimeError("the validated rank-two peripheral gates failed")


if __name__ == "__main__":
    main()
