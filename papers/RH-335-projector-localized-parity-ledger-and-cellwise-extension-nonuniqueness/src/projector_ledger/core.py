"""Exact finite fixtures for the RH-335 projector-localized ledger.

All calculations use :class:`fractions.Fraction`.  They reproduce finite
algebra used in the manuscript; they are not models of the physical noisy
quadratic operator and they carry no moving-order information.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable


F = Fraction
Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


K_FIXTURE: Matrix = (
    (F(3, 17), F(7, 51), F(35, 51)),
    (F(4, 85), F(83, 255), F(32, 51)),
    (F(58, 85), F(1, 51), F(76, 255)),
)

E_MINUS_FIXTURE: Matrix = (
    (F(10, 17), -F(5, 51), -F(25, 51)),
    (F(8, 17), -F(4, 51), -F(20, 51)),
    (-F(10, 17), F(5, 51), F(25, 51)),
)

RIGHT_MINUS: Vector = (F(1), F(4, 5), -F(1))
LEFT_MINUS: Vector = (F(10, 17), -F(5, 51), -F(25, 51))


def identity(size: int) -> Matrix:
    """Return the exact identity matrix."""

    return tuple(
        tuple(F(int(i == j)) for j in range(size))
        for i in range(size)
    )


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    """Add two matrices of the same shape."""

    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def matrix_subtract(left: Matrix, right: Matrix) -> Matrix:
    """Subtract two matrices of the same shape."""

    return tuple(
        tuple(left[i][j] - right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def matrix_scale(scalar: Fraction, matrix: Matrix) -> Matrix:
    """Multiply a matrix by an exact scalar."""

    return tuple(tuple(scalar * value for value in row) for row in matrix)


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    """Multiply exact rectangular matrices."""

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
    """Raise a square matrix to a nonnegative integer power."""

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
    """Return the exact trace."""

    return sum((matrix[i][i] for i in range(len(matrix))), F(0))


def diagonal(matrix: Matrix) -> Vector:
    """Return the diagonal as a vector."""

    return tuple(matrix[i][i] for i in range(len(matrix)))


def outer(left: Vector, right: Vector) -> Matrix:
    """Return the exact rank-one outer product."""

    return tuple(tuple(x * y for y in right) for x in left)


def vector_dot(left: Vector, right: Vector) -> Fraction:
    """Return an exact vector pairing."""

    return sum((x * y for x, y in zip(left, right, strict=True)), F(0))


def vector_sum(values: Iterable[Fraction]) -> Fraction:
    """Sum an iterable of exact scalars."""

    return sum(values, F(0))


def perron_projector() -> Matrix:
    """Return the spectral projector of ``K_FIXTURE`` at eigenvalue one."""

    unit = identity(3)
    plus_two_fifths = matrix_add(K_FIXTURE, matrix_scale(F(2, 5), unit))
    minus_one_fifth = matrix_add(K_FIXTURE, matrix_scale(-F(1, 5), unit))
    return matrix_scale(
        F(25, 28), matrix_multiply(plus_two_fifths, minus_one_fifth)
    )


def remaining_projector() -> Matrix:
    """Return the spectral projector at eigenvalue ``1/5``."""

    return matrix_subtract(
        matrix_subtract(identity(3), perron_projector()), E_MINUS_FIXTURE
    )


def middle_cell_multiplier() -> Matrix:
    """Return ``M_2=diag(0,1,0)`` in one-based cell notation."""

    return (
        (F(0), F(0), F(0)),
        (F(0), F(1), F(0)),
        (F(0), F(0), F(0)),
    )


def commutator(left: Matrix, right: Matrix) -> Matrix:
    """Return ``left*right-right*left``."""

    return matrix_subtract(
        matrix_multiply(left, right), matrix_multiply(right, left)
    )


def scaled_rank_one_projector(
    right_scale: Fraction = F(7, 3),
    left_scale: Fraction = F(11, 5),
) -> Matrix:
    """Independently rescale both eigenvectors and renormalize the projector."""

    if right_scale == 0 or left_scale == 0:
        raise ValueError("eigenvector scales must be nonzero")
    right = tuple(right_scale * value for value in RIGHT_MINUS)
    left = tuple(left_scale * value for value in LEFT_MINUS)
    pairing = vector_dot(left, right)
    return matrix_scale(F(1, 1) / pairing, outer(right, left))


def projector_masses() -> Vector:
    """Return the three singleton masses ``Tr(M_i E_-)``."""

    return diagonal(E_MINUS_FIXTURE)


def localized_ledger_fixture() -> dict[str, object]:
    """Return the exact ``n=2`` singleton-cell ledger.

    The deterministic localized entries are set to zero solely for this
    algebraic fixture.  The output is not a first-alias fixture because the
    archived counterloop definition requires ``k>=2``.
    """

    n = 2
    r_h = F(17, 20)
    lambda_minus = -F(2, 5)
    k_squared = matrix_power(K_FIXTURE, n)
    localized_noisy = diagonal(k_squared)
    localized_deterministic = (F(0), F(0), F(0))
    masses = projector_masses()
    parity_scalar = F((-1) ** n) - lambda_minus**n
    hardy_scale = r_h ** (-n)
    corrected = tuple(
        hardy_scale
        * (
            localized_noisy[index]
            - localized_deterministic[index]
            + parity_scalar * masses[index]
        )
        for index in range(3)
    )
    global_difference = hardy_scale * (
        matrix_trace(k_squared)
        - vector_sum(localized_deterministic)
        + parity_scalar
    )
    return {
        "n": n,
        "r_H": r_h,
        "lambda_minus": lambda_minus,
        "K_squared": k_squared,
        "localized_noisy": localized_noisy,
        "localized_deterministic": localized_deterministic,
        "projector_masses": masses,
        "parity_scalar": parity_scalar,
        "hardy_scale": hardy_scale,
        "corrected_cells": corrected,
        "corrected_total": vector_sum(corrected),
        "global_difference": global_difference,
    }


def commutator_fixture() -> dict[str, object]:
    """Return the exact strict local-deflation commutator at ``n=2``."""

    e_zero = perron_projector()
    deflation = matrix_add(e_zero, matrix_scale(F(4, 25), E_MINUS_FIXTURE))
    window = middle_cell_multiplier()
    bracket = commutator(window, deflation)
    return {
        "E_zero": e_zero,
        "deflation_E_zero_plus_lambda_squared_E_minus": deflation,
        "M_2": window,
        "commutator": bracket,
        "commutator_trace": matrix_trace(bracket),
        "commutator_is_nonzero": any(value != 0 for row in bracket for value in row),
    }


def extension_nonuniqueness_fixture() -> dict[str, object]:
    """Return two distinct cellwise allocations of the same global scalar."""

    parity_scalar = F(21, 25)
    base = tuple(parity_scalar * mass for mass in projector_masses())
    zero_total_perturbation = (F(1, 51), -F(1, 51), F(0))
    alternative = tuple(
        base[index] + zero_total_perturbation[index] for index in range(3)
    )
    return {
        "global_scalar": parity_scalar,
        "projector_gauge_allocation": base,
        "zero_total_perturbation": zero_total_perturbation,
        "alternative_allocation": alternative,
        "base_total": vector_sum(base),
        "perturbation_total": vector_sum(zero_total_perturbation),
        "alternative_total": vector_sum(alternative),
        "allocations_are_distinct": base != alternative,
    }


def exact_fixture_audit() -> dict[str, object]:
    """Return all exact algebraic checks used by the paper."""

    e_zero = perron_projector()
    e_plus = remaining_projector()
    zero = matrix_scale(F(0), identity(3))
    unit = identity(3)
    return {
        "positive_entries": all(value > 0 for row in K_FIXTURE for value in row),
        "row_sums": tuple(vector_sum(row) for row in K_FIXTURE),
        "spectrum": (F(1), -F(2, 5), F(1, 5)),
        "spectral_projector_sum": matrix_add(matrix_add(e_zero, E_MINUS_FIXTURE), e_plus),
        "spectral_projector_sum_is_identity": (
            matrix_add(matrix_add(e_zero, E_MINUS_FIXTURE), e_plus) == unit
        ),
        "E_minus_factorization": outer(RIGHT_MINUS, LEFT_MINUS),
        "left_right_pairing": vector_dot(LEFT_MINUS, RIGHT_MINUS),
        "scaled_factorization": scaled_rank_one_projector(),
        "E_minus_squared": matrix_multiply(E_MINUS_FIXTURE, E_MINUS_FIXTURE),
        "K_E_minus": matrix_multiply(K_FIXTURE, E_MINUS_FIXTURE),
        "E_minus_K": matrix_multiply(E_MINUS_FIXTURE, K_FIXTURE),
        "E_zero_squared": matrix_multiply(e_zero, e_zero),
        "E_plus_squared": matrix_multiply(e_plus, e_plus),
        "cross_projector_products_zero": all(
            product == zero
            for product in (
                matrix_multiply(e_zero, E_MINUS_FIXTURE),
                matrix_multiply(E_MINUS_FIXTURE, e_zero),
                matrix_multiply(e_zero, e_plus),
                matrix_multiply(e_plus, e_zero),
                matrix_multiply(E_MINUS_FIXTURE, e_plus),
                matrix_multiply(e_plus, E_MINUS_FIXTURE),
            )
        ),
        "K_E_zero": matrix_multiply(K_FIXTURE, e_zero),
        "K_E_plus": matrix_multiply(K_FIXTURE, e_plus),
        "trace_E_minus": matrix_trace(E_MINUS_FIXTURE),
        "projector_masses": projector_masses(),
        "projector_masses_are_probabilities": all(
            value >= 0 for value in projector_masses()
        ),
    }


def fraction_text(value: Fraction) -> str:
    """Serialize a fraction without losing exactness."""

    return f"{value.numerator}/{value.denominator}"
