#!/usr/bin/env python3
"""Deterministic exact-arithmetic certificate for TPC-39.

The finite model has alias labels ``k = -L, ..., L`` and additive quotient
twists modulo ``q``.  The normalized twist Gram is the collision matrix

    G[k,l] = (1/q) sum_{nu mod q} e_q(nu * (k-l))
           = 1_{k == l (mod q)}.

All computations below use integers and ``Fraction`` values.  Roots of unity
are handled only through exact cyclic orthogonality; no root is approximated
numerically.  The Monte Carlo section enumerates every second-moment monomial
using exact Haar character integrals and finite cyclic character sums.  It
does not draw random inputs.  In particular, it distinguishes continuous
Haar variance from the folded variance of the minimal finite twist grid.

Every failed check raises ``CertificateError`` explicitly.  There are no
``assert`` statements, floating-point literals, true-division expressions, or
random imports, so ``python`` and ``python -O`` execute the same certificate.

The certificate verifies finite additive tomography identities.  It does not
prove a twist-stable Mobius estimate, an alias-column analytic bound, a parity
break, a prime-pair asymptotic, or the twin-prime conjecture.
"""

from __future__ import annotations

import ast
import hashlib
import json
from fractions import Fraction
from itertools import product as cartesian_product
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


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


def vector_add(
    left: Sequence[Fraction], right: Sequence[Fraction]
) -> List[Fraction]:
    require(len(left) == len(right), "vector dimensions do not match")
    return [left[index] + right[index] for index in range(len(left))]


def vector_scale(
    scalar: Fraction | int, vector: Sequence[Fraction]
) -> List[Fraction]:
    return [Fraction(scalar) * value for value in vector]


def zero_vector(dimension: int) -> List[Fraction]:
    return [Fraction(0) for _ in range(dimension)]


def inner_product(
    left: Sequence[Fraction], right: Sequence[Fraction]
) -> Fraction:
    require(len(left) == len(right), "inner-product dimensions do not match")
    return sum(
        (left[index] * right[index] for index in range(len(left))),
        Fraction(0),
    )


def norm_squared(vector: Sequence[Fraction]) -> Fraction:
    return inner_product(vector, vector)


def cyclic_character_sum(modulus: int, exponent: int) -> int:
    """Return ``sum_{nu mod q} e_q(nu*exponent)`` exactly."""

    require(modulus >= 2, "additive modulus must be at least two")
    return modulus if exponent % modulus == 0 else 0


def normalized_root_average(modulus: int, exponent: int) -> int:
    """Return the normalized cyclic character average, which is zero or one."""

    total = cyclic_character_sum(modulus, exponent)
    require(total in (0, modulus), "cyclic sum is not a projector")
    return 1 if total == modulus else 0


def deterministic_alias_vectors(
    alias_labels: Sequence[int], dimension: int, salt: int
) -> Dict[int, List[Fraction]]:
    """Produce nontrivial rational Hilbert vectors without random input."""

    vectors: Dict[int, List[Fraction]] = {}
    for label in alias_labels:
        coordinates: List[Fraction] = []
        for coordinate in range(dimension):
            numerator = (
                ((label + 37) * (coordinate + 5) + 7 * salt + 3 * coordinate)
                % 29
            ) - 14
            denominator = coordinate + 2 + (salt % 3)
            coordinates.append(Fraction(numerator, denominator))
        vectors[label] = coordinates
    return vectors


def folded_vectors(
    labels: Sequence[int],
    vectors: Dict[int, List[Fraction]],
    modulus: int,
) -> Dict[int, List[Fraction]]:
    dimension = len(vectors[labels[0]])
    folded = {residue: zero_vector(dimension) for residue in range(modulus)}
    for label in labels:
        residue = label % modulus
        folded[residue] = vector_add(folded[residue], vectors[label])
    return folded


def collision_classes(labels: Sequence[int], modulus: int) -> List[List[int]]:
    classes: Dict[int, List[int]] = {}
    for position, label in enumerate(labels):
        classes.setdefault(label % modulus, []).append(position)
    return [classes[residue] for residue in sorted(classes)]


def collision_gram(labels: Sequence[int], modulus: int) -> List[List[int]]:
    return [
        [normalized_root_average(modulus, left - right) for right in labels]
        for left in labels
    ]


def int_matvec(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> List[int]:
    return [
        sum(row[column] * vector[column] for column in range(len(vector)))
        for row in matrix
    ]


def rational_rank(matrix: Sequence[Sequence[int]]) -> int:
    """Compute rank by exact Gaussian elimination."""

    if not matrix:
        return 0
    rows = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0])
    require(
        all(len(row) == column_count for row in rows),
        "rank input is not rectangular",
    )
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
        pivot_inverse = Fraction(pivot_value.denominator, pivot_value.numerator)
        rows[pivot_row] = [
            value * pivot_inverse for value in rows[pivot_row]
        ]
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


def verify_minimal_identity_projector() -> Dict[str, object]:
    """Verify the sharp modulus for extracting only the zero alias."""

    start = CHECKS
    cases: List[Dict[str, object]] = []
    for radius in range(1, 65):
        labels = list(range(-radius, radius + 1))
        minimal_modulus = radius + 1

        for modulus in range(2, minimal_modulus):
            require(
                modulus in labels and modulus != 0,
                "small-modulus collision witness is outside the alias bank",
            )
            require(
                normalized_root_average(modulus, modulus) == 1,
                "small modulus unexpectedly removes its first nonzero alias",
            )

        projector = [
            normalized_root_average(minimal_modulus, label)
            for label in labels
        ]
        expected = [int(label == 0) for label in labels]
        require(projector == expected, "minimal zero-alias projector failed")
        require(
            all(
                normalized_root_average(modulus, label) == int(label == 0)
                for modulus in range(minimal_modulus, 2 * radius + 4)
                for label in labels
            ),
            "a modulus larger than the radius failed to isolate zero",
        )

        full_recovery_modulus = 2 * radius + 1
        require(
            len({label % full_recovery_modulus for label in labels})
            == len(labels),
            "full-recovery modulus has a collision",
        )
        for modulus in range(2, full_recovery_modulus):
            left = -radius
            right = left + modulus
            require(
                right <= radius and left != right,
                "full-recovery collision witness is outside the bank",
            )
            require(
                left % modulus == right % modulus,
                "full-recovery collision witness does not collide",
            )

        if radius in (1, 2, 3, 5, 8, 13, 21, 34, 64):
            cases.append(
                {
                    "L": radius,
                    "alias_count": 2 * radius + 1,
                    "minimal_modulus_for_zero_only": minimal_modulus,
                    "minimal_modulus_for_all_columns": full_recovery_modulus,
                }
            )

    return {
        "checks": CHECKS - start,
        "radii_checked": 64,
        "representative_cases": cases,
        "distinction": (
            "q=L+1 isolates k=0 although nonzero residue classes are folded; "
            "q=2L+1 is minimal for recovering every alias column"
        ),
    }


def verify_collision_gram_spectrum_and_parseval() -> Dict[str, object]:
    """Verify exact collision spectra and folded Hilbert-valued Parseval."""

    start = CHECKS
    case_count = 0
    entry_count = 0
    parseval_count = 0
    featured: List[Dict[str, object]] = []

    for radius in range(1, 19):
        labels = list(range(-radius, radius + 1))
        size = len(labels)
        vectors = deterministic_alias_vectors(labels, 4, radius)
        for modulus in range(2, 2 * radius + 4):
            gram = collision_gram(labels, modulus)
            classes = collision_classes(labels, modulus)
            class_sizes = [len(item) for item in classes]
            case_count += 1

            for left, left_label in enumerate(labels):
                for right, right_label in enumerate(labels):
                    require(
                        gram[left][right]
                        == int(left_label % modulus == right_label % modulus),
                        "normalized twist Gram is not the collision matrix",
                    )
                    entry_count += 1

            eigenvector_dimension = 0
            for positions in classes:
                indicator = [0 for _ in labels]
                for position in positions:
                    indicator[position] = 1
                require(
                    int_matvec(gram, indicator)
                    == [len(positions) * value for value in indicator],
                    "class-indicator eigenvector failed",
                )
                eigenvector_dimension += 1
                anchor = positions[-1]
                for position in positions[:-1]:
                    contrast = [0 for _ in labels]
                    contrast[position] = 1
                    contrast[anchor] = -1
                    require(
                        int_matvec(gram, contrast) == [0 for _ in labels],
                        "within-class null eigenvector failed",
                    )
                    eigenvector_dimension += 1
            require(
                eigenvector_dimension == size,
                "explicit collision eigenbasis has the wrong dimension",
            )

            trace = sum(gram[index][index] for index in range(size))
            trace_square = sum(
                gram[left][right] * gram[right][left]
                for left in range(size)
                for right in range(size)
            )
            require(trace == size, "collision Gram trace failed")
            require(
                sum(class_sizes) == size,
                "collision spectral trace identity failed",
            )
            require(
                trace_square == sum(value * value for value in class_sizes),
                "collision squared-trace identity failed",
            )
            distinct_rows = {tuple(row) for row in gram}
            require(
                len(distinct_rows) == len(classes),
                "collision matrix row-class rank identity failed",
            )
            require(
                rational_rank(gram) == len(classes),
                "exact Gaussian rank disagrees with the collision rank",
            )

            if radius < modulus <= 2 * radius + 1:
                expected_doubletons = 2 * radius + 1 - modulus
                expected_singletons = 2 * modulus - (2 * radius + 1)
                require(
                    class_sizes.count(2) == expected_doubletons,
                    "general tomography doubleton multiplicity failed",
                )
                require(
                    class_sizes.count(1) == expected_singletons,
                    "general tomography singleton multiplicity failed",
                )
                require(
                    all(value in (1, 2) for value in class_sizes),
                    "a no-wrap tomography bucket has size above two",
                )

            folded = folded_vectors(labels, vectors, modulus)
            folded_energy = sum(
                (norm_squared(vector) for vector in folded.values()),
                Fraction(0),
            )
            gram_energy = sum(
                (
                    Fraction(gram[left][right])
                    * inner_product(vectors[left_label], vectors[right_label])
                    for left, left_label in enumerate(labels)
                    for right, right_label in enumerate(labels)
                ),
                Fraction(0),
            )
            require(
                folded_energy == gram_energy,
                "folded rational Hilbert Parseval identity failed",
            )
            parseval_count += 1

            if modulus == radius + 1:
                require(
                    sorted(class_sizes) == [1] + [2 for _ in range(radius)],
                    "q=L+1 folded-class sizes failed",
                )
                zero_class = next(
                    positions
                    for positions in classes
                    if labels[positions[0]] % modulus == 0
                )
                require(
                    len(zero_class) == 1 and labels[zero_class[0]] == 0,
                    "q=L+1 identity class is not the singleton zero alias",
                )
                if radius in (2, 5, 11, 18):
                    featured.append(
                        {
                            "L": radius,
                            "q": modulus,
                            "dimension": size,
                            "rank": len(classes),
                            "nonzero_eigenvalues": {
                                "1": 1,
                                "2": radius,
                            },
                            "zero_multiplicity": radius,
                            "folded_parseval_energy": frac_text(folded_energy),
                        }
                    )
            if modulus >= 2 * radius + 1:
                require(gram == [
                    [int(left == right) for right in range(size)]
                    for left in range(size)
                ], "collision-free Gram is not the identity")

    return {
        "checks": CHECKS - start,
        "radii_checked": 18,
        "modulus_cases": case_count,
        "gram_entries_checked": entry_count,
        "rational_hilbert_parseval_cases": parseval_count,
        "featured_q_equals_L_plus_1_cases": featured,
    }


def verify_zero_recovery_and_partial_bank_counterexamples() -> Dict[str, object]:
    """Verify exact zero extraction and sharp missing-frequency witnesses."""

    start = CHECKS
    base = [Fraction(3), Fraction(-4, 5), Fraction(7, 3)]
    require(norm_squared(base) > 0, "partial-bank witness vector is zero")
    arbitrary_missing_cases = 0
    rational_cases: List[Dict[str, object]] = []

    for radius in range(1, 25):
        modulus = radius + 1
        labels = list(range(-radius, radius + 1))
        vectors = deterministic_alias_vectors(labels, 3, 2 * radius + 1)

        recovered = zero_vector(3)
        for label in labels:
            coefficient = normalized_root_average(modulus, label)
            recovered = vector_add(
                recovered, vector_scale(coefficient, vectors[label])
            )
        require(recovered == vectors[0], "full twist bank did not recover Z_0")

        # Rational witness 1: the untwisted measurement alone cannot recover
        # zero.  Z_0=v and Z_1=-v give Y_0=0.
        untwisted_sum = vector_add(base, vector_scale(-1, base))
        require(
            untwisted_sum == zero_vector(len(base)),
            "untwisted-only rational witness failed",
        )

        # Rational witness 2: put the same residue sum v in every quotient
        # class.  Every nonzero twist vanishes, while the zero class is v.
        dc_deleted_vectors = {
            label: zero_vector(len(base)) for label in labels
        }
        for residue in range(modulus):
            require(
                residue in dc_deleted_vectors,
                "chosen quotient representative is outside the alias bank",
            )
            dc_deleted_vectors[residue] = list(base)
        dc_deleted_folded = folded_vectors(
            labels, dc_deleted_vectors, modulus
        )
        require(
            all(dc_deleted_folded[residue] == base for residue in range(modulus)),
            "rational DC-deleted witness has incorrect folded residue data",
        )
        for frequency in range(1, modulus):
            coefficient = cyclic_character_sum(modulus, frequency)
            require(
                coefficient == 0,
                "DC-deleted rational partial-bank witness failed",
            )
        require(base != zero_vector(len(base)), "rational hidden Z_0 vanished")

        # For an arbitrary omitted frequency nu_0, take quotient residue data
        # V_a=e_q(-nu_0*a)v.  Its twist transform is supported only at nu_0.
        # This is an exact cyclotomic-field witness, checked without numerical
        # roots of unity.
        for omitted in range(modulus):
            for frequency in range(modulus):
                transform_coefficient = cyclic_character_sum(
                    modulus, frequency - omitted
                )
                require(
                    transform_coefficient
                    == (modulus if frequency == omitted else 0),
                    "arbitrary missing-frequency witness failed",
                )
            arbitrary_missing_cases += 1

        if radius in (1, 3, 7, 15, 24):
            rational_cases.append(
                {
                    "L": radius,
                    "q": modulus,
                    "full_bank_size": modulus,
                    "untwisted_only_hidden_norm_squared": frac_text(
                        norm_squared(base)
                    ),
                    "all_nonzero_frequencies_hidden_norm_squared": frac_text(
                        norm_squared(base)
                    ),
                    "arbitrary_omitted_frequency_witness_field": (
                        "exact cyclotomic scalar extension"
                    ),
                }
            )

    return {
        "checks": CHECKS - start,
        "radii_checked": 24,
        "arbitrary_missing_frequency_cases": arbitrary_missing_cases,
        "representative_counterexamples": rational_cases,
        "conclusion": (
            "all q=L+1 twists recover Z_0 exactly; any omitted twist admits "
            "an exact cyclotomic null witness with nonzero Z_0"
        ),
    }


def divisibility_matrix(window_bound: int, max_modulus: int) -> List[List[int]]:
    labels = list(range(-window_bound, window_bound + 1))
    return [
        [int(label % modulus == 0) for modulus in range(1, max_modulus + 1)]
        for label in labels
    ]


def verify_divisibility_indicator_no_go() -> Dict[str, object]:
    """Verify that moduli at most D<=B cannot synthesize delta at F=0."""

    start = CHECKS
    no_go_cases = 0
    threshold_cases: List[Dict[str, object]] = []
    for window_bound in range(1, 19):
        determinants = list(range(-window_bound, window_bound + 1))
        target = [int(value == 0) for value in determinants]
        for max_modulus in range(1, window_bound + 1):
            matrix = divisibility_matrix(window_bound, max_modulus)
            augmented = [
                matrix[row] + [target[row]]
                for row in range(len(determinants))
            ]
            matrix_rank = rational_rank(matrix)
            augmented_rank = rational_rank(augmented)
            require(
                matrix_rank == max_modulus,
                "window-internal divisibility columns lost rank",
            )
            require(
                augmented_rank == matrix_rank + 1,
                "window-internal indicators unexpectedly synthesize delta_0",
            )

            # The positive rows k=1,...,D form a unit lower-triangular
            # divisibility matrix.  They force every coefficient to zero.
            triangular = [
                [
                    int(row % modulus == 0)
                    for modulus in range(1, max_modulus + 1)
                ]
                for row in range(1, max_modulus + 1)
            ]
            for row in range(max_modulus):
                for column in range(max_modulus):
                    if column > row:
                        require(
                            triangular[row][column] == 0,
                            "divisibility matrix is not lower triangular",
                        )
                require(
                    triangular[row][row] == 1,
                    "divisibility matrix diagonal is not one",
                )
            no_go_cases += 1

        successful_modulus = window_bound + 1
        successful_column = [
            int(value % successful_modulus == 0) for value in determinants
        ]
        require(
            successful_column == target,
            "first modulus above the window failed to isolate zero",
        )

        # Full rigidity check: every modulus above B gives the same delta_0
        # column, while the B internal columns together with delta_0 are
        # independent.  Hence an exact representation has zero aggregate
        # coefficient at each internal modulus and total external weight one.
        extended_matrix = divisibility_matrix(
            window_bound, window_bound + 4
        )
        for column in range(window_bound, window_bound + 4):
            require(
                [row[column] for row in extended_matrix] == target,
                "a superwindow divisibility column is not delta_0",
            )
        internal_plus_target = [
            row[:window_bound] + [target[index]]
            for index, row in enumerate(extended_matrix)
        ]
        require(
            rational_rank(internal_plus_target) == window_bound + 1,
            "divisibility rigidity basis lost rank",
        )
        if window_bound in (1, 2, 4, 8, 12, 18):
            threshold_cases.append(
                {
                    "B": window_bound,
                    "largest_no_go_modulus": window_bound,
                    "first_single_indicator_success": successful_modulus,
                }
            )

    return {
        "checks": CHECKS - start,
        "window_bounds_B_checked": 18,
        "no_go_rank_cases": no_go_cases,
        "threshold_cases": threshold_cases,
        "scope": (
            "exact finite-span no-go for the bank "
            "{1_{m divides F}: 1<=m<=D} on |F|<=B when D<=B; "
            "superwindow columns all equal delta_0 and supply the only "
            "additional direction"
        ),
    }


def product_character_sum(
    modulus: int, exponent_coefficients: Sequence[int]
) -> int:
    """Sum one root monomial over a complete frequency tuple exactly."""

    total = 1
    for coefficient in exponent_coefficients:
        total *= cyclic_character_sum(modulus, coefficient)
    return total


def exact_finite_grid_sample_mean_variance(
    modulus: int,
    labels: Sequence[int],
    vectors: Dict[int, List[Fraction]],
    sample_count: int,
) -> Fraction:
    """Enumerate the complete product-space second moment by characters."""

    nonzero_labels = [label for label in labels if label != 0]
    sample_space_size = modulus ** sample_count
    denominator = sample_space_size * sample_count * sample_count
    numerator = Fraction(0)
    for left_sample in range(sample_count):
        for right_sample in range(sample_count):
            for left_label in nonzero_labels:
                for right_label in nonzero_labels:
                    coefficients = [0 for _ in range(sample_count)]
                    coefficients[left_sample] += left_label
                    coefficients[right_sample] -= right_label
                    root_sum = product_character_sum(modulus, coefficients)
                    numerator += (
                        root_sum
                        * inner_product(
                            vectors[left_label], vectors[right_label]
                        )
                    )
    return numerator * Fraction(1, denominator)


def product_circle_character_moment(
    exponent_coefficients: Sequence[int],
) -> int:
    """Integrate a character monomial over a product of Haar circles."""

    return int(all(coefficient == 0 for coefficient in exponent_coefficients))


def exact_circle_sample_mean_variance(
    labels: Sequence[int],
    vectors: Dict[int, List[Fraction]],
    sample_count: int,
) -> Fraction:
    """Enumerate every second-moment monomial for continuous Haar phases."""

    nonzero_labels = [label for label in labels if label != 0]
    numerator = Fraction(0)
    for left_sample in range(sample_count):
        for right_sample in range(sample_count):
            for left_label in nonzero_labels:
                for right_label in nonzero_labels:
                    coefficients = [0 for _ in range(sample_count)]
                    coefficients[left_sample] += left_label
                    coefficients[right_sample] -= right_label
                    moment = product_circle_character_moment(coefficients)
                    numerator += (
                        moment
                        * inner_product(
                            vectors[left_label], vectors[right_label]
                        )
                    )
    return numerator * Fraction(1, sample_count * sample_count)


def verify_exact_monte_carlo_variance() -> Dict[str, object]:
    """Certify continuous and finite-grid variances by exact moments."""

    start = CHECKS
    cases: List[Dict[str, object]] = []
    for radius in range(1, 13):
        minimal_modulus = radius + 1
        full_grid_modulus = 2 * radius + 1
        labels = list(range(-radius, radius + 1))
        vectors = deterministic_alias_vectors(labels, 3, 3 * radius + 2)

        for label in labels:
            require(
                product_circle_character_moment([label]) == int(label == 0),
                "continuous random-phase estimator is biased for Z_0",
            )
            require(
                normalized_root_average(full_grid_modulus, label)
                == int(label == 0),
                "full-grid random-phase estimator is biased for Z_0",
            )

        raw_trace_variance = sum(
            (norm_squared(vectors[label]) for label in labels if label != 0),
            Fraction(0),
        )
        continuous_pair_expansion = sum(
            (
                Fraction(int(left == right))
                * inner_product(vectors[left], vectors[right])
                for left in labels
                if left != 0
                for right in labels
                if right != 0
            ),
            Fraction(0),
        )
        require(
            raw_trace_variance == continuous_pair_expansion,
            "continuous single-sample trace variance formula failed",
        )

        folded = folded_vectors(labels, vectors, minimal_modulus)
        minimal_grid_variance = sum(
            (
                norm_squared(folded[residue])
                for residue in range(1, minimal_modulus)
            ),
            Fraction(0),
        )
        minimal_grid_pair_expansion = sum(
            (
                Fraction(
                    normalized_root_average(minimal_modulus, left - right)
                )
                * inner_product(vectors[left], vectors[right])
                for left in labels
                if left != 0
                for right in labels
                if right != 0
            ),
            Fraction(0),
        )
        require(
            minimal_grid_variance == minimal_grid_pair_expansion,
            "minimal-grid single-sample folded variance formula failed",
        )

        for sample_count in range(1, 5):
            continuous_enumerated = exact_circle_sample_mean_variance(
                labels, vectors, sample_count
            )
            full_grid_enumerated = exact_finite_grid_sample_mean_variance(
                full_grid_modulus, labels, vectors, sample_count
            )
            minimal_grid_enumerated = exact_finite_grid_sample_mean_variance(
                minimal_modulus, labels, vectors, sample_count
            )
            require(
                continuous_enumerated
                == raw_trace_variance * Fraction(1, sample_count),
                "continuous Haar product-moment variance failed",
            )
            require(
                full_grid_enumerated
                == raw_trace_variance * Fraction(1, sample_count),
                "collision-free finite-grid variance failed",
            )
            require(
                minimal_grid_enumerated
                == minimal_grid_variance * Fraction(1, sample_count),
                "minimal folded finite-grid variance failed",
            )
            if radius in (2, 5, 12) and sample_count in (1, 2, 4):
                cases.append(
                    {
                        "L": radius,
                        "minimal_q": minimal_modulus,
                        "collision_free_grid_q": full_grid_modulus,
                        "sample_count": sample_count,
                        "continuous_Haar_variance": frac_text(
                            continuous_enumerated
                        ),
                        "collision_free_grid_variance": frac_text(
                            full_grid_enumerated
                        ),
                        "minimal_folded_grid_variance": frac_text(
                            minimal_grid_enumerated
                        ),
                        "single_sample_raw_trace": frac_text(
                            raw_trace_variance
                        ),
                        "single_sample_minimal_folded_energy": frac_text(
                            minimal_grid_variance
                        ),
                    }
                )

    return {
        "checks": CHECKS - start,
        "radii_checked": 12,
        "sample_counts_checked_per_radius": [1, 2, 3, 4],
        "method": (
            "complete second-moment monomial enumeration using exact Haar "
            "character integrals and exact finite cyclic character sums"
        ),
        "continuous_Haar_formula": "raw_nonzero_trace/m",
        "collision_free_grid_formula": "raw_nonzero_trace/m",
        "minimal_q_grid_formula": "folded_nonzero_energy/m",
        "uses_random_draws": False,
        "uses_floating_point": False,
        "representative_cases": cases,
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
    random_imports: List[str] = []
    imports: List[str] = []
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
    source_hashes = {
        "experiments/tpc39_certificate.py": sha256_bytes(script_path.read_bytes())
    }
    report: Dict[str, object] = {
        "schema": "tpc39-additive-quotient-certificate-v1",
        "status": "pass",
        "arithmetic": (
            "exact integers and rational Hilbert vectors; roots of unity "
            "evaluated only by exact cyclic orthogonality"
        ),
        "source_constraints": verify_source_constraints(script_path),
        "source_sha256": source_hashes,
        "minimal_identity_projector": verify_minimal_identity_projector(),
        "folded_parseval_and_collision_gram_spectrum": (
            verify_collision_gram_spectrum_and_parseval()
        ),
        "zero_recovery_and_partial_bank_counterexamples": (
            verify_zero_recovery_and_partial_bank_counterexamples()
        ),
        "divisibility_indicator_no_go": verify_divisibility_indicator_no_go(),
        "exact_monte_carlo_variance": verify_exact_monte_carlo_variance(),
        "claims": {
            "finite_alias_quotient_projector_checks": True,
            "minimal_q_for_zero_only_is_L_plus_1": True,
            "minimal_q_for_all_columns_is_2L_plus_1": True,
            "finite_folded_residue_parseval_checks": True,
            "finite_normalized_collision_gram_checks": True,
            "finite_collision_spectrum_eigenvector_checks": True,
            "finite_collision_trace_and_rank_checks": True,
            "finite_exact_zero_recovery_checks": True,
            "finite_partial_bank_counterexamples": True,
            "finite_divisibility_indicator_no_go_checks": True,
            "finite_divisibility_indicator_rigidity_checks": True,
            "exact_continuous_Haar_variance_moment_enumeration": True,
            "finite_collision_free_grid_variance_enumeration": True,
            "finite_minimal_grid_folded_variance_enumeration": True,
            "uses_floating_point": False,
            "uses_random_inputs": False,
            "proves_twist_stable_mobius_estimate": False,
            "proves_mobius_autocorrelation": False,
            "proves_affine_chowla": False,
            "proves_uniform_alias_column_bound": False,
            "proves_physical_equality_output_bound": False,
            "breaks_sieve_parity": False,
            "proves_hardy_littlewood_prime_pairs": False,
            "proves_twin_primes": False,
        },
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
    summary = {
        "certificate": str(output_path),
        "checks": report["check_total"],
        "digest": report["certificate_digest"],
        "json_sha256": sha256_bytes(encoded),
        "source_sha256": report["source_sha256"][
            "experiments/tpc39_certificate.py"
        ],
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
