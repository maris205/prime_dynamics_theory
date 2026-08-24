#!/usr/bin/env python3
"""Adversarial mutations for the TPC-227 axis contract."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from axis_separation import AxisSeparationFailure, validate_payload  # noqa: E402


def main() -> int:
    baseline = json.loads((PROJECT / "results/certificate.json").read_text())
    mutations = []

    item = copy.deepcopy(baseline)
    item["schema"] = "tpc227-mutated"
    mutations.append(item)

    item = copy.deepcopy(baseline)
    item["claim_level"] = "PROVED_ARITHMETIC_L2"
    mutations.append(item)

    item = copy.deepcopy(baseline)
    item["theorem"]["criterion"] = "pairwise profile boundedness is sufficient"
    mutations.append(item)

    item = copy.deepcopy(baseline)
    item["fixtures"]["common_physical"]["compatible_with_target"] = False
    mutations.append(item)

    item = copy.deepcopy(baseline)
    item["fixtures"]["row_dependent_odd_sign"]["compatible_with_target"] = True
    mutations.append(item)

    item = copy.deepcopy(baseline)
    item["checks"]["q25_resonance_off_diagonal_mismatch_exact"] = False
    mutations.append(item)

    rejected = 0
    for mutation in mutations:
        try:
            validate_payload(mutation)
        except AxisSeparationFailure:
            rejected += 1
    if rejected != len(mutations):
        print(f"TPC227_AXIS_ADVERSARY=FAIL: rejected {rejected}/{len(mutations)}", file=sys.stderr)
        return 1
    print("TPC227_AXIS_ADVERSARY=PASS")
    print(f"mutations_rejected={rejected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
