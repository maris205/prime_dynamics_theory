import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_closure_certificate_boundaries():
    data = load("intrinsic_identification_closure_certificate.json")
    conclusion = data["program_conclusion"]
    assert conclusion["normalized_coupling_gate_closed"]
    assert conclusion["factor_aware_finite_matrix_transfer_theorem_closed"]
    assert conclusion["growing_horizon_block_robustness_closed"]
    assert conclusion["conditional_RH48_to_RH53_composition_closed"]
    assert not conclusion["production_intrinsic_riesz_interval_enclosure_executed"]
    assert not conclusion["dyadically_uniform_riesz_conditioning_modulus_proved"]
    assert not conclusion["stage_A1_uniform_hardy_budget_closed"]
    assert not conclusion["stage_A3_fully_closed"]
    assert not conclusion["stage_A4_unconditional_identification_closed"]


def test_five_scale_stress_gates():
    data = load("factor_aware_transfer_pilot.json")
    assert [row["fine_dimension"] for row in data["rows"]] == [
        32,
        64,
        128,
        256,
        512,
    ]
    extrema = data["extrema"]
    assert extrema["all_factor_bounds_dominate_actual"]
    assert extrema["all_transferred_blocks_contract"]
    assert extrema["maximum_stress_markov_spectral_defect"] < 7.0e-8
    assert extrema["maximum_stress_block_margin_ratio"] < 3.4e-7
    for row in data["rows"]:
        for comparison in row["comparisons"]:
            for side in ("left", "right"):
                values = comparison[side]
                assert values["factor_bounds_dominate_actual"]
                assert values["transferred_block_norm_upper"] < 1.0
                assert values["actual_block_power_defect"] <= (
                    values["semigroup_telescope_upper"] * (1.0 + 1.0e-8)
                    + 1.0e-14
                )
                assert values["full_exact_hardy_energy"] <= (
                    values["transferred_full_energy_upper"]
                )


def test_arb_scope_and_gates():
    data = load("arb_factor_transfer_audit.json")
    assert data["precision_bits"] == 256
    assert data["normalization_premise_certified"]
    assert data["normalization_bound_certified"]
    assert data["transferred_block_contraction_certified"]
    assert not data["production_intrinsic_riesz_interval_executed"]
