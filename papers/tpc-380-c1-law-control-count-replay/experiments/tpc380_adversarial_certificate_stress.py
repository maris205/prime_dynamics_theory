#!/usr/bin/env python3
"""Adversarial schema/firewall mutations for the TPC-380 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-380-c1-law-control-count-replay/results/"
    "tpc380_certificate.json")

SCHEMA = "TPC380_C1_LAW_CONTROL_COUNT_REPLAY_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_COUNT_REPLAY"
ORIGINS = [1300001, 1308021, 1316041]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
Q_ANCHORS = [512, 2048, 8192]
PROFILE = {
    "all_plus": [0, 3, 3], "alternating_index": [0, 0, 0],
    "mod4_character": [0, 0, 0], "half_split": [0, 0, 0]}


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def validate_shape(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1, "version")
    need(document.get("claim_status") == STATUS, "status")
    payload = document.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_schema") ==
        "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1" and
        parent.get("parent_round2_clue") ==
        "TEST_C1_LAW_CONTROL_COUNT_REPLAY" and
         parent.get("parent_profile") == [0, 3, 3], "parent")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1300001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1300001 + 401 * i for i in range(41)] and
         selection.get("origin_indices") == [0, 20, 40] and
         selection.get("origins") == ORIGINS and
         selection.get("window_count") == 2048 and
         selection.get("block_length") == 256 and
         selection.get("block_count") == 8 and
         selection.get("q_anchors") == Q_ANCHORS and
         selection.get("laws") == LAWS and
         selection.get("law_rule") ==
         "all four sign laws fixed before any response is read" and
         selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == ORIGINS and
         protocol.get("window_count") == 2048 and
         protocol.get("block_length") == 256 and
         protocol.get("block_count") == 8 and
         protocol.get("band_cutoff") == 1 and
         protocol.get("q_anchors") == Q_ANCHORS and
         protocol.get("kernel_exponents") == [1] and
         protocol.get("laws") == LAWS and protocol.get("betas") == [2] and
         protocol.get("height") == 66 and
         protocol.get("common_geometry") is True and
         protocol.get("source_response_used") is False and
         protocol.get("origin_selection_used") is False and
         protocol.get("law_selection_used") is False and
         protocol.get("row_selection_used") is False, "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 36 and audit.get("origin_count") == 3 and
         audit.get("q_count") == 3 and audit.get("law_count") == 4 and
         audit.get("spectral_rows") == 36 and
         audit.get("spectral_cap_violations") == 6 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_law_Q") == PROFILE and
         audit.get("all_plus_failure_profile") == [0, 3, 3] and
         audit.get("signed_control_failure_profiles") == {
             law: [0, 0, 0] for law in LAWS if law != "all_plus"} and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("law_control_complete") is True and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    phase = payload.get("phase_summary", {})
    need(phase.get("rows") == 36 and phase.get("laws") == LAWS and
         phase.get("law_count") == 4 and
         phase.get("failure_profile_by_law_Q") == PROFILE and
         phase.get("spectral_cap_violations") == 6 and
         phase.get("schur_cap_violations") == 0 and
         phase.get("signed_controls_all_below_spectral_cap") is True,
         "phase")
    need(payload.get("round2_clue") ==
         "TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY", "clue")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC380_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC380_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC380_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC380_TWIN_PRIME_RESULT") == "NONE", "firewall")
    rows = payload.get("rows", [])
    need(isinstance(rows, list) and len(rows) == 36, "rows")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    need({(row.get("origin"), row.get("Q"), row.get("law"))
          for row in rows} ==
         {(origin, q0, law) for origin in ORIGINS
          for q0 in Q_ANCHORS for law in LAWS}, "row keys")
    for row in rows:
        need(row.get("count") == 2048 and row.get("block_length") == 256 and
             row.get("block_count") == 8 and row.get("kernel_exponent") == 1 and
             row.get("beta") == 2 and row.get("height") == 66 and
             row.get("law") in LAWS and
             row.get("band_failure") in (True, False) and
             row.get("schur_failure") in (True, False), "row header")


def mutations(document: dict[str, Any]) -> list[dict[str, Any]]:
    paths = [
        ("claim_status", lambda d: d.__setitem__("claim_status", "PROVED")),
        ("schema", lambda d: d["payload"].__setitem__("schema", "X")),
        ("payload_status", lambda d: d["payload"].__setitem__("status", "PROVED")),
        ("grid_start", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_start", 1300002)),
        ("grid_step", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_step", 400)),
        ("candidate_origins", lambda d: d["payload"]["selection_protocol"].__setitem__("candidate_origins", [1300001] * 41)),
        ("indices", lambda d: d["payload"]["selection_protocol"].__setitem__("origin_indices", [0, 19, 40])),
        ("response_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("response_used_for_selection", True)),
        ("window_count", lambda d: d["payload"]["selection_protocol"].__setitem__("window_count", 1024)),
        ("block_length", lambda d: d["payload"]["protocol"].__setitem__("block_length", 128)),
        ("band_cutoff", lambda d: d["payload"]["protocol"].__setitem__("band_cutoff", 2)),
        ("laws", lambda d: d["payload"]["protocol"].__setitem__("laws", ["all_plus"])),
        ("law_rule", lambda d: d["payload"]["selection_protocol"].__setitem__("law_rule", "response-dependent")),
        ("beta", lambda d: d["payload"]["protocol"].__setitem__("betas", [0])),
        ("q_anchors", lambda d: d["payload"]["protocol"].__setitem__("q_anchors", [512, 1024, 8192])),
        ("row_delete", lambda d: d["payload"]["rows"].pop()),
        ("row_law", lambda d: d["payload"]["rows"][0].__setitem__("law", "all_plus" if d["payload"]["rows"][0]["law"] != "all_plus" else "half_split")),
        ("row_origin", lambda d: d["payload"]["rows"][0].__setitem__("origin", 1300002)),
        ("row_failure", lambda d: d["payload"]["rows"][0].__setitem__("band_failure", not d["payload"]["rows"][0]["band_failure"])),
        ("spectral_census", lambda d: d["payload"]["finite_audit"].__setitem__("spectral_cap_violations", 5)),
        ("schur_census", lambda d: d["payload"]["finite_audit"].__setitem__("schur_cap_violations", 1)),
        ("law_profile", lambda d: d["payload"]["finite_audit"].__setitem__("failure_profile_by_law_Q", {**PROFILE, "half_split": [0, 0, 1]})),
        ("control_profile", lambda d: d["payload"]["finite_audit"]["signed_control_failure_profiles"].__setitem__("half_split", [0, 0, 1])),
        ("arithmetic", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC380_ARITHMETIC_ADVANCE", "YES")),
        ("clue", lambda d: d["payload"].__setitem__("round2_clue", "UNDECLARED")),
    ]
    output = []
    for name, action in paths:
        candidate = copy.deepcopy(document)
        action(candidate)
        output.append(candidate)
    return output


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate_shape(document)
        rejected = 0
        for candidate in mutations(document):
            try:
                validate_shape(candidate)
            except Failure:
                rejected += 1
        need(rejected == 25, "mutation coverage")
        print("TPC380_STRESS=PASS mutations=25")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC380_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
