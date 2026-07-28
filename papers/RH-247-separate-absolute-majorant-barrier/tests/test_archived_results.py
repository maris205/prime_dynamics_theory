import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_absolute_barrier():
    payload = json.loads((ROOT / "results/absolute_majorant_audit.json").read_text())
    assert payload["case_count"] == 352
    assert payload["case_root_rates_above_one_count"] == 352
    assert payload["minimum_case_root_rate"] > 1.25
    assert payload["maximum_case_majorant_over_residual"] > 1e15
    boundary = payload["theorem_boundary"]
    assert boundary["absolute_majorant_can_prove_subunit_envelope"] is False
    assert boundary["signed_or_grouped_quotient_route_excluded"] is False
    assert boundary["gate_A"] is False
