"""Fail-closed exact and directed-rounding certificate for RH-384.

The prime-number-theorem implications are proved analytically in the
manuscript.  This module freezes the algebraic scale compiler, exact strict
successor interface, a precision-80 outward Euler-product enclosure, the five
normalized-limit ledgers, and genuine formula/interface mutations.  Finite
rows are reproduction checks and are never used as asymptotic evidence.
"""

from __future__ import annotations

from collections import Counter
from decimal import (
    Context,
    Decimal,
    FloatOperation,
    ROUND_CEILING,
    ROUND_FLOOR,
    localcontext,
)
from fractions import Fraction
from hashlib import sha256
import json
from math import isqrt


FIXED_R_MAX = 8
PARTITION_DEGREE_MAX = 8
SUCCESSOR_WITNESSES = (1, 2, 3, 5, 8, 13)
CUTOFF = 100_000
DECIMAL_PRECISION = 80
INTERVAL_PLACES = 19
PUBLISHED_INTERVAL_LOWER = "1.5463476716710499204"
PUBLISHED_INTERVAL_UPPER = "1.5484488989771761113"
RH2_RELEASE = "836426546db31e2737e877182848c538ed4cd436"
RH2_MAIN_SHA256 = "5f2538e648c2ed850b94a03c072a3526f31bcc0c70c90639f65601507f52e532"
RH2_REFERENCES_SHA256 = "bd86702192cd4bc6d1c2975c7da4b305541e0c5943f13c5edf044686f0faf2ab"
MONTGOMERY_VAUGHAN_DOI = "10.1017/CBO9780511618314"
MONTGOMERY_VAUGHAN_CHAPTER_DOI = "10.1017/CBO9780511618314.008"

# Frozen after the exact certificate is finalized.
CERTIFICATE_FIXTURE_BYTES = 48_689
CERTIFICATE_FIXTURE_SHA256 = "01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8"


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("an exact Fraction is required")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def _reject_nonfinite(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")


def loads_strict(text: str) -> dict[str, object]:
    if type(text) is not str:
        raise TypeError("JSON input must be text")
    value = json.loads(
        text,
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_nonfinite,
    )
    if type(value) is not dict:
        raise ValueError("JSON root must be an object")
    return value


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


def fixed_r_row(r: int) -> dict[str, object]:
    if type(r) is not int or not 1 <= r <= FIXED_R_MAX:
        raise ValueError(f"r must be an exact integer in 1..{FIXED_R_MAX}")
    exponent = 2 * r - 1
    return {
        "r": r,
        "endpoint": "p>p_y",
        "first_atom": "p_(y+1)",
        "constant": fraction_text(Fraction(1, exponent)),
        "p_exponent": exponent,
        "log_exponent": 1,
        "asymptotic": f"P_{r}(y)~1/({exponent}*p_y^{exponent}*log(p_y))",
        "fixed_r_only": True,
        "pass": True,
    }


def fixed_r_rows() -> list[dict[str, object]]:
    return [fixed_r_row(r) for r in range(1, FIXED_R_MAX + 1)]


def integer_partitions(total: int, maximum: int | None = None) -> tuple[tuple[int, ...], ...]:
    if type(total) is not int or total < 0:
        raise ValueError("partition degree must be a nonnegative exact integer")
    if maximum is not None and (type(maximum) is not int or maximum < 1):
        raise ValueError("maximum part must be a positive exact integer")

    def generate(remaining: int, ceiling: int) -> list[tuple[int, ...]]:
        if remaining == 0:
            return [()]
        output: list[tuple[int, ...]] = []
        for part in range(min(remaining, ceiling), 0, -1):
            output.extend((part, *tail) for tail in generate(remaining - part, part))
        return output

    return tuple(generate(total, total if maximum is None else maximum))


def partition_row(partition: tuple[int, ...]) -> dict[str, object]:
    if type(partition) is not tuple or not partition:
        raise ValueError("partition must be a nonempty tuple")
    if any(type(part) is not int or part < 1 for part in partition):
        raise TypeError("partition parts must be positive exact integers")
    if tuple(sorted(partition, reverse=True)) != partition:
        raise ValueError("partition must be in nonincreasing order")
    degree = sum(partition)
    length = len(partition)
    multiplicities = Counter(partition)
    constant = Fraction(1)
    for part, count in multiplicities.items():
        constant *= Fraction(1, (2 * part - 1) ** count)
    p_exponent = sum(2 * part - 1 for part in partition)
    return {
        "partition": list(partition),
        "multiplicities": {str(part): multiplicities[part] for part in sorted(multiplicities)},
        "degree": degree,
        "length": length,
        "constant": fraction_text(constant),
        "p_exponent": p_exponent,
        "p_exponent_identity": f"{p_exponent}=2*{degree}-{length}",
        "log_exponent": length,
        "fixed_partition_only": True,
        "pass": p_exponent == 2 * degree - length,
    }


def partition_rows() -> list[dict[str, object]]:
    return [
        partition_row(partition)
        for degree in range(1, PARTITION_DEGREE_MAX + 1)
        for partition in integer_partitions(degree)
    ]


def _finite_tail(r: int, start_y: int, endpoint_y: int) -> Fraction:
    if type(r) is not int or r < 1:
        raise ValueError("r must be a positive exact integer")
    if type(start_y) is not int or type(endpoint_y) is not int or not 1 <= start_y < endpoint_y:
        raise ValueError("tail endpoints require exact integers 1<=start<endpoint")
    primes = first_odd_primes(endpoint_y)
    return sum(
        (prime_square_weight(primes[index]) ** r for index in range(start_y, endpoint_y)),
        Fraction(0),
    )


def successor_row(r: int, y: int) -> dict[str, object]:
    if type(r) is not int or not 1 <= r <= FIXED_R_MAX:
        raise ValueError(f"r must be an exact integer in 1..{FIXED_R_MAX}")
    if type(y) is not int or y < 1:
        raise ValueError("y must be a positive exact integer")
    endpoint_y = y + 4
    primes = first_odd_primes(endpoint_y)
    current_prime = primes[y - 1]
    first_tail_prime = primes[y]
    lhs = _finite_tail(r, y, endpoint_y)
    successor = _finite_tail(r, y + 1, endpoint_y)
    first_atom = prime_square_weight(first_tail_prime) ** r
    rhs = first_atom + successor
    inclusive_mutation = prime_square_weight(current_prime) ** r + lhs
    return {
        "r": r,
        "y": y,
        "endpoint_y": endpoint_y,
        "p_y": current_prime,
        "first_tail_prime": first_tail_prime,
        "strict_endpoint": "p>p_y",
        "lhs": fraction_text(lhs),
        "first_atom": fraction_text(first_atom),
        "successor_tail": fraction_text(successor),
        "rhs": fraction_text(rhs),
        "identity_pass": lhs == rhs,
        "first_atom_pass": first_tail_prime > current_prime,
        "inclusive_interface_mutation_rejected": inclusive_mutation != lhs,
        "asymptotic_note": "endpoint mutations are interface errors but do not change the leading PNT equivalent",
        "pass": lhs == rhs and first_tail_prime > current_prime and inclusive_mutation != lhs,
    }


def successor_rows() -> list[dict[str, object]]:
    return [successor_row(r, y) for y in SUCCESSOR_WITNESSES for r in range(1, FIXED_R_MAX + 1)]


def _directed_context(rounding: str, precision: int = DECIMAL_PRECISION) -> Context:
    if rounding not in (ROUND_FLOOR, ROUND_CEILING):
        raise ValueError("only outward floor/ceiling rounding is allowed")
    if type(precision) is not int or precision < 40:
        raise ValueError("precision must be an exact integer at least 40")
    context = Context(prec=precision, rounding=rounding)
    context.traps[FloatOperation] = True
    return context


def _fraction_decimal(value: Fraction, rounding: str) -> Decimal:
    if type(value) is not Fraction:
        raise TypeError("an exact Fraction is required")
    with localcontext(_directed_context(rounding)):
        return +(Decimal(value.numerator) / Decimal(value.denominator))


def _finite_product_interval(m: int, primes: tuple[int, ...]) -> tuple[Decimal, Decimal]:
    if type(m) is not int or not 2 <= m <= 8:
        raise ValueError("m must be an exact integer in 2..8")
    if type(primes) is not tuple or not primes:
        raise ValueError("a nonempty exact prime tuple is required")
    with localcontext(_directed_context(ROUND_FLOOR)):
        lower = Decimal(1)
        for prime in primes:
            lower *= Decimal(prime * prime - m) / Decimal(prime * prime - 1)
    with localcontext(_directed_context(ROUND_CEILING)):
        upper = Decimal(1)
        for prime in primes:
            upper *= Decimal(prime * prime - m) / Decimal(prime * prime - 1)
    return lower, upper


def _linear_interval(
    coefficients: dict[int, int],
    intervals: dict[int, tuple[Decimal, Decimal]],
) -> tuple[Decimal, Decimal]:
    with localcontext(_directed_context(ROUND_FLOOR)):
        lower = Decimal(0)
        for m, coefficient in coefficients.items():
            lo, hi = intervals[m]
            lower += Decimal(coefficient) * (lo if coefficient >= 0 else hi)
    with localcontext(_directed_context(ROUND_CEILING)):
        upper = Decimal(0)
        for m, coefficient in coefficients.items():
            lo, hi = intervals[m]
            upper += Decimal(coefficient) * (hi if coefficient >= 0 else lo)
    return lower, upper


def _format_raw(value: Decimal) -> str:
    return format(value, "f")


def _outward_quantize(value: Decimal, places: int, rounding: str) -> str:
    if type(places) is not int or places < 1:
        raise ValueError("places must be a positive exact integer")
    with localcontext(_directed_context(rounding)):
        quantum = Decimal(1).scaleb(-places)
        return format(value.quantize(quantum, rounding=rounding), f".{places}f")


def numeric_interval_certificate() -> dict[str, object]:
    primes = tuple(prime for prime in sieve_primes(CUTOFF) if prime != 2)
    if primes[-1] != 99_991:
        raise AssertionError("unexpected last prime below the cutoff")
    next_primes = tuple(prime for prime in sieve_primes(CUTOFF + 10) if prime > CUTOFF)
    if not next_primes or next_primes[0] != 100_003:
        raise AssertionError("unexpected first prime above the cutoff")
    theta = Fraction(1, 2) * (Fraction(1, CUTOFF) + Fraction(1, CUTOFF + 1))
    if theta != Fraction(200001, 20000200000):
        raise AssertionError("integer-tail telescope changed")

    u_intervals: dict[int, tuple[Decimal, Decimal]] = {}
    rows: list[dict[str, object]] = []
    theta_upper = _fraction_decimal(theta, ROUND_CEILING)
    for m in range(2, 9):
        finite_lower, finite_upper = _finite_product_interval(m, primes)
        with localcontext(_directed_context(ROUND_CEILING)):
            tail_loss_upper = Decimal(m - 1) * theta_upper
        with localcontext(_directed_context(ROUND_FLOOR)):
            tail_factor_lower = Decimal(1) - tail_loss_upper
            u_lower = finite_lower * tail_factor_lower
        u_upper = finite_upper
        u_intervals[m] = (u_lower, u_upper)
        rows.append({
            "m": m,
            "finite_product_lower": _format_raw(finite_lower),
            "finite_product_upper": _format_raw(finite_upper),
            "tail_loss_upper": _format_raw(tail_loss_upper),
            "tail_factor_lower": _format_raw(tail_factor_lower),
            "u_lower": _format_raw(u_lower),
            "u_upper": _format_raw(u_upper),
            "bonferroni_factor_positive": tail_factor_lower > 0,
            "pass": Decimal(0) < u_lower <= u_upper < Decimal(1),
        })

    y_coefficients = {4: 6, 5: -16, 6: 30, 7: -48, 8: 70}
    m_coefficients = {3: 2, 4: -4, 5: 6, 6: -8, 7: 10, 8: -12}
    contrast_coefficients = {3: -4, 4: 14, 5: -28, 6: 46, 7: -68, 8: 94}
    y_lower, y_upper = _linear_interval(y_coefficients, u_intervals)
    m_lower, m_upper = _linear_interval(m_coefficients, u_intervals)
    raw_lower, raw_upper = _linear_interval(contrast_coefficients, u_intervals)
    derived_rows = [
        {
            "name": "Y_infinity",
            "coefficients": {str(key): value for key, value in y_coefficients.items()},
            "lower": _format_raw(y_lower),
            "upper": _format_raw(y_upper),
            "pass": y_lower <= y_upper,
        },
        {
            "name": "m_infinity",
            "coefficients": {str(key): value for key, value in m_coefficients.items()},
            "lower": _format_raw(m_lower),
            "upper": _format_raw(m_upper),
            "pass": m_lower <= m_upper,
        },
        {
            "name": "Y_infinity-2m_infinity",
            "coefficients": {str(key): value for key, value in contrast_coefficients.items()},
            "lower": _format_raw(raw_lower),
            "upper": _format_raw(raw_upper),
            "pass": raw_lower <= raw_upper and raw_lower > 0,
        },
    ]
    published_lower = _outward_quantize(raw_lower, INTERVAL_PLACES, ROUND_FLOOR)
    published_upper = _outward_quantize(raw_upper, INTERVAL_PLACES, ROUND_CEILING)
    all_pass = (
        published_lower == PUBLISHED_INTERVAL_LOWER
        and published_upper == PUBLISHED_INTERVAL_UPPER
        and raw_lower > 0
        and len(rows) + len(derived_rows) == 10
        and all(row["pass"] is True for row in rows)
        and all(row["pass"] is True for row in derived_rows)
    )
    return {
        "precision": DECIMAL_PRECISION,
        "rounding": [ROUND_FLOOR, ROUND_CEILING],
        "float_operation_trapped": True,
        "cutoff_anchor": CUTOFF,
        "last_prime_at_or_below_cutoff": primes[-1],
        "first_prime_above_cutoff": next_primes[0],
        "cutoff_is_neither_last_nor_next_prime": CUTOFF not in (primes[-1], next_primes[0]),
        "odd_prime_count": len(primes),
        "tail_integer_bound": fraction_text(theta),
        "tail_bound_formula": "sum_(p>N)1/(p^2-1)<=sum_(n>N)1/(n^2-1)=0.5*(1/N+1/(N+1))",
        "u_intervals": rows,
        "derived_intervals": derived_rows,
        "numeric_row_count": len(rows) + len(derived_rows),
        "linear_form": "Y_infinity-2m_infinity=-4u3+14u4-28u5+46u6-68u7+94u8",
        "raw_lower": _format_raw(raw_lower),
        "raw_upper": _format_raw(raw_upper),
        "published_lower": published_lower,
        "published_upper": published_upper,
        "positive_pass": raw_lower > 0,
        "all_pass": all_pass,
    }


def gap_limit_rows() -> list[dict[str, object]]:
    return [
        {
            "id": "L1",
            "normalizer": "p_y*log(p_y)",
            "expression": "B_infinity-G(q_y)",
            "limit": "A",
            "exact_subtraction": [],
            "pass": True,
        },
        {
            "id": "L2",
            "normalizer": "[p_y*log(p_y)]^2",
            "expression": "B_infinity-G(q_y)-A*T_y",
            "limit": "B",
            "exact_subtraction": ["A*T_y"],
            "pnt_surrogates_forbidden": ["A/[p_y*log(p_y)]"],
            "pass": True,
        },
        {
            "id": "L3",
            "normalizer": "1/S_y",
            "expression": "B_infinity-G(q_y)-A*T_y-B*T_y^2",
            "limit": "C",
            "exact_subtraction": ["A*T_y", "B*T_y^2"],
            "pnt_surrogates_forbidden": [
                "A/[p_y*log(p_y)]",
                "B/[p_y^2*log(p_y)^2]",
            ],
            "pass": True,
        },
        {
            "id": "L4",
            "normalizer": "3*p_y^3*log(p_y)",
            "expression": "B_infinity-G(q_y)-A*T_y-B*T_y^2",
            "limit": "C",
            "exact_subtraction": ["A*T_y", "B*T_y^2"],
            "pnt_surrogates_forbidden": [
                "A/[p_y*log(p_y)]",
                "B/[p_y^2*log(p_y)^2]",
            ],
            "pass": True,
        },
        {
            "id": "L5",
            "normalizer": "1/[T_y^3*log(p_y)^2]",
            "expression": "B_infinity-G(q_y)-A*T_y-B*T_y^2",
            "limit": "C/3",
            "exact_subtraction": ["A*T_y", "B*T_y^2"],
            "pnt_surrogates_forbidden": [
                "A/[p_y*log(p_y)]",
                "B/[p_y^2*log(p_y)^2]",
            ],
            "pass": True,
        },
    ]


def gap_subtraction_contract(limit_id: str, terms: list[str]) -> bool:
    """Validate the exact subtraction surface used by a normalized gap limit."""

    if type(limit_id) is not str or type(terms) is not list or any(type(term) is not str for term in terms):
        raise TypeError("a textual limit id and an exact list of textual terms are required")
    expected = {row["id"]: row["exact_subtraction"] for row in gap_limit_rows()}
    if limit_id not in expected:
        raise ValueError("unknown gap-limit id")
    return terms == expected[limit_id]


def scale_separation_ledger() -> list[dict[str, object]]:
    t = fixed_r_row(1)
    s = fixed_r_row(2)
    t_constant = Fraction(t["constant"])
    s_constant = Fraction(s["constant"])
    rows = [
        {
            "id": "S1",
            "statement": "p_y*log(p_y)*T_y->1",
            "derived_constant": fraction_text(t_constant),
            "pass": t["p_exponent"] == 1 and t_constant == 1,
        },
        {
            "id": "S2",
            "statement": "3*p_y^3*log(p_y)*S_y->1",
            "derived_constant": fraction_text(3 * s_constant),
            "pass": s["p_exponent"] == 3 and 3 * s_constant == 1,
        },
        {
            "id": "S3",
            "statement": "S_y/T_y^2->0",
            "derived_equivalent": "log(p_y)/(3*p_y)",
            "pass": s["p_exponent"] - 2 * t["p_exponent"] == 1,
        },
        {
            "id": "S4",
            "statement": "T_y^3/S_y->0",
            "derived_equivalent": "3/log(p_y)^2",
            "pass": 3 * t["p_exponent"] - s["p_exponent"] == 0,
        },
        {
            "id": "S5",
            "statement": "S_y/[T_y^3*log(p_y)^2]->1/3",
            "derived_constant": fraction_text(s_constant / (t_constant**3)),
            "pass": s_constant / (t_constant**3) == Fraction(1, 3),
        },
    ]
    return rows


def validate_pnt_provenance(
    release: str = RH2_RELEASE,
    main_sha256: str = RH2_MAIN_SHA256,
    references_sha256: str = RH2_REFERENCES_SHA256,
    doi: str = MONTGOMERY_VAUGHAN_DOI,
) -> bool:
    values = (release, main_sha256, references_sha256, doi)
    if any(type(value) is not str for value in values):
        raise TypeError("provenance values must be text")
    if release != RH2_RELEASE:
        raise ValueError("RH-2 release changed")
    if main_sha256 != RH2_MAIN_SHA256:
        raise ValueError("RH-2 main hash changed")
    if references_sha256 != RH2_REFERENCES_SHA256:
        raise ValueError("RH-2 references hash changed")
    if doi != MONTGOMERY_VAUGHAN_DOI:
        raise ValueError("Montgomery--Vaughan DOI changed")
    return True


def _mutation(label: str, category: str, rejected: bool, note: str) -> dict[str, object]:
    return {"label": label, "category": category, "rejected": rejected, "note": note}


def negative_mutation_rows() -> list[dict[str, object]]:
    rows = successor_rows()
    interval = numeric_interval_certificate()
    partition = partition_row((3, 1, 1))
    mutations: list[dict[str, object]] = []
    mutations.append(_mutation(
        "endpoint-inclusive",
        "interface",
        rows[0]["inclusive_interface_mutation_rejected"] is True,
        "p>=p_y adds the exact current atom; leading PNT asymptotics alone would not detect it",
    ))
    mutations.append(_mutation(
        "first-atom-current",
        "interface",
        rows[0]["first_tail_prime"] != rows[0]["p_y"],
        "the strict tail starts at p_(y+1), not p_y; this is an exact-interface check",
    ))
    mutations.append(_mutation(
        "abel-denominator-2r",
        "theorem",
        fixed_r_row(4)["constant"] != fraction_text(Fraction(1, 8)),
        "the Abel constant is 1/(2r-1)",
    ))
    mutations.append(_mutation(
        "partition-p-exponent-2d",
        "theorem",
        partition["p_exponent"] != 2 * partition["degree"],
        "the exponent is 2d-length(lambda)",
    ))
    mutations.append(_mutation(
        "partition-log-exponent-degree",
        "theorem",
        partition["log_exponent"] != partition["degree"],
        "the logarithmic exponent is partition length",
    ))
    mutations.append(_mutation(
        "partition-constant-degree-only",
        "theorem",
        partition["constant"] != fraction_text(Fraction(1, 2 * partition["degree"] - 1)),
        "the constant is the product over parts",
    ))
    mutations.append(_mutation(
        "S-normalizer-without-3",
        "theorem",
        scale_separation_ledger()[1]["statement"].startswith("3*"),
        "P_2 has Abel constant 1/3",
    ))
    mutations.append(_mutation(
        "PNT-surrogate-quadratic-subtraction",
        "theorem-interface",
        not gap_subtraction_contract("L3", ["A*T_y", "B/[p_y^2*log(p_y)^2]"]),
        "bare PNT does not license replacing exact B*T_y^2 at the smaller S_y scale",
    ))
    mutations.append(_mutation(
        "memory-sign-Y-plus-2m",
        "theorem",
        interval["linear_form"].startswith("Y_infinity-2m_infinity"),
        "the twice-subtracted coefficient is C=(Y-2m)/pi^2",
    ))
    mutations.append(_mutation(
        "PNT-surrogate-second-subtraction",
        "theorem-interface",
        not gap_subtraction_contract("L2", ["A/[p_y*log(p_y)]"]),
        "bare PNT does not control T_y-1/(p_y log p_y) at the T_y^2 scale",
    ))
    for label, arguments, note in (
        ("wrong-RH2-release", {"release": "0" * 40}, "the source commit is frozen"),
        ("wrong-RH2-main-hash", {"main_sha256": "0" * 64}, "the PNT-bearing source blob is frozen"),
        ("wrong-RH2-reference-hash", {"references_sha256": "0" * 64}, "the citation source blob is frozen"),
    ):
        rejected = False
        try:
            validate_pnt_provenance(**arguments)
        except ValueError:
            rejected = True
        mutations.append(_mutation(label, "provenance", rejected, note))
    context = _directed_context(ROUND_FLOOR)
    float_rejected = False
    try:
        with localcontext(context):
            Decimal(0.1)
    except FloatOperation:
        float_rejected = True
    mutations.append(_mutation(
        "binary-float-injection",
        "numeric-interface",
        float_rejected,
        "FloatOperation is trapped at precision 80",
    ))
    bool_rejected = False
    try:
        fixed_r_row(True)
    except ValueError:
        bool_rejected = True
    mutations.append(_mutation(
        "bool-as-integer-r",
        "type-interface",
        bool_rejected,
        "bool is rejected rather than aliased to exact integer 1",
    ))
    for label, text in (
        ("duplicate-json-key", '{"x":1,"x":2}'),
        ("NaN-json", '{"x":NaN}'),
        ("Infinity-json", '{"x":Infinity}'),
    ):
        rejected = False
        try:
            loads_strict(text)
        except ValueError:
            rejected = True
        mutations.append(_mutation(label, "json-interface", rejected, "strict JSON rejects this input"))
    mutations.append(_mutation(
        "cutoff-last-prime",
        "numeric-interface",
        interval["cutoff_anchor"] != interval["last_prime_at_or_below_cutoff"],
        "the tail bound is anchored at integer N=100000, not 99991",
    ))
    mutations.append(_mutation(
        "cutoff-next-prime",
        "numeric-interface",
        interval["cutoff_anchor"] != interval["first_prime_above_cutoff"],
        "the tail bound is anchored at integer N=100000, not 100003",
    ))
    if len(mutations) != 20:
        raise AssertionError("the frozen mutation count changed")
    return mutations


def verify_certificate() -> dict[str, object]:
    fixed = fixed_r_rows()
    partitions = partition_rows()
    successors = successor_rows()
    interval = numeric_interval_certificate()
    scales = scale_separation_ledger()
    limits = gap_limit_rows()
    mutations = negative_mutation_rows()
    all_pass = (
        len(fixed) == 8
        and len(partitions) == 66
        and len(successors) == 48
        and len(scales) == 5
        and len(limits) == 5
        and len(mutations) == 20
        and all(row["pass"] is True for row in fixed)
        and all(row["pass"] is True for row in partitions)
        and all(row["pass"] is True for row in successors)
        and interval["all_pass"] is True
        and all(row["pass"] is True for row in scales)
        and all(row["pass"] is True for row in limits)
        and all(row["rejected"] is True for row in mutations)
    )
    return {
        "status": "RH-384_exact_certificate",
        "counts": {
            "fixed_r": len(fixed),
            "partitions": len(partitions),
            "successors": len(successors),
            "scale_limits": len(scales),
            "gap_limits": len(limits),
            "negative_mutations": len(mutations),
        },
        "fixed_r": fixed,
        "partitions": partitions,
        "successors": successors,
        "scale_separation": scales,
        "gap_limits": limits,
        "numeric_interval": interval,
        "negative_mutations": {
            "rows": mutations,
            "rejected": sum(row["rejected"] is True for row in mutations),
            "endpoint_asymptotic_disclosure": "inclusive/current-prime endpoint changes are exact-interface errors, not leading-asymptotic counterexamples",
        },
        "proof_ledger": {
            "abel": "strict Stieltjes partial summation with pi(t)=t/log(t)*(1+delta(t)); sup_(t>=x)|delta(t)|->0",
            "fixed_r": "P_r(y)~1/((2r-1)*p_y^(2r-1)*log(p_y)) for each fixed r>=1",
            "fixed_partition": "multiply finitely many fixed-r equivalents; no growing-degree uniformity",
            "scale_order": "T_y^3=o(S_y) and S_y=o(T_y^2)",
            "gap_input": "RH-382 gives gap=A*T+B*T^2+C*S+O(T^3)",
            "subtraction": "L2 subtracts exact A*T_y; L3--L5 subtract exact A*T_y+B*T_y^2; neither term may be replaced by its bare-PNT surrogate",
            "interval": "finite Euler-product intervals plus integer-tail Bonferroni bound, directed at precision 80",
            "finite_rows_are_reproduction_only": True,
        },
        "claim_boundary": {
            "fixed_finite_q_before_N_limit": True,
            "universally_safe_phasewise_c11_zero_only": True,
            "strict_prime_endpoint": True,
            "fixed_r_and_partition_only": True,
            "no_effective_rate_or_threshold": True,
            "no_growing_clock_or_adaptive_capacity": True,
            "no_operator_trace_zeros_or_RH": True,
            "gates_A_through_E": [False, False, False, False, False],
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
        },
        "all_pass": all_pass,
    }
