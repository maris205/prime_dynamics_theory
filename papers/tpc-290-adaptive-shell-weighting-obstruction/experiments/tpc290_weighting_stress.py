#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-290 finite weighting certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-290-adaptive-shell-weighting-obstruction"
SOURCE = PROJECT / "code/tpc290_adaptive_shell_weighting_certificate.py"
RESULT = PROJECT / "results/tpc290_certificate.json"

spec = importlib.util.spec_from_file_location("tpc290_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC290_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.frozen_document()
    # Freeze the one expensive trusted construction; all following cases
    # exercise the fail-closed equality and hash checks.
    producer.frozen_document = lambda: expected
    mutations: list[tuple[str, dict]] = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["nonnegative_no_decay"] = "R(w)>=0"
    mutations.append(("theorem", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["thresholds"]["eta"] = "1/2"
    mutations.append(("threshold", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["grid"]["policies"].append("prime_inverse")
    mutations.append(("policy_grid", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["policies"]["uniform"]["ratio"] = "1"
    mutations.append(("weighted_ratio", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][8]["equal_pair_subunit_count"] = 0
    mutations.append(("sparse_escape", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][8]["equal_pair_subunit_witnesses"][0][
        "subunit"] = False
    mutations.append(("pair_witness", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["drop_one_all_amplified"] = False
    mutations.append(("drop_one", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["all_full_support_policies_amplified_rows"] -= 1
    mutations.append(("audit_count", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["tpc289_result_sha256"] = "0" * 64
    mutations.append(("provenance", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    for label, candidate in mutations:
        try:
            producer.check_data(candidate)
        except Exception:
            continue
        print("TPC290_STRESS=FAIL mutation accepted " + label, flush=True)
        return 1
    labels = " ".join(label + "=REJECTED" for label, _ in mutations)
    print("TPC290_STRESS=PASS mutations=10 " + labels, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
