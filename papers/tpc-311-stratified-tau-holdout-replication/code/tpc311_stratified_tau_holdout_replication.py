#!/usr/bin/env python3
"""TPC-311: declared stratification and tau-slice holdout replication.

TPC-310 showed that pooling and equal-row aggregation can reverse a finite
preference class.  This child therefore freezes one two-stage design rule:

1. within each (transition, exponent, tau, radius) stratum, pool the three
   LOW/BASE/HIGH profile-ladder completion extrema before taking a ratio;
2. give the resulting design strata equal arithmetic weight.

The calibration slice is tau in {0.25, 0.5}; tau=0.75 is held out as a
confirmation slice.  Radius zero is the primary native-completion endpoint,
and radii 1--2 are declared stress controls.  This is a finite parameter-slice
audit on one locked parent atlas, not a fresh physical sample, an externally
timestamped preregistration, or an arithmetic/asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

import mpmath as mp

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
TPC310_CODE = ROOT / (
    "papers/tpc-310-cross-holdout-aggregation-order/code/"
    "tpc310_cross_holdout_aggregation_order.py")
TPC310_RESULT = ROOT / (
    "papers/tpc-310-cross-holdout-aggregation-order/results/"
    "tpc310_certificate.json")
TPC309_CODE = ROOT / (
    "papers/tpc-309-profile-prefix-shift-sensitivity/code/"
    "tpc309_profile_prefix_shift_sensitivity.py")
TPC309_RESULT = ROOT / (
    "papers/tpc-309-profile-prefix-shift-sensitivity/results/"
    "tpc309_certificate.json")
RESULT = PROJECT / "results/tpc311_certificate.json"

TPC310_CODE_SHA256 = (
    "a3d47a7349d52ed94ac92d1a6c151a537d4655ab50947a0050a994318965882a")
TPC310_RESULT_SHA256 = (
    "5bb814e86e742752678d36925e5f719f0b7f998eac76b6c113913aa716f97866")
TPC309_CODE_SHA256 = (
    "2284d9ccfcadd02eb5e82a301bdbfa85013e3e9a8352d8f3b078d020742890d9")
TPC309_RESULT_SHA256 = (
    "a4c8f7cd4aef327682b9457c21236f3756f454f4b82f5a901ab2933f1d4cad4a")
TPC310_STATUS = (
    "PROVED_EXACT_FINITE_CROSS_HOLDOUT_AGGREGATION_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_AGGREGATION_ORDER_OBSTRUCTION_ATLAS")
TPC309_STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS")
STATUS = (
    "PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS")
SCHEMA = "TPC311_STRATIFIED_TAU_SLICE_HOLDOUT_REPLICATION_V1"
ROUND2_CLUE = (
    "REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_LAW_"
    "BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM")

LADDERS = ("LOW", "BASE", "HIGH")
PAIRS = ((50, 60), (60, 70), (70, 90))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
CALIBRATION_TAUS = ("0.25", "0.5")
CONFIRMATION_TAUS = ("0.75",)
RADII = (0, 1, 2)
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


def interval(value: Any, label: str) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, label + " shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(0 < lo <= hi, label + " positive order")
    return lo, hi


def classify(bounds: tuple[mp.mpf, mp.mpf]) -> str:
    lo, hi = bounds
    if hi < CLASSIFY_BELOW:
        return "RIGHT_COMPLETION_LOWER"
    if lo > CLASSIFY_ABOVE:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def load_canonical(path: Path, expected_hash: str,
                   expected_status: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " provenance")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == expected_status,
         path.name + " header")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def locked_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    need(digest(TPC310_CODE.read_bytes()) == TPC310_CODE_SHA256,
         "TPC-310 code provenance")
    need(digest(TPC309_CODE.read_bytes()) == TPC309_CODE_SHA256,
         "TPC-309 code provenance")
    parent = load_canonical(TPC310_RESULT, TPC310_RESULT_SHA256, TPC310_STATUS)
    source = load_canonical(TPC309_RESULT, TPC309_RESULT_SHA256, TPC309_STATUS)
    need(parent["payload"].get("schema") ==
         "TPC310_CROSS_HOLDOUT_AGGREGATION_ORDER_AUDIT_V1",
         "TPC-310 schema")
    need(parent["payload"].get("round2_clue") ==
         "TEST_PREREGISTERED_STRATIFIED_WEIGHTS_AND_HOLDOUT_REPLICATION_"
         "BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM", "TPC-310 route clue")
    need(parent["payload"].get("parent_lock") == {
        "tpc309_code_sha256": TPC309_CODE_SHA256,
        "tpc309_result_sha256": TPC309_RESULT_SHA256,
        "tpc309_profile_cases": 54,
        "tpc309_envelope_observations": 162,
    }, "TPC-310 parent lock")
    need(source["payload"].get("schema") ==
         "TPC309_THREE_WINDOW_PROFILE_PREFIX_SHIFT_AUDIT_V1",
         "TPC-309 schema")
    audit = source["payload"].get("finite_audit", {})
    need(audit.get("profile_case_observations") == 54 and
         audit.get("envelope_observations") == 162,
         "TPC-309 source census")
    return parent, source


def extract_observations(source: dict[str, Any]) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for case in source["payload"]["cases"]:
        ladder = case["profile_ladder"]
        pair = (int(case["from_Q"]), int(case["to_Q"]))
        exponent = int(case["kernel_exponent"])
        tau = case["tau"]
        need(ladder in LADDERS and pair in PAIRS and
             exponent in EXPONENTS and tau in TAUS, "source case key")
        for envelope in case["envelopes"]:
            radius = int(envelope["radius"])
            key = (pair, exponent, tau, radius, ladder)
            need(radius in RADII and key not in seen,
                 "source envelope key")
            seen.add(key)
            right = envelope["right_completion"]
            left = envelope["left_completion"]
            right_min = interval(right["envelope_min_mse"], "right minimum")
            right_max = interval(right["envelope_max_mse"], "right maximum")
            left_min = interval(left["envelope_min_mse"], "left minimum")
            left_max = interval(left["envelope_max_mse"], "left maximum")
            need(right_min[0] <= right_min[1] <= right_max[1],
                 "right extrema order")
            need(left_min[0] <= left_min[1] <= left_max[1],
                 "left extrema order")
            observations.append({
                "pair": pair,
                "exponent": exponent,
                "tau": tau,
                "radius": radius,
                "ladder": ladder,
                "right_min_lo": right_min[0],
                "right_max_hi": right_max[1],
                "left_min_lo": left_min[0],
                "left_max_hi": left_max[1],
            })
    need(len(observations) == 162 and len(seen) == 162,
         "source observation census")
    return observations


def profile_pool(observations: list[dict[str, Any]], pair: tuple[int, int],
                 exponent: int, tau: str, radius: int,
                 ladders: tuple[str, ...] = LADDERS) -> dict[str, Any]:
    selected = [row for row in observations
                if row["pair"] == pair and row["exponent"] == exponent and
                row["tau"] == tau and row["radius"] == radius and
                row["ladder"] in ladders]
    need(len(selected) == len(ladders), "profile stratum coverage")
    right_lower = mp.fsum(row["right_min_lo"] for row in selected)
    right_upper = mp.fsum(row["right_max_hi"] for row in selected)
    left_lower = mp.fsum(row["left_min_lo"] for row in selected)
    left_upper = mp.fsum(row["left_max_hi"] for row in selected)
    bounds = (right_lower / left_upper, right_upper / left_lower)
    need(0 < bounds[0] <= bounds[1], "profile-pooled interval")
    return {
        "from_Q": pair[0],
        "to_Q": pair[1],
        "kernel_exponent": exponent,
        "tau": tau,
        "radius": radius,
        "ladders": list(ladders),
        "parent_observation_count": len(selected),
        "ratio_interval": [emit(bounds[0]), emit(bounds[1])],
        "class": classify(bounds),
        "diagnostic": {
            "right_lower_sum": emit(right_lower),
            "right_upper_sum": emit(right_upper),
            "left_lower_sum": emit(left_lower),
            "left_upper_sum": emit(left_upper),
        },
    }


def stratified_block(observations: list[dict[str, Any]], name: str,
                     taus: tuple[str, ...], radii: tuple[int, ...],
                     pairs: tuple[tuple[int, int], ...] = PAIRS,
                     exponents: tuple[int, ...] = EXPONENTS,
                     ladders: tuple[str, ...] = LADDERS) -> dict[str, Any]:
    strata = [profile_pool(observations, pair, exponent, tau, radius,
                           ladders)
              for pair in pairs
              for exponent in exponents
              for tau in taus
              for radius in radii]
    need(bool(strata), "nonempty stratified block")
    lower = mp.fsum(mp.mpf(row["ratio_interval"][0])
                    for row in strata) / len(strata)
    upper = mp.fsum(mp.mpf(row["ratio_interval"][1])
                    for row in strata) / len(strata)
    bounds = (lower, upper)
    need(0 < lower <= upper, "stratified block interval")
    return {
        "name": name,
        "tau_subset": list(taus),
        "radius_subset": list(radii),
        "transition_subset": [list(pair) for pair in pairs],
        "exponent_subset": list(exponents),
        "ladder_subset": list(ladders),
        "stratum_count": len(strata),
        "parent_observation_count": len(strata) * len(ladders),
        "ratio_interval": [emit(lower), emit(upper)],
        "class": classify(bounds),
    }


def replication(calibration: dict[str, Any], confirmation: dict[str, Any]
                ) -> str:
    first = calibration["class"]
    second = confirmation["class"]
    strict = {"RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"}
    if first == second and first in strict:
        return "STRICT_CLASS_REPLICATED"
    if {first, second} == strict:
        return "STRICT_CLASS_REVERSED"
    return "NONREPLICATED_WITH_UNRESOLVED_SLICE"


def class_counts(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts = {"RIGHT_COMPLETION_LOWER": 0,
              "LEFT_COMPLETION_LOWER": 0,
              "PREFERENCE_UNRESOLVED": 0}
    for row in rows:
        counts[row["class"]] += 1
    return counts


def build_payload() -> dict[str, Any]:
    _, source = locked_inputs()
    observations = extract_observations(source)
    strata = [profile_pool(observations, pair, exponent, tau, radius)
              for pair in PAIRS
              for exponent in EXPONENTS
              for tau in TAUS
              for radius in RADII]
    need(len(strata) == 54, "stratum census")

    block_specs = (
        ("CALIBRATION_NATIVE", CALIBRATION_TAUS, (0,)),
        ("CONFIRMATION_NATIVE", CONFIRMATION_TAUS, (0,)),
        ("FULL_NATIVE", TAUS, (0,)),
        ("CALIBRATION_ALL_RADII", CALIBRATION_TAUS, RADII),
        ("CONFIRMATION_ALL_RADII", CONFIRMATION_TAUS, RADII),
        ("FULL_ALL_RADII", TAUS, RADII),
    )
    blocks = [stratified_block(observations, name, taus, radii)
              for name, taus, radii in block_specs]
    by_name = {row["name"]: row for row in blocks}
    need(len(by_name) == len(blocks), "block names")

    sensitivity: list[dict[str, Any]] = []
    for exponent in EXPONENTS:
        for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                            ("CONFIRMATION", CONFIRMATION_TAUS)):
            sensitivity.append(stratified_block(
                observations, "NATIVE_" + label + "_EXPONENT_" + str(exponent),
                taus, (0,), exponents=(exponent,)))
    for pair in PAIRS:
        pair_label = str(pair[0]) + "_TO_" + str(pair[1])
        for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                            ("CONFIRMATION", CONFIRMATION_TAUS)):
            sensitivity.append(stratified_block(
                observations, "NATIVE_" + label + "_PAIR_" + pair_label,
                taus, (0,), pairs=(pair,)))
    for omitted in PAIRS:
        retained = tuple(pair for pair in PAIRS if pair != omitted)
        omitted_label = str(omitted[0]) + "_TO_" + str(omitted[1])
        for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                            ("CONFIRMATION", CONFIRMATION_TAUS)):
            sensitivity.append(stratified_block(
                observations, "NATIVE_" + label + "_OMIT_PAIR_" + omitted_label,
                taus, (0,), pairs=retained))
    for omitted in LADDERS:
        retained_ladders = tuple(ladder for ladder in LADDERS
                                 if ladder != omitted)
        for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                            ("CONFIRMATION", CONFIRMATION_TAUS)):
            sensitivity.append(stratified_block(
                observations, "NATIVE_" + label + "_OMIT_LADDER_" + omitted,
                taus, (0,), ladders=retained_ladders))
    need(len(sensitivity) == 22, "sensitivity census")

    native_relation = replication(by_name["CALIBRATION_NATIVE"],
                                  by_name["CONFIRMATION_NATIVE"])
    stress_relation = replication(by_name["CALIBRATION_ALL_RADII"],
                                  by_name["CONFIRMATION_ALL_RADII"])
    need(by_name["CALIBRATION_NATIVE"]["class"] ==
         "LEFT_COMPLETION_LOWER" and
         by_name["CONFIRMATION_NATIVE"]["class"] ==
         "RIGHT_COMPLETION_LOWER" and
         native_relation == "STRICT_CLASS_REVERSED",
         "native tau-slice reversal")
    need(by_name["CALIBRATION_ALL_RADII"]["class"] ==
         "LEFT_COMPLETION_LOWER" and
         by_name["CONFIRMATION_ALL_RADII"]["class"] ==
         "PREFERENCE_UNRESOLVED" and
         stress_relation == "NONREPLICATED_WITH_UNRESOLVED_SLICE",
         "all-radius nonreplication")
    sensitivity_by_name = {row["name"]: row for row in sensitivity}
    need(sensitivity_by_name[
        "NATIVE_CALIBRATION_OMIT_LADDER_BASE"]["class"] ==
         "RIGHT_COMPLETION_LOWER", "BASE omission reversal")
    need(sensitivity_by_name[
        "NATIVE_CALIBRATION_EXPONENT_1"]["class"] ==
         "LEFT_COMPLETION_LOWER" and
         sensitivity_by_name[
        "NATIVE_CALIBRATION_EXPONENT_2"]["class"] ==
         "RIGHT_COMPLETION_LOWER", "exponent interaction")

    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc310_code_sha256": TPC310_CODE_SHA256,
            "tpc310_result_sha256": TPC310_RESULT_SHA256,
            "tpc309_code_sha256": TPC309_CODE_SHA256,
            "tpc309_result_sha256": TPC309_RESULT_SHA256,
            "tpc309_profile_cases": 54,
            "tpc309_envelope_observations": 162,
        },
        "protocol": {
            "ladders": list(LADDERS),
            "transitions": [list(pair) for pair in PAIRS],
            "kernel_exponents": list(EXPONENTS),
            "tolerances": list(TAUS),
            "radii": list(RADII),
            "calibration_tolerances": list(CALIBRATION_TAUS),
            "confirmation_tolerances": list(CONFIRMATION_TAUS),
            "primary_radius": 0,
            "design_stratum":
                "fixed transition, exponent, tolerance, and completion radius",
            "within_stratum_rule":
                "sum LOW/BASE/HIGH completion extrema before taking right/left ratio",
            "between_stratum_rule":
                "equal arithmetic weight for every selected design stratum",
            "thresholds": {"right_upper_lt": "0.9",
                           "left_lower_gt": "1.1"},
            "registration_status":
                "DECLARED_CHILD_PROTOCOL_NOT_EXTERNALLY_TIMESTAMPED_PREREGISTRATION",
            "holdout_status":
                "DISJOINT_TAU_PARAMETER_SLICE_WITHIN_ONE_LOCKED_PARENT_ATLAS",
        },
        "exact_theorem": {
            "balanced_stratum_count":
                "3 transitions x 2 exponents x 3 tolerances x 3 radii = 54",
            "profile_pool_extrema":
                "independent finite completion extrema add within each profile stratum",
            "equal_stratum_interval_map":
                "positive arithmetic averaging preserves endpoint enclosure",
            "tau_partition":
                "{0.25,0.5} and {0.75} are disjoint and cover the declared tau grid",
            "scope":
                "finite two-stage stratification and parameter-slice replication audit",
        },
        "strata": strata,
        "blocks": blocks,
        "sensitivity": sensitivity,
        "finite_audit": {
            "parent_observations": 162,
            "profile_pooled_strata": 54,
            "primary_and_control_blocks": 6,
            "sensitivity_blocks": 22,
            "stratum_class_counts": class_counts(strata),
            "native_calibration_class":
                by_name["CALIBRATION_NATIVE"]["class"],
            "native_confirmation_class":
                by_name["CONFIRMATION_NATIVE"]["class"],
            "native_replication": native_relation,
            "all_radii_calibration_class":
                by_name["CALIBRATION_ALL_RADII"]["class"],
            "all_radii_confirmation_class":
                by_name["CONFIRMATION_ALL_RADII"]["class"],
            "all_radii_replication": stress_relation,
            "native_calibration_base_omission":
                sensitivity_by_name[
                    "NATIVE_CALIBRATION_OMIT_LADDER_BASE"]["class"],
            "native_calibration_exponent_classes": {
                "1": sensitivity_by_name[
                    "NATIVE_CALIBRATION_EXPONENT_1"]["class"],
                "2": sensitivity_by_name[
                    "NATIVE_CALIBRATION_EXPONENT_2"]["class"],
            },
            "target_generation_leakage":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "fresh_physical_holdout": "NONE_SAME_LOCKED_PARENT_ATLAS",
            "external_weight_justification": "OPEN",
            "formal_interval_certificate":
                "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "causal_identification": "NONE_PARAMETER_SLICE_DIAGNOSTIC_ONLY",
            "uniform_asymptotic_budget": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
            "full_gate_b": "OPEN",
            "twin_prime_result": "NONE",
        },
        "firewall": {
            "TPC311_STRATIFIED_PROTOCOL": "PROVED_EXACT_FINITE",
            "TPC311_PROFILE_POOL_EXTREMA": "PROVED_EXACT_FINITE",
            "TPC311_EQUAL_STRATUM_INTERVAL_MAP": "PROVED_EXACT_FINITE",
            "TPC311_TAU_PARTITION": "PROVED_EXACT_FINITE",
            "TPC311_STRATIFIED_ATLAS":
                "NUMERICALLY_REPRODUCED_FINITE_54_STRATA_6_BLOCKS_22_SENSITIVITY_BLOCKS",
            "TPC311_NATIVE_TAU_REPLICATION":
                "REFUTED_FINITE_STRICT_CALIBRATION_LEFT_CONFIRMATION_RIGHT",
            "TPC311_ALL_RADII_TAU_REPLICATION":
                "REFUTED_FINITE_CALIBRATION_LEFT_CONFIRMATION_UNRESOLVED",
            "TPC311_PROFILE_ROBUSTNESS":
                "REFUTED_FINITE_BASE_OMISSION_CHANGES_NATIVE_CALIBRATION_CLASS",
            "TPC311_EXPONENT_ROBUSTNESS":
                "REFUTED_FINITE_NATIVE_CALIBRATION_EXPONENT_1_LEFT_EXPONENT_2_RIGHT",
            "TPC311_REGISTRATION_STATUS":
                "DECLARED_CHILD_PROTOCOL_NOT_EXTERNALLY_TIMESTAMPED_PREREGISTRATION",
            "TPC311_FRESH_PHYSICAL_HOLDOUT": "NONE_SAME_LOCKED_PARENT_ATLAS",
            "TPC311_TARGET_GENERATION_LEAKAGE":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "TPC311_CAUSAL_IDENTIFICATION":
                "NONE_PARAMETER_SLICE_DIAGNOSTIC_ONLY",
            "TPC311_FORMAL_INTERVAL_CERTIFICATE":
                "OPEN_PARENT_FLOAT_REPLAY_NOT_DIRECTED_ROUNDING",
            "TPC311_EXTERNAL_WEIGHT_JUSTIFICATION": "OPEN",
            "TPC311_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC311_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC311_FIXED_POWER_CREDIT": 0,
            "TPC311_FULL_GATE_B": "OPEN",
            "TPC311_TWIN_PRIME_RESULT": "NONE",
            "TPC311_STATUS": STATUS,
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
    print("TPC311_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["profile_pooled_strata"] == 54 and
         audit["native_replication"] == "STRICT_CLASS_REVERSED" and
         audit["all_radii_replication"] ==
         "NONREPLICATED_WITH_UNRESOLVED_SLICE", "finite audit")
    print("TPC311_CERTIFICATE=PASS strata=54 blocks=6 sensitivity=22 "
          "native=CAL_L_CONFIRM_R all_radii=CAL_L_CONFIRM_U")


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
        print("TPC311_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
