from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CERTIFICATES = (
    RESULTS / "exact_target_inertia_sigma_1e-2_op24.json",
    RESULTS / "exact_target_inertia_sigma_4e-3_op24.json",
    RESULTS / "exact_target_inertia_sigma_2e-3.json",
)


def test_three_archived_exact_target_inertia_certificates() -> None:
    expected_dimensions = {0.01: 4109, 0.004: 10255, 0.002: 20497}
    for path in CERTIFICATES:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["status"] == (
            "rigorous_exact_target_asymmetric_threshold_inertia_certificate"
        )
        assert data["exact_channel_enclosure"]
        sigma = float(data["sigma"])
        dimension = expected_dimensions[sigma]
        bracket = data["inertia_bracket"]
        assert bracket["admissible"]
        assert int(bracket["positive_count"]) == dimension
        assert int(bracket["negative_count"]) == dimension
        assert float(bracket["lower_shift_error_upper"]) < float(
            bracket["lower_shift"]
        )
        assert float(bracket["upper_shift_error_upper"]) < float(
            bracket["upper_shift"]
        )
        for row in data["shifted_factorizations"]:
            assert row["row_permutation_is_identity"]
            assert row["column_permutation_is_identity"]
            assert int(
                row["backward_error"]["elimination_operation_factor"]
            ) == 24


def test_summary_matches_archived_certificates() -> None:
    with (RESULTS / "threshold_inertia_summary.csv").open(
        encoding="utf-8"
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert [float(row["sigma"]) for row in rows] == [0.01, 0.004, 0.002]
    assert max(
        max(float(row["lower_utilization"]), float(row["upper_utilization"]))
        for row in rows
    ) < 1.0
    assert min(float(row["budget_margin_lower"]) for row in rows) > 1.99
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "three_exact_target_threshold_inertia_certificates"
    assert summary["maximum_shift_utilization"] < 1.0
    assert summary["minimum_budget_margin_lower"] > 1.99
