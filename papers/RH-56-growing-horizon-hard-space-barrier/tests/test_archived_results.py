import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_strong_space_threshold_is_far_below_edge() -> None:
    pilot = load("results/hardy_barrier_pilot.json")
    threshold = pilot["strong_space_barrier"]["common_rate_threshold"]
    assert threshold < 0.28
    assert pilot["deterministic_edge_radius"] > 0.77
    assert pilot["extrema"]["edge_two_side_total_power"] > 1.25


def test_all_column_audit_keeps_energy_clock_small() -> None:
    pilot = load("results/hardy_barrier_pilot.json")
    assert len(pilot["all_column_dense_audit"]) == 5
    assert pilot["extrema"]["maximum_all_column_hardy_energy"] < 1.77
    assert pilot["extrema"]["maximum_all_column_energy_over_radial_clock"] < 1.10
    assert pilot["extrema"]["maximum_deterministic_tail_relative_excess"] < 5.0e-4


def test_certificate_preserves_route_boundary() -> None:
    certificate = load("results/hardy_barrier_certificate.json")
    barrier = certificate["black_box_barrier"]
    conclusion = certificate["program_conclusion"]
    assert barrier["does_not_claim_hardy_divergence"]
    assert conclusion["standard_global_strong_space_route_obstructed"]
    assert conclusion["directional_overlap_route_viable"]
    assert not conclusion["stage_A1_uniform_hardy_budget_closed"]
    assert not conclusion["stage_A4_unconditional_identification_closed"]


def test_arb_audit_is_scalar_only() -> None:
    audit = load("results/arb_hardy_barrier_ledger.json")
    assert audit["precision_bits"] == 256
    assert audit["threshold_below_point_two_eight_certified"]
    assert audit["edge_total_exceeds_quarter_certified"]
    assert not audit["production_operator_interval_eigensolver_executed"]


def test_arb_sector_resonance_closes_full_contour() -> None:
    audit = load("results/arb_sector_resonance_certificate.json")
    assert audit["precision_bits"] == 512
    assert audit["finite_eigenvalues_in_contour"] == 1
    assert audit["rate_lower_exceeds_r_to_eight_certified"]
    assert "0.077270" in audit["full_contour_perturbation_product_ball"]
    assert not audit["production_noisy_bulk_eigensolver_executed"]
