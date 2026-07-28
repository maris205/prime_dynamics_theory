import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_block_diagnostic_is_finite_not_uniform():
    payload = json.loads((ROOT / "results/block_power_audit.json").read_text())
    assert payload["source_endpoint_count"] == 17
    assert payload["block_size"] == 12
    assert payload["finite_sample_geometric_rate_q12"] < 0.4
    assert payload["finite_sample_unit_disk_logarithmic_tail_bound_from_order_12"] < 2e-5
    assert payload["minimum_first_contractive_power_depth"] == 3
    assert payload["maximum_first_contractive_power_depth"] == 7
    boundary = payload["theorem_boundary"]
    assert boundary["block_power_trace_envelope_criterion"] is True
    assert boundary["uniform_noise_block_constants"] is False
    assert boundary["uniform_all_order_trace_envelope"] is False
