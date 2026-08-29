#!/usr/bin/env python3
"""TPC-298 literal source-profile angle and dimension ladder.

This certificate keeps the physical operator frozen and replaces the four
cutoff snapshot of TPC-297 by an ordered prefix ladder.  All profile and
physical entries are formed exactly over ``Fraction`` before the finite
linear-algebra audit is replayed at high precision.  The asymptotic arithmetic
problem is deliberately outside the certificate's claim ceiling.
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
    "papers/tpc-297-literal-source-profile-span-audit/code/"
    "tpc297_literal_source_profile_span_certificate.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-297-literal-source-profile-span-audit/results/"
    "tpc297_certificate.json")
LABEL_RESULT = ROOT / (
    "papers/tpc-295-source-correlation-image-audit/results/"
    "tpc295_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc298_certificate.json"

PARENT_CODE_SHA256 = (
    "ae60f5400e083875012cb817285916e1370064f1d55599878def5c59a89a6aa5")
PARENT_RESULT_SHA256 = (
    "2ffe4cfd0f564fb2cd63669dccbd8dc99f5911123b3b4a3f8b766262f88d97b6")
LABEL_RESULT_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

STATUS = (
    "PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER")
SCHEMA = "TPC298_PROFILE_ANGLE_DIMENSION_CERTIFICATE_V1"
ROUND2_CLUE = (
    "TEST_WEIGHTED_PROFILE_DIMENSION_AGAINST_LEAST_NORM_SOURCE_BUDGET_AND_"
    "CONDITIONING")
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
MODULI = (1000000007, 998244353)
MP_DPS = 70
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-18")
HALF_RMS = mp.mpf("0.5")
PLUS_HALF_DIMENSION_MAX = 6

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc297_for_tpc298", PARENT_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-297 parent unavailable")
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


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-297 code provenance")
    raw_parent = PARENT_RESULT.read_bytes()
    need(digest(raw_parent) == PARENT_RESULT_SHA256,
         "TPC-297 result provenance")
    parent = json.loads(raw_parent)
    need(raw_parent == canonical(parent), "TPC-297 canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY"),
         "TPC-297 status")
    raw_labels = LABEL_RESULT.read_bytes()
    need(digest(raw_labels) == LABEL_RESULT_SHA256,
         "TPC-295 result provenance")
    labels = json.loads(raw_labels)
    need(raw_labels == canonical(labels), "TPC-295 canonicality")
    need(labels.get("certificate_version") == 1 and
         labels.get("claim_status", "").startswith(
             "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION"),
         "TPC-295 status")
    need(len(parent["payload"]["rows"]) == 18 and
         len(labels["payload"]["rows"]) == 18, "parent census")
    return {
        "tpc297_code_sha256": PARENT_CODE_SHA256,
        "tpc297_result_sha256": PARENT_RESULT_SHA256,
        "tpc295_label_result_sha256": LABEL_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
    }


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def load_rows() -> tuple[list[dict[str, Any]], dict[tuple[int, int, int, int, int],
                                                      dict[str, Any]]]:
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


def mod_fraction(value: Fraction, modulus: int) -> int:
    denominator = value.denominator % modulus
    need(denominator != 0, "profile denominator is noninvertible")
    return (value.numerator % modulus) * pow(denominator, modulus - 2,
                                             modulus) % modulus


def modular_rank(matrix: list[list[Fraction]], modulus: int) -> int:
    if not matrix or not matrix[0]:
        return 0
    a = [[mod_fraction(value, modulus) for value in row] for row in matrix]
    rows, columns = len(a), len(a[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((r for r in range(pivot_row, rows)
                      if a[r][column] != 0), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        inverse = pow(a[pivot_row][column], modulus - 2, modulus)
        a[pivot_row] = [(value * inverse) % modulus
                        for value in a[pivot_row]]
        for row in range(rows):
            if row == pivot_row or a[row][column] == 0:
                continue
            factor = a[row][column]
            a[row] = [(left - factor * right) % modulus
                      for left, right in zip(a[row], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def matrix_from_columns(columns: list[list[Fraction]]) -> mp.matrix:
    return mp.matrix([[as_mp(columns[j][i]) for j in range(len(columns))]
                      for i in range(len(columns[0]))])


def profile_matrix(indices: list[int]) -> list[list[Fraction]]:
    return [[literal_beta(value, cutoff) for cutoff in PROFILE_CUTOFFS]
            for value in indices]


def finite_prefix_metrics(V: mp.matrix, labels: dict[str, list[int]],
                          k: int) -> dict[str, Any]:
    shell_size = len(labels["plus"])
    W = mp.matrix([[V[i, j] for j in range(k)]
                   for i in range(shell_size)])
    singular = mp.svd(W, compute_uv=False)
    condition = singular[0] / singular[k - 1]
    targets: dict[str, dict[str, Any]] = {}
    raw: dict[str, mp.mpf] = {}
    for name, label in labels.items():
        b = mp.matrix(label)
        coefficients = mp.qr_solve(W, b)[0]
        residual = W * coefficients - b
        rms = mp.sqrt(mp.fsum(residual[i] ** 2
                              for i in range(shell_size)) / shell_size)
        captured = 1 - rms ** 2
        angle = mp.asin(max(mp.mpf(0), min(mp.mpf(1), rms)))
        coefficient_norm = mp.fsum(coefficients[i] ** 2
                                   for i in range(k))
        targets[name] = {
            "rms_residual": enclosure(rms),
            "captured_fraction": enclosure(captured),
            "principal_angle_sine": enclosure(rms),
            "principal_angle_radians": enclosure(angle),
            "coefficient_l2_squared": enclosure(coefficient_norm),
            "rank_used": k,
        }
        raw[name] = rms
    return {
        "k": k,
        "cutoff": PROFILE_CUTOFFS[k - 1],
        "rank": k,
        "singular_value_max": enclosure(singular[0]),
        "singular_value_min_nonzero": enclosure(singular[k - 1]),
        "condition_number": enclosure(condition),
        "targets": targets,
        "raw": raw,
    }


def build_row(parent_row: dict[str, Any]) -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    scale = int(parent_row["scale"])
    height = int(parent_row["H"])
    q0 = int(parent_row["Q"])
    comparison_cutoff = int(parent_row["comparison_cutoff_z"])
    exponent = int(parent_row["kernel_exponent"])
    indices, frozen_beta, _ = ENGINE.source_weights(scale, comparison_cutoff)
    shell = shell_between(q0)
    columns = [PARENT.PARENT.physical_output(
        indices, frozen_beta, height, prime, exponent) for prime in shell]
    A = matrix_from_columns(columns)
    U_exact = profile_matrix(indices)
    V_exact = [[sum(columns[j][i] * U_exact[i][k]
                    for i in range(len(indices)))
                for k in range(len(PROFILE_CUTOFFS))]
               for j in range(len(shell))]
    rank_ladder: list[dict[str, Any]] = []
    for k in range(1, len(PROFILE_CUTOFFS) + 1):
        ranks = [modular_rank([row[:k] for row in V_exact], modulus)
                 for modulus in MODULI]
        expected = min(k, len(shell))
        need(ranks == [expected, expected], "prefix rank ladder")
        rank_ladder.append({
            "k": k,
            "cutoff": PROFILE_CUTOFFS[k - 1],
            "expected_rank": expected,
            "ranks": [{"modulus": modulus, "rank": rank}
                      for modulus, rank in zip(MODULI, ranks)],
        })
    U = mp.matrix([[as_mp(U_exact[i][k])
                    for k in range(len(PROFILE_CUTOFFS))]
                   for i in range(len(indices))])
    V = A.T * U
    labels = {
        "minimum": [int(value) for value in parent_row["minimum_signed_label"]],
        "maxcut": [int(value) for value in parent_row["maxcut_label"]],
        "plus": [1] * len(shell),
    }
    prefix_count = min(len(shell), len(PROFILE_CUTOFFS))
    prefixes: list[dict[str, Any]] = []
    for k in range(1, prefix_count + 1):
        metrics = finite_prefix_metrics(V, labels, k)
        raw = metrics.pop("raw")
        need(all(0 <= raw[name] <= 1 + mp.mpf("1e-45")
                 for name in labels), "residual range")
        prefixes.append(metrics)
    half_dimensions = {
        name: next((entry["k"] for entry in prefixes
                    if mp.mpf(entry["targets"][name]["rms_residual"][1]) <=
                    HALF_RMS), None)
        for name in labels
    }
    need(all(value is not None for value in half_dimensions.values()),
         "half-RMS prefix exists")
    weighted_half = int(half_dimensions["minimum"])
    plus_half = int(half_dimensions["plus"])
    need(3 * weighted_half >= 2 * len(shell), "weighted dimension floor")
    need(plus_half <= PLUS_HALF_DIMENSION_MAX, "positive dimension ceiling")
    final = prefixes[-1]
    need(all(mp.mpf(final["targets"][name]["rms_residual"][1]) <=
             mp.mpf("1e-15") for name in labels), "full finite capture")
    reference = prefixes[min(3, len(prefixes) - 1)]
    return {
        "axis": str(parent_row["axis"]),
        "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": comparison_cutoff,
        "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "profile_cutoffs": list(PROFILE_CUTOFFS),
        "tested_prefix_count": prefix_count,
        "profile_rank_ladder_modular": rank_ladder,
        "prefixes": prefixes,
        "half_rms_dimensions": half_dimensions,
        "half_rms_dimension_ratios": {
            name: [str(Fraction(int(value), len(shell))),
                   mp.nstr(mp.mpf(int(value)) / len(shell), 24)]
            for name, value in half_dimensions.items()
        },
        "reference_prefix_k": reference["k"],
        "physical_operator_replayed": True,
        "full_prefix_captures_finite_target": True,
    }


def build_payload() -> dict[str, Any]:
    lock = parent_lock()
    ordered, _ = load_rows()
    workers = min(len(ordered), max(1, os.cpu_count() or 1))
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(build_row, ordered)
        except (AttributeError, OSError, RuntimeError):
            rows = [build_row(row) for row in ordered]
    else:
        rows = [build_row(row) for row in ordered]
    need(len(rows) == 18, "row census")
    weighted_ratios = [
        Fraction(int(row["half_rms_dimensions"]["minimum"]),
                  row["shell_cardinality"]) for row in rows]
    plus_dimensions = [int(row["half_rms_dimensions"]["plus"]) for row in rows]
    need(min(weighted_ratios) >= Fraction(2, 3), "weighted ratio census")
    need(max(plus_dimensions) <= PLUS_HALF_DIMENSION_MAX,
         "positive dimension census")
    need(all(row["full_prefix_captures_finite_target"] for row in rows),
         "full capture census")
    all_prefixes = [prefix for row in rows for prefix in row["prefixes"]]
    max_condition = max(mp.mpf(prefix["condition_number"][1])
                        for prefix in all_prefixes)
    return {
        "schema": SCHEMA,
        "profile_family": {
            "formula": "beta_z(t)=lambda(t)-sum_{d<=z,d|t} mu(d)",
            "ordered_cutoffs": list(PROFILE_CUTOFFS),
            "prefix_definition": "U_k=[beta_z1,...,beta_zk]",
            "source_side": True,
            "target_dependent_directions": False,
        },
        "parent_lock": lock,
        "exact_theorem": {
            "image": "V_k=A^T U_k",
            "projection": "min_c ||V_k c-b||^2=b^T(I-P_k)b",
            "principal_angle": "r_k=sin(theta_k), cos^2(theta_k)=1-r_k^2",
            "nested_prefix": "range(V_k) subseteq range(V_{k+1})",
            "threshold_dimension": "k_tau(b)=min{k:r_k<=tau}",
            "finite_full_capture": "rank(V_m)=m implies P_m=I on the shell",
            "scope": "finite declared literal cutoff prefixes",
        },
        "finite_audit": {
            "rows": 18,
            "shell_edges": 1380,
            "profile_count": len(PROFILE_CUTOFFS),
            "prefix_rank_rows_both_moduli": sum(
                all(item["ranks"][0]["rank"] == item["expected_rank"] and
                    item["ranks"][1]["rank"] == item["expected_rank"]
                    for item in row["profile_rank_ladder_modular"])
                for row in rows),
            "rank_prefix_entries": sum(
                len(row["profile_rank_ladder_modular"]) for row in rows),
            "weighted_half_rms_ratio_floor": "2/3",
            "weighted_half_rms_ratio_rows": sum(
                Fraction(int(row["half_rms_dimensions"]["minimum"]),
                         row["shell_cardinality"]) >= Fraction(2, 3)
                for row in rows),
            "all_positive_half_rms_dimension_max": PLUS_HALF_DIMENSION_MAX,
            "all_positive_half_rms_dimension_rows": sum(
                int(row["half_rms_dimensions"]["plus"]) <=
                PLUS_HALF_DIMENSION_MAX for row in rows),
            "full_prefix_capture_rows": sum(
                row["full_prefix_captures_finite_target"] for row in rows),
            "maximum_prefix_condition_upper": enclosure(max_condition),
            "working_precision_decimal_digits": MP_DPS,
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC298_PROJECTION_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC298_PRINCIPAL_ANGLE_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC298_NESTED_PREFIX_MONOTONICITY": "PROVED_EXACT_FINITE",
            "TPC298_TWO_MODULUS_PREFIX_RANK":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
            "TPC298_WEIGHTED_HALF_RMS_DIMENSION":
                "NUMERICAL_OBSERVATION_18_OF_18_RATIO_AT_LEAST_2_OVER_3",
            "TPC298_PLUS_HALF_RMS_DIMENSION":
                "NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_6",
            "TPC298_FULL_PREFIX_CAPTURE":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
            "TPC298_GROWING_DIMENSION_THEOREM": "OPEN",
            "TPC298_CONDITIONING_GROWTH": "OPEN",
            "TPC298_SOURCE_BUDGET_GROWTH": "OPEN",
            "TPC298_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC298_FIXED_POWER_CREDIT": 0,
            "TPC298_FULL_GATE_B": "OPEN",
            "TPC298_TWIN_PRIME_RESULT": "NONE",
            "TPC298_STATUS": STATUS,
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
    print("TPC298_CERTIFICATE=PASS rows={} prefixes={} weighted_ratio={} "
          "plus_dim_max={} full_capture={} fixed_power_credit={}".format(
              audit["rows"], audit["rank_prefix_entries"],
              audit["weighted_half_rms_ratio_floor"],
              audit["all_positive_half_rms_dimension_max"],
              audit["full_prefix_capture_rows"],
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
        print("TPC298_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
