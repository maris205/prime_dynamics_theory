#!/usr/bin/env python3
"""Independent high-precision replay for TPC-296.

The checker does not import the TPC-296 producer.  It reads only the frozen
TPC-295 result and the frozen cutoff engine, accumulates physical columns in
source-first order, and redoes the least-norm/profile calculations.
"""

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
PROJECT = ROOT / "papers/tpc-296-source-norm-budget-interface"
PARENT_RESULT = ROOT / (
    "papers/tpc-295-source-correlation-image-audit/results/"
    "tpc295_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc296_certificate.json"
PARENT_RESULT_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET_AND_SOURCE_ENERGY_TRADEOFF_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_COST_PROFILE_ATLAS")
SCHEMA = "TPC296_SOURCE_NORM_BUDGET_CERTIFICATE_V1"
MODULI = (1000000007, 998244353)
MP_DPS = 70
CHECK_RADIUS = mp.mpf("1e-12")
BUDGET_RATIO_THRESHOLD = mp.mpf("1e-3")
PROFILE_RMS_THRESHOLD = mp.mpf("0.9")

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
    "tpc296_independent_engine", ENGINE_CODE)
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
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "engine provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC295 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC295 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION"),
         "TPC295 status")
    return data


def source_first(indices: list[int], beta: list[Fraction], height: int,
                 prime: int, exponent: int) -> list[Fraction]:
    output = [Fraction(0) for _ in indices]
    for source, coefficient in zip(indices, beta):
        if source % prime == 0:
            continue
        for position, target in enumerate(indices):
            if target == source or target % prime == 0:
                continue
            centered = Fraction(int(target % prime == source % prime), 1)
            centered -= Fraction(1, prime - 1)
            output[position] += (prime * ENGINE.kernel(target - source,
                                                        height, exponent) *
                                 centered * coefficient)
    return output


def as_mp(value: Fraction | int) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def interval_contains(value: mp.mpf, interval: list[str]) -> bool:
    lo, hi = (mp.mpf(interval[0]), mp.mpf(interval[1]))
    tolerance = CHECK_RADIUS * max(mp.mpf(1), abs(value))
    return lo - tolerance <= value <= hi + tolerance


def expected(item: tuple[tuple[int, int, int, int, int], str,
                    dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    mp.mp.dps = MP_DPS
    (scale, height, q0, cutoff, exponent), axis, parent_row = item
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    columns = [source_first(indices, beta, height, prime, exponent)
               for prime in shell]
    A = mp.matrix([[as_mp(columns[j][i]) for j in range(len(shell))]
                   for i in range(len(indices))])
    G = A.T * A
    eigenvalues = mp.eigsy(G, eigvals_only=True)
    eigen_min = eigenvalues[0]
    eigen_max = eigenvalues[len(shell) - 1]
    need(eigen_min > 0, "independent positive eigenvalue")
    beta_norm_squared = mp.fsum(as_mp(value) ** 2 for value in beta)
    beta_source = mp.matrix([as_mp(value) for value in beta])
    native = A.T * beta_source
    native_norm_squared = (native.T * native)[0]
    raw_targets: dict[str, dict[str, mp.mpf]] = {}
    for name, key in (("minimum", "minimum_signed_label"),
                      ("maxcut", "maxcut_label"),
                      ("plus", "all_positive_label")):
        label = [int(value) for value in parent_row[key]]
        if name == "plus":
            label = [1] * len(shell)
        b = mp.matrix(label)
        coefficients = mp.lu_solve(G, b)
        h = A * coefficients
        recovered = A.T * h
        residual = max(abs(recovered[i] - b[i]) for i in range(len(shell)))
        cost = (b.T * coefficients)[0]
        source_norm_squared = (h.T * h)[0]
        energy = (b.T * (G * b))[0]
        profile_alpha = (native.T * b)[0] / native_norm_squared
        profile_rms = mp.sqrt(mp.fsum(
            (profile_alpha * native[i] - b[i]) ** 2
            for i in range(len(shell))) / len(shell))
        trade_product = cost * energy / (mp.mpf(len(shell)) ** 2)
        need(residual < mp.mpf("1e-45"), "independent correlation residual")
        need(abs(source_norm_squared - cost) < mp.mpf("1e-45"),
             "independent norm identity")
        need(trade_product >= 1 - mp.mpf("1e-40"),
             "independent tradeoff")
        raw_targets[name] = {
            "least_norm_cost": cost,
            "cost_over_beta_norm_squared": cost / beta_norm_squared,
            "profile_ray_rms": profile_rms,
            "physical_energy": energy,
            "source_energy_trade_product": trade_product,
        }
    raw = {
        "condition": eigen_max / eigen_min,
        "beta_norm_squared": beta_norm_squared,
        "eigen_min": eigen_min,
        "eigen_max": eigen_max,
        "targets": raw_targets,
    }
    return {"axis": axis, "scale": scale, "H": height, "Q": q0,
            "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
            "shell": shell, "shell_cardinality": len(shell)}, raw


def check_row(actual: dict[str, Any], expected_row: dict[str, Any],
              raw: dict[str, Any]) -> None:
    for key in ("axis", "scale", "H", "Q", "comparison_cutoff_z",
                "kernel_exponent", "shell", "shell_cardinality"):
        need(actual.get(key) == expected_row[key], "row metadata: " + key)
    for key, value in (("beta_norm_squared", raw["beta_norm_squared"]),
                       ("gram_eigenvalue_min", raw["eigen_min"]),
                       ("gram_eigenvalue_max", raw["eigen_max"]),
                       ("gram_condition_number", raw["condition"])):
        need(interval_contains(value, actual[key]), "row interval: " + key)
    for name, metrics in raw["targets"].items():
        got = actual["targets"][name]
        for key, value in metrics.items():
            if key == "least_norm_cost":
                field = "least_norm_cost"
            elif key == "cost_over_beta_norm_squared":
                field = "cost_over_beta_norm_squared"
            elif key == "profile_ray_rms":
                field = "profile_ray_rms"
            elif key == "physical_energy":
                field = "physical_energy"
            else:
                field = "source_energy_trade_product"
            need(interval_contains(value, got[field]),
                 "target interval: " + name + ":" + field)
        need(mp.mpf(got["correlation_residual_upper"]) < mp.mpf("1e-40"),
             "stored correlation residual")
        need(mp.mpf(got["norm_identity_residual_upper"]) < mp.mpf("1e-40"),
             "stored norm residual")


def main() -> int:
    parent = parent_data()
    mapping = {}
    for row in parent["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))
        mapping[key] = row
    items = [(args, axis, mapping[args]) for args, axis in ROWS]
    workers = min(len(items), max(1, os.cpu_count() or 1))
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                replay = pool.map(expected, items)
        except (AttributeError, OSError, RuntimeError):
            replay = [expected(item) for item in items]
    else:
        replay = [expected(item) for item in items]
    actual = json.loads(RESULT.read_bytes())
    raw_result = RESULT.read_bytes()
    need(raw_result == canonical(actual), "TPC296 canonicality")
    need(actual.get("certificate_version") == 1 and
         actual.get("claim_status") == STATUS, "TPC296 header")
    payload = actual["payload"]
    need(payload.get("schema") == SCHEMA, "TPC296 schema")
    need(payload["parent_lock"]["tpc295_result_sha256"] ==
         PARENT_RESULT_SHA256, "parent lock")
    raw_rows = []
    for actual_row, (expected_row, raw) in zip(payload["rows"], replay):
        check_row(actual_row, expected_row, raw)
        raw_rows.append(raw)
    audit = payload["finite_audit"]
    need(audit["rows"] == 18 and audit["shell_edges"] == 1380,
         "audit counts")
    min_budget = [r["targets"]["minimum"]["cost_over_beta_norm_squared"]
                  for r in raw_rows]
    min_profile = [r["targets"]["minimum"]["profile_ray_rms"]
                   for r in raw_rows]
    conditions = [r["condition"] for r in raw_rows]
    trades = [r["targets"][name]["source_energy_trade_product"]
              for r in raw_rows for name in ("minimum", "maxcut", "plus")]
    need(sum(v <= BUDGET_RATIO_THRESHOLD for v in min_budget) ==
         audit["weighted_minimizer_budget_below_threshold_rows"] == 18,
         "budget census")
    need(sum(v >= PROFILE_RMS_THRESHOLD for v in min_profile) ==
         audit["weighted_minimizer_profile_ray_rms_at_least_threshold_rows"] == 18,
         "profile census")
    need(max(conditions) < mp.mpf("2500"), "condition bound")
    need(min(trades) >= 1, "trade census")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC296_INDEPENDENT_CHECK=PASS rows=18 min_budget=18 "
          "min_profile=18 trade_failures=0")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC296_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
