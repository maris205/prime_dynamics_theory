import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_obstruction_audit():
    payload = json.loads((ROOT / "results/frobenius_obstruction_audit.json").read_text())
    assert payload["window_count"] == 126
    assert payload["root_case_count"] == 416
    assert payload["one_root_complement_free_compatible_count"] == 0
    assert payload["whole_packet_complement_free_compatible_count"] == 0
    assert payload["one_root_complement_burden_range"] == {"minimum": 63, "maximum": 255}
