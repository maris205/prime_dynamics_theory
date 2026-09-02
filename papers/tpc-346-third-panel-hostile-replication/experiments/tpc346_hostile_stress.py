#!/usr/bin/env python3
"""Mutation stress for the TPC-346 hostile-replication certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc346_certificate.json"
SCHEMA = "TPC346_THIRD_PANEL_HOSTILE_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_THIRD_PANEL_HOSTILE_REPLICATION"
ORIGINS = [48097, 48609, 49217, 40097, 40609, 41121, 44097, 44609, 45217]


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
        "panels": 3, "rows": 9, "origins": 9, "controls": 9,
        "categories": 4, "raw_records": 324,
        "nonempty_raw_records": 261, "weightings": 2,
        "pairwise_geometry_comparisons": 6,
        "directed_panel_predictions_per_weighting": 6,
        "leave_one_panel_out_per_weighting": 3,
        "fresh_control_loo_per_weighting": 9,
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }, "finite audit")
    protocol = payload.get("protocol", {})
    need(protocol.get("scale") == 1024 and
         protocol.get("operator") == {
             "law": "all_plus", "Q": 54,
             "kernel_exponent": 1, "height": 66} and
         protocol.get("fresh_panel") == "TPC346" and
         protocol.get("model_guard") == "residual retention < 0.30" and
         protocol.get("prediction_guard") ==
         "prediction residual retention < 0.30", "protocol")
    panels = protocol.get("panels", [])
    need([item.get("name") for item in panels] ==
         ["TPC341", "TPC342", "TPC346"] and
         [item.get("kind") for item in panels] ==
         ["parent", "parent", "fresh"] and
         [item.get("origins") for item in panels] ==
         [ORIGINS[:3], ORIGINS[3:6], ORIGINS[6:]], "panel protocol")
    rows = payload.get("rows", [])
    need(len(rows) == 9 and
         [item.get("origin") for item in rows] == ORIGINS, "row origins")
    for row in rows:
        need(row.get("source_interval") ==
             [row["origin"], row["origin"] + 511] and
             row.get("cutoff_safe") is True and
             len(row.get("raw_records", [])) == 36, "row geometry")
    weightings = payload.get("weighting_results", [])
    need([item.get("label") for item in weightings] == ["raw", "equal_row"],
         "weightings")
    for item in weightings:
        need(len(item.get("panel_geometry", [])) == 3 and
             len(item.get("pairwise_geometry", [])) == 3 and
             len(item.get("directed_predictions", [])) == 6 and
             len(item.get("leave_one_panel_out", [])) == 3 and
             len(item.get("fresh_control_loo", [])) == 9,
             "nested census")
        for panel in item["panel_geometry"]:
            need(panel.get("target_projection", {}).get("identity_holds") is True,
                 "panel identity")
        need(item.get("shared_three_panel", {}).get("identity_holds") is True and
             item.get("panel_adaptive_three_panel", {}).get(
                 "identity_holds") is True, "model identities")
    summary = payload.get("summary", {})
    need(float(summary.get("fresh_panel_raw_retention", 0)) >= 0.30 and
         float(summary.get("fresh_panel_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("shared_three_panel_raw_retention", 0)) >= 0.30 and
         float(summary.get("shared_three_panel_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("panel_adaptive_three_panel_raw_retention", 1)) < 0.30 and
         float(summary.get("panel_adaptive_three_panel_equal_row_retention", 0)) >= 0.30 and
         float(summary.get("directed_prediction_min", 0)) > 0.30 and
         float(summary.get("leave_one_panel_out_min", 0)) > 0.30 and
         float(summary.get("fresh_control_loo_min", 0)) > 0.30 and
         summary.get("panel_adaptive_raw_guard") == "PASS_FINITE_SCOPED" and
         summary.get("panel_adaptive_equal_row_guard") == "REFUTED_SCOPED" and
         summary.get("fresh_panel_own_fit") == "REFUTED_SCOPED" and
         summary.get("third_panel_transfer") == "REFUTED_SCOPED" and
         summary.get("route_decision") ==
         "FREEZE_PANEL_ADAPTIVE_ROUTE_FINITE_SCOPED", "summary guards")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC346_NESTED_MODEL_IDENTITY") ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall.get("TPC346_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC346_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC346_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC346_TWIN_PRIME_RESULT") == "NONE", "firewall")
    anchor = payload.get("exact_anchor", {})
    need(anchor.get("identity_exact") is True and
         anchor.get("shared_projected_energy") == "2" and
         anchor.get("additional_contrast_energy") == "1/2", "anchor")


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
        item["payload"]["protocol"]["panels"][2]["origins"][0] = 44098
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["panel_adaptive_three_panel_raw_retention"] = "0.4"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"][
            "panel_adaptive_three_panel_equal_row_retention"] = "0.1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["fresh_panel_raw_retention"] = "0.1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["directed_prediction_min"] = "0.1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["fresh_control_loo_min"] = "0.1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["summary"]["shared_three_panel_raw_retention"] = "0.1"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["claim_firewall"]["TPC346_ARITHMETIC_ADVANCE"] = "YES"
        reseal(item); mutations.append(item)

        item = copy.deepcopy(original)
        item["payload"]["exact_anchor"]["shared_projected_energy"] = "3"
        reseal(item); mutations.append(item)

        rejected = 0
        for mutation in mutations:
            try:
                validate(mutation)
            except Failure:
                rejected += 1
        need(rejected == len(mutations), "mutation rejection")
        print("TPC346_STRESS=PASS mutations=10 rejected=10 "
              "fresh_fit_guard=1 adaptive_weighting_guard=1 "
              "prediction_guard=1 semantic_guards=7")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC346_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
