#!/usr/bin/env python3
"""TPC-301 finite tolerance and source-normalization robustness audit.

TPC-300 exported the native profile budget as an exact finite dual witness.
This release attacks the finite obstruction itself: it varies the target
tolerance, compares common and target-specific profile prefixes, and audits
three source-side normalizations.  The theorem layer is finite and elementary;
the atlas remains numerical and carries no asymptotic arithmetic credit.
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
UPSTREAM_CODE = ROOT / (
    "papers/tpc-299-native-profile-budget-frontier/code/"
    "tpc299_native_profile_budget_frontier_certificate.py")
UPSTREAM_RESULT = ROOT / (
    "papers/tpc-299-native-profile-budget-frontier/results/"
    "tpc299_certificate.json")
TPC300_CODE = ROOT / (
    "papers/tpc-300-native-budget-dual-certificate/code/"
    "tpc300_native_budget_dual_certificate.py")
TPC300_RESULT = ROOT / (
    "papers/tpc-300-native-budget-dual-certificate/results/"
    "tpc300_certificate.json")
RESULT = PROJECT / "results/tpc301_certificate.json"

UPSTREAM_CODE_SHA256 = (
    "94cb7f191378698de2f08157a475586864c59bba02621e447da98f5ffbbc7279")
UPSTREAM_RESULT_SHA256 = (
    "9be51f5bcb93e3a297a70e1c12985d52aee2b74e5e3fe4a64fbf7d5a054c559e")
TPC300_CODE_SHA256 = (
    "eb45a6c301b55ffb9816e84b55d73f46a52846b394f5677e80cabfb38f510e1e")
TPC300_RESULT_SHA256 = (
    "c07a45ecce710e98281556018f9976e7ba36b28efdb2582bdc3b72c5857acc71")

STATUS = (
    "PROVED_EXACT_FINITE_TOLERANCE_MONOTONICITY_AND_HOMOGENEITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_GAP_ROBUSTNESS_ATLAS")
SCHEMA = "TPC301_NATIVE_BUDGET_GAP_ROBUSTNESS_AUDIT_V1"
ROUND2_CLUE = (
    "EXTEND_TOLERANCE_AND_SOURCE_NORMALIZATION_AUDIT_TO_GROWING_SHELLS_"
    "AND_ARITHMETIC_L2_INTERFACE")
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
TAU_LABELS = ("0.25", "0.5", "0.75")
TAU_VALUES = {
    "0.25": mp.mpf("0.25"),
    "0.5": mp.mpf("0.5"),
    "0.75": mp.mpf("0.75"),
}
NORMALIZATION_NAMES = (
    "beta_norm_squared",
    "profile_trace_mean",
    "first_profile_norm_squared",
)
MP_DPS = 60
FRONTIER_STEPS = 180
FRONTIER_TOL = mp.mpf("1e-42")
FRONTIER_RESIDUAL_TOL = mp.mpf("1e-35")
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-17")
GAP_THRESHOLDS = ("2", "5", "10")
COMMON_BUDGET_FLOOR = mp.mpf("3e-5")

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc299_for_tpc301", UPSTREAM_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-299 upstream unavailable")
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
    return [mp.nstr(value - radius, 38), mp.nstr(value + radius, 38)]


def center(interval: list[str]) -> mp.mpf:
    need(isinstance(interval, list) and len(interval) == 2,
         "two-sided interval")
    return (mp.mpf(interval[0]) + mp.mpf(interval[1])) / 2


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def parent_lock() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    need(digest(UPSTREAM_CODE.read_bytes()) == UPSTREAM_CODE_SHA256,
         "TPC-299 code provenance")
    raw_upstream = UPSTREAM_RESULT.read_bytes()
    need(digest(raw_upstream) == UPSTREAM_RESULT_SHA256,
         "TPC-299 result provenance")
    upstream = json.loads(raw_upstream)
    need(raw_upstream == canonical(upstream), "TPC-299 canonicality")
    need(upstream.get("certificate_version") == 1 and
         upstream.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER"),
         "TPC-299 status")
    audit = upstream.get("payload", {}).get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("shell_edges") == 1380 and
         audit.get("profile_count") == len(PROFILE_CUTOFFS),
         "TPC-299 finite census")
    need(upstream["payload"]["profile_family"]["ordered_cutoffs"] ==
         list(PROFILE_CUTOFFS), "profile cutoff lock")

    need(digest(TPC300_CODE.read_bytes()) == TPC300_CODE_SHA256,
         "TPC-300 code provenance")
    raw_tpc300 = TPC300_RESULT.read_bytes()
    need(digest(raw_tpc300) == TPC300_RESULT_SHA256,
         "TPC-300 result provenance")
    tpc300 = json.loads(raw_tpc300)
    need(raw_tpc300 == canonical(tpc300), "TPC-300 canonicality")
    need(tpc300.get("certificate_version") == 1 and
         tpc300.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_NATIVE_BUDGET_DUALITY"),
         "TPC-300 status")
    t300_audit = tpc300.get("payload", {}).get("finite_audit", {})
    need(t300_audit.get("rows") == 18 and
         t300_audit.get("dual_witness_cases") == 72,
         "TPC-300 finite census")

    rows, _ = PARENT.load_rows()
    need(len(rows) == 18, "upstream row census")
    return rows, {
        "tpc299_code_sha256": UPSTREAM_CODE_SHA256,
        "tpc299_result_sha256": UPSTREAM_RESULT_SHA256,
        "tpc300_code_sha256": TPC300_CODE_SHA256,
        "tpc300_result_sha256": TPC300_RESULT_SHA256,
    }


def exact_matrices(source_row: dict[str, Any]) -> tuple[
        list[int], list[Fraction], list[list[Fraction]],
        list[list[Fraction]]]:
    scale = int(source_row["scale"])
    height = int(source_row["H"])
    q0 = int(source_row["Q"])
    cutoff = int(source_row["comparison_cutoff_z"])
    exponent = int(source_row["kernel_exponent"])
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = PARENT.shell_between(q0)
    columns = [PARENT.PARENT.PARENT.PARENT.physical_output(
        indices, beta, height, prime, exponent) for prime in shell]
    profiles = PARENT.source_profile_matrix(indices)
    profile_count = len(PROFILE_CUTOFFS)
    image = [[sum((columns[row][index] * profiles[index][column]
                   for index in range(len(indices))), Fraction(0))
              for column in range(profile_count)]
             for row in range(len(shell))]
    gram = [[sum((profiles[index][left] * profiles[index][right]
                  for index in range(len(indices))), Fraction(0))
             for right in range(profile_count)]
            for left in range(profile_count)]
    return shell, beta, image, gram


def mp_matrices(image: list[list[Fraction]],
                gram: list[list[Fraction]]) -> tuple[mp.matrix, mp.matrix]:
    V = mp.matrix([[as_mp(value) for value in row] for row in image])
    M = mp.matrix([[as_mp(value) for value in row] for row in gram])
    return V, M


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
    residual_squared = dot(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    return coefficients, residual_squared, source_squared


def budget_frontier(V: mp.matrix, M: mp.matrix, target: mp.matrix,
                    tau: mp.mpf) -> dict[str, mp.mpf]:
    target_norm_squared = dot(target)
    radius_squared = tau ** 2 * target_norm_squared
    _, ls_residual_squared, _ = least_squares(V, M, target)
    need(ls_residual_squared <= radius_squared + FRONTIER_TOL,
         "infeasible prefix")
    if radius_squared >= target_norm_squared:
        return {
            "rho": mp.mpf(0),
            "residual_squared": target_norm_squared,
            "source_squared": mp.mpf(0),
            "relative_rms": mp.mpf(1),
        }
    if abs(ls_residual_squared - radius_squared) <= FRONTIER_TOL:
        coefficients, residual_squared, source_squared = least_squares(
            V, M, target)
        return {
            "rho": mp.mpf(0),
            "residual_squared": residual_squared,
            "source_squared": source_squared,
            "relative_rms": mp.sqrt(residual_squared / target_norm_squared),
        }
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
    return {
        "rho": rho,
        "residual_squared": residual_squared,
        "source_squared": source_squared,
        "relative_rms": mp.sqrt(residual_squared / target_norm_squared),
    }


def normalizers(M: mp.matrix, k: int,
                beta_norm_squared: mp.mpf) -> dict[str, mp.mpf]:
    trace_mean = mp.fsum(M[index, index] for index in range(k)) / k
    first = M[0, 0]
    need(beta_norm_squared > 0 and trace_mean > 0 and first > 0,
         "positive normalizer")
    return {
        "beta_norm_squared": beta_norm_squared,
        "profile_trace_mean": trace_mean,
        "first_profile_norm_squared": first,
    }


def make_case(V: mp.matrix, M: mp.matrix, target: mp.matrix,
              tau: mp.mpf, k: int, cutoff: int,
              beta_norm_squared: mp.mpf) -> tuple[dict[str, Any], dict[str, Any]]:
    Vk = V[:, :k]
    Mk = M[:k, :k]
    raw = budget_frontier(Vk, Mk, target, tau)
    norms = normalizers(M, k, beta_norm_squared)
    ratios = {
        name: raw["source_squared"] / value
        for name, value in norms.items()
    }
    saved = {
        "k": k,
        "cutoff": cutoff,
        "relative_rms": enclosure(raw["relative_rms"]),
        "ridge_parameter_rho": enclosure(raw["rho"]),
        "source_budget": enclosure(raw["source_squared"]),
        "normalizers": {
            name: enclosure(value) for name, value in norms.items()
        },
        "budget_over_normalizer": {
            name: enclosure(value) for name, value in ratios.items()
        },
    }
    return saved, {
        "source_budget": raw["source_squared"],
        "ratios": ratios,
        "relative_rms": raw["relative_rms"],
    }


def case_gap(weighted: dict[str, mp.mpf],
             positive: dict[str, mp.mpf]) -> dict[str, mp.mpf]:
    return {
        name: weighted[name] / positive[name]
        for name in NORMALIZATION_NAMES
    }


def build_row(source_row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    mp.mp.dps = MP_DPS
    shell, beta, image, gram = exact_matrices(source_row)
    V, M = mp_matrices(image, gram)
    shell_size = len(shell)
    prefix_count = min(shell_size, len(PROFILE_CUTOFFS))
    beta_norm_squared = mp.fsum(as_mp(value) ** 2 for value in beta)
    labels = {
        "weighted": mp.matrix([
            mp.mpf(int(value)) for value in source_row["minimum_signed_label"]]),
        "positive": mp.matrix([mp.mpf(1) for _ in shell]),
    }
    for target in labels.values():
        need(dot(target) == shell_size,
             "signed target normalization lock")

    least_squares_rms: dict[str, list[list[str]]] = {}
    least_squares_raw: dict[str, list[mp.mpf]] = {}
    for name, target in labels.items():
        values = []
        raw_values = []
        for k in range(1, prefix_count + 1):
            _, residual_squared, _ = least_squares(
                V[:, :k], M[:k, :k], target)
            value = mp.sqrt(residual_squared / dot(target))
            raw_values.append(value)
            values.append(enclosure(value))
        least_squares_rms[name] = values
        least_squares_raw[name] = raw_values

    tolerance_records: dict[str, Any] = {}
    summaries: dict[str, Any] = {}
    normalization_invariance = 0
    prefix_order = 0
    full_monotone = 0
    for tau_label in TAU_LABELS:
        tau = TAU_VALUES[tau_label]
        threshold_k: dict[str, int] = {}
        for name in labels:
            found = next(
                (index + 1 for index, value in
                 enumerate(least_squares_raw[name])
                 if value <= tau), None)
            need(found is not None, "threshold prefix missing")
            threshold_k[name] = int(found)
        need(threshold_k["positive"] <= threshold_k["weighted"],
             "positive prefix should not exceed weighted prefix")
        prefix_order += 1
        contexts: dict[str, Any] = {}
        context_raw: dict[str, Any] = {}
        context_specs = {
            "common_weighted_prefix": {
                name: threshold_k["weighted"] for name in labels},
            "target_specific_prefix": threshold_k,
            "full_prefix": {name: prefix_count for name in labels},
        }
        for context, k_by_target in context_specs.items():
            saved_targets: dict[str, Any] = {}
            raw_targets: dict[str, Any] = {}
            k_values = set(k_by_target.values())
            for name, target in labels.items():
                k = int(k_by_target[name])
                saved, raw = make_case(
                    V, M, target, tau, k, PROFILE_CUTOFFS[k - 1],
                    beta_norm_squared)
                saved_targets[name] = saved
                raw_targets[name] = raw
            if context != "target_specific_prefix":
                need(len(k_values) == 1, "common context prefix")
            gaps = case_gap(
                raw_targets["weighted"]["ratios"],
                raw_targets["positive"]["ratios"])
            if context == "common_weighted_prefix":
                spread = max(gaps.values()) - min(gaps.values())
                need(spread < mp.mpf("1e-35"),
                     "normalization-invariant common gap")
                normalization_invariance += 1
            contexts[context] = {
                "k_by_target": {name: int(value)
                                for name, value in k_by_target.items()},
                "cutoff_by_target": {
                    name: PROFILE_CUTOFFS[int(k_by_target[name]) - 1]
                    for name in labels
                },
                "targets": saved_targets,
                "weighted_to_positive_gap": {
                    name: enclosure(value) for name, value in gaps.items()
                },
            }
            context_raw[context] = {
                "targets": raw_targets,
                "gaps": gaps,
            }
        tolerance_records[tau_label] = contexts
        full_targets = context_raw["full_prefix"]["targets"]
        # Fixed-prefix tolerance monotonicity is tested by retaining the
        # full prefix.  The threshold prefixes themselves vary with tau.
        summaries[tau_label] = {
            "threshold_k": threshold_k,
            "common_gap": context_raw["common_weighted_prefix"]["gaps"],
            "full_gap": context_raw["full_prefix"]["gaps"],
            "common_weighted_ratios":
                context_raw["common_weighted_prefix"]["targets"]["weighted"][
                    "ratios"],
            "full_source_budget": {
                name: full_targets[name]["source_budget"]
                for name in labels
            },
        }

    # The full-prefix source budget is nonincreasing as tau is relaxed.
    for name in labels:
        sequence = [summaries[label]["full_source_budget"][name]
                    for label in TAU_LABELS]
        need(sequence[0] + mp.mpf("1e-35") >= sequence[1] and
             sequence[1] + mp.mpf("1e-35") >= sequence[2],
             "tolerance monotonicity")
        full_monotone += 1

    row = {
        "axis": str(source_row["axis"]),
        "scale": int(source_row["scale"]),
        "H": int(source_row["H"]),
        "Q": int(source_row["Q"]),
        "comparison_cutoff_z": int(source_row["comparison_cutoff_z"]),
        "kernel_exponent": int(source_row["kernel_exponent"]),
        "shell": shell,
        "shell_cardinality": shell_size,
        "profile_cutoffs": list(PROFILE_CUTOFFS),
        "tested_prefix_count": prefix_count,
        "beta_norm_squared": enclosure(beta_norm_squared),
        "target_norm_squared": shell_size,
        "least_squares_rms": least_squares_rms,
        "tolerance_audits": {
            label: {
                "threshold_k": summaries[label]["threshold_k"],
                "contexts": tolerance_records[label]
            }
            for label in TAU_LABELS
        },
        "invariance_checks": {
            "common_prefix_gap_normalizations": normalization_invariance,
            "full_prefix_tolerance_monotonicity": full_monotone,
        },
    }
    return row, {
        "prefix_order": prefix_order,
        "normalization_invariance": normalization_invariance,
        "full_monotone": full_monotone,
        "summaries": summaries,
    }


def build_payload() -> dict[str, Any]:
    rows, locks = parent_lock()
    workers = min(len(rows), max(1, os.cpu_count() or 1))
    arguments = rows
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                completed = pool.map(build_row, arguments)
        except (AttributeError, OSError, RuntimeError):
            completed = [build_row(row) for row in arguments]
    else:
        completed = [build_row(row) for row in arguments]
    certificates = [item[0] for item in completed]
    summaries = [item[1] for item in completed]
    need(len(certificates) == 18, "row census")
    need(sum(len(row["shell"]) for row in certificates) == 219,
         "shell target census")
    need(all(row["tested_prefix_count"] == min(row["shell_cardinality"], 17)
             for row in certificates), "prefix census")
    need(sum(item["prefix_order"] for item in summaries) == 54,
         "prefix ordering census")
    need(sum(item["normalization_invariance"] for item in summaries) == 54,
         "normalization invariance census")
    need(sum(item["full_monotone"] for item in summaries) == 36,
         "tolerance monotonicity census")

    common_gap: dict[str, list[mp.mpf]] = {label: [] for label in TAU_LABELS}
    full_gap: dict[str, list[mp.mpf]] = {label: [] for label in TAU_LABELS}
    common_weighted: dict[str, list[mp.mpf]] = {
        name: [] for name in NORMALIZATION_NAMES}
    for item in summaries:
        for label in TAU_LABELS:
            common_gap[label].append(
                item["summaries"][label]["common_gap"]["beta_norm_squared"])
            full_gap[label].append(
                item["summaries"][label]["full_gap"]["beta_norm_squared"])
            for name in NORMALIZATION_NAMES:
                common_weighted[name].append(
                    item["summaries"][label]["common_weighted_ratios"][name])

    def gap_counts(values: list[mp.mpf]) -> dict[str, int]:
        return {
            threshold: sum(value > mp.mpf(threshold) for value in values)
            for threshold in GAP_THRESHOLDS
        }

    common_budget_floor_counts = {
        name: sum(value > COMMON_BUDGET_FLOOR
                  for value in common_weighted[name])
        for name in NORMALIZATION_NAMES
    }
    need(all(value == 54 for value in common_budget_floor_counts.values()),
         "common weighted budget floor")

    audit = {
        "rows": len(certificates),
        "shell_target_count": sum(len(row["shell"]) for row in certificates),
        "inherited_grid_edge_count": 1380,
        "profile_count": len(PROFILE_CUTOFFS),
        "tolerance_ladder": list(TAU_LABELS),
        "budget_cases": 18 * len(TAU_LABELS) * 3 * 2,
        "common_gap_min_by_tau": {
            label: enclosure(min(common_gap[label])) for label in TAU_LABELS
        },
        "common_gap_max_by_tau": {
            label: enclosure(max(common_gap[label])) for label in TAU_LABELS
        },
        "common_gap_above_threshold_by_tau": {
            label: gap_counts(common_gap[label]) for label in TAU_LABELS
        },
        "full_gap_min_by_tau": {
            label: enclosure(min(full_gap[label])) for label in TAU_LABELS
        },
        "full_gap_above_threshold_by_tau": {
            label: gap_counts(full_gap[label]) for label in TAU_LABELS
        },
        "common_weighted_budget_min_by_normalization": {
            name: enclosure(min(common_weighted[name]))
            for name in NORMALIZATION_NAMES
        },
        "common_weighted_budget_max_by_normalization": {
            name: enclosure(max(common_weighted[name]))
            for name in NORMALIZATION_NAMES
        },
        "common_weighted_budget_above_3e-5_by_normalization":
            common_budget_floor_counts,
        "prefix_order_cases": sum(item["prefix_order"] for item in summaries),
        "normalization_invariance_cases": sum(
            item["normalization_invariance"] for item in summaries),
        "full_tolerance_monotonicity_cases": sum(
            item["full_monotone"] for item in summaries),
        "fixed_power_credit": 0,
    }
    return {
        "schema": SCHEMA,
        "parent_lock": locks,
        "exact_theorem": {
            "budget_definition": (
                "B_(k,tau)(b)=min{c^T M_k c: "
                "||V_k c-b||_2<=tau||b||_2}"),
            "tolerance_monotonicity": (
                "tau_1<=tau_2 implies B_(k,tau_1)(b)>=B_(k,tau_2)(b) "
                "at every fixed feasible prefix"),
            "target_homogeneity": (
                "B_(k,tau)(alpha b)=alpha^2 B_(k,tau)(b) for alpha != 0"),
            "prefix_threshold_monotonicity": (
                "the first feasible prefix index k_tau(b) is nonincreasing "
                "as tau increases"),
            "normalization_invariance": (
                "at one common prefix, dividing both target budgets by any "
                "positive target-independent source normalizer preserves their gap"),
            "scope": "finite Euclidean target balls and positive-definite source Gram",
        },
        "audit_definition": {
            "target_classes": {
                "weighted": "TPC-299 minimum signed label",
                "positive": "all-one control",
            },
            "prefix_contexts": [
                "common_weighted_prefix",
                "target_specific_prefix",
                "full_prefix",
            ],
            "normalizations": {
                "beta_norm_squared": "||beta||_2^2",
                "profile_trace_mean": "tr(M_k)/k",
                "first_profile_norm_squared": "M_k[1,1]",
            },
            "tolerance": (
                "relative target RMS: ||V_kc-b||_2/||b||_2 <= tau"),
            "primary_comparison": (
                "weighted/positive budget gap at the common weighted prefix"),
            "secondary_comparison": (
                "target-specific and full-prefix contexts"),
                "finite_grid": (
                    "18 rows, 219 explicit shell targets, inherited 1,380-edge grid, "
                    "17 literal cutoffs"),
        },
        "finite_audit": audit,
        "claim_firewall": {
            "finite_tolerance_monotonicity": True,
            "finite_target_homogeneity": True,
            "finite_normalization_gap_invariance": True,
            "finite_gap_robustness_atlas": True,
            "growing_profile_budget_theorem": False,
            "arithmetic_L2": False,
            "full_gate_B": False,
            "twin_prime_result": False,
        },
        "rows": certificates,
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
    need(audit.get("rows") == 18 and
         audit.get("shell_target_count") == 219 and
         audit.get("inherited_grid_edge_count") == 1380 and
         audit.get("profile_count") == 17 and
         audit.get("tolerance_ladder") == list(TAU_LABELS) and
         audit.get("budget_cases") == 324,
         "finite audit census")
    need(audit.get("prefix_order_cases") == 54 and
         audit.get("normalization_invariance_cases") == 54 and
         audit.get("full_tolerance_monotonicity_cases") == 36 and
         audit.get("common_weighted_budget_above_3e-5_by_normalization") ==
         {name: 54 for name in NORMALIZATION_NAMES} and
         audit.get("fixed_power_credit") == 0,
         "finite theorem census")
    need(set(payload.get("rows", [{}])[0].get("tolerance_audits", {})) ==
         set(TAU_LABELS), "tolerance records")
    need(len(payload.get("rows", [])) == 18, "row payload")


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
        print("TPC301_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    audit = document["payload"]["finite_audit"]
    print("TPC301_CERTIFICATE=PASS rows=18 shell_targets=219 "
          "inherited_grid_edges=1380 taus=3 "
          "common_gap_min_025=" +
          audit["common_gap_min_by_tau"]["0.25"][0] +
          " common_gap_min_050=" +
          audit["common_gap_min_by_tau"]["0.5"][0] +
          " common_gap_min_075=" +
          audit["common_gap_min_by_tau"]["0.75"][0] +
          " fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
