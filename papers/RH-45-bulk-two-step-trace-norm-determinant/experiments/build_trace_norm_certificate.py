"""Compose Hilbert--Schmidt, trace-norm, and determinant convergence gates."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"
RH44 = PAPERS / "RH-44-validated-rank-two-peripheral-complement"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH42 / "src"),
    str(RH43 / "src"),
]

from bulk_trace import (  # noqa: E402
    bulk_trace_norm_ledger,
    determinant_lipschitz_upper,
    even_trace_error_upper,
    hilbert_schmidt_galerkin_defect,
)
from bulk_trace.bounds import upper_add, upper_multiply  # noqa: E402
from euclidean_contour import (  # noqa: E402
    HilbertEnvelope,
    adaptive_multiple,
    discrete_normalization_defect,
    hilbert_haar_bounds,
    hilbert_schur_step,
    midpoint_galerkin_defect,
    neumann_transfer,
    relaxed_cutoff_defect,
)
from weighted_kernel import (  # noqa: E402
    weighted_lipschitz_upper,
    weighted_schur_transport,
)


RH42_CERTIFICATE_PATH = (
    RH42 / "results" / "uniform_euclidean_parity_certificate.json"
)
RH44_CERTIFICATE_PATH = (
    RH44 / "results" / "validated_rank_two_peripheral_complement.json"
)
OUTPUT = ROOT / "results" / "bulk_trace_norm_determinant_certificate.json"
DIMENSIONS = tuple(1 << power for power in range(16, 31))
DETERMINANT_RADII = (1.0e-4, 1.0e-3, 1.0e-2)


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


def contour_chain(
    *,
    dimension: int,
    envelope: HilbertEnvelope,
    contour: dict[str, float],
    continuum_resolvent_upper: float,
    galerkin_operator_defect_upper: float,
    midpoint_defect_upper: float,
    normalization_defect_upper: float,
    cutoff_defect_upper: float | None,
) -> dict[str, object]:
    radius = float(contour["radius"])
    minimum_modulus = float(contour["minimum_modulus_lower"])
    maximum_modulus = float(contour["maximum_modulus_upper"])
    continuum_resolvent = float(continuum_resolvent_upper)

    galerkin_transfer = neumann_transfer(
        continuum_resolvent, galerkin_operator_defect_upper
    )
    blocks = hilbert_haar_bounds(dimension, envelope)
    schur = hilbert_schur_step(
        galerkin_transfer.transferred_resolvent_upper,
        minimum_modulus,
        blocks,
    )
    complement_weighted = weighted_schur_transport(
        coarse_dimension=dimension,
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        coarse_resolvent_upper=(
            galerkin_transfer.transferred_resolvent_upper
        ),
        detail_to_coarse_upper=blocks.detail_to_coarse,
        coarse_to_detail_upper=blocks.coarse_to_detail,
        detail_resolvent_upper=schur.detail_resolvent_upper,
        schur_inverse_upper=continuum_resolvent,
    )

    midpoint_transfer = neumann_transfer(
        galerkin_transfer.transferred_resolvent_upper,
        midpoint_defect_upper,
    )
    midpoint_weighted = weighted_lipschitz_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=(
            galerkin_transfer.transferred_resolvent_upper
        ),
        second_resolvent_upper=(
            midpoint_transfer.transferred_resolvent_upper
        ),
        perturbation_upper=midpoint_defect_upper,
    )
    full_transfer = neumann_transfer(
        midpoint_transfer.transferred_resolvent_upper,
        normalization_defect_upper,
    )
    normalization_weighted = weighted_lipschitz_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=(
            midpoint_transfer.transferred_resolvent_upper
        ),
        second_resolvent_upper=full_transfer.transferred_resolvent_upper,
        perturbation_upper=normalization_defect_upper,
    )
    full_weighted_error = upper_add(
        complement_weighted.weighted_term_difference_upper,
        midpoint_weighted,
        normalization_weighted,
    )

    payload: dict[str, object] = {
        "galerkin_transfer": galerkin_transfer.as_dict(),
        "complement_blocks": blocks.as_dict(),
        "complement_detail_resolvent_upper": (
            schur.detail_resolvent_upper
        ),
        "complement_weighted_transport": complement_weighted.as_dict(),
        "midpoint_transfer": midpoint_transfer.as_dict(),
        "midpoint_weighted_error_upper": midpoint_weighted,
        "full_transfer": full_transfer.as_dict(),
        "normalization_weighted_error_upper": normalization_weighted,
        "full_weighted_operator_error_upper": full_weighted_error,
    }
    if cutoff_defect_upper is None:
        payload["adaptive_weighted_operator_error_upper"] = (
            full_weighted_error
        )
        payload["adaptive_resolvent_upper"] = (
            full_transfer.transferred_resolvent_upper
        )
        return payload

    cutoff_transfer = neumann_transfer(
        full_transfer.transferred_resolvent_upper,
        cutoff_defect_upper,
    )
    cutoff_weighted = weighted_lipschitz_upper(
        contour_radius=radius,
        contour_maximum_modulus=maximum_modulus,
        first_resolvent_upper=full_transfer.transferred_resolvent_upper,
        second_resolvent_upper=cutoff_transfer.transferred_resolvent_upper,
        perturbation_upper=cutoff_defect_upper,
    )
    payload["cutoff_transfer"] = cutoff_transfer.as_dict()
    payload["cutoff_weighted_error_upper"] = cutoff_weighted
    payload["adaptive_weighted_operator_error_upper"] = upper_add(
        full_weighted_error, cutoff_weighted
    )
    payload["adaptive_resolvent_upper"] = (
        cutoff_transfer.transferred_resolvent_upper
    )
    return payload


def main() -> None:
    rh42 = load(RH42_CERTIFICATE_PATH)
    rh44 = load(RH44_CERTIFICATE_PATH)
    if rh42["status"] != (
        "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
    ):
        raise RuntimeError("RH-42 Hilbert infrastructure is not closed")
    if rh44["status"] != (
        "rigorous_intrinsic_rank_two_peripheral_kernel_and_bulk_deflation"
    ):
        raise RuntimeError("RH-44 rank-two bulk gate is not closed")

    envelope = HilbertEnvelope(**rh42["hilbert_schmidt_envelope"])
    rank_two_hs = float(
        rh44["intrinsic_rank_two_kernel"]["envelope"][
            "kernel_hilbert_schmidt_upper"
        ]
    )
    continuum_bulk_hs = upper_add(envelope.kernel, rank_two_hs)
    contours = rh44["contours"]
    perron_resolvent = float(
        rh44["perron_continuum_contour"][
            "continuum_L2_resolvent_upper"
        ]
    )
    parity_resolvent = float(
        load(
            RH43
            / "results"
            / "validated_weighted_parity_kernel.json"
        )["continuum_complement_schur"][
            "improved_continuum_L2_resolvent_upper"
        ]
    )
    normalizer_lower = float(
        rh42["uniform_matrix_family"]["normalizer_lower"]
    )

    dimension_ledgers = {}
    all_gates = True
    for dimension in DIMENSIONS:
        galerkin_hs = hilbert_schmidt_galerkin_defect(
            dimension,
            envelope.source_first,
            envelope.target_first,
        )
        midpoint_hs = midpoint_galerkin_defect(dimension, envelope)
        normalization = discrete_normalization_defect(
            dimension,
            0.01,
            normalizer_lower,
            envelope.kernel,
            midpoint_hs,
        )
        full_markov_hs = upper_add(
            galerkin_hs,
            midpoint_hs,
            normalization.spectral_norm_defect_upper,
        )
        multiple = adaptive_multiple(dimension, 8.0)
        cutoff = relaxed_cutoff_defect(
            dimension, 0.01, multiple
        )
        adaptive_markov_hs = upper_add(
            full_markov_hs, cutoff.spectral_norm_upper
        )

        perron = contour_chain(
            dimension=dimension,
            envelope=envelope,
            contour=contours["perron"],
            continuum_resolvent_upper=perron_resolvent,
            galerkin_operator_defect_upper=galerkin_hs,
            midpoint_defect_upper=midpoint_hs,
            normalization_defect_upper=(
                normalization.spectral_norm_defect_upper
            ),
            cutoff_defect_upper=cutoff.spectral_norm_upper,
        )
        parity = contour_chain(
            dimension=dimension,
            envelope=envelope,
            contour=contours["parity"],
            continuum_resolvent_upper=parity_resolvent,
            galerkin_operator_defect_upper=galerkin_hs,
            midpoint_defect_upper=midpoint_hs,
            normalization_defect_upper=(
                normalization.spectral_norm_defect_upper
            ),
            cutoff_defect_upper=cutoff.spectral_norm_upper,
        )
        full_ledger = bulk_trace_norm_ledger(
            markov_hilbert_schmidt_error_upper=full_markov_hs,
            perron_weighted_operator_error_upper=float(
                perron["full_weighted_operator_error_upper"]
            ),
            parity_weighted_operator_error_upper=float(
                parity["full_weighted_operator_error_upper"]
            ),
            continuum_bulk_hilbert_schmidt_upper=continuum_bulk_hs,
        )
        adaptive_ledger = bulk_trace_norm_ledger(
            markov_hilbert_schmidt_error_upper=adaptive_markov_hs,
            perron_weighted_operator_error_upper=float(
                perron["adaptive_weighted_operator_error_upper"]
            ),
            parity_weighted_operator_error_upper=float(
                parity["adaptive_weighted_operator_error_upper"]
            ),
            continuum_bulk_hilbert_schmidt_upper=continuum_bulk_hs,
        )

        determinant_bounds = {}
        for radius in DETERMINANT_RADII:
            determinant_bounds[str(radius)] = {
                "bulk_square_disk_radius": radius,
                "symmetric_det2_disk_radius": math.sqrt(radius),
                "full_fredholm_determinant_error_upper": (
                    determinant_lipschitz_upper(
                        disk_radius=radius,
                        trace_norm_error_upper=(
                            full_ledger.square_trace_norm_error_upper
                        ),
                        first_trace_norm_upper=(
                            full_ledger.continuum_square_trace_norm_upper
                        ),
                        second_trace_norm_upper=(
                            full_ledger.approximate_square_trace_norm_upper
                        ),
                    )
                ),
                "adaptive_fredholm_determinant_error_upper": (
                    determinant_lipschitz_upper(
                        disk_radius=radius,
                        trace_norm_error_upper=(
                            adaptive_ledger.square_trace_norm_error_upper
                        ),
                        first_trace_norm_upper=(
                            adaptive_ledger.continuum_square_trace_norm_upper
                        ),
                        second_trace_norm_upper=(
                            adaptive_ledger.approximate_square_trace_norm_upper
                        ),
                    )
                ),
            }

        square_operator = max(
            full_ledger.continuum_square_trace_norm_upper,
            full_ledger.approximate_square_trace_norm_upper,
        )
        trace_coefficients = {
            str(power): even_trace_error_upper(
                square_power=power,
                square_trace_norm_error_upper=(
                    full_ledger.square_trace_norm_error_upper
                ),
                square_operator_norm_upper=square_operator,
            )
            for power in range(1, 5)
        }
        row_gates = (
            perron["galerkin_transfer"]["admissible"]
            and perron["midpoint_transfer"]["admissible"]
            and perron["full_transfer"]["admissible"]
            and perron["cutoff_transfer"]["admissible"]
            and parity["galerkin_transfer"]["admissible"]
            and parity["midpoint_transfer"]["admissible"]
            and parity["full_transfer"]["admissible"]
            and parity["cutoff_transfer"]["admissible"]
        )
        all_gates = bool(all_gates and row_gates)
        dimension_ledgers[str(dimension)] = {
            "dimension": dimension,
            "adaptive_support_multiple": multiple,
            "markov_hilbert_schmidt_components": {
                "continuum_to_galerkin_upper": galerkin_hs,
                "galerkin_to_midpoint_upper": midpoint_hs,
                "midpoint_to_full_normalized_upper": (
                    normalization.spectral_norm_defect_upper
                ),
                "adaptive_cutoff_upper": cutoff.spectral_norm_upper,
                "full_total_upper": full_markov_hs,
                "adaptive_total_upper": adaptive_markov_hs,
            },
            "perron_contour_chain": perron,
            "parity_contour_chain": parity,
            "full_bulk": full_ledger.as_dict(),
            "adaptive_bulk": adaptive_ledger.as_dict(),
            "even_trace_error_uppers": trace_coefficients,
            "determinant_disk_bounds": determinant_bounds,
            "all_contour_gates_closed": row_gates,
        }

    first = dimension_ledgers[str(DIMENSIONS[0])]
    last = dimension_ledgers[str(DIMENSIONS[-1])]
    asymptotic_checks = {
        "first_dimension": DIMENSIONS[0],
        "last_dimension": DIMENSIONS[-1],
        "full_bulk_hs_scaled_first": upper_multiply(
            DIMENSIONS[0],
            first["full_bulk"]["bulk_hilbert_schmidt_error_upper"],
        ),
        "full_bulk_hs_scaled_last": upper_multiply(
            DIMENSIONS[-1],
            last["full_bulk"]["bulk_hilbert_schmidt_error_upper"],
        ),
        "full_square_trace_scaled_first": upper_multiply(
            DIMENSIONS[0],
            first["full_bulk"]["square_trace_norm_error_upper"],
        ),
        "full_square_trace_scaled_last": upper_multiply(
            DIMENSIONS[-1],
            last["full_bulk"]["square_trace_norm_error_upper"],
        ),
        "adaptive_bulk_hs_scaled_last": upper_multiply(
            DIMENSIONS[-1],
            last["adaptive_bulk"]["bulk_hilbert_schmidt_error_upper"],
        ),
        "adaptive_square_trace_scaled_last": upper_multiply(
            DIMENSIONS[-1],
            last["adaptive_bulk"]["square_trace_norm_error_upper"],
        ),
    }

    status = (
        "rigorous_full_and_adaptive_bulk_square_trace_norm_and_determinant_convergence"
        if all_gates
        else "bulk_trace_norm_or_determinant_gate_not_closed"
    )
    payload = {
        "status": status,
        "scope": (
            "intrinsic Perron/parity-deflated full and adaptive exact-real "
            "bulk two-step families at sigma=1/100"
        ),
        "evidence_level": (
            "analytic_hilbert_schmidt_to_trace_ideal_theorem_plus_outward_contour_and_kernel_ledgers"
        ),
        "continuum_bulk": {
            "definition": "B=K-Q_+-Q_-",
            "hilbert_schmidt_upper": continuum_bulk_hs,
            "square_trace_norm_upper": upper_multiply(
                continuum_bulk_hs, continuum_bulk_hs
            ),
            "square_is_trace_class": True,
        },
        "main_theorems": {
            "full_bulk_hilbert_schmidt_rate": "O(n^-1)",
            "adaptive_bulk_hilbert_schmidt_rate": "O(n^-1)",
            "full_bulk_square_trace_norm_rate": "O(n^-1)",
            "adaptive_bulk_square_trace_norm_rate": "O(n^-1)",
            "even_trace_coefficient_convergence": (
                "tr(B_n^(2m))->tr(B^(2m)) for every fixed m>=1"
            ),
            "fredholm_determinant_convergence": (
                "det(I-w B_n^2)->det(I-w B^2) locally uniformly in w"
            ),
            "symmetric_det2_identity": (
                "det_2(I-zB) det_2(I+zB)=det(I-z^2 B^2)"
            ),
            "fixed_eight_sigma_continuum_convergence_claimed": False,
        },
        "dimension_ledgers": dimension_ledgers,
        "asymptotic_checks": asymptotic_checks,
        "dependencies": {
            "rh39_cutoff_certificate": repository_entry(
                RH39
                / "results"
                / "uniform_gaussian_cutoff_bridge_certificate.json"
            ),
            "rh42_uniform_euclidean_certificate": repository_entry(
                RH42_CERTIFICATE_PATH
            ),
            "rh43_weighted_schur_source": repository_entry(
                RH43 / "src" / "weighted_kernel" / "bounds.py"
            ),
            "rh44_rank_two_certificate": repository_entry(
                RH44_CERTIFICATE_PATH
            ),
        },
        "limitations": [
            "The theorem is at the fixed positive noise width sigma=1/100.",
            "The explicit trace-norm rate is first order because piecewise-constant Galerkin lifting approximates a smooth kernel in Hilbert-Schmidt norm at order n^-1.",
            "The determinant estimate is rigorous but deliberately coarse; it certifies local uniform convergence rather than a sharp large-disk enclosure at the threshold dimension.",
            "The fixed eight-sigma family is uniformly spectrally stable but is not claimed to converge to the full continuum bulk in Hilbert-Schmidt or trace norm.",
            "No zero-noise limit, arithmetic trace formula, prime-power identity, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, or Riemann-hypothesis claim is made.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not all_gates:
        raise RuntimeError("at least one trace-norm contour gate failed")


if __name__ == "__main__":
    main()
