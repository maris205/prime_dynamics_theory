#!/usr/bin/env python3
"""Independent source-image replay for TPC-295.

Only the frozen TPC-268 engine and the hash-locked TPC-294 result are read.
The physical columns are accumulated source-first, and modular rank/target
solves are reconstructed without importing either TPC-294 or TPC-295 code.
"""

from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-295-source-correlation-image-audit"
PARENT_RESULT = ROOT / (
    "papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/results/"
    "tpc294_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc295_certificate.json"
PARENT_RESULT_SHA256 = (
    "a6304d622dc017b15277866c261287000eed119d1f19b7291f9ac191545d14f2")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS")
SCHEMA = "TPC295_SOURCE_CORRELATION_IMAGE_CERTIFICATE_V1"
MODULI = (1000000007, 998244353)

GROWTH_S2 = (
    (128, 24, 9, 5, 2), (192, 32, 16, 5, 2),
    (256, 38, 27, 5, 2), (384, 50, 40, 5, 2),
    (512, 58, 50, 5, 2), (512, 58, 60, 5, 2),
    (512, 58, 70, 5, 2), (512, 58, 90, 5, 2),
)
EXPONENT_CROSSOVER = (
    (256, 38, 27, 5, 1), (384, 50, 40, 5, 1),
    (512, 58, 70, 5, 1), (512, 58, 90, 5, 1),
)
SOURCE_CONTROL_S2 = tuple(
    (384, height, 70, cutoff, 2)
    for height in (48, 52) for cutoff in (3, 5, 7))
ROWS = tuple((args, "GROWTH_S2") for args in GROWTH_S2) + tuple(
    (args, "EXPONENT_CROSSOVER") for args in EXPONENT_CROSSOVER) + tuple(
    (args, "SOURCE_CONTROL_S2") for args in SOURCE_CONTROL_S2)

engine_spec = importlib.util.spec_from_file_location(
    "tpc295_independent_engine", ENGINE_CODE)
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


def parent_data() -> dict[str, Any]:
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC294 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC294 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY"),
         "TPC294 status")
    need(data.get("payload", {}).get("finite_audit", {}).get("rows") == 18,
         "TPC294 rows")
    return data


def shell(q0: int) -> list[int]:
    return [p for p in ENGINE.PRIMES if q0 < p <= 2 * q0]


def source_first(indices: list[int], beta: list[Fraction], height: int,
                 prime: int, exponent: int) -> list[Fraction]:
    out = [Fraction(0) for _ in indices]
    for source, coefficient in zip(indices, beta):
        if source % prime == 0:
            continue
        for position, target in enumerate(indices):
            if target == source or target % prime == 0:
                continue
            centered = Fraction(int(target % prime == source % prime), 1)
            centered -= Fraction(1, prime - 1)
            out[position] += (prime * ENGINE.kernel(target - source, height,
                                                    exponent) * centered *
                              coefficient)
    return out


def residue(value: Fraction, modulus: int) -> int:
    denominator = value.denominator % modulus
    need(denominator != 0, "denominator divisible by modulus")
    return value.numerator % modulus * pow(denominator, modulus - 2,
                                           modulus) % modulus


def rank_and_det(gram: list[list[Fraction]], modulus: int) -> tuple[int, int]:
    a = [[residue(value, modulus) for value in row] for row in gram]
    n = len(a)
    determinant = 1
    rank = 0
    sign = 1
    for column in range(n):
        pivot = next((r for r in range(rank, n) if a[r][column]), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[pivot], a[rank] = a[rank], a[pivot]
            sign = -sign
        pivot_value = a[rank][column]
        determinant = determinant * pivot_value % modulus
        inv = pow(pivot_value, modulus - 2, modulus)
        for j in range(column, n):
            a[rank][j] = a[rank][j] * inv % modulus
        for r in range(rank + 1, n):
            factor = a[r][column]
            for j in range(column, n):
                a[r][j] = (a[r][j] - factor * a[rank][j]) % modulus
        rank += 1
    if sign < 0:
        determinant = (-determinant) % modulus
    return rank, determinant


def target_residual(gram: list[list[Fraction]], target: list[int],
                    modulus: int) -> int:
    n = len(gram)
    original = [[residue(value, modulus) for value in row] for row in gram]
    a = [original[i][:] + [target[i] % modulus] for i in range(n)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if a[r][column]), None)
        need(pivot is not None, "target solve singular")
        a[column], a[pivot] = a[pivot], a[column]
        inv = pow(a[column][column], modulus - 2, modulus)
        a[column] = [v * inv % modulus for v in a[column]]
        for r in range(n):
            if r == column:
                continue
            factor = a[r][column]
            if factor:
                a[r] = [(x - factor * y) % modulus
                        for x, y in zip(a[r], a[column])]
    solution = [a[i][-1] for i in range(n)]
    return max((sum(original[i][j] * solution[j] for j in range(n)) -
                target[i]) % modulus for i in range(n))


def expected_row(parent_row: dict[str, Any]) -> dict[str, Any]:
    scale, height, q0, cutoff, exponent = (
        int(parent_row["scale"]), int(parent_row["H"]), int(parent_row["Q"]),
        int(parent_row["comparison_cutoff_z"]),
        int(parent_row["kernel_exponent"]))
    primes = shell(q0)
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    columns = [source_first(indices, beta, height, q, exponent)
               for q in primes]
    gram = [[sum(columns[i][u] * columns[j][u]
                 for u in range(len(indices))) for j in range(len(primes))]
            for i in range(len(primes))]
    modular = []
    for p in MODULI:
        rank, determinant = rank_and_det(gram, p)
        need(rank == len(primes) and determinant != 0,
             "independent full rank")
        modular.append({"modulus": p, "rank": rank,
                        "determinant": determinant,
                        "all_denominators_invertible": True})
    minimum = [int(v) for v in parent_row["minimum_signed_label"]]
    maximum = [int(v) for v in parent_row["maximum_signed_label"]]
    cut = [int(v) for v in parent_row["maxcut_label"]]
    positive = [1] * len(primes)
    residuals = []
    for p in MODULI:
        residuals.append({
            "modulus": p,
            "minimum_target_residual": target_residual(gram, minimum, p),
            "maxcut_target_residual": target_residual(gram, cut, p),
            "all_positive_target_residual": target_residual(gram, positive, p),
        })
    need(all(item["minimum_target_residual"] == 0 and
             item["maxcut_target_residual"] == 0 and
             item["all_positive_target_residual"] == 0 for item in residuals),
         "independent target residual")
    return {
        "axis": str(parent_row["axis"]), "scale": scale, "H": height,
        "Q": q0, "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent, "shell": primes,
        "shell_cardinality": len(primes),
        "gram_column_rank_modular": modular,
        "minimum_signed_label": minimum,
        "maximum_signed_label": maximum, "maxcut_label": cut,
        "all_positive_label": positive,
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


def main() -> int:
    parent = parent_data()
    mapping = {}
    for row in parent["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))
        mapping[key] = row
    ordered = [mapping[(*args,)] for args, _axis in ROWS]
    workers = min(len(ordered), max(1, os.cpu_count() or 1))
    if workers > 1:
        try:
            with mp.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(expected_row, ordered)
        except (AttributeError, OSError, RuntimeError):
            rows = [expected_row(row) for row in ordered]
    else:
        rows = [expected_row(row) for row in ordered]
    raw = RESULT.read_bytes()
    actual = json.loads(raw)
    need(raw == canonical(actual), "certificate canonicality")
    need(actual.get("certificate_version") == 1 and
         actual.get("claim_status") == STATUS, "header")
    payload = actual["payload"]
    need(payload.get("schema") == SCHEMA, "schema")
    need(payload.get("rows") == rows, "row replay")
    audit = payload["finite_audit"]
    need(audit == {
        "rows": 18, "shell_edges": 1380,
        "moduli": list(MODULI),
        "full_rank_mod_1000000007_rows": 18,
        "full_rank_mod_998244353_rows": 18,
        "source_correlation_surjective_rows": 18,
        "weighted_minimizer_source_realizable_rows": 18,
        "native_restricted_profile_theorem": "OPEN",
        "source_witness_norm_budget": "OPEN",
        "fixed_power_credit": 0,
    }, "audit")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC295_INDEPENDENT_CHECK=PASS rows=18 mod_p1=18 mod_p2=18 "
          "surjective=18 weighted_realizable=18")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC295_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
