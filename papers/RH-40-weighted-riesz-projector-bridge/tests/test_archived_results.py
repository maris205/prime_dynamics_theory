from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_projector_pilot_has_stable_isolated_peripheral_data() -> None:
    pilot = load("weighted_projector_pilot_sigma_1e-02.json")
    assert pilot["status"] == "floating_stored_weighted_peripheral_projector_pilot"
    assert pilot["parity_convergence"]["second_to_first_increment_ratio"] < 0.251
    assert pilot["parity_convergence"]["richardson_disagreement"] < 1.0e-9
    for level in pilot["levels"].values():
        assert level["biorthogonality_two_norm_defect"] < 5.0e-15
        assert level["parity_to_observed_bulk_radial_gap"] > 0.31


def test_exact_stored_frobenius_ledger_closes() -> None:
    certificate = load("weighted_riesz_projector_bridge_certificate.json")
    assert certificate["status"] == (
        "analytic_conditional_weighted_riesz_bridge_with_exact_stored_peripheral_ledger"
    )
    assert certificate["stored_ledger_closed"]
    ratios = certificate["exact_stored_frobenius_ratios"]
    assert ratios["coarse_consistency"]["upper"] < 0.251
    assert ratios["detail_block"]["upper"] < 0.251
    assert ratios["coarse_to_detail"]["upper"] < 0.501
    assert ratios["detail_to_coarse"]["upper"] < 0.501
    assert certificate["maximum_exact_stored_biorthogonality_upper"] < 1.0e-13
