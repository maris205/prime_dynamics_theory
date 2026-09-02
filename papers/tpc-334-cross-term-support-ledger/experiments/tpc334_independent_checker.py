#!/usr/bin/env python3
"""Independent support replay for TPC-334.

The source values and support labels are rebuilt without importing either the
TPC-334 producer or the TPC-333 implementation.  Prime testing uses a trial
sieve and the tail product is accumulated in reverse order.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc334_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py"
PARENT_CERT = ROOT / "papers/tpc-333-source-polarization-cross-term/results/tpc333_certificate.json"
PARENT_CODE_SHA256 = "1e8b104db281b6998875f2fb5b4691910c3a22ef365c796bdc879f396f8a6bde"
PARENT_CERT_SHA256 = "3722702ab29b397c836b5ceb4cddd0b063d35e10139952dd93eb849ced2f53eb"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")
getcontext().prec = 100


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def primes_trial(limit: int) -> list[int]:
    primes: list[int] = []
    for candidate in range(2, limit + 1):
        if all(candidate % p for p in primes if p * p <= candidate):
            primes.append(candidate)
    return primes


PRIMES = primes_trial(50000)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for p in PRIMES:
        if p * p > value:
            break
        if value % p == 0:
            return value == p
    return True


def prime_power(value: int) -> tuple[int, int] | None:
    for p in PRIMES:
        power, exponent = p, 1
        while power < value:
            power *= p
            exponent += 1
        if power == value:
            return p, exponent
        if p > value:
            break
    return None


def factors(value: int) -> list[int]:
    remaining = value
    result: list[int] = []
    for p in reversed(PRIMES):
        if p * p > remaining:
            continue
        if remaining % p == 0:
            result.append(p)
            while remaining % p == 0:
                remaining //= p
    if remaining > 1:
        result.append(remaining)
    return result


TAIL: Fraction | None = None


def tail_upper() -> Fraction:
    global TAIL
    if TAIL is None:
        value = Decimal(1)
        for p in reversed(PRIMES):
            if p > 2:
                value *= Decimal((p - 1) ** 2 - 1) / Decimal((p - 1) ** 2)
        TAIL = Fraction(value)
    return TAIL


def arrays(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    upper = tail_upper()
    lower = upper * Fraction(49998, 49999)
    lam: list[float] = []
    comp: list[float] = []
    residual: list[float] = []
    for t in range(lo, hi + 1):
        pp = prime_power(t + 2)
        lambda_value = Fraction(Decimal(pp[0]).ln()) if pp else Fraction(0)
        if t % 2 == 0:
            comparison_value = Fraction(0)
        else:
            local = Fraction(2)
            for p in factors(t):
                if p > 2:
                    local *= Fraction(p - 1, p - 2)
            comparison_value = (lower + upper) / 2 * local
        lam.append(float(lambda_value))
        comp.append(float(comparison_value))
        residual.append(float(lambda_value - comparison_value))
    return (np.asarray(lam), np.asarray(comp), np.asarray(residual))


def category(t: int, lam: float, comp: float) -> str:
    if lam * comp == 0.0:
        return "zero_support"
    shifted = prime_power(t + 2)
    need(shifted is not None, "nonzero support is not a prime power")
    if shifted[1] == 1:
        return "twin_prime" if is_prime(t) else "non_twin_prime_shift"
    return "prime_power_shift"


def recompute(origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comp, residual = arrays(lo, hi)
    mass = {c: 0.0 for c in CATEGORIES}
    count = {c: 0 for c in CATEGORIES}
    for i, t in enumerate(range(lo, hi + 1)):
        c = category(t, float(lam[i]), float(comp[i]))
        count[c] += 1
        mass[c] += float(lam[i] * comp[i])
    cross = float(lam @ comp)
    support = {c: {"coordinate_count": count[c],
                   "cross_mass": mass[c],
                   "cross_mass_fraction": mass[c] / cross}
               for c in CATEGORIES}
    l2, c2, r2 = float(lam @ lam), float(comp @ comp), float(residual @ residual)
    return {
        "origin": origin, "scale": scale, "source_interval": [lo, hi],
        "source_count": scale // 2, "support": support,
        "total_cross_inner_product": cross,
        "cross_mass_partition_error": abs(sum(mass.values()) - cross),
        "twin_cross_mass_fraction": mass["twin_prime"] / cross,
        "non_twin_prime_shift_fraction": mass["non_twin_prime_shift"] / cross,
        "prime_power_shift_fraction": mass["prime_power_shift"] / cross,
        "lambda_l2": l2, "comparison_l2": c2, "residual_l2": r2,
    }


def close(a: float, b: float, label: str) -> None:
    need(abs(a - b) <= 4.0e-11 * max(1.0, abs(a), abs(b)), label)


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
             "parent producer provenance")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
             "parent certificate provenance")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER",
             "status")
        payload = document["payload"]
        need(payload["schema"] == "TPC334_CROSS_TERM_SUPPORT_LEDGER_V1",
             "schema")
        need(document["payload_sha256"] == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        need(len(payload["rows"]) == 6, "row count")
        for recorded in payload["rows"]:
            actual = recompute(recorded["origin"], recorded["scale"])
            for key, value in actual.items():
                if isinstance(value, float):
                    close(value, float(recorded[key]), "row " + key)
                elif isinstance(value, dict):
                    for cat in CATEGORIES:
                        for field, item in value[cat].items():
                            close(float(item), float(recorded[key][cat][field]),
                                  "support " + cat + " " + field)
                else:
                    need(recorded[key] == value, "row field " + key)
        summary = payload["summary"]
        need(summary["twin_fraction_below_0.10"] == 6 and
             summary["non_twin_fraction_above_0.90"] == 6,
             "support summary")
        need(payload["exact_anchor"]["partition_exact"] is True,
             "exact support anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC334_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC334_SOURCE_UNIFORM_L2"] == "OPEN" and
             firewall["TPC334_FIXED_POWER_CREDIT"] == 0,
             "firewall")
        print("TPC334_INDEPENDENT_CHECK=PASS windows=6 categories=4 "
              "twin_below_10pct=6 non_twin_above_90pct=6 reverse_support=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC334_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
