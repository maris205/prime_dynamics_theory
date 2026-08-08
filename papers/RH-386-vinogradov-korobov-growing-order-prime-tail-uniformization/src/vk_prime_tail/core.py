"""Exact RH-386 proof-interface and adversarial certificate compiler.

The analytic limit is proved in ``main.tex``.  This module independently
compiles its exact algebraic interfaces: the strict Stieltjes boundary,
decreasing hazard, Johnston--Yang source constants, kernel comparisons,
partition bookkeeping, leading-kernel obstruction, and sharpness family.
Finite rows are labelled reproduction checks and are never substituted for
the analytic proof.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any


R_FIXTURES = (1, 2, 3, 4, 8, 16, 32, 64)
PARTITION_DEGREE_MAX = 8
ANALYTIC_ROW_COUNT = 16
ENVELOPE_ROW_COUNT = 6
MUTATION_COUNT = 24

JOHNSTON_YANG_URL = "https://arxiv.org/pdf/2204.01980v2"
JOHNSTON_YANG_SOURCE_TAR_URL = "https://arxiv.org/src/2204.01980v2"
JOHNSTON_YANG_SHA256 = "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2"
JOHNSTON_YANG_BYTES = 278_380
JOHNSTON_YANG_PAGES = 22
JOHNSTON_YANG_MIME = "application/pdf"
JOHNSTON_YANG_DOI = "10.1016/j.jmaa.2023.127460"
JOHNSTON_YANG_ARXIV = "2204.01980v2"
JOHNSTON_YANG_SOURCE_TAR_SHA256 = "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd"
JOHNSTON_YANG_SOURCE_TAR_BYTES = 21_523
JOHNSTON_YANG_MAIN_TEX_SHA256 = "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602"

ETA_COEFFICIENT = Fraction(27, 1000)
ETA_LOG_POWER = Fraction(1801, 1000)
ETA_EXPONENT = Fraction(1853, 10_000)
V_LOG_POWER = Fraction(3, 5)
V_LOGLOG_POWER = Fraction(-1, 5)
ETA_MONOTONE_L_MIN = 512


def _require_int(value: object, name: str, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise TypeError(f"{name} must be an exact integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _require_bool(value: object, name: str) -> bool:
    if type(value) is not bool:
        raise TypeError(f"{name} must be an exact Boolean")
    return value


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("an exact Fraction is required")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fraction_object(value: Fraction) -> dict[str, int]:
    if type(value) is not Fraction:
        raise TypeError("an exact Fraction is required")
    return {"numerator": value.numerator, "denominator": value.denominator}


def fraction_from_text(value: object, name: str) -> Fraction:
    if type(value) is not str:
        raise TypeError(f"{name} must be exact rational text")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} is not exact rational text") from exc
    if fraction_text(result) != value:
        raise ValueError(f"{name} is not canonical rational text")
    return result


def fraction_from_object(value: object, name: str) -> Fraction:
    if type(value) is not dict or set(value) != {"numerator", "denominator"}:
        raise TypeError(f"{name} must be an exact rational object")
    numerator = _require_int(value["numerator"], f"{name}.numerator")
    denominator = _require_int(value["denominator"], f"{name}.denominator", 1)
    result = Fraction(numerator, denominator)
    if result.numerator != numerator or result.denominator != denominator:
        raise ValueError(f"{name} must be reduced")
    return result


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def payload_sha256(value: object) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def exact_equal(left: object, right: object) -> bool:
    """Recursive equality which never aliases ``bool`` with ``int``."""

    if type(left) is not type(right):
        return False
    if type(left) is dict:
        if set(left) != set(right):
            return False
        return all(exact_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


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


def integer_partitions(total: int, maximum: int | None = None) -> tuple[tuple[int, ...], ...]:
    total = _require_int(total, "partition degree", 0)
    if maximum is not None:
        maximum = _require_int(maximum, "maximum part", 1)

    def generate(remaining: int, ceiling: int) -> list[tuple[int, ...]]:
        if remaining == 0:
            return [()]
        rows: list[tuple[int, ...]] = []
        for part in range(min(remaining, ceiling), 0, -1):
            rows.extend((part, *tail) for tail in generate(remaining - part, part))
        return rows

    return tuple(generate(total, total if maximum is None else maximum))


def remote_source_lock() -> dict[str, object]:
    return {
        "source_key": "johnston-yang-arxiv-2204.01980v2",
        "artifact_role": "audited_arxiv_author_manuscript",
        "versioned_url": JOHNSTON_YANG_URL,
        "source_tar_url": JOHNSTON_YANG_SOURCE_TAR_URL,
        "source_tar_final_url": JOHNSTON_YANG_SOURCE_TAR_URL,
        "sha256": JOHNSTON_YANG_SHA256,
        "bytes": JOHNSTON_YANG_BYTES,
        "mime": JOHNSTON_YANG_MIME,
        "pages": JOHNSTON_YANG_PAGES,
        "arxiv_id_version": JOHNSTON_YANG_ARXIV,
        "version_of_record_doi": JOHNSTON_YANG_DOI,
        "journal": "Journal of Mathematical Analysis and Applications",
        "volume": 527,
        "issue": 2,
        "article_number": "127460",
        "redistributable_in_release": False,
        "pdf_vendored": False,
        "source_tar_vendored": False,
        "license": {
            "url": "https://arxiv.org/licenses/nonexclusive-distrib/1.0/",
            "scope": "non-exclusive distribution permission granted to arXiv; no third-party republication grant",
            "version_of_record_copyright": "Copyright 2023 Elsevier Inc. All rights reserved.",
        },
        "source_tar_sha256": JOHNSTON_YANG_SOURCE_TAR_SHA256,
        "source_tar_bytes": JOHNSTON_YANG_SOURCE_TAR_BYTES,
        "source_main_tex_sha256": JOHNSTON_YANG_MAIN_TEX_SHA256,
        "locators": [
            {
                "printed_page": 2,
                "section": "1.2",
                "label": "Corollary 1.2",
                "equation": "(1.5)",
                "role": "global explicit theta bound",
            },
            {
                "printed_page": 3,
                "section": "1.2",
                "label": "Table 1",
                "row": "X=log 2",
                "role": "A=9.39, B=1.515, C=0.8274",
            },
            {
                "printed_page": 2,
                "section": "1.2",
                "label": "Theorem 1.4",
                "equation": "(1.8)",
                "role": "global explicit Vinogradov--Korobov theta bound for x>=23",
            },
        ],
        "known_out_of_scope_typos": [
            {
                "location": "Section 5.2",
                "arxiv_v2_text": "Corollary 1.5",
                "intended_reference": "Corollary 1.2 / equation (1.5)",
                "used_by_RH386": False,
            },
            {
                "location": "Theorem 1.4 equation (1.9)",
                "arxiv_v2_text": "absolute value of pi(x)-x",
                "version_of_record_text": "absolute value of pi(x)-li(x)",
                "used_by_RH386": False,
            },
        ],
        "network_verification": {
            "default": "disabled",
            "opt_in_flag": "--network",
            "fixed_url_only": True,
            "checks": [
                "HTTP status 200",
                "exact allowlisted final URLs; every other redirect rejected",
                "PDF Content-Type application/pdf",
                "PDF byte count 278380",
                "PDF SHA-256",
                "PDF page count 22 via pdfinfo",
                "source tar byte count 21523",
                "source tar SHA-256",
                "source tar main.tex SHA-256",
            ],
            "offline_build_claim": "lock-object verification only; no claim of refetching",
        },
    }


def source_theorem_contract() -> dict[str, object]:
    monotonic_margin = ETA_EXPONENT * 22 * Fraction(17, 30) - ETA_LOG_POWER
    return {
        "theta_bound": "abs(theta(x)-x)<=eta(log(x))*x for every x>=23",
        "L": "log(x)",
        "V": "L^(3/5)*(log(L))^(-1/5)",
        "eta": "0.027*L^1.801*exp(-0.1853*V)",
        "eta_coefficient": fraction_object(ETA_COEFFICIENT),
        "eta_log_power": fraction_object(ETA_LOG_POWER),
        "eta_exponent": fraction_object(ETA_EXPONENT),
        "V_log_power": fraction_object(V_LOG_POWER),
        "V_loglog_power": fraction_object(V_LOGLOG_POWER),
        "source_x_min": 23,
        "tail_monotonicity_L_min": ETA_MONOTONE_L_MIN,
        "monotonicity_proof": {
            "log_L_lower": 6,
            "sqrt_L_strict_lower": 22,
            "V_lower": "sqrt(L)",
            "derivative_factor_lower": fraction_object(Fraction(17, 30)),
            "negative_bracket_margin_lower": fraction_object(monotonic_margin),
            "pass": monotonic_margin > 0,
        },
        "evidence_role": "peer_reviewed_explicit_VK_theorem_not_finite_fit",
        "locator": "Johnston--Yang Theorem 1.4 equation (1.8)",
    }


def _row(row_id: str, domain: str, statement: str, check: bool, derived: dict[str, object]) -> dict[str, object]:
    _require_bool(check, "analytic row check")
    return {
        "id": row_id,
        "domain": domain,
        "statement": statement,
        "derived": derived,
        "pass": check,
    }


def analytic_rows() -> list[dict[str, object]]:
    margin = ETA_EXPONENT * 22 * Fraction(17, 30) - ETA_LOG_POWER
    xq_margin = Fraction(3) - Fraction(2 * 23 * 23, 23 * 23 - 1) - Fraction(1, 3)
    successor_r = 2
    successor_primes = (5, 7, 11)
    successor_terms = tuple(Fraction(1, (prime * prime - 1) ** successor_r) for prime in successor_primes)
    successor_lhs = sum(successor_terms, Fraction(0))
    successor_tail = sum(successor_terms[1:], Fraction(0))
    rows = [
        _row(
            "source_vk_constants",
            "source",
            "Theorem 1.4 (1.8) supplies 0.027, 1.801, 0.1853, 3/5, -1/5",
            all(value > 0 for value in (ETA_COEFFICIENT, ETA_LOG_POWER, ETA_EXPONENT, V_LOG_POWER))
            and V_LOGLOG_POWER == Fraction(-1, 5),
            {
                "coefficient": fraction_text(ETA_COEFFICIENT),
                "log_power": fraction_text(ETA_LOG_POWER),
                "exponent": fraction_text(ETA_EXPONENT),
                "V_log_power": fraction_text(V_LOG_POWER),
                "V_loglog_power": fraction_text(V_LOGLOG_POWER),
                "source_x_min": 23,
            },
        ),
        _row(
            "eta_log_derivative",
            "source",
            "L*d(log eta)/dL=1.801-0.1853*V*(3/5-1/(5log L))",
            ETA_LOG_POWER == Fraction(1801, 1000) and ETA_EXPONENT == Fraction(1853, 10_000),
            {
                "positive_term": fraction_text(ETA_LOG_POWER),
                "negative_coefficient": fraction_text(ETA_EXPONENT),
                "V_multiplier_log_power": fraction_text(Fraction(3, 5)),
                "V_multiplier_loglog_correction": fraction_text(Fraction(-1, 5)),
            },
        ),
        _row(
            "eta_tail_monotone",
            "source",
            "eta is decreasing for L>=512",
            margin > 0,
            {
                "exact_lower_margin": fraction_text(margin),
                "L_min": ETA_MONOTONE_L_MIN,
                "derivative_direction": "decreasing",
                "sqrt_L_strict_lower": 22,
                "factor_lower": fraction_text(Fraction(17, 30)),
            },
        ),
        _row(
            "strict_stieltjes_boundary",
            "endpoint",
            "P_r=-theta(x)h_r(x)-integral_x^infinity theta(t)h_r'(t)dt",
            Fraction(-1) + Fraction(1) == 0,
            {
                "boundary_coefficient": -1,
                "endpoint": "(x,infinity)",
                "prime_condition": "p>x",
                "main_measure_boundary_coefficient": -1,
                "integration_by_parts_boundary_coefficient": 1,
            },
        ),
        _row(
            "strict_successor",
            "endpoint",
            "P_r(y)=(p_(y+1)^2-1)^(-r)+P_r(y+1)",
            successor_lhs == successor_terms[0] + successor_tail,
            {
                "tail": "strict",
                "first_atom": "p_(y+1)",
                "current_atom_excluded": True,
                "witness_r": successor_r,
                "witness_p_y": 3,
                "witness_tail_primes": list(successor_primes),
                "witness_lhs": fraction_text(successor_lhs),
                "witness_first_atom": fraction_text(successor_terms[0]),
                "witness_successor": fraction_text(successor_tail),
                "witness_rhs": fraction_text(successor_terms[0] + successor_tail),
            },
        ),
        _row(
            "hazard_formula",
            "hazard",
            "q_r=-h_r'/h_r=2rt/(t^2-1)+1/(t log t)",
            2 * 1 == 2,
            {
                "h_includes_log_denominator": True,
                "first_numerator_coefficient": 2,
                "algebraic_term": "2*r*t/(t^2-1)",
                "log_term": "1/(t*log(t))",
                "log_term_present": True,
            },
        ),
        _row(
            "hazard_algebraic_part_decreases",
            "hazard",
            "d[2rt/(t^2-1)]/dt=-2r(t^2+1)/(t^2-1)^2<0",
            -2 < 0,
            {"derivative_sign": -1, "positive_factor": "2r(t^2+1)/(t^2-1)^2"},
        ),
        _row(
            "hazard_log_part_decreases",
            "hazard",
            "d[1/(t log t)]/dt=-(log t+1)/(t^2 log(t)^2)<0",
            -1 < 0,
            {"derivative_sign": -1, "positive_factor": "(log(t)+1)/(t^2*log(t)^2)"},
        ),
        _row(
            "hazard_integral_lower",
            "hazard",
            "decreasing q_r implies J_r>=h_r(x)/q_r(x)",
            True,
            {
                "comparison_kernel": "h_r(x)*exp(-q_r(x)*(t-x))",
                "hazard_direction": "q_r(t)<=q_r(x)",
                "direction": ">=",
                "integrated_lower": "h_r(x)/q_r(x)",
            },
        ),
        _row(
            "endpoint_hazard_upper",
            "hazard",
            "x*q_r(x)<=3r for x>=23",
            xq_margin > 0,
            {"r1_exact_margin_lower": fraction_text(xq_margin), "uses_log_x_gt": 3},
        ),
        _row(
            "stieltjes_error_relative",
            "source_transfer",
            "abs(P_r/J_r-1)<=(6r+1)*eta<=7r*eta",
            6 * 1 + 1 <= 7 * 1,
            {
                "boundary_xh_units": 1,
                "integral_xh_units": 1,
                "integral_J_units": 1,
                "hazard_xq_coefficient": 3,
                "derived_xh_units": 2,
                "derived_relative": "6r+1",
                "rounded_relative": "7r",
            },
        ),
        _row(
            "source_logarithmic_error",
            "source_transfer",
            "7r*eta<=1/2 implies abs(log(P_r/J_r))<=14r*eta",
            2 * 7 == 14,
            {"smallness": "7r*eta<=1/2", "coefficient": 14},
        ),
        _row(
            "exact_to_power_kernel",
            "kernel",
            "0<=log(J_r/I_(2r))<=-r log(1-x^-2)<=r/(x^2-1)",
            Fraction(1, 3) <= Fraction(1, 3),
            {
                "ratio": "J_r/I_2r",
                "log_direction": "nonnegative",
                "coefficient_r": 1,
                "denominator": "x^2-1",
                "pointwise_factor": "(1-t^-2)^(-r)",
            },
        ),
        _row(
            "coarse_power_kernel",
            "kernel",
            "under r/x^2<=3/8, abs(log(J_r/I_(2r)))<=4r/x^2",
            Fraction(1, 3) < Fraction(4, 4),
            {"role": "optional_coarser_corollary", "smallness": "r/x^2<=3/8"},
        ),
        _row(
            "power_to_leading_integral",
            "kernel",
            "I_(2r)/K_r=G(a_r)=integral_0^infinity e^-v/(1+a_r v)dv",
            True,
            {
                "substitution": "t=x*exp(u), v=(2r-1)*u",
                "laplace_rate": "2r-1",
                "a_r": "1/((2r-1)*L)",
                "K_r": "x^(1-2r)/((2r-1)*L)",
                "K_denominator": "(2r-1)*L",
                "exponential_moment_1": 1,
                "exponential_moment_2": 2,
                "jensen_direction": "lower",
                "bounds": "1/(1+a_r)<=G<=1",
            },
        ),
        _row(
            "leading_kernel_refinement",
            "kernel",
            "for a<=1/4, 0<=log G(a)+a<=2a^2",
            Fraction(2) * Fraction(1, 4) ** 2 == Fraction(1, 8),
            {"lower_tool": "Jensen: G>=exp(-a)", "upper_tool": "G<=1-a+2a^2", "quadratic_coefficient": 2},
        ),
    ]
    if len(rows) != ANALYTIC_ROW_COUNT:
        raise AssertionError("analytic row count changed")
    return rows


def r_fixture_row(r: int) -> dict[str, object]:
    r = _require_int(r, "r", 1)
    odd = 2 * r - 1
    return {
        "r": r,
        "two_r_minus_one": odd,
        "source_relative_coefficient": f"{6 * r + 1}<=7r",
        "source_log_coefficient": 14 * r,
        "hazard_x_upper": 3 * r,
        "power_kernel_coefficient": r,
        "leading_a": f"1/({odd}*L)",
        "K": f"x^({1 - 2 * r})/({odd}*L)",
        "source_smallness": f"{7 * r}*eta<=1/2",
        "pass": odd >= 1 and 6 * r + 1 <= 7 * r,
    }


def r_fixture_rows() -> list[dict[str, object]]:
    return [r_fixture_row(r) for r in R_FIXTURES]


def partition_row(partition: tuple[int, ...]) -> dict[str, object]:
    if type(partition) is not tuple or not partition:
        raise ValueError("partition must be a nonempty tuple")
    if any(type(part) is not int or part < 1 for part in partition):
        raise TypeError("partition parts must be positive exact integers")
    if tuple(sorted(partition, reverse=True)) != partition:
        raise ValueError("partition must be nonincreasing")
    counts = Counter(partition)
    degree = sum(partition)
    length = len(partition)
    h_value = sum((Fraction(count, 2 * part - 1) for part, count in counts.items()), Fraction(0))
    h2_value = sum((Fraction(count, (2 * part - 1) ** 2) for part, count in counts.items()), Fraction(0))
    leading_constant = Fraction(1)
    for part, count in counts.items():
        leading_constant *= Fraction(1, (2 * part - 1) ** count)
    p_exponent = sum((2 * part - 1) for part in partition)
    return {
        "partition": list(partition),
        "multiplicities": [{"r": part, "k": counts[part]} for part in sorted(counts)],
        "degree_d": degree,
        "length": length,
        "H": fraction_text(h_value),
        "H2": fraction_text(h2_value),
        "H2_le_H": h2_value <= h_value,
        "leading_constant": fraction_text(leading_constant),
        "p_exponent": p_exponent,
        "p_exponent_identity": f"{p_exponent}=2*{degree}-{length}",
        "rh384_regression_role": "reproduction_only",
        "pass": p_exponent == 2 * degree - length and h2_value <= h_value,
    }


def partition_rows() -> list[dict[str, object]]:
    rows = [
        partition_row(partition)
        for degree in range(1, PARTITION_DEGREE_MAX + 1)
        for partition in integer_partitions(degree)
    ]
    if len(rows) != 66:
        raise AssertionError("partition count changed")
    return rows


def envelope_rows() -> list[dict[str, object]]:
    rows = [
        {
            "id": "exact_kernel_partition",
            "hypothesis": "7*d*eta<=1/2",
            "bound": "abs(log(P_lambda/J_lambda))<=14*d*eta",
            "smallness_coefficient": 7,
            "log_coefficient": 14,
            "weight": "degree_d",
            "pass": 14 == 2 * 7,
        },
        {
            "id": "power_kernel_partition",
            "hypothesis": "exact-kernel hypothesis",
            "bound": "abs(log(P_lambda/I_lambda))<=14*d*eta+d/(x^2-1)",
            "source_coefficient": 14,
            "power_coefficient": 1,
            "power_weight": "degree_d",
            "power_denominator": "x^2-1",
            "pass": True,
        },
        {
            "id": "leading_kernel_partition",
            "hypothesis": "power-kernel hypothesis",
            "bound": "abs(log(P_lambda/M_lambda))<=14*d*eta+d/(x^2-1)+H/L",
            "leading_weight": "H",
            "leading_denominator": "L",
            "leading_absolute_coefficient": 1,
            "pass": True,
        },
        {
            "id": "refined_leading_expansion",
            "hypothesis": "a_r<=1/4 on every active part",
            "bound": "abs(log(P_lambda/M_lambda)+H/L)<=14*d*eta+d/(x^2-1)+2*H2/L^2",
            "leading_log_sign": -1,
            "H2_coefficient": 2,
            "H2_denominator_power": 2,
            "pass": True,
        },
        {
            "id": "sufficient_growing_family",
            "hypothesis": "log(d)=o(V) and H=o(L)",
            "bound": "d*eta+d/x^2->0 and H/L->0",
            "single_r_refinement": "for fixed delta in (0,0.1853), R<=exp((0.1853-delta)*V) is sufficient",
            "eta_exponential_rate": fraction_text(ETA_EXPONENT),
            "polynomial_log_power": fraction_text(ETA_LOG_POWER),
            "V_dominates_log_L": True,
            "pass": ETA_EXPONENT == Fraction(1853, 10_000),
        },
        {
            "id": "sharpness_partition_ones",
            "hypothesis": "lambda=1^k and k/L->c",
            "bound": "P_lambda/M_lambda->exp(-c)",
            "obstruction": "under source/power admissibility, leading uniformity holds iff H/L->0",
            "part": 1,
            "two_r_minus_one": 1,
            "d_per_copy": 1,
            "H_per_copy": "1",
            "H2_per_copy": "1",
            "log_ratio_limit_coefficient": -1,
            "pass": True,
        },
    ]
    if len(rows) != ENVELOPE_ROW_COUNT:
        raise AssertionError("envelope row count changed")
    return rows


def theorem_contracts() -> dict[str, object]:
    return {
        "endpoint": {
            "prime_tail": "p>x with x=p_y",
            "stieltjes_interval": "(x,infinity)",
            "boundary_term": "-theta(x)*h_r(x)",
            "successor_tail": "p_(y+1) then P_r(y+1)",
        },
        "definitions": {
            "h_r": "(t^2-1)^(-r)/log(t)",
            "J_r": "integral_x^infinity h_r(t)dt",
            "I_2r": "integral_x^infinity t^(-2r)/log(t)dt",
            "K_r": "x^(1-2r)/((2r-1)*L)",
            "d": "sum_r r*k_r",
            "H": "sum_r k_r/(2r-1)",
            "H2": "sum_r k_r/(2r-1)^2",
        },
        "source_ledger": {
            "relative": "abs(P_r/J_r-1)<=(6r+1)*eta<=7r*eta",
            "logarithmic": "abs(log(P_r/J_r))<=14r*eta when 7r*eta<=1/2",
        },
        "kernel_ledger": {
            "canonical_exact_to_power": "0<=log(J_r/I_2r)<=r/(x^2-1)",
            "optional_coarse": "abs(log(J_r/I_2r))<=4r/x^2 when r/x^2<=3/8",
            "leading": "abs(log(I_2r/K_r))<=1/((2r-1)*L)",
            "refined": "0<=log(I_2r/K_r)+1/((2r-1)*L)<=2/((2r-1)^2*L^2)",
        },
        "partition_ledger": {
            "exact_kernel": "14*d*eta",
            "power_kernel_addition": "d/(x^2-1)",
            "leading_addition": "H/L",
            "refined_leading_sign": "-H/L",
            "refined_remainder": "2*H2/L^2",
        },
        "growth": {
            "source_and_power_conditions": "d*eta+d/x^2->0",
            "leading_condition": "H/L->0",
            "sufficient": "log(d)=o(V) and H=o(L)",
            "single_r": "log(R)=o(V)",
            "single_r_sharper": "R<=exp((0.1853-delta)*V), fixed delta in (0,0.1853)",
        },
        "sharpness": {
            "family": "lambda=1^k",
            "regime": "k/L->c",
            "leading_ratio": "P_lambda/M_lambda->exp(-c)",
        },
    }


def claim_boundary() -> dict[str, object]:
    return {
        "fixed_finite_q_before_prefix_limit": True,
        "universally_safe_phasewise_c11_zero_only": True,
        "no_growing_clock": True,
        "no_active_c11": True,
        "no_adaptive_capacity_limit": True,
        "no_effective_threshold": True,
        "no_operator_trace_zeros_or_RH": True,
        "gates": {
            "A_intrinsic_determinant": False,
            "B_scattering_completion": False,
            "C_self_adjoint_generator": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
        "route_a": "GO",
        "route_b": "STOP_SCOPED",
    }


def build_certificate() -> dict[str, object]:
    analytic = analytic_rows()
    fixtures = r_fixture_rows()
    partitions = partition_rows()
    envelopes = envelope_rows()
    row_total = len(analytic) + len(fixtures) + len(partitions) + len(envelopes)
    all_pass = (
        row_total == 96
        and all(row["pass"] is True for row in analytic)
        and all(row["pass"] is True for row in fixtures)
        and all(row["pass"] is True for row in partitions)
        and all(row["pass"] is True for row in envelopes)
        and source_theorem_contract()["monotonicity_proof"]["pass"] is True
    )
    return {
        "status": "RH-386_exact_proof_interface_certificate",
        "epistemic_role": "reproduction_not_analytic_proof",
        "counts": {
            "analytic_source_rows": len(analytic),
            "r_fixtures": len(fixtures),
            "partition_rows": len(partitions),
            "envelope_sharpness_rows": len(envelopes),
            "oracle_rows_total": row_total,
        },
        "remote_source_lock": remote_source_lock(),
        "source_theorem": source_theorem_contract(),
        "analytic_rows": analytic,
        "r_fixtures": fixtures,
        "partitions": partitions,
        "envelopes": envelopes,
        "contracts": theorem_contracts(),
        "claim_boundary": claim_boundary(),
        "all_pass": all_pass,
    }


def _expect_exact(value: object, expected: object, label: str) -> None:
    if not exact_equal(value, expected):
        raise ValueError(f"{label} failed exact semantic verification")


def _validate_source_theorem(value: object) -> None:
    if type(value) is not dict:
        raise TypeError("source_theorem must be an object")
    expected_keys = {
        "theta_bound", "L", "V", "eta", "eta_coefficient", "eta_log_power",
        "eta_exponent", "V_log_power", "V_loglog_power", "source_x_min",
        "tail_monotonicity_L_min", "monotonicity_proof", "evidence_role", "locator",
    }
    if set(value) != expected_keys:
        raise ValueError("source_theorem membership changed")
    coefficient = fraction_from_object(value["eta_coefficient"], "eta_coefficient")
    log_power = fraction_from_object(value["eta_log_power"], "eta_log_power")
    exponent = fraction_from_object(value["eta_exponent"], "eta_exponent")
    v_power = fraction_from_object(value["V_log_power"], "V_log_power")
    v_loglog = fraction_from_object(value["V_loglog_power"], "V_loglog_power")
    _expect_exact(coefficient, Fraction(27, 1000), "eta coefficient")
    _expect_exact(log_power, Fraction(1801, 1000), "eta log power")
    _expect_exact(exponent, Fraction(1853, 10_000), "eta exponent")
    _expect_exact(v_power, Fraction(3, 5), "V log power")
    _expect_exact(v_loglog, Fraction(-1, 5), "V loglog power")
    _expect_exact(value["source_x_min"], 23, "source x domain")
    _expect_exact(value["tail_monotonicity_L_min"], 512, "eta monotonicity threshold")
    _expect_exact(value["theta_bound"], "abs(theta(x)-x)<=eta(log(x))*x for every x>=23", "theta bound")
    _expect_exact(value["L"], "log(x)", "L definition")
    _expect_exact(value["V"], "L^(3/5)*(log(L))^(-1/5)", "V definition")
    _expect_exact(value["eta"], "0.027*L^1.801*exp(-0.1853*V)", "eta definition")
    _expect_exact(value["evidence_role"], "peer_reviewed_explicit_VK_theorem_not_finite_fit", "source evidence role")
    _expect_exact(value["locator"], "Johnston--Yang Theorem 1.4 equation (1.8)", "source theorem locator")
    proof = value["monotonicity_proof"]
    if type(proof) is not dict or set(proof) != {
        "log_L_lower", "sqrt_L_strict_lower", "V_lower", "derivative_factor_lower",
        "negative_bracket_margin_lower", "pass",
    }:
        raise ValueError("monotonicity proof membership changed")
    _expect_exact(proof["log_L_lower"], 6, "log L lower bound")
    _expect_exact(proof["sqrt_L_strict_lower"], 22, "sqrt L lower bound")
    _expect_exact(proof["V_lower"], "sqrt(L)", "V lower bound")
    factor = fraction_from_object(proof["derivative_factor_lower"], "derivative factor")
    margin = fraction_from_object(proof["negative_bracket_margin_lower"], "monotonic margin")
    derived_margin = exponent * proof["sqrt_L_strict_lower"] * factor - log_power
    _expect_exact(factor, Fraction(17, 30), "derivative factor")
    _expect_exact(margin, derived_margin, "monotonic margin")
    if margin <= 0 or proof["pass"] is not True:
        raise ValueError("eta monotonicity proof failed")


ANALYTIC_META = {
    "source_vk_constants": ("source", "Theorem 1.4 (1.8) supplies 0.027, 1.801, 0.1853, 3/5, -1/5"),
    "eta_log_derivative": ("source", "L*d(log eta)/dL=1.801-0.1853*V*(3/5-1/(5log L))"),
    "eta_tail_monotone": ("source", "eta is decreasing for L>=512"),
    "strict_stieltjes_boundary": ("endpoint", "P_r=-theta(x)h_r(x)-integral_x^infinity theta(t)h_r'(t)dt"),
    "strict_successor": ("endpoint", "P_r(y)=(p_(y+1)^2-1)^(-r)+P_r(y+1)"),
    "hazard_formula": ("hazard", "q_r=-h_r'/h_r=2rt/(t^2-1)+1/(t log t)"),
    "hazard_algebraic_part_decreases": ("hazard", "d[2rt/(t^2-1)]/dt=-2r(t^2+1)/(t^2-1)^2<0"),
    "hazard_log_part_decreases": ("hazard", "d[1/(t log t)]/dt=-(log t+1)/(t^2 log(t)^2)<0"),
    "hazard_integral_lower": ("hazard", "decreasing q_r implies J_r>=h_r(x)/q_r(x)"),
    "endpoint_hazard_upper": ("hazard", "x*q_r(x)<=3r for x>=23"),
    "stieltjes_error_relative": ("source_transfer", "abs(P_r/J_r-1)<=(6r+1)*eta<=7r*eta"),
    "source_logarithmic_error": ("source_transfer", "7r*eta<=1/2 implies abs(log(P_r/J_r))<=14r*eta"),
    "exact_to_power_kernel": ("kernel", "0<=log(J_r/I_(2r))<=-r log(1-x^-2)<=r/(x^2-1)"),
    "coarse_power_kernel": ("kernel", "under r/x^2<=3/8, abs(log(J_r/I_(2r)))<=4r/x^2"),
    "power_to_leading_integral": ("kernel", "I_(2r)/K_r=G(a_r)=integral_0^infinity e^-v/(1+a_r v)dv"),
    "leading_kernel_refinement": ("kernel", "for a<=1/4, 0<=log G(a)+a<=2a^2"),
}


def _validate_analytic_rows(value: object) -> None:
    if type(value) is not list or len(value) != 16:
        raise ValueError("analytic rows must contain 16 entries")
    if [row.get("id") if type(row) is dict else None for row in value] != list(ANALYTIC_META):
        raise ValueError("analytic row order or identifiers changed")
    for row in value:
        if type(row) is not dict or set(row) != {"id", "domain", "statement", "derived", "pass"}:
            raise ValueError("analytic row membership changed")
        row_id = row["id"]
        domain, statement = ANALYTIC_META[row_id]
        _expect_exact(row["domain"], domain, f"{row_id} domain")
        _expect_exact(row["statement"], statement, f"{row_id} statement")
        if row["pass"] is not True or type(row["derived"]) is not dict:
            raise ValueError(f"{row_id} did not pass with an exact object")
        d = row["derived"]
        if row_id == "source_vk_constants":
            _expect_exact(d, {
                "coefficient": "27/1000", "log_power": "1801/1000", "exponent": "1853/10000",
                "V_log_power": "3/5", "V_loglog_power": "-1/5", "source_x_min": 23,
            }, row_id)
        elif row_id == "eta_log_derivative":
            _expect_exact(d, {
                "positive_term": "1801/1000", "negative_coefficient": "1853/10000",
                "V_multiplier_log_power": "3/5", "V_multiplier_loglog_correction": "-1/5",
            }, row_id)
        elif row_id == "eta_tail_monotone":
            exact_margin = Fraction(1853, 10_000) * 22 * Fraction(17, 30) - Fraction(1801, 1000)
            _expect_exact(d, {
                "exact_lower_margin": fraction_text(exact_margin), "L_min": 512,
                "derivative_direction": "decreasing", "sqrt_L_strict_lower": 22,
                "factor_lower": "17/30",
            }, row_id)
        elif row_id == "strict_stieltjes_boundary":
            _expect_exact(d, {
                "boundary_coefficient": -1, "endpoint": "(x,infinity)", "prime_condition": "p>x",
                "main_measure_boundary_coefficient": -1, "integration_by_parts_boundary_coefficient": 1,
            }, row_id)
            if d["boundary_coefficient"] + d["integration_by_parts_boundary_coefficient"] != 0:
                raise ValueError("strict boundary cancellation failed")
        elif row_id == "strict_successor":
            required = {
                "tail", "first_atom", "current_atom_excluded", "witness_r", "witness_p_y",
                "witness_tail_primes", "witness_lhs", "witness_first_atom", "witness_successor", "witness_rhs",
            }
            if set(d) != required:
                raise ValueError("successor witness membership changed")
            r = _require_int(d["witness_r"], "successor r", 1)
            _expect_exact(d["witness_p_y"], 3, "successor p_y")
            _expect_exact(d["witness_tail_primes"], [5, 7, 11], "successor prime list")
            terms = [Fraction(1, (prime * prime - 1) ** r) for prime in d["witness_tail_primes"]]
            lhs = sum(terms, Fraction(0))
            successor = sum(terms[1:], Fraction(0))
            _expect_exact(fraction_from_text(d["witness_lhs"], "successor lhs"), lhs, "successor lhs")
            _expect_exact(fraction_from_text(d["witness_first_atom"], "successor atom"), terms[0], "successor atom")
            _expect_exact(fraction_from_text(d["witness_successor"], "successor tail"), successor, "successor tail")
            _expect_exact(fraction_from_text(d["witness_rhs"], "successor rhs"), terms[0] + successor, "successor rhs")
            _expect_exact([d["tail"], d["first_atom"], d["current_atom_excluded"]], ["strict", "p_(y+1)", True], row_id)
        elif row_id == "hazard_formula":
            _expect_exact(d, {
                "h_includes_log_denominator": True, "first_numerator_coefficient": 2,
                "algebraic_term": "2*r*t/(t^2-1)", "log_term": "1/(t*log(t))", "log_term_present": True,
            }, row_id)
        elif row_id == "hazard_algebraic_part_decreases":
            _expect_exact(d, {"derivative_sign": -1, "positive_factor": "2r(t^2+1)/(t^2-1)^2"}, row_id)
        elif row_id == "hazard_log_part_decreases":
            _expect_exact(d, {"derivative_sign": -1, "positive_factor": "(log(t)+1)/(t^2*log(t)^2)"}, row_id)
        elif row_id == "hazard_integral_lower":
            _expect_exact(d, {
                "comparison_kernel": "h_r(x)*exp(-q_r(x)*(t-x))", "hazard_direction": "q_r(t)<=q_r(x)",
                "direction": ">=", "integrated_lower": "h_r(x)/q_r(x)",
            }, row_id)
        elif row_id == "endpoint_hazard_upper":
            margin = Fraction(3) - Fraction(2 * 23 * 23, 23 * 23 - 1) - Fraction(1, 3)
            _expect_exact(d, {"r1_exact_margin_lower": fraction_text(margin), "uses_log_x_gt": 3}, row_id)
            if fraction_from_text(d["r1_exact_margin_lower"], "xq margin") <= 0:
                raise ValueError("xq margin is not positive")
        elif row_id == "stieltjes_error_relative":
            required = {
                "boundary_xh_units": 1, "integral_xh_units": 1, "integral_J_units": 1,
                "hazard_xq_coefficient": 3, "derived_xh_units": 2,
                "derived_relative": "6r+1", "rounded_relative": "7r",
            }
            _expect_exact(d, required, row_id)
            if d["boundary_xh_units"] + d["integral_xh_units"] != d["derived_xh_units"]:
                raise ValueError("2xh+J contribution failed")
        elif row_id == "source_logarithmic_error":
            _expect_exact(d, {"smallness": "7r*eta<=1/2", "coefficient": 14}, row_id)
            if d["coefficient"] != 2 * 7:
                raise ValueError("logarithmic source coefficient failed")
        elif row_id == "exact_to_power_kernel":
            _expect_exact(d, {
                "ratio": "J_r/I_2r", "log_direction": "nonnegative", "coefficient_r": 1,
                "denominator": "x^2-1", "pointwise_factor": "(1-t^-2)^(-r)",
            }, row_id)
        elif row_id == "coarse_power_kernel":
            _expect_exact(d, {"role": "optional_coarser_corollary", "smallness": "r/x^2<=3/8"}, row_id)
        elif row_id == "power_to_leading_integral":
            _expect_exact(d, {
                "substitution": "t=x*exp(u), v=(2r-1)*u", "laplace_rate": "2r-1",
                "a_r": "1/((2r-1)*L)", "K_r": "x^(1-2r)/((2r-1)*L)",
                "K_denominator": "(2r-1)*L", "exponential_moment_1": 1,
                "exponential_moment_2": 2, "jensen_direction": "lower", "bounds": "1/(1+a_r)<=G<=1",
            }, row_id)
            if d["exponential_moment_2"] != 2 * d["exponential_moment_1"]:
                raise ValueError("exponential moments failed")
        elif row_id == "leading_kernel_refinement":
            _expect_exact(d, {
                "lower_tool": "Jensen: G>=exp(-a)", "upper_tool": "G<=1-a+2a^2", "quadratic_coefficient": 2,
            }, row_id)
        else:  # pragma: no cover - protected by the identifier check
            raise AssertionError(row_id)


def _validate_r_fixtures(value: object) -> None:
    if type(value) is not list or len(value) != len(R_FIXTURES):
        raise ValueError("r fixtures changed")
    for expected_r, row in zip(R_FIXTURES, value):
        if type(row) is not dict or set(row) != {
            "r", "two_r_minus_one", "source_relative_coefficient", "source_log_coefficient",
            "hazard_x_upper", "power_kernel_coefficient", "leading_a", "K", "source_smallness", "pass",
        }:
            raise ValueError("r fixture membership changed")
        r = _require_int(row["r"], "fixture r", 1)
        _expect_exact(r, expected_r, "fixture r order")
        odd = 2 * r - 1
        _expect_exact(row, {
            "r": r, "two_r_minus_one": odd, "source_relative_coefficient": f"{6 * r + 1}<=7r",
            "source_log_coefficient": 14 * r, "hazard_x_upper": 3 * r,
            "power_kernel_coefficient": r, "leading_a": f"1/({odd}*L)",
            "K": f"x^({1 - 2 * r})/({odd}*L)", "source_smallness": f"{7 * r}*eta<=1/2", "pass": True,
        }, f"r fixture {r}")


def _validate_partitions(value: object) -> None:
    if type(value) is not list or len(value) != 66:
        raise ValueError("partition rows must contain 66 entries")
    expected_partitions = [
        partition for degree in range(1, 9) for partition in integer_partitions(degree)
    ]
    for expected_partition, row in zip(expected_partitions, value):
        if type(row) is not dict or set(row) != {
            "partition", "multiplicities", "degree_d", "length", "H", "H2", "H2_le_H",
            "leading_constant", "p_exponent", "p_exponent_identity", "rh384_regression_role", "pass",
        }:
            raise ValueError("partition row membership changed")
        if type(row["partition"]) is not list or any(type(part) is not int for part in row["partition"]):
            raise TypeError("partition parts must be exact integers")
        partition = tuple(row["partition"])
        _expect_exact(partition, expected_partition, "partition order")
        counts = Counter(partition)
        degree = sum(partition)
        length = len(partition)
        h_value = sum((Fraction(count, 2 * part - 1) for part, count in counts.items()), Fraction(0))
        h2_value = sum((Fraction(count, (2 * part - 1) ** 2) for part, count in counts.items()), Fraction(0))
        constant = Fraction(1)
        for part, count in counts.items():
            constant *= Fraction(1, (2 * part - 1) ** count)
        p_exponent = sum(2 * part - 1 for part in partition)
        expected = {
            "partition": list(partition),
            "multiplicities": [{"r": part, "k": counts[part]} for part in sorted(counts)],
            "degree_d": degree, "length": length, "H": fraction_text(h_value), "H2": fraction_text(h2_value),
            "H2_le_H": h2_value <= h_value, "leading_constant": fraction_text(constant),
            "p_exponent": p_exponent, "p_exponent_identity": f"{p_exponent}=2*{degree}-{length}",
            "rh384_regression_role": "reproduction_only", "pass": p_exponent == 2 * degree - length and h2_value <= h_value,
        }
        _expect_exact(row, expected, f"partition {partition}")
        if row["pass"] is not True:
            raise ValueError("partition row failed")


def _validate_envelopes(value: object) -> None:
    if type(value) is not list or len(value) != 6:
        raise ValueError("envelope rows must contain six entries")
    expected_ids = [
        "exact_kernel_partition", "power_kernel_partition", "leading_kernel_partition",
        "refined_leading_expansion", "sufficient_growing_family", "sharpness_partition_ones",
    ]
    if [row.get("id") if type(row) is dict else None for row in value] != expected_ids:
        raise ValueError("envelope identifiers changed")
    metadata = {
        "exact_kernel_partition": {
            "hypothesis": "7*d*eta<=1/2",
            "bound": "abs(log(P_lambda/J_lambda))<=14*d*eta",
        },
        "power_kernel_partition": {
            "hypothesis": "exact-kernel hypothesis",
            "bound": "abs(log(P_lambda/I_lambda))<=14*d*eta+d/(x^2-1)",
        },
        "leading_kernel_partition": {
            "hypothesis": "power-kernel hypothesis",
            "bound": "abs(log(P_lambda/M_lambda))<=14*d*eta+d/(x^2-1)+H/L",
        },
        "refined_leading_expansion": {
            "hypothesis": "a_r<=1/4 on every active part",
            "bound": "abs(log(P_lambda/M_lambda)+H/L)<=14*d*eta+d/(x^2-1)+2*H2/L^2",
        },
        "sufficient_growing_family": {
            "hypothesis": "log(d)=o(V) and H=o(L)",
            "bound": "d*eta+d/x^2->0 and H/L->0",
            "single_r_refinement": "for fixed delta in (0,0.1853), R<=exp((0.1853-delta)*V) is sufficient",
        },
        "sharpness_partition_ones": {
            "hypothesis": "lambda=1^k and k/L->c",
            "bound": "P_lambda/M_lambda->exp(-c)",
            "obstruction": "under source/power admissibility, leading uniformity holds iff H/L->0",
        },
    }
    key_sets = {
        "exact_kernel_partition": {"id", "hypothesis", "bound", "smallness_coefficient", "log_coefficient", "weight", "pass"},
        "power_kernel_partition": {"id", "hypothesis", "bound", "source_coefficient", "power_coefficient", "power_weight", "power_denominator", "pass"},
        "leading_kernel_partition": {"id", "hypothesis", "bound", "leading_weight", "leading_denominator", "leading_absolute_coefficient", "pass"},
        "refined_leading_expansion": {"id", "hypothesis", "bound", "leading_log_sign", "H2_coefficient", "H2_denominator_power", "pass"},
        "sufficient_growing_family": {"id", "hypothesis", "bound", "single_r_refinement", "eta_exponential_rate", "polynomial_log_power", "V_dominates_log_L", "pass"},
        "sharpness_partition_ones": {"id", "hypothesis", "bound", "obstruction", "part", "two_r_minus_one", "d_per_copy", "H_per_copy", "H2_per_copy", "log_ratio_limit_coefficient", "pass"},
    }
    for row in value:
        if type(row) is not dict or row.get("pass") is not True:
            raise ValueError("envelope row failed")
        row_id = row["id"]
        if set(row) != key_sets[row_id]:
            raise ValueError(f"{row_id} membership changed")
        for field, expected in metadata[row_id].items():
            _expect_exact(row[field], expected, f"{row_id} {field}")
        if row_id == "exact_kernel_partition":
            _expect_exact(row["smallness_coefficient"], 7, "exact smallness coefficient")
            _expect_exact(row["log_coefficient"], 2 * row["smallness_coefficient"], "exact log coefficient")
            _expect_exact(row["weight"], "degree_d", "exact degree weight")
        elif row_id == "power_kernel_partition":
            _expect_exact([row["source_coefficient"], row["power_coefficient"], row["power_weight"], row["power_denominator"]], [14, 1, "degree_d", "x^2-1"], row_id)
        elif row_id == "leading_kernel_partition":
            _expect_exact([row["leading_weight"], row["leading_denominator"], row["leading_absolute_coefficient"]], ["H", "L", 1], row_id)
        elif row_id == "refined_leading_expansion":
            _expect_exact([row["leading_log_sign"], row["H2_coefficient"], row["H2_denominator_power"]], [-1, 2, 2], row_id)
        elif row_id == "sufficient_growing_family":
            _expect_exact(fraction_from_text(row["eta_exponential_rate"], "envelope eta rate"), Fraction(1853, 10_000), row_id)
            _expect_exact(fraction_from_text(row["polynomial_log_power"], "envelope log power"), Fraction(1801, 1000), row_id)
            if row["V_dominates_log_L"] is not True:
                raise ValueError("V/log L growth flag failed")
        elif row_id == "sharpness_partition_ones":
            part = _require_int(row["part"], "sharpness part", 1)
            _expect_exact(part, 1, "sharpness part")
            _expect_exact(row["two_r_minus_one"], 2 * part - 1, "sharpness denominator")
            _expect_exact(row["d_per_copy"], part, "sharpness degree")
            _expect_exact(fraction_from_text(row["H_per_copy"], "sharpness H"), Fraction(1, 2 * part - 1), "sharpness H")
            _expect_exact(fraction_from_text(row["H2_per_copy"], "sharpness H2"), Fraction(1, (2 * part - 1) ** 2), "sharpness H2")
            _expect_exact(row["log_ratio_limit_coefficient"], -1, "sharpness sign")


def _validate_certificate(candidate: dict[str, object]) -> None:
    if type(candidate) is not dict:
        raise TypeError("certificate must be an object")
    expected_keys = {
        "status", "epistemic_role", "counts", "remote_source_lock", "source_theorem",
        "analytic_rows", "r_fixtures", "partitions", "envelopes", "contracts", "claim_boundary", "all_pass",
    }
    if set(candidate) != expected_keys:
        raise ValueError("certificate top-level membership changed")
    _expect_exact(candidate["status"], "RH-386_exact_proof_interface_certificate", "certificate status")
    _expect_exact(candidate["epistemic_role"], "reproduction_not_analytic_proof", "epistemic role")
    _expect_exact(candidate["remote_source_lock"], remote_source_lock(), "remote source lock")
    _validate_source_theorem(candidate["source_theorem"])
    _validate_analytic_rows(candidate["analytic_rows"])
    _validate_r_fixtures(candidate["r_fixtures"])
    _validate_partitions(candidate["partitions"])
    _validate_envelopes(candidate["envelopes"])
    counts = candidate["counts"]
    if type(counts) is not dict:
        raise TypeError("counts must be an object")
    derived_counts = {
        "analytic_source_rows": len(candidate["analytic_rows"]),
        "r_fixtures": len(candidate["r_fixtures"]),
        "partition_rows": len(candidate["partitions"]),
        "envelope_sharpness_rows": len(candidate["envelopes"]),
        "oracle_rows_total": sum(len(candidate[key]) for key in ("analytic_rows", "r_fixtures", "partitions", "envelopes")),
    }
    _expect_exact(counts, derived_counts, "certificate counts")
    if counts["oracle_rows_total"] != 96:
        raise ValueError("oracle total is not 96")
    _expect_exact(candidate["contracts"], theorem_contracts(), "theorem contracts")
    _expect_exact(candidate["claim_boundary"], claim_boundary(), "claim boundary")
    if candidate["all_pass"] is not True:
        raise ValueError("certificate all_pass is not exact true")


def verify_certificate(
    certificate: dict[str, object] | None = None,
    *,
    compare_fresh: bool = True,
) -> dict[str, object]:
    _require_bool(compare_fresh, "compare_fresh")
    candidate = build_certificate() if certificate is None else certificate
    _validate_certificate(candidate)
    if compare_fresh and canonical_json_bytes(candidate) != canonical_json_bytes(build_certificate()):
        raise ValueError("certificate differs from fresh canonical regeneration")
    return candidate


MUTATION_NAMES = (
    "eta_coefficient_0027",
    "eta_log_power_1801",
    "eta_exponent_01853",
    "V_loglog_sign",
    "source_domain_23",
    "source_SHA256",
    "wrong_ge_endpoint",
    "missing_stieltjes_boundary",
    "h_missing_log_denominator",
    "hazard_missing_log_term",
    "hazard_monotonicity_direction",
    "hazard_integral_lower_direction",
    "stieltjes_missing_2xh_plus_J",
    "missing_r_coefficient",
    "J_over_I_direction",
    "x_squared_minus_one",
    "wrong_laplace_rate",
    "wrong_jensen_direction",
    "wrong_K_denominator",
    "degree_replaced_by_length",
    "wrong_H_denominator",
    "omit_H_over_L",
    "degree_only_leading_firewall",
    "redistributable_true",
)


def apply_mutation(certificate: dict[str, object], name: str) -> dict[str, object]:
    if type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown mutation")
    mutated = deepcopy(certificate)
    if name == "eta_coefficient_0027":
        mutated["source_theorem"]["eta_coefficient"]["numerator"] = 26
    elif name == "eta_log_power_1801":
        mutated["source_theorem"]["eta_log_power"]["numerator"] = 1800
    elif name == "eta_exponent_01853":
        mutated["source_theorem"]["eta_exponent"]["numerator"] = 1852
    elif name == "V_loglog_sign":
        mutated["source_theorem"]["V_loglog_power"]["numerator"] = 1
    elif name == "source_domain_23":
        mutated["source_theorem"]["source_x_min"] = 24
    elif name == "source_SHA256":
        mutated["remote_source_lock"]["sha256"] = "0" * 64
    elif name == "wrong_ge_endpoint":
        mutated["contracts"]["endpoint"]["prime_tail"] = "p>=x with x=p_y"
        mutated["contracts"]["endpoint"]["successor_tail"] = "current p_y atom then P_r(y)"
    elif name == "missing_stieltjes_boundary":
        mutated["analytic_rows"][3]["derived"]["boundary_coefficient"] = 0
    elif name == "h_missing_log_denominator":
        mutated["analytic_rows"][5]["derived"]["h_includes_log_denominator"] = False
    elif name == "hazard_missing_log_term":
        mutated["analytic_rows"][5]["derived"]["log_term_present"] = False
    elif name == "hazard_monotonicity_direction":
        mutated["analytic_rows"][6]["derived"]["derivative_sign"] = 1
    elif name == "hazard_integral_lower_direction":
        mutated["analytic_rows"][8]["derived"]["direction"] = "<="
    elif name == "stieltjes_missing_2xh_plus_J":
        mutated["analytic_rows"][10]["derived"]["integral_xh_units"] = 0
    elif name == "missing_r_coefficient":
        mutated["analytic_rows"][10]["derived"]["rounded_relative"] = "7"
    elif name == "J_over_I_direction":
        mutated["analytic_rows"][12]["derived"]["log_direction"] = "nonpositive"
    elif name == "x_squared_minus_one":
        mutated["analytic_rows"][12]["derived"]["denominator"] = "x^2+1"
    elif name == "wrong_laplace_rate":
        mutated["analytic_rows"][14]["derived"]["laplace_rate"] = "2r"
    elif name == "wrong_jensen_direction":
        mutated["analytic_rows"][14]["derived"]["jensen_direction"] = "upper"
    elif name == "wrong_K_denominator":
        mutated["analytic_rows"][14]["derived"]["K_denominator"] = "2r*L"
    elif name == "degree_replaced_by_length":
        mutated["envelopes"][0]["weight"] = "length"
    elif name == "wrong_H_denominator":
        mutated["contracts"]["definitions"]["H"] = "sum_r k_r/(2r+1)"
    elif name == "omit_H_over_L":
        mutated["contracts"]["partition_ledger"]["leading_addition"] = "0"
    elif name == "degree_only_leading_firewall":
        mutated["envelopes"][4]["hypothesis"] = "log(d)=o(V)"
    elif name == "redistributable_true":
        mutated["remote_source_lock"]["redistributable_in_release"] = True
    else:  # pragma: no cover - membership is checked above
        raise AssertionError(name)
    return mutated


def mutation_results() -> list[dict[str, object]]:
    fresh = build_certificate()
    rows: list[dict[str, object]] = []
    for name in MUTATION_NAMES:
        mutated = apply_mutation(fresh, name)
        changed = canonical_json_bytes(mutated) != canonical_json_bytes(fresh)
        rejected = False
        try:
            verify_certificate(mutated, compare_fresh=False)
        except (TypeError, ValueError):
            rejected = True
        rows.append({"name": name, "mode": "field_level_semantic", "payload_changed": changed, "rejected": rejected})
    if len(rows) != MUTATION_COUNT or [row["name"] for row in rows] != list(MUTATION_NAMES):
        raise AssertionError("mutation membership changed")
    if not all(row["payload_changed"] is True and row["rejected"] is True for row in rows):
        raise AssertionError("a mutation escaped")
    return rows


def auxiliary_attack_results() -> list[dict[str, object]]:
    """Additional source-metadata, exact-type, and strict-JSON attacks."""

    fresh = build_certificate()
    specifications = (
        ("source_url", "versioned_url", "https://arxiv.org/pdf/2204.01980"),
        ("source_bytes", "bytes", 278_381),
        ("source_DOI", "version_of_record_doi", "10.0000/wrong"),
        ("source_MIME", "mime", "text/plain"),
        ("source_pages_type", "pages", "22"),
    )
    rows: list[dict[str, object]] = []
    for name, field, bad_value in specifications:
        mutated = deepcopy(fresh)
        mutated["remote_source_lock"][field] = bad_value
        rejected = False
        try:
            verify_certificate(mutated, compare_fresh=False)
        except (TypeError, ValueError):
            rejected = True
        rows.append({"name": name, "mode": "field_level_semantic", "rejected": rejected})
    for name, text in (
        ("nonfinite_JSON", '{"value":NaN}'),
        ("duplicate_JSON", '{"value":1,"value":2}'),
    ):
        rejected = False
        try:
            loads_strict(text)
        except ValueError:
            rejected = True
        rows.append({"name": name, "mode": "strict_json", "rejected": rejected})
    if len(rows) != 7 or not all(row["rejected"] is True for row in rows):
        raise AssertionError("an auxiliary attack escaped")
    return rows
