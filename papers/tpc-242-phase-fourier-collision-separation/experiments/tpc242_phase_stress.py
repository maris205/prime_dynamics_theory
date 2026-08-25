#!/usr/bin/env python3
"""Exhaustive bounded Gaussian-integer illustration for TPC-242."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import product


CLASSIFICATION = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, Gaussian]


class StressFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise StressFailure(message)


def add(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] + b[0], a[1] + b[1])


def multiply(a: Gaussian, b: Gaussian) -> Gaussian:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conjugate(a: Gaussian) -> Gaussian:
    return (a[0], -a[1])


def ipow(exponent: int) -> Gaussian:
    require(type(exponent) is int, "phase type")
    return (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(-1)),
    )[exponent % 4]


def inner(first: Vector, second: Vector) -> Gaussian:
    total = (Fraction(0), Fraction(0))
    for left, right in zip(first, second):
        total = add(total, multiply(conjugate(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    result = inner(value, value)
    require(result[1] == 0 and result[0] >= 0, "norm")
    return result[0]


def energy(x_value: Vector, y_value: Vector, j: int) -> Fraction:
    phase = ipow(j)
    combined = tuple(add(xc, multiply(phase, yc)) for xc, yc in zip(x_value, y_value))
    require(len(combined) == 2, "dimension")
    return norm_sq(combined)  # type: ignore[arg-type]


def dft(values: list[Fraction]) -> list[Gaussian]:
    result: list[Gaussian] = []
    for k in range(4):
        total = (Fraction(0), Fraction(0))
        for j, value in enumerate(values):
            total = add(total, multiply(ipow(k * j), (value, Fraction(0))))
        result.append((total[0] / 4, total[1] / 4))
    return result


def census() -> None:
    components = [
        (Fraction(real), Fraction(imag))
        for real in range(-1, 2)
        for imag in range(-1, 2)
    ]
    vectors: list[Vector] = [(a, b) for a, b in product(components, repeat=2)]
    ordered_pairs = 0
    phase_evaluations = 0
    zero_second_modes = 0
    offset = Fraction(7, 3)
    offset_delta = dft([offset] * 4)
    require(offset_delta == [
        (offset, Fraction(0)),
        (Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0)),
    ], "common offset")
    for x_value in vectors:
        for y_value in vectors:
            energies = [energy(x_value, y_value, j) for j in range(4)]
            spectrum = dft(energies)
            nx = norm_sq(x_value)
            ny = norm_sq(y_value)
            selected = inner(y_value, x_value)
            conjugate_selected = inner(x_value, y_value)
            require(spectrum == [
                (nx + ny, Fraction(0)), selected,
                (Fraction(0), Fraction(0)), conjugate_selected,
            ], "complete C4 spectrum")
            selected_sq = selected[0] ** 2 + selected[1] ** 2
            gram = nx * ny - selected_sq
            lhs = (nx + ny) ** 2 - 4 * selected_sq
            rhs = (nx - ny) ** 2 + 4 * gram
            require(gram >= 0 and lhs == rhs and 4 * selected_sq <= (nx + ny) ** 2,
                    "disk/defect")
            ordered_pairs += 1
            phase_evaluations += 4
            if spectrum[2] == (Fraction(0), Fraction(0)):
                zero_second_modes += 1
    require(ordered_pairs == len(vectors) ** 2 and zero_second_modes == ordered_pairs,
            "census coverage")
    payload = {
        "classification": CLASSIFICATION,
        "component_bound": 1,
        "dimension": 2,
        "gaussian_components": len(components),
        "ordered_pairs": ordered_pairs,
        "phase_evaluations": phase_evaluations,
        "status": "PASS",
        "vectors": len(vectors),
        "zero_second_modes": zero_second_modes,
    }
    print("TPC242_PHASE_STRESS=PASS")
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC242_PHASE_STRESS=FAIL: use --check")
    try:
        census()
    except (StressFailure, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC242_PHASE_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
