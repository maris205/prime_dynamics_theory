"""Exact rational RH-336 isospectral projector-cell fixtures.

The matrices in this module are finite, nonphysical algebraic witnesses.
They reproduce exact similarity, positivity, trace, projector-mass, and
localized-ledger formulas without asserting anything about the physical noisy
quadratic operator.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable


F = Fraction
Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


K_BASE: Matrix = (
    (F(3, 17), F(7, 51), F(35, 51)),
    (F(4, 85), F(83, 255), F(32, 51)),
    (F(58, 85), F(1, 51), F(76, 255)),
)

E_MINUS_BASE: Matrix = (
    (F(10, 17), -F(5, 51), -F(25, 51)),
    (F(8, 17), -F(4, 51), -F(20, 51)),
    (-F(10, 17), F(5, 51), F(25, 51)),
)

SUFFICIENT_LOWER = -F(5, 174)
SUFFICIENT_UPPER = F(1, 2)


def identity(size: int) -> Matrix:
    return tuple(
        tuple(F(int(i == j)) for j in range(size))
        for i in range(size)
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def matrix_subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] - right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def matrix_scale(scalar: Fraction, matrix: Matrix) -> Matrix:
    return tuple(tuple(scalar * value for value in row) for row in matrix)


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    width = len(right[0])
    inner = len(right)
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(inner)), F(0))
            for j in range(width)
        )
        for i in range(len(left))
    )


def matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    if exponent < 0:
        raise ValueError("matrix exponent must be nonnegative")
    result = identity(len(matrix))
    base = matrix
    power = exponent
    while power:
        if power & 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        power //= 2
    return result


def matrix_trace(matrix: Matrix) -> Fraction:
    return sum((matrix[i][i] for i in range(len(matrix))), F(0))


def diagonal(matrix: Matrix) -> Vector:
    return tuple(matrix[i][i] for i in range(len(matrix)))


def vector_sum(values: Iterable[Fraction]) -> Fraction:
    return sum(values, F(0))


def shear(t: Fraction) -> Matrix:
    """Return ``S_t``."""

    return (
        (F(1) - t, t, F(0)),
        (F(0), F(1), F(0)),
        (F(0), F(0), F(1)),
    )


def shear_inverse(t: Fraction) -> Matrix:
    """Return the exact inverse of ``S_t``."""

    if t == 1:
        raise ValueError("S_t is singular at t=1")
    return (
        (F(1) / (F(1) - t), -t / (F(1) - t), F(0)),
        (F(0), F(1), F(0)),
        (F(0), F(0), F(1)),
    )


def similarity_family(t: Fraction) -> Matrix:
    """Return ``K_t=S_t^{-1} K S_t``."""

    return matrix_multiply(matrix_multiply(shear_inverse(t), K_BASE), shear(t))


def audited_family_formula(t: Fraction) -> Matrix:
    """Return the displayed closed formula for ``K_t``."""

    if t == 1:
        raise ValueError("K_t is undefined at t=1")
    one_minus_t = F(1) - t
    return (
        (
            (F(15) - 4 * t) / 85,
            (F(35) - 38 * t - 12 * t**2) / (255 * one_minus_t),
            (F(35) - 32 * t) / (51 * one_minus_t),
        ),
        (
            4 * one_minus_t / 85,
            (F(83) + 12 * t) / 255,
            F(32, 51),
        ),
        (
            58 * one_minus_t / 85,
            (F(5) + 174 * t) / 255,
            F(76, 255),
        ),
    )


def projector_family(t: Fraction) -> Matrix:
    """Return ``E_-(t)=S_t^{-1}E_-S_t``."""

    return matrix_multiply(
        matrix_multiply(shear_inverse(t), E_MINUS_BASE), shear(t)
    )


def audited_projector_formula(t: Fraction) -> Matrix:
    """Return the closed exact formula for ``E_-(t)``."""

    if t == 1:
        raise ValueError("E_-(t) is undefined at t=1")
    one_minus_t = F(1) - t
    return (
        (
            (F(10) - 8 * t) / 17,
            (-F(5) + 34 * t - 24 * t**2) / (51 * one_minus_t),
            (-F(25) + 20 * t) / (51 * one_minus_t),
        ),
        (
            8 * one_minus_t / 17,
            (-F(4) + 24 * t) / 51,
            -F(20, 51),
        ),
        (
            -10 * one_minus_t / 17,
            (F(5) - 30 * t) / 51,
            F(25, 51),
        ),
    )


def projector_masses(t: Fraction) -> Vector:
    """Return the singleton masses ``diag(E_-(t))``."""

    return diagonal(projector_family(t))


def projector_mass_formula(t: Fraction) -> Vector:
    """Return the displayed affine mass formula."""

    return (
        (F(10) - 8 * t) / 17,
        (-F(4) + 24 * t) / 51,
        F(25, 51),
    )


def projector_mass_drift(t: Fraction) -> Vector:
    """Return ``pi(t)-pi(0)``."""

    return (-8 * t / 17, 8 * t / 17, F(0))


def power_trace_formula(exponent: int) -> Fraction:
    """Return ``1+(-2/5)^m+(1/5)^m``."""

    if exponent < 1:
        raise ValueError("power-trace formula is stated for m>=1")
    return F(1) + (-F(2, 5)) ** exponent + F(1, 5) ** exponent


def corrected_cells(t: Fraction) -> Vector:
    """Compute the RH-335 fixed-order corrected singleton cells directly."""

    n = 2
    r_h = F(17, 20)
    parity_scalar = F(21, 25)
    localized_noisy = diagonal(matrix_power(similarity_family(t), n))
    masses = projector_masses(t)
    return tuple(
        r_h ** (-n) * (localized_noisy[index] + parity_scalar * masses[index])
        for index in range(3)
    )


def corrected_cell_formula(t: Fraction) -> Vector:
    """Return the displayed affine formula for the three corrected cells."""

    return (
        (F(6800) - 5760 * t) / 4913,
        (F(400) + 5760 * t) / 4913,
        F(6672, 4913),
    )


def corrected_cell_drift(t: Fraction) -> Vector:
    """Return ``C(t)-C(0)``."""

    return (-5760 * t / 4913, 5760 * t / 4913, F(0))


def strictly_positive(t: Fraction) -> bool:
    """Test every entry of the exact similarity family."""

    return all(value > 0 for row in similarity_family(t) for value in row)


def in_sufficient_positivity_interval(t: Fraction) -> bool:
    """Test the convenient theorem interval ``(-5/174,1/2)``."""

    return SUFFICIENT_LOWER < t < SUFFICIENT_UPPER


def positivity_factor_ledger(t: Fraction) -> dict[str, Fraction]:
    """Return the nonconstant factors controlling positivity for ``t<1``."""

    return {
        "one_minus_t": F(1) - t,
        "row1_col1_numerator": F(15) - 4 * t,
        "row1_col2_numerator": F(35) - 38 * t - 12 * t**2,
        "row1_col3_numerator": F(35) - 32 * t,
        "row2_col2_numerator": F(83) + 12 * t,
        "row3_col2_numerator": F(5) + 174 * t,
    }


def family_audit(t: Fraction = F(1, 100), max_power: int = 12) -> dict[str, object]:
    """Return the complete exact finite family audit at one rational ``t``."""

    if max_power < 1:
        raise ValueError("max_power must be positive")
    k_t = similarity_family(t)
    e_t = projector_family(t)
    power_rows = tuple(
        {
            "m": exponent,
            "direct_trace": matrix_trace(matrix_power(k_t, exponent)),
            "spectral_trace": power_trace_formula(exponent),
        }
        for exponent in range(1, max_power + 1)
    )
    cells = corrected_cells(t)
    base_cells = corrected_cells(F(0))
    return {
        "t": t,
        "S_t": shear(t),
        "S_t_inverse": shear_inverse(t),
        "K_t": k_t,
        "K_formula": audited_family_formula(t),
        "E_minus_t": e_t,
        "E_minus_formula": audited_projector_formula(t),
        "row_sums": tuple(vector_sum(row) for row in k_t),
        "strictly_positive": strictly_positive(t),
        "in_sufficient_interval": in_sufficient_positivity_interval(t),
        "projector_idempotent": matrix_multiply(e_t, e_t) == e_t,
        "projector_intertwining_left": (
            matrix_multiply(k_t, e_t) == matrix_scale(-F(2, 5), e_t)
        ),
        "projector_intertwining_right": (
            matrix_multiply(e_t, k_t) == matrix_scale(-F(2, 5), e_t)
        ),
        "projector_trace": matrix_trace(e_t),
        "projector_masses": projector_masses(t),
        "projector_mass_formula": projector_mass_formula(t),
        "projector_mass_drift": projector_mass_drift(t),
        "power_rows": power_rows,
        "corrected_cells": cells,
        "corrected_cell_formula": corrected_cell_formula(t),
        "corrected_total": vector_sum(cells),
        "corrected_drift": tuple(
            cells[index] - base_cells[index] for index in range(3)
        ),
        "corrected_drift_formula": corrected_cell_drift(t),
    }


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"
