#!/usr/bin/env python3
"""Adversarial mutation stress for the TPC-361 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-361-independent-high-origin-tightness-replication/results/"
    "tpc361_certificate.json")
SCHEMA = "TPC361_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_HIGH_ORIGIN_TIGHTNESS_REPLICATION"


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    if document.get("certificate_version") != 1 or document.get("claim_status") != STATUS:
        raise Rejected("header")
    payload = document.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise Rejected("schema")
    if document.get("payload_sha256") != hashlib.sha256(canonical(payload)).hexdigest():
        raise Rejected("payload hash")
    protocol = payload.get("protocol", {})
    if (protocol.get("candidate_origins") !=
            [310001 + 233 * j for j in range(51)] or
            protocol.get("pilot_count") != 256 or
            protocol.get("minimum_separation") != 1536 or
            protocol.get("origins") != [313030, 311166, 321651] or
            protocol.get("counts") != [256, 512, 1024, 2048] or
            protocol.get("laws") != ["all_plus", "alternating_index",
                                       "mod4_character", "half_split"] or
            protocol.get("source_response_used") is not False or
            protocol.get("sign_response_used") is not False):
        raise Rejected("protocol")
    selection = payload.get("selection", {})
    if selection.get("selected_origins") != [313030, 311166, 321651]:
        raise Rejected("selection")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 288:
        raise Rejected("rows")
    keys = {(r.get("origin"), r.get("count"), r.get("Q"),
             r.get("kernel_exponent"), r.get("law")) for r in rows}
    if len(keys) != 288:
        raise Rejected("row keys")
    audit = payload.get("finite_audit", {})
    try:
        if (audit.get("rows") != 288 or audit.get("settings") != 72 or
                audit.get("laws") != 4 or audit.get("spectral_rows") != 180 or
                float(audit["normalized_schur_max"]) >= 0.83 or
                float(audit["normalized_spectral_max"]) >= 0.64 or
                float(audit["max_spectral_over_schur"]) >= 0.78 or
                float(audit["max_spectral_over_frobenius"]) >= 0.63 or
                audit.get("finite_schur_violations") != 0 or
                audit.get("finite_frobenius_violations") != 0 or
                audit.get("arithmetic_advance") != "NO" or
                audit.get("fixed_power_credit") != 0):
            raise Rejected("audit")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("audit values") from error
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC361_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC361_HIGH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC361_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC361_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC361_TIGHTNESS_REPLICATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC361_LAW_UNIFORM_SHORT_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC361_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC361_SOURCE_UNIFORM_L2": "OPEN",
        "TPC361_ARITHMETIC_ADVANCE": "NO",
        "TPC361_FIXED_POWER_CREDIT": 0,
        "TPC361_FULL_GATE_B": "OPEN",
        "TPC361_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        if firewall.get(key) != value:
            raise Rejected("firewall " + key)


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "protocol", "candidate_origins"), []),
            (("payload", "protocol", "origins"), [313030]),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "sign_response_used"), True),
            (("payload", "selection", "selected_origins"), [313030]),
            (("payload", "rows"), []),
            (("payload", "finite_audit", "rows"), 287),
            (("payload", "finite_audit", "spectral_rows"), 179),
            (("payload", "finite_audit", "normalized_schur_max"), "0.9"),
            (("payload", "finite_audit", "normalized_spectral_max"), "0.9"),
            (("payload", "finite_audit", "arithmetic_advance"), "YES"),
            (("payload", "claim_firewall", "TPC361_GROWING_OPERATOR_BOUND"), "PROVED"),
            (("payload", "claim_firewall", "TPC361_FIXED_POWER_CREDIT"), 1),
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
        if (rejected != len(mutations) or
                hashlib.sha256(canonical(document)).hexdigest() != baseline):
            raise Rejected("mutation census")
        print("TPC361_STRESS=PASS exact_baseline=1 mutations=15")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC361_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
