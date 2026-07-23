from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load(name: str): return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))

def test_full_audit() -> None:
    audit = load("exterior_concentration_audit.json")
    s = audit["audit_summary"]
    assert (s["scale_count"], s["channel_count"], s["update_count"], s["fine_update_count"]) == (5, 10, 360, 234)
    assert s["concentration_enclosure_failure_count"] == 0
    assert s["maximum_concentration"] < 2.34
    assert s["minimum_fine_refinement_gain"] > 1.83
    expected = {"1e-08": (78, 78, 78), "1e-06": (65, 69, 72), "1e-04": (42, 55, 55)}
    for key, counts in expected.items():
        row = audit["threshold_summary"][key]
        assert (row["fine_generic_support_count"], row["fine_refined_support_count"], row["fine_spectral_support_count"]) == counts

def test_barrier_and_boundary() -> None:
    audit = load("exterior_concentration_audit.json")
    for row in audit["barrier"]["rows"]:
        assert row["flat_concentration"] == row["dimension"]
        assert row["rank_four_concentration"] == 1.0
    boundary = audit["theorem_boundary"]
    assert boundary["tail_energy_concentration_upper_bound"]
    assert boundary["refined_trace_exterior_certificate"]
    assert not boundary["all_level_exterior_concentration_law_proved"]
    assert not boundary["uniform_stage_A_closed"]

def test_smoke() -> None:
    assert load("exterior_concentration_smoke.json")["audit_summary"]["update_count"] == 24
