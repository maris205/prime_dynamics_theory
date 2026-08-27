#!/usr/bin/env python3
"""Exact two-term additive-leakage compiler and finite transfer certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_PROJECT = ROOT / "papers/tpc-279-coherence-to-gain-theorem"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc279_coherence_to_gain_certificate.py"
)
PARENT_RESULT = PARENT_PROJECT / "results/tpc279_certificate.json"
RESULT = PROJECT / "results/tpc280_certificate.json"

PARENT_CODE_SHA256 = "66c7891b268c73cfe927b351e3f8a162eb7d809fd71eaa7396b7356e3be813c4"
PARENT_RESULT_SHA256 = "88759801d7b2a9de317bee4c706a96c43fc3f3e05bd6604f20d8120ffae2d101"
PARENT_SCHEMA = "TPC279_COHERENCE_TO_GAIN_THEOREM_CERTIFICATE_V1"
SCHEMA = "TPC280_LEAKAGE_AWARE_ENDPOINT_COMPILER_CERTIFICATE_V1"
STATUS = (
    "PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_"
    "NUMERICALLY_CERTIFIED_TRANSFER"
)
ROUND2_CLUE = "AUDIT_TYPED_ARITHMETIC_L2_INTERFACE_FOR_FULL_GATE_B"


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval_text(value: tuple[Fraction, Fraction]) -> list[str]:
    return [fraction_text(value[0]), fraction_text(value[1])]


def parse_interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = parse_fraction(value[0]), parse_fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def normalized_hash(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def load_parent() -> dict[str, Any]:
    need(normalized_hash(PARENT_CODE) == PARENT_CODE_SHA256,
         "parent code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest_bytes(raw) == PARENT_RESULT_SHA256,
         "parent result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER",
         "parent header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == PARENT_SCHEMA, "parent schema")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent rows")
    return data


def inverse_power(x: int, exponent: int) -> Fraction:
    need(x >= 1 and exponent >= 0, "power domain")
    return Fraction(1, x ** exponent)


CASES: tuple[dict[str, Any], ...] = (
    {
        "name": "balanced_main_and_fast_leakage",
        "X": 8, "d": Fraction(3, 2), "B": Fraction(1, 2),
        "ell": Fraction(1, 2), "gamma": 2, "delta": 3,
    },
    {
        "name": "slow_leakage_bottleneck",
        "X": 16, "d": Fraction(1), "B": Fraction(1),
        "ell": Fraction(2), "gamma": 4, "delta": 1,
    },
    {
        "name": "equal_exponents",
        "X": 10, "d": Fraction(5, 4), "B": Fraction(3, 5),
        "ell": Fraction(1, 4), "gamma": 2, "delta": 2,
    },
    {
        "name": "zero_additive_leakage",
        "X": 9, "d": Fraction(2), "B": Fraction(7, 4),
        "ell": Fraction(0), "gamma": 3, "delta": 5,
    },
    {
        "name": "leakage_only",
        "X": 32, "d": Fraction(2), "B": Fraction(0),
        "ell": Fraction(1), "gamma": 5, "delta": 1,
    },
    {
        "name": "fractional_budget_constants",
        "X": 25, "d": Fraction(5, 3), "B": Fraction(2, 3),
        "ell": Fraction(4, 3), "gamma": 1, "delta": 3,
    },
)


MARGIN_CASES: tuple[dict[str, Any], ...] = (
    {"name": "margin_paid_after_fast_leakage", "case": 0,
     "c": Fraction(1), "eta_D": Fraction(1), "epsilon": Fraction(0)},
    {"name": "margin_leakage_limited", "case": 1,
     "c": Fraction(1), "eta_D": Fraction(2), "epsilon": Fraction(0)},
    {"name": "margin_equal_exponent", "case": 2,
     "c": Fraction(3, 2), "eta_D": Fraction(1), "epsilon": Fraction(0)},
    {"name": "margin_zero_leakage", "case": 3,
     "c": Fraction(1), "eta_D": Fraction(2), "epsilon": Fraction(0)},
)


ENDPOINT_CASES: tuple[dict[str, Any], ...] = (
    {"name": "strictly_paid", "sigma": Fraction(1, 100),
     "eta_D": Fraction(1, 10), "gamma": 4, "delta": 2},
    {"name": "leakage_controls_exponent_but_still_paid", "sigma": Fraction(3, 1000),
     "eta_D": Fraction(1, 10), "gamma": 4, "delta": 1},
    {"name": "borderline_not_paid", "sigma": Fraction(1, 400),
     "eta_D": Fraction(1, 10), "gamma": 4, "delta": 2},
    {"name": "loss_exceeds_saving", "sigma": Fraction(1, 10),
     "eta_D": Fraction(1, 4), "gamma": 1, "delta": Fraction(1, 5)},
)


def compile_case(case: dict[str, Any]) -> dict[str, Any]:
    x = int(case["X"])
    d = Fraction(case["d"])
    b = Fraction(case["B"])
    ell = Fraction(case["ell"])
    gamma = int(case["gamma"])
    delta = int(case["delta"])
    need(x >= 1 and d > 0 and b >= 0 and ell >= 0, "case domain")
    ratio = ell / d
    main = b * inverse_power(x, gamma)
    leakage = ratio * inverse_power(x, delta)
    two_term = main + leakage
    kappa = min(gamma, delta)
    collapsed = (b + ratio) * inverse_power(x, kappa)
    need(two_term <= collapsed, "dominant exponent envelope")
    need(two_term > 0 and collapsed > 0, "positive compiler denominator")
    return {
        "name": case["name"], "X": x,
        "d": fraction_text(d), "B": fraction_text(b),
        "ell": fraction_text(ell), "ell_over_d": fraction_text(ratio),
        "gamma": gamma, "delta": delta, "kappa": kappa,
        "main_term": fraction_text(main),
        "normalized_leakage_term": fraction_text(leakage),
        "two_term_q_bound": fraction_text(two_term),
        "collapsed_q_bound": fraction_text(collapsed),
        "two_term_gain_lower": fraction_text(1 / two_term),
        "collapsed_gain_lower": fraction_text(1 / collapsed),
        "two_term_bound_leq_collapsed": True,
        "equality_witness_available": True,
    }


def compile_margin_case(spec: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    source = cases[int(spec["case"])]
    x = int(source["X"])
    c = Fraction(spec["c"])
    eta = Fraction(spec["eta_D"])
    epsilon = Fraction(spec["epsilon"])
    q_two = parse_fraction(source["two_term_q_bound"])
    q_collapsed = parse_fraction(source["collapsed_q_bound"])
    base = c * c * inverse_power(x, 2 * int(eta)) * inverse_power(
        x, 2 * int(epsilon))
    two = base / q_two
    collapsed = base / q_collapsed
    kappa_half = Fraction(int(source["kappa"]), 2)
    eta_eff = max(Fraction(0), eta - kappa_half)
    need(two >= collapsed, "margin compiler ordering")
    return {
        "name": spec["name"], "source_case": source["name"], "X": x,
        "c": fraction_text(c), "eta_D": fraction_text(eta),
        "epsilon": fraction_text(epsilon), "kappa": source["kappa"],
        "eta_eff": fraction_text(eta_eff),
        "margin_squared_two_term_lower": fraction_text(two),
        "margin_squared_collapsed_lower": fraction_text(collapsed),
        "two_term_is_at_least_collapsed": True,
        "compiler_status": "PROVED_CONDITIONAL",
    }


def compile_endpoint_case(spec: dict[str, Any]) -> dict[str, Any]:
    sigma = Fraction(spec["sigma"])
    eta = Fraction(spec["eta_D"])
    gamma = Fraction(spec["gamma"])
    delta = Fraction(spec["delta"])
    kappa = min(gamma, delta)
    eta_eff = max(Fraction(0), eta - kappa / 2)
    gap = sigma - eta_eff - Fraction(1, 400)
    status = "PAID_STRICT" if gap > 0 else "BORDERLINE_UNPAID" if gap == 0 else "UNPAID"
    return {
        "name": spec["name"], "sigma": fraction_text(sigma),
        "eta_D": fraction_text(eta), "gamma": fraction_text(gamma),
        "delta": fraction_text(delta), "kappa": fraction_text(kappa),
        "eta_eff": fraction_text(eta_eff),
        "strict_gap_after_1_over_400": fraction_text(gap),
        "status": status,
        "strict_condition": "sigma-eta_eff>1/400",
    }


def transfer_parent_rows(parent: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in parent["payload"]["rows"]:
        q = parse_interval(source["normalized_output_ratio_interval"])
        deficit = parse_interval(source["deficit_interval"])
        need(Fraction(0) <= q[0] <= q[1] <= Fraction(4),
             "parent ratio domain")
        need(deficit[0] < 1, "parent deficit domain")
        rows.append({
            "scale": int(source["scale"]), "H": int(source["H"]),
            "Q": int(source["Q"]),
            "comparison_cutoff_z": int(source["comparison_cutoff_z"]),
            "kernel_exponent": int(source["kernel_exponent"]),
            "role": source["role"],
            "q_interval": interval_text(q),
            "deficit_interval": interval_text(deficit),
            "parent_deficit_sign": source["deficit_sign"],
            "source_exact_digest": source["source_exact_digest"],
            "arithmetic": "EXACT_FINITE_COORDINATE_TRANSFER_FROM_TPC279",
        })
    return rows


def theorem_payload(parent: dict[str, Any]) -> dict[str, Any]:
    cases = [compile_case(case) for case in CASES]
    margins = [compile_margin_case(spec, cases) for spec in MARGIN_CASES]
    endpoints = [compile_endpoint_case(spec) for spec in ENDPOINT_CASES]
    rows = transfer_parent_rows(parent)
    need(len(rows) == 12, "transfer row count")
    need(sum(row["parent_deficit_sign"] == "POSITIVE_DEFICIT" for row in rows) == 8,
         "positive transfer census")
    need(sum(row["parent_deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows) == 4,
         "negative transfer census")
    equality = {
        "formal_source_floor": "D=d X^a",
        "formal_output_choice": "G=B X^(-gamma) D + ell X^(a-delta)",
        "normalized_ratio": "G/D=B X^(-gamma)+(ell/d)X^(-delta)",
        "interpretation": "both terms can be simultaneously sharp under the stated hypotheses",
    }
    return {
        "schema": SCHEMA,
        "parameters": {
            "source_exponent": "a (literal route may use a=5/3)",
            "source_floor": "D>=d X^a, d>0",
            "raw_bound": "G<=B X^(-gamma)D + ell X^(a-delta)",
            "coefficient_domain": "B>=0, ell>=0, gamma>=0, delta>=0",
            "normalized_bound": "G/D<=B X^(-gamma)+(ell/d)X^(-delta)",
            "collapsed_exponent": "kappa=min(gamma,delta)",
            "collapsed_constant": "C=B+ell/d",
            "margin_identity": "m^2=(D/G)m_D^2",
            "strict_endpoint_gap": "1/400",
        },
        "exact_theorem": {
            "two_term_gain_compiler": "r>=1/(B X^(-gamma)+(ell/d)X^(-delta))",
            "dominant_exponent_compiler": "r>=(B+ell/d)^(-1)X^kappa",
            "margin_squared_compiler": "m^2>=m_D^2/(B X^(-gamma)+(ell/d)X^(-delta))",
            "effective_margin_loss": "eta_eff=max(0,eta_D-kappa/2)",
            "conditional_endpoint": "sigma-eta_eff>1/400",
            "sharpness": "equality source/output family prevents a universal stronger two-term bound",
            "leakage_obstruction": "delta<gamma makes additive leakage the asymptotic bottleneck",
        },
        "equality_witness": equality,
        "budget_cases": cases,
        "margin_cases": margins,
        "endpoint_cases": endpoints,
        "finite_transfer": {
            "parent_schema": PARENT_SCHEMA,
            "parent_result_sha256": PARENT_RESULT_SHA256,
            "total_rows": len(rows),
            "positive_deficit_rows": sum(
                row["parent_deficit_sign"] == "POSITIVE_DEFICIT" for row in rows),
            "negative_deficit_rows": sum(
                row["parent_deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows),
            "fixed_power_credit": 0,
            "asymptotic_promotion": "REFUTED_SCOPED",
        },
        "rows": rows,
        "firewall": {
            "TPC280_TWO_TERM_COMPILER": "PROVED_CONDITIONAL",
            "TPC280_LEAKAGE_BOTTLENECK": "PROVED_CONDITIONAL_DELTA_LT_GAMMA",
            "TPC280_SHARPNESS": "PROVED_CONDITIONAL_EQUALITY_FAMILY",
            "TPC280_FINITE_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC280_FIXED_POWER_CREDIT": 0,
            "TPC280_ARITHMETIC_ADVANCE": "NO",
            "TPC280_L2": "NONE",
            "TPC280_FULL_GATE_B": "OPEN",
            "TPC280_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC280_TWIN_PRIME_RESULT": "NONE",
            "TPC280_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    parent = load_parent()
    payload = theorem_payload(parent)
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def validate(data: dict[str, Any]) -> None:
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(data.get("payload_sha256") ==
         hashlib.sha256(canonical(payload)).hexdigest(), "payload hash")
    exact = payload["exact_theorem"]
    need(exact["two_term_gain_compiler"] ==
         "r>=1/(B X^(-gamma)+(ell/d)X^(-delta))" and
         exact["dominant_exponent_compiler"] ==
         "r>=(B+ell/d)^(-1)X^kappa" and
         exact["effective_margin_loss"] ==
         "eta_eff=max(0,eta_D-kappa/2)", "theorem fields")
    transfer = payload["finite_transfer"]
    need(transfer == {
        "parent_schema": PARENT_SCHEMA,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "total_rows": 12, "positive_deficit_rows": 8,
        "negative_deficit_rows": 4, "fixed_power_credit": 0,
        "asymptotic_promotion": "REFUTED_SCOPED",
    }, "transfer fields")
    cases = payload["budget_cases"]
    need(cases == [compile_case(case) for case in CASES], "budget cases")
    need(payload["margin_cases"] ==
         [compile_margin_case(spec, cases) for spec in MARGIN_CASES],
         "margin cases")
    need(payload["endpoint_cases"] ==
         [compile_endpoint_case(spec) for spec in ENDPOINT_CASES],
         "endpoint cases")
    need(payload["rows"] == transfer_parent_rows(load_parent()),
         "parent transfer rows")
    need(payload["firewall"]["TPC280_FIXED_POWER_CREDIT"] == 0 and
         payload["firewall"]["TPC280_FULL_GATE_B"] == "OPEN",
         "firewall")


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    validate(data)
    need(data == document(), "certificate is not reproducible from parent")
    print("TPC280_CERTIFICATE=PASS theorem=TWO_TERM leakage_bottleneck=DELTA_LT_GAMMA "
          "transfer_rows=12 positive_deficit=8 negative_deficit=4 fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC280_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
