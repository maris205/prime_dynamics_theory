#!/usr/bin/env python3
"""TPC-309: a finite profile-prefix shift sensitivity atlas.

The TPC-308 common-ambient operator and its binary exclusive completions are
kept fixed.  The only changed object is the source-backed profile ladder: a
17-column ordered cutoff window is shifted one prime down, kept at the
TPC-308 baseline, or shifted one prime up.  Each ladder gets its own common
feasible prefix, frontier fit, budget ratio, and finite completion envelope.

This is a finite model-selection sensitivity experiment.  It is deliberately
not an arithmetic, causal, asymptotic, or twin-prime theorem.
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
    "papers/tpc-308-adversarial-exclusive-completion-envelope/code/"
    "tpc308_adversarial_exclusive_completion_envelope.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-308-adversarial-exclusive-completion-envelope/results/"
    "tpc308_certificate.json")
RESULT = PROJECT / "results/tpc309_certificate.json"

PARENT_CODE_SHA256 = (
    "08a5058cc2229b2fde2af6d1ee79ed7b7857270dfede5a0109a53364dbfac35c")
PARENT_RESULT_SHA256 = (
    "b25f9317f26dc85231c9315bb87c1343b316c2afa760a0e00798d37da1541453")
PARENT_STATUS = (
    "PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS")
STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS")
SCHEMA = "TPC309_THREE_WINDOW_PROFILE_PREFIX_SHIFT_AUDIT_V1"
ROUND2_CLUE = (
    "TEST_CROSS_HOLDOUT_AGGREGATION_AND_PROFILE_ROBUSTNESS_BEFORE_ANY_"
    "PREFERENCE_CLAIM")

Q_SPINE = (50, 60, 70, 90)
ADJACENT_PAIRS = tuple(zip(Q_SPINE[:-1], Q_SPINE[1:]))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
RADII = (0, 1, 2)
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")

# The baseline TPC-308 ladder is the middle 17-term window.  LOW and HIGH
# are its two neighboring windows in a declared consecutive prime pool.  All
# profile entries are values of the same locked literal-beta source formula.
PROFILE_POOL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67)
PROFILE_LADDERS = {
    "LOW": PROFILE_POOL[:17],
    "BASE": PROFILE_POOL[1:18],
    "HIGH": PROFILE_POOL[2:19],
}
BASELINE_LADDER = "BASE"

MP_DPS = 70
FRONTIER_RESIDUAL_TOL = mp.mpf("1e-15")
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-5")
CLASSIFY_BELOW = mp.mpf("0.9")
CLASSIFY_ABOVE = mp.mpf("1.1")
THRESHOLD_TOL = mp.mpf("1e-20")
mp.mp.dps = MP_DPS

spec = importlib.util.spec_from_file_location("frozen_tpc308", PARENT_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-308 parent unavailable")
T308 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T308)


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


def interval(value: Any) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def emit(value: mp.mpf) -> str:
    return mp.nstr(value, 34)


def enclosure(value: mp.mpf) -> list[str]:
    radius = INTERVAL_RELATIVE_RADIUS * max(abs(value), mp.mpf("1e-30"))
    return [emit(value - radius), emit(value + radius)]


def ratio_interval(numerator: list[str], denominator: list[str]) -> list[str]:
    nlo, nhi = interval(numerator)
    dlo, dhi = interval(denominator)
    need(dlo > 0, "positive ratio denominator")
    return [emit(nlo / dhi), emit(nhi / dlo)]


def ratio_from_values(numerator: mp.mpf, denominator: mp.mpf) -> list[str]:
    need(numerator > 0 and denominator > 0, "positive ratio values")
    return ratio_interval(enclosure(numerator), enclosure(denominator))


def classify(value: list[str]) -> str:
    lo, hi = interval(value)
    if hi < CLASSIFY_BELOW:
        return "RIGHT_COMPLETION_LOWER"
    if lo > CLASSIFY_ABOVE:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def locked_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-308 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-308 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC-308 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == PARENT_STATUS, "TPC-308 header")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "TPC-308 payload hash")
    payload = data["payload"]
    need(payload.get("schema") ==
         "TPC308_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_V1",
         "TPC-308 schema")
    audit = payload["finite_audit"]
    need(audit.get("cases") == 18 and audit.get("radii") == 3 and
         audit.get("envelope_observations") == 54,
         "TPC-308 census")
    need(len(payload.get("cases", [])) == 18, "TPC-308 cases")
    return data


def source_context(cutoffs: tuple[int, ...]
                   ) -> tuple[list[int], list[Any], np.ndarray, mp.matrix,
                              mp.mpf]:
    """Build one source-backed profile ladder using the locked formula."""
    base_indices, beta_values, _, _, beta_norm = T308.PARENT.source_context()
    need(len(cutoffs) == 17 and tuple(sorted(cutoffs)) == cutoffs,
         "profile ladder order")
    need(len(set(cutoffs)) == len(cutoffs), "profile ladder uniqueness")
    profile_array = np.asarray(
        [[float(T308.PARENT.PARENT.PARENT.literal_beta(value, cutoff))
          for cutoff in cutoffs] for value in base_indices], dtype=np.float64)
    gram = profile_array.T @ profile_array
    matrix = mp.matrix([[mp.mpf(repr(float(value))) for value in row]
                        for row in gram.tolist()])
    return base_indices, beta_values, profile_array, matrix, beta_norm


def completion_envelope(prediction: mp.matrix, target: list[int],
                        positions: list[int], radius: int
                        ) -> tuple[mp.mpf, mp.mpf, mp.mpf, int]:
    need(len(target) == len(positions) and bool(target),
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
                for offset, (index, value) in enumerate(
                    zip(positions, target)))
            values.append(value / len(positions))
    need(bool(values), "nonempty completion envelope")
    return native, min(values), max(values), len(values)


def empty_preference_counts() -> dict[str, int]:
    return {"RIGHT_COMPLETION_LOWER": 0,
            "LEFT_COMPLETION_LOWER": 0,
            "PREFERENCE_UNRESOLVED": 0}


def empty_agreement_counts() -> dict[str, int]:
    return {"CONCORDANT": 0, "DISCORDANT": 0, "UNRESOLVED": 0}


def agreement(budget: str, holdout: str) -> str:
    if budget == holdout and budget != "PREFERENCE_UNRESOLVED":
        return "CONCORDANT"
    if {budget, holdout} == {
            "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"}:
        return "DISCORDANT"
    return "UNRESOLVED"


def profile_case(parent_case: dict[str, Any],
                 rows: dict[tuple[int, int], dict[str, Any]],
                 indices: list[int], beta: list[Any], profiles: np.ndarray,
                 gram: mp.matrix, beta_norm: mp.mpf,
                 ladder_name: str,
                 image_cache: dict[tuple[str, int, int, int], mp.matrix]
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
    need(parent_case["union_cardinality"] == len(union) and
         parent_case["overlap_cardinality"] == len(overlap) and
         parent_case["exclusive_left_cardinality"] == len(exclusive_left) and
         parent_case["exclusive_right_cardinality"] == len(exclusive_right),
         "parent partition")
    raw_inner = sum(left_map[p] * right_map[p] for p in overlap)
    sign = 1 if raw_inner >= 0 else -1
    aligned_right = {p: sign * value for p, value in right_map.items()}
    image_key = (ladder_name, left_q, right_q, exponent)
    if image_key not in image_cache:
        image_cache[image_key] = T308.PARENT.physical_image(
            indices, beta, profiles, union, exponent)
    ambient = image_cache[image_key]
    position = {p: i for i, p in enumerate(union)}
    overlap_indices = [position[p] for p in overlap]
    left_indices = [position[p] for p in exclusive_left]
    right_indices = [position[p] for p in exclusive_right]
    overlap_matrix = mp.matrix(
        [[ambient[i, j] for j in range(ambient.cols)]
         for i in overlap_indices])
    left_target = mp.matrix([left_map[p] for p in overlap])
    right_target = mp.matrix([aligned_right[p] for p in overlap])
    left_k = T308.PARENT.feasible_prefix(
        overlap_matrix, gram, left_target, mp.mpf(tau))
    right_k = T308.PARENT.feasible_prefix(
        overlap_matrix, gram, right_target, mp.mpf(tau))
    k = max(left_k, right_k)
    left_fit = T308.PARENT.frontier(
        overlap_matrix[:, :k], gram[:k, :k], left_target, mp.mpf(tau))
    right_fit = T308.PARENT.frontier(
        overlap_matrix[:, :k], gram[:k, :k], right_target, mp.mpf(tau))
    left_coefficients, left_frontier = left_fit
    right_coefficients, right_frontier = right_fit
    left_prediction = ambient[:, :k] * left_coefficients
    right_prediction = ambient[:, :k] * right_coefficients
    left_source = left_frontier["source_squared"]
    right_source = right_frontier["source_squared"]
    norms = {
        "beta_norm_squared": beta_norm,
        "profile_trace_mean": mp.fsum(gram[i, i] for i in range(k)) / k,
        "first_profile_norm_squared": gram[0, 0],
    }
    budget_ratios = {
        name: ratio_from_values(right_source / value,
                                left_source / value)
        for name, value in norms.items()
    }
    budget_classes = {name: classify(value)
                      for name, value in budget_ratios.items()}
    need(len(set(budget_classes.values())) == 1,
         "profile normalizer-invariant budget preference")
    profile_budget = next(iter(budget_classes.values()))
    frozen_budget = parent_case["envelopes"][0]["budget_preference"]
    records = []
    for radius in RADII:
        left_native, left_min, left_max, left_count = completion_envelope(
            left_prediction,
            [left_map[p] for p in exclusive_left], left_indices, radius)
        right_native, right_min, right_max, right_count = completion_envelope(
            right_prediction,
            [aligned_right[p] for p in exclusive_right], right_indices, radius)
        holdout_ratio = ratio_interval(
            enclosure(right_min), enclosure(left_max))
        # The upper endpoint must use right_max / left_min; spelling both
        # endpoints explicitly keeps the interval proof auditable.
        holdout_ratio = [
            emit(interval(enclosure(right_min))[0] /
                 interval(enclosure(left_max))[1]),
            emit(interval(enclosure(right_max))[1] /
                 interval(enclosure(left_min))[0]),
        ]
        holdout = classify(holdout_ratio)
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
            "holdout_right_over_left_interval": holdout_ratio,
            "profile_budget_preference": profile_budget,
            "frozen_budget_preference": frozen_budget,
            "holdout_preference": holdout,
            "agreement": agreement(profile_budget, holdout),
            "frozen_agreement": agreement(frozen_budget, holdout),
        })
    return {
        "profile_ladder": ladder_name,
        "profile_cutoffs": list(PROFILE_LADDERS[ladder_name]),
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
        "budget_right_over_left_interval": budget_ratios,
        "profile_budget_preference": profile_budget,
        "frozen_budget_preference": frozen_budget,
        "envelopes": records,
    }


def build_ladder_summary(cases: list[dict[str, Any]], ladder: str
                         ) -> dict[str, Any]:
    subset = [case for case in cases if case["profile_ladder"] == ladder]
    need(len(subset) == 18, "ladder case census")
    budget = empty_preference_counts()
    frozen_budget = empty_preference_counts()
    holdout = {str(r): empty_preference_counts() for r in RADII}
    agreements = {str(r): empty_agreement_counts() for r in RADII}
    frozen_agreements = {str(r): empty_agreement_counts() for r in RADII}
    discordance = {str(r): {str(pair): 0 for pair in ADJACENT_PAIRS}
                   for r in RADII}
    frozen_discordance = {str(r): {str(pair): 0 for pair in ADJACENT_PAIRS}
                          for r in RADII}
    prefix_counts: dict[str, int] = {}
    for case in subset:
        budget[case["profile_budget_preference"]] += 1
        frozen_budget[case["frozen_budget_preference"]] += 1
        prefix = str(case["comparison_prefix_k"])
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
        for record in case["envelopes"]:
            radius = str(record["radius"])
            holdout[radius][record["holdout_preference"]] += 1
            agreements[radius][record["agreement"]] += 1
            frozen_agreements[radius][record["frozen_agreement"]] += 1
            pair = str((case["from_Q"], case["to_Q"]))
            if record["agreement"] == "DISCORDANT":
                discordance[radius][pair] += 1
            if record["frozen_agreement"] == "DISCORDANT":
                frozen_discordance[radius][pair] += 1
    return {
        "profile_ladder": ladder,
        "profile_cutoffs": list(PROFILE_LADDERS[ladder]),
        "cases": 18,
        "profile_budget_preference_counts": budget,
        "frozen_budget_preference_counts": frozen_budget,
        "holdout_preference_counts_by_radius": holdout,
        "agreement_counts_by_radius": agreements,
        "frozen_agreement_counts_by_radius": frozen_agreements,
        "discordance_by_pair_and_radius": discordance,
        "frozen_discordance_by_pair_and_radius": frozen_discordance,
        "comparison_prefix_counts": prefix_counts,
    }


def build_payload() -> dict[str, Any]:
    parent = locked_parent()
    rows = T308.parent_rows(parent)
    indices, beta, _, _, beta_norm = T308.PARENT.source_context()
    cases: list[dict[str, Any]] = []
    image_cache: dict[tuple[str, int, int, int], mp.matrix] = {}
    for ladder, cutoffs in PROFILE_LADDERS.items():
        _, _, profiles, gram, _ = source_context(cutoffs)
        for parent_case in parent["payload"]["cases"]:
            cases.append(profile_case(parent_case, rows, indices, beta,
                                      profiles, gram, beta_norm, ladder,
                                      image_cache))
    need(len(cases) == 54, "profile case census")
    ladder_summaries = [build_ladder_summary(cases, ladder)
                        for ladder in PROFILE_LADDERS]
    # Baseline is a direct reproduction of TPC-308's fixed profile path at
    # every radius.  The budget and holdout classes are checked here; exact
    # decimal enclosures remain locked by the certificate replay.
    baseline = [case for case in cases if case["profile_ladder"] == BASELINE_LADDER]
    for parent_case, case in zip(parent["payload"]["cases"], baseline):
        need(case["frozen_budget_preference"] ==
             parent_case["envelopes"][0]["budget_preference"],
             "baseline budget recovery")
        for old, new in zip(parent_case["envelopes"], case["envelopes"]):
            need(new["holdout_preference"] == old["holdout_preference"] and
                 new["frozen_agreement"] == old["agreement"],
                 "baseline TPC-308 class recovery")

    candidate_by_radius = {}
    for radius in RADII:
        candidate_by_radius[str(radius)] = sum(
            record["candidate_count"]
            for case in cases for record in case["envelopes"]
            if record["radius"] == radius)
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc308_code_sha256": PARENT_CODE_SHA256,
            "tpc308_result_sha256": PARENT_RESULT_SHA256,
            "tpc308_cases": 18,
            "tpc308_envelope_observations": 54,
        },
        "protocol": {
            "Q_spine": list(Q_SPINE),
            "kernel_exponents": list(EXPONENTS),
            "tolerances": list(TAUS),
            "hamming_radii": list(RADII),
            "profile_pool": list(PROFILE_POOL),
            "profile_ladders": {
                name: list(cutoffs) for name, cutoffs in PROFILE_LADDERS.items()},
            "ladder_rule": (
                "three contiguous 17-cutoff windows in the 19-prime pool"),
            "fit_lock": "same TPC-308 union rows, labels, and physical source",
            "completion_rule": (
                "flip at most r binary labels on each native exclusive holdout"),
            "ratio_rule": "right envelope holdout MSE / left envelope holdout MSE",
            "strict_classification": (
                "right lower iff upper ratio<0.9; left lower iff lower ratio>1.1"),
            "primary_budget_rule": "recompute source-budget ratio per profile ladder",
            "secondary_budget_rule": "freeze TPC-308 budget class for isolation",
        },
        "exact_theorem": {
            "window_construction": (
                "each ladder is an ordered contiguous 17-subwindow of the declared pool"),
            "prefix_nesting": (
                "least-squares feasibility is nested as the ordered prefix grows"),
            "hamming_extrema": (
                "finite completion enumeration attains each directional minimum and maximum"),
            "normalizer_invariance": (
                "the same positive normalizer cancels from a right/left source ratio"),
            "interval_soundness": (
                "an enclosure wholly outside 0.9 and 1.1 implies its finite class"),
            "scope": "finite profile-model sensitivity diagnostic",
        },
        "cases": cases,
        "ladder_summary": ladder_summaries,
        "finite_audit": {
            "profile_ladders": 3,
            "cases_per_ladder": 18,
            "profile_case_observations": 54,
            "envelope_observations": 162,
            "directional_envelope_records": 324,
            "candidate_evaluations_by_radius": candidate_by_radius,
            "candidate_evaluations_by_ladder_and_radius": {
                ladder["profile_ladder"]: {
                    str(radius): sum(
                        record["candidate_count"]
                        for case in cases
                        if case["profile_ladder"] == ladder["profile_ladder"]
                        for record in case["envelopes"]
                        if record["radius"] == radius)
                    for radius in RADII}
                for ladder in ladder_summaries},
            "baseline_tpc308_class_recovery": True,
            "target_generation_leakage":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "formal_interval_certificate": "OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "causal_identification": "NONE_PROFILE_SENSITIVITY_DIAGNOSTIC_ONLY",
            "uniform_asymptotic_budget": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
            "full_gate_b": "OPEN",
            "twin_prime_result": "NONE",
        },
        "firewall": {
            "TPC309_WINDOW_PROTOCOL": "PROVED_EXACT_FINITE",
            "TPC309_PREFIX_NESTING": "PROVED_EXACT_FINITE",
            "TPC309_HAMMING_EXTREMA": "PROVED_EXACT_FINITE",
            "TPC309_NORMALIZER_INVARIANCE": "PROVED_EXACT_FINITE",
            "TPC309_PROFILE_ATLAS":
                "NUMERICALLY_REPRODUCED_FINITE_54_PROFILE_CASES_162_ENVELOPES",
            "TPC309_BASELINE_RECOVERY": "NUMERICALLY_REPRODUCED_FINITE_TPC308_CLASSES",
            "TPC309_PROFILE_ROBUSTNESS": "OPEN_PROFILE_INDEPENDENT_PREFERENCE",
            "TPC309_CAUSAL_IDENTIFICATION":
                "NONE_PROFILE_SENSITIVITY_DIAGNOSTIC_ONLY",
            "TPC309_FORMAL_INTERVAL_CERTIFICATE":
                "OPEN_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "TPC309_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC309_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC309_FIXED_POWER_CREDIT": 0,
            "TPC309_FULL_GATE_B": "OPEN",
            "TPC309_TWIN_PRIME_RESULT": "NONE",
            "TPC309_STATUS": STATUS,
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
    print("TPC309_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["profile_ladders"] == 3 and
         audit["profile_case_observations"] == 54 and
         audit["envelope_observations"] == 162 and
         audit["directional_envelope_records"] == 324,
         "finite audit")
    print("TPC309_CERTIFICATE=PASS ladders=3 cases=54 envelopes=162 "
          "r0=108 r1=558 r2=1440")


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
        print("TPC309_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
