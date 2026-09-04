#!/usr/bin/env python3
"""Adversarial semantic mutations for the TPC-383 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-383-c1-pooled-normalization-audit/results/"
    "tpc383_certificate.json")
SCHEMA = "TPC383_C1_POOLED_NORMALIZATION_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_POOLED_NORMALIZATION_AUDIT"
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
NORMS = ["local_diagonal", "pooled_scalar"]
QS = [512, 2048, 8192]
ORIGINS = [1600001, 1608021, 1616041]


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
    need(selection.get("grid_start") == 1600001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("window_count") == 512 and
         selection.get("block_length") == 128 and
         selection.get("block_count") == 4 and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("spread_cap") == "0.01", "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 512 and
         protocol.get("block_length") == 128 and
         protocol.get("block_count") == 4 and
         protocol.get("band_cutoff") == 1 and
         protocol.get("q_anchors") == QS and
         protocol.get("laws") == LAWS and
         protocol.get("normalizations") == NORMS and
         protocol.get("source_response_used") is False and
         protocol.get("normalization_selection_used") is False, "protocol")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_schema") ==
         "TPC382_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT_V1" and
         parent.get("parent_round2_clue") ==
         "TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN", "parent")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 72, "rows")
    keys = {(row.get("origin"), row.get("Q"), row.get("law"),
             row.get("normalization")) for row in rows}
    need(keys == {(o, q, law, norm) for o in ORIGINS for q in QS
                  for law in LAWS for norm in NORMS}, "row keys")
    for row in rows:
        need(row.get("count") == 512 and row.get("block_length") == 128 and
             row.get("block_count") == 4 and row.get("band_cutoff") == 1 and
             row.get("normalization") in NORMS and row.get("law") in LAWS and
             row.get("Q") in QS and row.get("origin") in ORIGINS and
             math_finite(row.get("band_spectral")), "row header")
    phase = payload.get("phase_summary", {})
    need(isinstance(phase.get("cells"), list) and
         len(phase.get("cells")) == 24 and
         phase.get("row_count") == 72 and
         phase.get("stable_cells_local") == 9 and
         phase.get("stable_cells_pooled") == 9 and
         phase.get("all_plus_high_q_local_stable") is True and
         phase.get("all_plus_high_q_pooled_stable") is True, "phase")
    need(payload.get("finite_audit", {}).get("rows") == 72 and
         payload.get("finite_audit", {}).get("coordinate_disjoint_from_prior") is True,
         "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC383_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC383_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC383_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC383_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") ==
         "TEST_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM", "clue")


def math_finite(value: Any) -> bool:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return False
    return x == x and abs(x) != float("inf") and x >= 0.0


def mutations(document: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    actions: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("claim_status", lambda d: d.__setitem__("claim_status", "PROVED")),
        ("schema", lambda d: d["payload"].__setitem__("schema", "X")),
        ("payload_status", lambda d: d["payload"].__setitem__("status", "PROVED")),
        ("grid_start", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_start", 1600002)),
        ("grid_step", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_step", 400)),
        ("indices", lambda d: d["payload"]["selection_protocol"].__setitem__("origin_indices", [0, 19, 40])),
        ("origin", lambda d: d["payload"]["selection_protocol"].__setitem__("origins", [1600001, 1608020, 1616041])),
        ("response_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("response_used_for_selection", True)),
        ("count", lambda d: d["payload"]["selection_protocol"].__setitem__("window_count", 1024)),
        ("block_length", lambda d: d["payload"]["protocol"].__setitem__("block_length", 64)),
        ("band", lambda d: d["payload"]["protocol"].__setitem__("band_cutoff", 2)),
        ("laws", lambda d: d["payload"]["protocol"].__setitem__("laws", ["all_plus"])),
        ("norms", lambda d: d["payload"]["protocol"].__setitem__("normalizations", ["local_diagonal"])),
        ("parent_schema", lambda d: d["payload"]["parent_lock"].__setitem__("parent_schema", "X")),
        ("row_delete", lambda d: d["payload"]["rows"].pop()),
        ("row_origin", lambda d: d["payload"]["rows"][0].__setitem__("origin", 1600002)),
        ("row_q", lambda d: d["payload"]["rows"][0].__setitem__("Q", 1024)),
        ("row_norm", lambda d: d["payload"]["rows"][0].__setitem__("normalization", "pooled_scalar")),
        ("row_value", lambda d: d["payload"]["rows"][0].__setitem__("band_spectral", "0")),
        ("phase_delete", lambda d: d["payload"]["phase_summary"]["cells"].pop()),
        ("local_census", lambda d: d["payload"]["phase_summary"].__setitem__("stable_cells_local", 8)),
        ("pooled_census", lambda d: d["payload"]["phase_summary"].__setitem__("stable_cells_pooled", 8)),
        ("high_q", lambda d: d["payload"]["phase_summary"].__setitem__("all_plus_high_q_pooled_stable", False)),
        ("arithmetic", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC383_ARITHMETIC_ADVANCE", "YES")),
        ("clue", lambda d: d["payload"].__setitem__("round2_clue", "UNDECLARED")),
    ]
    result = []
    for name, action in actions:
        candidate = copy.deepcopy(document)
        action(candidate)
        result.append((name, candidate))
    return result


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
        print("TPC383_STRESS=PASS mutations=25")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC383_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
