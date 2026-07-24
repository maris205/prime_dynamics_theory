import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_finite_horizon_audit():
    data = load("finite_horizon_audit.json")
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["transition_count"] == 330
    assert summary["recurrent_transition_count"] == 216
    assert summary["long_run_blocked_recurrent_count"] == 33
    assert summary["long_run_blocked_but_finite_safe_count"] == 31
    assert summary["long_run_blocked_and_finite_unsafe_count"] == 2
    assert summary["greedy_safe_transition_count"] == 328
    assert summary["actual_safe_transition_count"] == 328
    assert summary["greedy_safe_chain_count"] == 28
    assert summary["actual_safe_chain_count"] == 28
    assert summary["polar_safe_chain_count"] == 21
    assert summary["dominance_failure_count"] == 0


def test_two_failures_are_physical_birth_obstructions():
    data = load("finite_horizon_audit.json")
    failed = [step for row in data["rows"] for step in row["steps"] if not step["greedy"]["safe"]]
    assert len(failed) == 2
    assert all(step["actual_target"]["value"] > 1.0 for step in failed)
    assert all(step["greedy"]["birth"]["value"] > 1.0 for step in failed)


def test_boundary_and_smoke():
    data = load("finite_horizon_audit.json")
    assert data["theorem_boundary"]["pointwise_optimal_young_envelope"]
    assert data["theorem_boundary"]["greedy_horizon_optimality_within_finite_candidate_family"]
    assert not data["theorem_boundary"]["global_orthogonal_horizon_optimizer"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("finite_horizon_smoke.json")["audit_summary"]["transition_count"] == 18
