#!/usr/bin/env python3
"""Independent replay for the TPC-330 multi-permutation response spectrum.

The checker deliberately does not import the producer.  It rebuilds the
prime shells, the finite V59 source vector, and the coherent matrices in a
different accumulation order, then replays every stored energy ratio,
placement control, and classification.  The arithmetic source is finite and
declared; no growing estimate is inferred from a successful replay.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

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
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
RATIO_GUARD = 5.0e-8
NUMERIC_TOL = 3.0e-6
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
EXACT_INTERVAL = (36001, 36016)
EXACT_DIRECT_DIGEST = "be04ff1900efb9eeba9482c063e74024171d1463b81650e9c4078049f60caf8a"
EXACT_DIAGONAL_DIGEST = "235c2de92d5c13b6e611bc40e4d24f6f8235d544eab333d694b98fda75a44922"
EXACT_OFF_DIGEST = "95466f98ab619552ee0fca7be44f2c29c6d30a7662175a4da26f3c578a2c5ee2"


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


def placement_permutation(size: int, multiplier: int,
                          offset: int) -> np.ndarray:
    indices = np.asarray(
        [(multiplier * index + offset) % size for index in range(size)],
        dtype=np.int64)
    need(len(set(int(item) for item in indices)) == size,
         "placement control")
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
    """Rebuild all five placement summaries from the row-level records."""
    details: list[dict[str, Any]] = []
    for row in rows:
        for control_name in CONTROL_NAMES:
            control = row["placement_controls"][control_name]
            for law in LAW_NAMES:
                identity = row["laws"][law]
                placed = control["laws"][law]
                identity_ratio = float(identity["ratio"])
                control_ratio = float(placed["ratio"])
                details.append({
                    "origin": row["origin"], "scale": row["scale"],
                    "Q": row["Q"], "kernel_exponent": row["kernel_exponent"],
                    "control": control_name, "law": law,
                    "identity_ratio": identity_ratio,
                    "control_ratio": control_ratio,
                    "absolute_ratio_difference": abs(
                        identity_ratio - control_ratio),
                    "identity_classification": identity["classification"],
                    "control_classification": placed["classification"],
                    "classification_equal": (
                        identity["classification"] ==
                        placed["classification"]),
                })

    need(recorded.get("rule") == PLACEMENT_RULE and
         recorded.get("controls") == list(CONTROL_NAMES) and
         recorded.get("control_count") == len(CONTROL_NAMES) == 5 and
         recorded.get("rows") == len(rows) == 32 and
         recorded.get("law_observations") == 640 and
         recorded.get("comparisons") == len(details) == 640,
         "placement header")

    expected_control_summaries: dict[str, Any] = {}
    for control_name, multiplier, offset, rule in PLACEMENT_CONTROLS:
        selected = [item for item in details
                    if item["control"] == control_name]
        by_law: dict[str, Any] = {}
        classification_census: dict[str, dict[str, int]] = {}
        for law in LAW_NAMES:
            law_rows = [item for item in selected if item["law"] == law]
            classification_census[law] = {
                label: sum(item["control_classification"] == label
                           for item in law_rows)
                for label in LABELS
            }
            by_law[law] = {
                "comparisons": len(law_rows),
                "classification_changed_vs_identity": sum(
                    not item["classification_equal"] for item in law_rows),
                "ratio_min": min(item["control_ratio"] for item in law_rows),
                "ratio_max": max(item["control_ratio"] for item in law_rows),
                "max_abs_ratio_difference": max(
                    item["absolute_ratio_difference"] for item in law_rows),
            }
        expected_control_summaries[control_name] = {
            "rule": rule,
            "multiplier": multiplier,
            "offset": offset,
            "bijection": True,
            "source_l2_norm_equal_rows": len(rows),
            "classification_census": classification_census,
            "by_law": by_law,
        }

    summaries = recorded.get("control_summaries")
    need(isinstance(summaries, dict) and
         set(summaries) == set(CONTROL_NAMES), "control summary keys")
    for control_name in CONTROL_NAMES:
        got = summaries[control_name]
        want = expected_control_summaries[control_name]
        need(got.get("rule") == want["rule"] and
             got.get("multiplier") == want["multiplier"] and
             got.get("offset") == want["offset"] and
             got.get("bijection") is True and
             got.get("source_l2_norm_equal_rows") == 32 and
             got.get("classification_census") ==
             want["classification_census"],
             "control summary metadata " + control_name)
        got_by_law = got.get("by_law")
        need(isinstance(got_by_law, dict),
             "control summary laws " + control_name)
        for law in LAW_NAMES:
            got_law = got_by_law.get(law)
            want_law = want["by_law"][law]
            need(isinstance(got_law, dict) and
                 got_law.get("comparisons") == want_law["comparisons"] == 32 and
                 got_law.get("classification_changed_vs_identity") ==
                 want_law["classification_changed_vs_identity"],
                 "control law census " + control_name + " " + law)
            for key in ("ratio_min", "ratio_max",
                        "max_abs_ratio_difference"):
                close(want_law[key], got_law.get(key),
                     "control law metric " + control_name + " " + law +
                     " " + key)

    need(recorded.get("source_l2_norm_equal_rows") == 160 and
         recorded.get("all_plus_affine_positive_rows") == 32 and
         recorded.get("all_plus_affine_consensus_rows") == 32 and
         recorded.get("all_plus_identity_reversal_same_rows") == 32,
         "placement aggregate census")

    expected_spectrum: dict[str, Any] = {}
    for law in LAW_NAMES:
        signatures: Counter[tuple[str, ...]] = Counter()
        ranges: list[float] = []
        for row in rows:
            signature = tuple(row["placement_controls"][control_name][
                "laws"][law]["classification"]
                for control_name in CONTROL_NAMES)
            signatures[signature] += 1
            ratios = [float(row["placement_controls"][control_name][
                "laws"][law]["ratio"])
                      for control_name in CONTROL_NAMES]
            ranges.append(max(ratios) - min(ratios))
        expected_spectrum[law] = {
            "rows": len(rows),
            "unanimous_negative_rows": sum(
                count for signature, count in signatures.items()
                if set(signature) == {"NEGATIVE_OFF_DIAGONAL"}),
            "unanimous_positive_rows": sum(
                count for signature, count in signatures.items()
                if set(signature) == {"POSITIVE_OFF_DIAGONAL"}),
            "mixed_control_rows": sum(
                count for signature, count in signatures.items()
                if len(set(signature)) > 1),
            "control_classification_signatures": {
                "|".join(signature): count
                for signature, count in sorted(signatures.items())
            },
            "ratio_range_min": min(ranges),
            "ratio_range_max": max(ranges),
        }
    spectrum = recorded.get("law_spectrum")
    need(isinstance(spectrum, dict) and set(spectrum) == set(LAW_NAMES),
         "law spectrum keys")
    for law in LAW_NAMES:
        got = spectrum[law]
        want = expected_spectrum[law]
        need(got.get("rows") == want["rows"] == 32 and
             got.get("unanimous_negative_rows") ==
             want["unanimous_negative_rows"] and
             got.get("unanimous_positive_rows") ==
             want["unanimous_positive_rows"] and
             got.get("mixed_control_rows") == want["mixed_control_rows"] and
             got.get("control_classification_signatures") ==
             want["control_classification_signatures"],
             "law spectrum census " + law)
        close(want["ratio_range_min"], got.get("ratio_range_min"),
              "law spectrum minimum " + law)
        close(want["ratio_range_max"], got.get("ratio_range_max"),
              "law spectrum maximum " + law)

    expected_pairs: dict[str, Any] = {}
    for left_index, left in enumerate(CONTROL_NAMES):
        for right in CONTROL_NAMES[left_index + 1:]:
            changes: list[tuple[bool, float]] = []
            for row in rows:
                for law in LAW_NAMES:
                    left_record = row["placement_controls"][left]["laws"][law]
                    right_record = row["placement_controls"][right]["laws"][law]
                    changes.append((
                        left_record["classification"] !=
                        right_record["classification"],
                        abs(float(left_record["ratio"]) -
                            float(right_record["ratio"]))))
            expected_pairs[f"{left}__{right}"] = {
                "left": left, "right": right,
                "comparisons": len(changes),
                "classification_changes": sum(item[0] for item in changes),
                "max_abs_ratio_difference": max(item[1] for item in changes),
            }
    pairs = recorded.get("pairwise_controls")
    need(isinstance(pairs, dict) and set(pairs) == set(expected_pairs),
         "pairwise control keys")
    for name, want in expected_pairs.items():
        got = pairs[name]
        need(got.get("left") == want["left"] and
             got.get("right") == want["right"] and
             got.get("comparisons") == want["comparisons"] == 128 and
             got.get("classification_changes") ==
             want["classification_changes"], "pairwise control census " + name)
        close(want["max_abs_ratio_difference"],
              got.get("max_abs_ratio_difference"),
              "pairwise control difference " + name)

    recorded_details = recorded.get("details")
    need(isinstance(recorded_details, list) and
         len(recorded_details) == len(details), "placement detail count")
    for index, (got, want) in enumerate(zip(recorded_details, details)):
        for key in ("origin", "scale", "Q", "kernel_exponent", "control",
                    "law", "identity_classification",
                    "control_classification", "classification_equal"):
            need(got.get(key) == want[key],
                 "placement detail key " + str(index) + " " + key)
        for key in ("identity_ratio", "control_ratio",
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
    need(lock["TPC329_producer_sha256"] == PARENT_CODE_SHA256 and
         lock["TPC329_certificate_sha256"] == PARENT_CERT_SHA256 and
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
         "DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS",
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
             "preserves_source_multiset": True,
             "controls": [
                 {"name": name, "multiplier": multiplier,
                  "offset": offset, "rule": rule}
                 for name, multiplier, offset, rule in PLACEMENT_CONTROLS
             ],
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
        for control_name, multiplier, offset, rule in PLACEMENT_CONTROLS:
            permutation = placement_permutation(len(residual), multiplier,
                                                offset)
            permuted_residual = residual[permutation]
            placement = row["placement_controls"][control_name]
            need(placement["rule"] == rule and
                 placement["multiplier"] == multiplier and
                 placement["offset"] == offset and
                 placement["bijection"] is True and
                 placement["source_l2_norm_equal"] is True and
                 bool(np.array_equal(np.sort(residual),
                                     np.sort(permuted_residual))) is True,
                 "placement metadata " + control_name)
            for law in LAW_NAMES:
                values = metric(matrices[law], permuted_residual)
                check_metric(placement["laws"][law], values,
                             "placement " + control_name + " " + law)
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
    need(firewall["TPC330_EXACT_GRAM_DECOMPOSITION"] ==
         "PROVED_EXACT_FINITE" and
         firewall["TPC330_SOURCE_NATIVE_VECTOR"] ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall["TPC330_COMPONENT_CONTROLS"] ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall["TPC330_SIGN_AT_SCALE_GROWTH"] ==
         "NUMERICALLY_CERTIFIED_FINITE" and
         firewall["TPC330_MULTI_PERMUTATION_SPECTRUM"] ==
         "NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS" and
         firewall["TPC330_AFFINE_ALL_PLUS_CONSENSUS"] ==
         "NUMERICALLY_CERTIFIED_FINITE_32_OF_32" and
         firewall["TPC330_GROWING_SOURCE_NATIVE_L2"] == "OPEN" and
         firewall["TPC330_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC330_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC330_FULL_GATE_B"] == "OPEN" and
         firewall["TPC330_TWIN_PRIME_RESULT"] == "NONE", "claim firewall")
    print("TPC330_INDEPENDENT_CHECK=PASS rows=32 origins=2 scales=2 laws=4 "
          "growth_pairs=64 placement_controls=5 placement_comparisons=640 "
          "exact_anchor=1")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError, np.linalg.LinAlgError) as error:
        print("TPC330_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
