#!/usr/bin/env python3
"""Mutation stress for the TPC-333 source polarization certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc333_certificate.json"
SCHEMA = "TPC333_SOURCE_POLARIZATION_CROSS_TERM_V1"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1, "version")
    need(document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER", "status")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(len(payload.get("rows", [])) == 6, "rows")
    need(len(payload.get("growth_pairs", [])) == 4, "growth pairs")
    need(payload.get("summary", {}).get("kappa_within_[.35,.37]") == 6,
         "summary")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC333_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC333_SOURCE_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC333_FIXED_POWER_CREDIT") == 0, "firewall")
    need(payload.get("exact_anchor", {}).get("identity_exact") is True,
         "anchor")


def main() -> int:
    try:
        document = json.loads(RESULT.read_bytes())
        validate(document)
        mutations = []
        item = copy.deepcopy(document); item["payload"]["rows"] = item["payload"]["rows"][:-1]; mutations.append(item)
        item = copy.deepcopy(document); item["payload"]["growth_pairs"][0]["cross_growth"] = "0"; mutations.append(item)
        item = copy.deepcopy(document); item["payload"]["summary"]["kappa_within_[.35,.37]"] = 5; mutations.append(item)
        item = copy.deepcopy(document); item["payload"]["claim_firewall"]["TPC333_ARITHMETIC_ADVANCE"] = "YES"; mutations.append(item)
        item = copy.deepcopy(document); item["payload"]["exact_anchor"]["identity_exact"] = False; mutations.append(item)
        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC333_STRESS=PASS mutations=5 rejected=5 "
              "windows=6 growth_pairs=4 firewall=fail_closed")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC333_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
