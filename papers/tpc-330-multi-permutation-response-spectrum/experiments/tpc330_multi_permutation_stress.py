#!/usr/bin/env python3
"""Hostile finite checks for the TPC-330 multi-permutation release.

This checker is intentionally small and independent of the producer.  It
checks schema/provenance mutations, all five declared bijections, the four-law
censuses, exact finite Gram algebra, and the fail-closed claim firewall.  It
does not turn the finite certificate into an asymptotic arithmetic result.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-330-multi-permutation-response-spectrum"
CERTIFICATE = PROJECT / "results/tpc330_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-329-heldout-growing-source-native-audit/code/"
    "tpc329_heldout_growing_source_native_audit.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-329-heldout-growing-source-native-audit/results/"
    "tpc329_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERTIFICATE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")
PARENT_CODE_SHA256 = (
    "7f4155d2d24f0062ef358cb496d274afa9295831cb982f06454e6ce2464e3adb")
PARENT_CERT_SHA256 = (
    "38999e2aeda85f53bb4318de89361893cc08bf6c80f39c534cd7e33b1ef0b958")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC330_MULTI_PERMUTATION_RESPONSE_SPECTRUM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM"
ORIGINS = (28001, 36001)
SCALES = (4096, 8192)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
RATIO_GUARD = 5.0e-8
PLACEMENT_CONTROLS = (
    ("identity", 1, 0, "pi_0(i)=i"),
    ("affine_3_11", 3, 11, "pi_3,11(i)=(3*i+11) mod source_count"),
    ("affine_5_17", 5, 17, "pi_5,17(i)=(5*i+17) mod source_count"),
    ("affine_7_29", 7, 29, "pi_7,29(i)=(7*i+29) mod source_count"),
    ("reversal", -1, -1, "pi_rev(i)=source_count-1-i"),
)
CONTROL_NAMES = tuple(item[0] for item in PLACEMENT_CONTROLS)
PLACEMENT_RULE = (
    "five_predeclared_bijections: identity, affine_3_11, affine_5_17, "
    "affine_7_29, reversal")
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
    if limit >= 0:
        sieve[0] = False
    if limit >= 1:
        sieve[1] = False
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            for multiple in range(prime * prime, limit + 1, prime):
                sieve[multiple] = False
    return [prime for prime, flag in enumerate(sieve) if flag]


def is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % prime for prime in range(2, math.isqrt(value) + 1))


def shell(q0: int) -> list[int]:
    return [prime for prime in primes_up_to(2 * max(Q_ANCHORS))
            if q0 < prime <= 2 * q0]


def placement_indices(size: int, multiplier: int, offset: int) -> list[int]:
    indices = [(multiplier * index + offset) % size
               for index in range(size)]
    need(len(set(indices)) == size, "placement is not bijective")
    return indices


def exact_entry(prime: int, u: int, t: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(int((u - t) % prime == 0), 1)
    centered -= Fraction(1, prime - 1)
    return prime * Fraction(HEIGHT * HEIGHT,
                            HEIGHT * HEIGHT + (u - t) ** 2) * centered


def small_matrix(values: list[int], signs: list[int]) -> list[list[Fraction]]:
    primes = [5, 7]
    return [[sum((signs[i] * exact_entry(primes[i], u, t)
                  for i in range(len(primes))), Fraction(0))
             for t in values] for u in values]


def finite_gram_identity() -> None:
    """Exercise the exact identity and two source/operator mutations."""
    values = list(range(20001, 20013))
    matrix = small_matrix(values, [1, 1])
    vector = [Fraction((index % 5) - 2, 3) for index in range(len(values))]
    output = [sum((matrix[u][t] * vector[t]
                   for t in range(len(values))), Fraction(0))
              for u in range(len(values))]
    energy = sum((item * item for item in output), Fraction(0))
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
    flipped_energy = sum((item * item for item in flipped_output), Fraction(0))
    need(flipped_energy != energy, "sign mutation is invisible")

    changed = list(vector)
    changed[3] += Fraction(1, 7)
    changed_output = [sum((matrix[u][t] * changed[t]
                           for t in range(len(values))), Fraction(0))
                      for u in range(len(values))]
    changed_energy = sum((item * item for item in changed_output), Fraction(0))
    need(changed_energy != energy, "source mutation is invisible")
    need(all(exact_entry(prime, values[2], values[2]) == 0
             for prime in (5, 7)), "deleted diagonal mutation")


def expected_census(rows: list[dict[str, Any]], control: str | None = None
                    ) -> dict[str, dict[str, int]]:
    return {
        law: {
            label: sum(
                (row["laws"][law] if control is None else
                 row["placement_controls"][control]["laws"][law])[
                    "classification"] == label
                for row in rows)
            for label in LABELS
        }
        for law in LAW_NAMES
    }


def check() -> None:
    payload = read_certificate()
    protocol = payload["protocol"]
    need(protocol["origins"] == list(ORIGINS) and
         protocol["scales"] == list(SCALES) and
         protocol["source_counts"] == [scale // 2 for scale in SCALES] and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS) and
         protocol["height"] == HEIGHT and
         protocol["placement_null"] == {
             "rule": PLACEMENT_RULE,
             "preserves_source_multiset": True,
             "controls": [
                 {"name": name, "multiplier": multiplier,
                  "offset": offset, "rule": rule}
                 for name, multiplier, offset, rule in PLACEMENT_CONTROLS
             ],
         }, "protocol")
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERTIFICATE.read_bytes()) == PARENT_CERT_SHA256 and
         digest(V59_CODE.read_bytes()) == V59_CODE_SHA256 and
         digest(V59_CERTIFICATE.read_bytes()) == V59_CERT_SHA256,
         "provenance locks")

    rows = payload["rows"]
    need(isinstance(rows, list) and len(rows) == 32, "row count")
    expected_keys = {(origin, scale, q0, exponent)
                     for origin in ORIGINS for scale in SCALES
                     for q0 in Q_ANCHORS for exponent in EXPONENTS}
    seen: set[tuple[int, int, int, int]] = set()
    actual_total = 0
    control_norm_counts = {name: 0 for name in CONTROL_NAMES}
    control_counts = {name: {law: {label: 0 for label in LABELS}
                             for law in LAW_NAMES}
                       for name in CONTROL_NAMES}

    for row in rows:
        key = (row["origin"], row["scale"], row["Q"],
               row["kernel_exponent"])
        need(key in expected_keys and key not in seen, "row key census")
        seen.add(key)
        origin, scale, q0, exponent = key
        source_count = scale // 2
        need(row["source_interval"] ==
             [origin, origin + source_count - 1] and
             row["source_count"] == source_count and
             row["height"] == HEIGHT and row["shell"] == shell(q0) and
             row["shell_cardinality"] == len(shell(q0)) and
             row["operator_shape"] == [source_count, source_count],
             "row geometry")
        width = float(row["source_weight_max_interval_width"])
        need(math.isfinite(width) and width > 0, "source enclosure width")
        for law in LAW_NAMES:
            record = row["laws"][law]
            need(record["classification"] in LABELS, "actual label")
            ratio = float(record["ratio"])
            lower, upper = map(float, record["ratio_interval"])
            need(math.isfinite(ratio) and
                 lower == ratio - RATIO_GUARD and
                 upper == ratio + RATIO_GUARD,
                 "actual ratio guard")
            actual_total += 1

        for name, multiplier, offset, rule in PLACEMENT_CONTROLS:
            indices = placement_indices(source_count, multiplier, offset)
            placement = row["placement_controls"][name]
            need(placement["rule"] == rule and
                 placement["multiplier"] == multiplier and
                 placement["offset"] == offset and
                 placement["bijection"] is True and
                 placement["source_l2_norm_equal"] is True and
                 len(indices) == source_count,
                 "placement metadata " + name)
            control_norm_counts[name] += int(
                placement["source_l2_norm_equal"] is True)
            for law in LAW_NAMES:
                record = placement["laws"][law]
                need(record["classification"] in LABELS,
                     "placement label " + name)
                ratio = float(record["ratio"])
                lower, upper = map(float, record["ratio_interval"])
                need(math.isfinite(ratio) and
                     lower == ratio - RATIO_GUARD and
                     upper == ratio + RATIO_GUARD,
                     "placement ratio guard " + name)
                control_counts[name][law][record["classification"]] += 1

        controls = row["component_controls_all_plus"]
        need(controls["lambda"]["classification"] ==
             "POSITIVE_OFF_DIAGONAL" and
             controls["comparison"]["classification"] ==
             "POSITIVE_OFF_DIAGONAL", "component control sign")

    need(seen == expected_keys and actual_total == 32 * 4,
         "row replay census")
    need(control_norm_counts == {name: 32 for name in CONTROL_NAMES},
         "control norm census")

    expected_actual = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 31,
                     "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 25,
                              "POSITIVE_OFF_DIAGONAL": 7, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                           "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 32,
                       "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
    }
    expected_controls = {
        "identity": expected_actual,
        "affine_3_11": {
            "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                         "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
            "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 20,
                                   "POSITIVE_OFF_DIAGONAL": 12,
                                   "UNRESOLVED": 0},
            "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 27,
                                "POSITIVE_OFF_DIAGONAL": 5,
                                "UNRESOLVED": 0},
            "half_split": {"NEGATIVE_OFF_DIAGONAL": 31,
                            "POSITIVE_OFF_DIAGONAL": 1,
                            "UNRESOLVED": 0},
        },
        "affine_5_17": {
            "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                         "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
            "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 30,
                                   "POSITIVE_OFF_DIAGONAL": 2,
                                   "UNRESOLVED": 0},
            "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                                "POSITIVE_OFF_DIAGONAL": 0,
                                "UNRESOLVED": 0},
            "half_split": {"NEGATIVE_OFF_DIAGONAL": 28,
                            "POSITIVE_OFF_DIAGONAL": 4,
                            "UNRESOLVED": 0},
        },
        "affine_7_29": {
            "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                         "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
            "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 21,
                                   "POSITIVE_OFF_DIAGONAL": 11,
                                   "UNRESOLVED": 0},
            "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                                "POSITIVE_OFF_DIAGONAL": 0,
                                "UNRESOLVED": 0},
            "half_split": {"NEGATIVE_OFF_DIAGONAL": 29,
                            "POSITIVE_OFF_DIAGONAL": 3,
                            "UNRESOLVED": 0},
        },
        "reversal": expected_actual,
    }
    need(expected_census(rows) == expected_actual, "actual law census")
    need(control_counts == expected_controls, "five-control census")

    growth = payload["growth_audit"]
    need(growth["small_scale"] == 4096 and
         growth["large_scale"] == 8192 and growth["pairs"] == 64 and
         growth["all_plus_sign_persistent_pairs"] == 15 and
         growth["all_plus_sign_crossings"] == 1 and
         isinstance(growth["pairs_detail"], list) and
         len(growth["pairs_detail"]) == 64 and
         len({(item["origin"], item["Q"], item["kernel_exponent"],
               item["law"]) for item in growth["pairs_detail"]}) == 64,
         "growth census")
    need(all(math.isfinite(float(item["energy_growth_factor"])) and
             float(item["energy_growth_factor"]) > 0
             for item in growth["pairs_detail"]), "growth finite metrics")

    placement = payload["placement_audit"]
    need(placement["rule"] == PLACEMENT_RULE and
         placement["controls"] == list(CONTROL_NAMES) and
         placement["control_count"] == 5 and
         placement["rows"] == 32 and
         placement["law_observations"] == 640 and
         placement["comparisons"] == 640 and
         placement["source_l2_norm_equal_rows"] == 160 and
         placement["all_plus_affine_positive_rows"] == 32 and
         placement["all_plus_affine_consensus_rows"] == 32 and
         placement["all_plus_identity_reversal_same_rows"] == 32,
         "placement audit header")
    details = placement["details"]
    need(isinstance(details, list) and len(details) == 640 and
         len({(item["origin"], item["scale"], item["Q"],
               item["kernel_exponent"], item["control"], item["law"])
              for item in details}) == 640,
         "placement detail uniqueness")
    need(set(placement["control_summaries"]) == set(CONTROL_NAMES) and
         set(placement["law_spectrum"]) == set(LAW_NAMES) and
         len(placement["pairwise_controls"]) == 10,
         "placement summary shape")

    anchor_values = list(range(36001, 36017))
    anchor_vector = [int(is_prime(value + 2)) - int(value % 2 == 1)
                     for value in anchor_values]
    need(any(value == 0 for value in anchor_vector) and
         any(value == -1 for value in anchor_vector),
         "source-native anchor vector")
    anchor = payload["exact_anchor"]
    need(anchor["shell"] == [5, 7] and
         anchor["interval"] == [36001, 36016] and
         anchor["identity_exact"] is True, "anchor metadata")

    firewall = payload["claim_firewall"]
    need(firewall["TPC330_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC330_MULTI_PERMUTATION_SPECTRUM"] ==
         "NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS" and
         firewall["TPC330_AFFINE_ALL_PLUS_CONSENSUS"] ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall["TPC330_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC330_GROWING_SOURCE_NATIVE_L2"] == "OPEN" and
         firewall["TPC330_FULL_GATE_B"] == "OPEN" and
         firewall["TPC330_TWIN_PRIME_RESULT"] == "NONE",
         "firewall")

    finite_gram_identity()
    print("TPC330_STRESS=PASS rows=32 growth_pairs=64 placement_controls=5 "
          "placement_comparisons=640 four_law_census=1 exact_gram_identity=1 "
          "mutations=2 firewall=fail_closed")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC330_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
