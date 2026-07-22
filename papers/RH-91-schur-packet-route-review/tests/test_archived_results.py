from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_route_review() -> None:
    review = load("route_review.json")
    assert len(review["layer_ledger"]) == 9
    assert review["archive_audit"]["theorem_flag_count"] == 29
    assert review["archive_audit"]["all_theorem_flags_green"]
    assert review["archive_audit"]["all_uniform_stage_A_boundaries_open"]
    budgets = {row["tolerance"]: row["updates"] for row in review["bootstrap_budget"]}
    assert budgets[1e-6] == 20
    assert budgets[1e-12] == 39
    assert review["route_frontier"]["stage_A_minimal_bundles"] == [["L"], ["O", "R", "S"]]


def test_boundaries() -> None:
    boundary = load("route_review.json")["theorem_boundary"]
    assert boundary["schur_to_effective_rank_bootstrap"]
    assert boundary["revised_completion_frontier"]
    assert not boundary["uniform_schur_margin_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["hilbert_polya_operator"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("route_review_smoke.json")["bootstrap_budget"]) == 2
