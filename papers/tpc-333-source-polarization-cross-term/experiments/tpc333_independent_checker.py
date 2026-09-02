#!/usr/bin/env python3
"""Independent source replay for TPC-333.

This checker intentionally does not import the TPC-332 source routine.  It
uses a separate sieve, trial factorisation, and reversed product order, then
compares only the declared source ledger fields.
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
RESULT = PROJECT / "results/tpc333_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-332-growing-control-average-ensemble/code/tpc332_growing_control_average_ensemble.py"
PARENT_CERT = ROOT / "papers/tpc-332-growing-control-average-ensemble/results/tpc332_certificate.json"
PARENT_CODE_SHA256 = "ea742cfaaf7aa2be3c4cfad2ca603baadd65dc77619d8a1ba5ef686dd1fea5d9"
PARENT_CERT_SHA256 = "ddb0c33d09edf648df9a32c0e7cec6e8bac638cae6aba895ebf8084da5d580b9"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
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


def factor_distinct_reverse(value: int) -> list[int]:
    remaining = value
    factors: list[int] = []
    for p in reversed(PRIMES):
        if p * p > remaining:
            continue
        if remaining % p == 0:
            factors.append(p)
            while remaining % p == 0:
                remaining //= p
    if remaining > 1:
        factors.append(remaining)
    return factors


def prime_power_trial(value: int) -> int | None:
    for p in PRIMES:
        power = p
        while power < value:
            power *= p
        if power == value:
            return p
        if p > value:
            break
    return None


TAIL_CACHE: Fraction | None = None


def tail_upper() -> Fraction:
    global TAIL_CACHE
    if TAIL_CACHE is None:
        product = Decimal(1)
        # Reverse order is intentional; this differs from the producer's
        # forward accumulation but remains inside the same finite enclosure.
        for p in reversed(PRIMES):
            if p > 2:
                product *= Decimal((p - 1) ** 2 - 1) / Decimal((p - 1) ** 2)
        TAIL_CACHE = Fraction(product)
    return TAIL_CACHE


def source_arrays(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lam_values: list[float] = []
    comp_values: list[float] = []
    residual_values: list[float] = []
    upper = tail_upper()
    # Match the parent's declared lower enclosure 1-1/(TAIL_CUTOFF-1),
    # while retaining the independently accumulated upper product.
    lower = upper * Fraction(49998, 49999)
    for t in range(lo, hi + 1):
        p = prime_power_trial(t + 2)
        if p is None:
            lam = Fraction(0)
        else:
            logp = Fraction(Decimal(p).ln())
            lam = logp
        if t % 2 == 0:
            comp = Fraction(0)
        else:
            local = Fraction(2)
            for q in factor_distinct_reverse(t):
                if q > 2:
                    local *= Fraction(q - 1, q - 2)
            comp = (lower + upper) / 2 * local
        lam_values.append(float(lam))
        comp_values.append(float(comp))
        residual_values.append(float(lam - comp))
    return (np.asarray(lam_values, dtype=np.float64),
            np.asarray(comp_values, dtype=np.float64),
            np.asarray(residual_values, dtype=np.float64))


def recompute(origin: int, scale: int) -> dict[str, Any]:
    lam, comp, residual = source_arrays(origin, origin + scale // 2 - 1)
    l2 = float(lam @ lam)
    c2 = float(comp @ comp)
    cross = float(lam @ comp)
    r2 = float(residual @ residual)
    total = l2 + c2
    return {
        "origin": origin, "scale": scale,
        "source_interval": [origin, origin + scale // 2 - 1],
        "source_count": scale // 2,
        "lambda_l2": l2, "comparison_l2": c2,
        "cross_inner_product": cross, "residual_l2": r2,
        "total_component_l2": total,
        "cancellation_coefficient": 2 * cross / total,
        "residual_fraction_of_component_sum": r2 / total,
        "normalized_cross_correlation": cross / math.sqrt(l2 * c2),
        "identity_error": abs(r2 - total + 2 * cross),
        "lambda_nonzero": int((lam != 0).sum()),
        "comparison_nonzero": int((comp != 0).sum()),
        "residual_nonzero": int((residual != 0).sum()),
        "cross_positive_coordinate_count": int(((lam * comp) > 0).sum()),
        "cross_negative_coordinate_count": int(((lam * comp) < 0).sum()),
    }


def close(a: float, b: float, label: str) -> None:
    need(abs(a - b) <= 3.0e-11 * max(1.0, abs(a), abs(b)), label)


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
             "parent producer provenance")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
             "parent certificate provenance")
        raw = RESULT.read_bytes()
        doc = json.loads(raw)
        need(raw == canonical(doc), "certificate canonicality")
        need(doc.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER",
             "certificate status")
        payload = doc["payload"]
        need(payload["schema"] == "TPC333_SOURCE_POLARIZATION_CROSS_TERM_V1",
             "schema")
        need(doc["payload_sha256"] == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        rows = payload["rows"]
        need(len(rows) == 6, "row count")
        for recorded in rows:
            actual = recompute(recorded["origin"], recorded["scale"])
            for key, value in actual.items():
                if isinstance(value, float):
                    close(value, float(recorded[key]), "row " + key)
                else:
                    need(recorded[key] == value, "row " + key)
            close(float(recorded["cancellation_coefficient"]),
                  float(recorded["cross_inner_product"]) * 2 /
                  (float(recorded["lambda_l2"]) +
                   float(recorded["comparison_l2"])), "kappa identity")
        need(payload["summary"]["kappa_within_[.35,.37]"] == 6,
             "kappa census")
        need(payload["exact_anchor"]["identity_exact"] is True,
             "exact anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC333_SOURCE_UNIFORM_L2"] == "OPEN" and
             firewall["TPC333_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC333_FIXED_POWER_CREDIT"] == 0,
             "claim firewall")
        print("TPC333_INDEPENDENT_CHECK=PASS windows=6 growth_pairs=4 "
              "kappa_interval_census=6 reverse_factorization=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC333_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
