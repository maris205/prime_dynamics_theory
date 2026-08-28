#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-289 coherence certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-289-cross-prime-gram-coherence"
SOURCE = PROJECT / "code/tpc289_cross_prime_gram_coherence_certificate.py"
RESULT = PROJECT / "results/tpc289_certificate.json"

spec = importlib.util.spec_from_file_location("tpc289_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC289_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.document()
    # Freeze the expensive recomputation after one trusted construction; the
    # mutation test then exercises the canonical equality and claim firewall.
    producer.document = lambda: expected
    mutations: list[tuple[str, dict]] = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["accumulation_bound"] = "R_E>=0"
    mutations.append(("theorem", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["thresholds"]["eta"] = "1/2"
    mutations.append(("threshold", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["grid"]["rows"] = 17
    mutations.append(("grid", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][8]["pair_negative"] = 0
    mutations.append(("sign_census", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][8]["negative_pairs"][0]["sign"] = "POSITIVE"
    mutations.append(("negative_pair", candidate))

    candidate = copy.deepcopy(base)
    strong = next(row for row in candidate["payload"]["rows"]
                  if row["strong_coherence_block"])
    strong["strong_coherence_block"] = False
    mutations.append(("strong_block", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["energy_ratio"] = "1"
    mutations.append(("energy", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["pairwise_positive_rows"] -= 1
    mutations.append(("audit_count", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["tpc288_result_sha256"] = "0" * 64
    mutations.append(("provenance", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    for label, candidate in mutations:
        try:
            producer.check_data(candidate)
        except Exception:
            continue
        print("TPC289_STRESS=FAIL mutation accepted " + label, flush=True)
        return 1
    labels = " ".join(label + "=REJECTED" for label, _ in mutations)
    print("TPC289_STRESS=PASS mutations=10 " + labels, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
