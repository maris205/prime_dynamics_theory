#!/usr/bin/env python3
"""Gauge-invariant overlap transport of TPC-302 sign labels for TPC-304.

TPC-303 found a fixed-source cardinality-monotonicity obstruction but did not
separate movement of the physical shell from movement of its source-first
weighted sign target.  This release performs the first exact crosswalk: it
restricts adjacent shell labels to their common primes, aligns the unavoidable
global sign, and compares the resulting transport defect with the TPC-303
budget-transition census.  The output is a finite localization certificate,
not a causal or asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

getcontext().prec = 80

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
RESULT = PROJECT / "results/tpc304_certificate.json"

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
    "PROVED_EXACT_FINITE_GAUGE_INVARIANT_OVERLAP_CORRELATION_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_LABEL_TRANSPORT_FRACTURE_AND_BUDGET_"
    "DESCENT_LOCALIZATION")
SCHEMA = "TPC304_OVERLAPPING_SHELL_LABEL_TRANSPORT_V1"
ROUND2_CLUE = (
    "COMPUTE_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGETS_TO_SEPARATE_TARGET_"
    "SWITCHING_FROM_OPERATOR_CHANGE")

Q_SPINE = (50, 60, 70, 90)
ADJACENT_PAIRS = tuple(zip(Q_SPINE[:-1], Q_SPINE[1:]))
EXPONENTS = (1, 2)
FRACTURE_CORRELATION_THRESHOLD = Fraction(1, 3)


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


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "fraction": fraction_text(value),
        "decimal": format(
            Decimal(value.numerator) / Decimal(value.denominator), ".28g"),
    }


def read_locked_json(path: Path, expected_hash: str, expected_status: str,
                     expected_schema: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " provenance")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == expected_status,
         path.name + " status")
    payload = data.get("payload", {})
    need(payload.get("schema") == expected_schema, path.name + " schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), path.name + " payload hash")
    return data


def parent_data() -> tuple[dict[str, Any], dict[str, Any]]:
    need(digest(TPC302_CODE.read_bytes()) == TPC302_CODE_SHA256,
         "TPC-302 code provenance")
    need(digest(TPC303_CODE.read_bytes()) == TPC303_CODE_SHA256,
         "TPC-303 code provenance")
    data302 = read_locked_json(
        TPC302_RESULT, TPC302_RESULT_SHA256, TPC302_STATUS,
        "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1")
    data303 = read_locked_json(
        TPC303_RESULT, TPC303_RESULT_SHA256, TPC303_STATUS,
        "TPC303_CARDINALITY_MONOTONICITY_OBSTRUCTION_V1")
    need(data302["payload"]["finite_audit"]["rows"] == 34,
         "TPC-302 row census")
    audit303 = data303["payload"]["finite_audit"]
    need(audit303["series"] == 18 and
         audit303["adjacent_transitions"] == 54 and
         audit303["certified_descents"] == 21 and
         audit303["certified_ascents"] == 33 and
         audit303["same_prefix_descents"] == 9,
         "TPC-303 transition census")
    return data302, data303


def source_rows(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    selected: dict[tuple[int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512 and
                row.get("H") == 58 and
                row.get("comparison_cutoff_z") == 5 and
                row.get("Q") in Q_SPINE and
                row.get("kernel_exponent") in EXPONENTS):
            key = (int(row["Q"]), int(row["kernel_exponent"]))
            need(key not in selected, "duplicate fixed-source label row")
            shell = row.get("shell", [])
            labels = row.get("weighted_target_label", [])
            need(shell == sorted(shell) and len(shell) == len(set(shell)),
                 "ordered distinct shell")
            need(len(labels) == len(shell) and labels[0] == 1 and
                 all(label in (-1, 1) for label in labels),
                 "signed target label")
            selected[key] = row
    need(len(selected) == len(Q_SPINE) * len(EXPONENTS),
         "fixed-source label-row census")
    return selected


def transport_row(left: dict[str, Any], right: dict[str, Any],
                  exponent: int) -> dict[str, Any]:
    left_map = dict(zip(left["shell"], left["weighted_target_label"]))
    right_map = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(left_map) & set(right_map))
    need(bool(overlap), "nonempty adjacent-shell overlap")
    left_labels = [int(left_map[prime]) for prime in overlap]
    right_labels = [int(right_map[prime]) for prime in overlap]
    raw_inner_product = sum(a * b for a, b in zip(left_labels, right_labels))
    alignment_sign = 1 if raw_inner_product >= 0 else -1
    aligned_right = [alignment_sign * value for value in right_labels]
    mismatch_primes = [prime for prime, a, b in zip(
        overlap, left_labels, aligned_right) if a != b]
    mismatch_count = len(mismatch_primes)
    match_count = len(overlap) - mismatch_count
    need(match_count >= mismatch_count, "optimal global-sign alignment")
    correlation = Fraction(abs(raw_inner_product), len(overlap))
    disagreement = Fraction(mismatch_count, len(overlap))
    need(disagreement == (1 - correlation) / 2,
         "correlation/disagreement identity")
    return {
        "kernel_exponent": exponent,
        "from_Q": int(left["Q"]),
        "to_Q": int(right["Q"]),
        "from_shell_cardinality": int(left["shell_cardinality"]),
        "to_shell_cardinality": int(right["shell_cardinality"]),
        "overlap_primes": overlap,
        "overlap_cardinality": len(overlap),
        "left_overlap_labels": left_labels,
        "right_overlap_labels": right_labels,
        "optimal_alignment_sign": alignment_sign,
        "aligned_right_overlap_labels": aligned_right,
        "raw_inner_product": raw_inner_product,
        "aligned_inner_product": abs(raw_inner_product),
        "aligned_matches": match_count,
        "aligned_mismatches": mismatch_count,
        "mismatch_primes": mismatch_primes,
        "aligned_correlation": fraction_record(correlation),
        "aligned_disagreement_fraction": fraction_record(disagreement),
        "fracture_at_correlation_one_third": (
            correlation <= FRACTURE_CORRELATION_THRESHOLD),
    }


def budget_crosswalk(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = {
        pair: [] for pair in ADJACENT_PAIRS}
    series = data["payload"]["series"]
    need(len(series) == 18, "TPC-303 series census")
    for item in series:
        for pair in ADJACENT_PAIRS:
            matches = [transition for transition in item["transitions"]
                       if (transition["from_Q"], transition["to_Q"]) == pair]
            need(len(matches) == 1, "unique TPC-303 adjacent transition")
            grouped[pair].append({
                "kernel_exponent": int(item["kernel_exponent"]),
                "tau": item["tau"],
                "normalizer": item["normalizer"],
                "classification": matches[0]["classification"],
                "same_prefix": bool(matches[0]["same_prefix"]),
            })
    answer: dict[tuple[int, int], dict[str, Any]] = {}
    for pair, transitions in grouped.items():
        need(len(transitions) == 18, "budget transition-group census")
        descents = sum(item["classification"] == "DESCENT_CERTIFIED"
                       for item in transitions)
        ascents = sum(item["classification"] == "ASCENT_CERTIFIED"
                      for item in transitions)
        unresolved = len(transitions) - descents - ascents
        same_prefix_descents = sum(
            item["classification"] == "DESCENT_CERTIFIED" and
            item["same_prefix"] for item in transitions)
        by_exponent = []
        for exponent in EXPONENTS:
            subset = [item for item in transitions
                      if item["kernel_exponent"] == exponent]
            exp_descents = sum(item["classification"] == "DESCENT_CERTIFIED"
                               for item in subset)
            exp_ascents = sum(item["classification"] == "ASCENT_CERTIFIED"
                              for item in subset)
            exp_unresolved = len(subset) - exp_descents - exp_ascents
            exp_same = sum(
                item["classification"] == "DESCENT_CERTIFIED" and
                item["same_prefix"] for item in subset)
            need(len(subset) == 9, "exponent transition-group census")
            by_exponent.append({
                "kernel_exponent": exponent,
                "certified_descents": exp_descents,
                "certified_ascents": exp_ascents,
                "unresolved": exp_unresolved,
                "same_prefix_descents": exp_same,
            })
        answer[pair] = {
            "certified_descents": descents,
            "certified_ascents": ascents,
            "unresolved": unresolved,
            "same_prefix_descents": same_prefix_descents,
            "descent_share": fraction_record(Fraction(descents, 18)),
            "by_exponent": by_exponent,
        }
    return answer


def build_payload() -> dict[str, Any]:
    data302, data303 = parent_data()
    rows = source_rows(data302)
    transports = []
    for exponent in EXPONENTS:
        for left_q, right_q in ADJACENT_PAIRS:
            transports.append(transport_row(
                rows[(left_q, exponent)], rows[(right_q, exponent)], exponent))
    need(len(transports) == 6, "transport-row census")
    budget = budget_crosswalk(data303)

    spine_crosswalk = []
    for left_q, right_q in ADJACENT_PAIRS:
        pair_rows = [row for row in transports
                     if (row["from_Q"], row["to_Q"]) == (left_q, right_q)]
        need(len(pair_rows) == 2, "two-exponent transport pair")
        correlations = [Fraction(
            row["aligned_correlation"]["numerator"],
            row["aligned_correlation"]["denominator"]) for row in pair_rows]
        disagreements = [Fraction(
            row["aligned_disagreement_fraction"]["numerator"],
            row["aligned_disagreement_fraction"]["denominator"])
                         for row in pair_rows]
        spine_crosswalk.append({
            "from_Q": left_q,
            "to_Q": right_q,
            "overlap_cardinality_by_exponent": [
                row["overlap_cardinality"] for row in pair_rows],
            "aligned_correlation_by_exponent": [
                row["aligned_correlation"] for row in pair_rows],
            "mean_aligned_correlation": fraction_record(
                sum(correlations, Fraction()) / len(correlations)),
            "mean_aligned_disagreement_fraction": fraction_record(
                sum(disagreements, Fraction()) / len(disagreements)),
            "fracture_rows": sum(
                row["fracture_at_correlation_one_third"]
                for row in pair_rows),
            "budget_transition_census": budget[(left_q, right_q)],
        })

    expected = {
        (50, 60): (Fraction(1, 2), 0, 3, 15, 0),
        (60, 70): (Fraction(1, 11), 2, 15, 3, 9),
        (70, 90): (Fraction(1, 2), 0, 3, 15, 0),
    }
    for item in spine_crosswalk:
        pair = (item["from_Q"], item["to_Q"])
        mean = Fraction(item["mean_aligned_correlation"]["numerator"],
                        item["mean_aligned_correlation"]["denominator"])
        wanted = expected[pair]
        census = item["budget_transition_census"]
        need(mean == wanted[0] and item["fracture_rows"] == wanted[1] and
             census["certified_descents"] == wanted[2] and
             census["certified_ascents"] == wanted[3] and
             census["same_prefix_descents"] == wanted[4] and
             census["unresolved"] == 0,
             "declared transport/budget crosswalk")

    correlation_min = min(spine_crosswalk, key=lambda item: Fraction(
        item["mean_aligned_correlation"]["numerator"],
        item["mean_aligned_correlation"]["denominator"]))
    descent_max = max(spine_crosswalk, key=lambda item:
                      item["budget_transition_census"]["certified_descents"])
    same_prefix_support = [item for item in spine_crosswalk
                           if item["budget_transition_census"][
                               "same_prefix_descents"] > 0]
    need((correlation_min["from_Q"], correlation_min["to_Q"]) == (60, 70),
         "unique transport minimum")
    need((descent_max["from_Q"], descent_max["to_Q"]) == (60, 70),
         "unique descent maximum")
    need(len(same_prefix_support) == 1 and
         (same_prefix_support[0]["from_Q"],
          same_prefix_support[0]["to_Q"]) == (60, 70),
         "same-prefix descent localization")
    need(sum(item["fracture_at_correlation_one_third"]
             for item in transports) == 2, "fracture-row census")

    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc302_code_sha256": TPC302_CODE_SHA256,
            "tpc302_result_sha256": TPC302_RESULT_SHA256,
            "tpc303_code_sha256": TPC303_CODE_SHA256,
            "tpc303_result_sha256": TPC303_RESULT_SHA256,
            "tpc302_source_rows": 8,
            "tpc303_series": 18,
            "tpc303_adjacent_transitions": 54,
        },
        "audit_definition": {
            "source_scale": 512,
            "height": 58,
            "comparison_cutoff_z": 5,
            "Q_spine": list(Q_SPINE),
            "kernel_exponents": list(EXPONENTS),
            "global_sign_alignment": (
                "choose epsilon in {-1,+1} maximizing overlap agreement"),
            "aligned_correlation": (
                "absolute overlap label inner product divided by overlap cardinality"),
            "aligned_disagreement_fraction": (
                "minimum mismatch count over the two global signs divided by overlap cardinality"),
            "fracture_modeling_threshold": "aligned correlation <= 1/3",
        },
        "exact_theorem": {
            "global_sign_invariance": (
                "absolute normalized overlap inner product is invariant under independent global label flips"),
            "correlation_disagreement_identity": (
                "d_align=(1-rho_align)/2 for labels in {-1,+1} on a nonempty overlap"),
            "finite_argmin_argmax_crosswalk": (
                "the unique minimum-correlation Q transition can be compared exactly with the finite budget census"),
            "scope": (
                "fixed source scale and declared moving-shell spine; no causal or asymptotic inference"),
        },
        "transport_rows": transports,
        "spine_crosswalk": spine_crosswalk,
        "finite_audit": {
            "transport_rows": 6,
            "adjacent_Q_groups": 3,
            "fracture_rows_at_one_third": 2,
            "unique_fracture_transition": [60, 70],
            "fracture_mean_correlation": fraction_record(Fraction(1, 11)),
            "nonfracture_mean_correlation_each_group": fraction_record(
                Fraction(1, 2)),
            "budget_descents_by_Q_group": [3, 15, 3],
            "budget_ascents_by_Q_group": [15, 3, 15],
            "same_prefix_descents_by_Q_group": [0, 9, 0],
            "fracture_to_each_nonfracture_descent_count_ratio":
                fraction_record(Fraction(5, 1)),
            "minimum_correlation_and_maximum_descent_coincide": True,
            "all_same_prefix_descents_localized_at_fracture": True,
            "causal_target_operator_separation": "OPEN",
            "uniform_asymptotic_budget_theorem": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
        },
        "firewall": {
            "TPC304_OVERLAP_CORRELATION_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC304_GLOBAL_SIGN_GAUGE_INVARIANCE": "PROVED_EXACT_FINITE",
            "TPC304_LABEL_TRANSPORT_CROSSWALK": "NUMERICALLY_CERTIFIED_FINITE_6_ROWS",
            "TPC304_TRANSPORT_FRACTURE": "NUMERICALLY_CERTIFIED_FINITE_Q60_TO_70_2_OF_2_EXPONENTS",
            "TPC304_BUDGET_DESCENT_LOCALIZATION": "NUMERICALLY_CERTIFIED_FINITE_15_3_3_AND_SAME_PREFIX_9_0_0",
            "TPC304_CAUSAL_SEPARATION": "OPEN",
            "TPC304_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC304_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC304_FIXED_POWER_CREDIT": 0,
            "TPC304_FULL_GATE_B": "OPEN",
            "TPC304_TWIN_PRIME_RESULT": "NONE",
            "TPC304_STATUS": STATUS,
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
    print("TPC304_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    need(audit["transport_rows"] == 6 and
         audit["fracture_rows_at_one_third"] == 2 and
         audit["budget_descents_by_Q_group"] == [3, 15, 3] and
         audit["same_prefix_descents_by_Q_group"] == [0, 9, 0] and
         audit["minimum_correlation_and_maximum_descent_coincide"] is True and
         audit["fixed_power_credit"] == 0,
         "certificate audit")
    print("TPC304_CERTIFICATE=PASS transport_rows=6 fracture_rows=2 "
          "mean_correlations=1/2,1/11,1/2 budget_descents=3,15,3 "
          "same_prefix_descents=0,9,0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one of --write or --check")
    if args.write:
        write()
    else:
        check()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError, json.JSONDecodeError) as error:
        print("TPC304_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
