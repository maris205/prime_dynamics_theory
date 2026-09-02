#!/usr/bin/env python3
"""Independent reverse-order checker for TPC-347.

This file deliberately rebuilds the prime shells, masks, kernels, and spectra
without importing the producer.  It checks the canonical certificate and the
finite claim firewall; it is not an official Route-A/Route-B evaluator.
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
PROJECT = ROOT / "papers/tpc-347-convolution-mask-defect-interface"
PRODUCER = PROJECT / "code/tpc347_convolution_mask_defect_interface.py"
RESULT = PROJECT / "results/tpc347_certificate.json"
PARENT = ROOT / "papers/tpc-346-third-panel-hostile-replication"
PARENT_CODE = PARENT / "code/tpc346_third_panel_hostile_replication.py"
PARENT_CERT = PARENT / "results/tpc346_certificate.json"

PRODUCER_SHA256 = "2b423b1863fa054b8987934824e0637e464ea5192ba560076abbcfc2394076fb"
PARENT_CODE_SHA256 = "2c0bb5fd2e8738fa18dc419491a91b29c5a1fb8cc4f5fabaaec19e0a45752d4a"
PARENT_CERT_SHA256 = "f15c5a5bf3ef9f14a5bdd9503bb74dbcc218b82b0598db0726d61deb01ee1e46"
SCHEMA = "TPC347_CONVOLUTION_MASK_DEFECT_INTERFACE_V1"
STATUS = (
    "PROVED_EXACT_FINITE_CONVOLUTION_MASK_DEFECT_INTERFACE_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SPECTRAL_AUDIT")
ORIGINS = (40097, 48097)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
RADIUS = 65_536
TOL = 5.0e-8


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


def close(actual: float, expected: Any, label: str,
          tolerance: float = TOL) -> None:
    a = float(actual)
    b = float(expected)
    need(math.isfinite(a) and math.isfinite(b) and
         abs(a - b) <= tolerance * max(1.0, abs(a), abs(b)), label)


def lock(path: Path, expected: str, label: str) -> None:
    need(path.is_file(), label + " missing")
    need(digest(path.read_bytes()) == expected, label + " hash")


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            first = p * p
            sieve[first:limit + 1:p] = b"\x00" * (
                (limit - first) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q: int) -> list[int]:
    return [p for p in PRIMES if q < p <= 2 * q]


def sign_vector(primes: list[int], law: str) -> list[int]:
    if law == "all_plus":
        return [1] * len(primes)
    if law == "alternating_index":
        return [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    if law == "mod4_character":
        return [1 if p % 4 == 1 else -1 for p in primes]
    if law == "half_split":
        return [1 if i < len(primes) / 2 else -1
                for i in range(len(primes))]
    raise Failure("law")


def norm2(matrix: np.ndarray) -> float:
    values = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    need(len(values) > 0 and bool(np.all(np.isfinite(values))), "spectrum")
    return max(abs(float(values[0])), abs(float(values[-1])))


def rebuild(origin: int, count: int, q: int, exponent: int,
            law: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[int]]:
    # Reverse shell order is intentional: it exercises a different accumulation
    # path from the producer while representing the same finite matrix.
    values = np.arange(origin, origin + count, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    physical = np.zeros((count, count), dtype=np.float64)
    ideal = np.zeros((count, count), dtype=np.float64)
    primes = shell(q)
    for prime, sign in reversed(list(zip(primes, sign_vector(primes, law)))):
        residue = ((differences % prime == 0).astype(np.float64) -
                   1.0 / (prime - 1))
        np.fill_diagonal(residue, 0.0)
        block = float(sign * prime) * kernel * residue
        ideal += block
        allowed = ((differences != 0) &
                   (values[:, None] % prime != 0) &
                   (values[None, :] % prime != 0))
        physical += block * allowed
    physical = (physical + physical.T) / 2.0
    ideal = (ideal + ideal.T) / 2.0
    return physical, ideal, physical - ideal, primes


def young(q: int, exponent: int, law: str) -> tuple[float, float, float]:
    distance = np.arange(1, RADIUS + 1, dtype=np.int64)
    h = (float(HEIGHT) ** (2 * exponent) /
         (HEIGHT * HEIGHT + distance.astype(np.float64) ** 2) ** exponent)
    value = np.zeros(RADIUS, dtype=np.float64)
    primes = shell(q)
    for prime, sign in reversed(list(zip(primes, sign_vector(primes, law)))):
        centered = ((distance % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        value += float(sign * prime) * h * centered
    finite = 2.0 * math.fsum(float(abs(x)) for x in value)
    tail = (2.0 * HEIGHT ** (2 * exponent) * sum(primes) /
            ((2 * exponent - 1) * RADIUS ** (2 * exponent - 1)))
    return finite + tail, finite, tail


def exact_matrix(count: int, q: int, exponent: int,
                 masked: bool) -> list[list[Fraction]]:
    values = list(range(1, count + 1))
    result = [[Fraction(0) for _ in values] for _ in values]
    for prime in reversed(shell(q)):
        for i, u in enumerate(values):
            for j, t in enumerate(values):
                if u == t or (masked and (u % prime == 0 or t % prime == 0)):
                    continue
                centered = Fraction(int((u - t) % prime == 0))
                centered -= Fraction(1, prime - 1)
                kernel = Fraction(HEIGHT ** (2 * exponent),
                                  (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
                result[i][j] += prime * kernel * centered
    return result


def fmdigest(matrix: list[list[Fraction]]) -> str:
    values = [[f"{x.numerator}/{x.denominator}" for x in row]
              for row in matrix]
    return hashlib.sha256(canonical(values)).hexdigest()


def check_anchor(payload: dict[str, Any]) -> None:
    anchor = payload["exact_anchor"]
    actual = exact_matrix(6, 4, 1, True)
    ideal = exact_matrix(6, 4, 1, False)
    defect = [[actual[i][j] - ideal[i][j] for j in range(6)]
              for i in range(6)]
    close_anchor = {
        "actual_digest": fmdigest(actual),
        "ideal_digest": fmdigest(ideal),
        "defect_digest": fmdigest(defect),
    }
    for key, value in close_anchor.items():
        need(anchor.get(key) == value, "anchor " + key)
    need(anchor.get("identity_exact") is True and
         anchor.get("symmetry_exact") is True, "anchor flags")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        lock(PRODUCER, PRODUCER_SHA256, "producer")
        lock(PARENT_CODE, PARENT_CODE_SHA256, "parent producer")
        lock(PARENT_CERT, PARENT_CERT_SHA256, "parent certificate")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
             "schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload digest")
        protocol = payload["protocol"]
        need(tuple(protocol["origins"]) == ORIGINS and
             tuple(protocol["source_counts"]) == COUNTS and
             tuple(protocol["q_anchors"]) == Q_ANCHORS and
             tuple(protocol["kernel_exponents"]) == EXPONENTS and
             tuple(protocol["laws"]) == LAWS and
             protocol["height"] == HEIGHT and
             protocol["young_radius"] == RADIUS, "protocol")
        need(payload["parent_lock"]["TPC346_producer_sha256"] ==
             PARENT_CODE_SHA256 and
             payload["parent_lock"]["TPC346_certificate_sha256"] ==
             PARENT_CERT_SHA256, "parent lock")
        rows = payload.get("rows", [])
        need(len(rows) == 192, "row count")
        calculated_young = {(q, e, law): young(q, e, law)
                            for q in Q_ANCHORS for e in EXPONENTS
                            for law in LAWS}
        actual_ratios: list[float] = []
        defect_ratios: list[float] = []
        occupancies: list[float] = []
        for index, stored in enumerate(rows):
            origin = int(stored["origin"])
            count = int(stored["count"])
            q = int(stored["q"])
            exponent = int(stored["kernel_exponent"])
            law = stored["law"]
            expected_origin = ORIGINS[index // (len(COUNTS) * len(Q_ANCHORS) *
                                                len(EXPONENTS) * len(LAWS))]
            need(origin == expected_origin and count in COUNTS and
                 q in Q_ANCHORS and exponent in EXPONENTS and law in LAWS,
                 "row ordering")
            physical, ideal, defect, primes = rebuild(origin, count, q,
                                                       exponent, law)
            an = norm2(physical)
            tn = norm2(ideal)
            dn = norm2(defect)
            df = float(np.linalg.norm(defect, ord="fro"))
            envelope, finite_l1, tail = calculated_young[(q, exponent, law)]
            close(an, stored["actual_norm"], "actual norm")
            close(tn, stored["ideal_norm"], "ideal norm")
            close(dn, stored["defect_norm"], "defect norm")
            close(df, stored["defect_frobenius_norm"], "defect Frobenius")
            close(dn / tn, stored["defect_to_ideal_ratio"], "defect ratio")
            close(an / tn, stored["actual_to_ideal_ratio"], "actual ratio")
            close(envelope, stored["young_l1_envelope"], "Young envelope")
            close(finite_l1, stored["young_finite_l1"], "Young finite")
            close(tail, stored["young_tail_majorant"], "Young tail")
            close(an / (envelope + df), stored["combined_occupancy"],
                  "combined occupancy")
            need(bool(np.max(np.abs(physical - ideal - defect)) <= 2e-8),
                 "matrix identity")
            need(an <= envelope + df + 1e-7 * max(1.0, envelope + df),
                 "combined bound")
            actual_ratios.append(an / tn)
            defect_ratios.append(dn / tn)
            occupancies.append(an / (envelope + df))
            need(stored["finite_bound_holds"] is True and
                 stored["operator_shape"] == [count, count] and
                 stored["shell"] == primes, "row metadata")
        invariance = payload.get("translation_invariance_audit", [])
        need(len(invariance) == 96 and
             all(item.get("invariant") is True for item in invariance),
             "invariance metadata")
        for item in invariance:
            count, q, exponent, law = (int(item["count"]), int(item["q"]),
                                       int(item["kernel_exponent"]), item["law"])
            _, left, _, _ = rebuild(ORIGINS[0], count, q, exponent, law)
            _, right, _, _ = rebuild(ORIGINS[1], count, q, exponent, law)
            close(float(np.max(np.abs(left - right))),
                  item["matrix_max_difference"], "translation difference")
            need(float(np.max(np.abs(left - right))) <= 2e-8,
                 "translation identity")
        check_anchor(payload)
        summary = payload["summary"]
        close(min(defect_ratios), summary["defect_to_ideal_ratio_min"],
              "summary defect min")
        close(max(defect_ratios), summary["defect_to_ideal_ratio_max"],
              "summary defect max")
        close(min(actual_ratios), summary["actual_to_ideal_ratio_min"],
              "summary actual min")
        close(max(actual_ratios), summary["actual_to_ideal_ratio_max"],
              "summary actual max")
        close(min(occupancies), summary["combined_occupancy_min"],
              "summary occupancy min")
        close(max(occupancies), summary["combined_occupancy_max"],
              "summary occupancy max")
        need(payload["finite_audit"]["combined_bound_violations"] == 0 and
             payload["finite_audit"]["fixed_power_credit"] == 0 and
             payload["finite_audit"]["arithmetic_advance"] == "NO",
             "claim ceiling")
        firewall = payload["claim_firewall"]
        need(firewall["TPC347_SOURCE_UNIFORM_ARITHMETIC_L2"] == "OPEN" and
             firewall["TPC347_UNIFORM_MASKED_OPERATOR_BOUND"] == "OPEN" and
             firewall["TPC347_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC347_TWIN_PRIME_RESULT"] == "NONE",
             "firewall")
        print("TPC347_INDEPENDENT_CHECK=PASS rows=192 invariance=96 "
              "bound_violations=0")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC347_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
