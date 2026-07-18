"""Floating Gauss--Legendre pilot for continuum Hilbert--Schmidt constants."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import erf, roots_legendre


ROOT = Path(__file__).resolve().parents[1]
CRITICAL_U = 1.543689012692076361570855971801747986525203297650983935240804
SIGMA = 0.01


def gauss_rule(order: int) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = roots_legendre(int(order))
    return (nodes + 1.0) / 2.0, weights / 2.0


def normalizer(mean: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sigma = SIGMA
    root_two = math.sqrt(2.0)
    prefactor = sigma * math.sqrt(math.pi / 2.0)
    left = np.exp(-((1.0 + mean) ** 2) / (2.0 * sigma**2))
    right = np.exp(-((1.0 - mean) ** 2) / (2.0 * sigma**2))
    value = prefactor * (
        erf((1.0 - mean) / (root_two * sigma))
        + erf((1.0 + mean) / (root_two * sigma))
    )
    first = left - right
    second = (
        -(1.0 + mean) * left - (1.0 - mean) * right
    ) / sigma**2
    return value, first, second


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-order", type=int, default=1024)
    parser.add_argument("--y-order", type=int, default=2048)
    parser.add_argument("--chunk", type=int, default=32)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/hilbert_constants_pilot.json"),
    )
    arguments = parser.parse_args()

    x, wx = gauss_rule(arguments.x_order)
    y, wy = gauss_rule(arguments.y_order)
    sigma = SIGMA
    totals = {
        "kernel": 0.0,
        "source_first": 0.0,
        "target_first": 0.0,
        "source_second": 0.0,
        "source_target": 0.0,
        "target_second": 0.0,
    }
    row_kernel_max = 0.0
    row_maxima = {name: 0.0 for name in totals}

    for lower in range(0, x.size, int(arguments.chunk)):
        upper = min(x.size, lower + int(arguments.chunk))
        source = x[lower:upper, None]
        source_weight = wx[lower:upper]
        target = y[None, :]
        mean = 1.0 - CRITICAL_U * source * source
        mean_first = -2.0 * CRITICAL_U * source
        mean_second = -2.0 * CRITICAL_U
        z, zm, zmm = normalizer(mean)

        positive_offset = target - mean
        negative_offset = target + mean
        positive = np.exp(-(positive_offset**2) / (2.0 * sigma**2))
        negative = np.exp(-(negative_offset**2) / (2.0 * sigma**2))
        raw = positive + negative
        raw_m = (
            positive_offset * positive - negative_offset * negative
        ) / sigma**2
        raw_mm = (
            (positive_offset**2 / sigma**4 - 1.0 / sigma**2) * positive
            + (negative_offset**2 / sigma**4 - 1.0 / sigma**2) * negative
        )
        raw_y = -(
            positive_offset * positive + negative_offset * negative
        ) / sigma**2
        raw_yy = raw_mm
        raw_my = (
            (1.0 / sigma**2 - positive_offset**2 / sigma**4) * positive
            + (-1.0 / sigma**2 + negative_offset**2 / sigma**4) * negative
        )

        ratio = zm / z
        kernel = raw / z
        parameter_first = (raw_m - ratio * raw) / z
        parameter_second = (
            raw_mm
            - 2.0 * ratio * raw_m
            - (zmm / z) * raw
            + 2.0 * ratio * ratio * raw
        ) / z
        target_first = raw_y / z
        target_second = raw_yy / z
        parameter_target = (raw_my - ratio * raw_y) / z
        source_first = mean_first * parameter_first
        source_second = (
            mean_first * mean_first * parameter_second
            + mean_second * parameter_first
        )
        source_target = mean_first * parameter_target

        arrays = {
            "kernel": kernel,
            "source_first": source_first,
            "target_first": target_first,
            "source_second": source_second,
            "source_target": source_target,
            "target_second": target_second,
        }
        for name, values in arrays.items():
            row_integrals = np.sum(values * values * wy[None, :], axis=1)
            totals[name] += float(np.sum(row_integrals * source_weight))
            row_maxima[name] = max(
                row_maxima[name], float(np.max(row_integrals))
            )
            if name == "kernel":
                row_kernel_max = row_maxima[name]

    payload = {
        "status": "floating_gauss_legendre_hilbert_constant_pilot",
        "critical_u": CRITICAL_U,
        "sigma": SIGMA,
        "x_order": int(arguments.x_order),
        "y_order": int(arguments.y_order),
        "hilbert_schmidt_norms": {
            name: math.sqrt(value) for name, value in totals.items()
        },
        "maximum_row_L2_norms": {
            name: math.sqrt(value) for name, value in row_maxima.items()
        },
        "kernel_L2_to_Linfinity_upper_pilot": math.sqrt(row_kernel_max),
    }
    output = ROOT / arguments.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
