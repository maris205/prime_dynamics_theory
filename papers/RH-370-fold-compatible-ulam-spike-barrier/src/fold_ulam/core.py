"""Exact finite linear algebra and the deterministic spike calculation.

The manuscript contains the analytic statements.  This module intentionally
uses rational arithmetic for the finite quotient identities and ordinary
double precision only for the displayed algebraic spike coefficient.
"""

from __future__ import annotations

from fractions import Fraction
from math import sqrt


Matrix = tuple[tuple[Fraction, ...], ...]


def _zeros(rows: int, cols: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(cols)] for _ in range(rows)]


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("incompatible matrix dimensions")
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def _matadd(left: Matrix, right: Matrix, sign: int = 1) -> Matrix:
    if len(left) != len(right) or len(left[0]) != len(right[0]):
        raise ValueError("incompatible matrix dimensions")
    return tuple(
        tuple(left[i][j] + sign * right[i][j] for j in range(len(left[0])))
        for i in range(len(left))
    )


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0])))


def _identity(size: int) -> Matrix:
    return tuple(
        tuple(Fraction(int(i == j)) for j in range(size)) for i in range(size)
    )


def _matpow(matrix: Matrix, exponent: int) -> Matrix:
    result = _identity(len(matrix))
    base = matrix
    while exponent:
        if exponent & 1:
            result = _matmul(result, base)
        base = _matmul(base, base)
        exponent >>= 1
    return result


def _trace(matrix: Matrix) -> Fraction:
    return sum(matrix[i][i] for i in range(len(matrix)))


def charpoly(matrix: Matrix) -> tuple[Fraction, ...]:
    """Return coefficients of det(lambda I - matrix), descending."""

    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("matrix must be nonempty and square")
    powers = [_identity(size)]
    for _ in range(size):
        powers.append(_matmul(powers[-1], matrix))
    coefficients = [Fraction(1)]
    for k in range(1, size + 1):
        value = sum(coefficients[k - i] * _trace(powers[i]) for i in range(1, k + 1))
        coefficients.append(-value / k)
    return tuple(coefficients)


def cyclic_folded_matrix(size: int) -> Matrix:
    """A rational row-stochastic folded test matrix."""

    if size < 1:
        raise ValueError("size must be positive")
    rows = _zeros(size, size)
    for i in range(size):
        rows[i][i] += Fraction(1, 2)
        rows[i][(i + 1) % size] += Fraction(1, 2)
    return tuple(tuple(row) for row in rows)


def mirror_extension(folded: Matrix, paired: int) -> dict[str, object]:
    """Build a finite mirror extension and its exact quotient identities.

    ``J`` copies folded observable values to mirror cells.  The extension is
    the normal-form representative of an exact cell-overlap matrix: its
    mirror rows agree and its antisymmetric density kernel is killed.  The
    quotient statement is invariant under the cell-length normalizations.
    """

    dimension = len(folded)
    if dimension < 1 or any(len(row) != dimension for row in folded):
        raise ValueError("folded matrix must be square")
    if not 0 <= paired < dimension:
        raise ValueError("paired count outside folded dimension")
    full_dimension = dimension + paired
    j = _zeros(full_dimension, dimension)
    # First paired folded cells receive two mirror rows; the rest are single.
    for index in range(paired):
        j[2 * index][index] = Fraction(1)
        j[2 * index + 1][index] = Fraction(1)
    for index in range(paired, dimension):
        j[paired + index][index] = Fraction(1)
    J = tuple(tuple(row) for row in j)

    # A is a left inverse of J.  The half weights are the cell-average
    # normalization for a mirrored pair.
    a = _zeros(dimension, full_dimension)
    for index in range(paired):
        a[index][2 * index] = Fraction(1, 2)
        a[index][2 * index + 1] = Fraction(1, 2)
    for index in range(paired, dimension):
        a[index][paired + index] = Fraction(1)
    A = tuple(tuple(row) for row in a)

    full = _matmul(_matmul(J, folded), A)
    # Pair-difference columns span the mirror-antisymmetric kernel.
    kernel = []
    for index in range(paired):
        vector = [Fraction(0)] * full_dimension
        vector[2 * index] = Fraction(1)
        vector[2 * index + 1] = Fraction(-1)
        kernel.append(tuple(vector))
    full_transpose = _transpose(full)

    def column_action(matrix: Matrix, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix)))

    kernel_images = [column_action(full_transpose, vector) for vector in kernel]
    observable_residual = _matadd(_matmul(full, J), _matmul(J, folded), sign=-1)
    return {
        "folded": folded,
        "full": full,
        "J": J,
        "A": A,
        "kernel": kernel,
        "observable_residual": observable_residual,
        "kernel_images": kernel_images,
        "char_full": charpoly(full),
        "char_folded": charpoly(folded),
    }


def spike_values(u: float, h: float) -> tuple[float, float]:
    """Adjacent terminal-cell averages of ``P_T 1``."""

    if u <= 0 or h <= 0:
        raise ValueError("u and h must be positive")
    first = 1.0 / sqrt(u * h)
    second = (sqrt(2.0) - 1.0) / sqrt(u * h)
    return first, second


def spike_jump(u: float, h: float) -> float:
    """The exact BV jump between the two terminal cell averages."""

    first, second = spike_values(u, h)
    return first - second


def finite_checks() -> dict[str, object]:
    """Run exact quotient checks at four increasing finite dimensions."""

    rows = []
    for paired, singles in ((2, 1), (3, 2), (4, 3), (5, 4)):
        folded = cyclic_folded_matrix(paired + singles)
        audit = mirror_extension(folded, paired)
        residual = max(
            (abs(value) for row in audit["observable_residual"] for value in row),
            default=Fraction(0),
        )
        kernel_residual = max(
            (abs(value) for vector in audit["kernel_images"] for value in vector),
            default=Fraction(0),
        )
        expected_char = audit["char_folded"] + (Fraction(0),) * paired
        rows.append({
            "paired_cells": paired,
            "unpaired_cells": singles,
            "full_dimension": len(audit["full"]),
            "observable_residual": str(residual),
            "kernel_residual": str(kernel_residual),
            "characteristic_factor": audit["char_full"] == expected_char,
            "pass": residual == 0 and kernel_residual == 0 and audit["char_full"] == expected_char,
        })
    return {"rows": rows, "all_pass": all(row["pass"] for row in rows)}


ROOT_U = 1.5436890126920764
