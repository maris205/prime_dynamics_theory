#!/usr/bin/env python3
"""TPC-330: a multi-permutation source-native placement-response spectrum.

TPC-329 showed that one norm-preserving affine placement null can reverse the
finite all-plus readout.  This release freezes a small, symmetric menu of
five coordinate bijections and measures the same finite object across the
whole menu.  For the literal deleted-diagonal prime-shell blocks B_p, it forms

    C_e = sum_p e_p B_p,
    E_e(v) = ||C_e v||_2^2,
    D_e(v) = sum_t v_t^2 ||C_e e_t||_2^2.

The identity E_e(v)-D_e(v) is the source-coordinate off-diagonal Gram
contribution.  The source vector is the finite V59 residual
Lambda(t+2)-b_x^(2)(t), evaluated with the declared finite Euler-tail and
logarithm enclosure.  All numerical conclusions are finite and guarded;
they do not assert a growing arithmetic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC330 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc330_certificate.json"

PARENT_PROJECT = ROOT / "papers/tpc-329-heldout-growing-source-native-audit"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc329_heldout_growing_source_native_audit.py")
PARENT_RESULT = PARENT_PROJECT / "results/tpc329_certificate.json"
PARENT_CODE_SHA256 = (
    "7f4155d2d24f0062ef358cb496d274afa9295831cb982f06454e6ce2464e3adb")
PARENT_RESULT_SHA256 = (
    "38999e2aeda85f53bb4318de89361893cc08bf6c80f39c534cd7e33b1ef0b958")

V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_RESULT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_RESULT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC330_MULTI_PERMUTATION_RESPONSE_SPECTRUM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MULTI_PERMUTATION_RESPONSE_SPECTRUM"
ROUND2_CLUE = (
    "DECOMPOSE_POSITION_RESPONSE_INTO_AFFINE_REVERSAL_AND_SOURCE_ALIGNED_COMPONENTS")

ORIGINS = (28001, 36001)
SCALES = (4096, 8192)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
LOG_GUARD = Fraction(Decimal("1e-70"))
RATIO_GUARD = 5.0e-8
RATIO_TOL = 1.0e-6
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
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")

EXACT_INTERVAL = (36001, 36016)
EXACT_Q = 4
EXACT_EXPONENT = 1
EXACT_VECTOR_NAME = "prime_indicator_minus_odd_indicator"


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def display(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def load_parent() -> tuple[dict[str, Any], dict[str, Any]]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC329 producer provenance")
    need(PARENT_RESULT.is_file() and
         digest(PARENT_RESULT.read_bytes()) == PARENT_RESULT_SHA256,
         "TPC329 certificate provenance")
    raw = PARENT_RESULT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "TPC329 certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT",
         "TPC329 certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") ==
         "TPC329_HELDOUT_GROWING_SOURCE_NATIVE_AUDIT_V1",
         "TPC329 payload type")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("scales") == list(SCALES) and
         protocol.get("Q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("height") == HEIGHT and
         protocol.get("placement_null", {}).get("rule") ==
         "pi(i)=(5*i+17) mod source_count",
         "TPC329 protocol lock")

    need(V59_CODE.is_file() and digest(V59_CODE.read_bytes()) == V59_CODE_SHA256,
         "V59 producer provenance")
    need(V59_RESULT.is_file() and
         digest(V59_RESULT.read_bytes()) == V59_RESULT_SHA256,
         "V59 certificate provenance")
    return document, payload


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [prime for prime in range(2, limit + 1) if sieve[prime]]


PRIMES = primes_up_to(TAIL_CUTOFF)


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def factor_distinct(value: int) -> list[int]:
    remaining = value
    factors: list[int] = []
    for prime in PRIMES:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            factors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 1:
        factors.append(remaining)
    return factors


def prime_power(value: int) -> tuple[int, int] | None:
    for prime in PRIMES:
        if prime > value:
            break
        power = prime
        exponent = 1
        while power < value:
            power *= prime
            exponent += 1
        if power == value:
            return prime, exponent
    return None


def is_prime_small(value: int) -> bool:
    """Independent trial-division predicate for the exact anchor vector."""
    if value < 2:
        return False
    for prime in PRIMES:
        if prime * prime > value:
            break
        if value % prime == 0:
            return value == prime
    return True


TAIL_CACHE: tuple[Fraction, Fraction] | None = None


def comparison_tail() -> tuple[Fraction, Fraction]:
    """Return the declared finite Euler-tail enclosure for C_2."""
    global TAIL_CACHE
    if TAIL_CACHE is None:
        finite = Decimal(1)
        for prime in PRIMES:
            if prime > COMPARISON_CUTOFF:
                numerator = Decimal((prime - 1) ** 2 - 1)
                denominator = Decimal((prime - 1) ** 2)
                finite *= numerator / denominator
        lower = finite * (1 - Decimal(1) / Decimal(TAIL_CUTOFF - 1))
        TAIL_CACHE = (Fraction(lower), Fraction(finite))
    return TAIL_CACHE


def log_interval(prime: int) -> tuple[Fraction, Fraction]:
    center = Fraction(Decimal(prime).ln())
    return center - LOG_GUARD, center + LOG_GUARD


def lambda_interval(value: int) -> tuple[Fraction, Fraction]:
    power = prime_power(value)
    if power is None:
        return Fraction(0), Fraction(0)
    lo, hi = log_interval(power[0])
    # The von Mangoldt function is Lambda(p^k)=log(p), without a 1/k
    # normalization.  Keep this aligned with the locked V59 model.
    return lo, hi


def comparison_interval(value: int) -> tuple[Fraction, Fraction]:
    if value % 2 == 0:
        return Fraction(0), Fraction(0)
    lower, upper = comparison_tail()
    local = Fraction(2)
    for prime in factor_distinct(value):
        if prime > COMPARISON_CUTOFF:
            local *= Fraction(prime - 1, prime - 2)
    return lower * local, upper * local


def midpoint(interval: tuple[Fraction, Fraction]) -> float:
    return float((interval[0] + interval[1]) / 2)


def source_vectors(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray, np.ndarray,
                                               float]:
    lambdas: list[float] = []
    comparisons: list[float] = []
    residuals: list[float] = []
    max_width = 0.0
    for value in range(lo, hi + 1):
        lam = lambda_interval(value + 2)
        comp = comparison_interval(value)
        lambdas.append(midpoint(lam))
        comparisons.append(midpoint(comp))
        residuals.append(midpoint((lam[0] - comp[1], lam[1] - comp[0])))
        max_width = max(max_width, float(lam[1] - lam[0] +
                                          comp[1] - comp[0]))
    lam_array = np.asarray(lambdas, dtype=np.float64)
    comp_array = np.asarray(comparisons, dtype=np.float64)
    residual = np.asarray(residuals, dtype=np.float64)
    need(bool(np.all(np.isfinite(residual))), "finite source residual")
    return lam_array, comp_array, residual, max_width


def kernel_matrix(values: np.ndarray, exponent: int) -> np.ndarray:
    differences = values[:, None] - values[None, :]
    distances = differences.astype(np.float64)
    return (float(HEIGHT) ** (2 * exponent) /
            (HEIGHT * HEIGHT + distances * distances) ** exponent)


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    count = len(primes)
    return {
        "all_plus": np.ones(count, dtype=np.float64),
        "alternating_index": np.asarray(
            [1 if index % 2 == 0 else -1 for index in range(count)],
            dtype=np.float64),
        "mod4_character": np.asarray(
            [1 if prime % 4 == 1 else -1 for prime in primes],
            dtype=np.float64),
        "half_split": np.asarray(
            [1 if index < count / 2 else -1 for index in range(count)],
            dtype=np.float64),
    }


def coherent_matrices(values: np.ndarray, q0: int, exponent: int
                      ) -> tuple[list[int], dict[str, np.ndarray]]:
    differences = values[:, None] - values[None, :]
    kernel_values = kernel_matrix(values, exponent)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrices = {
        name: np.zeros((len(values), len(values)), dtype=np.float64)
        for name in LAW_NAMES
    }
    for index, prime in enumerate(primes):
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        block = float(prime) * kernel_values * centered * valid
        for name in LAW_NAMES:
            matrices[name] += signs[name][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    return primes, matrices


def ratio_record(matrix: np.ndarray, vector: np.ndarray) -> dict[str, Any]:
    output = matrix @ vector
    energy = float(np.dot(output, output))
    diagonal = float(np.sum((matrix * matrix) * (vector[None, :] ** 2),
                            dtype=np.float64))
    need(energy > 0 and diagonal > 0 and
         math.isfinite(energy) and math.isfinite(diagonal),
         "positive arithmetic L2 quantities")
    off_diagonal = energy - diagonal
    ratio = energy / diagonal
    lower = ratio - RATIO_GUARD
    upper = ratio + RATIO_GUARD
    if upper < 1.0:
        classification = "NEGATIVE_OFF_DIAGONAL"
    elif lower > 1.0:
        classification = "POSITIVE_OFF_DIAGONAL"
    else:
        classification = "UNRESOLVED"
    return {
        "energy": display(energy),
        "coordinate_diagonal": display(diagonal),
        "off_diagonal": display(off_diagonal),
        "ratio": display(ratio),
        "ratio_interval": [display(lower), display(upper)],
        "classification": classification,
    }


def placement_permutation(size: int, multiplier: int,
                          offset: int) -> np.ndarray:
    """Build one predeclared, size-compatible coordinate bijection."""
    indices = np.asarray(
        [(multiplier * index + offset) % size for index in range(size)],
        dtype=np.int64)
    need(len(set(int(item) for item in indices)) == size,
        "placement control is not bijective")
    return indices


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(int((u - t) % prime == 0), 1)
    centered -= Fraction(1, prime - 1)
    return (prime * Fraction(HEIGHT ** (2 * exponent),
                             (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent)
            * centered)


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell_for(EXACT_Q)
    vector = [Fraction(int(is_prime_small(value + 2)), 1) -
              Fraction(int(value % 2 == 1), 1) for value in values]
    matrix = [[sum((exact_entry(prime, u, t, EXACT_EXPONENT)
                    for prime in primes), Fraction(0))
               for t in values] for u in values]
    output = [sum((matrix[u][t] * vector[t] for t in range(len(values))),
                  Fraction(0)) for u in range(len(values))]
    energy = sum((item * item for item in output), Fraction(0))
    diagonal = sum((vector[t] * vector[t] *
                    sum((matrix[u][t] * matrix[u][t]
                         for u in range(len(values))), Fraction(0))
                    for t in range(len(values))), Fraction(0))
    off = energy - diagonal
    need(energy > 0 and diagonal > 0, "exact anchor positivity")
    return {
        "interval": list(EXACT_INTERVAL),
        "Q": EXACT_Q,
        "shell": primes,
        "exponent": EXACT_EXPONENT,
        "vector": EXACT_VECTOR_NAME,
        "energy_digest": fraction_digest(energy),
        "coordinate_diagonal_digest": fraction_digest(diagonal),
        "off_diagonal_digest": fraction_digest(off),
        "energy_decimal": display(float(energy), 16),
        "coordinate_diagonal_decimal": display(float(diagonal), 16),
        "off_diagonal_decimal": display(float(off), 16),
        "identity_exact": energy == diagonal + off,
    }


def row_record(origin: int, scale: int, q0: int, exponent: int
               ) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comp, residual, width = source_vectors(lo, hi)
    primes, matrices = coherent_matrices(values, q0, exponent)
    laws = {name: ratio_record(matrices[name], residual)
            for name in LAW_NAMES}
    placement_controls: dict[str, dict[str, Any]] = {}
    for control_name, multiplier, offset, rule in PLACEMENT_CONTROLS:
        permutation = placement_permutation(len(values), multiplier, offset)
        permuted_residual = residual[permutation]
        placement_controls[control_name] = {
            "rule": rule,
            "multiplier": multiplier,
            "offset": offset,
            "bijection": True,
            "source_l2_norm_equal": bool(
                np.array_equal(np.sort(residual), np.sort(permuted_residual))),
            "laws": {name: ratio_record(matrices[name], permuted_residual)
                     for name in LAW_NAMES},
        }
    need(placement_controls["identity"]["laws"] == laws,
         "identity placement control mismatch")
    controls = {
        "lambda": ratio_record(matrices["all_plus"], lam),
        "comparison": ratio_record(matrices["all_plus"], comp),
    }
    need(all(item["classification"] != "UNRESOLVED"
             for item in laws.values()), "residual ratio separation")
    need(controls["lambda"]["classification"] == "POSITIVE_OFF_DIAGONAL" and
         controls["comparison"]["classification"] == "POSITIVE_OFF_DIAGONAL",
         "positive component controls")
    return {
        "origin": origin,
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": len(values),
        "Q": q0,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "comparison_cutoff": COMPARISON_CUTOFF,
        "shell": primes,
        "shell_cardinality": len(primes),
        "operator_shape": [len(values), len(values)],
        "source_model": "beta_x^(2)(t)=Lambda(t+2)-b_x^(2)(t)",
        "source_weight_max_interval_width": display(width, 8),
        "laws": laws,
        "placement_controls": placement_controls,
        "component_controls_all_plus": controls,
    }


def census(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    return {
        name: {
            label: sum(row["laws"][name]["classification"] == label
                       for row in rows)
            for label in LABELS
        }
        for name in LAW_NAMES
    }


def panel_summary(rows: list[dict[str, Any]], origin: int, scale: int
                  ) -> dict[str, Any]:
    selected = [row for row in rows
                if row["origin"] == origin and row["scale"] == scale]
    need(len(selected) == len(Q_ANCHORS) * len(EXPONENTS),
         "panel row census")
    return {
        "origin": origin,
        "scale": scale,
        "rows": len(selected),
        "all_plus_negative_off_diagonal": sum(
            row["laws"]["all_plus"]["classification"] ==
            "NEGATIVE_OFF_DIAGONAL" for row in selected),
        "all_plus_positive_off_diagonal": sum(
            row["laws"]["all_plus"]["classification"] ==
            "POSITIVE_OFF_DIAGONAL" for row in selected),
        "all_plus_ratio_min": display(min(
            float(row["laws"]["all_plus"]["ratio"]) for row in selected)),
        "all_plus_ratio_max": display(max(
            float(row["laws"]["all_plus"]["ratio"]) for row in selected)),
    }


def growth_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare the two held-out scales without importing an asymptotic claim."""
    small_scale, large_scale = SCALES
    pairs: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                small = next(row for row in rows if
                             row["origin"] == origin and
                             row["scale"] == small_scale and
                             row["Q"] == q0 and
                             row["kernel_exponent"] == exponent)
                large = next(row for row in rows if
                             row["origin"] == origin and
                             row["scale"] == large_scale and
                             row["Q"] == q0 and
                             row["kernel_exponent"] == exponent)
                for name in LAW_NAMES:
                    e_small = float(small["laws"][name]["energy"])
                    e_large = float(large["laws"][name]["energy"])
                    d_small = float(small["laws"][name]["coordinate_diagonal"])
                    d_large = float(large["laws"][name]["coordinate_diagonal"])
                    growth = e_large / e_small
                    diagonal_growth = d_large / d_small
                    slope = math.log(growth, 2.0)
                    pairs.append({
                        "origin": origin,
                        "Q": q0,
                        "kernel_exponent": exponent,
                        "law": name,
                        "small_scale": small_scale,
                        "large_scale": large_scale,
                        "energy_growth_factor": display(growth),
                        "diagonal_growth_factor": display(diagonal_growth),
                        "energy_log2_slope": display(slope),
                        "small_classification": small["laws"][name][
                            "classification"],
                        "large_classification": large["laws"][name][
                            "classification"],
                        "sign_persistent": (
                            small["laws"][name]["classification"] ==
                            large["laws"][name]["classification"]),
                    })
    all_plus = [item for item in pairs if item["law"] == "all_plus"]
    by_law = {}
    for name in LAW_NAMES:
        selected = [item for item in pairs if item["law"] == name]
        by_law[name] = {
            "pairs": len(selected),
            "sign_persistent_pairs": sum(
                item["sign_persistent"] for item in selected),
            "energy_growth_factor_min": display(min(
                float(item["energy_growth_factor"]) for item in selected)),
            "energy_growth_factor_max": display(max(
                float(item["energy_growth_factor"]) for item in selected)),
            "energy_log2_slope_min": display(min(
                float(item["energy_log2_slope"]) for item in selected)),
            "energy_log2_slope_max": display(max(
                float(item["energy_log2_slope"]) for item in selected)),
        }
    return {
        "small_scale": small_scale,
        "large_scale": large_scale,
        "pairs": len(pairs),
        "all_plus_sign_persistent_pairs": sum(
            item["sign_persistent"] for item in all_plus),
        "all_plus_sign_crossings": sum(
            not item["sign_persistent"] for item in all_plus),
        "all_plus_energy_growth_factor_min": display(min(
            float(item["energy_growth_factor"])
            for item in all_plus)),
        "all_plus_energy_growth_factor_max": display(max(
            float(item["energy_growth_factor"])
            for item in all_plus)),
        "all_plus_energy_log2_slope_min": display(min(
            float(item["energy_log2_slope"]) for item in all_plus)),
        "all_plus_energy_log2_slope_max": display(max(
            float(item["energy_log2_slope"]) for item in all_plus)),
        "by_law": by_law,
        "pairs_detail": pairs,
    }


def placement_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarise the predeclared multi-control placement response spectrum."""
    details: list[dict[str, Any]] = []
    for row in rows:
        for control_name in CONTROL_NAMES:
            control = row["placement_controls"][control_name]
            for law in LAW_NAMES:
                identity = row["laws"][law]
                placed = control["laws"][law]
                identity_ratio = float(identity["ratio"])
                placed_ratio = float(placed["ratio"])
                details.append({
                    "origin": row["origin"], "scale": row["scale"],
                    "Q": row["Q"],
                    "kernel_exponent": row["kernel_exponent"],
                    "control": control_name, "law": law,
                    "identity_ratio": display(identity_ratio),
                    "control_ratio": display(placed_ratio),
                    "absolute_ratio_difference": display(
                        abs(identity_ratio - placed_ratio)),
                    "identity_classification": identity["classification"],
                    "control_classification": placed["classification"],
                    "classification_equal": (
                        identity["classification"] ==
                        placed["classification"]),
                })

    control_summaries: dict[str, Any] = {}
    for control_name in CONTROL_NAMES:
        control = next(row["placement_controls"][control_name]
                       for row in rows)
        selected = [item for item in details
                    if item["control"] == control_name]
        by_law: dict[str, Any] = {}
        census: dict[str, dict[str, int]] = {}
        for law in LAW_NAMES:
            law_rows = [item for item in selected if item["law"] == law]
            census[law] = {
                label: sum(item["control_classification"] == label
                           for item in law_rows)
                for label in LABELS
            }
            by_law[law] = {
                "comparisons": len(law_rows),
                "classification_changed_vs_identity": sum(
                    not item["classification_equal"] for item in law_rows),
                "ratio_min": display(min(
                    float(item["control_ratio"]) for item in law_rows)),
                "ratio_max": display(max(
                    float(item["control_ratio"]) for item in law_rows)),
                "max_abs_ratio_difference": display(max(
                    float(item["absolute_ratio_difference"])
                    for item in law_rows)),
            }
        control_summaries[control_name] = {
            "rule": control["rule"],
            "multiplier": control["multiplier"],
            "offset": control["offset"],
            "bijection": control["bijection"],
            "source_l2_norm_equal_rows": sum(
                row["placement_controls"][control_name][
                    "source_l2_norm_equal"] for row in rows),
            "classification_census": census,
            "by_law": by_law,
        }

    law_spectrum: dict[str, Any] = {}
    for law in LAW_NAMES:
        signatures: Counter[tuple[str, ...]] = Counter()
        ranges: list[float] = []
        for row in rows:
            classes = tuple(row["placement_controls"][control_name][
                "laws"][law]["classification"] for control_name in
                CONTROL_NAMES)
            signatures[classes] += 1
            ratios = [float(row["placement_controls"][control_name][
                "laws"][law]["ratio"]) for control_name in CONTROL_NAMES]
            ranges.append(max(ratios) - min(ratios))
        law_spectrum[law] = {
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
            "ratio_range_min": display(min(ranges)),
            "ratio_range_max": display(max(ranges)),
        }

    pairwise_controls: dict[str, Any] = {}
    for left_index, left in enumerate(CONTROL_NAMES):
        for right in CONTROL_NAMES[left_index + 1:]:
            selected = [item for item in details
                        if item["control"] == right]
            left_rows = {(item["origin"], item["scale"], item["Q"],
                          item["kernel_exponent"], item["law"]): item
                         for item in details if item["control"] == left}
            changes = []
            for item in selected:
                key = (item["origin"], item["scale"], item["Q"],
                       item["kernel_exponent"], item["law"])
                other = left_rows[key]
                changes.append({
                    "classification_changed": (
                        item["control_classification"] !=
                        other["control_classification"]),
                    "ratio_difference": abs(
                        float(item["control_ratio"]) -
                        float(other["control_ratio"])),
                })
            pairwise_controls[f"{left}__{right}"] = {
                "left": left, "right": right,
                "comparisons": len(changes),
                "classification_changes": sum(
                    item["classification_changed"] for item in changes),
                "max_abs_ratio_difference": display(max(
                    item["ratio_difference"] for item in changes)),
            }

    affine_controls = ("affine_3_11", "affine_5_17", "affine_7_29")
    all_plus_affine_positive = 0
    all_plus_affine_same = 0
    identity_reversal_same = 0
    for row in rows:
        affine_classes = [row["placement_controls"][name]["laws"][
            "all_plus"]["classification"] for name in affine_controls]
        if all(item == "POSITIVE_OFF_DIAGONAL" for item in affine_classes):
            all_plus_affine_positive += 1
        if len(set(affine_classes)) == 1:
            all_plus_affine_same += 1
        if (row["placement_controls"]["identity"]["laws"]["all_plus"][
                "classification"] ==
                row["placement_controls"]["reversal"]["laws"][
                    "all_plus"]["classification"]):
            identity_reversal_same += 1

    return {
        "rule": PLACEMENT_RULE,
        "controls": list(CONTROL_NAMES),
        "control_count": len(CONTROL_NAMES),
        "rows": len(rows),
        "law_observations": len(rows) * len(CONTROL_NAMES) * len(LAW_NAMES),
        "comparisons": len(details),
        "source_l2_norm_equal_rows": sum(
            row["placement_controls"][control_name][
                "source_l2_norm_equal"]
            for row in rows for control_name in CONTROL_NAMES),
        "all_plus_affine_positive_rows": all_plus_affine_positive,
        "all_plus_affine_consensus_rows": all_plus_affine_same,
        "all_plus_identity_reversal_same_rows": identity_reversal_same,
        "control_summaries": control_summaries,
        "law_spectrum": law_spectrum,
        "pairwise_controls": pairwise_controls,
        "details": details,
    }


def build_payload(parent_payload: dict[str, Any]) -> dict[str, Any]:
    rows = [row_record(origin, scale, q0, exponent)
            for origin in ORIGINS for scale in SCALES
            for q0 in Q_ANCHORS for exponent in EXPONENTS]
    need(len(rows) == 32, "TPC330 row census")
    class_counts = census(rows)
    expected = {
        "all_plus": {"NEGATIVE_OFF_DIAGONAL": 31,
                     "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
        "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 25,
                              "POSITIVE_OFF_DIAGONAL": 7, "UNRESOLVED": 0},
        "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                           "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "half_split": {"NEGATIVE_OFF_DIAGONAL": 32,
                       "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
    }
    need(class_counts == expected, "held-out law census")
    lambda_ratios = [float(row["component_controls_all_plus"]["lambda"]
                           ["ratio"]) for row in rows]
    comparison_ratios = [float(row["component_controls_all_plus"]["comparison"]
                               ["ratio"]) for row in rows]
    need(min(lambda_ratios) > 1.0 + RATIO_GUARD and
         min(comparison_ratios) > 1.0 + RATIO_GUARD,
         "component control margin")
    summaries = [panel_summary(rows, origin, scale)
                 for origin in ORIGINS for scale in SCALES]
    growth = growth_summary(rows)
    placement = placement_summary(rows)
    need(growth["pairs"] == 64 and
         growth["all_plus_sign_persistent_pairs"] == 15 and
         growth["all_plus_sign_crossings"] == 1 and
         growth["by_law"]["alternating_index"][
             "sign_persistent_pairs"] == 15 and
         growth["by_law"]["mod4_character"][
             "sign_persistent_pairs"] == 16 and
         growth["by_law"]["half_split"][
             "sign_persistent_pairs"] == 16,
         "held-out growth census")
    expected_controls = {
        "identity": {
            "all_plus": {"NEGATIVE_OFF_DIAGONAL": 31,
                         "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
            "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 25,
                                   "POSITIVE_OFF_DIAGONAL": 7,
                                   "UNRESOLVED": 0},
            "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                                "POSITIVE_OFF_DIAGONAL": 0,
                                "UNRESOLVED": 0},
            "half_split": {"NEGATIVE_OFF_DIAGONAL": 32,
                            "POSITIVE_OFF_DIAGONAL": 0,
                            "UNRESOLVED": 0},
        },
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
        "reversal": {
            "all_plus": {"NEGATIVE_OFF_DIAGONAL": 31,
                         "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
            "alternating_index": {"NEGATIVE_OFF_DIAGONAL": 25,
                                   "POSITIVE_OFF_DIAGONAL": 7,
                                   "UNRESOLVED": 0},
            "mod4_character": {"NEGATIVE_OFF_DIAGONAL": 32,
                                "POSITIVE_OFF_DIAGONAL": 0,
                                "UNRESOLVED": 0},
            "half_split": {"NEGATIVE_OFF_DIAGONAL": 32,
                            "POSITIVE_OFF_DIAGONAL": 0,
                            "UNRESOLVED": 0},
        },
    }
    need(placement["comparisons"] == 640 and
         placement["control_count"] == 5 and
         placement["law_observations"] == 640 and
         placement["source_l2_norm_equal_rows"] == 160 and
         placement["all_plus_affine_positive_rows"] == 32 and
         placement["all_plus_affine_consensus_rows"] == 32 and
         placement["all_plus_identity_reversal_same_rows"] == 32 and
         placement["control_summaries"].keys() ==
         expected_controls.keys() and
         {name: placement["control_summaries"][name][
             "classification_census"] for name in CONTROL_NAMES} ==
         expected_controls,
         "multi-permutation response census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC329_producer_sha256": PARENT_CODE_SHA256,
            "TPC329_certificate_sha256": PARENT_RESULT_SHA256,
            "TPC267_V59_producer_sha256": V59_CODE_SHA256,
            "TPC267_V59_certificate_sha256": V59_RESULT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "comparison_cutoff": COMPARISON_CUTOFF,
            "euler_tail_cutoff": TAIL_CUTOFF,
            "source_interval_rule": "I_{o,N}=[o,o+N/2-1]",
            "matrix_entry": (
                "1_{u!=t,p not_divides ut} p H^(2s)/(H^2+(u-t)^2)^s "
                "(1_{u==t mod p}-1/(p-1))"),
            "coherent_operator": "C_e=sum_p e_p B_p",
            "arithmetic_source": "beta_x^(2)(t)=Lambda(t+2)-b_x^(2)(t)",
            "comparison": (
                "b_x^(2)(t)=2 C_2 1_{2 not_divides t} "
                "prod_{p|t,p>2}(p-1)/(p-2)"),
            "tail_enclosure": (
                "finite product through 50000 with lower multiplier "
                "1-1/(50000-1)"),
            "placement_null": {
                "rule": PLACEMENT_RULE,
                "preserves_source_multiset": True,
                "controls": [
                    {"name": name, "multiplier": multiplier,
                     "offset": offset, "rule": rule}
                    for name, multiplier, offset, rule in PLACEMENT_CONTROLS
                ],
            },
            "log_enclosure": "Decimal precision 100 with rational guard 1e-70",
            "ratio_guard": display(RATIO_GUARD, 8),
            "laws": list(LAW_NAMES),
        },
        "exact_theorem": {
            "gram_decomposition": "E_e(v)=D_e(v)+O_e(v)",
            "coordinate_diagonal": (
                "D_e(v)=sum_t v_t^2 sum_u C_e(u,t)^2"),
            "off_diagonal": (
                "O_e(v)=sum_{t!=t'} v_t v_t' sum_u "
                "C_e(u,t) C_e(u,t')"),
            "finite_scope": "Every displayed identity is finite and exact",
            "numerical_scope": (
                "ratio intervals use the declared float64 replay guard; "
                "they are not a growing theorem"),
        },
        "finite_audit": {
            "rows": len(rows),
            "origins": len(ORIGINS),
            "scales": len(SCALES),
            "all_plus_negative_off_diagonal": class_counts["all_plus"][
                "NEGATIVE_OFF_DIAGONAL"],
            "all_plus_positive_off_diagonal": class_counts["all_plus"][
                "POSITIVE_OFF_DIAGONAL"],
            "component_lambda_positive_controls": len(lambda_ratios),
            "component_comparison_positive_controls": len(comparison_ratios),
            "all_plus_ratio_min": display(min(
                float(row["laws"]["all_plus"]["ratio"]) for row in rows)),
            "all_plus_ratio_max": display(max(
                float(row["laws"]["all_plus"]["ratio"]) for row in rows)),
            "lambda_ratio_min": display(min(lambda_ratios)),
            "comparison_ratio_min": display(min(comparison_ratios)),
            "law_census": class_counts,
            "fixed_power_credit": 0,
        },
        "component_control": {
            "lambda": "positive von-Mangoldt component",
            "comparison": "positive twin-prime comparison component",
            "residual": "lambda-minus-comparison source vector",
            "all_plus_lambda_ratio_min": display(min(lambda_ratios)),
            "all_plus_comparison_ratio_min": display(min(comparison_ratios)),
            "both_positive_in_all_rows": True,
        },
        "panel_summaries": summaries,
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC330_EXACT_GRAM_DECOMPOSITION": "PROVED_EXACT_FINITE",
            "TPC330_SOURCE_NATIVE_VECTOR": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC330_COMPONENT_CONTROLS":
                "NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
            "TPC330_SIGN_AT_SCALE_GROWTH": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC330_MULTI_PERMUTATION_SPECTRUM":
                "NUMERICALLY_CERTIFIED_FINITE_5_CONTROLS",
            "TPC330_AFFINE_ALL_PLUS_CONSENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_32_OF_32",
            "TPC330_GROWING_SOURCE_NATIVE_L2": "OPEN",
            "TPC330_ARITHMETIC_ADVANCE": "NO",
            "TPC330_FIXED_POWER_CREDIT": 0,
            "TPC330_FULL_GATE_B": "OPEN",
            "TPC330_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "growth_audit": growth,
        "placement_audit": placement,
        "rows": rows,
    }


def build_document(parent_payload: dict[str, Any]) -> dict[str, Any]:
    payload = build_payload(parent_payload)
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate(parent_payload: dict[str, Any]) -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document(parent_payload)))


def check_certificate(parent_payload: dict[str, Any]) -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "TPC330 certificate canonicality")
    need(stored == build_document(parent_payload),
         "TPC330 certificate does not replay")
    print("TPC330_CERTIFICATE=PASS rows=32 origins=2 scales=2 laws=4 "
          "growth_pairs=64 placement_controls=5 placement_comparisons=640")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        _, parent_payload = load_parent()
        if args.write:
            write_certificate(parent_payload)
            print("TPC330_CERTIFICATE=WRITTEN")
        else:
            check_certificate(parent_payload)
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC330_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
