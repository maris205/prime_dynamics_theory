#!/usr/bin/env python3
"""Finite source-correlation image audit for the TPC-294 shell optima.

TPC-294 optimized signs in the ambient coefficient cube.  This release
studies the source-side correlation map A^T, where A has the physical shell
vectors as columns.  A nonzero Gram determinant makes that map surjective on
the finite rational source space.  The rank observations are certified by
two modular determinants; the native restricted source class remains open.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import multiprocessing as mp
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/code/"
    "tpc294_magnitude_weighted_signed_rayleigh_certificate.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/results/"
    "tpc294_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc295_certificate.json"

PARENT_CODE_SHA256 = (
    "74fadde1853e2e03aee223a61393ceb845326ce8c7baf5d2a4015be988dc62d2")
PARENT_RESULT_SHA256 = (
    "a6304d622dc017b15277866c261287000eed119d1f19b7291f9ac191545d14f2")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS")
SCHEMA = "TPC295_SOURCE_CORRELATION_IMAGE_CERTIFICATE_V1"
ROUND2_CLUE = "TEST_SOURCE_NORM_COST_AND_RESTRICTED_NATIVE_PROFILE_IMAGE"
MODULI = (1000000007, 998244353)

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc294_for_tpc295", PARENT_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-294 parent unavailable")
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


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC294 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC294 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC294 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY"),
         "TPC294 status")
    audit = data.get("payload", {}).get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("total_edges") == 1380,
         "TPC294 finite audit")
    return {"tpc294_code_sha256": PARENT_CODE_SHA256,
            "tpc294_result_sha256": PARENT_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "tpc294_rows": 18, "tpc294_edges": 1380}


def load_parent_rows() -> dict[tuple[int, int, int, int, int], dict[str, Any]]:
    raw = PARENT_RESULT.read_bytes()
    data = json.loads(raw)
    result: dict[tuple[int, int, int, int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))
        need(key not in result, "duplicate TPC294 row")
        result[key] = row
    need(len(result) == 18, "TPC294 row map")
    return result


def shell_between(q0: int) -> list[int]:
    return [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    """Target-first physical accumulation, inherited by the producer."""
    output: list[Fraction] = []
    for target in indices:
        total = Fraction(0)
        for source, coefficient in zip(indices, beta):
            if (target == source or target % prime == 0 or
                    source % prime == 0):
                continue
            centered = Fraction(int(target % prime == source % prime), 1)
            centered -= Fraction(1, prime - 1)
            total += (prime * ENGINE.kernel(target - source, height, exponent)
                      * centered * coefficient)
        output.append(total)
    return output


def mod_fraction(value: Fraction, modulus: int) -> int:
    denominator = value.denominator % modulus
    need(denominator != 0, "noninvertible Gram denominator")
    return (value.numerator % modulus) * pow(denominator, modulus - 2,
                                             modulus) % modulus


def modular_rank_determinant(gram: list[list[Fraction]],
                             modulus: int) -> tuple[int, int, bool]:
    matrix = [[mod_fraction(value, modulus) for value in row]
              for row in gram]
    size = len(matrix)
    determinant = 1
    rank = 0
    swaps = 0
    for column in range(size):
        pivot = next((row for row in range(rank, size)
                      if matrix[row][column] != 0), None)
        if pivot is None:
            continue
        if pivot != rank:
            matrix[pivot], matrix[rank] = matrix[rank], matrix[pivot]
            swaps += 1
        pivot_value = matrix[rank][column]
        determinant = determinant * pivot_value % modulus
        inverse = pow(pivot_value, modulus - 2, modulus)
        for j in range(column, size):
            matrix[rank][j] = matrix[rank][j] * inverse % modulus
        for row in range(rank + 1, size):
            factor = matrix[row][column]
            if factor:
                for j in range(column, size):
                    matrix[row][j] = (matrix[row][j] -
                                      factor * matrix[rank][j]) % modulus
        rank += 1
    if swaps % 2:
        determinant = (-determinant) % modulus
    return rank, determinant, all(
        value.denominator % modulus != 0
        for row in gram for value in row)


def target_residual_mod(gram: list[list[Fraction]], labels: list[int],
                        modulus: int) -> int:
    """Solve Gc=labels modulo p and return max residual (zero expected)."""
    size = len(gram)
    coefficient_matrix = [[mod_fraction(gram[i][j], modulus)
                           for j in range(size)] for i in range(size)]
    augmented = [coefficient_matrix[i][:] +
                 [labels[i] % modulus] for i in range(size)]
    rank = 0
    for column in range(size):
        pivot = next((row for row in range(rank, size)
                      if augmented[row][column]), None)
        need(pivot is not None, "modular target solve pivot")
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inverse = pow(augmented[rank][column], modulus - 2, modulus)
        augmented[rank] = [(value * inverse) % modulus
                           for value in augmented[rank]]
        for row in range(size):
            if row == rank:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(augmented[row], augmented[rank])]
        rank += 1
    solution = [augmented[row][-1] for row in range(size)]
    return max((sum(coefficient_matrix[row][column] * solution[column]
                    for column in range(size)) - labels[row]) % modulus
               for row in range(size))


def build_row(parent_row: dict[str, Any]) -> dict[str, Any]:
    scale = int(parent_row["scale"])
    height = int(parent_row["H"])
    q0 = int(parent_row["Q"])
    cutoff = int(parent_row["comparison_cutoff_z"])
    exponent = int(parent_row["kernel_exponent"])
    axis = str(parent_row["axis"])
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = shell_between(q0)
    outputs = [physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices))) for j in range(len(shell))]
            for i in range(len(shell))]
    need(all(gram[i][i] > 0 for i in range(len(shell))), "diagonal")
    modular: list[dict[str, Any]] = []
    for modulus in MODULI:
        rank, determinant, invertible = modular_rank_determinant(gram, modulus)
        need(invertible and rank == len(shell) and determinant != 0,
             "finite modular full rank")
        modular.append({"modulus": modulus, "rank": rank,
                        "determinant": determinant,
                        "all_denominators_invertible": invertible})
    minimum_label = [int(value) for value in parent_row["minimum_signed_label"]]
    maxcut_label = [int(value) for value in parent_row["maxcut_label"]]
    plus_label = [1] * len(shell)
    residuals = [{"modulus": modulus,
                  "minimum_target_residual": target_residual_mod(
                      gram, minimum_label, modulus),
                  "maxcut_target_residual": target_residual_mod(
                      gram, maxcut_label, modulus),
                  "all_positive_target_residual": target_residual_mod(
                      gram, plus_label, modulus)} for modulus in MODULI]
    need(all(item["minimum_target_residual"] == 0 and
             item["maxcut_target_residual"] == 0 and
             item["all_positive_target_residual"] == 0 for item in residuals),
         "modular source targets")
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "gram_column_rank_modular": modular,
        "minimum_signed_label": minimum_label,
        "maximum_signed_label": [int(value)
                                 for value in parent_row["maximum_signed_label"]],
        "maxcut_label": maxcut_label,
        "all_positive_label": plus_label,
        "minimum_signed_ratio": parent_row["minimum_signed_ratio"],
        "minimum_signed_ratio_decimal": parent_row[
            "minimum_signed_ratio_decimal"],
        "maxcut_ratio": parent_row["maxcut_ratio"],
        "maxcut_ratio_decimal": parent_row["maxcut_ratio_decimal"],
        "source_correlation_map": "A^T:h->(<h,g_q>)_q",
        "source_domain": "Q^I_on_the_frozen_finite_interval",
        "full_rank_condition": True,
        "source_correlation_surjective": True,
        "minimum_witness_formula": "h=A G^{-1} a_min",
        "maxcut_witness_formula": "h=A G^{-1} a_maxcut",
        "all_positive_witness_formula": "h=A G^{-1} 1",
        "target_residuals_modular": residuals,
        "restricted_native_profile_status": "OPEN",
    }


def build_payload() -> dict[str, Any]:
    parent_lock_value = parent_lock()
    parent_rows = load_parent_rows()
    ordered = []
    for args, axis in PARENT.ROWS:
        scale, height, q0, cutoff, exponent = args
        key = (scale, height, q0, cutoff, exponent)
        need(key in parent_rows, "parent row missing")
        ordered.append(parent_rows[key])
    workers = min(len(ordered), max(1, os.cpu_count() or 1))
    if workers > 1:
        try:
            with mp.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(build_row, ordered)
        except (AttributeError, OSError, RuntimeError):
            rows = [build_row(row) for row in ordered]
    else:
        rows = [build_row(row) for row in ordered]
    need(len(rows) == 18, "row census")
    need(all(row["source_correlation_surjective"] for row in rows),
         "source image census")
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock_value,
        "exact_theorem": {
            "matrix": "A=[g_q] and G=A^T A",
            "correlation_map": "C=A^T:Q^I->Q^m",
            "full_rank_implication": "rank(G)=m implies C is surjective",
            "explicit_witness": "h=A G^{-1} b gives A^T h=b",
            "sign_targets": "b in {+-1}^m are therefore attainable",
            "scope": "unrestricted finite rational source coordinates",
        },
        "finite_audit": {
            "rows": len(rows),
            "shell_edges": 1380,
            "moduli": list(MODULI),
            "full_rank_mod_1000000007_rows": sum(
                row["gram_column_rank_modular"][0]["rank"] == row["shell_cardinality"]
                for row in rows),
            "full_rank_mod_998244353_rows": sum(
                row["gram_column_rank_modular"][1]["rank"] == row["shell_cardinality"]
                for row in rows),
            "source_correlation_surjective_rows": sum(
                row["source_correlation_surjective"] for row in rows),
            "weighted_minimizer_source_realizable_rows": sum(
                row["source_correlation_surjective"] for row in rows),
            "native_restricted_profile_theorem": "OPEN",
            "source_witness_norm_budget": "OPEN",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC295_FULL_RANK_IMPLICATION": "PROVED_EXACT_FINITE",
            "TPC295_MODULAR_FULL_RANK_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_TWO_MODULI",
            "TPC295_UNRESTRICTED_SOURCE_CORRELATION_SURJECTIVITY":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
            "TPC295_WEIGHTED_MINIMIZER_SOURCE_REALIZABILITY":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED",
            "TPC295_RESTRICTED_NATIVE_PROFILE": "OPEN_LITERAL_SOURCE",
            "TPC295_SOURCE_WITNESS_NORM": "OPEN",
            "TPC295_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC295_FIXED_POWER_CREDIT": 0,
            "TPC295_FULL_GATE_B": "OPEN",
            "TPC295_TWIN_PRIME_RESULT": "NONE",
            "TPC295_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def frozen_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(frozen_document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data == frozen_document(), "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    print("TPC295_CERTIFICATE=PASS rows={} mod_p1={} mod_p2={} "
          "surjective={} weighted_realizable={} fixed_power_credit={}".format(
              audit["rows"], audit["full_rank_mod_1000000007_rows"],
              audit["full_rank_mod_998244353_rows"],
              audit["source_correlation_surjective_rows"],
              audit["weighted_minimizer_source_realizable_rows"],
              audit["fixed_power_credit"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    if args.write:
        write()
    else:
        check()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC295_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
