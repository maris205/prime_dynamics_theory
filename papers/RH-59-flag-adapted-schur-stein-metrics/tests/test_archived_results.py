import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_pilot_localizes_the_remaining_loss_to_the_outer_packet() -> None:
    payload = load("flag_metric_pilot.json")
    assert len(payload["rows"]) == 5
    smallest = payload["rows"][-1]
    assert smallest["sigma"] == 0.01

    left = smallest["left"]
    right = smallest["right"]
    assert 15.0 < left["metric_absolute_upper"] < 25.0
    assert 10.0 < right["metric_absolute_upper"] < 15.0
    assert (
        left["inherited_rh58"]["scalar_path_upper"]
        / left["metric_absolute_upper"]
        > 90.0
    )
    assert (
        right["inherited_rh58"]["scalar_path_upper"]
        / right["metric_absolute_upper"]
        > 30.0
    )
    assert left["packets"][-1]["metric_upper_over_exact"] > 20.0
    assert right["packets"][-1]["metric_upper_over_exact"] > 5.0
    assert left["packets"][0]["metric_upper_over_exact"] < 1.01

    left_power = payload["fits"]["left_metric_absolute_upper"][
        "growth_exponent"
    ]
    right_power = payload["fits"]["right_metric_absolute_upper"][
        "growth_exponent"
    ]
    assert 0.8 < left_power < 1.0
    assert 0.7 < right_power < 0.9


def test_arb_certificate_is_positive_and_model_limited() -> None:
    payload = load("arb_flag_metric_audit.json")
    assert payload["precision_bits"] == 256
    assert payload["local_lyapunov_identities_certified"]
    assert payload["dissipation_positive_definite_certified"]
    assert payload["supersolution_positive_semidefinite_certified"]
    assert payload["packet_upper_certified"]
    assert not payload["production_interval_schur_metric_executed"]
