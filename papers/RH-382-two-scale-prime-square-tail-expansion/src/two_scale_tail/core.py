"""Exact reproduction certificates for the RH-382 two-scale theorem.

The all-y statement is proved symbolically in the manuscript.  This module
uses only standard-library :class:`fractions.Fraction` arithmetic to replay
finite Euler/run identities, the product and cube ledgers used by the proof,
and a reproduction-only one-tail sign mutation.  No finite row is used as a
fit or as a substitute for the all-order inequalities.
"""

from __future__ import annotations

from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from math import isqrt


X_COEFFICIENTS = {4: 2, 5: -4, 6: 6, 7: -8, 8: 10}
M_COEFFICIENTS = {3: 2, 4: -4, 5: 6, 6: -8, 7: 10, 8: -12}
X_QUADRATIC_CONSTANT = Fraction(931, 4)
M_LIPSCHITZ_CONSTANT = 63
X_CHANNEL_CONSTANT = Fraction(931, 2)
MEMORY_CHANNEL_CONSTANT = Fraction(254, 3)
TOTAL_REMAINDER_CONSTANT = Fraction(3301, 6)
PUBLISHED_REMAINDER_CONSTANT = 551
WITNESS_PRIME = 71
WITNESS_START_Y = 18
WITNESS_ENDPOINT_Y = 19
FINITE_GAP_CASES = ((1, 8), (3, 12), (8, 19), (18, 19))
CERTIFICATE_FIXTURE_BYTES = 22543
CERTIFICATE_FIXTURE_SHA256 = "5fe227102a0a88307b5788f55d61bbbe07a17e5158aca11cfbbc79ec9e0cb624"


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("an exact Fraction is required")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def fraction_decimal(value: Fraction, places: int = 15) -> str:
    if type(value) is not Fraction or type(places) is not int or places < 1:
        raise TypeError("exact Fraction and positive exact integer places are required")
    context = Context(prec=max(places + 20, 40), rounding=ROUND_HALF_EVEN)
    with localcontext(context):
        decimal_value = Decimal(value.numerator) / Decimal(value.denominator)
        return format(decimal_value, f".{places}f")


def sieve_primes(limit: int) -> tuple[int, ...]:
    if type(limit) is not int or limit < 2:
        raise ValueError("prime cutoff must be an exact integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return tuple(index for index, flag in enumerate(sieve) if flag)


def first_odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive exact integer")
    limit = 64
    while True:
        primes = tuple(prime for prime in sieve_primes(limit) if prime != 2)
        if len(primes) >= count:
            return primes[:count]
        limit *= 2


def prime_square_weight(prime: int) -> Fraction:
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("an odd prime at least three is required")
    if any(prime % divisor == 0 for divisor in range(3, isqrt(prime) + 1, 2)):
        raise ValueError("an odd prime at least three is required")
    return Fraction(1, prime * prime - 1)


def _fraction_product(values: tuple[Fraction, ...]) -> Fraction:
    if any(type(value) is not Fraction for value in values):
        raise TypeError("product factors must be exact Fractions")
    output = Fraction(1)
    for value in values:
        output *= value
    return output


def _exact_integer(value: Fraction, label: str) -> int:
    if type(value) is not Fraction or value.denominator != 1:
        raise ArithmeticError(f"{label} is not an exact integer")
    return value.numerator


def square_parameters(y: int) -> dict[str, object]:
    primes = first_odd_primes(y)
    p_product = 1
    a_product = 1
    d_product = 1
    for prime in primes:
        p_product *= prime * prime
        a_product *= prime * prime - 1
        d_product *= prime * prime - 2
    return {"y": y, "primes": primes, "p_y": primes[-1], "P": p_product, "A": a_product, "D": d_product}


def finite_euler_values(y: int) -> dict[int, Fraction]:
    """Return E_1,...,E_9 and deliberately never construct E_10."""

    primes = first_odd_primes(y)
    return {
        m: _fraction_product(tuple(Fraction(prime * prime - m, prime * prime) for prime in primes))
        for m in range(1, 10)
    }


def normalized_euler_ratios(y: int) -> dict[int, Fraction]:
    values = finite_euler_values(y)
    return {m: values[m] / values[1] for m in range(1, 9)}


def square_run_counts(y: int) -> dict[int, int]:
    """Use second differences only through length seven and terminal R8=P E8."""

    parameters = square_parameters(y)
    period = parameters["P"]
    if type(period) is not int:
        raise TypeError("square period product is not an integer")
    euler = finite_euler_values(y)
    output = {
        length: _exact_integer(
            Fraction(period) * (euler[length] - 2 * euler[length + 1] + euler[length + 2]),
            f"R_{length}({y})",
        )
        for length in range(1, 8)
    }
    output[8] = _exact_integer(Fraction(period) * euler[8], f"terminal R_8({y})")
    return output


def run_statistics(y: int) -> dict[str, int]:
    runs = square_run_counts(y)
    even_runs = sum(runs[length] for length in (2, 4, 6, 8))
    even_sites = sum(length * runs[length] for length in (2, 4, 6, 8))
    return {
        "O": sum(runs[length] for length in (1, 3, 5, 7)),
        "E": even_runs,
        "L": even_sites,
        "M": sum((length - 1) * runs[length] for length in (1, 3, 5, 7)),
        "X": even_sites - 2 * even_runs,
        "R8": runs[8],
    }


def normalized_x(y: int) -> Fraction:
    ratios = normalized_euler_ratios(y)
    euler_form = sum((coefficient * ratios[m] for m, coefficient in X_COEFFICIENTS.items()), Fraction(0))
    parameters = square_parameters(y)
    statistics = run_statistics(y)
    run_form = Fraction(statistics["X"], parameters["A"])
    if euler_form != run_form:
        raise AssertionError("Euler and run forms of X_y disagree")
    return euler_form


def normalized_memory(y: int) -> Fraction:
    """Return M_y/A_y, checking the exact E9=0 terminal in the derivation."""

    euler = finite_euler_values(y)
    if euler[9] != 0:
        raise AssertionError("E_9 must vanish exactly because p_1=3")
    ratios = normalized_euler_ratios(y)
    euler_form = sum((coefficient * ratios[m] for m, coefficient in M_COEFFICIENTS.items()), Fraction(0))
    parameters = square_parameters(y)
    statistics = run_statistics(y)
    run_form = Fraction(statistics["M"], parameters["A"])
    if euler_form != run_form:
        raise AssertionError("Euler and run forms of M_y/A_y disagree")
    if not Fraction(0) <= euler_form <= Fraction(1):
        raise AssertionError("normalized memory is outside the site-count interval")
    return euler_form


def endpoint_coefficients(endpoint_y: int) -> dict[str, Fraction]:
    ratios = normalized_euler_ratios(endpoint_y)
    x_value = sum((coefficient * ratios[m] for m, coefficient in X_COEFFICIENTS.items()), Fraction(0))
    y_value = sum((coefficient * (m - 1) * ratios[m] for m, coefficient in X_COEFFICIENTS.items()), Fraction(0))
    m_value = sum((coefficient * ratios[m] for m, coefficient in M_COEFFICIENTS.items()), Fraction(0))
    if m_value != normalized_memory(endpoint_y):
        raise AssertionError("endpoint memory coefficient disagrees with run form")
    return {"X": x_value, "Y": y_value, "m": m_value}


def tail_weights(start_y: int, endpoint_y: int) -> tuple[Fraction, ...]:
    if type(start_y) is not int or type(endpoint_y) is not int:
        raise TypeError("tail endpoints must be exact integers")
    if start_y < 1 or endpoint_y <= start_y:
        raise ValueError("tail endpoints require 1 <= start_y < endpoint_y")
    primes = first_odd_primes(endpoint_y)
    return tuple(prime_square_weight(prime) for prime in primes[start_y:endpoint_y])


def bonferroni_product(weights: tuple[Fraction, ...]) -> dict[str, object]:
    if not weights or any(type(weight) is not Fraction for weight in weights):
        raise TypeError("a nonempty tuple of exact Fraction weights is required")
    if any(weight < 0 or weight >= 1 for weight in weights):
        raise ValueError("Bonferroni weights must lie in [0,1)")
    total = sum(weights, Fraction(0))
    product = _fraction_product(tuple(Fraction(1) - weight for weight in weights))
    loss = Fraction(1) - product
    lower = total - total * total / 2
    return {
        "count": len(weights),
        "T": fraction_text(total),
        "product": fraction_text(product),
        "loss": fraction_text(loss),
        "lower": fraction_text(lower),
        "lower_pass": lower <= loss,
        "upper_pass": loss <= total,
        "all_pass": lower <= loss <= total,
    }


def product_expansion_row(m: int, start_y: int, endpoint_y: int) -> dict[str, object]:
    if type(m) is not int or not 3 <= m <= 8:
        raise ValueError("m must be an exact integer in 3..8")
    weights = tail_weights(start_y, endpoint_y)
    k = m - 1
    scaled = tuple(k * weight for weight in weights)
    product = _fraction_product(tuple(Fraction(1) - value for value in scaled))
    start_ratio = normalized_euler_ratios(start_y)[m]
    endpoint_ratio = normalized_euler_ratios(endpoint_y)[m]
    total = sum(weights, Fraction(0))
    x = k * total
    delta = Fraction(1) - product
    remainder = start_ratio - endpoint_ratio - endpoint_ratio * x
    upper = start_ratio * x * x
    coarse_upper = Fraction(9 - m, 8) * x * x
    all_pass = (
        endpoint_ratio == start_ratio * product
        and product <= Fraction(1, 1 + x)
        and delta <= x
        and Fraction(0) <= remainder <= upper <= coarse_upper
    )
    return {
        "m": m,
        "start_y": start_y,
        "endpoint_y": endpoint_y,
        "tail_count": len(weights),
        "T": fraction_text(total),
        "x": fraction_text(x),
        "P": fraction_text(product),
        "U_start": fraction_text(start_ratio),
        "u_endpoint": fraction_text(endpoint_ratio),
        "remainder": fraction_text(remainder),
        "upper": fraction_text(upper),
        "coarse_upper": fraction_text(coarse_upper),
        "ratio_identity_pass": endpoint_ratio == start_ratio * product,
        "P_le_inverse_pass": product <= Fraction(1, 1 + x),
        "delta_le_x_pass": delta <= x,
        "quadratic_remainder_pass": Fraction(0) <= remainder <= upper <= coarse_upper,
        "all_pass": all_pass,
    }


def exact_tail_algebra(weights: tuple[Fraction, ...]) -> dict[str, object]:
    if not weights or any(type(weight) is not Fraction for weight in weights):
        raise TypeError("a nonempty tuple of exact Fraction weights is required")
    if any(weight < 0 for weight in weights):
        raise ValueError("tail weights must be nonnegative")
    suffix = Fraction(0)
    current_sum = Fraction(0)
    next_sum = Fraction(0)
    cross_cube_sum = Fraction(0)
    right_square_sum = Fraction(0)
    left_square_sum = Fraction(0)
    cube_sum = sum((weight**3 for weight in weights), Fraction(0))
    square_sum = sum((weight**2 for weight in weights), Fraction(0))
    for weight in reversed(weights):
        next_tail = suffix
        current_tail = next_tail + weight
        current_sum += weight * current_tail
        next_sum += weight * next_tail
        cross_cube_sum += weight * current_tail * next_tail
        right_square_sum += weight * next_tail * next_tail
        left_square_sum += weight * current_tail * current_tail
        suffix = current_tail
    current_rhs = (suffix * suffix + square_sum) / 2
    next_rhs = (suffix * suffix - square_sum) / 2
    cross_rhs = (suffix**3 - cube_sum) / 3
    all_pass = (
        current_sum == current_rhs
        and next_sum == next_rhs
        and cross_cube_sum == cross_rhs
        and right_square_sum <= suffix**3 / 3
        and left_square_sum <= suffix**3
    )
    return {
        "count": len(weights),
        "T": fraction_text(suffix),
        "S": fraction_text(square_sum),
        "C": fraction_text(cube_sum),
        "current": fraction_text(current_sum),
        "next": fraction_text(next_sum),
        "cross_cube": fraction_text(cross_cube_sum),
        "right_square": fraction_text(right_square_sum),
        "left_square": fraction_text(left_square_sum),
        "current_identity_pass": current_sum == current_rhs,
        "next_identity_pass": next_sum == next_rhs,
        "cross_cube_identity_pass": cross_cube_sum == cross_rhs,
        "right_square_cube_bound_pass": right_square_sum <= suffix**3 / 3,
        "left_square_cube_bound_pass": left_square_sum <= suffix**3,
        "all_pass": all_pass,
    }


def coefficient_ledger() -> dict[str, object]:
    x_terms = {
        str(m): Fraction(abs(coefficient) * (9 - m) * (m - 1) ** 2, 8)
        for m, coefficient in X_COEFFICIENTS.items()
    }
    m_terms = {
        str(m): Fraction(abs(coefficient) * (9 - m) * (m - 1), 8)
        for m, coefficient in M_COEFFICIENTS.items()
    }
    x_total = sum(x_terms.values(), Fraction(0))
    m_total = sum(m_terms.values(), Fraction(0))
    x_channel = 2 * x_total
    memory_m_channel = Fraction(4) * m_total / 3
    memory_h_channel = Fraction(4) * Fraction(1, 2) / 3
    memory_channel = memory_m_channel + memory_h_channel
    total = x_channel + memory_channel
    all_pass = (
        x_total == X_QUADRATIC_CONSTANT
        and m_total == M_LIPSCHITZ_CONSTANT
        and x_channel == X_CHANNEL_CONSTANT
        and memory_channel == MEMORY_CHANNEL_CONSTANT
        and total == TOTAL_REMAINDER_CONSTANT
        and total < PUBLISHED_REMAINDER_CONSTANT
    )
    return {
        "x_quadratic_terms": {key: fraction_text(value) for key, value in x_terms.items()},
        "x_quadratic_total": fraction_text(x_total),
        "memory_lipschitz_terms": {key: fraction_text(value) for key, value in m_terms.items()},
        "memory_lipschitz_total": fraction_text(m_total),
        "x_channel": fraction_text(x_channel),
        "memory_m_variation": fraction_text(memory_m_channel),
        "memory_H_variation": fraction_text(memory_h_channel),
        "memory_channel": fraction_text(memory_channel),
        "total": fraction_text(total),
        "published": PUBLISHED_REMAINDER_CONSTANT,
        "strict_margin": fraction_text(Fraction(PUBLISHED_REMAINDER_CONSTANT) - total),
        "all_pass": all_pass,
    }


def _finite_h_loss(next_y: int, endpoint_y: int) -> Fraction:
    if next_y > endpoint_y:
        raise ValueError("H tail starts beyond the endpoint")
    if next_y == endpoint_y:
        return Fraction(0)
    weights = tail_weights(next_y, endpoint_y)
    return Fraction(1) - _fraction_product(tuple(Fraction(1) - value for value in weights))


def finite_gap_row(start_y: int, endpoint_y: int) -> dict[str, object]:
    weights = tail_weights(start_y, endpoint_y)
    primes = first_odd_primes(endpoint_y)
    gap_pi2 = Fraction(0)
    for offset, weight in enumerate(weights):
        j = start_y + offset
        if weight != prime_square_weight(primes[j]):
            raise AssertionError("tail indexing drifted")
        gap_pi2 += 2 * weight * normalized_x(j)
        gap_pi2 += 4 * weight * normalized_memory(j) * _finite_h_loss(j + 1, endpoint_y)
    total = sum(weights, Fraction(0))
    square = sum((weight * weight for weight in weights), Fraction(0))
    coefficients = endpoint_coefficients(endpoint_y)
    approximation_pi2 = (
        2 * coefficients["X"] * total
        + (coefficients["Y"] + 2 * coefficients["m"]) * total * total
        + (coefficients["Y"] - 2 * coefficients["m"]) * square
    )
    residual = gap_pi2 - approximation_pi2
    strong_bound = TOTAL_REMAINDER_CONSTANT * total**3
    published_bound = PUBLISHED_REMAINDER_CONSTANT * total**3
    return {
        "start_y": start_y,
        "endpoint_y": endpoint_y,
        "tail_count": len(weights),
        "T": fraction_text(total),
        "S": fraction_text(square),
        "X_endpoint": fraction_text(coefficients["X"]),
        "Y_endpoint": fraction_text(coefficients["Y"]),
        "m_endpoint": fraction_text(coefficients["m"]),
        "gap_pi2": fraction_text(gap_pi2),
        "approximation_pi2": fraction_text(approximation_pi2),
        "residual_pi2": fraction_text(residual),
        "strong_bound_pi2": fraction_text(strong_bound),
        "published_bound_pi2": fraction_text(published_bound),
        "strong_bound_pass": abs(residual) <= strong_bound,
        "published_bound_pass": abs(residual) <= published_bound,
        "reproduction_only": True,
        "all_pass": abs(residual) <= strong_bound < published_bound,
    }


def one_tail_sign_mutation() -> dict[str, object]:
    row = finite_gap_row(WITNESS_START_Y, WITNESS_ENDPOINT_Y)
    primes = first_odd_primes(WITNESS_ENDPOINT_Y)
    if primes[-1] != WITNESS_PRIME or row["tail_count"] != 1:
        raise AssertionError("the one-tail witness is not the p=71 transition")
    a = prime_square_weight(WITNESS_PRIME)
    coefficients = endpoint_coefficients(WITNESS_ENDPOINT_Y)
    gap = Fraction(row["gap_pi2"])
    correct = Fraction(row["approximation_pi2"])
    wrong = (
        2 * coefficients["X"] * a
        + (coefficients["Y"] + 2 * coefficients["m"]) * a * a
        + (coefficients["Y"] + 2 * coefficients["m"]) * a * a
    )
    correct_residual = gap - correct
    wrong_residual = gap - wrong
    bound = PUBLISHED_REMAINDER_CONSTANT * a**3
    correct_ratio = abs(correct_residual) / bound
    wrong_ratio = abs(wrong_residual) / bound
    sign_difference = wrong - correct
    if sign_difference != 4 * coefficients["m"] * a * a:
        raise AssertionError("memory S-sign mutation is not exactly 4*m*S")
    return {
        "prime": WITNESS_PRIME,
        "start_y": WITNESS_START_Y,
        "endpoint_y": WITNESS_ENDPOINT_Y,
        "a": fraction_text(a),
        "T": fraction_text(a),
        "S": fraction_text(a * a),
        "m_endpoint": fraction_text(coefficients["m"]),
        "mutation": "replace the theorem memory coefficient -2*m_endpoint*S by +2*m_endpoint*S; numerator +Y*S is unchanged",
        "correct_residual_pi2": fraction_text(correct_residual),
        "wrong_residual_pi2": fraction_text(wrong_residual),
        "bound_551_T3_pi2": fraction_text(bound),
        "correct_ratio_exact": fraction_text(correct_ratio),
        "wrong_ratio_exact": fraction_text(wrong_ratio),
        "correct_ratio_15dp": fraction_decimal(correct_ratio),
        "wrong_ratio_15dp": fraction_decimal(wrong_ratio),
        "difference_exact": fraction_text(sign_difference),
        "difference_is_4mS": True,
        "correct_sign_pass": correct_ratio <= 1,
        "wrong_sign_rejected": wrong_ratio > 1,
        "reproduction_only": True,
        "all_pass": correct_ratio <= 1 < wrong_ratio,
    }


def terminal_ledger() -> dict[str, object]:
    rows = []
    for y in (1, 2, 3, 6):
        euler = finite_euler_values(y)
        runs = square_run_counts(y)
        parameters = square_parameters(y)
        terminal = _exact_integer(Fraction(parameters["P"]) * euler[8], "terminal R8")
        rows.append(
            {
                "y": y,
                "E9": fraction_text(euler[9]),
                "R8": runs[8],
                "P_times_E8": terminal,
                "E9_zero_pass": euler[9] == 0,
                "terminal_R8_pass": runs[8] == terminal,
                "all_pass": euler[9] == 0 and runs[8] == terminal,
            }
        )
    return {
        "construction": "R_ell=P(E_ell-2E_(ell+1)+E_(ell+2)) only for 1<=ell<=7; R8=P*E8 separately",
        "E10_constructed": False,
        "E9_reason": "E9=0 exactly because the p=3 Euler factor is 1-9/9",
        "rows": rows,
        "all_pass": all(row["all_pass"] for row in rows),
    }


def proof_ledger() -> dict[str, object]:
    return {
        "bonferroni": "T-T^2/2 <= 1-product(1-a) <= T for every finite tail, then monotone passage",
        "inverse_product": "0<=U-u-(m-1)uT<=U(m-1)^2T^2 with U<=(9-m)/8",
        "x_remainder": "abs(X_j-X_infinity-Y_infinity*T_j)<=931*T_j^2/4",
        "memory_convergence": "abs(M_j/A_j-m_infinity)<=63*T_j",
        "H_remainder": "if d=1-product(1-a), then abs(d-T)<=T^2/2",
        "quadratic_sums": "sum a*T_j=(T^2+S)/2 and sum a*T_(j+1)=(T^2-S)/2",
        "cube_telescope": "sum a*T_j*T_(j+1)=(T^3-sum a^3)/3; sum a*T_(j+1)^2<=T^3/3",
        "budget": "931/2+254/3=3301/6<551",
        "all_y_symbolic_not_fitted": True,
    }


def verify_certificate() -> dict[str, object]:
    product_rows = [
        product_expansion_row(m, start_y, endpoint_y)
        for start_y, endpoint_y in FINITE_GAP_CASES
        for m in range(3, 9)
    ]
    bonferroni_rows = [bonferroni_product(tail_weights(start, endpoint)) for start, endpoint in FINITE_GAP_CASES]
    tail_rows = [exact_tail_algebra(tail_weights(start, endpoint)) for start, endpoint in FINITE_GAP_CASES]
    gap_rows = [finite_gap_row(start, endpoint) for start, endpoint in FINITE_GAP_CASES]
    ledger = coefficient_ledger()
    terminal = terminal_ledger()
    mutation = one_tail_sign_mutation()
    all_pass = (
        all(row["all_pass"] for row in product_rows)
        and all(row["all_pass"] for row in bonferroni_rows)
        and all(row["all_pass"] for row in tail_rows)
        and all(row["all_pass"] for row in gap_rows)
        and ledger["all_pass"]
        and terminal["all_pass"]
        and mutation["all_pass"]
    )
    payload = {
        "product_expansion_rows": product_rows,
        "bonferroni_rows": bonferroni_rows,
        "tail_algebra_rows": tail_rows,
        "finite_gap_rows": gap_rows,
        "coefficient_ledger": ledger,
        "terminal_ledger": terminal,
        "one_tail_sign_mutation": mutation,
        "proof_ledger": proof_ledger(),
        "claim_boundary": {
            "fixed_finite_q_before_N_limit": True,
            "universally_safe_phasewise_c11_zero_only": True,
            "finite_rows_are_reproduction_only": True,
            "no_PNT_or_p_y_rewrite": True,
            "no_growing_clock_or_adaptive_capacity": True,
            "no_active_c11_theorem": True,
            "no_operator_trace_zeros_or_RH": True,
            "gates_A_through_E": [False, False, False, False, False],
        },
        "all_pass": all_pass,
    }
    if len(canonical_json_bytes(payload)) != CERTIFICATE_FIXTURE_BYTES:
        raise AssertionError("canonical RH-382 certificate byte count drifted")
    if payload_sha256(payload) != CERTIFICATE_FIXTURE_SHA256:
        raise AssertionError("canonical RH-382 certificate digest drifted")
    return payload
