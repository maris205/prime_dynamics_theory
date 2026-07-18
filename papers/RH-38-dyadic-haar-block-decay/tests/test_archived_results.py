from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_component_pilot_resolves_quarter_half_law() -> None:
    pilot = load("component_scaling_pilot_sigma_1e-02.json")
    assert pilot["status"] == "floating_componentwise_dyadic_scaling_pilot"
    exponents = {
        "coarse_consistency": 2,
        "coarse_to_detail": 1,
        "detail_to_coarse": 1,
        "detail_block": 2,
    }
    for rows in pilot["second_to_first_ratios"].values():
        for block, ratio in rows.items():
            assert abs(ratio - 2.0 ** (-exponents[block])) < 1.0e-3


def test_decay_certificate_closes() -> None:
    certificate = load("dyadic_haar_block_decay_certificate.json")
    assert certificate["status"] == (
        "analytic_quarter_half_law_with_closed_physical_scaling_ledger"
    )
    assert certificate["rigorous_scaling_ledger_closed"]
    assert certificate["all_four_components_follow_quarter_half_law"]
    assert max(certificate["renormalized_upper_spreads"].values()) < 1.001
    rates = certificate["analytic_rate_law"]
    assert rates["coarse_consistency"] == "O(h^2)"
    assert rates["coarse_to_detail"] == "O(h)"
    assert rates["detail_to_coarse"] == "O(h)"
    assert rates["detail_block"] == "O(h^2)"
