#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-337.

This checker does not import the TPC-337 producer.  It rebuilds the finite
source with trial factorisation, accumulates the prime shell in reverse order,
and recomputes the control-orbit covariance ledger.
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
RESULT = PROJECT / "results/tpc337_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-336-masked-signed-gram-response/code/"
PARENT_CODE = PARENT_CODE / "tpc336_masked_signed_gram_response.py"
PARENT_CERT = ROOT / "papers/tpc-336-masked-signed-gram-response/results/"
PARENT_CERT = PARENT_CERT / "tpc336_certificate.json"
PARENT_CODE_SHA256 = "0c2febd76d6bfdc5af4b58145739bcc04b435303f15c66b31e2d0b2e63497442"
PARENT_CERT_SHA256 = "926859be38cc601ef728363328899d4e9ab2001f77e7e1106ab028d64cf2814a"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
Q = 54
EXPONENT = 1
HEIGHT = 66
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0), ("affine_3_11", 3, 11),
    ("affine_5_17", 5, 17), ("affine_7_29", 7, 29),
    ("reversal", -1, -1),
)
SCHEMA = "TPC337_CONTROL_COVARIANCE_MASKED_RESPONSE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE"
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
    for number in range(2, limit + 1):
        if all(number % prime for prime in result if prime * prime <= number):
            result.append(number)
    return result


PRIMES = primes_trial(50_000)


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for prime in PRIMES:
        if prime * prime > number:
            break
        if number % prime == 0:
            return number == prime
    return True


def prime_power(number: int) -> tuple[int, int] | None:
    for prime in PRIMES:
        power, exponent = prime, 1
        while power < number:
            power *= prime
            exponent += 1
        if power == number:
            return prime, exponent
        if prime > number:
            break
    return None


def factors_reverse(number: int) -> list[int]:
    remaining = number
    factors: list[int] = []
    for prime in reversed(PRIMES):
        if prime * prime > remaining:
            continue
        if remaining % prime == 0:
            factors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 1:
        factors.append(remaining)
    return factors


TAIL: Fraction | None = None


def tail_upper() -> Fraction:
    global TAIL
    if TAIL is None:
        value = Decimal(1)
        for prime in reversed(PRIMES):
            if prime > 2:
                value *= Decimal((prime - 1) ** 2 - 1) / Decimal((prime - 1) ** 2)
        TAIL = Fraction(value)
    return TAIL


def source_arrays(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    upper = tail_upper()
    lower = upper * Fraction(49_998, 49_999)
    lambdas: list[float] = []
    comparisons: list[float] = []
    residuals: list[float] = []
    for value in range(lo, hi + 1):
        power = prime_power(value + 2)
        lam = Fraction(Decimal(power[0]).ln()) if power else Fraction(0)
        if value % 2 == 0:
            comparison = Fraction(0)
        else:
            local = Fraction(2)
            for prime in factors_reverse(value):
                if prime > 2:
                    local *= Fraction(prime - 1, prime - 2)
            comparison = (lower + upper) / 2 * local
        lambdas.append(float(lam))
        comparisons.append(float(comparison))
        residuals.append(float(lam - comparison))
    return (np.asarray(lambdas), np.asarray(comparisons),
            np.asarray(residuals))


def category(value: int, lam: float, comparison: float) -> str:
    if lam * comparison == 0.0:
        return "zero_support"
    power = prime_power(value + 2)
    need(power is not None, "support prime power")
    if power[1] == 1:
        return "twin_prime" if is_prime(value) else "non_twin_prime_shift"
    return "prime_power_shift"


def reverse_matrix(origin: int, scale: int) -> np.ndarray:
    values = np.arange(origin, origin + scale // 2, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    distance = difference.astype(np.float64)
    kernel = HEIGHT ** 2 / (HEIGHT ** 2 + distance * distance)
    matrix = np.zeros((len(values), len(values)), dtype=np.float64)
    shell = [prime for prime in PRIMES if Q < prime <= 2 * Q]
    for prime in reversed(shell):
        valid = ((difference != 0) & (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        matrix += float(prime) * kernel * centered * valid
    return (matrix + matrix.T) / 2.0


def control_indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        indices = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        indices = np.asarray([(multiplier * i + offset) % size
                              for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in indices)) == size, "control bijection")
    return indices


def recompute(origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comparison, residual = source_arrays(lo, hi)
    matrix = reverse_matrix(origin, scale)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for index, value in enumerate(range(lo, hi + 1)):
        masks[category(value, float(lam[index]), float(comparison[index]))][index] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs = np.zeros((len(CATEGORIES), len(CONTROLS), len(residual)))
    for control_index, (_, multiplier, offset) in enumerate(CONTROLS):
        indices = control_indices(len(residual), multiplier, offset)
        for category_index, name in enumerate(CATEGORIES):
            outputs[category_index, control_index] = matrix @ vectors[name][indices]
    means = outputs.mean(axis=1)
    centered = outputs - means[:, None, :]
    average = np.mean(np.sum(outputs * outputs, axis=2), axis=1)
    coherent = np.sum(means * means, axis=1)
    centered_energy = np.mean(np.sum(centered * centered, axis=2), axis=1)
    class_response: dict[str, Any] = {}
    for index, name in enumerate(CATEGORIES):
        class_response[name] = {
            "coordinate_count": int(masks[name].sum()),
            "source_l2": float(np.dot(vectors[name], vectors[name])),
            "average_energy": float(average[index]),
            "coherent_energy": float(coherent[index]),
            "centered_energy": float(centered_energy[index]),
            "coherent_fraction": float(coherent[index] / average[index]) if average[index] else 0.0,
            "centered_fraction": float(centered_energy[index] / average[index]) if average[index] else 0.0,
        }
    full = outputs.sum(axis=0)
    full_mean = means.sum(axis=0)
    full_centered = centered.sum(axis=0)
    full_average = float(np.mean(np.sum(full * full, axis=1)))
    full_coherent = float(np.dot(full_mean, full_mean))
    full_centered_energy = float(np.mean(np.sum(full_centered * full_centered, axis=1)))
    covariance = np.einsum("cjn,djn->cd", centered, centered) / len(CONTROLS)
    covariance = (covariance + covariance.T) / 2.0
    coherent_gram = means @ means.T
    average_gram = np.einsum("cjn,djn->cd", outputs, outputs) / len(CONTROLS)
    pair_covariance = {}
    for i, left in enumerate(CATEGORIES):
        for j in range(i + 1, len(CATEGORIES)):
            pair_covariance[left + "__" + CATEGORIES[j]] = float(covariance[i, j])
    return {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(residual),
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "class_response": class_response,
        "full_response": {
            "average_energy": full_average,
            "coherent_energy": full_coherent,
            "centered_energy": full_centered_energy,
            "coherent_fraction": full_coherent / full_average,
            "centered_fraction": full_centered_energy / full_average,
        },
        "average_gram": average_gram,
        "coherent_gram": coherent_gram,
        "covariance_gram": covariance,
        "covariance_eigenvalues": np.linalg.eigvalsh(covariance),
        "pair_covariance": pair_covariance,
    }


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 2.0e-7) -> None:
    expected = float(recorded)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual), abs(expected)),
         label)


def check_row(actual: dict[str, Any], recorded: dict[str, Any]) -> None:
    need(actual["origin"] == recorded["origin"] and
         actual["scale"] == recorded["scale"] and
         actual["source_interval"] == recorded["source_interval"] and
         actual["source_count"] == recorded["source_count"], "row geometry")
    need(actual["mask_counts"] == recorded["mask_counts"], "mask counts")
    for name, metrics in actual["class_response"].items():
        stored = recorded["class_response"][name]
        need(metrics["coordinate_count"] == stored["coordinate_count"],
             "class coordinate count")
        for field in ("source_l2", "average_energy", "coherent_energy",
                      "centered_energy", "coherent_fraction",
                      "centered_fraction"):
            close(metrics[field], stored[field], "class " + name + " " + field)
    for field in ("average_energy", "coherent_energy", "centered_energy",
                  "coherent_fraction", "centered_fraction"):
        close(actual["full_response"][field], recorded["full_response"][field],
              "full " + field)
    for matrix_name in ("average_gram", "coherent_gram", "covariance_gram"):
        matrix = actual[matrix_name]
        stored = recorded[matrix_name]
        for i in range(4):
            for j in range(4):
                close(float(matrix[i, j]), stored[i][j],
                      matrix_name + " entry")
    eigen = actual["covariance_eigenvalues"]
    for value, stored in zip(eigen, recorded["covariance_eigenvalues"]):
        close(float(value), stored, "covariance eigenvalue")
    for key, value in actual["pair_covariance"].items():
        close(value, recorded["pair_covariance"][key], "pair covariance " + key)
    need(float(min(eigen)) >= -1.0e-4, "covariance PSD guard")
    need(actual["full_response"]["centered_fraction"] > 0.75 and
         actual["full_response"]["coherent_fraction"] < 0.25,
         "finite covariance dominance")


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
             "parent producer hash")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
             "parent certificate hash")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("claim_status") == STATUS, "certificate status")
        payload = document["payload"]
        need(payload["schema"] == SCHEMA and
             document["payload_sha256"] == hashlib.sha256(
                 canonical(payload)).hexdigest(), "certificate digest")
        need(payload["finite_audit"] == {
            "rows": 6, "origins": 2, "scales": 3, "controls": 5,
            "categories": 4, "class_decomposition_observations": 24,
            "pair_covariance_observations": 36,
            "full_decomposition_observations": 6,
            "covariance_spectrum_observations": 6,
            "fixed_power_credit": 0, "arithmetic_advance": "NO"},
             "finite audit")
        for recorded in payload["rows"]:
            check_row(recompute(recorded["origin"], recorded["scale"]), recorded)
        summary = payload["summary"]
        need(float(summary["full_centered_fraction_min"]) > 0.75 and
             float(summary["full_coherent_fraction_max"]) < 0.25,
             "summary bounds")
        signs = summary["covariance_pair_signs"]
        need(signs["twin_prime__non_twin_prime_shift"]["positive"] == 6 and
             signs["twin_prime__zero_support"]["negative"] == 6 and
             signs["non_twin_prime_shift__zero_support"]["negative"] == 6,
             "summary signs")
        anchor = payload["exact_anchor"]
        need(anchor["identity_exact"] is True and anchor["average_cross"] == "0" and
             anchor["coherent_cross"] == "1/2" and
             anchor["centered_cross"] == "-1/2", "exact anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC337_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC337_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC337_SOURCE_UNIFORM_L2"] == "OPEN" and
             firewall["TPC337_FULL_GATE_B"] == "OPEN", "claim firewall")
        print("TPC337_INDEPENDENT_CHECK=PASS rows=6 controls=5 categories=4 "
              "reverse_shell=1 covariance_psd=1 sign_census=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC337_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
