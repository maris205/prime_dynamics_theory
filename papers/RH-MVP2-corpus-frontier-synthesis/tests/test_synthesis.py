from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_inventory_is_consecutive_and_claim_safe() -> None:
    payload = json.loads((ROOT / "results/corpus_inventory.json").read_text())
    assert payload["numbered_paper_count"] == 361
    assert payload["unique_numbers"] == list(range(1, 362))
    assert payload["review_anchor_count"] == 29
    assert payload["review_anchor_coverage_union_count"] == 349
    assert set(payload["legacy_alias_groups"]) == {"302", "303", "304", "306"}
    assert payload["route_coordinate"] == "actual_same_clock_unnormalized_head_transport_open"
    assert payload["first_missing_leaf"] == "D_(4k)(R)->0"
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["forbidden_claims"].values())


def test_canonical_sources_have_publication_anchors() -> None:
    payload = json.loads((ROOT / "results/corpus_inventory.json").read_text())
    for record in payload["canonical"].values():
        assert record["required"]["readme"]
        assert record["required"]["main_tex"]
        assert record["required"]["pdf"]


def test_summary_and_firewall_files_exist() -> None:
    for relative in (
        ".gitignore",
        "Makefile",
        "README.md",
        "CROSSWALK.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "results/summary.json",
        "results/dependency_manifest.json",
    ):
        assert (ROOT / relative).exists(), relative
