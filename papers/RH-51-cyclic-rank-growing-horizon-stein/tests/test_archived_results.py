from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_five_scale_gramian_complexity_grows() -> None:
    data = load("structured_stein_pilot.json")
    rows = data["rows"]
    assert len(rows) == 5
    assert rows[-1]["fine_dimension"] == 512
    assert [
        row["left_gramian"]["rank_for_99_percent_trace"] for row in rows
    ] == [5, 9, 17, 35, 69]
    assert [
        row["right_gramian"]["rank_for_99_percent_trace"] for row in rows
    ] == [5, 9, 17, 33, 64]
    assert rows[-1]["left_gramian"]["participation_rank"] > 25.0
    assert rows[-1]["right_gramian"]["participation_rank"] > 16.0


def test_directional_cyclic_rank_is_extensive_at_the_stored_threshold() -> None:
    rows = load("structured_stein_pilot.json")["rows"]
    terminal = [
        row["left_cyclic_rank_profile"][-1]["numerical_rank"]
        for row in rows
    ]
    assert terminal == [22, 43, 84, 165, 322]
    for row in rows[1:]:
        fraction = row["left_cyclic_rank_profile"][-1]["rank_fraction"]
        assert 0.62 < fraction < 0.68


def test_growing_horizon_block_completion_is_sharp() -> None:
    rows = load("structured_stein_pilot.json")["rows"]
    assert [
        row["left_block_completion"]["selected_horizon"] for row in rows
    ] == [4, 8, 16, 24, 32]
    assert [
        row["right_block_completion"]["selected_horizon"] for row in rows
    ] == [4, 8, 16, 24, 32]
    for row in rows:
        left = row["left_block_completion"]
        right = row["right_block_completion"]
        assert left["selected_power_norm"] < 0.04
        assert right["selected_power_norm"] < 0.04
        assert left["energy_upper"] / row["left_exact_hardy_energy"] - 1.0 < 7.0e-4
        assert right["energy_upper"] / row["right_exact_hardy_energy"] - 1.0 < 8.0e-4
        assert left["block_defect_minimum_eigenvalue"] > -1.0e-10
        assert right["block_defect_minimum_eigenvalue"] > -1.0e-10


def test_simple_metric_shortcuts_fail_on_the_stored_family() -> None:
    rows = load("structured_stein_pilot.json")["rows"]
    assert sum(
        row["identity_metric"]["scalar_identity_cone_obstructed"]
        for row in rows
    ) == 4
    assert all(
        not row["diagonal_of_exact_gramian"]["is_a_supersolution"]
        for row in rows
    )
    identity_minima = [
        row["identity_metric"]["minimum_unforced_defect_eigenvalue"]
        for row in rows
    ]
    assert identity_minima[-1] < -4.5


def test_external_source_hashes_match() -> None:
    data = load("structured_stein_pilot.json")
    for record in data["sources"].values():
        path = REPOSITORY / record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


def test_certificate_keeps_the_exact_boundary() -> None:
    data = load("structured_stein_certificate.json")
    assert data["minimal_gramian"]["minimality"] == (
        "H>=0 and H-A H A^*>=X X^* imply H>=G"
    )
    assert not data["cyclic_rank_obstruction"][
        "physical_divergence_proved_analytically_here"
    ]
    assert data["block_stein"]["horizon_may_grow_with_noise_or_dimension"]
    assert not data["block_stein"]["fixed_rank_obstruction_removed"]
    assert not data["program_conclusion"]["stage_A1_closed"]
    assert not data["floating_five_scale_audit"]["interval_validated"]
    assert "independent TPC" in " ".join(data["limitations"])
