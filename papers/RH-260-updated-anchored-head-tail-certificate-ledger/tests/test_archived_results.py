import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_updated_certificate_ledger():
    payload = json.loads(
        (ROOT / "results/updated_certificate_ledger.json").read_text()
    )
    assert payload["target_tail"]["analytic_interface_exists"] is True
    assert payload["target_tail"]["certified_boundary_supremum_available"] is False
    assert payload["anchored_head"]["audited_endpoint_count"] == 32
    assert payload["anchored_head"]["audited_class_endpoint_case_count"] == 64
    assert payload["anchored_head"]["total_pass_count"] == 0
    assert payload["quotient_tail"]["finite_endpoint_count"] == 23
    assert payload["quotient_tail"]["power_12_contractive_count"] == 23
    assert payload["quotient_tail"]["remaining_archived_endpoint_count"] == 9
    assert payload["quotient_tail"]["uniform_small_noise_certificate"] is False
    assert payload["complete_certificate_count"] == 0
    assert payload["component_status"]["satisfied_component_count"] == 1
    assert payload["component_status"]["complete"] is False
    assert payload["source_consistency_audit"]["failure_count"] == 0
    assert all(
        payload["theorem_boundary"][f"gate_{letter}"] is False
        for letter in "ABCDE"
    )
