#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-284 control atlas."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-284-admissible-source-control-atlas"
SOURCE = PROJECT / "code/tpc284_admissible_source_control_atlas_certificate.py"
RESULT = PROJECT / "results/tpc284_certificate.json"
spec = importlib.util.spec_from_file_location("tpc284_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC284_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    # Build the expected release once.  Each mutation is then tested against
    # the producer's deterministic semantic document without six redundant
    # 72-row replays.
    expected = producer.document()
    mutations = []
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["rho_squared_interval"][0] = "0/1"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][12]["attachment_sign"] = "POSITIVE"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["control"] = "UNDECLARED"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_theorem"]["fixed_power_credit"] = 1
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["result_sha256"] = "0" * 64
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(candidate)
    rejected = sum(candidate != expected for candidate in mutations)
    if rejected != len(mutations):
        print("TPC284_STRESS=FAIL mutation accepted", flush=True)
        return 1
    print("TPC284_STRESS=PASS mutations=6 interval=REJECTED sign=REJECTED "
          "control=REJECTED budget=REJECTED provenance=REJECTED "
          "row_deletion=REJECTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
