"""Exact deterministic finite certificate for TPC-22.

The certificate uses only the Python standard library.  Every algebraic
identity is checked with integers, :class:`fractions.Fraction`, or exact roots
of unity in the finite field F_61.  There are no floating-point tolerances and
no ``assert`` statements, so optimized ``python -O`` runs perform precisely
the same checks.

This is a finite consistency certificate.  It is not numerical evidence for
twin primes, an asymptotic formula, full residual dispersion, or a breach of
the sieve parity barrier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence, Tuple


FIELD_PRIME = 61
FIELD_ORDER = FIELD_PRIME - 1
Q = 30
PAIR_CASES = ((10, 15), (15, 10))


def require(condition: bool, message: str) -> None:
    """Raise in ordinary and optimized Python alike."""

    if not condition:
        raise RuntimeError(message)


def factorization(n: int) -> Dict[int, int]:
    require(n >= 1, "factorization requires a positive integer")
    answer: Dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            answer[divisor] = answer.get(divisor, 0) + 1
            n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        answer[n] = answer.get(n, 0) + 1
    return answer


def divisors(n: int) -> List[int]:
    result = [1]
    for prime, exponent in factorization(n).items():
        result = [
            old * prime**power
            for old in result
            for power in range(exponent + 1)
        ]
    return sorted(result)


def mobius(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def euler_phi(n: int) -> int:
    answer = n
    for prime in factorization(n):
        answer -= answer // prime
    return answer


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def primitive_root(prime: int) -> int:
    require(is_prime(prime), "primitive-root modulus is not prime")
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factorization(prime - 1)
        ):
            return candidate
    raise RuntimeError("primitive-root search failed")


FIELD_GENERATOR = primitive_root(FIELD_PRIME)


def field_root(order: int) -> int:
    require(order >= 1 and FIELD_ORDER % order == 0, "unsupported root order")
    root = pow(FIELD_GENERATOR, FIELD_ORDER // order, FIELD_PRIME)
    require(pow(root, order, FIELD_PRIME) == 1, "root has wrong order")
    for prime in factorization(order):
        require(
            pow(root, order // prime, FIELD_PRIME) != 1,
            "root is not primitive",
        )
    return root


def finite_exp(modulus: int, exponent: int) -> int:
    if modulus == 1:
        return 1
    return pow(field_root(modulus), exponent % modulus, FIELD_PRIME)


def units(modulus: int) -> List[int]:
    if modulus == 1:
        return [0]
    return [value for value in range(modulus) if math.gcd(value, modulus) == 1]


def ramanujan_sum(modulus: int, frequency: int) -> int:
    return sum(
        divisor * mobius(modulus // divisor)
        for divisor in divisors(math.gcd(modulus, frequency))
    )


def canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def fraction_record(value: Fraction | int) -> Dict[str, int | str]:
    value = Fraction(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


# A character modulo a squarefree integer is represented by one exponent
# modulo p-1 at every prime p dividing the modulus, in increasing prime order.
Character = Tuple[int, ...]


def all_characters(modulus: int) -> List[Character]:
    primes = list(factorization(modulus))
    if not primes:
        return [()]
    return list(itertools.product(*(range(prime - 1) for prime in primes)))


def principal_character(modulus: int) -> Character:
    return tuple(0 for _ in factorization(modulus))


def inverse_character(character: Character, modulus: int) -> Character:
    return tuple(
        (-index) % (prime - 1)
        for prime, index in zip(factorization(modulus), character)
    )


def multiply_characters(
    left: Character,
    right: Character,
    modulus: int,
) -> Character:
    primes = list(factorization(modulus))
    require(len(left) == len(primes), "left character has wrong arity")
    require(len(right) == len(primes), "right character has wrong arity")
    return tuple(
        (left_index + right_index) % (prime - 1)
        for prime, left_index, right_index in zip(primes, left, right)
    )


def restrict_character(
    source_modulus: int,
    character: Character,
    target_modulus: int,
) -> Character:
    source = dict(zip(factorization(source_modulus), character))
    target_primes = list(factorization(target_modulus))
    require(
        all(prime in source for prime in target_primes),
        "target character modulus does not divide the source support",
    )
    return tuple(source[prime] for prime in target_primes)


def external_product(
    modulus: int,
    factors: Sequence[Tuple[int, Character]],
) -> Character:
    local: Dict[int, int] = {}
    product = 1
    for factor_modulus, character in factors:
        require(math.gcd(product, factor_modulus) == 1, "noncoprime CRT factors")
        product *= factor_modulus
        primes = list(factorization(factor_modulus))
        require(len(primes) == len(character), "factor character has wrong arity")
        for prime, index in zip(primes, character):
            require(prime not in local, "CRT prime repeated")
            local[prime] = index
    require(product == modulus, "CRT factor product has wrong modulus")
    modulus_primes = list(factorization(modulus))
    require(set(local) == set(modulus_primes), "CRT character support mismatch")
    return tuple(local[prime] for prime in modulus_primes)


def local_discrete_log(prime: int, value: int) -> int:
    value %= prime
    require(value != 0, "discrete log requested at a nonunit")
    if prime == 2:
        return 0
    generator = primitive_root(prime)
    current = 1
    for exponent in range(prime - 1):
        if current == value:
            return exponent
        current = current * generator % prime
    raise RuntimeError("local discrete log failed")


def character_value(modulus: int, character: Character, value: int) -> int:
    primes = list(factorization(modulus))
    require(len(character) == len(primes), "character has wrong arity")
    if modulus == 1:
        return 1
    if math.gcd(value, modulus) != 1:
        return 0
    answer = 1
    for prime, index in zip(primes, character):
        if prime == 2:
            continue
        logarithm = local_discrete_log(prime, value)
        answer = (
            answer
            * pow(field_root(prime - 1), index * logarithm, FIELD_PRIME)
        ) % FIELD_PRIME
    return answer


def conjugate_character_value(
    modulus: int,
    character: Character,
    value: int,
) -> int:
    return character_value(modulus, inverse_character(character, modulus), value)


def character_conductor(modulus: int, character: Character) -> int:
    conductor = 1
    for prime, index in zip(factorization(modulus), character):
        if index != 0:
            conductor *= prime
    return conductor


def inducing_character(modulus: int, character: Character) -> Tuple[int, Character]:
    conductor = character_conductor(modulus, character)
    primitive = tuple(
        index
        for prime, index in zip(factorization(modulus), character)
        if index != 0
    )
    return conductor, primitive


def gauss_sum(modulus: int, character: Character, frequency: int) -> int:
    return sum(
        character_value(modulus, character, value)
        * finite_exp(modulus, frequency * value)
        for value in units(modulus)
    ) % FIELD_PRIME


def primitive_gauss_sum(conductor: int, character: Character) -> int:
    if conductor == 1:
        return 1
    return sum(
        character_value(conductor, character, value)
        * finite_exp(conductor, value)
        for value in units(conductor)
    ) % FIELD_PRIME


ROWS: List[Dict[str, int]] = [
    {"ell": 7, "d": 1, "m": 7, "x": 2, "y": -1},
    {"ell": 11, "d": 7, "m": 77, "x": -3, "y": 2},
    {"ell": 13, "d": 11, "m": 143, "x": 5, "y": 3},
    {"ell": 17, "d": 13, "m": 221, "x": 1, "y": -2},
    {"ell": 19, "d": 7, "m": 133, "x": -2, "y": 5},
    {"ell": 23, "d": 11, "m": 253, "x": 4, "y": 1},
    {"ell": 29, "d": 13, "m": 377, "x": -1, "y": 4},
    {"ell": 31, "d": 7, "m": 217, "x": 3, "y": -3},
    {"ell": 37, "d": 11, "m": 407, "x": 2, "y": 2},
    {"ell": 41, "d": 13, "m": 533, "x": -4, "y": 1},
]


def generic_mask(left: Mapping[str, int], right: Mapping[str, int]) -> int:
    return int(
        left["ell"] != right["ell"]
        and abs(left["m"] - right["m"]) > 70
        and math.gcd(left["d"], right["d"]) <= 1
    )


def masked_character_sum(
    left_modulus: int,
    right_modulus: int,
    left_character: Character,
    right_character: Character,
    mask: Callable[[Mapping[str, int], Mapping[str, int]], int] = generic_mask,
) -> int:
    return sum(
        left["x"]
        * right["y"]
        * mask(left, right)
        * character_value(left_modulus, left_character, left["m"])
        * character_value(right_modulus, right_character, right["m"])
        for left in ROWS
        for right in ROWS
    ) % FIELD_PRIME


def rectangle_sum(
    g: int,
    left_modulus: int,
    right_modulus: int,
    left_character: Character,
    right_character: Character,
    *,
    compatibility: bool = True,
) -> int:
    return sum(
        left["x"]
        * right["y"]
        * generic_mask(left, right)
        * int(not compatibility or (left["m"] - right["m"]) % g == 0)
        * character_value(left_modulus, left_character, left["m"])
        * character_value(right_modulus, right_character, right["m"])
        for left in ROWS
        for right in ROWS
    ) % FIELD_PRIME


def check_rectangularization() -> Tuple[Dict[str, object], int]:
    checks = 0
    records: List[Dict[str, object]] = []
    failure_totals = {
        "omit_compatibility": 0,
        "wrong_b_equals_v": 0,
        "omit_shared_g_coordinate": 0,
        "omit_shared_g_projector_sum": 0,
        "extra_one_over_phi_g": 0,
        "delete_one_sided_principal": 0,
    }

    for u, v in PAIR_CASES:
        g = math.gcd(u, v)
        a = u // g
        b = v // g
        require(math.lcm(u, v) == Q, "pair has wrong lcm")
        require(
            math.gcd(g, a) == math.gcd(g, b) == math.gcd(a, b) == 1,
            "g,a,b are not pairwise coprime",
        )
        case_failures = {key: 0 for key in failure_totals}
        transforms: List[Dict[str, object]] = []

        for chi in all_characters(Q):
            chi_g = restrict_character(Q, chi, g)
            chi_a = restrict_character(Q, chi, a)
            chi_b = restrict_character(Q, chi, b)
            alpha_u = external_product(u, ((g, chi_g), (a, chi_a)))
            beta_b = chi_b
            alpha_a = chi_a
            beta_v = external_product(v, ((g, chi_g), (b, chi_b)))

            convolution = 0
            principal_psi_term = 0
            for psi in all_characters(g):
                left_shared = multiply_characters(chi_g, psi, g)
                right_shared = inverse_character(psi, g)
                left_character = external_product(
                    u, ((g, left_shared), (a, chi_a))
                )
                right_character = external_product(
                    v, ((g, right_shared), (b, chi_b))
                )
                term = masked_character_sum(
                    u, v, left_character, right_character
                )
                convolution += term
                if psi == principal_character(g):
                    principal_psi_term = term
            projected = (
                convolution * pow(euler_phi(g), -1, FIELD_PRIME)
            ) % FIELD_PRIME

            primary = rectangle_sum(g, u, b, alpha_u, beta_b)
            symmetric = rectangle_sum(g, a, v, alpha_a, beta_v)
            require(projected == primary, "primary rectangularization failed")
            require(projected == symmetric, "symmetric rectangularization failed")
            checks += 2

            conductor = character_conductor(Q, chi)
            primary_product = (
                character_conductor(u, alpha_u)
                * character_conductor(b, beta_b)
            )
            symmetric_product = (
                character_conductor(a, alpha_a)
                * character_conductor(v, beta_v)
            )
            require(conductor == primary_product, "primary conductor product failed")
            require(
                conductor == symmetric_product,
                "symmetric conductor product failed",
            )
            checks += 2

            if chi == principal_character(Q):
                require(alpha_u == principal_character(u), "principal alpha mismatch")
                require(beta_b == principal_character(b), "principal beta mismatch")
                require(alpha_a == principal_character(a), "symmetric alpha mismatch")
                require(beta_v == principal_character(v), "symmetric beta mismatch")
                checks += 4

            wrong_omit_compatibility = rectangle_sum(
                g,
                u,
                b,
                alpha_u,
                beta_b,
                compatibility=False,
            )
            wrong_b_equals_v = rectangle_sum(g, u, v, alpha_u, beta_v)
            wrong_omit_shared = rectangle_sum(g, a, b, alpha_a, beta_b)
            wrong_omit_projector = (
                principal_psi_term * pow(euler_phi(g), -1, FIELD_PRIME)
            ) % FIELD_PRIME
            wrong_extra_normalization = (
                primary * pow(euler_phi(g), -1, FIELD_PRIME)
            ) % FIELD_PRIME

            variants = {
                "omit_compatibility": wrong_omit_compatibility,
                "wrong_b_equals_v": wrong_b_equals_v,
                "omit_shared_g_coordinate": wrong_omit_shared,
                "omit_shared_g_projector_sum": wrong_omit_projector,
                "extra_one_over_phi_g": wrong_extra_normalization,
            }
            for name, wrong_value in variants.items():
                if wrong_value != primary:
                    case_failures[name] += 1

            primary_one_sided = (
                character_conductor(u, alpha_u) == 1
            ) != (character_conductor(b, beta_b) == 1)
            symmetric_one_sided = (
                character_conductor(a, alpha_a) == 1
            ) != (character_conductor(v, beta_v) == 1)
            if primary != 0 and (primary_one_sided or symmetric_one_sided):
                case_failures["delete_one_sided_principal"] += 1

            transforms.append(
                {
                    "global_character": list(chi),
                    "global_conductor": conductor,
                    "primary_coordinate_conductors": [
                        character_conductor(u, alpha_u),
                        character_conductor(b, beta_b),
                    ],
                    "symmetric_coordinate_conductors": [
                        character_conductor(a, alpha_a),
                        character_conductor(v, beta_v),
                    ],
                    "rectangular_value_mod_61": primary,
                }
            )

        for name, count in case_failures.items():
            require(count > 0, f"hard-failure variant was not detected: {name}")
            checks += 1
            failure_totals[name] += count

        records.append(
            {
                "u": u,
                "v": v,
                "q": Q,
                "g": g,
                "a": a,
                "b": b,
                "character_count": len(all_characters(Q)),
                "hard_failure_counts": case_failures,
                "transforms": transforms,
                "digest_sha256": canonical_digest(transforms),
            }
        )

    for name, count in failure_totals.items():
        require(count > 0, f"global hard-failure count vanished: {name}")
        checks += 1

    return {
        "cases": records,
        "hard_failure_totals": failure_totals,
        "digest_sha256": canonical_digest(records),
    }, checks


def check_gauss_conductor_formula() -> Tuple[Dict[str, object], int]:
    checks = 0
    records: List[Dict[str, object]] = []
    conductor_counts: Dict[int, int] = {}
    failure_count_if_ramanujan_factor_is_omitted = 0

    for chi in all_characters(Q):
        conductor, primitive = inducing_character(Q, chi)
        d = Q // conductor
        tau = primitive_gauss_sum(conductor, primitive)
        conductor_counts[conductor] = conductor_counts.get(conductor, 0) + 1
        values: List[int] = []
        for frequency in range(Q):
            direct = gauss_sum(Q, chi, frequency)
            if math.gcd(frequency, conductor) > 1:
                predicted = 0
            else:
                predicted = (
                    conjugate_character_value(conductor, primitive, frequency)
                    * character_value(conductor, primitive, d)
                    * tau
                    * ramanujan_sum(d, frequency)
                ) % FIELD_PRIME
            require(direct == predicted, "induced Gauss formula failed")
            checks += 1

            if math.gcd(frequency, conductor) == 1:
                wrong = (
                    conjugate_character_value(conductor, primitive, frequency)
                    * character_value(conductor, primitive, d)
                    * tau
                ) % FIELD_PRIME
                if wrong != direct:
                    failure_count_if_ramanujan_factor_is_omitted += 1
            values.append(direct)

        records.append(
            {
                "character": list(chi),
                "conductor": conductor,
                "complementary_modulus": d,
                "primitive_gauss_sum_mod_61": tau,
                "all_frequency_values_mod_61": values,
            }
        )

    require(
        failure_count_if_ramanujan_factor_is_omitted > 0,
        "Ramanujan-factor hard failure was not detected",
    )
    checks += 1
    conductor_mass = sum(
        character_conductor(Q, chi) for chi in all_characters(Q)
    )
    require(conductor_mass == euler_phi(Q) ** 2, "conductor mass identity failed")
    checks += 1

    return {
        "q": Q,
        "character_count": len(all_characters(Q)),
        "frequency_count": Q,
        "all_r_mod_q_checked": True,
        "conductor_counts": {
            str(key): conductor_counts[key] for key in sorted(conductor_counts)
        },
        "conductor_mass": conductor_mass,
        "failures_if_ramanujan_factor_is_omitted": (
            failure_count_if_ramanujan_factor_is_omitted
        ),
        "characters": records,
        "digest_sha256": canonical_digest(records),
    }, checks


def eta_star_entries(beta: Fraction, delta: Fraction) -> Tuple[Fraction, ...]:
    return (
        1 - Fraction(3, 2) * beta,
        (beta + 4 * delta - 1) / 2,
        (6 * delta - beta) / 4,
    )


def profile_ledger(
    name: str,
    lambda_base: Fraction,
    d0_constant: Fraction,
    d0_sigma_coefficient: Fraction,
    delta_constant: Fraction,
    sigma: Fraction,
    t: Fraction,
) -> Dict[str, object]:
    lambda_value = lambda_base - sigma
    d0_exponent = d0_constant + d0_sigma_coefficient * sigma
    delta = delta_constant - Fraction(2, 3) * sigma + t
    beta_lower = lambda_value + d0_exponent
    beta_upper = lambda_value + Fraction(1, 4) - delta / 2
    lower_entries = eta_star_entries(beta_lower, delta)
    upper_entries = eta_star_entries(beta_upper, delta)
    uniform_entries = (upper_entries[0], lower_entries[1], upper_entries[2])
    require(beta_lower < beta_upper, f"{name} profile interval is empty")
    return {
        "profile": name,
        "sigma": fraction_record(sigma),
        "t": fraction_record(t),
        "lambda_exponent": fraction_record(lambda_value),
        "D0_exponent": fraction_record(d0_exponent),
        "delta": fraction_record(delta),
        "beta_range": {
            "strict_lower_endpoint": fraction_record(beta_lower),
            "upper_endpoint": fraction_record(beta_upper),
            "comes_from_actual_D_greater_than_D0": True,
        },
        "uniform_three_cell_margins": [
            fraction_record(value) for value in uniform_entries
        ],
    }


def check_exponent_profile_ledger() -> Tuple[Dict[str, object], int]:
    checks = 0
    published_zero = profile_ledger(
        "published",
        Fraction(10, 21),
        Fraction(1, 21),
        Fraction(-1),
        Fraction(19, 126),
        Fraction(0),
        Fraction(0),
    )
    li_zero = profile_ledger(
        "li_v6",
        Fraction(8, 17),
        Fraction(1, 17),
        Fraction(1, 2),
        Fraction(5, 34),
        Fraction(0),
        Fraction(0),
    )
    published_expected = (Fraction(1, 42), Fraction(4, 63), Fraction(4, 63))
    li_expected = (Fraction(1, 34), Fraction(1, 17), Fraction(1, 17))
    published_actual = tuple(
        Fraction(item["numerator"], item["denominator"])
        for item in published_zero["uniform_three_cell_margins"]
    )
    li_actual = tuple(
        Fraction(item["numerator"], item["denominator"])
        for item in li_zero["uniform_three_cell_margins"]
    )
    require(published_actual == published_expected, "published zero ledger failed")
    require(li_actual == li_expected, "Li zero ledger failed")
    checks += 2

    # Verify the full affine formulas at exact rational sample points.
    affine_samples: List[Dict[str, object]] = []
    for sigma, t in (
        (Fraction(1, 100), Fraction(0)),
        (Fraction(1, 200), Fraction(1, 1000)),
    ):
        record = profile_ledger(
            "published",
            Fraction(10, 21),
            Fraction(1, 21),
            Fraction(-1),
            Fraction(19, 126),
            sigma,
            t,
        )
        actual = tuple(
            Fraction(item["numerator"], item["denominator"])
            for item in record["uniform_three_cell_margins"]
        )
        expected = (
            Fraction(1, 42) + sigma + Fraction(3, 4) * t,
            Fraction(4, 63) - Fraction(7, 3) * sigma + 2 * t,
            Fraction(4, 63) - Fraction(5, 6) * sigma + Fraction(13, 8) * t,
        )
        require(actual == expected, "published affine ledger failed")
        require(all(value > 0 for value in actual), "published inherited margin failed")
        checks += 2
        affine_samples.append(record)

    for sigma, t in (
        (Fraction(1, 1000), Fraction(0)),
        (Fraction(1, 2000), Fraction(1, 1000)),
    ):
        record = profile_ledger(
            "li_v6",
            Fraction(8, 17),
            Fraction(1, 17),
            Fraction(1, 2),
            Fraction(5, 34),
            sigma,
            t,
        )
        actual = tuple(
            Fraction(item["numerator"], item["denominator"])
            for item in record["uniform_three_cell_margins"]
        )
        expected = (
            Fraction(1, 34) + sigma + Fraction(3, 4) * t,
            Fraction(1, 17) - Fraction(19, 12) * sigma + 2 * t,
            Fraction(1, 17) - Fraction(5, 6) * sigma + Fraction(13, 8) * t,
        )
        require(actual == expected, "Li affine ledger failed")
        require(all(value > 0 for value in actual), "Li inherited margin failed")
        checks += 2
        affine_samples.append(record)

    published_threshold = Fraction(4, 147)
    li_threshold = Fraction(12, 323)
    require(
        Fraction(4, 63) - Fraction(7, 3) * published_threshold == 0,
        "published arithmetic threshold failed",
    )
    require(
        Fraction(1, 17) - Fraction(19, 12) * li_threshold == 0,
        "Li arithmetic threshold failed",
    )
    require(
        Fraction(4, 63) - Fraction(5, 6) * published_threshold > 0,
        "published mixed cell should remain positive at the threshold",
    )
    require(
        Fraction(1, 17) - Fraction(5, 6) * li_threshold > 0,
        "Li mixed cell should remain positive at the threshold",
    )
    checks += 4

    return {
        "published_sigma_zero": published_zero,
        "li_v6_sigma_zero": li_zero,
        "published_sigma_threshold": fraction_record(published_threshold),
        "li_v6_sigma_threshold": fraction_record(li_threshold),
        "thresholds_are_arithmetic_not_upstream_extensions": True,
        "affine_samples": affine_samples,
        "digest_sha256": canonical_digest(affine_samples),
    }, checks


def main() -> None:
    require(FIELD_ORDER % 60 == 0, "F_61 lacks the required roots of unity")
    require(all(math.lcm(u, v) == Q for u, v in PAIR_CASES), "wrong pair lcm")
    require(all(math.gcd(row["m"], Q) == 1 for row in ROWS), "nonunit row")
    require(all(row["ell"] * row["d"] == row["m"] for row in ROWS), "bad row")

    rectangularization, rectangularization_checks = check_rectangularization()
    gauss, gauss_checks = check_gauss_conductor_formula()
    ledger, ledger_checks = check_exponent_profile_ledger()

    source_path = Path(__file__).resolve()
    coverage = {
        "rectangularization_symmetric_coordinates_conductor_equalities": (
            rectangularization_checks
        ),
        "induced_gauss_all_frequency_equalities": gauss_checks,
        "exact_fraction_profile_ledger_equalities": ledger_checks,
    }
    coverage["total_exact_equalities"] = sum(coverage.values())

    report = {
        "certificate": "TPC-22 conductor-rectangularized fibers exact certificate",
        "schema_version": 1,
        "status": "pass",
        "deterministic": True,
        "optimized_mode_safe": True,
        "arithmetic_backends": [
            "integers",
            "fractions.Fraction",
            "exact roots of unity in F_61",
        ],
        "input_summary": {
            "q": Q,
            "pair_cases": [
                {
                    "u": u,
                    "v": v,
                    "g": math.gcd(u, v),
                    "a": u // math.gcd(u, v),
                    "b": v // math.gcd(u, v),
                }
                for u, v in PAIR_CASES
            ],
            "row_count": len(ROWS),
            "finite_field": {
                "prime": FIELD_PRIME,
                "generator": FIELD_GENERATOR,
                "root_group_order": FIELD_ORDER,
            },
        },
        "coverage": coverage,
        "results": {
            "exact_pairwise_rectangularization": rectangularization,
            "induced_character_gauss_formula": gauss,
            "exact_exponent_profile_ledger": ledger,
        },
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "evidence_flags": {
            "twin_prime_evidence": False,
            "hardy_littlewood_evidence": False,
            "full_residual_dispersion_evidence": False,
            "parity_breakthrough_evidence": False,
            "asymptotic_evidence": False,
        },
        "scope_note": (
            "Exact finite algebra and rational exponent bookkeeping only; "
            "no twin-prime, Hardy-Littlewood, full residual-dispersion, "
            "or parity-barrier claim."
        ),
    }
    report["results_digest_sha256"] = canonical_digest(report["results"])
    report["certificate_digest_sha256"] = canonical_digest(report)

    output_path = source_path.with_suffix(".json")
    output_path.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="ascii",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": report["status"],
                "output": str(output_path),
                "total_exact_equalities": coverage["total_exact_equalities"],
                "certificate_digest_sha256": report[
                    "certificate_digest_sha256"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
