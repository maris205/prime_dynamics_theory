from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data() -> dict:
    return json.loads((ROOT / "results/volume_audit.json").read_text())


def test_inventory_and_phase_cover() -> None:
    payload = data()
    assert payload["numbered_paper_count"] == 81
    assert payload["atomic_index_count"] == 81
    assert payload["unique_numbers"] == list(range(161, 242))
    assert payload["review_anchor_numbers"] == [161, 171, 181, 191, 201, 211, 221, 231, 241]
    covered = []
    for phase in payload["phase_ranges"]:
        covered.extend(range(phase["start"], phase["end"] + 1))
    assert covered == list(range(161, 242))


def test_finite_counts_remain_finite() -> None:
    payload = data()
    assert payload["finite_review_item_counts"] == {
        "171": 3584, "181": 2600, "191": 2960, "201": 1352,
        "211": 649, "221": 2140, "231": 9870, "241": 7280,
    }
    assert payload["finite_review_item_total"] == 30435


def test_typed_assembly_and_frontier() -> None:
    payload = data()
    assert payload["typed_assembly"]["abstract_implication_proved"]
    assert payload["typed_assembly"]["determinant_types"] == [1, 2]
    assert all(value is False for value in payload["typed_assembly"]["physical_interfaces"].values())
    assert payload["fixed_order_trace_envelope_max_order"] == 12
    assert not payload["moving_noisy_all_order_trace_envelope_proved"]
    assert not payload["no_over_extraction_coefficient_anchor_proved"]
    assert payload["route_coordinate"] == "physical_riesz_cloud_assembled_moving_noisy_trace_envelope_open"
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["forbidden_claims"].values())


def test_publication_sources_exist() -> None:
    for relative in (
        "README.md", "CROSSWALK.md", "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md", "main.tex",
        "experiments/build_volume_audit.py", "experiments/build_archive.py",
        "experiments/verify_archive.py",
    ):
        assert (ROOT / relative).exists(), relative
