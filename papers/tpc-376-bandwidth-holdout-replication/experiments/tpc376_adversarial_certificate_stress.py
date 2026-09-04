#!/usr/bin/env python3
"""Adversarial schema and claim-firewall mutations for TPC-376."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-376-bandwidth-holdout-replication/results/"
    "tpc376_certificate.json")
SCHEMA = "TPC376_BANDWIDTH_HOLDOUT_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_HOLDOUT_REPLICATION"
ORIGINS = [1012006, 1016016, 1022031]
Q_ANCHORS = [512, 2048, 8192]
FIREWALL = {
    "TPC376_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC376_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE_INHERITED",
    "TPC376_HOLDOUT_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_9_ROWS",
    "TPC376_C1_FAILURE_PROFILE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC376_PARENT_Q_PROFILE_REPLICATION":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC376_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC376_ORIGIN_UNIFORMITY": "OPEN",
    "TPC376_WINDOW_UNIFORMITY": "OPEN",
    "TPC376_C1_SCALE_STABILITY": "OPEN",
    "TPC376_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC376_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC376_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC376_SOURCE_UNIFORM_L2": "OPEN",
    "TPC376_ARITHMETIC_ADVANCE": "NO",
    "TPC376_FIXED_POWER_CREDIT": 0,
    "TPC376_FULL_GATE_B": "OPEN",
    "TPC376_TWIN_PRIME_RESULT": "NONE",
}


class Rejected(Exception):
    pass


def reject(condition: bool, message: str) -> None:
    if condition:
        raise Rejected(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def finite(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def validate(document: dict[str, Any]) -> None:
    reject(document.get("certificate_version") != 1 or
           document.get("claim_status") != STATUS, "header")
    payload = document.get("payload")
    reject(not isinstance(payload, dict) or payload.get("schema") != SCHEMA or
           payload.get("status") != STATUS, "schema/status")
    reject(document.get("payload_sha256") != hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    selection = payload.get("selection_protocol")
    reject(selection != {
        "grid_start": 1010001, "grid_step": 401, "grid_count": 41,
        "candidate_rule": "a_j=1010001+401j, 0<=j<41",
        "training_indices": [0, 20, 40],
        "training_origins": [1010001, 1018021, 1026041],
        "holdout_indices": [5, 15, 30],
        "holdout_origins": ORIGINS,
        "holdout_rule": "first three predeclared reserved indices (5,15,30)",
        "response_used_for_selection": False,
        "signed_metric_used_for_selection": False,
    }, "selection")
    protocol = payload.get("protocol")
    reject(protocol != {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoff": 1,
        "band_definition": "sum of layers with block distance <= 1",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        "panel_complete_before_metric_read": True,
    }, "protocol")
    rows = payload.get("rows")
    reject(not isinstance(rows, list) or len(rows) != 9, "row count")
    reject({(r.get("origin"), r.get("Q")) for r in rows} !=
           {(o, q) for o in ORIGINS for q in Q_ANCHORS}, "row keys")
    for row in rows:
        reject(row.get("count") != 2048 or row.get("beta") != 2 or
               row.get("law") != "all_plus" or row.get("height") != 66 or
               row.get("kernel_exponent") != 1 or
               row.get("shell_cardinality", 0) <= 0, "row header")
        for section in ("full", "band", "tail", "mode"):
            values = row.get(section, {})
            reject(not isinstance(values, dict), "row section")
            for name, value in values.items():
                if name not in {"selected_mode", "mode_rule"}:
                    reject(not finite(value), "nonfinite row metric")
        reject(row.get("band_failure") is not True and
               row.get("band_failure") is not False, "failure type")
    phase = payload.get("phase_summary", {})
    reject(phase.get("rows") != 9 or phase.get("band_cutoff") != 1 or
           phase.get("spectral_cap_violations") != 6 or
           phase.get("schur_cap_violations") != 0 or
           phase.get("failure_profile_by_Q") != [0, 3, 3] or
           phase.get("caps") != {
               "spectral": "0.64000000000000001",
               "schur": "0.82999999999999996"}, "phase")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 9 or
           audit.get("origin_count") != 3 or audit.get("q_count") != 3 or
           audit.get("spectral_rows") != 9 or
           audit.get("spectral_cap_violations") != 6 or
           audit.get("schur_cap_violations") != 0 or
           audit.get("failure_profile_by_Q") != [0, 3, 3] or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    reject(payload.get("claim_firewall") != FIREWALL, "firewall")
    reject(payload.get("round2_clue") != "TEST_C1_WINDOW_SCALE_HOLDOUT",
           "clue")


def mutate(document: dict[str, Any], path: tuple[Any, ...], value: Any,
           refresh: bool = True) -> dict[str, Any]:
    item = copy.deepcopy(document)
    target: Any = item
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    if refresh and path[0] == "payload":
        item["payload_sha256"] = hashlib.sha256(
            canonical(item["payload"])).hexdigest()
    return item


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        reject(raw != canonical(document), "certificate canonicality")
        validate(document)
        mutations = [
            (("certificate_version",), 2),
            (("claim_status",), "PROVED"),
            (("payload", "schema"), "MUTATED"),
            (("payload", "selection_protocol", "holdout_indices"), [5, 15]),
            (("payload", "selection_protocol",
              "response_used_for_selection"), True),
            (("payload", "protocol", "band_cutoff"), 2),
            (("payload", "protocol", "window_count"), 4096),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "row_selection_used"), True),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "band_failure"), "true"),
            (("payload", "rows", 0, "full", "spectral"), "nan"),
            (("payload", "phase_summary", "spectral_cap_violations"), 5),
            (("payload", "phase_summary", "failure_profile_by_Q"), [1, 2, 3]),
            (("payload", "finite_audit", "rows"), 8),
            (("payload", "finite_audit", "fixed_power_credit"), 1),
            (("payload", "finite_audit", "arithmetic_advance"), "YES"),
            (("payload", "claim_firewall", "TPC376_C1_SCALE_STABILITY"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC376_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "round2_clue"), "CLAIM_TWIN_PRIMES"),
            (("payload", "status"), "PROVED"),
            (("payload_sha256",), "0" * 64, False),
        ]
        for path, value, *rest in mutations:
            refresh = rest[0] if rest else True
            try:
                validate(mutate(document, path, value, refresh))
            except Rejected:
                continue
            raise Rejected("mutation accepted: " + repr(path))
        print("TPC376_STRESS=PASS mutations=" + str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC376_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
