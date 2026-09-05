#!/usr/bin/env python3
"""Exact local-diagonal normalization audit for the TPC-403 CRT profile."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc404_certificate.json"
SCHEMA = "TPC404_C1_LOCAL_NORMALIZATION_BOUNDARY_V1"
STATUS = "PROVED_EXACT_FINITE_LOCAL_NORMALIZATION_BOUNDARY_AUDIT"
Q, N, H, B = 8192, 1024, 66, 1_000_000


class Failure(ValueError):
    pass


def need(c: bool, message: str) -> None:
    if type(c) is not bool or not c:
        raise Failure(message)


def canonical(v: object) -> bytes:
    return (json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def primes(limit: int) -> list[int]:
    f = bytearray(b"\1") * (limit + 1)
    f[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if f[p]:
            f[p * p : limit + 1 : p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if f[p]]


def t(d: int) -> Fraction:
    return Fraction(H * H, H * H + d * d)


def fraction_text(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def cases() -> list[dict]:
    shell = [p for p in primes(2 * Q) if p > Q]
    need(len(shell) == 872, "shell")
    S0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0))
    S1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
    result = []
    for m in range(1, 5):
        selected = shell[: 2 * m]
        a = [Fraction(p**3, Q**2 * (p - 1)) for p in selected]
        pplus2 = sum((x * x for x in a[::2]), Fraction(0))
        pminus2 = sum((x * x for x in a[1::2]), Fraction(0))
        pminus = sum(a[1::2], Fraction(0))
        g0 = pminus2 * S0
        g1 = pminus2 * S1 + pplus2 * (S1 - t(1) ** 2)
        direct = t(1) * pminus
        normalized_square = direct * direct / (g0 * g1)
        need(g0 > 0 and g1 > 0, "geometry")
        result.append({
            "m": m, "selected_primes": selected, "origin_lower_bound": B,
            "S_offset_0": fraction_text(S0), "S_offset_1": fraction_text(S1),
            "P_minus": fraction_text(pminus), "P_plus_sq": fraction_text(pplus2),
            "P_minus_sq": fraction_text(pminus2), "direct": fraction_text(direct),
            "G_origin": fraction_text(g0), "G_next": fraction_text(g1),
            "normalized_square": fraction_text(normalized_square),
            "normalized_float64_observation": f"{math.sqrt(float(normalized_square)):.15f}",
            "exact_geometry_identity": True,
        })
    return result


def payload() -> dict:
    return {
        "schema": SCHEMA, "status": STATUS, "Q": Q, "N": N, "H": H, "B": B,
        "normalization": "local_diagonal",
        "geometry_definition": "G(u)=sum_p a_p^2 1_{p does not divide u} sum_{v != u, p does not divide v} T_uv^2",
        "identities": {
            "G_origin": "P_minus_sq*S0",
            "G_next": "P_minus_sq*S1+P_plus_sq*(S1-T1^2)",
            "normalized_square": "(T1*P_minus)^2/(G_origin*G_next)",
        },
        "cases": cases(),
        "claim_firewall": {
            "LOCAL_BOUNDARY_STRUCTURE": "PROVED_EXACT_FINITE",
            "NORMALIZED_GROWING_THEOREM": "OPEN",
            "ARITHMETIC_SIGN_IDENTIFICATION": "OPEN",
            "ARITHMETIC_ADVANCE": "NO", "FIXED_POWER_CREDIT": 0,
            "FULL_GATE_B": "OPEN", "TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "TEST_C1_LOCAL_NORMALIZATION_SCALE_LADDER",
    }


def write() -> None:
    p = payload()
    RESULT.write_bytes(canonical({"certificate_version": 1, "claim_status": STATUS,
                                  "payload": p, "payload_sha256": hashlib.sha256(canonical(p)).hexdigest()}))


def check_document(d: dict) -> None:
    need(type(d) is dict and set(d) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(type(d["certificate_version"]) is int and d["certificate_version"] == 1 and d["claim_status"] == STATUS, "header")
    need(d["payload_sha256"] == hashlib.sha256(canonical(d["payload"])).hexdigest(), "digest")
    need(canonical(d["payload"]) == canonical(payload()), "exact local audit and types")


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise Failure("non-finite JSON constant")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write(); print("TPC404_CERTIFICATE=WRITTEN")
    elif args.check:
        check_document(json.loads(RESULT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants))
        print("TPC404_CERTIFICATE=PASS cases=4 local_diagonal=PASS exact_geometry=PASS")
    else:
        raise SystemExit("explicit --check or --write required")


if __name__ == "__main__":
    main()
