#!/usr/bin/env python3
"""Hostile mutation audit for the TPC-287 finite cancellation certificate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-287-prime-shell-cancellation-depth"
SOURCE = PROJECT / "code/tpc287_prime_shell_cancellation_certificate.py"
RESULT = PROJECT / "results/tpc287_certificate.json"

spec = importlib.util.spec_from_file_location("tpc287_producer", SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC287_STRESS=FAIL producer unavailable")
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


def main() -> int:
    base = json.loads(RESULT.read_text(encoding="utf-8"))
    expected = producer.document()
    # One full regeneration is enough for this mutation test.  Reuse that
    # locked document while exercising the fail-closed validator so that nine
    # hostile cases do not multiply the already expensive rational replay.
    producer.document = lambda: expected
    mutations: list[tuple[str, dict]] = []

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_theorem"]["attachment_identity"] = (
        "C_shell=C_1-C_2")
    mutations.append(("theorem", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["shell_ladder"][2]["primes"].append(19)
    mutations.append(("ladder", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][5]["components"][0]["prime"] = 3
    mutations.append(("component_prime", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][0]["shell_attachment_interval"][0] = "0"
    mutations.append(("shell_interval", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][4]["retention_upper"] = "1"
    mutations.append(("retention", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"][7]["leave_one_out"][0][
        "nonzero_sign_flip"] = not candidate["payload"]["rows"][7][
            "leave_one_out"][0]["nonzero_sign_flip"]
    mutations.append(("leave_out_flag", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["finite_audit"]["fixed_power_credit"] = 1
    mutations.append(("budget", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["parent_lock"]["tpc286_result_sha256"] = "0" * 64
    mutations.append(("provenance", candidate))

    candidate = copy.deepcopy(base)
    candidate["payload"]["rows"].pop()
    mutations.append(("row_deletion", candidate))

    # The producer's fail-closed equality check is intentionally exercised on
    # every mutation.  It also catches stale payload hashes because the
    # canonical document is recomputed from the locked engine and parent.
    for label, candidate in mutations:
        try:
            producer.check_data(candidate)
        except Exception:
            continue
        print("TPC287_STRESS=FAIL mutation accepted " + label, flush=True)
        return 1
    labels = " ".join(label + "=REJECTED" for label, _ in mutations)
    print("TPC287_STRESS=PASS mutations=9 " + labels, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
