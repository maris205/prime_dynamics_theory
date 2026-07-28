import json
from pathlib import Path


def test_archived_periodic_superloop_audit():
    payload = json.loads(
        (Path(__file__).parents[1] / "results/periodic_superloop_audit.json").read_text()
    )
    assert payload["enumerated_loop_identity_case_count"] == 12
    assert payload["archived_determinant_relevant_trace_case_count"] == 352
    assert payload["archived_sign_counts"] == {"negative": 179, "positive": 173, "zero": 0}
    assert payload["every_archived_order_has_both_signs"]
    boundary = payload["theorem_boundary"]
    assert boundary["projection_free_graded_counterloop_representation"]
    assert not boundary["uniform_all_order_trace_envelope"]
    assert not boundary["deterministic_numerator_coefficient_anchor"]
    assert not boundary["gate_A"]
