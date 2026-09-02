#!/usr/bin/env python3
"""Mutation stress for TPC-335's masked norm certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc335_certificate.json"


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
         "NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM", "status")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC335_TWIN_ISOLATED_SOURCE_NORM_V1", "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "digest")
    need(len(payload.get("rows", [])) == 6, "rows")
    need(payload.get("summary", {}).get(
        "twin_norm_fraction_between_0.09_0.13") == 6, "summary")
    fw = payload.get("claim_firewall", {})
    need(fw.get("TPC335_ARITHMETIC_ADVANCE") == "NO" and
         fw.get("TPC335_SOURCE_UNIFORM_L2") == "OPEN" and
         fw.get("TPC335_FIXED_POWER_CREDIT") == 0, "firewall")
    need(payload.get("exact_anchor", {}).get("partition_exact") is True, "anchor")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes()); validate(original)
        mutations = []
        item = copy.deepcopy(original); item["payload"]["rows"] = item["payload"]["rows"][:-1]; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["rows"][0]["twin_residual_norm_fraction"] = "0"; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["summary"]["twin_norm_fraction_between_0.09_0.13"] = 5; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["claim_firewall"]["TPC335_ARITHMETIC_ADVANCE"] = "YES"; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["exact_anchor"]["partition_exact"] = False; mutations.append(item)
        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == 5, "mutation rejection")
        print("TPC335_STRESS=PASS mutations=5 rejected=5 windows=6 "
              "categories=4 firewall=fail_closed")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC335_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
