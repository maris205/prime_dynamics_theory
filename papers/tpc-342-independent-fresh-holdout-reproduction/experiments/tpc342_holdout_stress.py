#!/usr/bin/env python3
"""Fail-closed mutation stress for TPC-342."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc342_certificate.json"
SCHEMA = "TPC342_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION"


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
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(payload.get("finite_audit") == {
        "rows": 3, "origins": 3, "scales": 1, "controls": 9,
        "categories": 4, "raw_records": 108,
        "nonempty_raw_records": 81,
        "in_sample_projection_records": 3,
        "leave_one_control_out_records": 27,
        "rank_failures": 0, "fixed_power_credit": 0,
        "arithmetic_advance": "NO"}, "audit")
    rows = payload.get("rows", [])
    need(len(rows) == 3, "row count")
    for row in rows:
        need(row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36 and
             len(row.get("holdout", [])) == 9, "row geometry")
        need(row.get("in_sample", {}).get("identity_holds") is True and
             row.get("in_sample", {}).get("nuisance_rank") in (2, 3),
             "in-sample geometry")
        for item in row["holdout"]:
            need(item.get("identity_holds") is True and
                 item.get("nuisance_rank") in (2, 3), "holdout geometry")
    summary = payload.get("summary", {})
    need(summary.get("rank_failures") == 0 and
         summary.get("raw_records") == 108 and
         summary.get("nonempty_raw_records") == 81 and
         summary.get("holdout_records") == 27 and
         summary.get("rank_values") == [2], "summary census")
    need(float(summary.get("in_sample_retention_max", 1)) < 0.30 and
         float(summary.get("holdout_retention_min", 0)) > 0.40,
         "decision guards")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("identity_exact") is True and
         anchor.get("target_energy") == "3" and
         anchor.get("residual_energy") == "1", "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC342_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC342_CONTROL_STABILITY") == "REFUTED_SCOPED" and
         firewall.get("TPC342_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC342_FULL_GATE_B") == "OPEN", "firewall")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes())
        validate(original)
        mutations: list[dict[str, Any]] = []

        item = copy.deepcopy(original)
        item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["rows"][0]["cutoff_safe"] = False
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["in_sample_retention_max"] = "0.9"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["holdout_retention_min"] = "0.1"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["finite_audit"]["rank_failures"] = 1
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC342_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item)
        mutations.append(item)

        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC342_STRESS=PASS mutations=6 rejected=6 rank_guard=1 "
              "holdout_guard=1 cutoff_guard=1 semantic_guards=3")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC342_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
