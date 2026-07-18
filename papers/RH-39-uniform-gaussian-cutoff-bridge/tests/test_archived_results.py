from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_floating_pilot_obeys_tail_identity_and_analytic_bounds() -> None:
    pilot = load("cutoff_pilot_sigma_1e-02.json")
    assert pilot["status"] == "floating_full_versus_archived_cutoff_pilot"
    for row in pilot["dimensions"]:
        assert row["tail_identity_maximum_error"] < 1.0e-28
        assert row["maximum_omitted_mass"] < row["analytic_omitted_mass_upper"]
        assert row["frobenius_norm"] < row["analytic_two_norm_upper"]


def test_cutoff_certificate_closes_the_markov_gate_only() -> None:
    certificate = load("uniform_gaussian_cutoff_bridge_certificate.json")
    assert certificate["status"] == (
        "analytic_uniform_cutoff_bridge_with_arb_finite_grid_enclosures"
    )
    assert certificate["maximum_cutoff_upper_over_floating_markov_block"] < 4.0e-9
    assert certificate["fixed_eight_sigma_nonvanishing_limit"][
        "mean_zero_continuum_omitted_mass_lower"
    ] > 0.0
    assert certificate["schedule"]["eight_sigma_crossover_dimension_floor"] > 8_000_000
