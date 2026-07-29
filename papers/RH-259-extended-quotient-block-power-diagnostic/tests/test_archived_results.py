import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_extended_quotient_diagnostic():
    payload = json.loads((ROOT / "results/extended_quotient_audit.json").read_text())
    assert payload["maximum_dimension"] == 1024
    assert payload["eligible_endpoint_count"] == 23
    assert payload["new_endpoint_count"] == 6
    assert payload["rank_mismatch_count"] == 0
    assert payload["power_12_contractive_count"] == 23
    assert payload["maximum_q12"] < 1.0
    assert payload["maximum_q12"] > payload["inherited_rh246_q12"]
    assert payload["theorem_boundary"]["finite_dimension_1024_diagnostic"] is True
    assert payload["theorem_boundary"]["all_eligible_power_12_blocks_contractive"] is True
    assert payload["theorem_boundary"]["uniform_small_noise_block_power"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
