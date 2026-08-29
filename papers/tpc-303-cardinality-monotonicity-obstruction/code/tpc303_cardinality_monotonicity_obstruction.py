#!/usr/bin/env python3
"""Finite fixed-source cardinality-monotonicity obstruction for TPC-303.

TPC-302 showed that a weighted/positive budget *gap* survives its growing
grid.  This release asks the stronger and different question whether the
weighted native budget itself grows monotonically with shell cardinality.
It freezes source scale, height, comparison cutoff, tolerance, exponent, and
normalization, then checks the Q=50,60,70,90 spine.  Certified interval
descents refute cardinality-only monotonicity on this declared finite path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

getcontext().prec = 80

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/code/"
    "tpc302_growing_shell_budget_gap_audit.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/results/"
    "tpc302_certificate.json")
RESULT = PROJECT / "results/tpc303_certificate.json"

PARENT_CODE_SHA256 = (
    "1edd94f87af501e59ddaa07a6f2c9a5d458d7cb28e0623064f51bfb3d10ae517")
PARENT_RESULT_SHA256 = (
    "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6")
STATUS = (
    "PROVED_EXACT_INTERVAL_DESCENT_CRITERION_PLUS_NUMERICALLY_CERTIFIED_"
    "FIXED_SOURCE_CARDINALITY_MONOTONICITY_OBSTRUCTION")
SCHEMA = "TPC303_CARDINALITY_MONOTONICITY_OBSTRUCTION_V1"
ROUND2_CLUE = (
    "LOCALIZE_BUDGET_DESCENTS_BY_TRANSPORTING_SIGN_LABELS_ACROSS_"
    "OVERLAPPING_SHELLS")

Q_SPINE = (50, 60, 70, 90)
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")


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


def decimal_text(value: Decimal) -> str:
    return format(value, ".38g")


def interval(value: object) -> tuple[Decimal, Decimal]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lower, upper = Decimal(value[0]), Decimal(value[1])
    need(Decimal(0) < lower <= upper, "positive ordered interval")
    return lower, upper


def parent_data() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-302 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-302 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC-302 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_FINITE_SOURCE_FIRST_SIGN_ENUMERATION"),
         "TPC-302 status")
    payload = data.get("payload", {})
    need(payload.get("schema") == "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1",
         "TPC-302 schema")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 34 and
         audit.get("explicit_shell_target_count") == 430 and
         audit.get("frontier_cases") == 612,
         "TPC-302 census")
    return data


def source_rows(data: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    selected: dict[tuple[int, int], dict[str, Any]] = {}
    for row in data["payload"]["rows"]:
        if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512 and
                row.get("H") == 58 and
                row.get("comparison_cutoff_z") == 5 and
                row.get("Q") in Q_SPINE and
                row.get("kernel_exponent") in EXPONENTS):
            key = (int(row["Q"]), int(row["kernel_exponent"]))
            need(key not in selected, "duplicate spine row")
            selected[key] = row
    need(len(selected) == len(Q_SPINE) * len(EXPONENTS),
         "spine row census")
    return selected


def point(row: dict[str, Any], tau: str, normalizer: str) -> dict[str, Any]:
    audit = row["tolerance_audits"][tau]
    context = audit["contexts"]["common_prefix"]
    target = context["targets"]["weighted"]
    value = target["budget_over_normalizer"][normalizer]
    lower, upper = interval(value)
    need(target["k"] == context["k_by_target"]["weighted"] ==
         context["k_by_target"]["positive"], "common prefix lock")
    return {
        "Q": int(row["Q"]),
        "shell_cardinality": int(row["shell_cardinality"]),
        "shell": row["shell"],
        "common_prefix_k": int(target["k"]),
        "common_prefix_cutoff": int(target["cutoff"]),
        "budget_interval": [str(value[0]), str(value[1])],
        "budget_centre": decimal_text((lower + upper) / 2),
    }


def transition(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_lo, left_hi = interval(left["budget_interval"])
    right_lo, right_hi = interval(right["budget_interval"])
    ratio_lo = right_lo / left_hi
    ratio_hi = right_hi / left_lo
    if right_hi < left_lo:
        classification = "DESCENT_CERTIFIED"
    elif right_lo > left_hi:
        classification = "ASCENT_CERTIFIED"
    else:
        classification = "OVERLAP_UNRESOLVED"
    return {
        "from_Q": left["Q"], "to_Q": right["Q"],
        "from_shell_cardinality": left["shell_cardinality"],
        "to_shell_cardinality": right["shell_cardinality"],
        "from_prefix_k": left["common_prefix_k"],
        "to_prefix_k": right["common_prefix_k"],
        "same_prefix": left["common_prefix_k"] == right["common_prefix_k"],
        "classification": classification,
        "right_over_left_interval": [decimal_text(ratio_lo),
                                     decimal_text(ratio_hi)],
        "strict_interval_margin": decimal_text(
            left_lo - right_hi if classification == "DESCENT_CERTIFIED"
            else right_lo - left_hi if classification == "ASCENT_CERTIFIED"
            else Decimal(0)),
    }


def build_payload() -> dict[str, Any]:
    data = parent_data()
    rows = source_rows(data)
    series = []
    all_transitions = []
    for exponent in EXPONENTS:
        for tau in TAUS:
            for normalizer in NORMALIZERS:
                points = [point(rows[(q, exponent)], tau, normalizer)
                          for q in Q_SPINE]
                need([item["shell_cardinality"] for item in points] ==
                     [10, 13, 15, 17], "cardinality spine")
                transitions = [transition(points[i], points[i + 1])
                               for i in range(len(points) - 1)]
                descents = sum(item["classification"] == "DESCENT_CERTIFIED"
                               for item in transitions)
                ascents = sum(item["classification"] == "ASCENT_CERTIFIED"
                              for item in transitions)
                unresolved = len(transitions) - descents - ascents
                series.append({
                    "kernel_exponent": exponent,
                    "tau": tau,
                    "normalizer": normalizer,
                    "points": points,
                    "transitions": transitions,
                    "certified_descents": descents,
                    "certified_ascents": ascents,
                    "unresolved_transitions": unresolved,
                    "cardinality_monotone_nondecreasing": descents == 0,
                    "nonmonotone_certified": descents > 0 and ascents > 0,
                })
                for item in transitions:
                    all_transitions.append({
                        "kernel_exponent": exponent, "tau": tau,
                        "normalizer": normalizer, **item})

    descents = [item for item in all_transitions
                if item["classification"] == "DESCENT_CERTIFIED"]
    ascents = [item for item in all_transitions
               if item["classification"] == "ASCENT_CERTIFIED"]
    unresolved = [item for item in all_transitions
                  if item["classification"] == "OVERLAP_UNRESOLVED"]
    same_prefix_descents = [item for item in descents if item["same_prefix"]]
    need(len(series) == 18 and len(all_transitions) == 54,
         "series/transition census")
    need(len(descents) == 21 and len(ascents) == 33 and not unresolved,
         "transition classification census")
    need(sum(item["nonmonotone_certified"] for item in series) == 18,
         "all-series nonmonotonicity")
    need(len(same_prefix_descents) == 9, "same-prefix descent census")
    strongest = min(descents, key=lambda item: (
        Decimal(item["right_over_left_interval"][1]),
        item["kernel_exponent"], item["tau"], item["normalizer"]))
    strongest_same = min(same_prefix_descents, key=lambda item: (
        Decimal(item["right_over_left_interval"][1]),
        item["kernel_exponent"], item["tau"], item["normalizer"]))
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc302_code_sha256": PARENT_CODE_SHA256,
            "tpc302_result_sha256": PARENT_RESULT_SHA256,
            "tpc302_rows": 34,
            "tpc302_shell_targets": 430,
        },
        "exact_theorem": {
            "interval_descent": (
                "for positive enclosures [L_j,U_j], U_(j+1)<L_j proves "
                "B_(j+1)<B_j for every represented value"),
            "interval_ascent": (
                "L_(j+1)>U_j proves B_(j+1)>B_j"),
            "finite_refutation": (
                "one certified descent refutes a nondecreasing "
                "cardinality-only law on the declared finite spine"),
            "same_prefix_firewall": (
                "a descent with equal common-prefix indices cannot be "
                "attributed to changing profile dimension"),
            "scope": (
                "fixed scale=512, H=58, source cutoff=5, Q in "
                "{50,60,70,90}; finite and non-asymptotic"),
        },
        "audit_definition": {
            "scale": 512, "H": 58, "comparison_cutoff_z": 5,
            "Q_spine": list(Q_SPINE),
            "shell_cardinality_spine": [10, 13, 15, 17],
            "kernel_exponents": list(EXPONENTS),
            "tolerances": list(TAUS),
            "normalizers": list(NORMALIZERS),
            "object": "TPC-302 common-prefix weighted native budget",
        },
        "finite_audit": {
            "series": len(series),
            "adjacent_transitions": len(all_transitions),
            "certified_descents": len(descents),
            "certified_ascents": len(ascents),
            "unresolved_transitions": len(unresolved),
            "nonmonotone_series": sum(item["nonmonotone_certified"]
                                      for item in series),
            "same_prefix_descents": len(same_prefix_descents),
            "strongest_descent": strongest,
            "strongest_same_prefix_descent": strongest_same,
            "uniform_asymptotic_budget_theorem": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
        },
        "series": series,
        "firewall": {
            "TPC303_INTERVAL_DESCENT_CRITERION": "PROVED_EXACT_FINITE",
            "TPC303_CARDINALITY_MONOTONICITY":
                "REFUTED_SCOPED_DECLARED_FINITE_SPINE",
            "TPC303_ALL_SERIES_NONMONOTONE":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18",
            "TPC303_SAME_PREFIX_DESCENTS":
                "NUMERICALLY_CERTIFIED_FINITE_9",
            "TPC303_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC303_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC303_FIXED_POWER_CREDIT": 0,
            "TPC303_FULL_GATE_B": "OPEN",
            "TPC303_TWIN_PRIME_RESULT": "NONE",
            "TPC303_STATUS": STATUS,
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
    need(data == document(), "certificate reproducibility")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    print("TPC303_CERTIFICATE=PASS series={} transitions={} descents={} "
          "ascents={} same_prefix_descents={} nonmonotone={}".format(
              audit["series"], audit["adjacent_transitions"],
              audit["certified_descents"], audit["certified_ascents"],
              audit["same_prefix_descents"], audit["nonmonotone_series"]))


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
        print("TPC303_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
