#!/usr/bin/env python3
"""Two-way operator/target decomposition for the TPC-305 atlas.

TPC-305 supplies four positive budget cells for every adjacent shell pair:
each of two physical operators is evaluated on its native target and on the
aligned neighboring target.  TPC-306 turns those cells into two log target
switch effects, a main contrast, and an operator-interaction contrast.  The
identity between the squared contrasts is exact; the finite log intervals are
derived from the locked TPC-305 ratio intervals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mpmath as mp
import sys
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
TPC305_CODE = ROOT / (
    "papers/tpc-305-counterfactual-transported-label-budget/code/"
    "tpc305_counterfactual_transported_label_budget.py")
TPC305_RESULT = ROOT / (
    "papers/tpc-305-counterfactual-transported-label-budget/results/"
    "tpc305_certificate.json")
RESULT = PROJECT / "results/tpc306_certificate.json"

TPC305_CODE_SHA256 = (
    "fa43b82a3a7a7adf8821cf8ebacbfadad80759b917787d00ce365e43adfd4c5d")
TPC305_RESULT_SHA256 = (
    "e2f243ed86132af0cd4a6de169723246f3e2fdc0e4fa595fa3b1ffafe657cad3")
TPC305_STATUS = (
    "PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_"
    "NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS")
STATUS = (
    "PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS")
SCHEMA = "TPC306_TWO_WAY_OPERATOR_TARGET_INTERACTION_V1"
ROUND2_CLUE = (
    "TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_"
    "BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM")
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")
PAIR_ORDER = ((50, 60), (60, 70), (70, 90))
MAIN_RATIO_CEILING = mp.mpf("0.88")
INTERACTION_RATIO_FLOOR = mp.mpf("1.2")
MP_DPS = 80
DERIVED_PADDING = mp.mpf("1e-30")
mp.mp.dps = MP_DPS


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


def interval(value: Any) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def emit(value: mp.mpf) -> str:
    return mp.nstr(value, 38)


def saved(bounds: tuple[mp.mpf, mp.mpf]) -> list[str]:
    lo, hi = bounds
    need(lo <= hi, "derived interval order")
    return [emit(lo), emit(hi)]


def positive_log(value: Any) -> tuple[mp.mpf, mp.mpf]:
    lo, hi = interval(value)
    need(lo > 0, "log domain")
    a, b = mp.log(lo), mp.log(hi)
    pad = DERIVED_PADDING * max(mp.mpf(1), abs(a), abs(b))
    return a - pad, b + pad


def negate(bounds: tuple[mp.mpf, mp.mpf]) -> tuple[mp.mpf, mp.mpf]:
    return -bounds[1], -bounds[0]


def add(left: tuple[mp.mpf, mp.mpf], right: tuple[mp.mpf, mp.mpf]
        ) -> tuple[mp.mpf, mp.mpf]:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: tuple[mp.mpf, mp.mpf], right: tuple[mp.mpf, mp.mpf]
             ) -> tuple[mp.mpf, mp.mpf]:
    return left[0] - right[1], left[1] - right[0]


def halve(bounds: tuple[mp.mpf, mp.mpf]) -> tuple[mp.mpf, mp.mpf]:
    return bounds[0] / 2, bounds[1] / 2


def multiply(left: tuple[mp.mpf, mp.mpf], right: tuple[mp.mpf, mp.mpf]
             ) -> tuple[mp.mpf, mp.mpf]:
    candidates = [left[0] * right[0], left[0] * right[1],
                  left[1] * right[0], left[1] * right[1]]
    return min(candidates), max(candidates)


def absolute(bounds: tuple[mp.mpf, mp.mpf]) -> tuple[mp.mpf, mp.mpf]:
    if bounds[0] >= 0:
        return bounds
    if bounds[1] <= 0:
        return -bounds[1], -bounds[0]
    return mp.mpf(0), max(-bounds[0], bounds[1])


def divide_positive(numerator: tuple[mp.mpf, mp.mpf],
                    denominator: tuple[mp.mpf, mp.mpf]
                    ) -> tuple[mp.mpf, mp.mpf]:
    need(denominator[0] > 0, "positive derived denominator")
    return numerator[0] / denominator[1], numerator[1] / denominator[0]


def sign_class(left: tuple[mp.mpf, mp.mpf],
               right: tuple[mp.mpf, mp.mpf]) -> str:
    if left[1] < 0 and right[1] < 0:
        return "RIGHT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    if left[0] > 0 and right[0] > 0:
        return "LEFT_LABEL_CHEAPER_ON_BOTH_OPERATORS"
    return "MIXED_OPERATOR_PREFERENCE"


def dominance(product: tuple[mp.mpf, mp.mpf]) -> str:
    if product[0] > 0:
        return "TARGET_MAIN_DOMINATES"
    if product[1] < 0:
        return "OPERATOR_INTERACTION_DOMINATES"
    return "DOMINANCE_UNRESOLVED"


def load_parent() -> dict[str, Any]:
    need(digest(TPC305_CODE.read_bytes()) == TPC305_CODE_SHA256,
         "TPC-305 code provenance")
    raw = TPC305_RESULT.read_bytes()
    need(digest(raw) == TPC305_RESULT_SHA256, "TPC-305 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC-305 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == TPC305_STATUS, "TPC-305 status")
    payload = data.get("payload", {})
    need(payload.get("schema") == "TPC305_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGET_V1",
         "TPC-305 schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "TPC-305 payload hash")
    need(payload.get("finite_audit", {}).get("cases") == 18 and
         payload.get("finite_audit", {}).get("operator_budget_tables") == 36,
         "TPC-305 census")
    return data


def build_case(case: dict[str, Any]) -> dict[str, Any]:
    decompositions: dict[str, Any] = {}
    for name in NORMALIZERS:
        left_ratio = positive_log(
            case["left_operator"]["transported_over_native_interval"][name])
        right_ratio = positive_log(
            case["right_operator"]["transported_over_native_interval"][name])
        # d_L is the log effect of switching left -> right on the left
        # operator.  d_R uses the same target switch on the right operator.
        d_left = left_ratio
        d_right = negate(right_ratio)
        main = halve(add(d_left, d_right))
        interaction = halve(subtract(d_left, d_right))
        product = multiply(d_left, d_right)
        abs_main = absolute(main)
        abs_interaction = absolute(interaction)
        ratio = divide_positive(abs_interaction, abs_main)
        decompositions[name] = {
            "left_log_target_effect": saved(d_left),
            "right_log_target_effect": saved(d_right),
            "target_main_contrast": saved(main),
            "operator_interaction_contrast": saved(interaction),
            "squared_dominance_gap": saved(product),
            "interaction_to_main_abs_ratio": saved(ratio),
            "target_preference": sign_class(d_left, d_right),
            "dominance_status": dominance(product),
        }
    target_preferences = {
        item["target_preference"] for item in decompositions.values()}
    dominance_statuses = {
        item["dominance_status"] for item in decompositions.values()}
    need(len(target_preferences) == 1 and len(dominance_statuses) == 1,
         "normalizer-invariant decomposition")
    parent = case["parent_budget_case_census"]
    return {
        "from_Q": case["from_Q"],
        "to_Q": case["to_Q"],
        "kernel_exponent": case["kernel_exponent"],
        "tau": case["tau"],
        "parent_target_orientation": case["target_orientation"],
        "same_prefix_parent_descent": parent["same_prefix_descents"] > 0,
        "decomposition_by_normalizer": decompositions,
        "target_preference": next(iter(target_preferences)),
        "dominance_status": next(iter(dominance_statuses)),
    }


def build_payload() -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    parent = load_parent()
    cases = [build_case(case) for case in parent["payload"]["cases"]]
    need(len(cases) == 18, "decomposition case census")
    main_cases = [case for case in cases
                  if case["dominance_status"] == "TARGET_MAIN_DOMINATES"]
    interaction_cases = [case for case in cases
                         if case["dominance_status"] ==
                         "OPERATOR_INTERACTION_DOMINATES"]
    unresolved_cases = [case for case in cases
                        if case["dominance_status"] == "DOMINANCE_UNRESOLVED"]
    need(len(main_cases) == 12 and len(interaction_cases) == 6 and
         not unresolved_cases, "global dominance census")

    pair_summary = []
    for pair in PAIR_ORDER:
        subset = [case for case in cases
                  if (case["from_Q"], case["to_Q"]) == pair]
        need(len(subset) == 6, "pair decomposition census")
        pair_summary.append({
            "from_Q": pair[0],
            "to_Q": pair[1],
            "case_count": len(subset),
            "target_main_dominates": sum(
                item["dominance_status"] == "TARGET_MAIN_DOMINATES"
                for item in subset),
            "operator_interaction_dominates": sum(
                item["dominance_status"] ==
                "OPERATOR_INTERACTION_DOMINATES" for item in subset),
            "same_prefix_target_main_dominates": sum(
                item["same_prefix_parent_descent"] and
                item["dominance_status"] == "TARGET_MAIN_DOMINATES"
                for item in subset),
        })
    middle = next(item for item in pair_summary
                  if item["from_Q"] == 60 and item["to_Q"] == 70)
    need(middle["target_main_dominates"] == 5 and
         middle["operator_interaction_dominates"] == 1 and
         middle["same_prefix_target_main_dominates"] == 3,
         "middle dominance census")

    main_ratios = []
    interaction_ratios = []
    middle_same_prefix_ratios = []
    for case in cases:
        for name in NORMALIZERS:
            record = case["decomposition_by_normalizer"][name]
            bounds = interval(record["interaction_to_main_abs_ratio"])
            if case["dominance_status"] == "TARGET_MAIN_DOMINATES":
                main_ratios.append(bounds)
            else:
                interaction_ratios.append(bounds)
            if ((case["from_Q"], case["to_Q"]) == (60, 70) and
                    case["same_prefix_parent_descent"]):
                middle_same_prefix_ratios.append(bounds)
    max_main = max(bounds[1] for bounds in main_ratios)
    min_interaction = min(bounds[0] for bounds in interaction_ratios)
    max_middle_same = max(bounds[1] for bounds in middle_same_prefix_ratios)
    need(max_main < MAIN_RATIO_CEILING and
         min_interaction > INTERACTION_RATIO_FLOOR and
         max_middle_same < mp.mpf("0.64"), "contrast separation margins")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc305_code_sha256": TPC305_CODE_SHA256,
            "tpc305_result_sha256": TPC305_RESULT_SHA256,
            "tpc305_cases": 18,
            "tpc305_operator_tables": 36,
        },
        "definition": {
            "cell_table": "B_LL,B_LR,B_RL,B_RR with operator first and target second",
            "left_effect": "d_L=log(B_LR/B_LL)",
            "right_effect": "d_R=log(B_RR/B_RL)",
            "target_main_contrast": "m=(d_L+d_R)/2",
            "operator_interaction_contrast": "i=(d_L-d_R)/2",
            "squared_identity": "m^2-i^2=d_L*d_R",
            "normalizers": list(NORMALIZERS),
            "ratio_interval_padding": emit(DERIVED_PADDING),
        },
        "exact_theorem": {
            "four_cell_log_decomposition": (
                "d_L=m+i and d_R=m-i"),
            "squared_dominance_identity": "m^2-i^2=d_L*d_R",
            "stable_preference_criterion": (
                "same-sign d_L,d_R iff |m|>|i|"),
            "mixed_preference_criterion": (
                "opposite-sign d_L,d_R iff |i|>|m|"),
            "row_positive_scaling_invariance": (
                "multiplying both cells in one operator row by a positive factor leaves its log effect unchanged"),
            "scope": (
                "finite shell-specific target completions; algebraic decomposition, not causal identification"),
        },
        "cases": cases,
        "pair_summary": pair_summary,
        "finite_audit": {
            "cases": len(cases),
            "decomposition_rows": len(cases) * len(NORMALIZERS),
            "target_main_dominates_cases": len(main_cases),
            "operator_interaction_dominates_cases": len(interaction_cases),
            "unresolved_cases": len(unresolved_cases),
            "middle_pair": [60, 70],
            "middle_target_main_dominates": middle["target_main_dominates"],
            "middle_operator_interaction_dominates": middle[
                "operator_interaction_dominates"],
            "middle_same_prefix_target_main_dominates": middle[
                "same_prefix_target_main_dominates"],
            "all_main_ratio_intervals_below_0_88": True,
            "all_interaction_ratio_intervals_above_1_2": True,
            "middle_same_prefix_max_ratio_below_0_64": True,
            "max_main_ratio_interval": saved((
                max(bounds[0] for bounds in main_ratios), max_main)),
            "min_interaction_ratio_interval": saved((
                min_interaction,
                min(bounds[1] for bounds in interaction_ratios))),
            "middle_same_prefix_max_ratio_interval": saved((
                max(bounds[0] for bounds in middle_same_prefix_ratios),
                max_middle_same)),
            "fixed_power_credit": 0,
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "uniform_asymptotic_budget": "OPEN",
            "causal_identification": "OPEN_COMMON_AMBIENT_HOLDOUT",
        },
        "firewall": {
            "TPC306_LOG_DECOMPOSITION": "PROVED_EXACT_FINITE",
            "TPC306_SQUARED_DOMINANCE_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC306_ROW_SCALING_INVARIANCE": "PROVED_EXACT_FINITE",
            "TPC306_TARGET_MAIN_DOMINANCE": "NUMERICALLY_CERTIFIED_FINITE_12_OF_18",
            "TPC306_OPERATOR_INTERACTION_DOMINANCE": "NUMERICALLY_CERTIFIED_FINITE_6_OF_18",
            "TPC306_MIDDLE_TARGET_MAIN_DOMINANCE": "NUMERICALLY_CERTIFIED_FINITE_5_OF_6",
            "TPC306_MIDDLE_SAME_PREFIX_TARGET_MAIN": "NUMERICALLY_CERTIFIED_FINITE_3_OF_3",
            "TPC306_CAUSAL_IDENTIFICATION": "OPEN_COMMON_AMBIENT_HOLDOUT",
            "TPC306_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC306_FIXED_POWER_CREDIT": 0,
            "TPC306_FULL_GATE_B": "OPEN",
            "TPC306_TWIN_PRIME_RESULT": "NONE",
            "TPC306_STATUS": STATUS,
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
    print("TPC306_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["cases"] == 18 and
         audit["decomposition_rows"] == 54 and
         audit["target_main_dominates_cases"] == 12 and
         audit["operator_interaction_dominates_cases"] == 6 and
         audit["middle_target_main_dominates"] == 5 and
         audit["middle_same_prefix_target_main_dominates"] == 3 and
         audit["fixed_power_credit"] == 0,
         "finite audit")
    print("TPC306_CERTIFICATE=PASS cases=18 decomposition_rows=54 "
          "target_main=12/18 interaction=6/18 middle=5/6 same_prefix=3/3")


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
        print("TPC306_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
