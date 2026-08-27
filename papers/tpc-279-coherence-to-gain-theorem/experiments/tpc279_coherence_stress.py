#!/usr/bin/env python3
"""Hostile mutation checks for the TPC-279 theorem certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-279-coherence-to-gain-theorem"
SOURCE = PROJECT / "code/tpc279_coherence_to_gain_certificate.py"
RESULT = PROJECT / "results/tpc279_certificate.json"

spec = importlib.util.spec_from_file_location("tpc279_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC279_STRESS=FAIL producer unavailable")
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
    candidate["payload"]["exact_theorem"]["pairwise_gain_floor"] = "r>=1"
    mutations.append(("theorem_mutation", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["normalized_output_ratio_interval"][0] = "0/1"
    mutations.append(("interval_mutation", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_transfer"]["fixed_power_credit"] = 1
    mutations.append(("power_promotion", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_transfer"]["parent_result_sha256"] = "0" * 64
    mutations.append(("parent_rebind", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["sharpness_witnesses"][0]["bound_is_sharp"] = False
    mutations.append(("sharpness_mutation", candidate))

    rejected = sum(not valid(candidate) for _name, candidate in mutations)
    if rejected != len(mutations):
        print("TPC279_STRESS=FAIL mutation accepted", flush=True)
        return 1
    print("TPC279_STRESS=PASS mutations=6 theorem=REJECTED interval=REJECTED "
          "power_promotion=REJECTED parent_rebind=REJECTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
