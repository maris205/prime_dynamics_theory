import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_archived_branch_correspondence():
    p=json.loads((ROOT/"results/branch_correspondence_audit.json").read_text())
    assert p["unique_assignment_case_count"] == p["adjacent_case_count"] == 4
    assert p["minimum_pointwise_assignment_margin"] > 0.088
    assert p["maximum_left_right_branch_mismatch"] < 0.008
    assert p["maximum_descriptive_displacement_ratio"] < 0.359
    assert not p["theorem_boundary"]["asymptotic_branch_convergence"]
