from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_multilevel_perron_archive_closes() -> None:
    data = load("multilevel_perron_grushin.json")
    assert data["status"] == (
        "rigorous_multilevel_exact_stored_euclidean_perron_factors"
    )
    assert set(data["levels"]) == {"2048", "4096", "8192"}
    for row in data["levels"].values():
        assert row["contour_ledger"]["rouche_count_one"]
        assert row["contour_ledger"]["contour_resolvent_upper"] < 66.0
        assert row["residual_two_upper"] < 4.0e-10


def test_rank_two_certificate_closes() -> None:
    data = load("validated_rank_two_peripheral_complement.json")
    assert data["status"] == (
        "rigorous_intrinsic_rank_two_peripheral_kernel_and_bulk_deflation"
    )
    assert data["contours"]["disjoint"]
    assert data["contours"]["union_inside_count"] == 2
    assert data["stored_perron_factor_validation"][
        "all_three_levels_are_actual_spectral_factors"
    ]
    assert data["stored_rank_two_haar_law"][
        "all_ratio_targets_within_one_thousandth"
    ]
    assert data["perron_continuum_contour"][
        "continuum_L2_resolvent_upper"
    ] < 82.0
    assert data["intrinsic_rank_two_kernel"]["rank"] == 2


def test_actual_rank_two_haar_ratios_are_spectral() -> None:
    data = load("validated_rank_two_peripheral_complement.json")
    ratios = data["stored_rank_two_haar_law"]["actual_spectral_ratios"]
    for name in ("coarse_consistency", "detail_block"):
        assert 0.249 < ratios[name]["lower"]
        assert ratios[name]["upper"] < 0.251
    for name in ("coarse_to_detail", "detail_to_coarse"):
        assert 0.499 < ratios[name]["lower"]
        assert ratios[name]["upper"] < 0.501


def test_uniform_rank_two_family_and_boundary() -> None:
    data = load("validated_rank_two_peripheral_complement.json")
    family = data["uniform_perron_and_rank_two_families"]
    assert family["certified_threshold_dimension"] == 65536
    assert family["uniform_union_contour_resolvent_upper"] < 268.0
    assert family["uniform_rank_two_weighted_riesz_cutoff_upper"] < 1.0e-9
    assert family[
        "uniform_rank_two_intrinsically_deflated_cutoff_upper"
    ] < 1.0e-9
    limitations = " ".join(data["limitations"]).lower()
    for phrase in (
        "fixed positive noise",
        "pointwise interval",
        "exact-real",
        "binary64",
        "row norm",
        "structural operator",
        "arithmetic trace",
        "prime-power",
        "zero-noise",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    ):
        assert phrase in limitations
