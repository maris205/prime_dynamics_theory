#!/usr/bin/env python3
"""Counterfactual native budgets for transported TPC-304 labels.

TPC-304 localized a low-overlap label fracture but could not say whether the
label change or the physical shell change drives the budget descent.  TPC-305
keeps each full physical shell/operator fixed, swaps only the labels on its
overlap with the neighboring shell, and recomputes the constrained native
profile budget.  The experiment is deliberately finite and reports a partial
target/operator separation, not a causal or asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp

getcontext().prec = 80
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
TPC302_CODE = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/code/"
    "tpc302_growing_shell_budget_gap_audit.py")
TPC302_RESULT = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/results/"
    "tpc302_certificate.json")
TPC303_CODE = ROOT / (
    "papers/tpc-303-cardinality-monotonicity-obstruction/code/"
    "tpc303_cardinality_monotonicity_obstruction.py")
TPC303_RESULT = ROOT / (
    "papers/tpc-303-cardinality-monotonicity-obstruction/results/"
    "tpc303_certificate.json")
RESULT = PROJECT / "results/tpc305_certificate.json"

TPC302_CODE_SHA256 = (
    "1edd94f87af501e59ddaa07a6f2c9a5d458d7cb28e0623064f51bfb3d10ae517")
TPC302_RESULT_SHA256 = (
    "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6")
TPC303_CODE_SHA256 = (
    "8f6112aa89899dfd5f6f5fdd90307ed9bf56ab2264d66158b064d76623b21c4c")
TPC303_RESULT_SHA256 = (
    "4d282a8a32ac1e916ac328a2579bb25744d8a00cfca4911f14b908387391255a")

TPC302_STATUS = (
    "PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION_AND_BUDGET_"
    "MONOTONICITY_PLUS_NUMERICALLY_CERTIFIED_GROWING_GRID_AUDIT")
TPC303_STATUS = (
    "PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_"
    "FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION")
STATUS = (
    "PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_"
    "NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS")
SCHEMA = "TPC305_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGET_V1"
ROUND2_CLUE = (
    "TEST_TWO_WAY_OPERATOR_HOLDOUT_AND_INTERACTION_TERM_BEFORE_ANY_"
    "CAUSAL_TARGET_OPERATOR_CLAIM")

Q_SPINE = (50, 60, 70, 90)
ADJACENT_PAIRS = tuple(zip(Q_SPINE[:-1], Q_SPINE[1:]))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)

# The finite frontier is recomputed at high precision.  The explicit output
# enclosure is wider than the bisection/linear-solve error at this setting.
MP_DPS = 55
FRONTIER_STEPS = 130
FRONTIER_TOL = mp.mpf("1e-30")
FRONTIER_RESIDUAL_TOL = mp.mpf("1e-18")
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-11")
THRESHOLD_TOL = mp.mpf("1e-25")

spec = importlib.util.spec_from_file_location(
    "frozen_tpc302_for_tpc305", TPC302_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-302 parent unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)
PARENT.MP_DPS = MP_DPS
PARENT.FRONTIER_STEPS = FRONTIER_STEPS
PARENT.FRONTIER_TOL = FRONTIER_TOL
PARENT.FRONTIER_RESIDUAL_TOL = FRONTIER_RESIDUAL_TOL
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


def interval(value: object) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def ratio_interval(numerator: list[str], denominator: list[str]) -> list[str]:
    nlo, nhi = interval(numerator)
    dlo, dhi = interval(denominator)
    need(dlo > 0, "positive ratio denominator")
    return [mp.nstr(nlo / dhi, 38), mp.nstr(nhi / dlo, 38)]


def order_status(value: list[str]) -> str:
    lo, hi = interval(value)
    if hi < 1:
        return "BELOW_ONE_CERTIFIED"
    if lo > 1:
        return "ABOVE_ONE_CERTIFIED"
    return "ONE_INTERVAL_UNRESOLVED"


def locked_json(path: Path, expected_hash: str, expected_status: str,
                expected_schema: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " provenance")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == expected_status,
         path.name + " status")
    need(data.get("payload", {}).get("schema") == expected_schema,
         path.name + " schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def parent_data() -> tuple[dict[str, Any], dict[str, Any]]:
    need(digest(TPC302_CODE.read_bytes()) == TPC302_CODE_SHA256,
         "TPC-302 code provenance")
    need(digest(TPC303_CODE.read_bytes()) == TPC303_CODE_SHA256,
         "TPC-303 code provenance")
    data302 = locked_json(
        TPC302_RESULT, TPC302_RESULT_SHA256, TPC302_STATUS,
        "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1")
    data303 = locked_json(
        TPC303_RESULT, TPC303_RESULT_SHA256, TPC303_STATUS,
        "TPC303_CARDINALITY_MONOTONICITY_OBSTRUCTION_V1")
    need(data302["payload"]["finite_audit"]["rows"] == 34 and
         data302["payload"]["finite_audit"]["explicit_shell_target_count"] == 430,
         "TPC-302 census")
    need(data303["payload"]["finite_audit"]["series"] == 18 and
         data303["payload"]["finite_audit"]["adjacent_transitions"] == 54,
         "TPC-303 census")
    return data302, data303


def fixed_rows(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    rows: dict[tuple[int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512 and
                row.get("H") == 58 and row.get("comparison_cutoff_z") == 5 and
                row.get("Q") in Q_SPINE and
                row.get("kernel_exponent") in EXPONENTS):
            key = (int(row["Q"]), int(row["kernel_exponent"]))
            need(key not in rows, "duplicate fixed row")
            shell = row["shell"]
            labels = row["weighted_target_label"]
            need(shell == sorted(shell) and len(shell) == len(labels) and
                 all(label in (-1, 1) for label in labels),
                 "fixed row labels")
            rows[key] = row
    need(len(rows) == 8, "fixed-row census")
    return rows


def budget_census(
        data: dict[str, Any]
        ) -> dict[tuple[int, int, int, str], dict[str, Any]]:
    answer: dict[tuple[int, int, int, str], dict[str, Any]] = {}
    for series in data["payload"]["series"]:
        exponent = int(series["kernel_exponent"])
        tau = series["tau"]
        normalizer = series["normalizer"]
        for left_q, right_q in ADJACENT_PAIRS:
            hits = [item for item in series["transitions"]
                    if item["from_Q"] == left_q and item["to_Q"] == right_q]
            need(len(hits) == 1, "parent transition lookup")
            # Keep the exponent in the key: the same-prefix obstruction is
            # a case-level fact, and aggregating the two exponents would make
            # an `any(...)` query falsely transfer one exponent's prefix to
            # the other.
            key = (left_q, right_q, exponent, tau)
            item = answer.setdefault(key, {"by_normalizer": []})
            item["by_normalizer"].append({
                "normalizer": normalizer,
                "classification": hits[0]["classification"],
                "same_prefix": bool(hits[0]["same_prefix"]),
            })
    for key, item in answer.items():
        entries = item["by_normalizer"]
        # Each exponent/tolerance case has one entry per normalizer.
        need(len(entries) == 3 and
             {item["normalizer"] for item in entries} == set(NORMALIZERS),
             "parent exponent/tolerance census")
        desc = sum(x["classification"] == "DESCENT_CERTIFIED" for x in entries)
        asc = sum(x["classification"] == "ASCENT_CERTIFIED" for x in entries)
        unresolved = len(entries) - desc - asc
        same = sum(x["classification"] == "DESCENT_CERTIFIED" and
                   x["same_prefix"] for x in entries)
        item.update({"descents": desc, "ascents": asc,
                     "unresolved": unresolved,
                     "same_prefix_descents": same})
    need(len(answer) == 18, "parent exponent/tolerance case census")
    return answer


def source_and_profiles() -> tuple[list[int], list[Fraction], list[list[Fraction]], mp.matrix, mp.mpf]:
    indices, beta, _ = ENGINE.source_weights(512, 5)
    profiles = PARENT.source_profile_matrix(indices)
    profile_gram = [[sum((profiles[u][i] * profiles[u][j]
                           for u in range(len(indices))), Fraction(0))
                     for j in range(len(PROFILE_CUTOFFS))]
                    for i in range(len(PROFILE_CUTOFFS))]
    matrix = mp.matrix([[as_mp(value) for value in row]
                        for row in profile_gram])
    beta_norm_squared = mp.fsum(as_mp(value) ** 2 for value in beta)
    return indices, beta, profiles, matrix, beta_norm_squared


def physical_image(indices: list[int], beta: list[Fraction],
                   profiles: list[list[Fraction]], shell: list[int],
                   exponent: int) -> mp.matrix:
    outputs, _ = PARENT.physical_gram(indices, beta, 58, shell, exponent)
    image = [[sum((outputs[i][u] * profiles[u][j]
                   for u in range(len(indices))), Fraction(0))
              for j in range(len(PROFILE_CUTOFFS))]
             for i in range(len(shell))]
    return mp.matrix([[as_mp(value) for value in row] for row in image])


def feasible_prefix(V: mp.matrix, M: mp.matrix, target: list[int],
                    tau: str) -> int:
    vector = mp.matrix([mp.mpf(value) for value in target])
    target_norm = PARENT.dot(vector)
    for k in range(1, min(V.rows, V.cols) + 1):
        _, residual, _ = PARENT.least_squares(
            V[:, :k], M[:k, :k], vector)
        if mp.sqrt(residual / target_norm) <= mp.mpf(tau) + THRESHOLD_TOL:
            return k
    raise CheckFailure("no feasible counterfactual prefix")


def budget_record(V: mp.matrix, M: mp.matrix, native: list[int],
                  transported: list[int], tau: str,
                  beta_norm_squared: mp.mpf,
                  shell: list[int], operator_name: str) -> dict[str, Any]:
    native_k = feasible_prefix(V, M, native, tau)
    transported_k = feasible_prefix(V, M, transported, tau)
    k = max(native_k, transported_k)
    native_vector = mp.matrix([mp.mpf(value) for value in native])
    transported_vector = mp.matrix([mp.mpf(value) for value in transported])
    native_raw = PARENT.budget_frontier(
        V[:, :k], M[:k, :k], native_vector, mp.mpf(tau))
    transported_raw = PARENT.budget_frontier(
        V[:, :k], M[:k, :k], transported_vector, mp.mpf(tau))
    normalizers = PARENT.normalizers(M, k, beta_norm_squared)
    native_budget = {
        name: enclosure(native_raw["source_squared"] / value)
        for name, value in normalizers.items()}
    transported_budget = {
        name: enclosure(transported_raw["source_squared"] / value)
        for name, value in normalizers.items()}
    ratios = {name: ratio_interval(transported_budget[name], native_budget[name])
              for name in NORMALIZERS}
    statuses = {name: order_status(ratios[name]) for name in NORMALIZERS}
    need(len(set(statuses.values())) == 1,
         "normalizer-invariant target effect")
    return {
        "operator": operator_name,
        "shell": shell,
        "shell_cardinality": len(shell),
        "native_threshold_k": native_k,
        "transported_threshold_k": transported_k,
        "comparison_prefix_k": k,
        "comparison_cutoff": PROFILE_CUTOFFS[k - 1],
        "native_budget_over_normalizer": native_budget,
        "transported_budget_over_normalizer": transported_budget,
        "transported_over_native_interval": ratios,
        "transported_over_native_status": statuses,
    }


def orientation(left_status: str, right_status: str) -> str:
    if (left_status == "BELOW_ONE_CERTIFIED" and
            right_status == "ABOVE_ONE_CERTIFIED"):
        return "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    if (left_status == "ABOVE_ONE_CERTIFIED" and
            right_status == "BELOW_ONE_CERTIFIED"):
        return "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    if (left_status == "ABOVE_ONE_CERTIFIED" and
            right_status == "ABOVE_ONE_CERTIFIED"):
        return "HOME_OPERATOR_FAVORED"
    if (left_status == "BELOW_ONE_CERTIFIED" and
            right_status == "BELOW_ONE_CERTIFIED"):
        return "CROSS_TARGET_FAVORED"
    return "ORIENTATION_UNRESOLVED"


def build_case(
        rows: dict[tuple[int, int], dict[str, Any]],
        budget: dict[tuple[int, int, int, str], dict[str, Any]],
               indices: list[int], beta: list[Fraction],
               profiles: list[list[Fraction]], M: mp.matrix,
               beta_norm_squared: mp.mpf, left_q: int, right_q: int,
               exponent: int, tau: str,
               image_cache: dict[tuple[tuple[int, ...], int], mp.matrix]
               ) -> dict[str, Any]:
    left = rows[(left_q, exponent)]
    right = rows[(right_q, exponent)]
    left_map = dict(zip(left["shell"], left["weighted_target_label"]))
    right_map = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(left_map) & set(right_map))
    need(bool(overlap), "nonempty shell overlap")
    raw_inner = sum(left_map[p] * right_map[p] for p in overlap)
    align_sign = 1 if raw_inner >= 0 else -1
    transported_left = [
        align_sign * right_map[p] if p in right_map else left_map[p]
        for p in left["shell"]]
    transported_right = [
        align_sign * left_map[p] if p in left_map else right_map[p]
        for p in right["shell"]]
    left_key = (tuple(left["shell"]), exponent)
    right_key = (tuple(right["shell"]), exponent)
    if left_key not in image_cache:
        image_cache[left_key] = physical_image(
            indices, beta, profiles, left["shell"], exponent)
    if right_key not in image_cache:
        image_cache[right_key] = physical_image(
            indices, beta, profiles, right["shell"], exponent)
    left_record = budget_record(
        image_cache[left_key], M, left["weighted_target_label"],
        transported_left, tau, beta_norm_squared, left["shell"], "left")
    right_record = budget_record(
        image_cache[right_key], M, right["weighted_target_label"],
        transported_right, tau, beta_norm_squared, right["shell"], "right")
    statuses_left = left_record["transported_over_native_status"]
    statuses_right = right_record["transported_over_native_status"]
    orientation_by_normalizer = {
        name: orientation(statuses_left[name], statuses_right[name])
        for name in NORMALIZERS}
    need(len(set(orientation_by_normalizer.values())) == 1,
         "normalizer-invariant orientation")
    parent_case = budget[(left_q, right_q, exponent, tau)]
    # Retain the exact exponent/tolerance case-level entries so a reader can
    # see how the counterfactual aligns with the parent transition.
    parent_entries = [item for item in parent_case["by_normalizer"]
                      if item["normalizer"] in NORMALIZERS]
    need(len(parent_entries) == 3, "parent case entries")
    return {
        "from_Q": left_q,
        "to_Q": right_q,
        "kernel_exponent": exponent,
        "tau": tau,
        "overlap_primes": overlap,
        "overlap_cardinality": len(overlap),
        "raw_overlap_inner_product": raw_inner,
        "optimal_alignment_sign": align_sign,
        "native_left_label": left["weighted_target_label"],
        "native_right_label": right["weighted_target_label"],
        "transported_left_label": transported_left,
        "transported_right_label": transported_right,
        "left_operator": left_record,
        "right_operator": right_record,
        "target_orientation_by_normalizer": orientation_by_normalizer,
        "target_orientation": next(iter(orientation_by_normalizer.values())),
        "parent_budget_case_census": parent_case,
    }


def build_payload() -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    data302, data303 = parent_data()
    rows = fixed_rows(data302)
    budget = budget_census(data303)
    indices, beta, profiles, M, beta_norm_squared = source_and_profiles()
    image_cache: dict[tuple[tuple[int, ...], int], mp.matrix] = {}
    cases = []
    for exponent in EXPONENTS:
        for left_q, right_q in ADJACENT_PAIRS:
            for tau in TAUS:
                cases.append(build_case(
                    rows, budget, indices, beta, profiles, M,
                    beta_norm_squared, left_q, right_q, exponent, tau,
                    image_cache))
    need(len(cases) == 18, "counterfactual case census")
    by_pair: list[dict[str, Any]] = []
    for left_q, right_q in ADJACENT_PAIRS:
        subset = [case for case in cases
                  if case["from_Q"] == left_q and case["to_Q"] == right_q]
        need(len(subset) == 6, "pair case census")
        counts = {name: sum(case["target_orientation"] == name
                             for case in subset)
                  for name in (
                      "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
                      "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS",
                      "HOME_OPERATOR_FAVORED", "CROSS_TARGET_FAVORED",
                      "ORIENTATION_UNRESOLVED")}
        parent_descents = [
            sum(case["parent_budget_case_census"]["descents"]
                for case in subset if case["tau"] == tau)
            for tau in TAUS]
        same_prefix_cases = [case for case in subset
                             if case["parent_budget_case_census"][
                                    "same_prefix_descents"] > 0]
        by_pair.append({
            "from_Q": left_q,
            "to_Q": right_q,
            "case_count": len(subset),
            "orientation_counts": counts,
            "same_prefix_case_count": len(same_prefix_cases),
            "same_prefix_orientation_counts": {
                name: sum(case["target_orientation"] == name
                          for case in same_prefix_cases)
                for name in counts},
            "parent_budget_descents_by_tau": parent_descents,
        })
    middle = next(item for item in by_pair
                  if item["from_Q"] == 60 and item["to_Q"] == 70)
    need(middle["orientation_counts"][
        "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"] == 5 and
         middle["orientation_counts"]["HOME_OPERATOR_FAVORED"] == 1 and
         middle["same_prefix_case_count"] == 3 and
         middle["same_prefix_orientation_counts"][
             "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"] == 3,
         "middle target-switch census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc302_code_sha256": TPC302_CODE_SHA256,
            "tpc302_result_sha256": TPC302_RESULT_SHA256,
            "tpc303_code_sha256": TPC303_CODE_SHA256,
            "tpc303_result_sha256": TPC303_RESULT_SHA256,
            "tpc302_fixed_source_rows": 8,
            "tpc303_series": 18,
            "tpc303_adjacent_transitions": 54,
        },
        "audit_definition": {
            "source_scale": 512,
            "height": 58,
            "comparison_cutoff_z": 5,
            "Q_spine": list(Q_SPINE),
            "kernel_exponents": list(EXPONENTS),
            "tolerances": list(TAUS),
            "normalizers": list(NORMALIZERS),
            "transport_rule": (
                "replace overlap labels by the optimally globally aligned neighboring label; retain native labels off the overlap"),
            "comparison_rule": (
                "for each operator and tolerance use the maximum feasible prefix for native and transported targets"),
            "orientation_rule": (
                "compare transported/native budget ratios on left and right operators"),
        },
        "exact_theorem": {
            "fixed_operator_counterfactual": (
                "within each operator row, only the target label vector is changed"),
            "global_sign_invariance": (
                "a simultaneous global sign on a complete target leaves its budget unchanged"),
            "scope": (
                "finite full-shell target swap with native off-overlap extension; no causal or asymptotic inference"),
        },
        "cases": cases,
        "pair_summary": by_pair,
        "finite_audit": {
            "cases": 18,
            "operator_budget_tables": 36,
            "pair_groups": 3,
            "middle_pair": [60, 70],
            "middle_right_label_cheaper_cases": 5,
            "middle_cases": 6,
            "middle_same_prefix_cases": 3,
            "middle_same_prefix_right_label_cheaper_cases": 3,
            "orientation_counts_by_pair": [
                item["orientation_counts"] for item in by_pair],
            "causal_target_operator_separation": "PARTIAL_COUNTERFACTUAL_ONLY",
            "uniform_asymptotic_budget_theorem": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
        },
        "firewall": {
            "TPC305_FIXED_OPERATOR_TARGET_SWAP": "PROVED_EXACT_FINITE_PROTOCOL",
            "TPC305_COUNTERFACTUAL_BUDGET_ATLAS": "NUMERICALLY_CERTIFIED_FINITE_18_CASES_36_OPERATOR_TABLES",
            "TPC305_MIDDLE_TARGET_ORIENTATION": "NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_5_OF_6",
            "TPC305_MIDDLE_SAME_PREFIX_ORIENTATION": "NUMERICALLY_CERTIFIED_FINITE_RIGHT_LABEL_CHEAPER_3_OF_3",
            "TPC305_CAUSAL_SEPARATION": "PARTIAL_COUNTERFACTUAL_ONLY",
            "TPC305_OPERATOR_INTERACTION_TERM": "OPEN",
            "TPC305_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC305_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC305_FIXED_POWER_CREDIT": 0,
            "TPC305_FULL_GATE_B": "OPEN",
            "TPC305_TWIN_PRIME_RESULT": "NONE",
            "TPC305_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))
    print("TPC305_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["cases"] == 18 and
         audit["operator_budget_tables"] == 36 and
         audit["middle_right_label_cheaper_cases"] == 5 and
         audit["middle_same_prefix_right_label_cheaper_cases"] == 3 and
         audit["fixed_power_credit"] == 0,
         "finite audit")
    print("TPC305_CERTIFICATE=PASS cases=18 operator_tables=36 "
          "middle_right_label_cheaper=5/6 middle_same_prefix=3/3")


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
    except (CheckFailure, OSError, json.JSONDecodeError) as error:
        print("TPC305_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
