import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_route_review_archive_is_present() -> None:
    route = json.loads(
        (ROOT / "results" / "route_review.json").read_text(encoding="utf-8")
    )
    arb = json.loads(
        (ROOT / "results" / "arb_bridge_slack_audit.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(route["paper_ledger"]) == 9
    assert route["frontiers"]["finite_scale"] == [
        "upstream_interval_triple"
    ]
    assert set(route["frontiers"]["stage_A1"]) == {
        "upstream_interval_triple",
        "uniform_family_scaling",
    }
    assert arb["all_one_percent_slacks_positive"]
