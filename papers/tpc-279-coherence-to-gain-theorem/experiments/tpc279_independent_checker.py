#!/usr/bin/env python3
"""Independent interval and sharpness replay for TPC-279."""

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
PROJECT = ROOT / "papers/tpc-279-coherence-to-gain-theorem"
PARENT_RESULT = ROOT / "papers/tpc-278-cross-scale-gain-stability/results/tpc278_certificate.json"
RESULT = PROJECT / "results/tpc279_certificate.json"
PARENT_RESULT_SHA256 = "ba51dc737f07ce73ba0c60d5e98af84b7e06f1dce6754004df838e072ae28acc"
PARENT_SCHEMA = "TPC278_CROSS_SCALE_GAIN_STABILITY_CERTIFICATE_V1"
SCHEMA = "TPC279_COHERENCE_TO_GAIN_THEOREM_CERTIFICATE_V1"
STATUS = "PROVED_EXACT_MINIMAL_COHERENCE_TO_GAIN_CRITERION_PLUS_NUMERICALLY_CERTIFIED_TRANSFER"


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


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def text_pair(value: tuple[Fraction, Fraction]) -> list[str]:
    return [f"{value[0].numerator}/{value[0].denominator}",
            f"{value[1].numerator}/{value[1].denominator}"]


def load_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical JSON: " + str(path))
    return data


def expected_witnesses() -> list[dict[str, Any]]:
    result = []
    for mu in (Fraction(0), Fraction(1, 2), Fraction(1)):
        diagonal = Fraction(4)
        signed = 4 * (1 + 3 * mu)
        result.append({
            "mu": f"{mu.numerator}/{mu.denominator}",
            "gram_diagonal": "4/1",
            "gram_sum": f"{signed.numerator}/{signed.denominator}",
            "ratio_G_over_D": f"{(signed / diagonal).numerator}/{(signed / diagonal).denominator}",
            "gain_D_over_G": f"{(diagonal / signed).numerator}/{(diagonal / signed).denominator}",
            "pairwise_bound": f"{(1 + 3 * mu).numerator}/{(1 + 3 * mu).denominator}",
            "eigenvalues": [f"{(1 - mu).numerator}/{(1 - mu).denominator}"] * 3 +
                           [f"{(1 + 3 * mu).numerator}/{(1 + 3 * mu).denominator}"],
            "bound_is_sharp": True,
        })
    epsilon = Fraction(1, 10)
    diagonal = 3 + (3 - epsilon) ** 2
    signed = epsilon ** 2
    result.append({
        "epsilon": "1/10",
        "packet_scalars": ["1", "1", "1", "-29/10"],
        "D": f"{diagonal.numerator}/{diagonal.denominator}",
        "G": f"{signed.numerator}/{signed.denominator}",
        "gain_D_over_G": f"{(diagonal / signed).numerator}/{(diagonal / signed).denominator}",
        "mu": "1", "deficit": f"{(1 - signed / diagonal).numerator}/{(1 - signed / diagonal).denominator}",
        "interpretation": "near-cancellation can create arbitrarily large gain only when G/D is independently small",
    })
    return result


def check() -> None:
    parent = load_json(PARENT_RESULT)
    need(digest(PARENT_RESULT.read_bytes()) == PARENT_RESULT_SHA256,
         "parent hash")
    need(parent["payload"]["schema"] == PARENT_SCHEMA and
         len(parent["payload"]["rows"]) == 12, "parent schema/rows")
    data = load_json(RESULT)
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS, "certificate header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA, "certificate schema")
    need(data["payload_sha256"] == digest(canonical(payload)), "payload hash")
    exact = payload["exact_theorem"]
    need(exact == {
        "universal_ratio": "0 <= G/D <= 4",
        "deficit_identity": "Delta=1-G/D=-2E/D",
        "gain_identity": "r=(1-Delta)^(-1)",
        "power_gain_equivalence": "r>=b*X^gamma iff G/D<=b^(-1)*X^(-gamma)",
        "pairwise_coherence_envelope": "G/D<=min(4,1+3*mu)",
        "pairwise_gain_floor": "r>=max(1/4,1/(1+3*mu))",
        "sharpness": "all three envelopes are attained by explicit Gram/scalar witnesses",
        "minimal_source_input": "a lower bound Delta>=1-b^(-1)*X^(-gamma), equivalently an upper bound on G/D",
    }, "exact theorem fields")
    transfer = payload["finite_transfer"]
    need(transfer["parent_schema"] == PARENT_SCHEMA and
         transfer["parent_result_sha256"] == PARENT_RESULT_SHA256 and
         transfer["total_rows"] == 12 and
         transfer["positive_deficit_rows"] == 8 and
         transfer["negative_deficit_rows"] == 4 and
         transfer["fixed_power_credit"] == 0, "transfer fields")
    rows = payload["rows"]
    need(len(rows) == len(parent["payload"]["rows"]) == 12, "row count")
    for source, row in zip(parent["payload"]["rows"], rows):
        gain = interval(source["gain_interval"])
        q = (Fraction(1, gain[1]), Fraction(1, gain[0]))
        reciprocal_delta = (1 - q[1], 1 - q[0])
        stored_delta = interval(source["cancellation_fraction_interval"])
        need(max(reciprocal_delta[0], stored_delta[0]) <=
             min(reciprocal_delta[1], stored_delta[1]),
             "deficit interval overlap")
        delta = (max(reciprocal_delta[0], stored_delta[0]),
                 min(reciprocal_delta[1], stored_delta[1]))
        need(row["gain_interval"] == text_pair(gain), "gain transfer")
        need(row["normalized_output_ratio_interval"] == text_pair(q), "reciprocal interval")
        need(row["deficit_interval"] == text_pair(delta), "deficit interval")
        need(row["parent_cross_sign"] == source["cross_sign"] and
             row["source_exact_digest"] == source["exact_replay_digest"], "parent identity")
        expected_sign = ("POSITIVE_DEFICIT" if delta[0] > 0 else
                         "NEGATIVE_DEFICIT" if delta[1] < 0 else "ZERO_OR_CROSSING")
        need(row["deficit_sign"] == expected_sign, "deficit sign")
        need(0 <= q[0] <= q[1] <= 4 and delta[0] < 1, "ratio domain")
    need(sum(row["deficit_sign"] == "POSITIVE_DEFICIT" for row in rows) == 8 and
         sum(row["deficit_sign"] == "NEGATIVE_DEFICIT" for row in rows) == 4,
         "sign census")
    need(payload["sharpness_witnesses"] == expected_witnesses(),
         "sharpness witnesses")
    firewall = payload["firewall"]
    need(firewall["TPC279_PAIRWISE_COHERENCE_POWER"] ==
         "REFUTED_EXACT_BY_ORTHOGONAL_WITNESS" and
         firewall["TPC279_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC279_SOURCE_LEVEL_DEFICIT"] == "OPEN_ASYMPTOTIC",
         "firewall")
    print("TPC279_INDEPENDENT_CHECK=PASS rows=12 exact_reciprocal_transfers=12 "
          "sharp_witnesses=4 positive_deficit=8 negative_deficit=4")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC279_INDEPENDENT_CHECK=FAIL: " + str(error))
