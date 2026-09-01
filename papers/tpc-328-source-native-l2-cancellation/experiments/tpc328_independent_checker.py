#!/usr/bin/env python3
"""Independent replay for the TPC-328 source-native L2 atlas.

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
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
RATIO_GUARD = 5.0e-8
NUMERIC_TOL = 3.0e-6
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character",
             "half_split")
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")
EXACT_INTERVAL = (20001, 20016)
EXACT_DIRECT_DIGEST = (
    "34a3720cc5edefae7d277fc91ac90846886a54860e76653f57ad5d7ea08241a1")
EXACT_DIAGONAL_DIGEST = (
    "471ba6760b9567f1619c5e1a785c47b727c4b0a78488f9e9337085bbab33b262")
EXACT_OFF_DIGEST = (
    "cc7a9f5f61dea745d57fb30e041decb28a79afac5c383d87838b4d1f57738074")


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
    need(lock["TPC327_producer_sha256"] == PARENT_CODE_SHA256 and
         lock["TPC327_certificate_sha256"] == PARENT_CERT_SHA256 and
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
    locked_parent_checks(payload)

    protocol = payload["protocol"]
    need(protocol["origins"] == list(ORIGINS) and
         protocol["scales"] == list(SCALES) and
         protocol["source_counts"] == [x // 2 for x in SCALES] and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS) and
         protocol["height"] == HEIGHT and
         protocol["comparison_cutoff"] == COMPARISON_CUTOFF and
         protocol["euler_tail_cutoff"] == TAIL_CUTOFF, "protocol")

    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 96, "row census")
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
    need(counts == expected and lambda_positive == 96 and
         comparison_positive == 96, "census/control summary")
    audit = payload["finite_audit"]
    need(audit["rows"] == 96 and audit["origins"] == 3 and
         audit["scales"] == 4 and
         audit["all_plus_negative_off_diagonal"] == 81 and
         audit["all_plus_positive_off_diagonal"] == 15 and
         audit["component_lambda_positive_controls"] == 96 and
         audit["component_comparison_positive_controls"] == 96 and
         audit["fixed_power_credit"] == 0, "audit firewall")

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
    need(firewall["TPC328_EXACT_GRAM_DECOMPOSITION"] ==
         "PROVED_EXACT_FINITE" and
         firewall["TPC328_SOURCE_NATIVE_VECTOR"] ==
         "PROVED_EXACT_FINITE_DECLARED_MODEL" and
         firewall["TPC328_COMPONENT_CONTROLS"] ==
         "NUMERICALLY_CERTIFIED_FINITE_96_OF_96" and
         firewall["TPC328_ALL_PLUS_CANCELLATION"] ==
         "NUMERICALLY_CERTIFIED_FINITE_81_OF_96" and
         firewall["TPC328_ALL_PLUS_OBSTRUCTION"] ==
         "NUMERICALLY_CERTIFIED_FINITE_15_OF_96" and
         firewall["TPC328_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC328_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC328_GROWING_SOURCE_NATIVE_L2"] == "OPEN" and
         firewall["TPC328_FULL_GATE_B"] == "OPEN" and
         firewall["TPC328_TWIN_PRIME_RESULT"] == "NONE", "claim firewall")
    print("TPC328_INDEPENDENT_CHECK=PASS rows=96 laws=4 "
          "all_plus_negative=81 all_plus_positive=15 components=96/96 "
          "exact_anchor=1")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError, np.linalg.LinAlgError) as error:
        print("TPC328_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
