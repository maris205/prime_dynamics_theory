#!/usr/bin/env python3
"""Independent reverse-shell replay for the TPC-338 nested orbit test."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc338_certificate.json"
PARENT_CODE = ROOT / "papers/tpc-337-control-covariance-masked-response/code/"
PARENT_CODE = PARENT_CODE / "tpc337_control_covariance_masked_response.py"
PARENT_CERT = ROOT / "papers/tpc-337-control-covariance-masked-response/results/"
PARENT_CERT = PARENT_CERT / "tpc337_certificate.json"
PARENT_CODE_SHA256 = "e74d621fa48fe7c15ff4e520dc2a051e5b195a5045c706592f275a6ead6b384d"
PARENT_CERT_SHA256 = "558f9a2dc60cd6616230785b46934a415459211a2e1bc31083447c53dd40e1d2"
SCHEMA = "TPC338_GROWING_CONTROL_COVARIANCE_SPECTRUM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
Q = 54
HEIGHT = 66
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0), ("affine_3_11", 3, 11),
    ("affine_5_17", 5, 17), ("affine_7_29", 7, 29),
    ("reversal", -1, -1), ("affine_9_1", 9, 1),
    ("affine_11_13", 11, 13), ("affine_13_17", 13, 17),
    ("affine_17_19", 17, 19),
)
CONTROL_NAMES = tuple(item[0] for item in CONTROLS)
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
    result: list[int] = []
    for prime in reversed(PRIMES):
        if prime * prime > remaining:
            continue
        if remaining % prime == 0:
            result.append(prime)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 1:
        result.append(remaining)
    return result


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
    lam: list[float] = []
    comparison: list[float] = []
    residual: list[float] = []
    for value in range(lo, hi + 1):
        power = prime_power(value + 2)
        lv = Fraction(Decimal(power[0]).ln()) if power else Fraction(0)
        if value % 2 == 0:
            cv = Fraction(0)
        else:
            local = Fraction(2)
            for prime in factors_reverse(value):
                if prime > 2:
                    local *= Fraction(prime - 1, prime - 2)
            cv = (lower + upper) / 2 * local
        lam.append(float(lv)); comparison.append(float(cv))
        residual.append(float(lv - cv))
    return np.asarray(lam), np.asarray(comparison), np.asarray(residual)


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
    for prime in reversed([p for p in PRIMES if Q < p <= 2 * Q]):
        valid = ((difference != 0) & (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((difference % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        matrix += float(prime) * kernel * centered * valid
    return (matrix + matrix.T) / 2.0


def control_indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        result = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        result = np.asarray([(multiplier * i + offset) % size
                             for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in result)) == size, "control bijection")
    return result


def ensemble(outputs: np.ndarray, selected: Iterable[int]) -> dict[str, Any]:
    selected = list(selected)
    orbit = outputs[:, selected, :]
    means = orbit.mean(axis=1)
    centered = orbit - means[:, None, :]
    class_average = np.mean(np.sum(orbit * orbit, axis=2), axis=1)
    class_coherent = np.sum(means * means, axis=1)
    class_centered = np.mean(np.sum(centered * centered, axis=2), axis=1)
    classes = {}
    for i, name in enumerate(CATEGORIES):
        classes[name] = {
            "average_energy": float(class_average[i]),
            "coherent_energy": float(class_coherent[i]),
            "centered_energy": float(class_centered[i]),
            "coherent_fraction": float(class_coherent[i] / class_average[i]) if class_average[i] else 0.0,
            "centered_fraction": float(class_centered[i] / class_average[i]) if class_average[i] else 0.0,
        }
    full = orbit.sum(axis=0); full_mean = means.sum(axis=0)
    full_centered = centered.sum(axis=0)
    full_average = float(np.mean(np.sum(full * full, axis=1)))
    full_coherent = float(full_mean @ full_mean)
    full_centered_energy = float(np.mean(np.sum(full_centered * full_centered, axis=1)))
    covariance = np.einsum("cjn,djn->cd", centered, centered) / len(selected)
    covariance = (covariance + covariance.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(covariance)
    trace = float(np.trace(covariance))
    normalized = eigenvalues / trace if trace else eigenvalues
    pairs = {}
    for i, left in enumerate(CATEGORIES):
        for j in range(i + 1, len(CATEGORIES)):
            pairs[left + "__" + CATEGORIES[j]] = float(covariance[i, j])
    return {"class_response": classes,
            "full_response": {"average_energy": full_average,
                               "coherent_energy": full_coherent,
                               "centered_energy": full_centered_energy,
                               "coherent_fraction": full_coherent / full_average,
                               "centered_fraction": full_centered_energy / full_average},
            "covariance_gram": covariance,
            "covariance_eigenvalues": eigenvalues,
            "normalized_covariance_eigenvalues": normalized,
            "pair_covariance": pairs}


def recompute(origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    lam, comparison, residual = source_arrays(lo, hi)
    matrix = reverse_matrix(origin, scale)
    masks = {name: np.zeros(len(residual), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[category(value, float(lam[i]), float(comparison[i]))][i] = True
    vectors = {name: residual * masks[name] for name in CATEGORIES}
    outputs = np.zeros((4, len(CONTROLS), len(residual)))
    for j, (_, multiplier, offset) in enumerate(CONTROLS):
        permutation = control_indices(len(residual), multiplier, offset)
        for i, name in enumerate(CATEGORIES):
            outputs[i, j] = matrix @ vectors[name][permutation]
    five = ensemble(outputs, range(5)); nine = ensemble(outputs, range(9))
    e5 = five["normalized_covariance_eigenvalues"]
    e9 = nine["normalized_covariance_eigenvalues"]
    k5 = five["covariance_gram"]; k9 = nine["covariance_gram"]
    return {"origin": origin, "scale": scale,
            "source_interval": [lo, hi], "source_count": len(residual),
            "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
            "five_control": five, "nine_control": nine,
            "normalized_spectrum_l1_distance": float(np.sum(np.abs(e5 - e9))),
            "covariance_relative_frobenius_change": float(
                np.linalg.norm(k9 - k5) / np.linalg.norm(k5))}


def close(actual: float, stored: Any, label: str,
          tolerance: float = 3.0e-7) -> None:
    expected = float(stored)
    need(math.isfinite(actual) and math.isfinite(expected) and
         abs(actual - expected) <= tolerance * max(1.0, abs(actual), abs(expected)),
         label)


def check_ensemble(actual: dict[str, Any], stored: dict[str, Any], label: str) -> None:
    need(actual["class_response"].keys() == stored["class_response"].keys(),
         label + " classes")
    for name, metrics in actual["class_response"].items():
        for field, value in metrics.items():
            close(value, stored["class_response"][name][field],
                  label + " class " + name + " " + field)
    for field, value in actual["full_response"].items():
        close(value, stored["full_response"][field], label + " full " + field)
    for i in range(4):
        for j in range(4):
            close(float(actual["covariance_gram"][i, j]),
                  stored["covariance_gram"][i][j], label + " covariance")
    for value, saved in zip(actual["covariance_eigenvalues"],
                            stored["covariance_eigenvalues"]):
        close(float(value), saved, label + " eigenvalue")
    for value, saved in zip(actual["normalized_covariance_eigenvalues"],
                            stored["normalized_covariance_eigenvalues"]):
        close(float(value), saved, label + " normalized eigenvalue")
    for key, value in actual["pair_covariance"].items():
        close(value, stored["pair_covariance"][key], label + " pair " + key)
    need(float(actual["full_response"]["centered_fraction"]) > 0.75,
         label + " centered guard")


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256, "parent code")
        need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent cert")
        raw = RESULT.read_bytes(); document = json.loads(raw)
        need(raw == canonical(document), "canonicality")
        need(document.get("claim_status") == STATUS, "status")
        payload = document["payload"]
        need(payload["schema"] == SCHEMA and
             document["payload_sha256"] == hashlib.sha256(
                 canonical(payload)).hexdigest(), "digest")
        need(payload["finite_audit"] == {
            "rows": 6, "origins": 2, "scales": 3, "five_controls": 5,
            "nine_controls": 9, "categories": 4, "nested_decompositions": 48,
            "normalized_spectrum_comparisons": 6, "pair_sign_ensembles": 2,
            "fixed_power_credit": 0, "arithmetic_advance": "NO"}, "audit")
        for saved in payload["rows"]:
            actual = recompute(saved["origin"], saved["scale"])
            need(actual["source_interval"] == saved["source_interval"] and
                 actual["source_count"] == saved["source_count"] and
                 actual["mask_counts"] == saved["mask_counts"], "geometry")
            check_ensemble(actual["five_control"], saved["five_control"], "five")
            check_ensemble(actual["nine_control"], saved["nine_control"], "nine")
            close(actual["normalized_spectrum_l1_distance"],
                  saved["normalized_spectrum_l1_distance"], "spectrum distance")
            close(actual["covariance_relative_frobenius_change"],
                  saved["covariance_relative_frobenius_change"], "matrix change")
            need(float(saved["five_control"]["pair_covariance"][
                "twin_prime__zero_support"]) < 0 and
                 float(saved["nine_control"]["pair_covariance"][
                     "twin_prime__zero_support"]) > 0, "nested sign reversal")
        summary = payload["summary"]
        need(float(summary["nine_centered_fraction_min"]) > 0.85 and
             float(summary["nine_coherent_fraction_max"]) < 0.15 and
             summary["twin_zero_sign_reversal"] is True, "summary")
        signs = summary["sign_census"]
        need(signs["five_control"]["twin_prime__zero_support"]["negative"] == 6 and
             signs["nine_control"]["twin_prime__zero_support"]["positive"] == 6,
             "sign census")
        need(payload["exact_anchor"]["identity_exact"] is True, "anchor")
        firewall = payload["claim_firewall"]
        need(firewall["TPC338_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC338_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC338_FULL_GATE_B"] == "OPEN", "firewall")
        print("TPC338_INDEPENDENT_CHECK=PASS rows=6 five_controls=5 nine_controls=9 "
              "energy_dominance=6 twin_zero_reversal=6 reverse_shell=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC338_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
