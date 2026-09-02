#!/usr/bin/env python3
"""Mutation stress for the TPC-345 geometry certificate and claim firewall."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc345_certificate.json"
SCHEMA = "TPC345_PRINCIPAL_ANGLE_GRASSMANN_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PRINCIPAL_ANGLE_GRASSMANN_AUDIT"
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
        "panels": 2, "rows": 6, "controls": 9, "categories": 4,
        "raw_records": 216, "nonempty_raw_records": 171,
        "weightings": 2, "principal_angle_pairs": 2,
        "loo_angle_pairs": 18, "basis_invariance_checks": 2,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }, "finite audit")
    protocol = payload.get("protocol", {})
    need(protocol.get("scale") == 1024 and
         protocol.get("operator") == {
             "law": "all_plus", "Q": 54,
             "kernel_exponent": 1, "height": 66} and
         protocol.get("cross_panel_transfer_guard") ==
         "both target directions must have residual retention < 0.30",
         "protocol")
    rows = payload.get("rows", [])
    need(len(rows) == 6 and [row.get("origin") for row in rows] == ORIGINS,
         "row origins")
    for row in rows:
        need(row.get("source_interval") == [
            row["origin"], row["origin"] + 511] and
             row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36,
             "row geometry")
    weightings = payload.get("weighting_results", [])
    need([item.get("label") for item in weightings] == ["raw", "equal_row"],
         "weightings")
    for item in weightings:
        geometry = item.get("principal_geometry", {})
        cosines = geometry.get("principal_cosines", [])
        angles = geometry.get("principal_angles_degrees", [])
        need(len(cosines) == 2 and len(angles) == 2 and
             geometry.get("left_rank") == 3 and
             geometry.get("right_rank") == 2 and
             item.get("basis_invariance", {}).get("span_invariant") is True,
             "principal geometry")
        need(float(item.get("target_panel_1_on_panel_0", {}).get(
            "residual_retention", 0.0)) >= 0.30,
             "mutual transfer obstruction")
        need(len(item.get("leave_one_control_out", [])) == 9,
             "loo geometry")
        for entry in item["leave_one_control_out"]:
            geo = entry.get("geometry", {})
            need(geo.get("left_rank") == 3 and geo.get("right_rank") == 2 and
                 len(geo.get("principal_cosines", [])) == 2,
                 "loo rank")
    summary = payload.get("summary", {})
    need(summary.get("raw_principal_cosines") ==
         weightings[0].get("principal_geometry", {}).get(
             "principal_cosines") and
         summary.get("equal_row_principal_cosines") ==
         weightings[1].get("principal_geometry", {}).get(
             "principal_cosines"), "summary geometry consistency")
    need(float(summary.get("raw_principal_cosines", [0])[0]) > 0.99 and
         float(summary.get("raw_principal_cosines", [1, 1])[1]) < 0.20 and
         float(summary.get("equal_row_principal_cosines", [1, 1])[1]) < 0.20 and
         float(summary.get("dominant_angle_shift_degrees", 0)) > 10.0 and
         summary.get("basis_invariance") == "NUMERICALLY_CERTIFIED_FINITE" and
         summary.get("weighting_stability") == "REFUTED_SCOPED" and
         summary.get("cross_panel_transfer_relevance") == "REFUTED_SCOPED",
         "summary guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC345_PRINCIPAL_ANGLE_IDENTITY") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC345_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC345_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC345_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC345_TWIN_PRIME_RESULT") == "NONE",
         "firewall")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("identity_exact") is True and
         anchor.get("squared_principal_cosine") == "1/2",
         "exact anchor")


def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes())
        need(RESULT.read_bytes() == canonical(original), "canonicality")
        validate(original)
        mutations: list[dict[str, Any]] = []

        item = copy.deepcopy(original)
        item["payload"]["rows"] = item["payload"]["rows"][:-1]
        mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["weighting_results"][0]["principal_geometry"][
            "principal_cosines"][0] = "0.5"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["dominant_angle_shift_degrees"] = "1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["weighting_results"][1]["principal_geometry"][
            "principal_cosines"][1] = "0.9"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["target_transfer_corruption"] = True
        item["payload"]["weighting_results"][0][
            "target_panel_1_on_panel_0"]["residual_retention"] = "0.1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["weighting_results"][0]["basis_invariance"][
            "span_invariant"] = False
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["finite_audit"]["loo_angle_pairs"] = 17
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC345_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["exact_anchor"]["squared_principal_cosine"] = "1/3"
        reseal(item); mutations.append(item)

        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC345_STRESS=PASS mutations=9 rejected=9 "
              "angle_guard=1 transfer_guard=1 invariance_guard=1 "
              "semantic_guards=6")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC345_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
