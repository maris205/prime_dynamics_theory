"""Validated Perron/parity factors for exact stochastic repaired matrices."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from flint import arb, arb_mat, ctx
import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH72 = PAPERS / "RH-72-validated-folded-gaussian-assembly"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH14 / "src"),
    str(RH42 / "src"),
    str(RH72 / "src"),
]

from euclidean_contour import euclidean_grushin_ledger  # noqa: E402
from folded_assembly import exact_stochastic_repair  # noqa: E402
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from peripheral_validation import (  # noqa: E402
    newton_contraction_radius,
)


FULL_OUTPUT = ROOT / "results" / "peripheral_validation_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "peripheral_validation_smoke.json"
SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
FINE_RESOLUTION = 5.12
PRECISION_BITS = 160
PARITY_CONTOUR_RADIUS = 0.01


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def exact_arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower_float(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def fraction_matrix_to_float(rows: list[list[Fraction]]) -> np.ndarray:
    return np.asarray(
        [[float(value) for value in row] for row in rows],
        dtype=np.float64,
    )


def fraction_matrix_to_arb(rows: list[list[Fraction]]) -> arb_mat:
    return arb_mat(
        [
            [exact_arb_fraction(value) for value in row]
            for row in rows
        ]
    )


def float_matrix_to_arb(values: np.ndarray) -> arb_mat:
    array = np.asarray(values, dtype=np.float64)
    return arb_mat(
        [
            [exact_arb_float(array[row, column]) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def float_vector_to_arb(values: np.ndarray) -> arb_mat:
    vector = np.asarray(values, dtype=np.float64).reshape(-1)
    return arb_mat([[exact_arb_float(value)] for value in vector])


def fraction_vector_to_arb(values: list[Fraction]) -> arb_mat:
    return arb_mat([[exact_arb_fraction(value)] for value in values])


def identity_arb(dimension: int) -> arb_mat:
    return arb_mat(
        [
            [arb(1) if row == column else arb(0) for column in range(dimension)]
            for row in range(dimension)
        ]
    )


def frobenius_norm(matrix: arb_mat) -> arb:
    return sum((entry**2 for entry in matrix.entries()), arb(0)).sqrt()


def vector_norm(vector: arb_mat) -> arb:
    return frobenius_norm(vector)


def arb_dot(left: np.ndarray, right: np.ndarray) -> arb:
    """Exact dyadic dot product enclosed at the active Arb precision."""

    left_values = np.asarray(left, dtype=np.float64).reshape(-1)
    right_values = np.asarray(right, dtype=np.float64).reshape(-1)
    if left_values.shape != right_values.shape:
        raise ValueError("dot-product dimensions do not agree")
    return sum(
        (
            exact_arb_float(float(left_value))
            * exact_arb_float(float(right_value))
            for left_value, right_value in zip(left_values, right_values)
        ),
        arb(0),
    )


def exact_left_residual(
    exact_rows: list[list[Fraction]],
    parity_value: float,
    left: np.ndarray,
) -> arb:
    """Enclose A^T l-lambda l without a rounded matrix product."""

    dimension = len(exact_rows)
    left_fractions = [
        Fraction.from_float(float(value)) for value in np.asarray(left)
    ]
    lambda_fraction = Fraction.from_float(parity_value)
    residual = []
    for column in range(dimension):
        value = sum(
            exact_rows[row][column] * left_fractions[row]
            for row in range(dimension)
        ) - lambda_fraction * left_fractions[column]
        residual.append(value)
    return vector_norm(fraction_vector_to_arb(residual))


def certified_projector_ledger(
    right_norm: arb,
    left_norm: arb,
    right_error: arb,
    left_error: arb,
) -> tuple[dict[str, object], arb]:
    """Arb enclosure of the normalized rank-one projector error."""

    normalization = (left_norm + left_error) * right_error
    gram_lower = arb(1) - normalization
    if lower_float(gram_lower) <= 0.0:
        raise RuntimeError("parity projector normalization reaches zero")
    numerator = right_error * (left_norm + left_error) + right_norm * left_error
    projector_error = (
        numerator / gram_lower
        + right_norm * left_norm * normalization / gram_lower
    )
    return {
        "normalization_error_ball": str(normalization),
        "normalization_error_upper": upper_float(normalization),
        "normalization_gram_lower_ball": str(gram_lower),
        "normalization_gram_lower": lower_float(gram_lower),
        "numerator_error_ball": str(numerator),
        "numerator_error_upper": upper_float(numerator),
        "projector_two_norm_error_ball": str(projector_error),
        "projector_two_norm_error_upper": upper_float(projector_error),
    }, projector_error


def exact_repaired_matrix(sigma: float) -> list[list[Fraction]]:
    dimension = max(
        32,
        2 * int(round(FINE_RESOLUTION / sigma / 2.0)),
    )
    frozen = sparse_folded_gaussian_matrix(dimension, sigma).toarray()
    rows = []
    for row in frozen:
        _, _, repaired = exact_stochastic_repair(row)
        rows.append(list(repaired))
    return rows


def exact_coarse_matrix(
    fine: list[list[Fraction]],
) -> list[list[Fraction]]:
    dimension = len(fine)
    coarse = dimension // 2
    result = []
    for row in range(coarse):
        values = []
        for column in range(coarse):
            total = (
                fine[2 * row][2 * column]
                + fine[2 * row][2 * column + 1]
                + fine[2 * row + 1][2 * column]
                + fine[2 * row + 1][2 * column + 1]
            )
            values.append(total / 2)
        if sum(values, Fraction(0, 1)) != 1:
            raise ArithmeticError("coarse matrix lost stochasticity")
        result.append(values)
    return result


def approximate_peripheral(matrix: np.ndarray) -> dict[str, object]:
    values, left, right = eig(
        matrix, left=True, right=True, check_finite=False
    )
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    real_negative = np.flatnonzero(
        (np.abs(values.imag) < 1.0e-8) & (values.real < 0.0)
    )
    if not real_negative.size:
        raise RuntimeError("no real negative parity eigenvalue")
    parity_index = int(real_negative[np.argmin(values[real_negative].real)])

    stationary = np.asarray(left[:, perron_index].real)
    stationary /= np.sum(stationary)
    if np.sum(stationary) < 0.0:
        stationary *= -1.0

    parity_value = float(values[parity_index].real)
    parity_right = np.asarray(right[:, parity_index].real)
    parity_right /= np.linalg.norm(parity_right)
    parity_left = np.asarray(left[:, parity_index].real)
    parity_left /= float(np.dot(parity_left, parity_right))
    return {
        "stationary": stationary,
        "parity_value": parity_value,
        "parity_right": parity_right,
        "parity_left": parity_left,
        "minimum_other_eigenvalue_distance": float(
            np.min(
                np.abs(
                    np.delete(values, parity_index) - parity_value
                )
            )
        ),
    }


def inverse_certificate(
    exact_matrix: arb_mat,
    approximate_matrix: np.ndarray,
) -> tuple[arb_mat, dict[str, object]]:
    inverse = np.linalg.inv(np.asarray(approximate_matrix, dtype=np.float64))
    inverse_ball = float_matrix_to_arb(inverse)
    defect = identity_arb(approximate_matrix.shape[0]) - inverse_ball * exact_matrix
    gamma = frobenius_norm(defect)
    inverse_norm = frobenius_norm(inverse_ball)
    if upper_float(gamma) >= 1.0:
        raise RuntimeError("Neumann inverse certificate failed")
    return inverse_ball, {
        "inverse_frobenius_ball": str(inverse_norm),
        "inverse_frobenius_upper": upper_float(inverse_norm),
        "inverse_residual_frobenius_ball": str(gamma),
        "inverse_residual_frobenius_upper": upper_float(gamma),
        "inverse_certified": True,
    }


def stationary_certificate(
    exact_rows: list[list[Fraction]],
    matrix: np.ndarray,
    stationary: np.ndarray,
) -> dict[str, object]:
    dimension = matrix.shape[0]
    one_over_n = Fraction(1, dimension)
    system_rows = [
        [
            (Fraction(1, 1) if row == column else Fraction(0, 1))
            - exact_rows[column][row]
            + one_over_n
            for column in range(dimension)
        ]
        for row in range(dimension)
    ]
    right_hand_side = [one_over_n for _ in range(dimension)]
    system_float = fraction_matrix_to_float(system_rows)
    system_ball = fraction_matrix_to_arb(system_rows)
    inverse_ball, inverse_record = inverse_certificate(
        system_ball, system_float
    )
    residual = (
        fraction_vector_to_arb(right_hand_side)
        - system_ball * float_vector_to_arb(stationary)
    )
    correction = inverse_ball * residual
    beta = vector_norm(correction)
    gamma = arb(inverse_record["inverse_residual_frobenius_ball"])
    error = beta / (arb(1) - gamma)
    return {
        **inverse_record,
        "stationary_residual_ball": str(vector_norm(residual)),
        "preconditioned_stationary_residual_ball": str(beta),
        "stationary_two_norm_error_ball": str(error),
        "stationary_two_norm_error_upper": upper_float(error),
        "stationary_normalization_defect": abs(
            float(np.sum(stationary)) - 1.0
        ),
        "perron_projector_two_norm_error_upper": math.sqrt(dimension)
        * upper_float(error),
        "perron_simple_certified": True,
    }


def parity_newton_certificate(
    exact_rows: list[list[Fraction]],
    matrix: np.ndarray,
    parity_value: float,
    right: np.ndarray,
    left: np.ndarray,
) -> tuple[dict[str, object], arb, arb, arb]:
    dimension = matrix.shape[0]
    lambda_fraction = Fraction.from_float(parity_value)
    right_fractions = [Fraction.from_float(float(value)) for value in right]
    left_fractions = [Fraction.from_float(float(value)) for value in left]
    jacobian_rows: list[list[Fraction]] = []
    for row in range(dimension):
        jacobian_rows.append(
            [
                exact_rows[row][column]
                - (
                    lambda_fraction
                    if row == column
                    else Fraction(0, 1)
                )
                for column in range(dimension)
            ]
            + [-right_fractions[row]]
        )
    jacobian_rows.append(left_fractions + [Fraction(0, 1)])
    jacobian_float = fraction_matrix_to_float(jacobian_rows)
    jacobian_ball = fraction_matrix_to_arb(jacobian_rows)
    inverse_ball, inverse_record = inverse_certificate(
        jacobian_ball, jacobian_float
    )

    residual_values = []
    for row in range(dimension):
        value = sum(
            exact_rows[row][column] * right_fractions[column]
            for column in range(dimension)
        ) - lambda_fraction * right_fractions[row]
        residual_values.append(value)
    residual_values.append(
        sum(
            left_fractions[index] * right_fractions[index]
            for index in range(dimension)
        )
        - 1
    )
    residual = fraction_vector_to_arb(residual_values)
    beta = vector_norm(inverse_ball * residual)
    gamma = arb(inverse_record["inverse_residual_frobenius_ball"])
    inverse_norm = arb(inverse_record["inverse_frobenius_ball"])
    ledger = newton_contraction_radius(
        upper_float(beta),
        upper_float(gamma),
        upper_float(inverse_norm),
    )
    radius = exact_arb_float(ledger.radius)
    contraction = gamma + inverse_norm * radius
    self_map = beta + gamma * radius + inverse_norm * radius**2
    if upper_float(contraction) >= 1.0 or self_map.upper() > radius.lower():
        raise RuntimeError("interval Newton self-map failed")

    right_norm = vector_norm(float_vector_to_arb(right))
    left_norm = vector_norm(float_vector_to_arb(left))
    right_residual = vector_norm(
        fraction_vector_to_arb(residual_values[:-1])
    )
    return {
        **inverse_record,
        "parity_value_center": parity_value,
        "right_norm_ball": str(right_norm),
        "left_norm_ball": str(left_norm),
        "right_residual_ball": str(right_residual),
        "newton_beta_ball": str(beta),
        "newton_radius_ball": str(radius),
        "newton_radius_upper": upper_float(radius),
        "newton_contraction_ball": str(contraction),
        "newton_contraction_upper": upper_float(contraction),
        "newton_self_map_ball": str(self_map),
        "right_eigenpair_certified": True,
    }, radius, right_norm, left_norm


def left_parity_certificate(
    exact_rows: list[list[Fraction]],
    matrix: np.ndarray,
    parity_value: float,
    right: np.ndarray,
    left: np.ndarray,
    eigen_radius: arb,
) -> dict[str, object]:
    dimension = matrix.shape[0]
    lambda_fraction = Fraction.from_float(parity_value)
    right_fractions = [Fraction.from_float(float(value)) for value in right]
    left_fractions = [Fraction.from_float(float(value)) for value in left]
    system_rows: list[list[Fraction]] = []
    for row in range(dimension):
        system_rows.append(
            [
                exact_rows[column][row]
                - (
                    lambda_fraction
                    if row == column
                    else Fraction(0, 1)
                )
                for column in range(dimension)
            ]
            + [left_fractions[row]]
        )
    system_rows.append(right_fractions + [Fraction(0, 1)])
    system_float = fraction_matrix_to_float(system_rows)
    system_ball = fraction_matrix_to_arb(system_rows)
    inverse_ball, inverse_record = inverse_certificate(
        system_ball, system_float
    )
    candidate = np.concatenate((left, np.zeros(1)))
    rhs = [Fraction(0, 1) for _ in range(dimension)] + [Fraction(1, 1)]
    residual = (
        fraction_vector_to_arb(rhs)
        - system_ball * float_vector_to_arb(candidate)
    )
    beta0 = vector_norm(inverse_ball * residual)
    inverse_norm = arb(inverse_record["inverse_frobenius_ball"])
    gamma = arb(inverse_record["inverse_residual_frobenius_ball"])
    left_norm = vector_norm(float_vector_to_arb(left))
    total_defect = gamma + inverse_norm * eigen_radius
    total_beta = beta0 + inverse_norm * eigen_radius * left_norm
    if upper_float(total_defect) >= 1.0:
        raise RuntimeError("left parity interval solve failed")
    error = total_beta / (arb(1) - total_defect)
    return {
        **inverse_record,
        "left_solve_beta_zero_ball": str(beta0),
        "left_solve_total_defect_ball": str(total_defect),
        "left_solve_total_defect_upper": upper_float(total_defect),
        "left_two_norm_error_ball": str(error),
        "left_two_norm_error_upper": upper_float(error),
        "left_eigenvector_certified": True,
    }


def channel_certificate(
    name: str,
    exact_rows: list[list[Fraction]],
) -> dict[str, object]:
    started = time.perf_counter()
    matrix = fraction_matrix_to_float(exact_rows)
    approximate = approximate_peripheral(matrix)
    stationary = stationary_certificate(
        exact_rows, matrix, np.asarray(approximate["stationary"])
    )
    right = np.asarray(approximate["parity_right"])
    left = np.asarray(approximate["parity_left"])
    parity, radius, right_norm, left_norm = parity_newton_certificate(
        exact_rows,
        matrix,
        float(approximate["parity_value"]),
        right,
        left,
    )
    left_certificate = left_parity_certificate(
        exact_rows,
        matrix,
        float(approximate["parity_value"]),
        right,
        left,
        radius,
    )
    left_error_ball = arb(left_certificate["left_two_norm_error_ball"])
    projector_record, projector_error_ball = certified_projector_ledger(
        right_norm,
        left_norm,
        radius,
        left_error_ball,
    )
    perron_projector_error_ball = (
        arb(matrix.shape[0]).sqrt()
        * arb(stationary["stationary_two_norm_error_ball"])
    )
    rank_two_projector_error_ball = (
        perron_projector_error_ball + projector_error_ball
    )
    parity_modulus_ball = (
        exact_arb_float(abs(float(approximate["parity_value"]))) + radius
    )
    parity_projector_norm_ball = right_norm * left_norm
    bulk_error_ball = (
        perron_projector_error_ball
        + parity_modulus_ball * projector_error_ball
        + radius * parity_projector_norm_ball
    )
    gram_ball = arb_dot(left, right)
    gram_lower = lower_float(gram_ball)
    gram_upper = upper_float(gram_ball)
    if gram_lower <= 0.0 or gram_upper < gram_lower:
        raise RuntimeError("approximate parity Gram ball is invalid")
    center_inverse_ball = (
        arb(parity["inverse_frobenius_ball"])
        / (arb(1) - arb(parity["inverse_residual_frobenius_ball"]))
    )
    left_residual_ball = exact_left_residual(
        exact_rows,
        float(approximate["parity_value"]),
        left,
    )
    contour = euclidean_grushin_ledger(
        radius=PARITY_CONTOUR_RADIUS,
        center_reduced_inverse_upper=upper_float(center_inverse_ball),
        right_mode_two_upper=upper_float(right_norm),
        left_mode_two_upper=upper_float(left_norm),
        right_residual_two_upper=upper_float(
            arb(parity["right_residual_ball"])
        ),
        left_residual_two_upper=upper_float(left_residual_ball),
        gram_lower=gram_lower,
        gram_upper=gram_upper,
        border_scale=1.0,
    )
    if not contour.rouche_count_one:
        raise RuntimeError("parity contour count did not close")
    return {
        "name": name,
        "dimension": matrix.shape[0],
        "parity_value_center": approximate["parity_value"],
        "minimum_other_eigenvalue_distance_diagnostic": approximate[
            "minimum_other_eigenvalue_distance"
        ],
        "stationary": stationary,
        "parity_right": parity,
        "parity_left": left_certificate,
        "parity_projector": projector_record,
        "approximate_parity_gram_ball": str(gram_ball),
        "approximate_parity_gram_lower": gram_lower,
        "approximate_parity_gram_upper": gram_upper,
        "left_residual_ball": str(left_residual_ball),
        "center_reduced_inverse_ball": str(center_inverse_ball),
        "perron_projector_two_norm_error_ball": str(
            perron_projector_error_ball
        ),
        "perron_projector_two_norm_error_upper": upper_float(
            perron_projector_error_ball
        ),
        "rank_two_projector_two_norm_error_ball": str(
            rank_two_projector_error_ball
        ),
        "rank_two_projector_two_norm_error_upper": upper_float(
            rank_two_projector_error_ball
        ),
        "deflated_bulk_two_norm_error_ball": str(bulk_error_ball),
        "deflated_bulk_two_norm_error_upper": upper_float(bulk_error_ball),
        "parity_contour": contour.as_dict(),
        "all_channel_gates_green": bool(
            stationary["perron_simple_certified"]
            and parity["right_eigenpair_certified"]
            and left_certificate["left_eigenvector_certified"]
            and contour.rouche_count_one
            and upper_float(rank_two_projector_error_ball) < 1.0e-6
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            fine = exact_repaired_matrix(sigma)
            coarse = exact_coarse_matrix(fine)
            channels = [
                channel_certificate("fine", fine),
                channel_certificate("coarse", coarse),
            ]
            row = {
                "sigma": sigma,
                "fine_dimension": len(fine),
                "channels": channels,
                "all_channels_green": all(
                    channel["all_channel_gates_green"]
                    for channel in channels
                ),
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "sigma": sigma,
                        "fine_dimension": len(fine),
                        "fine_rank_two_error": channels[0][
                            "rank_two_projector_two_norm_error_upper"
                        ],
                        "coarse_rank_two_error": channels[1][
                            "rank_two_projector_two_norm_error_upper"
                        ],
                        "elapsed_seconds": sum(
                            channel["elapsed_seconds"] for channel in channels
                        ),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    finally:
        ctx.prec = previous_precision
    payload = {
        "status": "rh73_validated_peripheral_rank_two_deflation",
        "precision_bits": PRECISION_BITS,
        "parity_contour_radius": PARITY_CONTOUR_RADIUS,
        "rows": rows,
        "all_executed_channels_green": all(
            row["all_channels_green"] for row in rows
        ),
        "theorem_boundary": {
            "stationary_left_vector_validated": True,
            "perron_simple_validated": True,
            "negative_parity_eigenpair_validated": True,
            "parity_contour_count_one": True,
            "rank_two_projector_validated": True,
            "deflated_bulk_error_enclosed": True,
            "source_observation_transfer_validated": False,
            "augmented_hardy_bridge_executed": False,
            "stage_A1_closed": False,
        },
        "route_consequence": (
            "The exact stochastic repaired fine/coarse matrices now have "
            "validated Perron and parity rank-two deflations. The remaining "
            "finite-scale upstream task is to propagate these factor balls "
            "through normalized source/observation construction and execute "
            "the augmented Hardy difference bridge."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "row_count": len(rows),
                "all_green": payload["all_executed_channels_green"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
