#!/usr/bin/env python3
"""Contract-level mutation tests for the TPC-402 certificate."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-402-c1-signed-diagonal-term-audit/results/tpc402_certificate.json"
SCHEMA = "TPC402_C1_SIGNED_DIAGONAL_TERM_AUDIT_V1"
STATUS = "PROVED_EXACT_FINITE_SIGNED_DIAGONAL_TERM_AUDIT"


class Failure(ValueError):
    pass


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Failure("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise Failure("non-finite JSON constant")


def validate(document: dict) -> None:
    if type(document) is not dict or set(document) != {"certificate_version", "claim_status", "payload", "payload_sha256"}:
        raise Failure("document schema")
    if type(document["certificate_version"]) is not int or document["certificate_version"] != 1:
        raise Failure("version")
    if document["claim_status"] != STATUS:
        raise Failure("claim status")
    payload = document["payload"]
    if type(payload) is not dict or document["payload_sha256"] != hashlib.sha256(canonical(payload)).hexdigest():
        raise Failure("digest or payload")
    if set(payload) != {"schema", "status", "audit", "anchor_boundary", "identity", "claim_firewall", "round2_clue"}:
        raise Failure("payload schema")
    if payload["schema"] != SCHEMA or payload["status"] != STATUS:
        raise Failure("payload header")
    audit = payload["audit"]
    if type(audit) is not dict or audit != {
        "H": 66, "N": 1024, "Q": 8192,
        "origins": [7600001, 7603209, 7606417, 7609625, 7612833, 7616041],
        "positions": [0, 1, 512, 1022, 1023], "shell_cardinality": 872,
        "laws": ["all_plus", "alternating_index"], "signed_component_rows": 240,
        "signed_component_prime_comparisons": 209280,
        "rows_by_law": {"all_plus": 120, "alternating_index": 120},
        "diagonal_pairs_skipped": 60, "all_signed_coefficients_exact": True,
    }:
        raise Failure("audit contract")
    if payload["round2_clue"] != "TEST_C1_SIGNED_DIAGONAL_TERM_GROWING_OBSTRUCTION":
        raise Failure("clue")


def load() -> dict:
    return json.loads(CERT.read_bytes(), object_pairs_hook=reject_duplicate_keys,
                      parse_constant=reject_constant)


def main() -> None:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    original = load()
    validate(original)
    mutations = ("schema", "status", "signed_component_rows")
    rejected = 0
    for field in mutations:
        mutated = copy.deepcopy(original)
        if field == "schema":
            mutated["payload"]["schema"] = "BAD"
        elif field == "status":
            mutated["payload"]["status"] = "BAD"
        else:
            mutated["payload"]["audit"][field] = 239
        mutated["payload_sha256"] = hashlib.sha256(canonical(mutated["payload"])).hexdigest()
        try:
            validate(mutated)
        except Failure:
            rejected += 1
    if rejected != len(mutations):
        raise Failure("mutation escaped")
    print("TPC402_STRESS=PASS mutations=3 strict_contract=PASS")


if __name__ == "__main__":
    main()
