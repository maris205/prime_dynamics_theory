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
        "conditional_transport",
        "constants",
        "counterexample",
        "counterexample_fixture_rows",
        "counterloop_theorem",
        "diagnostic_constants",
        "diagnostic_rows",
        "exact_fixture_rows",
        "false_claims",
        "finite_rows_are_formula_reproduction_only",
        "gates",
        "normalized_weak_condition",
        "scope",
        "source_anchors",
        "source_types",
        "status",
        "terminal_fixture_rows",
        "verdict",
    }


def test_unconditional_counterloop_theorem_is_explicit():
    theorem = _result()["counterloop_theorem"]
    assert theorem["raw_asymptotic"].startswith("C_up~")
    assert theorem["normalized_asymptotic"].startswith("x^(-k)")
    assert theorem["normalized_kth_root"] == "x>1"
    assert theorem["terminal_share"] == "(x-1)/x"


def test_actual_transport_is_conditioned_on_original_unnormalized_leaf():
    data = _result()["conditional_transport"]
    assert data["hypothesis"].startswith("original_unnormalized_D_")
    assert data["hypothesis_is_proved_here"] is False
    assert data["uniform_even_relative_precision"] == "o(k*x^(-k))"
    assert data["terminal_relative_precision"] == "o(k*x^(-2k))"


def test_weak_normalized_condition_has_exact_scope():
    data = _result()["normalized_weak_condition"]
    assert data["aggregate_normalized_budget_transfer"] is True
    assert data["terminal_relative_precision"] == "o(k*x^(-k))"
    assert data["uniform_bandwise_relative_matching"] is False
    assert data["does_not_imply_unnormalized_D_4k"] is True


def test_counterexample_is_information_class_only():
    data = _result()["counterexample"]
    assert data["relative_error_at_N"] == "1"
    assert data["normalized_defect"].endswith("->0")
    assert data["unnormalized_defect"].endswith("->infinity")
    assert data["scope"] == "finite_conjugation_closed_normal_information_class_only"


def test_all_rows_are_reproduction_only():
    data = _result()
    assert data["finite_rows_are_formula_reproduction_only"] is True
    assert len(data["exact_fixture_rows"]) == 4
    assert len(data["terminal_fixture_rows"]) == 4
    assert len(data["counterexample_fixture_rows"]) == 4
    assert len(data["diagnostic_rows"]) == 4
    assert all(row["finite_formula_only"] for row in data["diagnostic_rows"])
    assert all(row["synthetic_multiplier_law"] for row in data["diagnostic_rows"])


def test_all_gates_and_forbidden_claims_remain_false():
    data = _result()
    assert len(data["gates"]) == 5
    assert not any(data["gates"].values())
    assert len(data["false_claims"]) == 14
    assert not any(data["false_claims"].values())


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
        ROOT / "upper-alias-counterloop-burden-and-head-transfer-precision.pdf"
    ).read_bytes()
