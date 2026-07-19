from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_trace_norm_certificate_closes() -> None:
    data = load("bulk_trace_norm_determinant_certificate.json")
    assert data["status"] == (
        "rigorous_full_and_adaptive_bulk_square_trace_norm_and_determinant_convergence"
    )
    assert data["continuum_bulk"]["square_is_trace_class"]
    assert len(data["dimension_ledgers"]) == 15
    assert all(
        row["all_contour_gates_closed"]
        for row in data["dimension_ledgers"].values()
    )


def test_threshold_and_asymptotic_ledgers() -> None:
    data = load("bulk_trace_norm_determinant_certificate.json")
    first = data["dimension_ledgers"]["65536"]
    last = data["dimension_ledgers"]["1073741824"]
    assert first["full_bulk"]["bulk_hilbert_schmidt_error_upper"] < 0.129
    assert first["full_bulk"]["square_trace_norm_error_upper"] < 3.968
    assert last["full_bulk"]["bulk_hilbert_schmidt_error_upper"] < 3.79e-6
    assert last["full_bulk"]["square_trace_norm_error_upper"] < 1.17e-4
    assert last["determinant_disk_bounds"]["0.01"][
        "full_fredholm_determinant_error_upper"
    ] < 3.69e-4


def test_determinant_pilot_is_diagnostic_and_stabilizes_dyadically() -> None:
    data = load("stored_bulk_square_determinants.json")
    assert data["status"] == (
        "floating_stored_adaptive_bulk_square_determinant_pilot"
    )
    assert data["evidence_level"] == (
        "binary64_sparse_lu_diagnostic_not_validated"
    )
    assert set(data["levels"]) == {"2048", "4096", "8192"}
    assert data["maximum_symmetric_det2_identity_error"] < 3.0e-16
    first = data["consecutive_absolute_differences"]["2048_to_4096"]
    second = data["consecutive_absolute_differences"]["4096_to_8192"]
    for radius in data["square_parameters"]:
        key = str(radius)
        assert second[key] < 0.26 * first[key]


def test_theorem_boundary_excludes_fixed_width_and_arithmetic_claims() -> None:
    data = load("bulk_trace_norm_determinant_certificate.json")
    assert not data["main_theorems"][
        "fixed_eight_sigma_continuum_convergence_claimed"
    ]
    limitations = " ".join(data["limitations"]).lower()
    for phrase in (
        "fixed positive noise",
        "fixed eight-sigma",
        "zero-noise",
        "arithmetic trace",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    ):
        assert phrase in limitations
