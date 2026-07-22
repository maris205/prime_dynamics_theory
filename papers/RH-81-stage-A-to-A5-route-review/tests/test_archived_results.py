from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def bundles(rows):
    return {frozenset(row) for row in rows}


def test_route_review_frontiers() -> None:
    review = load("route_review.json")
    assert len(review["paper_ledger"]) == 9
    assert review["input_theorem_gate_count"] == 41
    assert review["all_input_theorem_gates_true"]
    assert bundles(review["minimal_completion_bundles"]["stage_A1"]) == {
        frozenset({"all_level_log_square_block_law"}),
        frozenset({"all_level_postblock_effective_rank_law"}),
    }
    a5 = bundles(review["minimal_completion_bundles"]["stage_A5_relative_fixed_disk_limit"])
    assert len(a5) == 2
    assert all(len(bundle) == 4 for bundle in a5)


def test_claim_boundary() -> None:
    boundary = load("route_review.json")["program_boundary"]
    assert boundary["finite_scale_end_to_end_hardy_closed"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["stage_A5_relative_limit_closed"]
    assert not boundary["self_adjoint_generator"]
    assert not boundary["riemann_hypothesis"]


def test_arb_frontier_audit() -> None:
    audit = load("arb_frontier_audit.json")
    assert audit["precision_bits"] == 256
    assert len(audit["rows"]) == 6
    assert audit["all_executed_margin_gates_green"]


def test_smoke_archives() -> None:
    assert len(load("route_review_smoke.json")["paper_ledger"]) == 1
    assert len(load("arb_frontier_smoke.json")["rows"]) == 2

