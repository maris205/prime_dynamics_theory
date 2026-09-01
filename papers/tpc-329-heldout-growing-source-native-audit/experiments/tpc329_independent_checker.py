#!/usr/bin/env python3
"""Independent replay for the TPC-329 held-out growing source-native audit.

The checker deliberately does not import the producer.  It rebuilds the
prime shells, the finite V59 source vector, and the coherent matrices in a
different accumulation order, then replays every stored energy ratio and
classification.  The arithmetic source is finite and declared; no growing
estimate is inferred from a successful replay.
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

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

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
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
RATIO_GUARD = 5.0e-8
NUMERIC_TOL = 3.0e-6
PERMUTATION_MULTIPLIER = 5
PERMUTATION_OFFSET = 17
PLACEMENT_RULE = "pi(i)=(5*i+17) mod source_count"
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character",
             "half_split")
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")
EXACT_INTERVAL = (28001, 28016)
EXACT_DIRECT_DIGEST = "031f9a525f90ab196de1ae14ab7fd421f714523729919e939ee213e0f1f73312"
EXACT_DIAGONAL_DIGEST = "2a6749e1d49aef201792a755454767d19ae2613049bbab2f8ed3ca898d5a6dc2"
EXACT_OFF_DIGEST = "7dc1a942e30b9e242c9d3189f1aee7267f6f99e3276015f2fa80fc739e84dd63"


class Failure(RuntimeError):
    """Raised on the first fail-closed mismatch."""


class DuplicateKey(ValueError):
    """Reject duplicate JSON object members instead of silently rebinding."""


def pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def load_json(path: Path) -> tuple[bytes, dict[str, Any]]:
    raw = path.read_bytes()
    value = json.loads(raw, object_pairs_hook=pairs_no_duplicates)
    need(isinstance(value, dict), f"object expected: {path}")
    need(raw == canonical(value), f"noncanonical JSON: {path}")
    return raw, value


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (
                (limit - p * p) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


TAIL_PRIMES = primes_up_to(TAIL_CUTOFF)
SHELL_PRIMES = primes_up_to(2 * max(Q_ANCHORS))
TAIL_CENTER: Decimal | None = None


def shell(q0: int) -> list[int]:
    return [p for p in SHELL_PRIMES if q0 < p <= 2 * q0]


def distinct_factors(value: int) -> list[int]:
    remaining = value
    factors: list[int] = []
    for p in TAIL_PRIMES:
        if p * p > remaining:
            break
        if remaining % p == 0:
            factors.append(p)
            while remaining % p == 0:
                remaining //= p
    if remaining > 1:
        factors.append(remaining)
    return factors


def prime_power_base(value: int) -> int | None:
    factors = distinct_factors(value)
    return factors[0] if len(factors) == 1 else None


def is_prime(value: int) -> bool:
    return value >= 2 and prime_power_base(value) == value


def comparison_midpoint(value: int) -> float:
    global TAIL_CENTER
    if value % 2 == 0:
        return 0.0
    if TAIL_CENTER is None:
        finite = Decimal(1)
        for p in TAIL_PRIMES:
            if p > COMPARISON_CUTOFF:
                numerator = Decimal((p - 1) ** 2 - 1)
                denominator = Decimal((p - 1) ** 2)
                finite *= numerator / denominator
        lower = finite * (1 - Decimal(1) / Decimal(TAIL_CUTOFF - 1))
        TAIL_CENTER = (lower + finite) / Decimal(2)
    local = Decimal(2)
    for p in distinct_factors(value):
        if p > COMPARISON_CUTOFF:
            local *= Decimal(p - 1) / Decimal(p - 2)
    return float(TAIL_CENTER * local)


def lambda_value(value: int) -> float:
    base = prime_power_base(value)
    return 0.0 if base is None else float(Decimal(base).ln())


def source_vector(origin: int, scale: int
                  ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = range(origin, origin + scale // 2)
    lambdas = []
    comparisons = []
    for t in values:
        lambdas.append(lambda_value(t + 2))
        comparisons.append(comparison_midpoint(t))
    lam = np.asarray(lambdas, dtype=np.float64)
    comp = np.asarray(comparisons, dtype=np.float64)
    return lam, comp, lam - comp


def sign_vectors(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1.0 if i % 2 == 0 else -1.0 for i in range(len(primes))]),
        "mod4_character": np.asarray(
            [1.0 if p % 4 == 1 else -1.0 for p in primes]),
        "half_split": np.asarray(
            [1.0 if i < len(primes) / 2 else -1.0
             for i in range(len(primes))]),
    }


def coherent_matrices(origin: int, scale: int, q0: int, exponent: int
                      ) -> tuple[list[int], dict[str, np.ndarray]]:
    values = np.arange(origin, origin + scale // 2, dtype=np.int64)
    delta = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + delta.astype(np.float64) ** 2) ** exponent)
    primes = shell(q0)
    sign_map = sign_vectors(primes)
    matrices = {name: np.zeros((len(values), len(values)), dtype=np.float64)
                for name in LAW_NAMES}
    # Reverse shell order is intentional: it gives a replay with a different
    # summation order from the producer.
    for index, p in reversed(list(enumerate(primes))):
        valid = ((delta != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = ((delta % p == 0).astype(np.float64) - 1.0 / (p - 1))
        block = float(p) * kernel * centered * valid
        for name in LAW_NAMES:
            matrices[name] += sign_map[name][index] * block
    for name in LAW_NAMES:
        matrices[name] = (matrices[name] + matrices[name].T) / 2.0
    return primes, matrices


def metric(matrix: np.ndarray, vector: np.ndarray) -> tuple[float, float, float,
                                                                 str]:
    output = matrix @ vector
    energy = float(np.dot(output, output))
    diagonal = float(np.sum(matrix * matrix * (vector[None, :] ** 2),
                            dtype=np.float64))
    need(energy > 0 and diagonal > 0 and math.isfinite(energy) and
         math.isfinite(diagonal), "nonpositive replay metric")
    ratio = energy / diagonal
    if ratio + RATIO_GUARD < 1.0:
        label = "NEGATIVE_OFF_DIAGONAL"
    elif ratio - RATIO_GUARD > 1.0:
        label = "POSITIVE_OFF_DIAGONAL"
    else:
        label = "UNRESOLVED"
    return energy, diagonal, energy - diagonal, ratio, label


def placement_permutation(size: int) -> np.ndarray:
    indices = np.asarray(
        [(PERMUTATION_MULTIPLIER * index + PERMUTATION_OFFSET) % size
         for index in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in indices)) == size,
         "placement permutation")
    return indices


def close(actual: float, recorded: Any, label: str) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(target) and math.isfinite(actual), label + " nonfinite")
    scale = max(1.0, abs(actual), abs(target))
    need(abs(actual - target) <= NUMERIC_TOL * scale,
         label + " mismatch")


def check_metric(recorded: dict[str, Any], values: tuple[float, float, float,
                                                          str], label: str
                 ) -> None:
    energy, diagonal, off, ratio, classification = values
    need(recorded.get("classification") == classification,
         label + " classification")
    close(energy, recorded.get("energy"), label + " energy")
    close(diagonal, recorded.get("coordinate_diagonal"),
         label + " diagonal")
    close(off, recorded.get("off_diagonal"), label + " off")
    close(ratio, recorded.get("ratio"), label + " ratio")
    interval = recorded.get("ratio_interval")
    need(isinstance(interval, list) and len(interval) == 2,
         label + " ratio interval")
    lo, hi = float(interval[0]), float(interval[1])
    need(math.isfinite(lo) and math.isfinite(hi) and lo <= ratio <= hi,
         label + " ratio enclosure")
    close(ratio - RATIO_GUARD, lo, label + " lower guard")
    close(ratio + RATIO_GUARD, hi, label + " upper guard")


def replay_growth(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Recompute the two-scale pairing from row-level energies."""
    small_scale, large_scale = SCALES
    indexed = {(row["origin"], row["scale"], row["Q"],
                row["kernel_exponent"]): row for row in rows}
    details = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                small = indexed[(origin, small_scale, q0, exponent)]
                large = indexed[(origin, large_scale, q0, exponent)]
                for law in LAW_NAMES:
                    es = float(small["laws"][law]["energy"])
                    el = float(large["laws"][law]["energy"])
                    ds = float(small["laws"][law]["coordinate_diagonal"])
                    dl = float(large["laws"][law]["coordinate_diagonal"])
                    growth = el / es
                    diagonal_growth = dl / ds
                    details.append({
                        "origin": origin, "Q": q0,
                        "kernel_exponent": exponent, "law": law,
                        "small_scale": small_scale, "large_scale": large_scale,
                        "energy_growth_factor": growth,
                        "diagonal_growth_factor": diagonal_growth,
                        "energy_log2_slope": math.log(growth, 2.0),
                        "small_classification": small["laws"][law][
                            "classification"],
                        "large_classification": large["laws"][law][
                            "classification"],
                        "sign_persistent": small["laws"][law][
                            "classification"] == large["laws"][law][
                            "classification"],
                    })
    by_law = {}
    for law in LAW_NAMES:
        selected = [item for item in details if item["law"] == law]
        by_law[law] = {
            "pairs": len(selected),
            "sign_persistent_pairs": sum(item["sign_persistent"]
                                          for item in selected),
            "energy_growth_factor_min": min(
                item["energy_growth_factor"] for item in selected),
            "energy_growth_factor_max": max(
                item["energy_growth_factor"] for item in selected),
            "energy_log2_slope_min": min(
                item["energy_log2_slope"] for item in selected),
            "energy_log2_slope_max": max(
                item["energy_log2_slope"] for item in selected),
        }
    all_plus = [item for item in details if item["law"] == "all_plus"]
    return {
        "small_scale": small_scale, "large_scale": large_scale,
        "pairs": len(details),
        "all_plus_sign_persistent_pairs": sum(
            item["sign_persistent"] for item in all_plus),
        "all_plus_sign_crossings": sum(
            not item["sign_persistent"] for item in all_plus),
        "all_plus_energy_growth_factor_min": min(
            item["energy_growth_factor"] for item in all_plus),
        "all_plus_energy_growth_factor_max": max(
            item["energy_growth_factor"] for item in all_plus),
        "all_plus_energy_log2_slope_min": min(
            item["energy_log2_slope"] for item in all_plus),
        "all_plus_energy_log2_slope_max": max(
            item["energy_log2_slope"] for item in all_plus),
        "by_law": by_law,
        "pairs_detail": details,
    }


def check_growth(recorded: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    expected = replay_growth(rows)
    need(recorded.get("small_scale") == expected["small_scale"] and
         recorded.get("large_scale") == expected["large_scale"] and
         recorded.get("pairs") == expected["pairs"] == 64,
         "growth header")
    for key in ("all_plus_sign_persistent_pairs", "all_plus_sign_crossings"):
        need(recorded.get(key) == expected[key], "growth sign census")
    for key in ("all_plus_energy_growth_factor_min",
                "all_plus_energy_growth_factor_max",
                "all_plus_energy_log2_slope_min",
                "all_plus_energy_log2_slope_max"):
        close(expected[key], recorded.get(key), "growth " + key)
    actual_by_law = recorded.get("by_law")
    need(isinstance(actual_by_law, dict), "growth law summary")
    for law in LAW_NAMES:
        got = actual_by_law.get(law)
        want = expected["by_law"][law]
        need(isinstance(got, dict) and got.get("pairs") == want["pairs"] == 16
             and got.get("sign_persistent_pairs") ==
             want["sign_persistent_pairs"], "growth law census")
        for key in ("energy_growth_factor_min", "energy_growth_factor_max",
                    "energy_log2_slope_min", "energy_log2_slope_max"):
            close(want[key], got.get(key), "growth law " + law + " " + key)
    details = recorded.get("pairs_detail")
    want_details = expected["pairs_detail"]
    need(isinstance(details, list) and len(details) == len(want_details),
         "growth detail count")
    for index, (got, want) in enumerate(zip(details, want_details)):
        for key in ("origin", "Q", "kernel_exponent", "law", "small_scale",
                    "large_scale", "small_classification",
                    "large_classification", "sign_persistent"):
            need(got.get(key) == want[key],
                 "growth detail key " + str(index) + " " + key)
        for key in ("energy_growth_factor", "diagonal_growth_factor",
                    "energy_log2_slope"):
            close(want[key], got.get(key),
                  "growth detail " + str(index) + " " + key)


def check_placement(recorded: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    details = []
    for row in rows:
        for law in LAW_NAMES:
            actual = row["laws"][law]
            permuted = row["placement_control"]["laws"][law]
            ar = float(actual["ratio"])
            pr = float(permuted["ratio"])
            details.append({
                "origin": row["origin"], "scale": row["scale"],
                "Q": row["Q"], "kernel_exponent": row["kernel_exponent"],
                "law": law, "actual_ratio": ar, "permuted_ratio": pr,
                "absolute_ratio_difference": abs(ar - pr),
                "actual_classification": actual["classification"],
                "permuted_classification": permuted["classification"],
                "classification_equal": (
                    actual["classification"] == permuted["classification"]),
            })
    need(recorded.get("rule") ==
         PLACEMENT_RULE and
         recorded.get("multiplier") == PERMUTATION_MULTIPLIER and
         recorded.get("offset") == PERMUTATION_OFFSET and
         recorded.get("comparisons") == len(details) == 128 and
         recorded.get("all_plus_comparisons") == 32,
         "placement header")
    all_plus = [item for item in details if item["law"] == "all_plus"]
    need(recorded.get("all_plus_classification_equal") == sum(
             item["classification_equal"] for item in all_plus) and
         recorded.get("all_plus_classification_changed") == sum(
             not item["classification_equal"] for item in all_plus),
         "placement all-plus census")
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
    expected_permuted = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 0,
                     "POSITIVE_OFF_DIAGONAL": 32, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 30,
                              "POSITIVE_OFF_DIAGONAL": 2, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                           "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 28,
                       "POSITIVE_OFF_DIAGONAL": 4, "UNRESOLVED": 0},
    }
    actual_census = {law: {label: sum(
        item["actual_classification"] == label
        for item in details if item["law"] == law) for label in LABELS}
                     for law in LAW_NAMES}
    permuted_census = {law: {label: sum(
        item["permuted_classification"] == label
        for item in details if item["law"] == law) for label in LABELS}
                       for law in LAW_NAMES}
    need(recorded.get("source_l2_norm_equal_rows") == len(rows) == 32 and
         recorded.get("actual_classification_census") == actual_census ==
         expected_actual and
         recorded.get("permuted_classification_census") == permuted_census ==
         expected_permuted, "placement class census")
    for law in LAW_NAMES:
        selected = [item for item in details if item["law"] == law]
        got = recorded["by_law"][law]
        need(got["comparisons"] == len(selected) == 32 and
             got["classification_changed"] == sum(
                 not item["classification_equal"] for item in selected),
             "placement law census")
        close(max(item["absolute_ratio_difference"] for item in selected),
              got["max_abs_ratio_difference"],
              "placement law difference " + law)
    need(isinstance(recorded.get("details"), list) and
         len(recorded["details"]) == len(details), "placement detail count")
    for index, (got, want) in enumerate(zip(recorded["details"], details)):
        for key in ("origin", "scale", "Q", "kernel_exponent", "law",
                    "actual_classification", "permuted_classification",
                    "classification_equal"):
            need(got.get(key) == want[key],
                 "placement detail key " + str(index) + " " + key)
        for key in ("actual_ratio", "permuted_ratio",
                    "absolute_ratio_difference"):
            close(want[key], got.get(key),
                  "placement detail " + str(index) + " " + key)


def exact_anchor() -> tuple[str, str, str, float, float, float]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = [5, 7]
    matrix = [[Fraction(0) for _ in values] for _ in values]
    for p in primes:
        for ui, u in enumerate(values):
            for ti, t in enumerate(values):
                if u == t or u % p == 0 or t % p == 0:
                    continue
                centered = Fraction(int((u - t) % p == 0), 1)
                centered -= Fraction(1, p - 1)
                matrix[ui][ti] += p * Fraction(HEIGHT * HEIGHT,
                    HEIGHT * HEIGHT + (u - t) ** 2) * centered
    vector = [Fraction(int(is_prime(t + 2)), 1) -
              Fraction(int(t % 2 == 1), 1) for t in values]
    output = [sum((matrix[u][t] * vector[t]
                   for t in range(len(values))), Fraction(0))
              for u in range(len(values))]
    energy = sum((x * x for x in output), Fraction(0))
    diagonal = sum((vector[t] * vector[t] *
                    sum((matrix[u][t] * matrix[u][t]
                         for u in range(len(values))), Fraction(0))
                    for t in range(len(values))), Fraction(0))
    off = energy - diagonal
    return (fraction_digest(energy), fraction_digest(diagonal),
            fraction_digest(off), float(energy), float(diagonal), float(off))


def locked_parent_checks(payload: dict[str, Any]) -> None:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent producer hash")
    need(digest(PARENT_CERTIFICATE.read_bytes()) == PARENT_CERT_SHA256,
         "parent certificate hash")
    need(digest(V59_CODE.read_bytes()) == V59_CODE_SHA256,
         "V59 producer hash")
    need(digest(V59_CERTIFICATE.read_bytes()) == V59_CERT_SHA256,
         "V59 certificate hash")
    lock = payload["parent_lock"]
    need(lock["TPC328_producer_sha256"] == PARENT_CODE_SHA256 and
         lock["TPC328_certificate_sha256"] == PARENT_CERT_SHA256 and
         lock["TPC267_V59_producer_sha256"] == V59_CODE_SHA256 and
         lock["TPC267_V59_certificate_sha256"] == V59_CERT_SHA256,
         "parent lock fields")


def check() -> None:
    raw, document = load_json(CERTIFICATE)
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
         canonical(payload)).hexdigest(), "payload hash")
    need(payload.get("round2_clue") ==
         "SEPARATE_SOURCE_NORM_FROM_ARITHMETIC_PLACEMENT_WITH_MULTIPLE_PREDECLARED_CONTROLS",
         "round2 clue")
    locked_parent_checks(payload)

    protocol = payload["protocol"]
    need(protocol["origins"] == list(ORIGINS) and
         protocol["scales"] == list(SCALES) and
         protocol["source_counts"] == [x // 2 for x in SCALES] and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS) and
         protocol["height"] == HEIGHT and
         protocol["comparison_cutoff"] == COMPARISON_CUTOFF and
         protocol["euler_tail_cutoff"] == TAIL_CUTOFF and
         protocol["placement_null"] == {
             "rule": PLACEMENT_RULE,
             "multiplier": PERMUTATION_MULTIPLIER,
             "offset": PERMUTATION_OFFSET,
             "preserves_source_multiset": True,
         }, "protocol")

    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 32, "row census")
    expected_keys = {(o, n, q, s) for o in ORIGINS for n in SCALES
                     for q in Q_ANCHORS for s in EXPONENTS}
    seen: set[tuple[int, int, int, int]] = set()
    counts = {law: {label: 0 for label in LABELS} for law in LAW_NAMES}
    lambda_positive = 0
    comparison_positive = 0

    for row in rows:
        key = (row["origin"], row["scale"], row["Q"],
               row["kernel_exponent"])
        need(key not in seen and key in expected_keys, "row key census")
        seen.add(key)
        origin, scale, q0, exponent = key
        lo, hi = origin, origin + scale // 2 - 1
        sh = shell(q0)
        need(row["source_interval"] == [lo, hi] and
             row["source_count"] == scale // 2 and
             row["height"] == HEIGHT and row["shell"] == sh and
             row["shell_cardinality"] == len(sh) and
             row["operator_shape"] == [scale // 2, scale // 2],
             "row geometry")
        lam, comp, residual = source_vector(origin, scale)
        _, matrices = coherent_matrices(origin, scale, q0, exponent)
        for law in LAW_NAMES:
            values = metric(matrices[law], residual)
            check_metric(row["laws"][law], values, law)
            counts[law][values[-1]] += 1
        permutation = placement_permutation(len(residual))
        permuted_residual = residual[permutation]
        placement = row["placement_control"]
        need(placement["rule"] ==
             PLACEMENT_RULE and
             placement["multiplier"] == PERMUTATION_MULTIPLIER and
             placement["offset"] == PERMUTATION_OFFSET and
             placement["bijection"] is True and
             placement["source_l2_norm_equal"] is True,
             "placement metadata")
        for law in LAW_NAMES:
            values = metric(matrices[law], permuted_residual)
            check_metric(placement["laws"][law], values,
                         "placement " + law)
        all_plus_matrix = matrices["all_plus"]
        lambda_metric = metric(all_plus_matrix, lam)
        comparison_metric = metric(all_plus_matrix, comp)
        check_metric(row["component_controls_all_plus"]["lambda"],
                     lambda_metric, "lambda control")
        check_metric(row["component_controls_all_plus"]["comparison"],
                     comparison_metric, "comparison control")
        need(lambda_metric[-1] == "POSITIVE_OFF_DIAGONAL" and
             comparison_metric[-1] == "POSITIVE_OFF_DIAGONAL",
             "component control sign")
        lambda_positive += 1
        comparison_positive += 1

    need(seen == expected_keys and counts == payload["finite_audit"][
        "law_census"], "full row replay")
    need(lambda_positive == 32 and comparison_positive == 32,
         "census/control summary")
    expected_counts = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 31,
                     "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 25,
                              "POSITIVE_OFF_DIAGONAL": 7, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                           "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 32,
                       "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
    }
    need(counts == expected_counts, "held-out census")
    audit = payload["finite_audit"]
    need(audit["rows"] == 32 and audit["origins"] == 2 and
         audit["scales"] == 2 and
         audit["component_lambda_positive_controls"] == 32 and
         audit["component_comparison_positive_controls"] == 32 and
         audit["fixed_power_credit"] == 0, "audit firewall")
    check_growth(payload["growth_audit"], rows)
    growth = payload["growth_audit"]
    need(growth["all_plus_sign_persistent_pairs"] == 15 and
         growth["all_plus_sign_crossings"] == 1 and
         growth["by_law"]["alternating_index"]["sign_persistent_pairs"] == 15 and
         growth["by_law"]["mod4_character"]["sign_persistent_pairs"] == 16 and
         growth["by_law"]["half_split"]["sign_persistent_pairs"] == 16,
         "held-out growth census")
    check_placement(payload["placement_audit"], rows)

    anchor = payload["exact_anchor"]
    direct, diagonal, off, energy_value, diagonal_value, off_value = exact_anchor()
    need(anchor["energy_digest"] == direct and
         anchor["coordinate_diagonal_digest"] == diagonal and
         anchor["off_diagonal_digest"] == off and
         anchor["identity_exact"] is True and
         direct == EXACT_DIRECT_DIGEST and diagonal == EXACT_DIAGONAL_DIGEST and
         off == EXACT_OFF_DIGEST, "exact anchor replay")
    need(abs(energy_value - diagonal_value - off_value) < 1.0e-10,
         "exact anchor float identity")

    firewall = payload["claim_firewall"]
    need(firewall["TPC329_EXACT_GRAM_DECOMPOSITION"] ==
         "PROVED_EXACT_FINITE" and
         firewall["TPC329_SOURCE_NATIVE_VECTOR"] ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall["TPC329_COMPONENT_CONTROLS"] ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall["TPC329_SIGN_AT_SCALE_GROWTH"] ==
         "NUMERICALLY_CERTIFIED_FINITE" and
         firewall["TPC329_PLACEMENT_NULL"] ==
         "NUMERICALLY_CERTIFIED_FINITE_MULTISET_PRESERVING_CONTROL" and
         firewall["TPC329_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC329_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC329_GROWING_SOURCE_NATIVE_L2"] == "OPEN" and
         firewall["TPC329_FULL_GATE_B"] == "OPEN" and
         firewall["TPC329_TWIN_PRIME_RESULT"] == "NONE", "claim firewall")
    print("TPC329_INDEPENDENT_CHECK=PASS rows=32 origins=2 scales=2 laws=4 "
          "growth_pairs=64 exact_anchor=1")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError, np.linalg.LinAlgError) as error:
        print("TPC329_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
