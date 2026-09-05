#!/usr/bin/env python3
"""Exact CRT-origin obstruction for the declared TPC proxy."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc403_certificate.json"
SCHEMA = "TPC403_C1_CRT_ORIGIN_PROXY_OBSTRUCTION_V1"
STATUS = "PROVED_EXACT_FINITE_CRT_PROXY_OBSTRUCTION"
Q, N, H, B = 8192, 1024, 66, 1_000_000


class Failure(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def primes(limit: int) -> list[int]:
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p : limit + 1 : p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def crt(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    modulus = math.prod(moduli)
    value = 0
    for residue, modulus_i in zip(residues, moduli):
        quotient = modulus // modulus_i
        value += residue * quotient * pow(quotient, -1, modulus_i)
    return value % modulus, modulus


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def build_cases() -> list[dict]:
    shell = [p for p in primes(2 * Q) if Q < p <= 2 * Q]
    need(len(shell) == 872, "shell cardinality")
    cases = []
    for m in range(1, 5):
        selected = shell[: 2 * m]
        residues = [0 if i % 2 == 0 else -N for i in range(2 * m)]
        residue, period = crt(residues, selected)
        origin = residue + ((B - residue) // period + 1) * period
        weights = [Fraction(p**3, Q**2 * (p - 1)) for p in selected]
        signed = [w if i % 2 == 0 else -w for i, w in enumerate(weights)]
        total = sum(signed, Fraction(0))
        p_minus = sum(weights[1::2], Fraction(0))
        t1 = Fraction(H * H, H * H + 1)
        direct = Fraction(0)
        for p, coefficient in zip(selected, signed):
            if origin % p and (origin + 1) % p:
                direct -= coefficient * t1
        bu = sum((coefficient for p, coefficient in zip(selected, signed) if origin % p == 0), Fraction(0))
        bv = sum((coefficient for p, coefficient in zip(selected, signed) if (origin + 1) % p == 0), Fraction(0))
        reduced = t1 * (-total + bu + bv)
        need(origin > B, "origin bound")
        need(all(origin % p == residue_i % p for p, residue_i in zip(selected, residues)), "CRT")
        need(all((origin + 1) % p for p in selected), "right endpoint unit")
        need(all(origin % p == 0 for p in selected[::2]), "positive hits")
        need(all(origin % p for p in selected[1::2]), "negative primes miss window")
        need(direct == reduced == t1 * p_minus, "signed coefficient")
        need(bu == sum(signed[::2], Fraction(0)) and bv == 0, "profile")
        cases.append({
            "m": m, "selected_primes": selected, "residues": residues,
            "crt_residue": residue, "crt_period": period, "origin": origin,
            "origin_lower_bound": B, "window_pair": [origin, origin + 1],
            "positive_prime_hits_offset": [0], "negative_prime_hits_offset": [N],
            "A_sigma": fraction_text(total), "P_minus": fraction_text(p_minus),
            "T1": fraction_text(t1), "direct": fraction_text(direct),
            "reduced": fraction_text(reduced),
            "raw_ratio_to_abs_A": fraction_text(t1 * p_minus / abs(total)),
            "exact_identity": True,
        })
    return cases


def payload() -> dict:
    return {
        "schema": SCHEMA, "status": STATUS, "Q": Q, "N": N, "H": H, "B": B,
        "sign_law": "alternating_index", "sign_definition": "sigma_i=(-1)^i",
        "negative_congruence": "o = -N (mod p_i) for odd i",
        "identity": "M_sigma(o,o+1)=T1[-A_sigma+b_sigma(o)+b_sigma(o+1)]",
        "cases": build_cases(),
        "claim_firewall": {
            "CRT_PROXY_STRUCTURE": "PROVED_EXACT_FINITE",
            "ARITHMETIC_SIGN_IDENTIFICATION": "OPEN",
            "NORMALIZED_GROWING_OBSTRUCTION": "OPEN",
            "ARITHMETIC_ADVANCE": "NO", "FIXED_POWER_CREDIT": 0,
            "FULL_GATE_B": "OPEN", "TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "TEST_C1_CRT_PROXY_NORMALIZATION_BOUNDARY",
    }


def write() -> None:
    p = payload()
    RESULT.write_bytes(canonical({"certificate_version": 1, "claim_status": STATUS,
                                  "payload": p, "payload_sha256": hashlib.sha256(canonical(p)).hexdigest()}))


def check_document(document: dict) -> None:
    need(type(document) is dict and set(document) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "claim status")
    p = document["payload"]
    need(document["payload_sha256"] == hashlib.sha256(canonical(p)).hexdigest(), "digest")
    need(p == payload(), "certificate differs from exact CRT replay")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write()
        print("TPC403_CERTIFICATE=WRITTEN")
    elif args.check:
        check_document(json.loads(RESULT.read_bytes()))
        print("TPC403_CERTIFICATE=PASS cases=4 max_m=4 crt_origin=PASS signed_obstruction=PASS")
    else:
        raise SystemExit("explicit --check or --write required")


if __name__ == "__main__":
    main()
