#!/usr/bin/env python3
"""Independent exact reverse-order replay for TPC-402."""
from __future__ import annotations
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-402-c1-signed-diagonal-term-audit/results/tpc402_certificate.json"
SCHEMA = "TPC402_C1_SIGNED_DIAGONAL_TERM_AUDIT_V1"
STATUS = "PROVED_EXACT_FINITE_SIGNED_DIAGONAL_TERM_AUDIT"
Q, N, H = 8192, 1024, 66
ORIGINS = (7600001, 7603209, 7606417, 7609625, 7612833, 7616041)
POSITIONS = (0, 1, 512, 1022, 1023)


class Failure(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


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


def load_document() -> dict:
    return json.loads(CERT.read_bytes(), object_pairs_hook=reject_duplicate_keys,
                      parse_constant=reject_constant)


def primes(limit: int) -> list[int]:
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p : limit + 1 : p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def reverse_audit() -> dict:
    shell_ascending = [p for p in primes(2 * Q) if p > Q]
    need(len(shell_ascending) == 872, "shell")
    laws = ("all_plus", "alternating_index")
    rows_by_law = {law: 0 for law in laws}
    comparisons = 0
    diagonal_skipped = 0
    for law in laws:
        signed_weights = [
            Fraction(p**3, Q**2 * (p - 1)) * (1 if law == "all_plus" or i % 2 == 0 else -1)
            for i, p in enumerate(shell_ascending)
        ]
        total = sum(signed_weights, Fraction(0))
        for origin in ORIGINS:
            for x in POSITIONS:
                u = origin + x
                bu = sum((w for w, p in zip(signed_weights, shell_ascending) if u % p == 0), Fraction(0))
                for y in POSITIONS:
                    v = origin + y
                    if u == v:
                        diagonal_skipped += 1
                        continue
                    bv = sum((w for w, p in zip(signed_weights, shell_ascending) if v % p == 0), Fraction(0))
                    kernel = Fraction(H * H, H * H + (u - v) * (u - v))
                    direct = Fraction(0)
                    for w, p in reversed(tuple(zip(signed_weights, shell_ascending))):
                        if u % p and v % p:
                            direct -= w * kernel
                    reduced = kernel * (-total + bu + bv)
                    need(direct == reduced, "reverse signed coefficient")
                    rows_by_law[law] += 1
                    comparisons += len(shell_ascending)
    return {
        "H": H, "N": N, "Q": Q, "origins": list(ORIGINS), "positions": list(POSITIONS),
        "shell_cardinality": len(shell_ascending), "laws": list(laws),
        "signed_component_rows": sum(rows_by_law.values()),
        "signed_component_prime_comparisons": comparisons,
        "rows_by_law": rows_by_law, "diagonal_pairs_skipped": diagonal_skipped,
        "all_signed_coefficients_exact": True,
    }


def expected_anchor() -> dict:
    return {"Q": 8, "N": 13, "p": 11, "u": 7600001, "v": 7600012,
            "active_masks": True, "difference": -11, "divisibility_indicator": True,
            "production_condition_holds": False}


def main() -> None:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    document = load_document()
    need(type(document) is dict, "document type")
    need(set(document) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document schema")
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "claim status")
    payload = document["payload"]
    need(type(payload) is dict, "payload type")
    need(document["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(), "digest")
    need(payload["schema"] == SCHEMA and payload["status"] == STATUS, "payload header")
    expected = reverse_audit()
    need(payload["audit"] == expected, "certificate audit differs from reverse replay")
    need(payload["anchor_boundary"] == expected_anchor(), "anchor")
    need(payload["round2_clue"] == "TEST_C1_SIGNED_DIAGONAL_TERM_GROWING_OBSTRUCTION", "clue")
    print("TPC402_INDEPENDENT_CHECK=PASS signed_rows=240 prime_comparisons=209280 reverse_shell=PASS anchor_boundary=PASS")


if __name__ == "__main__":
    main()
