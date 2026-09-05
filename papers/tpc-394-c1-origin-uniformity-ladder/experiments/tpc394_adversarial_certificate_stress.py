#!/usr/bin/env python3
"""Mutation firewall for the TPC-394 certificate contract."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-394-c1-origin-uniformity-ladder"
CERTIFICATE = PROJECT / "results/tpc394_certificate.json"
sys.path.insert(0, str(PROJECT / "experiments"))
import tpc394_independent_checker as independent  # noqa: E402


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
        rows = payload["rows"]
        cells = payload["origin_summary"]["cells"]
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
            "parent_interface_used_for_current_fit", True))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "origins", [1, 2, 3]))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "response_used_for_selection", True))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "holdout_role_fixed_before_readout", False))
        mutate(lambda d: d["payload"]["rows"].pop())
        mutate(lambda d: d["payload"]["rows"].append(copy.deepcopy(rows[0])))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "origin_role", "holdout_1024"))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "band_spectral", "0"))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "spectral_failure", not rows[0]["spectral_failure"]))
        mutate(lambda d: d["payload"]["origin_summary"].__setitem__(
            "row_count", 63))
        mutate(lambda d: d["payload"]["origin_summary"].__setitem__(
            "origin_uniformity_stable_cells", 0))
        mutate(lambda d: d["payload"]["origin_summary"]
               ["origin_uniformity_pass_counts"].__setitem__(
                   "local_diagonal", 0))
        mutate(lambda d: d["payload"]["origin_summary"]
               ["holdout_transfer_pass_counts"].__setitem__(
                   "origin_scalar", 0))
        mutate(lambda d: d["payload"]["origin_summary"]
               ["spectral_failures_by_normalization"].__setitem__(
                   "local_diagonal", 0))
        mutate(lambda d: d["payload"]["origin_summary"]["cells"][0]
               ["all_origin_stats"].__setitem__("relative_spread", "0"))
        mutate(lambda d: d["payload"]["origin_summary"]["cells"][0]
               .__setitem__("within_holdout_transfer_cap", False))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC394_ARITHMETIC_ADVANCE", "YES"))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC394_FIXED_POWER_CREDIT", 1))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC394_FULL_GATE_B", "CLOSED"))
        mutate(lambda d: d["payload"].__setitem__(
            "round2_clue", "WRONG_CLUE"))
        mutate(lambda d: d["payload"]["exact_anchor"].__setitem__(
            "shell", [7, 11]))

        if len(mutations) != 25 or not all(reject(item) for item in mutations):
            raise RuntimeError("mutation accepted")
        print("TPC394_STRESS=PASS mutations=25")
        return 0
    except Exception as error:
        print("TPC394_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
