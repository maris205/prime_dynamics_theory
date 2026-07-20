from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def branch(row, section: str, mode: str):
    return next(item for item in row[section] if item["mode"] == mode)


def test_five_scale_weak_factor_bounds() -> None:
    rows = load("factor_transfer_pilot.json")["rows"]
    assert len(rows) == 5
    assert rows[-1]["fine_dimension"] == 40960
    weak = [
        branch(
            row, "fine_factor_branches", "parity"
        )["weak_condition_product"]
        for row in rows
    ]
    assert max(weak) < 1.1
    assert min(weak) > 1.03
    assert all(
        abs(
            branch(row, "fine_factor_branches", "perron")[
                "weak_condition_product"
            ]
            - 1.0
        )
        < 1.0e-12
        for row in rows
    )


def test_sharp_details_and_two_sided_coupling_clocks_are_flat() -> None:
    rows = load("factor_transfer_pilot.json")["rows"]
    perron = [
        branch(row, "fine_factor_branches", "perron")[
            "left_detail_over_sharp_h_sigma_inverse"
        ]
        for row in rows
    ]
    parity = [
        branch(row, "fine_factor_branches", "parity")[
            "left_detail_over_sharp_h_sigma_inverse"
        ]
        for row in rows
    ]
    assert min(perron) > 0.039 and max(perron) < 0.045
    assert min(parity) > 0.046 and max(parity) < 0.056
    assert all(
        0.094 < row[
            "B_hilbert_schmidt_over_h_sigma_minus_three_halves"
        ] < 0.096
        for row in rows
    )
    assert all(
        0.167 < row[
            "C_hilbert_schmidt_over_h_sigma_minus_three_halves"
        ] < 0.168
        for row in rows
    )


def test_direct_residue_actions_vanish_with_archived_powers() -> None:
    data = load("factor_transfer_pilot.json")
    fits = data["fits"]
    assert 0.52 < fits["fine_perron_residue"]["vanishing_exponent"] < 0.54
    assert 0.54 < fits["fine_parity_residue"]["vanishing_exponent"] < 0.56
    assert 0.92 < fits["right_parity_residue"]["vanishing_exponent"] < 0.95
    for row in data["rows"]:
        assert branch(
            row, "coarse_right_residue_actions", "perron"
        )["right_residue_action_over_C_hilbert_schmidt"] < 3.0e-15


def test_adjacent_intrinsic_factors_are_stable() -> None:
    rows = load("factor_transfer_pilot.json")["rows"]
    parity = [
        branch(row, "adjacent_factor_transfer", "parity") for row in rows
    ]
    assert max(
        row["left_l1_normalized_adjacent_error"] for row in parity
    ) < 8.3e-5
    assert max(
        row["right_linf_normalized_adjacent_error"] for row in parity
    ) < 2.91e-4
    assert max(
        row["projector_relative_adjacent_defect"] for row in parity
    ) < 1.46e-4


def test_source_hashes_match() -> None:
    data = load("factor_transfer_pilot.json")
    for record in data["sources"].values():
        path = REPOSITORY / record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


def test_certificate_closes_only_the_sufficient_A2_gate() -> None:
    data = load("factor_transfer_certificate.json")
    closure = data["direct_residue_closure"]
    assert not closure["sharp_finite_detail_transfer_required"]
    assert not closure["finite_projector_polylog_upper_required"]
    barrier = data["sharp_detail_barrier"]
    assert not barrier["physical_sharp_transfer_proved_here"]
    conclusion = data["program_conclusion"]
    assert conclusion["stage_A2_sufficient_residue_gate_closed"]
    assert not conclusion[
        "stage_A2_original_sharp_sqrt_sigma_target_closed"
    ]
    assert not data["floating_five_scale_audit"]["interval_validated"]
