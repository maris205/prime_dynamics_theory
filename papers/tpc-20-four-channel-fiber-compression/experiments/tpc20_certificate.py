"""Exact deterministic certificate for the TPC-20 finite algebra.

Every proof check uses integers, fractions, formal prime-log polynomials,
or finite fields with exact roots of unity.  The small displayed magnitude
samples are explicitly diagnostic.  They are not evidence for asymptotics,
residual dispersion, prime pairs, or the twin-prime conjecture.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


Monomial = Tuple[int, ...]
Polynomial = Dict[Monomial, Fraction]
LinearForm = Dict[str, Fraction]


def require(condition: bool, message: str) -> None:
    """Raise in ordinary and optimized Python alike."""

    if not condition:
        raise RuntimeError(message)


def prime_factorization(n: int) -> Dict[int, int]:
    require(n >= 1, "factorization requires a positive integer")
    factors: Dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisors(n: int) -> List[int]:
    answer = [1]
    for prime, exponent in prime_factorization(n).items():
        answer = [
            divisor * prime**power
            for divisor in answer
            for power in range(exponent + 1)
        ]
    return sorted(answer)


def mobius(n: int) -> int:
    factors = prime_factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def euler_phi(n: int) -> int:
    answer = n
    for prime in prime_factorization(n):
        answer -= answer // prime
    return answer


def radical(n: int) -> int:
    return math.prod(prime_factorization(n))


def ramanujan_sum(q: int, n: int) -> int:
    return sum(d * mobius(q // d) for d in divisors(math.gcd(q, n)))


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


def fraction_record(value: Fraction) -> dict:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def normalize_polynomial(polynomial: Polynomial) -> Polynomial:
    return {
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if coefficient
    }


def constant_polynomial(value: Fraction | int) -> Polynomial:
    value = Fraction(value)
    return {} if not value else {(): value}


def add_polynomials(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
    return normalize_polynomial(answer)


def scale_polynomial(
    polynomial: Polynomial, scalar: Fraction | int
) -> Polynomial:
    scalar = Fraction(scalar)
    return normalize_polynomial(
        {monomial: scalar * coefficient for monomial, coefficient in polynomial.items()}
    )


def multiply_polynomials(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            answer[monomial] = (
                answer.get(monomial, Fraction(0))
                + coefficient_left * coefficient_right
            )
    return normalize_polynomial(answer)


def subtract_polynomials(left: Polynomial, right: Polynomial) -> Polynomial:
    return add_polynomials(left, scale_polynomial(right, -1))


def log_integer_polynomial(n: int) -> Polynomial:
    return {
        (prime,): Fraction(exponent)
        for prime, exponent in prime_factorization(n).items()
    }


def formal_von_mangoldt(n: int) -> Polynomial:
    if n < 2:
        return {}
    factors = prime_factorization(n)
    if len(factors) != 1:
        return {}
    prime = next(iter(factors))
    return {(prime,): Fraction(1)}


def a_polynomial(u: int) -> Polynomial:
    return scale_polynomial(log_integer_polynomial(u), -mobius(u))


def monomial_label(monomial: Monomial) -> str:
    if not monomial:
        return "1"
    return "*".join(f"log({prime})" for prime in monomial)


def polynomial_record(polynomial: Polynomial) -> dict:
    return {
        monomial_label(monomial): fraction_record(coefficient)
        for monomial, coefficient in sorted(
            normalize_polynomial(polynomial).items(),
            key=lambda item: (len(item[0]), item[0]),
        )
    }


def polynomial_digest(polynomial: Polynomial) -> str:
    return canonical_digest(polynomial_record(polynomial))


def evaluate_polynomial(polynomial: Polynomial) -> float:
    total = 0.0
    for monomial, coefficient in polynomial.items():
        value = float(coefficient)
        for prime in monomial:
            value *= math.log(prime)
        total += value
    return total


@lru_cache(maxsize=None)
def lambda_prime(r_cutoff: int, u: int) -> Fraction:
    if u > r_cutoff:
        return Fraction(0)
    return Fraction(u) * sum(
        (
            Fraction(mobius(u * b) * mobius(b), euler_phi(u * b))
            for b in range(1, r_cutoff // u + 1)
        ),
        start=Fraction(0),
    )


def lambda_model_value(r_cutoff: int, n: int) -> Fraction:
    return sum(
        (lambda_prime(r_cutoff, u) for u in divisors(n)),
        start=Fraction(0),
    )


def b_polynomial(r_cutoff: int, u: int) -> Polynomial:
    return add_polynomials(
        a_polynomial(u), constant_polynomial(-lambda_prime(r_cutoff, u))
    )


def crt_two(
    residue_1: int, modulus_1: int, residue_2: int, modulus_2: int
) -> Tuple[int, int] | None:
    common = math.gcd(modulus_1, modulus_2)
    if (residue_2 - residue_1) % common:
        return None
    reduced_2 = modulus_2 // common
    if reduced_2 == 1:
        multiplier = 0
    else:
        multiplier = (
            (residue_2 - residue_1)
            // common
            * pow(modulus_1 // common, -1, reduced_2)
        ) % reduced_2
    modulus = math.lcm(modulus_1, modulus_2)
    return (residue_1 + modulus_1 * multiplier) % modulus, modulus


def inverse_or_zero(value: int, modulus: int) -> int:
    return 0 if modulus == 1 else pow(value, -1, modulus)


def primitive_root(prime: int) -> int:
    require(is_prime(prime), "finite-field modulus is not prime")
    factors = list(prime_factorization(prime - 1))
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise RuntimeError("primitive root not found")


def exact_root(prime: int, order: int) -> Tuple[int, int]:
    require((prime - 1) % order == 0, "root order does not divide p-1")
    generator = primitive_root(prime)
    root = pow(generator, (prime - 1) // order, prime)
    require(pow(root, order, prime) == 1, "candidate root has wrong order")
    for factor in prime_factorization(order):
        require(
            pow(root, order // factor, prime) != 1,
            "candidate root has a proper suborder",
        )
    return generator, root


def fraction_mod(value: Fraction | int, prime: int) -> int:
    value = Fraction(value)
    require(value.denominator % prime, "fraction denominator vanishes in field")
    return (
        value.numerator % prime * pow(value.denominator, -1, prime)
    ) % prime


def root_character(
    root_of_order_t: int, total_order: int, modulus: int, exponent: int, prime: int
) -> int:
    if modulus == 1:
        return 1
    require(total_order % modulus == 0, "character modulus does not divide order")
    return pow(
        root_of_order_t,
        (total_order // modulus) * (exponent % modulus),
        prime,
    )


def kernel_case_data(case: Mapping[str, int]) -> dict:
    h = case["h"]
    H = case["H"]
    u = case["u"]
    v = case["v"]
    m_1 = case["m_1"]
    m_2 = case["m_2"]
    field_prime = case["field_prime"]
    require(H == radical(abs(h)), "H must equal rad(|h|)")
    require(math.gcd(u, m_1 * H) == 1, "first modulus is not primitive")
    require(math.gcd(v, m_2 * H) == 1, "second modulus is not primitive")
    common = math.gcd(u, v)
    a_value = u // common
    b_value = v // common
    q = math.lcm(u, v)
    period = H * q
    compatible = (m_1 - m_2) % common == 0
    kappa_1 = 0 if u == 1 else (-h * pow(m_1, -1, u)) % u
    kappa_2 = 0 if v == 1 else (-h * pow(m_2, -1, v)) % v
    crt = crt_two(kappa_1, u, kappa_2, v)
    require((crt is not None) == compatible, "CRT compatibility mismatch")
    kappa = None if crt is None else crt[0]

    kernel: List[Fraction] = []
    for x in range(period):
        mask = int(math.gcd(x, H) == 1)
        first = Fraction(int((m_1 * x + h) % u == 0), 1) - Fraction(1, u)
        second = Fraction(int((m_2 * x + h) % v == 0), 1) - Fraction(1, v)
        kernel.append(mask * first * second)

    zero_direct = sum(kernel, start=Fraction(0)) / period
    zero_formula = Fraction(
        euler_phi(H) * (common * int(compatible) - 1), H * u * v
    )
    require(zero_direct == zero_formula, "primitive zero mode failed")

    energy_direct = sum((value * value for value in kernel), start=Fraction(0)) / period
    energy_formula = Fraction(euler_phi(H), H) * (
        Fraction((u - 1) * (v - 1), u * u * v * v)
        + Fraction(common * int(compatible) - 1, u * v)
        * Fraction(u - 2, u)
        * Fraction(v - 2, v)
    )
    require(energy_direct == energy_formula, "rational kernel Plancherel failed")

    generator, root = exact_root(field_prime, period)
    direct_dft: List[int] = []
    formula_dft: List[int] = []
    common_dft: List[int] = []
    inverse_period = pow(period, -1, field_prime)
    inverse_h_q = inverse_or_zero(H, q)
    inverse_h_u = inverse_or_zero(H, u)
    inverse_h_v = inverse_or_zero(H, v)
    for r in range(period):
        direct = sum(
            fraction_mod(value, field_prime)
            * pow(root, (-r * x) % period, field_prime)
            for x, value in enumerate(kernel)
        )
        direct %= field_prime
        direct = direct * inverse_period % field_prime
        direct_dft.append(direct)

        bracket = 0
        if compatible:
            require(kappa is not None, "missing compatible joint class")
            bracket += common * root_character(
                root,
                period,
                q,
                -r * inverse_h_q * kappa,
                field_prime,
            )
        if r % b_value == 0:
            bracket -= root_character(
                root,
                period,
                u,
                -(r // b_value) * inverse_h_u * kappa_1,
                field_prime,
            )
        if r % a_value == 0:
            bracket -= root_character(
                root,
                period,
                v,
                -(r // a_value) * inverse_h_v * kappa_2,
                field_prime,
            )
        if r % q == 0:
            bracket += 1
        formula = (
            ramanujan_sum(H, r)
            * fraction_mod(Fraction(1, H * u * v), field_prime)
            * bracket
        ) % field_prime
        formula_dft.append(formula)
        require(direct == formula, "full finite-field DFT coefficient failed")

        if compatible:
            multiplier = (
                common
                - int(r % b_value == 0)
                - int(r % a_value == 0)
                + int(r % q == 0)
            )
            common_formula = (
                ramanujan_sum(H, r)
                * fraction_mod(Fraction(1, H * u * v), field_prime)
                * root_character(
                    root,
                    period,
                    q,
                    -r * inverse_h_q * int(kappa),
                    field_prime,
                )
                * multiplier
            ) % field_prime
            common_dft.append(common_formula)
            require(
                common_formula == formula,
                "compatible common multiplier failed",
            )

    field_parseval = sum(
        direct_dft[r] * direct_dft[(-r) % period] for r in range(period)
    ) % field_prime
    require(
        field_parseval == fraction_mod(energy_direct, field_prime),
        "finite-field kernel Parseval failed",
    )

    multiplier_record = None
    if compatible:
        multipliers = [
            common
            - int(r % b_value == 0)
            - int(r % a_value == 0)
            + int(r % q == 0)
            for r in range(q)
        ]
        full_count = sum(value == common for value in multipliers)
        square_energy = sum(value * value for value in multipliers)
        expected_count = q - u - v + common
        expected_energy = (
            q * common * common
            + (1 - 2 * common) * (u + v)
            + 4 * common
            - 3
        )
        require(all(0 <= value <= common for value in multipliers), "B range failed")
        require(full_count == expected_count, "B full-value count failed")
        require(square_energy == expected_energy, "B energy failed")
        multiplier_record = {
            "value_range": [min(multipliers), max(multipliers)],
            "full_value_count": full_count,
            "expected_full_value_count": expected_count,
            "square_energy": square_energy,
            "expected_square_energy": expected_energy,
            "multiplier_sha256": canonical_digest(multipliers),
            "all_checks_hold": True,
        }

    return {
        "name": case["name"],
        "h": h,
        "H": H,
        "u": u,
        "v": v,
        "g": common,
        "a": a_value,
        "b": b_value,
        "q_lcm": q,
        "period": period,
        "m_1": m_1,
        "m_2": m_2,
        "compatible": compatible,
        "kappa_1": kappa_1,
        "kappa_2": kappa_2,
        "kappa": kappa,
        "zero_mode_direct": fraction_record(zero_direct),
        "zero_mode_formula": fraction_record(zero_formula),
        "energy_direct": fraction_record(energy_direct),
        "energy_formula": fraction_record(energy_formula),
        "finite_field": {
            "prime": field_prime,
            "primitive_generator": generator,
            "root_order": period,
            "root": root,
            "exact_order_verified": True,
        },
        "DFT_coefficient_count": period,
        "DFT_failure_count": 0,
        "DFT_sha256": canonical_digest(direct_dft),
        "formula_DFT_sha256": canonical_digest(formula_dft),
        "field_parseval_holds": True,
        "compatible_multiplier": multiplier_record,
        "all_checks_hold": True,
    }


def kernel_dft_certificate() -> dict:
    cases = [
        {
            "name": "coprime-compatible-F61",
            "h": 2,
            "H": 2,
            "u": 3,
            "v": 5,
            "m_1": 7,
            "m_2": 11,
            "field_prime": 61,
        },
        {
            "name": "shared-content-compatible-F421",
            "h": 2,
            "H": 2,
            "u": 15,
            "v": 21,
            "m_1": 11,
            "m_2": 17,
            "field_prime": 421,
        },
        {
            "name": "shared-content-incompatible-F421",
            "h": 2,
            "H": 2,
            "u": 15,
            "v": 21,
            "m_1": 11,
            "m_2": 19,
            "field_prime": 421,
        },
        {
            "name": "nontrivial-primitive-mask-F421",
            "h": 6,
            "H": 6,
            "u": 5,
            "v": 7,
            "m_1": 11,
            "m_2": 13,
            "field_prime": 421,
        },
    ]
    records = [kernel_case_data(case) for case in cases]
    fields = sorted({record["finite_field"]["prime"] for record in records})
    require(len(fields) >= 2, "DFT checks did not use two finite fields")
    return {
        "method": "exact roots of unity in finite prime fields",
        "finite_fields": fields,
        "case_count": len(records),
        "cases": records,
        "all_DFT_zero_mode_multiplier_and_Plancherel_checks_hold": True,
    }


def row_formal_components(
    r_cutoff: int,
    h: int,
    H: int,
    horizon: int,
    ell: int,
    d: int,
    j: int,
) -> dict:
    m = ell * d
    target = m * j + h
    require(target <= horizon, "target exceeds formal horizon")
    require(math.gcd(target, m * H) == 1, "target is not primitive")
    require(ell > r_cutoff and is_prime(ell), "invalid source prime")
    require(mobius(d) != 0 and math.gcd(d, H) == 1, "invalid divisor row")
    rho_prime = Fraction(H, euler_phi(H)) * Fraction(m, euler_phi(m))
    rho_model = Fraction(H, euler_phi(H)) * Fraction(d, euler_phi(d))
    eligible_r = [
        u
        for u in range(1, r_cutoff + 1)
        if math.gcd(u, m * H) == 1
    ]
    calibrated_model_sum = sum(
        (lambda_prime(r_cutoff, u) / u for u in eligible_r),
        start=Fraction(0),
    )
    require(
        calibrated_model_sum == rho_model,
        "finite-model calibration sum failed",
    )

    prime_signal = add_polynomials(
        formal_von_mangoldt(target), constant_polynomial(-rho_prime)
    )
    model_signal = constant_polynomial(
        lambda_model_value(r_cutoff, target) - rho_model
    )
    common_signal = subtract_polynomials(prime_signal, model_signal)

    epsilon = constant_polynomial(-rho_prime)
    terms: List[Tuple[int, Polynomial]] = []
    divisor_von_mangoldt: Polynomial = {}
    for u in range(1, horizon + 1):
        if math.gcd(u, m * H) != 1:
            continue
        coefficient_a = a_polynomial(u)
        epsilon = add_polynomials(
            epsilon, scale_polynomial(coefficient_a, Fraction(1, u))
        )
        if target % u == 0:
            divisor_von_mangoldt = add_polynomials(
                divisor_von_mangoldt, coefficient_a
            )
        centered = Fraction(int(target % u == 0), 1) - Fraction(1, u)
        coefficient_b = b_polynomial(r_cutoff, u)
        if coefficient_b and centered:
            terms.append((u, scale_polynomial(coefficient_b, centered)))

    require(
        divisor_von_mangoldt == formal_von_mangoldt(target),
        "formal von Mangoldt divisor identity failed",
    )
    centered_sum = add_polynomials(*(polynomial for _, polynomial in terms))
    recombined = add_polynomials(epsilon, centered_sum)
    require(recombined == common_signal, "pointwise common recombination failed")
    return {
        "P": prime_signal,
        "M": model_signal,
        "Z": common_signal,
        "epsilon": epsilon,
        "centered_terms": terms,
        "centered_sum": centered_sum,
        "target": target,
        "m": m,
        "rho_prime": rho_prime,
        "rho_model": rho_model,
    }


def formal_recombination_certificate() -> dict:
    r_cutoff = 10
    h = 2
    H = 2
    horizon = 200
    row_1 = (11, 3)
    row_2 = (13, 3)
    j_values = [1, 3, 5]
    records = []
    for j in j_values:
        first = row_formal_components(
            r_cutoff, h, H, horizon, row_1[0], row_1[1], j
        )
        second = row_formal_components(
            r_cutoff, h, H, horizon, row_2[0], row_2[1], j
        )
        direct_product = multiply_polynomials(first["Z"], second["Z"])
        raw_four_channels = add_polynomials(
            multiply_polynomials(first["P"], second["P"]),
            scale_polynomial(multiply_polynomials(first["P"], second["M"]), -1),
            scale_polynomial(multiply_polynomials(first["M"], second["P"]), -1),
            multiply_polynomials(first["M"], second["M"]),
        )

        epsilon_epsilon = multiply_polynomials(
            first["epsilon"], second["epsilon"]
        )
        epsilon_first = multiply_polynomials(
            first["epsilon"], second["centered_sum"]
        )
        epsilon_second = multiply_polynomials(
            second["epsilon"], first["centered_sum"]
        )
        double_channel: Polynomial = {}
        for _, first_term in first["centered_terms"]:
            for _, second_term in second["centered_terms"]:
                double_channel = add_polynomials(
                    double_channel,
                    multiply_polynomials(first_term, second_term),
                )
        common_four_channels = add_polynomials(
            epsilon_epsilon,
            epsilon_first,
            epsilon_second,
            double_channel,
        )
        require(
            direct_product == raw_four_channels == common_four_channels,
            "formal four-channel product recombination failed",
        )
        records.append(
            {
                "j": j,
                "targets": [first["target"], second["target"]],
                "first_centered_term_count": len(first["centered_terms"]),
                "second_centered_term_count": len(second["centered_terms"]),
                "common_product_term_count": len(direct_product),
                "common_product_sha256": polynomial_digest(direct_product),
                "raw_four_channel_sha256": polynomial_digest(raw_four_channels),
                "recombined_four_channel_sha256": polynomial_digest(
                    common_four_channels
                ),
                "identity_holds": True,
            }
        )
    return {
        "arithmetic": "Fraction coefficients and formal prime-log polynomials",
        "R": r_cutoff,
        "h": h,
        "H": H,
        "horizon": horizon,
        "rows": [
            {"ell": row_1[0], "d": row_1[1]},
            {"ell": row_2[0], "d": row_2[1]},
        ],
        "pointwise_cases": records,
        "pointwise_case_count": len(records),
        "all_common_recombination_checks_hold": True,
    }


@lru_cache(maxsize=None)
def calibration_A(x: int) -> Tuple[Tuple[Monomial, Fraction], ...]:
    polynomial: Polynomial = {}
    for n in range(1, x + 1):
        polynomial = add_polynomials(
            polynomial,
            scale_polynomial(log_integer_polynomial(n), Fraction(-mobius(n), n)),
        )
    return tuple(sorted(polynomial.items()))


@lru_cache(maxsize=None)
def calibration_B(x: int) -> Fraction:
    return sum((Fraction(mobius(n), n) for n in range(1, x + 1)), Fraction(0))


def polynomial_from_tuple(
    entries: Tuple[Tuple[Monomial, Fraction], ...]
) -> Polynomial:
    return dict(entries)


def supported_on_M(k: int, M: int) -> bool:
    return all(prime in prime_factorization(M) for prime in prime_factorization(k))


def calibration_convolution_certificate() -> dict:
    cases = [(20, 1), (30, 6), (45, 10), (60, 30), (75, 42)]
    records = []
    total_convolution_tests = 0
    for horizon, M in cases:
        failure_count = 0
        for n in range(1, horizon + 1):
            convolution = sum(
                mobius(d) * int(supported_on_M(n // d, M))
                for d in divisors(n)
            )
            expected = mobius(n) * int(math.gcd(n, M) == 1)
            failure_count += int(convolution != expected)
            total_convolution_tests += 1
        require(failure_count == 0, "coprime Mobius convolution failed")

        direct: Polynomial = {}
        for n in range(1, horizon + 1):
            if math.gcd(n, M) == 1:
                direct = add_polynomials(
                    direct,
                    scale_polynomial(
                        log_integer_polynomial(n), Fraction(-mobius(n), n)
                    ),
                )

        convolution_form: Polynomial = {}
        for k in range(1, horizon + 1):
            if not supported_on_M(k, M):
                continue
            convolution_form = add_polynomials(
                convolution_form,
                scale_polynomial(
                    polynomial_from_tuple(calibration_A(horizon // k)),
                    Fraction(1, k),
                ),
                scale_polynomial(
                    log_integer_polynomial(k),
                    -Fraction(1, k) * calibration_B(horizon // k),
                ),
            )
        require(
            direct == convolution_form,
            "finite calibration convolution identity failed",
        )
        records.append(
            {
                "U": horizon,
                "M": M,
                "pointwise_convolution_failure_count": failure_count,
                "formal_term_count": len(direct),
                "direct_sha256": polynomial_digest(direct),
                "convolution_sha256": polynomial_digest(convolution_form),
                "identity_holds": True,
                "diagnostic_finite_magnitude": {
                    "value": format(evaluate_polynomial(direct), ".12e"),
                    "interpretation": (
                        "finite evaluation only; not evidence for uniform "
                        "calibration asymptotics"
                    ),
                    "analytic_evidence": False,
                },
            }
        )
    return {
        "identity": "mu(n)1_(n,M)=1 = (mu*g_M)(n) and its log convolution",
        "pointwise_convolution_test_count": total_convolution_tests,
        "cases": records,
        "finite_magnitude_samples_are_diagnostic_only": True,
        "all_finite_convolution_checks_hold": True,
    }


def deterministic_pair_weight(m_1: int, m_2: int) -> Fraction:
    numerator = (3 * m_1 + 5 * m_2) % 13 - 6
    denominator = 1 + (m_1 + 2 * m_2) % 7
    return Fraction(numerator, denominator)


def fiber_case_data(case: Mapping[str, object]) -> dict:
    h = int(case["h"])
    H = int(case["H"])
    u = int(case["u"])
    v = int(case["v"])
    field_prime = int(case["field_prime"])
    rows_1 = [int(value) for value in case["rows_1"]]  # type: ignore[index]
    rows_2 = [int(value) for value in case["rows_2"]]  # type: ignore[index]
    common = math.gcd(u, v)
    a_value = u // common
    b_value = v // common
    q = math.lcm(u, v)
    require(
        all(math.gcd(m, u * H) == 1 for m in rows_1),
        "first fiber row is not primitive",
    )
    require(
        all(math.gcd(m, v * H) == 1 for m in rows_2),
        "second fiber row is not primitive",
    )
    generator, root = exact_root(field_prime, q)
    inverse_h_q = pow(H, -1, q)
    units = [kappa for kappa in range(q) if math.gcd(kappa, q) == 1]
    Z = {kappa: Fraction(0) for kappa in units}
    compatible_pairs = []
    for m_1 in rows_1:
        for m_2 in rows_2:
            if (m_1 - m_2) % common or m_1 == m_2:
                continue
            weight = deterministic_pair_weight(m_1, m_2)
            if not weight:
                continue
            kappa_1 = (-h * pow(m_1, -1, u)) % u
            kappa_2 = (-h * pow(m_2, -1, v)) % v
            crt = crt_two(kappa_1, u, kappa_2, v)
            require(crt is not None and crt[1] == q, "fiber CRT failed")
            kappa = crt[0]
            require(kappa in Z, "joint class is not a unit")
            require(
                m_1 % u == (-h * pow(kappa, -1, u)) % u
                and m_2 % v == (-h * pow(kappa, -1, v)) % v,
                "row-fiber inverse map failed",
            )
            Z[kappa] += weight
            compatible_pairs.append((m_1, m_2, weight, kappa))
    require(compatible_pairs, "empty compatible fiber test")

    transform: List[int] = []
    direct_three_phase: List[int] = []
    inverse_h_g = inverse_or_zero(H, common)
    inverse_h_a = inverse_or_zero(H, a_value)
    inverse_h_b = inverse_or_zero(H, b_value)
    for r in range(q):
        value = sum(
            fraction_mod(Z[kappa], field_prime)
            * root_character(
                root, q, q, r * inverse_h_q * kappa, field_prime
            )
            for kappa in units
        ) % field_prime
        transform.append(value)

        direct = 0
        for m_1, m_2, weight, _ in compatible_pairs:
            phase_g = root_character(
                root,
                q,
                common,
                -h
                * r
                * inverse_h_g
                * inverse_or_zero(m_1, common)
                * inverse_or_zero(a_value * b_value, common),
                field_prime,
            )
            phase_a = root_character(
                root,
                q,
                a_value,
                -h
                * r
                * inverse_h_a
                * inverse_or_zero(m_1, a_value)
                * inverse_or_zero(common * b_value, a_value),
                field_prime,
            )
            phase_b = root_character(
                root,
                q,
                b_value,
                -h
                * r
                * inverse_h_b
                * inverse_or_zero(m_2, b_value)
                * inverse_or_zero(common * a_value, b_value),
                field_prime,
            )
            direct += (
                fraction_mod(weight, field_prime) * phase_g * phase_a * phase_b
            )
        direct %= field_prime
        direct_three_phase.append(direct)
        require(value == direct, "three inverse phases did not compress to DFT")

    parseval_left = sum(
        transform[r] * transform[(-r) % q] for r in range(q)
    ) % field_prime
    parseval_right = (
        q
        * sum(
            fraction_mod(value, field_prime) ** 2 for value in Z.values()
        )
    ) % field_prime
    require(parseval_left == parseval_right, "fiber Parseval failed")

    mean = sum(Z.values(), start=Fraction(0)) / euler_phi(q)
    discrepancy = {kappa: Z[kappa] - mean for kappa in units}
    discrepancy_transform = []
    for r in range(q):
        discrepancy_value = sum(
            fraction_mod(discrepancy[kappa], field_prime)
            * root_character(
                root, q, q, r * inverse_h_q * kappa, field_prime
            )
            for kappa in units
        ) % field_prime
        discrepancy_transform.append(discrepancy_value)
        mean_formula = (
            fraction_mod(mean, field_prime) * ramanujan_sum(q, r)
            + discrepancy_value
        ) % field_prime
        require(mean_formula == transform[r], "mean-discrepancy DFT split failed")

    discrepancy_parseval_left = sum(
        discrepancy_transform[r] * discrepancy_transform[(-r) % q]
        for r in range(q)
    ) % field_prime
    discrepancy_parseval_right = (
        q
        * sum(
            fraction_mod(value, field_prime) ** 2
            for value in discrepancy.values()
        )
    ) % field_prime
    require(
        discrepancy_parseval_left == discrepancy_parseval_right,
        "discrepancy Parseval failed",
    )

    kappa_0 = units[0]
    one_fiber_weight = Fraction(7, 5)
    one_fiber_field = fraction_mod(one_fiber_weight, field_prime)
    for r in range(q):
        one_value = (
            one_fiber_field
            * root_character(
                root, q, q, r * inverse_h_q * kappa_0, field_prime
            )
        ) % field_prime
        phase_inverse = root_character(
            root, q, q, -r * inverse_h_q * kappa_0, field_prime
        )
        require(
            one_value * phase_inverse % field_prime == one_fiber_field,
            "one-fiber saturation failed",
        )

    return {
        "name": str(case["name"]),
        "H": H,
        "u": u,
        "v": v,
        "g": common,
        "a": a_value,
        "b": b_value,
        "q": q,
        "finite_field": {
            "prime": field_prime,
            "primitive_generator": generator,
            "root_order": q,
            "root": root,
        },
        "row_pair_count": len(compatible_pairs),
        "nonzero_fiber_count": sum(bool(value) for value in Z.values()),
        "unit_fiber_count": len(units),
        "Z_sha256": canonical_digest(
            {str(kappa): fraction_record(Z[kappa]) for kappa in units}
        ),
        "DFT_sha256": canonical_digest(transform),
        "three_phase_sha256": canonical_digest(direct_three_phase),
        "mean": fraction_record(mean),
        "discrepancy_sha256": canonical_digest(
            {
                str(kappa): fraction_record(discrepancy[kappa])
                for kappa in units
            }
        ),
        "fiber_Parseval_holds": True,
        "mean_discrepancy_split_holds": True,
        "discrepancy_Parseval_holds": True,
        "one_fiber_saturation_holds": True,
        "all_checks_hold": True,
    }


def fiber_certificate() -> dict:
    cases = [
        {
            "name": "fiber-F61-q15",
            "h": 2,
            "H": 2,
            "u": 3,
            "v": 5,
            "field_prime": 61,
            "rows_1": [1, 7, 13, 19, 25, 31],
            "rows_2": [1, 11, 21, 31, 41],
        },
        {
            "name": "fiber-F421-q105",
            "h": 2,
            "H": 2,
            "u": 15,
            "v": 21,
            "field_prime": 421,
            "rows_1": [1, 7, 11, 13, 17, 19, 23, 29, 31, 37],
            "rows_2": [1, 5, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41],
        },
    ]
    records = [fiber_case_data(case) for case in cases]
    return {
        "method": "ordinary DFT of exact CRT-fiber weights in finite fields",
        "case_count": len(records),
        "cases": records,
        "all_fiber_compression_and_energy_checks_hold": True,
    }


def sign_migration_certificate() -> dict:
    triples = [(1, 3, 5), (3, 5, 7), (5, 7, 11), (7, 11, 13)]
    test_count = 0
    coprime_frequency_count = 0
    sample_records = []
    for common, a_value, b_value in triples:
        require(
            mobius(common * a_value * b_value) != 0
            and math.gcd(common, a_value) == 1
            and math.gcd(common, b_value) == 1
            and math.gcd(a_value, b_value) == 1,
            "invalid sign-migration triple",
        )
        q = common * a_value * b_value
        for r in range(1, 2 * q + 1):
            d_g = math.gcd(r, common)
            d_a = math.gcd(r, a_value)
            d_b = math.gcd(r, b_value)
            left = mobius(a_value) * mobius(b_value) * ramanujan_sum(q, r)
            right = (
                mobius(common // d_g)
                * mobius(d_a)
                * mobius(d_b)
                * euler_phi(d_g * d_a * d_b)
            )
            require(left == right, "squarefree sign migration failed")
            if math.gcd(r, q) == 1:
                require(left == mobius(common), "coprime sign migration failed")
                coprime_frequency_count += 1
            test_count += 1
        sample_records.append(
            {
                "g": common,
                "a": a_value,
                "b": b_value,
                "q": q,
                "tested_r_range": [1, 2 * q],
            }
        )
    return {
        "test_count": test_count,
        "coprime_frequency_count": coprime_frequency_count,
        "triples": sample_records,
        "all_squarefree_sign_migration_checks_hold": True,
    }


def normalize_linear(form: LinearForm) -> LinearForm:
    return {key: value for key, value in form.items() if value}


def add_linear(*forms: LinearForm) -> LinearForm:
    answer: LinearForm = {}
    for form in forms:
        for key, value in form.items():
            answer[key] = answer.get(key, Fraction(0)) + value
    return normalize_linear(answer)


def scale_linear(form: LinearForm, scalar: Fraction | int) -> LinearForm:
    scalar = Fraction(scalar)
    return normalize_linear({key: scalar * value for key, value in form.items()})


def linear_record(form: LinearForm) -> dict:
    return {key: fraction_record(value) for key, value in sorted(form.items())}


def exponent_ledger_certificate() -> dict:
    one = {"1": Fraction(1)}
    delta = {"delta": Fraction(1)}
    sigma = {"sigma": Fraction(1)}
    single_boundary = add_linear(scale_linear(one, Fraction(1, 2)), delta)
    joint_boundary = scale_linear(delta, 2)
    wedge_width = add_linear(single_boundary, scale_linear(joint_boundary, -1))
    expected_width = add_linear(
        scale_linear(one, Fraction(1, 2)), scale_linear(delta, -1)
    )
    require(wedge_width == expected_width, "wedge width identity failed")

    profiles = [
        ("published", Fraction(10, 21), Fraction(19, 126)),
        ("version_locked", Fraction(8, 17), Fraction(5, 34)),
    ]
    profile_records = []
    for name, lambda_constant, critical_constant in profiles:
        lambda_form = add_linear(
            scale_linear(one, lambda_constant), scale_linear(sigma, -1)
        )
        largest_row = add_linear(
            lambda_form,
            scale_linear(one, Fraction(1, 4)),
            scale_linear(delta, Fraction(-1, 2)),
        )
        critical_delta = add_linear(
            scale_linear(one, critical_constant),
            scale_linear(sigma, Fraction(-2, 3)),
        )
        margin = add_linear(single_boundary, scale_linear(largest_row, -1))
        expected_margin = scale_linear(
            add_linear(delta, scale_linear(critical_delta, -1)),
            Fraction(3, 2),
        )
        require(margin == expected_margin, "profile threshold identity failed")
        direct_critical = scale_linear(
            add_linear(lambda_form, scale_linear(one, Fraction(-1, 4))),
            Fraction(2, 3),
        )
        require(
            direct_critical == critical_delta,
            "critical profile exponent failed",
        )
        profile_records.append(
            {
                "name": name,
                "lambda": linear_record(lambda_form),
                "largest_row_exponent": linear_record(largest_row),
                "critical_delta": linear_record(critical_delta),
                "single_minus_largest_row": linear_record(margin),
                "identity": "margin=(3/2)(delta-critical_delta)",
                "identity_holds": True,
            }
        )
    return {
        "single_boundary": linear_record(single_boundary),
        "joint_boundary": linear_record(joint_boundary),
        "wedge_width": linear_record(wedge_width),
        "profiles": profile_records,
        "all_exponent_ledger_checks_hold": True,
    }


def finite_diagnostics() -> dict:
    return {
        "kind": "finite deterministic regression magnitudes only",
        "analytic_evidence": False,
        "asymptotic_evidence": False,
        "residual_dispersion_evidence": False,
        "twin_prime_evidence": False,
        "excluded_interpretations": [
            "not evidence for a residual-dispersion estimate",
            "not evidence for a prime-pair asymptotic",
            "not evidence for the twin-prime conjecture",
            "not a parity-barrier breakthrough",
        ],
    }


def build_certificate() -> dict:
    recombination = formal_recombination_certificate()
    calibration = calibration_convolution_certificate()
    kernel = kernel_dft_certificate()
    fibers = fiber_certificate()
    sign_migration = sign_migration_certificate()
    exponent_ledger = exponent_ledger_certificate()
    all_exact_checks_passed = all(
        [
            recombination["all_common_recombination_checks_hold"],
            calibration["all_finite_convolution_checks_hold"],
            kernel[
                "all_DFT_zero_mode_multiplier_and_Plancherel_checks_hold"
            ],
            fibers["all_fiber_compression_and_energy_checks_hold"],
            sign_migration["all_squarefree_sign_migration_checks_hold"],
            exponent_ledger["all_exponent_ledger_checks_hold"],
        ]
    )
    require(all_exact_checks_passed, "one or more exact layers failed")
    return {
        "certificate": "TPC-20 exact four-channel and CRT-fiber certificate",
        "scope": (
            "finite exact algebra only: integers, Fraction, formal prime-log "
            "polynomials, and finite fields with exact roots of unity"
        ),
        "twin_prime_evidence": False,
        "residual_dispersion_evidence": False,
        "asymptotic_evidence": False,
        "formal_common_recombination": recombination,
        "finite_calibration_convolution": calibration,
        "kernel_DFT_zero_mode_multiplier_and_Plancherel": kernel,
        "CRT_fiber_DFT_and_Parseval": fibers,
        "squarefree_sign_migration": sign_migration,
        "exponent_ledger": exponent_ledger,
        "finite_diagnostics": finite_diagnostics(),
        "all_exact_checks_passed": all_exact_checks_passed,
    }


def validate(certificate: Mapping[str, object]) -> None:
    require(certificate["twin_prime_evidence"] is False, "twin flag is not false")
    require(
        certificate["residual_dispersion_evidence"] is False,
        "residual-dispersion flag is not false",
    )
    require(
        certificate["asymptotic_evidence"] is False,
        "asymptotic flag is not false",
    )
    require(
        certificate["all_exact_checks_passed"] is True,
        "exact checks did not all pass",
    )
    diagnostics = certificate["finite_diagnostics"]
    require(isinstance(diagnostics, Mapping), "missing diagnostic mapping")
    for flag in (
        "twin_prime_evidence",
        "residual_dispersion_evidence",
        "asymptotic_evidence",
        "analytic_evidence",
    ):
        require(diagnostics[flag] is False, f"diagnostic flag {flag} is not false")


def main() -> None:
    certificate = build_certificate()
    validate(certificate)
    output_path = Path(__file__).with_suffix(".json")
    output_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"TPC-20 exact certificate passed: {output_path}")
    print("Twin-prime, residual-dispersion, and asymptotic evidence: false.")


if __name__ == "__main__":
    main()
