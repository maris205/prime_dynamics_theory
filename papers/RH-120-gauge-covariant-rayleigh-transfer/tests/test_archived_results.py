from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    audit = load("gauge_transfer_audit.json")
    summary = audit["audit_summary"]
    assert summary["sample_count"] == 4096
    assert summary["hypothesis_failure_count"] == 0
    assert summary["gamma_failure_count"] == 0
    assert summary["volume_failure_count"] == 0
    assert summary["sharp_gamma_relative_error"] < 1e-12
    assert summary["sharp_volume_relative_error"] < 1e-12


def test_smoke_and_boundary() -> None:
    assert load("gauge_transfer_smoke.json")["audit_summary"]["sample_count"] == 128
    boundary = load("gauge_transfer_audit.json")["theorem_boundary"]
    assert boundary["gauge_covariant_gamma_transfer"]
    assert boundary["four_volume_transfer"]
    assert not boundary["all_level_physical_gauge_law_proved"]
    assert not boundary["riemann_hypothesis"]

