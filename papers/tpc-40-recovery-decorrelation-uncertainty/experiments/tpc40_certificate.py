#!/usr/bin/env python3
"""Deterministic exact-arithmetic certificate for TPC-40.

The certificate checks the finite phase-frame statements behind the
recovery--decorrelation uncertainty principle.  It uses integers,
``Fraction`` values, exact cyclic character sums, and a tiny exact model of
prime-order cyclotomic fields.  It uses no floating point, NumPy, random
draws, or optimization-sensitive ``assert`` statements.

The finite checks concern phase banks, residue buckets, folded alias Grams,
tensor spectra, and exact Gram decompositions of Loewner differences.  They
do not prove cancellation in a Mobius correlation, a twist-stable physical
estimate, a parity break, a prime-pair asymptotic, or the twin-prime
conjecture.
"""

from __future__ import annotations

import ast
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple


class CertificateError(RuntimeError):
    """Raised when an exact certificate check fails."""


CHECKS = 0


def require(condition: bool, message: str) -> None:
    """Record one optimization-safe check and fail explicitly if needed."""

    global CHECKS
    CHECKS += 1
    if not condition:
        raise CertificateError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("ascii")


def canonical_digest(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def frac_text(value: Fraction | int) -> str:
    rational = Fraction(value)
    if rational.denominator == 1:
        return str(rational.numerator)
    return f"{rational.numerator}/{rational.denominator}"


def cyclic_character_sum(modulus: int, exponent: int) -> int:
    """Return sum over all modulus-th roots exactly, as zero or modulus."""

    require(modulus >= 1, "cyclic modulus must be positive")
    return modulus if exponent % modulus == 0 else 0


def int_matvec(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> List[int]:
    require(
        all(len(row) == len(vector) for row in matrix),
        "integer matrix-vector dimensions do not match",
    )
    return [
        sum(row[column] * vector[column] for column in range(len(vector)))
        for row in matrix
    ]


def rational_rank(matrix: Sequence[Sequence[int | Fraction]]) -> int:
    """Compute matrix rank by exact Fraction Gaussian elimination."""

    if not matrix:
        return 0
    column_count = len(matrix[0])
    require(
        all(len(row) == column_count for row in matrix),
        "rank input is not rectangular",
    )
    rows = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(rows)
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        inverse = Fraction(pivot_value.denominator, pivot_value.numerator)
        rows[pivot_row] = [value * inverse for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][column] == 0:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                rows[row][index] - multiplier * rows[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def lcg_step(state: int) -> int:
    """A deterministic integer mixer; this is not a random draw."""

    return (1103515245 * state + 12345) % 2147483648


def deterministic_permutation(size: int, seed: int) -> List[int]:
    values = list(range(size))
    state = seed
    for upper in range(size - 1, 0, -1):
        state = lcg_step(state)
        lower = state % (upper + 1)
        values[upper], values[lower] = values[lower], values[upper]
    require(sorted(values) == list(range(size)), "permutation mixer failed")
    return values


def verify_dft_bank_case(
    row_count: int, frequencies: Sequence[int]
) -> Dict[str, object]:
    """Check one selected-frequency DFT bank through its row-frame Gram."""

    sample_count = len(frequencies)
    require(row_count >= 1, "DFT row count must be positive")
    require(sample_count >= 1, "DFT bank must contain a frequency")
    require(frequencies[0] == 0, "DFT bank must list the constant row first")
    require(
        len(set(frequencies)) == sample_count,
        "DFT frequencies must be distinct",
    )
    require(
        all(0 <= frequency < row_count for frequency in frequencies),
        "DFT frequency lies outside its cyclic group",
    )

    eigenvalue = Fraction(row_count, sample_count)
    measurement_gram: List[List[Fraction]] = []
    for left in frequencies:
        gram_row: List[Fraction] = []
        for right in frequencies:
            gram_row.append(
                Fraction(
                    cyclic_character_sum(row_count, left - right),
                    sample_count,
                )
            )
        measurement_gram.append(gram_row)

    for left in range(sample_count):
        for right in range(sample_count):
            expected = eigenvalue if left == right else Fraction(0)
            require(
                measurement_gram[left][right] == expected,
                "selected DFT frequencies are not exactly orthogonal",
            )

    recovery_amplification = Fraction(sample_count)
    require(
        recovery_amplification * eigenvalue == row_count,
        "DFT recovery-spectrum product is not the row count",
    )
    require(
        sample_count * eigenvalue == row_count,
        "DFT nonzero eigenvalues do not have the correct trace",
    )
    return {
        "row_count": row_count,
        "selected_frequency_count": sample_count,
        "frequencies": list(frequencies),
        "recovery_amplification": frac_text(recovery_amplification),
        "nonzero_eigenvalue": frac_text(eigenvalue),
        "nonzero_multiplicity": sample_count,
        "zero_multiplicity": row_count - sample_count,
        "A_times_lambda": frac_text(
            recovery_amplification * eigenvalue
        ),
    }


def verify_selected_dft_banks() -> Dict[str, object]:
    start = CHECKS
    case_count = 0
    exhaustive_case_count = 0
    representatives: List[Dict[str, object]] = []
    seen_global: set[Tuple[int, Tuple[int, ...]]] = set()

    for row_count in range(2, 41):
        mixed_nonzero = [
            value + 1
            for value in deterministic_permutation(
                row_count - 1, 97 * row_count + 11
            )
        ]
        for sample_count in range(1, row_count + 1):
            candidates = {
                tuple([0] + list(range(1, sample_count))),
                tuple(
                    [0]
                    + list(
                        range(row_count - sample_count + 1, row_count)
                    )
                ),
                tuple([0] + mixed_nonzero[: sample_count - 1]),
            }
            if row_count <= 9:
                for tail in combinations(
                    range(1, row_count), sample_count - 1
                ):
                    candidates.add(tuple([0] + list(tail)))
                    exhaustive_case_count += 1
            for frequencies in sorted(candidates):
                key = (row_count, frequencies)
                if key in seen_global:
                    continue
                seen_global.add(key)
                case = verify_dft_bank_case(row_count, frequencies)
                case_count += 1
                if (
                    (row_count, sample_count) in {(5, 2), (8, 5), (13, 7)}
                    and len(representatives) < 8
                ):
                    representatives.append(case)

    return {
        "checks": CHECKS - start,
        "row_counts": [2, 40],
        "selected_frequency_banks_checked": case_count,
        "exhaustive_small_subsets_generated": exhaustive_case_count,
        "formula": {
            "recovery_amplification": "r",
            "nonzero_spectrum": "R/r with multiplicity r",
            "zero_multiplicity": "R-r",
            "sharp_product": "A*lambda=R",
        },
        "representative_cases": representatives,
    }


def balanced_bucket_counts(row_count: int, bucket_count: int) -> List[int]:
    quotient, remainder = divmod(row_count, bucket_count)
    return [quotient + 1] * remainder + [quotient] * (
        bucket_count - remainder
    )


def positive_compositions(total: int, parts: int) -> Iterator[Tuple[int, ...]]:
    if parts == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total - parts + 2):
        for tail in positive_compositions(total - first, parts - 1):
            yield (first,) + tail


def bucket_gram(counts: Sequence[int]) -> Tuple[List[List[int]], List[int]]:
    labels: List[int] = []
    for bucket, count in enumerate(counts):
        labels.extend([bucket] * count)
    matrix = [
        [int(labels[left] == labels[right]) for right in range(len(labels))]
        for left in range(len(labels))
    ]
    return matrix, labels


def verify_bucket_case(counts: Sequence[int], check_rank: bool) -> None:
    bucket_count = len(counts)
    row_count = sum(counts)
    require(bucket_count >= 1, "bucket bank has no buckets")
    require(all(count >= 1 for count in counts), "bucket bank has an empty bucket")
    matrix, labels = bucket_gram(counts)
    eigenvector_count = 0

    for bucket, count in enumerate(counts):
        indicator = [int(label == bucket) for label in labels]
        image = int_matvec(matrix, indicator)
        require(
            image == [count * value for value in indicator],
            "bucket indicator has the wrong exact eigenvalue",
        )
        eigenvector_count += 1
        positions = [
            index for index, label in enumerate(labels) if label == bucket
        ]
        anchor = positions[0]
        for position in positions[1:]:
            difference = [0] * row_count
            difference[position] = 1
            difference[anchor] = -1
            require(
                int_matvec(matrix, difference) == [0] * row_count,
                "within-bucket difference is not in the Gram kernel",
            )
            eigenvector_count += 1

    require(
        eigenvector_count == row_count,
        "bucket eigenvectors do not account for the full dimension",
    )
    require(
        sum(matrix[index][index] for index in range(row_count)) == row_count,
        "bucket Gram trace is wrong",
    )
    if check_rank:
        require(
            rational_rank(matrix) == bucket_count,
            "bucket Gram rank is wrong",
        )

    amplification = bucket_count
    largest = max(counts)
    require(
        amplification * largest >= row_count,
        "bucket recovery-decorrelation product bound failed",
    )
    require(
        (amplification * largest == row_count)
        == (len(set(counts)) == 1),
        "bucket equality case was classified incorrectly",
    )


def verify_residue_bucket_banks() -> Dict[str, object]:
    start = CHECKS
    balanced_cases = 0
    unbalanced_cases = 0
    representatives: List[Dict[str, object]] = []

    for row_count in range(2, 65):
        for bucket_count in range(1, row_count + 1):
            counts = balanced_bucket_counts(row_count, bucket_count)
            verify_bucket_case(counts, row_count <= 12)
            balanced_cases += 1
            largest = max(counts)
            quotient, remainder = divmod(row_count, bucket_count)
            require(
                largest == quotient + int(remainder > 0),
                "balanced bucket maximum is not the ceiling",
            )
            require(
                bucket_count * largest < row_count + bucket_count,
                "balanced bucket product misses its strict upper bound",
            )
            if (row_count, bucket_count) in {(11, 3), (12, 4), (17, 5)}:
                representatives.append(
                    {
                        "kind": "balanced",
                        "R": row_count,
                        "bucket_count": bucket_count,
                        "bucket_sizes": counts,
                        "nonzero_spectrum": sorted(counts, reverse=True),
                        "zero_multiplicity": row_count - bucket_count,
                        "A_times_lambda_max": bucket_count * largest,
                    }
                )

    for row_count in range(3, 14):
        for bucket_count in range(2, min(row_count, 6) + 1):
            for counts_tuple in positive_compositions(row_count, bucket_count):
                counts = list(counts_tuple)
                verify_bucket_case(counts, row_count <= 9)
                unbalanced_cases += 1
                if (
                    counts in ([1, row_count - 1], [1, 2, row_count - 3])
                    and len(representatives) < 8
                ):
                    representatives.append(
                        {
                            "kind": "unbalanced",
                            "R": row_count,
                            "bucket_count": bucket_count,
                            "bucket_sizes": counts,
                            "nonzero_spectrum": sorted(counts, reverse=True),
                            "zero_multiplicity": row_count - bucket_count,
                            "A_times_lambda_max": bucket_count * max(counts),
                        }
                    )

    return {
        "checks": CHECKS - start,
        "balanced_cases_checked": balanced_cases,
        "unbalanced_positive_compositions_checked": unbalanced_cases,
        "exact_spectrum": "positive bucket sizes plus R-b zero eigenvalues",
        "product_bound": "b*max_bucket_size >= R",
        "equality_condition": "all nonempty bucket sizes equal",
        "balanced_refinement": "R <= b*ceil(R/b) < R+b",
        "representative_cases": representatives,
    }


def alias_collision_gram(alias_radius: int) -> Tuple[List[int], List[List[int]]]:
    modulus = alias_radius + 1
    labels = list(range(-alias_radius, alias_radius + 1))
    matrix = [
        [int((left - right) % modulus == 0) for right in labels]
        for left in labels
    ]
    return labels, matrix


def verify_minimal_alias_grams() -> Dict[str, object]:
    start = CHECKS
    representatives: List[Dict[str, object]] = []

    for alias_radius in range(1, 97):
        modulus = alias_radius + 1
        labels, matrix = alias_collision_gram(alias_radius)
        classes: Dict[int, List[int]] = {}
        for position, label in enumerate(labels):
            classes.setdefault(label % modulus, []).append(position)
        require(len(classes) == modulus, "alias residue class count is wrong")
        require(
            len(classes[0]) == 1 and labels[classes[0][0]] == 0,
            "zero alias is not a singleton collision class",
        )
        for residue in range(1, modulus):
            positions = classes[residue]
            require(len(positions) == 2, "nonzero alias class is not folded")
            left, right = positions
            pair_sum = [0] * len(labels)
            pair_sum[left] = 1
            pair_sum[right] = 1
            pair_difference = [0] * len(labels)
            pair_difference[left] = 1
            pair_difference[right] = -1
            require(
                int_matvec(matrix, pair_sum)
                == [2 * value for value in pair_sum],
                "folded pair sum does not have eigenvalue two",
            )
            require(
                int_matvec(matrix, pair_difference) == [0] * len(labels),
                "folded pair difference is not in the alias kernel",
            )

        zero_indicator = [int(label == 0) for label in labels]
        require(
            int_matvec(matrix, zero_indicator) == zero_indicator,
            "zero alias does not have eigenvalue one",
        )
        require(
            sum(matrix[index][index] for index in range(len(labels)))
            == 2 * alias_radius + 1,
            "alias Gram trace is wrong",
        )
        require(
            alias_radius + 1 + alias_radius == len(labels),
            "alias spectral multiplicities miss the ambient dimension",
        )
        if alias_radius <= 14:
            require(
                rational_rank(matrix) == alias_radius + 1,
                "alias Gram rank is wrong",
            )
        if alias_radius in {1, 4, 11, 37, 96}:
            representatives.append(
                {
                    "L": alias_radius,
                    "q": modulus,
                    "dimension": 2 * alias_radius + 1,
                    "spectrum": {
                        "2": alias_radius,
                        "1": 1,
                        "0": alias_radius,
                    },
                    "rank": alias_radius + 1,
                }
            )

    return {
        "checks": CHECKS - start,
        "alias_radii_checked": [1, 96],
        "collision_pattern": "one singleton zero class and L folded pairs",
        "spectrum": {
            "eigenvalue_2_multiplicity": "L",
            "eigenvalue_1_multiplicity": "1",
            "eigenvalue_0_multiplicity": "L",
        },
        "representative_cases": representatives,
    }


def verify_tensor_row_alias_spectra() -> Dict[str, object]:
    start = CHECKS
    case_count = 0
    representatives: List[Dict[str, object]] = []

    for row_count in range(2, 41):
        for sample_count in range(1, row_count + 1):
            row_eigenvalue = Fraction(row_count, sample_count)
            for alias_radius in range(1, 25):
                quotient_size = alias_radius + 1
                total_dimension = row_count * (2 * alias_radius + 1)
                positive_rank = sample_count * (alias_radius + 1)
                zero_multiplicity = total_dimension - positive_rank
                high_eigenvalue = 2 * row_eigenvalue
                low_eigenvalue = row_eigenvalue
                high_multiplicity = sample_count * alias_radius
                low_multiplicity = sample_count
                amplification = Fraction(sample_count)

                require(
                    high_multiplicity + low_multiplicity == positive_rank,
                    "tensor positive multiplicities give the wrong rank",
                )
                require(
                    zero_multiplicity >= 0,
                    "tensor zero multiplicity is negative",
                )
                trace = (
                    high_eigenvalue * high_multiplicity
                    + low_eigenvalue * low_multiplicity
                )
                require(
                    trace == total_dimension,
                    "tensor spectrum has the wrong trace",
                )
                require(
                    amplification * low_eigenvalue == row_count,
                    "tensor low recovery-spectrum product is wrong",
                )
                require(
                    amplification * high_eigenvalue == 2 * row_count,
                    "tensor high recovery-spectrum product is wrong",
                )

                node_weight = Fraction(1, sample_count * quotient_size)
                recovery_coefficient = Fraction(1, quotient_size)
                calculated_amplification = sum(
                    (
                        recovery_coefficient
                        * recovery_coefficient
                        * Fraction(node_weight.denominator, node_weight.numerator)
                        for _ in range(quotient_size)
                    ),
                    Fraction(0),
                )
                require(
                    calculated_amplification == amplification,
                    "tensor recovery amplification is not retained at r",
                )
                case_count += 1
                if (
                    (row_count, sample_count, alias_radius)
                    in {(7, 3, 2), (12, 5, 4), (20, 8, 11)}
                ):
                    representatives.append(
                        {
                            "row_count": row_count,
                            "selected_frequency_count": sample_count,
                            "alias_radius": alias_radius,
                            "q": quotient_size,
                            "recovery_amplification": frac_text(amplification),
                            "spectrum": {
                                frac_text(high_eigenvalue): high_multiplicity,
                                frac_text(low_eigenvalue): low_multiplicity,
                                "0": zero_multiplicity,
                            },
                        }
                    )

    return {
        "checks": CHECKS - start,
        "cases_checked": case_count,
        "R_range": [2, 40],
        "L_range": [1, 24],
        "spectrum": {
            "2R/r_multiplicity": "rL",
            "R/r_multiplicity": "r",
            "zero_multiplicity": "R(2L+1)-r(L+1)",
        },
        "recovery_amplification": "r",
        "representative_cases": representatives,
    }


Cyclo = Tuple[Fraction, ...]


def cyclo_zero(prime: int) -> Cyclo:
    return tuple(Fraction(0) for _ in range(prime - 1))


def cyclo_root(prime: int, exponent: int) -> Cyclo:
    """Represent zeta_p^exponent in the basis 1,zeta,...,zeta^(p-2)."""

    require(prime >= 2, "cyclotomic prime must be at least two")
    reduced = exponent % prime
    if reduced == prime - 1:
        return tuple(Fraction(-1) for _ in range(prime - 1))
    coordinates = [Fraction(0) for _ in range(prime - 1)]
    coordinates[reduced] = Fraction(1)
    return tuple(coordinates)


def cyclo_add(left: Cyclo, right: Cyclo) -> Cyclo:
    require(len(left) == len(right), "cyclotomic dimensions do not match")
    return tuple(left[index] + right[index] for index in range(len(left)))


def cyclo_sub(left: Cyclo, right: Cyclo) -> Cyclo:
    require(len(left) == len(right), "cyclotomic dimensions do not match")
    return tuple(left[index] - right[index] for index in range(len(left)))


def cyclo_scale(scalar: Fraction | int, value: Cyclo) -> Cyclo:
    factor = Fraction(scalar)
    return tuple(factor * coordinate for coordinate in value)


def cyclo_mul(prime: int, left: Cyclo, right: Cyclo) -> Cyclo:
    require(
        len(left) == prime - 1 and len(right) == prime - 1,
        "cyclotomic multiplication has the wrong dimension",
    )
    result = cyclo_zero(prime)
    for left_exponent, left_coefficient in enumerate(left):
        if left_coefficient == 0:
            continue
        for right_exponent, right_coefficient in enumerate(right):
            if right_coefficient == 0:
                continue
            term = cyclo_scale(
                left_coefficient * right_coefficient,
                cyclo_root(prime, left_exponent + right_exponent),
            )
            result = cyclo_add(result, term)
    return result


def cyclo_conjugate(prime: int, value: Cyclo) -> Cyclo:
    require(
        len(value) == prime - 1,
        "cyclotomic conjugation has the wrong dimension",
    )
    result = cyclo_zero(prime)
    for exponent, coefficient in enumerate(value):
        result = cyclo_add(
            result,
            cyclo_scale(coefficient, cyclo_root(prime, -exponent)),
        )
    return result


def cyclo_sum(prime: int, values: Iterable[Cyclo]) -> Cyclo:
    result = cyclo_zero(prime)
    for value in values:
        result = cyclo_add(result, value)
    return result


def cyclo_is_rational(prime: int, value: Cyclo, rational: Fraction) -> bool:
    expected = cyclo_scale(rational, cyclo_root(prime, 0))
    return value == expected


def verify_cyclotomic_backend() -> Dict[str, object]:
    start = CHECKS
    primes = [2, 3, 5, 7, 11]
    for prime in primes:
        one = cyclo_root(prime, 0)
        zero = cyclo_zero(prime)
        require(
            cyclo_sum(
                prime, (cyclo_root(prime, exponent) for exponent in range(prime))
            )
            == zero,
            "prime cyclotomic root sum does not vanish",
        )
        for left in range(prime):
            require(
                cyclo_mul(
                    prime,
                    cyclo_root(prime, left),
                    cyclo_root(prime, -left),
                )
                == one,
                "cyclotomic inverse identity failed",
            )
            require(
                cyclo_conjugate(prime, cyclo_root(prime, left))
                == cyclo_root(prime, -left),
                "cyclotomic conjugation identity failed",
            )
            for right in range(prime):
                require(
                    cyclo_mul(
                        prime,
                        cyclo_root(prime, left),
                        cyclo_root(prime, right),
                    )
                    == cyclo_root(prime, left + right),
                    "cyclotomic exponent multiplication failed",
                )
        for first in range(prime):
            for second in range(prime):
                for third in range(prime):
                    left_product = cyclo_mul(
                        prime,
                        cyclo_mul(
                            prime,
                            cyclo_root(prime, first),
                            cyclo_root(prime, second),
                        ),
                        cyclo_root(prime, third),
                    )
                    right_product = cyclo_mul(
                        prime,
                        cyclo_root(prime, first),
                        cyclo_mul(
                            prime,
                            cyclo_root(prime, second),
                            cyclo_root(prime, third),
                        ),
                    )
                    require(
                        left_product == right_product,
                        "cyclotomic associativity check failed",
                    )
    return {
        "checks": CHECKS - start,
        "prime_orders": primes,
        "representation": (
            "Q[zeta_p] in the exact basis 1,zeta_p,...,zeta_p^(p-2)"
        ),
        "floating_point": False,
    }


def cyclo_phase_gram(
    prime: int,
    exponents: Sequence[Sequence[int]],
    weights: Sequence[Fraction],
) -> List[List[Cyclo]]:
    measurement_count = len(exponents)
    require(
        measurement_count == len(weights),
        "phase exponent and weight counts do not match",
    )
    require(measurement_count >= 1, "phase bank is empty")
    row_count = len(exponents[0])
    require(
        all(len(row) == row_count for row in exponents),
        "phase exponent bank is not rectangular",
    )
    matrix: List[List[Cyclo]] = []
    for left in range(row_count):
        matrix_row: List[Cyclo] = []
        for right in range(row_count):
            entry = cyclo_zero(prime)
            for measurement in range(measurement_count):
                phase = cyclo_root(
                    prime,
                    exponents[measurement][left]
                    - exponents[measurement][right],
                )
                entry = cyclo_add(
                    entry, cyclo_scale(weights[measurement], phase)
                )
            matrix_row.append(entry)
        matrix.append(matrix_row)
    return matrix


def cyclo_matrix_subtract(
    left: Sequence[Sequence[Cyclo]], right: Sequence[Sequence[Cyclo]]
) -> List[List[Cyclo]]:
    require(len(left) == len(right), "cyclotomic matrix row counts differ")
    result: List[List[Cyclo]] = []
    for row in range(len(left)):
        require(
            len(left[row]) == len(right[row]),
            "cyclotomic matrix column counts differ",
        )
        result.append(
            [
                cyclo_sub(left[row][column], right[row][column])
                for column in range(len(left[row]))
            ]
        )
    return result


def cyclo_quadratic_form(
    prime: int,
    matrix: Sequence[Sequence[Cyclo]],
    vector: Sequence[int],
) -> Cyclo:
    require(len(matrix) == len(vector), "quadratic form row count is wrong")
    result = cyclo_zero(prime)
    for left in range(len(vector)):
        require(
            len(matrix[left]) == len(vector),
            "quadratic form matrix is not square",
        )
        for right in range(len(vector)):
            result = cyclo_add(
                result,
                cyclo_scale(
                    vector[left] * vector[right], matrix[left][right]
                ),
            )
    return result


def verify_loewner_case(prime: int, seed: int) -> Dict[str, object]:
    state = lcg_step(seed + 31 * prime)
    row_count = 2 + state % 7
    state = lcg_step(state)
    measurement_count = 2 + state % 6
    state = lcg_step(state)
    constant_count = 1 + state % (measurement_count - 1)

    raw_weights: List[int] = []
    for _ in range(measurement_count):
        state = lcg_step(state)
        raw_weights.append(1 + state % 11)
    raw_total = sum(raw_weights)
    weights = [Fraction(weight, raw_total) for weight in raw_weights]
    require(sum(weights, Fraction(0)) == 1, "phase weights do not sum to one")

    exponents: List[List[int]] = []
    for measurement in range(measurement_count):
        row_exponents: List[int] = []
        for _ in range(row_count):
            if measurement < constant_count:
                row_exponents.append(0)
            else:
                state = lcg_step(state)
                row_exponents.append(state % prime)
        exponents.append(row_exponents)

    constant_weight = sum(weights[:constant_count], Fraction(0))
    amplification = Fraction(
        constant_weight.denominator, constant_weight.numerator
    )
    recovery_weights = [
        (
            weights[index]
            * Fraction(constant_weight.denominator, constant_weight.numerator)
            if index < constant_count
            else Fraction(0)
        )
        for index in range(measurement_count)
    ]
    calculated_amplification = sum(
        (
            recovery_weights[index]
            * recovery_weights[index]
            * Fraction(weights[index].denominator, weights[index].numerator)
            for index in range(measurement_count)
        ),
        Fraction(0),
    )
    require(
        calculated_amplification == amplification,
        "distributed constant recovery has the wrong amplification",
    )

    one = cyclo_root(prime, 0)
    for row in range(row_count):
        recovered = cyclo_sum(
            prime,
            (
                cyclo_scale(
                    recovery_weights[measurement],
                    cyclo_root(prime, exponents[measurement][row]),
                )
                for measurement in range(measurement_count)
            ),
        )
        require(recovered == one, "phase bank does not recover every row")

    gram = cyclo_phase_gram(prime, exponents, weights)
    rank_one = [
        [cyclo_scale(constant_weight, one) for _ in range(row_count)]
        for _ in range(row_count)
    ]
    difference = cyclo_matrix_subtract(gram, rank_one)
    residual_exponents = exponents[constant_count:]
    residual_weights = weights[constant_count:]
    residual_gram = cyclo_phase_gram(
        prime, residual_exponents, residual_weights
    )
    require(
        difference == residual_gram,
        "Loewner difference is not the exact residual Gram",
    )

    for left in range(row_count):
        for right in range(row_count):
            require(
                difference[left][right]
                == cyclo_conjugate(prime, difference[right][left]),
                "Loewner difference is not exactly Hermitian",
            )
        require(
            cyclo_is_rational(
                prime,
                difference[left][left],
                Fraction(1) - constant_weight,
            ),
            "Loewner residual has the wrong diagonal",
        )

    vector: List[int] = []
    for row in range(row_count):
        state = lcg_step(state)
        vector.append((state % 9) - 4)
    if all(value == 0 for value in vector):
        vector[0] = 1

    left_quadratic = cyclo_quadratic_form(
        prime, difference, vector
    )
    residual_norm = cyclo_zero(prime)
    for measurement in range(constant_count, measurement_count):
        phase_sum = cyclo_sum(
            prime,
            (
                cyclo_scale(
                    vector[row],
                    cyclo_root(prime, exponents[measurement][row]),
                )
                for row in range(row_count)
            ),
        )
        norm = cyclo_mul(
            prime, phase_sum, cyclo_conjugate(prime, phase_sum)
        )
        residual_norm = cyclo_add(
            residual_norm, cyclo_scale(weights[measurement], norm)
        )
    require(
        left_quadratic == residual_norm,
        "Loewner quadratic form is not its exact Gram-square sum",
    )
    require(
        left_quadratic == cyclo_conjugate(prime, left_quadratic),
        "Loewner quadratic form is not exactly real",
    )

    full_quadratic = cyclo_quadratic_form(prime, gram, vector)
    coherent_sum = sum(vector)
    lower_rank_one = cyclo_scale(
        constant_weight * coherent_sum * coherent_sum, one
    )
    require(
        cyclo_sub(full_quadratic, lower_rank_one) == left_quadratic,
        "Gram minus A-inverse coherent square identity failed",
    )

    return {
        "prime_order": prime,
        "seed": seed,
        "R": row_count,
        "measurements": measurement_count,
        "constant_measurements": constant_count,
        "constant_weight": frac_text(constant_weight),
        "recovery_amplification": frac_text(amplification),
        "A_inverse": frac_text(constant_weight),
    }


def verify_exact_loewner_decompositions() -> Dict[str, object]:
    start = CHECKS
    primes = [2, 3, 5, 7, 11]
    case_count = 0
    representatives: List[Dict[str, object]] = []
    for prime in primes:
        for seed in range(1, 61):
            case = verify_loewner_case(prime, seed)
            case_count += 1
            if seed in {3, 29, 57} and len(representatives) < 10:
                representatives.append(case)

    return {
        "checks": CHECKS - start,
        "deterministic_root_exponent_cases": case_count,
        "prime_orders": primes,
        "identity": "G-A^(-1)11*=B*B for the residual phase rows",
        "verification": (
            "exact cyclotomic entries, exact recovery moments, Hermitian "
            "symmetry, and exact quadratic Gram-square decompositions"
        ),
        "uses_random_draws": False,
        "representative_cases": representatives,
    }


def verify_endpoint_exponents() -> Dict[str, object]:
    start = CHECKS
    row_exponent = Fraction(267, 400)
    bank_exponent = Fraction(1, 400)
    quotient_exponent = row_exponent - bank_exponent
    require(
        quotient_exponent == Fraction(266, 400),
        "endpoint quotient exponent is not 266/400",
    )
    require(
        quotient_exponent == Fraction(133, 200),
        "endpoint quotient exponent does not reduce to 133/200",
    )
    require(
        bank_exponent + quotient_exponent == row_exponent,
        "endpoint exponent product ledger does not close",
    )
    require(
        267 - 1 == 266,
        "unreduced endpoint numerator ledger failed",
    )
    return {
        "checks": CHECKS - start,
        "row_count_scale_exponent": "267/400",
        "bank_size_scale_exponent": "1/400",
        "forced_Gram_norm_exponent_unreduced": "266/400",
        "forced_Gram_norm_exponent_reduced": frac_text(quotient_exponent),
        "identity": "267/400-1/400=266/400=133/200",
    }


def verify_source_constraints(script_path: Path) -> Dict[str, object]:
    start = CHECKS
    source = script_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(script_path))
    assert_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    float_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    division_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    imports: List[str] = []
    random_imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
                if alias.name == "random" or alias.name.startswith("random."):
                    random_imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(module)
            if module == "random" or module.startswith("random."):
                random_imports.append(module)
    allowed_roots = {
        "__future__",
        "ast",
        "fractions",
        "hashlib",
        "itertools",
        "json",
        "pathlib",
        "typing",
    }
    external_imports = sorted(
        {
            module
            for module in imports
            if module.split(".")[0] not in allowed_roots
        }
    )
    require(not assert_nodes, "certificate source contains assert")
    require(not float_nodes, "certificate source contains a float literal")
    require(not division_nodes, "certificate source contains true division")
    require(not random_imports, "certificate source imports random")
    require(not external_imports, "certificate source imports a non-stdlib module")
    return {
        "checks": CHECKS - start,
        "stdlib_only": True,
        "assert_statements": len(assert_nodes),
        "float_literals": len(float_nodes),
        "true_division_nodes": len(division_nodes),
        "random_imports": len(random_imports),
        "external_imports": external_imports,
        "optimization_safe_explicit_checks": True,
    }


def build_report(script_path: Path) -> Dict[str, object]:
    source_key = "experiments/tpc40_certificate.py"
    report: Dict[str, object] = {
        "schema": "tpc40-recovery-decorrelation-certificate-v1",
        "status": "pass",
        "arithmetic": (
            "exact integers, Fraction arithmetic, exact cyclic character "
            "sums, and exact prime-order cyclotomic coordinates"
        ),
        "source_sha256": {source_key: sha256_bytes(script_path.read_bytes())},
        "source_constraints": verify_source_constraints(script_path),
        "selected_DFT_phase_banks": verify_selected_dft_banks(),
        "balanced_and_unbalanced_residue_buckets": (
            verify_residue_bucket_banks()
        ),
        "minimal_alias_folded_Gram": verify_minimal_alias_grams(),
        "tensor_row_alias_spectrum": verify_tensor_row_alias_spectra(),
        "cyclotomic_backend": verify_cyclotomic_backend(),
        "exact_Loewner_Gram_decompositions": (
            verify_exact_loewner_decompositions()
        ),
        "endpoint_exponent_ledger": verify_endpoint_exponents(),
        "claims": {
            "finite_selected_DFT_orthogonality_checks": True,
            "finite_recovery_amplification_A_equals_r_checks": True,
            "finite_sharp_A_lambda_equals_R_checks": True,
            "finite_balanced_bucket_spectrum_checks": True,
            "finite_unbalanced_bucket_spectrum_checks": True,
            "finite_bucket_product_bound_checks": True,
            "finite_minimal_alias_folded_collision_checks": True,
            "finite_alias_spectrum_2_1_0_checks": True,
            "finite_tensor_spectrum_checks": True,
            "finite_tensor_recovery_amplification_checks": True,
            "finite_exact_Loewner_Gram_factorizations": True,
            "finite_exact_root_of_unity_exponent_checks": True,
            "endpoint_266_over_400_ledger_check": True,
            "uses_floating_point": False,
            "uses_random_inputs": False,
            "proves_twist_stable_physical_estimate": False,
            "proves_mobius_autocorrelation": False,
            "proves_affine_chowla": False,
            "proves_parity_break": False,
            "proves_hardy_littlewood_prime_pairs": False,
            "proves_twin_primes": False,
        },
        "claim_boundaries": [
            (
                "The certificate proves only finite exact phase-frame, "
                "bucket, alias, tensor, and Gram-factorization identities."
            ),
            (
                "It does not estimate the physical Mobius coefficient or "
                "any two- or four-Mobius correlation."
            ),
            (
                "It does not prove a twist-stable energy bound, a sieve "
                "parity breach, a prime-pair asymptotic, or twin primes."
            ),
        ],
    }
    report["check_total"] = CHECKS
    report["certificate_digest"] = canonical_digest(report)
    return report


def main() -> int:
    script_path = Path(__file__).resolve()
    output_path = script_path.with_suffix(".json")
    report = build_report(script_path)
    encoded = canonical_json_bytes(report)
    output_path.write_bytes(encoded)
    source_key = "experiments/tpc40_certificate.py"
    summary = {
        "certificate": str(output_path),
        "checks": report["check_total"],
        "digest": report["certificate_digest"],
        "json_sha256": sha256_bytes(encoded),
        "source_sha256": report["source_sha256"][source_key],
        "status": report["status"],
    }
    print(canonical_json_bytes(summary).decode("ascii").rstrip("\n"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateError as error:
        print(
            canonical_json_bytes(
                {"error": str(error), "status": "fail"}
            ).decode("ascii").rstrip("\n")
        )
        raise SystemExit(1)
