from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_factor_pilot_reaches_small_noise() -> None:
    data = load("small_noise_peripheral_factor_pilot.json")
    assert data["status"] == (
        "floating_small_noise_peripheral_factor_conditioning_pilot"
    )
    assert len(data["rows"]) == 9
    smallest = data["rows"][-1]
    assert smallest["sigma"] == 1.0e-4
    assert smallest["dimension"] == 204800
    assert smallest["perron_projector_norm"] > 1.4
    assert smallest["parity_projector_norm"] > 1.35
    assert smallest["perron_contour_resolvent_lower"] > 28.0


def test_endpoint_coefficients_approach_analytic_tail() -> None:
    data = load("small_noise_peripheral_factor_pilot.json")
    expected = data["analytic_endpoint_tail_constant"]
    smallest = data["rows"][-1]
    assert abs(smallest["endpoint_perron_tail_coefficient"] - expected) < 0.02
    assert abs(smallest["endpoint_parity_tail_coefficient"] - expected) < 0.02


def test_log_fits_have_positive_slopes() -> None:
    data = load("small_noise_peripheral_factor_pilot.json")
    assert data["perron_log_fit"]["slope"] > 0.15
    assert data["parity_log_fit"]["slope"] > 0.12
    assert data["rank_two_log_fit"]["slope"] > 0.30


def test_main_certificate_marks_resolvent_obstruction() -> None:
    data = load("logarithmic_peripheral_conditioning_certificate.json")
    assert data["status"] == (
        "rigorous_logarithmic_peripheral_conditioning_anchored_bulk_mesh_and_intrinsic_identification_boundary"
    )
    conditioning = data["peripheral_conditioning_theorem"]
    assert conditioning["regular_variation_index"] == 0.0
    assert not conditioning["bounded_in_L2"]
    obstruction = data["resolvent_obstruction"]
    assert not obstruction["fixed_geometry_uniform_L2_resolvent"]
    assert obstruction["forced_lower_growth"] == (
        "Omega(sqrt(log(1/sigma)))"
    )


def test_anchored_bulk_closes_but_identification_remains_open() -> None:
    data = load("logarithmic_peripheral_conditioning_certificate.json")
    anchored = data["continuum_anchored_bulk"]
    assert anchored["critical_power"] == 2.0
    assert anchored["strict_power_condition"] == (
        "p>2 for n(sigma)~sigma^-p"
    )
    boundary = data["intrinsic_discrete_identification_boundary"]
    assert not boundary["controlled_here"]
    schedules = data["normalized_power_schedule_audit"]
    assert not schedules["2.0"]["square_trace_norm_converges"]
    assert schedules["2.25"]["square_trace_norm_converges"]


def test_theorem_boundaries_are_explicit() -> None:
    data = load("logarithmic_peripheral_conditioning_certificate.json")
    text = " ".join(data["limitations"]).lower()
    for phrase in (
        "from below",
        "reduced resolvent",
        "compressed continuum",
        "actual weighted riesz",
        "not proved",
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
