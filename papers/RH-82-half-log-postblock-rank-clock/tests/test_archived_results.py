from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_clock_audit() -> None:
    audit = load("half_log_rank_audit.json")
    assert audit["precision_bits"] == 192
    assert len(audit["rows"]) == 5
    assert audit["all_executed_clock_gates_green"]
    assert audit["audit_summary"]["maximum_clock_rank"] == 7
    assert audit["audit_summary"]["maximum_relative_residual"] < 2.4e-7
    assert audit["audit_summary"]["maximum_full_future_hardy_perturbation"] < 6e-9
    assert len(audit["endpoint_linear_row_model"]["rows"]) == 6
    assert audit["endpoint_linear_row_model"]["maximum_clock_plus_two_tail"] < 1e-7


def test_boundary_is_conditional() -> None:
    boundary = load("half_log_rank_audit.json")["theorem_boundary"]
    assert boundary["endpoint_exponential_excess_rank_tail"]
    assert boundary["factor_through_resolution_transfer_criterion"]
    assert not boundary["actual_endpoint_postblock_factorization_proved"]
    assert not boundary["uniform_stage_A1_closed"]
    assert not boundary["riemann_hypothesis"]


def test_smoke_exists() -> None:
    assert len(load("half_log_rank_smoke.json")["rows"]) == 1
