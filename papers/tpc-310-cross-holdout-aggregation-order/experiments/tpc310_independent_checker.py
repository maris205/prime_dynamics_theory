#!/usr/bin/env python3
"""Independent replay for the TPC-310 aggregation-order atlas.

This checker intentionally does not import the TPC-310 producer.  It parses the
locked TPC-309 interval atlas, reconstructs all 49 selectors, recomputes the
three aggregation maps with an independent float implementation, and checks
the stored classes, census, and headline reversal.  It is a finite replay
check, not a directed-rounding certificate.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-310-cross-holdout-aggregation-order"
RESULT = PROJECT / "results/tpc310_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-309-profile-prefix-shift-sensitivity/code/"
    "tpc309_profile_prefix_shift_sensitivity.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-309-profile-prefix-shift-sensitivity/results/"
    "tpc309_certificate.json")

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
LADDERS = ("LOW", "BASE", "HIGH")
RADII = (0, 1, 2)
MODES = ("POOLED_MSE", "BALANCED_RATIO", "GEOMETRIC_RATIO")
SLACK_RELATIVE = 5e-8


class Failure(RuntimeError):
    """A fail-closed replay error."""


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def load(path: Path, expected_hash: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    if expected_hash is not None:
        need(digest(raw) == expected_hash, path.name + " provenance")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1, path.name + " version")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def interval(value: Any) -> tuple[float, float]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = float(value[0]), float(value[1])
    need(math.isfinite(lo) and math.isfinite(hi) and 0 < lo <= hi,
         "positive finite interval")
    return lo, hi


def close(stored: Any, expected: tuple[float, float], label: str) -> None:
    lo, hi = interval(stored)
    for actual, target in zip((lo, hi), expected):
        margin = SLACK_RELATIVE * max(abs(target), 1e-12) + 1e-12
        need(abs(actual - target) <= margin, label + " interval")


def classify(bounds: tuple[float, float]) -> str:
    lo, hi = bounds
    if hi < 0.9:
        return "RIGHT_COMPLETION_LOWER"
    if lo > 1.1:
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


def parent_observations(parent: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for case in parent["payload"]["cases"]:
        case_key = (case["profile_ladder"], int(case["from_Q"]),
                    int(case["to_Q"]), int(case["kernel_exponent"]),
                    case["tau"])
        for envelope in case["envelopes"]:
            key = case_key + (int(envelope["radius"]),)
            need(key not in seen, "duplicate parent key")
            seen.add(key)
            ratio_lo, ratio_hi = interval(
                envelope["holdout_right_over_left_interval"])
            right = envelope["right_completion"]
            left = envelope["left_completion"]
            rmin = interval(right["envelope_min_mse"])
            rmax = interval(right["envelope_max_mse"])
            lmin = interval(left["envelope_min_mse"])
            lmax = interval(left["envelope_max_mse"])
            need(rmin[0] <= rmin[1] <= rmax[1], "right extrema")
            need(lmin[0] <= lmin[1] <= lmax[1], "left extrema")
            rows.append({"key": key, "ladder": case["profile_ladder"],
                         "radius": int(envelope["radius"]),
                         "ratio_lo": ratio_lo, "ratio_hi": ratio_hi,
                         "right_min_lo": rmin[0], "right_max_hi": rmax[1],
                         "left_min_lo": lmin[0], "left_max_hi": lmax[1]})
    need(len(rows) == 162 and len(seen) == 162, "parent observation census")
    return rows


def budget_vote(parent: dict[str, Any], ladder_subset: tuple[str, ...]
                ) -> tuple[str, dict[str, int]]:
    counts = {"RIGHT_COMPLETION_LOWER": 0,
              "LEFT_COMPLETION_LOWER": 0,
              "PREFERENCE_UNRESOLVED": 0}
    for case in parent["payload"]["cases"]:
        if case["profile_ladder"] in ladder_subset:
            counts[case["profile_budget_preference"]] += 1
    top = sorted(counts.values(), reverse=True)
    if top[0] == 0 or (len(top) > 1 and top[0] == top[1]):
        return "PREFERENCE_UNRESOLVED", counts
    return max(counts, key=counts.get), counts


def aggregate(rows: list[dict[str, Any]], mode: str
              ) -> tuple[float, float]:
    need(rows and mode in MODES, "aggregate input")
    n = len(rows)
    if mode == "POOLED_MSE":
        return (sum(row["right_min_lo"] for row in rows) /
                sum(row["left_max_hi"] for row in rows),
                sum(row["right_max_hi"] for row in rows) /
                sum(row["left_min_lo"] for row in rows))
    if mode == "BALANCED_RATIO":
        return (sum(row["ratio_lo"] for row in rows) / n,
                sum(row["ratio_hi"] for row in rows) / n)
    return (math.exp(sum(math.log(row["ratio_lo"]) for row in rows) / n),
            math.exp(sum(math.log(row["ratio_hi"]) for row in rows) / n))


def selector_key(selector: dict[str, Any]) -> tuple[tuple[str, ...], tuple[int, ...]]:
    return (tuple(selector["ladder_subset"]),
            tuple(int(x) for x in selector["radius_subset"]))


def main() -> int:
    try:
        need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
             "parent code provenance")
        parent = load(PARENT_RESULT, PARENT_RESULT_SHA256)
        need(parent["claim_status"] == PARENT_STATUS, "parent status")
        parent_payload = parent["payload"]
        need(parent_payload["schema"] ==
             "TPC309_THREE_WINDOW_PROFILE_PREFIX_SHIFT_AUDIT_V1",
             "parent schema")
        child = load(RESULT)
        need(child.get("claim_status") == STATUS, "child status")
        payload = child["payload"]
        need(payload.get("schema") == SCHEMA, "child schema")
        need(payload.get("parent_lock") == {
            "tpc309_code_sha256": PARENT_CODE_SHA256,
            "tpc309_result_sha256": PARENT_RESULT_SHA256,
            "tpc309_profile_cases": 54,
            "tpc309_envelope_observations": 162,
        }, "parent lock")
        protocol = payload["protocol"]
        need(protocol["ladders"] == list(LADDERS) and
             protocol["radii"] == list(RADII) and
             protocol["aggregation_modes"] == list(MODES) and
             protocol["selector_count"] == 49, "protocol")

        observations = parent_observations(parent)
        expected_keys = {(ls, rs) for ls in subsets(LADDERS)
                         for rs in subsets(RADII)}
        stored_selectors = payload["selectors"]
        need(len(stored_selectors) == 49, "selector count")
        stored_by_key = {selector_key(s): s for s in stored_selectors}
        need(len(stored_by_key) == 49 and
             set(stored_by_key) == expected_keys, "selector coverage")

        class_counts = {mode: {"RIGHT_COMPLETION_LOWER": 0,
                               "LEFT_COMPLETION_LOWER": 0,
                               "PREFERENCE_UNRESOLVED": 0}
                        for mode in MODES}
        agreement_counts = {mode: {"CONCORDANT": 0, "DISCORDANT": 0,
                                   "UNRESOLVED": 0} for mode in MODES}
        pair_counts: dict[str, dict[str, int]] = {
            "POOLED_MSE_vs_BALANCED_RATIO": {},
            "POOLED_MSE_vs_GEOMETRIC_RATIO": {},
            "BALANCED_RATIO_vs_GEOMETRIC_RATIO": {},
        }
        for ls, rs in sorted(expected_keys,
                             key=lambda x: (len(x[0]), x[0], len(x[1]), x[1])):
            selected = [row for row in observations
                        if row["ladder"] in ls and row["radius"] in rs]
            selector = stored_by_key[(ls, rs)]
            need(selector["observation_count"] == len(selected) and
                 len(selected) == 18 * len(ls) * len(rs),
                 "selector size")
            vote, counts = budget_vote(parent, ls)
            need(selector["budget_vote"] == vote and
                 selector["budget_counts"] == counts, "budget vote")
            stored_modes = {item["mode"]: item
                            for item in selector["aggregates"]}
            need(set(stored_modes) == set(MODES), "mode coverage")
            for mode in MODES:
                item = stored_modes[mode]
                expected = aggregate(selected, mode)
                close(item["ratio_interval"], expected,
                      mode + " " + str((ls, rs)))
                expected_class = classify(expected)
                need(item["class"] == expected_class and
                     item["budget_vote"] == vote and
                     item["budget_agreement"] == agreement(vote, expected_class),
                     mode + " classification")
                class_counts[mode][expected_class] += 1
                agreement_counts[mode][item["budget_agreement"]] += 1
            classes = {mode: stored_modes[mode]["class"] for mode in MODES}
            for first, second, name in (
                    ("POOLED_MSE", "BALANCED_RATIO",
                     "POOLED_MSE_vs_BALANCED_RATIO"),
                    ("POOLED_MSE", "GEOMETRIC_RATIO",
                     "POOLED_MSE_vs_GEOMETRIC_RATIO"),
                    ("BALANCED_RATIO", "GEOMETRIC_RATIO",
                     "BALANCED_RATIO_vs_GEOMETRIC_RATIO")):
                key = classes[first] + "|" + classes[second]
                pair_counts[name][key] = pair_counts[name].get(key, 0) + 1

        expected_classes = {
            "POOLED_MSE": {"RIGHT_COMPLETION_LOWER": 42,
                           "LEFT_COMPLETION_LOWER": 1,
                           "PREFERENCE_UNRESOLVED": 6},
            "BALANCED_RATIO": {"RIGHT_COMPLETION_LOWER": 1,
                               "LEFT_COMPLETION_LOWER": 32,
                               "PREFERENCE_UNRESOLVED": 16},
            "GEOMETRIC_RATIO": {"RIGHT_COMPLETION_LOWER": 26,
                                 "LEFT_COMPLETION_LOWER": 0,
                                 "PREFERENCE_UNRESOLVED": 23},
        }
        need(class_counts == expected_classes, "class census")
        need(payload["finite_audit"]["class_counts_by_mode"] == class_counts and
             payload["finite_audit"]["agreement_counts_by_mode"] == agreement_counts and
             payload["finite_audit"]["pairwise_class_counts"] == pair_counts,
             "stored aggregate census")

        full = stored_by_key[(LADDERS, RADII)]
        full_modes = {row["mode"]: row for row in full["aggregates"]}
        need({mode: full_modes[mode]["class"] for mode in MODES} == {
            "POOLED_MSE": "RIGHT_COMPLETION_LOWER",
            "BALANCED_RATIO": "LEFT_COMPLETION_LOWER",
            "GEOMETRIC_RATIO": "RIGHT_COMPLETION_LOWER",
        }, "headline reversal")
        need(payload["finite_audit"]["full_selector_classes"] == {
            "POOLED_MSE": "RIGHT_COMPLETION_LOWER",
            "BALANCED_RATIO": "LEFT_COMPLETION_LOWER",
            "GEOMETRIC_RATIO": "RIGHT_COMPLETION_LOWER",
        }, "headline record")
        audit = payload["finite_audit"]
        need(audit["parent_profile_cases"] == 54 and
             audit["parent_envelope_observations"] == 162 and
             audit["parent_candidate_evaluations"] == 2106 and
             audit["ladder_subset_count"] == 7 and
             audit["radius_subset_count"] == 7 and
             audit["selectors"] == 49 and
             audit["aggregate_observations"] == 147 and
             audit["fixed_power_credit"] == 0 and
             audit["full_gate_b"] == "OPEN" and
             audit["twin_prime_result"] == "NONE",
             "finite audit")
        need(audit["target_generation_leakage"] ==
             "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS" and
             audit["formal_interval_certificate"] ==
             "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING" and
             audit["causal_identification"] == "NONE_AGGREGATION_DIAGNOSTIC_ONLY",
             "claim firewall")
        print("TPC310_INDEPENDENT_CHECK=PASS selectors=49 aggregates=147 "
              "pooled=R42/L1/U6 balanced=R1/L32/U16 geometric=R26/L0/U23")
        return 0
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            OverflowError, ZeroDivisionError) as error:
        print("TPC310_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
