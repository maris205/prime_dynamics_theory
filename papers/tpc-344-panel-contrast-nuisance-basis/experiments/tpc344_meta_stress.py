#!/usr/bin/env python3
"""Mutation stress for the TPC-344 certificate schema and claim firewall."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc344_certificate.json"
SCHEMA = "TPC344_PANEL_CONTRAST_NUISANCE_BASIS_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PANEL_CONTRAST_BASIS_AUDIT"
ORIGINS = [48097, 48609, 49217, 40097, 40609, 41121]


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
        "panels": 2, "rows": 6, "origins": 6, "scales": 1,
        "controls": 9, "categories": 4, "raw_records": 216,
        "nonempty_raw_records": 171, "in_sample_records": 6,
        "holdout_records": 18, "crossfit_directions": 4,
        "basis_columns_declared": 6, "basis_rank_observed": 5,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }, "finite audit")
    protocol = payload.get("protocol", {})
    need(protocol.get("panel_sign_vector") == [1, -1] and
         protocol.get("scale") == 1024 and
         protocol.get("operator") == {
             "law": "all_plus", "Q": 54,
             "kernel_exponent": 1, "height": 66}, "protocol")
    rows = payload.get("rows", [])
    need(len(rows) == 6 and [row.get("origin") for row in rows] == ORIGINS,
         "row origins")
    for row in rows:
        need(row.get("source_interval") == [
            row["origin"], row["origin"] + 511] and
             row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36 and
             len(row.get("holdout", [])) == 9 and
             row.get("in_sample", {}).get("identity_holds") is True,
             "row geometry")
    baseline = payload.get("baseline", {})
    contrast = payload.get("panel_contrast", {})
    for key in ("row_block_raw", "row_block_equal_row", "shared_raw",
                "shared_equal_row"):
        need(baseline.get(key, {}).get("identity_holds") is True,
             "baseline identity")
    for key in ("contrast_raw", "contrast_equal_row",
                "adaptive_raw", "adaptive_equal_row"):
        need(contrast.get(key, {}).get("identity_holds") is True,
             "contrast identity")
    summary = payload.get("summary", {})
    need(float(summary.get("contrast_raw_retention", 1)) < 0.30 and
         float(summary.get("contrast_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("holdout_retention_min", 0)) > 0.40 and
         float(summary.get("crossfit_retention_min", 0)) > 0.30 and
         summary.get("raw_guard") == "PASS_FINITE_SCOPED" and
         summary.get("weighting_stability") == "REFUTED_SCOPED" and
         summary.get("crossfit_transfer") == "REFUTED_SCOPED",
         "summary guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC344_CONTRAST_SPAN_IDENTITY") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC344_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC344_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC344_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC344_TWIN_PRIME_RESULT") == "NONE",
         "firewall")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("identity_exact") is True and
         anchor.get("projected_energy") == "2" and
         anchor.get("residual_energy") == "2", "anchor")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes())
        need(RESULT.read_bytes() == canonical(original), "original canonicality")
        validate(original)
        mutations: list[dict[str, Any]] = []

        item = copy.deepcopy(original)
        item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["protocol"]["panel_sign_vector"] = [1, 1]
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["contrast_raw_retention"] = "0.4"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["contrast_equal_row_retention"] = "0.1"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["holdout_retention_min"] = "0.1"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["crossfit_retention_min"] = "0.1"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC344_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["finite_audit"]["basis_rank_observed"] = 6
        reseal(item)
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["exact_anchor"]["projected_energy"] = "3"
        reseal(item)
        mutations.append(item)

        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC344_STRESS=PASS mutations=9 rejected=9 "
              "raw_guard=1 weighting_guard=1 transfer_guard=1 "
              "semantic_guards=6")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC344_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
