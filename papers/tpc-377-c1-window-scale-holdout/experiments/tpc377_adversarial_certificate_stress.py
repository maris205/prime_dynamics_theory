#!/usr/bin/env python3
"""Adversarial schema and claim-firewall mutations for TPC-377."""

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
    "papers/tpc-377-c1-window-scale-holdout/results/"
    "tpc377_certificate.json")
SCHEMA = "TPC377_C1_WINDOW_SCALE_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_WINDOW_SCALE_HOLDOUT"
ORIGINS = [1012006, 1016016, 1022031]
COUNTS = [1024, 1536, 2048]
Q_ANCHORS = [512, 2048, 8192]
FIREWALL = {
    "TPC377_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC377_NESTED_PREFIX_PROTOCOL": "PROVED_EXACT_FINITE",
    "TPC377_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE_INHERITED",
    "TPC377_SCALE_LADDER_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_27_ROWS",
    "TPC377_C1_PROFILE_STABILITY":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC377_PARENT_Q_PROFILE_PERSISTENCE":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC377_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC377_ORIGIN_UNIFORMITY": "OPEN",
    "TPC377_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC377_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC377_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC377_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC377_SOURCE_UNIFORM_L2": "OPEN",
    "TPC377_ARITHMETIC_ADVANCE": "NO",
    "TPC377_FIXED_POWER_CREDIT": 0,
    "TPC377_FULL_GATE_B": "OPEN",
    "TPC377_TWIN_PRIME_RESULT": "NONE",
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
        "origins": ORIGINS,
        "origin_rule":
            "TPC376 response-blind holdout origins, inherited unchanged",
        "counts": COUNTS,
        "count_rule":
            "predeclared nested prefixes of lengths 1024,1536,2048",
        "block_length": 256, "block_counts": [4, 6, 8],
        "q_anchors": Q_ANCHORS,
        "response_used_for_selection": False,
        "signed_metric_used_for_selection": False,
        "panel_complete_before_metric_read": True,
    }, "selection")
    protocol = payload.get("protocol")
    reject(protocol != {
        "origins": ORIGINS, "window_counts": COUNTS,
        "block_length": 256, "block_counts": [4, 6, 8],
        "partition": "nested prefixes with contiguous 256-point blocks",
        "band_cutoff": 1,
        "band_definition": "sum of layers with block distance <= 1",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "count_selection_used": False,
        "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
    }, "protocol")
    rows = payload.get("rows")
    reject(not isinstance(rows, list) or len(rows) != 27, "row count")
    reject({(r.get("origin"), r.get("count"), r.get("Q")) for r in rows} !=
           {(o, n, q) for o in ORIGINS for n in COUNTS
            for q in Q_ANCHORS}, "row keys")
    for row in rows:
        reject(row.get("count") not in COUNTS or
               row.get("origin") not in ORIGINS or
               row.get("Q") not in Q_ANCHORS or
               row.get("block_length") != 256 or
               row.get("block_count") != row.get("count") // 256 or
               row.get("beta") != 2 or row.get("law") != "all_plus" or
               row.get("height") != 66 or row.get("kernel_exponent") != 1,
               "row header")
        for section in ("full", "band", "tail", "mode"):
            values = row.get(section, {})
            reject(not isinstance(values, dict), "row section")
            for name, value in values.items():
                if name not in {"selected_mode", "mode_rule"}:
                    reject(not finite(value), "nonfinite row metric")
        reject(row.get("band_failure") not in (True, False) or
               row.get("schur_failure") not in (True, False),
               "failure type")
    phase = payload.get("phase_summary", {})
    reject(phase.get("rows") != 27 or
           phase.get("band_cutoff") != 1 or
           phase.get("spectral_cap_violations") != 18 or
           phase.get("schur_cap_violations") != 0 or
           phase.get("failure_profile_by_count_Q") !=
           [[0, 3, 3], [0, 3, 3], [0, 3, 3]] or
           phase.get("caps") != {
               "spectral": "0.64000000000000001",
               "schur": "0.82999999999999996"}, "phase")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 27 or
           audit.get("origin_count") != 3 or
           audit.get("count_count") != 3 or
           audit.get("q_count") != 3 or
           audit.get("spectral_rows") != 27 or
           audit.get("spectral_cap_violations") != 18 or
           audit.get("schur_cap_violations") != 0 or
           audit.get("failure_profile_by_count_Q") !=
           [[0, 3, 3], [0, 3, 3], [0, 3, 3]] or
           audit.get("scale_profile_invariant") is not True or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    reject(payload.get("claim_firewall") != FIREWALL, "firewall")
    reject(payload.get("round2_clue") !=
           "TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT", "clue")


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
            (("payload", "selection_protocol", "counts"), [1024, 2048]),
            (("payload", "selection_protocol",
              "response_used_for_selection"), True),
            (("payload", "protocol", "band_cutoff"), 2),
            (("payload", "protocol", "window_counts"), [512, 1024, 2048]),
            (("payload", "protocol", "count_selection_used"), True),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "count"), 512),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "band_failure"), "true"),
            (("payload", "rows", 0, "full", "spectral"), "nan"),
            (("payload", "phase_summary", "spectral_cap_violations"), 17),
            (("payload", "phase_summary",
              "failure_profile_by_count_Q"), [[0, 2, 3]] * 3),
            (("payload", "finite_audit", "rows"), 26),
            (("payload", "finite_audit", "scale_profile_invariant"), False),
            (("payload", "finite_audit", "fixed_power_credit"), 1),
            (("payload", "finite_audit", "arithmetic_advance"), "YES"),
            (("payload", "claim_firewall",
              "TPC377_WINDOW_SCALE_UNIFORMITY"), "PROVED"),
            (("payload", "claim_firewall",
              "TPC377_ARITHMETIC_ADVANCE"), "YES"),
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
        print("TPC377_STRESS=PASS mutations=" + str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC377_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
