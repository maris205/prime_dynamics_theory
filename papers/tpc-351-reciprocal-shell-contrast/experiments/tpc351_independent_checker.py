#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-351.

The checker intentionally does not import the producer.  It rebuilds the
literal matrices in reverse shell order, recomputes all 192 reciprocal rows,
checks the parent comparison, growth series, and exact anchor.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-351-reciprocal-shell-contrast"
PRODUCER = PROJECT / "code/tpc351_reciprocal_shell_contrast.py"
RESULT = PROJECT / "results/tpc351_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-350-fresh-growth-signed-incidence/code/"
    "tpc350_fresh_growth_signed_incidence.py")
PARENT_CERT = ROOT / (
    "papers/tpc-350-fresh-growth-signed-incidence/results/"
    "tpc350_certificate.json")

PRODUCER_SHA256 = (
    "820f6195408a4d0fbbfed46f5bdd8054d812ae24eb87aaa1169791055f33328a")
PARENT_CODE_SHA256 = (
    "7819fb38be3f6d33688ca3a4caa1920da2dd8624805356411d8099fc069e185d")
PARENT_CERT_SHA256 = (
    "bc874009cfdd8fd7d6ea06d5d109a46d8bd9a732cd4933852f9176c5801bb086")
CERTIFICATE_SHA256 = (
    "74ca0045ca201712a69870669612b7bc16ccd0c019f27f3ea1d3dccb4b687db0")

SCHEMA = "TPC351_RECIPROCAL_SHELL_CONTRAST_V1"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_SCALE_REPAIR_AUDIT")
ORIGINS = (60097, 72097, 84097)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (36, 80, 128, 256)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index")
HEIGHT = 66
TOL = 8.0e-9


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def close(given: Any, value: float) -> bool:
    try:
        return abs(float(given) - float(value)) <= TOL * max(1.0, abs(value))
    except (TypeError, ValueError):
        return False


def locked(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def show(value: float) -> str:
    return format(float(value), ".12g")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(2 * max(Q_ANCHORS))


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def source_signs(primes: list[int], law: str) -> list[int]:
    need(law in LAW_NAMES, "unknown source law")
    if law == "all_plus":
        return [1] * len(primes)
    return [1 if index % 2 == 0 else -1
            for index in range(len(primes))]


def reciprocal_coefficients(primes: list[int]) -> list[Fraction]:
    reciprocals = [Fraction(1, prime) for prime in primes]
    mean = sum(reciprocals, Fraction(0)) / len(reciprocals)
    result = [value - mean for value in reciprocals]
    need(sum(result, Fraction(0)) == 0, "reciprocal coefficient balance")
    need(all(value != 0 for value in result),
         "reciprocal coefficients are nonzero")
    return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def spectral_norm(matrix: np.ndarray) -> float:
    eig = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    need(len(eig) > 0 and bool(np.all(np.isfinite(eig))), "finite spectrum")
    return max(abs(float(eig[0])), abs(float(eig[-1])))


def reverse_matrices(origin: int, count: int, q0: int, exponent: int,
                     law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                                         list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + differences.astype(np.float64) ** 2) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell_for(q0)
    for prime, sign in reversed(list(zip(primes, source_signs(primes, law)))):
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(sign * prime) * kernel * centered
        ideal += block
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        physical += block * valid
    physical = (physical + physical.T) / 2.0
    ideal = (ideal + ideal.T) / 2.0
    return physical, ideal, physical - ideal, primes


def incidence(values: np.ndarray, primes: list[int],
              coefficients: list[int]) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float64)
    for prime, coefficient in zip(primes, coefficients):
        if coefficient:
            result += coefficient * (values % prime == 0)
    return result


def fraction_matrix(origin: int, count: int, q0: int, exponent: int,
                    law: str, masked: bool) -> list[list[Fraction]]:
    values = list(range(origin, origin + count))
    result = [[Fraction(0) for _ in values] for _ in values]
    primes = shell_for(q0)
    for prime, sign in zip(primes, source_signs(primes, law)):
        for i, u in enumerate(values):
            for j, t in enumerate(values):
                if u == t:
                    continue
                if masked and (u % prime == 0 or t % prime == 0):
                    continue
                centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += sign * prime * kernel * centered
    return result


def vector_digest(vector: list[Fraction]) -> str:
    text = [f"{item.numerator}/{item.denominator}" for item in vector]
    return hashlib.sha256(canonical(text)).hexdigest()


def check_anchor(anchor: dict[str, Any]) -> None:
    origin, count, q0, exponent, law = 97, 14, 4, 1, "all_plus"
    actual = fraction_matrix(origin, count, q0, exponent, law, True)
    ideal = fraction_matrix(origin, count, q0, exponent, law, False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(count)]
              for i in range(count)]
    primes = shell_for(q0)
    coefficients = reciprocal_coefficients(primes)
    vector = [sum((coefficients[k]
                  for k, prime in enumerate(primes) if value % prime == 0)
                  , Fraction(0))
              for value in range(origin, origin + count)]
    image = [sum(defect[i][j] * vector[j] for j in range(count))
             for i in range(count)]
    square = sum(item * item for item in image)
    need(anchor.get("interval") == [97, 110] and
         anchor.get("shell") == [5, 7] and
         anchor.get("coefficients") == ["1/35", "-1/35"] and
         anchor.get("incidence_vector") ==
         ["0/1", "-1/35", "0/1", "1/35", "0/1", "0/1", "0/1",
          "0/1", "0/1", "0/1", "0/1", "0/1", "0/1", "1/35"] and
         anchor.get("incidence_vector_squared_norm") == "3/1225" and
         anchor.get("response_vector_squared_norm") ==
         f"{square.numerator}/{square.denominator}" and
         anchor.get("response_vector_digest") == vector_digest(image) and
         anchor.get("identity_exact") is True, "exact anchor")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        locked(PRODUCER, PRODUCER_SHA256, "producer")
        locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC350 producer")
        locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC350 certificate")
        parent_raw = PARENT_CERT.read_bytes()
        parent_document = json.loads(parent_raw)
        need(parent_raw == canonical(parent_document),
             "TPC350 certificate canonicality")
        need(parent_document.get("certificate_version") == 1 and
             parent_document.get("claim_status") ==
             "PROVED_EXACT_FINITE_SIGNED_INCIDENCE_LOWER_WITNESS_PLUS_"
             "NUMERICALLY_CERTIFIED_FRESH_GROWTH_AND_SCALE_AUDIT",
             "TPC350 certificate header")
        parent_rows = {(item["origin"], item["count"], item["q"],
                        item["kernel_exponent"], item["law"]): item
                       for item in parent_document["payload"]["rows"]}
        need(len(parent_rows) == 192, "TPC350 parent row census")
        locked(RESULT, CERTIFICATE_SHA256, "certificate")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
             "certificate schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        protocol = payload.get("protocol", {})
        need(protocol.get("origins") == list(ORIGINS) and
             protocol.get("source_counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("height") == HEIGHT and
             protocol.get("laws") == list(LAW_NAMES), "protocol")
        rows = payload.get("rows", [])
        need(len(rows) == 192, "row census")
        by_key = {(row["origin"], row["count"], row["q"],
                   row["kernel_exponent"], row["law"]): row for row in rows}
        need(len(by_key) == 192, "row keys")
        positive = beaten = half = improved = 0
        computed = []
        for origin in ORIGINS:
            for count in COUNTS:
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        for law in LAW_NAMES:
                            row = by_key[(origin, count, q0, exponent, law)]
                            _, ideal, defect, primes = reverse_matrices(
                                origin, count, q0, exponent, law)
                            values = np.arange(origin, origin + count,
                                               dtype=np.int64)
                            coefficients = reciprocal_coefficients(primes)
                            vector = incidence(
                                values, primes,
                                [float(item) for item in coefficients])
                            norm = float(np.linalg.norm(vector))
                            need(norm > 0.0, "zero signed vector")
                            unit = vector / norm
                            response = float(np.linalg.norm(defect @ unit))
                            defect_norm = spectral_norm(defect)
                            ideal_norm = spectral_norm(ideal)
                            hit = np.any(np.array([(values % prime) == 0
                                                   for prime in primes]), axis=0)
                            coordinate = float(np.linalg.norm(
                                defect[:, hit], axis=0).max())
                            gram = np.zeros(count, dtype=np.float64)
                            for prime, coefficient in zip(primes, coefficients):
                                if coefficient != 0:
                                    gram += float(coefficient) * (defect @
                                        (values % prime == 0).astype(float))
                            gram_error = float(np.max(np.abs(
                                defect @ unit - gram / norm)))
                            parent = parent_rows[(origin, count, q0,
                                                  exponent, law)]
                            parent_response = float(
                                parent["signed_witness_response_norm"])
                            response_gain = response / parent_response
                            need(row.get("reciprocal_coefficients") ==
                                 [fraction_text(item) for item in coefficients] and
                                 row.get("reciprocal_coefficient_sum") == "0/1" and
                                 row.get("reciprocal_active_prime_count") ==
                                 sum(value != 0 for value in coefficients) and
                                 row.get("reciprocal_incidence_support") ==
                                 int(np.count_nonzero(vector)) and
                                 close(row.get("reciprocal_incidence_norm"), norm) and
                                 close(row.get("reciprocal_witness_response_norm"), response) and
                                 close(row.get("reciprocal_to_defect_ratio"),
                                       response / defect_norm) and
                                 close(row.get("reciprocal_to_ideal_ratio"),
                                       response / ideal_norm) and
                                 close(row.get("reciprocal_to_coordinate_ratio"),
                                       response / coordinate) and
                                 row.get("parent_balanced_response_norm") ==
                                 parent["signed_witness_response_norm"] and
                                 row.get("parent_balanced_to_defect_ratio") ==
                                 parent["signed_to_defect_ratio"] and
                                 close(row.get("reciprocal_to_parent_response_ratio"),
                                       response_gain) and
                                 row.get("improves_parent_balanced") is
                                 (response_gain > 1.0 + 1.0e-10) and
                                 close(row.get("defect_operator_norm"), defect_norm) and
                                 close(row.get("ideal_operator_norm"), ideal_norm) and
                                 close(row.get("incidence_gram_max_error"),
                                       gram_error), "reverse row mismatch")
                            need(gram_error <= TOL and
                                 response <= defect_norm * (1.0 + TOL) and
                                 response > 0.0, "row witness bound")
                            positive += 1
                            if response_gain > 1.0 + 1.0e-10:
                                improved += 1
                            if response / coordinate > 1.0 + 1.0e-10:
                                beaten += 1
                            if response / defect_norm >= 0.5 - 1.0e-12:
                                half += 1
                            computed.append({
                                "origin": origin, "count": count, "q": q0,
                                "kernel_exponent": exponent, "law": law,
                                "ratio": response / defect_norm,
                                "support": int(np.count_nonzero(vector)),
                            })
        need(positive == 192 and beaten == 86 and half == 111 and
             improved == 180,
             "aggregate census")
        series = payload.get("growth_series", [])
        need(len(series) == 48, "growth series census")
        expected_series = {}
        for item in computed:
            key = (item["origin"], item["q"], item["kernel_exponent"],
                   item["law"])
            expected_series.setdefault(key, []).append(item)
        nondec = 0
        for item in series:
            key = (item.get("origin"), item.get("q"),
                   item.get("kernel_exponent"), item.get("law"))
            got = sorted(expected_series.get(key, []), key=lambda x: x["count"])
            ratios = [x["ratio"] for x in got]
            need(item.get("counts") == list(COUNTS) and
                 len(ratios) == 4 and
                 all(close(g, v) for g, v in zip(
                     item.get("reciprocal_to_defect_ratios", []), ratios)),
                 "growth series mismatch")
            monotone = all(ratios[i + 1] >= ratios[i] - 1.0e-12
                            for i in range(3))
            need(item.get("nondecreasing") is monotone, "series monotonicity")
            slope = math.log(ratios[-1] / ratios[0], 2.0) / 3.0
            need(close(item.get("endpoint_log2_slope"), slope),
                 "series slope")
            nondec += monotone
        need(nondec == 25, "monotonic series census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 192 and audit.get("series") == 48 and
             audit.get("positive_reciprocal_witness_rows") == 192 and
             audit.get("zero_sum_records") == 192 and
             audit.get("incidence_gram_records") == 192 and
             audit.get("improved_parent_rows") == 180 and
             audit.get("parent_comparison_records") == 192 and
             audit.get("coordinate_beaten_rows") == 86 and
             audit.get("half_defect_rows") == 111 and
             audit.get("min_reciprocal_support") == 24 and
             audit.get("max_reciprocal_support") == 339 and
             audit.get("nondecreasing_series") == 25 and
             audit.get("fixed_power_credit") == 0 and
             audit.get("arithmetic_advance") == "NO" and
             close(audit.get("min_reciprocal_to_defect_ratio"),
                   min(item["ratio"] for item in computed)) and
             close(audit.get("max_reciprocal_to_defect_ratio"),
                   max(item["ratio"] for item in computed)), "audit")
        check_anchor(payload.get("exact_anchor", {}))
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC351_UNIFORM_QUARTER_FLOOR") ==
             "REFUTED_SCOPED" and
             firewall.get("TPC351_PARENT_IMPROVEMENT_CENSUS") ==
             "NUMERICALLY_CERTIFIED_FINITE_180_OF_192" and
             firewall.get("TPC351_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC351_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC351_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC351_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
        print("TPC351_INDEPENDENT_CHECK=PASS rows=192 positive_witness=192 "
              "improved_parent=180/192 ratio_floor=0.0917557319271")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC351_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
