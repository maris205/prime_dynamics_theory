from __future__ import annotations

import csv
import json
from pathlib import Path

from certificate_ledger import sha256_file


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def load_json(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_projected_count_archive() -> None:
    payload = load_json("projected_count_certificates.json")
    assert payload["status"] == "rigorous_exact_binary64_projected_counts"
    assert payload["model_family"] == "RH-28 reconstructed primal base realizations"
    assert len(payload["scales"]) == 3
    for row in payload["scales"]:
        assert row["projected_zero_count"] == 1
        assert row["projected_pole_count"] == 0
        assert row["projected_determinant_winding"] == 1
        assert row["augmented"]["ambiguous_count"] == 0
        assert row["projected_poles"]["ambiguous_count"] == 0
        model = REPOSITORY / row["model_path"]
        assert sha256_file(model) == row["model_sha256"]


def test_rh28_reconstruction_is_exact_and_not_silently_rh24() -> None:
    reconstruction = load_json("model_reconstruction_audit.json")
    verification = load_json("rh28_reconstruction_verification.json")
    assert reconstruction["status"] == "deterministic_rh28_base_snapshots_archived"
    assert verification["status"] == (
        "all_deterministic_rh28_fields_exactly_reproduced"
    )
    assert len(verification["scales"]) == 3
    for relation in reconstruction["scales"]:
        assert not relation["bitwise_equal_to_rh24_discovery_model"]
        assert relation["maximum_absolute_entry_difference"] > 0.0
    for row in verification["scales"]:
        assert row["arc_mismatch_count"] == 0
        assert row["summary_mismatch_count"] == 0
        assert row["snapshot_matches_fresh_rebuild_bitwise"]
        assert row["status"] == "exact_archive_reproduction"


def test_composition_archive_is_local_not_global() -> None:
    with (ROOT / "results" / "composition_summary.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert [int(row["accepted_arc_count"]) for row in rows] == [936, 2065, 6368]
    for row in rows:
        assert int(row["transport_closed_arc_count"]) == 1
        assert int(row["neumann_failure_arc_count"]) == int(
            row["accepted_arc_count"]
        ) - 1
        assert int(row["ambiguous_arc_count"]) == 0
        assert int(row["selected_arc_closed"]) == 1
        assert int(row["full_contour_closed"]) == 0
        assert float(row["selected_arc_neumann_product_upper"]) < 1.0
        assert float(row["nearest_unselected_neumann_product_lower"]) > 1.0


def test_dependency_and_object_identity_archives() -> None:
    dependency = load_json("dependency_ledger.json")
    identity = load_json("object_identity_checks.json")
    assert dependency["status"] == "all_recorded_upstream_hashes_verified"
    assert all(dependency["checks"].values())
    assert all(edge["verified"] for edge in dependency["edges"])
    assert identity["status"] == "all_cross_paper_object_identities_verified"
    assert all(identity["checks"].values())
    for node in dependency["nodes"].values():
        assert sha256_file(REPOSITORY / node["path"]) == node["sha256"]


def test_summary_result_hashes() -> None:
    summary = load_json("summary.json")
    assert summary["status"] == (
        "projected_base_certified_selected_arcs_closed_full_contours_open"
    )
    assert len(summary["remaining_gates"]) == 2
    for name, expected in summary["result_hashes"].items():
        assert sha256_file(ROOT / "results" / name) == expected
