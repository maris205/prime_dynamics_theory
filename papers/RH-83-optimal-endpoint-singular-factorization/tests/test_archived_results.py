from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_factorization_audit() -> None:
    audit = load("singular_factorization_audit.json")
    assert audit["precision_bits"] == 192
    assert len(audit["rows"]) == 5
    assert audit["all_executed_factorization_gates_green"]
    summary = audit["audit_summary"]
    assert summary["maximum_optimal_factor_constant"] < 0.162
    assert summary["maximum_optimal_remainder"] < 1.24e-9
    assert summary["minimum_coordinate_dictionary_relative_residual"] > 0.46
    assert summary["maximum_factor_rank_defect_from_clock"] <= 1


def test_boundary() -> None:
    boundary = load("singular_factorization_audit.json")["theorem_boundary"]
    assert boundary["optimal_singular_factorization_theorem"]
    assert not boundary["coordinate_identity_endpoint_route_supported"]
    assert not boundary["all_level_singular_majorization_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("singular_factorization_smoke.json")["rows"]) == 1
