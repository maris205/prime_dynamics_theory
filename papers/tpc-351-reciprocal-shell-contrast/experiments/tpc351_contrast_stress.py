#!/usr/bin/env python3
"""Hostile mutation checks for the TPC-351 reciprocal contrast certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc351_certificate.json"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT")
SCHEMA = "TPC351_RECIPROCAL_SHELL_CONTRAST_V1"


class StressFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise StressFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [60097, 72097, 84097] and
         protocol.get("source_counts") == [256, 512, 1024, 2048] and
         protocol.get("q_anchors") == [36, 80, 128, 256] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index"],
         "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 192 and audit.get("series") == 48 and
         audit.get("positive_reciprocal_witness_rows") == 192 and
         audit.get("zero_sum_records") == 192 and
         audit.get("incidence_gram_records") == 192 and
         audit.get("improved_parent_rows") == 180 and
         audit.get("parent_comparison_records") == 192 and
         audit.get("coordinate_beaten_rows") == 86 and
         audit.get("half_defect_rows") == 111 and
         audit.get("min_reciprocal_support") == 24 and
         audit.get("max_reciprocal_support") == 339 and
         audit.get("min_reciprocal_to_defect_ratio") == "0.0917557319271" and
         audit.get("max_reciprocal_to_defect_ratio") == "0.901734353382" and
         audit.get("nondecreasing_series") == 25 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    rows = payload.get("rows", [])
    need(len(rows) == 192 and all(
        row.get("reciprocal_coefficient_sum") == "0/1" and
        row.get("reciprocal_active_prime_count") in (9, 15, 23, 43) and
        row.get("reciprocal_incidence_support", 0) > 0 and
        row.get("coordinate_lower_bound_holds") is True
        for row in rows), "rows")
    series = payload.get("growth_series", [])
    need(len(series) == 48 and
         sum(item.get("nondecreasing") is True for item in series) == 25 and
         all(item.get("counts") == [256, 512, 1024, 2048]
             for item in series), "growth series")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("interval") == [97, 110] and
         anchor.get("coefficients") == ["1/35", "-1/35"] and
         anchor.get("incidence_vector") ==
         ["0/1", "-1/35", "0/1", "1/35", "0/1", "0/1", "0/1",
          "0/1", "0/1", "0/1", "0/1", "0/1", "0/1", "1/35"] and
         anchor.get("incidence_vector_squared_norm") == "3/1225" and
         anchor.get("identity_exact") is True, "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC351_UNIFORM_QUARTER_FLOOR") ==
         "REFUTED_SCOPED" and
         firewall.get("TPC351_PARENT_IMPROVEMENT_CENSUS") ==
         "NUMERICALLY_CERTIFIED_FINITE_180_OF_192" and
         firewall.get("TPC351_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC351_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC351_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC351_TWIN_PRIME_RESULT") == "NONE", "firewall")


def must_reject(label: str, document: dict[str, Any],
                mutate: Callable[[dict[str, Any]], None]) -> None:
    candidate = copy.deepcopy(document)
    mutate(candidate)
    try:
        validate(candidate)
    except StressFailure:
        return
    raise StressFailure("mutation accepted: " + label)


def main() -> int:
    try:
        document = json.loads(RESULT.read_text(encoding="utf-8"))
        validate(document)
        mutations = 0
        must_reject("origin replacement", document,
                    lambda d: d["payload"]["protocol"]["origins"].__setitem__(
                        0, 40097))
        mutations += 1
        must_reject("drop high shell", document,
                    lambda d: d["payload"]["protocol"]["q_anchors"].pop())
        mutations += 1
        must_reject("wrong positive census", document,
                    lambda d: d["payload"]["finite_audit"].__setitem__(
                        "positive_reciprocal_witness_rows", 191))
        mutations += 1
        must_reject("false quarter floor", document,
                    lambda d: d["payload"]["claim_firewall"].__setitem__(
                        "TPC351_UNIFORM_QUARTER_FLOOR", "PASS"))
        mutations += 1
        must_reject("monotonicity inflation", document,
                    lambda d: d["payload"]["finite_audit"].__setitem__(
                        "nondecreasing_series", 48))
        mutations += 1
        must_reject("anchor coefficient deletion", document,
                    lambda d: d["payload"]["exact_anchor"][
                        "incidence_vector"].__setitem__(1, 0))
        mutations += 1
        must_reject("parent replacement", document,
                    lambda d: d["payload"]["parent_lock"].__setitem__(
                        "TPC350_certificate_sha256", "0" * 64))
        mutations += 1
        must_reject("false parent improvement", document,
                    lambda d: d["payload"]["finite_audit"].__setitem__(
                        "improved_parent_rows", 192))
        mutations += 1
        print("TPC351_STRESS=PASS exact_anchor=1 mutations=" + str(mutations))
        return 0
    except (StressFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC351_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
