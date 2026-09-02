#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-355.

This file intentionally does not import the producer.  It rebuilds the finite
V59 source, literal masked components, unsigned geometry diagonal, raw signed
operators, and the symmetric position-aware congruence while accumulating the
prime shell in reverse order.
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
PROJECT = ROOT / "papers/tpc-355-position-aware-mask-energy-normalization"
CERTIFICATE = PROJECT / "results/tpc355_certificate.json"
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
KAPPA_GUARD = 1.0e-7
NUMERIC_TOL = 2.0e-5
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
EXACT_INTERVAL = (29001, 29014)
EXACT_LEFT = (1, -1, 0, 2, -1, 0, 1, 0, 0, -1, 1, 0, 0, 1)
EXACT_RIGHT = (0, 1, 1, -1, 0, 2, 0, -1, 1, 0, -1, 0, 1, 0)


class Failure(RuntimeError):
    pass


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


def close(actual: float, recorded: Any, label: str) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " nonnumeric") from error
    need(math.isfinite(actual) and math.isfinite(target), label + " nonfinite")
    need(abs(actual - target) <= NUMERIC_TOL * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


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


def shell(q0: int) -> list[int]:
    return [prime for prime in TAIL_PRIMES if q0 < prime <= 2 * q0]


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


TAIL_CENTER: Decimal | None = None


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


def source_vectors(origin: int, count: int
                   ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lambdas = []
    comparisons = []
    for value in range(origin, origin + count):
        base = prime_power_base(value + 2)
        lambdas.append(0.0 if base is None else float(Decimal(base).ln()))
        comparisons.append(comparison_midpoint(value))
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


def reverse_components(origin: int, count: int, q0: int, exponent: int
                       ) -> tuple[list[int], dict[str, np.ndarray], np.ndarray]:
    values = np.arange(origin, origin + count, dtype=np.int64)
    delta = values[:, None] - values[None, :]
    distance = delta.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + distance * distance) ** exponent)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    sign_map = signs(primes)
    matrices = {name: np.zeros((count, count), dtype=np.float64)
                for name in LAW_NAMES}
    geometry = np.zeros(count, dtype=np.float64)
    for index, prime in reversed(list(enumerate(primes))):
        centered = ((delta % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((delta != 0) & (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        block = float(prime) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for name in LAW_NAMES:
            matrices[name] += sign_map[name][index] * block
    for name in LAW_NAMES:
        matrices[name] = (matrices[name] + matrices[name].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))),
         "reverse geometry positivity")
    return primes, matrices, geometry


def polarization(matrix: np.ndarray, lam: np.ndarray, comp: np.ndarray,
                 residual: np.ndarray) -> dict[str, float | str]:
    y_lam = matrix @ lam
    y_comp = matrix @ comp
    y_res = matrix @ residual
    e_l = float(y_lam @ y_lam)
    e_b = float(y_comp @ y_comp)
    cross = float(y_lam @ y_comp)
    e_r = float(y_res @ y_res)
    total = e_l + e_b
    need(e_l > 0 and e_b > 0 and e_r > 0 and math.isfinite(total),
         "reverse output energies")
    kappa = 2.0 * cross / total
    fraction = e_r / total
    lower = ((math.sqrt(e_l) - math.sqrt(e_b)) ** 2 / total)
    upper = ((math.sqrt(e_l) + math.sqrt(e_b)) ** 2 / total)
    cosine = cross / math.sqrt(e_l * e_b)
    identity_error = abs(e_r - total + 2.0 * cross)
    label = ("POSITIVE_OUTPUT_ALIGNMENT" if kappa > KAPPA_GUARD else
             "NEGATIVE_OUTPUT_ALIGNMENT" if kappa < -KAPPA_GUARD else
             "UNRESOLVED")
    return {
        "lambda_output_energy": e_l,
        "comparison_output_energy": e_b,
        "component_output_energy_sum": total,
        "output_cross_inner_product": cross,
        "residual_output_energy": e_r,
        "output_polarization_kappa": kappa,
        "residual_fraction_of_component_sum": fraction,
        "cauchy_lower_fraction": lower,
        "cauchy_upper_fraction": upper,
        "output_cosine": cosine,
        "identity_error": identity_error,
        "classification": label,
    }


def check_metrics(recorded: dict[str, Any], replay: dict[str, float | str],
                  source_kappa: float, label: str) -> float:
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
    return float(replay["output_polarization_kappa"])


def exact_entry(prime: int, u: int, t: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(int((u - t) % prime == 0), 1)
    centered -= Fraction(1, prime - 1)
    return prime * Fraction(HEIGHT * HEIGHT,
                            HEIGHT * HEIGHT + (u - t) ** 2) * centered


def exact_anchor() -> dict[str, str | bool]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    matrix = [[sum((exact_entry(prime, u, t) for prime in (5, 7)),
                   Fraction(0)) for t in values] for u in values]
    geometry = [sum((exact_entry(prime, u, t) ** 2 for prime in (5, 7)
                     for t in values), Fraction(0)) for u in values]
    left = [Fraction(value) for value in EXACT_LEFT]
    right = [Fraction(value) for value in EXACT_RIGHT]

    def image(vector: list[Fraction]) -> list[Fraction]:
        return [sum((matrix[i][j] * vector[j]
                     for j in range(len(values))), Fraction(0))
                for i in range(len(values))]

    li, ri = image(left), image(right)
    residual = [a - b for a, b in zip(li, ri)]
    le = sum((value * value for value in li), Fraction(0))
    re = sum((value * value for value in ri), Fraction(0))
    cross = sum((a * b for a, b in zip(li, ri)), Fraction(0))
    be = sum((value * value for value in residual), Fraction(0))
    need(be == le + re - 2 * cross, "reverse exact anchor identity")
    geometry_digest = hashlib.sha256(canonical([
        f"{value.numerator}/{value.denominator}" for value in geometry
    ])).hexdigest()
    return {
        "left_energy_digest": fraction_digest(le),
        "right_energy_digest": fraction_digest(re),
        "cross_digest": fraction_digest(cross),
        "residual_energy_digest": fraction_digest(be),
        "geometry_digest": geometry_digest,
        "geometry_positive": True,
        "identity_exact": True,
    }


def load_json(path: Path, expected: str, label: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected, label + " digest")
    document = json.loads(raw)
    need(raw == canonical(document), label + " canonicality")
    need(isinstance(document, dict), label + " object")
    return document


def main() -> int:
    if any(arg != "--check" for arg in sys.argv[1:]) or len(sys.argv) != 2:
        raise SystemExit("--check is the only argument")
    try:
        document = load_json(CERTIFICATE, digest(CERTIFICATE.read_bytes()),
                             "TPC355 certificate")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
             "schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload hash")
        for path, expected, label in (
                (PARENT_354_CODE, PARENT_354_CODE_SHA256, "TPC354 code"),
                (PARENT_354_CERT, PARENT_354_CERT_SHA256, "TPC354 certificate"),
                (PARENT_353_CODE, PARENT_353_CODE_SHA256, "TPC353 code"),
                (PARENT_353_CERT, PARENT_353_CERT_SHA256, "TPC353 certificate"),
                (V59_CODE, V59_CODE_SHA256, "V59 code"),
                (V59_CERT, V59_CERT_SHA256, "V59 certificate")):
            need(path.is_file() and digest(path.read_bytes()) == expected,
                 label + " provenance")
        protocol = payload.get("protocol", {})
        need(protocol.get("panel_names") == list(PANEL_NAMES) and
             protocol.get("origins_by_panel") == {
                 key: list(value) for key, value in ORIGINS_BY_PANEL.items()} and
             protocol.get("source_counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("height") == HEIGHT and
             protocol.get("laws") == list(LAW_NAMES), "protocol")
        normalization = protocol.get("normalization", {})
        need(normalization.get("response_independent") is True and
             normalization.get("source_independent") is True and
             normalization.get("sign_law_independent") is True,
             "normalization independence")
        rows = payload.get("rows")
        need(isinstance(rows, list) and len(rows) == 648, "row census")
        indexed = {}
        for row in rows:
            key = (row["panel"], row["origin"], row["count"], row["Q"],
                   row["kernel_exponent"], row["law"])
            need(key not in indexed, "duplicate row key")
            indexed[key] = row
        expected_keys = {(panel, origin, count, q0, exponent, law)
                         for panel in PANEL_NAMES
                         for origin in ORIGINS_BY_PANEL[panel]
                         for count in COUNTS for q0 in Q_ANCHORS
                         for exponent in EXPONENTS for law in LAW_NAMES}
        need(set(indexed) == expected_keys, "row key set")
        need(payload.get("row_digest") == hashlib.sha256(
            canonical(rows)).hexdigest(), "row digest")

        values = {metric: {panel: {law: [] for law in LAW_NAMES}
                           for panel in PANEL_NAMES}
                  for metric in ("raw_metrics", "normalized_metrics")}
        raw_positive = raw_negative = raw_unresolved = 0
        norm_positive = norm_negative = norm_unresolved = 0
        identity_max = 0.0
        for panel in PANEL_NAMES:
            for origin in ORIGINS_BY_PANEL[panel]:
                for count in COUNTS:
                    lam, comp, residual = source_vectors(origin, count)
                    source_kappa = 2.0 * float(lam @ comp) / float(
                        lam @ lam + comp @ comp)
                    for q0 in Q_ANCHORS:
                        for exponent in EXPONENTS:
                            primes, matrix_map, geometry = reverse_components(
                                origin, count, q0, exponent)
                            for law in LAW_NAMES:
                                row = indexed[(panel, origin, count, q0,
                                               exponent, law)]
                                need(row["shell"] == primes and
                                     row["operator_shape"] == [count, count] and
                                     isinstance(row["unsigned_geometry_energy_min"], str) and
                                     isinstance(row["unsigned_geometry_energy_max"], str),
                                     "row geometry")
                                raw = polarization(matrix_map[law], lam, comp,
                                                    residual)
                                normalized_matrix = matrix_map[law] / np.sqrt(
                                    geometry[:, None] * geometry[None, :])
                                normalized = polarization(
                                    normalized_matrix, lam, comp, residual)
                                label = (f"{panel}/{origin}/{count}/{q0}/"
                                         f"{exponent}/{law}")
                                rk = check_metrics(row["raw_metrics"], raw,
                                                   source_kappa, label + "/raw")
                                nk = check_metrics(
                                    row["normalized_metrics"], normalized,
                                    source_kappa, label + "/normalized")
                                values["raw_metrics"][panel][law].append(rk)
                                values["normalized_metrics"][panel][law].append(nk)
                                identity_max = max(
                                    identity_max, raw["identity_error"],
                                    normalized["identity_error"])
                                raw_positive += rk > KAPPA_GUARD
                                raw_negative += rk < -KAPPA_GUARD
                                raw_unresolved += abs(rk) <= KAPPA_GUARD
                                norm_positive += nk > KAPPA_GUARD
                                norm_negative += nk < -KAPPA_GUARD
                                norm_unresolved += abs(nk) <= KAPPA_GUARD

        need((raw_positive, raw_negative, raw_unresolved) == (647, 1, 0),
             "raw census")
        need((norm_positive, norm_negative, norm_unresolved) == (647, 1, 0),
             "normalized census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 648 and
             audit.get("raw_positive_alignment") == 647 and
             audit.get("raw_negative_alignment") == 1 and
             audit.get("normalized_positive_alignment") == 647 and
             audit.get("normalized_negative_alignment") == 1 and
             audit.get("fixed_power_credit") == 0 and
             audit.get("arithmetic_advance") == "NO", "audit firewall")
        close(identity_max, audit.get("max_identity_error"),
              "identity maximum")

        summaries = payload.get("panel_summaries", {})
        for metric in ("raw_metrics", "normalized_metrics"):
            for panel in PANEL_NAMES:
                for law in LAW_NAMES:
                    actual = values[metric][panel][law]
                    recorded = summaries[panel][law][metric]
                    need(len(actual) == 54 and recorded.get("rows") == 54,
                         "summary rows")
                    need(recorded.get("positive_alignment") ==
                         sum(x > KAPPA_GUARD for x in actual) and
                         recorded.get("negative_alignment") ==
                         sum(x < -KAPPA_GUARD for x in actual) and
                         recorded.get("unresolved") ==
                         sum(abs(x) <= KAPPA_GUARD for x in actual),
                         "summary census")
                    close(min(actual), recorded.get("kappa_min"),
                          f"{panel}/{law}/{metric}/min")
                    close(max(actual), recorded.get("kappa_max"),
                          f"{panel}/{law}/{metric}/max")
                    close(sum(actual) / len(actual), recorded.get("kappa_mean"),
                          f"{panel}/{law}/{metric}/mean")

        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC355_GEOMETRY_DEFINITION") ==
             "PROVED_EXACT_FINITE_DECLARED_MODEL" and
             firewall.get("TPC355_DIAGONAL_CONGRUENCE") ==
             "PROVED_EXACT_FINITE" and
             firewall.get("TPC355_PANEL_REPLAY") ==
             "NUMERICALLY_CERTIFIED_FINITE_648_ROWS" and
             firewall.get("TPC355_ALL_PLUS_FLOOR_REPAIR") ==
             "NUMERICALLY_CERTIFIED_FINITE_PARTIAL" and
             firewall.get("TPC355_ALL_PLUS_MEAN_REPAIR") ==
             "REFUTED_SCOPED" and
             firewall.get("TPC355_SOURCE_UNIFORM_L2") == "OPEN" and
             firewall.get("TPC355_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC355_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC355_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
        anchor = payload.get("exact_anchor", {})
        actual_anchor = exact_anchor()
        for key, value in actual_anchor.items():
            need(anchor.get(key) == value, "exact anchor " + key)
        print("TPC355_INDEPENDENT_CHECK=PASS panels=3 rows=648 "
              "raw_positive=647/648 normalized_positive=647/648 "
              "exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC355_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
