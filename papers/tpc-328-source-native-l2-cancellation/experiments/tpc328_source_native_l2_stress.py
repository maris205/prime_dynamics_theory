#!/usr/bin/env python3
"""Hostile finite checks for the TPC-328 source-native L2 release."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-328-source-native-l2-cancellation"
CERTIFICATE = PROJECT / "results/tpc328_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-327-three-origin-scale-triangulation/code/"
    "tpc327_three_origin_scale_triangulation.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-327-three-origin-scale-triangulation/results/"
    "tpc327_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERTIFICATE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")
PARENT_CODE_SHA256 = (
    "ddb5117b4533608a0f1ffb510f901d02d53ea6158c08d921aeced4f0c1653f47")
PARENT_CERT_SHA256 = (
    "1550f36b41c71dc09d68f220658a3fdf12f52822a4fd13fcebcf7aefea0f403f")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC328_SOURCE_NATIVE_L2_CANCELLATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS"
ORIGINS = (12001, 16001, 20001)
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
RATIO_GUARD = 5.0e-8
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character",
             "half_split")
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")


class Failure(RuntimeError):
    pass


class DuplicateKey(ValueError):
    pass


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
        if key in answer:
            raise DuplicateKey(key)
        answer[key] = value
    return answer


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def read_certificate() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw, object_pairs_hook=no_duplicates)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    return payload


def primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[:2] = [False, False]
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return [p for p, flag in enumerate(sieve) if flag]


def is_prime(value: int) -> bool:
    return value >= 2 and all(value % p for p in range(2, math.isqrt(value) + 1))


def shell(q0: int) -> list[int]:
    return [p for p in primes_up_to(2 * max(Q_ANCHORS))
            if q0 < p <= 2 * q0]


def exact_entry(p: int, u: int, t: int) -> Fraction:
    if u == t or u % p == 0 or t % p == 0:
        return Fraction(0)
    centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
    return p * Fraction(HEIGHT * HEIGHT,
                        HEIGHT * HEIGHT + (u - t) ** 2) * centered


def small_matrix(values: list[int], signs: list[int]) -> list[list[Fraction]]:
    primes = [5, 7]
    return [[sum((signs[i] * exact_entry(primes[i], u, t)
                  for i in range(len(primes))), Fraction(0))
             for t in values] for u in values]


def finite_gram_identity() -> None:
    values = list(range(20001, 20013))
    matrix = small_matrix(values, [1, 1])
    vector = [Fraction((i % 5) - 2, 3) for i in range(len(values))]
    output = [sum((matrix[u][t] * vector[t]
                   for t in range(len(values))), Fraction(0))
              for u in range(len(values))]
    energy = sum((x * x for x in output), Fraction(0))
    diagonal = sum((vector[t] * vector[t] *
                    sum((matrix[u][t] * matrix[u][t]
                         for u in range(len(values))), Fraction(0))
                    for t in range(len(values))), Fraction(0))
    off = sum((vector[t] * vector[v] *
               sum((matrix[u][t] * matrix[u][v]
                    for u in range(len(values))), Fraction(0))
               for t in range(len(values))
               for v in range(len(values)) if t != v), Fraction(0))
    need(energy == diagonal + off and energy > 0 and diagonal > 0,
         "finite Gram identity")

    flipped = small_matrix(values, [1, -1])
    flipped_output = [sum((flipped[u][t] * vector[t]
                           for t in range(len(values))), Fraction(0))
                      for u in range(len(values))]
    flipped_energy = sum((x * x for x in flipped_output), Fraction(0))
    need(flipped_energy != energy, "sign mutation is invisible")

    changed = list(vector)
    changed[3] += Fraction(1, 7)
    changed_output = [sum((matrix[u][t] * changed[t]
                           for t in range(len(values))), Fraction(0))
                      for u in range(len(values))]
    changed_energy = sum((x * x for x in changed_output), Fraction(0))
    need(changed_energy != energy, "source mutation is invisible")
    need(all(exact_entry(p, values[2], values[2]) == 0 for p in (5, 7)),
         "deleted diagonal mutation")


def check() -> None:
    payload = read_certificate()
    protocol = payload["protocol"]
    need(protocol["origins"] == list(ORIGINS) and
         protocol["scales"] == list(SCALES) and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS) and
         protocol["height"] == HEIGHT, "protocol")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERTIFICATE.read_bytes()) == PARENT_CERT_SHA256 and
         digest(V59_CODE.read_bytes()) == V59_CODE_SHA256 and
         digest(V59_CERTIFICATE.read_bytes()) == V59_CERT_SHA256,
         "provenance locks")

    rows = payload["rows"]
    need(len(rows) == 96, "row count")
    counts = {law: {label: 0 for label in LABELS} for law in LAW_NAMES}
    nonzero_widths = 0
    for row in rows:
        need(row["source_interval"] == [
            row["origin"], row["origin"] + row["scale"] // 2 - 1],
             "source interval")
        need(row["shell"] == shell(row["Q"]) and
             row["shell_cardinality"] == len(shell(row["Q"])),
             "shell geometry")
        width = float(row["source_weight_max_interval_width"])
        need(math.isfinite(width) and width > 0, "source enclosure width")
        nonzero_widths += 1
        for law in LAW_NAMES:
            record = row["laws"][law]
            label = record["classification"]
            need(label in LABELS, "unknown law label")
            counts[law][label] += 1
            ratio = float(record["ratio"])
            lo, hi = map(float, record["ratio_interval"])
            need(math.isfinite(ratio) and lo == ratio - RATIO_GUARD and
                 hi == ratio + RATIO_GUARD, "ratio guard mutation")
        controls = row["component_controls_all_plus"]
        need(controls["lambda"]["classification"] ==
             "POSITIVE_OFF_DIAGONAL" and
             controls["comparison"]["classification"] ==
             "POSITIVE_OFF_DIAGONAL", "component control sign")
    expected = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 81,
                     "POSITIVE_OFF_DIAGONAL": 15, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 73,
                              "POSITIVE_OFF_DIAGONAL": 23, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 74,
                           "POSITIVE_OFF_DIAGONAL": 22, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 61,
                       "POSITIVE_OFF_DIAGONAL": 35, "UNRESOLVED": 0},
    }
    need(counts == expected and nonzero_widths == 96,
         "four-law census")

    # The exact anchor vector must really contain a prime indicator, rather
    # than being silently replaced by the oddness control alone.
    anchor_values = list(range(20001, 20017))
    anchor_vector = [int(is_prime(t + 2)) - int(t % 2 == 1)
                     for t in anchor_values]
    need(any(value == 0 for value in anchor_vector) and
         any(value == -1 for value in anchor_vector),
         "source-native anchor vector")
    anchor = payload["exact_anchor"]
    need(anchor["shell"] == [5, 7] and anchor["interval"] == [20001, 20016] and
         anchor["identity_exact"] is True, "anchor metadata")

    firewall = payload["claim_firewall"]
    need(firewall["TPC328_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC328_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC328_GROWING_SOURCE_NATIVE_L2"] == "OPEN" and
         firewall["TPC328_FULL_GATE_B"] == "OPEN" and
         firewall["TPC328_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    finite_gram_identity()
    print("TPC328_STRESS=PASS rows=96 four_law_census=1 "
          "source_enclosure=96 exact_gram_identity=1 mutations=2 "
          "firewall=fail_closed")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC328_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
