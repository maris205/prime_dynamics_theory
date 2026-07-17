from __future__ import annotations

import json
from pathlib import Path

from resolvent_atlas import sha256_file, verify_leaf_ledger


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def load_json(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_summary_closes_boundary_but_not_interior_count() -> None:
    summary = load_json("summary.json")
    assert summary["status"] == (
        "rigorous_full_boundary_resolvent_atlas_and_relative_winding_one_"
        "interior_complement_count_open"
    )
    assert summary["center_count"] == 109
    assert summary["rh28_parent_center_count"] == 88
    assert summary["adaptive_center_count"] == 21
    assert summary["refined_leaf_count"] == 949
    assert summary["whole_parent_arc_count"] == 933
    assert summary["exact_rational_partition_verified"]
    assert summary["full_boundary_rouche_inequality_certified"]
    assert summary["stored_feshbach_boundary_winding"] == 1
    assert summary["exact_augmented_block_minus_complement_count"] == 1
    assert not summary["interior_complement_pole_count_certified"]
    assert not summary["ordinary_feshbach_zero_count_certified"]
    assert summary["maximum_neumann_product_upper"] < 1.0
    assert summary["maximum_budget_ratio_upper"] < 1.0


def test_all_center_certificate_files_are_hashed_and_admissible() -> None:
    manifest = load_json("center_manifest_sigma_1e-02.json")
    assert manifest["center_count"] == 109
    identifiers = set()
    for row in manifest["centers"]:
        path = ROOT / row["path"]
        assert sha256_file(path) == row["sha256"]
        assert float(row["residual_upper"]) < 1.0
        assert float(row["inverse_upper"]) > 0.0
        identifiers.add(row["center_id"])
    assert len(identifiers) == 109


def test_leaf_ledger_is_exact_closed_partition() -> None:
    audit = verify_leaf_ledger(
        ROOT / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    )
    assert audit["leaf_count"] == 949
    assert audit["closed_leaf_count"] == 949
    assert audit["unresolved_leaf_count"] == 0
    assert audit["exact_rational_partition_verified"]
    assert audit["maximum_neumann_product_upper"] < 1.0
    assert audit["maximum_budget_ratio_upper"] < 1.0
    assert len(audit["used_center_ids"]) == 109


def test_dependency_and_result_hashes() -> None:
    dependency = load_json("dependency_manifest.json")
    summary = load_json("summary.json")
    assert dependency["status"] == "all_consumed_upstream_files_hashed"
    for group in ("inputs", "sources"):
        for row in dependency[group].values():
            path = REPOSITORY / row["path"]
            assert sha256_file(path) == row["sha256"]
    for name, expected in summary["result_hashes"].items():
        assert sha256_file(ROOT / "results" / name) == expected
