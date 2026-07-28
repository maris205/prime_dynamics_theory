import json
from pathlib import Path


def test_archived_determinant_frontier_review():
    payload = json.loads((Path(__file__).parents[1] / "results/determinant_frontier_review.json").read_text())
    assert payload["paper_numbers"] == list(range(222, 231))
    assert payload["identity_failure_count"] == 0
    assert payload["finite_ledger_items"] > 9000
    assert not any(payload["macro_gates"].values())
    assert payload["statuses"]["rank_growing_cloud"]
    assert not payload["statuses"]["uniform_complement_ideal_control"]
    assert not payload["theorem_boundary"]["riemann_hypothesis_implication"]
