#!/usr/bin/env python3
"""Fail-closed mutation stress for TPC-339."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc339_certificate.json"
SCHEMA = "TPC339_MASK_AWARE_FROBENIUS_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE"


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
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "digest")
    need(payload.get("finite_audit") == {
        "rows": 6, "origins": 2, "scales": 3, "controls": 9,
        "categories": 4, "records": 216, "nonempty_records": 198,
        "bound_checks": 216, "bound_violations": 0,
        "broad_mask_records": 162, "fixed_power_credit": 0,
        "arithmetic_advance": "NO"}, "audit")
    need(len(payload.get("rows", [])) == 6, "rows")
    for row in payload["rows"]:
        need(len(row.get("records", [])) == 36 and
             len(row.get("controls", [])) == 9, "row geometry")
        for record in row["records"]:
            need(record.get("bound_holds") is True and
                 float(record["envelope_gap"]) >= -1.0e-4,
                 "record bound")
    summary = payload.get("summary", {})
    need(summary.get("bound_violations") == 0 and
         summary.get("nonempty_records") == 198 and
         float(summary.get("broad_mask_occupancy_max", 1)) < 0.2,
         "summary")
    need(payload.get("exact_anchor", {}).get("equality_exact") is True,
         "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC339_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC339_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC339_FULL_GATE_B") == "OPEN", "firewall")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes()); validate(original)
        mutations: list[dict[str, Any]] = []
        item = copy.deepcopy(original)
        item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["records"][0]["bound_holds"] = False
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["summary"]["broad_mask_occupancy_max"] = "0.5"
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["finite_audit"]["bound_violations"] = 1
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC339_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item); mutations.append(item)
        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC339_STRESS=PASS mutations=5 rejected=5 "
              "bound_guard=2 semantic_guards=3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC339_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
