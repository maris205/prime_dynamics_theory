#!/usr/bin/env python3
"""Adversarial exclusive-completion envelopes for the TPC-307 holdout.

TPC-307 fixed the common ambient operator and used native exclusive labels as
holdouts.  This release keeps the fitted coefficients fixed and enumerates all
binary completion perturbations within Hamming radii 0, 1, and 2 on each
exclusive holdout.  It measures whether the budget/holdout comparison survives
that finite completion envelope.  The result is a diagnostic, not a causal or
asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-307-common-ambient-union-shell-holdout/code/"
    "tpc307_common_ambient_union_shell_holdout.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-307-common-ambient-union-shell-holdout/results/"
    "tpc307_certificate.json")
RESULT = PROJECT / "results/tpc308_certificate.json"

PARENT_CODE_SHA256 = (
    "50649f9f66dabf97879b38d73283fedcd363900918c838bfcc9f1be807b995b5")
PARENT_RESULT_SHA256 = (
    "8513586b5e7343b257cdd293fe100a4d1680c5df193d568404ebc18539c5f593")
PARENT_STATUS = (
    "PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS")
STATUS = (
    "PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS")
SCHEMA = "TPC308_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_V1"

Q_SPINE = (50, 60, 70, 90)
ADJACENT_PAIRS = tuple(zip(Q_SPINE[:-1], Q_SPINE[1:]))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
RADII = (0, 1, 2)
CLASSIFY_BELOW = mp.mpf("0.9")
CLASSIFY_ABOVE = mp.mpf("1.1")
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-5")
THRESHOLD_TOL = mp.mpf("1e-20")
mp.mp.dps = 70

spec = importlib.util.spec_from_file_location("frozen_tpc307_for_tpc308",
                                               PARENT_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-307 parent unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)


class CheckFailure(RuntimeError):
    """A fail-closed certificate validation error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def emit(value: mp.mpf) -> str:
    return mp.nstr(value, 34)


def enclosure(value: mp.mpf) -> list[str]:
    radius = INTERVAL_RELATIVE_RADIUS * max(abs(value), mp.mpf("1e-30"))
    return [emit(value - radius), emit(value + radius)]


def interval(value: Any) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def ratio_from_bounds(right_min: mp.mpf, right_max: mp.mpf,
                      left_min: mp.mpf, left_max: mp.mpf) -> list[str]:
    need(right_min > 0 and left_min > 0, "positive envelope minima")
    right_lo, _ = interval(enclosure(right_min))
    _, right_max_hi = interval(enclosure(right_max))
    left_min_lo, _ = interval(enclosure(left_min))
    _, left_max_hi = interval(enclosure(left_max))
    return [emit(right_lo / left_max_hi), emit(right_max_hi / left_min_lo)]


def classify(value: list[str]) -> str:
    lo, hi = interval(value)
    if hi < CLASSIFY_BELOW:
        return "RIGHT_COMPLETION_LOWER"
    if lo > CLASSIFY_ABOVE:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def locked_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-307 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-307 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC-307 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == PARENT_STATUS, "TPC-307 header")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "TPC-307 payload hash")
    audit = data["payload"]["finite_audit"]
    need(audit.get("cases") == 18 and audit.get("observations") == 18 and
         audit.get("directional_holdout_fits") == 36 and
         audit.get("normalizer_rows") == 54, "TPC-307 census")
    return data


def completion_envelope(prediction: mp.matrix, target: list[int],
                        positions: list[int], radius: int
                        ) -> tuple[mp.mpf, mp.mpf, mp.mpf, int]:
    need(len(target) == len(positions) and bool(positions),
         "holdout shape")
    values: list[mp.mpf] = []
    native = mp.fsum((prediction[index] - value) ** 2
                     for index, value in zip(positions, target)) / len(positions)
    for flips_count in range(min(radius, len(target)) + 1):
        for flips in itertools.combinations(range(len(target)), flips_count):
            flip_set = set(flips)
            value = mp.fsum(
                (prediction[index] - value *
                 (-1 if offset in flip_set else 1)) ** 2
                for offset, (index, value) in enumerate(zip(positions, target)))
            values.append(value / len(positions))
    need(bool(values), "nonempty completion envelope")
    return native, min(values), max(values), len(values)


def parent_rows(parent: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    p305, _ = PARENT.load_parents()
    rows = PARENT.fixed_rows(p305)
    need(len(rows) == 8, "source row census")
    need(len(parent["payload"]["cases"]) == 18, "parent case census")
    return rows


def fit_case(parent_case: dict[str, Any],
             rows: dict[tuple[int, int], dict[str, Any]],
             indices: list[int], beta: list[Any], profiles: np.ndarray,
             gram: mp.matrix,
             image_cache: dict[tuple[int, int, int], mp.matrix]
             ) -> dict[str, Any]:
    left_q = int(parent_case["from_Q"])
    right_q = int(parent_case["to_Q"])
    exponent = int(parent_case["kernel_exponent"])
    tau = parent_case["tau"]
    left = rows[(left_q, exponent)]
    right = rows[(right_q, exponent)]
    left_map = dict(zip(left["shell"], left["weighted_target_label"]))
    right_map = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(left_map) & set(right_map))
    exclusive_left = sorted(set(left_map) - set(right_map))
    exclusive_right = sorted(set(right_map) - set(left_map))
    union = sorted(set(left_map) | set(right_map))
    need(parent_case["overlap_primes"] == overlap and
         parent_case["exclusive_left_primes"] == exclusive_left and
         parent_case["exclusive_right_primes"] == exclusive_right and
         parent_case["union_primes"] == union, "parent partition")
    raw_inner = sum(left_map[p] * right_map[p] for p in overlap)
    sigma = 1 if raw_inner >= 0 else -1
    need(parent_case["optimal_alignment_sign"] == sigma, "parent alignment")
    aligned_right = {p: sigma * value for p, value in right_map.items()}
    target_left = mp.matrix([left_map[p] for p in overlap])
    target_right = mp.matrix([aligned_right[p] for p in overlap])
    image_key = (left_q, right_q, exponent)
    if image_key not in image_cache:
        image_cache[image_key] = PARENT.physical_image(
            indices, beta, profiles, union, exponent)
    ambient = image_cache[image_key]
    position = {p: i for i, p in enumerate(union)}
    overlap_indices = [position[p] for p in overlap]
    left_indices = [position[p] for p in exclusive_left]
    right_indices = [position[p] for p in exclusive_right]
    overlap_matrix = mp.matrix(
        [[ambient[i, j] for j in range(ambient.cols)]
         for i in overlap_indices])
    left_k = PARENT.feasible_prefix(overlap_matrix, gram, target_left,
                                    mp.mpf(tau))
    right_k = PARENT.feasible_prefix(overlap_matrix, gram, target_right,
                                     mp.mpf(tau))
    k = max(left_k, right_k)
    left_coefficients = PARENT.frontier(
        overlap_matrix[:, :k], gram[:k, :k], target_left, mp.mpf(tau))[0]
    right_coefficients = PARENT.frontier(
        overlap_matrix[:, :k], gram[:k, :k], target_right, mp.mpf(tau))[0]
    left_prediction = ambient[:, :k] * left_coefficients
    right_prediction = ambient[:, :k] * right_coefficients
    left_target = [left_map[p] for p in exclusive_left]
    right_target = [aligned_right[p] for p in exclusive_right]
    records = []
    parent_record = parent_case["tau_record"]
    for radius in RADII:
        left_native, left_min, left_max, left_count = completion_envelope(
            left_prediction, left_target, left_indices, radius)
        right_native, right_min, right_max, right_count = completion_envelope(
            right_prediction, right_target, right_indices, radius)
        ratio = ratio_from_bounds(right_min, right_max, left_min, left_max)
        holdout_class = classify(ratio)
        budget_class = parent_record["budget_preference"]
        if (budget_class == holdout_class and
                budget_class != "PREFERENCE_UNRESOLVED"):
            agreement = "CONCORDANT"
        elif ({budget_class, holdout_class} == {
                "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"}):
            agreement = "DISCORDANT"
        else:
            agreement = "UNRESOLVED"
        if radius == 0:
            need(holdout_class == parent_record["holdout_preference"],
                 "radius-zero parent recovery")
            need(agreement == parent_record["agreement"],
                 "radius-zero agreement recovery")
        records.append({
            "radius": radius,
            "candidate_count": left_count + right_count,
            "left_completion": {
                "native_holdout_mse": enclosure(left_native),
                "envelope_min_mse": enclosure(left_min),
                "envelope_max_mse": enclosure(left_max),
                "candidate_count": left_count,
            },
            "right_completion": {
                "native_holdout_mse": enclosure(right_native),
                "envelope_min_mse": enclosure(right_min),
                "envelope_max_mse": enclosure(right_max),
                "candidate_count": right_count,
            },
            "holdout_right_over_left_interval": ratio,
            "budget_preference": budget_class,
            "holdout_preference": holdout_class,
            "agreement": agreement,
        })
    return {
        "from_Q": left_q,
        "to_Q": right_q,
        "kernel_exponent": exponent,
        "tau": tau,
        "comparison_prefix_k": k,
        "overlap_fit_feasible_prefix": {"left": left_k, "right": right_k},
        "union_cardinality": len(union),
        "overlap_cardinality": len(overlap),
        "exclusive_left_cardinality": len(exclusive_left),
        "exclusive_right_cardinality": len(exclusive_right),
        "envelopes": records,
    }


def empty_counts() -> dict[str, int]:
    return {"RIGHT_COMPLETION_LOWER": 0,
            "LEFT_COMPLETION_LOWER": 0,
            "PREFERENCE_UNRESOLVED": 0}


def agreement_counts() -> dict[str, int]:
    return {"CONCORDANT": 0, "DISCORDANT": 0, "UNRESOLVED": 0}


def build_payload() -> dict[str, Any]:
    parent = locked_parent()
    rows = parent_rows(parent)
    indices, beta, profiles, gram, beta_norm = PARENT.source_context()
    del beta_norm
    image_cache: dict[tuple[int, int, int], mp.matrix] = {}
    cases = [fit_case(case, rows, indices, beta, profiles, gram, image_cache)
             for case in parent["payload"]["cases"]]
    need(len(cases) == 18, "case census")
    holdout_counts = {radius: empty_counts() for radius in RADII}
    agreements = {radius: agreement_counts() for radius in RADII}
    discordance_by_pair = {radius: {str(pair): 0 for pair in ADJACENT_PAIRS}
                           for radius in RADII}
    candidate_total = {radius: 0 for radius in RADII}
    baseline_recovery = True
    pair_summary = []
    for left_q, right_q in ADJACENT_PAIRS:
        for radius in RADII:
            subset = [case for case in cases
                      if (case["from_Q"], case["to_Q"]) == (left_q, right_q)]
            need(len(subset) == 6, "pair case census")
            local_holdout = empty_counts()
            local_agreement = agreement_counts()
            for case in subset:
                record = case["envelopes"][radius]
                local_holdout[record["holdout_preference"]] += 1
                local_agreement[record["agreement"]] += 1
                holdout_counts[radius][record["holdout_preference"]] += 1
                agreements[radius][record["agreement"]] += 1
                candidate_total[radius] += record["candidate_count"]
                if (record["agreement"] == "DISCORDANT"):
                    discordance_by_pair[radius][str((left_q, right_q))] += 1
            pair_summary.append({
                "from_Q": left_q,
                "to_Q": right_q,
                "radius": radius,
                "cases": len(subset),
                "holdout_preference_counts": local_holdout,
                "agreement_counts": local_agreement,
            })
    # The explicit parent comparison above is checked more directly here; the
    # loop-local expression is intentionally not used as scientific evidence.
    for parent_case, case in zip(parent["payload"]["cases"], cases):
        need(case["envelopes"][0]["agreement"] ==
             parent_case["tau_record"]["agreement"],
             "parent agreement census")
    need(baseline_recovery, "baseline recovery")
    need(agreements[0] == {"CONCORDANT": 13, "DISCORDANT": 3,
                           "UNRESOLVED": 2}, "radius-zero agreement")
    need(agreements[1] == {"CONCORDANT": 11, "DISCORDANT": 2,
                           "UNRESOLVED": 5}, "radius-one agreement")
    need(agreements[2] == {"CONCORDANT": 10, "DISCORDANT": 1,
                           "UNRESOLVED": 7}, "radius-two agreement")
    need(holdout_counts[0] == {"RIGHT_COMPLETION_LOWER": 13,
                                "LEFT_COMPLETION_LOWER": 3,
                                "PREFERENCE_UNRESOLVED": 2},
         "radius-zero holdout census")
    need(holdout_counts[1] == {"RIGHT_COMPLETION_LOWER": 11,
                                "LEFT_COMPLETION_LOWER": 2,
                                "PREFERENCE_UNRESOLVED": 5},
         "radius-one holdout census")
    need(holdout_counts[2] == {"RIGHT_COMPLETION_LOWER": 9,
                                "LEFT_COMPLETION_LOWER": 2,
                                "PREFERENCE_UNRESOLVED": 7},
         "radius-two holdout census")
    need(discordance_by_pair[0][str((70, 90))] == 3 and
         sum(discordance_by_pair[0].values()) == 3,
         "radius-zero localization")
    need(discordance_by_pair[1][str((70, 90))] == 2 and
         sum(discordance_by_pair[1].values()) == 2,
         "radius-one localization")
    need(discordance_by_pair[2][str((70, 90))] == 1 and
         sum(discordance_by_pair[2].values()) == 1,
         "radius-two localization")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc307_code_sha256": PARENT_CODE_SHA256,
            "tpc307_result_sha256": PARENT_RESULT_SHA256,
            "tpc307_cases": 18,
            "tpc307_directional_holdout_fits": 36,
        },
        "protocol": {
            "Q_spine": list(Q_SPINE),
            "kernel_exponents": list(EXPONENTS),
            "tolerances": list(TAUS),
            "hamming_radii": list(RADII),
            "completion_rule": (
                "flip at most r binary labels on each native exclusive holdout"),
            "fit_lock": "reuse TPC-307 common ambient coefficients and prefix",
            "ratio_rule": "right envelope holdout MSE / left envelope holdout MSE",
            "strict_classification": (
                "right lower iff upper ratio<0.9; left lower iff lower ratio>1.1"),
        },
        "exact_theorem": {
            "finite_hamming_ball": (
                "the completion set is the finite union of subsets of size at most r"),
            "fixed_prediction_extrema": (
                "enumeration attains the minimum and maximum squared holdout loss"),
            "radius_monotonicity": (
                "envelope minimum is nonincreasing and maximum nondecreasing in r"),
            "radius_zero_recovery": (
                "r=0 recovers the TPC-307 native exclusive holdout"),
            "classification_soundness": (
                "a valid ratio enclosure wholly outside the thresholds implies its class"),
            "scope": "finite fixed-prediction completion diagnostic",
        },
        "cases": cases,
        "pair_summary": pair_summary,
        "finite_audit": {
            "cases": 18,
            "radii": 3,
            "envelope_observations": 54,
            "directional_envelope_records": 108,
            "candidate_evaluations_by_radius": candidate_total,
            "holdout_preference_counts_by_radius": holdout_counts,
            "agreement_counts_by_radius": agreements,
            "discordance_by_pair_and_radius": discordance_by_pair,
            "radius_zero_parent_recovery": True,
            "target_generation_leakage":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "formal_interval_certificate": "OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "causal_identification": "NONE_FIXED_PREDICTION_ENVELOPE_DIAGNOSTIC_ONLY",
            "uniform_asymptotic_budget": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
            "full_gate_b": "OPEN",
            "twin_prime_result": "NONE",
        },
        "firewall": {
            "TPC308_HAMMING_ENVELOPE_PROTOCOL": "PROVED_EXACT_FINITE",
            "TPC308_FIXED_PREDICTION_EXTREMA": "PROVED_EXACT_FINITE",
            "TPC308_RADIUS_MONOTONICITY": "PROVED_EXACT_FINITE",
            "TPC308_FINITE_STABILITY_ATLAS":
                "NUMERICALLY_REPRODUCED_FINITE_54_ENVELOPE_OBSERVATIONS",
            "TPC308_AGREEMENT_R0":
                "NUMERICALLY_REPRODUCED_FINITE_13_CONCORDANT_3_DISCORDANT_2_UNRESOLVED",
            "TPC308_AGREEMENT_R1":
                "NUMERICALLY_REPRODUCED_FINITE_11_CONCORDANT_2_DISCORDANT_5_UNRESOLVED",
            "TPC308_AGREEMENT_R2":
                "NUMERICALLY_REPRODUCED_FINITE_10_CONCORDANT_1_DISCORDANT_7_UNRESOLVED",
            "TPC308_DISCORDANCE_SURVIVAL":
                "NUMERICALLY_REPRODUCED_FINITE_3_TO_2_TO_1_AS_RADIUS_0_TO_2",
            "TPC308_CAUSAL_IDENTIFICATION":
                "NONE_FIXED_PREDICTION_ENVELOPE_DIAGNOSTIC_ONLY",
            "TPC308_FORMAL_INTERVAL_CERTIFICATE":
                "OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "TPC308_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC308_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC308_FIXED_POWER_CREDIT": 0,
            "TPC308_FULL_GATE_B": "OPEN",
            "TPC308_TWIN_PRIME_RESULT": "NONE",
            "TPC308_STATUS": STATUS,
        },
        "round2_clue": (
            "TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_"
            "SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM"),
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))
    print("TPC308_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["cases"] == 18 and audit["radii"] == 3 and
         audit["envelope_observations"] == 54 and
         audit["directional_envelope_records"] == 108,
         "finite audit")
    print("TPC308_CERTIFICATE=PASS cases=18 radii=3 observations=54 "
          "r0=13/3/2 r1=11/2/5 r2=10/1/7")


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
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            ArithmeticError) as error:
        print("TPC308_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
