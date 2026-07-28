import json
from pathlib import Path


def test_archived_frobenius_tail_barrier():
    payload = json.loads((Path(__file__).parents[1] / "results/frobenius_tail_audit.json").read_text())
    assert payload["endpoint_count"] == 32
    assert payload["small_tail_gate_pass_count"] == 0
    assert payload["minimum_full_frobenius_log_tail_upper"] > 1.0
    assert payload["maximum_full_frobenius_log_tail_upper"] > payload["minimum_full_frobenius_log_tail_upper"]
    assert payload["maximum_q_on_unit_disk"] < 1.0
    assert not payload["theorem_boundary"]["unit_disk_frobenius_tail_gate_passed"]
    assert not payload["theorem_boundary"]["sharper_complement_ideal_bound_ruled_out"]
