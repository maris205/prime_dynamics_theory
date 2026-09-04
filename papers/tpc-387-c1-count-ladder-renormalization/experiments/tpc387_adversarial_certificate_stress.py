#!/usr/bin/env python3
"""Mutation firewall for the TPC-387 count-ladder certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / "papers/tpc-387-c1-count-ladder-renormalization/results/tpc387_certificate.json"
SCHEMA = "TPC387_C1_COUNT_LADDER_RENORMALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_LADDER_RENORMALIZATION"
ORIGINS = [2400001, 2404011, 2408021, 2412031, 2416041]
CALIBRATION = [2400001, 2404011, 2408021]
HOLDOUT = [2412031, 2416041]
COUNTS = [512, 768]
MODES = ["fixed_c3", "full_relative"]
QS = [2048, 8192]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
NORMS = ["local_diagonal", "pooled_train_scalar"]


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def valid_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value)) and float(value) >= 0.0
    except (TypeError, ValueError):
        return False


def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("forecast_is_fitted") is False and
         isinstance(parent.get("parent_code_sha256"), str) and
         isinstance(parent.get("parent_certificate_sha256"), str), "parent")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == ORIGINS and
         selection.get("calibration_origins") == CALIBRATION and
         selection.get("holdout_origins") == HOLDOUT and
         selection.get("calibration_counts") == COUNTS and
         selection.get("holdout_count") == 1024 and
         selection.get("band_modes") == MODES and
         selection.get("q_anchors") == QS and
         selection.get("laws") == LAWS and
         selection.get("normalizations") == NORMS and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("slope_fit_uses_holdout") is False, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "rows")
    expected = ({(o, n, q, law, norm, mode) for o in CALIBRATION
                 for n in COUNTS for q in QS for law in LAWS
                 for norm in NORMS for mode in MODES} |
                {(o, 1024, q, law, norm, mode) for o in HOLDOUT
                 for q in QS for law in LAWS for norm in NORMS
                 for mode in MODES})
    observed = {(r.get("origin"), r.get("count"), r.get("Q"),
                 r.get("law"), r.get("normalization"), r.get("band_mode"))
                for r in rows}
    need(observed == expected, "row keys")
    for row in rows:
        role = (f"calibration_{row.get('count')}"
                if row.get("origin") in CALIBRATION else "holdout_1024")
        need(row.get("origin_role") == role and
             row.get("count") in (512, 768, 1024) and
             valid_number(row.get("band_spectral")) and
             valid_number(row.get("band_schur")) and
             valid_number(row.get("band_frobenius")), "row shape")
    summary = payload.get("ladder_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("renorm_pass_count_all_cells") == 32 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32 and
         isinstance(summary.get("forecast_summary_all_plus_Q8192"), list) and
         len(summary["forecast_summary_all_plus_Q8192"]) == 4, "summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 256 and audit.get("cell_count") == 32 and
         audit.get("calibration_counts") == COUNTS and
         audit.get("holdout_count") == 1024 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC387_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC387_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC387_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC387_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == "TEST_C1_COUNT_LADDER_SECOND_HOLDOUT", "clue")


def mutations(document: dict[str, Any]) -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("status", lambda d: d.__setitem__("claim_status", "PROVED")),
        ("schema", lambda d: d["payload"].__setitem__("schema", "X")),
        ("payload_status", lambda d: d["payload"].__setitem__("status", "PROVED")),
        ("origins", lambda d: d["payload"]["selection_protocol"].__setitem__("origins", [2400001, 2404011, 2408022, 2412031, 2416041])),
        ("calibration", lambda d: d["payload"]["selection_protocol"].__setitem__("calibration_origins", [2400001, 2404011])),
        ("holdout", lambda d: d["payload"]["selection_protocol"].__setitem__("holdout_origins", [2412031])),
        ("cal_counts", lambda d: d["payload"]["selection_protocol"].__setitem__("calibration_counts", [256, 768])),
        ("hold_count", lambda d: d["payload"]["selection_protocol"].__setitem__("holdout_count", 768)),
        ("modes", lambda d: d["payload"]["selection_protocol"].__setitem__("band_modes", ["fixed_c3"])),
        ("q_anchors", lambda d: d["payload"]["selection_protocol"].__setitem__("q_anchors", [1024, 8192])),
        ("laws", lambda d: d["payload"]["selection_protocol"].__setitem__("laws", ["all_plus"])),
        ("normalizations", lambda d: d["payload"]["selection_protocol"].__setitem__("normalizations", ["local_diagonal"])),
        ("response_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("response_used_for_selection", True)),
        ("slope_flag", lambda d: d["payload"]["selection_protocol"].__setitem__("slope_fit_uses_holdout", True)),
        ("row_delete", lambda d: d["payload"]["rows"].pop()),
        ("row_origin", lambda d: d["payload"]["rows"][0].__setitem__("origin", 2400002)),
        ("row_role", lambda d: d["payload"]["rows"][0].__setitem__("origin_role", "holdout_1024")),
        ("row_count", lambda d: d["payload"]["rows"][0].__setitem__("count", 1024)),
        ("row_value", lambda d: d["payload"]["rows"][0].__setitem__("band_spectral", "NaN")),
        ("row_digest", lambda d: d["payload"].__setitem__("row_digest", "0")),
        ("cell_delete", lambda d: d["payload"]["ladder_summary"]["cells"].pop()),
        ("forecast_delete", lambda d: d["payload"]["ladder_summary"]["forecast_summary_all_plus_Q8192"].pop()),
        ("audit_count", lambda d: d["payload"]["finite_audit"].__setitem__("holdout_count", 768)),
        ("arithmetic", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC387_ARITHMETIC_ADVANCE", "YES")),
        ("clue", lambda d: d["payload"].__setitem__("round2_clue", "X")),
    ]


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        rejected = 0
        for _, action in mutations(document):
            candidate = copy.deepcopy(document)
            action(candidate)
            try:
                validate(candidate)
            except (Failure, TypeError, ValueError, KeyError):
                rejected += 1
        need(rejected == 25, "mutation coverage")
        print("TPC387_STRESS=PASS mutations=25")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC387_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
