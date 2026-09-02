#!/usr/bin/env python3
"""Fail-closed mutation stress for the TPC-337 covariance certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc337_certificate.json"
SCHEMA = "TPC337_CONTROL_COVARIANCE_MASKED_RESPONSE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE"


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
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    audit = payload.get("finite_audit", {})
    need(audit == {"rows": 6, "origins": 2, "scales": 3, "controls": 5,
                   "categories": 4, "class_decomposition_observations": 24,
                   "pair_covariance_observations": 36,
                   "full_decomposition_observations": 6,
                   "covariance_spectrum_observations": 6,
                   "fixed_power_credit": 0, "arithmetic_advance": "NO"},
         "finite audit")
    need(len(payload.get("rows", [])) == 6, "row census")
    for row in payload["rows"]:
        need(len(row.get("controls", [])) == 5 and
             len(row.get("class_response", {})) == 4 and
             len(row.get("covariance_eigenvalues", [])) == 4,
             "row geometry")
        need(float(row["full_response"]["centered_fraction"]) > 0.75 and
             float(row["full_response"]["coherent_fraction"]) < 0.25,
             "row covariance dominance")
    summary = payload.get("summary", {})
    need(float(summary.get("full_centered_fraction_min", 0)) > 0.75 and
         float(summary.get("full_coherent_fraction_max", 1)) < 0.25,
         "summary bounds")
    signs = summary.get("covariance_pair_signs", {})
    need(signs.get("twin_prime__non_twin_prime_shift", {}).get("positive") == 6 and
         signs.get("twin_prime__zero_support", {}).get("negative") == 6 and
         signs.get("non_twin_prime_shift__zero_support", {}).get("negative") == 6,
         "sign census")
    need(payload.get("exact_anchor", {}).get("identity_exact") is True,
         "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC337_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC337_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC337_SOURCE_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC337_FULL_GATE_B") == "OPEN", "firewall")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes())
        validate(original)
        mutations: list[dict[str, Any]] = []

        item = copy.deepcopy(original)
        item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["full_response"]["centered_fraction"] = "0.1"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["covariance_pair_signs"][
            "twin_prime__zero_support"]["negative"] = 5
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["controls"] = item["payload"]["rows"][0]["controls"][:-1]
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["exact_anchor"]["identity_exact"] = False
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC337_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item)
        mutations.append(item)

        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC337_STRESS=PASS mutations=6 rejected=6 "
              "semantic_guards=5 firewall=fail_closed")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC337_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
