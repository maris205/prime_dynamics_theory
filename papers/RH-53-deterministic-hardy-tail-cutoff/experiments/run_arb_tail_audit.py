"""Small outward-rounded Arb audit of the block Hardy certificate."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from flint import arb, arb_mat, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_tail_audit.json"


def ball_matrix(values: np.ndarray, radius: float) -> arb_mat:
    array = np.asarray(values, dtype=np.float64)
    return arb_mat(
        [
            [arb(str(array[row, column]), str(radius)) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def identity(dimension: int) -> arb_mat:
    return arb_mat(
        [[1 if row == column else 0 for column in range(dimension)] for row in range(dimension)]
    )


def frobenius_square(matrix: arb_mat) -> arb:
    return sum((entry * entry for entry in matrix.entries()), arb(0))


def spectral_norm_upper(matrix: arb_mat) -> tuple[arb, list[str]]:
    """Return a rigorous Frobenius upper and diagnostic eigenvalue balls."""

    square = matrix * matrix.transpose()
    eigenvalues = square.eig()
    return frobenius_square(matrix).sqrt(), [str(value) for value in eigenvalues]


def main() -> None:
    ctx.prec = 256
    rng = np.random.default_rng(5301)
    dimension = 4
    source_rank = 2
    horizon = 6
    operator = rng.normal(size=(dimension, dimension))
    operator *= 0.52 / max(abs(np.linalg.eigvals(operator)))
    source = rng.normal(size=(dimension, source_rank)) / 3.0
    observation = rng.normal(size=(3, dimension)) / 3.0
    input_radius = 1.0e-30
    a = ball_matrix(operator, input_radius)
    x = ball_matrix(source, input_radius)
    y = ball_matrix(observation, input_radius)

    state = x
    main_sum = arb(0)
    source_gramian = arb_mat(dimension, dimension)
    power = identity(dimension)
    for _ in range(horizon):
        image = y * state
        main_sum += frobenius_square(image)
        source_gramian += state * state.transpose()
        state = a * state
        power = a * power

    q, power_eigenvalues = spectral_norm_upper(power)
    margin = arb(1) - q * q
    if float(margin.lower()) <= 0.0:
        raise RuntimeError("Arb block contraction was not certified")
    residual = power * source_gramian * power.transpose()
    residual_norm, residual_eigenvalues = spectral_norm_upper(residual)
    observation_hs_squared = frobenius_square(y)
    tail = residual_norm * observation_hs_squared / margin
    energy_squared = main_sum + tail
    energy = energy_squared.sqrt()

    payload = {
        "status": "arb_outward_rounded_small_matrix_full_hardy_certificate",
        "evidence_level": "256-bit Arb interval execution",
        "dimension": dimension,
        "source_rank": source_rank,
        "horizon": horizon,
        "input_entry_radius": input_radius,
        "main_energy_squared_ball": str(main_sum),
        "block_power_frobenius_norm_upper_ball": str(q),
        "contraction_margin_ball": str(margin),
        "tail_energy_squared_upper_ball": str(tail),
        "full_energy_squared_upper_ball": str(energy_squared),
        "full_energy_upper_ball": str(energy),
        "block_power_square_eigenvalue_balls": power_eigenvalues,
        "tail_residual_square_eigenvalue_balls": residual_eigenvalues,
        "norm_note": (
            "Frobenius interval uppers are used in the certificate and therefore "
            "also bound the required spectral norms; eigenvalue balls are diagnostic"
        ),
        "certified_block_contraction": float(q.upper()) < 1.0,
        "arithmetic_scope": (
            "small abstract real matrix with interval input balls; this demonstrates "
            "the outward-rounded algorithm but is not the folded-Gaussian production matrix"
        ),
        "production_matrix_interval_executed": False,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
