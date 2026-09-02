#!/usr/bin/env python3
"""Fail-closed schema and claim-firewall mutation stress for TPC-359."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / "papers/tpc-359-geometry-adversarial-high-origin-holdout/results/tpc359_certificate.json"
SCHEMA = "TPC359_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_HIGH_ORIGIN_HOLDOUT"


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
    if (protocol.get("candidate_origins") != list(range(260001, 270552, 211)) or
            protocol.get("origins") != [267175, 261267, 269074] or
            protocol.get("counts") != [256, 512, 1024, 2048] or
            protocol.get("q_anchors") != [24, 54, 80] or
            protocol.get("kernel_exponents") != [1, 2] or
            protocol.get("source_response_used") is not False or
            protocol.get("sign_response_used") is not False):
        raise Rejected("protocol")
    selection = payload.get("selection", {})
    if selection.get("selected_origins") != [267175, 261267, 269074] or not selection.get("records"):
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
        if (audit.get("rows") != 288 or audit.get("origins") != 3 or
                audit.get("candidate_count") != 51 or
                audit.get("finite_schur_violations") != 0 or
                audit.get("finite_frobenius_violations") != 0 or
                audit.get("fixed_power_credit") != 0 or
                audit.get("arithmetic_advance") != "NO" or
                float(audit["normalized_schur_max"]) >= 0.83 or
                float(audit["normalized_all_plus_spectral_max"]) >= 0.64 or
                float(audit["raw_all_plus_spectral_max"]) <= 1200):
            raise Rejected("audit")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("audit values") from error
    trans = audit.get("normalized_spectral_transitions", {})
    if trans.get("increase", 0) <= 0 or trans.get("decrease", 0) <= 0:
        raise Rejected("transition obstruction")
    firewall = payload.get("claim_firewall", {})
    expected = {
        "TPC359_GEOMETRY_SELECTION": "PROVED_EXACT_FINITE_RESPONSE_BLIND",
        "TPC359_HIGH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
        "TPC359_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC359_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
        "TPC359_PARENT_CAP_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC359_NORMALIZED_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC359_SPECTRAL_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
        "TPC359_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC359_SOURCE_UNIFORM_L2": "OPEN",
        "TPC359_ARITHMETIC_ADVANCE": "NO",
        "TPC359_FIXED_POWER_CREDIT": 0,
        "TPC359_FULL_GATE_B": "OPEN", "TPC359_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected.items():
        if firewall.get(key) != value:
            raise Rejected("firewall " + key)
    anchor = payload.get("exact_anchor", {})
    if anchor.get("matrix_symmetric") is not True or anchor.get("geometry_positive") is not True:
        raise Rejected("anchor")


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "rows"), []),
            (("payload", "protocol", "origins"), [52001, 120001, 220001]),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "selection", "selected_origins"), [260001, 260212, 260423]),
            (("payload", "finite_audit", "candidate_count"), 50),
            (("payload", "finite_audit", "normalized_schur_max"), "0.99"),
            (("payload", "finite_audit", "normalized_all_plus_spectral_max"), "0.91"),
            (("payload", "finite_audit", "normalized_spectral_transitions", "increase"), 0),
            (("payload", "claim_firewall", "TPC359_GROWING_OPERATOR_BOUND"), "PROVED"),
            (("payload", "claim_firewall", "TPC359_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC359_FIXED_POWER_CREDIT"), 1),
            (("payload", "exact_anchor", "geometry_positive"), False),
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
        if rejected != len(mutations) or hashlib.sha256(canonical(document)).hexdigest() != baseline:
            raise Rejected("mutation census")
        print("TPC359_STRESS=PASS exact_baseline=1 mutations=14")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print("TPC359_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
