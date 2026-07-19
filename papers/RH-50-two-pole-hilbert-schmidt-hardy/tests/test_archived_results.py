from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def _load():
    return json.loads(
        (ROOT / "results" / "two_pole_hardy_pilot.json").read_text(
            encoding="utf-8"
        )
    )


def _load_certificate():
    return json.loads(
        (ROOT / "results" / "two_pole_hardy_certificate.json").read_text(
            encoding="utf-8"
        )
    )


def test_five_scale_hardy_energies_and_bulk_products_remain_flat() -> None:
    data = _load()
    assert len(data["rows"]) == 5
    assert data["rows"][-1]["fine_dimension"] == 40960
    assert data["fits"]["left_energy_r085"]["growth_exponent"] == 0.0
    assert data["fits"]["maximum_bulk_product"]["growth_exponent"] == 0.0
    assert data["fits"]["right_energy_r085"]["growth_exponent"] < 0.09
    assert max(
        row["hardy_energies"]["r=0.85"]["left_truncated_hardy_energy"]
        for row in data["rows"]
    ) < 1.7
    assert max(
        row["hardy_energies"]["r=0.85"]["right_truncated_hardy_energy"]
        for row in data["rows"]
    ) < 2.4


def test_tail_bases_track_the_two_pole_bulk_radius() -> None:
    data = _load()
    for row in data["rows"]:
        bulk = float(row["fine_bulk_radius_candidate"])
        assert abs(float(row["left_tail_fit"]["decay_base"]) - bulk) < 0.007
        assert abs(float(row["right_tail_fit"]["decay_base"]) - bulk) < 0.008
        assert row["left_power_gain_sequence"][-1] < 4.0e-9
        assert row["right_power_gain_sequence"][-1] < 1.5e-8


def test_directional_residue_actions_vanish() -> None:
    data = _load()
    first = data["rows"][0]["residue_action_ledgers"]
    last = data["rows"][-1]["residue_action_ledgers"]
    for index in (0, 1):
        assert last["fine_left"][index][
            "left_residue_action_over_B_hilbert_schmidt"
        ] < first["fine_left"][index][
            "left_residue_action_over_B_hilbert_schmidt"
        ]
    assert last["coarse_right"][0][
        "right_residue_action_over_C_hilbert_schmidt"
    ] < 1.0e-14
    assert last["coarse_right"][1][
        "right_residue_action_over_C_hilbert_schmidt"
    ] < 0.002


def test_archived_source_hash_matches() -> None:
    data = _load()
    source = data["source"]
    path = REPOSITORY / source["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]


def test_certificate_preserves_the_exact_conditional_boundary() -> None:
    data = _load_certificate()
    assert data["hardy_energy_theorem"]["condition"] == (
        "rho(N)<r<inf_(z in Gamma)|z|"
    )
    assert not data["stein_certificate"][
        "global_inverse_or_global_power_contraction_required"
    ]
    assert data["sharp_spike_derivative"]["law"] == (
        "||pi_sigma'||_2+||g_sigma'||_2=Theta(sigma^(-1))"
    )
    residue = data["fine_side_residue_suppression"]
    assert residue["compressed_continuum_detail_estimate_proved"]
    assert not residue[
        "dyadically_uniform_intrinsic_finite_factor_transfer_proved_here"
    ]
    assert not data["conditional_hilbert_schmidt_closure"][
        "premises_proved_for_full_small_noise_family_here"
    ]


def test_global_no_go_does_not_rule_out_directional_gramians() -> None:
    data = _load_certificate()["global_contraction_no_go"]
    assert "-> 1" in data["small_noise_consequence"]
    assert not data["directional_gramian_route_ruled_out"]
