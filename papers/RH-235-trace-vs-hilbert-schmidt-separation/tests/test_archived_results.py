import json
from pathlib import Path


def test_archived_trace_hs_separation():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/trace_hs_separation_audit.json").read_text()
    )
    assert payload["endpoint_count"] == 32
    assert payload["maximum_complement_trace_square_modulus"] < 0.14
    assert payload["maximum_complement_hilbert_schmidt_squared_upper"] > 300
    assert payload["maximum_hs_squared_to_trace_square_ratio"] > 1e4
    assert payload["theorem_boundary"]["divergent_hilbert_schmidt_norm_can_coexist_with_trivial_det2"]
