import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_counting_obstruction():
    payload = json.loads((ROOT / "results/counting_obstruction_audit.json").read_text())
    assert payload["maximum_repeated_degree"] == 256
    assert payload["maximum_repeated_distinct_support"] == 4
    assert payload["theorem_boundary"]["growing_divisor_required_for_spectral_count"]
    assert not payload["theorem_boundary"]["growing_physical_divisor_constructed"]
