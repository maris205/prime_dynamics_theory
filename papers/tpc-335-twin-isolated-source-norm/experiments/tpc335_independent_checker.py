#!/usr/bin/env python3
"""Independent coordinate-mask and norm replay for TPC-335."""

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
RESULT = PROJECT / "results/tpc335_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-334-cross-term-support-ledger/code/tpc334_cross_term_support_ledger.py"
PARENT_CERT = ROOT / "papers/tpc-334-cross-term-support-ledger/results/tpc334_certificate.json"
PARENT_CODE_SHA256 = "a7e6d5f77b17449eea11d8b673e0d7bfa1701bc3f0f92601cc86d4891f3beef8"
PARENT_CERT_SHA256 = "9e9639965d70b0d66b2d63d2dbe30cad7007db00ec77d8fc54dce5baca03b7c6"
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
    result: list[int] = []
    for candidate in range(2, limit + 1):
        if all(candidate % p for p in result if p * p <= candidate):
            result.append(candidate)
    return result


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


def factors_reverse(value: int) -> list[int]:
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


def source_arrays(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    upper = tail_upper(); lower = upper * Fraction(49998, 49999)
    lam: list[float] = []; comp: list[float] = []; beta: list[float] = []
    for t in range(lo, hi + 1):
        pp = prime_power(t + 2)
        lv = Fraction(Decimal(pp[0]).ln()) if pp else Fraction(0)
        if t % 2 == 0:
            cv = Fraction(0)
        else:
            local = Fraction(2)
            for p in factors_reverse(t):
                if p > 2:
                    local *= Fraction(p - 1, p - 2)
            cv = (lower + upper) / 2 * local
        lam.append(float(lv)); comp.append(float(cv)); beta.append(float(lv - cv))
    return np.asarray(lam), np.asarray(comp), np.asarray(beta)


def category(t: int, lam: float, comp: float) -> str:
    if lam * comp == 0.0:
        return "zero_support"
    pp = prime_power(t + 2)
    need(pp is not None, "support prime power")
    if pp[1] == 1:
        return "twin_prime" if is_prime(t) else "non_twin_prime_shift"
    return "prime_power_shift"


def recompute(origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comp, beta = source_arrays(lo, hi)
    norm = {c: 0.0 for c in CATEGORIES}; cross = {c: 0.0 for c in CATEGORIES}
    count = {c: 0 for c in CATEGORIES}
    for i, t in enumerate(range(lo, hi + 1)):
        c = category(t, float(lam[i]), float(comp[i])); count[c] += 1
        norm[c] += float(beta[i] * beta[i]); cross[c] += float(lam[i] * comp[i])
    full = float(beta @ beta); total_cross = float(lam @ comp)
    support = {c: {"coordinate_count": count[c],
                   "residual_squared_norm": norm[c],
                   "residual_norm_fraction": norm[c] / full,
                   "cross_mass": cross[c],
                   "cross_mass_fraction": cross[c] / total_cross}
               for c in CATEGORIES}
    twin_norm = norm["twin_prime"] / full
    twin_cross = cross["twin_prime"] / total_cross
    return {"origin": origin, "scale": scale, "source_interval": [lo, hi],
            "source_count": scale // 2, "support": support,
            "full_residual_l2": full, "lambda_l2": float(lam @ lam),
            "comparison_l2": float(comp @ comp),
            "cross_inner_product": total_cross,
            "norm_partition_error": abs(sum(norm.values()) - full),
            "cross_partition_error": abs(sum(cross.values()) - total_cross),
            "twin_residual_norm_fraction": twin_norm,
            "twin_cross_mass_fraction": twin_cross,
            "twin_norm_to_cross_amplification": twin_norm / twin_cross}


def close(a: float, b: float, label: str) -> None:
    need(abs(a - b) <= 4.0e-11 * max(1.0, abs(a), abs(b)), label)


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256, "parent code")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent cert")
        raw = RESULT.read_bytes(); document = json.loads(raw)
        need(raw == canonical(document), "canonicality")
        need(document.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM", "status")
        payload = document["payload"]
        need(payload["schema"] == "TPC335_TWIN_ISOLATED_SOURCE_NORM_V1", "schema")
        need(document["payload_sha256"] == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        need(len(payload["rows"]) == 6, "rows")
        for recorded in payload["rows"]:
            actual = recompute(recorded["origin"], recorded["scale"])
            for key, value in actual.items():
                if isinstance(value, dict):
                    for c in CATEGORIES:
                        for field, item in value[c].items():
                            close(float(item), float(recorded[key][c][field]),
                                  "support " + c + " " + field)
                elif isinstance(value, float):
                    close(value, float(recorded[key]), "row " + key)
                else:
                    need(recorded[key] == value, "row " + key)
        summary = payload["summary"]
        need(summary["twin_norm_fraction_between_0.09_0.13"] == 6 and
             summary["background_norm_fraction_between_0.65_0.72"] == 6,
             "summary census")
        need(payload["exact_anchor"]["partition_exact"] is True, "anchor")
        fw = payload["claim_firewall"]
        need(fw["TPC335_ARITHMETIC_ADVANCE"] == "NO" and
             fw["TPC335_SOURCE_UNIFORM_L2"] == "OPEN" and
             fw["TPC335_FIXED_POWER_CREDIT"] == 0, "firewall")
        print("TPC335_INDEPENDENT_CHECK=PASS windows=6 categories=4 "
              "twin_norm_9_to_13pct=6 background_norm_65_to_72pct=6 "
              "reverse_factorization=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC335_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
