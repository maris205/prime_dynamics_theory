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
        "actual_completion_laws",
        "clock",
        "constants",
        "false_claims",
        "finite_minimax_witness",
        "finite_rows",
        "finite_rows_are_formula_reproduction_only",
        "gates",
        "phase_free_theorem",
        "rate_theorem",
        "scope",
        "source_anchors",
        "source_types",
        "status",
        "verdict",
    }


def test_actual_two_order_laws_and_gap_are_explicit():
    data = _result()
    laws = data["actual_completion_laws"]
    theorem = data["phase_free_theorem"]
    assert laws["critical"].startswith("C_M*Y_k^0")
    assert laws["first_lower"].startswith("C_M*Y_k^-")
    assert theorem["affine_gap"].startswith("Z_k^0-lambda")
    assert theorem["minimax_liminf"].endswith(">1/9")


def test_finite_rows_are_formula_reproduction_only():
    data = _result()
    assert data["finite_rows_are_formula_reproduction_only"] is True
    assert len(data["finite_rows"]) == 4
    assert all(row["finite_formula_only"] for row in data["finite_rows"])
    assert all(row["gap_identity_exact"] for row in data["finite_rows"])


def test_minimax_fixture_is_exact():
    witness = _result()["finite_minimax_witness"]
    assert witness["optimizer_gamma"] == "15/8"
    assert witness["minimax_value"] == "1/8"
    assert witness["critical_at_optimizer"] == "1/8"
    assert witness["first_lower_at_optimizer"] == "-1/8"
    assert witness["opposite_equal_errors"] is True


def test_direct_target_scale_claims_remain_false():
    claims = _result()["false_claims"]
    assert claims["critical_direct_o_H_proved"] is False
    assert claims["first_lower_direct_o_H_proved"] is False
    assert claims["full_E_off_decided"] is False


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
        ROOT / "critical-first-lower-actual-signed-completion-gap.pdf"
    ).read_bytes()
