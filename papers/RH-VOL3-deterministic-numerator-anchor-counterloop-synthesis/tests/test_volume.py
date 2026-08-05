from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data() -> dict:
    return json.loads((ROOT / "results/volume_audit.json").read_text())


def test_inventory_and_phase_cover() -> None:
    payload = data()
    assert payload["numbered_paper_count"] == 40
    assert payload["atomic_index_count"] == 40
    assert payload["unique_numbers"] == list(range(242, 282))
    assert payload["review_anchor_numbers"] == [251, 261, 271, 281]
    covered = []
    for phase in payload["phase_ranges"]:
        covered.extend(range(phase["start"], phase["end"] + 1))
    assert covered == list(range(242, 282))


def test_deterministic_results_and_physical_boundary() -> None:
    payload = data()
    envelope = payload["deterministic_envelope"]
    assert envelope["proved"]
    assert envelope["constant"] == 48
    assert envelope["start_order"] == 2
    assert envelope["sharp_ratio_limit"] == 1
    assert payload["deterministic_counterloop_bridge_proved"]
    assert not payload["actual_cloud_coefficient_bridge_proved"]
    assert not payload["aggregate_noisy_cloud_transport_proved"]
    assert not payload["variable_rank_quotient_instantiated"]


def test_claim_firewall() -> None:
    payload = data()
    assert payload["route_coordinate"] == "deterministic_all_order_closed_actual_cloud_identification_open"
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
