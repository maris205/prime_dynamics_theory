#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-288 Gram obstruction certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-288-growing-shell-gram-obstruction"
SOURCE = PROJECT / "code/tpc288_growing_shell_gram_certificate.py"
RESULT = PROJECT / "results/tpc288_certificate.json"

spec = importlib.util.spec_from_file_location("tpc288_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC288_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.document()
    producer.document = lambda: expected
    mutations: list[tuple[str, dict]] = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["energy_identity"] = (
        "||g_S||_2^2=trace(G)")
    mutations.append(("theorem", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["grid"]["growth_path"][0][2] = 10
    mutations.append(("grid", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["energy_ratio"] = "1"
    mutations.append(("energy", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["gram_rank_mod"] -= 1
    mutations.append(("gram_rank", candidate))

    candidate = copy.deepcopy(base)
    audited = next(row for row in candidate["payload"]["rows"]
                   if row["operator_rank_audited"])
    audited["operator_rank_mod"] -= 1
    mutations.append(("operator_rank", candidate))

    candidate = copy.deepcopy(base)
    mismatch = next(row for row in candidate["payload"]["rows"]
                    if row["scalar_energy_mismatch"])
    mismatch["scalar_energy_mismatch"] = False
    mutations.append(("mismatch_flag", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["energy_amplified_rows"] -= 1
    mutations.append(("audit_count", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["fixed_power_credit"] = 1
    mutations.append(("budget", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["tpc287_result_sha256"] = "0" * 64
    mutations.append(("provenance", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    for label, candidate in mutations:
        try:
            producer.check_data(candidate)
        except Exception:
            continue
        print("TPC288_STRESS=FAIL mutation accepted " + label, flush=True)
        return 1
    labels = " ".join(label + "=REJECTED" for label, _ in mutations)
    print("TPC288_STRESS=PASS mutations=10 " + labels, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
