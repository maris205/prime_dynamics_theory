import hashlib
import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic_and_schema_is_strict():
    data = _result()
    assert data == result_payload()
    assert set(data) == {
        "actual_consequences",
        "constants",
        "false_claims",
        "finite_formula_rows",
        "finite_identity_witness",
        "finite_rows_are_formula_reproduction_only",
        "gates",
        "growing_window",
        "route_coordinate_closed",
        "scope",
        "source_anchors",
        "source_bounds",
        "status",
        "uniform_rate_theorem",
        "unnormalized_barrier",
        "verdict",
    }


def test_result_locks_actual_coefficient_and_growing_order_scope():
    data = _result()
    assert data["uniform_rate_theorem"]["actual_direct_coefficient"] is True
    assert data["uniform_rate_theorem"]["growing_order_uniform"] is True
    assert data["growing_window"]["depth"] == "J_k->infinity_and_J_k=o(k)"
    assert data["scope"] == "actual_normalized_selected_lower_even_natural_scale_only"


def test_actual_consequences_and_small_Y_negative_are_explicit():
    actual = _result()["actual_consequences"]
    assert actual["normalized_direct_budget"].startswith("L_k^act->0_exponentially")
    assert actual["aggregate_positive_liminf"].endswith(">0")
    assert actual["rh350_small_Y_hypothesis"] == "false_for_actual_coefficients"


def test_unnormalized_barrier_is_not_promoted_to_a_verdict():
    barrier = _result()["unnormalized_barrier"]
    assert barrier["separate_noisy_majorant_root"].endswith(">1")
    assert barrier["actual_unnormalized_verdict"] == "open"
    assert _result()["false_claims"]["unnormalized_selected_prefix_vanishing_proved"] is False


def test_all_gates_and_forbidden_claims_remain_false():
    data = _result()
    assert len(data["gates"]) == 5
    assert not any(data["gates"].values())
    assert len(data["false_claims"]) == 15
    assert not any(data["false_claims"].values())


def test_finite_rows_are_formula_reproduction_only():
    data = _result()
    assert data["finite_rows_are_formula_reproduction_only"] is True
    assert [row["k"] for row in data["finite_formula_rows"]] == [64, 144, 256]
    assert all(row["finite_formula_reproduction_only"] for row in data["finite_formula_rows"])
    assert all(row["all_scale_conversions_exact"] for row in data["finite_formula_rows"])
    assert data["finite_identity_witness"]["physical_trace_observation"] is False


def test_dependency_manifest_rehashes_all_publication_files():
    manifest = json.loads(
        (ROOT / "results/dependency_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["file_count"] == 17
    assert len(manifest["files"]) == 17
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_individual_archive_verification_is_exact():
    verification = json.loads(
        (ROOT / "results/archive_verification.json").read_text(encoding="utf-8")
    )
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["file_count"] == 17


def test_semantic_pdf_is_byte_identical_to_main_pdf():
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "modulus-cap-forced-growing-ladder-signed-cancellation.pdf"
    ).read_bytes()
