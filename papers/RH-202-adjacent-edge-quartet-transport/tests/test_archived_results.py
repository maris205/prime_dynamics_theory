import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_transport_obstruction_and_boundaries():
    payload = json.loads((ROOT / "results/adjacent_transport_audit.json").read_text())
    assert payload["adjacent_case_count"] == 4
    assert payload["mode_transport_count"] == 16
    assert payload["maximum_right_subspace_sine"] > 0.82
    assert payload["maximum_left_subspace_sine"] > 0.82
    assert payload["maximum_oblique_projector_defect"] > 2.29
    assert payload["theorem_boundary"]["finite_floating_projector_transport"]
    assert not payload["theorem_boundary"]["all_level_shell_map"]
    assert not payload["theorem_boundary"]["gate_A"]
