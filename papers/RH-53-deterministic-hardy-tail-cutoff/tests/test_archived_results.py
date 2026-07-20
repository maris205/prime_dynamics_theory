from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_five_scale_deterministic_full_energy_audit() -> None:
    rows = load("deterministic_tail_pilot.json")["rows"]
    assert [row["fine_dimension"] for row in rows] == [32, 64, 128, 256, 512]
    assert [row["left"]["horizon"] for row in rows] == [4, 8, 16, 24, 32]
    for row in rows:
        for side in ("left", "right"):
            data = row[side]
            assert data["block_power_norm"] < 0.04
            assert data["full_energy_upper"] >= data["exact_dense_energy"]
            assert data["relative_energy_excess"] < 5.0e-4
            assert data["selected_infinite_tail_upper"] > 0.0


def test_cutoff_ledger_separates_stored_and_asymptotic_claims() -> None:
    rows = load("deterministic_tail_pilot.json")["rows"]
    assert max(
        row["cutoff_bounds"][-1]["two_norm_upper"] for row in rows
    ) < 3.0e-14
    assert all(
        row["adaptive_cutoff"]["declared_multiple"] < 8.0 for row in rows
    )
    assert all(
        row["dense_full_kernel_comparison"] is not None for row in rows[:3]
    )
    assert all(
        row["dense_full_kernel_comparison"] is None for row in rows[3:]
    )


def test_arb_algorithm_is_real_but_not_the_production_execution() -> None:
    audit = load("arb_tail_audit.json")
    assert audit["certified_block_contraction"]
    assert not audit["production_matrix_interval_executed"]
    assert audit["dimension"] == 4
    assert "Arb" in audit["evidence_level"]


def test_production_cutoff_constants_are_arb_enclosures() -> None:
    audit = load("arb_production_cutoff_ledger.json")
    assert audit["precision_bits"] == 256
    assert audit["largest_dimension"] == 40960
    assert audit["maximum_fixed_eight_two_norm_upper"] < 5.7e-13
    assert audit["all_fixed_eight_above_adaptive_requirement"]


def test_external_hashes_match() -> None:
    data = load("deterministic_tail_pilot.json")
    for record in data["sources"].values():
        path = REPOSITORY / record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]


def test_certificate_keeps_stage_A3_boundary() -> None:
    data = load("hardy_tail_cutoff_certificate.json")
    conclusion = data["program_conclusion"]
    assert conclusion["deterministic_finite_matrix_tail_mechanism_closed"]
    assert conclusion["adaptive_exact_real_cutoff_route_closed"]
    assert not conclusion["production_scale_interval_trace_executed"]
    assert not conclusion["stage_A3_fully_closed"]
    assert not conclusion["stage_A1_uniform_trace_budget_closed"]
    assert not conclusion["stage_A4_intrinsic_identification_closed"]
