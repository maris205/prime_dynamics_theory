import hashlib
import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic_and_schema_is_strict():
    data = _result()
    assert data == result_payload()
    assert set(data) == {
        "batch_gate_values_expected_false",
        "discharged_actual_signed_remainder_count",
        "expected_batch_publication_files",
        "expected_batch_tree_files",
        "expected_review_publication_files",
        "expected_upstream_publication_files",
        "false_claims",
        "finite_rows_are_abstract_algebra_checks_only",
        "finite_witness_rows",
        "gates",
        "growing_window",
        "information_class_theorem",
        "layer_count",
        "layers",
        "open_obligation_count",
        "open_obligations",
        "paper_numbers",
        "proved_scoped_conclusion_count",
        "rh241_ancestry",
        "route_coordinate",
        "scope",
        "source_anchors",
        "status",
        "upstream_gate_values_expected_false",
        "verdict",
    }


def test_all_nine_upstream_gate_ledgers_are_false():
    names = (
        "RH-342-common-hardy-head-counterloop-rank-lock-obstruction",
        "RH-343-equal-rank-equal-mass-first-alias-underdetermination",
        "RH-344-complete-critical-boundary-orbit-atom-decomposition",
        "RH-345-double-alias-parity-phase-compensation-obstruction",
        "RH-346-complete-lower-sideband-boundary-orbit-decomposition",
        "RH-347-lower-sideband-scalar-balance-underdetermination",
        "RH-348-punctured-lower-even-boundary-orbit-ladder",
        "RH-349-two-lower-sideband-phase-incompatibility",
        "RH-350-growing-depth-lower-sideband-phase-incompatibility",
    )
    values = []
    for name in names:
        source = json.loads((PAPERS / name / "results/result.json").read_text())
        assert len(source["gates"]) == 5
        values.extend(source["gates"].values())
    assert len(values) == 45
    assert not any(values)
    assert _result()["batch_gate_values_expected_false"] == 50


def test_result_locks_growing_depth_information_class_scope():
    data = _result()
    assert data["route_coordinate"] == "actual_growing_lower_even_signed_remainder_open"
    assert data["growing_window"]["depth"] == "J_k->infinity_and_J_k=o(k)"
    theorem = data["information_class_theorem"]
    assert theorem["budget_exchange"].startswith("Yagg(close)=L(far)")
    assert theorem["far_positive_liminf"].endswith(">0")
    assert theorem["physical_realizability_claimed"] is False


def test_finite_rows_are_never_promoted_to_physical_evidence():
    data = _result()
    assert data["finite_rows_are_abstract_algebra_checks_only"] is True
    assert all(
        not row["physical_operator_constructed"]
        for row in data["finite_witness_rows"]
    )


def test_dependency_manifest_rehashes_all_publication_files():
    manifest = json.loads(
        (ROOT / "results/dependency_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["file_count"] == 19
    assert len(manifest["files"]) == 19
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_individual_and_batch_archive_verification_are_exact():
    individual = json.loads(
        (ROOT / "results/archive_verification.json").read_text(encoding="utf-8")
    )
    batch = json.loads(
        (ROOT / "results/batch_archive_verification.json").read_text(encoding="utf-8")
    )
    assert individual["failure_count"] == 0
    assert individual["failures"] == []
    assert individual["file_count"] == 19
    assert batch["failure_count"] == 0
    assert batch["failures"] == []
    assert batch["file_count"] == 154


def test_semantic_pdf_is_byte_identical_to_main_pdf():
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "ten-layer-signed-completion-frontier-review.pdf"
    ).read_bytes()
