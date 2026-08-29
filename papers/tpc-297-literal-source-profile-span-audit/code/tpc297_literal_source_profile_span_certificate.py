#!/usr/bin/env python3
"""TPC-297 literal cutoff-profile span certificate.

The source directions are the actual finite Mobius/Euler cutoff profiles
beta_z, z in {3,5,7,11}.  The physical columns are frozen from TPC-295.
The exact theorem is the restricted least-squares projection identity; the
atlas is deliberately finite and receives no asymptotic or arithmetic credit.
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
    "papers/tpc-295-source-correlation-image-audit/code/"
    "tpc295_source_correlation_image_certificate.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-295-source-correlation-image-audit/results/"
    "tpc295_certificate.json")
TPC296_RESULT = ROOT / (
    "papers/tpc-296-source-norm-budget-interface/results/"
    "tpc296_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc297_certificate.json"

PARENT_CODE_SHA256 = (
    "3cdb1ea78f0fd04fd70d268997ffb1ee6842c2b523dd0c69a28adff6fab8c6c4")
PARENT_RESULT_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")
TPC296_RESULT_SHA256 = (
    "469076735f28d1bf55dd7cdc882fe312b74f821f089d9ed352f47c5b26ffe88c")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS")
SCHEMA = "TPC297_LITERAL_SOURCE_PROFILE_SPAN_CERTIFICATE_V1"
ROUND2_CLUE = "TEST_NATIVE_PROFILE_PRINCIPAL_ANGLES_AND_MINIMUM_DIMENSION"
PROFILE_CUTOFFS = (3, 5, 7, 11)
MODULI = (1000000007, 998244353)
MP_DPS = 70
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-18")
WEIGHTED_FLOOR = mp.mpf("0.6")
PLUS_CEILING = mp.mpf("0.15")

spec = importlib.util.spec_from_file_location("frozen_tpc295_for_tpc297",
                                              PARENT_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-295 parent unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)
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
         "TPC-295 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-295 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC-295 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION"),
         "TPC-295 status")
    raw296 = TPC296_RESULT.read_bytes()
    need(digest(raw296) == TPC296_RESULT_SHA256, "TPC-296 result provenance")
    data296 = json.loads(raw296)
    need(raw296 == canonical(data296), "TPC-296 canonicality")
    need(data296.get("certificate_version") == 1 and
         data296.get("claim_status", "").startswith(
             "PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET"), "TPC-296 status")
    need(len(data["payload"]["rows"]) == 18 and
         len(data296["payload"]["rows"]) == 18, "parent census")
    return {
        "tpc295_code_sha256": PARENT_CODE_SHA256,
        "tpc295_result_sha256": PARENT_RESULT_SHA256,
        "tpc296_result_sha256": TPC296_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
    }


def load_rows() -> dict[tuple[int, int, int, int, int], dict[str, Any]]:
    data = json.loads(PARENT_RESULT.read_bytes())
    result: dict[tuple[int, int, int, int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))
        need(key not in result, "duplicate parent row")
        result[key] = row
    need(len(result) == 18, "parent row map")
    return result


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


def target_residuals(V: mp.matrix, labels: dict[str, list[int]],
                     rank: int) -> tuple[dict[str, dict[str, Any]],
                                            dict[str, mp.mpf]]:
    # The first rank cutoff profiles are independently ranked on every row.
    W = V[:, :rank]
    targets: dict[str, dict[str, Any]] = {}
    raw: dict[str, mp.mpf] = {}
    for name, label in labels.items():
        b = mp.matrix(label)
        coefficients = mp.qr_solve(W, b)[0]
        residual = W * coefficients - b
        rms = mp.sqrt(mp.fsum(residual[i] ** 2 for i in range(len(label))) /
                      len(label))
        capture = 1 - rms ** 2
        source_coeff_norm = mp.fsum(coefficients[i] ** 2 for i in range(rank))
        targets[name] = {
            "rms_residual": enclosure(rms),
            "captured_fraction": enclosure(capture),
            "coefficient_l2_squared": enclosure(source_coeff_norm),
            "rank_used": rank,
        }
        raw[name] = rms
    return targets, raw


def build_row(parent_row: dict[str, Any]) -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    scale = int(parent_row["scale"])
    height = int(parent_row["H"])
    q0 = int(parent_row["Q"])
    cutoff = int(parent_row["comparison_cutoff_z"])
    exponent = int(parent_row["kernel_exponent"])
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = shell_between(q0)
    columns = [PARENT.physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    A = matrix_from_columns(columns)
    U_exact = profile_matrix(indices)
    V_exact = [[sum(columns[j][i] * U_exact[i][k]
                    for i in range(len(indices)))
                for k in range(len(PROFILE_CUTOFFS))]
               for j in range(len(shell))]
    ranks = [modular_rank(V_exact, modulus) for modulus in MODULI]
    need(ranks[0] == ranks[1], "modular profile rank disagreement")
    expected_rank = min(len(shell), len(PROFILE_CUTOFFS))
    need(ranks[0] == expected_rank, "unexpected finite profile rank")
    rank = ranks[0]
    U = mp.matrix([[as_mp(U_exact[i][k])
                    for k in range(len(PROFILE_CUTOFFS))]
                   for i in range(len(indices))])
    V = A.T * U
    singular = mp.svd(V, compute_uv=False)
    labels = {
        "minimum": [int(value) for value in parent_row["minimum_signed_label"]],
        "maxcut": [int(value) for value in parent_row["maxcut_label"]],
        "plus": [1] * len(shell),
    }
    targets, raw = target_residuals(V, labels, rank)
    need(raw["minimum"] >= WEIGHTED_FLOOR if len(shell) >= 5 else
         raw["minimum"] >= 0, "weighted threshold")
    need(raw["plus"] <= PLUS_CEILING, "positive threshold")
    base_beta = mp.matrix([as_mp(value) for value in beta])
    native = A.T * base_beta
    base_norm = (native.T * native)[0]
    one_ray: dict[str, mp.mpf] = {}
    for name, label in labels.items():
        b = mp.matrix(label)
        alpha = (native.T * b)[0] / base_norm
        one_ray[name] = mp.sqrt(mp.fsum((alpha * native[i] - b[i]) ** 2
                                         for i in range(len(shell))) /
                                len(shell))
        need(raw[name] <= one_ray[name] + mp.mpf("1e-45"),
             "nested profile did not improve")
    return {
        "axis": str(parent_row["axis"]),
        "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "profile_cutoffs": list(PROFILE_CUTOFFS),
        "profile_rank_modular": [
            {"modulus": modulus, "rank": rank_value}
            for modulus, rank_value in zip(MODULI, ranks)],
        "profile_rank": rank,
        "profile_singular_value_max": enclosure(singular[0]),
        "profile_singular_value_min": enclosure(singular[rank - 1]),
        "profile_condition_number": enclosure(singular[0] / singular[rank - 1]),
        "targets": targets,
        "one_ray_rms": {name: enclosure(value)
                        for name, value in one_ray.items()},
        "profile_contains_frozen_beta": True,
        "physical_operator_replayed": True,
    }


def build_payload() -> dict[str, Any]:
    lock = parent_lock()
    parent_rows = load_rows()
    ordered: list[dict[str, Any]] = []
    parent_data = json.loads(PARENT_RESULT.read_bytes())
    for parent_row in parent_data["payload"]["rows"]:
        key = (int(parent_row["scale"]), int(parent_row["H"]),
               int(parent_row["Q"]), int(parent_row["comparison_cutoff_z"]),
               int(parent_row["kernel_exponent"]))
        need(key in parent_rows, "parent row missing")
        ordered.append(parent_rows[key])
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
    large = [row for row in rows if row["shell_cardinality"] >= 5]
    weighted_values = [mp.mpf(row["targets"]["minimum"]["rms_residual"][0])
                       for row in large]
    plus_values = [mp.mpf(row["targets"]["plus"]["rms_residual"][1])
                   for row in rows]
    no_worse = all(
        mp.mpf(row["targets"][name]["rms_residual"][1]) <=
        mp.mpf(row["one_ray_rms"][name][0]) + mp.mpf("1e-15")
        for row in rows for name in ("minimum", "maxcut", "plus"))
    need(no_worse, "nested residual census")
    need(len(weighted_values) == 17 and min(weighted_values) >= WEIGHTED_FLOOR,
         "weighted census")
    need(len(plus_values) == 18 and max(plus_values) <= PLUS_CEILING,
         "positive census")
    return {
        "schema": SCHEMA,
        "profile_family": {
            "formula": "beta_z(t)=lambda(t)-sum_{d<=z,d|t} mu(d)",
            "cutoffs": list(PROFILE_CUTOFFS),
            "source_side": True,
            "target_dependent_directions": False,
        },
        "parent_lock": lock,
        "exact_theorem": {
            "restricted_map": "c -> A^T U c",
            "projection": "min_c ||A^T U c-b||^2=b^T(I-P_V)b",
            "image": "V=A^T U",
            "full_column_rank_projection": "P_V=V(V^T V)^(-1)V^T",
            "nested_span": "adding columns to U cannot increase the residual",
            "scope": "finite declared four-cutoff source family",
        },
        "finite_audit": {
            "rows": 18,
            "shell_edges": 1380,
            "profile_count": len(PROFILE_CUTOFFS),
            "rank_3_rows": sum(row["profile_rank"] == 3 for row in rows),
            "rank_4_rows": sum(row["profile_rank"] == 4 for row in rows),
            "rank_agreement_rows_both_moduli": sum(
                row["profile_rank_modular"][0]["rank"] ==
                row["profile_rank_modular"][1]["rank"] for row in rows),
            "large_shell_rows": len(large),
            "weighted_rms_at_least_0_6_rows_large_shell": sum(
                mp.mpf(row["targets"]["minimum"]["rms_residual"][0]) >=
                WEIGHTED_FLOOR for row in large),
            "all_positive_rms_at_most_0_15_rows": sum(
                mp.mpf(row["targets"]["plus"]["rms_residual"][1]) <=
                PLUS_CEILING for row in rows),
            "profile_no_worse_than_one_ray_rows": sum(
                all(mp.mpf(row["targets"][name]["rms_residual"][1]) <=
                    mp.mpf(row["one_ray_rms"][name][0]) + mp.mpf("1e-15")
                    for name in ("minimum", "maxcut", "plus"))
                for row in rows),
            "working_precision_decimal_digits": MP_DPS,
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC297_PROJECTION_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC297_NESTED_PROFILE_MONOTONICITY": "PROVED_EXACT_FINITE",
            "TPC297_TWO_MODULUS_IMAGE_RANK":
                "NUMERICALLY_CERTIFIED_FINITE_3_PLUS_4",
            "TPC297_WEIGHTED_PROFILE_SEPARATION":
                "NUMERICAL_OBSERVATION_17_OF_17_AT_LEAST_0_6",
            "TPC297_ALL_POSITIVE_PROFILE_CAPTURE":
                "NUMERICAL_OBSERVATION_18_OF_18_AT_MOST_0_15",
            "TPC297_PROFILE_FAMILY": "MODELING_CHOICE_LITERAL_CUTOFFS_3_5_7_11",
            "TPC297_GROWING_PROFILE_DIMENSION": "OPEN",
            "TPC297_PRINCIPAL_ANGLE_THEOREM": "OPEN",
            "TPC297_SOURCE_BUDGET_GROWTH": "OPEN",
            "TPC297_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC297_FIXED_POWER_CREDIT": 0,
            "TPC297_FULL_GATE_B": "OPEN",
            "TPC297_TWIN_PRIME_RESULT": "NONE",
            "TPC297_STATUS": STATUS,
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
    print("TPC297_CERTIFICATE=PASS rows={} rank3={} rank4={} weighted_large={} "
          "plus={} no_worse={} fixed_power_credit={}".format(
              audit["rows"], audit["rank_3_rows"], audit["rank_4_rows"],
              audit["weighted_rms_at_least_0_6_rows_large_shell"],
              audit["all_positive_rms_at_most_0_15_rows"],
              audit["profile_no_worse_than_one_ray_rows"],
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
        print("TPC297_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
