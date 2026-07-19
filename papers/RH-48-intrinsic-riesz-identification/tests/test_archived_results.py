from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_archived_quadratic_schur_certificate() -> None:
    data = load("intrinsic_riesz_identification_certificate.json")
    assert data["status"] == (
        "rigorous_quadratic_schur_and_dyadic_reduction_with_directional_small_noise_gate"
    )
    assert not data["exact_schur_identification"][
        "global_full_resolvent_required"
    ]
    assert "quadratic" in data["exact_schur_identification"][
        "structural_order"
    ]
    assert data["dyadic_telescoping"]["quadratic_geometric_factor"] == 4.0 / 3.0
    closure = data["conditional_small_noise_closure"]
    assert closure["preserves_every_n_sigma_squared_schedule_when"] == (
        "gamma<=1/2"
    )
    assert not closure["unconditional_for_the_folded_gaussian_family_here"]


def test_archived_exact_haar_audit() -> None:
    data = load("intrinsic_riesz_identification_certificate.json")
    audit = data["floating_exact_haar_audit"]
    assert audit["noise_levels"] == 6
    assert audit["adjacent_defects"] == 18
    assert audit["largest_dimension"] == 204800
    assert audit["largest_nonzeros"] == 133873007
    assert abs(audit["joint_power_fit"]["dimension_power"] + 2.0) < 0.01
    assert abs(audit["joint_power_fit"]["sigma_power"] + 2.0) < 0.05
    assert audit["double_resolution_replay"][
        "maximum_relative_difference"
    ] < 2.0e-4
    assert not audit["candidate_law_is_a_theorem"]


def test_archived_directional_gate_stays_open() -> None:
    data = load("intrinsic_riesz_identification_certificate.json")
    reduced = data["residue_reduced_split"]
    assert not reduced["full_reduced_resolvent_upper_proved_here"]
    assert not reduced["directional_reduced_resolvent_upper_proved_here"]
    limitations = " ".join(data["limitations"]).lower()
    assert "riemann-hypothesis" in limitations
    assert "zeta-zero" in limitations
