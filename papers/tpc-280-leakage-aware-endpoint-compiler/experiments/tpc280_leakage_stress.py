#!/usr/bin/env python3
"""Hostile mutation checks for the TPC-280 release certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-280-leakage-aware-endpoint-compiler"
SOURCE = PROJECT / "code/tpc280_leakage_aware_endpoint_certificate.py"
RESULT = PROJECT / "results/tpc280_certificate.json"

spec = importlib.util.spec_from_file_location("tpc280_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC280_STRESS=FAIL producer unavailable")
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
    candidate["payload"]["exact_theorem"]["dominant_exponent_compiler"] = "r>=1"
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["budget_cases"][1]["kappa"] = 4
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["margin_cases"].pop()
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["endpoint_cases"][2]["status"] = "PAID_STRICT"
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_transfer"]["fixed_power_credit"] = 1
    mutations.append(candidate)

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_transfer"]["parent_result_sha256"] = "0" * 64
    mutations.append(candidate)

    rejected = sum(not valid(candidate) for candidate in mutations)
    if rejected != len(mutations):
        print("TPC280_STRESS=FAIL mutation accepted", flush=True)
        return 1
    print("TPC280_STRESS=PASS mutations=6 theorem=REJECTED budget=REJECTED "
          "endpoint=REJECTED parent_rebind=REJECTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
