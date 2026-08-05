from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data() -> dict:
    return json.loads((ROOT / "results/volume_audit.json").read_text())


def test_inventory_and_series_boundary() -> None:
    payload = data()
    assert payload["series"] == {
        "volume": 4,
        "source_range": [282, 361],
        "numbered_endpoint_changed": False,
        "atomic_sources_preserved": True,
    }
    assert payload["numbered_paper_count"] == 80
    assert payload["atomic_index_count"] == 80
    assert payload["unique_numbers"] == list(range(282, 362))
    assert payload["consecutive_numbering"]
    assert set(payload["legacy_alias_groups"]) == {"302", "303", "304", "306"}


def test_review_phases_cover_the_range() -> None:
    payload = data()
    assert payload["review_anchor_numbers"] == [291, 301, 311, 321, 331, 341, 351, 361]
    covered = []
    for phase in payload["phase_ranges"]:
        covered.extend(range(phase["start"], phase["end"] + 1))
    assert covered == list(range(282, 362))


def test_typed_frontier_is_not_promoted() -> None:
    payload = data()
    assert payload["typed_identities"] == ["p=tau-a=q-d", "d=h-s", "q=p+d", "h=s+d"]
    assert payload["actual_branch_range"] == [352, 354]
    assert payload["deterministic_branch_range"] == [355, 360]
    assert not payload["same_clock_bridge_proved"]
    assert not payload["physical_obstruction_proved"]
    assert payload["route_coordinate"] == "actual_same_clock_unnormalized_head_transport_open"
    assert payload["first_missing_leaf"] == "D_(4k)(R)->0"
    assert not payload["rh_362_activated"]
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["forbidden_claims"].values())


def test_publication_sources_exist() -> None:
    for relative in (
        "README.md",
        "CROSSWALK.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "experiments/build_volume_audit.py",
        "experiments/build_archive.py",
        "experiments/verify_archive.py",
    ):
        assert (ROOT / relative).exists(), relative
