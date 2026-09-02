#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-352.

This file deliberately does not import the producer.  It rebuilds the new
holdout in reverse shell order and checks the frozen certificate contract.
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
PROJECT = ROOT / "papers/tpc-352-reciprocal-shell-adversarial-holdout"
PRODUCER = PROJECT / "code/tpc352_reciprocal_shell_adversarial_holdout.py"
RESULT = PROJECT / "results/tpc352_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-351-reciprocal-shell-contrast/code/"
    "tpc351_reciprocal_shell_contrast.py")
PARENT_CERT = ROOT / (
    "papers/tpc-351-reciprocal-shell-contrast/results/"
    "tpc351_certificate.json")

PRODUCER_SHA256 = "5fc838faef2832b1d8a2aac1613b94506ff0b08fd4c905820a6194f23ebe0cbe"
PARENT_CODE_SHA256 = (
    "820f6195408a4d0fbbfed46f5bdd8054d812ae24eb87aaa1169791055f33328a")
PARENT_CERT_SHA256 = (
    "74ca0045ca201712a69870669612b7bc16ccd0c019f27f3ea1d3dccb4b687db0")
CERTIFICATE_SHA256 = "e4219b0efaf22c7cbe818341a8240f07fc8252550e8c4d1b02ef5dea3419a888"

SCHEMA = "TPC352_RECIPROCAL_ADVERSARIAL_HOLDOUT_V1"
STATUS = (
    "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
    "NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT")
ORIGINS = (96097, 120097, 144097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (64, 128, 256, 512)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index")
HEIGHT = 66
TOL = 1.0e-8


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


def locked(path: Path, expected: str, label: str) -> None:
    need(expected != "TO_BE_FILLED", label + " hash placeholder")
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " provenance")


def close(given: Any, value: float) -> bool:
    try:
        return abs(float(given) - value) <= TOL * max(1.0, abs(value))
    except (TypeError, ValueError):
        return False


def show(value: float) -> str:
    return format(float(value), ".12g")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [x for x in range(2, limit + 1) if sieve[x]]


PRIMES = primes_up_to(2 * max(Q_ANCHORS))


def shell_for(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def source_signs(primes: list[int], law: str) -> list[int]:
    need(law in LAW_NAMES, "law")
    return ([1] * len(primes) if law == "all_plus" else
            [1 if i % 2 == 0 else -1 for i in range(len(primes))])


def reciprocal_coefficients(primes: list[int]) -> list[Fraction]:
    values = [Fraction(1, p) for p in primes]
    mean = sum(values, Fraction(0)) / len(values)
    result = [x - mean for x in values]
    need(sum(result, Fraction(0)) == 0, "reciprocal balance")
    return result


def balanced_coefficients(primes: list[int]) -> list[int]:
    h = len(primes) // 2
    result = [1 if i < h else (-1 if i >= len(primes) - h else 0)
              for i in range(len(primes))]
    need(sum(result) == 0, "balanced balance")
    return result


def fraction_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def spectral_norm(matrix: np.ndarray) -> float:
    eig = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    need(len(eig) > 0 and bool(np.all(np.isfinite(eig))), "spectrum")
    return max(abs(float(eig[0])), abs(float(eig[-1])))


def reverse_matrices(origin: int, count: int, q0: int, exponent: int,
                     law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                                         list[int]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
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


def incidence(values: np.ndarray, primes: list[int], coefficients) -> np.ndarray:
    result = np.zeros(len(values), dtype=np.float64)
    for prime, coefficient in zip(primes, coefficients):
        if coefficient:
            result += float(coefficient) * (values % prime == 0)
    return result


def exact_anchor(anchor: dict[str, Any]) -> None:
    origin, count, q0, exponent, law = 193, 14, 4, 1, "all_plus"
    values = list(range(origin, origin + count))
    def frac(masked: bool) -> list[list[Fraction]]:
        out = [[Fraction(0) for _ in values] for _ in values]
        for prime, sign in zip(shell_for(q0), source_signs(shell_for(q0), law)):
            for i, u in enumerate(values):
                for j, t in enumerate(values):
                    if u == t or (masked and (u % prime == 0 or t % prime == 0)):
                        continue
                    centered = (Fraction(1) if (u - t) % prime == 0
                                else Fraction(0)) - Fraction(1, prime - 1)
                    kernel = Fraction(HEIGHT ** (2 * exponent),
                                      (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                    out[i][j] += sign * prime * kernel * centered
        return out
    actual, ideal = frac(True), frac(False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(count)]
              for i in range(count)]
    primes = shell_for(q0); coefficients = reciprocal_coefficients(primes)
    vector = [sum((coefficients[k] for k, p in enumerate(primes)
                   if value % p == 0), Fraction(0)) for value in values]
    image = [sum(defect[i][j] * vector[j] for j in range(count))
             for i in range(count)]
    square = sum(x * x for x in image)
    need(anchor.get("interval") == [193, 206] and
         anchor.get("shell") == [5, 7] and
         anchor.get("coefficients") == ["1/35", "-1/35"] and
         anchor.get("incidence_vector") ==
         ["0/1", "0/1", "1/35", "-1/35", "0/1", "0/1", "0/1",
          "1/35", "0/1", "0/1", "-1/35", "0/1", "1/35", "0/1"] and
         anchor.get("incidence_vector_squared_norm") == "1/245" and
         anchor.get("response_vector_squared_norm") ==
         f"{square.numerator}/{square.denominator}" and
         anchor.get("response_vector_digest") ==
         hashlib.sha256(canonical([fraction_text(x) for x in image])).hexdigest() and
         anchor.get("identity_exact") is True, "exact anchor")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        locked(PRODUCER, PRODUCER_SHA256, "producer")
        locked(PARENT_CODE, PARENT_CODE_SHA256, "TPC351 producer")
        locked(PARENT_CERT, PARENT_CERT_SHA256, "TPC351 certificate")
        parent = json.loads(PARENT_CERT.read_bytes())
        need(PARENT_CERT.read_bytes() == canonical(parent), "parent canonicality")
        locked(RESULT, CERTIFICATE_SHA256, "certificate")
        raw = RESULT.read_bytes(); document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload", {})
        need(payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "schema/digest")
        protocol = payload.get("protocol", {})
        need(protocol.get("origins") == list(ORIGINS) and
             protocol.get("source_counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("laws") == list(LAW_NAMES) and
             protocol.get("height") == HEIGHT, "protocol")
        need(payload.get("parent_lock") == {
            "TPC351_producer_sha256": PARENT_CODE_SHA256,
            "TPC351_certificate_sha256": PARENT_CERT_SHA256,
        }, "parent lock")
        rows = payload.get("rows", [])
        need(len(rows) == 144, "row census")
        by_key = {(x["origin"], x["count"], x["q"],
                   x["kernel_exponent"], x["law"]): x for x in rows}
        need(len(by_key) == 144, "row keys")
        positive = improved = rhalf = bhalf = rcoord = bcoord = 0
        series_values = {}
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
                            rc = reciprocal_coefficients(primes)
                            bc = balanced_coefficients(primes)
                            rv = incidence(values, primes, rc)
                            bv = incidence(values, primes, bc)
                            rn = float(np.linalg.norm(rv)); bn = float(np.linalg.norm(bv))
                            rr = float(np.linalg.norm(defect @ (rv / rn)))
                            br = float(np.linalg.norm(defect @ (bv / bn)))
                            dn = spectral_norm(defect); inn = spectral_norm(ideal)
                            hit = np.any(np.array([(values % p) == 0 for p in primes]), axis=0)
                            cb = float(np.linalg.norm(defect[:, hit], axis=0).max())
                            gram = np.zeros(count, dtype=np.float64)
                            for p, c in zip(primes, rc):
                                gram += float(c) * (defect @ (values % p == 0).astype(float))
                            ge = float(np.max(np.abs(defect @ (rv / rn) - gram / rn)))
                            rgain = rr / br
                            need(row.get("reciprocal_coefficients") ==
                                 [fraction_text(x) for x in rc] and
                                 row.get("reciprocal_coefficient_sum") == "0/1" and
                                 row.get("balanced_coefficients") == bc and
                                 row.get("balanced_coefficient_sum") == 0 and
                                 row.get("reciprocal_incidence_support") == int(np.count_nonzero(rv)) and
                                 row.get("balanced_incidence_support") == int(np.count_nonzero(bv)) and
                                 close(row.get("reciprocal_incidence_norm"), rn) and
                                 close(row.get("balanced_incidence_norm"), bn) and
                                 close(row.get("reciprocal_witness_response_norm"), rr) and
                                 close(row.get("balanced_witness_response_norm"), br) and
                                 close(row.get("reciprocal_to_defect_ratio"), rr / dn) and
                                 close(row.get("balanced_to_defect_ratio"), br / dn) and
                                 close(row.get("reciprocal_to_ideal_ratio"), rr / inn) and
                                 close(row.get("balanced_to_ideal_ratio"), br / inn) and
                                 close(row.get("reciprocal_to_coordinate_ratio"), rr / cb) and
                                 close(row.get("balanced_to_coordinate_ratio"), br / cb) and
                                 row.get("reciprocal_beats_coordinate") is (rr / cb > 1 + 1e-10) and
                                 row.get("balanced_beats_coordinate") is (br / cb > 1 + 1e-10) and
                                 row.get("reciprocal_at_least_half") is (rr / dn >= .5 - 1e-12) and
                                 row.get("balanced_at_least_half") is (br / dn >= .5 - 1e-12) and
                                 close(row.get("defect_operator_norm"), dn) and
                                 close(row.get("ideal_operator_norm"), inn) and
                                 close(row.get("incidence_gram_max_error"), ge) and
                                 close(row.get("reciprocal_to_balanced_response_ratio"), rgain) and
                                 row.get("improves_balanced_parent") is (rgain > 1 + 1e-10),
                                 "reverse row mismatch")
                            need(ge <= TOL and rr > 0 and br > 0 and
                                 rr <= dn * (1 + TOL) and br <= dn * (1 + TOL),
                                 "witness bound")
                            positive += 1; improved += rgain > 1 + 1e-10
                            rhalf += rr / dn >= .5 - 1e-12
                            bhalf += br / dn >= .5 - 1e-12
                            rcoord += rr / cb > 1 + 1e-10
                            bcoord += br / cb > 1 + 1e-10
                            series_values.setdefault((origin, q0, exponent, law), []).append((count, rr / dn, br / dn))
        need(positive == 144 and improved == 118 and rhalf == 49 and bhalf == 46 and
             rcoord == 47 and bcoord == 30, "aggregate census")
        series = payload.get("growth_series", []); need(len(series) == 48, "series census")
        rn = bn = 0
        for item in series:
            key = (item.get("origin"), item.get("q"), item.get("kernel_exponent"), item.get("law"))
            got = sorted(series_values.get(key, []))
            need(item.get("counts") == list(COUNTS), "series counts")
            need(all(close(a, b) for a, b in zip(item.get("reciprocal_to_defect_ratios", []), [x[1] for x in got])) and
                 all(close(a, b) for a, b in zip(item.get("balanced_to_defect_ratios", []), [x[2] for x in got])), "series values")
            rm = all(got[i + 1][1] >= got[i][1] - 1e-12 for i in range(2))
            bm = all(got[i + 1][2] >= got[i][2] - 1e-12 for i in range(2))
            need(item.get("reciprocal_nondecreasing") is rm and item.get("balanced_nondecreasing") is bm, "series monotonicity")
            rn += rm; bn += bm
        need(rn == 22 and bn == 22, "monotone census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 144 and audit.get("series") == 48 and
             audit.get("positive_reciprocal_rows") == 144 and
             audit.get("positive_balanced_rows") == 144 and
             audit.get("zero_sum_records") == 144 and
             audit.get("improved_parent_rows") == 118 and
             audit.get("coordinate_beaten_reciprocal") == 47 and
             audit.get("coordinate_beaten_balanced") == 30 and
             audit.get("half_defect_reciprocal") == 49 and
             audit.get("half_defect_balanced") == 46 and
             audit.get("reciprocal_support_min") == 28 and
             audit.get("reciprocal_support_max") == 140 and
             audit.get("balanced_support_min") == 25 and
             audit.get("balanced_support_max") == 128 and
             audit.get("reciprocal_nondecreasing_series") == 22 and
             audit.get("balanced_nondecreasing_series") == 22 and
             audit.get("arithmetic_advance") == "NO" and
             audit.get("fixed_power_credit") == 0, "audit")
        exact_anchor(payload.get("exact_anchor", {}))
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC352_UNIFORM_REPAIR_TRANSFER") == "REFUTED_SCOPED" and
             firewall.get("TPC352_HIGH_SHELL_REPAIR") == "REFUTED_SCOPED" and
             firewall.get("TPC352_PARENT_IMPROVEMENT_CENSUS") ==
             "NUMERICALLY_CERTIFIED_FINITE_118_OF_144" and
             firewall.get("TPC352_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC352_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC352_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC352_TWIN_PRIME_RESULT") == "NONE", "firewall")
        print("TPC352_INDEPENDENT_CHECK=PASS rows=144 positive_reciprocal=144 improved_parent=118/144 ratio_floor=0.0801262572786")
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC352_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
