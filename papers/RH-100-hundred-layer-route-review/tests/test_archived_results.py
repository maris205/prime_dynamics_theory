from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str): return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_inventory() -> None:
    review = load("hundred_layer_route_review.json")
    summary = review["inventory_summary"]
    assert summary["paper_count"] == 99
    assert summary["first_layer"] == 1
    assert summary["last_layer"] == 99
    assert summary["readme_count"] == 99
    assert summary["main_tex_count"] == 99
    assert summary["paper_pdf_count"] == 99
    assert summary["summary_count"] == 70
    assert len(review["exact_milestones"]) >= 19
    assert len(review["negative_route_markers"]) >= 15


def test_frontier() -> None:
    review = load("hundred_layer_route_review.json")
    assert len(review["stage_A_minimal_completion_bundles"]) == 3
    assert len(review["stage_A5_minimal_completion_bundles"]) == 3
    assert ["L_all_level_full_block_law"] in review["stage_A_minimal_completion_bundles"]
    assert review["preferred_packet_bundle"] in review["stage_A_minimal_completion_bundles"]
    assert [plan["layer"] for plan in review["next_three_layers"]] == [101, 102, 103]


def test_claim_boundary() -> None:
    boundary = load("hundred_layer_route_review.json")["claim_boundary"]
    assert not boundary["unconditional_stage_A_closed"]
    assert not boundary["moving_cloud_A5_closed"]
    assert not boundary["self_adjoint_hilbert_polya_operator"]
    assert not boundary["zeta_zero_identification"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_inventory() -> None:
    smoke = load("hundred_layer_route_review_smoke.json")
    assert smoke["inventory_summary"]["paper_count"] == 10
