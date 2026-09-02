#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-354.

This checker does not import the TPC-354 producer.  It rebuilds the V59 source
midpoints, the literal endpoint-masked matrices, all four sign laws, and every
operator-polarization metric.  Shells are accumulated in reverse order to vary
the floating-point path; the locked TPC-353 certificate is checked separately
as the parent for the origins-only transfer comparison.
"""

from __future__ import annotations

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

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 100

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-354-higher-origin-masked-l2-holdout"
CERTIFICATE = PROJECT / "results/tpc354_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-353-source-native-masked-l2-polarization/code/"
    "tpc353_source_native_masked_l2_polarization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-353-source-native-masked-l2-polarization/results/"
    "tpc353_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERT = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")
PARENT_CODE_SHA256 = (
    "2638df53704a08d6f278de7b60ddf472873c69b6eebdbdad172b4c225b2fb7e9")
PARENT_CERT_SHA256 = (
    "bfe0199b687898f3b4bfd5ca4f2b9f645890d6c54fe434b1f2ceaf0ae8c6ef82")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

SCHEMA = "TPC354_HIGHER_ORIGIN_MASKED_L2_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_HIGHER_ORIGIN_MASKED_L2_HOLDOUT"
ORIGINS = (21001, 23001, 25001)
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
KAPPA_GUARD = 1.0e-7
NUMERIC_TOL = 8.0e-6
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
EXACT_INTERVAL = (21001, 21014)
EXACT_LEFT = (1, -1, 0, 2, -1, 0, 1, 0, 0, -1, 1, 0, 0, 1)
EXACT_RIGHT = (0, 1, 1, -1, 0, 2, 0, -1, 1, 0, -1, 0, 1, 0)
EXACT_LEFT_DIGEST = (
    "70d45bec53471bb116856860de853d15c7666cae6be1d6360574f71ee29db40f")
EXACT_RIGHT_DIGEST = (
    "3f5a65b4c64101f74d3cf99316d173bd5a3374cb0b67e9787764c36aa8426f1f")
EXACT_CROSS_DIGEST = (
    "5e71cbdb8ab17c9e8a8fb03c7cca88aae1a9e384e4749b6123154f731d3c1b86")
EXACT_RESIDUAL_DIGEST = (
    "d117b15bf976101f433adca036eba30c473970ac388ee1a359bdb7d00aebae4b")


class Failure(RuntimeError):
    pass


class DuplicateKey(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


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
    need(isinstance(value, dict), "certificate object")
    need(raw == canonical(value), "certificate canonicality")
    return raw, value


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


TAIL_PRIMES = primes_up_to(TAIL_CUTOFF)
SHELL_PRIMES = primes_up_to(2 * max(Q_ANCHORS))
TAIL_CENTER: Decimal | None = None


def shell(q0: int) -> list[int]:
    return [prime for prime in SHELL_PRIMES if q0 < prime <= 2 * q0]


def distinct_factors(value: int) -> list[int]:
    remaining = value
    factors: list[int] = []
    for prime in TAIL_PRIMES:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            factors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 1:
        factors.append(remaining)
    return factors


def prime_power_base(value: int) -> int | None:
    factors = distinct_factors(value)
    if len(factors) != 1:
        return None
    base = factors[0]
    power = base
    while power < value:
        power *= base
    return base if power == value else None


def comparison_midpoint(value: int) -> float:
    global TAIL_CENTER
    if value % 2 == 0:
        return 0.0
    if TAIL_CENTER is None:
        finite = Decimal(1)
        for prime in TAIL_PRIMES:
            if prime > COMPARISON_CUTOFF:
                finite *= (Decimal((prime - 1) ** 2 - 1) /
                           Decimal((prime - 1) ** 2))
        lower = finite * (1 - Decimal(1) / Decimal(TAIL_CUTOFF - 1))
        TAIL_CENTER = (lower + finite) / Decimal(2)
    local = Decimal(2)
    for prime in distinct_factors(value):
        if prime > COMPARISON_CUTOFF:
            local *= Decimal(prime - 1) / Decimal(prime - 2)
    return float(TAIL_CENTER * local)


def lambda_value(value: int) -> float:
    base = prime_power_base(value)
    return 0.0 if base is None else float(Decimal(base).ln())


def source_vectors(origin: int, count: int
                   ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lambdas = [lambda_value(t + 2) for t in range(origin, origin + count)]
    comparisons = [comparison_midpoint(t)
                   for t in range(origin, origin + count)]
    lam = np.asarray(lambdas, dtype=np.float64)
    comp = np.asarray(comparisons, dtype=np.float64)
    return lam, comp, lam - comp


def signs(primes: list[int]) -> dict[str, np.ndarray]:
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


def matrices(origin: int, count: int, q0: int, exponent: int
             ) -> tuple[list[int], dict[str, np.ndarray]]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    delta = values[:, None] - values[None, :]
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + delta.astype(np.float64) ** 2) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    sign_map = signs(primes)
    result = {name: np.zeros((count, count), dtype=np.float64)
              for name in LAW_NAMES}
    for index, prime in reversed(list(enumerate(primes))):
        centered = ((delta % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((delta != 0) & (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = float(prime) * kernel * centered * valid
        for name in LAW_NAMES:
            result[name] += sign_map[name][index] * block
    for name in LAW_NAMES:
        result[name] = (result[name] + result[name].T) / 2.0
    return primes, result


def polarization(matrix: np.ndarray, lam: np.ndarray, comp: np.ndarray,
                 residual: np.ndarray) -> dict[str, float | str]:
    y_lam = matrix @ lam
    y_comp = matrix @ comp
    y_res = matrix @ residual
    energy_lam = float(y_lam @ y_lam)
    energy_comp = float(y_comp @ y_comp)
    cross = float(y_lam @ y_comp)
    energy_res = float(y_res @ y_res)
    component_sum = energy_lam + energy_comp
    kappa = 2.0 * cross / component_sum
    fraction = energy_res / component_sum
    lower = ((math.sqrt(energy_lam) - math.sqrt(energy_comp)) ** 2 /
             component_sum)
    upper = ((math.sqrt(energy_lam) + math.sqrt(energy_comp)) ** 2 /
             component_sum)
    cosine = cross / math.sqrt(energy_lam * energy_comp)
    identity_error = abs(energy_res - component_sum + 2.0 * cross)
    label = ("POSITIVE_OUTPUT_ALIGNMENT" if kappa > KAPPA_GUARD else
             "NEGATIVE_OUTPUT_ALIGNMENT" if kappa < -KAPPA_GUARD else
             "UNRESOLVED")
    return {
        "lambda_output_energy": energy_lam,
        "comparison_output_energy": energy_comp,
        "component_output_energy_sum": component_sum,
        "output_cross_inner_product": cross,
        "residual_output_energy": energy_res,
        "output_polarization_kappa": kappa,
        "residual_fraction_of_component_sum": fraction,
        "cauchy_lower_fraction": lower,
        "cauchy_upper_fraction": upper,
        "output_cosine": cosine,
        "identity_error": identity_error,
        "classification": label,
    }


def close(actual: float, recorded: Any, label: str) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " is not numeric") from error
    need(math.isfinite(actual) and math.isfinite(target), label + " nonfinite")
    scale = max(1.0, abs(actual), abs(target))
    need(abs(actual - target) <= NUMERIC_TOL * scale, label + " mismatch")


def check_metrics(recorded: dict[str, Any], replay: dict[str, float | str],
                  source_kappa: float, label: str) -> None:
    need(recorded.get("classification") == replay["classification"],
         label + " classification")
    for field in (
            "lambda_output_energy", "comparison_output_energy",
            "component_output_energy_sum", "output_cross_inner_product",
            "residual_output_energy", "output_polarization_kappa",
            "residual_fraction_of_component_sum", "cauchy_lower_fraction",
            "cauchy_upper_fraction", "output_cosine", "identity_error"):
        close(float(replay[field]), recorded.get(field), label + " " + field)
    close(source_kappa, recorded.get("source_polarization_kappa"),
          label + " source kappa")
    close(float(replay["output_polarization_kappa"]) - source_kappa,
          recorded.get("output_minus_source_kappa"), label + " delta")


def exact_entry(prime: int, u: int, t: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(int((u - t) % prime == 0), 1)
    centered -= Fraction(1, prime - 1)
    return (prime * Fraction(HEIGHT * HEIGHT,
                             HEIGHT * HEIGHT + (u - t) ** 2) * centered)


def exact_anchor() -> tuple[str, str, str, str]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    matrix = [[sum((exact_entry(prime, u, t) for prime in (5, 7)),
                   Fraction(0)) for t in values] for u in values]
    left = [Fraction(value) for value in EXACT_LEFT]
    right = [Fraction(value) for value in EXACT_RIGHT]

    def image(vector: list[Fraction]) -> list[Fraction]:
        return [sum((matrix[i][j] * vector[j] for j in range(len(values))),
                    Fraction(0)) for i in range(len(values))]

    left_image, right_image = image(left), image(right)
    residual_image = [a - b for a, b in zip(left_image, right_image)]
    left_energy = sum((value * value for value in left_image), Fraction(0))
    right_energy = sum((value * value for value in right_image), Fraction(0))
    cross = sum((a * b for a, b in zip(left_image, right_image)), Fraction(0))
    residual_energy = sum((value * value for value in residual_image),
                          Fraction(0))
    need(residual_energy == left_energy + right_energy - 2 * cross,
         "exact anchor identity")
    return tuple(fraction_digest(value) for value in
                 (left_energy, right_energy, cross, residual_energy))


def check_parent_comparison(recorded: dict[str, Any],
                            summaries: dict[str, dict[str, Any]]) -> None:
    raw, parent_document = load_json(PARENT_CERT)
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate digest")
    parent_payload = parent_document.get("payload", {})
    parent_protocol = parent_payload.get("protocol", {})
    need(parent_protocol.get("origins") == [6001, 8001, 10001] and
         parent_protocol.get("source_counts") == list(COUNTS) and
         parent_protocol.get("q_anchors") == list(Q_ANCHORS) and
         parent_protocol.get("kernel_exponents") == list(EXPONENTS) and
         parent_protocol.get("laws") == list(LAW_NAMES),
         "parent comparison protocol")
    parent_summaries = parent_payload.get("law_summaries", {})
    parent_audit = parent_payload.get("finite_audit", {})
    need(recorded.get("parent_release") == "TPC-353" and
         recorded.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         recorded.get("protocol_difference") == "origins_only" and
         recorded.get("parent_origins") == [6001, 8001, 10001] and
         recorded.get("holdout_origins") == list(ORIGINS) and
         recorded.get("parent_rows") == 216 and
         recorded.get("holdout_rows") == 216 and
         recorded.get("parent_positive_alignment") == 216 and
         recorded.get("holdout_positive_alignment") == 216,
         "parent comparison header")
    for law in LAW_NAMES:
        current = summaries[law]
        previous = parent_summaries.get(law, {})
        item = recorded.get("law_summaries", {}).get(law, {})
        need(previous.get("rows") == 54 and
             previous.get("positive_output_alignment") == 54 and
             item.get("parent_kappa_min") == previous.get("kappa_min") and
             item.get("parent_kappa_max") == previous.get("kappa_max") and
             item.get("parent_kappa_mean") == previous.get("kappa_mean") and
             item.get("holdout_kappa_min") == current.get("kappa_min") and
             item.get("holdout_kappa_max") == current.get("kappa_max") and
             item.get("holdout_kappa_mean") == current.get("kappa_mean") and
             item.get("parent_positive_alignment") == 54 and
             item.get("holdout_positive_alignment") == 54,
             law + " parent comparison values")
        close(float(current["kappa_min"]) - float(previous["kappa_min"]),
              item.get("holdout_minus_parent_kappa_min"),
              law + " parent minimum delta")
        close(float(current["kappa_max"]) - float(previous["kappa_max"]),
              item.get("holdout_minus_parent_kappa_max"),
              law + " parent maximum delta")
        close(float(current["kappa_mean"]) - float(previous["kappa_mean"]),
              item.get("holdout_minus_parent_kappa_mean"),
              law + " parent mean delta")
    need(parent_audit.get("rows") == 216 and
         parent_audit.get("positive_output_alignment") == 216,
         "parent finite audit")


def check() -> None:
    _, document = load_json(CERTIFICATE)
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")

    for path, expected, label in (
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC353 code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC353 certificate"),
            (V59_CODE, V59_CODE_SHA256, "V59 code"),
            (V59_CERT, V59_CERT_SHA256, "V59 certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    lock = payload.get("parent_lock", {})
    need(lock.get("TPC353_code_sha256") == PARENT_CODE_SHA256 and
         lock.get("TPC353_certificate_sha256") == PARENT_CERT_SHA256 and
         lock.get("V59_code_sha256") == V59_CODE_SHA256 and
         lock.get("V59_certificate_sha256") == V59_CERT_SHA256,
         "parent lock fields")

    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == list(ORIGINS) and
         protocol.get("source_counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("height") == HEIGHT and
         protocol.get("laws") == list(LAW_NAMES), "protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 216, "row census")
    need(payload.get("row_digest") == hashlib.sha256(canonical(rows)).hexdigest(),
         "row digest")
    indexed: dict[tuple[int, int, int, int, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["origin"], row["count"], row["Q"],
               row["kernel_exponent"], row["law"])
        need(key not in indexed, "duplicate row key")
        indexed[key] = row
    expected_keys = {(origin, count, q0, exponent, law)
                     for origin in ORIGINS for count in COUNTS
                     for q0 in Q_ANCHORS for exponent in EXPONENTS
                     for law in LAW_NAMES}
    need(set(indexed) == expected_keys, "row key set")

    positive = 0
    law_values: dict[str, list[float]] = {law: [] for law in LAW_NAMES}
    identity_max = 0.0
    for origin in ORIGINS:
        for count in COUNTS:
            lam, comp, residual = source_vectors(origin, count)
            source_kappa = (2.0 * float(lam @ comp) /
                            float(lam @ lam + comp @ comp))
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    primes, matrix_map = matrices(origin, count, q0, exponent)
                    for law in LAW_NAMES:
                        row = indexed[(origin, count, q0, exponent, law)]
                        need(row["source_interval"] ==
                             [origin, origin + count - 1] and
                             row["source_count"] == count and
                             row["shell"] == primes and
                             row["shell_cardinality"] == len(primes) and
                             row["operator_shape"] == [count, count],
                             "row geometry")
                        replay = polarization(matrix_map[law], lam, comp,
                                              residual)
                        check_metrics(row["metrics"], replay, source_kappa,
                                      f"{origin}/{count}/{q0}/{exponent}/{law}")
                        positive += replay["classification"] == \
                            "POSITIVE_OUTPUT_ALIGNMENT"
                        law_values[law].append(float(
                            replay["output_polarization_kappa"]))
                        identity_max = max(identity_max,
                                           float(replay["identity_error"]))
    need(positive == 216, "positive alignment census")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 216 and
         audit.get("positive_output_alignment") == 216 and
         audit.get("negative_output_alignment") == 0 and
         audit.get("unresolved") == 0 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "finite audit")
    close(identity_max, audit.get("max_identity_error"), "identity maximum")
    summaries = payload.get("law_summaries", {})
    current_summaries: dict[str, dict[str, Any]] = {}
    for law, values in law_values.items():
        summary = summaries.get(law, {})
        need(summary.get("rows") == 54 and
             summary.get("positive_output_alignment") == 54 and
             summary.get("negative_output_alignment") == 0,
             law + " summary census")
        close(min(values), summary.get("kappa_min"), law + " min")
        close(max(values), summary.get("kappa_max"), law + " max")
        close(sum(values) / len(values), summary.get("kappa_mean"),
              law + " mean")
        current_summaries[law] = {
            "rows": summary.get("rows"),
            "positive_output_alignment": summary.get(
                "positive_output_alignment"),
            "kappa_min": summary.get("kappa_min"),
            "kappa_max": summary.get("kappa_max"),
            "kappa_mean": summary.get("kappa_mean"),
        }
    check_parent_comparison(payload.get("parent_comparison", {}),
                            current_summaries)

    anchor = payload.get("exact_anchor", {})
    digests = exact_anchor()
    need(digests == (EXACT_LEFT_DIGEST, EXACT_RIGHT_DIGEST,
                     EXACT_CROSS_DIGEST, EXACT_RESIDUAL_DIGEST) and
         anchor.get("left_energy_digest") == digests[0] and
         anchor.get("right_energy_digest") == digests[1] and
         anchor.get("cross_digest") == digests[2] and
         anchor.get("residual_energy_digest") == digests[3] and
         anchor.get("identity_exact") is True, "exact anchor")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC354_FINITE_OPERATOR_POLARIZATION") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC354_OPERATOR_REPLAY") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_ROWS" and
         firewall.get("TPC354_POSITIVE_ALIGNMENT") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_OF_216" and
         firewall.get("TPC354_HIGHER_ORIGIN_HOLDOUT") ==
         "NUMERICALLY_CERTIFIED_FINITE_216_ROWS" and
         firewall.get("TPC354_UNIFORM_L2") == "OPEN" and
         firewall.get("TPC354_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC354_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC354_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC354_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")
    print("TPC354_INDEPENDENT_CHECK=PASS rows=216 "
          "positive_alignment=216/216 exact_anchor=1")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError, np.linalg.LinAlgError) as error:
        print("TPC354_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
