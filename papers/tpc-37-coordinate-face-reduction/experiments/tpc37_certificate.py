#!/usr/bin/env python3
"""Deterministic exact-arithmetic certificate for TPC-37.

The certificate uses only the Python standard library.  It deliberately uses
no floating-point arithmetic, randomness, or ``assert`` statements.  Failed
checks raise ``CertificateError`` explicitly, so the verification is unchanged
under ``python -O``.
"""

from __future__ import annotations

import ast
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


class CertificateError(RuntimeError):
    """Raised when an exact certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def frac_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: object) -> str:
    data = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return sha256_bytes(data)


def product(values: Iterable[Fraction]) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def inv_mod(value: int, modulus: int) -> int:
    value %= modulus
    require(value != 0, f"attempted to invert zero modulo {modulus}")
    return pow(value, modulus - 2, modulus)


# The three Jacobi checks use q=5,7,11, hence cyclotomic orders 4,6,10.
# Coefficients are listed in ascending powers and each polynomial is monic.
CYCLOTOMIC_POLYNOMIALS: Dict[int, Tuple[int, ...]] = {
    4: (1, 0, 1),
    6: (1, -1, 1),
    10: (1, -1, 1, -1, 1),
}


class Cyclo:
    """An exact element of Q[z]/Phi_n(z) for n in {4,6,10}."""

    __slots__ = ("n", "coeffs")

    def __init__(self, n: int, coeffs: Sequence[Fraction | int]) -> None:
        require(n in CYCLOTOMIC_POLYNOMIALS, f"unsupported cyclotomic order {n}")
        self.n = n
        phi = CYCLOTOMIC_POLYNOMIALS[n]
        degree = len(phi) - 1
        work = [Fraction(item) for item in coeffs]
        if not work:
            work = [Fraction(0)]
        while len(work) > degree:
            top_index = len(work) - 1
            top = work[top_index]
            shift = top_index - degree
            if top:
                for offset, coefficient in enumerate(phi):
                    work[shift + offset] -= top * coefficient
            require(work[top_index] == 0, "monic polynomial reduction failed")
            work.pop()
        work.extend(Fraction(0) for _ in range(degree - len(work)))
        self.coeffs = tuple(work)

    @classmethod
    def zero(cls, n: int) -> "Cyclo":
        return cls(n, (0,))

    @classmethod
    def constant(cls, n: int, value: Fraction | int) -> "Cyclo":
        return cls(n, (Fraction(value),))

    @classmethod
    def monomial(cls, n: int, exponent: int) -> "Cyclo":
        exponent %= n
        coeffs = [Fraction(0)] * (exponent + 1)
        coeffs[exponent] = Fraction(1)
        return cls(n, coeffs)

    def _same_order(self, other: "Cyclo") -> None:
        require(self.n == other.n, "mixed cyclotomic orders")

    def __add__(self, other: "Cyclo") -> "Cyclo":
        self._same_order(other)
        return Cyclo(self.n, [a + b for a, b in zip(self.coeffs, other.coeffs)])

    def __sub__(self, other: "Cyclo") -> "Cyclo":
        self._same_order(other)
        return Cyclo(self.n, [a - b for a, b in zip(self.coeffs, other.coeffs)])

    def __neg__(self) -> "Cyclo":
        return Cyclo(self.n, [-item for item in self.coeffs])

    def __mul__(self, other: "Cyclo") -> "Cyclo":
        self._same_order(other)
        size = len(self.coeffs) + len(other.coeffs) - 1
        coeffs = [Fraction(0)] * size
        for left_index, left in enumerate(self.coeffs):
            for right_index, right in enumerate(other.coeffs):
                coeffs[left_index + right_index] += left * right
        return Cyclo(self.n, coeffs)

    def scale(self, scalar: Fraction | int) -> "Cyclo":
        scalar = Fraction(scalar)
        return Cyclo(self.n, [scalar * item for item in self.coeffs])

    def conjugate(self) -> "Cyclo":
        result = Cyclo.zero(self.n)
        for exponent, coefficient in enumerate(self.coeffs):
            result = result + Cyclo.monomial(self.n, -exponent).scale(coefficient)
        return result

    def is_constant(self, value: Fraction | int) -> bool:
        expected = [Fraction(0)] * len(self.coeffs)
        expected[0] = Fraction(value)
        return self.coeffs == tuple(expected)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cyclo):
            return False
        return self.n == other.n and self.coeffs == other.coeffs

    def encoded(self) -> List[str]:
        return [frac_text(item) for item in self.coeffs]


def cyclo_sum(values: Iterable[Cyclo], n: int) -> Cyclo:
    result = Cyclo.zero(n)
    for value in values:
        result = result + value
    return result


def cyclo_abs_square(value: Cyclo) -> Cyclo:
    return value.conjugate() * value


def prime_factors(value: int) -> List[int]:
    factors: List[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return factors


def primitive_root(prime: int) -> int:
    order = prime - 1
    factors = prime_factors(order)
    for candidate in range(2, prime):
        if all(pow(candidate, order // factor, prime) != 1 for factor in factors):
            return candidate
    raise CertificateError(f"no primitive root found modulo {prime}")


def discrete_log_table(prime: int, generator: int) -> List[int]:
    order = prime - 1
    table = [-1] * prime
    value = 1
    for exponent in range(order):
        require(table[value] == -1, "primitive-root orbit repeated early")
        table[value] = exponent
        value = (value * generator) % prime
    require(value == 1, "primitive-root orbit did not close")
    require(all(table[value] >= 0 for value in range(1, prime)), "incomplete log table")
    return table


def jacobi_sum(
    prime: int, logs: Sequence[int], psi_index: int, chi_index: int
) -> Cyclo:
    """Return J(psi, conjugate(chi)) in the exact cyclotomic ring."""

    order = prime - 1
    result = Cyclo.zero(order)
    for x_value in range(1, prime):
        y_value = (1 - x_value) % prime
        if y_value == 0:
            continue
        exponent = psi_index * logs[x_value] - chi_index * logs[y_value]
        result = result + Cyclo.monomial(order, exponent)
    return result


def verify_jacobi_matrix(prime: int) -> Dict[str, object]:
    order = prime - 1
    require(order in CYCLOTOMIC_POLYNOMIALS, "missing exact cyclotomic model")
    generator = primitive_root(prime)
    logs = discrete_log_table(prime, generator)
    indices = list(range(1, order))
    matrix = [
        [jacobi_sum(prime, logs, psi, chi) for psi in indices]
        for chi in indices
    ]
    dimension = len(indices)

    for left in range(dimension):
        for right in range(dimension):
            gram = cyclo_sum(
                (
                    matrix[row][left].conjugate() * matrix[row][right]
                    for row in range(dimension)
                ),
                order,
            )
            expected = order * order - prime if left == right else -prime
            require(
                gram.is_constant(expected),
                f"K^*K failed for q={prime}, ({left},{right}): {gram.encoded()}",
            )

            other_gram = cyclo_sum(
                (
                    matrix[left][column] * matrix[right][column].conjugate()
                    for column in range(dimension)
                ),
                order,
            )
            require(
                other_gram.is_constant(expected),
                f"KK^* failed for q={prime}, ({left},{right})",
            )

    for row in range(dimension):
        row_sum = cyclo_sum(matrix[row], order)
        require(row_sum.is_constant(1), f"Jacobi row sum failed for q={prime}")
    for column in range(dimension):
        column_sum = cyclo_sum(
            (matrix[row][column] for row in range(dimension)), order
        )
        require(column_sum.is_constant(1), f"Jacobi column sum failed for q={prime}")

    z_vector = [(-1 if index % 2 else 1) * (index + 2) for index in range(dimension)]
    transformed: List[Cyclo] = []
    for row in range(dimension):
        transformed.append(
            cyclo_sum(
                (matrix[row][column].scale(z_vector[column]) for column in range(dimension)),
                order,
            ).scale(Fraction(1, order))
        )
    energy = cyclo_sum((cyclo_abs_square(item) for item in transformed), order)
    sum_squares = sum(item * item for item in z_vector)
    vector_sum = sum(z_vector)
    predicted = Fraction(sum_squares) - Fraction(prime * vector_sum * vector_sum, order * order)
    require(
        energy.is_constant(predicted),
        f"Jacobi singular-energy identity failed for q={prime}: {energy.encoded()}",
    )

    all_ones_energy = cyclo_sum(
        (
            cyclo_abs_square(cyclo_sum(matrix[row], order).scale(Fraction(1, order)))
            for row in range(dimension)
        ),
        order,
    )
    require(
        all_ones_energy.is_constant(Fraction(dimension, order * order)),
        f"small singular direction failed for q={prime}",
    )

    return {
        "q": prime,
        "primitive_root": generator,
        "cyclotomic_order": order,
        "matrix_dimension": dimension,
        "gram_diagonal": order * order - prime,
        "gram_off_diagonal": -prime,
        "singular_values_squared": {
            "large": order * order,
            "large_multiplicity": prime - 3,
            "small": 1,
            "small_multiplicity": 1,
        },
        "energy_test_vector": z_vector,
        "energy_value": frac_text(predicted),
    }


def verify_physical_zero_faces(prime: int) -> Dict[str, int]:
    h_value = 2 % prime
    if h_value == 0:
        h_value = 1
    labels = [
        value for value in range(2 * prime + 1, 6 * prime + 3) if value % prime != 0
    ]
    times = list(range(1, prime))
    span = max(labels) - min(labels)
    interval_class_bound = span // prime + 1

    counts_by_time = []
    for time in times:
        count = sum(1 for label in labels if (label * time + h_value) % prime == 0)
        counts_by_time.append(count)
        require(
            count <= interval_class_bound,
            f"fixed-time residue occupancy failed modulo {prime}",
        )

    max_times_per_row = 0
    for label in labels:
        count = sum(1 for time in times if (label * time + h_value) % prime == 0)
        max_times_per_row = max(max_times_per_row, count)
        require(count <= 1, f"fixed-row orbit occupancy failed modulo {prime}")

    for left in range(prime):
        for right in range(prime):
            zero_product = (left * right) % prime == 0
            coordinate_face = left == 0 or right == 0
            require(
                zero_product == coordinate_face,
                f"zero-coordinate equivalence failed modulo {prime}",
            )

    return {
        "q": prime,
        "row_count": len(labels),
        "orbit_count": len(times),
        "row_label_span": span,
        "interval_class_bound": interval_class_bound,
        "maximum_rows_on_one_target_residue": max(counts_by_time),
        "maximum_times_for_one_row": max_times_per_row,
    }


def correlation(
    first: Sequence[Fraction],
    second: Sequence[Fraction],
    a_value: int,
    slope: int,
    h_value: int,
    prime: int,
) -> Fraction:
    slope_inverse = inv_mod(slope, prime)
    return sum(
        first[d_value]
        * second[(slope_inverse * (a_value * d_value + h_value)) % prime]
        for d_value in range(prime)
    )


def verify_punctured_centering(prime: int) -> Dict[str, object]:
    h_value = 2 % prime
    if h_value == 0:
        h_value = 1
    raw_f = [Fraction((d_value + 1) ** 2 - 3 * d_value) for d_value in range(prime)]
    raw_g = [Fraction(0)] + [
        Fraction(((-1) ** u_value) * (2 * u_value + 1))
        for u_value in range(1, prime)
    ]
    mean_f = sum(raw_f, Fraction(0)) / prime
    beta = sum(raw_g[1:], Fraction(0)) / (prime - 1)
    centered_f = [value - mean_f for value in raw_f]
    centered_g = [Fraction(0)] + [value - beta for value in raw_g[1:]]
    require(sum(centered_f, Fraction(0)) == 0, "left centering failed")
    require(sum(centered_g, Fraction(0)) == 0, "punctured centering failed")
    require(centered_g[0] == 0, "punctured value is not zero")

    checked_correlations = 0
    for a_value in range(1, prime):
        deleted = (-h_value * inv_mod(a_value, prime)) % prime
        for slope in range(1, prime):
            raw = correlation(raw_f, raw_g, a_value, slope, h_value, prime)
            core = correlation(
                centered_f, centered_g, a_value, slope, h_value, prime
            )
            predicted = core - beta * centered_f[deleted] + (prime - 1) * mean_f * beta
            require(raw == predicted, "punctured-centering identity failed")
            checked_correlations += 1

    def raw_r(a_value: int, slope: int) -> Fraction:
        return correlation(raw_f, raw_g, a_value, slope, h_value, prime)

    def centered_r(a_value: int, slope: int) -> Fraction:
        return correlation(centered_f, centered_g, a_value, slope, h_value, prime)

    weights = {ell: Fraction((ell + 2) * ((-1) ** ell)) for ell in range(1, prime)}
    weight_sum = sum(weights.values(), Fraction(0))
    checked_product_identities = 0
    for j_value in range(1, prime):
        h_f = sum(
            weights[ell]
            * centered_f[
                (-h_value * inv_mod((ell * j_value) % prime, prime)) % prime
            ]
            for ell in range(1, prime)
        )
        for slope in range(1, prime):
            raw_t = sum(
                weights[ell] * raw_r((ell * j_value) % prime, slope)
                for ell in range(1, prime)
            )
            core_t = sum(
                weights[ell] * centered_r((ell * j_value) % prime, slope)
                for ell in range(1, prime)
            )
            predicted = core_t - beta * h_f + (prime - 1) * mean_f * beta * weight_sum
            require(raw_t == predicted, "product-slope centering identity failed")
            checked_product_identities += 1

    for a_value in range(1, prime):
        trace = sum(
            (centered_r(a_value, slope) for slope in range(1, prime)),
            Fraction(0),
        )
        require(trace == 0, "complete complementary-factor trace failed")

    test_j = 1
    t_values: Dict[int, Fraction] = {}
    for slope in range(1, prime):
        t_values[slope] = sum(
            weights[ell] * centered_r((ell * test_j) % prime, slope)
            for ell in range(1, prime)
        )
    require(sum(t_values.values(), Fraction(0)) == 0, "complete T trace failed")

    start = -prime + 2
    length = 4 * prime - 2
    interval = list(range(start, start + length))
    cycles, remainder = divmod(length, prime)
    lift_counts = {
        residue: sum(1 for integer in interval if integer % prime == residue)
        for residue in range(1, prime)
    }
    boundary = {residue: count - cycles for residue, count in lift_counts.items()}
    require(
        all(value in (0, 1) for value in boundary.values()),
        "interval lift is not complete cycles plus a 0/1 boundary",
    )
    require(
        sum(1 for value in boundary.values() if value != 0) < prime,
        "boundary support is not punctured",
    )
    lifted_sum = sum(
        lift_counts[residue] * t_values[residue] for residue in range(1, prime)
    )
    boundary_sum = sum(
        boundary[residue] * t_values[residue] for residue in range(1, prime)
    )
    require(lifted_sum == boundary_sum, "complete-cycle removal failed")

    return {
        "q": prime,
        "mean_F": frac_text(mean_f),
        "punctured_mean_beta": frac_text(beta),
        "affine_correlations_checked": checked_correlations,
        "product_slope_identities_checked": checked_product_identities,
        "cycle_decomposition": {
            "interval_start": start,
            "interval_length": length,
            "complete_cycles": cycles,
            "remainder_length": remainder,
            "boundary_support": sum(1 for value in boundary.values() if value != 0),
        },
    }


def face_vector(
    primes: Sequence[int], target: int, residue: int
) -> Tuple[List[Fraction], Fraction, Fraction]:
    m_values: List[Fraction] = []
    c_values: List[Fraction] = []
    for prime in primes:
        p_value = Fraction(1, prime - 1)
        coordinate = residue % prime
        delta = Fraction(1 if coordinate == 0 else 0)
        mask = Fraction(1 if coordinate != (-target) % prime else 0)
        principal = p_value * mask
        centered = delta - principal
        m_values.append(principal)
        c_values.append(centered)

    faces: List[Fraction] = []
    for mask in range(8):
        factors = [
            c_values[index] if mask & (1 << index) else m_values[index]
            for index in range(3)
        ]
        faces.append(product(factors))
    proper = sum(faces[:7], Fraction(0))
    full = faces[7]
    return faces, proper, full


def verify_crt_faces(primes: Tuple[int, int, int], target: int) -> Dict[str, object]:
    modulus = primes[0] * primes[1] * primes[2]
    require(all(target % prime != 0 for prime in primes), "target is not a CRT unit")
    values: List[List[Fraction]] = [[] for _ in range(8)]
    proper_values: List[Fraction] = []
    full_values: List[Fraction] = []

    for residue in range(modulus):
        faces, proper, full = face_vector(primes, target, residue)
        delta = Fraction(1 if residue == 0 else 0)
        require(sum(faces, Fraction(0)) == delta, "eight-face identity failed")
        require(proper == delta - full, "proper-union identity failed")
        for mask in range(8):
            values[mask].append(faces[mask])
        proper_values.append(proper)
        full_values.append(full)

    for left, right in combinations(range(8), 2):
        inner = sum(
            (values[left][residue] * values[right][residue] for residue in range(modulus)),
            Fraction(0),
        )
        require(inner == 0, f"CRT face orthogonality failed for {left},{right}")

    p_values = [Fraction(1, prime - 1) for prime in primes]
    face_summaries: List[Dict[str, object]] = []
    for mask in range(8):
        l_two = sum((value * value for value in values[mask]), Fraction(0))
        l_one = sum((abs(value) for value in values[mask]), Fraction(0))
        expected_l_two = product(
            (Fraction(1) - p_values[index])
            if mask & (1 << index)
            else p_values[index]
            for index in range(3)
        )
        expected_l_one = Fraction(2 ** mask.bit_count()) * product(
            Fraction(1) - p_values[index]
            for index in range(3)
            if mask & (1 << index)
        )
        require(l_two == expected_l_two, f"face L2 norm failed for mask {mask}")
        require(l_one == expected_l_one, f"face L1 norm failed for mask {mask}")
        require(values[mask][0] == l_two, f"joint face value failed for mask {mask}")
        face_summaries.append(
            {
                "mask": format(mask, "03b"),
                "l1": frac_text(l_one),
                "l2_squared": frac_text(l_two),
            }
        )

    a_value = product(Fraction(1) - p_value for p_value in p_values)
    proper_l_inf = max(abs(value) for value in proper_values)
    proper_l_one = sum((abs(value) for value in proper_values), Fraction(0))
    proper_l_two = sum((value * value for value in proper_values), Fraction(0))
    full_l_one = sum((abs(value) for value in full_values), Fraction(0))
    full_l_two = sum((value * value for value in full_values), Fraction(0))
    require(proper_l_inf == 1 - a_value, "proper-union L-infinity norm failed")
    require(proper_l_one == 1 + 6 * a_value, "proper-union L1 norm failed")
    require(proper_l_two == 1 - a_value, "proper-union L2 norm failed")
    require(full_l_one == 8 * a_value, "full-face L1 norm failed")
    require(full_l_two == a_value, "full-face L2 norm failed")

    proper_off_joint = sum(
        (value * value for value in proper_values[1:]), Fraction(0)
    )
    full_off_joint = sum(
        (value * value for value in full_values[1:]), Fraction(0)
    )
    require(
        proper_off_joint == a_value * (1 - a_value),
        "proper ghost energy failed",
    )
    require(full_off_joint == a_value * (1 - a_value), "full ghost energy failed")

    return {
        "primes": list(primes),
        "target": target,
        "modulus": modulus,
        "A": frac_text(a_value),
        "faces": face_summaries,
        "proper_union": {
            "linfinity": frac_text(proper_l_inf),
            "l1": frac_text(proper_l_one),
            "l2_squared": frac_text(proper_l_two),
            "off_joint_l2_squared": frac_text(proper_off_joint),
        },
        "full_face": {
            "l1": frac_text(full_l_one),
            "l2_squared": frac_text(full_l_two),
            "off_joint_l2_squared": frac_text(full_off_joint),
        },
    }


def divisor_count(value: int) -> int:
    require(value > 0, "divisor_count requires a positive integer")
    result = 1
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            result *= exponent + 1
        divisor += 1
    if remaining > 1:
        result *= 2
    return result


def verify_determinant_periodization() -> Dict[str, object]:
    primes = (3, 5, 7)
    modulus = 3 * 5 * 7
    target = 2
    bound = 2 * modulus + 17
    max_product = target + bound
    multiplicities: Dict[int, int] = {}
    pair_count = 0
    for left in range(1, max_product + 1):
        for right in range(1, max_product // left + 1):
            determinant = left * right - target
            if abs(determinant) <= bound:
                multiplicities[determinant] = multiplicities.get(determinant, 0) + 1
                pair_count += 1

    require(multiplicities, "empty determinant test family")
    for determinant, count in multiplicities.items():
        expected = divisor_count(target + determinant)
        require(count == expected, "determinant-fiber divisor multiplicity failed")

    period_faces = [face_vector(primes, target, residue) for residue in range(modulus)]
    block_count = (2 * bound + 1 + modulus - 1) // modulus
    norm_checks: Dict[str, Dict[str, str | int]] = {}
    for name, selector in (
        ("proper", lambda record: record[1]),
        ("full", lambda record: record[2]),
    ):
        for exponent in (1, 2):
            period_norm = sum(
                (abs(selector(record)) ** exponent for record in period_faces),
                Fraction(0),
            )
            interval_norm = sum(
                (
                    abs(selector(period_faces[determinant % modulus])) ** exponent
                    for determinant in range(-bound, bound + 1)
                ),
                Fraction(0),
            )
            require(
                interval_norm <= block_count * period_norm,
                "exact periodic-block bound failed",
            )
            pair_norm = sum(
                (
                    count
                    * abs(selector(period_faces[determinant % modulus])) ** exponent
                    for determinant, count in multiplicities.items()
                ),
                Fraction(0),
            )
            regrouped_norm = sum(
                (
                    divisor_count(target + determinant)
                    * abs(selector(period_faces[determinant % modulus])) ** exponent
                    for determinant in multiplicities
                ),
                Fraction(0),
            )
            require(pair_norm == regrouped_norm, "determinant-first regrouping failed")
            norm_checks[f"{name}_r{exponent}"] = {
                "period_norm": frac_text(period_norm),
                "interval_norm": frac_text(interval_norm),
                "pair_norm": frac_text(pair_norm),
                "period_block_count": block_count,
            }

    ghost_primes = (5, 7, 11)
    ghost_target = 2
    ghost_modulus = 5 * 7 * 11
    p_one = Fraction(1, ghost_primes[0] - 1)
    p_two = Fraction(1, ghost_primes[1] - 1)
    p_three = Fraction(1, ghost_primes[2] - 1)
    expected_ghost_full = -(1 - p_one) * (1 - p_two) * p_three
    ghost_count = 0
    for k_value in range(1, 4 * ghost_primes[2] + 1):
        ultra = ghost_target + k_value * ghost_primes[0] * ghost_primes[1]
        if k_value % ghost_primes[2] == 0 or ultra % ghost_primes[2] == 0:
            continue
        determinant = ultra - ghost_target
        _, proper, full = face_vector(ghost_primes, ghost_target, determinant)
        require(full == expected_ghost_full, "two-hit ghost amplitude failed")
        require(proper == -full, "two-hit proper/full cancellation failed")
        ghost_count += 1
    require(ghost_count > 0, "no two-hit ghost examples were checked")

    a_value = product(
        Fraction(prime - 2, prime - 1) for prime in ghost_primes
    )
    for k_value in range(-3, 4):
        determinant = k_value * ghost_modulus
        _, proper, full = face_vector(ghost_primes, ghost_target, determinant)
        require(full == a_value, "joint-alias full value failed")
        require(proper == 1 - a_value, "joint-alias proper value failed")

    return {
        "fiber_test": {
            "primes": list(primes),
            "target": target,
            "modulus": modulus,
            "determinant_bound": bound,
            "positive_factor_pairs": pair_count,
            "determinant_fibers": len(multiplicities),
            "maximum_fiber_multiplicity": max(multiplicities.values()),
            "norm_checks": norm_checks,
        },
        "ghost_test": {
            "primes": list(ghost_primes),
            "target": ghost_target,
            "two_hit_examples": ghost_count,
            "two_hit_full_amplitude": frac_text(expected_ghost_full),
            "joint_aliases_checked": 7,
            "joint_full_amplitude": frac_text(a_value),
            "joint_proper_amplitude": frac_text(1 - a_value),
        },
    }


def verify_source_constraints(script_path: Path) -> Dict[str, object]:
    source = script_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(script_path))
    assert_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    float_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    random_imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            random_imports.extend(alias.name for alias in node.names if alias.name == "random")
        elif isinstance(node, ast.ImportFrom) and node.module == "random":
            random_imports.append(node.module)
    require(not assert_nodes, "certificate contains an assert statement")
    require(not float_nodes, "certificate contains a float literal")
    require(not random_imports, "certificate imports random")
    return {
        "stdlib_only": True,
        "assert_statements": len(assert_nodes),
        "float_literals": len(float_nodes),
        "random_imports": len(random_imports),
        "optimization_safe_explicit_checks": True,
    }


def build_report(script_path: Path) -> Dict[str, object]:
    paper_directory = script_path.parent.parent
    source_relatives = [
        "main.tex",
        "sections/physical-zero-faces.tex",
        "sections/punctured-centering.tex",
        "sections/two-character.tex",
        "sections/three-modulus.tex",
        "experiments/tpc37_certificate.py",
    ]
    source_hashes: Dict[str, str] = {}
    for relative in source_relatives:
        source_path = paper_directory / relative
        require(source_path.is_file(), f"missing certificate source: {relative}")
        source_hashes[relative] = sha256_bytes(source_path.read_bytes())

    report: Dict[str, object] = {
        "schema": "tpc37-exact-certificate-v1",
        "status": "pass",
        "arithmetic": "exact integers, rational numbers, and cyclotomic quotient rings",
        "source_constraints": verify_source_constraints(script_path),
        "source_sha256": source_hashes,
        "physical_zero_faces": [
            verify_physical_zero_faces(prime) for prime in (5, 7, 11)
        ],
        "punctured_centering": [
            verify_punctured_centering(prime) for prime in (5, 7, 11)
        ],
        "jacobi_near_isometry": [
            verify_jacobi_matrix(prime) for prime in (5, 7, 11)
        ],
        "crt_face_calculus": [
            verify_crt_faces((3, 5, 7), 2),
            verify_crt_faces((5, 7, 11), 2),
        ],
        "determinant_periodization_and_ghosts": verify_determinant_periodization(),
    }
    report["certificate_digest"] = canonical_digest(report)
    return report


def main() -> int:
    script_path = Path(__file__).resolve()
    output_path = script_path.with_suffix(".json")
    report = build_report(script_path)
    encoded = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    output_path.write_text(encoded, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "certificate": str(output_path),
                "digest": report["certificate_digest"],
                "status": report["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateError as error:
        print(json.dumps({"status": "fail", "error": str(error)}, sort_keys=True))
        raise SystemExit(1)
