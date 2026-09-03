#!/usr/bin/env python3
"""Mutation stress test for the TPC-365 finite certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-365-beta2-fresh-holdout/results/tpc365_certificate.json")
SCHEMA = "TPC365_BETA2_FRESH_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BETA2_FRESH_HOLDOUT"
ORIGINS = [413342, 410258, 416940]
COUNTS = [256, 512]
Q_ANCHORS = [80, 128, 256, 512]
EXPONENTS = [1, 2]
BETAS = [0, 2]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def reject(condition: bool, message: str) -> None:
    if condition:
        raise Rejected(message)


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
    reject(selection.get("selected_origins") != ORIGINS or
           selection.get("candidate_count") != 51 or
           selection.get("pilot_count") != 256 or
           selection.get("selection_beta") != 2 or
           selection.get("minimum_separation") != 2048, "selection")
    rows = payload.get("rows")
    reject(not isinstance(rows, list) or len(rows) != 384, "rows")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows}
    reject(len(keys) != 384, "row keys")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap_repair_betas") != [2], "repair beta")
    by_beta = phase.get("by_beta", {})
    for beta, violations in ((0, 30), (2, 0)):
        item = by_beta.get(str(beta), {})
        reject(item.get("rows") != 192 or
               item.get("spectral_cap_violations") != violations,
               "phase " + str(beta))
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 384 or
           audit.get("settings_per_beta") != 48 or
           audit.get("beta_count") != 2 or
           audit.get("spectral_rows") != 384 or
           audit.get("beta2_holdout_rows") != 192 or
           audit.get("beta2_holdout_cap_violations") != 0 or
           audit.get("baseline_beta0_cap_violations") != 30 or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC365_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC365_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC365_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_384_ROWS",
        "TPC365_BETA2_HOLDOUT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC365_BETA2_CAP_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC365_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC365_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC365_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC365_SOURCE_UNIFORM_L2": "OPEN",
        "TPC365_ARITHMETIC_ADVANCE": "NO",
        "TPC365_FIXED_POWER_CREDIT": 0,
        "TPC365_FULL_GATE_B": "OPEN", "TPC365_TWIN_PRIME_RESULT": "NONE",
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
            (("payload", "protocol", "q_anchors"), [80, 128, 256]),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "selection_response_blind"), False),
            (("payload", "selection", "selected_origins"), ORIGINS[:2]),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "beta"), 99),
            (("payload", "finite_audit", "rows"), 383),
            (("payload", "finite_audit", "beta2_holdout_rows"), 191),
            (("payload", "finite_audit", "beta2_holdout_cap_violations"), 1),
            (("payload", "phase_summary", "cap_repair_betas"), [0]),
            (("payload", "phase_summary", "by_beta", "2",
              "spectral_cap_violations"), 1),
            (("payload", "phase_summary", "by_beta", "0",
              "spectral_cap_violations"), 0),
            (("payload", "claim_firewall", "TPC365_BETA2_ASYMPTOTIC_REPAIR"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC365_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "claim_firewall", "TPC365_FIXED_POWER_CREDIT"), 1),
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
        print("TPC365_STRESS=PASS exact_baseline=1 mutations=19")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC365_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
