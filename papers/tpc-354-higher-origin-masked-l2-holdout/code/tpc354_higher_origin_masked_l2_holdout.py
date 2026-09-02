#!/usr/bin/env python3
"""TPC-354: higher-origin holdout for source-native masked L2 polarization.

TPC-353 joined the finite V59 residual to the literal divisibility-masked
operator on a low-origin panel.  This release keeps every formula, shell,
law, count, and exponent fixed while moving to a disjoint higher-origin
holdout.  For

    beta = Lambda - b,       A = sum_p e_p B_p,

it records the exact finite identity

    ||A beta||^2 = ||A Lambda||^2 + ||A b||^2
                   - 2 <A Lambda, A b>.

the resulting polarization coefficient is a finite transfer diagnostic only.
No source-uniform estimate, asymptotic statement, or twin-prime conclusion is
claimed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
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
    raise SystemExit("TPC354 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc354_certificate.json"

PARENT_CODE = ROOT / (
    "papers/tpc-353-source-native-masked-l2-polarization/code/"
    "tpc353_source_native_masked_l2_polarization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-353-source-native-masked-l2-polarization/results/"
    "tpc353_certificate.json")
PARENT_CODE_SHA256 = (
    "2638df53704a08d6f278de7b60ddf472873c69b6eebdbdad172b4c225b2fb7e9")
PARENT_CERT_SHA256 = (
    "bfe0199b687898f3b4bfd5ca4f2b9f645890d6c54fe434b1f2ceaf0ae8c6ef82")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC354_HIGHER_ORIGIN_MASKED_L2_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT"
ROUND2_CLUE = (
    "TEST_POSITION_AWARE_MASKED_BOUND_ORIGIN_SCALE_NORMALIZATION_OR_"
    "CONTROLLED_SIGN_LAW_SUBSPACE")

# This panel keeps TPC-353's protocol fixed but moves to higher, disjoint
# origins.  It remains below the inherited 50,000 source cutoff; counts are
# the actual interval lengths.
ORIGINS = (21001, 23001, 25001)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
LOG_GUARD = Fraction(Decimal("1e-70"))
KAPPA_GUARD = 1.0e-7
IDENTITY_TOL = 2.0e-6
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("POSITIVE_OUTPUT_ALIGNMENT", "NEGATIVE_OUTPUT_ALIGNMENT",
          "UNRESOLVED")

EXACT_INTERVAL = (21001, 21014)
EXACT_Q = 4
EXACT_EXPONENT = 1
EXACT_LEFT = (1, -1, 0, 2, -1, 0, 1, 0, 0, -1, 1, 0, 0, 1)
EXACT_RIGHT = (0, 1, 1, -1, 0, 2, 0, -1, 1, 0, -1, 0, 1, 0)


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


def show(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


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
    return [value for value in range(2, limit + 1) if sieve[value]]


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
    global TAIL_CACHE
    if TAIL_CACHE is None:
        finite = Decimal(1)
        for prime in PRIMES:
            if prime > COMPARISON_CUTOFF:
                finite *= (Decimal((prime - 1) ** 2 - 1) /
                           Decimal((prime - 1) ** 2))
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


def source_vectors(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray,
                                               np.ndarray, float]:
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


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    return {
        "all_plus": np.ones(len(primes), dtype=np.float64),
        "alternating_index": np.asarray(
            [1 if i % 2 == 0 else -1 for i in range(len(primes))],
            dtype=np.float64),
        "mod4_character": np.asarray(
            [1 if prime % 4 == 1 else -1 for prime in primes],
            dtype=np.float64),
        "half_split": np.asarray(
            [1 if i < len(primes) / 2 else -1
             for i in range(len(primes))], dtype=np.float64),
    }


def coherent_matrices(values: np.ndarray, q0: int, exponent: int
                      ) -> tuple[list[int], dict[str, np.ndarray]]:
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrices = {name: np.zeros((len(values), len(values)), dtype=np.float64)
                for name in LAW_NAMES}
    for index, prime in enumerate(primes):
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(prime) * kernel * centered
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block *= valid
        for name in LAW_NAMES:
            matrices[name] += signs[name][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    return primes, matrices


def ratio_label(kappa: float) -> str:
    if kappa > KAPPA_GUARD:
        return "POSITIVE_OUTPUT_ALIGNMENT"
    if kappa < -KAPPA_GUARD:
        return "NEGATIVE_OUTPUT_ALIGNMENT"
    return "UNRESOLVED"


def polarization_record(matrix: np.ndarray, lam: np.ndarray,
                        comp: np.ndarray, residual: np.ndarray,
                        source_kappa: float) -> dict[str, Any]:
    y_lam = matrix @ lam
    y_comp = matrix @ comp
    y_res = matrix @ residual
    energy_lam = float(np.dot(y_lam, y_lam))
    energy_comp = float(np.dot(y_comp, y_comp))
    cross = float(np.dot(y_lam, y_comp))
    energy_res = float(np.dot(y_res, y_res))
    component_sum = energy_lam + energy_comp
    need(energy_lam > 0 and energy_comp > 0 and energy_res > 0 and
         math.isfinite(component_sum), "positive output energies")
    kappa = 2.0 * cross / component_sum
    residual_fraction = energy_res / component_sum
    identity_error = abs(energy_res - (component_sum - 2.0 * cross))
    cauchy_lower = ((math.sqrt(energy_lam) - math.sqrt(energy_comp)) ** 2 /
                    component_sum)
    cauchy_upper = ((math.sqrt(energy_lam) + math.sqrt(energy_comp)) ** 2 /
                    component_sum)
    cosine = cross / math.sqrt(energy_lam * energy_comp)
    need(abs(identity_error) <= IDENTITY_TOL, "output polarization identity")
    need(cauchy_lower - 2e-10 <= residual_fraction <= cauchy_upper + 2e-10,
         "Cauchy envelope")
    need(-1.000001 <= cosine <= 1.000001, "output cosine")
    return {
        "lambda_output_energy": show(energy_lam),
        "comparison_output_energy": show(energy_comp),
        "component_output_energy_sum": show(component_sum),
        "output_cross_inner_product": show(cross),
        "residual_output_energy": show(energy_res),
        "output_polarization_kappa": show(kappa),
        "residual_fraction_of_component_sum": show(residual_fraction),
        "cauchy_lower_fraction": show(cauchy_lower),
        "cauchy_upper_fraction": show(cauchy_upper),
        "output_cosine": show(cosine),
        "identity_error": show(identity_error),
        "classification": ratio_label(kappa),
        "source_polarization_kappa": show(source_kappa),
        "output_minus_source_kappa": show(kappa - source_kappa),
    }


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
    matrix = [[sum((exact_entry(prime, u, t, EXACT_EXPONENT)
                    for prime in primes), Fraction(0))
               for t in values] for u in values]
    left = [Fraction(value) for value in EXACT_LEFT]
    right = [Fraction(value) for value in EXACT_RIGHT]
    residual = [a - b for a, b in zip(left, right)]

    def image(vector: list[Fraction]) -> list[Fraction]:
        return [sum((matrix[i][j] * vector[j]
                     for j in range(len(values))), Fraction(0))
                for i in range(len(values))]

    def energy(vector: list[Fraction]) -> Fraction:
        return sum((item * item for item in image(vector)), Fraction(0))

    left_image, right_image = image(left), image(right)
    residual_image = image(residual)
    left_energy = sum((item * item for item in left_image), Fraction(0))
    right_energy = sum((item * item for item in right_image), Fraction(0))
    cross = sum((a * b for a, b in zip(left_image, right_image)), Fraction(0))
    residual_energy = sum((item * item for item in residual_image), Fraction(0))
    need(residual_energy == left_energy + right_energy - 2 * cross,
         "exact polarization anchor")
    return {
        "interval": list(EXACT_INTERVAL),
        "Q": EXACT_Q,
        "shell": primes,
        "exponent": EXACT_EXPONENT,
        "left_vector": list(EXACT_LEFT),
        "right_vector": list(EXACT_RIGHT),
        "left_energy_digest": fraction_digest(left_energy),
        "right_energy_digest": fraction_digest(right_energy),
        "cross_digest": fraction_digest(cross),
        "residual_energy_digest": fraction_digest(residual_energy),
        "left_energy_decimal": show(float(left_energy), 16),
        "right_energy_decimal": show(float(right_energy), 16),
        "cross_decimal": show(float(cross), 16),
        "residual_energy_decimal": show(float(residual_energy), 16),
        "identity_exact": True,
    }


def row_record(origin: int, count: int, q0: int, exponent: int,
               law: str) -> dict[str, Any]:
    lo, hi = origin, origin + count - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comp, residual, width = source_vectors(lo, hi)
    source_denom = float(np.dot(lam, lam) + np.dot(comp, comp))
    source_kappa = 2.0 * float(np.dot(lam, comp)) / source_denom
    primes, matrices = coherent_matrices(values, q0, exponent)
    metrics = polarization_record(matrices[law], lam, comp, residual,
                                  source_kappa)
    need(metrics["classification"] != "UNRESOLVED",
         "source-native output alignment unresolved")
    return {
        "origin": origin,
        "count": count,
        "source_interval": [lo, hi],
        "source_count": count,
        "Q": q0,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "comparison_cutoff": COMPARISON_CUTOFF,
        "shell": primes,
        "shell_cardinality": len(primes),
        "operator_shape": [count, count],
        "law": law,
        "source_model": "beta_x^(2)(t)=Lambda(t+2)-b_x^(2)(t)",
        "source_weight_max_interval_width": show(width, 8),
        "metrics": metrics,
    }


def row_digest(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical(rows)).hexdigest()


def law_summary(rows: list[dict[str, Any]], law: str) -> dict[str, Any]:
    selected = [row for row in rows if row["law"] == law]
    need(len(selected) == len(ORIGINS) * len(COUNTS) * len(Q_ANCHORS) *
         len(EXPONENTS), "law row census")
    values = [float(row["metrics"]["output_polarization_kappa"])
              for row in selected]
    fractions = [float(row["metrics"]["residual_fraction_of_component_sum"])
                 for row in selected]
    source_values = [float(row["metrics"]["source_polarization_kappa"])
                     for row in selected]
    deltas = [float(row["metrics"]["output_minus_source_kappa"])
              for row in selected]
    cosines = [float(row["metrics"]["output_cosine"]) for row in selected]
    return {
        "rows": len(selected),
        "positive_output_alignment": sum(value > KAPPA_GUARD
                                          for value in values),
        "negative_output_alignment": sum(value < -KAPPA_GUARD
                                          for value in values),
        "kappa_min": show(min(values)),
        "kappa_max": show(max(values)),
        "kappa_mean": show(sum(values) / len(values)),
        "residual_fraction_min": show(min(fractions)),
        "residual_fraction_max": show(max(fractions)),
        "source_kappa_min": show(min(source_values)),
        "source_kappa_max": show(max(source_values)),
        "output_minus_source_min": show(min(deltas)),
        "output_minus_source_max": show(max(deltas)),
        "output_cosine_min": show(min(cosines)),
        "output_cosine_max": show(max(cosines)),
    }


def load_parent_payload() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    need(document.get("certificate_version") == 1, "parent certificate version")
    payload = document.get("payload")
    need(isinstance(payload, dict), "parent certificate payload")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "parent certificate payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("height") == HEIGHT and
         protocol.get("laws") == list(LAW_NAMES),
         "parent protocol compatibility")
    return payload


def holdout_comparison(summaries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    parent = load_parent_payload()
    parent_summaries = parent.get("law_summaries", {})
    need(isinstance(parent_summaries, dict), "parent law summaries")
    comparison: dict[str, Any] = {}
    for law in LAW_NAMES:
        current = summaries[law]
        previous = parent_summaries.get(law, {})
        need(previous.get("rows") == current["rows"] == 54,
             "parent law row census")
        comparison[law] = {
            "parent_kappa_min": previous["kappa_min"],
            "holdout_kappa_min": current["kappa_min"],
            "holdout_minus_parent_kappa_min": show(
                float(current["kappa_min"]) - float(previous["kappa_min"])),
            "parent_kappa_max": previous["kappa_max"],
            "holdout_kappa_max": current["kappa_max"],
            "holdout_minus_parent_kappa_max": show(
                float(current["kappa_max"]) - float(previous["kappa_max"])),
            "parent_kappa_mean": previous["kappa_mean"],
            "holdout_kappa_mean": current["kappa_mean"],
            "holdout_minus_parent_kappa_mean": show(
                float(current["kappa_mean"]) - float(previous["kappa_mean"])),
            "parent_positive_alignment": previous[
                "positive_output_alignment"],
            "holdout_positive_alignment": current[
                "positive_output_alignment"],
        }
    parent_audit = parent.get("finite_audit", {})
    return {
        "parent_release": "TPC-353",
        "parent_certificate_path": str(PARENT_CERT.relative_to(ROOT)),
        "parent_certificate_sha256": PARENT_CERT_SHA256,
        "protocol_difference": "origins_only",
        "parent_origins": parent.get("protocol", {}).get("origins"),
        "holdout_origins": list(ORIGINS),
        "parent_rows": parent_audit.get("rows"),
        "holdout_rows": len(ORIGINS) * len(COUNTS) * len(Q_ANCHORS) *
        len(EXPONENTS) * len(LAW_NAMES),
        "parent_positive_alignment": parent_audit.get(
            "positive_output_alignment"),
        "holdout_positive_alignment": 216,
        "law_summaries": comparison,
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC353 producer provenance")
    need(PARENT_CERT.is_file() and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC353 certificate provenance")
    need(V59_CODE.is_file() and digest(V59_CODE.read_bytes()) == V59_CODE_SHA256,
         "V59 producer provenance")
    need(V59_CERT.is_file() and digest(V59_CERT.read_bytes()) == V59_CERT_SHA256,
         "V59 certificate provenance")
    rows = [row_record(origin, count, q0, exponent, law)
            for origin in ORIGINS for count in COUNTS for q0 in Q_ANCHORS
            for exponent in EXPONENTS for law in LAW_NAMES]
    expected_rows = (len(ORIGINS) * len(COUNTS) * len(Q_ANCHORS) *
                     len(EXPONENTS) * len(LAW_NAMES))
    need(len(rows) == expected_rows == 216, "total row census")
    summaries = {law: law_summary(rows, law) for law in LAW_NAMES}
    need(all(summary["positive_output_alignment"] == summary["rows"]
             for summary in summaries.values()),
         "positive output alignment census")
    source_kappas = [float(row["metrics"]["source_polarization_kappa"])
                     for row in rows]
    output_kappas = [float(row["metrics"]["output_polarization_kappa"])
                     for row in rows]
    deltas = [out - src for out, src in zip(output_kappas, source_kappas)]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC353_code_path": str(PARENT_CODE.relative_to(ROOT)),
            "TPC353_code_sha256": PARENT_CODE_SHA256,
            "TPC353_certificate_path": str(PARENT_CERT.relative_to(ROOT)),
            "TPC353_certificate_sha256": PARENT_CERT_SHA256,
            "V59_code_sha256": V59_CODE_SHA256,
            "V59_certificate_sha256": V59_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "source_counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "source_cutoff": TAIL_CUTOFF,
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked shell operator",
            "source_model": "finite V59 beta=Lambda(t+2)-b^(2)(t) with inherited tail enclosure",
            "panel_scope": "disjoint higher-origin holdout for TPC353 with origins-only protocol change",
        },
        "exact_theorem": {
            "operator_polarization": (
                "For beta=Lambda-b, ||A beta||_2^2 = ||A Lambda||_2^2 "
                "+ ||A b||_2^2 - 2 <A Lambda,A b>"),
            "normalized_coefficient": (
                "kappa_A=2<A Lambda,A b>/(||A Lambda||_2^2+||A b||_2^2)"),
            "residual_fraction": "||A beta||_2^2/(component sum)=1-kappa_A",
            "cauchy_envelope": (
                "(sqrt(E_L)-sqrt(E_b))^2/(E_L+E_b) <= residual fraction "
                "<= (sqrt(E_L)+sqrt(E_b))^2/(E_L+E_b)"),
            "scope": "finite real matrices and the declared finite source model only",
        },
        "finite_audit": {
            "rows": len(rows),
            "origins": len(ORIGINS),
            "source_counts": len(COUNTS),
            "q_anchors": len(Q_ANCHORS),
            "kernel_exponents": len(EXPONENTS),
            "laws": len(LAW_NAMES),
            "positive_output_alignment": len(rows),
            "negative_output_alignment": 0,
            "unresolved": 0,
            "max_identity_error": show(max(
                float(row["metrics"]["identity_error"]) for row in rows)),
            "source_kappa_min": show(min(source_kappas)),
            "source_kappa_max": show(max(source_kappas)),
            "output_kappa_min": show(min(output_kappas)),
            "output_kappa_max": show(max(output_kappas)),
            "output_minus_source_min": show(min(deltas)),
            "output_minus_source_max": show(max(deltas)),
            "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "parent_comparison": holdout_comparison(summaries),
        "law_summaries": summaries,
        "claim_firewall": {
            "TPC354_FINITE_OPERATOR_POLARIZATION": "PROVED_EXACT_FINITE",
            "TPC354_FINITE_CAUCHY_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC354_SOURCE_NATIVE_MODEL": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC354_OPERATOR_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
            "TPC354_POSITIVE_ALIGNMENT": "NUMERICALLY_CERTIFIED_FINITE_216_OF_216",
            "TPC354_HIGHER_ORIGIN_HOLDOUT": "NUMERICALLY_CERTIFIED_FINITE_216_ROWS",
            "TPC354_OUTPUT_SOURCE_MISMATCH": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC354_UNIFORM_L2": "OPEN",
            "TPC354_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC354_ARITHMETIC_ADVANCE": "NO",
            "TPC354_FIXED_POWER_CREDIT": 0,
            "TPC354_FULL_GATE_B": "OPEN",
            "TPC354_TWIN_PRIME_RESULT": "NONE",
            "TPC354_STRONGEST_OBSTRUCTION": (
                "HIGHER_ORIGIN_HOLDOUT_LOWER_FLOOR_THAN_TPC353_PARENT"),
        },
        "exact_anchor": exact_anchor(),
        "row_digest": row_digest(rows),
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write_certificate() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored.get("certificate_version") == 1 and
         stored.get("claim_status") == STATUS, "certificate header")
    payload = stored.get("payload")
    need(isinstance(payload, dict) and
         stored.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload hash")
    need(payload == build_payload(), "certificate does not replay")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            write_certificate()
            print("TPC354_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            print("TPC354_CERTIFICATE=PASS rows=216 positive_alignment=216/216 "
                  "unresolved=0 fixed_power_credit=0")
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError) as error:
        print("TPC354_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
