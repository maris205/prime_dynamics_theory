#!/usr/bin/env python3
"""Fail-closed mutation stress for TPC-338."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc338_certificate.json"
SCHEMA = "TPC338_GROWING_CONTROL_COVARIANCE_SPECTRUM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def reseal(document: dict[str, Any]) -> None:
    document["payload_sha256"] = hashlib.sha256(
        canonical(document["payload"])).hexdigest()


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1, "version")
    need(document.get("claim_status") == STATUS, "status")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "digest")
    need(payload.get("finite_audit") == {
        "rows": 6, "origins": 2, "scales": 3, "five_controls": 5,
        "nine_controls": 9, "categories": 4, "nested_decompositions": 48,
        "normalized_spectrum_comparisons": 6, "pair_sign_ensembles": 2,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    need(len(payload.get("rows", [])) == 6, "rows")
    for row in payload["rows"]:
        need(len(row.get("controls", [])) == 9 and
             row.get("five_control", {}).get("control_count") == 5 and
             row.get("nine_control", {}).get("control_count") == 9,
             "control geometry")
        need(float(row["five_control"]["full_response"]["centered_fraction"]) > 0.75 and
             float(row["nine_control"]["full_response"]["centered_fraction"]) > 0.85,
             "energy dominance")
        need(float(row["five_control"]["pair_covariance"][
            "twin_prime__zero_support"]) < 0 and
             float(row["nine_control"]["pair_covariance"][
                 "twin_prime__zero_support"]) > 0, "sign reversal")
    summary = payload.get("summary", {})
    need(summary.get("energy_dominance_rows") == 6 and
         summary.get("twin_zero_sign_reversal") is True and
         float(summary.get("nine_centered_fraction_min", 0)) > 0.85,
         "summary")
    need(payload.get("exact_anchor", {}).get("identity_exact") is True,
         "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC338_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC338_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC338_FULL_GATE_B") == "OPEN", "firewall")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes())
        validate(original)
        mutations: list[dict[str, Any]] = []
        item = copy.deepcopy(original)
        item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["nine_control"]["full_response"]["centered_fraction"] = "0.2"
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["summary"]["twin_zero_sign_reversal"] = False
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["controls"] = item["payload"]["rows"][0]["controls"][:-1]
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC338_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item); mutations.append(item)
        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC338_STRESS=PASS mutations=5 rejected=5 "
              "nested_sign_guard=1 semantic_guards=4")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC338_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
