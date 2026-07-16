"""Certify a three-point numerical-range obstruction for the lifted operator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from flint import acb, arb, arb_mat, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
sys.path[:0] = [
    str(ROOT / "src"),
    str(ROOT / "experiments"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from outward_residuals import (  # noqa: E402
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
    componentwise_add,
    componentwise_dense_exact_matmul,
    componentwise_matmul,
    componentwise_scalar_multiply,
    componentwise_subtract,
)
from run_resolvent_pilot import tightest_arc  # noqa: E402


def exact_norm_ball(values: np.ndarray) -> arb:
    vector = np.asarray(values).reshape(-1)
    total = arb(0)
    for value in vector:
        real = arb(float(np.real(value)))
        imag = arb(float(np.imag(value)))
        total += real * real + imag * imag
    return total.sqrt()


def scalar_ball_to_acb(ball: ComponentwiseBall) -> acb:
    center = complex(np.asarray(ball.center).reshape(-1)[0])
    radius = float(np.asarray(ball.radius).reshape(-1)[0])
    return acb(arb(center.real, radius), arb(center.imag, radius))


def interval_pair(value: arb) -> tuple[float, float]:
    return (
        float(np.nextafter(float(value.lower()), -np.inf)),
        float(np.nextafter(float(value.upper()), np.inf)),
    )


def main() -> None:
    sigma = 1.0e-2
    setting = rh24.physical_settings()[sigma]
    arc = tightest_arc(sigma)
    point = complex(float(arc["center_real"]), float(arc["center_imag"]))
    environment = rh25_global.add_adjoint_actions(
        rh25_global.build_environment(sigma, setting)
    )
    spectrum = environment["spectrum"]
    graph = ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )
    triplet = np.load(
        ROOT / "results" / "triplets" / "dangerous_triplet_sigma_1e-02.npz"
    )
    witness = np.load(ROOT / "results" / "compressed_numerical_range_witness.npz")
    singular = float(triplet["singular_value"][0])
    left = np.asarray(triplet["left"])
    right = np.asarray(triplet["right"])
    vectors = np.asarray(witness["witnesses"])

    previous_precision = ctx.prec
    ctx.prec = 192
    try:
        left_norm = exact_norm_ball(left)
        right_norm = exact_norm_ball(right)
        points: list[acb] = []
        for column in range(vectors.shape[1]):
            vector = np.asarray(vectors[:, column])
            vector_ball = ComponentwiseBall.exact(vector[:, None])
            shifted = componentwise_subtract(
                componentwise_scalar_multiply(point, vector_ball),
                graph.action(vector_ball),
            )
            row = vector.conj()[None, :]
            direct = componentwise_dense_exact_matmul(row, shifted)
            left_dot = componentwise_dense_exact_matmul(
                row, ComponentwiseBall.exact(left[:, None])
            )
            right_dot = componentwise_dense_exact_matmul(
                right.conj()[None, :], vector_ball
            )
            rank_product = componentwise_matmul(left_dot, right_dot)
            rank_product = componentwise_scalar_multiply(
                1.0 - singular, rank_product
            )
            vector_norm = exact_norm_ball(vector)
            direct_value = scalar_ball_to_acb(direct) / (vector_norm * vector_norm)
            rank_value = scalar_ball_to_acb(rank_product) / (
                vector_norm * vector_norm * left_norm * right_norm
            )
            points.append(direct_value + rank_value)

        matrix = arb_mat(
            [
                [value.real for value in points],
                [value.imag for value in points],
                [arb(1), arb(1), arb(1)],
            ]
        )
        source = arb_mat([[arb(0)], [arb(0)], [arb(1)]])
        weights = matrix.solve(source)
        point_intervals = [
            {
                "real_lower": interval_pair(value.real)[0],
                "real_upper": interval_pair(value.real)[1],
                "imag_lower": interval_pair(value.imag)[0],
                "imag_upper": interval_pair(value.imag)[1],
            }
            for value in points
        ]
        weight_intervals = [
            {
                "lower": interval_pair(weights[index, 0])[0],
                "upper": interval_pair(weights[index, 0])[1],
            }
            for index in range(3)
        ]
        minimum_weight_lower = min(row["lower"] for row in weight_intervals)
        result = {
            "sigma": sigma,
            "dimension": int(setting["dimension"]),
            "spectral_parameter_real": point.real,
            "spectral_parameter_imag": point.imag,
            "lift": 1.0,
            "stored_singular_scalar": singular,
            "point_intervals": point_intervals,
            "weight_intervals": weight_intervals,
            "minimum_weight_lower": minimum_weight_lower,
            "strict_origin_in_convex_hull_certified": int(minimum_weight_lower > 0.0),
            "precision_bits": int(ctx.prec),
        }
    finally:
        ctx.prec = previous_precision

    output = ROOT / "results" / "certified_numerical_range_witness.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
