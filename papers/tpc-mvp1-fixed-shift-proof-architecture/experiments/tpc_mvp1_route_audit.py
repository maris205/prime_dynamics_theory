#!/usr/bin/env python3
"""Deterministic dependency and exponent audit for TPC-MVP1.

This script checks the internal logic of the roadmap.  It does not
test any asymptotic prime or Mobius estimate.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from fractions import Fraction


NODES = {
    "E15_anchor": ("E", "L1"),
    "E18_interface": ("E", "L1"),
    "E98_constant_return": ("E", "L1"),
    "E100_q_u_return": ("E", "L1"),
    "E102_master": ("E", "L1"),
    "E_prime_power_removal": ("E", "classical"),
    **{f"H{i}": ("H", "unproved") for i in range(1, 10)},
    "C_resonance": ("C", "conditional"),
    "C_all_packets": ("C", "conditional"),
    "C_HL": ("C", "conditional"),
    "C_prime_pairs": ("C", "conditional"),
}

EDGES = [
    ("E98_constant_return", "C_resonance"),
    ("E100_q_u_return", "C_resonance"),
    ("E102_master", "C_resonance"),
    ("H2", "C_resonance"),
    ("C_resonance", "C_all_packets"),
    ("H3", "C_all_packets"),
    ("H4", "C_all_packets"),
    ("H5", "C_all_packets"),
    ("E15_anchor", "C_HL"),
    ("E18_interface", "C_HL"),
    ("H1", "C_HL"),
    ("H6", "C_HL"),
    ("H7", "C_HL"),
    ("H8", "C_HL"),
    ("H9", "C_HL"),
    ("C_all_packets", "C_HL"),
    ("C_HL", "C_prime_pairs"),
    ("E_prime_power_removal", "C_prime_pairs"),
]

GATES = {
    "atom_cap": ("W_X <= X^o", "actual polynomial atom", "signed/heavy-atom split"),
    "principal_mass": ("P_X <= X^o Q^2", "actual polynomial excess", "centered signed route"),
    "map_quotient": ("lossless canonical quotient", "unavoidable multiplicity", "collision theorem"),
    "cross_map": ("X_X <= X^o Q^2", "actual distinct-map excess", "signed filter"),
    "generic_affine": ("fixed-h0 signed gain", "coherent literal saturation", "change geometry/no-go"),
    "determinant_zero": ("lambda_D <= 2 eta_Z", "strict incompatibility", "direct physical route"),
    "canonical_frame": ("subpower condition cost", "polynomial condition loss", "native-h0 route"),
    "localization": ("return to prescribed h0", "average-only theorem", "qualified publication"),
    "full_return": ("exact cover or controlled remainder", "actual-support remainder", "repair/no-go"),
    "endpoint": ("Lambda_phys < 1/400", "Lambda_phys >= 1/400", "reoptimize/stop"),
}

QUEUE = tuple(range(103, 121))


def topological_order() -> list[str]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    indegree = {node: 0 for node in NODES}
    for source, target in EDGES:
        assert source in NODES and target in NODES
        outgoing[source].append(target)
        indegree[target] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for target in outgoing[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    assert len(order) == len(NODES), "dependency graph has a directed cycle"
    return order


def ancestors(target: str) -> set[str]:
    incoming: dict[str, list[str]] = defaultdict(list)
    for source, destination in EDGES:
        incoming[destination].append(source)
    seen: set[str] = set()
    stack = list(incoming[target])
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(incoming[node])
    return seen


def main() -> None:
    order = topological_order()
    allowed_tags = {"E", "H", "C"}
    allowed_levels = {"L1", "classical", "unproved", "conditional"}
    for tag, level in NODES.values():
        assert tag in allowed_tags
        assert level in allowed_levels

    hl_ancestors = ancestors("C_HL")
    required_hypotheses = {f"H{i}" for i in range(1, 10)}
    assert required_hypotheses <= hl_ancestors

    established_l2 = [
        node
        for node, (tag, level) in NODES.items()
        if tag == "E" and level == "L2"
    ]
    assert not established_l2

    for gate, record in GATES.items():
        assert gate and len(record) == 3
        assert all(field.strip() for field in record)

    assert QUEUE == tuple(range(103, 121))
    assert len(QUEUE) == 18

    rational_checks = {
        "Q_plus_J": Fraction(267, 400) + Fraction(133, 400),
        "long_fiber_gain": Fraction(267, 800) - Fraction(67, 400),
        "ttstar_double_saving": Fraction(1, 200),
        "physical_sample_margin": Fraction(1, 400) - Fraction(1, 500),
        "prime_power_exponent": Fraction(1, 2),
    }
    assert rational_checks["Q_plus_J"] == 1
    assert rational_checks["long_fiber_gain"] == Fraction(133, 800)
    assert rational_checks["ttstar_double_saving"] == 2 * Fraction(1, 400)
    assert rational_checks["physical_sample_margin"] == Fraction(1, 2000)
    assert rational_checks["prime_power_exponent"] < 1

    counts = {
        "typed_nodes": len(NODES),
        "valid_edges": len(EDGES),
        "topological_nodes": len(order),
        "hypotheses_reaching_conditional_HL": len(required_hypotheses),
        "stop_go_fallback_records": len(GATES),
        "future_queue_records": len(QUEUE),
        "rational_ledger_checks": len(rational_checks),
        "established_L2_nodes": len(established_l2),
    }

    result = {
        "schema": "tpc-mvp1-route-audit-v1",
        "status": "PASS",
        "counts": counts,
        "total_audited_records": sum(counts.values()),
        "rational_ledger": {key: str(value) for key, value in rational_checks.items()},
        "claim_boundary": {
            "finite_dependency_audit_only": True,
            "new_growing_fixed_h0_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
