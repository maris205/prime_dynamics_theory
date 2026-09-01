#!/usr/bin/env python3
"""Independent reverse/einsum replay for TPC-324.

This checker deliberately rebuilds the two holdout panels without importing
the producer.  It validates profile metrics and interval containment; long
floating-point eigenvalue byte digests remain provenance hints rather than
cross-LAPACK equality claims.
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
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC324 independent checker requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
CERTIFICATE = PROJECT / "results/tpc324_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-323-signed-profile-majorization/results/"
    "tpc323_certificate.json")
PARENT_SHA256 = (
    "5f7d3c35a83f0176fa5e3573377bc96514ffa105203129995a2bd16e73c31faa")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PANEL_INTERVALS = {
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
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")
PROFILE_TOL = 1.0e-10
PATH = "numpy_reverse"
SMALL_INTERVAL = (4001, 4016)
SMALL_Q = 4
SMALL_DIRECT_DIGEST = (
    "97225bdbd0cb628956b3701748cec3b2eca7b4d559c0d0b42044300f7c26889b")
SMALL_SIGNED_DIGEST = (
    "b475bf82b2fd579e2bcdaf1a47311b2f49f5e6a5a2102dfcd404209f98845bd3")


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


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [prime for prime in PRIMES if q0 < prime <= 2 * q0]


def signs_for(name: str, primes: list[int]) -> np.ndarray:
    if name == "all_plus":
        return np.ones(len(primes), dtype=np.float64)
    if name == "alternating_index":
        return np.asarray([1 if index % 2 == 0 else -1
                           for index in range(len(primes))], dtype=np.float64)
    if name == "mod4_character":
        return np.asarray([1 if prime % 4 == 1 else -1
                           for prime in primes], dtype=np.float64)
    if name == "half_split":
        return np.asarray([1 if index < len(primes) / 2 else -1
                           for index in range(len(primes))], dtype=np.float64)
    raise Failure("unknown sign law")


def literal_block(values: np.ndarray, differences: np.ndarray, prime: int,
                  exponent: int) -> np.ndarray:
    dd = differences.astype(np.float64)
    kernel = HEIGHT ** (2 * exponent) / (
        HEIGHT * HEIGHT + dd * dd) ** exponent
    valid = ((differences != 0) &
             (values[:, None] % prime != 0) &
             (values[None, :] % prime != 0))
    centered = (np.equal(np.mod(differences, prime), 0).astype(np.float64) -
                1.0 / (prime - 1))
    return prime * kernel * centered * valid


def rebuild_all(panel: str, scale: int, q0: int, exponent: int) -> tuple[
        np.ndarray, dict[str, np.ndarray]]:
    lo, hi = PANEL_INTERVALS[panel][scale]
    values = np.arange(lo, hi + 1, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    primes = shell(q0)
    direct = np.zeros((len(values), len(values)), dtype=np.float64)
    sign_map = {name: signs_for(name, primes) for name in LAW_NAMES}
    coherents = {name: np.zeros_like(direct) for name in LAW_NAMES}
    for reverse_index, prime in enumerate(reversed(primes)):
        index = len(primes) - 1 - reverse_index
        block = literal_block(values, differences, prime, exponent)
        direct += np.einsum("ij,ik->jk", block, block, optimize=False)
        for name in LAW_NAMES:
            coherents[name] += float(sign_map[name][index]) * block
    signed = {
        name: np.einsum("ij,ik->jk", coherent, coherent, optimize=False)
        for name, coherent in coherents.items()
    }
    direct = (direct + direct.T) / 2.0
    signed = {name: (gram + gram.T) / 2.0
              for name, gram in signed.items()}
    return direct, signed


def profile(gram: np.ndarray) -> np.ndarray:
    values = np.linalg.eigvalsh((gram + gram.T) / 2.0)
    need(bool(np.all(np.isfinite(values))), "finite replay spectrum")
    values = np.maximum(values, 0.0)[::-1]
    total = float(np.sum(values, dtype=np.float64))
    need(total > 0 and math.isfinite(total), "positive replay trace")
    result = values / total
    need(math.isclose(float(np.sum(result, dtype=np.float64)), 1.0,
                      rel_tol=3.0e-14, abs_tol=3.0e-14),
         "replay profile normalisation")
    return result


def metrics(signed: np.ndarray, direct: np.ndarray) -> dict[str, Any]:
    delta = np.cumsum(signed - direct, dtype=np.float64)[:-1]
    minimum, maximum = float(delta.min()), float(delta.max())
    if minimum >= -PROFILE_TOL and maximum > PROFILE_TOL:
        label = "SIGNED_MAJORISES_DIRECT"
    elif maximum <= PROFILE_TOL and minimum < -PROFILE_TOL:
        label = "DIRECT_MAJORISES_SIGNED"
    elif minimum < -PROFILE_TOL and maximum > PROFILE_TOL:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    return {
        "tv": 0.5 * float(np.abs(signed - direct).sum(dtype=np.float64)),
        "lorenz_ks": float(np.max(np.abs(delta))),
        "integrated_lorenz": float(np.mean(np.abs(delta))),
        "minimum_prefix": minimum,
        "maximum_prefix": maximum,
        "majorization": label,
    }


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=8.0e-7, abs_tol=2.0e-9)


def interval_contains(interval: list[str], value: float) -> bool:
    low, high = map(float, interval)
    return low <= value <= high


def exact_anchor() -> tuple[str, str]:
    values = list(range(SMALL_INTERVAL[0], SMALL_INTERVAL[1] + 1))
    primes = shell(SMALL_Q)

    def entry(prime: int, u: int, t: int) -> Fraction:
        if u == t or u % prime == 0 or t % prime == 0:
            return Fraction(0)
        centered = Fraction(1) if (u - t) % prime == 0 else Fraction(0)
        centered -= Fraction(1, prime - 1)
        return prime * Fraction(HEIGHT ** 2,
                                HEIGHT * HEIGHT + (u - t) ** 2) * centered

    blocks = [[[entry(prime, u, t) for t in values] for u in values]
              for prime in primes]
    gram = [[sum((blocks[i][u][t] * blocks[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    signs = (1, -1)
    signed = sum((signs[i] * signs[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))

    def fd(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()

    return fd(direct), fd(signed)


def check() -> None:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_SHA256, "parent certificate provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION",
         "certificate header")
    payload = document["payload"]
    need(payload["schema"] == "TPC324_SOURCE_PROFILE_HOLDOUT_V1" and
         document["payload_sha256"] == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload digest")
    need(payload["parent_lock"]["certificate_sha256"] == PARENT_SHA256,
         "payload parent lock")
    protocol = payload["protocol"]
    expected_panels = {
        panel: {str(scale): list(PANEL_INTERVALS[panel][scale])
                for scale in SCALES}
        for panel in PANEL_NAMES
    }
    need(protocol["source_panels"] == expected_panels and
         protocol["source_scales"] == list(SCALES) and
         protocol["height"] == HEIGHT and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS) and
         protocol["profile"] == "pi_j(G)=lambda_j(G)/tr(G), descending" and
         protocol["paths"] == ["scipy_forward", "numpy_forward",
                               "numpy_reverse"], "protocol")
    need(tuple(payload["exact_small_audit"]["shell"]) == tuple(shell(4)),
         "exact anchor shell")
    need((payload["exact_small_audit"]["direct_energy_digest"],
          payload["exact_small_audit"]["signed_energy_digest"]) ==
         exact_anchor(), "exact anchor")

    indexed: set[tuple[str, int, int, int]] = set()
    class_counts = {name: {label: 0 for label in LABELS}
                    for name in LAW_NAMES}
    panel_counts = {
        panel: {name: {label: 0 for label in LABELS}
                for name in LAW_NAMES}
        for panel in PANEL_NAMES
    }
    energy_counts = {name: {"below_one": 0, "above_one": 0}
                     for name in LAW_NAMES}
    for row in payload["rows"]:
        key = (row["panel"], row["scale"], row["Q"],
               row["kernel_exponent"])
        need(key not in indexed and key[0] in PANEL_NAMES and
             key[1] in SCALES and key[2] in Q_ANCHORS and
             key[3] in EXPONENTS, "row key")
        panel, scale, q0, exponent = key
        lo, hi = PANEL_INTERVALS[panel][scale]
        primes = shell(q0)
        count = scale // 2
        need(row["source_interval"] == [lo, hi] and
             row["source_count"] == count and row["shell"] == primes and
             row["profile_dimension"] == count and
             row["operator_columns"] == count and
             row["operator_rows"] == count * len(primes), "row geometry")
        direct, signed_grams = rebuild_all(panel, scale, q0, exponent)
        direct_profile = profile(direct)
        direct_record = row["direct_profile_paths"][PATH]
        need(isinstance(direct_record["profile_digest"], str) and
             len(direct_record["profile_digest"]) == 64,
             "direct profile digest format")
        for name in LAW_NAMES:
            signs = signs_for(name, primes)
            law = row["laws"][name]
            need(law["signs"] == [int(value) for value in signs],
                 "sign law labels")
            signed_profile = profile(signed_grams[name])
            got = metrics(signed_profile, direct_profile)
            stored = law["paths"][PATH]
            need(isinstance(stored["profile_digest"], str) and
                 len(stored["profile_digest"]) == 64,
                 "signed profile digest format")
            for field in ("tv", "lorenz_ks", "integrated_lorenz",
                          "minimum_prefix", "maximum_prefix"):
                need(close(got[field], float(stored[field])),
                     "replay metric: " + field)
            need(got["majorization"] == stored["majorization"] and
                 got["majorization"] == law["majorization"],
                 "replay majorization")
            need(interval_contains(law["profile_tv_interval"], got["tv"]) and
                 interval_contains(law["profile_ks_interval"],
                                   got["lorenz_ks"]) and
                 interval_contains(law["minimum_prefix_interval"],
                                   got["minimum_prefix"]),
                 "outward intervals")
            class_counts[name][got["majorization"]] += 1
            panel_counts[panel][name][got["majorization"]] += 1
            rho = float(law["energy_ratio_estimate"])
            energy_counts[name]["below_one" if rho < 1.0 else "above_one"] += 1
        indexed.add(key)

    expected = {
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
    need(len(indexed) == 48 and class_counts == expected,
         "profile class census")
    need(panel_counts == {panel: one for panel in PANEL_NAMES},
         "per-panel class census")
    need(energy_counts == {
        "all_plus": {"below_one": 6, "above_one": 42},
        "alternating_index": {"below_one": 42, "above_one": 6},
        "mod4_character": {"below_one": 38, "above_one": 10},
        "half_split": {"below_one": 42, "above_one": 6},
    }, "energy census")
    finite = payload["finite_audit"]
    need(finite["rows"] == 48 and
         finite["panel_rows"] == {panel: 24 for panel in PANEL_NAMES} and
         finite["profile_majorization_counts"] == expected and
         finite["per_panel_profile_majorization_counts"] ==
         {panel: one for panel in PANEL_NAMES} and
         finite["all_plus_strict_majorization_rows"] == 48 and
         float(finite["all_plus_minimum_prefix_lower"]) > 0 and
         finite["replication_match_to_tpc323"] is True and
         finite["fixed_power_credit"] == 0, "finite audit")
    firewall = payload["claim_firewall"]
    need(firewall["TPC324_SOURCE_LOCATION_HOLDOUT"] ==
         "NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS" and
         firewall["TPC324_ALL_PLUS_PROFILE_REPLICATION"] ==
         "NUMERICALLY_CERTIFIED_FINITE_48_OF_48" and
         firewall["TPC324_TRANSLATION_COVARIANCE"] ==
         "PROVED_EXACT_FINITE_CONDITIONAL" and
         firewall["TPC324_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC324_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC324_FULL_GATE_B"] == "OPEN" and
         firewall["TPC324_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    print("TPC324_INDEPENDENT_CHECK=PASS rows=48 panels=2 "
          "all_plus_profile=48/48 per_panel=24/24 "
          "alternative=34/14,42/6,36/12")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC324_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
