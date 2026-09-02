#!/usr/bin/env python3
"""Fail-closed mutation stress for the TPC-356 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-356-geometry-adversarial-normalization-holdout/results/"
    "tpc356_certificate.json")
SCHEMA = "TPC356_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT"
PARENT_CERT_HASH = (
    "29c5e824b415e675c931396567337cbb583b8f952b489ea2a386a63c649fff7b")


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    if document.get("certificate_version") != 1 or             document.get("claim_status") != STATUS:
        raise Rejected("header")
    payload = document.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise Rejected("schema")
    if document.get("payload_sha256") != hashlib.sha256(
            canonical(payload)).hexdigest():
        raise Rejected("payload hash")
    lock = payload.get("parent_lock", {})
    if lock.get("TPC355_certificate_sha256") != PARENT_CERT_HASH:
        raise Rejected("parent lock")
    protocol = payload.get("protocol", {})
    if protocol.get("selected_origins") != [38423, 42010, 45597] or             protocol.get("candidate_origins") != list(range(38001, 48552, 211)) or             protocol.get("pilot_count") != 256 or             protocol.get("minimum_separation") != 1536 or             protocol.get("source_counts") != [256, 512, 1024] or             protocol.get("q_anchors") != [24, 54, 80] or             protocol.get("kernel_exponents") != [1, 2]:
        raise Rejected("protocol")
    if protocol.get("selection_uses_response") is not False or             protocol.get("selection_uses_source") is not False:
        raise Rejected("selection independence")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 216:
        raise Rejected("rows")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("law")) for row in rows}
    if len(keys) != 216:
        raise Rejected("duplicate key")
    if payload.get("row_digest") != hashlib.sha256(
            canonical(rows)).hexdigest():
        raise Rejected("row digest")
    audit = payload.get("finite_audit", {})
    if audit.get("rows") != 216 or             audit.get("raw_positive_alignment") != 216 or             audit.get("raw_negative_alignment") != 0 or             audit.get("normalized_positive_alignment") != 216 or             audit.get("normalized_negative_alignment") != 0 or             audit.get("fixed_power_credit") != 0 or             audit.get("arithmetic_advance") != "NO":
        raise Rejected("audit")
    try:
        if not (float(audit["normalization_min_gain"]) > 0 and
                float(audit["normalization_mean_gain"]) > 0):
            raise Rejected("gains")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("gains") from error
    firewall = payload.get("claim_firewall", {})
    for key, value in (
            ("TPC356_GEOMETRY_SELECTION", "PROVED_EXACT_FINITE_DETERMINISTIC"),
            ("TPC356_SELECTION_RESPONSE_INDEPENDENCE", "PROVED_EXACT_FINITE"),
            ("TPC356_PANEL_REPLAY", "NUMERICALLY_CERTIFIED_FINITE_216_ROWS"),
            ("TPC356_ALL_PLUS_MIN_GAIN",
             "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC356_ALL_PLUS_MEAN_GAIN",
             "NUMERICALLY_CERTIFIED_FINITE_SCOPED"),
            ("TPC356_SOURCE_UNIFORM_L2", "OPEN"),
            ("TPC356_ARITHMETIC_ADVANCE", "NO"),
            ("TPC356_FULL_GATE_B", "OPEN"),
            ("TPC356_TWIN_PRIME_RESULT", "NONE")):
        if firewall.get(key) != value:
            raise Rejected("firewall " + key)
    anchor = payload.get("exact_anchor", {})
    if anchor.get("identity_exact") is not True or             anchor.get("geometry_positive") is not True:
        raise Rejected("anchor")


def main() -> int:
    if any(arg != "--check" for arg in sys.argv[1:]) or len(sys.argv) != 2:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "rows"), None),
            (("payload", "parent_lock", "TPC355_certificate_sha256"),
             "0" * 64),
            (("payload", "finite_audit", "fixed_power_credit"), 1),
            (("payload", "finite_audit", "raw_positive_alignment"), 215),
            (("payload", "protocol", "selection_uses_response"), True),
            (("payload", "claim_firewall", "TPC356_SOURCE_UNIFORM_L2"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC356_TWIN_PRIME_RESULT"),
             "PROVED"),
            (("payload", "exact_anchor", "identity_exact"), False),
            (("payload_sha256",), "0" * 64),
        ]
        rejected = 0
        for path, value in mutations:
            item = copy.deepcopy(document)
            target: Any = item
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = (target[path[-1]][:-1]
                                if path[-1] == "rows" and value is None
                                else value)
            try:
                validate(item)
            except Rejected:
                rejected += 1
        if rejected != len(mutations) or                 hashlib.sha256(canonical(document)).hexdigest() != baseline:
            raise Rejected("mutation census")
        print("TPC356_STRESS=PASS exact_baseline=1 mutations=10")
        return 0
    except (Rejected, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print("TPC356_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
