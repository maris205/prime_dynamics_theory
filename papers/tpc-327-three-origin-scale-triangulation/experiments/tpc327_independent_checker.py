#!/usr/bin/env python3
"""Independent literal replay for the TPC-327 third-origin panel.

This checker does not import the TPC-327 producer.  It reconstructs the
deleted-diagonal blocks from the displayed formula, accumulates Gram matrices
in reverse order, and independently recomputes the three-origin envelope
range recorded in the certificate.
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

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-327-three-origin-scale-triangulation"
CERTIFICATE = PROJECT / "results/tpc327_certificate.json"
PARENT_CERTIFICATE = ROOT / "papers/tpc-326-cross-origin-scale-replication/results/tpc326_certificate.json"
GRANDPARENT_CERTIFICATE = ROOT / "papers/tpc-325-scale-ladder-profile/results/tpc325_certificate.json"
PARENT_CERT_SHA256 = "9b52f8f74fe2edd5fa8c512fcb7a87c9bfef06cb4e888c93945419006bcff2ec"
GRANDPARENT_CERT_SHA256 = "7afe4fcf56b4432dcf2e5320479cd144a53cdcea29ccbd5cb26c558fd9f06766"

ORIGIN = 20001
ORIGINS = (12001, 16001, 20001)
SCALES = (320, 640, 1280, 2560)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
LABELS = ("SIGNED_MAJORISES_DIRECT", "DIRECT_MAJORISES_SIGNED",
          "MIXED", "UNRESOLVED")
TOL = 2.0e-6
EXACT_INTERVAL = (20001, 20016)
EXACT_DIRECT_DIGEST = "97225bdbd0cb628956b3701748cec3b2eca7b4d559c0d0b42044300f7c26889b"
EXACT_SIGNED_DIGEST = "f38ac7229026dcd2ada592c5b245871d3ef1856e4bac21c86010e89766a9f9f7"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load_payload(path: Path, expected: str | None = None) -> dict[str, object]:
    raw = path.read_bytes()
    if expected is not None:
        need(digest(raw) == expected, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    if path == CERTIFICATE:
        need(document.get("claim_status") ==
             "NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION",
             "certificate status")
        payload = document.get("payload", {})
        need(document.get("payload_sha256") == hashlib.sha256(
            canonical(payload)).hexdigest(), "certificate payload hash")
    return document["payload"]


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * ((limit - p * p) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def blocks(scale: int, q0: int, exponent: int) -> tuple[list[int], list[np.ndarray]]:
    values = np.arange(ORIGIN, ORIGIN + scale // 2, dtype=np.int64)
    differences = values[:, None] - values[None, :]
    dd = differences.astype(np.float64)
    kernel = (float(HEIGHT) ** (2 * exponent) /
              (HEIGHT * HEIGHT + dd * dd) ** exponent)
    result = []
    for p in shell(q0):
        valid = ((differences != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        centered = ((differences % p == 0).astype(np.float64) -
                    1.0 / (p - 1))
        result.append(p * kernel * centered * valid)
    return shell(q0), result


def profile(gram: np.ndarray) -> np.ndarray:
    values = np.linalg.eigvalsh((gram + gram.T) / 2.0)
    values = np.maximum(values, 0.0)
    total = float(np.sum(values, dtype=np.float64))
    need(total > 0 and math.isfinite(total), "spectral trace")
    answer = values[::-1] / total
    need(abs(float(np.sum(answer)) - 1.0) < 4.0e-14, "profile sum")
    return answer


def metric(signed: np.ndarray, direct: np.ndarray) -> tuple[str, float, float]:
    delta = np.cumsum(signed - direct, dtype=np.float64)[:-1]
    lo, hi = float(np.min(delta)), float(np.max(delta))
    if lo >= -1.0e-10 and hi > 1.0e-10:
        label = "SIGNED_MAJORISES_DIRECT"
    elif hi <= 1.0e-10 and lo < -1.0e-10:
        label = "DIRECT_MAJORISES_SIGNED"
    elif lo < -1.0e-10 and hi > 1.0e-10:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    tv = 0.5 * float(np.sum(np.abs(signed - direct), dtype=np.float64))
    return label, lo, tv


def signs(primes: list[int]) -> dict[str, np.ndarray]:
    m = len(primes)
    return {
        "all_plus": np.ones(m, dtype=np.float64),
        "alternating_index": np.asarray(
            [1 if i % 2 == 0 else -1 for i in range(m)], dtype=np.float64),
        "mod4_character": np.asarray(
            [1 if p % 4 == 1 else -1 for p in primes], dtype=np.float64),
        "half_split": np.asarray(
            [1 if i < m / 2 else -1 for i in range(m)], dtype=np.float64),
    }


def exact_anchor() -> tuple[str, str]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = shell(4)
    data = [[[Fraction(0) for _ in values] for _ in values]
            for _ in primes]
    for i, p in enumerate(primes):
        for u, value_u in enumerate(values):
            for t, value_t in enumerate(values):
                if value_u == value_t or value_u % p == 0 or value_t % p == 0:
                    continue
                centered = Fraction(1 if (value_u - value_t) % p == 0 else 0)
                centered -= Fraction(1, p - 1)
                data[i][u][t] = p * Fraction(HEIGHT * HEIGHT,
                    HEIGHT * HEIGHT + (value_u - value_t) ** 2) * centered
    gram = [[sum((data[i][u][t] * data[j][u][t]
                  for u in range(len(values)) for t in range(len(values))),
                 Fraction(0)) for j in range(len(primes))]
            for i in range(len(primes))]
    direct = sum((gram[i][i] for i in range(len(primes))), Fraction(0))
    law = [1 if i % 2 == 0 else -1 for i in range(len(primes))]
    signed = sum((law[i] * law[j] * gram[i][j]
                  for i in range(len(primes)) for j in range(len(primes))),
                 Fraction(0))

    def fraction_digest(value: Fraction) -> str:
        return hashlib.sha256(
            f"{value.numerator}/{value.denominator}\n".encode("ascii")
        ).hexdigest()

    return fraction_digest(direct), fraction_digest(signed)


def check() -> None:
    payload = load_payload(CERTIFICATE)
    need(payload["schema"] == "TPC327_THREE_ORIGIN_SCALE_TRIANGULATION_V1",
         "schema")
    protocol = payload["protocol"]
    need(protocol["source_origin"] == ORIGIN and
         protocol["origins"] == list(ORIGINS) and
         protocol["source_scales"] == list(SCALES) and
         protocol["Q_anchors"] == list(Q_ANCHORS) and
         protocol["kernel_exponents"] == list(EXPONENTS), "protocol")
    rows = payload["rows"]
    need(len(rows) == 32, "row count")
    counts = {name: {label: 0 for label in LABELS} for name in LAW_NAMES}
    energy = {name: {"below_one": 0, "above_one": 0} for name in LAW_NAMES}
    summaries = {scale: {"tv": [], "energy": []} for scale in SCALES}
    for row in rows:
        scale, q0, exponent = row["scale"], row["Q"], row["kernel_exponent"]
        need(scale in SCALES and q0 in Q_ANCHORS and exponent in EXPONENTS,
             "row protocol")
        need(row["source_interval"] == [ORIGIN, ORIGIN + scale // 2 - 1],
             "source interval")
        primes, data = blocks(scale, q0, exponent)
        direct = np.zeros((len(data[0]), len(data[0])), dtype=np.float64)
        for block in reversed(data):
            direct += np.einsum("ij,ik->jk", block, block, optimize=False)
        direct = (direct + direct.T) / 2.0
        direct_profile = profile(direct)
        for name, vector in signs(primes).items():
            coherent = np.zeros_like(data[0])
            for block, sign in zip(reversed(data), reversed(vector)):
                coherent += float(sign) * block
            signed = np.einsum("ij,ik->jk", coherent, coherent, optimize=False)
            signed = (signed + signed.T) / 2.0
            signed_profile = profile(signed)
            label, minimum, tv = metric(signed_profile, direct_profile)
            recorded = row["laws"][name]
            counts[name][label] += 1
            need(recorded["majorization"] == label, "label replay")
            need(float(recorded["profile_tv_interval"][0]) - TOL <= tv <=
                 float(recorded["profile_tv_interval"][1]) + TOL,
                 "TV interval")
            need(float(recorded["minimum_prefix_interval"][0]) - TOL <= minimum <=
                 float(recorded["minimum_prefix_interval"][1]) + TOL,
                 "prefix interval")
            ratio = float(np.trace(signed) / np.trace(direct))
            energy[name]["below_one" if ratio < 1.0 else "above_one"] += 1
            if name == "all_plus":
                summaries[scale]["tv"].append(tv)
                summaries[scale]["energy"].append(ratio)
    need(counts == payload["finite_audit"]["profile_majorization_counts"],
         "profile census")
    need(energy == payload["finite_audit"]["energy_ratio_counts"],
         "energy census")
    parent2 = load_payload(PARENT_CERTIFICATE, PARENT_CERT_SHA256)
    parent1 = load_payload(GRANDPARENT_CERTIFICATE, GRANDPARENT_CERT_SHA256)
    need(counts == parent1["finite_audit"]["profile_majorization_counts"] and
         counts == parent2["finite_audit"]["profile_majorization_counts"],
         "both parent profile censuses")
    need(energy == parent1["finite_audit"]["energy_ratio_counts"] and
         energy == parent2["finite_audit"]["energy_ratio_counts"],
         "both parent energy censuses")

    tv_by_origin = {
        12001: {x["scale"]: float(x["all_plus_tv_lower_envelope"])
                for x in parent1["scale_ladder"]},
        16001: {x["scale"]: float(x["all_plus_tv_lower_envelope"])
                for x in parent2["scale_ladder"]},
        20001: {scale: min(values["tv"]) for scale, values in summaries.items()},
    }
    energy_by_origin = {
        12001: {x["scale"]: float(x["all_plus_energy_ratio_max"])
                for x in parent1["scale_ladder"]},
        16001: {x["scale"]: float(x["all_plus_energy_ratio_max"])
                for x in parent2["scale_ladder"]},
        20001: {scale: max(values["energy"])
                for scale, values in summaries.items()},
    }
    max_tv = 0.0
    max_energy = 0.0
    for scale in SCALES:
        max_tv = max(max_tv, max(tv_by_origin[o][scale] for o in ORIGINS) -
                     min(tv_by_origin[o][scale] for o in ORIGINS))
        max_energy = max(max_energy,
                         max(energy_by_origin[o][scale] for o in ORIGINS) -
                         min(energy_by_origin[o][scale] for o in ORIGINS))
    ensemble = payload["origin_ensemble"]
    need(abs(float(ensemble["max_pairwise_tv_difference"]) - max_tv) < TOL and
         abs(float(ensemble["max_pairwise_energy_difference"]) - max_energy) < TOL,
         "ensemble range replay")
    need(ensemble["all_pairwise_tv_within_threshold"] is True and
         ensemble["all_pairwise_energy_within_threshold"] is True and
         ensemble["nonzero_finite_origin_spread"] is True, "ensemble flags")
    need(exact_anchor() == (EXACT_DIRECT_DIGEST, EXACT_SIGNED_DIGEST),
         "exact anchor")
    print("TPC327_INDEPENDENT_CHECK=PASS rows=32 origins=3 "
          "reverse_einsum=1 both_parent_census=1 exact_anchor=1")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check()
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC327_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
