#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-281 certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-281-arithmetic-l2-gate-b-interface-audit"
SOURCE = PROJECT / "code/tpc281_arithmetic_l2_interface_certificate.py"
RESULT = PROJECT / "results/tpc281_certificate.json"

spec = importlib.util.spec_from_file_location("tpc281_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC281_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def valid(candidate: dict) -> bool:
    try:
        producer.validate(candidate)
        return candidate == producer.document()
    except Exception:
        return False


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    mutations = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["typed_two_term_L2"] = "||A_X S||_2^2<=0"
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["packets"][0]["vectors"][0][0] = "2/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["interface_cases"][1]["operator_bound_squared"] = "1/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["packets"][2]["perpendicular_attachment"] = "1/1"
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_transfer"]["parent_result_sha256"] = "0" * 64
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(candidate)

    rejected = sum(not valid(candidate) for candidate in mutations)
    if rejected != len(mutations):
        print("TPC281_STRESS=FAIL mutation accepted", flush=True)
        return 1
    print("TPC281_STRESS=PASS mutations=6 theorem=REJECTED vector=REJECTED "
          "operator_budget=REJECTED attachment=REJECTED parent_rebind=REJECTED "
          "row_deletion=REJECTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
