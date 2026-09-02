#!/usr/bin/env python3
"""Mutation stress for the TPC-360 tightness/law-uniform certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / "papers/tpc-360-schur-tightness-law-uniform-audit/results/tpc360_certificate.json"
SCHEMA = "TPC360_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SCHUR_TIGHTNESS_LAW_UNIFORM_AUDIT"


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(doc: dict[str, Any]) -> None:
    if doc.get("certificate_version") != 1 or doc.get("claim_status") != STATUS:
        raise Rejected("header")
    payload = doc.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise Rejected("schema")
    if doc.get("payload_sha256") != hashlib.sha256(canonical(payload)).hexdigest():
        raise Rejected("payload hash")
    protocol = payload.get("protocol", {})
    if (protocol.get("origins") != [267175, 261267, 269074] or
            protocol.get("counts") != [256, 512] or
            protocol.get("laws") != ["all_plus", "alternating_index",
                                       "mod4_character", "half_split"] or
            protocol.get("spectra_for_all_laws") is not True or
            protocol.get("source_response_used") is not False):
        raise Rejected("protocol")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 144:
        raise Rejected("rows")
    if len({(r.get("origin"), r.get("count"), r.get("Q"),
             r.get("kernel_exponent"), r.get("law")) for r in rows}) != 144:
        raise Rejected("row keys")
    audit = payload.get("finite_audit", {})
    try:
        if (audit.get("rows") != 144 or audit.get("settings") != 36 or
                audit.get("laws") != 4 or
                float(audit["max_spectral_over_schur"]) >= 0.78 or
                float(audit["max_spectral_over_frobenius"]) >= 0.63 or
                audit.get("finite_schur_violations") != 0 or
                audit.get("finite_frobenius_violations") != 0 or
                audit.get("arithmetic_advance") != "NO" or
                audit.get("fixed_power_credit") != 0):
            raise Rejected("audit")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("audit values") from error
    if payload.get("law_winner_audit", {}).get("winner_counts") != {
            "all_plus": 30, "alternating_index": 0,
            "mod4_character": 6, "half_split": 0}:
        raise Rejected("winner census")
    expected = {
        "TPC360_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC360_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC360_ALL_LAW_SPECTRAL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC360_SCHUR_SLACK": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC360_LAW_UNIFORM_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC360_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC360_SOURCE_UNIFORM_L2": "OPEN", "TPC360_ARITHMETIC_ADVANCE": "NO",
        "TPC360_FIXED_POWER_CREDIT": 0, "TPC360_FULL_GATE_B": "OPEN",
        "TPC360_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        if payload.get("claim_firewall", {}).get(key) != value:
            raise Rejected("firewall " + key)


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        doc = json.loads(CERTIFICATE.read_bytes())
        validate(doc)
        baseline = hashlib.sha256(canonical(doc)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "rows"), []),
            (("payload", "protocol", "counts"), [256, 512, 1024]),
            (("payload", "protocol", "spectra_for_all_laws"), False),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "finite_audit", "max_spectral_over_schur"), "0.9"),
            (("payload", "finite_audit", "max_spectral_over_frobenius"), "0.9"),
            (("payload", "finite_audit", "rows"), 143),
            (("payload", "law_winner_audit", "winner_counts", "all_plus"), 29),
            (("payload", "claim_firewall", "TPC360_SCHUR_SLACK"), "PROVED"),
            (("payload", "claim_firewall", "TPC360_LAW_UNIFORM_CAP"), "PROVED"),
            (("payload", "claim_firewall", "TPC360_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC360_FIXED_POWER_CREDIT"), 1),
            (("payload_sha256",), "0" * 64),
        ]
        rejected = 0
        for path, value in mutations:
            item = copy.deepcopy(doc)
            target: Any = item
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            try:
                validate(item)
            except Rejected:
                rejected += 1
        if rejected != len(mutations) or hashlib.sha256(canonical(doc)).hexdigest() != baseline:
            raise Rejected("mutation census")
        print("TPC360_STRESS=PASS exact_baseline=1 mutations=14")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC360_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
