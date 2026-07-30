import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["physical_folded_row_formula_proved"] is True
    assert data["exact_same_clearance_tv_identity_proved"] is True
    assert data["clearance_phase_nonuniversality_proved"] is True
    assert data["phase_independent_universal_profile_proved"] is False
    assert data["joint_first_alias_trace_law_proved"] is False
    assert data["full_trace_replacement_proved"] is False
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_hypothesis_proved"] is False
    assert not any(data["gates"].values())
