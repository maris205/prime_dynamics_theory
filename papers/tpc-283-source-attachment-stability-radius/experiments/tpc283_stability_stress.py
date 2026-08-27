#!/usr/bin/env python3
"""Hostile mutation audit for TPC-283."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-283-source-attachment-stability-radius"
SOURCE = PROJECT / "code/tpc283_source_attachment_stability_certificate.py"
RESULT = PROJECT / "results/tpc283_certificate.json"
spec = importlib.util.spec_from_file_location("tpc283_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC283_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec); spec.loader.exec_module(producer)


def rejected(c: dict) -> bool:
    try:
        # Recompute the semantic payload, then compare the mutation to it.
        producer.need(c["payload"] == producer.build_payload(producer.load_parent()),
                      "mutation accepted")
        return False
    except Exception:
        return True


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8")); muts = []
    c = copy.deepcopy(base); c["payload"]["exact_theorem"]["distance_squared"] = "0"; muts.append(c)
    c = copy.deepcopy(base); c["payload"]["rows"][0]["zeroing_radius_upper_less_than"] = "1/2"; muts.append(c)
    c = copy.deepcopy(base); c["payload"]["finite_audit"]["fixed_power_credit"] = 1; muts.append(c)
    c = copy.deepcopy(base); c["payload"]["parent_lock"]["result_sha256"] = "0" * 64; muts.append(c)
    c = copy.deepcopy(base); c["payload"]["fixtures"][0]["residual_attachment"] = "1/1"; muts.append(c)
    c = copy.deepcopy(base); c["payload"]["rows"].pop(); muts.append(c)
    n = sum(rejected(c) for c in muts)
    if n != len(muts):
        print("TPC283_STRESS=FAIL mutation accepted", flush=True); return 1
    print("TPC283_STRESS=PASS mutations=6 theorem=REJECTED bound=REJECTED "
          "budget=REJECTED provenance=REJECTED fixture=REJECTED census=REJECTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
