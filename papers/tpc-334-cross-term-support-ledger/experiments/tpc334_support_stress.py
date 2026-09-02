#!/usr/bin/env python3
"""Fail-closed mutation stress for TPC-334."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc334_certificate.json"


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
         "NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER", "status")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC334_CROSS_TERM_SUPPORT_LEDGER_V1",
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(len(payload.get("rows", [])) == 6 and
         len(payload.get("protocol", {}).get("categories", [])) == 4,
         "geometry")
    need(payload.get("summary", {}).get("twin_fraction_below_0.10") == 6,
         "twin census")
    fw = payload.get("claim_firewall", {})
    need(fw.get("TPC334_ARITHMETIC_ADVANCE") == "NO" and
         fw.get("TPC334_SOURCE_UNIFORM_L2") == "OPEN" and
         fw.get("TPC334_FIXED_POWER_CREDIT") == 0, "firewall")
    need(payload.get("exact_anchor", {}).get("partition_exact") is True,
         "anchor")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes())
        validate(original)
        mutations = []
        item = copy.deepcopy(original); item["payload"]["rows"] = item["payload"]["rows"][:-1]; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["rows"][0]["support"]["twin_prime"]["cross_mass_fraction"] = "0"; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["summary"]["twin_fraction_below_0.10"] = 5; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["claim_firewall"]["TPC334_ARITHMETIC_ADVANCE"] = "YES"; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["exact_anchor"]["partition_exact"] = False; mutations.append(item)
        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == 5, "mutation rejection")
        print("TPC334_STRESS=PASS mutations=5 rejected=5 windows=6 "
              "categories=4 firewall=fail_closed")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC334_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
