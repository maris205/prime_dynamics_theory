#!/usr/bin/env python3
"""Mutation stress for the TPC-336 masked response certificate."""

from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path
from typing import Any

RESULT = Path(__file__).resolve().parents[1] / "results/tpc336_certificate.json"

class Failure(RuntimeError): pass
def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition: raise Failure(message)
def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")
def validate(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1, "version")
    need(document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE", "status")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC336_MASKED_SIGNED_GRAM_RESPONSE_V1", "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "digest")
    need(len(payload.get("rows", [])) == 6 and
         payload.get("finite_audit", {}).get("gain_ordering_census") == 6,
         "geometry")
    need(payload.get("summary", {}).get("destructive_interaction_rows") == 6,
         "summary")
    fw = payload.get("claim_firewall", {})
    need(fw.get("TPC336_ARITHMETIC_ADVANCE") == "NO" and
         fw.get("TPC336_FIXED_POWER_CREDIT") == 0 and
         fw.get("TPC336_SOURCE_UNIFORM_L2") == "OPEN", "firewall")
    need(payload.get("exact_anchor", {}).get("identity_exact") is True, "anchor")

def main() -> int:
    try:
        original = json.loads(RESULT.read_bytes()); validate(original)
        mutations = []
        item = copy.deepcopy(original); item["payload"]["rows"] = item["payload"]["rows"][:-1]; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["rows"][0]["self_metrics"]["twin_prime"]["response_gain"] = "0"; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["summary"]["destructive_interaction_rows"] = 5; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["claim_firewall"]["TPC336_ARITHMETIC_ADVANCE"] = "YES"; mutations.append(item)
        item = copy.deepcopy(original); item["payload"]["exact_anchor"]["identity_exact"] = False; mutations.append(item)
        rejected = 0
        for item in mutations:
            try: validate(item)
            except Failure: rejected += 1
        need(rejected == 5, "mutation rejection")
        print("TPC336_STRESS=PASS mutations=5 rejected=5 rows=6 categories=4 "
              "firewall=fail_closed")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC336_STRESS=FAIL " + str(error), file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
