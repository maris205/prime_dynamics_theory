import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_pilot_shows_fixed_horizon_completion() -> None:
    payload = load("phase_tail_pilot.json")
    assert len(payload["rows"]) == 5
    assert payload["selected_horizon"] == 32
    smallest = payload["rows"][-1]
    assert smallest["sigma"] == 0.01

    for row in payload["rows"]:
        for side in ("left", "right"):
            channel = row[side]
            selected = channel["horizons"]["32"]
            assert channel["selected_phase_aware_upper"] >= (
                channel["exact_hardy_energy"] * (1.0 - 1.0e-9)
            )
            assert selected["phase_aware_upper"] == (
                channel["selected_phase_aware_upper"]
            )
            assert selected["finite_fused_energy"] + selected["tail_sum"] == (
                selected["phase_aware_upper"]
            )
            assert selected["finite_gram_minimum_eigenvalue"] > -1.0e-9

    assert smallest["left"]["selected_phase_aware_upper"] < 1.6
    assert smallest["right"]["selected_phase_aware_upper"] < 1.9
    assert (
        smallest["left"]["selected_phase_aware_upper_over_exact"] < 1.01
    )
    assert (
        smallest["right"]["selected_phase_aware_upper_over_exact"] < 1.01
    )
    assert smallest["left"]["horizons"]["32"]["tail_sum"] < 0.01
    assert smallest["right"]["horizons"]["32"]["tail_sum"] < 0.01

    left_power = payload["fits"]["left_phase_aware"]["growth_exponent"]
    right_power = payload["fits"]["right_phase_aware"]["growth_exponent"]
    assert 0.15 < left_power < 0.19
    assert 0.18 < right_power < 0.22


def test_arb_certificate_is_strict_and_model_limited() -> None:
    payload = load("arb_phase_tail_audit.json")
    assert payload["precision_bits"] == 256
    assert payload["local_lyapunov_identities_certified"]
    assert payload["dissipation_positive_definite_certified"]
    assert payload["supersolution_positive_definite_certified"]
    assert payload["tail_upper_certified"]
    assert payload["completion_upper_certified"]
    assert not payload["production_interval_audit_executed"]
