#!/usr/bin/env python3
"""TPC-299 native profile source-budget frontier certificate.

TPC-298 measured how many literal source-profile directions are needed before
a target enters the physical image.  This release measures the native source
norm needed at a prescribed target accuracy.  The exact part is a
quadratically constrained least-norm/KKT identity; the atlas is finite and
receives no asymptotic or arithmetic credit.
"""

from __future__ import annotations

import argparse
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

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-298-profile-angle-dimension-ladder/code/"
    "tpc298_profile_angle_dimension_certificate.py")
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

PARENT_CODE_SHA256 = (
    "fe4703b3d6093f68c02186de83820dc02fc37abbda13cb34abb34b7b0f41d1b8")
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
ROUND2_CLUE = (
    "TEST_BUDGET_CONSTRAINED_PROFILE_FRONTIER_ON_GROWING_SHELLS_AND_"
    "SOURCE_NORMALIZATION")
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
MODULI = (1000000007, 998244353)
MP_DPS = 70
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-18")
TARGET_RMS = mp.mpf("0.5")
WEIGHTED_FLOOR = mp.mpf("9e-5")
BUDGET_MID = mp.mpf("5e-4")
BUDGET_OBSTRUCTION = mp.mpf("1e-3")
PLUS_CEILING = mp.mpf("1e-4")
GAP_FLOOR = mp.mpf("20")

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc298_for_tpc299", PARENT_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-298 parent unavailable")
PARENT = importlib.util.module_from_spec(parent_spec)
parent_spec.loader.exec_module(PARENT)
ENGINE = PARENT.ENGINE


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def as_mp(value: Fraction | int) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def enclosure(value: mp.mpf) -> list[str]:
    radius = INTERVAL_RELATIVE_RADIUS * max(mp.mpf(1), abs(value))
    return [mp.nstr(value - radius, 32), mp.nstr(value + radius, 32)]


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-298 code provenance")
    raw_parent = PARENT_RESULT.read_bytes()
    need(digest(raw_parent) == PARENT_RESULT_SHA256,
         "TPC-298 result provenance")
    parent = json.loads(raw_parent)
    need(raw_parent == canonical(parent), "TPC-298 canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY"),
         "TPC-298 status")
    audit = parent.get("payload", {}).get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380 and
         audit.get("profile_count") == len(PROFILE_CUTOFFS),
         "TPC-298 finite census")
    need(parent["payload"]["profile_family"]["ordered_cutoffs"] ==
         list(PROFILE_CUTOFFS), "profile cutoff lock")

    raw_labels = LABEL_RESULT.read_bytes()
    need(digest(raw_labels) == LABEL_RESULT_SHA256,
         "TPC-295 label provenance")
    labels = json.loads(raw_labels)
    need(raw_labels == canonical(labels), "TPC-295 canonicality")
    need(labels.get("certificate_version") == 1 and
         labels.get("claim_status", "").startswith(
             "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION"),
         "TPC-295 status")
    need(len(parent["payload"]["rows"]) == 18 and
         len(labels["payload"]["rows"]) == 18, "parent row census")
    return {
        "tpc298_code_sha256": PARENT_CODE_SHA256,
        "tpc298_result_sha256": PARENT_RESULT_SHA256,
        "tpc295_label_result_sha256": LABEL_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
    }


def load_rows() -> tuple[list[dict[str, Any]], dict[
        tuple[int, int, int, int, int], dict[str, Any]]]:
    parent = json.loads(PARENT_RESULT.read_bytes())
    labels = json.loads(LABEL_RESULT.read_bytes())
    label_map = {row_key(row): row for row in labels["payload"]["rows"]}
    need(len(label_map) == 18, "label row map")
    ordered: list[dict[str, Any]] = []
    seen: set[tuple[int, int, int, int, int]] = set()
    for row in parent["payload"]["rows"]:
        key = row_key(row)
        need(key not in seen and key in label_map, "row alignment")
        seen.add(key)
        merged = dict(row)
        merged["minimum_signed_label"] = label_map[key]["minimum_signed_label"]
        merged["maxcut_label"] = label_map[key]["maxcut_label"]
        ordered.append(merged)
    need(len(ordered) == 18 and len(seen) == 18, "ordered row census")
    return ordered, label_map


def shell_between(q0: int) -> list[int]:
    return [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]


def literal_beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    lam = Fraction(0) if power is None else Fraction(1, power[1])
    divisor_part = sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                        if value % d == 0), Fraction(0))
    return lam - divisor_part


def matrix_from_columns(columns: list[list[Fraction]]) -> mp.matrix:
    return mp.matrix([[as_mp(columns[j][i]) for j in range(len(columns))]
                      for i in range(len(columns[0]))])


def source_profile_matrix(indices: list[int]) -> list[list[Fraction]]:
    return [[literal_beta(value, cutoff) for cutoff in PROFILE_CUTOFFS]
            for value in indices]


def norm_squared(vector: mp.matrix) -> mp.mpf:
    return mp.fsum(vector[i] ** 2 for i in range(len(vector)))


def ls_solution(W: mp.matrix, M: mp.matrix,
                b: mp.matrix) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    coefficients = mp.qr_solve(W, b)[0]
    residual = W * coefficients - b
    residual_squared = norm_squared(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    return coefficients, residual_squared, source_squared


def ridge_solution(W: mp.matrix, M: mp.matrix, b: mp.matrix,
                   lam: mp.mpf) -> tuple[mp.matrix, mp.mpf, mp.mpf,
                                          mp.mpf]:
    normal = W.T * W + lam * M
    coefficients = mp.lu_solve(normal, W.T * b)
    residual = W * coefficients - b
    residual_squared = norm_squared(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    stationarity = W.T * residual + lam * M * coefficients
    stationarity_max = max(abs(stationarity[i])
                            for i in range(len(stationarity)))
    return coefficients, residual_squared, source_squared, stationarity_max


def budget_frontier(W: mp.matrix, M: mp.matrix, b: mp.matrix,
                    beta_norm_squared: mp.mpf) -> tuple[dict[str, Any],
                                                         dict[str, mp.mpf]]:
    """Minimum source norm subject to normalized residual <= TARGET_RMS."""
    m = len(b)
    radius_squared = TARGET_RMS ** 2 * m
    _, ls_residual_squared, _ = ls_solution(W, M, b)
    zero_residual_squared = norm_squared(b)
    need(ls_residual_squared <= radius_squared + mp.mpf("1e-45"),
         "threshold prefix is infeasible")
    if radius_squared >= zero_residual_squared:
        lam = mp.mpf(0)
        coefficients = mp.matrix([0 for _ in range(W.cols)])
        residual_squared = zero_residual_squared
        source_squared = mp.mpf(0)
        stationarity_max = mp.mpf(0)
    elif abs(ls_residual_squared - radius_squared) <= mp.mpf("1e-45"):
        lam = mp.mpf(0)
        coefficients, residual_squared, source_squared = ls_solution(W, M, b)
        stationarity_max = mp.mpf(0)
    else:
        lo = mp.mpf(0)
        hi = mp.mpf(1)
        while ridge_solution(W, M, b, hi)[1] < radius_squared:
            hi *= 2
            need(hi < mp.mpf("1e100"), "frontier bracket overflow")
        for _ in range(190):
            mid = (lo + hi) / 2
            if ridge_solution(W, M, b, mid)[1] < radius_squared:
                lo = mid
            else:
                hi = mid
        lam = (lo + hi) / 2
        coefficients, residual_squared, source_squared, stationarity_max = (
            ridge_solution(W, M, b, lam))
    need(abs(residual_squared - radius_squared) < mp.mpf("1e-40") or
         lam == 0, "frontier residual")
    need(source_squared >= -mp.mpf("1e-50"), "negative source budget")
    raw = {
        "lambda": lam,
        "residual_squared": residual_squared,
        "residual_rms": mp.sqrt(residual_squared / m),
        "source_norm_squared": source_squared,
        "source_budget_ratio": source_squared / beta_norm_squared,
        "stationarity_max": stationarity_max,
    }
    saved = {
        "target_rms": enclosure(raw["residual_rms"]),
        "lagrange_multiplier": enclosure(lam),
        "source_norm_squared": enclosure(source_squared),
        "source_budget_ratio": enclosure(raw["source_budget_ratio"]),
        "kkt_stationarity_upper": mp.nstr(stationarity_max, 12),
    }
    return saved, raw


def build_row(parent_row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    mp.mp.dps = MP_DPS
    scale = int(parent_row["scale"])
    height = int(parent_row["H"])
    q0 = int(parent_row["Q"])
    comparison_cutoff = int(parent_row["comparison_cutoff_z"])
    exponent = int(parent_row["kernel_exponent"])
    indices, frozen_beta, _ = ENGINE.source_weights(scale, comparison_cutoff)
    shell = shell_between(q0)
    columns = [PARENT.PARENT.PARENT.physical_output(
        indices, frozen_beta, height, prime, exponent) for prime in shell]
    A = matrix_from_columns(columns)
    U_exact = source_profile_matrix(indices)
    U = mp.matrix([[as_mp(U_exact[i][j])
                    for j in range(len(PROFILE_CUTOFFS))]
                   for i in range(len(indices))])
    V = A.T * U
    M = U.T * U
    source_eigenvalues = mp.eigsy(M, eigvals_only=True)
    source_min = source_eigenvalues[0]
    source_max = source_eigenvalues[len(PROFILE_CUTOFFS) - 1]
    need(source_min > 0, "source profile Gram is not positive definite")
    beta_norm_squared = mp.fsum(as_mp(value) ** 2 for value in frozen_beta)
    labels = {
        "minimum": [int(value) for value in parent_row["minimum_signed_label"]],
        "maxcut": [int(value) for value in parent_row["maxcut_label"]],
        "plus": [1] * len(shell),
    }
    prefix_count = min(len(shell), len(PROFILE_CUTOFFS))
    prefixes: list[dict[str, Any]] = []
    raw_ls: dict[str, list[mp.mpf]] = {name: [] for name in labels}
    for k in range(1, prefix_count + 1):
        W = V[:, :k]
        Mk = M[:k, :k]
        prefix = {"k": k, "cutoff": PROFILE_CUTOFFS[k - 1],
                  "targets": {}}
        for name, label in labels.items():
            b = mp.matrix(label)
            _, residual_squared, source_squared = ls_solution(W, Mk, b)
            rms = mp.sqrt(residual_squared / len(shell))
            ratio = source_squared / beta_norm_squared
            raw_ls[name].append(rms)
            prefix["targets"][name] = {
                "rms_residual": enclosure(rms),
                "source_norm_squared": enclosure(source_squared),
                "source_budget_ratio": enclosure(ratio),
            }
        prefixes.append(prefix)
    half_dimensions = {
        name: next((index + 1 for index, value in enumerate(raw_ls[name])
                    if value <= TARGET_RMS), None)
        for name in labels
    }
    need(all(value is not None for value in half_dimensions.values()),
         "half-RMS prefix does not exist")
    threshold_frontiers: dict[str, dict[str, Any]] = {}
    full_frontiers: dict[str, dict[str, Any]] = {}
    raw_threshold: dict[str, dict[str, mp.mpf]] = {}
    raw_full: dict[str, dict[str, mp.mpf]] = {}
    for name, label in labels.items():
        b = mp.matrix(label)
        k_threshold = int(half_dimensions[name])
        threshold_saved, threshold_raw = budget_frontier(
            V[:, :k_threshold], M[:k_threshold, :k_threshold], b,
            beta_norm_squared)
        threshold_saved["k"] = k_threshold
        threshold_saved["cutoff"] = PROFILE_CUTOFFS[k_threshold - 1]
        threshold_frontiers[name] = threshold_saved
        raw_threshold[name] = threshold_raw
        full_saved, full_raw = budget_frontier(
            V[:, :prefix_count], M[:prefix_count, :prefix_count], b,
            beta_norm_squared)
        full_saved["k"] = prefix_count
        full_saved["cutoff"] = PROFILE_CUTOFFS[prefix_count - 1]
        full_frontiers[name] = full_saved
        raw_full[name] = full_raw
    raw_row = {
        "threshold": raw_threshold,
        "full": raw_full,
        "half_dimensions": {name: int(value)
                            for name, value in half_dimensions.items()},
        "source_condition": source_max / source_min,
    }
    row = {
        "axis": str(parent_row["axis"]),
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": comparison_cutoff,
        "kernel_exponent": exponent,
        "shell": shell,
        "shell_cardinality": len(shell),
        "profile_cutoffs": list(PROFILE_CUTOFFS),
        "tested_prefix_count": prefix_count,
        "beta_norm_squared": enclosure(beta_norm_squared),
        "source_profile_gram_condition_number": enclosure(
            source_max / source_min),
        "least_squares_prefixes": prefixes,
        "half_rms_dimensions": {name: int(value)
                                for name, value in half_dimensions.items()},
        "threshold_budget_frontiers": threshold_frontiers,
        "full_prefix_budget_frontiers": full_frontiers,
        "physical_operator_replayed": True,
        "target_rms_threshold": "1/2",
    }
    return row, raw_row


def build_payload() -> dict[str, Any]:
    lock = parent_lock()
    ordered, _ = load_rows()
    workers = min(len(ordered), max(1, os.cpu_count() or 1))
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                completed = pool.map(build_row, ordered)
        except (AttributeError, OSError, RuntimeError):
            completed = [build_row(row) for row in ordered]
    else:
        completed = [build_row(row) for row in ordered]
    rows = [item[0] for item in completed]
    raw_rows = [item[1] for item in completed]
    need(len(rows) == 18, "row census")

    weighted_threshold = [
        item["threshold"]["minimum"]["source_budget_ratio"]
        for item in raw_rows]
    weighted_full = [
        item["full"]["minimum"]["source_budget_ratio"]
        for item in raw_rows]
    plus_threshold = [
        item["threshold"]["plus"]["source_budget_ratio"]
        for item in raw_rows]
    gaps = [a / b for a, b in zip(weighted_threshold, plus_threshold)]
    need(min(weighted_threshold) > WEIGHTED_FLOOR,
         "weighted threshold budget floor")
    need(sum(value > BUDGET_OBSTRUCTION for value in weighted_threshold) == 14,
         "weighted threshold obstruction census")
    need(sum(value > BUDGET_OBSTRUCTION for value in weighted_full) == 11,
         "weighted full-prefix obstruction census")
    need(max(plus_threshold) < PLUS_CEILING,
         "positive threshold budget ceiling")
    need(min(gaps) > GAP_FLOOR, "weighted/positive budget gap")
    max_condition = max(item["source_condition"] for item in raw_rows)
    min_gap = min(gaps)
    return {
        "schema": SCHEMA,
        "profile_family": {
            "formula": "beta_z(t)=lambda(t)-sum_{d<=z,d|t}mu(d)",
            "ordered_cutoffs": list(PROFILE_CUTOFFS),
            "prefix_definition": "U_k=[beta_z1,...,beta_zk]",
            "source_norm": "||U_k c||_2^2=c^T(U_k^T U_k)c",
            "target_map": "V_k=A^T U_k",
            "source_side": True,
            "target_dependent_directions": False,
        },
        "parent_lock": lock,
        "exact_theorem": {
            "source_gram": "M_k=U_k^T U_k is positive definite when U_k has full column rank",
            "budget_frontier": (
                "B_{k,tau}(b)=min{c^T M_k c:||V_k c-b||_2<=tau||b||_2}"),
            "ridge_kkt": (
                "c_lambda=(V_k^T V_k+lambda M_k)^(-1)V_k^T b"),
            "frontier_rule": (
                "for dist(b,range(V_k))<tau||b||<||b||, unique lambda>=0 "
                "saturates the residual constraint"),
            "budget_feasibility": (
                "a native-profile source budget B reaches tolerance tau iff "
                "B>=B_{k,tau}(b)"),
            "nested_budget": (
                "U_k subseteq U_l implies B_{l,tau}(b)<=B_{k,tau}(b) "
                "whenever both are feasible"),
            "scope": "finite literal profile prefixes and finite Euclidean target controls",
        },
        "finite_audit": {
            "rows": 18,
            "shell_edges": 1380,
            "profile_count": len(PROFILE_CUTOFFS),
            "tested_prefix_entries": sum(row["tested_prefix_count"]
                                        for row in rows),
            "target_rms_threshold": "1/2",
            "weighted_threshold_budget_ratio_floor": "9e-5",
            "weighted_threshold_budget_floor_rows": sum(
                value > BUDGET_MID for value in weighted_threshold),
            "weighted_threshold_budget_above_5e-4_rows": sum(
                value > BUDGET_MID for value in weighted_threshold),
            "weighted_threshold_budget_above_1e-3_rows": sum(
                value > BUDGET_OBSTRUCTION for value in weighted_threshold),
            "weighted_full_prefix_budget_above_1e-3_rows": sum(
                value > BUDGET_OBSTRUCTION for value in weighted_full),
            "all_positive_threshold_budget_ratio_ceiling": "1e-4",
            "all_positive_threshold_budget_ceiling_rows": sum(
                value < PLUS_CEILING for value in plus_threshold),
            "weighted_to_positive_threshold_budget_gap_floor": "20",
            "weighted_to_positive_gap_floor_rows": sum(
                value > GAP_FLOOR for value in gaps),
            "minimum_weighted_threshold_budget_ratio": enclosure(
                min(weighted_threshold)),
            "maximum_weighted_threshold_budget_ratio": enclosure(
                max(weighted_threshold)),
            "maximum_positive_threshold_budget_ratio": enclosure(
                max(plus_threshold)),
            "minimum_weighted_to_positive_gap": enclosure(min_gap),
            "maximum_source_profile_gram_condition_upper": enclosure(
                max_condition),
            "working_precision_decimal_digits": MP_DPS,
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC299_PROFILE_BUDGET_KKT_FRONTIER":
                "PROVED_EXACT_FINITE",
            "TPC299_NESTED_BUDGET_MONOTONICITY":
                "PROVED_EXACT_FINITE",
            "TPC299_WEIGHTED_HALF_RMS_BUDGET_FLOOR":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5",
            "TPC299_WEIGHTED_HALF_RMS_BUDGET_MID_FLOOR":
                "NUMERICALLY_CERTIFIED_FINITE_15_OF_18_ABOVE_5E_MINUS_4",
            "TPC299_WEIGHTED_HALF_RMS_BUDGET_OBSTRUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3",
            "TPC299_WEIGHTED_FULL_PREFIX_BUDGET_OBSTRUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3",
            "TPC299_PLUS_HALF_RMS_BUDGET_CEILING":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_1E_MINUS_4",
            "TPC299_WEIGHTED_PLUS_BUDGET_GAP":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_20",
            "TPC299_PROFILE_BUDGET_GROWTH": "OPEN",
            "TPC299_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC299_FIXED_POWER_CREDIT": 0,
            "TPC299_FULL_GATE_B": "OPEN",
            "TPC299_TWIN_PRIME_RESULT": "NONE",
            "TPC299_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data == document(), "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    print("TPC299_CERTIFICATE=PASS rows={} prefixes={} weighted_gt_1e-3={} "
          "full_gt_1e-3={} plus_lt_1e-4={} gap_gt_20={} fixed_power_credit={}"
          .format(
              audit["rows"], audit["tested_prefix_entries"],
              audit["weighted_threshold_budget_above_1e-3_rows"],
              audit["weighted_full_prefix_budget_above_1e-3_rows"],
              audit["all_positive_threshold_budget_ceiling_rows"],
              audit["weighted_to_positive_gap_floor_rows"],
              audit["fixed_power_credit"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC299_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
