#!/usr/bin/env python3
"""Fail-closed in-memory mutation stress for the TPC-355 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/results/"
    "tpc355_certificate.json")
SCHEMA = "TPC355_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT"
PARENT_354_HASH = (
    "033be8d4e2b2f977975a35f014b564ed0f7523578ec2909eb66405fa789e4ceb")


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    if document.get("certificate_version") != 1 or \
            document.get("claim_status") != STATUS:
        raise Rejected("header")
    payload = document.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise Rejected("schema")
    if document.get("payload_sha256") != hashlib.sha256(
            canonical(payload)).hexdigest():
        raise Rejected("payload hash")
    lock = payload.get("parent_lock", {})
    if lock.get("TPC354_certificate_sha256") != PARENT_354_HASH:
        raise Rejected("parent lock")
    protocol = payload.get("protocol", {})
    if protocol.get("panel_names") != ["low_parent", "higher_parent",
                                        "fresh_holdout"] or \
            protocol.get("source_counts") != [256, 512, 1024] or \
            protocol.get("q_anchors") != [24, 54, 80] or \
            protocol.get("kernel_exponents") != [1, 2]:
        raise Rejected("protocol")
    normalization = protocol.get("normalization", {})
    if normalization.get("response_independent") is not True or \
            normalization.get("source_independent") is not True or \
            normalization.get("sign_law_independent") is not True:
        raise Rejected("normalization independence")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 648:
        raise Rejected("rows")
    keys = {(row.get("panel"), row.get("origin"), row.get("count"),
             row.get("Q"), row.get("kernel_exponent"), row.get("law"))
            for row in rows}
    if len(keys) != 648:
        raise Rejected("duplicate key")
    if payload.get("row_digest") != hashlib.sha256(
            canonical(rows)).hexdigest():
        raise Rejected("row digest")
    audit = payload.get("finite_audit", {})
    if audit.get("rows") != 648 or \
            audit.get("raw_positive_alignment") != 647 or \
            audit.get("raw_negative_alignment") != 1 or \
            audit.get("normalized_positive_alignment") != 647 or \
            audit.get("normalized_negative_alignment") != 1 or \
            audit.get("raw_unresolved") != 0 or \
            audit.get("normalized_unresolved") != 0 or \
            audit.get("fixed_power_credit") != 0 or \
            audit.get("arithmetic_advance") != "NO":
        raise Rejected("audit")
    floor = payload.get("transfer_summary", {}).get("all_plus_floor", {})
    try:
        if not (float(floor["raw_higher_drop"]) >
                float(floor["normalized_higher_drop"]) > 0 and
                0 < float(floor["drop_reduction_fraction"]) < 1):
            raise Rejected("floor repair")
    except (KeyError, TypeError, ValueError) as error:
        raise Rejected("floor repair values") from error
    firewall = payload.get("claim_firewall", {})
    if firewall.get("TPC355_GEOMETRY_DEFINITION") != \
            "PROVED_EXACT_FINITE_DECLARED_MODEL" or \
            firewall.get("TPC355_ALL_PLUS_FLOOR_REPAIR") != \
            "NUMERICALLY_CERTIFIED_FINITE_PARTIAL" or \
            firewall.get("TPC355_ALL_PLUS_MEAN_REPAIR") != "REFUTED_SCOPED" or \
            firewall.get("TPC355_SOURCE_UNIFORM_L2") != "OPEN" or \
            firewall.get("TPC355_ARITHMETIC_ADVANCE") != "NO" or \
            firewall.get("TPC355_FULL_GATE_B") != "OPEN" or \
            firewall.get("TPC355_TWIN_PRIME_RESULT") != "NONE":
        raise Rejected("firewall")
    anchor = payload.get("exact_anchor", {})
    if anchor.get("identity_exact") is not True or \
            anchor.get("geometry_positive") is not True:
        raise Rejected("anchor")


def main() -> int:
    if any(arg != "--check" for arg in sys.argv[1:]) or len(sys.argv) != 2:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations: list[dict[str, Any]] = []
        for path, value in (
                (("payload", "schema"), "MUTATED"),
                (("payload", "rows"), None),
                (("payload", "parent_lock", "TPC354_certificate_sha256"),
                 "0" * 64),
                (("payload", "finite_audit", "fixed_power_credit"), 1),
                (("payload", "finite_audit", "raw_positive_alignment"), 648),
                (("payload", "protocol", "normalization",
                  "response_independent"), False),
                (("payload", "claim_firewall", "TPC355_SOURCE_UNIFORM_L2"),
                 "PROVED"),
                (("payload", "claim_firewall", "TPC355_TWIN_PRIME_RESULT"),
                 "PROVED"),
                (("payload", "exact_anchor", "identity_exact"), False),
                (("payload_sha256",), "0" * 64)):
            item = copy.deepcopy(document)
            target: Any = item
            for key in path[:-1]:
                target = target[key]
            if path[-1] == "rows" and value is None:
                target[path[-1]] = target[path[-1]][:-1]
            else:
                target[path[-1]] = value
            mutations.append(item)
        rejected = 0
        for mutated in mutations:
            try:
                validate(mutated)
            except Rejected:
                rejected += 1
        if rejected != len(mutations) or \
                hashlib.sha256(canonical(document)).hexdigest() != baseline:
            raise Rejected("mutation census")
        print("TPC355_STRESS=PASS exact_baseline=1 mutations=10")
        return 0
    except (Rejected, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print("TPC355_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
