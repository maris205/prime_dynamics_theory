#!/usr/bin/env python3
"""Deterministic exact-arithmetic certificate for TPC-38.

The program uses only the Python standard library and only exact integer and
``Fraction`` arithmetic.  It contains no random input, floating-point literal,
or ``assert`` statement.  Every failed identity raises ``CertificateError``
through an explicit check, so running with ``python -O`` changes nothing.

The finite checks certify the algebraic models archived with TPC-38.  They do
not certify any asymptotic Mobius estimate, moving-shift diagonal estimate,
joint-alias Gram bound, parity-breaking statement, or twin-prime theorem.
"""

from __future__ import annotations

import ast
import hashlib
import json
from fractions import Fraction
from itertools import product as cartesian_product
from math import gcd
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


def frac_text(value: Fraction | int) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return sha256_bytes(encoded)


def int_product(values: Iterable[int]) -> int:
    answer = 1
    for value in values:
        answer *= value
    return answer


def fraction_product(values: Iterable[Fraction | int]) -> Fraction:
    answer = Fraction(1)
    for value in values:
        answer *= Fraction(value)
    return answer


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
    raise CertificateError(f"no primitive root modulo {prime}")


def discrete_log_table(prime: int) -> Tuple[int, List[int]]:
    generator = primitive_root(prime)
    order = prime - 1
    table = [-1] * prime
    value = 1
    for exponent in range(order):
        require(table[value] == -1, f"primitive-root orbit repeats modulo {prime}")
        table[value] = exponent
        value = value * generator % prime
    require(value == 1, f"primitive-root orbit does not close modulo {prime}")
    require(
        all(table[value] >= 0 for value in range(1, prime)),
        f"incomplete discrete-log table modulo {prime}",
    )
    return generator, table


def cyclic_character_sum(order: int, exponent: int) -> int:
    """Return sum_{k mod order} zeta^(k*exponent) exactly."""

    return order if exponent % order == 0 else 0


def local_character_projectors(
    prime: int, target: int, shift: int, logs: Sequence[int]
) -> Tuple[Fraction, Fraction]:
    """Return all-character and nonprincipal local projectors."""

    order = prime - 1
    target_mod = target % prime
    translated = (target + shift) % prime
    require(target_mod != 0, "character projector target is not a unit")
    if translated == 0:
        return Fraction(0), Fraction(0)
    exponent = logs[translated] - logs[target_mod]
    all_numerator = cyclic_character_sum(order, exponent)
    principal_numerator = 1
    return (
        Fraction(all_numerator, order),
        Fraction(all_numerator - principal_numerator, order),
    )


def local_face(prime: int, target: int, shift: int) -> Tuple[Fraction, Fraction]:
    p_value = Fraction(1, prime - 1)
    delta = Fraction(int(shift % prime == 0))
    unit_mask = Fraction(int((target + shift) % prime != 0))
    principal = p_value * unit_mask
    centered = delta - principal
    return principal, centered


def coordinate_faces(
    primes: Sequence[int], target: int, shift: int
) -> Tuple[List[Fraction], Fraction, Fraction]:
    local = [local_face(prime, target, shift) for prime in primes]
    faces: List[Fraction] = []
    for mask in range(1 << len(primes)):
        faces.append(
            fraction_product(
                local[index][1] if mask & (1 << index) else local[index][0]
                for index in range(len(primes))
            )
        )
    full = faces[-1]
    proper = sum(faces[:-1], Fraction(0))
    return faces, proper, full


def full_face_value(primes: Sequence[int], target: int, shift: int) -> Fraction:
    return fraction_product(
        local_face(prime, target, shift)[1] for prime in primes
    )


def unit_residues(modulus: int) -> List[int]:
    return [value for value in range(modulus) if gcd(value, modulus) == 1]


def density_a(primes: Sequence[int]) -> Fraction:
    return fraction_product(
        Fraction(prime - 2, prime - 1) for prime in primes
    )


def verify_faces_and_fixed_target_norms(
    primes: Tuple[int, int, int]
) -> Dict[str, object]:
    start = CHECKS
    modulus = int_product(primes)
    phi = int_product(prime - 1 for prime in primes)
    units = unit_residues(modulus)
    require(len(units) == phi, "Euler-product unit count failed")
    logs = {prime: discrete_log_table(prime)[1] for prime in primes}
    a_value = density_a(primes)
    require(a_value * phi == int_product(prime - 2 for prime in primes),
            "full character-family size failed")

    fixed_norms: List[Tuple[Fraction, Fraction]] = []
    offjoint_count = 0
    for target in units:
        full_norm = Fraction(0)
        proper_norm = Fraction(0)
        for shift in range(modulus):
            faces, proper, full = coordinate_faces(primes, target, shift)
            delta = Fraction(int(shift == 0))
            require(sum(faces, Fraction(0)) == delta,
                    "coordinate-face recombination failed")
            require(full + proper == delta, "full/proper recombination failed")

            spectral_all = Fraction(1)
            spectral_full = Fraction(1)
            for prime in primes:
                local_all, local_nonprincipal = local_character_projectors(
                    prime, target, shift, logs[prime]
                )
                principal, centered = local_face(prime, target, shift)
                require(local_all - local_nonprincipal == principal,
                        "principal character face failed")
                require(local_nonprincipal == centered,
                        "nonprincipal character face failed")
                spectral_all *= local_all
                spectral_full *= local_nonprincipal
            require(spectral_all == delta, "all-character CRT projector failed")
            require(spectral_full == full, "full-character CRT projector failed")
            require(spectral_all - spectral_full == proper,
                    "proper-character CRT projector failed")

            if shift == 0:
                require(full == a_value, "full face at the joint residue failed")
                require(proper == 1 - a_value,
                        "proper face at the joint residue failed")
            else:
                require(proper == -full, "offjoint proper/full cancellation failed")
                offjoint_count += 1
            full_norm += full * full
            proper_norm += proper * proper
        require(full_norm == a_value, "fixed-target full squared norm failed")
        require(proper_norm == 1 - a_value,
                "fixed-target proper squared norm failed")
        fixed_norms.append((full_norm, proper_norm))

    witness_target = units[0]
    witness_full = Fraction(0)
    witness_proper = Fraction(0)
    witness_l_one = Fraction(0)
    witness_support = 0
    for shift in range(1, modulus):
        _, proper, full = coordinate_faces(primes, witness_target, shift)
        if full == 0:
            continue
        phase = Fraction(1 if full > 0 else -1)
        witness_full += full * phase
        witness_proper += proper * phase
        witness_l_one += abs(full)
        witness_support += 1
    require(witness_support > 0, "offjoint witness has empty support")
    require(witness_full == witness_l_one,
            "offjoint full witness did not align")
    require(witness_proper == -witness_l_one,
            "offjoint proper witness did not anti-align")
    require(witness_full + witness_proper == 0,
            "offjoint recombined witness did not vanish")

    return {
        "checks": CHECKS - start,
        "primes": list(primes),
        "modulus": modulus,
        "phi": phi,
        "A": frac_text(a_value),
        "full_family_size": int(a_value * phi),
        "proper_family_size": int((1 - a_value) * phi),
        "targets_checked": len(units),
        "target_shift_pairs_checked": len(units) * modulus,
        "offjoint_cancellation_checks": offjoint_count,
        "fixed_target_full_norm_squared": frac_text(fixed_norms[0][0]),
        "fixed_target_proper_norm_squared": frac_text(fixed_norms[0][1]),
        "aligned_offjoint_witness": {
            "target": witness_target,
            "support": witness_support,
            "separate_output_norm": frac_text(witness_l_one),
            "recombined_output_norm": "0",
        },
    }


def matvec(matrix: Sequence[Sequence[Fraction]], vector: Sequence[Fraction]) -> List[Fraction]:
    return [
        sum((entry * vector[column] for column, entry in enumerate(row)), Fraction(0))
        for row in matrix
    ]


def local_target_row(prime: int, target: int) -> List[Fraction]:
    return [local_face(prime, target, shift)[1] for shift in range(prime)]


def local_principal_eigenvalue(prime: int) -> Fraction:
    return Fraction(prime * (prime - 2) * (prime - 2), (prime - 1) * (prime - 1))


def local_nonprincipal_eigenvalue(prime: int) -> Fraction:
    return Fraction(1, (prime - 1) * (prime - 1))


def verify_local_target_grams() -> Dict[str, object]:
    start = CHECKS
    cases: List[Dict[str, object]] = []
    for prime in (3, 5, 7, 11, 13):
        units = list(range(1, prime))
        p_value = Fraction(1, prime - 1)
        rows = [local_target_row(prime, target) for target in units]
        gram: List[List[Fraction]] = []
        for left_index, left in enumerate(units):
            row: List[Fraction] = []
            for right_index, right in enumerate(units):
                value = sum(
                    (rows[left_index][shift] * rows[right_index][shift]
                     for shift in range(prime)),
                    Fraction(0),
                )
                expected = 1 - p_value if left == right else 1 - p_value - p_value * p_value
                require(value == expected, "local target Gram entry failed")
                row.append(value)
            gram.append(row)

        principal = [Fraction(1) for _ in units]
        lambda_principal = local_principal_eigenvalue(prime)
        lambda_nonprincipal = local_nonprincipal_eigenvalue(prime)
        require(
            matvec(gram, principal) == [lambda_principal for _ in units],
            "local principal target eigenvalue failed",
        )
        for index in range(len(units) - 1):
            contrast = [Fraction(0) for _ in units]
            contrast[index] = 1
            contrast[-1] = -1
            require(
                matvec(gram, contrast)
                == [lambda_nonprincipal * value for value in contrast],
                "local nonprincipal target eigenvalue failed",
            )
        trace_from_rows = sum((gram[index][index] for index in range(len(units))), Fraction(0))
        trace_from_spectrum = lambda_principal + (prime - 2) * lambda_nonprincipal
        require(trace_from_rows == trace_from_spectrum,
                "local target-spectrum trace failed")
        cases.append(
            {
                "q": prime,
                "target_dimension": prime - 1,
                "row_norm_squared": frac_text(1 - p_value),
                "principal_squared_singular_value": frac_text(lambda_principal),
                "nonprincipal_squared_singular_value": frac_text(lambda_nonprincipal),
                "nonprincipal_multiplicity": prime - 2,
            }
        )
    return {"checks": CHECKS - start, "cases": cases}


def tensor_vector(
    target_tuples: Sequence[Tuple[int, ...]],
    units_by_prime: Sequence[Sequence[int]],
    nonprincipal_mask: int,
) -> List[Fraction]:
    local_vectors: List[Dict[int, Fraction]] = []
    for index, units in enumerate(units_by_prime):
        if nonprincipal_mask & (1 << index):
            local = {unit: Fraction(0) for unit in units}
            local[units[0]] = 1
            local[units[-1]] = -1
        else:
            local = {unit: Fraction(1) for unit in units}
        local_vectors.append(local)
    return [
        fraction_product(local_vectors[index][target[index]] for index in range(len(target)))
        for target in target_tuples
    ]


def verify_global_target_gram_and_spectrum(
    primes: Tuple[int, int, int]
) -> Dict[str, object]:
    start = CHECKS
    modulus = int_product(primes)
    phi = int_product(prime - 1 for prime in primes)
    a_value = density_a(primes)
    units_by_prime = [list(range(1, prime)) for prime in primes]
    target_tuples = list(cartesian_product(*units_by_prime))
    require(len(target_tuples) == phi, "global target tuple count failed")

    rows: List[List[Fraction]] = []
    for target in target_tuples:
        row = [
            fraction_product(
                local_face(prime, target[index], shift)[1]
                for index, prime in enumerate(primes)
            )
            for shift in range(modulus)
        ]
        rows.append(row)

    gram: List[List[Fraction]] = []
    proper_gram: List[List[Fraction]] = []
    cross_gram: List[List[Fraction]] = []
    for left_index, left_target in enumerate(target_tuples):
        gram_row: List[Fraction] = []
        proper_row: List[Fraction] = []
        cross_row: List[Fraction] = []
        for right_index, right_target in enumerate(target_tuples):
            direct = sum(
                (rows[left_index][shift] * rows[right_index][shift]
                 for shift in range(modulus)),
                Fraction(0),
            )
            expected = fraction_product(
                (Fraction(1) - Fraction(1, prime - 1))
                if left_target[index] == right_target[index]
                else (
                    Fraction(1)
                    - Fraction(1, prime - 1)
                    - Fraction(1, (prime - 1) * (prime - 1))
                )
                for index, prime in enumerate(primes)
            )
            require(direct == expected, "global target Gram tensor formula failed")
            proper_direct = sum(
                ((Fraction(int(shift == 0)) - rows[left_index][shift])
                 * (Fraction(int(shift == 0)) - rows[right_index][shift])
                 for shift in range(modulus)),
                Fraction(0),
            )
            cross_direct = sum(
                (rows[left_index][shift]
                 * (Fraction(int(shift == 0)) - rows[right_index][shift])
                 for shift in range(modulus)),
                Fraction(0),
            )
            require(proper_direct == 1 - 2 * a_value + direct,
                    "proper target Gram rank-one formula failed")
            require(cross_direct == a_value - direct,
                    "full/proper cross Gram formula failed")
            gram_row.append(direct)
            proper_row.append(proper_direct)
            cross_row.append(cross_direct)
        gram.append(gram_row)
        proper_gram.append(proper_row)
        cross_gram.append(cross_row)

    ledger: List[Dict[str, object]] = []
    full_trace = Fraction(0)
    proper_trace = Fraction(0)
    lambda_full_principal = fraction_product(
        local_principal_eigenvalue(prime) for prime in primes
    )
    lambda_proper_principal = lambda_full_principal + phi * (1 - 2 * a_value)
    for mask in range(1 << len(primes)):
        eigenvalue = fraction_product(
            local_nonprincipal_eigenvalue(prime)
            if mask & (1 << index)
            else local_principal_eigenvalue(prime)
            for index, prime in enumerate(primes)
        )
        multiplicity = int_product(
            prime - 2 if mask & (1 << index) else 1
            for index, prime in enumerate(primes)
        )
        vector = tensor_vector(target_tuples, units_by_prime, mask)
        require(
            matvec(gram, vector) == [eigenvalue * value for value in vector],
            "global full target-spectrum action failed",
        )
        proper_eigenvalue = lambda_proper_principal if mask == 0 else eigenvalue
        require(
            matvec(proper_gram, vector)
            == [proper_eigenvalue * value for value in vector],
            "global proper target-spectrum action failed",
        )
        full_trace += multiplicity * eigenvalue
        proper_trace += multiplicity * proper_eigenvalue
        ledger.append(
            {
                "nonprincipal_coordinate_mask": format(mask, "03b"),
                "multiplicity": multiplicity,
                "full_squared_singular_value": frac_text(eigenvalue),
                "proper_squared_singular_value": frac_text(proper_eigenvalue),
            }
        )
    require(full_trace == phi * a_value, "global full spectral trace failed")
    require(proper_trace == phi * (1 - a_value),
            "global proper spectral trace failed")
    require(lambda_full_principal == max(
        Fraction(item["full_squared_singular_value"])
        for item in ledger
    ), "full synthesis norm ledger failed")
    require(lambda_proper_principal == max(
        Fraction(item["proper_squared_singular_value"])
        for item in ledger
    ), "proper synthesis norm ledger failed")

    return {
        "checks": CHECKS - start,
        "primes": list(primes),
        "modulus": modulus,
        "target_dimension": phi,
        "A": frac_text(a_value),
        "full_synthesis_norm_squared": frac_text(lambda_full_principal),
        "proper_synthesis_norm_squared": frac_text(lambda_proper_principal),
        "full_trace": frac_text(full_trace),
        "proper_trace": frac_text(proper_trace),
        "mode_ledger": ledger,
    }


def ratio_fiber_summary(
    primes: Tuple[int, int, int], shift: int, units: Sequence[int]
) -> Tuple[int, int, int]:
    modulus = int_product(primes)
    buckets: Dict[int, int] = {}
    domain_size = 0
    for target in units:
        if gcd(target + shift, modulus) != 1:
            continue
        ratio = (target + shift) * pow(target, -1, modulus) % modulus
        buckets[ratio] = buckets.get(ratio, 0) + 1
        domain_size += 1
    require(domain_size > 0, "ratio domain is empty")
    maximum = max(buckets.values())
    require(all(value == maximum for value in buckets.values()),
            "ratio fibers on the image do not have constant size")
    return maximum, len(buckets), domain_size


def divisor_mask(primes: Sequence[int], value: int) -> int:
    mask = 0
    for index, prime in enumerate(primes):
        if value % prime == 0:
            mask |= 1 << index
    return mask


def expected_fixed_shift_mass(primes: Sequence[int], shift: int) -> Fraction:
    return fraction_product(
        Fraction(prime - 1) * Fraction(prime - 2, prime - 1) ** 2
        if shift % prime == 0
        else Fraction(prime - 2, (prime - 1) * (prime - 1))
        for prime in primes
    )


def verify_ratio_fibers_and_shift_masses(
    primes: Tuple[int, int, int]
) -> Dict[str, object]:
    start = CHECKS
    modulus = int_product(primes)
    phi = int_product(prime - 1 for prime in primes)
    units = unit_residues(modulus)
    a_value = density_a(primes)
    strata: Dict[int, Dict[str, object]] = {}
    total_full_mass = Fraction(0)
    total_proper_mass = Fraction(0)

    for shift in range(modulus):
        mask = divisor_mask(primes, shift)
        expected_multiplicity = int_product(
            prime - 1
            for index, prime in enumerate(primes)
            if mask & (1 << index)
        )
        maximum, image_size, domain_size = ratio_fiber_summary(primes, shift, units)
        expected_domain_size = int_product(
            prime - 1 if mask & (1 << index) else prime - 2
            for index, prime in enumerate(primes)
        )
        expected_image_size = int_product(
            1 if mask & (1 << index) else prime - 2
            for index, prime in enumerate(primes)
        )
        require(maximum == expected_multiplicity,
                "exact ratio-fiber multiplicity failed")
        require(domain_size == expected_domain_size,
                "ratio domain cardinality failed")
        require(image_size == expected_image_size,
                "ratio image cardinality failed")
        require(domain_size == maximum * image_size,
                "ratio domain/image/fiber product failed")

        full_mass = sum(
            (full_face_value(primes, target, shift) ** 2 for target in units),
            Fraction(0),
        )
        proper_mass = sum(
            ((Fraction(int(shift == 0)) - full_face_value(primes, target, shift)) ** 2
             for target in units),
            Fraction(0),
        )
        expected_full_mass = expected_fixed_shift_mass(primes, shift)
        require(full_mass == expected_full_mass,
                "fixed-shift full target mass failed")
        if shift == 0:
            require(proper_mass == phi * (1 - a_value) ** 2,
                    "joint proper target mass failed")
        else:
            require(proper_mass == full_mass,
                    "offjoint proper target mass failed")
        total_full_mass += full_mass
        total_proper_mass += proper_mass

        if mask not in strata:
            strata[mask] = {
                "shift_count": 0,
                "fiber_multiplicity": maximum,
                "ratio_image_size": image_size,
                "ratio_domain_size": domain_size,
                "full_target_mass": frac_text(full_mass),
            }
        else:
            require(strata[mask]["fiber_multiplicity"] == maximum,
                    "stratum fiber multiplicity is not constant")
            require(strata[mask]["ratio_image_size"] == image_size,
                    "stratum ratio image size is not constant")
            require(strata[mask]["ratio_domain_size"] == domain_size,
                    "stratum ratio domain size is not constant")
            require(strata[mask]["full_target_mass"] == frac_text(full_mass),
                    "stratum target mass is not constant")
        strata[mask]["shift_count"] = int(strata[mask]["shift_count"]) + 1

    for mask, item in strata.items():
        expected_shift_count = int_product(
            1 if mask & (1 << index) else prime - 1
            for index, prime in enumerate(primes)
        )
        require(item["shift_count"] == expected_shift_count,
                "determinant-stratum CRT count failed")
    require(len(strata) == 1 << len(primes),
            "not every determinant stratum occurred")
    require(total_full_mass == phi * a_value,
            "full fixed-shift masses do not recover the trace")
    require(total_proper_mass == phi * (1 - a_value),
            "proper fixed-shift masses do not recover the trace")

    ordered_strata = []
    for mask in sorted(strata):
        item = dict(strata[mask])
        item["divisible_coordinate_mask"] = format(mask, "03b")
        ordered_strata.append(item)
    return {
        "checks": CHECKS - start,
        "primes": list(primes),
        "modulus": modulus,
        "phi": phi,
        "shifts_checked": modulus,
        "strata": ordered_strata,
        "period_full_mass": frac_text(total_full_mass),
        "period_proper_mass": frac_text(total_proper_mass),
    }


def verify_four_modulus_no_wrap() -> Dict[str, object]:
    start = CHECKS
    cases: List[Dict[str, object]] = []
    for primes in ((3, 5, 7, 11), (5, 7, 11, 13)):
        modulus = int_product(primes)
        bound = modulus - 1
        for shift in range(-bound, bound + 1):
            require((shift % modulus == 0) == (shift == 0),
                    "four-modulus no-wrap identity failed")
        a_four = density_a(primes)
        target = 1
        require(full_face_value(primes, target, 0) == a_four,
                "four-modulus equality-face value failed")
        require(a_four > 0 and a_four < 1,
                "four-modulus equality-face density range failed")
        require((-modulus < -bound) and (bound < modulus),
                "four-modulus first aliases are not outside the interval")
        cases.append(
            {
                "primes": list(primes),
                "modulus": modulus,
                "tested_interval": [-bound, bound],
                "tested_integer_count": 2 * bound + 1,
                "nonzero_alias_count": 0,
                "equality_full_face_value": frac_text(a_four),
                "first_nonzero_aliases": [-modulus, modulus],
            }
        )
    return {"checks": CHECKS - start, "cases": cases}


def vector_norm_squared(vector: Sequence[Fraction | int]) -> Fraction:
    return sum((Fraction(value) * Fraction(value) for value in vector), Fraction(0))


def verify_sharp_rank_one_alias_loss() -> Dict[str, object]:
    start = CHECKS
    modulus = 17
    base_vector = [Fraction(3), Fraction(4)]
    b_zero = vector_norm_squared(base_vector)
    require(b_zero == 25, "rank-one witness base norm failed")
    cases: List[Dict[str, object]] = []
    for alias_radius in (0, 1, 3, 5):
        bound = alias_radius * modulus
        indices = list(range(-alias_radius, alias_radius + 1))
        k_count = 2 * (bound // modulus) + 1
        require(k_count == len(indices), "alias-index count formula failed")
        columns = [list(base_vector) for _ in indices]
        diagonal_trace = sum((vector_norm_squared(column) for column in columns), Fraction(0))
        summed = [
            sum((column[coordinate] for column in columns), Fraction(0))
            for coordinate in range(len(base_vector))
        ]
        summed_norm = vector_norm_squared(summed)
        require(diagonal_trace == b_zero * k_count,
                "rank-one alias diagonal trace failed")
        require(summed_norm == b_zero * k_count * k_count,
                "rank-one coherent alias norm failed")
        require(summed_norm == k_count * diagonal_trace,
                "rank-one witness does not saturate Cauchy")

        gram = [
            [
                sum((columns[left][coordinate] * columns[right][coordinate]
                     for coordinate in range(len(base_vector))), Fraction(0))
                for right in range(k_count)
            ]
            for left in range(k_count)
        ]
        require(all(entry == b_zero for row in gram for entry in row),
                "rank-one alias Gram is not constant")
        ones = [Fraction(1) for _ in range(k_count)]
        require(matvec(gram, ones) == [b_zero * k_count for _ in range(k_count)],
                "rank-one alias Gram principal eigenvalue failed")
        for index in range(k_count - 1):
            contrast = [Fraction(0) for _ in range(k_count)]
            contrast[index] = 1
            contrast[-1] = -1
            require(matvec(gram, contrast) == [Fraction(0) for _ in range(k_count)],
                    "rank-one alias Gram nullspace failed")
        cases.append(
            {
                "alias_radius": alias_radius,
                "B_over_M": alias_radius,
                "K_B": k_count,
                "B_0": frac_text(b_zero),
                "diagonal_trace": frac_text(diagonal_trace),
                "coherent_sum_norm_squared": frac_text(summed_norm),
                "sharp_loss_factor": k_count,
                "gram_nonzero_eigenvalue": frac_text(b_zero * k_count),
            }
        )
    return {"checks": CHECKS - start, "cases": cases}


def verify_equality_nonrecoverability_witness() -> Dict[str, object]:
    """Check that completed face fields do not determine the equality column."""

    start = CHECKS
    primes = (3, 5, 7)
    modulus = int_product(primes)
    a_value = density_a(primes)
    base_vector = [Fraction(3), Fraction(4)]
    base_norm = vector_norm_squared(base_vector)
    require(base_norm > 0, "equality witness base column is zero")

    # The labels are determinant shifts.  Both nonzero columns lie in the
    # identity ratio bucket: F=0 and F=2M.  The listed nonjoint shifts carry
    # zero columns, so adding them cannot reveal the hidden equality column.
    joint_columns = {
        0: list(base_vector),
        2 * modulus: [-value for value in base_vector],
    }
    nonjoint_columns = {
        1: [Fraction(0), Fraction(0)],
        modulus - 1: [Fraction(0), Fraction(0)],
        modulus + 1: [Fraction(0), Fraction(0)],
    }
    require(len(joint_columns) >= 2, "fewer than two joint alias columns")
    require(all(shift % modulus == 0 for shift in joint_columns),
            "a purported joint alias is nonjoint")
    require(all(shift % modulus != 0 for shift in nonjoint_columns),
            "a purported nonjoint column is joint")
    require(all(vector_norm_squared(column) == 0
                for column in nonjoint_columns.values()),
            "a nonjoint witness column is nonzero")

    alias_total = [
        sum((column[coordinate] for column in joint_columns.values()), Fraction(0))
        for coordinate in range(len(base_vector))
    ]
    require(alias_total == [Fraction(0), Fraction(0)],
            "opposite joint aliases do not cancel")
    completed_full = [a_value * value for value in alias_total]
    completed_proper = [(1 - a_value) * value for value in alias_total]
    require(vector_norm_squared(completed_full) == 0,
            "completed full-face output is nonzero")
    require(vector_norm_squared(completed_proper) == 0,
            "completed proper-face output is nonzero")
    equality_norm = vector_norm_squared(joint_columns[0])
    require(equality_norm == base_norm and equality_norm > 0,
            "hidden equality column has zero norm")

    scaling_cases: List[Dict[str, object]] = []
    for scale in (Fraction(-7), Fraction(1), Fraction(5, 3), Fraction(19)):
        scaled_zero = [scale * value for value in joint_columns[0]]
        scaled_alias = [scale * value for value in joint_columns[2 * modulus]]
        scaled_total = [
            scaled_zero[coordinate] + scaled_alias[coordinate]
            for coordinate in range(len(base_vector))
        ]
        scaled_norm = vector_norm_squared(scaled_zero)
        require(scaled_total == [Fraction(0), Fraction(0)],
                "scaled joint aliases do not cancel")
        require(scaled_norm == scale * scale * base_norm,
                "equality-column quadratic scaling law failed")
        require(scaled_norm > 0, "nonzero scale killed the equality column")
        require(vector_norm_squared([a_value * value for value in scaled_total]) == 0,
                "scaled completed full output is nonzero")
        require(vector_norm_squared([(1 - a_value) * value for value in scaled_total]) == 0,
                "scaled completed proper output is nonzero")
        scaling_cases.append(
            {
                "scale": frac_text(scale),
                "equality_column_norm_squared": frac_text(scaled_norm),
                "alias_total_norm_squared": "0",
                "completed_full_norm_squared": "0",
                "completed_proper_norm_squared": "0",
            }
        )

    return {
        "checks": CHECKS - start,
        "primes": list(primes),
        "modulus": modulus,
        "A": frac_text(a_value),
        "joint_shifts": sorted(joint_columns),
        "zero_nonjoint_shifts": sorted(nonjoint_columns),
        "base_equality_column_norm_squared": frac_text(equality_norm),
        "alias_total_norm_squared": "0",
        "completed_full_norm_squared": "0",
        "completed_proper_norm_squared": "0",
        "formal_scaling_law": f"{frac_text(base_norm)}*t^2",
        "nonzero_rational_scaling_cases": scaling_cases,
        "interpretation": (
            "completed full/proper outputs can both vanish while the F=0 "
            "equality column is nonzero and has unbounded quadratic scale"
        ),
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
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            random_imports.extend(
                alias.name for alias in node.names
                if alias.name == "random" or alias.name.startswith("random.")
            )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "random" or module.startswith("random."):
                random_imports.append(module)
    require(not assert_nodes, "certificate source contains assert")
    require(not float_nodes, "certificate source contains a float literal")
    require(not division_nodes, "certificate source contains true division")
    require(not random_imports, "certificate source imports random")
    return {
        "checks": CHECKS - start,
        "stdlib_only": True,
        "assert_statements": len(assert_nodes),
        "float_literals": len(float_nodes),
        "true_division_nodes": len(division_nodes),
        "random_imports": len(random_imports),
        "optimization_safe_explicit_checks": True,
    }


def build_report(script_path: Path) -> Dict[str, object]:
    paper_directory = script_path.parent.parent
    source_relatives = [
        "main.tex",
        "sections/target-character-projectors.tex",
        "sections/ratio-parseval.tex",
        "sections/target-synthesis-spectrum.tex",
        "sections/recombined-alias-gate.tex",
        "experiments/tpc38_certificate.py",
    ]
    source_hashes: Dict[str, str] = {}
    for relative in source_relatives:
        source_path = paper_directory.joinpath(relative)
        require(source_path.is_file(), f"missing certificate source: {relative}")
        source_hashes[relative] = sha256_bytes(source_path.read_bytes())

    report: Dict[str, object] = {
        "schema": "tpc38-exact-certificate-v1",
        "status": "pass",
        "arithmetic": "exact integers and rational numbers only",
        "source_constraints": verify_source_constraints(script_path),
        "source_sha256": source_hashes,
        "face_projectors_recombination_and_fixed_target_norms": [
            verify_faces_and_fixed_target_norms((3, 5, 7)),
            verify_faces_and_fixed_target_norms((5, 7, 11)),
        ],
        "local_target_grams_and_synthesis_eigenvalues": verify_local_target_grams(),
        "global_target_gram_and_tensor_spectrum":
            verify_global_target_gram_and_spectrum((3, 5, 7)),
        "ratio_fibers_and_fixed_shift_target_masses": [
            verify_ratio_fibers_and_shift_masses((3, 5, 7)),
            verify_ratio_fibers_and_shift_masses((5, 7, 11)),
        ],
        "four_modulus_no_wrap": verify_four_modulus_no_wrap(),
        "sharp_rank_one_alias_loss": verify_sharp_rank_one_alias_loss(),
        "equality_nonrecoverability_witness":
            verify_equality_nonrecoverability_witness(),
        "claims": {
            "finite_character_projector_checks": True,
            "finite_full_proper_recombination_checks": True,
            "finite_fixed_target_norm_checks": True,
            "finite_local_and_global_target_gram_checks": True,
            "finite_target_synthesis_spectrum_checks": True,
            "finite_exact_ratio_fiber_checks": True,
            "finite_fixed_shift_target_mass_checks": True,
            "finite_four_modulus_no_wrap_checks": True,
            "finite_offjoint_cancellation_checks": True,
            "finite_sharp_rank_one_alias_loss_checks": True,
            "finite_equality_nonrecoverability_witness": True,
            "uses_floating_point": False,
            "uses_random_inputs": False,
            "proves_uniform_moving_shift_diagonal": False,
            "proves_joint_alias_gram_gate": False,
            "proves_physical_orbit_gate": False,
            "proves_mobius_autocorrelation": False,
            "proves_affine_chowla": False,
            "proves_equality_recovery": False,
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
    encoded = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    output_path.write_text(encoded, encoding="utf-8", newline="\n")
    output_bytes = output_path.read_bytes()
    print(
        json.dumps(
            {
                "certificate": str(output_path),
                "checks": report["check_total"],
                "digest": report["certificate_digest"],
                "json_sha256": sha256_bytes(output_bytes),
                "source_sha256": report["source_sha256"]["experiments/tpc38_certificate.py"],
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
