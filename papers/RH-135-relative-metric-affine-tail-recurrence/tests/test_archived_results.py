import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit():
    data = load("relative_affine_audit.json")
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["transition_count"] == 330
    assert summary["zero_target_transition_count"] == 90
    assert summary["first_birth_count"] == 24
    assert summary["recurrent_transition_count"] == 216
    assert summary["recurrent_contractive_feasible_count"] == 51
    assert summary["recurrent_contractive_infeasible_count"] == 165
    assert summary["nontrivial_contractive_feasible_count"] == 75
    assert summary["recurrence_failure_count"] == 0
    assert summary["optimized_fixed_floor_subunit_count"] == 165
    assert summary["maximum_metric_factor_log10"] > 16.0
    assert summary["maximum_optimized_fixed_floor"] < 5e-6


def test_boundary_and_smoke():
    data = load("relative_affine_audit.json")
    assert data["theorem_boundary"]["relative_metric_affine_recurrence_theorem"]
    assert data["theorem_boundary"]["vanishing_absolute_forcing_obstruction"]
    assert not data["theorem_boundary"]["uniform_subunit_rho_proved"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("relative_affine_smoke.json")["audit_summary"]["transition_count"] == 8
