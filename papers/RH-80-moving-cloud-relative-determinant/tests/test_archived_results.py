from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit_boundary() -> None:
    audit = load("cloud_renormalization_audit.json")
    boundary = audit["theorem_boundary"]
    assert boundary["fixed_pole_cancellation_failure_in_canonical_model"]
    assert boundary["exact_reducing_cloud_factorization"]
    assert boundary["uniform_complement_trace_norm_is_sufficient"]
    assert not boundary["actual_cloud_riesz_projection_constructed"]
    assert not boundary["uniform_complement_trace_norm_proved"]
    assert not boundary["stage_A5_closed"]
    assert not boundary["riemann_hypothesis"]


def test_cloud_archive_gate() -> None:
    audit = load("cloud_renormalization_audit.json")
    assert len(audit["archived_cloud_rows"]) == 7
    finest = audit["finest_cloud_gate"]
    assert finest["sigma"] == 0.0001
    assert finest["degree"] == 7
    assert finest["central_profile_mean_error_upper"] < 0.037
    assert finest["central_profile_max_error_upper"] < 0.117
    assert 0.11 < finest["relative_center_mismatch_upper"] < 0.12


def test_smoke_audit_exists() -> None:
    smoke = load("cloud_renormalization_smoke.json")
    assert len(smoke["archived_cloud_rows"]) == 1

