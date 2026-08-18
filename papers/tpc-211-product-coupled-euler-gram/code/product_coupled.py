"""Exact finite algebra for TPC-211.

The module models the literal V46 local Euler factors on a common CRT
residue space.  It deliberately contains no prime-distribution estimate:
all values are exact Fractions and every construction is finite.
"""

from __future__ import annotations

from fractions import Fraction
from math import prod


Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def prime_masks(primes: tuple[int, ...]) -> tuple[int, ...]:
    require(len(primes) >= 1, "at least one active prime")
    require(all(type(p) is int and p > 2 for p in primes), "odd primes")
    require(tuple(sorted(set(primes))) == primes, "strictly increasing primes")
    return tuple(range(1, 1 << len(primes)))


def modulus(primes: tuple[int, ...]) -> int:
    prime_masks(primes)
    return prod(primes)


def mask_product(primes: tuple[int, ...], mask: int) -> int:
    prime_masks(primes)
    require(1 <= mask < (1 << len(primes)), "nonempty mask")
    return prod(
        prime for index, prime in enumerate(primes) if (mask >> index) & 1
    )


def mask_mobius(mask: int) -> int:
    require(mask > 0, "nonempty mask")
    return -1 if mask.bit_count() % 2 else 1


def local_f(prime: int, residue: int) -> Fraction:
    require(prime > 2, "odd local prime")
    return (
        Fraction(0, 1)
        if (residue + 2) % prime == 0
        else Fraction(prime, prime - 1)
    )


def local_g(prime: int, cutoff: int, residue: int) -> Fraction:
    require(prime > cutoff, "active prime must exceed cutoff")
    return (
        Fraction(prime, prime - 1)
        if residue % prime == 0
        else Fraction(prime * (prime - 2), (prime - 1) ** 2)
    )


def profiles(
    primes: tuple[int, ...], cutoff: int
) -> tuple[tuple[int, Vector], ...]:
    """Return lifted Delta_S=P_S-B_S profiles on Z/(product p)Z."""

    masks = prime_masks(primes)
    require(cutoff < primes[0], "all active primes exceed cutoff")
    modulus_value = modulus(primes)
    rows: list[tuple[int, Vector]] = []
    for mask in masks:
        values: list[Fraction] = []
        for residue in range(modulus_value):
            p_value = Fraction(1, 1)
            b_value = Fraction(1, 1)
            for index, prime in enumerate(primes):
                if (mask >> index) & 1:
                    p_value *= local_f(prime, residue)
                    b_value *= local_g(prime, cutoff, residue)
            values.append(p_value - b_value)
        rows.append((mask, tuple(values)))
    return tuple(rows)


def inner(left: Vector, right: Vector) -> Fraction:
    require(len(left) == len(right), "inner-product shape")
    return sum((a * b for a, b in zip(left, right)), Fraction(0, 1))


def gram(rows: tuple[tuple[int, Vector], ...]) -> Matrix:
    return tuple(
        tuple(inner(left, right) for _, right in rows) for _, left in rows
    )


def rank(matrix: tuple[tuple[Fraction, ...], ...]) -> int:
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    require(all(len(row) == column_count for row in work), "matrix shape")
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(pivot_row, row_count) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(row_count):
            if index == pivot_row or not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[index], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def determinant(matrix: Matrix) -> Fraction:
    if not matrix:
        return Fraction(1, 1)
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "square matrix")
    work = [list(row) for row in matrix]
    value = Fraction(1, 1)
    for column in range(size):
        pivot = next(
            (index for index in range(column, size) if work[index][column]),
            None,
        )
        if pivot is None:
            return Fraction(0, 1)
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        work[column] = [entry / diagonal for entry in work[column]]
        for index in range(column + 1, size):
            if not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[index], work[column])
            ]
    return value


def solve(matrix: Matrix, target: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    size = len(matrix)
    require(size == len(target), "linear-system shape")
    require(all(len(row) == size for row in matrix), "square linear system")
    augmented = [list(row) + [target[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (index for index in range(column, size) if augmented[index][column]),
            None,
        )
        require(pivot is not None, "singular linear system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for index in range(size):
            if index == column or not augmented[index][column]:
                continue
            factor = augmented[index][column]
            augmented[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(augmented[index], augmented[column])
            ]
    return tuple(row[-1] for row in augmented)


def dual_endpoint_alignment(
    rows: tuple[tuple[int, Vector], ...]
) -> tuple[Vector, tuple[Fraction, ...]]:
    """Build a common endpoint w with <w,Delta_S>=mu(S)."""

    matrix = gram(rows)
    target = tuple(Fraction(mask_mobius(mask), 1) for mask, _ in rows)
    coefficients = solve(matrix, target)
    endpoint = tuple(
        sum(
            (coefficient * vector[index] for coefficient, (_, vector) in zip(coefficients, rows)),
            Fraction(0, 1),
        )
        for index in range(len(rows[0][1]))
    )
    correlations = tuple(inner(endpoint, vector) for _, vector in rows)
    require(correlations == target, "common-endpoint alignment")
    return endpoint, correlations


def cocycle_residual_with_primes(
    primes: tuple[int, ...], cutoff: int, left_mask: int, right_mask: int
) -> Vector:
    rows = dict(profiles(primes, cutoff))
    require(left_mask & right_mask == 0, "disjoint masks")
    union = left_mask | right_mask
    modulus_value = modulus(primes)
    output: list[Fraction] = []
    for residue in range(modulus_value):
        p_left = b_left = p_right = b_right = Fraction(1, 1)
        for index, prime in enumerate(primes):
            if (left_mask >> index) & 1:
                p_left *= local_f(prime, residue)
                b_left *= local_g(prime, cutoff, residue)
            if (right_mask >> index) & 1:
                p_right *= local_f(prime, residue)
                b_right *= local_g(prime, cutoff, residue)
        expected = p_left * rows[right_mask][residue] + b_right * rows[left_mask][residue]
        output.append(rows[union][residue] - expected)
    return tuple(output)


def derivative_components(
    primes: tuple[int, ...], cutoff: int
) -> tuple[tuple[int, Vector], ...]:
    """Return D_p=P_p prod(1-P_r)-B_p prod(1-B_r)."""

    prime_masks(primes)
    modulus_value = modulus(primes)
    components: list[tuple[int, Vector]] = []
    for marked, prime in enumerate(primes):
        values: list[Fraction] = []
        for residue in range(modulus_value):
            p_term = Fraction(1, 1)
            b_term = Fraction(1, 1)
            for index, other in enumerate(primes):
                p_factor = local_f(other, residue)
                b_factor = local_g(other, cutoff, residue)
                if index == marked:
                    p_term *= p_factor
                    b_term *= b_factor
                else:
                    p_term *= 1 - p_factor
                    b_term *= 1 - b_factor
            values.append(p_term - b_term)
        components.append((prime, tuple(values)))
    return tuple(components)


def coefficientwise_log_derivative_identity(
    primes: tuple[int, ...], cutoff: int
) -> bool:
    rows = dict(profiles(primes, cutoff))
    derivatives = dict(derivative_components(primes, cutoff))
    for index, prime in enumerate(primes):
        coefficient = [Fraction(0, 1) for _ in range(modulus(primes))]
        for mask, vector in rows.items():
            if (mask >> index) & 1:
                sign = mask_mobius(mask)
                coefficient = [
                    old + sign * value for old, value in zip(coefficient, vector)
                ]
        if tuple(old + new for old, new in zip(coefficient, derivatives[prime])) != tuple(
            Fraction(0, 1) for _ in coefficient
        ):
            return False
    return True


def endpoint_packet_coefficients(primes: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(
            mask_mobius(mask)
            for mask in prime_masks(primes)
            if (mask >> index) & 1
        )
        for index in range(len(primes))
    )


def finite_case(primes: tuple[int, ...], cutoff: int) -> dict[str, object]:
    rows = profiles(primes, cutoff)
    matrix = gram(rows)
    endpoint, correlations = dual_endpoint_alignment(rows)
    masks = tuple(mask for mask, _ in rows)
    coherent = sum(
        correlation * mask_mobius(mask)
        for mask, correlation in zip(masks, correlations)
    )
    diagonal = sum(correlation * correlation for correlation in correlations)
    return {
        "primes": list(primes),
        "cutoff": cutoff,
        "modulus": modulus(primes),
        "divisor_masks": list(masks),
        "divisor_count": len(rows),
        "profile_rank": rank(tuple(vector for _, vector in rows)),
        "gram_determinant": str(determinant(matrix)),
        "endpoint_alignment": True,
        "mobius_correlations": [str(value) for value in correlations],
        "coherent_energy": str(coherent * coherent),
        "diagonal_energy": str(diagonal),
        "coherent_to_diagonal_ratio": str(coherent * coherent / diagonal),
        "log_derivative_identity": coefficientwise_log_derivative_identity(
            primes, cutoff
        ),
        "endpoint_packet_coefficients": list(endpoint_packet_coefficients(primes)),
        "cocycle_5_7": (
            all(
                value == 0
                for value in cocycle_residual_with_primes(primes, cutoff, 1, 2)
            )
            if len(primes) >= 2
            else None
        ),
        "endpoint_vector_norm_squared": str(inner(endpoint, endpoint)),
    }
