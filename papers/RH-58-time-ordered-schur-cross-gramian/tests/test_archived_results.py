import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_pilot_records_both_the_gain_and_the_route_obstruction() -> None:
    payload = load("schur_fusion_pilot.json")
    assert len(payload["rows"]) == 5
    assert payload["rows"][-1]["sigma"] == 0.01

    for row in payload["rows"]:
        for side in ("left", "right"):
            channel = row[side]
            exact = channel["exact_hardy_energy"]
            assert channel["source_packet_gram"]["coherence_upper"] >= (
                exact * (1.0 - 1.0e-10)
            )
            assert channel["state_block_gram"]["coherence_upper"] >= (
                exact * (1.0 - 1.0e-10)
            )
            assert channel["schur_partition"]["reconstruction_defect"] < 1.0e-10
            assert channel["cross_stein_recursion"]["maximum_residual_norm"] < (
                1.0e-10
            )

    smallest = payload["rows"][-1]
    assert smallest["left"]["source_packet_gram"]["coherence_upper"] < 2.0
    assert smallest["right"]["source_packet_gram"]["coherence_upper"] < 2.0
    assert smallest["left"]["scalar_path_majorant"]["energy_upper"] > 1000.0
    assert smallest["right"]["scalar_path_majorant"]["energy_upper"] > 300.0

    maximum_projector = max(
        smallest[side]["inherited_rh57_radial_riesz"][
            "maximum_projector_norm"
        ]
        for side in ("left", "right")
    )
    assert maximum_projector > 1000.0


def test_arb_certificate_is_explicitly_model_limited() -> None:
    payload = load("arb_schur_audit.json")
    assert payload["precision_bits"] == 256
    assert payload["all_recursion_residuals_contain_zero"]
    assert payload["primal_dual_identity_certified"]
    assert payload["path_majorant_certified"]
    assert not payload["production_interval_schur_executed"]
