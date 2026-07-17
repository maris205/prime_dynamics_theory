from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from complement_poles import classify_binary64_diagonal, sha256_array


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_schur_certificate_closes_the_stored_interior_count() -> None:
    result = load_json("schur_similarity_sigma_1e-02.json")
    assert result["status"] == (
        "rigorous_stored_complement_count_zero_and_ordinary_winding_one"
    )
    assert result["scope"] == "exact finite model defined by stored binary64 factors"
    assert result["physical_dimension"] == 2048
    assert result["rh33_leaf_count"] == 949
    assert result["rh33_exact_rational_partition_verified"]
    assert result["schur_residual_frobenius_upper"] < 1.0e-8
    assert result["unitarity_defect_frobenius_upper"] < 1.0
    assert result["maximum_homotopy_neumann_product_upper"] < 1.0
    assert result["all_leaf_homotopies_certified"]
    assert result["triangular_inside_count"] == 0
    assert result["triangular_boundary_count"] == 0
    assert result["interior_complement_pole_count_certified"]
    assert result["interior_complement_pole_count"] == 0
    assert result["ordinary_feshbach_zero_count_certified"]
    assert result["ordinary_feshbach_zero_count"] == 1
    assert result["stored_augmented_block_inside_count"] == 1


def test_archived_diagonal_reclassifies_exactly() -> None:
    result = load_json("schur_similarity_sigma_1e-02.json")
    with np.load(ROOT / result["diagonal_npz"]) as archive:
        diagonal = np.asarray(archive["diagonal"])
        center = complex(archive["contour_center"].item())
        radius = float(archive["contour_radius"].item())
    assert sha256_array(diagonal) == result["triangular_diagonal_sha256"]
    classification = classify_binary64_diagonal(diagonal, center, radius)
    assert classification.inside_count == 0
    assert classification.outside_count == 2048
    assert classification.boundary_count == 0
    assert classification.nearest_index == result["nearest_diagonal_index"]


def test_every_archived_leaf_homotopy_is_closed() -> None:
    result = load_json("schur_similarity_sigma_1e-02.json")
    with (ROOT / result["homotopy_ledger"]).open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 949
    assert all(row["homotopy_certified"] == "True" for row in rows)
    assert max(float(row["homotopy_neumann_product_upper"]) for row in rows) < 1.0
    assert min(float(row["homotopy_denominator_lower"]) for row in rows) > 0.0


def test_compact_summary_and_dependency_hashes() -> None:
    summary = load_json("summary.json")
    dependency = load_json("dependency_manifest.json")
    assert summary["status"] == (
        "rigorous_stored_complement_count_zero_and_ordinary_winding_one"
    )
    assert dependency["status"] == "all_consumed_inputs_and_sources_hashed"
    for name, expected in summary["result_hashes"].items():
        digest = hashlib.sha256((ROOT / "results" / name).read_bytes()).hexdigest()
        assert digest == expected
