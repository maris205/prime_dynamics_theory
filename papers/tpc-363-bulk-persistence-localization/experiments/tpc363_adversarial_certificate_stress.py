#!/usr/bin/env python3
"""Adversarial mutation stress for the TPC-363 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-363-bulk-persistence-localization/results/"
    "tpc363_certificate.json")
SCHEMA = "TPC363_BULK_PERSISTENCE_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION"


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
    protocol = payload.get("protocol", {})
    if (protocol.get("origins") != [313030, 311166, 321651] or
            protocol.get("counts") != [256, 512] or
            protocol.get("q_anchors") != [80, 128, 256] or
            protocol.get("kernel_exponents") != [1, 2] or
            protocol.get("laws") != ["all_plus", "alternating_index",
                                       "mod4_character", "half_split"] or
            protocol.get("spectra_for_all_laws") is not True or
            protocol.get("source_response_used") is not False or
            protocol.get("trim_denominator") != 20):
        raise Rejected("protocol")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 144:
        raise Rejected("rows")
    if len({(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("law"))
            for row in rows}) != 144:
        raise Rejected("row keys")
    audit = payload.get("finite_audit", {})
    try:
        if (audit.get("rows") != 144 or audit.get("settings") != 36 or
                audit.get("laws") != 4 or audit.get("spectral_rows") != 144 or
                audit.get("first_spectral_cap_failure_Q") != 128 or
                audit.get("spectral_cap_violations") != 18 or
                audit.get("spectral_cap_violations_Q128") != 6 or
                audit.get("spectral_cap_violations_Q256") != 12 or
                audit.get("bulk_persistence_after_schur_trim") != 18 or
                audit.get("bulk_persistence_after_eigenvector_trim") != 18 or
                float(audit["min_trimmed_spectral_over_violations"]) <= 0.64 or
                float(audit["max_trimmed_spectral_Q80_control"]) >= 0.64 or
                audit.get("finite_schur_violations") != 0 or
                audit.get("finite_frobenius_violations") != 0 or
                audit.get("fixed_power_credit") != 0 or
                audit.get("arithmetic_advance") != "NO"):
            raise Rejected("audit")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("audit values") from error
    if payload.get("law_census", {}).get("violation_law_counts") != {
            "all_plus": 18, "alternating_index": 0,
            "mod4_character": 0, "half_split": 0}:
        raise Rejected("law census")
    expected = {
        "TPC363_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC363_FINITE_ENVELOPE_INEQUALITIES": "PROVED_EXACT_FINITE",
        "TPC363_FIRST_Q128_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_BULK_PERSISTENCE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_SINGLE_ROW_SPIKE_EXPLANATION": "REFUTED_SCOPED_ON_DECLARED_TRIMS",
        "TPC363_EIGENVECTOR_DELOCALIZATION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC363_RENORMALIZED_REPAIR": "OPEN",
        "TPC363_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC363_SOURCE_UNIFORM_L2": "OPEN",
        "TPC363_ARITHMETIC_ADVANCE": "NO",
        "TPC363_FIXED_POWER_CREDIT": 0,
        "TPC363_FULL_GATE_B": "OPEN", "TPC363_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        if payload.get("claim_firewall", {}).get(key) != value:
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
            (("payload", "protocol", "q_anchors"), [80, 128]),
            (("payload", "protocol", "trim_denominator"), 10),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "rows"), []),
            (("payload", "finite_audit", "rows"), 143),
            (("payload", "finite_audit", "first_spectral_cap_failure_Q"), 256),
            (("payload", "finite_audit", "spectral_cap_violations"), 0),
            (("payload", "finite_audit", "spectral_cap_violations_Q128"), 5),
            (("payload", "finite_audit", "bulk_persistence_after_schur_trim"), 17),
            (("payload", "finite_audit", "min_trimmed_spectral_over_violations"), "0.2"),
            (("payload", "law_census", "violation_law_counts", "all_plus"), 17),
            (("payload", "claim_firewall", "TPC363_BULK_PERSISTENCE"), "PROVED"),
            (("payload", "claim_firewall", "TPC363_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC363_FIXED_POWER_CREDIT"), 1),
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
        print("TPC363_STRESS=PASS exact_baseline=1 mutations=16")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC363_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
