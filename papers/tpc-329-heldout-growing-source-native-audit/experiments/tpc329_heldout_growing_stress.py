#!/usr/bin/env python3
"""Hostile finite checks for the TPC-329 growing holdout release."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-329-heldout-growing-source-native-audit"
CERTIFICATE = PROJECT / "results/tpc329_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-328-source-native-l2-cancellation/code/"
    "tpc328_source_native_l2_cancellation.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-328-source-native-l2-cancellation/results/"
    "tpc328_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERTIFICATE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")
PARENT_CODE_SHA256 = (
    "d9e0e534d8cf5f75172cdb55ecd872cf74cb6ed2e4b13782cccb5c645843e1c9")
PARENT_CERT_SHA256 = (
    "0b772ad7810b282a2961f82f7e0ff5d11f0844e60728669268e95188d31cfe4d")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC329_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT"
ORIGINS = (28001, 36001)
SCALES = (4096, 8192)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
RATIO_GUARD = 5.0e-8
PERMUTATION_MULTIPLIER = 5
PERMUTATION_OFFSET = 17
PLACEMENT_RULE = "pi(i)=(5*i+17) mod source_count"
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
         protocol["height"] == HEIGHT and
         protocol["placement_null"] == {
             "rule": PLACEMENT_RULE,
             "multiplier": PERMUTATION_MULTIPLIER,
             "offset": PERMUTATION_OFFSET,
             "preserves_source_multiset": True,
         }, "protocol")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERTIFICATE.read_bytes()) == PARENT_CERT_SHA256 and
         digest(V59_CODE.read_bytes()) == V59_CODE_SHA256 and
         digest(V59_CERTIFICATE.read_bytes()) == V59_CERT_SHA256,
         "provenance locks")

    rows = payload["rows"]
    need(len(rows) == 32, "row count")
    counts = {law: {label: 0 for label in LABELS} for law in LAW_NAMES}
    placement_counts = {law: {label: 0 for label in LABELS}
                        for law in LAW_NAMES}
    nonzero_widths = 0
    placement_norm_equal = 0
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
            placement = row["placement_control"]["laws"][law]
            placement_label = placement["classification"]
            need(placement_label in LABELS, "unknown placement law label")
            placement_counts[law][placement_label] += 1
            placement_ratio = float(placement["ratio"])
            placement_lo, placement_hi = map(
                float, placement["ratio_interval"])
            need(math.isfinite(placement_ratio) and
                 placement_lo == placement_ratio - RATIO_GUARD and
                 placement_hi == placement_ratio + RATIO_GUARD,
                 "placement ratio guard mutation")
        placement_control = row["placement_control"]
        need(placement_control["rule"] == PLACEMENT_RULE and
             placement_control["multiplier"] == PERMUTATION_MULTIPLIER and
             placement_control["offset"] == PERMUTATION_OFFSET and
             placement_control["bijection"] is True and
             placement_control["source_l2_norm_equal"] is True,
             "placement metadata")
        placement_norm_equal += 1
        controls = row["component_controls_all_plus"]
        need(controls["lambda"]["classification"] ==
             "POSITIVE_OFF_DIAGONAL" and
             controls["comparison"]["classification"] ==
             "POSITIVE_OFF_DIAGONAL", "component control sign")
    need(nonzero_widths == 32 and sum(counts[law][label]
                                      for law in LAW_NAMES
                                      for label in LABELS) == 32 * 4,
         "four-law census")
    expected_placement_counts = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                     "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 30,
                              "POSITIVE_OFF_DIAGONAL": 2, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                           "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 28,
                       "POSITIVE_OFF_DIAGONAL": 4, "UNRESOLVED": 0},
    }
    need(placement_norm_equal == 32 and
         placement_counts == expected_placement_counts,
         "placement census")

    growth = payload["growth_audit"]
    need(growth["small_scale"] == 4096 and growth["large_scale"] == 8192 and
         growth["pairs"] == 64 and
         growth["all_plus_sign_persistent_pairs"] +
         growth["all_plus_sign_crossings"] == 16,
         "growth census")
    details = growth["pairs_detail"]
    need(isinstance(details, list) and len(details) == 64 and
         len({(item["origin"], item["Q"], item["kernel_exponent"],
               item["law"]) for item in details}) == 64,
         "growth detail uniqueness")
    need(all(math.isfinite(float(item["energy_growth_factor"])) and
             math.isfinite(float(item["energy_log2_slope"])) and
             float(item["energy_growth_factor"]) > 0 for item in details),
         "growth finite metrics")

    placement_audit = payload["placement_audit"]
    need(placement_audit["rule"] == PLACEMENT_RULE and
         placement_audit["multiplier"] == PERMUTATION_MULTIPLIER and
         placement_audit["offset"] == PERMUTATION_OFFSET and
         placement_audit["comparisons"] == 128 and
         placement_audit["all_plus_comparisons"] == 32 and
         placement_audit["source_l2_norm_equal_rows"] == 32 and
         placement_audit["all_plus_classification_equal"] == 1 and
         placement_audit["all_plus_classification_changed"] == 31 and
         placement_audit["actual_classification_census"] == payload[
             "finite_audit"]["law_census"] and
         placement_audit["permuted_classification_census"] ==
         expected_placement_counts,
         "placement audit")
    placement_details = placement_audit["details"]
    need(isinstance(placement_details, list) and
         len(placement_details) == 128 and
         len({(item["origin"], item["scale"], item["Q"],
              item["kernel_exponent"], item["law"])
             for item in placement_details}) == 128,
         "placement detail uniqueness")

    # The exact anchor vector must really contain a prime indicator, rather
    # than being silently replaced by the oddness control alone.
    anchor_values = list(range(28001, 28017))
    anchor_vector = [int(is_prime(t + 2)) - int(t % 2 == 1)
                     for t in anchor_values]
    need(any(value == 0 for value in anchor_vector) and
         any(value == -1 for value in anchor_vector),
         "source-native anchor vector")
    anchor = payload["exact_anchor"]
    need(anchor["shell"] == [5, 7] and anchor["interval"] == [28001, 28016] and
         anchor["identity_exact"] is True, "anchor metadata")

    firewall = payload["claim_firewall"]
    need(firewall["TPC329_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC329_PLACEMENT_NULL"] ==
         "NUMERICALLY_CERTIFIED_FINITE_MULTISET_PRESERVING_CONTROL" and
         firewall["TPC329_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC329_GROWING_SOURCE_NATIVE_L2"] == "OPEN" and
         firewall["TPC329_FULL_GATE_B"] == "OPEN" and
         firewall["TPC329_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    finite_gram_identity()
    print("TPC329_STRESS=PASS rows=32 growth_pairs=64 placement_comparisons=128 "
          "four_law_census=1 source_enclosure=32 exact_gram_identity=1 mutations=2 "
          "firewall=fail_closed")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC329_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
