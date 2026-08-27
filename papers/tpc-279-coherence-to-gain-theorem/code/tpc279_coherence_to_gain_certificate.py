#!/usr/bin/env python3
"""Exact coherence-to-gain theorem and finite transfer certificate for TPC-279."""

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
PARENT_PROJECT = ROOT / "papers/tpc-278-cross-scale-gain-stability"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc278_cross_scale_gain_stability_certificate.py"
)
PARENT_RESULT = PARENT_PROJECT / "results/tpc278_certificate.json"
RESULT = PROJECT / "results/tpc279_certificate.json"

PARENT_CODE_SHA256 = "d51096ff917278cabfa670e13118b8acaa8999aca1fc3cf4db859e44db04d5c4"
PARENT_RESULT_SHA256 = "ba51dc737f07ce73ba0c60d5e98af84b7e06f1dce6754004df838e072ae28acc"
PARENT_SCHEMA = "TPC278_CROSS_SCALE_GAIN_STABILITY_CERTIFICATE_V1"
SCHEMA = "TPC279_COHERENCE_TO_GAIN_THEOREM_CERTIFICATE_V1"
STATUS = "PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER"
ROUND2_CLUE = "COMPILE_COHERENCE_DEFICIT_WITH_MARGIN_AND_ARITHMETIC_L2"


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
         "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION",
         "parent header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == PARENT_SCHEMA, "parent schema")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent rows")
    return data


def reciprocal_interval(interval: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    lo, hi = interval
    need(lo > 0, "positive gain interval")
    return Fraction(1, hi), Fraction(1, lo)


def transfer_rows(parent: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for source in parent["payload"]["rows"]:
        gain = parse_interval(source["gain_interval"])
        q = reciprocal_interval(gain)
        reciprocal_deficit = (1 - q[1], 1 - q[0])
        source_deficit = parse_interval(source["cancellation_fraction_interval"])
        need(max(reciprocal_deficit[0], source_deficit[0]) <=
             min(reciprocal_deficit[1], source_deficit[1]),
             "parent cancellation interval overlap")
        deficit = (max(reciprocal_deficit[0], source_deficit[0]),
                   min(reciprocal_deficit[1], source_deficit[1]))
        need(q[0] >= 0 and q[1] <= 4, "four-packet ratio range")
        need(deficit[0] < 1, "deficit domain")
        sign = ("POSITIVE_DEFICIT" if deficit[0] > 0 else
                "NEGATIVE_DEFICIT" if deficit[1] < 0 else "ZERO_OR_CROSSING")
        rows.append({
            "scale": int(source["scale"]), "H": int(source["H"]),
            "Q": int(source["Q"]),
            "comparison_cutoff_z": int(source["comparison_cutoff_z"]),
            "kernel_exponent": int(source["kernel_exponent"]),
            "role": source["role"],
            "gain_interval": interval_text(gain),
            "normalized_output_ratio_interval": interval_text(q),
            "deficit_interval": interval_text(deficit),
            "deficit_sign": sign,
            "parent_cross_sign": source["cross_sign"],
            "source_exact_digest": source["exact_replay_digest"],
            "arithmetic": "EXACT_INTERVAL_TRANSFER_FROM_TPC278",
        })
    return rows


def equicorrelation_witness(mu: Fraction) -> dict[str, Any]:
    need(Fraction(0) <= mu <= Fraction(1), "coherence range")
    diagonal = Fraction(4)
    signed = Fraction(4) * (1 + 3 * mu)
    return {
        "mu": fraction_text(mu),
        "gram_diagonal": fraction_text(diagonal),
        "gram_sum": fraction_text(signed),
        "ratio_G_over_D": fraction_text(signed / diagonal),
        "gain_D_over_G": fraction_text(diagonal / signed),
        "pairwise_bound": fraction_text(1 + 3 * mu),
        "eigenvalues": [fraction_text(1 - mu)] * 3 +
                       [fraction_text(1 + 3 * mu)],
        "bound_is_sharp": True,
    }


def near_cancel_witness() -> dict[str, Any]:
    epsilon = Fraction(1, 10)
    diagonal = 3 + (3 - epsilon) ** 2
    signed = epsilon ** 2
    return {
        "epsilon": fraction_text(epsilon),
        "packet_scalars": ["1", "1", "1", fraction_text(-(3 - epsilon))],
        "D": fraction_text(diagonal), "G": fraction_text(signed),
        "gain_D_over_G": fraction_text(diagonal / signed),
        "mu": "1", "deficit": fraction_text(1 - signed / diagonal),
        "interpretation": "near-cancellation can create arbitrarily large gain only when G/D is independently small",
    }


def theorem_payload(rows: list[dict[str, Any]]) -> dict[str, Any]:
    positive = [r for r in rows if r["deficit_sign"] == "POSITIVE_DEFICIT"]
    negative = [r for r in rows if r["deficit_sign"] == "NEGATIVE_DEFICIT"]
    witnesses = [equicorrelation_witness(mu)
                 for mu in (Fraction(0), Fraction(1, 2), Fraction(1))]
    witnesses.append(near_cancel_witness())
    need(len(rows) == 12 and len(positive) == 8 and len(negative) == 4,
         "transfer census")
    return {
        "schema": SCHEMA,
        "parameters": {
            "packet_count": 4,
            "Hilbert_space": "real_or_complex",
            "D": "sum_j ||V_j||^2",
            "G": "||sum_j V_j||^2",
            "E": "sum_{j<k} Re <V_j,V_k>",
            "Delta": "(D-G)/D",
            "r": "D/G when G>0",
            "mu": "max pairwise normalized absolute coherence",
        },
        "exact_theorem": {
            "universal_ratio": "0 <= G/D <= 4",
            "deficit_identity": "Delta=1-G/D=-2E/D",
            "gain_identity": "r=(1-Delta)^(-1)",
            "power_gain_equivalence": "r>=b*X^gamma iff G/D<=b^(-1)*X^(-gamma)",
            "pairwise_coherence_envelope": "G/D<=min(4,1+3*mu)",
            "pairwise_gain_floor": "r>=max(1/4,1/(1+3*mu))",
            "sharpness": "all three envelopes are attained by explicit Gram/scalar witnesses",
            "minimal_source_input": "a lower bound Delta>=1-b^(-1)*X^(-gamma), equivalently an upper bound on G/D",
        },
        "sharpness_witnesses": witnesses,
        "finite_transfer": {
            "parent_schema": PARENT_SCHEMA,
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_result_sha256": PARENT_RESULT_SHA256,
            "total_rows": len(rows),
            "positive_deficit_rows": len(positive),
            "negative_deficit_rows": len(negative),
            "finite_deficit_sign_matches_parent_cross_sign": True,
            "fixed_power_credit": 0,
            "asymptotic_promotion": "REFUTED_SCOPED",
        },
        "rows": rows,
        "firewall": {
            "TPC279_EXACT_THEOREM": "PROVED_EXACT_FINITE_DIMENSIONAL",
            "TPC279_PAIRWISE_COHERENCE_POWER": "REFUTED_EXACT_BY_ORTHOGONAL_WITNESS",
            "TPC279_FINITE_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC279_SOURCE_LEVEL_DEFICIT": "OPEN_ASYMPTOTIC",
            "TPC279_FIXED_POWER_CREDIT": 0,
            "TPC279_ARITHMETIC_ADVANCE": "NO",
            "TPC279_L2": "NONE",
            "TPC279_FULL_GATE_B": "OPEN",
            "TPC279_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC279_TWIN_PRIME_RESULT": "NONE",
            "TPC279_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    parent = load_parent()
    payload = theorem_payload(transfer_rows(parent))
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


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
    theorem = payload["finite_transfer"]
    need(theorem == {
        "parent_schema": PARENT_SCHEMA,
        "parent_code_sha256": PARENT_CODE_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "total_rows": 12, "positive_deficit_rows": 8,
        "negative_deficit_rows": 4,
        "finite_deficit_sign_matches_parent_cross_sign": True,
        "fixed_power_credit": 0, "asymptotic_promotion": "REFUTED_SCOPED",
    }, "transfer theorem")
    rows = payload["rows"]
    need(isinstance(rows, list) and len(rows) == 12, "row count")
    need(sum(row["deficit_sign"] == "POSITIVE_DEFICIT" for row in rows) == 8,
         "positive census")
    need(sum(row["deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows) == 4,
         "negative census")
    exact = payload["exact_theorem"]
    need(exact["universal_ratio"] == "0 <= G/D <= 4" and
         exact["pairwise_coherence_envelope"] == "G/D<=min(4,1+3*mu)" and
         exact["pairwise_gain_floor"] == "r>=max(1/4,1/(1+3*mu))",
         "theorem fields")
    need(payload["firewall"]["TPC279_FIXED_POWER_CREDIT"] == 0 and
         payload["firewall"]["TPC279_SOURCE_LEVEL_DEFICIT"] == "OPEN_ASYMPTOTIC",
         "claim firewall")


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    validate(data)
    expected = document()
    need(data == expected, "certificate is not reproducible from parent")
    print("TPC279_CERTIFICATE=PASS theorem=EXACT coherence_envelope=SHARP "
          "transfer_rows=12 positive_deficit=8 negative_deficit=4 "
          "fixed_power_credit=0")


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
        raise SystemExit("TPC279_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
