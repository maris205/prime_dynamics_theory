"""Exact finite diagnostics for weighted centered sieve kernels.

All reported identities use integers and fractions.  No floating-point
Fourier transform or asymptotic inference is involved.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple


PRIMES: Tuple[int, ...] = (5, 7, 11)
Q = math.prod(PRIMES)


def units(modulus: int) -> List[int]:
    return [a for a in range(modulus) if math.gcd(a, modulus) == 1]


def interval(start: int, length: int) -> List[int]:
    if length <= 0:
        raise ValueError("interval length must be positive")
    return list(range(start, start + length))


def nonempty_supports(primes: Sequence[int] = PRIMES) -> List[int]:
    values: List[int] = []
    for mask in range(1, 1 << len(primes)):
        q = 1
        for i, p in enumerate(primes):
            if mask & (1 << i):
                q *= p
        values.append(q)
    return sorted(values)


def support_primes(q: int, primes: Sequence[int] = PRIMES) -> Tuple[int, ...]:
    selected = tuple(p for p in primes if q % p == 0)
    if math.prod(selected) != q:
        raise ValueError("q must be a squarefree divisor of Q")
    return selected


def kappa(h: int, primes: Sequence[int] = PRIMES) -> Fraction:
    value = Fraction(1)
    for p in primes:
        if h % p != 0:
            value *= Fraction(p - 2, p - 1)
    return value


def require_fully_active(h: int) -> None:
    if math.gcd(h, Q) != 1:
        raise ValueError("exact conductor formulas require (h, Q) = 1")


def centered_kernel(m: int, n: int, h: int) -> Fraction:
    if math.gcd(m * n, Q) != 1:
        raise ValueError("kernel arguments must be Q-units")
    active = math.gcd(m * n + h, Q) == 1
    return (Fraction(1, 1) / kappa(h) if active else Fraction(0)) - 1


def q_unit_coefficients(
    values: Iterable[int], coefficient: Callable[[int], int]
) -> Dict[int, int]:
    return {
        n: coefficient(n)
        for n in values
        if math.gcd(n, Q) == 1 and coefficient(n) != 0
    }


def box_form(a: Mapping[int, int], b: Mapping[int, int], h: int) -> Fraction:
    return sum(
        (
            Fraction(am * bn) * centered_kernel(m, n, h)
            for m, am in a.items()
            for n, bn in b.items()
        ),
        Fraction(0),
    )


def weighted_target(a: Mapping[int, int], b: Mapping[int, int], h: int) -> int:
    return sum(
        am * bn
        for m, am in a.items()
        for n, bn in b.items()
        if math.gcd(m * n + h, Q) == 1
    )


def exact_character_gram(q: int, x: int, y: int) -> int:
    """Sum of chi(x) conjugate(chi(y)) over exact-conductor-q chars."""

    value = 1
    for p in support_primes(q):
        value *= (p - 2) if x % p == y % p else -1
    return value


def second_character_energy(q: int, coefficients: Mapping[int, int]) -> int:
    residue_sums: Dict[int, int] = {}
    for n, value in coefficients.items():
        residue_sums[n % q] = residue_sums.get(n % q, 0) + value
    return sum(
        cx * cy * exact_character_gram(q, x, y)
        for x, cx in residue_sums.items()
        for y, cy in residue_sums.items()
    )


def product_residue_sums(
    q: int, a: Mapping[int, int], b: Mapping[int, int]
) -> Dict[int, int]:
    result: Dict[int, int] = {}
    for m, am in a.items():
        for n, bn in b.items():
            residue = (m * n) % q
            result[residue] = result.get(residue, 0) + am * bn
    return result


def fourth_character_energy(
    q: int, a: Mapping[int, int], b: Mapping[int, int]
) -> int:
    products = product_residue_sums(q, a, b)
    return sum(
        cx * cy * exact_character_gram(q, x, y)
        for x, cx in products.items()
        for y, cy in products.items()
    )


def conductor_weight(q: int) -> Fraction:
    value = Fraction(1)
    for p in support_primes(q):
        value *= Fraction(1, p - 2)
    return value


def fixed_support_contribution(
    q: int, a: Mapping[int, int], b: Mapping[int, int], h: int
) -> Fraction:
    require_fully_active(h)
    local_primes = support_primes(q)
    total = 0
    for m, am in a.items():
        for n, bn in b.items():
            factor = 1
            for p in local_primes:
                factor *= (p - 2) if (m * n + h) % p == 0 else -1
            total += am * bn * factor
    return ((-1) ** len(local_primes)) * conductor_weight(q) * total


def exact_conductor_energy(
    q: int, a: Mapping[int, int], b: Mapping[int, int]
) -> Fraction:
    return conductor_weight(q) ** 2 * fourth_character_energy(q, a, b)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def coefficient_summary(coefficients: Mapping[int, int]) -> Dict[str, int]:
    return {
        "support_size": len(coefficients),
        "sum": sum(coefficients.values()),
        "l1": sum(abs(value) for value in coefficients.values()),
        "l2_squared": sum(value * value for value in coefficients.values()),
    }


def completion_cost(primes: Sequence[int] = PRIMES) -> Fraction:
    kap = kappa(2, primes)
    r = len(primes)
    return kap ** -2 * 4**r + 2 * kap ** -1 * 3**r + 2**r


def build_certificate() -> Dict[str, object]:
    i_values = interval(19, 43)
    j_values = interval(47, 43)
    a = q_unit_coefficients(i_values, lambda n: ((n * n + 3 * n + 1) % 7) - 3)
    b = q_unit_coefficients(j_values, lambda n: ((2 * n + 5) % 5) - 2)
    h = 2
    direct_box = box_form(a, b, h)
    target = weighted_target(a, b, h)
    centered_relation = Fraction(target, 1) / kappa(h) - sum(a.values()) * sum(b.values())

    supports = nonempty_supports()
    fixed_parts = {q: fixed_support_contribution(q, a, b, h) for q in supports}

    shift_values = units(Q)
    shift_boxes = {ell: box_form(a, b, 2 * ell) for ell in shift_values}
    complete_sum = sum((value * value for value in shift_boxes.values()), Fraction(0))
    complete_mean = sum(shift_boxes.values(), Fraction(0)) / len(shift_values)
    complete_mean_square = complete_sum / len(shift_values)

    conductor_energies = {q: exact_conductor_energy(q, a, b) for q in supports}
    second_a = {q: second_character_energy(q, a) for q in supports}
    second_b = {q: second_character_energy(q, b) for q in supports}
    energy_a = coefficient_summary(a)["l2_squared"]
    energy_b = coefficient_summary(b)["l2_squared"]

    short_start = 23
    short_length = 31
    short_all = interval(short_start, short_length)
    short_units = [ell for ell in short_all if math.gcd(ell, Q) == 1]
    short_sum = sum(
        (box_form(a, b, 2 * ell) ** 2 for ell in short_units), Fraction(0)
    )
    completion_discrepancy = abs(short_sum - Fraction(short_length, Q) * complete_sum)
    completion_bound = (
        completion_cost()
        * coefficient_summary(a)["l1"] ** 2
        * coefficient_summary(b)["l1"] ** 2
    )
    unit_count_discrepancy = abs(
        Fraction(len(short_units), 1)
        - Fraction(short_length * len(shift_values), Q)
    )

    return {
        "schema": "tpc5-exact-weighted-kernel-v1",
        "modulus": Q,
        "primes": list(PRIMES),
        "group_size": len(shift_values),
        "kappa_h2": fraction_text(kappa(2)),
        "intervals": {
            "I": {"start": i_values[0], "length": len(i_values)},
            "J": {"start": j_values[0], "length": len(j_values)},
        },
        "coefficients": {
            "a": coefficient_summary(a),
            "b": coefficient_summary(b),
        },
        "fixed_h2": {
            "weighted_target": target,
            "direct_box": fraction_text(direct_box),
            "centered_relation": fraction_text(centered_relation),
            "support_contributions": {
                str(q): fraction_text(value) for q, value in fixed_parts.items()
            },
            "support_sum": fraction_text(sum(fixed_parts.values(), Fraction(0))),
        },
        "complete_shift": {
            "mean": fraction_text(complete_mean),
            "mean_square": fraction_text(complete_mean_square),
            "conductor_energies": {
                str(q): fraction_text(value)
                for q, value in conductor_energies.items()
            },
            "conductor_energy_sum": fraction_text(
                sum(conductor_energies.values(), Fraction(0))
            ),
        },
        "exact_conductor_second_moments": {
            str(q): {
                "a": second_a[q],
                "a_bound": (q + len(i_values)) * energy_a,
                "b": second_b[q],
                "b_bound": (q + len(j_values)) * energy_b,
            }
            for q in supports
        },
        "short_shift_completion": {
            "start": short_start,
            "length": short_length,
            "unit_count": len(short_units),
            "unit_count_discrepancy": fraction_text(unit_count_discrepancy),
            "unit_count_bound": 2 ** len(PRIMES),
            "square_sum_discrepancy": fraction_text(completion_discrepancy),
            "completion_bound": fraction_text(completion_bound),
        },
    }


def validate_certificate(certificate: Mapping[str, object]) -> None:
    fixed = certificate["fixed_h2"]
    complete = certificate["complete_shift"]
    short = certificate["short_shift_completion"]
    if fixed["direct_box"] != fixed["centered_relation"]:
        raise AssertionError("weighted centering relation failed")
    if fixed["direct_box"] != fixed["support_sum"]:
        raise AssertionError("fixed conductor reconstruction failed")
    if complete["mean"] != "0":
        raise AssertionError("complete shift mean is not zero")
    if complete["mean_square"] != complete["conductor_energy_sum"]:
        raise AssertionError("shift Parseval reconstruction failed")
    for entry in certificate["exact_conductor_second_moments"].values():
        if not (0 <= entry["a"] <= entry["a_bound"]):
            raise AssertionError("a conductor orthogonality bound failed")
        if not (0 <= entry["b"] <= entry["b_bound"]):
            raise AssertionError("b conductor orthogonality bound failed")
    if Fraction(short["unit_count_discrepancy"]) > short["unit_count_bound"]:
        raise AssertionError("unit count completion bound failed")
    if Fraction(short["square_sum_discrepancy"]) > Fraction(short["completion_bound"]):
        raise AssertionError("weighted shift completion bound failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    validate_certificate(certificate)
    rendered = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
