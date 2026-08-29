#!/usr/bin/env python3
"""TPC-310: cross-holdout aggregation-order audit.

The input is the locked finite TPC-309 profile/completion atlas.  This release
does not choose a preferred profile ladder.  Instead it enumerates every
nonempty subset of the three profile ladders and every nonempty subset of the
three completion radii, then applies three explicitly declared aggregation
maps to the positive holdout intervals:

* pooled MSE, which sums directional completion extrema before taking a ratio;
* equal-case arithmetic mean of the row ratios; and
* equal-case geometric mean of the row ratios.

The finite algebra is exact relative to the parent interval inputs.  The
parent physical values are numerical replay data, so the resulting atlas is
not an asymptotic or directed-rounding theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

import mpmath as mp

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-309-profile-prefix-shift-sensitivity/code/"
    "tpc309_profile_prefix_shift_sensitivity.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-309-profile-prefix-shift-sensitivity/results/"
    "tpc309_certificate.json")
RESULT = PROJECT / "results/tpc310_certificate.json"

PARENT_CODE_SHA256 = (
    "2284d9ccfcadd02eb5e82a301bdbfa85013e3e9a8352d8f3b078d020742890d9")
PARENT_RESULT_SHA256 = (
    "a4c8f7cd4aef327682b9457c21236f3756f454f4b82f5a901ab2933f1d4cad4a")
PARENT_STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS")
STATUS = (
    "PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS")
SCHEMA = "TPC310_CROSS_HOLDOUT_AGGREGATION_ORDER_AUDIT_V1"
ROUND2_CLUE = (
    "TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_BEFORE_"
    "ANY_GLOBAL_PREFERENCE_CLAIM")

LADDERS = ("LOW", "BASE", "HIGH")
RADII = (0, 1, 2)
MODES = ("POOLED_MSE", "BALANCED_RATIO", "GEOMETRIC_RATIO")
CLASSIFY_BELOW = mp.mpf("0.9")
CLASSIFY_ABOVE = mp.mpf("1.1")
MP_DPS = 70
mp.mp.dps = MP_DPS


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


def interval(value: Any) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def positive_interval(value: Any, label: str) -> tuple[mp.mpf, mp.mpf]:
    lo, hi = interval(value)
    need(lo > 0, label + " positivity")
    return lo, hi


def classify(value: tuple[mp.mpf, mp.mpf]) -> str:
    lo, hi = value
    if hi < CLASSIFY_BELOW:
        return "RIGHT_COMPLETION_LOWER"
    if lo > CLASSIFY_ABOVE:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def agreement(budget: str, holdout: str) -> str:
    if budget == holdout and budget != "PREFERENCE_UNRESOLVED":
        return "CONCORDANT"
    if {budget, holdout} == {
            "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"}:
        return "DISCORDANT"
    return "UNRESOLVED"


def subsets(values: tuple[Any, ...]) -> tuple[tuple[Any, ...], ...]:
    return tuple(tuple(values[i] for i in choice)
                 for size in range(1, len(values) + 1)
                 for choice in itertools.combinations(range(len(values)), size))


LADDER_SUBSETS = subsets(LADDERS)
RADIUS_SUBSETS = subsets(RADII)


def empty_class_counts() -> dict[str, int]:
    return {"RIGHT_COMPLETION_LOWER": 0,
            "LEFT_COMPLETION_LOWER": 0,
            "PREFERENCE_UNRESOLVED": 0}


def empty_agreement_counts() -> dict[str, int]:
    return {"CONCORDANT": 0, "DISCORDANT": 0, "UNRESOLVED": 0}


def locked_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-309 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-309 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC-309 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == PARENT_STATUS, "TPC-309 header")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "TPC-309 payload hash")
    payload = data["payload"]
    need(payload.get("schema") ==
         "TPC309_THREE_WINDOW_PROFILE_PREFIX_SHIFT_AUDIT_V1",
         "TPC-309 schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("profile_case_observations") == 54 and
         audit.get("envelope_observations") == 162,
         "TPC-309 parent census")
    need(len(payload.get("cases", [])) == 54 and
         all(len(case.get("envelopes", [])) == 3
             for case in payload["cases"]), "TPC-309 parent shape")
    return data


def extract_observations(parent: dict[str, Any]) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for case in parent["payload"]["cases"]:
        ladder = case["profile_ladder"]
        need(ladder in LADDERS, "parent ladder")
        case_key = (ladder, int(case["from_Q"]), int(case["to_Q"]),
                    int(case["kernel_exponent"]), case["tau"])
        for envelope in case["envelopes"]:
            radius = int(envelope["radius"])
            key = case_key + (radius,)
            need(key not in seen, "duplicate parent envelope")
            seen.add(key)
            ratio_lo, ratio_hi = positive_interval(
                envelope["holdout_right_over_left_interval"],
                "parent holdout ratio")
            right = envelope["right_completion"]
            left = envelope["left_completion"]
            right_min_lo, right_min_hi = positive_interval(
                right["envelope_min_mse"], "right minimum")
            right_max_lo, right_max_hi = positive_interval(
                right["envelope_max_mse"], "right maximum")
            left_min_lo, left_min_hi = positive_interval(
                left["envelope_min_mse"], "left minimum")
            left_max_lo, left_max_hi = positive_interval(
                left["envelope_max_mse"], "left maximum")
            need(right_min_lo <= right_min_hi <= right_max_hi,
                 "right extrema order")
            need(left_min_lo <= left_min_hi <= left_max_hi,
                 "left extrema order")
            observations.append({
                "key": key,
                "ladder": ladder,
                "radius": radius,
                "ratio_lo": ratio_lo,
                "ratio_hi": ratio_hi,
                "right_min_lo": right_min_lo,
                "right_max_hi": right_max_hi,
                "left_min_lo": left_min_lo,
                "left_max_hi": left_max_hi,
            })
    need(len(observations) == 162 and len(seen) == 162,
         "observation census")
    return observations


def budget_vote(parent: dict[str, Any], ladder_subset: tuple[str, ...]
                ) -> tuple[str, dict[str, int]]:
    counts = empty_class_counts()
    for case in parent["payload"]["cases"]:
        if case["profile_ladder"] in ladder_subset:
            label = case["profile_budget_preference"]
            need(label in counts, "budget label")
            counts[label] += 1
    values = sorted(counts.values(), reverse=True)
    if values[0] == 0 or (len(values) > 1 and values[0] == values[1]):
        return "PREFERENCE_UNRESOLVED", counts
    winner = max(counts, key=counts.get)
    return winner, counts


def aggregate(selected: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    need(bool(selected) and mode in MODES, "aggregate input")
    n = len(selected)
    if mode == "POOLED_MSE":
        # Independent completion choices make the extrema of a sum additive.
        right_lower = mp.fsum(row["right_min_lo"] for row in selected)
        right_upper = mp.fsum(row["right_max_hi"] for row in selected)
        left_lower = mp.fsum(row["left_min_lo"] for row in selected)
        left_upper = mp.fsum(row["left_max_hi"] for row in selected)
        bounds = (right_lower / left_upper, right_upper / left_lower)
        diagnostic = {
            "right_lower_sum": emit(right_lower),
            "right_upper_sum": emit(right_upper),
            "left_lower_sum": emit(left_lower),
            "left_upper_sum": emit(left_upper),
        }
    elif mode == "BALANCED_RATIO":
        lower_sum = mp.fsum(row["ratio_lo"] for row in selected)
        upper_sum = mp.fsum(row["ratio_hi"] for row in selected)
        bounds = (lower_sum / n, upper_sum / n)
        diagnostic = {
            "ratio_lower_sum": emit(lower_sum),
            "ratio_upper_sum": emit(upper_sum),
        }
    else:
        lower_log_sum = mp.fsum(mp.log(row["ratio_lo"])
                                for row in selected)
        upper_log_sum = mp.fsum(mp.log(row["ratio_hi"])
                                for row in selected)
        bounds = (mp.exp(lower_log_sum / n),
                  mp.exp(upper_log_sum / n))
        diagnostic = {
            "log_ratio_lower_sum": emit(lower_log_sum),
            "log_ratio_upper_sum": emit(upper_log_sum),
        }
    need(bounds[0] > 0 and bounds[0] <= bounds[1],
         "aggregate interval")
    return {
        "mode": mode,
        "observation_count": n,
        "ratio_interval": [emit(bounds[0]), emit(bounds[1])],
        "class": classify(bounds),
        "diagnostic": diagnostic,
    }


def selector_record(parent: dict[str, Any], observations: list[dict[str, Any]],
                    ladder_subset: tuple[str, ...],
                    radius_subset: tuple[int, ...]) -> dict[str, Any]:
    selected = [row for row in observations
                if row["ladder"] in ladder_subset and
                row["radius"] in radius_subset]
    need(len(selected) == 18 * len(ladder_subset) * len(radius_subset),
         "selector observation count")
    vote, counts = budget_vote(parent, ladder_subset)
    aggregates = [aggregate(selected, mode) for mode in MODES]
    for row in aggregates:
        row["budget_vote"] = vote
        row["budget_agreement"] = agreement(vote, row["class"])
    return {
        "ladder_subset": list(ladder_subset),
        "radius_subset": list(radius_subset),
        "observation_count": len(selected),
        "budget_vote": vote,
        "budget_counts": counts,
        "aggregates": aggregates,
    }


def find_selector(selectors: list[dict[str, Any]],
                  ladders: tuple[str, ...], radii: tuple[int, ...]
                  ) -> dict[str, Any]:
    for selector in selectors:
        if (tuple(selector["ladder_subset"]) == ladders and
                tuple(selector["radius_subset"]) == radii):
            return selector
    raise CheckFailure("selector not found")


def class_counts(selectors: list[dict[str, Any]], mode: str
                 ) -> dict[str, int]:
    counts = empty_class_counts()
    for selector in selectors:
        row = next(item for item in selector["aggregates"]
                   if item["mode"] == mode)
        counts[row["class"]] += 1
    return counts


def pairwise_counts(selectors: list[dict[str, Any]], first: str,
                    second: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for selector in selectors:
        classes = {item["mode"]: item["class"]
                   for item in selector["aggregates"]}
        key = classes[first] + "|" + classes[second]
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def agreement_counts(selectors: list[dict[str, Any]], mode: str
                     ) -> dict[str, int]:
    counts = empty_agreement_counts()
    for selector in selectors:
        row = next(item for item in selector["aggregates"]
                   if item["mode"] == mode)
        counts[row["budget_agreement"]] += 1
    return counts


def compact_selector(selector: dict[str, Any]) -> dict[str, Any]:
    return {
        "ladder_subset": selector["ladder_subset"],
        "radius_subset": selector["radius_subset"],
        "budget_vote": selector["budget_vote"],
        "aggregates": [
            {"mode": row["mode"], "class": row["class"],
             "ratio_interval": row["ratio_interval"],
             "budget_agreement": row["budget_agreement"]}
            for row in selector["aggregates"]],
    }


def build_payload() -> dict[str, Any]:
    parent = locked_parent()
    observations = extract_observations(parent)
    selectors = [selector_record(parent, observations, ladders, radii)
                 for ladders in LADDER_SUBSETS
                 for radii in RADIUS_SUBSETS]
    need(len(selectors) == 49, "selector census")
    full = find_selector(selectors, LADDERS, RADII)
    full_classes = {row["mode"]: row["class"] for row in full["aggregates"]}
    need(full_classes == {"POOLED_MSE": "RIGHT_COMPLETION_LOWER",
                          "BALANCED_RATIO": "LEFT_COMPLETION_LOWER",
                          "GEOMETRIC_RATIO": "RIGHT_COMPLETION_LOWER"},
         "full aggregation-order reversal")
    profile_singletons = [
        compact_selector(find_selector(selectors, (ladder,), RADII))
        for ladder in LADDERS]
    radius_singletons = [
        compact_selector(find_selector(selectors, LADDERS, (radius,)))
        for radius in RADII]
    leave_one_ladder_out = [
        compact_selector(find_selector(
            selectors, tuple(l for l in LADDERS if l != omitted), RADII))
        for omitted in LADDERS]
    leave_one_radius_out = [
        compact_selector(find_selector(
            selectors, LADDERS, tuple(r for r in RADII if r != omitted)))
        for omitted in RADII]

    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc309_code_sha256": PARENT_CODE_SHA256,
            "tpc309_result_sha256": PARENT_RESULT_SHA256,
            "tpc309_profile_cases": 54,
            "tpc309_envelope_observations": 162,
        },
        "protocol": {
            "ladders": list(LADDERS),
            "radii": list(RADII),
            "aggregation_modes": list(MODES),
            "selector_rule": (
                "all nonempty ladder subsets crossed with all nonempty radius subsets"),
            "selector_count": 49,
            "pooled_rule": (
                "sum right/left completion extrema before ratio"),
            "balanced_rule": "arithmetic mean of positive row-ratio intervals",
            "geometric_rule": "geometric mean of positive row-ratio intervals",
            "thresholds": {"right_upper_lt": "0.9",
                           "left_lower_gt": "1.1"},
            "budget_anchor": (
                "strict majority of profile-budget classes over selected ladders;"
                " ties are unresolved"),
        },
        "exact_theorem": {
            "selector_enumeration": (
                "the 7 nonempty ladder subsets and 7 nonempty radius subsets give 49 selectors"),
            "pooled_extrema": (
                "independent finite completion choices make sum extrema additive"),
            "positive_interval_maps": (
                "positive sums, arithmetic means, log, and exp preserve sound interval order"),
            "weighted_mean_identity": (
                "sum_i a_i/sum_i b_i equals the b_i-weighted mean of a_i/b_i for b_i>0"),
            "scope": "finite aggregation-order and profile-robustness diagnostic",
        },
        "selectors": selectors,
        "finite_audit": {
            "parent_profile_cases": 54,
            "parent_envelope_observations": 162,
            "parent_candidate_evaluations": 2106,
            "ladder_subset_count": 7,
            "radius_subset_count": 7,
            "selectors": 49,
            "aggregate_observations": 147,
            "class_counts_by_mode": {
                mode: class_counts(selectors, mode) for mode in MODES},
            "agreement_counts_by_mode": {
                mode: agreement_counts(selectors, mode) for mode in MODES},
            "pairwise_class_counts": {
                "POOLED_MSE_vs_BALANCED_RATIO":
                    pairwise_counts(selectors, "POOLED_MSE", "BALANCED_RATIO"),
                "POOLED_MSE_vs_GEOMETRIC_RATIO":
                    pairwise_counts(selectors, "POOLED_MSE", "GEOMETRIC_RATIO"),
                "BALANCED_RATIO_vs_GEOMETRIC_RATIO":
                    pairwise_counts(selectors, "BALANCED_RATIO", "GEOMETRIC_RATIO"),
            },
            "full_selector_classes": full_classes,
            "profile_singletons_all_radii": profile_singletons,
            "radius_singletons_all_ladders": radius_singletons,
            "leave_one_ladder_out": leave_one_ladder_out,
            "leave_one_radius_out": leave_one_radius_out,
            "target_generation_leakage":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "formal_interval_certificate":
                "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "causal_identification": "NONE_AGGREGATION_DIAGNOSTIC_ONLY",
            "uniform_asymptotic_budget": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
            "full_gate_b": "OPEN",
            "twin_prime_result": "NONE",
        },
        "firewall": {
            "TPC310_SELECTOR_PROTOCOL": "PROVED_EXACT_FINITE",
            "TPC310_POOLED_EXTREMA": "PROVED_EXACT_FINITE",
            "TPC310_POSITIVE_INTERVAL_MAPS": "PROVED_EXACT_FINITE",
            "TPC310_WEIGHTED_MEAN_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC310_AGGREGATION_ATLAS":
                "NUMERICALLY_REPRODUCED_FINITE_49_SELECTORS_147_AGGREGATES",
            "TPC310_FULL_SELECTOR_REVERSAL":
                "NUMERICALLY_REPRODUCED_FINITE_POOLED_RIGHT_BALANCED_LEFT_GEOMETRIC_RIGHT",
            "TPC310_PROFILE_ROBUSTNESS":
                "REFUTED_FINITE_NO_UNIVERSAL_AGGREGATION_CLASS",
            "TPC310_TARGET_GENERATION_LEAKAGE":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "TPC310_CAUSAL_IDENTIFICATION": "NONE_AGGREGATION_DIAGNOSTIC_ONLY",
            "TPC310_FORMAL_INTERVAL_CERTIFICATE":
                "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "TPC310_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC310_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC310_FIXED_POWER_CREDIT": 0,
            "TPC310_FULL_GATE_B": "OPEN",
            "TPC310_TWIN_PRIME_RESULT": "NONE",
            "TPC310_STATUS": STATUS,
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
    print("TPC310_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["selectors"] == 49 and
         audit["aggregate_observations"] == 147,
         "finite audit")
    print("TPC310_CERTIFICATE=PASS selectors=49 aggregates=147 "
          "classes=POOLED_R42_L1_U6,BALANCED_R1_L32_U16,"
          "GEOMETRIC_R26_L0_U23")


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
        print("TPC310_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
