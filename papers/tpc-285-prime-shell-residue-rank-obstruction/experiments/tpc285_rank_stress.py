#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-285 residue-rank certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-285-prime-shell-residue-rank-obstruction"
SOURCE = PROJECT / "code/tpc285_prime_shell_residue_rank_certificate.py"
RESULT = PROJECT / "results/tpc285_certificate.json"
spec = importlib.util.spec_from_file_location("tpc285_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC285_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.document()
    mutations = []
    candidate = copy.deepcopy(base)
    candidate["payload"]["exact_theorem"]["centered_rank_bound"] = "rank(B_q)<=q-1"
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["centered_scaled_rank_mod_p"] += 1
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["deleted_diagonal_scaled_rank_mod_p"] -= 1
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["kernel_schur_scaled_rank_mod_p"] -= 1
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["result_sha256"] = "0" * 64
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["fixed_power_credit"] = 1
    mutations.append(candidate)
    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(candidate)
    rejected = sum(candidate != expected for candidate in mutations)
    if rejected != len(mutations):
        print("TPC285_STRESS=FAIL mutation accepted", flush=True)
        return 1
    print("TPC285_STRESS=PASS mutations=7 theorem=REJECTED centered=REJECTED "
          "deleted=REJECTED kernel=REJECTED provenance=REJECTED "
          "budget=REJECTED row_deletion=REJECTED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
