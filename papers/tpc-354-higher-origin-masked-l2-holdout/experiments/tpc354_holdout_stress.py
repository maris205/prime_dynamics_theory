#!/usr/bin/env python3
"""Mutation stress for the TPC-354 higher-origin holdout certificate.

The stress suite never writes the canonical JSON.  It mutates in-memory
copies and checks that the fail-closed structural validator rejects them.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-354-higher-origin-masked-l2-holdout/results/"
    "tpc354_certificate.json")
SCHEMA = "TPC354_HIGHER_ORIGIN_MASKED_L2_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT"
PARENT_HASH = (
    "2638df53704a08d6f278de7b60ddf472873c69b6eebdbdad172b4c225b2fb7e9")


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
    if lock.get("TPC353_code_sha256") != PARENT_HASH:
        raise Rejected("parent lock")
    protocol = payload.get("protocol", {})
    if protocol.get("origins") != [21001, 23001, 25001] or \
            protocol.get("source_counts") != [256, 512, 1024] or \
            protocol.get("q_anchors") != [24, 54, 80] or \
            protocol.get("kernel_exponents") != [1, 2]:
        raise Rejected("protocol")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 216:
        raise Rejected("rows")
    if payload.get("row_digest") != hashlib.sha256(
            canonical(rows)).hexdigest():
        raise Rejected("row digest")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("law")) for row in rows}
    if len(keys) != 216:
        raise Rejected("duplicate key")
    audit = payload.get("finite_audit", {})
    if audit.get("positive_output_alignment") != 216 or \
            audit.get("negative_output_alignment") != 0 or \
            audit.get("unresolved") != 0 or \
            audit.get("fixed_power_credit") != 0 or \
            audit.get("arithmetic_advance") != "NO":
        raise Rejected("audit firewall")
    firewall = payload.get("claim_firewall", {})
    if firewall.get("TPC354_UNIFORM_L2") != "OPEN" or \
            firewall.get("TPC354_ARITHMETIC_ADVANCE") != "NO" or \
            firewall.get("TPC354_FULL_GATE_B") != "OPEN":
        raise Rejected("claim firewall")
    anchor = payload.get("exact_anchor", {})
    if anchor.get("identity_exact") is not True or \
            anchor.get("left_energy_digest") != \
            "70d45bec53471bb116856860de853d15c7666cae6be1d6360574f71ee29db40f":
        raise Rejected("anchor")


def main() -> int:
    if any(arg not in ("--check",) for arg in sys.argv[1:]):
        raise SystemExit("optional --check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations: list[dict[str, Any]] = []

        item = copy.deepcopy(document)
        item["payload"]["schema"] = "MUTATED"
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload"]["rows"].pop()
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload"]["rows"][0]["law"] = "mutated_law"
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload"]["parent_lock"]["TPC353_code_sha256"] = "0" * 64
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload"]["finite_audit"]["fixed_power_credit"] = 1
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload"]["claim_firewall"]["TPC354_UNIFORM_L2"] = "PROVED"
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload"]["exact_anchor"]["left_energy_digest"] = "0" * 64
        mutations.append(item)
        item = copy.deepcopy(document)
        item["payload_sha256"] = "0" * 64
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
        print("TPC354_STRESS=PASS exact_baseline=1 mutations=8")
        return 0
    except (Rejected, OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print("TPC354_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
