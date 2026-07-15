"""Exact deterministic finite certificate for TPC-21.

All pass/fail decisions use integers, :class:`fractions.Fraction`, or exact
roots of unity in the finite field F_61.  In particular, the certificate does
not use floating-point tolerances and does not use ``assert`` (which would be
disabled by ``python -O``).

The finite identities certified here are algebraic consistency checks.  They
are not numerical evidence for twin primes, residual dispersion, an
asymptotic formula, or a breach of the sieve parity barrier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple


FIELD_PRIME = 61
FIELD_ORDER = FIELD_PRIME - 1
Q = 30
U = 10
V = 15
G = 5
H_SHIFT = 47
H_RADICAL = 47
SHARED_FACTOR_CASES = [(10, 15), (15, 10)]


def require(condition: bool, message: str) -> None:
    """Raise in ordinary and optimized Python alike."""

    if not condition:
        raise RuntimeError(message)


def prime_factorization(n: int) -> Dict[int, int]:
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
    for prime, exponent in prime_factorization(n).items():
        result = [
            old * prime**power
            for old in result
            for power in range(exponent + 1)
        ]
    return sorted(result)


def mobius(n: int) -> int:
    factors = prime_factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def euler_phi(n: int) -> int:
    result = n
    for prime in prime_factorization(n):
        result -= result // prime
    return result


def is_squarefree(n: int) -> bool:
    return all(exponent == 1 for exponent in prime_factorization(n).values())


def units(n: int) -> List[int]:
    if n == 1:
        return [0]
    return [value for value in range(n) if math.gcd(value, n) == 1]


def reduce_unit(value: int, modulus: int) -> int:
    return 0 if modulus == 1 else value % modulus


def ramanujan_sum(q: int, n: int) -> int:
    return sum(
        divisor * mobius(q // divisor)
        for divisor in divisors(math.gcd(q, n))
    )


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
    require(prime >= 2, "prime modulus must be at least two")
    require(is_prime(prime), "modulus is not prime")
    factors = prime_factorization(prime - 1)
    for candidate in range(1, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise RuntimeError("primitive root search failed")


FIELD_GENERATOR = primitive_root(FIELD_PRIME)


def field_root(order: int) -> int:
    """Return a primitive ``order``-th root of unity in F_61."""

    require(order >= 1 and FIELD_ORDER % order == 0, "unsupported root order")
    root = pow(FIELD_GENERATOR, FIELD_ORDER // order, FIELD_PRIME)
    require(pow(root, order, FIELD_PRIME) == 1, "root has wrong power")
    for prime in prime_factorization(order):
        require(
            pow(root, order // prime, FIELD_PRIME) != 1,
            "root is not primitive",
        )
    return root


def fraction_to_field(value: Fraction | int) -> int:
    value = Fraction(value)
    require(value.denominator % FIELD_PRIME != 0, "bad field denominator")
    return (
        value.numerator
        * pow(value.denominator, -1, FIELD_PRIME)
    ) % FIELD_PRIME


def finite_exp(modulus: int, exponent: int) -> int:
    if modulus == 1:
        return 1
    return pow(field_root(modulus), exponent % modulus, FIELD_PRIME)


def fraction_record(value: Fraction | int) -> Dict[str, int | str]:
    value = Fraction(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def inverse_character(character: Tuple[int, ...], modulus: int) -> Tuple[int, ...]:
    return tuple(
        (-index) % (prime - 1)
        for prime, index in zip(prime_factorization(modulus), character)
    )


def multiply_characters(
    left: Tuple[int, ...],
    right: Tuple[int, ...],
    modulus: int,
) -> Tuple[int, ...]:
    """Multiply two characters represented by local exponent tuples."""

    primes = list(prime_factorization(modulus))
    require(len(left) == len(primes), "left character has wrong arity")
    require(len(right) == len(primes), "right character has wrong arity")
    return tuple(
        (left_index + right_index) % (prime - 1)
        for prime, left_index, right_index in zip(primes, left, right)
    )


def external_product_character(
    modulus: int,
    factors: Sequence[Tuple[int, Tuple[int, ...]]],
) -> Tuple[int, ...]:
    """Assemble characters on pairwise-coprime factors by CRT."""

    local: Dict[int, int] = {}
    factor_product = 1
    for factor_modulus, character in factors:
        require(
            math.gcd(factor_product, factor_modulus) == 1,
            "CRT character factors are not coprime",
        )
        factor_product *= factor_modulus
        primes = list(prime_factorization(factor_modulus))
        require(len(character) == len(primes), "factor character has wrong arity")
        for prime, index in zip(primes, character):
            require(prime not in local, "CRT character prime was repeated")
            local[prime] = index
    require(factor_product == modulus, "CRT character factors have wrong product")
    modulus_primes = list(prime_factorization(modulus))
    require(set(local) == set(modulus_primes), "CRT character support mismatch")
    return tuple(local[prime] for prime in modulus_primes)


def all_characters(modulus: int) -> List[Tuple[int, ...]]:
    primes = list(prime_factorization(modulus))
    if not primes:
        return [()]
    return list(itertools.product(*(range(prime - 1) for prime in primes)))


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


def character_value(
    modulus: int,
    character: Tuple[int, ...],
    value: int,
) -> int:
    """Evaluate a Dirichlet character as an exact element of F_61."""

    primes = list(prime_factorization(modulus))
    require(len(character) == len(primes), "character has wrong arity")
    if modulus == 1:
        return 1
    if math.gcd(value, modulus) != 1:
        return 0
    result = 1
    for prime, index in zip(primes, character):
        order = prime - 1
        if order == 1:
            continue
        logarithm = local_discrete_log(prime, value)
        result = (
            result * pow(field_root(order), index * logarithm, FIELD_PRIME)
        ) % FIELD_PRIME
    return result


def conjugate_character_value(
    modulus: int,
    character: Tuple[int, ...],
    value: int,
) -> int:
    return character_value(modulus, inverse_character(character, modulus), value)


def character_restriction(
    source_modulus: int,
    character: Tuple[int, ...],
    target_modulus: int,
) -> Tuple[int, ...]:
    require(target_modulus >= 1, "target modulus must be positive")
    source = dict(zip(prime_factorization(source_modulus), character))
    require(
        all(prime in source for prime in prime_factorization(target_modulus)),
        "target is not supported on the source primes",
    )
    return tuple(source[prime] for prime in prime_factorization(target_modulus))


def character_conductor(modulus: int, character: Tuple[int, ...]) -> int:
    conductor = 1
    for prime, index in zip(prime_factorization(modulus), character):
        if index != 0:
            conductor *= prime
    return conductor


def induced_primitive_character(
    modulus: int,
    character: Tuple[int, ...],
) -> Tuple[int, Tuple[int, ...]]:
    conductor = character_conductor(modulus, character)
    selected = [
        index
        for prime, index in zip(prime_factorization(modulus), character)
        if index != 0
    ]
    return conductor, tuple(selected)


def multiplicative_transform(
    modulus: int,
    values: Mapping[int, int],
    character: Tuple[int, ...],
) -> int:
    return sum(
        values[kappa]
        * conjugate_character_value(modulus, character, kappa)
        for kappa in units(modulus)
    ) % FIELD_PRIME


def gauss_sum(modulus: int, character: Tuple[int, ...], frequency: int) -> int:
    return sum(
        character_value(modulus, character, kappa)
        * finite_exp(modulus, frequency * kappa)
        for kappa in units(modulus)
    ) % FIELD_PRIME


def primitive_gauss_sum(
    conductor: int,
    primitive_character: Tuple[int, ...],
) -> int:
    if conductor == 1:
        return 1
    return sum(
        character_value(conductor, primitive_character, value)
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


THETA: Dict[int, Fraction] = {
    1: Fraction(2),
    2: Fraction(-1),
    3: Fraction(3, 2),
    5: Fraction(-2, 3),
    6: Fraction(1),
    10: Fraction(5, 4),
    15: Fraction(-3, 2),
    30: Fraction(7, 5),
}


def generic_mask(left: Mapping[str, int], right: Mapping[str, int]) -> int:
    """A concrete instance of the three-factor generic Schur mask."""

    return int(
        left["ell"] != right["ell"]
        and abs(left["m"] - right["m"]) > 70
        and math.gcd(left["d"], right["d"]) <= 1
    )


def joint_kappa(m1: int, m2: int, u: int, v: int, h: int) -> int | None:
    q = math.lcm(u, v)
    solutions = [
        kappa
        for kappa in units(q)
        if (m1 * kappa + h) % u == 0
        and (m2 * kappa + h) % v == 0
    ]
    require(len(solutions) <= 1, "joint congruence is not unique")
    return solutions[0] if solutions else None


def joint_fiber(
    u: int,
    v: int,
    mask: Callable[[Mapping[str, int], Mapping[str, int]], int],
) -> Dict[int, Fraction]:
    q = math.lcm(u, v)
    answer = {kappa: Fraction(0) for kappa in units(q)}
    for left in ROWS:
        for right in ROWS:
            coefficient = Fraction(left["x"] * right["y"] * mask(left, right))
            if coefficient == 0:
                continue
            kappa = joint_kappa(left["m"], right["m"], u, v, H_SHIFT)
            if kappa is not None:
                answer[kappa] += coefficient
    return answer


def one_row_fiber(modulus: int, coordinate: int, weight: str) -> Fraction:
    return sum(
        (
            Fraction(row[weight])
            for row in ROWS
            if (row["m"] * coordinate + H_SHIFT) % modulus == 0
        ),
        start=Fraction(0),
    )


def prefix(modulus: int, coordinate: int, weight: str) -> Fraction:
    return sum(
        (
            THETA[divisor]
            * one_row_fiber(
                divisor,
                reduce_unit(coordinate, divisor),
                weight,
            )
            for divisor in divisors(modulus)
        ),
        start=Fraction(0),
    )


def unmasked_lcm_fiber(modulus: int, coordinate: int) -> Fraction:
    total = Fraction(0)
    for u in divisors(modulus):
        for v in divisors(modulus):
            if math.lcm(u, v) != modulus:
                continue
            total += (
                THETA[u]
                * THETA[v]
                * one_row_fiber(u, reduce_unit(coordinate, u), "x")
                * one_row_fiber(v, reduce_unit(coordinate, v), "y")
            )
    return total


def prefix_product_mean(modulus: int) -> Fraction:
    return sum(
        (
            prefix(modulus, coordinate, "x")
            * prefix(modulus, coordinate, "y")
            for coordinate in units(modulus)
        ),
        start=Fraction(0),
    ) / euler_phi(modulus)


def centered_prefix(modulus: int, coordinate: int) -> Fraction:
    return (
        prefix(modulus, coordinate, "x")
        * prefix(modulus, coordinate, "y")
        - prefix_product_mean(modulus)
    )


def lcm_mean(modulus: int) -> Fraction:
    return sum(
        (unmasked_lcm_fiber(modulus, kappa) for kappa in units(modulus)),
        start=Fraction(0),
    ) / euler_phi(modulus)


def centered_lcm(modulus: int, coordinate: int) -> Fraction:
    return unmasked_lcm_fiber(modulus, coordinate) - lcm_mean(modulus)


def additive_transform_fraction(
    modulus: int,
    values: Mapping[int, Fraction],
    frequency: int,
) -> int:
    h_inverse = 0 if modulus == 1 else pow(H_RADICAL, -1, modulus)
    return sum(
        fraction_to_field(values[kappa])
        * finite_exp(modulus, frequency * h_inverse * kappa)
        for kappa in units(modulus)
    ) % FIELD_PRIME


def check_compatible_fibers() -> Tuple[Dict[str, object], int]:
    records: List[Dict[str, object]] = []
    checks = 0
    cases = [(10, 15), (6, 10), (5, 15), (1, 30), (6, 15)]
    for u, v in cases:
        q = math.lcm(u, v)
        fiber = joint_fiber(u, v, generic_mask)
        compatible_total = Fraction(0)
        compatible_pairs = 0
        for left in ROWS:
            for right in ROWS:
                coefficient = Fraction(
                    left["x"] * right["y"] * generic_mask(left, right)
                )
                if coefficient == 0:
                    continue
                if joint_kappa(left["m"], right["m"], u, v, H_SHIFT) is not None:
                    compatible_pairs += 1
                    compatible_total += coefficient
        fiber_total = sum(fiber.values(), start=Fraction(0))
        require(fiber_total == compatible_total, "compatible fiber total failed")
        checks += 1
        mean = fiber_total / euler_phi(q)
        require(
            sum((value - mean for value in fiber.values()), start=Fraction(0)) == 0,
            "compatible fiber centering failed",
        )
        checks += 1
        records.append(
            {
                "u": u,
                "v": v,
                "q": q,
                "compatible_pairs": compatible_pairs,
                "total": fraction_record(fiber_total),
                "mean": fraction_record(mean),
            }
        )
    return {"cases": records, "digest_sha256": canonical_digest(records)}, checks


def check_lcm_occupancy_product() -> Tuple[Dict[str, object], int]:
    records: List[Dict[str, object]] = []
    checks = 0
    for q in [1, 2, 3, 5, 6, 10, 15, 30, 42, 70, 105, 210]:
        require(is_squarefree(q), "occupancy test modulus is not squarefree")
        left = sum(
            (
                Fraction(1, u * v)
                for u in divisors(q)
                for v in divisors(q)
                if math.lcm(u, v) == q
            ),
            start=Fraction(0),
        )
        right = Fraction(1)
        for prime in prime_factorization(q):
            right *= Fraction(2, prime) + Fraction(1, prime * prime)
        alternative = Fraction(1, q)
        for prime in prime_factorization(q):
            alternative *= 2 + Fraction(1, prime)
        require(left == right == alternative, "squarefree lcm product failed")
        checks += 2
        records.append({"q": q, "value": fraction_record(left)})
    return {"cases": records, "digest_sha256": canonical_digest(records)}, checks


def check_divisor_reassembly() -> Tuple[Dict[str, object], int]:
    checks = 0
    records: List[Dict[str, object]] = []
    for s in divisors(Q):
        for coordinate in units(s):
            cumulative = sum(
                (
                    unmasked_lcm_fiber(q, reduce_unit(coordinate, q))
                    for q in divisors(s)
                ),
                start=Fraction(0),
            )
            product = prefix(s, coordinate, "x") * prefix(s, coordinate, "y")
            require(cumulative == product, "cumulative rank-one product failed")
            checks += 1

    for q in divisors(Q):
        for coordinate in units(q):
            reassembled = sum(
                (
                    mobius(q // s)
                    * prefix(s, reduce_unit(coordinate, s), "x")
                    * prefix(s, reduce_unit(coordinate, s), "y")
                    for s in divisors(q)
                ),
                start=Fraction(0),
            )
            require(
                reassembled == unmasked_lcm_fiber(q, coordinate),
                "divisor-lattice Mobius reassembly failed",
            )
            checks += 1

        lifted_mean = sum(
            (
                mobius(q // s) * prefix_product_mean(s)
                for s in divisors(q)
            ),
            start=Fraction(0),
        )
        require(lifted_mean == lcm_mean(q), "mean Mobius lift failed")
        checks += 1
        for coordinate in units(q):
            lifted_center = sum(
                (
                    mobius(q // s)
                    * centered_prefix(s, reduce_unit(coordinate, s))
                    for s in divisors(q)
                ),
                start=Fraction(0),
            )
            require(
                lifted_center == centered_lcm(q, coordinate),
                "centered divisor lift failed",
            )
            checks += 1

        # Exact connected covariance identity.
        lhs = sum(
            (centered_lcm(q, coordinate) ** 2 for coordinate in units(q)),
            start=Fraction(0),
        )
        covariance_sum = Fraction(0)
        for s1 in divisors(q):
            for s2 in divisors(q):
                common_modulus = math.lcm(s1, s2)
                covariance = sum(
                    (
                        centered_prefix(s1, reduce_unit(xi, s1))
                        * centered_prefix(s2, reduce_unit(xi, s2))
                        for xi in units(common_modulus)
                    ),
                    start=Fraction(0),
                ) / euler_phi(common_modulus)
                covariance_sum += (
                    mobius(q // s1) * mobius(q // s2) * covariance
                )
        rhs = euler_phi(q) * covariance_sum
        require(lhs == rhs, "connected divisor covariance failed")
        checks += 1
        records.append(
            {
                "q": q,
                "mean": fraction_record(lcm_mean(q)),
                "centered_energy": fraction_record(lhs),
            }
        )
    return {"layers": records, "digest_sha256": canonical_digest(records)}, checks


def check_additive_divisor_lift() -> Tuple[Dict[str, object], int]:
    require(FIELD_ORDER % Q == 0, "field does not contain q-th roots")
    checks = 0
    direct_values = {
        coordinate: centered_lcm(Q, coordinate) for coordinate in units(Q)
    }
    records: List[Dict[str, int]] = []
    omitted_h_inverse_failures = 0
    for frequency in range(Q):
        direct = additive_transform_fraction(Q, direct_values, frequency)
        without_h_inverse = sum(
            fraction_to_field(direct_values[coordinate])
            * finite_exp(Q, frequency * coordinate)
            for coordinate in units(Q)
        ) % FIELD_PRIME
        if without_h_inverse != direct:
            omitted_h_inverse_failures += 1
        lifted = 0
        signless = 0
        for s in divisors(Q):
            t = Q // s
            prefix_values = {
                coordinate: centered_prefix(s, coordinate)
                for coordinate in units(s)
            }
            argument = 0 if s == 1 else frequency * pow(t, -1, s) % s
            transformed = additive_transform_fraction(s, prefix_values, argument)
            lifted += mobius(t) * ramanujan_sum(t, frequency) * transformed
            signless += transformed
        lifted %= FIELD_PRIME
        signless %= FIELD_PRIME
        require(direct == lifted, "additive CRT divisor lift failed")
        checks += 1
        primitive = math.gcd(frequency, Q) == 1
        if primitive:
            require(direct == signless, "primitive-frequency sign loss failed")
            checks += 1
        records.append(
            {"r": frequency, "transform": direct, "primitive": int(primitive)}
        )
    require(
        omitted_h_inverse_failures > 0,
        "the omitted H-inverse additive phase was not detected",
    )
    checks += 1
    return {
        "field_modulus": FIELD_PRIME,
        "H_inverse_mod_q": pow(H_RADICAL, -1, Q),
        "failures_if_H_inverse_is_omitted": omitted_h_inverse_failures,
        "frequencies": records,
        "primitive_frequency_count": euler_phi(Q),
        "digest_sha256": canonical_digest(records),
    }, checks


def check_multiplicative_parseval() -> Tuple[Dict[str, object], int]:
    checks = 0
    records: List[Dict[str, object]] = []
    for modulus in [10, 15, 30]:
        rational_values = {
            coordinate: centered_lcm(modulus, coordinate)
            for coordinate in units(modulus)
        }
        values = {
            coordinate: fraction_to_field(value)
            for coordinate, value in rational_values.items()
        }
        transforms = {
            character: multiplicative_transform(modulus, values, character)
            for character in all_characters(modulus)
        }
        physical = sum(value * value for value in values.values()) % FIELD_PRIME
        spectral = sum(
            transforms[character]
            * transforms[inverse_character(character, modulus)]
            for character in all_characters(modulus)
        )
        spectral *= pow(euler_phi(modulus), -1, FIELD_PRIME)
        spectral %= FIELD_PRIME
        require(physical == spectral, "multiplicative Parseval failed")
        checks += 1
        principal = tuple(0 for _ in prime_factorization(modulus))
        require(transforms[principal] == 0, "centered principal mode is nonzero")
        checks += 1
        nonprincipal = sum(
            transforms[character]
            * transforms[inverse_character(character, modulus)]
            for character in all_characters(modulus)
            if character != principal
        )
        nonprincipal *= pow(euler_phi(modulus), -1, FIELD_PRIME)
        nonprincipal %= FIELD_PRIME
        require(physical == nonprincipal, "connected Parseval failed")
        checks += 1
        records.append(
            {
                "modulus": modulus,
                "character_count": len(transforms),
                "energy_mod_61": physical,
            }
        )
    return {"cases": records, "digest_sha256": canonical_digest(records)}, checks


def masked_character_sum(
    u: int,
    v: int,
    alpha: Tuple[int, ...],
    beta: Tuple[int, ...],
) -> int:
    total = 0
    for left in ROWS:
        for right in ROWS:
            total += (
                left["x"]
                * right["y"]
                * generic_mask(left, right)
                * character_value(u, alpha, left["m"])
                * character_value(v, beta, right["m"])
            )
    return total % FIELD_PRIME


def check_shared_factor_character_convolution() -> Tuple[Dict[str, object], int]:
    checks = 0
    characters_q = all_characters(Q)
    case_records: List[Dict[str, object]] = []
    total_wrong_phase_failures = 0
    total_omitted_normalization_failures = 0
    total_omitted_left_exclusive_failures = 0
    total_omitted_right_exclusive_failures = 0

    for u, v in SHARED_FACTOR_CASES:
        q = math.lcm(u, v)
        g = math.gcd(u, v)
        a = u // g
        b = v // g
        require(q == Q, "shared-factor case has wrong lcm")
        require(g == G, "shared-factor case has wrong gcd")
        require(
            math.gcd(g, a) == math.gcd(g, b) == math.gcd(a, b) == 1,
            "shared-factor CRT factors are not pairwise coprime",
        )
        characters_g = all_characters(g)
        fiber_fraction = joint_fiber(u, v, generic_mask)
        fiber = {
            coordinate: fraction_to_field(value)
            for coordinate, value in fiber_fraction.items()
        }
        transform_records: List[Dict[str, object]] = []
        nonzero_rhs = 0
        omitted_normalization_failures = 0
        wrong_phase_failures = 0
        omitted_left_exclusive_failures = 0
        omitted_right_exclusive_failures = 0

        # The shared-g projector, including its normalization, for every row pair.
        for left in ROWS:
            for right in ROWS:
                projected = sum(
                    character_value(g, psi, left["m"])
                    * conjugate_character_value(g, psi, right["m"])
                    for psi in characters_g
                )
                projected *= pow(euler_phi(g), -1, FIELD_PRIME)
                projected %= FIELD_PRIME
                expected = int((left["m"] - right["m"]) % g == 0)
                require(projected == expected, "shared-g projector failed")
                checks += 1

        compatible_masked_pairs = 0
        phase_checks = 0
        for left in ROWS:
            for right in ROWS:
                if not generic_mask(left, right):
                    continue
                kappa = joint_kappa(left["m"], right["m"], u, v, H_SHIFT)
                if kappa is None:
                    continue
                compatible_masked_pairs += 1
                for character in characters_q:
                    chi_g = character_restriction(Q, character, g)
                    chi_a = character_restriction(Q, character, a)
                    chi_b = character_restriction(Q, character, b)
                    direct_phase = conjugate_character_value(Q, character, kappa)
                    predicted_phase = (
                        conjugate_character_value(Q, character, -H_SHIFT)
                        * character_value(g, chi_g, left["m"])
                        * character_value(a, chi_a, left["m"])
                        * character_value(b, chi_b, right["m"])
                    ) % FIELD_PRIME
                    require(
                        direct_phase == predicted_phase,
                        "row-character phase failed",
                    )
                    checks += 1
                    phase_checks += 1

        for character in characters_q:
            direct = multiplicative_transform(Q, fiber, character)
            chi_g = character_restriction(Q, character, g)
            chi_a = character_restriction(Q, character, a)
            chi_b = character_restriction(Q, character, b)
            convolution = 0
            convolution_without_left_exclusive = 0
            convolution_without_right_exclusive = 0
            principal_a = tuple(0 for _ in prime_factorization(a))
            principal_b = tuple(0 for _ in prime_factorization(b))
            for psi in characters_g:
                shared_left = multiply_characters(chi_g, psi, g)
                shared_right = inverse_character(psi, g)
                alpha = external_product_character(
                    u,
                    [(g, shared_left), (a, chi_a)],
                )
                beta = external_product_character(
                    v,
                    [(g, shared_right), (b, chi_b)],
                )
                convolution += masked_character_sum(u, v, alpha, beta)
                alpha_without_left = external_product_character(
                    u,
                    [(g, shared_left), (a, principal_a)],
                )
                beta_without_right = external_product_character(
                    v,
                    [(g, shared_right), (b, principal_b)],
                )
                convolution_without_left_exclusive += masked_character_sum(
                    u, v, alpha_without_left, beta
                )
                convolution_without_right_exclusive += masked_character_sum(
                    u, v, alpha, beta_without_right
                )
            convolution %= FIELD_PRIME
            convolution_without_left_exclusive %= FIELD_PRIME
            convolution_without_right_exclusive %= FIELD_PRIME
            phase_and_normalization = (
                conjugate_character_value(Q, character, -H_SHIFT)
                * pow(euler_phi(g), -1, FIELD_PRIME)
            ) % FIELD_PRIME
            predicted = (
                phase_and_normalization * convolution
            ) % FIELD_PRIME
            require(direct == predicted, "masked shared-g convolution failed")
            checks += 1

            if (
                phase_and_normalization * convolution_without_left_exclusive
                % FIELD_PRIME
                != direct
            ):
                omitted_left_exclusive_failures += 1
            if (
                phase_and_normalization * convolution_without_right_exclusive
                % FIELD_PRIME
                != direct
            ):
                omitted_right_exclusive_failures += 1

            wrong_phase = (
                character_value(Q, character, -H_SHIFT)
                * pow(euler_phi(g), -1, FIELD_PRIME)
                * convolution
            ) % FIELD_PRIME
            if wrong_phase != direct:
                wrong_phase_failures += 1

            if predicted:
                nonzero_rhs += 1
                without_normalization = (
                    conjugate_character_value(Q, character, -H_SHIFT)
                    * convolution
                ) % FIELD_PRIME
                require(
                    without_normalization != direct,
                    "the 1/phi(g) normalization was accidentally dispensable",
                )
                checks += 1
                omitted_normalization_failures += 1
            transform_records.append(
                {"character": list(character), "transform_mod_61": direct}
            )

        require(compatible_masked_pairs > 0, "generic mask has no compatible pairs")
        require(nonzero_rhs > 0, "generic transform is accidentally zero")
        require(
            wrong_phase_failures > 0,
            "the missing conjugation in the global phase was not detected",
        )
        require(
            omitted_normalization_failures > 0,
            "the omitted shared-factor normalization was not detected",
        )
        if euler_phi(a) > 1:
            require(
                omitted_left_exclusive_failures > 0,
                "the omitted left-exclusive character was not detected",
            )
            checks += 1
        if euler_phi(b) > 1:
            require(
                omitted_right_exclusive_failures > 0,
                "the omitted right-exclusive character was not detected",
            )
            checks += 1
        checks += 4
        total_wrong_phase_failures += wrong_phase_failures
        total_omitted_normalization_failures += omitted_normalization_failures
        total_omitted_left_exclusive_failures += omitted_left_exclusive_failures
        total_omitted_right_exclusive_failures += omitted_right_exclusive_failures
        case_records.append(
            {
                "q": q,
                "u": u,
                "v": v,
                "g": g,
                "a": a,
                "b": b,
                "normalization": fraction_record(Fraction(1, euler_phi(g))),
                "compatible_masked_pairs": compatible_masked_pairs,
                "row_phase_checks": phase_checks,
                "nonzero_character_transforms": nonzero_rhs,
                "failures_if_phase_conjugation_is_omitted": wrong_phase_failures,
                "failures_if_one_over_phi_g_is_omitted": omitted_normalization_failures,
                "failures_if_left_exclusive_character_is_omitted": (
                    omitted_left_exclusive_failures
                ),
                "failures_if_right_exclusive_character_is_omitted": (
                    omitted_right_exclusive_failures
                ),
                "transforms": transform_records,
                "digest_sha256": canonical_digest(transform_records),
            }
        )

    return {
        "cases": case_records,
        "total_failures_if_phase_conjugation_is_omitted": total_wrong_phase_failures,
        "total_failures_if_one_over_phi_g_is_omitted": (
            total_omitted_normalization_failures
        ),
        "total_failures_if_left_exclusive_character_is_omitted": (
            total_omitted_left_exclusive_failures
        ),
        "total_failures_if_right_exclusive_character_is_omitted": (
            total_omitted_right_exclusive_failures
        ),
        "digest_sha256": canonical_digest(case_records),
    }, checks


def check_gauss_conductor_formula() -> Tuple[Dict[str, object], int]:
    checks = 0
    records: List[Dict[str, object]] = []
    conductor_counts: Dict[int, int] = {}
    gauss_table: Dict[Tuple[Tuple[int, ...], int], int] = {}
    for character in all_characters(Q):
        conductor, primitive_character = induced_primitive_character(Q, character)
        conductor_counts[conductor] = conductor_counts.get(conductor, 0) + 1
        d = Q // conductor
        tau = primitive_gauss_sum(conductor, primitive_character)
        for frequency in range(Q):
            direct = gauss_sum(Q, character, frequency)
            if math.gcd(frequency, conductor) > 1:
                predicted = 0
            else:
                predicted = (
                    conjugate_character_value(
                        conductor, primitive_character, frequency
                    )
                    * character_value(conductor, primitive_character, d)
                    * tau
                    * ramanujan_sum(d, frequency)
                ) % FIELD_PRIME
            require(direct == predicted, "induced-character Gauss formula failed")
            checks += 1
            gauss_table[(character, frequency)] = direct
        records.append(
            {"character": list(character), "conductor": conductor, "tau_mod_61": tau}
        )

    conductor_mass = sum(
        character_conductor(Q, character) for character in all_characters(Q)
    )
    require(conductor_mass == euler_phi(Q) ** 2, "conductor mass failed")
    checks += 1

    # Exact paired form of sum_chi |G(chi;t)|^2 = phi(q)^2.
    for frequency in range(Q):
        energy = sum(
            gauss_table[(character, frequency)]
            * gauss_table[(inverse_character(character, Q), (-frequency) % Q)]
            for character in all_characters(Q)
        ) % FIELD_PRIME
        require(
            energy == euler_phi(Q) ** 2 % FIELD_PRIME,
            "Gauss character Parseval failed",
        )
        checks += 1

    return {
        "character_count": len(all_characters(Q)),
        "frequency_count": Q,
        "conductor_counts": {str(k): conductor_counts[k] for k in sorted(conductor_counts)},
        "conductor_mass": conductor_mass,
        "characters": records,
        "digest_sha256": canonical_digest(records),
    }, checks


def check_additive_character_bridge() -> Tuple[Dict[str, object], int]:
    checks = 0
    fiber_fraction = joint_fiber(U, V, generic_mask)
    fiber = {
        coordinate: fraction_to_field(value)
        for coordinate, value in fiber_fraction.items()
    }
    transforms = {
        character: multiplicative_transform(Q, fiber, character)
        for character in all_characters(Q)
    }
    records: List[Dict[str, int]] = []
    h_inverse = pow(H_RADICAL, -1, Q)
    for frequency in range(Q):
        effective_frequency = frequency * h_inverse % Q
        direct = sum(
            fiber[kappa] * finite_exp(Q, effective_frequency * kappa)
            for kappa in units(Q)
        ) % FIELD_PRIME
        lifted = sum(
            transforms[character] * gauss_sum(Q, character, effective_frequency)
            for character in all_characters(Q)
        )
        lifted *= pow(euler_phi(Q), -1, FIELD_PRIME)
        lifted %= FIELD_PRIME
        require(direct == lifted, "additive/multiplicative character bridge failed")
        checks += 1
        records.append(
            {
                "r": frequency,
                "r_times_H_inverse_mod_q": effective_frequency,
                "value_mod_61": direct,
            }
        )
    return {"frequencies": records, "digest_sha256": canonical_digest(records)}, checks


def check_row_diagonal_spike() -> Tuple[Dict[str, object], int]:
    checks = 0
    row = ROWS[0]
    gamma = sum(
        (
            THETA[u] * THETA[v]
            for u in divisors(Q)
            for v in divisors(Q)
            if math.lcm(u, v) == Q
        ),
        start=Fraction(0),
    )
    prefix_gamma = sum(
        (
            mobius(Q // s)
            * sum((THETA[u] for u in divisors(s)), start=Fraction(0)) ** 2
            for s in divisors(Q)
        ),
        start=Fraction(0),
    )
    require(gamma == prefix_gamma, "row-diagonal Gamma prefix formula failed")
    checks += 1
    amplitude = Fraction(row["x"] ** 2) * gamma
    require(amplitude != 0, "row-diagonal amplitude vanished")
    checks += 1
    kappa0 = (-H_SHIFT * pow(row["m"], -1, Q)) % Q
    require(kappa0 in units(Q), "row-diagonal class is not a unit")
    checks += 1
    spike = {
        kappa: amplitude if kappa == kappa0 else Fraction(0)
        for kappa in units(Q)
    }
    mean = amplitude / euler_phi(Q)
    centered = {kappa: value - mean for kappa, value in spike.items()}
    energy = sum((value * value for value in centered.values()), start=Fraction(0))
    predicted_energy = amplitude * amplitude * (1 - Fraction(1, euler_phi(Q)))
    require(energy == predicted_energy, "row-diagonal spike energy failed")
    checks += 1

    centered_field = {
        kappa: fraction_to_field(value) for kappa, value in centered.items()
    }
    amplitude_field = fraction_to_field(amplitude)
    for character in all_characters(Q):
        principal = all(index == 0 for index in character)
        transform = multiplicative_transform(Q, centered_field, character)
        if principal:
            require(transform == 0, "spike principal character did not vanish")
        else:
            inverse = inverse_character(character, Q)
            inverse_transform = multiplicative_transform(Q, centered_field, inverse)
            require(
                transform * inverse_transform % FIELD_PRIME
                == amplitude_field * amplitude_field % FIELD_PRIME,
                "spike nonprincipal character magnitude failed",
            )
        checks += 1

    for frequency in range(Q):
        direct = additive_transform_fraction(Q, centered, frequency)
        h_inverse = pow(H_RADICAL, -1, Q)
        predicted = amplitude_field * (
            finite_exp(Q, frequency * h_inverse * kappa0)
            - ramanujan_sum(Q, frequency)
            * pow(euler_phi(Q), -1, FIELD_PRIME)
        )
        predicted %= FIELD_PRIME
        require(direct == predicted, "row-diagonal additive spike failed")
        checks += 1

    return {
        "row_m": row["m"],
        "kappa0": kappa0,
        "gamma": fraction_record(gamma),
        "amplitude": fraction_record(amplitude),
        "mean": fraction_record(mean),
        "centered_energy": fraction_record(energy),
    }, checks


def check_gain_ledger() -> Tuple[Dict[str, object], int]:
    checks = 0
    records: List[Dict[str, object]] = []
    profiles = {
        "published": Fraction(10, 21),
        "li_v6": Fraction(8, 17),
    }
    samples = [
        (Fraction(1, 7), Fraction(1, 1000)),
        (Fraction(3, 20), Fraction(1, 500)),
        (Fraction(4, 25), Fraction(1, 200)),
    ]
    for profile_name, lambda_base in profiles.items():
        for delta, sigma0 in samples:
            lambda_value = lambda_base - sigma0
            beta = lambda_value + Fraction(1, 4) - delta / 2
            j = 1 - beta
            y = 1 - 2 * delta
            general = (y - j) / 2
            maximal = (beta - 2 * delta) / 2
            profile = lambda_value / 2 + Fraction(1, 8) - 5 * delta / 4
            require(general == maximal == profile, "gain ledger equivalence failed")
            checks += 2
            if profile_name == "published":
                displayed = Fraction(61, 168) - sigma0 / 2 - 5 * delta / 4
            else:
                displayed = Fraction(49, 136) - sigma0 / 2 - 5 * delta / 4
            require(profile == displayed, "profile gain ledger failed")
            checks += 1
            omega = profile + Fraction(1, 100)
            remaining_exponent = (y - j) / 2 - omega
            require(remaining_exponent == Fraction(-1, 100), "gain margin failed")
            checks += 1
            records.append(
                {
                    "profile": profile_name,
                    "delta": fraction_record(delta),
                    "sigma0": fraction_record(sigma0),
                    "beta": fraction_record(beta),
                    "j": fraction_record(j),
                    "y": fraction_record(y),
                    "required_omega": fraction_record(profile),
                    "tested_margin": fraction_record(Fraction(1, 100)),
                }
            )
    return {"cases": records, "digest_sha256": canonical_digest(records)}, checks


def main() -> None:
    require(Q == math.lcm(U, V), "global lcm parameters are inconsistent")
    require(G == math.gcd(U, V), "global gcd parameters are inconsistent")
    require(all(math.gcd(row["m"], Q) == 1 for row in ROWS), "nonunit row")
    require(math.gcd(H_SHIFT, Q) == 1, "shift is not a unit modulo q")
    require(math.gcd(H_RADICAL, Q) == 1, "H is not a unit modulo q")
    require(H_SHIFT == H_RADICAL, "finite test expects H to equal the prime shift")
    require(
        all(math.gcd(H_SHIFT, row["m"]) == 1 for row in ROWS),
        "shift is not coprime to every test row",
    )
    require(all(row["ell"] * row["d"] == row["m"] for row in ROWS), "bad row label")
    require(all(is_squarefree(d) for d in THETA), "theta support is not squarefree")
    require(set(THETA) == set(divisors(Q)), "theta test support is incomplete")
    require(FIELD_ORDER % Q == 0, "finite field lacks additive roots")

    compatible, compatible_checks = check_compatible_fibers()
    occupancy, occupancy_checks = check_lcm_occupancy_product()
    reassembly, reassembly_checks = check_divisor_reassembly()
    additive, additive_checks = check_additive_divisor_lift()
    parseval, parseval_checks = check_multiplicative_parseval()
    convolution, convolution_checks = check_shared_factor_character_convolution()
    gauss, gauss_checks = check_gauss_conductor_formula()
    bridge, bridge_checks = check_additive_character_bridge()
    spike, spike_checks = check_row_diagonal_spike()
    ledger, ledger_checks = check_gain_ledger()

    source_path = Path(__file__).resolve()
    input_summary = {
        "q": Q,
        "u": U,
        "v": V,
        "g": G,
        "shift_h": H_SHIFT,
        "radical_H": H_RADICAL,
        "H_inverse_mod_q": pow(H_RADICAL, -1, Q),
        "shared_factor_cases": [
            {"u": u, "v": v, "g": math.gcd(u, v), "q": math.lcm(u, v)}
            for u, v in SHARED_FACTOR_CASES
        ],
        "rows": ROWS,
        "theta": {str(key): fraction_record(THETA[key]) for key in sorted(THETA)},
        "generic_mask": {
            "different_ell": True,
            "absolute_row_gap_strictly_greater_than": 70,
            "d_gcd_at_most": 1,
        },
        "finite_field": {
            "prime": FIELD_PRIME,
            "generator": FIELD_GENERATOR,
            "supported_root_orders": [1, 2, 3, 4, 5, 6, 10, 15, 30],
        },
    }
    input_summary["digest_sha256"] = canonical_digest(input_summary)

    coverage = {
        "compatible_fiber_equalities": compatible_checks,
        "squarefree_lcm_product_equalities": occupancy_checks,
        "divisor_reassembly_and_covariance_equalities": reassembly_checks,
        "additive_crt_and_primitive_sign_equalities": additive_checks,
        "multiplicative_parseval_equalities": parseval_checks,
        "shared_g_projector_phase_and_convolution_equalities": convolution_checks,
        "induced_gauss_and_conductor_equalities": gauss_checks,
        "additive_character_bridge_equalities": bridge_checks,
        "row_diagonal_spike_equalities": spike_checks,
        "rational_gain_ledger_equalities": ledger_checks,
    }
    coverage["total_exact_equalities"] = sum(coverage.values())

    report = {
        "certificate": "TPC-21 connected fiber energy exact finite certificate",
        "schema_version": 1,
        "status": "pass",
        "deterministic": True,
        "optimized_mode_safe": True,
        "arithmetic_backends": [
            "integers",
            "fractions.Fraction",
            "exact roots of unity in F_61",
        ],
        "input_summary": input_summary,
        "coverage": coverage,
        "results": {
            "compatible_fiber_total_and_mean": compatible,
            "squarefree_lcm_occupancy_product": occupancy,
            "divisor_lattice_reassembly": reassembly,
            "additive_crt_divisor_lift": additive,
            "multiplicative_character_parseval": parseval,
            "generic_mask_shared_g_convolution": convolution,
            "induced_character_gauss_formula": gauss,
            "additive_character_bridge": bridge,
            "row_diagonal_one_fiber_spike": spike,
            "rational_gain_ledger": ledger,
        },
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "evidence_flags": {
            "twin_prime_evidence": False,
            "residual_dispersion_evidence": False,
            "parity_breakthrough_evidence": False,
            "asymptotic_evidence": False,
        },
        "scope_note": (
            "Exact finite algebra only; no asymptotic, residual-dispersion, "
            "twin-prime, or parity-barrier claim."
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
                "certificate_digest_sha256": report["certificate_digest_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
