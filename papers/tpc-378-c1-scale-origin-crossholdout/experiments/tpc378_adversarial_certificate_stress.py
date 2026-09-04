#!/usr/bin/env python3
"""Mutation stress test for the TPC-378 finite certificate contract."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-378-c1-scale-origin-crossholdout/results/"
    "tpc378_certificate.json")
ROW_DIGEST = "2116145cd9e4668b0a4709fe79ab6d4720f6355b5cd4bee5b1b1c7eb12bee3a6"


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def validate_shape(document: dict) -> None:
    need(document.get("certificate_version") == 1, "version")
    need(document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_SCALE_ORIGIN_CROSSHOLDOUT",
         "status")
    payload = document.get("payload", {})
    need(payload.get("schema") == "TPC378_C1_SCALE_ORIGIN_CROSSHOLDOUT_V1",
         "schema")
    need(payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_SCALE_ORIGIN_CROSSHOLDOUT",
         "payload status")
    selection = payload.get("selection_protocol", {})
    need(selection.get("grid_start") == 1100001 and
         selection.get("grid_step") == 401 and
         selection.get("grid_count") == 41 and
         selection.get("candidate_origins") ==
         [1100001 + 401 * i for i in range(41)], "grid")
    need(selection.get("origins") == [1100001, 1108021, 1116041],
         "origins")
    need(selection.get("counts") == [1024, 2048], "counts")
    need(selection.get("origin_indices") == [0, 20, 40], "indices")
    need(selection.get("block_length") == 256 and
         selection.get("block_counts") == [4, 8] and
         selection.get("q_anchors") == [512, 2048, 8192],
         "selection scales")
    need(selection.get("response_used_for_selection") is False and
         selection.get("signed_metric_used_for_selection") is False and
         selection.get("panel_complete_before_metric_read") is True,
         "response selection")
    protocol = payload.get("protocol", {})
    need(protocol.get("band_cutoff") == 1 and
         protocol.get("block_length") == 256 and
         protocol.get("q_anchors") == [512, 2048, 8192] and
         protocol.get("betas") == [2] and
         protocol.get("laws") == ["all_plus"], "protocol")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 18 and
         audit.get("spectral_cap_violations") == 12 and
         audit.get("schur_cap_violations") == 0 and
         audit.get("failure_profile_by_count_Q") == [[0, 3, 3], [0, 3, 3]] and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("profile_transfer") is True, "audit")
    need(payload.get("round2_clue") ==
         "TEST_C1_CROSSHOLDOUT_LAW_CONTROL", "clue")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC378_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC378_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC378_FULL_GATE_B") == "OPEN", "firewall")
    rows = payload.get("rows", [])
    need(isinstance(rows, list) and len(rows) == 18, "rows")
    need(payload.get("row_digest") == ROW_DIGEST and
         hashlib.sha256(canonical(rows)).hexdigest() == ROW_DIGEST,
         "row digest")
    need({(row.get("origin"), row.get("count"), row.get("Q"))
          for row in rows} ==
         {(origin, count, q) for origin in [1100001, 1108021, 1116041]
          for count in [1024, 2048] for q in [512, 2048, 8192]},
         "row keys")
    for row in rows:
        need(row.get("block_length") == 256 and
             row.get("block_count") == row.get("count", 0) // 256 and
             row.get("kernel_exponent") == 1 and
             row.get("beta") == 2 and row.get("law") == "all_plus" and
             row.get("height") == 66 and
             row.get("band_failure") in (True, False) and
             row.get("schur_failure") in (True, False), "row header")


def mutations(document: dict) -> list[dict]:
    paths = [
        ("claim_status", lambda d: d.__setitem__("claim_status", "PROVED")),
        ("schema", lambda d: d["payload"].__setitem__("schema", "X")),
        ("payload_status", lambda d: d["payload"].__setitem__("status", "PROVED")),
        ("origins", lambda d: d["payload"]["selection_protocol"].__setitem__("origins", [1100002, 1108021, 1116041])),
        ("counts", lambda d: d["payload"]["selection_protocol"].__setitem__("counts", [1024, 1536])),
        ("indices", lambda d: d["payload"]["selection_protocol"].__setitem__("origin_indices", [0, 19, 40])),
        ("response_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("response_used_for_selection", True)),
        ("grid_step", lambda d: d["payload"]["selection_protocol"].__setitem__("grid_step", 400)),
        ("block_length", lambda d: d["payload"]["protocol"].__setitem__("block_length", 128)),
        ("band_cutoff", lambda d: d["payload"]["protocol"].__setitem__("band_cutoff", 2)),
        ("law", lambda d: d["payload"]["protocol"].__setitem__("laws", ["alternating_index"])),
        ("beta", lambda d: d["payload"]["protocol"].__setitem__("betas", [0])),
        ("q_anchors", lambda d: d["payload"]["protocol"].__setitem__("q_anchors", [512, 1024, 8192])),
        ("row_delete", lambda d: d["payload"]["rows"].pop()),
        ("row_origin", lambda d: d["payload"]["rows"][0].__setitem__("origin", 1100002)),
        ("row_count", lambda d: d["payload"]["rows"][0].__setitem__("count", 1536)),
        ("row_failure", lambda d: d["payload"]["rows"][0].__setitem__("band_failure", not d["payload"]["rows"][0]["band_failure"])),
        ("spectral_census", lambda d: d["payload"]["finite_audit"].__setitem__("spectral_cap_violations", 11)),
        ("schur_census", lambda d: d["payload"]["finite_audit"].__setitem__("schur_cap_violations", 1)),
        ("profile", lambda d: d["payload"]["finite_audit"].__setitem__("failure_profile_by_count_Q", [[0, 3, 2], [0, 3, 3]])),
        ("profile_transfer", lambda d: d["payload"]["finite_audit"].__setitem__("profile_transfer", False)),
        ("arithmetic", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC378_ARITHMETIC_ADVANCE", "YES")),
        ("credit", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC378_FIXED_POWER_CREDIT", 1)),
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
        need(rejected == 24, "mutation coverage")
        print("TPC378_STRESS=PASS mutations=24")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC378_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
