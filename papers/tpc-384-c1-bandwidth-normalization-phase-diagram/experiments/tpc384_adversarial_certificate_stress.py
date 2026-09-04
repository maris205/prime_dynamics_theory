#!/usr/bin/env python3
"""Semantic mutation firewall for the TPC-384 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / "papers/tpc-384-c1-bandwidth-normalization-phase-diagram/results/tpc384_certificate.json"
SCHEMA = "TPC384_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_BANDWIDTH_NORMALIZATION_PHASE_DIAGRAM"
ORIGINS = [1800001, 1808021, 1816041]
QS = [512, 2048, 8192]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
NORMS = ["local_diagonal", "pooled_scalar"]
CUTOFFS = [0, 1, 2, 3]
STABLE = {"c0_local_diagonal": 6, "c0_pooled_scalar": 7,
          "c1_local_diagonal": 8, "c1_pooled_scalar": 7,
          "c2_local_diagonal": 8, "c2_pooled_scalar": 8,
          "c3_local_diagonal": 8, "c3_pooled_scalar": 8}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def math_finite(value: Any) -> bool:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(x) and x >= 0.0


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1800001 and
         selection.get("grid_step") == 401 and selection.get("grid_count") == 41 and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("window_count") == 512 and
         selection.get("block_length") == 128 and selection.get("block_count") == 4 and
         selection.get("band_cutoffs") == CUTOFFS and
         selection.get("q_anchors") == QS and selection.get("laws") == LAWS and
         selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False, "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 512 and protocol.get("block_length") == 128 and
         protocol.get("block_count") == 4 and protocol.get("band_cutoffs") == CUTOFFS and
         protocol.get("q_anchors") == QS and protocol.get("laws") == LAWS and
         protocol.get("normalizations") == NORMS and
         protocol.get("source_response_used") is False and
         protocol.get("bandwidth_selection_used") is False and
         protocol.get("normalization_selection_used") is False, "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 288, "rows")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    expected = {(o, q, law, norm, c) for o in ORIGINS for q in QS
                for law in LAWS for norm in NORMS for c in CUTOFFS}
    need({(r.get("origin"), r.get("Q"), r.get("law"),
            r.get("normalization"), r.get("band_cutoff")) for r in rows} == expected,
         "row keys")
    for row in rows:
        need(row.get("count") == 512 and row.get("block_length") == 128 and
             row.get("block_count") == 4 and row.get("band_cutoff") in CUTOFFS and
             row.get("law") in LAWS and row.get("normalization") in NORMS and
             row.get("Q") in QS and row.get("origin") in ORIGINS and
             math_finite(row.get("band_spectral")), "row header")
    phase = payload.get("phase_summary", {})
    need(phase.get("cell_count") == 96 and phase.get("row_count") == 288 and
         phase.get("stable_cells_by_cutoff_normalization") == STABLE and
         isinstance(phase.get("cells"), list) and len(phase["cells"]) == 96,
         "phase")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 288 and audit.get("cell_count") == 96 and
         audit.get("bandwidth_count") == 4 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC384_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC384_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC384_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC384_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_BANDWIDTH_ORIGIN_HOLDOUT", "clue")


def mutations(document: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    actions: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("claim_status", lambda d: d.__setitem__("claim_status", "PROVED")),
        ("schema", lambda d: d["payload"].__setitem__("schema", "X")),
        ("payload_status", lambda d: d["payload"].__setitem__("status", "PROVED")),
        ("grid_start", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_start", 1800002)),
        ("grid_step", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_step", 400)),
        ("indices", lambda d: d["payload"]["selection_protocol"].__setitem__("origin_indices", [0, 19, 40])),
        ("origins", lambda d: d["payload"]["selection_protocol"].__setitem__("origins", [1800001, 1808020, 1816041])),
        ("response_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("response_used_for_selection", True)),
        ("metric_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("metric_used_for_selection", True)),
        ("bandwidths", lambda d: d["payload"]["selection_protocol"].__setitem__("band_cutoffs", [0, 1, 2])),
        ("count", lambda d: d["payload"]["selection_protocol"].__setitem__("window_count", 1024)),
        ("block_length", lambda d: d["payload"]["protocol"].__setitem__("block_length", 64)),
        ("q_anchors", lambda d: d["payload"]["selection_protocol"].__setitem__("q_anchors", [512, 1024, 8192])),
        ("laws", lambda d: d["payload"]["selection_protocol"].__setitem__("laws", ["all_plus"])),
        ("normalizations", lambda d: d["payload"]["selection_protocol"].__setitem__("normalizations", ["local_diagonal"])),
        ("row_delete", lambda d: d["payload"]["rows"].pop()),
        ("row_origin", lambda d: d["payload"]["rows"][0].__setitem__("origin", 1800002)),
        ("row_cutoff", lambda d: d["payload"]["rows"][0].__setitem__("band_cutoff", 4)),
        ("row_value", lambda d: d["payload"]["rows"][0].__setitem__("band_spectral", "0")),
        ("row_digest", lambda d: d["payload"].__setitem__("row_digest", "0")),
        ("phase_delete", lambda d: d["payload"]["phase_summary"]["cells"].pop()),
        ("stable_census", lambda d: d["payload"]["phase_summary"]["stable_cells_by_cutoff_normalization"].__setitem__("c0_local_diagonal", 7)),
        ("failure_census", lambda d: d["payload"]["phase_summary"].__setitem__("failure_counts_by_cutoff_normalization", {})),
        ("arithmetic", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC384_ARITHMETIC_ADVANCE", "YES")),
        ("clue", lambda d: d["payload"].__setitem__("round2_clue", "UNDECLARED")),
    ]
    return [(name, (lambda action: (lambda d: action(d)))(action))
            for name, action in actions]


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        rejected = 0
        for _, action in mutations(document):
            candidate = copy.deepcopy(document)
            action(candidate)
            try:
                validate(candidate)
            except (Failure, TypeError, ValueError, KeyError):
                rejected += 1
        need(rejected == 25, "mutation coverage")
        print("TPC384_STRESS=PASS mutations=25")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC384_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
