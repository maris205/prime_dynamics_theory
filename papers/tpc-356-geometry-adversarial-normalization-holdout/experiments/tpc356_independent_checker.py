#!/usr/bin/env python3
"""Independent reverse-shell replay for TPC-356.

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
PROJECT = ROOT / "papers/tpc-356-geometry-adversarial-normalization-holdout"
CERTIFICATE = PROJECT / "results/tpc356_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CERT = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/results/"
    "tpc355_certificate.json")
PARENT_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CERT_SHA256 = (
    "29c5e824b415e675c931396567337cbb583b8f952b489ea2a386a63c649fff7b")

SCHEMA = "TPC356_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GEOMETRY_ADVERSARIAL_NORMALIZATION_HOLDOUT"
PANEL_NAME = "geometry_adversarial_holdout"
CANDIDATE_ORIGINS = tuple(range(38001, 48552, 211))
PILOT_COUNT = 256
SELECTED_ORIGINS = (38423, 42010, 45597)
MIN_SEPARATION = 1536
COUNTS = (256, 512, 1024)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
COMPARISON_CUTOFF = 2
TAIL_CUTOFF = 50_000
KAPPA_GUARD = 1.0e-7
NUMERIC_TOL = 2.0e-5
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
EXACT_INTERVAL = (38431, 38444)
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
        actual = float(actual)
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


def geometry_selection() -> tuple[list[dict[str, Any]], list[int]]:
    """Rebuild the response-blind pilot ranking independently."""
    records = []
    for origin in CANDIDATE_ORIGINS:
        settings = []
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                _, _, geometry = reverse_components(origin, PILOT_COUNT,
                                                    q0, exponent)
                settings.append({
                    "Q": q0,
                    "kernel_exponent": exponent,
                    "spread": max(geometry) / min(geometry),
                    "coefficient_of_variation": float(
                        np.std(geometry) / np.mean(geometry)),
                })
        best = max(settings, key=lambda item: (
            item["spread"], -item["Q"], -item["kernel_exponent"]))
        records.append({
            "origin": origin,
            "pilot_count": PILOT_COUNT,
            "score": best["spread"],
            "max_coefficient_of_variation": max(
                item["coefficient_of_variation"] for item in settings),
            "argmax_Q": best["Q"],
            "argmax_kernel_exponent": best["kernel_exponent"],
            "settings": settings,
        })
    ranked = sorted(records, key=lambda item: (-item["score"],
                                                item["origin"]))
    chosen = []
    for record in ranked:
        if all(abs(record["origin"] - old) >= MIN_SEPARATION
               for old in chosen):
            chosen.append(record["origin"])
        if len(chosen) == len(SELECTED_ORIGINS):
            break
    need(tuple(chosen) == SELECTED_ORIGINS, "selected origin rule")
    return records, chosen


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
        raw_certificate = CERTIFICATE.read_bytes()
        document = load_json(CERTIFICATE, digest(raw_certificate),
                             "TPC356 certificate")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
             "schema")
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "payload hash")
        for path, expected, label in (
                (PARENT_CODE, PARENT_CODE_SHA256, "TPC355 code"),
                (PARENT_CERT, PARENT_CERT_SHA256, "TPC355 certificate")):
            need(path.is_file() and digest(path.read_bytes()) == expected,
                 label + " provenance")
        protocol = payload.get("protocol", {})
        need(protocol.get("panel_name") == PANEL_NAME and
             protocol.get("candidate_origins") == list(CANDIDATE_ORIGINS) and
             protocol.get("pilot_count") == PILOT_COUNT and
             protocol.get("selected_origins") == list(SELECTED_ORIGINS) and
             protocol.get("minimum_separation") == MIN_SEPARATION and
             protocol.get("source_counts") == list(COUNTS) and
             protocol.get("q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("height") == HEIGHT and
             protocol.get("laws") == list(LAW_NAMES), "protocol")
        need(protocol.get("selection_uses_response") is False and
             protocol.get("selection_uses_source") is False, "selection firewall")

        selection, chosen = geometry_selection()
        audit_selection = payload.get("selection_audit", {})
        need(audit_selection.get("candidate_count") == len(selection) and
             audit_selection.get("selected_origins") == list(SELECTED_ORIGINS),
             "selection audit header")
        recorded_selection = audit_selection.get("ranked_records")
        need(isinstance(recorded_selection, list) and
             len(recorded_selection) == len(selection), "selection census")
        for actual, recorded in zip(selection, recorded_selection):
            need(actual["origin"] == recorded.get("origin") and
                 actual["pilot_count"] == recorded.get("pilot_count") and
                 actual["argmax_Q"] == recorded.get("argmax_Q") and
                 actual["argmax_kernel_exponent"] ==
                 recorded.get("argmax_kernel_exponent"), "selection metadata")
            close(actual["score"], recorded.get("score"),
                  f"selection/{actual['origin']}/score")
            close(actual["max_coefficient_of_variation"],
                  recorded.get("max_coefficient_of_variation"),
                  f"selection/{actual['origin']}/cv")
            got_settings = actual["settings"]
            saved_settings = recorded.get("settings")
            need(isinstance(saved_settings, list) and
                 len(saved_settings) == len(got_settings), "selection settings")
            for got, saved in zip(got_settings, saved_settings):
                need(got["Q"] == saved.get("Q") and
                     got["kernel_exponent"] == saved.get("kernel_exponent"),
                     "selection setting key")
                close(got["spread"], saved.get("spread"),
                      f"selection/{actual['origin']}/spread")
                close(got["coefficient_of_variation"],
                     saved.get("coefficient_of_variation"),
                     f"selection/{actual['origin']}/cv-setting")

        rows = payload.get("rows")
        need(isinstance(rows, list) and len(rows) == 216, "row census")
        indexed = {}
        for row in rows:
            key = (row["origin"], row["count"], row["Q"],
                   row["kernel_exponent"], row["law"])
            need(key not in indexed, "duplicate row key")
            indexed[key] = row
        expected_keys = {(origin, count, q0, exponent, law)
                         for origin in SELECTED_ORIGINS
                         for count in COUNTS for q0 in Q_ANCHORS
                         for exponent in EXPONENTS for law in LAW_NAMES}
        need(set(indexed) == expected_keys, "row key set")
        need(payload.get("row_digest") == hashlib.sha256(
            canonical(rows)).hexdigest(), "row digest")

        values = {metric: {law: [] for law in LAW_NAMES}
                  for metric in ("raw_metrics", "normalized_metrics")}
        raw_positive = raw_negative = raw_unresolved = 0
        norm_positive = norm_negative = norm_unresolved = 0
        identity_max = 0.0
        for origin in SELECTED_ORIGINS:
            for count in COUNTS:
                lam, comp, residual = source_vectors(origin, count)
                source_kappa = 2.0 * float(lam @ comp) / float(
                    lam @ lam + comp @ comp)
                for q0 in Q_ANCHORS:
                    for exponent in EXPONENTS:
                        primes, matrix_map, geometry = reverse_components(
                            origin, count, q0, exponent)
                        for law in LAW_NAMES:
                            row = indexed[(origin, count, q0, exponent, law)]
                            need(row["panel"] == PANEL_NAME and
                                 row["shell"] == primes and
                                 row["operator_shape"] == [count, count] and
                                 isinstance(row["unsigned_geometry_energy_min"], str) and
                                 isinstance(row["unsigned_geometry_energy_max"], str),
                                 "row geometry")
                            raw = polarization(matrix_map[law], lam, comp,
                                                residual)
                            normalized = polarization(
                                matrix_map[law] / np.sqrt(
                                    geometry[:, None] * geometry[None, :]),
                                lam, comp, residual)
                            label = f"{origin}/{count}/{q0}/{exponent}/{law}"
                            rk = check_metrics(row["raw_metrics"], raw,
                                               source_kappa, label + "/raw")
                            nk = check_metrics(row["normalized_metrics"],
                                               normalized, source_kappa,
                                               label + "/normalized")
                            values["raw_metrics"][law].append(rk)
                            values["normalized_metrics"][law].append(nk)
                            identity_max = max(identity_max, raw["identity_error"],
                                               normalized["identity_error"])
                            raw_positive += rk > KAPPA_GUARD
                            raw_negative += rk < -KAPPA_GUARD
                            raw_unresolved += abs(rk) <= KAPPA_GUARD
                            norm_positive += nk > KAPPA_GUARD
                            norm_negative += nk < -KAPPA_GUARD
                            norm_unresolved += abs(nk) <= KAPPA_GUARD

        need((raw_positive, raw_negative, raw_unresolved) == (216, 0, 0),
             "raw census")
        need((norm_positive, norm_negative, norm_unresolved) == (216, 0, 0),
             "normalized census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 216 and
             audit.get("raw_positive_alignment") == 216 and
             audit.get("raw_negative_alignment") == 0 and
             audit.get("normalized_positive_alignment") == 216 and
             audit.get("normalized_negative_alignment") == 0 and
             audit.get("fixed_power_credit") == 0 and
             audit.get("arithmetic_advance") == "NO", "audit firewall")
        close(identity_max, audit.get("max_identity_error"),
              "identity maximum")

        summaries = payload.get("law_summaries", {})
        for metric in ("raw_metrics", "normalized_metrics"):
            for law in LAW_NAMES:
                actual = values[metric][law]
                recorded = summaries[law][metric]
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
                      f"{law}/{metric}/min")
                close(max(actual), recorded.get("kappa_max"),
                      f"{law}/{metric}/max")
                close(sum(actual) / len(actual), recorded.get("kappa_mean"),
                      f"{law}/{metric}/mean")

        raw_min = float(summaries["all_plus"]["raw_metrics"]["kappa_min"])
        norm_min = float(summaries["all_plus"]["normalized_metrics"]["kappa_min"])
        raw_mean = float(summaries["all_plus"]["raw_metrics"]["kappa_mean"])
        norm_mean = float(summaries["all_plus"]["normalized_metrics"]["kappa_mean"])
        need(norm_min > raw_min and norm_mean > raw_mean,
             "scoped normalization gains")
        close(norm_min - raw_min, audit.get("normalization_min_gain"),
              "normalization min gain")
        close(norm_mean - raw_mean, audit.get("normalization_mean_gain"),
              "normalization mean gain")

        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC356_GEOMETRY_SELECTION") ==
             "PROVED_EXACT_FINITE_DETERMINISTIC" and
             firewall.get("TPC356_SELECTION_RESPONSE_INDEPENDENCE") ==
             "PROVED_EXACT_FINITE" and
             firewall.get("TPC356_PANEL_REPLAY") ==
             "NUMERICALLY_CERTIFIED_FINITE_216_ROWS" and
             firewall.get("TPC356_ALL_PLUS_MIN_GAIN") ==
             "NUMERICALLY_CERTIFIED_FINITE_SCOPED" and
             firewall.get("TPC356_ALL_PLUS_MEAN_GAIN") ==
             "NUMERICALLY_CERTIFIED_FINITE_SCOPED" and
             firewall.get("TPC356_SOURCE_UNIFORM_L2") == "OPEN" and
             firewall.get("TPC356_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC356_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC356_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
        anchor = payload.get("exact_anchor", {})
        actual_anchor = exact_anchor()
        for key, value in actual_anchor.items():
            need(anchor.get(key) == value, "exact anchor " + key)
        print("TPC356_INDEPENDENT_CHECK=PASS candidates=51 selected=3 "
              "rows=216 raw_positive=216/216 normalized_positive=216/216 "
              "exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC356_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
