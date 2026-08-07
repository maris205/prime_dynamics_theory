import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archive_verification_if_present():
    report = ROOT / "results" / "archive_verification.json"
    if not report.is_file():
        return
    payload = json.loads(report.read_text())
    assert payload["status"] == "RH-375_archive_verified"
    assert payload["failure_count"] == 0
    assert payload["publication_file_count"] == 22
    assert payload["external_input_count"] == 21
