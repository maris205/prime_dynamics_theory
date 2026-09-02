#!/usr/bin/env python3
"""Fail-closed mutation stress for the TPC-357 operator certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-357-operator-norm-scale-ladder/results/"
    "tpc357_certificate.json")
SCHEMA = "TPC357_OPERATOR_NORM_SCALE_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER"
PARENT_CERT_HASH = (
    "76afe58c8cf13c0cf122c9e167e031fa831335d0ff1cf2597efed9f130ca0ad6")


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    if (document.get("certificate_version") != 1 or
            document.get("claim_status") != STATUS):
        raise Rejected("header")
    payload = document.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise Rejected("schema")
    if document.get("payload_sha256") != hashlib.sha256(
            canonical(payload)).hexdigest():
        raise Rejected("payload hash")
    lock = payload.get("parent_lock", {})
    if lock.get("TPC356_certificate_sha256") != PARENT_CERT_HASH:
        raise Rejected("parent certificate lock")
    protocol = payload.get("protocol", {})
    if (protocol.get("origins") != [38423, 42010, 45597] or
            protocol.get("counts") != [256, 512, 1024, 2048] or
            protocol.get("q_anchors") != [24, 54, 80] or
            protocol.get("kernel_exponents") != [1, 2] or
            protocol.get("spectral_laws") != ["all_plus"] or
            protocol.get("source_response_used") is not False):
        raise Rejected("protocol")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 288:
        raise Rejected("rows")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("law")) for row in rows}
    if len(keys) != 288:
        raise Rejected("row keys")
    if payload.get("row_digest") != hashlib.sha256(
            canonical(rows)).hexdigest():
        raise Rejected("row digest")
    audit = payload.get("finite_audit", {})
    if (audit.get("rows") != 288 or
            audit.get("finite_schur_violations") != 0 or
            audit.get("finite_frobenius_violations") != 0 or
            audit.get("fixed_power_credit") != 0 or
            audit.get("arithmetic_advance") != "NO"):
        raise Rejected("audit census")
    try:
        if not (float(audit["normalized_schur_max"]) < 0.83 and
                float(audit["normalized_all_plus_spectral_max"]) < 0.64 and
                float(audit["raw_all_plus_spectral_max"]) > 1500.0):
            raise Rejected("audit thresholds")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("audit values") from error
    transitions = payload.get("scale_transition_audit", {}).get("census", {})
    spectral = transitions.get("normalized_spectral", {})
    if (spectral.get("increase", 0) <= 0 or
            spectral.get("decrease", 0) <= 0):
        raise Rejected("scale obstruction")
    firewall = payload.get("claim_firewall", {})
    for key, value in (
            ("TPC357_FINITE_SCHUR_ENVELOPE", "PROVED_EXACT_FINITE"),
            ("TPC357_FINITE_FROBENIUS_ENVELOPE", "PROVED_EXACT_FINITE"),
            ("TPC357_OPERATOR_REPLAY", "NUMERICALLY_CERTIFIED_FINITE_288_ROWS"),
            ("TPC357_NORMALIZED_SCHUR_CAP", "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC357_ALL_PLUS_SPECTRAL_CAP", "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC357_SCALE_MONOTONE_DECAY", "REFUTED_SCOPED_ON_DECLARED_LADDER"),
            ("TPC357_GROWING_OPERATOR_BOUND", "OPEN"),
            ("TPC357_SOURCE_UNIFORM_L2", "OPEN"),
            ("TPC357_ARITHMETIC_ADVANCE", "NO"),
            ("TPC357_FULL_GATE_B", "OPEN"),
            ("TPC357_TWIN_PRIME_RESULT", "NONE")):
        if firewall.get(key) != value:
            raise Rejected("firewall " + key)
    anchor = payload.get("exact_anchor", {})
    if (anchor.get("matrix_symmetric") is not True or
            anchor.get("geometry_positive") is not True):
        raise Rejected("exact anchor")


def main() -> int:
    if any(arg != "--check" for arg in sys.argv[1:]) or len(sys.argv) != 2:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "rows"), []),
            (("payload", "parent_lock", "TPC356_certificate_sha256"),
             "0" * 64),
            (("payload", "finite_audit", "rows"), 287),
            (("payload", "finite_audit", "normalized_schur_max"), "0.91"),
            (("payload", "finite_audit", "raw_all_plus_spectral_max"), "12"),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "scale_transition_audit", "census",
              "normalized_spectral", "increase"), 0),
            (("payload", "claim_firewall", "TPC357_GROWING_OPERATOR_BOUND"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC357_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "exact_anchor", "matrix_symmetric"), False),
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
        print("TPC357_STRESS=PASS exact_baseline=1 mutations=12")
        return 0
    except (Rejected, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC357_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
