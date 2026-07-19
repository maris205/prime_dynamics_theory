from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_main_certificate_closes() -> None:
    data = load("small_noise_mesh_double_pole_certificate.json")
    assert data["status"] == (
        "rigorous_markov_mesh_laws_two_step_double_pole_obstruction_and_conditional_bulk_route"
    )
    theorem = data["raw_markov_resolution_theorems"]
    assert theorem["one_step_hilbert_schmidt_sufficient_condition"] == (
        "n(sigma)*sigma^(3/2)->infinity"
    )
    assert theorem["two_step_trace_norm_sufficient_condition"] == (
        "n(sigma)*sigma^2->infinity"
    )


def test_power_schedule_gates() -> None:
    data = load("small_noise_mesh_double_pole_certificate.json")
    schedules = data["power_schedule_audit"]
    assert not schedules["1.5"]["hilbert_schmidt_converges"]
    assert schedules["2.0"]["hilbert_schmidt_converges"]
    assert not schedules["2.0"]["square_trace_norm_converges"]
    assert schedules["2.25"]["square_trace_norm_converges"]
    assert schedules["2.5"]["square_trace_norm_converges"]


def test_double_pole_and_uniform_peripheral_boundary() -> None:
    data = load("small_noise_mesh_double_pole_certificate.json")
    pole = data["two_step_small_noise_obstruction"]
    assert pole["two_step_factor"] == (
        "D_0,square(w)=H(w)/(1-w/lambda)^2"
    )
    assert not pole["locally_uniform_entire_small_noise_limit"]
    assert not pole["family_locally_bounded_on_disks_R_gt_lambda"]
    assert not data["conditional_bulk_extension"]["proved_uniformly_in_sigma"]


def test_gaussian_row_pilot_reaches_asymptotic_constant() -> None:
    data = load("gaussian_row_projection_pilot.json")
    assert data["status"] == (
        "floating_exact_gaussian_row_cell_projection_pilot"
    )
    assert data["finest_relative_error"] < 1.0e-6


def test_squared_cloud_pilot_identity_and_scope() -> None:
    data = load("two_step_square_cloud_pilot.json")
    assert data["status"] == (
        "floating_two_step_squared_resonance_cloud_scattering_pilot"
    )
    assert data["maximum_ideal_cloud_polynomial_identity_error"] < 4.0e-15
    assert set(data["levels"]) == {
        "0.01",
        "0.004",
        "0.002",
        "0.001",
        "0.0005",
        "0.0002",
        "0.0001",
    }
    assert data["levels"]["0.0001"]["effective_degree"] == 7


def test_theorem_boundaries_are_explicit() -> None:
    data = load("small_noise_mesh_double_pole_certificate.json")
    text = " ".join(data["limitations"]).lower()
    for phrase in (
        "markov kernel",
        "weighted-riesz",
        "not proved",
        "cell-average",
        "not a necessary",
        "floating diagnostics",
        "arithmetic trace",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    ):
        assert phrase in text
