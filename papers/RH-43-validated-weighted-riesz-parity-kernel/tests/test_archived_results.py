from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_multilevel_grushin_archive_closes() -> None:
    data = load("multilevel_euclidean_grushin.json")
    assert data["status"] == (
        "rigorous_multilevel_exact_stored_euclidean_parity_factors"
    )
    assert set(data["levels"]) == {"2048", "4096", "8192"}
    for row in data["levels"].values():
        assert row["contour_ledger"]["rouche_count_one"]
        assert row["contour_ledger"]["contour_resolvent_upper"] < 85.0
        assert row["residual_two_upper"] < 4.0e-10


def test_actual_spectral_haar_ratios_are_validated() -> None:
    data = load("validated_weighted_parity_kernel.json")
    ratios = data["stored_parity_haar_law"]["actual_spectral_ratios"]
    for name in ("coarse_consistency", "detail_block"):
        assert 0.249 < ratios[name]["lower"]
        assert ratios[name]["upper"] < 0.251
    for name in ("coarse_to_detail", "detail_to_coarse"):
        assert 0.499 < ratios[name]["lower"]
        assert ratios[name]["upper"] < 0.501


def test_theorem_boundary_excludes_rank_two_and_zero_noise() -> None:
    data = load("validated_weighted_parity_kernel.json")
    limitations = " ".join(data["limitations"]).lower()
    for phrase in (
        "fixed positive noise",
        "perron",
        "rank-two",
        "zero-noise",
        "zeta-zero",
        "hilbert-polya",
        "riemann-hypothesis",
    ):
        assert phrase in limitations
