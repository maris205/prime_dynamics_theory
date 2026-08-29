#!/usr/bin/env python3
"""Source-first growing-shell budget-gap audit for TPC-302.

TPC-301 established a finite tolerance and normalization robustness result on
18 inherited rows.  This release moves the same native profile budget test
to the 34-row growing/control grid declared by TPC-288.  The signed target is
not imported from the older 18-row atlas: for every row we reconstruct the
literal physical prime outputs, form their exact Gram matrix, and enumerate
all equal-sign labelings.  The resulting minimum is then used as the
weighted target in the source-profile budget calculation.

All physical and profile matrices are rational.  The budget frontier is a
finite high-precision numerical calculation.  Nothing in this file promotes
the finite grid to a growing-shell or arithmetic L2 theorem.
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
TPC288_CODE = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/code/"
    "tpc288_growing_shell_gram_certificate.py")
TPC288_RESULT = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/results/"
    "tpc288_certificate.json")
TPC301_CODE = ROOT / (
    "papers/tpc-301-budget-gap-robustness-audit/code/"
    "tpc301_budget_gap_robustness_audit.py")
TPC301_RESULT = ROOT / (
    "papers/tpc-301-budget-gap-robustness-audit/results/"
    "tpc301_certificate.json")
RESULT = PROJECT / "results/tpc302_certificate.json"

TPC288_CODE_SHA256 = (
    "ee88cef250dc37d14b5fa5bbc22cc9cd5d0a44da6a4e4412118895b27e214987")
TPC288_RESULT_SHA256 = (
    "39ab30b6701015bfaf85ebb670706182ecd7b52120e9963d58d0731a0a8e947d")
TPC301_CODE_SHA256 = (
    "7935d3908b67b6f6cc1c42a330c06ac3de70728268a2d38a6437fad9203b15a8")
TPC301_RESULT_SHA256 = (
    "f92a3c71855541f842b951b72e60e1bfcd641758ec7487d9dfbe3459a7e6e75d")

STATUS = (
    "PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_"
    "MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT")
SCHEMA = "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1"
ROUND2_CLUE = "TEST_UNIFORM_NATIVE_BUDGET_GROWTH_OR_CONSTRUCT_A_GROWING_SHELL_COUNTEREXAMPLE"

PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
TAU_LABELS = ("0.25", "0.5", "0.75")
TAU_VALUES = {label: mp.mpf(label) for label in TAU_LABELS}
NORMALIZATION_NAMES = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")
MP_DPS = 60
FRONTIER_STEPS = 180
FRONTIER_TOL = mp.mpf("1e-42")
FRONTIER_RESIDUAL_TOL = mp.mpf("1e-35")
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-17")

spec = importlib.util.spec_from_file_location("frozen_tpc288_for_tpc302",
                                               TPC288_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-288 parent unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)
ENGINE = PARENT.ENGINE


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    # Do not use assert: the bridge checker deliberately runs with -O too.
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
    return [mp.nstr(value - radius, 38), mp.nstr(value + radius, 38)]


def centre(value: list[str]) -> mp.mpf:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    return (mp.mpf(value[0]) + mp.mpf(value[1])) / 2


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def parent_lock() -> dict[str, Any]:
    need(digest(TPC288_CODE.read_bytes()) == TPC288_CODE_SHA256,
         "TPC-288 code provenance")
    raw288 = TPC288_RESULT.read_bytes()
    need(digest(raw288) == TPC288_RESULT_SHA256, "TPC-288 result provenance")
    data288 = json.loads(raw288)
    need(raw288 == canonical(data288), "TPC-288 canonicality")
    need(data288.get("certificate_version") == 1 and
         data288.get("claim_status", "").startswith(
             "PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY"),
         "TPC-288 status")
    audit288 = data288["payload"]["finite_audit"]
    need(audit288.get("rows") == 34 and
         audit288.get("growth_rows") == 16 and
         audit288.get("source_control_rows") == 18,
         "TPC-288 grid census")

    need(digest(TPC301_CODE.read_bytes()) == TPC301_CODE_SHA256,
         "TPC-301 code provenance")
    raw301 = TPC301_RESULT.read_bytes()
    need(digest(raw301) == TPC301_RESULT_SHA256, "TPC-301 result provenance")
    data301 = json.loads(raw301)
    need(raw301 == canonical(data301), "TPC-301 canonicality")
    need(data301.get("certificate_version") == 1 and
         data301.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY"),
         "TPC-301 status")
    need(data301["payload"]["finite_audit"].get("rows") == 18,
         "TPC-301 row census")
    return {
        "tpc288_code_sha256": TPC288_CODE_SHA256,
        "tpc288_result_sha256": TPC288_RESULT_SHA256,
        "tpc301_code_sha256": TPC301_CODE_SHA256,
        "tpc301_result_sha256": TPC301_RESULT_SHA256,
        "tpc288_rows": 34,
        "tpc301_rows": 18,
    }


def source_specs() -> tuple[tuple[int, int, int, int, int, str], ...]:
    specs: list[tuple[int, int, int, int, int, str]] = []
    for scale, height, q0, cutoff in PARENT.GROWTH_PATH:
        for exponent in (1, 2):
            specs.append((scale, height, q0, cutoff, exponent,
                          "GROWTH_PATH"))
    for scale, height, q0, cutoff, exponent in PARENT.CONTROL_GRID:
        specs.append((scale, height, q0, cutoff, exponent,
                      "SOURCE_CONTROL_GRID"))
    return tuple(specs)


def literal_beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    lam = Fraction(0) if power is None else Fraction(1, power[1])
    divisor_part = sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                        if value % d == 0), 0)
    return lam - divisor_part


def source_profile_matrix(indices: list[int]) -> list[list[Fraction]]:
    return [[literal_beta(value, cutoff) for cutoff in PROFILE_CUTOFFS]
            for value in indices]


def integer_matrix(matrix: list[list[Fraction]]) -> tuple[list[list[int]], int]:
    denominator = 1
    for row in matrix:
        for value in row:
            denominator = __import__("math").lcm(denominator,
                                                  value.denominator)
    scaled = [[value.numerator * (denominator // value.denominator)
               for value in row] for row in matrix]
    return scaled, denominator


def exhaustive_signed_minimum(matrix: list[list[Fraction]]) -> dict[str, Any]:
    """Enumerate all signs with the first label fixed to +1."""
    scaled, denominator = integer_matrix(matrix)
    m = len(scaled)
    need(m > 0 and all(len(row) == m for row in scaled), "square Gram")
    labels = [1] * m
    fields = [sum(scaled[i][j] for j in range(m) if j != i)
              for i in range(m)]
    value = sum(scaled[i][j] for i in range(m) for j in range(m))
    minimum = value
    maximum = value
    minimum_label = tuple(labels)
    maximum_label = tuple(labels)
    minimum_count = 1
    maximum_count = 1
    previous_gray = 0
    for code in range(1, 1 << (m - 1)):
        gray = code ^ (code >> 1)
        changed = gray ^ previous_gray
        vertex = changed.bit_length()
        old = labels[vertex]
        value -= 4 * old * fields[vertex]
        labels[vertex] = -old
        for other in range(m):
            if other != vertex:
                fields[other] -= 2 * old * scaled[other][vertex]
        previous_gray = gray
        candidate = tuple(labels)
        if value < minimum:
            minimum, minimum_label, minimum_count = value, candidate, 1
        elif value == minimum:
            minimum_count += 1
            if candidate < minimum_label:
                minimum_label = candidate
        if value > maximum:
            maximum, maximum_label, maximum_count = value, candidate, 1
        elif value == maximum:
            maximum_count += 1
            if candidate > maximum_label:
                maximum_label = candidate
    trace = sum(scaled[i][i] for i in range(m))
    need(trace > 0, "positive Gram trace")
    return {
        "scaled": scaled,
        "common_denominator": denominator,
        "trace": trace,
        "minimum_integer": minimum,
        "maximum_integer": maximum,
        "minimum_label": minimum_label,
        "maximum_label": maximum_label,
        "minimum_count": minimum_count,
        "maximum_count": maximum_count,
        "enumerated_labelings": 1 << (m - 1),
    }


def physical_gram(indices: list[int], beta: list[Fraction], height: int,
                  shell: list[int], exponent: int
                  ) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    outputs = [PARENT.physical_prime_output(indices, beta, height, prime,
                                             exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u] for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    return outputs, gram


def ratio(scaled: list[list[int]], labels: tuple[int, ...], trace: int
          ) -> Fraction:
    numerator = sum(labels[i] * labels[j] * scaled[i][j]
                    for i in range(len(labels)) for j in range(len(labels)))
    return Fraction(numerator, trace)


def mp_matrices(image: list[list[Fraction]],
                gram: list[list[Fraction]]) -> tuple[mp.matrix, mp.matrix]:
    return (mp.matrix([[as_mp(value) for value in row] for row in image]),
            mp.matrix([[as_mp(value) for value in row] for row in gram]))


def dot(vector: mp.matrix) -> mp.mpf:
    return mp.fsum(vector[index] ** 2 for index in range(len(vector)))


def least_squares(V: mp.matrix, M: mp.matrix,
                  target: mp.matrix) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    coefficients = mp.qr_solve(V, target)[0]
    residual = V * coefficients - target
    residual_squared = dot(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    return coefficients, residual_squared, source_squared


def ridge(V: mp.matrix, M: mp.matrix, target: mp.matrix,
          rho: mp.mpf) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    coefficients = mp.lu_solve(V.T * V + rho * M, V.T * target)
    residual = V * coefficients - target
    return coefficients, dot(residual), (coefficients.T * M * coefficients)[0]


def budget_frontier(V: mp.matrix, M: mp.matrix, target: mp.matrix,
                    tau: mp.mpf) -> dict[str, mp.mpf]:
    target_norm_squared = dot(target)
    radius_squared = tau ** 2 * target_norm_squared
    _, ls_residual_squared, _ = least_squares(V, M, target)
    need(ls_residual_squared <= radius_squared + FRONTIER_TOL,
         "infeasible profile prefix")
    if radius_squared >= target_norm_squared:
        return {"rho": mp.mpf(0), "residual_squared": target_norm_squared,
                "source_squared": mp.mpf(0), "relative_rms": mp.mpf(1)}
    if abs(ls_residual_squared - radius_squared) <= FRONTIER_TOL:
        _, residual_squared, source_squared = least_squares(V, M, target)
        return {"rho": mp.mpf(0), "residual_squared": residual_squared,
                "source_squared": source_squared,
                "relative_rms": mp.sqrt(residual_squared /
                                         target_norm_squared)}
    lo = mp.mpf(0)
    hi = mp.mpf(1)
    while ridge(V, M, target, hi)[1] < radius_squared:
        hi *= 2
        need(hi < mp.mpf("1e100"), "frontier bracket overflow")
    for _ in range(FRONTIER_STEPS):
        mid = (lo + hi) / 2
        if ridge(V, M, target, mid)[1] < radius_squared:
            lo = mid
        else:
            hi = mid
    rho = (lo + hi) / 2
    _, residual_squared, source_squared = ridge(V, M, target, rho)
    need(abs(residual_squared - radius_squared) < FRONTIER_RESIDUAL_TOL,
         "frontier residual")
    return {"rho": rho, "residual_squared": residual_squared,
            "source_squared": source_squared,
            "relative_rms": mp.sqrt(residual_squared /
                                     target_norm_squared)}


def normalizers(M: mp.matrix, k: int,
                beta_norm_squared: mp.mpf) -> dict[str, mp.mpf]:
    trace_mean = mp.fsum(M[i, i] for i in range(k)) / k
    first = M[0, 0]
    need(beta_norm_squared > 0 and trace_mean > 0 and first > 0,
         "positive source normalizer")
    return {"beta_norm_squared": beta_norm_squared,
            "profile_trace_mean": trace_mean,
            "first_profile_norm_squared": first}


def saved_budget(raw: dict[str, mp.mpf], M: mp.matrix, k: int,
                 beta_norm_squared: mp.mpf) -> tuple[dict[str, Any], dict[str, mp.mpf]]:
    norms = normalizers(M, k, beta_norm_squared)
    ratios = {name: raw["source_squared"] / value
              for name, value in norms.items()}
    return ({"k": k, "cutoff": PROFILE_CUTOFFS[k - 1],
             "relative_rms": enclosure(raw["relative_rms"]),
             "ridge_parameter_rho": enclosure(raw["rho"]),
             "source_budget": enclosure(raw["source_squared"]),
             "normalizers": {name: enclosure(value)
                             for name, value in norms.items()},
             "budget_over_normalizer": {name: enclosure(value)
                                        for name, value in ratios.items()}},
            {"source_squared": raw["source_squared"], "ratios": ratios,
             "relative_rms": raw["relative_rms"]})


def make_context(V: mp.matrix, M: mp.matrix, targets: dict[str, mp.matrix],
                 k_by_target: dict[str, int], tau: mp.mpf,
                 beta_norm_squared: mp.mpf) -> tuple[dict[str, Any], dict[str, Any]]:
    saved: dict[str, Any] = {}
    raw: dict[str, Any] = {}
    for name, target in targets.items():
        k = int(k_by_target[name])
        item, raw_item = saved_budget(
            budget_frontier(V[:, :k], M[:k, :k], target, tau), M, k,
            beta_norm_squared)
        saved[name] = item
        raw[name] = raw_item
    gaps = {name: raw["weighted"]["ratios"][name] /
            raw["positive"]["ratios"][name]
            for name in NORMALIZATION_NAMES}
    return ({"k_by_target": {name: int(value)
                              for name, value in k_by_target.items()},
             "cutoff_by_target": {
                 name: PROFILE_CUTOFFS[int(k_by_target[name]) - 1]
                 for name in targets},
             "targets": saved,
             "weighted_to_positive_gap": {
                 name: enclosure(value) for name, value in gaps.items()}},
            {"targets": raw, "gaps": gaps})


def build_row(specification: tuple[int, int, int, int, int, str]
              ) -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    scale, height, q0, cutoff, exponent, axis = specification
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    need(len(shell) >= 3, "small prime shell")
    outputs, gram = physical_gram(indices, beta, height, shell, exponent)
    need(all(gram[i][i] > 0 for i in range(len(shell))), "Gram diagonal")
    optimum = exhaustive_signed_minimum(gram)
    scaled = optimum["scaled"]
    trace = optimum["trace"]
    weighted_ratio = ratio(scaled, optimum["minimum_label"], trace)
    positive_ratio = ratio(scaled, (1,) * len(shell), trace)

    profiles = source_profile_matrix(indices)
    image = [[sum((outputs[row][u] * profiles[u][column]
                   for u in range(len(indices))), Fraction(0))
              for column in range(len(PROFILE_CUTOFFS))]
             for row in range(len(shell))]
    profile_gram = [[sum((profiles[u][left] * profiles[u][right]
                          for u in range(len(indices))), Fraction(0))
                     for right in range(len(PROFILE_CUTOFFS))]
                    for left in range(len(PROFILE_CUTOFFS))]
    V, M = mp_matrices(image, profile_gram)
    targets = {
        "weighted": mp.matrix([mp.mpf(int(value))
                                for value in optimum["minimum_label"]]),
        "positive": mp.matrix([mp.mpf(1) for _ in shell]),
    }
    beta_norm_squared = mp.fsum(as_mp(value) ** 2 for value in beta)
    prefix_count = min(len(shell), len(PROFILE_CUTOFFS))
    least_squares_rms: dict[str, list[list[str]]] = {name: []
                                                      for name in targets}
    ls_raw: dict[str, list[mp.mpf]] = {name: [] for name in targets}
    for name, target in targets.items():
        for k in range(1, prefix_count + 1):
            _, residual_squared, _ = least_squares(
                V[:, :k], M[:k, :k], target)
            value = mp.sqrt(residual_squared / dot(target))
            ls_raw[name].append(value)
            least_squares_rms[name].append(enclosure(value))

    tolerance_records: dict[str, Any] = {}
    raw_records: dict[str, Any] = {}
    prefix_order_cases = 0
    normalization_cases = 0
    monotone_cases = 0
    for tau_label in TAU_LABELS:
        tau = TAU_VALUES[tau_label]
        thresholds = {}
        for name in targets:
            found = next((i + 1 for i, value in enumerate(ls_raw[name])
                          if value <= tau), None)
            need(found is not None, "no feasible prefix")
            thresholds[name] = int(found)
        if thresholds["positive"] <= thresholds["weighted"]:
            prefix_order_cases += 1
        # A common prefix is the smallest prefix feasible for both targets.
        common = max(thresholds.values())
        contexts: dict[str, Any] = {}
        contexts_raw: dict[str, Any] = {}
        specs = {
            "common_prefix": {name: common for name in targets},
            "target_specific_prefix": thresholds,
            "full_prefix": {name: prefix_count for name in targets},
        }
        for context_name, k_by_target in specs.items():
            saved, raw = make_context(V, M, targets, k_by_target, tau,
                                      beta_norm_squared)
            contexts[context_name] = saved
            contexts_raw[context_name] = raw
            if context_name == "common_prefix":
                spread = (max(raw["gaps"].values()) -
                          min(raw["gaps"].values()))
                need(spread < mp.mpf("1e-35"),
                     "common normalization invariance")
                normalization_cases += 1
        tolerance_records[tau_label] = {
            "threshold_k": thresholds,
            "contexts": contexts,
        }
        raw_records[tau_label] = contexts_raw

    for name in targets:
        sequence = [raw_records[label]["full_prefix"]["targets"][name]
                    ["source_squared"] for label in TAU_LABELS]
        need(sequence[0] + mp.mpf("1e-35") >= sequence[1] and
             sequence[1] + mp.mpf("1e-35") >= sequence[2],
             "full-prefix tolerance monotonicity")
        monotone_cases += 1

    common_gaps = []
    common_budgets = {name: [] for name in NORMALIZATION_NAMES}
    full_gaps = []
    for label in TAU_LABELS:
        common_raw = raw_records[label]["common_prefix"]
        full_raw = raw_records[label]["full_prefix"]
        common_gaps.append(common_raw["gaps"]["beta_norm_squared"])
        full_gaps.append(full_raw["gaps"]["beta_norm_squared"])
        for name in NORMALIZATION_NAMES:
            common_budgets[name].append(
                common_raw["targets"]["weighted"]["ratios"][name])

    return {
        "axis": axis,
        "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": len(indices), "shell": shell,
        "shell_cardinality": len(shell),
        "profile_cutoffs": list(PROFILE_CUTOFFS),
        "tested_prefix_count": prefix_count,
        "beta_norm_squared": enclosure(beta_norm_squared),
        "target_norm_squared": len(shell),
        "weighted_target_label": list(optimum["minimum_label"]),
        "positive_target_label": [1] * len(shell),
        "target_label_provenance": (
            "source-first exact physical Gram; exhaustive equal-sign enumeration "
            "with global sign fixed at the first shell prime"),
        "enumerated_labelings": optimum["enumerated_labelings"],
        "weighted_minimum_ratio": str(weighted_ratio),
        "weighted_minimum_ratio_decimal": ENGINE.decimal_text(weighted_ratio),
        "positive_ratio": str(positive_ratio),
        "positive_ratio_decimal": ENGINE.decimal_text(positive_ratio),
        "weighted_below_one": weighted_ratio < 1,
        "positive_above_one": positive_ratio > 1,
        "minimum_count_mod_global_sign": optimum["minimum_count"],
        "maximum_count_mod_global_sign": optimum["maximum_count"],
        "common_denominator_bits": optimum["common_denominator"].bit_length(),
        "least_squares_rms": least_squares_rms,
        "tolerance_audits": tolerance_records,
        "common_gap_centres": [mp.nstr(value, 38)
                               for value in common_gaps],
        "full_gap_centres": [mp.nstr(value, 38)
                             for value in full_gaps],
        "common_weighted_budget_centres": {
            name: [mp.nstr(value, 38)
                   for value in values]
            for name, values in common_budgets.items()},
        "invariance_checks": {
            "prefix_order_positive_le_weighted": prefix_order_cases,
            "common_prefix_normalization": normalization_cases,
            "full_prefix_tolerance_monotonicity": monotone_cases,
        },
    }


def build_rows() -> list[dict[str, Any]]:
    specs = source_specs()
    requested = os.environ.get("TPC302_WORKERS", "8")
    try:
        workers = max(1, min(len(specs), int(requested)))
    except ValueError:
        workers = 8
    if workers == 1:
        return [build_row(item) for item in specs]
    try:
        with mp_pool.get_context("fork").Pool(processes=workers) as pool:
            return pool.map(build_row, specs)
    except (AttributeError, OSError, RuntimeError):
        return [build_row(item) for item in specs]


def build_payload() -> dict[str, Any]:
    rows = build_rows()
    need(len(rows) == 34, "row census")
    need(sum(len(row["shell"]) for row in rows) == 430,
         "explicit shell target census")
    need(all(row["tested_prefix_count"] ==
             min(row["shell_cardinality"], len(PROFILE_CUTOFFS))
             for row in rows), "prefix census")
    need(all(row["weighted_below_one"] for row in rows),
         "weighted contraction census")
    need(all(row["positive_above_one"] for row in rows),
         "positive amplification census")

    common = {label: [] for label in TAU_LABELS}
    full = {label: [] for label in TAU_LABELS}
    budgets = {name: [] for name in NORMALIZATION_NAMES}
    for row in rows:
        for index, label in enumerate(TAU_LABELS):
            common[label].append(mp.mpf(row["common_gap_centres"][index]))
            full[label].append(mp.mpf(row["full_gap_centres"][index]))
            for name in NORMALIZATION_NAMES:
                budgets[name].append(mp.mpf(
                    row["common_weighted_budget_centres"][name][index]))

    def counts(values: list[mp.mpf], threshold: str) -> int:
        return sum(value > mp.mpf(threshold) for value in values)

    minimum_weighted = min(rows, key=lambda row: mp.mpf(
        row["weighted_minimum_ratio_decimal"]))
    minimum_gap = {label: min(common[label]) for label in TAU_LABELS}
    minimum_full_gap = {label: min(full[label]) for label in TAU_LABELS}
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "grid": {
            "source_specs": [list(item) for item in source_specs()],
            "growth_rows": 16, "source_control_rows": 18,
            "profile_cutoffs": list(PROFILE_CUTOFFS),
            "tolerance_ladder": list(TAU_LABELS),
            "explicit_shell_target_count": 430,
            "inherited_parent_grid_edge_count": 1380,
        },
        "exact_theorem": {
            "physical_gram": "G_{q,r}=<g_q,g_r>",
            "psd_identity": "c^T G c=||sum_q c_q g_q||_2^2>=0",
            "global_sign_reduction": (
                "the quadratic form is invariant under c -> -c, so fixing "
                "the first sign to +1 enumerates every global-sign class"),
            "gray_enumeration": (
                "the reflected Gray traversal changes one sign at a time and "
                "visits exactly 2^(|S|-1) classes"),
            "budget_definition": (
                "B_(k,tau)(b)=min{c^T M_k c: ||V_kc-b|| <= tau||b||}"),
            "budget_monotonicity": (
                "relaxing tau or enlarging a profile prefix cannot increase "
                "the feasible-set minimum"),
            "common_normalization": (
                "a positive target-independent normalizer cancels in a "
                "same-prefix weighted/positive ratio"),
            "scope": "finite literal source, finite prime shells, and declared tolerances",
        },
        "finite_audit": {
            "rows": len(rows), "growth_rows": 16,
            "source_control_rows": 18,
            "explicit_shell_target_count": 430,
            "inherited_parent_grid_edge_count": 1380,
            "profile_count": len(PROFILE_CUTOFFS),
            "tolerance_ladder": list(TAU_LABELS),
            "frontier_cases": len(rows) * len(TAU_LABELS) * 3 * 2,
            "weighted_below_one_rows": sum(row["weighted_below_one"]
                                            for row in rows),
            "positive_above_one_rows": sum(row["positive_above_one"]
                                           for row in rows),
            "common_gap_min_by_tau": {
                label: mp.nstr(value, 38)
                for label, value in minimum_gap.items()},
            "full_gap_min_by_tau": {
                label: mp.nstr(value, 38)
                for label, value in minimum_full_gap.items()},
            "common_gap_above_10_by_tau": {
                label: counts(common[label], "10") for label in TAU_LABELS},
            "common_gap_above_2_by_tau": {
                label: counts(common[label], "2") for label in TAU_LABELS},
            "full_gap_above_10_by_tau": {
                label: counts(full[label], "10") for label in TAU_LABELS},
            "common_budget_min_by_normalization": {
                name: mp.nstr(min(values), 38)
                for name, values in budgets.items()},
            "common_budget_above_1e-5_by_normalization": {
                name: counts(values, "1e-5")
                for name, values in budgets.items()},
            "prefix_order_cases": sum(
                row["invariance_checks"]["prefix_order_positive_le_weighted"]
                for row in rows),
            "common_normalization_cases": sum(
                row["invariance_checks"]["common_prefix_normalization"]
                for row in rows),
            "full_tolerance_monotonicity_cases": sum(
                row["invariance_checks"]["full_prefix_tolerance_monotonicity"]
                for row in rows),
            "minimum_weighted_ratio_witness": {
                key: minimum_weighted[key] for key in (
                    "axis", "scale", "H", "Q", "comparison_cutoff_z",
                    "kernel_exponent", "shell", "weighted_minimum_ratio_decimal")
            },
            "growing_profile_budget_theorem": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC302_SOURCE_FIRST_SIGN_ENUMERATION": "PROVED_EXACT_FINITE",
            "TPC302_PHYSICAL_GRAM_PSD": "PROVED_EXACT_FINITE",
            "TPC302_BUDGET_TOLERANCE_AND_PREFIX_MONOTONICITY":
                "PROVED_EXACT_FINITE",
            "TPC302_GROWING_GRID_BUDGET_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_34_ROWS",
            "TPC302_COMMON_NORMALIZATION_AUDIT":
                "NUMERICALLY_CERTIFIED_FINITE",
            "TPC302_UNIFORM_GROWING_PROFILE_BUDGET": "OPEN",
            "TPC302_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC302_FIXED_POWER_CREDIT": 0,
            "TPC302_FULL_GATE_B": "OPEN",
            "TPC302_TWIN_PRIME_RESULT": "NONE",
            "TPC302_STATUS": STATUS,
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
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    need(data.get("payload", {}).get("schema") == SCHEMA,
         "certificate schema")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    need(audit.get("rows") == 34 and
         audit.get("explicit_shell_target_count") == 430 and
         audit.get("frontier_cases") == 612 and
         audit.get("profile_count") == 17 and
         audit.get("tolerance_ladder") == list(TAU_LABELS),
         "finite census")
    need(len(data["payload"].get("rows", [])) == 34,
         "row payload")
    print("TPC302_CERTIFICATE=PASS rows=34 shell_targets=430 "
          "frontier_cases=612 weighted_below_one={} positive_above_one={} "
          "gap_gt_10={}/{}/{}".format(
              audit["weighted_below_one_rows"],
              audit["positive_above_one_rows"],
              audit["common_gap_above_10_by_tau"]["0.25"],
              audit["common_gap_above_10_by_tau"]["0.5"],
              audit["common_gap_above_10_by_tau"]["0.75"]))


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
        print("TPC302_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
