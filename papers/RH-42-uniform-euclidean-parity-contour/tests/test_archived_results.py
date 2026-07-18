from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_euclidean_grushin_archive_closes() -> None:
    data = load("euclidean_grushin_contour_certificate.json")
    assert data["status"] == (
        "rigorous_exact_stored_euclidean_parity_circle_count_one"
    )
    assert data["residual_two_upper"] < 2.0e-10
    assert data["contour_ledger"]["rouche_count_one"]
    assert data["contour_ledger"]["contour_resolvent_upper"] < 85.0


def test_euclidean_midpoint_bridge_archive_is_small() -> None:
    data = load("euclidean_stored_to_midpoint_bridge.json")
    assert data["status"] == (
        "arb_exact_stored_to_midpoint_euclidean_bridge"
    )
    assert data["support_geometry_verified_for_all_rows"]
    assert data["spectral_norm_upper"] < 1.1e-5


def test_hilbert_envelope_archive_is_rigorous() -> None:
    data = load("hilbert_schmidt_envelope_certificate.json")
    assert data["status"] == (
        "rigorous_arb_hilbert_schmidt_derivative_envelope"
    )
    for row in data["quantities"].values():
        assert row["imaginary_part_contains_zero"]
        assert row["norm_upper"] > 0.0


def test_uniform_euclidean_archive_closes_sparse_family() -> None:
    data = load("uniform_euclidean_parity_certificate.json")
    assert data["status"] == (
        "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
    )
    assert data["gate_summary"]["all_gates_closed"]
    assert data["continuum_L2_conclusion"]["inside_count"] == 1
    family = data["uniform_matrix_family"]
    assert family["certified_threshold_dimension"] == 131072
    assert (
        family["inside_count_for_full_and_adaptive_sparse_matrices"]
        == 1
    )
    assert family["uniform_adaptive_sparse_resolvent_upper"] < 839.0
    assert data["gate_summary"]["cutoff_product_upper"] < 2.0e-10
