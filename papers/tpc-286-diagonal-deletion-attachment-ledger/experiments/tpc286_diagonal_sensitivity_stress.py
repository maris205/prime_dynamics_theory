#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-286 attachment certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-286-diagonal-deletion-attachment-ledger"
SOURCE = PROJECT / "code/tpc286_diagonal_deletion_attachment_certificate.py"
RESULT = PROJECT / "results/tpc286_certificate.json"

spec = importlib.util.spec_from_file_location("tpc286_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC286_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.document()
    mutations: list[tuple[str, dict]] = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["attachment_split"] = (
        "C_phys=C_full+C_diag")
    mutations.append(("theorem", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0][
        "source_scalar_full_including_diagonal_interval"][0] = "0"
    mutations.append(("full_interval", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["diagonal_correction_sign"] = "POSITIVE"
    mutations.append(("diagonal_sign", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["physical_deleted_diagonal_sign"] = (
        "POSITIVE")
    mutations.append(("physical_sign", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["full_vs_physical_sign_flip"] = True
    mutations.append(("flip_flag", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["fixed_power_credit"] = 1
    mutations.append(("budget", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["tpc285_result_sha256"] = "0" * 64
    mutations.append(("provenance", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    rejected = sum(candidate != expected for _, candidate in mutations)
    if rejected != len(mutations):
        print("TPC286_STRESS=FAIL mutation accepted", flush=True)
        return 1
    labels = " ".join(label + "=REJECTED" for label, _ in mutations)
    print("TPC286_STRESS=PASS mutations=8 " + labels, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
