#!/usr/bin/env python3
"""Finite exact hard-window stress census for TPC-243."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import product
from math import isqrt


CLASSIFICATION = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
STATUS = "PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER"
ComplexQ = tuple[Fraction, Fraction]
Vector = tuple[ComplexQ, ...]
Matrix = tuple[tuple[ComplexQ, ...], ...]


class StressFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise StressFailure(message)


def c(real: int | Fraction = 0, imag: int | Fraction = 0) -> ComplexQ:
    require(type(real) in (int, Fraction) and type(imag) in (int, Fraction),
            "complex component type")
    return (Fraction(real), Fraction(imag))


def add(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (left[0] + right[0], left[1] + right[1])


def subtract(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (left[0] - right[0], left[1] - right[1])


def multiply(left: ComplexQ, right: ComplexQ) -> ComplexQ:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: ComplexQ) -> ComplexQ:
    return (value[0], -value[1])


def scale(value: ComplexQ, scalar: Fraction) -> ComplexQ:
    require(type(scalar) is Fraction, "scale type")
    return (scalar * value[0], scalar * value[1])


def absolute_square(value: ComplexQ) -> Fraction:
    return value[0] ** 2 + value[1] ** 2


def fourth_root(exponent: int) -> ComplexQ:
    require(type(exponent) is int, "phase exponent")
    return (c(1), c(0, 1), c(-1), c(0, -1))[exponent % 4]


def inner(first: Vector, second: Vector) -> ComplexQ:
    require(len(first) == len(second), "inner-product dimension")
    total = c()
    for left, right in zip(first, second):
        total = add(total, multiply(conjugate(left), right))
    return total


def norm_squared(value: Vector) -> Fraction:
    result = inner(value, value)
    require(result[1] == 0 and result[0] >= 0, "norm")
    return result[0]


def synthesize(coefficients: Vector, start: int, length: int) -> Vector:
    require(len(coefficients) == 4, "coefficient dimension")
    output: list[ComplexQ] = []
    for integer in range(start, start + length):
        value = c()
        for frequency, coefficient in enumerate(coefficients):
            value = add(value, multiply(coefficient, fourth_root(integer * frequency)))
        output.append(value)
    return tuple(output)


def gram(start: int, length: int) -> Matrix:
    rows: list[tuple[ComplexQ, ...]] = []
    for alpha in range(4):
        row: list[ComplexQ] = []
        for beta in range(4):
            value = c()
            for integer in range(start, start + length):
                value = add(value, fourth_root(integer * (beta - alpha)))
            row.append(value)
        rows.append(tuple(row))
    return tuple(rows)


def exact_magnitude(value: ComplexQ) -> Fraction:
    square = absolute_square(value)
    numerator = isqrt(square.numerator)
    denominator = isqrt(square.denominator)
    require(numerator * numerator == square.numerator, "irrational fixture magnitude")
    require(denominator * denominator == square.denominator, "magnitude denominator")
    return Fraction(numerator, denominator)


def maximum_row_mass(matrix: Matrix) -> Fraction:
    masses: list[Fraction] = []
    for row_index, row in enumerate(matrix):
        mass = Fraction(0)
        for column_index, entry in enumerate(row):
            if row_index != column_index:
                mass += exact_magnitude(entry)
        masses.append(mass)
    return max(masses)


def census() -> None:
    delta = Fraction(1, 4)
    harmonic = Fraction(3, 2)
    row_bound = harmonic / delta
    require(row_bound == 6, "row bound")
    intervals = [(-3, 1), (-3, 4), (0, 8), (-3, 17)]
    alphabet = (c(), c(1), c(0, 1))
    vectors: list[Vector] = [tuple(items) for items in product(alphabet, repeat=4)]
    require(len(vectors) == 81, "vector census size")

    quadratic_checks = 0
    row_checks = 0
    maximum_observed_row_mass = Fraction(0)
    for start, length in intervals:
        matrix = gram(start, length)
        require(all(matrix[index][index] == c(length) for index in range(4)),
                "Gram diagonal")
        observed = maximum_row_mass(matrix)
        require(observed <= row_bound, "row bound violation")
        maximum_observed_row_mass = max(maximum_observed_row_mass, observed)
        row_checks += 4
        for vector in vectors:
            image = synthesize(vector, start, length)
            coefficient_energy = norm_squared(vector)
            window_energy = norm_squared(image)
            lower = max(Fraction(0), Fraction(length) - row_bound) * coefficient_energy
            upper = (Fraction(length) + row_bound) * coefficient_energy
            require(lower <= window_energy <= upper, "quadratic frame violation")
            quadratic_checks += 1

    main_start = -3
    main_length = 17
    epsilon = row_bound / main_length
    images = {vector: synthesize(vector, main_start, main_length) for vector in vectors}
    ordered_pairs = 0
    bilinear_checks = 0
    orientation_checks = 0
    orientation_sensitive_pairs = 0
    for z_value in vectors:
        for w_value in vectors:
            coefficient = inner(z_value, w_value)
            window = inner(images[z_value], images[w_value])
            unnormalized_error = subtract(
                window, scale(coefficient, Fraction(main_length))
            )
            bound_squared = (
                row_bound * row_bound * norm_squared(z_value) * norm_squared(w_value)
            )
            require(absolute_square(unnormalized_error) <= bound_squared,
                    "bilinear transfer violation")
            bilinear_checks += 1

            target = inner(w_value, z_value)
            selected = scale(inner(images[w_value], images[z_value]),
                             Fraction(1, main_length))
            selected_error = subtract(selected, target)
            selected_bound = (
                epsilon * epsilon * norm_squared(w_value) * norm_squared(z_value)
            )
            require(absolute_square(selected_error) <= selected_bound,
                    "TPC-242 orientation violation")
            require(selected == conjugate(scale(window, Fraction(1, main_length))),
                    "selected conjugacy")
            if target != coefficient:
                orientation_sensitive_pairs += 1
            orientation_checks += 1
            ordered_pairs += 1

    require(ordered_pairs == len(vectors) ** 2, "ordered-pair coverage")
    require(orientation_sensitive_pairs > 0, "orientation census vacuous")
    payload = {
        "bilinear_checks": bilinear_checks,
        "classification": CLASSIFICATION,
        "coefficient_alphabet": ["0", "1", "i"],
        "frequencies": 4,
        "intervals": len(intervals),
        "maximum_observed_row_mass": str(maximum_observed_row_mass),
        "ordered_pairs": ordered_pairs,
        "orientation_checks": orientation_checks,
        "orientation_sensitive_pairs": orientation_sensitive_pairs,
        "quadratic_checks": quadratic_checks,
        "row_bound": str(row_bound),
        "row_checks": row_checks,
        "status": "PASS",
        "theorem_status": STATUS,
        "vectors": len(vectors),
    }
    print("TPC243_HARD_WINDOW_STRESS=PASS")
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC243_HARD_WINDOW_STRESS=FAIL: use --check")
    try:
        census()
    except (StressFailure, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC243_HARD_WINDOW_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
