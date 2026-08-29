#!/usr/bin/env python3
"""TPC-300 exact dual lower-bound certificates for native profile budgets.

TPC-299 solved a finite primal source-budget frontier.  This release derives
the strong Lagrange dual, corrects the reciprocal convention between the KKT
multiplier and the ridge parameter, and compiles rational ridge parameters
into independently checkable exact lower bounds.
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
    "papers/tpc-299-native-profile-budget-frontier/code/"
    "tpc299_native_profile_budget_frontier_certificate.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-299-native-profile-budget-frontier/results/"
    "tpc299_certificate.json")
RESULT = PROJECT / "results/tpc300_certificate.json"

PARENT_CODE_SHA256 = (
    "94cb7f191378698de2f08157a475586864c59bba02621e447da98f5ffbbc7279")
PARENT_RESULT_SHA256 = (
    "9be51f5bcb93e3a297a70e1c12985d52aee2b74e5e3fe4a64fbf7d5a054c559e")

STATUS = (
    "PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY_AND_RECIPROCAL_"
    "MULTIPLIER_CORRECTION_PLUS_NUMERICALLY_CERTIFIED_FINITE_"
    "RATIONAL_DUAL_WITNESS_ATLAS")
SCHEMA = "TPC300_NATIVE_BUDGET_DUAL_CERTIFICATE_V1"
ROUND2_CLUE = (
    "HOSTILE_TEST_THE_DUAL_BUDGET_GAP_ACROSS_TOLERANCE_AND_"
    "SOURCE_NORMALIZATION_LADDERS")
MP_DPS = 90
RHO_SIGNIFICANT_DIGITS = 20
TIGHTNESS_FLOOR = mp.mpf("0.999999999")
WEIGHTED_FLOOR = Fraction(9, 100000)
WEIGHTED_MID = Fraction(5, 10000)
WEIGHTED_OBSTRUCTION = Fraction(1, 1000)
TARGET_RMS_SQUARED = Fraction(1, 4)

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc299_for_tpc300", PARENT_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-299 parent unavailable")
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


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")).hexdigest()


def vector_digest(values: list[Fraction]) -> str:
    raw = "".join(
        f"{value.numerator}/{value.denominator}\n" for value in values)
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def as_mp(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def enclosure(value: Fraction) -> list[str]:
    center = as_mp(value)
    radius = mp.mpf("1e-30") * max(mp.mpf(1), abs(center))
    return [mp.nstr(center - radius, 36), mp.nstr(center + radius, 36)]


def exact_solve(matrix: list[list[Fraction]],
                rhs: list[Fraction]) -> list[Fraction]:
    """Gauss-Jordan solve over Q; matrices here are positive definite."""
    n = len(rhs)
    need(len(matrix) == n and all(len(row) == n for row in matrix),
         "square exact system")
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if augmented[row][column] != 0), None)
        need(pivot is not None, "singular rational dual system")
        augmented[column], augmented[pivot] = (
            augmented[pivot], augmented[column])
        scale = augmented[column][column]
        augmented[column] = [value / scale
                             for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    augmented[row][entry] -
                    factor * augmented[column][entry]
                    for entry in range(n + 1)]
    return [augmented[row][-1] for row in range(n)]


def parent_lock() -> tuple[dict[str, Any], list[dict[str, Any]],
                           list[dict[str, Any]]]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-299 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256,
         "TPC-299 result provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC-299 canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER"),
         "TPC-299 status")
    payload = document.get("payload", {})
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380 and
         audit.get("profile_count") == 17, "TPC-299 finite census")
    source_rows, _ = PARENT.load_rows()
    certificate_rows = payload.get("rows", [])
    need(len(source_rows) == 18 and len(certificate_rows) == 18,
         "TPC-299 row census")
    certificate_map = {row_key(row): row for row in certificate_rows}
    need(len(certificate_map) == 18, "TPC-299 certificate row map")
    aligned = [certificate_map[row_key(row)] for row in source_rows]
    return document, source_rows, aligned


def exact_matrices(source_row: dict[str, Any]) -> tuple[
        list[int], list[Fraction], list[list[Fraction]],
        list[list[Fraction]]]:
    scale = int(source_row["scale"])
    height = int(source_row["H"])
    q0 = int(source_row["Q"])
    comparison_cutoff = int(source_row["comparison_cutoff_z"])
    exponent = int(source_row["kernel_exponent"])
    indices, beta, _ = ENGINE.source_weights(scale, comparison_cutoff)
    shell = PARENT.shell_between(q0)
    columns = [PARENT.PARENT.PARENT.PARENT.physical_output(
        indices, beta, height, prime, exponent) for prime in shell]
    profiles = PARENT.source_profile_matrix(indices)
    profile_count = len(PARENT.PROFILE_CUTOFFS)
    image = [[sum((columns[row][index] * profiles[index][column]
                   for index in range(len(indices))), Fraction(0))
              for column in range(profile_count)]
             for row in range(len(shell))]
    gram = [[sum((profiles[index][left] * profiles[index][right]
                  for index in range(len(indices))), Fraction(0))
             for right in range(profile_count)]
            for left in range(profile_count)]
    return shell, beta, image, gram


def rational_rho(interval: list[str]) -> Fraction:
    need(isinstance(interval, list) and len(interval) == 2,
         "parent ridge interval")
    midpoint = (mp.mpf(interval[0]) + mp.mpf(interval[1])) / 2
    text = mp.nstr(midpoint, RHO_SIGNIFICANT_DIGITS)
    value = Fraction(text)
    need(value > 0, "positive ridge parameter")
    return value


def build_case(image: list[list[Fraction]],
               gram: list[list[Fraction]], beta_norm_squared: Fraction,
               target: list[Fraction], frontier: dict[str, Any],
               context: str, target_name: str) -> tuple[dict[str, Any],
                                                         dict[str, Any]]:
    k = int(frontier["k"])
    rho = rational_rho(frontier["lagrange_multiplier"])
    rows = len(image)
    V = [row[:k] for row in image]
    M = [row[:k] for row in gram[:k]]
    normal = [[sum((V[row][left] * V[row][right]
                    for row in range(rows)), Fraction(0)) +
               rho * M[left][right]
               for right in range(k)] for left in range(k)]
    rhs = [sum((V[row][column] * target[row]
                for row in range(rows)), Fraction(0))
           for column in range(k)]
    coefficients = exact_solve(normal, rhs)
    image_value = [sum((V[row][column] * coefficients[column]
                        for column in range(k)), Fraction(0))
                   for row in range(rows)]
    btv_c = sum((target[row] * image_value[row]
                 for row in range(rows)), Fraction(0))
    target_norm_squared = sum((value * value for value in target),
                              Fraction(0))
    radius_squared = TARGET_RMS_SQUARED * rows
    dual = (target_norm_squared - radius_squared - btv_c) / rho
    need(dual > 0, "positive rational dual witness")
    budget_ratio = dual / beta_norm_squared
    parent_interval = frontier["source_norm_squared"]
    parent_upper = mp.mpf(parent_interval[1])
    tightness_lower = as_mp(dual) / parent_upper
    need(tightness_lower > TIGHTNESS_FLOOR and
         tightness_lower <= 1 + mp.mpf("1e-14"),
         "rational dual witness tightness")
    residual_squared = sum(((image_value[row] - target[row]) ** 2
                            for row in range(rows)), Fraction(0))
    kkt_multiplier = Fraction(rho.denominator, rho.numerator)
    saved = {
        "context": context,
        "target": target_name,
        "k": k,
        "cutoff": int(frontier["cutoff"]),
        "ridge_parameter_rho": {
            "numerator": str(rho.numerator),
            "denominator": str(rho.denominator),
        },
        "kkt_multiplier_mu_equals_one_over_rho": {
            "numerator": str(kkt_multiplier.numerator),
            "denominator": str(kkt_multiplier.denominator),
        },
        "dual_lower_bound_source_norm_squared": enclosure(dual),
        "dual_budget_ratio": enclosure(budget_ratio),
        "dual_to_parent_primal_ratio_lower": mp.nstr(tightness_lower, 24),
        "parent_primal_source_norm_squared": parent_interval,
        "selected_residual_squared": enclosure(residual_squared),
        "exact_dual_fraction_sha256": fraction_digest(dual),
        "exact_coefficient_vector_sha256": vector_digest(coefficients),
    }
    raw = {
        "context": context,
        "target": target_name,
        "dual": dual,
        "budget_ratio": budget_ratio,
        "tightness_lower": tightness_lower,
    }
    return saved, raw


def build_row(arguments: tuple[dict[str, Any], dict[str, Any]]) -> tuple[
        dict[str, Any], list[dict[str, Any]]]:
    mp.mp.dps = MP_DPS
    source_row, certificate_row = arguments
    shell, beta, image, gram = exact_matrices(source_row)
    beta_norm_squared = sum((value * value for value in beta), Fraction(0))
    labels = {
        "minimum": [Fraction(int(value))
                    for value in source_row["minimum_signed_label"]],
        "maxcut": [Fraction(int(value))
                   for value in source_row["maxcut_label"]],
        "plus": [Fraction(1) for _ in shell],
    }
    cases: list[dict[str, Any]] = []
    raw_cases: list[dict[str, Any]] = []
    for target_name in ("minimum", "maxcut", "plus"):
        saved, raw = build_case(
            image, gram, beta_norm_squared, labels[target_name],
            certificate_row["threshold_budget_frontiers"][target_name],
            "threshold", target_name)
        cases.append(saved)
        raw_cases.append(raw)
    saved, raw = build_case(
        image, gram, beta_norm_squared, labels["minimum"],
        certificate_row["full_prefix_budget_frontiers"]["minimum"],
        "full_prefix", "minimum")
    cases.append(saved)
    raw_cases.append(raw)
    row = {
        "axis": str(source_row["axis"]),
        "scale": int(source_row["scale"]),
        "H": int(source_row["H"]),
        "Q": int(source_row["Q"]),
        "comparison_cutoff_z": int(source_row["comparison_cutoff_z"]),
        "kernel_exponent": int(source_row["kernel_exponent"]),
        "shell": shell,
        "shell_cardinality": len(shell),
        "beta_norm_squared": enclosure(beta_norm_squared),
        "dual_cases": cases,
        "exact_physical_operator_replayed": True,
    }
    return row, raw_cases


def build_payload() -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    _, source_rows, certificate_rows = parent_lock()
    arguments = list(zip(source_rows, certificate_rows))
    workers = min(len(arguments), max(1, os.cpu_count() or 1))
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                completed = pool.map(build_row, arguments)
        except (AttributeError, OSError, RuntimeError):
            completed = [build_row(argument) for argument in arguments]
    else:
        completed = [build_row(argument) for argument in arguments]
    rows = [item[0] for item in completed]
    raw_cases = [case for item in completed for case in item[1]]
    need(len(rows) == 18 and len(raw_cases) == 72,
         "dual witness census")
    tightness = [case["tightness_lower"] for case in raw_cases]
    weighted_threshold = [case["budget_ratio"] for case in raw_cases
                          if case["context"] == "threshold" and
                          case["target"] == "minimum"]
    weighted_full = [case["budget_ratio"] for case in raw_cases
                     if case["context"] == "full_prefix" and
                     case["target"] == "minimum"]
    need(len(weighted_threshold) == 18 and len(weighted_full) == 18,
         "weighted dual census")
    need(sum(value > WEIGHTED_FLOOR
             for value in weighted_threshold) == 18,
         "weighted dual floor")
    need(sum(value > WEIGHTED_MID
             for value in weighted_threshold) == 15,
         "weighted dual mid census")
    need(sum(value > WEIGHTED_OBSTRUCTION
             for value in weighted_threshold) == 14,
         "weighted threshold dual obstruction")
    need(sum(value > WEIGHTED_OBSTRUCTION
             for value in weighted_full) == 11,
         "weighted full dual obstruction")
    need(min(tightness) > TIGHTNESS_FLOOR,
         "global dual tightness")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc299_code_sha256": PARENT_CODE_SHA256,
            "tpc299_result_sha256": PARENT_RESULT_SHA256,
        },
        "parameter_correction": {
            "parent_field": "lagrange_multiplier",
            "correct_interpretation": "ridge_parameter_rho",
            "kkt_multiplier": "mu=1/rho",
            "parent_budget_values_affected": False,
            "scope": "notation and KKT/ridge reciprocity only",
        },
        "exact_theorem": {
            "primal": "B_R(b)=min{c^T M c:||Vc-b||_2<=R}",
            "dual_lower_bound": (
                "D_rho=(||b||_2^2-R^2-b^T Vc_rho)/rho<=B_R(b)"),
            "ridge_system": (
                "(V^T V+rho M)c_rho=V^T b, rho>0"),
            "multiplier_reciprocity": "mu=1/rho",
            "strong_duality": (
                "if dist(b,range(V))<R<||b||, max_{rho>0}D_rho=B_R(b)"),
            "equality_rule": (
                "equality holds when ||Vc_rho-b||_2=R"),
            "scope": "finite positive-definite source Gram and Euclidean target ball",
        },
        "rational_witness_protocol": {
            "rho_selection": (
                "20-significant-digit rational midpoint of the frozen TPC-299 ridge interval"),
            "linear_algebra": "exact Fraction Gauss-Jordan over Q",
            "dual_fraction": "exact rational before decimal enclosure",
            "contexts": ["threshold:minimum,maxcut,plus",
                         "full_prefix:minimum"],
        },
        "finite_audit": {
            "rows": 18,
            "shell_edges": 1380,
            "dual_witness_cases": 72,
            "exact_rational_dual_cases": 72,
            "dual_tightness_floor": "0.999999999",
            "dual_tightness_floor_cases": sum(
                value > TIGHTNESS_FLOOR for value in tightness),
            "minimum_dual_to_parent_primal_ratio_lower": mp.nstr(
                min(tightness), 24),
            "weighted_threshold_dual_above_9e-5_rows": sum(
                value > WEIGHTED_FLOOR for value in weighted_threshold),
            "weighted_threshold_dual_above_5e-4_rows": sum(
                value > WEIGHTED_MID for value in weighted_threshold),
            "weighted_threshold_dual_above_1e-3_rows": sum(
                value > WEIGHTED_OBSTRUCTION for value in weighted_threshold),
            "weighted_full_prefix_dual_above_1e-3_rows": sum(
                value > WEIGHTED_OBSTRUCTION for value in weighted_full),
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "finite_rational_dual_certificate": True,
            "growing_profile_budget_theorem": False,
            "arithmetic_L2": False,
            "full_gate_B": False,
            "twin_prime_result": False,
        },
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def check_document(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1, "certificate version")
    need(document.get("claim_status") == STATUS, "claim status")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380 and
         audit.get("dual_witness_cases") == 72 and
         audit.get("exact_rational_dual_cases") == 72,
         "finite audit")
    need(audit.get("dual_tightness_floor_cases") == 72 and
         audit.get("weighted_threshold_dual_above_9e-5_rows") == 18 and
         audit.get("weighted_threshold_dual_above_5e-4_rows") == 15 and
         audit.get("weighted_threshold_dual_above_1e-3_rows") == 14 and
         audit.get("weighted_full_prefix_dual_above_1e-3_rows") == 11 and
         audit.get("fixed_power_credit") == 0,
         "dual census")
    need(len(payload.get("rows", [])) == 18 and
         all(len(row.get("dual_cases", [])) == 4
             for row in payload["rows"]), "row payload")


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    try:
        document = build_document()
        check_document(document)
        raw = canonical(document)
        if arguments.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(raw)
        else:
            need(RESULT.is_file(), "missing certificate")
            need(RESULT.read_bytes() == raw, "certificate mismatch")
    except (CheckFailure, OSError, ValueError, json.JSONDecodeError) as error:
        print("TPC300_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC300_CERTIFICATE=PASS rows=18 dual_cases=72 "
          "tight_cases=72 weighted_gt_9e-5=18 weighted_gt_1e-3=14 "
          "full_gt_1e-3=11 fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
