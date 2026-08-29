#!/usr/bin/env python3
"""Independent source-first replay for TPC-299."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import multiprocessing as mp_pool
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-299-native-profile-budget-frontier"
PARENT_RESULT = ROOT / (
    "papers/tpc-298-profile-angle-dimension-ladder/results/"
    "tpc298_certificate.json")
LABEL_RESULT = ROOT / (
    "papers/tpc-295-source-correlation-image-audit/results/"
    "tpc295_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc299_certificate.json"

PARENT_RESULT_SHA256 = (
    "30650bc9e7fb2d942c7a4c03de0b5657040653fefb500c2b585bdea3013a7bf1")
LABEL_RESULT_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS")
SCHEMA = "TPC299_NATIVE_PROFILE_BUDGET_FRONTIER_CERTIFICATE_V1"
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
MODULI = (1000000007, 998244353)
MP_DPS = 70
CHECK_RADIUS = mp.mpf("1e-10")
TARGET_RMS = mp.mpf("0.5")

engine_spec = importlib.util.spec_from_file_location(
    "independent_tpc299_engine", ENGINE_CODE)
if engine_spec is None or engine_spec.loader is None:
    raise RuntimeError("engine unavailable")
ENGINE = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(ENGINE)


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


def inside(value: mp.mpf, interval: list[str]) -> bool:
    lo, hi = map(mp.mpf, interval)
    tolerance = CHECK_RADIUS * max(mp.mpf(1), abs(value))
    return lo - tolerance <= value <= hi + tolerance


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def as_mp(value: Fraction | int) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    lam = Fraction(0) if power is None else Fraction(1, power[1])
    return lam - sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                      if value % d == 0), Fraction(0))


def source_first(indices: list[int], values: list[Fraction], height: int,
                 prime: int, exponent: int) -> list[Fraction]:
    output = [Fraction(0) for _ in indices]
    for source, coefficient in zip(indices, values):
        if source % prime == 0:
            continue
        for position, target in enumerate(indices):
            if target == source or target % prime == 0:
                continue
            centered = Fraction(int(target % prime == source % prime), 1)
            centered -= Fraction(1, prime - 1)
            output[position] += (prime * ENGINE.kernel(target - source,
                                 height, exponent) * centered * coefficient)
    return output


def norm_squared(vector: mp.matrix) -> mp.mpf:
    return mp.fsum(vector[i] ** 2 for i in range(len(vector)))


def ls(W: mp.matrix, M: mp.matrix,
       b: mp.matrix) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    c = mp.qr_solve(W, b)[0]
    residual = W * c - b
    residual_squared = norm_squared(residual)
    source_squared = (c.T * M * c)[0]
    return c, residual_squared, source_squared


def ridge(W: mp.matrix, M: mp.matrix, b: mp.matrix,
          lam: mp.mpf) -> tuple[mp.matrix, mp.mpf, mp.mpf, mp.mpf]:
    c = mp.lu_solve(W.T * W + lam * M, W.T * b)
    residual = W * c - b
    residual_squared = norm_squared(residual)
    source_squared = (c.T * M * c)[0]
    stationarity = W.T * residual + lam * M * c
    stationarity_max = max(abs(stationarity[i])
                            for i in range(len(stationarity)))
    return c, residual_squared, source_squared, stationarity_max


def frontier(W: mp.matrix, M: mp.matrix, b: mp.matrix,
             beta_norm_squared: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    target = TARGET_RMS ** 2 * len(b)
    _, least_residual, _ = ls(W, M, b)
    need(least_residual <= target + mp.mpf("1e-45"),
         "independent threshold infeasible")
    lo, hi = mp.mpf(0), mp.mpf(1)
    while ridge(W, M, b, hi)[1] < target:
        hi *= 2
        need(hi < mp.mpf("1e100"), "independent bracket overflow")
    for _ in range(190):
        mid = (lo + hi) / 2
        if ridge(W, M, b, mid)[1] < target:
            lo = mid
        else:
            hi = mid
    lam = (lo + hi) / 2
    _, residual_squared, source_squared, stationarity = ridge(
        W, M, b, lam)
    need(abs(residual_squared - target) < mp.mpf("1e-40"),
         "independent frontier residual")
    need(stationarity < mp.mpf("1e-40"),
         "independent KKT stationarity")
    return (mp.sqrt(residual_squared / len(b)),
            source_squared / beta_norm_squared, lam)


def one(item: tuple[dict[str, Any], dict[str, Any],
                     dict[str, Any]]) -> dict[str, Any]:
    parent_row, actual, label_row = item
    mp.mp.dps = MP_DPS
    x = int(parent_row["scale"])
    height = int(parent_row["H"])
    q0 = int(parent_row["Q"])
    cutoff = int(parent_row["comparison_cutoff_z"])
    exponent = int(parent_row["kernel_exponent"])
    indices = list(range(x // 2 + 1, x + 1))
    _, frozen, _ = ENGINE.source_weights(x, cutoff)
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    columns = [source_first(indices, frozen, height, q, exponent)
               for q in shell]
    profiles = [[beta(t, z) for z in PROFILE_CUTOFFS] for t in indices]
    A = mp.matrix([[as_mp(columns[j][i]) for j in range(len(shell))]
                   for i in range(len(indices))])
    U = mp.matrix([[as_mp(profiles[i][j])
                    for j in range(len(PROFILE_CUTOFFS))]
                   for i in range(len(indices))])
    V = A.T * U
    M = U.T * U
    beta_norm_squared = mp.fsum(as_mp(v) ** 2 for v in frozen)
    labels = {
        "minimum": [int(v) for v in label_row["minimum_signed_label"]],
        "maxcut": [int(v) for v in label_row["maxcut_label"]],
        "plus": [1] * len(shell),
    }
    prefix_count = min(len(shell), len(PROFILE_CUTOFFS))
    residuals: dict[str, list[mp.mpf]] = {name: [] for name in labels}
    for position, k in enumerate(range(1, prefix_count + 1)):
        W = V[:, :k]
        Mk = M[:k, :k]
        stored = actual["least_squares_prefixes"][position]
        need(stored["k"] == k and
             stored["cutoff"] == PROFILE_CUTOFFS[k - 1],
             "independent prefix ordering")
        for name, label in labels.items():
            b = mp.matrix(label)
            _, residual_squared, source_squared = ls(W, Mk, b)
            rms = mp.sqrt(residual_squared / len(shell))
            ratio = source_squared / beta_norm_squared
            residuals[name].append(rms)
            saved = stored["targets"][name]
            need(inside(rms, saved["rms_residual"]),
                 "independent residual interval: " + name)
            need(inside(source_squared, saved["source_norm_squared"]),
                 "independent source interval: " + name)
            need(inside(ratio, saved["source_budget_ratio"]),
                 "independent budget interval: " + name)
            if position:
                need(rms <= residuals[name][-2] + mp.mpf("1e-45"),
                     "independent residual monotonicity")
    half = {
        name: next((i + 1 for i, value in enumerate(residuals[name])
                    if value <= TARGET_RMS), None)
        for name in labels
    }
    need(all(value is not None for value in half.values()),
         "independent half dimension")
    need(actual["half_rms_dimensions"] == {
        name: int(value) for name, value in half.items()},
         "independent half dimension mismatch")
    threshold_raw: dict[str, tuple[mp.mpf, mp.mpf, mp.mpf]] = {}
    full_raw: dict[str, tuple[mp.mpf, mp.mpf, mp.mpf]] = {}
    for name, label in labels.items():
        b = mp.matrix(label)
        k = int(half[name])
        threshold_raw[name] = frontier(
            V[:, :k], M[:k, :k], b, beta_norm_squared)
        full_raw[name] = frontier(
            V[:, :prefix_count], M[:prefix_count, :prefix_count], b,
            beta_norm_squared)
        for key, raw in (("threshold_budget_frontiers", threshold_raw[name]),
                         ("full_prefix_budget_frontiers", full_raw[name])):
            saved = actual[key][name]
            need(saved["k"] == (k if key.startswith("threshold") else
                                prefix_count), "independent frontier k")
            need(inside(raw[0], saved["target_rms"]),
                 "independent frontier RMS")
            need(inside(raw[1], saved["source_budget_ratio"]),
                 "independent frontier budget")
    need(actual["shell"] == shell, "independent shell")
    need(actual["tested_prefix_count"] == prefix_count,
         "independent prefix count")
    weighted = threshold_raw["minimum"][1]
    positive = threshold_raw["plus"][1]
    full_weighted = full_raw["minimum"][1]
    return {
        "weighted_threshold": weighted,
        "positive_threshold": positive,
        "full_weighted": full_weighted,
        "gap": weighted / positive,
    }


def main() -> int:
    try:
        raw = RESULT.read_bytes()
        data = json.loads(raw)
        need(raw == canonical(data), "certificate canonicality")
        need(data.get("certificate_version") == 1 and
             data.get("claim_status") == STATUS, "certificate header")
        need(data["payload"].get("schema") == SCHEMA, "certificate schema")
        parent_raw = PARENT_RESULT.read_bytes()
        labels_raw = LABEL_RESULT.read_bytes()
        need(digest(parent_raw) == PARENT_RESULT_SHA256,
             "TPC-298 provenance")
        need(digest(labels_raw) == LABEL_RESULT_SHA256,
             "TPC-295 provenance")
        need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
             "engine provenance")
        parent = json.loads(parent_raw)
        labels = json.loads(labels_raw)
        parent_rows = {row_key(row): row for row in parent["payload"]["rows"]}
        label_rows = {row_key(row): row for row in labels["payload"]["rows"]}
        need(len(parent_rows) == 18 and len(label_rows) == 18,
             "independent row census")
        items = []
        for row in parent["payload"]["rows"]:
            key = row_key(row)
            need(key in label_rows, "independent row alignment")
            actual = next(candidate for candidate in data["payload"]["rows"]
                          if row_key(candidate) == key)
            items.append((row, actual, label_rows[key]))
        workers = min(len(items), max(1, os.cpu_count() or 1))
        if workers > 1:
            try:
                with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                    checked = pool.map(one, items)
            except (AttributeError, OSError, RuntimeError):
                checked = [one(item) for item in items]
        else:
            checked = [one(item) for item in items]
        need(len(checked) == 18, "independent checked census")
        weighted = [item["weighted_threshold"] for item in checked]
        positive = [item["positive_threshold"] for item in checked]
        full_weighted = [item["full_weighted"] for item in checked]
        gaps = [item["gap"] for item in checked]
        need(min(weighted) > mp.mpf("9e-5"), "independent weighted floor")
        need(sum(v > mp.mpf("5e-4") for v in weighted) == 15,
             "independent mid floor count")
        need(sum(v > mp.mpf("1e-3") for v in weighted) == 14,
             "independent obstruction count")
        need(sum(v > mp.mpf("1e-3") for v in full_weighted) == 11,
             "independent full obstruction count")
        need(max(positive) < mp.mpf("1e-4"),
             "independent positive ceiling")
        need(min(gaps) > mp.mpf("20"), "independent gap")
        audit = data["payload"]["finite_audit"]
        need(audit["tested_prefix_entries"] == 219 and
             audit["weighted_threshold_budget_floor_rows"] == 15 and
             audit["weighted_threshold_budget_above_5e-4_rows"] == 15 and
             audit["weighted_threshold_budget_above_1e-3_rows"] == 14 and
             audit["weighted_full_prefix_budget_above_1e-3_rows"] == 11 and
             audit["all_positive_threshold_budget_ceiling_rows"] == 18 and
             audit["weighted_to_positive_gap_floor_rows"] == 18,
             "independent aggregate census")
        print("TPC299_INDEPENDENT_CHECK=PASS rows=18 prefixes=219 "
              "weighted_gt_1e-3=14 full_gt_1e-3=11 plus_lt_1e-4=18 "
              "gap_gt_20=18")
        return 0
    except (Failure, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC299_INDEPENDENT_CHECK=FAIL " + str(error),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
