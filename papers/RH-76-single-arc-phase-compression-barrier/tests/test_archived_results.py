import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_phase_archive_has_negative_verdict() -> None:
    payload = json.loads((ROOT / "results" / "phase_compression_audit.json").read_text(encoding="utf-8"))
    assert payload["all_executed_moment_solves_certified"]
    assert not payload["route_verdict"]["single_arc_phase_compression_supported"]
    assert payload["route_verdict"]["effective_rank_fallback_required"]
    assert len([c for row in payload["rows"] for c in row["channels"]]) == 10


def test_finest_scale_needs_full_surrogate_depth() -> None:
    payload = json.loads((ROOT / "results" / "phase_compression_audit.json").read_text(encoding="utf-8"))
    for channel in payload["rows"][-1]["channels"]:
        assert channel["required_depth_10_percent_diagnostic"] == channel["horizon"] + 1
