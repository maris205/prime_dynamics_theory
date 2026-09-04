#!/usr/bin/env python3
"""Mutation firewall for the TPC-388 certificate contract."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-388-c1-cross-family-slope-transfer"
CERTIFICATE = PROJECT / "results/tpc388_certificate.json"
sys.path.insert(0, str(PROJECT / "experiments"))
import tpc388_independent_checker as independent  # noqa: E402


def reject(document) -> bool:
    try:
        independent.check_document(document, recompute=False)
    except Exception:
        return True
    return False


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        document = independent.parse_no_duplicates(CERTIFICATE.read_bytes())
        payload = document["payload"]
        cells = payload["transfer_summary"]["cells"]
        rows = payload["rows"]
        mutations = []

        def mutate(fn):
            item = copy.deepcopy(document)
            fn(item)
            mutations.append(item)

        mutate(lambda d: d["payload"].__setitem__("schema", "BAD"))
        mutate(lambda d: d.__setitem__("claim_status", "BAD"))
        mutate(lambda d: d.__setitem__("payload_sha256", "0" * 64))
        mutate(lambda d: d["payload"]["parent_lock"].__setitem__(
            "parent_certificate_sha256", "0" * 64))
        mutate(lambda d: d["payload"]["parent_lock"].__setitem__(
            "parent_slopes_frozen", False))
        mutate(lambda d: d["payload"]["parent_lock"].__setitem__(
            "parent_slopes_refit_on_current_family", True))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "origins", [1, 2, 3, 4, 5]))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "holdout_role_fixed_before_readout", False))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "response_used_for_selection", True))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "parent_slope_refit", True))
        mutate(lambda d: d["payload"]["rows"].pop())
        mutate(lambda d: d["payload"]["rows"].append(copy.deepcopy(rows[0])))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "origin_role", "holdout_1024"))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "spectral_failure", not rows[0]["spectral_failure"]))
        mutate(lambda d: d["payload"]["transfer_summary"].__setitem__(
            "row_count", 255))
        mutate(lambda d: d["payload"]["transfer_summary"].__setitem__(
            "parent_transfer_pass_count", 31))
        mutate(lambda d: d["payload"]["transfer_summary"].__setitem__(
            "local_control_pass_count", 31))
        mutate(lambda d: d["payload"]["transfer_summary"]
               ["failure_counts_by_mode_normalization"]
               ["fixed_c3_local_diagonal"].__setitem__("spectral", 9))
        mutate(lambda d: d["payload"]["transfer_summary"]["stable_cells"]
               .__setitem__("1024_holdout", 27))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC388_ARITHMETIC_ADVANCE", "YES"))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC388_FIXED_POWER_CREDIT", 1))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC388_FULL_GATE_B", "CLOSED"))
        mutate(lambda d: d["payload"].__setitem__(
            "round2_clue", "WRONG_CLUE"))
        mutate(lambda d: d["payload"]["exact_anchor"].__setitem__(
            "shell", [7, 11]))
        mutate(lambda d: d["payload"]["transfer_summary"]["cells"][0]
               .__setitem__("parent_transfer_error", "0"))

        if len(mutations) != 25 or not all(reject(item) for item in mutations):
            raise RuntimeError("mutation accepted")
        print("TPC388_STRESS=PASS mutations=25")
        return 0
    except Exception as error:
        print("TPC388_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
