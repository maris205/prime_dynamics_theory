#!/usr/bin/env python3
"""Independent exact replay for the TPC-280 two-term leakage compiler."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-280-leakage-aware-endpoint-compiler"
PARENT = ROOT / "papers/tpc-279-coherence-to-gain-theorem/results/tpc279_certificate.json"
RESULT = PROJECT / "results/tpc280_certificate.json"
PARENT_SHA256 = "88759801d7b2a9de317bee4c706a96c43fc3f3e05bd6604f20d8120ffae2d101"
PARENT_SCHEMA = "TPC279_COHERENCE_TO_GAIN_THEOREM_CERTIFICATE_V1"
SCHEMA = "TPC280_LEAKAGE_AWARE_ENDPOINT_COMPILER_CERTIFICATE_V1"
STATUS = (
    "PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_"
    "NUMERICALLY_CERTIFIED_TRANSFER"
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def ftext(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def itext(value: tuple[Fraction, Fraction]) -> list[str]:
    return [ftext(value[0]), ftext(value[1])]


CASES = (
    ("balanced_main_and_fast_leakage", 8, Fraction(3, 2), Fraction(1, 2),
     Fraction(1, 2), 2, 3),
    ("slow_leakage_bottleneck", 16, Fraction(1), Fraction(1), Fraction(2), 4, 1),
    ("equal_exponents", 10, Fraction(5, 4), Fraction(3, 5), Fraction(1, 4), 2, 2),
    ("zero_additive_leakage", 9, Fraction(2), Fraction(7, 4), Fraction(0), 3, 5),
    ("leakage_only", 32, Fraction(2), Fraction(0), Fraction(1), 5, 1),
    ("fractional_budget_constants", 25, Fraction(5, 3), Fraction(2, 3),
     Fraction(4, 3), 1, 3),
)


def inverse_power(x: int, exponent: int) -> Fraction:
    return Fraction(1, x ** exponent)


def expected_case(spec: tuple[Any, ...]) -> dict[str, Any]:
    name, x, d, b, ell, gamma, delta = spec
    ratio = ell / d
    main = b * inverse_power(x, gamma)
    leak = ratio * inverse_power(x, delta)
    two = main + leak
    kappa = min(gamma, delta)
    collapsed = (b + ratio) * inverse_power(x, kappa)
    need(two <= collapsed and two > 0 and collapsed > 0, "case envelope")
    return {
        "name": name, "X": x, "d": ftext(d), "B": ftext(b),
        "ell": ftext(ell), "ell_over_d": ftext(ratio),
        "gamma": gamma, "delta": delta, "kappa": kappa,
        "main_term": ftext(main), "normalized_leakage_term": ftext(leak),
        "two_term_q_bound": ftext(two), "collapsed_q_bound": ftext(collapsed),
        "two_term_gain_lower": ftext(1 / two),
        "collapsed_gain_lower": ftext(1 / collapsed),
        "two_term_bound_leq_collapsed": True,
        "equality_witness_available": True,
    }


def expected_margin(case: dict[str, Any], name: str, c: Fraction,
                    eta: Fraction, epsilon: Fraction) -> dict[str, Any]:
    x = case["X"]
    q_two = frac(case["two_term_q_bound"])
    q_collapsed = frac(case["collapsed_q_bound"])
    base = c * c * inverse_power(x, 2 * int(eta)) * inverse_power(
        x, 2 * int(epsilon))
    two = base / q_two
    collapsed = base / q_collapsed
    kappa = case["kappa"]
    eta_eff = max(Fraction(0), eta - Fraction(kappa, 2))
    return {
        "name": name, "source_case": case["name"], "X": x,
        "c": ftext(c), "eta_D": ftext(eta), "epsilon": ftext(epsilon),
        "kappa": kappa, "eta_eff": ftext(eta_eff),
        "margin_squared_two_term_lower": ftext(two),
        "margin_squared_collapsed_lower": ftext(collapsed),
        "two_term_is_at_least_collapsed": True,
        "compiler_status": "PROVED_CONDITIONAL",
    }


def expected_endpoint(name: str, sigma: Fraction, eta: Fraction,
                      gamma: Fraction, delta: Fraction) -> dict[str, Any]:
    kappa = min(gamma, delta)
    eta_eff = max(Fraction(0), eta - kappa / 2)
    gap = sigma - eta_eff - Fraction(1, 400)
    status = ("PAID_STRICT" if gap > 0 else
              "BORDERLINE_UNPAID" if gap == 0 else "UNPAID")
    return {
        "name": name, "sigma": ftext(sigma), "eta_D": ftext(eta),
        "gamma": ftext(gamma), "delta": ftext(delta),
        "kappa": ftext(kappa), "eta_eff": ftext(eta_eff),
        "strict_gap_after_1_over_400": ftext(gap), "status": status,
        "strict_condition": "sigma-eta_eff>1/400",
    }


def load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical JSON: " + str(path))
    return data


def check() -> None:
    parent_raw = PARENT.read_bytes()
    parent = load(PARENT)
    need(digest(parent_raw) == PARENT_SHA256, "parent hash")
    need(parent["payload"]["schema"] == PARENT_SCHEMA and
         len(parent["payload"]["rows"]) == 12, "parent schema/rows")
    data = load(RESULT)
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS, "certificate header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA, "certificate schema")
    need(data["payload_sha256"] == digest(canonical(payload)), "payload hash")
    exact = payload["exact_theorem"]
    need(exact["two_term_gain_compiler"] ==
         "r>=1/(B X^(-gamma)+(ell/d)X^(-delta))" and
         exact["dominant_exponent_compiler"] ==
         "r>=(B+ell/d)^(-1)X^kappa" and
         exact["leakage_obstruction"] ==
         "delta<gamma makes additive leakage the asymptotic bottleneck",
         "exact theorem")
    expected_cases = [expected_case(spec) for spec in CASES]
    need(payload["budget_cases"] == expected_cases, "budget cases")
    margin_specs = (
        ("margin_paid_after_fast_leakage", 0, Fraction(1), Fraction(1), Fraction(0)),
        ("margin_leakage_limited", 1, Fraction(1), Fraction(2), Fraction(0)),
        ("margin_equal_exponent", 2, Fraction(3, 2), Fraction(1), Fraction(0)),
        ("margin_zero_leakage", 3, Fraction(1), Fraction(2), Fraction(0)),
    )
    expected_margins = [expected_margin(expected_cases[index], name, c, eta, eps)
                        for name, index, c, eta, eps in margin_specs]
    need(payload["margin_cases"] == expected_margins, "margin cases")
    endpoint_specs = (
        ("strictly_paid", Fraction(1, 100), Fraction(1, 10), Fraction(4), Fraction(2)),
        ("leakage_controls_exponent_but_still_paid", Fraction(3, 1000),
         Fraction(1, 10), Fraction(4), Fraction(1)),
        ("borderline_not_paid", Fraction(1, 400), Fraction(1, 10), Fraction(4), Fraction(2)),
        ("loss_exceeds_saving", Fraction(1, 10), Fraction(1, 4), Fraction(1), Fraction(1, 5)),
    )
    expected_endpoints = [expected_endpoint(*spec) for spec in endpoint_specs]
    need(payload["endpoint_cases"] == expected_endpoints, "endpoint cases")
    transfer = payload["finite_transfer"]
    need(transfer == {
        "parent_schema": PARENT_SCHEMA,
        "parent_result_sha256": PARENT_SHA256,
        "total_rows": 12, "positive_deficit_rows": 8,
        "negative_deficit_rows": 4, "fixed_power_credit": 0,
        "asymptotic_promotion": "REFUTED_SCOPED",
    }, "transfer metadata")
    rows = payload["rows"]
    need(len(rows) == 12, "transfer row count")
    for source, row in zip(parent["payload"]["rows"], rows):
        q = interval(source["normalized_output_ratio_interval"])
        delta = interval(source["deficit_interval"])
        need(row["q_interval"] == itext(q) and
             row["deficit_interval"] == itext(delta), "transfer coordinate")
        need(row["parent_deficit_sign"] == source["deficit_sign"] and
             row["source_exact_digest"] == source["source_exact_digest"],
             "transfer identity")
        need(0 <= q[0] <= q[1] <= 4 and delta[0] < 1,
             "transfer domain")
    need(sum(row["parent_deficit_sign"] == "POSITIVE_DEFICIT" for row in rows) == 8 and
         sum(row["parent_deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows) == 4,
         "transfer census")
    firewall = payload["firewall"]
    need(firewall["TPC280_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC280_FULL_GATE_B"] == "OPEN" and
         firewall["TPC280_L2"] == "NONE", "firewall")
    print("TPC280_INDEPENDENT_CHECK=PASS cases=6 margin_cases=4 endpoint_cases=4 "
          "transfer_rows=12 positive_deficit=8 negative_deficit=4")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC280_INDEPENDENT_CHECK=FAIL: " + str(error))
