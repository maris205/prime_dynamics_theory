#!/usr/bin/env python3
"""Independent replay for the TPC-311 tau-slice stratification audit.

This checker deliberately does not import the TPC-311 producer.  It parses the
locked TPC-309 interval rows, reconstructs the profile-pooled strata and the
declared equal-stratum blocks with ordinary double precision, and checks the
stored certificate within a small replay slack.  It is an independent finite
replay, not a directed-rounding interval certificate or a fresh data set.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-311-stratified-tau-holdout-replication"
RESULT = PROJECT / "results/tpc311_certificate.json"
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
LADDERS = ("LOW", "BASE", "HIGH")
PAIRS = ((50, 60), (60, 70), (70, 90))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
CALIBRATION_TAUS = ("0.25", "0.5")
CONFIRMATION_TAUS = ("0.75",)
RADII = (0, 1, 2)
SLACK_RELATIVE = 5e-9


class Failure(RuntimeError):
    """A fail-closed replay error."""


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load(path: Path, expected_hash: str, expected_status: str
         ) -> dict[str, Any]:
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


def positive_interval(value: Any, label: str) -> tuple[float, float]:
    need(isinstance(value, list) and len(value) == 2, label + " shape")
    lo, hi = float(value[0]), float(value[1])
    need(math.isfinite(lo) and math.isfinite(hi) and 0 < lo <= hi,
         label + " order")
    return lo, hi


def close(stored: Any, expected: tuple[float, float], label: str) -> None:
    actual = positive_interval(stored, label)
    for x, y in zip(actual, expected):
        margin = SLACK_RELATIVE * max(abs(y), 1e-12) + 1e-12
        need(abs(x - y) <= margin, label + " numerical replay")


def classify(bounds: tuple[float, float]) -> str:
    lo, hi = bounds
    if hi < 0.9:
        return "RIGHT_COMPLETION_LOWER"
    if lo > 1.1:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def observations(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for case in source["payload"]["cases"]:
        pair = (int(case["from_Q"]), int(case["to_Q"]))
        base = (pair, int(case["kernel_exponent"]), case["tau"],
                case["profile_ladder"])
        for envelope in case["envelopes"]:
            key = base + (int(envelope["radius"]),)
            need(key not in seen, "duplicate source key")
            seen.add(key)
            right = envelope["right_completion"]
            left = envelope["left_completion"]
            rmin = positive_interval(right["envelope_min_mse"], "right min")
            rmax = positive_interval(right["envelope_max_mse"], "right max")
            lmin = positive_interval(left["envelope_min_mse"], "left min")
            lmax = positive_interval(left["envelope_max_mse"], "left max")
            need(rmin[0] <= rmin[1] <= rmax[1], "right extrema")
            need(lmin[0] <= lmin[1] <= lmax[1], "left extrema")
            rows.append({
                "pair": pair,
                "exponent": int(case["kernel_exponent"]),
                "tau": case["tau"],
                "radius": int(envelope["radius"]),
                "ladder": case["profile_ladder"],
                "right_min_lo": rmin[0],
                "right_max_hi": rmax[1],
                "left_min_lo": lmin[0],
                "left_max_hi": lmax[1],
            })
    need(len(rows) == 162 and len(seen) == 162, "source census")
    return rows


def profile_pool(rows: list[dict[str, Any]], pair: tuple[int, int],
                 exponent: int, tau: str, radius: int,
                 ladders: tuple[str, ...] = LADDERS) -> dict[str, Any]:
    selected = [row for row in rows
                if row["pair"] == pair and row["exponent"] == exponent and
                row["tau"] == tau and row["radius"] == radius and
                row["ladder"] in ladders]
    need(len(selected) == len(ladders), "stratum coverage")
    bounds = (
        sum(row["right_min_lo"] for row in selected) /
        sum(row["left_max_hi"] for row in selected),
        sum(row["right_max_hi"] for row in selected) /
        sum(row["left_min_lo"] for row in selected),
    )
    return {
        "from_Q": pair[0], "to_Q": pair[1],
        "kernel_exponent": exponent, "tau": tau, "radius": radius,
        "ladders": list(ladders),
        "parent_observation_count": len(selected),
        "ratio_interval": [repr(bounds[0]), repr(bounds[1])],
        "class": classify(bounds),
    }


def block(rows: list[dict[str, Any]], name: str, taus: tuple[str, ...],
          radii: tuple[int, ...], pairs: tuple[tuple[int, int], ...] = PAIRS,
          exponents: tuple[int, ...] = EXPONENTS,
          ladders: tuple[str, ...] = LADDERS) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    strata = [profile_pool(rows, pair, exponent, tau, radius, ladders)
              for pair in pairs for exponent in exponents for tau in taus
              for radius in radii]
    need(bool(strata), "nonempty block")
    bounds = (sum(float(x["ratio_interval"][0]) for x in strata) / len(strata),
              sum(float(x["ratio_interval"][1]) for x in strata) / len(strata))
    return ({
        "name": name,
        "tau_subset": list(taus), "radius_subset": list(radii),
        "transition_subset": [list(pair) for pair in pairs],
        "exponent_subset": list(exponents), "ladder_subset": list(ladders),
        "stratum_count": len(strata),
        "parent_observation_count": len(strata) * len(ladders),
        "ratio_interval": [repr(bounds[0]), repr(bounds[1])],
        "class": classify(bounds),
    }, strata)


def check_block(stored: dict[str, Any], expected: dict[str, Any],
                label: str) -> None:
    need(stored["name"] == expected["name"] and
         stored["tau_subset"] == expected["tau_subset"] and
         stored["radius_subset"] == expected["radius_subset"] and
         stored["transition_subset"] == expected["transition_subset"] and
         stored["exponent_subset"] == expected["exponent_subset"] and
         stored["ladder_subset"] == expected["ladder_subset"] and
         stored["stratum_count"] == expected["stratum_count"] and
         stored["parent_observation_count"] == expected["parent_observation_count"],
         label + " metadata")
    close(stored["ratio_interval"],
          tuple(float(x) for x in expected["ratio_interval"]), label)
    need(stored["class"] == expected["class"], label + " class")


def main() -> int:
    try:
        need(digest(TPC310_CODE.read_bytes()) == TPC310_CODE_SHA256,
             "TPC-310 code provenance")
        need(digest(TPC309_CODE.read_bytes()) == TPC309_CODE_SHA256,
             "TPC-309 code provenance")
        tpc310 = load(TPC310_RESULT, TPC310_RESULT_SHA256, TPC310_STATUS)
        tpc309 = load(TPC309_RESULT, TPC309_RESULT_SHA256, TPC309_STATUS)
        need(tpc310["payload"]["schema"] ==
             "TPC310_CROSS_HOLDOUT_AGGREGATION_ORDER_AUDIT_V1",
             "TPC-310 schema")
        need(tpc310["payload"]["parent_lock"] == {
            "tpc309_code_sha256": TPC309_CODE_SHA256,
            "tpc309_result_sha256": TPC309_RESULT_SHA256,
            "tpc309_profile_cases": 54,
            "tpc309_envelope_observations": 162,
        }, "TPC-310 parent lock")
        child = load(RESULT, digest(RESULT.read_bytes()), STATUS)
        payload = child["payload"]
        need(payload["schema"] == SCHEMA, "child schema")
        need(payload["parent_lock"] == {
            "tpc310_code_sha256": TPC310_CODE_SHA256,
            "tpc310_result_sha256": TPC310_RESULT_SHA256,
            "tpc309_code_sha256": TPC309_CODE_SHA256,
            "tpc309_result_sha256": TPC309_RESULT_SHA256,
            "tpc309_profile_cases": 54,
            "tpc309_envelope_observations": 162,
        }, "child parent lock")
        protocol = payload["protocol"]
        need(protocol["ladders"] == list(LADDERS) and
             protocol["transitions"] == [list(x) for x in PAIRS] and
             protocol["kernel_exponents"] == list(EXPONENTS) and
             protocol["tolerances"] == list(TAUS) and
             protocol["radii"] == list(RADII), "protocol")

        rows = observations(tpc309)
        expected_strata = [profile_pool(rows, pair, exponent, tau, radius)
                           for pair in PAIRS for exponent in EXPONENTS
                           for tau in TAUS for radius in RADII]
        stored_strata = payload["strata"]
        need(len(stored_strata) == 54, "stratum count")
        for stored, expected in zip(stored_strata, expected_strata):
            need(stored["from_Q"] == expected["from_Q"] and
                 stored["to_Q"] == expected["to_Q"] and
                 stored["kernel_exponent"] == expected["kernel_exponent"] and
                 stored["tau"] == expected["tau"] and
                 stored["radius"] == expected["radius"] and
                 stored["ladders"] == expected["ladders"] and
                 stored["parent_observation_count"] ==
                 expected["parent_observation_count"], "stratum metadata")
            close(stored["ratio_interval"],
                  tuple(float(x) for x in expected["ratio_interval"]),
                  "stratum")
            need(stored["class"] == expected["class"], "stratum class")

        specs = (
            ("CALIBRATION_NATIVE", CALIBRATION_TAUS, (0,)),
            ("CONFIRMATION_NATIVE", CONFIRMATION_TAUS, (0,)),
            ("FULL_NATIVE", TAUS, (0,)),
            ("CALIBRATION_ALL_RADII", CALIBRATION_TAUS, RADII),
            ("CONFIRMATION_ALL_RADII", CONFIRMATION_TAUS, RADII),
            ("FULL_ALL_RADII", TAUS, RADII),
        )
        expected_blocks = []
        for name, taus, radii in specs:
            expected_blocks.append(block(rows, name, taus, radii)[0])
        for stored, expected in zip(payload["blocks"], expected_blocks):
            check_block(stored, expected, stored.get("name", "block"))
        by_name = {x["name"]: x for x in payload["blocks"]}
        need(by_name["CALIBRATION_NATIVE"]["class"] ==
             "LEFT_COMPLETION_LOWER" and
             by_name["CONFIRMATION_NATIVE"]["class"] ==
             "RIGHT_COMPLETION_LOWER", "native reversal")
        need(by_name["CALIBRATION_ALL_RADII"]["class"] ==
             "LEFT_COMPLETION_LOWER" and
             by_name["CONFIRMATION_ALL_RADII"]["class"] ==
             "PREFERENCE_UNRESOLVED", "stress obstruction")

        expected_sensitivity = []
        for exponent in EXPONENTS:
            for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                                ("CONFIRMATION", CONFIRMATION_TAUS)):
                name = "NATIVE_" + label + "_EXPONENT_" + str(exponent)
                expected_sensitivity.append(block(rows, name, taus, (0,),
                                                  exponents=(exponent,))[0])
        for pair in PAIRS:
            pair_label = str(pair[0]) + "_TO_" + str(pair[1])
            for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                                ("CONFIRMATION", CONFIRMATION_TAUS)):
                name = "NATIVE_" + label + "_PAIR_" + pair_label
                expected_sensitivity.append(block(rows, name, taus, (0,),
                                                  pairs=(pair,))[0])
        for omitted in PAIRS:
            retained = tuple(pair for pair in PAIRS if pair != omitted)
            omitted_label = str(omitted[0]) + "_TO_" + str(omitted[1])
            for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                                ("CONFIRMATION", CONFIRMATION_TAUS)):
                name = "NATIVE_" + label + "_OMIT_PAIR_" + omitted_label
                expected_sensitivity.append(block(
                    rows, name, taus, (0,), pairs=retained)[0])
        for omitted in LADDERS:
            retained = tuple(x for x in LADDERS if x != omitted)
            for label, taus in (("CALIBRATION", CALIBRATION_TAUS),
                                ("CONFIRMATION", CONFIRMATION_TAUS)):
                name = "NATIVE_" + label + "_OMIT_LADDER_" + omitted
                expected_sensitivity.append(block(
                    rows, name, taus, (0,), ladders=retained)[0])
        need(len(expected_sensitivity) == 22 and
             len(payload["sensitivity"]) == 22, "sensitivity count")
        for stored, expected in zip(payload["sensitivity"], expected_sensitivity):
            check_block(stored, expected, stored.get("name", "sensitivity"))

        audit = payload["finite_audit"]
        need(audit["parent_observations"] == 162 and
             audit["profile_pooled_strata"] == 54 and
             audit["primary_and_control_blocks"] == 6 and
             audit["sensitivity_blocks"] == 22 and
             audit["native_replication"] == "STRICT_CLASS_REVERSED" and
             audit["all_radii_replication"] ==
             "NONREPLICATED_WITH_UNRESOLVED_SLICE", "audit summary")
        print("TPC311_INDEPENDENT_CHECK=PASS strata=54 blocks=6 "
              "sensitivity=22 native=REVERSED all_radii=UNRESOLVED")
        return 0
    except (Failure, OSError, ValueError, KeyError, json.JSONDecodeError,
            ZeroDivisionError) as error:
        print("TPC311_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
