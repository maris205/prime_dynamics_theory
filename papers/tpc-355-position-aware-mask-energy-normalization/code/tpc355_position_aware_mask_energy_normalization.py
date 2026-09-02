#!/usr/bin/env python3
"""TPC-355: position-aware mask-energy normalization audit.

TPC-354 showed that the finite source/operator polarization survives a
higher-origin holdout but its all-plus floor moves.  This release freezes a
response-independent diagonal preconditioner before replaying three panels:

    G_i = sum_{p in S_Q} sum_{t in I} B_p(i,t)^2,
    A^# = D_G^{-1/2} A D_G^{-1/2},  D_G = diag(G_i),

where B_p is the unsigned literal masked prime component.  The normalization
uses neither a source vector nor an observed response.  All statements remain
finite declared-model statements or numerically certified finite observations;
no asymptotic estimate or twin-prime conclusion is asserted.
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
    raise SystemExit("TPC355 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc355_certificate.json"

PARENT_354_CODE = ROOT / (
    "papers/tpc-354-higher-origin-masked-l2-holdout/code/"
    "tpc354_higher_origin_masked_l2_holdout.py")
PARENT_354_CERT = ROOT / (
    "papers/tpc-354-higher-origin-masked-l2-holdout/results/"
    "tpc354_certificate.json")
PARENT_353_CODE = ROOT / (
    "papers/tpc-353-source-native-masked-l2-polarization/code/"
    "tpc353_source_native_masked_l2_polarization.py")
PARENT_353_CERT = ROOT / (
    "papers/tpc-353-source-native-masked-l2-polarization/results/"
    "tpc353_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")

PARENT_354_CODE_SHA256 = (
    "effb33810ea773467c367679b9a7bf755b626b4759d812c916336cb226877aed")
PARENT_354_CERT_SHA256 = (
    "033be8d4e2b2f977975a35f014b564ed0f7523578ec2909eb66405fa789e4ceb")
PARENT_353_CODE_SHA256 = (
    "2638df53704a08d6f278de7b60ddf472873c69b6eebdbdad172b4c225b2fb7e9")
PARENT_353_CERT_SHA256 = (
    "bfe0199b687898f3b4bfd5ca4f2b9f645890d6c54fe434b1f2ceaf0ae8c6ef82")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC355_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_POSITION_AWARE_MASK_ENERGY_NORMALIZATION_AUDIT"
ROUND2_CLUE = (
    "TEST_ADVERSARIAL_POSITION_NORMALIZATION_OR_LAW_INVARIANT_BOUND_ON_"
    "FRESH_ORIGINS")

PANEL_NAMES = ("low_parent", "higher_parent", "fresh_holdout")
ORIGINS_BY_PANEL = {
    "low_parent": (6001, 8001, 10001),
    "higher_parent": (21001, 23001, 25001),
    "fresh_holdout": (29001, 33001, 37001),
}
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
LOG_GUARD = Fraction(Decimal("1e-70"))
KAPPA_GUARD = 1.0e-7
IDENTITY_TOL = 4.0e-6
PARENT_TOL = 8.0e-6
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")

EXACT_INTERVAL = (29001, 29014)
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


def comparison_tail() -> tuple[Fraction, Fraction]:
    finite = Decimal(1)
    for prime in PRIMES:
        if prime > COMPARISON_CUTOFF:
            finite *= (Decimal((prime - 1) ** 2 - 1) /
                       Decimal((prime - 1) ** 2))
    lower = finite * (1 - Decimal(1) / Decimal(TAIL_CUTOFF - 1))
    return Fraction(lower), Fraction(finite)


TAIL_INTERVAL: tuple[Fraction, Fraction] | None = None


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
    global TAIL_INTERVAL
    if value % 2 == 0:
        return Fraction(0), Fraction(0)
    if TAIL_INTERVAL is None:
        TAIL_INTERVAL = comparison_tail()
    lower, upper = TAIL_INTERVAL
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
            [1.0 if i % 2 == 0 else -1.0 for i in range(len(primes))]),
        "mod4_character": np.asarray(
            [1.0 if prime % 4 == 1 else -1.0 for prime in primes]),
        "half_split": np.asarray(
            [1.0 if i < len(primes) / 2 else -1.0
             for i in range(len(primes))]),
    }


def component_matrices(values: np.ndarray, q0: int, exponent: int
                       ) -> tuple[list[int], dict[str, np.ndarray], np.ndarray]:
    differences = values[:, None] - values[None, :]
    distance = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell_for(q0)
    signs = sign_patterns(primes)
    matrices = {name: np.zeros((len(values), len(values)), dtype=np.float64)
                for name in LAW_NAMES}
    geometry = np.zeros(len(values), dtype=np.float64)
    for index, prime in enumerate(primes):
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        block = float(prime) * kernel * centered
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block *= valid
        geometry += np.sum(block * block, axis=1)
        for name in LAW_NAMES:
            matrices[name] += signs[name][index] * block
    for matrix in matrices.values():
        matrix[:] = (matrix + matrix.T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "positive unsigned mask-energy diagonal")
    return primes, matrices, geometry


def polarization(matrix: np.ndarray, lam: np.ndarray, comp: np.ndarray,
                 residual: np.ndarray, source_kappa: float
                 ) -> dict[str, Any]:
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
    fraction = energy_res / component_sum
    lower = ((math.sqrt(energy_lam) - math.sqrt(energy_comp)) ** 2 /
             component_sum)
    upper = ((math.sqrt(energy_lam) + math.sqrt(energy_comp)) ** 2 /
             component_sum)
    cosine = cross / math.sqrt(energy_lam * energy_comp)
    identity_error = abs(energy_res - component_sum + 2.0 * cross)
    need(identity_error <= IDENTITY_TOL, "finite polarization identity")
    need(lower - 2e-10 <= fraction <= upper + 2e-10,
         "finite Cauchy envelope")
    need(-1.000001 <= cosine <= 1.000001, "finite output cosine")
    label = ("POSITIVE_OUTPUT_ALIGNMENT" if kappa > KAPPA_GUARD else
             "NEGATIVE_OUTPUT_ALIGNMENT" if kappa < -KAPPA_GUARD else
             "UNRESOLVED")
    return {
        "lambda_output_energy": show(energy_lam),
        "comparison_output_energy": show(energy_comp),
        "component_output_energy_sum": show(component_sum),
        "output_cross_inner_product": show(cross),
        "residual_output_energy": show(energy_res),
        "output_polarization_kappa": show(kappa),
        "residual_fraction_of_component_sum": show(fraction),
        "cauchy_lower_fraction": show(lower),
        "cauchy_upper_fraction": show(upper),
        "output_cosine": show(cosine),
        "identity_error": show(identity_error),
        "classification": label,
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
    geometry = [sum((exact_entry(prime, u, t, EXACT_EXPONENT) ** 2
                     for prime in primes for t in values), Fraction(0))
                for u in values]
    need(all(value > 0 for value in geometry), "exact anchor geometry")
    left = [Fraction(value) for value in EXACT_LEFT]
    right = [Fraction(value) for value in EXACT_RIGHT]

    def image(vector: list[Fraction]) -> list[Fraction]:
        return [sum((matrix[i][j] * vector[j]
                     for j in range(len(values))), Fraction(0))
                for i in range(len(values))]

    left_image, right_image = image(left), image(right)
    residual_image = [a - b for a, b in zip(left_image, right_image)]
    left_energy = sum((item * item for item in left_image), Fraction(0))
    right_energy = sum((item * item for item in right_image), Fraction(0))
    cross = sum((a * b for a, b in zip(left_image, right_image)), Fraction(0))
    residual_energy = sum((item * item for item in residual_image), Fraction(0))
    need(residual_energy == left_energy + right_energy - 2 * cross,
         "exact anchor polarization")
    geometry_digest = hashlib.sha256(canonical([
        f"{value.numerator}/{value.denominator}" for value in geometry
    ])).hexdigest()
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
        "geometry_digest": geometry_digest,
        "geometry_positive": True,
        "identity_exact": True,
    }


def row_record(panel: str, origin: int, count: int, q0: int,
               exponent: int, law: str) -> dict[str, Any]:
    lo, hi = origin, origin + count - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comp, residual, width = source_vectors(lo, hi)
    source_denom = float(np.dot(lam, lam) + np.dot(comp, comp))
    source_kappa = 2.0 * float(np.dot(lam, comp)) / source_denom
    primes, matrices, geometry = component_matrices(values, q0, exponent)
    normalized = matrices[law] / np.sqrt(geometry[:, None] * geometry[None, :])
    return {
        "panel": panel,
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
        "unsigned_geometry_energy_min": show(float(np.min(geometry))),
        "unsigned_geometry_energy_max": show(float(np.max(geometry))),
        "raw_metrics": polarization(matrices[law], lam, comp, residual,
                                     source_kappa),
        "normalized_metrics": polarization(normalized, lam, comp, residual,
                                             source_kappa),
    }


def row_digest(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical(rows)).hexdigest()


def summarize(rows: list[dict[str, Any]], panel: str, law: str,
              metric_name: str) -> dict[str, Any]:
    selected = [row for row in rows if row["panel"] == panel and
                row["law"] == law]
    need(len(selected) == 54, f"{panel}/{law}/{metric_name} row census")
    values = [float(row[metric_name]["output_polarization_kappa"])
              for row in selected]
    fractions = [float(row[metric_name]["residual_fraction_of_component_sum"])
                 for row in selected]
    return {
        "rows": len(values),
        "positive_alignment": sum(value > KAPPA_GUARD for value in values),
        "negative_alignment": sum(value < -KAPPA_GUARD for value in values),
        "unresolved": sum(abs(value) <= KAPPA_GUARD for value in values),
        "kappa_min": show(min(values)),
        "kappa_max": show(max(values)),
        "kappa_mean": show(sum(values) / len(values)),
        "residual_fraction_min": show(min(fractions)),
        "residual_fraction_max": show(max(fractions)),
    }


def all_summaries(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    return {panel: {law: {metric: summarize(rows, panel, law, metric)
                          for metric in ("raw_metrics", "normalized_metrics")}
                    for law in LAW_NAMES}
            for panel in PANEL_NAMES}


def load_parent(path: Path, expected_digest: str, label: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_digest, label + " digest")
    document = json.loads(raw)
    need(raw == canonical(document), label + " canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict), label + " payload")
    return payload


def close(actual: float, recorded: Any, label: str,
          tolerance: float = PARENT_TOL) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise CheckFailure(label + " is not numeric") from error
    need(math.isfinite(actual) and math.isfinite(target), label + " nonfinite")
    need(abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


def parent_comparison(summaries: dict[str, dict[str, dict[str, Any]]]
                      ) -> dict[str, Any]:
    parents = (
        ("low_parent", PARENT_353_CERT, PARENT_353_CERT_SHA256,
         "TPC-353", [6001, 8001, 10001]),
        ("higher_parent", PARENT_354_CERT, PARENT_354_CERT_SHA256,
         "TPC-354", [21001, 23001, 25001]),
    )
    result: dict[str, Any] = {}
    for panel, path, expected, release, origins in parents:
        parent = load_parent(path, expected, release + " certificate")
        protocol = parent.get("protocol", {})
        need(protocol.get("origins") == origins and
             protocol.get("source_counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("laws") == list(LAW_NAMES),
             release + " protocol compatibility")
        previous = parent.get("law_summaries", {})
        result[panel] = {"release": release,
                         "certificate_path": str(path.relative_to(ROOT)),
                         "certificate_sha256": expected,
                         "origins": origins, "raw": {}}
        for law in LAW_NAMES:
            old = previous.get(law, {})
            current = summaries[panel][law]["raw_metrics"]
            need(old.get("rows") == 54, release + "/" + law + " rows")
            for field in ("kappa_min", "kappa_max", "kappa_mean"):
                close(float(current[field]), old.get(field),
                      release + "/" + law + "/" + field)
            result[panel]["raw"][law] = {
                "parent_kappa_min": old["kappa_min"],
                "parent_kappa_max": old["kappa_max"],
                "parent_kappa_mean": old["kappa_mean"],
                "replay_kappa_min": current["kappa_min"],
                "replay_kappa_max": current["kappa_max"],
                "replay_kappa_mean": current["kappa_mean"],
                "within_tolerance": True,
            }
    return result


def transfer_summary(summaries: dict[str, dict[str, dict[str, Any]]]
                     ) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for law in LAW_NAMES:
        result[law] = {}
        for metric in ("raw_metrics", "normalized_metrics"):
            low = summaries["low_parent"][law][metric]
            high = summaries["higher_parent"][law][metric]
            fresh = summaries["fresh_holdout"][law][metric]
            result[law][metric] = {
                "higher_minus_low_min": show(
                    float(high["kappa_min"]) - float(low["kappa_min"])),
                "higher_minus_low_max": show(
                    float(high["kappa_max"]) - float(low["kappa_max"])),
                "higher_minus_low_mean": show(
                    float(high["kappa_mean"]) - float(low["kappa_mean"])),
                "fresh_minus_higher_min": show(
                    float(fresh["kappa_min"]) - float(high["kappa_min"])),
                "fresh_minus_higher_max": show(
                    float(fresh["kappa_max"]) - float(high["kappa_max"])),
                "fresh_minus_higher_mean": show(
                    float(fresh["kappa_mean"]) - float(high["kappa_mean"])),
            }
    low_raw = summaries["low_parent"]["all_plus"]["raw_metrics"]
    high_raw = summaries["higher_parent"]["all_plus"]["raw_metrics"]
    fresh_raw = summaries["fresh_holdout"]["all_plus"]["raw_metrics"]
    low_norm = summaries["low_parent"]["all_plus"]["normalized_metrics"]
    high_norm = summaries["higher_parent"]["all_plus"]["normalized_metrics"]
    fresh_norm = summaries["fresh_holdout"]["all_plus"]["normalized_metrics"]
    raw_drop = float(low_raw["kappa_min"]) - float(high_raw["kappa_min"])
    norm_drop = float(low_norm["kappa_min"]) - float(high_norm["kappa_min"])
    need(raw_drop > 0 and norm_drop > 0 and norm_drop < raw_drop,
         "declared all-plus partial floor repair")
    return {
        "law_transfers": result,
        "all_plus_floor": {
            "raw_low_min": low_raw["kappa_min"],
            "raw_higher_min": high_raw["kappa_min"],
            "raw_fresh_min": fresh_raw["kappa_min"],
            "normalized_low_min": low_norm["kappa_min"],
            "normalized_higher_min": high_norm["kappa_min"],
            "normalized_fresh_min": fresh_norm["kappa_min"],
            "raw_higher_drop": show(raw_drop),
            "normalized_higher_drop": show(norm_drop),
            "drop_reduction_fraction": show(1.0 - norm_drop / raw_drop),
            "raw_fresh_minus_higher": show(
                float(fresh_raw["kappa_min"]) - float(high_raw["kappa_min"])),
            "normalized_fresh_minus_higher": show(
                float(fresh_norm["kappa_min"]) - float(high_norm["kappa_min"])),
        },
        "all_plus_mean": {
            "raw_higher_drop": show(
                float(low_raw["kappa_mean"]) - float(high_raw["kappa_mean"])),
            "normalized_higher_drop": show(
                float(low_norm["kappa_mean"]) - float(high_norm["kappa_mean"])),
            "raw_fresh_minus_higher": show(
                float(fresh_raw["kappa_mean"]) - float(high_raw["kappa_mean"])),
            "normalized_fresh_minus_higher": show(
                float(fresh_norm["kappa_mean"]) - float(high_norm["kappa_mean"])),
        },
    }


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
            (PARENT_354_CODE, PARENT_354_CODE_SHA256, "TPC354 code"),
            (PARENT_354_CERT, PARENT_354_CERT_SHA256, "TPC354 certificate"),
            (PARENT_353_CODE, PARENT_353_CODE_SHA256, "TPC353 code"),
            (PARENT_353_CERT, PARENT_353_CERT_SHA256, "TPC353 certificate"),
            (V59_CODE, V59_CODE_SHA256, "V59 code"),
            (V59_CERT, V59_CERT_SHA256, "V59 certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    rows = [row_record(panel, origin, count, q0, exponent, law)
            for panel in PANEL_NAMES for origin in ORIGINS_BY_PANEL[panel]
            for count in COUNTS for q0 in Q_ANCHORS
            for exponent in EXPONENTS for law in LAW_NAMES]
    need(len(rows) == 648, "total row census")
    summaries = all_summaries(rows)
    values = {metric: [float(row[metric]["output_polarization_kappa"])
                       for row in rows]
              for metric in ("raw_metrics", "normalized_metrics")}
    counts = {
        metric: {
            "positive": sum(value > KAPPA_GUARD for value in vals),
            "negative": sum(value < -KAPPA_GUARD for value in vals),
            "unresolved": sum(abs(value) <= KAPPA_GUARD for value in vals),
        } for metric, vals in values.items()
    }
    identity_max = max(float(row[metric]["identity_error"])
                       for row in rows
                       for metric in ("raw_metrics", "normalized_metrics"))
    geometry_values = [float(row["unsigned_geometry_energy_min"])
                       for row in rows]
    geometry_maxima = [float(row["unsigned_geometry_energy_max"])
                       for row in rows]
    need(counts["raw_metrics"] == {"positive": 647, "negative": 1,
                                   "unresolved": 0}, "raw alignment census")
    need(counts["normalized_metrics"] == {"positive": 647, "negative": 1,
                                           "unresolved": 0},
         "normalized alignment census")
    comparison = parent_comparison(summaries)
    transfer = transfer_summary(summaries)
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC354_code_sha256": PARENT_354_CODE_SHA256,
            "TPC354_certificate_sha256": PARENT_354_CERT_SHA256,
            "TPC353_code_sha256": PARENT_353_CODE_SHA256,
            "TPC353_certificate_sha256": PARENT_353_CERT_SHA256,
            "V59_code_sha256": V59_CODE_SHA256,
            "V59_certificate_sha256": V59_CERT_SHA256,
        },
        "protocol": {
            "panel_names": list(PANEL_NAMES),
            "origins_by_panel": {key: list(value)
                                 for key, value in ORIGINS_BY_PANEL.items()},
            "source_counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "source_cutoff": TAIL_CUTOFF,
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked shell operator",
            "source_model": "finite V59 beta=Lambda(t+2)-b^(2)(t) with inherited tail enclosure",
            "normalization": {
                "name": "unsigned_mask_energy_symmetric_congruence",
                "component": "B_p(u,t)=p*K_s(u-t)*(1_(p|u-t)-1/(p-1))*endpoint_masks",
                "geometry_energy": "G_u=sum_(p in S_Q) sum_(t in I) B_p(u,t)^2",
                "normalized_operator": "A_hash=D_G^(-1/2) A D_G^(-1/2)",
                "response_independent": True,
                "source_independent": True,
                "sign_law_independent": True,
            },
            "panel_scope": "TPC353/TPC354 locked panels plus disjoint fresh origins-only holdout",
        },
        "exact_theorem": {
            "geometry_positivity": "For every declared finite row, G_u is a finite sum of nonnegative terms and the audited diagonal is positive.",
            "diagonal_congruence": "For D_G=diag(G_u)>0, A_hash=D_G^(-1/2) A D_G^(-1/2) is a well-defined finite real matrix.",
            "operator_polarization": "For beta=Lambda-b and either A or A_hash, ||T beta||_2^2=||T Lambda||_2^2+||T b||_2^2-2<T Lambda,T b>.",
            "normalized_cauchy_envelope": "The finite Cauchy envelope applies to either operator after the diagonal congruence.",
            "scope": "finite real matrices and the declared finite source model only",
        },
        "finite_audit": {
            "rows": 648,
            "panels": 3,
            "rows_per_panel": 216,
            "raw_positive_alignment": counts["raw_metrics"]["positive"],
            "raw_negative_alignment": counts["raw_metrics"]["negative"],
            "raw_unresolved": counts["raw_metrics"]["unresolved"],
            "normalized_positive_alignment": counts["normalized_metrics"]["positive"],
            "normalized_negative_alignment": counts["normalized_metrics"]["negative"],
            "normalized_unresolved": counts["normalized_metrics"]["unresolved"],
            "max_identity_error": show(identity_max),
            "geometry_energy_min": show(min(geometry_values)),
            "geometry_energy_max": show(max(geometry_maxima)),
            "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "panel_summaries": summaries,
        "parent_comparison": comparison,
        "transfer_summary": transfer,
        "claim_firewall": {
            "TPC355_GEOMETRY_DEFINITION": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC355_DIAGONAL_CONGRUENCE": "PROVED_EXACT_FINITE",
            "TPC355_OPERATOR_POLARIZATION": "PROVED_EXACT_FINITE",
            "TPC355_PANEL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
            "TPC355_RAW_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
            "TPC355_NORMALIZED_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_648_ROWS",
            "TPC355_ALL_PLUS_FLOOR_REPAIR": "NUMERICALLY_CERTIFIED_FINITE_PARTIAL",
            "TPC355_ALL_PLUS_MEAN_REPAIR": "REFUTED_SCOPED",
            "TPC355_ALL_LAW_POSITIVE_ALIGNMENT": "REFUTED_SCOPED",
            "TPC355_SOURCE_UNIFORM_L2": "OPEN",
            "TPC355_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC355_ARITHMETIC_ADVANCE": "NO",
            "TPC355_FIXED_POWER_CREDIT": 0,
            "TPC355_FULL_GATE_B": "OPEN",
            "TPC355_TWIN_PRIME_RESULT": "NONE",
            "TPC355_STRONGEST_POSITIVE": "ALL_PLUS_FLOOR_DROP_PARTIALLY_REDUCED_BY_RESPONSE_INDEPENDENT_NORMALIZATION",
            "TPC355_STRONGEST_OBSTRUCTION": "FRESH_MOD4_NEGATIVE_ROW_AND_MEAN_REPAIR_FAILURE",
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
            print("TPC355_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            print("TPC355_CERTIFICATE=PASS rows=648 raw_positive=647/648 "
                  "normalized_positive=647/648 fixed_power_credit=0")
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError) as error:
        print("TPC355_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
