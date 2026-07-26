#!/usr/bin/env python3
"""Exact finite audit for the TPC-120 typed dependency graph.

This script checks decision logic and archive structure only.  It does
not estimate any arithmetic sum and is not numerical evidence for H1--H9.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


PAPERS = {
    103: ("PROVED_L1", ["H2"]),
    104: ("OPEN_INPUT", ["H2"]),
    105: ("PROVED_L1", ["H1", "H2"]),
    106: ("REROUTE_SUBROUTE", ["H2"]),
    107: ("PROVED_L1", ["H2", "H3"]),
    108: ("OPEN_INPUT", ["H3"]),
    109: ("REROUTE_SUBROUTE", ["H2", "H3"]),
    110: ("OPEN_INPUT", ["H5"]),
    111: ("OPEN_INPUT", ["H5"]),
    112: ("CONDITIONAL_L1", ["H5", "H9"]),
    113: ("OPEN_INPUT", ["H1", "H9"]),
    114: ("OPEN_INPUT", ["H1", "H9"]),
    115: ("OPEN_INPUT", ["H7", "H9"]),
    116: ("OPEN_INPUT", ["H4", "H9"]),
    117: ("NOT_TESTABLE", ["H6", "H9"]),
    118: ("INCOMPLETE", ["H9"]),
    119: ("NOT_TESTABLE", ["H8"]),
}

GATES = {
    "H1": "NOT_TESTABLE",
    "H2": "OPEN",
    "H3": "OPEN",
    "H4": "OPEN",
    "H5": "NOT_TESTABLE",
    "H6": "NOT_TESTABLE",
    "H7": "OPEN",
    "H8": "NOT_TESTABLE",
    "H9": "NOT_TESTABLE",
}

NEXT_GATES = {
    121: "actual post-bin determinant-energy inputs",
    122: "signed-prefix/BV/content-remainder zero-mode transfer",
    123: "complete native-atom reconnection archive",
    124: "one literal fixed-shift H3 block test",
}


def endpoint_classification(value: Fraction | None, complete: bool) -> str:
    """Classify an exact physical endpoint certificate."""
    if not complete or value is None:
        return "NOT_TESTABLE"
    threshold = Fraction(1, 400)
    if value < threshold:
        return "GO"
    if value == threshold:
        return "STOP_EQUALITY"
    return "STOP_ABOVE"


def global_verdict(gates: dict[str, str], endpoint: str) -> str:
    """Return the route verdict without promoting a local obstruction."""
    if any(state == "INFEASIBLE_GLOBAL" for state in gates.values()):
        return "INFEASIBLE"
    if all(state == "PROVED" for state in gates.values()):
        if endpoint == "GO":
            return "GO"
        if endpoint in {"STOP_EQUALITY", "STOP_ABOVE"}:
            return "STOP_ROUTE"
        return "NOT_TESTABLE"
    if any(
        state in {"OPEN", "NOT_TESTABLE", "CONDITIONAL", "INCOMPLETE"}
        for state in gates.values()
    ):
        return "NOT_TESTABLE"
    return "REROUTE"


def main() -> None:
    assertions = 0

    assert set(GATES) == {f"H{i}" for i in range(1, 10)}
    assertions += 1

    ancestors = {gate: set() for gate in GATES}
    for paper, (_, supported_gates) in PAPERS.items():
        assert 103 <= paper <= 119
        for gate in supported_gates:
            ancestors[gate].add(paper)
    assert all(ancestors[gate] for gate in GATES)
    assertions += 1

    assert not any(state in {"PROVED_L2", "PROVED"} for state, _ in PAPERS.values())
    assertions += 1

    assert global_verdict(GATES, "NOT_TESTABLE") == "NOT_TESTABLE"
    assertions += 1

    local_stop = dict(GATES)
    local_stop["H2"] = "OPEN"
    assert global_verdict(local_stop, "NOT_TESTABLE") != "INFEASIBLE"
    assertions += 1

    assert endpoint_classification(Fraction(1, 500), True) == "GO"
    assertions += 1
    assert endpoint_classification(Fraction(1, 400), True) == "STOP_EQUALITY"
    assertions += 1
    assert endpoint_classification(Fraction(1, 300), True) == "STOP_ABOVE"
    assertions += 1
    assert endpoint_classification(None, False) == "NOT_TESTABLE"
    assertions += 1

    proved_gates = {gate: "PROVED" for gate in GATES}
    assert global_verdict(proved_gates, "STOP_EQUALITY") == "STOP_ROUTE"
    assert global_verdict(proved_gates, "STOP_ABOVE") == "STOP_ROUTE"
    assertions += 2

    # Missing costs cannot be silently filled by zero.
    open_costs = {
        "frame": None,
        "grouping": None,
        "localization": None,
        "tail": None,
        "cover": None,
    }
    assert any(value is None for value in open_costs.values())
    assert endpoint_classification(
        sum(
            ((value or Fraction(0)) for value in open_costs.values()),
            Fraction(0),
        ),
        complete=all(value is not None for value in open_costs.values()),
    ) == "NOT_TESTABLE"
    assertions += 1

    assert set(NEXT_GATES) == {121, 122, 123, 124}
    assertions += 1

    result = {
        "schema": "tpc-120-mvp2-global-route-audit-v1",
        "status": "PASS",
        "assertions_checked": assertions,
        "claim_level": "L0/L1_AUDIT_ONLY",
        "audit_snapshot_date": "2026-07-26",
        "endpoint": {
            "strict_threshold": "1/400",
            "equality": "STOP_EQUALITY",
            "unknown_costs": "NOT_ZERO_AND_NOT_TESTABLE",
            "determinant_reserve_reusable": False,
        },
        "gate_status": GATES,
        "global_verdict": global_verdict(GATES, "NOT_TESTABLE"),
        "next_gates": {str(number): title for number, title in NEXT_GATES.items()},
        "paper_status": {
            str(number): {
                "status": status,
                "feeds": feeds,
            }
            for number, (status, feeds) in PAPERS.items()
        },
        "stopped_subroute_is_global_infeasibility": False,
    }

    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
