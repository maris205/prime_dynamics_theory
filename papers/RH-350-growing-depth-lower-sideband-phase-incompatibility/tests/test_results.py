import json
import hashlib
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic_and_schema_is_strict():
    data = _result()
    assert data == result_payload()
    assert set(data) == {
        "coefficient_identity",
        "conditional_conclusion",
        "constants",
        "false_claims",
        "finite_fixture",
        "finite_rows",
        "finite_rows_are_reproduction_checks_only",
        "gates",
        "index_family",
        "minimax_theorems",
        "route_boundary",
        "scope",
        "source_anchors",
        "status",
        "uniform_theorems",
        "verdict",
    }


def test_index_family_is_genuinely_growing_depth():
    index = _result()["index_family"]
    assert index["depth"] == "J_k->infinity_and_J_k=o(k)"
    assert index["eventual_RH348_membership"] is True


def test_exact_direct_type_preserves_the_actual_remainder():
    identity = _result()["coefficient_identity"]
    assert identity["direct"].startswith("p_(k,j)=")
    assert "-d_" in identity["actual_remainder"]
    assert identity["demand"].startswith("S_(k,j)=")


def test_both_uniform_scalar_laws_are_recorded_without_actual_Y_control():
    theorem = _result()["uniform_theorems"]
    assert theorem["demand"].startswith("sup_j_abs")
    assert theorem["parity"].startswith("sup_j_abs")
    assert theorem["actual_remainder_estimated"] is False


def test_relative_and_weighted_minimax_families_are_archived():
    theorem = _result()["minimax_theorems"]
    assert len(theorem["relative_rows"]) == 4
    assert len(theorem["weighted_rows"]) == 4
    assert theorem["weighted_optimizer"] == "a=1"
    assert theorem["weighted_limit"].endswith(">0")


def test_actual_aggregate_hypothesis_is_explicit_and_unproved():
    conclusion = _result()["conditional_conclusion"]
    assert conclusion["actual_aggregate_hypothesis"].endswith("->0")
    assert conclusion["hypothesis_proved"] is False
    assert conclusion["unconditional_conclusion"] is False


def test_finite_rows_are_formula_reproduction_only():
    data = _result()
    assert len(data["finite_rows"]) == 4
    assert data["finite_rows_are_reproduction_checks_only"] is True
    assert data["finite_fixture"]["remainder"] == "Y_(k,j)=0"


def test_claim_firewall_and_gates_remain_false():
    data = _result()
    assert len(data["false_claims"]) == 20
    assert not any(data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert not any(data["gates"].values())


def test_route_moves_only_to_the_ten_layer_review():
    route = _result()["route_boundary"]
    assert route["growing_deterministic_uniformity"] == "PROVED"
    assert route["actual_remainder_control"].startswith("NOT_TESTABLE")
    assert route["full_E_off"].startswith("NOT_TESTABLE")
    assert route["next_route"].startswith("RH-351")


def test_dependency_manifest_rehashes_all_publication_files():
    manifest = json.loads(
        (ROOT / "results/dependency_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["file_count"] == 15
    assert len(manifest["files"]) == 15
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_archive_verification_and_semantic_pdf_are_exact():
    verification = json.loads(
        (ROOT / "results/archive_verification.json").read_text(encoding="utf-8")
    )
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["file_count"] == 15
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "growing-depth-lower-sideband-phase-incompatibility.pdf"
    ).read_bytes()
