import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_outward_composition_audit():
    data = load("outward_composition_audit.json")
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["transition_count"] == 330
    assert summary["raw_certification_failure_count"] == 0
    assert summary["bridge_certification_failure_count"] == 0
    assert summary["tail_dominance_failure_count"] == 0
    assert summary["support_dominance_failure_count"] == 0
    assert summary["positive_support_transition_count"] == 328
    assert summary["positive_support_chain_count"] == 28
    assert summary["terminal_above_1e-8_count"] == 21
    assert summary["terminal_above_1e-6_count"] == 16
    assert summary["terminal_above_1e-4_count"] == 12


def test_precision_gate_and_small_outward_corrections():
    summary = load("outward_composition_audit.json")["audit_summary"]
    assert summary["fp64_positive_base_count"] == 320
    assert summary["decimal16_positive_base_count"] == 318
    assert summary["decimal18_positive_base_count"] == 324
    assert summary["decimal20_positive_base_count"] == 330
    assert summary["maximum_forcing_padding"] < 3e-45
    assert summary["maximum_bound_additive_inflation"] < 3e-23


def test_boundary_and_smoke():
    data = load("outward_composition_audit.json")
    assert data["theorem_boundary"]["outward_two_residual_composition_theorem"]
    assert data["theorem_boundary"]["outward_normalized_base_lower"]
    assert not data["theorem_boundary"]["reference_assembly_is_interval_source_model"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("outward_composition_smoke.json")["audit_summary"]["transition_count"] == 18
