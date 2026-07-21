import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_pilot_has_two_positive_packet_metric_levels() -> None:
    payload = json.loads(
        (ROOT / "results" / "flag_metric_pilot_smoke.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["status"] == "binary64_packetwise_flag_metric_stein_audit"
    assert len(payload["rows"]) == 2

    for row in payload["rows"]:
        for side in ("left", "right"):
            channel = row[side]
            assert channel["metric_absolute_upper"] >= (
                channel["exact_hardy_energy"] * (1.0 - 1.0e-10)
            )
            assert channel["rh58_exact_relative_defect"] < 1.0e-10
            for packet in channel["packets"]:
                assert packet["metric_energy_upper"] >= (
                    packet["exact_packet_energy"] * (1.0 - 1.0e-10)
                )
                assert packet["minimum_dissipation_eigenvalue"] > 1.0e-8
                assert packet["minimum_supersolution_eigenvalue"] > -1.0e-9
                assert packet["optimizer"]["direct_success"]
