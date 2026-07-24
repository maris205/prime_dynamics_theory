import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_metric_balanced_audit():
    data = load("metric_balanced_audit.json")
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["recurrent_transition_count"] == 216
    assert summary["orthogonal_contractivity_possible_count"] == 183
    assert summary["orthogonal_contractivity_impossible_count"] == 33
    assert summary["polar_contractive_feasible_count"] == 51
    assert summary["balanced_contractive_feasible_count"] == 183
    assert summary["newly_recovered_contractive_count"] == 132
    assert summary["lost_polar_contractive_count"] == 0
    assert summary["balanced_subunit_fixed_floor_count"] == 183
    assert summary["maximum_balanced_fixed_floor"] < 0.0026


def test_boundary_and_smoke_archive():
    data = load("metric_balanced_audit.json")
    assert data["theorem_boundary"]["orthogonal_metric_minimax_theorem"]
    assert data["theorem_boundary"]["metric_contractivity_lower_obstruction"]
    assert not data["theorem_boundary"]["global_affine_objective_optimizer_proved"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    smoke = load("metric_balanced_smoke.json")["audit_summary"]
    assert smoke["recurrent_transition_count"] == 7
