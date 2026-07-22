import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_shrinking_disk_archive_is_green() -> None:
    payload = json.loads((ROOT / "results" / "determinant_transfer_audit.json").read_text(encoding="utf-8"))
    assert payload["all_executed_shrinking_disk_gates_green"]
    values = [row["shrinking_disk_determinant_error_upper"] for row in payload["rows"]]
    assert all(right < left for left, right in zip(values, values[1:]))


def test_fixed_disk_bound_worsens() -> None:
    payload = json.loads((ROOT / "results" / "determinant_transfer_audit.json").read_text(encoding="utf-8"))
    assert payload["fixed_disk_standard_bound_eventually_worsens"]
    assert payload["rows"][-1]["fixed_disk_determinant_error_upper"] > payload["rows"][1]["fixed_disk_determinant_error_upper"]
