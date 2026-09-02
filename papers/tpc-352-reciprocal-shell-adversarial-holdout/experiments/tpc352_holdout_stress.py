#!/usr/bin/env python3
"""Hostile mutation tests for the TPC-352 holdout certificate."""

from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-352-reciprocal-shell-adversarial-holdout/results/tpc352_certificate.json"


class StressFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise StressFailure(message)


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict) -> None:
    need(document.get("certificate_version") == 1, "version")
    need(document.get("claim_status") ==
         "PROVED_EXACT_FINITE_RECIPROCAL_ZERO_SUM_INCIDENCE_WITNESS_PLUS_"
         "NUMERICALLY_CERTIFIED_DISJOINT_HOLDOUT_AUDIT", "status")
    payload = document.get("payload", {})
    need(payload.get("schema") == "TPC352_RECIPROCAL_ADVERSARIAL_HOLDOUT_V1", "schema")
    need(document.get("payload_sha256") == __import__("hashlib").sha256(
        canonical(payload)).hexdigest(), "payload digest")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [96097, 120097, 144097] and
         protocol.get("source_counts") == [256, 512, 1024] and
         protocol.get("q_anchors") == [64, 128, 256, 512] and
         protocol.get("kernel_exponents") == [1, 2] and
         protocol.get("laws") == ["all_plus", "alternating_index"] and
         protocol.get("height") == 66, "protocol")
    need(payload.get("parent_lock", {}).get("TPC351_producer_sha256") ==
         "820f6195408a4d0fbbfed46f5bdd8054d812ae24eb87aaa1169791055f33328a" and
         payload.get("parent_lock", {}).get("TPC351_certificate_sha256") ==
         "74ca0045ca201712a69870669612b7bc16ccd0c019f27f3ea1d3dccb4b687db0",
         "parent lock")
    rows = payload.get("rows", [])
    need(len(rows) == 144 and len({(x.get("origin"), x.get("count"),
                                  x.get("q"), x.get("kernel_exponent"),
                                  x.get("law")) for x in rows}) == 144, "rows")
    audit = payload.get("finite_audit", {})
    need(audit.get("improved_parent_rows") == 118 and
         audit.get("positive_reciprocal_rows") == 144 and
         audit.get("reciprocal_nondecreasing_series") == 22 and
         audit.get("balanced_nondecreasing_series") == 22 and
         audit.get("fixed_power_credit") == 0 and
         audit.get("arithmetic_advance") == "NO", "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC352_UNIFORM_REPAIR_TRANSFER") == "REFUTED_SCOPED" and
         firewall.get("TPC352_HIGH_SHELL_REPAIR") == "REFUTED_SCOPED" and
         firewall.get("TPC352_FULL_GATE_B") == "OPEN", "firewall")


def reject(label: str, mutate) -> None:
    document = json.loads(CERT.read_text(encoding="utf-8"))
    mutate(document)
    try:
        validate(document)
    except (StressFailure, KeyError, TypeError, ValueError):
        return
    raise StressFailure("mutation accepted: " + label)


def main() -> int:
    try:
        document = json.loads(CERT.read_text(encoding="utf-8"))
        validate(document)
        mutations = [
            ("origin", lambda d: d["payload"]["protocol"]["origins"].__setitem__(0, 96098)),
            ("scale", lambda d: d["payload"]["protocol"]["q_anchors"].__setitem__(0, 65)),
            ("row-delete", lambda d: d["payload"]["rows"].pop()),
            ("row-value", lambda d: d["payload"]["rows"][0].__setitem__("reciprocal_to_defect_ratio", "9")),
            ("census", lambda d: d["payload"]["finite_audit"].__setitem__("improved_parent_rows", 119)),
            ("claim", lambda d: d["payload"]["claim_firewall"].__setitem__("TPC352_UNIFORM_REPAIR_TRANSFER", "PASS")),
            ("anchor", lambda d: d["payload"]["exact_anchor"]["incidence_vector"].__setitem__(2, "0/1")),
            ("parent", lambda d: d["payload"]["parent_lock"].__setitem__("TPC351_certificate_sha256", "0" * 64)),
        ]
        for label, mutation in mutations:
            reject(label, mutation)
        print("TPC352_STRESS=PASS exact_baseline=1 mutations=" + str(len(mutations)))
        return 0
    except (StressFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC352_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
