#!/usr/bin/env python3
"""TPC-328: a source-native arithmetic L2 cancellation atlas.

TPC-327 established a finite three-origin profile triangulation but did not
put the twin-prime residual into the operator.  This release does exactly
that.  For the literal deleted-diagonal prime-shell blocks B_p, it forms

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
    raise SystemExit("TPC328 requires numpy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc328_certificate.json"

PARENT_PROJECT = ROOT / "papers/tpc-327-three-origin-scale-triangulation"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc327_three_origin_scale_triangulation.py")
PARENT_RESULT = PARENT_PROJECT / "results/tpc327_certificate.json"
PARENT_CODE_SHA256 = (
    "ddb5117b4533608a0f1ffb510f901d02d53ea6158c08d921aeced4f0c1653f47")
PARENT_RESULT_SHA256 = (
    "1550f36b41c71dc09d68f220658a3fdf12f52822a4fd13fcebcf7aefea0f403f")

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

SCHEMA = "TPC328_SOURCE_NATIVE_L2_CANCELLATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_NATIVE_L2_CANCELLATION_ATLAS"
ROUND2_CLUE = (
    "TEST_SOURCE_NATIVE_L2_ON_GROWING_ORIGIN_ENSEMBLE_OR_"
    "PROVE_SIGNED_GRAM_BOUND")

ORIGINS = (12001, 16001, 20001)
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
LOG_GUARD = Fraction(Decimal("1e-70"))
RATIO_GUARD = 5.0e-8
RATIO_TOL = 1.0e-6
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")

EXACT_INTERVAL = (20001, 20016)
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
         "TPC327 producer provenance")
    need(PARENT_RESULT.is_file() and
         digest(PARENT_RESULT.read_bytes()) == PARENT_RESULT_SHA256,
         "TPC327 certificate provenance")
    raw = PARENT_RESULT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "TPC327 certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION",
         "TPC327 certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict), "TPC327 payload type")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("source_scales") == list(SCALES) and
         protocol.get("Q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("height") == HEIGHT, "TPC327 protocol lock")

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


def build_payload(parent_payload: dict[str, Any]) -> dict[str, Any]:
    rows = [row_record(origin, scale, q0, exponent)
            for origin in ORIGINS for scale in SCALES
            for q0 in Q_ANCHORS for exponent in EXPONENTS]
    need(len(rows) == 96, "TPC328 row census")
    class_counts = census(rows)
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
    need(class_counts == expected, "source-native law census")
    lambda_ratios = [float(row["component_controls_all_plus"]["lambda"]
                           ["ratio"]) for row in rows]
    comparison_ratios = [float(row["component_controls_all_plus"]["comparison"]
                               ["ratio"]) for row in rows]
    need(min(lambda_ratios) > 1.0 + RATIO_GUARD and
         min(comparison_ratios) > 1.0 + RATIO_GUARD,
         "component control margin")
    summaries = [panel_summary(rows, origin, scale)
                 for origin in ORIGINS for scale in SCALES]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "TPC327_producer_sha256": PARENT_CODE_SHA256,
            "TPC327_certificate_sha256": PARENT_RESULT_SHA256,
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
            "TPC328_EXACT_GRAM_DECOMPOSITION": "PROVED_EXACT_FINITE",
            "TPC328_SOURCE_NATIVE_VECTOR": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC328_COMPONENT_CONTROLS":
                "NUMERICALLY_CERTIFIED_FINITE_96_OF_96",
            "TPC328_ALL_PLUS_CANCELLATION":
                "NUMERICALLY_CERTIFIED_FINITE_81_OF_96",
            "TPC328_ALL_PLUS_OBSTRUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_15_OF_96",
            "TPC328_NO_UNIFORM_SIGNED_CONTRACTION":
                "REFUTED_SCOPED_FOUR_DECLARED_LAWS",
            "TPC328_ARITHMETIC_ADVANCE": "NO",
            "TPC328_FIXED_POWER_CREDIT": 0,
            "TPC328_GROWING_SOURCE_NATIVE_L2": "OPEN",
            "TPC328_FULL_GATE_B": "OPEN",
            "TPC328_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
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
    need(raw == canonical(stored), "TPC328 certificate canonicality")
    need(stored == build_document(parent_payload),
         "TPC328 certificate does not replay")
    print("TPC328_CERTIFICATE=PASS rows=96 origins=3 laws=4 "
          "all_plus_negative=81 all_plus_positive=15 components=96/96")


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
            print("TPC328_CERTIFICATE=WRITTEN")
        else:
            check_certificate(parent_payload)
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC328_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
