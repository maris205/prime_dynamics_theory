#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-336."""

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
RESULT = PROJECT / "results/tpc336_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py"
PARENT_CERT = ROOT / "papers/tpc-335-twin-isolated-source-norm/results/tpc335_certificate.json"
PARENT_CODE_SHA256 = "e6d66a3963f974c9d3f03b20441b327a34dd9e684fabb72e0777d31082c4e608"
PARENT_CERT_SHA256 = "cee2aee00208cbfe8331abc80e066c7a736824414f4d8208a73e4c545bfa4934"
ORIGINS = (42001, 44001); SCALES = (2048, 4096, 8192)
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")
getcontext().prec = 100


class Failure(RuntimeError): pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition: raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def primes_trial(limit: int) -> list[int]:
    ps: list[int] = []
    for n in range(2, limit + 1):
        if all(n % p for p in ps if p * p <= n): ps.append(n)
    return ps


PRIMES = primes_trial(50000)


def is_prime(n: int) -> bool:
    if n < 2: return False
    for p in PRIMES:
        if p * p > n: break
        if n % p == 0: return n == p
    return True


def prime_power(n: int) -> tuple[int, int] | None:
    for p in PRIMES:
        power, k = p, 1
        while power < n: power *= p; k += 1
        if power == n: return p, k
        if p > n: break
    return None


def factors_reverse(n: int) -> list[int]:
    remaining = n; result: list[int] = []
    for p in reversed(PRIMES):
        if p * p > remaining: continue
        if remaining % p == 0:
            result.append(p)
            while remaining % p == 0: remaining //= p
    if remaining > 1: result.append(remaining)
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
        if t % 2 == 0: cv = Fraction(0)
        else:
            local = Fraction(2)
            for p in factors_reverse(t):
                if p > 2: local *= Fraction(p - 1, p - 2)
            cv = (lower + upper) / 2 * local
        lam.append(float(lv)); comp.append(float(cv)); beta.append(float(lv - cv))
    return np.asarray(lam), np.asarray(comp), np.asarray(beta)


def category(t: int, lam: float, comp: float) -> str:
    if lam * comp == 0.0: return "zero_support"
    pp = prime_power(t + 2); need(pp is not None, "prime-power support")
    if pp[1] == 1: return "twin_prime" if is_prime(t) else "non_twin_prime_shift"
    return "prime_power_shift"


def reverse_matrix(origin: int, scale: int) -> np.ndarray:
    values = np.arange(origin, origin + scale // 2, dtype=np.int64)
    delta = values[:, None] - values[None, :]
    kernel = 66.0 ** 2 / (66.0 ** 2 + delta.astype(np.float64) ** 2)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    shell = [p for p in PRIMES if 54 < p <= 108]
    for p in reversed(shell):
        valid = ((delta != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = (delta % p == 0).astype(np.float64) - 1.0 / (p - 1)
        matrix += float(p) * kernel * centered * valid
    return (matrix + matrix.T) / 2.0


def recompute(origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comp, beta = source_arrays(lo, hi); matrix = reverse_matrix(origin, scale)
    masks = {c: np.zeros(len(beta), dtype=bool) for c in CATEGORIES}
    for i, t in enumerate(range(lo, hi + 1)):
        masks[category(t, float(lam[i]), float(comp[i]))][i] = True
    vectors = {c: beta * masks[c] for c in CATEGORIES}
    outputs = {c: matrix @ vectors[c] for c in CATEGORIES}
    col = np.sum(matrix * matrix, axis=0, dtype=np.float64)
    metrics = {}
    for c in CATEGORIES:
        source_l2 = float(vectors[c] @ vectors[c]); energy = float(outputs[c] @ outputs[c])
        diagonal = float(np.sum(col * vectors[c] * vectors[c]))
        metrics[c] = {"coordinate_count": int(masks[c].sum()),
                      "source_l2": source_l2, "response_energy": energy,
                      "coordinate_diagonal": diagonal,
                      "off_diagonal": energy - diagonal,
                      "response_gain": energy / source_l2 if source_l2 else 0.0}
    pairwise = {}
    for i, left in enumerate(CATEGORIES):
        for right in CATEGORIES[i:]:
            pairwise[left + "__" + right] = float(outputs[left] @ outputs[right])
    full = matrix @ beta; full_energy = float(full @ full)
    self_sum = sum(metrics[c]["response_energy"] for c in CATEGORIES)
    pair_twice = 2 * sum(pairwise[left + "__" + right]
                         for i, left in enumerate(CATEGORIES)
                         for right in CATEGORIES[i + 1:])
    ordering = sorted(CATEGORIES, key=lambda c: (-metrics[c]["response_gain"], c))
    return {"origin": origin, "scale": scale, "source_interval": [lo, hi],
            "source_count": scale // 2,
            "operator": {"law": "all_plus", "Q": 54, "kernel_exponent": 1,
                         "height": 66},
            "self_metrics": metrics, "output_pairwise_gram": pairwise,
            "full_source_l2": float(beta @ beta),
            "full_response_energy": full_energy,
            "full_response_gain": full_energy / float(beta @ beta),
            "self_response_energy_sum": self_sum,
            "twice_pair_interaction_sum": pair_twice,
            "response_identity_error": abs(full_energy - self_sum - pair_twice),
            "self_to_full_energy_ratio": self_sum / full_energy,
            "destructive_interaction": full_energy < self_sum,
            "response_gain_order": ordering}


def close(a: float, b: float, label: str) -> None:
    need(abs(a - b) <= 8.0e-9 * max(1.0, abs(a), abs(b)), label)


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256, "parent code")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent cert")
        raw = RESULT.read_bytes(); document = json.loads(raw)
        need(raw == canonical(document), "canonicality")
        need(document.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE", "status")
        payload = document["payload"]
        need(payload["schema"] == "TPC336_MASKED_SIGNED_GRAM_RESPONSE_V1", "schema")
        need(document["payload_sha256"] == hashlib.sha256(
            canonical(payload)).hexdigest(), "digest")
        for recorded in payload["rows"]:
            actual = recompute(recorded["origin"], recorded["scale"])
            for key, value in actual.items():
                if isinstance(value, dict):
                    if key == "self_metrics":
                        for c in CATEGORIES:
                            for field, item in value[c].items():
                                if isinstance(item, float):
                                    close(item, float(recorded[key][c][field]),
                                          "metric " + c + " " + field)
                                else: need(item == recorded[key][c][field], "metric field")
                    else:
                        for field, item in value.items():
                            if isinstance(item, float):
                                close(item, float(recorded[key][field]), "dict " + field)
                            else: need(item == recorded[key][field], "dict field")
                elif isinstance(value, float):
                    if key == "response_identity_error":
                        need(value < 5.0e-6 and float(recorded[key]) < 5.0e-6,
                             "row response identity guard")
                    else:
                        close(value, float(recorded[key]), "row " + key)
                else: need(value == recorded[key], "row field " + key)
            need(actual["response_gain_order"] == ["zero_support",
                 "non_twin_prime_shift", "twin_prime", "prime_power_shift"],
                 "gain ordering")
        need(payload["summary"]["destructive_interaction_rows"] == 6, "summary")
        need(payload["exact_anchor"]["identity_exact"] is True, "anchor")
        fw = payload["claim_firewall"]
        need(fw["TPC336_ARITHMETIC_ADVANCE"] == "NO" and
             fw["TPC336_FIXED_POWER_CREDIT"] == 0 and
             fw["TPC336_SOURCE_UNIFORM_L2"] == "OPEN", "firewall")
        print("TPC336_INDEPENDENT_CHECK=PASS rows=6 categories=4 "
              "gain_ordering=6 destructive_interaction=6 reverse_shell=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC336_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__": raise SystemExit(main())
