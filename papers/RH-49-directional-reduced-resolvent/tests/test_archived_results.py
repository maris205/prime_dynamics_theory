from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def _load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def _fit_gamma(sigmas, values) -> float:
    slope, _ = np.polyfit(np.log(sigmas), np.log(values), 1)
    return float(max(0.0, -slope))


def test_stable_rank_audit_resolves_the_quarter_power() -> None:
    data = _load("coupling_stable_rank_pilot.json")
    fits = data["fits"]
    assert 0.47 < fits["B_hilbert_schmidt_norm"]["growth_exponent"] < 0.52
    assert 0.23 < fits["B_operator_candidate"]["growth_exponent"] < 0.27
    assert 0.23 < fits["B_sqrt_stable_rank_candidate"]["growth_exponent"] < 0.27
    assert 0.48 < fits["C_sqrt_stable_rank_candidate"]["growth_exponent"] < 0.52
    assert (
        fits["minimum_sqrt_stable_rank_candidate"]["maximum_log_residual"]
        < 2.0e-3
    )


def test_hilbert_schmidt_directional_products_remain_flat() -> None:
    data = _load("reduced_directional_pilot.json")
    sigmas = [float(row["sigma"]) for row in data["rows"]]
    reduced = []
    full = []
    for row in data["rows"]:
        reduced.append(
            sum(
                float(branch["maximum_left_reduced_frobenius_gain"])
                * float(branch["maximum_right_reduced_frobenius_gain"])
                for branch in row["branches"].values()
            )
        )
        full.append(
            sum(
                float(branch["maximum_left_full_frobenius_gain"])
                * float(branch["maximum_right_full_frobenius_gain"])
                for branch in row["branches"].values()
            )
        )
    assert _fit_gamma(sigmas, reduced) < 0.08
    assert _fit_gamma(sigmas, full) == 0.0
    assert max(full[-3:]) < 4.3


def test_direct_mixed_candidates_stay_below_the_quarter_power() -> None:
    data = _load("mixed_operator_gain_pilot.json")
    sigmas = [float(row["sigma"]) for row in data["rows"]]
    combined = [
        sum(
            float(branch["mixed_directional_product_candidate"])
            for branch in row["branches"].values()
        )
        for row in data["rows"]
    ]
    assert _fit_gamma(sigmas, combined) < 0.20
    assert _fit_gamma(sigmas[-3:], combined[-3:]) < 0.13
    for row in data["rows"]:
        for branch in row["branches"].values():
            assert float(branch["maximum_gmres_relative_residual"]) < 2.1e-10
            assert float(branch["maximum_branch_leakage"]) < 4.0e-13


def test_archived_source_hashes_match() -> None:
    for name in (
        "reduced_directional_pilot.json",
        "mixed_operator_gain_pilot.json",
        "coupling_stable_rank_pilot.json",
    ):
        data = _load(name)
        source = data["source"]
        path = REPOSITORY / source["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]
