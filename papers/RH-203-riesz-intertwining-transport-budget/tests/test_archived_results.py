import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def test_archived_identity_ledger():
    payload = json.loads((ROOT / "results/riesz_transport_identity_audit.json").read_text())
    assert payload["resolvent_identity_case_count"] == 120
    assert payload["channel_decomposition_case_count"] == 120
    assert payload["identity_failure_count"] == 0
    assert payload["maximum_resolvent_identity_residual"] < 1e-12
    assert payload["maximum_channel_identity_residual"] < 1e-10
    assert payload["theorem_boundary"]["riesz_projector_transport_identity"]
    assert not payload["theorem_boundary"]["closed_physical_transport_certificate"]
