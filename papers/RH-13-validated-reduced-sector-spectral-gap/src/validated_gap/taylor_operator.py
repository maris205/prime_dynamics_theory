"""Taylor-matrix models for the two reduced transfer sectors.

This module starts with floating-point exploration.  The formulas are chosen
so that the same construction can later be evaluated with certified balls.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

import numpy as np


U_CRITICAL = 1.5436890126920763615708559718017479865
R_FIXED = U_CRITICAL - 1.0
LAMBDA_FIXED = 2.0 * U_CRITICAL * R_FIXED


def multiply(left: np.ndarray, right: np.ndarray, degree: int) -> np.ndarray:
    return np.convolve(left, right)[:degree]


def reciprocal(values: np.ndarray, degree: int) -> np.ndarray:
    result = np.zeros(degree, dtype=np.float64)
    result[0] = 1.0 / values[0]
    for n in range(1, degree):
        result[n] = -np.dot(values[1 : n + 1], result[n - 1 :: -1]) / values[0]
    return result


def square_root(values: np.ndarray, degree: int) -> np.ndarray:
    result = np.zeros(degree, dtype=np.float64)
    result[0] = np.sqrt(values[0])
    for n in range(1, degree):
        middle = np.dot(result[1:n], result[n - 1 : 0 : -1])
        result[n] = (values[n] - middle) / (2.0 * result[0])
    return result


@dataclass(frozen=True)
class TaylorIngredients:
    disk_radius: float
    inverse_square: np.ndarray
    beta_one_weight: np.ndarray
    beta_two_odd_weight: np.ndarray


def taylor_ingredients(degree: int, disk_radius: float) -> TaylorIngredients:
    if degree < 2:
        raise ValueError("degree must be at least two")
    if not R_FIXED < disk_radius < 1.0:
        raise ValueError("disk_radius must lie between r and one")
    u = U_CRITICAL
    one_minus_z = np.zeros(degree)
    one_minus_z[0] = 1.0
    one_minus_z[1] = -disk_radius
    root = square_root(one_minus_z, degree)
    inverse_square = -root / (u * np.sqrt(u))
    inverse_square[0] += 1.0 / u

    one = np.zeros(degree)
    one[0] = 1.0
    one_minus_ut = one - u * inverse_square
    two_minus_ut = one_minus_ut.copy()
    two_minus_ut[0] += 1.0
    one_minus_t = one - inverse_square
    radicand = u * multiply(two_minus_ut, one_minus_t, degree)
    beta_one_weight = 0.25 * multiply(
        square_root(radicand, degree),
        reciprocal(one_minus_ut, degree),
        degree,
    )
    beta_two_odd_weight = multiply(
        beta_one_weight,
        reciprocal(2.0 * u**2 * one_minus_ut, degree),
        degree,
    )
    return TaylorIngredients(
        disk_radius=disk_radius,
        inverse_square=inverse_square,
        beta_one_weight=beta_one_weight,
        beta_two_odd_weight=beta_two_odd_weight,
    )


def sector_matrices(degree: int, disk_radius: float) -> tuple[np.ndarray, np.ndarray]:
    ingredients = taylor_ingredients(degree, disk_radius)
    t = ingredients.inverse_square
    beta_one = np.zeros((degree, degree), dtype=np.float64)
    beta_two = np.zeros((degree, degree), dtype=np.float64)
    power = np.zeros(degree)
    power[0] = 1.0
    for k in range((degree + 1) // 2):
        even_column = 2 * k
        if even_column < degree:
            beta_one[:, even_column] = (
                2.0
                * multiply(ingredients.beta_one_weight, power, degree)
                / disk_radius**even_column
            )
        odd_column = 2 * k + 1
        if odd_column < degree:
            beta_two[:, odd_column] = (
                multiply(ingredients.beta_two_odd_weight, power, degree)
                / disk_radius**odd_column
            )
        power = multiply(power, t, degree)
    return beta_one, beta_two


def circle_mean_functional(degree: int, disk_radius: float) -> np.ndarray:
    functional = np.zeros(degree, dtype=np.float64)
    ratio = R_FIXED / disk_radius
    for k in range((degree + 1) // 2):
        index = 2 * k
        if index < degree:
            functional[index] = comb(2 * k, k) * (ratio / 2.0) ** (2 * k)
    return functional


def reduced_beta_one_matrix(degree: int, disk_radius: float) -> np.ndarray:
    beta_one, _ = sector_matrices(degree, disk_radius)
    mean = circle_mean_functional(degree, disk_radius)
    embedding = np.zeros((degree, degree - 1), dtype=np.float64)
    embedding[0, :] = -mean[1:]
    embedding[1:, :] = np.eye(degree - 1)
    return (beta_one @ embedding)[1:, :]


def leading_eigenvalues(matrix: np.ndarray, count: int = 6) -> list[complex]:
    values = np.linalg.eigvals(matrix)
    return sorted(values, key=abs, reverse=True)[:count]


def weighted_absolute_radius(matrix: np.ndarray) -> float:
    return float(max(abs(value) for value in np.linalg.eigvals(np.abs(matrix))))
