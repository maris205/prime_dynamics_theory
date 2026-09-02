#!/usr/bin/env python3
"""Hostile mutation checks for the TPC-349 signed-incidence certificate."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc349_certificate.json"
STATUS = (
    "PROVED_EXACT_FINITE_PRIME_BALANCED_INCIDENCE_LOWER_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_AUDIT")
SCHEMA = "TPC349_PRIME_BALANCED_SIGNED_DEFECT_WITNESS_V1"


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
    need(document.get("payload_sha256") == __import__("hashlib").sha256(
        canonical(payload)).hexdigest(), "payload digest")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [40097, 48097] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [24, 36, 54, 80] and
         protocol.get("kernel_exponents") == [1, 2], "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 192 and
         audit.get("positive_signed_witness_rows") == 192 and
         audit.get("balanced_sum_records") == 192 and
         audit.get("incidence_gram_records") == 192 and
         audit.get("coordinate_beaten_rows") == 136 and
         audit.get("half_defect_rows") == 175 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    rows = payload.get("rows", [])
    need(len(rows) == 192, "rows")
    need(all(row.get("balanced_coefficient_sum") == 0 and
             row.get("coordinate_lower_bound_holds") is True
             for row in rows), "row balance")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("incidence_vector") ==
         [0, 0, 0, 0, 1, 0, -1, 0, 0, 1, 0, 0, 0, -1] and
         anchor.get("incidence_vector_squared_norm") == "4" and
         anchor.get("identity_exact") is True, "anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC349_UNIVERSAL_BALANCED_GAIN") == "REFUTED_SCOPED" and
         firewall.get("TPC349_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC349_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC349_TWIN_PRIME_RESULT") == "NONE", "firewall")


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
        must_reject("wrong first balanced coefficient", document,
                    lambda d: d["payload"]["rows"][0][
                        "balanced_coefficients"].__setitem__(0, -1))
        mutations += 1
        must_reject("owner-only incidence anchor", document,
                    lambda d: d["payload"]["exact_anchor"][
                        "incidence_vector"].__setitem__(6, 0))
        mutations += 1
        must_reject("changed census", document,
                    lambda d: d["payload"]["finite_audit"].__setitem__(
                        "coordinate_beaten_rows", 137))
        mutations += 1
        must_reject("false universal gain", document,
                    lambda d: d["payload"]["claim_firewall"].__setitem__(
                        "TPC349_UNIVERSAL_BALANCED_GAIN", "PASS"))
        mutations += 1
        must_reject("changed response range", document,
                    lambda d: d["payload"]["summary"].__setitem__(
                        "signed_to_defect_ratio_min", "0.5"))
        mutations += 1
        must_reject("changed payload parent", document,
                    lambda d: d["payload"]["parent_lock"].__setitem__(
                        "TPC348_certificate_sha256", "0" * 64))
        mutations += 1
        print("TPC349_STRESS=PASS exact_anchor=1 mutations=" + str(mutations))
        return 0
    except (StressFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC349_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
