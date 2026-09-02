#!/usr/bin/env python3
"""Fail-closed mutation stress for TPC-340."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc340_certificate.json"
SCHEMA = "TPC340_SCHUR_FROBENIUS_HYBRID_ENVELOPE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE"


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
        "schur_branch_records": 54, "frobenius_branch_records": 162,
        "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
    need(len(payload.get("rows", [])) == 6, "rows")
    for row in payload["rows"]:
        need(len(row.get("records", [])) == 36 and
             row.get("branch_counts") == {"FROBENIUS": 27, "SCHUR": 9},
             "row geometry")
        for item in row["records"]:
            need(item.get("bound_holds") is True and
                 float(item["hybrid_gap"]) >= -1.0e-4,
                 "bound record")
    summary = payload.get("summary", {})
    need(summary.get("bound_violations") == 0 and
         summary.get("branch_total") == {"FROBENIUS": 162, "SCHUR": 54} and
         float(summary.get("broad_hybrid_occupancy_max", 1)) < 0.2,
         "summary")
    need(payload.get("exact_anchor", {}).get("inequality_exact") is True,
         "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC340_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC340_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC340_FULL_GATE_B") == "OPEN", "firewall")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes()); validate(original)
        mutations: list[dict[str, Any]] = []
        item = copy.deepcopy(original); item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["records"][0]["bound_holds"] = False
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["summary"]["branch_total"]["SCHUR"] = 53
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["summary"]["broad_hybrid_occupancy_max"] = "0.5"
        reseal(item); mutations.append(item)
        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC340_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item); mutations.append(item)
        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC340_STRESS=PASS mutations=5 rejected=5 "
              "hybrid_bound_guard=1 branch_guard=1 semantic_guards=3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC340_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
