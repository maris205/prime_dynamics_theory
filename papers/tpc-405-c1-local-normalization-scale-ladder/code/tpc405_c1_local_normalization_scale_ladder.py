#!/usr/bin/env python3
"""Exact scale ladder and uniform adjacent-entry bound for the TPC-404 proxy."""
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
RESULT = PROJECT / "results/tpc405_certificate.json"
SCHEMA = "TPC405_C1_LOCAL_NORMALIZATION_SCALE_LADDER_V1"
STATUS = "PROVED_UNIFORM_FINITE_CRT_PROXY_ADJACENT_ENTRY_BOUND"
Q, B = 8192, 1_000_000
HEIGHTS = (16, 32, 66, 128, 256)
MULTIPLICITIES = (1, 2, 3, 4)


class Failure(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise Failure("non-finite JSON constant")


def primes(limit: int) -> list[int]:
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p : limit + 1 : p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def crt(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    period = math.prod(moduli)
    residue = sum(r * (period // p) * pow(period // p, -1, p)
                  for r, p in zip(residues, moduli)) % period
    return residue, period


def text_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def row(H: int, m: int, shell: list[int]) -> dict:
    N = 4 * H
    selected = shell[: 2 * m]
    residues = [0 if i % 2 == 0 else -N for i in range(2 * m)]
    residue, period = crt(residues, selected)
    origin = residue + ((B - residue) // period + 1) * period
    t = lambda d: Fraction(H * H, H * H + d * d)
    S0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0))
    S1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
    amplitudes = [Fraction(p ** 3, Q * Q * (p - 1)) for p in selected]
    Vminus = sum((a * a for a in amplitudes[1::2]), Fraction(0))
    Vplus = sum((a * a for a in amplitudes[::2]), Fraction(0))
    Pminus = sum(amplitudes[1::2], Fraction(0))
    amin = min(amplitudes)
    G0 = Vminus * S0
    G1 = Vminus * S1 + Vplus * (S1 - t(1) ** 2)
    direct = t(1) * Pminus
    z2 = direct * direct / (G0 * G1)
    sharp2 = t(1) ** 2 / (amin * amin * S0 * S1)
    coarse2 = Fraction(16, H * H)
    need(origin > B and G0 > 0 and G1 > 0, "positive profile")
    need(z2 <= sharp2 <= coarse2, "uniform bound")
    return {
        "H": H, "N": N, "m": m, "Q": Q, "origin_lower_bound": B,
        "selected_primes": selected, "residues": residues,
        "crt_residue": residue, "crt_period": period, "origin": origin,
        "S0": text_fraction(S0), "S1": text_fraction(S1),
        "a_min": text_fraction(amin), "P_minus": text_fraction(Pminus),
        "V_minus": text_fraction(Vminus), "V_plus": text_fraction(Vplus),
        "G0": text_fraction(G0), "G1": text_fraction(G1),
        "direct": text_fraction(direct), "normalized_square": text_fraction(z2),
        "sharp_bound_square": text_fraction(sharp2),
        "coarse_bound_square_4_over_H": text_fraction(coarse2),
        "uniform_bound_exact": True,
        "normalized_float64_observation": f"{math.sqrt(float(z2)):.15f}",
        "H_times_normalized_float64_observation": f"{H * math.sqrt(float(z2)):.15f}",
    }


def payload() -> dict:
    shell = [p for p in primes(2 * Q) if p > Q]
    need(len(shell) == 872, "shell census")
    return {
        "schema": SCHEMA, "status": STATUS, "Q": Q, "origin_lower_bound": B,
        "heights": list(HEIGHTS), "multiplicities": list(MULTIPLICITIES),
        "window_rule": "N=4H", "normalization": "selected-prime local diagonal",
        "theorem_domain": {
            "H_and_N": "integers H,N with H>=1 and N>=H+2",
            "Q_and_primes": "integer Q>N and distinct primes Q<p_i<=2Q",
            "profile": "2m ordered primes, m>=1; even i residue 0, odd i residue -N",
            "origin": "o is a CRT solution above the declared origin lower bound",
            "proxy": "selected-prime masked local geometry from TPC-404",
        },
        "theorem": {
            "exact_sharp_bound": "0<=z<=t1/(a_min*sqrt(S0*S1))",
            "coarse_uniform_bound": "z<=4/(a_min*H)<=4/H",
            "proof_steps": ["P_minus^2<=m*V_minus", "G1>=V_minus*S1",
                            "V_minus>=m*a_min^2", "S0>=H/4", "S1>=H/4", "a_min>=1"],
            "scope": "one adjacent normalized proxy entry, not the full operator",
        },
        "cases": [row(H, m, shell) for H in HEIGHTS for m in MULTIPLICITIES],
        "claim_firewall": {
            "LOCAL_PROXY_ENTRY_BOUND": "PROVED_UNIFORM",
            "SCALE_LADDER_DECIMALS": "NUMERICAL_OBSERVATION",
            "FULL_OPERATOR_NORM": "OPEN", "NORMALIZED_GROWING_THEOREM": "OPEN",
            "ARITHMETIC_SIGN_IDENTIFICATION": "OPEN", "ARITHMETIC_ADVANCE": "NO",
            "FIXED_POWER_CREDIT": 0, "FULL_GATE_B": "OPEN", "TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "TEST_C1_LOCAL_NORMALIZATION_COMPLETE_SHELL_ENTRY_BOUNDARY",
    }


def write() -> None:
    p = payload()
    RESULT.write_bytes(canonical({"certificate_version": 1, "claim_status": STATUS,
                                  "payload": p,
                                  "payload_sha256": hashlib.sha256(canonical(p)).hexdigest()}))


def check_document(document: dict) -> None:
    need(type(document) is dict and set(document) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "claim status")
    need(document["payload_sha256"] == hashlib.sha256(canonical(document["payload"])).hexdigest(), "digest")
    need(canonical(document["payload"]) == canonical(payload()), "exact scale ladder")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write(); print("TPC405_CERTIFICATE=WRITTEN")
    elif args.check:
        check_document(json.loads(RESULT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants))
        print("TPC405_CERTIFICATE=PASS cases=20 heights=5 multiplicities=4 exact_bound=PASS")
    else:
        raise SystemExit("explicit --check or --write required")


if __name__ == "__main__":
    main()
