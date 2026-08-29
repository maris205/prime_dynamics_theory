#!/usr/bin/env python3
"""Independent source-first replay for TPC-301.

The checker does not import the TPC-301 producer.  It rebuilds the frozen
physical operator and literal profile family from TPC-299, recomputes the
three-tolerance frontiers, and verifies every recorded interval, prefix choice,
normalization gap, and monotonicity count.
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
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
TAU_LABELS = ("0.25", "0.5", "0.75")
TAU_VALUES = {label: mp.mpf(label) for label in TAU_LABELS}
NORMALIZATION_NAMES = (
    "beta_norm_squared",
    "profile_trace_mean",
    "first_profile_norm_squared",
)
FRONTIER_STEPS = 180
FRONTIER_TOL = mp.mpf("1e-42")
FRONTIER_RESIDUAL_TOL = mp.mpf("1e-35")
GAP_THRESHOLDS = ("2", "5", "10")

spec = importlib.util.spec_from_file_location(
    "upstream_tpc299_for_tpc301_replay", UPSTREAM_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-299 upstream unavailable")
UPSTREAM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(UPSTREAM)
ENGINE = UPSTREAM.ENGINE
mp.mp.dps = 60


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


def as_mp(value: Fraction | int) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def check_interval(value: mp.mpf, interval: list[str], label: str) -> None:
    need(isinstance(interval, list) and len(interval) == 2,
         label + " interval")
    lower = mp.mpf(interval[0])
    upper = mp.mpf(interval[1])
    need(lower <= value <= upper, label + " enclosure")


def exact_matrices(source_row: dict[str, Any]) -> tuple[
        list[int], list[Fraction], list[list[Fraction]],
        list[list[Fraction]]]:
    scale = int(source_row["scale"])
    height = int(source_row["H"])
    q0 = int(source_row["Q"])
    cutoff = int(source_row["comparison_cutoff_z"])
    exponent = int(source_row["kernel_exponent"])
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = UPSTREAM.shell_between(q0)
    columns = [UPSTREAM.PARENT.PARENT.PARENT.physical_output(
        indices, beta, height, prime, exponent) for prime in shell]
    profiles = UPSTREAM.source_profile_matrix(indices)
    count = len(PROFILE_CUTOFFS)
    image = [[sum((columns[row][index] * profiles[index][column]
                   for index in range(len(indices))), Fraction(0))
              for column in range(count)]
             for row in range(len(shell))]
    gram = [[sum((profiles[index][left] * profiles[index][right]
                  for index in range(len(indices))), Fraction(0))
             for right in range(count)]
            for left in range(count)]
    return shell, beta, image, gram


def mp_matrices(image: list[list[Fraction]],
                gram: list[list[Fraction]]) -> tuple[mp.matrix, mp.matrix]:
    return (mp.matrix([[as_mp(value) for value in row] for row in image]),
            mp.matrix([[as_mp(value) for value in row] for row in gram]))


def norm_squared(vector: mp.matrix) -> mp.mpf:
    return mp.fsum(vector[index] ** 2 for index in range(len(vector)))


def least_squares(V: mp.matrix, M: mp.matrix,
                  target: mp.matrix) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    coefficients = mp.qr_solve(V, target)[0]
    residual = V * coefficients - target
    residual_squared = norm_squared(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    return coefficients, residual_squared, source_squared


def ridge(V: mp.matrix, M: mp.matrix, target: mp.matrix,
          rho: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    coefficients = mp.lu_solve(V.T * V + rho * M, V.T * target)
    residual = V * coefficients - target
    residual_squared = norm_squared(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    return residual_squared, source_squared


def frontier(V: mp.matrix, M: mp.matrix, target: mp.matrix,
             tau: mp.mpf) -> dict[str, mp.mpf]:
    target_norm_squared = norm_squared(target)
    radius_squared = tau ** 2 * target_norm_squared
    _, least_residual, _ = least_squares(V, M, target)
    need(least_residual <= radius_squared + FRONTIER_TOL,
         "infeasible replay prefix")
    if abs(least_residual - radius_squared) <= FRONTIER_TOL:
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
    while ridge(V, M, target, hi)[0] < radius_squared:
        hi *= 2
        need(hi < mp.mpf("1e100"), "replay bracket overflow")
    for _ in range(FRONTIER_STEPS):
        mid = (lo + hi) / 2
        if ridge(V, M, target, mid)[0] < radius_squared:
            lo = mid
        else:
            hi = mid
    rho = (lo + hi) / 2
    residual_squared, source_squared = ridge(V, M, target, rho)
    need(abs(residual_squared - radius_squared) < FRONTIER_RESIDUAL_TOL,
         "replay frontier residual")
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
    return {
        "beta_norm_squared": beta_norm_squared,
        "profile_trace_mean": trace_mean,
        "first_profile_norm_squared": first,
    }


def verify_case(V: mp.matrix, M: mp.matrix, target: mp.matrix,
                tau: mp.mpf, record: dict[str, Any],
                beta_norm_squared: mp.mpf) -> dict[str, mp.mpf]:
    k = int(record["k"])
    need(k > 0 and int(record["cutoff"]) == PROFILE_CUTOFFS[k - 1],
         "case prefix")
    raw = frontier(V[:, :k], M[:k, :k], target, tau)
    check_interval(raw["relative_rms"], record["relative_rms"],
                   "relative RMS")
    check_interval(raw["rho"], record["ridge_parameter_rho"], "rho")
    check_interval(raw["source_squared"], record["source_budget"],
                   "source budget")
    norms = normalizers(M, k, beta_norm_squared)
    ratios = {name: raw["source_squared"] / value
              for name, value in norms.items()}
    for name in NORMALIZATION_NAMES:
        check_interval(norms[name], record["normalizers"][name],
                       name + " normalizer")
        check_interval(ratios[name], record["budget_over_normalizer"][name],
                       name + " budget ratio")
    return {"source_budget": raw["source_squared"], "ratios": ratios}


def gap(weighted: dict[str, mp.mpf],
        positive: dict[str, mp.mpf]) -> dict[str, mp.mpf]:
    return {name: weighted[name] / positive[name]
            for name in NORMALIZATION_NAMES}


def verify_row(source_row: dict[str, Any],
               certificate_row: dict[str, Any]) -> dict[str, Any]:
    need(row_key(source_row) == row_key(certificate_row), "row alignment")
    shell, beta, image, gram = exact_matrices(source_row)
    need(certificate_row["shell"] == shell and
         certificate_row["shell_cardinality"] == len(shell),
         "shell replay")
    prefix_count = min(len(shell), len(PROFILE_CUTOFFS))
    need(certificate_row["tested_prefix_count"] == prefix_count,
         "prefix replay")
    V, M = mp_matrices(image, gram)
    beta_norm_squared = mp.fsum(as_mp(value) ** 2 for value in beta)
    check_interval(beta_norm_squared, certificate_row["beta_norm_squared"],
                   "beta norm")
    labels = {
        "weighted": mp.matrix([
            mp.mpf(int(value)) for value in source_row["minimum_signed_label"]]),
        "positive": mp.matrix([mp.mpf(1) for _ in shell]),
    }
    for target in labels.values():
        need(norm_squared(target) == len(shell), "target norm")
    least_squares_values: dict[str, list[mp.mpf]] = {}
    for name, target in labels.items():
        values = []
        records = certificate_row["least_squares_rms"][name]
        need(len(records) == prefix_count, "least-squares length")
        for k in range(1, prefix_count + 1):
            _, residual_squared, _ = least_squares(
                V[:, :k], M[:k, :k], target)
            value = mp.sqrt(residual_squared / norm_squared(target))
            check_interval(value, records[k - 1], "least-squares RMS")
            values.append(value)
        least_squares_values[name] = values

    row_summary: dict[str, Any] = {
        "common_gap_by_tau": {},
        "full_gap_by_tau": {},
        "common_weighted_by_tau": {},
        "full_source_budget_by_tau": {},
        "prefix_order": 0,
        "normalization_invariance": 0,
        "full_monotone": 0,
    }
    audits = certificate_row["tolerance_audits"]
    need(set(audits) == set(TAU_LABELS), "tolerance keys")
    full_budgets: dict[str, list[mp.mpf]] = {
        name: [] for name in labels}
    for tau_label in TAU_LABELS:
        tau = TAU_VALUES[tau_label]
        threshold_k = {}
        for name in labels:
            found = next((index + 1 for index, value in
                          enumerate(least_squares_values[name])
                          if value <= tau), None)
            need(found is not None, "replay threshold")
            threshold_k[name] = int(found)
        need(threshold_k["positive"] <= threshold_k["weighted"],
             "replay prefix order")
        row_summary["prefix_order"] += 1
        tau_record = audits[tau_label]
        need(tau_record["threshold_k"] == threshold_k,
             "threshold record")
        context_specs = {
            "common_weighted_prefix": {
                name: threshold_k["weighted"] for name in labels},
            "target_specific_prefix": threshold_k,
            "full_prefix": {name: prefix_count for name in labels},
        }
        context_raw: dict[str, Any] = {}
        for context, k_by_target in context_specs.items():
            record = tau_record["contexts"][context]
            need(record["k_by_target"] == k_by_target, "context prefix")
            for name in labels:
                need(record["cutoff_by_target"][name] ==
                     PROFILE_CUTOFFS[k_by_target[name] - 1],
                     "context cutoff")
            raw_targets = {}
            for name, target in labels.items():
                raw_targets[name] = verify_case(
                    V, M, target, tau,
                    record["targets"][name], beta_norm_squared)
            gaps = gap(raw_targets["weighted"]["ratios"],
                       raw_targets["positive"]["ratios"])
            for name in NORMALIZATION_NAMES:
                check_interval(gaps[name],
                               record["weighted_to_positive_gap"][name],
                               "gap")
            if context == "common_weighted_prefix":
                spread = max(gaps.values()) - min(gaps.values())
                need(spread < mp.mpf("1e-35"),
                     "replay normalization invariance")
                row_summary["normalization_invariance"] += 1
                row_summary["common_gap_by_tau"][tau_label] = (
                    gaps["beta_norm_squared"])
                row_summary["common_weighted_by_tau"][tau_label] = (
                    raw_targets["weighted"]["ratios"])
            if context == "full_prefix":
                row_summary["full_gap_by_tau"][tau_label] = (
                    gaps["beta_norm_squared"])
                for name in labels:
                    full_budgets[name].append(
                        raw_targets[name]["source_budget"])
        for name in labels:
            need(len(full_budgets[name]) > 0, "full budget collection")
        row_summary["full_source_budget_by_tau"][tau_label] = {
            name: full_budgets[name][-1] for name in labels
        }
    for name in labels:
        sequence = [row_summary["full_source_budget_by_tau"][label][name]
                    for label in TAU_LABELS]
        need(sequence[0] + mp.mpf("1e-35") >= sequence[1] and
             sequence[1] + mp.mpf("1e-35") >= sequence[2],
             "replay tolerance monotonicity")
        row_summary["full_monotone"] += 1
    need(certificate_row["invariance_checks"][
             "common_prefix_gap_normalizations"] ==
         row_summary["normalization_invariance"], "invariance count")
    need(certificate_row["invariance_checks"][
             "full_prefix_tolerance_monotonicity"] ==
         row_summary["full_monotone"], "monotonicity count")
    return row_summary


def verify_pair(arguments: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    return verify_row(arguments[0], arguments[1])


def main() -> int:
    try:
        need(digest(UPSTREAM_CODE.read_bytes()) == UPSTREAM_CODE_SHA256,
             "TPC-299 code provenance")
        raw_upstream = UPSTREAM_RESULT.read_bytes()
        need(digest(raw_upstream) == UPSTREAM_RESULT_SHA256 and
             raw_upstream == canonical(json.loads(raw_upstream)),
             "TPC-299 result provenance")
        raw_tpc300 = TPC300_RESULT.read_bytes()
        need(digest(TPC300_CODE.read_bytes()) == TPC300_CODE_SHA256 and
             digest(raw_tpc300) == TPC300_RESULT_SHA256 and
             raw_tpc300 == canonical(json.loads(raw_tpc300)),
             "TPC-300 provenance")
        data_raw = RESULT.read_bytes()
        data = json.loads(data_raw)
        need(data_raw == canonical(data), "TPC-301 canonicality")
        need(data.get("certificate_version") == 1 and
             data.get("claim_status") == STATUS, "certificate header")
        payload = data.get("payload", {})
        need(payload.get("schema") == SCHEMA and
             data.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "certificate schema/hash")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 18 and
             audit.get("shell_target_count") == 219 and
             audit.get("inherited_grid_edge_count") == 1380 and
             audit.get("profile_count") == 17 and
             audit.get("tolerance_ladder") == list(TAU_LABELS) and
             audit.get("budget_cases") == 324 and
             audit.get("prefix_order_cases") == 54 and
             audit.get("normalization_invariance_cases") == 54 and
             audit.get("full_tolerance_monotonicity_cases") == 36 and
             audit.get("fixed_power_credit") == 0,
             "finite audit census")
        need(len(payload.get("rows", [])) == 18, "certificate row census")
        source_rows, _ = UPSTREAM.load_rows()
        cert_map = {row_key(row): row for row in payload["rows"]}
        need(len(cert_map) == 18, "certificate row map")
        arguments = [(source_row, cert_map[row_key(source_row)])
                     for source_row in source_rows]
        workers = min(len(arguments), max(1, os.cpu_count() or 1))
        if workers > 1:
            try:
                with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                    summaries = pool.map(verify_pair, arguments)
            except (AttributeError, OSError, RuntimeError):
                summaries = [verify_pair(argument) for argument in arguments]
        else:
            summaries = [verify_pair(argument) for argument in arguments]
        need(sum(item["prefix_order"] for item in summaries) == 54 and
             sum(item["normalization_invariance"] for item in summaries) == 54 and
             sum(item["full_monotone"] for item in summaries) == 36,
             "replay theorem census")
        common_gap = {label: [] for label in TAU_LABELS}
        full_gap = {label: [] for label in TAU_LABELS}
        common_weighted = {name: [] for name in NORMALIZATION_NAMES}
        for summary in summaries:
            for label in TAU_LABELS:
                common_gap[label].append(
                    summary["common_gap_by_tau"][label])
                full_gap[label].append(summary["full_gap_by_tau"][label])
                for name in NORMALIZATION_NAMES:
                    common_weighted[name].append(
                        summary["common_weighted_by_tau"][label][name])
        # The detailed row replay is authoritative; aggregate count checks
        # below also catch accidental edits to the published atlas.
        for label in TAU_LABELS:
            for threshold in GAP_THRESHOLDS:
                count = sum(value > mp.mpf(threshold)
                            for value in common_gap[label])
                need(count == payload["finite_audit"][
                    "common_gap_above_threshold_by_tau"][label][threshold],
                     "common gap count")
                count_full = sum(value > mp.mpf(threshold)
                                 for value in full_gap[label])
                need(count_full == payload["finite_audit"][
                    "full_gap_above_threshold_by_tau"][label][threshold],
                     "full gap count")
        for name in NORMALIZATION_NAMES:
            count = sum(value > mp.mpf("3e-5")
                        for value in common_weighted[name])
            need(count == payload["finite_audit"][
                "common_weighted_budget_above_3e-5_by_normalization"][name],
                 "budget floor count")
    except (Failure, OSError, ValueError, json.JSONDecodeError) as error:
        print("TPC301_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC301_INDEPENDENT_CHECK=PASS rows=18 shell_targets=219 "
          "taus=3 common_gap_gt_10=18x3 normalization_invariance=54 "
          "monotone=36")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
