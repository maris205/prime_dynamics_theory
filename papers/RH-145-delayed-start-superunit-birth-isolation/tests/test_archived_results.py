import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_delayed_start_audit():
    summary = load("delayed_start_audit.json")["audit_summary"]
    assert summary["superunit_birth_count"] == 2
    assert summary["superunit_birth_anchor_count"] == 1
    assert summary["empty_kernel_superunit_count"] == 2
    assert summary["minimum_superunit_candidate_family_floor"] > 9.5
    assert summary["first_clean_suffix_cutoff"] == 0.04
    assert summary["first_clean_suffix_chain_count"] == 18
    assert summary["first_clean_suffix_minimum_terminal_floor"] > 1.5e-10


def test_boundary_and_smoke():
    data = load("delayed_start_audit.json")
    boundary = data["theorem_boundary"]
    assert boundary["finite_prefix_invariance_of_limsup_liminf"]
    assert boundary["clean_finer_anchor_suffix_from_sigma_0_04"]
    assert not boundary["all_future_levels_are_free_of_superunit_births"]
    assert not boundary["normalized_base_liminf"]
    assert not boundary["riemann_hypothesis"]
    assert load("delayed_start_smoke.json")["audit_summary"]["suffix_count"] == 2

