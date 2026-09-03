#!/usr/bin/env python3
"""Mutation stress test for the TPC-366 finite certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-366-beta2-higher-q-ladder/results/tpc366_certificate.json")
SCHEMA = "TPC366_BETA2_HIGHER_Q_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BETA2_HIGHER_Q_LADDER"
ORIGINS = [623071, 631360, 629211]
COUNTS = [256, 512]
Q_ANCHORS = [512, 1024, 2048, 4096, 8192]
EXPONENTS = [1, 2]
BETAS = [0, 2]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]


class Rejected(Exception):
    pass


def reject(condition: bool, message: str) -> None:
    if condition:
        raise Rejected(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    reject(document.get("certificate_version") != 1 or
           document.get("claim_status") != STATUS, "header")
    payload = document.get("payload")
    reject(not isinstance(payload, dict) or payload.get("schema") != SCHEMA,
           "schema")
    reject(document.get("payload_sha256") != hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    protocol = payload.get("protocol", {})
    reject(protocol.get("origins") != ORIGINS or
           protocol.get("counts") != COUNTS or
           protocol.get("q_anchors") != Q_ANCHORS or
           protocol.get("kernel_exponents") != EXPONENTS or
           protocol.get("laws") != LAWS or
           protocol.get("betas") != BETAS or
           protocol.get("selection_beta") != 2 or
           protocol.get("pilot_count") != 256 or
           protocol.get("minimum_separation") != 2048 or
           protocol.get("spectra_for_all_laws") is not True or
           protocol.get("source_response_used") is not False or
           protocol.get("selection_response_blind") is not True, "protocol")
    selection = payload.get("selection", {})
    reject(selection.get("candidate_count") != 41 or
           selection.get("selected_origins") != ORIGINS or
           selection.get("selection_beta") != 2 or
           selection.get("pilot_count") != 256 or
           selection.get("minimum_separation") != 2048, "selection")
    rows = payload.get("rows")
    reject(not isinstance(rows, list) or len(rows) != 480, "rows")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows}
    reject(len(keys) != 480, "row keys")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap_repair_betas") != [2], "repair beta")
    by_beta = phase.get("by_beta", {})
    for beta, violations, schur_violations in ((0, 60, 60), (2, 0, 0)):
        item = by_beta.get(str(beta), {})
        reject(item.get("rows") != 240 or
               item.get("spectral_cap_violations") != violations or
               item.get("schur_cap_violations") != schur_violations,
               "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 480 or
           audit.get("settings_per_beta") != 240 or
           audit.get("beta_count") != 2 or
           audit.get("spectral_rows") != 480 or
           audit.get("beta2_rows") != 240 or
           audit.get("beta2_cap_violations") != 0 or
           audit.get("beta2_schur_cap_violations") != 0 or
           audit.get("baseline_beta0_cap_violations") != 60 or
           audit.get("baseline_beta0_schur_cap_violations") != 60 or
           audit.get("q_min") != 512 or audit.get("q_max") != 8192 or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC366_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC366_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC366_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_480_ROWS",
        "TPC366_HIGHER_Q_LADDER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC366_BETA2_HIGHER_Q_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC366_BETA2_SCALE_UNIFORMITY": "OPEN",
        "TPC366_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC366_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC366_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC366_SOURCE_UNIFORM_L2": "OPEN",
        "TPC366_ARITHMETIC_ADVANCE": "NO",
        "TPC366_FIXED_POWER_CREDIT": 0,
        "TPC366_FULL_GATE_B": "OPEN", "TPC366_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        reject(firewall.get(key) != value, "firewall " + key)


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        reject(raw != canonical(document), "certificate canonicality")
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "protocol", "q_anchors"), [512, 1024, 2048]),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "selection_response_blind"), False),
            (("payload", "protocol", "minimum_separation"), 1024),
            (("payload", "selection", "selected_origins"), ORIGINS[:2]),
            (("payload", "selection", "candidate_count"), 40),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 256),
            (("payload", "rows", 0, "beta"), 99),
            (("payload", "finite_audit", "rows"), 479),
            (("payload", "finite_audit", "q_max"), 4096),
            (("payload", "finite_audit", "beta2_rows"), 239),
            (("payload", "finite_audit", "beta2_cap_violations"), 1),
            (("payload", "phase_summary", "cap_repair_betas"), [0]),
            (("payload", "phase_summary", "by_beta", "2",
              "spectral_cap_violations"), 1),
            (("payload", "phase_summary", "by_beta", "0",
              "schur_cap_violations"), 0),
            (("payload", "claim_firewall", "TPC366_BETA2_ASYMPTOTIC_REPAIR"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC366_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "claim_firewall", "TPC366_FIXED_POWER_CREDIT"), 1),
            (("payload", "row_digest"), "0" * 64),
            (("payload_sha256",), "0" * 64),
        ]
        rejected = 0
        for path, value in mutations:
            item = copy.deepcopy(document)
            target: Any = item
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            try:
                validate(item)
            except Rejected:
                rejected += 1
        reject(rejected != len(mutations), "mutation census")
        reject(hashlib.sha256(canonical(document)).hexdigest() != baseline,
               "baseline changed")
        print("TPC366_STRESS=PASS exact_baseline=1 mutations=23")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC366_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
