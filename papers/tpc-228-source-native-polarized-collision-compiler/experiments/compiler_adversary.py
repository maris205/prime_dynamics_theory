#!/usr/bin/env python3
"""Mutation adversary for the TPC-228 compiler contract."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))
from source_native_compiler import CompilerFailure, validate_payload  # noqa: E402


def main() -> int:
    base = json.loads((PROJECT / "results/certificate.json").read_text())
    mutations = []
    for path, value in (
        (("schema",), "mutated"),
        (("claim_level",), "PROVED_ARITHMETIC_L2"),
        (("theorem", "phase_axis"), "PROFILE"),
        (("theorem", "profile_axis"), "PACKET_DEPENDENT"),
        (("fixtures", "positive", "direct_collision_value"), "0"),
        (("fixtures", "negative", "direct_collision_value"), "1/40000"),
        (("fixtures", "row_cancellation", "direct_collision_value"), "1"),
        (("checks", "diagonal_deleted_before_collision_sum"), False),
    ):
        item = copy.deepcopy(base)
        target = item
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        mutations.append(item)
    rejected = 0
    for item in mutations:
        try:
            validate_payload(item)
        except CompilerFailure:
            rejected += 1
    if rejected != len(mutations):
        print(f"TPC228_COMPILER_ADVERSARY=FAIL: {rejected}/{len(mutations)}", file=sys.stderr)
        return 1
    print("TPC228_COMPILER_ADVERSARY=PASS")
    print(f"mutations_rejected={rejected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
