#!/usr/bin/env python3
"""Numerical Gram/window stress test for the TPC-238 theorem."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from math import gcd
from typing import Any

import numpy as np


class StressFailure(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise StressFailure(message)


def rationals(height: int) -> list[Fraction]:
    values = [
        Fraction(numerator, denominator)
        for denominator in range(1, height + 1)
        for numerator in range(denominator)
        if gcd(numerator, denominator) == 1
    ]
    values.sort()
    demand(len(values) == len(set(values)), "duplicate reduced fraction")
    return values


def window_weights(start: int, length: int) -> np.ndarray:
    order = (length + 1) // 2
    center = start + order - 1
    return np.asarray(
        [
            max(0.0, 1.0 - abs(integer - center) / order)
            for integer in range(start, start + length)
        ],
        dtype=np.float64,
    )


def matrix_for(
    frequencies: list[Fraction],
    start: int,
    length: int,
    weighted: bool,
) -> np.ndarray:
    frequency_array = np.asarray(
        [float(frequency) for frequency in frequencies], dtype=np.float64
    )
    integers = np.arange(start, start + length, dtype=np.float64)
    vectors = np.exp(2j * math.pi * np.outer(integers, frequency_array))
    if weighted:
        weights = window_weights(start, length)
        matrix = vectors.conj().T @ (weights[:, None] * vectors)
    else:
        matrix = vectors.conj().T @ vectors
    return (matrix + matrix.conj().T) / 2.0


def stress() -> dict[str, Any]:
    parameter_grid = [(2, 9), (3, 25), (4, 41), (5, 81)]
    starts = [-31, 0, 7, 1003]
    total_windows = 0
    smallest_theorem_margin = math.inf
    smallest_minorant_margin = math.inf
    largest_translation_drift = 0.0
    minimum_normalized_hard_frame = math.inf
    maximum_frequency_count = 0

    for height, length in parameter_grid:
        frequencies = rationals(height)
        maximum_frequency_count = max(maximum_frequency_count, len(frequencies))
        order = (length + 1) // 2
        theorem_lower = max(
            0.0, order - math.pi * math.pi * height**4 / (12.0 * order)
        )
        normalized_lower = max(
            0.0, 0.5 - math.pi * math.pi * height**4 / (6.0 * length**2)
        )
        hard_reference: np.ndarray | None = None
        weighted_reference: np.ndarray | None = None

        for start in starts:
            weights = window_weights(start, length)
            demand(np.min(weights) >= -1.0e-15, "negative triangular weight")
            demand(np.max(weights) <= 1.0 + 1.0e-15, "weight above one")
            demand(
                abs(float(np.sum(weights)) - order) < 1.0e-12,
                "triangular mass",
            )
            weighted_matrix = matrix_for(
                frequencies, start, length, weighted=True
            )
            hard_matrix = matrix_for(frequencies, start, length, weighted=False)
            weighted_eigenvalues = np.linalg.eigvalsh(weighted_matrix)
            hard_eigenvalues = np.linalg.eigvalsh(hard_matrix)
            weighted_minimum = float(weighted_eigenvalues[0])
            hard_minimum = float(hard_eigenvalues[0])
            theorem_margin = weighted_minimum - theorem_lower
            minorant_margin = hard_minimum - weighted_minimum
            demand(theorem_margin >= -5.0e-9, "theorem stress failure")
            demand(minorant_margin >= -5.0e-9, "minorant stress failure")
            demand(
                hard_minimum / length + 5.0e-9 >= normalized_lower,
                "normalized theorem stress failure",
            )
            smallest_theorem_margin = min(
                smallest_theorem_margin, theorem_margin
            )
            smallest_minorant_margin = min(
                smallest_minorant_margin, minorant_margin
            )
            minimum_normalized_hard_frame = min(
                minimum_normalized_hard_frame, hard_minimum / length
            )
            if hard_reference is None:
                hard_reference = hard_eigenvalues
                weighted_reference = weighted_eigenvalues
            else:
                hard_drift = float(
                    np.max(np.abs(hard_eigenvalues - hard_reference))
                )
                weighted_drift = float(
                    np.max(np.abs(weighted_eigenvalues - weighted_reference))
                )
                largest_translation_drift = max(
                    largest_translation_drift, hard_drift, weighted_drift
                )
                demand(hard_drift < 5.0e-8, "hard translation drift")
                demand(weighted_drift < 5.0e-8, "weighted translation drift")
            total_windows += 1

    return {
        "TPC238_GRAM_WINDOW_STRESS": "PASS",
        "classification": "NUMERICALLY_CERTIFIED_FINITE_CHECK",
        "largest_translation_spectral_drift": float(
            f"{largest_translation_drift:.12g}"
        ),
        "maximum_frequency_count": maximum_frequency_count,
        "minimum_hard_normalized_frame_observed": float(
            f"{minimum_normalized_hard_frame:.12g}"
        ),
        "parameter_sets": len(parameter_grid),
        "smallest_hard_minus_triangular_margin": float(
            f"{smallest_minorant_margin:.12g}"
        ),
        "smallest_triangular_minus_theorem_margin": float(
            f"{smallest_theorem_margin:.12g}"
        ),
        "windows": total_windows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(stress(), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StressFailure as error:
        raise SystemExit(f"TPC238_GRAM_WINDOW_STRESS=FAIL: {error}")
