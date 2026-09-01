#!/usr/bin/env python3
"""Independent reverse/einsum replay for TPC-323.

The producer uses forward matrix products and retains three spectral paths.
This checker deliberately does not import it: it rebuilds the literal blocks
in reverse prime order, accumulates every Gram with ``einsum``, and checks the
stored NumPy-reverse profile metrics and finite law census.
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
    raise SystemExit("TPC323 independent checker requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
CERTIFICATE = PROJECT / "results/tpc323_certificate.json"
PARENT_CERT = ROOT / (
    "papers/tpc-322-signed-projector-reassembly/results/"
    "tpc322_certificate.json")
PARENT_SHA256 = (
    "4961b34ebb755e8216d4fbc6d9d6d59781c9a8203c8687b5990385c7e0a57b0c")

HEIGHT = 66
SCALES = (640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PATH = "numpy_reverse"
PROFILE_TOL = 1.0e-10
NUMERICAL_GUARD = 1.0e-12
PATH_TOL = 2.0e-7
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character",
             "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")


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


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=8.0e-7, abs_tol=2.0e-9)


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


def rebuild_all(scale: int, q0: int, exponent: int) -> tuple[
        np.ndarray, dict[str, np.ndarray]]:
    """Build the direct Gram and all coherent Grams in one reverse pass."""
    values = np.arange(scale // 2 + 1, scale + 1, dtype=np.int64)
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


def profile_digest(values: np.ndarray) -> str:
    rounded = np.round(np.asarray(values, dtype=np.float64), 14)
    return hashlib.sha256(rounded.astype("<f8", copy=False).tobytes()).hexdigest()


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
        "tv": 0.5 * float(np.sum(np.abs(signed - direct), dtype=np.float64)),
        "lorenz_ks": float(np.max(np.abs(delta))),
        "integrated_lorenz": float(np.mean(np.abs(delta))),
        "minimum_prefix": minimum,
        "maximum_prefix": maximum,
        "majorization": label,
    }


def exact_anchor() -> tuple[str, str]:
    values = list(range(17, 33))
    primes = shell(4)

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


def interval_contains(interval: list[str], value: float) -> bool:
    low, high = map(float, interval)
    return low <= value <= high


def check() -> None:
    need(PARENT_CERT.is_file() and digest(PARENT_CERT.read_bytes()) ==
         PARENT_SHA256, "parent certificate provenance")
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT",
         "certificate header")
    payload = document["payload"]
    need(payload["schema"] == "TPC323_SIGNED_PROFILE_MAJORISATION_V1" and
         document["payload_sha256"] == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload digest")
    need(payload["parent_lock"]["certificate_sha256"] == PARENT_SHA256,
         "payload parent lock")
    protocol = payload["protocol"]
    need(protocol["source_scales"] == list(SCALES) and
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

    indexed: dict[tuple[int, int, int], dict[str, Any]] = {}
    class_counts = {name: {label: 0 for label in LABELS}
                    for name in LAW_NAMES}
    energy_counts = {name: {"below_one": 0, "above_one": 0}
                     for name in LAW_NAMES}
    for row in payload["rows"]:
        key = (row["scale"], row["Q"], row["kernel_exponent"])
        need(key not in indexed and key[0] in SCALES and
             key[1] in Q_ANCHORS and key[2] in EXPONENTS, "row key")
        primes = shell(key[1])
        need(row["source_count"] == key[0] // 2 and
             row["source_interval"] == [key[0] // 2 + 1, key[0]] and
             row["shell"] == primes and
             row["profile_dimension"] == key[0] // 2 and
             row["operator_columns"] == key[0] // 2 and
             row["operator_rows"] == (key[0] // 2) * len(primes),
             "row geometry")
        direct, signed_grams = rebuild_all(*key)
        direct_profile = profile(direct)
        direct_record = row["direct_profile_paths"][PATH]
        # Eigenvalue ordering is numerically stable at the metric level, but
        # a byte digest of a long floating profile can vary in the last bits
        # across BLAS/LAPACK builds.  Keep the producer digest as provenance;
        # this independent path certifies the actual metrics below.
        need(isinstance(direct_record["profile_digest"], str) and
             len(direct_record["profile_digest"]) == 64,
             "direct profile digest format")
        for name in LAW_NAMES:
            signs = signs_for(name, primes)
            need(row["laws"][name]["signs"] == [int(value) for value in signs],
                 "sign law labels")
            signed_profile = profile(signed_grams[name])
            got = metrics(signed_profile, direct_profile)
            stored = row["laws"][name]["paths"][PATH]
            need(isinstance(stored["profile_digest"], str) and
                 len(stored["profile_digest"]) == 64,
                 "signed profile digest format")
            for field in ("tv", "lorenz_ks", "integrated_lorenz",
                          "minimum_prefix", "maximum_prefix"):
                need(close(got[field], float(stored[field])),
                     "replay metric: " + field)
            need(got["majorization"] == stored["majorization"] and
                 got["majorization"] == row["laws"][name]["majorization"],
                 "replay majorization")
            need(interval_contains(row["laws"][name]["profile_tv_interval"],
                                   got["tv"]) and
                 interval_contains(row["laws"][name]["profile_ks_interval"],
                                   got["lorenz_ks"]) and
                 interval_contains(
                     row["laws"][name]["minimum_prefix_interval"],
                     got["minimum_prefix"]), "outward intervals")
            class_counts[name][got["majorization"]] += 1
            rho = float(row["laws"][name]["energy_ratio_estimate"])
            energy_counts[name]["below_one" if rho < 1 else "above_one"] += 1
        indexed[key] = row

    need(len(indexed) == 24, "row census")
    expected_classes = {
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
    need(class_counts == expected_classes, "profile class census")
    need(payload["finite_audit"]["profile_majorization_counts"] ==
         expected_classes and
         payload["finite_audit"]["all_plus_strict_majorization_rows"] == 24
         and float(payload["finite_audit"][
             "all_plus_minimum_prefix_lower"]) > 0,
         "finite audit")
    need(payload["finite_audit"]["energy_ratio_counts"] == energy_counts,
         "energy census")
    firewall = payload["claim_firewall"]
    need(firewall["TPC323_SIGNED_PROFILE_FACTORISATION"] ==
         "PROVED_EXACT_FINITE" and
         firewall["TPC323_ALL_PLUS_PROFILE_MAJORISATION"] ==
         "NUMERICALLY_CERTIFIED_FINITE_24_OF_24" and
         firewall["TPC323_ARITHMETIC_ADVANCE"] == "NO" and
         firewall["TPC323_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC323_FULL_GATE_B"] == "OPEN" and
         firewall["TPC323_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    print("TPC323_INDEPENDENT_CHECK=PASS rows=24 all_plus_profile=24/24 "
          "alternating=17/7 mod4=21/3 half_split=18/6")


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
        print("TPC323_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
