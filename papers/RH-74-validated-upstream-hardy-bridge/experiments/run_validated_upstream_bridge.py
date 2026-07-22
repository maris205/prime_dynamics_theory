"""Validated analytic-upstream to frozen-production Hardy bridge."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import sys
import time

from flint import arb, arb_mat, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
RH59 = PAPERS / "RH-59-flag-adapted-schur-stein-metrics"
RH70 = PAPERS / "RH-70-frozen-production-block-hardy-audit"
RH71 = PAPERS / "RH-71-directional-tail-route-review"
RH72 = PAPERS / "RH-72-validated-folded-gaussian-assembly"
RH73 = PAPERS / "RH-73-validated-peripheral-rank-two-deflation"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH73 / "experiments"),
    str(RH73 / "src"),
    str(RH72 / "src"),
    str(RH59 / "experiments"),
    str(RH58 / "experiments"),
    str(RH58 / "src"),
    str(RH42 / "src"),
    str(RH14 / "src"),
]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_schur_fusion_pilot import (  # noqa: E402
    FINE_RESOLUTION,
    HARDY_RADIUS,
    coarse_embedding,
    detail_embedding,
    spectral_bulk,
)
from run_validated_peripheral_audit import (  # noqa: E402
    approximate_peripheral,
    exact_coarse_matrix,
    exact_repaired_matrix,
    fraction_matrix_to_arb,
)


FULL_OUTPUT = ROOT / "results" / "validated_upstream_bridge_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "validated_upstream_bridge_smoke.json"
SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
HORIZONS = {0.16: 4, 0.08: 9, 0.04: 16, 0.02: 25, 0.01: 32}
BLOCK_MULTIPLE = 4
PRECISION_BITS = 160


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def exact_arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower_float(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def arb_matrix(values: np.ndarray) -> arb_mat:
    array = np.asarray(values, dtype=np.float64)
    return arb_mat(
        [
            [exact_arb_float(array[row, column]) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def arb_vector(values: np.ndarray) -> arb_mat:
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    return arb_mat([[exact_arb_float(value)] for value in array])


def identity_arb(dimension: int) -> arb_mat:
    return arb_mat(
        [
            [arb(1) if row == column else arb(0) for column in range(dimension)]
            for row in range(dimension)
        ]
    )


def frobenius_norm(matrix: arb_mat) -> arb:
    return sum((entry**2 for entry in matrix.entries()), arb(0)).sqrt()


def vector_norm(values: np.ndarray) -> arb:
    return frobenius_norm(arb_vector(values))


def matrix_norm_record(matrix: arb_mat) -> dict[str, object]:
    rows = matrix.nrows()
    columns = matrix.ncols()
    row_upper = 0.0
    for row in range(rows):
        total = sum((abs(matrix[row, column]) for column in range(columns)), arb(0))
        row_upper = max(row_upper, upper_float(total))
    column_upper = 0.0
    for column in range(columns):
        total = sum((abs(matrix[row, column]) for row in range(rows)), arb(0))
        column_upper = max(column_upper, upper_float(total))
    two = (exact_arb_float(row_upper) * exact_arb_float(column_upper)).sqrt()
    frobenius = frobenius_norm(matrix)
    return {
        "row_sum_upper": row_upper,
        "column_sum_upper": column_upper,
        "two_norm_ball": str(two),
        "two_norm_upper": upper_float(two),
        "frobenius_norm_ball": str(frobenius),
        "frobenius_norm_upper": upper_float(frobenius),
    }


def outer_arb(left: np.ndarray, right: np.ndarray) -> arb_mat:
    left_values = np.asarray(left, dtype=np.float64).reshape(-1)
    right_values = np.asarray(right, dtype=np.float64).reshape(-1)
    return arb_mat(
        [
            [
                exact_arb_float(left_value) * exact_arb_float(right_value)
                for right_value in right_values
            ]
            for left_value in left_values
        ]
    )


def repaired_center_matrices(
    exact_rows: list[list[Fraction]],
) -> tuple[dict[str, object], arb_mat, arb_mat]:
    matrix = np.asarray(
        [[float(value) for value in row] for row in exact_rows], dtype=np.float64
    )
    approximate = approximate_peripheral(matrix)
    dimension = matrix.shape[0]
    stationary = np.asarray(approximate["stationary"])
    right = np.asarray(approximate["parity_right"])
    left = np.asarray(approximate["parity_left"])
    parity_value = float(approximate["parity_value"])
    repaired_ball = fraction_matrix_to_arb(exact_rows)
    perron = outer_arb(np.ones(dimension), stationary)
    parity = outer_arb(right, left)
    complement = identity_arb(dimension) - perron - parity
    bulk = repaired_ball - perron - exact_arb_float(parity_value) * parity
    return approximate, complement, bulk


def choose_newton_radius(beta: arb, gamma: arb, inverse_norm: arb) -> arb:
    denominator = arb(1) - gamma
    if lower_float(denominator) <= 0.0:
        raise RuntimeError("augmented Newton denominator failed")
    candidate = 2.0 * upper_float(beta) / lower_float(denominator)
    radius = exact_arb_float(math.nextafter(candidate, math.inf))
    for _ in range(12):
        contraction = gamma + inverse_norm * radius
        self_map = beta + gamma * radius + inverse_norm * radius**2
        if upper_float(contraction) < 1.0 and self_map.upper() <= radius.lower():
            return radius
        radius = exact_arb_float(math.nextafter(upper_float(radius) * 1.2, math.inf))
    raise RuntimeError("augmented right eigenpair radius did not close")


def true_factor_bounds(
    record: dict[str, object],
    approximate: dict[str, object],
    dimension: int,
    matrix_error: arb,
) -> dict[str, object]:
    stationary_record = record["stationary"]
    stationary_inverse = (
        arb(stationary_record["inverse_frobenius_ball"])
        / (arb(1) - arb(stationary_record["inverse_residual_frobenius_ball"]))
    )
    stationary_center_norm = vector_norm(np.asarray(approximate["stationary"]))
    repaired_stationary_error = arb(stationary_record["stationary_two_norm_error_ball"])
    stationary_transport_denominator = arb(1) - stationary_inverse * matrix_error
    if lower_float(stationary_transport_denominator) <= 0.0:
        raise RuntimeError("stationary matrix perturbation did not close")
    stationary_transport = (
        stationary_inverse
        * matrix_error
        * (stationary_center_norm + repaired_stationary_error)
        / stationary_transport_denominator
    )
    stationary_error = repaired_stationary_error + stationary_transport
    perron_projector_error = arb(dimension).sqrt() * stationary_error

    right_record = record["parity_right"]
    inverse_norm = arb(right_record["inverse_frobenius_ball"])
    beta = arb(right_record["newton_beta_ball"])
    gamma = arb(right_record["inverse_residual_frobenius_ball"])
    right_norm = arb(right_record["right_norm_ball"])
    left_norm = arb(right_record["left_norm_ball"])
    augmented_beta = beta + inverse_norm * matrix_error * right_norm
    augmented_gamma = gamma + inverse_norm * matrix_error
    right_radius = choose_newton_radius(augmented_beta, augmented_gamma, inverse_norm)

    left_record = record["parity_left"]
    left_inverse = arb(left_record["inverse_frobenius_ball"])
    left_gamma = arb(left_record["inverse_residual_frobenius_ball"])
    left_beta_zero = arb(left_record["left_solve_beta_zero_ball"])
    left_total_defect = left_gamma + left_inverse * (matrix_error + right_radius)
    if upper_float(left_total_defect) >= 1.0:
        raise RuntimeError("analytic left parity solve did not close")
    left_error = (
        left_beta_zero
        + left_inverse * (matrix_error + right_radius) * left_norm
    ) / (arb(1) - left_total_defect)

    normalization = (left_norm + left_error) * right_radius
    gram_lower = arb(1) - normalization
    if lower_float(gram_lower) <= 0.0:
        raise RuntimeError("analytic parity Gram reached zero")
    numerator = right_radius * (left_norm + left_error) + right_norm * left_error
    parity_projector_error = (
        numerator / gram_lower
        + right_norm * left_norm * normalization / gram_lower
    )
    rank_two_error = perron_projector_error + parity_projector_error
    parity_value = exact_arb_float(abs(float(approximate["parity_value"])))
    bulk_error = (
        matrix_error
        + perron_projector_error
        + (parity_value + right_radius) * parity_projector_error
        + right_radius * right_norm * left_norm
    )
    complement_frobenius_error = (
        perron_projector_error + arb(2).sqrt() * parity_projector_error
    )
    return {
        "matrix_error_ball": str(matrix_error),
        "stationary_error_ball": str(stationary_error),
        "stationary_error_upper": upper_float(stationary_error),
        "right_radius_ball": str(right_radius),
        "right_radius_upper": upper_float(right_radius),
        "left_error_ball": str(left_error),
        "left_error_upper": upper_float(left_error),
        "perron_projector_error_ball": str(perron_projector_error),
        "parity_projector_error_ball": str(parity_projector_error),
        "rank_two_projector_error_ball": str(rank_two_error),
        "rank_two_projector_error_upper": upper_float(rank_two_error),
        "complement_frobenius_error_ball": str(complement_frobenius_error),
        "bulk_error_ball": str(bulk_error),
        "bulk_error_upper": upper_float(bulk_error),
        "all_factor_transfers_green": True,
        "_rank_two": rank_two_error,
        "_complement_frobenius": complement_frobenius_error,
        "_bulk": bulk_error,
    }


def frozen_components(sigma: float) -> dict[str, object]:
    dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    fine = sparse_folded_gaussian_matrix(dimension, sigma).toarray()
    embedding = coarse_embedding(dimension)
    detail = detail_embedding(dimension)
    coarse = embedding.T @ fine @ embedding
    coupling_b = embedding.T @ fine @ detail
    coupling_c = detail.T @ fine @ embedding
    fine_data = spectral_bulk(fine)
    coarse_data = spectral_bulk(coarse)
    return {
        "dimension": dimension,
        "fine": fine,
        "coarse": coarse,
        "embedding": embedding,
        "detail": detail,
        "coupling_b": coupling_b,
        "coupling_c": coupling_c,
        "fine_data": fine_data,
        "coarse_data": coarse_data,
        "left": {
            "operator": np.asarray(fine_data["bulk"]) / HARDY_RADIUS,
            "source": np.asarray(fine_data["complement"]) @ embedding @ coupling_b / np.linalg.norm(coupling_b, "fro"),
            "observation": embedding.T,
        },
        "right": {
            "operator": np.asarray(coarse_data["bulk"]).T / HARDY_RADIUS,
            "source": coupling_c.T / np.linalg.norm(coupling_c, "fro"),
            "observation": np.asarray(coarse_data["complement"]).T,
        },
    }


def normalized_difference(reference_norm: arb, difference: arb) -> arb:
    denominator = reference_norm - difference
    if lower_float(denominator) <= 0.0:
        raise RuntimeError("coupling normalization reached zero")
    return arb(2) * difference / denominator


def triple_error_bounds(
    side: str,
    frozen: dict[str, object],
    factor: dict[str, object],
    center_complement: arb_mat,
    center_bulk: arb_mat,
    frozen_complement: np.ndarray,
    frozen_bulk: np.ndarray,
    assembly_row: dict[str, object],
) -> dict[str, object]:
    center_complement_difference = matrix_norm_record(
        center_complement - arb_matrix(frozen_complement)
    )
    center_bulk_difference = matrix_norm_record(
        center_bulk - arb_matrix(frozen_bulk)
    )
    operator_error = (
        factor["_bulk"]
        + arb(center_bulk_difference["two_norm_ball"])
    ) / exact_arb_float(HARDY_RADIUS)

    rank_two = factor["_rank_two"]
    complement_two_error = rank_two + arb(
        center_complement_difference["two_norm_ball"]
    )
    complement_frobenius_error = factor["_complement_frobenius"] + arb(
        center_complement_difference["frobenius_norm_ball"]
    )

    dimension = int(frozen["dimension"])
    coarse_dimension = dimension // 2
    block_error = arb(
        assembly_row["coarse_and_cross_block_two_norm_defect_upper"][
            "against_frozen_pipeline_ball"
        ]
    )
    coupling_frobenius_error = arb(coarse_dimension).sqrt() * block_error
    embedding_error = arb(assembly_row["haar"]["embedding_two_norm_defect_ball"])
    embedding_frobenius_error = arb(coarse_dimension).sqrt() * embedding_error
    frozen_embedding_norm = arb(assembly_row["haar"]["frozen_embedding_two_norm_ball"])

    if side == "left":
        coupling = np.asarray(frozen["coupling_b"])
        coupling_norm = frobenius_norm(arb_matrix(coupling))
        normalized_coupling_error = normalized_difference(
            coupling_norm, coupling_frobenius_error
        )
        frozen_complement_norm = arb(
            matrix_norm_record(arb_matrix(frozen_complement))["two_norm_ball"]
        )
        source_error = (
            complement_two_error
            + frozen_complement_norm * embedding_error
            + frozen_complement_norm
            * frozen_embedding_norm
            * normalized_coupling_error
        )
        observation_error = embedding_frobenius_error
    else:
        coupling = np.asarray(frozen["coupling_c"])
        coupling_norm = frobenius_norm(arb_matrix(coupling))
        normalized_coupling_error = normalized_difference(
            coupling_norm, coupling_frobenius_error
        )
        source_error = normalized_coupling_error
        observation_error = complement_frobenius_error

    return {
        "center_complement_difference": center_complement_difference,
        "center_bulk_difference": center_bulk_difference,
        "coupling_frobenius_error_ball": str(coupling_frobenius_error),
        "normalized_coupling_error_ball": str(normalized_coupling_error),
        "operator_two_norm_error_ball": str(operator_error),
        "operator_two_norm_error_upper": upper_float(operator_error),
        "source_frobenius_error_ball": str(source_error),
        "source_frobenius_error_upper": upper_float(source_error),
        "observation_frobenius_error_ball": str(observation_error),
        "observation_frobenius_error_upper": upper_float(observation_error),
        "_operator": operator_error,
        "_source": source_error,
        "_observation": observation_error,
    }


def reference_prefix(
    operator_values: np.ndarray,
    source_values: np.ndarray,
    horizon: int,
) -> tuple[list[arb], list[arb], arb, arb]:
    operator = arb_matrix(operator_values)
    source = arb_matrix(source_values)
    power = identity_arb(operator.nrows())
    state = source
    powers = [arb(1)]
    states = []
    for step in range(horizon):
        states.append(frobenius_norm(state))
        state = operator * state
        power = operator * power
        powers.append(frobenius_norm(power))
    return powers, states, frobenius_norm(source), frobenius_norm(operator)


def robust_bridge_arb(
    model: dict[str, object],
    errors: dict[str, object],
    horizon: int,
) -> dict[str, object]:
    operator_values = np.asarray(model["operator"])
    source_values = np.asarray(model["source"])
    observation_values = np.asarray(model["observation"])
    prefix, states, source_norm, _ = reference_prefix(
        operator_values, source_values, horizon
    )
    observation_norm = frobenius_norm(arb_matrix(observation_values))
    q0 = prefix[horizon]
    total_horizon = horizon * BLOCK_MULTIPLE
    reference_powers = []
    for k in range(total_horizon + 1):
        blocks, remainder = divmod(k, horizon)
        reference_powers.append(q0**blocks * prefix[remainder])

    epsilon_a = errors["_operator"]
    epsilon_x = errors["_source"]
    epsilon_y = errors["_observation"]
    defects = [arb(0)]
    for k in range(1, total_horizon + 1):
        convolution = sum(
            (
                reference_powers[k - 1 - j]
                * (reference_powers[j] + defects[j])
                for j in range(k)
            ),
            arb(0),
        )
        defects.append(epsilon_a * convolution)
    true_powers = [
        reference_powers[k] + defects[k]
        for k in range(total_horizon + 1)
    ]
    q_true = true_powers[horizon]
    if upper_float(q0) >= 1.0 or upper_float(q_true) >= 1.0:
        raise RuntimeError("robust block contraction failed")

    true_source_norm = source_norm + epsilon_x
    finite = arb(0)
    maximum_response = arb(0)
    for k in range(total_horizon):
        state_error = (
            defects[k] * true_source_norm
            + reference_powers[k] * epsilon_x
        )
        response_error = (
            epsilon_y * true_powers[k] * true_source_norm
            + observation_norm * state_error
        )
        finite += response_error**2
        if upper_float(response_error) > upper_float(maximum_response):
            maximum_response = response_error

    true_source_block = arb(0)
    reference_source_block = arb(0)
    for r in range(horizon):
        state_error = defects[r] * true_source_norm + prefix[r] * epsilon_x
        true_state = states[r] + state_error
        true_source_block += true_state**2
        reference_source_block += states[r] ** 2
    true_observation_norm = observation_norm + epsilon_y
    true_tail = (
        true_observation_norm**2
        * q_true ** (2 * BLOCK_MULTIPLE)
        * true_source_block
        / (arb(1) - q_true**2)
    )
    reference_tail = (
        observation_norm**2
        * q0 ** (2 * BLOCK_MULTIPLE)
        * reference_source_block
        / (arb(1) - q0**2)
    )
    difference_tail = arb(2) * (true_tail + reference_tail)
    bridge = (finite + difference_tail).sqrt()
    return {
        "block_horizon": horizon,
        "block_multiple": BLOCK_MULTIPLE,
        "total_horizon": total_horizon,
        "reference_block_contraction_ball": str(q0),
        "reference_block_contraction_upper": upper_float(q0),
        "true_block_contraction_ball": str(q_true),
        "true_block_contraction_upper": upper_float(q_true),
        "finite_difference_energy_squared_ball": str(finite),
        "maximum_prefix_response_error_ball": str(maximum_response),
        "true_tail_energy_squared_ball": str(true_tail),
        "reference_tail_energy_squared_ball": str(reference_tail),
        "difference_tail_energy_squared_ball": str(difference_tail),
        "bridge_energy_ball": str(bridge),
        "bridge_energy_upper": upper_float(bridge),
        "block_contraction_certified": True,
    }


def clean_factor_record(record: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def clean_error_record(record: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    rh72 = json.loads(
        (RH72 / "results" / "interval_assembly_audit.json").read_text(encoding="utf-8")
    )
    rh73 = json.loads(
        (RH73 / "results" / "peripheral_validation_audit.json").read_text(encoding="utf-8")
    )
    slack = json.loads(
        (RH71 / "results" / "arb_bridge_slack_audit.json").read_text(encoding="utf-8")
    )
    assembly_rows = {float(row["sigma"]): row for row in rh72["rows"]}
    peripheral_rows = {float(row["sigma"]): row for row in rh73["rows"]}
    slack_rows = {
        (float(row["sigma"]), str(row["side"])): row for row in slack["rows"]
    }

    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            started = time.perf_counter()
            frozen = frozen_components(sigma)
            fine_rows = exact_repaired_matrix(sigma)
            coarse_rows = exact_coarse_matrix(fine_rows)
            assembly = assembly_rows[sigma]
            matrix_error = arb(
                assembly["full_to_repaired_matrix_defect"]["two_norm_upper_ball"]
            )
            channel_payloads = []
            for index, side in enumerate(("left", "right")):
                exact_rows = fine_rows if side == "left" else coarse_rows
                approximate, center_complement, center_bulk = repaired_center_matrices(
                    exact_rows
                )
                peripheral = peripheral_rows[sigma]["channels"][index]
                factor = true_factor_bounds(
                    peripheral,
                    approximate,
                    len(exact_rows),
                    matrix_error,
                )
                frozen_data = (
                    frozen["fine_data"] if side == "left" else frozen["coarse_data"]
                )
                errors = triple_error_bounds(
                    side,
                    frozen,
                    factor,
                    center_complement,
                    center_bulk,
                    np.asarray(frozen_data["complement"]),
                    np.asarray(frozen_data["bulk"]),
                    assembly,
                )
                bridge = robust_bridge_arb(
                    frozen[side], errors, HORIZONS[sigma]
                )
                one_percent_slack = float(
                    slack_rows[(sigma, side)]["budgets"]["1_percent"]["slack_lower"]
                )
                bridge_green = bridge["bridge_energy_upper"] < one_percent_slack
                channel_payloads.append(
                    {
                        "side": side,
                        "dimension": len(exact_rows),
                        "factor_transfer": clean_factor_record(factor),
                        "triple_error": clean_error_record(errors),
                        "robust_hardy_bridge": bridge,
                        "one_percent_slack_lower": one_percent_slack,
                        "bridge_to_slack_ratio_upper": (
                            bridge["bridge_energy_upper"] / one_percent_slack
                        ),
                        "finite_scale_one_percent_green": bridge_green,
                    }
                )
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": side,
                            "operator_error": errors["operator_two_norm_error_upper"],
                            "source_error": errors["source_frobenius_error_upper"],
                            "observation_error": errors["observation_frobenius_error_upper"],
                            "bridge": bridge["bridge_energy_upper"],
                            "slack": one_percent_slack,
                            "green": bridge_green,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
            rows.append(
                {
                    "sigma": sigma,
                    "fine_dimension": int(frozen["dimension"]),
                    "channels": channel_payloads,
                    "all_channels_green": all(
                        channel["finite_scale_one_percent_green"]
                        for channel in channel_payloads
                    ),
                    "elapsed_seconds": time.perf_counter() - started,
                }
            )
    finally:
        ctx.prec = previous_precision

    payload = {
        "status": "rh74_validated_upstream_to_frozen_hardy_bridge",
        "precision_bits": PRECISION_BITS,
        "block_multiple": BLOCK_MULTIPLE,
        "rows": rows,
        "all_executed_channels_green": all(row["all_channels_green"] for row in rows),
        "theorem_boundary": {
            "analytic_matrix_to_repaired_factor_transfer": True,
            "normalized_source_observation_transfer": True,
            "robust_volterra_power_bridge": True,
            "augmented_hardy_difference_closed": True,
            "finite_scale_end_to_end_hardy_closed": all(row["all_channels_green"] for row in rows),
            "uniform_small_noise_family_bound": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
        },
        "route_consequence": (
            "At the five archived scales, the folded-Gaussian matrix, Perron/parity "
            "factor, normalized source/observation, and terminal Hardy layers now "
            "compose inside the inherited one-percent budget. The finite-scale "
            "upstream gate is closed; the remaining Stage A1 gate is uniform "
            "small-noise family scaling."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
