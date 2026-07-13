"""Exact finite diagnostics for the power-short rough-box paper.

The calculations use only Python integers and ``fractions.Fraction``.  They
are certificates for finite identities and inequalities, not numerical
evidence for a prime-pair statement.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


PRIMES: Tuple[int, ...] = (5, 7, 11)
Q = math.prod(PRIMES)


def frac_record(value: Fraction) -> Dict[str, int]:
    """Return a stable JSON representation of an exact rational number."""

    return {"numerator": value.numerator, "denominator": value.denominator}


def units(modulus: int) -> List[int]:
    return [a for a in range(modulus) if math.gcd(a, modulus) == 1]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def validate_primes(primes: Sequence[int], minimum: int = 3) -> None:
    if not primes or len(set(primes)) != len(primes):
        raise ValueError("primes must be a nonempty sequence of distinct primes")
    if any(p < minimum or not is_prime(p) for p in primes):
        raise ValueError(f"every prime must be at least {minimum}")


def nonempty_supports(primes: Sequence[int]) -> List[Tuple[int, ...]]:
    return [
        support
        for size in range(1, len(primes) + 1)
        for support in combinations(primes, size)
    ]


def phi_squarefree(primes: Iterable[int]) -> int:
    return math.prod(p - 1 for p in primes)


def unit_density(primes: Iterable[int]) -> Fraction:
    value = Fraction(1)
    for p in primes:
        value *= Fraction(p - 1, p)
    return value


def kappa(primes: Iterable[int]) -> Fraction:
    value = Fraction(1)
    for p in primes:
        value *= Fraction(p - 2, p - 1)
    return value


def xi(primes: Iterable[int]) -> Fraction:
    value = Fraction(1)
    for p in primes:
        value *= Fraction(p, p - 2)
    return value


def legendre_symbol(a: int, p: int) -> int:
    """Quadratic character modulo an odd prime, extended by zero."""

    residue = a % p
    if residue == 0:
        return 0
    value = pow(residue, (p - 1) // 2, p)
    return -1 if value == p - 1 else value


def rough_character_sum(
    start: int, length: int, all_primes: Sequence[int], support: Sequence[int]
) -> int:
    """Sum the product quadratic character on Q-rough integers in an interval."""

    if length < 0:
        raise ValueError("length must be nonnegative")
    modulus = math.prod(all_primes)
    total = 0
    for m in range(start, start + length):
        if math.gcd(m, modulus) != 1:
            continue
        value = 1
        for p in support:
            value *= legendre_symbol(m, p)
        total += value
    return total


def rough_fiber_certificate(
    start: int, length: int, all_primes: Sequence[int], support: Sequence[int]
) -> Dict[str, object]:
    """Verify the exact inclusion--exclusion fiber discrepancy bound."""

    validate_primes(all_primes)
    if length < 0:
        raise ValueError("length must be nonnegative")
    if (
        not support
        or len(set(support)) != len(support)
        or not set(support).issubset(all_primes)
    ):
        raise ValueError("support must be a nonempty distinct subset of all_primes")
    q = math.prod(support)
    complement = tuple(p for p in all_primes if p not in support)
    counts = {a: 0 for a in units(q)}
    modulus = math.prod(all_primes)
    for m in range(start, start + length):
        if math.gcd(m, modulus) == 1:
            counts[m % q] += 1

    main_term = Fraction(length, q) * unit_density(complement)
    errors = {a: Fraction(count) - main_term for a, count in counts.items()}
    max_error = max(abs(error) for error in errors.values())
    fiber_bound = Fraction(2 ** len(complement))

    char_sum = rough_character_sum(start, length, all_primes, support)
    char_bound = phi_squarefree(support) * 2 ** len(complement)

    return {
        "support_modulus": q,
        "support_primes": list(support),
        "interval": {"start": start, "length": length},
        "main_fiber_term": frac_record(main_term),
        "maximum_fiber_error": frac_record(max_error),
        "fiber_error_bound": frac_record(fiber_bound),
        "fiber_bound_verified": max_error <= fiber_bound,
        "quadratic_character_sum": char_sum,
        "character_bound": char_bound,
        "character_bound_verified": abs(char_sum) <= char_bound,
    }


def designed_square_certificate(
    primes: Sequence[int] = PRIMES, forbidden_residue: int = 1
) -> Dict[str, object]:
    """Construct the shifted-divisor Selberg-form square killing singleton modes."""

    validate_primes(primes, minimum=5)
    modulus = math.prod(primes)
    if math.gcd(forbidden_residue, modulus) != 1:
        raise ValueError("the forbidden residue must be a unit modulo every prime")
    a_parameter = sum((Fraction(1, p - 3) for p in primes), Fraction(0))
    c_parameter = Fraction(2, 1) / (1 + 2 * a_parameter)
    t = {p: c_parameter * Fraction(p - 1, p - 3) for p in primes}

    weights: Dict[int, Fraction] = {}
    upper_bound_verified = True
    for a in units(modulus):
        f_value = Fraction(1) - sum(
            (t[p] for p in primes if a % p == forbidden_residue % p),
            Fraction(0),
        )
        weight = f_value * f_value
        weights[a] = weight
        admissible = all(a % p != forbidden_residue % p for p in primes)
        upper_bound_verified &= weight >= int(admissible)

    mu = sum(weights.values(), Fraction(0)) / phi_squarefree(primes)
    centered = {a: weights[a] / mu - 1 for a in weights}

    # A function on a product group has no Fourier mode supported at one prime
    # iff every one-coordinate conditional sum of its centered part is zero.
    fiber_sums: Dict[str, Dict[str, Dict[str, int]]] = {}
    for p in primes:
        local: Dict[str, Dict[str, int]] = {}
        for residue in range(1, p):
            value = sum(
                (u for a, u in centered.items() if a % p == residue), Fraction(0)
            )
            local[str(residue)] = frac_record(value)
        fiber_sums[str(p)] = local

    all_one_prime_modes_zero = all(
        value["numerator"] == 0
        for local in fiber_sums.values()
        for value in local.values()
    )

    pair_coefficients: Dict[str, Dict[str, int]] = {}
    pair_identity_verified = True
    for index, p in enumerate(primes):
        for q in primes[index + 1 :]:
            magnitude = (
                2
                * t[p]
                * t[q]
                / (mu * (p - 1) * (q - 1))
            )
            pair_coefficients[str(p * q)] = frac_record(magnitude)

    theta = {p: Fraction(1, p - 1) for p in primes}
    for a in units(modulus):
        pair_part = sum(
            (
                2
                * t[p]
                * t[q]
                * (int(a % p == forbidden_residue % p) - theta[p])
                * (int(a % q == forbidden_residue % q) - theta[q])
                for p, q in combinations(primes, 2)
            ),
            Fraction(0),
        )
        pair_identity_verified &= weights[a] - mu == pair_part

    centered_second_moment = (
        sum((value * value for value in centered.values()), Fraction(0))
        / phi_squarefree(primes)
    )
    pair_parseval_mass = sum(
        (
            (p - 2)
            * (q - 2)
            * Fraction(
                pair_coefficients[str(p * q)]["numerator"],
                pair_coefficients[str(p * q)]["denominator"],
            )
            ** 2
            for p, q in combinations(primes, 2)
        ),
        Fraction(0),
    )

    pattern_multiplicities: Counter[Tuple[int, ...]] = Counter()
    pattern_weight_sums: Dict[Tuple[int, ...], Fraction] = {}
    for a, weight in weights.items():
        pattern = tuple(
            p for p in primes if a % p == forbidden_residue % p
        )
        pattern_multiplicities[pattern] += 1
        pattern_weight_sums[pattern] = pattern_weight_sums.get(pattern, Fraction(0)) + weight

    pattern_records: Dict[str, Dict[str, object]] = {}
    for pattern, multiplicity in sorted(
        pattern_multiplicities.items(), key=lambda item: (len(item[0]), item[0])
    ):
        key = "empty" if not pattern else "*".join(str(p) for p in pattern)
        pattern_records[key] = {
            "multiplicity": multiplicity,
            "weight": frac_record(pattern_weight_sums[pattern] / multiplicity),
        }

    return {
        "modulus": modulus,
        "primes": list(primes),
        "forbidden_residue": forbidden_residue,
        "A": frac_record(a_parameter),
        "C": frac_record(c_parameter),
        "t": {str(p): frac_record(t[p]) for p in primes},
        "mean_weight": frac_record(mu),
        "upper_bound_verified": upper_bound_verified,
        "one_prime_conditional_sums": fiber_sums,
        "all_one_prime_modes_zero": all_one_prime_modes_zero,
        "pointwise_pair_hoeffding_identity_verified": pair_identity_verified,
        "centered_second_moment": frac_record(centered_second_moment),
        "pair_parseval_mass": frac_record(pair_parseval_mass),
        "pair_parseval_verified": centered_second_moment == pair_parseval_mass,
        "transform_convention": "|G|^-1 sum of U(a) conjugate(chi(a)), U=W/mu-1",
        "nonzero_support_moduli": sorted(int(q) for q in pair_coefficients),
        "pair_fourier_coefficient_magnitudes": pair_coefficients,
        "indicator_pattern_records": pattern_records,
    }


def local_box_form(
    start_i: int,
    start_j: int,
    length: int,
    h: int,
    primes: Sequence[int] = PRIMES,
) -> Tuple[int, int, int, Fraction]:
    """Return U_I, U_J, N_h and the exactly centered local box form."""

    validate_primes(primes)
    if length < 0:
        raise ValueError("length must be nonnegative")
    modulus = math.prod(primes)
    i_values = [
        m for m in range(start_i, start_i + length) if math.gcd(m, modulus) == 1
    ]
    j_values = [
        n for n in range(start_j, start_j + length) if math.gcd(n, modulus) == 1
    ]
    active = tuple(p for p in primes if h % p != 0)
    n_h = sum(
        1
        for m in i_values
        for n in j_values
        if all((m * n + h) % p != 0 for p in active)
    )
    centered_form = Fraction(n_h, 1) / kappa(active) - len(i_values) * len(j_values)
    return len(i_values), len(j_values), n_h, centered_form


def exact_support_contributions(
    start_i: int,
    start_j: int,
    length: int,
    h: int,
    primes: Sequence[int] = PRIMES,
) -> Tuple[Dict[int, Fraction], Dict[int, Fraction]]:
    """Return fully-active fixed-kernel and shift energy by exact conductor.

    Character orthogonality is evaluated through the exact local identity
    ``sum_{chi_p != 1} chi_p(x) conjugate(chi_p(y)) = p-2`` when
    ``x == y (mod p)``, and ``-1`` otherwise.  No floating-point roots of
    unity are used.
    """

    validate_primes(primes)
    if length < 0:
        raise ValueError("length must be nonnegative")
    modulus = math.prod(primes)
    if math.gcd(h, modulus) != 1:
        raise ValueError("exact support decomposition requires (h, Q) = 1")
    i_values = [
        m for m in range(start_i, start_i + length) if math.gcd(m, modulus) == 1
    ]
    j_values = [
        n for n in range(start_j, start_j + length) if math.gcd(n, modulus) == 1
    ]

    fixed: Dict[int, Fraction] = {}
    energy: Dict[int, Fraction] = {}
    for support in nonempty_supports(primes):
        q = math.prod(support)
        d_value = Fraction(1, math.prod(p - 2 for p in support))

        fixed_numerator = 0
        for m in i_values:
            for n in j_values:
                local_sum = 1
                for p in support:
                    local_sum *= p - 2 if (m * n + h) % p == 0 else -1
                fixed_numerator += local_sum
        fixed[q] = (-1) ** len(support) * d_value * fixed_numerator

        product_counts = Counter((m * n) % q for m in i_values for n in j_values)
        energy_numerator = 0
        for left, left_count in product_counts.items():
            for right, right_count in product_counts.items():
                local_sum = 1
                for p in support:
                    local_sum *= p - 2 if left % p == right % p else -1
                energy_numerator += left_count * right_count * local_sum
        energy[q] = d_value * d_value * energy_numerator

    return fixed, energy


def kernel_certificate(
    start_i: int = 19,
    start_j: int = 73,
    length: int = 83,
    cutoff: int = 40,
    primes: Sequence[int] = PRIMES,
) -> Dict[str, object]:
    """Check finite fixed-shift and complete-shift inequalities."""

    validate_primes(primes)
    if length < 0:
        raise ValueError("length must be nonnegative")
    if cutoff < 1:
        raise ValueError("cutoff must be positive")
    modulus = math.prod(primes)
    group = units(modulus)
    u_i, u_j, n_two, b_two = local_box_form(
        start_i, start_j, length, 2, primes
    )

    shift_values: List[Fraction] = []
    for ell in group:
        _, _, _, value = local_box_form(
            start_i, start_j, length, 2 * ell, primes
        )
        shift_values.append(value)
    shift_mean_square = sum((v * v for v in shift_values), Fraction(0)) / len(group)
    shift_mean = sum(shift_values, Fraction(0)) / len(group)

    fixed_support, energy_support = exact_support_contributions(
        start_i, start_j, length, 2, primes
    )
    fixed_low = sum(
        (value for q, value in fixed_support.items() if q <= cutoff), Fraction(0)
    )
    fixed_high = sum(
        (value for q, value in fixed_support.items() if q > cutoff), Fraction(0)
    )
    energy_low = sum(
        (value for q, value in energy_support.items() if q <= cutoff), Fraction(0)
    )
    energy_high = sum(
        (value for q, value in energy_support.items() if q > cutoff), Fraction(0)
    )

    xi_value = xi(primes)
    r = len(primes)
    g = phi_squarefree(primes)
    complete_low_bound = Fraction(17**r * cutoff**3)
    complete_high_bound = (
        xi_value * xi_value * g * length**3 / (cutoff * cutoff)
    )
    fixed_low_bound = Fraction(5**r * cutoff**2)
    fixed_high_bound = xi_value * g * length / cutoff

    return {
        "modulus": modulus,
        "primes": list(primes),
        "interval_i": {"start": start_i, "length": length},
        "interval_j": {"start": start_j, "length": length},
        "cutoff": cutoff,
        "unit_counts": {"I": u_i, "J": u_j},
        "h_2_allowed_pair_count": n_two,
        "h_2_centered_box_form": frac_record(b_two),
        "fixed_contributions_by_conductor": {
            str(q): frac_record(value) for q, value in sorted(fixed_support.items())
        },
        "fixed_low_part": frac_record(fixed_low),
        "fixed_high_part": frac_record(fixed_high),
        "fixed_parts_reconstruct": fixed_low + fixed_high == b_two,
        "fixed_low_bound": frac_record(fixed_low_bound),
        "fixed_high_bound": frac_record(fixed_high_bound),
        "fixed_low_bound_verified": abs(fixed_low) <= fixed_low_bound,
        "fixed_high_bound_verified": abs(fixed_high) <= fixed_high_bound,
        "complete_shift_mean": frac_record(shift_mean),
        "complete_shift_mean_square": frac_record(shift_mean_square),
        "energy_contributions_by_conductor": {
            str(q): frac_record(value) for q, value in sorted(energy_support.items())
        },
        "complete_low_energy": frac_record(energy_low),
        "complete_high_energy": frac_record(energy_high),
        "energy_parts_reconstruct": energy_low + energy_high == shift_mean_square,
        "complete_low_energy_bound": frac_record(complete_low_bound),
        "complete_high_energy_bound": frac_record(complete_high_bound),
        "complete_low_bound_verified": energy_low <= complete_low_bound,
        "complete_high_bound_verified": energy_high <= complete_high_bound,
    }


def build_certificate() -> Dict[str, object]:
    fibers = [
        rough_fiber_certificate(37, 83, PRIMES, support)
        for support in nonempty_supports(PRIMES)
    ]
    return {
        "description": (
            "Exact finite certificates for inclusion-exclusion character "
            "suppression, designed one-prime mode annihilation, and local "
            "kernel bounds. These are not prime-pair computations."
        ),
        "rough_fibers": fibers,
        "designed_square": designed_square_certificate(),
        "kernel": kernel_certificate(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="write the JSON certificate to this path; otherwise print it",
    )
    args = parser.parse_args()
    payload = json.dumps(build_certificate(), indent=2, sort_keys=True)
    if args.output is None:
        print(payload)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
