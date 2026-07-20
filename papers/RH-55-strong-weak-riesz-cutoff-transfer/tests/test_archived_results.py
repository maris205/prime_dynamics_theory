import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_archived_midpoint_ulam_scales() -> None:
    pilot = load("results/riesz_cutoff_pilot.json")
    rows = pilot["midpoint_ulam_audit"]
    assert [row["dimension"] for row in rows] == [32, 64, 128, 256]
    assert max(row["row_l1_over_h2_sigma_minus2"] for row in rows) < 0.43
    assert max(row["row_bv_over_h_sigma_minus2"] for row in rows) < 0.25


def test_inherited_factor_audit_and_hash() -> None:
    pilot = load("results/riesz_cutoff_pilot.json")
    rows = pilot["archived_intrinsic_factor_audit"]
    assert len(rows) == 15
    stress = [row for row in rows if row["declared_multiple"] == 5.0]
    assert len(stress) == 5
    assert max(row["actual_sum"] for row in stress) < 6.6e-8
    assert pilot["external_input"]["sha256"] == (
        "53e7a632480e2f1c0731f0b2028a5f5b1a64b7e524b11081da78f43e66f77c18"
    )


def test_certificate_keeps_theorem_boundary() -> None:
    certificate = load("results/riesz_cutoff_closure_certificate.json")
    conclusion = certificate["program_conclusion"]
    assert conclusion["adaptive_sparse_full_projector_modulus_closed"]
    assert conclusion["adaptive_sparse_full_weighted_riesz_modulus_closed"]
    assert conclusion["rh54_factor_aware_cutoff_premise_closed"]
    assert not conclusion["stage_A1_uniform_hardy_budget_closed"]
    assert not conclusion["stage_A4_unconditional_identification_closed"]
    assert not conclusion["production_intrinsic_riesz_interval_eigensolver_executed"]


def test_arb_formula_audit_is_not_a_production_eigensolver() -> None:
    audit = load("results/arb_riesz_cutoff_ledger.json")
    assert audit["precision_bits"] == 256
    assert audit["adaptive_schedule_audit"]["below_sqrt_sigma_certified"]
    assert not audit["production_intrinsic_riesz_interval_eigensolver_executed"]
