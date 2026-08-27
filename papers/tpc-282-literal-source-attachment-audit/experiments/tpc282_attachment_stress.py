#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-282 source-lock certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-282-literal-source-attachment-audit"
SOURCE = PROJECT / "code/tpc282_literal_source_attachment_certificate.py"
RESULT = PROJECT / "results/tpc282_certificate.json"

spec = importlib.util.spec_from_file_location("tpc282_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC282_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def valid(candidate: dict) -> bool:
    try:
        producer.check_data(candidate)
        return False
    except Exception:
        return True


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    mutations = []
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["source_scalar_C_interval"][0] = "0/1"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][9]["attachment_sign"] = "NEGATIVE"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][9]["attachment_cosine_squared_interval"][0] = "0/1"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["source_lock"]["parent_result_sha256"] = "0" * 64
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_theorem"]["fixed_power_credit"] = 1
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(candidate)
    rejected = sum(valid(candidate) for candidate in mutations)
    if rejected != len(mutations):
        print("TPC282_STRESS=FAIL mutation accepted", flush=True)
        return 1
    print("TPC282_STRESS=PASS mutations=6 scalar=REJECTED sign=REJECTED "
          "cosine=REJECTED parent_rebind=REJECTED budget=REJECTED "
          "row_deletion=REJECTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
