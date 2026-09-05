#!/usr/bin/env python3
"""Independent reverse-order CRT and coefficient replay for TPC-403."""
from __future__ import annotations
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-403-c1-crt-origin-proxy-obstruction/results/tpc403_certificate.json"
STATUS = "PROVED_EXACT_FINITE_CRT_PROXY_OBSTRUCTION"
Q, N, H, B = 8192, 1024, 66, 1_000_000


class Failure(ValueError):
    pass


def need(c: bool, message: str) -> None:
    if type(c) is not bool or not c:
        raise Failure(message)


def canonical(v: object) -> bytes:
    return (json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise Failure("duplicate key")
        d[k] = v
    return d


def no_constants(v):
    raise Failure("non-finite constant")


def primes(limit: int) -> list[int]:
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p : limit + 1 : p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def crt_reverse(residues: list[int], moduli: list[int]) -> tuple[int, int]:
    period = math.prod(moduli)
    total = 0
    for residue, modulus in reversed(tuple(zip(residues, moduli))):
        q = period // modulus
        total += residue * q * pow(q, -1, modulus)
    return total % period, period


def text_fraction(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def replay() -> list[dict]:
    shell = [p for p in primes(2 * Q) if p > Q]
    need(len(shell) == 872, "shell")
    result = []
    for m in range(1, 5):
        selected = shell[: 2 * m]
        residues = [0 if i % 2 == 0 else -N for i in range(2 * m)]
        residue, period = crt_reverse(residues, selected)
        origin = residue + ((B - residue) // period + 1) * period
        weights = [Fraction(p**3, Q**2 * (p - 1)) for p in selected]
        signed = [w if i % 2 == 0 else -w for i, w in enumerate(weights)]
        A = sum(signed, Fraction(0))
        pminus = sum(weights[1::2], Fraction(0))
        t1 = Fraction(H * H, H * H + 1)
        direct = Fraction(0)
        for p, coefficient in reversed(tuple(zip(selected, signed))):
            if origin % p and (origin + 1) % p:
                direct -= coefficient * t1
        bu = sum((coefficient for p, coefficient in zip(selected, signed) if origin % p == 0), Fraction(0))
        bv = sum((coefficient for p, coefficient in zip(selected, signed) if (origin + 1) % p == 0), Fraction(0))
        reduced = t1 * (-A + bu + bv)
        need(origin > B and direct == reduced == t1 * pminus, "coefficient replay")
        need(all(origin % p == 0 for p in selected[::2]), "positive mask")
        need(all(origin % p != 0 and (origin + 1) % p != 0 for p in selected[1::2]), "negative mask")
        result.append({
            "m": m, "selected_primes": selected, "residues": residues,
            "crt_residue": residue, "crt_period": period, "origin": origin,
            "origin_lower_bound": B, "window_pair": [origin, origin + 1],
            "positive_prime_hits_offset": [0], "negative_prime_hits_offset": [N],
            "A_sigma": text_fraction(A), "P_minus": text_fraction(pminus),
            "T1": text_fraction(t1), "direct": text_fraction(direct),
            "reduced": text_fraction(reduced),
            "raw_ratio_to_abs_A": text_fraction(t1 * pminus / abs(A)),
            "exact_identity": True,
        })
    return result


def main() -> None:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    d = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants)
    need(d["claim_status"] == STATUS and d["certificate_version"] == 1, "header")
    need(d["payload_sha256"] == hashlib.sha256(canonical(d["payload"])).hexdigest(), "digest")
    p = d["payload"]
    need(p["cases"] == replay(), "certificate differs from reverse CRT replay")
    need(p["negative_congruence"] == "o = -N (mod p_i) for odd i", "corrected congruence")
    print("TPC403_INDEPENDENT_CHECK=PASS cases=4 max_m=4 reverse_crt=PASS signed_obstruction=PASS")


if __name__ == "__main__":
    main()
