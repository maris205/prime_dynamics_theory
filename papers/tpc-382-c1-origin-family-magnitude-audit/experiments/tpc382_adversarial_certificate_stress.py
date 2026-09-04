#!/usr/bin/env python3
"""Adversarial mutation tests for the TPC-382 finite audit certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-382-c1-origin-family-magnitude-audit/results/"
    "tpc382_certificate.json")
SCHEMA = "TPC382_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT"
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
QS = (512, 2048, 8192)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    selection = payload.get("selection_protocol", {})
    need(selection.get("parent_panels_fixed_before_metric_read") is True and
         selection.get("parent_hashes_fixed_before_aggregation") is True and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("same_count_labels") == ["TPC380", "TPC381"] and
         selection.get("scale_control_label") == "TPC379" and
         selection.get("laws") == list(LAWS) and
         selection.get("q_anchors") == list(QS) and
         selection.get("relative_spread_cap") == "0.01" and
         selection.get("scale_contrast_cap") == "0.01" and
         selection.get("high_q") == 8192, "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("same_count") == 2048 and
         protocol.get("same_count_panels") == ["TPC380", "TPC381"] and
         protocol.get("scale_control_count") == 1024 and
         protocol.get("scale_control_panel") == "TPC379" and
         protocol.get("laws") == list(LAWS) and
         protocol.get("q_anchors") == list(QS) and
         protocol.get("cells_per_panel") == 12 and
         protocol.get("same_count_value_count") == 72 and
         protocol.get("scale_control_value_count") == 36, "protocol")
    locks = payload.get("parent_locks")
    need(isinstance(locks, list) and len(locks) == 3 and
         [item.get("label") for item in locks] ==
         ["TPC379", "TPC380", "TPC381"], "parent locks")
    same = payload.get("same_count_cells")
    scale = payload.get("scale_control_cells")
    contrasts = payload.get("scale_contrasts")
    need(isinstance(same, list) and len(same) == 12 and
         isinstance(scale, list) and len(scale) == 12 and
         isinstance(contrasts, list) and len(contrasts) == 12, "cell census")
    expected_keys = {(law, q0) for law in LAWS for q0 in QS}
    need({(item.get("law"), item.get("Q")) for item in same} == expected_keys,
         "same keys")
    need({(item.get("law"), item.get("Q")) for item in scale} == expected_keys,
         "scale keys")
    need({(item.get("law"), item.get("Q")) for item in contrasts} ==
         expected_keys, "contrast keys")
    for item in same + scale:
        values = [float(x) for x in item.get("values", [])]
        need(values and item.get("value_count") == len(values), "values")
        minimum, maximum = min(values), max(values)
        mean = sum(values) / len(values)
        relative = (maximum - minimum) / mean
        need(item.get("within_one_percent") is (relative <= 0.01),
             "spread flag")
        for key, value in (("minimum", minimum), ("maximum", maximum),
                           ("mean", mean),
                           ("absolute_spread", maximum - minimum),
                           ("relative_spread", relative)):
            need(abs(float(item.get(key)) - value) <=
                 5e-12 * max(1.0, abs(value)), "spread statistic")
    summary = payload.get("phase_summary", {})
    need(summary.get("same_count_cells") == 12 and
         summary.get("same_count_values") == 72 and
         summary.get("same_count_cells_within_one_percent") == 8 and
         summary.get("signed_cells_over_one_percent") == 4 and
         summary.get("all_plus_high_q_within_one_percent") is True and
         summary.get("all_plus_high_q_scale_within_one_percent") is False,
         "summary")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC382_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC382_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC382_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC382_TWIN_PRIME_RESULT") == "NONE",
         "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN", "clue")


def mutations(document: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    actions: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("claim_status", lambda d: d.__setitem__("claim_status", "PROVED")),
        ("schema", lambda d: d["payload"].__setitem__("schema", "X")),
        ("payload_status", lambda d: d["payload"].__setitem__("status", "PROVED")),
        ("selection_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("response_used_for_selection", True)),
        ("parent_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("parent_hashes_fixed_before_aggregation", False)),
        ("law_list", lambda d: d["payload"]["selection_protocol"].__setitem__("laws", ["all_plus"])),
        ("spread_cap", lambda d: d["payload"]["selection_protocol"].__setitem__("relative_spread_cap", "0.02")),
        ("high_q", lambda d: d["payload"]["selection_protocol"].__setitem__("high_q", 2048)),
        ("same_count", lambda d: d["payload"]["protocol"].__setitem__("same_count", 1024)),
        ("panel_order", lambda d: d["payload"]["protocol"].__setitem__("same_count_panels", ["TPC381", "TPC380"])),
        ("value_count", lambda d: d["payload"]["protocol"].__setitem__("same_count_value_count", 71)),
        ("parent_label", lambda d: d["payload"]["parent_locks"][0].__setitem__("label", "TPC380")),
        ("parent_hash", lambda d: d["payload"]["parent_locks"][1].__setitem__("certificate_sha256", "0" * 64)),
        ("same_delete", lambda d: d["payload"]["same_count_cells"].pop()),
        ("same_law", lambda d: d["payload"]["same_count_cells"][0].__setitem__("law", "other")),
        ("same_value", lambda d: d["payload"]["same_count_cells"][0]["values"].__setitem__(0, "0")),
        ("same_flag", lambda d: d["payload"]["same_count_cells"][1].__setitem__("within_one_percent", False)),
        ("same_mean", lambda d: d["payload"]["same_count_cells"][2].__setitem__("mean", "0")),
        ("scale_delete", lambda d: d["payload"]["scale_control_cells"].pop()),
        ("scale_value", lambda d: d["payload"]["scale_control_cells"][0]["values"].__setitem__(0, "0")),
        ("contrast_delete", lambda d: d["payload"]["scale_contrasts"].pop()),
        ("contrast_value", lambda d: d["payload"]["scale_contrasts"][0].__setitem__("relative_change", "0")),
        ("stable_census", lambda d: d["payload"]["phase_summary"].__setitem__("same_count_cells_within_one_percent", 7)),
        ("arithmetic", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC382_ARITHMETIC_ADVANCE", "YES")),
        ("clue", lambda d: d["payload"].__setitem__("round2_clue", "UNDECLARED")),
    ]
    output = []
    for name, action in actions:
        candidate = copy.deepcopy(document)
        action(candidate)
        output.append((name, candidate))
    return output


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        rejected = 0
        for _, candidate in mutations(document):
            try:
                validate(candidate)
            except (Failure, TypeError, ValueError, KeyError):
                rejected += 1
        need(rejected == 25, "mutation coverage")
        print("TPC382_STRESS=PASS mutations=25")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC382_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
