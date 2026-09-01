#!/usr/bin/env python3
"""TPC-324: source-location holdout for signed spectral profiles.

TPC-323 found an all-plus profile-majorization pattern on three contiguous
source intervals.  This producer freezes two disjoint, source-location-only
holdouts with the same cardinalities, shell anchors, height, and kernel
exponents.  It records the full four-law profile census without making an
asymptotic or arithmetic claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
    from scipy.linalg import eigh
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC324 requires numpy and scipy: " + str(error))

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc324_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-323-signed-profile-majorization/results/"
    "tpc323_certificate.json")
PARENT_CERT_SHA256 = (
    "5f7d3c35a83f0176fa5e3573377bc96514ffa105203129995a2bd16e73c31faa")

SCHEMA = "TPC324_SOURCE_PROFILE_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION"
ROUND2_CLUE = "TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2"

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PATHS = ("scipy_forward", "numpy_forward", "numpy_reverse")
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")
PROFILE_TOL = 1.0e-10
NUMERICAL_GUARD = 1.0e-12
PATH_TOL = 2.0e-7

# These intervals are frozen before the calculation.  The first panel is the
# natural continuation after the TPC-323 source union.  The second is a
# separated hostile panel; neither shares a source integer with training.
PANEL_INTERVALS: dict[str, dict[int, tuple[int, int]]] = {
    "continuation": {
        640: (2561, 2880),
        1280: (2881, 3520),
        2560: (3521, 4800),
    },
    "gap_offset": {
        640: (5001, 5320),
        1280: (6001, 6640),
        2560: (8001, 9280),
    },
}
PANEL_NAMES = tuple(PANEL_INTERVALS)
SMALL_INTERVAL = (4001, 4016)
SMALL_Q = 4
SMALL_EXPONENT = 1
SMALL_DIRECT_DIGEST = (
    "97225bdbd0cb628956b3701748cec3b2eca7b4d559c0d0b42044300f7c26889b")
SMALL_SIGNED_DIGEST = (
    "b475bf82b2fd579e2bcdaf1a47311b2f49f5e6a5a2102dfcd404209f98845bd3")


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


PRIMES = primes_up_to(160)


def shell_for(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def source_interval(panel: str, scale: int) -> tuple[int, int, int]:
    need(panel in PANEL_INTERVALS and scale in SCALES,
         "unknown source panel")
    lo, hi = PANEL_INTERVALS[panel][scale]
    count = hi - lo + 1
    need(count == scale // 2, "holdout cardinality")
    return lo, hi, count


def block_matrix(panel: str, scale: int, q0: int, exponent: int) -> tuple[
        list[int], list[np.ndarray]]:
    lo, hi, _ = source_interval(panel, scale)
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + dd * dd) ** exponent)
    blocks: list[np.ndarray] = []
    primes = shell_for(q0)
    for prime in primes:
        valid = ((differences != 0) &
                 (values[:, None] % prime != 0) &
                 (values[None, :] % prime != 0))
        centered = ((differences % prime == 0).astype(np.float64) -
                    1.0 / (prime - 1))
        blocks.append(prime * kernel * centered * valid)
    return primes, blocks


def accumulate_direct(blocks: list[np.ndarray], reverse: bool,
                       einsum: bool) -> np.ndarray:
    order = range(len(blocks) - 1, -1, -1) if reverse else range(len(blocks))
    result = np.zeros((blocks[0].shape[1], blocks[0].shape[1]),
                      dtype=np.float64)
    for index in order:
        block = blocks[index]
        if einsum:
            result += np.einsum("ij,ik->jk", block, block, optimize=False)
        else:
            result += block.T @ block
    return (result + result.T) / 2.0


def accumulate_coherent(blocks: list[np.ndarray], signs: np.ndarray,
                        reverse: bool, einsum: bool) -> np.ndarray:
    order = range(len(blocks) - 1, -1, -1) if reverse else range(len(blocks))
    coherent = np.zeros_like(blocks[0])
    for index in order:
        coherent += float(signs[index]) * blocks[index]
    if einsum:
        gram = np.einsum("ij,ik->jk", coherent, coherent, optimize=False)
    else:
        gram = coherent.T @ coherent
    return (gram + gram.T) / 2.0


def sign_patterns(primes: list[int]) -> dict[str, np.ndarray]:
    m = len(primes)
    return {
        "all_plus": np.ones(m, dtype=np.float64),
        "alternating_index": np.asarray(
            [1 if index % 2 == 0 else -1 for index in range(m)],
            dtype=np.float64),
        "mod4_character": np.asarray(
            [1 if prime % 4 == 1 else -1 for prime in primes],
            dtype=np.float64),
        "half_split": np.asarray(
            [1 if index < m / 2 else -1 for index in range(m)],
            dtype=np.float64),
    }


def spectral_profile(gram: np.ndarray, solver: str) -> np.ndarray:
    gram = (gram + gram.T) / 2.0
    if solver == "scipy":
        values = eigh(gram, eigvals_only=True, check_finite=False,
                      driver="evr")
    elif solver == "numpy":
        values = np.linalg.eigvalsh(gram)
    else:  # pragma: no cover
        raise CheckFailure("unknown spectral solver")
    need(bool(np.all(np.isfinite(values))), "finite eigenvalues")
    values = np.maximum(np.asarray(values, dtype=np.float64), 0.0)
    total = float(np.sum(values, dtype=np.float64))
    need(total > 0 and math.isfinite(total), "positive spectral trace")
    profile = values[::-1] / total
    need(bool(np.all(np.isfinite(profile))) and
         math.isclose(float(np.sum(profile, dtype=np.float64)), 1.0,
                      rel_tol=3.0e-14, abs_tol=3.0e-14),
         "normalised spectral profile")
    return profile


def profile_digest(profile: np.ndarray) -> str:
    rounded = np.round(np.asarray(profile, dtype=np.float64), 14)
    return hashlib.sha256(rounded.astype("<f8", copy=False).tobytes()).hexdigest()


def profile_metrics(signed: np.ndarray, direct: np.ndarray) -> dict[str, Any]:
    need(len(signed) == len(direct) and len(signed) > 1,
         "profile dimensions")
    delta = np.cumsum(signed - direct, dtype=np.float64)[:-1]
    minimum = float(np.min(delta))
    maximum = float(np.max(delta))
    if minimum >= -PROFILE_TOL and maximum > PROFILE_TOL:
        label = "SIGNED_MAJORISES_DIRECT"
    elif maximum <= PROFILE_TOL and minimum < -PROFILE_TOL:
        label = "DIRECT_MAJORISES_SIGNED"
    elif minimum < -PROFILE_TOL and maximum > PROFILE_TOL:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    tv = 0.5 * float(np.sum(np.abs(signed - direct), dtype=np.float64))
    ks = float(np.max(np.abs(delta)))
    integrated = float(np.mean(np.abs(delta)))
    need(0 <= tv <= 1 and 0 <= ks <= 1 and 0 <= integrated <= 1 and
         math.isfinite(minimum) and math.isfinite(maximum),
         "profile metric range")
    return {
        "tv": tv,
        "lorenz_ks": ks,
        "integrated_lorenz": integrated,
        "minimum_prefix": minimum,
        "maximum_prefix": maximum,
        "majorization": label,
    }


def outward(values: list[float], lower: float | None = None,
            upper: float | None = None) -> list[str]:
    low = min(values) - NUMERICAL_GUARD
    high = max(values) + NUMERICAL_GUARD
    if lower is not None:
        low = max(lower, low)
    if upper is not None:
        high = min(upper, high)
    need(low <= min(values) <= max(values) <= high,
         "outward interval")
    return [display(low), display(high)]


def exact_entry(prime: int, u: int, t: int, exponent: int) -> Fraction:
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
    centered -= Fraction(1, prime - 1)
    return prime * Fraction(HEIGHT ** (2 * exponent),
                            (HEIGHT * HEIGHT + (u - t) ** 2) ** exponent) * centered


def exact_small_audit() -> dict[str, Any]:
    values = list(range(SMALL_INTERVAL[0], SMALL_INTERVAL[1] + 1))
    primes = shell_for(SMALL_Q)
    blocks = [[[exact_entry(prime, u, t, SMALL_EXPONENT)
                for t in values] for u in values] for prime in primes]
    gram = [[sum((blocks[i][u][t] * blocks[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signs = (1, -1) if len(primes) == 2 else tuple(
        1 if index % 2 == 0 else -1 for index in range(len(primes)))
    signed = sum((signs[i] * signs[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))

    def fraction_digest(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()

    need(direct > 0 and signed > 0, "exact anchor positivity")
    direct_digest = fraction_digest(direct)
    signed_digest = fraction_digest(signed)
    need(direct_digest == SMALL_DIRECT_DIGEST and
         signed_digest == SMALL_SIGNED_DIGEST, "exact anchor digest")
    return {
        "interval": list(SMALL_INTERVAL),
        "Q": SMALL_Q,
        "shell": primes,
        "exponent": SMALL_EXPONENT,
        "direct_energy_digest": direct_digest,
        "signed_energy_digest": signed_digest,
        "direct_energy_decimal": display(float(direct), 16),
        "signed_energy_decimal": display(float(signed), 16),
        "signed_over_direct_decimal": display(float(signed / direct), 16),
        "identity_exact": True,
    }


def path_metric_record(metric: dict[str, Any], profile: np.ndarray) -> dict[str, Any]:
    return {
        "profile_digest": profile_digest(profile),
        "tv": display(metric["tv"], 16),
        "lorenz_ks": display(metric["lorenz_ks"], 16),
        "integrated_lorenz": display(metric["integrated_lorenz"], 16),
        "minimum_prefix": display(metric["minimum_prefix"], 16),
        "maximum_prefix": display(metric["maximum_prefix"], 16),
        "majorization": metric["majorization"],
    }


def row_record(panel: str, scale: int, q0: int, exponent: int) -> dict[str, Any]:
    primes, blocks = block_matrix(panel, scale, q0, exponent)
    need(len(primes) > 0 and len(blocks) == len(primes), "shell geometry")
    direct_forward = accumulate_direct(blocks, reverse=False, einsum=False)
    direct_reverse = accumulate_direct(blocks, reverse=True, einsum=True)
    direct_profiles = {
        "scipy_forward": spectral_profile(direct_forward, "scipy"),
        "numpy_forward": spectral_profile(direct_forward, "numpy"),
        "numpy_reverse": spectral_profile(direct_reverse, "numpy"),
    }
    need(max(float(np.max(np.abs(direct_profiles["numpy_forward"] - value)))
           for value in direct_profiles.values()) < PATH_TOL,
         "direct profile path agreement")
    direct_trace = float(np.trace(direct_forward))
    need(direct_trace > 0 and math.isfinite(direct_trace), "direct trace")

    laws: dict[str, dict[str, Any]] = {}
    for name, signs in sign_patterns(primes).items():
        signed_forward = accumulate_coherent(
            blocks, signs, reverse=False, einsum=False)
        signed_reverse = accumulate_coherent(
            blocks, signs, reverse=True, einsum=True)
        signed_profiles = {
            "scipy_forward": spectral_profile(signed_forward, "scipy"),
            "numpy_forward": spectral_profile(signed_forward, "numpy"),
            "numpy_reverse": spectral_profile(signed_reverse, "numpy"),
        }
        need(max(float(np.max(np.abs(signed_profiles["numpy_forward"] - value)))
                for value in signed_profiles.values()) < PATH_TOL,
             "signed profile path agreement")
        path_metrics = {
            path: profile_metrics(signed_profiles[path],
                                  direct_profiles[path])
            for path in PATHS
        }
        labels = sorted({item["majorization"] for item in path_metrics.values()})
        need(len(labels) == 1, "majorization path consensus")
        direct_energy_values = [float(np.trace(direct_forward)),
                                float(np.trace(direct_reverse))]
        signed_energy_values = [float(np.trace(signed_forward)),
                                float(np.trace(signed_reverse))]
        ratios = [value / base for value, base in
                  zip(signed_energy_values, direct_energy_values)]
        need(all(value > 0 and math.isfinite(value) for value in ratios),
             "energy ratio")
        metric_values = list(path_metrics.values())
        laws[name] = {
            "signs": [int(value) for value in signs],
            "energy_ratio_interval": outward(ratios, lower=0.0),
            "energy_ratio_estimate": display(ratios[0], 16),
            "paths": {
                path: path_metric_record(path_metrics[path],
                                         signed_profiles[path])
                for path in PATHS
            },
            "profile_tv_interval": outward(
                [item["tv"] for item in metric_values], lower=0.0, upper=1.0),
            "profile_ks_interval": outward(
                [item["lorenz_ks"] for item in metric_values],
                lower=0.0, upper=1.0),
            "integrated_lorenz_interval": outward(
                [item["integrated_lorenz"] for item in metric_values],
                lower=0.0, upper=1.0),
            "minimum_prefix_interval": outward(
                [item["minimum_prefix"] for item in metric_values]),
            "maximum_prefix_interval": outward(
                [item["maximum_prefix"] for item in metric_values]),
            "majorization": labels[0],
            "path_majorization_consensus": labels,
            "path_profile_linf_max": display(max(
                float(np.max(np.abs(signed_profiles["numpy_forward"] - value)))
                for value in signed_profiles.values()), 16),
            "path_metric_tv_max": display(max(
                item["tv"] for item in metric_values), 16),
        }

    lo, hi, count = source_interval(panel, scale)
    return {
        "panel": panel,
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": count,
        "Q": q0,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "shell": primes,
        "shell_cardinality": len(primes),
        "operator_rows": count * len(primes),
        "operator_columns": count,
        "profile_dimension": count,
        "direct_trace": display(direct_trace, 16),
        "direct_profile_paths": {
            path: {"profile_digest": profile_digest(direct_profiles[path]),
                   "top_share": display(float(direct_profiles[path][0]), 16)}
            for path in PATHS
        },
        "direct_profile_path_linf_max": display(max(
            float(np.max(np.abs(direct_profiles["numpy_forward"] - value)))
            for value in direct_profiles.values()), 16),
        "laws": laws,
        "profile_definition": (
            "pi_j(G)=lambda_j(G)/tr(G), descending; signed G_e=C_e^T C_e; "
            "direct G_direct=sum_p B_p^T B_p"),
        "finite_numerical_guard": display(NUMERICAL_GUARD),
    }


def expected_profile_counts() -> dict[str, dict[str, int]]:
    return {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 48,
                     "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 0,
                     "UNRESOLVED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 34,
                              "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 14,
                              "UNRESOLVED": 0},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 42,
                            "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 6,
                            "UNRESOLVED": 0},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 36,
                        "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 12,
                        "UNRESOLVED": 0},
    }


def expected_panel_profile_counts() -> dict[str, dict[str, dict[str, int]]]:
    one = {
        "all_plus": {"SIGNED_MAJORISES_DIRECT": 24,
                     "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 0,
                     "UNRESOLVED": 0},
        "alternating_index": {"SIGNED_MAJORISES_DIRECT": 17,
                              "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 7,
                              "UNRESOLVED": 0},
        "mod4_character": {"SIGNED_MAJORISES_DIRECT": 21,
                            "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 3,
                            "UNRESOLVED": 0},
        "half_split": {"SIGNED_MAJORISES_DIRECT": 18,
                        "DIRECT_MAJORISES_SIGNED": 0, "MIXED": 6,
                        "UNRESOLVED": 0},
    }
    return {panel: one for panel in PANEL_NAMES}


def build_payload() -> dict[str, Any]:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_CERT_SHA256, "TPC323 parent certificate lock")
    rows = [row_record(panel, scale, q0, exponent)
            for panel in PANEL_NAMES for scale in SCALES
            for q0 in Q_ANCHORS for exponent in EXPONENTS]
    need(len(rows) == 48, "row census")
    class_counts = {
        name: {label: sum(row["laws"][name]["majorization"] == label
                          for row in rows)
               for label in LABELS}
        for name in LAW_NAMES
    }
    panel_class_counts: dict[str, dict[str, dict[str, int]]] = {}
    for panel in PANEL_NAMES:
        panel_rows = [row for row in rows if row["panel"] == panel]
        panel_class_counts[panel] = {
            name: {label: sum(row["laws"][name]["majorization"] == label
                              for row in panel_rows)
                   for label in LABELS}
            for name in LAW_NAMES
        }
    energy_counts = {
        name: {
            "below_one": sum(float(row["laws"][name]["energy_ratio_estimate"])
                              < 1.0 for row in rows),
            "above_one": sum(float(row["laws"][name]["energy_ratio_estimate"])
                              > 1.0 for row in rows),
        }
        for name in LAW_NAMES
    }
    need(class_counts == expected_profile_counts(), "profile census")
    need(panel_class_counts == expected_panel_profile_counts(),
         "per-panel profile census")
    need(energy_counts == {
        "all_plus": {"below_one": 6, "above_one": 42},
        "alternating_index": {"below_one": 42, "above_one": 6},
        "mod4_character": {"below_one": 38, "above_one": 10},
        "half_split": {"below_one": 42, "above_one": 6},
    }, "energy census")
    all_plus_min_prefix = min(
        float(row["laws"]["all_plus"]["minimum_prefix_interval"][0])
        for row in rows)
    need(all_plus_min_prefix > 0, "strict all-plus holdout majorization")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "project": "TPC-323 signed profile majorization",
            "certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "source_panels": {
                panel: {str(scale): list(PANEL_INTERVALS[panel][scale])
                        for scale in SCALES}
                for panel in PANEL_NAMES
            },
            "source_scales": list(SCALES),
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "domain": "ell^2(I_panel,scale)",
            "direct_gram": "G_direct=sum_p B_p^T B_p",
            "signed_gram": "G_e=C_e^T C_e, C_e=sum_p e_p B_p",
            "profile": "pi_j(G)=lambda_j(G)/tr(G), descending",
            "paths": list(PATHS),
            "profile_tolerance": PROFILE_TOL,
            "numerical_guard": NUMERICAL_GUARD,
            "majorization_rule": (
                "signed cumulative-minus-direct cumulative is nonnegative "
                "at every interior rank"),
            "canonical_sign_laws": list(LAW_NAMES),
            "holdout_rule": (
                "two frozen disjoint source panels with the TPC-323 counts; "
                "no source integer overlaps the TPC-323 training union"),
        },
        "exact_small_audit": exact_small_audit(),
        "finite_audit": {
            "rows": len(rows),
            "panel_rows": {panel: 24 for panel in PANEL_NAMES},
            "panel_names": list(PANEL_NAMES),
            "profile_majorization_counts": class_counts,
            "per_panel_profile_majorization_counts": panel_class_counts,
            "energy_ratio_counts": energy_counts,
            "all_plus_strict_majorization_rows": 48,
            "all_plus_minimum_prefix_lower": display(all_plus_min_prefix, 16),
            "replication_match_to_tpc323": True,
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC324_SOURCE_LOCATION_HOLDOUT":
                "NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS",
            "TPC324_ALL_PLUS_PROFILE_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_48_OF_48",
            "TPC324_PER_PANEL_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24_EACH",
            "TPC324_ALTERNATIVE_PROFILE_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_48_ROWS",
            "TPC324_TRANSLATION_COVARIANCE": "PROVED_EXACT_FINITE_CONDITIONAL",
            "TPC324_ARITHMETIC_ADVANCE": "NO",
            "TPC324_FIXED_POWER_CREDIT": 0,
            "TPC324_FULL_GATE_B": "OPEN",
            "TPC324_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(build_document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored == build_document(), "certificate does not replay")
    print("TPC324_CERTIFICATE=PASS rows=48 panels=2 all_plus_profile=48/48 "
          "per_panel=24/24 alternative=34/14,42/6,36/12")


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
            print("TPC324_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC324_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
