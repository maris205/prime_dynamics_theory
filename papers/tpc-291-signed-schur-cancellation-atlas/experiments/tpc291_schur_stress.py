#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-291 Schur atlas."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-291-signed-schur-cancellation-atlas"
SOURCE = PROJECT / "code/tpc291_signed_schur_cancellation_certificate.py"
RESULT = PROJECT / "results/tpc291_certificate.json"

spec = importlib.util.spec_from_file_location("tpc291_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC291_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.frozen_document()
    producer.frozen_document = lambda: expected
    mutations: list[tuple[str, dict]] = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["schur_identity"] = "residual=1"
    mutations.append(("theorem", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["thresholds"]["residual"][0] = "2/3"
    mutations.append(("threshold", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["best_coherence_pair"][
        "schur_residual"] = "0"
    mutations.append(("best_pair", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][8]["negative_pair_records"][0][
        "same_sign_cancellation"] = False
    mutations.append(("sign_cost", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][7]["residual_counts"]["1/10"] -= 1
    mutations.append(("row_count", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["residual_totals"]["1/4"] -= 1
    mutations.append(("audit_count", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["negative_pairs"] = 0
    mutations.append(("sign_census", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["fixed_power_credit"] = 1
    mutations.append(("budget", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["tpc290_result_sha256"] = "0" * 64
    mutations.append(("provenance", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    for label, candidate in mutations:
        try:
            producer.check_data(candidate)
        except Exception:
            continue
        print("TPC291_STRESS=FAIL mutation accepted " + label, flush=True)
        return 1
    labels = " ".join(label + "=REJECTED" for label, _ in mutations)
    print("TPC291_STRESS=PASS mutations=10 " + labels, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
