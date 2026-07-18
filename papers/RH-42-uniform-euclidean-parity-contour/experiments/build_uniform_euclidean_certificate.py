"""Compose the Euclidean Grushin, Hilbert Galerkin, and sparse cutoff gates."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH40 = PAPERS / "RH-40-weighted-riesz-projector-bridge"
RH41 = PAPERS / "RH-41-validated-parity-continuum-contour"
sys.path.insert(0, str(ROOT / "src"))

from euclidean_contour import (  # noqa: E402
    HilbertEnvelope,
    adaptive_multiple,
    continuum_galerkin_defect,
    discrete_normalization_defect,
    hilbert_haar_bounds,
    hilbert_schur_step,
    midpoint_galerkin_defect,
    neumann_transfer,
    relaxed_cutoff_defect,
    weighted_riesz_perturbation_upper,
)


GRUSHIN_PATH = (
    ROOT / "results" / "euclidean_grushin_contour_certificate.json"
)
MIDPOINT_PATH = (
    ROOT / "results" / "euclidean_stored_to_midpoint_bridge.json"
)
HILBERT_PATH = (
    ROOT / "results" / "hilbert_schmidt_envelope_certificate.json"
)
OUTPUT = ROOT / "results" / "uniform_euclidean_parity_certificate.json"
SIGMA = 0.01
START_DIMENSION = 4096
CONTINUUM_GALERKIN_DIMENSION = 65536
MINIMUM_ADAPTIVE_MULTIPLE = 8.0


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


def normalizer_lower() -> tuple[float, str]:
    previous = ctx.prec
    ctx.prec = 224
    try:
        sigma = arb(1) / 100
        value = (
            sigma
            * (arb.pi() / 2).sqrt()
            * (arb(2).sqrt() / sigma).erf()
        )
        upper_safe_lower = math.nextafter(
            float(value.lower()), -math.inf
        )
        return upper_safe_lower, str(value)
    finally:
        ctx.prec = previous


def envelope_from_certificate(
    certificate: dict[str, object]
) -> HilbertEnvelope:
    quantities = certificate["quantities"]
    return HilbertEnvelope(
        kernel=float(quantities["kernel"]["norm_upper"]),
        source_first=float(
            quantities["source_first"]["norm_upper"]
        ),
        target_first=float(
            quantities["target_first"]["norm_upper"]
        ),
        source_second=float(
            quantities["source_second"]["norm_upper"]
        ),
        source_target=float(
            quantities["source_target"]["norm_upper"]
        ),
        target_second=float(
            quantities["target_second"]["norm_upper"]
        ),
        source_second_target_second=float(
            quantities["source_second_target_second"]["norm_upper"]
        ),
    )


def main() -> None:
    grushin = load(GRUSHIN_PATH)
    midpoint = load(MIDPOINT_PATH)
    hilbert = load(HILBERT_PATH)
    if grushin["status"] != (
        "rigorous_exact_stored_euclidean_parity_circle_count_one"
    ):
        raise RuntimeError("the Euclidean Grushin gate is not closed")
    if midpoint["status"] != (
        "arb_exact_stored_to_midpoint_euclidean_bridge"
    ):
        raise RuntimeError("the Euclidean midpoint gate is not closed")
    if hilbert["status"] != (
        "rigorous_arb_hilbert_schmidt_derivative_envelope"
    ):
        raise RuntimeError("the Hilbert envelope gate is not closed")

    envelope = envelope_from_certificate(hilbert)
    center = float(grushin["center"])
    radius = float(grushin["radius"])
    minimum_modulus = math.nextafter(abs(center) - radius, 0.0)
    maximum_modulus = math.nextafter(abs(center) + radius, math.inf)
    stored_resolvent = float(
        grushin["contour_ledger"]["contour_resolvent_upper"]
    )

    stored_to_midpoint = neumann_transfer(
        stored_resolvent, float(midpoint["spectral_norm_upper"])
    )
    midpoint_to_galerkin_defect = midpoint_galerkin_defect(
        START_DIMENSION, envelope
    )
    midpoint_to_galerkin = neumann_transfer(
        stored_to_midpoint.transferred_resolvent_upper,
        midpoint_to_galerkin_defect,
    )

    dyadic_steps = {}
    current_dimension = START_DIMENSION
    current_resolvent = (
        midpoint_to_galerkin.transferred_resolvent_upper
    )
    while current_dimension < CONTINUUM_GALERKIN_DIMENSION:
        blocks = hilbert_haar_bounds(current_dimension, envelope)
        step = hilbert_schur_step(
            current_resolvent, minimum_modulus, blocks
        )
        fine_dimension = 2 * current_dimension
        dyadic_steps[
            f"{current_dimension}_to_{fine_dimension}"
        ] = {
            "blocks": blocks.as_dict(),
            "resolvent_step": step.as_dict(),
            "inside_count_after_transfer": (
                1 if step.count_transfers else None
            ),
        }
        current_dimension = fine_dimension
        current_resolvent = step.fine_resolvent_upper

    finite_rank_operator_resolvent = max(
        current_resolvent,
        math.nextafter(1.0 / minimum_modulus, math.inf),
    )
    continuum_defect = continuum_galerkin_defect(
        CONTINUUM_GALERKIN_DIMENSION, envelope
    )
    continuum_transfer = neumann_transfer(
        finite_rank_operator_resolvent, continuum_defect
    )

    family_dimension = CONTINUUM_GALERKIN_DIMENSION
    while True:
        family_dimension *= 2
        family_defect = math.nextafter(
            continuum_galerkin_defect(
                family_dimension, envelope
            )
            + midpoint_galerkin_defect(
                family_dimension, envelope
            ),
            math.inf,
        )
        midpoint_family_transfer = neumann_transfer(
            continuum_transfer.transferred_resolvent_upper,
            family_defect,
        )
        if midpoint_family_transfer.admissible:
            break
        if family_dimension > 1 << 30:
            raise RuntimeError("no Euclidean midpoint threshold was found")

    z_lower, z_ball = normalizer_lower()
    normalization = discrete_normalization_defect(
        family_dimension,
        SIGMA,
        z_lower,
        envelope.kernel,
        midpoint_galerkin_defect(family_dimension, envelope),
    )
    normalization_transfer = neumann_transfer(
        midpoint_family_transfer.transferred_resolvent_upper,
        normalization.spectral_norm_defect_upper,
    )
    declared_multiple = adaptive_multiple(
        family_dimension, MINIMUM_ADAPTIVE_MULTIPLE
    )
    cutoff = relaxed_cutoff_defect(
        family_dimension, SIGMA, declared_multiple
    )
    cutoff_transfer = neumann_transfer(
        normalization_transfer.transferred_resolvent_upper,
        cutoff.spectral_norm_upper,
    )
    weighted_riesz_cutoff = weighted_riesz_perturbation_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=(
            normalization_transfer.transferred_resolvent_upper
        ),
        second_resolvent_upper=(
            cutoff_transfer.transferred_resolvent_upper
        ),
        perturbation_upper=cutoff.spectral_norm_upper,
    )

    all_dyadic = all(
        row["resolvent_step"]["count_transfers"]
        for row in dyadic_steps.values()
    )
    all_gates = bool(
        stored_to_midpoint.admissible
        and midpoint_to_galerkin.admissible
        and all_dyadic
        and continuum_transfer.admissible
        and midpoint_family_transfer.admissible
        and normalization_transfer.admissible
        and cutoff_transfer.admissible
    )
    status = (
        "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
        if all_gates
        else "uniform_euclidean_parity_contour_not_closed"
    )
    payload = {
        "status": status,
        "scope": (
            "exact-real folded-Gaussian full and adaptive sparse midpoint "
            "Markov matrices at sigma=1/100, with Euclidean norm identified "
            "with the L2 cell basis"
        ),
        "evidence_level": (
            "analytic_hilbert_operator_theorem_plus_outward_arb_and_binary64_certificates"
        ),
        "contour": {
            "center": center,
            "radius": radius,
            "minimum_modulus_lower": minimum_modulus,
            "maximum_modulus_upper": maximum_modulus,
        },
        "hilbert_schmidt_envelope": envelope.as_dict(),
        "stored_euclidean_theorem": {
            "dimension": START_DIMENSION,
            "inside_count": 1,
            "contour_resolvent_upper": stored_resolvent,
        },
        "stored_to_exact_midpoint_4096": {
            "spectral_norm_defect_upper": midpoint[
                "spectral_norm_upper"
            ],
            "neumann_transfer": stored_to_midpoint.as_dict(),
            "inside_count_after_transfer": (
                1 if stored_to_midpoint.admissible else None
            ),
        },
        "midpoint_to_galerkin_4096": {
            "spectral_norm_defect_upper": (
                midpoint_to_galerkin_defect
            ),
            "neumann_transfer": midpoint_to_galerkin.as_dict(),
            "inside_count_after_transfer": (
                1 if midpoint_to_galerkin.admissible else None
            ),
        },
        "dyadic_hilbert_galerkin_steps": dyadic_steps,
        "galerkin_to_continuum_L2": {
            "dimension": CONTINUUM_GALERKIN_DIMENSION,
            "galerkin_matrix_resolvent_upper": current_resolvent,
            "zero_complement_resolvent_upper": (
                math.nextafter(1.0 / minimum_modulus, math.inf)
            ),
            "finite_rank_operator_resolvent_upper": (
                finite_rank_operator_resolvent
            ),
            "operator_norm_defect_upper": continuum_defect,
            "neumann_transfer": continuum_transfer.as_dict(),
            "inside_count_after_transfer": (
                1 if continuum_transfer.admissible else None
            ),
        },
        "continuum_L2_conclusion": {
            "inside_count": 1 if all_gates else None,
            "contour_resolvent_upper": (
                continuum_transfer.transferred_resolvent_upper
            ),
            "eigenvalue_is_real_negative_and_simple": all_gates,
        },
        "uniform_matrix_family": {
            "certified_threshold_dimension": family_dimension,
            "applies_to_every_larger_dimension": True,
            "continuum_to_exact_midpoint_defect_upper_at_threshold": (
                family_defect
            ),
            "exact_midpoint_transfer": (
                midpoint_family_transfer.as_dict()
            ),
            "normalizer_lower_ball": z_ball,
            "normalizer_lower": z_lower,
            "discrete_normalization": normalization.as_dict(),
            "discrete_normalization_transfer": (
                normalization_transfer.as_dict()
            ),
            "adaptive_schedule": (
                "L_n=max(8,2 sqrt(log n)); the archived eight-sigma "
                "window is retained until growth is needed"
            ),
            "fixed_eight_sigma_family": {
                "applies_to_every_larger_dimension": True,
                "uniform_cutoff_defect_upper": cutoff.spectral_norm_upper,
                "uniform_resolvent_upper": (
                    cutoff_transfer.transferred_resolvent_upper
                ),
                "inside_count": 1 if all_gates else None,
                "row_norm_convergence_claimed": False,
                "comment": (
                    "the fixed window is uniformly tiny in Euclidean norm "
                    "but has the nonzero row-defect floor proved in RH-39"
                ),
            },
            "adaptive_family": {
                "schedule": "L_n=max(8,2 sqrt(log n))",
                "applies_to_every_larger_dimension": True,
                "uniform_resolvent_upper": (
                    cutoff_transfer.transferred_resolvent_upper
                ),
                "inside_count": 1 if all_gates else None,
                "euclidean_cutoff_rate": (
                    "O(n^-2 (log n)^-1/4) after the growth branch begins"
                ),
                "weighted_riesz_bridge_is_second_order": all_gates,
            },
            "declared_multiple_at_threshold": declared_multiple,
            "cutoff_defect_at_threshold": cutoff.as_dict(),
            "cutoff_transfer": cutoff_transfer.as_dict(),
            "inside_count_for_full_and_adaptive_sparse_matrices": (
                1 if all_gates else None
            ),
            "uniform_full_matrix_resolvent_upper": (
                normalization_transfer.transferred_resolvent_upper
            ),
            "uniform_adaptive_sparse_resolvent_upper": (
                cutoff_transfer.transferred_resolvent_upper
            ),
            "weighted_riesz_cutoff_perturbation_upper_at_threshold": (
                weighted_riesz_cutoff
            ),
            "uniform_fixed_eight_weighted_riesz_difference_upper": (
                weighted_riesz_cutoff
            ),
        },
        "gate_summary": {
            "stored_to_midpoint_product_upper": (
                stored_to_midpoint.neumann_product_upper
            ),
            "midpoint_to_galerkin_product_upper": (
                midpoint_to_galerkin.neumann_product_upper
            ),
            "maximum_dyadic_schur_product_upper": max(
                row["resolvent_step"][
                    "schur_neumann_product_upper"
                ]
                for row in dyadic_steps.values()
            ),
            "continuum_product_upper": (
                continuum_transfer.neumann_product_upper
            ),
            "midpoint_family_product_upper": (
                midpoint_family_transfer.neumann_product_upper
            ),
            "normalization_product_upper": (
                normalization_transfer.neumann_product_upper
            ),
            "cutoff_product_upper": (
                cutoff_transfer.neumann_product_upper
            ),
            "all_gates_closed": all_gates,
        },
        "dependencies": {
            "euclidean_grushin_certificate": repository_entry(
                GRUSHIN_PATH
            ),
            "euclidean_midpoint_bridge": repository_entry(MIDPOINT_PATH),
            "hilbert_envelope_certificate": repository_entry(HILBERT_PATH),
            "rh39_cutoff_certificate": repository_entry(
                RH39
                / "results"
                / "uniform_gaussian_cutoff_bridge_certificate.json"
            ),
            "rh40_weighted_riesz_manuscript": repository_entry(
                RH40 / "main.tex"
            ),
            "rh41_continuum_certificate": repository_entry(
                RH41
                / "results"
                / "validated_parity_continuum_certificate.json"
            ),
        },
        "limitations": [
            "The theorem is at the fixed positive noise width sigma=1/100.",
            "The all-dimension sparse family is an exact-real mathematical matrix family; no uniform theorem for every binary64 transcendental evaluation is claimed.",
            "The fourth mixed derivative enclosure is deliberately coarse but contributes only at order h^4.",
            "The result does not take a zero-noise limit or identify any zeta zero.",
            "No self-adjoint Hilbert-Polya operator or Riemann-hypothesis claim is made.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if status != (
        "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
    ):
        raise RuntimeError("the uniform Euclidean certificate did not close")


if __name__ == "__main__":
    main()
