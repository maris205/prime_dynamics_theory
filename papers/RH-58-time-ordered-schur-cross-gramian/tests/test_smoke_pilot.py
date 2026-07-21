import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_pilot_has_two_dual_packet_levels() -> None:
    payload = json.loads(
        (ROOT / "results" / "schur_fusion_pilot_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"] == (
        "binary64_unitary_schur_packet_and_absolute_path_audit"
    )
    assert len(payload["rows"]) == 2
    assert payload["fits"]["left_state_block_upper"]["levels"] == 2
    assert payload["fits"]["right_state_block_upper"]["levels"] == 2

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
            assert channel["source_reconstruction_relative_defect"] < 1.0e-10
            assert channel["state_reconstruction_relative_defect"] < 1.0e-10
            assert (
                channel["primal_dual_energy_squared_relative_defect"]
                < 1.0e-10
            )
