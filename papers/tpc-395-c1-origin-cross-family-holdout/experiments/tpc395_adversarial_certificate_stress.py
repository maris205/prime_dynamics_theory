#!/usr/bin/env python3
"""Mutation firewall for the TPC-395 cross-family certificate."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-395-c1-origin-cross-family-holdout"
CERTIFICATE = PROJECT / "results/tpc395_certificate.json"
sys.path.insert(0, str(PROJECT / "experiments"))
import tpc395_independent_checker as independent  # noqa: E402


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
            "parent_means_used_as_response_blind_baseline", False))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "origins", [1, 2, 3]))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "response_used_for_selection", True))
        mutate(lambda d: d["payload"]["selection_protocol"].__setitem__(
            "parent_means_frozen_before_current_readout", False))
        mutate(lambda d: d["payload"]["rows"].pop())
        mutate(lambda d: d["payload"]["rows"].append(copy.deepcopy(rows[0])))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "origin_role", "holdout_1024"))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "band_spectral", "0"))
        mutate(lambda d: d["payload"]["rows"][0].__setitem__(
            "spectral_failure", not rows[0]["spectral_failure"]))
        mutate(lambda d: d["payload"]["origin_summary"].__setitem__(
            "row_count", 47))
        mutate(lambda d: d["payload"]["origin_summary"].__setitem__(
            "origin_stable_cells", 0))
        mutate(lambda d: d["payload"]["origin_summary"]
               ["cross_family_holdout_pass_counts"].__setitem__(
                   "local_diagonal", 0))
        mutate(lambda d: d["payload"]["origin_summary"]
               ["within_family_transfer_pass_counts"].__setitem__(
                   "origin_scalar", 0))
        mutate(lambda d: d["payload"]["origin_summary"]
               ["spectral_failures_by_normalization"].__setitem__(
                   "local_diagonal", 0))
        mutate(lambda d: d["payload"]["origin_summary"]["cells"][0]
               .__setitem__("parent_family_mean", "0"))
        mutate(lambda d: d["payload"]["origin_summary"]["cells"][0]
               .__setitem__("within_cross_family_holdout_cap", False))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC395_ARITHMETIC_ADVANCE", "YES"))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC395_FIXED_POWER_CREDIT", 1))
        mutate(lambda d: d["payload"]["claim_firewall"].__setitem__(
            "TPC395_FULL_GATE_B", "CLOSED"))
        mutate(lambda d: d["payload"].__setitem__(
            "round2_clue", "WRONG_CLUE"))
        mutate(lambda d: d["payload"]["exact_anchor"].__setitem__(
            "shell", [7, 11]))

        if len(mutations) != 25 or not all(reject(item) for item in mutations):
            raise RuntimeError("mutation accepted")
        print("TPC395_STRESS=PASS mutations=25")
        return 0
    except Exception as error:
        print("TPC395_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
