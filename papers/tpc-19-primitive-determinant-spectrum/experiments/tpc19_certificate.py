"""Exact finite certificate for the TPC-19 primitive determinant spectrum.

The proof layer in this program uses only integers, ``Fraction`` objects, and
formal indeterminates ``log(p)``.  It verifies exact identities for the
truncated Ramanujan model and for the full residual divisor expansion.  A
small sharp-window prime-data calculation is kept in a separately labelled
diagnostic section.  That diagnostic is a regression test for the code path;
it is not evidence for an asymptotic, a dispersion estimate, Hardy--Littlewood,
or the twin-prime conjecture.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


Monomial = Tuple[int, ...]
Polynomial = Dict[Monomial, Fraction]


def require(condition: bool, message: str) -> None:
    """Raise independently of Python's optional assertion optimization."""

    if not condition:
        raise RuntimeError(message)


def prime_factorization(n: int) -> Dict[int, int]:
    """Return the exact prime factorization of a positive integer."""

    if n < 1:
        raise ValueError("n must be positive")
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


def is_prime(n: int) -> bool:
    return n >= 2 and prime_factorization(n) == {n: 1}


def prime_power_base(n: int) -> int | None:
    """Return p when n is a positive power of one prime, otherwise None."""

    if n < 2:
        return None
    factors = prime_factorization(n)
    if len(factors) != 1:
        return None
    return next(iter(factors))


def fraction_record(value: Fraction) -> dict:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


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


def scale_polynomial(polynomial: Polynomial, scalar: Fraction | int) -> Polynomial:
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


def log_integer_polynomial(n: int) -> Polynomial:
    return {
        (prime,): Fraction(exponent)
        for prime, exponent in prime_factorization(n).items()
    }


def formal_von_mangoldt(n: int) -> Polynomial:
    prime = prime_power_base(n)
    return {} if prime is None else {(prime,): Fraction(1)}


def monomial_label(monomial: Monomial) -> str:
    if not monomial:
        return "1"
    return "*".join(f"log({prime})" for prime in monomial)


def polynomial_record(polynomial: Polynomial) -> dict:
    polynomial = normalize_polynomial(polynomial)
    return {
        monomial_label(monomial): fraction_record(coefficient)
        for monomial, coefficient in sorted(
            polynomial.items(), key=lambda item: (len(item[0]), item[0])
        )
    }


def polynomial_digest(polynomial: Polynomial) -> str:
    canonical = json.dumps(
        polynomial_record(polynomial), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def stable_decimal(value: float) -> str:
    """Serialize a diagnostic float at a platform-stable displayed precision."""

    return format(value, ".12e")


def lambda_prime_r_direct(r_cutoff: int, u: int) -> Fraction:
    """The divisor coefficient lambda'_R(u) from the Ramanujan model."""

    return Fraction(u) * sum(
        (
            Fraction(mobius(u * a) * mobius(a), euler_phi(u * a))
            for a in range(1, r_cutoff // u + 1)
        ),
        start=Fraction(0),
    )


def lambda_prime_r_squarefree(r_cutoff: int, u: int) -> Fraction:
    """The squarefree closed form for lambda'_R(u)."""

    mu_u = mobius(u)
    if not mu_u:
        return Fraction(0)
    positive_sum = sum(
        (
            Fraction(mobius(a) ** 2, euler_phi(a))
            for a in range(1, r_cutoff // u + 1)
            if math.gcd(a, u) == 1
        ),
        start=Fraction(0),
    )
    return Fraction(mu_u * u, euler_phi(u)) * positive_sum


def lambda_coefficients(r_cutoff: int) -> List[Fraction]:
    return [Fraction(0)] + [
        lambda_prime_r_direct(r_cutoff, u) for u in range(1, r_cutoff + 1)
    ]


def lambda_r_value(n: int, coefficients: Sequence[Fraction]) -> Fraction:
    return sum(
        (
            coefficients[u]
            for u in divisors(n)
            if u < len(coefficients)
        ),
        start=Fraction(0),
    )


def ramanujan_sum(q: int, n: int) -> int:
    """Compute c_q(n) from its divisor formula in exact arithmetic."""

    return sum(
        divisor * mobius(q // divisor)
        for divisor in divisors(math.gcd(q, n))
    )


@lru_cache(maxsize=None)
def lambda_r_ramanujan_value(r_cutoff: int, n: int) -> Fraction:
    """Evaluate Lambda_R from its original truncated Ramanujan definition."""

    return sum(
        (
            Fraction(mobius(q), euler_phi(q)) * ramanujan_sum(q, n)
            for q in range(1, r_cutoff + 1)
        ),
        start=Fraction(0),
    )


def coprime_lambda_sum(r_cutoff: int, a_value: int) -> Fraction:
    coefficients = lambda_coefficients(r_cutoff)
    return sum(
        (
            coefficients[u] / u
            for u in range(1, r_cutoff + 1)
            if math.gcd(u, a_value) == 1
        ),
        start=Fraction(0),
    )


def common_period(r_cutoff: int, h: int) -> int:
    period = abs(h)
    for modulus in range(1, r_cutoff + 1):
        period = math.lcm(period, modulus)
    return period


def require_primitive_model_row(
    r_cutoff: int, h: int, ell: int, d: int
) -> None:
    """Check the hypotheses used by the exact centering theorem."""

    require(h != 0, "the fixed shift must be nonzero")
    require(is_prime(ell) and ell > r_cutoff, "source must be a prime above R")
    require(mobius(d) != 0, "the divisor row must be squarefree")
    h_radical = radical(abs(h))
    require(math.gcd(d, h_radical) == 1, "row must be primitive")
    require(d * h_radical <= r_cutoff, "centering requires d*rad(h)<=R")


def masked_row_mean_record(r_cutoff: int, h: int, ell: int, d: int) -> dict:
    require_primitive_model_row(r_cutoff, h, ell, d)
    h_radical = radical(abs(h))
    period = common_period(r_cutoff, h)
    allowed = [j for j in range(period) if math.gcd(j, abs(h)) == 1]
    total = sum(
        (
            lambda_r_ramanujan_value(r_cutoff, ell * d * j + h)
            for j in allowed
        ),
        start=Fraction(0),
    )
    unnormalized = total / period
    conditional = total / len(allowed)
    expected_unnormalized = Fraction(d, euler_phi(d))
    expected_conditional = Fraction(h_radical, euler_phi(h_radical)) * expected_unnormalized
    holds = (
        unnormalized == expected_unnormalized
        and conditional == expected_conditional
    )
    require(holds, "masked finite-model row mean failed")
    return {
        "R": r_cutoff,
        "h": h,
        "ell": ell,
        "d": d,
        "period": period,
        "allowed_residue_count": len(allowed),
        "unnormalized_mean": fraction_record(unnormalized),
        "conditional_mean": fraction_record(conditional),
        "expected_conditional_mean": fraction_record(expected_conditional),
        "identity_holds": holds,
    }


def finite_model_covariance_formula(
    r_cutoff: int,
    h: int,
    ell_1: int,
    d_1: int,
    ell_2: int,
    d_2: int,
) -> Fraction:
    require_primitive_model_row(r_cutoff, h, ell_1, d_1)
    require_primitive_model_row(r_cutoff, h, ell_2, d_2)
    coefficients = lambda_coefficients(r_cutoff)
    h_radical = radical(abs(h))
    m_1 = ell_1 * d_1
    m_2 = ell_2 * d_2
    answer = Fraction(0)
    for u in range(1, r_cutoff + 1):
        if math.gcd(u, d_1 * h_radical) != 1:
            continue
        for v in range(1, r_cutoff + 1):
            if math.gcd(v, d_2 * h_radical) != 1:
                continue
            common = math.gcd(u, v)
            bracket = common * int((m_1 - m_2) % common == 0) - 1
            answer += coefficients[u] * coefficients[v] * Fraction(
                bracket, u * v
            )
    return answer


def centered_finite_model_row(
    r_cutoff: int, h: int, ell: int, d: int
) -> Tuple[List[int], List[Fraction]]:
    require_primitive_model_row(r_cutoff, h, ell, d)
    h_radical = radical(abs(h))
    center = Fraction(h_radical, euler_phi(h_radical)) * Fraction(
        d, euler_phi(d)
    )
    period = common_period(r_cutoff, h)
    allowed = [j for j in range(period) if math.gcd(j, abs(h)) == 1]
    row = [
        lambda_r_ramanujan_value(r_cutoff, ell * d * j + h) - center
        for j in allowed
    ]
    require(sum(row, start=Fraction(0)) == 0, "centered row has nonzero mean")
    return allowed, row


def direct_finite_model_covariance(
    r_cutoff: int,
    h: int,
    ell_1: int,
    d_1: int,
    ell_2: int,
    d_2: int,
) -> Fraction:
    allowed_1, row_1 = centered_finite_model_row(r_cutoff, h, ell_1, d_1)
    allowed_2, row_2 = centered_finite_model_row(r_cutoff, h, ell_2, d_2)
    require(allowed_1 == allowed_2, "row periods do not agree")
    return sum(
        (left * right for left, right in zip(row_1, row_2)),
        start=Fraction(0),
    ) / len(allowed_1)


def determinant(matrix: Sequence[Sequence[Fraction]]) -> Fraction:
    size = len(matrix)
    if size == 0:
        return Fraction(1)
    work = [list(row) for row in matrix]
    answer = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for entry in range(column, size):
            work[column][entry] /= pivot_value
        for row in range(column + 1, size):
            multiplier = work[row][column]
            if not multiplier:
                continue
            for entry in range(column, size):
                work[row][entry] -= multiplier * work[column][entry]
    return answer


def gram_and_psd_certificate() -> dict:
    r_cutoff = 12
    h = 2
    rows = [(31, 3), (41, 3), (43, 3), (47, 3)]
    centered_rows: List[List[Fraction]] = []
    allowed_reference: List[int] | None = None
    for ell, d in rows:
        allowed, row = centered_finite_model_row(r_cutoff, h, ell, d)
        if allowed_reference is None:
            allowed_reference = allowed
        require(allowed == allowed_reference, "Gram rows have different periods")
        centered_rows.append(row)
    require(allowed_reference is not None, "empty Gram row family")
    sample_count = len(allowed_reference)

    direct_matrix = [
        [
            sum(
                (
                    centered_rows[i][index] * centered_rows[j][index]
                    for index in range(sample_count)
                ),
                start=Fraction(0),
            )
            / sample_count
            for j in range(len(rows))
        ]
        for i in range(len(rows))
    ]
    formula_matrix = [
        [
            finite_model_covariance_formula(
                r_cutoff, h, rows[i][0], rows[i][1], rows[j][0], rows[j][1]
            )
            for j in range(len(rows))
        ]
        for i in range(len(rows))
    ]
    matrix_identity_holds = direct_matrix == formula_matrix
    require(matrix_identity_holds, "direct Gram matrix and CRT kernel differ")

    principal_minors = []
    for subset_size in range(1, len(rows) + 1):
        for subset in itertools.combinations(range(len(rows)), subset_size):
            submatrix = [
                [formula_matrix[i][j] for j in subset] for i in subset
            ]
            minor = determinant(submatrix)
            principal_minors.append({
                "indices": list(subset),
                "determinant": fraction_record(minor),
            })
            require(minor >= 0, "a covariance principal minor is negative")

    tested_vectors = 0
    minimum_quadratic_value: Fraction | None = None
    for vector in itertools.product(range(-2, 3), repeat=len(rows)):
        quadratic = sum(
            (
                vector[i] * formula_matrix[i][j] * vector[j]
                for i in range(len(rows))
                for j in range(len(rows))
            ),
            start=Fraction(0),
        )
        tested_vectors += 1
        minimum_quadratic_value = (
            quadratic
            if minimum_quadratic_value is None
            else min(minimum_quadratic_value, quadratic)
        )
        require(quadratic >= 0, "Gram quadratic form is negative")

    return {
        "R": r_cutoff,
        "h": h,
        "rows": [{"ell": ell, "d": d} for ell, d in rows],
        "conditional_period_sample_count": sample_count,
        "direct_matrix_equals_crt_kernel": matrix_identity_holds,
        "matrix": [
            [fraction_record(entry) for entry in row] for row in formula_matrix
        ],
        "principal_minors": principal_minors,
        "all_principal_minors_nonnegative": True,
        "tested_integer_vectors": tested_vectors,
        "minimum_tested_quadratic_value": fraction_record(
            minimum_quadratic_value or Fraction(0)
        ),
        "gram_psd_checks_hold": True,
    }


def g_one_cancellation_certificate() -> dict:
    r_cutoff = 12
    h = 2
    d_1 = d_2 = 3
    h_radical = radical(h)
    coefficients = lambda_coefficients(r_cutoff)
    eligible_pair_count = 0
    nonzero_bracket_count = 0
    contribution = Fraction(0)
    for u in range(1, r_cutoff + 1):
        if math.gcd(u, d_1 * h_radical) != 1:
            continue
        for v in range(1, r_cutoff + 1):
            if math.gcd(v, d_2 * h_radical) != 1:
                continue
            if math.gcd(u, v) != 1:
                continue
            eligible_pair_count += 1
            bracket = math.gcd(u, v) - 1
            nonzero_bracket_count += int(bracket != 0)
            contribution += coefficients[u] * coefficients[v] * Fraction(
                bracket, u * v
            )
    holds = nonzero_bracket_count == 0 and contribution == 0
    require(holds, "g=1 centered covariance did not cancel exactly")
    return {
        "R": r_cutoff,
        "h": h,
        "d_1": d_1,
        "d_2": d_2,
        "eligible_ordered_uv_pairs": eligible_pair_count,
        "nonzero_bracket_count": nonzero_bracket_count,
        "total_contribution": fraction_record(contribution),
        "all_g_equals_one_terms_cancel": holds,
    }


def rho_polynomial(r_cutoff: int, u: int) -> Polynomial:
    logarithmic_part = scale_polynomial(log_integer_polynomial(u), -mobius(u))
    finite_part = (
        constant_polynomial(-lambda_prime_r_direct(r_cutoff, u))
        if u <= r_cutoff
        else {}
    )
    return add_polynomials(logarithmic_part, finite_part)


def w_polynomial(r_cutoff: int, u: int) -> Polynomial:
    mu_u = mobius(u)
    if not mu_u:
        return {}
    answer = log_integer_polynomial(u)
    if u <= r_cutoff:
        positive_part = lambda_prime_r_direct(r_cutoff, u) / mu_u
        require(positive_part > 0, "the rational part of w_R is not positive")
        answer = add_polynomials(answer, constant_polynomial(positive_part))
    return answer


def formal_residual_direct(r_cutoff: int, n: int) -> Polynomial:
    return add_polynomials(
        formal_von_mangoldt(n),
        constant_polynomial(-lambda_r_ramanujan_value(r_cutoff, n)),
    )


def formal_residual_divisor_sum(r_cutoff: int, n: int) -> Polynomial:
    return add_polynomials(*(rho_polynomial(r_cutoff, u) for u in divisors(n)))


def formal_residual_certificate() -> dict:
    r_cutoff = 12
    coefficient_failure_count = 0
    nonsquarefree_support_failure_count = 0
    checked_u = range(1, 121)
    for u in checked_u:
        rho = rho_polynomial(r_cutoff, u)
        if mobius(u):
            expected = scale_polynomial(w_polynomial(r_cutoff, u), -mobius(u))
            coefficient_failure_count += int(rho != expected)
        else:
            nonsquarefree_support_failure_count += int(bool(rho))

    identity_failure_count = 0
    sample_records = {}
    for n in range(1, 361):
        direct = formal_residual_direct(r_cutoff, n)
        divisor_sum = formal_residual_divisor_sum(r_cutoff, n)
        identity_failure_count += int(direct != divisor_sum)
        if n in (1, 13, 77, 121, 210, 359):
            sample_records[str(n)] = polynomial_record(direct)

    h = 2
    ell_1, ell_2, d = 31, 41, 3
    m_1, m_2 = ell_1 * d, ell_2 * d
    direct_pair_sum: Polynomial = {}
    divisor_pair_sum: Polynomial = {}
    crt_pair_sum: Polynomial = {}
    determinant_support_failure_count = 0
    primitive_coprimality_failure_count = 0
    gab_coordinate_failure_count = 0
    gab_sign_failure_count = 0
    crt_compatibility_failure_count = 0
    g_channel_sums: Dict[int, Polynomial] = {}
    tested_j = [j for j in range(1, 25) if math.gcd(j, h) == 1]
    first_target_values = []
    second_target_values = []
    for j in tested_j:
        n_1 = m_1 * j + h
        n_2 = m_2 * j + h
        first_target_values.append(n_1)
        second_target_values.append(n_2)
        direct_pair_sum = add_polynomials(
            direct_pair_sum,
            multiply_polynomials(
                formal_residual_direct(r_cutoff, n_1),
                formal_residual_direct(r_cutoff, n_2),
            ),
        )
        rho_1 = [(u, rho_polynomial(r_cutoff, u)) for u in divisors(n_1)]
        rho_2 = [(v, rho_polynomial(r_cutoff, v)) for v in divisors(n_2)]
        for u, polynomial_u in rho_1:
            for v, polynomial_v in rho_2:
                common = math.gcd(u, v)
                determinant_support_failure_count += int(
                    (m_1 - m_2) % common != 0
                )
                product = multiply_polynomials(polynomial_u, polynomial_v)
                divisor_pair_sum = add_polynomials(divisor_pair_sum, product)
                g_channel_sums[common] = add_polynomials(
                    g_channel_sums.get(common, {}), product
                )

    # Independently reorder the same finite box by divisor moduli, construct
    # the generalized CRT class, and count its visits to the j-window.
    u_candidates = sorted(
        {u for target in first_target_values for u in divisors(target)}
    )
    v_candidates = sorted(
        {v for target in second_target_values for v in divisors(target)}
    )
    for u in u_candidates:
        polynomial_u = rho_polynomial(r_cutoff, u)
        if not polynomial_u:
            continue
        primitive_coprimality_failure_count += int(
            math.gcd(u, m_1 * radical(h)) != 1
        )
        for v in v_candidates:
            polynomial_v = rho_polynomial(r_cutoff, v)
            if not polynomial_v:
                continue
            primitive_coprimality_failure_count += int(
                math.gcd(v, m_2 * radical(h)) != 1
            )
            common = math.gcd(u, v)
            a_value = u // common
            b_value = v // common
            coordinates_hold = (
                mobius(common) != 0
                and mobius(a_value) != 0
                and mobius(b_value) != 0
                and math.gcd(common, a_value) == 1
                and math.gcd(common, b_value) == 1
                and math.gcd(a_value, b_value) == 1
            )
            gab_coordinate_failure_count += int(not coordinates_hold)
            expected_product = scale_polynomial(
                multiply_polynomials(
                    w_polynomial(r_cutoff, u), w_polynomial(r_cutoff, v)
                ),
                mobius(a_value) * mobius(b_value),
            )
            actual_product = multiply_polynomials(polynomial_u, polynomial_v)
            gab_sign_failure_count += int(actual_product != expected_product)

            residue_u = 0 if u == 1 else (-h * pow(m_1, -1, u)) % u
            residue_v = 0 if v == 1 else (-h * pow(m_2, -1, v)) % v
            compatible = (m_1 - m_2) % common == 0
            brute_visits = [
                j
                for j in tested_j
                if (m_1 * j + h) % u == 0 and (m_2 * j + h) % v == 0
            ]
            if compatible:
                reduced_v = v // common
                if reduced_v == 1:
                    multiplier = 0
                else:
                    multiplier = (
                        ((residue_v - residue_u) // common)
                        * pow(u // common, -1, reduced_v)
                    ) % reduced_v
                joint_modulus = math.lcm(u, v)
                joint_residue = (residue_u + u * multiplier) % joint_modulus
                crt_visits = [
                    j for j in tested_j if j % joint_modulus == joint_residue
                ]
            else:
                crt_visits = []
            crt_compatibility_failure_count += int(brute_visits != crt_visits)
            if crt_visits:
                crt_pair_sum = add_polynomials(
                    crt_pair_sum,
                    scale_polynomial(actual_product, len(crt_visits)),
                )

    pair_identity_holds = direct_pair_sum == divisor_pair_sum
    crt_pair_identity_holds = direct_pair_sum == crt_pair_sum
    all_checks_hold = (
        coefficient_failure_count == 0
        and nonsquarefree_support_failure_count == 0
        and identity_failure_count == 0
        and determinant_support_failure_count == 0
        and primitive_coprimality_failure_count == 0
        and gab_coordinate_failure_count == 0
        and gab_sign_failure_count == 0
        and crt_compatibility_failure_count == 0
        and pair_identity_holds
        and crt_pair_identity_holds
    )
    require(all_checks_hold, "formal full-residual identity failed")
    return {
        "R": r_cutoff,
        "u_range": [checked_u.start, checked_u.stop - 1],
        "rho_equals_minus_mu_times_w_failure_count": coefficient_failure_count,
        "nonsquarefree_support_failure_count": nonsquarefree_support_failure_count,
        "pointwise_n_range": [1, 360],
        "pointwise_identity_failure_count": identity_failure_count,
        "formal_samples": sample_records,
        "pair_test": {
            "h": h,
            "ell_1": ell_1,
            "ell_2": ell_2,
            "d": d,
            "j_values": tested_j,
            "direct_polynomial_term_count": len(direct_pair_sum),
            "direct_polynomial_sha256": polynomial_digest(direct_pair_sum),
            "divisor_polynomial_sha256": polynomial_digest(divisor_pair_sum),
            "crt_polynomial_sha256": polynomial_digest(crt_pair_sum),
            "g_channels": {
                str(common): {
                    "term_count": len(polynomial),
                    "sha256": polynomial_digest(polynomial),
                }
                for common, polynomial in sorted(g_channel_sums.items())
            },
            "determinant_support_failure_count": determinant_support_failure_count,
            "primitive_coprimality_failure_count": (
                primitive_coprimality_failure_count
            ),
            "gab_coordinate_failure_count": gab_coordinate_failure_count,
            "gab_sign_failure_count": gab_sign_failure_count,
            "crt_compatibility_failure_count": crt_compatibility_failure_count,
            "formal_pair_identity_holds": pair_identity_holds,
            "formal_crt_reassembly_holds": crt_pair_identity_holds,
        },
        "all_formal_residual_checks_hold": all_checks_hold,
    }


def finite_model_algebra_certificate() -> dict:
    lambda_test_count = 0
    lambda_failure_count = 0
    nonsquarefree_failure_count = 0
    for r_cutoff in (8, 10, 12, 18):
        for u in range(1, r_cutoff + 1):
            direct = lambda_prime_r_direct(r_cutoff, u)
            closed = lambda_prime_r_squarefree(r_cutoff, u)
            lambda_test_count += 1
            lambda_failure_count += int(direct != closed)
            if not mobius(u):
                nonsquarefree_failure_count += int(bool(direct))

    model_divisor_test_count = 0
    model_divisor_failure_count = 0
    for r_cutoff in (8, 12, 18):
        coefficients = lambda_coefficients(r_cutoff)
        for n in range(1, 181):
            model_divisor_test_count += 1
            model_divisor_failure_count += int(
                lambda_r_ramanujan_value(r_cutoff, n)
                != lambda_r_value(n, coefficients)
            )

    coprime_cases = [
        (8, 1),
        (8, 6),
        (10, 6),
        (12, 6),
        (12, 10),
        (18, 15),
    ]
    coprime_records = []
    coprime_failure_count = 0
    for r_cutoff, a_value in coprime_cases:
        require(radical(a_value) <= r_cutoff, "invalid coprime-sum test case")
        direct = coprime_lambda_sum(r_cutoff, a_value)
        expected = Fraction(radical(a_value), euler_phi(radical(a_value)))
        coprime_failure_count += int(direct != expected)
        coprime_records.append({
            "R": r_cutoff,
            "A": a_value,
            "direct": fraction_record(direct),
            "expected": fraction_record(expected),
            "identity_holds": direct == expected,
        })

    mean_records = [
        masked_row_mean_record(8, 2, 11, 3),
        masked_row_mean_record(10, 3, 11, 2),
        masked_row_mean_record(12, 2, 31, 3),
    ]

    witness_formula = finite_model_covariance_formula(12, 2, 31, 3, 41, 3)
    witness_direct = direct_finite_model_covariance(12, 2, 31, 3, 41, 3)
    expected_witness = Fraction(433, 450)
    witness_holds = witness_formula == witness_direct == expected_witness
    require(witness_holds, "the 433/450 covariance witness failed")

    negative_formula = finite_model_covariance_formula(12, 2, 31, 3, 43, 3)
    negative_direct = direct_finite_model_covariance(12, 2, 31, 3, 43, 3)
    expected_negative = Fraction(-259, 900)
    negative_holds = negative_formula == negative_direct == expected_negative
    require(negative_holds, "the negative covariance regression case failed")

    all_checks_hold = (
        lambda_failure_count == 0
        and nonsquarefree_failure_count == 0
        and model_divisor_failure_count == 0
        and coprime_failure_count == 0
        and all(record["identity_holds"] for record in mean_records)
        and witness_holds
        and negative_holds
    )
    require(all_checks_hold, "finite-model algebra checks failed")
    return {
        "lambda_prime_squarefree_formula": {
            "test_count": lambda_test_count,
            "failure_count": lambda_failure_count,
            "nonsquarefree_support_failure_count": nonsquarefree_failure_count,
            "identity_and_support_hold": True,
        },
        "ramanujan_to_divisor_model": {
            "test_count": model_divisor_test_count,
            "failure_count": model_divisor_failure_count,
            "identity_holds": model_divisor_failure_count == 0,
        },
        "coprime_mean_sum": {
            "cases": coprime_records,
            "failure_count": coprime_failure_count,
            "all_cases_hold": True,
        },
        "masked_row_means": mean_records,
        "covariance_regression_cases": {
            "positive_componentwise_no_go_witness": {
                "R": 12,
                "h": 2,
                "ell_1": 31,
                "ell_2": 41,
                "d_1": 3,
                "d_2": 3,
                "direct": fraction_record(witness_direct),
                "formula": fraction_record(witness_formula),
                "expected": fraction_record(expected_witness),
                "identity_holds": witness_holds,
                "interpretation": (
                    "nonzero primitive distinct-source finite-model covariance; "
                    "not a counterexample "
                    "to residual DD_h"
                ),
            },
            "signed_negative_case": {
                "R": 12,
                "h": 2,
                "ell_1": 31,
                "ell_2": 43,
                "d_1": 3,
                "d_2": 3,
                "direct": fraction_record(negative_direct),
                "formula": fraction_record(negative_formula),
                "expected": fraction_record(expected_negative),
                "identity_holds": negative_holds,
            },
        },
        "all_finite_model_algebra_checks_hold": all_checks_hold,
    }


def von_mangoldt_float(n: int) -> float:
    prime = prime_power_base(n)
    return 0.0 if prime is None else math.log(prime)


def diagnostic_case(r_cutoff: int, ell_scale: int, d_scale: int, j_scale: int) -> dict:
    """A small deterministic sharp-window diagnostic, never a theorem check."""

    h = 2
    kappa = 0.15
    h_radical = radical(h)
    v_limit = math.isqrt(r_cutoff)
    ells = [ell for ell in range(ell_scale, 2 * ell_scale) if is_prime(ell)]
    d_values = [
        d
        for d in range(d_scale, min(2 * d_scale, v_limit + 1))
        if mobius(d) and math.gcd(d, h) == 1
    ]
    j_values = [
        j for j in range(j_scale, 2 * j_scale) if math.gcd(j, h) == 1
    ]
    labels = [(ell, d) for ell in ells for d in d_values]
    coefficients = lambda_coefficients(r_cutoff)
    lambda_rows: List[List[float]] = []
    model_rows: List[List[float]] = []
    raw_residual_rows: List[List[float]] = []
    for ell, d in labels:
        source_weight = mobius(d) * math.log(ell)
        center_model = Fraction(h_radical, euler_phi(h_radical)) * Fraction(
            d, euler_phi(d)
        )
        center_prime = Fraction(h_radical, euler_phi(h_radical)) * Fraction(
            ell * d, (ell - 1) * euler_phi(d)
        )
        lambda_row = []
        model_row = []
        raw_row = []
        for j in j_values:
            target = ell * d * j + h
            lambda_value = von_mangoldt_float(target)
            model_value = float(lambda_r_value(target, coefficients))
            lambda_row.append(source_weight * (lambda_value - float(center_prime)))
            model_row.append(source_weight * (model_value - float(center_model)))
            raw_row.append(source_weight * (lambda_value - model_value))
        lambda_rows.append(lambda_row)
        model_rows.append(model_row)
        raw_residual_rows.append(raw_row)

    x_scale = ell_scale * d_scale * j_scale
    q_scale = ell_scale * d_scale
    determinant_threshold = q_scale * x_scale ** (-kappa)
    gcd_threshold = x_scale**kappa

    def is_generic(index_1: int, index_2: int) -> bool:
        if index_1 == index_2:
            return False
        ell_1, d_1 = labels[index_1]
        ell_2, d_2 = labels[index_2]
        if ell_1 == ell_2:
            return False
        difference = abs(ell_1 * d_1 - ell_2 * d_2)
        return (
            difference > determinant_threshold
            and math.gcd(d_1, d_2) <= gcd_threshold
        )

    def correlation(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> float:
        total = 0.0
        for index_1 in range(len(labels)):
            for index_2 in range(len(labels)):
                if not is_generic(index_1, index_2):
                    continue
                total += sum(
                    value_1 * value_2
                    for value_1, value_2 in zip(left[index_1], right[index_2])
                )
        return total / (x_scale * q_scale)

    ll_value = correlation(lambda_rows, lambda_rows)
    lm_value = correlation(lambda_rows, model_rows)
    ml_value = correlation(model_rows, lambda_rows)
    mm_value = correlation(model_rows, model_rows)
    paired_value = ll_value - lm_value - ml_value + mm_value
    raw_value = correlation(raw_residual_rows, raw_residual_rows)
    require(
        abs(paired_value - correlation(
            [
                [left - right for left, right in zip(lambda_row, model_row)]
                for lambda_row, model_row in zip(lambda_rows, model_rows)
            ],
            [
                [left - right for left, right in zip(lambda_row, model_row)]
                for lambda_row, model_row in zip(lambda_rows, model_rows)
            ],
        )) < 1e-12,
        "diagnostic paired expansion is inconsistent",
    )
    return {
        "R": r_cutoff,
        "L": ell_scale,
        "D": d_scale,
        "J": j_scale,
        "V": v_limit,
        "h": h,
        "ell_count": len(ells),
        "d_values": d_values,
        "primitive_j_count": len(j_values),
        "row_count": len(labels),
        "X_scale": x_scale,
        "Q_scale": q_scale,
        "kappa": kappa,
        "normalized_components": {
            "serialization": "signed scientific-decimal strings, 12 digits",
            "Lambda_Lambda": stable_decimal(ll_value),
            "Lambda_Lambda_R": stable_decimal(lm_value),
            "Lambda_R_Lambda": stable_decimal(ml_value),
            "Lambda_R_Lambda_R": stable_decimal(mm_value),
            "paired_centered_residual": stable_decimal(paired_value),
            "raw_residual": stable_decimal(raw_value),
        },
    }


def optional_prime_diagnostic() -> dict:
    cases = [
        diagnostic_case(30, 70, 3, 80),
        diagnostic_case(60, 130, 4, 100),
    ]
    return {
        "kind": "finite sharp-window numerical regression only",
        "prime_asymptotic_evidence": False,
        "uses_smooth_paper_cutoffs": False,
        "excluded_interpretations": [
            "not evidence for DD_h(theta)",
            "not evidence for a prime-pair asymptotic",
            "not evidence for Hardy--Littlewood",
            "not evidence for the twin-prime conjecture",
        ],
        "cases": cases,
    }


def build_certificate(include_diagnostic: bool = True) -> dict:
    finite_model = finite_model_algebra_certificate()
    g_one = g_one_cancellation_certificate()
    gram = gram_and_psd_certificate()
    residual = formal_residual_certificate()
    all_exact_checks_passed = (
        finite_model["all_finite_model_algebra_checks_hold"]
        and g_one["all_g_equals_one_terms_cancel"]
        and gram["gram_psd_checks_hold"]
        and residual["all_formal_residual_checks_hold"]
    )
    require(all_exact_checks_passed, "one or more exact certificate layers failed")
    certificate = {
        "certificate": "TPC-19 exact primitive determinant-spectrum certificate",
        "scope": (
            "exact finite integer/Fraction/formal-log identities; optional finite "
            "prime-data diagnostic is isolated and non-evidentiary"
        ),
        "prime_asymptotic_evidence": False,
        "excluded_claims": [
            "no proof or numerical evidence for DD_h(theta)",
            "no asymptotic distribution theorem for primes",
            "no fixed-shift Hardy--Littlewood asymptotic",
            "no evidence for the twin-prime conjecture",
            "no parity-barrier breakthrough",
            "no Kuznetsov or spectral cancellation estimate",
        ],
        "finite_model_algebra": finite_model,
        "g_equals_one_cancellation": g_one,
        "gram_and_psd": gram,
        "formal_full_residual": residual,
        "optional_prime_diagnostic": (
            optional_prime_diagnostic()
            if include_diagnostic
            else {
                "kind": "skipped by command-line request",
                "prime_asymptotic_evidence": False,
                "cases": [],
            }
        ),
        "all_exact_checks_passed": all_exact_checks_passed,
    }
    return certificate


def validate(certificate: dict) -> None:
    checks = (
        certificate["prime_asymptotic_evidence"] is False,
        certificate["finite_model_algebra"][
            "all_finite_model_algebra_checks_hold"
        ],
        certificate["g_equals_one_cancellation"][
            "all_g_equals_one_terms_cancel"
        ],
        certificate["gram_and_psd"]["gram_psd_checks_hold"],
        certificate["formal_full_residual"][
            "all_formal_residual_checks_hold"
        ],
        certificate["optional_prime_diagnostic"][
            "prime_asymptotic_evidence"
        ]
        is False,
        certificate["all_exact_checks_passed"],
    )
    require(all(checks), "certificate validation failed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-diagnostic",
        action="store_true",
        help="run only exact checks and omit the small prime-data diagnostic",
    )
    arguments = parser.parse_args()
    certificate = build_certificate(include_diagnostic=not arguments.skip_diagnostic)
    validate(certificate)
    output_path = Path(__file__).with_suffix(".json")
    output_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"TPC-19 exact determinant-spectrum certificate passed: {output_path}")
    print("Prime asymptotic evidence: false.")


if __name__ == "__main__":
    main()
